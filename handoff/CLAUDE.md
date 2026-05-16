# CLAUDE.md — ZPOTS migration brief

You are migrating this repo from **Streamlit** to **Next.js 14 + FastAPI**, using the design system and reference components in `handoff/`.

## Ground rules

1. **Read `handoff/MIGRATION.md` first** — it maps every Streamlit file to a Next.js route and explains the data model. Treat it as the source of truth for scope.
2. **Do not rewrite the design system.** `handoff/design-system/shared.css` and `handoff/design-system/tailwind.config.ts` are settled. Copy them into the new project verbatim.
3. **Keep `utils/gemini.py` working.** It's the one piece of business logic worth preserving line-for-line. Move it into the FastAPI backend, swap `st.secrets` → `os.getenv`, fix the invalid model name (see MIGRATION.md gotcha #2).
4. **Do not delete the current Streamlit app until Phase 3 is green.** Keep it runnable so you can A/B.
5. **One commit per phase checklist item** in MIGRATION.md. Small PRs, easy reviews.

## Stack decisions (already made — don't re-litigate)

- **Frontend:** Next.js 14 App Router, TypeScript strict, Tailwind, `pnpm`
- **Backend:** FastAPI, Python 3.11, SQLAlchemy 2.0, Pydantic v2, `uv` or `pip`
- **DB:** Postgres (Supabase in dev, any managed provider in prod)
- **Auth:** NextAuth v5 with email + Google
- **Charts:** Recharts (not Plotly)
- **QR:** `qrcode.react` (client-side)
- **Data fetching:** TanStack Query + `fetch` with a typed client
- **Deploy:** Vercel (web) + Railway (api)

If you have a strong reason to deviate (e.g. team already uses Prisma), pause and ask.

## Project layout

```
.
├── apps/
│   ├── web/               # Next.js app (move here from repo root)
│   │   ├── app/
│   │   │   ├── (player)/
│   │   │   ├── (owner)/
│   │   │   ├── api/       # thin BFF routes that proxy to FastAPI
│   │   │   └── page.tsx   # landing
│   │   ├── components/
│   │   ├── lib/
│   │   └── tailwind.config.ts
│   └── api/               # FastAPI (move pages/owner logic here)
│       ├── main.py
│       ├── schemas.py
│       ├── ai.py          # was utils/gemini.py
│       ├── routers/
│       └── db.py
├── legacy/                # the old Streamlit app lives here during migration
│   ├── app.py
│   ├── pages/
│   └── ...
└── handoff/               # this brief + design system (keep for reference)
```

Move everything under current repo root into `legacy/` as step zero. Keeps diffs clean.

## Execution order

Work through `handoff/MIGRATION.md` **Phase 1 → 4 in order**. Don't jump to data/auth before the read-only screens render from mock data.

### Phase 1 checklist (do this first)

1. `mkdir legacy && git mv app.py pages/ components/ data/ utils/ .streamlit/ requirements.txt legacy/`
2. `pnpm create next-app apps/web --typescript --tailwind --app --no-src-dir --import-alias "@/*"`
3. Copy `handoff/design-system/shared.css` → `apps/web/app/globals.css` (replace default)
4. Copy `handoff/design-system/tailwind.config.ts` → `apps/web/tailwind.config.ts`
5. Copy `handoff/components/` → `apps/web/components/`
6. Copy `handoff/screens/*.tsx` → temp place, import one into `apps/web/app/page.tsx` to smoke-test
7. `pnpm --filter web dev` — verify the landing + one player screen render with correct typography and lime accents
8. **Commit:** `"feat: scaffold Next.js app with ZPOTS design system"`

Do not move to Phase 2 until the smoke test is clean in the browser and there are no Tailwind build warnings.

## When you hit decisions I haven't made

Pause and ask the human, don't guess, on:
- Database schema specifics (e.g. court → venue cardinality, pricing model fields)
- Whether to keep feature flags for half-finished screens
- Real brand assets (photography, logos beyond the bolt glyph)
- Anything auth-related (providers, roles, RLS)

## Things to flag in your first PR

- The invalid Gemini model name in `legacy/utils/gemini.py` (see MIGRATION.md gotcha #2)
- Any Streamlit-specific behavior that doesn't have a clean React equivalent (`st.rerun`, `st.spinner`, sidebar auto-hide)
- Any component in `legacy/components/css.py` that has a visual effect not captured in `handoff/design-system/`

## Tone

The design system has strong opinions: lime accent on AI features, dark forest sidebar for owner, Space Grotesk displays, Lexend eyebrows in small-caps. When in doubt, match existing ZPOTS visual DNA rather than inventing new patterns. Emoji placeholders are **placeholders** — replace with real imagery as it becomes available, but don't invent SVG illustrations to fill the gap.
