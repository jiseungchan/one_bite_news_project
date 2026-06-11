---
title: NVIDIA RTX Spark — PC에 AI 두뇌를 심다
category: AI
source: NVIDIA Newsroom
sourceUrl: https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark
date: 2026-06-05
description: 엔비디아가 Computex 2026에서 PC용 AI 슈퍼칩 'RTX Spark'를 공개했다. 1 페타플롭 AI 연산 성능으로 120B 파라미터 LLM을 오프라인에서 구동하며, 2026년 가을 Dell·HP·Microsoft 등 6개 브랜드에 탐재 예정이다.
image: https://picsum.photos/seed/2026-06-05-nvidia-rtx-spark-pc-ai/800/500
---

## 한 줄 요약
> 엔비디아가 PC 칩 시장에 첫발을 내디디며, 로친 AI 에이전트 시대의 물꼼를 템다.

## 리드 — 왜 지금 이게 중요한가?

Computex 2026에서 엔비디아가 공개한 'RTX Spark'는 단순한 신형 칩이 아니다. AI 연산 성능 1 페타플롭(1초에 1,000조 번 연산하는 속도)을 PC 한 대에 담아냈다. 인터넷 없이도 120억 파라미터급(B는 billion, 10억 단위)이 아닌 무려 1,200억(120B) 파라미터 규모의 대형 언어 모델을 100만 토큰 컨텍스트(AI가 한 번에 처리할 수 있는 텍스트 분량)로 돌릴 수 있다는 뜻이다. 클라우드 없이, 구독료 없이.

## 배경 — 기존에는 어딸나?

지금까지 PC 칩 시장은 사실상 인텔과 AMD의 양자 구도였다. CPU(중앙처리장치)가 두 회사의 전유물이었고, 그래픽이나 AI 연산이 필요하면 별도의 GPU(그래픽처리장치) 카드를 추가로 꼽는 방식이었다.

AI 시대로 넘어오면서 이 한계는 더 도드라졌다. ChatGPT 같은 대형 AI 모델을 로컈에서 실행하려면 막대한 VRAM(GPU 전용 메모리)이 필요한데, 일반 PC로는 현실적으로 불가능했다. 결국 대부분의 AI 작업은 클라우드 서버에 의존해야 했다.

## 핵심 — RTX Spark는 무엇이 다른가?

RTX Spark의 핵심은 '통합 설계'다. 통합 메모리(CPU와 GPU가 같은 메모리 풀을 공유하는 구조)를 채택해 두 프로세서가 데이터를 복사하지 않고 직접 공유한다. MediaTek과 공동 설계한 Arm 기반 CPU(최대 20코어)와 Blackwell 세대 GPU(CUDA 코어 — GPU 안의 연산 처리 단위 — 6,144개)가 한 칩 위에 올라간다.

| 항목 | 기존 PC (CPU + 외장 GPU) | RTX Spark |
|---|---|---|
| 메모리 구조 | CPU·GPU 메모리 분리 | 최대 128GB LPDDR5X 통합 |
| 메모리 대역폭 | 수십 GB/s 수준 | 최대 300 GB/s |
| AI 성능 | 별도 GPU 카드 필요 | 1 페타플롭 (내장) |
| LLM 로컈 실행 | 소형 모델에 그침 | 120B 파라미터, 오프라인 가능 |

마이크로소프트와의 협력도 눈여겻볼 대목이다. Windows를 AI 에이전트 OS(사용자 대신 작업을 자율 수행하는 AI가 내장된 운영체제)로 전환하는 것이 공동 목표로, RTX Spark는 그 하드웨어 기반을 맡는다.

## 시장 영향 — 어디에 쓰이나?

- **출시 예정**: 2026년 가을, Dell·HP·Microsoft·ASUS·Lenovo·MSI 6개 브랜드 PC에 탐재
- **AI 에이전트 생태계**: 인터넷 연결 없이 개인 PC에서 대형 모델 구동 → 프라이버시 중심 AI 서비스 확산 가능
- **경쟁 구도**: AMD 주가 -8%, 인텔도 하락 — 30년 가까이 유지된 x86 PC 칩 독점 구도에 처음으로 균열이 생겼다

## 병규의 한 줄

이번 발표에서 주목할 건 스펙 수치보다 전략적 선언이다. 엔비디아는 "AI는 클라우드에 있다"는 지난 10년의 전제를 뒤집고, AI의 무게 중심을 다시 엣지(사용자 기기)로 당기겠다는 판단을 내렸다.

## 출처 & 더 읽기
- 원문: https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark
