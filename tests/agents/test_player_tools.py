import os
import tempfile
import pytest
from data import database as db
from agents.player import tools


@pytest.fixture(autouse=True)
def fresh_db(monkeypatch):
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    monkeypatch.setattr(db, "DB_PATH", tmp.name)
    db.get_connection.clear()
    db.init_db()
    yield
    os.unlink(tmp.name)


def test_search_courts_filters_by_sport():
    result = tools.search_courts(sport="Badminton")
    assert len(result) >= 1
    assert all(c["sport"] == "Badminton" for c in result)
    assert set(result[0].keys()) >= {"id", "name", "sport", "district", "price_per_hour"}


def test_search_courts_filters_by_max_price():
    result = tools.search_courts(max_price=500)
    assert all(c["price_per_hour"] <= 500 for c in result)


def test_get_availability_returns_free_hours():
    db.create_booking(
        player_id=1, player_name="Alex", court_id="bbc-01",
        court_name="BBC", date_iso="2026-06-01",
        time_start="18:00", time_end="19:00", duration=1, total_price=450,
    )
    free = tools.get_availability(court_id="bbc-01", date_iso="2026-06-01")
    assert "18:00" not in free
    assert "19:00" in free or "20:00" in free


def test_list_my_bookings_scoped_to_user():
    # player_id=3 (owner) has no seeded bookings; player_id=2 has seeded bookings.
    # This ensures list_my_bookings returns only the one booking we create for user 3.
    db.create_booking(
        player_id=3, player_name="Owner", court_id="bbc-01", court_name="BBC",
        date_iso="2026-06-01", time_start="18:00", time_end="19:00",
        duration=1, total_price=450,
    )
    db.create_booking(
        player_id=2, player_name="Narin", court_id="sky-02", court_name="Sky",
        date_iso="2026-06-02", time_start="20:00", time_end="22:00",
        duration=2, total_price=2400,
    )
    rows = tools.list_my_bookings(user_id=3)
    assert len(rows) == 1
    assert rows[0]["court_id"] == "bbc-01"


def test_propose_booking_returns_draft_with_price():
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2026-06-01", time_start="18:00", duration=2,
    )
    assert draft["kind"] == "booking_draft"
    assert draft["court_name"] == "Bangkok Badminton Center"
    assert draft["total_price"] == 450 * 2
    assert draft["time_end"] == "20:00"


def test_propose_booking_rejects_taken_slot():
    db.create_booking(
        player_id=2, player_name="Narin", court_id="bbc-01", court_name="BBC",
        date_iso="2026-06-01", time_start="18:00", time_end="19:00",
        duration=1, total_price=450,
    )
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2026-06-01", time_start="18:00", duration=1,
    )
    assert draft["kind"] == "error"
    assert "not available" in draft["message"].lower()


def test_propose_cancel_returns_draft_for_own_booking():
    txn = db.create_booking(
        player_id=1, player_name="Alex", court_id="bbc-01", court_name="BBC",
        date_iso="2026-06-01", time_start="18:00", time_end="19:00",
        duration=1, total_price=450,
    )
    bid = next(b for b in db.get_bookings_by_user(1) if b["txn_id"] == txn)["id"]
    draft = tools.propose_cancel(user_id=1, booking_id=bid)
    assert draft["kind"] == "cancel_draft"
    assert draft["booking_id"] == bid


def test_propose_cancel_rejects_other_users():
    txn = db.create_booking(
        player_id=2, player_name="Narin", court_id="bbc-01", court_name="BBC",
        date_iso="2026-06-01", time_start="18:00", time_end="19:00",
        duration=1, total_price=450,
    )
    bid = next(b for b in db.get_bookings_by_user(2) if b["txn_id"] == txn)["id"]
    draft = tools.propose_cancel(user_id=1, booking_id=bid)
    assert draft["kind"] == "error"
