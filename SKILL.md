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

Choose exactly one interaction mode for each media state: scroll-scrubbed video
(scroll progress controls time), mouse-scrubbed video (pointer position controls
time), or triggered playback (an event starts or pauses normal playback). Keep
these three modes distinct; do not combine their controls on the same media state.

Use [platform routing](references/platform-routing.md) whenever a static image
needs motion generation, a capability must be selected, authorization or async
work is involved, or no suitable capability is apparent. It defines the required
selection, authorization, persistence, retry, and failure-report rules.

Before delivery, verify the assembled page in a browser: assets load from their durable paths, the selected interaction works without trapped scroll, a touch fallback works, responsive and reduced-motion behavior remain usable, and the console has no relevant errors.
