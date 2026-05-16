# Phase 2 — Player Flows (Read-Only) Design

**Date:** 2026-05-16
**Status:** Approved
**Base spec:** `docs/superpowers/specs/2026-05-16-nextjs-migration-design.md`
**Phase position:** 2 of 4 (Phase 1 scaffold + landing merged in PR #5)

---

## Goal

Build all 8 player-side pages in `apps/web/` using a mock data layer that mirrors the shape of `data/database.py`. Booking flow is fully clickable end-to-end and persists to browser storage so "My Bookings" reflects what the user just booked. No real backend yet — that's Phase 3+4.

---

## Architecture

```
apps/web/app/(player)/
├── layout.tsx                                    # PlayerTopBar + main container
├── login/page.tsx                                # form UI only, hardcoded redirect to /player
├── page.tsx                                      # home — hero + sport row + featured + explainer
├── search/page.tsx                               # filters via URL params, court grid
├── courts/[id]/
│   ├── page.tsx                                  # court details — hero/amenities/slot grid/summary
│   └── book/page.tsx                             # booking form — date/slot/duration/payment
└── bookings/
    ├── page.tsx                                  # my bookings — merged seeded + localStorage
    └── [txnId]/
        ├── confirmation/page.tsx                 # success screen, writes booking to store
        ├── checkin/page.tsx                      # QR code + booking details
        └── feedback/page.tsx                     # star rating + tags + textarea
```

```
apps/web/lib/
├── mock-data.ts        # COURTS, seeded bookings, getCourt(id), getSlots(courtId, date)
├── booking-store.ts    # Zustand store, localStorage-persisted
├── auth-stub.ts        # hardcoded currentUser (deleted in Phase 4)
└── format.ts           # ฿ price, date, time helpers
```

```
apps/web/components/         # shared (some Phase 1, some new in Phase 2)
├── (Phase 1) Button, Icon, CourtCard, KpiCard, PlayerTopBar, Tags, types
└── player/                  # NEW — page-local components extracted to keep page files focused
    ├── SlotGrid.tsx
    ├── BookingSummaryCard.tsx
    ├── StarRating.tsx
    └── FeedbackTagPicker.tsx
```

---

## Route map (Streamlit → Next.js)

| Streamlit page | Next.js route | Notes |
|---|---|---|
| `pages/player/login.py` | `app/(player)/login/page.tsx` | Form UI only; submit redirects to `/player` |
| `pages/player/home.py` | `app/(player)/page.tsx` | Hero, sport row (Badminton/Football/Basketball/Tennis/Volleyball/Padel), featured courts grid, 3-step explainer |
| `pages/player/search.py` | `app/(player)/search/page.tsx` | Filters in URL search params (`?sport=Badminton&district=Sukhumvit&max_price=500`), court grid below |
| `pages/player/court_details.py` | `app/(player)/courts/[id]/page.tsx` | Hero + responsive amenities grid (the bug we just fixed) + date/duration controls + slot grid + booking summary side panel |
| `pages/player/booking.py` | `app/(player)/courts/[id]/book/page.tsx` | Read draft from URL (`?date=&time_start=&duration=`), summary, payment method radio (UI only) |
| `pages/player/confirmation.py` | `app/(player)/bookings/[txnId]/confirmation/page.tsx` | On mount: writes booking to Zustand store. Shows success screen + txn id + share buttons |
| `pages/player/my_bookings.py` | `app/(player)/bookings/page.tsx` | Reads merged set (seeded mock bookings + store), tabs for All / Past |
| `pages/player/checkin.py` | `app/(player)/bookings/[txnId]/checkin/page.tsx` | QR (via `qrcode.react`) + booking details + venue address |
| `pages/player/feedback.py` | `app/(player)/bookings/[txnId]/feedback/page.tsx` | 5-star rating + tag chips + textarea; submit logs to console (real submit Phase 4) |

---

## Data shapes

Mirror `data/database.py`'s `bookings` table so Phase 4 swap to the API is mechanical.

```ts
// apps/web/lib/types.ts (new) — re-exports + adds Booking
export type Court = { /* from handoff types.ts, unchanged */ };

export type Booking = {
  id: number;
  txn_id: string;          // e.g. "ZP-12345"
  court_id: string;
  court_name: string;
  date: string;            // YYYY-MM-DD
  time_start: string;      // HH:00
  time_end: string;        // HH:00
  duration: number;        // hours
  total_price: number;     // THB
  status: 'CONFIRMED' | 'CANCELLED';
  created_at: string;      // ISO
};

export type BookingDraft = Omit<Booking, 'id' | 'txn_id' | 'status' | 'created_at'>;
```

---

## State management

| State | Where it lives | Why |
|---|---|---|
| Court list, court detail | `lib/mock-data.ts` (static) | Read-only seed data |
| Slot availability | `lib/mock-data.ts:getSlots(id, date)` (deterministic mock) | Derives "booked slots" from any bookings in the Zustand store |
| User bookings | Zustand store, persisted to localStorage under `zpots.bookings.v1` | Survives refresh, survives navigation |
| Current user | `lib/auth-stub.ts` exports `{ id: 1, name: "Alex Siriwan", email: "player@zpots.ai" }` | Avoids prop-drilling; deleted in Phase 4 |
| Search filters | URL search params | Linkable, shareable, survives back/forward |
| Booking-form selection (date, slot, duration) | URL search params on the court-details page | Linkable; passed to /book route as query string |
| Feedback form (stars, tags, text) | Local React state | Submitted to console, no persistence |

---

## What gets reused from Phase 1

- `apps/web/components/Button.tsx` — primary CTA
- `apps/web/components/Icon.tsx` — Material Symbols
- `apps/web/components/CourtCard.tsx` — used on home (featured) + search (grid)
- `apps/web/components/KpiCard.tsx` — used on home + court details
- `apps/web/components/PlayerTopBar.tsx` — wired into `(player)/layout.tsx`
- `apps/web/components/Tags.tsx` — AITag, StatusBadge, Chip, Eyebrow
- Design system classes (`zpots-card`, `ai-tag`, `btn-primary`, status pills) — already in globals.css
- `font-display` / `font-sans` / `text-zpots-*` Tailwind utilities

---

## New dependencies

- `zustand` — booking store
- `qrcode.react` — check-in page

That's it. No react-hook-form, no Recharts (player pages don't have charts), no NextAuth yet, no react-query yet (mock data is sync).

