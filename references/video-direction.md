# Video direction for immersive fly-throughs

Use this reference only when generating or optimizing video. A supplied video skips it unless optimization guidance is needed.

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

Select a provider based on its demonstrated ability to preserve a reference subject, honor start/end frames, sustain a stable camera path, render the requested aspect ratio, and produce sufficient duration and resolution. Favor controllability and temporal consistency over novelty. Confirm rights, cost, latency, watermark policy, and export constraints before committing.

## One-retry correction contract

Allow one corrective retry only. Diagnose the first output against the shot plan, then issue a concise delta prompt naming the failed requirement and the required correction—for example, “retain the original chair silhouette; slow the orbit; keep the final frame centered.” Keep all approved constraints unchanged. If the retry still fails, stop and surface alternatives rather than silently iterating.
