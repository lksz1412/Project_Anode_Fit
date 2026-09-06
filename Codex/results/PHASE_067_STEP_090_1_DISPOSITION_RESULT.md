# Phase 067 Step 90.1 Disposition Result

Date: 2026-09-06  
Branch: `codex/anode-fit-v1025_2-canonical-completion`  
Expected parent: `38f93bd1638c674ff7fd7fb40ed57036a07fd8fd`  
Expected subject: `audit(phase067): disposition code test fitting evidence`  
Content Gate: `PASS_P067_STEP90_1_DISPOSITION`  
Persistence state: `PASS_PENDING_PERSISTENCE`  
Required terminal: `PASS_P067_STEP90_1_PERSISTENCE`

## 1. Result

Step 90.1은 Step 82–89의 persisted machine evidence를 expected-parent Git objects에서 다시 읽어
Python source, test, demo, result/tool, golden 및 fitting guide를 exclusive disposition했다.
Python 분모는 occurrence `129`, unique blob `84`, unique-blob physical line `29,952`, release
`20`으로 유지했다. Test `44/29`, demo `30/26`, result/tool `35/14`는 이 `129/84`의 role
partition이므로 별도 source 수로 재가산하지 않았다. Golden `8/2`와 guide `20/8/854`는
Python 밖의 별도 namespace다.

Source occurrence disposition은 총 `157`개다. Python blob마다 Step 88의 production/optimizer
selection을 exact join하여 canonical production 또는 exact historical optimizer source에 속한
Python occurrence `21`개와 golden `8`개를 `PRESERVE`했다. 나머지 Python occurrence `108`개와
guide `20`개는 삭제하지 않고 exact origin pointer/hash를 보존한 채 canonical authority에서
`WITHHOLD`했다. 따라서 source disposition은 `PRESERVE/WITHHOLD=29/128`이고
`CORRECT/DISCARD/GROUND_NOT_FOUND=0/0/0`이다. Python `84`, golden `2`, guide `8`의 blob group
총 `94`개가 모든 occurrence를 역참조한다.

Steps 82–89의 source-native record는 축약하거나 다시 쓰지 않고 immutable input의 RFC-6901
pointer와 canonical row SHA-256으로 `1,168`개 disposition record에 연결했다. 분포는
`PRESERVE/CORRECT/WITHHOLD/DISCARD/GROUND_NOT_FOUND=1,016/2/117/0/33`이다. 여기서
`PRESERVE`는 내부 정적·runtime·test·replay evidence의 보존이고 external scientific truth가
아니다. `CORRECT` 두 건은 Step 88 O01 capacity-rate 단위 경계와 O03 convergence-return
경계다. `GROUND_NOT_FOUND`는 exact-name config search, executable transfer precondition,
Step 89 missing evidence 및 original optimizer-state field를 빈칸이나 성공으로 바꾸지 않고
그대로 보존한다.

## 2. Immutable Input Coverage

입력은 prose 서술이 아니라 expected parent의 기계 JSON `13`개다. Step 82–89 machine JSON
`12`개와 `Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json`을 `git show`로 읽고, 각
path/mode/blob/byte/raw SHA-256/declared semantic seal을 고정했다. Step 82의 legacy
blank-field pretty semantic projection, Steps 83–89의 compact-LF projection, Phase 066 carry의
legacy compact-no-LF projection을 각각 원래 schema대로 재계산했다. 모든 입력은
`semantic_seal_status=VERIFIED`다.

Lossless coverage는 다음 family를 포함한다.

- Step 82: Python occurrence/blob `129/84`, complete-read attestation `84`, genealogy `64`;
- Step 83: flow/source `100/20`;
- Step 84: behavior/blob graph/coverage/source `140/15/120/20`;
- Step 85: case/input/saved profile/runtime/process pair `13/7/3/26/2`와 owner resolution `1`;
- Step 86: static Python/runtime/golden blob/golden route/guide blob/tool blob
  `69/110/2/23/8/14`, plus exact occurrence projections;
