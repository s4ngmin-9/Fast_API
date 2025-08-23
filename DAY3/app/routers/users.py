# app/routers/users.py

from datetime import datetime, timezone
from typing import List, Dict
from fastapi import APIRouter, HTTPException, Path, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserSearch
from app.schemas.token import Token
from app.utils.jwt import create_access_token, get_current_user

# APIRouter 인스턴스를 생성하고, 경로 prefix와 태그를 설정합니다.
router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """
    새로운 유저를 생성합니다.
    """
    new_user = UserModel.create(
        username=user_data.username,
        password=user_data.password,
        age=user_data.age,
        gender=user_data.gender
    )
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists."
        )
    return new_user


@router.get("/", response_model=List[UserRead], status_code=status.HTTP_200_OK)
async def get_all_users():
    """
    모든 유저 정보를 반환합니다.
    """
    users = UserModel.all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: Dict = Depends(get_current_user)):
    """
    현재 인증된 유저의 정보를 반환합니다.
    Returns information about the currently authenticated user.
    """
    return current_user


@router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_user(
        user_id: int = Path(..., gt=0),
        user_update_data: UserUpdate = ...
):
    """
    특정 유저의 정보를 업데이트합니다.
    """
    user = UserModel.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.update(user_update_data)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int = Path(..., gt=0)):
    """
    특정 유저를 삭제합니다.
    """
    user = UserModel.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    UserModel.delete(user_id)


@router.get("/search/", response_model=List[UserRead], status_code=status.HTTP_200_OK)
async def search_users(params: UserSearch = Depends()):
    """
    쿼리 매개변수를 사용하여 유저를 검색합니다.
    """
    users = UserModel.search(
        username=params.username,
        age=params.age,
        gender=params.gender
    )
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    로그인 정보를 받아 JWT 액세스 토큰을 발급합니다.
    Receives login information and issues a JWT access token.
    """
    user = UserModel.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 마지막 로그인 시간을 업데이트합니다.
    # Update the last login time.
    user["last_login"] = datetime.now(timezone.utc)

    # JWT 토큰을 생성합니다.
    # Create a JWT token.
    access_token = create_access_token(data={"user_id": str(user["id"])})

    return {"access_token": access_token, "token_type": "bearer"}
