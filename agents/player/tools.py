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
