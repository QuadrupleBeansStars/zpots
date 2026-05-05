"""
Builder script: creates ml/notebooks/01_demand_forecasting.ipynb
Run with: conda run -n MADT python ml/notebooks/_build_nb1.py
"""
import nbformat
from pathlib import Path

nb = nbformat.v4.new_notebook()
nb.metadata["kernelspec"] = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}
nb.metadata["language_info"] = {
    "name": "python",
    "version": "3.10.0",
}

cells = []

# ── Section 1: Title & framing ────────────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
# Demand Forecasting for ZPOTS

**Goal:** predict how many bookings a court will receive in a given hour, so the owner dashboard can show a 7-day demand heatmap.

**Why this matters:** if we know which slots will be hot, owners can:
- raise prices on peak slots
- run promotions on dead slots
- spot demand surges before the customer feels them

**The ML task:** *time-series regression* — input = features describing a court-hour, output = a number (predicted bookings).\
"""))

# ── Section 2: Load & peek ────────────────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 1. Load the data

Each row is one (court, hour) over the last 12 weeks.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("../data/bookings.csv", parse_dates=["timestamp"])
print(f"Rows: {len(df):,}")
df.head()\
"""))

cells.append(nbformat.v4.new_code_cell("""\
df.describe(include="all").T\
"""))

# ── Section 3: Visualize patterns ────────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 2. What does the data look like?

Before any modeling, **always look at the data**. We're hunting for patterns
the model will need to learn — and for surprises.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
hourly = df.groupby("hour")["bookings"].mean()
hourly.plot(kind="bar", figsize=(8,3), title="Average bookings by hour of day")
plt.ylabel("avg bookings"); plt.xlabel("hour"); plt.show()\
"""))

cells.append(nbformat.v4.new_code_cell("""\
dow_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
daily = df.groupby("day_of_week")["bookings"].mean()
daily.index = dow_labels
daily.plot(kind="bar", figsize=(6,3), title="Average bookings by day of week", color="#506300")
plt.show()\
"""))

cells.append(nbformat.v4.new_code_cell("""\
df.groupby(["sport","weather"])["bookings"].mean().unstack().plot(
    kind="bar", figsize=(8,3), title="Bookings by sport × weather"
)
plt.ylabel("avg bookings"); plt.show()\
"""))

cells.append(nbformat.v4.new_markdown_cell("""\
**What we see:**
- Big evening peak (18–21h)
- Weekends slightly lower on average (the *evening peak* is what drives demand, not the day)
- Football and Basketball drop hard on rainy days — **weather matters for outdoor sports**

These are exactly the patterns we expect a model to capture.\
"""))

# ── Section 4: Feature engineering ───────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 3. Feature engineering

A model can't read words like "Sunday" or "rainy". We need numbers.

**One-hot encoding** turns one categorical column into many 0/1 columns —
one per category. We use `pd.get_dummies` for this.

We also add **lag features**: "how many bookings did this same court see at this hour *yesterday*?"
For time series, the recent past is often the strongest predictor.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
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
features.head()\
"""))

# ── Section 5: Train/test split ───────────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 4. Train/test split

For most ML problems we shuffle the data and split randomly. **Not for time series.**
If we randomly mix past and future rows, the model "cheats" — it learns from
tomorrow to predict today. That looks great in evaluation and fails in production.

We split **chronologically**: first 80% of time → train, last 20% → test.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
split_idx = int(len(df) * 0.80)
X_train, X_test = features.iloc[:split_idx], features.iloc[split_idx:]
y_train, y_test = target.iloc[:split_idx], target.iloc[split_idx:]

print(f"Train: {len(X_train):,} rows, Test: {len(X_test):,} rows")
print(f"Train period: {df['timestamp'].iloc[0]} → {df['timestamp'].iloc[split_idx-1]}")
print(f"Test  period: {df['timestamp'].iloc[split_idx]} → {df['timestamp'].iloc[-1]}")\
"""))

# ── Section 6: Linear Regression baseline ────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 5. Baseline model: Linear Regression

**Always start with a simple model.** It gives you a yardstick for whether
fancier models are actually helping, and it's easy to debug.

Linear Regression assumes the answer is a weighted sum of the features:
`bookings ≈ w1·feature1 + w2·feature2 + ...`. Simple, fast, very interpretable.

We measure error with:
- **MAE** (Mean Absolute Error): "on average we're off by this many bookings"
- **RMSE** (Root Mean Squared Error): like MAE but penalizes big misses harder\
"""))

