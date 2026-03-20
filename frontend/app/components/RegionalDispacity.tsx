import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts";

const data = [
  { region: "Kigali", high: 78, medium: 0, low: 0 },
  { region: "Eastern", high: 0, medium: 61, low: 0 },
  { region: "Western", high: 0, medium: 0, low: 55 },
  { region: "Northern", high: 0, medium: 0, low: 58 },
  { region: "Southern", high: 0, medium: 0, low: 52 },
];

export function RegionalDisparityChart() {
  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="mb-6">
        <h3 className="text-lg font-bold text-gray-900 mb-1">Regional Gender Equity Scores</h3>
        <p className="text-sm text-gray-500">Province-level gender parity index (0–100)</p>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
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
              domain={[0, 100]}
            />
            <Bar
              dataKey="high"
              name="High (≥70)"
              stackId="a"
              fill="#4f46e5"
              radius={[4, 4, 0, 0]}
            />
            <Bar
              dataKey="medium"
              name="Medium (60–69)"
              stackId="a"
              fill="#818cf8"
              radius={[4, 4, 0, 0]}
            />
            <Bar dataKey="low" name="Low (<60)" stackId="a" fill="#c7d2fe" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="flex items-center gap-4 mt-4 text-xs text-gray-500">
        <div className="flex items-center gap-1.5">
          <div className="h-2.5 w-2.5 rounded-sm bg-indigo-600" />
          <span>High (≥70)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="h-2.5 w-2.5 rounded-sm bg-indigo-400" />
          <span>Medium (60–69)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="h-2.5 w-2.5 rounded-sm bg-indigo-200" />
          <span>Low (&lt;60)</span>
        </div>
      </div>
    </div>
  );
}
