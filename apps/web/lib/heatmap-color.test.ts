import { describe, it, expect } from 'vitest';
import { lerpHex } from './heatmap-color';

describe('lerpHex', () => {
  it('returns from at t=0', () => {
    expect(lerpHex('#F2F9EE', '#1E4A00', 0)).toBe('#f2f9ee');
  });
  it('returns to at t=1', () => {
    expect(lerpHex('#F2F9EE', '#1E4A00', 1)).toBe('#1e4a00');
  });
  it('returns a midpoint at t=0.5', () => {
    const mid = lerpHex('#000000', '#ffffff', 0.5);
    expect(mid).toBe('#808080');
  });
  it('clamps below 0', () => {
    expect(lerpHex('#F2F9EE', '#1E4A00', -1)).toBe('#f2f9ee');
  });
  it('clamps above 1', () => {
    expect(lerpHex('#F2F9EE', '#1E4A00', 2)).toBe('#1e4a00');
  });
});
