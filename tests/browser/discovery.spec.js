import { test, expect } from '@playwright/test';
test('discovery queue searches, filters, resets and exports with no qualification inflation', async ({page}) => {
  const errors = []; page.on('pageerror', e => errors.push(e.message));
  await page.goto('/discovery.html');
  await expect(page.locator('.lead')).toHaveCount(50);
  await page.locator('#query').fill('Ho Pronamic');
  await expect(page.locator('.lead')).toHaveCount(1);
  await expect(page.locator('.lead')).toContainText('Suspension flagged');
  await page.getByRole('button',{name:'Reset',exact:true}).click();
  await page.locator('#stage').selectOption('checked');
  await expect(page.locator('.lead')).toHaveCount(4);
  const dl = page.waitForEvent('download');
  await page.getByRole('button',{name:'Export visible CSV'}).click();
  expect((await dl).suggestedFilename()).toBe('sunset-discovery-wave17.csv');
  await page.locator('#stage').selectOption('unread');
  await expect(page.locator('.lead')).toHaveCount(46);
  await page.locator('#query').fill('not-a-real-lead');
  await expect(page.locator('#queue')).toContainText('No leads match');
  expect(errors).toEqual([]);
});
test('discovery works on mobile and opens source evidence', async ({page}) => {
  await page.setViewportSize({width:390,height:844});
  await page.goto('/discovery.html');
  await expect(page.locator('.lead')).toHaveCount(50);
  await page.locator('#stage').selectOption('suspended');
  await page.locator('.lead summary').click();
  await expect(page.locator('.lead')).toContainText('Contractors Bond Suspension');
  const width = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(width).toBeLessThanOrEqual(390);
  await expect(page.locator('.lead-links a').first()).toHaveAttribute('href', /data.sf.gov/);
});
test('discovery handles unavailable evidence without claiming an empty successful search', async ({page}) => {
  await page.route('**/data/wave17.json', route => route.fulfill({status:503,body:'unavailable'}));
  await page.goto('/discovery.html');
  await expect(page.locator('#result-count')).toHaveText('Discovery could not load.');
  await expect(page.locator('#export')).toBeDisabled();
});
