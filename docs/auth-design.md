# 기술 설계: 한국투자증권(KIS) API 인증 모듈

## 1. 개요
한국투자증권 Open API(KIS API)를 사용하기 위한 인증 시스템을 구축한다. 이 모듈은 접근 토큰(Access Token)의 발급, 유효성 검사, 자동 갱신, 토큰 폐기 및 실시간 웹소켓 접속키 발급을 담당한다.

## 2. 인증 워크플로우
1. **AppKey/AppSecret 준비**: 사용자의 계정 환경 변수 또는 설정에서 로드.
2. **접근 토큰 관리**:
    - 최초 호출 시 `/oauth2/tokenP`를 통해 토큰 발급.
    - 메모리에 캐싱하여 재사용하며, 만료 임박 시 자동 갱신.
    - 프로그램 종료 또는 필요 시 `/oauth2/revokeP`를 통해 토큰 폐기.
3. **실시간 접속키 관리**:
    - 웹소켓 연결이 필요한 경우 `/oauth2/Approval`을 통해 접속키 발급.

## 3. 상세 설계

### 3.1. 모듈 구조
- **파일**: `src/auth/kis_auth.py`
- **클래스**: `KISAuthenticator`
  - `__init__(app_key, app_secret, is_paper_trading=True)`
  - `get_access_token()`: 유효한 접근 토큰 반환 (자동 갱신 포함)
  - `revoke_token()`: 현재 사용 중인 토큰을 폐기
  - `get_approval_key()`: 실시간 웹소켓용 접속키 발급
  - `_request_new_token()`: KIS API를 호출하여 새 토큰 발급
  - `_is_token_expired()`: 현재 토큰의 만료 여부 판단

### 3.2. API 정보 (기반: docs/api-spec.md)
| 기능 | Endpoint (POST) | 주요 파라미터 |
|------|-----------------|---------------|
| 토큰 발급 | `/oauth2/tokenP` | `grant_type`, `appkey`, `appsecret` |
| 토큰 폐기 | `/oauth2/revokeP` | `appkey`, `appsecret`, `token` |
| 웹소켓 키 발급 | `/oauth2/Approval` | `grant_type`, `appkey`, `secretkey` |

### 3.3. API 엔드포인트 Base URL
- **실전투자**: `https://openapi.koreainvestment.com:9443`
- **모의투자**: `https://openapivts.koreainvestment.com:29443`

### 3.4. Rate Limit 제약 및 처리
- **정책**: 한국투자증권 API 제한에 따라 **1초당 최대 5건**의 호출을 넘지 않도록 관리한다.
- **구현**: 요청 간 최소 간격을 유지하거나, 호출 횟수를 카운팅하여 제어한다.

## 4. 예외 처리 및 로깅
- API 서버 응답 에러(4xx, 5xx) 발생 시 `KISAuthError` 발생 및 상세 내용 로깅.
- Rate Limit 초과 시 대기 후 재시도 로직 포함.
- 모든 인증 이벤트(발급, 갱신, 폐기)를 `logging` 모듈로 기록.

## 5. 토큰 저장 전략
- **초기 버전**: `KISAuthenticator` 인스턴스 내 메모리 캐싱.
- **보안**: 메모리 외부에 토큰을 저장하지 않으며, 세션 종료 시 폐기를 권장함.

## 6. 테스트 전략 (TDD)
- **접근 토큰 발급 테스트**: 토큰 부재 시 신규 발급 및 만료 시간 계산 검증.
- **토큰 재사용/갱신 테스트**: 만료 전 재사용 및 만료 후 자동 갱신 로직 검증.
- **토큰 폐기 테스트**: 폐기 요청 시 정상 처리 및 로컬 캐시 초기화 검증.
- **웹소켓 키 발급 테스트**: 실시간 접속키 정상 수신 및 반환 검증.
- **Mocking**: `unittest.mock`을 사용하여 모든 HTTP 요청을 모킹 처리.
