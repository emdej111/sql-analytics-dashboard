import type { ReactNode } from "react";
import { formatCompactCurrency, formatCompactNumber } from "../lib/format";

interface KPICardProps {
  label: string;
  value: number;
  icon: ReactNode;
  format?: "currency" | "number";
  loading?: boolean;
  /** Ties the card's accent to a chart series color (blue = slot 1, teal = slot 3) so KPI accents and chart hues read as one system. */
  tone?: "blue" | "teal";
}

const TONE_CLASSES: Record<NonNullable<KPICardProps["tone"]>, { bar: string; badge: string; icon: string }> = {
  blue: { bar: "bg-accent", badge: "bg-accent-soft", icon: "text-accent" },
  teal: { bar: "bg-teal", badge: "bg-teal-soft", icon: "text-teal" },
};

export function KPICard({ label, value, icon, format = "number", loading, tone = "blue" }: KPICardProps) {
  const displayValue = format === "currency" ? formatCompactCurrency(value) : formatCompactNumber(value);
  const toneClasses = TONE_CLASSES[tone];

  return (
    <div className="group relative overflow-hidden rounded-xl border border-line bg-surface p-5 shadow-sm transition-shadow hover:shadow-md">
      <span className={`absolute inset-x-0 top-0 h-1 ${toneClasses.bar}`} aria-hidden="true" />

      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-ink-muted">{label}</p>
          {loading ? (
            <div className="mt-2.5 h-8 w-24 animate-pulse rounded bg-line" aria-hidden="true" />
          ) : (
            <p className="mt-1.5 truncate text-3xl font-bold tracking-tight text-ink">{displayValue}</p>
          )}
        </div>

        <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${toneClasses.badge}`}>
          <span className={`h-5 w-5 ${toneClasses.icon}`}>{icon}</span>
        </div>
      </div>
    </div>
  );
}
