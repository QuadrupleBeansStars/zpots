# Phase 4a — Seed Data Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the three hardcoded copies of courts + bookings data with a single seed-file source that the backend loads into in-memory stores on startup, exposes via HTTP, and the frontend fetches at runtime.

**Architecture:** `apps/api/seed/*.json` → `data/seed_loader.py` (pure) → `data/store.py` (singletons) → `routers/data.py` (GET/POST) → consumed by both agent tools and the frontend's `data-client.ts`. Date-relative seed (`days_from_today: 1`) keeps demos fresh. State is in-memory; container restart resets to clean seed.

**Tech Stack:** Python 3.11 · FastAPI · Pydantic v2 · pytest · Next.js 16 · TypeScript · Zustand (existing)

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase4a-seed-data-layer-design.md`
**Branch:** create `feat/nextjs-phase4a` off main

---

## File structure (end of Phase 4a)

```
apps/api/
├── seed/                             # NEW
│   ├── courts.json
│   └── bookings.json
├── data/                             # NEW
│   ├── __init__.py
│   ├── seed_loader.py
│   └── store.py
├── schemas/
│   └── data.py                       # NEW (Court, Booking, CreateBookingRequest)
├── routers/
│   └── data.py                       # NEW
├── agents/owner/tools.py             # MODIFIED — drop fixtures, use stores
├── agents/player/tools.py            # MODIFIED — drop COURTS, drop bookings param
├── agents/player/agent.py            # MODIFIED — drop bookings param
├── schemas/chat.py                   # MODIFIED — drop BookingSnapshot, drop bookings field
├── routers/chat.py                   # MODIFIED — drop bookings passing
├── main.py                           # MODIFIED — startup hook → init_stores()
├── conftest.py                       # MODIFIED — autouse store-reset + frozen date
└── tests/                            # NEW + REWRITTEN
    ├── test_seed_loader.py
    ├── test_store.py
    ├── test_data_routes.py
    ├── test_player_tools.py          # REWRITTEN
    ├── test_owner_tools.py           # REWRITTEN
    ├── test_player_agent.py          # MODIFIED — drop bookings param
    └── test_chat_routes.py           # MODIFIED — drop bookings field

apps/web/
├── lib/
│   ├── data-client.ts                # NEW
│   ├── mock-data.ts                  # MODIFIED — FALLBACK_COURTS + drop SEEDED_BOOKINGS, keep helpers
│   ├── booking-store.ts              # MODIFIED — drop persist, add hydrate, POST via API
│   └── chat-types.ts                 # MODIFIED — drop BookingSnapshot, drop bookings field
├── components/
│   └── BookingsHydrator.tsx          # NEW
├── components/chat/ChatWidget.tsx    # MODIFIED — drop bookings from request
└── app/
    ├── player/layout.tsx             # MODIFIED — mount BookingsHydrator
    ├── owner/layout.tsx              # MODIFIED — mount BookingsHydrator
    ├── player/search/page.tsx        # MODIFIED — getCourts
    ├── player/courts/[id]/page.tsx   # MODIFIED — getCourt
    ├── player/courts/[id]/book/page.tsx  # MODIFIED — getCourt
    ├── owner/venues/page.tsx         # MODIFIED — getCourts
    └── owner/venues/[id]/edit/page.tsx   # MODIFIED — getCourt
```

---

## Task 0: Branch + scratch verification

- [ ] **Step 1: Cut a new branch off main.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS && git checkout main && git pull && git checkout -b feat/nextjs-phase4a
```

- [ ] **Step 2: Sanity-check the existing test count baseline.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest -q
```

Expected: **32 passed** (Phase 3c baseline). Anything else means a prior phase broke something — stop and report.

---

## Task 1: Create `seed/courts.json`

**Files:**
- Create: `apps/api/seed/courts.json`

The frontend `Court` type is rich (amenities, sub-courts, color, etc.). Put the **full** shape in the seed file so a single `/courts` response can drive both frontend pages and backend agent tools (the latter ignore the extra fields).

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/seed/courts.json`** with the 6 courts. Copy each entry verbatim from `apps/web/lib/mock-data.ts:COURTS` (lines 3-169 in the existing file) and add the `utilization_pct` field that the owner agent needs:

```json
[
  {
    "id": "bbc-01",
    "name": "Bangkok Badminton Center",
    "short_name": "Bangkok Badminton",
    "sport": "Badminton",
    "rating": 4.8,
    "reviews": 100,
    "location": "Pathum Wan, Bangkok 10330, Thailand",
    "address": "88 Ratchadapisek Rd.",
    "district": "Sukhumvit",
    "price_per_hour": 450,
    "prime_price": 650,
    "amenities": [
      { "icon": "ac_unit", "label": "Climate", "value": "Full AC" },
      { "icon": "local_parking", "label": "Parking", "value": "Free (50+ Slots)" },
      { "icon": "checkroom", "label": "Facilities", "value": "Changing Rooms" },
      { "icon": "water_drop", "label": "Water", "value": "Dispenser" }
    ],
    "surface": "Premium Synthetic",
    "status": "ACTIVE",
    "utilization": 88,
    "utilization_pct": 88,
    "peak_hours": "17:00-22:00",
    "ai_efficiency": "Elite",
    "tags": ["AI RECOMMENDED"],
    "color": "#1a3a2a",
    "courts": [
      { "number": "01", "surface": "Premium Synthetic" },
      { "number": "02", "surface": "Standard Wood" }
    ]
  },
  {
    "id": "sky-02",
    "name": "Skyline Arena Football",
    "short_name": "Skyline Arena",
    "sport": "Football",
    "rating": 4.7,
    "reviews": 85,
    "location": "Thonglor District",
    "address": "42 Thonglor Soi 15",
    "district": "Thong Lor",
    "price_per_hour": 1200,
    "prime_price": 1800,
    "amenities": [
      { "icon": "ac_unit", "label": "Climate", "value": "Open Air" },
      { "icon": "local_parking", "label": "Parking", "value": "20 Slots" },
      { "icon": "checkroom", "label": "Facilities", "value": "Locker Rooms" },
      { "icon": "water_drop", "label": "Water", "value": "Dispenser" }
    ],
    "surface": "Artificial Turf",
    "status": "ACTIVE",
    "utilization": 74,
    "utilization_pct": 74,
    "peak_hours": "18:00-22:00",
    "ai_efficiency": "High",
    "tags": [],
    "color": "#1c2526",
    "courts": [{ "number": "01", "surface": "Artificial Turf" }]
  },
  {
    "id": "dwh-03",
    "name": "Downtown Hoops",
    "short_name": "Downtown Hoops",
    "sport": "Basketball",
    "rating": 4.5,
    "reviews": 62,
    "location": "Ari Soi 4",
    "address": "Ari Soi 4",
    "district": "Ari",
    "price_per_hour": 600,
    "prime_price": 800,
    "amenities": [
      { "icon": "ac_unit", "label": "Climate", "value": "Indoor AC" },
      { "icon": "local_parking", "label": "Parking", "value": "Street" },
      { "icon": "checkroom", "label": "Facilities", "value": "Showers" },
      { "icon": "water_drop", "label": "Water", "value": "Dispenser" }
    ],
    "surface": "Hardwood",
    "status": "ACTIVE",
    "utilization": 68,
    "utilization_pct": 68,
    "peak_hours": "17:00-21:00",
    "ai_efficiency": "High",
    "tags": [],
    "color": "#3a1f1f",
    "courts": [{ "number": "01", "surface": "Hardwood" }]
  },
  {
    "id": "pdl-04",
    "name": "Padel House Sukhumvit",
    "short_name": "Padel House",
    "sport": "Padel",
    "rating": 4.2,
    "reviews": 41,
    "location": "Sukhumvit Soi 39",
    "address": "Sukhumvit Soi 39",
    "district": "Sukhumvit",
    "price_per_hour": 800,
    "prime_price": 1100,
    "amenities": [
      { "icon": "ac_unit", "label": "Climate", "value": "Open Air" },
      { "icon": "local_parking", "label": "Parking", "value": "15 Slots" },
      { "icon": "checkroom", "label": "Facilities", "value": "Lounge" },
      { "icon": "water_drop", "label": "Water", "value": "Cafe" }
    ],
    "surface": "Glass Panels",
    "status": "ACTIVE",
    "utilization": 79,
    "utilization_pct": 79,
    "peak_hours": "18:00-22:00",
    "ai_efficiency": "Moderate",
    "tags": [],
    "color": "#2a3a1f",
    "courts": [{ "number": "01", "surface": "Glass Panels" }]
  },
  {
    "id": "rbs-05",
    "name": "Royal Bangkok Sports Club",
    "short_name": "Royal Bangkok",
    "sport": "Tennis",
    "rating": 5.0,
    "reviews": 120,
    "location": "Pathumwan",
    "address": "Henri Dunant Rd",
    "district": "Pathumwan",
    "price_per_hour": 950,
    "prime_price": 1400,
    "amenities": [
      { "icon": "ac_unit", "label": "Climate", "value": "Open Air" },
      { "icon": "local_parking", "label": "Parking", "value": "Valet" },
      { "icon": "checkroom", "label": "Facilities", "value": "Premium Lounge" },
      { "icon": "water_drop", "label": "Water", "value": "Bar" }
    ],
    "surface": "Clay",
    "status": "ACTIVE",
    "utilization": 92,
    "utilization_pct": 92,
    "peak_hours": "16:00-20:00",
    "ai_efficiency": "Elite",
    "tags": ["MEMBERS ONLY"],
    "color": "#1a3030",
    "courts": [{ "number": "01", "surface": "Clay" }]
  },
  {
    "id": "ivh-06",
    "name": "Impact Volleyball Hall",
    "short_name": "Impact Volleyball",
    "sport": "Volleyball",
    "rating": 4.8,
    "reviews": 33,
    "location": "Muang Thong Thani",
    "address": "Muang Thong Thani",
    "district": "Nonthaburi",
    "price_per_hour": 350,
    "prime_price": 500,
    "amenities": [
      { "icon": "ac_unit", "label": "Climate", "value": "Full AC" },
      { "icon": "local_parking", "label": "Parking", "value": "Free" },
      { "icon": "checkroom", "label": "Facilities", "value": "Locker Rooms" },
      { "icon": "water_drop", "label": "Water", "value": "Dispenser" }
    ],
    "surface": "Sprung Floor",
    "status": "ACTIVE",
    "utilization": 55,
    "utilization_pct": 55,
    "peak_hours": "19:00-22:00",
    "ai_efficiency": "High",
    "tags": [],
    "color": "#1f1f3a",
    "courts": [{ "number": "01", "surface": "Sprung Floor" }]
  }
]
```

