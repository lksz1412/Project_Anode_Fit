# Phase 066 Step 081.1 — Source Disposition and Carry-Forward Result

## 1. 판정

선택 Gate는 `PASS_P066_STEP81_1_DISPOSITIONS_WITH_CONCERNS`다. Phase 066 내부
계보 감사와 owner routing은 완결했지만 Ref. 7 원문, 원 실험 데이터의 exact binding,
원 optimizer state, 독립 held-out 검증 및 최종 PDF build는 남아 있으므로 Phase ceiling은
`CONDITIONAL_P066`다. 외부 과학·재료·실험·출판 권위는 승격하지 않는다.

Step 80 exact-eight commit `ec02d8e0017c4441d9d02c08e22ad432b8c47bc5`는 이미
push/live-remote 검증과 Python 3.12/3.14 `PASS_P066_STEP80_PERSISTENCE`를 통과했다.
Step 81.1의 expected parent는 이 commit이고 expected subject는
`audit(phase066): disposition v1025 lineage evidence`다.

## 2. Source occurrence disposition

Step 76에서 고정한 manifest occurrence `433`개와 unique blob `167`개를 전수 연결했다.
각 occurrence는 exactly one disposition row를 가지며 supplemental narrative `2`개는
manifest denominator에 합치지 않았다.

| 항목 | 결과 |
|---|---:|
| occurrence | 433 |
| unique blob | 167 |
| `PRESERVE` | 424 |
| `CORRECT` | 3 |
| `WITHHOLD` | 6 |
| `DISCARD` | 0 |
| `GROUND_NOT_FOUND` occurrence | 0 |
| supplemental | 2 |

`CORRECT=3`은 시각 결함 2개와 v1.0.25.2 production source의 stale
header/docstring/comment 충돌 blob 1개다. `WITHHOLD=6`은 v1.0.25.2의 stale PDF
3 occurrence와 이름과 실제 형식이 다른 snapshot 3 occurrence다. Stale PDF의 inventory
identity는 `PRESERVE`하되 release/build evidence만 `WITHHOLD`했다. 같은 PDF blob의
v1.0.25.1 occurrence는 역사 증거로 보존하고 v1.0.25.2 occurrence만 changed TeX에 대한
release evidence에서 보류했다. 따라서 blob projection은 `PRESERVE-only=160`,
`CORRECT-only=3`, `WITHHOLD-only=1`, context-mixed `PRESERVE/WITHHOLD=3`이다.

## 3. Process와 supplemental 경계

Release/routed process commit은 `17/20`, routed-only는 `3`이다. Supplemental을 건드린
commit은 `5`, supplemental-only commit은 `3`이다. 모든 process row는 원 changed-path
route와 record hash를 유지하며 release/routed/path-level orphan은 `0`이다.

Supplemental `2/655행`은 raw/LF SHA-256, byte/line extent, full-read status, 관련 routed
commit 및 acceptance를 별도 row로 유지했다. 이 두 문건을 433 occurrence 또는 167 blob
projection에 합치지 않았다.

## 4. Phase 057 intent routing

Phase 065가 보존한 Phase 057 observation은 `82`, Phase 066 신규 AO–AW는 `95`,
AY shared reference는 `10`이다. 전체 unique universe는 `177`, numeric ID `0228–0404`
연속이며 lost/duplicate new ID는 `0/0`이다. AY `0395–0404`는 기존 origin hash,
owner/state/target을 그대로 재사용해 신규 obligation을 만들지 않았다. AX `0388–0394`
7개는 prior-only history로 그대로 남는다.

신규 95개는 각자 하나의 evidence-bounded owner와 acceptance를 갖는다. 사용자 결정·완료된
운영 사실 12개는 `BOUNDED_HISTORICAL`, 나머지 83개는 Phase 072–090의 해당 검증 owner로
`OPEN_CARRY`했다. 비식별성은 Phase 081, equation/model separation은 Phase 082,
구현·default contract는 Phase 083/085, 실제 데이터 validation은 Phase 086, 문건·red-team·
PDF 검증은 Phase 087–089에 배치했다.

## 5. Step 76–80 carry

Step 76–80의 `68`개 disposition record를 보존했다.

