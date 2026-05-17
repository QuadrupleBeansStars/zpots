# Phase 5a — Design Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install the design-system foundation — new tokens (typography, color, surface, motion, spacing), distinctive primitives, a unified TopNav replacing both `PlayerTopBar` and `OwnerSidebar`, and a shared `PageShell` — without changing any page content.

**Architecture:** Add new tokens *alongside* the existing `zpots.*` palette, so old class usage keeps working until each page is migrated in 5b+. Load Geist + Geist Mono *alongside* the legacy fonts. The only visibly different thing in 5a is the chassis: the new TopNav (glass, lime underline, Geist) replaces both nav components.

**Tech Stack:** Next.js 16 · Tailwind v3 · React 19 · Vitest 4 · IntersectionObserver · CSS custom properties

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase5a-design-foundation-design.md`
**Branch:** create `feat/nextjs-phase5a` off main

**Critical alignment note (read first):**
The spec phrase "existing tokens get remapped" should be read as a 5b+ *goal*, not a 5a *action*. In 5a we ADD the new tokens; existing pages keep using the old `zpots.*` tokens visually unchanged. Fonts similarly added alongside, not replacing. Only the nav chassis visibly changes.

---

## File structure (end of Phase 5a)

```
apps/web/
├── app/
│   ├── globals.css                # MODIFIED — new :root vars, focus-ring, noise SVG, reduced-motion media query
│   ├── layout.tsx                 # MODIFIED — add Geist + Geist Mono <link>
│   ├── player/layout.tsx          # MODIFIED — uses <PageShell role="player">
│   └── owner/layout.tsx           # MODIFIED — uses <PageShell role="owner">
├── tailwind.config.ts             # MODIFIED — extend with new tokens (ink/lime/surface ramps, spacing, durations, geist)
├── components/
│   ├── primitives/                # NEW
│   │   ├── GlassPanel.tsx
│   │   ├── DarkHero.tsx
│   │   ├── CountUp.tsx
│   │   ├── NumberFlip.tsx
│   │   ├── RevealOnScroll.tsx
│   │   ├── PulseAccent.tsx
│   │   ├── DiagonalDivider.tsx
│   │   └── Ticker.tsx
│   ├── nav/                       # NEW
│   │   ├── TopNav.tsx
│   │   ├── NavLink.tsx
│   │   └── UserChip.tsx
│   ├── PageShell.tsx              # NEW
│   ├── PlayerTopBar.tsx           # UNTOUCHED — unused after 5a (delete in 5d)
│   └── OwnerSidebar.tsx           # UNTOUCHED — unused after 5a (delete in 5c)
├── lib/
│   ├── motion.ts                  # NEW — useReducedMotion + duration constants
│   └── noise.ts                   # NEW — SVG turbulence data URI
└── tests/
    ├── CountUp.test.tsx           # NEW
    ├── NumberFlip.test.tsx        # NEW
    ├── RevealOnScroll.test.tsx    # NEW
    └── TopNav.test.tsx            # NEW
```

Playwright tests (`apps/web/tests/*.spec.ts`) may need selector updates as the nav DOM changes — covered in Task 13.

---

## Task 0: Branch + baseline

- [ ] **Step 1: Cut branch.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS && git checkout main && git pull && git checkout -b feat/nextjs-phase5a
```

- [ ] **Step 2: Baseline test suite (everything green before we start).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build 2>&1 | tail -5
```

Expected: Vitest **30 passed**, `pnpm build` clean. If not, stop and investigate.

---

## Task 1: Load Geist + Geist Mono fonts

**Files:**
- Modify: `apps/web/app/layout.tsx`

Add Geist alongside the existing fonts. Existing `.display` (Space Grotesk) / body Inter / `.eyebrow` Lexend keep working; Geist becomes available for new components.

- [ ] **Step 1: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/app/layout.tsx`:**

```tsx
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ZPOTS — AI-Powered Sports Court Booking',
  description: 'Discover, book, and manage sports courts in Bangkok.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {/* Load Google Fonts via <link> rather than @import in globals.css —
            Tailwind/PostCSS sometimes silently fails to fetch remote @imports,
            which leaves Material Symbols spans showing their ligature text
            (arrow_forward, ac_unit, …) instead of icons. */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@300;400;500;600;700&family=Lexend:wght@300;400;500;600;700&display=swap"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Geist+Mono:wght@400;500;600&display=swap"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
        />
      </head>
      <body className="font-sans bg-white text-zpots-ink antialiased">
        {children}
      </body>
    </html>
  );
}
```

- [ ] **Step 2: Verify build still passes.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build 2>&1 | tail -3
```

Expected: clean.

- [ ] **Step 3: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/app/layout.tsx
git commit -m "feat(web): load Geist + Geist Mono fonts (alongside legacy)"
```

---

## Task 2: New CSS variables, focus ring, noise, reduced-motion

**Files:**
- Modify: `apps/web/app/globals.css`

Add the new design tokens as CSS variables. Existing styles stay intact above the new section.

- [ ] **Step 1: Append the following to `/Users/nchawanp/Desktop/ZPOTS/apps/web/app/globals.css`** (after the existing styles, before the `@tailwind` directives — those must stay last):

Find this line:
```
/* Tailwind v3 directives — required for utility classes used in JSX */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Insert **above** that block:

