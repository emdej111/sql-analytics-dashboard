import type { ReactNode } from "react";
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import type { ChartPoint } from "../types/chart";
import { ChartCard } from "./ChartCard";
import { ChartTooltip } from "./ChartTooltip";
import { CATEGORICAL_COLORS, OTHER_COLOR } from "./chartTheme";

interface PieChartCardProps {
  title: string;
  data: ChartPoint[];
  loading?: boolean;
  headerRight?: ReactNode;
}

const MAX_SLICES = 6; // part-to-whole reads at a glance only up to ~6 segments

interface Slice extends ChartPoint {
  color: string;
}

function buildSlices(data: ChartPoint[]): Slice[] {
  const sorted = [...data].sort((a, b) => b.value - a.value);
  const kept = sorted.slice(0, MAX_SLICES);
  const folded = sorted.slice(MAX_SLICES);

  // Color assignment is by alphabetical label, not by value rank, so a given
  // territory keeps its color across different filter selections instead of
  // being repainted whenever the sort order changes (see anti-patterns: never
  // recolor on filter).
  const colorByLabel = new Map(
    [...kept]
      .sort((a, b) => a.label.localeCompare(b.label))
      .map((point, index) => [point.label, CATEGORICAL_COLORS[index % CATEGORICAL_COLORS.length]]),
  );

  const slices: Slice[] = kept.map((point) => ({ ...point, color: colorByLabel.get(point.label)! }));

  const otherTotal = folded.reduce((sum, point) => sum + point.value, 0);
  if (otherTotal > 0) {
    slices.push({ label: "Other", value: otherTotal, color: OTHER_COLOR });
  }

  return slices;
}

export function PieChartCard({ title, data, loading, headerRight }: PieChartCardProps) {
  const slices = buildSlices(data);

  return (
    <ChartCard
      title={title}
      loading={loading}
      isEmpty={data.length === 0}
      headerRight={headerRight}
      footer={<Legend slices={slices} />}
    >
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Tooltip content={<ChartTooltip />} />
          <Pie
            data={slices}
            dataKey="value"
            nameKey="label"
            cx="50%"
            cy="50%"
            innerRadius="55%"
            outerRadius="80%"
            paddingAngle={2}
            stroke="none"
          >
            {slices.map((slice) => (
              <Cell key={slice.label} fill={slice.color} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function Legend({ slices }: { slices: Slice[] }) {
  return (
    <ul className="mt-4 flex flex-wrap gap-x-4 gap-y-2 text-sm">
      {slices.map((slice) => (
        <li key={slice.label} className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 shrink-0 rounded-sm" style={{ backgroundColor: slice.color }} />
          <span className="font-medium text-ink-secondary">{slice.label}</span>
        </li>
      ))}
    </ul>
  );
}
