import {clamp, expEase, interpolateEyeTrack, pointerToNormalized, pupilOffset, timeForProgress} from './interaction-core.mjs';

const root = document.documentElement;
const scene = document.querySelector('[data-pointer-scene]');
const follower = document.querySelector('[data-pointer-follower]');
const hotspot = document.querySelector('[data-hotspot]');
const hotspotDetail = document.querySelector('[data-hotspot-detail]');
const stage = document.querySelector('[data-media-stage]');
const status = document.querySelector('[role="status"]');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const hasFineHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
const eyeTrack = [{t: 0, left: [.64, .48], right: [.705, .48], radius: .011, visible: true}];

const state = {active: false, pointer: [.5, .5], renderedPointer: [.5, .5], scrollProgress: 0, frame: 0, lastFrame: performance.now()};
const playback = {activeSection: null, controller: null};

function setMotionPreference() {
  root.dataset.motion = prefersReducedMotion.matches ? 'reduced' : 'full';
  if (prefersReducedMotion.matches) {
    cancelAnimationFrame(state.frame);
    state.frame = 0;
    follower.dataset.active = 'false';
    state.active = false;
  } else if (!state.frame) {
    state.lastFrame = performance.now();
    state.frame = requestAnimationFrame(renderFrame);
  }
}

function updatePointerTarget(event) {
  state.pointer = pointerToNormalized(event, scene.getBoundingClientRect());
  state.active = true;
}

function clearPointerTarget() {
  state.active = false;
  state.pointer = [.5, .5];
}

function updateScrollTarget() {
  const extent = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
  state.scrollProgress = clamp(window.scrollY / extent);
}

function renderFrame(now) {
  const delta = Math.min(.1, Math.max(0, (now - state.lastFrame) / 1000));
  state.lastFrame = now;
  state.renderedPointer = state.renderedPointer.map((value, index) => expEase(value, state.pointer[index], 12, delta));
  const [x, y] = state.renderedPointer;
  root.style.setProperty('--pointer-x', `${x * window.innerWidth}px`);
  root.style.setProperty('--pointer-y', `${y * window.innerHeight}px`);
  scene.style.setProperty('--reveal-x', `${x * 100}%`);
  scene.style.setProperty('--reveal-y', `${y * 100}%`);
  scene.style.setProperty('--tilt-x', `${(y - .5) * -5}deg`);
  scene.style.setProperty('--tilt-y', `${(x - .5) * 5}deg`);
  follower.dataset.active = String(state.active && hasFineHover);
  const anchors = interpolateEyeTrack(eyeTrack, timeForProgress(state.scrollProgress, 0));
  const offset = anchors ? pupilOffset(anchors.left, state.renderedPointer, anchors.radius) : [0, 0];
  root.style.setProperty('--pupil-x', `${offset[0] * scene.clientWidth}px`);
  root.style.setProperty('--pupil-y', `${offset[1] * scene.clientHeight}px`);
  state.frame = requestAnimationFrame(renderFrame);
}

function toggleHotspot() {
  const open = hotspot.getAttribute('aria-expanded') !== 'true';
  hotspot.setAttribute('aria-expanded', String(open));
  hotspotDetail.hidden = !open;
}

function requestTriggeredPlayback(section, video) {
  if (playback.activeSection !== section) {
    playback.controller?.abort();
    playback.activeSection = section;
    playback.controller = new AbortController();
  }
  const {signal} = playback.controller;
  video.play().catch(() => {
    if (!signal.aborted) status.textContent = 'Playback needs a direct user gesture on this device.';
  });
}

function cancelTriggeredPlayback(section, video) {
  if (playback.activeSection !== section) return;
  playback.controller?.abort();
  playback.controller = null;
  playback.activeSection = null;
  video.pause();
}

function installLocalMedia(media) {
  const item = media.find(({src}) => typeof src === 'string' && src.startsWith('./'));
  if (!item) return;
  const video = document.createElement('video');
  video.controls = true;
  video.muted = true;
  video.playsInline = true;
  video.preload = 'metadata';
  video.poster = item.poster || '';
  video.src = item.src;
  video.addEventListener('pointerenter', () => requestTriggeredPlayback(scene, video), {passive: true});
  video.addEventListener('pointerleave', () => cancelTriggeredPlayback(scene, video), {passive: true});
  stage.prepend(video);
  status.textContent = 'Local media is ready. Hover to preview or use native controls.';
}

async function loadManifest() {
  try {
    const response = await fetch('./media-manifest.json');
    const manifest = await response.json();
    installLocalMedia(Array.isArray(manifest.media) ? manifest.media : []);
  } catch {
    status.textContent = 'Media manifest unavailable. The static poster remains available.';
  }
}

setMotionPreference();
prefersReducedMotion.addEventListener('change', setMotionPreference);
scene.addEventListener('pointermove', updatePointerTarget, {passive: true});
scene.addEventListener('pointerenter', updatePointerTarget, {passive: true});
scene.addEventListener('pointerleave', clearPointerTarget, {passive: true});
scene.addEventListener('focusin', () => { state.active = hasFineHover; }, {passive: true});
window.addEventListener('scroll', updateScrollTarget, {passive: true});
hotspot.addEventListener('click', toggleHotspot);
hotspot.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    toggleHotspot();
  }
});
updateScrollTarget();
loadManifest();
