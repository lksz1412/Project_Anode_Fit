# Phase 058 v1.0.13 50-page 설명 폐쇄성 판정

정본일: 2026-07-28  
대상: Phase 058 Step 31.4  
기계 matrix:
`Codex/results/PHASE_058_V1013_CLOSURE_AUDIT.json`  
구조 추출기:
`Codex/work/v1010_v1013_phase058/inspect_phase058_v1013_closure.py`  
재현 검산기:
`Codex/work/v1010_v1013_phase058/validate_phase058_v1013_closure.py`

## 결론

v1.0.13 Chapter 1의 50쪽은 단순한 빈 분량이 아니다. 이상 격자기체,
전기화학 평형, 보존식, logistic peak, 인과 완화, LCO 전자 엔트로피
등을 실제로 길게 유도한 교육적 자산이 있다.

그러나 그 50쪽이 다음 사슬을 닫지는 못했다.

\[
\text{미시 자유에너지}
\to\text{재료별 상 topology}
\to\text{비평형 상태방정식}
\to\text{측정 observable}
\to\text{공개 데이터 fit}
\to\text{불확실성·반증}
\]

최종 판정은

`V1013_HAS_REAL_PEDAGOGICAL_DEPTH_BUT_50_PAGES_DO_NOT_CLOSE_THE_PHYSICS_CHEMISTRY_OBSERVATION_OR_VALIDATION_CHAIN`

이다.

따라서 v1.0.13은 “정본의 교육적 뼈대 후보”이지 정본 자체가 아니다.
분량을 그대로 늘리는 방향도, 전부 폐기하는 방향도 맞지 않는다.
이상계 유도와 부호·보존식을 추려 재배치하고, 비이상 상평형,
국소상태 동역학, 재료 화학, 관측 모형과 공개 데이터 검증을 새로
닫아야 한다.

## 1. 50쪽의 실제 구성

Chapter 1은 2,934 source lines, 50 PDF pages, heading block 51개,
equation label 111개다. Chapter 2는 776행, heading block 18개,
equation label 22개다.

Chapter 1을 내용 경계로 나누면 다음과 같다.

| 구간 | 행 | 분량 | 식 label | 코드 식별자 |
|---|---:|---:|---:|---:|
| front matter | 1–200 | 200 | 0 | 6 |
| 기호·실험조건 mapping | 201–315 | 115 | 1 | 39 |
| 통계역학 Part 0 | 316–816 | 501 | 28 | 0 |
| graphite operational spine | 817–1834 | 1,018 | 43 | 73 |
| LCO 이론 | 1835–2629 | 795 | 30 | 10 |
| 넓게 잡은 구현 경계 | 2630–2852 | 223 | 9 | 86 |
| 부호 검산·문헌 | 2853–2934 | 82 | 0 | 1 |

Part 0의 501행은 실제 first-principles 설명량이다. Graphite
operational spine 1,018행도 보존식과 유한전류 식을 포함한다.
LCO 795행도 빈 문장이 아니라 regular solution, Sommerfeld,
entropy decomposition을 전개한다.

문제는 “식이 많다”가 아니라 각 식이 재료·관측·검증 단계까지
연결됐는지다.

## 2. 장문 반복의 성격

### 2.1 이상 partition–logistic 사슬

같은 이상 평형 사슬이 다음 네 범위에서 겹쳐 설명된다.

- Chapter 1 Part 0: 316–816행
- Chapter 1 평형 중심: 872–944행
- Chapter 1 폭·진행률: 1106–1317행
- Chapter 2 분배함수·logistic: 111–218행

이는 전부 무의미한 복사는 아니다. Part 0은 미시 출발점,
후반은 계산 순서, Chapter 2는 entropy 연결이라는 교육적 역할이
다르다. 그러나 같은 이상 결과를 여러 번 전개하는 동안
\(\Omega\ne0\)의 implicit isotherm, convexification, binodal,
공통 host에서의 다중상 topology는 닫히지 않았다.

