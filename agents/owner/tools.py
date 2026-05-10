"""Owner-agent tools (read-only v1).

Tools query the SQLite bookings table and the static COURTS list. No write
tools in v1 — pricing and slot-block changes still require the dedicated
Streamlit pages.
"""
from data import database as db
from data.dummy_data import COURTS


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
    sql = "SELECT * FROM bookings WHERE 1=1"
    args: list = []
    if date_from:
        sql += " AND date >= ?"; args.append(date_from)
    if date_to:
        sql += " AND date <= ?"; args.append(date_to)
    if court_id:
        sql += " AND court_id = ?"; args.append(court_id)
    if status:
        sql += " AND status = ?"; args.append(status)
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
