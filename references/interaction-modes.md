# Interaction modes

All interaction modes use the same update discipline: raw event handlers only
update normalized targets or intent flags. One `requestAnimationFrame` loop
reads those targets, eases any state, and performs every DOM, canvas, CSS, or
media write. This prevents handlers from competing for layout and keeps visual
motion coherent.

## Pointer and image response

- **Image reveal:** Pointer input is normalized to the reveal element's bounds
  and stored as the mask origin. The frame loop eases the visible reveal
  position and updates its clip path, mask, or image transform.
- **Cursor follower:** Pointer movement sets a target position; the frame loop
  eases the follower toward it. Disable it for coarse/non-hover pointers.
- **Magnetic elements:** A pointer inside an element's activation radius sets a
  bounded attraction target. The frame loop translates the element and returns
  it to its resting position when the target clears.
- **Highlights and hotspots:** Pointer or keyboard focus selects a semantic
  target. The frame loop renders its highlight; click, Enter, and Space invoke
  the same hotspot action.

## Media response

### Persistent background scene

- Keep one full-bleed background video mounted behind the entire topical scene;
  scroll should normally update foreground chapter progress, masks, text, and
  media cards rather than swapping or resetting the background element.
- Compute one clamped, continuous scene progress and derive every chapter from
  it. Overlap chapter ranges and interpolate both directions so reverse scroll
  is the exact inverse of forward scroll.
- Release the sticky scene only after the final topic chapter. Footer, address,
  brand/year, legal links, and other non-topic information belong outside the
  scene wrapper in normal document flow.

- **Persistent ambient background:** The assembled master film is one mounted,
  muted, inline video that plays continuously or loops as an atmospheric layer.
  Scene progress changes the foreground and masks; it does not switch the film
  or create per-chapter players. Only an explicit frame-accurate scroll request
  may seek this same mounted element.

- **Scroll scrub:** Convert the section's clamped scroll progress to a clamped
  media time with `timeForProgress`. The frame loop seeks only when the desired
  time meaningfully differs from the current time.
- **Mouse scrub:** A horizontal pointer target maps to the media duration in
  the same way. It must not run on touch-only devices where horizontal motion
  is likely a scroll gesture.
- **Triggered playback:** Interaction changes a desired play/pause state;
  the frame loop synchronizes `play()` or `pause()` and handles rejected play
  promises without retry loops.
- **Parallax and video-plane response:** Store bounded normalized scroll and
  pointer targets. The frame loop applies a modest, clamped transform to the
  layer or video plane, never directly mutating it in the raw handler.

## Eye tracking

- **Fixed anchors:** Use normalized eye centers relative to the video frame.
  `pupilOffset` clamps both eye and pointer coordinates, then limits pupil
  travel to the supplied radius.
- **Moving time-based anchors:** Provide time-ordered keyframes containing
  `t`, `left`, `right`, `radius`, and `visible`. Each frame uses
  `interpolateEyeTrack` at the current media time; adjacent invisible
  keyframes make the eye overlay invisible.
- **Tracking confidence:** Define the tracker or authored-track confidence
  threshold explicitly. When confidence falls below it, set `visible: false`
  and hide the overlay until a later keyframe restores a trustworthy anchor;
  never let pupils drift across the subject during uncertain tracking.
- **Pointer leave:** Clear the pointer target and ease both pupils back to
  `[0, 0]` rather than leaving them at their last edge position.
- **Visibility reset:** On `visibilitychange` to hidden, clear transient
  pointer targets, reset pupils, and pause continuous decorative updates. On
  return, rebuild geometry before the next frame.

## Input and accessibility fallbacks

- **Touch fallback:** Do not attach continuous hover tracking on coarse or
  non-hover input. Keep controls tappable, expose hotspots as buttons or links,
  and use a static centered-eye treatment.
- **Reduced motion:** Honor `prefers-reduced-motion` by removing easing-driven
  decorative movement, parallax, cursor followers, and automatic reveal
  animation. Preserve direct controls, information, and an intentional static
  state.
