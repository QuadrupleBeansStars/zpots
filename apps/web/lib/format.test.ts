import { describe, it, expect } from 'vitest';
import { formatPrice, formatDateShort, formatTimeRange, formatDateFull } from './format';

describe('formatPrice', () => {
  it('renders THB symbol and grouped thousands', () => {
    expect(formatPrice(1234)).toBe('฿1,234');
    expect(formatPrice(450)).toBe('฿450');
    expect(formatPrice(0)).toBe('฿0');
  });
});

describe('formatDateShort', () => {
  it('renders ISO date as "Mon, 18 May"', () => {
    expect(formatDateShort('2026-05-18')).toBe('Mon, 18 May');
  });
});

describe('formatDateFull', () => {
  it('renders ISO date as "Monday, May 18, 2026"', () => {
    expect(formatDateFull('2026-05-18')).toBe('Monday, May 18, 2026');
  });
});

describe('formatTimeRange', () => {
  it('renders start-end with em dash', () => {
    expect(formatTimeRange('18:00', '20:00')).toBe('18:00 – 20:00');
  });
});
