# Phase 068 Step 95 — Conformance model source/output manifest addendum

## Summary

활성 Astra master와 Phase 068 continuation detailed plan의 Step 95 입력·출력 경계를 실행 전에 고정한다.
기존 conformance source는 수정/채택하지 않는다. scientific authority, implementation value,
duplicate-lineage risk를 별개로 판정하고 최종 5상태 처분은 Step 97로 넘긴다.

## Current Ground Truth

- Active branch: codex/anode-fit-v1025_2-canonical-completion.
- Step 94 완료/pushed/live HEAD: 1c77c69004aa4bdb6fbfb2efe01087a25ccd5d14.
- 이번 재개에서 HEAD와 live origin 일치 및 clean tree 직접 확인.
- Frozen conformance tip: 11f90544865dd179739ca5bc5062b28c1078e504.
- Protected/main/Claude/frozen refs와 기존 원고·구현은 변경하지 않는다.
- C92-19–24, F92-P1-04/F92-P2-01은 새 재현·분석 전 미결이다.
- Phase 067 RESULT 전문 확인: 일곱 internal conformance determinant와 외부 문헌/재료/held-out 부채 유지.

## Phase Range

Phase 068, 누적 Step 95 하나. 94의 실제 persistence를 index에 반영하고, 95 결과 포함 commit/push 후 96으로 간다.

## Non-goals

canonical 이론/production code 수정, 물리 모델 선정, PDF release, 실제 fit 재수행,
whole-commit adoption, 추측 원문/문헌 보강, 과거 결과 덮어쓰기 금지.
불필요한 범용 validator/AST hardening은 만들지 않는다.

## Input Manifest / Read Plan

아래 42개는 모두 frozen tip의 정확한 Git blob이며 1–EOF 전문 검독한다.
표는 실행 전 범위이고 완료 attestation이 아니다. 실제 fresh/reused와 reader는 결과에 기록한다.
모델 11, tests 10, manuscript 16, 계약/empirical 5개다.
계획 준비로 README, _reference, run_all, verify_manuscript 전문은 이미 읽었지만 나머지는 미완료다.

