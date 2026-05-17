# Phase 4a — Seed Data Layer Design

**Status:** approved 2026-05-17
**Sub-phase of:** Phase 4 (deploy). Sibling sub-phases: 4b Dockerfiles, 4c Cloud Run.
**Out of scope:** Postgres, NextAuth, persistence across container restarts.

## Goal

Make ZPOTS's demo data fresh-every-restart and single-source-of-truth, without a database. Seed files on disk become the only place data is defined; backend loads them into in-memory stores on startup; frontend pages fetch from new HTTP endpoints; the chat agents read from the same stores. Bookings created during a session live in memory and are lost on restart — which is the desired demo behavior.

## Motivation

Today the same data exists in three disconnected places:

1. `apps/web/lib/mock-data.ts:COURTS` (frontend hardcoded)
2. `apps/api/agents/player/tools.py:COURTS` (backend player agent hardcoded)
3. `apps/api/agents/owner/tools.py:COURTS` + `_BOOKINGS_FIXTURE` (backend owner agent hardcoded)

Plus bookings split across `apps/web/lib/booking-store.ts` (frontend Zustand with localStorage) and the owner fixture above. The split means owner-view never sees bookings the player creates in chat, and dates in fixtures grow stale (booking for "2026-06-01" is meaningless next month).

A real DB would solve this but is overkill for a demo product. A seed-file refactor solves it cheaply: one place to edit, dates resolve relative to today, all views see the same data, container restart resets to a clean demo state.

## Architecture

```
apps/api/
├── seed/
│   ├── courts.json              # 6 courts, static
│   └── bookings.json            # seed bookings with days_from_today offsets
├── data/
│   ├── __init__.py
│   ├── seed_loader.py           # pure JSON → resolved-dict functions
│   └── store.py                 # in-memory singletons + reset/init
├── routers/
│   └── data.py                  # GET /courts*, GET/POST /bookings*
├── schemas/
│   └── data.py                  # Court, Booking, CreateBookingRequest
└── main.py                      # MODIFIED — startup hook loads seed
```

Frontend pages stop importing `COURTS` from `mock-data.ts` and call `getCourts()` / `getBookings()` from a new typed client. The Zustand booking store becomes a thin cache mirroring backend state (POST through API, hydrate on mount, no localStorage persist).

Agent tools delete their hardcoded constants and read from the same stores the routes use. The `bookings` parameter is removed from player-tool signatures and from `ChatPlayerRequest` (backend already has the data).

### Single-instance caveat

In-memory storage means a Cloud Run deployment must run with `--min-instances=1 --max-instances=1` for the demo. Multi-instance deployments would see divergent state across containers. Document this in `main.py` and in the Phase 4c deploy spec.

## Components

### `seed/courts.json`

Static. Same fields the frontend already uses, plus `utilization_pct` (used only by owner agent today).

```json
[
  {
    "id": "bbc-01",
    "name": "Bangkok Badminton Center",
    "sport": "Badminton",
    "district": "Sukhumvit",
    "price_per_hour": 450,
    "rating": 4.8,
    "utilization_pct": 88
  }
]
```

Six entries mirror today's hardcoded list across the three call sites.

### `seed/bookings.json`

Date-relative. Negative offsets allowed (e.g. `-7` = a week ago) for revenue demos.

```json
[
  {
    "txn_id": "ZP-90101",
    "user_id": 1,
    "player_name": "Alex Siriwan",
    "court_id": "bbc-01",
    "days_from_today": 1,
    "time_start": "18:00",
    "duration": 2,
    "status": "CONFIRMED"
  }
]
```

`seed_loader` derives `date` (`today + days_from_today`), `time_end` (`time_start + duration`), `court_name` and `total_price` (from the court). Derived fields stay out of the seed to avoid drift.

### `data/seed_loader.py`

Pure functions, no module state.

```python
def _today() -> date: return date.today()           # indirection for test freezing

def load_courts() -> list[dict]: ...
def load_bookings(courts: list[dict]) -> list[dict]:
    # reads seed/bookings.json, joins courts, resolves derived fields
```

### `data/store.py`

Module-level singletons reset on startup and on test setup.

