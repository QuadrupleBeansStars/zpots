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
