# Demand Forecasting & No-Show Prediction — Design Spec

**Date:** 2026-05-05
**Author:** ZPOTS team
**Status:** Approved (pending written review)

## 1. Goal

Add two traditional ML features to the ZPOTS Streamlit app, with companion Jupyter notebooks intended to teach the underlying ML concepts to a beginner.

1. **Demand Forecasting** — time-series regression predicting hourly bookings per court for the next 7 days. Powers the heatmap on `pages/owner/ai_insights.py` and the highlighted opportunity on `pages/owner/optimization.py`.
2. **No-Show / Cancellation Prediction** — binary classifier predicting the probability that a confirmed booking will be a no-show. Powers a "Risk" badge column on `pages/owner/booking_dashboard.py`.

Both notebooks are written for a beginner-friendly audience: every concept is explained in markdown cells with small, focused code cells.

## 2. Non-Goals

- Real historical data integration (everything runs on a synthetic generator).
- Online retraining / MLOps pipelines.
- Hyperparameter tuning beyond reasonable defaults.
- Replacing the existing LLM-driven copy in AI Insights — only the heatmap and the optimization headline slot are model-driven.

## 3. File & Directory Layout

```
ZPOTS/
├── ml/
│   ├── data/
│   │   ├── generate_bookings.py
│   │   ├── bookings.csv
│   │   └── bookings_labeled.csv
│   ├── notebooks/
│   │   ├── 01_demand_forecasting.ipynb
│   │   └── 02_no_show_prediction.ipynb
│   ├── models/
│   │   ├── demand_rf.pkl
│   │   ├── noshow_rf.pkl
│   │   └── demand_predictions.parquet
│   └── README.md
├── utils/
│   └── ml_inference.py
└── requirements.txt   (+ scikit-learn, joblib, jupyter, pyarrow)
```

The `ml/` tree is self-contained — a learner can clone, open notebooks, retrain, without touching the app. The app depends only on the artifacts in `ml/models/`.

## 4. Mock Data Generator

Single script `ml/data/generate_bookings.py` produces both datasets so they remain consistent.

**Granularity:** one row per *court × hour* across operating hours (08:00–22:00) for the trailing ~12 weeks ending today.

**Schema (`bookings.csv`):**

| column | type | notes |
|---|---|---|
| `timestamp` | datetime | hourly |
| `court_id` | str | from existing `data/dummy_data.py::COURTS` |
| `sport` | str | derived from court |
| `district` | str | derived from court |
| `day_of_week` | int | 0=Mon |
| `hour` | int | 8–22 |
| `is_weekend` | bool | |
| `is_holiday` | bool | sparse, ~5 flagged days in window |
| `weather` | enum | sunny / cloudy / rainy |
| `price` | int | from court base/prime price |
| `bookings` | int | **target** for demand model |

**Patterns baked in (clean, Q2 option A):**

- Weekday 18–21h → ~85% booked
- Weekend afternoons high; weekend mornings sport-dependent (badminton high, football low)
- Outdoor sports (football, basketball when noted open-air) drop ~60% on `rainy`
- Small Gaussian noise so models have signal to learn rather than memorize

**No-show dataset (`bookings_labeled.csv`, Q2 option B-lite):** take rows where `bookings > 0`, add a `status` column with rule-based labels plus noise:

- Base no-show rate: 8%
- `lead_time_days > 14` → +15%
- `price > 700` → −5%
- `is_repeat_customer == False` → +10%
- 5% random label flips for realistic noise
- Final labels: `completed` / `no_show` / `cancelled` (cancelled is a small slice, used as positive class together with no_show)

**Approx volume:** ~10 courts × 15 hrs × 84 days ≈ 12.6k rows for demand; ~6k booked rows for no-show.

## 5. Notebook 1 — `01_demand_forecasting.ipynb`

Beginner-friendly. Each numbered section is a markdown cell + one or more small code cells.

1. What are we predicting? — problem framing, one row preview
2. Load & peek at the data — `pd.read_csv`, `.head()`, `.describe()`
3. Visualize the patterns — bookings by hour, by day, by sport (matplotlib bars)
4. Feature engineering — explain one-hot encoding and lag features; build `X` and `y`
5. Train/test split — explain *why* time-series is split chronologically (no shuffle); 80/20
6. Baseline: Linear Regression — fit, MAE/RMSE, predicted-vs-actual scatter
7. Why linear isn't enough — residual plot, evening-peak underprediction
8. Upgrade: Random Forest Regressor — fit, compare metrics
9. Feature importance plot — interpret which features matter
10. Generate the 7-day × 24-hour forecast — predict next week per court, save to `demand_predictions.parquet`

## 6. Notebook 2 — `02_no_show_prediction.ipynb`

Same teaching arc as Notebook 1.

1. What are we predicting? — binary classification framing
2. Load labeled data — show class balance (imbalanced)
3. Visualize: who no-shows? — bars by lead_time, price, repeat_customer
4. Feature engineering — encode categoricals, derive `lead_time_days`, `is_repeat_customer`
5. Train/test split — **stratified**; explain why for imbalanced data
6. Baseline: Logistic Regression — fit, confusion matrix, precision/recall, ROC curve
7. Interpret coefficients — which features push risk up/down
8. Upgrade: Random Forest Classifier — fit, compare ROC AUC
9. Threshold tuning — show precision/recall trade-off; pick cutoffs for Low / Medium / High tiers (e.g., <0.15, 0.15–0.40, >0.40)
10. Save model — `joblib.dump` to `noshow_rf.pkl`

## 7. App Integration

### `utils/ml_inference.py` (new)

Two public functions, both Streamlit-cached:

- `get_demand_forecast() -> pd.DataFrame` — reads `demand_predictions.parquet`. Cached with `@st.cache_data`. Columns: `court_id, day_of_week, hour, predicted_bookings`.
- `predict_noshow_risk(booking: dict) -> tuple[str, float]` — loads `noshow_rf.pkl` once via `@st.cache_resource`, returns `("Low"|"Medium"|"High", probability)`.

### `pages/owner/ai_insights.py`

Replace the dummy gradient `<div>` heatmap with a Plotly imshow heatmap (rows = days, cols = hours) built from `get_demand_forecast()`. Sport/court selector reuses existing UI patterns.

### `pages/owner/optimization.py`

Find the slot with the largest predicted-vs-current uplift in the forecast and render its day/time/sport into the existing "LIVE OPPORTUNITY" card. Replace hardcoded "Sunday Morning +20%" copy.

### `pages/owner/booking_dashboard.py`

Add a "Risk" column rendered as a colored pill using existing CSS classes (`status-active` for Low, a warning variant for Medium, `status-cancelled` for High). Powered by `predict_noshow_risk()` per row.

## 8. Dependencies

Add to `requirements.txt`:

```
scikit-learn>=1.4
joblib>=1.3
jupyter>=1.0
pyarrow>=14
```

## 9. Out of Scope / Future Work

- Live retraining when new bookings come in
- Per-player personalization (would require real user history)
- Holiday calendar tied to Thai public holidays specifically (currently random sparse flags)
- A/B testing of pricing recommendations driven by the demand model
