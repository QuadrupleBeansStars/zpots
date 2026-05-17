import { describe, it, expect } from 'vitest';
import { FALLBACK_COURTS, fallbackCourt, getFreeSlotStarts } from './mock-data';

describe('FALLBACK_COURTS', () => {
  it('exposes at least bbc-01 and sky-02 with required fields', () => {
    const ids = FALLBACK_COURTS.map((c) => c.id);
    expect(ids).toContain('bbc-01');
    expect(ids).toContain('sky-02');
    const bbc = FALLBACK_COURTS.find((c) => c.id === 'bbc-01')!;
    expect(bbc.name).toBe('Bangkok Badminton Center');
    expect(bbc.sport).toBe('Badminton');
    expect(bbc.price_per_hour).toBe(450);
  });
});

describe('fallbackCourt', () => {
  it('returns the court by id', () => {
    expect(fallbackCourt('bbc-01')?.name).toBe('Bangkok Badminton Center');
  });
  it('returns undefined for unknown id', () => {
    expect(fallbackCourt('nope')).toBeUndefined();
  });
});

describe('getFreeSlotStarts', () => {
  it('returns all 16 hour-starts (07:00–22:00) when no bookings', () => {
    const free = getFreeSlotStarts('bbc-01', '2099-01-01', []);
    expect(free).toContain('07:00');
    expect(free).toContain('22:00');
    expect(free).toHaveLength(16);
  });
  it('excludes hours covered by an existing booking', () => {
    const taken = [{
      court_id: 'bbc-01', date: '2099-01-01',
      time_start: '18:00', duration: 2, status: 'CONFIRMED',
    }] as any;
    const free = getFreeSlotStarts('bbc-01', '2099-01-01', taken);
    expect(free).not.toContain('18:00');
    expect(free).not.toContain('19:00');
    expect(free).toContain('20:00');
  });
  it('ignores bookings for other courts', () => {
    const taken = [{
      court_id: 'sky-02', date: '2099-01-01',
      time_start: '18:00', duration: 1, status: 'CONFIRMED',
    }] as any;
    const free = getFreeSlotStarts('bbc-01', '2099-01-01', taken);
    expect(free).toContain('18:00');
  });
  it('ignores CANCELLED bookings', () => {
    const taken = [{
      court_id: 'bbc-01', date: '2099-01-01',
      time_start: '18:00', duration: 1, status: 'CANCELLED',
    }] as any;
    const free = getFreeSlotStarts('bbc-01', '2099-01-01', taken);
    expect(free).toContain('18:00');
  });
});
