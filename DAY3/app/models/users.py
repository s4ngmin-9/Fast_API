import json
from passlib.context import CryptContext
from typing import Optional, Dict, List
from app.schemas.users import UserCreate, UserUpdate
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel:
    _db: List[Dict] = []
    _id_counter: int = 1

    @classmethod
    def get_hashed_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create(cls, username: str, password: str, age: int, gender: str) -> Optional[Dict]:
        if any(user.get("username") == username for user in cls._db):
            return None  # 이미 존재하는 유저명

        # 비밀번호 해시
        # Hash the password.
        hashed_password = cls.get_hashed_password(password)

        new_user = {
            "id": cls._id_counter,
            "username": username,
            "hashed_password": hashed_password,
            "age": age,
            "gender": gender,
            "last_login": None,  # last_login 필드 추가
        }
        cls._db.append(new_user)
        cls._id_counter += 1
        return new_user

    @classmethod
    def all(cls) -> List[Dict]:
        return cls._db

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[Dict]:
        return next((user for user in cls._db if user["id"] == user_id), None)

    @classmethod
    def get_by_username(cls, username: str) -> Optional[Dict]:
        return next((user for user in cls._db if user["username"] == username), None)

    @classmethod
    def update(cls, user_id: int, user_update_data: UserUpdate) -> Optional[Dict]:
        user = cls.get_by_id(user_id)
        if user is None:
            return None

        update_data = user_update_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "password":
                user["hashed_password"] = cls.get_hashed_password(value)
            elif key == "last_login":
                user["last_login"] = value
            else:
                user[key] = value
        return user

    @classmethod
    def delete(cls, user_id: int) -> bool:
        user_to_delete = cls.get_by_id(user_id)
        if user_to_delete:
            cls._db.remove(user_to_delete)
            return True
        return False

    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional[Dict]:
        user = cls.get_by_username(username)
        if user and cls.verify_password(password, user["hashed_password"]):
            return user
        return None

    @classmethod
    def create_dummy(cls):
        if not cls._db:
            cls.create(username="john_doe", password="password123", age=30, gender="male")
            cls.create(username="jane_doe", password="password456", age=25, gender="female")

    @classmethod
    def search(cls, username: Optional[str] = None, age: Optional[int] = None, gender: Optional[str] = None) -> List[
        Dict]:
        results = cls._db
        if username:
            results = [user for user in results if user.get("username") == username]
        if age:
            results = [user for user in results if user.get("age") == age]
        if gender:
            results = [user for user in results if user.get("gender") == gender]
        return results

