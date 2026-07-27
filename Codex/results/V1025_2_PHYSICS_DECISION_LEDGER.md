# v1.0.25.2 Physics Decision Ledger

## Purpose

이 문서는 새 manuscript와 구현이 따라야 할 물리 결정을 먼저 고정한다.
코드의 현재 구조는 결정 근거가 아니며, 구현은 이 ledger의 downstream
artifact다.

Status:

- `ADOPT`: 정본으로 채택
- `ADOPT-BOUNDED`: 명시된 적용범위 안에서만 채택
- `EMPIRICAL`: 관측 곡선 표현으로만 채택
- `THEORY-ONLY`: 이론·대안으로 보존, production closure 아님
- `REJECT`: 현 형태 폐기
- `OPEN`: 추가 자료 또는 유도 필요

## A. State, coordinates, and observation

### PHY-001 — One physical state orientation

Status: `ADOPT`

각 transition의 진행좌표 \(\xi_j\)는 반응 orientation 하나에 대해 고정한다.
충전·방전은 같은 상태축 위의 signed rate로 표현한다.

\[
\dot\xi_j \gtrless 0,\qquad
I_j=z_jF\dot n_j
\]

branch가 바뀌어도 \(\xi_j\mapsto1-\xi_j\)로 재정의하거나 equilibrium
logistic orientation을 뒤집지 않는다.

용량 부호도 state orientation과 별도로 고정한다. 선언된 electrode-capacity
convention에서

\[
a_j\equiv\left(\frac{\partial Q_{\mathrm{chem}}}
{\partial\xi_j}\right)_{T,\ldots}
\]

는 **signed** storage coefficient이며 양수라고 가정하지 않는다. 완전한
monotonic transition에 대해

\[
s_j\equiv \xi_j(+\infty)-\xi_j(-\infty)\in\{-1,+1\}
\]

도 reaction/potential convention으로 한 번 정하고 branch마다 바꾸지
않는다. \(a_j\), \(s_j\), 관측 데이터의 capacity sign은 서로 다른
계약이다.

Downstream:

- Chapter 5 sign derivation 전면 재작성
- charge/discharge heat sign을 signed extent/current로 재유도
- branch-specific center/free energy는 허용하되 state meaning은 유지

### PHY-002 — Applied, internal, drive, and equilibrium potentials are distinct

Status: `ADOPT`

\[
V_{\mathrm{app}},\quad V_n,\quad V_{\mathrm{drive}},\quad
V_{\mathrm{eq},j}(\xi,T)
\]

를 서로 다른 양으로 유지한다. \(V_{\mathrm{drive}}=V_n\)은 기본 근사일 수
있지만 항등식이 아니다. thermodynamic affinity는 equilibrium에서 0이어야
하며, 단순 \(F(V_{\mathrm{drive}}-U_j)\)는 일반 상태의 affinity가 아니라
center-referenced mobility coordinate로만 쓸 수 있다.

### PHY-003 — Monotonic curve and time trajectory are different problems

Status: `ADOPT`

- monotonic single branch: \(V\)를 독립변수로 쓴 curve model
- reversal/rest/nonmonotonic data: acquisition-time order를 보존하는 trajectory
  model

전압 정렬로 trajectory를 대체하지 않는다.

### PHY-004 — Observation background and chemical storage are separate

Status: `ADOPT`

\[
y_{\mathrm{signed}}(V_{\mathrm{app}})
=C_{\mathrm{meas}}(V_{\mathrm{app}})
+\frac{\mathrm dQ_{\mathrm{chem}}}{\mathrm dV_{\mathrm{app}}},
\]

\[
Q_{\mathrm{chem}}
=Q_{\mathrm{bg}}^{\mathrm{chem}}
+\sum_j a_j\xi_j.
\]

관측 baseline \(C_{\mathrm{meas}}\)는 전기화학 저장·double-layer·계측 baseline
등의 합일 수 있다. \(Q_{\mathrm{bg}}^{\mathrm{chem}}\)와 동일시하려면 별도
free-energy/state definition이 필요하다.

