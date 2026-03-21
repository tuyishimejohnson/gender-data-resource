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

export interface GenderMetric {
  Female: number;
  Male: number;
}

export interface CoreMetricsDataPoint {
  year: number;
  employment_rate: GenderMetric;
  unemployment_rate: GenderMetric;
  lfpr: GenderMetric;
}

export interface CoreMetricsData {
  data: CoreMetricsDataPoint[];
}

export interface BoxPlotStats {
  min: number;
  q1: number;
  median: number;
  q3: number;
  max: number;
  mean: number;
}

export interface AverageIncomeData {
  year: number;
  data: {
    Female: BoxPlotStats;
    Male: BoxPlotStats;
  };
}

export interface IncomeDistributionData {
  year: number;
  brackets: number[];
  data: {
    Female: number[];
    Male: number[];
  };
}

export interface HourlyWageData {
  year: number;
  data: {
    Female: BoxPlotStats;
    Male: BoxPlotStats;
  };
}

export interface SectorEmploymentPoint {
  sector: string;
  Female: number;
  Male: number;
  female_percentage: number;
  male_percentage: number;
}

export interface SectorEmploymentData {
  year: number;
  data: SectorEmploymentPoint[];
}

export interface FormalInformalPoint {
  category: string;
  Female: number;
  Male: number;
  female_percentage: number;
  male_percentage: number;
}

export interface FormalInformalData {
  year: number;
  data: FormalInformalPoint[];
}

export interface OccupationPoint {
  code: number;
  occupation: string;
  Female: number;
  Male: number;
  female_percentage: number;
  male_percentage: number;
  total: number;
}

export interface OccupationSegregationData {
  year: number;
  data: OccupationPoint[];
}

export interface ProvinceEmploymentPoint {
  province: string;
  code: number;
  Female: number;
  Male: number;
  gap: number;
  female_employed: number;
  male_employed: number;
}

export interface ProvinceEmploymentData {
  year: number;
  data: ProvinceEmploymentPoint[];
}

export interface UrbanRuralPoint {
  area: string;
  Female: number;
  Male: number;
  gap: number;
  female_employed: number;
  male_employed: number;
  female_total: number;
  male_total: number;
}

export interface UrbanRuralData {
  year: number;
  data: UrbanRuralPoint[];
}
