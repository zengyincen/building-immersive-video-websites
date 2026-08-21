export function clamp(value, minimum = 0, maximum = 1) {
  return Math.min(Math.max(value, minimum), maximum);
}

export function expEase(current, target, response, deltaSeconds) {
  const alpha = 1 - Math.exp(-Math.max(0, response) * Math.max(0, deltaSeconds));
  return current + (target - current) * alpha;
}

export function pointerToNormalized(pointer, rect) {
  const width = Math.max(0, rect.width);
  const height = Math.max(0, rect.height);

  return [
    width === 0 ? 0 : clamp((pointer.clientX - rect.left) / width),
    height === 0 ? 0 : clamp((pointer.clientY - rect.top) / height),
  ];
}

export function timeForProgress(progress, duration) {
  return clamp(progress) * Math.max(0, duration);
}

export function interpolateEyeTrack(track, time) {
  if (!track.length) return null;

  const clampedTime = clamp(time, track[0].t, track.at(-1).t);
  const nextIndex = track.findIndex((keyframe) => keyframe.t >= clampedTime);
  const end = track[nextIndex === -1 ? track.length - 1 : nextIndex];
  const start = track[Math.max(0, nextIndex - 1)];
  const span = end.t - start.t;
  const progress = span === 0 ? 0 : (clampedTime - start.t) / span;

  return {
    left: interpolatePoint(start.left, end.left, progress),
    right: interpolatePoint(start.right, end.right, progress),
    radius: interpolateNumber(start.radius, end.radius, progress),
    visible: start.visible && end.visible,
  };
}

export function pupilOffset(anchor, pointer, radius) {
  const safeAnchor = anchor.map((value) => clamp(value));
  const safePointer = pointer.map((value) => clamp(value));
  const deltaX = safePointer[0] - safeAnchor[0];
  const deltaY = safePointer[1] - safeAnchor[1];
  const distance = Math.hypot(deltaX, deltaY);
  const maximumDistance = Math.max(0, radius);

  if (distance === 0 || maximumDistance === 0) return [0, 0];

  const scale = maximumDistance / distance;
  return [deltaX * scale, deltaY * scale];
}

function interpolateNumber(start, end, progress) {
  return start + (end - start) * progress;
}

function interpolatePoint(start, end, progress) {
  return [
    clamp(interpolateNumber(start[0], end[0], progress)),
    clamp(interpolateNumber(start[1], end[1], progress)),
  ];
}
