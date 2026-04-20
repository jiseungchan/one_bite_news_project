# 주식 영향 뉴스 브리핑 서비스 — 운영 가이드

## 서비스 한 줄 정의

13개 RSS 피드에서 오늘 발행된 기사를 수집하고, 주식 시장 영향도 7점 이상 기사만 선별해 방송/영상용 대본을 자동 작성하는 **일일 주식 뉴스 브리핑 파이프라인**.

---

## 에이전트 라우팅

| 요청 유형 | 사용 에이전트 | 트리거 키워드 |
|----------|-------------|-------------|
| 전체 브리핑 파이프라인 | `stock-orchestrator` | "오늘 주식 뉴스", "주식 브리핑", "뉴스 대본 만들어줘" |
| RSS 수집만 | `rss-collector` | "RSS 수집", "오늘 기사 목록 가져와줘" |
| 영향도 평가만 | `stock-impact-scorer` | "영향도 평가", "점수 매겨줘" |
| 대본 작성만 | `news-script-writer` | "대본 써줘", "스크립트 작성" |

---

## 파이프라인 흐름

```
[Phase 1] rss-collector
          13개 RSS 피드에서 오늘 기사 수집
          → _pipeline/stock-01-rss-pool.md
                    ↓
[Phase 2] stock-impact-scorer
          제목 1차 필터 → 본문 fetch → 영향도 7점+ 선별
          → _pipeline/stock-02-scored.md
                    ↓
[Phase 3] news-script-writer
          7점+ 기사 대본 작성
          → _stock-news/YYYY-MM-DD-stock-brief.md
                    ↓
          병규 확인
```

**토큰 예상**: RSS 15개 피드 수집 + 후보 기사 본문 fetch (최대 10건) → 약 80,000~120,000 토큰

---

## 폴더 구조

```
stock-service/
├── CLAUDE.md                    ← 이 파일. 운영 가이드
├── .claude/
│   └── agents/
│       ├── stock-orchestrator.md   ← 파이프라인 조율
│       ├── stock-impact-scorer.md  ← 영향도 평가 (1~10점)
│       ├── rss-collector.md        ← RSS 수집 (15개 피드)
│       └── news-script-writer.md  ← 대본 작성
├── _pipeline/                   ← 에이전트 간 중간 파일
│   ├── stock-01-rss-pool.md     ← RSS 수집 결과
│   └── stock-02-scored.md       ← 영향도 평가 결과
└── _stock-news/                 ← 최종 브리핑 대본
    └── YYYY-MM-DD-stock-brief.md
```

---

## 수집 대상 RSS 피드 (15개)

### 한국경제 (4)
- 주식(IT/전자), IT, 경제, 산업

### 매일경제 (4)
- 경제, IT/과학, 부동산/금융, 증권/기업

### 로이터 (3)
- Business, Technology, Company

### 블룸버그 (4)
- Markets, Technology, Energy, Economics

---

## 주식 영향도 점수 기준

| 점수 | 기준 |
|------|------|
| 9~10 | 금리 결정, 대형 M&A, 경기침체 선언, 반도체 수출 규제 |
| 7~8 | 빅테크 실적, AI 핵심 기술 발표, 대기업 대형 투자, 주요 경제지표 |
| 5~6 | 스타트업 투자, 정책 예고, 신제품 출시 |
| 3~4 | 인사 변동, 해외 소규모 사건, 학술 연구 |
| 1~2 | 홍보성 보도, 주식과 무관한 소식 |

**7점 이상만 대본 작성 대상으로 선별**

---

## 면책 고지

이 서비스의 모든 브리핑은 정보 제공 목적이며 투자 권유가 아닙니다.  
투자 결정 시 반드시 공식 출처의 원문을 확인하세요.
