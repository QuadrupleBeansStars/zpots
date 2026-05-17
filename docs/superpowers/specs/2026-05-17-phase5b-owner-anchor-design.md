# Phase 5b — Owner Dashboard Anchor Design

**Status:** approved 2026-05-17 (autonomous execution per [[feedback-design-revamp-autonomy]])
**Sub-phase of:** Phase 5. Prior: 5a foundation. Next: 5c owner cascade.

## Goal

Apply Kinetic Precision + Motion to the three highest-value owner surfaces — Dashboard, AI Insights, and Bookings — using the primitives shipped in 5a. This is the "wow" moment: the dashboard goes from generic-grid-of-cards to dark-hero-with-live-numbers, the AI callout pulses, charts reveal on scroll, KPIs flip in.

## Pages in scope

1. `/owner` — main dashboard (biggest transformation)
2. `/owner/insights` — AI insights (dark hero header, restyled cards)
3. `/owner/bookings` — booking list (revenue hero, restyled rows)

Other owner pages (venues, slots, pricing, optimization) stay on legacy `zpots.*` tokens until 5c.

## Visual language

**Header pattern (every page in scope):**
- `<DarkHero glow="lime">` full-bleed at the top
- Inside: eyebrow date stamp · big display-lg numbers via `<NumberFlip>` · sub-line · right-aligned CTA
- Below the hero: page content on `surface-low` background

**Card pattern:**
- Replace `.zpots-card` (white + rounded-card + shadow-card) usages with: `bg-white rounded-kp-card shadow-float p-5` — no border, just background-shift
- Use `<RevealOnScroll>` with `delay={i * 80}` for staggered groups

**Data-emphasis pattern:**
- Numbers in `font-geist-mono tabular-nums` with `<CountUp>` or `<NumberFlip>` on first paint
- Trend deltas in `text-lime-deep` (positive) or `text-red-700` (negative) with arrow glyphs
- KPIs that update over time use `<NumberFlip>`; one-shot reveals use `<CountUp>`

**AI callout pattern:**
- `<DarkHero>` inner mini variant — dark ink background, lime accent text
- CTA wrapped in `<PulseAccent>` until user interacts

## Page-by-page

### 1. `/owner/page.tsx` — Dashboard

**Hero (replaces header + first KPI row):**
```
DarkHero(glow=lime)
  eyebrow: LIVE · MON OCT 28
  h1 display-lg: <NumberFlip value=128/> bookings.
  h1 display-lg lime: <NumberFlip value=64500 format=currency/>
  sub body-md/60: "Court 3 is your top performer — 92% utilization this week."
  right side: [+ Add Court] CTA (bg-lime, text-ink-900)
```

**Pill tab strip** under hero:
- `UTILIZATION ↗ +12%` (active, lime bg, ink text)
- `REVENUE` (text-only)
- `NO-SHOW RISK` (text-only)

**Two-col split** (2/3 + 1/3):
- **Left (2/3): Chart card** — white bg, rounded-kp-card, shadow-float. Title `Utilization Trends` in geist title-md. Below: `<UtilizationBars>` updated to use lime gradient bars (replace flat green) with on-mount reveal stagger.
- **Right (1/3): AI Card** — `<DarkHero>` inner with `<PulseAccent>` around the Approve CTA. Content: `▲ Raise Friday pricing 18% → +฿2,400/wk expected`.

**Today's Bookings** (full width below):
- Geist title `Today's Bookings`
- Stack of booking rows in `<RevealOnScroll delay={i*80}>` wrappers
- Each row: time (display-md geist-mono) + court info + status badge

**Manage Venues** (4-col grid below, replaces sidebar list):
- Each venue card: image header + name + sport pill + util% + edit cta
- Use real venue placeholders for now (next sub-phase brings real images)

### 2. `/owner/insights/page.tsx` — AI Insights

**Hero:**
```
DarkHero(glow=lime)
  eyebrow: AI INSIGHTS · 7-DAY FORECAST
  h1 display-md: Bangkok demand intelligence.
  sub: "Live signals from your venues + our models, fused."
  right: [Generate AI Summary] CTA
```

**Below hero:** existing layout adapted with new card style:
- Generated summary block (when present) → `bg-surface-low rounded-kp-card p-5` with AITag accent
- Two-col: Demand Heatmap + Peak Utilization (both restyled with new shadow + geist titles)
- District demand row (3-col) — keep StatusBadge for tier
- No-show Risk Analysis + AI Mitigation Strategies (two-col bottom)

### 3. `/owner/bookings/page.tsx` — Bookings

**Hero:**
```
DarkHero(glow=lime)
  eyebrow: TODAY · MON OCT 28
  h1 display-lg: <NumberFlip value=4280 format=currency/>
  sub: "+15.6% from yesterday · 12 upcoming sessions"
  right-aligned mini-breakdown chips: Main Arena ฿1,240 · Padel Pod 2 ฿890 · Indoor Turf ฿2,150
```

**Below hero:** existing filter chips + venue/sort selects (restyled inputs) + bookings table — restyled rows with new tokens (`bg-white rounded-kp-card shadow-float p-3`).

`<RevenueBanner>` component effectively replaced by the hero; either delete it from this page or repurpose as a smaller secondary breakdown.

## Components / new in 5b

- `<PageHero>` — wrapper around `<DarkHero>` with the eyebrow + headline + sub + CTA slot. Reusable across all three pages.
- `<KpiPill>` — small inline KPI for the hero's right side (e.g. revenue breakdown chips). Lime text on dark ink bg.
- `<TabStrip>` — pill-tab navigation row (UTIL / REVENUE / NO-SHOW). State stays page-local in 5b; future phases may wire it to actual tab content.

All other 5a primitives reused.

## Migration of existing components

- `KpiCard` — restyled internally to new tokens. Still consumed by 5c pages, so don't delete; just upgrade the visuals.
- `UtilizationBars` — bars get `lime-gradient` background and on-mount scale-y reveal with stagger
- `RevenueBanner` — repurposed as a sub-section (no longer the page header on bookings)
- Tags / StatusBadge / Eyebrow / AITag — no API change; small token-color tweaks only

## Tests

| Suite | Expected |
|---|---|
| Streamlit | 29 / 29 ✅ (untouched) |
| FastAPI | 53 / 53 ✅ (untouched) |
| Vitest | 39+ / 39+ ✅ (add tests for `<PageHero>`, `<TabStrip>` — ~3-4 tests) |
| Playwright | 2 / 3 (player-flow still pre-existing fail; owner-flow needs selector update for new dashboard DOM) |
| `pnpm build` | clean |

**Manual smoke critical:** the dashboard load animation (NumberFlip, RevealOnScroll, PulseAccent) is the entire point — confirm via browser.

## Out of scope (defer to 5c)

- Venues / Slots / Pricing / Optimization pages
- Delete `OwnerSidebar.tsx` (still present, unused)
- Owner-side data table redesign beyond the bookings page

## Open questions

None — autonomous execution per memory note.
