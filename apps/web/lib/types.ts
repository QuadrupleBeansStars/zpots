import type { Court, Amenity, TimeSlot } from '@/components/types';

export type { Court, Amenity, TimeSlot };

export type Booking = {
  id: number;
  txn_id: string;
  court_id: string;
  court_name: string;
  date: string;
  time_start: string;
  time_end: string;
  duration: number;
  total_price: number;
  status: 'CONFIRMED' | 'CANCELLED';
  created_at: string;
};

export type BookingDraft = {
  court_id: string;
  court_name: string;
  date: string;
  time_start: string;
  time_end: string;
  duration: number;
  total_price: number;
};
