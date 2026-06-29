# Phase 2.1 — v8 9종 교차 검토 (검토1) 종합

> 9 Opus 검수(리뷰 전용·~500행 청크·refute mandate·★G-derive 1급 렌즈·KNOWN_DEFECTS 전수 대조). 개별 = 각 `v8-NN/REVIEW1.md`.

## 점수 매트릭스 (척추·부호·G-derive·G-follow·G-usable·완결성·그림 등, 합 /35)

| 버전 | 모델 | 합 | 부호 8항 | D-PEAK(★상속) | 그 외 KNOWN_DEFECTS | 가장 약한 1곳 |
|---|---|---:|---|---|---|---|
| **v8-06** | Opus | **31** | 8/8 | ✗ 미수정(L916·931) | VEQ·DHEFF·WEFF·UBR·VN **5종 해소** | D-PEAK(fig:relaxode 캡션이 오개념 강화) |
| v8-07 | Codex | 31 | 8/8 | ✗ 미수정(L890) | VEQ·DHEFF·fig 해소 / UBR·WEFF 부분 | D-PEAK |
| v8-05 | Opus | 30 | 8/8 | ✗ 미수정(L889) | DHEFF·WEFF·UBR 해소 / VEQ 부분 | D-PEAK |
| v8-09 | Codex | 30 | 8/8 | ✗ 미수정(L919) | VEQ·DHEFF·UBR 해소 / WEFF | D-PEAK |
| v8-08 | Codex | 27 | 8/8 | ✗ 미수정(L896) | DHEFF·fig 해소 / VEQ·WEFF | D-PEAK·D-VEQ |
| **v8-01** | Sonnet | 26 | 8/8 | ✅ **유일 미보유**(이산 모드 분기) | VEQ·WEFF 해소 / UBR·DHEFF 부분 | ★CRIT: staging U값 오류(0.120/0.090/0.075≠정본)·eq:vn 중복 라벨 |
| v8-02 | Sonnet | 26 | 8/8 | ✗ 미수정(L863) | VN·fig 해소 / PEAK·DHEFF·WEFF·VEQ 잔존 | D-PEAK |
| v8-04 | Opus | 26 | 8/8(본문) | ✗ 미수정(L905) | WEFF(4Fw 검산통과)·UBR·DHEFF·VN 해소 | ★CRIT: fig:overshoot 식번호 오기(1.18=1.16→1.13=1.10)·라벨 뒤바뀜 |
| v8-03 | Sonnet | 24 | 8/8 | ✗ 미수정(L867) | UBR만 해소 / PEAK·VEQ·DHEFF·WEFF 잔존 | D-PEAK |

## ★ 헤드라인 — 系統 결함 D-PEAK 의 전파 (경쟁의 핵심 성과)
**eq:peakshape 의 "$L_V$ 작으면 평형 종 환원" 은 v7-11 상속 수학 오류**($\rho=e^{-\Delta_{grid}/L_V}$, $L_V\to0\Rightarrow\rho\to0\Rightarrow$ peak$\to0$; 종 환원은 반대극한 $L_V\gg\Delta_{grid}$; 작은 $L_V$ 평형회복은 eq:branch 코드 스위치 담당). **9종 중 8종이 v7-11 박스·문장을 보존하다 그대로 전파**했고, **v8-01 만 독립적으로 회피**(평형/꼬리를 이산 모드 분기로 처리). 부호 8항은 전 9종 v11 1:1 PASS(결함 0) — 결함은 *유도 서술*에 집중(G-derive 렌즈가 아니었으면 통과됐을 것). v8-04 의 자체 다중-agent 감사가 이 결함을 선적발한 것이 KNOWN_DEFECTS 의 출발.

## 체리픽 플랜 (Phase 5 — v6 합류)
- **베이스 = v8-06**(31·KNOWN_DEFECTS 5종 해소·유도 본문 풍부·그림 9개). 보완 후 최종 베이스 확정.
- **★핵심 graft = v8-01 의 D-PEAK 처리**(평형/꼬리 이산 모드 분기 서술 — 거짓 극한 없는 유일본). 단 v8-01 의 staging 표 오류는 이식 금지.
- 추가 graft 후보: v8-04 D-WEFF 4Fw 다리(검산 통과)·v8-05 D-DHEFF/UBR 유도·v8-06 5종 해소 유도·그림 경쟁 풀(v8-06 9개 등에서 최적).
- **★이식 금지**: v8-01 staging U값 오류·eq:vn 중복 라벨 / v8-04 fig:overshoot 식번호 오기·라벨 뒤바뀜·곡선 중복.

## 보완 방향 (Phase 3 재지시 — 방향성만)
- **전 8종(01 제외)**: ★D-PEAK 수정 — "L_V 작으면 종 환원" 삭제, 평형회복은 eq:branch 스위치·매끈한 환원은 $L_V\gg\Delta_{grid}$ 로 정정.
- v8-06/05/07/09/08/02/03: 각자 잔존 D-VEQ(inline 다리)·D-DHEFF(χ_d 중간식)·D-WEFF(4Fw 다리)·D-UBR(ansatz 명시) 보완.
- v8-01: staging 표 U값을 정본(0.140/0.120/0.085…)으로·eq:vn 중복 라벨 제거·D-UBR/DHEFF 보완(D-PEAK 처리는 유지=강점).
- v8-04: fig:overshoot 식번호(1.13=1.10)·분기 라벨 정정·곡선 중복 제거·D-PEAK·D-VEQ·orphan bib.
- 공통: orphan bib(eyring/bazant/dreyer) 본문 인용, 그림 orphan 0.

## Gate
PASS_REVIEW1 — 9종 G-derive 포함 전 렌즈 검토·D-PEAK 전파 확정·v8-01 graft 자산 식별·체리픽 베이스(v8-06)·이식 금지 명문. 다음 = Phase 3.1(보완, step 19).
