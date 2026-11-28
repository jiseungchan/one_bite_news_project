---
title: "에이전트 스킬 표준, 중립 재단에 기증 — AI 에이전트의 공통 언어가 만들어지고 있다"
date: 2026-10-28
category: AI
source: "Anthropic"
sourceUrl: "https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation"
description: "앤트로픽이 Agent Skills 오픈 표준을 에이전틱 AI 파운데이션(AAIF)에 기증했다. ChatGPT·Cursor·GitHub Copilot 등 70개 플랫폼이 이미 통합, 설치 수 2억 8,000만 건을 넘겼다."
---

앤트로픽이 2025년 12월 발표한 '에이전트 스킬(Agent Skills)' 오픈 표준을 에이전틱 AI 파운데이션(Agentic AI Foundation, AAIF)에 기증했다. AAIF는 앤트로픽이 블록(Block)과 오픈AI(OpenAI)와 함께 공동 창설한 리눅스 재단(Linux Foundation) 산하 기관이다.

## 에이전트 스킬이란 무엇인가

에이전트 스킬은 AI 에이전트에게 특정 업무 도메인의 절차적 지식과 워크플로(workflow — 업무 처리 절차)를 패키지 형태로 전달하는 표준이다. 핵심은 단순하다 — SKILL.md 파일이 담긴 폴더 하나가 하나의 스킬이다. 여기에 해당 업무에 필요한 스크립트나 레퍼런스 자료를 함께 담는다.

이 표준은 이론에서 출발한 게 아니다. 앤트로픽이 Claude Code(AI 기반 코딩 에이전트 도구)를 직접 만들면서 "범용 AI 에이전트는 실제 업무에서 절차적 지식이 부족하다"는 문제를 몸으로 겪고 개발한 표준이다.

## 숫자로 보는 현황

표준 공개 이후 지금까지:
- 배포된 스킬 수: **약 100만 개**
- 설치 수: **2억 8,000만 건**
- 통합 완료 에이전트 플랫폼: **70개 이상**

통합한 플랫폼 중에는 ChatGPT, Cursor, GitHub Copilot, VS Code가 포함된다. 경쟁 관계에 있는 플랫폼들이 같은 표준을 공유하고 있다는 점이 의미 있다.

## 이번 기증에서 넘긴 것들

앤트로픽이 AAIF에 넘긴 건 표준 명세(specification)만이 아니다. Agent Skills라는 이름과 로고, GitHub 조직 계정, agentskills.io 도메인까지 통째로 이전했다. AAIF에 합류하지 않은 조직도 이 표준을 자유롭게 쓰거나 기여할 수 있다.

기술 유지 관리는 앤트로픽·구글·오픈AI 등의 엔지니어들이 개인 자격으로 담당하며, 리드 메인테이너(Lead Maintainers)는 다비드 소리아 파라(David Soria Parra)와 마헤시 무라그(Mahesh Murag)가 맡는다.

## MCP와 같은 패턴

앤트로픽은 앞서 MCP(Model Context Protocol — AI 모델이 외부 도구·데이터에 접근하는 표준 프로토콜)도 AAIF에 기증한 전례가 있다. 이번 Agent Skills 기증은 같은 전략의 두 번째 실행이다.

이번에 내가 주목한 건 설계 철학이다. 에이전트들이 서로 다른 회사에서 만들어지더라도, 같은 스킬 파일을 공유할 수 있다면 '에이전트 생태계'가 비로소 성립한다. 앤트로픽이 MCP와 Agent Skills를 순차적으로 중립 기관에 넘기는 건 단순한 오픈소스 기여가 아니다 — AI 에이전트 시대의 공통 인프라를 스스로 설계하고, 그 위에 생태계를 쌓으려는 장기 포석이다.

표준을 기증하면 영향력이 줄어드는 게 아니라, 그 표준이 업계 표준이 될 때 영향력이 더 커진다. 이 역설을 앤트로픽이 이미 두 번째로 실행 중이다.

---

**원문**: [Donating Agent Skills to the Agentic AI Foundation](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation)
