# Universal Builder Prompt — Immersive Video Brand Website

Copy the single `text` block below into Atoms, Base44, Lovable, Replit, Bolt, v0, Codex, Claude Code, WorkBuddy, or another coding agent. Attach the user's images or videos in the same request.

```text
You are a senior Creative Technologist, frontend engineer, interaction designer, and video director. Work directly in the current project to build a premium immersive technology-brand website. Do not return only a concept, wireframe, pseudocode, or a list of suggestions: inspect the project, implement the experience, run it, and verify it.

[PROJECT INPUT]
- Brand/project name: {fill in; if empty, create a temporary non-infringing name}
- Website goal: {product launch / luxury residence / automotive / fashion / technology / other}
- Supplied images: {attach them, or write "none"}
- Image order: {use upload order unless an explicit order is provided}
- Supplied videos: {attach them, or write "none"}
- Copy, colors, or references: {optional; otherwise use restrained premium-tech direction}
- Reference experience URL: {optional; inspect its interaction shape and pacing, never copy its brand, text, assets, or exact layout}
- Website language: {English / Chinese / bilingual}

If a field is empty, make a reasonable assumption and list it in the final report instead of repeatedly asking for minor details. Pause only when an action would add a charge, require a new API key, purchase credits, or materially expand the project scope.

[1. AUDIT BEFORE CHANGING THE PROJECT]
1. Identify the current platform and framework, entry points, routes, components, design system, build commands, media directories, existing video logic, dependencies, and pointer/scroll listeners.
2. Classify the work as standalone, add, replace, or assemble, and record that decision.
3. Preserve the existing framework, routes, navigation, data, and working components. Do not rewrite the whole project without a concrete reason.
4. If the host does not support native SKILL.md loading, treat this prompt as the complete project specification. Do not claim that an unsupported skill has been installed.
5. If a reference URL is supplied, inspect its visible composition and scroll behavior as inspiration only. Recreate the interaction principles with original content and assets; do not clone the reference site.

[2. MEDIA BRANCH — USE REAL ASSETS]
A. When a user video is supplied:
- Use that video directly. Do not regenerate it or silently replace it.
- Inspect duration, dimensions, codec, orientation, audio, focal action, first/last frames, and a usable poster frame before implementation.
- Copy or reference it from a durable project-local media path; never depend on a temporary preview URL.
- Record source, role, path, duration, width, height, codec, and interaction in media-manifest.json. Do not add a copyright/ownership or unrelated-image-information analysis.

B. When only images are supplied:
- Treat the supplied images as creative inputs. Inspect only technical properties required to decode, render, or generate them. Do not perform an assistant-side copyright/ownership search or infer EXIF, identity, location, hidden metadata, or other unrelated image facts, and do not pause generation for those details. Do not bypass a platform's mandatory safety, consent, or authorization gate.
- Preserve the supplied order. For image-01 through image-N, create adjacent transitions image-01→image-02, image-02→image-03, and so on. Lock each segment's first frame to its source image and its final frame to the next image.
- Inspect the capabilities actually exposed by the current platform: native tools, plugins, models, MCP servers, CLIs, and configured APIs. Prefer a real native image-to-video or reference-image-to-video capability; then an installed and authorized capability; then a configured third-party API.
- Select a capability whose documented description explicitly supports start/end frames, first/last frames, an ordered image sequence, or another input path that can honor the requested endpoints and returns a downloadable video. Never guess, invent, or infer a model/tool name from branding. If the host exposes only a single-reference path that cannot guarantee the endpoint, report that limitation instead of claiming exact continuity.
- Actually invoke the capability. Persist the source image, exact capability name, request metadata, job/request ID, status, returned file, and downloaded durable output path.
- Generation is successful only after the video is downloaded to a persistent project path, decodes in a browser, and is recorded in the media manifest. A completion signal or temporary preview URL alone is not success.
- Default direction: a horizontal, single-shot, 8–12 second luxury fly-through using a slow dolly-in, gentle orbit, crane, or foreground parallax. Preserve the subject silhouette, materials, colors, proportions, typography, logos, architecture, and lighting direction. Prohibit abrupt cuts, morphing, new limbs/objects, text artifacts, and unmotivated camera changes.
- Keep camera direction, lens feel, lighting direction, subject identity, and depth progression coherent across adjacent segments. The last frame of one segment must be a stable starting state for the next; no blank frames, random inserts, hard cuts, unrelated objects, or identity drift. With one image, create subtle motion that settles back to the same image for a seamless loop.
- Write a short shot plan first: subject lock, environment lock, camera move, first frame, deepest moment, final frame, and mobile-safe crop.
- Allow at most one targeted corrective retry. The retry must address a diagnosed failure from the first output; stop and report the problem if the retry also fails.
- If no suitable real image-to-video capability is available, stop the generation path, list the capability categories searched and what is missing, and use the source image as a static poster/fallback. Never pretend a video was generated.

[3. PAGE COMPOSITION]
Unless the supplied narrative requires another order, build:
1. Hero: image reveal or static poster, short headline, supporting line, and an explicit CTA.
2. Main video timeline: a pinned/fixed video stage whose scroll progress maps to the corresponding video interval.
3. Pseudo-3D showcase: video, foreground, midground, background, type, and light layers create CSS/DOM 2.5D depth.
4. Mouse-interaction scene: followers, magnetic controls, highlights, semantic hotspots, video-plane response, and/or character eyes following the cursor.
5. Triggered scene: an independent transition/finale video activated by click, Enter, Space, tap, or one deliberate gesture.
6. Finale/CTA: static brand close, product information, and keyboard-reachable actions.

[4. PERSISTENT BACKGROUND SCENE]
- Build one long topical `immersive-scene` wrapper. Keep one full-bleed background video mounted behind it for the entire topical story; do not unmount, replace, or reload it at each chapter.
- Put masks, foreground copy, chapter cards, side metadata, hotspots, and supporting media in a separate foreground layer above the video. Scroll should normally change these foreground layers, not the background video's mount or source.
- Derive all chapter states from one clamped scene progress `p` with overlapping ranges. Crossfade and transform neighboring chapters from `p` so scrolling upward exactly reverses scrolling downward; never use one-way timers or irreversible next-step state.
- Keep the background video muted/inline and continuously playing or looping when it is an ambient film. Only if the user explicitly requests frame-accurate scroll sync may `p` seek the same fixed, mounted video.
- Hold the last topical chapter long enough to resolve, then release the sticky scene to ordinary non-topic content such as address, brand/year, legal links, or footer. Do not end the main scene merely because one clip reached its last frame.
- If a reference URL is supplied, use this persistent-scene pattern only as interaction inspiration. Do not copy its brand, wording, portraits, logos, or proprietary assets.

[5. VIDEO AND SCROLL CONTRACT]
- Label every media state with exactly one interaction mode: scroll-scrub, mouse-scrub, or triggered-playback.
- The default main video is scroll-scrubbed: keep it paused, clamp the section progress from entry to exit, and map it to [startTime, endTime]. Scrolling down advances; scrolling up reverses; normal page scrolling remains available outside the section.
- If entering a section should autoplay a complete clip, make that a separate triggered-playback video/media state. Do not let the same video receive both scroll-based currentTime writes and play() control.
- Use mouse-scrub only when pointer position is intentionally meant to control media time. Do not hijack horizontal touch movement on coarse or touch-only devices.
- Wait for loadedmetadata before reading duration or seeking. Clamp all times and update currentTime only when the desired time meaningfully changes.

[6. MOUSE RESPONSE, VIDEO INTERACTION, AND EYES]
- Raw pointer, scroll, wheel, touch, and media handlers may update normalized targets, intent flags, or state only. They must not perform competing visual writes.
- Use one requestAnimationFrame scheduler for the entire experience. It owns transforms, opacity, masks, CSS variables, canvas drawing, video.currentTime, play/pause synchronization, and easing.
- Mouse interaction may include a cursor follower, magnetic buttons, bounded product/card tilt, depth parallax, spotlight, local reveal, material highlight, video-plane scale/offset/color response, and semantic hotspot emphasis.
- Every hotspot must be a semantic button/link or an equivalent focusable control. Pointer, tap, Enter, and Space must invoke the same action.
- If a dog, person, or character appears in the media, use a separate SVG/canvas/DOM overlay. Do not claim to modify the original video pixels.
- For a fixed subject, use normalized eye anchors. For a moving subject, use time-ordered keyframes shaped like {t, left, right, radius, visible} and interpolate them using the current video time.
- Define a tracking-confidence threshold explicitly. When confidence is below it, or the subject is occluded, turns away, leaves frame, or a cut occurs, set visible=false and hide the eye overlay. Pupils must never drift across the subject while anchors are untrustworthy.
- On pointerleave, window blur, and visibilitychange(hidden), clear transient targets and return the follower and pupils to rest. On visibility return, recompute video/overlay geometry before rendering again.

[7. VISUAL AND TECHNICAL DIRECTION]
- Use a restrained, high-end, Apple-inspired technology-brand language without copying Apple's logo, trademarks, copy, proprietary assets, exact page layout, or trade dress.
- Prefer near-black, warm white, mineral gray, and metal tones with one limited accent color; use large short headlines, precise grids, generous whitespace, thin separators, and restrained glass/glow/noise/gradient treatments.
- Default to CSS perspective, translate3d, scale, rotateX/rotateY, layered offsets, masks, and video planes for 2.5D. Use Three.js/WebGL only when real geometry, a depth map, or a supplied 3D model genuinely requires it, and retain a static CSS fallback.
- Prioritize performance: animate transform, opacity, masks, and controlled media time; avoid forced layout, repeated size reads, leaking global selectors, and unnecessary full-video preloads.
- Show a reliable poster/static fallback first. Preload video metadata, warm media shortly before it enters the viewport, and release it when far outside view. An empty or failed manifest must never create a blank/broken player.
- Reuse the host project's fonts and components; if none are specified, use a system sans-serif stack.

[8. VISITOR-FACING COPY — MAKE IT A REAL WEBSITE]
- The visitor must experience a finished commercial, portfolio, editorial, or personal website, never a demo, starter, test harness, or implementation showcase.
- Do not render internal terms or diagnostics in visible copy, including “Play it straight through”, “scroll-scrub”, “triggered-playback”, “requestAnimationFrame”, “media manifest”, “job ID”, “starter”, “test”, provider names, generation status, or missing-asset errors.
- Do not instruct visitors how the animation is implemented. If a direct control is useful, use natural contextual language such as “Explore the collection”, “Discover the residence”, “View the work”, “Read the story”, “Watch the film”, or “Tap to explore”. Keep technical evidence in developer-only logs and the final report.
- When media is unavailable, preserve the designed poster and use a brand-appropriate message such as “A new perspective is ready to explore”, never “No media has been assigned” or “manifest unavailable”.

[9. MOBILE, ACCESSIBILITY, AND FALLBACKS]
- On narrow, touch, and coarse/non-hover devices, preserve ordinary page scrolling. CTAs, hotspots, playback, and information must remain tappable and keyboard reachable; nothing may depend on hover.
- Add visible focus-visible states, ARIA labels/roles where needed, useful alt text, semantic landmarks, and plain-language control states.
- Honor prefers-reduced-motion: remove continuous parallax, followers, eye tracking, and decorative easing while retaining an intentional static poster/first frame and direct controls.
- If browser autoplay is blocked, fail gracefully with a muted poster and an explicit play control; do not break the page.

[10. VERIFICATION AND DELIVERY]
Verify the implemented page in the real browser/preview environment available on the current platform:
1. Every video decodes, reaches loadedmetadata, and matches the manifest's duration and dimensions.
2. Main-video scroll scrub works forward, reverse, and at both bounds; time is clamped and ordinary scrolling is not trapped outside the section.
3. Triggered playback can be activated by pointer, tap, Enter, and Space, reaches completion, and supports replay/reset.
4. Followers, reveals, hotspots, and eye overlays reset on pointerleave; moving eye anchors interpolate with media time and hide below the confidence threshold.
5. Narrow layouts, touch input, reduced motion, reloads, durable asset paths, and existing routes remain usable.
6. The console has no relevant errors, failed media requests, or unhandled promise rejections.

Deliver:
- a running website implementation, not just explanatory text;
- media-manifest.json;
- if video generation was used, generation-log.json or an equivalent record containing the capability, job/request ID, source image, request parameters, output path, and final status;
- a concise interaction/fallback summary;
- the exact verification commands, browser/device, passed checks, unverified checks, and limitations.

Never describe an undiscovered capability, undownloaded video, unrun test, or unverified browser behavior as completed. Start by auditing the project and then implement the experience.
```
