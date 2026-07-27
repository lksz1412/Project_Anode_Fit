# Phase 054 — v1.0.25.2 최신 계보 대응 리뷰

작성일: 2026-07-27
작업 브랜치: `codex/v1025_2-physics-conformance`
검토 대상 최신본: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`
핵심 기본값 정정: `7b342dd88aad6bf9ff08cb3568da374837008ca7`
기존 Codex 후보: `2abf019c7fee9bebd84b49cc9530f6983b08a8fa`
기존 후보의 기준점: `ab196b292e14492b647f87a6c0d1d8c9ed0630ab`
최신 계보 병합 커밋: `4316d8a`
제외 대상: v1.0.26 및 `main`의 v1.0.26 계보

## 1. 결론

기존 `2abf019` 리뷰는 최신 v1.0.25.2 대응본이 아니었다. 공통 조상
`ab196b2` 이후 최신 계보의 세 커밋, 특히 기본값 역전을 철회한
`7b342dd`를 포함하지 않았기 때문이다. 이 지적은 맞다.

이미 공개된 브랜치 이력을 강제 재작성하지 않기 위해 rebase/force-push
대신 최신 인정본 `3b5fd05`를 현재 브랜치에 비강제 병합했다. 따라서 이
addendum부터는 최신 v1.0.25.2를 실제 입력으로 읽고 판단한다. `main`은
수정하지 않았고 v1.0.26은 과학적 권위로 사용하지 않았다.

최신 대응 후의 핵심 판정은 다음과 같다.

1. 현 배포 기본값은 흑연 4전이 + `sic` Si 2전이다. 7+7 skew는 명시적
   opt-in이다.
2. 4전이 기본은 288.15→308.15 K에서 최대 `0.5252164419568519`만큼
   변한다. 7+7 opt-in은 `6.394884621840902e-14`로 수치적으로
   T-동결이다.
3. 실제 direct14 피팅의 재현성은 그대로다. 저장 8자리 파라미터로
   `R²=0.99964941790404`, `BIC=-4760.653827485789`를 재현했다.
   다만 이것은 현 배포 기본값도, 흑연/Si 상 분해도 아니다.
4. 새 `conformance_model`과 새 원고의 내부 정합성은 최신 배포 코드의
   기본 배선 검증과 별개의 축이다. 51개 시험이 통과하더라도 최신
   legacy 배포본을 자동으로 검증하는 것은 아니다.
5. Claude의 정칙용액 지적 중 “대조가 없었다”는 주장은 사실이 아니다.
   기존 F-011·PHY-008·Phase 044 probe가 최신과 동일한
   `eq:sifr-twophase`를 직접 대조했다. 다만 최신 handover의 3항을 한
   표로 재현하지 않았던 가독성 결손은 이번 Phase 054 표로 보완했다.
6. 최신 `3b5fd05` 자체도 완전 정합하지 않다. 실행 기본값은 복구됐지만
   코드 헤더·주석·생성자 docstring과 일부 이론 본문에는 철회 전
   “7-gallery 기본” 설명이 남아 있다.

이 리뷰는 “실제 데이터 피팅이 안 된다”는 판정이 아니다. direct14는
주어진 전처리·목적함수에서 실제 데이터를 잘 맞춘다. 여기서 구분하는
것은 적합 성공, 배포 기본 배선, 물리적 상 해석, 다온도 열역학 계약의
네 가지가 서로 같은 주장이 아니라는 점이다.

## 2. 계보와 산출물의 지위

### 2.1 두 검증 축을 분리한다

| 검증 축 | 대상 | 최신 판정 |
|---|---|---|
| 배포본 정합성 | 최신 legacy `Anode_Fit_v1.0.24.py`와 v1.0.25.2 문건 | Phase 044의 구 기본값 전제는 stale, Phase 054가 대체 |
| 후보 내부 정합성 | 새 물리 원고와 새 `conformance_model` | 독립적으로 보존 가능, 단 배포본 최신 대응의 증거는 아님 |

후보 산출물의 정확한 분류는 다음과 같다.

```text
Artifact class:
Independent reconstruction candidate — parallel and non-canonical

Source basis:
latest accepted v1.0.25.2 at 3b5fd05, including 7b342dd

Manuscript lineage:
alternative candidate, not an in-place amendment or release successor

Implementation role:
bounded reference implementation, not the legacy production replacement

