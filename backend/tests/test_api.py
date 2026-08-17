"""
Tests for every API endpoint in main.py, run against a seeded Postgres
test database (see conftest.py for fixture data and expected totals).
"""

import pytest


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# /api/kpis
# ---------------------------------------------------------------------------


def test_kpis_structure_and_values_all_time(client):
    response = client.get("/api/kpis")
    assert response.status_code == 200
    body = response.json()

    assert set(body.keys()) == {"total_sales", "total_orders", "average_order_value", "total_customers"}
    assert isinstance(body["total_sales"], float)
    assert isinstance(body["total_orders"], int)
    assert isinstance(body["average_order_value"], float)
    assert isinstance(body["total_customers"], int)

    assert body["total_sales"] == 53.5
    assert body["total_orders"] == 3
    assert body["average_order_value"] == 17.83
    assert body["total_customers"] == 2


def test_kpis_date_range_filters_to_january(client):
    response = client.get("/api/kpis", params={"start_date": "2024-01-01", "end_date": "2024-01-31"})
    assert response.status_code == 200
    body = response.json()

    assert body["total_sales"] == 20.0
    assert body["total_orders"] == 1
    assert body["average_order_value"] == 20.0
    assert body["total_customers"] == 1


def test_kpis_date_range_filters_to_february(client):
    response = client.get("/api/kpis", params={"start_date": "2024-02-01", "end_date": "2024-02-29"})
    assert response.status_code == 200
    body = response.json()

    assert body["total_sales"] == 33.5
    assert body["total_orders"] == 2
    assert body["average_order_value"] == 16.75
    assert body["total_customers"] == 2


def test_kpis_only_start_date(client):
    response = client.get("/api/kpis", params={"start_date": "2024-02-01"})
    assert response.status_code == 200
    body = response.json()

    assert body["total_sales"] == 33.5
    assert body["total_orders"] == 2


def test_kpis_only_end_date(client):
    response = client.get("/api/kpis", params={"end_date": "2024-01-31"})
    assert response.status_code == 200
    body = response.json()

    assert body["total_sales"] == 20.0
    assert body["total_orders"] == 1


def test_kpis_empty_range_returns_zeroed_response(client):
    response = client.get("/api/kpis", params={"start_date": "2025-01-01", "end_date": "2025-01-31"})
    assert response.status_code == 200
    body = response.json()

    assert body["total_sales"] == 0.0
    assert body["total_orders"] == 0
    assert body["average_order_value"] == 0.0
    assert body["total_customers"] == 0


def test_kpis_invalid_date_range_returns_400(client):
    response = client.get("/api/kpis", params={"start_date": "2024-02-01", "end_date": "2024-01-01"})
    assert response.status_code == 400
    assert "start_date" in response.json()["detail"]


# ---------------------------------------------------------------------------
# /api/sales-over-time
# ---------------------------------------------------------------------------


def test_sales_over_time_structure_and_values(client):
    response = client.get("/api/sales-over-time")
    assert response.status_code == 200
    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 2
    for point in body:
        assert set(point.keys()) == {"period", "total_sales"}
        assert isinstance(point["period"], str)
        assert isinstance(point["total_sales"], float)

    assert body[0] == {"period": "2024-01-01", "total_sales": 20.0}
    assert body[1] == {"period": "2024-02-01", "total_sales": 33.5}


def test_sales_over_time_date_range_filtering(client):
    response = client.get(
        "/api/sales-over-time",
        params={"start_date": "2024-02-01", "end_date": "2024-02-29"},
    )
    assert response.status_code == 200
    body = response.json()

    assert body == [{"period": "2024-02-01", "total_sales": 33.5}]


def test_sales_over_time_territory_filter(client, territory_ids):
    response = client.get("/api/sales-over-time", params={"territory_id": territory_ids["North"]})
    assert response.status_code == 200
    body = response.json()

    assert body == [
        {"period": "2024-01-01", "total_sales": 20.0},
        {"period": "2024-02-01", "total_sales": 20.0},
    ]


def test_sales_over_time_week_granularity_accepted(client):
    response = client.get("/api/sales-over-time", params={"granularity": "week"})
    assert response.status_code == 200
    body = response.json()

    assert isinstance(body, list)
    for point in body:
        assert set(point.keys()) == {"period", "total_sales"}


def test_sales_over_time_invalid_granularity_returns_422(client):
    response = client.get("/api/sales-over-time", params={"granularity": "year"})
    assert response.status_code == 422


