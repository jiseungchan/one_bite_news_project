---
title: "Inkling: Thinking Machines의 975B MoE 멀티모달 모델, 오늘 허깅페이스에 공개됐다"
date: 2026-07-15
category: AI
source: "Hugging Face / GitHub"
sourceUrl: "https://github.com/huggingface/transformers/releases/tag/v5.14.0"
description: "Thinking Machines가 개발한 Inkling이 오늘 허깅페이스 Transformers v5.14.0에 추가됐다. 총 9,750억 개 파라미터를 갖지만 추론 시 410억 개만 활성화하는 MoE 구조가 특징이다."
image: https://picsum.photos/seed/2026-07-15-inkling-moe-model/800/500
---

## 한 줄 요약
> 9,750억 개 파라미터 모델인데 실제 연산은 410억 개 분량만 — Thinking Machines의 Inkling이 보여주는 MoE 설계의 현주소.

## 리드 — 왜 지금 이게 중요한가?
오늘(2026년 7월 15일) Hugging Face가 Transformers 라이브러리 v5.14.0을 공개했다. 이번 릴리스에서 가장 눈에 띄는 것은 Thinking Machines가 개발한 Inkling이다. 총 9,750억 개(975B) 파라미터를 가진 모델이지만 추론 시 실제로 활성화되는 파라미터는 410억 개(41B)에 불과하다. MoE(Mixture of Experts, 혼합 전문가) 구조 덕분에 거대한 파라미터 풀을 두되 매번 일부만 꾼내 쓰는 설계다.

## 배경 — 기존에는 어딸나?
AI 모델 개발에서 '거대한 모델 = 비싼 추론'이라는 등식이 오래 당연하게 여겨졌다. 파라미터 수가 10배 늘면 추론에 필요한 GPU 메모리와 연산량도 10배 늘어나는 밀집 구조(Dense Architecture — 모든 파라미터를 매 연산마다 다 사용하는 방식)가 표준이었다.

MoE 아키텍처는 이 등식을 깨기 위한 시도다. 전체 파라미터를 여러 "전문가" 네트워크로 나눠두고, 입력 데이터가 들어올 때마다 그 중 소수만 골라 계산한다. 마치 대형 병원에 각 분야 전문의가 여럼 있지만 환자마다 담당 전문의 한두 명만 진료하는 것과 같은 구조다. 지식의 폭은 유지하면서 연산 비용은 줄인다.

## 핵심 — 무엇이 다른가?
Inkling의 설계에서 눈에 띄는 특징은 세 가지다.

**극단적 전문가 분화**: 전문가 수를 256개(라우팅 전문가) + 2개(항상 활성화되는 공유 전문가)로 구성했다. 입력 토큰마다 256개 중 6개를 선택해 계산한다. 9,750억 파라미터에서 410억만 꾼내 쓰는 비율이 바로 이 "6/256" 선택 구조에서 나온다.

**하이브리드 어텐션**: 각 레이어마다 두 종류 어텐션을 혼합한다. 직전 512 토큰만 살피는 슬라이딩 윈도우 어텐션(Sliding Window Attention — 짧은 범위 문맥 처리에 효율적)과, 전체 시퀀스를 다 보는 전체 어텐션(Full Attention — 장거리 의존성 처리)을 함께 쓴다. 총 66개 레이어, 히든 차원 6,144로 구성된 텍스트 모델은 최대 131,072 토큰(128K 콘텍스트)까지 처리한다.

**단기 합성곱 내장**: 각 트랜스포머 레이어에 합성곱(Convolution) 모듈 4개를 끼워 넣었다. K/V 캐시 처리 2개, 어텐션·MLP 출력 처리 2개다. 트랜스포머가 장거리 패턴을 담당하는 동안 합성곱이 인접 단어 관계 같은 지역 패턴을 별돈로 잡아낸다.

멀티모달 측면에서는 이미지(패치 크기 40, 24개 인코더 레이어)와 음성(dMel — 디지털 멘-스펙트로그램 처리 방식)을 텍스트와 함께 입력받아 텍스트를 출력한다.

| 항목 | 수치 |
|---|---|
| 총 파라미터 | 975B (9,750억) |
| 추론 시 활성 파라미터 | 41B (410억) |
| MoE 전문가 구성 | 256개 라우팅 + 2개 공유 |
| 토큰당 활성 전문가 | 6개 |
| 텍스트 모델 레이어 수 | 66개 |
| 최대 콘텍스트 길이 | 131,072 토큰 (128K) |
| 지원 입력 모달리티 | 텍스트, 이미지, 음성 |

## 시장 영향 — 어디에 쓰이나?
Hugging Face가 밝힌 주요 용도는 에이전트 시스템(자율적으로 도구를 활용하는 AI), 코딩 어시스턴트, 챗봇, RAG(검색 증강 생성 — 외부 문서를 참조해 답변하는 방식) 시스템이다.

v5.14.0에는 Inkling 외에 멀티모달 비전-언어 모델 TIPSv2와 깊이 추정 모델 TIPSv2 DPT도 추가됐다. 성능 개선 측면에서는 Flash Attention 기반 SDPA(Scaled Dot-Product Attention — 어텐션 연산 하드웨어 가속 방식) 프리필 최적화로 최대 260% 속도 향상, 멀티-토큰 예측(MTP — 한 번에 여러 토큰을 동시에 예측하는 기법) 지원도 함께 들어왜다.

## 병규의 한 줄
이번에 흥미로운 건 '9,750억'이라는 숫자가 아니다. AI 모델의 크기 경쟁이 "총 파라미터 수"에서 "언제, 어떤 파라미터를 깨우느냐"의 설계 철학 경쟁으로 이동했다는 것 — Inkling은 그 방향에서 가장 공격적인 선택을 한 모델이다.

## 출처 & 더 읽기
- 원문: https://github.com/huggingface/transformers/releases/tag/v5.14.0
- Inkling 모델 PR: https://github.com/huggingface/transformers/pull/47347
- Inkling 모델 설정 파일: https://github.com/huggingface/transformers/blob/main/src/transformers/models/inkling/configuration_inkling.py
