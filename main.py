from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return "FIJE 사이트 연결 성공!"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
