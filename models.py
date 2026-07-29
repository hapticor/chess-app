from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False) # 학번/아이디
    name = Column(String, nullable=False)                               # 이름
    rating = Column(Float, default=1200.0)                               # 점수
    wins = Column(Integer, default=0)                                    # 승
    draws = Column(Integer, default=0)                                   # 무
    losses = Column(Integer, default=0)                                  # 패
    is_approved = Column(Boolean, default=False)                         # 승인 여부
