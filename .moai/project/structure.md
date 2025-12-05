---
id: STRUCTURE-001
version: 0.3.0
status: active
created: 2025-10-01
updated: 2025-12-05
author: @architect
priority: medium
---

# yourfuture Structure Design

## HISTORY

### v0.3.0 (2025-12-05)
- **UPDATED**: Vanilla JS + 단일 파일 구조로 변경
- **AUTHOR**: @Alfred
- **SECTIONS**: 아키텍처, 파일 구조, 모듈 설계 전면 변경
- **REASON**: 사용자 프롬프트 기반 (빌드 없는 단순 구조)

### v0.2.0 (2025-12-05)
- **UPDATED**: Next.js SSG 아키텍처로 설계
- **AUTHOR**: @Alfred

### v0.1.0 (2025-10-01)
- **INITIAL**: 프로젝트 구조 설계 문서 작성
- **AUTHOR**: @architect

---

## @DOC:ARCHITECTURE-001 시스템 아키텍처

### 아키텍처 전략

**정적 단일 페이지 (No Build SPA)** - Vanilla JS + HTML

```
yourfuture Architecture
├── Presentation Layer     # HTML + Tailwind CSS (CDN)
├── Application Layer      # Vanilla JavaScript (단일 파일 내)
├── Data Layer             # data.json (fetch로 로드)
└── Automation Layer       # Python 스크립트 (데이터 갱신)
```

**선택 이유**:
- **빌드 없음**: npm install, webpack 등 빌드 과정 불필요
- **즉시 실행**: index.html 더블클릭으로 바로 실행
- **서버 불필요**: 모든 로직이 브라우저에서 실행
- **GitHub Pages 배포**: 정적 파일만으로 배포 가능
- **유지보수 용이**: 단일 파일로 전체 로직 파악 가능

### 파일 구조

```
yourfuture/
├── index.html              # 메인 페이지 (모든 로직 포함)
│   ├── <style>             # Tailwind CSS (CDN) + 커스텀 스타일
│   ├── <script>            # 모든 JavaScript 로직
│   │   ├── 상수 정의        # 임금 상승률, 연금 상품 정보
│   │   ├── 계산 함수        # 임금/국민연금/개인연금/세금
│   │   ├── UI 함수          # 테이블 생성, 이벤트 핸들링
│   │   └── 초기화          # data.json 로드, 이벤트 바인딩
│   └── <body>              # HTML 마크업
│
├── data.json               # 외부 데이터 (Python으로 갱신)
│   ├── nps_a_value         # 국민연금 A값 (평균소득)
│   ├── inflation_rate      # 물가상승률
│   ├── market_returns      # 시장 수익률 (S&P500 등)
│   └── updated_at          # 마지막 갱신일
│
├── update_data.py          # 데이터 갱신 스크립트 (Python)
│
├── .moai/                  # MoAI-ADK 설정 (유지)
├── .claude/                # Claude Code 설정 (유지)
└── CLAUDE.md               # 프로젝트 가이드
```

## @DOC:MODULES-001 모듈별 책임 구분

### 1. 상수 정의 (Constants)

```javascript
// 임금 상승 곡선 (Wage Curve)
const WAGE_GROWTH_RATES = { ... };

// 국민연금 상수
const NPS_CONSTANTS = {
  EMPLOYEE_RATE: 0.045,   // 근로자 본인 부담률
  EMPLOYER_RATE: 0.045,   // 회사 부담률
  SELF_EMPLOYED_RATE: 0.09, // 사업자 부담률
  REPLACEMENT_RATE: 0.40  // 소득대체율 (현행)
};

// 개인연금 상품 정보
const PRIVATE_PENSION_PRODUCTS = [
  { name: 'S&P500 ETF', return: 0.08, fee: 0.0003 },
  { name: 'TDF 2050', return: 0.05, fee: 0.005 },
  { name: '예금형', return: 0.025, fee: 0 }
];

// 세금 상수
const TAX_RATES = {
  PENSION_INCOME_TAX: 0.055,  // 연금소득세 (70세 미만)
  PENSION_INCOME_TAX_70: 0.044,
  PENSION_INCOME_TAX_85: 0.033
};
```

### 2. 계산 함수 (Calculation Functions)

