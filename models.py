from sqlalchemy import Boolean, ForeignKey ,Column, Integer, String, Date, CHAR, DateTime
# from sqlalchemy.orm import relationship
from database import Base

# class BookPicture(Base, Image):
#     __tablename__= 'bookPic'
#     book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
#     book = relationship('Book')

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
    price = Column(String, index=True)
    menuImage = Column(String, index=True)
    
# class Orders(Base):
#     __tablename__ = 'orders'

#     id = Column(Integer, primary_key=True, index=True)
#     menu = Column(String, index=True)
#     number = Column(String, index=True)
#     date = Column(DateTime, index=True)
#     description = Column(String, index=True)


