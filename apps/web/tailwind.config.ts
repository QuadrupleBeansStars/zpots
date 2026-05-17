import type { Config } from 'tailwindcss';

/**
 * ZPOTS design tokens as Tailwind theme.
 *
 * Phase 5a: NEW tokens (lime ramp, ink ramp, surface ramp, geist fonts,
 * canonical spacing scale, motion durations, signature radius) are added
 * alongside the legacy zpots.* tokens. Legacy classes keep working until
 * each page is migrated in 5b+.
 */
const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        zpots: {
          lime: '#CFFC00',
          moss: '#2E6B00',
          forest: '#1E4A00',
          night: '#0D1F0D',
          surface: '#F2F9EE',
          mint: '#E3F0DE',
          ink: '#1C2526',
          muted: '#3D4455',
          danger: '#C62828',
          warn: '#E65100',
          info: '#1565C0',
        },
        // Phase 5a — KP + Motion ramps
        lime: {
          DEFAULT: '#cffc00',
          press: '#b8e600',
          deep: '#3a4d10',          // text-on-lime ONLY, never fill
        },
        ink: {
          900: '#15192a',
          800: '#1c2136',
          700: '#272e42',
        },
        surface: {
          DEFAULT: '#f6f6ff',
          low: '#eef0ff',
          med: '#e2e7ff',
          high: '#d1dcff',
        },
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        eyebrow: ['Lexend', 'system-ui', 'sans-serif'],
        // Phase 5a — Geist for new components
        geist: ['Geist', 'system-ui', 'sans-serif'],
        'geist-mono': ['"Geist Mono"', 'ui-monospace', 'monospace'],
      },
      fontSize: {
        eyebrow: ['10px', { letterSpacing: '0.1em', fontWeight: '600' }],
        // Phase 5a scale
        'display-lg': ['3.5rem', { lineHeight: '1', letterSpacing: '-0.02em', fontWeight: '700' }],
        'display-md': ['2.5rem', { lineHeight: '1.05', letterSpacing: '-0.02em', fontWeight: '700' }],
        'title-lg':   ['1.5rem',  { lineHeight: '1.2', fontWeight: '600' }],
        'title-md':   ['1.125rem',{ lineHeight: '1.3', fontWeight: '600' }],
        'body-md':    ['1rem',    { lineHeight: '1.5' }],
        'body-sm':    ['0.875rem',{ lineHeight: '1.5' }],
        'label-sm':   ['0.75rem', { letterSpacing: '0.04em', fontWeight: '600' }],
      },
      spacing: {
        // Phase 5a canonical rhythm (Fibonacci-ish). Additional to defaults.
        '13': '52px',
      },
      borderRadius: {
        card: '16px',
        pill: '9999px',
        // Phase 5a
        'kp-card': '12px',
        'kp-pill': '999px',
        'kp-chip': '2px',
      },
      boxShadow: {
        card: '0 4px 16px rgba(28,37,38,0.06)',
        'card-lift': '0 8px 24px rgba(28,37,38,0.10)',
        lime: '0 4px 12px rgba(207,252,0,0.35)',
        // Phase 5a
        float: '0 8px 24px rgba(39, 46, 66, 0.06)',
        lift: '0 1px 0 rgba(255,255,255,0.04) inset, 0 24px 60px -20px rgba(15,19,42,0.45)',
      },
      backgroundImage: {
        'lime-grad': 'linear-gradient(135deg,#cffc00,#b8e000)',
        'lime-soft': 'linear-gradient(135deg,#cffc00,#e4ff7a)',
        'night-sky': 'linear-gradient(160deg,#060e20 0%,#0d1b2e 40%,#162d3e 70%,#1a3040 100%)',
      },
      transitionTimingFunction: {
        precision: 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
      transitionDuration: {
        instant: '120ms',
        quick:   '220ms',
        smooth:  '360ms',
        lush:    '720ms',
      },
    },
  },
  plugins: [],
};

export default config;
