import { TrendingUp, Calendar, MapPin, Filter } from "lucide-react";

export function DashboardFilters() {
  return (
    <div className="bg-white border rounded-xl p-6 flex items-center justify-between">
      <div className="flex items-center gap-6 flex-1">
        <div className="flex-1">
          <label className="flex items-center gap-2 text-xs font-medium text-gray-500 mb-2">
            <TrendingUp className="h-4 w-4" />
            INDICATOR
          </label>
          <select className="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-900">
            <option>Employment Rate (%)</option>
            <option>Literacy Rate (%)</option>
            <option>Primary Education (%)</option>
          </select>
        </div>
        <div className="flex-1">
          <label className="flex items-center gap-2 text-xs font-medium text-gray-500 mb-2">
            <Calendar className="h-4 w-4" />
            YEAR
          </label>
          <select className="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-900">
            <option>2023</option>
            <option>2022</option>
            <option>2021</option>
          </select>
        </div>
        <div className="flex-1">
          <label className="flex items-center gap-2 text-xs font-medium text-gray-500 mb-2">
            <MapPin className="h-4 w-4" />
            REGION
          </label>
          <select className="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-900">
            <option>All Regions</option>
            <option>Eastern</option>
            <option>Northern</option>
            <option>Southern</option>
          </select>
        </div>
      </div>
      <div className="flex items-center gap-2 ml-6 text-xs text-gray-500">
        <Filter className="h-3 w-3" />
        <span>5 data points loaded</span>
      </div>
    </div>
  );
}
