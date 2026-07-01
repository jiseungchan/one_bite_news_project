---
title: "Claude Sonnet 5, Google Cloud 정식 탑재 — AI 클라우드 3파전의 판이 바뀐다"
category: 경제·주식
source: "Google Cloud Blog"
sourceUrl: "https://cloud.google.com/blog/topics/inside-google-cloud/whats-new-google-cloud"
date: 2026-07-01
description: "Anthropic의 최신 모델 Claude Sonnet 5가 Google Cloud Agent Platform에 정식 출시됐다. 강화된 추론, 코드 생성 개선, 데스크탑·브라우저 자동화 기능을 탑재했으며, 구글은 이로써 기업용 AI 시장에서 OpenAI(Azure), Claude(AWS)와 3파전 구도를 형성했다."
image: "https://picsum.photos/seed/2026-07-01-claude-sonnet5-google-cloud/800/500"
---

## 한 줄 요약
> Anthropic의 Claude Sonnet 5가 Google Cloud에 정식 올라탔다 — 이는 단순한 모델 업데이트가 아니라, AI 클라우드 시장에서 구글이 '선택지 다양성'으로 기업 고객을 잡겠다는 선언이다.

## 리드 — 왜 지금 이게 중요한가?

이번 주(6월 29일~7월 3일), Anthropic의 Claude Sonnet 5가 Google Cloud Agent Platform에서 정식 출시됐다. 기존 Claude Sonnet 4.6의 완전한 대체 모델로 포지셔닝됐으며, 기업은 API 연동을 바꾸지 않고도 최신 모델로 전환할 수 있다. AI 클라우드 시장에서 구글이 Anthropic 모델을 앞세워 Microsoft Azure(OpenAI 독점 파트너), AWS Bedrock과 본격 3각 경쟁에 돌입했다는 신호다.

## 배경 — AI 클라우드는 지금 '모델 전쟁'

기업용 AI 클라우드 시장은 2025년까지 단순히 '누가 더 싼 컴퓨팅을 제공하느냐'의 싸움이었다. 하지만 2026년부터는 판이 달라졌다. 기업 고객들은 최고 성능의 AI 모델을 자신이 이미 쓰는 클라우드 인프라에서 직접 호출하길 원한다. 모델을 직접 운영하거나 외부 API를 별도로 관리하는 복잡함을 없애고 싶기 때문이다.

이 틈새를 가장 먼저 치고 나간 건 Microsoft였다. Azure는 OpenAI에 수백억 달러를 투자하며 GPT 계열 모델을 Azure OpenAI Service로 독점 제공한다. AWS는 Bedrock을 통해 Anthropic, Meta, AI21 등 다양한 모델을 제공하며 '중립적 플랫폼' 전략을 폈다. 이에 맞서 Google Cloud는 자체 Gemini 모델과 함께 Anthropic의 Claude를 Vertex AI(버텍스 AI·구글의 AI 개발 플랫폼)에 탑재하는 전략을 선택했다.

## 핵심 — Claude Sonnet 5가 달라진 것

Claude Sonnet 5는 구글 클라우드의 Agent Platform(에이전트 플랫폼·기업용 AI 에이전트 구축·운영 통합 플랫폼)에 올라온 가장 최신 Anthropic 모델이다.

기존 Sonnet 4.6 대비 달라진 점 세 가지:

| 항목 | Sonnet 4.6 | Sonnet 5 |
|---|---|---|
| 추론 능력 | 기본 수준 | 강화(Enhanced Reasoning) |
| 코드 생성 | 일반 수준 | 개선된 클린 코드 생성 |
| 컴퓨터 제어 | 미지원 | 데스크탑·브라우저 자동화 지원 |

특히 '컴퓨터 사용(Computer Use)' 기능이 주목할 만하다. AI 모델이 직접 마우스와 키보드를 제어하듯 데스크탑 프로그램이나 브라우저를 조작할 수 있다. 마치 AI 직원이 컴퓨터 앞에 앉아 작업을 대신하는 것과 같은 개념이다. 이는 RPA(로보틱 프로세스 자동화)와 맞닿은 기업용 자동화 시장에 직접 영향을 준다.

구글은 이미 Claude Opus 4.8(5월 출시)도 Gemini Enterprise Agent Platform에서 제공 중이다. 기업은 상황에 따라 고성능 Opus 4.8과 빠르고 실용적인 Sonnet 5를 선택해 쓸 수 있다.

## 시장 영향 — 기업 AI 클라우드 선택 구도가 바뀐다

- **기업 선택지 확대**: 기존엔 Azure(GPT), AWS Bedrock(Anthropic+기타)이 양강이었다면, 이번으로 Google Cloud도 Anthropic 최신 모델을 제공하는 '풀스택' 선택지가 됐다
- **컴퓨터 사용 기능**: RPA 시장(2025년 기준 약 40억 달러 규모) 대체 수요를 AI 에이전트가 흡수하는 흐름을 가속할 수 있다
- **Google의 Anthropic 투자 실익**: Google은 Anthropic에 수억 달러를 투자한 주요 투자자이기도 하다. Claude가 구글 플랫폼에서 더 많이 쓰일수록 Anthropic의 클라우드 API 매출이 늘고, 구글의 투자 수익도 커지는 구조다

## 병규의 한 줄

이번 소식에서 흥미로운 건 모델 성능이 아니라 '배포 레이어'다. 구글은 자체 Gemini로 OpenAI와 경쟁하는 동시에, OpenAI의 최대 경쟁사(Anthropic)를 플랫폼에 올려 Microsoft를 에워싸는 전략을 쓰고 있다. AI 전쟁의 전선은 모델에서 클라우드 플랫폼 지배력으로 옮겨가고 있다.

## 출처 & 더 읽기
- 원문: https://cloud.google.com/blog/topics/inside-google-cloud/whats-new-google-cloud
