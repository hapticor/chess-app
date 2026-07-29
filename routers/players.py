from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import PlayerCreate, PlayerResponse

router = APIRouter(prefix="/players", tags=["Players"])

# 선수 등록 신청
@router.post("", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def register_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == player.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 학번/아이디입니다.")

    new_user = User(
        username=player.username,
        name=player.name,
        profile_image=player.profile_image,
        rating=1200.0,
        is_approved=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 승인된 선수 목록 (랭킹용)
@router.get("", response_model=List[PlayerResponse])
def get_approved_players(db: Session = Depends(get_db)):
    return db.query(User).filter(User.is_approved == True).all()

# 승인 대기 중인 선수 목록 (관리자용)
@router.get("/pending", response_model=List[PlayerResponse])
def get_pending_players(db: Session = Depends(get_db)):
    return db.query(User).filter(User.is_approved == False).all()

# 선수 승인하기 (관리자용)
@router.post("/{player_id}/approve", response_model=PlayerResponse)
def approve_player(player_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == player_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="선수를 찾을 수 없습니다.")
    
    user.is_approved = True
    db.commit()
    db.refresh(user)
    return user
