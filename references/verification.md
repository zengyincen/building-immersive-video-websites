# Browser Verification

Verify the assembled project in a real target browser before reporting it done.
Record the browser/device, route, media source, and any unavailable test.

## Media and generation

- Confirm every video decodes and reaches metadata (`loadedmetadata` or an
  equivalent state); compare duration and dimensions with the media manifest.
- For an ordered image sequence, confirm assembly produced one durable
  `master-background-film` and that the page mounts at most one background
  `<video>`. Bridge files are intermediate inputs, not additional topical
  players or section-level background sources.
- Confirm each manifest path is durable and project-local or otherwise stable
  after reload; no temporary preview or expired generation URL may be required.
- For generated media, retain generation evidence: selected capability,
  job/request ID, source image, request metadata, output path, and final status.
  A completed job without a persisted, decoding file is a failure.

## Interaction acceptance

- For a persistent background scene, confirm the same background video remains
  mounted behind every topical chapter, foreground masks/text/media change from
  one continuous progress value, reverse scroll restores the prior state, and
  the sticky scene releases only before footer/non-topic content.
- For an ordered image sequence, confirm each adjacent segment honors its
  supplied first and last image, the handoff is visually continuous inside the
  master film, and the source order is preserved. Inspect frames around every
  assembly boundary for black frames, hard cuts, or jumps. Record any host
  limitation when exact endpoint control is unavailable; do not invent a
  successful transition.

- Scroll scrub: test forward and reverse scroll, both section bounds, clamped
  seeking, and ordinary page scrolling outside the section.
- Mouse scrub: test both horizontal directions on fine pointer input and ensure
  touch does not hijack horizontal scrolling.
- Triggered playback: activate through pointer and keyboard/tap equivalents;
  confirm normal playback reaches completion, then test replay or reset.
- Move the pointer out of every follower, reveal, highlight, and eye region;
  confirm transient targets clear and followers/pupils return to rest.
- For moving-eye overlays, seek through each anchor interval and visibility
  transition; confirm anchors interpolate with media time and invisible ranges
  hide the overlay.

## Accessibility, regression, and honesty

- Test a narrow mobile viewport and a coarse/non-hover input path: controls and
  hotspots remain tappable and no hover-only affordance is required.
- Test `prefers-reduced-motion`: remove decorative continuous motion while
  retaining a deliberate static state and direct controls.
- Reload and inspect the browser console; resolve relevant errors, failed media
  requests, and unhandled promise rejections.
- Confirm the footer, address, brand/year, and legal material appears only after
  the final topical scene hold; it must not release because an intermediate
  bridge ended.
- Recheck existing routes, entry points, and behaviors identified in the initial
  audit so the immersive change does not regress the host project.
- If a capability, device, browser, asset, or test is unavailable, state what
  was attempted, what could not be verified, why, and the resulting risk. Never
  describe an unrun or failed check as passed.
