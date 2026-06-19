---
title: "SQL 몰라도 된다 — Microsoft가 내놓은 AI 데이터 분석 도구 Data Formulator 0.7"
date: 2026-06-18
category: AI
source: "Microsoft Research Blog"
sourceUrl: "https://www.microsoft.com/en-us/research/blog/data-formulator-0-7-ai-powered-data-analytics-for-enterprise-data/"
description: "Microsoft Research가 오픈소스 AI 데이터 분석 플랫폼 Data Formulator 0.7을 공개했다. SQL이나 코딩 없이 자연어로 기업 데이터를 분석하고 시각화할 수 있다."
image: "https://picsum.photos/seed/2026-06-18-data-formulator-07-enterprise-analytics/800/500"
---

## 한 줄 요약
> SQL도, 파이썬도 몰라도 된다 — Microsoft Research가 AI 에이전트를 이용해 기업 데이터를 자연어로 분석하는 오픈소스 도구를 공개했다.

## 리드 — 왜 지금 이게 중요한가?

데이터 분석은 여전히 '코드를 쓸 줄 아는 사람의 영역'이라는 인식이 남아 있다. SQL(구조화 질의 언어 — 데이터베이스에서 원하는 정보를 꺼내는 명령어)을 모르면 IT팀에 요청을 넣고 며칠을 기다려야 한다. Microsoft Research는 이 병목을 AI 에이전트로 뚫겠다는 접근을 내놨다. 2026년 5월 말 공개된 Data Formulator 0.7이 그 결과다.

## 배경 — 기존에는 어땠나?

기업 데이터 분석의 구조적 문제는 크게 두 가지였다. 첫째, 데이터 소스가 제각각이다. 데이터베이스, 데이터 웨어하우스(대규모 데이터를 한데 모아두는 저장소), BI 시스템(비즈니스 인텔리전스 — 경영 의사결정용 데이터 분석 플랫폼), 클라우드 객체 스토리지, 로컬 파일이 흩어져 있다. 분석가는 소스마다 연결을 따로 설정해야 했다.

둘째, 분석 흐름이 단절된다. 엑셀이나 BI 도구는 일회성 쿼리에 강하지만, 맥락이 길어지는 탐색적 분석에는 약하다. 어제 만든 차트가 오늘 다시 필요하면 처음부터 다시 만들어야 하는 경우가 많았다.

## 핵심 — 무엇이 다른가?

Data Formulator 0.7이 내세우는 핵심은 세 가지다.

**1. Data Connectors — 한 번 연결, 팀 전체 공유**
데이터베이스, BI 시스템, 클라우드 스토리지 등 여러 소스에 '관리형 재사용 연결(governed, reusable connections)'을 만들어둔다. 누군가 한 번 연결을 설정해두면 팀 전체가 동일한 연결을 재사용할 수 있다. 매번 인증 정보를 입력하거나 IT팀에 부탁할 필요가 없어진다.

**2. Context-aware Agents — 흐름을 기억하는 AI**
AI 에이전트(특정 목적을 위해 자율적으로 작업을 수행하는 AI 프로그램)가 단순히 질문에 답하는 수준을 넘어, 데이터를 직접 검사하고 코드를 작성·실행하며 차트 사양을 생성한다. 이전 분석 맥락을 유지하면서 다음 단계를 제안한다는 점이 기존 챗봇과 다르다.

**3. Data Thread & Interactive Canvas — 분기 분석 지원**
'Data Thread'라는 구조화된 대화 형식으로 분석 이력이 쌓인다. 마치 코드 버전 관리처럼, 특정 시점으로 돌아가거나 분석을 두 방향으로 나눠 비교하는 것이 가능하다. 인터랙티브 캔버스에서는 생성된 시각화를 실시간으로 수정할 수 있다.

| 항목 | 기존 방식 | Data Formulator 0.7 |
|---|---|---|
| 데이터 연결 | 소스마다 개별 설정 | 관리형 연결 팀 공유 |
| 분석 도구 | SQL / Python 코딩 필요 | 자연어 질문으로 처리 |
| 분석 맥락 | 세션 종료 시 초기화 | Data Thread로 이력 보존 |
| 시각화 수정 | 코드 재작성 | 캔버스에서 직접 조작 |

## 시장 영향 — 어디에 쓰이나?

- 오픈소스로 공개돼 GitHub에서 바로 설치 가능하고, 데모 사이트(data-formulator.ai)에서 체험할 수 있다.
- SQL·코딩 비전문가인 기획자, 마케터, 경영진이 직접 데이터 탐색을 할 수 있는 환경을 만드는 것이 목표다.
- 연구팀은 Microsoft의 Chenglong Wang, Michel Galley, Jianfeng Gao 등이 주도했다.

## 병규의 한 줄

이 도구가 담고 있는 철학은 '데이터 민주화'라는 익숙한 단어보다 날카롭다. 코딩 없는 분석이 아니라, AI가 코드를 대신 써주면서도 분석 맥락이 끊기지 않도록 하는 구조 — '분기와 이력'을 분석 과정에 집어넣은 게 진짜 변화다.

## 출처 & 더 읽기
- 원문: https://www.microsoft.com/en-us/research/blog/data-formulator-0-7-ai-powered-data-analytics-for-enterprise-data/
