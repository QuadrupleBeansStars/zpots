from fastapi import FastAPI

from routers import ai, health

app = FastAPI(
    title="ZPOTS API",
    description="OpenAI/Azure helpers + ML inference for the Next.js frontend.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(ai.router)
