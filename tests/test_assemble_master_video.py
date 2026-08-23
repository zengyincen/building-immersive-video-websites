import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "assemble-master-video.py"


FAKE_FFPROBE = """#!/usr/bin/env python3
import json
from pathlib import Path
path = Path(__import__('sys').argv[-1])
duration = '4.000000'
if 'master-background-film' in path.name:
    duration = '7.000000'
print(json.dumps({'streams': [{'codec_type': 'video', 'codec_name': 'h264', 'width': 640, 'height': 360, 'duration': duration, 'avg_frame_rate': '24/1'}], 'format': {'duration': duration}}))
"""


FAKE_FFMPEG = """#!/usr/bin/env python3
from pathlib import Path
import sys
args = sys.argv[1:]
output = Path(args[-1])
output.parent.mkdir(parents=True, exist_ok=True)
output.write_bytes(b'fake-master-film')
"""


class AssembleMasterVideoTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.manifest = self.root / "bridges.json"
        self.segment_a = self.root / "image-01-to-image-02.mp4"
        self.segment_b = self.root / "image-02-to-image-03.mp4"
        self.segment_a.write_bytes(b"segment-a")
        self.segment_b.write_bytes(b"segment-b")
        self.ffprobe = self.root / "fake-ffprobe"
        self.ffmpeg = self.root / "fake-ffmpeg"
        self.ffprobe.write_text(FAKE_FFPROBE, encoding="utf-8")
        self.ffmpeg.write_text(FAKE_FFMPEG, encoding="utf-8")
        for tool in (self.ffprobe, self.ffmpeg):
            tool.chmod(tool.stat().st_mode | stat.S_IXUSR)

    def tearDown(self):
        self.tempdir.cleanup()

    def write_manifest(self, segments=None):
        self.manifest.write_text(json.dumps({
            "orderedSources": [
                {"id": "image-01", "path": "image-01.png"},
                {"id": "image-02", "path": "image-02.png"},
                {"id": "image-03", "path": "image-03.png"},
            ],
            "segments": segments if segments is not None else [
                {"id": "bridge-01", "from": "image-01", "to": "image-02", "src": self.segment_a.name},
                {"id": "bridge-02", "from": "image-02", "to": "image-03", "src": self.segment_b.name},
            ],
        }), encoding="utf-8")

    def run_cli(self, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.manifest), "--ffmpeg", str(self.ffmpeg), "--ffprobe", str(self.ffprobe), *extra],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def test_no_input_is_rejected(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode)

    def test_missing_segment_is_rejected(self):
        self.write_manifest([{"from": "image-01", "to": "image-02", "src": "missing.mp4"}, {"from": "image-02", "to": "image-03", "src": self.segment_b.name}])
        result = self.run_cli()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("segment_not_found", json.loads(result.stderr)["error"])

    def test_order_mismatch_is_rejected(self):
        self.write_manifest([{"from": "image-02", "to": "image-03", "src": self.segment_a.name}, {"from": "image-01", "to": "image-02", "src": self.segment_b.name}])
        result = self.run_cli()
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("segment_order_mismatch", json.loads(result.stderr)["error"])

    def test_missing_ffmpeg_is_reported(self):
        self.write_manifest()
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.manifest), "--ffmpeg", str(self.root / "not-installed"), "--ffprobe", str(self.ffprobe)], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual("ffmpeg_not_found", json.loads(result.stderr)["error"])

    def test_assembly_writes_one_master_and_manifest(self):
        self.write_manifest()
        output = self.root / "public" / "media" / "master-background-film.mp4"
        assembly_manifest = self.root / "public" / "media" / "master-background-film.manifest.json"
        result = self.run_cli("--output", str(output), "--output-manifest", str(assembly_manifest), "--transition", "1")
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        persisted = json.loads(assembly_manifest.read_text(encoding="utf-8"))
        self.assertTrue(output.is_file())
        self.assertTrue(payload["ok"])
        self.assertEqual("./public/media/master-background-film.mp4", payload["masterBackgroundVideo"]["src"])
        self.assertEqual(2, len(payload["masterBackgroundVideo"]["segments"]))
        self.assertEqual(2, payload["assembly"]["segmentCount"])
        self.assertEqual(payload["output"], persisted["output"])
        self.assertNotIn("image-01.mp4", payload["masterBackgroundVideo"]["src"])


if __name__ == "__main__":
    unittest.main()
