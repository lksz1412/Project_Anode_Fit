# Phase 058 v1.0.13 통계역학 독립 재유도

정본일: 2026-07-28  
대상: Phase 058 Step 31.1  
기계 검산:
`Codex/results/PHASE_058_V1013_STATMECH_VALIDATION.json`  
검산기:
`Codex/work/v1010_v1013_phase058/validate_phase058_v1013_statmech.py`

## 판정 경계

이 문건은 v1.0.13의 이론 사슬을 표준 통계역학에서 독립적으로
재유도한 감사 결과다. 향후 정본 이론 원고도 아니고, 실험 자료에
의한 외적 타당성 검증도 아니다.

판정은 다음 질문에 한정한다.

1. 한 자리 분배함수에서 점유율과 화학퍼텐셜이 같은 부호로 나오는가
2. Li/Li\(^+\) 기준 전위와 연결했을 때 Nernst/logistic이 일관적인가
3. dQ/dV 종의 높이·폭·면적이 보존식과 맞는가
4. 여러 전이의 합에 어떤 독립성·상태 위상 가정이 필요한가
5. 정규용액을 이상 logistic으로 대체할 수 있는 범위는 어디까지인가
6. 평형 점유에 주사 방향을 넣을 수 있는가

최종 판정은 다음과 같다.

`V1013_REPAIRS_THE_IDEAL_STATMECH_CHAIN_BUT_DOES_NOT_CLOSE_NONIDEAL_WIDTH_MULTI_TRANSITION_TOPOLOGY_OR_EQUILIBRIUM_DIRECTION`

즉 v1.0.13은 이상 격자기체의 기본 사슬을 이전 판본보다 훨씬
정확하게 세웠다. 그러나 비이상 상호작용, 폭 다중도, 다중 전이의
상태 위상과 평형/경로 분리는 아직 닫히지 않았다.

## 1. 한 자리 대정준 분배함수

빈 자리와 Li 점유 자리의 미시상태를 각각 \(n=0,1\)로 둔다.
빈 상태와 점유 상태의 내부 축퇴도를 \(g_0,g_1\), 점유 상태의
표준 에너지를 \(\epsilon\), Li 저장조 화학퍼텐셜을 \(\mu\)라 하면
한 자리 대정준 합은

\[
 \Xi_1
 =g_0+g_1\exp\!\left[-\frac{\epsilon-\mu}{k_BT}\right].
\]

따라서 Li 점유율은

\[
 \theta
 =\langle n\rangle
 =\frac{g_1\exp[-(\epsilon-\mu)/(k_BT)]}{\Xi_1},
\]

이고 odds를 취하면

\[
 \frac{\theta}{1-\theta}
 =\frac{g_1}{g_0}
  \exp\!\left[\frac{\mu-\epsilon}{k_BT}\right].
\]

몰 단위로 바꾸면

\[
 \boxed{
 \mu
 =\epsilon
 +RT\ln\!\left[
   \frac{g_0}{g_1}\frac{\theta}{1-\theta}
 \right]}.
\]

v1.0.13의 \(g_0=g_1=1\) 특수형

\[
 \mu=\mu^0+RT\ln\frac{\theta}{1-\theta}
\]

은 맞다. 다만 기호는 canonical \(Z\)보다 grand partition
\(\Xi\)가 더 명료하다. v1.0.13도 그 앙상블 차이를 주석으로
인식하고 있으므로 이는 물리 오류가 아니라 표기 개선 사항이다.

### 축퇴도의 역할

축퇴도 비 \(g_1/g_0\)는 logit에 상수만 더한다. 따라서 표준
엔트로피 또는 중심 전위를 이동시키지만 이상 곡선의 열적 폭은
바꾸지 않는다.

\[
 U_{1/2}
 =U_0+\frac{RT}{F}\ln\frac{g_1}{g_0}.
\]

298.15 K에서 \(g_1/g_0=3\)이면 중심은 28.226 mV 이동하지만
FWHM은 비축퇴 경우와 같은 90.579 mV다. 그러므로 축퇴도나
표준상태 엔트로피를 폭 다중도 \(n_j\)의 미시적 유도로 사용할
수 없다.

## 2. 전극 전위와 점유율의 부호

삽입 반응을

\[
 \mathrm{Li^+}+e^-+\Box
 \rightleftharpoons \mathrm{Li}_{\rm host}
\]

로 쓰고 Li 금속 기준전극과 평형을 잡으면

