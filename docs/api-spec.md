# 한국투자증권 KIS API 명세서

## 1. 인증 관련 API

### 1.1. 접근 토큰 발급 (P) [인증-001]
- **설명**: API 사용을 위한 OAuth2.0 접근 토큰(Access Token)을 발급받습니다.
- **HTTP Method**: `POST`
- **Endpoint**: 
    - 실전투자: `https://openapi.koreainvestment.com:9443/oauth2/tokenP`
    - 모의투자: `https://openapivts.koreainvestment.com:29443/oauth2/tokenP`
- **Request Body (JSON)**:
    - `grant_type`: `"client_credentials"` (고정값)
    - `appkey`: 한국투자증권 홈페이지에서 발급받은 AppKey
    - `appsecret`: 한국투자증권 홈페이지에서 발급받은 AppSecret
- **Response Body (JSON)**:
    - `access_token`: 발급된 접근 토큰
    - `token_type`: `"Bearer"`
    - `expires_in`: 토큰 유효 기간 (초 단위, 보통 86400)
    - `access_token_token_expired`: 접근 토큰 만료 일시 (YYYY-MM-DD HH:MM:SS)

### 1.2. 접근 토큰 폐기 (P) [인증-002]
- **설명**: 발급받은 접근 토큰을 명시적으로 폐기합니다.
- **HTTP Method**: `POST`
- **Endpoint**:
    - 실전투자: `https://openapi.koreainvestment.com:9443/oauth2/revokeP`
    - 모의투자: `https://openapivts.koreainvestment.com:29443/oauth2/revokeP`
- **Request Body (JSON)**:
    - `appkey`: 한국투자증권 홈페이지에서 발급받은 AppKey
    - `appsecret`: 한국투자증권 홈페이지에서 발급받은 AppSecret
    - `token`: 폐기할 접근 토큰
- **Response Body (JSON)**:
    - `code`: 결과 코드 (200: 성공)
    - `message`: 결과 메시지

## 2. 실시간 데이터 관련 API

### 2.1. 실시간 (웹소켓) 접속키 발급 [실시간-000]
- **설명**: 실시간 시세 수집을 위한 웹소켓 접속키(Approval Key)를 발급받습니다.
- **HTTP Method**: `POST`
- **Endpoint**:
    - 실전투자: `https://openapi.koreainvestment.com:9443/oauth2/Approval`
    - 모의투자: `https://openapivts.koreainvestment.com:29443/oauth2/Approval`
- **Request Body (JSON)**:
    - `grant_type`: `"client_credentials"` (고정값)
    - `appkey`: 한국투자증권 홈페이지에서 발급받은 AppKey
    - `secretkey`: 한국투자증권 홈페이지에서 발급받은 AppSecret
- **Response Body (JSON)**:
## 3. 국내주식 정보 조회 API

### 3.1. 상품 기본 조회 [CTPF1604R]
- **설명**: 주식 종목의 기본적인 상품 정보를 조회합니다.
- **HTTP Method**: `GET`
- **Endpoint**: `/uapi/domestic-stock/v1/quotations/search-info`
- **주요 Header**: `tr_id`: `"CTPF1604R"`

### 3.2. 주식현재가 시세 [CTPF1002R]
- **설명**: 특정 종목의 현재가 및 기본적인 시세 정보를 조회합니다.
- **HTTP Method**: `GET`
- **Endpoint**: `/uapi/domestic-stock/v1/quotations/search-stock-info`
- **주요 Header**: `tr_id`: `"CTPF1002R"`

### 3.3. 재무제표 조회 [FHKST66430100]
- **설명**: 종목의 대차대조표 등 재무제표 데이터를 조회합니다.
- **HTTP Method**: `GET`
- **Endpoint**: `/uapi/domestic-stock/v1/finance/balance-sheet`
- **주요 Header**: `tr_id`: `"FHKST66430100"`

### 3.4. 손익계산서 조회 [FHKST66430200]
- **설명**: 종목의 손익계산서 데이터를 조회합니다.
- **HTTP Method**: `GET`
- **Endpoint**: `/uapi/domestic-stock/v1/finance/income-statement`
- **주요 Header**: `tr_id`: `"FHKST66430200"`

### 3.5. 종목 투자 의견 조회 [FHKST663300C0]
- **설명**: 종목에 대한 전문가/기관의 투자 의견을 조회합니다.
- **HTTP Method**: `GET`
- **Endpoint**: `/uapi/domestic-stock/v1/quotations/invest-opinion`
- **주요 Header**: `tr_id`: `"FHKST663300C0"`

### 3.6. 증권사별 투자 의견 조회 [FHKST663400C0]
- **설명**: 증권사별 종목 투자 의견 상세 데이터를 조회합니다.
- **HTTP Method**: `GET`
- **Endpoint**: `/uapi/domestic-stock/v1/quotations/invest-opbysec`
- **주요 Header**: `tr_id`: `"FHKST663400C0"`
