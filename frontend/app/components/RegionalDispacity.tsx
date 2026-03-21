import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts";
import type { RegionalData } from "~/services";

interface RegionalDisparityChartProps {
  data: RegionalData | null;
  loading?: boolean;
}

export function RegionalDisparityChart({ data, loading }: RegionalDisparityChartProps) {
  if (loading || !data) {
    return (
      <div className="bg-white border rounded-xl p-6 animate-pulse">
        <div className="h-6 w-48 bg-gray-200 rounded mb-2" />
        <div className="h-4 w-64 bg-gray-200 rounded mb-6" />
        <div className="h-64 bg-gray-100 rounded" />
      </div>
    );
  }

  // Transform data for chart - showing gap values directly
  const chartData = data.data.map((d) => ({
    region: d.region,
    gap: d.gap,
  }));

  const maxGap = Math.max(...data.data.map((d) => d.gap), 10);

  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-gray-900 mb-1">Regional Gender Gap Distribution</h3>
        <p className="text-sm text-gray-500">Employment rate gender gap by province (%)</p>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 5, right: 5, left: 0, bottom: 5 }}
            barCategoryGap="40%"
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
            <XAxis
              dataKey="region"
              axisLine={false}
              tickLine={false}
              tick={{ fill: "#9ca3af", fontSize: 12 }}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: "#9ca3af", fontSize: 12 }}
              domain={[0, Math.ceil(maxGap * 1.2)]}
            />
            <Bar dataKey="gap" name="Gender Gap (%)" fill="#4f46e5" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 text-xs text-gray-500">
        <span>Year: {data.year} • Sorted by gap magnitude (highest to lowest)</span>
      </div>
    </div>
  );
}
