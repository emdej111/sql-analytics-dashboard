import type { ReactNode } from "react";
import { ChartEmptyState } from "./ChartEmptyState";
import { ChartSkeleton } from "./ChartSkeleton";

interface ChartCardProps {
  title: string;
  loading?: boolean;
  isEmpty: boolean;
  headerRight?: ReactNode;
  /** Content below the fixed-height plot area — e.g. a legend. Hidden during skeleton/empty states. */
  footer?: ReactNode;
  /** Height in px of the plot area (excludes footer). Fixed height always includes the axis band. */
  height?: number;
  children: ReactNode;
}

// Shared chrome for every chart card: title row, optional header control
// (e.g. the bar/pie toggle), and the loading/empty/content switch. Centralizing
// this is what keeps LineChartCard, BarChartCard, and PieChartCard looking
// identical instead of drifting apart.
export function ChartCard({ title, loading = false, isEmpty, headerRight, footer, height = 256, children }: ChartCardProps) {
  const showSkeleton = loading && isEmpty; // first load, nothing to show yet
  const showEmptyState = !loading && isEmpty; // finished loading, genuinely no data
  const showChart = !showSkeleton && !showEmptyState;

  return (
    <div className="rounded-xl border border-line bg-surface p-5 shadow-sm transition-shadow hover:shadow-md sm:p-6">
      <div className="flex items-center justify-between">
        <h2 className="text-base font-semibold tracking-tight text-ink">{title}</h2>
        {headerRight}
      </div>

      {/* Refetch keeps the frame: fade the existing chart rather than flashing a skeleton. */}
      <div className={`mt-4 transition-opacity ${loading && !isEmpty ? "opacity-50" : "opacity-100"}`}>
        <div style={{ height }}>
          {showSkeleton && <ChartSkeleton />}
          {showEmptyState && <ChartEmptyState />}
          {showChart && children}
        </div>
        {showChart && footer}
      </div>
    </div>
  );
}
