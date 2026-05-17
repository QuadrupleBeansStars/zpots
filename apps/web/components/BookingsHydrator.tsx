'use client';
import { useEffect } from 'react';

import { useBookingStore } from '@/lib/booking-store';

type Props = { userId: number };

/**
 * Calls the booking store's hydrate() once on mount. Runs at the layout level
 * so /player/* and /owner/* pages can rely on `useBookingStore` being populated.
 */
export function BookingsHydrator({ userId }: Props) {
  useEffect(() => {
    useBookingStore.getState().hydrate(userId);
  }, [userId]);

  return null;
}
