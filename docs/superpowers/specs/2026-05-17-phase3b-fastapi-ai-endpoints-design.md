# Phase 3b — FastAPI Scaffold + AI Helper Endpoints Design

**Date:** 2026-05-17
**Status:** Approved
**Base spec:** `docs/superpowers/specs/2026-05-16-nextjs-migration-design.md`
**Deploy doc:** `docs/superpowers/specs/2026-05-17-deployment-gcp-cloud-run.md`
**Phase position:** 3b of 4 (Phase 1, 2, 3a merged)

---

## Goal

Stand up a FastAPI service at `apps/api/` that wraps the existing `utils/gemini.py` (Azure OpenAI helpers) and `utils/ml_inference.py` (sklearn artifacts) as REST endpoints, then wire 4 frontend pages in `apps/web/` to call them through a thin Next.js proxy. After this phase, the owner AI Insights summary, demand-forecast heatmap, no-show risk pills, court-description generator, and the player natural-language search are all live instead of mocked.

---

## Architecture

```
Browser → Next.js (apps/web)
              │
              ▼
         apps/web/app/api/[...path]/route.ts   (generic proxy)
              │
              ▼  proxies to NEXT_API_TARGET (http://localhost:8000 local,
              │                              Cloud Run URL prod — Phase 4)
              ▼
         FastAPI (apps/api) on :8000
              │
              ├──► Azure OpenAI  (via ported llm_client.py)
              └──► ML artifacts  (joblib + parquet in ml/models/)
```

Single env var `NEXT_API_TARGET` flips dev ↔ production target. Frontend code never knows the FastAPI URL directly. No CORS to configure.

---

## Repo additions

```
apps/api/                            # NEW
├── main.py                          # FastAPI app + routers + /health
├── requirements.txt                 # fastapi, uvicorn, pydantic, openai,
│                                    #   scikit-learn, joblib, pandas, pyarrow,
│                                    #   python-dotenv
├── ai/
│   ├── __init__.py
│   ├── client.py                    # ← ported from agents/llm_client.py
│   └── helpers.py                   # ← ported from utils/gemini.py
├── ml/
│   ├── __init__.py
│   └── inference.py                 # ← ported from utils/ml_inference.py
│                                    #    (Streamlit cache decorators removed,
│                                    #     replaced with module-level lazy load)
├── routers/
│   ├── __init__.py
│   ├── ai.py                        # /ai/parse-search, /ai/insights,
│   │                                #   /ai/court-description
│   ├── ml.py                        # /ml/demand-forecast, /ml/noshow-risk/batch
│   └── health.py                    # /health
├── schemas/
│   ├── __init__.py
│   ├── ai.py                        # Pydantic request/response models
│   └── ml.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # autouse fixture mocks the OpenAI client
│   ├── test_ai_routes.py
│   ├── test_ml_routes.py
│   └── test_health.py
└── README.md                        # how to run locally, env vars

apps/web/
├── app/api/[...path]/route.ts       # NEW — generic proxy (GET, POST, etc.)
├── lib/api-client.ts                # NEW — typed fetch helpers
└── lib/api-types.ts                 # NEW — TS types mirroring Pydantic
```

`ml/models/` at the repo root is shared between legacy Streamlit and the new FastAPI — both stacks read the same joblib artifacts. Not duplicated.

---

## Endpoints

| Method | Path | Wraps | Frontend caller |
|---|---|---|---|
| `GET` | `/health` | — (returns `{"status":"ok"}`) | Cloud Scheduler keep-warm (Phase 4) |
| `POST` | `/ai/parse-search` | `parse_search_query(query)` | `/player/search` Search button |
| `POST` | `/ai/insights` | `generate_ai_insights(util, demand, bookings)` | `/owner/insights` Generate AI Summary |
| `POST` | `/ai/court-description` | `generate_court_description(name, sport, surface, location, amenities)` | `/owner/venues/[id]/edit` Generate Description |
| `GET` | `/ml/demand-forecast` | `get_demand_forecast()` | `/owner/insights` heatmap |
| `POST` | `/ml/noshow-risk/batch` | `predict_noshow_risk(booking)` looped over a list | `/owner/bookings` risk pills |

