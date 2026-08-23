---
name: building-immersive-video-websites
description: Use when building an immersive, scroll-controlled brand website from supplied images or video.
---

# Building Immersive Video Websites

Start with the supplied assets. If video is supplied, inspect it first (duration,
dimensions, audio, focal action, and usable frames), then bypass generation and
carry that video into the media manifest. For static images, discover available
capabilities by their descriptions; select only one that explicitly accepts the
needed input and returns a downloadable video. Do not invent model or tool names.

Audit build intent before implementation: is this a standalone site, an addition
to an existing site, a replacement, or an assembly of existing pieces? Record the
answer and hand off a media manifest containing each source asset, its role,
generation/job metadata when applicable, and its durable local path.

Choose exactly one interaction mode for each media state: persistent ambient
background (the master film plays/loops independently while scene progress drives
the foreground), scroll-scrubbed video (scroll progress controls time),
mouse-scrubbed video (pointer position controls time), or triggered playback (an
event starts or pauses normal playback). Keep these modes distinct; do not
combine their controls on the same media state.

For media generation or shot refinement, use [video direction](references/video-direction.md).
For scheduler discipline, followers, hotspots, eye tracking, touch behavior, and
motion fallbacks, use [interaction modes](references/interaction-modes.md). For
art direction, media loading, and progressive enhancement, use the
[visual system](references/visual-system.md).
For ordered still-image transitions, read the [video direction](references/video-direction.md)
input boundary and adjacent image-to-image transition contract; do not add a
copyright or unrelated-image-information audit to the generation path.
For multiple supplied images, the final site must use one assembled master
background film. Persist each adjacent bridge as intermediate media, then run
[`scripts/assemble-master-video.py`](scripts/assemble-master-video.py) (or a
verified equivalent) to normalize and crossfade the sequence before wiring the
page. Never create one background player per image or treat a job-complete
message as a usable master file.
When the background film must remain behind a long scroll story, use the
[persistent background scene](references/persistent-background-scene.md)
contract for the sticky scene shell, foreground chapters, reversible progress,
and footer release.

Use [platform routing](references/platform-routing.md) whenever a static image
needs motion generation, a capability must be selected, authorization or async
work is involved, or no suitable capability is apparent. It defines the required
selection, authorization, persistence, retry, and failure-report rules. In a
builder without native skill discovery, use the self-contained
[compatibility builder prompt](compatibility/builder-prompt.md), the
[project-agent snippet](compatibility/project-agents-snippet.md), and the
[installation map](compatibility/installation-map.md). These are imports, not a
claim that every platform supports native `SKILL.md` installation.
For a single copy-paste request, use the [universal English Builder Prompt](compatibility/universal-builder-prompt.en-US.md).
For Chinese-language projects, use the [universal Chinese Builder Prompt](compatibility/universal-builder-prompt.zh-CN.md).

Keep visitor-facing copy separate from implementation language. Generated pages
must read like normal commercial, portfolio, editorial, or personal websites:
never expose demo/starter wording, test instructions, tool names, media-manifest
fields, job IDs, scheduler terms, or phrases such as “Play it straight through”.
Use contextual brand CTAs and status messages instead; keep technical evidence in
the final report or developer-only metadata.

Before delivery, verify the assembled page in a browser: assets load from their durable paths, the selected interaction works without trapped scroll, a touch fallback works, responsive and reduced-motion behavior remain usable, and the console has no relevant errors.
Follow the complete [browser verification checklist](references/verification.md)
and report any unavailable capability or unverified check honestly.
