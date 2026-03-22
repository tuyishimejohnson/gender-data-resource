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
} from "recharts";
import type {
  ProvinceEmploymentData,
  UrbanRuralData,
} from "~/services";

interface GeographyInequalityProps {
  provinceData: ProvinceEmploymentData | null;
  urbanRuralData: UrbanRuralData | null;
  loading?: boolean;
}

export function GeographyInequality({
  provinceData,
  urbanRuralData,
  loading,
}: GeographyInequalityProps) {
  if (loading || !provinceData || !urbanRuralData) {
    return (
      <div className="bg-white border rounded-xl p-6 animate-pulse">
        <div className="h-6 w-64 bg-gray-200 rounded mb-2" />
        <div className="h-4 w-96 bg-gray-200 rounded mb-6" />
        <div className="grid grid-cols-2 gap-6">
          {[1, 2].map((i) => (
            <div key={i} className="h-80 bg-gray-100 rounded" />
          ))}
        </div>
      </div>
    );
  }

  const femaleColor = "#ec4899"; // pink-500
  const maleColor = "#3b82f6"; // blue-500

  const chartConfig = {
    margin: { top: 20, right: 5, left: 10, bottom: 5 },
    height: 320,
  };

  // Sort provinces by gap (highest first)
  const sortedProvinces = [...provinceData.data].sort((a, b) => b.gap - a.gap);

  // Find urban and rural data
  const urbanData = urbanRuralData.data.find((d) => d.area === "Urban");
  const ruralData = urbanRuralData.data.find((d) => d.area === "Rural");

  // Calculate insights
  const highestGapProvince = sortedProvinces[0];
  const lowestGapProvince = sortedProvinces[sortedProvinces.length - 1];
  const ruralGap = ruralData?.gap || 0;
  const urbanGap = urbanData?.gap || 0;
  const ruralDisadvantage = ruralGap > urbanGap;

  // Province colors - gradient from red (high gap) to green (low gap)
  const getProvinceColor = (gap: number) => {
    if (gap > 10) return "#ef4444"; // red-500
    if (gap > 5) return "#f59e0b"; // amber-500
    return "#10b981"; // green-500
  };

  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-gray-900 mb-1">
          Geography-Based Gender Inequality
        </h3>
        <p className="text-sm text-gray-500">
          Regional employment disparities and urban-rural gender gaps across Rwanda
        </p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Employment by Province */}
        <div className="border-r border-gray-100 pr-6">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-gray-700">
              Employment Rate by Province
            </h4>
            <span
              className={`text-xs font-medium px-2 py-1 rounded ${
                highestGapProvince.gap > 10
                  ? "bg-red-100 text-red-700"
                  : highestGapProvince.gap > 5
                  ? "bg-yellow-100 text-yellow-700"
                  : "bg-green-100 text-green-700"
              }`}
            >
              Max Gap: {highestGapProvince.gap}%
            </span>
          </div>
          <p className="text-xs text-gray-500 mb-4">
            Gender employment gap across Rwanda's five provinces
          </p>
          <div style={{ height: chartConfig.height }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={sortedProvinces}
                margin={chartConfig.margin}
                barCategoryGap="15%"
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#f0f0f0"
                  vertical={false}
                />
                <XAxis
                  dataKey="province"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 10 }}
                  angle={-20}
                  textAnchor="end"
                  height={60}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
                  width={40}
                  domain={[0, 100]}
                  label={{
                    value: "Employment Rate (%)",
                    angle: -90,
                    position: "insideLeft",
                    style: { fontSize: 10, fill: "#6b7280" },
                  }}
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
                <Bar
                  dataKey="Female"
                  fill={femaleColor}
                  radius={[4, 4, 0, 0]}
                />
                <Bar dataKey="Male" fill={maleColor} radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Highest Gap:</span>
              <span className="font-semibold text-red-700">
                {highestGapProvince.province} ({highestGapProvince.gap}%)
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Lowest Gap:</span>
              <span className="font-semibold text-green-700">
                {lowestGapProvince.province} ({lowestGapProvince.gap}%)
              </span>
            </div>
          </div>
        </div>

        {/* Urban vs Rural Gender Gap */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-gray-700">
              Urban vs Rural Gender Gap
            </h4>
            {ruralDisadvantage ? (
              <span className="text-xs font-medium px-2 py-1 rounded bg-red-100 text-red-700">
                Rural More Disadvantaged
              </span>
            ) : (
              <span className="text-xs font-medium px-2 py-1 rounded bg-blue-100 text-blue-700">
                Urban More Disadvantaged
              </span>
            )}
          </div>
          <p className="text-xs text-gray-500 mb-4">
            Rural women often face greater employment barriers
          </p>
          <div style={{ height: chartConfig.height }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={urbanRuralData.data}
                margin={chartConfig.margin}
                barCategoryGap="30%"
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#f0f0f0"
                  vertical={false}
                />
                <XAxis
                  dataKey="area"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 12 }}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
                  width={40}
                  domain={[0, 100]}
                  label={{
                    value: "Employment Rate (%)",
                    angle: -90,
                    position: "insideLeft",
                    style: { fontSize: 10, fill: "#6b7280" },
                  }}
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
                <Bar
                  dataKey="Female"
                  fill={femaleColor}
                  radius={[4, 4, 0, 0]}
                />
                <Bar dataKey="Male" fill={maleColor} radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-3">
            {urbanData && (
              <div className="bg-blue-50 rounded-lg p-3">
                <p className="text-xs font-semibold text-blue-900 mb-2">
                  Urban Areas
                </p>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-blue-700">Female:</span>
                    <span className="font-semibold ml-1">{urbanData.Female}%</span>
                  </div>
                  <div>
                    <span className="text-blue-700">Male:</span>
                    <span className="font-semibold ml-1">{urbanData.Male}%</span>
                  </div>
                  <div className="col-span-2">
                    <span className="text-blue-700">Gap:</span>
                    <span className="font-semibold ml-1">{urbanData.gap}%</span>
                  </div>
                </div>
              </div>
            )}
            {ruralData && (
              <div className="bg-green-50 rounded-lg p-3">
                <p className="text-xs font-semibold text-green-900 mb-2">
                  Rural Areas
                </p>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-green-700">Female:</span>
                    <span className="font-semibold ml-1">{ruralData.Female}%</span>
                  </div>
                  <div>
                    <span className="text-green-700">Male:</span>
                    <span className="font-semibold ml-1">{ruralData.Male}%</span>
                  </div>
                  <div className="col-span-2">
                    <span className="text-green-700">Gap:</span>
                    <span className="font-semibold ml-1">{ruralData.gap}%</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="mt-6 pt-6 border-t border-gray-100">
        <h5 className="text-xs font-semibold text-gray-700 mb-3">
          Key Geographic Insights
        </h5>
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div>
            <p className="font-semibold text-gray-700 mb-2">
              Provincial Disparities:
            </p>
            <ul className="space-y-1">
              {sortedProvinces.slice(0, 3).map((prov) => (
                <li key={prov.province} className="text-gray-600">
                  •{" "}
                  <span className="font-medium" style={{ color: getProvinceColor(prov.gap) }}>
                    {prov.province}
                  </span>
                  : {prov.gap}% gap (F: {prov.Female}%, M: {prov.Male}%)
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p className="font-semibold text-gray-700 mb-2">
              Urban-Rural Analysis:
            </p>
            <ul className="space-y-1 text-gray-600">
              <li>
                • Rural gap is{" "}
                <span className="font-semibold">
                  {ruralDisadvantage ? "larger" : "smaller"}
                </span>{" "}
                than urban
              </li>
              <li>
                • Difference: {Math.abs(ruralGap - urbanGap).toFixed(1)} percentage
                points
              </li>
              {ruralDisadvantage && (
                <li className="text-red-600">
                  • Rural women face greater employment barriers
                </li>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
