"""Synthetic booking-history generator for ZPOTS ML.

Produces two CSVs:
  - ml/data/bookings.csv           one row per (court, hour) in the last ~12 weeks
  - ml/data/bookings_labeled.csv   booked rows only, with a status label

Patterns baked in (clean enough to teach, noisy enough to learn):
  * Weekday 18-21h is hot
  * Weekend afternoons hot; weekend mornings sport-dependent
  * Outdoor sports drop on rainy days
  * Small Gaussian noise so models have signal, not memorization
"""
from __future__ import annotations
import os, sys, random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Allow `python ml/data/generate_bookings.py` from repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from data.dummy_data import COURTS  # noqa: E402

RNG = np.random.default_rng(42)
random.seed(42)

WEEKS = 12
HOURS = list(range(8, 23))  # 08:00 .. 22:00 inclusive
OUTDOOR_SPORTS = {"Football", "Basketball"}  # rainy hits these hardest
WEATHER_CHOICES = np.array(["sunny", "cloudy", "rainy"])
WEATHER_PROBS = np.array([0.55, 0.30, 0.15])


def base_demand(sport: str, dow: int, hour: int) -> float:
    """Return expected booking probability in [0,1] before weather/noise."""
    weekend = dow >= 5

    # Evening peak everywhere
    if 18 <= hour <= 21:
        peak = 0.85 if not weekend else 0.75
    elif 17 <= hour <= 22:
        peak = 0.55
    elif 12 <= hour <= 16:
        peak = 0.55 if weekend else 0.35
    else:  # mornings
        if weekend and sport == "Badminton":
            peak = 0.65
        elif weekend and sport == "Football":
            peak = 0.25
        else:
            peak = 0.20

    # Sport-specific tweaks
    if sport == "Padel":
        peak *= 1.05
    return float(np.clip(peak, 0.0, 0.95))


def generate_bookings_df() -> pd.DataFrame:
    end = datetime.now().replace(minute=0, second=0, microsecond=0)
    start = end - timedelta(weeks=WEEKS)

    # Sparse holiday flags: pick 5 random days in the window
    all_days = pd.date_range(start.date(), end.date(), freq="D")
    holidays = set(pd.to_datetime(RNG.choice(all_days, size=5, replace=False)).date)

    # Daily weather (one weather per calendar day)
    weather_by_day = {
        d.date(): RNG.choice(WEATHER_CHOICES, p=WEATHER_PROBS) for d in all_days
    }

    rows = []
    for court in COURTS:
        sport = court["sport"]
        # Number of sub-courts at this venue (some courts have multiple)
        n_sub = max(1, len(court.get("courts", [{"number": "01"}])))
        is_outdoor = sport in OUTDOOR_SPORTS

        ts = start
        while ts <= end:
            if ts.hour in HOURS:
                dow = ts.weekday()
                weather = str(weather_by_day[ts.date()])
                p = base_demand(sport, dow, ts.hour)
                if is_outdoor and weather == "rainy":
                    p *= 0.40
                # Each sub-court is an independent Bernoulli trial
                booked = int(RNG.binomial(n_sub, p))
                price = court["prime_price"] if 18 <= ts.hour <= 21 else court["price_per_hour"]
                rows.append({
                    "timestamp": ts,
                    "court_id": court["id"],
                    "sport": sport,
                    "district": court["district"],
                    "day_of_week": dow,
                    "hour": ts.hour,
                    "is_weekend": dow >= 5,
                    "is_holiday": ts.date() in holidays,
                    "weather": weather,
                    "price": int(price),
                    "n_courts": n_sub,
                    "bookings": booked,
                })
            ts += timedelta(hours=1)
    return pd.DataFrame(rows)


def label_no_shows(df: pd.DataFrame) -> pd.DataFrame:
    """Expand booked rows into one row per booking and assign a status label."""
    booked = df[df["bookings"] > 0].copy()
    # Explode so each individual booking is one row
    booked = booked.loc[booked.index.repeat(booked["bookings"])].reset_index(drop=True)

    n = len(booked)
    booked["lead_time_days"] = RNG.integers(0, 30, size=n)
    booked["is_repeat_customer"] = RNG.random(size=n) > 0.45  # 55% repeat

    # Base no-show probability
    p = np.full(n, 0.08)
    p += np.where(booked["lead_time_days"] > 14, 0.15, 0.0)
    p += np.where(booked["price"] > 700, -0.05, 0.0)
    p += np.where(~booked["is_repeat_customer"], 0.10, 0.0)
    p = np.clip(p, 0.01, 0.85)

    draws = RNG.random(size=n)
    is_no_show = draws < p
    flip = RNG.random(size=n) < 0.05
    is_no_show = np.where(flip, ~is_no_show, is_no_show)

    cancel = (~is_no_show) & (RNG.random(size=n) < 0.06)

    status = np.where(is_no_show, "no_show", np.where(cancel, "cancelled", "completed"))
    booked["status"] = status
    return booked


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    df = generate_bookings_df()
    df.to_csv(os.path.join(out_dir, "bookings.csv"), index=False)
    print(f"Wrote bookings.csv: {len(df):,} rows")

    labeled = label_no_shows(df)
    labeled.to_csv(os.path.join(out_dir, "bookings_labeled.csv"), index=False)
    print(f"Wrote bookings_labeled.csv: {len(labeled):,} rows")
    print("Status balance:")
    print(labeled["status"].value_counts(normalize=True).round(3))


if __name__ == "__main__":
    main()
