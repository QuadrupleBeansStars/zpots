# Phase 3b — FastAPI + AI Endpoints Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a FastAPI service at `apps/api/` wrapping the existing OpenAI/Azure helpers and sklearn ML artifacts as 6 REST endpoints, then wire 4 frontend pages in `apps/web/` to call them through a thin Next.js proxy.

**Architecture:** `apps/api/` is its own Python package: `main.py` mounts routers under `ai/`, `ml/`, `health/`; secrets come from env (Azure OpenAI in dev via `dev.env`, Cloud Run env vars in prod). The Next.js app proxies all `/api/*` calls to `NEXT_API_TARGET` so frontend code never knows the FastAPI URL. ML joblib artifacts at `ml/models/` are shared with the legacy Streamlit. Code ported from `agents/llm_client.py`, `utils/gemini.py`, `utils/ml_inference.py` (Streamlit decorators stripped); legacy at the repo root stays untouched.

**Tech Stack:** Python 3.11 · FastAPI · Pydantic v2 · uvicorn · openai · scikit-learn · joblib · pandas · pytest · Next.js 16 · TypeScript · react-markdown

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase3b-fastapi-ai-endpoints-design.md`
**Branch:** create `feat/nextjs-phase3b` off main

---

## File structure (end of Phase 3b)

```
apps/api/                            # NEW
├── __init__.py                      # marks apps/api as a package
├── main.py                          # FastAPI app, mounts routers
├── requirements.txt                 # deps
├── README.md                        # how to run locally
├── conftest.py                      # pytest autouse fixture (mocks OpenAI)
├── ai/
│   ├── __init__.py
│   ├── client.py                    # ← ported from agents/llm_client.py
│   └── helpers.py                   # ← ported from utils/gemini.py
├── ml/
│   ├── __init__.py
│   └── inference.py                 # ← ported from utils/ml_inference.py
├── routers/
│   ├── __init__.py
│   ├── health.py
│   ├── ai.py
│   └── ml.py
├── schemas/
│   ├── __init__.py
│   ├── ai.py
│   └── ml.py
└── tests/
    ├── __init__.py
    ├── test_health.py
    ├── test_ai_routes.py
    └── test_ml_routes.py

apps/web/
├── app/api/[...path]/route.ts       # NEW — generic proxy
├── lib/api-client.ts                # NEW — typed fetch helpers
├── lib/api-types.ts                 # NEW — TS types mirroring Pydantic
├── app/owner/insights/page.tsx      # MODIFIED — wire AI summary + heatmap
├── app/owner/bookings/page.tsx      # MODIFIED — wire no-show risk
├── components/owner/CourtForm.tsx   # MODIFIED — wire Generate Description
└── app/player/search/page.tsx       # MODIFIED — wire parse-search
```

---

## Pre-task setup

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git checkout main && git pull
git checkout -b feat/nextjs-phase3b
```

---

## Task 1: Scaffold `apps/api` + health endpoint

**Files:**
- Create: `apps/api/__init__.py`, `apps/api/main.py`, `apps/api/requirements.txt`, `apps/api/README.md`
- Create: `apps/api/conftest.py`, `apps/api/tests/__init__.py`, `apps/api/tests/test_health.py`
- Create: `apps/api/routers/__init__.py`, `apps/api/routers/health.py`

- [ ] **Step 1: Create empty package markers and the requirements file.**

```bash
mkdir -p /Users/nchawanp/Desktop/ZPOTS/apps/api/{ai,ml,routers,schemas,tests}
touch /Users/nchawanp/Desktop/ZPOTS/apps/api/__init__.py \
      /Users/nchawanp/Desktop/ZPOTS/apps/api/ai/__init__.py \
      /Users/nchawanp/Desktop/ZPOTS/apps/api/ml/__init__.py \
      /Users/nchawanp/Desktop/ZPOTS/apps/api/routers/__init__.py \
      /Users/nchawanp/Desktop/ZPOTS/apps/api/schemas/__init__.py \
      /Users/nchawanp/Desktop/ZPOTS/apps/api/tests/__init__.py
```

- [ ] **Step 2: Create `apps/api/requirements.txt`:**

```
fastapi>=0.115
uvicorn[standard]>=0.30
pydantic>=2.7
openai>=1.40
scikit-learn>=1.4
joblib>=1.3
pandas>=2.1
pyarrow>=14
python-dotenv>=1.0
httpx>=0.27
pytest>=8
```

(`httpx` is required by `fastapi.testclient.TestClient`.)

- [ ] **Step 3: Install deps into the existing `MADT` conda env.**

```bash
conda run -n MADT pip install -r /Users/nchawanp/Desktop/ZPOTS/apps/api/requirements.txt
```

Expected: clean install. Most deps are already present from the Streamlit/Vitest work; this just adds `fastapi`, `uvicorn`, `httpx`.

- [ ] **Step 4: Write the failing health test.** Create `apps/api/tests/test_health.py`:

```python
from fastapi.testclient import TestClient
from main import app


def test_health_returns_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 5: Run, expect ImportError on `main`.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_health.py -v
```

- [ ] **Step 6: Implement `apps/api/routers/health.py`:**

```python
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Liveness probe. Used by Cloud Scheduler to keep the container warm in Phase 4."""
    return {"status": "ok"}
```

- [ ] **Step 7: Implement `apps/api/main.py`:**

```python
from fastapi import FastAPI

from routers import health

app = FastAPI(
    title="ZPOTS API",
    description="OpenAI/Azure helpers + ML inference for the Next.js frontend.",
    version="0.1.0",
)

app.include_router(health.router)
```

- [ ] **Step 8: Run health test, expect pass.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_health.py -v
```

Expected: 1 passed.

- [ ] **Step 9: Manually smoke the dev server.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api
conda run -n MADT uvicorn main:app --port 8000 &
sleep 4
curl -sf http://localhost:8000/health && echo OK
kill %1 2>/dev/null || true
```

Expected: prints `{"status":"ok"}` followed by `OK`.

- [ ] **Step 10: Create `apps/api/README.md`:**

```markdown
# ZPOTS API

FastAPI service for the Next.js frontend. Wraps Azure OpenAI helpers and sklearn ML artifacts.

## Run locally

```bash
conda activate MADT
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open <http://localhost:8000/docs> for the Swagger UI.

## Tests

```bash
cd apps/api
pytest -q
```

## Env vars

See `dev.env` at repo root. Required for AI endpoints:
- `OPENAI_PROVIDER` (default `azure`)
- `AZURE_OPENAI_API_KEY`, `AZURE_API_VERSION`, `AZURE_ENDPOINT`, `AZURE_DEPLOYMENT`

ML endpoints read joblib artifacts from `../../ml/models/`.
```

- [ ] **Step 11: Commit.**

```bash
git add apps/api
git commit -m "feat(api): scaffold FastAPI app at apps/api with /health

