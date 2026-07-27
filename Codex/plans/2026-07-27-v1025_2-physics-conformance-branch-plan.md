# v1.0.25.2 Physics-Conformance Branch Plan

## Summary

이 계획은 `Project_Anode_Fit`의 `v1.0.25.2`를 보존한 채 별도 Git branch에서 기존 문건 계열을 전문 대조하고, 물리 명세를 먼저 확정한 다음 코드가 그 논리를 따르도록 보완하기 위한 실행 기준이다.

대조 대상은 두 계열이다.

1. `Codex/results`의 Chapter 1--5 이론 후보본
2. `Claude/docs/v1.0.25.2`의 graphite/LCO/Si 배포 문건, 배포 코드, 시험, 실측 피팅 provenance

이론 본문은 물리량, 가정, 유도, 경계조건, 적용범위만 서술한다. 함수명, 클래스명, 파일명, 시험명, 버전 이력은 본문에 넣지 않는다. 문건과 구현의 대응은 별도의 허용된 구현 절 또는 작업 대장에서만 기록한다.

## Current Ground Truth

### Git baseline

- Working branch: `codex/v1025_2-physics-conformance`
- Baseline commit: `ab196b292e14492b647f87a6c0d1d8c9ed0630ab`
- Baseline meaning: repository tree의 최신 인정본 `v1.0.25.2`
- Excluded scientific source: `v1.0.26`
- Existing unrelated working-tree change:
  `Claude/docs/v1.0.24.1/CODE_GUIDE_v24.html`
- 위 기존 변경은 본 계획에서 읽기·수정·복구·stage하지 않는다.

### Existing Codex manuscript candidates

| File | Lines at source freeze | Role |
|---|---:|---|
| `Codex/results/graphite_ica_ch1_codex_candidate_v5.tex` | 991 | graphite ICA, charge balance, equilibrium/lag |
| `Codex/results/graphite_ica_ch2_codex_candidate_v1.tex` | 854 | reversible heat and thermal linkage |
| `Codex/results/graphite_ica_ch3_codex_candidate_v1.tex` | 787 | directional kinetics |
| `Codex/results/graphite_ica_ch4_codex_candidate_v1.tex` | 863 | heat-generation closure |
| `Codex/results/graphite_ica_ch5_codex_candidate_v1.tex` | 825 | charge/discharge and hysteresis |

### Existing v1.0.25.2 release sources

| File | Lines at source freeze | Role |
|---|---:|---|
| `Claude/docs/v1.0.25.2/ch1_graphite_v1.0.24.tex` | 62 plus all included sections | graphite release manuscript |
| `Claude/docs/v1.0.25.2/ch2_lco_v1.0.24.tex` | 34 plus all included sections | LCO release manuscript |
| `Claude/docs/v1.0.25.2/ch3_si_v1.0.24.tex` | 34 plus all included sections | Si/blend release manuscript |
| `Claude/docs/v1.0.25.2/Anode_Fit_v1.0.24.py` | 2004 | release implementation |
| `Claude/docs/v1.0.25.2/CODE_GUIDE_v24.md` | 374 | implementation guide |
| `Claude/docs/v1.0.25.2/FITTING_GUIDE.md` | 137 | fitting guide |
| `Claude/docs/v1.0.25.2/results/HANDOVER_v1025_2.md` | 132 | release handover |
| `Claude/results/comp_v26_data/build_two_versions.py` | 223 | v1.0.25.2가 채택한 실측 fit provenance |
| `Claude/results/comp_v26_data/regsol_kernel.py` | 108 | builder의 top-level imported kernel dependency |
| `Claude/results/comp_v26_data/out_versions/C_skew/params_blend.json` | 101 | accepted empirical fit parameters |

### Confirmed constraints

- 실제 데이터가 정해진 전처리, 창, seed/bound 조건에서 피팅된다는 사실은 보존한다.
- curve-level fit success와 문건의 물리 파라미터 식별성은 별도 판정한다.
- 정칙용액, skew-logistic, causal relaxation, thermal/kinetic/hysteretic extension은 동일한 검증 지위를 자동으로 공유하지 않는다.
- manuscript의 논리 흐름을 코드 구조에 맞추어 왜곡하지 않는다.
- 구현은 확정된 물리 명세의 downstream artifact로 취급한다.

