---
title: "Google, Gemini 3.5 Flash 공개 — 에이전트 코딩에서 경쟁 모델 절반 가격으로 앞선다"
category: AI
source: "Google Cloud Blog"
sourceUrl: "https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud"
date: 2026-06-29
description: "Google I/O 2026에서 공개된 Gemini 3.5 Flash가 Terminal-Bench 2.1에서 76.2%, MCP Atlas에서 83.6%를 기록하며 동급 모델 대비 절반 이하의 비용을 실현했다. 24/7 개인 AI 에이전트 Gemini Spark도 함께 발표됐다."
image: "https://picsum.photos/seed/2026-06-29-gemini-35-flash-google-io/800/500"
---

## 한 줄 요약
> Google이 에이전트·코딩에 특화된 Gemini 3.5 Flash를 내놨다 — 비슷한 성능의 경쟁 모델 대비 절반 이하 가격으로.

## 리드 — 왜 지금 이게 중요한가?

Google이 Google I/O 2026에서 Gemini 3.5 Flash를 공개했다. 에이전트(자율적으로 작업을 수행하는 AI 시스템)와 코딩에 특화된 이 모델은 Terminal-Bench 2.1(AI의 터미널 작업 처리 능력을 평가하는 벤치마크) 76.2%, MCP Atlas(다중 에이전트 프로토콜 협업 평가) 83.6%를 기록하며 이전 세대 Gemini 3.1 Pro를 전 영역에서 앞섰다. 비용은 동급 경쟁 모델 대비 절반 이하 — AI 인프라 비용 전쟁이 새 국면에 들어섰다.

## 배경 — 기존에는 어땠나?

AI 모델 시장은 지난 2년 사이 빠르게 분화됐다. '최강 성능'을 자랑하는 대형 모델들은 API 비용이 높아서 스타트업이나 대용량 에이전트 시스템에 도입하기 어려웠고, 저가 경량 모델은 에이전트 작업에서 자주 실수했다. 특히 에이전트가 여러 도구를 연속으로 호출하거나, 멀티모달(텍스트·이미지·코드 등 여러 형식) 입력을 다뤄야 할 때 성능 격차가 두드러졌다.

기존 Gemini 3.1 Pro는 성능은 훌륭했지만 "에이전트 전용 가성비 모델"이라 부르기엔 가격대가 높았다. 3.5 Flash는 그 공백을 정면으로 겨냥한다.

## 핵심 — 무엇이 다른가?

Gemini 3.5 Flash의 주요 성능 지표:

- **Terminal-Bench 2.1:** 76.2% — 터미널 명령어 실행과 코드 작성 능력 평가
- **GDPval-AA:** 1,656 Elo — 범용 에이전트 능력 종합 평가
- **MCP Atlas:** 83.6% — 여러 AI 에이전트가 협력하는 멀티에이전트 프로토콜 평가
- **CharXiv(멀티모달 차트 이해 벤치마크):** 84.2%

모두 Gemini 3.1 Pro를 상회하며, 비용은 "comparable models"(유사 수준 경쟁 모델) 대비 절반 이하라고 Google은 밝혔다.

함께 발표된 **Gemini Spark**도 주목된다. 24시간 상시 가동되는 개인 AI 에이전트로, Workspace(구글 오피스 도구 모음)와 외부 서비스를 넘나들며 사용자를 대신해 반복 작업을 처리한다. 각 작업은 독립된 격리 VM(가상 머신)에서 실행돼 데이터 유출을 막는다.

| 항목 | Gemini 3.1 Pro | Gemini 3.5 Flash |
|------|----------------|------------------|
| Terminal-Bench 2.1 | (이전 세대) | 76.2% |
| MCP Atlas | (이전 세대) | 83.6% |
| 비용 | 기준 | 절반 이하 |
| 에이전트 최적화 | 일반 | 특화 |

## 시장 영향 — 어디에 쓰이나?

- **즉시 사용 가능:** Google AI Studio, Gemini Enterprise Agent Platform, Antigravity(구글의 에이전트 개발 도구)에서 이미 접근 가능
- **보안 코드 리뷰 에이전트 CodeMender:** Gemini 모델을 사용해 코드 취약점을 자동으로 탐지·수정·테스트
- **영향 직군:** AI 에이전트 개발자, 클라우드 인프라 담당자, 코딩 자동화 팀
- Gemini 3.5 Pro는 다음 달 테스트 후 출시 예정

## 병규의 한 줄

이번에 흥미로운 건 성능이 아니라 가격 전략이다. Google이 "더 좋은 모델"이 아닌 "비슷하게 좋으면서 훨씬 싼 모델"로 에이전트 시장을 공략하기 시작했다는 것 — AI 모델 전쟁의 무기가 성능에서 비용으로 이동하고 있다.

## 출처 & 더 읽기
- 원문: https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud
