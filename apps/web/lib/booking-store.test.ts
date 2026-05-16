import { describe, it, expect, beforeEach } from 'vitest';
import { useBookingStore, generateTxnId } from './booking-store';

beforeEach(() => {
  localStorage.clear();
  useBookingStore.setState({ bookings: [] });
});

describe('generateTxnId', () => {
  it('returns a string like ZP-NNNNN', () => {
    expect(generateTxnId()).toMatch(/^ZP-\d{5}$/);
  });
});

describe('useBookingStore', () => {
  it('starts empty', () => {
    expect(useBookingStore.getState().bookings).toEqual([]);
  });

  it('addBooking appends a Booking derived from a draft', () => {
    const txn = useBookingStore.getState().addBooking({
      court_id: 'bbc-01',
      court_name: 'Bangkok Badminton Center',
      date: '2099-01-01',
      time_start: '18:00',
      time_end: '19:00',
      duration: 1,
      total_price: 450,
    });
    const stored = useBookingStore.getState().bookings;
    expect(stored).toHaveLength(1);
    expect(stored[0].txn_id).toBe(txn);
    expect(stored[0].status).toBe('CONFIRMED');
    expect(stored[0].id).toBe(1);
  });

  it('addBooking is idempotent when called twice with the same txn_id', () => {
    const draft = {
      court_id: 'bbc-01',
      court_name: 'Bangkok Badminton Center',
      date: '2099-01-01',
      time_start: '18:00',
      time_end: '19:00',
      duration: 1,
      total_price: 450,
    };
    const t1 = useBookingStore.getState().addBookingWithTxn('ZP-12345', draft);
    const t2 = useBookingStore.getState().addBookingWithTxn('ZP-12345', draft);
    expect(t1).toBe('ZP-12345');
    expect(t2).toBe('ZP-12345');
    expect(useBookingStore.getState().bookings).toHaveLength(1);
  });

  it('cancelBooking flips status to CANCELLED', () => {
    const txn = useBookingStore.getState().addBooking({
      court_id: 'bbc-01',
      court_name: 'BBC',
      date: '2099-01-01',
      time_start: '18:00',
      time_end: '19:00',
      duration: 1,
      total_price: 450,
    });
    useBookingStore.getState().cancelBooking(txn);
    const stored = useBookingStore.getState().bookings;
    expect(stored[0].status).toBe('CANCELLED');
  });

  it('getByTxn returns the matching booking', () => {
    const txn = useBookingStore.getState().addBooking({
      court_id: 'bbc-01',
      court_name: 'BBC',
      date: '2099-01-01',
      time_start: '18:00',
      time_end: '19:00',
      duration: 1,
      total_price: 450,
    });
    expect(useBookingStore.getState().getByTxn(txn)?.court_id).toBe('bbc-01');
    expect(useBookingStore.getState().getByTxn('nope')).toBeUndefined();
  });
});
