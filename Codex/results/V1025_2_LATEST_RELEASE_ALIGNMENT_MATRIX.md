# v1.0.25.2 최신 배포본 정합성 행렬

기준 소스: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
기본값 정정 포함: `7b342dd88aad6bf9ff08cb3568da374837008ca7`
작성 브랜치: `codex/v1025_2-physics-conformance`
범위 밖: v1.0.26, `main` 승격, 원 optimizer 상태 재현

상태 뜻:

- `PASS`: 최신 실행 계약과 물리·문건 계약이 일치한다.
- `PARTIAL`: 핵심은 맞지만 조건부 결함 또는 증거 공백이 남는다.
- `FAIL`: 실행·문건·물리 중 둘 이상이 직접 충돌한다.
- `SUPERSEDED`: Phase 044의 구 계보 판정을 최신 현재형으로 쓰면 안 된다.
- `GOVERNANCE`: 사용자 계보 결정 전에는 기술적으로 닫을 수 없다.

| ID | 검토 계약 | 최신 실행/증거 | 판정 | 필요한 조치 |
|---|---|---|---|---|
| LR-001 | 과학적 입력은 최신 v1.0.25.2여야 함 | `3b5fd05`, `7b342dd`를 브랜치에 merge | PASS | 이 addendum 이후 이 계보만 최신 현재형에 사용 |
| LR-002 | fresh import 기본은 열역학 입력 보유 | 흑연 4 + `sic` Si 2 | PASS | default-path gate 추가 |
| LR-003 | 7+7은 명시 opt-in | `use_skew7_default(True)`에서만 7+7 | PASS | mutable global을 명시 profile로 교체 권고 |
| LR-004 | 기본 경로는 다온도 민감 | 288.15→308.15 K 최대 차 0.5252164419568519 | PASS | 수치 회귀 gate로 고정 |
| LR-005 | 7+7 시드는 현 상태에서 T-동결 | 최대 차 6.394884621840902e-14 | PASS | 정온 곡선 표현 전용 경고 유지 |
| LR-006 | `si_case` 검증은 profile과 무관해야 함 | 기본은 거부, 7+7 global opt-in은 잘못된 값을 무시 | PARTIAL | selector를 항상 검증하거나 explicit profile과 분리 |
| LR-007 | 공개 설명은 실제 default/symbol과 일치 | 헤더·주석·docstring에 7-gallery 기본과 삭제 symbol 잔존 | FAIL | 코드 설명만 최신 실행 계약으로 정정 |
| LR-008 | 이론 본문은 물리만, 코드 상태는 지정 절만 | `ch1_sec05b`에 버전/기본/기준선 충돌, `ch1_sec18`에 런타임 경고 동작 | FAIL | 물리 영역과 구현 부록/감사 기록으로 분리 |
| LR-009 | 구현 부록은 실제 공개 인터페이스를 지칭 | `use_legacy_4transition`은 없음, `use_skew7_default`만 callable | FAIL | 허용된 구현 부록에서 이름과 계약 정정 |
| LR-010 | direct14 저장 profile 재구성 | R² 0.99964941790404, BIC -4760.653827485789 | PASS | empirical observation profile로 라벨 고정 |
| LR-011 | direct14를 흑연/Si 상으로 읽지 않음 | host label/order 계약 없음 | PASS | phase/host assignment 금지 유지 |
| LR-012 | 저장 fit을 원 optimizer replay로 부르지 않음 | full precision·prediction·termination·active-set 부재 | PASS | rounded reconstruction으로만 서술 |
| LR-013 | Phase 044 shipped-default 판정 | 당시 7+7, 최신은 4+2 | SUPERSEDED | Phase 054 source probe 사용 |
| LR-014 | 구 source freeze/hash | `eaa019...`, 2,004행은 최신 아님 | SUPERSEDED | 최신 SHA `c281015...`, 2,024행 사용 |
| LR-015 | 새 원고와 새 참조 구현의 내부 대응 | 독립 `conformance_model` 시험 대상 | PARTIAL | 최신 legacy 검증과 분리해 라벨링 |
| LR-016 | conformance test가 최신 legacy default도 검증 | 51 tests는 legacy source를 import하지 않음 | FAIL | 별도 latest-wiring gate 유지 |
| LR-017 | legacy gate PASS가 shipped default를 검증 | v1024 gate가 `use_skew7_default(False)` 강제, 나머지도 explicit profile | FAIL | fresh-import default assertion 추가 |
| LR-018 | `eq:sifr-twophase` 면적 = Q | 해석 항 가중 합 1, 수치 최대 오차 7.77e-16 | PASS | 현 식 유지 |
| LR-019 | `Ω/(RT)≤2` Maxwell gap 없음 | 전 sweep gap weight 0 | PASS | 현 식 유지 |
| LR-020 | `Ω/(RT)→2+` 곡선 연속 | alpha 1/4/8에서 PASS | PASS | 현 식 유지 |
| LR-021 | 임계점 우측 1차 Ω 도함수 발산 | `max|ΔP|/ε` 유한, `/sqrt(ε)`→0 | FAIL | 발산 문장 철회; 질량 상쇄 유도 반영 |
| LR-022 | 기본 배경 상수가 실제 default에 소비됨 | 선언 0.55/0.051, 생성된 양 host Cbg=0 | FAIL | 상수를 wiring하거나 이름을 preset metadata로 제한 |
| LR-023 | keyless 폭의 T 미분 round-trip | 유한차분 8.61688e-05, 보고 0 | FAIL | 같은 폭 정의에서 analytic derivative 계산 |
| LR-024 | keyless Uoc entropy round-trip | 유한차분 -9.46661e-05, 보고 0 | FAIL | entropy path와 Uoc path의 기본 규약 통일 |
| LR-025 | logistic helper가 극단 입력에서도 경고 없음 | overflow/invalid warning 3건 | FAIL | branch-evaluated stable implementation 사용 |
| LR-026 | C-rate 시간 basis가 물리적으로 명시됨 | 같은 물리율 표현의 Lq 비 3600 | FAIL | 초/시간 변환을 API·식·검사에서 하나로 고정 |
| LR-027 | 후보의 정본/검증 지위가 명시됨 | 현재 병행 독립 후보, main 미병합 | GOVERNANCE | 검증 전용/정본 후보/부분 역이식 중 사용자 결정 |

## 해석 주의

LR-010과 LR-002의 R²를 서로 모델 선정 점수로 비교하면 안 된다.
direct14는 블렌드 자료에 직접 57개 파라미터를 맞췄고, LR-002의
진단은 standalone host profile을 고정한 채 `f_Si,Cbg` 두 값만
조절했다. 차이는 “실제 데이터 피팅 가능 여부”가 아니라 “저장 direct14
profile이 배포 기본 배선인가”만 답한다.

LR-018–021은 기존 Phase 044가 이미 같은 최신 식을 대조했다. 이번
행렬은 Claude handover의 3항을 같은 sweep 표로 재표현한 보완이며,
대조가 처음 생긴 것은 아니다.
