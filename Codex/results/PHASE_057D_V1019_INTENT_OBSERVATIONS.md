# Phase 057D — v1.0.19 사용자 의도 관찰

정본일: 2026-07-28
세부 Step: 19.3
범위: 3 unique documents, 324 lines
상태: `READ_NOT_YET_CANONICAL`

## Scope

다음 고유 blob을 첫 행부터 끝 행까지 검독했다.

| 경로 | 범위 |
|---|---:|
| `Claude/docs/v1.0.19/FITTING_GUIDE.md` | 1–135 |
| `Claude/docs/v1.0.19/HANDOVER_v1.0.19.md` | 1–38 |
| `Claude/docs/v1.0.19/samples/continuity_scan_report.txt` | 1–151 |

최초 일괄 출력에서 `FITTING_GUIDE.md` 중간이 truncation되었으므로
1–70행과 71–135행으로 나눠 전문을 다시 읽었다.
handover와 continuity report도 각각 독립 범위로 끝까지 확인했다.
이 result를 작성하며 실행한 행번호 부착 재표시는 출력 한도 때문에 일부가
다시 생략되었으나, coverage 판정은 그보다 앞선 분할 전문 검독에 근거한다.

## Provisional Findings

### INTENT-PROV-0020 — 문맥 연속성을 보존한 전면 재작성

`HANDOVER_v1.0.19.md:9-10`은 사용자의 직접 지시를 기록한다.
Ch1은 한 세션에서 물리·화학 논리를 검증하고 전면 재작성한 뒤,
서로 다른 10종 검수와 최종 수정을 거쳐야 했다.
기존 세부 구조는 버릴 수 있지만 물리 논리는 모두 보존하고,
문건만 다루며 코드는 배제하라는 조건도 함께 있다.
`HANDOVER_v1.0.19.md:19-24`는 Ch2에도 같은 방식을 적용했다고 기록한다.

판정: 강한 `USER_REQUIREMENT`, `PRESERVE`.
최종 문건은 구판에 문단을 덧대는 changelog식 patchwork가 아니라
한 권으로 읽히는 논리 구조를 새로 세워야 한다.

### INTENT-PROV-0021 — 이론 문건이 과학 권위이고 코드는 하류 산출물

`HANDOVER_v1.0.19.md:26-30`은 v1.0.19의 Ch1·Ch2를 authoritative로
선언하고, 코드는 그 문건에 맞춰 개정했다고 명시한다.
향후 개정도 문건에서 코드로 흐르는 `doc-leads` 원칙을 유지하고,
코드 편의에 맞춘 역방향 축소를 금지한다.

이는 다음 두 층을 분리한다.

1. 과학 의존성: 이론 문건 → 계산 명세 → 코드.
2. 표현 경계: 이론 본문에는 코드 함수명·변수명·버전 작업사를 넣지 않음.

판정: `USER_REQUIREMENT`, `PRESERVE`.
이번 최종 작업에서도 물리 채택식을 먼저 닫고,
코드는 그 식을 100% 반영하는 하류 구현으로만 개정해야 한다.

### INTENT-PROV-0022 — 자산 보존은 낡은 framework 보존이 아님

`HANDOVER_v1.0.19.md:10,13-16`은 기존 틀 폐기를 허용하면서도
이전본의 물리 자산을 빠짐없이 추출해 보존하라고 한다.
실제 수행 기록은 Ch1 336개, Ch2 133개 자산 체크리스트를 사용했다.

따라서 다음은 서로 다른 요구다.

- 보존 대상: 검증된 식, 가정, 부호, 단위, 극한, 반례, 문헌 근거.
- 재설계 대상: 장·절 배열, 설명 순서, 반복, forward reference,
  코드와 작업 이력이 섞인 서술.

판정: `PRESERVE`.
다만 과거 자산 수량과 “무결” 판정 자체는 새 재감사의 대체물이 아니며,
Phase 058–066에서 과학적 타당성을 다시 판정한다.

### INTENT-PROV-0023 — 수치 연속성과 골든 회귀는 실험 검증이 아님

`FITTING_GUIDE.md:112-128`은 정규화 잔차, 면적 보존,
13/13 bit-exact 회귀, 합성 round-trip과 유한차분 검증을 설명한다.
동 문건 `:128`은 유한차분 round-trip이 수치 무결성 가드일 뿐
통계적 식별성 증명이 아니라고 스스로 한정한다.

