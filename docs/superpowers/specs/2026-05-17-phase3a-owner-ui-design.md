# Phase 3a — Owner UI (Read-Only with Mock Data) Design

**Date:** 2026-05-17
**Status:** Approved
**Base spec:** `docs/superpowers/specs/2026-05-16-nextjs-migration-design.md`
**Phase position:** 3a of 4 (Phase 1 + Phase 2 merged)

---

## Goal

Build all 7 owner-side pages plus login and add/edit-court form in `apps/web/`, fed by a mock data layer in `apps/web/lib/owner-mock-data.ts`. No real backend yet — FastAPI lands in Phase 3b, chat in Phase 3c.

---

## Why "3a" instead of one Phase 3

The original Phase 3 lumped together (1) owner pages, (2) FastAPI scaffold + AI helper endpoints, and (3) the chat widget + chat backend. That's ~60 tasks across three independent subsystems. We split into:

- **3a (this spec):** Owner UI with mock data. Mirrors the Phase 2 pattern (`lib/mock-data.ts`-shaped data, no Zustand because no writes).
- **3b:** FastAPI scaffold at `apps/api/` + AI helper endpoints (parse-search, insights, court-description) called from Next.js via thin Route Handlers. Replaces mock AI summary with the live endpoint.
- **3c:** Chat agents — port `agents/player/*` and `agents/owner/*` to FastAPI routers, build a streaming chat widget in Next.js (Vercel AI SDK `useChat`).

Each gets its own brainstorm → spec → plan → PR cycle.

---

## Architecture

```
apps/web/app/owner/
├── layout.tsx                          # OwnerSidebar + content container
├── login/page.tsx                      # form UI only, redirects to /owner
├── page.tsx                            # dashboard
├── venues/
│   ├── page.tsx                        # manage courts (GRID/LIST toggle via URL param)
│   └── [id]/edit/page.tsx              # add/edit court — same page handles "new" via [id] = "new"
├── slots/page.tsx                      # week calendar with seeded slot blocks
├── pricing/page.tsx                    # base rates form + AI suggestion card + elasticity chart
├── bookings/page.tsx                   # revenue banner + filters + booking rows + no-show risk
├── insights/page.tsx                   # demand heatmap + utilization + no-show + mitigation
└── optimization/page.tsx               # opportunity card + predicted outcomes + benchmarks

apps/web/components/owner/
├── DemandHeatmap.tsx                   # CSS-grid heatmap 7×16, lime-scale color
├── SlotCalendar.tsx                    # week grid
├── RevenueBanner.tsx                   # green gradient banner used on /owner/bookings
└── OpportunityCard.tsx                 # lime card used on /owner/optimization

apps/web/lib/
├── owner-mock-data.ts                  # OWNER_VENUES, WEEKLY_UTILIZATION, DISTRICT_DEMAND,
│                                       # TODAYS_BOOKINGS, OWNER_BOOKINGS, DEMAND_FORECAST
└── auth-stub.ts                        # MODIFIED — adds currentOwner

apps/web/tests/
└── owner-flow.spec.ts                  # Playwright: landing → owner login → click sidebar items
```

---

## Route map (Streamlit → Next.js)

| Streamlit page | Next.js route | Notes |
|---|---|---|
| `pages/owner/login.py` | `/owner/login` | Form UI only; submit redirects to `/owner` |
| `pages/owner/dashboard.py` | `/owner` | 4 KPI cards + utilization bar chart + today's bookings list + manage-venues right column |
| `pages/owner/manage_courts.py` | `/owner/venues` | GRID/LIST toggle via `?view=list`. GRID iterates COURTS as cards; LIST as compact rows |
| `pages/owner/add_edit_court.py` | `/owner/venues/[id]/edit` and `/owner/venues/new` | Court fundamentals form, sport category, surface, location, amenities checkboxes, AI court description button (placeholder text in 3a, real call in 3b) |
| `pages/owner/manage_slots.py` | `/owner/slots` | Week header (MON 12 — SUN 18) + slot calendar grid + AI performance prediction KPIs |
| `pages/owner/pricing.py` | `/owner/pricing` | Base hourly rates form + AI Live Insight card with suggested adjustment + pricing elasticity chart |
| `pages/owner/booking_dashboard.py` | `/owner/bookings` | Green revenue banner + venue breakdown + Today/This Week/Calendar tabs + bookings table with status + no-show risk pill |
| `pages/owner/ai_insights.py` | `/owner/insights` | "Generate AI Summary" CTA (shows seeded mock text on click) + Bangkok demand heatmap + peak utilization bars + No-Show Risk Analysis + Mitigation Strategies card |
| `pages/owner/optimization.py` | `/owner/optimization` | Live opportunity card (Friday 21:00 +80% demand) + predicted outcomes lime card + benchmark cards |

---

## What gets reused from Phase 1+2

- `OwnerSidebar` (already in `apps/web/components/`) — wired into `app/owner/layout.tsx`
- `Button`, `Icon`, `KpiCard`, `Tags` (AITag, StatusBadge, Chip, Eyebrow)
- `UtilizationBars` from `apps/web/components/charts/` — Recharts wrapper
- Design system classes (`zpots-card`, `zpots-card-lime`, `zpots-card-dark`, `ai-tag`, status badges)
- Tailwind utilities (`font-display`, `text-zpots-*`)

---

## New data shapes

Add to `apps/web/lib/owner-mock-data.ts`:

