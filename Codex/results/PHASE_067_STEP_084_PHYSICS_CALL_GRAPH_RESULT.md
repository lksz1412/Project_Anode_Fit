# Phase 067 Step 84 Physics Call-Graph Result

정본일: 2026-09-02

## Gate

- selected content Gate: `PASS_P067_STEP84_PHYSICS_CALL_GRAPH`
- precommit state: `PASS_PENDING_PERSISTENCE`
- expected parent: `1af6c06fb5cff2918b846ed74ea213832f04f010`
- expected subject: `audit(phase067): reconstruct physics call graph`
- containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`
- required postcommit terminal: `PASS_P067_STEP84_PERSISTENCE`

이 Gate는 frozen production source의 static public-entry call-sequence와 branch/state-dependency
구조만 닫는다. 실제 runtime order, 이론의 참, 외부 과학·재료 타당성, canonical model 선택,
publication readiness를 확립하지 않는다.

## Recovery and Exact Inputs

작업 전 다음을 1행부터 EOF까지 직접 재확인했다.

- Phase 067 detailed plan: `1–766`
- Step 83 result: `1–89`
- parent execution ledger: `1–160`
- canonical completion ledger: `1–180`
- active handover: `1–437`

Git 경계는 local/upstream/tracking/live
`1af6c06fb5cff2918b846ed74ea213832f04f010`, protected local/tracking/live
`fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`, main tracking/live
`4069cb36a8a52b1b88c29d68aa54dcbe915b1618`, local main absent, clean tree,
protected-to-worktree `Claude/**` diff empty로 확인했다.

Committed inputs are pinned independently:

- Step 82 inventory raw/semantic: `b7f14370ad4f3ac5879a1963b2c973cb9dcfe7974598671c2b5459ac35b89e63` / `593e79c593eec9a05c154152be7e240c251900014eca0056eb109c2a33a8a5f1`
- Step 82 full-read attestation raw/semantic: `112684d7347524a5fe96d24bae7fe5c939adf550fd88ca0712effd72d31af174` / `e9ccde5895eae5269fb680b8db419c7f7fb6f7c55403556cb4aa187a492303c9`
- Step 83 matrix raw/semantic: `0a2f2ab9ef46ee4298ec1080a8690c9a93df61d137751a9c76b4e771d0ceb4a8` / `c2406c2100332eacf0431f18d9e530eff8f5adf02bd41b60f7d5d2526896df44`

## Source-Static Graph

Step 82 전체 `129` occurrence / `84` unique Python Git blobs / `29,952` unique-blob
physical lines / `20` releases를 그대로 결속했다. Step 84 graph 대상은 Step 83과 동일한
production `20` occurrences / `15` unique blobs이며 nonproduction `109` occurrences는
lossless exclusion으로 남는다.

Shared source blob은 한 번만 graph로 저장하고 각 occurrence가 release/path/blob/blob ordinal/
manifest entry/mode/hash/line identity로 이를 참조한다. Machine projection은 unique-blob graph
`15`, definition nodes `198`, retained physics call edges `219`(unresolved dynamic callable/dispatch
edges `80` 포함), named scenario rows `390=15×26`, 그중 source-static PRESENT `259`다.
Release-family coverage는 `20×6=120`, condition behavior는 `20×7=140`이다.

각 resolved edge는 caller/callee, callable expression, lexical ordinal, branch predicate, positional/
keyword argument, result binding, qualified owner, AST kind/extent, exact source slice SHA-256와
normalized AST SHA-256를 가진다. `self.Cbg`, `self.chi_split`, blend host instance dispatch는
resolved function edge로 승격하지 않는다.

## Grounded Order and Boundaries

- charge-balance: v1.0.19+ `solve_U_oc`의 params/total capacity → bracket → nested `_charge`
  residual → endpoint sign test → bisection을 결속한다. Exhaustion은 explicit nonconvergence
  raise 없이 final midpoint를 반환한다. Blend는 v1.0.22+ `_balance_host.solve_U_oc` dynamic
  instance dispatch로만 기록한다.
- background: callable/scalar `Cbg`는 `equilibrium`, `dqdv`, `host_contributions`에서 직접
  평가된다. Frozen source에 별도 background self-consistency solver는 없다.
- lag/trajectory: v1.0.10–14의 work-grid/T interpolation → `_causal_lowpass` → final interpolation,
  v1.0.15+ pointwise stable sort/inverse restoration, v1.0.23+ frozen `ksi_lag0` ratio path,
  v1.0.25+ pad/re-evaluation을 release별 구분한다.
- kinetics: `L_V` override가 우선하고 invalid override는 raise한다. nonpositive current 또는
  missing activation input은 zero lag, nonfinite `L_q`도 zero lag으로 source-static 분기한다.
- heat: `reversible_heat → entropy_coefficient`, `reversible_heat_x → entropy_coefficient_x`,
  `entropy_coefficient_x → solve_U_oc + entropy_coefficient`만 연결한다. Irreversible heat는
  direct calculation이며 entropy가 equilibrium/dqdv를 호출한다고 만들지 않는다.
- observation: `curve → dqdv`, direct `equilibrium`, blend host delegation과 early/late trajectory
  ordering을 분리한다. Standalone transfer helper는 public `curve/dqdv` edge가 아니다.

## Behavior Ledger

`OPTION_OFF`, `MISSING_KINETICS`, `ZERO_CURRENT`, `REVERSAL`, `REST`, `INVALID_ROOT`,
`MAX_ITER_EXHAUSTION`을 각 release에서 exclusive source status로 기록한다. Rest-aware
`func_U_j_hys(last_eta,last_rest)`와 `transfer_apparent_from_equilibrium`은 정의된 release에서도
fresh public-entry caller가 0이면 `DORMANT_NO_PUBLIC_CALLER`이며, prose/self-report로 edge를
보충하지 않는다. Scalar/singleton/identical-grid/unresolved/nonpositive lag의 equilibrium-term
선택은 source anchor가 있을 때만 기록했다.

`OPTION_OFF`는 v1.0.23+의 `elif self.lag_ratio_correction`에 대응하는 exact `else`이며,
false일 때 equilibrium-term이 아니라 ordinary `_causal_memory_pointwise`를 선택한다. 그 이전
release에는 이 option이 없어 `ABSENT_IN_FROZEN_SOURCE`다. 각 behavior는 자기 조건을 실제로
지지하는 named sequence만 참조하고, absent/dormant/GNF row의 sequence refs는 비어 있다.
`INVALID_ROOT` present row는 `x_bar` domain, nonpositive `Q_tot`, `U_lo >= U_hi`, endpoint-sign
failure의 네 closed subcase와 각각의 predicate/raise anchor를 별도로 저장한다. Max-iteration
exhaustion은 이 raise subcase들과 분리하며 final midpoint assignment만 결속한다.

## Correction History

첫 preview의 `7,698` DFS leaf paths는 한 public root의 sibling helper branches를 반복 전개한
combinatorial redundancy였으므로 폐기했다. 현재 `390`은 실행된 runtime path 수가 아니라
15 unique blobs 각각의 26개 named static scenario slot이다. Shared blob graph는 한 번만 저장하고
20 occurrence가 무손실 참조한다. 이 correction은 coverage `120`, behavior `140`, ambiguity와
absence evidence를 줄이지 않는다.

첫 full stable candidate와 그 PASS는 독립 검토에서 false OPTION_OFF anchor/status, absent/dormant를
포함한 모든 behavior로의 무차별 sequence fanout, INVALID_ROOT의 first-Raise underbinding이 확인돼
폐기됐다. 현재 보정본은 OPTION_OFF를 이전 release `14` ABSENT와 v1.0.23+ `6` PRESENT로 분리하고,
behavior별 source-grounded sequence refs만 허용해 non-present refs를 `0`으로 고정하며, v1.0.19+
INVALID_ROOT `10`개 각각을 네 predicate/raise subcase(`10×4`)로 결속한다.

## Authority and Open Gaps

- `actual_runtime_order_proven=false`; only static public-entry call-sequence is established.
- dynamic dispatch, background solver absence, dormant rest/transfer helpers는 Step 85/88 또는
  명시 owner에서 runtime/default/impact를 검증하기 전까지 승격하지 않는다.
- unit conversion and numerical behavior는 Step 87, fallback impact는 Step 88 소유권이다.
- Ref. 7 original, optimizer full state, held-out/external/material authority와 stale PDFs는 open이다.
- production source, `Claude/**`, LaTeX/PDF는 수정하지 않았다.

## Validation Boundary

Builder preview는 Python 3.12에서 `20/15`, nodes `198`, edges `219`, dynamic `80`, named
scenarios `390`/PRESENT `259`, coverage `120`, behavior `140`, determinism `2/2`를 재구성했다.
Validator는 builder를 import하지 않고 source Git blobs에서 독립 재구성하며 closed schema,
source/control hashes, semantic mutation controls, strict JSON, exact-seven worktree/stage/commit,
single-parent `%P`, refs, index/tree bytes, protected/main/Claude와 entry/terminal seal을 강제한다.

현재 self-audit는 `P0/P1/P2=0/0/0`이다. 이 문서는 result-first boundary이고 canonical JSON은
두 ledger와 handover 갱신 뒤 JSON-last로 한 번만 수집한다. Controller만 exact-seven을 stage하고
dual `--verify-staged`, exact subject commit/push/live/clean, dual
`PASS_P067_STEP84_PERSISTENCE`를 완료할 수 있다. 그 전 Step 85는 blocked다.
