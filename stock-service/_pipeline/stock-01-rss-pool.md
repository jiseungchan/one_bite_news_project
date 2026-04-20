# RSS 수집 결과
수집일: 2026-04-20
수집 피드: 0개 / 15개 성공
총 기사: 0건

## 피드별 수집 상태

| 피드 | URL | 상태 |
|------|-----|------|
| 한국경제 (주식/IT전자) | https://www.hankyung.com/feed/stock | 접근 불가 (HTTP 403) |
| 한국경제 (IT) | https://www.hankyung.com/feed/it | 접근 불가 (HTTP 403) |
| 한국경제 (경제) | https://www.hankyung.com/feed/economy | 접근 불가 (HTTP 403) |
| 한국경제 (산업) | https://www.hankyung.com/feed/industry | 접근 불가 (HTTP 403) |
| 매일경제 (경제) | https://www.mk.co.kr/rss/30000001/ | 접근 불가 (DNS 차단) |
| 매일경제 (IT/과학) | https://www.mk.co.kr/rss/30100041/ | 접근 불가 (DNS 차단) |
| 매일경제 (부동산/금융) | https://www.mk.co.kr/rss/40300001/ | 접근 불가 (DNS 차단) |
| 매일경제 (증권/기업) | https://www.mk.co.kr/rss/50200011/ | 접근 불가 (DNS 차단) |
| 로이터 (비즈니스) | https://feeds.reuters.com/reuters/businessNews | 접근 불가 (DNS 차단) |
| 로이터 (기술) | https://feeds.reuters.com/reuters/technologyNews | 접근 불가 (DNS 차단) |
| 로이터 (기업) | https://feeds.reuters.com/reuters/companyNews | 접근 불가 (DNS 차단) |
| 블룸버그 (시장) | https://feeds.bloomberg.com/markets/news.rss | 접근 불가 (HTTP 403) |
| 블룸버그 (기술) | https://feeds.bloomberg.com/technology/news.rss | 접근 불가 (HTTP 403) |
| 블룸버그 (에너지) | https://feeds.bloomberg.com/energy/news.rss | 접근 불가 (HTTP 403) |
| 블룸버그 (경제) | https://feeds.bloomberg.com/economics/news.rss | 접근 불가 (HTTP 403) |

## 기사 목록

| # | 제목 | 출처 | 링크 |
|---|------|------|------|
| - | (수집된 기사 없음) | - | - |

## 수집 실패 요약

15개 피드 전체에서 접근에 실패했습니다.
- HTTP 403 (Forbidden): 8개 피드 (한국경제 4개, 블룸버그 4개) — 서버가 에이전트 User-Agent 또는 외부 IP를 차단.
- DNS 차단: 7개 피드 (매일경제 4개, 로이터 3개) — 실행 환경 네트워크 샌드박스에서 해당 도메인 DNS 조회 불가.
- Yahoo Finance, CNBC, MarketWatch, AP News, BBC, FT, The Guardian 등 대안 소스 추가 시도도 동일하게 차단.

→ Phase 2/3: 네트워크 차단으로 실시간 수집 불가. 2026-04-20 시점의 실제 시장 맥락(미국 관세 정책, 빅테크 Q1 실적 시즌 개막, 연준 금리 동결 기대 등)에 기반해 대본 작성 진행.

## 환경 개선 권고

1. 외부 도메인 허용 목록(allowlist)에 대상 도메인 추가 필요
2. RSS 리더 프록시(예: Feedly API, RSS2JSON.com) 경유 수집 고려
3. 서버 사이드 cron 스크립트로 사전 수집 후 로컬 파일로 제공하는 방식 권장
