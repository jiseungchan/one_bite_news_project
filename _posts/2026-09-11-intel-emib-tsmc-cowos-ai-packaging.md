---
title: "구글·아마존은 인텔로, 엔비디아는 TSMC로 — AI 반도체 패키징 판세가 갈렸다"
date: 2026-09-11
category: 나노·소재
source: "TechTimes"
sourceUrl: "https://www.techtimes.com/articles/327312/20260911/emib-vs-cowos-google-amazon-back-intel-inference-nvidia-keeps-training-tsmc.htm"
description: "AI 칩이 거대해지면서 패키징 기술이 새 경쟁 전선이 됐다. TSMC CoWoS의 78주 리드타임과 고비용에 지친 구글·아마존이 인텔 EMIB를 선택하기 시작했고, 엔비디아는 여전히 TSMC를 고수했다."
---

## AI 칩이 커질수록 패키징이 문제가 된다

AI 가속기(AI 연산 전용 반도체)는 최근 수년간 급격히 거대해졌다. 엔비디아 GB200 같은 고성능 칩은 여러 개의 다이(die — 반도체 회로가 새겨진 개별 실리콘 조각)를 하나의 패키지에 연결해 하나처럼 작동시키는 '칩렛(chiplet)' 방식을 쓴다. 이 연결 과정을 '고급 패키징(Advanced Packaging)'이라 부르는데, 칩이 커질수록 패키징의 난이도와 비용이 기하급수적으로 오른다.

지금까지 이 시장의 사실상 독점자는 TSMC였다. TSMC의 CoWoS(Chip on Wafer on Substrate — 웨이퍼 위에 칩을 얹고 기판에 연결하는 방식)는 엔비디아·AMD 등 거의 모든 AI 칩의 패키징을 담당해왔다.

## TSMC CoWoS의 한계

문제는 공급이다. CoWoS의 내년 물량은 이미 주문이 완료됐고, 리드타임(발주부터 납품까지 걸리는 시간)은 최대 78주까지 늘어났다. 한 번 발주하면 1년 반을 기다려야 한다는 뜻이다. 루빈급 가속기 기준 칩 한 개당 패키징 비용도 약 900~1,000달러(약 135만 원)에 달한다.

## 인텔 EMIB의 역습

인텔이 내세우는 대안이 EMIB-T(Embedded Multi-die Interconnect Bridge Thin)다. 전체 기판 크기의 실리콘 인터포저 대신, 필요한 지점에만 소형 실리콘 브리지를 기판 안에 내장하는 방식이다. 덕분에 비용이 CoWoS 대비 약 50% 낮다. 인텔 EMIB 기준 패키징 비용은 수백 달러대로 알려졌다. 수율(생산 과정에서 정상 제품이 나오는 비율)도 최근 90%를 돌파하며 안정화 단계에 접어들었다.

| 항목 | TSMC CoWoS | 인텔 EMIB-T |
|------|-----------|------------|
| 패키징 비용 | 칩당 약 $900~1,000 | 수백 달러대 (약 50% 절감) |
| 수율 | 98~99% | 90%+ (개선 중) |
| 납품 대기 | 최대 78주 | 상대적으로 짧음 |
| 주요 고객 | 엔비디아 (훈련 워크로드) | 구글·아마존 (추론 워크로드) |

## 전략적 분리가 선명해졌다

9월 11일 현재, 빅테크 고객군이 두 갈래로 나뉘는 흐름이 구체화되고 있다. 구글과 아마존은 추론(inference — 이미 학습된 모델을 실제 서비스에 돌리는 연산) 워크로드에 인텔 EMIB를 선택하기 시작했다. 훈련(training — AI 모델 자체를 학습시키는 연산)보다 낮은 성능 마진, 더 높은 물량과 비용 효율 요구에 EMIB가 더 잘 맞기 때문이다. 반면 엔비디아는 자사 플래그십 훈련 가속기 라인에서 여전히 TSMC를 고수하고 있다.

TSMC도 손을 놓고 있지 않다. 대만 기판 전문 업체 킨서스(Kinsus Interconnect Technology)와 공동으로 EMIB 유사 기술을 개발 중이다.

## 병규의 한 줄

지금까지 AI 반도체 경쟁은 '누가 더 좋은 칩을 설계하느냐'였는데, 이제는 '누가 더 효율적으로 칩들을 연결하느냐'로 무게가 이동하고 있다. 패키징이 성능과 비용의 다음 병목이 된 것이다. 인텔이 칩 설계 경쟁에서 뒤처진 자리를 패키징으로 메우는 이 구도는 단순한 기술 경쟁이 아니라 AI 공급망 전략의 근본 재편이다.

---

**출처**: [TechTimes](https://www.techtimes.com/articles/327312/20260911/emib-vs-cowos-google-amazon-back-intel-inference-nvidia-keeps-training-tsmc.htm) · [아시아경제](https://www.asiae.co.kr/article/2026080711480224145) · [카운터포인트리서치](https://korea.counterpointresearch.com/intel-emib-zam-xbm-vs-tsmc-cowos-ai-packaging-2026/)
