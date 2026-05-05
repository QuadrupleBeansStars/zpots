# Demand Forecasting & No-Show Prediction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a demand-forecasting regression model and a no-show classification model to ZPOTS, with beginner-friendly Jupyter notebooks that teach the underlying ML, and wire both into the existing Streamlit owner pages.

**Architecture:** Self-contained `ml/` directory holds a synthetic-data generator, two notebooks, and saved artifacts (`*.pkl` for live inference, `*.parquet` for precomputed forecasts). A new `utils/ml_inference.py` is the only bridge between artifacts and the app. Three owner pages (`ai_insights`, `optimization`, `booking_dashboard`) consume the predictions.

**Tech Stack:** Python 3, pandas, numpy, scikit-learn (LinearRegression, LogisticRegression, RandomForestRegressor, RandomForestClassifier), matplotlib, plotly, joblib, pyarrow, jupyter, Streamlit.

**Spec:** `docs/superpowers/specs/2026-05-05-ml-demand-and-noshow-design.md`

**Note on TDD:** This plan involves notebooks and a Streamlit app; classical TDD does not fit cleanly. We use **verification steps** instead — run scripts, inspect output shapes, smoke-test the app — as the equivalent of "the test passed."

---

## Task 1: Bootstrap `ml/` tree and add dependencies

**Files:**
- Create: `ml/__init__.py`, `ml/data/__init__.py`, `ml/notebooks/.gitkeep`, `ml/models/.gitkeep`
- Create: `ml/README.md`
- Modify: `requirements.txt`
- Modify: `.gitignore`

- [ ] **Step 1: Create directory tree**

```bash
mkdir -p ml/data ml/notebooks ml/models
touch ml/__init__.py ml/data/__init__.py ml/notebooks/.gitkeep ml/models/.gitkeep
```

- [ ] **Step 2: Add dependencies to `requirements.txt`**

Append these lines (do not remove existing entries):

```
scikit-learn>=1.4
joblib>=1.3
jupyter>=1.0
pyarrow>=14
matplotlib>=3.8
numpy>=1.26
pandas>=2.1
```

- [ ] **Step 3: Update `.gitignore`** so generated CSVs and large artifacts can be committed but checkpoints are ignored. Append:

```
ml/notebooks/.ipynb_checkpoints/
```

- [ ] **Step 4: Write `ml/README.md`**

```markdown
# ZPOTS ML

Self-contained ML workspace. The Streamlit app consumes only the artifacts in `ml/models/`.

## Layout

- `data/generate_bookings.py` — synthetic data generator
- `data/bookings.csv` — hourly per-court booking history (target = `bookings`)
- `data/bookings_labeled.csv` — booked rows with no-show labels
- `notebooks/01_demand_forecasting.ipynb` — beginner walkthrough → trains `demand_rf.pkl` and writes `demand_predictions.parquet`
- `notebooks/02_no_show_prediction.ipynb` — beginner walkthrough → trains `noshow_rf.pkl`
- `models/` — saved artifacts loaded by the app

## Regenerate everything

```bash
python ml/data/generate_bookings.py
jupyter nbconvert --to notebook --execute ml/notebooks/01_demand_forecasting.ipynb --inplace
jupyter nbconvert --to notebook --execute ml/notebooks/02_no_show_prediction.ipynb --inplace
```
```

- [ ] **Step 5: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: scikit-learn, joblib, jupyter, pyarrow, matplotlib install cleanly.

- [ ] **Step 6: Commit**

```bash
git add ml/ requirements.txt .gitignore
git commit -m "chore: scaffold ml/ workspace and add ML dependencies"
```

---

## Task 2: Build the synthetic data generator

**Files:**
- Create: `ml/data/generate_bookings.py`

This script produces `bookings.csv` (full hourly grid with target `bookings`) and `bookings_labeled.csv` (booked rows + `status` label).

- [ ] **Step 1: Write `ml/data/generate_bookings.py`**

```python
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
                # Tiny continuous noise channel (kept implicit via Bernoulli)
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

    # Synthetic per-booking attributes
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
    # 5% random label flips for realism
    flip = RNG.random(size=n) < 0.05
    is_no_show = np.where(flip, ~is_no_show, is_no_show)

    # Cancellation slice (a small share of non-no-shows)
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
```

- [ ] **Step 2: Run the generator and verify output**

Run: `python ml/data/generate_bookings.py`

Expected stdout (numbers approximate):
```
Wrote bookings.csv: 12,xxx rows
Wrote bookings_labeled.csv: 6,xxx rows
Status balance:
completed    0.85x
no_show      0.10x
cancelled    0.05x
```

- [ ] **Step 3: Spot-check the data**

Run:
```bash
python -c "import pandas as pd; df = pd.read_csv('ml/data/bookings.csv'); print(df.head()); print(df.groupby('hour')['bookings'].mean().round(2))"
```

Expected: hour 18–21 mean clearly higher than hour 8–10. If not, the generator is wrong — fix before continuing.

- [ ] **Step 4: Commit**

```bash
git add ml/data/
git commit -m "feat(ml): add synthetic booking data generator + datasets"
```

---

## Task 3: Notebook 1 — Demand Forecasting (Sections 1–5: data, EDA, features, split)

**Files:**
- Create: `ml/notebooks/01_demand_forecasting.ipynb`

