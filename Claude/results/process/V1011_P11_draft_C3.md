# V1011 Phase 1.1 LCO 수식화 작성 드래프트 C3

대상: `docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex`의 `sec:lco-center`(L470-513) 및 `sec:lco-hys`(L684-708) 보강 supplement.  
범위: 드래프트만. `.tex`/코드 수정 없음. `sec:lco-map`, `sec:lco-Se`, `sec:lco-gate`, N7-N9는 손대지 않는다.

## 0. 직접 확인한 근거 범위

- base prompt: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/v1011_p11_base.txt` 전문 확인.
- 프로젝트 지침: `Codex/AGENTS.md` 전문 확인.
- Ch1 v1.0.11 원천: `sec:lco-map` L295-349, 흑연 forward 예시 `sec:pol`/`sec:center`/`sec:hys` L351-683, 대상 `sec:lco-center` L470-513, 대상 `sec:lco-hys` L684-708, 평형 peak 예시 L1168-1203, LCO decomp/code 연결 L1690-1765.
- 스타일 판정: `results/process/V1010_LCO_STYLE_REPORT.md` 전문 확인.
- SPEC: `results/builds/v9/v9-00_spine/AUTHOR_BRIEF.md` 전문 확인.
- calibration: `results/builds/ch1v10/review1/R1_broadening.md` 전문 확인.
- 참고 확인: `docs/v1.0.11/Anode_Fit_v1.0.11.py` L623-641의 `LCO_MSMR_LIT`는 tier-C 시연값으로만 확인했으며, 본 수식 드래프트의 물리 anchor로 승격하지 않는다.

## 1. `sec:lco-center` 재작성 드래프트

### 1.1 삽입 위치

- 권장 위치: L470 `\subsection{LCO 평형 중심과 ...}` 직후.
- 대체 범위: 현 L471-488의 줄글/단일식 블록을 아래 수식-주도 사슬로 교체.
- 보존 권장: L490-509 `verifybox`는 대표 스케일 검산이므로, 아래 사슬 뒤에 유지한다. 단, 새 사슬에서 `+0.83 mV/K -> +80 J/(mol K)`를 이미 수식으로 닫으므로 verifybox는 "대표 스케일 sanity"로 읽히게 된다.

### 1.2 재작성안

```latex
\textbf{(a) 출발 — 전극 공통 N0/N2 골격.}
식~\eqref{eq:n0map} 는 방향과 전류만
\[
\sigma_d=\begin{cases}+1&\text{방전}\\-1&\text{충전}\end{cases},
\qquad |I|=\text{c\_rate}\,Q_\cell
\]
으로 정하고, 전이 루프 안의 열역학 중심은 전이 인덱스 $j$ 와
반응 자유에너지 $\Delta G_j$ 가 정한다. LCO 로 넘어가도 이 자리에는
\[
j\in\mathcal J_\mathrm{LCO}=\{\mathrm T1,\mathrm T2,\mathrm T3\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j})
\mapsto
(\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat})
\]
만 대입된다. 곧 $\sigma_d$ 는 N1/N3/N8 의 방향 선택에 남고,
평형 중심 $U_j(T)$ 자체의 Gibbs 환산식에는 새 양극 부호가 끼지 않는다.

\textbf{(b) 연산 — Gibbs 항등식과 전위 환산 연결.}
전이 $j$ 의 비배치 반응 자유에너지를
\[
\Delta G_j^\mathrm{cat}(T)
=\Delta H_{\rxn,j}^\mathrm{cat}
-T\Delta S_{\rxn,j}^\mathrm{cat}
\]
로 쓰고, 앞 절의 평형 조건 식~\eqref{eq:eqcond} 를 LCO 입력값에 적용하면
($s=+1$)
\[
\Delta G_j^\mathrm{cat}(T)=-F\,U_j^\mathrm{cat}(T).
\]
따라서
\[
\Delta H_{\rxn,j}^\mathrm{cat}
-T\Delta S_{\rxn,j}^\mathrm{cat}
=-F\,U_j^\mathrm{cat}(T).
\]

