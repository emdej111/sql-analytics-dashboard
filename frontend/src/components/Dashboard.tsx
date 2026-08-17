import { useEffect, useState } from "react";
import { getKpis, getSalesByTerritory, getSalesOverTime, getTopProducts } from "../api/client";
import type { DashboardFilters, KPIs, SalesOverTimePoint, TerritorySales, TopProduct } from "../api/types";
import { formatMonthLabel } from "../lib/format";
import { FilterBar } from "./FilterBar";
import { BarChartIcon, DollarSignIcon, ShoppingCartIcon, TrendingUpIcon, UsersIcon } from "./icons";
import { KPICard } from "./KPICard";
import { LineChartCard } from "./LineChartCard";
import { TerritoryChartCard } from "./TerritoryChartCard";
import { TopProductsTable } from "./TopProductsTable";

const INITIAL_FILTERS: DashboardFilters = { startDate: null, endDate: null, territoryId: null };

export function Dashboard() {
  const [filters, setFilters] = useState<DashboardFilters>(INITIAL_FILTERS);

  const [kpis, setKpis] = useState<KPIs | null>(null);
  const [salesOverTime, setSalesOverTime] = useState<SalesOverTimePoint[]>([]);
  const [topProducts, setTopProducts] = useState<TopProduct[]>([]);
  const [salesByTerritory, setSalesByTerritory] = useState<TerritorySales[]>([]);
  const [territoryOptions, setTerritoryOptions] = useState<TerritorySales[]>([]);

  // Starts true so the first paint shows chart skeletons instead of a flash
  // of "no data" before the initial fetch effect has a chance to run.
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Populates the territory dropdown once, from the unfiltered sales-by-territory
  // endpoint (there's no dedicated /api/territories endpoint yet). This means a
  // territory with zero all-time sales won't appear as a filter option.
  useEffect(() => {
    getSalesByTerritory(INITIAL_FILTERS)
      .then(setTerritoryOptions)
      .catch(() => {
        // Dropdown just stays empty — not worth a page-level error for this.
      });
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    Promise.all([
      getKpis(filters),
      getSalesOverTime(filters),
      getTopProducts(filters),
      getSalesByTerritory(filters),
    ])
      .then(([kpisResult, salesOverTimeResult, topProductsResult, salesByTerritoryResult]) => {
        if (cancelled) return;
        setKpis(kpisResult);
        setSalesOverTime(salesOverTimeResult);
        setTopProducts(topProductsResult);
        setSalesByTerritory(salesByTerritoryResult);
      })
      .catch((err: Error) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [filters]);

  return (
    <div className="min-h-svh bg-page">
      <header
        className="px-4 py-8 shadow-sm sm:px-6 sm:py-10 lg:px-8"
        style={{ background: "linear-gradient(120deg, #0b2545 0%, #12447f 55%, #0f7f58 130%)" }}
      >
        <div className="mx-auto flex max-w-6xl items-center gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-white/10 ring-1 ring-white/20">
            <BarChartIcon className="h-6 w-6 text-white" />
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-teal-100/80">AdventureWorks sales</p>
            <h1 className="mt-1 text-2xl font-bold tracking-tight text-white sm:text-3xl">SQL Analytics Dashboard</h1>
            <p className="mt-1 text-sm text-blue-100/80">
              KPIs, trends, and top performers across your sales territories.
            </p>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-10 px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
            Couldn't load dashboard data: {error}
          </div>
        )}

        {/* Summary — the first thing visible, so the headline numbers land before any filtering. */}
        <section aria-labelledby="overview-heading">
          <h2 id="overview-heading" className="text-xs font-semibold uppercase tracking-widest text-ink-muted">
            Overview
          </h2>
          <div className="mt-4 grid grid-cols-2 gap-4 sm:gap-5 md:grid-cols-4">
            <KPICard
              label="Total sales"
              value={kpis?.total_sales ?? 0}
              format="currency"
              loading={loading && kpis === null}
              icon={<DollarSignIcon />}
              tone="blue"
            />
            <KPICard
              label="Total orders"
              value={kpis?.total_orders ?? 0}
              loading={loading && kpis === null}
              icon={<ShoppingCartIcon />}
              tone="teal"
            />
            <KPICard
              label="Average order value"
              value={kpis?.average_order_value ?? 0}
              format="currency"
              loading={loading && kpis === null}
              icon={<TrendingUpIcon />}
              tone="blue"
            />
            <KPICard
              label="Total customers"
              value={kpis?.total_customers ?? 0}
              loading={loading && kpis === null}
              icon={<UsersIcon />}
              tone="teal"
            />
          </div>
        </section>

        <FilterBar
          startDate={filters.startDate}
          endDate={filters.endDate}
          territoryId={filters.territoryId}
          territories={territoryOptions.map((t) => ({ id: t.territory_id, name: t.territory_name }))}
          onStartDateChange={(startDate) => setFilters((f) => ({ ...f, startDate }))}
          onEndDateChange={(endDate) => setFilters((f) => ({ ...f, endDate }))}
          onTerritoryChange={(territoryId) => setFilters((f) => ({ ...f, territoryId }))}
        />

        <div className="grid grid-cols-1 gap-4 sm:gap-6 lg:grid-cols-2">
          <LineChartCard
            title="Sales over time"
            data={salesOverTime.map((point) => ({
              label: formatMonthLabel(point.period),
              value: point.total_sales,
            }))}
            loading={loading}
          />
          <TerritoryChartCard
            data={salesByTerritory.map((t) => ({ label: t.territory_name, value: t.total_sales }))}
            loading={loading}
          />
        </div>

        <TopProductsTable products={topProducts} loading={loading} />
      </main>
    </div>
  );
}
