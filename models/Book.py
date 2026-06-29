from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base

# 书籍表：id，书名，作者，价格，出版社；
class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment='书籍id',
    )
    book_name: Mapped[str] = mapped_column(
        String(255),
        comment='书名',
    )
    author: Mapped[str] = mapped_column(
        String(255),
        comment='作者',
    )
    price: Mapped[float] = mapped_column(
        Float,
        comment='价格'
    )
    publisher: Mapped[str] = mapped_column(
        String(255),
        comment='出版社'
    )
