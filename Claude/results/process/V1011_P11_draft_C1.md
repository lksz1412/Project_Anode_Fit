# Anode_Fit v1.0.11 Phase 1.1 LCO 수식화 작성 드래프트 C1

## 0. 작업 범위와 직접 확인 범위

- 산출물: `D:/Projects/Project_Anode_Fit/Claude/results/process/V1011_P11_draft_C1.md`
- 대상 원고: `Claude/docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex`
- 직접 읽은 범위:
  - base prompt: `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/v1011_p11_base.txt` 전문
  - project instruction: `Codex/AGENTS.md` 전문
  - style report: `Claude/results/process/V1010_LCO_STYLE_REPORT.md` 전문
  - SPEC: `Claude/results/builds/v9/v9-00_spine/AUTHOR_BRIEF.md` 전문
  - calibration: `Claude/results/builds/ch1v10/review1/R1_broadening.md` 전문
  - TeX source: L192-207 (`eq:n0map`), L300-349 (`sec:lco-map` 및 LCO 표), L330-469 (흑연 forward 예시 시작), L470-683 (`sec:lco-center`와 흑연 `sec:hys` 본체), L684-932 (`sec:lco-hys` 포함 라우팅 범위), L933-1110 (전자항 부호와 게이트), L1168-1203 (평형 peak 예시), L1680-1728 (`sec:lco-decomp`), L1800-1850 (node map).
- 금지 준수: `.tex` 및 코드 수정 없음. 본 파일은 supplement draft 이다.

## 1. `sec:lco-center` 재작성안

### 1.1 삽입 위치

- 위치: `graphite_ica_ch1_v1.0.11.tex` L470 직후.
- 교체 권장 범위: L471-489의 줄글 결론을 아래 수식-주도 사슬로 교체.
- 유지 권장 범위: L490-509 `verifybox`는 수치 sanity와 전셀 혼동 금지 설명이므로 유지하되, 앞 수식 사슬 뒤에 이어 붙인다.

### 1.2 재작성 수식 사슬 `(a) -> (d)`

