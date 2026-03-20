import { Target, Users, UserCheck, BarChart3 } from "lucide-react";

export function StatsCards() {
  return (
    <div className="grid grid-cols-4 gap-6">
      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="h-12 w-12 bg-indigo-100 rounded-full flex items-center justify-center">
            <Target className="h-6 w-6 text-indigo-600" />
          </div>
          <div className="text-xs font-medium text-green-600 flex items-center gap-1">
            <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 7l5 5m0 0l-5 5m5-5H6"
              />
            </svg>
            54.2% since 2018
          </div>
        </div>
        <div className="text-xs font-medium text-gray-500 mb-1">AVG GENDER GAP</div>
        <div className="text-3xl font-bold text-gray-900 mb-1">4.8%</div>
        <div className="text-xs text-gray-500">Current disparity in selection</div>
      </div>

      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="h-12 w-12 bg-pink-100 rounded-full flex items-center justify-center">
            <Users className="h-6 w-6 text-pink-600" />
          </div>
        </div>
        <div className="text-xs font-medium text-gray-500 mb-1">FEMALE AVG</div>
        <div className="text-3xl font-bold text-gray-900 mb-1">52.7%</div>
        <div className="text-xs text-gray-500">Employment Rate (%)</div>
      </div>

      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="h-12 w-12 bg-blue-100 rounded-full flex items-center justify-center">
            <UserCheck className="h-6 w-6 text-blue-600" />
          </div>
        </div>
        <div className="text-xs font-medium text-gray-500 mb-1">MALE AVG</div>
        <div className="text-3xl font-bold text-gray-900 mb-1">57.5%</div>
        <div className="text-xs text-gray-500">Employment Rate (%)</div>
      </div>

      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="h-12 w-12 bg-indigo-100 rounded-full flex items-center justify-center">
            <BarChart3 className="h-6 w-6 text-indigo-600" />
          </div>
        </div>
        <div className="text-xs font-medium text-gray-500 mb-1">REGIONS TRACKED</div>
        <div className="text-3xl font-bold text-gray-900 mb-1">5</div>
        <div className="text-xs text-gray-500">6 indicators monitored</div>
      </div>
    </div>
  );
}