The no-show endpoint is batched because the bookings page wants risk for N rows in one round trip. Single-item version is not needed in Phase 3b.

### Request / response shapes

```python
# schemas/ai.py
class ParseSearchRequest(BaseModel):
    query: str

class ParseSearchResponse(BaseModel):
    sport: str | None
    district: str | None
    time_of_day: Literal['morning', 'afternoon', 'evening'] | None
    max_price: int | None

class InsightsRequest(BaseModel):
    weekly_utilization: dict[str, int]
    district_demand: list[dict]
    owner_bookings: list[dict]

class InsightsResponse(BaseModel):
    markdown: str

class CourtDescriptionRequest(BaseModel):
    name: str
    sport: str
    surface: str
    location: str
    amenities: list[str]

class CourtDescriptionResponse(BaseModel):
    description: str

# schemas/ml.py
class DemandCell(BaseModel):
    court_id: str
    day_of_week: int  # 0=Mon..6=Sun
    hour: int         # 7..22
    predicted_bookings: float

class NoShowRiskItem(BaseModel):
    sport: str
    district: str
    day_of_week: int
    hour: int
    is_weekend: bool
    is_holiday: bool
    weather: str
    price: int
    lead_time_days: int
    is_repeat_customer: bool

class NoShowRiskResult(BaseModel):
    tier: Literal['Low', 'Medium', 'High']
    probability: float

class NoShowRiskBatchRequest(BaseModel):
    items: list[NoShowRiskItem]

class NoShowRiskBatchResponse(BaseModel):
    results: list[NoShowRiskResult]
```

---

## Code reuse

Port these three files from the repo root into `apps/api/`:

| Source (root) | Target (apps/api) | Adaptation |
|---|---|---|
| `agents/llm_client.py` | `apps/api/ai/client.py` | None — already env-var based |
| `utils/gemini.py` | `apps/api/ai/helpers.py` | Update import paths (`agents.llm_client` → `apps.api.ai.client` or relative `.client`) |
| `utils/ml_inference.py` | `apps/api/ml/inference.py` | Remove `@st.cache_data` / `@st.cache_resource` decorators; replace with a module-level lazy load pattern (`_ARTIFACT: dict \| None = None`; `def _load(): if _ARTIFACT is None: ...`) |

Legacy Streamlit code at the repo root stays untouched. Both stacks keep working independently — the user's "Streamlit must stay runnable any time" requirement is preserved.

---

## Frontend wiring (4 pages)

### `/owner/insights`

- **Generate AI Summary button:** show loading state, call `aiInsights({weekly_utilization, district_demand, owner_bookings})`, render returned markdown via `react-markdown` (new dep). On error, toast.
- **Demand heatmap:** on mount, call `mlDemandForecast()`. Show skeleton while loading. On success, replace the imported `DEMAND_FORECAST` with the API response. On error, fall back to the mock constant + show a small "using cached forecast" hint.

### `/owner/bookings`

- On mount, call `mlNoshowRisk(allBookings)` (batch — one round trip). Hydrate each booking with the returned tier/probability. Replace the sport-derived `RISK_BY_SPORT` stub. Show "—" in the Risk column until the response arrives. On error, fall back to the stub silently.

### `/owner/venues/[id]/edit`

- "Generate Description" button calls `aiCourtDescription({name, sport, surface, location, amenities})` instead of writing the hardcoded blurb. Loading state on the button. Populate the textarea on success.

### `/player/search`