\textbf{(c) 중간식 — 중심과 온도 미분.}
먼저 중심을 풀면
\[
U_j^\mathrm{cat}(T)
=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}
+T\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
같은 결과를 Gibbs 항등식으로 미분해 다시 확인하면
\[
\frac{\partial\Delta G_j^\mathrm{cat}}{\partial T}
=-\Delta S_{\rxn,j}^\mathrm{cat},
\qquad
\frac{\partial\Delta G_j^\mathrm{cat}}{\partial T}
=-F\,\frac{\partial U_j^\mathrm{cat}}{\partial T},
\]
이므로
\[
-F\,\frac{\partial U_j^\mathrm{cat}}{\partial T}
=-\Delta S_{\rxn,j}^\mathrm{cat}
\quad\Longrightarrow\quad
\frac{\partial U_j^\mathrm{cat}}{\partial T}
=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]

\textbf{(d) 박스 — LCO 양극 중심.}
\begin{equation}
\boxed{\;
U_j^\mathrm{cat}(T)
=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}
+T\Delta S_{\rxn,j}^\mathrm{cat}}{F},
\qquad
\frac{\partial U_j^\mathrm{cat}}{\partial T}
=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}
\quad(j\in\{\mathrm T1,\mathrm T2,\mathrm T3\})\; .}
\label{eq:lco-dUdT}
\end{equation}
부호 검산은 직접적이다. $\Delta S_{\rxn,j}^\mathrm{cat}>0$ 이면
$\partial U_j^\mathrm{cat}/\partial T>0$ 이라 온도가 오를수록 LCO 하프셀 중심이 오른다.
대표 단전극 계수 $+0.83\,\mathrm{mV/K}$ 는
\[
\Delta S_{\rxn}^\mathrm{cat}
=F\frac{\partial U}{\partial T}
=96485\times0.83\times10^{-3}
\simeq 80\,\mathrm{J\,mol^{-1}K^{-1}}
\]
로 역산되며, $30$ K 창에서는 $\Delta U\simeq25$ mV 규모다. 이 값은 전이별 정밀값이
아니라 단전극 LCO 스케일 검산이고, 전이별 값은 표~\ref{tab:lco-staging} 및
식~\eqref{eq:lco-decomp} 의 config/vib/electronic 성분을 피팅해 정한다.
```

### 1.3 원 줄글 대비

- 원 L471-476은 "유도에 전극 가정이 없다"는 결론을 먼저 말한다. 위 드래프트는 `eq:n0map`의 방향 부호가 열역학 중심식에 들어가지 않는다는 대입식을 먼저 보이고, 그 다음 LCO 전이 집합과 cat 입력값만 갈아 끼운다.
- 원 L477-482는 `\partial U_j/\partial T=\Delta S/F`를 `식~\eqref{eq:Uj}` 미분으로만 제시한다. 위 드래프트는 `\Delta G=-FU`와 `\partial\Delta G/\partial T=-\Delta S`를 연결해 부호 다리를 닫는다.
- 원 L483-488의 대표 스케일 서술은 유지하되, `F(0.83 mV/K)=80 J/(mol K)` 변환을 별도 식으로 보여 G-follow를 높인다.

### 1.4 논리 감사

- 확정: 결과식과 부호는 원문과 동일하다. `\Delta S>0 -> \partial U/\partial T>0`, `\Delta S=0 -> 온도 이동 0` 극한이 모두 맞다.
- 확정: 차원은 `J/mol` 나누기 `C/mol = V`, `J/(mol K)` 나누기 `C/mol = V/K`로 닫힌다.
- 확정: `eq:n0map`의 `\sigma_d`는 분극, 분기 중심, 꼬리 방향을 고르는 부호이고, `U_j(T)` Gibbs 환산의 전극 구분자는 아니다. 따라서 "양극이라 미분 부호가 뒤집힌다"는 추가 부호는 넣지 않는다.
- 미검증/범위 밖: `\Delta H_{\rxn,j}^\mathrm{cat}`, `\Delta S_{\rxn,j}^\mathrm{cat}`가 강한 온도 함수일 경우의 고차 보정은 현재 Ch1 입력 모델 밖이다. 현 문서의 선형 `U_j(T)` 입력에서는 위 미분이 정합한다.
- 결함 여부: 물리 결함은 발견하지 못했다. 결함은 결과식이 아니라 기존 줄글의 유도 밀도 부족이다.

## 2. `sec:lco-hys` 재작성 드래프트

### 2.1 삽입 위치

- 권장 위치: L684 `\subsection{LCO order--disorder 와 MIT 2상역 ...}` 직후.
- 대체 범위: 현 L685-708의 세 단락을 아래 공통 LCO 대입 사슬 + 세 경우(T2/T3, T1, 도핑)로 교체.
- 보존 경계: `sec:lco-Se`, `sec:lco-gate`, N7-N9로 새 식을 밀어 넣지 않는다. 전자항은 여기서 유도하지 않고, 이미 있는 `sec:lco-electronic`/`sec:lco-decomp`를 참조만 한다.

### 2.2 재작성안

```latex
\textbf{(a) 출발 — LCO 전이별 정규용액 자유에너지.}
\S\ref{sec:hys} 의 격자기체 자유에너지~\eqref{eq:gxi} 에 LCO 전이 집합
\[
\mathcal J_\mathrm{LCO}^{2\phi}=\{\mathrm T1_\mathrm{MIT},\mathrm T2_\mathrm{OD},\mathrm T3_\mathrm{OD}\}
\]
을 대입한다. 여기서 LCO 의 2상역 표기는 흑연 broadening calibration 의
``LiC$_{12}$, LiC$_6$ 두 개만 two-phase''와 별개다. 흑연 안에서는 그 두 staging 만
two-phase 이고, LCO 안에서는 표~\ref{tab:lco-staging} 의 T1 MIT plateau 및 T2/T3
order--disorder 전이가 정규용액 2상역으로 들어온다. 각 LCO 전이 $k$ 에 대해
\begin{equation}
g_k^\mathrm{cat}(\xi)
=g_k^0
+RT\big[\xi\ln\xi+(1-\xi)\ln(1-\xi)\big]
+\Omega_k^\mathrm{cat}\xi(1-\xi),
\qquad k\in\mathcal J_\mathrm{LCO}^{2\phi}.
\label{eq:lco-gxi-sub}
\end{equation}
이다. $\Omega_k^\mathrm{cat}$ 의 단위는 J/mol 이며, 표~\ref{tab:lco-staging} 의
$0.47$, $1.49$ J/(K mol) charge-order 값은 $\Delta S^\mathrm{config}$ 초기값이지
$\Omega$ 가 아니다.