fit에 들어가는 \(y_{\mathrm{fit}}\)은 signed derivative 그대로일 수도 있고,
dataset 전체에 고정된 부호 \(\epsilon_{\mathrm{obs}}\in\{-1,+1\}\)를 곱한
값 또는 명시적인 magnitude preprocessing 결과일 수도 있다. 이 observation
map을 dataset provenance에 기록한다. fixed-sign map과 full transition
window에서는 관측 성분의 signed area가
\(\epsilon_{\mathrm{obs}}a_js_j\)다. magnitude preprocessing은 그 부호
정보를 버리므로 positive empirical area로부터 \(a_j\), \(s_j\), 반응
orientation을 역추론하지 않는다.

## B. Equilibrium and peak shape

### PHY-005 — Electron stoichiometry and peak width are independent

Status: `ADOPT`

반응 전자수 \(z_j\)는 balanced reaction이 정한다. Li insertion의 기본값은
\(z_j=1\)이다.

\[
z_j\not\equiv\frac{RT}{Fw_j}.
\]

\(w_j\) 또는 별도 \(\Gamma_j\)는 thermodynamic slope, static heterogeneity,
phase-size distribution, instrumental broadening 또는 empirical shape를
기술할 수 있다. 즉 \(z_j\)를 관측 폭으로 **정의하지 않는다**. 이상적
lattice-gas 한계 \(w_j=RT/(z_jF)\)에서는 수치적 등식이 성립할 수 있지만,
그 값을 일반 empirical width의 Faraday stoichiometry나 heat multiplier로
쓰지 않는다.

Rejected:

- “effective width가 effective electron number를 정한다”
- \(\sum_j(RT/Fw_j)I_j\eta_j\)를 일반 dissipation으로 사용

### PHY-006 — Ideal logistic has a narrow thermodynamic domain

Status: `ADOPT-BOUNDED`

\[
\xi_{\mathrm{eq}}
=\left[1+\exp\left(-s_j\frac{zF(V-U)}{RT}\right)\right]^{-1},
\qquad s_j\in\{-1,+1\}
\]

은 independent-site ideal lattice-gas baseline이다. \(s_j\)는 선택한
reaction/state coordinate가 전위 증가에 따라 증가하면 \(+1\), 감소하면
\(-1\)인 **고정 orientation**이다. 충전·방전 branch에 따라 바꾸지 않는다.

자유 \(w\)를 쓰는

\[
\xi_{\mathrm{eff}}
=\left[1+\exp\left(-\frac{V-U}{w}\right)\right]^{-1}
\]

은 effective observation/occupancy ansatz일 수 있지만, \(w=RT/(zF)\)가
아니면 ideal thermodynamic derivation과 동일하다고 쓰지 않는다.

### PHY-007 — Skew-logistic is the empirical observation profile

Status: `EMPIRICAL`

\[
\sigma=\left[1+\exp(-(V-U)/w)\right]^{-1},\qquad
q_{\mathrm{shape}}=\sigma^\alpha,
\]

\[
\frac{\mathrm dq_{\mathrm{shape}}}{\mathrm dV}
=\frac{\alpha}{w}\sigma^\alpha(1-\sigma).
\]

empirical fit layer의 계약은

\[
y_{\mathrm{fit}}(V)=B_{\mathrm{obs}}
+\sum_j A_j\frac{\mathrm dq_{\mathrm{shape},j}}{\mathrm dV},
\qquad A_j\ge0
\]

이다. \(A_j\)는 positive observation-area amplitude다. signed chemical
storage coefficient \(a_j\)가 아니며, fixed-sign observation map과
microscopic state mapping이 별도로 성립할 때만
\(A_j=\epsilon_{\mathrm{obs}}a_js_j\) 같은 연결을 검토할 수 있다.

장점:

- nonnegative
- monotonic empirical cumulative profile
- \(w>0,\alpha>0,V\in(-\infty,\infty)\)에서 derivative의 exact unit area
- current fit과 일치

제한:

- \(\alpha\)는 새 phase 수가 아니다.
- \(\alpha\)를 chemical activity, electron number 또는 reaction coordinate
  asymmetry로 자동 해석하지 않는다.
- \(q_{\mathrm{shape}}\)는 면적보존 empirical cumulative coordinate다.
  별도 microscopic closure 없이 \(\xi^{\mathrm{chem}}\), charge-balance
  state, chemical potential 또는 reversible-heat state로 재사용하지 않는다.
