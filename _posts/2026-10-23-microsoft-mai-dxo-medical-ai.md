---
title: "AI가 의사를 2.3배 이겼다 — 마이크로소프트 MAI-DxO, Science에 게재된 날"
date: 2026-10-23
category: AI
source: "Technology.org"
sourceUrl: "https://www.technology.org/2026/10/23/microsoft-mai-dxo-science-study-83-percent-diagnosis-doctors/"
description: "마이크로소프트의 멀티에이전트 진단 AI 'MAI-DxO'가 Science에 게재됐다. NEJM 복잡 증례 304건에서 83.2% 정확도를 기록했다 — 교과서와 인터넷을 쓸 수 있는 일반의의 36.1%와 비교되는 숫자다."
---

2026년 10월 22일, 마이크로소프트 연구팀이 Science 저널에 논문 하나를 실었다. 제목은 "Sequential diagnosis with language models". 여기 담긴 숫자가 조용히 의료계를 뒤흔들고 있다.

## 배경 — 기존 AI 진단의 한계

그동안 의료용 AI는 주로 이미지 분석에 강했다. X선이나 CT 스캔에서 병변을 찾아내는 식이었다. 하지만 내과 진단처럼 "이 환자의 증상들을 조합해 무슨 병인지 맞히는" 복잡한 추론 과제에서는 AI가 아직 의사를 못 따라간다는 게 업계의 통설이었다.

특히 **NEJM(New England Journal of Medicine — 세계에서 가장 권위 있는 의학 저널 중 하나)**이 출판하는 증례 기록은, 의과대학 교수들도 까다롭게 여기는 난이도다. 하나의 환자 증례를 다루면서 희귀한 패턴 인식과 감별 진단(differential diagnosis — 비슷한 증상을 가진 여러 질환 중 실제 병을 골라내는 과정)이 동시에 필요하기 때문이다.

이 영역에서 AI의 성적은 지금까지 인상적이지 않았다.

## 핵심 — MAI-DxO는 어떻게 다른가

마이크로소프트가 만든 **MAI-DxO(Multi-Agent Intelligent Diagnostic Orchestration — 멀티에이전트 지능형 진단 조율 시스템)**는 단일 AI 모델이 아니다. 여러 가상 의사 에이전트가 역할을 나눠 토론하듯 협력하는 구조다.

동작 방식은 이렇다:
1. 여러 에이전트가 증상 데이터를 받아 각자 가설 진단을 제안한다
2. 에이전트들이 서로의 진단에 반박하고, 추가 검사 필요 여부를 논의한다
3. 조율 레이어가 토론 결과를 통합해 최종 진단을 내린다

핵심 모델은 GPT-5다. 이 멀티에이전트 구조 위에서 구동된다.

**결과**: NEJM 복잡 증례 304건에서 **83.2% 정확도**. 교과서와 인터넷을 사용할 수 있는 일반의는 **36.1%**, 아무 도구 없이는 22%였다. 일반의 대비 약 2.3배 차이다.

응급실 입원 환자 325건에서도 **80.3%** — 의사는 **46.8%**였다.

## 시장 영향 — 하지만 진짜 시험은 아직

논문 저자에는 마이크로소프트 CEO 무스타파 술레이만(Mustafa Suleyman)과 AI 리서치 부사장 에릭 호비츠(Eric Horvitz)가 포함돼 있다. 회사가 이 연구를 얼마나 진지하게 밀고 있는지를 보여준다.

다음 단계는 **Beth Israel Deaconess Medical Center(보스턴 소재 하버드 의대 부속 병원)**에서의 실제 환자 대상 임상 연구다. 다만 현재 연구에는 몇 가지 명확한 한계가 있다.

- 이번 연구는 텍스트 기반 역사적 증례만 사용 — 실제 환자와의 대화, 신체 검진, 영상 판독은 포함되지 않음
- 비교 대상이 일반의(specialist가 아닌 generalist)였다는 점도 한계
- 저자 전원이 마이크로소프트 직원 — 독립적 재현 실험은 아직 없음

## 병규의 한 줄

이번에 흥미로운 건 숫자보다 구조다. MAI-DxO가 "혼자 똑똑한 AI"가 아니라 "서로 토론하는 AI들의 집합"이라는 설계 철학을 택했다는 점 — 의학적 판단의 불확실성을 AI 하나가 감당하게 두지 않겠다는 접근이다. 임상 검증까지 갈 길이 멀지만, 방향 자체는 옳아 보인다.

---

**출처**: [Technology.org](https://www.technology.org/2026/10/23/microsoft-mai-dxo-science-study-83-percent-diagnosis-doctors/) | [unite.ai](https://www.unite.ai/microsoft-diagnostic-ai-outperforms-generalist-physicians-in-science-study/) | Science Volume 394, 2026년 10월 22일
