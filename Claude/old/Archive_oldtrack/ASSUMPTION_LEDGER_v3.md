# Assumption Ledger v3 — Graphite Anode ICA Tail Theory

**Date**: 2026-05-28
**Binding**: `Claude/plans/MASTER_ROADMAP_v3.md` §2 (Assumption Grounding Protocol)
**역할**: Chapter 1 의 모든 assumption 의 grounding·상태·유효범위 authoritative 대장.
본문(chapter1.tex)의 모든 assumption 은 본 ledger 의 AL-# 를 인용한다.

**상태 tier (AGP-2)**: **GROUNDED** (직접 문헌/이론 근거, established 사용 가능) ·
**BOUNDED** (근거 있으나 유효범위 제한, 범위 명시 후 사용) · **FLAGGED** (직접 근거
부재 — hypothesis/ansatz/novel, established 로 사용 금지).

---

## 핵심 grounding 결과 2건 (가장 중요)

1. **Equilibrium isotherm 의 함수 형태**: lattice-gas / regular-solution chemical
   potential `μ(ξ)` 는 GROUNDED (McKinnon-Haering 1983; Bazant 2013). 반면
   **erf/Gaussian-cumulative isotherm 의 thermodynamic derivation 은 graphite
   intercalation 에 대해 문헌에 존재하지 않음** → FLAGGED ansatz 로만. 사용자 정정
   (2026-05-28): "가우시안"은 형태 확정이 아니라 sharp peak 예시 → erf 는 재현 목표 아님.
2. **ICA peak tail 의 kinetic 온도 의존 모델**: 선행 출판 모델 부재 → 본 chapter 의
   **novel contribution**. 가정이 아니라 grounded 조각(S1-S10)에서 유도해야 하며,
   경쟁 tail source 를 falsify 해야 성립.

---

## Ledger