- stored-value boundary coincidence와 grid 해상도는 profile별로 기록한다.
  accepted blend14는 \(w_{\min}=1.94054\) mV로 0.5 mV grid보다 넓지만
  stored-8dp \(w=0.12\) V 값이 수치상 상한과 같다. standalone
  graphite7에는 0.25 mV grid보다 좁은 \(w=0.15824\) mV 항이 있고,
  standalone Si7에는 stored-8dp \(\alpha=0.15,8.0\) 값이 수치상 양
  bound와 같다. 원 optimizer full-precision vector와 active-set 상태가
  없으므로 실제 bound hit로 단정하지 않는다. 서로 다른 profile의 경고를
  accepted blend14 하나의 결함처럼 합치지 않는다.

### PHY-008 — Regular solution is theory/reference until a physical solver is adopted

Status: `THEORY-ONLY`

\[
g(\xi,T)=g^0+RT[\xi\ln\xi+(1-\xi)\ln(1-\xi)]
+\Omega\xi(1-\xi)
\]

와

\[
\partial_\xi g
=RT\ln\frac{\xi}{1-\xi}+\Omega(1-2\xi)
\]

는 theory/reference로 보존한다.

\(\Omega\ne0\)에서는 equilibrium relation이 implicit이며,
\(\Omega>2RT\)에서는 nonconvex branch, common tangent/phase coexistence,
metastability와 spinodal을 다뤄야 한다. 이때 smooth free-width logistic을
regular-solution equilibrium이라고 부르지 않는다.

production adoption 조건:

- stable/global or specified metastable branch selection
- common-tangent or phase-field/finite-size closure
- charge and area conservation
- parameter identifiability
- implementation and tests

Maxwell gap을 finite-width kernel로 broaden한 곡선의
\(\Omega\to2RT^+\) regularity는 gap delta 항만 보고 판정하지 않는다.
gap mass \(m=1-2\theta_a=O(\sqrt{\Omega/RT-2})\)를 더하는 동시에, single-phase
적분에서 같은 mass의 중앙 조성구간이 빠진다. 두 leading
\(m\,\kappa(V-U^\circ)\) 항은 상쇄된다. 따라서 현 문건처럼 gap weight의
제곱근 개방만으로 broadened curve의 \(\partial_\Omega\) 발산을 결론내리는
것은 금지하며, 전체 measure의 asymptotic expansion 또는 수치 convergence로
판정한다.

### PHY-009 — Thermodynamic width, static broadening, and kinetic lag are separate

Status: `ADOPT`

\[
w_{\mathrm{obs}} \not\equiv w_{\mathrm{thermo}}
\not\equiv L_V.
\]

- \(w_{\mathrm{thermo}}(T)\): equilibrium isotherm derivative
- static broadening: distribution of centers/sizes/stress/instrument response
- \(L_V\): causal dynamic lag
- \(\alpha\): empirical asymmetry

다온도 reversible heat에는 thermodynamic width derivative만 들어갈 수 있다.
single-temperature fitted effective \(w\)의 \(T\)-derivative를 가정 없이
가역열로 사용하지 않는다.

## C. Charge balance and blends

### PHY-010 — Charge balance is the primary coupling

Status: `ADOPT`

\[
Q_{\mathrm{cell}}q
=Q_{\mathrm{bg}}^{\mathrm{chem}}(V_n,T)
+\sum_ja_j\xi_j.
\]

이 식을 먼저 두고 implicit \(V_n\) 또는 \(U_{\mathrm{OCV}}\)를 푼다.
ICA/DVA 식은 이 보존식의 derivative이며 별도 저장 law가 아니다.

### PHY-011 — Denominator failure is model inadmissibility

Status: `ADOPT`

\[
\frac{\mathrm dQ}{\mathrm dV_n}
=
\frac{C_{\mathrm{bg}}^{\mathrm{chem}}}
{1-Q_p\,\mathrm d\Theta/\mathrm dQ}
\]

\[
C_{\mathrm{bg}}^{\mathrm{chem}}
\equiv
\left.\frac{\partial Q_{\mathrm{bg}}^{\mathrm{chem}}}
{\partial V_n}\right|_T.
\]

