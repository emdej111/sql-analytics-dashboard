// Mirrors backend/schemas.py — keep these in sync with the FastAPI response_models.

export interface KPIs {
  total_sales: number;
  total_orders: number;
  average_order_value: number;
  total_customers: number;
}

export interface SalesOverTimePoint {
  period: string; // ISO date, first day of the bucket (week or month)
  total_sales: number;
}

export interface TopProduct {
  product_id: number;
  product_name: string;
  category: string;
  total_revenue: number;
  units_sold: number;
}

export interface TerritorySales {
  territory_id: number;
  territory_name: string;
  total_sales: number;
}

export interface CategorySales {
  category: string;
  total_sales: number;
}

export interface DashboardFilters {
  startDate: string | null; // YYYY-MM-DD
  endDate: string | null;
  territoryId: number | null;
}
