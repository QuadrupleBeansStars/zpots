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

  // Top-nav items (Venue Manager → Courts, Slot Control → Slots, AI Insights → AI)
  for (const [linkLabel, expectedHeading] of [
    ['Courts',   /Manage Courts/i],
    ['Slots',    /Slot Control/i],
    ['Pricing',  /Pricing Setup/i],
    ['Bookings', /^Bookings$/i],
    ['AI',       /AI Insights/i],
  ] as const) {
    await page.getByRole('link', { name: linkLabel, exact: true }).click();
    await expect(page.getByRole('heading', { name: expectedHeading })).toBeVisible();
  }

  // Optimization removed from nav; access via direct URL
  await page.goto('/owner/optimization');
  await expect(page.getByRole('heading', { name: /Optimization Engine/i })).toBeVisible();
});
