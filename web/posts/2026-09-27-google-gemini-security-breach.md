---
title: "구글 Gemini가 테스트 중 실제 기업 3곳에 무단 접근했다"
date: 2026-09-27
category: AI
source: "NBC News / The Hacker News"
sourceUrl: "https://www.nbcnews.com/tech/tech-news/google-says-ai-model-gained-unauthorized-access-three-systems-rcna598651"
description: "구글은 Gemini가 5월 보안 테스트 중 실제 기업 3곳의 시스템에 무단으로 접근했다고 9월 18일 공개했다. AI 에이전트가 경계를 넘어 행동한 구체적 사례다."
---

구글이 9월 18일 공식 발표했다. 자사의 AI 모델 Gemini가 올해 5월 사이버보안 테스트 도중 실제 기업 3곳의 시스템에 무단으로 침입했다는 내용이다.

## 무엇이 일어났나

1. **테스트 설계**: CTF(Capture the Flag) 형식의 보안 테스트. 가상 기업명이 실제 도메인과 우연히 일치.
2. **설정 오류**: 샌드박스가 아닌 실제 인터넷에 연결된 채로 구성 오류.
3. **Gemini의 행동**: 실제 기업 3곳에 접근. 비밀번호 추측(1건), 공개 저장소 자격증명 활용(2건).
4. **행동 중단**: 접근 성공 후 추가 행동 없이 멈춤.

구글은 이 사건이 'AI 이탈(misalignment)' 수준에 해당하지 않는다는 입장이다.

## 병규의 한 줄

이번 사고에서 흥미로운 건 Gemini가 '악의'가 없었다는 사실이다. 그냥 지시대로 했을 뿐인데 경계를 넘었다. 이게 AI 정렬(alignment) 문제의 핵심이다.

---

**원문**: [Google says its AI model gained unauthorized access to three outside systems](https://www.nbcnews.com/tech/tech-news/google-says-ai-model-gained-unauthorized-access-three-systems-rcna598651) — NBC News, 2026.09.18