이 chemical-storage derivative를 사용할 때 denominator가 0에 접근하는 것은 coordinate singularity,
음수가 되는 것은 선택한 monotonic inverse model의 admissibility failure다.
해당 관측점을 단순 삭제하는 근거로 쓰지 않는다.

### PHY-012 — Physical host blend and generic 14-component fit are separate models

Status: `ADOPT`

Physical host blend:

\[
Q=Q_{\mathrm{gr}}+Q_{\mathrm{Si}},\qquad
f_{\mathrm{Si}}=Q_{\mathrm{Si}}/Q,
\]

공통 internal potential과 host별 capacity allocation을 갖는다.
질량분율에서 용량분율로 바꿀 때 normalization basis도 함께 선언한다.
graphite native capacity를 고정하고 Si capacity를 추가한 raw \(Q\)는
고정 총 활물질 질량당 용량과 같은 양이 아니다.

Empirical blend:

\[
y(V)=B_{\mathrm{obs}}+\sum_{k=1}^{14}
Q_k\frac{\alpha_k}{w_k}\sigma_k^{\alpha_k}(1-\sigma_k).
\]

\(B_{\mathrm{obs}}\)는 constant observation baseline이며
\(C_{\mathrm{bg}}^{\mathrm{chem}}\)과 동일한 양이 아니다. 이 empirical
blend는 host assignment를 강제하지 않는다. 두 model을 같은 “default
blend” 이름으로 노출하지 않는다.

### PHY-013 — Material-specific closures remain material modules

Status: `ADOPT`

공통 core는 state, charge balance, equilibrium/kinetics/heat conventions만
소유한다. 다음은 material module에 둔다.

- graphite staging evidence and assignment
- LCO electronic/vibrational entropy and order/disorder evidence
- Si stress/plasticity and protocol-dependent amorphous/crystalline features

LCO와 Si/blend 현행 장을 graphite 공통장으로 덮어쓰지 않는다.
`sic`처럼 SiC와 silicon--carbon composite를 혼동할 수 있는 case 이름은
물질명을 풀어 쓰고 legacy alias만 남긴다.

## D. Kinetics and memory

### PHY-014 — Forward/backward rates own direction; mobility and target are separate

Status: `ADOPT`

\[
\dot\xi_j=J_j^+-J_j^-,
\qquad
J_j^+=r_j^+(1-\xi_j),\qquad
J_j^-=r_j^-\xi_j.
\]

\(r_j^\pm\)가 \(\xi_j\)와 무관하거나 local step에서 frozen일 때만

\[
\xi_{\mathrm{ss},j}
=\frac{r_j^+}{r_j^++r_j^-}
\]

가 explicit stationary target이다. state-dependent rate이면

\[
r_j^+(\xi_{\mathrm{ss}})(1-\xi_{\mathrm{ss}})
=r_j^-(\xi_{\mathrm{ss}})\xi_{\mathrm{ss}}
\]

의 implicit root를 푼다.

- rate sum: relaxation/mobility
- rate ratio: stationary target/detailed balance

Chapter 1의 scalar \(\chi\)와 Chapter 3의 transfer split \(\beta\)는 같은
parameter가 아니다.

### PHY-015 — Eyring prefactor includes an unknown transmission factor

Status: `ADOPT`

\[
k_0(T)=\frac{k_BT}{h}\kappa(T).
\]

\(\kappa(T)\)를 독립적으로 알지 못하면 activation entropy/intercept와
분리되지 않는다. \(k_0=k_BT/h\)를 universal equality로 두지 않는다.
또 partition-function ratio가 \(T\)에 의존할 때
\(\Delta S^\ddagger=R\ln(q^\ddagger/q_R)\)만으로 일반 activation entropy를
정의하지 않는다. 그 식은 \(T\)-의존을 \(\kappa\) 또는 effective fitted
parameter에 흡수한 제한된 해석이다.

### PHY-016 — Rate units are SI in the physical profile

Status: `ADOPT`

physical profile에서 \(dq/dt\)는 \(\mathrm s^{-1}\)로 Eyring 식에 넣는다.
\(\mathrm h^{-1}\) C-rate를 받으면 명시적으로 \(1/3600\)을 곱한다.

