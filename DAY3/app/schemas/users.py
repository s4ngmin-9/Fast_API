# app/schemas/users.py

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8)
    age: int = Field(..., gt=0)
    gender: str = Field(..., pattern="^(male|female|other)$")

class UserRead(BaseModel):
    id: int
    username: str
    age: int
    gender: str
    last_login: Optional[datetime] = None

class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, min_length=8)
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    last_login: Optional[datetime] = None

class UserSearch(BaseModel):
    username: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
