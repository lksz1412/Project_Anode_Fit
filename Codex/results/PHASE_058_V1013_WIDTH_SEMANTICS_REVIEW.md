# Phase 058 v1.0.13 interaction·degeneracy·multiplicity·width 분리

정본일: 2026-07-28  
대상: Phase 058 Step 31.2  
기계 matrix:
`Codex/results/PHASE_058_V1013_WIDTH_SEMANTICS.json`  
검산기:
`Codex/work/v1010_v1013_phase058/validate_phase058_v1013_width_semantics.py`

## 결론

v1.0.13의 \(n_j\)는 미시적으로 유도된 “다중도”가 아니다.
현재 식에서 허용할 수 있는 가장 정직한 의미는

\[
 \boxed{\lambda_j\equiv\frac{w_jF}{RT}}
\]

라는 무차원 경험적 logistic 폭 비다.

최종 판정:

`CURRENT_n_IS_AN_EMPIRICAL_WIDTH_RATIO_NOT_A_DERIVED_MULTIPLICITY;_EQUILIBRIUM_HETEROGENEITY_KINETICS_AND_OBSERVATION_MUST_BE_SEPARATE`

v1.0.13의 broadening 절은 유한율속 꼬리와 앙상블 분포를
개념적으로 분리하고, 측정 peak에서 분포를 무제약 역산하지
않겠다고 한 점이 좋다. 그러나 여러 물리 원인을 다시 \(n_j\) 또는
\(w_j\) 하나에 압축하면서 그 값에 \(RT/F\) 온도 서식을 붙였기
때문에 이론적 정체와 식별 가능성이 사라진다.

## 1. 서로 다른 “개수”를 한 기호로 부르면 안 되는 이유

### 1.1 반응 전자수 \(n_e\)

반응을 한 번 진행할 때 \(n_e\) mol의 전자가 이동하도록 반응식을
정의하면

\[
 \Delta G=-n_eFU
\]

이고 이상 Nernst logit은

\[
 U-U_0=\frac{RT}{n_eF}\ln\frac{\xi}{1-\xi}.
\]

따라서 이상 폭은

\[
 \boxed{w_{n_e}=\frac{RT}{n_eF}}.
\]

전자수가 커지면 폭은 좁아진다. 반면 v1.0.13 식
\(w=n_jRT/F\)에서는 \(n_j\)가 커질수록 폭이 넓어진다.

298.15 K에서

| 해석 | 폭 |
|---|---:|
| 1-electron ideal | 25.6926 mV |
| 2-electron Nernst | 12.8463 mV |
| 현 식의 `n=2` | 51.3852 mV |

현 식의 `n=2`는 2-electron Nernst 폭의 4배다. 따라서 현
\(n_j\)는 반응 전자수가 아니다.

실제 Li 삽입은 보통 Li 1개당 전자 1개로 정규화한다. 여러 Li가
협동적으로 움직이는 반응식을 쓸 때도 전위·용량·반응 진행도의
몰 기준을 먼저 고정해야 하며, 이를 폭 파라미터에 조용히 넣으면
용량과 엔트로피 정규화가 함께 틀어진다. 정본에서는 \(n_e\)를
반응 양론 전용으로 예약해야 한다.

### 1.2 독립 자리 수 \(M_j\)

동등하고 독립인 자리가 \(M\)개이면

\[
 \Xi_M=(1+z)^M,\qquad
 \frac{\langle N\rangle}{M}=\frac{z}{1+z}.
\]

자리 수는 총 점유량과 절대 요동

\[
 \langle N\rangle=M\theta,\qquad
 \operatorname{var}(N)=M\theta(1-\theta)
\]

을 키우지만 정규화 점유율 \(\theta\)의 전위 폭은 바꾸지 않는다.

fugacity \(z=0.7\)에서 \(M=1,10,50\)의 binomial 분배함수를
직접 합한 결과, 세 경우 모두

\[
 \langle N\rangle/M=0.4117647058823529
\]