- [ ] **Step 2: Validate JSON parses.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS && python -c "import json; json.load(open('apps/api/seed/courts.json')); print('ok')"
```

Expected: `ok`

- [ ] **Step 3: Commit.**

```bash
git add apps/api/seed/courts.json
git commit -m "feat(api): seed/courts.json (single source of truth for 6 courts)"
```

---

## Task 2: Create `seed/bookings.json`

**Files:**
- Create: `apps/api/seed/bookings.json`

Combine the 6 entries from `apps/api/agents/owner/tools.py:_BOOKINGS_FIXTURE` (lines 31-50) plus the 2 entries from `apps/web/lib/mock-data.ts:SEEDED_BOOKINGS` (lines 171-198, rewritten with offsets). All use `days_from_today` so dates always feel current.

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/seed/bookings.json`:**

```json
[
  {
    "txn_id": "ZP-90100",
    "user_id": 2,
    "player_name": "Marcus Lee",
    "court_id": "bbc-01",
    "days_from_today": 0,
    "time_start": "20:00",
    "duration": 1,
    "status": "CONFIRMED"
  },
  {
    "txn_id": "ZP-90101",
    "user_id": 1,
    "player_name": "Alex Siriwan",
    "court_id": "bbc-01",
    "days_from_today": 1,
    "time_start": "18:00",
    "duration": 2,
    "status": "CONFIRMED"
  },
  {
    "txn_id": "ZP-90102",
    "user_id": 2,
    "player_name": "Narin Kositchai",
    "court_id": "sky-02",
    "days_from_today": 2,
    "time_start": "20:00",
    "duration": 2,
    "status": "CONFIRMED"
  },
  {
    "txn_id": "ZP-90103",
    "user_id": 3,
    "player_name": "Maya Chen",
    "court_id": "pdl-04",
    "days_from_today": 3,
    "time_start": "07:00",
    "duration": 1,
    "status": "CONFIRMED"
  },
  {
    "txn_id": "ZP-90104",
    "user_id": 4,
    "player_name": "Tomás Vega",
    "court_id": "dwh-03",
    "days_from_today": 4,
    "time_start": "19:00",
    "duration": 2,
    "status": "CONFIRMED"
  },
  {
    "txn_id": "ZP-90105",
    "user_id": 5,
    "player_name": "Priya Singh",
    "court_id": "rbs-05",
    "days_from_today": 5,
    "time_start": "16:00",
    "duration": 1,
    "status": "CONFIRMED"
  },
  {
    "txn_id": "ZP-90001",
    "user_id": 1,
    "player_name": "Alex Siriwan",
    "court_id": "bbc-01",
    "days_from_today": -3,
    "time_start": "18:00",
    "duration": 2,
    "status": "CONFIRMED"
  },
  {
    "txn_id": "ZP-90002",
    "user_id": 1,
    "player_name": "Alex Siriwan",
    "court_id": "pdl-04",
    "days_from_today": 2,
    "time_start": "07:00",
    "duration": 1,
    "status": "CONFIRMED"
  }
]
```

Note: `user_id: 1` is the stub player (Alex Siriwan, who currently logs in via `auth-stub.ts`). The two trailing entries replace the old frontend SEEDED_BOOKINGS so the player's "My bookings" page shows something at session start.

- [ ] **Step 2: Validate JSON parses.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS && python -c "import json; json.load(open('apps/api/seed/bookings.json')); print('ok')"
```

- [ ] **Step 3: Commit.**

```bash
git add apps/api/seed/bookings.json
git commit -m "feat(api): seed/bookings.json (relative-date offsets, demo always fresh)"
```

---

## Task 3: `seed_loader.py` (TDD)

**Files:**
- Create: `apps/api/data/__init__.py` (empty)
- Create: `apps/api/data/seed_loader.py`
- Create: `apps/api/tests/test_seed_loader.py`

- [ ] **Step 1: Create the empty package marker.**

```bash
touch /Users/nchawanp/Desktop/ZPOTS/apps/api/data/__init__.py
```

- [ ] **Step 2: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_seed_loader.py`:

```python
from datetime import date

import pytest

from data import seed_loader


@pytest.fixture
def frozen_today(monkeypatch):
    monkeypatch.setattr(seed_loader, "_today", lambda: date(2099, 1, 1))


def test_load_courts_returns_six_with_required_fields():
    courts = seed_loader.load_courts()
    assert len(courts) == 6
    for c in courts:
        assert {"id", "name", "sport", "district", "price_per_hour", "utilization_pct"} <= set(c.keys())


def test_load_bookings_resolves_date_from_offset(frozen_today):
    courts = seed_loader.load_courts()
    rows = seed_loader.load_bookings(courts)
    # today=2099-01-01; days_from_today=1 entry should resolve to 2099-01-02
    today_plus_one = [r for r in rows if r["date"] == "2099-01-02"]
    assert len(today_plus_one) >= 1


def test_load_bookings_derives_time_end_and_court_name_and_total_price(frozen_today):
    courts = seed_loader.load_courts()
    rows = seed_loader.load_bookings(courts)
    alex = next(r for r in rows if r["txn_id"] == "ZP-90101")
    assert alex["time_end"] == "20:00"               # 18:00 + 2h
    assert alex["court_name"] == "Bangkok Badminton Center"
    assert alex["total_price"] == 900                # 450 * 2
    assert alex["date"] == "2099-01-02"


def test_load_bookings_raises_on_unknown_court():
    courts = [{"id": "only-this-court", "name": "X", "price_per_hour": 100}]
    with pytest.raises(KeyError):
        seed_loader.load_bookings(courts)
```

- [ ] **Step 3: Run, expect ImportError.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_seed_loader.py -v
```

Expected: ImportError or ModuleNotFoundError.

- [ ] **Step 4: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/data/seed_loader.py`:**

```python
"""Pure functions that load JSON seed files and resolve derived fields.

`_today()` is an indirection so tests can freeze the date with monkeypatch.
"""
import json
from datetime import date, timedelta
from pathlib import Path

_SEED_DIR = Path(__file__).resolve().parent.parent / "seed"


def _today() -> date:
    return date.today()


def load_courts() -> list[dict]:
    """Read seed/courts.json. Returns the rows verbatim (no transformation)."""
    return json.loads((_SEED_DIR / "courts.json").read_text())


def load_bookings(courts: list[dict]) -> list[dict]:
    """Read seed/bookings.json and resolve derived fields.

    Adds: date (today + days_from_today), time_end (time_start + duration),
    court_name and total_price (looked up from `courts`).

    Raises KeyError if a booking references a court_id not in `courts`.
    """
    by_id = {c["id"]: c for c in courts}
    raw = json.loads((_SEED_DIR / "bookings.json").read_text())
    today = _today()
    out: list[dict] = []
    for b in raw:
        court_id = b["court_id"]
        if court_id not in by_id:
            raise KeyError(f"seed/bookings.json references unknown court_id={court_id}")
        court = by_id[court_id]
        d = today + timedelta(days=int(b["days_from_today"]))
        start_h = int(b["time_start"].split(":")[0])
        duration = int(b["duration"])
        out.append({
            "txn_id": b["txn_id"],
            "user_id": int(b["user_id"]),
            "player_name": b["player_name"],
            "court_id": court_id,
            "court_name": court["name"],
            "date": d.isoformat(),
            "time_start": b["time_start"],
            "time_end": f"{start_h + duration:02d}:00",
            "duration": duration,
            "total_price": int(court["price_per_hour"]) * duration,
            "status": b["status"],
        })
    return out
```

- [ ] **Step 5: Run tests, expect 4 passed.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_seed_loader.py -v
```

- [ ] **Step 6: Commit.**

```bash
git add apps/api/data/__init__.py apps/api/data/seed_loader.py apps/api/tests/test_seed_loader.py
git commit -m "feat(api): seed_loader — load courts/bookings JSON with date resolution"
```

---

## Task 4: `store.py` (TDD)

**Files:**
- Create: `apps/api/data/store.py`
- Create: `apps/api/tests/test_store.py`

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_store.py`:

```python
import pytest

from data import store


SEED_COURTS = [
    {"id": "bbc-01", "name": "Bangkok Badminton Center", "sport": "Badminton",
     "district": "Sukhumvit", "price_per_hour": 450},
    {"id": "sky-02", "name": "Skyline", "sport": "Football",
     "district": "Thong Lor", "price_per_hour": 1200},
]

SEED_BOOKINGS = [
    {"txn_id": "ZP-1", "user_id": 1, "player_name": "Alex", "court_id": "bbc-01",
     "court_name": "Bangkok Badminton Center", "date": "2099-01-02",
     "time_start": "18:00", "time_end": "20:00", "duration": 2,
     "total_price": 900, "status": "CONFIRMED"},
    {"txn_id": "ZP-2", "user_id": 2, "player_name": "Bob", "court_id": "sky-02",
     "court_name": "Skyline", "date": "2099-01-03",
     "time_start": "20:00", "time_end": "21:00", "duration": 1,
     "total_price": 1200, "status": "CONFIRMED"},
]


def _make_bs():
    return store.BookingsStore(SEED_BOOKINGS)


def test_courts_store_by_id():
    cs = store.CourtsStore(SEED_COURTS)
    assert cs.by_id("bbc-01")["name"] == "Bangkok Badminton Center"
    assert cs.by_id("nope") is None
    assert len(cs.all()) == 2


def test_bookings_store_filters():
    bs = _make_bs()
    assert len(bs.for_user(1)) == 1
    assert bs.for_user(1)[0]["txn_id"] == "ZP-1"
    assert len(bs.for_court("sky-02")) == 1
    assert len(bs.all()) == 2


def test_bookings_store_add_assigns_txn_id_if_missing():
    bs = _make_bs()
    row = bs.add({
        "user_id": 1, "player_name": "Alex", "court_id": "bbc-01",
        "court_name": "Bangkok Badminton Center", "date": "2099-02-01",
        "time_start": "10:00", "time_end": "11:00", "duration": 1,
        "total_price": 450, "status": "CONFIRMED",
    })
    assert row["txn_id"].startswith("ZP-")
    assert len(bs.all()) == 3


def test_bookings_store_cancel_marks_status():
    bs = _make_bs()
    cancelled = bs.cancel("ZP-1")
    assert cancelled["status"] == "CANCELLED"
    assert bs.for_user(1)[0]["status"] == "CANCELLED"


def test_bookings_store_cancel_unknown_returns_none():
    bs = _make_bs()
    assert bs.cancel("ZP-DOES-NOT-EXIST") is None


def test_bookings_store_has_conflict_detects_overlap():
    bs = _make_bs()
    # bbc-01 on 2099-01-02 has 18:00-20:00 taken. Booking 19:00 should conflict.
    assert bs.has_conflict("bbc-01", "2099-01-02", "19:00", 1) is True
    # 20:00 same day starts where the existing ends — should NOT conflict.
    assert bs.has_conflict("bbc-01", "2099-01-02", "20:00", 1) is False
    # Different court, same time — no conflict.
    assert bs.has_conflict("sky-02", "2099-01-02", "18:00", 2) is False


def test_bookings_store_reset_replaces_all_rows():
    bs = _make_bs()
    bs.add({"user_id": 9, "player_name": "X", "court_id": "bbc-01",
            "court_name": "Bangkok Badminton Center", "date": "2099-03-01",
            "time_start": "10:00", "time_end": "11:00", "duration": 1,
            "total_price": 450, "status": "CONFIRMED"})
    assert len(bs.all()) == 3
    bs.reset(SEED_BOOKINGS)
    assert len(bs.all()) == 2
```

