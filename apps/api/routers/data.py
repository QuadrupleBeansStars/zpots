"""HTTP API for the seed-backed data stores."""
from fastapi import APIRouter, HTTPException

from data.store import get_bookings_store, get_courts_store
from schemas.data import Booking, Court, CreateBookingRequest

router = APIRouter(tags=["data"])


@router.get("/courts", response_model=list[Court])
def list_courts() -> list[dict]:
    return get_courts_store().all()


@router.get("/courts/{court_id}", response_model=Court)
def get_court(court_id: str) -> dict:
    court = get_courts_store().by_id(court_id)
    if court is None:
        raise HTTPException(status_code=404, detail=f"Unknown court {court_id}")
    return court


@router.get("/bookings", response_model=list[Booking])
def list_bookings(
    user_id: int | None = None,
    court_id: str | None = None,
    status: str | None = None,
) -> list[dict]:
    rows = get_bookings_store().all()
    if user_id is not None:
        rows = [b for b in rows if b.get("user_id") == user_id]
    if court_id is not None:
        rows = [b for b in rows if b.get("court_id") == court_id]
    if status is not None:
        rows = [b for b in rows if b.get("status") == status]
    return rows


@router.post("/bookings", response_model=Booking)
def create_booking(req: CreateBookingRequest) -> dict:
    courts = get_courts_store()
    bookings = get_bookings_store()

    court = courts.by_id(req.court_id)
    if court is None:
        # 422 is more accurate than 404 here — the request body is malformed,
        # not a missing resource at the request path.
        raise HTTPException(status_code=422, detail=f"Unknown court_id {req.court_id}")

    if bookings.has_conflict(req.court_id, req.date, req.time_start, req.duration):
        raise HTTPException(status_code=409, detail="Slot is not available")

    start_h = int(req.time_start.split(":")[0])
    row = bookings.add({
        "user_id": req.user_id,
        "player_name": req.player_name or "Player",
        "court_id": req.court_id,
        "court_name": court["name"],
        "date": req.date,
        "time_start": req.time_start,
        "time_end": f"{start_h + req.duration:02d}:00",
        "duration": req.duration,
        "total_price": int(court["price_per_hour"]) * req.duration,
        "status": "CONFIRMED",
    })
    return row


@router.post("/bookings/{txn_id}/cancel", response_model=Booking)
def cancel_booking(txn_id: str) -> dict:
    bookings = get_bookings_store()
    existing = bookings.by_txn(txn_id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Booking {txn_id} not found")
    if existing.get("status") == "CANCELLED":
        raise HTTPException(status_code=409, detail="Booking is already cancelled")
    cancelled = bookings.cancel(txn_id)
    return cancelled
