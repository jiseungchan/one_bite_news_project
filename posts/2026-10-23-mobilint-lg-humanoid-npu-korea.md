---
title: "국산 NPU로 움직이는 휴머노이드 — 모빌린트·LG·노타가 만드는 K-로봇 AI칩"
date: 2026-10-23
category: AI
source: "TechTimes"
sourceUrl: "https://www.techtimes.com/articles/329411/20261023/mobilint-tapped-lead-koreas-606m-device-ai-chip-program-humanoid-robots.htm"
description: "모빌린트가 정부 주도 K-온디바이스 AI 반도체 사업(2026~2030년, 약 8,002억 원)에서 휴머노이드 로봇 파트 주관 기업으로 선정됐다. LG전자가 로봇 시스템을, 모빌린트가 NPU를, 노타가 모델 경량화를 담당한다."
---

2026년 10월 22일, 스타트업 하나의 이름이 국내 로봇 산업 지형에 조용히 박혔다. 모빌린트(Mobilint)다.

## 배경 — 휴머노이드 로봇의 AI 두뇌 문제

휴머노이드 로봇이 작동하려면 시각, 언어, 행동을 동시에 처리하는 AI가 필요하다. 이걸 **VLA(Vision-Language-Action — 시각·언어·행동 통합) 모델**이라고 부른다. 문제는 이 모델이 무겁다는 것. 클라우드 서버에 연결해야 실시간으로 돌릴 수 있어서, 통신 지연이나 보안 문제가 생긴다.

그래서 업계의 숙제는 로봇 안에서 직접 AI를 구동하는 **온디바이스(on-device) AI**다. 스마트폰에 AI를 넣는 것보다 훨씬 복잡하다. 로봇은 배터리·발열·진동 환경에서 사람보다 빠른 반응 속도가 필요하기 때문이다.

현재 AI 로봇의 핵심 칩은 대부분 엔비디아 GPU다. 이 의존도를 낮추는 것이 한국 반도체 산업의 중장기 과제 중 하나였다.

## 핵심 — 세 회사의 역할 분담

한국 정부의 **K-온디바이스 AI 반도체 사업(2026~2030년, 약 8,002억 원 예산)**에서 모빌린트가 휴머노이드 서브프로젝트 주관 기업으로 선정됐다. 세 회사의 역할은 명확하게 나뉜다.

| 역할 | 담당 기업 |
|------|----------|
| 휴머노이드 시스템 설계·검증 | LG전자 |
| NPU(신경망처리장치 — AI 연산에 특화된 반도체) 공급 | 모빌린트 |
| VLA 모델 경량화 소프트웨어 | 노타(Nota AI) |

모빌린트가 만드는 것은 NPU 단독이 아니다. NPU, 소형 가속기 모듈, 소프트웨어를 묶은 **온디바이스 AI 컴퓨팅 플랫폼** 전체다.

노타는 VLA 모델을 모빌린트 칩 위에서 실행할 수 있도록 **토큰 압축**, **양자화(quantization — 모델 정밀도를 낮춰 크기를 줄이는 기술)**, **가지치기(pruning — 필요 없는 신경망 연결을 제거하는 기술)**를 적용한다.

LG전자 휴머노이드의 실제 운용 시나리오에서 단계적 검증이 이뤄질 예정이다. 파트너십은 9월 8일 처음 공개됐고, 모빌린트의 플랫폼 업데이트 발표가 10월 22일 나왔다.

## 시장 영향 — 국산 NPU의 첫 시험대

엔비디아는 로봇 AI 칩 시장에서도 주도권을 쥐려 하고 있다. 젯슨(Jetson) 시리즈 등 임베디드 AI 컴퓨팅 플랫폼을 확장해 왔다. 국산 NPU가 이 자리를 대체할 수 있다면, 로봇 산업에서의 AI 칩 공급망 구조가 바뀐다.

미국의 대(對)중국 반도체 수출 규제 이후, 한국 역시 핵심 AI 반도체의 공급 다변화 필요성이 높아졌다. 이 사업은 그 맥락 위에 있다.

- 모빌린트는 이외에도 두산로보틱스, 대동과 가전·로봇용 AI 칩 프로젝트를 추가로 진행 중
- 사업 예산 수치는 단일 보도 기준 — 공식 발표 확인 필요

## 병규의 한 줄

이번에 흥미로운 건 LG전자가 '검증자' 역할을 맡았다는 점이다. 칩을 만드는 게 아니라, 실제 운용 시나리오를 제공하는 쪽이다. 가전 강자가 로봇 AI 생태계의 테스트베드가 되는 구조 — 한국 제조업이 AI 시대에 자신의 포지션을 재정의하는 방식이 흥미롭다.

---

**출처**: [TechTimes](https://www.techtimes.com/articles/329411/20261023/mobilint-tapped-lead-koreas-606m-device-ai-chip-program-humanoid-robots.htm) | [Seoul Economic Daily](https://en.sedaily.com/technology/2026/10/22/mobilint-develops-ai-chip-platform-for-humanoid-robots-eyes) | [Edge AI and Vision Alliance](https://www.edge-ai-vision.com/2026/09/nota-ai-to-optimize-on-device-ai-for-humanoid-robots-connecting-lg-electronics-robot-platform-with-mobilints-npu/), 2026년 10월 22~23일
