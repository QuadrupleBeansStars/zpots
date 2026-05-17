from contextlib import asynccontextmanager

from fastapi import FastAPI

from data.store import init_stores
from routers import ai, chat, data, health, ml


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Single-instance demo: in-memory stores live for the lifetime of this
    # process. Cloud Run must be configured with min/max instances = 1 so
    # state stays coherent across requests.
    init_stores()
    yield


app = FastAPI(
    title="ZPOTS API",
    description="OpenAI/Azure helpers + ML inference + chat agents + seed-backed data.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(ai.router)
app.include_router(ml.router)
app.include_router(chat.router)
app.include_router(data.router)
