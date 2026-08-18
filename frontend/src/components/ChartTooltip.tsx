import { formatCurrency } from "../lib/format";

interface TooltipEntry {
  value: number;
  name?: string;
  color?: string;
  payload?: { fill?: string };
}

interface ChartTooltipProps {
  active?: boolean;
  label?: string;
  payload?: TooltipEntry[];
}

// Shared across Line/Bar/Pie so hover feedback looks identical everywhere.
// "Values lead, labels follow" — the number is the strong element, the
// series/category name is secondary. A colored left rule ties the card back
// to the mark it's describing without relying on a swatch alone.
export function ChartTooltip({ active, label, payload }: ChartTooltipProps) {
  if (!active || !payload?.length) return null;

  if (payload.length === 1) {
    const [entry] = payload;
    const color = entry.color ?? entry.payload?.fill;
    return (
      <div
        className="rounded-lg border border-line bg-surface px-3.5 py-2.5 text-sm shadow-lg"
        style={color ? { borderLeft: `3px solid ${color}` } : undefined}
      >
        <p className="text-base font-bold tabular-nums text-ink">{formatCurrency(entry.value)}</p>
        <p className="mt-0.5 text-ink-secondary">{label ?? entry.name}</p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-line bg-surface px-3.5 py-2.5 text-sm shadow-lg">
      {label && <p className="font-semibold text-ink-secondary">{label}</p>}
      <div className="mt-1.5 space-y-1.5">
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center gap-2">
            <span
              className="h-2.5 w-2.5 shrink-0 rounded-sm"
              style={{ backgroundColor: entry.color ?? entry.payload?.fill }}
            />
            <span className="font-semibold tabular-nums text-ink">{formatCurrency(entry.value)}</span>
            <span className="text-ink-secondary">{entry.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
