---
id: UI-001
version: 0.1.0
status: completed
created: 2025-12-06
updated: 2025-12-06
author: @Alfred
priority: medium
category: feature
labels:
  - ui
  - form
  - input
depends_on: []
blocks:
  - UI-002
scope:
  files:
    - index.html
---

# @SPEC:UI-001: 입력 폼 구현

## HISTORY

### v0.0.1 (2025-12-06)
- **INITIAL**: 입력 폼 UI 명세 작성
- **AUTHOR**: @Alfred
- **REASON**: 사용자 정보 입력을 위한 폼 구현

---

## 개요

사용자의 직업 구분, 현재 나이, 현재 소득 정보를 입력받는 폼을 구현합니다.
근로자와 사업자에 따라 입력 필드가 다르게 표시됩니다.

---

## Ubiquitous Requirements (기본 요구사항)

- 시스템은 직업 구분 선택 (근로자/사업자)을 제공해야 한다
- 시스템은 현재 나이 입력 필드를 제공해야 한다
- 시스템은 소득 입력 필드를 제공해야 한다
- 시스템은 계산하기 버튼을 제공해야 한다

---

## Event-driven Requirements (이벤트 기반)

### UI-001-E01: 직업 구분 전환
- **WHEN** 사용자가 근로자를 선택하면, 시스템은 연봉 입력 필드를 표시해야 한다
- **WHEN** 사용자가 사업자를 선택하면, 시스템은 월평균 사업소득 입력 필드를 표시해야 한다

### UI-001-E02: 계산 실행
- **WHEN** 사용자가 계산하기 버튼을 클릭하면, 시스템은 입력값을 검증해야 한다
- **WHEN** 입력값이 유효하면, 시스템은 결과 테이블을 생성해야 한다
- **WHEN** 입력값이 유효하지 않으면, 시스템은 오류 메시지를 표시해야 한다

---

## Constraints (제약사항)

- 나이는 20-59세 범위로 제한한다
- 소득은 양수여야 한다
- 모든 입력 필드는 숫자만 허용한다

---

## 인터페이스

```javascript
/**
 * 폼 데이터 수집
 * @returns {{
 *   jobType: 'laborer' | 'business',
 *   currentAge: number,
 *   currentIncome: number,
 *   isValid: boolean,
 *   errors: string[]
 * }}
 */
function getFormData() { ... }

/**
 * 폼 데이터 검증
 * @param {Object} data - 폼 데이터
 * @returns {{isValid: boolean, errors: string[]}}
 */
function validateFormData(data) { ... }

/**
 * 계산 실행 및 결과 표시
 * @param {Object} data - 검증된 폼 데이터
 */
function executeCalculation(data) { ... }
```

---

## UI 레이아웃

```
┌─────────────────────────────────────────┐
│ 직업 구분: [근로자 ●] [사업자 ○]        │
├─────────────────────────────────────────┤
│ 현재 나이: [30] 세                      │
├─────────────────────────────────────────┤
│ (근로자) 현재 연봉: [5,000] 만원        │
│ (사업자) 월평균 사업소득: [   ] 만원    │
└─────────────────────────────────────────┘
         [계산하기]
```

---

_이 SPEC은 `/alfred:2-build UI-001` 실행 시 TDD 구현의 기준이 됩니다._
