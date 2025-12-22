# 프로젝트 TODO LIST (Agent 진행 상황 반영)

## 📌 현재까지 Agent가 완료한 작업 (2025-12-19)

- [x] **1. FastAPI 프로젝트 기본 구조 생성**
    - `app/`, `app/core/`, `app/db/`, `app/models/pydantic/`, `app/models/orm/`, `app/repositories/`, `app/services/` 디렉토리 및 `__init__.py` 파일 생성
- [x] **2. 초기 의존성 추가 및 FastAPI 앱 구현**
    - `requirements.txt`에 `fastapi`, `uvicorn`, `pydantic-settings`, `passlib[pbkdf2_sha256]`, `pytest`, `pytest-fastapi`, `SQLAlchemy`, `psycopg2-binary`, `httpx` 추가
    - `app/main.py`에 기본적인 FastAPI 앱과 `get_db` 의존성 주입 구현
- [x] **3. Pydantic 모델 및 초기 서비스 로직 구현**
    - Pydantic 사용자 모델 (`app/models/pydantic/user.py`) 및 ORM 사용자 모델 (`app/models/orm/user.py`) 분리
    - `app/core/config.py`, `app/db/session.py`, `app/db/base.py` 등 DB 연동을 위한 설정 파일 및 유틸리티 구현
- [x] **4. `user_service` 단위 테스트 작성 및 통과**
    - `app/services/user_service.py` 리팩토링 및 `UserRepository`를 통한 DB 연동
    - 통합 테스트(`tests/api/test_users.py`) 환경 구축 및 테스트 통과
- [x] **5. 리포지토리 패턴(Repository Pattern) 도입**
    - `BaseRepository` 정의 (`app/repositories/base.py`)
    - `UserRepository` 구현 (`app/repositories/user_repository.py`)
- [x] **6. 실제 데이터베이스(PostgreSQL) 연동**
    - `app/core/config.py`에 `DATABASE_URL` 플레이스홀더 설정 (사용자 입력 필요)
    - SQLAlchemy ORM을 사용하여 DB 스키마 정의 및 세션 관리
- [x] **7. `attendance_service` 모듈 구현 및 테스트**
    - Pydantic 출결 모델 (`app/models/pydantic/attendance.py`) 및 ORM 출결 모델 (`app/models/orm/attendance.py`) 구현
    - `AttendanceRepository` 및 `AttendanceService` 구현 (`app/repositories/attendance_repository.py`, `app/services/attendance_service.py`)
    - `app/main.py`에 출결 관련 API 엔드포인트 추가
    - 통합 테스트(`tests/api/test_attendances.py`) 작성 및 통과
    - Pydantic 경고 및 `datetime.utcnow()` 사용 중단 경고 해결

---

## 📌 향후 프로젝트 TODO (Original TODO.md 기반)

### ☐ Ⅲ. 구현 및 품질 확보 단계

- [ ] **1. 모듈 구현**
    - [x] `grade_service`: 성적 처리 관련 비즈니스 로직 구현 (Pandas 활용)
    - [ ] `notification_service`: 알림 관련 비즈니스 로직 구현
- [ ] **2. 데이터베이스 연동 구현**
    - [ ] Repository Layer 구현 (DB CRUD 캡슐화) - **(Agent가 User, Attendance 모듈에 대해 완료)**
    - [ ] 데이터 모델(Schema, DTO, Response) 분리 (Pydantic 활용) - **(Agent가 User, Attendance 모듈에 대해 완료)**
- [ ] **3. 품질 확보**
    - [ ] 단위 테스트(Unit Test) 작성 - **(Agent가 User, Attendance 모듈에 대해 완료)**
    - [ ] 통합 테스트(Integration Test) 작성 - **(Agent가 User, Attendance 모듈에 대해 완료)**
    - [ ] E2E 테스트(Postman/Newman) 환경 구축 및 테스트
    - [ ] 부하 테스트(Locust) 환경 구축 및 테스트
    - [ ] 보안 점검 (OWASP Top 10 기준)

### ☐ Ⅳ. 운영·보안·고도화 단계

- [ ] **1. 배포 및 운영**
    - [ ] CI/CD 파이프라인 구축 (GitHub Actions + Docker)
    - [ ] 배포 전략(Blue-Green 또는 Rolling) 수립 및 구현
    - [ ] 모니터링 시스템 구축 (Prometheus + Grafana)
    - [ ] 로깅 시스템 구축 (ELK Stack)
- [ ] **2. 보안 강화**
    - [ ] 인증 시스템 구현 (OAuth2.0 / JWT)
    - [ ] 비밀번호 해시(bcrypt) 및 통신(HTTPS) 암호화 적용 - **(Agent가 User 모듈에 대해 해싱 적용)**
    - [ ] 개인정보(AES256) 암호화 적용
- [ ] **3. 데이터 관리**
    - [ ] 데이터 백업 정책 수립 및 구현 (주 1회)
    - [ ] 로그 보관 정책 수립 및 구현 (1년 이상)
- [ ] **4. 고도화 (선택/추가 기능)**
    - [ ] AI 기반 맞춤형 학습 추천 기능 개발
    - [ ] 실시간 알림 기능 개발 (WebSocket)
    - [ ] 모바일 앱 개발 (React Native/Flutter 등)
