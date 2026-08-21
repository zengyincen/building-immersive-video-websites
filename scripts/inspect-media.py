#!/usr/bin/env python3
"""Report normalized local-media metadata using ffprobe."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


IMAGE_EXTENSIONS = {".avif", ".bmp", ".gif", ".heic", ".jpeg", ".jpg", ".png", ".svg", ".tif", ".tiff", ".webp"}
VIDEO_EXTENSIONS = {".avi", ".m4v", ".mkv", ".mov", ".mp4", ".mpeg", ".mpg", ".webm"}


def emit(payload, exit_code):
    print(json.dumps(payload, separators=(",", ":")))
    return exit_code


def number_or_none(value):
    try:
        return float(value) if value not in (None, "", "N/A") else None
    except (TypeError, ValueError):
        return None


def classify(path, video_stream, format_name):
    extension = path.suffix.lower()
    if extension in IMAGE_EXTENSIONS:
        return "image"
    if video_stream or extension in VIDEO_EXTENSIONS or "video" in (format_name or "").lower():
        return "video"
    return "image"


def inspect(path, ffprobe):
    try:
        completed = subprocess.run(
            [ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
            capture_output=True,
            text=True,
            check=True,
        )
        probe = json.loads(completed.stdout)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError):
        return None

    streams = probe.get("streams", [])
    video_stream = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    format_data = probe.get("format", {})
    format_name = format_data.get("format_name")
    duration = number_or_none((video_stream or {}).get("duration"))
    if duration is None:
        duration = number_or_none(format_data.get("duration"))
    codec = (video_stream or {}).get("codec_name")
    kind = classify(path, video_stream, format_name)
    readiness = "needs_browser_test"
    if duration is None or not codec or not video_stream:
        readiness = "warning"

    return {
        "ok": True,
        "kind": kind,
        "path": str(path),
        "sizeBytes": path.stat().st_size,
        "durationSeconds": duration,
        "width": (video_stream or {}).get("width"),
        "height": (video_stream or {}).get("height"),
        "codec": codec,
        "format": format_name,
        "scrubReadiness": readiness,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--ffprobe")
    args = parser.parse_args(argv)
    path = args.path.resolve()

    if not path.is_file():
        return emit({"ok": False, "error": "file_not_found", "path": str(path)}, 2)

    ffprobe = args.ffprobe or shutil.which("ffprobe")
    if not ffprobe or not Path(ffprobe).is_file():
        return emit({"ok": False, "error": "ffprobe_not_found", "path": str(path)}, 3)

    payload = inspect(path, ffprobe)
    if payload is None:
        return emit({"ok": False, "error": "probe_failed", "path": str(path)}, 4)
    return emit(payload, 0)


if __name__ == "__main__":
    sys.exit(main())
