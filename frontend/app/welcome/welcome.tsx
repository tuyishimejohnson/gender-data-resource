import { Header } from "~/components/Header";
import { DashboardFilters } from "~/components/DashboardFilter";
import { StatsCards } from "~/components/StatCard";
import { GenderGapChart } from "~/components/GenderGraph";
import { MaleVsFemaleChart } from "~/components/MalevsFemale";
import { RegionalDisparityChart } from "~/components/RegionalDispacity";
import { IndicatorsTable } from "~/components/Indicator";
import { AIInsights } from "~/components/AllInsight";
import { AskIntelligence } from "~/components/AskIntelligent";
import { Crown } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-[1600px] mx-auto p-6">
        <div className="mb-6">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Gender Intelligence Dashboard
              </h1>
              <p className="text-gray-500">
                Rwanda · Real-time gender equity analytics powered by AI
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500 mb-2">
                Last updated: <span className="font-medium">Jun 2024</span>
              </div>
              <button className="flex items-center gap-2 px-3 py-1.5 bg-indigo-50 text-indigo-600 rounded-lg text-sm font-medium">
                <Crown className="h-4 w-4" />
                Pro Plan
              </button>
            </div>
          </div>
        </div>

        <div className="mb-6">
          <DashboardFilters />
        </div>

        <div className="flex gap-6">
          <div className="flex-1 space-y-6">
            <StatsCards />
            <GenderGapChart />
            <MaleVsFemaleChart />
            <RegionalDisparityChart />
            <IndicatorsTable />
          </div>
          <div className="w-96 space-y-6 sticky top-6 h-fit">
            <AIInsights />
            <AskIntelligence />
          </div>
        </div>
      </main>
    </div>
  );
}
