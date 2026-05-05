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
