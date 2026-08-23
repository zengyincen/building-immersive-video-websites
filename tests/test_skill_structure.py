from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/platform-routing.md",
    "references/video-direction.md",
    "references/interaction-modes.md",
    "references/persistent-background-scene.md",
    "references/visual-system.md",
    "references/verification.md",
    "compatibility/builder-prompt.md",
    "compatibility/project-agents-snippet.md",
    "compatibility/installation-map.md",
}


class SkillStructureTests(unittest.TestCase):
    def test_required_files_exist(self):
        missing = sorted(path for path in REQUIRED if not (ROOT / path).is_file())
        self.assertEqual([], missing)

    def test_frontmatter_is_discoverable(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertIn("name: building-immersive-video-websites", text)
        match = re.search(r"^description: (.+)$", text, re.MULTILINE)
        self.assertIsNotNone(match)
        self.assertTrue(match.group(1).startswith("Use when "))

    def test_markdown_links_resolve(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", text)
        self.assertGreaterEqual(len(links), 5)
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)

    def test_router_distinguishes_modes_and_touch_fallback(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "scroll-scrubbed video",
            "mouse-scrubbed video",
            "triggered playback",
            "touch fallback",
            "responsive and reduced-motion",
            "persistent background scene",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
