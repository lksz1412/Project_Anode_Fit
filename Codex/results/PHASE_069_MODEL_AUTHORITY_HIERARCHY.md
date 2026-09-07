# Phase069 Step102 — 모델 계층과 주장 권위

## Summary / 현재 결정

상태: CONTENT_VERIFIED_AWAITING_PUSH; PASS_P069_STEP102_MODEL_AUTHORITY_HIERARCHY. 승인된 권위 계약의 완료이며 새 물리모델의 채택/검증 완료가 아니다.
기준: Step99 canonical audit, Step100 요구사항, Step101 본문 경계, 활성 master와069 detailed Step102.
Step101은76b07667085c0d1d886b667ce2b490b40470af7a로 결과 포함commit/push/live/clean까지 확인됐다.
정확한10입력 identity는 PHASE_069_STEP_102_MODEL_HIERARCHY_RESULT.md에 둔다.
여기서 empirical/reduced-physics/production-physics는 이 프로젝트의 역할 구분이지 보편적 인증 등급이 아니다.

모델의 복잡도·구현 분량과 과학적 근거의 강도는 다른 축이다.
세 층은 이름만 바꾸며 올라가는 자동 승급 사다리가 아니며, 같은 식도 사용 목적·가정·증거에 따라 다른 주장을 갖는다.
예측 정확도, 수식의 정합성, 원문 support, 모수 식별성, 실제 재료/기전 해석, 구현 충실성은 별도로 판정한다.
단순 empirical 모델이 특정 자료에서 더 잘 맞는 사실을 보존하고, 큰 물리모델이라는 이유로 우월성을 선언하지 않는다.

## 계층별 입력·가정·수식·자료·식별성·허용 주장

| 비교 축 | Empirical observation fit | Source-supported reduced physics | Protocol/material production physics |
|---|---|---|---|
| 목적 | 관측 곡선 재구성·비교·한정된 예측의 실제 가치를 보존 | 명시 가정/축약 하에서 상태·보존·관측의 물리적 관계를 설명 | 지정 재료·조건·protocol의 동적 상태와 관측을 검증 가능한 운용 범위에서 계산 |
| 입력 | 관측 Q/V/time/current/temperature, capacity basis, branch, 전처리/잔차 모델과 fit 모수 | 좌표·상태·basis·원문 변수 mapping, 물리 모수/축약 closure, 초기·경계 조건, 온도·protocol 범위 | 검증된 재료/전극/constituent 정보, signed time/current·rest/reversal·초기상태, 필요한 수송·열·미세구조 조건과 관측 연산 |
| 가정 | basis component는 관측 형상의 표현이며 phase/site/gallery/기전으로 선해석하지 않음 | 생략한 자유도와 시간·길이 scale, equilibrium/metastable/nonequilibrium 범위, closure의 경험적 부분을 공개 | 채택 축약의 유효 범위와 필요한 coupling을 명시. 이름만으로 모든 입자/전극/열/기계를 포함했다고 주장하지 않음 |
| 수식 책임 | 관측 표현·미분/적분·면적·정규화·domain을 실제 정의대로 검사; 형상 모수를 상태함수로 전환하지 않음 | 정의→가정→보존/열역학/반응·수송→중간식→관측량 유도, 단위/부호/domain/극한과 원문 exact anchor | 채택식 전체의 연결, protocol chronology/state transfer/finite-window accounting, 보존/극한/경계, 오차·실패 계약의 일관성 |
| 외부 자료 | in-sample fit은 해당 데이터의 재구성 증거. 다른 조건 예측은 따로 held-out 평가 | 수식 적용 가능성과 재료 해석을 지지하는 원문·구조/열역학/실험 자료; calibration과 검증 구분 | 실제 specimen/protocol/basis/provenance가 확인된 calibration 및 독립 held-out 조건/cell/material transfer 자료 |
| 식별성 | 여러 분해가 같은 곡선을 설명할 가능성, width/center/area/background 상호 보상과 잔차/전처리 불확도 공개 | 구조적/실용적 비식별 모수 조합과 대안 기전, 고정한 closure/priors의 영향을 공개 | 사용 범위에서 모수·예측 불확도와 민감 조건, 외삽/전이 실패, 관측 해상도 및 independent validation의 제한 명시 |
| 허용 주장 | EMPIRICAL_ONLY인 곡선 재구성·실측으로 확인한 예측 범위와 실제 오차. 물리적 설명으로 포장하지 않음 | 근거가 확인된 가정/범위 안의 유도 및 제한적 물리 해석. 데이터가 지지하지 않는 재료상·고유 상수·범용 전이는 미확인 | 실제 통과한 재료/조건/관측량에 한정된 VALIDATED_FOR_DECLARED_SCOPE. 안전 인증·모든 전지·모든 조건의 참을 의미하지 않음 |
| 미달 시 상태 | 실패한 fit/없는 자료/비식별성을 명시; 성공한 다른 empirical 결과를 삭제하지 않음 | SOURCE_UNVERIFIED/DERIVATION_INCOMPLETE/CONDITIONAL 등 실제 부족한 축을 명시 | PRODUCTION_CANDIDATE_NOT_VALIDATED 또는 조건별 CONDITIONAL/FAIL; 다른 claim의 통과로 묻지 않음 |

세 열은 지금의 실제 후속 구현 파일명·namespace·default 또는 최종 Equation ID schema가 아니다.
관측 변환과 좌표·단위 검사를 empirical 층에서 면제하지 않는다.
Reduced 모델도 근거와 검증이 갖춰진 지정 범위에서 실용적으로 사용할 수 있다.
Production 모델도 정당한 reduced closure를 포함할 수 있으며 완전한 미시적 해상도를 강요하지 않는다.
어떤 이름이든 허용 주장의 범위는 사용된 가정·closure·자료·검증이 실제 지지하는 범위를 넘지 않는다.

## 근거 축을 분리한 판정 규칙

| 확인한 증거 | 그것으로 말할 수 있는 것 | 자동으로 말할 수 없는 것 |
|---|---|---|
| DOI/서지 record 존재 | 해당 서지의 실재성·metadata 확인 범위 | 원문의 특정 식·가정·재료 주장을 실제 읽고 지지했다는 결론 |
| 원문 exact anchor와 적용 변수·가정 대조 | 그 source가 지지하는 조건부 이론/관측 범위 | 구현 충실성, 현재 specimen의 물성, 모든 protocol의 검증 |
| 독립 유도·차원·부호·극한·보존 검사 | 정해진 가정 아래 식의 검산 범위 | 그 가정의 물질 타당성, 기전의 유일성 또는 데이터 fit |
| Synthetic/golden/internal conformance 검사 | 그 시험의 정의된 대수·구현·재구성 성질 | 실제 재료/held-out/primary-source 지지, 원래 historical optimizer state |
| 실제 in-sample 곡선과 R²/BIC | 원자료·잔차·비교 가정이 확인된 해당 적합도/모델 비교 | phase/gallery/성분 수, 고유 물성·기전·final model 선택 |
| Held-out 실제 관측량 예측 | 분리된 조건·시료와 평가 protocol에서 관찰된 예측 성능 | 관측만으로 구별되지 않는 hidden state/기전의 유일한 물리 해석 |
| 독립 구조·열역학·역학·열 자료와 식별성 | 해당 재료·조건에서 추가로 제한한 물리 해석 | 미측정 조성·도펀트·온도·rate·history로의 무조건 전이 |
| 성공 종료·convergence·bit-exact equality | 각각 실제 확인한 별개의 실행/수렴/동일성 성질 | 서로의 대체, 외부 과학 validation, 전체 suite의 무조건PASS |

R² 또는 naive BIC만으로 어느 층의 물리적 권위를 올리지 않는다. BIC/AIC의 잔차·likelihood·비교 가정,
상관/이분산·전처리 오차·식별성은081의 검토 사항으로 남긴다. 여기서는 새 통계 정리나 가짜 인용을 만들지 않는다.
원문이 없으면 SOURCE_UNVERIFIED이며 본문 load-bearing 근거로 사용하지 않는다.
내부 유도만 완성된 후보를 source-supported라고 부르지 않는다. 마찬가지로 수식은 맞지만 자료가 없으면 외부 검증 완료가 아니다.

## 계층 사이 이동 / 합성 조건

1. Empirical 성과는 원 데이터·전처리·basis·모수·실제 fit 범위와 함께 EMPIRICAL_ONLY로 보존한다.
   특정 분해가 잘 맞는 사실을 삭제하지 않되 그 component를 staging/phase/site 수로 재명명하지 않는다.
2. 물리 해석을 추가하려면 그 주장의 출발식·중간 유도·가정·domain·원문 exact anchor를 먼저 확보한다.
   기존 fit 함수에 물리적 이름을 붙이는 것으로 대체하지 않는다. 물리적 식과 관측 kernel은 대응을 따로 검증한다.
3. 원문/유도가 있어도 closure와 모수의 비식별성, 자료의 specimen/protocol 적합성, competing mechanisms를 분리해 남긴다.
   실제 자료가 없다고 임의 material parameter나 code-only default를 채우지 않는다.
4. 지정 운용 범위의 생산용 권위를 부여하려면 채택식–구현–시험 추적, conservation/limit/state checks,
   실제 calibration/held-out 검증과 불확도, 재현 조건이 모두 해당 주장에 대해 충족돼야 한다.
   실행 성공만으로 이 문장의 다른 요건을 대체하지 않는다.
5. 일부 하위 항이 empirical closure라면 그 역할·가정·보정 자료와 전이 범위를 드러낸다.
   합성 결과의 각 주장은 그 주장에 필요한 모든 의존 항의 근거 한계와 함께 전달한다.
   하나의 미검증 항을 전체에 숨기지도, 직접 관련 없는 독립 과학 결과까지 자동 기각하지도 않는다.
6. 적합도 우세는 기존 물리적 source의 오류 증명이 아니다. 상충하는 결과는 식/가정/좌표/자료 차이로 대조하고,
   정당한 대안은 ALTERNATIVE로 남긴다. 역사적 regsol 구현 삭제를 미래 자유에너지 후보의 영구 금지로 읽지 않는다.
7. 식의 부호·도메인 오류를 고치거나 경험적 항을 분리할 때 원래 claim/asset·변경 이유·대체 위치를 남긴다.
   이 단계에서는 frozen 원본/기존 완료 결과를 수정하지 않는다.

정당한 수치 오차 제어와 invalid domain/NaN/nonphysical input의 명시적 실패는 허용한다.
반면 결과의 물리적 의미를 조용히 바꾸는 cap/clip/clamp/softplus/threshold/grid guard/사후 smoothing은 금지한다.
필요한 regularization은 목적·bias·convergence·제거 극한을 명시하고, fixed grid가 물리 branch를 선택하지 않게 한다.
Adaptive error control/event detection/conservative integration/domain-preserving parameterization은 근거와 계약 아래 검토한다.
Default 검증 전에 값을 바꿔 시험을 통과시키지 않는다. Legacy bit-exact regression과 새 physics acceptance는 별도다.

## 현재 후보에 적용하는 권위 상한

| 현재 감사에서 확인한 대상 | 유지할 가치 / 현재 상한 | 아직 남는 조건 |
|---|---|---|
| 기존 logistic/skew/다성분 곡선 재구성 | 실제 자료·basis·범위가 확인된 empirical 능력; component 수는 phase 수 아님 | 관측·잔차·식별성, 재료/기전·held-out 근거 |
| Ideal/regular-solution 및 다른 자유에너지 후보 | 정확한 가정의 유도·대안 검토 대상, 최종 family/default 미선정 | 071 원문,074–082 독립 유도·적용 가능성, 재료별 closure |
| U13 고정 smooth kernel의 미분/정규화 | 감사가 구분한 고정 kernel·변수·구간의 제한된 수학적 결과 | 변화하는 kernel/동시 sharp limit 일반화 금지; source·재료 채택과 원고 수정 별개 |
| 066의14component/57parameter/12start fitting | 실제 실행 기록이 있으나 runtime_success=false 및 selected_trial_converged=false | 원 optimizer state/rawbinding, 실제 fitting 성공/수렴, 자료·외부 validation |
| 066의36 profile process 성공과 현재 runtime/curve 일치 | 해당 profile 생성 및 current IDENTICAL/TOLERANCE_EQUIVALENT 범위 | stored NOT_EQUIVALENT 및 original25statefields GROUND_NOT_FOUND를 대체하지 않음 |
| 068 prepared candidate51실행=49PASS+2historicalhashFAIL | 통과한 개별 conformance 성질과 실패 두 건을 각각 보존 | 전체 suitePASS/역사적 bit-exact 재현/물리적 채택으로 승격하지 않음 |
| 정적 call graph / 테스트·demo 기록 | 기록된 static 분석 및 실제 실행 cell별 상한 | C03 dynamic dispatch/runtime order, C06 required dual-runtime execution 또는 owner-bound withholding |
| 자료·문헌 미확보 material claim | UNVERIFIED/CONDITIONAL로 범위와 이유 유지 | 실제 원문·specimen/protocol·구조·열·역학·held-out 검증 |

위 표는 불변 audit의 기록을 현재 권위 분류에 연결한 것이다. 이번 Step102에서 원 optimizer, 수치과학,
기존 suite나 PDF를 재실행했다는 뜻이 아니다. 원래 원행/검증 결과의 세부 조건이 표보다 우선한다.
Graphite, doped high-voltage LCO, Si, SiOx, Si–C, graphite+Si blend 모두 같은 구분을 적용하되
서로 다른 재료의 실제 가정·반응·열·역학·자료 필요조건을 하나로 합치지 않는다. 구체 요구량은 Step103에서 다룬다.
Low-temperature/finite-current peak suppression 등은 특정 specimen/protocol에서 검증할 연구 관찰이지
모든 모델이 강제로 만족해야 할 보편 fit constraint가 아니다.

## 후속 문건과 구현 경계

071은 실제 source truth,072/103–104는 자료 조건/가능성,073은 이론 구조와 계층 역할,
074–082는 공통·재료 유도와 equation freeze,083은 이론–구현 계약,
084–085는 alpha·구조 고정,086은 실제 자료 평가,088은 독립 scientific red-team을 담당한다.
배치 기준은 Step101을 그대로 따른다. 이론·가정·유도·실험 한계는 학술 본문에,
API/file/code/test/실행 설명은 designated implementation appendix OR separate companion에 둔다.
변경 이력·Step/commit 감사 내용은 results/ledger이며 위 감사표를 학술 본문에 그대로 삽입하지 않는다.
모델 계층 분리나 machinecheck PASS로 원고/PDF/ZIP 또는 downstream science gate를 완료 처리하지 않는다.


