# v1.0.10--v1.0.25.2 Scientific and Implementation Lineage Review

## Executive judgment

이 계보는 전부 폐기할 대상도, v1.0.25.2를 그대로 승인할 상태도 아니다.
보존할 수 있는 중심축은 다음과 같다.

1. v1.0.13의 reaction-direction/configurational convention 교정
2. v1.0.19의 implicit charge balance와 fixed-state/fixed-charge derivative
3. v1.0.22의 common-potential equilibrium blend architecture
4. v1.0.25의 area-preserving empirical skew profile
5. v1.0.25.2에 남아 있는 stored-8dp direct blend14 fit

반대로 causal-memory 경계, observed width의 thermodynamic 해석, finite-rate
host 합성, heat/hysteresis sign closure, mutable default, 신규 default test,
fit provenance에는 미해결 문제가 남아 있다.

가장 중요한 v1.0.25.2 판정은 다음 두 문장을 동시에 유지하는 것이다.

- **실제 direct14 data fit은 성립한다.**
- **그 fit configuration은 shipped default 7+7 경로가 아니다.**

따라서 v1.0.25.2는 현재 `release truth`가 아니라
`physics-conformance candidate`로 동결하는 것이 타당하다.

## Scope and method

Scientific source exclusion:

- `Claude/docs/v1.0.26A-regsol`
- `Claude/docs/v1.0.26B-gallery`

`Claude/results/comp_v26_data`라는 directory name은 과학적 권위를 주지
않는다. v1.0.25.2 handover가 직접 채택한 fit의 계산 provenance와 artifact만
읽었다.

Review method:

- current v1.0.25.2의 56 recursive TeX sources, release code, guides, gates,
  handovers와 adopted fit path를 전문 검독
- v1.0.10--v1.0.25.2의 version-local authoritative plan, execution result,
  ledger, handover와 central code changes를 version별 대조
- 전체 1,386-file inventory와 duplicate-content map으로 누락·중복 확인
- 인접 버전 byte diff를 locator로 사용
- 현재 source에 대한 독립 수치 probe와 fit reconstruction
- 이전 5.5 계열 audit의 PASS, defect count와 scientific conclusion은 미승계

Coverage limitation:

모든 authoritative plan/handover/ledger와 current release source는
직접 판독했다. 수백 개 competition worker draft와 중복 review 초안은 전체
경로를 inventory하고 중앙 union/result 및 byte duplicate를 추적했지만,
서로 중복된 모든 draft를 문장별로 다시 판정한 것은 아니다. 따라서 이
문서는 “저장소의 모든 파일을 line-by-line 읽었다”고 주장하지 않는다.

## Byte-level lineage index

아래 수치는 scientific change count가 아니다. versioned filename rename도
add/remove로 잡히며, unchanged file도 물리적으로 옳다는 뜻이 아니다.
원자료는 `PHASE_044_LINEAGE_DIFF.json`이다.
보존 중인 dirty
`Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html` 하나만 exact path로
제외했다. 다른 버전의 동명 HTML은 포함되므로 v1.0.24.1 전후
add/remove에는 이 의도적 공백이 반영된다.

| Version | Text files | Added | Removed | Changed | Unchanged |
|---|---:|---:|---:|---:|---:|
| 1.0.10 | 12 | — | — | — | — |
| 1.0.11 | 8 | 4 | 8 | 0 | 4 |
| 1.0.12 | 8 | 4 | 4 | 1 | 3 |
| 1.0.13 | 10 | 6 | 4 | 4 | 0 |
| 1.0.14 | 12 | 8 | 6 | 4 | 0 |
| 1.0.15 | 12 | 7 | 7 | 4 | 1 |
| 1.0.16 | 11 | 6 | 7 | 4 | 1 |
| 1.0.17 | 11 | 6 | 6 | 4 | 1 |
| 1.0.18.1 | 11 | 6 | 6 | 4 | 1 |
| 1.0.18.2 | 12 | 7 | 6 | 5 | 0 |
| 1.0.19 | 49 | 47 | 10 | 2 | 0 |
| 1.0.20 | 195 | 154 | 8 | 28 | 13 |
| 1.0.21 | 63 | 21 | 153 | 19 | 23 |
| 1.0.22 | 200 | 159 | 22 | 36 | 5 |
| 1.0.23 | 78 | 24 | 146 | 3 | 51 |
| 1.0.24 | 124 | 69 | 23 | 42 | 13 |
| 1.0.24.1 | 124 | 1 | 1 | 0 | 123 |
| 1.0.25 | 137 | 13 | 0 | 21 | 103 |
| 1.0.25.1 | 138 | 1 | 0 | 7 | 130 |
| 1.0.25.2 | 140 | 2 | 0 | 11 | 127 |

