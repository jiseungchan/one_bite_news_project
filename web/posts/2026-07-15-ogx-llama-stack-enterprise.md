---
title: "Meta의 Llama Stack이 OGX로 진화했다 — GPT·Claude도 품은 오픈소스 AI 서버"
date: 2026-07-15
category: AI
source: "OGX 공식 블로그"
sourceUrl: "https://github.com/ogx-ai/ogx/blob/main/docs/blog/2026-07-14-multi-tenant-capabilities.md"
description: "Meta가 만든 Llama Stack이 'OGX'(Open GenAI Stack)로 이름을 바꾸고 모델 중립적 AI 인프라 서버로 탈바꾸었다. 최신 v1.2.0은 기업용 멀티테넌트 보안을 추가하며 엔터프라이즈 시장을 겨냥했다."
image: "https://picsum.photos/seed/2026-07-15-ogx-llama-stack-enterprise/800/500"
---

## 한 줄 요약
> Meta가 만든 오픈소스 AI 서버 Llama Stack이 'OGX'로 개명하고, 특정 모델에 얽매이지 않는 범용 AI 인프라 서버로 전략 전환했다.

## 리드 — 왜 지금 이게 중요한가?

7월 10일, OGX v1.2.0이 출시됐다. 릴리스 노트 한 줄로 요약하면 "기업이 단일 서버로 여러 고객사를 안전하게 서빙할 수 있는 멀티테넌트(multi-tenant, 하나의 서버 인스턴스를 여러 조직이 분리된 공간으로 나눠 쓰는 방식) 기능 추가"다. 이 업데이트가 눈에 띄는 이유는 기능 자체보다 그 배경에 있다. 한때 'Llama Stack'이라고 불렸던 이 프로젝트가 이제 GPT·Claude·Gemini를 포함한 23개 이상의 AI 모델을 동등하게 지원하는 범용 AI 서버로 진화해 있다는 점이다.

## 배경 — 기존에는 어딸나?

Llama Stack은 2026년 초 Meta가 자사 Llama 모델의 배포 표준화를 위해 공개한 오픈소스 프레임워크다. 그런데 문제가 있었다. 실제로는 GPT-4, Claude, Gemini, Mistral 등 23개 추론 제공자(inference provider)를 이미 지원하고 있었는데, 이름 탐에 "Meta 모델 전용 도구"로 오해받았다. 또한 'Stack'이라는 단어가 라이브러리 묶음시럼 느껴지만, 실체는 HTTP 서버였다.

결국 2026년 4월 28일, Meta 팀은 이름을 'OGX(Open GenAI Stack)'로 바꾸기로 결정했다. 공식 블로그에서 밝힌 이유는 세 가지다. "Llama 브랜드의 제한성", "'Stack'이 주는 프레임워크 오해", "멀티 제공자·멀티 SDK 서버로의 진화". 단순한 리브랜딩이 아니라 전략적 방향 전환이었다.

## 핵심 — 무엇이 다른가?

**모델 불가지론적(model-agnostic) 설계**
OGX는 OpenAI, Anthropic, Google의 API를 네이티브로 지원한다. 즉, 애플리케이션 코드를 한 줄도 바꾸지 않고 Llama에서 GPT로, GPT에서 Claude로 백엔드 모델을 교체할 수 있다. OpenAI API 호환 서버이기도 해서 기존 OpenAI SDK를 그대로 쓸 수 있다.

**v1.2.0의 멀티테넌트 보안 4단계**

기업이 단일 OGX 인스턴스로 여러 고객사를 운영하려면 데이터 격리가 필수다. v1.2.0은 이를 4단계 독립 보안 계층으로 구현했다.

| 계층 | 기술 | 설명 |
|------|------|------|
| 1단계 | 테넌트 파티션 | 모든 DB 쿼리에 `tenant_id` 필터 강제 적용 |
| 2단계 | 라우트 레벨 | API 경로별 접근 제어 |
| 3단계 | 리소스 레벨 | ABAC(속성 기반 접근 제어) |
| 4단계 | 레코드 레벨 | 소유자·팀 기반 세부 권한 |

ABAC(Attribute-Based Access Control, 속성 기반 접근 제어)란 "이 사용자는 이 팀에 속하고, 이 팀이 소유한 레코드만 읽을 수 있다"는 식으로 YAML 정송으로 권한을 선언하는 방식이다. 운영 모드는 세 가지다: 단일 사용자용 disabled, 단일 테넌트용 single, 멀티 조직용 multi.

인증은 OAuth2/OIDC, Kubernetes 서비스 계정, GitHub API 등 표준 신원 제공자와 연동된다.

## 시장 영향 — 어디에 쓰이나?

- **AI SaaS 스타트업**: 단일 OGX 인스턴스로 고객사별 데이터를 격리해 서빙 가능
- **기업 IT팀**: 자체 온프레미스(on-premises, 직접 운영하는 서버 환경) AI 인프라 구축 시 OpenAI 종속 탈피
- **AI 에이전트 플랫폼**: MCP(Model Context Protocol, 모델과 외부 도구 연결 표준) 통합으로 멀티스텝 에이전트 오케스트레이션 지원

GitHub에서 8,400개 이상의 스타를 받았으며, v1.2.1이 7월 14일 추가 버그픽스와 함께 출시됐다.

## 병규의 한 줄

"Llama"를 버린 건 겸손함이 아니다 — Meta가 자사 모델 에코시스템의 울타리를 스스로 헐물고 'AI 인프라 표준'이라는 더 큰 자리를 차지하려는 계산이다. 모델이 범용화될수록 인프라를 장악하는 쪽이 이긴다.

## 출처 & 더 읽기
- 원문(멀티테넌트 블로그): https://github.com/ogx-ai/ogx/blob/main/docs/blog/2026-07-14-multi-tenant-capabilities.md
- OGX 저장소: https://github.com/ogx-ai/ogx
- Llama Stack → OGX 배경: https://github.com/ogx-ai/ogx/blob/main/docs/blog/2026-04-28-from-llama-stack-to-ogx.md
