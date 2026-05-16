/** Types mirroring `data/dummy_data.py`. Keep in sync with the FastAPI Pydantic schemas. */

export type Amenity = { icon: string; label: string; value: string };

export type CourtUnit = { number: string; surface: string };

export type Court = {
  id: string;
  name: string;
  short_name: string;
  sport: 'Badminton' | 'Football' | 'Basketball' | 'Padel' | 'Tennis' | string;
  rating: number;
  reviews: number;
  location: string;
  address: string;
  district: string;
  price_per_hour: number;
  prime_price: number;
  amenities: Amenity[];
  surface: string;
  status: 'ACTIVE' | 'MAINTENANCE' | string;
  utilization: number;
  peak_hours: string;
  ai_efficiency: 'Elite' | 'High' | 'Moderate' | string;
  tags: string[];
  color: string;
  courts: CourtUnit[];
};

export type TimeSlot = {
  time_start: string;
  time_end: string;
  price: number;
  status: 'available' | 'booked' | 'maintenance';
  ai_tag?: string | null;
};

export type PlayerBooking = {
  id: string;
  court_id: string;
  court_name: string;
  court_number: string;
  surface: string;
  date: string;
  date_full: string;
  time_start: string;
  time_end: string;
  duration_min: number;
  status: 'CONFIRMED' | 'CANCELLED' | 'COMPLETED';
  base_price: number;
  discount: number;
  service_fee: number;
  total: number;
  payment_method: string;
  ai_verified: boolean;
  team_members: string[];
  qr_code: string;
  address: string;
  address_note: string;
  color: string;
};

export type OwnerVenue = {
  id: string;
  name: string;
  location: string;
  courts_count: number;
  revenue_today: number;
  color: string;
};

export type DistrictDemand = { name: string; demand: number; level: 'Peak' | 'Moderate' | 'Saturated' };
