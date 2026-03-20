import { Download, CheckCircle2, AlertTriangle } from "lucide-react";

export function IndicatorsTable() {
  const indicators = [
    {
      name: "Employment Rate (%)",
      female: "52.7%",
      male: "57.5%",
      gap: "4.8%",
      status: "On Track",
      statusColor: "text-green-600",
    },
    {
      name: "Literacy Rate (%)",
      female: "59.9%",
      male: "64.8%",
      gap: "4.9%",
      status: "On Track",
      statusColor: "text-green-600",
    },
    {
      name: "Primary Education (%)",
      female: "61.9%",
      male: "70.2%",
      gap: "8.4%",
      status: "Needs Attention",
      statusColor: "text-amber-600",
    },
    {
      name: "Wage (Monthly Avg)",
      female: "62.5%",
      male: "67.6%",
      gap: "5.1%",
      status: "On Track",
      statusColor: "text-green-600",
    },
    {
      name: "Healthcare Access (%)",
      female: "52.6%",
      male: "62.9%",
      gap: "10.3%",
      status: "Needs Attention",
      statusColor: "text-amber-600",
    },
    {
      name: "Business Ownership (%)",
      female: "57.3%",
      male: "64.0%",
      gap: "6.6%",
      status: "On Track",
      statusColor: "text-green-600",
    },
  ];

  return (
    <div className="bg-white border rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-gray-900 mb-1">All Indicators Overview</h3>
          <p className="text-sm text-gray-500">
            Comparative gender gaps across all tracked indicators — 2023
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
            {indicators.map((indicator, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="py-4 px-4 text-sm text-gray-900">{indicator.name}</td>
                <td className="py-4 px-4 text-sm font-medium text-pink-600">{indicator.female}</td>
                <td className="py-4 px-4 text-sm font-medium text-blue-600">{indicator.male}</td>
                <td className="py-4 px-4 text-sm font-medium text-gray-900">{indicator.gap}</td>
                <td className="py-4 px-4">
                  <div
                    className={`flex items-center gap-2 text-sm font-medium ${indicator.statusColor}`}
                  >
                    {indicator.status === "On Track" ? (
                      <CheckCircle2 className="h-4 w-4" />
                    ) : (
                      <AlertTriangle className="h-4 w-4" />
                    )}
                    {indicator.status}
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
