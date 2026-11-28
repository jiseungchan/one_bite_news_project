---
title: "작은 모델도 충분하다 — 마이크로소프트의 MagenticLite가 AI 에이전트의 공식을 바꾼다"
category: AI
source: "Microsoft Research"
sourceUrl: "https://www.microsoft.com/en-us/research/blog/magenticlite-magenticbrain-fara1-5-an-agentic-experience-optimized-for-small-models/"
date: 2026-06-10
description: "마이크로소프트 리서치가 소형 모델 기반 AI 에이전트 시스템 MagenticLite를 공개했다. 14B 파라미터 모델이 웹 내비게이션 벤치마크에서 90% 이상을 달성하며, '더 큰 모델 = 더 똑똑한 에이전트'라는 공식에 도전한다."
image: "https://picsum.photos/seed/2026-06-10-magentic-lite-small-ai-agents/800/500"
---

## 한 줄 요약
> 마이크로소프트 리서치가 공개한 MagenticLite는 소형 모델로도 복잡한 웹 작업을 자율 수행할 수 있음을 보여준다 — 핵심은 모델 크기가 아니라 시스템 설계다.

## 리드 — 왜 지금 이게 중요한가?

AI 에이전트(사람이 지시하면 스스로 여러 단계를 밟아 작업을 완료하는 AI 시스템)는 지금까지 대형 모델이 필수라는 인식이 강했다. GPT-4급 이상이라야 복잡한 웹 탐색이나 파일 관리를 안정적으로 처리할 수 있다는 것이 업계의 통념이었다. 마이크로소프트 리서치 AI 프런티어스 팀이 2026년 5월 공개한 MagenticLite는 이 통념에 정면으로 도전한다. Fara1.5-27B는 OnlineMind2Web(웹 기반 작업 자동화 정확도를 측정하는 벤치마크)에서 90% 이상을 기록했고, 14B 파라미터짜리 오케스트레이션(여러 AI 도구를 지휘·조율하는 역할) 모델 MagenticBrain이 그 뒤를 받쳤다.

## 배경 — 기존에는 어땠나?

AI 에이전트 연구는 지난 2년간 빠르게 발전했지만, 실용적인 장벽이 하나 있었다. 복잡한 멀티스텝 작업을 신뢰성 있게 수행하려면 파라미터(모델의 학습 가중치 수 — 클수록 연산 비용이 높아진다)가 수백 억 이상인 대형 모델이 필요했다. 문제는 비용과 속도다. 수백 억짜리 모델을 매번 호출하면 응답 시간이 느려지고, 클라우드 비용이 급격히 올라간다. 기업에서 AI 에이전트를 실제 업무에 투입하기 어려운 이유 중 하나였다.

## 핵심 — 무엇이 다른가?

MagenticLite는 세 가지 구성 요소가 맞물려 작동한다.

**MagenticBrain** — Qwen 3 기반의 14B 파라미터 오케스트레이션 모델이다. 사용자의 지시를 받아 전체 작업 계획을 세우고, 하위 에이전트에게 세부 작업을 위임한다.

**Fara1.5** — 실제 브라우저를 조작하는 컴퓨터 사용 모델(Computer-Use Agent — 화면을 보고 클릭·입력을 수행하는 AI)이다. 4B, 9B, 27B 세 가지 크기로 제공되며, 전작 Fara-7B 대비 웹 내비게이션 성능을 거의 2배 향상했다.

| 항목 | 기존 방식 | MagenticLite 방식 |
|---|---|---|
| 핵심 가정 | 큰 모델 = 좋은 에이전트 | 오케스트레이션 설계가 성능 결정 |
| 오케스트레이터 크기 | 수백억 파라미터급 | 14B (MagenticBrain) |
| 컴퓨터 사용 모델 | 대형 범용 모델 | Fara1.5 특화 소형 모델 (4B~27B) |

## 시장 영향

MagenticLite는 GitHub에 오픈소스로 공개되고, MagenticBrain과 Fara1.5는 마이크로소프트 파운드리를 통해 제공된다. 소형 모델 조합으로 비슷한 성능을 낼 수 있다면, 기업이 에이전트를 온프레미스(자체 서버)에 직접 배치하거나 저비용으로 운용할 수 있는 길이 열린다.

## 병규의 한 줄

이번에 흥미로운 건 벤치마크 수치보다 팀이 택한 가설이다. "모델이 크면 에이전트가 똑똑해진다"는 업계의 기본 전제를 설계 단계에서 의심했고, 데이터·아키텍처·오케스트레이션·UX를 함께 엔드투엔드로 최적화한 결과가 수치로 나왔다. 모델 경쟁이 아닌 시스템 설계 경쟁이 시작된 것일 수 있다.

---

**출처**: [Microsoft Research](https://www.microsoft.com/en-us/research/blog/magenticlite-magenticbrain-fara1-5-an-agentic-experience-optimized-for-small-models/)