\textbf{(b) 연산 — 곡률과 spinodal 문턱.}
식~\eqref{eq:lco-gxi-sub} 를 두 번 미분하면 흑연과 같은 곡률식에 LCO 전이별
$\Omega_k^\mathrm{cat}$ 만 들어간다:
\begin{equation}
\frac{\partial^2 g_k^\mathrm{cat}}{\partial\xi^2}
=\frac{RT}{\xi(1-\xi)}-2\Omega_k^\mathrm{cat}.
\label{eq:lco-gpp-sub}
\end{equation}
따라서 spinodal 은
\begin{equation}
\xi_{s,k}^{\pm}
=\frac12(1\pm u_k),\qquad
u_k=\sqrt{1-\frac{2RT}{\Omega_k^\mathrm{cat}}},
\qquad
\Omega_k^\mathrm{cat}>2RT.
\label{eq:lco-spinodal-sub}
\end{equation}
$\Omega_k^\mathrm{cat}\le2RT$ 이면 $u_k$ 가 실수가 아니므로 그 전이의 구조적
spinodal gap 은 코드처럼 $0$ 으로 둔다.

\textbf{(c) 중간식 — LCO 전위 곡선에 spinodal 대입.}
전위 곡선~\eqref{eq:Veq} 에 LCO 중심 $U_k^\mathrm{cat}(T)$ 와
$\Omega_k^\mathrm{cat}$ 를 넣으면
\begin{equation}
V_{\eq,k}^\mathrm{cat}(\xi)
=U_k^\mathrm{cat}(T)
+\frac{RT}{F}\ln\frac{\xi}{1-\xi}
+\frac{\Omega_k^\mathrm{cat}}{F}(1-2\xi).
\label{eq:lco-Veq-sub}
\end{equation}
식~\eqref{eq:lco-spinodal-sub} 의 두 끝점에서
\[
\frac{\xi}{1-\xi}\bigg|_{\xi_{s,k}^{\pm}}
=\frac{1\pm u_k}{1\mp u_k},
\qquad
(1-2\xi)\big|_{\xi_{s,k}^{\pm}}=\mp u_k
\]
이므로 극대-극소 차는
\begin{align}
\Delta U_{k}^{\hys,\mathrm{cat}}
&=V_{\eq,k}^\mathrm{cat}(\xi_{s,k}^{-})
-V_{\eq,k}^\mathrm{cat}(\xi_{s,k}^{+})\notag\\
&=\frac{RT}{F}\left[
\ln\frac{1-u_k}{1+u_k}
-\ln\frac{1+u_k}{1-u_k}\right]
+\frac{\Omega_k^\mathrm{cat}}{F}\{u_k-(-u_k)\}\notag\\
&=\frac{2}{F}\left[
\Omega_k^\mathrm{cat}u_k
-2RT\,\mathrm{artanh}\,u_k\right].
\label{eq:lco-hysdiff-sub}
\end{align}