Notebooks are JSON. Use `jupyter nbconvert` for execution. Construct the notebook by writing a Python helper that emits the JSON, OR build it interactively. Below we list the cells in order. Each section is one or more cells. Use markdown cells liberally — this notebook is for teaching.

> **Implementation tip:** the easiest authoring path is to write a small Python script `ml/notebooks/_build_nb1.py` that uses `nbformat` to assemble cells, run it once, then delete the script. Or write the `.ipynb` JSON directly. Either works — the *cell contents below are the contract*.

- [ ] **Step 1: Section 1 — Title & problem framing (markdown)**

```markdown
# Demand Forecasting for ZPOTS

**Goal:** predict how many bookings a court will receive in a given hour, so the owner dashboard can show a 7-day demand heatmap.

**Why this matters:** if we know which slots will be hot, owners can:
- raise prices on peak slots
- run promotions on dead slots
- spot demand surges before the customer feels them

**The ML task:** *time-series regression* — input = features describing a court-hour, output = a number (predicted bookings).
```

- [ ] **Step 2: Section 2 — Load & peek (markdown + code)**

Markdown:
```markdown
## 1. Load the data

Each row is one (court, hour) over the last 12 weeks.
```

Code:
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("../data/bookings.csv", parse_dates=["timestamp"])
print(f"Rows: {len(df):,}")
df.head()
```

Code (next cell):
```python
df.describe(include="all").T
```

- [ ] **Step 3: Section 3 — Visualize patterns (markdown + 3 code cells)**

Markdown:
```markdown
## 2. What does the data look like?

Before any modeling, **always look at the data**. We're hunting for patterns
the model will need to learn — and for surprises.
```

Code (cell 1 — by hour):
```python
hourly = df.groupby("hour")["bookings"].mean()
hourly.plot(kind="bar", figsize=(8,3), title="Average bookings by hour of day")
plt.ylabel("avg bookings"); plt.xlabel("hour"); plt.show()
```

Code (cell 2 — by day of week):
```python
dow_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
daily = df.groupby("day_of_week")["bookings"].mean()
daily.index = dow_labels
daily.plot(kind="bar", figsize=(6,3), title="Average bookings by day of week", color="#506300")
plt.show()
```

Code (cell 3 — by sport × weather):
```python
df.groupby(["sport","weather"])["bookings"].mean().unstack().plot(
    kind="bar", figsize=(8,3), title="Bookings by sport × weather"
)
plt.ylabel("avg bookings"); plt.show()
```

Markdown (cell 4 — interpretation):
```markdown
**What we see:**
- Big evening peak (18–21h)
- Weekends slightly lower on average (the *evening peak* is what drives demand, not the day)
- Football and Basketball drop hard on rainy days — **weather matters for outdoor sports**

These are exactly the patterns we expect a model to capture.
```

- [ ] **Step 4: Section 4 — Feature engineering (markdown + code)**

Markdown:
```markdown
## 3. Feature engineering

A model can't read words like "Sunday" or "rainy". We need numbers.

**One-hot encoding** turns one categorical column into many 0/1 columns —
one per category. We use `pd.get_dummies` for this.

We also add **lag features**: "how many bookings did this same court see at this hour *yesterday*?"
For time series, the recent past is often the strongest predictor.
```

Code:
```python
# Sort so lag features are well-defined
df = df.sort_values(["court_id", "timestamp"]).reset_index(drop=True)

# Lag: same court, 24 hours ago
df["bookings_lag_24h"] = df.groupby("court_id")["bookings"].shift(24).fillna(0)

# One-hot encode categoricals
features = pd.get_dummies(
    df[["court_id","sport","district","day_of_week","hour",
        "is_weekend","is_holiday","weather","price","n_courts","bookings_lag_24h"]],
    columns=["court_id","sport","district","weather"],
    drop_first=True,
)
target = df["bookings"]

print("Feature matrix shape:", features.shape)
features.head()
```

- [ ] **Step 5: Section 5 — Train/test split (markdown + code)**

Markdown:
```markdown
## 4. Train/test split

For most ML problems we shuffle the data and split randomly. **Not for time series.**
If we randomly mix past and future rows, the model "cheats" — it learns from
tomorrow to predict today. That looks great in evaluation and fails in production.

We split **chronologically**: first 80% of time → train, last 20% → test.
```

Code:
```python
split_idx = int(len(df) * 0.80)
X_train, X_test = features.iloc[:split_idx], features.iloc[split_idx:]
y_train, y_test = target.iloc[:split_idx], target.iloc[split_idx:]

print(f"Train: {len(X_train):,} rows, Test: {len(X_test):,} rows")
print(f"Train period: {df['timestamp'].iloc[0]} → {df['timestamp'].iloc[split_idx-1]}")
print(f"Test  period: {df['timestamp'].iloc[split_idx]} → {df['timestamp'].iloc[-1]}")
```

- [ ] **Step 6: Save the notebook and execute Sections 1–5**

```bash
jupyter nbconvert --to notebook --execute ml/notebooks/01_demand_forecasting.ipynb --inplace
```

Expected: no execution errors, "Train: ~10k, Test: ~2.5k rows" prints.

- [ ] **Step 7: Commit**

```bash
git add ml/notebooks/01_demand_forecasting.ipynb
git commit -m "feat(ml): notebook 1 sections 1-5 (load, EDA, features, split)"
```

---

## Task 4: Notebook 1 — Sections 6–7 (Linear Regression baseline + residuals)

**Files:**
- Modify: `ml/notebooks/01_demand_forecasting.ipynb`

- [ ] **Step 1: Section 6 — Linear Regression baseline (markdown + code)**

Markdown:
```markdown
## 5. Baseline model: Linear Regression

