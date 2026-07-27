# Phase 057C — v1.0.14–v1.0.18.2 사용자 의도 관찰

정본일: 2026-07-28
세부 Step: 19.2
범위: 12 unique documents, 689 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 고유 blob을 첫 행부터 끝 행까지 검독했다.

| 경로 | 범위 |
|---|---:|
| `Claude/docs/v1.0.14/FITTING_GUIDE.md` | 1–99 |
| `Claude/docs/v1.0.14/HANDOVER_v1.0.14.md` | 1–26 |
| `Claude/docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md` | 1–29 |
| `Claude/docs/v1.0.15/HANDOVER_v1.0.15.md` | 1–29 |
| `Claude/docs/v1.0.15/CLOSING_v1.0.15.md` | 1–105 |
| `Claude/docs/v1.0.16/FITTING_GUIDE.md` | 1–115 |
| `Claude/docs/v1.0.16/HANDOVER_v1.0.16.md` | 1–28 |
| `Claude/docs/v1.0.17/HANDOVER_v1.0.17.md` | 1–32 |
| `Claude/docs/v1.0.18.1/HANDOVER_v1.0.18.1.md` | 1–23 |
| `Claude/docs/v1.0.18.2/FITTING_GUIDE.md` | 1–125 |
| `Claude/docs/v1.0.18.2/HANDOVER_v1.0.18.2.md` | 1–29 |
| `Claude/docs/v1.0.18.2/ROADMAP_future_physics.md` | 1–49 |

두 번의 일괄 출력에서 중간 truncation이 발생했다.
잘린 kickoff, v1.0.15 handover/closing, v1.0.16 fitting guide 및
v1.0.18.2 fitting guide의 누락 범위는 별도 호출로 다시 읽었다.
특히 `CLOSING_v1.0.15.md`는 1–60행과 61–105행으로 나눠 전체를 재확인했고,
v1.0.18.2 fitting guide의 누락 60–67행도 별도 확인했다.

## Provisional Findings

### INTENT-PROV-0010 — 이론 본문과 구현 정보의 위치 분리

`HANDOVER_v1.0.14.md:5-8`은 사용자가 코드 연계를 단방향으로 두고
문건 안에서 코드 변수명을 금지했다고 기록한다.

`CLOSING_v1.0.15.md:11-16`은 교재의 렌더링 본문에 코드 함수명,
내부 작업 라벨, 구현 대응과 버전 이력을 노출하지 말라고 명시한다.

`HANDOVER_v1.0.17.md:17,23`은 이 원칙에 따라 제목의
“코드 진행”을 “계산 진행”으로 바꾸고 코드·구현·dict·진입점·토글을
물리·모델 표현으로 정리했다고 기록한다.

판정: `USER_REQUIREMENT` 후보, `PRESERVE`.
현재 사용자의 “이론 본문에는 물리·화학 논리만, 코드 언급은 지정 절/외부 계약만”
요구와 직접 이어진다.

### INTENT-PROV-0011 — 최상위 문건 헌법

`CLOSING_v1.0.15.md:7-32`는 사용자 발언을 verbatim으로 기록하며
다음 우선순위를 최상위 헌법으로 둔다.

1. 교과서 수준의 안정적이고 객관적인 register.
2. 논문 수준의 깊이와 면밀한 완결 유도.
3. 수식만 따라가도 물리·화학 논리를 이해할 수 있는 수식 중심 구조.

하위 규칙은 다음과 같다.

- 각주 압축보다 완결 유도 우선.
- 출발식, 연산, 중간식, 결과식의 사슬을 생략하지 않음.
- 부호·차원·극한을 검산.
- 실측 검증과 자기일관성 검증을 분리.
- DOI와 1차 문헌 공백 및 evidence tier를 명시.
- 절 도입과 다음 절의 연결을 보존.

`HANDOVER_v1.0.14.md:5-8` 및
`HANDOVER_v1.0.15.md:9-10`에서도 같은 방향이 반복된다.

판정: 강한 `USER_REQUIREMENT`, `PRESERVE`.

