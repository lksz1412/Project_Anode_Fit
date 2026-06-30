# Review Ledger: graphite_ica_chapter2.tex — 10-round 재검 (재진행판)

**Date**: 2026-05-29 (재진행)
**대상**: `Claude/docs/graphite_ica_chapter2.tex` (Chapter 2, ~432 lines, 수정 후)
**계획서**: `Claude/plans/MASTER_ROADMAP_CH2_v1.md` (T1–T8 spine, AL-10 승계 + AL-11~16)
**맥락**: 직전 세션(모델 4.8 업데이트로 중단)에서 CH2 10회 재검수가 끊김. 사용자 지시 = "챕터2 기준
10회 재검수를 진행하던중 끊겼으면 그걸 재진행. 이전 세션작업방식 확인해서 벤치마킹." → 재진행.

## ★ Supersession 고지
본 렛저는 이전 `REVIEW_LEDGER_CH2_10ROUND.md` (백업: `..._priorpass_superseded.md`) 를 **대체**한다.
이전 렛저는 "10-round ACCEPT, 잔여 결함 0" 으로 마감됐으나, **재진행 결과 핵심 결함(factor-of-2 의
spectrum 부당 일반화) 을 놓친 부정확한 sign-off** 였음이 확인됐다. 독립 적대 agent 3개(R1·R3·R5)와
자체 재유도가 동일 CRITICAL 에 수렴. 이전 ACCEPT 는 무효, 본 재진행판이 권위 기록.

## 벤치마킹한 이전 세션 방식 (CH1 v5.3 / CH2 prior 렛저 공통)
독립 적대(adversarial) sub-agent 다중 렌즈(전수 정독, 결함만 보고·칭찬 금지) + 자체 재유도 + grounding
DOI web 검증. 라운드: R1 물리·차원 / R2 LaTeX / R3 P1·smooth·Ch1 notation / R4 grounding·DOI /
R5 내부정합·논리·Ch1 link → R6 수정 → R7 검증 → R8–10 최종 sign-off. (글로벌 메모리
`feedback_phase_audit_workflow` 의 10차원×3-Pass 와 정합: Pass1 발견=R1–5, Pass2 수정=R6, Pass3 재검증=R7–10.)

---

## Phase 0: grounding DOI web 재검증 (6/6 정확)
| cite | DOI | 검증 |
|---|---|---|
| bernardi1985 | 10.1149/1.2113792 | 확인 (J. Electrochem. Soc. 132(1), 5, 1985) |
| reynier2003 | 10.1016/S0378-7753(03)00285-4 | 확인 (J. Power Sources 119–121, 850, 2003) |
| thomasnewman2003 | 10.1016/S0378-7753(03)00283-0 | 확인 (J. Power Sources 119–121, 844, 2003) |
| eyring1935 | 10.1063/1.1749604 | 확인 (J. Chem. Phys. 3(2), 107, 1935) |
| bazant2013 | 10.1021/ar300145c | 확인 (Acc. Chem. Res. 46, 1144, 2013) |
| onsager1931 | 10.1103/PhysRev.37.405 | 확인 (Phys. Rev. 37, 405, 1931) |

DOI/서지 결함 0건 (전부 web 실측 일치).

## 10 라운드 기록
| R | 렌즈 / 작업 | 방법 | 결과 |
|---|---|---|---|
| 1 | 물리·차원 정합 | adversarial + 자체 재유도 | 차원(전 정의식)·σ=g''kr²/T·부호상쇄·Ch1 정합 SOUND. **★CRITICAL 발견: factor-of-2 spectrum 일반화 부당**. **HIGH: small-r 유도 vs large-r 응용 모순**. MEDIUM 2(A_L^(2) 가중, q_rev 부호귀속). |
| 2 | LaTeX 무결성 | adversarial | **컴파일 clean**. ref/cite/label resolve, 중복 0, 환경 balance, longtable 컬럼 일치. LOW(미사용 매크로 \bg/\cell/\ext), INFO(dead label). 차단 결함 0. |
| 3 | P1·smooth·Ch1 notation | adversarial (Ch1 대조) | P1/smooth 위반 0, 한글+영어용어 OK, reaction↔activation entropy 구분 exemplary. **CRITICAL(2배 감쇠) 독립 재확인**, **HIGH(signed I 부호규약 미연결)**, MEDIUM(ΔG_rxn vs 𝒜), LOW(η_conc↔η_tr). |
| 4 | grounding·citations·DOI | adversarial + web | DOI 6/6 정확. **MEDIUM: AL-10 dangling(Ledger 미등재)**, MEDIUM(bazant 과잉귀속), LOW(self-check "11–15"→"11–16" 오기, partial-current 무태그). |
| 5 | 내부정합·논리·Ch1 link | adversarial (Ch1 대조) | cross-section 일관, Ch1 link 정확. **CRITICAL(2배 감쇠) 3번째 독립 수렴**, **HIGH(kernel 1/L_q 비대칭, TN2 검증불가)**, MEDIUM(§intro 절명칭, TN1–4=N1–4 1:1 과대), Θ_tail vs θ 혼동. |
| 6 | 수정 적용 (Pass 2) | Edit ×17 | 아래 "수정 요약" 17건 반영. |
| 7 | 수정 검증 + 회귀 | 자체 read/grep | `Iη` 부호 잔재 0; `2배 감쇠` 잔존 2건 모두 부정·한정 문맥; 수정 구간 전수 재독 정합. |
| 8–10 | 최종 종합 sign-off | adversarial (전수 재독) | **ACCEPT**. 6 수정군 정확·완전, 부호 회귀 0, per-mode 2배 제한의 spectrum 정정 수학적으로 옳음, LaTeX 무결(boundbox 3·AL-10 행·표 컬럼·ref/cite resolve), 신규/미해소 결함 0. |

