# Building Immersive Video Websites

A portable Agent Skill for turning supplied videos or static images into immersive luxury-brand websites with scroll-controlled video, mouse interaction, 2.5D depth, hotspots, and cursor-reactive elements such as moving eyes.

The skill uses an existing video directly. When only images are supplied, it discovers and invokes a real image-to-video capability exposed by the current platform, persists the returned file, and never invents a model name or generation result.

## What it builds

- Scroll-scrubbed, mouse-scrubbed, or gesture-triggered video states
- Mouse followers, parallax, highlights, magnetic elements, hotspots, and time-keyframed eye tracking
- CSS/DOM 2.5D scenes with a restrained Apple-inspired luxury visual language
- Touch, keyboard, responsive, and `prefers-reduced-motion` fallbacks
- A single `requestAnimationFrame` scheduler for visual and media writes

These modes can coexist in one site, but one media state never uses multiple competing video-time controls.

## Native installation

Clone the repository, enter it, and run the installer for the local agent:

```bash
git clone https://github.com/zengyincen/building-immersive-video-websites.git
cd building-immersive-video-websites

# Codex
python3 scripts/install-skill.py --target codex

# Claude Code, where local Skills are enabled
python3 scripts/install-skill.py --target claude

# Agents using the shared ~/.agents/skills convention
python3 scripts/install-skill.py --target agents
```

For a project-specific installation:

```bash
python3 scripts/install-skill.py --target project \
  --dest /absolute/path/to/project/.agents/skills/building-immersive-video-websites
```

The installer refuses to overwrite an existing destination. Use `--dry-run` to inspect the target or `--force` to move the existing installation to a timestamped backup before installing.

## Atoms, Base44, Lovable, Replit, Bolt, v0, and other builders

These platforms do not share a universal native `SKILL.md` interface. Import [compatibility/builder-prompt.md](compatibility/builder-prompt.md) into the builder's project instructions or prompt surface, and add [compatibility/project-agents-snippet.md](compatibility/project-agents-snippet.md) when persistent project guidance is supported.

For a single copy-paste prompt, use the English [Universal Builder Prompt](compatibility/universal-builder-prompt.en-US.md). It combines project audit, real image-to-video capability discovery, supplied-video bypass, scroll/video modes, pseudo-3D, mouse tracking, eye overlays, fallbacks, and browser verification in one prompt.

中文版单段 Prompt 见 [Universal Builder Prompt — 中文版](compatibility/universal-builder-prompt.zh-CN.md)，内容与英文版保持同一套能力路由和交互约束。

[compatibility/installation-map.md](compatibility/installation-map.md) distinguishes native skill installation from compatibility import for every supported platform class.

## Usage examples

With an existing video:

```text
Use $building-immersive-video-websites with public/media/product.mp4.
Build a scroll-scrubbed hero, a mouse-reactive product highlight section,
and a touch-safe static fallback. Do not regenerate the supplied video.
```

With a static image:

```text
Use $building-immersive-video-websites with assets/villa.jpg.
Find and call an available native image-to-video capability, create a restrained
luxury fly-through, persist the video, and build the immersive website around it.
```

If the current environment exposes no suitable image-to-video capability, the skill reports what it checked and what is missing instead of pretending a video was generated. Extra-billable generation or new credentials still require authorization.

## Media prerequisites

- Supply durable project-local image or video paths whenever possible.
- Existing videos should expose readable duration and dimensions and support browser seeking.
- `scripts/inspect-media.py` uses `ffprobe` to report normalized metadata and scrub-readiness warnings.
- The starter in `assets/vanilla-starter/` is a framework-neutral fallback; existing projects retain their current framework and design system.

Inspect a video:

```bash
python3 scripts/inspect-media.py /absolute/path/to/video.mp4
```

## Tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
npm install
npm test
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

The browser suite uses Playwright. The skill's full acceptance checklist is in [references/verification.md](references/verification.md).