**Always start with a simple model.** It gives you a yardstick for whether
fancier models are actually helping, and it's easy to debug.

Linear Regression assumes the answer is a weighted sum of the features:
`bookings ≈ w1·feature1 + w2·feature2 + ...`. Simple, fast, very interpretable.

We measure error with:
- **MAE** (Mean Absolute Error): "on average we're off by this many bookings"
- **RMSE** (Root Mean Squared Error): like MAE but penalizes big misses harder
```

Code:
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

lin = LinearRegression()
lin.fit(X_train, y_train)
pred_lin = lin.predict(X_test)

mae = mean_absolute_error(y_test, pred_lin)
rmse = mean_squared_error(y_test, pred_lin, squared=False)
print(f"Linear  MAE: {mae:.3f}   RMSE: {rmse:.3f}")
```

Code (predicted vs actual scatter):
```python
plt.figure(figsize=(5,5))
plt.scatter(y_test, pred_lin, alpha=0.2, s=8)
plt.plot([0, y_test.max()], [0, y_test.max()], "r--", label="perfect")
plt.xlabel("actual bookings"); plt.ylabel("predicted bookings")
plt.title("Linear Regression: predicted vs actual"); plt.legend(); plt.show()
```

- [ ] **Step 2: Section 7 — Residual analysis (markdown + code)**

Markdown:
```markdown
## 6. Where does the linear model fail?

A **residual** is `actual − predicted`. Plotting residuals by hour shows us
*when* the model is wrong, not just *how much*.
```

Code:
```python
test_df = df.iloc[split_idx:].copy()
test_df["pred"] = pred_lin
test_df["residual"] = test_df["bookings"] - test_df["pred"]

test_df.groupby("hour")["residual"].mean().plot(
    kind="bar", figsize=(8,3), title="Avg residual by hour (positive = under-predicted)"
)
plt.axhline(0, color="black", lw=0.8); plt.show()
```

Markdown (interpretation):
```markdown
The linear model **systematically under-predicts** the evening peak. Linear models
can't easily capture interactions like "evening AND weekend AND not rainy".
We need a model that handles non-linear feature interactions automatically.
```

- [ ] **Step 3: Re-execute and commit**

```bash
jupyter nbconvert --to notebook --execute ml/notebooks/01_demand_forecasting.ipynb --inplace
git add ml/notebooks/01_demand_forecasting.ipynb
git commit -m "feat(ml): notebook 1 sections 6-7 (linear baseline + residuals)"
```

---

## Task 5: Notebook 1 — Sections 8–9 (Random Forest + feature importance)

**Files:**
- Modify: `ml/notebooks/01_demand_forecasting.ipynb`

- [ ] **Step 1: Section 8 — Random Forest (markdown + code)**

Markdown:
```markdown
## 7. Upgrade: Random Forest

A **Random Forest** is a collection of decision trees. Each tree learns a different
set of "if-then" rules; the forest averages their predictions. This naturally
captures interactions like "evening AND weekend".

`n_estimators=200` means 200 trees. More = better up to a point, slower to train.
```

Code:
```python
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)

mae_rf = mean_absolute_error(y_test, pred_rf)
rmse_rf = mean_squared_error(y_test, pred_rf, squared=False)
print(f"Linear  MAE: {mae:.3f}   RMSE: {rmse:.3f}")
print(f"Forest  MAE: {mae_rf:.3f}   RMSE: {rmse_rf:.3f}")
```

- [ ] **Step 2: Section 9 — Feature importance (markdown + code)**

Markdown:
```markdown
## 8. Which features matter?

Random Forests can tell us which features drove the prediction. If we trained
a model and the most important feature was random noise, we'd know something
was wrong.
```

Code:
```python
importances = pd.Series(rf.feature_importances_, index=features.columns)
top = importances.sort_values(ascending=True).tail(15)
top.plot(kind="barh", figsize=(7,5), title="Top 15 feature importances", color="#506300")
plt.show()
```

Markdown:
```markdown
**Sanity check:** `hour`, `bookings_lag_24h`, and `day_of_week` should dominate.
If `is_holiday` (which we made very sparse) ranked first, the model probably overfit.
```

- [ ] **Step 3: Re-execute and commit**

```bash
jupyter nbconvert --to notebook --execute ml/notebooks/01_demand_forecasting.ipynb --inplace
git add ml/notebooks/01_demand_forecasting.ipynb
git commit -m "feat(ml): notebook 1 sections 8-9 (random forest + importance)"
```

---

## Task 6: Notebook 1 — Section 10 (generate 7-day forecast + save artifacts)

**Files:**
- Modify: `ml/notebooks/01_demand_forecasting.ipynb`
- Output: `ml/models/demand_rf.pkl`, `ml/models/demand_predictions.parquet`

- [ ] **Step 1: Section 10 — Forecast & persist (markdown + code)**

Markdown:
```markdown
## 9. Generate next week's forecast

We build a synthetic feature matrix for the next 7 days × 24 hours × every court,
predict, and save to `demand_predictions.parquet`. The Streamlit app reads this
file directly — no model loading needed for the heatmap.
```

