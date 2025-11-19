import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('index.html');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Maximum PC Builds Archive/);
});