기존 fitted curve를 보존하는 hour-based convention은 별도
`legacy-compatible` profile로 격리한다. 3600은 \(T\)-independent
rate multiplier이므로 다온도 \(\ln(k/T)\) 대 \(1/T\)의 slope와 그
slope에서 식별한 \(\Delta H_a\) 자체는 바꾸지 않고 intercept를 바꾼다.
fixed \(\Delta H_a\) convention에서는

\[
\Delta S_a^{\mathrm{phys}}-\Delta S_a^{\mathrm{legacy}}
=-R\ln3600.
\]

따라서 다온도 slope, 일정한 prefactor/전달계수, 동일한 단위 convention이
확인된 \(\Delta H_a\)를 단위오류만으로 일괄 폐기하지 않는다. 반면
단일온도 fit에서는 \(\Delta H_a\)와 \(\Delta S_a\)가 분리 식별되지 않는다.
\(\Delta S_a\)를 고정해 offset을 enthalpy에 흡수한 경우
298.15 K에서 \(RT\ln3600=20.298\) kJ/mol은 apparent correction일 뿐이며,
그 legacy 값을 독립적인 physical activation enthalpy로 보고하지 않는다.

### PHY-017 — A causal kernel requires an initial/prehistory contract

Status: `ADOPT`

\[
\dot\xi=(\xi_{\mathrm{tar}}-\xi)/\tau
\]

또는 voltage-domain convolution에는 다음 중 하나가 필요하다.

- measured prehistory
- supplied initial state
- explicitly stated asymptotic prehistory
- finite-padding approximation with tolerance

5\(L\) padding을 exact \(-\infty\) boundary라고 쓰지 않는다.

### PHY-018 — Relaxation spectrum normalization is separate from residual amplitude

Status: `ADOPT`

\[
\int a(L)\,\mathrm dL=1,\qquad
\Theta(q)=\int a(L)\xi_L(q)\,\mathrm dL,
\]

\[
K(\Delta q)=\int a(L)L^{-1}e^{-\Delta q/L}\,\mathrm dL.
\]

tail-start residual amplitude는 별도 \(b(L)\)로 둔다. normalized measure와
amplitude-bearing spectrum을 동일 symbol로 재사용하지 않는다.

## E. Temperature and heat

### PHY-019 — Fixed-state, fixed-charge, and path derivatives are distinct

Status: `ADOPT`

\[
\left.\partial_TV\right|_{\xi},\qquad
\left.\partial_TU_{\mathrm{OCV}}\right|_q,\qquad
\frac{\mathrm dV}{\mathrm dT}\bigg|_{\mathrm{trajectory}}
\]

를 구분한다. apparent voltage의 path derivative를 reversible entropy
coefficient로 쓰지 않는다.

### PHY-020 — Reversible heat uses one declared sign convention

Status: `ADOPT`

하나의 written forward reaction에 대해

\[
U_{\mathrm{eq}}
\equiv-\frac{\Delta_rG}{zF},\qquad
I_{\mathrm{rxn}}\equiv zF\dot n_{\mathrm{rxn}},
\qquad \dot n_{\mathrm{rxn}}>0
\]

로 정의한다. 같은 reaction/state convention에서

\[
\Delta_rS
=zF\left.\frac{\partial U_{\mathrm{eq}}}{\partial T}\right|_{\mathrm{state}}.
\]

control volume에 남는 열을 양으로 세는 heat-generation-positive 규약이면
\(\dot Q_{\mathrm{rev,gen}}=-T\Delta_rS\,\dot n_{\mathrm{rxn}}\)이므로:

\[
\dot Q_{\mathrm{rev,gen}}
=
-I_{\mathrm{rxn}}T
\left.\frac{\partial U_{\mathrm{eq}}}{\partial T}\right|_{\mathrm{state}}.
\]

full-cell에서도 written forward cell reaction의 진행을 양으로 세어
\(I_{\mathrm{cell}}=zF\dot n_{\mathrm{cell}}>0\)로 고정하고:

\[
U_{\mathrm{cell}}=U_p-U_n,\qquad
\dot Q_{\mathrm{rev,gen}}
=-I_{\mathrm{cell}}T\frac{\partial U_{\mathrm{cell}}}{\partial T}.
\]