\[
 \mu_{\rm Li}^{\rm host}
 -\mu_{\rm Li}^{\rm ref}
 =-FU.
\]

표준 host 상태 \(\epsilon\)에 대해

\[
 U_0=\frac{\mu_{\rm Li}^{\rm ref}-\epsilon}{F}
\]

로 정의하면

\[
 \mu-\epsilon=-F(U-U_0).
\]

비축퇴 이상 자리에서

\[
 \frac{\theta}{1-\theta}
 =\exp\!\left[-\frac{F(U-U_0)}{RT}\right].
\]

탈리튬화 진행률을 \(\xi=1-\theta\)로 정의하면

\[
 \boxed{
 \xi(U,T)
 =\frac{1}{1+\exp[-F(U-U_0)/(RT)]}}
\]

이고 이를 뒤집으면

\[
 \boxed{
 U(\xi,T)
 =U_0(T)+\frac{RT}{F}\ln\frac{\xi}{1-\xi}}.
\]

따라서 Li/Li\(^+\) 하프셀에서 전위를 올리면
\(\theta\)는 감소하고 \(\xi\)는 증가한다. 이 부호는
v1.0.13 Part 0와 Chapter 2가 사용한 부호와 일치한다.

여기서 \(U\)는 전극의 평형 상태변수다. 충전/방전 또는 전위
주사의 방향은 같은 \(U,T\)에서 평형 점유를 바꾸지 않는다.
방향에 따라 값이 달라지려면 핵생성 장벽, 과전압, 유한 속도,
내부 상태 기억처럼 경로 의존 변수가 추가되어야 한다.

## 3. 이상 logistic dQ/dV 불변량

\[
 w_0=\frac{RT}{F}
\]

라 두면

\[
 \frac{d\xi}{dU}
 =\frac{\xi(1-\xi)}{w_0}.
\]

이 종의 세 불변량은

\[
 \int_{-\infty}^{\infty}\frac{d\xi}{dU}\,dU=1,
\qquad
 \left.\frac{d\xi}{dU}\right|_{U_0}=\frac{1}{4w_0},
\]

\[
 \mathrm{FWHM}
 =4\,\operatorname{arcosh}(\sqrt2)\,w_0
 \simeq3.525494\,w_0.
\]

298.15 K의 표준 상수를 쓰면

| 양 | 독립 계산 |
|---|---:|
| \(w_0=RT/F\) | 25.692579 mV |
| FWHM | 90.579042 mV |
| peak height | 9.730436 V\(^{-1}\) |
| 무차원 면적 | 1 |

기계 검산에서 분배함수로 계산한 \(\xi\)와 직접 logistic의 최대
차이는 \(1.67\times10^{-16}\), \(\pm30w_0\) 수치 적분 면적은
0.9999999999998128이었다.

전이 \(j\)의 용량이 \(Q_j\)라면

\[
 Q_j\frac{d\xi_j}{dU}
\]

의 배경 차감 면적은 \(Q_j\), 중심 높이는 \(Q_j/(4w_j)\)다.
v1.0.13의 이상 peak 미분, 높이와 면적 설명은 보존한다.

## 4. 여러 전이의 합은 언제 성립하는가

### 4.1 독립 자리군인 경우

서로 겹치지 않는 자리군 또는 독립 반응군 \(j\)가 각각
\(M_j\)개 존재한다면 전역 대정준 합은

\[
 \Xi_{\rm total}
 =\prod_j\Xi_j^{M_j}
\]

로 인수분해된다. 이때 \(Q_j\)를 해당 자리군의 완전 전환
용량으로 정의하면

\[
 Q_{\rm rxn}(U)=\sum_jQ_j\xi_j(U)
\]

이고

\[
 \boxed{
 \frac{dQ_{\rm rxn}}{dU}
 =\sum_jQ_j\frac{d\xi_j}{dU}}.
\]

세 독립 전이에 \(Q_j=(0.20,0.35,0.45)\)를 준 검산에서 합성 peak
면적은 1.0으로 총 용량과 일치했다.

### 4.2 연속 staging 상태인 경우

각 logistic이 같은 Li 자리의 연속 상태를 다시 세는 것이라면
독립 Bernoulli 변수의 곱은 자동으로 성립하지 않는다. 이 경우
미시상태 \(\alpha\)를 명시한

\[
 \Xi=\sum_\alpha g_\alpha
 \exp[-\beta(E_\alpha-\mu N_\alpha)]
\]