`samples/continuity_scan_report.txt:13-142`는 dense grid에서
spike 후보 0, \(U_{\mathrm{oc}}(\bar{x})\) 단조성,
문건 예제와의 수치 일치를 보였다.
그러나 이 입력은 코드가 생성한 자기 모델 곡선이며,
공개 LIB 실험 데이터 holdout이 아니다.

판정:

- 연속성·회귀·round-trip 결과는 `INTERNAL_CONSISTENCY`.
- 재료 물리와 파라미터의 실험적 타당성은 `UNVERIFIED`.
- 두 판정을 합쳐 “물리 검증 완료”로 부르는 것을 `REJECT`.

### INTENT-PROV-0024 — LCO 핵심 물성은 권위값이 아니며 미폐쇄

`FITTING_GUIDE.md:10,21-31`은 LCO의 \(\Omega_j^{\mathrm{cat}}\)와
\(\Delta H_{a,j}^{\mathrm{cat}}\)가 미배정이고 문헌 anchor도 찾지 못했다고
명시한다. 제시된 수천–1.3만 J/mol 및 25–59 kJ/mol 범위는
흑연과 일반 계면 활성화 스케일에서 가져온 “경향 anchor”이며,
신뢰값이 아니라 피팅 출발점일 뿐이다.

`FITTING_GUIDE.md:66`과 `HANDOVER_v1.0.19.md:27,34-38`은
다온도 LCO 전자항의 실측 \(T\) 복원, 비가역열 3분해,
LCO tier-2/3 실측 초기값이 미구현 또는 외부 실측 대기라고 적는다.

판정:

- 해당 숫자를 LCO 기본 물성으로 승격하는 것은 `REJECT`.
- LCO 고전압·도핑 데이터에 대한 물리 폐쇄는 `UNVERIFIED`.
- 문헌 anchor와 실제 데이터가 확보될 때까지 opt-in
  `EMPIRICAL_ONLY` 출발점 이상으로 취급하지 않는다.

### INTENT-PROV-0025 — \(\bar{x}\) 진입점은 유용한 구조 확장이나 검증 범위가 제한됨

`FITTING_GUIDE.md:68`은 전하보존 음함수의 유일근으로
\(\bar{x}\to U_{\mathrm{oc}}\)를 구하고,
그 위에서 엔트로피 계수와 가역열을 계산하는 추가 진입점을 설명한다.
`HANDOVER_v1.0.19.md:26-27`은 이 확장을 기존 경로에 additive하고
기존 골든은 bit-exact라고 기록한다.

continuity report의 `:86-142`는 해당 솔버의 수치 연속성, 단조성,
부호 교대와 worked example 일치를 확인한다.
하지만 이는 solver와 문건 식 사이의 수치 자기일관성 검증이다.

판정:

- SOC/조성축 실험과 연결하는 architecture 후보로 `PRESERVE`.
- 유일근 존재 범위, multi-phase plateau, 비단조 full-cell mapping,
  실제 조성 측정 불확도에 대한 검증은 `UNVERIFIED`.

## Conflicts to Carry Forward

1. v1.0.19이 “물리 골격 오류 0”라고 선언했지만,
   같은 기록은 LCO 핵심값과 다온도 전자항을 미폐쇄로 둔다.
   완결 선언과 적용 범위를 분리해 재판정해야 한다.
2. 자산 336/336 및 133/133 보존은 누락 방지 증거이지
   각 자산의 물리 타당성 증거가 아니다.
3. \(n\), 현상학적 two-phase 폭, 단일 Einstein mode,
   lumped activation tail의 재료별 적용 범위를 문헌과 실데이터로 검증해야 한다.
4. \(\bar{x}\) 음함수 솔버의 수학적 유일성 주장을
   채택된 free-energy/phase model 전체에서 다시 증명해야 한다.
5. LCO 방향 규약은 반쪽전지와 full-cell 전압 부호를 분리해
   실제 데이터 pipeline에서 end-to-end 시험해야 한다.

## Coverage Status

- 이 batch의 3문건은 `READ`.
- 누적 Phase 057 coverage: 22문건, 1,458행.
- 아직 Phase 057 최종 `VERIFIED`가 아니다.

## Next

Step 19.4:
v1.0.20에서 처음 등장한 고유 intent 문건 81개, 17,041행을
계획·실행 원장·결과·인계·검토 산출물의 논리 순서로 나눠
첫 행부터 끝 행까지 검독한다.
