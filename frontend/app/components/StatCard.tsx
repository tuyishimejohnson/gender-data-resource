import { Target, Users, UserCheck, BarChart3 } from "lucide-react";
import type { KPIData } from "~/services";

interface StatsCardsProps {
  data: KPIData | null;
  loading?: boolean;
}

export function StatsCards({ data, loading }: StatsCardsProps) {
  if (loading || !data) {
    return (
      <div className="grid grid-cols-4 gap-6">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white border rounded-xl p-6 animate-pulse">
            <div className="h-12 w-12 bg-gray-200 rounded-full mb-4" />
            <div className="h-3 w-24 bg-gray-200 rounded mb-2" />
            <div className="h-8 w-16 bg-gray-200 rounded mb-1" />
            <div className="h-3 w-32 bg-gray-200 rounded" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-4 gap-6">
      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="h-12 w-12 bg-indigo-100 rounded-full flex items-center justify-center">
            <Target className="h-6 w-6 text-indigo-600" />
          </div>
        </div>
        <div className="text-xs font-medium text-gray-500 mb-1">AVG GENDER GAP</div>
        <div className="text-3xl font-bold text-gray-900 mb-1">{data.avg_gender_gap}%</div>
        <div className="text-xs text-gray-500">{data.indicator}</div>
      </div>

      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="h-12 w-12 bg-pink-100 rounded-full flex items-center justify-center">
            <Users className="h-6 w-6 text-pink-600" />
          </div>
        </div>
        <div className="text-xs font-medium text-gray-500 mb-1">FEMALE AVG</div>
        <div className="text-3xl font-bold text-gray-900 mb-1">{data.female_avg}%</div>
        <div className="text-xs text-gray-500">{data.indicator}</div>
      </div>

      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="h-12 w-12 bg-blue-100 rounded-full flex items-center justify-center">
            <UserCheck className="h-6 w-6 text-blue-600" />
          </div>
        </div>
        <div className="text-xs font-medium text-gray-500 mb-1">MALE AVG</div>
        <div className="text-3xl font-bold text-gray-900 mb-1">{data.male_avg}%</div>
        <div className="text-xs text-gray-500">{data.indicator}</div>
      </div>

      <div className="bg-white border rounded-xl p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="h-12 w-12 bg-indigo-100 rounded-full flex items-center justify-center">
            <BarChart3 className="h-6 w-6 text-indigo-600" />
          </div>
        </div>
        <div className="text-xs font-medium text-gray-500 mb-1">REGIONS TRACKED</div>
        <div className="text-3xl font-bold text-gray-900 mb-1">{data.regions_tracked}</div>
        <div className="text-xs text-gray-500">Provinces monitored</div>
      </div>
    </div>
  );
}
