# ZPOTS

Sports court booking platform built with Streamlit. Two user roles — players (search, book, check in, leave feedback) and venue owners (manage courts, slots, pricing, view bookings, ML-driven insights).

## Quick start

This project uses the conda env **`MADT`**.

```bash
conda activate MADT
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

## Project layout

```
.
├── app.py                # entry point, page router
├── components/           # shared UI (CSS, navigation)
├── data/                 # dummy data + SQLite database
├── pages/
│   ├── player/           # login, home, search, court_details, booking,
│   │                     # confirmation, my_bookings, checkin, feedback
│   └── owner/            # login, dashboard, manage_courts, add_edit_court,
│                         # manage_slots, pricing, booking_dashboard,
│                         # ai_insights, optimization
├── utils/
│   └── ml_inference.py   # bridge: trained ML artifacts → app
├── ml/                   # self-contained ML workspace (see ml/README.md)
└── docs/superpowers/     # design specs and implementation plans
```

## Features

### Player
- Search and filter courts by sport, district, price
- Book a slot with QR-code check-in flow
- View past and upcoming bookings, leave feedback

### Owner
- Manage courts, slots, and pricing
- Booking dashboard with revenue tracking and **ML-driven no-show risk badges**
- AI Insights page with **Random Forest demand forecast heatmap** (7-day, hourly)
- Optimization Engine with **model-driven top-uplift slot recommendation**

## Machine learning

Two traditional ML models ship with the app, trained on a synthetic dataset and consumed via `utils/ml_inference.py`.

| Model | Algorithm | Used by | Test metric |
|---|---|---|---|
| Demand forecasting | Random Forest Regressor | AI Insights heatmap, Optimization headline | MAE 0.57 (vs 1.17 linear baseline) |
| No-show prediction | Random Forest Classifier | Booking Dashboard risk pills | ROC AUC 0.59; tier miss rates Low 23% / Med 30% / High 36% |

Beginner-friendly Jupyter notebooks walk through both pipelines end-to-end (load → EDA → features → split → baseline → upgrade → save). See `ml/README.md` for full details, regeneration commands, and model caveats.

```bash
# Regenerate data + retrain both models
conda activate MADT
python ml/data/generate_bookings.py
jupyter nbconvert --to notebook --execute ml/notebooks/01_demand_forecasting.ipynb --inplace
jupyter nbconvert --to notebook --execute ml/notebooks/02_no_show_prediction.ipynb --inplace
```

## Tech stack

- **Streamlit** UI, custom CSS in `components/css.py`
- **Plotly** charts (heatmap, dashboards)
- **scikit-learn** for ML models, **joblib** for persistence
- **pandas / numpy / pyarrow** for data
- **Anthropic Claude (Opus 4.7)** for LLM-generated AI summaries on the insights page
- **SQLite** via `data/database.py` for booking persistence

## Documentation

- `ml/README.md` — ML workspace, model performance, regeneration steps
- `docs/superpowers/specs/` — design specs
- `docs/superpowers/plans/` — implementation plans
