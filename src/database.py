from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# ORM으로 데이터베이스와 python을 연결하기 
# 1. 엔진 2. 세션 3. Base 모델

load_dotenv()
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "database_name")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
if not DB_URL:
    raise RuntimeError("DB_URL이 준비되지 않았습니다.")

engine = create_engine(
    DB_URL,
    pool_pre_ping = True,
    future = True,
    pool_size = 10,
    max_overflow = 20,
    pool_timeout = 30
)

SessionLocal = sessionmaker(autocommit = False,   # 확정 자동 x
                            autoflush = False,    # 자동 새로고침 x
                            bind = engine,        # 어떤 DB와 연결하여 Session 생성?
                            future = True)

# 이 클래스는 데이터 베이스 테이블과 파이썬의 클래스와 연결 역할
Base = declarative_base()

# def create_tables():
#     Base.metadata.create_all(bine=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()