```ts
export type OwnerVenue = {
  id: string;
  name: string;
  location: string;
  courts_count: number;
  revenue_today: number;
  color: string;
};

export type WeeklyUtilization = { day: string; pct: number }[];

export type DistrictDemand = {
  name: string;
  demand: number;
  level: 'Peak' | 'Moderate' | 'Saturated';
};

export type OwnerBookingRow = {
  customer: string;
  member_id: string;
  court: string;
  sport: string;
  time: string;
  status: 'CONFIRMED' | 'COMPLETED' | 'IN PROGRESS' | 'CANCELLED';
  avatar_color: string;
};

export type DemandCell = {
  day_of_week: number;   // 0=Mon..6=Sun
  hour: number;          // 7..22
  predicted_bookings: number;
};
```

Seeded constants modelled on `legacy/data/dummy_data.py` (currently at the root since Streamlit stays put — read once, copy values verbatim). Three owner venues, weekly utilization for Mon-Sun, three demand districts, ~12 today's bookings + historical demo rows, full 7×16 demand forecast.

---

## Components

### `DemandHeatmap.tsx`

Pure-CSS grid heatmap (no chart library). Renders a 16-column (hours 07–22) × 7-row (Mon–Sun) grid of `<div>` cells whose `background` interpolates between `#F2F9EE` (zpots-surface) and `#1E4A00` (zpots-forest) based on `predicted_bookings`. Axis labels (hour / day) rendered as flex rows around the grid. ~50 lines.

### `SlotCalendar.tsx`

7-column grid (one per day of the week). Each column has a header pill (`MON 12`, `TUE 13`, …) and a vertical stack of slot blocks. Today's column gets `chip-selected`. Slot block colors derived from the slot type (Open Booking = lime, Maintenance = warm, Tournament = mint). ~80 lines.

### `RevenueBanner.tsx`

Green gradient `<div>` matching the legacy Streamlit pattern. Takes `total: number`, `delta: string`, `breakdown: { label: string; amount: number }[]`. White text on `linear-gradient(135deg, #1a3a2a, #2E6B00)`. ~30 lines.

### `OpportunityCard.tsx`

Two-column flex: left side is "LIVE OPPORTUNITY" eyebrow + headline + revenue lift + body text + Adjust Slots Now / Dismiss Insight buttons. Right side is "PREDICTED OUTCOMES" lime card with weekly earnings + occupancy rate. ~80 lines.

---

## State management

| State | Where |
|---|---|
| Court list, owner venues, weekly stats, district demand, today's bookings, demand forecast | `lib/owner-mock-data.ts` (static) |
| `/owner/venues` GRID/LIST view | URL search param `?view=list` |
| `/owner/bookings` venue/sort filters | URL search params `?venue=&sort=` |
| Pricing inputs (Standard, Prime) | local React state — no submit |
| Add/edit court inputs (name, sport, surface, amenities checkboxes, description) | local React state — no submit |
| AI insights "Generate Summary" | local state — clicking shows the seeded mock summary string |
| `currentOwner` | exported from `lib/auth-stub.ts` |

**No Zustand needed** because nothing writes to persistent state — every form in 3a is display-only. Real writes (price updates, court CRUD, AI calls) land in Phase 3b/4.

---

## Owner login

Mirror the player login:

- Same dark-navy background (`inject_login_css` equivalent) via a one-off Tailwind background utility on the page itself
- Solid white glass card (the white-on-white fix from PR #3)
- Inputs prefilled with `owner@zpots.ai` / `owner123`
- Submit (any non-empty fields) → `router.push('/owner')`
- No real auth

---

## What's explicitly out of scope (3a)

- FastAPI scaffold and any real API call — Phase 3b
- Live AI calls (parse search, insights, court description, court image gen) — Phase 3b
- Chat widget on owner pages — Phase 3c
- Real bookings CRUD by the owner (cancel a player's booking, etc.) — Phase 4
- Real pricing updates — Phase 4 once Postgres lands
- NextAuth — Phase 4
- Mobile responsive polish beyond what Tailwind defaults give
- Replacing emoji placeholders with real photography

---

## Testing

- **Vitest** for new pure functions only. Likely 1 small helper for the heatmap color interpolation; 2–3 assertions.
- **Playwright** owner-flow E2E at `apps/web/tests/owner-flow.spec.ts`:
  - Landing → "Enter as Owner" → `/owner/login` → submit → `/owner`
  - Click each sidebar item (Dashboard / Venue Manager / Slot Control / Pricing / Bookings / AI Insights / Optimization) → assert each page renders an identifying heading
  - ~10 assertions
- Phase 2 player Playwright must stay green (we don't touch player code)
- Streamlit `pytest tests/` must stay green (we don't touch Streamlit)

---

## Success criteria

1. All 9 owner routes render without console errors
2. The owner-flow Playwright passes
3. `pnpm build` exits 0 (16+ routes after this lands)
4. Manual: log in as owner, click through every sidebar item, no broken pages
5. Streamlit at the repo root still runs unchanged (`streamlit run app.py`)

---

## Sub-project handoff order

After this merges:

1. **Phase 3b** brainstorm — FastAPI at `apps/api/`, AI helper endpoints, replace the mock summary on `/owner/insights` with a live call. Decide on Vercel/Railway deploy story for the backend.
2. **Phase 3c** brainstorm — port chat agents (`agents/player/*` and `agents/owner/*`) to FastAPI routers + add a streaming chat widget to the Next.js apps. Decide on Vercel AI SDK vs custom hook.
3. **Phase 4** — Postgres, NextAuth magic-link, deploy.

---

## Handoff

When approved, invoke `superpowers:writing-plans` to produce the Phase 3a implementation plan.
