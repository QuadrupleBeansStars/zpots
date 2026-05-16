import type { Config } from 'tailwindcss';

/**
 * ZPOTS design tokens as Tailwind theme.
 * Paired with `globals.css` (copy of `handoff/design-system/shared.css`).
 */
const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        zpots: {
          lime: '#CFFC00',        // primary AI accent, CTAs
          moss: '#2E6B00',        // brand green, on-light text emphasis
          forest: '#1E4A00',      // button text on lime
          night: '#0D1F0D',       // dark sidebar / dark surfaces
          surface: '#F2F9EE',     // page bg (light mode)
          mint: '#E3F0DE',        // borders / thin dividers
          ink: '#1C2526',         // body text
          muted: '#3D4455',       // secondary text
          danger: '#C62828',
          warn: '#E65100',
          info: '#1565C0',
        },
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        eyebrow: ['Lexend', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        eyebrow: ['10px', { letterSpacing: '0.1em', fontWeight: '600' }],
      },
      borderRadius: {
        card: '16px',
        pill: '9999px',
      },
      boxShadow: {
        card: '0 4px 16px rgba(28,37,38,0.06)',
        'card-lift': '0 8px 24px rgba(28,37,38,0.10)',
        lime: '0 4px 12px rgba(207,252,0,0.35)',
      },
      backgroundImage: {
        'lime-grad': 'linear-gradient(135deg,#cffc00,#b8e000)',
        'lime-soft': 'linear-gradient(135deg,#cffc00,#e4ff7a)',
        'night-sky': 'linear-gradient(160deg,#060e20 0%,#0d1b2e 40%,#162d3e 70%,#1a3040 100%)',
      },
    },
  },
  plugins: [],
};

export default config;
