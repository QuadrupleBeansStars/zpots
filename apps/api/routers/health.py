from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Liveness probe. Used by Cloud Scheduler to keep the container warm in Phase 4."""
    return {"status": "ok"}