였다. 그러므로 자리 “개수”는 \(Q_j\)와 peak 면적·진폭에
연결할 양이지 \(w_j\)가 아니다.

### 1.3 상태 축퇴도 \(g_1/g_0\)

상수 축퇴도 비는

\[
 \frac{\theta}{1-\theta}
 =\frac{g_1}{g_0}
  \exp\!\left[\frac{\mu-\epsilon}{RT}\right]
\]

에서 중심 또는 표준 엔트로피만 옮긴다.

\[
 \Delta U_{1/2}
 =\frac{RT}{F}\ln\frac{g_1}{g_0}.
\]

이상 FWHM은 변하지 않는다. 조성에 따라 “축퇴도”가 바뀐다면
그것은 더 이상 상수 상태 계수가 아니라 ordering, interaction
또는 별도 내부상태 자유에너지다.

### 1.4 상호작용 \(\Omega_j\)

정규용액 상호작용은

\[
 F(U-U_0)
 =RT\ln\frac{\xi}{1-\xi}
 +\Omega(1-2\xi)
\]

처럼 등온선 전체를 비선형으로 바꾼다. 이를 상수 \(n_j\) 하나로
대체할 수 없다.

임계 이하에서 중심 기울기만 logistic에 맞추면

\[
 \lambda_{\rm center}
 =\frac{w_{\rm center}F}{RT}
 =1-\frac{\Omega}{2RT}.
\]

그러나 이는 중심의 국소 등가값일 뿐이고 조성 전 범위의 모양은
logistic이 아니다. 임계점에서 0이 되고 그 위 homogeneous
branch에서는 부호까지 바뀌므로 보편 폭으로 쓸 수 없다.

## 2. 현 \(n_j\)를 어떻게 읽어야 하는가

함수형만 놓고 보면

\[
 \xi=\operatorname{logistic}
 \left[\frac{F(U-U_0)}{\lambda_jRT}\right]
\]

이므로

\[
 h_j\equiv\frac1{\lambda_j}
\]

를 등가 Hill 기울기라고 부를 수 있다. 하지만 이는 fitted
logistic의 기울기를 다시 표현한 것이지, \(h_j\)개의 Li가 실제로
한 덩어리로 전환한다는 증거가 아니다.

v1.0.13 sample의 \(n=0.12\)는

\[
 \lambda=0.12,\qquad h_{\rm equivalent}=8.3333
\]

이고 298.15 K에서

\[
 w=3.0831\ {\rm mV},\qquad
 \mathrm{FWHM}=10.8695\ {\rm mV}
\]

다. 이 설정이 네 peak를 분리해 그릴 수 있다는 것은 수치 표현력의
증거다. microscopic cooperativity \(=8.33\), 특정 staging
상전이의 분자수 또는 전자수의 증거는 아니다. sample 자체도 이를
`phenomenological free fit width`라고 적은 점은 보존한다.

MSMR의 무차원 \(\omega_j\)와 현재 \(n_j\)의 대응도 함수형
재모수화로는 가능하다.

\[
 w_j=\omega_j\frac{RT}{F}.
\]

그러나 함수형 동형은 재료별 자유에너지, 반응종의 독립성 또는
폭의 미시 기원이 같다는 뜻이 아니다. 정본에서는 현재 `n`을
\(\lambda_j\) 또는 MSMR 문맥의 \(\omega_j\)로 바꾸고,
“다중도”라는 이름을 폐기하는 것이 안전하다.

## 3. configurational entropy와 경험적 폭의 혼동

이상 한 자리 격자기체에서

\[
 U(\xi,T)
 =U_0(T)+\frac{RT}{F}\ln\frac{\xi}{1-\xi}
\]

이므로 고정 \(\xi\)에서

\[
 \left.\frac{\partial U}{\partial T}\right|_\xi
 =\frac{\Delta S^0}{F}
 +\frac{R}{F}\ln\frac{\xi}{1-\xi}.
\]