```css
/* ============================================================
   Phase 5a — Kinetic Precision + Motion design tokens.
   Used by /components/primitives/ + /components/nav/.
   Existing zpots.* tokens stay untouched until each page migrates in 5b+.
   ============================================================ */
:root {
  /* Lime palette */
  --color-lime: #cffc00;
  --color-lime-press: #b8e600;
  --color-lime-deep: #3a4d10;

  /* Ink ramp — dark hero cards live here */
  --color-ink-900: #15192a;
  --color-ink-800: #1c2136;
  --color-ink-700: #272e42;

  /* Surface ramp */
  --color-surface: #f6f6ff;
  --color-surface-low: #eef0ff;
  --color-surface-med: #e2e7ff;
  --color-surface-high: #d1dcff;

  /* Motion */
  --ease-precision: cubic-bezier(0.16, 1, 0.3, 1);
  --dur-instant: 120ms;
  --dur-quick:   220ms;
  --dur-smooth:  360ms;
  --dur-lush:    720ms;

  /* Shadows */
  --shadow-float: 0 8px 24px rgba(39, 46, 66, 0.06);
  --shadow-lift:  0 1px 0 rgba(255, 255, 255, 0.04) inset,
                  0 24px 60px -20px rgba(15, 19, 42, 0.45);

  /* Noise — SVG turbulence data-URI, layered on dark heroes at 4% to
     kill the flat-vector AI look. Generated once; matches lib/noise.ts. */
  --noise-url: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='1'/></svg>");
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --dur-instant: 1ms;
    --dur-quick:   1ms;
    --dur-smooth:  1ms;
    --dur-lush:    80ms;
  }
}

/* Focus ring — brand + a11y in one. Apply via .focus-ring class. */
.focus-ring:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-ink-900),
              0 0 0 4px var(--color-lime);
}

/* Tabular-nums utility — KPIs don't dance during CountUp. */
.tabular-nums { font-variant-numeric: tabular-nums; }
```

- [ ] **Step 2: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build 2>&1 | tail -3
```

Expected: clean.

- [ ] **Step 3: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/app/globals.css
git commit -m "feat(web): KP+Motion CSS tokens (ink/lime/surface ramps, motion, noise)

Adds :root CSS vars for the new design system alongside existing
zpots.* tokens (which stay untouched). Includes prefers-reduced-motion
collapse, .focus-ring utility, .tabular-nums utility, and SVG noise
data URI for dark-hero backgrounds."
```

---

## Task 3: Extend Tailwind config with new tokens

**Files:**
- Modify: `apps/web/tailwind.config.ts`

Add new token names (ink, lime ramp, surface ramp, spacing, durations, Geist font families, signature radius). Existing `zpots.*` tokens stay exactly as they are.

- [ ] **Step 1: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/tailwind.config.ts`:**

```ts
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
        'label-sm':   ['0.75rem', { letterSpacing: '0.04em', textTransform: 'uppercase', fontWeight: '600' }],
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
```

- [ ] **Step 2: Verify Tailwind picks up the new classes (build sanity).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build 2>&1 | tail -5
```

Expected: clean.

- [ ] **Step 3: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/tailwind.config.ts
git commit -m "feat(web): Tailwind tokens for KP+Motion (lime/ink/surface ramps + geist + motion)

Adds new utility classes (bg-ink-900, text-lime, font-geist, ease-precision,
duration-smooth, shadow-lift, etc.) alongside the legacy zpots.* palette.
Legacy classes unchanged."
```

---

## Task 4: lib/motion.ts + lib/noise.ts utilities

**Files:**
- Create: `apps/web/lib/motion.ts`
- Create: `apps/web/lib/noise.ts`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/lib/motion.ts`:**

```ts
'use client';
import { useEffect, useState } from 'react';

/**
 * Duration constants in milliseconds. Mirror --dur-* CSS variables.
 * Use these in JS-driven animations (CountUp, NumberFlip).
 */
export const DUR = {
  instant: 120,
  quick:   220,
  smooth:  360,
  lush:    720,
} as const;

export const REDUCED_DUR = {
  instant: 1,
  quick:   1,
  smooth:  1,
  lush:    80,
} as const;

/**
 * React hook — returns true when the user has prefers-reduced-motion enabled.
 * SSR-safe: returns false on first render, updates after mount.
 */
export function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    setReduced(mq.matches);
    const onChange = (e: MediaQueryListEvent) => setReduced(e.matches);
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);
  return reduced;
}

/**
 * Pick the right duration based on reduced-motion preference.
 */
export function pickDur(key: keyof typeof DUR, reduced: boolean): number {
  return reduced ? REDUCED_DUR[key] : DUR[key];
}
```

- [ ] **Step 2: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/lib/noise.ts`:**

```ts
/**
 * SVG turbulence data URI. Layered on dark surfaces at low opacity
 * to add organic texture and kill the flat-vector AI look.
 *
 * Identical to --noise-url CSS variable in globals.css — keep these
 * in sync if either changes.
 */
export const NOISE_URL =
  "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='1'/></svg>\")";
```

- [ ] **Step 3: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/lib/motion.ts apps/web/lib/noise.ts
git commit -m "feat(web): motion + noise utilities

lib/motion.ts: DUR constants + useReducedMotion hook + pickDur helper.
lib/noise.ts: SVG turbulence data URI matching --noise-url CSS var."
```

---

## Task 5: GlassPanel + DarkHero primitives

**Files:**
- Create: `apps/web/components/primitives/GlassPanel.tsx`
- Create: `apps/web/components/primitives/DarkHero.tsx`

Both are pure wrappers — no logic, no tests beyond manual verification.

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/primitives/GlassPanel.tsx`:**

```tsx
import React, { type ElementType, type HTMLAttributes } from 'react';

type GlassPanelProps<T extends ElementType = 'div'> = {
  as?: T;
  className?: string;
  children?: React.ReactNode;
} & Omit<HTMLAttributes<HTMLElement>, 'className' | 'children'>;

