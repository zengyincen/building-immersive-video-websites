# Behavioral Evaluation Scenarios

## A. Existing video bypass
The user supplies `hero.mp4` and two still images. Build an immersive brand page. Explain whether you invoke image-to-video generation, how you map scroll input, and what you verify before delivery.

Expected invariants: do not generate a replacement video; inspect the supplied video; keep scroll scrub distinct from triggered playback.

## B. Static image with discovered native capability
The user supplies `villa.jpg`. The tool registry contains one capability whose description says it accepts a reference image and returns a downloadable generated video. Build a luxury fly-through site and state the exact capability-selection and persistence decisions.

Expected invariants: use the described native capability; do not invent a model name; persist the returned video; define a bounded retry policy.

## C. Moving dog eye tracking
The user supplies a background video in which a dog moves across the frame and asks for its eyes to follow the mouse. Describe the interaction architecture and mobile/reduced-motion behavior.

Expected invariants: use time-based normalized eye anchors or tracking data; hide overlays when confidence is insufficient; use a single rAF loop; provide non-hover fallbacks.
