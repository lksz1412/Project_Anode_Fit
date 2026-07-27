# Phase 057BB — commit claim–patch matrix result

정본일: 2026-07-28
세부 Step: 20.2
상태: `PASS_P057_COMMIT_PATCH_MATRIX`

## Outputs

- generator:
  `Codex/work/v1010_v1025_2_reaudit/generate_phase057_commit_claim_matrix.py`
- matrix:
  `Codex/results/PHASE_057_COMMIT_CLAIM_MATRIX.json`
- matrix SHA-256:
  `b2b85c56449675d1976dd75dce14ceb89b0ed129b3cbe18b32a1e79ccab4b151`

generator를 두 번 실행해 같은 SHA-256을 확인했다.

## Result

```text
related commits                              229
first-parent changed-file events           2,381
commits with completion marker               102
empty first-parent patches                     0
merge commits in this set                      0
subject-scope/no-patch-artifact triage commits 70
```

### Completion-marker commit의 실제 patch scope

102개 모두 narrative/report artifact를 바꿨다. 그중:

```text
theory .tex                    53
PDF                            52
code .py                       23
test/gate-named path           16
machine record                 13
image                          11
only narrative/governance      37
```

한 commit이 여러 scope에 속하므로 합은 102보다 크다.

### Subject가 지목했지만 같은 commit patch에 직접 artifact가 없는 scope

```text
THEORY_TEXT       30
CODE              20
TEST_OR_GATE      16
DATA_OR_FIT        8
PLAN               5
LEDGER_OR_LOG      3
BUILD_OR_PDF       1
HANDOVER           1
```

이는 자동 오류 판정이 아니다. 예를 들어 “코드 무변경 확인”은
의도적으로 `.py`를 바꾸지 않을 수 있고, “재빌드는 나중에”라는
문장도 `빌드` token을 포함한다. 이 필드는 Step 20.3–20.4에서
원문 증거를 찾기 위한 triage다.

## Material Findings

### 1. commit title은 실행 증거가 아니다

`PASS`, `GREEN`, `전건`, `bit-exact`를 포함한 제목이라도
test output, command transcript, machine result, raw data가 같은
patch에 없을 수 있다. 반대로 test file을 바꾸지 않고 기존
test를 실행했을 수도 있다.

판정:

- commit subject는 claim source로 보존한다.
- 과학·실행 acceptance는 result body, command, exit status,
  input blob, output hash까지 연결해야 한다.
- patch artifact 부재만으로 false라 하지 않고 `EVIDENCE_GAP`
  후보로 둔다.

### 2. 대형 version commit은 대부분 copy-forward다

changed-file count 상위에는 다음이 있다.

- v1.0.25.2 작업본 배치: 153 files
- v1.0.25 생성: 142 files
- v1.0.25.1 생성: 142 files
- v1.0.24.1 archive: 132 files
- v1.0.24 R0 baseline copy: 70 files
- v1.0.23 P0 copy: 67 files

파일 수는 새로운 물리의 양이 아니다. version snapshot의
대량 `ADD`와 실제 수정 `MODIFY`를 분리해야 한다.

### 3. “문건 완료”와 “전체 연구 완료”는 서로 다른 claim이다

completion-marker commit 37개는 narrative/governance 범위만
수정했다. 해당 작업이 문건 검수나 handover 작성이라면 제목과
patch가 일치할 수 있다. 그러나 이를 코드·실험·물리 검증
완료로 확대하면 안 된다.

### 4. 첫-parent full patch를 보아야 숨은 범위가 드러난다

intent-document history만 보면 문건 계보만 보이지만 실제
commit에는 `.tex`, `.py`, PDF, image, JSON, test, ledger가
함께 들어간 경우가 많다. matrix는 229 commit의 저장소 전체
path/status를 보존해 후속 판정이 일부 파일만 보고 내려지지
않도록 했다.

## Validation Boundary

matrix는 commit subject의 scope token과 실제 changed path를
연결한다. 다음은 아직 하지 않았다.

- 문건 본문 속 `완료`, `PASS`, `정본`, `무변경`, `bit-exact`
  문장의 line-level 추출
- 각 주장에 대응하는 실제 command/output 판정
- `CONFIRMED`, `OVERCLAIMED`, `PARTIAL`, `UNVERIFIED` 최종 분류

## Next

Step 20.3:
271문건에서 completion/authority/invariance claim을 줄 번호,
문맥, blob, commit과 함께 추출하고 false-positive를 수동
검독할 수 있는 claim ledger를 만든다.