## Version-by-version scientific judgment

| Version | Actual advance | Independent limitation | Disposition |
|---|---|---|---|
| 1.0.10 | graphite/LCO/heat baseline; logistic area and direction skeleton | LCO/tail closures are placeholders | keep historical skeleton only |
| 1.0.11 | release core is effectively v1.0.10 | incomplete copy; no independent scientific step | do not use as authority |
| 1.0.12 | manuscript/math corrections | numerical core remains v1.0.10 | keep edits after revalidation |
| 1.0.13 | electrode-aware direction; configurational \(R/F\to nR/F\); width-only config handling; scalar behavior | later \(T\), fit and ensemble claims still absent | first reliable implementation correction spine |
| 1.0.14 | Hill/phase-separation and manuscript rigor | active numerical logic is essentially v1.0.13 | theory/reference, not new solver release |
| 1.0.15 | voltage-domain sequential memory | output depends on observation window, array/scalar call and sampling; finite-window recurrence is not pointwise/window-independent | replace memory API; do not preserve strong claim |
| 1.0.16 | keyed \(n(T)\) derivative | no-key width derivative is inconsistent; observed empirical width is overused as reversible-entropy input | preserve keyed math only inside declared assumptions |
| 1.0.17 | documentation progression | code is byte-identical to v1.0.18.1 and near prior numerical spine | documentation release only |
| 1.0.18.1 | documentation progression | no distinct code step | documentation release only |
| 1.0.18.2 | optional Einstein heat-capacity correction | default datasets do not exercise it | keep as opt-in material closure |
| 1.0.19 | implicit charge-balance \(U_{\rm oc}\), entropy coefficient and normalized-state entry points | normalized state is transition progress, not automatically crystallographic composition; synthetic self-fit is not validation | strongest common-core baseline |
| 1.0.20 | documentation expansion | function bodies remain v1.0.19 | fold into corrected manuscript, not code lineage |
| 1.0.21 | documentation/TST expansion | partition-ratio entropy statement overgeneralizes when the ratio is \(T\)-dependent; code remains v1.0.19 | salvage bounded derivations only |
| 1.0.22 | common-potential host equilibrium blend and capacity accounting | additive finite-rate host response is first-order only; Si data are tier-C; mass/capacity normalization and handover status conflict | keep equilibrium architecture; gate finite-rate path |
| 1.0.23 | optional Fredholm/transfer-function lag ratio with default off | synthetic/Picard/transfer gates only; no real-data physical validation or compute saving | keep as optional analytical diagnostic |
| 1.0.24 | data registry, XRD/gallery seeds, LCO toggle, equilibrium-only regular-solution experiment | planned GITT/rate/temperature matrix was unavailable; initial fit did not exercise regsol and was later corrected; \(\Omega\) is imposed/nonidentified on single-\(T\) pOCV | keep data/provenance lessons and theory layer; discard old regsol production path |
| 1.0.24.1 | notation/layout/code-appendix cleanup | code byte-identical to v1.0.24; no new physics/fit | editorial snapshot, not a model release |
| 1.0.25 | empirical skew \(\alpha\), finite 5\(L\) pad, regsol removal, optional Si7 | \(\alpha\) is strongly degenerate and empirical; 5\(L\) is not \(-\infty\); mutable global switch; contemporary fit provenance incomplete | keep skew kernel and honesty corrections; rewrite defaults/memory claims |
| 1.0.25.1 | four interpretation touch-ups, including weaker \(n=1\)/multi-cell claims | code byte-identical to v1.0.25; no new fit | authoritative editorial correction to v1.0.25 |
| 1.0.25.2 | stored direct blend14 fit, 7+7 standalone profiles, explicit theory/fit split, closed two-phase reference expression | no standalone plan/change ledger; direct14 is not shipped default; fitted background constants unused; tests force legacy or omit new defaults; optimizer precision lost; broadened-threshold derivative claim is false | conformance candidate only; preserve fit artifact and corrected theory pieces |

