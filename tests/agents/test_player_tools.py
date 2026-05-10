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
