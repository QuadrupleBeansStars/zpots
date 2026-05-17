# Phase 4b — Dockerfiles Design

**Status:** approved 2026-05-17
**Sub-phase of:** Phase 4 (deploy). Prior: 4a seed data layer. Next: 4c Cloud Run deploy.
**Out of scope:** image registry push, CI workflows, multi-arch builds, Cloud Run config.

## Goal

Containerize both ZPOTS services (FastAPI + Next.js) with production-ready multi-stage Dockerfiles, plus a `docker-compose.yml` that runs the full stack locally so the images can be verified end-to-end before Cloud Run deploy in 4c.

## Motivation

4c needs container images to deploy to Cloud Run. Without working Dockerfiles, every iteration on the deploy spec is gated on first writing them. Splitting this out keeps 4c focused on Cloud Run config and IAM, not Dockerfile debugging. The compose file is a cheap insurance policy — it surfaces image bugs (wrong paths, missing files, broken env-var wiring) on the local machine instead of in a Cloud Build log.

## Architecture

Two Dockerfiles, one compose file, two `.dockerignore` files. Build context for both Dockerfiles is the **repo root** so the API image can include `ml/models/` (the joblib artifacts live there, outside `apps/api/`).

```
apps/api/Dockerfile          # multi-stage: builder → runtime
apps/api/.dockerignore       # __pycache__, .pytest_cache, tests
apps/web/Dockerfile          # multi-stage: deps → builder → runner
apps/web/.dockerignore       # node_modules, .next, test-results
docker-compose.yml           # repo root; api + web services
```

**No conda in either image.** Conda is local-dev only ([[project-python-env]]). Docker uses plain `pip` with `apps/api/requirements.txt` — slim, fast, standard.

**No new tests.** Existing 53 FastAPI + 30 Vitest + 3 Playwright suites cover behavior; 4b verifies the containers preserve that behavior.

## Components

### `apps/api/Dockerfile`

