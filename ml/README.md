# ZPOTS ML

Self-contained ML workspace. The Streamlit app consumes only the artifacts in `ml/models/`.

## Layout

- `data/generate_bookings.py` — synthetic data generator
- `data/bookings.csv` — hourly per-court booking history (target = `bookings`)
- `data/bookings_labeled.csv` — booked rows with no-show labels
- `notebooks/01_demand_forecasting.ipynb` — beginner walkthrough → trains `demand_rf.pkl` and writes `demand_predictions.parquet`
- `notebooks/02_no_show_prediction.ipynb` — beginner walkthrough → trains `noshow_rf.pkl`
- `models/` — saved artifacts loaded by the app

## Regenerate everything (run inside conda env MADT)

```bash
conda activate MADT
python ml/data/generate_bookings.py
jupyter nbconvert --to notebook --execute ml/notebooks/01_demand_forecasting.ipynb --inplace
jupyter nbconvert --to notebook --execute ml/notebooks/02_no_show_prediction.ipynb --inplace
```

## Model performance

Numbers below are from the most recent training run on the synthetic dataset
(seed 42, 12 weeks of hourly data across all courts in `data/dummy_data.py::COURTS`).
Re-run the notebooks to refresh.

### 1. Demand forecasting — regression

The target is the number of bookings per court-hour, so we report error rather
than accuracy.

| Model                          | MAE   | RMSE  |
| ------------------------------ | ----- | ----- |
| Linear Regression (baseline)   | 1.167 | 1.376 |
| **Random Forest (shipped)**    | **0.570** | **0.703** |

- Train/test split is **chronological** 80/20 (~6,052 train / ~1,514 test rows).
- Top feature importances: `hour` (0.46), `n_courts` (0.21), `day_of_week` (0.09),
  `bookings_lag_24h` (0.06).
- Sanity check: predicted bookings for hour 19 are ~3× hour 8, matching the
  evening-peak pattern in the data.

### 2. No-show prediction — binary classification

Class balance: ~25.7% positive (no_show + cancelled). Plain accuracy is
misleading here, so we report ROC AUC and per-tier miss rates.

| Model                              | ROC AUC |
| ---------------------------------- | ------- |
| Logistic Regression (baseline)     | 0.600   |
| **Random Forest (shipped)**        | **0.587** |

The shipped artifact ships **probability-quantile thresholds** (Low/Med/High)
so the UI shows tiers instead of raw probabilities:

| Tier   | Predicted slice | Actual miss rate on test set |
| ------ | --------------- | ---------------------------- |
| Low    | bottom 70%      | 22.9% |
| Medium | next 20%        | 29.9% |
| High   | top 10%         | 36.2% |

Tiers are monotonic — High is ~1.6× Low — which is the property the booking
dashboard relies on.

### Caveats

- All numbers are on **synthetic data**. Real-world AUC will differ.
- The no-show signal is intentionally weak (AUC ~0.59). On real data we'd want
  ≥0.70 before trusting it for automated decisions like overbooking.
- The demand model's MAE of 0.57 bookings/hour against typical 0–4 bookings/hour
  is roughly a 14% relative error — fine for a heatmap, not for revenue forecasting.
