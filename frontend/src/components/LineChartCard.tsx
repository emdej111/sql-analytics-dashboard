import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { formatCompactCurrency } from "../lib/format";
import type { ChartPoint } from "../types/chart";
import { AXIS_TICK_STYLE, CHART_CHROME, SERIES_COLOR } from "./chartTheme";
import { ChartCard } from "./ChartCard";
import { ChartTooltip } from "./ChartTooltip";

interface LineChartCardProps {
  title: string;
  data: ChartPoint[];
  loading?: boolean;
}

export function LineChartCard({ title, data, loading }: LineChartCardProps) {
  return (
    <ChartCard title={title} loading={loading} isEmpty={data.length === 0}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="salesFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={SERIES_COLOR} stopOpacity={0.28} />
              <stop offset="100%" stopColor={SERIES_COLOR} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid vertical={false} stroke={CHART_CHROME.grid} />
          <XAxis
            dataKey="label"
            tick={AXIS_TICK_STYLE}
            axisLine={{ stroke: CHART_CHROME.axisLine }}
            tickLine={false}
          />
          <YAxis
            tick={AXIS_TICK_STYLE}
            axisLine={false}
            tickLine={false}
            tickFormatter={(value: number) => formatCompactCurrency(value)}
            width={56}
          />
          <Tooltip content={<ChartTooltip />} cursor={{ stroke: CHART_CHROME.axisLine, strokeWidth: 1 }} />
          <Area
            type="monotone"
            dataKey="value"
            stroke={SERIES_COLOR}
            strokeWidth={2.5}
            fill="url(#salesFill)"
            dot={false}
            activeDot={{ r: 5, fill: SERIES_COLOR, stroke: "#ffffff", strokeWidth: 2 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}
