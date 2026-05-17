"""Player-agent tools. Reads from data.store; no bookings param required."""
from typing import Any

from data.store import get_bookings_store, get_courts_store

_HOURS = [f"{h:02d}:00" for h in range(7, 23)]  # 07:00..22:00


def search_courts(
    sport: str | None = None,
    district: str | None = None,
    max_price: int | None = None,
) -> list[dict]:
    out = []
    for c in get_courts_store().all():
        if sport and c["sport"].lower() != sport.lower():
            continue
        if district and district.lower() not in c["district"].lower():
            continue
        if max_price is not None and c["price_per_hour"] > max_price:
            continue
        out.append({
            "id": c["id"], "name": c["name"], "sport": c["sport"],
            "district": c["district"], "price_per_hour": c["price_per_hour"],
            "rating": c.get("rating"),
        })
    return out


def get_availability(court_id: str, date_iso: str) -> list[str]:
    """Return free hour-start times (HH:00) for a court on a given date."""
    bs = get_bookings_store()
    free: list[str] = []
    for h in _HOURS:
        if not bs.has_conflict(court_id, date_iso, h, 1):
            free.append(h)
    return free


def list_my_bookings(user_id: int) -> list[dict]:
    return [
        {
            "txn_id": b["txn_id"], "court_id": b["court_id"], "court_name": b["court_name"],
            "date": b["date"], "time_start": b["time_start"], "time_end": b["time_end"],
            "total_price": b["total_price"], "status": b["status"],
        }
        for b in get_bookings_store().for_user(user_id)
    ]


def propose_booking(
    user_id: int, court_id: str, date_iso: str, time_start: str, duration: int,
) -> dict:
    court = get_courts_store().by_id(court_id)
    if court is None:
        return {"kind": "error", "message": f"Unknown court id {court_id}"}

    if get_bookings_store().has_conflict(court_id, date_iso, time_start, duration):
        return {"kind": "error", "message": f"Slot is not available on {date_iso} at {time_start}."}

    start_h = int(time_start.split(":")[0])
    time_end = f"{start_h + duration:02d}:00"
    total = court["price_per_hour"] * duration
    return {
        "kind": "booking_draft",
        "court_id": court_id,
        "court_name": court["name"],
        "date": date_iso,
        "time_start": time_start,
        "time_end": time_end,
        "duration": duration,
        "total_price": total,
    }


def propose_cancel(user_id: int, txn_id: str) -> dict:
    booking = get_bookings_store().by_txn(txn_id)
    if booking is None:
        return {"kind": "error", "message": f"Booking {txn_id} not found."}
    if booking.get("status") == "CANCELLED":
        return {"kind": "error", "message": "Booking is already cancelled."}
    return {
        "kind": "cancel_draft",
        "txn_id": booking["txn_id"],
        "court_name": booking["court_name"],
        "date": booking["date"],
        "time_start": booking["time_start"],
    }


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_courts",
            "description": "Find courts matching sport/district/max_price filters. Returns id, name, sport, district, price_per_hour, rating.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sport": {"type": "string", "description": "e.g. Badminton, Football, Padel"},
                    "district": {"type": "string"},
                    "max_price": {"type": "integer", "description": "Max THB per hour"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_availability",
            "description": "List free hour-start times (HH:00) for a court on a given date.",
            "parameters": {
                "type": "object",
                "required": ["court_id", "date_iso"],
                "properties": {
                    "court_id": {"type": "string"},
                    "date_iso": {"type": "string", "description": "YYYY-MM-DD"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_my_bookings",
            "description": "Return all bookings belonging to the current user.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "propose_booking",
            "description": "Draft a booking for confirmation. Does NOT write. The user will see Confirm/Cancel buttons. Always call this before booking.",
            "parameters": {
                "type": "object",
                "required": ["court_id", "date_iso", "time_start", "duration"],
                "properties": {
                    "court_id": {"type": "string"},
                    "date_iso": {"type": "string", "description": "YYYY-MM-DD"},
                    "time_start": {"type": "string", "description": "HH:00 24-hour"},
                    "duration": {"type": "integer", "description": "Hours, 1-4"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "propose_cancel",
            "description": "Draft a cancellation for confirmation. Does NOT write. Takes the txn_id (string, like 'ZP-12345') from list_my_bookings.",
            "parameters": {
                "type": "object",
                "required": ["txn_id"],
                "properties": {"txn_id": {"type": "string"}},
            },
        },
    },
]


def dispatch(name: str, args: dict, user_id: int) -> Any:
    """Run a tool by name. Threads only user_id; bookings come from the store."""
    if name == "search_courts":
        return search_courts(**args)
    if name == "get_availability":
        return get_availability(**args)
    if name == "list_my_bookings":
        return list_my_bookings(user_id=user_id)
    if name == "propose_booking":
        return propose_booking(user_id=user_id, **args)
    if name == "propose_cancel":
        return propose_cancel(user_id=user_id, **args)
    return {"kind": "error", "message": f"Unknown tool {name}"}
