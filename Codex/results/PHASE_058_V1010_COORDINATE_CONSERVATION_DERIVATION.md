# Phase 058 v1.0.10 좌표·보존식·dQ/dV 독립 재유도

정본일: 2026-07-28
대상: Phase 058 Step 29.1
기계 검산:
`Codex/results/PHASE_058_V1010_COORDINATE_CONSERVATION_VALIDATION.json`

## 1. 먼저 분리해야 하는 네 좌표

v1.0.10은 \(Q\), \(q\), 조성 \(x\), 전이 진행률 \(\xi_j\)를
한 식에 연결하지만, 실제 물리에서는 다음 네 양을 먼저 구별해야 한다.

1. \(Q_{\rm pass}(t)=\int I\,dt\): 전기회로를 지난 signed charge
2. \(Q_{\rm rxn}\): 선택한 전극 반응 방향의 상태좌표
3. \(q=Q_{\rm rxn}/Q_{\rm scale}\): 무차원 반응 진행좌표
4. \(x_{\rm Li}\): host formula unit당 Li 조성

한 전자/Li 반응이고 active host가 \(n_{\rm host}\) mol이면

\[
  dQ_{\rm rxn}=-n_{\rm host}F\,dx_{\rm Li}
\]

로 묶인다. 여기서는 \(Q_{\rm rxn}\)을 탈리튬화 방향에서 증가하도록
정했으므로 \(x_{\rm Li}\)가 감소할 때 \(Q_{\rm rxn}\)이 증가한다.
부호를 반대로 택해도 되지만 문건 전체에서 한 번만 택해야 한다.

전이별 진행률 \(\xi_j\in[0,1]\)와 전이 charge \(Q_j\)를 쓰면

\[
  Q_{\rm rxn}(V)
  =Q_{\rm bg}(V)+\sum_j Q_j\xi_j(V),
  \qquad
  x_{\rm Li}(V)
  =x_{\rm ref}
  -\frac{Q_{\rm rxn}(V)}{n_{\rm host}F}.
\]

따라서 \(Q_j\)를 실제 coulomb으로 쓸 때만 두 번째 식이 바로 조성으로
연결된다. \(Q_j\)가 정규화 가중 \(\alpha_j\)라면
\(Q_j=Q_{\rm scale}\alpha_j\)와 active-material/stoichiometric
window가 별도로 필요하다.

## 2. 보존식에서 dQ/dV로

위 상태식을 전위로 미분하면

\[
  \frac{dQ_{\rm rxn}}{dV}
  =\frac{dQ_{\rm bg}}{dV}
  +\sum_j Q_j\frac{d\xi_j}{dV}
  \equiv C_{\rm bg}(V)
  +\sum_j Q_j\frac{d\xi_j}{dV}.
\]

이 선형 합 구조는 보존식의 직접 미분이므로 보존할 수 있다. 다만
v1.0.10의 표현처럼 \(Q_{\rm cell}q\)라고 쓸 때는
\(Q_{\rm cell}\)이 다음 중 무엇인지 반드시 고정해야 한다.

- 실제 charge \(Q_{\rm cell,C}\,[{\rm C}]\)
- capacity \(Q_{\rm cell,Ah}\,[{\rm Ah}]\)
- 무차원 정규화 scale

세 정의를 한 인자에 겹치면 C-rate와 kinetics 단위가 무너진다.

## 3. 평형 logistic kernel

탈리튬화 진행률을

\[
  \xi_{\rm eq}(V)
  =\frac{1}{1+\exp[-(V-U)/w]}
\]

로 둔 이상 단일 전이의 미분은

\[
  \frac{d\xi_{\rm eq}}{dV}
  =\frac{\xi_{\rm eq}(1-\xi_{\rm eq})}{w}
  =\frac{1}{4w}
   {\rm sech}^2\!\left(\frac{V-U}{2w}\right).
\]

따라서 다음 세 성질은 정확하다.

\[
\int_{-\infty}^{\infty}
Q_j\frac{d\xi_{\rm eq}}{dV}\,dV=Q_j,
\]

\[
\left(\frac{dQ}{dV}\right)_{\max,j}
=\frac{Q_j}{4w_j},
\]

\[
{\rm FWHM}_j
=4w_j\,{\rm arcosh}\sqrt2
=3.52549\ldots\,w_j.
\]

