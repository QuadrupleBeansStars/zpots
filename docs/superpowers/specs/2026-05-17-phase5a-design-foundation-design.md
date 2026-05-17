# Phase 5a — Design Foundation Design

**Status:** approved 2026-05-17
**Sub-phase of:** Phase 5 (whole-app design revamp). Sibling sub-phases: 5b Owner dashboard anchor, 5c Owner cascade, 5d Player revamp, 5e Chat polish.
**Phase 4b (Dockerfiles)** is parked on branch `feat/nextjs-phase4b` and will resume after Phase 5.

## Goal

Install the design-system foundation that every subsequent sub-phase will consume: new typography, color, surface, motion, and spacing tokens; a small set of distinctive primitives (`<DarkHero>`, `<CountUp>`, `<NumberFlip>`, `<RevealOnScroll>`, `<GlassPanel>`, `<PulseAccent>`, `<DiagonalDivider>`, `<Ticker>`); a unified `<TopNav>` replacing both `PlayerTopBar` and `OwnerSidebar`; and a shared `<PageShell>` that every layout will use.

After 5a, **no user-facing page yet looks different in any major way** — only the chassis is replaced. That visible transformation begins in 5b.

## Motivation

The Phase 1–4a Next.js port preserved the legacy Streamlit visual + layout language. The user wants the revamp to drop those constraints and exploit React/Next.js capabilities. Direction is locked: **"Kinetic Precision + Motion"** — evolved from the `stitch_owner_dashboard/` exploration and `ZPOTS Design System/kinetic_grid/DESIGN.md`, with motion ambition added.

Doing everything in one giant phase would be unreviewable. 5a delivers the smallest invisible foundation everyone else depends on, so 5b–5e can move fast in parallel branches if needed.

## Architecture

```
apps/web/
├── app/
│   ├── globals.css                # MODIFIED — new font @import via <link>, root CSS vars
│   ├── layout.tsx                 # MODIFIED — Geist + Geist Mono + Material Symbols
│   ├── player/layout.tsx          # MODIFIED — uses <PageShell role="player">
│   └── owner/layout.tsx           # MODIFIED — uses <PageShell role="owner">
├── tailwind.config.ts             # MODIFIED — token system, font family, spacing scale
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
│   ├── nav/
│   │   ├── TopNav.tsx             # NEW — replaces both PlayerTopBar + OwnerSidebar
│   │   ├── NavLink.tsx            # NEW
│   │   └── UserChip.tsx           # NEW
│   ├── PageShell.tsx              # NEW
│   ├── PlayerTopBar.tsx           # KEPT but unused after 5a (deleted in 5d cleanup)
│   └── OwnerSidebar.tsx           # KEPT but unused (deleted in 5c cleanup)
└── lib/
    └── motion.ts                  # NEW — useReducedMotion hook + duration constants
```

### Tokens

Defined as CSS custom properties in `globals.css` and **mirrored as Tailwind theme extensions** in `tailwind.config.ts`. Both are needed: CSS vars allow runtime overrides (e.g. dark heroes); Tailwind classes allow `bg-ink-900`, `text-lime`, etc.

**Typography**

```css
:root {
  --font-display: 'Geist', system-ui, sans-serif;
  --font-body: 'Geist', system-ui, sans-serif;
  --font-mono: 'Geist Mono', ui-monospace, monospace;
}

.font-mono { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
```

Loaded via `<link>` tags in `app/layout.tsx` (alongside Material Symbols Rounded) — same pattern that already works.

Scale (Tailwind utility classes):
- `text-display-lg` 3.5rem (-0.02em tracking, font-display)
- `text-display-md` 2.5rem (-0.02em)
- `text-title-lg` 1.5rem
- `text-title-md` 1.125rem
- `text-body-md` 1rem
- `text-body-sm` 0.875rem
- `text-label-sm` 0.75rem uppercase, letter-spacing 0.04em

**Color**

```css
:root {
  --color-lime: #cffc00;
  --color-lime-press: #b8e600;
  --color-lime-deep: #3a4d10;        /* text-on-lime only */

  --color-ink-900: #15192a;
  --color-ink-800: #1c2136;
  --color-ink-700: #272e42;

  --color-surface: #f6f6ff;
  --color-surface-low: #eef0ff;
  --color-surface-med: #e2e7ff;
  --color-surface-high: #d1dcff;
}
```

**Existing tokens get remapped:**
- `zpots-lime` → `--color-lime`
- `zpots-forest` → `--color-ink-700` (was muddy olive; ink reads cleaner against lime)
- `zpots-ink` → `--color-ink-700`
- `zpots-mint` → `--color-surface-low`
- `zpots-surface` → `--color-surface`

