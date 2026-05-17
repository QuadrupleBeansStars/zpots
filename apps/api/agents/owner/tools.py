"""Owner-agent tools (read-only).

In Phase 3c there is no Postgres yet, so the tools read from a hardcoded
`_BOOKINGS_FIXTURE` representing the venue's recent activity. Phase 4 swaps
this for a real query.
"""
from datetime import date as _date, timedelta as _td
from typing import Any

from ml.inference import predict_noshow_risk
from ml.inference import get_demand_forecast as _get_demand_df

_LIST_BOOKINGS_MAX = 200


# Mirror of the legacy SQLite seed data plus some upcoming bookings so the
# owner agent has interesting things to rank/summarize. Phase 4 swaps for
# a Postgres query.
def _upcoming(days_ahead: int, **overrides) -> dict:
    d = (_date.today() + _td(days=days_ahead)).isoformat()
    base = {
        "txn_id": "ZP-00000", "player_name": "Demo",
        "court_id": "bbc-01", "court_name": "Bangkok Badminton Center",
        "date": d, "time_start": "18:00", "time_end": "19:00",
        "duration": 1, "total_price": 450, "status": "CONFIRMED",
    }
    base.update(overrides)
    return base


_BOOKINGS_FIXTURE: list[dict] = [
    _upcoming(1, txn_id="ZP-90101", player_name="Alex Siriwan",
              court_id="bbc-01", court_name="Bangkok Badminton Center",
              time_start="18:00", time_end="20:00", duration=2, total_price=900),
    _upcoming(2, txn_id="ZP-90102", player_name="Narin Kositchai",
              court_id="sky-02", court_name="Skyline Arena Football",
              time_start="20:00", time_end="22:00", duration=2, total_price=2400),
    _upcoming(3, txn_id="ZP-90103", player_name="Maya Chen",
              court_id="pdl-04", court_name="Padel House Sukhumvit",
              time_start="07:00", time_end="08:00", duration=1, total_price=800),
    _upcoming(4, txn_id="ZP-90104", player_name="Tomás Vega",
              court_id="dwh-03", court_name="Downtown Hoops",
              time_start="19:00", time_end="21:00", duration=2, total_price=1200),
    _upcoming(5, txn_id="ZP-90105", player_name="Priya Singh",
              court_id="rbs-05", court_name="Royal Bangkok Sports Club",
              time_start="16:00", time_end="17:00", duration=1, total_price=950),
    _upcoming(0, txn_id="ZP-90100", player_name="Marcus Lee",
              court_id="bbc-01", court_name="Bangkok Badminton Center",
              time_start="20:00", time_end="21:00", duration=1, total_price=450),
]


COURTS: list[dict] = [
    {"id": "bbc-01", "name": "Bangkok Badminton Center", "sport": "Badminton",
     "district": "Sukhumvit", "price_per_hour": 450, "utilization": 88},
    {"id": "sky-02", "name": "Skyline Arena Football", "sport": "Football",
     "district": "Thong Lor", "price_per_hour": 1200, "utilization": 74},
    {"id": "dwh-03", "name": "Downtown Hoops", "sport": "Basketball",
     "district": "Ari", "price_per_hour": 600, "utilization": 68},
    {"id": "pdl-04", "name": "Padel House Sukhumvit", "sport": "Padel",
     "district": "Sukhumvit", "price_per_hour": 800, "utilization": 79},
    {"id": "rbs-05", "name": "Royal Bangkok Sports Club", "sport": "Tennis",
     "district": "Pathumwan", "price_per_hour": 950, "utilization": 92},
    {"id": "ivh-06", "name": "Impact Volleyball Hall", "sport": "Volleyball",
     "district": "Nonthaburi", "price_per_hour": 350, "utilization": 55},
]


def get_revenue(date_from: str, date_to: str) -> dict:
    total = 0
    n = 0
    for b in _BOOKINGS_FIXTURE:
        if b["status"] != "CONFIRMED":
            continue
        if date_from <= b["date"] <= date_to:
            total += b["total_price"]
            n += 1
    return {"total_thb": total, "bookings": n,
            "date_from": date_from, "date_to": date_to}


