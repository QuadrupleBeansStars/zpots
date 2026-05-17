// Mirrors apps/api/schemas/ai.py
export type ParseSearchRequest = { query: string };
export type ParseSearchResponse = {
  sport: string | null;
  district: string | null;
  time_of_day: 'morning' | 'afternoon' | 'evening' | null;
  max_price: number | null;
};

export type InsightsRequest = {
  weekly_utilization: Record<string, number>;
  district_demand: { name: string; demand: number; level: string }[];
  owner_bookings: { customer: string; sport: string; status: string }[];
};
export type InsightsResponse = { markdown: string };

export type CourtDescriptionRequest = {
  name: string;
  sport: string;
  surface: string;
  location: string;
  amenities: string[];
};
export type CourtDescriptionResponse = { description: string };

// Mirrors apps/api/schemas/ml.py
export type DemandCell = {
  court_id: string;
  day_of_week: number;
  hour: number;
  predicted_bookings: number;
};
export type DemandForecastResponse = { cells: DemandCell[] };

export type NoShowRiskItem = {
  sport?: string;
  district?: string;
  day_of_week?: number;
  hour?: number;
  is_weekend?: boolean;
  is_holiday?: boolean;
  weather?: string;
  price?: number;
  lead_time_days?: number;
  is_repeat_customer?: boolean;
};
export type NoShowRiskResult = {
  tier: 'Low' | 'Medium' | 'High';
  probability: number;
};
export type NoShowRiskBatchRequest = { items: NoShowRiskItem[] };
export type NoShowRiskBatchResponse = { results: NoShowRiskResult[] };
