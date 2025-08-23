# 🎬 FastAPI User & Movie API

FastAPI 기반의 **유저 관리** 및 **영화 관리** API 프로젝트입니다.  
JWT 인증, OAuth2 로그인, CRUD API 라우팅, 비밀번호 해싱 등 다양한 기능을 포함합니다.


---

## 🚀 기능 개요

### 1. API Router 분리
- **`app/routers/users.py`**  
  - 유저 생성, 조회, 수정, 삭제, 검색 기능 구현
- **`app/routers/movies.py`**  
  - 영화 생성, 조회, 수정, 삭제, 검색 기능 구현
- `main.py`에서 `include_router()`로 등록하여 API 엔드포인트 구성

---

### 2. 유저 비밀번호 처리 & 인증
`app/models/users.py`  
- **`get_hashed_password()`** : Passlib + Bcrypt로 비밀번호 해싱  
- **`verify_password()`** : 평문 비밀번호와 해시 비교  
- **`authenticate()`** : username + password로 사용자 인증  

---

### 3. JWT 유틸리티
`app/utils/jwt.py`
- **`create_access_token(data: dict)`**
  - HS256 알고리즘, 30분 만료의 JWT 생성
- **`get_current_user()`**
  - OAuth2 Bearer 토큰 검증 후 현재 유저 반환
  - 토큰 검증 실패 시 `401 Unauthorized` 반환

---

### 4. 로그인 API
`POST /users/login`
- FormData(`username`, `password`) 입력
- `OAuth2PasswordRequestForm` 사용하여 데이터 검증
- `UserModel.authenticate()`로 인증
- 성공 시:
  - `last_login` 갱신
  - JWT Access Token 발급
- 실패 시:
  - `401 Unauthorized` 응답

**응답 예시**
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer"
}