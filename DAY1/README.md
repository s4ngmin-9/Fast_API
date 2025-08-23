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

## 📦 프로젝트 구조

이 프로젝트는 다음과 같은 모범 사례를 따르는 구조로 구성되어 있습니다.

.
├── app/
│   ├── models/           # 데이터 모델 (임시 DB 역할)
│   │   └── users.py
│   ├── schemas/          # Pydantic 데이터 검증/응답 모델
│   │   └── users.py
│   └── init.py
├── main.py               # FastAPI 애플리케이션의 진입점
├── poetry.lock
├── pyproject.toml
└── README.md