Code:
```python
import joblib, os, sys
sys.path.insert(0, os.path.abspath("../.."))
from data.dummy_data import COURTS
from datetime import datetime, timedelta

future_rows = []
start_day = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
for court in COURTS:
    for d in range(7):
        for h in range(8, 23):
            ts = start_day + timedelta(days=d, hours=h)
            price = court["prime_price"] if 18 <= h <= 21 else court["price_per_hour"]
            future_rows.append({
                "timestamp": ts,
                "court_id": court["id"],
                "sport": court["sport"],
                "district": court["district"],
                "day_of_week": ts.weekday(),
                "hour": h,
                "is_weekend": ts.weekday() >= 5,
                "is_holiday": False,
                "weather": "sunny",  # neutral default
                "price": int(price),
                "n_courts": max(1, len(court.get("courts", [{"a":1}]))),
                "bookings_lag_24h": 0,  # cold start
            })

future = pd.DataFrame(future_rows)
future_features = pd.get_dummies(
    future[["court_id","sport","district","day_of_week","hour",
            "is_weekend","is_holiday","weather","price","n_courts","bookings_lag_24h"]],
    columns=["court_id","sport","district","weather"],
    drop_first=True,
)
# Align columns with training features (missing → 0)
future_features = future_features.reindex(columns=features.columns, fill_value=0)
future["predicted_bookings"] = rf.predict(future_features).clip(min=0)

out = future[["timestamp","court_id","day_of_week","hour","predicted_bookings"]]
os.makedirs("../models", exist_ok=True)
out.to_parquet("../models/demand_predictions.parquet", index=False)
joblib.dump(rf, "../models/demand_rf.pkl")
print("Saved:", os.listdir("../models"))
out.head()
```

Markdown (sanity check):
```markdown
**Quick sanity check:** average predicted bookings by hour should still show
the evening peak. If it's flat, something went wrong with feature alignment.
```

Code:
```python
out.groupby("hour")["predicted_bookings"].mean().plot(
    kind="bar", figsize=(8,3), title="Forecast: avg predicted bookings by hour"
)
plt.show()
```

- [ ] **Step 2: Re-execute the full notebook end-to-end**

```bash
jupyter nbconvert --to notebook --execute ml/notebooks/01_demand_forecasting.ipynb --inplace
```

Expected: notebook runs clean; `ml/models/demand_rf.pkl` and `ml/models/demand_predictions.parquet` exist.

- [ ] **Step 3: Verify the parquet**

```bash
python -c "import pandas as pd; df = pd.read_parquet('ml/models/demand_predictions.parquet'); print(df.shape); print(df.head()); print('hour mean:'); print(df.groupby('hour')['predicted_bookings'].mean().round(2))"
```

Expected: shape ~(630-1050, 5), evening hours clearly higher than morning hours.

- [ ] **Step 4: Commit**

```bash
git add ml/notebooks/01_demand_forecasting.ipynb ml/models/demand_rf.pkl ml/models/demand_predictions.parquet
git commit -m "feat(ml): notebook 1 forecast generation + saved artifacts"
```

---

## Task 7: Notebook 2 — No-Show Prediction Sections 1–5 (data, EDA, features, split)

**Files:**
- Create: `ml/notebooks/02_no_show_prediction.ipynb`

- [ ] **Step 1: Section 1 — Title & framing (markdown)**

```markdown
# No-Show / Cancellation Prediction

**Goal:** for each booking, predict the probability that the customer won't show up.
Owners use this to flag risky bookings so they can confirm with the customer or
oversell the slot.

**The ML task:** *binary classification* — input = booking features, output = 0 (will show) or 1 (won't).
```

- [ ] **Step 2: Section 2 — Load & class balance (markdown + code)**

Markdown:
```markdown
## 1. Load the data and check class balance

In classification, we always check **how rare each class is**. If only 8% of
bookings are no-shows, a dumb model that always predicts "will show" gets 92%
accuracy — and is useless. **Class imbalance changes how we measure success.**
```

Code:
```python
import pandas as pd, numpy as np, matplotlib.pyplot as plt
df = pd.read_csv("../data/bookings_labeled.csv", parse_dates=["timestamp"])
print(f"Rows: {len(df):,}")
print(df["status"].value_counts(normalize=True).round(3))

# Treat both no_show and cancelled as "missed" (positive class)
df["is_missed"] = df["status"].isin(["no_show","cancelled"]).astype(int)
print(f"\nMissed rate: {df['is_missed'].mean():.1%}")
df.head()
```

- [ ] **Step 3: Section 3 — Who no-shows? (markdown + 3 code cells)**

Markdown:
```markdown
## 2. Visualize: who no-shows?

Looking at the miss rate broken down by each feature tells us which signals
the model will likely use.
```

Code (cell 1):
```python
df.groupby(pd.cut(df["lead_time_days"], bins=[-1,3,7,14,30]))["is_missed"].mean().plot(
    kind="bar", figsize=(6,3), title="Miss rate by lead time"
)
plt.ylabel("miss rate"); plt.show()
```

Code (cell 2):
```python
df.groupby("is_repeat_customer")["is_missed"].mean().plot(
    kind="bar", figsize=(4,3), title="Miss rate: repeat vs new customer", color="#506300"
)
plt.show()
```

