from fastapi import FastAPI

from routers import ai, chat, health, ml

app = FastAPI(
    title="ZPOTS API",
    description="OpenAI/Azure helpers + ML inference + chat agents for the Next.js frontend.",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(ai.router)
app.include_router(ml.router)
app.include_router(chat.router)
