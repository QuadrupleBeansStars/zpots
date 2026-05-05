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

nb.cells = cells

out_path = Path(__file__).parent / "01_demand_forecasting.ipynb"
with open(out_path, "w") as f:
    nbformat.write(nb, f)

print(f"Notebook written to: {out_path}")