def test_sales_over_time_empty_range_returns_empty_list(client):
    response = client.get(
        "/api/sales-over-time",
        params={"start_date": "2025-01-01", "end_date": "2025-01-31"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_sales_over_time_invalid_date_range_returns_400(client):
    response = client.get(
        "/api/sales-over-time",
        params={"start_date": "2024-02-01", "end_date": "2024-01-01"},
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# /api/top-products
# ---------------------------------------------------------------------------


def test_top_products_structure_and_values(client):
    response = client.get("/api/top-products")
    assert response.status_code == 200
    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 2
    for product in body:
        assert set(product.keys()) == {"product_id", "product_name", "category", "total_revenue", "units_sold"}
        assert isinstance(product["product_id"], int)
        assert isinstance(product["product_name"], str)
        assert isinstance(product["category"], str)
        assert isinstance(product["total_revenue"], float)
        assert isinstance(product["units_sold"], int)

    # Ordered by revenue descending: Widget (30.00) before Gadget (23.50).
    assert body[0]["product_name"] == "Widget"
    assert body[0]["total_revenue"] == 30.0
    assert body[0]["units_sold"] == 3
    assert body[1]["product_name"] == "Gadget"
    assert body[1]["total_revenue"] == 23.5
    assert body[1]["units_sold"] == 5


def test_top_products_date_range_filtering(client):
    response = client.get(
        "/api/top-products",
        params={"start_date": "2024-01-01", "end_date": "2024-01-31"},
    )
    assert response.status_code == 200
    body = response.json()

    assert len(body) == 1
    assert body[0]["product_name"] == "Widget"
    assert body[0]["total_revenue"] == 20.0
    assert body[0]["units_sold"] == 2


def test_top_products_limit_parameter(client):
    response = client.get("/api/top-products", params={"limit": 1})
    assert response.status_code == 200
    body = response.json()

    assert len(body) == 1
    assert body[0]["product_name"] == "Widget"


def test_top_products_limit_out_of_range_returns_422(client):
    assert client.get("/api/top-products", params={"limit": 0}).status_code == 422
    assert client.get("/api/top-products", params={"limit": 101}).status_code == 422


def test_top_products_empty_range_returns_empty_list(client):
    response = client.get(
        "/api/top-products",
        params={"start_date": "2025-01-01", "end_date": "2025-01-31"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_top_products_invalid_date_range_returns_400(client):
    response = client.get(
        "/api/top-products",
        params={"start_date": "2024-02-01", "end_date": "2024-01-01"},
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# /api/sales-by-territory
# ---------------------------------------------------------------------------


def test_sales_by_territory_structure_and_values(client):
    response = client.get("/api/sales-by-territory")
    assert response.status_code == 200
    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 2
    for territory in body:
        assert set(territory.keys()) == {"territory_id", "territory_name", "total_sales"}
        assert isinstance(territory["territory_id"], int)
        assert isinstance(territory["territory_name"], str)
        assert isinstance(territory["total_sales"], float)

    # Ordered by total_sales descending: North (40.00) before South (13.50).
    assert body[0]["territory_name"] == "North"
    assert body[0]["total_sales"] == 40.0
    assert body[1]["territory_name"] == "South"
    assert body[1]["total_sales"] == 13.5


def test_sales_by_territory_date_range_filtering(client):
    response = client.get(
        "/api/sales-by-territory",
        params={"start_date": "2024-02-01", "end_date": "2024-02-29"},
    )
    assert response.status_code == 200
    body = response.json()

    # Only order2 (South) and order3 (North) fall in February.
    by_name = {row["territory_name"]: row["total_sales"] for row in body}
    assert by_name == {"North": 20.0, "South": 13.5}


def test_sales_by_territory_empty_range_returns_empty_list(client):
    response = client.get(
        "/api/sales-by-territory",
        params={"start_date": "2025-01-01", "end_date": "2025-01-31"},
    )
    assert response.status_code == 200
    assert response.json() == []


def test_sales_by_territory_invalid_date_range_returns_400(client):
    response = client.get(
        "/api/sales-by-territory",
        params={"start_date": "2024-02-01", "end_date": "2024-01-01"},
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Cross-endpoint edge cases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path",
    ["/api/kpis", "/api/sales-over-time", "/api/top-products", "/api/sales-by-territory"],
)
def test_malformed_date_returns_422(client, path):
    response = client.get(path, params={"start_date": "not-a-date"})
    assert response.status_code == 422
