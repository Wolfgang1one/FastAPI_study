from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.initDatabase import create_tables
from models.Book import Book
from schemas.BookSchema import BookQuery, BookResponse, BookAggregationResponse, BookBase
from schemas.Page import PageResponse, PageQuery, paginate

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post(
    path="/books/getBooksPage",
    response_model=PageResponse[BookResponse],
    description='分页查询'
)
async def get_books_page(
        page_query: PageQuery,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(Book).order_by(Book.book_id)
    db_result = await paginate(db, stmt, page_query.page, page_query.size)
    return db_result


@app.post(
    path="/books/getBook",
    response_model=BookResponse,
    description='Book单个查询'
)
async def get_book(
        book_query: BookBase,
        db: AsyncSession = Depends(get_db),
):
    # 字段映射：schema 字段名 → (ORM字段, 比较方式)
    field_map = {
        "book_id": (Book.book_id, lambda v, f: f == v),
        "book_name": (Book.book_name, lambda v, f: f == v),
        "author": (Book.author, lambda v, f: f == v),
        "price": (Book.price, lambda v, f: f >= v),
        "publisher": (Book.publisher, lambda v, f: f == v),
    }

    data = book_query.model_dump(exclude_none=True)

    if not data:
        book = await db.scalar(select(Book).order_by(Book.book_id.desc()).limit(1))
        if not book:
            raise HTTPException(status_code=404, detail="未找到匹配的图书")
        return book

    conditions = [comparator(value, orm_field) for field, value in data.items()
                  for orm_field, comparator in [field_map[field]]]

    book = await db.scalar(select(Book).where(*conditions))
    if not book:
        raise HTTPException(status_code=404, detail="未找到匹配的图书")
    return book


@app.post(
    path="/books/getBookList",
    response_model=List[BookResponse],
    description='Book列表查询'
)
async def get_book_list(
        book_query: BookQuery,
        db: AsyncSession = Depends(get_db)
):
    # 字段映射：schema 字段名 → (ORM字段, 比较方式)
    field_map = {
        "book_id": (Book.book_id, lambda v, f: f == v),
        "book_id_list": (Book.book_id, lambda v, f: f.in_(v)),   # ✅ 新增 book_id_list 的处理
        "book_name": (Book.book_name, lambda v, f: f == v),
        "author": (Book.author, lambda v, f: f == v),
        "price": (Book.price, lambda v, f: f >= v),
        "publisher": (Book.publisher, lambda v, f: f == v),
    }

    data = book_query.model_dump(exclude_none=True)

    if not data:
        raise HTTPException(status_code=404, detail='未找到匹配的图书')

    # 动态构建查询条件
    conditions = []
    for field, value in data.items():
        orm_field, comparator = field_map[field]
        conditions.append(comparator(value, orm_field))

    # 返回所有匹配的记录
    books = (await db.execute(select(Book).where(*conditions))).scalars().all()
    if not books:
        raise HTTPException(status_code=404, detail="未找到匹配的图书")
    return books


@app.post(
    path="/books/addBook",
    response_model=BookResponse,
    description='Book添加',
)
async def add_book(
        book_query: BookBase,
        db: AsyncSession = Depends(get_db)):
    # 校验必填字段
    required_fields = {"book_name", "author", "price", "publisher"}
    if any(book_query.model_dump(exclude_none=True, include=required_fields).get(f) is None
           for f in required_fields):
        raise HTTPException(
            status_code=400,
            detail="新增图书需要提供 book_name、author、price、publisher"
        )
    new_book = Book(**book_query.model_dump(exclude={"book_id"}))
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book