정본에서는 이상계 유도는 한 번 완결하고, 이후 장에서는 정의된
정리와 적용 범위를 참조해야 한다. 반복 분량은 nonideal closure에
재투자하는 것이 낫다.

### 2.2 방향·부호 사슬

방향 규약은 201–315, 817–845, 1046–1105, 1733–1784,
1913–1993, 2853–2908행에 걸쳐 반복된다.

이 반복은 실제로 LCO charge와 cathode delithiation을 연결하는
v1.0.13 수정을 낳았으므로 가치가 있다. 그러나 같은 부호 계약을
여러 번 적은 것은 실험적 유효성이나 상평형의 방향 의존성을
증명하지 않는다.

정본에서는 다음 세 층만 분리해 한 번 정의한다.

1. 반응 진행도와 전극 lithiation/delithiation
2. half-cell/full-cell charge/discharge label
3. 측정 전압·전류의 부호

그 다음 장은 이 계약을 재인용해야 한다.

### 2.3 폭 식

literal \(w_j=n_jRT/F\) 또는 \(n_jRT/F\)는 Chapter 1에 18회
나온다. 하지만 반복 횟수는 \(n_j\)의 미시적 정체를 만들지 않는다.
Step 31.2에서 확인했듯 현재 \(n_j\)는 전자수, 자리수, 상수 축퇴도
중 어느 것에서도 유도되지 않는다.

같은 식을 solid solution의 평형 폭, two-phase의 현상학적 폭,
heterogeneity의 유효 폭에 모두 쓰는 순간 설명이 아니라
원인 압축이 된다.

## 3. 이론 문건과 코드의 분리 규칙

Chapter 1에는 `\code{...}`가 215회 있고 51개 heading block 중
31개에 코드 식별자가 있다.

기존 `sec:lco-code` 2630–2752행만 허용된 구현 절로 보면
그 안은 4회, 밖은 211회다. 범위를 더 넓혀 LCO code 절,
전체 입력표, facade까지 2630–2852행을 구현 경계로 인정해도
안은 86회, 밖은 129회다. 그 넓은 경계 밖에서도 코드가 등장하는
heading block은 28개다.

따라서 v1.0.13 Chapter 1은 사용자가 확정한 문건 원칙을 구조적으로
만족하지 않는다.

- 이론 본문: 물리·화학·수학·실험 observable만
- 구현: 이론과 동일한 기호·단위·부호를 반영
- traceability: 별도 conformance matrix 또는 한 개의 명시적
  구현 경계

Chapter 2는 코드 식별자 0회라 이 분리 원칙에 훨씬 가깝다. 다만
Chapter 2의 물리식도 width/entropy 의미 오류가 있으면 고쳐야
하며, 코드 언급이 없다는 사실만으로 물리 정본이 되지는 않는다.

## 4. 물리 폐쇄성

### 4.1 보존할 이상계

다음은 명시적 적용 범위와 함께 보존할 수 있다.

- grand partition에서 occupancy로 가는 유도
- 이상 lattice-gas의 Nernst/logistic
- \(Q_j|\mathrm d\xi_j/\mathrm dV|\)의 면적·높이·FWHM
- 전하 보존에 따른 전이별 용량 가중 합
- cell label과 electrode reaction direction의 분리
- \(S_e=(\pi^2/3)k_B^2Tg(E_F)\)의 Sommerfeld 끝점 식과
  eV–J, particle–mole 단위 다리

이 항목들은 정본의 기초 장과 검산 예제로 사용할 가치가 높다.

### 4.2 비이상 상평형은 미완

v1.0.13은 \(\Omega>2RT\)에서 비볼록 정규용액 곡선과 spinodal을
유도한다. 그러나 spinodal gap을 그대로 평형 plateau나 측정
hysteresis의 폐쇄식으로 쓰면 안 된다.

필요한 것은 다음의 분리다.

- homogeneous stable/metastable/unstable branch
- binodal과 common tangent
- convexified equilibrium free energy
- nucleation barrier와 경로 의존 metastability
- ensemble transformation과 measured hysteresis

