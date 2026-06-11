# Ch1 v2 — 친절 수식 보강 + 그림 개선 pass (V.U) Plan

## Summary
사용자 5차 피드백 두 건. (1) "조금 더 친절하게 중간중간 수식 추가 보완" — 특히 §1.8, §1.11–1.13.
(2) "설명을 위해 추가된 이미지들이 다소 부족 — 인터넷의 더 나은 이미지로 대체하거나 더 나은 이미지를 생성."
이미지는 **TikZ 개선·신규 생성 채택** (외부 이미지 = 저작권 리스크 + 실계산 좌표 원칙 위배 — Assumptions 참조).

## Current Ground Truth
- HEAD 07ba82b, V.T pass 완료 상태: 42p, 번호식 69개, build_gate 0/0/0, diff True/True, run_example PASS.
- 그림 인벤토리(10): barrier·isofamily·doublewell·kernel·anatomy·fusion·superpose·vdwloop·gapT·chain. 전부 TikZ 실계산.
- 작업 규율 승계: 절별 한큐 루프, Temp python 패치(assert count==1), docs 디렉토리 빌드, 단정형 build_gate.py, 매 단계 커밋+푸쉬, Workflow 금지(Agent 만), FWHM 류 불요 유도 부활 금지.

## Phase Range
U.0 계획서(본 문서) → U.1–U.4 수식 보강(§1.8/§1.11/§1.12/§1.13) → U.5–U.11 그림 개선·신설 → U.R1–U.R10 검수 10회.

## U.1–U.4 수식 친절 보강 (각 절 = [정독→인벤토리→refute→수정→재정독→build_gate→커밋])
- **U.1 §1.8**: (i) 상승부 극한 — 기억 적분에서 dξ_eq/dq 를 현재값으로 꺼내는 단계와 ∫e^{-(q-q')/L}dq' = L(1-e^{-(q-q0)/L})→L 평가를 번호식으로. (ii) 꼬리 극한 — eq:rsol 직전 "동차 몫만 남는다" 한 단계 + 관측항 dξ_j/dq=-dr_j/dq 의 근거(ξ_eq 포화) 번호식. (iii) eq:tail 의 ∝ 를 진폭까지 닫기 — dQ/dV|tail = Q_j(dξ_j/dq)/(dV_n/dq) 연쇄 단계.
- **U.2 §1.11**: 면적 회계 번호식 — 종 ∫=Q_j(1-r_a), 꼬리 ∫=Q_j r_a, 합 Q_j (현 prose 의 "상승부 적분에서 -Q_j r_a 깎임" 전개). kinetic 이동 둘째 몫의 1차 규모식(ΔV_peak ~ L_V) 한 줄.
- **U.3 §1.12**: 융합 임계 전류 닫힌 꼴 — L_V(I,T)=|U_{j+1}-U_j| 를 |I| 에 대해 풀어 |I|_fuse(T) 번호식(저온일수록 낮은 전류에서 융합의 정량판). FWHM 유도는 금지 대상이라 첫째 조건은 정성 유지.
- **U.4 §1.13**: 극값=spinodal 동일성 sF dV_eq/dξ=g''(ξ) 를 미분 단계와 함께 번호식 승격. 분기 중심 대칭 — (V_eq(ξ_s^-)+V_eq(ξ_s^+))/2=U_j (logit 합·(1-2ξ) 합이 0) 번호식. eq:Veq 풀이 한 단계 명시.

## U.5–U.11 그림 개선·신설 (각 그림 = [좌표 python 실계산→TikZ 교체→빌드·시각 확인→커밋])
- **U.5 fig:barrier** → 2패널: (a) 평형 풍경+ΔG_a, (b) 구동 풍경 — 정방향 ΔG_a-χA·역방향 ΔG_a+(1-χ)A·골짜기 차 A 를 화살표로 분해 표기 (§1.4 의 bv 식과 시각 정합).
- **U.6 fig:doublewell** → 준안정(binodal–spinodal)·불안정(spinodal 내부) 띠 음영 + 영역 라벨.
- **U.7 fig:kernel** → 2케이스: L_q≪상승부 폭(추종)·L_q>폭(지연·꼬리) 두 지연 곡선 대비 + 기억 창 음영.
- **U.8 fig:anatomy** → 종 면적 Q_j(1-r_a)·꼬리 면적 Q_j r_a 음영+라벨(면적 회계 U.2 와 시각 정합).
- **U.9 fig:vdwloop** → 방전 과주행 경로(상승 가지→ξ_s^- 낙하)·충전 경로를 굵은 경로+낙하 점선으로, 가역 plateau 수평선 대비.
- **U.10 fig:fusion** → 꼬리가 골을 메우는 영역 음영+주석 화살표.
- **U.11 신규 staging 도식**(서론 stagebox 시각화) — stage 4→3→2L→2→1 의 갤러리 채움 패턴 TikZ (개념 도입 그림).
- isofamily·superpose·gapT·chain 은 양호 판정 — 검수 라운드에서 재평가만.

## U.R1–U.R10 검수 10회
R1–R2 Codex+Fable 전문 통독 병행(신규 수식 재검산·그림-본문 정합) → R3 삼각검증 수정 → R4 독자 시뮬(그림 판독성 중점) → R5 시각 전 페이지 스윕 → R6 수정 → R7 Codex 최종 → R8 수정 → R9 최종 정독 → R10 종합 게이트+RESULT·ledger.

## Non-goals
ch3/ch4 무수정(번호 재매핑은 별도 phase). §1.17 코드 동작 변경 없음(주석·수치 불변 유지). FWHM 유도 부활 금지. 외부 이미지 삽입 안 함.

## Gates
매 단계: build_gate.py 0/0/0 · 그림 단계는 pdftoppm 해당 페이지 시각 확인 · §1.17 접촉 시 diff True/True+run_example PASS · 커밋+푸쉬.

## Test Plan
신규 수식 전수 손 재검산(독립 2원: Codex+Fable) · 신규 그림 좌표는 python 실계산 스크립트를 Temp 에 남기고 캡션과 대조 · 42p 전수 시각.

## Assumptions
- 이미지 트랙은 "대체하거나 생성하거나" 중 **생성** 채택: 회사 배포 문서에 인터넷 이미지는 저작권·출처 표기 리스크가 있고, 본 문서 그림 전부가 모델 실계산 좌표라 외부 그림은 수치 정합이 깨진다. 더 나은 표현은 TikZ 재설계로 달성한다.
- 5차 피드백은 직접 실행 요청("요청한다")으로 읽어 GO 대기 없이 본 계획서 커밋 직후 U.1 부터 무중단 진행한다.

## Decisions Required
없음 (위 두 가정에 이견 시 깃헙 코멘트/다음 메시지로 정정 — 정정 시 Correction History 에 기록 후 재baseline).

## Correction History
(없음)
