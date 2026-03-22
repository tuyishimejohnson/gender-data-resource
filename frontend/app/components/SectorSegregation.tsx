import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import type {
  SectorEmploymentData,
  FormalInformalData,
  OccupationSegregationData,
} from "~/services";

interface SectorSegregationProps {
  sectorEmploymentData: SectorEmploymentData | null;
  formalInformalData: FormalInformalData | null;
  occupationData: OccupationSegregationData | null;
  loading?: boolean;
}

export function SectorSegregation({
  sectorEmploymentData,
  formalInformalData,
  occupationData,
  loading,
}: SectorSegregationProps) {
  if (loading || !sectorEmploymentData || !formalInformalData || !occupationData) {
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
  const colors = {
    Formal: "#10b981", // green-500
    Informal: "#f59e0b", // amber-500
    Other: "#6b7280", // gray-500
  };

  const chartConfig = {
    margin: { top: 20, right: 5, left: 0, bottom: 5 },
    height: 280,
  };

  // Transform formal/informal data for pie charts
  const femaleDistribution = formalInformalData.data.map((item) => ({
    name: item.category,
    value: item.Female,
    percentage: item.female_percentage,
  }));

  const maleDistribution = formalInformalData.data.map((item) => ({
    name: item.category,
    value: item.Male,
    percentage: item.male_percentage,
  }));

  // Get top 10 occupations
  const topOccupations = occupationData.data.slice(0, 10);

  // Calculate key insights
  const agricultureSector = sectorEmploymentData.data.find(
    (s) => s.sector === "Agriculture"
  );
  const informalFemale = formalInformalData.data.find(
    (f) => f.category === "Informal"
  )?.female_percentage || 0;
  const informalMale = formalInformalData.data.find(
    (f) => f.category === "Informal"
  )?.male_percentage || 0;

  const CustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    if (percent < 0.05) return null; // Don't show label for small slices

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? "start" : "end"}
        dominantBaseline="central"
        className="text-xs font-semibold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-gray-900 mb-1">
          Sector & Job Type Segregation
        </h3>
        <p className="text-sm text-gray-500">
          Analysis of gender distribution across economic sectors, employment types, and occupations
        </p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Employment by Sector */}
        <div className="border-r border-gray-100 pr-6">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-gray-700">
              Employment by Sector
            </h4>
            {agricultureSector && (
              <span className="text-xs font-medium px-2 py-1 rounded bg-blue-50 text-blue-700">
                {agricultureSector.female_percentage}% F in Agri
              </span>
            )}
          </div>
          <p className="text-xs text-gray-500 mb-4">
            Are women concentrated in agriculture/informal sectors?
          </p>
          <div style={{ height: chartConfig.height }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={sectorEmploymentData.data}
                margin={chartConfig.margin}
                barCategoryGap="20%"
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#f0f0f0"
                  vertical={false}
                />
                <XAxis
                  dataKey="sector"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 11 }}
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
          <div className="mt-4 space-y-2 text-xs">
            {sectorEmploymentData.data.map((sector) => (
              <div key={sector.sector} className="flex items-center justify-between">
                <span className="text-gray-600">{sector.sector}:</span>
                <span className="font-semibold">
                  {sector.female_percentage}% F / {sector.male_percentage}% M
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Formal vs Informal Employment */}
        <div className="border-r border-gray-100 pr-6">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-semibold text-gray-700">
              Formal vs Informal Employment
            </h4>
            <span
              className={`text-xs font-medium px-2 py-1 rounded ${
                informalFemale > informalMale
                  ? "bg-red-100 text-red-700"
                  : "bg-green-100 text-green-700"
              }`}
            >
              {informalFemale > informalMale ? "F>" : "M>"}Informal
            </span>
          </div>
          <p className="text-xs text-gray-500 mb-4">
            Women often overrepresented in informal jobs
          </p>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs font-semibold text-center mb-2 text-gray-700">
                Female
              </p>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={femaleDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={CustomLabel}
                    outerRadius={70}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {femaleDistribution.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={colors[entry.name as keyof typeof colors]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ fontSize: 11, borderRadius: 8 }}
                    formatter={(value: number, name: string, props: any) =>
                      `${props.payload.percentage}%`
                    }
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div>
              <p className="text-xs font-semibold text-center mb-2 text-gray-700">
                Male
              </p>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={maleDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={CustomLabel}
                    outerRadius={70}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {maleDistribution.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={colors[entry.name as keyof typeof colors]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ fontSize: 11, borderRadius: 8 }}
                    formatter={(value: number, name: string, props: any) =>
                      `${props.payload.percentage}%`
                    }
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="mt-4 flex items-center justify-center gap-4 text-xs">
            {Object.entries(colors).map(([name, color]) => (
              <div key={name} className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: color }}
                />
                <span className="text-gray-600">{name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Occupation Segregation */}
        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">
            Occupation Segregation (Top 10)
          </h4>
          <p className="text-xs text-gray-500 mb-4">
            Gender-based job clustering by ISCO codes
          </p>
          <div style={{ height: chartConfig.height }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={topOccupations}
                layout="horizontal"
                margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
                barCategoryGap="10%"
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#f0f0f0"
                  horizontal={false}
                />
                <XAxis
                  type="number"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 10 }}
                  width={40}
                />
                <YAxis
                  type="category"
                  dataKey="code"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9ca3af", fontSize: 9 }}
                  width={30}
                />
                <Tooltip
                  contentStyle={{ fontSize: 11, borderRadius: 8 }}
                  formatter={(value: number, name: string) => [
                    value.toFixed(0),
                    name,
                  ]}
                  labelFormatter={(code: number) => {
                    const occ = topOccupations.find((o) => o.code === code);
                    return occ?.occupation || code;
                  }}
                />
                <Legend
                  iconType="circle"
                  iconSize={6}
                  wrapperStyle={{ fontSize: 10 }}
                />
                <Bar
                  dataKey="Female"
                  fill={femaleColor}
                  radius={[0, 4, 4, 0]}
                />
                <Bar dataKey="Male" fill={maleColor} radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="mt-6 pt-6 border-t border-gray-100">
        <h5 className="text-xs font-semibold text-gray-700 mb-3">
          Key Occupation Insights
        </h5>
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div>
            <p className="font-semibold text-gray-700 mb-2">
              Female-Dominated Occupations:
            </p>
            <ul className="space-y-1">
              {occupationData.data
                .filter((o) => o.female_percentage > 60)
                .slice(0, 3)
                .map((occ) => (
                  <li key={occ.code} className="text-gray-600">
                    • {occ.occupation} ({occ.female_percentage}% F)
                  </li>
                ))}
            </ul>
          </div>
          <div>
            <p className="font-semibold text-gray-700 mb-2">
              Male-Dominated Occupations:
            </p>
            <ul className="space-y-1">
              {occupationData.data
                .filter((o) => o.male_percentage > 60)
                .slice(0, 3)
                .map((occ) => (
                  <li key={occ.code} className="text-gray-600">
                    • {occ.occupation} ({occ.male_percentage}% M)
                  </li>
                ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