## Historical Authority Evidence — 기록된 실행 범위의 재사용

위 표의 current IDENTICAL/TOLERANCE_EQUIVALENT는 Phase066 당시 재구성 런 사이의 저장된 비교다.
Step102에서 새로 optimizer/profile/suite를 실행한 결과가 아니다.
다른 two-parameter fit의 성공도 원래25statefields 또는 original historical optimum의 재현으로 대체하지 못한다.
아래 history/H44 추출은 원문 fullread를 다시 수행한 것으로 계수하지 않고, 기록된 selected fields와 immutable identity를 연결한다.
원C03/C06의 전체 조건은 index의 original_record를 계속 정본으로 두며 아래 추출에서 빠진 다른 원필드도 삭제하지 않는다.

```json
{
  "schema": "phase069.step102.history-authority-review.v1",
  "role": "history/H44",
  "scope": "Compact extraction of historical fit/runtime/convergence/reproduction/conformance/external-authority boundaries only; not a hierarchy-document approval or new scientific validation.",
  "input_base": "76b07667085c0d1d886b667ce2b490b40470af7a",
  "read_coverage": [
    {
      "path": "Codex/results/PHASE_069_STEP_102_MODEL_HIERARCHY_RESULT.md",
      "mode": "FRESH_FULL_TEXT_CURRENT_WIP",
      "ranges": [
        [
          1,
          108
        ]
      ],
      "bytes": 5050,
      "sha256": "1f4380ef98347a190dff18a00621b9cc94be998fe010f6e805247e5d1f1781c2",
      "limit": "IN_PROGRESS input-manifest snapshot only; root will subsequently author the result."
    },
    {
      "path": "Codex/plans/2026-09-08-phase069-canonical-audit-launch-detailed-plan.md",
      "mode": "FRESH_FULL_TEXT",
      "ranges": [
        [
          1,
          245
        ]
      ],
      "blob": "81620a8b58948d4823dc47e5058a65195bab9e77",
      "sha256": "8316e3287e093259841d33213fed7ac63481e6c42d0e9791828f102e114f2f3d",
      "application": "Step102 authority dimensions and scope; designated implementation appendix OR separate companion exception preserved."
    },
    {
      "path": "Codex/results/PHASE_069_CANONICAL_AUDIT_INDEX.json",
      "commit": "76b07667085c0d1d886b667ce2b490b40470af7a",
      "blob": "c0e8ef979469eee14e16b0b13c9b9e2f4ea83b89",
      "mode": "FRESH_SELECTED_FIELDS_FROM_IMMUTABLE_GIT_SHOW",
      "selectors": [
        "phases[phase=66].{canonical_report,validation,recorded_gate,current_interpretation,retained_content}",
        "phases[phase=66].recorded_validation_fields.{fit,optimizer,authority_ceiling,exclusive_gate,ref7}",
        "phases[phase=67].{canonical_report,validation,recorded_gate}",
        "phases[phase=67].recorded_validation_fields.{canonical_evidence_reuse,authority_boundary,gate_evaluation,coverage_summary.test_runtime_outcomes}",
        "phases[phase=68].{canonical_report,validation,recorded_gate,retained_content,current_interpretation,recorded_validation_fields.scientific_authority}",
        "unindexed_existing_conditions[0:2] every field"
      ],
      "limit": "Not fresh full index, requirements, all carry, raw science, PDF or runtime reading."
    },
    {
      "path": "Codex/results/PHASE_066_RESULT.md",
      "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
      "blob": "362dc96b93a198ef66ec9985648111781f1ac175",
      "mode": "PRIOR_PERSONAL_STEP99_FULL_READ_REUSED",
      "ranges": [
        [
          1,
          85
        ]
      ]
    },
    {
      "path": "Codex/results/PHASE_067_RESULT.md",
      "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
      "blob": "4981e37937792f34de5b2337c9f64f34b1559d6e",
      "mode": "PRIOR_PERSONAL_STEP99_FULL_READ_REUSED",
      "ranges": [
        [
          1,
          93
        ]
      ]
    },
    {
      "path": "Codex/results/PHASE_068_RESULT.md",
      "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
      "blob": "f1335d16ccad071dcbfdeff5fd0b0b4ada8f3c34",
      "mode": "PRIOR_PERSONAL_STEP99_FULL_READ_REUSED",
      "ranges": [
        [
          1,
          32
        ]
      ]
    },
    {
      "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
      "path": "Codex/results/PHASE_066_VALIDATION.json",
      "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
      "selector": "/integrated_assertions/{fit,optimizer,runtime,profile,authority,exclusive_gate,ref7}; /authority_ceiling",
      "mode": "PRIOR_PERSONAL_SELECTED_FIELD_READ_REUSED_NOT_FRESH_RAW_SOURCE"
    },
    {
      "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
      "path": "Codex/results/PHASE_067_VALIDATION.json",
      "blob": "cddf1d49c54418c29e74ab67c8b5780da077115d",
      "selector": "/conformance_rows/2; /conformance_rows/5; /authority_boundary; /canonical_evidence_reuse; /coverage_summary; /gate_evaluation",
      "mode": "PRIOR_PERSONAL_SELECTED_FIELD_READ_REUSED_NOT_FRESH_RAW_SOURCE"
    },
    {
      "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
      "path": "Codex/results/PHASE_068_VALIDATION.json",
      "blob": "0317468ba71094430e3beb698df6830fce72c8ce",
      "selector": "/gate_predicates/7; /scientific_authority; /unresolved",
      "mode": "PRIOR_PERSONAL_SELECTED_FIELD_READ_REUSED_NOT_FRESH_RAW_SOURCE",
      "limit": "Gate8 evidence links point to original Step95 runs; their raw runs are not reopened in Step102."
    }
  ],
  "identity_reuse_check": {
    "index_matches_manifest": true,
    "validation66_identity": true,
    "validation67_identity": true,
    "validation68_identity": true,
    "fit": true,
    "optimizer": true,
    "C03_C06": [
      {
        "id": "C03",
        "exact_original_row": true
      },
      {
        "id": "C06",
        "exact_original_row": true
      }
    ]
  },
  "conditions": [
    {
      "distinction": "Historical fit success",
      "allowed": "A named historical result may retain its actual bounded empirical fit statement and source-provenance ceiling.",
      "not_allowed": "A saved curve, displayed parameters, R2/BIC, a separate two-parameter fit or a newer successful process does not prove the historical optimizer converged or recreate its unavailable original state.",
      "evidence": [
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/integrated_assertions/fit"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/integrated_assertions/optimizer"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_068_VALIDATION.json",
          "blob": "0317468ba71094430e3beb698df6830fce72c8ce",
          "selector": "/gate_predicates/7"
        }
      ],
      "current_facts": "Do not invent an original successful/converged direct14 run from the reconstructed Phase066 execution; original25statefields remain GROUND_NOT_FOUND."
    },
    {
      "distinction": "Current runtime execution and process success",
      "allowed": "Attribute each observed exit/success to its named process, runtime and historical execution interval. The Phase066 reconstruction's word current refers to that recorded comparison, not a fresh Step102 run.",
      "not_allowed": "optimizer_execution_complete=true is not runtime_success=true; 36 successful profile processes are not 36 successful optimizer fits. Missing dependencies/manual observations are not passing tests.",
      "evidence": [
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/integrated_assertions/fit"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/integrated_assertions/runtime"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/integrated_assertions/profile"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_067_VALIDATION.json",
          "blob": "cddf1d49c54418c29e74ab67c8b5780da077115d",
          "selector": "/coverage_summary/test_runtime_outcomes"
        }
      ],
      "current_facts": {
        "fit": {
          "components": 14,
          "parameters": 57,
          "starts": 12,
          "optimizer_execution_complete": true,
          "runtime_success": false,
          "selected_trial_converged": false
        },
        "profile_processes": 36,
        "profile_process_successes": 36,
        "profile_routes": {
          "total": 16,
          "temperature_dependent": 9,
          "temperature_independent": 7
        },
        "phase067_runtime_outcomes": {
          "DEPENDENCY_MISSING": 34,
          "FAIL_EXIT_GATE": 5,
          "MANUAL_OBSERVATION": 38,
          "PASS_EXIT_GATE": 33
        }
      }
    },
    {
      "distinction": "Convergence",
      "allowed": "Keep the recorded solver convergence diagnostic separate from execution completion, curve agreement and returned values.",
      "not_allowed": "The Phase06612-start run cannot be called converged or a successfully recovered optimum: selected_trial_converged=false and runtime_success=false. Even a genuine convergence flag would not by itself prove material/phase identity or external predictive validity.",
      "evidence": [
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/integrated_assertions/fit"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_067_VALIDATION.json",
          "blob": "cddf1d49c54418c29e74ab67c8b5780da077115d",
          "selector": "/gate_evaluation"
        }
      ],
      "current_facts": "Phase067 C14 exhaustion/state obligation also remains active; no fresh fix or rerun was performed."
    },
    {
      "distinction": "Exact historical state reproduction",
      "allowed": "State precisely which existing comparison was established: current reconstruction cross-runtime IDENTICAL, curve TOLERANCE_EQUIVALENT, stored replay NOT_EQUIVALENT.",
      "not_allowed": "IDENTICAL across two current reconstructions does not imply equality with the historical saved run. Tolerance-equivalent curve output is not bitwise/full-state equivalence. Do not fabricate any of the25 missing original state fields or replace their existing acceptance with a different reduced fit.",
      "evidence": [
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/integrated_assertions/optimizer"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/authority_ceiling"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_068_VALIDATION.json",
          "blob": "0317468ba71094430e3beb698df6830fce72c8ce",
          "selector": "/gate_predicates/7"
        }
      ],
      "current_facts": {
        "cross_runtime": "IDENTICAL",
        "curve": "TOLERANCE_EQUIVALENT",
        "original_state_fields": 25,
        "original_state_status": "GROUND_NOT_FOUND",
        "stored_replay": "NOT_EQUIVALENT"
      }
    },
    {
      "distinction": "Internal conformance and suite status",
      "allowed": "Use exact formula/unit/API/conservation/limit/domain checks and individual test outcomes only for their declared internal assumptions and evidence axes; retain whole-suite and per-test status separately.",
      "not_allowed": "Prepared51executed49PASS+2historical-hashFAIL, suiteexit1 per prepared runtime, is not suitePASS. Phase068 gate8PASS means coverage/adjudication, not candidate adoption or material validation. The two hash failures remain unresolved; no root cause is inferred here.",
      "evidence": [
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_068_VALIDATION.json",
          "blob": "0317468ba71094430e3beb698df6830fce72c8ce",
          "selector": "/gate_predicates/7"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_067_VALIDATION.json",
          "blob": "cddf1d49c54418c29e74ab67c8b5780da077115d",
          "selector": "/gate_evaluation"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_067_VALIDATION.json",
          "blob": "cddf1d49c54418c29e74ab67c8b5780da077115d",
          "selector": "/conformance_rows/2"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_067_VALIDATION.json",
          "blob": "cddf1d49c54418c29e74ab67c8b5780da077115d",
          "selector": "/conformance_rows/5"
        }
      ],
      "current_facts": "C03 actual dynamic/runtime-order proof and C06 required test/demo runtime-cell evidence remain partial; source static coverage and successful collection cannot close either."
    },
    {
      "distinction": "External protocol/material validation",
      "allowed": "Preserve claim/material/protocol-scoped source, specimen/data, held-out and identifiability requirements from the approved hierarchy plan and original conditional records.",
      "not_allowed": "Internal tests, synthetic recovery, empirical curve agreement, successful process execution, solver convergence or exact replication cannot alone promote empirical fit to source-supported reduced physics or externally validated production physics.",
      "evidence": [
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/integrated_assertions/authority"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_066_VALIDATION.json",
          "blob": "2a2a5fcec65730b928b8a1bbeb0ab0b488574cba",
          "selector": "/integrated_assertions/exclusive_gate/conditional_conditions"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_067_VALIDATION.json",
          "blob": "cddf1d49c54418c29e74ab67c8b5780da077115d",
          "selector": "/authority_boundary"
        },
        {
          "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
          "path": "Codex/results/PHASE_068_VALIDATION.json",
          "blob": "0317468ba71094430e3beb698df6830fce72c8ce",
          "selector": "/scientific_authority"
        }
      ],
      "current_facts": "Eight Phase066 authority rows retain one empirical PASS butzero physical/phase/external/proposition promotion; six heldout NOT_TESTED andone primary-text GROUND_NOT_FOUND. Ref7 fulltext, raw/preprocess exactbinding, original optimizer, specimen/protocol/material, stalePDF and external debts remain."
    }
  ],
  "preserved_unindexed_conditions": [
    {
      "source": {
        "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
        "path": "Codex/results/PHASE_067_VALIDATION.json",
        "blob": "cddf1d49c54418c29e74ab67c8b5780da077115d",
        "selector": "conformance_rows[row_id=C03]",
        "exact_array_pointer": "/conformance_rows/2"
      },
      "row_id": "C03",
      "status": "PARTIAL",
      "owner": "PHASE-083-IMPLEMENTATION-CONTRACT",
      "acceptance_criterion": "DIRECT_RUNTIME_CALL_ORDER_AND_DYNAMIC_DISPATCH_EVIDENCE_FOR_NAMED_PHYSICS_ROUTES",
      "authority_ceiling": "SOURCE_STATIC_GRAPH; 80 DYNAMIC EDGES AND RUNTIME ORDER UNPROVEN",
      "required_internal_axes": [
        "theory_code",
        "code_test"
      ],
      "axes": {
        "code_test": "NOT_TESTED",
        "test_data": "NOT_APPLICABLE",
        "theory_code": "PARTIAL",
        "theory_data": "NOT_APPLICABLE"
      },
      "obligation_ids": [],
      "origin": {
        "path": "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json",
        "pointer": "/authority/actual_runtime_order_proven",
        "record_sha256": "2ed27c1421e6928dbe13dbfdb5c59e1045b30341fe7ebe05700006bc5ac572c0"
      },
      "supporting_origins": [
        {
          "path": "Codex/results/PHASE_067_PHYSICS_CALL_GRAPH.json",
          "pointer": "/coverage/dynamic_edges",
          "record_sha256": "95aebc97bc646c67fdcd923a5965b001f3c8a5c4d3a77075112e12a3a311d760"
        }
      ],
      "current_carry_route": "EXACT_ROUTE_NOT_FOUND",
      "resolution_required": "Keep exact existing owner/acceptance/authority, determine precise launch-input mapping inStep105 and gate106/107. Do not substitute narrower similarly-owned carry or close this predicate."
    },
    {
      "source": {
        "commit": "04ed9c209794f31cde9aa41d8b94accfb56515ca",
        "path": "Codex/results/PHASE_067_VALIDATION.json",
        "blob": "cddf1d49c54418c29e74ab67c8b5780da077115d",
        "selector": "conformance_rows[row_id=C06]",
        "exact_array_pointer": "/conformance_rows/5"
      },
      "row_id": "C06",
      "status": "PARTIAL",
      "owner": "PHASE-088-SCIENTIFIC-REDTEAM",
      "acceptance_criterion": "REQUIRED_PHASE067_TEST_AND_DEMO_RUNTIME_CELLS_EXECUTE_UNDER_BOTH_RUNTIMES_OR_REMAIN_EXPLICITLY_WITHHELD_WITH_OWNER",
      "authority_ceiling": "33 PASS_EXIT_GATE; 5 FAIL_EXIT_GATE; 34 DEPENDENCY_MISSING; 38 MANUAL_OBSERVATION",
      "required_internal_axes": [
        "code_test",
        "test_data"
      ],
      "axes": {
        "code_test": "PARTIAL",
        "test_data": "PARTIAL",
        "theory_code": "NOT_APPLICABLE",
        "theory_data": "NOT_APPLICABLE"
      },
      "obligation_ids": [],
      "origin": {
        "path": "Codex/results/PHASE_067_TEST_DEMO_GOLDEN_MATRIX.json",
        "pointer": "/runtime_records",
        "record_sha256": "45673d528eaa826d4f1876ef67d09d8c0ec41d7e757f357b263b48a8cfd0a267"
      },
      "supporting_origins": [],
      "current_carry_route": "EXACT_ROUTE_NOT_FOUND",
      "resolution_required": "Keep exact existing owner/acceptance/authority, determine precise launch-input mapping inStep105 and gate106/107. Do not substitute narrower similarly-owned carry or close this predicate."
    }
  ],
  "unresolved_boundary": "316registered active carry and655dispositions remain unchanged, zero inherited closure. C03/C06 are pre-existing broad source conditions with no verified exact316route, not two new IDs or proof of318disjoint obligations. Carry selection belongs to the other assigned reviewer; no new mapping is proposed.",
  "checks": {
    "native_index_identity_command": "git rev-parse 76b07667085c0d1d886b667ce2b490b40470af7a:Codex/results/PHASE_069_CANONICAL_AUDIT_INDEX.json",
    "native_index_read_command": "git show 76b07667085c0d1d886b667ce2b490b40470af7a:Codex/results/PHASE_069_CANONICAL_AUDIT_INDEX.json",
    "outer_powershell_exit": 0,
    "stream_basis": "Native JSON parsed and only selected fields returned through combined exec_command output; no separate native stderr claim.",
    "original_scientific_execution_count": 0,
    "network_count": 0,
    "repository_writes": 0
  },
  "remaining_findings": {
    "P0": 0,
    "P1": 0,
    "P2": 0
  },
  "limitations": [
    "Extraction of existing evidence boundaries only; root's new hierarchy document has not been reviewed here.",
    "Prior 개인 full reads and exact immutable source identities are reused, not newly recounted. Current10manifest descriptors were read but unassigned ten full source bodies were not all read.",
    "No new external source/DOI/fulltext/data/heldout/optimizer/reproduction proof, code changes, tests, PDF review, ledger audit, source adoption or scientific closure.",
    "Step106wholecoverage and107launch remain unexecuted/unselected. Root-provided Step101persistence is not independently rerun by this reviewer."
  ]
}
```

