from fastapi import APIRouter

from ml.inference import get_demand_forecast, predict_noshow_risk
from schemas.ml import (
    DemandCell,
    DemandForecastResponse,
    NoShowRiskBatchRequest,
    NoShowRiskBatchResponse,
    NoShowRiskResult,
)

router = APIRouter(prefix="/ml", tags=["ml"])


@router.get("/demand-forecast", response_model=DemandForecastResponse)
def demand_forecast() -> DemandForecastResponse:
    df = get_demand_forecast()
    cells = [
        DemandCell(
            court_id=str(row["court_id"]),
            day_of_week=int(row["day_of_week"]),
            hour=int(row["hour"]),
            predicted_bookings=float(row["predicted_bookings"]),
        )
        for _, row in df.iterrows()
    ]
    return DemandForecastResponse(cells=cells)


@router.post("/noshow-risk/batch", response_model=NoShowRiskBatchResponse)
def noshow_risk_batch(req: NoShowRiskBatchRequest) -> NoShowRiskBatchResponse:
    results = []
    for item in req.items:
        tier, probability = predict_noshow_risk(item.model_dump())
        results.append(NoShowRiskResult(tier=tier, probability=probability))
    return NoShowRiskBatchResponse(results=results)