Adds requirements.txt (fastapi, uvicorn, pydantic, openai, sklearn,
joblib, pandas, pyarrow, dotenv, httpx, pytest), bare-package marker
files, main.py mounting a single /health router, and a pytest test.
'cd apps/api && uvicorn main:app' boots cleanly and curl /health
returns {status:ok}."
```

---

## Task 2: Port LLM client (`apps/api/ai/client.py`)

**Files:**
- Create: `apps/api/ai/client.py`

- [ ] **Step 1: Create `apps/api/ai/client.py` (copy + adapt from `agents/llm_client.py` at the repo root).** The source already reads env vars correctly; only the docstring needs trimming. Write this content:

```python
"""Thin LLM client wrapper. Single SDK boundary for the FastAPI service.

Provider is chosen by env var `OPENAI_PROVIDER` (default "azure"). Secrets and
deployment ids are loaded from the project's dev.env via python-dotenv in dev;
Cloud Run injects them as env vars in production.
"""
import logging
import os

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI

_ENV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "dev.env",
)
load_dotenv(_ENV_PATH)

MAX_TOKENS = 2048

_log = logging.getLogger(__name__)
_client: AzureOpenAI | OpenAI | None = None


def _resolve_model() -> str:
    explicit = os.getenv("ZPOTS_AGENT_MODEL") or os.getenv("AZURE_DEPLOYMENT")
    if explicit:
        return explicit
    provider = os.getenv("OPENAI_PROVIDER", "azure").lower()
    if provider == "azure":
        raise RuntimeError(
            "Azure deployment name is required. Set AZURE_DEPLOYMENT (or "
            "ZPOTS_AGENT_MODEL) in dev.env to your Azure OpenAI deployment name."
        )
    return "gpt-4o-mini"


def _build_client() -> AzureOpenAI | OpenAI:
    provider = os.getenv("OPENAI_PROVIDER", "azure").lower()
    if provider == "azure":
        missing = [
            name for name in ("AZURE_OPENAI_API_KEY", "AZURE_API_VERSION", "AZURE_ENDPOINT")
            if not os.getenv(name)
        ]
        if missing:
            raise RuntimeError(
                f"Azure OpenAI is missing env vars: {', '.join(missing)}. "
                f"Set them in dev.env."
            )
        return AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI()


def _get_client() -> AzureOpenAI | OpenAI:
    global _client
    if _client is None:
        _client = _build_client()
    return _client


def _model() -> str:
    return _resolve_model()


def complete(
    user_prompt: str,
    system: str | None = None,
    max_tokens: int = 512,
    json_mode: bool = False,
) -> str:
    """One-shot text generation. Raises on API errors."""
    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user_prompt})
    kwargs: dict = {"model": _model(), "messages": messages, "max_tokens": max_tokens}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = _get_client().chat.completions.create(**kwargs)
    return (response.choices[0].message.content or "").strip()


def chat_completion(
    messages: list[dict],
    system: str,
    max_tokens: int = 512,
) -> str:
    """Multi-turn text completion without tools. Raises on API errors."""
    api_messages: list[dict] = [{"role": "system", "content": system}]
    api_messages.extend({"role": m["role"], "content": m["content"]} for m in messages)
    response = _get_client().chat.completions.create(
        model=_model(),
        messages=api_messages,
        max_tokens=max_tokens,
    )
    return (response.choices[0].message.content or "").strip()
```

(`chat()` for tool-calling is omitted — not needed by 3b. Phase 3c will add it back.)

- [ ] **Step 2: Smoke import.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT python -c "from ai.client import complete, chat_completion; print('ok')"
```

Expected: `ok`.

- [ ] **Step 3: Commit.**

```bash
git add apps/api/ai/client.py
git commit -m "feat(api): port LLM client into apps/api/ai/client.py

Copied from agents/llm_client.py at repo root. complete() and
chat_completion() only — chat() for tool-calling is deferred to Phase 3c.
Env-var-driven; reads dev.env locally, Cloud Run env vars in prod."
```

---

## Task 3: Port AI helpers (`apps/api/ai/helpers.py`)

**Files:**
- Create: `apps/api/ai/helpers.py`

- [ ] **Step 1: Create `apps/api/ai/helpers.py` (copy + adapt from `utils/gemini.py`):**

```python
"""AI helpers for the FastAPI service. Ported from utils/gemini.py."""
import json
import logging

from ai.client import chat_completion, complete

_log = logging.getLogger(__name__)

SPORTS_LIST = ["Badminton", "Football", "Basketball", "Padel"]
DISTRICTS = ["Sukhumvit", "Thong Lor", "Ari", "Pathumwan", "Silom"]


def parse_search_query(query: str) -> dict:
    """Parse a natural-language court search query into structured filters.

    Returns dict with keys: sport, district, time_of_day, max_price.
    Any unrecognised field is null. Returns all-null on parser failure.
    """
    prompt = f"""Extract sports court search filters from this query and return ONLY valid JSON.

Query: "{query}"

Return JSON with exactly these keys (use null if not mentioned):
- "sport": one of {SPORTS_LIST} or null
- "district": one of {DISTRICTS} or null
- "time_of_day": one of ["morning", "afternoon", "evening"] or null
  (morning = 06:00-12:00, afternoon = 12:00-17:00, evening = 17:00-22:00)
- "max_price": integer (baht per hour) or null"""

    try:
        text = complete(prompt, max_tokens=256, json_mode=True)
        return json.loads(text)
    except Exception:
        _log.exception("parse_search_query failed; returning empty filters")
        return {"sport": None, "district": None, "time_of_day": None, "max_price": None}


def generate_ai_insights(weekly_util: dict, district_demand: list, owner_bookings: list) -> str:
    """Generate natural-language AI insights for a venue owner. Returns markdown."""
    booking_summary = ", ".join(
        f"{b['customer']} ({b['sport']} - {b['status']})" for b in owner_bookings
    )
    util_str = ", ".join(f"{day}: {pct}%" for day, pct in weekly_util.items())
    demand_str = ", ".join(f"{d['name']}: {d['demand']}% ({d['level']})" for d in district_demand)

    prompt = f"""You are an AI analytics expert for ZPOTS, a sports court booking platform in Bangkok, Thailand.

Here is the venue data:
- Weekly utilization: {util_str}
- District demand levels: {demand_str}
- Recent bookings: {booking_summary}

Generate a concise venue performance summary (3–4 short paragraphs) covering:
1. Peak performance days/times and what's driving demand
2. No-show risk assessment with specific risk factors
3. Two or three actionable pricing or scheduling recommendations to increase revenue

Use markdown formatting with **bold** for key numbers. Be specific and data-driven. Keep it under 200 words."""

    try:
        return complete(prompt, max_tokens=512)
    except Exception:
        _log.exception("generate_ai_insights failed")
        return "Unable to generate insights at this time. Please try again."


def generate_court_description(name: str, sport: str, surface: str, location: str, amenities: list) -> str:
    """Generate a compelling court listing description for venue owners."""
    amenities_str = ", ".join(amenities) if amenities else "standard facilities"
    prompt = f"""Write a compelling 2–3 sentence listing description for a sports court in Bangkok.

Court details:
- Name: {name}
- Sport: {sport}
- Surface: {surface}
- Location: {location}
- Amenities: {amenities_str}

Tone: professional, energetic, appealing to Bangkok sports enthusiasts.
Output ONLY the description text — no headings, no quotes, no extra commentary."""

    try:
        return complete(prompt, max_tokens=256)
    except Exception:
        _log.exception("generate_court_description failed")
        return "Unable to generate description at this time."
```

