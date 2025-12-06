---
id: TAX-001
version: 0.1.0
status: completed
created: 2025-12-06
updated: 2025-12-06
author: @Alfred
priority: medium
category: feature
labels:
  - calculation
  - tax
  - pension
depends_on:
  - CALC-001
  - CALC-002
  - CALC-003
blocks:
  - UI-002
scope:
  files:
    - index.html
---

# @SPEC:TAX-001: 세금 계산 로직

## HISTORY

### v0.0.1 (2025-12-06)
- **INITIAL**: 연금소득세 계산 로직 명세 작성
- **AUTHOR**: @Alfred
- **REASON**: 세후 수령액 비교를 위한 세금 계산 기능

---

## 개요

국민연금과 개인연금의 세후 수령액을 계산합니다.
연금소득세를 적용하여 실질 수령액을 비교할 수 있도록 합니다.

---

## Ubiquitous Requirements (기본 요구사항)

- 시스템은 국민연금 수령액에 대한 세금을 계산해야 한다
- 시스템은 개인연금 수령액에 대한 세금을 계산해야 한다
- 시스템은 세전/세후 금액을 모두 제공해야 한다

---

## Event-driven Requirements (이벤트 기반)

### TAX-001-E01: 국민연금 세금 계산
- **WHEN** calculateNPSTax(monthlyBenefit)가 호출되면, 시스템은 연금소득세를 계산해야 한다
- **WHEN** 월 수령액이 과세 기준 이하이면, 시스템은 세금 0을 반환해야 한다

### TAX-001-E02: 개인연금 세금 계산
- **WHEN** calculatePrivatePensionTax(monthlyBenefit, age)가 호출되면, 시스템은 연령별 세율을 적용해야 한다
- **WHEN** 수령자 연령이 70세 미만이면, 시스템은 5.5% 세율을 적용해야 한다
- **WHEN** 수령자 연령이 70~79세이면, 시스템은 4.4% 세율을 적용해야 한다
- **WHEN** 수령자 연령이 80세 이상이면, 시스템은 3.3% 세율을 적용해야 한다

---

## Constraints (제약사항)

- 계산 결과는 정수(원 단위)로 반올림해야 한다
- 세금은 음수가 될 수 없다
- 간소화된 세율 적용 (실제 세법과 다를 수 있음)

---

## 인터페이스

```javascript
/**
 * 국민연금 세금 계산 (간이세액표 간소화)
 * @param {number} monthlyBenefit - 월 수령액
 * @returns {{
 *   grossAmount: number,    // 세전 금액
 *   taxAmount: number,      // 세금
 *   netAmount: number       // 세후 금액
 * }}
 */
function calculateNPSTax(monthlyBenefit) { ... }

/**
 * 개인연금 세금 계산
 * @param {number} monthlyBenefit - 월 수령액
 * @param {number} age - 수령 시 연령 (기본값: 60)
 * @returns {{
 *   grossAmount: number,    // 세전 금액
 *   taxAmount: number,      // 세금
 *   netAmount: number,      // 세후 금액
 *   taxRate: number         // 적용 세율
 * }}
 */
function calculatePrivatePensionTax(monthlyBenefit, age = 60) { ... }
```

---

## 계산 로직

```
국민연금 세금 (간소화):
- 연금소득 간이세액표 기반
- 연간 350만원 이하: 비과세
- 연간 350만원 초과분: 약 5% 적용 (간소화)

개인연금 세금:
- 연금소득세 (분리과세 선택 시)
- 70세 미만: 5.5% (소득세 5% + 지방소득세 0.5%)
- 70~79세: 4.4%
- 80세 이상: 3.3%

예시: 월 100만원 국민연금 수령 (연 1,200만원)
- 과세 대상: 1,200만원 - 350만원 = 850만원
- 세금: 850만원 × 5% = 42.5만원 (연간)
- 월 세금: 약 35,417원
```

---

_이 SPEC은 `/alfred:2-build TAX-001` 실행 시 TDD 구현의 기준이 됩니다._
