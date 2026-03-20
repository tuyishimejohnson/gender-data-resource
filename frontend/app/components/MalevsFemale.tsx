import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Legend } from "recharts";

const data = [
  { category: "Education", male: 68, female: 72 },
  { category: "Employment", male: 74, female: 52 },
  { category: "Health", male: 61, female: 78 },
  { category: "Leadership", male: 81, female: 24 },
  { category: "Finance", male: 70, female: 44 },
];

export function MaleVsFemaleChart() {
  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-gray-900 mb-1">Male vs Female Participation</h3>
        <p className="text-sm text-gray-500">Sector breakdown by gender (%)</p>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 5, right: 5, left: 0, bottom: 5 }}
            barCategoryGap="30%"
            barGap={4}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
            <XAxis
              dataKey="category"
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
            <Bar dataKey="male" name="Male" fill="#4f46e5" radius={[4, 4, 0, 0]} />
            <Bar dataKey="female" name="Female" fill="#a5b4fc" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
