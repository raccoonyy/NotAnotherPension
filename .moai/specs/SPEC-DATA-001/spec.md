---
id: DATA-001
version: 0.1.0
status: completed
created: 2025-12-05
updated: 2025-12-05
author: @Alfred
priority: critical
category: feature
labels:
  - data
  - json
  - core
blocks:
  - CALC-001
  - CALC-002
  - CALC-003
  - TAX-001
scope:
  packages:
    - data
  files:
    - data.json
    - update_data.py
---

# @SPEC:DATA-001: 데이터 파일 구조 및 로딩 시스템

## HISTORY

### v0.1.0 (2025-12-05)
- **CHANGED**: TDD 구현 완료 (status: draft → completed)
- **AUTHOR**: @Alfred
- **REASON**: RED-GREEN-REFACTOR 사이클 완료

### v0.0.1 (2025-12-05)
- **INITIAL**: data.json 구조 및 로딩 시스템 명세 작성
- **AUTHOR**: @Alfred
- **REASON**: 국민연금/개인연금 계산에 필요한 외부 데이터 관리 체계 정의

---

## 개요

NotAnotherPension 웹앱의 핵심 계산 로직에 필요한 외부 데이터를 관리하는 시스템입니다.
모든 계산 모듈(CALC-001~003, TAX-001)이 이 데이터에 의존합니다.

### 핵심 가치
- **분리**: 변동 가능한 데이터(A값, 수익률)를 코드에서 분리
- **갱신 용이**: Python 스크립트로 데이터 자동/수동 갱신
- **폴백 안전성**: 데이터 로드 실패 시 기본값 사용

---

## Ubiquitous Requirements (기본 요구사항)

- 시스템은 data.json 파일에서 외부 데이터를 로드하는 기능을 제공해야 한다
- 시스템은 국민연금 관련 데이터(A값, 소득대체율, 상하한선)를 포함해야 한다
- 시스템은 시장 수익률 데이터(S&P500, KOSPI, 물가상승률)를 포함해야 한다
- 시스템은 연령별 임금상승률 데이터를 포함해야 한다
- 시스템은 데이터 갱신일(updated_at)을 기록해야 한다

---

## Event-driven Requirements (이벤트 기반)

### DATA-001-E01: 데이터 로딩
- **WHEN** 페이지가 로드되면, 시스템은 data.json 파일을 fetch로 비동기 로드해야 한다
- **WHEN** fetch 요청이 성공하면, 시스템은 JSON 데이터를 파싱하여 전역 변수에 저장해야 한다
- **WHEN** fetch 요청이 실패하면, 시스템은 하드코딩된 기본값을 사용해야 한다

### DATA-001-E02: 데이터 검증
- **WHEN** JSON 데이터가 로드되면, 시스템은 필수 필드 존재 여부를 검증해야 한다
- **WHEN** 필수 필드가 누락되면, 시스템은 해당 필드에 기본값을 사용해야 한다

---

## State-driven Requirements (상태 기반)

### DATA-001-S01: 데이터 사용 가능 상태
- **WHILE** 데이터가 로딩 중일 때, 시스템은 계산 기능을 비활성화해야 한다
- **WHILE** 데이터가 로드 완료된 상태일 때, 시스템은 모든 계산 기능을 활성화해야 한다

---

## Constraints (제약사항)

### DATA-001-C01: 데이터 구조 제약
- data.json은 UTF-8 인코딩이어야 한다
- JSON 파일 크기는 10KB를 초과하지 않아야 한다
- 모든 숫자 값은 소수점 형태로 저장해야 한다 (예: 40% → 0.40)

### DATA-001-C02: 네트워크 제약
- fetch 요청 타임아웃은 5초를 초과하지 않아야 한다
- CORS 에러 방지를 위해 같은 도메인에서 호스팅해야 한다

---

## 데이터 스키마

### data.json 구조

```json
{
  "updated_at": "2025-12-05",
  "nps": {
    "a_value": 2989352,
    "replacement_rate": 0.40,
    "max_monthly_income": 5900000,
    "min_monthly_income": 370000
  },
  "market": {
    "sp500_10yr_avg": 0.10,
    "kospi_10yr_avg": 0.05,
    "inflation_rate": 0.025
  },
  "wage_curve": {
    "20s": 0.05,
    "30s": 0.05,
    "40s": 0.03,
    "50s_early": 0.00,
    "50s_late": -0.02
  }
}
```

### 필드 설명

| 필드 | 타입 | 설명 | 단위 |
|------|------|------|------|
| `updated_at` | string | 데이터 갱신일 | YYYY-MM-DD |
| `nps.a_value` | number | 국민연금 A값 (전년도 평균소득) | 원/년 |
| `nps.replacement_rate` | number | 소득대체율 | 비율 (0~1) |
| `nps.max_monthly_income` | number | 기준소득월액 상한 | 원/월 |
| `nps.min_monthly_income` | number | 기준소득월액 하한 | 원/월 |
| `market.sp500_10yr_avg` | number | S&P500 10년 평균 수익률 | 비율 (0~1) |
| `market.kospi_10yr_avg` | number | KOSPI 10년 평균 수익률 | 비율 (0~1) |
| `market.inflation_rate` | number | 물가상승률 | 비율 (0~1) |
| `wage_curve.20s` | number | 20대 연 임금상승률 | 비율 (-1~1) |
| `wage_curve.30s` | number | 30대 연 임금상승률 | 비율 (-1~1) |
| `wage_curve.40s` | number | 40대 연 임금상승률 | 비율 (-1~1) |
| `wage_curve.50s_early` | number | 50대 초반 연 임금상승률 | 비율 (-1~1) |
| `wage_curve.50s_late` | number | 55세 이후 연 임금상승률 (임금피크) | 비율 (-1~1) |

### 기본값 (폴백)

```javascript
const DEFAULT_DATA = {
  updated_at: "2025-01-01",
  nps: {
    a_value: 2989352,
    replacement_rate: 0.40,
    max_monthly_income: 5900000,
    min_monthly_income: 370000
  },
  market: {
    sp500_10yr_avg: 0.08,
    kospi_10yr_avg: 0.05,
    inflation_rate: 0.025
  },
  wage_curve: {
    "20s": 0.05,
    "30s": 0.05,
    "40s": 0.03,
    "50s_early": 0.00,
    "50s_late": -0.02
  }
};
```

---

## 인터페이스

### 로딩 함수

```javascript
/**
 * data.json을 비동기로 로드하고 전역 변수에 저장
 * @returns {Promise<Object>} 로드된 데이터 또는 기본값
 */
async function loadData() { ... }

/**
 * 데이터 필드 검증
 * @param {Object} data - 로드된 JSON 데이터
 * @returns {Object} 검증 및 기본값 병합된 데이터
 */
function validateData(data) { ... }

/**
 * 특정 데이터 조회
 * @param {string} path - 점 표기법 경로 (예: "nps.a_value")
 * @returns {*} 해당 경로의 값
 */
function getData(path) { ... }
```

---

## 테스트 시나리오

### TC-DATA-001-01: 정상 로드
- **Given**: data.json 파일이 올바른 형식으로 존재
- **When**: 페이지 로드
- **Then**: 데이터가 전역 변수에 저장됨

### TC-DATA-001-02: 로드 실패 폴백
- **Given**: data.json 파일이 없거나 네트워크 오류
- **When**: 페이지 로드
- **Then**: 기본값이 사용됨, 콘솔에 경고 메시지

### TC-DATA-001-03: 부분 데이터 병합
- **Given**: data.json에 일부 필드만 존재
- **When**: 페이지 로드
- **Then**: 누락된 필드는 기본값으로 채워짐

---

## 관련 문서

- **구조 설계**: `.moai/project/structure.md#integration-001`
- **기술 스택**: `.moai/project/tech.md#deploy-001`
- **의존 SPEC**: CALC-001, CALC-002, CALC-003, TAX-001 (모두 이 SPEC에 의존)

---

_이 SPEC은 `/alfred:2-build DATA-001` 실행 시 TDD 구현의 기준이 됩니다._
