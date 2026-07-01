---
title: "구글, AI 에이전트 개발 전 과정을 단일 CLI로 통합한 'agents-cli' v1.0 출시"
category: AI
source: "GitHub (google/agents-cli)"
sourceUrl: "https://github.com/google/agents-cli"
date: 2026-07-01
description: "구글이 AI 에이전트를 빌드·평가·배포하는 전 과정을 단일 CLI로 묶은 'agents-cli' v1.0.0을 7월 1일 정식 출시했다. Claude Code, Codex 등 주요 코딩 어시스턴트와 직접 연동된다."
image: "https://picsum.photos/seed/2026-07-01-google-agents-cli/800/500"
---

## 한 줄 요약
> 구글 클라우드에서 AI 에이전트를 만들고 평가하고 배포하는 과정 전체가, CLI 명령 몇 줄로 줄어들었다.

## 리드 — 왜 지금 이게 중요한가?
구글이 7월 1일, AI 에이전트 개발 도구 `agents-cli`의 v1.0.0 — 즉 GA(General Availability, 정식 출시) 버전을 공개했다. 출시 당일에만 GitHub 스타 4,500개 이상이 쌓였다. 단순한 CLI 도구가 아니라, 코딩 어시스턴트(Claude Code, Codex 등)에 "에이전트 전문가 스킬"을 심어주는 방식이 주목받고 있다.

## 배경 — 기존에는 어땠나?
AI 에이전트 개발의 진짜 병목은 코딩이 아닌 배포 이후다. 구글의 ADK(Agent Development Kit — 구글의 AI 에이전트 개발 프레임워크)로 에이전트를 만들어도, Cloud Run이나 GKE(Google Kubernetes Engine — 구글의 컨테이너 오케스트레이션 서비스)에 올리는 설정을 별도로 구성해야 했다. 더 큰 문제는 재배포할 때마다 기존 설정이 초기화됐다는 점이다. 평가 파이프라인도 개발자마다 제각각으로 구축해야 했다.

## 핵심 — 무엇이 다른가?

agents-cli의 설계 철학은 "에이전트를 만드는 코딩 어시스턴트에게 스킬을 주입한다"는 것이다. 명령 한 줄(`npx skills add google/agents-cli`)로 Claude Code 같은 도구에 설치하면, 이후 에이전트 개발의 전 과정이 자동화된다.

| 단계 | 기존 방식 | agents-cli |
|------|-----------|----------|
| 프로젝트 생성 | 수동 ADK 구성 | `uvx google-agents-cli setup` 1회 |
| 평가 | 개발자가 직접 메트릭 정의 | LLM 기반 채점 + 추적 내장 |
| 배포 | Cloud Run/GKE 수동 설정 | 명령 1개, 기존 설정 유지 |
| RAG 연동 | 별도 구현 | "clone-and-study" 샘플 제공 |

RAG(검색 증강 생성 — AI가 외부 문서를 검색해 답변을 보강하는 기법)는 v1.0에서 큰 변화가 있었다. 기존 복잡한 템플릿 방식 대신 `rag-vector-search`, `rag-agent-search` 샘플을 보고 따라 구현하는 "레시피" 형태로 전환됐다. 관찰성(Cloud Trace 기반 로깅)도 기본 탑재돼, 에이전트가 어떻게 동작하는지 프로덕션에서 추적할 수 있다.

## 시장 영향 — 어디에 쓰이나?
- **지원 코딩 도구**: Claude Code, Codex, Antigravity CLI 등
- **배포 대상**: Google Cloud Run, GKE, Agent Runtime, Gemini Enterprise
- **라이선스**: Apache 2.0 (상업 사용 자유)
- **요구 환경**: Python 3.11+, uv, Node.js

## 병규의 한 줄
이번에 흥미로운 건 ADK(에이전트 프레임워크)와 agents-cli(개발 전주기 도구)를 분리한 설계다. "프레임워크는 따로, 파이프라인은 따로"라는 구분 — 구글이 에이전트 개발의 표준 워크플로를 먼저 정의하고 생태계를 고정하려는 움직임으로 읽힌다.

## 출처 & 더 읽기
- 원문: https://github.com/google/agents-cli
- 릴리즈 노트: https://github.com/google/agents-cli/releases/tag/v1.0.0