둘째 항이 실제 이상 configurational 부분몰 엔트로피다.

반면 empirical form

\[
 w(T)=\lambda\frac{RT}{F}
\]

를 먼저 가정하고 미분하면

\[
 \frac{\partial U}{\partial T}
 =\frac{\Delta S^0}{F}
 +\frac{\lambda R}{F}\ln\frac{\xi}{1-\xi}.
\]

이 식은 가정한 \(w(T)\)의 대수적 미분으로는 맞다. 그러나
\(\lambda\ne1\)일 때 둘째 항을 이상 자리 configurational entropy와
동일시할 수는 없다.

\(\xi=0.8\)에서

| 항 | \(\partial U/\partial T\) |
|---|---:|
| 이상 한 자리 config | 0.119462 mV/K |
| \(\lambda=0.12\) 폭 서식의 대수항 | 0.014335 mV/K |

후자는 전자의 정확히 0.12배다. 이것을 config entropy라고 부르면
경험적 peak 폭이 반응 엔트로피를 임의로 재규격화한다.

v1.0.13 Chapter 2는 이 검증이 \(w=nRT/F\) 서식 아래의
자기일관성이고 실측 검증이 아니라고 정직하게 한정했다. 이 한정은
보존한다. 그러나 그 다음 단계에서는

- \(\lambda=1,\Omega=0\)의 실제 config entropy,
- 비이상 자유에너지에서 직접 미분한 entropy,
- empirical \(w(T)\)를 미분한 단순 대수항

을 서로 다른 것으로 표기해야 한다.

## 4. `n` 모드와 `w` 모드는 단순 별칭이 아니다

현재 매개변수 우선순위는 다음과 같다.

1. `n`이 있으면 \(w(T)=nRT/F\)
2. `n`이 없고 `w`가 있으면 \(n(T)=wF/(RT)\)로 역산해
   활성 폭을 \(w=\)상수로 유지
3. 둘 다 없으면 \(n=1\)

따라서 `n`과 `w`는 같은 값을 다른 방식으로 입력하는 단순 별칭이
아니다.

- `n` 모드: 폭이 \(T\)에 선형 비례
- `w` 모드: 폭이 \(T\)에 대해 동결

이는 서로 다른 물리 모형이다. default graphite 4개와 LCO 3개
전이는 모두 `n=1`과 `w`를 동시에 가지므로, 일곱 stored `w`가
모두 가려지고 실제 폭은 298.15 K에서 25.6912 mV다.

따라서 문건이나 fitting interface는 값과 온도 법칙을 분리해야 한다.
예를 들면 기준온도 폭 \(w_{j,\rm ref}\)와

\[
 w_j(T,I,x)
\]

의 물리 모델을 별도 필드로 두어야 한다. 입력 키의 존재 여부가
온도 물리를 암묵적으로 선택하게 해서는 안 된다.

## 5. 관측 폭을 만드는 네 층

사용자의 핵심 관측을 설명하려면 peak 생성 사슬을 다음처럼
분리해야 한다.

\[
 p_{\rm obs}
 =
 K_{\rm obs}
 *K_{\rm kin}
 *\rho_{\rm het}
 *p_{\rm eq}.
\]

여기서 \(p=d\xi/dU\)는 면적 1로 정규화한 전이 밀도다.

### 5.1 평형 \(p_{\rm eq}\)

- 이상 고용체: logistic derivative
- 비이상 단상: 선택한 자유에너지의 암시적 미분
- 두-상 거시평형: common-tangent plateau에 대응하는 날카로운
  전환과 binodal 끝단

평형층은 \(T\), 조성, 압력·응력, 재료 자유에너지로 정한다.
주사 방향이나 계측 평활을 넣지 않는다.

### 5.2 이질성 \(\rho_{\rm het}\)

