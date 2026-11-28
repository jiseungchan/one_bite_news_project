---
title: "Google AI Threat Defense: AI가 사이버 공격을 자동으로 막는 시대"
category: AI
source: "Google Cloud Blog"
sourceUrl: "https://cloud.google.com/blog/products/identity-security/introducing-google-ai-threat-defense"
date: 2026-06-10
description: "Google Cloud가 AI 기반 자동 사이버보안 솔루션 'Google AI Threat Defense'를 출시했다. 취약점을 찾는 것을 넘어 우선순위 지정과 자동 수정까지 처리하는 방어 체계다."
image: "https://picsum.photos/seed/2026-06-10-google-ai-threat-defense/800/500"
---

## 한 줄 요약
> Google이 AI로 사이버 공격 방어를 자동화했다. '발견'이 아닌 '수정'까지 기계가 처리하는 체계다.

## 리드 — 왜 지금 이게 중요한가?

Google Cloud는 자사 인프라에서 매분 1천만 개의 스팸 이메일을 자동 차단한다고 밝혔다. 이 규모의 공격을 사람이 일일이 검토하는 것은 불가능하다. 2026년 5월 27일, Google Cloud는 이 경험을 외부 기업에 적용하는 'Google AI Threat Defense'를 공식 출시했다.

## 배경 — 기존에는 어땠나?

전통적인 사이버보안 접근 방식은 크게 두 단계로 나뉜다. 취약점 스캐너(보안 약점을 찾는 도구)가 문제를 탐지하면, 보안 팀이 목록을 검토하고 어떤 것을 먼저 고칠지 판단한 뒤 개발팀에 전달한다. 이 과정에 수일에서 수주가 걸린다.

문제는 공격자도 AI를 쓰기 시작했다는 점이다. 사람이 패치 우선순위를 논의하는 동안, 자동화된 공격 도구는 이미 알려진 취약점을 빠르게 스캔하고 침투를 시도한다. 기존 AI 보안 솔루션의 한계도 있었다. 대부분의 경쟁 제품은 취약점을 발견하는 것에 집중했고, 발견 이후의 우선순위 결정과 패치 작업은 여전히 인간의 몫이었다.

## 핵심 — 무엇이 다른가?

Google AI Threat Defense는 4단계 자동화 사이클로 작동한다.

1. **Prepare(준비)**: 조직의 보안 기반을 점검하고 자동 대응 체계를 설정한다.
2. **Scan and Prioritize(스캔 및 우선순위)**: AI가 취약점을 탐지하고 실제 침투 가능성 기준으로 우선순위를 매긴다. Wiz(클라우드 보안 스타트업으로 Google이 인수한 기업)의 위험 맵핑 기술이 활용된다.
3. **Remediate(수정)**: CodeMender(AI 기반 코드 보안 에이전트)가 자동으로 패치를 생성하고 검증한다.
4. **Monitor(모니터링)**: Mandiant(사이버보안 전문 기업으로 Google이 보유)의 위협 인텔리전스와 결합해 지속적으로 새로운 공격 패턴을 감시한다.

| 항목 | 기존 방식 | Google AI Threat Defense |
|------|-----------|-------------------------|
| 취약점 발견 | 스캐너 도구 | AI 기반 스캔 |
| 우선순위 결정 | 보안 팀 수동 검토 | AI 자동 위험 분류 |
| 패치 작업 | 개발자 직접 수정 | CodeMender 자동 생성 |
| 대응 속도 | 수일~수주 | 기계 속도(실시간) |

## 시장 영향

- 도입 사례: Morgan Stanley, MSCI, TELUS, Thales 등 금융·통신·방산 기업
- 구현 파트너: Accenture, Deloitte, PwC
- DORA 조사 기준 응답자의 90%가 직장에서 AI 도구를 사용한다고 밝혔으며, 보안 영역도 이 흐름에서 예외가 아니다.

## 병규의 한 줄

이번에 흥미로운 건 제품 기능보다 전제가 달라졌다는 점이다. 기존 보안 솔루션은 '인간이 판단하고 도구가 보조한다'는 구조였다면, Google AI Threat Defense는 '기계가 판단하고 수정하며 인간은 감독한다'는 역할 역전을 공식 선언한 셈이다.

---

**출처**: [Google Cloud Blog](https://cloud.google.com/blog/products/identity-security/introducing-google-ai-threat-defense)