```python
class CourtsStore:
    def __init__(self, seed: list[dict]): ...
    def all(self) -> list[dict]: ...
    def by_id(self, court_id: str) -> dict | None: ...

class BookingsStore:
    def __init__(self, seed: list[dict]): ...
    def all(self) -> list[dict]: ...
    def for_user(self, user_id: int) -> list[dict]: ...
    def for_court(self, court_id: str) -> list[dict]: ...
    def has_conflict(self, court_id: str, date: str, time_start: str, duration: int) -> bool: ...
    def add(self, b: dict) -> dict: ...           # assigns txn_id if missing, returns full row
    def cancel(self, txn_id: str) -> dict | None: ...
    def reset(self, seed: list[dict]) -> None: ...

courts_store: CourtsStore | None = None
bookings_store: BookingsStore | None = None

def init_stores() -> None: ...                    # called on FastAPI startup
```

GIL + single-process is sufficient concurrency; no explicit locks.

### `routers/data.py`

| Method | Path | Returns | Errors |
|---|---|---|---|
| `GET` | `/courts` | `list[Court]` | — |
| `GET` | `/courts/{id}` | `Court` | 404 |
| `GET` | `/bookings?user_id=&court_id=&status=` | `list[Booking]` | — |
| `POST` | `/bookings` | `Booking` | 422 unknown court, 409 slot conflict |
| `POST` | `/bookings/{txn_id}/cancel` | `Booking` | 404 missing, 409 already cancelled |

Mounted in `main.py` alongside the existing `ai`, `ml`, `chat`, `health` routers. Startup hook calls `init_stores()`.

### `schemas/data.py`

```python
class Court(BaseModel): id, name, sport, district, price_per_hour, rating, utilization_pct
class Booking(BaseModel): txn_id, user_id, player_name, court_id, court_name,
                         date, time_start, time_end, duration, total_price, status
class CreateBookingRequest(BaseModel): user_id, court_id, date, time_start, duration,
                                       player_name | None
```

`schemas/chat.py:BookingSnapshot` is deleted; references swap to `Booking`.

### Agent refactor

**`agents/owner/tools.py`** — delete `_BOOKINGS_FIXTURE` and `COURTS`. Each tool reads from `courts_store` / `bookings_store`. `dispatch(name, args, user_id)` unchanged.

**`agents/player/tools.py`** — delete `COURTS`. Drop the `bookings` parameter from every tool and from `dispatch(name, args, user_id)`. Tools that need bookings call `bookings_store.for_user(user_id)`. `propose_booking` calls `bookings_store.has_conflict(...)`. `propose_cancel` looks up by `txn_id` in the store.

**`agents/{player,owner}/agent.py`** — `run_turn(messages, user)` drops the `bookings` param.

**`schemas/chat.py:ChatPlayerRequest`** — drop the `bookings` field.

**`routers/chat.py`** — stop passing `bookings` to `player_run_turn`.

### Frontend refactor

**`apps/web/lib/data-client.ts` (new):**

```ts
export const getCourts: () => Promise<Court[]>
export const getCourt: (id: string) => Promise<Court>
export const getBookings: (params?: {user_id?: number; court_id?: string; status?: string}) => Promise<Booking[]>
export const createBooking: (req: CreateBookingRequest) => Promise<Booking>
export const cancelBooking: (txnId: string) => Promise<Booking>
```

Mirrors `chat-client.ts` style; uses the existing `/api/[...path]` proxy.

**`apps/web/lib/mock-data.ts`** — repurposed as `FALLBACK_COURTS`. Pages use it only when `getCourts()` fails.

**`apps/web/lib/booking-store.ts`:**
- Drop the `persist` middleware (truth is backend, in-memory is fine).
- Add `hydrate()` action that calls `getBookings({user_id: currentUser.id})` and replaces local state.
- `addBookingWithTxn(draft)` calls `createBooking(...)`, then pushes the server response. Signature unchanged so callers (ChatWidget) need no edit beyond what's listed.
- `cancelBooking(txn)` calls API then mutates.

**`apps/web/components/BookingsHydrator.tsx` (new):** client component that runs `useBookingStore.getState().hydrate()` once on mount. Mounted in `app/player/layout.tsx`. The owner layout mounts an equivalent `OwnerBookingsHydrator` that hydrates whatever owner-side state exists today.

