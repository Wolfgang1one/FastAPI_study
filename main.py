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

# 需求：查询作者以 曹开头的图书  曹 % _
@app.post("/books/author", response_model=List[BookResponse])
async def query_book_list_by_author(
        db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(select(Book).where(Book.author.like('曹_')))
    reponse_result = db_result.scalars().all()
    return reponse_result

# 需求：查询作者以 曹开头的图书  曹 % _
@app.post("/books/queryBookListByIdList", response_model=List[BookResponse])
async def query_book_list_by_id_list(
        book_query: BookQuery,
        db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(select(Book).where(Book.id.in_(book_query.book_id_list)))
    reponse_result = db_result.scalars().all()
    return reponse_result

# 查询所有图书
@app.get("/books")
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book

# get请求，根据路径参数查询图书
@app.get("/books/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(select(Book).where(Book.id == book_id))
    response_result = db_result.scalar_one_or_none()
    return response_result

# post请求，查询大于等于图书价格的图书
@app.post("/books/book_price", response_model=List[BookResponse])
async def search_books_by_price(book_query: BookQuery, db: AsyncSession = Depends(get_db)):
    db_result = await db.execute(select(Book).where(Book.price >= book_query.price))
    reponse_result = db_result.scalars().all()
    return reponse_result

@app.get("/")
async def root():
    return {"message": "Hello World"}
