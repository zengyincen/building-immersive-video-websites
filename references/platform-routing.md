# Platform Capability Routing

Use this contract before generating motion from a static image or invoking an
asynchronous media workflow.

## Capability order

Select capabilities by their documented descriptions, never by guessed or
invented names. Search in this order:

1. Native builder tools registered in the current environment.
2. Installed skills, MCP servers, and CLI tools available in the current environment.
3. Configured API integrations documented as available to the current environment.

Choose only a capability whose description states that it accepts the required
source input and returns a downloadable video. Do not substitute a different
media type or capability merely because its name sounds suitable.

For an ordered image sequence, search specifically for documented start-frame /
end-frame, first-frame / last-frame, reference-frame, or image-sequence input.
Use the capability's actual contract; never claim exact endpoint continuity when
the host does not expose a matching input path.
After generation, treat those adjacent outputs as bridge assets and assemble
them into one durable master background film before building the page. The page
must not use one generated clip per image or per scroll chapter; use
`scripts/assemble-master-video.py` (or a verified equivalent) and retain its
assembly manifest.

## Input inspection boundary

Treat user-supplied images as creative inputs. Inspect only technical properties
needed to decode, generate, or render them. Do not perform assistant-side
copyright/ownership checks or infer EXIF, identity, location, hidden metadata, or
other unrelated image information, and do not pause for those details. Platform-
required safety, consent, or authorization checks remain in force and must not be
bypassed.

## Authorization and durable output

Use included credits when the selected capability documents that they cover the
work. Ask for confirmation before work that adds charges or requires new
credentials. A generation is successful only after its returned media has been
downloaded to a durable project path and recorded in the media manifest; a job
completion signal alone is not success.

For an asynchronous job, persist its job ID and request metadata before polling.
Poll only within the provider's documented interval and a stated bounded attempt
or time limit. On a transient failure, make one targeted retry only, preserving
the original job record. Report a terminal failure with the job ID, attempted
capability, and the last provider status.

## Direct and unavailable paths

When an existing video is supplied, inspect it and use it directly; do not
generate a replacement. If no available capability's description supports the
requested input-to-downloadable-video path, stop and provide a failure report
listing the searched capability categories, why each candidate was unsuitable,
and the unavailable requirement.
