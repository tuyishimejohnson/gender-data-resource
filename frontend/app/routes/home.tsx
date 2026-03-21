import { useState, useEffect } from "react";
import { Header } from "~/components/Header";
import { DashboardFilters } from "~/components/DashboardFilter";
import { StatsCards } from "~/components/StatCard";
import { CoreMetrics } from "~/components/CoreMetrics";
import { GenderGapChart } from "~/components/GenderGraph";
import { MaleVsFemaleChart } from "~/components/MalevsFemale";
import { RegionalDisparityChart } from "~/components/RegionalDispacity";
import { IndicatorsTable } from "~/components/Indicator";
import { IncomeInequality } from "~/components/IncomeInequality";
import { SectorSegregation } from "~/components/SectorSegregation";
import { GeographyInequality } from "~/components/GeographyInequality";
import { AIInsights } from "~/components/AllInsight";
import { AskIntelligence } from "~/components/AskIntelligent";
import { Crown } from "lucide-react";
import { dashboardApi } from "~/services";
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
} from "~/services";

export default function App() {
  const [selectedYear, setSelectedYear] = useState(2023);
  const [kpiData, setKpiData] = useState<KPIData | null>(null);
  const [trendData, setTrendData] = useState<TrendData | null>(null);
  const [timeseriesData, setTimeseriesData] = useState<TimeseriesData | null>(null);
  const [regionalData, setRegionalData] = useState<RegionalData | null>(null);
  const [indicatorsData, setIndicatorsData] = useState<IndicatorsData | null>(null);
  const [coreMetricsData, setCoreMetricsData] = useState<CoreMetricsData | null>(null);
  const [averageIncomeData, setAverageIncomeData] = useState<AverageIncomeData | null>(null);
  const [incomeDistributionData, setIncomeDistributionData] =
    useState<IncomeDistributionData | null>(null);
  const [hourlyWageData, setHourlyWageData] = useState<HourlyWageData | null>(null);
  const [sectorEmploymentData, setSectorEmploymentData] = useState<SectorEmploymentData | null>(
    null
  );
  const [formalInformalData, setFormalInformalData] = useState<FormalInformalData | null>(null);
  const [occupationData, setOccupationData] = useState<OccupationSegregationData | null>(null);
  const [provinceData, setProvinceData] = useState<ProvinceEmploymentData | null>(null);
  const [urbanRuralData, setUrbanRuralData] = useState<UrbanRuralData | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch data on mount and when year changes
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [
          kpis,
          trend,
          timeseries,
          regional,
          indicators,
          coreMetrics,
          avgIncome,
          incomeDist,
          hourlyWage,
          sectorEmp,
          formalInf,
          occupation,
          province,
          urbanRural,
        ] = await Promise.all([
          dashboardApi.getKPIs(selectedYear),
          dashboardApi.getTrend(),
          dashboardApi.getTimeseries(),
          dashboardApi.getRegional(selectedYear),
          dashboardApi.getIndicators(selectedYear),
          dashboardApi.getCoreMetrics(),
          dashboardApi.getAverageIncome(selectedYear),
          dashboardApi.getIncomeDistribution(selectedYear),
          dashboardApi.getHourlyWage(selectedYear),
          dashboardApi.getSectorEmployment(selectedYear),
          dashboardApi.getFormalInformal(selectedYear),
          dashboardApi.getOccupationSegregation(selectedYear),
          dashboardApi.getProvinceEmployment(selectedYear),
          dashboardApi.getUrbanRuralGap(selectedYear),
        ]);

        setKpiData(kpis);
        setTrendData(trend);
        setTimeseriesData(timeseries);
        setRegionalData(regional);
        setIndicatorsData(indicators);
        setCoreMetricsData(coreMetrics);
        setAverageIncomeData(avgIncome);
        setIncomeDistributionData(incomeDist);
        setHourlyWageData(hourlyWage);
        setSectorEmploymentData(sectorEmp);
        setFormalInformalData(formalInf);
        setOccupationData(occupation);
        setProvinceData(province);
        setUrbanRuralData(urbanRural);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedYear]);

  const getLastUpdateDate = () => {
    const yearMonths: { [key: number]: string } = {
      2024: "Jun 2024",
      2023: "Dec 2023",
      2022: "Dec 2022",
    };
    return yearMonths[selectedYear] || `Year ${selectedYear}`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-[1600px] mx-auto p-6">
        <div className="mb-6">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Gender Intelligence Dashboard
              </h1>
              <p className="text-gray-500">
                Rwanda · Real-time gender equity analytics powered by AI
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500 mb-2">
                Last updated: <span className="font-medium">{getLastUpdateDate()}</span>
              </div>
              <button className="flex items-center gap-2 px-3 py-1.5 bg-indigo-50 text-indigo-600 rounded-lg text-sm font-medium">
                <Crown className="h-4 w-4" />
                Pro Plan
              </button>
            </div>
          </div>
        </div>

        <div className="mb-6">
          <DashboardFilters
            selectedYear={selectedYear}
            onYearChange={setSelectedYear}
            dataPointsCount={kpiData?.regions_tracked || 0}
          />
        </div>

        <div className="flex gap-6">
          <div className="flex-1 space-y-6">
            <StatsCards data={kpiData} loading={loading} />
            <CoreMetrics data={coreMetricsData} loading={loading} />
            <IncomeInequality
              averageIncomeData={averageIncomeData}
              incomeDistributionData={incomeDistributionData}
              hourlyWageData={hourlyWageData}
              loading={loading}
            />
            <SectorSegregation
              sectorEmploymentData={sectorEmploymentData}
              formalInformalData={formalInformalData}
              occupationData={occupationData}
              loading={loading}
            />
            <GeographyInequality
              provinceData={provinceData}
              urbanRuralData={urbanRuralData}
              loading={loading}
            />

            <IndicatorsTable data={indicatorsData} loading={loading} />
          </div>
          <div className="w-96 space-y-6 sticky top-6 h-fit">
            <AskIntelligence />
            <AIInsights />
          </div>
        </div>
      </main>
    </div>
  );
}
