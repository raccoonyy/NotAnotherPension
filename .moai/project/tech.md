---
id: TECH-001
version: 0.3.0
status: active
created: 2025-10-01
updated: 2025-12-05
author: @tech-lead
priority: medium
---

# NotAnotherPension Technology Stack

## HISTORY

### v0.3.0 (2025-12-05)
- **UPDATED**: Vanilla JS + HTML + Python 스택으로 변경
- **AUTHOR**: @Alfred
- **SECTIONS**: 전체 기술 스택 전면 변경
- **REASON**: 사용자 프롬프트 기반 (빌드 없는 단순 구조)

### v0.2.0 (2025-12-05)
- **UPDATED**: Next.js + TypeScript + shadcn/ui 스택
- **AUTHOR**: @Alfred

### v0.1.0 (2025-10-01)
- **INITIAL**: 프로젝트 기술 스택 문서 작성
- **AUTHOR**: @tech-lead

---

## @DOC:STACK-001 언어 & 런타임

### Frontend - 주 언어

| 항목 | 선택 | 버전/설명 |
|------|------|----------|
| **마크업** | HTML5 | 시맨틱 태그 활용 |
| **스타일링** | Tailwind CSS | CDN 사용 (빌드 불필요) |
| **스크립트** | Vanilla JavaScript | ES6+ 문법, 모듈 없음 |

**선택 이유**:
- **빌드 과정 없음**: npm, webpack, vite 등 불필요
- **즉시 실행**: 브라우저에서 바로 동작
- **단일 파일**: 모든 로직이 index.html 하나에 포함
- **CDN 활용**: 외부 라이브러리는 CDN으로 로드

### Backend - 자동화

| 항목 | 선택 | 버전/설명 |
|------|------|----------|
| **스크립트** | Python | 3.8+ |
| **HTTP 클라이언트** | requests | 2.x |
| **JSON 처리** | json (built-in) | - |

**선택 이유**:
- **데이터 갱신 자동화**: data.json 주기적 업데이트
- **간단한 스크립트**: API 호출 + JSON 생성
- **GitHub Actions 연동 가능**: 자동 실행 파이프라인

### 런타임 환경

| 환경 | 용도 | 요구사항 |
|------|------|----------|
| **브라우저** | 프로덕션 실행 | ES6+ 지원 (Chrome, Firefox, Safari, Edge) |
| **Python** | 데이터 갱신 | Python 3.8+ |
| **로컬 서버** | 개발 테스트 | Live Server (VS Code) 또는 `python -m http.server` |

## @DOC:FRAMEWORK-001 핵심 라이브러리 (CDN)

### Tailwind CSS

```html
<!-- Tailwind CSS CDN -->
<script src="https://cdn.tailwindcss.com"></script>
```

**용도**: 유틸리티 퍼스트 CSS 스타일링
**버전**: 최신 (CDN 자동 업데이트)

### 선택적 라이브러리 (필요 시 추가)

```html
<!-- Chart.js (차트가 필요한 경우) -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- Day.js (날짜 처리가 필요한 경우) -->
<script src="https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js"></script>
```

## @DOC:QUALITY-001 품질 게이트 & 정책

### 코드 품질 (수동 검증)

| 항목 | 기준 | 검증 방법 |
|------|------|----------|
| **파일 크기** | index.html ≤ 500KB | 파일 크기 확인 |
| **함수 길이** | ≤ 50줄 | 코드 리뷰 |
| **중첩 깊이** | ≤ 3단계 | 코드 리뷰 |

### 브라우저 호환성

| 브라우저 | 지원 상태 | 테스트 방법 |
|----------|-----------|------------|
| Chrome | 완전 지원 | 수동 테스트 |
| Firefox | 완전 지원 | 수동 테스트 |
| Safari | 완전 지원 | 수동 테스트 |
| Edge | 완전 지원 | 수동 테스트 |
| IE11 | 미지원 | - |

### 테스트 전략

