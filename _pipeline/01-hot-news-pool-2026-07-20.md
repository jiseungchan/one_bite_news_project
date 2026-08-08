# 한입뉴스 뉴스 풀 — 2026-07-20

> **수집 실패 — 프록시 차단 (HTTP 403)**
>
> 수집 시도 일시: 2026-07-20
> 원인: 에이전트 실행 환경의 HTTPS 프록시가 모든 외부 도메인 요청을 차단 중
> 시도한 소스:
> - https://www.technologyreview.com/topic/artificial-intelligence/feed/
> - https://venturebeat.com/ai/
> - https://www.aitimes.com/rss/allArticle.xml
> - https://www.aitimes.com
> - https://www.aitimes.kr/rss/allArticle.xml
> - https://www.aitimes.kr
> - https://www.hankyung.com/it
> - https://news.google.com/rss/search (Google News RSS)
> - https://techcrunch.com/category/artificial-intelligence/
> - https://arxiv.org/list/cs.AI/recent
>
> 모든 도메인에서 HTTP 403 Forbidden 반환. 개별 사이트 차단이 아닌
> 프록시 레벨 전면 차단으로 판단됨.
>
> **조치 필요**: `/root/.ccr/README.md` 확인 및
> `curl -sS "$HTTPS_PROXY/__agentproxy/status"` 실행으로 프록시 상태 점검 요망.
> 프록시 정상화 후 수집 에이전트를 재실행해야 합니다.

---

## 수집 결과

| 소스 | 상태 |
|------|------|
| MIT Technology Review | 접근 불가 (403) |
| VentureBeat (대체) | 접근 불가 (403) |
| AI타임스 | 접근 불가 (403) |
| 인공지능신문 | 접근 불가 (403) |
| 한국경제 | 접근 불가 (403) |

수집 건수: 0건 / 목표 4건
