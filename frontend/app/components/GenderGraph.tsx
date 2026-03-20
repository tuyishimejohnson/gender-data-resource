import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts";

const data = [
  { year: "2018", gap: 10.5, forecast: null },
  { year: "2019", gap: 9.8, forecast: null },
  { year: "2020", gap: 8.2, forecast: null },
  { year: "2021", gap: 7.1, forecast: null },
  { year: "2022", gap: 6.4, forecast: null },
  { year: "2023", gap: 5.2, forecast: null },
  { year: "2024", gap: null, forecast: 4.1 },
  { year: "2025", gap: null, forecast: 3.2 },
  { year: "2026", gap: null, forecast: 2.5 },
];

export function GenderGapChart() {
  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-gray-900 mb-1">Gender Gap Trend & Forecast</h3>
          <p className="text-sm text-gray-500">2018–2023 historical · 2024–2026 ML forecast</p>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 bg-indigo-600 rounded-full"></div>
            <span className="text-gray-600">Gap</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 bg-gray-300 rounded-full"></div>
            <span className="text-gray-600">Forecast</span>
          </div>
        </div>
      </div>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 5, left: 0, bottom: 5 }}>
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
              domain={[0, 12]}
              ticks={[0, 3, 6, 9, 12]}
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
              stroke="#4f46e5"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={{ fill: "#4f46e5", r: 4 }}
              connectNulls={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
