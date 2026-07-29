from pydantic import BaseModel
from typing import Optional

# 선수 등록할 때 받는 데이터 양식
class PlayerCreate(BaseModel):
    username: str
    name: str
    profile_image: Optional[str] = ""

# 화면에 선수 정보 보내줄 때 데이터 양식
class PlayerResponse(BaseModel):
    id: int
    username: str
    name: str
    profile_image: Optional[str]
    rating: float
    wins: int
    draws: int
    losses: int
    is_approved: bool

    class Config:
        from_attributes = True
