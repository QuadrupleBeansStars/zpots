# ZPOTS Next.js Migration — Design

**Date:** 2026-05-16
**Status:** Approved — decompose into per-phase specs+plans
**Base brief:** `ZPOTS Design System/handoff/MIGRATION.md` and `ZPOTS Design System/handoff/CLAUDE.md`

This document is a **delta spec**. It references the existing handoff brief as the source of truth for stack, route map, component map, and gotchas. It captures only what has changed since the brief was written and the sub-project boundaries we'll work in.

---

## Goal

Migrate ZPOTS from Streamlit to a production **Next.js 14 + FastAPI** stack, using the design system and reference TSX components already prepared in `ZPOTS Design System/handoff/`. End state: pixel-accurate to the Stitch mockups, deployed to Vercel (frontend) + Railway (backend), with the legacy Streamlit kept runnable in `legacy/` until Phase 3 ships green.

---

## Stack — confirmed unchanged from MIGRATION.md

| Layer | Choice |
|---|---|
| Frontend | Next.js 14 App Router, TypeScript strict, Tailwind, `pnpm` |
| Backend | FastAPI, Python 3.11, SQLAlchemy 2.0, Pydantic v2 |
| Database | Postgres (Supabase dev → managed in prod) |
| Auth | NextAuth v5, **email magic-link only** (no Google for v1) |
| Charts | Recharts |
| QR | `qrcode.react` (client-side) |
| Data fetching | TanStack Query + typed fetch client |
| Deploy | Vercel (web) + Railway (api) |

---

## Repo layout

Monorepo, single git history:

```
.
├── apps/
│   ├── web/      # Next.js 14 (new)
│   └── api/      # FastAPI (new)
├── legacy/       # all current Streamlit code (moved as Phase-1 step 0)
├── handoff/      # kept verbatim as reference
├── docs/         # specs + plans (this file)
└── ml/           # ML notebooks + artifacts (stays at root, both apps can read)
```

`legacy/` keeps deploying to its current Streamlit Cloud URL through Phase 3 so we can A/B.

---

## Deltas vs MIGRATION.md

### 1. LLM provider

The brief assumes Gemini (`utils/gemini.py`, `GEMINI_API_KEY`). Since the brief was written we migrated everything to **OpenAI / Azure OpenAI** (PR #2). The single SDK boundary is `agents/llm_client.py`, which exposes `chat()`, `complete()`, `chat_completion()` and reads secrets from `dev.env` via `python-dotenv`.

**Migration path:** port `agents/llm_client.py` and `utils/gemini.py` into `apps/api/ai/` mostly unchanged. Drop the brief's Gemini-model-name gotcha (not applicable). Secrets become env vars on Railway.

### 2. Persistence

The brief assumes `data/dummy_data.py` is the truth and Postgres migration happens in Phase 4. Since then we shipped **`data/database.py`** — a real SQLite schema with `users` and `bookings` tables, used by the player booking flow and the agent tools.

**Migration path:** the SQLite schema becomes the Postgres schema (SQLAlchemy models). Phase-2 mock data follows the same shape so the swap to live endpoints in Phase 4 is mechanical.

### 3. Chat agents

The brief predates the player + owner chat agents (PR #2, merged). We have:
- `agents/llm_client.py` — shared LLM wrapper
- `agents/player/{tools,system_prompt,knowledge,agent}.py` — search / availability / propose-and-confirm booking + cancel
- `agents/owner/{tools,system_prompt,knowledge,agent}.py` — revenue, list bookings, no-show risk, demand forecast, court summary
- `components/chat_widget.py` — Streamlit floating chat UI

**Migration path:** added to Phase 3.
- **Server:** tools become FastAPI handlers (`POST /api/chat/player`, `POST /api/chat/owner`), agent loops live in `apps/api/agents/`.
- **Client:** floating 64px launcher in `apps/web/components/ChatWidget.tsx`. Uses Vercel AI SDK `useChat` hook for **streaming** responses (token-by-token in the panel). Two-phase player writes still surface inline Confirm / Cancel buttons in the chat panel; the commit hits a separate `/api/bookings` endpoint on confirm, not the LLM.

### 4. Auth

Brief says NextAuth v5 with email **+ Google**. v1 drops Google (less infra to set up); keep magic-link only. Role (`player` / `owner`) stored on the user row, read in middleware to gate `(player)` vs `(owner)` route groups.

---

## Phase plan

Each phase is **its own brainstorm → spec → plan → implementation PR** cycle. We don't pre-write Phase 2-4 specs; later phases depend on what Phase 1 surfaces.

### Phase 1 — Scaffold & design system (this is the first spec we'll write a plan for)
- Move current Streamlit into `legacy/`
- Scaffold `apps/web` with `pnpm create next-app`
- Drop in `handoff/design-system/{shared.css, tailwind.config.ts}` and `handoff/components/*.tsx`
- Wire Space Grotesk / Inter / Lexend / Material Symbols Rounded fonts
- Render the landing page (Player vs Owner picker) in Next.js
- Smoke-test: typography + lime accents render correctly, no Tailwind build warnings
- Commit: `feat: scaffold Next.js app with ZPOTS design system`

### Phase 2 — Read-only player flows
home, search, court details, booking, confirmation, my-bookings, check-in, feedback. Mock data layer in `apps/web/lib/mock-data.ts` mirroring `data/database.py` row shapes.

### Phase 3 — Owner console + AI + chat agents
- Owner pages: dashboard, manage courts (grid + list), slots, pricing, bookings, AI insights, optimization
- FastAPI scaffold with the AI helper endpoints (`ai/parse-search`, `ai/insights`, `ai/court-description`)
- Chat endpoints (`chat/player`, `chat/owner`) with tools ported from `agents/`
- Streaming chat widget on both flows
- Wire live AI helpers (mock data still for non-AI calls)
- **Auth dependency:** chat widget + role-based route gating need a logged-in user. Phase 3 uses a **stubbed session** (hard-coded test user via env-var `DEV_USER_ID` and `DEV_FLOW=player|owner`) so screens render. Real NextAuth lands in Phase 4 and the stub is removed.

### Phase 4 — Data, auth, polish, deploy
- Postgres schema from SQLAlchemy models
- Migrate seed data from `data/database.py` and `data/dummy_data.py`
- Live REST endpoints replace mock data
- NextAuth v5 magic-link
- Lighthouse + a11y pass
- Vercel (apps/web) + Railway (apps/api) deploy

---

## Out of scope for v1

- Real payment (booking ends at "confirm")
- Real imagery (emoji placeholders stay until photography is sourced)
- Mobile-first responsive (desktop-first; mobile pass in Phase 4)
- Per-owner court scoping (every owner still sees all courts — same as today)
- Streaming AI Insights page (one-shot like today; only the chat widget streams)
- Google OAuth (magic-link only in v1)

---

## Success criteria

**Per-phase:** the smoke test described in that phase passes in a real browser.

**End-to-end (Phase 4):** all 19 Streamlit routes have working Next.js equivalents, all player flows complete (find → book → check-in), all owner pages render real data, both chat agents work end-to-end with streaming, and the Vercel + Railway deploys are healthy. Legacy Streamlit can be turned off.

---

## Sub-project handoff order

When this design is approved:

1. Invoke `superpowers:writing-plans` for **Phase 1 only** (scaffold).
2. Execute Phase 1 plan, merge.
3. Come back to brainstorming for Phase 2 — what we learned in Phase 1 informs decisions (e.g., did Recharts work cleanly with the design tokens? did `pnpm` work in the repo's CI?). Repeat the brainstorm → spec → plan → PR cycle.
4. Same for Phase 3 and Phase 4.

This is intentional: writing all four phase plans upfront would be premature; the brief in `handoff/MIGRATION.md` already tells us *what* to build, the per-phase plans capture *how* with current-context knowledge.