half-cell coefficient를 electrode-local heat로 배분하는 문제는
counter/reference electrode와 interface control volume을 명시할 때까지
`OPEN`으로 둔다.

### PHY-021 — OCV and transition entropy bases require an explicit closure

Status: `ADOPT`

두 basis를 동시에 독립 열원으로 더하지 않는다.

선택 A:

- measured/derived fixed-state OCV coefficient를 사용

선택 B:

- standard reaction entropy
- state-dependent configurational/partial-molar entropy
- background storage entropy

를 모두 정의하고 fixed-state derivative와 같음을 유도

현재 원고의 \(U'(T)\)만으로 된 transition basis는 일반 정합식으로 채택하지
않는다.

### PHY-022 — Irreversible production is local flux times conjugate affinity

Status: `ADOPT-BOUNDED`

\[
T\dot S_{\mathrm{irr},j}
=\dot n_j\mathcal A_j^{\mathrm{chem}}\ge0,
\]

또는 two-state network에서

\[
T\dot S_{\mathrm{irr},j}
=\frac{Q_j}{z_jF}RT(J_j^+-J_j^-)
\ln\frac{J_j^+}{J_j^-}\ge0.
\]

여기서 \(J_j^\pm\)는 PHY-014의 occupancy flux로 단위가
\(\mathrm s^{-1}\)이고 양수인 domain에서 log ratio를 쓴다. \(Q_j\)는
transition 전체의 **SI charge [C]**다. fit parameter가 mAh이면
\(Q_j^{\rm SI}=3.6Q_j^{\rm mAh}\), Ah이면
\(Q_j^{\rm SI}=3600Q_j^{\rm Ah}\)로 변환해야 위 식이 W가 된다.

이를 heat source와 동일시할 때는 unresolved internal-energy storage가 없다는
control-volume 가정을 명시한다.

단일 terminal polarization path에서는

\[
\dot Q_{\mathrm{irr,terminal}}=I(U_{\mathrm{oc}}-V)\ge0
\]

를 lumped approximation으로 쓸 수 있다. 단, signed current/potential
convention이 이 곱의 비음성을 보장하고, terminal voltage gap에 포함된
소산만 계산하며, rest의 internal relaxation과 hidden state-energy storage를
포함하지 않는다는 적용범위를 붙인다. 이는 위 local network law의 일반
대체식이 아니다.

금지:

- 외부 \(|I|\) 하나로 모든 내부 소산을 인수분해
- rest에서 \(I_{\mathrm{external}}=0\)이라는 이유로 내부 소산을 0으로 설정
- \(RT/(Fw)\)를 electron multiplier로 삽입

### PHY-023 — Relaxation heat must not be double counted

Status: `ADOPT`

같은 free-energy decrease를

- irreversible entropy production
- 별도 relaxation heat

로 두 번 더하지 않는다. reversible state-energy change, dissipated part,
stored part를 하나의 energy balance에서 분해한다.

### PHY-024 — Thermal tail needs a fresh power/energy derivation

Status: `REJECT`

현 후보의 thermal mirror는 채택하지 않는다.

보존 가능한 것은 특정 단일-mode, local-linear, stable-curvature 근사에서
residual 제곱이 \(e^{-2\Delta q/L}\) 꼴을 만들 수 있다는 정성적 관찰뿐이다.
amplitude와 \(1/L\) scaling은 power 식에서 다시 유도한다.

## F. Hysteresis

### PHY-025 — Branch dependence belongs to landscape, target, or mobility

Status: `ADOPT`

허용 가능한 원인:

- metastable branch free energy
- nucleation barrier/pinning
- stress/plastic memory
- dynamic lag
- branch-dependent mobility

같은 state coordinate의 orientation reversal은 원인으로 채택하지 않는다.

### PHY-026 — Local and global detailed balance are distinct

Status: `ADOPT`

branch-local transition rates가 local detailed balance를 만족해도, 계가
global equilibrium에 도달하지 않았을 수 있다. 모든 hysteresis를
“detailed-balance violation”으로 부르지 않는다.

### PHY-027 — Loop area is loss only for a closed comparable cycle

Status: `ADOPT-BOUNDED`

전압--전하 loop area를 dissipated work로 읽으려면:

- 동일 initial/final internal state
- side reaction 없음
- aging/capacity drift 없음
- consistent full/half-cell convention

이 필요하다.

## G. Empirical profile and evidence

### PHY-028 — Freeze the surviving stored-8dp accepted profile

Status: `ADOPT-BOUNDED`

정본:

- input hashes
- archived `sigr.csv`가 blend로 label되어 있으나 experimental protocol은
  현재 `UNKNOWN`이라는 provenance state
- active preprocessing body
- 0.060--0.700 V window
- 0.5 mV grid
- linear unweighted residual
- seed sets/restarts/RNG state/bounds
- 저장된 8-decimal 57-parameter vector
- 그 저장 벡터에서 재계산한 prediction과 residual hashes
- package versions and dtype

`build_two_versions.py`는 optimizer `best`를 저장 전에 소수 8자리로
반올림하고 당시 `pred`를 summary에서 제외했다. 따라서 원 optimizer의
full-precision vector와 prediction은 보존되어 있지 않으며 현 artifact만으로
exact optimizer reproduction을 주장할 수 없다. 6-decimal transition JSON은
presentation artifact다. 저장된 8-decimal profile은 **현재 남아 있는
canonical empirical reference**일 뿐 optimizer 원본은 아니다. builder는
`r.success`를 요구하지 않았고 termination/Jacobian/evaluation count도
보존하지 않아 original convergence와 global optimality 역시 확정하지 않는다.

### PHY-029 — Fit success does not assign mechanisms

Status: `ADOPT`

높은 \(R^2\)와 낮은 BIC가 지지하는 것은 비교한 candidate family 안에서의
curve representation이다. 다음을 자동으로 지지하지 않는다.

- 각 peak의 phase identity
- graphite/Si host identity
- equilibrium vs kinetic asymmetry
- activation enthalpy
- reversible heat
- unique parameter decomposition

### PHY-030 — Evidence grades travel with each claim

Status: `ADOPT`

최소 등급:

- direct measurement / raw dataset
- literature anchored
- independently derived
- calibrated empirical
- seed/placeholder
- not identified
- not implemented

한 parameter가 다른 절로 이동할 때 등급을 잃지 않는다.

## H. Manuscript and implementation boundary

### PHY-031 — Manuscript body is physics-only

Status: `ADOPT`

본문에는 물리량, 가정, 유도, 적용범위, falsification을 둔다. existence와
uniqueness, admissibility, stable/metastable branch selection, boundary/initial
condition처럼 mathematical closure에 필요한 해법 조건도 물리 본문에 남긴다.

code symbol, library, loop/tolerance, file path, test gate, commit과 작업 이력은
지정된 implementation section 또는 외부 conformance ledger에 둔다.

### PHY-032 — Code must trace to physics IDs

Status: `ADOPT`

각 production behavior는 다음을 갖는다.

- Physics ID
- physical statement
- validity domain
- implementation symbol
- invariant/test
- conformance status

구현 편의를 이유로 physics decision을 역수정하지 않는다.

## Open decisions

| ID | Question | Needed evidence |
|---|---|---|
| OPEN-01 | graphite transition별 thermodynamic width의 실제 \(T\) law | multi-temperature equilibrium/near-equilibrium data |
| OPEN-02 | \(\alpha\)를 단순 empirical shape 이상으로 해석할 수 있는가 | independent structural or microscopic derivation |
| OPEN-03 | Si/blend 14 empirical components의 host attribution | host-resolved or composition-series constraints |
| OPEN-04 | half-cell entropy heat의 electrode/interface spatial allocation | full control-volume model and calorimetry |
| OPEN-05 | regular-solution/phase-field production closure | stable branch solver and data |
| OPEN-06 | true rate-independent hysteresis | rate-to-zero with controlled dwell/nucleation protocol |
| OPEN-07 | `sigr.csv` experimental protocol | source metadata; current addendum marks it unknown |

## Promotion gate

이 ledger의 `REJECT` 항이 기존 candidate에 남아 있는 동안 Chapter 1--5는
정본으로 승격하지 않는다. `OPEN` 항은 명시적으로 열린 채 manuscript에
남길 수 있지만, fit parameter나 silent fallback으로 닫은 것처럼 표현하지
않는다.