```tex
\subsection{LCO 평형 중심과 $\partial U_j/\partial T$ — 양극 부호}\label{sec:lco-center}

\textbf{(a) 출발 — 전극이 아니라 반응 자유에너지.}
전이 $j$ 의 중심 전위는 전극 종류가 아니라 삽입 반응의 비배치 자유에너지 몫이 정한다.
\S\ref{sec:center} 의 평형 조건은
\begin{equation}
\Delta G_j(T)=-F\,U_j(T)
\qquad(s=+1,\ \text{식~\eqref{eq:eqcond} 의 방전 규약})
\label{eq:lco-GU-start}
\end{equation}
이고, LCO 양극에서는 같은 자리에 양극 반응값
$\Delta G_{\rxn,j}^\mathrm{cat}(T)$ 를 넣는다. 표~\ref{tab:lco-staging} 의
T1--T3 는 곧 이 $j$ 색인의 LCO 입력값이다.

\textbf{(b) 연산 — LCO 반응값 대입.}
상수 $\Delta H_{\rxn,j}^\mathrm{cat}$, $\Delta S_{\rxn,j}^\mathrm{cat}$ 로 평가하는
전이 슬롯에서는
\begin{equation}
\Delta G_{\rxn,j}^\mathrm{cat}
=\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}
=-F\,U_j^\mathrm{cat}(T).
\label{eq:lco-G-sub}
\end{equation}
따라서
\begin{equation}
U_j^\mathrm{cat}(T)
=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}
      +T\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\label{eq:lco-U-mid}
\end{equation}
흑연의 식~\eqref{eq:Uj} 와 다른 것은
$(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$ 의 값과 전이표뿐이다. LCO 의 높은 중심
($\sim3.9$--$4.2$ V)은 분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양인
양극 반응값에서 온다.

\textbf{(c) 중간식 — Gibbs 항등식으로 온도 미분을 닫기.}
온도 미분은 식~\eqref{eq:lco-U-mid} 를 외워 미분하는 것이 아니라
\begin{equation}
\frac{\partial \Delta G_{\rxn,j}^\mathrm{cat}}{\partial T}\Big|_{P}
=-\Delta S_{\rxn,j}^\mathrm{cat}
\label{eq:lco-gibbs-identity}
\end{equation}
와 식~\eqref{eq:lco-GU-start} 를 직접 연결해 닫는다:
\begin{equation}
\frac{\partial}{\partial T}\{-F U_j^\mathrm{cat}(T)\}
=-\Delta S_{\rxn,j}^\mathrm{cat}
\quad\Longrightarrow\quad
\frac{\partial U_j^\mathrm{cat}}{\partial T}
=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\label{eq:lco-dUdT-mid}
\end{equation}
상수 엔트로피 슬롯에서는 이 결과가 식~\eqref{eq:lco-U-mid} 의 직접 미분과 같다.
T1 전자항처럼 $\Delta S_{e,j}(x,T)\propto T$ 인 경우에는
식~\eqref{eq:lco-dUdT-mid} 를 미분형 기준식으로 삼고, 실제 $U_1(T)$ 는
\S\ref{sec:lco-electronic} 의 식~\eqref{eq:U1T2} 처럼 적분해 얻는다.
즉 $T\Delta S(T)$ 를 단순 곱으로 미분해 전자항의 $\tfrac12$ 적분 계수를 잃지 않는다.

\textbf{(d) 박스 — LCO 양극 결과식.}
\begin{equation}
\boxed{\;
U_j^\mathrm{cat}(T)
=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}
      +T\Delta S_{\rxn,j}^\mathrm{cat}}{F},
\qquad
\frac{\partial U_j^\mathrm{cat}}{\partial T}
=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}\;.
}
\label{eq:lco-U-dUdT-box}
\end{equation}
식~\eqref{eq:n0map} 의 N0 대입을 함께 보면 전극무관성이 더 명확하다:
\begin{equation}
\sigma_d=
\begin{cases}
+1 & \mathrm{discharge}\\
-1 & \mathrm{charge}
\end{cases},
\qquad
|I|=\mathrm{c\_rate}\,Q_\cell,
\label{eq:lco-n0-recall}
\end{equation}
인데, 이 두 실험조건 입력은 분극(N1), 분기 중심 선택(N3), 꼬리 방향(N8)에만 작용하고
N2 중심식 $U_j^\mathrm{cat}(T)$ 에는 들어가지 않는다. 따라서 LCO 에서 바뀌는 것은
전극 라벨이 아니라 $j\in\{\mathrm{T1, T2, T3}\}$ 의 양극 파라미터다.
``전극무관''은 선언이 아니라
\begin{equation}
U_j^\mathrm{cat}(T)
=U_j(T)\Big|_{\Delta H_{\rxn,j}\to\Delta H_{\rxn,j}^\mathrm{cat},
              \ \Delta S_{\rxn,j}\to\Delta S_{\rxn,j}^\mathrm{cat}}
\end{equation}
라는 대입식으로 읽힌다.
```

### 1.3 원 줄글 대비

- 기존 L471-476은 "유도에 전극 가정이 없다"를 선언한 뒤 높은 LCO 전위를 엔탈피값 차이로 설명했다. 위 재작성안은 같은 결론을 `ΔG=-FU`와 LCO 파라미터 대입식으로 닫는다.
- 기존 L477-482는 `∂U_j/∂T=ΔS/F`만 제시했다. 위 재작성안은 `∂ΔG/∂T=-ΔS`와 `ΔG=-FU`의 미분을 한 줄로 연결한다.
- 기존 L483-489의 LCO `ΔS_cat` 분해 예고와 스케일 비교는 유지 가능하다. 다만 전자항이 `T` 의존이라는 기존 L1048-1065와 충돌하지 않도록, 상수 슬롯 직접 미분과 T1 전자항 적분형을 분리해 쓴다.

### 1.4 논리 감사

