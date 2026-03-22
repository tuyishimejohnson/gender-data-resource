import { Bell, ChevronDown } from "lucide-react";
import { Button } from "./ui/button";

export function Header() {
  return (
    <header className="border-b bg-white px-6 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
              <div className="flex flex-col gap-0.5">
                <div className="h-0.5 w-4 bg-white rounded"></div>
                <div className="h-0.5 w-4 bg-white rounded"></div>
                <div className="h-0.5 w-4 bg-white rounded"></div>
              </div>
            </div>
            <div>
              <div className="font-bold text-gray-900">ParityMetrics</div>
              <div className="text-[10px] text-gray-500 leading-none">AI PLATFORM</div>
            </div>
          </div>
          <nav className="flex items-center gap-1">
            <button className="px-4 py-2 text-sm font-medium text-indigo-600 bg-indigo-50 rounded-lg">
              Dashboard
            </button>
            <button className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900">
              Datasets
            </button>
            <button className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900">
              Methodology
            </button>
            <button className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900">
              Reports
            </button>
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-sm">
            <div className="h-2 w-2 bg-green-500 rounded-full"></div>
            <span className="text-gray-600">Live Data</span>
          </div>
          <button className="p-2 text-gray-400 hover:text-gray-600">
            <Bell className="h-5 w-5" />
          </button>
          <Button className="bg-indigo-600 hover:bg-indigo-700 text-white">Export</Button>
          <button className="flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 rounded-lg hover:bg-gray-200">
            <div className="h-8 w-8 bg-indigo-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
              R
            </div>
            <span className="text-gray-900">Researcher</span>
            <ChevronDown className="h-4 w-4 text-gray-400" />
          </button>
        </div>
      </div>
    </header>
  );
}
