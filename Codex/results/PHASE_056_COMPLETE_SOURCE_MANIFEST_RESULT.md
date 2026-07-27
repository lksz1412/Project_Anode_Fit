# Phase 056 — 전체 파일 manifest와 중복 지도 결과

정본일: 2026-07-28
계획 Steps: 9–17
Gate: `PASS_P056_COMPLETE_MANIFEST`

## Summary

기준 commit `3b5fd05`의 v1.0.10–v1.0.25.2 tracked tree를 대상으로
모든 path, Git blob, 역할, 검독 방식 및 파일별 extent를 기록했다.

총 1,520개 path와 862개 고유 blob이 확인됐으며 최초 집계와 일치했다.
동일 blob의 복제 발생 658건은 248개 중복 group에 연결했다.
서로 다른 blob은 내용이 유사해 보여도 별도 검독 대상으로 유지했다.

이 phase는 목록화와 비파괴 메타데이터 조사만 수행했다.
어떤 source도 내용 전문 검독 완료로 표시하지 않았다.

## Step Range

| Step | 수행 내용 | 결과 |
|---:|---|---|
| 9 | 전체 tracked path와 blob hash 추출 | 1,520 paths |
| 10 | 버전·확장자·역할·text/binary 분류 | 완료 |
| 11 | text 행 수·encoding·content hash 기록 | 완료 |
| 12 | PDF 페이지 수와 직접 대응 `.tex` 후보 기록 | 완료 |
| 13 | PNG 해상도·모드·format·frame 기록 | 완료 |
| 14 | NPZ key·dtype·shape·비파괴 수치 범위 기록 | 완료 |
| 15 | 동일 blob의 모든 path를 dedup group으로 연결 | 248 groups |
| 16 | 고유 blob별 검독 방식과 UNREAD queue 배정 | 862 groups |
| 17 | path/blob/coverage 합계와 parse·재현성 검증 | PASS |

## Files Created

- `Codex/work/v1010_v1025_2_reaudit/build_source_manifest.py`
- `Codex/results/PHASE_056_V1010_V1025_2_SOURCE_MANIFEST.json`
- `Codex/results/PHASE_056_V1010_V1025_2_READ_COVERAGE.json`

## Manifest Totals

### Path totals

| 검독 방식 | path 수 |
|---|---:|
| `FULL_TEXT` | 1,356 |
| `FULL_PDF` | 70 |
| `FULL_IMAGE` | 85 |
| `BINARY_INTROSPECTION` | 8 |
| `GENERATED_ONLY` | 1 |
| 합계 | 1,520 |

### Unique-blob review queue

| 검독 방식 | 고유 blob 수 |
|---|---:|
| `FULL_TEXT` | 746 |
| `FULL_PDF` | 64 |
| `FULL_IMAGE` | 49 |
| `BINARY_INTROSPECTION` | 2 |
| `GENERATED_ONLY` | 1 |
| 합계 | 862 |

### Duplicate accounting

- 중복 path: 0
- 동일 내용 복제 발생: 658
- 둘 이상의 path를 가진 blob group: 248
- metadata inspection error: 0

## Read Coverage State

- `UNREAD`: 862
- `IN_PROGRESS`: 0
- `READ`: 0
- `VERIFIED`: 0

목록을 만들거나 행·페이지 수를 계산한 행위는 전문 검독으로 간주하지 않았다.

## Execution Evidence

manifest 생성:

```text
python Codex/work/v1010_v1025_2_reaudit/build_source_manifest.py
```

검증 범위:

```text
manifest entries == 1520
unique manifest paths == 1520
unique manifest blobs == 862
coverage groups == 862
flattened coverage paths == 1520
all coverage status == UNREAD
all coverage arrays empty
FULL_TEXT lines >= 1
FULL_PDF pages >= 1
FULL_IMAGE width,height >= 1
inspection_error_count == 0
```

generator source는 쓰기 없이 compile 검사를 통과했다.
생성기를 연속 두 번 실행했을 때 산출물 hash가 동일해 deterministic함을 확인했다.

## Artifact Hashes

- source manifest SHA-256:
  `60f6fbaa356bbba1c1fbc1e718496880ad2ca3930c481384d18ca404f52ceaef`
- read coverage SHA-256:
  `aa14dce8120cb8dee1f68b180dde1dd1545d4d1c57ddd611adb89b6b1ce053f7`

## Validation

- 기준 path count 일치: PASS
- 기준 unique blob count 일치: PASS
- path 중복 없음: PASS
- 모든 path가 dedup group에 연결됨: PASS
- 모든 고유 blob이 read queue에 연결됨: PASS
- PDF/PNG/NPZ metadata 조사 오류 없음: PASS
- JSON parse: PASS
- generator compile: PASS
- deterministic regeneration: PASS
- `git diff --check`: PASS

## Confirmed Non-Changes

- v1.0.10–v1.0.25.2 원천 파일 변경 없음.
- Claude 폴더 변경 없음.
- 이론 본문·생산 코드 변경 없음.
- read coverage의 허위 완료 표시 없음.
- v1.0.26 입력 없음.

## Gate

`PASS_P056_COMPLETE_MANIFEST`

## Open Issues / Decision Queue

- PDF의 직접 동명 `.tex`가 없는 경우 include graph와 Git 이력으로 생성 관계를
  Phase 058–066에서 별도 확인해야 한다.
- `.pyc` 1개는 generated artifact로 등록됐으며 source 누락 여부를
  관련 버전 감사에서 확인해야 한다.
- role 분류는 검독 순서 제어용이며 과학적 권위를 의미하지 않는다.

## Next

Phase 057 Step 18:
plan, result, handover, change log와 ledger의 고유 blob을 시간순 read queue로
정렬하고 사용자 의도 복원을 시작한다.
