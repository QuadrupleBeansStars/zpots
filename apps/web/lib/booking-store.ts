import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { Booking, BookingDraft } from './types';

export function generateTxnId(): string {
  const n = Math.floor(Math.random() * 90000) + 10000;
  return `ZP-${n}`;
}

type State = {
  bookings: Booking[];
  addBooking: (draft: BookingDraft) => string;
  addBookingWithTxn: (txnId: string, draft: BookingDraft) => string;
  cancelBooking: (txnId: string) => void;
  getByTxn: (txnId: string) => Booking | undefined;
};

export const useBookingStore = create<State>()(
  persist(
    (set, get) => ({
      bookings: [],

      addBooking: (draft) => {
        const txnId = generateTxnId();
        return get().addBookingWithTxn(txnId, draft);
      },

      addBookingWithTxn: (txnId, draft) => {
        const existing = get().bookings.find((b) => b.txn_id === txnId);
        if (existing) return existing.txn_id;
        const next: Booking = {
          id: get().bookings.length + 1,
          txn_id: txnId,
          court_id: draft.court_id,
          court_name: draft.court_name,
          date: draft.date,
          time_start: draft.time_start,
          time_end: draft.time_end,
          duration: draft.duration,
          total_price: draft.total_price,
          status: 'CONFIRMED',
          created_at: new Date().toISOString(),
        };
        set({ bookings: [...get().bookings, next] });
        return txnId;
      },

      cancelBooking: (txnId) => {
        set({
          bookings: get().bookings.map((b) =>
            b.txn_id === txnId ? { ...b, status: 'CANCELLED' } : b,
          ),
        });
      },

      getByTxn: (txnId) => get().bookings.find((b) => b.txn_id === txnId),
    }),
    {
      name: 'zpots.bookings.v1',
      storage: createJSONStorage(() => localStorage),
    },
  ),
);