- [ ] **Step 2: Smoke import.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT python -c "from ai.helpers import parse_search_query, generate_ai_insights, generate_court_description; print('ok')"
```

Expected: `ok`.

- [ ] **Step 3: Commit.**

```bash
git add apps/api/ai/helpers.py
git commit -m "feat(api): port AI helpers into apps/api/ai/helpers.py

Copied from utils/gemini.py at repo root, minus chat_with_court_assistant
(that becomes part of Phase 3c). Uses ai.client.complete (JSON mode for
parse_search_query). Errors log + return safe fallbacks."
```

---

## Task 4: Port ML inference (`apps/api/ml/inference.py`)

**Files:**
- Create: `apps/api/ml/inference.py`

The legacy `utils/ml_inference.py` uses `@st.cache_data` / `@st.cache_resource` decorators. FastAPI has no equivalent; replace with module-level lazy load.

- [ ] **Step 1: Create `apps/api/ml/inference.py`:**

```python
"""ML inference helpers for the FastAPI service. Ported from utils/ml_inference.py."""
from __future__ import annotations
import os
from typing import Any

import joblib
import pandas as pd

ML_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "ml", "models",
)
DEMAND_PARQUET = os.path.join(ML_DIR, "demand_predictions.parquet")
NOSHOW_PKL = os.path.join(ML_DIR, "noshow_rf.pkl")

_demand_df: pd.DataFrame | None = None
_noshow_artifact: dict[str, Any] | None = None


def get_demand_forecast() -> pd.DataFrame:
    """Return precomputed 7-day forecast. Empty DataFrame if artifact is missing."""
    global _demand_df
    if _demand_df is None:
        if not os.path.exists(DEMAND_PARQUET):
            _demand_df = pd.DataFrame(columns=["court_id", "day_of_week", "hour", "predicted_bookings"])
        else:
            _demand_df = pd.read_parquet(DEMAND_PARQUET)
    return _demand_df


def _load_noshow_artifact() -> dict[str, Any] | None:
    global _noshow_artifact
    if _noshow_artifact is None and os.path.exists(NOSHOW_PKL):
        _noshow_artifact = joblib.load(NOSHOW_PKL)
    return _noshow_artifact


def predict_noshow_risk(booking: dict) -> tuple[str, float]:
    """Predict no-show risk for a single booking dict.

    Expected keys (best-effort; missing ones default to neutral values):
      sport, district, day_of_week, hour, is_weekend, is_holiday, weather,
      price, lead_time_days, is_repeat_customer
    """
    art = _load_noshow_artifact()
    if art is None:
        return ("Low", 0.0)

    row = {
        "sport": booking.get("sport", "Badminton"),
        "district": booking.get("district", "Sukhumvit"),
        "day_of_week": int(booking.get("day_of_week", 2)),
        "hour": int(booking.get("hour", 18)),
        "is_weekend": bool(booking.get("is_weekend", False)),
        "is_holiday": bool(booking.get("is_holiday", False)),
        "weather": booking.get("weather", "sunny"),
        "price": int(booking.get("price", 500)),
        "lead_time_days": int(booking.get("lead_time_days", 3)),
        "is_repeat_customer": bool(booking.get("is_repeat_customer", True)),
    }
    df = pd.DataFrame([row])
    encoded = pd.get_dummies(df, columns=["sport", "district", "weather"], drop_first=True)
    encoded = encoded.reindex(columns=art["feature_columns"], fill_value=0)
    p = float(art["model"].predict_proba(encoded)[0, 1])

    if p < art["threshold_low_med"]:
        tier = "Low"
    elif p < art["threshold_med_high"]:
        tier = "Medium"
    else:
        tier = "High"
    return tier, p
```

- [ ] **Step 2: Smoke that the artifacts load (only if joblib pkl is on disk).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT python -c "
from ml.inference import get_demand_forecast, predict_noshow_risk
df = get_demand_forecast()
print('demand rows:', len(df))
tier, p = predict_noshow_risk({'sport': 'Badminton', 'hour': 18, 'district': 'Sukhumvit'})
print('noshow:', tier, round(p, 3))
"
```

Expected: prints e.g. `demand rows: 672` and `noshow: Low 0.18` (exact numbers depend on the artifact).

- [ ] **Step 3: Commit.**

```bash
git add apps/api/ml/inference.py
git commit -m "feat(api): port ML inference into apps/api/ml/inference.py

Copied from utils/ml_inference.py at repo root. Streamlit cache
decorators replaced with module-level lazy load. Reads the same joblib
+ parquet artifacts in ml/models/ (shared with legacy Streamlit)."
```

---

## Task 5: pytest conftest with OpenAI mock + Pydantic schemas

**Files:**
- Create: `apps/api/conftest.py`
- Create: `apps/api/schemas/ai.py`
- Create: `apps/api/schemas/ml.py`

- [ ] **Step 1: Create `apps/api/conftest.py`:**

```python
"""Pytest autouse fixtures. Mocks the OpenAI client so tests never hit Azure."""
from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def mock_openai_client(monkeypatch):
    """Replace ai.client._get_client() with a MagicMock that returns canned responses.

    Tests that need a specific response payload override `chat.completions.create.return_value`.
    """
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

- [ ] **Step 2: Create `apps/api/schemas/ai.py`:**

```python
from typing import Literal

from pydantic import BaseModel, Field


class ParseSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)


class ParseSearchResponse(BaseModel):
    sport: str | None = None
    district: str | None = None
    time_of_day: Literal["morning", "afternoon", "evening"] | None = None
    max_price: int | None = None


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
```

- [ ] **Step 3: Create `apps/api/schemas/ml.py`:**

```python
from typing import Literal

from pydantic import BaseModel, Field


class DemandCell(BaseModel):
    court_id: str
    day_of_week: int = Field(..., ge=0, le=6)
    hour: int = Field(..., ge=0, le=23)
    predicted_bookings: float


class DemandForecastResponse(BaseModel):
    cells: list[DemandCell]


class NoShowRiskItem(BaseModel):
    sport: str = "Badminton"
    district: str = "Sukhumvit"
    day_of_week: int = Field(default=2, ge=0, le=6)
    hour: int = Field(default=18, ge=0, le=23)
    is_weekend: bool = False
    is_holiday: bool = False
    weather: str = "sunny"
    price: int = 500
    lead_time_days: int = 3
    is_repeat_customer: bool = True


