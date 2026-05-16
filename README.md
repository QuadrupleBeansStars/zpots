# ZPOTS

Sports court booking platform — currently mid-migration from Streamlit to Next.js 14 + FastAPI. **Both stacks run side-by-side** during the migration: Streamlit stays at the repo root (fully runnable, no reconfig needed), Next.js lives at `apps/web/`.

Two user roles — players (search, book, check in, leave feedback) and venue owners (manage courts, slots, pricing, view bookings, ML-driven insights).

## Quick start

### Streamlit (current production, always runnable)

This project uses the conda env **`MADT`**.

```bash
conda activate MADT
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

### Next.js (in progress — Phase 1+)

```bash
cd apps/web
pnpm install
pnpm dev          # http://localhost:3000
pnpm test         # Playwright smoke
pnpm build        # production build
```

Requires Node 20+ and `pnpm` (install with `npm install -g pnpm` if missing).

## Migration progress

See `docs/superpowers/specs/2026-05-16-nextjs-migration-design.md` for the overall plan and `docs/superpowers/plans/2026-05-16-phase1-nextjs-scaffold.md` for Phase 1 (scaffold + landing page).

## Project layout

```
.
├── apps/
│   └── web/              # Next.js 14 app (in progress)
├── app.py                # Streamlit entry point, page router
├── components/           # Streamlit shared UI (CSS, navigation)
├── data/                 # dummy data + SQLite database
├── pages/
│   ├── player/           # Streamlit player pages — login, home, search, court_details,
│   │                     # booking, confirmation, my_bookings, checkin, feedback
│   └── owner/            # Streamlit owner pages — login, dashboard, manage_courts,
│                         # add_edit_court, manage_slots, pricing, booking_dashboard,
│                         # ai_insights, optimization
├── agents/               # Streamlit chat agents (player + owner)
├── handoff/              # design system + reference TSX components (for Next.js work)
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
- **OpenAI / Azure OpenAI** for LLM-generated AI summaries, search-query parsing, and the player + owner chat agents (single client in `agents/llm_client.py`)
- **SQLite** via `data/database.py` for booking persistence

## Documentation

- `ml/README.md` — ML workspace, model performance, regeneration steps
- `docs/superpowers/specs/` — design specs
- `docs/superpowers/plans/` — implementation plans
