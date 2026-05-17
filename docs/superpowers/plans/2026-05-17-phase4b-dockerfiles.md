# Phase 4b — Dockerfiles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Containerize FastAPI + Next.js with multi-stage Dockerfiles and a docker-compose.yml that runs the full stack locally, so 4c (Cloud Run) starts with verified images.

**Architecture:** Two Dockerfiles (build context = repo root so the API image can include `ml/models/`), two `.dockerignore` files, one `docker-compose.yml`. No conda in images (pip only). Next.js uses `output: 'standalone'` to keep the runtime image slim. ML artifact path made env-var-driven so the same code works locally and in-container.

**Tech Stack:** Docker · Docker Compose · python:3.11-slim · node:20-alpine · pnpm · pip · uvicorn · Next.js standalone

**Reference spec:** `docs/superpowers/specs/2026-05-17-phase4b-dockerfiles-design.md`
**Branch:** create `feat/nextjs-phase4b` off main

---

## File structure (end of Phase 4b)

```
apps/api/
├── Dockerfile             # NEW — multi-stage: builder → runtime
├── .dockerignore          # NEW
└── ml/inference.py        # MODIFIED — ZPOTS_ML_DIR env override

apps/web/
├── Dockerfile             # NEW — multi-stage: deps → builder → runner
├── .dockerignore          # NEW
└── next.config.ts         # MODIFIED — output: 'standalone'

docker-compose.yml         # NEW
```

---

## Task 0: Branch + sanity baseline

- [ ] **Step 1: Cut branch.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS && git checkout main && git pull && git checkout -b feat/nextjs-phase4b
```

- [ ] **Step 2: Confirm Docker is running.**

```bash
docker version >/dev/null 2>&1 && echo "docker ok" || echo "START DOCKER FIRST"
```

If "START DOCKER FIRST", launch Docker Desktop and rerun before continuing.

- [ ] **Step 3: Baseline test suite to confirm pre-4b state is green.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest -q
```

Expected: **53 passed** (Phase 4a baseline). Anything else means a prior phase broke something — stop and investigate.

---

## Task 1: Patch `ml/inference.py` to honor `ZPOTS_ML_DIR`

**Files:**
- Modify: `apps/api/ml/inference.py:9-12`

This patch must land before the API Dockerfile, because the Dockerfile copies `ml/models/` to `/ml/models/` (absolute path) and sets `ZPOTS_ML_DIR=/ml/models`. Without the patch, the container's `ML_DIR` would compute a broken relative path.

- [ ] **Step 1: Edit `/Users/nchawanp/Desktop/ZPOTS/apps/api/ml/inference.py`.** Replace lines 9–12 (the current `ML_DIR = os.path.join(...)` block) with:

```python
ML_DIR = os.environ.get(
    "ZPOTS_ML_DIR",
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        "ml", "models",
    ),
)
```

The fallback is the existing path — local dev with `ZPOTS_ML_DIR` unset keeps working.

- [ ] **Step 2: Run the API test suite to confirm nothing regressed.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/api && conda run -n MADT pytest -q
```

Expected: **53 passed**.

- [ ] **Step 3: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/api/ml/inference.py
git commit -m "feat(api): ZPOTS_ML_DIR env override for ml artifact location

Lets Docker point ML_DIR at /ml/models without the runtime path math
walking out of the container root. Local dev unaffected (env unset
keeps the existing relative path)."
```

---

## Task 2: API `.dockerignore`

**Files:**
- Create: `apps/api/.dockerignore`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/.dockerignore`:**

```
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
htmlcov/
tests/
conftest.py
*.md
```

The `tests/` and `conftest.py` exclusion keeps `pytest` (a build-only dep) out of the production image. `*.md` excludes `apps/api/README.md`.

- [ ] **Step 2: Commit.**

```bash
git add apps/api/.dockerignore
git commit -m "build(api): .dockerignore (drop tests, caches, docs from image context)"
```

---

## Task 3: `apps/api/Dockerfile`

**Files:**
- Create: `apps/api/Dockerfile`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/api/Dockerfile`:**

