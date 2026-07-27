# Phase 058 v1.0.10 평형·broadening·hysteresis·kinetics 독립 재유도

정본일: 2026-07-28
대상: Phase 058 Step 29.2
기계 검산:
`Codex/results/PHASE_058_V1010_KINETICS_VALIDATION.json`

## 1. 평형 상태는 protocol 방향에 의존하지 않는다

한 전이의 평형 진행률은 같은 \(V,T\), 조성과 물질 상태에서 유일해야
한다. 이상 two-state site라면 탈리튬화 진행률을

\[
 \xi_{\rm eq}(V,T)
 =\frac{1}{1+\exp[-F(V-U)/RT]}
\]

처럼 둘 수 있다. reverse sweep에서도 평형 목표는 같은 함수다.
바뀌는 것은 시간 진행방향과 실제 상태 \(\xi(t)\)가 목표에 접근하는
경로이지, \(\xi_{\rm eq}\) 자체가 아니다.

v1.0.10은

\[
 \xi_{\rm eq}
 =\{1+\exp[-\sigma_d(V-U^d)/w]\}^{-1}
\]

로 protocol sign을 평형 함수 안에 넣는다. 같은 \(V-U=w\)에서
\(\sigma_d=+1\)과 \(-1\)의 값은 각각 0.7311과 0.2689이며 합은
1이다. 즉 한 branch의 평형 상태가 다른 branch에서 여집합으로
바뀐다.

\(\xi(1-\xi)/w\) kernel은 두 값에서 같기 때문에 dQ/dV bell만 보면
오류가 숨는다. 그러나 state variable, entropy, lag와 composition
mapping에는 숨지 않는다. 평형 함수에서는 protocol sign을 제거하고,
reaction direction과 time ordering을 evolution/observation layer에서
처리해야 한다.

## 2. ideal logistic와 regular solution을 한 평형식으로 섞을 수 없다

이상 격자기체 자유에너지는

\[
 g_{\rm id}(\xi)
 =RT[\xi\ln\xi+(1-\xi)\ln(1-\xi)]
\]

이고, 전기화학 구동력과 평형시키면 logistic가 나온다. 이때
\(w=RT/F\)와 logistic derivative는 서로 일관적이다.

상호작용을 넣은 regular solution은

\[
 g(\xi)
 =g_{\rm id}(\xi)+\Omega\xi(1-\xi)
\]

이며

\[
 F(V-U)
 =RT\ln\frac{\xi}{1-\xi}+\Omega(1-2\xi).
\]

따라서 \(\Omega\ne0\)이면 \(\xi(V)\)는 더 이상 explicit ideal
logistic가 아니다. implicit derivative는

\[
 \frac{d\xi}{dV}
 =\frac{F}{
      RT/[\xi(1-\xi)]-2\Omega
   }
\]

이고, \(\Omega>2RT\)에서는 중간 조성의 denominator가 음수가 되어
homogeneous branch가 불안정해진다.

v1.0.10은 \(\Omega\)로 spinodal/hysteresis를 계산하면서 평형 peak는
여전히 ideal logistic로 계산한다. 이는 하나의 free energy에서 나온
두 식이 아니다. 다음처럼 분리해야 한다.

- \(\Omega=0\) ideal/single-site limit: logistic를 이론식으로 사용
- \(0<\Omega\le2RT\) homogeneous regular solution: implicit isotherm 사용
- \(\Omega>2RT\) phase-separating system: common-tangent/binodal,
  phase fraction과 nucleation/transport를 사용
- 위 구조를 쓰지 않는 유효 bell: empirical observation kernel로 명명

## 3. finite-rate 1차 relaxation은 살릴 수 있는 reduced model이다

평형 목표를 따라가는 가장 단순한 relaxation은

\[
 \frac{d\xi}{dt}=k(\xi_{\rm eq}-\xi)
\]

이다. constant current에서

\[
 \dot q=\frac{|I|}{Q_{\rm scale}},\qquad
 L_q=\frac{|I|}{Q_{\rm scale}k}
\]

를 정의하면

\[
 \frac{d\xi}{dq}
 =\frac{\xi_{\rm eq}-\xi}{L_q}.
\]

국소적으로 \(V(q)\)가 선형이고 \(L_V=|dV/dq|L_q\)라면

\[
 \frac{d\xi}{dV}
 =\frac{\xi_{\rm eq}-\xi}{L_V}.
\]

