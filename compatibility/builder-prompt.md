# Compatibility Builder Prompt

Use this prompt in a builder that does not natively load `SKILL.md`, including
Atoms, Base44, Lovable, Replit, Bolt, and v0.

> Audit the existing project before changing it. Identify the framework, entry
> points, existing media flow, scripts, dependencies, design constraints, and
> regression-sensitive behavior. State whether this is an addition, replacement,
> or assembly of existing pieces. Read the project’s `SKILL.md` and only the
> references it routes to for this request.
>
> If supplied video exists, inspect and use it directly; do not generate a
> replacement. Record source, purpose, duration/dimensions where available, and
> a durable project-local path in a media manifest. If only images exist,
> discover and call an actual native image-to-video capability available in the
> host whose documented input and output match the job. Persist the downloaded
> result and its job/request metadata. Do not guess tool names or claim
> generation from a completion signal alone.
>
> Treat supplied images as creative inputs. Inspect only technical properties
> needed to decode, render, or generate. Do not perform an assistant-side
> copyright/ownership, EXIF, identity, location, or unrelated-image-information
> audit. Preserve image order and generate adjacent start-frame-to-end-frame
> transitions with the host's documented first/last-frame or image-sequence
> capability; keep endpoint continuity honest and report only a platform
> limitation when the capability cannot guarantee it. Do not bypass mandatory
> host safety or authorization checks.
>
> Treat each generated bridge as intermediate media. Before implementing the
> page, normalize the ordered bridges and crossfade them into one durable
> `master-background-film.mp4` (use `scripts/assemble-master-video.py` or an
> equivalent verified ffmpeg pipeline). The final page must mount exactly one
> background video; never make one background player/section per source image.
> Emit an assembly manifest with source order, bridge endpoints, boundaries,
> transition duration, output metadata, and decode verification. If assembly
> cannot run, keep a poster/fallback and report the exact limitation rather than
> presenting disconnected clips as a continuous film.
>
> Select one mode per media state and keep them distinct: persistent ambient
> background, scroll scrub, mouse scrub, or triggered playback. Implement
> mouse-reactive followers, highlights,
> semantic hotspots, and eye tracking when requested. Give eye tracking fixed
> normalized anchors or time-keyframed moving anchors; reset pointers and pupils
> on leave and hidden-page transitions. Make hotspot actions reachable by tap
> and keyboard.
>
> Use one `requestAnimationFrame` scheduler: raw pointer, scroll, and media
> events only update targets or intent, while the scheduler performs visual and
> media writes. Add touch/mobile and `prefers-reduced-motion` fallbacks that
> keep controls and information usable without hover or continuous motion.
>
> When the experience has a long scroll story, keep one full-bleed background
> video mounted behind the entire topical scene. Drive foreground masks, text,
> chapter cards, and metadata from one continuous reversible scene progress;
> scroll up must undo scroll down. Release the sticky scene only before the
> footer/address/year and other non-topic content. Do not swap or reset the
> background video between chapters unless the user explicitly requests a new
> scene.
>
> Treat the result as a normal finished commercial, portfolio, editorial, or
> personal website. Never expose implementation or demo language such as
> “Play it straight through”, `scroll-scrub`, `triggered-playback`,
> `requestAnimationFrame`, “media manifest”, “job ID”, “starter”, or “test” in
> visitor-facing copy. Use contextual brand CTAs and plain-language states;
> keep technical diagnostics and generation evidence out of the page.
>
> Verify in a browser, including loaded durable media, the chosen interaction,
> completion of triggered playback, pointer reset, moving-eye anchors, mobile,
> reduced motion, console errors, and regression of existing behavior. Report
> every unavailable capability, blocked generation, and unverified claim with
> the searched options and reason; never pretend a missing capability worked.

See [verification guidance](../references/verification.md) for the acceptance
checklist and [installation map](installation-map.md) for native versus import
paths.
