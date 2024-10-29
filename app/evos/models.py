from typing import List

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.repository.base import Base


class Category(Base):

    name: Mapped[str] = mapped_column(String(256), index=True)

    # id dish - Many to one
    dishes: Mapped[List["Dish"]] = relationship("Dish", back_populates="category")


class Dish(Base):
    name: Mapped[str] = mapped_column(String(256), index=True)
    price: Mapped[int] = mapped_column(Integer)

    # id category -  Many to one
    category: Mapped[Category] = relationship("Category", back_populates="dishes")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))

    # id cart - Many to one
    cart: Mapped["Cart"] = relationship("Cart", back_populates="dishes")
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id"), nullable=True)

    # id order_items - Many to one
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="dish")


class Cart(Base):

    quantity: Mapped[int] = mapped_column(Integer, nullable=True)

    # user id - one to one
    user: Mapped["User"] = relationship("User", back_populates="cart")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    # dish id - One to many
    dishes: Mapped[List["Dish"]] = relationship("Dish", back_populates="cart")


class Order(Base):

    # user id - Many to one
    user: Mapped["User"] = relationship("User", back_populates="orders")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    # orderItems - Many to one
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(Base):

    quantity: Mapped[int] = mapped_column(Integer)

    # dish id - One to many
    dish: Mapped["Dish"] = relationship("Dish", back_populates="order_items")
    dish_id: Mapped[int] = mapped_column(Integer, ForeignKey("dishes.id"))

    # order id - One to many
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
