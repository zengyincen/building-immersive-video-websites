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
> Select one mode per media state and keep them distinct: scroll scrub, mouse
> scrub, or triggered playback. Implement mouse-reactive followers, highlights,
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