- [ ] **Step 2: Run, expect ImportError.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_store.py -v
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/data/store.py`:**

```python
"""In-memory data stores. Loaded on FastAPI startup; reset by tests.

Singletons are module-level so routers, agent tools, and tests share state.
Concurrency: single-process FastAPI + the GIL is enough — no locks.
"""
import random
from data import seed_loader


class CourtsStore:
    def __init__(self, seed: list[dict]) -> None:
        self._rows = list(seed)
        self._by_id = {c["id"]: c for c in seed}

    def all(self) -> list[dict]:
        return list(self._rows)

    def by_id(self, court_id: str) -> dict | None:
        return self._by_id.get(court_id)


class BookingsStore:
    def __init__(self, seed: list[dict]) -> None:
        self._rows: list[dict] = list(seed)

    def reset(self, seed: list[dict]) -> None:
        self._rows = list(seed)

    def all(self) -> list[dict]:
        return list(self._rows)

    def for_user(self, user_id: int) -> list[dict]:
        return [b for b in self._rows if b.get("user_id") == user_id]

    def for_court(self, court_id: str) -> list[dict]:
        return [b for b in self._rows if b.get("court_id") == court_id]

    def by_txn(self, txn_id: str) -> dict | None:
        return next((b for b in self._rows if b.get("txn_id") == txn_id), None)

    def has_conflict(
        self, court_id: str, date_iso: str, time_start: str, duration: int,
    ) -> bool:
        start_h = int(time_start.split(":")[0])
        needed = {f"{start_h + i:02d}:00" for i in range(duration)}
        for b in self._rows:
            if b.get("court_id") != court_id or b.get("date") != date_iso:
                continue
            if b.get("status") != "CONFIRMED":
                continue
            b_start = int(b["time_start"].split(":")[0])
            taken = {f"{b_start + i:02d}:00" for i in range(int(b["duration"]))}
            if needed & taken:
                return True
        return False

    def add(self, b: dict) -> dict:
        row = dict(b)
        if not row.get("txn_id"):
            row["txn_id"] = _generate_txn_id()
        row.setdefault("status", "CONFIRMED")
        self._rows.append(row)
        return dict(row)

    def cancel(self, txn_id: str) -> dict | None:
        for b in self._rows:
            if b.get("txn_id") == txn_id:
                b["status"] = "CANCELLED"
                return dict(b)
        return None


def _generate_txn_id() -> str:
    return f"ZP-{random.randint(10000, 99999)}"


# Module-level singletons. None until init_stores() runs (on FastAPI startup).
courts_store: CourtsStore | None = None
bookings_store: BookingsStore | None = None


def init_stores() -> None:
    """Load seed files into the module-level stores. Idempotent."""
    global courts_store, bookings_store
    courts = seed_loader.load_courts()
    courts_store = CourtsStore(courts)
    bookings_store = BookingsStore(seed_loader.load_bookings(courts))


def get_courts_store() -> CourtsStore:
    """Accessor that raises if stores aren't initialized — protects against
    tests/routes that forget the startup hook."""
    if courts_store is None:
        raise RuntimeError("CourtsStore not initialized — call init_stores() first")
    return courts_store


def get_bookings_store() -> BookingsStore:
    if bookings_store is None:
        raise RuntimeError("BookingsStore not initialized — call init_stores() first")
    return bookings_store
```

- [ ] **Step 4: Run tests, expect 7 passed.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_store.py -v
```

- [ ] **Step 5: Commit.**

```bash
git add apps/api/data/store.py apps/api/tests/test_store.py
git commit -m "feat(api): in-memory CourtsStore + BookingsStore (singletons, no locks)"
```

---

## Task 5: `schemas/data.py` (Pydantic models)

**Files:**
- Create: `apps/api/schemas/data.py`

No tests for this task — Pydantic validation gets exercised by the route tests in Task 6.

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/schemas/data.py`:**

```python
"""Pydantic schemas for /courts and /bookings endpoints.

Court keeps the rich frontend shape so a single response satisfies both
frontend pages and agent tools (agents ignore the extra fields).
"""
from typing import Literal

from pydantic import BaseModel


class Amenity(BaseModel):
    icon: str
    label: str
    value: str


class CourtSubCourt(BaseModel):
    number: str
    surface: str


class Court(BaseModel):
    id: str
    name: str
    short_name: str | None = None
    sport: str
    rating: float | None = None
    reviews: int | None = None
    location: str | None = None
    address: str | None = None
    district: str
    price_per_hour: int
    prime_price: int | None = None
    amenities: list[Amenity] = []
    surface: str | None = None
    status: Literal["ACTIVE", "INACTIVE"] | None = "ACTIVE"
    utilization: int | None = None
    utilization_pct: int | None = None
    peak_hours: str | None = None
    ai_efficiency: str | None = None
    tags: list[str] = []
    color: str | None = None
    courts: list[CourtSubCourt] = []


class Booking(BaseModel):
    txn_id: str
    user_id: int
    player_name: str
    court_id: str
    court_name: str
    date: str
    time_start: str
    time_end: str
    duration: int
    total_price: int
    status: Literal["CONFIRMED", "CANCELLED"]


class CreateBookingRequest(BaseModel):
    user_id: int
    court_id: str
    date: str
    time_start: str
    duration: int
    player_name: str | None = None
```

- [ ] **Step 2: Smoke import.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT python -c "from schemas.data import Court, Booking, CreateBookingRequest; print('ok')"
```

Expected: `ok`

- [ ] **Step 3: Commit.**

```bash
git add apps/api/schemas/data.py
git commit -m "feat(api): Pydantic schemas for /courts and /bookings"
```

---

## Task 6: `routers/data.py` + mount in `main.py` (TDD)

**Files:**
- Create: `apps/api/routers/data.py`
- Create: `apps/api/tests/test_data_routes.py`
- Modify: `apps/api/main.py`
- Modify: `apps/api/conftest.py`

- [ ] **Step 1: Modify `/Users/nchawanp/Desktop/ZPOTS/apps/api/conftest.py`** to add an autouse fixture that freezes today and resets stores. Replace the file's contents with:

```python
"""Pytest configuration and autouse fixtures.

- Adds apps/api/ to sys.path so tests can `from main import app` etc.
- Mocks ai.client._get_client() so tests never hit Azure OpenAI.
- Freezes seed_loader._today() to a deterministic date.
- Reinitializes the in-memory stores before every test.
"""
import os
import sys
from datetime import date
from unittest.mock import MagicMock

import pytest

# Ensure apps/api/ is on sys.path so test imports of `main`, `ai.*`, etc. resolve.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FROZEN_TODAY = date(2099, 1, 1)


@pytest.fixture(autouse=True)
def freeze_today_and_reset_stores(monkeypatch):
    """Freeze 'today' and rebuild the in-memory stores before each test.

    Without this, tests depending on dates would be flaky as days pass,
    and tests that mutate the BookingsStore would bleed state into each
    other.
    """
    from data import seed_loader, store

    monkeypatch.setattr(seed_loader, "_today", lambda: FROZEN_TODAY)
    store.init_stores()
    yield


@pytest.fixture(autouse=True)
def mock_openai_client(monkeypatch):
    """Replace ai.client._get_client() with a MagicMock that returns canned responses."""
    fake_msg = MagicMock()
    fake_msg.content = '{"sport": null, "district": null, "time_of_day": null, "max_price": null}'
    fake_choice = MagicMock()
    fake_choice.message = fake_msg
    fake_response = MagicMock()
    fake_response.choices = [fake_choice]
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = fake_response
    monkeypatch.setattr("ai.client._get_client", lambda: fake_client)
    monkeypatch.setattr("ai.client._model", lambda: "test-deployment")
    return fake_client
```

- [ ] **Step 2: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_data_routes.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_courts_returns_six():
    r = client.get("/courts")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 6
    assert body[0]["id"] == "bbc-01"


def test_get_court_by_id_404_for_unknown():
    assert client.get("/courts/nope").status_code == 404


def test_get_court_by_id_success():
    r = client.get("/courts/bbc-01")
    assert r.status_code == 200
    assert r.json()["name"] == "Bangkok Badminton Center"


def test_get_bookings_filters_by_user_id():
    r = client.get("/bookings?user_id=1")
    assert r.status_code == 200
    rows = r.json()
    assert all(row["user_id"] == 1 for row in rows)
    assert len(rows) >= 2  # ZP-90101 + ZP-90001 + ZP-90002


