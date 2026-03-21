import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts";
import type { TrendData } from "~/services";

interface GenderGapChartProps {
  data: TrendData | null;
  loading?: boolean;
}

export function GenderGapChart({ data, loading }: GenderGapChartProps) {
  if (loading || !data) {
    return (
      <div className="bg-white border rounded-xl p-6 animate-pulse">
        <div className="h-6 w-48 bg-gray-200 rounded mb-2" />
        <div className="h-4 w-64 bg-gray-200 rounded mb-6" />
        <div className="h-64 bg-gray-100 rounded" />
      </div>
    );
  }

  // Transform data for chart
  const chartData = data.data.map((d) => ({
    year: d.year.toString(),
    gap: d.segment === "Historical" ? d.gap : null,
    forecast: d.segment === "Forecast" ? d.gap : null,
  }));

  const historical = data.data.filter((d) => d.segment === "Historical");
  const minYear = historical.length > 0 ? Math.min(...historical.map((d) => d.year)) : 2022;
  const maxYear = Math.max(...data.data.map((d) => d.year));

  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-gray-900 mb-1">Gender Gap Trend & Forecast</h3>
          <p className="text-sm text-gray-500">
            {minYear}–{historical[historical.length - 1]?.year} historical · {maxYear - 1}–{maxYear}{" "}
            forecast
          </p>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 bg-indigo-600 rounded-full"></div>
            <span className="text-gray-600">Historical</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 bg-gray-400 rounded-full"></div>
            <span className="text-gray-600">Forecast</span>
          </div>
        </div>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 5, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
            <XAxis
              dataKey="year"
              axisLine={false}
              tickLine={false}
              tick={{ fill: "#9ca3af", fontSize: 12 }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: "#9ca3af", fontSize: 12 }}
              domain={[0, "auto"]}
            />
            <Line
              type="monotone"
              dataKey="gap"
              stroke="#4f46e5"
              strokeWidth={2}
              dot={{ fill: "#4f46e5", r: 4 }}
              connectNulls={false}
            />
            <Line
              type="monotone"
              dataKey="forecast"
              stroke="#9ca3af"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={{ fill: "#9ca3af", r: 4 }}
              connectNulls={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
