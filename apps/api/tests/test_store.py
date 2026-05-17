import pytest

from data import store


SEED_COURTS = [
    {"id": "bbc-01", "name": "Bangkok Badminton Center", "sport": "Badminton",
     "district": "Sukhumvit", "price_per_hour": 450},
    {"id": "sky-02", "name": "Skyline", "sport": "Football",
     "district": "Thong Lor", "price_per_hour": 1200},
]

SEED_BOOKINGS = [
    {"txn_id": "ZP-1", "user_id": 1, "player_name": "Alex", "court_id": "bbc-01",
     "court_name": "Bangkok Badminton Center", "date": "2099-01-02",
     "time_start": "18:00", "time_end": "20:00", "duration": 2,
     "total_price": 900, "status": "CONFIRMED"},
    {"txn_id": "ZP-2", "user_id": 2, "player_name": "Bob", "court_id": "sky-02",
     "court_name": "Skyline", "date": "2099-01-03",
     "time_start": "20:00", "time_end": "21:00", "duration": 1,
     "total_price": 1200, "status": "CONFIRMED"},
]


def _make_bs():
    return store.BookingsStore(SEED_BOOKINGS)


def test_courts_store_by_id():
    cs = store.CourtsStore(SEED_COURTS)
    assert cs.by_id("bbc-01")["name"] == "Bangkok Badminton Center"
    assert cs.by_id("nope") is None
    assert len(cs.all()) == 2


def test_bookings_store_filters():
    bs = _make_bs()
    assert len(bs.for_user(1)) == 1
    assert bs.for_user(1)[0]["txn_id"] == "ZP-1"
    assert len(bs.for_court("sky-02")) == 1
    assert len(bs.all()) == 2


def test_bookings_store_add_assigns_txn_id_if_missing():
    bs = _make_bs()
    row = bs.add({
        "user_id": 1, "player_name": "Alex", "court_id": "bbc-01",
        "court_name": "Bangkok Badminton Center", "date": "2099-02-01",
        "time_start": "10:00", "time_end": "11:00", "duration": 1,
        "total_price": 450, "status": "CONFIRMED",
    })
    assert row["txn_id"].startswith("ZP-")
    assert len(bs.all()) == 3


def test_bookings_store_cancel_marks_status():
    bs = _make_bs()
    cancelled = bs.cancel("ZP-1")
    assert cancelled["status"] == "CANCELLED"
    assert bs.for_user(1)[0]["status"] == "CANCELLED"


def test_bookings_store_cancel_unknown_returns_none():
    bs = _make_bs()
    assert bs.cancel("ZP-DOES-NOT-EXIST") is None


def test_bookings_store_has_conflict_detects_overlap():
    bs = _make_bs()
    # bbc-01 on 2099-01-02 has 18:00-20:00 taken. Booking 19:00 should conflict.
    assert bs.has_conflict("bbc-01", "2099-01-02", "19:00", 1) is True
    # 20:00 same day starts where the existing ends — should NOT conflict.
    assert bs.has_conflict("bbc-01", "2099-01-02", "20:00", 1) is False
    # Different court, same time — no conflict.
    assert bs.has_conflict("sky-02", "2099-01-02", "18:00", 2) is False


def test_bookings_store_reset_replaces_all_rows():
    bs = _make_bs()
    bs.add({"user_id": 9, "player_name": "X", "court_id": "bbc-01",
            "court_name": "Bangkok Badminton Center", "date": "2099-03-01",
            "time_start": "10:00", "time_end": "11:00", "duration": 1,
            "total_price": 450, "status": "CONFIRMED"})
    assert len(bs.all()) == 3
    bs.reset(SEED_BOOKINGS)
    assert len(bs.all()) == 2
