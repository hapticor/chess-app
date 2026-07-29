from fastapi import FastAPI, Depends
from sqlalchemy import text
from database import engine, Base, get_db
from routers import players

# DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FIJE 체스 사이트 백엔드")

# 분리한 선수 API 라우터 등록
app.include_router(players.router)

@app.get("/")
def home():
    return {"message": "FIJE 체스 사이트 백엔드 서버 동작 중!"}

@app.get("/db-check")
def check_db(db: Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "PostgreSQL 데이터베이스 연결 성공!"}
    except Exception as e:
        return {"status": "error", "message": f"DB 연결 실패: {str(e)}"}
