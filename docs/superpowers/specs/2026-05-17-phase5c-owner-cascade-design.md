# Phase 5c — Owner Cascade Design

**Status:** approved 2026-05-17 (autonomous per [[feedback-design-revamp-autonomy]])
**Sub-phase of:** Phase 5. Prior: 5b owner anchor.

## Goal

Apply the KP+Motion language (locked in 5b) to the remaining owner pages: Venues, Slots, Pricing, Optimization, and the Add/Edit Court forms. Each page gets a `<PageHero>` header, new card style (`bg-white rounded-kp-card shadow-float`), and Geist typography. After 5c, every owner-side page shares the same language and the legacy `OwnerSidebar` component can finally be deleted.

## Pages in scope

1. `/owner/venues` — venue grid/list
2. `/owner/venues/new` — register new venue (wraps `CourtForm`)
3. `/owner/venues/[id]/edit` — edit venue (wraps `CourtForm`)
4. `/owner/slots` — slot calendar control
5. `/owner/pricing` — pricing setup
6. `/owner/optimization` — opportunity insights

## Transformation rules

These rules apply uniformly across all six pages. The implementer pattern-matches.

**Header pattern (every page):**
```tsx
// Before:
<div>
  <h1 className="font-display text-3xl font-bold">Title</h1>
  <p className="text-sm text-zpots-muted">Subtitle...</p>
</div>

// After:
<PageHero
  eyebrow="EYEBROW · CONTEXT"
  headline="Page title."
  sub="Subtitle copy here."
  cta={<CtaButton />}
/>
```

**Card style swaps (mechanical):**

| Old class | New class |
|---|---|
| `zpots-card p-X` | `bg-white rounded-kp-card shadow-float p-X` |
| `zpots-card-surface p-X` | `bg-surface-low rounded-kp-card p-X` |
| `zpots-card-dark p-X` | wrap content in `<DarkHero glow="lime" className="p-X">...</DarkHero>` |
| `zpots-card-lime p-X` | wrap content in `<DarkHero glow="lime" className="p-X">...</DarkHero>` (lime callout becomes dark hero with lime accents inside) |
| `font-display` | `font-geist` |
| `font-display text-3xl font-bold` | use `<PageHero headline=...>` for h1; for sub-section h3 use `font-geist font-semibold text-title-md` |
| `text-zpots-muted` | `text-ink-700/60` |
| `text-zpots-moss` | `text-lime-deep` (for emphasis text on light bg) |
| `text-zpots-ink` | `text-ink-900` |
| `bg-zpots-surface` | `bg-surface-low` |
| `border-zpots-mint` | drop the border (no-line philosophy); use background-shift |
| `rounded-card` (16px) | `rounded-kp-card` (12px) |
| `rounded-pill` | `rounded-kp-pill` |

**Motion:**
- Wrap major sections (page-level groups, not individual cards) in `<RevealOnScroll>` with `delay={i * 80}` for sequential groups
- Big numbers (KPIs, revenue) use `<NumberFlip>` or `<CountUp>` on first mount

**Card containers:**
- All section headings use `font-geist font-semibold text-title-md text-ink-900` (was `font-semibold` only)
- Card sub-labels use `text-label-sm text-ink-700/60` (was `font-eyebrow` or `text-xs text-zpots-muted`)

**`KpiCard`, `AITag`, `Eyebrow`, `StatusBadge`** — API unchanged; the underlying components were upgraded in 5b. Just use them.

## Page-specific

### `/owner/venues`
- PageHero: eyebrow `MANAGE COURTS · 6 LOCATIONS`, headline `Your court portfolio.`, sub copy, CTA `+ Register Venue`
- View toggle chips (GRID / LIST) use the new chip style: `bg-lime text-ink-900` for active, `bg-surface-low text-ink-700` for inactive
- Court cards: inline status pill changes to `bg-lime text-ink-900` (already accommodates the readability issue noted in the comment)
- Court card body uses new typography

### `/owner/venues/new` and `/owner/venues/[id]/edit`
These are very thin wrappers around `components/owner/CourtForm.tsx`. Read the form, apply card-style swaps and font-display → font-geist within it. Page wrappers get `<PageHero>` with appropriate copy.

### `/owner/slots`
- PageHero: eyebrow `SLOT CONTROL`, headline `Precision schedule.`, sub mentions AI 97% forecast, CTA `+ Add New Slot`
- AI tag stays inline below hero
- `SlotCalendar` component (inside `components/owner/`) — apply token swaps internally
- KpiCards work as-is (they were upgraded in 5b)

### `/owner/pricing`
- PageHero: eyebrow `PRICING SETUP · 6 TIERS LIVE`, headline `Revenue Today: <NumberFlip currency 128400/>`, sub copy
- Replace `.zpots-card-dark` revenue banner with content folded into hero (since hero already shows revenue)
- Court tier strip: `bg-white rounded-kp-card shadow-float` instead of `.zpots-card`
- Base rates form: `bg-white rounded-kp-card shadow-float p-5`; inputs use existing `.field-input` (preserved through 5c)
- Lime AI card → `<DarkHero glow="lime" className="p-5">` with PulseAccent on the suggested-price CTA

### `/owner/optimization`
- PageHero: eyebrow `AI OPS · PRIORITY INSIGHT`, headline `Optimization engine.`, sub copy
- `OpportunityCard` component (inside `components/owner/`) — apply token swaps
- Three benchmark cards below: `bg-white rounded-kp-card shadow-float p-4` with new typography

## Components to upgrade in-place

- `components/owner/SlotCalendar.tsx` — token + typography swap
- `components/owner/OpportunityCard.tsx` — token + typography swap
- `components/owner/CourtForm.tsx` — token + typography swap

## Delete after cascade

- `components/OwnerSidebar.tsx` — no consumer left after 5c. Delete in the same PR.

## Tests

| Suite | Expected |
|---|---|
| Streamlit | 29 / 29 ✅ (untouched) |
| FastAPI | 53 / 53 ✅ (untouched) |
| Vitest | 43 / 43 ✅ (no new tests; token swaps are pattern application) |
| Playwright | 2 / 3 ✅ (owner-flow may need minor selector updates if heading text changed) |
| `pnpm build` | clean |

## Out of scope

- Player pages → 5d
- Chat widget → 5e
- New unit tests (the pattern-application is visual; manual smoke covers regressions)

## Open questions

None.
