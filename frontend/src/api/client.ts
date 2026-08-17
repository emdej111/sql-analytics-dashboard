import type { DashboardFilters, KPIs, SalesOverTimePoint, TerritorySales, TopProduct } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

type QueryParams = Record<string, string | number | null | undefined>;

async function apiGet<T>(path: string, params: QueryParams = {}): Promise<T> {
  const url = new URL(path, API_BASE_URL);
  for (const [key, value] of Object.entries(params)) {
    if (value !== null && value !== undefined && value !== "") {
      url.searchParams.set(key, String(value));
    }
  }

  const response = await fetch(url.toString());
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `Request to ${path} failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

function dateRangeParams(filters: DashboardFilters): QueryParams {
  return { start_date: filters.startDate, end_date: filters.endDate };
}

export function getKpis(filters: DashboardFilters): Promise<KPIs> {
  return apiGet<KPIs>("/api/kpis", dateRangeParams(filters));
}

export function getSalesOverTime(
  filters: DashboardFilters,
  granularity: "week" | "month" = "month",
): Promise<SalesOverTimePoint[]> {
  return apiGet<SalesOverTimePoint[]>("/api/sales-over-time", {
    ...dateRangeParams(filters),
    territory_id: filters.territoryId,
    granularity,
  });
}

export function getTopProducts(filters: DashboardFilters, limit = 10): Promise<TopProduct[]> {
  return apiGet<TopProduct[]>("/api/top-products", { ...dateRangeParams(filters), limit });
}

export function getSalesByTerritory(filters: DashboardFilters): Promise<TerritorySales[]> {
  return apiGet<TerritorySales[]>("/api/sales-by-territory", dateRangeParams(filters));
}
