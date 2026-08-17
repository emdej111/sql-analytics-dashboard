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

# Variant lists used to expand a single template into multiple SKUs.
FRAME_SIZES = ["44", "48", "52", "56", "58", "60"]
CLOTHING_SIZES = ["S", "M", "L", "XL", "XXL"]

# (name_template, category, price range, size variants or None for a single SKU)
PRODUCT_TEMPLATES = [
    # Bikes — few product lines, sold in multiple frame sizes.
    ("Mountain-{n}", "Bikes", (900, 2800), FRAME_SIZES),
    ("Road-{n}", "Bikes", (800, 2600), FRAME_SIZES),
    ("Touring-{n}", "Bikes", (700, 2200), FRAME_SIZES),

    # Components — many distinct parts, not sized like apparel.
    ("HL Road Frame", "Components", (300, 600), None),
    ("LL Road Frame", "Components", (150, 350), None),
    ("HL Mountain Frame", "Components", (300, 650), None),
    ("LL Mountain Frame", "Components", (150, 380), None),
    ("Chainring Bolts", "Components", (5, 15), None),
    ("Chainring Nut", "Components", (3, 8), None),
    ("Chainring", "Components", (20, 60), None),
    ("Crown Race", "Components", (10, 25), None),
    ("Front Derailleur", "Components", (40, 120), None),
    ("Rear Derailleur", "Components", (50, 150), None),
    ("ML Mountain Handlebars", "Components", (60, 130), None),
    ("HL Mountain Handlebars", "Components", (80, 160), None),
    ("Road Handlebars", "Components", (50, 110), None),
    ("Mountain Crankset", "Components", (90, 220), None),
    ("Road Crankset", "Components", (100, 260), None),
    ("Chain", "Components", (15, 40), None),
    ("Cassette", "Components", (40, 100), None),
    ("Freewheel", "Components", (30, 70), None),
    ("Front Brakes", "Components", (30, 80), None),
    ("Rear Brakes", "Components", (30, 80), None),
    ("Headset", "Components", (20, 60), None),
    ("Bottom Bracket", "Components", (25, 70), None),
    ("Seat Post", "Components", (20, 55), None),
    ("Road Pedal", "Components", (30, 80), None),
    ("Mountain Pedal", "Components", (30, 80), None),
    ("Spokes", "Components", (2, 6), None),
    ("Wheel Hub", "Components", (15, 45), None),
    ("Rim", "Components", (25, 65), None),
    ("Fork", "Components", (60, 150), None),
    ("Shift Lever", "Components", (20, 55), None),
    ("Brake Lever", "Components", (15, 45), None),
    ("Cable Housing Set", "Components", (10, 25), None),
    ("Freehub Body", "Components", (20, 50), None),
    ("Quick Release Skewer", "Components", (10, 25), None),
    ("Valve Stem", "Components", (2, 5), None),

    # Clothing — sized apparel.
    ("Short-Sleeve Classic Jersey", "Clothing", (40, 70), CLOTHING_SIZES),
    ("Long-Sleeve Logo Jersey", "Clothing", (45, 80), CLOTHING_SIZES),
    ("Long-Sleeve Tricot Jersey", "Clothing", (45, 85), CLOTHING_SIZES),
    ("Bike Shorts", "Clothing", (50, 90), CLOTHING_SIZES),
    ("Bib-Shorts", "Clothing", (55, 95), CLOTHING_SIZES),
    ("Classic Vest", "Clothing", (35, 65), CLOTHING_SIZES),

    # Accessories — many distinct SKUs, not sized.
    ("Sport-100 Helmet", "Accessories", (25, 45), None),
    ("Logo Cap", "Accessories", (8, 15), None),
    ("Water Bottle", "Accessories", (5, 10), None),
    ("Bottle Cage", "Accessories", (8, 20), None),
    ("Patch Kit", "Accessories", (3, 8), None),
    ("Mountain Tire", "Accessories", (20, 45), None),
    ("Road Tire", "Accessories", (15, 35), None),
    ("Touring Tire", "Accessories", (18, 40), None),
    ("Bike Lock", "Accessories", (25, 60), None),
    ("Cable Lock", "Accessories", (15, 35), None),
    ("Mountain Pump", "Accessories", (15, 35), None),
    ("Road Pump", "Accessories", (15, 35), None),
    ("Frame Pump", "Accessories", (12, 30), None),
    ("Hydration Pack", "Accessories", (20, 50), None),
    ("Fender Set", "Accessories", (15, 40), None),
    ("Kickstand", "Accessories", (10, 25), None),
    ("Bike Bag", "Accessories", (20, 55), None),
    ("Saddle Bag", "Accessories", (12, 30), None),
    ("Panniers", "Accessories", (40, 90), None),
    ("Tail Light", "Accessories", (10, 25), None),
    ("Head Light", "Accessories", (15, 35), None),
    ("Reflector Kit", "Accessories", (5, 15), None),
    ("Tool Kit", "Accessories", (15, 40), None),
    ("Multi-Tool", "Accessories", (10, 25), None),
    ("Tire Levers", "Accessories", (3, 8), None),
    ("Chain Tool", "Accessories", (8, 20), None),
    ("Bike Computer", "Accessories", (25, 70), None),
    ("Handlebar Tape", "Accessories", (8, 20), None),
    ("Toe Clips", "Accessories", (10, 25), None),
    ("Bar Ends", "Accessories", (10, 25), None),
    ("Half-Finger Gloves", "Accessories", (15, 30), None),
    ("Cycling Socks", "Accessories", (8, 15), None),
    ("Cycling Sunglasses", "Accessories", (20, 55), None),
    ("Saddle", "Accessories", (30, 90), None),
    ("Bike Cover", "Accessories", (15, 40), None),
]

NUM_CUSTOMERS = 300
NUM_ORDERS = 2000
ORDER_DATE_START = date.today() - timedelta(days=730)  # 2 years of history
ORDER_DATE_END = date.today()


def make_products() -> list[Product]:
    products = []
    for name_template, category, (low, high), sizes in PRODUCT_TEMPLATES:
        variants = sizes if sizes else [None]
        for size in variants:
            if size is None:
                name = name_template
            elif "{n}" in name_template:
                name = name_template.format(n=size)
            else:
                name = f"{name_template} - {size}"
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
