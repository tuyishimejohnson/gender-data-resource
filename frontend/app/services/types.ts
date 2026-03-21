// Dashboard API Types
export interface KPIData {
  avg_gender_gap: number;
  female_avg: number;
  male_avg: number;
  regions_tracked: number;
  year: number;
  indicator: string;
}

export interface TrendDataPoint {
  year: number;
  gap: number;
  segment: "Historical" | "Forecast";
}

export interface TrendData {
  data: TrendDataPoint[];
}

export interface TimeseriesDataPoint {
  year: number;
  Female: number;
  Male: number;
}

export interface TimeseriesData {
  data: TimeseriesDataPoint[];
}

export interface RegionalDataPoint {
  region: string;
  gap: number;
}

export interface RegionalData {
  data: RegionalDataPoint[];
  year: number;
}

export interface IndicatorRow {
  INDICATOR: string;
  FEMALE: string;
  MALE: string;
  GAP: string;
  STATUS: string;
}

export interface IndicatorsData {
  data: IndicatorRow[];
  year: number;
}
