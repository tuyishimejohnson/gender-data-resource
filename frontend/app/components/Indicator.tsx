import { Download, CheckCircle2, AlertTriangle } from "lucide-react";
import type { IndicatorsData } from "~/services";

interface IndicatorsTableProps {
  data: IndicatorsData | null;
  loading?: boolean;
}

export function IndicatorsTable({ data, loading }: IndicatorsTableProps) {
  if (loading || !data) {
    return (
      <div className="bg-white border rounded-xl p-6 animate-pulse">
        <div className="h-6 w-48 bg-gray-200 rounded mb-2" />
        <div className="h-4 w-64 bg-gray-200 rounded mb-6" />
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-12 bg-gray-100 rounded" />
          ))}
        </div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    if (status.includes("On Track") || status.includes("🟢")) {
      return "text-green-600";
    }
    return "text-amber-600";
  };

  const getStatusIcon = (status: string) => {
    if (status.includes("On Track") || status.includes("🟢")) {
      return <CheckCircle2 className="h-4 w-4" />;
    }
    return <AlertTriangle className="h-4 w-4" />;
  };

  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-gray-900 mb-1">All Indicators Overview</h3>
          <p className="text-sm text-gray-500">
            Comparative gender gaps across all tracked indicators — {data.year}
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-indigo-600 hover:bg-indigo-50 rounded-lg">
          <Download className="h-4 w-4" />
          Export CSV
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                INDICATOR
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                FEMALE
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                MALE
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                GAP
              </th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
                STATUS
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {data.data.map((indicator, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="py-4 px-4 text-sm text-gray-900">{indicator.INDICATOR}</td>
                <td className="py-4 px-4 text-sm font-medium text-pink-600">{indicator.FEMALE}</td>
                <td className="py-4 px-4 text-sm font-medium text-blue-600">{indicator.MALE}</td>
                <td className="py-4 px-4 text-sm font-medium text-gray-900">{indicator.GAP}</td>
                <td className="py-4 px-4">
                  <div
                    className={`flex items-center gap-2 text-sm font-medium ${getStatusColor(
                      indicator.STATUS
                    )}`}
                  >
                    {getStatusIcon(indicator.STATUS)}
                    {indicator.STATUS.replace("🟢 ", "").replace("🟡 ", "")}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
