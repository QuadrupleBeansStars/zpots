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
