"""In-memory data stores. Loaded on FastAPI startup; reset by tests.

Singletons are module-level so routers, agent tools, and tests share state.
Concurrency: single-process FastAPI + the GIL is enough — no locks.
"""
import random
from data import seed_loader


class CourtsStore:
    def __init__(self, seed: list[dict]) -> None:
        self._rows = list(seed)
        self._by_id = {c["id"]: c for c in seed}

    def all(self) -> list[dict]:
        return list(self._rows)

    def by_id(self, court_id: str) -> dict | None:
        return self._by_id.get(court_id)


class BookingsStore:
    def __init__(self, seed: list[dict]) -> None:
        self._rows: list[dict] = [dict(r) for r in seed]

    def reset(self, seed: list[dict]) -> None:
        self._rows = list(seed)

    def all(self) -> list[dict]:
        return list(self._rows)

    def for_user(self, user_id: int) -> list[dict]:
        return [b for b in self._rows if b.get("user_id") == user_id]

    def for_court(self, court_id: str) -> list[dict]:
        return [b for b in self._rows if b.get("court_id") == court_id]

    def by_txn(self, txn_id: str) -> dict | None:
        return next((b for b in self._rows if b.get("txn_id") == txn_id), None)

    def has_conflict(
        self, court_id: str, date_iso: str, time_start: str, duration: int,
    ) -> bool:
        start_h = int(time_start.split(":")[0])
        needed = {f"{start_h + i:02d}:00" for i in range(duration)}
        for b in self._rows:
            if b.get("court_id") != court_id or b.get("date") != date_iso:
                continue
            if b.get("status") != "CONFIRMED":
                continue
            b_start = int(b["time_start"].split(":")[0])
            taken = {f"{b_start + i:02d}:00" for i in range(int(b["duration"]))}
            if needed & taken:
                return True
        return False

    def add(self, b: dict) -> dict:
        row = dict(b)
        if not row.get("txn_id"):
            row["txn_id"] = _generate_txn_id()
        row.setdefault("status", "CONFIRMED")
        self._rows.append(row)
        return dict(row)

    def cancel(self, txn_id: str) -> dict | None:
        for b in self._rows:
            if b.get("txn_id") == txn_id:
                b["status"] = "CANCELLED"
                return dict(b)
        return None


def _generate_txn_id() -> str:
    return f"ZP-{random.randint(10000, 99999)}"


# Module-level singletons. None until init_stores() runs (on FastAPI startup).
courts_store: CourtsStore | None = None
bookings_store: BookingsStore | None = None


def init_stores() -> None:
    """Load seed files into the module-level stores. Idempotent."""
    global courts_store, bookings_store
    courts = seed_loader.load_courts()
    courts_store = CourtsStore(courts)
    bookings_store = BookingsStore(seed_loader.load_bookings(courts))


def get_courts_store() -> CourtsStore:
    """Accessor that raises if stores aren't initialized — protects against
    tests/routes that forget the startup hook."""
    if courts_store is None:
        raise RuntimeError("CourtsStore not initialized — call init_stores() first")
    return courts_store


def get_bookings_store() -> BookingsStore:
    if bookings_store is None:
        raise RuntimeError("BookingsStore not initialized — call init_stores() first")
    return bookings_store
