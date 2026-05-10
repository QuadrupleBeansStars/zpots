import os
import tempfile
import pytest
from data import database as db
from agents.owner import tools


@pytest.fixture(autouse=True)
def fresh_db(monkeypatch):
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    monkeypatch.setattr(db, "DB_PATH", tmp.name)
    db.get_connection.clear()
    db.init_db()
    yield
    os.unlink(tmp.name)


def test_get_revenue_sums_confirmed_bookings_in_range():
    db.create_booking(player_id=1, player_name="A", court_id="bbc-01", court_name="BBC",
                      date_iso="2026-06-01", time_start="18:00", time_end="19:00",
                      duration=1, total_price=500)
    db.create_booking(player_id=1, player_name="A", court_id="bbc-01", court_name="BBC",
                      date_iso="2026-06-02", time_start="18:00", time_end="19:00",
                      duration=1, total_price=700)
    db.create_booking(player_id=1, player_name="A", court_id="bbc-01", court_name="BBC",
                      date_iso="2026-07-01", time_start="18:00", time_end="19:00",
                      duration=1, total_price=999)

    result = tools.get_revenue(date_from="2026-06-01", date_to="2026-06-30")
    assert result["total_thb"] == 1200
    assert result["bookings"] == 2


def test_get_revenue_excludes_cancelled():
    txn = db.create_booking(player_id=1, player_name="A", court_id="bbc-01", court_name="BBC",
                            date_iso="2026-06-01", time_start="18:00", time_end="19:00",
                            duration=1, total_price=500)
    bid = next(b for b in db.get_bookings_by_user(1) if b["txn_id"] == txn)["id"]
    db.cancel_booking(bid, player_id=1)

    result = tools.get_revenue(date_from="2026-06-01", date_to="2026-06-30")
    assert result["total_thb"] == 0
    assert result["bookings"] == 0


def test_list_bookings_filters_by_court():
    db.create_booking(player_id=1, player_name="A", court_id="tst-01", court_name="Test Court",
                      date_iso="2026-06-01", time_start="18:00", time_end="19:00",
                      duration=1, total_price=500)
    db.create_booking(player_id=1, player_name="A", court_id="sky-02", court_name="Sky",
                      date_iso="2026-06-01", time_start="18:00", time_end="19:00",
                      duration=1, total_price=1200)

    rows = tools.list_bookings(court_id="tst-01")
    assert len(rows) == 1
    assert rows[0]["court_id"] == "tst-01"


def test_list_bookings_filters_by_date_range():
    db.create_booking(player_id=1, player_name="A", court_id="bbc-01", court_name="BBC",
                      date_iso="2026-06-15", time_start="18:00", time_end="19:00",
                      duration=1, total_price=500)
    db.create_booking(player_id=1, player_name="A", court_id="bbc-01", court_name="BBC",
                      date_iso="2026-07-15", time_start="18:00", time_end="19:00",
                      duration=1, total_price=500)

    rows = tools.list_bookings(date_from="2026-06-01", date_to="2026-06-30")
    assert len(rows) == 1
    assert rows[0]["date"] == "2026-06-15"


def test_rank_noshow_risk_returns_sorted_upcoming_bookings(monkeypatch):
    # Stub the ML predictor so the test does not depend on artifacts on disk.
    fake = {"bbc-01": ("High", 0.82), "sky-02": ("Low", 0.11)}
    def fake_predict(booking):
        return fake.get(booking["court_id"], ("Medium", 0.5))
    monkeypatch.setattr("agents.owner.tools.predict_noshow_risk", fake_predict)

    db.create_booking(player_id=1, player_name="Alex", court_id="bbc-01", court_name="BBC",
                      date_iso="2099-06-01", time_start="18:00", time_end="19:00",
                      duration=1, total_price=500)
    db.create_booking(player_id=1, player_name="Narin", court_id="sky-02", court_name="Sky",
                      date_iso="2099-06-01", time_start="20:00", time_end="22:00",
                      duration=2, total_price=2400)

    ranked = tools.rank_noshow_risk(date_from="2099-06-01", date_to="2099-06-30", limit=10)
    assert len(ranked) == 2
    assert ranked[0]["court_id"] == "bbc-01"
    assert ranked[0]["risk_tier"] == "High"
    assert 0.0 <= ranked[0]["risk_probability"] <= 1.0
    assert ranked[1]["court_id"] == "sky-02"
