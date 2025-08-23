# FastAPI 유저 관리 API

이 프로젝트는 FastAPI를 사용하여 기본적인 유저(User) 관리 기능을 제공하는 RESTful API입니다.
CRUD(Create, Read, Update, Delete) 및 검색 기능을 포함하고 있으며, Pydantic을 활용한 데이터 유효성 검증과 파일 구조 분리를 통해 확장성과 유지보수성을 고려하여 설계되었습니다.

---

## 🚀 주요 기능

-   **유저 생성 (Create)**: `POST /users/`
    -   `username`, `age`, `gender` 정보를 받아 유저를 생성합니다.
-   **모든 유저 조회 (Read)**: `GET /users/`
    -   등록된 모든 유저 정보를 리스트 형태로 반환합니다.
-   **특정 유저 조회 (Read)**: `GET /users/{user_id}`
    -   경로 매개변수로 받은 `user_id`에 해당하는 유저 정보를 반환합니다.
-   **유저 정보 업데이트 (Update)**: `PUT /users/{user_id}`
    -   `user_id`에 해당하는 유저의 `username`과 `age`를 업데이트합니다.
-   **유저 삭제 (Delete)**: `DELETE /users/{user_id}`
    -   `user_id`에 해당하는 유저를 삭제합니다.
-   **유저 검색 (Search)**: `GET /users/search/`
    -   `username`, `age`, `gender`를 쿼리 매개변수로 받아 유저를 검색합니다.

---

## 🛠️ 설치 및 실행

### 1. 의존성 설치

프로젝트의 의존성 관리를 위해 Poetry를 사용합니다.

```bash
# Poetry 설치 (설치되어 있지 않다면)
pip install poetry

# 프로젝트 의존성 설치
poetry install
```
---
🌐 API 문서
서버가 실행되면, 다음 URL에서 자동으로 생성된 API 문서를 확인할 수 있습니다.

Swagger UI: http://127.0.0.1:8000/docs