- Step 87: limitation/probe/feature/occurrence/tolerance `1/16/15/20/10`;
- Step 88: candidate/guard/probe/default/open gap/optimizer route/feature/occurrence
  `84/24/27/8/3/3/15/20`와 supplemental optimizer source `1`;
- Step 89: evidence/absent class/bounded obligation/comparison source/saved profile/Phase 066
  input/supplemental input/supplemental route `12/2/2/3/3/6/10/2`, optimizer-field
  availability `25`, saved check `3`, sealed replay `2`, static check `4`, missing-evidence
  key `6`.

## 3. Three Active Phase 067 Owners

The inherited active obligations are not marked resolved. Each receives exactly one bounded
transition and remains open carry:

1. `P065-OBL-0054/P065-S72-F04`: `WITHHOLD` →
   `PHASE-080-BLEND-CLOSURE`. The next gate must declare one consistent blend denominator and
   derive finite-rate host current partition/nonadditivity without treating an in-sample fit as
   material proof.
2. `P066-OBL-0120/P066-P79-07`: `WITHHOLD` →
   `PHASE-080-BLEND-CLOSURE`, relation-linked to `P065-OBL-0054`. Whole-curve in-sample agreement
   does not establish host independence, current partition or nonadditive blend behavior.
3. `P066-OBL-0125/P066-R80-14`: `WITHHOLD` →
   `PHASE-083-IMPLEMENTATION-CONTRACT`. A production loader/schema must dispatch regular-solution
   kernel metadata or reject it explicitly; direct constructor acceptance and exact-name search do
   not establish serialized compatibility.

## 4. New Findings and Existing Routes

Step 88 O01 refines existing `P065-OBL-0061/D74-009` under `PHASE-074-FOUNDATION`; no duplicate
obligation is created. Three new obligations are added, each with one owner, acceptance criterion,
authority ceiling and origin:

- `P067-OBL-0001/P067-S88-O02` → `PHASE-083-IMPLEMENTATION-CONTRACT`: explicitly constrain
  monotonic ordered trajectories or implement chronology-preserving behavior.
- `P067-OBL-0002/P067-S88-O03` → `PHASE-083-IMPLEMENTATION-CONTRACT`: return checked
  convergence/residual state on every root and optimizer exit; links retain the prior root and
  nonconverged-replay owners.
- `P067-OBL-0003/P067-S88-G21` → `PHASE-083-IMPLEMENTATION-CONTRACT`: enforce/test the
  transfer helper's grid/length preconditions or declare the unchecked domain explicitly.

The active set therefore moves from `219` to `222`; the duplicate-check registry moves from `355`
to `358`. Ownerless, multiply-owned, lost inherited and external-authority-promotion counts are all
`0`.

## 5. Authority Ceiling and Preserved Debt

This Gate is an internal code-history disposition Gate only. External scientific authority,
held-out validation, identifiability, material assignment, phase/mechanism identification,
specimen/protocol binding, original optimizer state, stale-PDF release evidence, canonical-model
selection and publication readiness remain false.

The complete Phase 066 carry is embedded without mutation. In particular, Ref. 7 remains
`GROUND_NOT_FOUND` under `P065-OBL-0059`; original optimizer fields remain the 25 obligations
`P066-OBL-0089`–`0113`; held-out and raw specimen/protocol routes remain `P066-OBL-0087` and
`P066-OBL-0086`; material/phase/species routes `P066-OBL-0116`–`0119` remain open; and the nine
stale-PDF release obligations remain assigned to `PHASE-089-LATEX-PDF-RELEASE-QA`. No PDF was
rebuilt and no external or primary-source claim was promoted. Missing complete competing-profile
external synthesis `P066-OBL-0115` remains assigned to
`PHASE-069-STEPS-102-104-MODEL-AND-DATA-SYNTHESIS`.

## 6. Validation and Persistence Boundary

Before either JSON output existed, Python 3.12 and 3.14 both returned the expected RED terminal
`E_SOURCE_MISSING`. This proves the validator does not obtain a content PASS from result/control prose
alone; the generated machine evidence remains mandatory.

