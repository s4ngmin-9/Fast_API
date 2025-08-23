from pydantic import BaseModel, Field
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    playtime: int
    genre: str

class MovieRead(BaseModel):
    id: int
    title: str
    playtime: int
    genre: str

class MovieSearch(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None

# 영화 정보 업데이트 요청에 사용되는 모델
class MovieUpdate(BaseModel):
    title: str
    playtime: int = Field(gt=0)
    genre: str