**Pages that read courts:**
- `/player/search` — replace `COURTS` import with a Server Component `await getCourts()`.
- `/player/courts/[id]`, `/player/courts/[id]/book` — `await getCourt(params.id)`.
- `/owner/venues`, `/owner/venues/[id]/edit` — same pattern.

**ChatWidget** (`components/chat/ChatWidget.tsx`) — drop the `bookings` field from the player request body.

**`lib/chat-types.ts`** — drop `BookingSnapshot` and the `bookings` field from `ChatPlayerRequest`.

## Data flow

```
Container start
   └─ FastAPI lifespan: init_stores()
       ├─ courts_store ← load_courts()
       └─ bookings_store ← load_bookings(courts)

Page load (player /search)
   └─ Server Component: await getCourts() → GET /courts
       └─ courts_store.all()

Layout mount (player)
   └─ <BookingsHydrator /> → getBookings({user_id}) → bookings_store.for_user()
       └─ useBookingStore.setState({bookings: ...})

Player chat: "book bbc-01 tomorrow 6pm"
   └─ POST /chat/player {messages, user}
       └─ player_run_turn → propose_booking tool
           └─ bookings_store.has_conflict() check, returns draft
   └─ ChatWidget: user clicks Confirm
       └─ createBooking() → POST /bookings
           ├─ bookings_store.add()
           └─ ChatWidget pushes returned booking into useBookingStore

Owner chat: "list bookings today"
   └─ POST /chat/owner → owner agent → bookings_store.all()
       (sees everything, including the booking the player just made)
```

## Testing

Backend (new):
| Suite | Count |
|---|---|
| `tests/test_seed_loader.py` | 4 (date math, time_end derivation, court hydration, error on missing court) |
| `tests/test_store.py` | 6 (filter by user/court/status, add returns row, cancel marks status, conflict detection, reset idempotency) |
| `tests/test_data_routes.py` | 6 (each endpoint happy path + 404/409 paths) |

Backend (rewritten):
| Suite | Count |
|---|---|
| `tests/test_player_tools.py` | 8 (no `bookings` arg; store seeded via fixture) |
| `tests/test_owner_tools.py` | 8 (reads from store, not module fixture) |
| `tests/test_player_agent.py` | 3 (drop `bookings` param) |
| `tests/test_owner_agent.py` | 2 (unchanged interface) |
| `tests/test_chat_routes.py` | 2 (drop `bookings` from player request body) |

Expected post-4a pytest total: ~45 (was 32 in Phase 3c). Health/ai/ml routes unchanged.

Frontend (new):
- Vitest: 2-3 tests for `data-client.ts` (fetch + fallback) and `BookingsHydrator` (calls hydrate once).
- Playwright: no new tests; the existing player-flow and owner-flow specs should still pass with FastAPI running and stores seeded.

**Test fixtures.** `apps/api/conftest.py` adds an autouse fixture that:
1. Monkeypatches `seed_loader._today()` to return a frozen date.
2. Calls `store.init_stores()` then `bookings_store.reset(seed)` with a deterministic, smaller test dataset.

## Error handling

**Backend:**
- Seed file missing or invalid JSON → startup fails with a clear traceback (preferred over silently serving nothing).
- `POST /bookings` with unknown `court_id` → 422 with field error.
- Slot conflict → 409 `{detail: "Slot is not available"}`.
- `POST /bookings/{txn}/cancel` on missing → 404; on already-cancelled → 409.

**Frontend:**
- `getCourts()` fails → page uses `FALLBACK_COURTS` and shows a small "demo data" eyebrow (Phase 3b precedent).
- `createBooking()` fails (409, network) → `ConfirmDraft` surfaces the message; nothing pushed to cache; user stays on draft.
- `BookingsHydrator` fails → cache stays empty; pages render empty state instead of crashing.

## Out of scope (defer to later sub-phases or never)

- Postgres, migrations, Alembic
- NextAuth (sessions, real users) → Phase 4 sub-phase TBD
- Persistence across container restarts
- Multi-instance consistency (Cloud Run must run min=1 max=1 for demo)
- Streamlit migration to the new data layer — Streamlit keeps its own SQLite path untouched
- Dockerfiles → Phase 4b
- Cloud Run deploy → Phase 4c
- CSV/Sheets editor experience (JSON only)

## Open questions

None. All resolved during brainstorming.
