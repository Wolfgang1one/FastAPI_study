from typing import List, Optional
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    book_id: Optional[int] = None
    author: Optional[str] = None
    price: Optional[float] = None
    publisher: Optional[str] = None
    book_name: Optional[str] = None


class BookQuery(BookBase):  # 用于接收请求体
    book_id_list: Optional[List[int]] = None


class BookResponse(BookBase):  # 用于返回数据（可选，方便控制输出字段）
    class Config:
        from_attributes = True


# ✅ 新增：用于聚合查询返回的模型
class BookAggregationResponse(BaseModel):
    total_price: float
    total_book_number: int
    max_price: float
