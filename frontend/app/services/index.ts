import axios from "axios";
import type {
  KPIData,
  TrendData,
  TimeseriesData,
  RegionalData,
  IndicatorsData,
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
};
