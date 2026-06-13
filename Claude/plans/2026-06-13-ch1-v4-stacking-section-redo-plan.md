# Ch1 v4 §1.18 적층 준안정 절 — 확립 방식 재작업 (V4R) Plan

## Summary
사용자 지적: §1.18(적층 준안정)이 우리 확립 방식을 안 지킴 — (1) 계획서 없이 시작, (2) 절 전체를 통째
배치 Write(방법론 §2 위반), (3) 검수 1회뿐(방법론 §3 = N회 가변-청크·연속 2R 0결함 수렴 미달).
본 plan 으로 계획서부터 다시: 단위 구성 루프로 재검토·정합, N회 가변-청크 검수로 수렴까지.
물리 모델 자체는 이미 이중 감사(Codex+Fable) 통과·게이트 PASS 이므로 blank 재작성이 아니라 **단위별
재정독·재유도·정합 + 정식 N회 검수**로 품질 격자를 다시 거른다.

## Current Ground Truth
- HEAD 88c1b56. `graphite_ica_ch1_Opus_v4.tex` 50p, §1.18 = sec:stacking(문서 끝, 코드 절 뒤).
- 식 1.98–1.103(gcoupled·sigmaeq·xistack·dxistack·dvstack·gapsplit), 그림 fig:stackloop, 참고문헌 6편.
- 게이트: build_gate Opus_v4 0/0/0 50p · comment_gate Opus_v4 15/15 · v3 하위호환 0/0/0 48p.
- §1.1–§1.17 = v3 바이트 동일(diff 확정). v3 동결.

## 이미 식별된 실질 누락 (재작업에서 처리)
- ★ 신규 기호 σ·B_j·κ_j·ξ_{c,j}·ξ_open·ξ_close·Δξ_stack·ΔV_stack 가 §1.1 기호표에 부재(G-usable).
  → §1.1 표 "충방전 확장" 블록에 추가(표는 식 번호 무이동 — 안전).
- fig:stackloop 가 ±1 평탄 가지(이상화)를 그림 — 준안정 가지 곡률 생략을 캡션이 명시하는지 점검.
- eq:gapsplit 의 적층 몫이 peak 중심에 적용되는지(창 [ξ_open,ξ_close] 와 peak 중심 정합) 점검.

## Phase Range
V4R.0 본 plan → V4R.1 단위 구성 루프(8 단위 재정독·정합·기호표 보강) → V4R.R1–R10 N회 가변-청크
검수(수렴까지) → V4R.종합 게이트·RESULT·ledger.

## V4R.1 단위 구성 루프 (자연 단위 하나씩 — 통째 배치 금지)
각 단위: [정독→재유도/정합 확인→(수정 시)빌드→ledger 사유; 무수정도 정독 근거 기록].
- U1 도입 문단: §1.13(eq:hysdU·γ_j) 받기, 인용 6편 motivation 정합.
- U2 §1.18.1 σ 정의 + eq:gcoupled: 우물·결합 차원·물리. ★기호표 보강 동반.
- U3 §1.18.2 eq:sigmaeq + saddle-node(σ=±1/√3, h=±2/3√3) + eq:xistack + eq:dxistack: 전 대수 재유도.
- U4 fig:stackloop: 좌표·방향(ξ=탈리 진행률; 충전=ξ↓)·캡션 정합, ±1 이상화 명시.
- U5 §1.18.3 eq:dvstack + B→0 회수: 2κ/sF 유도, 폭 Δξ→0 회수(자가정정분) 재확인.
- U6 §1.18.4 eq:gapsplit + 반증: configurational(T_c−T)^{3/2} vs athermal 바닥, 구조 지문 인용.
- U7 keybox: 가설 3중 표시·γ_j 흡수 관계.
- U8 참고문헌 6편 서지·§1.16 포인터 호응.

## V4R.R1–R10 N회 가변-청크 검수 (확립 체계)
매 라운드 청크 스킴·렌즈 전환, Codex+Fable 병행, refute+가장약한1곳+빈통과금지, 삼각검증→master 수정→커밋.
- R1 식별 청크(식 하나=단위): 전 대수 적대 재계산(Codex) + G-follow/G-usable(Fable).
- R2 절 구조·종단 서사: §1.13/§1.16 다리·기호 생애·전방참조.
- R3 삼각검증 수정.
- R4 문장 단위 prose: 구어체·전보체·티배깅 0·한글+영어 규율.
- R5 시각 고해상 전수: 절 페이지(p.47–49) + 그림 확대 렌더.
- R6 완전성·인용-사실: 6편이 실제로 말한 것 vs 본문(fresh 재대조).
- R7 물리 극한 전수: T→0/∞·B→0/∞·κ→0/∞·σ→±1·ξ→0/1·ξ_c 이동 — 비물리 사냥.
- R8 수정.
- R9 fresh 수렴: 직전 수정의 새 결함 0 확인.
- R10 종합 게이트 + 기록. (수렴=연속 2R 0결함이면 조기 종료 가능.)

## Gates
매 단위·라운드: build_gate Opus_v4 0/0/0 · comment_gate Opus_v4 15/15 · 그림 변경 시 렌더 검증 ·
커밋+푸쉬. §1.1 표 보강은 식 번호 무이동 확인. v3·코드 .py 무손상.

## Non-goals
물리 모델의 새 주장 추가 금지(재검토·정합·검수만). §1.1–§1.17 본문 무수정(기호표 행 추가만 예외 —
식 번호 불변). v3 동결.

## Assumptions
"제대로 다시 ... 작업해" = GO 무중단. Workflow 금지(문서 작업 — Agent 도구만). 코드 동작·수치 불변.

## Correction History
(수정 1 — 본 plan 의 존재 이유) 직전 V4.1/V4.R 는 계획서 없이 통째 배치 Write + 검수 1회로 진행 —
방법론 §2·§3 위반. 본 plan 이 그 baseline 을 단위 구성 루프 + N회 검수로 재수립한다. 직전 V4.R 의
유효 수정(B→0 자가정정·Ω_eff 제거·차원 1:1·schmitt2022 활용)은 보존하고 그 위에서 재검수한다.
