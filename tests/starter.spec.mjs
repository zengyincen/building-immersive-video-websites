import {expect, test} from '@playwright/test';

test('pointer updates the follower and leaving resets it', async ({page}) => {
  await page.goto('/');
  const scene = page.locator('[data-pointer-scene]');
  await scene.hover({position: {x: 700, y: 250}});
  await page.waitForTimeout(100);
  await expect(page.locator('[data-pointer-follower]')).toHaveAttribute('data-active', 'true');
  await page.locator('footer').hover();
  await expect(page.locator('[data-pointer-follower]')).toHaveAttribute('data-active', 'false');
});

test('reduced motion exposes a static experience', async ({browser}) => {
  const context = await browser.newContext({reducedMotion: 'reduce'});
  const page = await context.newPage();
  await page.goto('/');
  await expect(page.locator('html')).toHaveAttribute('data-motion', 'reduced');
  await context.close();
});

test('an empty media manifest keeps the hero in its designed static fallback', async ({page}) => {
  await page.goto('/');
  await expect(page.getByRole('status')).toContainText('A new perspective is ready to explore');
  await expect(page.locator('[data-media-stage] video')).toHaveCount(0);
});

test('visitor copy does not expose implementation or demo language', async ({page}) => {
  await page.goto('/');
  const bodyText = await page.locator('body').innerText();
  expect(bodyText).not.toMatch(/Play it straight through|No media has been assigned|Vanilla immersive starter|media manifest|scroll-scrub|triggered-playback/i);
});

test('topic content uses one persistent background scene layer', async ({page}) => {
  await page.goto('/');
  await expect(page.locator('[data-scene-background]')).toHaveCount(1);
  await expect(page.locator('[data-scene-foreground]')).toHaveCount(1);
  await expect(page.locator('[data-scene-background]')).toHaveCSS('position', 'sticky');
  const sceneOrder = await page.locator('main').evaluate((main) =>
    [...main.children].map((child) => child.getAttribute('data-scene-background') !== null ? 'background' : child.getAttribute('data-scene-foreground') !== null ? 'foreground' : 'other'));
  expect(sceneOrder.slice(0, 2)).toEqual(['background', 'foreground']);
});

test('a master manifest mounts one background video and ignores bridge players', async ({page}) => {
  await page.route('**/media-manifest.json', async (route) => {
    await route.fulfill({
      contentType: 'application/json',
      body: JSON.stringify({
        masterBackgroundVideo: {
          src: './media/master-background-film.mp4',
          role: 'persistent-background-video',
          background: true,
          interaction: 'persistent-ambient-background',
        },
        media: [
          {src: './media/image-01-to-image-02.mp4', background: true, role: 'bridge-intermediate'},
          {src: './media/image-02-to-image-03.mp4', background: true, role: 'bridge-intermediate'},
        ],
      }),
    });
  });
  await page.route('**/media/master-background-film.mp4', async (route) => {
    await route.fulfill({status: 200, contentType: 'video/mp4', body: Buffer.alloc(0)});
  });
  await page.goto('/');
  await expect(page.locator('[data-scene-background] video')).toHaveCount(1);
  await expect(page.locator('[data-scene-background] video')).toHaveAttribute('data-master-background', 'true');
  await expect(page.locator('[data-media-stage] video')).toHaveCount(0);
});
