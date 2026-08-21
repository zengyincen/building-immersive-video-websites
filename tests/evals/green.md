# GREEN Behavioral Evaluation

These responses were collected from fresh evaluators using the completed skill. Their text is verbatim. Scores use the same invariants as `baseline.md`.

## A. Existing video bypass

Use the supplied `hero.mp4` directly; I would not invoke image-to-video generation. I’d inspect its duration, dimensions, audio, focal action, and usable poster frame, then record it (and both stills) in a durable media manifest. The stills remain static supporting art/posters unless motion is explicitly needed.

Make the hero a scroll-scrubbed media state only. Clamp progress through its pinned section to `[0, 1]`, map it to `video.currentTime = progress × duration`, and seek only from a single `requestAnimationFrame` loop when the target time materially changes. Raw scroll events update only the normalized target; ordinary page scrolling remains available outside the section. Do not combine pointer scrubbing or triggered playback with that state.

Before delivery, verify in a real browser that:

- Every asset loads from its durable local path and the video reaches metadata with manifest-matching duration/dimensions.
- Scrubbing works forward and backward, clamps at both bounds, and does not trap scroll.
- The static poster/fallback is intentional before media readiness and on touch.
- Mobile/coarse-pointer controls remain usable; no hover-only dependency.
- `prefers-reduced-motion` presents a usable static composition.
- Reloading produces no relevant console, media-request, or promise errors.

I would present the page as a sparse dark brand stage: one focused hero frame, the two stills as editorial supporting scenes, high-contrast typography, restrained accent color, responsive hierarchy, and visible keyboard focus.

| Invariant | Score |
| --- | --- |
| Do not generate a replacement video | Pass |
| Inspect the supplied video | Pass |
| Keep scroll scrub distinct from triggered playback | Pass |
| **Total** | **3/3** |

## B. Static image with discovered native capability

Intent: standalone luxury villa fly-through microsite.

Capability selection: select only the registry capability explicitly described as accepting a reference image and returning a downloadable generated video. No guessed model/tool name or image-only alternative is acceptable. Use `villa.jpg` as its reference with one 16:9, 8–12-second restrained forward dolly: preserve the villa’s architecture, materials, landscaping, lighting, and composition; glide toward the entry with stable foreground parallax; no cuts, morphing, new structures, or text artifacts.

Persistence: before any async polling, persist the returned job ID and full request metadata. On completion, download the actual video—not merely its preview URL—to a durable project path such as `assets/media/villa-flythrough.mp4`, then record it in `media-manifest.json` with:

- source: `villa.jpg`
- role: hero fly-through/poster source
- selected capability: its exact registry-provided name
- job/request ID and prompt metadata
- durable output path and final status

Use one corrective retry at most for a failed stability/architecture-preservation requirement; retain the original job record. A completion signal without a downloaded, decoding local video is failure.

Site: a dark, sparse luxury stage with mineral neutrals, off-white display type, thin separators, and a static `villa.jpg` poster while metadata loads. The hero uses **scroll-scrubbed video only**: section scroll progress maps to video time through one `requestAnimationFrame` loop. Do not combine pointer scrubbing or triggered playback on that same media. Include a keyboard-focusable “Explore residence” anchor, touch-safe ordinary scrolling, and a reduced-motion static poster state.

Before delivery, verify that the persisted video decodes, its manifest paths survive reload, scroll scrub works forward/reverse without trapping scroll, touch and narrow layouts remain usable, reduced motion is static and intentional, and the browser console is clean.

| Invariant | Score |
| --- | --- |
| Use the described native capability | Pass |
| Do not invent a model name | Pass |
| Persist the returned video | Pass |
| Define a bounded retry policy | Pass |
| **Total** | **4/4** |

## C. Moving dog eye tracking

Use the video as normal triggered/looped playback; mouse input controls only a separate eye-overlay layer, never video time.

- Place a canvas/SVG overlay over the video, sharing its object-fit crop geometry.
- Track the dog’s two eye centers with time-ordered video-time keyframes: `{t, left, right, radius, visible}`. Interpolate each animation frame; mark eyes invisible during occlusion, off-frame moments, or cuts.
- On pointer move, store normalized coordinates relative to the rendered video bounds. A single `requestAnimationFrame` loop reads that target and the current video time, resolves the keyframed eye anchors, clamps each pupil offset to its eye radius, and performs all drawing. On pointer leave, ease pupils back to center.
- Recalculate overlay/video geometry on resize and when the tab becomes visible; clear transient pointer state when hidden.

For mobile/coarse-pointer devices, disable hover tracking entirely—horizontal motion must remain available for scrolling. Show a deliberate static, centered-pupil treatment while retaining normal video controls/playback.

For `prefers-reduced-motion`, remove pupil easing and all decorative movement (including parallax/cursor effects). Keep an intentional static eye state, or allow direct tap/play controls without any automatic animated response.

| Invariant | Score |
| --- | --- |
| Use time-based normalized eye anchors or tracking data | Pass |
| Hide overlays when confidence is insufficient | Fail |
| Use a single rAF loop | Pass |
| Provide non-hover fallbacks | Pass |
| **Total** | **3/4** |

The response hides overlays for occlusion, off-frame moments, and cuts but does not state a confidence threshold. The targeted correction is now in `references/interaction-modes.md`: authored or tracked anchors define a threshold, set `visible: false` below it, and remain hidden until trustworthy anchors return. Per the user's direction to stop further review cycles, this scenario was not dispatched again after that narrow correction.

## Result

The completed skill improved the baseline from 6/11 passing invariants to 10/11 in the recorded fresh responses. The only missed wording produced a targeted confidence-gating instruction before publication; no unsupported platform capability was represented as verified.
