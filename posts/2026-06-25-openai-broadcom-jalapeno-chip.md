---
title: "OpenAI, 첫 자체 AI 칩 '할라피뇨' 공개 — NVIDIA 의존에서 벗어나는 첫 걸음"
category: AI
source: "OpenAI"
sourceUrl: "https://openai.com/index/openai-broadcom-jalapeno-inference-chip/"
date: 2026-06-25
description: "OpenAI가 Broadcom과 9개월 만에 공동 개발한 첫 자체 AI 추론 칩 'Jalapeño'를 공개했다. 현 세대 GPU 대비 전력 효율이 실질적으로 높으며 2026년 말 배포 예정이다."
image: "https://picsum.photos/seed/2026-06-25-openai-broadcom-jalapeno-chip/800/500"
---

## 한 줄 요약
> OpenAI가 처음으로 자체 설계한 AI 추론 전용 칩 'Jalapeño'를 공개하며, 수년간 이어온 NVIDIA 단일 의존 구조에서 벗어나는 첫 발을 내딛었다.

## 리드 — 왜 지금 이게 중요한가?

OpenAI와 Broadcom이 공동 개발한 첫 번째 자체 AI 칩 'Jalapeño(할라피뇨)'가 공개됐다. 착수 후 단 9개월 만에 테이프아웃(chip tape-out — 반도체 설계 완료 후 실제 실리콘 제작 단계로 넘어가는 것)에 성공했고, 초기 테스트에서 현 세대 최고 수준 GPU 대비 전력 효율이 실질적으로 높다는 결과가 나왔다. 2026년 말 데이터센터에 배포될 예정이다.

## 배경 — 기존에는 어땠나?

지금까지 OpenAI를 포함한 대부분의 AI 기업은 NVIDIA의 H100, B200 같은 GPU에 전적으로 의존해 왔다. 이는 학습(training — 대규모 데이터로 모델 파라미터를 조정하는 과정)과 추론(inference — 학습된 모델이 실시간으로 답을 생성하는 과정) 모두를 범용 GPU 하나로 처리하는 구조다.

문제는 비용이다. 추론은 학습과 달리 특정 모델 구조에 최적화된 연산만 반복하면 되기 때문에, 범용 GPU의 수많은 기능이 실제로는 낭비된다. 그래서 구글은 TPU를, 아마존은 Trainium을, 메타는 MTIA를 독자 개발해 추론 비용을 낮춰왔다. OpenAI만 이 대열에서 빠져 있었다.

## 핵심 — 무엇이 다른가?

Jalapeño는 ASIC(Application-Specific Integrated Circuit — 특정 목적 하나만을 위해 설계된 전용 반도체)으로 만들어진다. 범용 GPU와 달리 AI 추론 연산에만 최적화해 불필요한 회로를 걷어낸 구조다. 마치 도로를 달리는 SUV 대신 트랙 전용 레이싱카를 만든 것과 같다.

역할 분담도 명확하다. 칩 설계는 OpenAI가 직접 담당하고, 제조 파트너십은 Broadcom이 맡는다. Broadcom은 이미 Google의 TPU v4·v5 제조 파트너를 맡아온 검증된 곳이다.

| 항목 | 기존 방식 | Jalapeño |
|------|-----------|----------|
| 칩 종류 | 범용 GPU (NVIDIA) | 추론 전용 ASIC |
| 설계 주체 | NVIDIA | OpenAI |
| 제조 | TSMC (NVIDIA 위탁) | Broadcom 파트너십 |
| 전력 효율 | 기준점 | 현 세대 대비 실질적으로 우위 (초기 테스트) |

## 시장 영향 — 어디에 쓰이나?

- OpenAI 자체 데이터센터에 2026년 말 우선 배포 예정
- NVIDIA 의존도를 줄이는 첫 신호탄 — 중장기적으로 GPU 구매 예산 절감 가능
- Broadcom(AVGO) 입장에서는 Google에 이어 OpenAI라는 두 번째 대형 ASIC 고객 확보
- AI 추론 전용 칩 시장에서 Google·Amazon·Meta·OpenAI 모두 자체 칩을 보유하게 되며, NVIDIA의 추론 시장 점유율에 구조적 압력이 가해질 전망

## 병규의 한 줄

이번 발표에서 주목할 건 칩 성능 수치가 아니라 설계 철학의 변화다. OpenAI는 지금까지 "하드웨어는 사지, 만들지 않는다"는 암묵적 원칙을 따랐는데, 이번에 그 전제를 스스로 깼다. AI 소프트웨어 회사가 실리콘 레벨까지 수직 통합하는 흐름 — 이제 OpenAI도 그 대열에 올라탔다.

## 출처 & 더 읽기
- 원문: https://openai.com/index/openai-broadcom-jalapeno-inference-chip/
