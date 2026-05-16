# ZPOTS Handoff Package

Everything Claude Code needs to migrate the ZPOTS Streamlit app to a production Next.js + FastAPI stack.

## Start here

1. Read **`CLAUDE.md`** — the brief for Claude Code.
2. Read **`MIGRATION.md`** — file-by-file map from your Streamlit code to the new stack, plus a 4-week phase plan.
3. Read **`design-system/tokens.md`** — quick color/type reference.

## Contents

```
handoff/
├── CLAUDE.md                ← brief — put at repo root when you start
├── MIGRATION.md             ← scope, route map, phase plan
├── README.md                ← this file
├── design-system/
│   ├── shared.css           ← drop into app/globals.css
│   ├── tailwind.config.ts   ← drop into project root
│   └── tokens.md
├── components/              ← ready-to-use React (TSX) components
│   ├── Icon.tsx
│   ├── Button.tsx
│   ├── Tags.tsx             (AITag, StatusBadge, Chip, Eyebrow)
│   ├── CourtCard.tsx
│   ├── KpiCard.tsx
│   ├── PlayerTopBar.tsx
│   ├── OwnerSidebar.tsx
│   ├── charts/UtilizationBars.tsx
│   └── types.ts
├── screens/                 ← reference full-page implementations
│   ├── PlayerSearch.tsx
│   └── OwnerDashboard.tsx
├── backend/                 ← FastAPI skeleton
│   ├── main.py
│   ├── schemas.py
│   ├── ai.py                (your gemini.py, de-Streamlit'd)
│   └── requirements.txt
└── assets/
    ├── bolt-glyph.svg
    ├── wordmark.svg
    └── wordmark-dark.svg
```

## How to use with Claude Code

```bash
cd /path/to/your/zpots/clone
git checkout -b feat/nextjs-migration
# copy the handoff/ folder into the repo (or unzip next to it)
# open Claude Code in the repo
```

Then: **"Read handoff/CLAUDE.md and handoff/MIGRATION.md, then start Phase 1."**

Claude Code will:
1. Move current Streamlit files into `legacy/`
2. Scaffold a Next.js 14 app with the ZPOTS design system
3. Copy the components and screens over
4. Smoke-test, then commit

Review the PR, then tell it to continue with Phase 2.

## Stack summary

| Layer | Choice |
|---|---|
| Frontend | Next.js 14 App Router + TypeScript + Tailwind |
| Backend | FastAPI + Python 3.11 + Pydantic v2 |
| Database | Postgres (Supabase / Neon / Railway) |
| Auth | NextAuth v5 |
| Charts | Recharts |
| Deploy | Vercel (web) + Railway (api) |
