from datetime import datetime

from fastapi import FastAPI
from sqlalchemy import DateTime, func, String, Float
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

ASYNC_DATABASE_URL = "mysql+aiomysql://root:891460493@localhost:3306/fastapi_test?charset=utf8mb4"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

# 基类：创建时间，更新时间；
# 书籍表：id，书名，作者，价格，出版社；

class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        insert_default=func.now(),
        comment='创建时间',
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        insert_default=func.now(),
        onupdate=func.now(),
        comment='更新时间',
    )


class Book(Base):
    __tablename__ = "book"
    id :Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment='书籍id',
    )
    book_name :Mapped[str] = mapped_column(
        String(255),
        comment='书名',
    )
    author:Mapped[str] = mapped_column(
        String(255),
        comment='作者',
    )
    price:Mapped[float] = mapped_column(
        Float,
        comment='价格'
    )
    publisher:Mapped[str] = mapped_column(
        String(255),
        comment='出版社'
    )

class User(Base):
    __tablename__ = "user"
    user_id :Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment='用户id'
    )
    username :Mapped[str] = mapped_column(
        String(255),
        comment='用户名'
    )
    password :Mapped[str] = mapped_column(
        String(255),
        comment='密码'
    )

# 建数据表

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}