| Path | Blob | Full line range | Assigned read |
|---|---|---:|---|
| Codex/work/v1025_2_physics_branch/conformance_model/README.md | 62ec65b9f3d10c1271e0459fceafb514adbb1dc6 | 1–30 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/__init__.py | de2cd9ec1df27934a94519087293f1b27da8e68f | 1–80 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/constants.py | 0990ad6571e09855bd18d4d0f9bb73b29cf40370 | 1–42 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/dynamics.py | 8a752ddd16b5020c8d278d359d446b7cbeafade0 | 1–150 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/empirical.py | 0fdba1082c4758088a3fc1f0ddd52eb33bd6b744 | 1–269 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/heat.py | aa80827bc1b72ef3fd6cb79bd665e02d903fec5a | 1–117 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/kinetics.py | dc0c02805cc9a667657cc5ff65e751b4f1c57525 | 1–120 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/numerics.py | f8a8fa11de960c6bc209e9b538735446b5da3b54 | 1–71 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/observation.py | 7b318efa7cf86677b878b706f056c3c7f58ad76d | 1–99 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/physical.py | e29d68e69875c1303ed23c5ea1a30336c32b8ca5 | 1–523 | model reviewer |
| Codex/work/v1025_2_physics_branch/conformance_model/presets.py | da9ceac3afcb0d2fdd3e1ed47b4e4b69dbf944a6 | 1–132 | model reviewer |
| Codex/work/v1025_2_physics_branch/tests/README.md | f52d7a51b856fcd02283c989a8be08e41c77a251 | 1–36 | root |
| Codex/work/v1025_2_physics_branch/tests/_reference.py | 81b5fd88fa75a49a6d957842288bc6f4fa1fe343 | 1–177 | root |
| Codex/work/v1025_2_physics_branch/tests/run_all.py | acb6c3ae94e3ca60a79590b2850f3a36f33fb0b6 | 1–21 | root |
| Codex/work/v1025_2_physics_branch/tests/test_dynamics.py | 0a82ad55ea547fb4d4bd2bf87c80fabc8327676e | 1–145 | root |
| Codex/work/v1025_2_physics_branch/tests/test_empirical_profile.py | c71a7b821b879d4963f916f0436654865f3cfb17 | 1–267 | root |
| Codex/work/v1025_2_physics_branch/tests/test_kinetics_heat.py | a91576484f918550d0895c4d7f2fc3c70b5e842d | 1–203 | root |
| Codex/work/v1025_2_physics_branch/tests/test_manuscript_static.py | ec7f22f56c632c2c6dbfd12366a8bf38f0494bc7 | 1–134 | root |
| Codex/work/v1025_2_physics_branch/tests/test_numerics_observation.py | 0b94ce10159d01933d5ef73039bf477ac0552bc5 | 1–104 | root |
| Codex/work/v1025_2_physics_branch/tests/test_physical_equilibrium.py | e78561105abfc63f2108948adba6d2c979df10b2 | 1–292 | root |
| Codex/work/v1025_2_physics_branch/tests/verify_manuscript.py | a09da31e70a5cdd70aa69b1324fe571bb7801c0e | 1–440 | root |
| Codex/results/v1025_2_physics_branch/manuscript/anode_physics_master.tex | 439cbf2fbea260c91561ac3f1c298c64605ac250 | 1–174 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/appendices/assumption_register.tex | 8c018772eeacbb7b92d94ed8c369b4503aa9e686 | 1–72 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/appendices/derivation_checks.tex | 5a90f2698ab81c4fe537d7322619f8f0b2a17179 | 1–120 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/appendices/implementation_interface.tex | 867754ff009503bc9217eef803cfb64b26d18536 | 1–114 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/chapters/ch01_equilibrium_observation.tex | 6564bb71bda2e0b927420400e8e9e670969ff8ef | 1–235 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/chapters/ch02_thermodynamics_heat.tex | d2d0a3f3937552f38bf5d24ea5d21b8bece9c8c2 | 1–197 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/chapters/ch03_kinetics.tex | 1e286bac33584b12edb803d111c1e5325db625dc | 1–200 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/chapters/ch04_integrated_eos.tex | 900a2f32d4e8ba0e590503181962e32f2dc9294b | 1–146 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/chapters/ch05_hysteresis.tex | f7251fd1117ac72eb9f9925fbab1d0ca0e827ed2 | 1–120 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/common/conventions.tex | 6a8d957f88fedc1096882019c361a7ee79888424 | 1–45 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/common/evidence_grades.tex | fd147f69ab13dbe5b1bbd3b40e334f353fb6b329 | 1–30 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/common/notation.tex | 83a0eda0d44a378c84e379f5919c0d2359d78450 | 1–50 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/empirical/skew14_profile.tex | 20107d8f8f69ab8e4f10c3ca233d32380e919523 | 1–132 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/materials/graphite_application.tex | bda7825d1dc6081634b4544cc43e0221b250a41f | 1–81 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/materials/lco_application.tex | b23532f83353cf8a4ef37dd17116f3c4f5176013 | 1–101 | root + model reviewer anchors |
| Codex/results/v1025_2_physics_branch/manuscript/materials/si_blend_application.tex | 8112e8c10c0170e67f2bec109df79343b3b02bac | 1–99 | root + model reviewer anchors |
| Codex/results/V1025_2_PHYSICS_DECISION_LEDGER.md | e1dc03e575c68a601388bde28196bfad71774597 | 1–745 | root |
| Codex/results/V1025_2_PHYSICS_IMPLEMENTATION_CONFORMANCE_MATRIX.md | c5406428dc9cf954c17c69e8fdabf0bc581b9bdb | 1–239 | root |
| Codex/results/V1025_3_PHYSICS_IMPLEMENTATION_CONFORMANCE_MATRIX.md | f4c9ab14bee81d3995f800fb59321b6c1eedcd84 | 1–64 | root |
| Codex/results/v1025_2_physics_branch/EMPIRICAL_SKEW14_PROFILE.md | 6c8a055628e6f133f4ad0a2bbb1eef8adbb43215 | 1–172 | root |
| Codex/results/v1025_2_physics_branch/artifacts/empirical_blend14_v10252.json | d76fb828bc5b49ec171ef8abedd1cd0253f6b767 | 1–215 | root |

Runtime-only fixtures는 아래와 같다. 전체 bytes hash/parse/dataset numeric invariants를 검사하되,
CSV 16,736행을 사람이 전문 검독했다고 주장하지 않는다. 외부 provenance 확인은 별도 후속 단계다.

| Path | Blob | Lines | Scope |
|---|---|---:|---|
| Claude/results/comp_v26_data/out_versions/summary_versions.json | c0a475352abe2f2df145442d8ed722d132ab5d03 | 873 | strict parse; C_skew/blend used slice and parameter identity |
| Claude/results/comp_v24/sintef_data/sigr.csv | 4b06fefa1bb81de842386c95fbba5bdd431602d4 | 16736 | bytes identity; actual historical preprocessing only |
| Claude/results/comp_v26_data/test_skew_regsol_v2.py | c064a11241c07195a11ad12878fa7a3914c1f15b | 300 | bytes identity required by existing test; not executed |
| Claude/results/comp_v26_data/bdd_dqdv.py | c4fc6b997bad2a15617f1c7255708bf736b9e37a | 177 | bytes identity required by existing test; not imported |
| Claude/results/comp_v26_data/regsol_kernel.py | 5bb1a3b2dafdafc29d990366d734c0d072c7092c | 108 | bytes identity required by existing test; not imported |
| Claude/results/comp_v24/sintef_data/gr.csv | 223cd9eb690d91045921eb66ed0c2187f666bafe | 16828 | bytes identity only |
| Claude/results/comp_v24/sintef_data/si.csv | 0d634f92b681707c57da2e75bfcb9465d9204cc1 | 10832 | bytes identity only |