- 확정: 결과식과 부호는 기존 원고와 불변이다. `ΔS/F`의 단위는 `[J/(mol K)]/[C/mol]=V/K` 이다.
- 확정: `eq:n0map`의 `σ_d`, `|I|`는 중심식에 직접 들어가지 않는다. LCO 양극 적용은 `N0'` 전이 dict 교체이지 새로운 전극 부호식이 아니다.
- 확정: LCO 단전극 `+0.83 mV/K` sanity는 기존 verifybox와 정합한다. `ΔS=F dU/dT` 이므로 양의 계수는 양의 전체 반응 엔트로피 스케일을 뜻한다.
- 보완 필요: "식~\eqref{eq:Uj} 의 T 미분"이라는 기존 표현은 상수 `ΔS` 슬롯에서는 충분하지만, T1 전자항처럼 `ΔS_e\propto T` 인 경우에는 오독 여지가 있다. 기존 전자항 절의 식~\eqref{eq:U1T2}가 이미 올바른 적분형을 갖고 있으므로, center 절에서는 Gibbs 미분형을 기준으로 명시하는 편이 안전하다. 결과식 변경은 아니다.

## 2. `sec:lco-hys` 재작성안

### 2.1 삽입 위치

- 위치: `graphite_ica_ch1_v1.0.11.tex` L684.
- 교체 권장 범위: L684-708 전체 subsection.
- 유지할 연결: 뒤의 `sec:width` L709 이후는 수정하지 않는다.

### 2.2 재작성 수식 사슬 `(a) -> (d)`

