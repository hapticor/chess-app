from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return "FIJE 사이트 연결 성공!"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Render의 환경 변수(DATABASE_URL)를 가져오고, 없으면 기본적으로 SQLite 사용
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chess.db")

# 2. Render가 제공하는 postgres:// 주소를 SQLAlchemy 규격인 postgresql:// 로 자동 호환 변환
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. DB 엔진 생성 (SQLite냐 PostgreSQL이냐에 따른 옵션 분기)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
