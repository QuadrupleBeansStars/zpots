import { test, expect } from '@playwright/test';

test('player can book a court end-to-end', async ({ page }) => {
  // 1. Landing
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toContainText('ZPOTS');

  // 2. Enter as Player — landing's RoleCard links to /player/login.
  await page.getByRole('button', { name: /Enter as Player/i }).click();
  await expect(page).toHaveURL(/\/player\/login$/);

  // 3. Log in (form-UI-only — accepts the prefilled demo creds)
  await page.getByRole('button', { name: /^LOG IN$/i }).click();
  await expect(page).toHaveURL(/\/player$/);
  await expect(page.getByRole('heading', { name: /Discover/i })).toBeVisible();

  // 4. Go to search, filter by Badminton
  await page.goto('/player/search');
  await expect(page.getByRole('heading', { name: /Find Your Court/i })).toBeVisible();
  await page.getByRole('button', { name: 'Badminton', exact: true }).click();
  await expect(page).toHaveURL(/sport=Badminton/);

  // 5. Open the badminton court directly
  await page.goto('/player/courts/bbc-01');
  await expect(page.getByRole('heading', { name: /BANGKOK BADMINTON CENTER/i })).toBeVisible();

  // 6. Pick a slot (08:00 should be free on any future date)
  await page.getByRole('button', { name: /^08:00/ }).first().click();

  // 7. Proceed to booking
  await page.getByRole('link', { name: /PROCEED TO BOOKING/i }).click();
  await expect(page).toHaveURL(/\/book\?date=/);

  // 8. Confirm
  await page.getByRole('button', { name: /Confirm & Pay/i }).click();
  await expect(page).toHaveURL(/\/bookings\/ZP-\d{5}\/confirmation$/);
  await expect(page.getByRole('heading', { name: /Booking/i }).first()).toBeVisible();

  // 9. Navigate to My Bookings and confirm the new booking is listed
  await page.goto('/player/bookings');
  await expect(page.getByText('Bangkok Badminton Center').first()).toBeVisible();
});
