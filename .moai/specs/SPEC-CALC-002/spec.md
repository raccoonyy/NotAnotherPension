---
id: CALC-002
version: 0.1.0
status: completed
created: 2025-12-06
updated: 2025-12-06
author: @Alfred
priority: high
category: feature
labels:
  - calculation
  - nps
  - pension
depends_on:
  - DATA-001
  - CALC-001
blocks:
  - TAX-001
  - UI-002
scope:
  files:
    - index.html
---

# @SPEC:CALC-002: 국민연금 예상 수령액 계산

## HISTORY

### v0.0.1 (2025-12-06)
- **INITIAL**: 국민연금 예상 수령액 계산 로직 명세 작성
- **AUTHOR**: @Alfred
- **REASON**: 국민연금 수령액을 계산하여 개인연금과 비교 가능하게 함

---

## 개요

사용자의 소득 이력을 기반으로 국민연금 예상 수령액을 계산합니다.
근로자(4.5%+4.5%)와 사업자(9%) 구분을 지원합니다.

---

## Ubiquitous Requirements (기본 요구사항)

- 시스템은 소득 배열과 직업 유형을 입력받아 국민연금 예상 수령액을 계산해야 한다
- 시스템은 근로자와 사업자의 보험료율 차이를 반영해야 한다
- 시스템은 국민연금 A값과 소득대체율을 data.json에서 로드하여 적용해야 한다

---

## Event-driven Requirements (이벤트 기반)

### CALC-002-E01: 국민연금 계산
- **WHEN** calculateNPS(incomes, jobType)가 호출되면, 시스템은 월 예상 수령액을 반환해야 한다
- **WHEN** 직업 유형이 'laborer'이면, 시스템은 본인+회사 부담(9%)을 적용해야 한다
- **WHEN** 직업 유형이 'business'이면, 시스템은 본인 전액 부담(9%)을 적용해야 한다

---

## Constraints (제약사항)

- 기준소득월액은 상한(590만원)과 하한(37만원)을 초과/미달하지 않아야 한다
- 계산 결과는 정수(원 단위)로 반올림해야 한다

---

## 인터페이스

```javascript
/**
 * 국민연금 예상 월 수령액 계산
 * @param {Array<{age: number, income: number}>} incomes - 연도별 소득 배열
 * @param {string} jobType - 직업 유형 ('laborer' | 'business')
 * @returns {{
 *   monthlyBenefit: number,      // 월 예상 수령액 (세전)
 *   totalContribution: number,   // 총 납입액
 *   selfContribution: number,    // 본인 부담 총액
 *   employerContribution: number // 회사 부담 총액 (근로자만)
 * }}
 */
function calculateNPS(incomes, jobType) { ... }
```

---

## 계산 로직

```
국민연금 기본 산식 (간소화):
월 수령액 = (A + B) × 소득대체율 × 가입월수/480

- A값: 전체 가입자 평균소득 (data.json에서 로드)
- B값: 본인의 기준소득월액 평균
- 소득대체율: 40% (현행, data.json에서 로드)
- 가입월수: 소득 배열 길이 × 12

근로자 보험료:
- 본인 부담: 소득 × 4.5%
- 회사 부담: 소득 × 4.5%

사업자 보험료:
- 본인 전액: 소득 × 9%
```

---

_이 SPEC은 `/alfred:2-build CALC-002` 실행 시 TDD 구현의 기준이 됩니다._