**단위 테스트 (계산 로직)**:
```javascript
// 브라우저 콘솔에서 테스트
console.assert(
  calculateWageCurve(30, 5000).length === 31,
  '30세부터 60세까지 31개 연도'
);

console.assert(
  calculateNPS([...], 'laborer') > 0,
  '국민연금 예상액은 양수'
);
```

**통합 테스트 (수동)**:
1. 근로자 입력 → 결과 테이블 확인
2. 사업자 입력 → 결과 테이블 확인
3. 가로 스크롤 동작 확인
4. 툴팁 표시 확인

### 자동화 스크립트

```bash
# 로컬 서버 실행 (개발용)
python -m http.server 8000

# 또는 VS Code Live Server 사용
```

## @DOC:SECURITY-001 보안 정책 & 운영

### 클라이언트 보안

- **XSS 방지**: 사용자 입력값 이스케이핑
- **외부 스크립트**: CDN만 사용 (신뢰할 수 있는 소스)
- **민감 정보**: 클라이언트에 민감 정보 없음

### 데이터 보안

- **서버 전송 없음**: 모든 계산이 브라우저 내에서 수행
- **개인정보 수집 없음**: 입력값은 저장되지 않음
- **URL 공유 시**: 입력값이 URL에 포함될 수 있음 (선택적 기능)

### Python 스크립트 보안

```python
# update_data.py 보안 고려사항
# - API 키는 환경 변수로 관리
# - HTTPS만 사용
# - 응답 데이터 검증
```

## @DOC:DEPLOY-001 배포 채널 & 전략

### 1. 배포 채널

- **주 채널**: GitHub Pages
- **배포 파일**: `index.html`, `data.json`
- **URL**: `https://{username}.github.io/NotAnotherPension/`

### 2. 배포 방법

**수동 배포**:
```bash
git add index.html data.json
git commit -m "Update pension calculator"
git push origin main
# GitHub Pages 자동 배포
```

**GitHub Actions (선택적)**:
```yaml
# .github/workflows/update-data.yml
name: Update Data

on:
  schedule:
    - cron: '0 0 1 * *'  # 매월 1일 실행
  workflow_dispatch:  # 수동 실행

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install requests
      - run: python update_data.py
      - run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add data.json
          git commit -m "Auto-update data.json" || exit 0
          git push
```

### 3. 개발 환경 설정

```bash
# 프로젝트 클론
git clone https://github.com/{username}/NotAnotherPension.git
cd NotAnotherPension

# 로컬 서버 실행 (CORS 문제 방지)
python -m http.server 8000
# 브라우저에서 http://localhost:8000 접속

# 또는 VS Code Live Server 확장 사용
```

### 4. 파일 구조

```
NotAnotherPension/
├── index.html          # 메인 페이지 (필수)
├── data.json           # 데이터 파일 (필수)
├── update_data.py      # 데이터 갱신 스크립트
├── .moai/              # MoAI-ADK 설정
├── .claude/            # Claude Code 설정
├── .github/
│   └── workflows/
│       └── update-data.yml  # 자동 데이터 갱신 (선택)
└── CLAUDE.md           # 프로젝트 가이드
```

## @CODE:TECH-DEBT-001 기술 부채 관리

### 현재 기술 부채

1. **index.html 미생성** - 아직 코드 작성 전 (우선순위: 높음)
2. **data.json 미생성** - 예시 데이터 필요 (우선순위: 높음)
3. **update_data.py 미생성** - Python 스크립트 필요 (우선순위: 높음)

### 개선 계획

- **즉시 필요**: 3개 파일 생성 (index.html, data.json, update_data.py)
- **단계적 개선**: 테스트 케이스 추가, 접근성 개선
- **장기 계획**: PWA 지원, 다국어 지원 (향후)

## 결과물 요약

| 파일 | 설명 | 상태 |
|------|------|------|
| `index.html` | 메인 페이지 (HTML + CSS + JS) | 미생성 |
| `data.json` | 외부 데이터 (A값, 수익률 등) | 미생성 |
| `update_data.py` | 데이터 갱신 스크립트 | 미생성 |

---

_이 기술 스택은 `/alfred:2-build` 실행 시 TDD 도구 선택과 품질 게이트 적용의 기준이 됩니다._
