from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    nationality = Column(String(50), nullable=False)
    birth_year = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    genre = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    copies_available = Column(Integer, nullable=False)

    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship("Author", back_populates="books")
