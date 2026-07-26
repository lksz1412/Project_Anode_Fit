# PHASE 022B - Chapter 1 Claude-Base 10-Pass Review

## Coverage

- Reviewed source: `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_rebuilt_codex_v1.tex`
- Direct full-file read: lines 1-839 in four ranges: 1-220, 221-440, 441-660, 661-839.
- Chunk coverage file: `PHASE_022B_CH1_CHUNK_COVERAGE.txt`
- Chunk sizes used: 37, 49, 61, 73, 89, 109, 131, 157, 191, 233 lines.
- Parallel read-only review agents: convention/dimension/sign, physics/assumption/citation, followability/fitting usability.

## Pass Summary

1. User-critique replay: Section 7+ improved vs older drafts, but Plan A/B and Volterra still dominate the reader-facing flow.
2. Section-boundary continuity: charge -> equilibrium -> rate -> kernel was mostly present; fitting handoff needed reordering.
3. Variable meaning: `Theta_eq`, `Theta_init`, `Theta_0`, `L_varphi`, and amplitude spectrum meaning needed explicit definitions.
4. Equation provenance: several equations mixed derived result, bounded ansatz, and solver instruction without enough labeling.
5. Physics consistency: common-mode mobility and BV/Marcus directional barrier split were conflated.
6. Dimensional/sign audit: q/Q/V bridge was mostly sound; C-rate interpretation conflicted with `L=|I|/(Q_cell k)`.
7. Spectrum/kernel audit: `A_L` overloaded probability and amplitude meanings; single-mode delta missed amplitude.
8. Self-consistency audit: user's refs 6/7 support unknown-ratio closure for Fredholm equations, not direct Volterra transplantation.
9. Simplefit usability audit: Chapter 1 needed an explicit observable `Y_tail` and small-tail condition.
10. Manuscript hygiene: process metadata and placeholder bibliography needed removal/correction.

## Key Defects Found

### 잘못된 부분

- Lithiation staging direction was not separated from discharge/delithiation branch convention.
- `A_L` was used as both probability fraction and amplitude spectrum.
- Single-mode limit used `A_L=delta(L-L0)` without amplitude, inconsistent with `Theta_0/L` form.
- C-rate paragraph claimed unconditional shortening despite `L=|I|/(Q_cell k)`.
- BV/Marcus directional barrier logic was used to justify common-mode mobility without enough separation.
- `chi_j` was too close to transfer coefficient `beta_j` despite Level-A scalar mobility interpretation.

### 부족한 부분

- Simple observable fitting formula was not explicit enough.
- `V_n` conversion from measured `V_n,app` under polarization needed a practical route.
- Arrhenius extraction conditions omitted prefactor, entropy, and fixed-drive requirements.
- Barrier-only disorder assumption needed to be named.
- Self-consistency closure needed to be demoted from main proof to bounded correction.

### 개선할 부분

- Put convention and assumption ledger near the beginning.
- Use Korean explanatory prose with English technical terms.
- Reorder late chapter flow: kernel -> simplefit -> optional self-consistency correction.
- Make `Y_tail(q) approx B exp[-(q-q_a)/L]` the Chapter 1 deliverable.
- Explain C-rate as competition among current prefactor, potential-assisted rate increase, and apparent-axis polarization.

### 좋은 점/흡수할 부분

- Charge conservation as the definition of `V_n`.
- `d xi/dt -> d xi/dq` and dimensionless `L` derivation.
- Jacobian `RT/L` vs kernel `1/L` origin separation.
- Double-counting warning in Volterra formulation.
- Sequential identifiability: equilibrium stage and `R_n` before `chi_j`.

### 추가 검증 필요

- Low-rate OCV/GITT should support selected equilibrium target and width.
- Plan A closure must be checked against Plan B before quantitative use.
- `rho_G` is not uniquely invertible from one tail curve.

## External Source Checks

- User PDF `JCP 147, 144111 (2017)` was inspected with pypdf for pages containing Eq. (32)--(34) and references.
- Web metadata was checked for DOI/title corrections:
  - `10.1063/1.5000882`: Lee et al., JCP 147, 144111 (2017).
  - `10.1063/1.3565476`: Lee, Son, Sung, Chong, JCP 134, 121102 (2011).
  - `10.1063/1.4802584`: Son et al., JCP 138, 164123 (2013).