이 식은 causal exponential memory와 같다. 독립 연속계 검산에서
\(L_V/w\)를 0, 0.25, 0.5, 1, 2로 키우면 다음이 나타났다.

| \(L_V/w\) | 상대 peak 높이 | 상대 FWHM | peak shift |
|---:|---:|---:|---:|
| 0 | 1.000 | 1.000 | 0 |
| 0.25 | 0.985 | 1.017 | \(+0.00620\) V |
| 0.5 | 0.951 | 1.058 | \(+0.01154\) V |
| 1 | 0.865 | 1.164 | \(+0.01982\) V |
| 2 | 0.710 | 1.389 | \(+0.03092\) V |

충분한 전위창에서 면적은 모두 1에 \(2\times10^{-4}\) 이내로
보존됐다. 따라서 “유한율속에서 peak가 낮아지고 넓어지며 진행방향으로
치우친다”는 사용자의 출발 관측을 설명할 수 있는 최소 골격은 맞다.

다만 이것은 single relaxation-time reduced model이다. 실제
phase-boundary motion, nucleation, solid diffusion, charge transfer와
porous-electrode transport 중 무엇이 \(k\)를 정하는지는 별도
constitutive closure가 필요하다.

## 4. continuum 저율극한과 legacy grid switch

연속 방정식에서 \(L_V\to0^+\)이면 singular perturbation expansion으로

\[
 \xi
 =\xi_{\rm eq}-L_V\frac{d\xi_{\rm eq}}{dV}+O(L_V^2)
\]

이므로

\[
 \frac{\xi_{\rm eq}-\xi}{L_V}
 \to\frac{d\xi_{\rm eq}}{dV}.
\]

즉 물리적 continuum은 저율에서 평형 derivative로 매끄럽게
돌아간다. v1.0.10 문건이 “작은 \(L_V\)에서는 0/0이라 연속 극한이
아니다”라고 쓴 것은 물리식의 성질이 아니라 현재 sampled recurrence의
분해능 문제다.

legacy code는 \(L_V<2\Delta V_{\rm grid}\)이면 kinetic 식을 버리고
평형 kernel로 전환한다. 대표 \(w=0.02\) V,
\(\Delta V_{\rm grid}=0.0002\) V에서 threshold 바로 위 kinetic
peak는 평형 peak의 0.7707이었다. threshold 아래에서는 갑자기
1.0이 되므로 mode switch가 약 22.9% jump를 만든다.

따라서 grid threshold는 physics가 아니며 결과가 grid resolution에
의존한다. 후속 구현은 analytic convolution, stable ODE solver 또는
grid-converged discretization으로 \(L_V\to0\)을 연속 복원해야 한다.

## 5. 저장 default는 broadening mechanism을 실제로 켜지 않는다

저온 258.15 K, numeric \(I=1\), \(Q_{\rm cell}=1\)이라는 legacy
시연 조건에서도 네 default 전이의 \(L_V\)는

\[
 9.46\times10^{-6},\
 2.34\times10^{-6},\
 5.78\times10^{-7},\
 4.45\times10^{-8}\ {\rm V}
\]

였다. 대표 switch threshold는 \(4.06\times10^{-4}\) V이고 최대
비는 0.0233뿐이다. 네 전이 모두 평형 branch로 강제된다.

이 때문에 앞서 실행한 default graphite curve가 0–1 A에서 동일했다.
이론이 qualitative mechanism을 적었다는 것과 shipped default가
그 mechanism으로 관측 현상을 계산했다는 것은 다른 주장이다.

분자 Eyring prefactor \(k_BT/h\)를 electrode-scale phase-fraction
relaxation에 바로 넣으면 relaxation이 지나치게 빠른 것도 원인이다.
microscopic hop rate를 macroscopic \(k\)로 올리려면 site density,
reaction area, particle geometry, nucleation population과 transport
coarse-graining이 필요하다.

## 6. direct L_V는 I→0을 위반한다

v1.0.10은 transition에 `L_V`가 있으면 전류와 barrier 계산을 모두
우회한다. 독립 probe에서 \(L_V=0.04\) V를 직접 지정하고 \(I=0\)으로
계산했을 때도

- peak height는 평형의 0.772
- FWHM은 평형의 1.288
- peak는 \(+0.02656\) V 이동

