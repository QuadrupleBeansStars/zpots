import { create } from 'zustand';
import type { Booking, BookingDraft } from './types';
import { cancelBookingApi, createBooking, getBookings } from './data-client';

export function generateTxnId(): string {
  const n = Math.floor(Math.random() * 90000) + 10000;
  return `ZP-${n}`;
}

type State = {
  bookings: Booking[];
  hydrated: boolean;
  hydrate: (userId: number) => Promise<void>;
  addBooking: (userId: number, draft: BookingDraft) => Promise<string>;
  addBookingWithTxn: (txnId: string, draft: BookingDraft) => string;
  cancelBooking: (txnId: string) => Promise<void>;
  getByTxn: (txnId: string) => Booking | undefined;
};

export const useBookingStore = create<State>()((set, get) => ({
  bookings: [],
  hydrated: false,

  hydrate: async (userId) => {
    try {
      const rows = await getBookings({ user_id: userId });
      // Backend rows lack the frontend's `id` (sequential number) and
      // `created_at` fields. Synthesize them so consumers don't have to
      // deal with optional fields.
      const hydrated: Booking[] = rows.map((r, i) => ({
        id: i + 1,
        txn_id: r.txn_id,
        court_id: r.court_id,
        court_name: r.court_name,
        date: r.date,
        time_start: r.time_start,
        time_end: r.time_end,
        duration: r.duration,
        total_price: r.total_price,
        status: r.status,
        created_at: new Date().toISOString(),
      }));
      set({ bookings: hydrated, hydrated: true });
    } catch {
      // Leave cache empty if hydration fails; pages render empty state.
      set({ hydrated: true });
    }
  },

  addBooking: async (userId, draft) => {
    const row = await createBooking({
      user_id: userId,
      court_id: draft.court_id,
      date: draft.date,
      time_start: draft.time_start,
      duration: draft.duration,
    });
    const next: Booking = {
      id: get().bookings.length + 1,
      txn_id: row.txn_id,
      court_id: row.court_id,
      court_name: row.court_name,
      date: row.date,
      time_start: row.time_start,
      time_end: row.time_end,
      duration: row.duration,
      total_price: row.total_price,
      status: row.status,
      created_at: new Date().toISOString(),
    };
    set({ bookings: [...get().bookings, next] });
    return row.txn_id;
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

  cancelBooking: async (txnId) => {
    try {
      const row = await cancelBookingApi(txnId);
      set({
        bookings: get().bookings.map((b) =>
          b.txn_id === txnId ? { ...b, status: row.status } : b,
        ),
      });
    } catch {
      // Optimistic local cancel as a fallback so the UI doesn't get stuck.
      set({
        bookings: get().bookings.map((b) =>
          b.txn_id === txnId ? { ...b, status: 'CANCELLED' } : b,
        ),
      });
    }
  },

  getByTxn: (txnId) => get().bookings.find((b) => b.txn_id === txnId),
}));
