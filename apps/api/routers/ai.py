from fastapi import APIRouter

from ai.helpers import (
    generate_ai_insights,
    generate_court_description,
    parse_search_query,
)
from schemas.ai import (
    CourtDescriptionRequest,
    CourtDescriptionResponse,
    InsightsRequest,
    InsightsResponse,
    ParseSearchRequest,
    ParseSearchResponse,
)

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/parse-search", response_model=ParseSearchResponse)
def parse_search(req: ParseSearchRequest) -> ParseSearchResponse:
    parsed = parse_search_query(req.query)
    return ParseSearchResponse(**parsed)


@router.post("/insights", response_model=InsightsResponse)
def insights(req: InsightsRequest) -> InsightsResponse:
    markdown = generate_ai_insights(
        req.weekly_utilization, req.district_demand, req.owner_bookings,
    )
    return InsightsResponse(markdown=markdown)


@router.post("/court-description", response_model=CourtDescriptionResponse)
def court_description(req: CourtDescriptionRequest) -> CourtDescriptionResponse:
    text = generate_court_description(
        req.name, req.sport, req.surface, req.location, req.amenities,
    )
    return CourtDescriptionResponse(description=text)
