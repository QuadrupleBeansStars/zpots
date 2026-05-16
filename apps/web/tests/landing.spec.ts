import { test, expect } from '@playwright/test';

test('landing renders the role picker', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { level: 1 })).toContainText('ZPOTS');
  await expect(page.getByRole('heading', { name: "I'm a Player" })).toBeVisible();
  await expect(page.getByRole('heading', { name: "I'm a Court Owner" })).toBeVisible();
  await expect(page.getByRole('button', { name: /Enter as Player/i })).toBeVisible();
  await expect(page.getByRole('button', { name: /Enter as Owner/i })).toBeVisible();
  await expect(page.getByText('KINETIC PRECISION ENGINEERED')).toBeVisible();
});
