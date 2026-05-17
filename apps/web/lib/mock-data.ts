import type { Court, Booking } from './types';

export const FALLBACK_COURTS: Court[] = [
  {
    id: 'bbc-01',
    name: 'Bangkok Badminton Center',
    short_name: 'Bangkok Badminton',
    sport: 'Badminton',
    rating: 4.8,
    reviews: 100,
    location: 'Pathum Wan, Bangkok 10330, Thailand',
    address: '88 Ratchadapisek Rd.',
    district: 'Sukhumvit',
    price_per_hour: 450,
    prime_price: 650,
    amenities: [
      { icon: 'ac_unit', label: 'Climate', value: 'Full AC' },
      { icon: 'local_parking', label: 'Parking', value: 'Free (50+ Slots)' },
      { icon: 'checkroom', label: 'Facilities', value: 'Changing Rooms' },
      { icon: 'water_drop', label: 'Water', value: 'Dispenser' },
    ],
    surface: 'Premium Synthetic',
    status: 'ACTIVE',
    utilization: 88,
    peak_hours: '17:00-22:00',
    ai_efficiency: 'Elite',
    tags: ['AI RECOMMENDED'],
    color: '#1a3a2a',
    courts: [
      { number: '01', surface: 'Premium Synthetic' },
      { number: '02', surface: 'Standard Wood' },
    ],
  },
  {
    id: 'sky-02',
    name: 'Skyline Arena Football',
    short_name: 'Skyline Arena',
    sport: 'Football',
    rating: 4.7,
    reviews: 85,
    location: 'Thonglor District',
    address: '42 Thonglor Soi 15',
    district: 'Thong Lor',
    price_per_hour: 1200,
    prime_price: 1800,
    amenities: [
      { icon: 'ac_unit', label: 'Climate', value: 'Open Air' },
      { icon: 'local_parking', label: 'Parking', value: '20 Slots' },
      { icon: 'checkroom', label: 'Facilities', value: 'Locker Rooms' },
      { icon: 'water_drop', label: 'Water', value: 'Dispenser' },
    ],
    surface: 'Artificial Turf',
    status: 'ACTIVE',
    utilization: 74,
    peak_hours: '18:00-22:00',
    ai_efficiency: 'High',
    tags: [],
    color: '#1c2526',
    courts: [{ number: '01', surface: 'Artificial Turf' }],
  },
  {
    id: 'dwh-03',
    name: 'Downtown Hoops',
    short_name: 'Downtown Hoops',
    sport: 'Basketball',
    rating: 4.5,
    reviews: 62,
    location: 'Ari Soi 4',
    address: 'Ari Soi 4',
    district: 'Ari',
    price_per_hour: 600,
    prime_price: 800,
    amenities: [
      { icon: 'ac_unit', label: 'Climate', value: 'Indoor AC' },
      { icon: 'local_parking', label: 'Parking', value: 'Street' },
      { icon: 'checkroom', label: 'Facilities', value: 'Showers' },
      { icon: 'water_drop', label: 'Water', value: 'Dispenser' },
    ],
    surface: 'Hardwood',
    status: 'ACTIVE',
    utilization: 68,
    peak_hours: '17:00-21:00',
    ai_efficiency: 'High',
    tags: [],
    color: '#3a1f1f',
    courts: [{ number: '01', surface: 'Hardwood' }],
  },
  {
    id: 'pdl-04',
    name: 'Padel House Sukhumvit',
    short_name: 'Padel House',
    sport: 'Padel',
    rating: 4.2,
    reviews: 41,
    location: 'Sukhumvit Soi 39',
    address: 'Sukhumvit Soi 39',
    district: 'Sukhumvit',
    price_per_hour: 800,
    prime_price: 1100,
    amenities: [
      { icon: 'ac_unit', label: 'Climate', value: 'Open Air' },
      { icon: 'local_parking', label: 'Parking', value: '15 Slots' },
      { icon: 'checkroom', label: 'Facilities', value: 'Lounge' },
      { icon: 'water_drop', label: 'Water', value: 'Cafe' },
    ],
    surface: 'Glass Panels',
    status: 'ACTIVE',
    utilization: 79,
    peak_hours: '18:00-22:00',
    ai_efficiency: 'Moderate',
    tags: [],
    color: '#2a3a1f',
    courts: [{ number: '01', surface: 'Glass Panels' }],
  },
  {
    id: 'rbs-05',
    name: 'Royal Bangkok Sports Club',
    short_name: 'Royal Bangkok',
    sport: 'Tennis',
    rating: 5.0,
    reviews: 120,
    location: 'Pathumwan',
    address: 'Henri Dunant Rd',
    district: 'Pathumwan',
    price_per_hour: 950,
    prime_price: 1400,
    amenities: [
      { icon: 'ac_unit', label: 'Climate', value: 'Open Air' },
      { icon: 'local_parking', label: 'Parking', value: 'Valet' },
      { icon: 'checkroom', label: 'Facilities', value: 'Premium Lounge' },
      { icon: 'water_drop', label: 'Water', value: 'Bar' },
    ],
    surface: 'Clay',
    status: 'ACTIVE',
    utilization: 92,
    peak_hours: '16:00-20:00',
    ai_efficiency: 'Elite',
    tags: ['MEMBERS ONLY'],
    color: '#1a3030',
    courts: [{ number: '01', surface: 'Clay' }],
  },
  {
    id: 'ivh-06',
    name: 'Impact Volleyball Hall',
    short_name: 'Impact Volleyball',
    sport: 'Volleyball',
    rating: 4.8,
    reviews: 33,
    location: 'Muang Thong Thani',
    address: 'Muang Thong Thani',
    district: 'Nonthaburi',
    price_per_hour: 350,
    prime_price: 500,
    amenities: [
      { icon: 'ac_unit', label: 'Climate', value: 'Full AC' },
      { icon: 'local_parking', label: 'Parking', value: 'Free' },
      { icon: 'checkroom', label: 'Facilities', value: 'Locker Rooms' },
      { icon: 'water_drop', label: 'Water', value: 'Dispenser' },
    ],
    surface: 'Sprung Floor',
    status: 'ACTIVE',
    utilization: 55,
    peak_hours: '19:00-22:00',
    ai_efficiency: 'High',
    tags: [],
    color: '#1f1f3a',
    courts: [{ number: '01', surface: 'Sprung Floor' }],
  },
];

const HOURS = Array.from({ length: 16 }, (_, i) => `${String(i + 7).padStart(2, '0')}:00`);

export function fallbackCourt(id: string): Court | undefined {
  return FALLBACK_COURTS.find((c) => c.id === id);
}

/**
 * Returns hour-start times (HH:00) free for a given court+date, given an
 * external list of bookings to consider as "taken". Caller passes the
 * combined seeded + store-persisted bookings so a freshly-booked slot
 * disappears immediately.
 */
export function getFreeSlotStarts(
  courtId: string,
  dateIso: string,
  bookings: Pick<Booking, 'court_id' | 'date' | 'time_start' | 'duration' | 'status'>[],
): string[] {
  const taken = new Set<string>();
  for (const b of bookings) {
    if (b.court_id !== courtId || b.date !== dateIso || b.status !== 'CONFIRMED') continue;
    const startH = parseInt(b.time_start.slice(0, 2), 10);
    for (let i = 0; i < b.duration; i++) {
      taken.add(`${String(startH + i).padStart(2, '0')}:00`);
    }
  }
  return HOURS.filter((h) => !taken.has(h));
}

export const ALL_HOURS = HOURS;