## Cross-version technical findings

### 1. Fit validity and model identity

For the archived blend-labeled curve whose experimental protocol remains
unknown, the surviving stored-8dp direct14 vector reconstructs:

\[
R^2=0.99964941790404,\qquad
\mathrm{BIC}=-4760.653827485789.
\]

The BIC is a builder working-likelihood statistic on smoothed, correlated
residuals and is used only for comparison inside the same preprocessing and
objective.

The frozen \(s=+1\) release path agrees numerically with an independent direct
formula to \(1.4211\times10^{-14}\) mAh/V maximum absolute difference on that
grid.

The shipped default path instead combines standalone graphite7 and Si7
profiles. On the same processed blend data, fitting only \(f_{\mathrm{Si}}\)
and nonnegative observation baseline \(B_{\mathrm{obs}}\) gives:

\[
f_{\mathrm{Si}}=0.58122565,\quad
B_{\mathrm{obs}}\simeq0,\quad
R^2=-1.61321666.
\]

This proves a wiring/documentation mismatch, not that the physical blend model
class is impossible. The two paths were trained under different objectives,
protocols, grids and normalization.

### 2. Fit provenance is incomplete

The builder computed prediction and metrics from its selected `best` vector,
then stored the vector at eight decimals and omitted the original prediction.
It did not require `r.success` or save termination, Jacobian or evaluation
count. The six-decimal transition JSON loses more precision. The original
optimizer state cannot be exactly reconstructed, and convergence/global
optimality are not established by the surviving artifact.

### 3. Current default tests do not establish current default behavior

The v1.0.24 gate switches immediately to legacy four-transition defaults.
The v1.0.25 gate covers skew compatibility, area and smoothness but does not
construct the new shipped 7+7/background path. Passing gates are valid for
their tested invariants, not evidence that the v1.0.25.2 default reproduces the
accepted fit.

### 4. Time-unit error is an intercept convention, not generally an enthalpy shift

The code supplies C-rate in h\(^{-1}\) to an Eyring expression using SI
\(h/k_B\). The factor 3600 is \(T\)-independent. At fixed activation enthalpy:

\[
\Delta S_a^{\rm phys}-\Delta S_a^{\rm legacy}
=-R\ln3600
\simeq-68.081\ {\rm J\,mol^{-1}\,K^{-1}}.
\]

\(RT\ln3600=20.298\) kJ/mol is only a 298.15 K apparent enthalpy offset if
entropy is artificially held fixed; it is not a multi-temperature enthalpy
correction.

### 5. Broadened regular-solution threshold derivative is finite

For the documented two-phase measure, the gap mass
\(m=O(\sqrt{\Omega/RT-2})\) added at \(U^\circ\) cancels the same leading mass
removed from the central stable-branch integral. Numerical quadrature of the
documented equation gives

\[
\max|P_{2+\epsilon}-P_2|/\epsilon\to5.89913\ {\rm V^{-1}},
\qquad
\max|P_{2+\epsilon}-P_2|/\sqrt{\epsilon}\to0.
\]

The area-preserving expression and continuity can be retained. The claim that
the broadened curve's \(\Omega\)-derivative diverges must be removed.

### 6. Causal and trajectory contracts remain incomplete

