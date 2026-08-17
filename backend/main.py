from datetime import date
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import schemas
from database import get_db
from models import Customer, Order, OrderDetail, Product, SalesTerritory

app = FastAPI(title="SQL Analytics Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(SQLAlchemyError)
def handle_db_error(request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=503,
        content={"detail": "Database is unavailable. Please try again later."},
    )


# quantity * unit_price * (1 - discount) — revenue for a single order line.
# Reused across every endpoint so "revenue" is calculated the same way everywhere.
LINE_TOTAL = OrderDetail.quantity * OrderDetail.unit_price * (1 - OrderDetail.unit_price_discount)


def _validate_date_range(start_date: date | None, end_date: date | None) -> None:
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be on or before end_date")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/kpis", response_model=schemas.KPIResponse)
def get_kpis(
    start_date: date | None = Query(None, description="Inclusive lower bound on order_date"),
    end_date: date | None = Query(None, description="Inclusive upper bound on order_date"),
    db: Session = Depends(get_db),
):
    _validate_date_range(start_date, end_date)

    sales_query = (
        db.query(
            func.coalesce(func.sum(LINE_TOTAL), 0).label("total_sales"),
            func.count(func.distinct(Order.id)).label("total_orders"),
        )
        .select_from(Order)
        .join(OrderDetail, OrderDetail.order_id == Order.id)
    )
    if start_date:
        sales_query = sales_query.filter(Order.order_date >= start_date)
    if end_date:
        sales_query = sales_query.filter(Order.order_date <= end_date)

    result = sales_query.one()
    total_sales = float(result.total_sales)
    total_orders = result.total_orders
    average_order_value = total_sales / total_orders if total_orders else 0.0

    if start_date or end_date:
        customers_query = db.query(func.count(func.distinct(Order.customer_id))).select_from(Order)
        if start_date:
            customers_query = customers_query.filter(Order.order_date >= start_date)
        if end_date:
            customers_query = customers_query.filter(Order.order_date <= end_date)
        total_customers = customers_query.scalar()
    else:
        total_customers = db.query(func.count(Customer.id)).scalar()

    return schemas.KPIResponse(
        total_sales=round(total_sales, 2),
        total_orders=total_orders,
        average_order_value=round(average_order_value, 2),
        total_customers=total_customers,
    )


@app.get("/api/sales-over-time", response_model=list[schemas.SalesOverTimePoint])
def get_sales_over_time(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    territory_id: int | None = Query(None),
    granularity: Literal["week", "month"] = Query("month"),
    db: Session = Depends(get_db),
):
    _validate_date_range(start_date, end_date)

    period = func.date_trunc(granularity, Order.order_date).label("period")

    query = (
        db.query(period, func.sum(LINE_TOTAL).label("total_sales"))
        .select_from(Order)
        .join(OrderDetail, OrderDetail.order_id == Order.id)
        .group_by(period)
        .order_by(period)
    )
    if start_date:
        query = query.filter(Order.order_date >= start_date)
    if end_date:
        query = query.filter(Order.order_date <= end_date)
    if territory_id:
        query = query.filter(Order.territory_id == territory_id)

    return [
        schemas.SalesOverTimePoint(
            period=row.period.date().isoformat(),
            total_sales=round(float(row.total_sales), 2),
        )
        for row in query.all()
    ]


@app.get("/api/top-products", response_model=list[schemas.TopProduct])
def get_top_products(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    _validate_date_range(start_date, end_date)

    query = (
        db.query(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Product.category.label("category"),
            func.sum(LINE_TOTAL).label("total_revenue"),
            func.sum(OrderDetail.quantity).label("units_sold"),
        )
        .select_from(Product)
        .join(OrderDetail, OrderDetail.product_id == Product.id)
        .join(Order, Order.id == OrderDetail.order_id)
        .group_by(Product.id, Product.name, Product.category)
        .order_by(func.sum(LINE_TOTAL).desc())
    )
    if start_date:
        query = query.filter(Order.order_date >= start_date)
    if end_date:
        query = query.filter(Order.order_date <= end_date)
    query = query.limit(limit)

    return [
        schemas.TopProduct(
            product_id=row.product_id,
            product_name=row.product_name,
            category=row.category,
            total_revenue=round(float(row.total_revenue), 2),
            units_sold=int(row.units_sold),
        )
        for row in query.all()
    ]


@app.get("/api/sales-by-territory", response_model=list[schemas.TerritorySales])
def get_sales_by_territory(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
):
    _validate_date_range(start_date, end_date)

    query = (
        db.query(
            SalesTerritory.id.label("territory_id"),
            SalesTerritory.name.label("territory_name"),
            func.sum(LINE_TOTAL).label("total_sales"),
        )
        .select_from(SalesTerritory)
        .join(Order, Order.territory_id == SalesTerritory.id)
        .join(OrderDetail, OrderDetail.order_id == Order.id)
        .group_by(SalesTerritory.id, SalesTerritory.name)
        .order_by(func.sum(LINE_TOTAL).desc())
    )
    if start_date:
        query = query.filter(Order.order_date >= start_date)
    if end_date:
        query = query.filter(Order.order_date <= end_date)

    return [
        schemas.TerritorySales(
            territory_id=row.territory_id,
            territory_name=row.territory_name,
            total_sales=round(float(row.total_sales), 2),
        )
        for row in query.all()
    ]
