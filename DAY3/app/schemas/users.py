# app/schemas/users.py

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    """
    유저 생성을 위한 Pydantic 모델
    Pydantic model for user creation.
    """
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8)
    age: int = Field(..., gt=0)
    gender: str = Field(..., pattern="^(male|female|other)$")

class UserRead(BaseModel):
    """
    유저 정보 읽기를 위한 Pydantic 모델 (응답용)
    Pydantic model for reading user information (for response).
    """
    id: int
    username: str
    age: int
    gender: str
    last_login: Optional[datetime] = None

class UserUpdate(BaseModel):
    """
    유저 정보 수정을 위한 Pydantic 모델
    Pydantic model for updating user information.
    """
    password: Optional[str] = Field(None, min_length=8)
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    last_login: Optional[datetime] = None

class UserSearch(BaseModel):
    """
    유저 검색을 위한 Pydantic 모델
    Pydantic model for user search.
    """
    username: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
