# V1012 Phase 4.3 draft C2 s1 — center/hys supplement

대상: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`

범위: `sec:lco-center`(L476--519), `sec:lco-hys`(L696--719) 두 절만.  
출발점: `Claude/results/process/V1011_P11_map_v10.md` 전문 확인 후 v1.0.12 원문 줄 위치와 수식 참조를 재대조했다.  
금지 준수: `.tex`/코드 수정 없음, `sec:lco-map`/`sec:lco-Se`/`sec:lco-gate` 본문 불가침, 물리/결과식/부호/수치 불변, `\Omega_j` 기호 유지, 수치 날조 없음.

읽은 범위:
- `V1011_P11_map_v10.md`: 1--319행 전체.
- `graphite_ica_ch1_v1.0.12.tex`: N2/N3 원문 411--721행 직접 확인.
- 보조 grep: `eq:lco-dUdT`, `eq:lco-decomp`, `tab:lco-staging`, `eq:n0map`, 매크로 `\dd`, `\eq`, `\rxn`, `\hys`, `\code`, `\mathrm{artanh}` 사용 여부.

---

## 1. `sec:lco-center`

### 위치

- 현재 헤더: L476 `\subsection{LCO 평형 중심과 $\partial U_j/\partial T$ — 양극 부호}\label{sec:lco-center}`
- 현재 줄글/식 후보 범위: L477--494.
- 보존 권장: L496--516 `verifybox`, L518--519 다음 절 연결 문장.
- `eq:lco-dUdT`는 현재 L487에 정의되고 L493, L498, L1229, L1750, L1790, L1877에서 참조된다. 따라서 이 supplement를 실제 편입할 경우 같은 라벨을 (d) 박스에 유지해야 한다.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — 흑연 forward 식의 전극-중립 골격.}
\S\ref{sec:center} 의 중심 전위 유도에서 물질명이 들어가는 곳은 입력값뿐이다. 평형 조건
식~\eqref{eq:eqcond} 는 삽입 반쪽반응의 전기화학 평형에서
\[
\Delta G_j=-sF U_j,\qquad s=+1
\]
로 닫히고, 비배치 반응 자유에너지는
\[
\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}
\]
이다. 그러므로 LCO 로 갈 때 새 부호를 세우지 않고 전이 집합과 입력값만 양극 슬롯으로 바꾼다:
\begin{equation}
j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j})
\mapsto
(\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat}).
\label{eq:lco-n0sub}
\end{equation}
방향 부호 $\sigma_d$ 는 식~\eqref{eq:n0map} 의 충방전 선택과 N3 분기 중심에서 쓰이는 값이고,
N2 의 평형 중심 환산식 자체에는 끼지 않는다.

\textbf{(b) 연산 — LCO 반응 자유에너지 대입.}
LCO 전이 $j$ 에 대해
\[
\Delta G_j^\mathrm{cat}
=\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}
\]
를 식~\eqref{eq:eqcond} 의 $\Delta G_j=-FU_j$ 에 넣으면
\begin{equation}
\Delta H_{\rxn,j}^\mathrm{cat}
-T\Delta S_{\rxn,j}^\mathrm{cat}
=-F\,U_j^\mathrm{cat}(T).
\label{eq:lco-Ujmid}
\end{equation}
이는 흑연 식~\eqref{eq:Ujmid} 에 상첨자 $\mathrm{cat}$ 만 붙인 형태다.

\textbf{(c) 중간식 — 중심과 온도 미분.}
식~\eqref{eq:lco-Ujmid} 를 $U_j^\mathrm{cat}$ 로 풀면
\[
U_j^\mathrm{cat}(T)
=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}
+T\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
직접 미분하면
\[
\frac{\partial U_j^\mathrm{cat}}{\partial T}
=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
같은 결과는 Gibbs 항등식으로도 닫힌다. 식~\eqref{eq:gibbsdef} 에서
\[
\left.\frac{\partial \Delta G_j^\mathrm{cat}}{\partial T}\right|_P
=-\Delta S_{\rxn,j}^\mathrm{cat}
\]
이고, 식~\eqref{eq:eqcond} 의 $\Delta G_j^\mathrm{cat}=-FU_j^\mathrm{cat}$ 를 미분하면
\[
-F\frac{\partial U_j^\mathrm{cat}}{\partial T}
=-\Delta S_{\rxn,j}^\mathrm{cat}.
\]
따라서 두 경로가 같은 온도 계수에 도착한다.

\textbf{(d) 박스 — LCO 양극 중심과 온도 계수.}
\begin{equation}
\boxed{\;
U_j^\mathrm{cat}(T)=
\frac{-\Delta H_{\rxn,j}^\mathrm{cat}
+T\Delta S_{\rxn,j}^\mathrm{cat}}{F},
\qquad
\frac{\partial U_j^\mathrm{cat}}{\partial T}
=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}
\quad(j\in\mathcal J_\mathrm{LCO})\;}
\label{eq:lco-dUdT}
\end{equation}
양극 영역의 높은 중심($\sim$3.9--4.2 V)은 식이 달라져서가 아니라
LCO 입력에서 분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양이 되기 때문이다. LCO 의
$\Delta S_{\rxn,j}^\mathrm{cat}$ 는 \S\ref{sec:lco-decomp} 의 config$\cdot$vib$\cdot$전자 성분 합으로
들어가며, 대표 단전극 엔트로피 계수 $\dd\phi/\dd T\approx+0.83$ mV/K 는
$F\times0.83\times10^{-3}\approx+80$ J/(mol\,K) 의 전체 단전극 스케일 확인값이다. 이 값은
표~\ref{tab:lco-staging} 의 전이별 성분값과 층위가 다르므로 직접 등치하지 않는다.
``전체 계수의 대표 스케일''과 ``T1 전자항의 국소 음의 보정''은 서로 다른 층위의 양이다.
```