현재의 방향별 \(\gamma_j,h_{\eta,j}\) shift는 원고 스스로도
“유도되지 않는 현상학적 축소 인자”라고 인정한다. 따라서
regular-solution 수학은 보존하되 hysteresis closure 선언은
기각한다.

### 4.3 다중 transition 합은 조건부

여러 logistic peak의 선형 합은 서로소 독립 reaction extent와
capacity partition이 정의될 때는 성립한다. 그러나 같은 graphite
host의 staging 상들이 공통 조성을 공유할 때는 각 peak가 독립
두상계라는 보장이 없다.

정본에서는

- 독립 site class 모델,
- mutually exclusive multi-state 모델,
- 연속 조성 자유에너지의 phase topology

를 구분하고, 어느 재료에 어느 모델을 쓰는지 먼저 정해야 한다.

## 5. 사용자가 출발점으로 제시한 현상

사용자의 핵심 관측은 다음 두 가지다.

1. 저온에서, 무전류보다 정전류 조건에서 dQ/dV peak가 낮아지고
   넓어진다.
2. 상전이 활성화 장벽은 온도, 전류, 전극 전위의 영향을 받아야
   한다.

### 5.1 v1.0.13이 잡은 것

1계 완화식은 평형 목표를 유한 속도로 따라가는 causal reduced
model이며, Arrhenius relaxation time은 저온에서 커진다. 따라서
평형 logistic 폭이 저온에서 \(T\)에 비례해 좁아지더라도,
kinetic lag가 더 빨리 커져 measured peak를 넓히고 낮출 수 있다는
정성 방향은 맞다.

이는 정본의 nonequilibrium 출발점으로 보존할 수 있다.

### 5.2 아직 닫지 못한 것

v1.0.13은 그 경쟁을 조건 matrix의 실제 곡선·데이터로 보여주지
않았다.

- 배포 default는 rate broadening이 활성화되지 않는다.
- \(L_V\) 직접 입력은 \(I\to0\) 환원을 우회할 수 있다.
- 문서화한 C-rate–capacity 계약에는 factor 3600 문제가 있다.
- affinity는 local electrode potential 함수가 아니라 cut에서
  동결된 transition scalar다.
- 장벽 보정 \(\Delta H_a-\chi\Omega\)도 진행 중 전극 전위와
  조성에 따라 갱신되는 local barrier가 아니다.
- lowpass/평형 분기 handoff는 원고 자체 계산으로 기본
  \(\nu=2\)에서 약 23% 점프가 난다.
- 전 curve 밖에 지속되는 cycle-history state가 없어 닫힌
  hysteresis memory가 아니다.

따라서 현재 모델에는 \(T\)와 \(|I|\)의 축소 의존성은 있으나,
사용자가 요구한 \(E_a(T,I,U,\text{state})\) 또는 동등한 local
free-energy barrier closure는 없다.

### 5.3 다음 정본의 동역학 요구

다음은 서로 분리해야 한다.

\[
\Delta G^\ddagger
=\Delta G^\ddagger(T,\xi,\eta,\text{phase state},\text{history})
\]

- \(T\): Eyring/Arrhenius와 entropy of activation
- \(I\): 직접 독립변수가 아니라 flux·overpotential·concentration
  field를 통해 들어오는 구동
- \(U\): local electrochemical affinity와 charge-transfer barrier
- \(\xi\): 조성·상분율·상경계 이동
- history: nucleation, metastability, path state

그 위에서 peak broadening, skew, shift와 height suppression을
면적 보존과 함께 검증해야 한다. 수치 branch의 면적 손실을
물리적 peak suppression으로 오인하면 안 된다.

## 6. Graphite 폐쇄성

Graphite 네 peak parameterization은 실제 데이터 표현에 쓸 수 있는
출발점이다. 그러나 v1.0.13 default는 검증된 재료 상수가 아니다.

- 네 transition 모두 `n=1`이라 저장된 `w`가 가려진다.
- 모든 초기 \(\Omega\)가 298 K에서 \(2RT\)보다 큰데 원고는 일부를
  solid solution으로 fit될 것으로 “기대”한다.
