# 뉴스 수집 풀 — 2026-07-26

수집일: 2026-07-26
수집 기간: 2026-07-20 이후 기사

---

## 프록시 상태

- 프록시: 활성 (`http://127.0.0.1:38547`, `selective: false`)
- 최근 릴레이 실패: 없음
- 차단 원인: 에그레스 정책에 의한 외부 도메인 전면 차단 (`CONNECT tunnel failed, response 403`)
  - 재시도 또는 우회 불가 (README 지침: "Do not retry or route around it — report the blocked host")

---

## MIT Technology Review

수집 실패 (프록시 에그레스 정책 차단 — `www.technologyreview.com` 403 Forbidden)

시도한 URL:
- `https://www.technologyreview.com/topic/artificial-intelligence/feed/` → 403
- `https://www.technologyreview.com/feed/` → 403

---

## AI타임스

수집 실패 (프록시 에그레스 정책 차단 — `www.aitimes.com` 403 Forbidden)

시도한 URL:
- `https://www.aitimes.com/rss/allArticle.xml` → 403
- `https://www.aitimes.com` → 403

---

## 인공지능신문

수집 실패 (프록시 에그레스 정책 차단 — `www.aitimes.kr` 403 Forbidden)

시도한 URL:
- `https://www.aitimes.kr/rss/allArticle.xml` → 403
- `https://www.aitimes.kr` → 403

---

## 한국경제

수집 실패 (프록시 에그레스 정책 차단 — `www.hankyung.com` 403 Forbidden)

시도한 URL:
- `https://www.hankyung.com/feed/economy` → 403
- `https://www.hankyung.com/economy` → 403
- `https://www.hankyung.com` → 403

---

## 조치 필요 사항

4개 소스 전체 수집 실패. 아래 중 하나를 병규가 선택해야 파이프라인을 재개할 수 있습니다:

1. **세션 외부에서 직접 수집**: 브라우저에서 각 사이트 접속 후 URL 목록을 직접 붙여넣기
2. **허용 도메인 요청**: Anthropic 관리자에게 해당 도메인 에그레스 허용 요청
3. **대체 소스 활용**: 에그레스 정책에서 허용된 다른 RSS/뉴스 소스가 있다면 병규가 URL 제공
