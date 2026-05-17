# Deployment — GCP Cloud Run (Deferred to Phase 4)

**Date:** 2026-05-17
**Status:** Decision recorded — actual deployment work happens in Phase 4
**Phase:** target deploy story for the Next.js + FastAPI stack

---

## Decision

Deploy the new stack to **Google Cloud Run** (containerized). Use **Neon** for managed Postgres on its free tier. Keep the legacy Streamlit on Streamlit Cloud running in parallel until Phase 4 ships green.

Chosen over the original handoff brief's "Vercel + Railway" because Cloud Run + Neon is genuinely free at expected demo traffic, while Vercel+Railway runs ~$5/month after the Railway trial expires. The trade-off is more setup (Dockerfiles, `gcloud` CLI) and FastAPI cold-start latency.

---

## Stack mapping

| Piece | Service | Tier |
|---|---|---|
| Next.js frontend (apps/web) | Cloud Run | Free (2M req/mo, 360k GB-s, 180k vCPU-s) |
| FastAPI backend (apps/api) | Cloud Run | Free (same pool, shared across services) |
| Postgres | Neon (external — not GCP) | Free (0.5 GB) |
| Docker images | GCP Artifact Registry | Free (first 500 MB) |
| Secrets (Azure OpenAI keys, DB URL) | Cloud Run env vars + Secret Manager | Secret Manager: 6 secrets free |
| Keep-warm pings | Cloud Scheduler → `/health` every 5 min | Free (3 jobs free per month) |
| ML artifacts (joblib, parquet) | Baked into the FastAPI Docker image | n/a |

Total at low traffic: **$0/month**.

---

## Cold-start mitigation

Cloud Run scales to zero. First request after idle wakes the container:

- Next.js (Node): ~1–3 s cold start. Tolerable.
- FastAPI with sklearn + pandas + joblib loaded: **~5–10 s cold start**. Awkward for demos.

**Mitigation: Cloud Scheduler cron job hits `GET /api/health` on the FastAPI service every 5 minutes.** Keeps the container warm without paying for `--min-instances=1` (which would be ~$25–35/month).

If cold start still bothers the demo experience later, we can flip `--min-instances=1` on just the FastAPI service for the cost above.

---

## What needs to change in the codebase (Phase 4 work, NOT now)

These are deferred — Phase 3b should build the FastAPI such that adding Dockerfiles later is a clean addition, not a refactor.

**Frontend (`apps/web/`):**
- Add `output: 'standalone'` to `next.config.mjs` so the build emits a self-contained server
- Add `apps/web/Dockerfile` (multi-stage: deps → build → runner)
- Add `apps/web/.dockerignore` (exclude `.next/cache`, `node_modules`, `tests/`)
- Use `NEXT_PUBLIC_API_BASE` env var — set to `http://localhost:8000` locally, the Cloud Run service URL in production

**Backend (`apps/api/`):**
- `apps/api/Dockerfile` (`python:3.11-slim`, copy `ml/models/*` in)
- `apps/api/.dockerignore`
- `GET /health` endpoint for Cloud Scheduler pings
- Read `DATABASE_URL`, `AZURE_OPENAI_API_KEY`, `AZURE_API_VERSION`, `AZURE_ENDPOINT`, `AZURE_DEPLOYMENT` from env vars (no `dev.env` in production)

**Deploy automation:**
- One of:
  - Manual `gcloud run deploy --source apps/web` + `gcloud run deploy --source apps/api`
  - `cloudbuild.yaml` triggered by GitHub push (free under Cloud Build's monthly minutes)
  - `make deploy` target for now, automate later

---

## What NOT to do in Phase 3b because of this decision

- No Vercel-specific code (`@vercel/og`, `vercel.json`, Vercel Postgres SDK, etc.)
- No Railway-specific config files
- No `next/font` Vercel-CDN-specific behavior assumptions
- No serverless-function size optimizations (Cloud Run containers don't have the 250 MB limit)

The FastAPI app should be a plain ASGI app under `uvicorn`. No serverless adapters.

---

## Open questions to revisit at Phase 4

1. **Region.** `asia-southeast1` (Jakarta) is closest to Bangkok users. Cold-start cost is the same. Defaults to `us-central1` if unset; explicitly set to `asia-southeast1` at deploy time.
2. **Custom domain.** Cloud Run lets you map a domain free; cert is auto-provisioned. Decide if `zpots.app` (or whatever) is in scope or if Cloud Run's default URL is fine.
3. **GitHub Actions vs Cloud Build.** Cloud Build is free at low usage and lives in GCP. GitHub Actions has its own free tier and lives next to the code. Pick whichever feels less context-switchy.
4. **Backups.** Neon free tier has 7-day point-in-time recovery. Probably enough for v1.

---

## Reference notes

- Cloud Run free tier: https://cloud.google.com/run/pricing#tier (read at decision time, may have changed)
- Neon free tier: 0.5 GB, 5 projects, auto-suspend after 5 min inactivity. ZPOTS will use one project.
- Streamlit Cloud cost: stays $0; we're not removing it.
