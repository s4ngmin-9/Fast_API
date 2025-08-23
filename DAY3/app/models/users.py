# app/models/users.py

import json
from passlib.context import CryptContext
from typing import Optional, Dict, List
from app.schemas.users import UserCreate, UserUpdate
from datetime import datetime, timezone

# 비밀번호 해시를 위한 CryptContext 설정
# Configure CryptContext for password hashing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel:
    # 더미 데이터베이스 (실제로는 데이터베이스를 사용해야 합니다)
    # Dummy database (in a real application, you would use a proper database).
    _db: List[Dict] = []
    _id_counter: int = 1

    @classmethod
    def get_hashed_password(cls, password: str) -> str:
        """
        주어진 비밀번호를 해시하여 반환합니다.
        Hashes the given password and returns the hash.
        """
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        평문 비밀번호와 해시된 비밀번호를 비교합니다.
        Compares a plain-text password with a hashed password.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create(cls, username: str, password: str, age: int, gender: str) -> Optional[Dict]:
        """
        새로운 유저를 생성하고 더미 DB에 추가합니다.
        Creates a new user and adds them to the dummy DB.
        """
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
        """
        모든 유저 정보를 반환합니다.
        Returns all user information.
        """
        return cls._db

    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[Dict]:
        """
        ID로 유저를 찾아서 반환합니다.
        Finds and returns a user by ID.
        """
        return next((user for user in cls._db if user["id"] == user_id), None)

    @classmethod
    def get_by_username(cls, username: str) -> Optional[Dict]:
        """
        유저명으로 유저를 찾아서 반환합니다.
        Finds and returns a user by username.
        """
        return next((user for user in cls._db if user["username"] == username), None)

    @classmethod
    def update(cls, user_id: int, user_update_data: UserUpdate) -> Optional[Dict]:
        """
        특정 유저 정보를 업데이트합니다.
        Updates a specific user's information.
        """
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
        """
        특정 유저를 삭제합니다.
        Deletes a specific user.
        """
        user_to_delete = cls.get_by_id(user_id)
        if user_to_delete:
            cls._db.remove(user_to_delete)
            return True
        return False

    @classmethod
    def authenticate(cls, username: str, password: str) -> Optional[Dict]:
        """
        유저를 인증하고, 성공 시 유저 객체를 반환합니다.
        Authenticates a user and returns the user object on success.
        """
        user = cls.get_by_username(username)
        if user and cls.verify_password(password, user["hashed_password"]):
            return user
        return None

    @classmethod
    def create_dummy(cls):
        """
        테스트를 위한 더미 유저를 생성합니다.
        Creates dummy users for testing.
        """
        if not cls._db:
            cls.create(username="john_doe", password="password123", age=30, gender="male")
            cls.create(username="jane_doe", password="password456", age=25, gender="female")

    @classmethod
    def search(cls, username: Optional[str] = None, age: Optional[int] = None, gender: Optional[str] = None) -> List[
        Dict]:
        """
        주어진 매개변수로 유저를 검색합니다.
        Searches for users based on the given parameters.
        """
        results = cls._db
        if username:
            results = [user for user in results if user.get("username") == username]
        if age:
            results = [user for user in results if user.get("age") == age]
        if gender:
            results = [user for user in results if user.get("gender") == gender]
        return results