한 nonequilibrium curve가 남았다. 따라서 direct \(L_V\)를 material
parameter로 읽을 수 없다.

fit convenience로 남길 경우에도

\[
 L_V(I,T,\ldots)\to0\quad\text{as}\quad I\to0
\]

을 강제하는 protocol-level nuisance parameter로 격리해야 한다.

## 7. local affinity가 frozen cut constant로 바뀌었다

thermodynamically consistent rate는 최소한

\[
 \frac{r_+}{r_-}=\exp\!\left(\frac{\mathcal A}{RT}\right)
\]

를 만족하고, affinity는 local electrochemical state에서

\[
 \mathcal A
 =-\Delta_r G(x,T,\phi,\sigma,\ldots)
\]

로 평가돼야 한다. applied current는 근본 barrier에 직접 꽂는
독립 knob라기보다 overpotential, concentration와 phase state를
바꾸어 \(\mathcal A\)와 transition-state free energy에 간접적으로
들어간다.

v1.0.10은

\[
 \mathcal A
 =\min(z_{\rm cut}nRT,A_{\rm cap}RT)
\]

를 전이당 한 번 계산해 고정한다. default \(n=1\)에서는
\(z_{\rm cut}=4.357\)보다 \(A_{\rm cap}=4.0\)가 항상 먼저 걸려
\(\mathcal A=4RT\)다. 결과적으로

\[
 \frac{\partial\ln L_q}{\partial V}=0
\]

이며 사용자 핵심 조건인 electrode-potential-dependent barrier가
구현되지 않았다.

더구나 default

\[
 \Delta H_a^{\rm eff}=\Delta H_a-\chi_d\Omega
\]

는 equilibrium mixing parameter \(\Omega\)를 activation barrier
감소량으로도 사용한다. \(\Omega\)는 chemical potential을 통해
affinity에 이미 들어가야 하므로, saddle-state excess free energy를
별도로 유도하지 않고 \(-\chi\Omega\)를 더하면 역할 중복과
double counting 위험이 있다.

후속 정본은

\[
 \Delta G^\ddagger_\pm
 =G^\ddagger(x,T,\sigma,\ldots)-G_{\rm initial/final}
\]

에서 forward/reverse barrier를 각각 세우고, 그 비가 detailed
balance를 만족하는지 검산해야 한다. barrier의 \(T,V,x\) 의존은
이 식에서 나와야 하며 arbitrary cut에서 나오면 안 된다.

## 8. regular-solution spinodal 식의 정확한 지위

regular solution의 spinodal은

\[
 \xi_s^\pm=\frac{1\pm u}{2},\qquad
 u=\sqrt{1-\frac{2RT}{\Omega}},
 \qquad \Omega>2RT
\]

이고 두 homogeneous extrema의 전위 차는

\[
 \Delta U_{\rm sp}
 =\frac{2}{F}
  [\Omega u-2RT\,{\rm artanh}(u)].
\]

legacy 함수는 이 닫힌형과 최대 \(3.68\times10^{-20}\) V 오차로
일치하고, \(\Omega\le2RT\)에서 0으로 닫힌다. 수학식은 보존할 수 있다.

그러나 \(\Delta U_{\rm sp}\)는 homogeneous regular-solution
metastability의 spinodal upper scale이다. 실제 hysteresis는
nucleation barrier, interfacial/gradient energy, coherent strain,
defect와 history에 의해 spinodal 전에 전환될 수 있다. 따라서

\[
 U^d=U+\tfrac12\sigma_d h_\eta\gamma\Delta U_{\rm sp}
\]

의 \(\gamma,h_\eta\)는 이론에서 유도된 closure가 아니라
phenomenological interpolation이다.

현재 default graphite transition에는 `gamma`가 하나도 없어
hysteresis가 전부 비활성이다. 또한 호출 사이에 phase fraction,
turning point, rest time 또는 internal history state가 저장되지
않으므로 partial-cycle memory를 계산하지 못한다. \(h_\eta\)라는
입력 숫자가 상태방정식을 대신하지 않는다.

## 9. apparent-U 분포의 두 종류를 분리해야 한다

v1.0.10은

\[
\left\langle\frac{dQ}{dV}\right\rangle
=\int \rho(U_{\rm app})
\left(\frac{dQ}{dV}\right)_{\rm single}
dU_{\rm app}
\]

