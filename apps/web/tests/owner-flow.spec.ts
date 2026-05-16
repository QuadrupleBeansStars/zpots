import { test, expect } from '@playwright/test';

test('owner can sign in and navigate the sidebar', async ({ page }) => {
  // Landing → Enter as Owner
  await page.goto('/');
  await page.getByRole('button', { name: /Enter as Owner/i }).click();
  await expect(page).toHaveURL(/\/owner-login$/);

  // Submit login (prefilled creds)
  await page.getByRole('button', { name: /ENTER CONSOLE/i }).click();
  await expect(page).toHaveURL(/\/owner$/);

  // Dashboard heading
  await expect(page.getByRole('heading', { name: /Venue Performance/i })).toBeVisible();

  // Sidebar items
  for (const [linkLabel, expectedHeading] of [
    ['Venue Manager', /Manage Courts/i],
    ['Slot Control',  /Slot Control/i],
    ['Pricing',       /Pricing Setup/i],
    ['Bookings',      /^Bookings$/i],
    ['AI Insights',   /AI Insights/i],
    ['Optimization',  /Optimization Engine/i],
  ] as const) {
    await page.getByRole('link', { name: linkLabel, exact: false }).click();
    await expect(page.getByRole('heading', { name: expectedHeading })).toBeVisible();
  }
});