\textbf{(d) 박스 — LCO 전이별 gap 과 분기 중심.}
\begin{equation}
\boxed{\;
\Delta U_k^{\hys,\mathrm{cat}}(T)
=
\begin{cases}
\dfrac{2}{F}\left[
\Omega_k^\mathrm{cat}u_k
-2RT\,\mathrm{artanh}\,u_k\right],
& \Omega_k^\mathrm{cat}>2RT,\\[6pt]
0,& \Omega_k^\mathrm{cat}\le2RT,
\end{cases}
\quad
u_k=\sqrt{1-\dfrac{2RT}{\Omega_k^\mathrm{cat}}}\; .}
\label{eq:lco-dUhys-sub}
\end{equation}
방향별 중심은 흑연 식~\eqref{eq:Ubranch} 의 같은 대입이다:
\begin{equation}
\boxed{\;
U_k^{d,\mathrm{cat}}
=U_k^\mathrm{cat}(T)
+\frac12\sigma_d h_{\eta,k}\gamma_k
\Delta U_k^{\hys,\mathrm{cat}}(T)\; .}
\label{eq:lco-Ubranch-sub}
\end{equation}
방전($\sigma_d=+1$)은 LCO 분기 중심을 $+$ 쪽으로, 충전($\sigma_d=-1$)은
$-$ 쪽으로 옮긴다. $\gamma_k\to0$ 또는 $\Omega_k^\mathrm{cat}\le2RT$ 에서
두 방향은 같은 $U_k^\mathrm{cat}(T)$ 로 돌아간다.
```

### 2.3 LCO-특화 세 경우

#### 2.3.1 T2/T3 order--disorder 대입

```latex
\textbf{(T2/T3) order--disorder.}
T2($\sim4.05$ V, hex$\to$monoclinic)와 T3($\sim4.17$--$4.20$ V,
monoclinic$\to$hex)는 LCO 의 order--disorder 쌍이다. 두 전이에 대해서는
\[
k\in\{\mathrm T2,\mathrm T3\},\qquad
\Omega_k^\mathrm{cat}>2RT
\]
이면 식~\eqref{eq:lco-dUhys-sub} 가 각각
\[
\Delta U_{\mathrm T2}^{\hys,\mathrm{cat}}
=\frac{2}{F}\left[
\Omega_{\mathrm T2}^\mathrm{cat}u_{\mathrm T2}
-2RT\,\mathrm{artanh}\,u_{\mathrm T2}\right],
\quad
u_{\mathrm T2}=\sqrt{1-\frac{2RT}{\Omega_{\mathrm T2}^\mathrm{cat}}},
\]
\[
\Delta U_{\mathrm T3}^{\hys,\mathrm{cat}}
=\frac{2}{F}\left[
\Omega_{\mathrm T3}^\mathrm{cat}u_{\mathrm T3}
-2RT\,\mathrm{artanh}\,u_{\mathrm T3}\right],
\quad
u_{\mathrm T3}=\sqrt{1-\frac{2RT}{\Omega_{\mathrm T3}^\mathrm{cat}}}
\]
로 열린다. 대응하는 분기 중심은
\[
U_{\mathrm T2}^{d,\mathrm{cat}}
=U_{\mathrm T2}^\mathrm{cat}(T)
+\frac12\sigma_d h_{\eta,\mathrm T2}\gamma_{\mathrm T2}
\Delta U_{\mathrm T2}^{\hys,\mathrm{cat}},
\]
\[
U_{\mathrm T3}^{d,\mathrm{cat}}
=U_{\mathrm T3}^\mathrm{cat}(T)
+\frac12\sigma_d h_{\eta,\mathrm T3}\gamma_{\mathrm T3}
\Delta U_{\mathrm T3}^{\hys,\mathrm{cat}}.
\]
Motohashi 의 $0.47$ 및 $1.49$ J/(mol K)는 이 두 전이의 config 엔트로피
초기값으로 $U_k^\mathrm{cat}(T)$ 의 $\Delta S_{\rxn,k}^\mathrm{cat}$ 슬롯에 들어가며,
spinodal 문턱을 정하는 $\Omega_k^\mathrm{cat}$ 수치로 대입하지 않는다.
```

#### 2.3.2 T1 MIT 2상역 대입

```latex
\textbf{(T1) MIT 2상역.}
T1($\sim3.90$ V, $x\approx0.94$--$0.75$)의 절연체$\to$금속 천이는
전위 plateau 를 갖는 LCO 2상역이므로 구조적 분기에는 같은 정규용액 문턱을 쓴다:
\[
u_{\mathrm T1}
=\sqrt{1-\frac{2RT}{\Omega_{\mathrm T1}^\mathrm{cat}}},
\qquad
\Delta U_{\mathrm T1}^{\hys,\mathrm{cat}}
=\frac{2}{F}\left[
\Omega_{\mathrm T1}^\mathrm{cat}u_{\mathrm T1}
-2RT\,\mathrm{artanh}\,u_{\mathrm T1}\right]
\quad(\Omega_{\mathrm T1}^\mathrm{cat}>2RT).
\]
그리고
\[
U_{\mathrm T1}^{d,\mathrm{cat}}
=U_{\mathrm T1}^\mathrm{cat}(T)
+\frac12\sigma_d h_{\eta,\mathrm T1}\gamma_{\mathrm T1}
\Delta U_{\mathrm T1}^{\hys,\mathrm{cat}}.
\]
여기서 MIT 의 전자 자유도는 $\Omega_{\mathrm T1}^\mathrm{cat}$ 로 흡수하지 않는다.
전자항은 식~\eqref{eq:lco-decomp} 의
$\Delta S_{e,\mathrm T1}^{\mathrm{mol}}(x,T)$ 로
$U_{\mathrm T1}^\mathrm{cat}(T)$ 와
$\partial U_{\mathrm T1}^\mathrm{cat}/\partial T$ 에 들어가고,
구조적 2상 gap 은 $\Omega_{\mathrm T1}^\mathrm{cat}$, $\gamma_{\mathrm T1}$ 가 맡는다.
이 분리가 config 2상역과 electronic 엔트로피를 이중계산하지 않는 조건이다.
```

#### 2.3.3 도핑 보정 대입

```latex
\textbf{도핑 보정(우리 시료).}
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 전자항 자체를 새 전이로 만들지 않고,
order--disorder/MIT 상전이의 유효 세기를 낮추는 입력 변화로 둔다. 수식상으로는
\[
\Omega_{k,\mathrm{dop}}^\mathrm{cat}
\le \Omega_{k,\mathrm{pure}}^\mathrm{cat}
\]
인 LCO 전이별 대입이다. 따라서
\[
\Delta U_{k,\mathrm{dop}}^{\hys,\mathrm{cat}}
=
\begin{cases}
\dfrac{2}{F}\left[
\Omega_{k,\mathrm{dop}}^\mathrm{cat}u_{k,\mathrm{dop}}
-2RT\,\mathrm{artanh}\,u_{k,\mathrm{dop}}\right],
& \Omega_{k,\mathrm{dop}}^\mathrm{cat}>2RT,\\[6pt]
0,& \Omega_{k,\mathrm{dop}}^\mathrm{cat}\le2RT,
\end{cases}
\]
\[
u_{k,\mathrm{dop}}
=\sqrt{1-\frac{2RT}{\Omega_{k,\mathrm{dop}}^\mathrm{cat}}},
\qquad
U_{k,\mathrm{dop}}^{d,\mathrm{cat}}
=U_{k,\mathrm{dop}}^\mathrm{cat}(T)
+\frac12\sigma_d h_{\eta,k}\gamma_k
\Delta U_{k,\mathrm{dop}}^{\hys,\mathrm{cat}}.
\]
$\Omega_{k,\mathrm{dop}}^\mathrm{cat}\to2RT^+$ 에서
$u_{k,\mathrm{dop}}\to0$ 이고
$\Delta U_{k,\mathrm{dop}}^{\hys,\mathrm{cat}}\to0$ 이므로,
상분리 gap 과 충방전 히스가 사라지는 원 줄글의 "smear" 서술이 수식으로 닫힌다.
$U_{k,\mathrm{dop}}^\mathrm{cat}$ 의 미세 shift 와 폭은 현 문서 원칙대로 우리 데이터 피팅 몫이며,
PSD convolution 또는 새 $\rho(U_\app)$ 모델을 도입하지 않는다.
```

### 2.4 원 줄글 대비

- 원 L685-687은 "같은 틀 그대로 적용"으로 끝난다. 위 드래프트는 `g_k^\mathrm{cat} -> g'' -> \xi_s^\pm -> \Delta U^\hys -> U^d`까지 LCO 전이별 기호를 실제로 대입한다.
- 원 L689-694의 T2/T3 설명은 정렬 현상과 엔트로피 값을 말하지만, spinodal 중간식이 없다. 위 드래프트는 T2와 T3의 `u_T2`, `u_T3`, `\Delta U_T2`, `\Delta U_T3`, `U_T2^d`, `U_T3^d`를 각각 펼친다.
- 원 L696-701의 MIT 설명은 `\Delta U_j^\hys`와 `\gamma_j`를 받는다고만 말한다. 위 드래프트는 T1 MIT의 구조적 gap과 electronic entropy 슬롯을 분리해, `\Omega_T1`와 `\Delta S_e`가 서로 다른 역할임을 닫는다.
- 원 L703-708의 도핑 설명은 "Ω를 2RT 쪽으로 낮춘다"는 서술이다. 위 드래프트는 `\Omega_{dop}\to2RT^+` 극한에서 `\Delta U^\hys\to0`, `\Omega_{dop}\le2RT`에서 gap 0을 보인다.

### 2.5 논리 감사

- 확정: LCO hys 결과식은 흑연 `sec:hys`의 `eq:gxi`, `eq:gpp`, `eq:spinodal`, `eq:Veq`, `eq:dUhys`, `eq:Ubranch`를 전이별 LCO 입력으로 대입한 것이다. 결과식, 부호, 코드 대응 원칙은 바꾸지 않는다.
- 확정: 부호는 원문과 동일하다. `\Delta U^\hys\ge0`, 방전 `\sigma_d=+1`은 `+1/2` shift, 충전 `\sigma_d=-1`은 `-1/2` shift다. `\gamma\to0`에서 구조적 히스가 꺼진다.
- 확정: 극한은 맞다. `\Omega\le2RT`에서는 `u`가 실수가 아니므로 gap 0, `\Omega\to2RT^+`에서는 `u\to0` 및 Taylor 전개로 `\Delta U^\hys\to0`이다.
- 확정: LCO와 흑연의 two-phase calibration은 서로 다른 전이 집합에 적용된다. R1 broadening calibration의 "LiC 계열 two-phase는 LiC12/LiC6 두 개만"은 흑연 내부 구분이고, LCO `sec:lco-hys`의 T1/T2/T3 2상역 서술과 모순이 아니다.
- 결함/수정안: `0.47`, `1.49` J/(mol K)는 `\Delta S^\mathrm{config}` 값이지 `\Omega`가 아니다. 이를 `\Omega_j`로 수치 대입하면 차원 오류가 된다. 따라서 hys 사슬에는 `\Omega_{\mathrm T2}`, `\Omega_{\mathrm T3}`를 J/mol 기호로 두고, `0.47/1.49`는 center/decomp의 entropy 슬롯에만 남겨야 한다.
- 근거 미발견: 현재 확인 범위 안에서는 T1/T2/T3의 신뢰 가능한 `\Omega_k^\mathrm{cat}` 수치가 제시되지 않았다. 그러므로 실제 수치 gap을 계산하지 않고, 문서 원칙대로 `\Omega_k`는 초기값/피팅값 자리로 둔다.
- detailed balance 감사: 구조적 히스가 꺼지는 `\gamma=0` 또는 `\Omega\le2RT` 한계에서 충전/방전 중심이 같은 `U_k^\mathrm{cat}`로 합쳐진다. 분기 평균도 `U_k^\mathrm{cat}`이므로, 새 사슬은 중심을 임의로 이동시키지 않는다.
- 신규 개념 금지 준수: PSD convolution, `\rho(U_\app)`, 새 `\rho_G` 모델, 새 gate는 도입하지 않았다. 도핑은 원문처럼 `\Omega` 저하와 fit shift/width로만 적었다.

## 3. 최종 편입 시 주의점

- `eq:lco-dUdT`는 이미 원문 L481에 존재한다. master 편입 시 라벨 중복을 피하려면 기존 라벨을 유지하고 본 드래프트의 박스식이 그 라벨을 차지하게 하면 된다.
- 본 supplement의 `eq:lco-*` 라벨은 드래프트용이다. master가 실제 `.tex`에 편입할 때 라벨명은 기존 번호 흐름에 맞춰 조정하면 된다.
- `LCO_MSMR_LIT` 코드 시연값 `3.930/3.880/4.050`, `x_MIT=0.50`은 원문 표 캡션에서도 tier-C placeholder로 분리되어 있다. 본 드래프트는 물리 anchor `T1~3.90`, `T2~4.05`, `T3~4.17--4.20`와 혼동하지 않는다.
- `sec:lco-hys`에서 `\Omega_k^\mathrm{cat}` 수치를 새로 만들지 않는다. 수치가 필요하면 round-trip 피팅 또는 별도 SPEC 근거가 있어야 한다.

## 4. 5줄 요약

1. center 핵심: `eq:n0map`은 방향/전류만 정하고, LCO 중심은 `\Delta G^\mathrm{cat}=-FU^\mathrm{cat}`와 Gibbs 항등식으로 `U=(-\Delta H+T\Delta S)/F`, `\partial U/\partial T=\Delta S/F`가 그대로 닫힌다.
2. hys 핵심: LCO T1/T2/T3 각각에 `g(\xi)->g''->\xi_s^\pm->\Delta U^\hys->U^d`를 실제 대입해 "같은 틀 적용" 줄글을 수식 사슬로 바꿨다.
3. 논리 결함: 결과식의 물리 결함은 발견하지 못했지만, `0.47/1.49 J/(mol K)`를 `\Omega`처럼 쓰면 차원 오류이므로 반드시 `\Delta S^\mathrm{config}`로만 취급해야 한다.
4. 물리 불변: 부호, 결과식, `\Omega\le2RT -> 0`, `\gamma\to0 -> 중심 합류`, LCO 단전극 `+0.83 mV/K -> +80 J/(mol K)` 스케일은 원문 원칙과 일치한다.
5. 가장 약했던 원 줄글: `sec:lco-hys`의 order--disorder/MIT/도핑 세 단락이 모두 `식 그대로 받는다`로 닫혀, LCO 전이별 `\Omega_k` 대입 중간식과 entropy/interaction 차원 분리가 빠져 있었다.
