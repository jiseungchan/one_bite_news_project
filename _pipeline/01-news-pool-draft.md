# 뉴스 풀
수집일: 2026.07.14
소스: MIT Technology Review + AI타임스 + 인공지능신문 + 한국경제

---

## 수집 상태

| 소스 | HTTP 상태 | 비고 |
|------|----------|------|
| MIT Technology Review RSS (`/topic/artificial-intelligence/feed/`) | 403 | 프록시 차단 |
| MIT Technology Review 웹 (`/topic/artificial-intelligence/`) | 403 | 프록시 차단 |
| AI타임스 RSS (`/rss/allArticle.xml`) | 403 | 프록시 차단 |
| AI타임스 웹 (`/news/articleList.html`) | 403 | 프록시 차단 |
| 인공지능신문 RSS (`/rss/allArticle.xml`) | 403 | 프록시 차단 |
| 인공지능신문 웹 | 403 | 프록시 차단 |
| 한국경제 RSS (`/feed/economy`) | 403 | 프록시 차단 |
| 한국경제 웹 (`/economy/`) | 403 | 프록시 차단 |
| 연합인포맥스 RSS | 접근불가 | ENOTFOUND (DNS 차단) |
| Google News RSS | 403 | 프록시 차단 |
| TechCrunch / VentureBeat / Anthropic.com / OpenAI.com | 403 | 프록시 차단 |
| Hacker News API / arXiv RSS | 403 | 프록시 차단 |

**진단**: 에이전트 프록시가 외부 뉴스·미디어 도메인 전반을 차단 중.
GitHub raw 콘텐츠만 접근 가능한 상태 (확인됨). Wikipedia 등 일반 사이트도 403.

---

## 기사 목록

수집된 기사: **0건** (외부 웹 접근 불가)

---

## 다음 단계 제안

**해결 방법:**

1. 터미널에서 프록시 상태 확인:
   ```
   curl -sS "$HTTPS_PROXY/__agentproxy/status"
   cat /root/.ccr/README.md
   ```
   WebFetch 도구에 대한 외부 도메인 허용 설정 확인

2. 또는 아래 소스에서 기사 목록을 직접 복사해서 붙여넣어 주시면
   파이프라인 다음 단계를 즉시 진행합니다:
   - https://www.technologyreview.com/topic/artificial-intelligence/
   - https://www.aitimes.com/
   - https://www.aitimes.kr/
   - https://www.hankyung.com/economy/