입자·결정립·도메인별 조성, 결함, dopant, 응력, 표면 상태와
접촉 환경이 \(U_0,\Omega\), 용량 또는 장벽을 분포시킨다.
정규화 분포를 forward로 합성하면 면적을 보존하면서 peak를
넓힌다. 구조적 이질성은 \(I\to0\)에서도 남을 수 있다.

v1.0.13이 무제약 역산을 금하고 forward 평균만 허용한 것은
타당하다. 다만 “평형 중심은 입자 무관 상수이고 분포하는 것은
오직 \(\eta\)”라는 강한 가정은 재료와 제조 조건별 검증 대상이다.
dopant·표면·응력은 실제 평형 자유에너지와 중심도 바꿀 수 있다.

### 5.3 동역학 \(K_{\rm kin}\)

국소 선형 근사에서

\[
 L_U=|\dot U|\tau(T,U,x)
\]

인 one-sided relaxation kernel은 평균을 \(L_U\)만큼 이동시키고
분산에 \(L_U^2\)를 더하며 비대칭 꼬리를 만든다.

이 성분은

\[
 |\dot U|\to0\quad\text{또는}\quad I\to0
 \quad\Longrightarrow\quad L_U\to0
\]

이어야 한다. 실제로는 Butler–Volmer/MHC 반응, 고체확산,
핵생성·계면 이동의 여러 시간척도와 내부 상태가 있으므로 고정
합성곱보다 state evolution이 일반형이다.

### 5.4 관측 \(K_{\rm obs}\)

전압 분해능, sampling, 필터, spline, differentiation과 smoothing이
별도 폭을 만든다. 원시 데이터와 preprocessing metadata가 없으면
재료 폭과 분리할 수 없다.

모든 kernel이 비음수·면적 1이고 적분창이 충분하면 peak 면적은
보존된다. 또한 정규화 kernel \(K\)에 대해

\[
 \|p*K\|_\infty\le\|p\|_\infty
\]

이므로 broadening은 peak 높이를 올리지 않는다. 이것이 고정
전이 용량에서 낮아진 peak와 넓어진 peak를 함께 설명하는
가장 직접적인 보존 법칙이다.

## 6. 폭의 분산 장부

독립 stationary kernel의 단순화된 경우 평균과 분산은 더해진다.
이상 logistic의 분산은

\[
 \sigma_{\rm eq}^2=\frac{\pi^2w_{\rm eq}^2}{3}.
\]

Gaussian 이질성 \(\sigma_U\), exponential lag \(L_U\),
관측 분산 \(\sigma_{\rm obs}^2\)를 쓰면

\[
 \boxed{
 \sigma_{\rm obs,peak}^2
 =\frac{\pi^2w_{\rm eq}^2}{3}
 +\sigma_U^2+L_U^2+\sigma_{\rm obs}^2}.
\]

이는 각 원인을 구분하기 위한 moment 장부이지, 합성 결과가 다시
정확한 logistic이라는 뜻은 아니다. 특히 one-sided lag는
비대칭이므로 단일 FWHM이나 \(w\)가 정보를 잃는다.

예시로 298.15 K 이상 폭, \(\sigma_U=10\) mV,
\(L_U=20\) mV, \(\sigma_{\rm obs}=5\) mV를 넣으면
총 표준편차는 51.929 mV다. 이를 분산만 같은 logistic으로
환산한 기술적 폭은 28.630 mV다. 이 28.630 mV를 다시
“평형 \(nRT/F\)”로 읽으면 네 출처를 하나로 오인한다.

## 7. 사용자의 저온·유한전류 관측과의 연결

평형 이상 폭 \(RT/F\)만 보면 온도가 내려갈 때 peak는 좁아지고
높아져야 한다. 298.15→273.15 K에서 폭 비는

\[
 273.15/298.15=0.91615
\]

다.

반면 활성화형 시간척도

\[
 \tau\propto\exp(E_a/RT)
\]

는 저온에서 커진다. \(E_a=40\) kJ/mol인 단순 예시에서는 같은
온도 변화로 \(\tau\)가 4.379배가 된다. 이는 재료값의 확정이
아니라 경쟁하는 스케일의 수치 예시다.

