export type OwnerVenue = {
  id: string;
  name: string;
  location: string;
  courts_count: number;
  revenue_today: number;
  color: string;
};

export type DistrictDemand = {
  name: string;
  demand: number;
  level: 'Peak' | 'Moderate' | 'Saturated';
};

export type TodaysBookingRow = {
  time: string;
  type: string;
  title: string;
  customer: string;
  venue: string;
  status: 'CONFIRMED' | 'IN PROGRESS' | 'UPCOMING' | 'COMPLETED' | 'CANCELLED';
};

export type OwnerBookingRow = {
  customer: string;
  member_id: string;
  court: string;
  sport: string;
  time: string;
  status: 'BOOKED' | 'COMPLETED' | 'CANCELLED';
  avatar_color: string;
};

export type SlotBlock = {
  time: string;
  label: string;
  type: 'booking' | 'maintenance' | 'open';
  color: string;
};

export type DemandCell = {
  day_of_week: number;
  hour: number;
  predicted_bookings: number;
};

export const OWNER_VENUES: OwnerVenue[] = [
  { id: 'venue-01', name: 'Main Arena',         location: 'BANGKOK CENTRAL',      courts_count: 6, revenue_today: 1240, color: '#1a3a2a' },
  { id: 'venue-02', name: 'Ari Sports Center',  location: 'PHAYA THAI, BANGKOK',  courts_count: 4, revenue_today:  890, color: '#1a2a3a' },
  { id: 'venue-03', name: 'Sukhumvit Padel',    location: 'KLONG TOEY, BANGKOK',  courts_count: 3, revenue_today: 2150, color: '#2a1a2a' },
];

export const WEEKLY_UTILIZATION: { day: string; pct: number }[] = [
  { day: 'Mon', pct: 65 },
  { day: 'Tue', pct: 72 },
  { day: 'Wed', pct: 58 },
  { day: 'Thu', pct: 80 },
  { day: 'Fri', pct: 91 },
  { day: 'Sat', pct: 88 },
  { day: 'Sun', pct: 45 },
];

export const DISTRICT_DEMAND: DistrictDemand[] = [
  { name: 'Sukhumvit',    demand: 94, level: 'Peak' },
  { name: 'Ari District', demand: 62, level: 'Moderate' },
  { name: 'Thong Lor',    demand: 98, level: 'Saturated' },
];

export const TODAYS_BOOKINGS: TodaysBookingRow[] = [
  { time: '17:00', type: 'PM', title: 'Padel Championship Practice', customer: 'Amanda S.', venue: 'Sukhumvit Padel',    status: 'CONFIRMED' },
  { time: '18:30', type: 'PM', title: 'Casual Tennis Session',       customer: 'Michael W.', venue: 'Ari Sports Center',  status: 'IN PROGRESS' },
  { time: '20:00', type: 'PM', title: 'Late Night Badminton',        customer: 'Sarah L.',   venue: 'Ari Sports Center',  status: 'UPCOMING' },
];

export const OWNER_BOOKINGS: OwnerBookingRow[] = [
  { customer: 'Marcus Sterling',  member_id: '#ZP-2940', court: 'Center Court',     sport: 'Padel',  time: '14:00 - 15:30 (90 min)',  status: 'BOOKED',    avatar_color: '#506300' },
  { customer: 'Elena Rodriguez',  member_id: '#ZP-5811', court: 'Practice Wall 2',  sport: 'Tennis', time: '10:00 - 11:00 (60 min)',  status: 'COMPLETED', avatar_color: '#615e00' },
  { customer: 'Jonathan Wu',      member_id: '#ZP-1087', court: 'West Pitch',       sport: 'Soccer', time: '16:00 - 20:00 (240 min)', status: 'CANCELLED', avatar_color: '#b02500' },
  { customer: 'Sarah Connor',     member_id: '#ZP-0622', court: 'High-Perf Studio', sport: 'Yoga',   time: '18:00 - 19:00 (60 min)',  status: 'BOOKED',    avatar_color: '#3a506b' },
];

export const SLOT_CALENDAR: Record<number, SlotBlock[]> = {
  0: [
    { time: '08:00-10:00', label: 'Advanced Padel', type: 'booking',     color: '#e2e7ff' },
    { time: '14:00-15:00', label: 'Maintenance',    type: 'maintenance', color: '#ffddcc' },
  ],
  1: [
    { time: '10:00-12:00', label: 'Open Booking',   type: 'open',        color: '#f0ffc0' },
  ],
  2: [
    { time: '09:00-11:00', label: 'Maintenance',    type: 'maintenance', color: '#ffddcc' },
    { time: '16:00-18:00', label: 'Open Booking',   type: 'open',        color: '#f0ffc0' },
    { time: '19:00-21:00', label: 'Pickleball Slam',type: 'booking',     color: '#e2e7ff' },
  ],
  3: [],
  4: [],
  5: [
    { time: '08:00-12:00', label: 'Tournament',     type: 'booking',     color: '#e2e7ff' },
  ],
  6: [],
};

/** Demand heatmap: 7 days × 16 hours (07–22). Deterministic pseudo-random
 *  values that look like a real weekly demand pattern (peak Friday evening). */
export const DEMAND_FORECAST: DemandCell[] = (() => {
  const out: DemandCell[] = [];
  for (let dow = 0; dow < 7; dow++) {
    for (let h = 7; h <= 22; h++) {
      const eveningBoost = h >= 17 && h <= 21 ? 1.6 : 1.0;
      const weekendBoost = dow === 4 || dow === 5 ? 1.4 : 1.0;
      const base = 0.3 + 0.5 * Math.sin((h - 7) / 8);
      out.push({
        day_of_week: dow,
        hour: h,
        predicted_bookings: Math.round(base * eveningBoost * weekendBoost * 100) / 100,
      });
    }
  }
  return out;
})();

/** 16 hourly bars (07-22). Used on /owner/insights "Peak Utilization". */
export const PEAK_UTILIZATION_BARS: number[] = [30, 35, 38, 42, 50, 58, 62, 68, 75, 85, 92, 95, 88, 70, 50, 30];
