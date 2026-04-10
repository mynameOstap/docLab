import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Author, Book
from interfaces import IRepository


class SqliteRepository(IRepository):

    def __init__(self, db_url: str = "sqlite:///library.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def read_csv(self, file_path: str) -> list[dict]:
        data = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def save_author_with_book(self, author_dict: dict, book_dict: dict):
        session = self.Session()
        try:
            existing = (
                session.query(Author)
                .filter_by(email=author_dict['email'])
                .first()
            )
            if existing:
                author = existing
            else:
                author = Author(
                    full_name=author_dict['full_name'],
                    nationality=author_dict['nationality'],
                    birth_year=int(author_dict['birth_year']),
                    email=author_dict['email'],
                )
                session.add(author)
                session.flush()

            book = Book(
                title=book_dict['title'],
                genre=book_dict['genre'],
                price=float(book_dict['price']),
                copies_available=int(book_dict['copies_available']),
                author_id=author.id,
            )
            session.add(book)
            session.commit()
        except Exception as exc:
            session.rollback()
            print(f"[ERROR] save_author_with_book: {exc}")
        finally:
            session.close()

    def get_all_books(self) -> list[Book]:
        session = self.Session()
        books = session.query(Book).all()
        session.close()
        return books

    def get_all_authors(self) -> list[Author]:
        session = self.Session()
        authors = session.query(Author).all()
        session.close()
        return authors