| # | Assumption (English term 중심) | 물리적 의미 | Grounding (문헌/이론, DOI) | 상태 | 유효범위·주의 |
|---|---|---|---|---|---|
| **AL-1** | Activation free energy `ΔG_a(T)=ΔH_a−TΔS_a`; Eyring/transition-state-theory rate `k=(k_B T/h)·κ·exp(−ΔG^‡/RT)` | activation barrier 를 통과하는 thermally activated transition | Eyring 1935 (10.1063/1.1749604); Evans-Polanyi 1935 (10.1039/TF9353100875) | **GROUNDED** | prefactor 는 `k_B T/h` (Eyring) — arbitrary attempt frequency ν 아님. ν=κ·k_BT/h 로 해석 |
| **AL-2** | Effective barrier `ΔG_eff = ΔG_a − χ·F·(V−U)` (potential lowers barrier linearly) | electrode potential 이 activation barrier 를 선형으로 lowering | Butler-Volmer (Bard & Faulkner Ch.3); BEP Evans-Polanyi 1938 (10.1039/TF9383400011); Marcus 1956 (10.1063/1.1742723) | **BOUNDED** | 선형 lowering = leading-order (small driving force). 큰 \|V−U\| 에서 Marcus curvature/inverted region 으로 깨짐. "Marcus 가 선형을 전역 정당화"라 주장 금지 |
| **AL-3a** | Equilibrium isotherm = lattice-gas / regular-solution `μ(ξ)`; ideal limit → logistic `ξ_eq=1/(1+exp(−(V−U)/w))`. **smooth, 0→1 step jump 아님** | 균질 site occupancy 의 statistical thermodynamics | McKinnon-Haering 1983 (Modern Aspects of Electrochemistry 15); Bazant 2013 (10.1021/ar300145c) | **GROUNDED** | width `w=RT/F` (ideal) 또는 interaction 보정 (regular solution). ★ 본 chapter 의 equilibrium baseline |
| **AL-3b** | erf/Gaussian-cumulative isotherm (heterogeneous site-potential disorder) | transition center potential 의 불균질 분포 (broadening 의 한 option) | Bässler Gaussian Disorder Model 1993 (organic semiconductor, 10.1002/pssb.2221750102) **analogy**; 경험적 dQ/dV Gaussian peak-fit (Dubarry) | **FLAGGED ansatz** | graphite intercalation 직접 thermodynamic 근거 **부재**. 사용자 "가우시안"=sharp peak 예시일 뿐 → 목표 아닌 option. "ansatz" 로만 |
| **AL-4** | Graphite staging (Stage 4 / 3 / 2L / 2 / 1; LiC₆, LiC₁₂) → distinct dQ/dV peaks | phase transition 의 voltage signature | Dahn 1991 (10.1103/PhysRevB.44.9170); Ohzuku 1993 (10.1149/1.2220849); review Asenbauer 2020 | **GROUNDED** | 2L = liquid-like stage-2 (별도 stage 번호 아님). 인접 stage 가 σ 이내면 observable peak 로 fusion (N_p≈3~4) |
| **AL-5** | First-order linear relaxation `dξ/dt = k(ξ_eq − ξ)` | non-equilibrium 진행률이 equilibrium 으로 완화 | De Donder 1936; De Groot-Mazur 1962 Ch.X; Onsager 1931; Eigen-De Maeyer 1963 | **BOUNDED** | 임의 rate law 의 equilibrium 근처 1st-order Taylor 선형화. 평형서 멀면 무효; k=k(ξ_eq,T) 일반적으로 시간의존 |
| **AL-6** | Activation-energy distribution `ρ(g)` → dispersive / stretched (KWW) kinetics | barrier 의 ensemble 분산 → 비지수 완화 | Kohlrausch 1854; Williams-Watts 1970; Plonka *Dispersive Kinetics* 2001 | **BOUNDED (optional)** | stretched→분포 inverse mapping **non-unique** (retrapping 도 재현). 옵션 항. 남용 금지 |
| **AL-7** | Ratio-substitution / propagator method (self-consistent integral equation closure) | Refs 6/7 (사용자 PhD) — Fredholm 2nd-kind 적분방정식 폐형화 | Lee, Son, Sung, Chong 2011 (10.1063/1.3565476); Son et al. 2013 (10.1063/1.4802584, "method for solving Fredholm integral equations of the second kind") | **GROUNDED (기법) + DQ (적용성)** | Refs 는 **Fredholm** (steady-state). 본 time-integration 은 **Volterra** (upper limit t). 적용성은 Phase 10 에서 검증 (DQ-v3-2) |
| **AL-8** | ICA peak tail 의 kinetic 온도 의존 (low T → small k → large lag → long tail) | tail = ξ 가 ξ_eq 를 못 따라가는 relaxation lag | **선행 출판 모델 부재** (리서치 확인) | **FLAGGED novel** | S1-S10 에서 유도 (가정 금지). 경쟁 source (AL-10 의 R_n 등) falsify 필수 |
| **AL-9** | Implicit electrode potential via charge/site balance `Q_cell·q = Q_bg(V,T)+ΣQ_{j,tot}ξ_j` | V_n 은 외부 lookup 이 아니라 charge/site balance 로 결정 | Doyle-Fuller-Newman 1993 (10.1149/1.2221597); Newman & Thomas-Alyea *Electrochemical Systems* 3rd | **GROUNDED** | SPM/lattice-gas μ(ξ) limit 에서 external OCV lookup 과 등가. unique root: `∂Q_bg/∂V_n ≥ ε>0` |
| **AL-10** | ICA/DVA diagnostic; rate/T broadening; competing polarization sources `R_n` | dQ/dV 는 진단 도구; rate↑ broadening; tail 은 분극·transport 도 기여 가능 | Dubarry-Anseán 2022 (10.3389/fenrg.2022.1023555); Fly-Chen 2020 (10.1016/j.est.2020.101329) | **GROUNDED** | C/6 최적 rate. tail 의 barrier 귀속 전에 R_n·transport·width 배제(falsify) 필요 |

---

## 본문 사용 규칙 (AGP 재확인)

- **FLAGGED (AL-3b, AL-8, AL-7 적용성)** 는 본문에서 "established" 로 쓰지 않는다.
  AL-3b 는 "ansatz", AL-8 은 "본 chapter 의 novel 유도", AL-7 적용성은 "검증 대상"으로
  명시.
- **BOUNDED (AL-2, AL-5, AL-6)** 는 유효범위를 항상 병기 (예: AL-2 → "near-equilibrium
  linear; Marcus curvature bounds it").
- **step-function / 0→1 급점프 / max·min·Heaviside·hard-switch 금지** (사용자 2026-05-28
  명시; AGP-3, Dim #11). 모든 transition 은 smooth.

---

## Correction History

| 일자 | 변경 |
|---|---|
| 2026-05-28 | 초판. 문헌 grounding 리서치 결과 통합. AL-1~10 + 상태/유효범위. 사용자 정정 2건 반영: (1) "가우시안"=sharp peak 예시(형태 확정 아님), (2) activation barrier 유지·step jump 가 금지 대상. |
