---
title: "수학 병목을 깨다 — 스타트업 Subquadratic, LLM의 10년 묵은 한계에 도전"
date: 2026-06-22
category: AI
source: "MIT Technology Review"
sourceUrl: "https://www.technologyreview.com/2026/06/19/1139313/a-startup-claims-it-broke-through-a-bottleneck-thats-holding-back-llms/"
description: "마이애미 스타트업 Subquadratic이 AI 언어 모델의 가장 오래된 병목을 수학적으로 해결했다고 주장한다. SubQ는 1,200만 토큰 컨텍스트를 처리하면서 비용은 기존 대비 300배 이상 절감."
image: "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=800"
---

LLM을 공부하다 보면 자연스럽게 만나는 질문이 있다. "왜 긴 문서를 한꺼번에 처리하면 비용이 폭발적으로 늘어나지?" 이번에 그 질문에 정면으로 부딪힌 회사가 등장했다.

## 기존에는 어땠나?

2017년 트랜스포머(Transformer, 현대 AI 언어 모델의 기반 구조)가 등장한 이후, LLM은 사실상 하나의 수학적 제약을 안고 있었다. 어텐션 메커니즘(Attention, 모델이 어떤 단어에 집중할지 계산하는 핵심 연산)의 연산량이 입력 길이의 제곱에 비례해 증가한다는 것이다. 텍스트를 두 배 늘리면 연산량은 네 배가 된다. 이 때문에 맥락을 길게 처리할수록 비용이 기하급수적으로 불어났고, "100만 토큰 컨텍스트"를 광고하는 모델들도 실제로 쓰면 청구서가 현실을 가로막는 구조였다.

## 무엇이 다른가?

마이애미 기반 스타트업 Subquadratic이 2026년 5월 스텔스(비공개 개발 단계)에서 등장하며 내놓은 SubQ 모델의 핵심은 SSA(서브쿼드래틱 스파스 어텐션, Subquadratic Sparse Attention — 연산량을 입력 길이의 제곱이 아니라 선형에 가깝게 줄이는 희소 주의 메커니즘)다.

작동 원리는 이렇다. 어떤 문서를 처리할 때, 실제로 의미 있는 토큰(단어 조각) 간 관계는 전체의 극히 일부에 불과하다. SSA는 그 중요한 연산만 선별해 수행하고 나머지는 건너뛰는 방식이다. 결과적으로 연산량이 길이에 거의 선형으로 비례하도록 줄었다.

숫자로 보면 임팩트가 뚜렷하다:

| 항목 | 기존 프런티어 모델 | SubQ |
|------|-----------------|------|
| RULER 128K 점수 | 유사 수준 | 97% |
| 동일 작업 비용 | 약 $2,600 | $8 |
| 최대 컨텍스트 윈도우 | 100만~200만 토큰 | 1,200만 토큰 |

12 million 토큰은 책 수백 권을 한꺼번에 처리할 수 있는 분량이다. MIT Technology Review는 독립 테스트 기관 Appen의 검증 결과를 인용해 이 주장이 단순 마케팅이 아님을 확인했다.

물론 의문도 남는다. Subquadratic은 중국 오픈소스 모델 Qwen의 가중치를 사용해 SubQ를 부트스트랩(초기 구동)했으며, 처음부터 독자 학습한 모델이 아니라는 점이 논쟁의 여지로 남아 있다. 접근 경로도 아직 제한적이다.

## 이번에 흥미로운 건 수치보다 철학이다

지난 10년간 AI 업계는 더 많은 GPU를 쌓고, 더 큰 데이터셋으로 훈련하는 방식으로 성능을 올려왔다. Subquadratic은 그 방향 대신 "애초에 계산 자체를 바꾸자"는 길을 택했다. 만약 이 방향이 맞다면, AI 장문 추론의 비용 구조가 근본적으로 달라질 수 있다. 300배라는 숫자는 단순한 효율이 아니라 누가 AI를 쓸 수 있는지를 다시 정의할 수도 있다.

---

원문: [MIT Technology Review — A startup claims it broke through a bottleneck that's holding back LLMs](https://www.technologyreview.com/2026/06/19/1139313/a-startup-claims-it-broke-through-a-bottleneck-thats-holding-back-llms/)
