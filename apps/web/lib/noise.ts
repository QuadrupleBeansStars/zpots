/**
 * SVG turbulence data URI. Layered on dark surfaces at low opacity
 * to add organic texture and kill the flat-vector AI look.
 *
 * Identical to --noise-url CSS variable in globals.css — keep these
 * in sync if either changes.
 */
export const NOISE_URL =
  "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='1'/></svg>\")";