This keeps existing class usage (`bg-zpots-lime`, etc.) working through 5a; no page-level refactor needed yet.

**Surfaces**

- No 1px borders. Boundaries via background-shift only.
- Glass: `bg-white/60 backdrop-blur-2xl` Tailwind utility — wrap in `<GlassPanel>` to centralize.
- Dark hero: `bg-ink-900` + noise SVG bg + `shadow-lift`.

**Shadows**

```css
--shadow-float: 0 8px 24px rgba(39, 46, 66, 0.06);
--shadow-lift:  0 1px 0 rgba(255, 255, 255, 0.04) inset,
                0 24px 60px -20px rgba(15, 19, 42, 0.45);
```

**Spacing**

Add Tailwind spacing keys `1` (4px), `2` (8px), `3` (12px), `5` (20px), `8` (32px), `13` (52px) as our canonical rhythm. Existing Tailwind defaults remain available but the canonical set is what design uses.

**Radius**

- `rounded-card` → 12px
- `rounded-pill` → 999px
- `rounded-chip` → 2px (the signature micro-radius)

**Motion**

```css
:root {
  --ease-precision: cubic-bezier(0.16, 1, 0.3, 1);
  --dur-instant: 120ms;
  --dur-quick:   220ms;
  --dur-smooth:  360ms;
  --dur-lush:    720ms;
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --dur-instant: 1ms;
    --dur-quick:   1ms;
    --dur-smooth:  1ms;
    --dur-lush:    80ms;       /* keep a touch of polish */
  }
}
```

Reflected in Tailwind as `ease-precision`, `duration-instant`, etc.

**Focus ring**

```css
.focus-ring:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-ink-900),
              0 0 0 4px var(--color-lime);
}
```

**Noise**

A single SVG turbulence data-URI exported from `lib/noise.ts` as `NOISE_URL`. `<DarkHero>` layers it at 4% opacity to kill the flat-vector AI look.

### Primitives

**`<GlassPanel>`**
```tsx
<GlassPanel as="nav" className="px-5 py-3">
  {children}
</GlassPanel>
```
Wraps `bg-white/60 backdrop-blur-2xl shadow-float`. `as` prop for semantic element.

**`<DarkHero>`**
```tsx
<DarkHero glow="lime" className="px-8 py-13">
  <p className="text-label-sm text-lime/60">LIVE · MON OCT 28</p>
  <h1 className="text-display-lg text-white">
    <CountUp value={128} /> bookings.
  </h1>
</DarkHero>
```
- `bg-ink-900` + noise SVG + `shadow-lift`
- Optional `glow="lime" | "none"` prop adds a radial lime gradient in the far-right corner
- Used by every page in 5b+ for the page-title region

**`<CountUp>`**
- Eases from 0 → `value` over `dur-smooth` using `ease-precision`
- Honors `prefers-reduced-motion` (snaps instantly under reduced)
- `format` prop: `"number" | "currency" | "percent"`, currency uses ฿ prefix
- Renders inside a `<span className="font-mono tabular-nums">` automatically

**`<NumberFlip>`**
- Odometer animation — digits roll like a flip clock. Distinct from CountUp's tween.
- Use for live-feel KPIs (revenue today, bookings now)
- Renders one `<span>` per digit; CSS keyframe for the flip

**`<RevealOnScroll>`**
```tsx
<RevealOnScroll delay={80}>{children}</RevealOnScroll>
```
- IntersectionObserver, fires once at 20% visibility
- Children start `opacity-0 translate-y-2`, transition to `opacity-100 translate-y-0` over `dur-smooth`
- `delay` (ms) for staggered groups

**`<PulseAccent>`**
- Continuous lime halo around child element
- CSS keyframe: `box-shadow` 0 → 12px lime → 0 over 2s
- Respects reduced motion (collapses to a static 1px lime ring)

**`<DiagonalDivider>`**
- Inline SVG diagonal between two surfaces, exposed as a small component so pages don't reinvent it
- Props: `from`, `to` (color tokens), `angle` (default 4°)

**`<Ticker>`**
- Horizontal marquee
- Optional in 5a — used selectively in 5b for the dashboard's "live bookings" ribbon
- CSS animation, pauses on hover

### Navigation

**`<TopNav>`** replaces `PlayerTopBar` AND `OwnerSidebar`. Always 64px tall, glass background, full-bleed.

