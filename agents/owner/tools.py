"""Owner-agent tools (read-only v1).

Tools query the SQLite bookings table and the static COURTS list. No write
tools in v1 — pricing and slot-block changes still require the dedicated
Streamlit pages.
"""
from datetime import date as _date

from data import database as db
from data.dummy_data import COURTS
from utils.ml_inference import predict_noshow_risk
from utils.ml_inference import get_demand_forecast as get_demand_forecast_df

_LIST_BOOKINGS_MAX = 200


def get_revenue(date_from: str, date_to: str) -> dict:
    """Sum total_price across CONFIRMED bookings whose date is within [date_from, date_to]."""
    conn = db.get_connection()
    row = conn.execute(
        "SELECT COALESCE(SUM(total_price), 0) AS total, COUNT(*) AS n "
        "FROM bookings WHERE status='CONFIRMED' AND date BETWEEN ? AND ?",
        (date_from, date_to),
    ).fetchone()
    return {"total_thb": int(row["total"]), "bookings": int(row["n"]),
            "date_from": date_from, "date_to": date_to}


def list_bookings(
    date_from: str | None = None,
    date_to: str | None = None,
    court_id: str | None = None,
    status: str | None = None,
    limit: int = 50,
) -> list[dict]:
    """Return bookings matching the supplied filters, newest first, capped by limit."""
    limit = max(1, min(int(limit), _LIST_BOOKINGS_MAX))
    sql = "SELECT * FROM bookings WHERE 1=1"
    args: list = []
    if date_from:
        sql += " AND date >= ?"
        args.append(date_from)
    if date_to:
        sql += " AND date <= ?"
        args.append(date_to)
    if court_id:
        sql += " AND court_id = ?"
        args.append(court_id)
    if status:
        sql += " AND status = ?"
        args.append(status)
    sql += " ORDER BY date DESC, time_start DESC LIMIT ?"
    args.append(limit)
    rows = db.get_connection().execute(sql, args).fetchall()
    return [
        {
            "id": r["id"], "txn_id": r["txn_id"], "player_name": r["player_name"],
            "court_id": r["court_id"], "court_name": r["court_name"],
            "date": r["date"], "time_start": r["time_start"], "time_end": r["time_end"],
            "duration": r["duration"], "total_price": r["total_price"], "status": r["status"],
        }
        for r in rows
    ]


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
    """Rank upcoming CONFIRMED bookings by predicted no-show probability (high → low)."""
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
    """Return the top_n predicted-busiest (court_id, day_of_week, hour) rows."""
    df = get_demand_forecast_df()
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
    """Return one row per court: id, name, sport, district, price_per_hour, utilization."""
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
                    "date_from": {"type": "string", "description": "YYYY-MM-DD inclusive"},
                    "date_to":   {"type": "string", "description": "YYYY-MM-DD inclusive"},
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
                    "date_from": {"type": "string"},
                    "date_to":   {"type": "string"},
                    "court_id":  {"type": "string"},
                    "status":    {"type": "string", "enum": ["CONFIRMED", "CANCELLED"]},
                    "limit":     {"type": "integer", "description": "Default 50, max 200"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "rank_noshow_risk",
            "description": "Return upcoming CONFIRMED bookings ranked by predicted no-show probability (highest first). Each row has txn_id, player_name, court, date, time_start, risk_tier, risk_probability.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_from": {"type": "string"},
                    "date_to":   {"type": "string"},
                    "limit":     {"type": "integer"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_demand_forecast",
            "description": "Top predicted-busiest (court, day_of_week, hour) cells from the trained demand-forecast model. day_of_week: 0=Mon..6=Sun.",
            "parameters": {
                "type": "object",
                "properties": {"top_n": {"type": "integer", "description": "Default 10"}},
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


def dispatch(name: str, args: dict, user_id: int) -> dict | list:
    """Run an owner tool by name. user_id is accepted for parity with the player dispatcher but unused in v1."""
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