## Source-native Carry Evidence — 선별된 의무의 보존

직접 관련59=47inherited+12new 의무를 아래에 원 ID/owner/phase/state/acceptance/관계와 연결했다.
선별 상태는56 OPEN_CARRY,2 OPEN_CARRY_EXPLICITLY_BOUNDED_P067,1 PRESERVED_ACTIVE이며 서로 바꾸지 않는다.
나머지257는 관련이 없거나 해소됐다는 뜻이 아니라 전체316의 immutable pointer를 따라 계속 보존된다.
등록316=222inherited+94new,655dispositions, inheritedclosure0을 변경하지 않는다.
C03/C06 원 source predicates는 Step105에서 연결하며 새 ID 또는318개 독립 의무로 바꾸지 않는다.

아래 semantic_source.meaning은 원천의 설명 또는 검증 대상인 원래 주장이다.
특히 단정형으로 적힌 fit→phase/material/current partition 문장을 이번 Step의 과학적 확정으로 읽지 않는다.
권위 판정은 위 계층 계약과 원 current_record.acceptance_criterion/원 source의 미결 조건을 함께 따른다.
원 의미와 원 acceptance를 보존하는 것은 해당 주장을 사실로 승인하는 행위가 아니다.

Source/carry 역할 export의 최종 raw identity:138355bytes/2883lines,
SHA2568fa9fb6570bed7dd485b6e7b58aad810465710bdddf176b86baf5027d19b0003.
아래 JSON은 모든 필드/배열/값을 보존한 논리적 동일 복사이며 줄바꿈·들여쓰기만 compact하게 표현한다.
Root는 모든 metadata와 selected0–58의 모든 필드를 구간별로 직접 읽었다.
이는 export의 전체 논리 필드 검독이며 원문 science/PDF 또는316전체의 새 전문 검독이 아니다.

artifact_identities의 raw bytes/SHA는 당시 working bytes, commit/blob은 native Git object를 가리킨다.
057provisionalledger와 Codex/AGENTS.md는 working CRLF를 LF로 정규화해야 Git bytes와 일치한다.
066carry는 실제 확인상 working/native가 동일 LF다. 아래 WIP result179line identity는 이전 draft snapshot이지 최종result hash가 아니다.
원천 비교의 정본은 native Git blob이며 raw-working 수치를 GitLF SHA로 잘못 비교하지 않는다.