cells.append(nbformat.v4.new_code_cell("""\
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

lin = LinearRegression()
lin.fit(X_train, y_train)
pred_lin = lin.predict(X_test)

mae = mean_absolute_error(y_test, pred_lin)
rmse = root_mean_squared_error(y_test, pred_lin)
print(f"Linear  MAE: {mae:.3f}   RMSE: {rmse:.3f}")\
"""))

cells.append(nbformat.v4.new_code_cell("""\
plt.figure(figsize=(5,5))
plt.scatter(y_test, pred_lin, alpha=0.2, s=8)
plt.plot([0, y_test.max()], [0, y_test.max()], "r--", label="perfect")
plt.xlabel("actual bookings"); plt.ylabel("predicted bookings")
plt.title("Linear Regression: predicted vs actual"); plt.legend(); plt.show()\
"""))

# ── Section 7: Residual analysis ─────────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 6. Where does the linear model fail?

A **residual** is `actual − predicted`. Plotting residuals by hour shows us
*when* the model is wrong, not just *how much*.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
test_df = df.iloc[split_idx:].copy()
test_df["pred"] = pred_lin
test_df["residual"] = test_df["bookings"] - test_df["pred"]

test_df.groupby("hour")["residual"].mean().plot(
    kind="bar", figsize=(8,3), title="Avg residual by hour (positive = under-predicted)"
)
plt.axhline(0, color="black", lw=0.8); plt.show()\
"""))

cells.append(nbformat.v4.new_markdown_cell("""\
The linear model **systematically under-predicts** the evening peak. Linear models
can't easily capture interactions like "evening AND weekend AND not rainy".
We need a model that handles non-linear feature interactions automatically.\
"""))

# ── Section 8: Random Forest Regressor ───────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 7. Upgrade: Random Forest

A **Random Forest** is a collection of decision trees. Each tree learns a different
set of "if-then" rules; the forest averages their predictions. This naturally
captures interactions like "evening AND weekend".

`n_estimators=200` means 200 trees. More = better up to a point, slower to train.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)

mae_rf = mean_absolute_error(y_test, pred_rf)
rmse_rf = root_mean_squared_error(y_test, pred_rf)
print(f"Linear  MAE: {mae:.3f}   RMSE: {rmse:.3f}")
print(f"Forest  MAE: {mae_rf:.3f}   RMSE: {rmse_rf:.3f}")\
"""))

# ── Section 9: Feature importance ────────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 8. Which features matter?

Random Forests can tell us which features drove the prediction. If we trained
a model and the most important feature was random noise, we'd know something
was wrong.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
importances = pd.Series(rf.feature_importances_, index=features.columns)
top = importances.sort_values(ascending=True).tail(15)
top.plot(kind="barh", figsize=(7,5), title="Top 15 feature importances", color="#506300")
plt.show()\
"""))

cells.append(nbformat.v4.new_markdown_cell("""\
**Sanity check:** `hour`, `bookings_lag_24h`, and `day_of_week` should dominate.
If `is_holiday` (which we made very sparse) ranked first, the model probably overfit.\
"""))

## Section 9: Feature importance (already above) ends here

# ── Section 10: Forecast generation + save artifacts ─────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 9. Generate next week's forecast

We build a synthetic feature matrix for the next 7 days × 24 hours × every court,
predict, and save to `demand_predictions.parquet`. The Streamlit app reads this
file directly — no model loading needed for the heatmap.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
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
                "weather": "sunny",
                "price": int(price),
                "n_courts": max(1, len(court.get("courts", [{"a":1}]))),
                "bookings_lag_24h": 0,
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
out.head()\
"""))

cells.append(nbformat.v4.new_markdown_cell("""\
**Quick sanity check:** average predicted bookings by hour should still show
the evening peak. If it's flat, something went wrong with feature alignment.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
out.groupby("hour")["predicted_bookings"].mean().plot(
    kind="bar", figsize=(8,3), title="Forecast: avg predicted bookings by hour"
)
plt.show()\
"""))

nb.cells = cells

out_path = Path(__file__).parent / "01_demand_forecasting.ipynb"
with open(out_path, "w") as f:
    nbformat.write(nb, f)

print(f"Notebook written to: {out_path}")
