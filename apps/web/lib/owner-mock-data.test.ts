import { describe, it, expect } from 'vitest';
import { OWNER_VENUES, WEEKLY_UTILIZATION, DISTRICT_DEMAND, TODAYS_BOOKINGS, OWNER_BOOKINGS, SLOT_CALENDAR, DEMAND_FORECAST, PEAK_UTILIZATION_BARS } from './owner-mock-data';

describe('owner-mock-data', () => {
  it('has 3 venues', () => {
    expect(OWNER_VENUES).toHaveLength(3);
    expect(OWNER_VENUES[0].name).toBe('Main Arena');
  });
  it('has weekly utilization for all 7 days', () => {
    expect(WEEKLY_UTILIZATION).toHaveLength(7);
    expect(WEEKLY_UTILIZATION.map((w) => w.day)).toEqual(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']);
  });
  it('has 3 district demand entries', () => {
    expect(DISTRICT_DEMAND).toHaveLength(3);
    expect(DISTRICT_DEMAND.find((d) => d.name === 'Sukhumvit')?.demand).toBe(94);
  });
  it("has 3 today's bookings", () => {
    expect(TODAYS_BOOKINGS).toHaveLength(3);
  });
  it('has 4 owner bookings', () => {
    expect(OWNER_BOOKINGS).toHaveLength(4);
  });
  it('slot calendar has 7 day keys', () => {
    expect(Object.keys(SLOT_CALENDAR)).toHaveLength(7);
    expect(SLOT_CALENDAR[2]).toHaveLength(3);
  });
  it('demand forecast covers 7 days × 16 hours', () => {
    expect(DEMAND_FORECAST).toHaveLength(7 * 16);
  });
  it('peak utilization bars cover 16 hours', () => {
    expect(PEAK_UTILIZATION_BARS).toHaveLength(16);
  });
});
