from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

DATABASE_URL = "sqlite:///./library.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class AuthorORM(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    nationality = Column(String(50), nullable=False)
    birth_year = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    books = relationship("BookORM", back_populates="author")


class BookORM(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250), nullable=False)
    genre = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    copies_available = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("AuthorORM", back_populates="books")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AuthorCreate(BaseModel):
    full_name: str = Field(..., example="Франко Іван", description="ПІБ автора")
    nationality: str = Field(..., example="Українська", description="Національність")
    birth_year: int = Field(..., example=1956, description="Рік народження")
    email: str = Field(..., example="author@library.ua", description="Email автора (унікальний)")


class AuthorResponse(AuthorCreate):
    id: int

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str = Field(..., example="Таємниця старого замку", description="Назва книги")
    genre: str = Field(..., example="Детектив", description="Жанр книги")
    price: float = Field(..., gt=0, example=350.00, description="Ціна (грн)")
    copies_available: int = Field(..., ge=0, example=25, description="Кількість примірників")
    author_id: int = Field(..., example=1, description="ID автора")


class BookResponse(BookCreate):
    id: int
    author: Optional[AuthorResponse] = None

    class Config:
        from_attributes = True


class ImportResponse(BaseModel):
    imported: int
    message: str


app = FastAPI(
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get(
    "/authors",
    response_model=list[AuthorResponse],
    tags=["Автори"],
    summary="Отримати всіх авторів",
)
def list_authors(db: Session = Depends(get_db)):
    return db.query(AuthorORM).all()


@app.post(
    "/authors",
    response_model=AuthorResponse,
    status_code=201,
    tags=["Автори"],
    summary="Додати нового автора",
)
def create_author(payload: AuthorCreate, db: Session = Depends(get_db)):
    existing = db.query(AuthorORM).filter_by(email=payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Автор з таким email вже існує")
    author = AuthorORM(**payload.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@app.get(
    "/authors/{author_id}",
    response_model=AuthorResponse,
    tags=["Автори"],
    summary="Отримати автора за ID",
)
def get_author(author_id: int, db: Session = Depends(get_db)):
    a = db.query(AuthorORM).filter_by(id=author_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Автора не знайдено")
    return a


@app.delete(
    "/authors/{author_id}",
    tags=["Автори"],
    summary="Видалити автора",
)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    a = db.query(AuthorORM).filter_by(id=author_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Автора не знайдено")
    db.delete(a)
    db.commit()
    return {"detail": f"Автора #{author_id} видалено"}


@app.get(
    "/books",
    response_model=list[BookResponse],
    tags=["Книги"],
    summary="Отримати всі книги",
)
def list_books(
    genre: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db),
):
    q = db.query(BookORM)
    if genre:
        q = q.filter(BookORM.genre == genre)
    if min_price is not None:
        q = q.filter(BookORM.price >= min_price)
    if max_price is not None:
        q = q.filter(BookORM.price <= max_price)
    return q.all()


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=201,
    tags=["Книги"],
    summary="Додати нову книгу",
)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    author = db.query(AuthorORM).filter_by(id=payload.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail=f"Автора #{payload.author_id} не знайдено")
    book = BookORM(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["Книги"],
    summary="Отримати книгу за ID",
)
def get_book(book_id: int, db: Session = Depends(get_db)):
    b = db.query(BookORM).filter_by(id=book_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return b


@app.delete(
    "/books/{book_id}",
    tags=["Книги"],
    summary="Видалити книгу",
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    b = db.query(BookORM).filter_by(id=book_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    db.delete(b)
    db.commit()
    return {"detail": f"Книгу #{book_id} видалено"}


@app.post(
    "/import",
    response_model=ImportResponse,
    tags=["Імпорт CSV"],
    summary="Імпортувати дані з data.csv у базу",
    description="Читає файл `data.csv` з поточної директорії та завантажує всі записи в базу. Автори дедублікуються за email.",
)
def import_csv(db: Session = Depends(get_db)):
    import csv, os

    file_path = "data.csv"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл data.csv не знайдено. Спочатку запустіть: python generate_csv.py")

    count = 0
    with open(file_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            author = db.query(AuthorORM).filter_by(email=row["author_email"]).first()
            if not author:
                author = AuthorORM(
                    full_name=row["author_full_name"],
                    nationality=row["author_nationality"],
                    birth_year=int(row["author_birth_year"]),
                    email=row["author_email"],
                )
                db.add(author)
                db.flush()

            db.add(BookORM(
                title=row["book_title"],
                genre=row["book_genre"],
                price=float(row["price"]),
                copies_available=int(row["copies_available"]),
                author_id=author.id,
            ))
            count += 1

    db.commit()
    return ImportResponse(imported=count, message=f"Успішно імпортовано {count} книг з data.csv")


@app.get("/", include_in_schema=False)
def root():
    return HTMLResponse("""
    <html><body style="font-family:sans-serif;max-width:600px;margin:60px auto;text-align:center">
        <h1>📚 Library API</h1>
        <p>Відкрий <a href="/docs"><strong>Swagger UI → /docs</strong></a></p>
        <p>Або <a href="/redoc">ReDoc → /redoc</a></p>
    </body></html>
    """)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
