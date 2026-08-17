import { useState } from "react";
import type { ChartPoint } from "../types/chart";
import { BarChartCard } from "./BarChartCard";
import { PieChartCard } from "./PieChartCard";

interface TerritoryChartCardProps {
  data: ChartPoint[];
  loading?: boolean;
}

type View = "bar" | "pie";

const TITLE = "Sales by territory";

export function TerritoryChartCard({ data, loading }: TerritoryChartCardProps) {
  const [view, setView] = useState<View>("bar");
  const toggle = <ViewToggle view={view} onChange={setView} />;

  return view === "bar" ? (
    <BarChartCard title={TITLE} data={data} loading={loading} headerRight={toggle} />
  ) : (
    <PieChartCard title={TITLE} data={data} loading={loading} headerRight={toggle} />
  );
}

function ViewToggle({ view, onChange }: { view: View; onChange: (view: View) => void }) {
  return (
    <div className="flex rounded-lg border border-line bg-surface-alt p-0.5 text-xs" role="group" aria-label="Chart type">
      {(["bar", "pie"] as const).map((option) => (
        <button
          key={option}
          type="button"
          aria-pressed={view === option}
          onClick={() => onChange(option)}
          className={`rounded-md px-2.5 py-1 font-medium capitalize transition-colors ${
            view === option ? "bg-accent text-white shadow-sm" : "text-ink-muted hover:text-ink"
          }`}
        >
          {option}
        </button>
      ))}
    </div>
  );
}
