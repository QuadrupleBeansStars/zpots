from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_demand_forecast_returns_cells():
    r = client.get("/ml/demand-forecast")
    assert r.status_code == 200
    body = r.json()
    assert "cells" in body
    # Either real artifact loaded (many cells) or missing artifact (empty list)
    assert isinstance(body["cells"], list)
    if body["cells"]:
        cell = body["cells"][0]
        assert {"court_id", "day_of_week", "hour", "predicted_bookings"} <= set(cell.keys())


def test_noshow_risk_batch_returns_one_result_per_item():
    r = client.post("/ml/noshow-risk/batch", json={
        "items": [
            {"sport": "Badminton", "hour": 18, "district": "Sukhumvit"},
            {"sport": "Football", "hour": 19, "district": "Thong Lor"},
        ],
    })
    assert r.status_code == 200
    body = r.json()
    assert len(body["results"]) == 2
    for result in body["results"]:
        assert result["tier"] in ("Low", "Medium", "High")
        assert 0.0 <= result["probability"] <= 1.0


def test_noshow_risk_batch_empty_input():
    r = client.post("/ml/noshow-risk/batch", json={"items": []})
    assert r.status_code == 200
    assert r.json() == {"results": []}
