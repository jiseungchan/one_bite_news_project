# 리서치: Can AI learn to trust itself? The emerging science of model self-evaluation
수집일: 2026.05.13
원문 URL: https://www.technologyreview.com/2026/05/13/1116201/ai-model-self-evaluation-trustworthy/
출처 매체: MIT Technology Review

---

## 원문 핵심 단락

**단락 1 (리드)**
AI models are increasingly being trained to evaluate the quality of their own answers—a capability that researchers say could reduce hallucinations and improve factual accuracy without the cost of constant human oversight.

**단락 2 (연구 데이터)**
A March 2026 paper from Google DeepMind found that models trained with self-evaluation feedback improved calibration—meaning that when they say they are 90% confident, they are correct 90% of the time—by 27%. On factual accuracy benchmarks like SimpleQA, self-evaluating models scored 61.3% compared to 48.1% for standard models.

**단락 3 (기업 적용)**
OpenAI has incorporated forms of self-assessment into o4-mini's reasoning process. Google's Gemini 2.5 Pro now includes a confidence score layer that allows users to see the model's internal certainty level for different claims.

**단락 4 (기술 방식)**
At Stanford's AI Safety Center, researchers developed a technique called cascade evaluation: a smaller 'critic model' scores the output of a larger primary model in real time. In medical question-answering tasks, this approach reduced hallucinations by 34% without requiring additional human labeling.

**단락 5 (한계·반론)**
Yoshua Bengio's Mila team published a counterargument in April 2026: they call this the 'mirror problem.' A model that is systematically wrong in a domain is also likely to be systematically wrong in evaluating its own wrongness. You cannot ask a biased system to find its own bias.

**단락 6 (Anthropic 맥락)**
Anthropic's Constitutional AI (CAI) was an early form of this concept, training models to critique and revise their own outputs based on a list of principles ('constitution') set by the researchers.

---

## 핵심 수치 정리

| 수치 | 의미 | 출처 |
|------|------|------|
| 27% | 캘리브레이션 향상률 | Google DeepMind 2026.03 |
| 61.3% vs 48.1% | 자기평가 모델 vs 기존 모델 SimpleQA 점수 | Google DeepMind |
| 13.2%p | 정확도 격차 | 계산값 |
| 34% | 환각률 감소 (의료 QA) | Stanford AI Safety Center |

---

## 등장 기업·기관

- Google DeepMind
- OpenAI (o4-mini)
- Google (Gemini 2.5 Pro)
- Meta (Llama 4 자기평가 기능 개발 중)
- Anthropic (Constitutional AI)
- Stanford AI Safety Center (cascade evaluation)
- Mila — Yoshua Bengio 팀 (mirror problem 반론)

---

## 용어 정리

| 용어 | 설명 |
|------|------|
| Calibration | AI가 확신 수준을 실제 정확도와 일치시키는 능력 |
| SimpleQA | 사실 정확도 측정 벤치마크 |
| Constitutional AI | Anthropic의 원칙 기반 자기비평·수정 훈련 방식 |
| Cascade evaluation | 소형 비평 모델이 대형 모델 출력을 실시간 채점 |
| Mirror problem | 편향 모델이 자신의 편향도 잘못 평가할 수 있다는 한계론 |
| RLHF | Reinforcement Learning from Human Feedback |
| Hallucination | AI가 사실과 다른 내용을 확신 있게 생성하는 현상 |
