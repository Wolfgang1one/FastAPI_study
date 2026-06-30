from typing import Generic, TypeVar, List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

T = TypeVar("T")

class PageQuery(BaseModel):
    page: int
    size: int

class PageResponse(BaseModel, Generic[T]):
    """统一的分页响应格式"""
    items: List[T]  # 当前页的数据列表
    total: int  # 总记录数
    page: int  # 当前页码
    size: int  # 每页条数
    pages: int  # 总页数


async def paginate(
        db: AsyncSession,
        stmt,  # 基础查询语句（不含 limit/offset）
        page: int = 1,
        size: int = 10,
):
    # 1. 计算总记录数
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt)

    # 2. 执行分页查询
    offset = (page - 1) * size
    paginated_stmt = stmt.offset(offset).limit(size)
    result = await db.execute(paginated_stmt)
    items = result.scalars().all()

    # 4. 返回标准分页对象
    return PageResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )
