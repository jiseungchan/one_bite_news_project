---
title: "중국 Z.ai의 GLM-5.2 — 753B 오픈소스 모델이 GPT-5.5를 1/6 비용으로 이겼다"
date: 2026-06-27
category: AI
source: "VentureBeat"
sourceUrl: "https://venturebeat.com/technology/z-ais-open-weights-glm-5-2-beats-gpt-5-5-on-multiple-long-horizon-coding-benchmarks-for-1-6th-the-cost"
description: "중국 Z.ai가 6월 13일 공개한 GLM-5.2는 753B 파라미터 MoE 오픈소스 모델로, FrontierSWE 코딩 벤치마크에서 GPT-5.5를 1/6 비용에 능가했다. MIT 라이선스, 1M 컨텍스트."
image: "https://picsum.photos/seed/2026-06-27-glm52-zai-open-weights-beats-gpt55/800/500"
---

## 오픈소스가 또 한 번 경계를 밀어붙였다

6월 13일, 중국의 AI 기업 Z.ai(구 Zhipu AI, 청화대 스핀오프)가 GLM-5.2를 공개했다. 이 모델이 화제가 된 이유는 하나다: 코딩 벤치마크에서 OpenAI의 GPT-5.5를 이겼고, 비용은 1/6에 불과하다.

## GLM-5.2가 뭔가

**GLM(General Language Model)** 시리즈의 최신 플래그십이다. Z.ai는 Zhipu AI의 소비자 브랜드명이다.

핵심 스펙:

- **파라미터**: 753B (MoE 구조 — 총 파라미터는 753B지만, 토큰 처리 시 실제 활성화되는 파라미터는 약 40B)
- **컨텍스트**: 1M 토큰 (책 한 권 분량을 한 번에 처리 가능)
- **라이선스**: MIT (상업적 사용, 수정, 재배포 모두 자유)
- **특화**: 장기(long-horizon) 자율 코딩 및 소프트웨어 엔지니어링

MoE(Mixture of Experts, 전문가 혼합 구조)란 모든 파라미터를 매번 사용하는 대신, 입력에 따라 관련 전문가 모듈만 활성화하는 방식이다. 계산 효율이 크게 올라간다.

## 벤치마크 성적표

| 벤치마크 | 순위 | 비고 |
|---------|------|------|
| FrontierSWE (코딩) | GPT-5.5 능가 | 비용 1/6 수준 |
| Design Arena | 1위 | 전체 모델 중 |
| Code Arena Frontend | 2위 | |
| Artificial Analysis Intelligence Index v4.1 | 오픈소스 1위 | |

FrontierSWE(프런티어SWE)는 실제 소프트웨어 엔지니어링 작업 — 버그 수정, 기능 구현, 리팩토링 등 — 을 기준으로 AI 코딩 능력을 측정하는 벤치마크다.

## 어떻게 접근할 수 있나

- **오픈소스 가중치**: Hugging Face의 `zai-org/GLM-5.2` — 무료 다운로드, 로컬 실행 가능
- **API**: Z.ai 메터드 API — 종량제 과금
- **구독**: GLM Coding Plan (Lite / Pro / Max / Team) — 월 $12.60부터 시작

753B 모델을 로컬에서 돌리려면 상당한 GPU 자원이 필요하다. 실용적인 선택은 API나 Z.ai 구독 플랜이다.

## 이번에 흥미로운 건

이번 모델이 증명하는 건 '오픈소스가 따라잡는 속도'가 아니라, '오픈소스가 이미 앞서기 시작했다'는 것이다. 1/6 비용이라는 숫자는 단순 절약이 아니다 — GPT-5.5를 쓰던 기업 입장에서는 같은 예산으로 6배 더 많은 코딩 작업을 처리할 수 있다는 뜻이다. AI 개발 비용의 무게중심이 클로즈드 소스에서 오픈소스로 이동하는 흐름이 가속되고 있다.

---

**출처**: [VentureBeat](https://venturebeat.com/technology/z-ais-open-weights-glm-5-2-beats-gpt-5-5-on-multiple-long-horizon-coding-benchmarks-for-1-6th-the-cost) · [Simon Willison](https://simonwillison.net/2026/jun/17/glm-52/) (2026-06-13 발표, 6월 중순 오픈소스 공개)
