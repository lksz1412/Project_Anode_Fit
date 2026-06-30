# 비교 (6차): Claude v5.2 merged vs Codex rebuilt_v5 convention_safe_polish

**Date**: 2026-05-29
**대상**:
- Claude: `Claude/docs/graphite_ica_chapter1.tex` (v5.2 merged, ~830 lines)
- Codex: `Codex/results/graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex` (858 lines)
**근거**: 양쪽 전문 정독 (Codex L1-858 완독)
**전제**: 4차 complacency 자책 이후 — 결함은 결함으로, 대칭 평가. 수렴률 % 자제.

---

## §0. TL;DR
Codex v5 = v4 의 **terminology/de-scaffolding polish** (substantive 물리 변화 거의 없음).
- Codex 가 새로 한 것: "DQ"→"GATED"/"Validation gate"/"VG-1·VG-2", "AGP"→"Validation rule",
  in-manuscript 날짜·process 스탬프 제거, **자기 provenance 누출("Codex 산출물…") 제거**,
  grounding-audit 를 "Assumption and validation status" 로 중립화.
- **Codex 가 v5 에서도 \emph{여전히 안 고친} 내가 이미 고친 3건**: (1) A_0 double-counting,
  (2) dangling "M1-M5+ε", (3) D7b(1/L_q 출처) 부재. → \textbf{v5.2 가 물리 정확성·exposition
  에서 계속 앞섬}.
- Codex 가 앞선 것: **manuscript de-scaffolding 2건** (DQ-v3-N 버전 누출 → VG-N; 날짜 스탬프
  제거). 이건 내가 C3/C4 에서 한 provenance 제거와 \emph{같은 방향} — 내 v5.2 에 남은 잔여
  scaffolding 을 드러냄 (정직히 인정).
- 지속 fork: concrete(Claude) vs abstract operator(Codex) Plan A. JCP 2017 출처 = 양쪽 공통 미해결.

---

## §1. 수렴 (동일 core)
physics core·falsification(χ/η_ct co-linearity, N1-N4)·L_q/L_Q·D1b·∂θ_eq·inline AL ledger·
Plan B-core/Plan A-gated/R1-R5 — 동일. (L_q/L_Q·D1b·ledger 는 6차 시점 양쪽 모두 보유: 나는
v5.2 에서 흡수, Codex 는 v4 부터.)

---

## §2. ★ Claude v5.2 가 계속 앞선 점 (Codex v5 도 미수정)

| # | 항목 | 내 v5.2 | Codex v5 | 판정 |
|---|---|---|---|---|
| C1 | **A_0 double-counting** | population 은 ρ_G; A_0 = amplitude 뿐 | **L446 "population weight" 잔존 — 동일 버그** | **Claude 우위 (물리 결함)** |
| C2 | **dangling ε** | ε 전무 (M5 = limiting-case 해석적) | **L774·L792 "M1-M5+ε" 인데 M-list 엔 ε 없음** | **Claude 우위 (내부 모순)** |
| C3 | **D7b (1/L_q 출처: kinematic vs Jacobian)** | 명시 유도 + 두 1/L_q 출처 주석 | **부재** — single_kernel(1/L_q 없음) vs kernel_integral(1/λ) 외견상 불일치 미해소 | **Claude 우위 (exposition)** |
| C4 | **concrete gated Plan A (eq:closed)** | ratio-substitution 실제 적용한 구체식(gated) | abstract operator C_ratio placeholder | **fork** (§4) |

---

## §3. ★ Codex v5 가 앞선 점 (내가 흡수 고려할 de-scaffolding)

| # | Codex v5 강점 | Codex 위치 | 내 v5.2 현재 | 판정 |
|---|---|---|---|---|
| K1 | **"DQ-v3-N" → "VG-N (Validation Gate)"** | L147 VG-2, L332 VG-1, S10 "BOUNDED+GATED" | "DQ-v3-1/2", "BOUNDED+DQ" — \emph{roadmap v3 버전 누출} | **Codex 우위** — 내 provenance 제거와 동일 방향, 잔여 누출 |
| K2 | **in-manuscript 날짜·process 스탬프 제거** | "기준 해석", "smooth-only convention" | "해석 정정 (사용자 2026-05-28)", "(사용자 2026-05-28)" 잔존 | **Codex 우위** — inline-changelog 성격, 제거가 깔끔 |

> K1/K2 는 cosmetic 이나 \emph{내가 시작한 de-scaffolding(C3/C4) 의 미완} 을 드러냄. 흡수 권장.

---

## §4. 지속 fork: Plan A concrete vs abstract
4·5차와 동일. 사용자 deliverable("피팅에 쓸 논리식")엔 concrete(Claude) 부합; Codex 보수성은
내 M1-M5 gating 이 포함 → 내 쪽 superset 유지. 변화 없음.

## §5. 양쪽 공통 미해결: "JCP 2017 paper" (Codex L533)
Codex 가 refs 6/7 출처를 "사용자의 JCP 2017 paper" 로 특정 (v4·v5 동일). 내 v5.2 는 미특정.
사용자 확인 필요 — 맞으면 양쪽 출처 명시, 아니면 Codex 측 제거 대상.

## §6. 권고
1. **v5.2 가 substance 우위 유지** (A_0·ε·D7b). Codex 에 이 3건 수정 권고 (5차와 동일, 미반영됨).
2. **Codex de-scaffolding 2건(K1·K2) 흡수 → v5.3** (선택): DQ-v3-N → VG-N, 날짜 스탬프 중립화.
   내가 이미 한 provenance 제거의 논리적 연장이라 정합적. cosmetic·저위험.
3. concrete Plan A 유지. JCP 2017 사용자 확인.

## §7. 한 줄 결론
6차: Codex v5 = v4 의 polish (DQ→VG, 날짜 제거, 자기 provenance 제거). **substantive 3건
(A_0·ε·D7b) 은 Codex 가 v5 에서도 미수정 → v5.2 가 물리·exposition 우위 유지.** Codex 유일
실익 = de-scaffolding 2건(K1·K2), 이는 내 v5.2 잔여 scaffolding 을 드러내므로 v5.3 으로 흡수
권장. fork(concrete Plan A)·JCP 2017 은 4-6차 불변.