```tex
\subsection{LCO order--disorder 와 MIT 2상역 — 같은 정규용액 틀}\label{sec:lco-hys}

\textbf{(a) 출발 — LCO 세 전이의 정규용액 자유에너지.}
\S\ref{sec:hys} 의 가정은 전극명이 아니라
``동등한 리튬 자리의 점유/공공이 평균장 상호작용 $\Omega_j$ 를 갖는다''는 것이다.
따라서 LCO 전이 $j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}$ 에 대해서도 같은 조성 의존 자유에너지를 쓴다:
\begin{equation}
g_j^\mathrm{cat}(\xi)
=g_{j,0}^\mathrm{cat}
 +RT\{\xi\ln\xi+(1-\xi)\ln(1-\xi)\}
 +\Omega_j^\mathrm{cat}\,\xi(1-\xi).
\label{eq:lco-gxi}
\end{equation}
여기서 $\Omega_j^\mathrm{cat}$ 는 LCO 전이별 상호작용 파라미터이며, 수치로 대입하지 않는다.
표~\ref{tab:lco-staging} 의 $0.47$, $1.49$ J/K mol 값은 T2/T3 charge-order
엔트로피 스케일이지 $\Omega_j^\mathrm{cat}$ 값이 아니다.

\textbf{(b) 연산 — spinodal 조건을 LCO 전이마다 적용.}
식~\eqref{eq:lco-gxi} 의 곡률은 흑연과 같은 형식이다:
\begin{equation}
\frac{\partial^2 g_j^\mathrm{cat}}{\partial \xi^2}
=\frac{RT}{\xi(1-\xi)}-2\Omega_j^\mathrm{cat}.
\label{eq:lco-gpp}
\end{equation}
따라서 LCO 전이 $j$ 가 정규용액 two-phase 로 작동하는 조건은
\begin{equation}
\Omega_j^\mathrm{cat}>2RT
\quad\Longleftrightarrow\quad
\xi_{s,j}^{\pm,\mathrm{cat}}
=\frac12(1\pm u_j^\mathrm{cat}),\qquad
u_j^\mathrm{cat}
=\sqrt{1-\frac{2RT}{\Omega_j^\mathrm{cat}}}.
\label{eq:lco-spinodal}
\end{equation}
이 문건의 LCO calibration 에서는 T1 MIT plateau 와 T2/T3 order--disorder 전이가
이 정규용액 two-phase 대입 대상이다. R1 broadening 의
``two-phase = LiC$_{12}$, LiC$_6$ 두 개'' 결정은 흑연 staging 안의 전이별 구분이고,
LCO 전이표의 T1--T3 판정까지 배제하는 문장이 아니다.

\textbf{(c) 중간식 — T1, T2, T3 에 실제 대입.}
T1(MIT, $\sim3.90$ V, $x\approx0.94$--$0.75$)은 구조적 2상 plateau 와 전자 엔트로피 항을 함께 가진다:
\begin{align}
u_1^\mathrm{cat}(T)
&=\sqrt{1-\frac{2RT}{\Omega_1^\mathrm{cat}}},\qquad
\xi_{s,1}^{\pm,\mathrm{cat}}=\frac12(1\pm u_1^\mathrm{cat}), \notag\\
\Delta U_{1,\mathrm{MIT}}^\hys
&=\frac{2}{F}\left[
\Omega_1^\mathrm{cat}u_1^\mathrm{cat}
-2RT\,\mathrm{artanh}\,u_1^\mathrm{cat}
\right], \notag\\
U_1^{d,\mathrm{cat}}
&=U_1^\mathrm{cat}(T)
+\frac12\sigma_d h_{\eta,1}\gamma_1\Delta U_{1,\mathrm{MIT}}^\hys.
\label{eq:lco-T1-hys}
\end{align}
여기서 $U_1^\mathrm{cat}(T)$ 의 온도 이동은
$\Delta S_{\rxn,1}^\mathrm{cat}
=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}
\Delta S_{e,1}^{\mathrm{mol}}(x,T)$ 로 정해지고,
전자항은 히스테리시스 gap 식의 $\Omega_1^\mathrm{cat}$ 를 대체하지 않는다.

T2(order--disorder a, $\sim4.05$ V, $x\approx0.55$)는 전자항 off 인 charge-order 전이다:
\begin{align}
u_2^\mathrm{cat}(T)
&=\sqrt{1-\frac{2RT}{\Omega_2^\mathrm{cat}}},\qquad
\xi_{s,2}^{\pm,\mathrm{cat}}=\frac12(1\pm u_2^\mathrm{cat}), \notag\\
\Delta U_{2,\mathrm{OD}}^\hys
&=\frac{2}{F}\left[
\Omega_2^\mathrm{cat}u_2^\mathrm{cat}
-2RT\,\mathrm{artanh}\,u_2^\mathrm{cat}
\right], \notag\\
U_2^{d,\mathrm{cat}}
&=U_2^\mathrm{cat}(T)
+\frac12\sigma_d h_{\eta,2}\gamma_2\Delta U_{2,\mathrm{OD}}^\hys.
\label{eq:lco-T2-hys}
\end{align}
표~\ref{tab:lco-staging} 의 $\approx0.47$ J/K mol 은
$\Delta S_2^\mathrm{config}$ 중심 표준값의 문헌 스케일로만 쓰고,
$\Omega_2^\mathrm{cat}$ 는 위 식처럼 기호로 유지한다.

T3(order--disorder b, $\sim4.17$--$4.20$ V, $x\approx0.48$)도 같은 대입이다:
\begin{align}
u_3^\mathrm{cat}(T)
&=\sqrt{1-\frac{2RT}{\Omega_3^\mathrm{cat}}},\qquad
\xi_{s,3}^{\pm,\mathrm{cat}}=\frac12(1\pm u_3^\mathrm{cat}), \notag\\
\Delta U_{3,\mathrm{OD}}^\hys
&=\frac{2}{F}\left[
\Omega_3^\mathrm{cat}u_3^\mathrm{cat}
-2RT\,\mathrm{artanh}\,u_3^\mathrm{cat}
\right], \notag\\
U_3^{d,\mathrm{cat}}
&=U_3^\mathrm{cat}(T)
+\frac12\sigma_d h_{\eta,3}\gamma_3\Delta U_{3,\mathrm{OD}}^\hys.
\label{eq:lco-T3-hys}
\end{align}
표~\ref{tab:lco-staging} 의 $\approx1.49$ J/K mol 도
$\Delta S_3^\mathrm{config}$ 중심 표준값이며, $\Omega_3^\mathrm{cat}$ 수치가 아니다.

\textbf{(d) 박스 — LCO 정규용액 two-phase 와 도핑 보정.}
\begin{equation}
\boxed{\;
\Delta U_j^{\hys,\mathrm{cat}}
=
\begin{cases}
\dfrac{2}{F}\left[
\Omega_j^\mathrm{cat}u_j^\mathrm{cat}
-2RT\,\mathrm{artanh}\,u_j^\mathrm{cat}
\right],
& \Omega_j^\mathrm{cat}>2RT,\\[8pt]
0, & \Omega_j^\mathrm{cat}\le2RT,
\end{cases}
\quad
u_j^\mathrm{cat}
=\sqrt{1-\frac{2RT}{\Omega_j^\mathrm{cat}}},
\quad
j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}.
\;}
\label{eq:lco-dUhys-box}
\end{equation}
\begin{equation}
\boxed{\;
U_j^{d,\mathrm{cat}}
=U_j^\mathrm{cat}(T)
+\frac12\sigma_d h_{\eta,j}\gamma_j
\Delta U_j^{\hys,\mathrm{cat}}\;.
}
\label{eq:lco-Ubranch-box}
\end{equation}
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 새 식을 만들지 않는다. 같은 박스식의
$\Omega_j^\mathrm{cat}$ 가 우리 시료 피팅에서 더 작은 값으로 들어가면
$u_j^\mathrm{cat}$ 와 $\Delta U_j^{\hys,\mathrm{cat}}$ 가 함께 줄고,
$\Omega_j^\mathrm{cat}\to2RT^+$ 에서 gap 은 연속적으로 $0$ 으로 닫힌다.
$U_j$ 의 미세 shift 도 기존 중심 파라미터 피팅으로 들어가며,
PSD convolution 또는 새 $\rho_G$ 모델은 도입하지 않는다.
```