### INTENT-PROV-0012 — 전문 정독과 검증 없는 완료 금지

`CLOSING_v1.0.15.md:36-60`은 다음을 사용자 지적 기반 운영 규칙으로 둔다.

- 새 문제를 제안하기 전에 과거 계획·handover·result·ledger와 현행 본문을 확인.
- 대상 base 문건을 부분 검색이 아니라 전문 정독.
- 사용자의 명시 선택을 작업자의 효율 판단으로 바꾸지 않음.
- import, grep, sample 통과만으로 완료 또는 golden으로 선언하지 않음.
- 해석적 극한, 수렴과 round-trip을 실제로 검증.

`CLOSING_v1.0.15.md:64-80`은 base 절을 읽지 않아 실제 코드 폭과
worked example을 다르게 쓴 사건을 재발 방지 근거로 기록한다.

판정: 명시적인 `USER_REQUIREMENT`, `PRESERVE`.
이번 전체 재감사의 직접 운영 근거다.

### INTENT-PROV-0013 — 이산 전압 격자 완전 퇴출

`HANDOVER_v1.0.15_KICKOFF.md:5-16`에는 사용자의 직접 발언이 남아 있다.
실제 양·음극 전압 샘플에서 값을 바로 계산할 수 있는데
작업 격자→변환→재변환을 거치는 것은 실데이터 피팅 효율을 해치므로
이산 전압 격자를 완전히 제거하라는 결정이다.

`HANDOVER_v1.0.15.md:9-19`은 점별 기억 적분으로의 전환을 기록한다.

판정: `USER_REQUIREMENT`, `PRESERVE`.
단, v1.0.15의 점별 구현이 시간 인과성과 비단조 trajectory까지 올바르게
처리하는지는 Phase 059/067에서 별도 검증한다.

### INTENT-PROV-0014 — 문건과 코드의 상호충실성, 표현 층위는 분리

`HANDOVER_v1.0.15.md:9-10`은 Ch1·Ch2·코드의 세 축을 동등하게 두고
“코드에 없는 내용 X + 문건 내용은 코드에 반영”하는 양방향 동기를
사용자 지시로 기록한다.

이는 v1.0.14의 “문건 내 코드 변수명 금지”와 모순이라기보다
과학 내용의 상호충실성과 본문 표현 위치를 구분한 것으로 해석할 수 있다.

- 과학 의존성: 이론이 코드의 권위이며 코드가 채택 이론을 반영.
- 표현 경계: 이론 본문에는 코드 기호와 구현 이력을 노출하지 않음.

판정: 위 두 층의 분리는 `PRESERVE` 후보.
후속 기록에서 현재 사용자의 100% 반영 요구와 최종 연결한다.

### INTENT-PROV-0015 — 폭의 온도의존은 선험 고정이 아니라 데이터 판정

`CLOSING_v1.0.15.md:84-94`는 다음 사용자 결정을 기록한다.

- 폭은 맨값 \(w\)보다 \(n\)을 우선 fit하고 \(w=nRT/F\)를 물리 anchor로 사용.
- 실제 측정 온도를 입력.
- 여러 온도에서 per-temperature \(n\)을 먼저 확인.
- 상수 \(n\)이 실패하면 상수 \(w\), 그다음 최소 \(n(T)\)로 단계 확장.
- \(n(T)\)를 쓰면 가역 발열의 configurational 항도 같은 \(n(T)\)로 동기.

v1.0.16 guide/handover는 이 기능을 구현했으나
실제 어느 전이에 어떤 폭 모델을 쓸지는 실데이터가 결정한다고 명시한다.

판정:

- 데이터로 온도의존을 판정한다는 원칙은 `PRESERVE`.
- \(n\)의 물리 해석과 \(w=nRT/F\)의 보편 타당성은 `UNVERIFIED`.
- 후속 상전이·PSD·수송 이론에 따라 `CORRECT`될 수 있다.

### INTENT-PROV-0016 — 위험한 물리 확장은 안전 기준선과 분리

`HANDOVER_v1.0.18.1.md:8-19`은 사용자가 두 버전을 요구했다고 기록한다.