class NoShowRiskResult(BaseModel):
    tier: Literal["Low", "Medium", "High"]
    probability: float


class NoShowRiskBatchRequest(BaseModel):
    items: list[NoShowRiskItem]


class NoShowRiskBatchResponse(BaseModel):
    results: list[NoShowRiskResult]
```

- [ ] **Step 4: Commit.**

```bash
git add apps/api/conftest.py apps/api/schemas/
git commit -m "feat(api): pytest conftest with OpenAI mock + Pydantic schemas

Autouse fixture intercepts ai.client._get_client() so route tests never
hit Azure. Schemas for /ai/* and /ml/* routes."
```

---

## Task 6: `/ai/*` routes (TDD)

**Files:**
- Create: `apps/api/routers/ai.py`
- Modify: `apps/api/main.py` (mount the router)
- Create: `apps/api/tests/test_ai_routes.py`

- [ ] **Step 1: Write failing tests.** Create `apps/api/tests/test_ai_routes.py`:

```python
import json
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _set_response(mock_openai_client, content: str):
    """Helper: override the conftest mock to return a specific content string."""
    msg = MagicMock(); msg.content = content
    choice = MagicMock(); choice.message = msg
    resp = MagicMock(); resp.choices = [choice]
    mock_openai_client.chat.completions.create.return_value = resp


def test_parse_search_returns_filters(mock_openai_client):
    _set_response(mock_openai_client, '{"sport": "Badminton", "district": "Sukhumvit", "time_of_day": "evening", "max_price": 400}')
    r = client.post("/ai/parse-search", json={"query": "badminton near Sukhumvit Friday evening under 400 baht"})
    assert r.status_code == 200
    body = r.json()
    assert body["sport"] == "Badminton"
    assert body["district"] == "Sukhumvit"
    assert body["time_of_day"] == "evening"
    assert body["max_price"] == 400


def test_parse_search_returns_nulls_on_garbled_response(mock_openai_client):
    _set_response(mock_openai_client, "not json at all")
    r = client.post("/ai/parse-search", json={"query": "anything"})
    assert r.status_code == 200
    body = r.json()
    assert body == {"sport": None, "district": None, "time_of_day": None, "max_price": None}


def test_parse_search_validates_empty_query():
    r = client.post("/ai/parse-search", json={"query": ""})
    assert r.status_code == 422


def test_insights_returns_markdown(mock_openai_client):
    _set_response(mock_openai_client, "**Friday peaks** drive 41% of revenue.")
    r = client.post("/ai/insights", json={
        "weekly_utilization": {"Mon": 65, "Fri": 91},
        "district_demand": [{"name": "Sukhumvit", "demand": 94, "level": "Peak"}],
        "owner_bookings": [{"customer": "Alex", "sport": "Padel", "status": "CONFIRMED"}],
    })
    assert r.status_code == 200
    assert "Friday peaks" in r.json()["markdown"]


def test_court_description_returns_text(mock_openai_client):
    _set_response(mock_openai_client, "A premium climate-controlled badminton venue.")
    r = client.post("/ai/court-description", json={
        "name": "BBC", "sport": "Badminton", "surface": "Synthetic",
        "location": "Sukhumvit", "amenities": ["AC", "Parking"],
    })
    assert r.status_code == 200
    assert "premium" in r.json()["description"].lower()
```

- [ ] **Step 2: Run, expect 4 failures (router not mounted yet).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_ai_routes.py -v
```

- [ ] **Step 3: Implement `apps/api/routers/ai.py`:**

```python
from fastapi import APIRouter

from ai.helpers import (
    generate_ai_insights,
    generate_court_description,
    parse_search_query,
)
from schemas.ai import (
    CourtDescriptionRequest,
    CourtDescriptionResponse,
    InsightsRequest,
    InsightsResponse,
    ParseSearchRequest,
    ParseSearchResponse,
)

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/parse-search", response_model=ParseSearchResponse)
def parse_search(req: ParseSearchRequest) -> ParseSearchResponse:
    parsed = parse_search_query(req.query)
    return ParseSearchResponse(**parsed)


@router.post("/insights", response_model=InsightsResponse)
def insights(req: InsightsRequest) -> InsightsResponse:
    markdown = generate_ai_insights(
        req.weekly_utilization, req.district_demand, req.owner_bookings,
    )
    return InsightsResponse(markdown=markdown)


@router.post("/court-description", response_model=CourtDescriptionResponse)
def court_description(req: CourtDescriptionRequest) -> CourtDescriptionResponse:
    text = generate_court_description(
        req.name, req.sport, req.surface, req.location, req.amenities,
    )
    return CourtDescriptionResponse(description=text)
```

- [ ] **Step 4: Mount the router in `apps/api/main.py`. Replace the file content with:**

```python
from fastapi import FastAPI

from routers import ai, health

app = FastAPI(
    title="ZPOTS API",
    description="OpenAI/Azure helpers + ML inference for the Next.js frontend.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(ai.router)
```

- [ ] **Step 5: Run tests, expect 5 passed (4 new + 1 health).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest -v
```

- [ ] **Step 6: Commit.**

```bash
git add apps/api/routers/ai.py apps/api/main.py apps/api/tests/test_ai_routes.py
git commit -m "feat(api): /ai/parse-search, /ai/insights, /ai/court-description

Routes wrap ai.helpers functions with Pydantic request/response schemas.
parse-search uses JSON mode + returns null filters on parser failure.
4 tests, all OpenAI calls mocked via conftest autouse fixture."
```

---

## Task 7: `/ml/*` routes (TDD)

**Files:**
- Create: `apps/api/routers/ml.py`
- Modify: `apps/api/main.py` (mount the router)
- Create: `apps/api/tests/test_ml_routes.py`

- [ ] **Step 1: Write failing tests.** Create `apps/api/tests/test_ml_routes.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_demand_forecast_returns_cells():
    r = client.get("/ml/demand-forecast")
    assert r.status_code == 200
    body = r.json()
    assert "cells" in body
    # Either real artifact loaded (many cells) or missing artifact (empty list)
    assert isinstance(body["cells"], list)
    if body["cells"]:
        cell = body["cells"][0]
        assert {"court_id", "day_of_week", "hour", "predicted_bookings"} <= set(cell.keys())


def test_noshow_risk_batch_returns_one_result_per_item():
    r = client.post("/ml/noshow-risk/batch", json={
        "items": [
            {"sport": "Badminton", "hour": 18, "district": "Sukhumvit"},
            {"sport": "Football", "hour": 19, "district": "Thong Lor"},
        ],
    })
    assert r.status_code == 200
    body = r.json()
    assert len(body["results"]) == 2
    for result in body["results"]:
        assert result["tier"] in ("Low", "Medium", "High")
        assert 0.0 <= result["probability"] <= 1.0


def test_noshow_risk_batch_empty_input():
    r = client.post("/ml/noshow-risk/batch", json={"items": []})
    assert r.status_code == 200
    assert r.json() == {"results": []}
```

- [ ] **Step 2: Run, expect 3 failures (router not mounted).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest tests/test_ml_routes.py -v
```

- [ ] **Step 3: Implement `apps/api/routers/ml.py`:**

```python
from fastapi import APIRouter

from ml.inference import get_demand_forecast, predict_noshow_risk
from schemas.ml import (
    DemandCell,
    DemandForecastResponse,
    NoShowRiskBatchRequest,
    NoShowRiskBatchResponse,
    NoShowRiskResult,
)

router = APIRouter(prefix="/ml", tags=["ml"])


@router.get("/demand-forecast", response_model=DemandForecastResponse)
def demand_forecast() -> DemandForecastResponse:
    df = get_demand_forecast()
    cells = [
        DemandCell(
            court_id=str(row["court_id"]),
            day_of_week=int(row["day_of_week"]),
            hour=int(row["hour"]),
            predicted_bookings=float(row["predicted_bookings"]),
        )
        for _, row in df.iterrows()
    ]
    return DemandForecastResponse(cells=cells)


@router.post("/noshow-risk/batch", response_model=NoShowRiskBatchResponse)
def noshow_risk_batch(req: NoShowRiskBatchRequest) -> NoShowRiskBatchResponse:
    results = []
    for item in req.items:
        tier, probability = predict_noshow_risk(item.model_dump())
        results.append(NoShowRiskResult(tier=tier, probability=probability))
    return NoShowRiskBatchResponse(results=results)
```

- [ ] **Step 4: Mount the router in `apps/api/main.py`. Update the imports + include_router:**

```python
from fastapi import FastAPI

from routers import ai, health, ml

app = FastAPI(
    title="ZPOTS API",
    description="OpenAI/Azure helpers + ML inference for the Next.js frontend.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(ai.router)
app.include_router(ml.router)
```

- [ ] **Step 5: Run tests, expect 8 passed (1 health + 4 ai + 3 ml).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest -v
```

- [ ] **Step 6: Commit.**

```bash
git add apps/api/routers/ml.py apps/api/main.py apps/api/tests/test_ml_routes.py
git commit -m "feat(api): /ml/demand-forecast and /ml/noshow-risk/batch

demand-forecast streams the precomputed parquet rows as Pydantic cells.
noshow-risk/batch loops the sklearn classifier over the request items
(one round trip serves the entire owner bookings table).
8 tests total passing."
```

---

## Task 8: Next.js proxy + typed API client

**Files:**
- Create: `apps/web/app/api/[...path]/route.ts`
- Create: `apps/web/lib/api-types.ts`
- Create: `apps/web/lib/api-client.ts`

- [ ] **Step 1: Create `apps/web/app/api/[...path]/route.ts`:**

```ts
import { NextRequest, NextResponse } from 'next/server';

const TARGET = process.env.NEXT_API_TARGET ?? 'http://localhost:8000';

async function proxy(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  const url = `${TARGET}/${path.join('/')}${req.nextUrl.search}`;

  const body = ['GET', 'HEAD'].includes(req.method) ? undefined : await req.text();

  const headers = new Headers(req.headers);
  headers.delete('host');
  headers.delete('connection');

  try {
    const upstream = await fetch(url, {
      method: req.method,
      headers,
      body,
      // No streaming for Phase 3b; chat streaming lands in 3c.
    });
    const responseBody = await upstream.text();
    return new NextResponse(responseBody, {
      status: upstream.status,
      headers: { 'content-type': upstream.headers.get('content-type') ?? 'application/json' },
    });
  } catch (err) {
    return NextResponse.json(
      { error: 'API unreachable', detail: String(err) },
      { status: 502 },
    );
  }
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const PATCH = proxy;
export const DELETE = proxy;
```

- [ ] **Step 2: Create `apps/web/lib/api-types.ts` (mirrors `apps/api/schemas/`):**

```ts
// Mirrors apps/api/schemas/ai.py
export type ParseSearchRequest = { query: string };
export type ParseSearchResponse = {
  sport: string | null;
  district: string | null;
  time_of_day: 'morning' | 'afternoon' | 'evening' | null;
  max_price: number | null;
};

export type InsightsRequest = {
  weekly_utilization: Record<string, number>;
  district_demand: { name: string; demand: number; level: string }[];
  owner_bookings: { customer: string; sport: string; status: string }[];
};
export type InsightsResponse = { markdown: string };

export type CourtDescriptionRequest = {
  name: string;
  sport: string;
  surface: string;
  location: string;
  amenities: string[];
};
export type CourtDescriptionResponse = { description: string };

// Mirrors apps/api/schemas/ml.py
export type DemandCell = {
  court_id: string;
  day_of_week: number;
  hour: number;
  predicted_bookings: number;
};
export type DemandForecastResponse = { cells: DemandCell[] };

export type NoShowRiskItem = {
  sport?: string;
  district?: string;
  day_of_week?: number;
  hour?: number;
  is_weekend?: boolean;
  is_holiday?: boolean;
  weather?: string;
  price?: number;
  lead_time_days?: number;
  is_repeat_customer?: boolean;
};
export type NoShowRiskResult = {
  tier: 'Low' | 'Medium' | 'High';
  probability: number;
};
export type NoShowRiskBatchRequest = { items: NoShowRiskItem[] };
export type NoShowRiskBatchResponse = { results: NoShowRiskResult[] };
```

- [ ] **Step 3: Create `apps/web/lib/api-client.ts`:**

```ts
import type {
  CourtDescriptionRequest, CourtDescriptionResponse,
  DemandForecastResponse,
  InsightsRequest, InsightsResponse,
  NoShowRiskBatchRequest, NoShowRiskBatchResponse,
  ParseSearchRequest, ParseSearchResponse,
} from './api-types';

async function postJson<TReq, TRes>(path: string, body: TReq): Promise<TRes> {
  const res = await fetch(`/api/${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST /api/${path} failed: ${res.status}`);
  return res.json();
}

async function getJson<TRes>(path: string): Promise<TRes> {
  const res = await fetch(`/api/${path}`);
  if (!res.ok) throw new Error(`GET /api/${path} failed: ${res.status}`);
  return res.json();
}

export const aiParseSearch = (req: ParseSearchRequest) =>
  postJson<ParseSearchRequest, ParseSearchResponse>('ai/parse-search', req);

export const aiInsights = (req: InsightsRequest) =>
  postJson<InsightsRequest, InsightsResponse>('ai/insights', req);

export const aiCourtDescription = (req: CourtDescriptionRequest) =>
  postJson<CourtDescriptionRequest, CourtDescriptionResponse>('ai/court-description', req);

export const mlDemandForecast = () =>
  getJson<DemandForecastResponse>('ml/demand-forecast');

export const mlNoshowRiskBatch = (req: NoShowRiskBatchRequest) =>
  postJson<NoShowRiskBatchRequest, NoShowRiskBatchResponse>('ml/noshow-risk/batch', req);
```

- [ ] **Step 4: Verify build still passes.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

Expected: exit 0.

- [ ] **Step 5: End-to-end proxy smoke (requires FastAPI running).**

```bash
# Terminal 1 (leave running)
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT uvicorn main:app --port 8000

# Terminal 2
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm dev &
sleep 6
curl -sf http://localhost:3000/api/health
kill %1 2>/dev/null || true
```

Expected: `{"status":"ok"}`. (The proxy at `/api/[...path]` forwards `/api/health` → `http://localhost:8000/health`.)

- [ ] **Step 6: Commit.**

```bash
git add apps/web/app/api apps/web/lib/api-client.ts apps/web/lib/api-types.ts
git commit -m "feat(web): Next.js proxy + typed API client

apps/web/app/api/[...path]/route.ts forwards every method to NEXT_API_TARGET
(defaults to http://localhost:8000). lib/api-client.ts wraps each FastAPI
endpoint in a typed function. lib/api-types.ts mirrors apps/api/schemas/."
```

---

## Task 9: Wire `/owner/insights` page (AI Summary + heatmap)

**Files:**
- Modify: `apps/web/app/owner/insights/page.tsx`
- Modify: `apps/web/package.json` (add `react-markdown`)

- [ ] **Step 1: Install `react-markdown`.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm add react-markdown
```

- [ ] **Step 2: Replace the body of `apps/web/app/owner/insights/page.tsx`** with the wired-up version. Keep the original imports and add: `useEffect`, `Markdown` from `react-markdown`, `aiInsights`, `mlDemandForecast`, and types:

```tsx
'use client';
import { useEffect, useState } from 'react';
import Markdown from 'react-markdown';
import { Button } from '@/components/Button';
import { AITag, Eyebrow, StatusBadge } from '@/components/Tags';
import { DemandHeatmap } from '@/components/owner/DemandHeatmap';
import {
  DEMAND_FORECAST, DISTRICT_DEMAND, PEAK_UTILIZATION_BARS,
  WEEKLY_UTILIZATION, OWNER_BOOKINGS,
} from '@/lib/owner-mock-data';
import { aiInsights, mlDemandForecast } from '@/lib/api-client';
import type { DemandCell } from '@/lib/api-types';

const LEVEL_TO_STATUS: Record<string, 'confirmed' | 'progress' | 'cancelled'> = {
  Peak: 'confirmed', Moderate: 'progress', Saturated: 'cancelled',
};

export default function InsightsPage() {
  const [summary, setSummary] = useState('');
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [summaryError, setSummaryError] = useState<string | null>(null);
  const [heatmap, setHeatmap] = useState<DemandCell[]>(DEMAND_FORECAST);
  const [heatmapFromApi, setHeatmapFromApi] = useState(false);

  useEffect(() => {
    mlDemandForecast()
      .then((res) => {
        if (res.cells.length > 0) {
          setHeatmap(res.cells);
          setHeatmapFromApi(true);
        }
      })
      .catch(() => { /* keep mock fallback */ });
  }, []);

  async function generate() {
    setSummaryLoading(true);
    setSummaryError(null);
    try {
      const weekly_utilization = Object.fromEntries(
        WEEKLY_UTILIZATION.map((w) => [w.day, w.pct]),
      );
      const res = await aiInsights({
        weekly_utilization,
        district_demand: DISTRICT_DEMAND,
        owner_bookings: OWNER_BOOKINGS.map((b) => ({
          customer: b.customer, sport: b.sport, status: b.status,
        })),
      });
      setSummary(res.markdown);
    } catch (e) {
      setSummaryError('Could not generate summary. Is the API running?');
    } finally {
      setSummaryLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-5">
      <div className="flex justify-between items-end">
        <div className="flex items-center gap-3">
          <h1 className="font-display text-3xl font-bold">AI Insights</h1>
          <AITag>ELITE VENUE PARTNER</AITag>
        </div>
        <div className="flex gap-2">
          <Button variant="primary" icon="smart_toy" onClick={generate} disabled={summaryLoading}>
            {summaryLoading ? 'Generating…' : 'Generate AI Summary'}
          </Button>
          <Button variant="secondary" onClick={() => setSummary('')}>Clear</Button>
        </div>
      </div>

      {summaryError && (
        <div className="zpots-card p-3 text-sm text-red-700">{summaryError}</div>
      )}

      {summary && (
        <div className="zpots-card-surface p-4">
          <AITag>AI GENERATED SUMMARY</AITag>
          <div className="mt-2 text-sm leading-relaxed prose prose-sm max-w-none">
            <Markdown>{summary}</Markdown>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="zpots-card p-5">
          <h3 className="font-semibold">Bangkok Demand Heatmap</h3>
          <Eyebrow>
            {heatmapFromApi ? '7-DAY FORECAST · LIVE FROM MODEL' : '7-DAY FORECAST · CACHED'}
          </Eyebrow>
          <div className="mt-3">
            <DemandHeatmap data={heatmap} />
          </div>
        </div>
        <div className="zpots-card p-5">
          <h3 className="font-semibold">Peak Utilization</h3>
          <Eyebrow>HOURLY DISTRIBUTION</Eyebrow>
          <div className="flex items-end gap-[3px] h-24 mt-3">
            {PEAK_UTILIZATION_BARS.map((v, i) => (
              <div key={i} className="flex-1 rounded-t" style={{
                height: `${v}%`,
                background: v > 80 ? '#CFFC00' : v > 50 ? '#2E6B00' : '#A5D6A7',
              }} />
            ))}
          </div>
          <div className="mt-3 zpots-card-surface p-3 flex justify-between">
            <div><span className="text-zpots-lime">⚡</span> <strong>Golden Slot</strong></div>
            <span className="font-display font-bold text-zpots-moss">฿2,400/hr</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        {DISTRICT_DEMAND.map((d) => (
          <div key={d.name} className="zpots-card-surface p-4 text-center">
            <Eyebrow>{d.name}</Eyebrow>
            <div className="font-display text-2xl font-bold my-1">{d.demand}%</div>
            <StatusBadge status={LEVEL_TO_STATUS[d.level]}>{d.level}</StatusBadge>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="zpots-card p-5 min-h-[260px] flex flex-col">
          <h3 className="font-semibold">No-Show Risk Analysis ⚠️</h3>
          <span className="font-eyebrow text-[10px] uppercase tracking-wider mt-1" style={{ color: '#b02500' }}>
            PRIORITY: HIGH INTERVENTION
          </span>
          <div className="zpots-card-surface mt-3 p-3 flex justify-between">
            <span>Probable No-Shows</span>
            <span className="font-display text-base">12% <span className="text-xs text-red-700">(+4% WoW)</span></span>
          </div>
          <div className="zpots-card-surface mt-2 p-3 flex-1">
            <Eyebrow>PRIMARY ROOT CAUSE</Eyebrow>
            <div className="text-sm mt-1">Traffic delays on Rama IV during rain predicted (70% probability).</div>
          </div>
        </div>
        <div className="zpots-card-surface p-5 min-h-[260px] flex flex-col">
          <h3 className="font-semibold">AI Mitigation Strategies</h3>
          <div className="flex gap-3 flex-1 mt-3">
            <div className="zpots-card p-3 flex-1">
              <h4 className="text-sm font-bold">Smart Reschedule</h4>
              <p className="text-xs text-zpots-muted leading-snug mt-1">Auto-offer 15-min delay window to users in high-traffic zones.</p>
              <span className="font-eyebrow text-[10px] uppercase tracking-wider" style={{ color: '#506300' }}>+23% RETENTION</span>
            </div>
            <div className="zpots-card p-3 flex-1">
              <h4 className="text-sm font-bold">Pre-Check Deposit</h4>
              <p className="text-xs text-zpots-muted leading-snug mt-1">20% commitment fee for high-demand Saturday slots.</p>
              <span className="font-eyebrow text-[10px] uppercase tracking-wider" style={{ color: '#506300' }}>-60% NO-SHOWS</span>
            </div>
          </div>
          <Button variant="primary" className="w-full justify-center mt-3">Execute All</Button>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 3: Verify build still passes.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

- [ ] **Step 4: Commit.**

```bash
git add apps/web/app/owner/insights/page.tsx apps/web/package.json apps/web/pnpm-lock.yaml
git commit -m "feat(web): wire /owner/insights to live AI + ML endpoints

Generate AI Summary calls /api/ai/insights, renders markdown via
react-markdown. Demand heatmap loads from /api/ml/demand-forecast on
mount; falls back to mock DEMAND_FORECAST on API error. Eyebrow label
shows LIVE FROM MODEL vs CACHED so the source is visible."
```

---

## Task 10: Wire `/owner/bookings` page (no-show risk)

**Files:**
- Modify: `apps/web/app/owner/bookings/page.tsx`

- [ ] **Step 1: Replace the file with the wired version:**

```tsx
'use client';
import { useEffect, useState } from 'react';
import { RevenueBanner } from '@/components/owner/RevenueBanner';
import { StatusBadge, Eyebrow } from '@/components/Tags';
import { OWNER_BOOKINGS } from '@/lib/owner-mock-data';
import { mlNoshowRiskBatch } from '@/lib/api-client';
import type { NoShowRiskResult } from '@/lib/api-types';

const STATUS_TO_VARIANT: Record<string, 'confirmed' | 'completed' | 'cancelled'> = {
  BOOKED: 'confirmed',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
};

const TIER_TO_VARIANT: Record<string, 'confirmed' | 'progress' | 'cancelled'> = {
  Low: 'confirmed', Medium: 'progress', High: 'cancelled',
};

const SPORT_TO_DISTRICT: Record<string, string> = {
  Padel: 'Sukhumvit', Tennis: 'Pathumwan', Soccer: 'Thong Lor', Yoga: 'Ari',
};

function parseHour(time: string): number {
  const m = /^(\d{2}):/.exec(time);
  return m ? parseInt(m[1], 10) : 18;
}

export default function BookingDashboardPage() {
  const [risks, setRisks] = useState<NoShowRiskResult[] | null>(null);

  useEffect(() => {
    mlNoshowRiskBatch({
      items: OWNER_BOOKINGS.map((b) => ({
        sport: b.sport,
        district: SPORT_TO_DISTRICT[b.sport] ?? 'Sukhumvit',
        hour: parseHour(b.time),
      })),
    })
      .then((res) => setRisks(res.results))
      .catch(() => setRisks(null));
  }, []);

  return (
    <div className="flex flex-col gap-5">
      <h1 className="font-display text-3xl font-bold">Bookings</h1>

      <RevenueBanner
        total={4280}
        delta="+15.6% from yesterday · Upcoming"
        breakdown={[
          { label: 'MAIN ARENA',  amount: 1240 },
          { label: 'PADEL POD 2', amount:  890 },
          { label: 'INDOOR TURF', amount: 2150, highlight: true },
        ]}
      />

      <div className="flex gap-2">
        <button className="chip chip-selected">Today</button>
        <button className="chip chip-default">This Week</button>
        <button className="chip chip-default">Calendar</button>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <select className="field-input"><option>All Venues</option><option>Main Arena</option><option>Padel Pod 2</option><option>Indoor Turf</option></select>
        <select className="field-input"><option>Time Descending</option><option>Time Ascending</option><option>Status</option></select>
      </div>

      <div className="grid grid-cols-[2fr_2fr_1fr_1fr] gap-3 px-4 py-3">
        <Eyebrow>Customer</Eyebrow>
        <Eyebrow>Session info</Eyebrow>
        <Eyebrow>Status</Eyebrow>
        <Eyebrow>Risk</Eyebrow>
      </div>

      <div className="flex flex-col gap-2">
        {OWNER_BOOKINGS.map((b, i) => {
          const risk = risks?.[i];
          return (
            <div key={b.member_id} className="zpots-card grid grid-cols-[2fr_2fr_1fr_1fr] gap-3 items-center p-3">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-full text-white flex items-center justify-center font-semibold" style={{ background: b.avatar_color }}>{b.customer[0]}</div>
                <div>
                  <div className="font-semibold text-sm">{b.customer}</div>
                  <div className="text-xs text-zpots-muted">Member ID: {b.member_id}</div>
                </div>
              </div>
              <div>
                <div className="text-sm">🏟 {b.court} • {b.sport}</div>
                <div className="text-xs text-zpots-muted">🕐 {b.time}</div>
              </div>
              <StatusBadge status={STATUS_TO_VARIANT[b.status] ?? 'confirmed'}>{b.status}</StatusBadge>
              {risk ? (
                <StatusBadge status={TIER_TO_VARIANT[risk.tier]}>
                  {risk.tier} ({(risk.probability * 100).toFixed(0)}%)
                </StatusBadge>
              ) : (
                <span className="text-xs text-zpots-muted">—</span>
              )}
            </div>
          );
        })}
      </div>

      <div className="text-xs text-zpots-muted">SHOWING {OWNER_BOOKINGS.length} BOOKINGS · seeded demo data</div>
    </div>
  );
}
```

- [ ] **Step 2: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

- [ ] **Step 3: Commit.**

```bash
git add apps/web/app/owner/bookings/page.tsx
git commit -m "feat(web): wire /owner/bookings no-show risk to live ML endpoint

On mount, batch-call /api/ml/noshow-risk/batch with one item per
booking, populate the Risk column. Shows '—' until response. Falls back
silently to '—' on API error (was previously a sport-derived stub)."
```

---

## Task 11: Wire `/owner/venues/[id]/edit` (court description)

**Files:**
- Modify: `apps/web/components/owner/CourtForm.tsx`

- [ ] **Step 1: In `apps/web/components/owner/CourtForm.tsx`, replace the Generate Description button's onClick with a real call.** Find:

```tsx
<Button variant="primary" className="mt-2" type="button"
        onClick={() => setDescription('A premium climate-controlled venue with elite-grade equipment, located in the heart of Bangkok. Open daily 06:00–23:00.')}>
  <AITag>AI</AITag> Generate Description
</Button>
```

Replace with:

```tsx
<Button variant="primary" className="mt-2" type="button"
        disabled={descLoading}
        onClick={async () => {
          setDescLoading(true);
          try {
            const res = await aiCourtDescription({ name, sport, surface, location, amenities });
            setDescription(res.description);
          } catch {
            setDescription('Unable to generate description. Is the API running?');
          } finally {
            setDescLoading(false);
          }
        }}>
  <AITag>AI</AITag> {descLoading ? 'Generating…' : 'Generate Description'}
</Button>
```

- [ ] **Step 2: Add the import and the `descLoading` state.** At the top of the file:

```tsx
import { aiCourtDescription } from '@/lib/api-client';
```

Inside `CourtForm`, near the other `useState` calls:

```tsx
const [descLoading, setDescLoading] = useState(false);
```

- [ ] **Step 3: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

- [ ] **Step 4: Commit.**

```bash
git add apps/web/components/owner/CourtForm.tsx
git commit -m "feat(web): wire Generate Description to /api/ai/court-description

Was a hardcoded blurb; now calls the FastAPI endpoint with the form's
current values. Loading state on the button. Friendly error message in
the textarea on API failure."
```

---

## Task 12: Wire `/player/search` (parse-search)

**Files:**
- Modify: `apps/web/app/player/search/page.tsx`

- [ ] **Step 1: In `apps/web/app/player/search/page.tsx`, replace the Search button's onClick** so it actually calls the parser. Find the no-op:

```tsx
<Button variant="primary" onClick={() => { /* AI parse: Phase 3 */ }}>Search</Button>
```

Replace with:

```tsx
<Button variant="primary" disabled={searchLoading} onClick={async () => {
  if (!query.trim()) return;
  setSearchLoading(true);
  try {
    const parsed = await aiParseSearch({ query });
    const next = new URLSearchParams(params.toString());
    if (parsed.sport) next.set('sport', parsed.sport); else next.delete('sport');
    if (parsed.district) next.set('district', parsed.district); else next.delete('district');
    if (parsed.max_price !== null) next.set('max_price', String(parsed.max_price)); else next.delete('max_price');
    router.push(`/player/search?${next.toString()}`);
  } catch {
    // silent — user can still type and filter manually
  } finally {
    setSearchLoading(false);
  }
}}>{searchLoading ? 'Parsing…' : 'Search'}</Button>
```

- [ ] **Step 2: Add the import and state at the top of `SearchPageInner`:**

```tsx
import { aiParseSearch } from '@/lib/api-client';
// ...
const [searchLoading, setSearchLoading] = useState(false);
```

- [ ] **Step 3: Verify build.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm build
```

- [ ] **Step 4: Commit.**

```bash
git add apps/web/app/player/search/page.tsx
git commit -m "feat(web): wire /player/search natural-language input to AI parser

Submit calls /api/ai/parse-search, merges {sport, district, max_price}
into URL params so the existing chip filters update. Silent on parse
failure — typed value stays in the input."
```

---

## Task 13: Final smoke + open PR

- [ ] **Step 1: Run all automated checks.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS

# Streamlit
conda run -n MADT pytest tests/ -q

# FastAPI
cd apps/api && conda run -n MADT pytest -q && cd ..

# Vitest + Playwright (Playwright spec set unchanged — should still pass)
cd apps/web && pnpm test:unit && pnpm build && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm test
cd ../..
```

Expected:
- Streamlit pytest: 29 passed
- FastAPI pytest: 8 passed
- Vitest: 31 passed
- pnpm build: exit 0
- Playwright: 3 passed (landing + player-flow + owner-flow)

- [ ] **Step 2: Manual browser smoke (requires Azure env vars in dev.env).**

Open two terminals:

```bash
# Terminal A
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT uvicorn main:app --reload --port 8000

# Terminal B
cd /Users/nchawanp/Desktop/ZPOTS/apps/web && pnpm dev
```

Open http://localhost:3000 in Chrome and verify:

1. `/owner/insights` → click "Generate AI Summary" → markdown appears (not the seeded mock string).
2. `/owner/insights` heatmap → eyebrow shows "LIVE FROM MODEL" (not "CACHED").
3. `/owner/bookings` → Risk column populates with `Low (12%)` / `Medium (34%)` / etc. (not stub).
4. `/owner/venues/bbc-01/edit` → click "Generate Description" → AI text appears in the textarea.
5. `/player/search` → type "badminton sukhumvit evening under 400", click Search → URL updates to `?sport=Badminton&district=Sukhumvit&max_price=400`, chips reflect new filters.

- [ ] **Step 3: Smoke graceful degradation.** Stop the FastAPI (`Ctrl+C` in Terminal A). Reload `/owner/insights`. Heatmap should still render (mock fallback). Click Generate AI Summary → error message appears, page does not crash.

- [ ] **Step 4: Confirm Streamlit at the root still runs unchanged.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS && conda run -n MADT streamlit run app.py
```

Open http://localhost:8501 — landing renders normally.

- [ ] **Step 5: Push and open PR.**

```bash
git push -u origin feat/nextjs-phase3b
gh pr create --base main --title "Phase 3b: FastAPI scaffold + AI helper endpoints" --body-file ...
```

PR body should mention:
- Link to spec + this plan
- Test counts (Streamlit 29, FastAPI 8, Vitest 31, Playwright 3)
- Local dev: 2 terminals (uvicorn + pnpm dev)
- Deploy story (Cloud Run, deferred to Phase 4 per `2026-05-17-deployment-gcp-cloud-run.md`)
- Confirmation that legacy Streamlit + Phase 2 player + Phase 3a owner all still work
- That Azure env vars are needed in `dev.env` for the live AI endpoints to actually return content (otherwise falls back to error toast / cached mock)

---

## Out of scope for 3b (do NOT add)

- Chat agents (port + streaming widget) — Phase 3c
- NextAuth — Phase 4
- Postgres — Phase 4
- Dockerfiles + Cloud Run deploy — Phase 4
- E2E tests against real Azure
- Streaming AI responses
- OpenAPI → TS codegen
- A `pnpm dev:all` convenience script
- Cancel/reschedule a player's booking from the owner side
- Real `Execute All` button on the AI mitigation card
