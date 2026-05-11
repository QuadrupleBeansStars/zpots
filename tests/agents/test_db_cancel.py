import os
import tempfile
import pytest
from data import database as db


@pytest.fixture(autouse=True)
def fresh_db(monkeypatch):
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    monkeypatch.setattr(db, "DB_PATH", tmp.name)
    db.get_connection.clear()  # bust streamlit cache_resource
    db.init_db()
    yield
    os.unlink(tmp.name)


def test_cancel_booking_marks_status_cancelled():
    txn = db.create_booking(
        player_id=1, player_name="Alex Siriwan",
        court_id="bbc-01", court_name="Bangkok Badminton Center",
        date_iso="2026-06-01", time_start="18:00", time_end="19:00",
        duration=1, total_price=450,
    )
    booking = next(b for b in db.get_bookings_by_user(1) if b["txn_id"] == txn)

    ok = db.cancel_booking(booking["id"], player_id=1)

    assert ok is True
    after = next(b for b in db.get_bookings_by_user(1) if b["txn_id"] == txn)
    assert after["status"] == "CANCELLED"


def test_cancel_booking_rejects_other_users_booking():
    txn = db.create_booking(
        player_id=1, player_name="Alex",
        court_id="bbc-01", court_name="BBC",
        date_iso="2026-06-01", time_start="18:00", time_end="19:00",
        duration=1, total_price=450,
    )
    bid = next(b for b in db.get_bookings_by_user(1) if b["txn_id"] == txn)["id"]

    ok = db.cancel_booking(bid, player_id=2)
    assert ok is False