- stage assignment, capacity, \(\Delta H,\Delta S,\Delta H_a\)는
  공개 데이터 fit과 holdout으로 확정되지 않았다.
- ensemble \(\rho(U_\mathrm{app})\) 적분은 설명식일 뿐 실행
  observation layer가 아니다.

따라서 graphite는 “generic kernel + rough initials” 단계다.
물리적으로 문제없는 최종 조합이라고 부를 수 없다.

## 7. LCO 폐쇄성

### 7.1 세 transition

T1 MIT, T2/T3 order–disorder라는 재료 서술은 유용한 review seed다.
그러나 세 transition에 같은 scalar regular-solution/logistic을
복사한 것은 material-specific free energy의 유도가 아니다.

원고도 다음을 인정한다.

- LCO \(\Omega_j^\mathrm{cat}\) 수치는 미배정
- 미배정이면 hysteresis branch 비활성
- transition initial은 Tier C
- \(x\leftrightarrow\xi\)는 단순 선형보간
- multi-temperature \(T^2\) 곡률은 현행 구현에 없음

따라서 세 peak 위치·상 귀속과 default는 미검증이다.

### 7.2 electronic entropy

Sommerfeld 끝점 식은 보존할 수 있다. 그러나
\(g(E_F,x)\)를 composition-logistic으로 둔 것은 Fermi–Dirac
energy occupancy에서 유도되지 않는다.

전자 에너지 \(E\)에 대한 Fermi 함수와 조성 \(x\)에 따른 MIT
발현 곡선은 서로 다른 축이다. 함수 모양이 같다는 사실은
composition gate의 미시적 증명이 아니다. 원고가 연속
\(g(E_F,x)\)의 1차 문헌이 없다고 밝힌 점은 정직하며, 따라서
그 gate는 현상학적 가정으로 남겨야 한다.

더구나 유도한 관측 식별 신호는 \(U(T)\)의 \(T^2\) 곡률인데
현재 구현은 \(x,T\)를 기준점에 동결해 선형 \(U(T)\)만 만든다.
문건–코드 100% 반영 조건을 만족하지 않는다.

### 7.3 도핑·고전압 안정성

도핑은 현재

\[
\Omega^\mathrm{pure}\to\Omega^\mathrm{dop}
\]

의 감소와 별도 중심 shift로만 표현된다. 이것은 상전이 smear의
한 축일 뿐 “고전압까지 버티는 doped LCO”의 화학을 설명하지
못한다.

빠진 것은 적어도 다음이다.

- dopant species, site, valence와 charge compensation
- Co oxidation 및 oxygen redox
- oxygen loss와 surface reconstruction
- Co migration, stacking/phase transition
- microcracking·strain·transport·interfacial impedance
- electrolyte oxidation과 upper cutoff coupling

원고의 T4 약 4.55 V O3→H1-3 전이는 1902행에서 명시적으로 범위
밖이다. 그러므로 현재 사용자 목표의 doped high-voltage LCO를
다뤘다고 볼 수 없다.

## 8. Silicon과 graphite–silicon composite

v1.0.13 이론·코드에는 silicon 경로가 0개다. Graphite+silicon
composite의 병렬 용량, 전극 내 전위 공유, Si alloying plateau,
상변태, 팽창·응력, SEI·비가역 용량, particle/contact heterogeneity도
없다.

이는 작은 보완 절이 아니라 별도 재료 자유에너지와 관측 합성
장으로 만들어야 할 미착수 영역이다.

## 9. 관측·피팅·반증 폐쇄성

v1.0.13 디렉터리의 top-level file은 14개지만 공개 실험 dataset,
fit result, optimizer state는 모두 0개다. NPZ 하나는 실험이 아니라
기존 graphite model-output golden snapshot이다.

또한 다음이 없다.

- raw voltage–capacity–time–temperature provenance
- smoothing/differentiation/filtering observation model
- voltage resolution, sampling, noise, baseline
- capacity normalization과 electrode loading uncertainty
- train/validation/holdout split
- parameter prior·bound·correlation
- profile likelihood, posterior 또는 confidence interval
- model ablation과 alternative mechanism comparison