### 원문 대비

- 현재 L477--481의 “식과 부호 관계는 흑연과 1:1” 결론을 (a) 전극-중립 출발점, (b) `\Delta G=-FU` 대입, (c) 이항과 미분, (d) 박스 수식으로 풀었다.
- 현재 L483--488의 온도 미분식은 결과만 제시되어 있다. draft는 직접 미분과 Gibbs 항등식 경로를 모두 써서 부호를 재검산한다.
- 현재 L489--494의 대표 스케일 설명은 유지하되, `+80` J/(mol K)가 전체 단전극 스케일이고 `tab:lco-staging`의 전이별 성분과 층위가 다르다는 guard를 더 명시했다.
- L496--516 `verifybox`의 수치와 부호 검산은 건드리지 않는 전제다. 위 (d) 박스가 `eq:lco-dUdT` 라벨을 이어받으면 기존 참조는 유지된다.

### 논리 감사

- 부호: `s=+1`, `\Delta G=-FU`, `\Delta G=\Delta H-T\Delta S` 이므로 `U=(-\Delta H+T\Delta S)/F`. 원문 식~\eqref{eq:Uj}와 동일하다.
- 차원: `\Delta H`, `T\Delta S`는 J/mol, `F`는 C/mol이므로 `U`는 J/C = V. `\Delta S/F`는 J/(mol K) / C/mol = V/K.
- 극한: `\Delta S_{\rxn,j}^\mathrm{cat}=0`이면 `\partial U/\partial T=0`; `\Delta H_{\rxn,j}^\mathrm{cat}`가 크게 음이면 `-\Delta H`가 양이 되어 중심이 오른다.
- 결과식 불변: 기존 `eq:lco-dUdT`의 물리 내용은 그대로이며, 라벨 위치만 (실제 편입 시) 결과 박스로 이동하는 구조다.
- 미확인/불가침: `sec:lco-decomp`, `sec:lco-Se`, `sec:lco-gate` 본문은 재작성하지 않았다. 여기서는 기존 참조 관계만 사용했다.

---

## 2. `sec:lco-hys`

### 위치