따라서 유한 전류에서

\[
 L_U=|\dot U|\tau
\]

가 지배하면 저온일수록 관측 peak가 더 넓고 낮아질 수 있다.
전류가 없을 때보다 정전류에서 peak가 낮아지고 넓어진다는 사용자의
관측도 같은 방향이다.

핵심은 저온 broadening을 평형 \(w\propto T\)의 부호를 뒤집어
설명하는 것이 아니다. 평형층은 저온에서 좁아지고, 동역학 장벽과
이질적 relaxation이 그보다 더 크게 넓히는 경쟁으로 설명해야 한다.
이 분리가 되어야

- \(I\to0\) 환원,
- 온도별 rate series,
- rest/GITT 뒤 회복,
- peak 면적 보존,
- peak 비대칭

을 동시에 검증할 수 있다.

## 8. 권장 기호 계약

| 기호 | 전용 의미 |
|---|---|
| \(n_e\) | 반응 전자 양론 |
| \(M_j\) | 자리/종 개수, \(Q_j\)에 연결 |
| \(g_0,g_1\) | 상태 축퇴도 |
| \(\Omega_j\) | 자유에너지 상호작용 |
| \(\lambda_j\) | 경험적 logistic 폭 비 \(wF/(RT)\) |
| \(w_{\rm eq,j}\) | 선택한 평형 자유에너지에서 유도한 폭/국소 척도 |
| \(\rho_{\rm het,j}\) | 정규화 forward 이질성 분포 |
| \(\tau_j\) | 온도·전위·상태 의존 동역학 시간척도 |
| \(K_{\rm obs}\) | 관측·전처리 kernel |
| \(w_{\rm reported,j}\) | 최종 peak의 기술 통계, 물리 원인이 아님 |

전달계수 \(\alpha\) 또는 \(\chi\)는 정·역 장벽의 비대칭을 정하지만
detailed balance의 평형비에서는 소거되어야 한다. 이를 평형 폭에
넣지 않는다.

## 9. v1.0.13 처분

보존:

- \(n=0.12\)를 현상학적 자유 fit이라고 한 sample의 한정
- 유한율속 \(L_V\)와 정적 폭의 이중계산 금지
- apparent-\(U\) 분포의 forward-only 평균
- \(I\to0\)에서 kinetic broadening이 사라져야 한다는 경계
- 두-상 실측 폭을 평형 \(\Omega\) 하나로 정하지 않는다는 문제의식
- Chapter 2의 “현재 온도 서식 아래 자기일관성일 뿐 실측 검증이
  아니다”라는 한정

교정:

- \(n_j\) “폭 다중도” → \(\lambda_j\) “경험적 폭 비”
- 모든 \(\Omega\le2RT\)에 \(nRT/F\) logistic을 적용하는 문장
- \(\lambda R\logit/F\)를 일반 configurational entropy로 부르는 문장
- `n`과 `w`를 별칭처럼 설명하는 interface
- 모든 입자의 평형 중심이 반드시 같고 오직 과전압만 분포한다는
  재료 비의존 가정

폐기:

- \(n_j\)를 전자수, 자리수, 축퇴도 또는 microscopic cooperativity로
  사후 동일시하는 해석
- equilibrium, heterogeneity, kinetics와 observation을 한
  \(w_j\)에서 동시에 물리적으로 식별했다는 주장
- 저온 실측 broadening을 평형 \(RT/F\)만으로 설명하는 주장

## Gate

source hash, 기호 분리, 전자수/자리수/entropy/variance 검산과
default precedence를 포함한 47개 check가 모두 통과했다.

`PASS_P058_V1013_WIDTH_SEMANTICS`

다음 Step 31.3에서는 v1.0.13의 실제 신규 식·문단·default와
production/test 변화를 v1.0.12에 exact patch로 연결한다.
