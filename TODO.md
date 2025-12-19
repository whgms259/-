# 프로젝트 TODO LIST

## Ⅲ. 구현 및 품질 확보 단계

- [ ] **1. 모듈 구현**
    - [ ] `user_service`: 사용자 관련 비즈니스 로직 구현
    - [ ] `attendance_service`: 출결 관련 비즈니스 로직 구현 (QR, GPS 기반)
    - [ ] `grade_service`: 성적 처리 관련 비즈니스 로직 구현 (Pandas 활용)
    - [ ] `notification_service`: 알림 관련 비즈니스 로직 구현
- [ ] **2. 데이터베이스 연동 구현**
    - [ ] Repository Layer 구현 (DB CRUD 캡슐화)
    - [ ] 데이터 모델(Schema, DTO, Response) 분리 (Pydantic 활용)
- [ ] **3. 품질 확보**
    - [ ] 단위 테스트(Unit Test) 작성
    - [ ] 통합 테스트(Integration Test) 작성
    - [ ] E2E 테스트(Postman/Newman) 환경 구축 및 테스트
    - [ ] 부하 테스트(Locust) 환경 구축 및 테스트
    - [ ] 보안 점검 (OWASP Top 10 기준)

## Ⅳ. 운영·보안·고도화 단계

- [ ] **1. 배포 및 운영**
    - [ ] CI/CD 파이프라인 구축 (GitHub Actions + Docker)
    - [ ] 배포 전략(Blue-Green 또는 Rolling) 수립 및 구현
    - [ ] 모니터링 시스템 구축 (Prometheus + Grafana)
    - [ ] 로깅 시스템 구축 (ELK Stack)
- [ ] **2. 보안 강화**
    - [ ] 인증 시스템 구현 (OAuth2.0 / JWT)
    - [ ] 비밀번호 해시(bcrypt) 및 통신(HTTPS) 암호화 적용
    - [ ] 개인정보(AES256) 암호화 적용
- [ ] **3. 데이터 관리**
    - [ ] 데이터 백업 정책 수립 및 구현 (주 1회)
    - [ ] 로그 보관 정책 수립 및 구현 (1년 이상)
- [ ] **4. 고도화 (선택/추가 기능)**
    - [ ] AI 기반 맞춤형 학습 추천 기능 개발
    - [ ] 실시간 알림 기능 개발 (WebSocket)
    - [ ] 모바일 앱 개발 (React Native/Flutter 등)