- Search button now calls `aiParseSearch({query})`. Response merged into URL search params (`?sport=Badminton&district=Sukhumvit&max_price=400`); existing filter chips update accordingly. On error, do nothing (the search input keeps the typed value, chips don't change).

---

## Local dev

Two terminals (simple, no extra tooling):
```bash
# Terminal 1
cd apps/api && uvicorn main:app --reload --port 8000

# Terminal 2
cd apps/web && pnpm dev   # NEXT_API_TARGET defaults to http://localhost:8000
```

A `make dev` or `pnpm dev:all` (concurrently) script is nice-to-have, not in scope.

---

## Python environment

Reuse the existing `MADT` conda env. `apps/api/requirements.txt` lists what's needed (fastapi, uvicorn, pydantic, openai, scikit-learn, joblib, pandas, pyarrow, python-dotenv). MADT already has all of them; `pip install -r apps/api/requirements.txt` is idempotent.

For Phase 4 (Docker), the requirements file becomes the `pip install` command in the Dockerfile.

---

## Schema sharing

Manual TS types in `apps/web/lib/api-types.ts` mirroring the Pydantic models. Drift risk is low for 6 endpoints; OpenAPI codegen via `openapi-typescript` is a clean nice-to-have for later if drift becomes painful.

---

## Testing

- **pytest** for `apps/api/`:
  - `conftest.py` autouse fixture mocks `openai.AzureOpenAI` (same boundary the existing legacy `tests/agents/test_gemini_helpers.py` uses)
  - `test_health.py` — boots the app, asserts `/health` returns 200 + ok
  - `test_ai_routes.py` — one test per AI route. Stub `complete()` / `chat_completion()` to return canned strings; assert the route parses the response and wraps it in the right Pydantic schema
  - `test_ml_routes.py` — `/ml/demand-forecast` returns rows of the right shape; `/ml/noshow-risk/batch` returns one result per input. Real joblib artifacts used (small, fast).
  - ~10 tests total
- **Existing legacy `pytest tests/`** stays green (29 tests). We don't touch root-level code.
- **Existing Vitest** stays green (31 tests).
- **Existing Playwright** stays green (3 tests). They test that pages render, not the AI flow.
- **No new Playwright** in 3b. Stubbing AI at the network layer for E2E is overkill; unit coverage is enough.

---

## Error handling

| Layer | Strategy |
|---|---|
| FastAPI route | `try: ... except OpenAIError as e: raise HTTPException(503, ...)`. Catch-all 500 for unexpected. |
| Next.js proxy route | Pass through status code and body. On network error reaching FastAPI, return 502 with `{error: "API unreachable"}`. |
| Frontend page | Per page (see Frontend wiring section). Generally: silent fallback to mock for non-critical paths (heatmap, no-show risk), toast for user-initiated actions (Generate AI Summary, Generate Description, Search). |

---

## Configuration

| Env var | Where read | Default |
|---|---|---|
| `NEXT_API_TARGET` | `apps/web` proxy route | `http://localhost:8000` |
| `OPENAI_PROVIDER` | `apps/api/ai/client.py` | `azure` |
| `AZURE_OPENAI_API_KEY` | `apps/api/ai/client.py` | (required if Azure) |
| `AZURE_API_VERSION` | `apps/api/ai/client.py` | (required if Azure) |
| `AZURE_ENDPOINT` | `apps/api/ai/client.py` | (required if Azure) |
| `AZURE_DEPLOYMENT` | `apps/api/ai/client.py` | (required if Azure) |
| `OPENAI_API_KEY` | `apps/api/ai/client.py` | (required if provider=openai) |
| `ZPOTS_AGENT_MODEL` | `apps/api/ai/client.py` | falls back to `AZURE_DEPLOYMENT` |

Local dev reads from `dev.env` (already gitignored). Production env vars (Phase 4) come from Cloud Run's env-var panel.

---

## Out of scope for 3b

- Chat agents (port + frontend widget) — Phase 3c
- NextAuth — Phase 4
- Postgres — Phase 4
- Dockerfiles + Cloud Run deploy — Phase 4
- E2E tests against real Azure
- Streaming AI responses (insights are one-shot; chat streaming lands in 3c)
- OpenAPI → TS codegen
- A `pnpm dev:all` convenience script

---

## Success criteria

1. `cd apps/api && uvicorn main:app --port 8000` boots cleanly
2. `curl localhost:8000/health` → `{"status":"ok"}`
3. `cd apps/api && pytest -q` passes (~10 tests, all OpenAI mocked)
4. All 4 frontend pages exercise the live API in the browser when Azure env vars are set
5. With Azure env vars NOT set, frontend gracefully falls back (heatmap to mock, AI Summary to error toast, etc.)
6. Legacy Streamlit + Vitest + Playwright all stay green
7. `cd apps/web && pnpm build` clean

---

## Handoff

When approved, invoke `superpowers:writing-plans` to produce the Phase 3b implementation plan. Phase 3c (chat agents + streaming widget) gets its own brainstorm after 3b merges.