- 현재 헤더: L696 `\subsection{LCO order--disorder 와 MIT 2상역 — 같은 정규용액 틀}\label{sec:lco-hys}`
- 현재 줄글 후보 범위: L697--719.
- 다음 경계: L722 `\section{폭과 평형 점유 ...}\label{sec:width}`.
- 흑연 N3의 근거식은 L539 `eq:mu`, L545 `eq:gxi`, L552 `eq:gpp`, L558--560 `eq:spinodal`, L600--601 `eq:Veq`, L617--630 `eq:dUhys`, L647--648 `eq:Ubranch`에서 확인했다.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — LCO 세 전이를 같은 정규용액 자유에너지에 둔다.}
\S\ref{sec:hys} 의 격자기체$\cdot$정규용액 틀은 한 전이를
``동등한 자리에 리튬이 차고 빈다''는 진행률 문제로 적는다. 이 가정이 서는 LCO 전이에 대해
\begin{equation}
\mathcal J_\mathrm{LCO}=\{1:\mathrm{MIT},\ 2:\mathrm{OD}_a,\ 3:\mathrm{OD}_b\}
\label{eq:lco-J}
\end{equation}
를 두고, 각 전이의 진행률 $\xi_j$ 에 같은 자유에너지 몫을 쓴다:
\begin{equation}
g_j^\mathrm{cat}(\xi_j)=g_{0,j}^\mathrm{cat}
+RT\{\xi_j\ln\xi_j+(1-\xi_j)\ln(1-\xi_j)\}
+\Omega_j^\mathrm{cat}\xi_j(1-\xi_j).
\label{eq:lco-gxi}
\end{equation}
여기서 새 물리는 넣지 않는다. 바뀌는 것은
$U_j\mapsto U_j^\mathrm{cat}$, $\Omega_j\mapsto\Omega_j^\mathrm{cat}$,
$\gamma_j$, $h_{\eta,j}$ 같은 전이별 입력값이다.

\textbf{(b) 연산 — 곡률과 spinodal 문턱.}
식~\eqref{eq:lco-gxi} 를 두 번 미분하면
\begin{equation}
\frac{\partial^2 g_j^\mathrm{cat}}{\partial\xi_j^2}
=\frac{RT}{\xi_j(1-\xi_j)}-2\Omega_j^\mathrm{cat}.
\label{eq:lco-gpp}
\end{equation}
따라서 spinodal 조건 $g_j''=0$ 은
\begin{equation}
\xi_{s,j}^{\pm}
=\tfrac12(1\pm u_j^\mathrm{cat}),\qquad
u_j^\mathrm{cat}
=\sqrt{1-\frac{2RT}{\Omega_j^\mathrm{cat}}}
\quad(\Omega_j^\mathrm{cat}>2RT).
\label{eq:lco-spinodal}
\end{equation}
$\Omega_j^\mathrm{cat}\le2RT$ 이면 $u_j^\mathrm{cat}$ 가 실수가 아니므로 해당 전이의 spinodal gap 은
없다. 이 문턱식은 흑연 식~\eqref{eq:spinodal} 의 LCO 대입형이다.

\textbf{(c) 중간식 — LCO 전위 곡선에 spinodal 대입.}
흑연 식~\eqref{eq:Veq} 에 LCO 입력을 넣으면
\begin{equation}
V_{\eq,j}^\mathrm{cat}(\xi)
=U_j^\mathrm{cat}
+\frac{RT}{F}\ln\frac{\xi}{1-\xi}
+\frac{\Omega_j^\mathrm{cat}}{F}(1-2\xi).
\label{eq:lco-Veq}
\end{equation}
두 spinodal 끝점에서
\[
\frac{\xi}{1-\xi}\bigg|_{\xi_{s,j}^{\pm}}
=\frac{1\pm u_j^\mathrm{cat}}{1\mp u_j^\mathrm{cat}},
\qquad
(1-2\xi)\big|_{\xi_{s,j}^{\pm}}
=\mp u_j^\mathrm{cat}.
\]
그러므로 극대에서 극소를 빼면 상수 중심 $U_j^\mathrm{cat}$ 는 상쇄되고
\[
\Delta U_j^{\hys,\mathrm{cat}}
=V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^-)
-V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^+)
=\frac{2}{F}
\left[
\Omega_j^\mathrm{cat}u_j^\mathrm{cat}
-2RT\,\mathrm{artanh}\,u_j^\mathrm{cat}
\right].
\]

