"""
Shared fixtures for the API test suite.

Tests run against a real, disposable Postgres database (created on the same
server as DATABASE_URL, suffixed "_test") rather than SQLite, because the
endpoints rely on Postgres-specific SQL (func.date_trunc).

The API is read-only (GET endpoints only), so fixture data is seeded once
per test session and reused across every test.
"""

import os
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402
from models import Customer, Order, OrderDetail, Product, SalesTerritory  # noqa: E402

BASE_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/adventureworks_dashboard",
)
_base_url = make_url(BASE_DATABASE_URL)
TEST_DATABASE_URL = _base_url.set(database=f"{_base_url.database}_test")

# Fixture data — kept small and hand-computable so expected totals below
# can be verified by eye.
#
#   order1: 2024-01-15, North, customer Ann  -> Widget x2 @ 10.00        = 20.00
#   order2: 2024-02-10, South, customer Bo   -> Gadget x3 @ 5.00 (10%)   = 13.50
#   order3: 2024-02-20, North, customer Ann  -> Widget x1 @ 10.00        = 10.00
#                                              + Gadget x2 @ 5.00        = 10.00
#                                                                 (order total = 20.00)
#
# Totals:
#   All time:  total_sales=53.50 total_orders=3 avg=17.83 total_customers=2
#   Jan 2024:  total_sales=20.00 total_orders=1 avg=20.00 total_customers=1
#   Feb 2024:  total_sales=33.50 total_orders=2 avg=16.75 total_customers=2
#   Top products (all time): Widget revenue=30.00 units=3, Gadget revenue=23.50 units=5
#   By territory (all time): North=40.00, South=13.50
#   By month: 2024-01-01=20.00, 2024-02-01=33.50


def _create_test_database() -> None:
    admin_url = _base_url.set(database="postgres")
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    test_db_name = TEST_DATABASE_URL.database
    with admin_engine.connect() as conn:
        conn.execute(text(f'DROP DATABASE IF EXISTS "{test_db_name}" WITH (FORCE)'))
        conn.execute(text(f'CREATE DATABASE "{test_db_name}"'))
    admin_engine.dispose()


@pytest.fixture(scope="session")
def engine():
    _create_test_database()
    test_engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(test_engine)
    yield test_engine
    test_engine.dispose()


@pytest.fixture(scope="session")
def session_factory(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def territory_ids(session_factory, seed_data):
    db = session_factory()
    try:
        rows = db.query(SalesTerritory.name, SalesTerritory.id).all()
        return {name: territory_id for name, territory_id in rows}
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def seed_data(session_factory):
    db = session_factory()
    try:
        north = SalesTerritory(name="North", country_region_code="US", group="NA")
        south = SalesTerritory(name="South", country_region_code="US", group="NA")
        db.add_all([north, south])
        db.flush()

        widget = Product(name="Widget", category="A", list_price=Decimal("10.00"))
        gadget = Product(name="Gadget", category="B", list_price=Decimal("5.00"))
        db.add_all([widget, gadget])
        db.flush()

        ann = Customer(first_name="Ann", last_name="Lee", email="ann@example.com", territory=north)
        bo = Customer(first_name="Bo", last_name="Kim", email="bo@example.com", territory=south)
        db.add_all([ann, bo])
        db.flush()

        order1 = Order(customer=ann, territory=north, order_date=date(2024, 1, 15))
        order1.order_details.append(
            OrderDetail(product=widget, quantity=2, unit_price=Decimal("10.00"), unit_price_discount=Decimal("0"))
        )

        order2 = Order(customer=bo, territory=south, order_date=date(2024, 2, 10))
        order2.order_details.append(
            OrderDetail(product=gadget, quantity=3, unit_price=Decimal("5.00"), unit_price_discount=Decimal("0.1"))
        )

        order3 = Order(customer=ann, territory=north, order_date=date(2024, 2, 20))
        order3.order_details.append(
            OrderDetail(product=widget, quantity=1, unit_price=Decimal("10.00"), unit_price_discount=Decimal("0"))
        )
        order3.order_details.append(
            OrderDetail(product=gadget, quantity=2, unit_price=Decimal("5.00"), unit_price_discount=Decimal("0"))
        )

        db.add_all([order1, order2, order3])
        db.commit()
    finally:
        db.close()


@pytest.fixture()
def client(session_factory):
    def _get_test_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
