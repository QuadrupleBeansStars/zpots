import pytest

from agents.player import tools


SAMPLE_BOOKINGS = [
    {
        "txn_id": "ZP-90001", "court_id": "bbc-01", "court_name": "Bangkok Badminton Center",
        "date": "2099-06-01", "time_start": "18:00", "time_end": "20:00",
        "duration": 2, "total_price": 900, "status": "CONFIRMED",
    },
]


def test_search_courts_filters_by_sport():
    result = tools.search_courts(sport="Badminton")
    assert len(result) >= 1
    assert all(c["sport"] == "Badminton" for c in result)


def test_get_availability_excludes_taken_slots():
    free = tools.get_availability(
        court_id="bbc-01", date_iso="2099-06-01", bookings=SAMPLE_BOOKINGS,
    )
    assert "18:00" not in free
    assert "19:00" not in free
    assert "20:00" in free


def test_get_availability_ignores_other_court():
    free = tools.get_availability(
        court_id="sky-02", date_iso="2099-06-01", bookings=SAMPLE_BOOKINGS,
    )
    assert "18:00" in free


def test_propose_booking_returns_draft_with_price():
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2099-07-01", time_start="18:00", duration=2,
        bookings=[],
    )
    assert draft["kind"] == "booking_draft"
    assert draft["court_name"] == "Bangkok Badminton Center"
    assert draft["total_price"] == 450 * 2
    assert draft["time_end"] == "20:00"


def test_propose_booking_rejects_taken_slot():
    draft = tools.propose_booking(
        user_id=1, court_id="bbc-01",
        date_iso="2099-06-01", time_start="18:00", duration=1,
        bookings=SAMPLE_BOOKINGS,
    )
    assert draft["kind"] == "error"
    assert "not available" in draft["message"].lower()


def test_propose_cancel_returns_draft_for_existing():
    draft = tools.propose_cancel(
        user_id=1, txn_id="ZP-90001", bookings=SAMPLE_BOOKINGS,
    )
    assert draft["kind"] == "cancel_draft"
    assert draft["txn_id"] == "ZP-90001"
    assert draft["court_name"] == "Bangkok Badminton Center"


def test_propose_cancel_rejects_unknown_txn():
    draft = tools.propose_cancel(
        user_id=1, txn_id="ZP-99999", bookings=SAMPLE_BOOKINGS,
    )
    assert draft["kind"] == "error"


def test_dispatch_propose_booking_threads_bookings():
    result = tools.dispatch(
        "propose_booking",
        {"court_id": "bbc-01", "date_iso": "2099-08-01", "time_start": "10:00", "duration": 1},
        user_id=1,
        bookings=[],
    )
    assert result["kind"] == "booking_draft"
