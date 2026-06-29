from pydantic import BaseModel


class BookQuery(BaseModel):      # 用于接收请求体
    price: float


class BookResponse(BaseModel):   # 用于返回数据（可选，方便控制输出字段）
    id: int
    book_name: str
    author: str
    price: float
    publisher: str

    class Config:
        from_attributes = True   # 允许从 ORM 对象转换