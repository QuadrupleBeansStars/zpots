"""Pure functions that load JSON seed files and resolve derived fields.

`_today()` is an indirection so tests can freeze the date with monkeypatch.
"""
import json
from datetime import date, timedelta
from pathlib import Path

_SEED_DIR = Path(__file__).resolve().parent.parent / "seed"


def _today() -> date:
    return date.today()


def load_courts() -> list[dict]:
    """Read seed/courts.json. Returns the rows verbatim (no transformation)."""
    return json.loads((_SEED_DIR / "courts.json").read_text())


def load_bookings(courts: list[dict]) -> list[dict]:
    """Read seed/bookings.json and resolve derived fields.

    Adds: date (today + days_from_today), time_end (time_start + duration),
    court_name and total_price (looked up from `courts`).

    Raises KeyError if a booking references a court_id not in `courts`.
    """
    by_id = {c["id"]: c for c in courts}
    raw = json.loads((_SEED_DIR / "bookings.json").read_text())
    today = _today()
    out: list[dict] = []
    for b in raw:
        court_id = b["court_id"]
        if court_id not in by_id:
            raise KeyError(f"seed/bookings.json references unknown court_id={court_id}")
        court = by_id[court_id]
        d = today + timedelta(days=int(b["days_from_today"]))
        start_h = int(b["time_start"].split(":")[0])
        duration = int(b["duration"])
        out.append({
            "txn_id": b["txn_id"],
            "user_id": int(b["user_id"]),
            "player_name": b["player_name"],
            "court_id": court_id,
            "court_name": court["name"],
            "date": d.isoformat(),
            "time_start": b["time_start"],
            "time_end": f"{start_h + duration:02d}:00",
            "duration": duration,
            "total_price": int(court["price_per_hour"]) * duration,
            "status": b["status"],
        })
    return out
