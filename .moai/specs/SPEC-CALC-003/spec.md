---
id: CALC-003
version: 0.0.1
status: draft
created: 2025-12-06
updated: 2025-12-06
author: @Alfred
priority: high
category: feature
labels:
  - calculation
  - private-pension
  - investment
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

# @SPEC:CALC-003: 개인연금 복리 계산

## HISTORY

### v0.0.1 (2025-12-06)
- **INITIAL**: 개인연금 복리 계산 로직 명세 작성
- **AUTHOR**: @Alfred
- **REASON**: 국민연금과 동일 금액을 개인연금에 투자했을 때 예상 수령액 비교

---

## 개요

국민연금 납입액(9%)과 동일한 금액을 개인연금 상품에 투자했을 때의 예상 수령액을 계산합니다.
S&P500 ETF, TDF 2050, 예금형 등 다양한 상품을 비교합니다.

---

## Ubiquitous Requirements (기본 요구사항)

- 시스템은 소득 배열과 상품 정보를 입력받아 개인연금 예상 적립액을 계산해야 한다
- 시스템은 복리 수익률과 수수료(보수율)를 반영해야 한다
- 시스템은 여러 상품을 동시에 비교할 수 있어야 한다

---

## Event-driven Requirements (이벤트 기반)

### CALC-003-E01: 개인연금 계산
- **WHEN** calculatePrivatePension(incomes, product)가 호출되면, 시스템은 예상 적립액을 반환해야 한다
- **WHEN** 상품이 지정되지 않으면, 시스템은 모든 기본 상품에 대해 계산해야 한다

---

## Constraints (제약사항)

- 납입액은 국민연금 납입액(소득의 9%)과 동일하게 가정한다
- 수익률에서 수수료를 차감한 실질 수익률을 적용한다
- 계산 결과는 정수(원 단위)로 반올림해야 한다

---

## 인터페이스

```javascript
/**
 * 개인연금 상품 정보
 */
const PRIVATE_PENSION_PRODUCTS = [
  { id: 'sp500', name: 'S&P500 ETF', return: 0.08, fee: 0.0003 },
  { id: 'tdf2050', name: 'TDF 2050', return: 0.05, fee: 0.005 },
  { id: 'savings', name: '예금형', return: 0.025, fee: 0 }
];

/**
 * 개인연금 예상 적립액 계산
 * @param {Array<{age: number, income: number}>} incomes - 연도별 소득 배열
 * @param {Object} product - 상품 정보 (선택, 미지정 시 전체 상품)
 * @returns {{
 *   productId: string,
 *   productName: string,
 *   totalContribution: number,  // 총 납입액
 *   totalBalance: number,       // 총 적립액 (복리)
 *   monthlyBenefit: number      // 월 예상 수령액 (20년 분할)
 * }[]}
 */
function calculatePrivatePension(incomes, product) { ... }
```

---

## 계산 로직

```
개인연금 복리 산식:
- 연간 납입액 = 소득 × 9% (국민연금과 동일)
- 실질 수익률 = 수익률 - 수수료
- 연도별 적립액 = 이전 잔액 × (1 + 실질수익률) + 당해 납입액

월 예상 수령액 (60세 이후 20년 분할):
- 월 수령액 = 총 적립액 / (20년 × 12개월)

예시: S&P500 ETF (수익률 8%, 수수료 0.03%)
- 30세, 연봉 5000만원
- 연간 납입액: 5000만원 × 9% = 450만원
- 실질 수익률: 8% - 0.03% = 7.97%
```

---

_이 SPEC은 `/alfred:2-build CALC-003` 실행 시 TDD 구현의 기준이 됩니다._