def test_post_booking_creates_and_returns_full_row():
    r = client.post("/bookings", json={
        "user_id": 1, "court_id": "ivh-06",
        "date": "2099-06-01", "time_start": "10:00", "duration": 1,
        "player_name": "Test",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["court_name"] == "Impact Volleyball Hall"
    assert body["total_price"] == 350
    assert body["status"] == "CONFIRMED"
    assert body["txn_id"].startswith("ZP-")


def test_post_booking_unknown_court_returns_422():
    r = client.post("/bookings", json={
        "user_id": 1, "court_id": "does-not-exist",
        "date": "2099-06-01", "time_start": "10:00", "duration": 1,
    })
    assert r.status_code == 422


def test_post_booking_slot_conflict_returns_409():
    # ZP-90101 holds bbc-01 on 2099-01-02 18:00-20:00. Try 19:00 same day.
    r = client.post("/bookings", json={
        "user_id": 1, "court_id": "bbc-01",
        "date": "2099-01-02", "time_start": "19:00", "duration": 1,
    })
    assert r.status_code == 409


def test_cancel_booking_marks_cancelled():
    r = client.post("/bookings/ZP-90101/cancel")
    assert r.status_code == 200
    assert r.json()["status"] == "CANCELLED"


def test_cancel_unknown_returns_404():
    assert client.post("/bookings/ZP-NOPE/cancel").status_code == 404
```

- [ ] **Step 3: Run, expect 404s (router not mounted).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_data_routes.py -v
```

- [ ] **Step 4: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/routers/data.py`:**

```python
"""HTTP API for the seed-backed data stores."""
from fastapi import APIRouter, HTTPException

from data.store import get_bookings_store, get_courts_store
from schemas.data import Booking, Court, CreateBookingRequest

router = APIRouter(tags=["data"])


@router.get("/courts", response_model=list[Court])
def list_courts() -> list[dict]:
    return get_courts_store().all()


@router.get("/courts/{court_id}", response_model=Court)
def get_court(court_id: str) -> dict:
    court = get_courts_store().by_id(court_id)
    if court is None:
        raise HTTPException(status_code=404, detail=f"Unknown court {court_id}")
    return court


@router.get("/bookings", response_model=list[Booking])
def list_bookings(
    user_id: int | None = None,
    court_id: str | None = None,
    status: str | None = None,
) -> list[dict]:
    rows = get_bookings_store().all()
    if user_id is not None:
        rows = [b for b in rows if b.get("user_id") == user_id]
    if court_id is not None:
        rows = [b for b in rows if b.get("court_id") == court_id]
    if status is not None:
        rows = [b for b in rows if b.get("status") == status]
    return rows


@router.post("/bookings", response_model=Booking)
def create_booking(req: CreateBookingRequest) -> dict:
    courts = get_courts_store()
    bookings = get_bookings_store()

    court = courts.by_id(req.court_id)
    if court is None:
        # 422 is more accurate than 404 here — the request body is malformed,
        # not a missing resource at the request path.
        raise HTTPException(status_code=422, detail=f"Unknown court_id {req.court_id}")

    if bookings.has_conflict(req.court_id, req.date, req.time_start, req.duration):
        raise HTTPException(status_code=409, detail="Slot is not available")

    start_h = int(req.time_start.split(":")[0])
    row = bookings.add({
        "user_id": req.user_id,
        "player_name": req.player_name or "Player",
        "court_id": req.court_id,
        "court_name": court["name"],
        "date": req.date,
        "time_start": req.time_start,
        "time_end": f"{start_h + req.duration:02d}:00",
        "duration": req.duration,
        "total_price": int(court["price_per_hour"]) * req.duration,
        "status": "CONFIRMED",
    })
    return row


@router.post("/bookings/{txn_id}/cancel", response_model=Booking)
def cancel_booking(txn_id: str) -> dict:
    bookings = get_bookings_store()
    existing = bookings.by_txn(txn_id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Booking {txn_id} not found")
    if existing.get("status") == "CANCELLED":
        raise HTTPException(status_code=409, detail="Booking is already cancelled")
    cancelled = bookings.cancel(txn_id)
    return cancelled
```

- [ ] **Step 5: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/api/main.py` to mount + add startup hook:**

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

from data.store import init_stores
from routers import ai, chat, data, health, ml


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Single-instance demo: in-memory stores live for the lifetime of this
    # process. Cloud Run must be configured with min/max instances = 1 so
    # state stays coherent across requests.
    init_stores()
    yield


app = FastAPI(
    title="ZPOTS API",
    description="OpenAI/Azure helpers + ML inference + chat agents + seed-backed data.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(ai.router)
app.include_router(ml.router)
app.include_router(chat.router)
app.include_router(data.router)
```

- [ ] **Step 6: Run all api tests, expect green.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest -v
```

Expected: previously-32 + 4 (seed_loader) + 7 (store) + 9 (data_routes) = **52 passed**. (Existing tests still green because the autouse fixture initializes stores even though the old tests don't read them.)

- [ ] **Step 7: Commit.**

```bash
git add apps/api/routers/data.py apps/api/main.py apps/api/conftest.py apps/api/tests/test_data_routes.py
git commit -m "feat(api): /courts and /bookings routes + startup store init

Mount data router. Lifespan hook calls init_stores(). conftest now
freezes today and resets the in-memory stores before each test."
```

---

## Task 7: Refactor `agents/owner/tools.py` to read from stores

**Files:**
- Modify: `apps/api/agents/owner/tools.py`
- Rewrite: `apps/api/tests/test_owner_tools.py`

- [ ] **Step 1: Replace the contents of `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_owner_tools.py`** with tests that exercise the store-backed implementation:

```python
from agents.owner import tools


def test_get_revenue_sums_confirmed_in_range():
    # Seed has ZP-90001 at days_from_today=-3 (2098-12-29 with frozen 2099-01-01)
    # and several upcoming, all CONFIRMED. A wide range hits all.
    result = tools.get_revenue(date_from="2090-01-01", date_to="2099-12-31")
    assert result["total_thb"] > 0
    assert result["bookings"] > 0


def test_get_revenue_empty_range():
    result = tools.get_revenue(date_from="1900-01-01", date_to="1900-12-31")
    assert result["total_thb"] == 0


def test_list_bookings_filters_by_court():
    rows = tools.list_bookings(court_id="bbc-01")
    assert all(r["court_id"] == "bbc-01" for r in rows)
    assert len(rows) >= 1


def test_list_bookings_clamps_limit():
    rows = tools.list_bookings(limit=999)
    assert len(rows) <= 200


def test_summarize_courts_returns_all():
    out = tools.summarize_courts()
    assert any(c["id"] == "bbc-01" for c in out)
    assert all({"id", "name", "sport", "district", "price_per_hour"} <= set(c.keys()) for c in out)


def test_get_demand_forecast_returns_list():
    out = tools.get_demand_forecast(top_n=5)
    assert isinstance(out, list)
    assert len(out) <= 5


def test_rank_noshow_risk_sorted_or_empty():
    out = tools.rank_noshow_risk(limit=5)
    assert isinstance(out, list)
    if len(out) >= 2:
        probs = [r["risk_probability"] for r in out]
        assert probs == sorted(probs, reverse=True)


def test_dispatch_summarize_courts():
    result = tools.dispatch("summarize_courts", {}, user_id=3)
    assert isinstance(result, list)
    assert len(result) > 0
```

- [ ] **Step 2: Run, expect failures (old fixture still in tools.py).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_owner_tools.py -v
```

Some tests will still pass against the old fixture; that's fine. The point of TDD here is the next step rewrites tools.py.

- [ ] **Step 3: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/owner/tools.py`** with the store-backed version. Delete `_BOOKINGS_FIXTURE`, `COURTS`, `_upcoming`. Keep `TOOLS` and `dispatch()` shape unchanged.

```python
"""Owner-agent tools (read-only). Reads from data.store singletons."""
from datetime import date as _date
from typing import Any

from data.store import get_bookings_store, get_courts_store
from ml.inference import predict_noshow_risk
from ml.inference import get_demand_forecast as _get_demand_df

_LIST_BOOKINGS_MAX = 200


def get_revenue(date_from: str, date_to: str) -> dict:
    total = 0
    n = 0
    for b in get_bookings_store().all():
        if b["status"] != "CONFIRMED":
            continue
        if date_from <= b["date"] <= date_to:
            total += b["total_price"]
            n += 1
    return {"total_thb": total, "bookings": n,
            "date_from": date_from, "date_to": date_to}


def list_bookings(
    date_from: str | None = None,
    date_to: str | None = None,
    court_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
) -> list[dict]:
    limit = max(1, min(int(limit), _LIST_BOOKINGS_MAX))
    rows = get_bookings_store().all()
    if date_from:
        rows = [r for r in rows if r["date"] >= date_from]
    if date_to:
        rows = [r for r in rows if r["date"] <= date_to]
    if court_id:
        rows = [r for r in rows if r["court_id"] == court_id]
    if status:
        rows = [r for r in rows if r["status"] == status]
    rows.sort(key=lambda r: (r["date"], r["time_start"]), reverse=True)
    return rows[:limit]


def _hydrate_for_noshow(b: dict) -> dict:
    court = get_courts_store().by_id(b["court_id"]) or {}
    d = _date.fromisoformat(b["date"])
    dow = d.weekday()
    hour = int(b["time_start"].split(":")[0])
    return {
        "court_id": b["court_id"],
        "sport": court.get("sport", "Badminton"),
        "district": court.get("district", "Sukhumvit"),
        "day_of_week": dow,
        "hour": hour,
        "is_weekend": dow >= 5,
        "is_holiday": False,
        "weather": "sunny",
        "price": int(b["total_price"]) // max(1, int(b["duration"])),
        "lead_time_days": max(0, (d - _date.today()).days),
        "is_repeat_customer": True,
    }


def rank_noshow_risk(
    date_from: str | None = None, date_to: str | None = None, limit: int = 10,
) -> list[dict]:
    bookings = list_bookings(date_from=date_from, date_to=date_to,
                             status="CONFIRMED", limit=_LIST_BOOKINGS_MAX)
    scored = []
    for b in bookings:
        feats = _hydrate_for_noshow(b)
        tier, p = predict_noshow_risk(feats)
        scored.append({
            "txn_id": b["txn_id"],
            "player_name": b["player_name"],
            "court_id": b["court_id"],
            "court_name": b["court_name"],
            "date": b["date"],
            "time_start": b["time_start"],
            "risk_tier": tier,
            "risk_probability": round(p, 3),
        })
    scored.sort(key=lambda r: r["risk_probability"], reverse=True)
    return scored[:limit]


def get_demand_forecast(top_n: int = 10) -> list[dict]:
    df = _get_demand_df()
    if df.empty:
        return []
    top = df.sort_values("predicted_bookings", ascending=False).head(top_n)
    return [
        {
            "court_id": r["court_id"],
            "day_of_week": int(r["day_of_week"]),
            "hour": int(r["hour"]),
            "predicted_bookings": round(float(r["predicted_bookings"]), 2),
        }
        for _, r in top.iterrows()
    ]


def summarize_courts() -> list[dict]:
    return [
        {
            "id": c["id"], "name": c["name"], "sport": c["sport"],
            "district": c["district"], "price_per_hour": c["price_per_hour"],
            "utilization_pct": c.get("utilization_pct") or c.get("utilization"),
        }
        for c in get_courts_store().all()
    ]


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_revenue",
            "description": "Sum confirmed-booking revenue (THB) over a date range. Returns {total_thb, bookings, date_from, date_to}.",
            "parameters": {
                "type": "object",
                "required": ["date_from", "date_to"],
                "properties": {
                    "date_from": {"type": "string"}, "date_to": {"type": "string"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_bookings",
            "description": "List bookings filtered by date range, court, or status. Returns up to `limit` rows, newest first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_from": {"type": "string"}, "date_to": {"type": "string"},
                    "court_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["CONFIRMED", "CANCELLED"]},
                    "limit": {"type": "integer"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rank_noshow_risk",
            "description": "Return upcoming CONFIRMED bookings ranked by predicted no-show probability (highest first).",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_from": {"type": "string"}, "date_to": {"type": "string"},
                    "limit": {"type": "integer"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_demand_forecast",
            "description": "Top predicted-busiest (court, day_of_week, hour) cells. day_of_week: 0=Mon..6=Sun.",
            "parameters": {
                "type": "object",
                "properties": {"top_n": {"type": "integer"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_courts",
            "description": "List all courts with id, name, sport, district, price_per_hour, utilization_pct.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def dispatch(name: str, args: dict, user_id: int) -> Any:
    """Owner dispatcher. user_id accepted for parity with the player one but unused."""
    if name == "get_revenue":
        return get_revenue(**args)
    if name == "list_bookings":
        return list_bookings(**args)
    if name == "rank_noshow_risk":
        return rank_noshow_risk(**args)
    if name == "get_demand_forecast":
        return get_demand_forecast(**args)
    if name == "summarize_courts":
        return summarize_courts()
    return {"kind": "error", "message": f"Unknown tool {name}"}
```

- [ ] **Step 4: Run tests, expect 8 passed.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_owner_tools.py -v
```

- [ ] **Step 5: Commit.**

```bash
git add apps/api/agents/owner/tools.py apps/api/tests/test_owner_tools.py
git commit -m "refactor(api): owner tools read from data.store (drop hardcoded fixtures)"
```

---

## Task 8: Refactor `agents/player/tools.py` (drop `bookings` param)

**Files:**
- Modify: `apps/api/agents/player/tools.py`
- Rewrite: `apps/api/tests/test_player_tools.py`

- [ ] **Step 1: Replace the contents of `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_player_tools.py`:**

```python
from agents.player import tools
from data import store


def test_search_courts_filters_by_sport():
    result = tools.search_courts(sport="Badminton")
    assert len(result) >= 1
    assert all(c["sport"] == "Badminton" for c in result)


def test_get_availability_excludes_taken_slots():
    # Seed has ZP-90101 on bbc-01 at 2099-01-02 18:00-20:00 (frozen today=2099-01-01)
    free = tools.get_availability(court_id="bbc-01", date_iso="2099-01-02")
    assert "18:00" not in free
    assert "19:00" not in free
    assert "20:00" in free


def test_get_availability_ignores_other_court():
    free = tools.get_availability(court_id="sky-02", date_iso="2099-01-02")
    assert "18:00" in free


def test_list_my_bookings_filters_by_user():
    rows = tools.list_my_bookings(user_id=1)
    assert all(r.get("court_id") for r in rows)
    assert len(rows) >= 2  # ZP-90101 + ZP-90001 + ZP-90002 belong to user_id=1


def test_propose_booking_returns_draft_with_price():
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2099-07-01", time_start="18:00", duration=2,
    )
    assert draft["kind"] == "booking_draft"
    assert draft["court_name"] == "Bangkok Badminton Center"
    assert draft["total_price"] == 450 * 2
    assert draft["time_end"] == "20:00"


def test_propose_booking_rejects_taken_slot():
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2099-01-02", time_start="18:00", duration=1,
    )
    assert draft["kind"] == "error"
    assert "not available" in draft["message"].lower()


def test_propose_cancel_returns_draft_for_existing():
    draft = tools.propose_cancel(user_id=1, txn_id="ZP-90101")
    assert draft["kind"] == "cancel_draft"
    assert draft["txn_id"] == "ZP-90101"
    assert draft["court_name"] == "Bangkok Badminton Center"


def test_propose_cancel_rejects_unknown_txn():
    draft = tools.propose_cancel(user_id=1, txn_id="ZP-99999")
    assert draft["kind"] == "error"


def test_dispatch_propose_booking_no_bookings_param():
    result = tools.dispatch(
        "propose_booking",
        {"court_id": "bbc-01", "date_iso": "2099-08-01", "time_start": "10:00", "duration": 1},
        user_id=1,
    )
    assert result["kind"] == "booking_draft"
```

- [ ] **Step 2: Run, expect errors (signatures don't match yet).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_player_tools.py -v
```

- [ ] **Step 3: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/player/tools.py`:**

```python
"""Player-agent tools. Reads from data.store; no bookings param required."""
from typing import Any

from data.store import get_bookings_store, get_courts_store

_HOURS = [f"{h:02d}:00" for h in range(7, 23)]  # 07:00..22:00


def search_courts(
    sport: str | None = None,
    district: str | None = None,
    max_price: int | None = None,
) -> list[dict]:
    out = []
    for c in get_courts_store().all():
        if sport and c["sport"].lower() != sport.lower():
            continue
        if district and district.lower() not in c["district"].lower():
            continue
        if max_price is not None and c["price_per_hour"] > max_price:
            continue
        out.append({
            "id": c["id"], "name": c["name"], "sport": c["sport"],
            "district": c["district"], "price_per_hour": c["price_per_hour"],
            "rating": c.get("rating"),
        })
    return out


def get_availability(court_id: str, date_iso: str) -> list[str]:
    """Return free hour-start times (HH:00) for a court on a given date."""
    bs = get_bookings_store()
    free: list[str] = []
    for h in _HOURS:
        if not bs.has_conflict(court_id, date_iso, h, 1):
            free.append(h)
    return free


def list_my_bookings(user_id: int) -> list[dict]:
    return [
        {
            "txn_id": b["txn_id"], "court_id": b["court_id"], "court_name": b["court_name"],
            "date": b["date"], "time_start": b["time_start"], "time_end": b["time_end"],
            "total_price": b["total_price"], "status": b["status"],
        }
        for b in get_bookings_store().for_user(user_id)
    ]


def propose_booking(
    user_id: int, court_id: str, date_iso: str, time_start: str, duration: int,
) -> dict:
    court = get_courts_store().by_id(court_id)
    if court is None:
        return {"kind": "error", "message": f"Unknown court id {court_id}"}

    if get_bookings_store().has_conflict(court_id, date_iso, time_start, duration):
        return {"kind": "error", "message": f"Slot is not available on {date_iso} at {time_start}."}

    start_h = int(time_start.split(":")[0])
    time_end = f"{start_h + duration:02d}:00"
    total = court["price_per_hour"] * duration
    return {
        "kind": "booking_draft",
        "court_id": court_id,
        "court_name": court["name"],
        "date": date_iso,
        "time_start": time_start,
        "time_end": time_end,
        "duration": duration,
        "total_price": total,
    }


def propose_cancel(user_id: int, txn_id: str) -> dict:
    booking = get_bookings_store().by_txn(txn_id)
    if booking is None:
        return {"kind": "error", "message": f"Booking {txn_id} not found."}
    if booking.get("status") == "CANCELLED":
        return {"kind": "error", "message": "Booking is already cancelled."}
    return {
        "kind": "cancel_draft",
        "txn_id": booking["txn_id"],
        "court_name": booking["court_name"],
        "date": booking["date"],
        "time_start": booking["time_start"],
    }


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_courts",
            "description": "Find courts matching sport/district/max_price filters. Returns id, name, sport, district, price_per_hour, rating.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sport": {"type": "string", "description": "e.g. Badminton, Football, Padel"},
                    "district": {"type": "string"},
                    "max_price": {"type": "integer", "description": "Max THB per hour"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_availability",
            "description": "List free hour-start times (HH:00) for a court on a given date.",
            "parameters": {
                "type": "object",
                "required": ["court_id", "date_iso"],
                "properties": {
                    "court_id": {"type": "string"},
                    "date_iso": {"type": "string", "description": "YYYY-MM-DD"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_my_bookings",
            "description": "Return all bookings belonging to the current user.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "propose_booking",
            "description": "Draft a booking for confirmation. Does NOT write. The user will see Confirm/Cancel buttons. Always call this before booking.",
            "parameters": {
                "type": "object",
                "required": ["court_id", "date_iso", "time_start", "duration"],
                "properties": {
                    "court_id": {"type": "string"},
                    "date_iso": {"type": "string", "description": "YYYY-MM-DD"},
                    "time_start": {"type": "string", "description": "HH:00 24-hour"},
                    "duration": {"type": "integer", "description": "Hours, 1-4"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "propose_cancel",
            "description": "Draft a cancellation for confirmation. Does NOT write. Takes the txn_id (string, like 'ZP-12345') from list_my_bookings.",
            "parameters": {
                "type": "object",
                "required": ["txn_id"],
                "properties": {"txn_id": {"type": "string"}},
            },
        },
    },
]


def dispatch(name: str, args: dict, user_id: int) -> Any:
    """Run a tool by name. Threads only user_id; bookings come from the store."""
    if name == "search_courts":
        return search_courts(**args)
    if name == "get_availability":
        return get_availability(**args)
    if name == "list_my_bookings":
        return list_my_bookings(user_id=user_id)
    if name == "propose_booking":
        return propose_booking(user_id=user_id, **args)
    if name == "propose_cancel":
        return propose_cancel(user_id=user_id, **args)
    return {"kind": "error", "message": f"Unknown tool {name}"}
```

- [ ] **Step 4: Run tests, expect 9 passed** (was 8 in Phase 3c; +1 because dispatch test was split).

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_player_tools.py -v
```

- [ ] **Step 5: Commit.**

```bash
git add apps/api/agents/player/tools.py apps/api/tests/test_player_tools.py
git commit -m "refactor(api): player tools read from data.store (drop bookings param)"
```

---

## Task 9: Update player agent + chat router + chat schemas (drop `bookings`)

**Files:**
- Modify: `apps/api/agents/player/agent.py`
- Modify: `apps/api/routers/chat.py`
- Modify: `apps/api/schemas/chat.py`
- Modify: `apps/api/tests/test_player_agent.py`
- Modify: `apps/api/tests/test_chat_routes.py`

- [ ] **Step 1: Update `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/player/agent.py`** — drop the `bookings` parameter. Replace the file with:

```python
"""Player agent tool-calling loop (OpenAI / Azure OpenAI)."""
import json

from ai.client import chat
from agents.player import tools as player_tools
from agents.player.system_prompt import build_system_prompt

MAX_HOPS = 6


def run_turn(messages: list[dict], user: dict) -> dict:
    """Run one user turn through the agent.

    Returns:
        {"text": <final assistant text>, "draft": <pending draft dict or None>,
         "history": <updated message history>}
    """
    messages = list(messages)
    system = build_system_prompt(user)
    pending_draft = None

    for _ in range(MAX_HOPS):
        response = chat(messages, tools=player_tools.TOOLS, system=system)
        choice = response.choices[0]
        msg = choice.message

        assistant_turn: dict = {"role": "assistant", "content": msg.content or ""}
        if msg.tool_calls:
            assistant_turn["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ]
        messages.append(assistant_turn)

        if choice.finish_reason != "tool_calls":
            return {
                "text": (msg.content or "").strip(),
                "draft": pending_draft,
                "history": messages,
            }

        for tc in msg.tool_calls or []:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            result = player_tools.dispatch(
                tc.function.name, args, user_id=user["id"],
            )
            if isinstance(result, dict) and result.get("kind") in ("booking_draft", "cancel_draft"):
                pending_draft = result
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, default=str),
            })

    return {"text": "(agent hop limit reached)", "draft": pending_draft, "history": messages}
```

- [ ] **Step 2: Update `/Users/nchawanp/Desktop/ZPOTS/apps/api/schemas/chat.py`** — drop `BookingSnapshot` and the `bookings` field. Replace the file with:

```python
"""Chat request / response schemas. Used by /chat/player and /chat/owner."""
from typing import Literal

from pydantic import BaseModel


class ChatUser(BaseModel):
    id: int
    name: str


class ChatMessage(BaseModel):
    role: Literal['user', 'assistant', 'tool', 'system']
    content: str | None = None
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None


class BookingDraft(BaseModel):
    kind: Literal['booking_draft'] = 'booking_draft'
    court_id: str
    court_name: str
    date: str
    time_start: str
    time_end: str
    duration: int
    total_price: int


class CancelDraft(BaseModel):
    kind: Literal['cancel_draft'] = 'cancel_draft'
    txn_id: str
    court_name: str
    date: str
    time_start: str


class ChatPlayerRequest(BaseModel):
    messages: list[ChatMessage]
    user: ChatUser


class ChatPlayerResponse(BaseModel):
    text: str
    draft: BookingDraft | CancelDraft | None = None
    history: list[ChatMessage]


class ChatOwnerRequest(BaseModel):
    messages: list[ChatMessage]
    user: ChatUser


class ChatOwnerResponse(BaseModel):
    text: str
    history: list[ChatMessage]
```

- [ ] **Step 3: Update `/Users/nchawanp/Desktop/ZPOTS/apps/api/routers/chat.py`** — stop passing `bookings`. Replace the file with:

```python
from fastapi import APIRouter

from agents.player.agent import run_turn as player_run_turn
from agents.owner.agent import run_turn as owner_run_turn
from schemas.chat import (
    ChatOwnerRequest, ChatOwnerResponse,
    ChatPlayerRequest, ChatPlayerResponse,
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/player", response_model=ChatPlayerResponse)
def chat_player(req: ChatPlayerRequest) -> ChatPlayerResponse:
    result = player_run_turn(
        messages=[m.model_dump(exclude_none=True) for m in req.messages],
        user=req.user.model_dump(),
    )
    return ChatPlayerResponse(
        text=result["text"],
        draft=result["draft"],
        history=result["history"],
    )


@router.post("/owner", response_model=ChatOwnerResponse)
def chat_owner(req: ChatOwnerRequest) -> ChatOwnerResponse:
    result = owner_run_turn(
        messages=[m.model_dump(exclude_none=True) for m in req.messages],
        user=req.user.model_dump(),
    )
    return ChatOwnerResponse(
        text=result["text"],
        history=result["history"],
    )
```

- [ ] **Step 4: Update `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_player_agent.py`** — drop the `bookings=` kwarg in three places:

```python
from unittest.mock import MagicMock

from agents.player import agent


def _msg(content: str | None = None, tool_calls: list | None = None):
    msg = MagicMock(); msg.content = content; msg.tool_calls = tool_calls
    choice = MagicMock(); choice.message = msg
    choice.finish_reason = "tool_calls" if tool_calls else "stop"
    resp = MagicMock(); resp.choices = [choice]
    return resp


def _tool_call(name: str, args: str = "{}", tc_id: str = "t1"):
    tc = MagicMock(); tc.id = tc_id
    tc.function.name = name
    tc.function.arguments = args
    return tc


def test_run_turn_returns_text_when_no_tool_calls(monkeypatch, mock_openai_client):
    mock_openai_client.chat.completions.create.return_value = _msg(content="Hi Alex!")
    result = agent.run_turn(
        messages=[{"role": "user", "content": "hello"}],
        user={"id": 1, "name": "Alex"},
    )
    assert result["text"] == "Hi Alex!"
    assert result["draft"] is None
    assert len(result["history"]) == 2


def test_run_turn_dispatches_tool_then_responds(monkeypatch, mock_openai_client):
    mock_openai_client.chat.completions.create.side_effect = [
        _msg(tool_calls=[_tool_call("search_courts", '{"sport": "Badminton"}')]),
        _msg(content="Found Bangkok Badminton Center."),
    ]
    result = agent.run_turn(
        messages=[{"role": "user", "content": "find badminton"}],
        user={"id": 1, "name": "Alex"},
    )
    assert "Bangkok Badminton" in result["text"]
    assert mock_openai_client.chat.completions.create.call_count == 2


def test_run_turn_surfaces_booking_draft(monkeypatch, mock_openai_client):
    mock_openai_client.chat.completions.create.side_effect = [
        _msg(tool_calls=[_tool_call(
            "propose_booking",
            '{"court_id": "bbc-01", "date_iso": "2099-06-01", "time_start": "18:00", "duration": 1}',
        )]),
        _msg(content="Confirm to book?"),
    ]
    result = agent.run_turn(
        messages=[{"role": "user", "content": "book bbc-01 tomorrow 6pm"}],
        user={"id": 1, "name": "Alex"},
    )
    assert result["draft"] is not None
    assert result["draft"]["kind"] == "booking_draft"
    assert result["draft"]["court_name"] == "Bangkok Badminton Center"
```

- [ ] **Step 5: Update `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_chat_routes.py`** — drop the `bookings: []` from the player request body:

```python
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _msg(content: str | None = None, tool_calls: list | None = None):
    msg = MagicMock(); msg.content = content; msg.tool_calls = tool_calls
    choice = MagicMock(); choice.message = msg
    choice.finish_reason = "tool_calls" if tool_calls else "stop"
    resp = MagicMock(); resp.choices = [choice]
    return resp


def test_chat_player_returns_text_and_history(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value = _msg(content="Hi Alex!")
    r = client.post("/chat/player", json={
        "messages": [{"role": "user", "content": "hello"}],
        "user": {"id": 1, "name": "Alex"},
    })
    assert r.status_code == 200
    body = r.json()
    assert body["text"] == "Hi Alex!"
    assert body["draft"] is None
    assert len(body["history"]) >= 2


def test_chat_owner_returns_text_and_history(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value = _msg(content="Revenue today: ฿1,420.")
    r = client.post("/chat/owner", json={
        "messages": [{"role": "user", "content": "revenue?"}],
        "user": {"id": 3, "name": "Venue Admin"},
    })
    assert r.status_code == 200
    body = r.json()
    assert "1,420" in body["text"]
    assert "draft" not in body
```

- [ ] **Step 6: Run all api tests, expect green.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest -v
```

Expected: **53 passed** (52 after Task 6 + 1 from the Task 8 player_tools delta; Task 7 and Task 9 don't change counts).

- [ ] **Step 7: Commit.**

```bash
git add apps/api/agents/player/agent.py apps/api/schemas/chat.py apps/api/routers/chat.py apps/api/tests/test_player_agent.py apps/api/tests/test_chat_routes.py
git commit -m "refactor(api): drop bookings param from player chat (store is the truth)"
```

---

## Task 10: Frontend — `data-client.ts` + `chat-types.ts` drop bookings

**Files:**
- Create: `apps/web/lib/data-client.ts`
- Modify: `apps/web/lib/chat-types.ts`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/lib/data-client.ts`:**

```ts
import type { Court, Booking } from './types';

export type CreateBookingRequest = {
  user_id: number;
  court_id: string;
  date: string;
  time_start: string;
  duration: number;
  player_name?: string;
};

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`/api${path}`);
  if (!res.ok) throw new Error(`GET /api${path} failed: ${res.status}`);
  return res.json();
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`/api${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`POST /api${path} failed: ${res.status}${text ? ` — ${text}` : ''}`);
  }
  return res.json();
}

export const getCourts = () => fetchJson<Court[]>('/courts');
export const getCourt = (id: string) => fetchJson<Court>(`/courts/${id}`);

export type BookingsQuery = { user_id?: number; court_id?: string; status?: string };
export function getBookings(params: BookingsQuery = {}): Promise<Booking[]> {
  const qs = new URLSearchParams();
  if (params.user_id !== undefined) qs.set('user_id', String(params.user_id));
  if (params.court_id) qs.set('court_id', params.court_id);
  if (params.status) qs.set('status', params.status);
  const suffix = qs.toString() ? `?${qs}` : '';
  return fetchJson<Booking[]>(`/bookings${suffix}`);
}

export const createBooking = (req: CreateBookingRequest) =>
  postJson<Booking>('/bookings', req);

export const cancelBookingApi = (txnId: string) =>
  postJson<Booking>(`/bookings/${txnId}/cancel`, {});
```

- [ ] **Step 2: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/lib/chat-types.ts`** — drop `BookingSnapshot` and the `bookings` field:

```ts
// Mirrors apps/api/schemas/chat.py

export type ChatRole = 'user' | 'assistant' | 'tool' | 'system';

export type ChatToolCall = {
  id: string;
  type: 'function';
  function: { name: string; arguments: string };
};

export type ChatMessage = {
  role: ChatRole;
  content?: string | null;
  tool_calls?: ChatToolCall[] | null;
  tool_call_id?: string | null;
};

export type ChatUser = { id: number; name: string };

export type BookingDraft = {
  kind: 'booking_draft';
  court_id: string;
  court_name: string;
  date: string;
  time_start: string;
  time_end: string;
  duration: number;
  total_price: number;
};

export type CancelDraft = {
  kind: 'cancel_draft';
  txn_id: string;
  court_name: string;
  date: string;
  time_start: string;
};

export type ChatDraft = BookingDraft | CancelDraft;

export type ChatPlayerRequest = {
  messages: ChatMessage[];
  user: ChatUser;
};
export type ChatPlayerResponse = {
  text: string;
  draft: ChatDraft | null;
  history: ChatMessage[];
};

export type ChatOwnerRequest = {
  messages: ChatMessage[];
  user: ChatUser;
};
export type ChatOwnerResponse = {
  text: string;
  history: ChatMessage[];
};
```

- [ ] **Step 3: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build
```

Build will likely fail at this step because ChatWidget still references `BookingSnapshot` and the `bookings` field — that's expected. Note the errors and proceed to Task 11.

- [ ] **Step 4: Commit.**

```bash
git add apps/web/lib/data-client.ts apps/web/lib/chat-types.ts
git commit -m "feat(web): data-client.ts + drop BookingSnapshot from chat-types"
```

---

## Task 11: Frontend — `booking-store.ts` refactor (hydrate via API)

**Files:**
- Modify: `apps/web/lib/booking-store.ts`

Drop the localStorage persist middleware. The store becomes a thin in-memory cache; `hydrate()` calls the API once on app mount; mutations go through the API and update the cache with the server's response.

- [ ] **Step 1: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/lib/booking-store.ts`:**

```ts
import { create } from 'zustand';
import type { Booking, BookingDraft } from './types';
import { cancelBookingApi, createBooking, getBookings } from './data-client';

export function generateTxnId(): string {
  const n = Math.floor(Math.random() * 90000) + 10000;
  return `ZP-${n}`;
}

type State = {
  bookings: Booking[];
  hydrated: boolean;
  hydrate: (userId: number) => Promise<void>;
  addBooking: (userId: number, draft: BookingDraft) => Promise<string>;
  addBookingWithTxn: (txnId: string, draft: BookingDraft) => string;
  cancelBooking: (txnId: string) => Promise<void>;
  getByTxn: (txnId: string) => Booking | undefined;
};

export const useBookingStore = create<State>()((set, get) => ({
  bookings: [],
  hydrated: false,

  hydrate: async (userId) => {
    try {
      const rows = await getBookings({ user_id: userId });
      // Backend rows lack the frontend's `id` (sequential number) and
      // `created_at` fields. Synthesize them so consumers don't have to
      // deal with optional fields.
      const hydrated: Booking[] = rows.map((r, i) => ({
        id: i + 1,
        txn_id: r.txn_id,
        court_id: r.court_id,
        court_name: r.court_name,
        date: r.date,
        time_start: r.time_start,
        time_end: r.time_end,
        duration: r.duration,
        total_price: r.total_price,
        status: r.status,
        created_at: new Date().toISOString(),
      }));
      set({ bookings: hydrated, hydrated: true });
    } catch {
      // Leave cache empty if hydration fails; pages render empty state.
      set({ hydrated: true });
    }
  },

  addBooking: async (userId, draft) => {
    const row = await createBooking({
      user_id: userId,
      court_id: draft.court_id,
      date: draft.date,
      time_start: draft.time_start,
      duration: draft.duration,
    });
    const next: Booking = {
      id: get().bookings.length + 1,
      txn_id: row.txn_id,
      court_id: row.court_id,
      court_name: row.court_name,
      date: row.date,
      time_start: row.time_start,
      time_end: row.time_end,
      duration: row.duration,
      total_price: row.total_price,
      status: row.status,
      created_at: new Date().toISOString(),
    };
    set({ bookings: [...get().bookings, next] });
    return row.txn_id;
  },

  // Kept for legacy non-API callers (e.g. the manual /book page flow if any
  // still uses it). Pushes a row into the cache without hitting the API.
  // Prefer addBooking for new code.
  addBookingWithTxn: (txnId, draft) => {
    const existing = get().bookings.find((b) => b.txn_id === txnId);
    if (existing) return existing.txn_id;
    const next: Booking = {
      id: get().bookings.length + 1,
      txn_id: txnId,
      court_id: draft.court_id,
      court_name: draft.court_name,
      date: draft.date,
      time_start: draft.time_start,
      time_end: draft.time_end,
      duration: draft.duration,
      total_price: draft.total_price,
      status: 'CONFIRMED',
      created_at: new Date().toISOString(),
    };
    set({ bookings: [...get().bookings, next] });
    return txnId;
  },

  cancelBooking: async (txnId) => {
    try {
      const row = await cancelBookingApi(txnId);
      set({
        bookings: get().bookings.map((b) =>
          b.txn_id === txnId ? { ...b, status: row.status } : b,
        ),
      });
    } catch {
      // Optimistic local cancel as a fallback so the UI doesn't get stuck.
      set({
        bookings: get().bookings.map((b) =>
          b.txn_id === txnId ? { ...b, status: 'CANCELLED' } : b,
        ),
      });
    }
  },

  getByTxn: (txnId) => get().bookings.find((b) => b.txn_id === txnId),
}));
```

- [ ] **Step 2: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build
```

Build may still fail because ChatWidget still passes `bookings` to chatPlayer and the manual /book page may call the old `addBooking(draft)` signature. Note errors — Task 12 + 13 fix them.

- [ ] **Step 3: Commit.**

```bash
git add apps/web/lib/booking-store.ts
git commit -m "refactor(web): booking-store hydrates from API, drops localStorage persist"
```

---

## Task 12: Frontend — `BookingsHydrator` + `ChatWidget` update + mount in layouts

**Files:**
- Create: `apps/web/components/BookingsHydrator.tsx`
- Modify: `apps/web/components/chat/ChatWidget.tsx`
- Modify: `apps/web/app/player/layout.tsx`
- Modify: `apps/web/app/owner/layout.tsx`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/BookingsHydrator.tsx`:**

```tsx
'use client';
import { useEffect } from 'react';

import { useBookingStore } from '@/lib/booking-store';

type Props = { userId: number };

/**
 * Calls the booking store's hydrate() once on mount. Runs at the layout level
 * so /player/* and /owner/* pages can rely on `useBookingStore` being populated.
 */
export function BookingsHydrator({ userId }: Props) {
  useEffect(() => {
    useBookingStore.getState().hydrate(userId);
  }, [userId]);

  return null;
}
```

- [ ] **Step 2: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/chat/ChatWidget.tsx`** — drop the `bookings` field from the request body, switch confirm-booking to the async `addBooking` path so it persists through the API:

```tsx
'use client';
import { useEffect, useRef, useState } from 'react';

import { Button } from '@/components/Button';
import { Icon } from '@/components/Icon';
import { ChatBubble } from './ChatBubble';
import { ConfirmDraft } from './ConfirmDraft';
import { currentUser, currentOwner } from '@/lib/auth-stub';
import { useBookingStore } from '@/lib/booking-store';
import { chatOwner, chatPlayer } from '@/lib/chat-client';
import type { ChatDraft, ChatMessage } from '@/lib/chat-types';

type Props = { role: 'player' | 'owner' };

const PLAYER_WELCOME =
  "Hi! I can find courts, check availability, or book you a slot. " +
  "Try **find badminton near Sukhumvit Friday under 400 baht** or **book bbc-01 tomorrow 6pm**.";

const OWNER_WELCOME =
  "Hi! Ask me about revenue, no-show risk, or busiest hours. " +
  "Try **what's my revenue this week?** or **which upcoming bookings are highest risk?**";

export function ChatWidget({ role }: Props) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [pendingDraft, setPendingDraft] = useState<ChatDraft | null>(null);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const user = role === 'player' ? currentUser : currentOwner;
  const addBookingAsync = useBookingStore((s) => s.addBooking);
  const cancelBookingAsync = useBookingStore((s) => s.cancelBooking);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, busy]);

  const visible = messages.filter(
    (m) => m.role === 'user' || (m.role === 'assistant' && m.content),
  );

  async function send() {
    const text = input.trim();
    if (!text || busy) return;
    setInput('');
    setError(null);
    setPendingDraft(null);

    const userMsg: ChatMessage = { role: 'user', content: text };
    const nextMessages = [...messages, userMsg];
    setMessages(nextMessages);
    setBusy(true);

    try {
      if (role === 'player') {
        const res = await chatPlayer({ messages: nextMessages, user });
        setMessages(res.history);
        setPendingDraft(res.draft);
      } else {
        const res = await chatOwner({ messages: nextMessages, user });
        setMessages(res.history);
      }
    } catch (e) {
      setError("Couldn't reach the assistant. Try again?");
    } finally {
      setBusy(false);
    }
  }

  async function handleConfirm() {
    if (!pendingDraft) return;
    try {
      if (pendingDraft.kind === 'booking_draft') {
        const txn = await addBookingAsync(user.id, {
          court_id: pendingDraft.court_id,
          court_name: pendingDraft.court_name,
          date: pendingDraft.date,
          time_start: pendingDraft.time_start,
          time_end: pendingDraft.time_end,
          duration: pendingDraft.duration,
          total_price: pendingDraft.total_price,
        });
        setMessages((m) => [
          ...m,
          { role: 'assistant', content: `✅ Booked! Transaction id **${txn}**.` },
        ]);
      } else {
        await cancelBookingAsync(pendingDraft.txn_id);
        setMessages((m) => [...m, { role: 'assistant', content: '✅ Cancelled.' }]);
      }
    } catch (e) {
      setMessages((m) => [
        ...m,
        { role: 'assistant', content: "Sorry — that didn't go through. Try again?" },
      ]);
    } finally {
      setPendingDraft(null);
    }
  }

  function handleDecline() {
    setMessages((m) => [...m, { role: 'assistant', content: 'Okay, no changes made.' }]);
    setPendingDraft(null);
  }

  const welcome = role === 'player' ? PLAYER_WELCOME : OWNER_WELCOME;

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-label={open ? 'Close chat' : 'Open chat'}
        className="fixed bottom-6 right-6 z-50 w-16 h-16 rounded-full bg-zpots-lime text-zpots-forest shadow-card-lift flex items-center justify-center text-2xl hover:scale-105 transition-transform"
      >
        {open ? '✕' : '💬'}
      </button>

      {open && (
        <div className="fixed bottom-24 right-6 z-50 w-[400px] h-[600px] bg-white rounded-card shadow-card-lift flex flex-col overflow-hidden border border-zpots-mint">
          <header className="px-4 py-3 border-b border-zpots-mint flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Icon name="smart_toy" style={{ fontSize: 18, color: '#2E6B00' }} />
              <span className="font-display font-bold text-sm">
                {role === 'player' ? 'ZPOTS Player Assistant' : 'ZPOTS Owner Assistant'}
              </span>
            </div>
            <button type="button" onClick={() => setOpen(false)} aria-label="Close chat">
              <Icon name="close" style={{ fontSize: 18, color: '#3d4455' }} />
            </button>
          </header>

          <div ref={scrollRef} className="flex-1 overflow-y-auto p-3 flex flex-col gap-3 bg-zpots-surface">
            {visible.length === 0 && <ChatBubble role="assistant">{welcome}</ChatBubble>}
            {visible.map((m, i) => (
              <ChatBubble key={i} role={m.role as 'user' | 'assistant'}>
                {m.content ?? ''}
              </ChatBubble>
            ))}
            {pendingDraft && (
              <ConfirmDraft
                draft={pendingDraft}
                onConfirm={handleConfirm}
                onCancel={handleDecline}
                disabled={busy}
              />
            )}
            {busy && <div className="text-xs text-zpots-muted italic px-2">Thinking…</div>}
            {error && <div className="text-xs text-red-700 px-2">{error}</div>}
          </div>

          <form
            className="border-t border-zpots-mint p-2 flex gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              send();
            }}
          >
            <input
              className="field-input flex-1"
              placeholder={role === 'player' ? 'Ask about courts or bookings…' : 'Ask about your venue…'}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={busy}
            />
            <Button variant="primary" type="submit" disabled={busy || !input.trim()}>
              Send
            </Button>
          </form>
        </div>
      )}
    </>
  );
}
```

- [ ] **Step 3: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/app/player/layout.tsx`:**