---

## Out of scope

- Real auth — landing → /player just navigates; the login page form does nothing functional (Phase 4)
- Owner pages (Phase 3)
- Chat widget (Phase 3)
- AI search-query parsing on `/search` — Phase 3 when the AI endpoint exists
- Real payment processing — booking flow has payment-method UI but doesn't process
- Cancel-from-my-bookings — needs real API (Phase 4)
- Server-side mock writes via Next.js Route Handlers — would be thrown out in Phase 3 when FastAPI lands
- AI Insights, Optimization (owner-only) — Phase 3
- Per-page Playwright tests — only one critical-path E2E test in Phase 2

---

## Testing

Single Playwright test exercising the critical path end-to-end:

```
landing → "Enter as Player" → /player → click "Search" → filter sport=Badminton
  → click a Bangkok Badminton court → pick a date → pick a slot → choose 1 hr
  → click "Proceed to booking" → see /book → click "Confirm & Pay"
  → see /bookings/.../confirmation → click "View My Bookings"
  → /bookings → assert the new booking appears in the list
```

~10 assertions. Lives at `apps/web/tests/player-flow.spec.ts`. Per-page detail tests are out of scope for this phase — Phase 4 will add an a11y/Lighthouse pass.

---

## Success criteria

1. All 8 routes render without console errors
2. The critical-path Playwright test passes
3. Manual smoke: book a court, confirm, navigate to "My Bookings", see the new booking; refresh the page, booking still there
4. `pnpm build` exits 0
5. The legacy Streamlit at the repo root still runs unchanged (`streamlit run app.py`)

---

## Handoff

When this design is approved, invoke `superpowers:writing-plans` to produce the Phase 2 implementation plan. Phase 3 (owner + chat + FastAPI) gets its own brainstorm cycle after Phase 2 merges.
