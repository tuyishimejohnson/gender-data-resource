import { Calendar, Filter } from "lucide-react";

interface DashboardFiltersProps {
  selectedYear: number;
  onYearChange: (year: number) => void;
  dataPointsCount?: number;
}

export function DashboardFilters({
  selectedYear,
  onYearChange,
  dataPointsCount = 0,
}: DashboardFiltersProps) {
  const availableYears = [2024, 2023, 2022];

  return (
    <div className="bg-white border rounded-xl p-6 flex items-center justify-between">
      <div className="flex items-center gap-6 flex-1">
        <div className="flex-1 max-w-xs">
          <label className="flex items-center gap-2 text-xs font-medium text-gray-500 mb-2">
            <Calendar className="h-4 w-4" />
            SURVEY YEAR
          </label>
          <select
            value={selectedYear}
            onChange={(e) => onYearChange(Number(e.target.value))}
            className="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {availableYears.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="flex items-center gap-2 ml-6 text-xs text-gray-500">
        <Filter className="h-3 w-3" />
        <span>{dataPointsCount} provinces tracked</span>
      </div>
    </div>
  );
}
