"""
Builder script: creates ml/notebooks/02_no_show_prediction.ipynb
Run with: conda run -n MADT python ml/notebooks/_build_nb2.py
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
# No-Show / Cancellation Prediction

**Goal:** for each booking, predict the probability that the customer won't show up.
Owners use this to flag risky bookings so they can confirm with the customer or
oversell the slot.

**The ML task:** *binary classification* — input = booking features, output = 0 (will show) or 1 (won't).\
"""))

# ── Section 2: Load & class balance ──────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 1. Load the data and check class balance

In classification, we always check **how rare each class is**. If only 8% of
bookings are no-shows, a dumb model that always predicts "will show" gets 92%
accuracy — and is useless. **Class imbalance changes how we measure success.**\
"""))

cells.append(nbformat.v4.new_code_cell("""\
import pandas as pd, numpy as np, matplotlib.pyplot as plt
df = pd.read_csv("../data/bookings_labeled.csv", parse_dates=["timestamp"])
print(f"Rows: {len(df):,}")
print(df["status"].value_counts(normalize=True).round(3))

# Treat both no_show and cancelled as "missed" (positive class)
df["is_missed"] = df["status"].isin(["no_show","cancelled"]).astype(int)
print(f"\\nMissed rate: {df['is_missed'].mean():.1%}")
df.head()\
"""))

# ── Section 3: Visualize — who no-shows? ─────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 2. Visualize: who no-shows?

Looking at the miss rate broken down by each feature tells us which signals
the model will likely use.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
df.groupby(pd.cut(df["lead_time_days"], bins=[-1,3,7,14,30]))["is_missed"].mean().plot(
    kind="bar", figsize=(6,3), title="Miss rate by lead time"
)
plt.ylabel("miss rate"); plt.show()\
"""))

cells.append(nbformat.v4.new_code_cell("""\
df.groupby("is_repeat_customer")["is_missed"].mean().plot(
    kind="bar", figsize=(4,3), title="Miss rate: repeat vs new customer", color="#506300"
)
plt.show()\
"""))

cells.append(nbformat.v4.new_code_cell("""\
df.groupby(pd.cut(df["price"], bins=[0,400,700,2000]))["is_missed"].mean().plot(
    kind="bar", figsize=(5,3), title="Miss rate by price band"
)
plt.show()\
"""))

cells.append(nbformat.v4.new_markdown_cell("""\
**Pattern check:** miss rate should rise with longer lead time and drop for
repeat customers. Those are the signals we baked into the data — confirming
the model has something real to learn.\
"""))

# ── Section 4: Feature engineering ───────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 3. Feature engineering

Same idea as Notebook 1 — turn categoricals into 0/1 columns.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
features = pd.get_dummies(
    df[["sport","district","day_of_week","hour","is_weekend","is_holiday",
        "weather","price","lead_time_days","is_repeat_customer"]],
    columns=["sport","district","weather"],
    drop_first=True,
)
target = df["is_missed"]
print("Feature matrix:", features.shape)
features.head()\
"""))

# ── Section 5: Stratified split ───────────────────────────────────────────────
cells.append(nbformat.v4.new_markdown_cell("""\
## 4. Train/test split — stratified

Because the positive class is rare, a random split could land most of the
no-shows in either train or test by chance. **Stratified split** preserves the
class ratio in both halves.\
"""))

cells.append(nbformat.v4.new_code_cell("""\
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42, stratify=target
)
print(f"Train miss rate: {y_train.mean():.3f}   Test miss rate: {y_test.mean():.3f}")\
"""))

# ── Assemble & write ──────────────────────────────────────────────────────────
nb.cells = cells

out_path = Path(__file__).parent / "02_no_show_prediction.ipynb"
with open(out_path, "w") as f:
    nbformat.write(nb, f)

print(f"Notebook written to: {out_path}")
