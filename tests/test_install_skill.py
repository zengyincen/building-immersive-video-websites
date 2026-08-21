import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class InstallSkillTests(unittest.TestCase):
    def setUp(self):
        self.project = Path(__file__).resolve().parents[1]
        self.installer = self.project / "scripts" / "install-skill.py"
        self.tempdir = tempfile.TemporaryDirectory()
        self.destination = Path(self.tempdir.name) / "installed-skill"

    def tearDown(self):
        self.tempdir.cleanup()

    def run_installer(self, *args):
        return subprocess.run(
            [sys.executable, str(self.installer), *args],
            cwd=self.project,
            capture_output=True,
            text=True,
        )

    def test_explicit_destination_copies_only_skill_payload(self):
        result = self.run_installer("--dest", str(self.destination))

        self.assertEqual(0, result.returncode)
        self.assertTrue((self.destination / "SKILL.md").is_file())
        self.assertTrue((self.destination / "references").is_dir())
        self.assertFalse((self.destination / "tests").exists())
        self.assertFalse((self.destination / ".git").exists())

    def test_existing_destination_exits_without_mutation(self):
        self.destination.mkdir(parents=True)
        marker = self.destination / "user-file.txt"
        marker.write_text("keep", encoding="utf-8")

        result = self.run_installer("--dest", str(self.destination))

        self.assertEqual(2, result.returncode)
        self.assertEqual("keep", marker.read_text(encoding="utf-8"))

    def test_force_moves_existing_destination_to_backup(self):
        self.destination.mkdir(parents=True)
        (self.destination / "user-file.txt").write_text("keep", encoding="utf-8")

        result = self.run_installer("--dest", str(self.destination), "--force")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        backup = Path(payload["backup"])
        self.assertTrue(backup.is_dir())
        self.assertEqual("keep", (backup / "user-file.txt").read_text(encoding="utf-8"))

    def test_dry_run_reports_destination_without_creating_it(self):
        result = self.run_installer("--dest", str(self.destination), "--dry-run")

        self.assertEqual(0, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("dry-run", payload["status"])
        self.assertEqual(str(self.destination.resolve()), payload["destination"])
        self.assertFalse(self.destination.exists())


if __name__ == "__main__":
    unittest.main()
