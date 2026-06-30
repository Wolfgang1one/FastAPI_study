from typing import List, Optional
from pydantic import BaseModel, Field

class BookQuery(BaseModel):  # 用于接收请求体
    book_id: Optional[int] = None
    book_id_list: Optional[List[int]] = None

    author: Optional[str] = None
    price: Optional[float] = None
    publisher: Optional[str] = None
    book_name: Optional[str] = None


class BookResponse(BaseModel):  # 用于返回数据（可选，方便控制输出字段）
    book_id: int = Field(validation_alias="id")
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
