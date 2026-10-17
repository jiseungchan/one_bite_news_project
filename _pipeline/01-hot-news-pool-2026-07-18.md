# 한입뉴스 기사 후보 풀 — 2026-07-18

수집일: 2026-07-18
상태: **수집 실패 — 프록시 차단**

---

## 수집 실패 원인

이 에이전트가 시도한 모든 외부 URL(example.com 포함)이 HTTP 403 Forbidden을 반환했습니다.
발신 HTTPS 트래픽이 에이전트 프록시 레벨에서 전면 차단된 것으로 판단됩니다.

시도한 소스:
- https://www.technologyreview.com/topic/artificial-intelligence/feed/ → 403
- https://venturebeat.com/category/ai/ → 403
- https://the-decoder.com/ → 403
- https://www.aitimes.com (메인 + RSS) → 403
- https://www.aitimes.kr (메인 + RSS) → 403
- https://www.hankyung.com/it → 403
- https://techcrunch.com/category/artificial-intelligence/ → 403
- https://arxiv.org/list/cs.AI/recent → 403
- https://news.ycombinator.com/ → 403
- https://example.com → 403 (프록시 전면 차단 확인)

---

## 조치 필요

환경 설정 문서(`/root/.ccr/README.md`)를 참고하거나 아래 명령으로 프록시 상태를 확인하세요:

```
curl -sS "$HTTPS_PROXY/__agentproxy/status"
```

프록시가 정상화된 후 이 에이전트를 재실행하면 수집이 진행됩니다.

---

## MIT Tech Review / 대체 소스

| 제목 | URL | 발행일 | 점수 |
|------|-----|--------|------|
| (수집 실패) | — | — | — |

## AI타임스 / 인공지능신문

| 제목 | URL | 발행일 | 점수 |
|------|-----|--------|------|
| (수집 실패) | — | — | — |

## 한국경제 / 경제·주식

| 제목 | URL | 발행일 | 점수 |
|------|-----|--------|------|
| (수집 실패) | — | — | — |

## 최종 선택 4건

수집 실패로 선택 불가. 프록시 정상화 후 재실행 필요.
