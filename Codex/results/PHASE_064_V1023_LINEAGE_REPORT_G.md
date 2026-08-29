# Phase 064 v1.0.23 Lineage Report G

Gate: `CONDITIONAL_P064`
상태: `CONDITIONAL_WITH_OPEN_EXTERNAL_AUTHORITY`
Containing commit: `PENDING_AT_PRECOMMIT_BY_DESIGN`
Expected parent: `ec1fb2eda54feb35cd6c15d2ab15f2478b26fc6d`
Expected subject: `audit(phase064): close v1023 lineage gate`
Postcommit persistence terminal: `PASS_P064_STEP69_2_PERSISTENCE`

## 결론

v1.0.23의 내부 계보, 원천 범위, 전문 검독, 수학 재유도, 실행 경계, 권위 판정과 후속 소유자 배정은 Phase 064의 선언 범위에서 완결됐다. 그러나 Ref. 7의 정확한 서지정보와 DOI `10.1063/1.4802584`만 확인됐고 원문은 `GROUND_NOT_FOUND`다. 따라서 내부 감사 완결성을 외부 문헌 완결성으로 승격하지 않고 `CONDITIONAL_P064`를 선택한다.

Ref. 7 단일 취득 owner는 `PHASE-071-PRIMARY-SOURCE-ACQUISITION`이다. Acceptance criterion은 합법적으로 원문을 확보하고 raw hash와 쪽수를 고정한 뒤 1–EOF 및 전 쪽을 실제 검독하기 전까지 method-content 사용을 금지하는 것이다. Primary target은 Phase 071 `PRIMARY_SOURCE_ACQUISITION`이다.

## 복구·입력 범위

- Phase 064 activation과 Steps 64–69.1의 고정 커밋, parent, subject, exact path set, validator hash를 재확인했다.
- machine artifact `11/11`을 duplicate-key 및 nonfinite 거부 조건으로 strict parse하고 모든 중첩 노드를 순회했다.
- 이전 결과 문건 `7/7`의 고정 커밋 바이트와 SHA-256을 대조했다.
- historical validator는 disposable historical context에서 precommit `8/8`, persistence `7/7`, 합계 `15/15`를 fresh replay했다.

## Source, process and read closure

Frozen denominator는 manifest source `83/83`, unique blob `83/83`, raw bytes `3,338,330`이다. Text는 `78/78` 파일과 `12,508/12,508` physical lines, PDF는 `3/3` 파일과 `129/129`쪽, image는 `2/2` original-resolution occurrence다. Coverage gap, duplicate route, source mutation은 모두 `0`이고 human read attestation은 complete다.

v1.0.23 process commit은 `14/14`를 고정했다. P4는 실패나 누락으로 재분류하지 않고 사용자 결정 D3에 따른 `SKIPPED_D3_NOT_APPROVED`로 보존한다. Phase 057 provisional observation `36/36`은 증거 행이지 신규 blocker 분모가 아니다.

## Literature authority

- JCP147 VOR은 `10/10`쪽을 전문·시각 검독했고 Eqs. 32–39 crop `8/8`과 세 applicability condition을 고정했다.
- Ref. 6 DOI `10.1063/1.3565476` VOR은 `4/4`쪽을 전문 검독했으며 raw SHA-256은 `c0f2dbefa26731581235da28477f19f07f81f1e897523f6144e272f6b0959460`이다. 현재 상태는 CLOSED bounded method authority다.
- Ref. 7 DOI `10.1063/1.4802584`는 official bibliographic metadata only다. Original full text는 `GROUND_NOT_FOUND`이며 method-content authority는 없다.
- `10.1063/1.4802005`는 hard-helices 논문이므로 Ref. 7 DOI 후보에서 명시적으로 폐기했다.
- Eq. 32/33의 exactness는 upstream Eqs. 19/20 orientation-averaging 근사계 내부에 한정되고, Eqs. 34/39는 approximation으로 유지한다.

## Fredholm, Volterra and transfer rederivation

JCP147 계는 고정된 반무한 영역의 Fredholm second-kind 문제다. v1.0.23 lag 계는 directed voltage coordinate의 nonlinear causal Volterra second-kind 문제이며 local first-order nonlinear ordinary differential equation과 동치다. 문제 종류가 다르므로 JCP solution-ratio를 graphite 계의 literal identity로 승격하지 않는다. 선택한 `kappa(xi)`는 `REDUCED_FEEDBACK_HYPOTHESIS`다.

Step 65 Eq. 38 semantic projection의 `exp(K*r*mu)`는 동일 원문 crop에 결속된 역사적 오기로 보존하되 Step 66의 `exp(K*sigma*mu)`로 supersede했다. 단일 binding `P064-EQ38-SUPERSESSION-001`은 Step 69.1에서 CLOSED이고 Phase 082 equation-freeze owner로 이어진다.

