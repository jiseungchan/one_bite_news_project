---
title: "OpenAI 차세대 모델 'Astra', 260만 원짜리 컴퓨팅으로 수학계 난제 10개 풀었다"
date: 2026-08-05
category: AI
source: "The Decoder"
sourceUrl: "https://the-decoder.com/openai-announces-its-next-major-model-astra-by-dropping-ten-previously-unsolved-math-solutions/"
description: "OpenAI가 아직 공개하지 않은 차세대 모델 Astra로 10년 이상 풀리지 않던 수학·이론 컴퓨터과학 난제 10개를 해결했다. 총 연산 비용은 약 2,000달러(약 260만 원). 모든 증명은 Lean 4로 기계 검증됐다."
image: "https://images.unsplash.com/photo-1509228627152-72ae9ae6848d?w=800&q=80"
---

## 배경: AI와 수학의 관계는 어디까지 왔나

수학은 오랫동안 AI가 넘기 어려운 벽으로 여겨졌다. 계산은 잘하지만, '증명'은 다른 문제다. 수학적 증명은 논리의 빈틈 없는 연결이어야 한다. 한 단계라도 틀리면 전체 증명이 무너진다.

2022년 딥마인드가 수학 올림피아드 문제를 풀기 시작했고, 2024년 OpenAI의 o3가 국제 수학 올림피아드(IMO)에서 금메달 수준의 점수를 기록했다. 그러나 이것들은 이미 '답이 있는 문제'였다. AI 커뮤니티의 다음 질문은 이것이었다: "아직 아무도 풀지 못한 문제도 풀 수 있을까?"

8월 1일, OpenAI가 그 답을 내놨다.

## 핵심: Astra가 해결한 것

OpenAI는 아직 공개하지 않은 차세대 모델 'Astra'가 수학과 이론 컴퓨터과학 분야의 미해결 난제 10개를 해결했다고 발표했다. 각 문제는 최소 10년 이상, 일부는 수십 년간 풀리지 않았던 것들이다.

총 연산 비용은 **약 2,000달러(약 260만 원)**. GPT-5.6 Sol API 기준 가격이다.

가장 주목받는 결과는 '비소픽 군(non-sofic group)'의 존재 증명이다. 수학자 미하일 그로모프(Mikhail Gromov)가 1999년 '소픽성(soficity)'이라는 개념을 도입하면서 제기한 질문이다 — "소픽하지 않은 군이 존재하는가?" 27년간 아무도 답을 내지 못했던 이 질문에 Astra가 처음으로 명시적인 구성(explicit construction)을 만들어냈다.

이 밖에 해결된 주요 문제들:

- **콘네스 강성 추측(Connes's rigidity conjecture) 반증**: 폰 노이만 대수(von Neumann algebra) 분야의 난제. 같은 폰 노이만 대수를 공유하지만 서로 동형이 아닌 무한히 많은 군이 존재함을 증명
- **고차원 구 패킹 밀도(sphere-packing density) 새 상한 도출**: 공간을 구로 채울 때 최대 밀도에 관한 수학적 한계를 새로 계산
- **에르되시 문제집(Erdős catalog) 3개 해결**: 폴 에르되시가 남긴 공개 문제 목록 중 다색 라이미 수(multicolor Ramsey numbers)에 관한 183번 문제 포함
- **에르하르트 부피 추측(Ehrhart's volume conjecture) 증명**

## 검증 방식이 다르다

이번 발표에서 가장 주목해야 할 부분은 '어떻게 검증했는가'이다.

OpenAI는 249페이지 분량의 논문과 함께 **Lean 4 증명 인증서(proof certificates)**를 GitHub에 공개했다(Apache 2.0 라이선스). Lean 4는 수학 증명을 기계가 자동으로 검증하는 증명 보조 시스템(proof assistant)이다. 중요한 건 저장소의 "sorry" 개수가 **0**이라는 것이다 — Lean에서 "sorry"는 '이 부분은 나중에 채울 구멍'을 의미한다. 즉, 10개 난제의 모든 논리적 단계가 빈틈 없이 기계 검증을 통과했다.

이것이 왜 중요하냐면, 수학자들이 'AI가 증명을 제안했지만 인간이 검토해야 한다'는 기존 구도를 이번에 완전히 뒤집었기 때문이다. 기계 검증된 Lean 증명은 인간의 재검토 없이도 참임을 보장한다.

기존 방식 | 이번 방식
--- | ---
AI가 증명 아이디어 제안 | AI가 완전한 Lean 4 증명 생성
인간 수학자가 검토·검증 | 기계가 자동 검증 (sorry=0)
검증 몇 달~몇 년 소요 | 즉시 기계 검증 완료
기존에 알려진 문제 공략 | 수십 년 미해결 문제 해결

## 중요한 맥락

OpenAI 수석 과학자 노암 브라운(Noam Brown)은 흥미로운 단서를 달았다: "안타깝게도 밀레니엄 난제는 아직이다 (yet)." 밀레니엄 난제(Millennium Prize Problems)는 P=NP, 리만 가설 등 7개 문제로 각각 100만 달러 상금이 걸려 있다. "아직(yet)"이라는 단어가 시사하는 바는 작지 않다.

Astra는 아직 일반에 공개되지 않았으며 공개 일정도 미정이다.

## 병규의 한 줄

이번에 흥미로운 건 수학 결과 자체보다 증명 방식의 변화다. 수학적 증명의 타당성을 판단하는 마지막 심판이 인간에서 기계로 넘어가는 순간, '수학이란 무엇인가'라는 질문이 다시 열린다. Lean 증명이 참이면 그게 수학적 진리다 — AI가 이 새 규칙을 가장 빠르게 활용하고 있다.

---

*원문: [OpenAI announces its "next major model" Astra by dropping ten previously unsolved math solutions — The Decoder](https://the-decoder.com/openai-announces-its-next-major-model-astra-by-dropping-ten-previously-unsolved-math-solutions/)*  
*참조: [Ten advances in mathematics and theoretical computer science — OpenAI](https://openai.com/index/ten-advances-in-mathematics/)*
