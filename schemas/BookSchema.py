from typing import List
from pydantic import BaseModel


class BookQuery(BaseModel):  # 用于接收请求体
    book_id: int
    book_id_list: List[int]
    author: str
    price: float
    publisher: str
    book_name: str


class BookResponse(BaseModel):  # 用于返回数据（可选，方便控制输出字段）
    id: int
    book_name: str
    author: str
    price: float
    publisher: str

    class Config:
        from_attributes = True


# ✅ 新增：用于聚合查询返回的模型
class BookAggregationResponse(BaseModel):
    total_price: float
    total_book_number: int
    max_price: float
