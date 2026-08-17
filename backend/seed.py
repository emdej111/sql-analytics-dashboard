"""
Seeds the adventureworks_dashboard database with a realistic-but-synthetic
sample dataset, styled after Microsoft's AdventureWorks sample (bikes,
components, clothing, accessories sold across sales territories).

Usage:
    venv/bin/python3 seed.py
"""

import random
from datetime import date, timedelta
from decimal import Decimal

from faker import Faker

from database import Base, SessionLocal, engine
from models import Customer, Order, OrderDetail, Product, SalesTerritory

fake = Faker()
Faker.seed(42)
random.seed(42)

# Matches the real AdventureWorks SalesLT.SalesTerritory table.
TERRITORIES = [
    ("Northwest", "US", "North America"),
    ("Northeast", "US", "North America"),
    ("Central", "US", "North America"),
    ("Southwest", "US", "North America"),
    ("Southeast", "US", "North America"),
    ("Canada", "CA", "North America"),
    ("France", "FR", "Europe"),
    ("Germany", "DE", "Europe"),
    ("United Kingdom", "GB", "Europe"),
    ("Australia", "AU", "Pacific"),
]

# (name, category, price range)
PRODUCT_TEMPLATES = [
    ("Mountain-{n}", "Bikes", (900, 2800)),
    ("Road-{n}", "Bikes", (800, 2600)),
    ("Touring-{n}", "Bikes", (700, 2200)),
    ("HL Road Frame", "Components", (300, 600)),
    ("LL Road Frame", "Components", (150, 350)),
    ("Chainring Bolts", "Components", (5, 15)),
    ("Front Derailleur", "Components", (40, 120)),
    ("Rear Derailleur", "Components", (50, 150)),
    ("ML Mountain Handlebars", "Components", (60, 130)),
    ("Short-Sleeve Classic Jersey", "Clothing", (40, 70)),
    ("Long-Sleeve Logo Jersey", "Clothing", (45, 80)),
    ("Bike Shorts", "Clothing", (50, 90)),
    ("Full-Finger Gloves", "Clothing", (20, 40)),
    ("Sport-100 Helmet", "Accessories", (25, 45)),
    ("Water Bottle", "Accessories", (5, 10)),
    ("Bottle Cage", "Accessories", (8, 20)),
    ("Patch Kit", "Accessories", (3, 8)),
    ("Mountain Tire", "Accessories", (20, 45)),
    ("Road Tire", "Accessories", (15, 35)),
    ("Bike Lock", "Accessories", (25, 60)),
]
SIZES = ["38", "40", "42", "44", "48", "52", "56", "58", "60", "62"]

NUM_CUSTOMERS = 300
NUM_ORDERS = 2000
ORDER_DATE_START = date.today() - timedelta(days=730)  # 2 years of history
ORDER_DATE_END = date.today()


def make_products() -> list[Product]:
    products = []
    for name_template, category, (low, high) in PRODUCT_TEMPLATES:
        variants = SIZES[:6] if "{n}" in name_template else [None]
        for variant in variants:
            name = name_template.format(n=variant) if variant else name_template
            price = Decimal(random.randint(low * 100, high * 100)) / 100
            products.append(Product(name=name, category=category, list_price=price))
    return products


def make_customers(territories: list[SalesTerritory]) -> list[Customer]:
    customers = []
    seen_emails = set()
    for _ in range(NUM_CUSTOMERS):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        seen_emails.add(email)
        customers.append(
            Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                territory=random.choice(territories),
            )
        )
    return customers


def random_order_date() -> date:
    span_days = (ORDER_DATE_END - ORDER_DATE_START).days
    return ORDER_DATE_START + timedelta(days=random.randint(0, span_days))


def make_orders(customers: list[Customer], products: list[Product]) -> list[Order]:
    orders = []
    for _ in range(NUM_ORDERS):
        customer = random.choice(customers)
        order = Order(
            customer=customer,
            territory=customer.territory,
            order_date=random_order_date(),
        )
        for product in random.sample(products, k=random.randint(1, 5)):
            quantity = random.randint(1, 6)
            discount = random.choice([0, 0, 0, 0.05, 0.1, 0.15])
            order.order_details.append(
                OrderDetail(
                    product=product,
                    quantity=quantity,
                    unit_price=product.list_price,
                    unit_price_discount=Decimal(str(discount)),
                )
            )
        orders.append(order)
    return orders


def main() -> None:
    print(f"Creating tables on {engine.url.render_as_string(hide_password=True)} ...")
    Base.metadata.create_all(engine)

    db = SessionLocal()
    try:
        if db.query(Order).first() is not None:
            print("Database already has orders — skipping seed. "
                  "Drop the tables first if you want to reseed.")
            return

        print("Seeding sales territories...")
        territories = [
            SalesTerritory(name=name, country_region_code=code, group=group)
            for name, code, group in TERRITORIES
        ]
        db.add_all(territories)
        db.flush()  # assigns territory.id without committing yet

        print("Seeding products...")
        products = make_products()
        db.add_all(products)
        db.flush()

        print(f"Seeding {NUM_CUSTOMERS} customers...")
        customers = make_customers(territories)
        db.add_all(customers)
        db.flush()

        print(f"Seeding {NUM_ORDERS} orders with line items...")
        orders = make_orders(customers, products)
        db.add_all(orders)

        db.commit()
        print(
            f"Done: {len(territories)} territories, {len(products)} products, "
            f"{len(customers)} customers, {len(orders)} orders."
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