/**
 * Glassmorphic surface — used by TopNav, floating menus, hover overlays.
 * Wraps `bg-white/60 backdrop-blur-2xl shadow-float`.
 */
export function GlassPanel<T extends ElementType = 'div'>({
  as,
  className = '',
  children,
  ...rest
}: GlassPanelProps<T>) {
  const Tag = (as || 'div') as ElementType;
  return (
    <Tag
      className={`bg-white/60 backdrop-blur-2xl shadow-float ${className}`}
      {...rest}
    >
      {children}
    </Tag>
  );
}
```

- [ ] **Step 2: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/primitives/DarkHero.tsx`:**

```tsx
import React from 'react';

import { NOISE_URL } from '@/lib/noise';

type Props = {
  glow?: 'none' | 'lime';
  className?: string;
  children?: React.ReactNode;
};

/**
 * Editorial dark hero card. Used by every page's title region in 5b+.
 * `glow="lime"` adds a radial lime gradient anchored top-right.
 */
export function DarkHero({ glow = 'lime', className = '', children }: Props) {
  return (
    <div
      className={`relative overflow-hidden bg-ink-900 text-white rounded-kp-card shadow-lift ${className}`}
      style={{
        backgroundImage: NOISE_URL,
        backgroundBlendMode: 'overlay',
        backgroundSize: '160px 160px',
        backgroundColor: '#15192a',
      }}
    >
      {glow === 'lime' && (
        <div
          aria-hidden
          className="absolute pointer-events-none"
          style={{
            top: '-20%',
            right: '-10%',
            width: '380px',
            height: '380px',
            background: 'radial-gradient(circle, rgba(207,252,0,0.35) 0%, rgba(207,252,0,0) 70%)',
          }}
        />
      )}
      <div className="relative">{children}</div>
    </div>
  );
}
```

- [ ] **Step 3: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build 2>&1 | tail -3
```

Expected: clean.

- [ ] **Step 4: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/components/primitives/GlassPanel.tsx apps/web/components/primitives/DarkHero.tsx
git commit -m "feat(web): GlassPanel + DarkHero primitives"
```

---

## Task 6: CountUp primitive (TDD)

**Files:**
- Create: `apps/web/components/primitives/CountUp.tsx`
- Create: `apps/web/tests/CountUp.test.tsx`

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/tests/CountUp.test.tsx`:

```tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

import { CountUp } from '@/components/primitives/CountUp';

describe('CountUp', () => {
  it('eventually renders the target value', async () => {
    vi.useFakeTimers();
    render(<CountUp value={128} />);
    vi.advanceTimersByTime(500);
    expect(screen.getByTestId('countup').textContent).toBe('128');
    vi.useRealTimers();
  });

  it('formats currency with the ฿ prefix', async () => {
    vi.useFakeTimers();
    render(<CountUp value={64500} format="currency" />);
    vi.advanceTimersByTime(500);
    expect(screen.getByTestId('countup').textContent).toContain('฿');
    expect(screen.getByTestId('countup').textContent).toContain('64');
    vi.useRealTimers();
  });
});
```

- [ ] **Step 2: Run, expect failure.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit -- CountUp 2>&1 | tail -10
```

Expected: import error / file not found.

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/primitives/CountUp.tsx`:**

```tsx
'use client';
import React, { useEffect, useRef, useState } from 'react';

import { DUR, useReducedMotion } from '@/lib/motion';

type Format = 'number' | 'currency' | 'percent';

type Props = {
  value: number;
  format?: Format;
  duration?: number;        // override; defaults to DUR.smooth
  className?: string;
};

function formatValue(n: number, format: Format): string {
  if (format === 'currency') {
    return '฿' + Math.round(n).toLocaleString();
  }
  if (format === 'percent') {
    return Math.round(n) + '%';
  }
  return Math.round(n).toLocaleString();
}

/**
 * Tween from 0 → `value` using ease-precision. Honors prefers-reduced-motion
 * (snaps instantly under reduced). Renders inside a tabular-nums span so
 * digits don't dance.
 */
export function CountUp({ value, format = 'number', duration, className = '' }: Props) {
  const reduced = useReducedMotion();
  const [display, setDisplay] = useState(reduced ? value : 0);
  const startRef = useRef<number | null>(null);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    if (reduced) {
      setDisplay(value);
      return;
    }
    const dur = duration ?? DUR.smooth;
    startRef.current = null;

    const tick = (ts: number) => {
      if (startRef.current === null) startRef.current = ts;
      const elapsed = ts - startRef.current;
      const t = Math.min(1, elapsed / dur);
      // ease-precision approx: cubic-bezier(0.16, 1, 0.3, 1) ≈ 1 - (1 - t)^3 * (1 + sharper start)
      const eased = 1 - Math.pow(1 - t, 3);
      setDisplay(value * eased);
      if (t < 1) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        setDisplay(value);
      }
    };

    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    };
  }, [value, duration, reduced]);

  return (
    <span data-testid="countup" className={`font-geist-mono tabular-nums ${className}`}>
      {formatValue(display, format)}
    </span>
  );
}
```

- [ ] **Step 4: Run tests, expect green.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit -- CountUp 2>&1 | tail -10
```

Expected: 2 passed.

- [ ] **Step 5: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/components/primitives/CountUp.tsx apps/web/tests/CountUp.test.tsx
git commit -m "feat(web): CountUp primitive (eased tween, tabular-nums, reduced-motion safe)"
```

---

## Task 7: NumberFlip primitive (TDD)

**Files:**
- Create: `apps/web/components/primitives/NumberFlip.tsx`
- Create: `apps/web/tests/NumberFlip.test.tsx`

Renders one `<span>` per digit. CSS keyframe flips the digit on change. Distinct from CountUp — the flip is per-digit, not a tween.

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/tests/NumberFlip.test.tsx`:

```tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

import { NumberFlip } from '@/components/primitives/NumberFlip';

describe('NumberFlip', () => {
  it('renders one span per digit, in order', () => {
    render(<NumberFlip value={128} />);
    const digits = screen.getAllByTestId('flip-digit');
    expect(digits.map((d) => d.textContent)).toEqual(['1', '2', '8']);
  });

  it('renders an empty container for value 0', () => {
    render(<NumberFlip value={0} />);
    const digits = screen.getAllByTestId('flip-digit');
    expect(digits.map((d) => d.textContent)).toEqual(['0']);
  });
});
```

- [ ] **Step 2: Run, expect failure.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit -- NumberFlip 2>&1 | tail -10
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/primitives/NumberFlip.tsx`:**

```tsx
'use client';
import React, { useEffect, useState } from 'react';

type Props = {
  value: number;
  className?: string;
};

/**
 * Odometer-style flip per digit. The sports-tech signature variant of CountUp.
 * Each digit is a span that animates on change.
 *
 * The CSS keyframe is inline so this component is self-contained and doesn't
 * need to be registered in globals.css.
 */
export function NumberFlip({ value, className = '' }: Props) {
  const [prev, setPrev] = useState(value);
  useEffect(() => {
    setPrev(value);
  }, [value]);

  const digits = String(Math.round(value)).split('');

  return (
    <>
      <style>{`
        @keyframes flip-digit {
          0% { transform: rotateX(0deg); opacity: 1; }
          50% { transform: rotateX(90deg); opacity: 0.5; }
          100% { transform: rotateX(0deg); opacity: 1; }
        }
        .flip-digit { display:inline-block; animation: flip-digit var(--dur-smooth, 360ms) var(--ease-precision, cubic-bezier(0.16,1,0.3,1)); }
        @media (prefers-reduced-motion: reduce) { .flip-digit { animation: none; } }
      `}</style>
      <span className={`font-geist-mono tabular-nums ${className}`}>
        {digits.map((d, i) => (
          <span
            key={`${prev}-${i}-${d}`}
            data-testid="flip-digit"
            className="flip-digit"
          >
            {d}
          </span>
        ))}
      </span>
    </>
  );
}
```

- [ ] **Step 4: Run tests, expect green.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit -- NumberFlip 2>&1 | tail -10
```

Expected: 2 passed.

- [ ] **Step 5: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/components/primitives/NumberFlip.tsx apps/web/tests/NumberFlip.test.tsx
git commit -m "feat(web): NumberFlip primitive (odometer-style digit flip)"
```

---

## Task 8: RevealOnScroll primitive (TDD)

**Files:**
- Create: `apps/web/components/primitives/RevealOnScroll.tsx`
- Create: `apps/web/tests/RevealOnScroll.test.tsx`

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/tests/RevealOnScroll.test.tsx`:

```tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect, beforeEach, vi } from 'vitest';

import { RevealOnScroll } from '@/components/primitives/RevealOnScroll';

// Capture the callback so we can fire it manually.
let observerCallback: IntersectionObserverCallback | null = null;

beforeEach(() => {
  observerCallback = null;
  class MockIO {
    callback: IntersectionObserverCallback;
    constructor(cb: IntersectionObserverCallback) {
      this.callback = cb;
      observerCallback = cb;
    }
    observe = vi.fn();
    unobserve = vi.fn();
    disconnect = vi.fn();
    takeRecords = vi.fn(() => []);
    root = null;
    rootMargin = '';
    thresholds = [];
  }
  // @ts-expect-error — test-time global
  global.IntersectionObserver = MockIO;
});

describe('RevealOnScroll', () => {
  it('children start hidden, become visible after intersection', () => {
    render(
      <RevealOnScroll>
        <p data-testid="content">hi</p>
      </RevealOnScroll>,
    );

    const wrap = screen.getByTestId('reveal-wrap');
    expect(wrap.className).toContain('opacity-0');

    // Fire the intersection callback.
    observerCallback?.(
      [{ isIntersecting: true, intersectionRatio: 0.5 } as IntersectionObserverEntry],
      {} as IntersectionObserver,
    );

    // Re-query after state update.
    expect(screen.getByTestId('reveal-wrap').className).not.toContain('opacity-0');
  });

  it('renders children regardless of visibility', () => {
    render(
      <RevealOnScroll>
        <p data-testid="content">visible-text</p>
      </RevealOnScroll>,
    );
    expect(screen.getByTestId('content').textContent).toBe('visible-text');
  });
});
```

- [ ] **Step 2: Run, expect failure.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit -- RevealOnScroll 2>&1 | tail -10
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/primitives/RevealOnScroll.tsx`:**

```tsx
'use client';
import React, { useEffect, useRef, useState } from 'react';

type Props = {
  delay?: number;             // ms — staggers child reveal
  className?: string;
  children?: React.ReactNode;
};

/**
 * IntersectionObserver-driven fade-up. Fires once at 20% visibility.
 * Children start opacity-0 translate-y-2; reveal to opacity-100 translate-y-0
 * over dur-smooth with ease-precision.
 */