- v1.0.18.1: register/정합만 정리한 안전 폴백.
- v1.0.18.2: Einstein vibrational correction을 더한 물리 확장판.

v1.0.18.2 guide/handover는 `theta_E`가 없는 기본 경로를 bit-exact로 두고,
실제 적용에는 준양자 범위를 가로지르는 온도점 세 개 이상이 필요하다고 명시한다.

판정:

- 검증 전 물리 확장을 기본값과 분리하는 원칙은 `PRESERVE`.
- Einstein 단일모드 모델 자체는 `THEORY_ONLY` 또는 opt-in 후보이며,
  실제 host 데이터 없이는 기본 권위가 없다.

### INTENT-PROV-0017 — PSD는 영구 금지가 아니라 forward 확장 후보

v1.0.10 계열은 ill-posed한 \(\rho(U_{\mathrm{app}})\) 역산과
PSD 모델 재도입을 금지했다.
그러나 `ROADMAP_future_physics.md:37-41`은 측정 PSD를 입력으로
Gibbs–Thomson shift를 forward 적분하는 나노입자 확장을 명시적으로 제안한다.

따라서 과거 금지는 모든 PSD 물리를 폐기한 것이 아니라,
근거 없는 역산 또는 마이크론 흑연에서 과대해석하는 것을 막은 것으로
재해석해야 한다.

판정:

- ill-posed inverse PSD를 피하는 것은 `PRESERVE`.
- measured PSD forward integration은 `THEORY_ONLY` 후보이며
  후속 문헌·데이터로 재검증.

### INTENT-PROV-0018 — 실제 데이터 미폐쇄가 계속 승계됨

v1.0.14–v1.0.18.2의 handover들은 반복해서 다음을 이월한다.

- multi-temperature per-T 폭 진단.
- two-phase 폭의 실제 온도의존.
- LCO \(\Omega\), \(dH_a\), 전자항의 실값.
- 고온/저온 곡률 및 Einstein/electronic 항 분리.
- 실측 PSD, EIS, rate-series를 필요로 하는 확장.

판정: 해당 버전들의 “완료”는 내부 계획과 capability 구현의 완료다.
실험 데이터 기반 재료 모델 완결을 의미하지 않는다.

### INTENT-PROV-0019 — 이론 본문은 작업 일지가 아니어야 함

`CLOSING_v1.0.15.md:11-16,23-32`는
구판 비교, 폐기 이력, 작업 단계, 방어적 자기고백과 구현 라벨을
이론 본문에서 제거하라고 명시한다.

`CLOSING_v1.0.15.md:75-80`은 changelog식 patchwork가 문건을
누더기로 만든다는 사용자 지적을 기록한다.

판정: `USER_REQUIREMENT`, `PRESERVE`.
작업 이력은 별도 result/ledger에만 둔다.

## Conflicts to Carry Forward

1. \(n\)을 물리적 비이상/분산 인자로 해석하는 근거가 충분한가.
2. two-phase 폭을 현상학적 \(w\) 하나로 두는 것이 상전이·PSD·수송 분리를
   방해하는가.
3. v1.0.15 점별 적분이 비단조 trajectory와 current reversal에서 인과적인가.
4. Einstein 단일모드가 graphite/LCO/Si host의 실제 phonon DOS를
   대신할 수 있는 적용 범위.
5. \(\Omega(\xi)\), Cahn–Hilliard, Butler–Volmer/Nernst–Planck,
   measured PSD forward model 중 어떤 것이 핵심 모델에 필요한가.
6. 과거 “코드에 없는 내용 X”를 현재의 이론서 깊이와 어떻게 조화할지.
   현재 기준은 이론적 배경은 허용하되 계산 채택식과 이론 전용식을
   외부 계약에서 구분하는 방식이 유력하다.

## Coverage Status

- 이 batch의 12문건은 `READ`.
- 누적 Phase 057 coverage: 19문건, 1,134행.
- 아직 Phase 057 최종 `VERIFIED`가 아니다.

## Next

Step 19.3:
v1.0.19에서 처음 등장한 고유 intent 문건을 전문 검독한다.
