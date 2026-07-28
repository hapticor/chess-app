import os
from fastapi import FastAPI, Depends
import uvicorn
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# ==========================================
# 1. 데이터베이스(DB) 연결 설정
# ==========================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chess.db")

# Render가 제공하는 postgres:// 주소를 SQLAlchemy 규격인 postgresql:// 로 변환
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# DB 엔진 및 세션 생성
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 세션 가져오기 도우미 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 2. FastAPI 앱 생성
# ==========================================
app = FastAPI(title="FIJE 체스 사이트 백엔드")

# ==========================================
# 3. API 엔드포인트(웹 주소) 정의
# ==========================================

# 메인 페이지 (https://fije-jbsh-net.onrender.com/)
@app.get("/")
def home():
    return {"message": "FIJE 사이트 연결 성공!"}

# DB 연결 확인용 테스트 페이지 (https://fije-jbsh-net.onrender.com/db-check)
@app.get("/db-check")
def check_db(db: Session = Depends(get_db)):
    try:
        # DB에 간단한 쿼리를 날려 연결 상태 확인
        db.execute(text("SELECT 1"))
        return {
            "status": "success", 
            "message": "PostgreSQL 데이터베이스에 성공적으로 연결되었습니다!"
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"DB 연결 실패: {str(e)}"
        }

# ==========================================
# 4. 로컬 테스트 실행용
# ==========================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
