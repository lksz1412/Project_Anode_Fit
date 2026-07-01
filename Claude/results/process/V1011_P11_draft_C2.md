# Anode_Fit v1.0.11 Phase 1.1 LCO 수식화 작성 드래프트 C2

## 0. 수행 범위와 정독 근거

- 산출물: `Claude/results/process/V1011_P11_draft_C2.md`
- 금지 준수: `.tex`/코드 수정 없음. 본 파일은 삽입용 supplement 초안만 제시한다.
- 직접 읽은 범위:
  - `docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex` L190-349 (`eq:n0map`, LCO map)
  - 같은 파일 L351-469 (`sec:pol`, `sec:center` 흑연 수식-주도 예시)
  - 같은 파일 L470-683 (`sec:lco-center` 전문)
  - 같은 파일 L684-932 (`sec:lco-hys` 전문 및 뒤따르는 width/logistic 문맥)
  - 같은 파일 L1168-1216 (`sec:eqpeak` 수식-주도 예시와 LCO peak 문맥)
  - 같은 파일 L1690-1765 (`sec:lco-decomp`, LCO 코드 일반화 문맥)
  - `results/process/V1010_LCO_STYLE_REPORT.md` 전문
  - `results/builds/v9/v9-00_spine/AUTHOR_BRIEF.md` 전문
  - `results/builds/ch1v10/review1/R1_broadening.md` 전문

아래 초안은 `sec:lco-map`, `sec:lco-Se`, `sec:lco-gate`, N7--N9, 전자엔트로피 본 유도는 건드리지 않고, `sec:lco-center`와 `sec:lco-hys`의 줄글 결론을 흑연 forward 절의 `(a) 출발 -> (b) 연산 -> (c) 중간식 -> (d) 박스` 밀도로 바꾸는 문안이다.

---

## 1. `sec:lco-center` 재작성안

### 1.1 삽입 위치

- 권장 교체 범위: `graphite_ica_ch1_v1.0.11.tex` L471-488
- 보존 권장 범위: L490-509 verifybox는 수치 sanity와 단전극/전셀 구분이 유효하므로, 아래 수식 사슬 뒤에 유지하거나 verifybox 첫 문장을 새 박스식 번호에 맞춰 연결한다.

### 1.2 재작성 수식 사슬

```latex
\textbf{(a) 출발 -- 전극 무관한 전기화학 평형.}
흑연 절의 평형 조건은 전극 재료명이 아니라 Li 1몰 이동의 Gibbs 자유에너지와 전기일의 균형에서 왔다.
따라서 LCO 양극 전이 $j$ 에도 같은 하프셀(vs Li/Li$^+$) 기준으로
\begin{equation}
\Delta G_{\rxn,j}^{\cat}(T)=-F\,U_j^{\cat}(T)
\label{eq:lco-GU}
\end{equation}
를 쓴다. 여기서 바뀌는 것은 전극 골격이 아니라 입력값
$(\Delta H_{\rxn,j}^{\cat},\Delta S_{\rxn,j}^{\cat})$ 이다.

\textbf{(b) 연산 -- LCO 반응 자유에너지 대입.}
전이 $j$ 의 비배치 몫을 기준값으로 보면
\begin{equation}
\Delta G_{\rxn,j}^{\cat}
=\Delta H_{\rxn,j}^{\cat}-T\Delta S_{\rxn,j}^{\cat}.
\label{eq:lco-GHS}
\end{equation}
이를 식~\eqref{eq:lco-GU} 에 넣으면
\begin{equation}
\Delta H_{\rxn,j}^{\cat}-T\Delta S_{\rxn,j}^{\cat}
=-F\,U_j^{\cat}.
\label{eq:lco-U-mid}
\end{equation}

\textbf{(c) 중간식 -- 중심 전위와 Gibbs 미분 다리.}
먼저 식~\eqref{eq:lco-U-mid} 를 $U_j^{\cat}$ 로 풀어
\begin{equation}
U_j^{\cat}(T)
=\frac{-\Delta H_{\rxn,j}^{\cat}
+T\Delta S_{\rxn,j}^{\cat}}{F}.
\label{eq:lco-Uj}
\end{equation}
온도 미분은 단순 괄호 미분으로만 말하지 않고 Gibbs 항등식으로 한 번 닫는다:
\begin{equation}
\frac{\partial\Delta G_{\rxn,j}^{\cat}}{\partial T}\Big|_{P,j}
=-\Delta S_{\rxn,j}^{\cat},
\qquad
\frac{\partial(-F U_j^{\cat})}{\partial T}
=-F\,\frac{\partial U_j^{\cat}}{\partial T}.
\label{eq:lco-Gibbs-bridge}
\end{equation}
두 식을 같게 놓으면
\begin{equation}
-F\,\frac{\partial U_j^{\cat}}{\partial T}
=-\Delta S_{\rxn,j}^{\cat}.
\label{eq:lco-dUdT-mid}
\end{equation}

\textbf{(d) 박스 -- 양극 엔트로피 계수.}
\begin{equation}
\boxed{\;
\frac{\partial U_j^{\cat}}{\partial T}
=\frac{\Delta S_{\rxn,j}^{\cat}}{F}\; }
\qquad
\left[
\Delta S_{\rxn,j}^{\cat}
=\Delta S_j^\mathrm{config}
+\Delta S_j^\mathrm{vib}
+\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)
\right].
\label{eq:lco-dUdT-chain}
\end{equation}
즉 LCO 단전극에서 $\Delta S_{\rxn,j}^{\cat}>0$ 이면 $U_j^{\cat}$ 는 온도에 따라 오른다.
대표 계수 $+0.83$ mV/K 는
$F(0.83\times10^{-3})\simeq80$ J/(mol K) 의 전체 단전극 스케일을 뜻하며,
T1 전자항의 작은 음의 보정과 같은 종류의 양으로 직접 비교하지 않는다.
``전체 계수''와 ``전이별 성분''의 층위를 분리하면 부호 충돌은 없다.
```

