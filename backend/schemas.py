from pydantic import BaseModel


class KPIResponse(BaseModel):
    total_sales: float
    total_orders: int
    average_order_value: float
    total_customers: int


class SalesOverTimePoint(BaseModel):
    period: str
    total_sales: float


class TopProduct(BaseModel):
    product_id: int
    product_name: str
    category: str
    total_revenue: float
    units_sold: int


class TerritorySales(BaseModel):
    territory_id: int
    territory_name: str
    total_sales: float