Verification role:
verifies the new manuscript/reference pair;
latest legacy release wiring requires separate probes

Promotion status:
not promoted; explicit user lineage decision required
```

“conformance”만으로 부르기에는 범위가 크다. `2abf019`는 58파일,
26,385줄이며 이 중 14,795줄은 생성 manifest다. 이를 제외해도
11,590줄이고, 최소한 다음 세 산출물을 포함한다.

- 독립 재구성 원고 후보: TeX 16개, 1,916줄, 28쪽 PDF
- bounded reference implementation: 1,603줄
- 검증 자산: tests 약 1.8k줄, probes 1,012줄

따라서 이 브랜치는 단순 검사 도구가 아니라 “병행 원고 후보 + 제한된
참조 구현 + 정합성 시험”이다. v1.0.25.3 후속판이나 정본 승격으로
읽혀서는 안 된다.

### 2.2 기존 공개 상태 기록 정정

기존 handover와 execution ledger의 “commit/push/merge performed: no”는
잘못됐다.

| 항목 | 실제 상태 |
|---|---|
| `2abf019` 커밋 | yes |
| 원격 `codex/v1025_2-physics-conformance` 푸시 | yes |
| `main` 병합 | no |
| 정본 승격 | no |
| Phase 054 최신 계보 병합 | 현재 작업 브랜치에서 yes |

기존 파일은 당시 기록으로 보존하고 별도 handover correction으로
supersede한다.

## 3. 최신 배포 기본 배선 재검증

근거 파일:
`PHASE_054_V1025_2_LATEST_SOURCE_PROBES.json`.

| 항목 | 현 기본 | 7+7 skew opt-in | direct14 저장 피팅 |
|---|---:|---:|---:|
| 흑연 성분 수 | 4 | 7 | host 라벨 없는 총 14성분 |
| Si 성분 수 | `sic` 2 | 7 | host 라벨 없음 |
| 중심/폭 T 입력 | 보유 | 결여 | 저장 곡선 파라미터 |
| 288.15→308.15 K 최대 차 | 0.5252164419568519 | 6.394884621840902e-14 | 해당 저장 적합만으로 판정 불가 |
| invalid `si_case` | 거부 | 조용히 무시되어 수용 | 해당 없음 |
| 블렌드 자료에서 `f_Si,Cbg`만 재적합한 R² | 0.07507231361482658 | -1.6132166646788586 | 0.99964941790404 |

마지막 R² 행은 모델 우열 비교가 아니다. 4+2와 7+7 host profile은
standalone host 자료에 맞춘 뒤 `f_Si,Cbg`만 풀었고, direct14는 같은
블렌드 자료에 57개 파라미터를 직접 맞췄다. 이 수치는 오직
“direct14가 배포 기본값에 그대로 연결됐는가”를 구분한다.

최신 계약은 코드 1447–1470행과 일치한다.

- `DEFAULT_GRAPHITE_TRANSITIONS = GRAPHITE_STAGING_LIT`
- `DEFAULT_SI_TRANSITIONS = None`
- `use_skew7_default(True)`일 때만 7+7 전역 전환
- `use_skew7_default(False)`가 4전이 + Si case로 복귀

따라서 Phase 044의 다음 문구는 최신 현재형으로 사용하면 안 된다.

- “current/shipped default = 7+7”
- 기본 7+7의 `R²=-1.613216...`
- 기본 경로가 invalid `si_case`를 수용한다는 일반화
- 구 코드 SHA `eaa019...`와 2,004행 기준의 source freeze

역사적 `ab196b2` 상태 설명으로는 보존할 수 있다. 또한 invalid
`si_case` 결함은 완전히 사라진 것이 아니다. 현 기본에서는 거부되지만
7+7 전역 opt-in 뒤에는 `DEFAULT_SI_TRANSITIONS`가 우선되어 잘못된
`si_case`가 무시된다. 이것은 profile-dependent API 모호성으로 남는다.

## 4. 최신본 자체의 잔존 불일치

### 4.1 실행 계약과 코드 설명이 충돌한다

실행 코드는 4전이 기본으로 고쳐졌지만 다음 설명은 철회 전 상태다.

- 코드 4–6행: 7-gallery 기본과 삭제된 `use_legacy_4transition`을 선언
- 코드 1387–1393행: 기본 전환이 의도됐다고 서술하고 구 스위치를 안내
- 코드 1431–1438행: 7-gallery가 기본이고 4전이가 opt-in이라고 서술
- `BlendedAnodeDQDV` docstring 1597–1599행: 같은 구 기본과 구 함수를 안내
- Codex 구현 부록 61행: 삭제된 `use_legacy_4transition`을 현 인터페이스처럼 표기

Phase 054 probe에서 삭제된 이름은 실제 callable이 아니고, 최신 이름
`use_skew7_default`만 callable임을 확인했다. 소스 본문 안에는 구 이름이
5회 남아 있다.

### 4.2 물리 본문에도 제품 상태 서술이 남아 있다

사용자 문건 규칙은 “본문은 물리 논리를 설명하고, 코드 언급은 지정된
절에서만 하며, 코드는 그 논리를 따른다”이다. 이 기준에서 최신
`ch1_sec05b_gr2L.tex` 177–184행은 정리가 필요하다.

- 177–181행은 7-gallery를 정온 곡선 표현, 4전이를 다온도 열역학
  기준으로 구분해 물리적으로 타당하다.
- 182행은 바로 다음에 “곡선 표현의 기본 해상도가 바뀌었다”고 말해
  실행 기본 복구와 충돌한다.
- 184행은 7-gallery를 “v1.0.25.2의 기준선”으로 다시 부른다.
- 270행의 해상도 사다리는 앞에서 열거한 7-gallery를 누락한다.

물리 본문에는 다음의 모델 영역만 남기는 편이 안전하다.

- 4전이: 열역학·다온도·가역발열 해석 가능
- 7-gallery skew: 현 파라미터 상태에서는 정온 곡선 표현 전용
- gallery 수와 물리 상 수는 같지 않음

버전, 런타임 기본값, 함수명, toggle, 시험 결과는 구현 부록 또는 외부
감사 기록에 둬야 한다.

`ch1_sec18_inputs.tex` 28–29행의 “구현은 ... 경고를 낸다”도 이론
본문에 들어온 구체적 런타임 동작이다. 식별성의 물리 경고는 본문에
남기되, 경고 발생 조건과 구현 동작은 지정 구현 부록으로 옮겨야 한다.

### 4.3 최신 handover의 과대단정

최신 handover는 정본 소스 상태를 찾는 입력으로는 유효하지만 그 안의
판정도 독립 검산 대상이다.

- 흑연 저장값의 최대 `alpha`는 `7.99623012`이며 정확히 상한 `8.0`이
  아니다. 원 optimizer 상태와 active-set 기록도 없다. 따라서 흑연
  alpha의 “경계 포화 확정”보다 “경계 근접·미식별 의심”이 정확하다.
- Si 저장값에는 `0.15`, `8.0`의 정확 경계값이 있다.
- “남은 작업=PDF+P1”이라는 요약은 같은 문서가 남긴 P3/P4
  미검토·미수정 항목과 충돌한다.

## 5. 정칙용액 `eq:sifr-twophase` 대조

### 5.1 Claude 지적 4의 판정

“같은 식을 두 구현이 계산했는데 대조가 없다”는 핵심 주장은 기각한다.

- 기존 `phase044_regsol_threshold_probe.py`는 docstring에서
  `eq:sifr-twophase` measure를 구현한다고 명시했다.
- 기존 JSON은 원식 위치를 직접 지목했다.
- 기존 F-011과 PHY-008은 면적·연속성을 보존하고, 원문의
  “임계점 우측 Ω 도함수 발산” 주장을 불일치로 판정했다.
- 최신 `3b5fd05`의 해당 TeX blob은 기존 `ab196b2`와 동일하다.

다만 기존 probe는 `alpha=1`, 298.15 K, 폭 10 mV, 우측 접근에
집중했고 Claude handover의 3항을 한 표로 전개하지 않았다. 그 좁은
가독성 결손은 인정하여 Phase 054에서 `alpha={1,4,8}`,
`Ω/(RT)={0,1,1.999,2,2.001,3,4,8}` 전 범위 표를 추가했다.

### 5.2 전 범위 결과

근거 파일: `PHASE_054_V1025_2_REGSOL_CROSSCHECK.json`.

| 검산 항목 | 결과 |
|---|---|
| 면적 | PASS: 해석적으로 `(1-2θ_a)+2θ_a=1`, Q를 곱하면 Q |
| 수치 면적 | PASS: ±1 V 창 최대 오차 `7.771561172376096e-16` |
| `Ω/(RT)≤2` gap weight | PASS: 전 행 정확히 0 |
| `Ω/(RT)→2+` 값 연속 | PASS |
| 1차 Ω 도함수 발산 | FAIL: 해당 식에서는 선도 `sqrt(ε)` 질량이 상쇄됨 |

`a=Ω/(RT)=2+ε`에서 gap 질량은 `1-2θ_a=O(sqrt(ε))`다. 그러나 같은
질량이 중앙 stable branch에서 제거되는 동시에
`(1-2θ_a)κ(V-U°)`로 되들어간다. 두 `O(sqrt(ε))` 항은 상쇄된다.
수치적으로 `max|P(2+ε)-P(2)|/ε`는 유한값으로 수렴하고
`/sqrt(ε)`는 0으로 간다.

| alpha | ε=1e-5에서 `max|ΔP|/ε` | `max|ΔP|/sqrt(ε)` |
|---:|---:|---:|
| 1 | 5.899110243134941 | 0.018654624536736084 |
| 4 | 9.68986076514966 | 0.030642030227774848 |
| 8 | 10.770849851837738 | 0.03406041786749438 |

따라서 발산 부재는 `alpha=1` 특수성이 아니다. 기존 probe의
`0.9966587419` 면적은 ±0.12 V 유한창 tail truncation 값이지
전구간 면적 실패가 아니다. 반대로 최신 기록의 `1.000000~1.000165`
중 Q보다 큰 부분은 비음·정규화 kernel의 유한창 손실로 설명할 수
없고 수치 이산화/가중 오차로 분류해야 한다.

## 6. 최신에서도 유지되는 구현 쟁점

기본값 복구가 다음 쟁점을 자동으로 고치지는 않는다.

| 쟁점 | 최신 재검증 |
|---|---|
| keyless transition의 `dw/dT` 보고 | 유한차분 `8.616883453126112e-05 V/K`, 보고값 0 |
| keyless `U_oc(T)`와 entropy round-trip | 유한차분 `-9.46661405376581e-05 V/K`, 보고값 0 |
| eager `np.where` logistic | overflow/invalid warning 3건 |
| C-rate 시간 단위 | 같은 물리율 표현에서 `L_q` 비 `3599.9999999999914` |
| 인과 pad의 중복 첫 점 | pad 점수 0 |
| 5 lag-length 절단 잔류 | `exp(-5)=0.006737946999085467` |
| 기본 배경 상수 | 선언 `0.55/0.051`, 실제 기본 생성자 양 host `Cbg=0` |

추가로 기존 감사의 다음 범주도 최신 수정 범위 밖이므로 해소 증거가
없다.

- 비단조 전위 정렬이 물리 진행 순서를 바꾸는 문제
- variable-T 경로의 부분적 일관성
- lag memory의 finite padding과 fallback 계약
- 단일 온도 apparent activation parameter의 시간단위 의존

이 항목들은 “실제 적합 결과가 좋다”와 양립한다. 관측곡선 회귀 성능과
열역학·동역학 파라미터의 물리적 식별 가능성은 별도 검증축이다.

## 7. 기존 Phase 044/046–053 산출물의 최신 판정

| 산출물 | 최신 지위 |
|---|---|
| `PHASE_044_SOURCE_FREEZE_MANIFEST.json` | `ab196b2` 역사 기록으로 보존; 최신 현재형 주장에는 사용 금지 |
| `PHASE_044_LINEAGE_DIFF.json` | 구 분기 비교 기록; Phase 054 manifest가 최신 입력을 대체 |
| `PHASE_044_CURRENT_SOURCE_PROBES.json` | direct14 및 비기본 probe는 보존; default 7+7 라벨은 폐기 |
| `PHASE_044_V1025_2_SOURCE_FREEZE_AND_COMPARISON_RESULT.md` | F-010/default·source hash 부분 stale; 나머지는 항목별 재판정 |
| `V1025_2_PHYSICS_IMPLEMENTATION_CONFORMANCE_MATRIX.md` | 최신 legacy 대응표로는 superseded |
| `V1025_3_PHYSICS_IMPLEMENTATION_CONFORMANCE_MATRIX.md` | 새 원고–새 참조 구현 내부표로만 유효 |
| `EMPIRICAL_SKEW14_PROFILE.md` | direct14 동결값 유효; shipped-default 서술 stale |
| `PHASE_046_053_V1025_3_RECONSTRUCTION_RESULT.md` | 후보 내부 결과 보존; publication state는 정정 필요 |
| 기존 handover/execution ledger | commit/push 상태를 새 correction이 supersede |

## 8. 권고 작업 순서

### P0 — 사실 기록부터 정정

1. 코드 헤더·철회 전 주석·생성자 docstring을 실제 4+2 기본과
   `use_skew7_default` 계약에 맞춘다.
2. 이론 본문의 버전/기본값/구현 경고 문장을 물리 영역 서술과 구현
   부록으로 분리한다.
3. 정칙용액의 “1차 Ω 도함수 발산” 문장을 철회한다.
4. default path를 직접 측정하는 gate를 추가한다. legacy gate PASS를
   현 global default 검증으로 재사용하지 않는다.

### P1 — 7-gallery 열역학 승격 전 물리 결정을 끝낸다

7-gallery를 다온도·가역발열 경로로 승격하려면 각 gallery 군집이 어느
staging 전이의 `ΔS_rxn`을 상속하는지 먼저 결정해야 한다.

- `n_j=w_jF/(RT_0)` 계산은 산술 문제다.
- `ΔH_rxn,j=-FU_j+T_0ΔS_rxn,j`도 산술 문제다.
- 어느 모전이의 entropy를 상속할지는 물리·구조 배정 문제다.
- 최근접 U 자동배정은 103 mV 군집을 서로 다른 entropy 부모로
  갈라놓으므로 금지한다.

이 결정 전에는 7+7을 정온 관측곡선 표현으로만 둔다.

### P2 — mutable global 대신 명시 profile 계약

전역 switch는 같은 생성자 호출의 의미를 실행 순서에 따라 바꾼다.
불변 profile/configuration을 명시 인자로 전달하고 다음 gate를 둔다.

- fresh import 기본 = 흑연 4 + Si case
- 현 기본의 288/308 K 차가 0이 아님
- 7+7은 명시 opt-in
- opt-in 경로가 T-동결임을 경고
- toggle round-trip 뒤 기본 복구
- invalid `si_case`가 profile과 무관하게 일관되게 거부됨
- 문서에 적힌 공개 symbol이 실제 callable인지 검사

### P3 — 회귀와 물리 추론을 분리

direct14의 좋은 적합은 보존하되 다음 라벨을 고정한다.

- empirical observation profile
- host/phase assignment 없음
- original optimizer state 재현 아님
- rounded stored parameter reconstruction
- BIC는 같은 전처리·목적함수 안에서만 비교
- 경계 근접값은 active-set 자료 없이 “포화 확정” 금지

### P4 — 후보 계보를 사용자 결정으로 닫는다

현재 후보는 정본 패치가 아니다. 다음 중 하나를 명시적으로 선택하기
전까지 parallel/non-canonical로 둔다.

1. 검증 전용 독립 구현
2. 향후 정본 원고 후보
3. 일부 식·시험만 기존 계보로 역이식

어느 선택이든 기존 Claude 원문을 이 브랜치에서 조용히 덮어쓰지 않는다.

## 9. 이번 addendum의 증거 경계

완독·비교한 최신 핵심 입력은 다음과 같다.

- `ARCHIVE_NOTE.md`
- `results/HANDOVER_v1025_2.md`
- `Anode_Fit_v1.0.24.py`
- `test_gates_v1024.py`
- `ch1_sec05b_gr2L.tex`
- `ch1_sec18_inputs.tex`
- `ch3v22_sec02b_sifr.tex`
- 기존 Phase 044 계보 리뷰·source comparison·decision ledger
- 기존 Phase 046–053 reconstruction result·handover·두 conformance matrix
- 새 후보의 원고 architecture와 implementation appendix
- 두 기존 probe와 JSON 전량

최신 입력 해시와 행수는
`PHASE_054_V1025_2_LATEST_SOURCE_FREEZE_MANIFEST.json`에 동결했다.
수치 판정은 두 Phase 054 JSON과 재실행 가능한 세 probe script에
기록했다.

원 optimizer의 full-precision 상태, 예측 배열, 종료 메타데이터,
active-set 상태는 여전히 없다. 따라서 저장 8자리 파라미터의 결정론적
재구성은 가능하지만 “원 optimizer 상태를 재현했다”거나 경계 활성을
확정하지 않는다.