### 1.3 `eq:n0map` 대입으로 전극무관 논증 보강

`sec:lco-map` 자체는 정상 도입부라 수정 대상이 아니지만, `sec:lco-center`의 "전극 가정이 없다" 단정은 아래 한 단락을 덧붙이면 비약이 줄어든다.

```latex
\textbf{전극무관성의 작용 위치.}
식~\eqref{eq:n0map} 에서 실험조건은
$\sigma_d=\pm1$, $|I|=\mathrm{c\_rate}Q_\cell$ 로만 들어가고,
평형 중심은 전이 루프의 입력 $U_j(T)$ 로 들어간다. LCO 로 바꾸어도
\begin{equation}
\{\sigma_d,|I|,T,U_j,\Delta S_{\rxn,j}\}
\longrightarrow
\{\sigma_d,|I|,T,U_j^{\cat},\Delta S_{\rxn,j}^{\cat}\}
\label{eq:lco-n0-sub}
\end{equation}
일 뿐, $V_n=V_\app-\sigma_d|I|R_n$ 의 분극 부호와
$\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 의 열역학 부호는 서로 다른 슬롯이다.
따라서 양극의 높은 절대 전위($\sim3.9$--$4.2$ V)는
$U_j^{\cat}$ 의 입력값 문제이고, 온도 계수의 부호는
$\Delta S_{\rxn,j}^{\cat}$ 의 부호가 따로 정한다.
```

### 1.4 원 줄글 대비

- 원 L471-476은 "전극 가정이 없다"를 결론으로 말하지만, `eq:n0map`의 어느 슬롯이 전극 독립인지 직접 보여주지 않는다. 위 문안은 `U_j`, `Delta S_j`, `sigma_d`, `|I|`의 역할을 분리해 단정 비약을 줄인다.
- 원 L477-482는 식 자체는 맞지만, `Delta G=-FU`와 `partial Delta G/partial T=-Delta S` 사이의 미분 다리가 없다. 위 문안은 Gibbs 항등식으로 `partial U/partial T=Delta S/F`를 닫는다.
- 원 verifybox의 수치 원칙은 유지한다: `+0.83` mV/K -> 약 `+80` J/(mol K), 30 K 창 -> 약 `+25` mV, 단전극/전셀 혼동 금지.

### 1.5 논리 감사 결과