독립 수치 검산은 \(T=298.15\) K, \(w=RT/F\)에서 unit-kernel 면적
오차 \(4.12\times10^{-9}\), FWHM 상대오차
\(2.68\times10^{-5}\)를 얻었다. v1.0.10 code의
\(\xi(1-\xi)/w\) 구현은 이 수학적 kernel과 일치한다.

그러나 이 결과는 logistic를 선택한 뒤의 정규화 성질이다. 두 상
전이의 유한 실험 폭, 입자 분포, 불균일 strain, nucleation과 transport를
logistic 하나가 유도했다는 뜻은 아니다. 특히 \(w=nRT/F\)의 \(n\)은
전자수의 Nernst 인자와 혼동하면 안 된다. 전자수 \(n_e\)는 이상
Nernst slope에서 보통 \(RT/(n_eF)\)로 들어간다. 폭을 늘리는
\(nRT/F\)의 \(n\)은 별도 미시 유도가 없으면 empirical width factor다.

## 4. signed dQ/dV와 양의 ICA bell

실험 장비의 누적 capacity를 각 branch에서 항상 양의 시간 방향으로
증가시키면

\[
  \frac{dQ_{\rm pass}}{dV}
  =\frac{|I|}{dV/dt}
\]

의 부호는 voltage sweep 방향에 따라 달라진다. 반면 탈리튬화 상태좌표
\(Q_{\rm rxn}(V)\)는 높은 전위에서 커지므로 \(dQ_{\rm rxn}/dV>0\)인
bell을 준다.

따라서 양의 ICA peak를 그릴 때는 다음 중 어느 것인지 밝혀야 한다.

- signed \(dQ_{\rm pass}/dV\)
- \(|dQ_{\rm pass}/dV|\)
- reaction-state derivative \(dQ_{\rm rxn}/dV\)

v1.0.10은 수식에서는 사실상 세 번째 또는 절댓값을 계산하지만
`discharge/charge` 이름을 함께 써 세 정의를 섞는다.

## 5. graphite/LCO/full-cell 방향은 하나의 cycle label이 아니다

전극 고유 반응 방향을 \(s_{\rm rxn}=+1\) delithiation으로 정의하면
graphite와 LCO 모두 높은 half-cell potential 쪽에서 일반적으로
\(x_{\rm Li}\)가 감소한다. 이 좌표는 전극을 가리지 않고 쓸 수 있다.

그러나 `charge`와 `discharge`는 반응 고유 명칭이 아니다.

- working-electrode vs Li half-cell의 discharge는 보통 lithiation,
  charge는 delithiation으로 기록된다.
- full-cell discharge에서는 graphite가 delithiate하고 cathode가
  lithiate한다.
- full-cell charge에서는 반대다.

v1.0.10 Ch1은 graphite half-cell potential을 선언하면서
`discharge = delithiation`을 쓰고, 같은 문건의 LCO 절은
`discharge = lithiation`을 쓴다. 같은 \(\sigma_d\)를
전극 독립이라고 부를 수 없다.

후속 정본은 최소한 다음 두 층을 분리해야 한다.

\[
  s_{\rm rxn}
  \quad\text{(lithiation/delithiation)}
  \qquad\text{vs}\qquad
  s_I,\ {\rm protocol}
  \quad\text{(instrument/full-cell/half-cell label)}.
\]

코드는 observation layer에서 electrode role과 protocol을 받아
\(s_{\rm rxn}\)으로 변환해야 한다. 열역학·kinetics 식에는
`discharge` 문자열을 직접 넣지 않는 편이 안전하다.

## 6. C-rate 단위의 factor-3600 결함

C-rate \(r_C\)의 단위는 \({\rm h^{-1}}\)다. 따라서

\[
  I[{\rm A}]
  =r_C[{\rm h^{-1}}]\,Q_{\rm cell}[{\rm Ah}]
\]

또는 charge를 coulomb으로 저장한다면

\[
  I[{\rm A}]
  =\frac{r_C[{\rm h^{-1}}]\,Q_{\rm cell}[{\rm C}]}{3600}.
\]

v1.0.10 이론 표는 \(Q_{\rm cell}\)을 C로 선언하지만, 문건과 facade는

\[
  I=r_CQ_{\rm cell}
\]

를 그대로 쓴다. 예를 들어 \(Q_{\rm cell}=3600\) C \(=1\) Ah,
\(r_C=0.2\,{\rm h^{-1}}\)이면 올바른 전류는 0.2 A인데 legacy 식은
숫자 720을 반환한다. 정확히 3600배 오류다.

