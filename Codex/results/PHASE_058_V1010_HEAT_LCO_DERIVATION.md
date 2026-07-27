# Phase 058 v1.0.10 entropy·heat·LCO 독립 재유도

정본일: 2026-07-28
대상: Phase 058 Step 29.3
기계 검산:
`Codex/results/PHASE_058_V1010_HEAT_LCO_VALIDATION.json`

## 1. 평형 전위와 반응 엔트로피

삽입 반응을 기준으로

\[
 \Delta_rG=\Delta_rH-T\Delta_rS=-FU_{\rm eq}
\]

라 두면

\[
 U_{\rm eq}
 =\frac{-\Delta_rH+T\Delta_rS}{F},
 \qquad
 \left(\frac{\partial U_{\rm eq}}{\partial T}\right)_{\rm state}
 =\frac{\Delta_rS}{F}
\]

이다. \(\Delta_rH,\Delta_rS\)가 온도에 따라 변하면 Gibbs–Helmholtz와
heat-capacity 항까지 포함해야 하지만, constant-\(\Delta H,\Delta S\)
근사 안에서 v1.0.10의 중심식은 단위와 부호가 맞다.

중요한 조건은 “어떤 reaction direction의 \(\Delta_rS\)인가”다.
삽입과 탈삽입은 부호가 반대이며, half-cell/full-cell current label과
섞으면 열 부호도 함께 뒤집힌다.

## 2. 겹친 전이의 entropy coefficient

전하 보존 음함수

\[
 \sum_jQ_j\xi_j(U_{\rm oc},T)=Qx
\]

를 고정 \(x\)에서 미분하면

\[
 \left.\frac{\partial U_{\rm oc}}{\partial T}\right|_x
 =-\frac{
 \sum_jQ_j(\partial\xi_j/\partial T)_U
 }{
 \sum_jQ_j(\partial\xi_j/\partial U)_T
 }.
\]

이 식 자체는 보존할 수 있다. ideal logistic

\[
 \xi_j
 =\operatorname{logistic}
 \left[\frac{U-U_j(T)}{w_j(T)}\right],
 \qquad
 g_j=\frac{\partial\xi_j}{\partial U}
\]

를 쓰면

\[
 \left.\frac{\partial U_{\rm oc}}{\partial T}\right|_x
 =
 \frac{
 \sum_jQ_jg_j
 [U'_j+z_jw'_j]
 }{
 \sum_jQ_jg_j
 },
 \qquad
 z_j=\frac{U-U_j}{w_j}.
\]

따라서 entropy coefficient의 configurational 항은 width contract에
따라 달라진다.

