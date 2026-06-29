# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

# 从环境变量读取数据库连接串
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,          # 连接前检查是否可用
    pool_recycle=3600,           # 连接回收时间（秒）
    echo=False,                  # 是否打印 SQL 日志（开发时可设为 True）
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类（用于定义模型）
Base = declarative_base()

# 依赖注入：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()