def list_bookings(
    date_from: str | None = None,
    date_to: str | None = None,
    court_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
) -> list[dict]:
    limit = max(1, min(int(limit), _LIST_BOOKINGS_MAX))
    rows = list(_BOOKINGS_FIXTURE)
    if date_from:
        rows = [r for r in rows if r["date"] >= date_from]
    if date_to:
        rows = [r for r in rows if r["date"] <= date_to]
    if court_id:
        rows = [r for r in rows if r["court_id"] == court_id]
    if status:
        rows = [r for r in rows if r["status"] == status]
    rows.sort(key=lambda r: (r["date"], r["time_start"]), reverse=True)
    return rows[:limit]


def _court_lookup(court_id: str) -> dict:
    return next((c for c in COURTS if c["id"] == court_id), {})


def _hydrate_for_noshow(b: dict) -> dict:
    court = _court_lookup(b["court_id"])
    d = _date.fromisoformat(b["date"])
    dow = d.weekday()
    hour = int(b["time_start"].split(":")[0])
    return {
        "court_id": b["court_id"],
        "sport": court.get("sport", "Badminton"),
        "district": court.get("district", "Sukhumvit"),
        "day_of_week": dow,
        "hour": hour,
        "is_weekend": dow >= 5,
        "is_holiday": False,
        "weather": "sunny",
        "price": int(b["total_price"]) // max(1, int(b["duration"])),
        "lead_time_days": max(0, (d - _date.today()).days),
        "is_repeat_customer": True,
    }


def rank_noshow_risk(
    date_from: str | None = None, date_to: str | None = None, limit: int = 10,
) -> list[dict]:
    bookings = list_bookings(date_from=date_from, date_to=date_to,
                             status="CONFIRMED", limit=_LIST_BOOKINGS_MAX)
    scored = []
    for b in bookings:
        feats = _hydrate_for_noshow(b)
        tier, p = predict_noshow_risk(feats)
        scored.append({
            "txn_id": b["txn_id"],
            "player_name": b["player_name"],
            "court_id": b["court_id"],
            "court_name": b["court_name"],
            "date": b["date"],
            "time_start": b["time_start"],
            "risk_tier": tier,
            "risk_probability": round(p, 3),
        })
    scored.sort(key=lambda r: r["risk_probability"], reverse=True)
    return scored[:limit]


def get_demand_forecast(top_n: int = 10) -> list[dict]:
    df = _get_demand_df()
    if df.empty:
        return []
    top = df.sort_values("predicted_bookings", ascending=False).head(top_n)
    return [
        {
            "court_id": r["court_id"],
            "day_of_week": int(r["day_of_week"]),
            "hour": int(r["hour"]),
            "predicted_bookings": round(float(r["predicted_bookings"]), 2),
        }
        for _, r in top.iterrows()
    ]


def summarize_courts() -> list[dict]:
    return [
        {
            "id": c["id"], "name": c["name"], "sport": c["sport"],
            "district": c["district"], "price_per_hour": c["price_per_hour"],
            "utilization_pct": c.get("utilization"),
        }
        for c in COURTS
    ]


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_revenue",
            "description": "Sum confirmed-booking revenue (THB) over a date range. Returns {total_thb, bookings, date_from, date_to}.",
            "parameters": {
                "type": "object",
                "required": ["date_from", "date_to"],
                "properties": {
                    "date_from": {"type": "string"}, "date_to": {"type": "string"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_bookings",
            "description": "List bookings filtered by date range, court, or status. Returns up to `limit` rows, newest first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_from": {"type": "string"}, "date_to": {"type": "string"},
                    "court_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["CONFIRMED", "CANCELLED"]},
                    "limit": {"type": "integer"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rank_noshow_risk",
            "description": "Return upcoming CONFIRMED bookings ranked by predicted no-show probability (highest first).",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_from": {"type": "string"}, "date_to": {"type": "string"},
                    "limit": {"type": "integer"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_demand_forecast",
            "description": "Top predicted-busiest (court, day_of_week, hour) cells. day_of_week: 0=Mon..6=Sun.",
            "parameters": {
                "type": "object",
                "properties": {"top_n": {"type": "integer"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_courts",
            "description": "List all courts with id, name, sport, district, price_per_hour, utilization_pct.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def dispatch(name: str, args: dict, user_id: int) -> Any:
    """Owner dispatcher. user_id is accepted for parity with the player one but unused."""
    if name == "get_revenue":
        return get_revenue(**args)
    if name == "list_bookings":
        return list_bookings(**args)
    if name == "rank_noshow_risk":
        return rank_noshow_risk(**args)
    if name == "get_demand_forecast":
        return get_demand_forecast(**args)
    if name == "summarize_courts":
        return summarize_courts()
    return {"kind": "error", "message": f"Unknown tool {name}"}
