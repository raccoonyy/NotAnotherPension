---
id: CALC-001
version: 0.0.1
status: draft
created: 2025-12-06
updated: 2025-12-06
author: @Alfred
priority: high
category: feature
labels:
  - calculation
  - wage
  - core
depends_on:
  - DATA-001
blocks:
  - CALC-002
  - UI-002
scope:
  files:
    - index.html
---

# @SPEC:CALC-001: 임금 상승 곡선 계산

## HISTORY

### v0.0.1 (2025-12-06)
- **INITIAL**: 임금 상승 곡선 계산 로직 명세 작성
- **AUTHOR**: @Alfred
- **REASON**: 연령별 예상 소득을 계산하여 연금 시뮬레이션의 기초 데이터 제공

---

## 개요

사용자의 현재 나이와 소득을 기반으로 60세까지의 연도별 예상 소득을 계산합니다.
한국의 일반적인 임금 곡선(30대 상승 → 40대 완만 → 50대 정체/하락)을 반영합니다.

---

## Ubiquitous Requirements (기본 요구사항)

- 시스템은 현재 나이와 현재 소득을 입력받아 연도별 예상 소득을 계산해야 한다
- 시스템은 연령대별 임금상승률을 data.json에서 로드하여 적용해야 한다
- 시스템은 60세까지의 예상 소득 배열을 반환해야 한다

---

## Event-driven Requirements (이벤트 기반)

### CALC-001-E01: 임금 곡선 계산
- **WHEN** calculateWageCurve(currentAge, currentIncome)가 호출되면, 시스템은 연도별 소득 배열을 반환해야 한다
- **WHEN** 현재 나이가 60세 이상이면, 시스템은 현재 소득만 포함된 배열을 반환해야 한다

---

## Constraints (제약사항)

- 계산 결과는 정수(원 단위)로 반올림해야 한다
- 최소 나이는 20세, 최대 나이는 59세로 제한한다
- 소득은 양수여야 한다

---

## 인터페이스

```javascript
/**
 * 연령별 예상 소득 계산
 * @param {number} currentAge - 현재 나이 (20-59)
 * @param {number} currentIncome - 현재 연소득 (원)
 * @returns {Array<{age: number, year: number, income: number}>} 연도별 소득 배열
 */
function calculateWageCurve(currentAge, currentIncome) { ... }
```

---

## 계산 로직

```
연령대별 상승률 (data.json 기준):
- 20대: +5%/년
- 30대: +5%/년
- 40대: +3%/년
- 50대 초반 (50-54): 0%/년
- 50대 후반 (55-59): -2%/년 (임금피크)

예시: 30세, 연봉 5000만원
- 31세: 5000 × 1.05 = 5250만원
- 32세: 5250 × 1.05 = 5512만원
- ...
- 40세: 3% 상승 적용
- ...
- 55세: -2% 적용 (임금피크)
```

---

_이 SPEC은 `/alfred:2-build CALC-001` 실행 시 TDD 구현의 기준이 됩니다._