export function RevealOnScroll({ delay = 0, className = '', children }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === 'undefined') {
      setVisible(true);
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (e.isIntersecting) {
            // setTimeout for delay; intersect-once and disconnect
            setTimeout(() => setVisible(true), delay);
            io.disconnect();
            break;
          }
        }
      },
      { threshold: 0.2 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, [delay]);

  return (
    <div
      ref={ref}
      data-testid="reveal-wrap"
      className={[
        'transition-all duration-smooth ease-precision',
        visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2',
        className,
      ].join(' ')}
    >
      {children}
    </div>
  );
}
```

- [ ] **Step 4: Run tests, expect green.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit -- RevealOnScroll 2>&1 | tail -10
```

Expected: 2 passed.

- [ ] **Step 5: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/components/primitives/RevealOnScroll.tsx apps/web/tests/RevealOnScroll.test.tsx
git commit -m "feat(web): RevealOnScroll primitive (IntersectionObserver fade-up)"
```

---

## Task 9: PulseAccent + DiagonalDivider + Ticker primitives

**Files:**
- Create: `apps/web/components/primitives/PulseAccent.tsx`
- Create: `apps/web/components/primitives/DiagonalDivider.tsx`
- Create: `apps/web/components/primitives/Ticker.tsx`

All three are pure CSS/SVG — no logic worth unit-testing. Manual smoke later.

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/primitives/PulseAccent.tsx`:**

```tsx
'use client';
import React from 'react';

type Props = {
  className?: string;
  children?: React.ReactNode;
};

/**
 * Continuous lime halo around child. Used for AI callouts.
 * Reduced-motion: collapses to a static 1px lime ring.
 */
export function PulseAccent({ className = '', children }: Props) {
  return (
    <>
      <style>{`
        @keyframes pulse-accent {
          0%, 100% { box-shadow: 0 0 0 0 rgba(207, 252, 0, 0.0); }
          50%      { box-shadow: 0 0 0 12px rgba(207, 252, 0, 0.0), 0 0 24px rgba(207, 252, 0, 0.55); }
        }
        .pulse-accent { animation: pulse-accent 2s ease-in-out infinite; }
        @media (prefers-reduced-motion: reduce) {
          .pulse-accent { animation: none; box-shadow: 0 0 0 1px rgba(207,252,0,0.6); }
        }
      `}</style>
      <span className={`pulse-accent inline-block rounded-kp-card ${className}`}>
        {children}
      </span>
    </>
  );
}
```

- [ ] **Step 2: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/primitives/DiagonalDivider.tsx`:**

```tsx
import React from 'react';

type Props = {
  from?: string;            // CSS color above the diagonal
  to?: string;              // CSS color below the diagonal
  angle?: number;           // degrees — default 4
  className?: string;
};

/**
 * Diagonal transition between two surface colors. SVG-based so it scales
 * cleanly. Sits in normal flow at full width × 40px height.
 */
export function DiagonalDivider({
  from = '#f6f6ff',
  to = '#eef0ff',
  angle = 4,
  className = '',
}: Props) {
  // Compute the y offset on each side from the angle.
  const offset = Math.tan((angle * Math.PI) / 180) * 50;
  const polyTop = `0,0 100,0 100,${50 - offset} 0,${50 + offset}`;
  const polyBot = `0,${50 + offset} 100,${50 - offset} 100,100 0,100`;

  return (
    <svg
      viewBox="0 0 100 100"
      preserveAspectRatio="none"
      className={`block w-full h-10 ${className}`}
      aria-hidden
    >
      <polygon points={polyTop} fill={from} />
      <polygon points={polyBot} fill={to} />
    </svg>
  );
}
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/primitives/Ticker.tsx`:**

```tsx
'use client';
import React from 'react';

type Props = {
  className?: string;
  speed?: number;           // pixels per second; default 40
  children?: React.ReactNode;
};

/**
 * Horizontal marquee. Pauses on hover. Reduced-motion: stops.
 * Content is duplicated inline so the loop is seamless.
 */
export function Ticker({ className = '', speed = 40, children }: Props) {
  return (
    <div className={`overflow-hidden whitespace-nowrap relative ${className}`}>
      <style>{`
        @keyframes ticker-scroll {
          from { transform: translateX(0); }
          to   { transform: translateX(-50%); }
        }
        .ticker-track {
          display: inline-flex;
          animation: ticker-scroll linear infinite;
          animation-duration: var(--ticker-dur, 30s);
        }
        .ticker-track:hover { animation-play-state: paused; }
        @media (prefers-reduced-motion: reduce) {
          .ticker-track { animation: none; }
        }
      `}</style>
      <div
        className="ticker-track"
        style={{ ['--ticker-dur' as string]: `${Math.max(8, 2000 / speed)}s` }}
      >
        <span className="px-8">{children}</span>
        <span className="px-8" aria-hidden>{children}</span>
      </div>
    </div>
  );
}
```

- [ ] **Step 4: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build 2>&1 | tail -3
```

Expected: clean.

- [ ] **Step 5: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/components/primitives/PulseAccent.tsx apps/web/components/primitives/DiagonalDivider.tsx apps/web/components/primitives/Ticker.tsx
git commit -m "feat(web): PulseAccent + DiagonalDivider + Ticker primitives"
```

---

## Task 10: TopNav + NavLink + UserChip (TDD)

**Files:**
- Create: `apps/web/components/nav/NavLink.tsx`
- Create: `apps/web/components/nav/UserChip.tsx`
- Create: `apps/web/components/nav/TopNav.tsx`
- Create: `apps/web/tests/TopNav.test.tsx`

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/tests/TopNav.test.tsx`:

```tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';

vi.mock('next/navigation', () => ({
  usePathname: () => '/owner',
}));

import { TopNav } from '@/components/nav/TopNav';

describe('TopNav', () => {
  it('role="player" renders player nav items', () => {
    render(<TopNav role="player" />);
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Search')).toBeInTheDocument();
    expect(screen.getByText('My Bookings')).toBeInTheDocument();
    expect(screen.queryByText('Dashboard')).toBeNull();
  });

  it('role="owner" renders owner nav items', () => {
    render(<TopNav role="owner" />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Courts')).toBeInTheDocument();
    expect(screen.getByText('Slots')).toBeInTheDocument();
    expect(screen.queryByText('Search')).toBeNull();
  });

  it('marks the matching link with aria-current="page"', () => {
    // mock returns '/owner', so Dashboard should be current
    render(<TopNav role="owner" />);
    expect(screen.getByText('Dashboard').closest('a')).toHaveAttribute('aria-current', 'page');
  });
});
```

- [ ] **Step 2: Run, expect failure.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit -- TopNav 2>&1 | tail -10
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/nav/NavLink.tsx`:**

```tsx
'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import React from 'react';

type Props = {
  href: string;
  exact?: boolean;
  children: React.ReactNode;
};

/**
 * Top-nav link. Active when pathname matches `href` (exact when `exact`,
 * prefix-match otherwise). Active state: lime underline 2px, 4px below.
 */
export function NavLink({ href, exact = false, children }: Props) {
  const pathname = usePathname();
  const active = exact ? pathname === href : pathname === href || pathname.startsWith(href + '/');
  return (
    <Link
      href={href}
      aria-current={active ? 'page' : undefined}
      className={[
        'relative px-3 py-2 text-body-sm font-geist transition-colors duration-quick ease-precision focus-ring rounded-kp-chip',
        active ? 'text-ink-900 font-semibold' : 'text-ink-700/70 hover:text-ink-900',
      ].join(' ')}
    >
      {children}
      {active && (
        <span
          aria-hidden
          className="absolute left-3 right-3 bg-lime"
          style={{ bottom: '-6px', height: '2px', borderRadius: '2px' }}
        />
      )}
    </Link>
  );
}
```

- [ ] **Step 4: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/nav/UserChip.tsx`:**

```tsx
'use client';
import React from 'react';

import { Icon } from '@/components/Icon';

type Props = {
  name: string;
  role: 'player' | 'owner';
};

/**
 * Avatar + name chip in the top-right of the nav. Phase 4 NextAuth will
 * make this open a dropdown; in 5a it's a static visual element.
 */
export function UserChip({ name, role }: Props) {
  const initial = name.charAt(0).toUpperCase();
  return (
    <div className="flex items-center gap-2 px-1">
      <div
        aria-label={`${name} (${role})`}
        className="w-8 h-8 rounded-kp-pill bg-ink-900 text-lime grid place-items-center text-body-sm font-geist font-semibold"
      >
        {initial}
      </div>
      <div className="hidden md:block">
        <div className="text-body-sm font-geist text-ink-900 leading-tight">{name}</div>
        <div className="text-label-sm text-ink-700/60 leading-tight">{role}</div>
      </div>
      <Icon name="expand_more" style={{ fontSize: 18, color: '#272e42' }} />
    </div>
  );
}
```

- [ ] **Step 5: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/nav/TopNav.tsx`:**

```tsx
'use client';
import React from 'react';
import Link from 'next/link';

import { GlassPanel } from '@/components/primitives/GlassPanel';
import { Icon } from '@/components/Icon';
import { currentUser, currentOwner } from '@/lib/auth-stub';
import { NavLink } from './NavLink';
import { UserChip } from './UserChip';

type Role = 'player' | 'owner';

const PLAYER_NAV = [
  { href: '/player', label: 'Home', exact: true },
  { href: '/player/search', label: 'Search' },
  { href: '/player/bookings', label: 'My Bookings' },
];

const OWNER_NAV = [
  { href: '/owner', label: 'Dashboard', exact: true },
  { href: '/owner/venues', label: 'Courts' },
  { href: '/owner/slots', label: 'Slots' },
  { href: '/owner/pricing', label: 'Pricing' },
  { href: '/owner/bookings', label: 'Bookings' },
  { href: '/owner/insights', label: 'AI' },
];

type Props = { role: Role };

/**
 * Unified glass top nav. Replaces PlayerTopBar (kept around, unused) and
 * OwnerSidebar (kept around, unused) until 5c/5d delete them.
 */
export function TopNav({ role }: Props) {
  const nav = role === 'player' ? PLAYER_NAV : OWNER_NAV;
  const user = role === 'player' ? currentUser : currentOwner;
  const ctaHref = role === 'player' ? '/player/search' : '/owner/venues/new';
  const ctaLabel = role === 'player' ? 'Find courts' : '+ Add Court';

  return (
    <GlassPanel as="header" className="sticky top-0 z-40 h-16 px-5 md:px-8 flex items-center gap-6 border-b border-surface-med">
      <Link href={role === 'player' ? '/player' : '/owner'} className="flex items-center gap-2 focus-ring rounded-kp-chip">
        <img src="/bolt-glyph.svg" width={22} height={22} alt="" />
        <span className="font-geist font-semibold text-title-md text-ink-900 tracking-wide">
          ZPOTS
        </span>
        <span className="hidden md:inline text-label-sm text-ink-700/50 ml-1">
          {role === 'player' ? 'PLAYER' : 'BUSINESS'}
        </span>
      </Link>

      <nav className="hidden md:flex flex-1 items-center gap-1" aria-label={`${role} navigation`}>
        {nav.map((it) => (
          <NavLink key={it.href} href={it.href} exact={it.exact}>{it.label}</NavLink>
        ))}
      </nav>

      <div className="hidden md:block flex-1 md:flex-none" />

      <Link
        href={ctaHref}
        className="hidden md:inline-flex items-center gap-1 px-4 py-2 bg-lime text-ink-900 font-geist font-semibold text-body-sm rounded-kp-pill transition-transform duration-quick ease-precision hover:scale-[1.02] active:bg-lime-press focus-ring"
      >
        {ctaLabel}
      </Link>

      <UserChip name={user.name} role={role} />

      {/* Mobile menu trigger — full implementation in 5d when player pages
          actually need it. For 5a a placeholder hamburger is fine; pages
          render top-nav-less on mobile until then. */}
      <button
        type="button"
        className="md:hidden ml-auto p-2 focus-ring rounded-kp-chip"
        aria-label="Open menu"
      >
        <Icon name="menu" style={{ fontSize: 22, color: '#272e42' }} />
      </button>
    </GlassPanel>
  );
}
```

- [ ] **Step 6: Run tests, expect green.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit -- TopNav 2>&1 | tail -10
```