- \(w_j=RT/F\): \(z_jw'_j=(R/F)z_j\)
- \(w_j=n_jRT/F\), constant \(n_j\):
  \(z_jw'_j=(n_jR/F)z_j\)
- constant empirical \(w_j\): \(z_jw'_j=0\)

v1.0.10 code는 세 경우 모두 \((R/F)z_j\)를 더한다. 독립 검산 결과:

| width contract | 올바른 값과 code 오차 |
|---|---:|
| \(n=1\) | 0 |
| \(n=2\) | \(1.1946\times10^{-4}\) V/K |
| constant \(w=0.04\) V | \(1.1946\times10^{-4}\) V/K |

\(n=2\) case에서는 code와 독립값의 부호까지 달라졌다. 즉 Chapter 2의
entropy formula는 ideal \(n=1\) limit에서만 code와 theory가
일치한다.

두-상 empirical width에 ideal configurational entropy를 자동으로
붙이는 것도 정당화되지 않는다. 그 폭이 heterogeneity·kinetics를
흡수한 fit parameter라면 \(w'(T)\)를 독립 데이터로 정해야 한다.

## 3. endpoint clipping은 열역학이 아니다

ideal configurational partial molar entropy의 logit은
\(\xi\to0,1\)에서 발산한다. 이는 ideal dilute limit의 수학적
결과지만 실제 endpoint에서는 defect, finite site inventory,
interaction와 phase boundary가 regularize한다.

legacy code는 \(\xi\)를 \(10^{-12}\)와 \(1-10^{-12}\) 사이로 clip해
유한값을 만든다. 이는 overflow 방지 수치 선택이며 물리 cutoff가
아니다. endpoint entropy 또는 heat prediction으로 해석하면 안 된다.

## 4. reversible heat의 보존 가능한 부분

heat generation을 양수로 두고 full-cell discharge current를
\(I>0\)로 정한 Bernardi convention에서는

\[
 \dot Q
 =I(U_{\rm oc}-V)
 -IT\frac{\partial U_{\rm oc}}{\partial T},
\]

\[
 \boxed{
 \dot Q_{\rm rev}
 =-IT\frac{\partial U_{\rm oc}}{\partial T}
 }
\]

이다. 단위는
\({\rm A}\cdot{\rm K}\cdot{\rm V\,K^{-1}}={\rm W}\)로 맞고,
온도 \(T\)는 한 번만 곱한다.

이 항등식은 보존할 수 있지만 세 조건을 함께 명시해야 한다.

1. current sign
2. heat-generation sign
3. \(U_{\rm oc}\)와 \(\Delta_rS\)의 reaction direction

v1.0.10은 graphite half-cell, LCO half-cell과 full-cell discharge
이름을 혼합하므로 그림의 열 부호는 이 조건을 자동 만족하지 않는다.
후속 코드는 signed electrode reaction rate로 계산한 뒤 observation
layer에서 cell heat로 조립해야 한다.

## 5. irreversible heat는 현재 \(\ge0\)가 아니다

비가역열은 entropy production과 일관되게

\[
 \dot Q_{\rm irr}=I\eta\ge0
\]

이어야 한다. terminal convention에서
\(\eta=U_{\rm oc}-V\)를 쓸 수 있는 branch라면 \(I\eta\)의 부호가
양수가 되도록 current와 voltage 정의가 함께 고정돼야 한다.

legacy helper는 입력을 그대로 곱한다.

\[
 I=1,\ U_{\rm oc}=4,\ V=3 \Rightarrow +1\ {\rm W},
\]

\[
 I=1,\ U_{\rm oc}=3,\ V=4 \Rightarrow -1\ {\rm W}.
\]

따라서 docstring의 `>=0`은 함수가 보장하는 invariant가 아니다.
음수를 clip하는 것도 해법이 아니다. charge-transfer, ohmic,
diffusion 각 항을 thermodynamic force × flux로 구성해 entropy
production을 구조적으로 보장해야 한다.

## 6. branch 평균은 equilibrium entropy의 일반식이 아니다

v1.0.10은 charge/discharge entropy coefficient의 산술평균을
reversible part로 둔다. 두 branch가 equilibrium center를 기준으로
완전히 대칭이고 같은 state를 비교할 때는 실용 근사가 될 수 있다.

그러나 metastable branch는 서로 다른 internal state일 수 있고,
temperature에 따라 hysteresis gap도 변한다. 일반적으로 reversible
entropy는 equilibrium free energy에서 직접 계산해야 하며,
hysteresis loop area는 cycle dissipation으로 별도 계산해야 한다.
stateless branch 평균을 thermodynamic theorem으로 승격할 수 없다.

## 7. LCO electronic entropy에서 보존할 것

degenerate metal이고 \(g(E)\)가 \(E_F\) 근처 열폭에서 완만하면
Sommerfeld 결과

\[
 S_e(T,x)
 =\frac{\pi^2}{3}k_B^2Tg(E_F,x)
\]

는 표준 저온 전자기체 근사다. DOS normalization이 formula unit당인지,
atom당인지, spin을 포함하는지 명시하면 molar conversion도 가능하다.

따라서

\[
 \left.\frac{\partial S_e}{\partial x}\right|_T
 =\frac{\pi^2}{3}k_B^2T
 \frac{\partial g(E_F,x)}{\partial x}
\]

라는 미분 구조는 후보 이론으로 보존할 수 있다. 단, MIT two-phase
window에서 homogeneous Sommerfeld metal 가정이 어디까지 성립하는지는
조성별 electronic-structure 또는 calorimetry와 대조해야 한다.

## 8. MIT logistic gate는 Fermi–Dirac에서 유도되지 않는다

전자 energy-level occupation

\[
 f(E)=\{1+\exp[(E-E_F)/k_BT]\}^{-1}
\]

이 logistic 형태라는 사실은 composition에 따른 DOS
\(g(E_F,x)\)가 logistic라는 것을 유도하지 않는다. 서로 다른
독립변수와 물리량이다.

v1.0.10은

\[
 g(E_F,x)=g_{\max}
 \left[
 1-\sigma\left(\frac{x-x_{\rm MIT}}{\Delta x_{\rm MIT}}\right)
 \right]
\]

를 놓는다. 이는 매끄러운 empirical transition model로는 쓸 수
있지만 “Fermi 함수와 같은 모양이므로 물리적으로 자연히 나온다”는
정당화는 기각한다.

## 9. 전자 entropy gate의 sum-rule 충돌

위 gate를 미분하면 중심 깊이

\[
 \Delta S_{e,\min}
 =-\frac{\pi^2}{3}R
   \frac{k_BT}{e_V}
   \frac{g_{\max}}{4\Delta x_{\rm MIT}}
\]

를 얻는다. \(T=298.15\) K, \(g_{\max}=13\),
\(\Delta x_{\rm MIT}=0.05\)이면 \(-45.678\) J/(mol K)다.
이 숫자는 legacy code와 일치한다.

그러나 derivative는 반드시 endpoint sum rule을 만족한다.

\[
 \int_0^1
 \frac{\partial S_e}{\partial x}\,dx
 =S_e(1)-S_e(0).
\]

독립 적분은 \(-9.135\) J/(mol K), 즉 \(-1.099R\)를 얻었다.
이는 같은 문건이 제시한 \(0.18k_B\) per atom
\(=1.497\) J/(mol K) anchor의 6.10배다.

문건은 peak depth와 partial anchor가 “서로 다른 양”이라 비교하지
않는다고 쓰지만, derivative의 적분과 endpoint 차이는 독립일 수 없다.
다음 중 하나를 데이터로 다시 정해야 한다.

- \(g_{\max}\) normalization
- 실제 MIT에서 변하는 DOS fraction
- \(\Delta x_{\rm MIT}\)와 gate shape
- \(0.18k_B\) 값의 정확한 thermodynamic quantity

따라서 \(-46\) J/(mol K)를 physical anchor로 고정하면 안 된다.

## 10. theory의 T²와 code의 frozen Tref

전자 entropy가

\[
 \Delta S_e(T)=a_eT
\]

라면

\[
 U(T)=U(T_0)
 +\frac{\Delta S_0}{F}(T-T_0)
 +\frac{a_e}{2F}(T^2-T_0^2).
\]

문건의 \(1/2\) 계수는 맞다. 그러나 code는 전자 entropy를
\(T_{\rm ref}=298.15\) K에서 한 번 평가해 상수로 동결하고
\(U=(-\Delta H+T\Delta S_{\rm eff}(T_{\rm ref}))/F\)를 쓴다.
따라서 \(d^2U/dT^2=0\)이다.

328.15 K에서 theory의 integrated \(T^2\) 식과 code의 차이는
0.7145 mV였다. 크기가 작더라도 conformance는 0%/100% 문제다.
문건이 식별 신호라고 강조한 곡률을 code가 계산하지 않는다.

## 11. LCO composition mapping도 구현되지 않았다

전자 entropy는 \(x\)의 함수지만 default code는 electronic
transition의 `x_center=0.50` 한 점에서만 평가한다. 문건의
물리 anchor \(x_{\rm MIT}\approx0.85\)와 default
`x_MIT=0.50`도 다르다.

\[
 V\longrightarrow \xi_j\longrightarrow x_{\rm Li}
\longrightarrow g(E_F,x)
\]

의 state mapping이 없으므로 저장 curve는 조성에 따른 MIT gate가
아니라 한 전이의 constant entropy offset이다.

## 12. default LCO는 고전압 도핑 모델이 아니다

default LCO transition은 세 개이고 listed center는
3.93, 3.88, 4.05 V다. 다음 값은 전부 0개다.

- \(\Omega\)
- \(\gamma\)
- activation enthalpy
- dopant fraction/state
- oxygen activity 또는 surface reconstruction state

최고 center가 4.05 V라 4.5 V 이상 영역도 없다. \(R_n=0\)에서
\(I=0\)과 1 A curve의 최대 차는 정확히 0이었다.

따라서 현재 LCO는 rate-invariant three-bell placeholder다.
Al/Mg 등 도핑에 따른 고전압 안정화를 \(\Omega\) 감소와 \(U\) shift로
설명한다는 prose도 default에는 반영되지 않았고, 설령 반영해도 다음
chemistry를 닫지 못한다.

- dopant/defect charge compensation
- Co valence와 oxygen-hole/oxygen-loss thermodynamics
- O3/order/monoclinic/H1-3 structural free energies
- coherent strain와 phase boundary
- surface reconstruction/interphase
- electrolyte oxidation과 cutoff/history

어떤 항이 필요한지는 후속 primary-literature audit와 public-data
protocol 분류에서 확정해야 한다. 현 단계에서 임의 상수로 채우지 않는다.

## 13. Step 29.3 처분

| 항목 | 판정 |
|---|---|
| \(\partial U/\partial T=\Delta S/F\) | `PRESERVE_WITH_REACTION_SIGN` |
| implicit entropy weighting | `PRESERVE_GENERAL_FORM` |
| code의 config 항 | `PRESERVE_IDEAL_N1_ONLY` |
| empirical \(n,w\)에도 같은 config 항 | `REJECT_WIDTH_ENTROPY_MISMATCH` |
| \(\dot Q_{\rm rev}=-IT\partial U/\partial T\) | `PRESERVE_WITH_SIGN_CONTRACT` |
| irreversible helper의 \(\ge0\) 주장 | `REJECT` |
| branch arithmetic mean = reversible entropy | `EMPIRICAL_SYMMETRY_APPROXIMATION` |
| Sommerfeld functional form | `PRESERVE_WITH_DOS_NORMALIZATION_AND_DOMAIN` |
| composition logistic DOS gate | `EMPIRICAL_ONLY` |
| \(-46\) J/(mol K) gate depth as anchor | `REJECT_SUM_RULE_CONFLICT` |
| documented \(T^2\) shift | `THEORY_ONLY_NOT_IMPLEMENTED` |
| LCO composition-dependent gate | `NOT_IMPLEMENTED` |
| doped high-voltage LCO | `NOT_IMPLEMENTED` |

판정은
`HEAT_IDENTITY_PRESERVED_ENTROPY_AND_LCO_CLOSURE_REJECTED`다.

이 문건은 감사 companion이므로 code를 대조한다. 향후 이론 정본은
열역학·전자구조·반응열 논리만 담고, code conformance와 numerical
guard는 별도 문건에 둔다.
