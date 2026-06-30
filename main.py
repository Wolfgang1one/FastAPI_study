from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.initDatabase import create_tables
from models.Book import Book
from schemas.BookSchema import BookQuery, BookResponse, BookAggregationResponse
from schemas.Page import PageResponse, PageQuery, paginate

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.post("/books/AggregationQueries", response_model=BookAggregationResponse)
async def aggregation_query(
        db: AsyncSession = Depends(get_db)
):
    db_result = await db.execute(
        select(func.sum(Book.price).label("total_price"))
    )
    total_price = db_result.scalar_one()
    db_result = await db.execute(
        select(func.count(Book.id).label("total_book_number"))
    )
    total_book_number = db_result.scalar_one()
    return BookAggregationResponse(total_price=total_price, total_book_number=total_book_number)


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


@app.post("/books/getBooksPage", response_model=PageResponse[BookResponse])
async def get_books_page(
        page_query: PageQuery,
        db: AsyncSession = Depends(get_db),
):
    stmt = select(Book).order_by(Book.id)
    db_result = await paginate(db, stmt, page_query.page, page_query.size)
    return db_result


@app.post(
    path="/books/getBook",
    response_model=BookResponse,
    description='获取book'
)
async def get_book(
        book_query: BookQuery,
        db: AsyncSession = Depends(get_db),
):
    # 判断是否所有字段都为空（都是 None 或默认值）
    if (book_query.book_name is None
            and book_query.author is None
            and book_query.price is None
            and book_query.publisher is None
            and book_query.book_id is None
            and book_query.book_id_list is None):
        # 查询 id 最大的那本书
        db_result = await db.execute(
            select(Book).order_by(Book.id.desc()).limit(1)
        )
        book = db_result.scalar_one_or_none()
        if not book:
            raise HTTPException(status_code=404, detail="图书数据为空")
        return book

    # 否则：根据传入的非空字段动态构建查询条件
    conditions = []
    if book_query.book_id is not None:
        conditions.append(Book.id == book_query.book_id)
    if book_query.book_id_list is not None:
        conditions.append(Book.id.in_(book_query.book_id_list))
    if book_query.book_name is not None:
        conditions.append(Book.book_name == book_query.book_name)
    if book_query.author is not None:
        conditions.append(Book.author == book_query.author)
    if book_query.price is not None:
        conditions.append(Book.price >= book_query.price)
    if book_query.publisher is not None:
        conditions.append(Book.publisher == book_query.publisher)

    db_result = await db.execute(
        select(Book).where(*conditions)
    )
    book = db_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="未找到匹配的图书")
    return book

@app.post(
    path="/books/addBook",
    response_model=BookResponse,
)
async def add_book(
        book_query: BookQuery,
        db: AsyncSession = Depends(get_db)):
    # 校验必填字段
    if (not book_query.book_name
            or not book_query.author
            or not book_query.publisher
            or book_query.price is None
    ):
        raise HTTPException(
            status_code=400,
            detail="新增图书需要提供 book_name、author、price、publisher"
        )
    new_book = Book(**book_query.model_dump(exclude={"book_id", "book_id_list"}))
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book