에서 상호배타 상태 확률을 함께 구하거나, 독립적인 반응 진행도
\(\xi_j\)와 그 구속조건을 정의해야 한다.

그러므로 v1.0.13의 용량 합은 전하 보존식으로는 타당하지만,
“한 자리 분배함수에서 아무 추가 가정 없이 나온 다중 전이”
라고 읽으면 과장이다. 다음 정본은 각 \(Q_j\)가

- 서로 다른 독립 자리군의 용량인지,
- 상호배타 staging 상태 사이 경계의 반응 용량인지,
- 경험적으로 분해한 관측 peak 면적인지

를 구분해야 한다. 그렇지 않으면 겹치는 logistic이 같은 Li를
중복 계수할 수 있다.

배경 \(C_{\rm bg}\)도 위 분배함수에서 유도되지 않는다. 별도
고용체 저장, 이중층 또는 관측 baseline 중 무엇인지 물리 역할을
정한 뒤 더해야 한다.

## 5. 정규용액은 임계 이하에서도 이상 logistic이 아니다

대칭 정규용액의 몰 자유에너지를

\[
 g(\theta)
 =g^0+\epsilon\theta
 +RT[\theta\ln\theta+(1-\theta)\ln(1-\theta)]
 +\Omega\theta(1-\theta)
\]

로 두면

\[
 \mu(\theta)
 =\epsilon
 +RT\ln\frac{\theta}{1-\theta}
 +\Omega(1-2\theta).
\]

\(\xi=1-\theta\)와 Li 기준 전위를 사용하면

\[
 \boxed{
 F(U-U_0)
 =RT\ln\frac{\xi}{1-\xi}
 +\Omega(1-2\xi)}.
\]

이 식은 \(\Omega=0\)일 때만 닫힌 이상 logistic으로 환원된다.
\(\Omega<2RT\)는 균질 자유에너지가 볼록하다는 뜻이지,
\(\Omega\) 항이 사라진다는 뜻이 아니다.

예를 들어 \(\Omega=RT\), \(\xi=0.8\)이면 정규용액 전위는
이상 Nernst 전위보다 15.416 mV 낮다. 중심 기울기는

\[
 \left.\frac{dU}{d\xi}\right|_{1/2}
 =\frac{4RT-2\Omega}{F}.
\]

이를 중심 기울기만 같은 logistic 폭으로 억지 환산하면

\[
 w_{\rm center}
 =\frac{RT-\Omega/2}{F}.
\]

\(\Omega=RT\)에서는 12.846 mV로 \(RT/F\)의 절반이다. 곡선 전체는
이 폭의 logistic과도 같지 않다.

따라서 v1.0.13 안에는 다음 두 문장이 공존한다.

- 올바른 문장: \(\Omega\ne0\)이면 닫힌 logistic이 아니다.
- 잘못 확장된 문장: 단상 \(\Omega\le2RT\)이면
  \(w=n_jRT/F\)가 분배함수의 평형 예측이다.

정확한 경계는 “비축퇴 이상 독립자리 \(\Omega=0\),
\(n_j=1\)”이다. \(n_j\), 비이상성, 분포 폭과 반응 전자수의
분리는 Step 31.2에서 이어서 판정한다.

## 6. 임계점, 공통 접선과 히스테리시스

정규용액 곡률은

\[
 g''(\theta)
 =\frac{RT}{\theta(1-\theta)}-2\Omega.
\]

따라서 대칭 모형의 임계 조건은

\[
 \boxed{\Omega_c=2RT}
\]

이고 이 부분은 v1.0.13이 맞다.

그러나 \(\Omega>2RT\)에서 나오는 비볼록 homogeneous loop를
그대로 최종 평형 전위로 사용할 수는 없다. 거시 평형은 자유에너지의
볼록 껍질, 즉 공통 접선으로 정해지고 공존 구간은 plateau가 된다.
대칭 정규용액의 binodal 끝점은

\[
 \ln\frac{\theta_a}{1-\theta_a}
 +\frac{\Omega}{RT}(1-2\theta_a)=0,
\qquad
\theta_b=1-\theta_a.
\]

\(\Omega=3RT\)에서

\[
 \theta_a=0.0707202,\qquad
 \theta_b=0.9292798.
\]

같은 조건의 spinodal은
\(\theta_s=0.211325/0.788675\)다. binodal은 평형 공존 조성이고,
spinodal은 homogeneous 상태의 국소 안정성 한계이므로 같은 양이
아니다.