## 발견·수정 요약 (Pass 2, 전부 반영)
**CRITICAL (4중 수렴: R1·R3·R5 + 자체재유도)**
1. "비가역열 tail 2배 빠른 감쇠(L_q/2)"의 spectrum 부당 일반화 → per-mode 한정 강등 + "spectrum 일반화
   한계" boundbox 신설(단일 mode 극한에서만 균일 2배; stretched spectrum 은 arc-length doubling+재가중) +
   A_L^(2)=재가중(동일 복제 아님) 명시 + kinematic 1/L_q 비대칭 명시. (abstract, T8, E6, cross-check 표, summary E6) ✅

**HIGH**
2. small-r 유도 vs large-r 응용 모순 → 저온 narrative 를 near-eq bound 내 "상대적 잔여 lag"로 정정 + 고차보정 범위외 명시. ✅
3. TN2 검증불가/self-defeating → "Ch1 spectrum 으로부터의 forward prediction 정합"으로 재정식화; "정확히 2배"는 단일 mode 극한 한정. ✅
4. signed I 부호규약 → q_irr=|I|η 전면 통일 (notation/T4/eq:qirr/total_heat/summary E4/AL-12); q_rev 는 signed I 유지(부호가변, 정확). 부호 convention(I>0=충전, q_rev>0=흡열) 명시. ✅

**MEDIUM**
5. AL-10 dangling → Ledger 표에 AL-10 METHOD 행 신설. ✅
6. bazant2013 과잉귀속 완화(표준 통계열역학 + 활용 예). ✅
7. §intro Ch1 절명칭 "★ Falsification"으로 정정. ✅
8. "TN1–4 = N1–4 열적 1:1 대응" 철회 → 부분 대응으로 정정. ✅
9. ΔG_rxn ≠ 𝒜_j 별개 양 명시(오독 방지). ✅
10. partial-current 합산 AL-12 태그. ✅

**LOW**
11. self-check AL 범위 "11–15"→"11–16(+승계 AL-10)" 오기 정정. ✅
12. η_conc=Ch1 η_tr, η_kin=Ch1 η_ct 명명 bridge(notation 표). ✅
13. AL-15 문구 H1 정합(잔여 lag, 균일 2배는 단일 mode 한정). ✅

(미수정 cosmetic: 미사용 매크로 \bg/\cell/\ext = Ch1 승계 잔재로 보존; dead label = 무해; tabularx 미사용 = 무해.)

## 최종 상태
**Chapter 2 = 10-round 재진행 재검 ACCEPT (잔여 결함 0).** 물리 SOUND (per-mode 2배 결과는 유지,
spectrum 일반화 overclaim 은 BOUNDED 로 정정 — novel content 보존하며 correctness 강화) · LaTeX 컴파일
clean · P1/smooth/grounding 준수 · Ch1 notation 정합 · 6 DOI web 검증 · reaction vs activation entropy
엄격 구분 · signed/|I| 부호 일관.

## 후속 (Chapter 3 후보, Ch2 §summary 전달)
staging-resolved ∂U/∂x 정량 모델; ICA tail + 비가역열 tail 동시 fitting (cross-modal identifiability);
충방전 hysteresis 의 heat/entropy 비대칭; full-cell 열 balance. "JCP 2017" Ch1 출처 미해결은 별건.

## 미커밋 상태 경고
본 CH2 산출물·렛저·로드맵 + CH1 v5.3 변경분은 git untracked/modified (미커밋). 또 한 번의 세션 중단 시
손실 위험 → 사용자 검토 후 커밋 권장.
