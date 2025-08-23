# main.py

from typing import List
from fastapi import FastAPI, HTTPException, Path, Depends, status
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserSearch
from app.models.movies import MovieModel
from app.schemas.movies import MovieCreate, MovieRead, MovieSearch, MovieUpdate

app = FastAPI()


# --- 유저 관련 라우터 (기존 구현 코드) ---
@app.post("/users/", response_model=UserRead)
async def create_user(user_data: UserCreate):
    new_user = UserModel.create(
        username=user_data.username,
        age=user_data.age,
        gender=user_data.gender
    )
    return new_user


@app.get("/users/", response_model=List[UserRead])
async def get_all_users():
    users = UserModel.all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@app.get("/users/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int = Path(..., gt=0)):
    user = UserModel.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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


@app.delete("/users/{user_id}")
async def delete_user(user_id: int = Path(..., gt=0)):
    user = UserModel.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    UserModel.delete(user_id)
    return {"detail": f"User: {user_id}, Successfully Deleted."}


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


# --- 영화 관련 라우터 ---
@app.post("/movies/", response_model=List[MovieRead], status_code=status.HTTP_201_CREATED)
async def create_movie(movie_data: MovieCreate):
    MovieModel.create(
        title=movie_data.title,
        playtime=movie_data.playtime,
        genre=movie_data.genre
    )
    all_movies = MovieModel.all()
    return all_movies


@app.get("/movies/", response_model=List[MovieRead], status_code=status.HTTP_200_OK)
async def get_movies(params: MovieSearch = Depends()):
    is_search_query = params.title is not None or params.genre is not None

    if is_search_query:
        movies = MovieModel.search(title=params.title, genre=params.genre)
        if not movies:
            movies = MovieModel.all()
    else:
        movies = MovieModel.all()

    return movies


@app.get("/movies/{movie_id}", response_model=MovieRead, status_code=status.HTTP_200_OK)
async def get_movie_by_id(movie_id: int = Path(..., gt=0)):
    movie = MovieModel.get_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.put("/movies/{movie_id}", response_model=MovieRead, status_code=status.HTTP_200_OK)
async def update_movie(
        movie_id: int = Path(..., gt=0),
        movie_update_data: MovieUpdate = ...
):
    movie = MovieModel.get_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.update(
        title=movie_update_data.title,
        playtime=movie_update_data.playtime,
        genre=movie_update_data.genre
    )
    return movie


# 특정 영화 삭제 라우터 (새로 추가)
@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int = Path(..., gt=0)):
    """
    movie_id에 해당하는 영화를 삭제합니다.
    """
    movie = MovieModel.get_by_id(movie_id)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    MovieModel.delete(movie_id)

    # 응답 본문 없이 상태코드만 반환하므로 return은 필요 없음