# Phase 058A v1.0.10–v1.0.13 audit queue 결과

정본일: 2026-07-28  
대상 단계: Phase 058 Step 26.1

## 판정

`PASS_P058_AUDIT_QUEUE`

Phase 056 manifest에서 v1.0.10–v1.0.13의 56 path를 추출하고
45 unique Git blob의 content-addressed queue로 닫았다.

| 항목 | 수 |
|---|---:|
| version paths | 56 |
| unique blobs | 45 |
| duplicated blob groups | 8 |
| full-text blobs | 27 |
| unique text lines | 13,757 |
| text chunks | 61 |
| PDFs | 8 |
| images | 8 |
| NPZ | 1 |
| generated pyc | 1 |

각 record는 대표 path, 모든 occurrence path, version, role,
review mode, size, extent와 300행 이하 text chunk를 보존한다.

## 산출물

- queue:
  `Codex/results/PHASE_058_V1010_V1013_AUDIT_QUEUE.json`
- initial coverage:
  `Codex/results/PHASE_058_V1010_V1013_TEXT_COVERAGE.json`
- generator:
  `Codex/work/v1010_v1013_phase058/generate_phase058_audit_queue.py`

두 번 생성한 hash:

- queue:
  `f799043afc31198322c2865594a91cda94eb06931847ec628409621cfb309843`
- initial coverage:
  `a6bd7e86b87c21fe13ca0b9c162fa543b70bf5b8f1ac8ad46a83ddf8f5dd0a7f`

## 다음 단계

Step 26.2에서 6개 unique theory blob을 모든 행 범위로 검독하고
section/equation/label/claim index와 coverage를 작성한다.