\textbf{(d) 박스 — LCO 전이별 gap 과 방향별 분기 중심.}
\begin{equation}
\boxed{\;
\Delta U_j^{\hys,\mathrm{cat}}(T)=
\begin{cases}
\dfrac{2}{F}
\left[
\Omega_j^\mathrm{cat}u_j^\mathrm{cat}
-2RT\,\mathrm{artanh}\,u_j^\mathrm{cat}
\right],
& \Omega_j^\mathrm{cat}>2RT,\\[4pt]
0, & \Omega_j^\mathrm{cat}\le2RT,
\end{cases}
\quad
u_j^\mathrm{cat}=\sqrt{1-\dfrac{2RT}{\Omega_j^\mathrm{cat}}}\;}
\label{eq:lco-dUhys}
\end{equation}
\begin{equation}
\boxed{\;
U_j^{\,d,\mathrm{cat}}
=U_j^\mathrm{cat}
+\tfrac12\sigma_d h_{\eta,j}\gamma_j
\Delta U_j^{\hys,\mathrm{cat}}(T)\;}
\label{eq:lco-Ubranch}
\end{equation}
방전($\sigma_d=+1$)은 분기 중심을 위로, 충전($\sigma_d=-1$)은 아래로 옮긴다.
이는 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 대입형이다.

\textbf{(T2$\cdot$T3) order--disorder.}
$x\approx0.5$ 부근의 T2($\sim$4.05 V)$\cdot$T3($\sim$4.17--4.20 V) 전이는
monoclinic 초격자와 관련된 order--disorder 사례이므로 위 박스에 $j=2,3$ 을 넣는다.
정렬의 charge-order 엔트로피 변화($\approx0.47$ J/(mol\,K)@$x=\tfrac12$,
$\approx1.49$ J/(mol\,K)@$x=\tfrac23$ [tier A, Motohashi~\cite{motohashi2009}])는
표~\ref{tab:lco-staging} 와 식~\eqref{eq:lco-decomp} 의
$\Delta S_j^\mathrm{config}$ 슬롯에 들어가는 엔트로피 성분이지,
spinodal 문턱을 정하는 상호작용 에너지 $\Omega_j^\mathrm{cat}$ 가 아니다.
따라서 이 수치를 $\Omega_j^\mathrm{cat}$ 로 환산하지 않는다.

\textbf{(T1) MIT 2상역.}
T1($\sim$3.90 V, $x\approx0.94$--$0.75$)의 구조적 2상 공존도 같은 박스에 $j=1$ 을 넣어
$\Delta U_1^{\hys,\mathrm{cat}}$ 와 $U_1^{\,d,\mathrm{cat}}$ 로 적는다. MIT 고유의 전자 자유도는
히스 gap 에 새 항으로 섞지 않는다. 그 항은
$\Delta S_{\rxn,1}^\mathrm{cat}
=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^\mathrm{mol}(x,T)$
를 통해 식~\eqref{eq:lco-dUdT} 의 온도 이동 슬롯에 들어간다. 곧 이 절의 구조적 gap 슬롯은
$\Omega_1^\mathrm{cat}$, 전자 엔트로피 슬롯은 $\Delta S_{e,1}^\mathrm{mol}$ 이다.

