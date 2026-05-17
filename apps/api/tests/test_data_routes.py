from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_courts_returns_six():
    r = client.get("/courts")
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 6
    assert body[0]["id"] == "bbc-01"


def test_get_court_by_id_404_for_unknown():
    assert client.get("/courts/nope").status_code == 404


def test_get_court_by_id_success():
    r = client.get("/courts/bbc-01")
    assert r.status_code == 200
    assert r.json()["name"] == "Bangkok Badminton Center"


def test_get_bookings_filters_by_user_id():
    r = client.get("/bookings?user_id=1")
    assert r.status_code == 200
    rows = r.json()
    assert all(row["user_id"] == 1 for row in rows)
    assert len(rows) >= 2  # ZP-90101 + ZP-90001 + ZP-90002


def test_post_booking_creates_and_returns_full_row():
    r = client.post("/bookings", json={
        "user_id": 1, "court_id": "ivh-06",
        "date": "2099-06-01", "time_start": "10:00", "duration": 1,
        "player_name": "Test",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["court_name"] == "Impact Volleyball Hall"
    assert body["total_price"] == 350
    assert body["status"] == "CONFIRMED"
    assert body["txn_id"].startswith("ZP-")


def test_post_booking_unknown_court_returns_422():
    r = client.post("/bookings", json={
        "user_id": 1, "court_id": "does-not-exist",
        "date": "2099-06-01", "time_start": "10:00", "duration": 1,
    })
    assert r.status_code == 422


def test_post_booking_slot_conflict_returns_409():
    # ZP-90101 holds bbc-01 on 2099-01-02 18:00-20:00. Try 19:00 same day.
    r = client.post("/bookings", json={
        "user_id": 1, "court_id": "bbc-01",
        "date": "2099-01-02", "time_start": "19:00", "duration": 1,
    })
    assert r.status_code == 409


def test_cancel_booking_marks_cancelled():
    r = client.post("/bookings/ZP-90101/cancel")
    assert r.status_code == 200
    assert r.json()["status"] == "CANCELLED"


def test_cancel_unknown_returns_404():
    assert client.post("/bookings/ZP-NOPE/cancel").status_code == 404
