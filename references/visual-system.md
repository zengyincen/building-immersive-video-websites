# Visual system

This starter takes cues from premium industrial design: a dark, sparse stage, high-contrast type, precise spacing, and restrained material light. It does not copy any company’s product, page structure, marks, imagery, or trade dress. Use one confident object or frame per scene, let negative space carry hierarchy, and give the primary action an obvious keyboard focus state.

## Material and type

- Use near-black and mineral neutrals as the field, an off-white reading color, and one limited luminous accent. Gradients should suggest metal, glass, or depth—not decoration for its own sake.
- Prefer a system sans stack, modest all-caps metadata, and large, tightly tracked display text. Keep body copy short and comfortably line-spaced.
- Set spacing with `clamp()` tokens, hairline separators, and a small number of breakpoints. The mobile composition may change, but it should retain the same focal hierarchy.

## Rendering and media

The default is CSS/DOM 2.5D: layered gradients, pseudo-elements, perspective, and transform-only motion. Upgrade to WebGL only after it provides a measured visual benefit that CSS cannot deliver, and retain the static CSS poster as the baseline. Scope visual state to each scene with data attributes and CSS custom properties; avoid global selectors that can leak between embeds.

Load critical poster art with an explicit preload only when it appears in the first viewport. Preload video metadata—not full media—until a direct user intent, and use a real poster image or the composed static fallback before the video is ready. Warm a viewport-bound video shortly before it enters view, then release it when it is far outside the viewport. Never show a blank or broken player because a manifest is empty or unavailable.

## Interaction discipline

Raw pointer and scroll listeners write targets only; a single `requestAnimationFrame` loop performs visual writes. Prefer opacity and `translate3d`/transform changes over layout, filter, or repeated style reads. Keep scroll scrub, mouse scrub, and triggered playback as separate modes. When a triggered playback request is superseded, cancel only the controller for that active section so other sections cannot be interrupted accidentally.

Fine-pointer hover may reveal a follower, highlight, image reveal, or eye overlay. On touch, those affordances must remain reachable through semantic buttons, tap, and keyboard focus; never attach continuous gaze tracking to a scroll gesture. Visible focus rings are mandatory, and all controls need a plain-language state label.

For `prefers-reduced-motion`, set a root state, stop continuous transforms, remove decorative followers and eye tracking, and keep a deliberate static poster plus direct controls. Motion is progressive enhancement, not the only way to understand or use the page.
