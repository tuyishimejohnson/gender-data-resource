import {
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  TrendingUp,
  Lightbulb,
  ArrowRight,
} from "lucide-react";

export function AIInsights() {
  const insights = [
    {
      icon: CheckCircle2,
      iconColor: "text-green-500",
      title: "Gap Closing",
      description: "Employment Rate (%) gender gap has decreasing by 54.2% since 2018.",
    },
    {
      icon: AlertTriangle,
      iconColor: "text-amber-500",
      title: "Highest Disparity",
      description: "Eastern Province shows the highest gap at 8.5%.",
    },
    {
      icon: TrendingUp,
      iconColor: "text-green-500",
      title: "Parity Leader",
      description: "Western Province leads in gender parity with gap of 2.2%.",
    },
    {
      icon: Lightbulb,
      iconColor: "text-indigo-500",
      title: "Forecast Signal",
      description: "ML model projects gap will decrease through 2026.",
    },
  ];

  return (
    <div className="bg-gradient-to-br from-gray-900 to-indigo-950 rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-indigo-400" />
          <h3 className="text-lg font-bold text-white">AI INSIGHTS</h3>
        </div>
        <div className="px-2 py-1 bg-green-500 text-white text-xs font-medium rounded">Live</div>
      </div>
      <div className="space-y-4">
        {insights.map((insight, index) => (
          <div key={index} className="bg-white/5 border border-white/10 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div className={`${insight.iconColor} mt-0.5`}>
                <insight.icon className="h-5 w-5" />
              </div>
              <div className="flex-1">
                <h4 className="text-white font-semibold text-sm mb-1">{insight.title}</h4>
                <p className="text-gray-400 text-sm leading-relaxed">{insight.description}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
      <button className="w-full mt-4 px-4 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg flex items-center justify-center gap-2">
        Full Impact Report
        <ArrowRight className="h-4 w-4" />
      </button>
    </div>
  );
}
