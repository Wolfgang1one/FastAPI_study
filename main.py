from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.initDatabase import create_tables
from models.Book import Book

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/books")
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    book = result.scalars().all()
    return book


@app.get("/")
async def root():
    return {"message": "Hello World"}
