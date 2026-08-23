# Persistent background scene

Use this architecture when the requested experience resembles a full-screen
scroll story: a background film remains present while foreground chapters,
masks, copy, cards, and metadata change over it.

## Scene shell

- Create one long `immersive-scene` wrapper for the topical story. Keep a
  `scene-background` layer mounted for the whole wrapper, usually `position:
  sticky`/fixed and full-bleed. Do not unmount, replace, or reload the video at
  every chapter.
- When the story came from multiple images, the mounted source is the single
  assembled master background film. Individual image-to-image bridges belong in
  generation storage and the assembly manifest only; they are never separate
  background players or per-chapter sections.
- Put all changing copy, masks, media cards, hotspot panels, chapter counters,
  and contrast scrims in a separate `scene-foreground` layer above the video.
- Keep persistent navigation and small status UI anchored to the scene frame;
  keep the footer, address, brand name/year, legal links, and other non-topic
  material outside the scene wrapper so normal document flow resumes there.
- Use the supplied reference only for interaction shape and pacing. Do not copy
  its brand, text, portrait, logos, exact layout, or proprietary assets.

## Scroll contract

- Calculate one normalized scene progress `p` from the scene wrapper's start and
  end. `p` must be continuous, clamped, and reversible: scrolling down and up
  through the same range produces the inverse visual state.
- Define topical chapters as overlapping progress ranges, for example
  `{id, start, end, eyebrow, title, body, media, mask, theme}`. Crossfade and
  transform neighboring chapters from the same `p`; do not use one-way timers,
  scroll-counted steps, or irreversible “next” state.
- The default background policy is persistent ambient playback: keep the video
  behind the whole topical scene, muted/inline, with normal loop or direct-play
  behavior. Scroll changes foreground state and masks, not the video's mount or
  source. If the user explicitly requests frame-accurate scroll sync, keep the
  same video fixed and mounted and seek its time from `p` in the single scheduler.
- Use a deliberate hold at the final topical chapter. End the sticky scene only
  after its last topic content has resolved; release to the footer or other
  non-essential information afterward. Never end the main story merely because
  one video clip reached its last frame.
- On reverse scroll, restore masks, text, media cards, counters, and theme
  transitions from the same chapter functions. Do not replay an entrance-only
  animation that cannot be undone.

## Layer and motion rules

- Render the background video as a quiet visual field with a restrained scrim,
  contrast shift, or blur only when needed for legibility. Keep it perceptually
  present while foreground content changes.
- Drive foreground `opacity`, `transform`, `clip-path`/mask, `filter`, and CSS
  variables from `p` in one `requestAnimationFrame` loop. Raw scroll events only
  update the target progress.
- Use long, overlapping easing windows so the transition feels continuous at
  any scroll velocity. Avoid abrupt card swaps, blank frames, hard cuts, or
  sudden layout jumps.
- On touch and reduced motion, keep the background and chapter content usable;
  replace continuous decorative motion with stable chapter states and direct
  controls rather than removing the story.

## Acceptance checklist

- The background video remains mounted and visually behind every topical
  chapter.
- Exactly one master background video element is mounted for the topical scene;
  adjacent source images are represented by continuous bridge boundaries inside
  that file rather than by separate web sections.
- Forward and reverse scroll traverse the same states without drift or jumps.
- Foreground masks, text, and media change independently of the background
  layer, unless explicit frame-sync was requested.
- The scene releases cleanly to ordinary footer/non-topic content at its end.
- No visitor-facing copy mentions the implementation, demo, test, or provider.