```tsx
import { PlayerTopBar } from '@/components/PlayerTopBar';
import { ChatWidget } from '@/components/chat/ChatWidget';
import { BookingsHydrator } from '@/components/BookingsHydrator';
import { currentUser } from '@/lib/auth-stub';

export default function PlayerLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <BookingsHydrator userId={currentUser.id} />
      <PlayerTopBar />
      <main className="max-w-[1200px] mx-auto px-8 py-6">{children}</main>
      <ChatWidget role="player" />
    </>
  );
}
```

- [ ] **Step 4: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/app/owner/layout.tsx`** — owner-side also hydrates bookings so the owner views (e.g. the bookings page) reflect what the player just booked:

```tsx
import { OwnerSidebar } from '@/components/OwnerSidebar';
import { ChatWidget } from '@/components/chat/ChatWidget';
import { BookingsHydrator } from '@/components/BookingsHydrator';
import { currentOwner } from '@/lib/auth-stub';

export default function OwnerLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-zpots-surface">
      <BookingsHydrator userId={currentOwner.id} />
      <OwnerSidebar />
      <main className="flex-1 px-8 py-6 max-w-[1400px]">{children}</main>
      <ChatWidget role="owner" />
    </div>
  );
}
```

- [ ] **Step 5: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build
```

May still fail if any other page calls `addBooking(draft)` with the old single-arg signature — Task 13 covers page-level fixes.

