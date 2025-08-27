## 기능 요구사항
- 미팅 생성 시 **제목(title)**, **장소(location)** 기본값 설정
- 제목과 장소를 개별 수정 가능
- 수정 후 최신 미팅 정보 반환

---

## API
- `PATCH /meetings/{url_code}/title` → 제목 수정
- `PATCH /meetings/{url_code}/location` → 장소 수정

---

## EdgeDB
- 쿼리: `update_meeting_title.edgeql`, `update_meeting_location.edgeql`
- 모델: `FullMeeting`에 `title`, `location` 추가
- 서비스: 각각의 업데이트 쿼리 호출

---

## MySQL (Tortoise ORM)
- 모델: `MeetingModel`에 `title`, `location` 필드 및 기본값 추가
- 메서드: `update_title`, `update_location` (특정 필드만 업데이트)
- 서비스: 각각의 업데이트 메서드 호출

---

## 기타
- 라우터에 PATCH 엔드포인트 추가
- DTO에 `title`, `location` 필드 포함
- 테스트: 정상 동작 + 예외 상황, 100% 커버리지