\textbf{도핑 보정(우리 시료).}
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox$\cdot$전자항을 보존하되
order--disorder$\cdot$MIT 상전이를 억제한다. 정규용액 틀에서는 pure-LCO 초기값
$\Omega_j^\mathrm{cat,pure}$ 가 도핑 피팅값 $\Omega_j^\mathrm{cat,dop}$ 로 낮아지는 입력 변화로 둔다.
문턱으로 접근하면
\begin{equation}
\Omega_j^\mathrm{cat,dop}\to2RT^+
\Longrightarrow
u_j^\mathrm{cat,dop}\to0,\qquad
\Delta U_j^{\hys,\mathrm{cat,dop}}
\to\frac{8RT}{3F}\big(u_j^\mathrm{cat,dop}\big)^3\to0.
\label{eq:lco-dope}
\end{equation}
$\Omega_j^\mathrm{cat,dop}\le2RT$ 로 피팅되는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다.
중심 전위의 미세 shift 는 별도 입력 $U_j^\mathrm{cat}$ 의 피팅값 이동으로 들어가며,
$\Omega_j^\mathrm{cat}$ 하나가 gap, smear, 중심 이동을 동시에 만든다고 쓰지 않는다.
```

### 원문 대비

- 현재 L697--699의 “같은 정규용액 틀” 결론을 `g_j^\mathrm{cat}` 출발식, 곡률, spinodal, 전위 곡선, gap, 분기 중심으로 전개했다.
- 현재 L701--706의 T2/T3 설명은 보존하되, `0.47/1.49` J/(mol K)가 엔트로피 성분이지 `\Omega_j^\mathrm{cat}`가 아니라는 혼동 방지를 명시했다.
- 현재 L708--713의 MIT 설명은 구조적 gap 슬롯(`\Omega_1^\mathrm{cat}`)과 전자 엔트로피 슬롯(`\Delta S_{e,1}^\mathrm{mol}`)을 분리하는 방식으로 재작성했다.
- 현재 L715--719의 도핑 설명은 `\Omega_j^\mathrm{cat,dop}\to2RT^+` 극한과 `gap -> 0` 식으로 닫았다. 중심 shift는 `U_j^\mathrm{cat}` 피팅값 이동으로 분리했다.
- `\Omega_j`의 실제 수치는 새로 만들지 않았다. pure-LCO 초기값과 도핑 피팅값의 관계만 기호로 유지했다.

### 논리 감사

- 부호: `V_{\eq,j}^\mathrm{cat}(\xi_s^-)-V_{\eq,j}^\mathrm{cat}(\xi_s^+)`에서 log 항은 `-4RT artanh(u)/F`, 상호작용 항은 `+2\Omega u/F`가 되어 기존 `eq:dUhys`와 같은 부호다. `\Delta U_j^\hys\ge0` 조건은 `\Omega_j>2RT` 영역에서 기존 원문과 일치한다.
- 차원: `\Omega_j`, `RT`는 J/mol, 대괄호 전체도 J/mol, `F`로 나누면 V. `U_j^{d}`는 `U_j`와 gap 전압의 합이라 V.
- 극한: `\Omega_j^\mathrm{cat}\to2RT^+`이면 `u_j^\mathrm{cat}\to0`이고 `\mathrm{artanh}u=u+u^3/3+\cdots`로 `\Delta U\to(8RT/3F)u^3\to0`; `\Omega_j^\mathrm{cat}\le2RT`에서는 gap을 0으로 둔다.
- 결과식 불변: 흑연 `eq:gxi`, `eq:gpp`, `eq:spinodal`, `eq:Veq`, `eq:dUhys`, `eq:Ubranch`의 LCO 대입형만 작성했다. 새 broadening 모델, PSD, `rho(U_app)`류 신규 개념은 넣지 않았다.
- 미확인/불가침: `sec:lco-map`, `sec:lco-Se`, `sec:lco-gate` 본문은 편집하지 않았다. 전자항은 기존 `eq:lco-decomp`/`eq:lco-dUdT` 참조 경로로만 언급했다.

---

## 3줄 요약

1. `sec:lco-center`는 `\Delta G=-FU`와 `\Delta G=\Delta H-T\Delta S`에서 `U_j^\mathrm{cat}=(-\Delta H^\mathrm{cat}+T\Delta S^\mathrm{cat})/F`, `\partial_T U_j^\mathrm{cat}=\Delta S^\mathrm{cat}/F`로 닫고 `eq:lco-dUdT` 라벨을 유지하는 사슬로 재작성했다.
2. `sec:lco-hys`는 흑연 N3의 정규용액 `g`, `g''`, spinodal, `V_eq`, `\Delta U^\hys`, `U^d` 결과를 LCO 전이별 `U_j^\mathrm{cat}`, `\Omega_j^\mathrm{cat}`로 대입하는 사슬로 재작성했다.
3. 자체 감사 결과 부호·차원·문턱 극한은 기존 흑연식과 정합하며, 수치·물리·`\Omega_j` 기호는 보존했고 `sec:lco-map`/`Se`/`gate` 및 tex/코드는 수정하지 않았다.
