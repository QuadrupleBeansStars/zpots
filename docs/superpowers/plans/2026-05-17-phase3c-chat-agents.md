# Phase 3c — Chat Agents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port the player and owner chat agents from legacy Streamlit to FastAPI, ship a floating chat widget on every logged-in Next.js page. One-shot responses; preserve the two-phase write pattern (agent proposes booking → widget commits via the existing `useBookingStore`).

**Architecture:** Backend agents live in `apps/api/agents/{player,owner}/` mirroring the legacy layout. `chat()` is added back to `apps/api/ai/client.py` (we dropped it in Phase 3b). Two new endpoints — `POST /chat/player` and `POST /chat/owner` — wrap the agent loops. Player tools take a `bookings` snapshot in the request body (no backend persistence in 3c). Owner tools read from a hardcoded fixture (mirror of `OWNER_BOOKINGS`). Frontend `<ChatWidget role={role} />` mounts in player + owner layouts, handles welcome message + confirm UI + booking-store integration.

**Tech Stack:** Python 3.11 · FastAPI · Pydantic v2 · pytest · Next.js 16 · TypeScript · Zustand (existing) · react-markdown (added in 3b)

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase3c-chat-agents-design.md`
**Branch:** create `feat/nextjs-phase3c` off main

---

## File structure (end of Phase 3c)

```
apps/api/
├── ai/client.py                        # MODIFIED — add chat()
├── agents/                             # NEW
│   ├── __init__.py
│   ├── player/
│   │   ├── __init__.py
│   │   ├── knowledge.md
│   │   ├── system_prompt.py
│   │   ├── tools.py                    # 5 tools adapted for bookings snapshot
│   │   └── agent.py
│   └── owner/
│       ├── __init__.py
│       ├── knowledge.md
│       ├── system_prompt.py
│       ├── tools.py                    # 5 read tools + _BOOKINGS_FIXTURE
│       └── agent.py
├── schemas/chat.py                     # NEW
├── routers/chat.py                     # NEW
├── main.py                             # MODIFIED — mount chat router
└── tests/
    ├── test_player_agent.py            # NEW
    ├── test_owner_agent.py             # NEW
    └── test_chat_routes.py             # NEW

apps/web/
├── lib/
│   ├── chat-types.ts                   # NEW
│   └── chat-client.ts                  # NEW
├── components/chat/                    # NEW
│   ├── ChatWidget.tsx
│   ├── ChatBubble.tsx
│   └── ConfirmDraft.tsx
├── app/player/layout.tsx               # MODIFIED — mount <ChatWidget role="player" />
└── app/owner/layout.tsx                # MODIFIED — mount <ChatWidget role="owner" />
```

---

## Pre-task setup

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git checkout main && git pull
git checkout -b feat/nextjs-phase3c
```

---

## Task 1: Add `chat()` back to `apps/api/ai/client.py`

**Files:**
- Modify: `apps/api/ai/client.py`

The Phase 3b port dropped `chat()` because no caller needed it. The chat agents need tool-calling, so it comes back.

- [ ] **Step 1: Append to `/Users/nchawanp/Desktop/ZPOTS/apps/api/ai/client.py`** (after `chat_completion()`):

```python


def chat(messages: list[dict], tools: list[dict], system: str):
    """Single tool-calling turn. Returns the raw OpenAI ChatCompletion object.

    `messages` is the running conversation (user/assistant/tool turns). `system`
    is prepended as the first system message. `tools` is OpenAI tool schema
    (`[{"type": "function", "function": {...}}, ...]`).
    """
    full = [{"role": "system", "content": system}] + list(messages)
    return _get_client().chat.completions.create(
        model=_model(),
        messages=full,
        # OpenAI rejects tools=[]; pass None when there are no tools.
        tools=tools or None,
        max_tokens=MAX_TOKENS,
    )
```

- [ ] **Step 2: Smoke import.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT python -c "from ai.client import chat; print('ok')"
```

Expected: `ok`.

- [ ] **Step 3: Verify nothing else broke.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest -q
```