Expected: 3 passed.

- [ ] **Step 7: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/components/nav/NavLink.tsx apps/web/components/nav/UserChip.tsx apps/web/components/nav/TopNav.tsx apps/web/tests/TopNav.test.tsx
git commit -m "feat(web): TopNav + NavLink + UserChip (unified glass nav, role-aware)

Replaces both PlayerTopBar and OwnerSidebar visually. Active link gets
lime underline + aria-current. Mobile hamburger placeholder (full mobile
menu implementation in 5d). Existing nav components untouched."
```

---

## Task 11: PageShell + rewire player + owner layouts

**Files:**
- Create: `apps/web/components/PageShell.tsx`
- Modify: `apps/web/app/player/layout.tsx`
- Modify: `apps/web/app/owner/layout.tsx`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/PageShell.tsx`:**

```tsx
import React from 'react';

import { TopNav } from './nav/TopNav';

type Props = {
  role: 'player' | 'owner';
  children?: React.ReactNode;
};

/**
 * Shared page shell. Top nav at the top, page content in a centered main.
 * Layouts mount BookingsHydrator + ChatWidget around this; that stays in
 * the per-role layout file (not here) so PageShell stays role-agnostic.
 */
export function PageShell({ role, children }: Props) {
  return (
    <>
      <TopNav role={role} />
      <main className="max-w-[1400px] mx-auto px-5 md:px-8 py-8">
        {children}
      </main>
    </>
  );
}
```

- [ ] **Step 2: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/app/player/layout.tsx`:**

```tsx
import { ChatWidget } from '@/components/chat/ChatWidget';
import { BookingsHydrator } from '@/components/BookingsHydrator';
import { PageShell } from '@/components/PageShell';
import { currentUser } from '@/lib/auth-stub';

export default function PlayerLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <BookingsHydrator userId={currentUser.id} />
      <PageShell role="player">{children}</PageShell>
      <ChatWidget role="player" />
    </>
  );
}
```

- [ ] **Step 3: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/app/owner/layout.tsx`:**

```tsx
import { ChatWidget } from '@/components/chat/ChatWidget';
import { BookingsHydrator } from '@/components/BookingsHydrator';
import { PageShell } from '@/components/PageShell';
import { currentOwner } from '@/lib/auth-stub';

export default function OwnerLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-surface">
      <BookingsHydrator userId={currentOwner.id} />
      <PageShell role="owner">{children}</PageShell>
      <ChatWidget role="owner" />
    </div>
  );
}
```

- [ ] **Step 4: Verify build + run dev server briefly to eyeball nav.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build 2>&1 | tail -5
```

Expected: clean.

Optional manual check (start dev server, browse `/player` and `/owner` — confirm the new glass TopNav appears on both, replacing the old sidebar/top bar). Skip if not in a position to launch a browser; PR review will cover it.

- [ ] **Step 5: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/components/PageShell.tsx apps/web/app/player/layout.tsx apps/web/app/owner/layout.tsx
git commit -m "feat(web): PageShell + rewire player + owner layouts to use TopNav

Existing PlayerTopBar + OwnerSidebar untouched (unused after this commit;
deleted in 5c/5d). BookingsHydrator + ChatWidget still mounted around
the shell."
```

---

## Task 12: Update Playwright selectors

**Files:**
- Modify: `apps/web/tests/owner-flow.spec.ts`
- Modify: `apps/web/tests/player-flow.spec.ts`

The owner sidebar is gone; tests that clicked sidebar links will fail. Player top-bar links may have changed labels (`Bookings` was probably `Bookings`; new is `My Bookings`). Update selectors.

- [ ] **Step 1: Read the existing specs to find the broken selectors.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web/tests && cat owner-flow.spec.ts player-flow.spec.ts
```

Read both files. For each link-click or text-locator that targets a nav element, update to the new label:

| Old (likely) | New |
|---|---|
| `'Venue Manager'` | `'Courts'` |
| `'Slot Control'` | `'Slots'` |
| `'AI Insights'` | `'AI'` |
| `'Optimization'` | (removed from nav; access via direct URL if test needs it) |
| Sidebar role/locator | Top-nav locator (e.g. `page.getByRole('navigation')` instead of an `aside`) |

- [ ] **Step 2: Apply minimum-viable selector updates.** Replace the broken locators with the new ones above. Do NOT rewrite the test logic — only the selectors.

- [ ] **Step 3: Run Playwright.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm test 2>&1 | tail -10
```

Expected: 3 passed (landing, player-flow, owner-flow).

If any test fails for a non-selector reason (e.g. the test references a feature genuinely gone after 5a), STOP and report — don't paper over real regressions.

