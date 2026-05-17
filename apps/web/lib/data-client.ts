import type { Court, Booking } from './types';

export type CreateBookingRequest = {
  user_id: number;
  court_id: string;
  date: string;
  time_start: string;
  duration: number;
  player_name?: string;
};

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`/api${path}`);
  if (!res.ok) throw new Error(`GET /api${path} failed: ${res.status}`);
  return res.json();
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`/api${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`POST /api${path} failed: ${res.status}${text ? ` — ${text}` : ''}`);
  }
  return res.json();
}

export const getCourts = () => fetchJson<Court[]>('/courts');
export const getCourt = (id: string) => fetchJson<Court>(`/courts/${id}`);

export type BookingsQuery = { user_id?: number; court_id?: string; status?: string };
export function getBookings(params: BookingsQuery = {}): Promise<Booking[]> {
  const qs = new URLSearchParams();
  if (params.user_id !== undefined) qs.set('user_id', String(params.user_id));
  if (params.court_id) qs.set('court_id', params.court_id);
  if (params.status) qs.set('status', params.status);
  const suffix = qs.toString() ? `?${qs}` : '';
  return fetchJson<Booking[]>(`/bookings${suffix}`);
}

export const createBooking = (req: CreateBookingRequest) =>
  postJson<Booking>('/bookings', req);

export const cancelBookingApi = (txnId: string) =>
  postJson<Booking>(`/bookings/${txnId}/cancel`, {});
