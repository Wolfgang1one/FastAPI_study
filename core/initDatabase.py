from sqlalchemy.ext.asyncio import create_async_engine
from models import Base

ASYNC_DATABASE_URL = "mysql+aiomysql://root:891460493@localhost:3306/fastapi_test?charset=utf8mb4"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

# 建数据表
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)