### Earlier Codex audit branch

- Prior audit branch:
  `origin/codex-local-audit-20260720`
- Tip:
  `20acd7dacc8aff62740e352bb68775758918602a`
- Recorded scope:
  v1.0.10--v1.0.23 lineage, scientific review, document--code fidelity,
  recent-theory review
- Authority status:
  **non-authoritative**

이 브랜치의 `file_manifest`, `read_coverage`, duplicate map, source-location
index는 원천 누락 방지용 색인으로만 사용할 수 있다. 그 브랜치의 PASS,
결함 수, 물리 판정, 강화 권고는 현재 검토의 결론으로 승계하지 않는다.
실제로 source locator로 채택한 주장만 현재 원문, 수식, 코드, 독립 계산으로
다시 판정했다. 이전 audit 전체의 claim-by-claim crosswalk는 수행하지
않았으며 완료 범위로 주장하지 않는다.

## Phase Range

| Phase | Name | Step Range | Purpose |
|---|---|---:|---|
| 044 | Source freeze and full-read comparison | 861--900 | 두 문건 계열, 코드, fit provenance를 고정하고 전문 대조한다. |
| 045 | Physics constitution and decision ledger | 901--950 | 공통 물리 사슬, 재료별 적용, 현상론 모델의 지위를 확정한다. |
| 046 | Manuscript architecture and clean branch copies | 951--990 | 기존 파일을 보존한 새 후보본 구조와 include graph를 만든다. |
| 047 | Graphite equilibrium/observation repair | 991--1040 | 전하보존, background, skew/regular-solution 지위를 정리한다. |
| 048 | Kinetics, temperature, and causal-boundary repair | 1041--1090 | fixed/total derivative, causal initial condition, branch history를 정리한다. |
| 049 | Heat, charge/discharge, and hysteresis repair | 1091--1140 | 가역/비가역열과 path dependence의 장간 전달식을 정리한다. |
| 050 | Material application modules | 1141--1190 | LCO와 Si/blend를 공통 물리 명세에 종속된 적용 모듈로 정리한다. |
| 051 | Empirical-fit preservation | 1191--1230 | 현재 14-peak 결과를 독립 재현 가능한 현상론 profile로 동결한다. |
| 052 | Implementation conformance and code repair | 1231--1300 | 허용된 구현 절에서 식/가정--구현--시험을 대응하고 코드를 보완한다. |
| 053 | Integrated verification and handover | 1301--1360 | 물리 불변량, fit 재현, TeX/PDF, ledger, handover를 닫는다. |

## Non-goals

- `Claude/`의 기존 파일을 수정하거나 덮어쓰지 않는다.
- `v1.0.26`의 과학적 결론을 채택하지 않는다.
- 실측 피팅 성공을 부정하거나 기존 parameter set을 임의 변경하지 않는다.
- 곡선 적합만으로 개별 peak의 phase assignment, graphite/Si 분해, 열역학 parameter 식별을 확정하지 않는다.
- 이론 본문에 코드명, 함수명, 파일명, test gate, commit hash, phase 기록을 삽입하지 않는다.
- 문건에 없는 silent clipping, implicit fallback, mutable global mode를 새로운 물리로 승인하지 않는다.
- 사용자가 요청하지 않은 push, merge, commit, PR 생성을 하지 않는다.

## Implementation Changes

### Create

- `Codex/results/PHASE_044_V1025_2_SOURCE_FREEZE_AND_COMPARISON_RESULT.md`
- `Codex/results/PHASE_044_053_V1025_2_CONFORMANCE_EXECUTION_LEDGER.md`
- `Codex/results/V1025_2_PHYSICS_DECISION_LEDGER.md`
- `Codex/results/V1025_2_PHYSICS_IMPLEMENTATION_CONFORMANCE_MATRIX.md`
- `Codex/results/v1025_2_physics_branch/` 아래의 새 manuscript candidate와 material module
- `Codex/work/v1025_2_physics_branch/` 아래의 구현 working copy와 검증 도구

### Preserve read-only

- `Codex/results`의 기존 candidate와 phase result 전부
- `Claude/docs/v1.0.25.2` 전부
- `Claude/results/comp_v26_data` 중 v1.0.25.2 handover가 직접 채택한 fit provenance
- 모든 이전 버전의 plan, handover, ledger, audit 원본

