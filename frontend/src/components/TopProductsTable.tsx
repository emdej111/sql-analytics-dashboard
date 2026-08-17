import type { TopProduct } from "../api/types";
import { formatCompactNumber, formatCurrency } from "../lib/format";
import { ChartEmptyState } from "./ChartEmptyState";

interface TopProductsTableProps {
  products: TopProduct[];
  loading?: boolean;
}

const SKELETON_ROWS = 5;

export function TopProductsTable({ products, loading }: TopProductsTableProps) {
  const isEmpty = products.length === 0;
  const showSkeleton = loading && isEmpty;
  const showEmptyState = !loading && isEmpty;

  return (
    <div className="rounded-xl border border-line bg-surface p-5 shadow-sm sm:p-6">
      <h2 className="text-base font-semibold tracking-tight text-ink">Top products by revenue</h2>
      <p className="mt-1 text-xs text-ink-muted">
        Ranked by total revenue, so higher-priced categories like Bikes naturally dominate this list. See{" "}
        <span className="font-medium text-ink-secondary">Revenue by category</span> above for the fuller picture
        across all categories.
      </p>
      <div className={`mt-4 transition-opacity ${loading && !isEmpty ? "opacity-50" : "opacity-100"}`}>
        {showSkeleton && <TableSkeleton />}
        {showEmptyState && (
          <div className="h-24">
            <ChartEmptyState />
          </div>
        )}
        {!showSkeleton && !showEmptyState && (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[28rem] text-sm">
              <thead>
                <tr className="rounded-lg bg-surface-alt text-left text-xs font-semibold uppercase tracking-wide text-ink-muted">
                  <th className="rounded-l-lg py-2.5 pl-3 font-semibold">Product</th>
                  <th className="py-2.5 font-semibold">Category</th>
                  <th className="py-2.5 pr-1 text-right font-semibold">Units sold</th>
                  <th className="rounded-r-lg py-2.5 pr-3 pl-1 text-right font-semibold">Revenue</th>
                </tr>
              </thead>
              <tbody className="[font-variant-numeric:tabular-nums]">
                {products.map((product) => (
                  <tr
                    key={product.product_id}
                    className="border-b border-line/60 transition-colors last:border-0 hover:bg-surface-alt"
                  >
                    <td className="py-2.5 pl-3 font-medium text-ink">{product.product_name}</td>
                    <td className="py-2.5">
                      <span className="inline-flex rounded-full bg-teal-soft px-2 py-0.5 text-xs font-medium text-teal-dark">
                        {product.category}
                      </span>
                    </td>
                    <td className="py-2.5 pr-1 text-right text-ink-secondary">
                      {formatCompactNumber(product.units_sold)}
                    </td>
                    <td className="py-2.5 pr-3 pl-1 text-right font-semibold text-accent">
                      {formatCurrency(product.total_revenue)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

function TableSkeleton() {
  return (
    <div className="animate-pulse space-y-2" aria-hidden="true">
      {Array.from({ length: SKELETON_ROWS }).map((_, index) => (
        <div key={index} className="h-6 rounded bg-line/60" />
      ))}
    </div>
  );
}
