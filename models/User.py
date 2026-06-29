from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class User(Base):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment='用户id'
    )
    username: Mapped[str] = mapped_column(
        String(255),
        comment='用户名'
    )
    password: Mapped[str] = mapped_column(
        String(255),
        comment='密码'
    )
