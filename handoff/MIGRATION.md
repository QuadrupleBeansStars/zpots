# ZPOTS Migration: Streamlit → Next.js + FastAPI

This document maps your **current Streamlit codebase** (`QuadrupleBeansStars/zpots@main`) onto a production **Next.js 14 + FastAPI** architecture, using the design system in `/design-system/`.

---

## Target architecture

```
┌─────────────────────────────────────────────────────┐
│  Browser (Next.js 14 App Router, TypeScript, Tailwind)│
│  • Player app routes     /(player)/*                │
│  • Owner console routes  /(owner)/*                 │
│  • Marketing / landing   /                          │
└──────────────┬──────────────────────────────────────┘
               │  REST (fetch) + NextAuth session
               ▼
┌─────────────────────────────────────────────────────┐
│  FastAPI (Python 3.11)                              │
│  • /api/courts, /api/bookings, /api/insights/*      │
│  • Gemini helpers (utils/gemini.py — reused as-is)  │
│  • Pydantic schemas mirroring data/dummy_data.py    │
└──────────────┬──────────────────────────────────────┘
               │  SQLAlchemy
               ▼
┌─────────────────────────────────────────────────────┐
│  Postgres (Supabase / Neon / Railway)               │
└─────────────────────────────────────────────────────┘
```

---

## What maps to what

### Streamlit page → Next.js route

| Streamlit file | Next.js route | Priority |
|---|---|---|
| `app.py` landing | `app/page.tsx` | ★★★ |
| `pages/player/login.py` | `app/(player)/login/page.tsx` | ★★★ |
| `pages/player/home.py` | `app/(player)/page.tsx` | ★★★ |
| `pages/player/search.py` | `app/(player)/search/page.tsx` | ★★★ |
| `pages/player/court_details.py` | `app/(player)/courts/[id]/page.tsx` | ★★★ |
| `pages/player/booking.py` | `app/(player)/courts/[id]/book/page.tsx` | ★★ |
| `pages/player/confirmation.py` | `app/(player)/bookings/[id]/confirmation/page.tsx` | ★★ |
| `pages/player/my_bookings.py` | `app/(player)/bookings/page.tsx` | ★★ |
| `pages/player/checkin.py` | `app/(player)/bookings/[id]/checkin/page.tsx` | ★ |
| `pages/player/feedback.py` | `app/(player)/bookings/[id]/feedback/page.tsx` | ★ |
| `pages/owner/login.py` | `app/(owner)/login/page.tsx` | ★★★ |
| `pages/owner/dashboard.py` | `app/(owner)/page.tsx` | ★★★ |
| `pages/owner/manage_courts.py` | `app/(owner)/venues/page.tsx` | ★★ |
| `pages/owner/add_edit_court.py` | `app/(owner)/venues/[id]/edit/page.tsx` | ★★ |
| `pages/owner/manage_slots.py` | `app/(owner)/slots/page.tsx` | ★★ |
| `pages/owner/pricing.py` | `app/(owner)/pricing/page.tsx` | ★★ |
| `pages/owner/booking_dashboard.py` | `app/(owner)/bookings/page.tsx` | ★★ |
| `pages/owner/ai_insights.py` | `app/(owner)/insights/page.tsx` | ★★★ |
| `pages/owner/optimization.py` | `app/(owner)/optimization/page.tsx` | ★ |

### Streamlit component → React component

| `components/` (Python) | `components/` (React) |
|---|---|
| `components/css.py` → `inject_global_css()` | `app/globals.css` + `tailwind.config.ts` |
| `components/nav.py` → `render_player_topbar()` | `components/PlayerTopBar.tsx` |
| `components/nav.py` → `render_owner_sidebar()` | `components/OwnerSidebar.tsx` |
| `components/cards.py` → `court_card()` | `components/CourtCard.tsx` |
| `components/cards.py` → `kpi_card()` | `components/KpiCard.tsx` |
| `components/charts.py` → Plotly charts | `components/charts/*.tsx` (Recharts or Plotly.js) |

### Data → API

| `data/dummy_data.py` | Backend equivalent |
|---|---|
| `COURTS` (list) | `GET /api/courts`, `GET /api/courts/{id}` — Postgres `courts` table |
| `get_time_slots(court_id)` | `GET /api/courts/{id}/slots?date=YYYY-MM-DD` |
| `PLAYER_BOOKINGS` | `GET /api/me/bookings`, `POST /api/bookings` |
| `OWNER_VENUES` | `GET /api/owner/venues` |
| `OWNER_BOOKINGS`, `TODAYS_BOOKINGS` | `GET /api/owner/bookings` |
| `WEEKLY_UTILIZATION`, `DISTRICT_DEMAND` | `GET /api/owner/analytics` |
| `SLOT_CALENDAR` | `GET /api/owner/calendar?week=YYYY-WW` |

### AI helpers (keep as-is)