Code (cell 3):
```python
df.groupby(pd.cut(df["price"], bins=[0,400,700,2000]))["is_missed"].mean().plot(
    kind="bar", figsize=(5,3), title="Miss rate by price band"
)
plt.show()
```

Markdown:
```markdown
**Pattern check:** miss rate should rise with longer lead time and drop for
repeat customers. Those are the signals we baked into the data — confirming
the model has something real to learn.
```

- [ ] **Step 4: Section 4 — Feature engineering (markdown + code)**

Markdown:
```markdown
## 3. Feature engineering

Same idea as Notebook 1 — turn categoricals into 0/1 columns.
```

Code:
```python
features = pd.get_dummies(
    df[["sport","district","day_of_week","hour","is_weekend","is_holiday",
        "weather","price","lead_time_days","is_repeat_customer"]],
    columns=["sport","district","weather"],
    drop_first=True,
)
target = df["is_missed"]
print("Feature matrix:", features.shape)
features.head()
```

- [ ] **Step 5: Section 5 — Stratified split (markdown + code)**

Markdown:
```markdown
## 4. Train/test split — stratified

Because the positive class is rare, a random split could land most of the
no-shows in either train or test by chance. **Stratified split** preserves the
class ratio in both halves.
```

Code:
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42, stratify=target
)
print(f"Train miss rate: {y_train.mean():.3f}   Test miss rate: {y_test.mean():.3f}")
```

- [ ] **Step 6: Execute & commit**

```bash
jupyter nbconvert --to notebook --execute ml/notebooks/02_no_show_prediction.ipynb --inplace
git add ml/notebooks/02_no_show_prediction.ipynb
git commit -m "feat(ml): notebook 2 sections 1-5 (load, EDA, features, split)"
```

---

## Task 8: Notebook 2 — Sections 6–7 (Logistic Regression baseline + interpretation)

**Files:**
- Modify: `ml/notebooks/02_no_show_prediction.ipynb`

- [ ] **Step 1: Section 6 — Logistic Regression (markdown + code)**

Markdown:
```markdown
## 5. Baseline: Logistic Regression

Despite the name, **logistic regression is a classifier**. It outputs a
probability between 0 and 1 by squashing a weighted sum through a sigmoid:

`P(missed) = 1 / (1 + exp(−(w·x + b)))`

We evaluate with:
- **Confusion matrix** — counts of TP / FP / FN / TN
- **Precision** — of the bookings we *flag* as risky, how many actually missed
- **Recall** — of the *actual* missed bookings, how many we caught
- **ROC curve / AUC** — overall ranking quality, threshold-independent
```

Code:
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
from sklearn.preprocessing import StandardScaler

# Logistic regression benefits from scaled inputs
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

logit = LogisticRegression(max_iter=1000, class_weight="balanced")
logit.fit(X_train_s, y_train)
pred_logit = logit.predict(X_test_s)
prob_logit = logit.predict_proba(X_test_s)[:, 1]

print("Confusion matrix:\n", confusion_matrix(y_test, pred_logit))
print("\n", classification_report(y_test, pred_logit, target_names=["showed","missed"]))
print(f"ROC AUC: {roc_auc_score(y_test, prob_logit):.3f}")
```

Code (ROC curve):
```python
fpr, tpr, _ = roc_curve(y_test, prob_logit)
plt.figure(figsize=(5,5))
plt.plot(fpr, tpr, label=f"Logit AUC={roc_auc_score(y_test, prob_logit):.2f}")
plt.plot([0,1],[0,1],"k--", lw=0.8)
plt.xlabel("False Positive Rate"); plt.ylabel("True Positive Rate")
plt.title("ROC curve"); plt.legend(); plt.show()
```

- [ ] **Step 2: Section 7 — Interpret coefficients (markdown + code)**

Markdown:
```markdown
## 6. What did the model learn?

Logistic regression coefficients are interpretable: a **positive** coefficient
means the feature pushes the prediction *toward* "missed". A **negative** one
pushes toward "showed up".
```

Code:
```python
coefs = pd.Series(logit.coef_[0], index=features.columns).sort_values()
fig, ax = plt.subplots(figsize=(6,5))
coefs.head(8).plot(kind="barh", ax=ax, color="#2e6b00", label="pushes toward SHOW")
coefs.tail(8).plot(kind="barh", ax=ax, color="#c62828", label="pushes toward MISS")
plt.title("Logistic regression coefficients (top push in each direction)")
plt.legend(); plt.show()
```

Markdown:
```markdown
**Expected:** `is_repeat_customer` should have a strong negative coefficient
(repeat customers show up); `lead_time_days` positive (long lead = forget).
```

- [ ] **Step 3: Execute & commit**

```bash
jupyter nbconvert --to notebook --execute ml/notebooks/02_no_show_prediction.ipynb --inplace
git add ml/notebooks/02_no_show_prediction.ipynb
git commit -m "feat(ml): notebook 2 sections 6-7 (logistic baseline + coefs)"
```

---

## Task 9: Notebook 2 — Sections 8–10 (Random Forest, threshold tuning, save)

**Files:**
- Modify: `ml/notebooks/02_no_show_prediction.ipynb`
- Output: `ml/models/noshow_rf.pkl`

- [ ] **Step 1: Section 8 — Random Forest classifier (markdown + code)**