```dockerfile
# Build from repo root: docker build -f apps/api/Dockerfile -t zpots-api .

# ---- Stage 1: builder -----------------------------------------------------
FROM python:3.11-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc \
    && rm -rf /var/lib/apt/lists/*
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Stage 2: runtime -----------------------------------------------------
FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/app/.local/bin:$PATH \
    PORT=8000

RUN useradd --create-home --uid 1000 app
USER app
WORKDIR /app

COPY --from=builder --chown=app:app /root/.local /home/app/.local
COPY --chown=app:app apps/api/ ./
COPY --chown=app:app ml/models/ /ml/models/

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD python -c "import urllib.request,os,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:' + os.environ.get('PORT','8000') + '/health').status == 200 else 1)" || exit 1
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
```

- [ ] **Step 2: Build the image (from repo root).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
docker build -f apps/api/Dockerfile -t zpots-api .
```

Expected: build finishes successfully. First build takes 1-3 minutes (pip install scikit-learn / pandas).

- [ ] **Step 3: Smoke run.**

```bash
docker run --rm -d --name zpots-api-smoke -p 8000:8000 --env-file dev.env zpots-api
sleep 4
curl -s localhost:8000/health
echo
curl -s localhost:8000/courts | head -c 200
echo
docker stop zpots-api-smoke
```

Expected: `/health` returns `{"status":"ok"}` (or similar 200), `/courts` returns the first ~200 chars of the JSON court list starting with `[{`.

- [ ] **Step 4: Image-size sanity.**

```bash
docker images zpots-api --format '{{.Size}}'
```

Expected: under 600 MB. (Note: 250 MB target in spec was optimistic — scikit-learn + pandas + pyarrow are heavy. 400-550 MB is normal; flag if over 700 MB.)

- [ ] **Step 5: Commit.**

```bash
git add apps/api/Dockerfile
git commit -m "build(api): multi-stage Dockerfile (python:3.11-slim, non-root, healthcheck)

Builder stage installs deps with build-essentials, runtime stage copies
the site-packages tree and runs as uid 1000. PORT env honored for
Cloud Run. ml/models/ copied to /ml/models/ (paired with the
ZPOTS_ML_DIR env override from the prior commit)."
```

---

## Task 4: Web `.dockerignore`

**Files:**
- Create: `apps/web/.dockerignore`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/.dockerignore`:**

```
node_modules/
.next/
.turbo/
test-results/
playwright-report/
*.log
.DS_Store
*.md
.env*.local
```

Excludes the local dev build output (`.next/`) and Playwright artifacts so they never leak into the image context.

- [ ] **Step 2: Commit.**

```bash
git add apps/web/.dockerignore
git commit -m "build(web): .dockerignore (drop local build output + playwright artifacts)"
```

---

## Task 5: Enable Next.js standalone output

**Files:**
- Modify: `apps/web/next.config.ts`

- [ ] **Step 1: Replace `/Users/nchawanp/Desktop/ZPOTS/apps/web/next.config.ts`** with:

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
};

export default nextConfig;
```

- [ ] **Step 2: Verify the local build still works and emits the standalone bundle.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS/apps/web
lsof -ti :3000 | xargs kill -9 2>/dev/null
pnpm build
ls .next/standalone/server.js
```

Expected: build succeeds; `.next/standalone/server.js` exists.

- [ ] **Step 3: Commit.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
git add apps/web/next.config.ts
git commit -m "build(web): output: 'standalone' for slim docker runtime image"
```

---

## Task 6: `apps/web/Dockerfile`

**Files:**
- Create: `apps/web/Dockerfile`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/apps/web/Dockerfile`:**

```dockerfile
# Build from repo root: docker build -f apps/web/Dockerfile -t zpots-web .

# ---- Stage 1: deps (cached on lockfile) -----------------------------------
FROM node:20-alpine AS deps
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY apps/web/package.json apps/web/pnpm-lock.yaml apps/web/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile

# ---- Stage 2: builder -----------------------------------------------------
FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY --from=deps /app/node_modules ./node_modules
COPY apps/web/ ./
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm build

# ---- Stage 3: runner (tiny) -----------------------------------------------
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOSTNAME=0.0.0.0

RUN addgroup -S app && adduser -S -G app app
USER app

COPY --from=builder --chown=app:app /app/.next/standalone ./
COPY --from=builder --chown=app:app /app/.next/static ./.next/static
COPY --from=builder --chown=app:app /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

- [ ] **Step 2: Build the image (from repo root).**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
docker build -f apps/web/Dockerfile -t zpots-web .
```

Expected: build succeeds. 2-4 minutes first time.

- [ ] **Step 3: Smoke run** (no API running — just verify the web image boots).

```bash
docker run --rm -d --name zpots-web-smoke -p 3000:3000 \
    -e NEXT_API_TARGET=http://host.docker.internal:8000 zpots-web
sleep 3
curl -sI localhost:3000/ | head -1
docker stop zpots-web-smoke
```

Expected: `HTTP/1.1 200 OK`. (API will be unreachable from inside; the landing page still renders because it doesn't call the API.)

- [ ] **Step 4: Image-size sanity.**

```bash
docker images zpots-web --format '{{.Size}}'
```

Expected: under 300 MB.

- [ ] **Step 5: Commit.**

```bash
git add apps/web/Dockerfile
git commit -m "build(web): multi-stage Dockerfile (node:20-alpine, standalone, non-root)

deps stage cached on pnpm-lock; builder runs pnpm build; runner copies
only .next/standalone + .next/static + public. HOSTNAME=0.0.0.0 so the
container is reachable; PORT env honored for Cloud Run."
```

---

## Task 7: `docker-compose.yml`

**Files:**
- Create: `docker-compose.yml`

- [ ] **Step 1: Create `/Users/nchawanp/Desktop/ZPOTS/docker-compose.yml`:**

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

- [ ] **Step 2: Bring the stack up.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS
lsof -ti :3000 | xargs kill -9 2>/dev/null
lsof -ti :8000 | xargs kill -9 2>/dev/null
docker compose up --build -d
sleep 8
docker compose ps
```

Expected: both `api` and `web` show `Up`, with `api` showing `(healthy)`.

- [ ] **Step 3: Verify the proxy chain works (web → api).**

```bash
# api directly
curl -s localhost:8000/courts | jq length
# web proxy → api
curl -s localhost:3000/api/courts | jq length
```

Expected: both return `6`.

- [ ] **Step 4: Tear down.**

```bash
docker compose down
```

- [ ] **Step 5: Commit.**

```bash
git add docker-compose.yml
git commit -m "build: docker-compose.yml for full-stack local testing

api + web on shared network. Web proxy points to http://api:8000.
api env_file: dev.env. depends_on healthy so the first page load
doesn't 502. NOT a dev environment — pnpm dev + uvicorn stay the
local-dev workflow."
```

---

## Task 8: Final smoke + open PR

- [ ] **Step 1: Full automated test suite still green.**

```bash
cd /Users/nchawanp/Desktop/ZPOTS

# Streamlit
conda run -n MADT pytest tests/ -q

# FastAPI
cd apps/api && conda run -n MADT pytest -q && cd ..

# Vitest + build + Playwright
cd apps/web && pnpm test:unit && pnpm build && lsof -ti :3000 | xargs kill -9 2>/dev/null; pnpm test
cd ../..
```

Expected: Streamlit 29 / FastAPI 53 / Vitest 30 / pnpm build clean / Playwright 3.

- [ ] **Step 2: Manual end-to-end browser smoke through the compose stack.**

```bash
docker compose up --build -d
# Browser → http://localhost:3000
```

Verify (sign-in flow + chat flow):
- [ ] `/player/search` shows 6 courts from API
- [ ] Player chat: "book bbc-01 tomorrow 6pm for 1 hour" → Confirm → ✅ Booked
- [ ] `/player/bookings` shows the new booking (persisted in API container's in-memory store)
- [ ] `/owner/bookings` shows the same booking
- [ ] Owner chat: "what's my revenue this week?" → returns a number
- [ ] `docker compose restart api` → reload `/player/bookings` → step-2 booking is gone (in-memory reset, intended)

```bash
docker compose down
```

- [ ] **Step 3: Confirm legacy local dev still works** (not touched, but verify).

```bash
cd apps/api && conda run -n MADT uvicorn main:app --port 8000 &
cd ../web && pnpm dev &
sleep 5
curl -sI localhost:3000/ | head -1
kill %1 %2 2>/dev/null
```

Expected: 200 OK from `localhost:3000`.

- [ ] **Step 4: Push + open PR.**

```bash
git push -u origin feat/nextjs-phase4b
gh pr create --base main --title "Phase 4b: Dockerfiles + compose stack" --body "$(cat <<'EOF'
## Summary

Phase 4b — production-ready containers for both ZPOTS services + a docker-compose stack for local end-to-end verification. Sets up everything 4c (Cloud Run) needs.

- Spec: \`docs/superpowers/specs/2026-05-17-phase4b-dockerfiles-design.md\`
- Plan: \`docs/superpowers/plans/2026-05-17-phase4b-dockerfiles.md\`

## What ships

| File | Purpose |
|---|---|
| \`apps/api/Dockerfile\` | python:3.11-slim, multi-stage builder→runtime, non-root, /health probe, \$PORT honored |
| \`apps/api/.dockerignore\` | excludes tests/caches |
| \`apps/api/ml/inference.py\` | \`ZPOTS_ML_DIR\` env override (fallback = existing relative path) |
| \`apps/web/Dockerfile\` | node:20-alpine, 3-stage deps→builder→runner, standalone output, non-root |
| \`apps/web/.dockerignore\` | excludes .next, test artifacts |
| \`apps/web/next.config.ts\` | \`output: 'standalone'\` for slim runtime |
| \`docker-compose.yml\` | api + web with health-gated startup |

## Tests

| Suite | Result |
|---|---|
| Streamlit \`pytest tests/\` | 29 / 29 ✅ |
| FastAPI \`pytest apps/api\` | 53 / 53 ✅ |
| Vitest | 30 / 30 ✅ |
| Playwright | 3 / 3 ✅ |
| \`docker compose up\` end-to-end | manual ✅ |

## Image sizes (sanity)

- zpots-api: ~450 MB (sklearn + pandas + pyarrow are heavy; acceptable)
- zpots-web: ~200 MB (Next.js standalone)

## Test plan (verifier should run)

\`\`\`bash
docker compose up --build
# http://localhost:3000 → player books → owner sees it → restart api → reset
\`\`\`

## What's NOT in this PR

- Cloud Run service config — Phase 4c
- Image push to registry — Phase 4c
- CI auto-build on PR — later phase
- Multi-arch buildx — Cloud Run is amd64-only

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Return the PR URL.

---

## Out of scope for Phase 4b (do NOT add)

- Cloud Run service config / IAM / domain mapping → Phase 4c
- Image push to gcr.io or Artifact Registry → Phase 4c
- CI workflow that builds on PR → later
- Multi-arch buildx → Cloud Run is amd64
- Production secret manager (Google Secret Manager) → Phase 4c
- Hot-reload volumes in compose (compose is for prod-image verification, not dev)
- Streamlit containerization (stays on Streamlit Cloud / local)