The first frozen builder candidate was rejected at independent review with `P0/P1/P2=0/1/0`:
`result_first` and `json_outputs_last` were serialized as true but the default write path did not
enforce the human prerequisites. That candidate and its preview hashes are correction history only.
The repaired default path must verify this result, both ledgers and the active handover as bounded
UTF-8 files carrying the exact Step/Gate/parent/subject/pending-state/next-Step contract before it may
build or atomically replace either JSON output. Fresh validation and full re-review are mandatory.

The first generated JSON-last candidate was then rejected by both runtimes at `E_CONTROL_TOKEN`
because this result heading used `Step 090.1` while the frozen control contract requires
`Step 90.1`. The heading was corrected before regenerating both JSON outputs; the earlier generated
bytes and failed validation are correction history only.

The next regenerated candidate was rejected by both runtimes at
`E_CONTROL_RESULT_GATE_SECTION`: the required explicit gate/next-condition section was absent even
though the same facts appeared elsewhere. This structural defect was corrected before another
JSON-last regeneration; that candidate is also correction history only.

Final validator review then rejected the next content-PASS candidate at `P0/P1/P2=0/1/1` because
filesystem `replace` calls were collected but not enforced and the displayed source-policy control
count was one low. The first count-only repair closed extra-owner insertion and corrected `55` to
`56`, but same-owner substitution still passed, so its `0/1/0` candidate was also rejected. The final
repair seals the exact sorted `(owner, AST call)` inventory as well as owner counts. The same-owner
`pointer_escape` substitution now fails at `E_REPLACE_CALL_SEAL`, and validator re-review returned
`P0/P1/P2=0/0/0`.

On the resulting frozen bytes, Python 3.12 and 3.14 independently returned source-policy `56/56`,
Git argv `28/28`, semantic mutation controls `24/24`, strict-JSON controls `7/7`, traversal
`81,728` nodes/depth `10`, and `PASS_P067_STEP90_1_DISPOSITION`. These are content/precommit facts,
not persistence evidence.

The human result and three control documents are written before the two canonical JSON outputs.
The builder emits compact sorted UTF-8 JSON with one terminal LF and semantic seals; repeated
preview reconstruction must be byte-identical across Python 3.12 and 3.14. The validator must
independently check strict JSON, all denominators and family counts, pointer/hash reciprocity,
exclusive dispositions, the three owner transitions, all `219` inherited obligations, the three
new obligations, owner registry integrity, named-debt non-promotion, source↔carry semantic binding,
the exact-eight repository boundary and staged/persistence states.

The content Gate does not establish its own commit or push. Until exact-eight independent review,
dual-runtime staged validation, commit, push, live-origin/clean verification and dual
`PASS_P067_STEP90_1_PERSISTENCE` complete, the state remains `PASS_PENDING_PERSISTENCE` and
Step 90.2 is blocked.

## Gate and Next Condition

Selected content Gate: `PASS_P067_STEP90_1_DISPOSITION`. Required persistence terminal:
`PASS_P067_STEP90_1_PERSISTENCE`. Step 90.2 remains blocked until the exact-eight child is
committed, pushed, live/clean verified and accepted by both persistence runtimes.

## 7. Exact-Eight Boundary

1. `Codex/work/v1025_phase067/build_phase067_step90_dispositions.py` — A
2. `Codex/work/v1025_phase067/validate_phase067_step90_dispositions.py` — A
3. `Codex/results/PHASE_067_SOURCE_DISPOSITION_MATRIX.json` — A
4. `Codex/results/PHASE_067_CARRY_FORWARD_DELTA.json` — A
5. `Codex/results/PHASE_067_STEP_090_1_DISPOSITION_RESULT.md` — A
6. `Codex/results/PHASE_055_069_FULL_LINEAGE_REAUDIT_EXECUTION_LEDGER.md` — M
7. `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md` — M
8. `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md` — M

No production source or `Claude/**` artifact is modified. The next executable unit is Step 90.2 only
after this exact child has passed both persistence runtimes.