### 2.3 원 줄글 대비

- 기존 L684-688은 "같은 정규용액 틀"과 "세 전이 모두 대응"을 선언했다. 위 재작성안은 `g_j^\mathrm{cat}(\xi) -> g'' -> spinodal` 을 LCO 세 전이에 직접 대입한다.
- 기존 L689-694는 T2/T3 order-disorder 설명과 `0.47/1.49 J/K mol` 값을 한 문단에 두었다. 위 재작성안은 이 값들이 `ΔS_config` 문헌 스케일임을 분리하고, `Ω_2^\mathrm{cat}`, `Ω_3^\mathrm{cat}` 를 기호로 유지한다.
- 기존 L696-701은 T1 MIT가 `ΔU_hys`, `γ_j`를 받는다고 말했다. 위 재작성안은 `u_1`, `ξ_s,1^\pm`, `ΔU_1^\hys`, `U_1^d` 를 실제로 전개하고, 전자 엔트로피는 `U_1(T)`의 `ΔS_cat` 경로에만 들어가며 `Ω_1` spinodal 식을 대체하지 않음을 명시한다.
- 기존 L703-707은 도핑 보정을 줄글로 설명했다. 위 재작성안은 "도핑 = 같은 식에서 피팅된 `Ω_j`가 낮아짐"으로 수식에 묶어, 새 물리나 분포 모델 없이 gap 감소를 보인다.

### 2.4 논리 감사

