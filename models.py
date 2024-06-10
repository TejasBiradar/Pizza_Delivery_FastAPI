from db.database import Base
from sqlalchemy import Column,Integer,Boolean,String,ForeignKey,Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, autoincrement=True)
    username = Column(String(50),unique=True)
    email = Column(String(50),unique=True)
    password = Column(Text,nullable=False)
    is_staff = Column(Boolean,default=False)
    is_active = Column(Boolean,default=False)

    orders = relationship("Order",back_populates="user")

    def __repr__(self):
        return f"Username : {self.username}"


class Order(Base):
    __tablename__ = "orders"


    order_status = (
        ("PENDING","pending"),
        ("IN-TRANSIT","in-transit"),
        ("DELIVERED","delivered")
    )

    pizza_sizes = (
        ("SMALL","small"),
        ("MEDIUM","medium"),
        ("LARGE","large"),
        ("EXTRA_LARGE","extra-large")
    )

    id = Column(Integer,primary_key=True, autoincrement=True)
    quantity = Column(Integer,nullable=False)
    order_status = Column(ChoiceType(choices=order_status),default="PENDING")
    pizza_size = Column(ChoiceType(choices=pizza_sizes),default="SMALL")
    user_id = Column(Integer,ForeignKey("users.id"))

    user = relationship("User",back_populates="orders")

    def __repr__(self):
        return f"id : {self.id}"

