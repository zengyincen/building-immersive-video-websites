# Video direction for immersive fly-throughs

Use this reference only when generating or optimizing video. A supplied video skips it unless optimization guidance is needed.

## Supplied-image input boundary

- Treat each image supplied by the user as the creative input for this task. Do
  not run an assistant-side copyright/ownership search or infer licensing,
  identity, location, EXIF, hidden metadata, or other unrelated image facts.
- Inspect only technical properties needed to decode, generate, or render the
  shot, such as file availability, decodability, dimensions, orientation, and
  a usable frame. Do not pause generation to request unrelated image details.
- Do not bypass a platform's mandatory safety, consent, or authorization gate.
  If the host blocks the request, report that platform limitation; otherwise
  proceed with the supplied images as creative references.

## Ordered image-to-image transition contract

- Preserve the user's image order. For `image-01 … image-N`, create adjacent
  transitions `image-01 → image-02`, `image-02 → image-03`, and so on. The
  first frame of each segment must honor its source image and the final frame
  must honor the next image.
- Prefer one documented capability that accepts start and end/reference frames
  or an ordered image sequence. If the host only exposes a single-reference
  capability, use it only when its documented output can honor the requested
  endpoint; otherwise report the limitation instead of pretending exact
  frame-to-frame continuity was generated.
- Keep camera direction, lens feel, lighting direction, subject identity, and
  depth progression coherent across adjacent segments. The final frame of one
  segment must be a valid starting state for the next; avoid blank frames,
  random inserts, hard cuts, morphing, or unrelated new objects.
- If adjacent images differ substantially, use a deliberate continuous bridge
  or a restrained overlap transition while preserving both endpoint images. If
  only one image is supplied, create subtle motion that returns to a stable
  version of the same image for a seamless loop.
- Persist the ordered source list, segment mapping, capability/job metadata,
  and durable output paths in the media manifest. Technical metadata required
  for the render is enough; do not add a rights or unrelated-image-information
  analysis to the workflow.

## Master background film assembly (mandatory for image sequences)

- The final web deliverable is one continuous `master-background-film.mp4` (or
  an equivalent single durable video file), not one web video per source image.
  `image-01.mp4`, `image-02.mp4`, and similar bridge files are intermediate
  generation assets only and must never become separate chapter players.
- Build the film from the ordered bridges in sequence. Every adjacent handoff
  must be a real overlap/bridge (`image-01 → image-02`, then
  `image-02 → image-03`, and so on) with a deliberate crossfade or equivalent
  continuous transition. Do not concatenate unrelated clips with a hard cut.
- When the host can generate only one bridge at a time, first persist all bridge
  files, then normalize them to a common width, height, aspect ratio, frame rate,
  pixel format, and time base. Assemble them with `scripts/assemble-master-video.py`
  or an equivalent verified ffmpeg pipeline. The script must fail clearly when
  ffmpeg/ffprobe, a bridge, or required metadata is unavailable; never fabricate
  a master file from a job-complete message or temporary URL.
- Write an assembly manifest containing the ordered sources, each bridge's
  `from`/`to` IDs, transition duration, output path, segment boundaries, codec,
  duration, dimensions, and frame rate. Verify the exported master decodes and
  inspect frames around each boundary for black frames, jumps, or hard cuts.
- Mount only the master file in the page's persistent background layer. The
  foreground scene may crossfade masks, copy, chapter cards, hotspots, or
  supporting media from one normalized scene progress value, but it must not
  replace, unload, or reload the background video at chapter boundaries.
- If an environment cannot produce or assemble a single master film, report the
  exact limitation and keep a static poster/fallback. Do not ship a page that
  presents independent bridge videos as if they were one continuous background.

## Shot-plan contract

Write a short plan before generation: identify the subject and its immutable visual traits, setting, horizontal aspect ratio, intended duration, camera move, first frame, final frame, and the moment of greatest depth. The plan must name a single continuous move and keep the subject readable throughout.

## Subject-preservation prompt recipe

Prompt in this order: **subject lock**, **environment lock**, **camera instruction**, **motion constraints**, then **finish**. Describe the supplied subject's silhouette, material, color, proportions, markings, and pose as fixed. Preserve identity, placement, wardrobe or product details, and lighting direction. Request continuous coherent motion; prohibit substitutions, extra limbs or objects, text artifacts, morphing, and abrupt cuts.

Example shape: “Preserve the supplied [subject] exactly: [immutable traits]. In [setting], make one slow [camera move] while the subject remains [placement/pose]. Maintain [lighting and finish]. Continuous shot only; no cuts, morphing, redesign, or new objects.”

## Frame stability

Define both endpoint frames. Start from a composed, fully readable subject with no motion blur; end with the same subject still recognizable, with a deliberate final composition and enough settling time to hold it. Avoid opening or ending mid-turn, cropped faces or products, snap zooms, and an endpoint that changes the subject's identity.

## Camera vocabulary

Use luxury motion sparingly: a slow dolly-in for invitation, a measured orbit for form, a gentle crane for reveal, and foreground parallax for depth. Ask for smooth, stabilized, restrained movement with a single dominant direction. Prefer slow acceleration and deceleration over energetic handheld, whip, or jittery moves.

## Horizontal and mobile-safe framing

Generate horizontal masters. Keep the subject and all critical action in the center-safe region so a mobile crop preserves the silhouette, face, product, and focal detail. Leave protected side margins for responsive crops; do not place text or required visual information at the edges.

## Provider selection

Select a capability based on its documented ability to preserve a reference subject, honor start/end frames, sustain a stable camera path, render the requested aspect ratio, and produce sufficient duration and resolution. Favor controllability and temporal consistency over novelty. Check only the host's required cost, authorization, latency, watermark, and export constraints; do not perform an assistant-side copyright or unrelated-image-information audit.

## One-retry correction contract

Allow one corrective retry only. Diagnose the first output against the shot plan, then issue a concise delta prompt naming the failed requirement and the required correction—for example, “retain the original chair silhouette; slow the orbit; keep the final frame centered.” Keep all approved constraints unchanged. If the retry still fails, stop and surface alternatives rather than silently iterating.
