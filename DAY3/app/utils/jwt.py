from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.users import UserModel

# JWT 토큰 설정을 위한 상수들입니다.
# Constants for JWT token configuration.
SECRET_KEY = "your-super-secret-key"  # 실제 프로젝트에서는 환경 변수 등을 사용하세요.
# In a real project, use environment variables for this.
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer는 헤더에서 토큰을 추출하는 데 사용됩니다.
# OAuth2PasswordBearer is used to extract the token from the header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    주어진 데이터를 페이로드로 사용하여 JWT 액세스 토큰을 생성합니다.
    Creates a JWT access token using the given data as the payload.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    JWT 토큰을 검증하고 현재 유저를 반환합니다.
    Verifies the JWT token and returns the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserModel.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
