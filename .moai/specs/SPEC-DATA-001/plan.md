# DATA-001 구현 계획

> **SPEC**: @SPEC:DATA-001
> **작성일**: 2025-12-05
> **작성자**: @Alfred

---

## 구현 개요

| 항목 | 내용 |
|------|------|
| **목표** | data.json 파일 생성 및 로딩 시스템 구현 |
| **산출물** | data.json, index.html 내 로딩 로직 |
| **의존성** | 없음 (최초 구현) |
| **블로킹** | CALC-001, CALC-002, CALC-003, TAX-001 |

---

## TDD 구현 단계

### Phase 1: RED - 실패하는 테스트 작성

**1.1 데이터 로딩 테스트**
```javascript
// 브라우저 콘솔에서 실행
console.assert(
  typeof loadData === 'function',
  'loadData 함수가 존재해야 함'
);

console.assert(
  typeof validateData === 'function',
  'validateData 함수가 존재해야 함'
);

console.assert(
  typeof getData === 'function',
  'getData 함수가 존재해야 함'
);
```

**1.2 데이터 구조 테스트**
```javascript
// data.json 로드 후 실행
const data = await loadData();

console.assert(
  data.nps && typeof data.nps.a_value === 'number',
  'nps.a_value가 숫자여야 함'
);

console.assert(
  data.market && typeof data.market.sp500_10yr_avg === 'number',
  'market.sp500_10yr_avg가 숫자여야 함'
);

console.assert(
  data.wage_curve && typeof data.wage_curve['30s'] === 'number',
  'wage_curve.30s가 숫자여야 함'
);
```

**1.3 폴백 테스트**
```javascript
// 네트워크 오류 시뮬레이션
// data.json을 일시적으로 제거하고 테스트
const data = await loadData();
console.assert(
  data.nps.a_value > 0,
  '로드 실패 시에도 기본값이 있어야 함'
);
```

---

### Phase 2: GREEN - 최소 구현

**2.1 data.json 파일 생성**
- 위치: 프로젝트 루트 `/data.json`
- 초기 데이터 삽입 (2024년 기준)

**2.2 index.html 내 로딩 로직**
```javascript
// 전역 변수
let APP_DATA = null;

// 기본값 정의
const DEFAULT_DATA = { ... };

// 로딩 함수
async function loadData() {
  try {
    const response = await fetch('/data.json');
    if (!response.ok) throw new Error('Fetch failed');
    const data = await response.json();
    APP_DATA = validateData(data);
    return APP_DATA;
  } catch (error) {
    console.warn('data.json 로드 실패, 기본값 사용:', error);
    APP_DATA = DEFAULT_DATA;
    return APP_DATA;
  }
}

// 검증 함수
function validateData(data) {
  return {
    updated_at: data.updated_at || DEFAULT_DATA.updated_at,
    nps: { ...DEFAULT_DATA.nps, ...data.nps },
    market: { ...DEFAULT_DATA.market, ...data.market },
    wage_curve: { ...DEFAULT_DATA.wage_curve, ...data.wage_curve }
  };
}

// 데이터 조회 함수
function getData(path) {
  const keys = path.split('.');
  let value = APP_DATA;
  for (const key of keys) {
    value = value?.[key];
  }
  return value;
}
```

**2.3 페이지 초기화 시 호출**
```javascript
document.addEventListener('DOMContentLoaded', async () => {
  await loadData();
  console.log('데이터 로드 완료:', APP_DATA.updated_at);
  // 계산 기능 활성화
  enableCalculation();
});
```

---

### Phase 3: REFACTOR - 코드 품질 개선

**3.1 에러 핸들링 강화**
- 타임아웃 추가 (5초)
- 상세 에러 메시지

**3.2 성능 최적화**
- 데이터 캐싱 (세션 스토리지)
- 중복 로드 방지

**3.3 문서화**
- JSDoc 주석 추가
- @CODE:DATA-001 TAG 삽입

---

## 파일별 작업 목록

### 1. data.json (신규 생성)
```
위치: /data.json
크기: ~500 bytes
역할: 외부 데이터 저장소
```

### 2. index.html (수정)
```
위치: /index.html
섹션: <script> 태그 내부
역할: 로딩 로직 추가
```

### 3. update_data.py (신규 생성 - 선택)
```
위치: /update_data.py
역할: data.json 자동 갱신 스크립트
의존성: requests 라이브러리
```

---

## 예상 일정

| 단계 | 작업 | 예상 시간 |
|------|------|----------|
| RED | 테스트 케이스 작성 | - |
| GREEN | data.json + 로딩 로직 | - |
| REFACTOR | 에러 핸들링, 문서화 | - |

---

## 완료 기준

- [ ] data.json 파일 생성 및 유효한 JSON 형식
- [ ] loadData() 함수가 정상 동작
- [ ] validateData() 함수가 누락 필드를 기본값으로 채움
- [ ] getData() 함수가 점 표기법으로 값 조회
- [ ] 네트워크 오류 시 기본값 사용
- [ ] @CODE:DATA-001 TAG 삽입
- [ ] 모든 테스트 통과

---

## 위험 요소 및 대응

| 위험 | 영향 | 대응 |
|------|------|------|
| CORS 에러 | 데이터 로드 실패 | 같은 도메인에서 호스팅, 기본값 폴백 |
| JSON 파싱 오류 | 앱 크래시 | try-catch로 예외 처리 |
| 데이터 누락 | 계산 오류 | 기본값 병합으로 안전하게 처리 |

---

_이 계획은 `/alfred:2-build DATA-001` 실행 시 참조됩니다._
