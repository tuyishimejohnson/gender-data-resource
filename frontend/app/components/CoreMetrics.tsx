import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";
import type { CoreMetricsData } from "~/services";

interface CoreMetricsProps {
  data: CoreMetricsData | null;
  loading?: boolean;
}

export function CoreMetrics({ data, loading }: CoreMetricsProps) {
  if (loading || !data) {
    return (
      <div className="bg-white border rounded-xl p-6 animate-pulse">
        <div className="h-6 w-64 bg-gray-200 rounded mb-2" />
        <div className="h-4 w-96 bg-gray-200 rounded mb-6" />
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-64 bg-gray-100 rounded" />
          ))}
        </div>
      </div>
    );
  }

  // Transform data for Employment Rate chart
  const employmentData = data.data.map((d) => ({
    year: d.year.toString(),
    Female: d.employment_rate.Female,
    Male: d.employment_rate.Male,
  }));

  // Transform data for Unemployment Rate chart
  const unemploymentData = data.data.map((d) => ({
    year: d.year.toString(),
    Female: d.unemployment_rate.Female,
    Male: d.unemployment_rate.Male,
  }));

  // Transform data for LFPR chart
  const lfprData = data.data.map((d) => ({
    year: d.year.toString(),
    Female: d.lfpr.Female,
    Male: d.lfpr.Male,
  }));

  // Shared chart configuration
  const chartConfig = {
    margin: { top: 5, right: 5, left: 0, bottom: 5 },
    height: 240,
  };

  const femaleColor = "#ec4899"; // pink-500
  const maleColor = "#3b82f6"; // blue-500

  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-gray-900 mb-1">
          Core Gender Gap Metrics
        </h3>
        <p className="text-sm text-gray-500">
          Comparative analysis of employment, unemployment, and labour force participation by gender
        </p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Employment Rate Chart */}
        <div className="border-r border-gray-100 pr-6 last:border-r-0">
          <h4 className="text-sm font-semibold text-gray-700 mb-4">
            Employment Rate (%)
          </h4>
          <div style={{ height: chartConfig.height }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={employmentData}
                margin={chartConfig.margin}
                barCategoryGap="20%"
                barGap={2}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                <XAxis
                  dataKey="year"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
                  domain={[0, 100]}
                  width={35}
                />
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 8 }}
                  formatter={(value: number) => `${value}%`}
                />
                <Legend
                  iconType="circle"
                  iconSize={6}
                  wrapperStyle={{ fontSize: 11 }}
                />
                <Bar dataKey="Male" name="Male" fill={maleColor} radius={[4, 4, 0, 0]} />
                <Bar dataKey="Female" name="Female" fill={femaleColor} radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Unemployment Rate Chart */}
        <div className="border-r border-gray-100 pr-6 last:border-r-0">
          <h4 className="text-sm font-semibold text-gray-700 mb-4">
            Unemployment Rate (%)
          </h4>
          <div style={{ height: chartConfig.height }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={unemploymentData} margin={chartConfig.margin}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                <XAxis
                  dataKey="year"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
                  domain={[0, "auto"]}
                  width={35}
                />
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 8 }}
                  formatter={(value: number) => `${value}%`}
                />
                <Legend
                  iconType="circle"
                  iconSize={6}
                  wrapperStyle={{ fontSize: 11 }}
                />
                <Line
                  type="monotone"
                  dataKey="Male"
                  name="Male"
                  stroke={maleColor}
                  strokeWidth={2}
                  dot={{ fill: maleColor, r: 4 }}
                />
                <Line
                  type="monotone"
                  dataKey="Female"
                  name="Female"
                  stroke={femaleColor}
                  strokeWidth={2}
                  dot={{ fill: femaleColor, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* LFPR Chart */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-4">
            Labour Force Participation Rate (%)
          </h4>
          <div style={{ height: chartConfig.height }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={lfprData} margin={chartConfig.margin}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                <XAxis
                  dataKey="year"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
                  domain={[0, 100]}
                  width={35}
                />
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 8 }}
                  formatter={(value: number) => `${value}%`}
                />
                <Legend
                  iconType="circle"
                  iconSize={6}
                  wrapperStyle={{ fontSize: 11 }}
                />
                <Line
                  type="monotone"
                  dataKey="Male"
                  name="Male"
                  stroke={maleColor}
                  strokeWidth={2}
                  dot={{ fill: maleColor, r: 4 }}
                />
                <Line
                  type="monotone"
                  dataKey="Female"
                  name="Female"
                  stroke={femaleColor}
                  strokeWidth={2}
                  dot={{ fill: femaleColor, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
