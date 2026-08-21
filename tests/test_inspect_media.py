import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSPECTOR = ROOT / "scripts" / "inspect-media.py"


class InspectMediaTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.video_path = self.root / "video.mp4"
        self.video_path.write_bytes(b"not-empty")
        self.fake_ffprobe = ROOT / "tests" / "fixtures" / "fake-ffprobe.py"

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_inspector(self, path, ffprobe):
        return subprocess.run(
            [sys.executable, str(INSPECTOR), str(path), "--ffprobe", str(ffprobe)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_video_metadata_is_normalized(self):
        result = self.run_inspector(self.video_path, self.fake_ffprobe)
        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual("video", payload["kind"])
        self.assertEqual(1920, payload["width"])
        self.assertEqual(1080, payload["height"])
        self.assertEqual(8.0, payload["durationSeconds"])
        self.assertEqual("h264", payload["codec"])

    def test_missing_file_returns_exit_two(self):
        result = self.run_inspector(self.root / "missing.mp4", self.fake_ffprobe)
        self.assertEqual(2, result.returncode)
        self.assertEqual("file_not_found", json.loads(result.stdout)["error"])

    def test_missing_ffprobe_returns_exit_three(self):
        result = self.run_inspector(self.video_path, self.root / "absent-ffprobe")
        self.assertEqual(3, result.returncode)
        self.assertEqual("ffprobe_not_found", json.loads(result.stdout)["error"])


if __name__ == "__main__":
    unittest.main()