- 판정: 결과식, 부호, 수치 원칙은 무결. 결함은 물리식 오류가 아니라 유도 다리 누락이다.
- 부호: `Delta G=-FU`와 Gibbs 항등식에서 `partial U/partial T=Delta S/F`가 나오므로, 양의 LCO 단전극 엔트로피 계수는 양의 온도 이동과 일치한다.
- 차원: `Delta S/F`는 J/(mol K) / C/mol = V/K.
- 극한: `Delta S=0`이면 중심 온도 이동이 없다. `|I|->0`은 `eq:n0map`의 분극 항만 지우며 평형 중심식은 변하지 않는다.
- 주의/보완: 전자항처럼 `Delta S_e(x,T)\propto T`인 항을 다온도 모델에 실제로 풀어 넣을 때는, `U(T)=(-Delta H+T Delta S(T))/F`를 고정 `Delta H`로 기계 미분하면 `Delta S+T partial_T Delta S`가 생긴다. 열역학적으로 유지해야 할 식은 위 박스의 `partial U/partial T=Delta S(T)/F`이며, 위치는 기준온도에서
  \[
  U_j(T)=U_j(T_\mathrm{ref})+\frac{1}{F}\int_{T_\mathrm{ref}}^T
  \Delta S_{\rxn,j}^{\cat}(T')\,dT'
  \]
  로 해석해야 한다. 현 본문은 LCO 코드 시연값에서 전자항을 기준온도 상수 오프셋으로 동결한다고 쓰고 있으므로(LCO 표 캡션 문맥), 현재 결과식의 즉시 오류는 아니다. 다만 다온도 전자항을 본문에 더 강하게 전개할 때는 이 가드를 문장으로 남기는 편이 안전하다.

---

## 2. `sec:lco-hys` 재작성안

### 2.1 삽입 위치

- 권장 교체 범위: `graphite_ica_ch1_v1.0.11.tex` L684-708
- 보존할 앞식: `sec:hys`의 식 `g_j(\xi)`, `g_j''`, `spinodal`, `Delta U_j^\hys`, `U_j^d`는 그대로 재사용한다.
- 보존할 뒤절: `sec:width` 이후 N4--N9는 수정하지 않는다.

### 2.2 재작성 수식 사슬: LCO 공통 틀

```latex
\textbf{(a) 출발 -- LCO 세 전이를 같은 정규용액 자유에너지에 올린다.}
LCO 에서는 전이 집합을
\begin{equation}
\mathcal J_\mathrm{LCO}=\{1:\mathrm{MIT},\;2:\mathrm{OD}_a,\;3:\mathrm{OD}_b\}
\label{eq:lco-J}
\end{equation}
로 두고, 각 전이의 진행률 $\xi_j$ 에 대해 흑연과 같은 정규용액 몫을 쓴다:
\begin{equation}
g_j^{\cat}(\xi_j)
=g_{0,j}^{\cat}
+RT\{\xi_j\ln\xi_j+(1-\xi_j)\ln(1-\xi_j)\}
+\Omega_j^{\cat}\xi_j(1-\xi_j).
\label{eq:lco-gxi}
\end{equation}
여기서 새 물리는 넣지 않는다. LCO 로 바뀌는 것은
$U_j^{\cat}$, $\Omega_j^{\cat}$, $\gamma_j$, $h_{\eta,j}$ 의 전이별 입력값이다.

\textbf{(b) 연산 -- 곡률과 spinodal 문턱.}
식~\eqref{eq:lco-gxi} 를 두 번 미분하면
\begin{equation}
\frac{\partial^2 g_j^{\cat}}{\partial \xi_j^2}
=\frac{RT}{\xi_j(1-\xi_j)}-2\Omega_j^{\cat}.
\label{eq:lco-gpp}
\end{equation}
따라서 spinodal 은
\begin{equation}
\xi_{s,j}^{\pm}
=\frac12(1\pm u_j^{\cat}),
\qquad
u_j^{\cat}
=\sqrt{1-\frac{2RT}{\Omega_j^{\cat}}},
\qquad
\Omega_j^{\cat}>2RT.
\label{eq:lco-spinodal}
\end{equation}
반대로 $\Omega_j^{\cat}\le2RT$ 이면 $u_j^{\cat}$ 가 실수가 아니므로
spinodal gap 은 없다.

\textbf{(c) 중간식 -- LCO 전위 곡선에 spinodal 값을 실제 대입.}
LCO 전이 $j$ 의 평형 전위 곡선은
\begin{equation}
V_{\eq,j}^{\cat}(\xi)
=U_j^{\cat}
+\frac{RT}{F}\ln\frac{\xi}{1-\xi}
+\frac{\Omega_j^{\cat}}{F}(1-2\xi)
\label{eq:lco-Veq}
\end{equation}
이고, 두 spinodal 끝점에서는
\begin{align}
V_{\eq,j}^{\cat}(\xi_{s,j}^{-})
&=U_j^{\cat}
-\frac{2RT}{F}\operatorname{artanh}u_j^{\cat}
+\frac{\Omega_j^{\cat}}{F}u_j^{\cat},\\
V_{\eq,j}^{\cat}(\xi_{s,j}^{+})
&=U_j^{\cat}
+\frac{2RT}{F}\operatorname{artanh}u_j^{\cat}
-\frac{\Omega_j^{\cat}}{F}u_j^{\cat}.
\label{eq:lco-Vspinodal-sub}
\end{align}
상수 중심 $U_j^{\cat}$ 는 차에서 상쇄되고 평균에서는 남는다.

\textbf{(d) 박스 -- LCO 전이별 gap 과 분기 중심.}
\begin{equation}
\boxed{\;
\Delta U_{j,\mathrm{LCO}}^\hys
=\frac{2}{F}\left[
\Omega_j^{\cat}u_j^{\cat}
-2RT\,\operatorname{artanh}u_j^{\cat}
\right],
\quad
u_j^{\cat}=\sqrt{1-\frac{2RT}{\Omega_j^{\cat}}}\; }
\label{eq:lco-dUhys}
\end{equation}
with
\begin{equation}
\boxed{\;
U_{j,\mathrm{LCO}}^{\,d}
=U_j^{\cat}
+\frac12\sigma_d h_{\eta,j}\gamma_j
\Delta U_{j,\mathrm{LCO}}^\hys\; }.
\label{eq:lco-Ubranch}
\end{equation}
이는 흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 대입형이다.
``같은 틀''이라는 말은 식을 생략한다는 뜻이 아니라,
$\Omega_j\mapsto\Omega_j^{\cat}$, $U_j\mapsto U_j^{\cat}$,
$j\in\mathcal J_\mathrm{LCO}$ 를 실제로 넣는다는 뜻이다.
```

### 2.3 T2/T3 order--disorder 대입 문안

```latex
\textbf{(T2$\cdot$T3) order--disorder.}
T2($\sim4.05$ V, $x\approx0.55$)와 T3($\sim4.17$--$4.20$ V, $x\approx0.48$)는
LCO 의 order--disorder 쌍이다. 각 전이에 식~\eqref{eq:lco-spinodal} 을 대입하면
\begin{align}
u_2^{\cat}
&=\sqrt{1-\frac{2RT}{\Omega_2^{\cat}}},
&
\Delta U_{2,\mathrm{LCO}}^\hys
&=\frac{2}{F}\left[
\Omega_2^{\cat}u_2^{\cat}
-2RT\,\operatorname{artanh}u_2^{\cat}
\right],\\
u_3^{\cat}
&=\sqrt{1-\frac{2RT}{\Omega_3^{\cat}}},
&
\Delta U_{3,\mathrm{LCO}}^\hys
&=\frac{2}{F}\left[
\Omega_3^{\cat}u_3^{\cat}
-2RT\,\operatorname{artanh}u_3^{\cat}
\right].
\label{eq:lco-od-dUhys}
\end{align}
따라서 분기 중심은
\begin{equation}
U_{2,\mathrm{LCO}}^{\,d}
=U_2^{\cat}+\frac12\sigma_d h_{\eta,2}\gamma_2\Delta U_{2,\mathrm{LCO}}^\hys,
\qquad
U_{3,\mathrm{LCO}}^{\,d}
=U_3^{\cat}+\frac12\sigma_d h_{\eta,3}\gamma_3\Delta U_{3,\mathrm{LCO}}^\hys.
\label{eq:lco-od-Ubranch}
\end{equation}
T2/T3 의 charge-order 엔트로피 초기값
($\approx0.47$ 및 $\approx1.49$ J/(mol K), tier A)은
$U_j^{\cat}(T)$ 의 온도 이동 슬롯에 들어가고,
order--disorder 의 2상 분기 자체는 $\Omega_2^{\cat},\Omega_3^{\cat}>2RT$ 여부가 정한다.
```

### 2.4 T1 MIT 대입 문안

```latex
\textbf{(T1) MIT 2상역.}
T1($\sim3.90$ V, $x\approx0.94$--$0.75$)도 LCO 의 2상 공존 plateau 로 취급한다.
정규용액 분기식에는 T1 의 상호작용 입력을 그대로 넣어
\begin{align}
u_1^{\cat}
&=\sqrt{1-\frac{2RT}{\Omega_1^{\cat}}},
&
\Delta U_{1,\mathrm{LCO}}^\hys
&=\frac{2}{F}\left[
\Omega_1^{\cat}u_1^{\cat}
-2RT\,\operatorname{artanh}u_1^{\cat}
\right],\\
U_{1,\mathrm{LCO}}^{\,d}
&=U_1^{\cat}
+\frac12\sigma_d h_{\eta,1}\gamma_1
\Delta U_{1,\mathrm{LCO}}^\hys.
\label{eq:lco-mit-Ubranch}
\end{align}
MIT 고유의 전자 자유도는 이 식에 새 항으로 섞지 않는다.
그 항은 이미
\[
\Delta S_{\rxn,1}^{\cat}
=\Delta S_1^\mathrm{config}
+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^{\,\mathrm{mol}}(x,T)
\]
를 통해 $U_1^{\cat}(T)$ 의 온도 이동에 들어간다.
따라서 T1 에서는
``구조적 2상 분기'' = $\Omega_1^{\cat}$ 가 정하는
$\Delta U_{1,\mathrm{LCO}}^\hys$,
``전자 엔트로피'' = $\Delta S_{e,1}^{\,\mathrm{mol}}$ 이 정하는
$\partial U_1^{\cat}/\partial T$
로 슬롯을 분리해 이중계산을 피한다.
```

### 2.5 도핑 보정 대입 문안

```latex
\textbf{도핑 보정(우리 시료).}
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 같은 식의 입력값을 바꾼다.
pure-LCO 초기값을 $\Omega_j^{\cat,\mathrm{pure}}$ 로 두고,
도핑 시료의 피팅값을 $\Omega_j^{\cat,\mathrm{dop}}$ 로 읽으면
\begin{equation}
u_j^{\cat,\mathrm{dop}}
=\sqrt{1-\frac{2RT}{\Omega_j^{\cat,\mathrm{dop}}}},
\qquad
\Delta U_{j,\mathrm{dop}}^\hys
=\frac{2}{F}\left[
\Omega_j^{\cat,\mathrm{dop}}u_j^{\cat,\mathrm{dop}}
-2RT\,\operatorname{artanh}u_j^{\cat,\mathrm{dop}}
\right].
\label{eq:lco-doped-gap}
\end{equation}
따라서
\begin{equation}
\Omega_j^{\cat,\mathrm{dop}}\to2RT^+
\quad\Longrightarrow\quad
u_j^{\cat,\mathrm{dop}}\to0,\qquad
\Delta U_{j,\mathrm{dop}}^\hys\to0,
\label{eq:lco-doped-limit}
\end{equation}
이고, $\Omega_j^{\cat,\mathrm{dop}}\le2RT$ 이면 코드 분기처럼
$\Delta U_{j,\mathrm{dop}}^\hys=0$ 이다.
이것이 상전이 억제에 따른 히스테리시스 축소와 peak smear 의 수식 표현이다.
중심 전위의 미세 이동은 같은 전이 dict 의 $U_j^{\cat}$ 피팅값 이동으로 따로 들어가며,
$\Omega_j$ 하나가 중심 이동까지 자동으로 만든다고 쓰지 않는다.
```

### 2.6 LCO two-phase calibration 명시

- 흑연 calibration의 "two-phase = LiC12(2L->2)ㆍLiC6(2->1) 두 개만"은 흑연 staging 전이 구분이다.
- LCO에는 LiC 계열 명칭을 적용하지 않는다.
- 현재 LCO 문맥에서 정규용액 two-phase/spinodal 대상으로 쓰는 전이는 `T1 MIT`, `T2 order--disorder a`, `T3 order--disorder b` 세 개다. 즉 LCO에서는 `j in {1,2,3}`가 pure-LCO 초기 문헌값/모델값 기준의 2상 plateau 후보이며, 각 전이의 실제 gap 유무는 최종 피팅된 `Omega_j^{cat} > 2RT`가 결정한다.
- T4 O3->H1-3 고전압 전이는 현재 하프셀 상한 범위 밖 옵션이므로 이 supplement의 hys 사슬에 넣지 않는다.
- 도핑 시료에서는 같은 세 전이에 대해 `Omega_j`가 `2RT` 쪽으로 낮아질 수 있고, `Omega_j <= 2RT`로 피팅되는 전이는 같은 식 안에서 spinodal gap이 0으로 닫힌다. 이는 새 물리가 아니라 기존 `func_dU_hys` 문턱의 LCO 대입이다.

### 2.7 원 줄글 대비

- 원 L685-688은 "같은 틀 적용, 값만 LCO"라고 말하지만, 실제 `g'' -> spinodal -> Delta U_hys -> U^d` 대입식이 없다. 위 2.2가 공통 사슬을 닫는다.
- 원 L689-694의 T2/T3 order--disorder 단락은 물리 설명은 맞지만 `Omega_2`, `Omega_3` 대입식이 없다. 위 2.3이 두 전이의 `u_j`, `Delta U_j`, `U_j^d`를 각각 쓴다.
- 원 L696-701의 T1 MIT 단락은 "그대로 받는다"로 끝난다. 위 2.4는 T1도 `Omega_1`로 gap을 받고, 전자항은 `U_1(T)` 온도 이동 슬롯에만 들어간다고 분리한다.
- 원 L703-707의 도핑 단락은 `Omega_j` 저하, smear, `U_j` shift가 한 문장에 묶여 있어 원인 슬롯이 흐리다. 위 2.5는 `Omega_j`는 gap/smear, `U_j` 피팅값은 중심 shift로 분리한다.

### 2.8 논리 감사 결과

- 판정: LCO hys의 물리 결과식은 무결. 주요 문제는 "같은 틀"이라는 줄글 결론이 수식 대입을 생략한 G-derive 위반이다.
- 부호: `Delta U_j^\hys`는 극대-극소 차로 정의되어 0 이상이다. `U_j^d=U_j+1/2 sigma_d h_eta gamma Delta U`이므로 방전(`sigma_d=+1`) 중심은 위로, 충전(`sigma_d=-1`) 중심은 아래로 이동한다. 흑연 부호와 동일하다.
- 차원: `Omega u/F`와 `RT artanh(u)/F`는 J/mol / C/mol = V. `u`, `gamma`, `h_eta`는 무차원이다.
- 극한: `Omega_j -> 2RT+`이면 `u_j -> 0`, `artanh u = u+u^3/3+...`로 `Delta U_j^\hys -> 0`; `gamma_j -> 0` 또는 `h_eta -> 0`이면 분기 중심은 `U_j`로 돌아간다.
- detailed balance: N4/N5 logistic 유도는 수정하지 않는다. hys는 평형 자유에너지의 비단조성으로 분기 중심을 이동시키고, 이후 같은 `xi_eq` 식의 중심 `U_j^d`에 들어간다. 속도식이나 tail 쪽에 새 항을 만들지 않으므로 N7--N9를 건드리지 않는다.
- 이중계산: T1 MIT에서 전자 엔트로피를 hys gap에 추가하지 않는 것이 중요하다. 전자항은 `Delta S_rxn,1^cat`을 통해 `partial U_1/partial T`에 들어가고, 구조적 2상 분기는 `Omega_1`이 담당한다.
- 결함/수정안: 원 도핑 문장만 "Omega 저하가 U_j shift까지 만든다"로 읽힐 수 있는 약한 논리 결함이 있다. 수정안은 `Omega_j` 변화와 `U_j` shift를 별도 피팅 슬롯으로 쓰는 2.5 문안이다. 이는 새 개념 도입이 아니라 기존 `Omega`와 `U` 입력의 역할 분리다.

---

## 3. 최종 5줄 요약

1. `sec:lco-center`는 `Delta G=-F U`와 `partial Delta G/partial T=-Delta S`를 연결해 `partial U_j^cat/partial T=Delta S_rxn,j^cat/F`를 박스로 닫으면 된다.
2. `sec:lco-hys`는 `j={T1 MIT,T2 OD-a,T3 OD-b}` 각각에 `Omega_j^cat`를 넣어 `u_j`, `Delta U_j^hys`, `U_j^d`를 실제로 써야 한다.
3. 물리 결과식, 부호, 대표 수치(`+0.83` mV/K -> 약 `+80` J/(mol K), `Omega->2RT`에서 gap 0)는 유지된다.
4. 진짜 수식 오류는 발견하지 못했다. 다만 도핑 단락은 `Omega_j`가 gap/smear를, `U_j` 피팅값이 center shift를 담당한다고 분리해야 논리적으로 안전하다.
5. 가장 약했던 원 줄글은 `sec:lco-hys`의 "같은 틀 그대로 적용" 3회 반복이다. 흑연의 정답 사슬과 달리 LCO 전이별 대입 중간식이 없어 G-derive 요구를 만족하지 못했다.