`utils/gemini.py` works unchanged inside FastAPI — just move `st.secrets["GEMINI_API_KEY"]` to `os.environ["GEMINI_API_KEY"]`. Expose each function as an endpoint:

| Function | Endpoint |
|---|---|
| `parse_search_query(q)` | `POST /api/ai/parse-search` |
| `generate_ai_insights(...)` | `POST /api/ai/insights` |
| `generate_court_description(...)` | `POST /api/ai/court-description` |
| `chat_with_court_assistant(...)` | `POST /api/ai/chat` |

---

## State management

Streamlit uses `st.session_state` heavily (`page`, `flow`, `selected_court_id`, `nl_filters`, etc.). In the React app:

| Streamlit state | React equivalent |
|---|---|
| `st.session_state.page` | Next.js route / URL |
| `st.session_state.flow` | URL segment `(player)` vs `(owner)` |
| `st.session_state.selected_court_id` | URL param `[id]` |
| `st.session_state.nl_filters` | URL search params `?sport=...&district=...` |
| `st.session_state.logged_in` | NextAuth session |
| `st.session_state.ai_insights_text` | TanStack Query cache, keyed by venue |

**Rule of thumb:** if it needs to survive a refresh or be linkable, put it in the URL. Use React state only for ephemeral UI (modal open, form typing).

---

## Phase plan (4 weeks, solo)

### Phase 1 — Scaffold & design system (days 1–3)
- [ ] `pnpm create next-app zpots-web --typescript --tailwind --app`
- [ ] Copy `design-system/shared.css` → `app/globals.css`
- [ ] Copy `design-system/tailwind.config.ts` → project root
- [ ] Copy `components/` from this handoff into `components/`
- [ ] Wire fonts (Space Grotesk, Inter, Lexend, Material Symbols Rounded)
- [ ] Confirm the landing page renders

### Phase 2 — Read-only player flows (days 4–8)
- [ ] Home, Search (natural-language bar goes to a local stub), Court details
- [ ] Mock data layer in `lib/mock-data.ts` (copy `data/dummy_data.py` values)
- [ ] Booking summary + flow (no payment yet)
- [ ] Success screen + QR (`npm i qrcode.react`)

### Phase 3 — Owner console + AI (days 9–14)
- [ ] Owner dashboard (KPIs + bar chart via Recharts)
- [ ] AI insights page (hit backend, show markdown with `react-markdown`)
- [ ] Pricing page, slot calendar
- [ ] Stand up FastAPI; replace mock data with live endpoints
- [ ] Wire Gemini endpoints

### Phase 4 — Data, auth, polish (days 15–21)
- [ ] Migrate `COURTS` and related tables to Postgres
- [ ] NextAuth with email + Google
- [ ] Replace emoji placeholders with real photography
- [ ] Lighthouse + a11y pass
- [ ] Vercel deploy (frontend) + Railway/Fly deploy (backend)

---

## Gotchas from your current code

1. **`utils/gemini.py` imports `streamlit`** just to read `st.secrets`. Swap for `os.getenv("GEMINI_API_KEY")` — nothing else in that file is Streamlit-specific, so it ports cleanly.
2. **Gemini model name** `"gemini-3-flash-preview"` isn't a real model ID — this will fail at runtime. Use `"gemini-2.5-flash"` or the current stable model. Worth fixing in both places before porting.
3. **Plotly charts** (`components/charts.py`) re-render on every Streamlit rerun. In React use Recharts (lighter, better tree-shake) unless you specifically need Plotly's interactivity. Kit screens assume the simpler Recharts approach.
4. **QR codes** (`pages/player/checkin.py` uses `qrcode` + Pillow) — replace with `qrcode.react` (client-side, no server needed).
5. **`components/css.py` is huge** (9KB of injected CSS). Don't port it line-for-line — everything useful is already captured in `design-system/shared.css` + the Tailwind config. Delete on migration.
6. **`st.rerun()` everywhere** — these become Next.js route pushes or React state setters. There is no direct equivalent; don't try to emulate.

---

## What's in this handoff

```
handoff/
├── MIGRATION.md            ← you are here
├── CLAUDE.md               ← brief for Claude Code in your local repo
├── design-system/
│   ├── shared.css          ← tokens, buttons, cards, status badges
│   ├── tailwind.config.ts  ← ZPOTS tokens as Tailwind theme
│   └── tokens.md           ← human-readable reference
├── components/             ← React components (TSX) ready to drop in
│   ├── player/
│   └── owner/
├── screens/                ← reference implementations of full pages
│   ├── PlayerHome.tsx
│   ├── PlayerSearch.tsx
│   ├── CourtDetails.tsx
│   ├── OwnerDashboard.tsx
│   └── OwnerAIInsights.tsx
├── backend/
│   ├── main.py             ← FastAPI skeleton
│   ├── schemas.py          ← Pydantic models mirroring your data shapes
│   ├── ai.py               ← your gemini.py, de-Streamlit'd
│   └── requirements.txt
└── assets/                 ← bolt glyph, wordmark, placeholders
```