## Phase 044 — Source Freeze and Full-Read Comparison

- [x] Step 861: branch, baseline commit, dirty-file exclusion을 기록한다.
- [x] Step 862: 전문 검독 대상의 line count와 SHA256을 고정한다.
- [x] Step 863: master TeX의 `\input`/`\include` graph를 해석한다.
- [x] Step 864: 모든 included source를 처음부터 끝까지 읽고 coverage를 기록한다.
- [x] Step 865: Codex Chapter 1--5 candidate를 각각 처음부터 끝까지 읽는다.
- [x] Step 866: release code, code guide, fitting guide, handover, tests를 각각 처음부터 끝까지 읽는다.
- [x] Step 867: accepted 14-peak fit builder, top-level/local import dependency,
  seed/bound/RNG flow와 parameter artifact를 처음부터 끝까지 읽는다.
- [x] Step 868: 공통 기호, 식, 가정, 경계조건을 lineage별로 추출한다.
- [x] Step 869: 이전 audit의 claim을 source locator와 재검증 대상 목록으로만 추출한다.
- [x] Step 870: 이전 audit에서 locator로 실제 사용한 claim을 현재
  원문·코드·독립 계산으로 재검증하고, 전수 claim crosswalk 미수행을
  coverage limitation으로 기록한다.
- [x] Step 871: `확정`, `조건부`, `현상론`, `격리`, `근거 미발견`, `미검증`으로 새로 판정한다.
- [x] Step 872: manuscript body의 코드 언급 금지 위반을 별도 분류한다.
- [x] Step 873: 문건--코드 차이는 manuscript 수정안과 implementation repair로 분리한다.
- [x] Step 874: Phase 044 result와 ledger를 저장한다.

Gate:

- 전문 검독 대상으로 선언한 파일과 included source의 누락이 없어야 한다.
- 각 판정에는 파일, 절 또는 식의 근거가 있어야 한다.
- 읽지 않은 raw review draft는 읽은 것으로 기록하지 않으며, 권위 결과문과 중복인지 별도 표시한다.
- 이전 audit의 PASS/0결함 주장은 독립 재검증 전에는 evidence로 계수하지 않는다.

## Phase 045 — Physics Constitution and Decision Ledger

- [x] Step 901: 변수와 좌표의 canonical convention을 확정한다.
- [x] Step 902: 관측식, chemical storage, equilibrium, kinetics, heat, hysteresis의 one-way dependency를 작성한다.
- [x] Step 903: `C_meas`와 `Q_bg^chem`을 분리한다.
- [x] Step 904: fixed-temperature derivative와 total derivative의 적용범위를 분리한다.
- [x] Step 905: monotonic single-branch model과 trajectory model을 분리한다.
- [x] Step 906: causal-memory 초기조건과 prehistory 계약을 확정한다.
- [x] Step 907: empirical skew mixture와 physical host model을 분리한다.
- [x] Step 908: regular-solution 식의 채택 범위와 alternative/reference 지위를 확정한다.
- [x] Step 909: graphite/LCO/Si의 공통 core와 material-specific closure를 분리한다.
- [x] Step 910: 각 항목을 decision ledger에 저장한다.

Gate:

- 물리 명세가 클래스나 함수 구조에 의존하지 않아야 한다.
- 동일 기호가 진행도, 용량, 조성처럼 서로 다른 의미로 사용되지 않아야 한다.
- 미결인 물리 선택은 코드 수정으로 우회하지 않는다.

## Phase 046 — Manuscript Architecture and Clean Branch Copies

- [x] Step 951: 기존 candidate를 변경하지 않고 새 branch manuscript directory를 만든다.
- [x] Step 952: 공통 물리 사슬을 정본으로 두고 material application을 종속 모듈로 배치한다.
- [x] Step 953: 본문, material module, implementation appendix의 경계를 문서 구조로 고정한다.
- [x] Step 954: 안정적인 equation/assumption identifier를 부여한다.
- [x] Step 955: 작업 이력과 검수표가 manuscript body에 들어가지 않는지 확인한다.
- [x] Step 956: include graph와 bibliography ownership을 고정한다.