spinodal 사이 loop만으로 실측 히스테리시스 폭을 확정할 수도 없다.
관측 charge/discharge 분리는 핵생성, 계면 이동, 탄성, 결함,
입자 분포와 유한시간 경로가 정해야 한다. 정규용액 자유에너지는
그 동역학의 구동력과 안정성 경계를 제공하지만 기억 법칙 자체는
아니다.

## 7. 중심 전위의 온도 의존

삽입 반응 표준 자유에너지를

\[
 \Delta G^0(T)
 =\Delta H^0(T)-T\Delta S^0(T)
 =-FU_0(T)
\]

로 두면, \(\Delta H^0,\Delta S^0\)를 좁은 온도 범위에서 상수로
근사할 때

\[
 U_0(T)
 =\frac{-\Delta H^0+T\Delta S^0}{F},
\qquad
 \frac{dU_0}{dT}=\frac{\Delta S^0}{F}.
\]

이 중심 이동과 이상 혼합 logit의 명시적 \(T\) 의존은 서로 다른
항이다. 넓은 온도 범위에서는 열용량 차이
\(\Delta C_p\), 상전이와 기준전극의 온도 의존을 포함해
\(\Delta H^0(T),\Delta S^0(T)\)를 적분해야 한다.

v1.0.13의 중심 \(H-TS\) 사슬은 좁은 범위 상수 근사로 보존하되,
재료별 실험 검증 전에는 보편 상수로 승격하지 않는다.

## 8. v1.0.13 claim별 처분

| ID | 판정 | 요지 |
|---|---|---|
| SM13-01 | PRESERVE | 단일자리 대정준 합에서 이상 점유 logistic 유도 |
| SM13-02 | PRESERVE_WITH_EXPLICIT_REFERENCE_REACTION | \(\theta,\xi,U\) 부호는 일관적 |
| SM13-03 | PRESERVE | 이상 종의 면적·높이·FWHM |
| SM13-04 | REJECT | 축퇴도는 중심을 옮기며 폭은 바꾸지 않음 |
| SM13-05 | REJECT | \(RT/F\) exact는 \(\Omega=0\)에 한정 |
| SM13-06 | REJECT, source도 경고 | \(\Omega\ne0\)은 암시적 등온선 |
| SM13-07 | PRESERVE | 대칭 정규용액 임계 \(\Omega=2RT\) |
| SM13-08 | REJECT | 비볼록 loop를 평형·실측 히스로 동일시 불가 |
| SM13-09 | PRESERVE_WITH_CONTRACT | 용량 합은 독립 extent와 \(Q_j\) 정의가 필요 |
| SM13-10 | REJECT | 다중 합은 한 자리 \(\Xi_1\)의 자동 결과가 아님 |
| SM13-11 | REJECT | 평형 점유에 주사 방향을 넣을 수 없음 |
| SM13-12 | REJECT | \(C_{\rm bg}\)는 표시된 분배함수 밖의 항 |
| SM13-13 | REJECT/HANDOFF | \(n_j\)는 단일자리 유도에서 나오지 않음 |

## 9. 정본으로 가져갈 최소 사슬

향후 이론 원고의 해당 절은 코드 언급 없이 다음 순서로만 닫는 것이
안전하다.

1. 상태와 축퇴도를 포함한 \(\Xi_1\)
2. \(\theta\), \(\mu(\theta)\), \(\xi=1-\theta\)
3. Li/Li\(^+\) 기준 반응과 \(U=(\mu_{\rm ref}-\mu_{\rm host})/F\)
4. 이상 \(\Omega=0\)의 Nernst/logistic
5. 이상 peak의 면적·높이·FWHM
6. 독립 자리군 product partition 또는 명시적 반응 extent
7. 정규용액 암시적 등온선
8. convexification, binodal, spinodal의 구분
9. 핵생성·계면 이동을 포함한 별도 비평형 상태방정식
10. 마지막에만 관측 dQ/dV로 사상

평형 free energy, path-dependent kinetics, electrode
heterogeneity와 observation kernel을 이 순서에서 섞지 않아야
사용자의 핵심 현상인 저온·유한전류 peak 저하와 broadening을
평형 \(RT/F\) 하나에 잘못 귀속하지 않게 된다.

## Gate

기계 검산 35개가 모두 통과했다.

`PASS_P058_V1013_STATMECH_REDERIVATION`

다음 Step 31.2는 interaction, degeneracy, multiplicity,
전자수와 현상학적 \(n_j/w_j\)를 서로 다른 물리량으로 분리한다.
