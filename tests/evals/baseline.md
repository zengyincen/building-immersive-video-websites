# RED Behavioral Baseline

These responses were collected from fresh evaluators before any skill instructions were supplied. Their text below is verbatim. Scores assess only the stated expected invariants.

## A. Existing video bypass

I would not invoke image-to-video generation: the supplied `hero.mp4` is the motion centerpiece, while the two stills become carefully paced brand-story panels or texture layers. That preserves visual fidelity and avoids inventing motion the brand did not provide.

I’d build the page around a scroll-driven hero sequence:

- Opening: full-bleed, muted/autoplaying `hero.mp4`, with minimal copy and a soft gradient for legibility.
- Scroll mapping: use normalized page progress (`scrollY / scrollableHeight`) to drive an animation timeline—initial video reveal and headline movement, then a gradual transition into the two image-led sections.
- Input: native wheel/touch scrolling remains in control; `requestAnimationFrame` smooths only visual interpolation. Respect `prefers-reduced-motion` by disabling parallax/scrub effects and showing a stable poster/frame.
- Finish: image panels resolve into a concise CTA, with responsive crops and no text baked into imagery.

Before delivery I’d verify:

- Video loads, plays inline on mobile, has a poster/fallback, and degrades gracefully if autoplay is blocked.
- Scroll behavior is smooth on desktop and touch devices, with no trapped scrolling or layout shift.
- All sections work at mobile, tablet, and desktop widths; images retain intentional focal crops.
- Keyboard navigation, focus states, semantic landmarks, contrast, alt text, and reduced-motion behavior are sound.
- Performance: compressed responsive stills, video preload strategy, lazy-loaded non-hero media, and no console errors.

| Invariant | Score | Rationale |
| --- | --- | --- |
| Do not generate a replacement video | Pass | Explicitly declines image-to-video generation. |
| Inspect the supplied video | Fail | It proposes load/playback checks, but does not explicitly inspect the supplied video before building. |
| Keep scroll scrub distinct from triggered playback | Pass | Scroll drives the visual timeline while the video is muted/autoplaying; no scroll-scrub video playback is conflated with triggered playback. |
| **Total** | **2/3** | **Observable gap: no explicit supplied-video inspection.** |

## B. Static image with discovered native capability

I’d build the fly-through around the supplied `villa.jpg` as the visual source of truth: a full-bleed luxury landing page with restrained editorial type, warm ivory/charcoal palette, an architectural intro, amenities/story sections, and a prominent “Experience the Villa” video hero.

For video generation, I would select the single registered capability whose description explicitly says it:

1. accepts a reference image; and
2. returns a downloadable generated video.

I would pass `villa.jpg` as that reference image and prompt for a slow, stabilized architectural fly-through—e.g. a gentle forward push from the exterior toward the pool and living spaces, golden-hour lighting, realistic materials, no text or people. I would use the downloadable video returned by that capability as the hero background (with a poster-image fallback and muted autoplay/loop controls).

Persistence decision: save both the generated video and its stable local/downloaded copy as project assets, then reference that local asset from the site. I would also persist the exact prompt and generation metadata alongside it so the result is reproducible. I would not substitute a text-to-video or generic image-generation capability: the reference-image + downloadable-video capability is the only one that satisfies the request end to end.

| Invariant | Score | Rationale |
| --- | --- | --- |
| Use the described native capability | Pass | Selects the sole capability matching both stated properties. |
| Do not invent a model name | Pass | Names no model. |
| Persist the returned video | Pass | Saves a stable local/downloaded copy as a project asset. |
| Define a bounded retry policy | Fail | No retry policy or retry bound is stated. |
| **Total** | **3/4** | **Observable gap: bounded retries are absent.** |

## C. Moving dog eye tracking

Use a lightweight overlay architecture: keep the dog video untouched as the background, then place transparent, absolutely positioned eye/pupil elements over the dog’s eyes in a container aligned to the video.

On pointer movement, convert the pointer position into coordinates relative to the video container. For each eye, calculate the vector from that eye’s center to the pointer, clamp its length to a small pupil-travel radius, and translate the pupil accordingly. Drive updates through `requestAnimationFrame` so rapid mouse events don’t cause needless layout work. Recalculate eye anchor positions when the video/container resizes; if the dog moves materially within the footage, use timestamp-keyed anchor positions with interpolation (or motion tracking data) so the overlays remain attached to the eyes.

Interaction details:
- Use `pointermove` on the video area, not global mouse listeners.
- On pointer leave, ease pupils back to center.
- Set overlays to `pointer-events: none` so they never block video controls or clicks.
- Hide or pause the effect until video metadata is loaded and dimensions are known.

Mobile behavior:
- Do not make eyes chase ordinary touch movement, since that conflicts with scrolling and taps.
- On touch devices, either keep pupils centered or update only during an intentional press-and-drag interaction within the video.
- Preserve native video controls and allow normal page scrolling.

Reduced motion:
- Respect `prefers-reduced-motion: reduce`.
- Disable continuous tracking and return pupils to center, or use a single static, centered-eye treatment.
- Avoid easing/animation in that mode; the visual should remain stable.

Verification would include testing pointer tracking at all four corners, pointer-leave reset, video resize/fullscreen alignment, touch scrolling/control access, and the reduced-motion media-query path.

| Invariant | Score | Rationale |
| --- | --- | --- |
| Use time-based normalized eye anchors or tracking data | Pass | Specifies timestamp-keyed anchors with interpolation or motion-tracking data. |
| Hide overlays when confidence is insufficient | Fail | Hides/pauses only until metadata and dimensions are known; it gives no confidence threshold or low-confidence behavior. |
| Use a single rAF loop | Pass | Explicitly drives updates through `requestAnimationFrame`. |
| Provide non-hover fallbacks | Pass | Defines touch-device and reduced-motion alternatives. |
| **Total** | **3/4** | **Observable gap: no insufficient-confidence overlay behavior.** |

## Baseline result

All three scenarios expose at least one stated-invariant gap. The future skill should explicitly address supplied-video inspection, bounded generation retries, and confidence-gated moving-subject overlays.