충분 수축 조건 `q=||sigma||_infinity K_kappa/kappa_min^2<1`은 선언한 remote-past/zero-initial 함수공간에서만 유효하다. `epsilon_local=gL0/(4w)`는 leading-order local heuristic이며 global convergence theorem이 아니다. Benchmark 마지막 행에서 `q>1`인데 Picard가 수렴한 사실은 충분조건의 필요조건화를 허용하지 않는다.

`H=1/(1+i*omega_x*L0)`는 `omega_x` 단위가 `V^-1`인 voltage-coordinate transfer다. Explicit sweep rate 없이 time response, electrochemical impedance spectroscopy 또는 instrument response로 해석하지 않는다. Unpadded discrete Fourier transform은 finite window에서 circular이며 일반 causal kernel을 보증하지 않는다.

## Algebraic, implementation and runtime boundary

세 문제 class는 charge-balance algebraic root, background algebraic self-consistency, causal lag Volterra/ODE이고 ratio-reference applicability는 순서대로 `false/false/true`다. Background solver는 frozen source에서 `GROUND_NOT_FOUND`이며 derivative addend와 혼동하지 않는다.

시간 단위 계약은 `dq/dt_s=I_A/(3600 Q_Ah)=C_h/3600`이다. 기존 경로는 kinetic length를 `3600`배 과대평가할 수 있으므로 실제 current regime의 승인 근거로 쓰지 않는다. Runtime은 Python 3.12/3.14에서 official/mutation expectation `10/10`, independent probe set `2/2`를 재현했다. Findings는 P0/P1/P2=`1/5/3`이며 모두 owner가 있는 downstream route다.

## Validation authority

Planned core gate `37/37`, complete authority record `47/47`, authority axis `7/7`, overclaim route `14/14`를 확인했다. Material validation, experimental validation, comprehensive external-primary validation은 각각 `0/0/0`이다. Internal synthetic/regression, selected Picard behavior와 voltage-coordinate identity는 bounded evidence이나 canonical selection, defect repair, identifiability, held-out fitting, final equation freeze, final LaTeX/PDF 또는 publication readiness를 뜻하지 않는다.

## Disposition and carry-forward

Source disposition `83/83`의 분포는 `CORRECT=35`, `PRESERVE=34`, `THEORY_ONLY=5`, `UNVERIFIED=9`이고 exact v1.0.22 counterpart는 `63/63`이다. Supplemental denominator는 별도 `6/6`이며 Ref. 7 acquisition route 하나가 OPEN이다.

Observation denominator는 Phase 057/Step 66/Step 67=`36/11/9`다. Canonical topical route는 Step 68 authority `14`와 residual `4`를 합친 `18`이며 OPEN `17`, CLOSED `1`이다. Phase 063 owner registry `308`을 보존하고 18 topical owner row를 더한 duplicate-check universe는 `326`이다. Ownerless, multiply-owned, new Phase 064 blocker와 external-authority promotion은 모두 `0`이다.

## Integrated controls

Historical replay `15/15`, named semantic/document/policy negative `37/37`, strict JSON negative `6/6`, real disposable Git boundary `17/17`, deterministic projection `2/2`를 요구하고 통과했다. Final exact-eight는 이 보고서, Gate Result, Phase Result, final validator, validation JSON, 두 execution ledger와 active handover다. Validation JSON은 나머지 일곱 결과를 먼저 고정한 뒤 마지막에 원자적으로 생성한다.

## 확정 / 미결 / 근거 미발견

확정: 내부 source/process/read, Ref. 6 bounded full-text authority, JCP147 equation provenance, Fredholm–Volterra 분리, Eq. 38 correction binding, factor `3600`, voltage-axis transfer ceiling, runtime reproduction, authority matrix와 owner routing.

미결: Ref. 7 original acquisition, downstream canonical selection, defect repair, identifiability, held-out fitting, final equation freeze, final LaTeX/PDF와 publication readiness.

근거 미발견: Ref. 7 original full text와 그 method-content authority, frozen production의 background algebraic solver.

## Alternatives rejected

- `PASS_P064_LINEAGE_G`: Ref. 7 original full text가 없으므로 계획의 full-literature Gate를 충족하지 못해 기각한다.
- `FAIL_P064`: 내부 denominator, 전문 검독, 재유도, 실행 검증과 owner routing이 완결됐고 외부 의존성을 정확히 한정했으므로 기각한다.

## 다음 단계

`PASS_P064_STEP69_2_PERSISTENCE` 전에는 Phase 065 detailed plan 또는 Step 70을 시작하지 않는다. Persistence가 확인된 뒤 `Codex/plans/`에 Phase 065 detailed plan을 먼저 저장·활성화하고, 그 다음 누적 Step 70을 실행한다.
