# Phase 3c — Chat Agents (FastAPI + Floating Widget) Design

**Date:** 2026-05-17
**Status:** Approved
**Base spec:** `docs/superpowers/specs/2026-05-16-nextjs-migration-design.md`
**Related:**
- `docs/superpowers/specs/2026-05-17-phase3b-fastapi-ai-endpoints-design.md`
- `docs/superpowers/specs/2026-05-10-chat-agents-design.md` (the original Streamlit chat agents)
**Phase position:** 3c of 4 (Phase 1, 2, 3a, 3b merged)

---

## Goal

Port the player and owner chat agents from the legacy Streamlit to FastAPI, ship a floating chat widget on every logged-in page of the Next.js app. Preserve the two-phase write pattern (agent proposes booking → widget confirms via the booking store). One-shot responses (no streaming) for v1.

---

## Architecture

```
Browser
  │
  ├─ /player/* pages (existing)
  └─ /owner/* pages (existing)
       │
       └─ <ChatWidget role={role} />    ← floating 💬 bubble + panel
              │
              ▼  POST /api/chat/{role}  via the Phase-3b proxy
         FastAPI /chat/player  and  /chat/owner
              │
              ├─ Tool-calling loop (chat() in apps/api/ai/client.py)
              ├─ Player tools: search, availability, propose_booking,
              │                list_my, propose_cancel
              └─ Owner tools:  revenue, list_bookings, noshow_risk,
                               demand_forecast, summarize_courts
```

`chat()` is added back to `apps/api/ai/client.py` (we dropped it in Phase 3b because no caller needed it yet). It returns the raw OpenAI ChatCompletion object with tool_calls support.

**Two-phase write preserved.** Player tools `propose_booking` and `propose_cancel` return a draft dict. The agent's reply asks "Confirm to book?". The widget renders Confirm/Cancel buttons below that message. On Confirm, the widget commits directly to `useBookingStore` (no LLM round trip) and appends a synthetic `✅ Booked! ZP-XXXXX.` message to chat history so the agent knows on the next turn.

---

## Repo additions

```
apps/api/
├── ai/client.py                        # MODIFIED — add chat(messages, tools, system)
├── agents/                             # NEW
│   ├── __init__.py
│   ├── player/
│   │   ├── __init__.py
│   │   ├── knowledge.md                # static reference text
│   │   ├── system_prompt.py            # build_system_prompt(user) → str
│   │   ├── tools.py                    # 5 tools + TOOLS list + dispatch()
│   │   └── agent.py                    # run_turn(messages, user, bookings) → response
│   └── owner/
│       ├── __init__.py
│       ├── knowledge.md
│       ├── system_prompt.py
│       ├── tools.py                    # 5 read tools + TOOLS list + dispatch()
│       └── agent.py                    # run_turn(messages, user) → response
├── routers/chat.py                     # NEW — POST /chat/player, POST /chat/owner
├── schemas/chat.py                     # NEW — ChatMessage, ChatPlayerRequest, etc.
└── tests/test_chat_routes.py           # NEW — ~12 tests

apps/web/
├── components/chat/                    # NEW
│   ├── ChatWidget.tsx                  # floating bubble + panel, role-aware
│   ├── ChatBubble.tsx                  # one message with Markdown
│   └── ConfirmDraft.tsx                # Confirm/Cancel buttons for drafts
├── lib/chat-client.ts                  # NEW — chatPlayer(), chatOwner()
├── lib/chat-types.ts                   # NEW — ChatMessage, drafts, response shapes
├── app/player/layout.tsx               # MODIFIED — mount <ChatWidget role="player" />
└── app/owner/layout.tsx                # MODIFIED — mount <ChatWidget role="owner" />
```

---

## Endpoints

| Method | Path | Body | Response |
|---|---|---|---|
| `POST` | `/chat/player` | `{messages, user, bookings}` | `{text, draft, history}` |
| `POST` | `/chat/owner` | `{messages, user}` | `{text, history}` |

### Request / response shapes (Pydantic + TS mirror)