Two stages. Builder installs Python deps with build-essentials; runtime is a slim `python:3.11-slim` with only the runtime packages copied across.

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && rm -rf /var/lib/apt/lists/*
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    PATH=/home/app/.local/bin:$PATH PORT=8000

RUN useradd --create-home --uid 1000 app
USER app
WORKDIR /app

COPY --from=builder --chown=app:app /root/.local /home/app/.local
COPY --chown=app:app apps/api/ ./
COPY --chown=app:app ml/models/ /ml/models/

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:'+__import__('os').environ.get('PORT','8000')+'/health').status==200 else 1)" || exit 1
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
```

Non-root user (`app`, uid 1000). `PORT` env var honored so Cloud Run (which sets `$PORT`) needs no Dockerfile change in 4c.

### `apps/api/ml/inference.py` — ML path patch

The existing `ML_DIR` computes a relative path from the source file. That works locally (where the file is four directories deep relative to repo root) but breaks inside the container (where `apps/api/` is copied to `/app/` and `ml/models/` is copied to `/ml/models/`).

Patch to read an env var with the existing relative path as fallback:

```python
ML_DIR = os.environ.get(
    "ZPOTS_ML_DIR",
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        "ml", "models",
    ),
)
```

Local dev: env unset → existing relative path. Docker: env set to `/ml/models` in compose + Cloud Run.

### `apps/api/.dockerignore`

```
__pycache__/
*.pyc
.pytest_cache/
.coverage
tests/
conftest.py
```

Tests are excluded from the production image — they pull in `pytest` which isn't needed at runtime.

### `apps/web/next.config.ts` — standalone output

Add `output: 'standalone'`:

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
};

export default nextConfig;
```

Drops the runtime image from ~800 MB (full `node_modules`) to ~200 MB by emitting a self-contained `.next/standalone/server.js` with only the deps the app actually imports.

### `apps/web/Dockerfile`

Three stages: deps (cached on lockfile), builder, runner (tiny).

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY apps/web/package.json apps/web/pnpm-lock.yaml apps/web/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile

FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY --from=deps /app/node_modules ./node_modules
COPY apps/web/ ./
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1 PORT=3000 HOSTNAME=0.0.0.0

RUN addgroup -S app && adduser -S -G app app
USER app

COPY --from=builder --chown=app:app /app/.next/standalone ./
COPY --from=builder --chown=app:app /app/.next/static ./.next/static
COPY --from=builder --chown=app:app /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

`HOSTNAME=0.0.0.0` is required — Next.js standalone defaults to localhost-only, which makes the container unreachable from outside.

No HEALTHCHECK — Next.js has no built-in `/health` route. Cloud Run probes work without one.

### `apps/web/.dockerignore`

```
node_modules/
.next/
.turbo/
test-results/
playwright-report/
*.log
```

### `docker-compose.yml`

```yaml
services:
  api:
    build:
      context: .
      dockerfile: apps/api/Dockerfile
    env_file: dev.env
    environment:
      ZPOTS_ML_DIR: /ml/models
      PORT: "8000"
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 3s
      start_period: 10s

  web:
    build:
      context: .
      dockerfile: apps/web/Dockerfile
    environment:
      NEXT_API_TARGET: http://api:8000
      PORT: "3000"
    ports:
      - "3000:3000"
    depends_on:
      api:
        condition: service_healthy
```

- `env_file: dev.env` injects Azure OpenAI creds into the api container at runtime; the file is already gitignored, never baked into the image.
- `NEXT_API_TARGET=http://api:8000` — the existing `apps/web/app/api/[...path]/route.ts` proxy reads this env var. From the browser at `localhost:3000`, the proxy server-side calls `http://api:8000` on the Docker network.
- `depends_on: service_healthy` — web waits for api's `/health` to pass before starting, so the first page load doesn't 502.
- Production-image compose, **not** a dev environment. `pnpm dev` + `uvicorn --reload` remain the local-dev workflow.

## Data flow

```
docker compose up
   ├─ api builds: pip install in builder → copy site-packages → copy apps/api + ml/models → uvicorn
   └─ web builds: pnpm install in deps → pnpm build in builder → copy standalone → node server.js

Browser → http://localhost:3000/player/search
   └─ web container: Server Component does await getCourts() → fetch /api/courts
       └─ /api/[...path]/route.ts proxy forwards to ${NEXT_API_TARGET}/courts = http://api:8000/courts
           └─ api container: routers/data.py reads from CourtsStore → 6 courts
```

## Validation

Smoke commands documented in the plan, run during implementation:

```bash
# API image, standalone
docker build -f apps/api/Dockerfile -t zpots-api .
docker run --rm -p 8000:8000 --env-file dev.env zpots-api
curl localhost:8000/health             # → {"status":"ok"}
curl localhost:8000/courts | jq length # → 6

# Web image, standalone
docker build -f apps/web/Dockerfile -t zpots-web .
docker run --rm -p 3000:3000 -e NEXT_API_TARGET=http://host.docker.internal:8000 zpots-web
curl -sI localhost:3000/ | head -1     # → HTTP/1.1 200 OK

# Full stack
docker compose up --build
# Browser → http://localhost:3000, run the manual Phase 4a smoke checklist
```

## Acceptance criteria

1. Both images build clean on a fresh Docker (no cached layers).
2. API image runs with only `dev.env` mounted; `/health`, `/courts`, `/bookings` all return 200.
3. Web image runs and serves `/`; `NEXT_API_TARGET` correctly proxies `/api/*` calls.
4. `docker compose up --build` brings up both; the "player books → owner sees it" loop works end-to-end through containers.
5. Image sizes: API ≤ 250 MB, Web ≤ 250 MB (sanity check via `docker images`).
6. Existing local dev (`pnpm dev` + `uvicorn`) still works unchanged (verified by running both side-by-side).
7. Existing test suites (Streamlit 29, FastAPI 53, Vitest 30, Playwright 3) all still pass.

## Error handling

**Build-time failures:**
- Missing `ml/models/*.pkl` → API image build still succeeds; runtime warns and demand/noshow endpoints return empty (existing behavior).
- Missing `dev.env` → compose errors clearly with "env_file dev.env not found". Document in README.

**Runtime failures:**
- Bad Azure creds → existing `/ai/*` endpoints fail; frontend already degrades gracefully (Phase 3b precedent).
- API container exits → web container's `depends_on` won't have it healthy, so web stays down. Restart `docker compose up` after fixing.

## Out of scope

- Image push to gcr.io / Artifact Registry — Phase 4c
- Cloud Run service config, IAM, networking — Phase 4c
- CI workflow that builds on PR — later phase
- Multi-arch `buildx` for arm64 + amd64 — Cloud Run is amd64, emulation handles the cross-build
- Production secret manager integration — Phase 4c uses GCP Secret Manager
- Volume mounts for hot-reload (compose is for prod-image testing, not dev)
- Legacy Streamlit containerization (Streamlit stays on Streamlit Cloud / local-only)

## Open questions

None.
