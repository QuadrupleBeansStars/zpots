"""ML inference helpers for the FastAPI service. Ported from utils/ml_inference.py."""
from __future__ import annotations
import os
from typing import Any

import joblib
import pandas as pd

ML_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "ml", "models",
)
DEMAND_PARQUET = os.path.join(ML_DIR, "demand_predictions.parquet")
NOSHOW_PKL = os.path.join(ML_DIR, "noshow_rf.pkl")

_demand_df: pd.DataFrame | None = None
_noshow_artifact: dict[str, Any] | None = None


def get_demand_forecast() -> pd.DataFrame:
    """Return precomputed 7-day forecast. Empty DataFrame if artifact is missing."""
    global _demand_df
    if _demand_df is None:
        if not os.path.exists(DEMAND_PARQUET):
            _demand_df = pd.DataFrame(columns=["court_id", "day_of_week", "hour", "predicted_bookings"])
        else:
            _demand_df = pd.read_parquet(DEMAND_PARQUET)
    return _demand_df


def _load_noshow_artifact() -> dict[str, Any] | None:
    global _noshow_artifact
    if _noshow_artifact is None and os.path.exists(NOSHOW_PKL):
        _noshow_artifact = joblib.load(NOSHOW_PKL)
    return _noshow_artifact


def predict_noshow_risk(booking: dict) -> tuple[str, float]:
    """Predict no-show risk for a single booking dict.

    Expected keys (best-effort; missing ones default to neutral values):
      sport, district, day_of_week, hour, is_weekend, is_holiday, weather,
      price, lead_time_days, is_repeat_customer
    """
    art = _load_noshow_artifact()
    if art is None:
        return ("Low", 0.0)

    row = {
        "sport": booking.get("sport", "Badminton"),
        "district": booking.get("district", "Sukhumvit"),
        "day_of_week": int(booking.get("day_of_week", 2)),
        "hour": int(booking.get("hour", 18)),
        "is_weekend": bool(booking.get("is_weekend", False)),
        "is_holiday": bool(booking.get("is_holiday", False)),
        "weather": booking.get("weather", "sunny"),
        "price": int(booking.get("price", 500)),
        "lead_time_days": int(booking.get("lead_time_days", 3)),
        "is_repeat_customer": bool(booking.get("is_repeat_customer", True)),
    }
    df = pd.DataFrame([row])
    encoded = pd.get_dummies(df, columns=["sport", "district", "weather"], drop_first=True)
    encoded = encoded.reindex(columns=art["feature_columns"], fill_value=0)
    p = float(art["model"].predict_proba(encoded)[0, 1])

    if p < art["threshold_low_med"]:
        tier = "Low"
    elif p < art["threshold_med_high"]:
        tier = "Medium"
    else:
        tier = "High"
    return tier, p
