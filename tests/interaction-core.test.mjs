import assert from 'node:assert/strict';
import test from 'node:test';

import {
  clamp,
  expEase,
  interpolateEyeTrack,
  pointerToNormalized,
  pupilOffset,
  timeForProgress,
} from '../assets/vanilla-starter/interaction-core.mjs';

test('clamp limits values to its supplied range', () => {
  assert.equal(clamp(-4, -2, 3), -2);
  assert.equal(clamp(1, -2, 3), 1);
  assert.equal(clamp(9, -2, 3), 3);
});

test('expEase is frame-rate independent for a fixed elapsed time', () => {
  const oneStep = expEase(0, 10, 4, 1);
  const twoSteps = expEase(expEase(0, 10, 4, 0.5), 10, 4, 0.5);
  assert.ok(Math.abs(oneStep - twoSteps) < 0.0000001);
  assert.equal(expEase(4, 10, 0, 1), 4);
});

test('pointerToNormalized clamps coordinates to a target rectangle', () => {
  assert.deepEqual(
    pointerToNormalized({clientX: 250, clientY: 0}, {left: 50, top: 25, width: 100, height: 50}),
    [1, 0],
  );
});

test('timeForProgress clamps before mapping', () => {
  assert.equal(timeForProgress(-1, 8), 0);
  assert.equal(timeForProgress(0.5, 8), 4);
  assert.equal(timeForProgress(2, 8), 8);
});

test('interpolateEyeTrack follows moving anchors', () => {
  const track = [
    {t: 0, left: [0.4, 0.3], right: [0.5, 0.3], radius: 0.01, visible: true},
    {t: 2, left: [0.6, 0.5], right: [0.7, 0.5], radius: 0.02, visible: true},
  ];
  assert.deepEqual(interpolateEyeTrack(track, 1), {
    left: [0.5, 0.4], right: [0.6, 0.4], radius: 0.015, visible: true,
  });
});

test('interpolateEyeTrack hides eyes around an invisible keyframe', () => {
  const track = [
    {t: 0, left: [0.4, 0.3], right: [0.5, 0.3], radius: 0.01, visible: true},
    {t: 2, left: [0.6, 0.5], right: [0.7, 0.5], radius: 0.02, visible: false},
  ];
  assert.equal(interpolateEyeTrack(track, 1).visible, false);
});

test('interpolateEyeTrack clamps normalized eye coordinates', () => {
  const track = [
    {t: 0, left: [-0.2, 1.2], right: [1.3, -0.1], radius: 0.01, visible: true},
  ];
  assert.deepEqual(interpolateEyeTrack(track, 0), {
    left: [0, 1], right: [1, 0], radius: 0.01, visible: true,
  });
});

test('pupilOffset never exceeds the eye radius', () => {
  const offset = pupilOffset([0.5, 0.5], [1, 1], 0.02);
  assert.ok(Math.hypot(offset[0], offset[1]) <= 0.0200001);
});

test('pupilOffset follows normalized pointer direction at the supplied radius', () => {
  const offset = pupilOffset([0.5, 0.5], [1, 0.5], 0.02);
  assert.deepEqual(offset, [0.02, 0]);
});