- [ ] **Step 6: Commit.**

```bash
git add apps/web/components/BookingsHydrator.tsx apps/web/components/chat/ChatWidget.tsx apps/web/app/player/layout.tsx apps/web/app/owner/layout.tsx
git commit -m "feat(web): BookingsHydrator + ChatWidget async confirm via API"
```

---

## Task 13: Frontend — refactor page components to use `data-client`

**Files:**
- Modify: `apps/web/lib/mock-data.ts` (repurpose as FALLBACK_COURTS, keep helpers)
- Modify: any page that imports `COURTS`, `getCourt`, or calls the old `addBooking(draft)` signature

This task is a sweep across page files. The implementer should grep for every consumer and update it; the spec calls out the major ones below.

- [ ] **Step 1: Find every consumer of the old mock-data exports.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS && grep -rln "from '@/lib/mock-data'" apps/web/app apps/web/components
```

Expected matches (rough): `app/player/search/page.tsx`, `app/player/courts/[id]/page.tsx`, `app/player/courts/[id]/book/page.tsx`, `app/owner/venues/page.tsx`, `app/owner/venues/[id]/edit/page.tsx`. Implementer must check the actual grep output and refactor each.

- [ ] **Step 2: For each consumer, replace the import + usage.** The patterns are:

  - **Server component reads `COURTS` for a list** → make the page `async`, replace with `await getCourts()`:
    ```tsx
    // before
    import { COURTS } from '@/lib/mock-data';
    export default function Page() {
      return <div>{COURTS.map(...)}</div>;
    }
    // after
    import { getCourts } from '@/lib/data-client';
    import { FALLBACK_COURTS } from '@/lib/mock-data';
    export default async function Page() {
      const courts = await getCourts().catch(() => FALLBACK_COURTS);
      return <div>{courts.map(...)}</div>;
    }
    ```

  - **Server component reads `getCourt(id)`** → `await getCourt(id).catch(() => FALLBACK_COURTS.find(c => c.id === id))`.

  - **Client component reads `COURTS`** → fetch via `useEffect`, render placeholder while loading.

  - **Any page that calls `useBookingStore.getState().addBooking(draft)`** must be updated to `await useBookingStore.getState().addBooking(currentUser.id, draft)`. Wrap in try/catch and surface errors.

- [ ] **Step 3: Repurpose `/Users/nchawanp/Desktop/ZPOTS/apps/web/lib/mock-data.ts`** — rename the export, drop SEEDED_BOOKINGS (backend serves those now), keep `getFreeSlotStarts`/`ALL_HOURS` as utilities and keep `getCourt` as a fallback lookup:

```ts
import type { Court, Booking } from './types';

