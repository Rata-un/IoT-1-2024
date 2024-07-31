from sqlalchemy import Boolean, ForeignKey ,Column, Integer, String, Date, CHAR, DateTime, Float
from sqlalchemy.orm import relationship, Mapped
from database import Base
from typing import List
import pytz
from database import Base
import datetime


bkk_timezone = pytz.timezone('Asia/Bangkok')

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)
    detail = Column(String, index=True)
    synopsis = Column(String, index=True)
    category = Column(String, index=True)
    image = Column(String, index=True)

class Students(Base):
    __tablename__ = 'students'

    stu_id = Column(String, primary_key=True, index=True)
    fname = Column(String, index=True)
    lname = Column(String, index=True)
    dob = Column(Date, index=True)
    gender = Column(CHAR, index=True)

class Beverages(Base):
    __tablename__ = 'berverages'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float, index=True)
    menuImage = Column(String, index=True)
    
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.now(tz=bkk_timezone))
    description = Column(String, index=True)
    total_price = Column(Float, nullable=False)
    order_items:Mapped[List["OrderItem"]]  = relationship(back_populates="order",lazy='joined', cascade="all, delete")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer,ForeignKey("orders.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("berverages.id"), nullable=False)
    quantity = Column(Integer, index=True)
    price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    order: Mapped["Order"] = relationship("Order", back_populates="order_items" , cascade="all, delete")
    menu : Mapped["Beverages"]= relationship("Beverages", backref="order_items",lazy='joined')
    