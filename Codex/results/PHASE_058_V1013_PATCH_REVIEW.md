# Phase 058 v1.0.12 → v1.0.13 exact patch 판정

정본일: 2026-07-28  
대상: Phase 058 Step 31.3  
기계 판정:
`Codex/results/PHASE_058_V1013_PATCH_ADJUDICATION.json`  
재현 검산기:
`Codex/work/v1010_v1013_phase058/validate_phase058_v1013_patch.py`

## 결론

v1.0.13은 단순 편집본도, 완성된 물리 폐쇄본도 아니다.

정확한 성격은 다음과 같다.

1. Chapter 1에 통계역학 Part 0을 실제로 추가하고 기존 이론을
   대규모로 재배열했다.
2. 생산 코드의 callable 30개 가운데 27개는 AST가 같고, 세 메서드만
   바뀌었다.
3. 그 세 메서드와 class-level default 변경은 scalar dQ/dV,
   entropy coefficient, LCO charge/discharge facade 및 LCO 기본
   transition의 온도 응답을 실제로 바꾼다.
4. graphite 기본 vector 경로가 보존된 것은 맞지만 “모든 거동이
   v1.0.12와 같다”는 주장은 틀리다.
5. 일부 수정은 명백한 결함 수리지만, \(n_j\)의 물리적 해석과 LCO
   default 재배치는 공개 데이터 검증이 없어 그대로 승격할 수 없다.
6. regression harness는 개선됐지만 새로 바뀐 세 경로를 gate하지
   못하며 현재 환경에서 원형 그대로 portable하지도 않다.

최종 판정은

`V1013_IS_A_REAL_THEORY_RESTRUCTURE_AND_TARGETED_EXECUTABLE_PATCH_NOT_A_PHYSICAL_CLOSURE_RELEASE`

이다.

이 문서는 계보·코드 정합성 감사 문서이므로 코드 변경을 직접
언급한다. 최종 이론 문건에는 이 내용을 옮기지 않고, 물리·화학적
논리와 가정 계층만 서술한다.

## 1. 비교 경계와 재현성

비교 대상은 v1.0.12와 v1.0.13 디렉터리의 대응 파일이다.
v1.0.13 계보는 첫 commit
`e33a3ac1e931bef87481cbc3af2adcabf39acbc5`부터 최종 commit
`5995d640e4e0d697a85238d1f1d9f5064749f802`까지 21개 commit이다.

대응되는 text 파일 8쌍의 exact patch는 다음과 같다.

| 역할 | 추가 | 삭제 |
|---|---:|---:|
| 생산 코드 | 96 | 57 |
| fitting guide | 15 | 14 |
| LCO heat demo | 16 | 15 |
| Chapter 1 | 1,570 | 994 |
| Chapter 2 | 162 | 163 |
| plot script | 5 | 5 |
| sample | 15 | 14 |
| regression | 11 | 6 |
| **합계** | **1,890** | **1,268** |

v1.0.13에는 이 밖에 24행 handover와 144행 graph suite가
추가됐다. 모든 원본 파일의 SHA-256과 위 line count는 기계 판정
파일에 고정했고 validator가 다시 계산한다.

## 2. 이론 문건의 실제 변화

### 2.1 Chapter 1

Chapter 1은 2,358행에서 2,934행으로 늘었다.

| 지표 | v1.0.12 | v1.0.13 |
|---|---:|---:|
| equation label | 86 | 111 |
| `\boxed` 출현 | 23 | 31 |
| section 계열 heading | 41 | 51 |

기존 equation label 86개는 모두 남았고 25개가 추가됐다. 그중
24개는 통계역학 Part 0의 `eq:sm-*` 계열이며 나머지는
`eq:lco-sigmaslot`이다. 기존 label 가운데 식 본문이 달라진 것은
10개다.

따라서 v1.0.13이 first-principles 출발점을 실제로 보강했다는
주장은 보존한다. 다만 Step 31.1에서 확정했듯 다음은 아직
완결되지 않았다.

- 이상 lattice-gas에서 logistic/Nernst로 가는 사슬은 복구할 수
  있으나, nonideal interaction과 관측 peak width는 같은 기호로
  흡수하면 안 된다.
- 여러 transition을 단순 합산한 것이 하나의 공통 partition
  function에서 유도된 상 topology라는 보장은 없다.
- 평형 분포에서 출발한 방향 convention이 전극·전지 charge와
  discharge의 부호까지 자동으로 정해 주지 않는다.

그러므로 “Part 0이 생겼다”와 “전체 모델이 통계역학적으로
폐쇄됐다”는 서로 다른 명제다.

### 2.2 Chapter 2

Chapter 2는 777행에서 776행으로 사실상 같은 규모이며 equation
label 22개, boxed 식 7개, heading 18개도 같다. 식 본문이 바뀐
label은 `eq:dxidT`, `eq:gj`, `eq:implicit`, `eq:muV`,
`eq:single_config` 다섯 개다.

즉 Chapter 2의 변화는 새 장을 추가한 것이 아니라 entropy와
implicit differentiation의 해석을 조정한 것이다. 이 조정 가운데
고정 empirical width에서 configurational term을 제거한 것은
보존할 수 있지만, arbitrary fitted \(n_j\)에 \(n_jR/F\) 항을
붙인 것은 미시적 configurational entropy의 유도가 아니다.

## 3. 생산 코드의 exact patch

두 생산 모듈은 callable이 각각 30개다. 함수·메서드의 AST를
정규화해 비교하면 27개는 같고 다음 세 개만 달라졌다.

- `GraphiteAnodeDischargeDQDV.curve`
- `GraphiteAnodeDischargeDQDV.dqdv`
- `GraphiteAnodeDischargeDQDV.entropy_coefficient`

추가되거나 삭제된 callable은 없다. 그러나 다음 class/module data도
바뀌었으므로 함수 개수만으로 실행 동등성을 주장해서는 안 된다.

- base class의 `_delith_is_discharge=True`
- LCO subclass의 `_delith_is_discharge=False`
- LCO electronic transition을 index 1, \(x_{\rm MIT}=0.50\)에서
  index 0, \(x_{\rm MIT}=0.85\)로 이동
- LCO index 0과 1의 \(\Delta H_{\rm rxn}\)을 각각
  \(-377400\to-391016.1\), \(-389174\to-375554.4\) J/mol로 변경

이 결과 v1.0.13은 “문서만 바뀐 버전”이 아니다.

## 4. 실행 거동 판정

### 4.1 graphite 기본 vector 경로

평형, 여섯 개 current/direction 조합, 기본 entropy coefficient를
포함한 8개 vector probe에서 v1.0.12와 v1.0.13의 최대 절대차는
0이었다.

이는 기존 graphite 기본 array 사용례가 보존됐다는 강한 증거다.
그러나 probe 경계 밖 scalar와 non-default transition까지 같다는
뜻은 아니다.

### 4.2 scalar dQ/dV 결함

배포 default에서 \(V=0.12\ {\rm V}\), \(T=298.15\ {\rm K}\),
\(I=1\), \(Q=1\), \(s=+1\)인 scalar 호출 결과는

| 대상 | dQ/dV |
|---|---:|
| v1.0.12 | 6.703622100010492 |
| v1.0.13 | 7.201379816667805 |
| 평형 reference | 7.201379816667805 |

다. v1.0.12의 상대오차는 \(-6.9119770\%\)다. 전압 array의 span이
0이 되는 scalar 입력에서 grid-dependent cutoff가 작동한
결함이며, v1.0.13의 degenerate-span guard는 실제 결함 수정으로
보존한다.

### 4.3 entropy coefficient

\(\xi=0.8\) probe에서 `n=2` transition은

\[
 -0.0463735\ {\rm mV/K}
 \longrightarrow
 +0.0730819\ {\rm mV/K}
\]

로 바뀐다. 이는 실행 거동의 실제 변경이다. 그러나 Step 31.2에서
검증했듯 현 \(n\)은 전자수·자리수·축퇴도에서 유도된 다중도가
아니라 empirical width ratio다. 따라서 변경식이 가정한
\(w=nRT/F\)를 미분한 대수적 자기일관성은 있어도, 그 항을 실제
configurational entropy라고 승격할 수 없다.

반대로 `n` 없이 \(w=0.04\ {\rm V}\)만 준 transition은

\[
 -0.0463735\ {\rm mV/K}
 \longrightarrow
 -0.1658289\ {\rm mV/K}
\]

로 바뀐다. \(w\)를 온도에 무관한 empirical width로 선언했다면
그 폭에서 configurational \(R/F\) 항을 생성하지 않는 것이
맞다. 이 수정은 “고정 폭이라는 가정 아래의 대수적 온도 모델”로
보존한다.

### 4.4 LCO 방향 facade

저수준 \(s=+1\) 경로를 기준으로 facade를 비교하면 다음과 같다.

| 비교 | 최대 절대차 |
|---|---:|
| v1.0.12 charge vs \(s=+1\) | 0.3608779 |
| v1.0.12 discharge vs \(s=+1\) | 0 |
| v1.0.13 charge vs \(s=+1\) | 0 |
| v1.0.13 discharge vs \(s=+1\) | 0.3609552 |

v1.0.13은 cell charge를 LCO delithiation에 연결한다. 전극 반응과
전지 운전 방향을 분리하는 원칙에 부합하므로 이 facade 수정은
보존한다.

### 4.5 LCO default 재배치

electronic transition과 \(\Delta H_{\rm rxn}\)의 재배치는
온도별 LCO curve와 entropy를 실제로 바꾼다.

