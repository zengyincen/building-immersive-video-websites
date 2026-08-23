#!/usr/bin/env python3
"""Assemble ordered image-to-image video bridges into one persistent master film.

The input manifest describes an ordered source list and one local video bridge for
each adjacent pair.  Individual bridge files are intermediate assets only: the
script writes one ``master-background-film.mp4`` and an assembly manifest that a
website can mount as its sole background video.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


class AssembleError(RuntimeError):
    """A user-actionable assembly failure."""

    def __init__(self, code: str, message: str, **details):
        super().__init__(message)
        self.code = code
        self.details = details


def emit(payload: dict, exit_code: int) -> int:
    stream = sys.stdout if exit_code == 0 else sys.stderr
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), file=stream)
    return exit_code


def resolve_tool(value: str | None, name: str) -> str:
    candidate = value or shutil.which(name)
    if not candidate:
        raise AssembleError(f"{name}_not_found", f"{name} is required to assemble a master video")
    resolved = Path(candidate).expanduser()
    if resolved.is_file():
        return str(resolved.resolve())
    located = shutil.which(candidate)
    if located:
        return located
    raise AssembleError(f"{name}_not_found", f"{name} is required to assemble a master video", requested=str(candidate))


def read_manifest(path: Path) -> tuple[dict, list[dict], list[dict]]:
    if not path.is_file():
        raise AssembleError("manifest_not_found", "Input manifest was not found", path=str(path))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AssembleError("manifest_invalid", "Input manifest is not valid JSON", path=str(path)) from exc
    if not isinstance(data, dict):
        raise AssembleError("manifest_invalid", "Input manifest must be a JSON object", path=str(path))

    sources = data.get("orderedSources") or data.get("sources") or data.get("images")
    segments = data.get("segments") or data.get("bridges")
    if not isinstance(sources, list) or len(sources) < 2:
        raise AssembleError(
            "ordered_sources_required",
            "Manifest must contain at least two orderedSources (or sources/images)",
        )
    if not isinstance(segments, list) or len(segments) != len(sources) - 1:
        raise AssembleError(
            "adjacent_bridges_required",
            "Provide exactly one video bridge for every adjacent source pair",
            expected=len(sources) - 1,
            received=len(segments) if isinstance(segments, list) else None,
        )

    normalized_sources: list[dict] = []
    source_ids: list[str] = []
    for index, source in enumerate(sources, start=1):
        if isinstance(source, str):
            source = {"id": f"image-{index:02d}", "path": source}
        if not isinstance(source, dict):
            raise AssembleError("source_invalid", "Each ordered source must be an object or path string", index=index)
        source_id = str(source.get("id") or source.get("name") or f"image-{index:02d}")
        if source_id in source_ids:
            raise AssembleError("source_id_duplicate", "Ordered source IDs must be unique", id=source_id)
        source_ids.append(source_id)
        normalized_sources.append({**source, "id": source_id})

    normalized_segments: list[dict] = []
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict):
            raise AssembleError("segment_invalid", "Each bridge must be an object", index=index)
        expected_from, expected_to = source_ids[index], source_ids[index + 1]
        from_id = str(segment.get("from") or segment.get("fromId") or "")
        to_id = str(segment.get("to") or segment.get("toId") or "")
        if from_id != expected_from or to_id != expected_to:
            raise AssembleError(
                "segment_order_mismatch",
                "Bridge order must match adjacent orderedSources exactly",
                index=index,
                expectedFrom=expected_from,
                expectedTo=expected_to,
                receivedFrom=from_id or None,
                receivedTo=to_id or None,
            )
        raw_path = segment.get("path") or segment.get("src") or segment.get("video")
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise AssembleError("segment_path_required", "Every bridge needs a local path or src", index=index)
        if raw_path.startswith(("http://", "https://", "data:")):
            raise AssembleError("segment_must_be_local", "Bridge files must be downloaded to a durable local path", path=raw_path)
        segment_path = (path.parent / raw_path).resolve() if not Path(raw_path).is_absolute() else Path(raw_path).resolve()
        if not segment_path.is_file():
            raise AssembleError("segment_not_found", "Bridge video was not found", index=index, path=str(segment_path))
        normalized_segments.append({**segment, "from": from_id, "to": to_id, "path": str(segment_path)})

    return data, normalized_sources, normalized_segments


def parse_number(value, label: str, path: Path) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise AssembleError("probe_invalid", f"ffprobe returned an invalid {label}", path=str(path), value=value) from exc
    if number <= 0:
        raise AssembleError("probe_invalid", f"ffprobe returned a non-positive {label}", path=str(path), value=value)
    return number


def parse_rate(value, path: Path) -> float:
    if isinstance(value, str) and "/" in value:
        numerator, denominator = value.split("/", 1)
        try:
            result = float(numerator) / float(denominator)
        except (ValueError, ZeroDivisionError) as exc:
            raise AssembleError("probe_invalid", "ffprobe returned an invalid frame rate", path=str(path), value=value) from exc
    else:
        result = parse_number(value, "frame rate", path)
    if result <= 0:
        raise AssembleError("probe_invalid", "ffprobe returned a non-positive frame rate", path=str(path), value=value)
    return result


def probe(path: Path, ffprobe: str) -> dict:
    command = [
        ffprobe,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=codec_name,width,height,avg_frame_rate,duration:format=duration",
        "-of", "json",
        str(path),
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=True)
        payload = json.loads(completed.stdout)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        detail = getattr(exc, "stderr", "")
        raise AssembleError("probe_failed", "Could not decode a bridge video with ffprobe", path=str(path), detail=detail[-1000:]) from exc
    streams = payload.get("streams") or []
    stream = next((item for item in streams if item.get("codec_type", "video") == "video"), None)
    if not stream:
        raise AssembleError("probe_invalid", "Bridge has no video stream", path=str(path))
    duration = stream.get("duration") or (payload.get("format") or {}).get("duration")
    width = stream.get("width")
    height = stream.get("height")
    codec = stream.get("codec_name")
    if not codec or not width or not height or not duration:
        raise AssembleError("probe_invalid", "Bridge is missing required video metadata", path=str(path))
    return {
        "path": str(path),
        "durationSeconds": parse_number(duration, "duration", path),
        "width": int(width),
        "height": int(height),
        "codec": codec,
        "fps": parse_rate(stream.get("avg_frame_rate") or stream.get("r_frame_rate") or 30, path),
    }


def format_fps(value: float) -> str:
    # A short decimal is accepted by ffmpeg and keeps the generated command readable.
    return f"{value:.6f}".rstrip("0").rstrip(".")


def build_filter(probes: list[dict], width: int, height: int, fps: float, transition: float) -> tuple[str, str, list[float]]:
    parts = []
    for index in range(len(probes)):
        parts.append(
            f"[{index}:v]scale={width}:{height}:force_original_aspect_ratio=increase," \
            f"crop={width}:{height},fps={format_fps(fps)}," \
            "format=yuv420p,setsar=1,settb=AVTB,setpts=PTS-STARTPTS[v" + str(index) + "]"
        )
    accumulated = probes[0]["durationSeconds"]
    current_label = "v0"
    boundaries: list[float] = [0.0]
    for index in range(1, len(probes)):
        output_label = f"xf{index}"
        offset = max(0.0, accumulated - transition)
        parts.append(
            f"[{current_label}][v{index}]xfade=transition=fade:duration={format_fps(transition)}:offset={format_fps(offset)}," \
            f"format=yuv420p,setsar=1,settb=AVTB,setpts=PTS-STARTPTS[{output_label}]"
        )
        current_label = output_label
        accumulated += probes[index]["durationSeconds"] - transition
        boundaries.append(offset)
    return ";".join(parts), current_label, boundaries


def run_ffmpeg(command: list[str]) -> None:
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", "")
        raise AssembleError("assembly_failed", "ffmpeg could not assemble the master background film", detail=detail[-2000:]) from exc
    if completed.returncode != 0:  # defensive for mocked subprocess implementations
        raise AssembleError("assembly_failed", "ffmpeg could not assemble the master background film", detail=completed.stderr[-2000:])


def assemble(input_manifest: Path, output: Path, output_manifest: Path, ffmpeg: str, ffprobe: str, transition: float, width: int | None, height: int | None, fps: float | None) -> dict:
    original, sources, segments = read_manifest(input_manifest)
    if transition <= 0:
        raise AssembleError("transition_invalid", "Transition duration must be greater than zero")

    probes = [probe(Path(segment["path"]), ffprobe) for segment in segments]
    for index, item in enumerate(probes):
        if item["durationSeconds"] <= transition:
            raise AssembleError(
                "segment_too_short",
                "Every bridge must be longer than the requested transition",
                index=index,
                durationSeconds=item["durationSeconds"],
                transitionSeconds=transition,
            )
    target_width = width or probes[0]["width"]
    target_height = height or probes[0]["height"]
    target_fps = fps or probes[0]["fps"]
    if target_width <= 0 or target_height <= 0 or target_fps <= 0:
        raise AssembleError("output_format_invalid", "Output width, height, and fps must be positive")

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output_manifest = output_manifest.resolve()
    output_manifest.parent.mkdir(parents=True, exist_ok=True)
    filter_graph, output_label, boundaries = build_filter(probes, int(target_width), int(target_height), float(target_fps), transition)
    command = [ffmpeg, "-y"]
    for segment in segments:
        command += ["-i", segment["path"]]
    command += [
        "-filter_complex", filter_graph,
        "-map", f"[{output_label}]",
        "-an",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output),
    ]
    run_ffmpeg(command)
    if not output.is_file() or output.stat().st_size == 0:
        raise AssembleError("output_missing", "ffmpeg completed without writing a master video", path=str(output))
    output_probe = probe(output, ffprobe)
    total_duration = sum(item["durationSeconds"] for item in probes) - transition * (len(probes) - 1)
    segment_boundaries = []
    cursor = 0.0
    for index, (segment, item) in enumerate(zip(segments, probes)):
        start = 0.0 if index == 0 else boundaries[index]
        end = cursor + item["durationSeconds"]
        segment_boundaries.append({
            "id": segment.get("id") or f"bridge-{index + 1:02d}",
            "from": segment["from"],
            "to": segment["to"],
            "source": segment["path"],
            "startSeconds": round(start, 6),
            "endSeconds": round(min(end, total_duration), 6),
            "transitionSeconds": transition if index < len(probes) - 1 else 0.0,
        })
        cursor += item["durationSeconds"] - (transition if index < len(probes) - 1 else 0.0)

    relative_output = os.path.relpath(output, input_manifest.parent.resolve()).replace(os.sep, "/")
    if not relative_output.startswith("."):
        relative_output = f"./{relative_output}"
    result = {
        "ok": True,
        "masterBackgroundVideo": {
            "src": relative_output,
            "path": str(output),
            "role": "persistent-background-video",
            "background": True,
            "interaction": "persistent-ambient-background",
            "orderedSources": sources,
            "segments": [{**segment, "path": segment["path"]} for segment in segments],
            "segmentBoundaries": segment_boundaries,
            "transitionSeconds": transition,
            "durationSeconds": output_probe["durationSeconds"],
            "width": output_probe["width"],
            "height": output_probe["height"],
            "fps": target_fps,
            "codec": output_probe["codec"],
        },
        "output": str(output),
        "outputManifest": str(output_manifest),
        "ffmpeg": ffmpeg,
        "ffprobe": ffprobe,
        "assembly": {
            "inputManifest": str(input_manifest.resolve()),
            "command": command,
            "sourceCount": len(sources),
            "segmentCount": len(segments),
            "totalDurationSeconds": round(total_duration, 6),
        },
    }
    output_manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON manifest with orderedSources and adjacent bridge segments")
    parser.add_argument("--output", type=Path, default=Path("public/media/master-background-film.mp4"))
    parser.add_argument("--output-manifest", type=Path)
    parser.add_argument("--transition", type=float, default=0.8, help="Crossfade duration in seconds")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--fps", type=float)
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    args = parser.parse_args(argv)
    output_manifest = args.output_manifest or args.output.with_name("master-background-film.manifest.json")
    try:
        ffmpeg = resolve_tool(args.ffmpeg, "ffmpeg")
        ffprobe = resolve_tool(args.ffprobe, "ffprobe")
        result = assemble(
            args.manifest.resolve(),
            args.output,
            output_manifest,
            ffmpeg,
            ffprobe,
            args.transition,
            args.width,
            args.height,
            args.fps,
        )
    except AssembleError as exc:
        return emit({"ok": False, "error": exc.code, "message": str(exc), **exc.details}, 1)
    return emit(result, 0)


if __name__ == "__main__":
    sys.exit(main())
