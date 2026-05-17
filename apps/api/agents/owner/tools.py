"""Owner-agent tools (read-only). Reads from data.store singletons."""
from datetime import date as _date
from typing import Any

from data.store import get_bookings_store, get_courts_store
from ml.inference import predict_noshow_risk
from ml.inference import get_demand_forecast as _get_demand_df

_LIST_BOOKINGS_MAX = 200


def get_revenue(date_from: str, date_to: str) -> dict:
    total = 0
    n = 0
    for b in get_bookings_store().all():
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
    rows = get_bookings_store().all()
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


def _hydrate_for_noshow(b: dict) -> dict:
    court = get_courts_store().by_id(b["court_id"]) or {}
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
            "utilization_pct": c.get("utilization_pct") or c.get("utilization"),
        }
        for c in get_courts_store().all()
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
    """Owner dispatcher. user_id accepted for parity with the player one but unused."""
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