라는 forward ensemble average를 적는다. 이 수학 구조는 유용하다.
하지만 \(U_{\rm app}=U+\eta\)의 \(\eta\) 안에 다음 두 현상을 함께
넣으면 안 된다.

- reversible thermodynamic heterogeneity:
  local composition, defect, strain, surface energy가 만드는
  \(U^0,\Omega,\Delta G\) 분포
- dissipative kinetic overpotential:
  current, charge transfer, diffusion와 contact resistance가 만드는
  rate/history-dependent \(\eta_{\rm kin}\)

첫째는 충분히 쉬어도 남고 둘째는 equilibrium에서 사라져야 한다.
“평형 \(U_j\)는 모든 입자에서 완전히 동일하고 local environment는
오직 \(\eta\)”라는 v1.0.10의 단정은 과도하다. particle size를 전면
배제하는 것도 특정 micrometre graphite 조건의 scale analysis 없이
보편 이론으로 승격할 수 없다.

또한 문건은 finite-rate skew를 \(L_V\)로 명시 계산하면서 두-상
empirical \(w_j\)가 같은 finite-rate broadening까지 “한꺼번에
흡수한다”고 쓴다. fit에서 둘을 동시에 풀면 double counting과
non-identifiability가 생긴다.

후속 모델은

\[
K_{\rm obs}
=K_{\rm equilibrium}
\ast \rho_{\rm thermo}
\quad\text{then evolved by}\quad
\mathcal K_{\rm kinetic}(I,T,\text{history})
\]

처럼 thermodynamic distribution과 kinetic evolution을 분리해야
한다. 각 층은 independent data 또는 hierarchy로 식별한다.

## 10. 필요한 대체 closure

사용자의 저온·유한전류 관측을 물리적으로 닫으려면 최소 다음 사슬이
필요하다.

1. material-specific free energy
   \(G(x,T,\text{phase/order/strain})\)
2. local electrochemical affinity
   \(\mathcal A=-\Delta_rG\)
3. detailed-balance-consistent forward/reverse rates
4. nucleation/phase-boundary 또는 population state의 시간 진화
5. electrode/particle transport와 current protocol
6. thermodynamic heterogeneity와 kinetic overpotential의 분리
7. state trajectory를 observation operator로 \(dQ/dV\)에 변환

이 구조에서는 저온이 \(k\)를 낮추고 같은 current가 더 큰
nonequilibrium lag/overpotential을 요구하므로 peak가 낮고 넓어지는
현상이 결과로 나올 수 있다. current 자체를 arbitrary barrier
correction으로 넣을 필요가 없다.

## 11. Step 29.2 처분

| 항목 | 판정 |
|---|---|
| ideal logistic derivative | `PRESERVE_IN_IDEAL_LIMIT` |
| \(\Omega\ne0\)인데 ideal logistic 유지 | `REJECT_THERMODYNAMIC_INCONSISTENCY` |
| first-order causal relaxation | `PRESERVE_AS_REDUCED_MODEL` |
| default가 current broadening을 구현 | `REJECT_DEFAULT_PATH_EQUILIBRIUM` |
| grid threshold handoff | `REJECT_GRID_DEPENDENT_DISCONTINUITY` |
| direct \(L_V\) | `EMPIRICAL_ONLY_AND_REQUIRE_I_TO_ZERO` |
| spinodal gap closed form | `PRESERVE_AS_UPPER_METASTABILITY_SCALE` |
| \(\gamma,h_\eta\) branch shift | `EMPIRICAL_STATELESS_ONLY` |
| frozen \(A=4RT\) cut | `REJECT_NO_LOCAL_POTENTIAL_DEPENDENCE` |
| \(\Delta H_a-\chi\Omega\) default | `REJECT_UNDERIVED_BARRIER_OVERLOAD` |
| apparent-U forward ensemble average | `PRESERVE_WITH_THERMO_KINETIC_SPLIT` |
| all broadening absorbed into \(w\) while \(L_V\) also active | `REJECT_DOUBLE_COUNTING_RISK` |

판정은
`REDUCED_RELAXATION_PROMISING_LEGACY_CLOSURE_REJECTED`다.

이 문건은 감사 companion이므로 code를 대조한다. 향후 이론 정본에는
물리 유도만 두고, numerical scheme·API·identifier 판정은 별도
conformance 문건에 둔다.