Markdown:
```markdown
## 7. Upgrade: Random Forest classifier

Same forest idea as Notebook 1, but predicting a class instead of a number.
Tree-based models don't need scaled features — we feed them the raw matrix.
```

Code:
```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=300, max_depth=10, class_weight="balanced",
    random_state=42, n_jobs=-1,
)
rf.fit(X_train, y_train)
prob_rf = rf.predict_proba(X_test)[:, 1]

print(f"Logistic AUC: {roc_auc_score(y_test, prob_logit):.3f}")
print(f"Forest   AUC: {roc_auc_score(y_test, prob_rf):.3f}")
```

- [ ] **Step 2: Section 9 — Threshold tuning (markdown + code)**

Markdown:
```markdown
## 8. Picking the Low / Medium / High thresholds

The model gives us a probability between 0 and 1. The owner UI shows three
tiers. We pick cutoffs by looking at how the population splits.

A reasonable starting point: bottom ~70% of risk = Low, next ~20% = Medium,
top ~10% = High. Check what probabilities those quantiles correspond to.
```

Code:
```python
q70, q90 = np.quantile(prob_rf, [0.70, 0.90])
print(f"Low/Med cutoff (70th pct): {q70:.3f}")
print(f"Med/High cutoff (90th pct): {q90:.3f}")

def tier(p):
    if p < q70: return "Low"
    if p < q90: return "Medium"
    return "High"

tiers = pd.Series([tier(p) for p in prob_rf])
miss_by_tier = pd.DataFrame({"tier": tiers, "missed": y_test.values}).groupby("tier")["missed"].mean()
print("\nActual miss rate per tier:")
print(miss_by_tier.round(3))
```

Markdown:
```markdown
**Sanity check:** High tier should have a substantially higher actual miss rate
than Low. If the tiers don't separate, the model has no real signal — we'd need
better features.
```

- [ ] **Step 3: Section 10 — Save artifacts (markdown + code)**

Markdown:
```markdown
## 9. Save the model

We save the trained forest **and** the cutoff thresholds, so the app uses
exactly the same tier logic you saw here.
```

Code:
```python
import joblib, os
os.makedirs("../models", exist_ok=True)
artifact = {
    "model": rf,
    "feature_columns": list(features.columns),
    "threshold_low_med": float(q70),
    "threshold_med_high": float(q90),
}
joblib.dump(artifact, "../models/noshow_rf.pkl")
print("Saved noshow_rf.pkl")
```

- [ ] **Step 4: Execute end-to-end and verify**

```bash
jupyter nbconvert --to notebook --execute ml/notebooks/02_no_show_prediction.ipynb --inplace
python -c "import joblib; a = joblib.load('ml/models/noshow_rf.pkl'); print(a.keys()); print('cuts:', a['threshold_low_med'], a['threshold_med_high'])"
```

Expected: dict-like keys printed, two threshold floats.

- [ ] **Step 5: Commit**

```bash
git add ml/notebooks/02_no_show_prediction.ipynb ml/models/noshow_rf.pkl
git commit -m "feat(ml): notebook 2 sections 8-10 (RF, thresholds, save)"
```

---

## Task 10: Build `utils/ml_inference.py`

**Files:**
- Create: `utils/ml_inference.py`

- [ ] **Step 1: Write `utils/ml_inference.py`**

```python
"""Bridge between trained ML artifacts in ml/models/ and the Streamlit app.

Two public functions:
  - get_demand_forecast() -> DataFrame with (court_id, day_of_week, hour, predicted_bookings)
  - predict_noshow_risk(booking) -> ("Low"|"Medium"|"High", probability)
"""
from __future__ import annotations
import os
import pandas as pd
import streamlit as st
import joblib

ML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ml", "models")
DEMAND_PARQUET = os.path.join(ML_DIR, "demand_predictions.parquet")
NOSHOW_PKL = os.path.join(ML_DIR, "noshow_rf.pkl")


@st.cache_data(show_spinner=False)
def get_demand_forecast() -> pd.DataFrame:
    """Return precomputed 7-day forecast. Empty DataFrame if artifact is missing."""
    if not os.path.exists(DEMAND_PARQUET):
        return pd.DataFrame(columns=["court_id","day_of_week","hour","predicted_bookings"])
    return pd.read_parquet(DEMAND_PARQUET)


@st.cache_resource(show_spinner=False)
def _load_noshow_artifact():
    if not os.path.exists(NOSHOW_PKL):
        return None
    return joblib.load(NOSHOW_PKL)


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
    encoded = pd.get_dummies(df, columns=["sport","district","weather"], drop_first=True)
    encoded = encoded.reindex(columns=art["feature_columns"], fill_value=0)
    p = float(art["model"].predict_proba(encoded)[0, 1])

    if p < art["threshold_low_med"]:
        tier = "Low"
    elif p < art["threshold_med_high"]:
        tier = "Medium"
    else:
        tier = "High"
    return tier, p
```

- [ ] **Step 2: Smoke test from the command line**

```bash
python -c "
from utils.ml_inference import get_demand_forecast, predict_noshow_risk
print('forecast shape:', get_demand_forecast().shape)
print('risk:', predict_noshow_risk({'lead_time_days': 20, 'is_repeat_customer': False, 'price': 450}))
"
```

Expected: forecast shape non-zero; risk prints a tier and a probability between 0 and 1.

