// Single source of truth for chart styling so LineChartCard, BarChartCard, and
// PieChartCard stay visually consistent. Values come from the validated
// reference palette (categorical hues in fixed order, chart chrome tokens).

export const SERIES_COLOR = "#2a78d6"; // categorical slot 1 — the single-series color for line/bar

// Fixed order — never cycle or reassign by rank. Slots 1-8.
export const CATEGORICAL_COLORS = [
  "#2a78d6", // blue
  "#eb6834", // orange
  "#1baf7a", // aqua
  "#eda100", // yellow
  "#e87ba4", // magenta
  "#008300", // green
  "#4a3aa7", // violet
  "#e34948", // red
];

export const OTHER_COLOR = "#aab4c6"; // neutral bucket for folded categories, not a series hue

export const CHART_CHROME = {
  grid: "#e1e7f0",
  axisLine: "#c2ccdc",
  tickText: "#64748b",
};

export const AXIS_TICK_STYLE = { fill: CHART_CHROME.tickText, fontSize: 12 };
