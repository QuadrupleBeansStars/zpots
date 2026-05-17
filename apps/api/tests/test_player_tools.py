from agents.player import tools
from data import store


def test_search_courts_filters_by_sport():
    result = tools.search_courts(sport="Badminton")
    assert len(result) >= 1
    assert all(c["sport"] == "Badminton" for c in result)


def test_get_availability_excludes_taken_slots():
    # Seed has ZP-90101 on bbc-01 at 2099-01-02 18:00-20:00 (frozen today=2099-01-01)
    free = tools.get_availability(court_id="bbc-01", date_iso="2099-01-02")
    assert "18:00" not in free
    assert "19:00" not in free
    assert "20:00" in free


def test_get_availability_ignores_other_court():
    free = tools.get_availability(court_id="sky-02", date_iso="2099-01-02")
    assert "18:00" in free


def test_list_my_bookings_filters_by_user():
    rows = tools.list_my_bookings(user_id=1)
    assert all(r.get("court_id") for r in rows)
    assert len(rows) >= 2  # ZP-90101 + ZP-90001 + ZP-90002 belong to user_id=1


def test_propose_booking_returns_draft_with_price():
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2099-07-01", time_start="18:00", duration=2,
    )
    assert draft["kind"] == "booking_draft"
    assert draft["court_name"] == "Bangkok Badminton Center"
    assert draft["total_price"] == 450 * 2
    assert draft["time_end"] == "20:00"


def test_propose_booking_rejects_taken_slot():
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2099-01-02", time_start="18:00", duration=1,
    )
    assert draft["kind"] == "error"
    assert "not available" in draft["message"].lower()


def test_propose_cancel_returns_draft_for_existing():
    draft = tools.propose_cancel(user_id=1, txn_id="ZP-90101")
    assert draft["kind"] == "cancel_draft"
    assert draft["txn_id"] == "ZP-90101"
    assert draft["court_name"] == "Bangkok Badminton Center"


def test_propose_cancel_rejects_unknown_txn():
    draft = tools.propose_cancel(user_id=1, txn_id="ZP-99999")
    assert draft["kind"] == "error"


def test_dispatch_propose_booking_no_bookings_param():
    result = tools.dispatch(
        "propose_booking",
        {"court_id": "bbc-01", "date_iso": "2099-08-01", "time_start": "10:00", "duration": 1},
        user_id=1,
    )
    assert result["kind"] == "booking_draft"