// Fallback courts used only when GET /api/courts fails. Mirrors the seed JSON
// so the UI degrades gracefully when the API is unreachable.
export const FALLBACK_COURTS: Court[] = [
  // ...copy the same 6 entries from the old COURTS array verbatim...
];

const HOURS = Array.from({ length: 16 }, (_, i) => `${String(i + 7).padStart(2, '0')}:00`);

export function fallbackCourt(id: string): Court | undefined {
  return FALLBACK_COURTS.find((c) => c.id === id);
}

/**
 * Returns hour-start times (HH:00) free for a given court+date, given an
 * external list of bookings. Used by the manual /book page for UI rendering.
 */
export function getFreeSlotStarts(
  courtId: string,
  dateIso: string,
  bookings: Pick<Booking, 'court_id' | 'date' | 'time_start' | 'duration' | 'status'>[],
): string[] {
  const taken = new Set<string>();
  for (const b of bookings) {
    if (b.court_id !== courtId || b.date !== dateIso || b.status !== 'CONFIRMED') continue;
    const startH = parseInt(b.time_start.slice(0, 2), 10);
    for (let i = 0; i < b.duration; i++) {
      taken.add(`${String(startH + i).padStart(2, '0')}:00`);
    }
  }
  return HOURS.filter((h) => !taken.has(h));
}

