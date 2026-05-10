"""Player-agent tools. Each tool is a plain Python function the agent loop dispatches.

Read tools execute freely. Write tools are two-phase: agent calls `propose_*` which
returns a draft dict; the chat widget renders Confirm/Cancel buttons and only the
widget calls the actual `data.database.create_booking` / `cancel_booking`.
"""
from data import database as db
from data.dummy_data import COURTS

_HOURS = [f"{h:02d}:00" for h in range(7, 23)]  # 07:00..22:00


def search_courts(
    sport: str | None = None,
    district: str | None = None,
    max_price: int | None = None,
) -> list[dict]:
    out = []
    for c in COURTS:
        if sport and c["sport"].lower() != sport.lower():
            continue
        if district and district.lower() not in c["district"].lower():
            continue
        if max_price is not None and c["price_per_hour"] > max_price:
            continue
        out.append({
            "id": c["id"],
            "name": c["name"],
            "sport": c["sport"],
            "district": c["district"],
            "price_per_hour": c["price_per_hour"],
            "rating": c.get("rating"),
        })
    return out


def get_availability(court_id: str, date_iso: str) -> list[str]:
    """Return the list of free hour-start times (HH:00) for a court on a given date."""
    booked = db.get_booked_slots(court_id, date_iso)
    return [h for h in _HOURS if h not in booked]


def list_my_bookings(user_id: int) -> list[dict]:
    rows = db.get_bookings_by_user(user_id)
    return [
        {
            "id": r["id"],
            "txn_id": r["txn_id"],
            "court_id": r["court_id"],
            "court_name": r["court_name"],
            "date": r["date"],
            "time_start": r["time_start"],
            "time_end": r["time_end"],
            "total_price": r["total_price"],
            "status": r["status"],
        }
        for r in rows
    ]


def _find_court(court_id: str) -> dict | None:
    return next((c for c in COURTS if c["id"] == court_id), None)


def propose_booking(
    user_id: int, court_id: str, date_iso: str, time_start: str, duration: int,
) -> dict:
    court = _find_court(court_id)
    if court is None:
        return {"kind": "error", "message": f"Unknown court id {court_id}"}

    start_h = int(time_start.split(":")[0])
    needed = {f"{start_h + i:02d}:00" for i in range(duration)}
    booked = db.get_booked_slots(court_id, date_iso)
    if needed & booked:
        return {"kind": "error", "message": f"Slot is not available on {date_iso} at {time_start}."}

    time_end = f"{start_h + duration:02d}:00"
    total = court["price_per_hour"] * duration
    return {
        "kind": "booking_draft",
        "user_id": user_id,
        "court_id": court_id,
        "court_name": court["name"],
        "date": date_iso,
        "time_start": time_start,
        "time_end": time_end,
        "duration": duration,
        "total_price": total,
    }


def propose_cancel(user_id: int, booking_id: int) -> dict:
    rows = db.get_bookings_by_user(user_id)
    booking = next((b for b in rows if b["id"] == booking_id), None)
    if booking is None:
        return {"kind": "error", "message": "Booking not found or not yours."}
    if booking["status"] == "CANCELLED":
        return {"kind": "error", "message": "Booking is already cancelled."}
    return {
        "kind": "cancel_draft",
        "user_id": user_id,
        "booking_id": booking_id,
        "txn_id": booking["txn_id"],
        "court_name": booking["court_name"],
        "date": booking["date"],
        "time_start": booking["time_start"],
    }