현재 chain 입력: active master/detailed, Step 94 result, compact index/handover 전문;
PHASE_067_RESULT.md 전문; Step 92 inventory는 structured selection으로 해당 claim/identity를 확인한다.
이 선택 확인을 Step 92 JSON의 fresh 전체 human read로 계수하지 않는다.

## Implementation Changes / Exact Output Allowlist

신규:
1. 이 계획: Codex/plans/2026-09-07-phase068-step095-conformance-model-manifest-addendum.md
2. Codex/results/PHASE_068_STEP_095_CONFORMANCE_MODEL_ADJUDICATION_RESULT.md
3. Codex/results/PHASE_068_CONFORMANCE_MODEL_ADJUDICATION.json
4. Codex/results/PHASE_068_STEP_095_RUNTIME_312.json
5. Codex/results/PHASE_068_STEP_095_RUNTIME_314.json
6. Codex/work/v1025_phase068/run_phase068_step95.py
7. Codex/work/v1025_phase068/test_phase068_step95.py

갱신:
8. Codex/results/ASTRA_CANONICAL_COMPLETION_EXECUTION_LEDGER.md
9. Codex/results/ACTIVE_HANDOVER_ASTRA_CANONICAL_COMPLETION.md

필요한 범위 확장은 실행 전에 이 addendum의 correction으로 명시하며 이전 계획은 수정하지 않는다.
외부 disposable directory의 frozen export와 test scratch는 추적하지 않는다.

## Step 95 — Execution

95.1. exact blob 42개 전문 검독을 분담하고 source→manuscript physics ID/식/가정 mapping을 작성한다.
95.2. 변수·단위·부호·초기/최종 state·default·guard/fallback·serialization을 검토한다.
95.3. 독립된 임시 directory로 위 frozen tree와 fixtures만 export한다.
historical tests에서 scratch 파일이 필요하면 원본 snapshot과 분리된 임시 경로만 쓴다.
95.4. Python 3.12/3.14 실제 run_all 및 standalone manuscript verifier를 실행한다.
NumPy/Pandas/SciPy와 fixtures preflight, collected/executed/skipped/errors를 구분하고 실제 child 출력/exit를 기록한다.
95.5. C92-19–22의 bounded finite-domain 후보를 원본 수정 없이 재현한다.
재현 failure는 모델 결함 증거이지 감사 실패 자체가 아니다. repair-before-adoption owner를 남긴다.
95.6. 모든 파일과 확인 이슈에 세 축 판정, 범위·근거·추천 처분·다음 owner/수용 시험을 붙인다.
scientific authority는 내부 대응/조건부 수학에 한정하며 외부 과학 진위로 승격하지 않는다.
95.7. 결과서 먼저 동결 후 JSON evidence/실제 runtime receipts를 저장한다.
입력 identity/coverage/claim accounting, runtime evidence와 금지 승격 0을 검증한다.
95.8. 정확한 pathset/단일 parent 1c77c69004aa4bdb6fbfb2efe01087a25ccd5d14,
subject audit(phase068): adjudicate conformance model and tests,
result 포함 commit/push/live equality/clean 확인 후 96으로 이어간다.

## Implementation Interfaces / Test Plan

- 읽기 표: path/blob/lines/reader/fresh-or-reused/unread.
- 모델 판정: file, equation IDs/anchors, units/sign/domain, authority, value, duplication, issues.
- Runtime: actual executable/version/dependencies, source hashes, command, stdout/stderr, exit,
collected/executed/skipped/error counts; 의도적 probe의 nonfinite는 JSON에서 문자열로 명시한다.
- 작은 runner의 입력 누락/변조, 실제 child 실패 capture, 파일 덮어쓰기 금지를 먼저 실패 시험으로 검증한다.
- 기존 과학 test를 고쳐 통과시키지 않는다. 현행 runtime failure와 frozen-source flaw를 구분한다.
- 외부 원천 검증/최적화/문헌 support는 이번 Gate 성공 조건으로 위장하지 않는다.

## Gate / Stop / Next

전문 42개/주장식 coverage, 세 축 분리, 두 runtime 실제 실행/실패 근거와 미결 owner가 완전하면
PASS_P068_STEP95_ADJUDICATION_CONTENT. 그 의미는 감사 완료이며 candidate all-tests-pass와 독립이다.
필수 입력/식 mapping 누락, 읽지 않은 완료 표기, 권위 혼동이면 완료 금지.
예상치 못한 remote/protected 변경 또는 추가 권한 없이는 의존 작업을 중단한다.
정상 commit/push 후 Step 96 claim conflict matrix로 계속한다.

## Assumptions / Correction History

2026-09-07: Step 94 실제 persistence 이후 신규 작성. 운영 경로·42-file 범위·runtime-only fixtures를 고정했다.
2026-09-07 pre-runtime: test_empirical_profile 전문에서 5개 추가 hash-only fixtures를 직접 확인해 위 표에 추가했다.
Full-read 대상 42개는 유지, frozen export는 49개다. Python 3.14의 Pandas 누락을 preflight로 확인했으므로
최초 의존성 실패를 기록하고 필요 시 외부 isolated venv에만 의존성을 설치한다. 전역 Python 환경은 수정하지 않는다.
