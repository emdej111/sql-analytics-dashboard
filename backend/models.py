from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database import Base


class SalesTerritory(Base):
    __tablename__ = "sales_territories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    country_region_code = Column(String(10), nullable=False)
    group = Column(String(50), nullable=False)

    customers = relationship("Customer", back_populates="territory")
    orders = relationship("Order", back_populates="territory")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    territory_id = Column(Integer, ForeignKey("sales_territories.id"), nullable=False)

    territory = relationship("SalesTerritory", back_populates="customers")
    orders = relationship("Order", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    list_price = Column(Numeric(10, 2), nullable=False)

    order_details = relationship("OrderDetail", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    territory_id = Column(Integer, ForeignKey("sales_territories.id"), nullable=False)
    order_date = Column(Date, nullable=False, index=True)

    customer = relationship("Customer", back_populates="orders")
    territory = relationship("SalesTerritory", back_populates="orders")
    order_details = relationship(
        "OrderDetail", back_populates="order", cascade="all, delete-orphan"
    )


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    unit_price_discount = Column(Numeric(4, 3), nullable=False, default=0)

    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")