- finite 5\(L\) prehistory leaves \(e^{-5}=0.0067379\) residual
- duplicate initial voltage can produce zero pad points
- voltage sorting discards acquisition history on reversal/nonmonotonic input
- mean temperature controls selected lag/branch terms while other terms use
  pointwise temperature
- nonfinite lag silently falls back to equilibrium

### 7. Thermodynamic interpretation is ahead of identification

- \(z_j\) must come from reaction stoichiometry, not \(RT/(Fw_j)\)
- empirical \(\alpha\) and \(w\) do not identify phase, host, reaction electron
  count, activation enthalpy or reversible heat
- accepted blend14의 stored-8dp width 하나는 수치상 upper bound와 같고
  sub-grid width는 없다. standalone graphite7에는 sub-grid width가 있고,
  standalone Si7의 stored-8dp alpha 값은 수치상 양 bound와 같다. 원
  optimizer active-set 상태는 유실되어 실제 bound hit 여부는 알 수 없다.
- `sigr.csv` experimental protocol remains unknown

## Recommended authority and product split

### A. Physics manuscript

The body contains only state definitions, assumptions, conservation,
derivations, validity domains, limits and falsification criteria.

Code symbols are permitted only in the designated implementation appendix.
File paths, commits, test outputs and work history remain in the external
conformance ledger.

### B. Empirical curve product

`EmpiricalSkew14Profile` owns:

- exact observation/preprocessing contract
- surviving stored-8dp vector and hashes
- background and metric definition
- empirical-only evidence grade

It owns no host/phase/heat/kinetic interpretation.

### C. Physical host-blend product

`PhysicalHostBlend` owns:

- common internal potential
- graphite/Si capacity allocation and normalization basis
- explicit background contract
- separately calibrated host/material closures
- bounded finite-rate approximation or time-ordered trajectory solver

It must not silently advertise the direct14 in-sample fit as its validation.

### D. Compatibility product

Legacy four-transition and hour-based rate behavior remain available only as
an immutable, named compatibility profile. A process-global toggle must not
change future object behavior.

## Repair order

1. Freeze v1.0.25.2 as a conformance candidate; keep v1.0.26 outside the
   scientific lineage.
2. Flatten append-only U1--U10 and stale handover statements into one authority
   ledger with explicit supersession.
3. Preserve the surviving direct14 profile and record the lost optimizer
   precision as an unrecoverable provenance gap.
4. Correct manuscript blockers before adapting code: state orientation,
   electron stoichiometry, reversible heat sign/basis, small-tail coefficient,
   network \(Q/(zF)\), threshold regularity and thermal-tail derivation.
5. Split empirical, physical-host and legacy-compatible constructors.
6. Wire background and profile parameters explicitly; remove mutable global
   defaults and unconditional/irrelevant material-case behavior.
7. Add new-default tests without a legacy toggle: preset count/alpha,
   background consumption, direct-profile curve hash, explicit-argument
   priority, invalid case, state leakage, temperature/rate units, monotonic
   validation and trajectory order.
8. Validate physical transfer claims with common-protocol graphite/Si/blend,
   multi-cell, multi-temperature/rate and holdout data.

## Final lineage disposition

- **Adopt as common core:** corrected v1.0.13 conventions, v1.0.19 implicit
  charge balance, bounded v1.0.22 equilibrium host blend.
- **Adopt as empirical layer:** v1.0.25 skew derivative and the v1.0.25.2
  surviving stored-8dp direct14 profile.
- **Keep as optional/theory:** v1.0.18.2 Einstein term, v1.0.23 transfer
  diagnostic, corrected Maxwell/regular-solution reference.
- **Rewrite before production:** causal/trajectory API, temperature/rate
  contract, heat/hysteresis, default/profile system and test coverage.
- **Do not treat as authority:** v1.0.11, code-identical/editorial releases as
  new physics, old regsol production path, prior 5.5 audit verdicts, or any
  v1.0.26 scientific conclusion.
