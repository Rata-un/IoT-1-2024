from pyparsing import Char
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, CHAR
# from sqlalchemy.orm import relationship

from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)

class Students(Base):
    __tablename__ = 'students'

    stu_id = Column(String, primary_key=True, index=True)
    fname = Column(String, index=True)
    lname = Column(String, index=True)
    dob = Column(Date, index=True)
    gender = Column(CHAR, index=True)