- [ ] **Step 4: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/tests/owner-flow.spec.ts apps/web/tests/player-flow.spec.ts
git commit -m "test(web): update Playwright selectors for new TopNav

Owner sidebar removed; nav items renamed (Venue Manager → Courts,
Slot Control → Slots, AI Insights → AI). Tests cover the same flows
through the new nav structure."
```

---

## Task 13: Final smoke + open PR

- [ ] **Step 1: Run all automated checks.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS

# Streamlit (untouched)
conda run -n MADT pytest tests/ -q

# FastAPI (untouched)
cd apps/api && conda run -n MADT pytest -q && cd ..

# Vitest + build + Playwright
cd apps/web && pnpm test:unit && pnpm build && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm test
cd ../..
```

Expected:
- Streamlit: **29 passed**
- FastAPI: **53 passed**
- Vitest: **39 passed** (30 baseline + 2 CountUp + 2 NumberFlip + 2 RevealOnScroll + 3 TopNav)
- `pnpm build`: clean
- Playwright: **3 passed**

- [ ] **Step 2: Manual browser smoke.**

Two terminals:
```bash
# Terminal A
cd apps/api && conda run -n MADT uvicorn main:app --port 8000

# Terminal B
cd apps/web && pnpm dev
```

Check `http://localhost:3000`:
- [ ] `/player` and `/owner` both show the new glass TopNav at the top
- [ ] Active link gets a lime underline below the text
- [ ] Page content below the nav still renders correctly (old `zpots.*` styles intact)
- [ ] Hovering the lime CTA scales slightly; clicking it shows the lime-press shade momentarily
- [ ] Focus ring (tab through nav) shows ink+lime double ring
- [ ] Toggle macOS "Reduce motion" in System Settings → reload → no perceptible animation on hover/focus, but lush durations still feel polished
- [ ] Chat widget still floats bottom-right and works as before
- [ ] No console errors

- [ ] **Step 3: Push + open PR.**

```bash
git push -u origin feat/nextjs-phase5a
gh pr create --base main --title "Phase 5a: design foundation (tokens + primitives + TopNav)" --body "$(cat <<'EOF'
## Summary

Phase 5a of the design revamp: foundation only. Adds new design tokens (KP + Motion: ink/lime/surface ramps, Geist fonts, motion + spacing scales), eight reusable primitives, a unified glass TopNav that replaces both PlayerTopBar and OwnerSidebar, and a PageShell shared across layouts.

**No page content visibly changes in this PR.** Only the chassis (nav) does. The new tokens/primitives are unused by pages until sub-phases 5b–5e migrate them.

- Spec: \`docs/superpowers/specs/2026-05-17-phase5a-design-foundation-design.md\`
- Plan: \`docs/superpowers/plans/2026-05-17-phase5a-design-foundation.md\`

## What ships

**Tokens** (added alongside legacy \`zpots.*\` which stays untouched):
- Color: \`lime\` / \`lime-press\` / \`lime-deep\` · \`ink-900/800/700\` · \`surface\` / \`surface-low/med/high\`
- Type: \`font-geist\` + \`font-geist-mono\` + display scale (display-lg, display-md, title-lg, title-md, body-md/sm, label-sm)
- Motion: \`duration-instant/quick/smooth/lush\` + \`ease-precision\` + \`prefers-reduced-motion\` collapse
- Surface: \`shadow-float\` + \`shadow-lift\` + glass utility, no-line philosophy
- Radius: \`rounded-kp-card\` (12px) / \`rounded-kp-pill\` (999) / \`rounded-kp-chip\` (2 — the signature)
- Accessibility: \`.focus-ring\` utility (ink + lime double ring), \`.tabular-nums\`

**Primitives** (\`components/primitives/\`):
\`GlassPanel\` · \`DarkHero\` · \`CountUp\` · \`NumberFlip\` · \`RevealOnScroll\` · \`PulseAccent\` · \`DiagonalDivider\` · \`Ticker\`

**Nav** (\`components/nav/\`):
\`TopNav\` (role="player" | "owner") + \`NavLink\` (active = lime underline + aria-current) + \`UserChip\`

**Shell** (\`components/PageShell.tsx\`):
Wraps page content in TopNav + centered \`<main>\`. Mounted in both \`app/player/layout.tsx\` and \`app/owner/layout.tsx\`.

## Tests

| Suite | Result |
|---|---|
| Streamlit | 29 / 29 ✅ |
| FastAPI | 53 / 53 ✅ |
| Vitest | 39 / 39 ✅ (+9 in 5a: CountUp, NumberFlip, RevealOnScroll, TopNav) |
| Playwright | 3 / 3 ✅ (selectors updated for new nav) |
| \`pnpm build\` | clean ✅ |

## What's intentionally NOT in this PR

- Page-level visual changes — 5b owner dashboard anchor
- Owner cascade (Venues / Slots / Pricing / etc.) — 5c
- Player revamp — 5d
- Chat widget polish — 5e
- Deletion of \`PlayerTopBar\` + \`OwnerSidebar\` — happens in 5c/5d when their last consumer is gone
- Backend changes — none planned for any 5x

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Return the PR URL.

---

## Out of scope for Phase 5a (do NOT add)

- Any visible change to page content (pages stay on legacy `zpots.*` tokens until per-page migration in 5b+)
- Page-level layout changes
- Dashboard / Search / Bookings / Court detail redesigns → 5b–5d
- ChatWidget visual update → 5e
- Visual regression tooling → revisit after 5b
- Deletion of legacy `PlayerTopBar` / `OwnerSidebar` → 5c/5d
- Backend changes
- Mobile menu full implementation (just a placeholder hamburger button in 5a) → 5d
- Streamlit changes
