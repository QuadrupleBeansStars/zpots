/**
 * Interpolates between `from` and `to` hex colors based on `t` in [0, 1].
 * Returns "#RRGGBB". Used by DemandHeatmap to color cells based on predicted bookings.
 */
export function lerpHex(from: string, to: string, t: number): string {
  const clamp = Math.max(0, Math.min(1, t));
  const f = parseInt(from.slice(1), 16);
  const g = parseInt(to.slice(1), 16);
  const fr = (f >> 16) & 0xff;
  const fg = (f >> 8) & 0xff;
  const fb = f & 0xff;
  const gr = (g >> 16) & 0xff;
  const gg = (g >> 8) & 0xff;
  const gb = g & 0xff;
  const r = Math.round(fr + (gr - fr) * clamp);
  const gC = Math.round(fg + (gg - fg) * clamp);
  const b = Math.round(fb + (gb - fb) * clamp);
  return `#${((r << 16) | (gC << 8) | b).toString(16).padStart(6, '0')}`;
}