- Step 76 visual defect `2`: Phase 089 open correction.
- Step 77 raw binding/held-out/nonconvergence와 optimizer contract: evidence identity와
  calibration acceptance를 분리했다.
- Step 78 original optimizer state `25` field를 각각 `GROUND_NOT_FOUND`로 유지하고,
  stored/replay vector 사실 및 curve-equivalence와 parameter-identifiability를 분리했다.
- Step 79 claim `8`: Direct14의 bounded empirical replay만 보존하고 physical/external/phase/
  proposition 권위는 별도 axis에서 모두 false 또는 WITHHOLD다.
- Step 80 route `16`과 evidence column `9`: runtime observation은 보존하되 stale source
  contradiction `4`는 correction owner에, serialized regsol route `R80-14`는 원 owner
  `P067-CODE-HISTORY`에 open carry했다.

Ref. 7의 Step 79 observation `P066-P79-08`은 bounded reference로만 남겼다. Active
obligation은 기존 `D74-006`/`P065-OBL-0059` 하나뿐이고 owner는
`PHASE-071-PRIMARY-SOURCE-ACQUISITION`, status는 `GROUND_NOT_FOUND`다.

## 6. Carry totals와 authority ceiling

Phase 065 observation/active/owner registry `192/94/192`를 byte-semantic snapshot으로
보존했다. Phase 066 신규 registry까지 합한 owner universe는 `355`, active obligation은
`219`다. ownerless, multiply-owned, lost inherited ID, AY duplicate obligation 및 external
authority promotion은 전부 `0`이다.

이 active count는 서로 다른 source field와 사용자 intent identity를 lossless하게 보존한
수치다. 동일 Ref. 7 semantic chain은 중복 active로 세지 않았고, Step 77 broad optimizer
contract는 bounded reference로만 두어 Step 78의 25 field-level GROUND_NOT_FOUND와 이중
계수하지 않았다.

## 7. 검증과 독립 검토

Validator는 immutable input `11`개를 commit/path/blob/raw SHA-256으로 다시 읽고 두 JSON을
독립 재구성한다. Strict JSON, semantic seal, occurrence/blob/supplemental/process projection,
Phase 065 snapshot, Phase 057 `177` universe, owner cardinality, Ref. 7 single owner,
empirical/physical axes, stale-PDF dual axis, determinism `2/2`를 검사한다.

Named negative controls는 occurrence drop/duplicate, blob projection drift, supplemental fold,
stale-PDF false closure, process orphan, inherited record loss, AY duplicate, ownerless active,
Ref. 7 promotion, empirical→physical promotion, optimizer-state substitution, AO–AW loss 및
Step 80 contradiction false closure뿐 아니라 dangling relation과 bounded record의 extra-active
승격을 거부한다. Current staged evidence는 semantic negative `16/16`, source-policy attack
`9/9`, JSON pair rollback transaction `1/1`, determinism `2/2`다.

독립 검토의 첫 초안 P1 15개는 현재 artifact에 반영했다. 특히 Ref. 7 이중 active,
Step 79/80 owner 손실, stale PDF 과잉 WITHHOLD, Phase 057 union 누락, authority-axis 병합,
process path orphan, supplemental identity 축약, held-out pointer 오류 및 optimizer 25-field
축약을 교정했다. Fresh dual-runtime staged validation 전에는 이 문서의 content Gate를
persistence 완료로 해석하지 않는다.

## 8. 생성·수정 파일과 다음 조건

- `Codex/work/v1025_phase066/build_phase066_step81_dispositions.py`
- `Codex/work/v1025_phase066/validate_phase066_step81_dispositions.py`
- `Codex/results/PHASE_066_SOURCE_DISPOSITION_MATRIX.json`
- `Codex/results/PHASE_066_CARRY_FORWARD_DELTA.json`
- 본 결과 문건
- 두 execution ledger
- `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`

현재 containing commit은 `PENDING_AT_PRECOMMIT_BY_DESIGN`이다. Exact-eight stage,
Python 3.12/3.14 content/staged validation, 독립 재검토, commit/push/live-remote verification,
그리고 양 runtime `PASS_P066_STEP81_1_PERSISTENCE` 뒤에만 Step 81.2를 시작한다.
