from agents.owner import tools


def test_get_revenue_sums_confirmed_in_range():
    # Seed has ZP-90001 at days_from_today=-3 (2098-12-29 with frozen 2099-01-01)
    # and several upcoming, all CONFIRMED. A wide range hits all.
    result = tools.get_revenue(date_from="2090-01-01", date_to="2099-12-31")
    assert result["total_thb"] > 0
    assert result["bookings"] > 0


def test_get_revenue_empty_range():
    result = tools.get_revenue(date_from="1900-01-01", date_to="1900-12-31")
    assert result["total_thb"] == 0


def test_list_bookings_filters_by_court():
    rows = tools.list_bookings(court_id="bbc-01")
    assert all(r["court_id"] == "bbc-01" for r in rows)
    assert len(rows) >= 1


def test_list_bookings_clamps_limit():
    rows = tools.list_bookings(limit=999)
    assert len(rows) <= 200


def test_summarize_courts_returns_all():
    out = tools.summarize_courts()
    assert any(c["id"] == "bbc-01" for c in out)
    assert all({"id", "name", "sport", "district", "price_per_hour"} <= set(c.keys()) for c in out)


def test_get_demand_forecast_returns_list():
    out = tools.get_demand_forecast(top_n=5)
    assert isinstance(out, list)
    assert len(out) <= 5


def test_rank_noshow_risk_sorted_or_empty():
    out = tools.rank_noshow_risk(limit=5)
    assert isinstance(out, list)
    if len(out) >= 2:
        probs = [r["risk_probability"] for r in out]
        assert probs == sorted(probs, reverse=True)


def test_dispatch_summarize_courts():
    result = tools.dispatch("summarize_courts", {}, user_id=3)
    assert isinstance(result, list)
    assert len(result) > 0
