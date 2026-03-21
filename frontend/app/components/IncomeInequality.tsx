import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
  Tooltip,
  Cell,
  ComposedChart,
  Line,
} from "recharts";
import type {
  AverageIncomeData,
  IncomeDistributionData,
  HourlyWageData,
} from "~/services";

interface IncomeInequalityProps {
  averageIncomeData: AverageIncomeData | null;
  incomeDistributionData: IncomeDistributionData | null;
  hourlyWageData: HourlyWageData | null;
  loading?: boolean;
}

export function IncomeInequality({
  averageIncomeData,
  incomeDistributionData,
  hourlyWageData,
  loading,
}: IncomeInequalityProps) {
  if (loading || !averageIncomeData || !incomeDistributionData || !hourlyWageData) {
    return (
      <div className="bg-white border rounded-xl p-6 animate-pulse">
        <div className="h-6 w-64 bg-gray-200 rounded mb-2" />
        <div className="h-4 w-96 bg-gray-200 rounded mb-6" />
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-80 bg-gray-100 rounded" />
          ))}
        </div>
      </div>
    );
  }

  const femaleColor = "#ec4899"; // pink-500
  const maleColor = "#3b82f6"; // blue-500

  // Transform Average Income data for box plot visualization
  const averageIncomeChartData = [
    {
      gender: "Female",
      min: averageIncomeData.data.Female.min,
      q1: averageIncomeData.data.Female.q1,
      median: averageIncomeData.data.Female.median,
      q3: averageIncomeData.data.Female.q3,
      max: averageIncomeData.data.Female.max,
      mean: averageIncomeData.data.Female.mean,
      color: femaleColor,
    },
    {
      gender: "Male",
      min: averageIncomeData.data.Male.min,
      q1: averageIncomeData.data.Male.q1,
      median: averageIncomeData.data.Male.median,
      q3: averageIncomeData.data.Male.q3,
      max: averageIncomeData.data.Male.max,
      mean: averageIncomeData.data.Male.mean,
      color: maleColor,
    },
  ];

  // Transform Hourly Wage data for box plot visualization
  const hourlyWageChartData = [
    {
      gender: "Female",
      min: hourlyWageData.data.Female.min,
      q1: hourlyWageData.data.Female.q1,
      median: hourlyWageData.data.Female.median,
      q3: hourlyWageData.data.Female.q3,
      max: hourlyWageData.data.Female.max,
      mean: hourlyWageData.data.Female.mean,
      color: femaleColor,
    },
    {
      gender: "Male",
      min: hourlyWageData.data.Male.min,
      q1: hourlyWageData.data.Male.q1,
      median: hourlyWageData.data.Male.median,
      q3: hourlyWageData.data.Male.q3,
      max: hourlyWageData.data.Male.max,
      mean: hourlyWageData.data.Male.mean,
      color: maleColor,
    },
  ];

  // Transform Income Distribution data for stacked bar chart
  const incomeDistData = incomeDistributionData.brackets.map((bracket, idx) => ({
    bracket: `Bracket ${bracket}`,
    Female: incomeDistributionData.data.Female[idx] || 0,
    Male: incomeDistributionData.data.Male[idx] || 0,
  }));

  // Calculate wage gap percentages
  const avgIncomeGap = averageIncomeData.data.Male.mean > 0
    ? ((averageIncomeData.data.Male.mean - averageIncomeData.data.Female.mean) /
        averageIncomeData.data.Male.mean) *
      100
    : 0;

  const hourlyWageGap = hourlyWageData.data.Male.mean > 0
    ? ((hourlyWageData.data.Male.mean - hourlyWageData.data.Female.mean) /
        hourlyWageData.data.Male.mean) *
      100
    : 0;

  const chartConfig = {
    margin: { top: 20, right: 5, left: 0, bottom: 5 },
    height: 280,
  };

  const CustomBoxPlot = ({ data }: { data: typeof averageIncomeChartData }) => (
    <ResponsiveContainer width="100%" height={chartConfig.height}>
      <ComposedChart data={data} margin={chartConfig.margin}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
        <XAxis
          dataKey="gender"
          axisLine={false}
          tickLine={false}
          tick={{ fill: "#9ca3af", fontSize: 12 }}
        />
        <YAxis
          axisLine={false}
          tickLine={false}
          tick={{ fill: "#9ca3af", fontSize: 11 }}
          width={50}
        />
        <Tooltip
          contentStyle={{ fontSize: 12, borderRadius: 8 }}
          formatter={(value: number) => value.toFixed(0)}
        />
        <Bar dataKey="q3" stackId="box" fill="transparent" />
        <Bar dataKey="q1" stackId="box">
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} opacity={0.3} />
          ))}
        </Bar>
        <Line
          type="monotone"
          dataKey="median"
          stroke="#1f2937"
          strokeWidth={3}
          dot={{ fill: "#1f2937", r: 4 }}
        />
        <Line
          type="monotone"
          dataKey="mean"
          stroke="#059669"
          strokeWidth={2}
          strokeDasharray="5 5"
          dot={{ fill: "#059669", r: 3 }}
        />
      </ComposedChart>
    </ResponsiveContainer>
  );

  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-gray-900 mb-1">
          Income Inequality Analysis
        </h3>
        <p className="text-sm text-gray-500">
          Comprehensive wage gap analysis showing distribution and true pay inequality
        </p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Average Income by Gender */}
        <div className="border-r border-gray-100 pr-6">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-gray-700">
              Average Income by Gender
            </h4>
            <span
              className={`text-xs font-medium px-2 py-1 rounded ${
                avgIncomeGap > 20
                  ? "bg-red-100 text-red-700"
                  : avgIncomeGap > 10
                  ? "bg-yellow-100 text-yellow-700"
                  : "bg-green-100 text-green-700"
              }`}
            >
              {avgIncomeGap.toFixed(1)}% gap
            </span>
          </div>
          <p className="text-xs text-gray-500 mb-4">
            Monthly income distribution (RWF)
          </p>
          <CustomBoxPlot data={averageIncomeChartData} />
          <div className="mt-4 space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Female Median:</span>
              <span className="font-semibold">
                {averageIncomeData.data.Female.median.toFixed(0)} RWF
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Male Median:</span>
              <span className="font-semibold">
                {averageIncomeData.data.Male.median.toFixed(0)} RWF
              </span>
            </div>
          </div>
        </div>

        {/* Income Distribution */}
        <div className="border-r border-gray-100 pr-6">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">
            Income Distribution (Male vs Female)
          </h4>
          <p className="text-xs text-gray-500 mb-4">
            Are women concentrated in lower brackets?
          </p>
          <div style={{ height: chartConfig.height }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={incomeDistData}
                margin={chartConfig.margin}
                barCategoryGap="15%"
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#f0f0f0"
                  vertical={false}
                />
                <XAxis
                  dataKey="bracket"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 10 }}
                  angle={-45}
                  textAnchor="end"
                  height={60}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
                  width={50}
                />
                <Tooltip
                  contentStyle={{ fontSize: 12, borderRadius: 8 }}
                  formatter={(value: number) => value.toFixed(0)}
                />
                <Legend
                  iconType="circle"
                  iconSize={6}
                  wrapperStyle={{ fontSize: 11 }}
                />
                <Bar
                  dataKey="Female"
                  stackId="a"
                  fill={femaleColor}
                  radius={[0, 0, 0, 0]}
                />
                <Bar
                  dataKey="Male"
                  stackId="a"
                  fill={maleColor}
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Hourly Wage Gap */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-gray-700">
              Hourly Wage Gap
            </h4>
            <span
              className={`text-xs font-medium px-2 py-1 rounded ${
                hourlyWageGap > 20
                  ? "bg-red-100 text-red-700"
                  : hourlyWageGap > 10
                  ? "bg-yellow-100 text-yellow-700"
                  : "bg-green-100 text-green-700"
              }`}
            >
              {hourlyWageGap.toFixed(1)}% gap
            </span>
          </div>
          <p className="text-xs text-gray-500 mb-4">
            True pay inequality (controls for hours)
          </p>
          <CustomBoxPlot data={hourlyWageChartData} />
          <div className="mt-4 space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Female Median:</span>
              <span className="font-semibold">
                {hourlyWageData.data.Female.median.toFixed(0)} RWF/hr
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Male Median:</span>
              <span className="font-semibold">
                {hourlyWageData.data.Male.median.toFixed(0)} RWF/hr
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 pt-6 border-t border-gray-100">
        <div className="flex items-center gap-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-0.5 bg-gray-800" />
            <span className="text-gray-600">Median</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-0.5 bg-green-600 border-dashed border-t-2 border-green-600" />
            <span className="text-gray-600">Mean</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 opacity-30 rounded-sm" />
            <span className="text-gray-600">Interquartile Range (Q1-Q3)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