- [ ] **Step 3: Commit**

```bash
git add utils/ml_inference.py
git commit -m "feat(ml): inference bridge for app-side predictions"
```

---

## Task 11: Wire demand forecast into `pages/owner/ai_insights.py`

**Files:**
- Modify: `pages/owner/ai_insights.py`

- [ ] **Step 1: Read the current file** to confirm line ranges before editing

```bash
sed -n '1,80p' pages/owner/ai_insights.py
```

- [ ] **Step 2: Replace the dummy gradient heatmap with a Plotly heatmap**

Locate the block that begins with `<div style="height:200px;background:radial-gradient(...)">...</div>` (currently around lines 53–58). Replace that single placeholder div with a Plotly heatmap rendered via `st.plotly_chart`.

Add at the top of the file (with other imports):
```python
import plotly.express as px
from utils.ml_inference import get_demand_forecast
```

Inside `render()`, before the existing `st.markdown` block that renders the heatmap card, build the figure:

```python
forecast = get_demand_forecast()
if not forecast.empty:
    pivot = (forecast.groupby(["day_of_week","hour"])["predicted_bookings"]
                     .mean().reset_index()
                     .pivot(index="day_of_week", columns="hour", values="predicted_bookings"))
    dow_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    pivot.index = [dow_labels[i] for i in pivot.index]
    fig = px.imshow(
        pivot, color_continuous_scale=["#F2F9EE","#CFFC00","#506300"],
        aspect="auto", labels=dict(x="Hour", y="Day", color="Predicted bookings"),
    )
    fig.update_layout(height=240, margin=dict(l=0, r=0, t=10, b=0))
```

Then in the existing card, replace the gradient `<div>` with:

```python
st.markdown('<div class="zpots-card" style="padding:20px;">', unsafe_allow_html=True)
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
    <div>
        <h3 class="display" style="font-size:16px;">Bangkok Demand Heatmap</h3>
        <div class="eyebrow" style="margin-top:2px;">7-DAY FORECAST · MODEL: RANDOM FOREST</div>
    </div>
</div>
""", unsafe_allow_html=True)
if not forecast.empty:
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Demand forecast not available — run notebook 01 to generate predictions.")
st.markdown('</div>', unsafe_allow_html=True)
```

(Remove the original card markup that contained the gradient div. Keep the rest of the page below it untouched.)

- [ ] **Step 3: Run the app and verify**

```bash
streamlit run app.py
```

Navigate: owner login → AI Insights. Confirm the heatmap renders with hour columns and day rows, evening hours visibly hotter than mornings.

- [ ] **Step 4: Commit**

```bash
git add pages/owner/ai_insights.py
git commit -m "feat(ml): real demand-forecast heatmap on AI Insights"
```

---

## Task 12: Wire top-uplift slot into `pages/owner/optimization.py`

**Files:**
- Modify: `pages/owner/optimization.py`

- [ ] **Step 1: Add import**

At the top of the file, add:
```python
from utils.ml_inference import get_demand_forecast
```

- [ ] **Step 2: Compute the headline slot**

Inside `render()`, **before** the existing "LIVE OPPORTUNITY" markdown block, add:

```python
forecast = get_demand_forecast()
if not forecast.empty:
    agg = forecast.groupby(["day_of_week","hour"])["predicted_bookings"].mean().reset_index()
    top = agg.sort_values("predicted_bookings", ascending=False).iloc[0]
    overall_avg = agg["predicted_bookings"].mean()
    uplift_pct = int(round((top["predicted_bookings"] - overall_avg) / max(overall_avg, 1e-6) * 100))
    dow_labels = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    headline_day = dow_labels[int(top["day_of_week"])]
    headline_hour = f"{int(top['hour']):02d}:00"
else:
    headline_day, headline_hour, uplift_pct = "Sunday", "08:00", 20
```

- [ ] **Step 3: Replace the hardcoded headline card**

Find the block with `Adjust availability for<br><span style="color:#506300; font-style:italic;">Sunday Morning</span> to capture<br><span style="color:#506300;">+20%</span> demand.` and rewrite the headline using f-string:

```python
st.markdown(f"""
<div class="zpots-card" style="padding:2rem;">
    <span class="ai-tag" style="margin-bottom:12px;">LIVE OPPORTUNITY</span>
    <h2 style="font-size:1.8rem; line-height:1.15; margin-top:12px;">Open up<br>
        <span style="color:#506300; font-style:italic;">{headline_day} {headline_hour}</span> to capture<br>
        <span style="color:#506300;">+{uplift_pct}%</span> demand.</h2>
    <div style="margin-top:1rem; font-size:20px; color:#506300; font-family:'Space Grotesk'; font-weight:700;">+{uplift_pct}%<br>
        <span style="font-size:12px; font-weight:400; color:#3d4455;">REVENUE LIFT</span></div>
</div>
""", unsafe_allow_html=True)
```

- [ ] **Step 4: Verify in app**

Restart Streamlit, navigate to Owner → Optimization Engine. The headline should reflect the model's top slot (almost certainly an evening hour).

- [ ] **Step 5: Commit**

```bash
git add pages/owner/optimization.py
git commit -m "feat(ml): drive optimization headline from demand forecast"
```

---

## Task 13: Wire no-show risk badge into `pages/owner/booking_dashboard.py`

