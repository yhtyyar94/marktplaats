from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float
from db.database import Base
from sqlalchemy import Column
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    books = relationship("Book", back_populates="owner")
    order_history = relationship("Order", back_populates="buyer")
    shopping_cart = relationship("ShoppingCart", back_populates="owner")
    reviews = relationship("Review", back_populates="user")
    reports = relationship("Report", back_populates="user")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    genre = Column(String)
    image_url = Column(String)
    condition = Column(String, default="New")
    price = Column(Float)
    isbn = Column(String)
    published_date = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="books")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))
    book = relationship("Book")
    buyer = relationship("User", back_populates="order_history")
    is_delivered = Column(Boolean, default=False)
    order_date = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    book = relationship("Book")
    owner = relationship("User", back_populates="shopping_cart")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    rating = Column(Integer)
    comment = Column(String)
    user = relationship("User", back_populates="reviews")
    book = relationship("Book")


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    reason = Column(String)
    user = relationship("User", back_populates="reports")
    book = relationship("Book")
