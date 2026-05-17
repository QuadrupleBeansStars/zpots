from datetime import date

import pytest

from data import seed_loader


@pytest.fixture
def frozen_today(monkeypatch):
    monkeypatch.setattr(seed_loader, "_today", lambda: date(2099, 1, 1))


def test_load_courts_returns_six_with_required_fields():
    courts = seed_loader.load_courts()
    assert len(courts) == 6
    for c in courts:
        assert {"id", "name", "sport", "district", "price_per_hour", "utilization_pct"} <= set(c.keys())


def test_load_bookings_resolves_date_from_offset(frozen_today):
    courts = seed_loader.load_courts()
    rows = seed_loader.load_bookings(courts)
    # today=2099-01-01; days_from_today=1 entry should resolve to 2099-01-02
    today_plus_one = [r for r in rows if r["date"] == "2099-01-02"]
    assert len(today_plus_one) >= 1


def test_load_bookings_derives_time_end_and_court_name_and_total_price(frozen_today):
    courts = seed_loader.load_courts()
    rows = seed_loader.load_bookings(courts)
    alex = next(r for r in rows if r["txn_id"] == "ZP-90101")
    assert alex["time_end"] == "20:00"               # 18:00 + 2h
    assert alex["court_name"] == "Bangkok Badminton Center"
    assert alex["total_price"] == 900                # 450 * 2
    assert alex["date"] == "2099-01-02"


def test_load_bookings_raises_on_unknown_court():
    courts = [{"id": "only-this-court", "name": "X", "price_per_hour": 100}]
    with pytest.raises(KeyError):
        seed_loader.load_bookings(courts)
