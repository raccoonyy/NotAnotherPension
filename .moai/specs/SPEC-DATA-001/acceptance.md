# DATA-001 인수 테스트

> **SPEC**: @SPEC:DATA-001
> **작성일**: 2025-12-05
> **작성자**: @Alfred

---

## 테스트 개요

| 항목 | 내용 |
|------|------|
| **테스트 방식** | 브라우저 콘솔 수동 테스트 |
| **테스트 환경** | Chrome/Firefox/Safari/Edge |
| **사전 조건** | 로컬 서버 실행 (`python -m http.server 8000`) |

---

## Given-When-Then 시나리오

### AC-DATA-001-01: 정상 데이터 로드

```gherkin
Feature: data.json 정상 로드

  Scenario: 페이지 로드 시 데이터 파일 로드
    Given data.json 파일이 프로젝트 루트에 존재하고
    And 파일 내용이 유효한 JSON 형식일 때
    When 사용자가 index.html 페이지에 접속하면
    Then APP_DATA 전역 변수에 데이터가 저장되고
    And 콘솔에 "데이터 로드 완료" 메시지가 출력된다

  검증 방법:
    1. 브라우저 개발자 도구 열기 (F12)
    2. Console 탭에서 확인:
       > APP_DATA
       > APP_DATA.nps.a_value  // 예: 2989352
       > APP_DATA.updated_at   // 예: "2025-12-05"
```

---

### AC-DATA-001-02: 데이터 로드 실패 시 폴백

```gherkin
Feature: 로드 실패 시 기본값 사용

  Scenario: 네트워크 오류 또는 파일 없음
    Given data.json 파일이 존재하지 않거나
    And 네트워크 요청이 실패할 때
    When 사용자가 index.html 페이지에 접속하면
    Then APP_DATA에 기본값(DEFAULT_DATA)이 저장되고
    And 콘솔에 "data.json 로드 실패, 기본값 사용" 경고가 출력된다

  검증 방법:
    1. data.json 파일을 임시로 삭제 또는 이름 변경
    2. 페이지 새로고침
    3. Console에서 확인:
       > APP_DATA.nps.a_value  // 기본값: 2989352
    4. 경고 메시지 확인
```

---

### AC-DATA-001-03: 부분 데이터 병합

```gherkin
Feature: 누락된 필드 기본값 병합

  Scenario: 일부 필드만 존재하는 JSON
    Given data.json에 nps 섹션만 존재하고
    And market, wage_curve 섹션이 누락되었을 때
    When 데이터가 로드되면
    Then 누락된 필드는 DEFAULT_DATA의 값으로 채워진다

  검증 방법:
    1. data.json을 아래처럼 수정:
       {"nps": {"a_value": 3000000}}
    2. 페이지 새로고침
    3. Console에서 확인:
       > APP_DATA.nps.a_value          // 3000000 (로드된 값)
       > APP_DATA.market.sp500_10yr_avg // 0.08 (기본값)
       > APP_DATA.wage_curve['30s']     // 0.05 (기본값)
```

---

### AC-DATA-001-04: getData 함수 조회

```gherkin
Feature: 점 표기법 데이터 조회

  Scenario: getData로 중첩 데이터 조회
    Given 데이터가 정상 로드되었을 때
    When getData('nps.a_value')를 호출하면
    Then 해당 경로의 값이 반환된다

  검증 방법:
    1. Console에서 실행:
       > getData('nps.a_value')         // 2989352
       > getData('market.inflation_rate') // 0.025
       > getData('wage_curve.50s_late') // -0.02
       > getData('invalid.path')        // undefined
```

---

### AC-DATA-001-05: 데이터 타입 검증

```gherkin
Feature: 데이터 타입 유효성

  Scenario: 모든 숫자 필드가 number 타입
    Given 데이터가 로드되었을 때
    When 각 숫자 필드를 확인하면
    Then typeof 결과가 'number'여야 한다

  검증 방법:
    Console에서 실행:
    > typeof APP_DATA.nps.a_value === 'number'           // true
    > typeof APP_DATA.nps.replacement_rate === 'number'  // true
    > typeof APP_DATA.market.sp500_10yr_avg === 'number' // true
    > typeof APP_DATA.wage_curve['30s'] === 'number'     // true
```

---

## 체크리스트

### 기능 요구사항

- [ ] **AC-01**: data.json이 정상 로드되면 APP_DATA에 저장
- [ ] **AC-02**: 로드 실패 시 기본값 사용 및 경고 메시지
- [ ] **AC-03**: 부분 데이터 시 누락 필드 기본값 병합
- [ ] **AC-04**: getData() 함수로 점 표기법 조회 가능
- [ ] **AC-05**: 모든 숫자 필드가 number 타입

### 비기능 요구사항

- [ ] 데이터 로드 시간 < 1초
- [ ] JSON 파일 크기 < 10KB
- [ ] UTF-8 인코딩 확인
- [ ] 타임아웃 5초 이내 처리

### 브라우저 호환성

- [ ] Chrome (최신 버전)
- [ ] Firefox (최신 버전)
- [ ] Safari (최신 버전)
- [ ] Edge (최신 버전)

---

## 테스트 실행 가이드

### 1. 로컬 서버 실행

```bash
cd /Users/alan.kim/workspace/yourfuture
python -m http.server 8000
```

### 2. 브라우저에서 접속

```
http://localhost:8000
```

### 3. 개발자 도구 열기

- Windows/Linux: `F12` 또는 `Ctrl+Shift+I`
- Mac: `Cmd+Option+I`

### 4. Console 탭에서 테스트 실행

```javascript
// 전체 데이터 확인
console.log(APP_DATA);

// 개별 필드 확인
console.log('A값:', APP_DATA.nps.a_value);
console.log('S&P500 수익률:', APP_DATA.market.sp500_10yr_avg);
console.log('30대 임금상승률:', APP_DATA.wage_curve['30s']);

// getData 테스트
console.log(getData('nps.replacement_rate'));
```

---

## 자동화 테스트 스크립트 (선택)

```javascript
// test-data.js - Console에서 실행
(function testDataModule() {
  const tests = [
    {
      name: 'APP_DATA 존재',
      test: () => APP_DATA !== null
    },
    {
      name: 'nps.a_value가 숫자',
      test: () => typeof APP_DATA.nps.a_value === 'number'
    },
    {
      name: 'a_value가 양수',
      test: () => APP_DATA.nps.a_value > 0
    },
    {
      name: 'replacement_rate가 0~1 사이',
      test: () => APP_DATA.nps.replacement_rate >= 0 && APP_DATA.nps.replacement_rate <= 1
    },
    {
      name: 'getData 함수 동작',
      test: () => getData('nps.a_value') === APP_DATA.nps.a_value
    },
    {
      name: 'getData 잘못된 경로',
      test: () => getData('invalid.path') === undefined
    }
  ];

  console.log('=== DATA-001 테스트 시작 ===');
  let passed = 0;
  tests.forEach(t => {
    try {
      const result = t.test();
      console.log(result ? '✅' : '❌', t.name);
      if (result) passed++;
    } catch (e) {
      console.log('❌', t.name, '- Error:', e.message);
    }
  });
  console.log(`=== 결과: ${passed}/${tests.length} 통과 ===`);
})();
```

---

_이 인수 테스트는 `/alfred:2-build DATA-001` 완료 후 검증에 사용됩니다._
