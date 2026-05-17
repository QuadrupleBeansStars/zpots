import type {
  CourtDescriptionRequest, CourtDescriptionResponse,
  DemandForecastResponse,
  InsightsRequest, InsightsResponse,
  NoShowRiskBatchRequest, NoShowRiskBatchResponse,
  ParseSearchRequest, ParseSearchResponse,
} from './api-types';

async function postJson<TReq, TRes>(path: string, body: TReq): Promise<TRes> {
  const res = await fetch(`/api/${path}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST /api/${path} failed: ${res.status}`);
  return res.json();
}

async function getJson<TRes>(path: string): Promise<TRes> {
  const res = await fetch(`/api/${path}`);
  if (!res.ok) throw new Error(`GET /api/${path} failed: ${res.status}`);
  return res.json();
}

export const aiParseSearch = (req: ParseSearchRequest) =>
  postJson<ParseSearchRequest, ParseSearchResponse>('ai/parse-search', req);

export const aiInsights = (req: InsightsRequest) =>
  postJson<InsightsRequest, InsightsResponse>('ai/insights', req);

export const aiCourtDescription = (req: CourtDescriptionRequest) =>
  postJson<CourtDescriptionRequest, CourtDescriptionResponse>('ai/court-description', req);

export const mlDemandForecast = () =>
  getJson<DemandForecastResponse>('ml/demand-forecast');

export const mlNoshowRiskBatch = (req: NoShowRiskBatchRequest) =>
  postJson<NoShowRiskBatchRequest, NoShowRiskBatchResponse>('ml/noshow-risk/batch', req);