한편 kinetics의

\[
  \frac{dq}{dt}=\frac{|I|}{Q_{\rm cell}},
  \qquad
  L_q=\frac{|I|}{Q_{\rm cell}k}
\]

는 \(I\)를 C/s, \(Q_{\rm cell}\)을 C로 쓰면 각각 s\(^{-1}\)와
무차원이어서 맞다. 즉 core 식의 SI 계약과 facade의 h\(^{-1}\)
계약이 서로 충돌한다.

## 7. default Q_j의 실제 지위

v1.0.10 default 전이 가중 합은 graphite 0.97, LCO 1.00이다.
demo는 \(Q_{\rm cell}=1\)을 쓰고 그림 축은 이후 버전에서
\([Q_{\rm cell}/{\rm V}]\)로 표시된다. 이는 default \(Q_j\)가
실제 coulomb보다 정규화 capacity fraction임을 강하게 시사한다.

따라서 이론 표의 \(Q_j[{\rm C}]\), code default의 무차원 숫자,
demo의 \(Q_{\rm cell}=1\)은 현재 하나의 unit contract가 아니다.
정본 설계에서는 다음처럼 타입을 분리해야 한다.

\[
  \alpha_j\ [-],\qquad \sum_j\alpha_j\le1,
  \qquad
  Q_j=\alpha_jQ_{\rm active},
\]

그리고 출력도

\[
  \frac{dq}{dV}\ [{\rm V^{-1}}]
  \quad\text{또는}\quad
  \frac{dQ}{dV}\ [{\rm Ah\,V^{-1}}]
\]

중 하나를 API와 그림에서 명시해야 한다.

## 8. 측정 전위와 내부 전위

constant current와 constant lumped resistance에서

\[
  V_{\rm int}=V_{\rm app}-s_I|I|R
\]

이면 \(dV_{\rm int}/dV_{\rm app}=1\)이므로
두 축의 differential-capacity 크기는 같고 peak 위치만 이동한다.
이 범위에서 v1.0.10의 보간은 수학적으로 가능하다.

하지만 \(R=R(x,T,I)\), charge-transfer overpotential,
concentration overpotential 또는 dynamic state가 들어가면

\[
  \frac{dQ}{dV_{\rm app}}
  =\frac{dQ}{dV_{\rm int}}
   \frac{dV_{\rm int}}{dV_{\rm app}}
\]

의 Jacobian을 생략할 수 없다. 단순 \(IR\) 이동은 peak broadening
physics가 아니며, 전류에 따른 높이 저하·폭 증가를 설명하지 않는다.

## 9. Step 29.1 처분

| 항목 | 판정 | 이유 |
|---|---|---|
| 전이 charge의 선형 합 | `PRESERVE_WITH_EXPLICIT_COORDINATE` | 보존식의 직접 결과 |
| logistic 미분 kernel | `PRESERVE` | 면적·높이·FWHM 독립 검산 통과 |
| \(Q_j\) 면적 보존 | `PRESERVE_CONDITIONALLY` | 충분한 전위창, 일관된 unit, 무배경 적분 조건 |
| \(Q_{\rm cell}[C]\)와 \(I=r_CQ_{\rm cell}\) | `REJECT_UNIT_INCONSISTENT` | 3600 환산 누락 |
| default \(Q_j\)를 C로 읽기 | `UNVERIFIED` | 실제 사용은 normalized weight |
| 전극 독립 discharge/charge 부호 | `REJECT_SEMANTIC_CONFLATION` | reaction direction과 protocol label 혼합 |
| constant \(IR\) shift를 broadening으로 읽기 | `REJECT` | 위치 이동일 뿐 폭 생성 아님 |
| \(w=nRT/F\)의 임의 \(n\)을 미시 물성으로 읽기 | `EMPIRICAL_ONLY` | 전자수와 반대 위치, 별도 유도 없음 |

Step 29.1의 수학 골격은 보존 가능하지만 좌표·단위·방향 계약은
재작성해야 한다. 판정은
`CORE_CONSERVATION_PRESERVED_COORDINATE_CONTRACT_REJECTED`다.

이 결과는 감사 companion이므로 code와 비교한다. 향후 이론 정본에는
위 물리 좌표와 식만 두고, identifier/API 대응은 별도 conformance
문건으로 분리해야 한다.
