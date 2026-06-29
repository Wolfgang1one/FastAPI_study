from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.initDatabase import create_tables
from models.Book import Book
from schemas.BookSchema import BookQuery, BookResponse  # ✅ 导入 Pydantic 模型


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/books")
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book

@app.get("/books/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(select(Book).where(Book.id == book_id))
    response_result = db_result.scalar_one_or_none()
    return response_result

@app.post("/books/book_price", response_model=List[BookResponse])
async def search_books_by_price(book_query: BookQuery, db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(select(Book).where(Book.price >= book_query.price))
    reponse_result = db_result.scalars().all()
    return reponse_result

@app.get("/")
async def root():
    return {"message": "Hello World"}
