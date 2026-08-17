import type { ReactNode } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { formatCompactCurrency } from "../lib/format";
import type { ChartPoint } from "../types/chart";
import { AXIS_TICK_STYLE, CHART_CHROME, SERIES_COLOR } from "./chartTheme";
import { ChartCard } from "./ChartCard";
import { ChartTooltip } from "./ChartTooltip";

interface BarChartCardProps {
  title: string;
  data: ChartPoint[];
  loading?: boolean;
  headerRight?: ReactNode;
}

export function BarChartCard({ title, data, loading, headerRight }: BarChartCardProps) {
  return (
    <ChartCard title={title} loading={loading} isEmpty={data.length === 0} headerRight={headerRight}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid vertical={false} stroke={CHART_CHROME.grid} />
          <XAxis
            dataKey="label"
            tick={AXIS_TICK_STYLE}
            axisLine={{ stroke: CHART_CHROME.axisLine }}
            tickLine={false}
            interval={0}
            angle={-20}
            textAnchor="end"
            height={48}
          />
          <YAxis
            tick={AXIS_TICK_STYLE}
            axisLine={false}
            tickLine={false}
            tickFormatter={(value: number) => formatCompactCurrency(value)}
            width={56}
          />
          <Tooltip content={<ChartTooltip />} cursor={{ fill: "#eef2f8" }} />
          {/* One series, nominal categories (territories) -> one color for every bar, never a rainbow. */}
          <Bar dataKey="value" fill={SERIES_COLOR} radius={[6, 6, 0, 0]} maxBarSize={28} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}