따라서 “곡선을 그릴 수 있다”는 수치 표현력은 있으나
“공개 데이터가 이 물리 원인을 지지한다”는 반증 가능한 증거는
없다.

## 10. review 논문 깊이 판정

Chapter 1과 2를 합친 bibliography key는 33개다. 일부 주제는 깊게
들어가지만 이는 systematic review가 아니다.

- 검색 protocol과 포함·제외 기준이 없다.
- material/temperature/rate/dopant별 evidence table이 없다.
- 서로 충돌하는 문헌 결과와 실험 조건 차이를 종합하지 않는다.
- Si, composite, 고전압 doped LCO, 관측·식별성 문헌이 비어 있다.
- 인용 anchor와 실제 fitting dataset이 연결되지 않는다.

그러므로 “선택한 세부 주제의 깊은 tutorial seed”로는 보존하지만
“review 논문 수준 완료” 판정은 보류한다. 후속 문헌 조사는 현재
문헌 목록을 검증하는 데서 끝내지 않고 범위를 새로 닫아야 한다.

## 11. 정본으로 가져갈 것

### 그대로 또는 범위 명시 후 보존

- 이상 grand-canonical → Nernst/logistic
- 전하 보존과 peak 면적·높이 관계
- 전극 반응 방향과 셀 운전 label 분리
- causal relaxation의 reduced-model 출발점
- equilibrium/heterogeneity/kinetics/observation 분리
- Sommerfeld endpoint와 단위 환산
- 문헌 anchor와 placeholder의 tier 구분

### 재유도·재작성

- nonideal free energy와 convexified phase equilibrium
- multi-transition host topology
- empirical width hierarchy
- local-state activation barrier
- persistent hysteresis state
- graphite stage-specific parameterization
- LCO material chemistry와 electronic gate
- observation/differentiation model

### 신규 작성

- silicon anode
- graphite–silicon composite
- doped high-voltage LCO degradation/stability
- public-data fitting, uncertainty, holdout, ablation
- 별도 theory–code conformance matrix와 executable gates

## 12. 정본 작성 원칙

새 이론 문건은 다음 구조를 따른다.

1. 물리량과 좌표를 정의한다.
2. 자유에너지 또는 보존법칙에서 식을 유도한다.
3. 적용 범위와 극한을 밝힌다.
4. 재료별 화학으로 파라미터와 상태를 제한한다.
5. 실험 observable로 가는 forward map을 둔다.
6. 어떤 데이터가 어떤 가정을 반증하는지 쓴다.

코드 식별자, API, default dict, 함수명은 이론 본문에서 제거한다.
구현 추적성은 별도 문서에서

\[
\text{theory equation}
\leftrightarrow
\text{code symbol}
\leftrightarrow
\text{test gate}
\]

로 관리한다. 이것이 “문건은 물리·화학만, 코드는 문건을 100%
반영”이라는 사용자 원칙을 가장 엄격하게 지키는 방식이다.

## 13. Phase 058 종합으로 넘길 판정

Step 32에서는 v1.0.10–v1.0.13 전체 자산을 최종 분류한다.
v1.0.13에 대해서는 다음을 carry-forward한다.

- 교육적 이상계 유도: `PRESERVE_WITH_CONSOLIDATION`
- nonideal phase closure: `CORRECT`
- \(n_j\) 미시 다중도: `REJECT`
- broadening four-layer 분리: `PRESERVE_CONCEPTUAL`
- 저온·유한전류 현상 설명: `THEORY_ONLY`
- local potential barrier: `CORRECT`
- graphite/LCO default: `UNVERIFIED`
- doped high-voltage LCO: `REJECT_AS_COVERED`
- Si/composite: `MISSING`
- public-data fit과 uncertainty: `MISSING`
- Chapter 1 theory-only 구조: `REJECT`

이 판정을 바탕으로 Step 32의 theory–code–test–artifact 4축 matrix를
닫는다.