- 확정: LCO T1, T2, T3를 정규용액 two-phase 대입 대상으로 두는 것은 대상 원고 L684-698 및 LCO 표 L335-337과 정합한다. R1의 "two-phase = LiC 계열 2개"는 흑연 staging calibration 이며, LCO 세 전이의 two-phase 판정을 부정하지 않는다.
- 확정: `Ω_j`의 차원은 J/mol 이고 `RT`와 같은 차원이다. `ΔU_hys`의 차원은 `[J/mol]/[C/mol]=V` 이다.
- 확정: `Ω_j>2RT` 에서만 `u_j`가 실수이며, `Ω_j\to2RT^+` 에서 `u_j\to0`, `artanh u=u+u^3/3+\cdots` 이므로 `ΔU_j^\hys\to0` 이다. 도핑으로 `Ω_j`가 낮아진다는 기존 문장은 gap 감소와 부호가 맞다.
- 확정: `ΔU_j^\hys\ge0`, `U_j^d=U_j+(1/2)\sigma_d h_{\eta,j}\gamma_j\Delta U_j^\hys` 이므로 방전 `σ_d=+1` 은 높은 분기, 충전 `σ_d=-1` 은 낮은 분기다. 기존 흑연 분기 부호와 1:1이다.
- 확정: detailed balance logistic 은 뒤 `sec:width`의 평형 점유 유도에 남아 있고, LCO hys 재작성은 그 logistic 중심 `U_j^d`를 제공한다. 즉 hys 수식화가 detailed balance 를 새로 가정하거나 깨지 않는다.
- 보완 필요: 원 줄글은 `0.47/1.49` 값을 order-disorder 문단에 두어, "Ω_j(0.47/1.49)"처럼 읽힐 위험이 있다. 그러나 원천 표 L333-337과 AUTHOR_BRIEF는 이 값을 `ΔS` 스케일로 둔다. 따라서 supplement에서는 `Ω_j`를 끝까지 기호로 유지해야 하며, 이 값들을 spinodal 수치에 대입하면 물리ㆍ차원 모두 오류가 된다.

## 3. 최종 논리 판정

- `sec:lco-center`: 결과식 결함은 발견하지 못했다. 다만 "식~\eqref{eq:Uj}의 T 미분"이라는 짧은 설명은 T1 전자항의 `ΔS_e(T)`까지 포함하면 오독될 수 있으므로, Gibbs 항등식 기반 미분형과 전자항 적분형을 함께 명시해야 한다.
- `sec:lco-hys`: 결과식 결함은 발견하지 못했다. 결함 후보는 물리 결과가 아니라 서술 밀도와 기호 혼동 위험이다. `Ω_j`를 `0.47/1.49`로 수치화하면 오류지만, 원고의 표와 SPEC 기준으로는 그 숫자가 `ΔS_config` 값임이 확인된다.
- 신규 개념 도입 없음: PSD convolution, `ρ(U_app)`, `ρ_G` 모델, 새 broadening 모델은 쓰지 않았다.
- 물리 불변: `∂U_j/∂T=ΔS/F`, `ΔU_hys=(2/F)[Ωu-2RT artanh u]`, `U_j^d=U_j+(1/2)\sigma_d h_\eta\gamma\Delta U_hys` 유지.
- 수치 원칙 불변: LCO `Ω_j`는 수치 날조 없이 기호로 유지했다. `0.47/1.49 J/K mol`은 T2/T3 config entropy 스케일로만 언급했다.

## 4. 5줄 요약

1. `center`는 `ΔG=-FU`와 `∂ΔG/∂T=-ΔS`를 직접 연결해 `∂U_j^\mathrm{cat}/∂T=ΔS_{\rxn,j}^\mathrm{cat}/F`로 닫는 수식 사슬이 필요하다.
2. `hys`는 `g_j^\mathrm{cat}(\xi) -> g'' -> \xi_s^\pm -> \Delta U_j^\hys -> U_j^d`를 T1/T2/T3 각각에 실제 대입하면 흑연 forward 절과 같은 밀도가 된다.
3. 논리 결함은 결과식 수준에서는 발견하지 못했다. 다만 `ΔS_e(T)`와 `0.47/1.49`의 기호 혼동은 보완하지 않으면 오독 가능성이 크다.
4. 물리ㆍ부호ㆍ결과식은 불변이다. `Ω_j`는 끝까지 기호로 유지했고 수치 대입은 하지 않았다.
5. 가장 약했던 원 줄글은 `hys`의 "같은 틀 그대로 적용" 3회 반복이다. 특히 order-disorder 엔트로피 값과 spinodal `Ω_j`가 같은 문단에 있어 구분 수식이 필요하다.