Gate:

- manuscript body에는 물리 내용만 남아야 한다.
- 구현 appendix 이외의 절에는 code symbol과 file path가 없어야 한다.

## Phases 047--050 — Scientific Repair

각 phase는 다음 루프를 독립적으로 수행한다.

1. 기존 두 lineage의 전문 대조
2. 수식 전개의 차원, 부호, 독립변수, 극한, 경계조건 확인
3. 확인된 결함만 새 candidate에서 수정
4. 수정 절의 앞뒤 논리 사슬 재검독
5. 해당 장 전체 재검독
6. static TeX 검증과 가능하면 XeLaTeX build
7. result와 ledger 갱신

완료 상태:

- [x] Phase 047: equilibrium, charge-balance, observation and graphite repair
- [x] Phase 048: kinetics, SI-rate and causal-boundary repair
- [x] Phase 049: reversible/irreversible heat and hysteresis-boundary repair
- [x] Phase 050: LCO and graphite--Si material-module repair

중요 경계:

- skew-logistic의 면적보존 수학은 보존하되 phase identification을 자동 부여하지 않는다.
- physical blend는 공통 내부전위, 조성비, 질량/용량 기준, 전하보존을 갖춰야 한다.
- Si와 LCO의 자유 parameter는 자료 등급과 식별 상태를 함께 표시한다.
- 정칙용액/Maxwell은 실제 채택 closure와 해석 대안을 구분한다.
- 반응속도 overflow를 평형으로 조용히 대체하지 않는다.
- 유한 관측창의 초기조건을 `-\infty` 자연경계와 동일시하지 않는다.

## Phase 051 — Empirical-Fit Preservation

- [x] Step 1191: input file hash, 전처리 순서, fitting window를 동결한다.
- [x] Step 1192: kernel 식, parameter order, bounds, seed, restart 조건을 동결한다.
- [x] Step 1193: surviving stored-8dp 14-peak + background artifact를 immutable
  empirical reference로 복사하고, original optimizer full precision과 당시
  prediction이 보존되지 않은 provenance gap을 기록한다.
- [x] Step 1194: 저장된 8-decimal vector의 metric을 독립 실행으로 재계산하고,
  optimizer에서 보고된 반올림 metric과 구분한다.
- [x] Step 1195: profile별 stored boundary coincidence, 원 optimizer
  active-set evidence와 measurement-resolution 이하 parameter를 구분해
  non-identified로 표시한다.
- [x] Step 1196: empirical-fit 결과가 검증하지 않는 물리 주장을 명시한다.

Gate:

- 물리 코드 보완 전후에 accepted curve 결과가 합의된 tolerance 안에서 재현되어야 한다.
- 실측 자료가 저장소에 없거나 provenance가 완결되지 않으면 `미검증`으로 중단하고 parameter를 새로 추정하지 않는다.

## Phase 052 — Implementation Conformance and Code Repair

- [x] Step 1231: canonical equation/assumption ID를 구현 symbol과 연결한다.
- [x] Step 1232: 각 연결에 unit/sign/limit/invariant test를 지정한다.
- [x] Step 1233: empirical, physical-host, regular-solution-reference profile을 분리한다.
  Regular solution은 production package에서 제외하고 manuscript theory/reference로 고정했다.
- [x] Step 1234: mutable global legacy switch를 명시적 compatibility profile로 대체한다.
  Clean candidate에는 global switch가 없고 legacy release 자체는 수정하지 않았다.
- [x] Step 1235: background와 default transition의 실제 소비 경로를 명시한다.
- [x] Step 1236: invalid material case와 parameter domain을 fail-fast 검증한다.
- [x] Step 1237: fixed-T path와 trajectory/variable-T path를 분리한다.
  Coupled variable-T trajectory closure는 구현된 것으로 주장하지 않는다.
- [x] Step 1238: causal boundary, duplicate voltage, monotonicity 계약을 구현한다.
- [x] Step 1239: overflow와 non-finite kinetic scale을 log-domain 또는 명시적 domain failure로 처리한다.
- [x] Step 1240: stored-8dp empirical profile reconstruction과 legacy
  compatibility를 각각 검증한다.

Gate:

- 코드 수정의 이유가 manuscript의 특정 물리 명세로 추적되어야 한다.
- 구현 편의가 manuscript의 지배방정식을 역으로 바꾸지 않아야 한다.
- production-default test는 legacy mode를 강제로 켜지 않은 상태에서 수행한다.

## Phase 053 — Integrated Verification and Handover

- [x] Step 1301: 모든 manuscript source의 전문 재검독 coverage를 닫는다.
- [x] Step 1302: dimension, sign, area, charge balance, limiting behavior gate를 실행한다.
- [x] Step 1303: accepted stored-8dp empirical profile reconstruction을
  실행하고 original optimizer reproduction은 unavailable 상태인지 확인한다.
- [x] Step 1304: physical-host synthetic recovery와 공개 자료 검증 가능 범위를 실행한다.
- [x] Step 1305: TeX static check와 XeLaTeX build를 실행한다.
- [x] Step 1306: PDF version/title/source hash를 확인한다.
- [x] Step 1307: implementation conformance matrix의 모든 row 상태를 갱신한다.
- [x] Step 1308: unresolved issue와 user decision queue를 handover에 남긴다.

Gate:

- 확인하지 않은 항목을 PASS로 기록하지 않는다.
- code, tests, TeX, PDF가 동일 source state를 가리켜야 한다.

## Implementation Interfaces

### Manuscript physical interface

본문에서 최소한 다음 위계를 명시한다.

\[
y(V_{\mathrm{app}})
=
C_{\mathrm{meas}}(V_{\mathrm{app}})
+
\frac{\mathrm d Q_{\mathrm{chem}}}{\mathrm d V_{\mathrm{app}}},
\]

\[
Q_{\mathrm{chem}}
=
Q_{\mathrm{bg}}^{\mathrm{chem}}
+
\sum_j Q_j\xi_j.
\]

위 두 식은 최종 채택식이 아니라 Phase 045에서 부호, 좌표, fixed/total derivative를 다시 판정할 starting interface다.

### Conformance row

| Field | Meaning |
|---|---|
| Physics ID | manuscript의 식 또는 가정 identifier |
| Physical statement | 코드에 독립적인 물리 명세 |
| Validity domain | 온도, 전압창, 단조 branch, 자료 등급 |
| Implementation symbol | 허용된 구현 대장에서만 기록 |
| Test/invariant | 차원, 부호, 면적, 용량, 극한, 재현 |
| Status | conforming / partial / divergent / not implemented / theory-only |
| Evidence | 파일과 정확한 절 또는 line range |

## Test Plan

- SHA256 and line-count source freeze
- resolved TeX include graph coverage
- static label/ref/cite/environment checks
- forbidden implementation-term scan outside allowed appendix
- symbolic/manual differentiation checks
- finite-difference derivative checks
- dimensional and sign checks
- area/capacity conservation
- causal-window and sampling convergence
- monotonic/nonmonotonic trajectory behavior
- stored-8dp empirical-profile reconstruction
- production-default and legacy-profile separation
- XeLaTeX build and PDF metadata/hash verification

## Assumptions

- `ab196b2` tree를 최신 인정본 `v1.0.25.2`로 취급한다.
- `v1.0.26`은 과학적 source로 사용하지 않는다.
- `origin/codex-local-audit-20260720`은 source index로만 사용하고 그 과학 판정은 승계하지 않는다.
- user가 별도 지시하기 전까지 모든 변경은 local branch와 `Codex/`에만 존재한다.
- archived `sigr.csv`의 stored-8dp profile은 재구성 가능하지만 experimental
  protocol과 original optimizer state는 unavailable/unknown이다.
- manuscript top-level architecture는 Phase 046 candidate로 고정했으나 실제
  TeX source promotion 전까지 deliverable source로 취급하지 않는다.

## Correction History

- 기존 계획의 미실행 Phase 044 `Integrated refs/full manuscript`는 본 계획의 Phase 044--050에 흡수한다.
- 단순 통합에 앞서 `v1.0.25.2`와 Codex Chapter 1--5 후보본의 전문 비교 및 물리 지위 판정이 필요하므로 Phase 044의 진입 작업을 source freeze와 comparison으로 확장했다.
- 기존 manuscript candidate와 Claude release source는 덮어쓰지 않고 새 branch artifact를 만든다.
