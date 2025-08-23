from typing import List
from fastapi import FastAPI, HTTPException, Path, Depends
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserSearch

app = FastAPI()


# 유저 생성 라우터
@app.post("/users/", response_model=UserRead)
async def create_user(user_data: UserCreate):
    new_user = UserModel.create(
        username=user_data.username,
        age=user_data.age,
        gender=user_data.gender
    )
    return new_user


# 모든 유저 정보를 가져오는 라우터
@app.get("/users/", response_model=List[UserRead])
async def get_all_users():
    users = UserModel.all()

    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    return users


# ID로 유저 정보를 가져오는 라우터
@app.get("/users/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int = Path(..., gt=0)):
    user = UserModel.get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# 유저 정보를 업데이트하는 라우터
@app.put("/users/{user_id}", response_model=UserRead)
async def update_user(
        user_id: int = Path(..., gt=0),
        user_update_data: UserUpdate = ...
):
    user = UserModel.get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.update(user_update_data)

    return user


# 유저를 삭제하는 라우터
@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(..., gt=0)):
    user = UserModel.get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    UserModel.delete(user_id)

    return {"detail": f"User: {user_id}, Successfully Deleted."}


# 유저를 검색하는 라우터
@app.get("/users/search/", response_model=List[UserRead])
async def search_users(params: UserSearch = Depends()):
    users = UserModel.search(
        username=params.username,
        age=params.age,
        gender=params.gender
    )

    if not users:
        raise HTTPException(status_code=404, detail="User not found")

    return users