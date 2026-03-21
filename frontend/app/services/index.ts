import axios from "axios";
import type {
  KPIData,
  TrendData,
  TimeseriesData,
  RegionalData,
  IndicatorsData,
  CoreMetricsData,
  AverageIncomeData,
  IncomeDistributionData,
  HourlyWageData,
  SectorEmploymentData,
  FormalInformalData,
  OccupationSegregationData,
  ProvinceEmploymentData,
  UrbanRuralData,
} from "./types";

export const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Re-export types
export type {
  KPIData,
  TrendData,
  TimeseriesData,
  RegionalData,
  IndicatorsData,
  CoreMetricsData,
  AverageIncomeData,
  IncomeDistributionData,
  HourlyWageData,
  SectorEmploymentData,
  FormalInformalData,
  OccupationSegregationData,
  ProvinceEmploymentData,
  UrbanRuralData,
} from "./types";

// Dashboard API Functions
export const dashboardApi = {
  getKPIs: async (year: number = 2023): Promise<KPIData> => {
    const response = await api.get(`/dashboard/kpis?year=${year}`);
    return response.data;
  },

  getTrend: async (): Promise<TrendData> => {
    const response = await api.get("/dashboard/trend");
    return response.data;
  },

  getTimeseries: async (): Promise<TimeseriesData> => {
    const response = await api.get("/dashboard/timeseries");
    return response.data;
  },

  getRegional: async (year: number = 2023): Promise<RegionalData> => {
    const response = await api.get(`/dashboard/regional?year=${year}`);
    return response.data;
  },

  getIndicators: async (year: number = 2023): Promise<IndicatorsData> => {
    const response = await api.get(`/dashboard/indicators?year=${year}`);
    return response.data;
  },

  getCoreMetrics: async (): Promise<CoreMetricsData> => {
    const response = await api.get("/dashboard/core-metrics");
    return response.data;
  },

  getAverageIncome: async (year: number = 2023): Promise<AverageIncomeData> => {
    const response = await api.get(`/dashboard/income-inequality/average-income?year=${year}`);
    return response.data;
  },

  getIncomeDistribution: async (year: number = 2023): Promise<IncomeDistributionData> => {
    const response = await api.get(`/dashboard/income-inequality/income-distribution?year=${year}`);
    return response.data;
  },

  getHourlyWage: async (year: number = 2023): Promise<HourlyWageData> => {
    const response = await api.get(`/dashboard/income-inequality/hourly-wage?year=${year}`);
    return response.data;
  },

  getSectorEmployment: async (year: number = 2023): Promise<SectorEmploymentData> => {
    const response = await api.get(`/dashboard/sector-segregation/employment-by-sector?year=${year}`);
    return response.data;
  },

  getFormalInformal: async (year: number = 2023): Promise<FormalInformalData> => {
    const response = await api.get(`/dashboard/sector-segregation/formal-informal?year=${year}`);
    return response.data;
  },

  getOccupationSegregation: async (year: number = 2023): Promise<OccupationSegregationData> => {
    const response = await api.get(`/dashboard/sector-segregation/occupation-segregation?year=${year}`);
    return response.data;
  },

  getProvinceEmployment: async (year: number = 2023): Promise<ProvinceEmploymentData> => {
    const response = await api.get(`/dashboard/geography/employment-by-province?year=${year}`);
    return response.data;
  },

  getUrbanRuralGap: async (year: number = 2023): Promise<UrbanRuralData> => {
    const response = await api.get(`/dashboard/geography/urban-rural-gap?year=${year}`);
    return response.data;
  },
};