```python
# apps/api/schemas/chat.py

class ChatUser(BaseModel):
    id: int
    name: str

class ChatMessage(BaseModel):
    """Mirrors OpenAI chat message format. Stored verbatim across turns."""
    role: Literal['user', 'assistant', 'tool', 'system']
    content: str | None = None
    tool_calls: list[dict] | None = None      # for assistant turns
    tool_call_id: str | None = None           # for tool turns

class BookingSnapshot(BaseModel):
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
    kind: Literal['booking_draft']
    court_id: str
    court_name: str
    date: str
    time_start: str
    time_end: str
    duration: int
    total_price: int

class CancelDraft(BaseModel):
    kind: Literal['cancel_draft']
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

`history` is the full conversation including assistant `tool_calls` turns and `tool` results. Frontend stores it and sends it back on the next turn. Avoids the frontend ever needing to construct OpenAI message shapes itself.

---

## Tool data sources (Phase 3c — no new DB)

| Tool needs | Source |
|---|---|
| Court catalog | Static `COURTS` constant in `apps/api/agents/player/tools.py` mirroring `apps/web/lib/mock-data.ts:COURTS` |
| Player's bookings | Sent in `bookings` field of request body from `useBookingStore` |
| Owner bookings | Static `OWNER_BOOKINGS` constant in `apps/api/agents/owner/tools.py` (mirror of Phase 3a) |
| Demand forecast | `apps/api/ml/inference.py:get_demand_forecast()` (Phase 3b) |
| No-show risk | `apps/api/ml/inference.py:predict_noshow_risk()` (Phase 3b) |
| Revenue / list_bookings (owner) | Static `OWNER_BOOKINGS` + derived sums |

No persistence in this phase. Phase 4 swaps every constant for a Postgres query.

---

## Frontend widget

`<ChatWidget role={role} />` — floating `💬` bubble bottom-right of every page under `app/player/*` and `app/owner/*` (NOT on `/`, `/player/login`, `/owner-login`).

**Visual:**
- 64px circle launcher (matches the legacy Streamlit polish from PR #4)
- Click → 400×600 panel with header, message list, input, send button
- ✕ in the header to close the panel without losing history

**Behavior:**
- Welcome message seeded on first open. Role-specific:
  - Player: `Hi! I can find courts, check availability, or book you a slot. Try **find badminton near Sukhumvit Friday under 400 baht** or **book bbc-01 tomorrow 6pm**.`
  - Owner: `Hi! Ask me about revenue, no-show risk, or busiest hours. Try **what's my revenue this week?** or **which upcoming bookings are highest risk?**`
- User message bubble right-aligned, lime-green background
- Assistant bubble left-aligned, white card with `react-markdown` (already a dep from Phase 3b)
- Spinner ("…") while the POST is in flight
- If response includes `draft`, render `<ConfirmDraft draft={draft} />` below the assistant text:
  - `booking_draft` → `📌 Confirm booking: <court> on <date> <start>–<end> for ฿<price>?` + Confirm + Cancel buttons
  - `cancel_draft` → `⚠️ Cancel booking <txn_id> at <court> on <date> <start>?` + Confirm + Cancel buttons
- On Confirm:
  - Booking: `useBookingStore.addBookingWithTxn(generateTxnId(), draft)`, append `✅ Booked! ZP-XXXXX.` as assistant message
  - Cancel: `useBookingStore.cancelBooking(draft.txn_id)`, append `✅ Cancelled.` as assistant message
- On Cancel: append `Okay, no changes made.` and clear the draft
- Owner widget has no Confirm UI (owner tools are read-only — no drafts returned)
- History stored in `useState` in the widget component; lost on page refresh (Phase 4 could persist)

---

## Tool-calling loop (server side)

`apps/api/agents/player/agent.py:run_turn(messages, user, bookings)`:

```
loop up to MAX_HOPS:
  response = chat(messages, tools=PLAYER_TOOLS, system=build_system_prompt(user))
  append assistant turn to messages (including tool_calls if any)
  if no tool_calls:
    return {"text": response text, "draft": last_seen_draft, "history": messages}
  for each tool_call:
    result = dispatch(tool_call.name, tool_call.args, user, bookings)
    if result.kind in ('booking_draft', 'cancel_draft'):
      last_seen_draft = result
    append tool result to messages
return {"text": "(agent hop limit reached)", "draft": last_seen_draft, "history": messages}
```

Same pattern in `apps/api/agents/owner/agent.py` but no draft tracking.

`MAX_HOPS = 6` — same cap as the legacy Streamlit version.

---

## Auth

Frontend sends `{user: {id, name}}` derived from the existing `currentUser` (player) or `currentOwner` (owner) auth-stub. FastAPI trusts the body. Phase 4 swaps in NextAuth + JWT verification — only the server-side reading changes; the request body shape stays the same.

---

## Error handling

| Scenario | Behavior |
|---|---|
| FastAPI unreachable | Widget shows `Couldn't reach the assistant. Try again?` inline; chat history preserved; can retry |
| Tool execution exception | Caught inside the agent loop; tool result becomes `{kind: 'error', message}`; agent responds about it |
| LLM API error (Azure 5xx) | FastAPI returns 503 with `{detail: ...}`; widget shows error toast |
| `propose_booking` rejects a taken slot | Returns `{kind: 'error', message: 'Slot not available'}`; agent surfaces the message |
| Draft confirm fails (booking-store write throws) | Existing Phase-2 error path |
| Empty `bookings` from frontend (e.g. localStorage cleared) | Player tools see empty list; `list_my_bookings` returns empty → agent says "You have no bookings" |

---

## Testing

**pytest** for `apps/api/agents/` — ~12 new tests:

- **Player tools** (5 tests):
  - `search_courts` filters by sport
  - `get_availability` returns free slots
  - `propose_booking` returns a draft with correct price
  - `propose_booking` rejects an already-booked slot
  - `propose_cancel` returns a cancel_draft for a valid booking
- **Owner tools** (4 tests):
  - `get_revenue` sums confirmed bookings
  - `rank_noshow_risk` orders by probability
  - `get_demand_forecast` wraps the ML helper
  - `summarize_courts` returns court catalog
- **Chat router** (3 tests, all with mocked OpenAI):
  - `/chat/player` returns text + history when LLM returns no tool_calls
  - `/chat/player` dispatches a tool, returns final text + draft on `propose_booking`
  - `/chat/owner` happy path

All OpenAI calls covered by the existing autouse `conftest.py` fixture. No real Azure hits in tests.

**No new Playwright.** The chat needs Azure configured to exercise end-to-end; stubbing the LLM at the network layer is overkill. Vitest + pytest + manual browser smoke is enough.

**All existing test suites must stay green** (29 Streamlit + 9 FastAPI + 31 Vitest + 3 Playwright).

---

## Out of scope for Phase 3c

- Streaming responses (Vercel AI SDK, SSE) — Phase 4 polish if desired
- Persistent chat history — Phase 4 (needs Postgres `chat_messages` table)
- Real NextAuth — Phase 4
- Tool-execution visibility ("searching courts…" intermediate states) — would need streaming
- Chat on the legacy Streamlit — separate codepath, not touched
- Voice input / multimodal
- Chat history search / export

---

## Success criteria

1. `POST /chat/player` and `POST /chat/owner` return the documented shapes
2. Manual player smoke: ask "find a badminton court", get a list; ask "book bbc-01 tomorrow 6pm", get a draft + confirm UI; confirm → booking appears in `useBookingStore` and shows on `/player/bookings`
3. Manual owner smoke: ask "what's my revenue this week?", get a number; ask "which upcoming bookings are highest risk?", get a ranked list
4. Floating `💬` visible on `/player/*` and `/owner/*` pages, NOT on `/`, `/player/login`, or `/owner-login`
5. `pnpm build` clean
6. All existing test suites stay green

---

## Handoff

When approved, invoke `superpowers:writing-plans` to produce the Phase 3c implementation plan. After this merges, Phase 4 (Postgres + NextAuth + Dockerfiles + Cloud Run) is the final phase.