export const ALL_HOURS = HOURS;
```

(Implementer: paste the full 6 court objects from the previous version into FALLBACK_COURTS.)

For any consumer that imported `COURTS` or `getCourt`, the migration is:

| Old import | New import |
|---|---|
| `import { COURTS } from '@/lib/mock-data'` (Server) | `import { getCourts } from '@/lib/data-client'; import { FALLBACK_COURTS } from '@/lib/mock-data'` |
| `import { getCourt } from '@/lib/mock-data'` (Server) | `import { getCourt } from '@/lib/data-client'; import { fallbackCourt } from '@/lib/mock-data'` |
| `import { SEEDED_BOOKINGS } from '@/lib/mock-data'` | Remove; bookings come from `useBookingStore` (hydrated by BookingsHydrator) |

- [ ] **Step 4: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm build
```

Expected: clean. If `addBookingWithTxn` is still called anywhere, leave that path alone — the function still exists for backward compatibility.

- [ ] **Step 5: Run vitest.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm test:unit
```

Expected: 31 passed (existing count; no new vitest tests required for 4a — the API has full coverage).

- [ ] **Step 6: Commit.**

```bash
git add apps/web/lib/mock-data.ts apps/web/app apps/web/components
git commit -m "refactor(web): page components fetch courts via data-client (FALLBACK_COURTS on error)"
```

---

## Task 14: Final smoke + open PR

- [ ] **Step 1: Run all automated checks.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS

# Streamlit (untouched)
conda run -n MADT pytest tests/ -q

# FastAPI
cd apps/api && conda run -n MADT pytest -q && cd ..

# Vitest + build + Playwright
cd apps/web && pnpm test:unit && pnpm build && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm test
cd ../..
```

Expected:
- Streamlit pytest: **29 passed**
- FastAPI pytest: **53 passed** (was 32; +4 seed_loader +7 store +9 data_routes +1 player_tools delta)
- Vitest: **31 passed** (unchanged)
- `pnpm build`: exit 0
- Playwright: **3 passed** (landing + player-flow + owner-flow)

- [ ] **Step 2: Manual browser smoke** (requires `dev.env` Azure vars).

Two terminals:

```bash
# Terminal A — FastAPI (must be 8000)
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT uvicorn main:app --reload --port 8000

# Terminal B — Next.js
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm dev
```

Verify at http://localhost:3000:

1. `/player/search` — shows 6 courts (from API). Kill the API, refresh → still shows 6 courts (FALLBACK_COURTS).
2. `/player/bookings` — Alex sees ZP-90001, ZP-90101, ZP-90002 (the three with user_id=1).
3. Open player chat → "book bbc-01 tomorrow 6pm for 1 hour" → Confirm → "✅ Booked! ZP-XXXXX" → reload `/player/bookings` → new booking present (persisted via API).
4. Switch to owner (`/owner/bookings`) → the player's newly-created booking is visible.
5. Open owner chat → "what's my revenue this week?" → returns a number that includes the new booking.
6. Restart Terminal A's uvicorn → reload `/player/bookings` → only seed entries; the booking from step 3 is gone (in-memory reset, as intended).
7. `streamlit run app.py` still works at http://localhost:8501 (untouched).

- [ ] **Step 3: Push + open PR.**

```bash
git push -u origin feat/nextjs-phase4a
gh pr create --base main --title "Phase 4a: seed data layer (JSON seed + in-memory stores)" --body "$(cat <<'EOF'
## Summary

Phase 4a of the Next.js migration: replaces three disconnected hardcoded copies of courts + bookings with a single seed-file source loaded into in-memory stores on every API startup. No DB. Date-relative seed (`days_from_today: 1`) keeps demos fresh; container restart resets to clean state.

- Spec: `docs/superpowers/specs/2026-05-17-phase4a-seed-data-layer-design.md`
- Plan: `docs/superpowers/plans/2026-05-17-phase4a-seed-data-layer.md`

## What ships

**Backend (`apps/api/`):**
- `seed/{courts,bookings}.json` — single source of truth, relative dates
- `data/seed_loader.py` + `data/store.py` — pure loader + in-memory singletons
- `schemas/data.py` — Court, Booking, CreateBookingRequest
- `routers/data.py` — GET /courts, GET /courts/{id}, GET /bookings, POST /bookings, POST /bookings/{txn}/cancel
- `main.py` — lifespan hook calls `init_stores()`
- Owner + player agent tools rewritten to read from stores
- Player chat router stops requiring `bookings` snapshot in request body

**Frontend (`apps/web/`):**
- `lib/data-client.ts` — getCourts/getCourt/getBookings/createBooking/cancelBookingApi
- `lib/booking-store.ts` — async hydrate + addBooking; localStorage persist removed
- `components/BookingsHydrator.tsx` — mounts in both layouts, calls hydrate() once
- `lib/mock-data.ts` — repurposed as `FALLBACK_COURTS` (used only when API down)
- Page components fetch via the new client; degrade gracefully to fallback

## Single-instance caveat

In-memory state means Cloud Run (Phase 4c) must run with `--min-instances=1 --max-instances=1`. Phase 5+ adds Postgres if multi-instance is ever needed.

## Tests

| Suite | Result |
|---|---|
| Streamlit `pytest tests/` | 29 / 29 ✅ |
| FastAPI `pytest apps/api` | 53 / 53 ✅ (+21 over Phase 3c) |
| Vitest | 31 / 31 ✅ |
| Playwright | 3 / 3 ✅ |
| `pnpm build` | clean ✅ |

## Test plan (browser smoke before merge)

- [ ] `/player/search` shows 6 courts from API, falls back to FALLBACK_COURTS when API is down
- [ ] `/player/bookings` shows Alex's 3 seed bookings on cold load
- [ ] Player chat: book bbc-01 tomorrow → Confirm → ZP-XXXXX → owner page sees it too
- [ ] Restart uvicorn → cache resets to seed-only
- [ ] Streamlit still runs unchanged at :8501

## What's NOT in this PR

- Postgres / migrations (deferred indefinitely; demo design)
- NextAuth (Phase 4b? TBD)
- Dockerfiles (Phase 4b)
- Cloud Run deploy (Phase 4c)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Return the PR URL.

---

## Out of scope for Phase 4a (do NOT add)

- Postgres, Alembic migrations, persistence across container restarts
- NextAuth / real users (auth-stub still in use)
- Multi-instance consistency
- Streamlit migration to the new data layer
- CSV/Sheets editor experience (JSON only)
- Dockerfiles
- Cloud Run deploy
- New Playwright tests (existing 3 cover the flows)