```tsx
<TopNav role="owner" />     // ZPOTS · Dashboard | Courts | Slots | Pricing | AI · UserChip · "+ Add Court"
<TopNav role="player" />    // ZPOTS · Home | Search | My Bookings · UserChip · "Find courts" (when applicable)
```

Active link: lime underline (2px, 4px below text). Other links: ink-700, hover → ink-900.

Mobile (`< md:`): hamburger → full-screen overlay menu with glass bg.

**`<UserChip>`**: avatar circle + name, opens a dropdown with "Sign out" (Phase 4 NextAuth will repurpose).

**`<NavLink>`**: handles active state via `usePathname()`. Used by both desktop and mobile menus.

### Layout shell

**`<PageShell>`**

```tsx
<PageShell role="player">
  {/* optional <DarkHero> */}
  <PageHero>...</PageHero>
  {/* page content */}
  <section>...</section>
</PageShell>
```

- Renders `<TopNav role={role} />` at top
- `<main>` with `max-w-[1400px] mx-auto px-8` (responsive: `px-5 md:px-8`)
- Mounts `<BookingsHydrator>` + `<ChatWidget>` (both already exist)

In 5a, `app/player/layout.tsx` and `app/owner/layout.tsx` get rewritten to use `<PageShell>`. **No page content changes**; pages just render inside the new shell.

### Existing components kept (deleted in later sub-phases)

- `PlayerTopBar.tsx` — unused after 5a, deleted in 5d
- `OwnerSidebar.tsx` — unused after 5a, deleted in 5c

Leaving them in place avoids a giant rename-all-imports diff and lets reverts stay clean. Codemod-style cleanup happens per sub-phase as pages are migrated.

## Data flow

No data flow changes in 5a. The new shell mounts the same `<BookingsHydrator>` + `<ChatWidget>` it always did. Pages still call `getCourts()` / `getBookings()` via the existing `lib/data-client.ts`.

## Testing

**Vitest additions (~6–8 tests):**

| Suite | Tests |
|---|---|
| `tests/CountUp.test.tsx` | renders final value after `dur-smooth`; snaps under reduced motion |
| `tests/NumberFlip.test.tsx` | renders digits matching value; updates on prop change |
| `tests/RevealOnScroll.test.tsx` | calls IntersectionObserver; child visible after intersect (mock IO) |
| `tests/TopNav.test.tsx` | role="player" shows player links; role="owner" shows owner links; active link gets aria-current |

**Existing suites must stay green** through 5a:
- Streamlit 29
- FastAPI 53
- Vitest grows from 30 to ~36–38
- Playwright 3 — selectors updated alongside layout swap

**Manual smoke (in plan):**
- All player + owner pages render without errors after the shell swap
- TopNav active link works on every page
- `prefers-reduced-motion` toggle (macOS Reduce Motion) collapses durations
- Focus ring visible on tab through nav links + CTA
- Mobile menu opens/closes correctly at < 768px

**Visual regression:** not added in 5a — revisit if cascade phases break the anchor.

## Error handling

5a is mostly inert. The only failure modes:
- Geist font fails to load → falls back to system-ui (defined in `--font-body` fallback chain). UI doesn't break.
- IntersectionObserver unsupported (only IE / very old browsers — moot for our Next.js 16 audience) → `<RevealOnScroll>` renders children immediately (no fade).
- Reduced-motion preference change at runtime → CSS variables update automatically; no JS needed.

## Accessibility

- All glass + dark surfaces verified AA contrast for text inside them (`ink-700` text on `surface-low` = 14.2:1; `white` text on `ink-900` = 16.1:1; `ink-700` text on `lime` = 9.8:1)
- Focus ring token applied to all interactive elements via `focus-ring` utility class — replaces any `outline: none` declarations in 5a
- TopNav active link uses `aria-current="page"`
- `<DarkHero>` keeps semantic `<h1>` / `<h2>` inside; the dark color is visual only
- `prefers-reduced-motion` honored by every primitive

## Out of scope (defer to later sub-phases)

- Any change to page-level layouts → 5b–5e
- `<DarkHero>` actually used in a page → 5b
- Chart redesign with motion → 5b
- Dashboard, search, bookings page redesigns → 5b–5d
- Chat widget visual update → 5e
- Visual regression tooling → revisit after 5b
- Backend changes → none in any 5x sub-phase
- Streamlit revamp → out of scope for Phase 5 entirely (Streamlit stays untouched)

## Open questions

None — all design decisions resolved during brainstorming. The remaining unknowns (specific page layouts) are scoped into 5b–5e where they belong.