Expected: 9 passed (Phase 3b's existing tests).

- [ ] **Step 4: Commit.**

```bash
git add apps/api/ai/client.py
git commit -m "feat(api): add chat() back to ai/client.py for tool-calling

Was dropped in Phase 3b because no caller used it. Phase 3c chat agents
need it. Verbatim copy from agents/llm_client.py at the repo root."
```

---

## Task 2: Pydantic chat schemas

**Files:**
- Create: `apps/api/schemas/chat.py`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/schemas/chat.py`:**

```python
"""Chat request / response schemas. Used by /chat/player and /chat/owner."""
from typing import Literal

from pydantic import BaseModel


class ChatUser(BaseModel):
    id: int
    name: str


class ChatMessage(BaseModel):
    """Mirrors OpenAI chat message format. Stored verbatim across turns.

    The frontend sends back the history it received from the previous turn
    plus the new user message. The server's loop appends assistant + tool
    turns and returns the updated history.
    """
    role: Literal['user', 'assistant', 'tool', 'system']
    content: str | None = None
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None


class BookingSnapshot(BaseModel):
    """Player's booking from the frontend's useBookingStore."""
    txn_id: str
    court_id: str
    court_name: str
    date: str
    time_start: str
    time_end: str
    duration: int
    total_price: int
    status: Literal['CONFIRMED', 'CANCELLED']


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
    bookings: list[BookingSnapshot] = []


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

- [ ] **Step 2: Smoke import.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT python -c "from schemas.chat import ChatPlayerRequest, ChatPlayerResponse, ChatOwnerRequest, ChatOwnerResponse, BookingDraft, CancelDraft; print('ok')"
```

Expected: `ok`.

- [ ] **Step 3: Commit.**

```bash
git add apps/api/schemas/chat.py
git commit -m "feat(api): Pydantic schemas for chat router

ChatMessage mirrors OpenAI shape. BookingSnapshot carries the player's
useBookingStore snapshot to the backend so tools see fresh data without
the server touching localStorage. BookingDraft/CancelDraft are the
two-phase write outputs."
```

---

## Task 3: Player agent — knowledge + system prompt

**Files:**
- Create: `apps/api/agents/__init__.py` (empty)
- Create: `apps/api/agents/player/__init__.py` (empty)
- Create: `apps/api/agents/player/knowledge.md`
- Create: `apps/api/agents/player/system_prompt.py`

- [ ] **Step 1: Create empty __init__ files.**

```bash
touch /Users/nchawanp/Desktop/ZPOTS/apps/api/agents/__init__.py \
      /Users/nchawanp/Desktop/ZPOTS/apps/api/agents/player/__init__.py
```

- [ ] **Step 2: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/player/knowledge.md`** (verbatim from `legacy/agents/player/knowledge.md`):

```markdown
# ZPOTS Player Knowledge

## Booking basics
- Slots are 1-hour granularity, 07:00–22:00 daily.
- Minimum booking: 1 hour. Maximum: 4 hours.
- Prices shown per hour; total = price_per_hour × duration.
- Payment is collected at the venue on arrival (no online payment in v1).

## Cancellation policy
- Players may cancel any of their own bookings at any time.
- Cancelled slots immediately become available to other players.

## Sports available
Badminton, Football, Padel, Tennis, Basketball.

## Districts
Sukhumvit, Thong Lor, Phaya Thai, Silom, Chatuchak.

## Check-in
A QR code is generated on confirmation; players scan it at the venue. The chatbot does not handle check-in.
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/player/system_prompt.py`:**

```python
from datetime import date
from pathlib import Path

_KB = (Path(__file__).parent / "knowledge.md").read_text()

_TEMPLATE = """You are the ZPOTS player assistant. You help logged-in players find courts, \
check availability, book slots, and manage their existing bookings.

# Current user
- name: {name}
- user_id: {user_id}
- today: {today}

# Reference knowledge
{knowledge}

# Behavior rules
- Be concise. Prefer 1–3 short sentences plus a short list.
- For any booking or cancellation, ALWAYS call `propose_booking` or `propose_cancel` first. \
The user will see Confirm/Cancel buttons; do NOT pretend the action happened until the system tells you it did.
- When showing courts, include name, district, and price per hour.
- All dates are ISO YYYY-MM-DD. Resolve relative dates (today, tomorrow, "Saturday") yourself \
based on the today value above.
- Never invent court ids or prices — call `search_courts` first.
"""


def build_system_prompt(user: dict) -> str:
    return _TEMPLATE.format(
        name=user.get("name", "Player"),
        user_id=user["id"],
        today=date.today().isoformat(),
        knowledge=_KB,
    )
```

- [ ] **Step 4: Smoke import.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT python -c "from agents.player.system_prompt import build_system_prompt; p = build_system_prompt({'id': 1, 'name': 'Alex'}); assert 'Alex' in p and 'Badminton' in p; print('ok', len(p), 'chars')"
```

Expected: `ok <N> chars`.

- [ ] **Step 5: Commit.**

```bash
git add apps/api/agents/__init__.py apps/api/agents/player/
git commit -m "feat(api): player knowledge + system prompt (verbatim from legacy)"
```

---

## Task 4: Player tools (TDD)

**Files:**
- Create: `apps/api/agents/player/tools.py`
- Create: `apps/api/tests/test_player_tools.py`

Adapted from legacy `agents/player/tools.py`. Two changes vs legacy:
1. `COURTS` is a hardcoded constant inside the file (mirror of `apps/web/lib/mock-data.ts:COURTS`), not imported from `data/dummy_data.py`.
2. Tools that need bookings take a `bookings: list[dict]` parameter (passed through by the dispatcher from the request body), not from SQLite.

Also: `propose_cancel` takes `txn_id` (string) instead of `booking_id` (integer) since the frontend's source of truth is `txn_id`.

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_player_tools.py`:

```python
import pytest

from agents.player import tools


SAMPLE_BOOKINGS = [
    {
        "txn_id": "ZP-90001", "court_id": "bbc-01", "court_name": "Bangkok Badminton Center",
        "date": "2099-06-01", "time_start": "18:00", "time_end": "20:00",
        "duration": 2, "total_price": 900, "status": "CONFIRMED",
    },
]


def test_search_courts_filters_by_sport():
    result = tools.search_courts(sport="Badminton")
    assert len(result) >= 1
    assert all(c["sport"] == "Badminton" for c in result)


def test_get_availability_excludes_taken_slots():
    free = tools.get_availability(
        court_id="bbc-01", date_iso="2099-06-01", bookings=SAMPLE_BOOKINGS,
    )
    assert "18:00" not in free
    assert "19:00" not in free
    assert "20:00" in free


def test_get_availability_ignores_other_court():
    free = tools.get_availability(
        court_id="sky-02", date_iso="2099-06-01", bookings=SAMPLE_BOOKINGS,
    )
    assert "18:00" in free


def test_propose_booking_returns_draft_with_price():
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2099-07-01", time_start="18:00", duration=2,
        bookings=[],
    )
    assert draft["kind"] == "booking_draft"
    assert draft["court_name"] == "Bangkok Badminton Center"
    assert draft["total_price"] == 450 * 2
    assert draft["time_end"] == "20:00"


def test_propose_booking_rejects_taken_slot():
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2099-06-01", time_start="18:00", duration=1,
        bookings=SAMPLE_BOOKINGS,
    )
    assert draft["kind"] == "error"
    assert "not available" in draft["message"].lower()


def test_propose_cancel_returns_draft_for_existing():
    draft = tools.propose_cancel(
        user_id=1, txn_id="ZP-90001", bookings=SAMPLE_BOOKINGS,
    )
    assert draft["kind"] == "cancel_draft"
    assert draft["txn_id"] == "ZP-90001"
    assert draft["court_name"] == "Bangkok Badminton Center"


def test_propose_cancel_rejects_unknown_txn():
    draft = tools.propose_cancel(
        user_id=1, txn_id="ZP-99999", bookings=SAMPLE_BOOKINGS,
    )
    assert draft["kind"] == "error"


def test_dispatch_propose_booking_threads_bookings():
    result = tools.dispatch(
        "propose_booking",
        {"court_id": "bbc-01", "date_iso": "2099-08-01", "time_start": "10:00", "duration": 1},
        user_id=1,
        bookings=[],
    )
    assert result["kind"] == "booking_draft"
```

- [ ] **Step 2: Run, expect ImportError.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_player_tools.py -v
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/player/tools.py`:**

```python
"""Player-agent tools. Each tool is a plain Python function the agent loop dispatches.

Tools take an explicit `bookings` snapshot (passed in from the request body)
instead of reading from a database. The frontend's useBookingStore is the
single source of truth for the player's bookings in Phase 3c.
"""
from typing import Any

_HOURS = [f"{h:02d}:00" for h in range(7, 23)]  # 07:00..22:00


# Mirror of apps/web/lib/mock-data.ts:COURTS. Phase 4 swaps for a Postgres query.
COURTS: list[dict] = [
    {
        "id": "bbc-01", "name": "Bangkok Badminton Center",
        "sport": "Badminton", "district": "Sukhumvit",
        "price_per_hour": 450, "rating": 4.8,
    },
    {
        "id": "sky-02", "name": "Skyline Arena Football",
        "sport": "Football", "district": "Thong Lor",
        "price_per_hour": 1200, "rating": 4.7,
    },
    {
        "id": "dwh-03", "name": "Downtown Hoops",
        "sport": "Basketball", "district": "Ari",
        "price_per_hour": 600, "rating": 4.5,
    },
    {
        "id": "pdl-04", "name": "Padel House Sukhumvit",
        "sport": "Padel", "district": "Sukhumvit",
        "price_per_hour": 800, "rating": 4.2,
    },
    {
        "id": "rbs-05", "name": "Royal Bangkok Sports Club",
        "sport": "Tennis", "district": "Pathumwan",
        "price_per_hour": 950, "rating": 5.0,
    },
    {
        "id": "ivh-06", "name": "Impact Volleyball Hall",
        "sport": "Volleyball", "district": "Nonthaburi",
        "price_per_hour": 350, "rating": 4.8,
    },
]


def _find_court(court_id: str) -> dict | None:
    return next((c for c in COURTS if c["id"] == court_id), None)


def _booked_starts(court_id: str, date_iso: str, bookings: list[dict]) -> set[str]:
    """Compute taken HH:00 starts for a court on a date from CONFIRMED bookings."""
    taken: set[str] = set()
    for b in bookings:
        if b.get("court_id") != court_id or b.get("date") != date_iso:
            continue
        if b.get("status") != "CONFIRMED":
            continue
        start_h = int(b["time_start"].split(":")[0])
        for i in range(int(b.get("duration", 1))):
            taken.add(f"{start_h + i:02d}:00")
    return taken


def search_courts(
    sport: str | None = None,
    district: str | None = None,
    max_price: int | None = None,
) -> list[dict]:
    out = []
    for c in COURTS:
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


def get_availability(court_id: str, date_iso: str, bookings: list[dict]) -> list[str]:
    """Return the list of free hour-start times (HH:00) for a court on a given date."""
    booked = _booked_starts(court_id, date_iso, bookings)
    return [h for h in _HOURS if h not in booked]


def list_my_bookings(user_id: int, bookings: list[dict]) -> list[dict]:
    """Return the player's bookings (the snapshot from the frontend)."""
    return [
        {
            "txn_id": b["txn_id"], "court_id": b["court_id"], "court_name": b["court_name"],
            "date": b["date"], "time_start": b["time_start"], "time_end": b["time_end"],
            "total_price": b["total_price"], "status": b["status"],
        }
        for b in bookings
    ]


def propose_booking(
    user_id: int, court_id: str, date_iso: str, time_start: str, duration: int,
    bookings: list[dict],
) -> dict:
    court = _find_court(court_id)
    if court is None:
        return {"kind": "error", "message": f"Unknown court id {court_id}"}

    start_h = int(time_start.split(":")[0])
    needed = {f"{start_h + i:02d}:00" for i in range(duration)}
    booked = _booked_starts(court_id, date_iso, bookings)
    if needed & booked:
        return {"kind": "error", "message": f"Slot is not available on {date_iso} at {time_start}."}

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


def propose_cancel(user_id: int, txn_id: str, bookings: list[dict]) -> dict:
    booking = next((b for b in bookings if b.get("txn_id") == txn_id), None)
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


def dispatch(name: str, args: dict, user_id: int, bookings: list[dict]) -> Any:
    """Run a tool by name. Threads user_id + bookings into tools that need them."""
    if name == "search_courts":
        return search_courts(**args)
    if name == "get_availability":
        return get_availability(bookings=bookings, **args)
    if name == "list_my_bookings":
        return list_my_bookings(user_id=user_id, bookings=bookings)
    if name == "propose_booking":
        return propose_booking(user_id=user_id, bookings=bookings, **args)
    if name == "propose_cancel":
        return propose_cancel(user_id=user_id, bookings=bookings, **args)
    return {"kind": "error", "message": f"Unknown tool {name}"}
```

- [ ] **Step 4: Run tests, expect 8 passed (the 7 in this file + 1 dispatch test).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_player_tools.py -v
```

- [ ] **Step 5: Commit.**

```bash
git add apps/api/agents/player/tools.py apps/api/tests/test_player_tools.py
git commit -m "feat(api): player chat tools (TDD)

search_courts, get_availability, list_my_bookings, propose_booking,
propose_cancel. Adapted from legacy agents/player/tools.py — COURTS
hardcoded in file, bookings snapshot threaded from request body, no
SQLite. propose_cancel takes txn_id (string) instead of integer id."
```

---

## Task 5: Player agent loop (TDD)

**Files:**
- Create: `apps/api/agents/player/agent.py`
- Create: `apps/api/tests/test_player_agent.py`

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_player_agent.py`:

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
    fake = mock_openai_client
    fake.chat.completions.create.return_value = _msg(content="Hi Alex!")

    result = agent.run_turn(
        messages=[{"role": "user", "content": "hello"}],
        user={"id": 1, "name": "Alex"},
        bookings=[],
    )

    assert result["text"] == "Hi Alex!"
    assert result["draft"] is None
    assert len(result["history"]) == 2  # user + assistant


def test_run_turn_dispatches_tool_then_responds(monkeypatch, mock_openai_client):
    fake = mock_openai_client
    fake.chat.completions.create.side_effect = [
        _msg(tool_calls=[_tool_call("search_courts", '{"sport": "Badminton"}')]),
        _msg(content="Found Bangkok Badminton Center."),
    ]

    result = agent.run_turn(
        messages=[{"role": "user", "content": "find badminton"}],
        user={"id": 1, "name": "Alex"},
        bookings=[],
    )

    assert "Bangkok Badminton" in result["text"]
    assert fake.chat.completions.create.call_count == 2


def test_run_turn_surfaces_booking_draft(monkeypatch, mock_openai_client):
    fake = mock_openai_client
    fake.chat.completions.create.side_effect = [
        _msg(tool_calls=[_tool_call(
            "propose_booking",
            '{"court_id": "bbc-01", "date_iso": "2099-06-01", "time_start": "18:00", "duration": 1}',
        )]),
        _msg(content="Confirm to book?"),
    ]

    result = agent.run_turn(
        messages=[{"role": "user", "content": "book bbc-01 tomorrow 6pm"}],
        user={"id": 1, "name": "Alex"},
        bookings=[],
    )

    assert result["draft"] is not None
    assert result["draft"]["kind"] == "booking_draft"
    assert result["draft"]["court_name"] == "Bangkok Badminton Center"
```

- [ ] **Step 2: Run, expect ImportError.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_player_agent.py -v
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/player/agent.py`:**

```python
"""Player agent tool-calling loop (OpenAI / Azure OpenAI)."""
import json

from ai.client import chat
from agents.player import tools as player_tools
from agents.player.system_prompt import build_system_prompt

MAX_HOPS = 6  # safety cap so the model can't loop forever


def run_turn(
    messages: list[dict], user: dict, bookings: list[dict],
) -> dict:
    """Run one user turn through the agent.

    `messages` is the full history (user / assistant / tool turns). The caller
    is responsible for appending the new user message before invoking.

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
                tc.function.name, args, user_id=user["id"], bookings=bookings,
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

- [ ] **Step 4: Run tests, expect 3 passed.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_player_agent.py -v
```

- [ ] **Step 5: Commit.**

```bash
git add apps/api/agents/player/agent.py apps/api/tests/test_player_agent.py
git commit -m "feat(api): player agent run_turn (tool-calling loop)

Ported from legacy/agents/player/agent.py. Signature changed: takes
full message history + bookings snapshot, returns text + draft +
history. MAX_HOPS=6 safety cap unchanged. 3 tests with mocked LLM."
```

---

## Task 6: Owner agent — knowledge + system prompt + __init__

**Files:**
- Create: `apps/api/agents/owner/__init__.py` (empty)
- Create: `apps/api/agents/owner/knowledge.md`
- Create: `apps/api/agents/owner/system_prompt.py`

- [ ] **Step 1: Create empty marker.**

```bash
touch /Users/nchawanp/Desktop/ZPOTS/apps/api/agents/owner/__init__.py
```

- [ ] **Step 2: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/owner/knowledge.md`** (verbatim from legacy):

```markdown
# ZPOTS Owner Knowledge

## What you can answer
- Revenue: today, this week, this month — sums of `total_price` from confirmed bookings.
- Bookings: list and filter by date range, court, or status.
- No-show risk: rank upcoming bookings by predicted risk (Low / Medium / High).
- Demand forecast: 7-day hourly predicted bookings from the trained Random Forest.
- Court summaries: name, sport, district, price per hour, current utilization.

## What you cannot do in v1
- You cannot change pricing, block slots, or edit court details from chat. Direct the owner to the relevant Streamlit page (Manage Slots, Pricing) for those.
- You cannot summarize player feedback — it is not yet stored in the database.

## ML model caveats
- No-show predictor is a Random Forest with ROC AUC 0.59. Tier accuracy: Low ~23% miss, Medium ~30% miss, High ~36% miss. Treat as directional, not deterministic.
- Demand forecast is a Random Forest regressor with MAE 0.57 bookings/hour. Use it for trend, not exact counts.

## Booking data shape
- Statuses: CONFIRMED (default), CANCELLED.
- Hours stored as HH:00 strings; date as YYYY-MM-DD.
- `total_price` is in THB.
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/owner/system_prompt.py`:**

```python
from datetime import date
from pathlib import Path

_KB = (Path(__file__).parent / "knowledge.md").read_text()

_TEMPLATE = """You are the ZPOTS owner assistant. You help logged-in venue owners understand \
their business: revenue, bookings, no-show risk, demand forecast, and court status.

# Current owner
- name: {name}
- user_id: {user_id}
- today: {today}

# Reference knowledge
{knowledge}

# Behavior rules
- Be concise. Lead with the answer; follow with 1-3 short supporting points.
- Format money as "฿1,234" (Thai baht, comma-separated thousands).
- All dates are ISO YYYY-MM-DD. Resolve relative dates ("this week", "today", "next Saturday") yourself based on the today value above. "This week" = Monday through Sunday containing today.
- For risk rankings, name specific bookings (court + date + time + player name).
- Never invent numbers. If a tool returns empty results, say so plainly.
- You have NO write tools. If asked to change pricing or block a slot, tell the user to use the Pricing or Manage Slots pages.
"""


def build_system_prompt(user: dict) -> str:
    return _TEMPLATE.format(
        name=user.get("name", "Owner"),
        user_id=user["id"],
        today=date.today().isoformat(),
        knowledge=_KB,
    )
```

- [ ] **Step 4: Smoke import.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT python -c "from agents.owner.system_prompt import build_system_prompt; p = build_system_prompt({'id': 3, 'name': 'Venue Admin'}); assert 'Venue Admin' in p; print('ok')"
```

- [ ] **Step 5: Commit.**

```bash
git add apps/api/agents/owner/
git commit -m "feat(api): owner knowledge + system prompt (verbatim from legacy)"
```

---

## Task 7: Owner tools (TDD)

**Files:**
- Create: `apps/api/agents/owner/tools.py`
- Create: `apps/api/tests/test_owner_tools.py`

Adapted from legacy. Single change: a `_BOOKINGS_FIXTURE` constant replaces the SQLite query. Phase 4 swaps for Postgres.

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_owner_tools.py`:

```python
from agents.owner import tools


def test_get_revenue_sums_confirmed_in_range():
    result = tools.get_revenue(date_from="2099-01-01", date_to="2099-12-31")
    assert result["total_thb"] == 0  # nothing in 2099
    assert result["bookings"] == 0


def test_get_revenue_excludes_cancelled():
    # The fixture is the same for all tests, so just verify the function
    # respects status. Use a known-empty range:
    result = tools.get_revenue(date_from="1900-01-01", date_to="1900-12-31")
    assert result["total_thb"] == 0


def test_list_bookings_filters_by_court():
    fixture_court = tools._BOOKINGS_FIXTURE[0]["court_id"]
    rows = tools.list_bookings(court_id=fixture_court)
    assert all(r["court_id"] == fixture_court for r in rows)


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
    assert len(out) <= 5  # might be 0 if artifact missing


def test_rank_noshow_risk_returns_sorted_or_empty():
    out = tools.rank_noshow_risk(limit=5)
    assert isinstance(out, list)
    if len(out) >= 2:
        # Sorted high → low by probability
        probs = [r["risk_probability"] for r in out]
        assert probs == sorted(probs, reverse=True)


def test_dispatch_summarize_courts():
    result = tools.dispatch("summarize_courts", {}, user_id=3)
    assert isinstance(result, list)
    assert len(result) > 0
```

- [ ] **Step 2: Run, expect ImportError.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_owner_tools.py -v
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/owner/tools.py`:**

```python
"""Owner-agent tools (read-only).

In Phase 3c there is no Postgres yet, so the tools read from a hardcoded
`_BOOKINGS_FIXTURE` representing the venue's recent activity. Phase 4 swaps
this for a real query.
"""
from datetime import date as _date, timedelta as _td
from typing import Any

from ml.inference import predict_noshow_risk
from ml.inference import get_demand_forecast as _get_demand_df

_LIST_BOOKINGS_MAX = 200


# Mirror of the legacy SQLite seed data plus some upcoming bookings so the
# owner agent has interesting things to rank/summarize. Phase 4 swaps for
# a Postgres query.
def _upcoming(days_ahead: int, **overrides) -> dict:
    d = (_date.today() + _td(days=days_ahead)).isoformat()
    base = {
        "txn_id": "ZP-00000", "player_name": "Demo",
        "court_id": "bbc-01", "court_name": "Bangkok Badminton Center",
        "date": d, "time_start": "18:00", "time_end": "19:00",
        "duration": 1, "total_price": 450, "status": "CONFIRMED",
    }
    base.update(overrides)
    return base


_BOOKINGS_FIXTURE: list[dict] = [
    _upcoming(1, txn_id="ZP-90101", player_name="Alex Siriwan",
              court_id="bbc-01", court_name="Bangkok Badminton Center",
              time_start="18:00", time_end="20:00", duration=2, total_price=900),
    _upcoming(2, txn_id="ZP-90102", player_name="Narin Kositchai",
              court_id="sky-02", court_name="Skyline Arena Football",
              time_start="20:00", time_end="22:00", duration=2, total_price=2400),
    _upcoming(3, txn_id="ZP-90103", player_name="Maya Chen",
              court_id="pdl-04", court_name="Padel House Sukhumvit",
              time_start="07:00", time_end="08:00", duration=1, total_price=800),
    _upcoming(4, txn_id="ZP-90104", player_name="Tomás Vega",
              court_id="dwh-03", court_name="Downtown Hoops",
              time_start="19:00", time_end="21:00", duration=2, total_price=1200),
    _upcoming(5, txn_id="ZP-90105", player_name="Priya Singh",
              court_id="rbs-05", court_name="Royal Bangkok Sports Club",
              time_start="16:00", time_end="17:00", duration=1, total_price=950),
    _upcoming(0, txn_id="ZP-90100", player_name="Marcus Lee",
              court_id="bbc-01", court_name="Bangkok Badminton Center",
              time_start="20:00", time_end="21:00", duration=1, total_price=450),
]


COURTS: list[dict] = [
    {"id": "bbc-01", "name": "Bangkok Badminton Center", "sport": "Badminton",
     "district": "Sukhumvit", "price_per_hour": 450, "utilization": 88},
    {"id": "sky-02", "name": "Skyline Arena Football", "sport": "Football",
     "district": "Thong Lor", "price_per_hour": 1200, "utilization": 74},
    {"id": "dwh-03", "name": "Downtown Hoops", "sport": "Basketball",
     "district": "Ari", "price_per_hour": 600, "utilization": 68},
    {"id": "pdl-04", "name": "Padel House Sukhumvit", "sport": "Padel",
     "district": "Sukhumvit", "price_per_hour": 800, "utilization": 79},
    {"id": "rbs-05", "name": "Royal Bangkok Sports Club", "sport": "Tennis",
     "district": "Pathumwan", "price_per_hour": 950, "utilization": 92},
    {"id": "ivh-06", "name": "Impact Volleyball Hall", "sport": "Volleyball",
     "district": "Nonthaburi", "price_per_hour": 350, "utilization": 55},
]


def get_revenue(date_from: str, date_to: str) -> dict:
    total = 0
    n = 0
    for b in _BOOKINGS_FIXTURE:
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
    rows = list(_BOOKINGS_FIXTURE)
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


def _court_lookup(court_id: str) -> dict:
    return next((c for c in COURTS if c["id"] == court_id), {})


def _hydrate_for_noshow(b: dict) -> dict:
    court = _court_lookup(b["court_id"])
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
            "utilization_pct": c.get("utilization"),
        }
        for c in COURTS
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
    """Owner dispatcher. user_id is accepted for parity with the player one but unused."""
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
git commit -m "feat(api): owner chat tools (TDD)

get_revenue, list_bookings, rank_noshow_risk, get_demand_forecast,
summarize_courts. Adapted from legacy — SQLite query replaced with a
hardcoded _BOOKINGS_FIXTURE (6 upcoming bookings). ML helpers reuse
ml/inference.py from Phase 3b. 8 tests."
```

---

## Task 8: Owner agent loop (TDD)

**Files:**
- Create: `apps/api/agents/owner/agent.py`
- Create: `apps/api/tests/test_owner_agent.py`

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_owner_agent.py`:

```python
from unittest.mock import MagicMock

from agents.owner import agent


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


def test_run_turn_returns_text_when_no_tool_calls(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value = _msg(content="Hi Owner")
    result = agent.run_turn(
        messages=[{"role": "user", "content": "hello"}],
        user={"id": 3, "name": "Venue Admin"},
    )
    assert result["text"] == "Hi Owner"
    assert "history" in result


def test_run_turn_dispatches_summarize_courts(mock_openai_client):
    mock_openai_client.chat.completions.create.side_effect = [
        _msg(tool_calls=[_tool_call("summarize_courts", "{}")]),
        _msg(content="You operate 6 courts across Bangkok."),
    ]
    result = agent.run_turn(
        messages=[{"role": "user", "content": "how many courts?"}],
        user={"id": 3, "name": "Venue Admin"},
    )
    assert "6 courts" in result["text"]
    assert mock_openai_client.chat.completions.create.call_count == 2
```

- [ ] **Step 2: Run, expect ImportError.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_owner_agent.py -v
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/agents/owner/agent.py`:**

```python
"""Owner agent tool-calling loop (read-only)."""
import json

from ai.client import chat
from agents.owner import tools as owner_tools
from agents.owner.system_prompt import build_system_prompt

MAX_HOPS = 6


def run_turn(messages: list[dict], user: dict) -> dict:
    """Run one user turn. Returns {"text": str, "history": list[dict]}."""
    messages = list(messages)
    system = build_system_prompt(user)

    for _ in range(MAX_HOPS):
        response = chat(messages, tools=owner_tools.TOOLS, system=system)
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
            return {"text": (msg.content or "").strip(), "history": messages}

        for tc in msg.tool_calls or []:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            result = owner_tools.dispatch(tc.function.name, args, user_id=user["id"])
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, default=str),
            })

    return {"text": "(agent hop limit reached)", "history": messages}
```

- [ ] **Step 4: Run tests, expect 2 passed.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_owner_agent.py -v
```

- [ ] **Step 5: Commit.**

```bash
git add apps/api/agents/owner/agent.py apps/api/tests/test_owner_agent.py
git commit -m "feat(api): owner agent run_turn (tool-calling loop, no drafts)"
```

---

## Task 9: Chat router (TDD) + mount in main

**Files:**
- Create: `apps/api/routers/chat.py`
- Create: `apps/api/tests/test_chat_routes.py`
- Modify: `apps/api/main.py`

- [ ] **Step 1: Write failing tests.** Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/tests/test_chat_routes.py`:

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
        "bookings": [],
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
    assert "draft" not in body  # owner response has no draft field
```

- [ ] **Step 2: Run, expect 404 (router not mounted).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_chat_routes.py -v
```

- [ ] **Step 3: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/routers/chat.py`:**

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
        bookings=[b.model_dump() for b in req.bookings],
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

- [ ] **Step 4: Mount the router in `/Users/nchawanp/Desktop/ZPOTS/apps/api/main.py`.** Replace the file content with:

```python
from fastapi import FastAPI

from routers import ai, chat, health, ml

app = FastAPI(
    title="ZPOTS API",
    description="OpenAI/Azure helpers + ML inference + chat agents for the Next.js frontend.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(ai.router)
app.include_router(ml.router)
app.include_router(chat.router)
```

- [ ] **Step 5: Run all api tests, expect everything green.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest -v
```

Expected pass count: 1 (health) + 5 (ai routes) + 3 (ml routes) + 8 (player tools) + 3 (player agent) + 8 (owner tools) + 2 (owner agent) + 2 (chat routes) = **32 passed**.

- [ ] **Step 6: Commit.**

```bash
git add apps/api/routers/chat.py apps/api/main.py apps/api/tests/test_chat_routes.py
git commit -m "feat(api): /chat/player and /chat/owner routes (TDD)

Mount chat router in main.py. Routes wrap the agent run_turn() loops
with Pydantic request/response schemas. 32 api tests total passing."
```

---

## Task 10: Frontend chat types + chat client

**Files:**
- Create: `apps/web/lib/chat-types.ts`
- Create: `apps/web/lib/chat-client.ts`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/lib/chat-types.ts`:**

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

export type BookingSnapshot = {
  txn_id: string;
  court_id: string;
  court_name: string;
  date: string;
  time_start: string;
  time_end: string;
  duration: number;
  total_price: number;
  status: 'CONFIRMED' | 'CANCELLED';
};

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
  bookings: BookingSnapshot[];
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

- [ ] **Step 2: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/lib/chat-client.ts`:**

```ts
import type {
  ChatOwnerRequest, ChatOwnerResponse,
  ChatPlayerRequest, ChatPlayerResponse,
} from './chat-types';

async function postJson<TReq, TRes>(path: string, body: TReq): Promise<TRes> {
  const res = await fetch(`/api/${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST /api/${path} failed: ${res.status}`);
  return res.json();
}

export const chatPlayer = (req: ChatPlayerRequest) =>
  postJson<ChatPlayerRequest, ChatPlayerResponse>('chat/player', req);

export const chatOwner = (req: ChatOwnerRequest) =>
  postJson<ChatOwnerRequest, ChatOwnerResponse>('chat/owner', req);
```

- [ ] **Step 3: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

- [ ] **Step 4: Commit.**

```bash
git add apps/web/lib/chat-types.ts apps/web/lib/chat-client.ts
git commit -m "feat(web): chat types + typed client helpers

Mirrors apps/api/schemas/chat.py. chatPlayer() and chatOwner() POST
through the existing /api/[...path] proxy."
```

---

## Task 11: ChatBubble + ConfirmDraft components

**Files:**
- Create: `apps/web/components/chat/ChatBubble.tsx`
- Create: `apps/web/components/chat/ConfirmDraft.tsx`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/chat/ChatBubble.tsx`:**

```tsx
import Markdown from 'react-markdown';

type Props = {
  role: 'user' | 'assistant';
  children: React.ReactNode;
};

export function ChatBubble({ role, children }: Props) {
  const isUser = role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={[
          'max-w-[85%] rounded-card px-3 py-2 text-sm',
          isUser
            ? 'bg-zpots-lime text-zpots-forest'
            : 'bg-white border border-zpots-mint text-zpots-ink',
        ].join(' ')}
      >
        {typeof children === 'string' ? (
          <div className="prose prose-sm max-w-none whitespace-pre-wrap">
            <Markdown>{children}</Markdown>
          </div>
        ) : (
          children
        )}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/chat/ConfirmDraft.tsx`:**

```tsx
'use client';
import { Button } from '@/components/Button';
import { formatPrice } from '@/lib/format';
import type { ChatDraft } from '@/lib/chat-types';

type Props = {
  draft: ChatDraft;
  onConfirm: () => void;
  onCancel: () => void;
  disabled?: boolean;
};

export function ConfirmDraft({ draft, onConfirm, onCancel, disabled }: Props) {
  return (
    <div className="zpots-card-surface p-3 mt-1 text-sm">
      {draft.kind === 'booking_draft' ? (
        <div className="text-zpots-ink">
          📌 Confirm booking:{' '}
          <strong>{draft.court_name}</strong> on {draft.date} {draft.time_start}–{draft.time_end} for{' '}
          <strong>{formatPrice(draft.total_price)}</strong>?
        </div>
      ) : (
        <div className="text-zpots-ink">
          ⚠️ Cancel booking{' '}
          <strong>{draft.txn_id}</strong> at {draft.court_name} on {draft.date} {draft.time_start}?
        </div>
      )}
      <div className="flex gap-2 mt-2">
        <Button variant="primary" onClick={onConfirm} disabled={disabled}>
          Confirm
        </Button>
        <Button variant="secondary" onClick={onCancel} disabled={disabled}>
          Cancel
        </Button>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

- [ ] **Step 4: Commit.**

```bash
git add apps/web/components/chat/ChatBubble.tsx apps/web/components/chat/ConfirmDraft.tsx
git commit -m "feat(web): ChatBubble + ConfirmDraft components

ChatBubble renders user/assistant messages with markdown for assistant.
ConfirmDraft shows the booking/cancel summary with Confirm/Cancel."
```

---

## Task 12: ChatWidget component

**Files:**
- Create: `apps/web/components/chat/ChatWidget.tsx`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/components/chat/ChatWidget.tsx`:**

```tsx
'use client';
import { useEffect, useRef, useState } from 'react';

import { Button } from '@/components/Button';
import { Icon } from '@/components/Icon';
import { ChatBubble } from './ChatBubble';
import { ConfirmDraft } from './ConfirmDraft';
import { currentUser, currentOwner } from '@/lib/auth-stub';
import { useBookingStore, generateTxnId } from '@/lib/booking-store';
import { chatOwner, chatPlayer } from '@/lib/chat-client';
import type {
  BookingDraft, CancelDraft, ChatDraft, ChatMessage,
} from '@/lib/chat-types';

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
  const bookings = useBookingStore((s) => s.bookings);
  const addBooking = useBookingStore((s) => s.addBookingWithTxn);
  const cancelBooking = useBookingStore((s) => s.cancelBooking);

  // Auto-scroll to bottom on new messages.
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, busy]);

  // Visible-only messages (drop tool turns from the rendered list).
  const visible = messages.filter((m) => m.role === 'user' || (m.role === 'assistant' && m.content));

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
        const res = await chatPlayer({
          messages: nextMessages,
          user,
          bookings: bookings.map((b) => ({
            txn_id: b.txn_id, court_id: b.court_id, court_name: b.court_name,
            date: b.date, time_start: b.time_start, time_end: b.time_end,
            duration: b.duration, total_price: b.total_price, status: b.status,
          })),
        });
        // Server-returned history already contains the final assistant turn —
        // don't append res.text again or it'll show twice.
        setMessages(res.history);
        setPendingDraft(res.draft);
      } else {
        const res = await chatOwner({ messages: nextMessages, user });
        // Same dedupe as the player branch above.
        setMessages(res.history);
      }
    } catch (e) {
      setError("Couldn't reach the assistant. Try again?");
    } finally {
      setBusy(false);
    }
  }

  function handleConfirm() {
    if (!pendingDraft) return;
    if (pendingDraft.kind === 'booking_draft') {
      const txn = generateTxnId();
      addBooking(txn, {
        court_id: pendingDraft.court_id,
        court_name: pendingDraft.court_name,
        date: pendingDraft.date,
        time_start: pendingDraft.time_start,
        time_end: pendingDraft.time_end,
        duration: pendingDraft.duration,
        total_price: pendingDraft.total_price,
      });
      setMessages((m) => [...m, { role: 'assistant', content: `✅ Booked! Transaction id **${txn}**.` }]);
    } else {
      cancelBooking(pendingDraft.txn_id);
      setMessages((m) => [...m, { role: 'assistant', content: '✅ Cancelled.' }]);
    }
    setPendingDraft(null);
  }

  function handleDecline() {
    setMessages((m) => [...m, { role: 'assistant', content: 'Okay, no changes made.' }]);
    setPendingDraft(null);
  }

  const welcome = role === 'player' ? PLAYER_WELCOME : OWNER_WELCOME;

  return (
    <>
      {/* Floating launcher */}
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-label={open ? 'Close chat' : 'Open chat'}
        className="fixed bottom-6 right-6 z-50 w-16 h-16 rounded-full bg-zpots-lime text-zpots-forest shadow-card-lift flex items-center justify-center text-2xl hover:scale-105 transition-transform"
      >
        {open ? '✕' : '💬'}
      </button>

      {/* Panel */}
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
            {visible.length === 0 && (
              <ChatBubble role="assistant">{welcome}</ChatBubble>
            )}
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
            {busy && (
              <div className="text-xs text-zpots-muted italic px-2">Thinking…</div>
            )}
            {error && (
              <div className="text-xs text-red-700 px-2">{error}</div>
            )}
          </div>

          <form
            className="border-t border-zpots-mint p-2 flex gap-2"
            onSubmit={(e) => { e.preventDefault(); send(); }}
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

- [ ] **Step 2: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

If the `addBookingWithTxn` signature in `apps/web/lib/booking-store.ts` is `(txn, draft) => string` (Phase 2 pattern), this code is correct. If it differs, adapt the call MINIMALLY.

- [ ] **Step 3: Commit.**

```bash
git add apps/web/components/chat/ChatWidget.tsx
git commit -m "feat(web): ChatWidget floating bubble + panel, role-aware

64px launcher bottom-right. 400×600 panel with welcome message, message
list, confirm UI for player drafts, input field, busy spinner, error
banner. Player drafts commit via useBookingStore directly (no LLM
round trip); owner has no confirm UI."
```

---

## Task 13: Mount widget in player + owner layouts

**Files:**
- Modify: `apps/web/app/player/layout.tsx`
- Modify: `apps/web/app/owner/layout.tsx`

- [ ] **Step 1: Open `/Users/nchawanp/Desktop/ZPOTS/apps/web/app/player/layout.tsx`** and add the import + mount. Final content should look like (preserve any other existing wrapper from Phase 2):

```tsx
import { PlayerTopBar } from '@/components/PlayerTopBar';
import { ChatWidget } from '@/components/chat/ChatWidget';

export default function PlayerLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <PlayerTopBar />
      <main className="max-w-[1200px] mx-auto px-6 py-6">{children}</main>
      <ChatWidget role="player" />
    </>
  );
}
```

Adjust to match whatever the existing layout is — the change is: import `ChatWidget` and render `<ChatWidget role="player" />` at the end.

- [ ] **Step 2: Open `/Users/nchawanp/Desktop/ZPOTS/apps/web/app/owner/layout.tsx`** and do the same:

```tsx
import { OwnerSidebar } from '@/components/OwnerSidebar';
import { ChatWidget } from '@/components/chat/ChatWidget';

export default function OwnerLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-zpots-surface">
      <OwnerSidebar />
      <main className="flex-1 px-8 py-6 max-w-[1400px]">{children}</main>
      <ChatWidget role="owner" />
    </div>
  );
}
```

Same change: import + render `<ChatWidget role="owner" />` at the end. Keep the existing structure.

- [ ] **Step 3: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

- [ ] **Step 4: Commit.**

```bash
git add apps/web/app/player/layout.tsx apps/web/app/owner/layout.tsx
git commit -m "feat(web): mount ChatWidget in player + owner layouts

Floating 💬 bubble now appears on every /player/* and /owner/* page.
Not present on the landing (/), player-login, or owner-login."
```

---

## Task 14: Final smoke + open PR

- [ ] **Step 1: Run all automated checks.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS

# Streamlit
conda run -n MADT pytest tests/ -q

# FastAPI
cd apps/api && conda run -n MADT pytest -q && cd ..

# Vitest + Playwright
cd apps/web && pnpm test:unit && pnpm build && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm test
cd ../..
```

Expected:
- Streamlit pytest: 29 passed
- FastAPI pytest: 32 passed (1 health + 5 ai + 3 ml + 8 player_tools + 3 player_agent + 8 owner_tools + 2 owner_agent + 2 chat_routes)
- Vitest: 31 passed
- `pnpm build`: exit 0
- Playwright: 3 passed (landing + player-flow + owner-flow — unchanged)

- [ ] **Step 2: Manual browser smoke (requires `dev.env` Azure vars).**

Two terminals:

```bash
# Terminal A
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT uvicorn main:app --reload --port 8000

# Terminal B
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm dev
```

Open http://localhost:3000 and verify:

1. Log in as player → land on `/player` → 💬 button bottom-right
2. Click 💬 → panel opens with welcome message
3. Type "find a badminton court under 500 baht" → press Send → assistant returns court list
4. Type "book bbc-01 tomorrow 6pm for 1 hour" → assistant proposes draft + Confirm/Cancel buttons appear
5. Click Confirm → "✅ Booked! ZP-XXXXX." appears; navigate to `/player/bookings` → new booking visible
6. Type "show my bookings" → assistant lists them (including the new one)
7. Log out, log in as owner → land on `/owner` → 💬 button visible
8. Click 💬 → owner welcome
9. Type "what's my revenue this week?" → assistant returns a number
10. Type "which upcoming bookings are highest risk?" → assistant ranks bookings
11. Verify 💬 is NOT visible on `/` (landing), `/player/login`, `/owner-login`

- [ ] **Step 3: Confirm legacy Streamlit still runs unchanged.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS && conda run -n MADT streamlit run app.py
```

- [ ] **Step 4: Push + open PR.**

```bash
git push -u origin feat/nextjs-phase3c
gh pr create --base main --title "Phase 3c: chat agents + floating widget" --body-file ...
```

PR body must include:
- Link to the spec + plan
- Test counts (Streamlit 29, FastAPI 32, Vitest 31, Playwright 3)
- Note that 3c is the last sub-phase of 3; Phase 4 is Postgres + NextAuth + Cloud Run
- Confirmation that legacy Streamlit + Phase 1/2/3a/3b all still work
- That Azure env vars in `dev.env` are needed for the chat to actually return content

---

## Out of scope for Phase 3c (do NOT add)

- Streaming responses — Phase 4 polish if desired
- Persistent chat history — Phase 4 (needs Postgres `chat_messages` table)
- Real NextAuth — Phase 4
- Tool-execution visibility ("searching courts…" intermediate states)
- Chat on the legacy Streamlit — separate codepath, untouched
- Voice input / multimodal
- Chat history search / export
- New Playwright tests
- Cancel button on the chat input itself (Confirm/Cancel is for drafts only)