```json
{
  "schema": "anode-step102-authority-carry-review-v1",
  "review_state": "COMPLETE_BOUNDED_SELECTION_NO_CLOSURE",
  "base_commit": "76b07667085c0d1d886b667ce2b490b40470af7a",
  "scope_guard": {
    "included": "Only active obligations whose source meaning explicitly constrains empirical/reduced/production-physics authority, fit/model-selection inference, conformance-vs-physical-validity, or independent-evidence scope.",
    "excluded": "No all-material/DOI sweep, optimizer/history reconstruction, source/PDF/code replay, scientific recalculation, new obligation, re-owner, closure, or claim that schema validation proves prose truth.",
    "authority_effect": "Pointers and source-native acceptance are preserved; selection does not satisfy or close any obligation."
  },
  "artifact_identities": {
    "Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json": {
      "path": "Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json",
      "bytes": 503096,
      "physical_lines": 12740,
      "raw_sha256": "768026e729c946cd0785883c8a80cb760941f7ed4e932cd7b8f889ebae806e03",
      "commit": "76b07667085c0d1d886b667ce2b490b40470af7a",
      "blob": "7d41aca4984c15bdb6161059994bdf3586ecdd76",
      "mode": "100644"
    },
    "Codex/results/PHASE_068_FORK_DISPOSITION_REGISTER.json": {
      "path": "Codex/results/PHASE_068_FORK_DISPOSITION_REGISTER.json",
      "bytes": 1596173,
      "physical_lines": 21000,
      "raw_sha256": "79cfc14cb4839d0a8dd2134eeeeab14f7a27784e9a4878a57a8767ecceb088cc",
      "commit": "76b07667085c0d1d886b667ce2b490b40470af7a",
      "blob": "70d20f2b02679a7b3fb4cf29ce98902dae839ef7",
      "mode": "100644"
    },
    "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json": {
      "path": "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json",
      "bytes": 572004,
      "physical_lines": 6496,
      "raw_sha256": "94f418a4207524c980ec73dcc70e978347e99bcfceeebf8051865e91849f7d4f",
      "commit": "76b07667085c0d1d886b667ce2b490b40470af7a",
      "blob": "e4000c331979a1f550d099a06712225829fafd32",
      "mode": "100644"
    },
    "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json": {
      "path": "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json",
      "bytes": 867754,
      "physical_lines": 19114,
      "raw_sha256": "847e74956d16cc9bdcc42c36b0ddd1d73ea5ac79464d55461d2e08cf09a60003",
      "commit": "76b07667085c0d1d886b667ce2b490b40470af7a",
      "blob": "6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95",
      "mode": "100644"
    },
    "Codex/results/PHASE_069_USER_REQUIREMENTS.json": {
      "path": "Codex/results/PHASE_069_USER_REQUIREMENTS.json",
      "bytes": 174137,
      "physical_lines": 4261,
      "raw_sha256": "16e4df4c626d0d5e8417e5397c2024914809d6a87139efa68c15b1156e382f87",
      "commit": "76b07667085c0d1d886b667ce2b490b40470af7a",
      "blob": "bc76d7c23032b1961ee4c9d99cf038d931310f0e",
      "mode": "100644"
    },
    "Codex/plans/2026-09-08-phase069-canonical-audit-launch-detailed-plan.md": {
      "path": "Codex/plans/2026-09-08-phase069-canonical-audit-launch-detailed-plan.md",
      "bytes": 18273,
      "physical_lines": 245,
      "raw_sha256": "8316e3287e093259841d33213fed7ac63481e6c42d0e9791828f102e114f2f3d",
      "commit": "76b07667085c0d1d886b667ce2b490b40470af7a",
      "blob": "81620a8b58948d4823dc47e5058a65195bab9e77",
      "mode": "100644"
    },
    "Codex/AGENTS.md": {
      "path": "Codex/AGENTS.md",
      "bytes": 14046,
      "physical_lines": 180,
      "raw_sha256": "a471c7cf6c5591639a3695891f6bec48164c2f7a5ac78654e71af4d0bef7a232",
      "commit": "76b07667085c0d1d886b667ce2b490b40470af7a",
      "blob": "68218ce741a9a85b75323853f1d6f3ac3dc102e7",
      "mode": "100644"
    },
    "Codex/results/PHASE_069_STEP_102_MODEL_HIERARCHY_RESULT.md": {
      "path": "Codex/results/PHASE_069_STEP_102_MODEL_HIERARCHY_RESULT.md",
      "bytes": 12022,
      "physical_lines": 179,
      "raw_sha256": "0341d9e3d3855ef502780f4d0c544818b88b4fe703c7158d13d700d83d56b925",
      "read_type": "CURRENT_WORKTREE_DRAFT_FULL_READ"
    }
  },
  "read_coverage": {
    "fresh_full_read": [
      {
        "path": "Codex/results/PHASE_069_STEP_102_MODEL_HIERARCHY_RESULT.md",
        "lines": "1-179",
        "bytes": 12022,
        "raw_sha256": "0341d9e3d3855ef502780f4d0c544818b88b4fe703c7158d13d700d83d56b925",
        "note": "Current root-authored worktree draft read byte 0 through EOF after the 179-line expansion; input manifest lines 12-98 checked."
      }
    ],
    "fresh_targeted_structured_read": [
      {
        "path": "Codex/results/PHASE_069_USER_REQUIREMENTS.json",
        "selectors": [
          "/requirements/17",
          "/requirements/18",
          "/requirements/19",
          "/requirements/20",
          "/requirements/21"
        ],
        "records": 5,
        "all_fields_each": true
      },
      {
        "path": "Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json",
        "selectors": [
          "/inherited_active/10",
          "/inherited_active/11",
          "/inherited_active/12",
          "/inherited_active/14",
          "/inherited_active/15",
          "/inherited_active/16",
          "/inherited_active/52",
          "/inherited_active/53",
          "/inherited_active/54",
          "/inherited_active/63",
          "/inherited_active/78",
          "/inherited_active/83",
          "/inherited_active/85",
          "/inherited_active/86",
          "/inherited_active/87",
          "/inherited_active/88",
          "/inherited_active/95",
          "/inherited_active/96",
          "/inherited_active/97",
          "/inherited_active/106",
          "/inherited_active/108",
          "/inherited_active/110",
          "/inherited_active/113",
          "/inherited_active/121",
          "/inherited_active/133",
          "/inherited_active/134",
          "/inherited_active/137",
          "/inherited_active/138",
          "/inherited_active/141",
          "/inherited_active/142",
          "/inherited_active/147",
          "/inherited_active/148",
          "/inherited_active/152",
          "/inherited_active/156",
          "/inherited_active/158",
          "/inherited_active/159",
          "/inherited_active/160",
          "/inherited_active/166",
          "/inherited_active/169",
          "/inherited_active/172",
          "/inherited_active/176",
          "/inherited_active/208",
          "/inherited_active/209",
          "/inherited_active/210",
          "/inherited_active/211",
          "/inherited_active/212",
          "/inherited_active/213",
          "/new_obligations/7",
          "/new_obligations/8",
          "/new_obligations/16",
          "/new_obligations/19",
          "/new_obligations/29",
          "/new_obligations/31",
          "/new_obligations/33",
          "/new_obligations/35",
          "/new_obligations/43",
          "/new_obligations/45",
          "/new_obligations/56",
          "/new_obligations/64"
        ],
        "records": 59,
        "all_fields_each": true
      },
      {
        "path": "Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json",
        "selectors": [
          "/records/396",
          "/records/397",
          "/records/398",
          "/records/400",
          "/records/401",
          "/records/402",
          "/records/293",
          "/records/294",
          "/records/295",
          "/records/305",
          "/records/307",
          "/records/309",
          "/records/312",
          "/records/321",
          "/records/336",
          "/records/337",
          "/records/340",
          "/records/341",
          "/records/345",
          "/records/346",
          "/records/352",
          "/records/355",
          "/records/359",
          "/records/364",
          "/records/366",
          "/records/367",
          "/records/368",
          "/records/374",
          "/records/378",
          "/records/381",
          "/records/386"
        ],
        "records": 31,
        "all_fields_each": true
      },
      {
        "path": "Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json",
        "selectors": [
          "/inherited_phase065_observations/141",
          "/inherited_phase065_observations/142",
          "/inherited_phase065_observations/145",
          "/inherited_phase065_observations/156",
          "/inherited_phase065_observations/175",
          "/inherited_phase065_observations/181",
          "/inherited_phase065_observations/183",
          "/inherited_phase065_observations/184",
          "/inherited_phase065_observations/185",
          "/inherited_phase065_observations/186",
          "/step76_80_disposition_records/36",
          "/step76_80_disposition_records/37",
          "/step76_80_disposition_records/38",
          "/step76_80_disposition_records/39",
          "/step76_80_disposition_records/40",
          "/step76_80_disposition_records/41"
        ],
        "records": 16,
        "all_fields_each": true
      },
      {
        "path": "Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json",
        "selector_family": "/target_routes/* for selected P068 origin_target_ids",
        "records": 38,
        "all_fields_each": true
      }
    ],
    "reused_prior_full_reads_after_current_identity_check": [
      {
        "path": "Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json",
        "prior_scope": "222 inherited + 94 new = 316 active rows; full fields previously read in Step97/Step101 role",
        "current_blob": "7d41aca4984c15bdb6161059994bdf3586ecdd76",
        "current_raw_sha256": "768026e729c946cd0785883c8a80cb760941f7ed4e932cd7b8f889ebae806e03",
        "fresh_claim_this_step": false
      },
      {
        "path": "Codex/results/PHASE_068_FORK_DISPOSITION_REGISTER.json",
        "prior_scope": "655 disposition rows/full fields previously read in Step97 role",
        "current_blob": "70d20f2b02679a7b3fb4cf29ce98902dae839ef7",
        "current_raw_sha256": "79cfc14cb4839d0a8dd2134eeeeab14f7a27784e9a4878a57a8767ecceb088cc",
        "fresh_claim_this_step": false
      },
      {
        "path": "Codex/AGENTS.md",
        "prior_scope": "full 1-180",
        "current_blob": "68218ce741a9a85b75323853f1d6f3ac3dc102e7",
        "current_raw_sha256": "a471c7cf6c5591639a3695891f6bec48164c2f7a5ac78654e71af4d0bef7a232",
        "fresh_claim_this_step": false
      },
      {
        "path": "Codex/plans/2026-09-08-phase069-canonical-audit-launch-detailed-plan.md",
        "prior_scope": "full 1-245 including Step102 lines 177-179",
        "current_blob": "81620a8b58948d4823dc47e5058a65195bab9e77",
        "current_raw_sha256": "8316e3287e093259841d33213fed7ac63481e6c42d0e9791828f102e114f2f3d",
        "fresh_claim_this_step": false
      }
    ]
  },
  "requirement_predicates": [
    {
      "id": "P069-REQ-018",
      "selector": "/requirements/17",
      "canonical_record_sha256": "8a8fed1dad293d328be0157e5ba41ba42ef1501f5b4b82372e787b928b583ae7",
      "title": "실제 피팅 가치와 모델 계층",
      "status": "REQUIRED_NOT_YET_SATISFIED",
      "authority_ceiling": "Requirement formalization only; no model adoption, source truth, material validation, scientific closure or new carry-obligation ID."
    },
    {
      "id": "P069-REQ-019",
      "selector": "/requirements/18",
      "canonical_record_sha256": "3f3dea77d1e0dbfb1182b173511ce42db3e24986e54db5603b88e16cad9d2b09",
      "title": "실제 자료·provenance와 부족한 근거",
      "status": "REQUIRED_NOT_YET_SATISFIED",
      "authority_ceiling": "Requirement formalization only; no model adoption, source truth, material validation, scientific closure or new carry-obligation ID."
    },
    {
      "id": "P069-REQ-020",
      "selector": "/requirements/19",
      "canonical_record_sha256": "56dd07d338a7f92ce80e3289d98c51ce4a2f5ba17afe9298fcd6499ea81f6ddb",
      "title": "식별성·불확도와 독립 검증",
      "status": "REQUIRED_NOT_YET_SATISFIED",
      "authority_ceiling": "Requirement formalization only; no model adoption, source truth, material validation, scientific closure or new carry-obligation ID."
    },
    {
      "id": "P069-REQ-021",
      "selector": "/requirements/20",
      "canonical_record_sha256": "994252ddcfcd4bc13d9b282e2365ccbfea0c8adea64784a25517f70114789b84",
      "title": "정당한 수치 방법과 숨은 조작 금지",
      "status": "REQUIRED_NOT_YET_SATISFIED",
      "authority_ceiling": "Requirement formalization only; no model adoption, source truth, material validation, scientific closure or new carry-obligation ID."
    },
    {
      "id": "P069-REQ-022",
      "selector": "/requirements/21",
      "canonical_record_sha256": "75396921efc25b6e0de6c90147bdcaa58bb0ee868bd085debe994d6f425fc13b",
      "title": "진짜 문헌과 load-bearing 근거",
      "status": "REQUIRED_NOT_YET_SATISFIED",
      "authority_ceiling": "Requirement formalization only; no model adoption, source truth, material validation, scientific closure or new carry-obligation ID."
    }
  ],
  "inherited_state": {
    "active_total": 316,
    "inherited": 222,
    "new": 94,
    "closed_inherited": 0,
    "register_rows": 655,
    "atomic_scientific_denominator_claimed": false,
    "C03_C06": "No exact route in the 316 was found in the prior carry review; preserve original Phase083/Phase088 owner and acceptance through Step105. Do not infer 318 or mint an ID."
  },
  "selection_summary": {
    "selected_total": 59,
    "by_prefix": {
      "P065": 16,
      "P066": 31,
      "P068": 12
    },
    "by_reason": {
      "CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY": 9,
      "EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY": 21,
      "FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL": 17,
      "PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE": 12
    },
    "selected_ids_sha256": "873d2ff0740dcd6a3db6f3c352077d524e3e0c4bb697a3b23cbe3ae6a7504253"
  },
  "selected_obligations": [
    {"obligation_id":"P065-OBL-0011","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/10"},"canonical_record_sha256":"d4b607f71ae3c7d03e37831a192122803f4b996db32e61a4206d6afc4b4e17c3","canonical_owner":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION","target_phase":81,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION must resolve or explicitly bound the exact observation without backward-projecting later evidence into v1.0.24.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/396"},"canonical_record_sha256":"1b975a27f7aa684c05c9198a1b2e17c613a99d62550b9c9cc42505e272a551da","source_id":"INTENT-PROV-0397","meaning":"현재 BIC는 강한 순위 신호지만 정식 model evidence로 쓸 수 없다","source_path":"Codex/results/PHASE_057AY_V1024_SNAPSHOT_V1025_2_KERNEL_REPORT_OBSERVATIONS.md","source_lines":[89,107],"source_block_sha256":"8b18d27f069eda3996471bdffb02042b8268ccf9865e681194feec76c965912c"}},
    {"obligation_id":"P065-OBL-0012","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/11"},"canonical_record_sha256":"ac935fd4c9152c86a17dbe0a075c73d274e6518e14d5094b70617b1a1aeda6c5","canonical_owner":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION","target_phase":81,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION must resolve or explicitly bound the exact observation without backward-projecting later evidence into v1.0.24.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/397"},"canonical_record_sha256":"66ac47982259cb74e85f63758765c0aad9b894b4197047e3254307abc15fc469","source_id":"INTENT-PROV-0398","meaning":"A 대 B 비교는 kernel만의 비교가 아니다","source_path":"Codex/results/PHASE_057AY_V1024_SNAPSHOT_V1025_2_KERNEL_REPORT_OBSERVATIONS.md","source_lines":[108,123],"source_block_sha256":"9341b978d83af1b1a5a5fd5dc6838ef241fa5c25aa5c91d1c25557eed78ce32e"}},
    {"obligation_id":"P065-OBL-0013","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/12"},"canonical_record_sha256":"e1ce842b1e8a9ba1152bbc30a27b07440605131d736b16fcd9a0020dcb919007","canonical_owner":"PHASE-077-GRAPHITE-CLOSURE","target_phase":77,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-077-GRAPHITE-CLOSURE must resolve or explicitly bound the exact observation without backward-projecting later evidence into v1.0.24.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/398"},"canonical_record_sha256":"c608aa56571554d3b014d522133fde44f948d808883b73dc0113390247f573be","source_id":"INTENT-PROV-0399","meaning":"C의 우세는 α의 물리적 식별을 뜻하지 않는다","source_path":"Codex/results/PHASE_057AY_V1024_SNAPSHOT_V1025_2_KERNEL_REPORT_OBSERVATIONS.md","source_lines":[124,145],"source_block_sha256":"d9d54f6d64cd0df0c20f5d612ace91e19d01375b787ea5481e21916b4847c76f"}},
    {"obligation_id":"P065-OBL-0015","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/14"},"canonical_record_sha256":"a092518c36babe84260c2f3e490cf25bf679f97c41281eeb5c7697b411559efa","canonical_owner":"PHASE-075-EQUILIBRIUM-PHASE","target_phase":75,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-075-EQUILIBRIUM-PHASE must resolve or explicitly bound the exact observation without backward-projecting later evidence into v1.0.24.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/400"},"canonical_record_sha256":"5b44a89dc396dede2496e24445a46c51cf85343f5cb4ac7fe0f8eeb4b950a059","source_id":"INTENT-PROV-0401","meaning":"fitted Ω/RT로 “흑연은 두-상”을 확정한 논리는 성립하지 않는다","source_path":"Codex/results/PHASE_057AY_V1024_SNAPSHOT_V1025_2_KERNEL_REPORT_OBSERVATIONS.md","source_lines":[166,183],"source_block_sha256":"ac07ec1b98c4f9598a23029a72ecb0c41d03fca454d5bfefc14cf0dd32ce3395"}},
    {"obligation_id":"P065-OBL-0016","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/15"},"canonical_record_sha256":"e598cf1a09634d5835f5ae9a0f98374a782106ff23eea0d90157cc86286024bf","canonical_owner":"PHASE-082-CANONICAL-EQUATION-FREEZE","target_phase":82,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-082-CANONICAL-EQUATION-FREEZE must resolve or explicitly bound the exact observation without backward-projecting later evidence into v1.0.24.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/401"},"canonical_record_sha256":"cbb5227a97b95f75ed8026a534fa432dc1da9a59fe6e2bf62af738158c73996f","source_id":"INTENT-PROV-0402","meaning":"report가 제안한 “상 구조와 곡선 표현 분리”는 살리되 단절 모델은 버린다","source_path":"Codex/results/PHASE_057AY_V1024_SNAPSHOT_V1025_2_KERNEL_REPORT_OBSERVATIONS.md","source_lines":[184,200],"source_block_sha256":"039fb7de95526f5931d7f94f3e71261ab8fd40ed8c621705bb38df58b337d61a"}},
    {"obligation_id":"P065-OBL-0017","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/16"},"canonical_record_sha256":"a74c17a98e1c0bb7a4376ca2553a7eebabd448db1c1607682b8b6fc5a0e8f4aa","canonical_owner":"PHASE-088-SCIENTIFIC-REDTEAM","target_phase":88,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-088-SCIENTIFIC-REDTEAM must resolve or explicitly bound the exact observation without backward-projecting later evidence into v1.0.24.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/402"},"canonical_record_sha256":"a2b7b7f12e1e8464c67cbfb4c3da9625d6751380a0d9e49c337444615c03a600","source_id":"INTENT-PROV-0403","meaning":"이 비교는 사용자의 최종 validation 범위를 거의 다루지 않는다","source_path":"Codex/results/PHASE_057AY_V1024_SNAPSHOT_V1025_2_KERNEL_REPORT_OBSERVATIONS.md","source_lines":[201,216],"source_block_sha256":"877064e33656ae229987536075253abb76815b2abd43498bde791d8d1ca750ad"}},
    {"obligation_id":"P065-OBL-0053","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/52"},"canonical_record_sha256":"b2d3f664842fa0040c2899a2f43243e9c56ccee86dd22b82c1d218a554c24174","canonical_owner":"PHASE-071-PRIMARY-SOURCE-ACQUISITION","target_phase":71,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must satisfy the bounded scientific-authority finding without promoting missing external evidence.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/141"},"canonical_record_sha256":"2917bbfd607d826e3d18a1fae711309f7dafd38b09e8fc939d0a55e39b3f5b67","source_id":"P065-S72-F03","meaning":"Several material conclusions are in-sample or bound-induced and do not establish external material truth.","source_acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must satisfy the bounded scientific-authority finding without promoting missing external evidence.","origin_record_pointer":"/findings/2"}},
    {"obligation_id":"P065-OBL-0054","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/53"},"canonical_record_sha256":"bed338ed5156219a9d1dafabc62cc56bc28a056168b03ecd705bd41be5617dc1","canonical_owner":"PHASE-080-BLEND-CLOSURE","target_phase":80,"state":"OPEN_CARRY_EXPLICITLY_BOUNDED_P067","external_authority_promoted":false,"acceptance_criterion":"Declare one consistent blend denominator and close the finite-rate current-partition/nonadditivity model contract without treating an in-sample fit as material proof.","relation_links":["P066-OBL-0120"]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/142"},"canonical_record_sha256":"d8ca905f478d4c1aad269e8d9becb42eb06241708e3d0d29b21f8a000f0ffa4f","source_id":"P065-S72-F04","meaning":"Blend additivity lacks one consistently declared denominator and finite-rate current-partition evidence.","source_acceptance_criterion":"P067-CODE-HISTORY must satisfy the bounded scientific-authority finding without promoting missing external evidence.","origin_record_pointer":"/findings/3"}},
    {"obligation_id":"P065-OBL-0055","selection_reason":"CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/54"},"canonical_record_sha256":"422346825298d31f042bd1865d0b1104845c03471fa92aa6b88d3e9fadefbb0e","canonical_owner":"PHASE-083-IMPLEMENTATION-CONTRACT","target_phase":83,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Replace the blanket claim with equation-ID and endpoint-specific conformance states, including explicit nonconforming paths.","relation_links":["P065-S70-F08","P065-S71-F01"]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/145"},"canonical_record_sha256":"d41eacb2ad457375f86064b9163c5bc771d8c7fb9791d2edb89c2ee62ba19b87","source_id":"D74-001","meaning":"The guide's blanket statement that the code implements the document equations exactly exceeds route-specific conformance.","source_acceptance_criterion":"Replace the blanket claim with equation-ID and endpoint-specific conformance states, including explicit nonconforming paths.","origin_record_pointer":"/conformance_rows/0"}},
    {"obligation_id":"P065-OBL-0064","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/63"},"canonical_record_sha256":"980c937bf25cbc55b7e9633dcd9511e14b2a1229db9556b731cf077c5eeca73c","canonical_owner":"PHASE-086-CALIBRATION-VALIDATION","target_phase":86,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Relabel the result as an analytic proxy and require independently registered measured LCO data for any real-fit or validation claim.","relation_links":["P065-S70-F14"]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/156"},"canonical_record_sha256":"a5448ac3f9806aef0cef093bcaa2c544c211a1726a35a260670b5d6023d531b4","source_id":"D74-012","meaning":"An analytic PyBaMM LCO proxy is labeled as the first real-data fit although no LCO-specific measured raw data were available.","source_acceptance_criterion":"Relabel the result as an analytic proxy and require independently registered measured LCO data for any real-fit or validation claim.","origin_record_pointer":"/conformance_rows/11"}},
    {"obligation_id":"P065-OBL-0079","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/78"},"canonical_record_sha256":"376958ca3d87fc7f740e3c65c9d6f4414188b4ea386bbae173692b7fbb9c980e","canonical_owner":"PHASE-083-IMPLEMENTATION-CONTRACT","target_phase":83,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"State that Omega alone affects other routes but does not select the equilibrium regsol kernel; require explicit model-family selection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/175"},"canonical_record_sha256":"a2bb4f09b6211685e17eb052762c24aa1841a5300791cd793b15cea2358147cd","source_id":"D74-031","meaning":"XRD profile Omega values do not activate regsol without the kernel key, a caveat not explicit at the profile-selection surface.","source_acceptance_criterion":"State that Omega alone affects other routes but does not select the equilibrium regsol kernel; require explicit model-family selection.","origin_record_pointer":"/conformance_rows/30"}},
    {"obligation_id":"P065-OBL-0084","selection_reason":"CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/83"},"canonical_record_sha256":"633df9b8b69c4dd02a416ccfa8e631139759a33174221703d0ff4ddbfbbc8389","canonical_owner":"PHASE-088-SCIENTIFIC-REDTEAM","target_phase":88,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Reclassify same-code checks as regression evidence and require independent equations/data for scientific or correctness claims.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/181"},"canonical_record_sha256":"24e0e73552b1a3ec21577f26dad3a8fcba04e51fd9e8d52eeaddc4f38f031d26","source_id":"D74-037","meaning":"Self-consistency and merge-ready/BUG0 records overstate validation because the fixed-point check uses the same implementation and open conformance gaps remain.","source_acceptance_criterion":"Reclassify same-code checks as regression evidence and require independent equations/data for scientific or correctness claims.","origin_record_pointer":"/conformance_rows/36"}},
    {"obligation_id":"P065-OBL-0086","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/85"},"canonical_record_sha256":"d866b1ac402ff5d6b38b7a1cec13183c7f799752727da013433efbbb6298ef29","canonical_owner":"PHASE-075-EQUILIBRIUM-PHASE","target_phase":75,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Downgrade the result to a bound-constrained in-sample diagnostic and require an unconstrained or independently justified inference with uncertainty before any phase-identity claim.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/183"},"canonical_record_sha256":"4f4cf9aa4ca8ce8ccff928e18bc745f7aba3a49f74ad7be022463498d924c135","source_id":"D74-039","meaning":"The graphite regular-solution helper treats Omega greater than 2RT as a phase confirmation even though the optimizer enforces Omega at or above 2.02RT.","source_acceptance_criterion":"Downgrade the result to a bound-constrained in-sample diagnostic and require an unconstrained or independently justified inference with uncertainty before any phase-identity claim.","origin_record_pointer":"/conformance_rows/38"}},
    {"obligation_id":"P065-OBL-0087","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/86"},"canonical_record_sha256":"59c9c759e832e7d017310d9fd335202bd4cf329185066e6f7a3e0b1d09e8e8c4","canonical_owner":"PHASE-079-SILICON-CLOSURE","target_phase":79,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Limit the statement to single-phase-consistent behavior under the stated fit and extraction assumptions, and test kinetic, disorder and extraction alternatives before a material phase conclusion.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/184"},"canonical_record_sha256":"6ffdb40de79a091287ec11567a62167c1a9458c36c3ac899eb53cb6a0d9521c8","source_id":"D74-040","meaning":"Finite fitted Si width ratios are presented as direct single-phase evidence although the same manuscript identifies them as fit-tier diagnostics.","source_acceptance_criterion":"Limit the statement to single-phase-consistent behavior under the stated fit and extraction assumptions, and test kinetic, disorder and extraction alternatives before a material phase conclusion.","origin_record_pointer":"/conformance_rows/39"}},
    {"obligation_id":"P065-OBL-0088","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/87"},"canonical_record_sha256":"7e424dff81c8440cd889141a9a0570ce685b8e6a446675f0936110b5d25d0da6","canonical_owner":"PHASE-077-GRAPHITE-CLOSURE","target_phase":77,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Report the gain as an in-sample flexibility diagnostic; require capacity-normalized parity, held-out comparison and uncertainty before transferring skew into a physical production model.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/185"},"canonical_record_sha256":"099e2d42c3a74a8329b687d5f93315dc1d1b2e3ea7cc364ae1ecd00f0d7fe63a","source_id":"D74-041","meaning":"A roughly one-percentage-point in-sample two-sided-width improvement is treated as transferable physical skew evidence although the prototype adds flexibility and does not preserve the production capacity normalization.","source_acceptance_criterion":"Report the gain as an in-sample flexibility diagnostic; require capacity-normalized parity, held-out comparison and uncertainty before transferring skew into a physical production model.","origin_record_pointer":"/conformance_rows/40"}},
    {"obligation_id":"P065-OBL-0089","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/88"},"canonical_record_sha256":"76c38b783d445b02b92b0af5b8335983eecc61937421a4d2cb8052cbb66061a2","canonical_owner":"P059-CFR-CF-01","target_phase":65,"state":"PRESERVED_ACTIVE","external_authority_promoted":false,"acceptance_criterion":"Preserve the bounded ideal statistical-mechanics and logistic-kernel identities without promoting them to material validation.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/inherited_phase065_observations/186"},"canonical_record_sha256":"a208d84a2cced669e87439e04e3a7fc3fe337d566c6b84d7c4283b2bf2873ace","source_id":"P059-CFR-CF-01","meaning":"Preserve the bounded ideal statistical-mechanics and logistic-kernel identities without promoting them to material validation.","source_acceptance_criterion":"Preserve the bounded ideal statistical-mechanics and logistic-kernel identities without promoting them to material validation.","origin_record_pointer":"/inherited_phase063_snapshot/prior_record/inherited_carry_items/12/prior_record/prior_record/prior_record/prior_record"}},
    {"obligation_id":"P066-OBL-0002","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/95"},"canonical_record_sha256":"5bcaeee1807576fba6ee7978d4f672bc44cd15ab86ed138a291a26d4f8895b76","canonical_owner":"PHASE-082-CANONICAL-EQUATION-FREEZE","target_phase":82,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-082-CANONICAL-EQUATION-FREEZE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/293"},"canonical_record_sha256":"47c95261aa20eb112844bee481bb9822e9f92e0a52d055e3d8112856506802f1","source_id":"INTENT-PROV-0294","meaning":"채택 모델과 이론 기록의 지위가 분리되어 있지만 경계가 충분히 강하지 않다","source_path":"Codex/results/PHASE_057AO_V1025_ARCHIVE_TOUCHUP_OBSERVATIONS.md","source_lines":[37,52],"source_block_sha256":"801a20571428c9273f89505e86c95525c107e40a22f98851ebce101c44d13c2f"}},
    {"obligation_id":"P066-OBL-0003","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/96"},"canonical_record_sha256":"693215573d3e778b07bcc5e367fb9c9ee37f2c272130dc72e5c7777e71e2bcb9","canonical_owner":"PHASE-086-CALIBRATION-VALIDATION","target_phase":86,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-086-CALIBRATION-VALIDATION must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/294"},"canonical_record_sha256":"297991a7c5f5e30c2304787401aa63baaf8e3cd92b6a593638c8e5a24bb6eede","source_id":"INTENT-PROV-0295","meaning":"v1.0.24의 양성 fitting 증거는 보존하되 검증 범위를 축소해야 한다","source_path":"Codex/results/PHASE_057AO_V1025_ARCHIVE_TOUCHUP_OBSERVATIONS.md","source_lines":[53,65],"source_block_sha256":"65036aa5c29e8688082687463a0b64c18e9d565d75eddd58e23a8749b5220d6f"}},
    {"obligation_id":"P066-OBL-0004","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/97"},"canonical_record_sha256":"6027ec402828a20ae13f11d6e4ee4ed5d7a6bfdc0177ce7e829edf4add656ee4","canonical_owner":"PHASE-077-GRAPHITE-CLOSURE","target_phase":77,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-077-GRAPHITE-CLOSURE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/295"},"canonical_record_sha256":"9e0317acd42452d9f3fc4ad97f98688912095feae39c57540ac5b517541afcf6","source_id":"INTENT-PROV-0296","meaning":"skew `alpha`는 정규화된 형상 자유도지만 아직 물질 물리 파라미터가 아니다","source_path":"Codex/results/PHASE_057AO_V1025_ARCHIVE_TOUCHUP_OBSERVATIONS.md","source_lines":[66,79],"source_block_sha256":"729bc155dd2b038e6ce92629e13ab422f0283ff854c0e23d4290be5823f127da"}},
    {"obligation_id":"P066-OBL-0013","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/106"},"canonical_record_sha256":"1f72cadb1d9991de7afecba80bf0fd0dea287c061f7ea8b2077411a430ef7470","canonical_owner":"PHASE-075-EQUILIBRIUM-PHASE","target_phase":75,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-075-EQUILIBRIUM-PHASE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/305"},"canonical_record_sha256":"6195189a96bf497dcf9b494aeefd8e2d9d500e471ec2f2977105a3919bcbcc2d","source_id":"INTENT-PROV-0306","meaning":"`Omega`를 kernel과 분리해 유지하면 fit과 상 판정이 서로 검증하지 못한다","source_path":"Codex/results/PHASE_057AP_V1025_DATA_ADDENDUM_OBSERVATIONS.md","source_lines":[78,92],"source_block_sha256":"912b165fc4f6233588deed4b30d91d4a45bda9f69be9713501a06478664cfc8f"}},
    {"obligation_id":"P066-OBL-0015","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/108"},"canonical_record_sha256":"2e9efc710438596a00be8765ef7ce6c0ec85525a965313fe286649226a9fb498","canonical_owner":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION","target_phase":81,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/307"},"canonical_record_sha256":"bc874ac8752eb3fa550c04fd23097722375d8ce3d1efcb53569bd4bf9175b74a","source_id":"INTENT-PROV-0308","meaning":"raw R² 비교만으로 전이 수·skew의 물리 필요성을 판정할 수 없다","source_path":"Codex/results/PHASE_057AP_V1025_DATA_ADDENDUM_OBSERVATIONS.md","source_lines":[109,123],"source_block_sha256":"263265f3954fe9548603f9b88049a14ecf62961630a7c70c86108f054fab01b7"}},
    {"obligation_id":"P066-OBL-0017","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/110"},"canonical_record_sha256":"922b32f78fe5c171d4f45944dac39cf02529154915cc2cafe538e9d1d26d286b","canonical_owner":"PHASE-077-GRAPHITE-CLOSURE","target_phase":77,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-077-GRAPHITE-CLOSURE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/309"},"canonical_record_sha256":"04ebef651e29b8cc8b3f90b87f88b3fd84bb6bd2a948346ba6532d027971611d","source_id":"INTENT-PROV-0310","meaning":"`gallery != phase`는 핵심 원칙이지만 basis 증가는 자동으로 물리적이지 않다","source_path":"Codex/results/PHASE_057AP_V1025_DATA_ADDENDUM_OBSERVATIONS.md","source_lines":[137,151],"source_block_sha256":"23fa10c25e24732929b4b63cb6342edc0b9c6b721316c102a38b4c0e3ff78d80"}},
    {"obligation_id":"P066-OBL-0020","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/113"},"canonical_record_sha256":"f948303f0a87731c8d0707bd9cc37c604c2408845481707cbc6070aa45d928ba","canonical_owner":"PHASE-086-CALIBRATION-VALIDATION","target_phase":86,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-086-CALIBRATION-VALIDATION must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/312"},"canonical_record_sha256":"9906f2858a5faa3e01945fa530214a44c8f44016713c75bcfc61970091d22cc4","source_id":"INTENT-PROV-0313","meaning":"이 addendum은 연구의 핵심 온도·전류·고전압 범위를 검증하지 않는다","source_path":"Codex/results/PHASE_057AP_V1025_DATA_ADDENDUM_OBSERVATIONS.md","source_lines":[180,191],"source_block_sha256":"5edbcf9312a07ce4b77444b8ab989353997698a2d424b40d6ab14d5493ec49c3"}},
    {"obligation_id":"P066-OBL-0028","selection_reason":"CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/121"},"canonical_record_sha256":"caf6a6f22428c35f57f28ee0babf6f5a02bac202426fb79d135bfac237902a0c","canonical_owner":"PHASE-088-SCIENTIFIC-REDTEAM","target_phase":88,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-088-SCIENTIFIC-REDTEAM must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/321"},"canonical_record_sha256":"591c99e98a46d46288f48cc31ed706daa552942f11541791f5738c938ffba9bd","source_id":"INTENT-PROV-0322","meaning":"문건·코드 감사 30/30은 물리 타당성 검증이 아니다","source_path":"Codex/results/PHASE_057AQ_V1025_CASCADE_LEDGER_OBSERVATIONS.md","source_lines":[141,153],"source_block_sha256":"095492e88b52dd0dbf96ee78e04f121b5253632310f5a1ea7b8fdbddbb0eba2f"}},
    {"obligation_id":"P066-OBL-0040","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/133"},"canonical_record_sha256":"25ec07b142dec448ca196603200579bb8756534a9fd469814c4cbe373ce18821","canonical_owner":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION","target_phase":81,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/336"},"canonical_record_sha256":"1d7b1d662b3503bdfef7d086f033983af71d1d4905a925f82379757bb1bf738d","source_id":"INTENT-PROV-0337","meaning":"empirical alpha가 entropy·reversible-heat 경로에 들어가면 열역학 오염 위험이 있다","source_path":"Codex/results/PHASE_057AS_V1025_DOC_EDIT_OBSERVATIONS.md","source_lines":[47,63],"source_block_sha256":"24fdefb0250e377fa78dee27d2def6bc7fac5286853b70cf884a3d4c08ec9b75"}},
    {"obligation_id":"P066-OBL-0041","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/134"},"canonical_record_sha256":"20f3e2e0c81cc1ca20b7106d378add9ff1389c1ff1716b9e6bc5428df46eced8","canonical_owner":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION","target_phase":81,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/337"},"canonical_record_sha256":"f7087263b0c8361e8023acf43ab1981fbc8fb881ab77adbf8a5180dcec953f6f","source_id":"INTENT-PROV-0338","meaning":"alpha는 비대칭뿐 아니라 위치와 폭도 바꾸는 강한 비식별 손잡이다","source_path":"Codex/results/PHASE_057AS_V1025_DOC_EDIT_OBSERVATIONS.md","source_lines":[64,77],"source_block_sha256":"7d148d9c43ec8818210693b4043d067b18d1c195d74d28b9042562b9c27993e2"}},
    {"obligation_id":"P066-OBL-0044","selection_reason":"CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/137"},"canonical_record_sha256":"5602b6e83cead9caec99e14d4ea8ec975fdef3a65e14c5e3724a1e1e202a21dc","canonical_owner":"PHASE-088-SCIENTIFIC-REDTEAM","target_phase":88,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-088-SCIENTIFIC-REDTEAM must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/340"},"canonical_record_sha256":"76f9b88c32adace945d09b55c911cff74333b5c2e3d8488bc19861c67c26c466","source_id":"INTENT-PROV-0341","meaning":"forbidden grep은 회귀 보조이지 의미 정합성 증명이 아니다","source_path":"Codex/results/PHASE_057AS_V1025_DOC_EDIT_OBSERVATIONS.md","source_lines":[108,119],"source_block_sha256":"a460e0cb79f53bf17602a846db6d6cc86d5d91428e0d9e7c2e465ddea3d12e35"}},
    {"obligation_id":"P066-OBL-0045","selection_reason":"CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/138"},"canonical_record_sha256":"45458b17d775d89b2abdf1f6218dfd048c32572444357509f691fd079c545e71","canonical_owner":"PHASE-088-SCIENTIFIC-REDTEAM","target_phase":88,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-088-SCIENTIFIC-REDTEAM must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/341"},"canonical_record_sha256":"b3a7eb2aa1c30fa84ad05b09880083d8fe4135729428cb8482d7635cbd8b6819","source_id":"INTENT-PROV-0342","meaning":"doc–code 30/30은 구현 충실도를 보이지만 같은 오류의 복제를 배제하지 못한다","source_path":"Codex/results/PHASE_057AS_V1025_DOC_EDIT_OBSERVATIONS.md","source_lines":[120,132],"source_block_sha256":"6377659240f92d5fbecd7c271a304ee5f079134293a29cb41b6a68c0793d2901"}},
    {"obligation_id":"P066-OBL-0048","selection_reason":"CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/141"},"canonical_record_sha256":"0b5fddc48739afc3056d6571cdd27582b9bcd3757a190a845f87808d08cd63f7","canonical_owner":"PHASE-083-IMPLEMENTATION-CONTRACT","target_phase":83,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-083-IMPLEMENTATION-CONTRACT must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/345"},"canonical_record_sha256":"0f6245795b1437a1992990294c2a4e9e2ad46cf5dfe38f81e58707ce1536acf1","source_id":"INTENT-PROV-0346","meaning":"“문건=코드”는 사용자가 명시한 핵심 기준이다","source_path":"Codex/results/PHASE_057AT_V1025_HANDOVER_INDEX_OBSERVATIONS.md","source_lines":[30,43],"source_block_sha256":"01ca450b8ec0ddf305637465924f2cf1f9dd96179d67eb3256d42226348f39a3"}},
    {"obligation_id":"P066-OBL-0049","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/142"},"canonical_record_sha256":"5e3cc1b6351e26a284d10bedcce375bbbdaeed18a7378f7cdd86416517e5238d","canonical_owner":"PHASE-072-DATA-PROVENANCE","target_phase":72,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-072-DATA-PROVENANCE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/346"},"canonical_record_sha256":"91c86bbf0d29f2a42301afee7908399d52528b35167a3a29356b7a9c8836000c","source_id":"INTENT-PROV-0347","meaning":"공개 데이터 직접 fitting과 peak·valley 형상 평가는 사용자 의도다","source_path":"Codex/results/PHASE_057AT_V1025_HANDOVER_INDEX_OBSERVATIONS.md","source_lines":[44,58],"source_block_sha256":"8c742effed35a1c2401ecfde16ff1599a1fa4c3ff0ca998f6703e183a31dc062"}},
    {"obligation_id":"P066-OBL-0054","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/147"},"canonical_record_sha256":"b00d1430920ebf6105c3ab2b4e78a95b7cc8c22d6163fbb7dba865b9496f0586","canonical_owner":"PHASE-088-SCIENTIFIC-REDTEAM","target_phase":88,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-088-SCIENTIFIC-REDTEAM must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/352"},"canonical_record_sha256":"0d42f0232fea8803cafc0d5880b33deb9223077d56774265c786c1094d7e8886","source_id":"INTENT-PROV-0353","meaning":"“Omega 물리는 전량 유효”는 검증 결과가 아니라 당시 handover 명령이다","source_path":"Codex/results/PHASE_057AT_V1025_HANDOVER_INDEX_OBSERVATIONS.md","source_lines":[128,141],"source_block_sha256":"09fe1230cd773f223fbada10960d37faf4b364a498179c0739b283d43ed37a10"}},
    {"obligation_id":"P066-OBL-0055","selection_reason":"CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/148"},"canonical_record_sha256":"2a38349d96e80d6dcdc493b054418b24f24eba2b9089c1075f08a53156656708","canonical_owner":"PHASE-088-SCIENTIFIC-REDTEAM","target_phase":88,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-088-SCIENTIFIC-REDTEAM must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/355"},"canonical_record_sha256":"811a139c42a9f0863942bbc051f91bbc6cb2ba77fecb37b716f010825bc78ded","source_id":"INTENT-PROV-0356","meaning":"MERGE-READY는 scientific validity나 endgame을 뜻하지 않는다","source_path":"Codex/results/PHASE_057AU_V1025_MERGE_READINESS_OBSERVATIONS.md","source_lines":[31,43],"source_block_sha256":"f4e5e6f15938bd6ba142be4793e7b05916cc182c1ae1ff7c423dc2a347d3d32b"}},
    {"obligation_id":"P066-OBL-0059","selection_reason":"CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/152"},"canonical_record_sha256":"41f1c4cf0ee964dcfc3e518f18443ac32ea25aa2e36908c284578e66717759b8","canonical_owner":"PHASE-088-SCIENTIFIC-REDTEAM","target_phase":88,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-088-SCIENTIFIC-REDTEAM must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/359"},"canonical_record_sha256":"8350ee0c3f80e350a0b4ed47865877aae53de835cfe0d885934187003b719281","source_id":"INTENT-PROV-0360","meaning":"“RED 0”은 물리 오류가 없다는 검사가 아니었다","source_path":"Codex/results/PHASE_057AU_V1025_MERGE_READINESS_OBSERVATIONS.md","source_lines":[85,98],"source_block_sha256":"2f130f1efe99f62fbd9d1dcc42c7e1f219ea46a395e54852ab23357f232fddb8"}},
    {"obligation_id":"P066-OBL-0063","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/156"},"canonical_record_sha256":"c0fa42888014d1c71c8220d64ad683f3b5bd5b7183293944945209cad6d65fe4","canonical_owner":"PHASE-077-GRAPHITE-CLOSURE","target_phase":77,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-077-GRAPHITE-CLOSURE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/364"},"canonical_record_sha256":"1bd3ff46b3c7e8c985fbdbd32f2be57fc13cc91fb2095411431e62ac0507fe39","source_id":"INTENT-PROV-0365","meaning":"skew7은 정온 곡선 표현에는 강하지만 thermodynamic model은 아니다","source_path":"Codex/results/PHASE_057AV_V1025_2_ARCHIVE_OBSERVATIONS.md","source_lines":[32,46],"source_block_sha256":"2727022dd1e621bd28a0324a23f9653029d828e0128eae7db0f8906d3e429121"}},
    {"obligation_id":"P066-OBL-0065","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/158"},"canonical_record_sha256":"feb478910b611e87874851fe59244652eefaa3db8eeaaa0dc252bd87d0f7a5f9","canonical_owner":"PHASE-077-GRAPHITE-CLOSURE","target_phase":77,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-077-GRAPHITE-CLOSURE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/366"},"canonical_record_sha256":"ac62999e68f5cb81837f1eec68bc83825aa26a99da7c76f0f3f9895ad0000e35","source_id":"INTENT-PROV-0367","meaning":"fit 성능 우세와 parameter 물리성은 문건 스스로 분리했다","source_path":"Codex/results/PHASE_057AV_V1025_2_ARCHIVE_OBSERVATIONS.md","source_lines":[62,75],"source_block_sha256":"137b26270d5726ad6131550eabc091dc8a1524d3add417935409097793efc849"}},
    {"obligation_id":"P066-OBL-0066","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/159"},"canonical_record_sha256":"b1463e6d646bc0b5d4041a1c31711064d5862851db0bf8c13e65a706bf38dad6","canonical_owner":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION","target_phase":81,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-081-IDENTIFIABILITY-AND-INVERSE-VALIDATION must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/367"},"canonical_record_sha256":"b5dbfc1768f1ad03ba07138a3fccb7d149865a069c1442ba3f5cfafe6ce144a7","source_id":"INTENT-PROV-0368","meaning":"BIC 우세는 독립 validation을 대신하지 않는다","source_path":"Codex/results/PHASE_057AV_V1025_2_ARCHIVE_OBSERVATIONS.md","source_lines":[76,88],"source_block_sha256":"316bd44c08f7baee26f198e695a198908f4733d0506799facc52c2aeaf51972e"}},
    {"obligation_id":"P066-OBL-0067","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/160"},"canonical_record_sha256":"791b642c1f33f1b9b6d966a1fb0bfba01e7e1c2b410ac82191c6187805360b74","canonical_owner":"PHASE-077-GRAPHITE-CLOSURE","target_phase":77,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-077-GRAPHITE-CLOSURE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/368"},"canonical_record_sha256":"f6f30441a454c2d47ec87bb80f2f97899b6bab25430bc4b19a50796517734434","source_id":"INTENT-PROV-0369","meaning":"fitted `Omega`를 logistic-skew 확정 구성의 phase 증거로 옮길 수 없다","source_path":"Codex/results/PHASE_057AV_V1025_2_ARCHIVE_OBSERVATIONS.md","source_lines":[89,104],"source_block_sha256":"70d60af57d4d21ca6a50532ab100f694ad9f3a544584479e0c48f69fcb0a66f3"}},
    {"obligation_id":"P066-OBL-0073","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/166"},"canonical_record_sha256":"60535414025e21b750b95547d65654ad36e8c22cf9017c85dc8b874a77324e79","canonical_owner":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS","target_phase":87,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/374"},"canonical_record_sha256":"dcff22494c679db7eda909ac2730028f44e966101100f52c52e9ff2873ac67ee","source_id":"INTENT-PROV-0375","meaning":"single-cell fit seed를 `_LIT`로 부르는 명명은 evidence tier를 흐린다","source_path":"Codex/results/PHASE_057AV_V1025_2_ARCHIVE_OBSERVATIONS.md","source_lines":[172,184],"source_block_sha256":"28d72fd57c66e112ddc89db69811c72218ed8f63a75925316755b662f2c06884"}},
    {"obligation_id":"P066-OBL-0076","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/169"},"canonical_record_sha256":"860abb9889e0e83403dfdaed54c9d5ea3f252f7ae45cb9f8452a277c38a27f77","canonical_owner":"PHASE-082-CANONICAL-EQUATION-FREEZE","target_phase":82,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-082-CANONICAL-EQUATION-FREEZE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/378"},"canonical_record_sha256":"dcf729e715cdf7a2e2ccfa3f46a522ce8aea223bc35d652b51ccea011b16d2c3","source_id":"INTENT-PROV-0379","meaning":"“이론 regsol, fitting logistic”은 사용자 확정 이력이지만 최종 consistency 해법은 아니다","source_path":"Codex/results/PHASE_057AW_V1025_2_HANDOVER_OBSERVATIONS.md","source_lines":[29,43],"source_block_sha256":"959ca0f7a8fa1b2b9482b4e766247c91b09a758af3d19bfc5d0dbd6308167b06"}},
    {"obligation_id":"P066-OBL-0079","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/172"},"canonical_record_sha256":"89266171f8cfe50937d8fefe154680a170e15c22f0fb22ccafcc358543e420ba","canonical_owner":"PHASE-082-CANONICAL-EQUATION-FREEZE","target_phase":82,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-082-CANONICAL-EQUATION-FREEZE must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/381"},"canonical_record_sha256":"5613e409107f67d3b9910b777a821cc59a72259c8a1fec0b83b0404cc5d40e51","source_id":"INTENT-PROV-0382","meaning":"더 나은 closure는 physical transition과 shape basis를 계층 분리하는 것이다","source_path":"Codex/results/PHASE_057AW_V1025_2_HANDOVER_OBSERVATIONS.md","source_lines":[71,85],"source_block_sha256":"eec7c2be845c2ed858d1f1c03db678d4f279ae64abafd785aaeb01fc19477b22"}},
    {"obligation_id":"P066-OBL-0083","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/176"},"canonical_record_sha256":"34771e5cd98b6cc1775429c88286adf003aa82f0b48e0c7139a9ec6cf7634896","canonical_owner":"PHASE-088-SCIENTIFIC-REDTEAM","target_phase":88,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-088-SCIENTIFIC-REDTEAM must resolve or explicitly bound this exact observation before canonical release without backward projection.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","selector":"/records/386"},"canonical_record_sha256":"a407d274fb9fa88eca978bedd45c51930457fce91fc4851829fc31dec67a1f64","source_id":"INTENT-PROV-0387","meaning":"v1.0.25.2는 사용자의 연구 목표를 위한 좋은 진단점이지 완성본은 아니다","source_path":"Codex/results/PHASE_057AW_V1025_2_HANDOVER_OBSERVATIONS.md","source_lines":[135,147],"source_block_sha256":"235faa38efef41d08abfbb39e22282ccb53c694c214be3c7b91183367d57a783"}},
    {"obligation_id":"P066-OBL-0115","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/208"},"canonical_record_sha256":"02c876f2ed6fae5b563996efb5b09806af004ad2d372727e50f3ceafc1c3f3a4","canonical_owner":"PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS","target_phase":69,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS must resolve or explicitly bound this observation before canonical release.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/step76_80_disposition_records/36"},"canonical_record_sha256":"77663e9afca4596a42357f8e03d78b426582c55b302fc5c2f6cfb185b39cffb6","source_id":"P066-E79-02","meaning":"The supplied Step 79 evidence establishes a complete competing-profile comparison and a transferable skew mechanism.","source_acceptance_criterion":"PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS must resolve or explicitly bound this observation before canonical release.","origin_record_pointer":"/claim_rows/1"}},
    {"obligation_id":"P066-OBL-0116","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/209"},"canonical_record_sha256":"b346c7d0a500ab184341c654b4768c1b2b3e1e46fa224848369e72cd1f8b122e","canonical_owner":"PHASE-071-PRIMARY-SOURCE-ACQUISITION","target_phase":71,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must resolve or explicitly bound this observation before canonical release.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/step76_80_disposition_records/37"},"canonical_record_sha256":"4deec3bdc2254378d671ea914643379d1623c32c9ebca84231d452c44d4d69b9","source_id":"P066-P79-03","meaning":"The whole-blend Direct14 components or frozen graphite profile labels establish graphite phase, gallery, or species identity.","source_acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must resolve or explicitly bound this observation before canonical release.","origin_record_pointer":"/claim_rows/2"}},
    {"obligation_id":"P066-OBL-0117","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/210"},"canonical_record_sha256":"6750a51c2702de4bd8ae408fcfcbd6f301008a5826a77509942c7d46af0c63a8","canonical_owner":"PHASE-071-PRIMARY-SOURCE-ACQUISITION","target_phase":71,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must resolve or explicitly bound this observation before canonical release.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/step76_80_disposition_records/38"},"canonical_record_sha256":"4fd50897b661c595c8436283fd1ded7827d0675732fabab31310265f699fcad5","source_id":"P066-P79-04","meaning":"The Direct14 fit establishes LCO phase, species, or thermodynamic-mechanism authority.","source_acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must resolve or explicitly bound this observation before canonical release.","origin_record_pointer":"/claim_rows/3"}},
    {"obligation_id":"P066-OBL-0118","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/211"},"canonical_record_sha256":"59e666f345306bde61ce82277ca0a54622a1a1226846e504a44148d2732548a1","canonical_owner":"PHASE-071-PRIMARY-SOURCE-ACQUISITION","target_phase":71,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must resolve or explicitly bound this observation before canonical release.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/step76_80_disposition_records/39"},"canonical_record_sha256":"eb85de9e02b73741d798a3ad0c28c872cea740a174de74400b908dd0acde98a3","source_id":"P066-P79-05","meaning":"The whole-blend Direct14 fit isolates Si phases or proves a symmetric-Frumkin or width-based Si mechanism.","source_acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must resolve or explicitly bound this observation before canonical release.","origin_record_pointer":"/claim_rows/4"}},
    {"obligation_id":"P066-OBL-0119","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/212"},"canonical_record_sha256":"524dcf8831636b221fdfd022238b7647cb527f2dc9ade4ed8c88b8bbbcb95583","canonical_owner":"PHASE-071-PRIMARY-SOURCE-ACQUISITION","target_phase":71,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must resolve or explicitly bound this observation before canonical release.","relation_links":[]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/step76_80_disposition_records/40"},"canonical_record_sha256":"28dc66f423398320302029bd7774eeedcca24625fc47a36454b5a13f101aff2f","source_id":"P066-P79-06","meaning":"Direct14 component areas on an absolute-mAh basis establish graphite/Si material fractions or a unique composition.","source_acceptance_criterion":"PHASE-071-PRIMARY-SOURCE-ACQUISITION must resolve or explicitly bound this observation before canonical release.","origin_record_pointer":"/claim_rows/5"}},
    {"obligation_id":"P066-OBL-0120","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/inherited_active/213"},"canonical_record_sha256":"ad5e24158c0339f2ee13775bb8329b5f38db63315ce79902579b5e03845d8cc0","canonical_owner":"PHASE-080-BLEND-CLOSURE","target_phase":80,"state":"OPEN_CARRY_EXPLICITLY_BOUNDED_P067","external_authority_promoted":false,"acceptance_criterion":"Derive the finite-rate host current-partition and nonadditive blend closure; retain the distinct in-sample fit identity without treating it as proof.","relation_links":["P065-OBL-0054"]},"semantic_source":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json","blob":"6366c5e3191aa933d0f8e1e03cfa780d7b3f0d95","selector":"/step76_80_disposition_records/41"},"canonical_record_sha256":"d348ffe7ab388c78c31bbff92ddfc8590bbec7b5de90b7cca55905d773dcf28c","source_id":"P066-P79-07","meaning":"A whole-curve fit tests finite-rate host independence, current partition, or nonadditive blend behavior.","source_acceptance_criterion":"P067-CODE-HISTORY must resolve or explicitly bound this observation before canonical release.","origin_record_pointer":"/claim_rows/6"}},
    {"obligation_id":"P068-OBL-0008","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/7"},"canonical_record_sha256":"d32fd48616f0c36dad2a7bf66199356a5c41e5db59dd8fd920720df22be9e87d","canonical_owner":"PHASE-077-GRAPHITE-CLOSURE","target_phase":77,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Replace all-above2 with the exact vector[1.916,2.027,2.472,2.604]; bound inference to identified fit/model and independently supported phase evidence.","relation_links":[]},"semantic_source":{"source_id":"GRAPHITE_THRESHOLD_ARITHMETIC","meaning":"GRAPHITE_THRESHOLD_ARITHMETIC","origin_target_ids":["C92-17","C92-18","F92-P1-02"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[122]","record_sha256":"4cef68bb6fbd7de454ae3b74dd64b0ade1028e59f095d425268444e6b7ec87a0"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[123]","record_sha256":"67a97dc27aa21b1ebd302b025e8404a1bca1e4ad3e4ee0b34da6f7e6ceb0150d"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_CODEX_FORK_DIFF_INVENTORY.json","blob":"c78e7ca1e1bbe6889f92f83e52d46798d4fb5c26","selector":"source_findings[1]","record_sha256":"9101865b90c75ff1a59ec2eef3da779ced9902b6cfc7386fc217d97def06307d"}],"target_route_pointers":[{"target_id":"C92-17","selector":"/target_routes/114","canonical_record_sha256":"b47629ca0d4c3529f5f4a51b43077ea00b3e0d373abcccb53c458bc73ed6cd55","state":"ACTIVE"},{"target_id":"C92-18","selector":"/target_routes/115","canonical_record_sha256":"2f9850c28d028da5bfc62c0873cd247c2450694a7ce2c85505c883d09df83af0","state":"ACTIVE"},{"target_id":"F92-P1-02","selector":"/target_routes/145","canonical_record_sha256":"d12dde29bee72002a1deae1933dcdd02e851665457a30446fd0a0cffb362ff9a","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0009","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/8"},"canonical_record_sha256":"11f5f4dde7765d78e22ae3295167acb9a89df0b223233c14449f8688e41fc214","canonical_owner":"PHASE-086-MATERIAL-VALIDATION","target_phase":86,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Preserve current49PASS2FAIL/51 and historical hashes unchanged; compare original arrays/runtime if available, otherwise bound reconstruction to current same-runtime/independent-formula agreement and reported R2/BIC. Do not infer old error size/cause from hashes.","relation_links":[]},"semantic_source":{"source_id":"FROZEN_CANDIDATE_HASH_DRIFT","meaning":"FROZEN_CANDIDATE_HASH_DRIFT","origin_target_ids":["C95-06","C92-09","C92-27","PHY-028","H44-FIT-014","H44-PRES-002","H44-GATE-002"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[290]","record_sha256":"0ed8c000fbdcf59993a237b8254f437fda97316828fe16e15bce24adc30a2881"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[114]","record_sha256":"4c67cbc1ade1756391d4dc708c5a0a44bc4524fbc96685c79de861da53fa5cc5"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[132]","record_sha256":"919bef8b69108bd6a29c4d05b2c3bd9156d168220303fb5ac05ec06df5466d52"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[324]","record_sha256":"3e31290e45051ba0363da8bc86a783882a0ef0b1cf4911cd055eb7dc6ec90e94"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[177]","record_sha256":"16c945644bde95f4d3a33eb080000afcca592a0651a13266e09e8a1a7396402c"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[206]","record_sha256":"6bd840788a2c30f446349f28de78d8a8ebb8e69239d45b8b004b69ee9a233c4c"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[251]","record_sha256":"3c597bfe6a5225f91dd91348f54dd6dd65ea661671fc5e725e2c9eb74a9771d9"}],"target_route_pointers":[{"target_id":"C95-06","selector":"/target_routes/133","canonical_record_sha256":"7c186feb59eef10849de46b84d465310527e21fe0c0a827880e77a81166538fd","state":"ACTIVE"},{"target_id":"C92-09","selector":"/target_routes/106","canonical_record_sha256":"89e9f43395ecffa5c32d18ed98345e7307c163aa079d3d26d048719ae5de6e6e","state":"ACTIVE"},{"target_id":"C92-27","selector":"/target_routes/124","canonical_record_sha256":"b7aed133158b59eec5c54ed86999229970e69c26214ddc5e2c7d0a91918550e8","state":"ACTIVE"},{"target_id":"PHY-028","selector":"/target_routes/635","canonical_record_sha256":"2a267360eb4a2ccf4653d6ced8aeb0ec912bf4328022cdfe4b6392077176ed18","state":"ACTIVE"},{"target_id":"H44-FIT-014","selector":"/target_routes/293","canonical_record_sha256":"11b0d24fd922c59c9331aec446ea4b6db8b5a7e613151e7496083753df220d14","state":"ACTIVE"},{"target_id":"H44-PRES-002","selector":"/target_routes/330","canonical_record_sha256":"0734f84522d972ae25f3a502ad00dace0c80c49799f2dc3eefb50f4c34ea0fe3","state":"ACTIVE"},{"target_id":"H44-GATE-002","selector":"/target_routes/295","canonical_record_sha256":"a36258d4297d95be49d1068020b32d6ac742078c7f99de94455beb4e39429e20","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0017","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/16"},"canonical_record_sha256":"9c73cee38abdd5c3f5417a77cc17318ece66237523dedde328f60a9789a60e80","canonical_owner":"PHASE-075-EQUILIBRIUM-PHASE","target_phase":75,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Unit derivative of sigma^alpha has area1; weighted component areaQj; finite-window cumulative differences and constant background are separate. Empirical-only interpretation and nonfinite/hash findings remain distinct.","relation_links":[]},"semantic_source":{"source_id":"EMPIRICAL_UNIT_KERNEL_AREA","meaning":"EMPIRICAL_UNIT_KERNEL_AREA","origin_target_ids":["C95-09","H44-PRES-001","PHY-007"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[293]","record_sha256":"eef87bfd4e95005a5b34fe75a4170bfff691388702365588cdee24a9d3b6727a"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[205]","record_sha256":"ff7662a850d7396aa401a8da7571408398c730d20535c4c4b31b6c4db0647d7b"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[303]","record_sha256":"b1a369090e956500799b5c46c734aec47fdff44682784b2e80fb0fe06ec16467"}],"target_route_pointers":[{"target_id":"C95-09","selector":"/target_routes/136","canonical_record_sha256":"879c07baa428e48c083df71cfce0135897874614c2bc5619a9216ecd02054333","state":"ACTIVE"},{"target_id":"H44-PRES-001","selector":"/target_routes/329","canonical_record_sha256":"f258450a9fe46eacf9b0f12b82fde35dc003dc56ca968ee6268f66d76c4f0548","state":"ACTIVE"},{"target_id":"PHY-007","selector":"/target_routes/614","canonical_record_sha256":"6d9221c7840517891385fc6ae971239abd12d7e9b49a0be4792fb5897e93926a","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0021","selection_reason":"CONFORMANCE_OR_REGRESSION_IS_NOT_PHYSICAL_VALIDITY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/19"},"canonical_record_sha256":"4f8710795c124cafba8be91f25b5ad192ae2e61327aac5cd213f392ca92a8591","canonical_owner":"PHASE-083-IMPLEMENTATION-CONTRACT","target_phase":83,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Keep each named legacy test predicate/domain/assertion/count separate from mathematical proof; recover corresponding transcripts or explicitly retain unknowns. Current candidate tests cannot replace legacy runs.","relation_links":[]},"semantic_source":{"source_id":"LEGACY_TEST_EVIDENCE_BOUNDARY","meaning":"LEGACY_TEST_EVIDENCE_BOUNDARY","origin_target_ids":["H44-TEST-P-001","H44-TEST-P-002","H44-TEST-P-003","H44-TEST-P-004","H44-TEST-P-005","H44-TEST-RUN-002","H44-TEST-RUN-003"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[235]","record_sha256":"042ed43169edca64be0c87bb3a4db70e74f846a33dc7b021c0712ed944849144"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[236]","record_sha256":"d58011a09ed1dac5d67ef6b213d5ba0a0677cdfc588a461214a94d57bf7debb5"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[237]","record_sha256":"5c8aa0ed027d77e5acd9df2d5d4f674b00ae5fa6e652ec4530ceaa1742bd592c"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[238]","record_sha256":"c02106e59cef2ed95e4a20c3fadec2a1e88ed1da197815482b5ff42d4704f320"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[239]","record_sha256":"953349d1689002650153812f0cde7e76d958dbd78ecb5e19fb60ef56586fe774"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[233]","record_sha256":"9c9c627c1f5c3080bdc08195f6520a2ac596a14dd6663018c3f2528656f0343a"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[234]","record_sha256":"5c89655dac997e92e0191a8bf6fec4614039c9eede2b71fa3d1e9b4623ceaea3"}],"target_route_pointers":[{"target_id":"H44-TEST-P-001","selector":"/target_routes/358","canonical_record_sha256":"dc4ba12ddff7e034135ab914152863904dfd27b2dc9c855d28f74256ee67a92f","state":"ACTIVE"},{"target_id":"H44-TEST-P-002","selector":"/target_routes/359","canonical_record_sha256":"4240b77aedfc88cafcf17df8848d342b6b79d7383af2a8c1e09fa462e90d1a07","state":"ACTIVE"},{"target_id":"H44-TEST-P-003","selector":"/target_routes/360","canonical_record_sha256":"8f6ff1b1bb5c11725b3fe1873028149681dad15568a35255bc9c6b090a32231a","state":"ACTIVE"},{"target_id":"H44-TEST-P-004","selector":"/target_routes/361","canonical_record_sha256":"c2b9d770ec93dcce75d85703bdbc1f22863e373a340b5a903b67bcdf057cefe0","state":"ACTIVE"},{"target_id":"H44-TEST-P-005","selector":"/target_routes/362","canonical_record_sha256":"b3b634d521851bc335ffc55f04fc7f2327b6bb43a6e62e7fe5ccfc191ac7ceaa","state":"ACTIVE"},{"target_id":"H44-TEST-RUN-002","selector":"/target_routes/364","canonical_record_sha256":"9300fb97e440863eb218a727a773ceb688b7089d796140438cfb248f35b31f84","state":"ACTIVE"},{"target_id":"H44-TEST-RUN-003","selector":"/target_routes/365","canonical_record_sha256":"71cf9cf99e6adb268d70b82c309467aae4fec4691f64d01ea386b3587aece218","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0031","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/29"},"canonical_record_sha256":"ba5017ab8cb9815f3f99b5f6a91c073227a716ef5e71333a559578fb51f827d2","canonical_owner":"PHASE-083-IMPLEMENTATION-CONTRACT","target_phase":83,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Separate immutable empirical profile/reconstruction product from source-backed physical state/material contracts; preserve source-specific equations/domain/failure behavior and failed historical hashes.","relation_links":[]},"semantic_source":{"source_id":"REFERENCE_IMPLEMENTATION_PRODUCTS","meaning":"REFERENCE_IMPLEMENTATION_PRODUCTS","origin_target_ids":["H44-ARCH-007","H44-PROD-001","H44-PROD-002"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[223]","record_sha256":"2977916fdba3f92d54ed2fb4b959b84701c75b12881e02cb5980334494d0ecae"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[226]","record_sha256":"fca158d5a45471dc36fd341aa648333022067fae509c751b4018b1fd65d995da"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[227]","record_sha256":"71b5eb691ae40783515749cf262af9c915b673bbe2096057dcdd78d3541c231b"}],"target_route_pointers":[{"target_id":"H44-ARCH-007","selector":"/target_routes/250","canonical_record_sha256":"cb5314cd3a0af04aa1858c2cfcc93a1ee272ff6f190ab774aa3b6533f5820639","state":"ACTIVE"},{"target_id":"H44-PROD-001","selector":"/target_routes/341","canonical_record_sha256":"b1e7673849264f88ac247b01d7f4c7c4dfe69b17e4a9c54b8e33c35287af02c9","state":"ACTIVE"},{"target_id":"H44-PROD-002","selector":"/target_routes/342","canonical_record_sha256":"59d20279eb019601714687ce1f509d8cc8699e6c35e6a5651ebbcbe9507db026","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0033","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/31"},"canonical_record_sha256":"9d139efa68622e0ffbc7f4984a08d81dc6350a428f3bf3e8ac29b56b0f8ce8b1","canonical_owner":"PHASE-074-FOUNDATION","target_phase":74,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Derive observation magnitude/skew map independently of signed physical occupancy, chemical background and material identity; keep empirical baseline separate.","relation_links":[]},"semantic_source":{"source_id":"OBSERVATION_STATE_SEPARATION","meaning":"OBSERVATION_STATE_SEPARATION","origin_target_ids":["H44-F007","PHY-004"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[184]","record_sha256":"df2cbbfc5bc3aede39d4c6f8427eb91c00299aedad0161472e77f83f4eec1996"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[300]","record_sha256":"a9d56ab02a6f0735a80f251bc1905f7bbd79f6d907817b45aa0b9543808e21d5"}],"target_route_pointers":[{"target_id":"H44-F007","selector":"/target_routes/275","canonical_record_sha256":"468a2915b7ee090adc5e893b67e2a93e89ba489e6a7f37571f56a99bcee53ea4","state":"ACTIVE"},{"target_id":"PHY-004","selector":"/target_routes/611","canonical_record_sha256":"d7b43412b0bb3297739c28b8e46320b26f99bfba47303937e02ef339e9206cfa","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0035","selection_reason":"PRODUCTION_PHYSICS_REQUIRES_INDEPENDENT_EVIDENCE_OR_BOUNDED_SCOPE","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/33"},"canonical_record_sha256":"bc1eb7d1b5f76860a1b45e2babedee086bf5fabf0706f504e8fd1d3c196a4daf","canonical_owner":"PHASE-075-EQUILIBRIUM-PHASE","target_phase":75,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Derive ideal independent-site reaction stoichiometry/thermal width and separate observation disorder or kinetics; support parameter/domain choices and do not infer nonideal implementation.","relation_links":[]},"semantic_source":{"source_id":"IDEAL_EQUILIBRIUM_CONTRACT","meaning":"IDEAL_EQUILIBRIUM_CONTRACT","origin_target_ids":["PHY-005","PHY-006","PHY-009"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[301]","record_sha256":"10ead23be80a9b9e58b0e17a5f3c905921791ac0ff0177108a1696025e6a45e5"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[302]","record_sha256":"5a671b292b6b61bb541ab14ec9f8ac0f118b283a9eb95e7b9121ca699eab3d6a"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[305]","record_sha256":"2ff7b0a23e6a51015fc89dfa50c1d5b22570eaaaf15cb0c0d23a1a13a75726d9"}],"target_route_pointers":[{"target_id":"PHY-005","selector":"/target_routes/612","canonical_record_sha256":"6c36ad644c96b61a46a3713439f5f8a625724506f430ce1d9ef7e900962249ca","state":"ACTIVE"},{"target_id":"PHY-006","selector":"/target_routes/613","canonical_record_sha256":"2ddcb4d0a321355dde30c00963391896fdaf0ed3f6ea2fd020b7b04269dc5a74","state":"ACTIVE"},{"target_id":"PHY-009","selector":"/target_routes/616","canonical_record_sha256":"ad398ce3cffeb37d4a774b7551f39191d4adf15e955f12d3a22e1fd6f31dfffd","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0037","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/35"},"canonical_record_sha256":"678addcce891d45d7bd188c6c29b7c8a7e3e9f4c10e6201c5a9c70d8e2ad392f","canonical_owner":"PHASE-081-INFERENCE-UNCERTAINTY","target_phase":81,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Require material-specific independently sourced configurational/vibrational/electronic entropy differences and held-variable definitions; empirical shape alone does not identify components.","relation_links":[]},"semantic_source":{"source_id":"MATERIAL_ENTROPY_SUPPORT","meaning":"MATERIAL_ENTROPY_SUPPORT","origin_target_ids":["PHY-021"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[317]","record_sha256":"6c6b487f4aa006bb250f3ecd33e7f9d4cbe0db7892c359b3dc99930e4c18f6bf"}],"target_route_pointers":[{"target_id":"PHY-021","selector":"/target_routes/628","canonical_record_sha256":"bc140b4bf4dc64d7758d555709f5a0e6be158e58dc41b0835fed3eb645157c1d","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0046","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/43"},"canonical_record_sha256":"a944cc84d963876b6bba3f20228cb20586670b2dd2215cbd79eeff420298d281","canonical_owner":"PHASE-077-GRAPHITE-CLOSURE","target_phase":77,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Require independent gallery/staging/host assignment, declared reactionstoichiometry/entropy/enthalpy and specimen/protocol; do not populate thermodynamic parameters from empirical width or component count.","relation_links":[]},"semantic_source":{"source_id":"MATERIAL_GRAPHITE_ASSIGNMENT","meaning":"MATERIAL_GRAPHITE_ASSIGNMENT","origin_target_ids":["C91-37","C91-77","C91-84","C91-85"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[36]","record_sha256":"409fa7a8eb57c90d6468b9f19113209b6f4adfbfb64b340db7d5b937233e9e37"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[76]","record_sha256":"260bb33482f6125be6026a0fbd93c2517a305b9135fd2411b768318831158908"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[83]","record_sha256":"d9abd91fe9dcd67e809a8b68cd93fd0b2b24a16015871edc72e860f0a0fda24f"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[84]","record_sha256":"316b4f40bf211dbb2d824cdbc6ab9e26d81f267c0510590ccb5a1b3b49068283"}],"target_route_pointers":[{"target_id":"C91-37","selector":"/target_routes/36","canonical_record_sha256":"40b4035665ef6bed6d53052f4ee9beda4d87c9dafe1a42771a7146717bf02acb","state":"ACTIVE"},{"target_id":"C91-77","selector":"/target_routes/76","canonical_record_sha256":"7484b59d7be0a03ca6943eb8f1345e693b3d4ce1de2ba6739ff98319b46fb629","state":"ACTIVE"},{"target_id":"C91-84","selector":"/target_routes/83","canonical_record_sha256":"45bb40f2ec6bfd287f7c9f4dcbc2c618fc7ad6d0dd3ca4eef9a727270288a447","state":"ACTIVE"},{"target_id":"C91-85","selector":"/target_routes/84","canonical_record_sha256":"413a9f14d1e0caad9db7a8e85ef3d2e9fea56c31a1864c76f46851019075aba0","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0048","selection_reason":"FIT_OR_INTERNAL_SCORE_DOES_NOT_SELECT_PHYSICAL_MODEL","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/45"},"canonical_record_sha256":"3fde3911860925503493768261638f981d589f93d3b235d436145d7ada4ad877","canonical_owner":"PHASE-081-INFERENCE-UNCERTAINTY","target_phase":81,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Require exact residual model/objective, independent data, identifiability/uncertainty/held-out evidence before physical interpretation; BIC under smoothed correlated errors remains working diagnostic.","relation_links":[]},"semantic_source":{"source_id":"INFERENCE_IDENTIFIABILITY","meaning":"INFERENCE_IDENTIFIABILITY","origin_target_ids":["H44-PRES-011","H44-FIT-012","H44-FIT-013"],"evidence_pointers":[{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[215]","record_sha256":"70d6125b90c5cb1b7facf680f1721dc0cc6ee60d26610ea79cdb26cd19da94f0"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[175]","record_sha256":"df7c579370091e4b107c08f58be2c8c5676c536e4110bdda7515a9c42b6643e3"},{"commit":"f9feef379d597d320cb5692ed2eda739a336d02f","path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[176]","record_sha256":"600438d51d6b865871813eca1b73df770dd13251e1b6367cd028aef83f19c549"}],"target_route_pointers":[{"target_id":"H44-PRES-011","selector":"/target_routes/339","canonical_record_sha256":"db476dff3bac906d1013f28da9ef33419a92daac54cd37e6bd6bf2cc648e9bf5","state":"ACTIVE"},{"target_id":"H44-FIT-012","selector":"/target_routes/291","canonical_record_sha256":"2681e6e99a8c864dbebfc71435656aa627033d801faae2c8fc201a3795306758","state":"ACTIVE"},{"target_id":"H44-FIT-013","selector":"/target_routes/292","canonical_record_sha256":"8cd38917a8aad001568829a4536469b9d40ee1149aa5b3870272bd56a58cb946","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0059","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/56"},"canonical_record_sha256":"ad0eed4aedc6929314c842eeb9022dff9cc7107255d4a95085ed72b35690e57f","canonical_owner":"PHASE-075-EQUILIBRIUM-PHASE","target_phase":75,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Derive ideal width under explicit reaction stoichiometry; separate empirical width and physical heterogeneity.","relation_links":[]},"semantic_source":{"source_id":"FILE_ACCEPTANCE_FILE97-006","meaning":"FILE_ACCEPTANCE_FILE97-006","origin_target_ids":["FILE97-006"],"evidence_pointers":[{"path":"Claude/docs/v1.0.25.2/_sections/ch1_sec05_width.tex","blob":"2003860215e0a721876bace4364b3b7a6a594031","record_sha256":"caead9f3e1d0995f41b233e7dd456d6ec7aa05a4a288d3f97c7ea6dd1b978828"}],"target_route_pointers":[{"target_id":"FILE97-006","selector":"/target_routes/154","canonical_record_sha256":"23a0c94e5d5bd788da10e838a68375dd03b4509681a0617f00b1fdff2652ec0f","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}},
    {"obligation_id":"P068-OBL-0067","selection_reason":"EMPIRICAL_OR_REDUCED_PHYSICS_AUTHORITY_BOUNDARY","current_record":{"pointer":{"commit":"76b07667085c0d1d886b667ce2b490b40470af7a","path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","selector":"/new_obligations/64"},"canonical_record_sha256":"642b0939429a04f463a692d5778e1ac1adae5a7d3e4ccac000f0be21a78b283b","canonical_owner":"PHASE-075-EQUILIBRIUM-PHASE","target_phase":75,"state":"OPEN_CARRY","external_authority_promoted":false,"acceptance_criterion":"Correct unit-kernel area1 versus weightedQj, finite-window endpoints/background and empirical-only authority.","relation_links":[]},"semantic_source":{"source_id":"FILE_ACCEPTANCE_FILE97-048","meaning":"FILE_ACCEPTANCE_FILE97-048","origin_target_ids":["FILE97-048"],"evidence_pointers":[{"path":"Codex/results/v1025_2_physics_branch/EMPIRICAL_SKEW14_PROFILE.md","blob":"6c8a055628e6f133f4ad0a2bbb1eef8adbb43215","record_sha256":"8dd6736383faa27145956cc92b4f2a94ed308eb0e1873cd9300d2724ab0f3700"}],"target_route_pointers":[{"target_id":"FILE97-048","selector":"/target_routes/196","canonical_record_sha256":"f9440c2c8936468e8eee4ca3270a11cd59af3ec8bd90d4e6eb3b216fca1318f3","state":"ACTIVE"}],"full_origin_acceptance_clauses_preserved_by_current_record_pointer":true}}
  ],
  "acceptance_crosscheck": {
    "all_selected_exist_once_in_current316": true,
    "all_selected_states_preserved_exactly_from_current_record": true,
    "selected_state_counts": {
      "OPEN_CARRY": 56,
      "OPEN_CARRY_EXPLICITLY_BOUNDED_P067": 2,
      "PRESERVED_ACTIVE": 1
    },
    "all_external_authority_promoted_false": true,
    "owner_target_phase_acceptance_copied_exactly_from_current_record": true,
    "semantic_source_exact_pointer_and_record_digest_present": true,
    "P068_target_routes_contain_selected_obligation": true,
    "no_new_id_reowner_or_closure": true
  },
  "unresolved": [],
  "findings": {
    "P0": [],
    "P1": [],
    "P2": []
  }
}
```

Step106 NOT_YET_EXECUTED; Step107 NOT_SELECTED. 070 이후는107 positive/persisted gate 전에는 시작하지 않는다.
