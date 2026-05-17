"""Player-agent tools. Each tool is a plain Python function the agent loop dispatches.

Tools take an explicit `bookings` snapshot (passed in from the request body)
instead of reading from a database. The frontend's useBookingStore is the
single source of truth for the player's bookings in Phase 3c.
"""
from typing import Any

_HOURS = [f"{h:02d}:00" for h in range(7, 23)]  # 07:00..22:00


# Mirror of apps/web/lib/mock-data.ts:COURTS. Phase 4 swaps for a Postgres query.
COURTS: list[dict] = [
    {
        "id": "bbc-01", "name": "Bangkok Badminton Center",
        "sport": "Badminton", "district": "Sukhumvit",
        "price_per_hour": 450, "rating": 4.8,
    },
    {
        "id": "sky-02", "name": "Skyline Arena Football",
        "sport": "Football", "district": "Thong Lor",
        "price_per_hour": 1200, "rating": 4.7,
    },
    {
        "id": "dwh-03", "name": "Downtown Hoops",
        "sport": "Basketball", "district": "Ari",
        "price_per_hour": 600, "rating": 4.5,
    },
    {
        "id": "pdl-04", "name": "Padel House Sukhumvit",
        "sport": "Padel", "district": "Sukhumvit",
        "price_per_hour": 800, "rating": 4.2,
    },
    {
        "id": "rbs-05", "name": "Royal Bangkok Sports Club",
        "sport": "Tennis", "district": "Pathumwan",
        "price_per_hour": 950, "rating": 5.0,
    },
    {
        "id": "ivh-06", "name": "Impact Volleyball Hall",
        "sport": "Volleyball", "district": "Nonthaburi",
        "price_per_hour": 350, "rating": 4.8,
    },
]


def _find_court(court_id: str) -> dict | None:
    return next((c for c in COURTS if c["id"] == court_id), None)


def _booked_starts(court_id: str, date_iso: str, bookings: list[dict]) -> set[str]:
    """Compute taken HH:00 starts for a court on a date from CONFIRMED bookings."""
    taken: set[str] = set()
    for b in bookings:
        if b.get("court_id") != court_id or b.get("date") != date_iso:
            continue
        if b.get("status") != "CONFIRMED":
            continue
        start_h = int(b["time_start"].split(":")[0])
        for i in range(int(b.get("duration", 1))):
            taken.add(f"{start_h + i:02d}:00")
    return taken


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
            "id": c["id"], "name": c["name"], "sport": c["sport"],
            "district": c["district"], "price_per_hour": c["price_per_hour"],
            "rating": c.get("rating"),
        })
    return out


def get_availability(court_id: str, date_iso: str, bookings: list[dict]) -> list[str]:
    """Return the list of free hour-start times (HH:00) for a court on a given date."""
    booked = _booked_starts(court_id, date_iso, bookings)
    return [h for h in _HOURS if h not in booked]


def list_my_bookings(user_id: int, bookings: list[dict]) -> list[dict]:
    """Return the player's bookings (the snapshot from the frontend)."""
    return [
        {
            "txn_id": b["txn_id"], "court_id": b["court_id"], "court_name": b["court_name"],
            "date": b["date"], "time_start": b["time_start"], "time_end": b["time_end"],
            "total_price": b["total_price"], "status": b["status"],
        }
        for b in bookings
    ]


def propose_booking(
    user_id: int, court_id: str, date_iso: str, time_start: str, duration: int,
    bookings: list[dict],
) -> dict:
    court = _find_court(court_id)
    if court is None:
        return {"kind": "error", "message": f"Unknown court id {court_id}"}

    start_h = int(time_start.split(":")[0])
    needed = {f"{start_h + i:02d}:00" for i in range(duration)}
    booked = _booked_starts(court_id, date_iso, bookings)
    if needed & booked:
        return {"kind": "error", "message": f"Slot is not available on {date_iso} at {time_start}."}

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


def propose_cancel(user_id: int, txn_id: str, bookings: list[dict]) -> dict:
    booking = next((b for b in bookings if b.get("txn_id") == txn_id), None)
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


def dispatch(name: str, args: dict, user_id: int, bookings: list[dict]) -> Any:
    """Run a tool by name. Threads user_id + bookings into tools that need them."""
    if name == "search_courts":
        return search_courts(**args)
    if name == "get_availability":
        return get_availability(bookings=bookings, **args)
    if name == "list_my_bookings":
        return list_my_bookings(user_id=user_id, bookings=bookings)
    if name == "propose_booking":
        return propose_booking(user_id=user_id, bookings=bookings, **args)
    if name == "propose_cancel":
        return propose_cancel(user_id=user_id, bookings=bookings, **args)
    return {"kind": "error", "message": f"Unknown tool {name}"}