**Files:**
- Modify: `pages/owner/booking_dashboard.py`
- Modify: `components/css.py` (add a warning pill style)

- [ ] **Step 1: Add a `status-warning` CSS class**

In `components/css.py`, find the cluster of `.status-*` rules (around lines 134–139) and add:

```css
.status-warning  { background: rgba(230,81,0,0.16); color: #c95400; }
```

- [ ] **Step 2: Import the predictor in `booking_dashboard.py`**

Add to imports:
```python
from datetime import datetime
from utils.ml_inference import predict_noshow_risk
```

- [ ] **Step 3: Update the table header** to include a Risk column

Find the header div (currently `grid-template-columns: 2fr 2fr 1fr 0.5fr`). Change to `2fr 2fr 1fr 1fr 0.5fr` and add a `<div>RISK</div>` between STATUS and ACTION:

```python
st.markdown("""
<div style="display:grid; grid-template-columns: 2fr 2fr 1fr 1fr 0.5fr; gap:0; padding:12px 16px; font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.08em; color:#3d4455;">
    <div>CUSTOMER</div><div>SESSION INFO</div><div>STATUS</div><div>RISK</div><div>ACTION</div>
</div>
""", unsafe_allow_html=True)
```

- [ ] **Step 4: Build a feature dict per booking and render the badge**

Replace the existing per-booking loop body (currently around lines 107–125) with:

```python
TIER_TO_CSS = {"Low": "status-active", "Medium": "status-warning", "High": "status-cancelled"}

for booking in all_bookings:
    status_class = f"status-{booking['status'].lower()}"
    # Best-effort feature extraction for the risk model
    sport = booking.get("sport", "Badminton")
    time_str = booking.get("time", "")
    try:
        hour = int(time_str.split(":")[0][-2:])
    except Exception:
        hour = 18
    today = datetime.now()
    feat = {
        "sport": sport,
        "district": "Sukhumvit",
        "day_of_week": today.weekday(),
        "hour": hour,
        "is_weekend": today.weekday() >= 5,
        "is_holiday": False,
        "weather": "sunny",
        "price": 500,
        "lead_time_days": 5,
        "is_repeat_customer": booking.get("status","").upper() == "COMPLETED",
    }
    tier, _prob = predict_noshow_risk(feat)
    risk_class = TIER_TO_CSS[tier]

    st.markdown(f"""
    <div class="zpots-card" style="display:grid; grid-template-columns: 2fr 2fr 1fr 1fr 0.5fr; gap:0; align-items:center; margin-bottom:8px; padding:12px 16px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:36px; height:36px; border-radius:50%; background:{booking['avatar_color']}; color:white; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600;">{booking['customer'][0]}</div>
            <div>
                <div style="font-family:'Inter'; font-weight:600; font-size:14px;">{booking['customer']}</div>
                <div style="font-size:11px; color:#3d4455;">Member ID: {booking['member_id']}</div>
            </div>
        </div>
        <div>
            <div style="font-size:13px;">🏟 {booking['court']} • {booking['sport']}</div>
            <div style="font-size:12px; color:#3d4455;">🕐 {booking['time']}</div>
        </div>
        <div><span class="status-badge {status_class}">{booking['status']}</span></div>
        <div><span class="status-badge {risk_class}">{tier}</span></div>
        <div style="text-align:center; cursor:pointer; font-size:18px;">⋮</div>
    </div>
    """, unsafe_allow_html=True)
```

- [ ] **Step 5: Verify in app**

Restart Streamlit, log in as owner, go to Bookings → Today tab. Each booking row should now have a Low / Medium / High pill in a new column. At least one of each tier should appear across the visible rows.

- [ ] **Step 6: Commit**

```bash
git add components/css.py pages/owner/booking_dashboard.py
git commit -m "feat(ml): no-show risk badges on booking dashboard"
```

---

## Task 14: End-to-end smoke test & wrap-up

**Files:**
- (no edits — verification only)

- [ ] **Step 1: Reset and regenerate everything from scratch**

```bash
rm -f ml/data/bookings.csv ml/data/bookings_labeled.csv
rm -f ml/models/demand_rf.pkl ml/models/demand_predictions.parquet ml/models/noshow_rf.pkl
python ml/data/generate_bookings.py
jupyter nbconvert --to notebook --execute ml/notebooks/01_demand_forecasting.ipynb --inplace
jupyter nbconvert --to notebook --execute ml/notebooks/02_no_show_prediction.ipynb --inplace
```

Expected: all four artifacts in `ml/models/` exist; notebooks executed without errors.

- [ ] **Step 2: Run the app and walk every integration point**

```bash
streamlit run app.py
```

Verify in order:
1. Owner → AI Insights → heatmap renders with evening peak.
2. Owner → Optimization Engine → headline slot is an evening hour with a positive uplift %.
3. Owner → Bookings → at least one of each Low / Medium / High pill is visible.

- [ ] **Step 3: Final commit (only if any artifact changed)**

```bash
git status
# If artifacts changed:
git add ml/notebooks/ ml/models/ ml/data/
git commit -m "chore(ml): regenerate artifacts end-to-end"
```

---

## Done

- [ ] All 14 tasks complete.
- [ ] App walkthrough confirms: real heatmap, model-driven optimization headline, risk badges per booking.
- [ ] Both notebooks open in Jupyter and run end-to-end with their teaching narrative intact.
