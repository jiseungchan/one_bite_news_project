---
title: "작은 모델도 충분하다 — 마이크로소프트의 MagenticLite가 AI 에이전트의 공식을 바꾼다"
category: AI
source: "Microsoft Research"
sourceUrl: "https://www.microsoft.com/en-us/research/blog/magenticlite-magenticbrain-fara1-5-an-agentic-experience-optimized-for-small-models/"
date: 2026-06-10
description: "마이크로소프트 리서치가 소형 모델 기반 AI 에이전트 시스템 MagenticLite를 공개했다. 14B 파라미터 모델이 웹 내비게이션 벤치마크에서 90% 이상을 달성하며, 더 큰 모델이 더 좋은 에이전트라는 공식에 도전한다."
image: "https://picsum.photos/seed/2026-06-10-magentic-lite-small-ai-agents/800/500"
---

## 한 줄 요약
> 소형 모델로도 복잡한 웹 작업을 자율 수행할 수 있음을 보여준다 — 핵심은 모델 크기가 아니라 시스템 설계다.

## 배경

AI 에이전트는 지금까지 대형 모델이 필수라는 인식이 강했다. 수백 억 파라미터 모델을 매번 호출하면 응답이 느려지고 비용이 올라가는 게 기업 도입의 걸림돌이었다.

## 핵심

MagenticLite는 두 개의 소형 모델 조합으로 작동한다.

- **MagenticBrain**: Qwen 3 기반 14B 오케스트레이션 모델
- **Fara1.5**: 실제 브라우저를 조작하는 컴퓨터 사용 모델 (4B~27B)

Fara1.5-27B는 OnlineMind2Web 벤치마크에서 90% 이상을 달성했다.

## 시장 영향

오픈소스로 GitHub에 공개됐다. 기업이 AI 에이전트를 온프레미스에 저비용으로 배치할 수 있는 길이 열렸다.

## 병규의 한 줄

모델 크기 경쟁이 아닌 시스템 설계 경쟁이 시작된 것일 수 있다.

**출처**: [Microsoft Research](https://www.microsoft.com/en-us/research/blog/magenticlite-magenticbrain-fara1-5-an-agentic-experience-optimized-for-small-models/)