| 함수 | 역할 | 입력 | 출력 |
|------|------|------|------|
| `calculateWageCurve()` | 연령별 예상 소득 계산 | 현재나이, 현재소득 | 연도별 소득 배열 |
| `calculateNPS()` | 국민연금 예상액 계산 | 소득 배열, 직업유형 | 예상 수령액 |
| `calculatePrivatePension()` | 개인연금 예상액 계산 | 납입액, 상품정보 | 예상 수령액 |
| `calculateTax()` | 세금 계산 | 세전 수령액, 연금유형 | 세후 수령액 |

### 3. UI 함수 (UI Functions)

| 함수 | 역할 |
|------|------|
| `renderInputForm()` | 직업별 입력 폼 렌더링 |
| `renderResultTable()` | 가로 스크롤 결과 테이블 생성 |
| `createTooltip()` | 세금 설명 툴팁 생성 |
| `formatCurrency()` | 금액 포맷팅 (만원 단위) |

### 4. 이벤트 핸들러 (Event Handlers)

| 이벤트 | 핸들러 |
|--------|--------|
| 직업 선택 변경 | `onJobTypeChange()` |
| 계산하기 버튼 클릭 | `onCalculate()` |
| 입력값 변경 | `onInputChange()` |

## @DOC:INTEGRATION-001 외부 시스템 통합

### data.json 연동

- **로딩 방식**: `fetch('/data.json')` (비동기)
- **폴백 처리**: 로드 실패 시 하드코딩된 기본값 사용
- **갱신 주기**: Python 스크립트로 수동/자동 갱신

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

### Python 스크립트 (update_data.py)

- **역할**: data.json 자동 갱신
- **데이터 소스**:
  - 국민연금 A값: 국민연금공단 (하드코딩 또는 API)
  - 물가상승률: 통계청 (하드코딩 또는 API)
  - 시장 수익률: Yahoo Finance 등 (하드코딩 또는 API)
- **실행 방식**: 수동 실행 또는 GitHub Actions 연동

### GitHub Pages 배포

- **배포 파일**: `index.html`, `data.json`
- **배포 방법**: main 브랜치 푸시 → 자동 배포
- **URL**: `https://{username}.github.io/yourfuture/`

## @DOC:TRACEABILITY-001 추적성 전략

### TAG 체계 적용

**TDD 완벽 정렬**: SPEC → 테스트 → 구현 → 문서
- `@SPEC:ID` (.moai/specs/) → `@TEST:ID` (tests/) → `@CODE:ID` (index.html 내) → `@DOC:ID` (docs/)

**구현 세부사항**: @CODE:ID 주석 레벨
- `@CODE:ID:CALC` - 계산 로직 (임금, 연금, 세금)
- `@CODE:ID:UI` - UI 함수 (테이블, 폼, 툴팁)
- `@CODE:ID:DATA` - 데이터 로딩 및 처리
- `@CODE:ID:EVENT` - 이벤트 핸들러

### 코드 내 TAG 예시

```javascript
// @CODE:CALC-001:WAGE | SPEC: SPEC-CALC-001.md
function calculateWageCurve(currentAge, currentIncome) {
  // 임금 상승 곡선 계산 로직
}

// @CODE:CALC-002:NPS | SPEC: SPEC-CALC-002.md
function calculateNPS(incomes, jobType) {
  // 국민연금 예상 수령액 계산
}
```

## Legacy Context

### 기존 시스템 현황

**MoAI-ADK 초기화 완료 상태**

```
기존 구조/
├── .moai/                # MoAI-ADK 설정 (유지)
├── .claude/              # Claude Code 설정 (유지)
└── CLAUDE.md             # 프로젝트 가이드 (유지)
```

### 변경 사항 요약

| 항목 | 이전 (v0.2.0) | 현재 (v0.3.0) |
|------|--------------|--------------|
| 프레임워크 | Next.js + React | Vanilla JS |
| 빌드 | 필요 (npm run build) | 불필요 |
| 파일 구조 | 다중 파일/폴더 | 단일 HTML 파일 |
| 스타일링 | Tailwind + shadcn/ui | Tailwind CSS (CDN) |
| 데이터 | 하드코딩 | data.json + Python |

## TODO:STRUCTURE-001 구조 개선 계획

1. **코드 모듈화**: 로직이 커지면 별도 JS 파일로 분리 검토
2. **테스트 전략**: 브라우저 기반 수동 테스트 + 계산 로직 단위 테스트
3. **PWA 검토**: Service Worker 추가하여 오프라인 지원 (향후)

---

_이 구조는 `/alfred:2-build` 실행 시 TDD 구현의 가이드라인이 됩니다._
