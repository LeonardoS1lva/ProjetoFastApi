from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///models/database.db")

Base = declarative_base()

# Vercel
Base.metadata.create_all(db)

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String) 
    status = Column("status", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, status=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.admin = admin

class Order(Base):
    __tablename__ = "orders"

    # ORDERS_STATUS = (
    #     ("PENDING", "PENDING"),
    #     ("CANCELLED", "CANCELLED"),
    #     ("COMPLETED", "COMPLETED")
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    user = Column("user", ForeignKey("users.id"))
    price = Column("price", Float)
    items = relationship("OrderItem", cascade="all, delete")

    def __init__(self, user, status="PENDING", price=0):
        self.user = user
        self.price = price
        self.status = status

    def calc_price(self):
        # order_price = 0
        # for item in self.items:
        #     item_price = item.unit_price * item.count
        #     order_price += item_price
        self.price = sum(item.unit_price * item.count for item in self.items)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    count = Column("count", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, count, flavor, size, unit_price, order):
        self.count = count
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order