| 온도 | direct \(s=+1\) dQ/dV 최대차 | entropy 최대차 |
|---:|---:|---:|
| 278.15 K | 1.26578 | 0.389294 mV/K |
| 298.15 K | 0.00248660 | 0.357811 mV/K |
| 318.15 K | 0.953977 | 0.325680 mV/K |

298.15 K의 dQ/dV만 보면 거의 같은 것처럼 보이지만, 온도를
움직이면 두 default는 크게 갈라진다. 공개 LCO 데이터와 독립
열역학 근거가 없으므로 \(x_{\rm MIT}=0.85\) 재배치를 물리적으로
검증된 상 할당으로 읽으면 안 된다. 현 단계에서는 Tier C
placeholder다.

## 5. regression과 검증 주장

v1.0.13 regression runner의 다음 개선은 보존한다.

- 기본 동작이 golden capture가 아니라 verify다.
- 알 수 없는 mode는 exit code 2로 실패한다.
- 생산 코드 경로는 환경변수로 덮어쓸 수 있다.
- graphite array 13개를 golden과 비교한다.

그러나 한계도 명확하다.

- Python `assert`는 0개이며 mismatch를 `sys.exit`로 gate한다.
- golden 경로는 Windows 절대경로 literal이고 환경변수 override가
  없어 현재 환경에서는 원형 그대로 portable하지 않다.
- 13개 output은 graphite array 경로뿐이다.
- 바뀐 scalar guard, 두 entropy branch, LCO default 및 방향
  facade를 전혀 gate하지 않는다.
- graph suite와 sample은 report script이지 failure gate가 아니다.

현재 환경에서 golden 13개 가운데 bit-exact는 1개지만
\(10^{-12}\) 허용오차에서는 13개가 모두 통과했고 최대 절대차는
\(2.6645\times10^{-15}\)다. 따라서 “13/13 bit-exact”는 당시
source environment의 기록일 수는 있어도 portable한 현재 상태
주장으로 보존할 수 없다.

## 6. 주장별 최종 처분

| ID | 주장 | 처분 |
|---|---|---|
| P13-01 | genuine Part 0 추가 | Step 31.1 수정과 함께 보존 |
| P13-02 | 문서만 바뀌고 실행 거동은 불변 | 기각 |
| P13-03 | legacy graphite vector path 보존 | probe한 8개 경우에 한해 보존 |
| P13-04 | 모든 v1.0.12 거동 보존 | 기각 |
| P13-05 | scalar span guard가 실제 결함 수정 | 보존 |
| P13-06 | 고정 \(w\) entropy gate | 가정 경계와 함께 보존 |
| P13-07 | arbitrary \(n_j\)가 config entropy를 유도 | 기각 |
| P13-08 | LCO charge → delithiation facade | 보존 |
| P13-09 | \(x_{\rm MIT}=0.85\)가 실험 검증됨 | 미검증 Tier C |
| P13-10 | regression이 모든 새 거동을 gate | 기각 |
| P13-11 | 13/13 bit-exact가 portable | 기각 |
| P13-12 | 남은 물리·부호 결함이 0 | 기각 |
| P13-13 | 계획 범위의 남은 작업이 없음 | 기각 |

## 7. 정본으로 가져갈 것과 폐기할 것

### 보존

- 통계역학 Part 0의 pedagogical 출발점
- scalar degenerate-span 결함 수정
- cell direction과 electrode delithiation을 분리한 LCO facade
- 고정 empirical \(w\)에서 가짜 config term을 만들지 않는 처리
- golden capture보다 verify를 기본으로 한 regression 운영 원칙

### 수정 후 보존

- ideal lattice-gas derivation
- \(w(T)\)를 미분한 entropy 식
- legacy graphite vector 회귀 결과
- LCO transition의 전기적·구조적 후보 해석

### 폐기 또는 강등

- 현 \(n_j\)를 미시적 다중도라고 부르는 표현
- LCO \(x_{\rm MIT}=0.85\)를 검증된 상 할당으로 단정하는 표현
- graphite-only regression을 전체 모델 gate로 부르는 표현
- “남은 결함 0”, “planned work 0” 같은 closure 선언

## 8. 다음 단계

Step 31.4에서는 “50-page급 상세성”이 실제 설명 폐쇄를 뜻하는지
검토한다. 분량·equation 수가 아니라 다음을 문단 단위로 분류한다.

1. 같은 가정을 반복한 부분
2. 유도는 있으나 적용 범위·한계가 빠진 부분
3. LCO 구조·산화환원·상전이 설명이 placeholder인 부분
4. 유한 전류에서 peak shift, suppression, broadening으로 가는
   동역학 연결이 선언에 머문 부분
5. 실험 observable과 latent thermodynamic state 사이 observation
   model이 빠진 부분

이 분류가 끝나야 v1.0.13에서 무엇을 정본의 교육적 뼈대로
보존하고 무엇을 새로 써야 하는지 확정할 수 있다.
