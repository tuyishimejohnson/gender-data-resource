import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Legend } from "recharts";
import type { TimeseriesData } from "~/services";

interface MaleVsFemaleChartProps {
  data: TimeseriesData | null;
  loading?: boolean;
}

export function MaleVsFemaleChart({ data, loading }: MaleVsFemaleChartProps) {
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
    Male: d.Male,
    Female: d.Female,
  }));

  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-gray-900 mb-1">Male vs Female Employment Rate</h3>
        <p className="text-sm text-gray-500">Employment rate trends by gender (%)</p>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 5, right: 5, left: 0, bottom: 5 }}
            barCategoryGap="30%"
            barGap={4}
          >
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
              domain={[0, 100]}
            />
            <Legend
              iconType="circle"
              iconSize={8}
              formatter={(value) => <span className="text-sm text-gray-600">{value}</span>}
            />
            <Bar dataKey="Male" name="Male" fill="#4f46e5" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Female" name="Female" fill="#a5b4fc" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
