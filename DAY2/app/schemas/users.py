from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class Gender(str, Enum):
    male = "male"
    female = "female"

# 유저 생성 요청
class UserCreate(BaseModel):
    username: str
    age: int
    gender: Gender

# 유저 정보를 읽어오는 응답
class UserRead(BaseModel):
    id: int
    username: str
    age: int
    gender: Gender

# 유저 정보 업데이트 요청
class UserUpdate(BaseModel):
    username: Optional[str] = None
    age: Optional[int] = None

# 유저 검색 쿼리 매개변수
class UserSearch(BaseModel):
    username: Optional[str] = None
    age: Optional[int] = Field(None, gt=0) # age는 0보다 큰 값만 허용
    gender: Optional[Gender] = None