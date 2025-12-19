# 학생 관리 시스템 개발 일지 (Agent 작업 기록)

## 2025년 12월 19일 - 작업 시작 및 초기 프로젝트 설정

*   **초기 요청 분석:** `C:\rokey\심화반\student_management`의 `project_plan.md`와 `development_log.md`를 참조하여 TODO 리스트를 생성하고, `https://github.com/whgms259/main_study` 리포지토리에 커밋 및 푸시 요청 접수. 빌드 및 배포 요청도 있었으나, 초기 코드 부재로 구조 구현으로 선회.
*   **TODO.md 생성 및 리포지토리 반영:** `development_log.md`에 있던 기존 TODO 리스트를 `main_study/TODO.md`로 복사하여 리포지토리에 커밋 및 푸시.

## 2025년 12월 19일 - `user_service` 구현 및 테스트 환경 구축

*   **FastAPI 프로젝트 기본 구조 생성:** `app/`, `app/core/`, `app/db/`, `app/models/pydantic/`, `app/models/orm/`, `app/repositories/`, `app/services/` 디렉토리와 `__init__.py` 파일들을 생성하여 기본적인 FastAPI 프로젝트 구조를 마련.
*   **초기 의존성 추가:** `requirements.txt`에 `fastapi`, `uvicorn`, `pydantic-settings`, `passlib[pbkdf2_sha256]`, `pytest`, `httpx`, `SQLAlchemy`, `psycopg2-binary` 등 핵심 라이브러리들을 추가.
*   **Pydantic 모델 및 ORM 모델 분리:** `user.py` 파일을 Pydantic 스키마(`app/models/pydantic/user.py`)와 SQLAlchemy ORM 모델(`app/models/orm/user.py`)로 분리하고, 관련 임포트 경로를 수정.
*   **데이터베이스 연동 설정:** `app/core/config.py`에 `DATABASE_URL` 플레이스홀더를 포함한 설정 파일을 생성하고, `app/db/session.py`에 DB 세션 관리 로직, `app/db/base.py`에 SQLAlchemy `Base`를 정의.
*   **리포지토리 패턴 도입:** `app/repositories/base.py`에 `BaseRepository` 인터페이스를 정의하고, `app/repositories/user_repository.py`에 SQLAlchemy를 사용하는 `UserRepository`를 구현.
*   **`user_service` 구현:** `app/services/user_service.py`를 리팩토링하여 `UserRepository`를 통해 DB 작업을 수행하도록 변경.
*   **FastAPI 엔드포인트 추가:** `app/main.py`에 사용자 생성(`POST /users/`) API 엔드포인트를 추가하고, DB 세션 의존성을 주입하도록 설정.
*   **테스트 환경 구축:** `tests/conftest.py`에 SQLite 인메모리 DB를 사용한 테스트용 DB 세션 및 `TestClient` 픽스처를 정의. `tests/api/test_users.py`에 사용자 생성 API에 대한 통합 테스트 작성.

## 2025년 12월 19일 - 문제 해결 및 `attendance_service` 구현

*   **`passlib` bcrypt 오류 해결:**
    *   초기 테스트 실행 시 `passlib`의 `bcrypt` 백엔드에서 `ValueError: password cannot be longer than 72 bytes` 및 `AttributeError` 발생.
    *   `passlib` 및 `bcrypt` 패키지 재설치 시도했으나 문제 지속.
    *   `app/repositories/user_repository.py`에서 `pwd_context`의 해싱 스키마를 `pbkdf2_sha256`으로 변경하여 문제 우회. 모든 테스트 통과 확인.
*   **Pydantic 경고 해결:** `ConfigDict` 임포트 누락으로 인한 경고(`NameError`)를 `app/models/pydantic/attendance.py` 및 `app/core/config.py`에 `from pydantic import ConfigDict` 추가하여 해결.
*   **`datetime.utcnow()` 경고 해결:** `tests/api/test_attendances.py`에서 `datetime.utcnow()`를 `datetime.now(timezone.utc)`로 변경하여 DeprecationWarning 해결.
*   **Pydantic `dict()` 메서드 경고 해결:** `app/repositories/attendance_repository.py`에서 `attendance.dict()`를 `attendance.model_dump()`로 변경하여 DeprecationWarning 해결.
*   **`attendance_service` 구현:**
    *   Pydantic 출결 모델(`app/models/pydantic/attendance.py`) 및 ORM 출결 모델(`app/models/orm/attendance.py`) 정의. `User` ORM 모델에 `attendances` 관계 추가.
    *   `AttendanceRepository`(`app/repositories/attendance_repository.py`) 및 `AttendanceService`(`app/services/attendance_service.py`) 구현.
    *   `app/main.py`에 출결 관련 API 엔드포인트(`POST /attendances/`, `GET /users/{user_id}/attendances/`) 추가.
*   **`attendance_service` 테스트:** `tests/api/test_attendances.py`에 출결 API 엔드포인트에 대한 통합 테스트 작성 및 모든 테스트 통과 확인.

## 다음 작업

*   사용자 정의 `DATABASE_URL`을 `app/core/config.py`에 설정하여 실제 PostgreSQL 데이터베이스와 연동.
*   TODO 리스트의 다음 항목인 `grade_service` 및 `notification_service` 구현.
*   품질 확보 (E2E, 부하 테스트, 보안 점검) 및 운영/배포 관련 작업 진행.
