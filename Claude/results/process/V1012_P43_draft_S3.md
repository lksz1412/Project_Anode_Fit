# V1.0.12 Phase 4.3 — 작성 드래프트 S3

> 역할: Phase 4.3 작성 드래프트 **S3**(N=10 경쟁: 3 Sonnet+3 Opus+3 Codex+1 Fable, 무통신 독립). 드래프트만(.md
> supplement) — `.tex`/코드 미수정(편입은 Fable master). 물리·결과식·부호·수치 불변, 전개 형식만 줄글→수식. 방법 =
> 절별 루핑 선형(절마다 [정독→수식 사슬 작성(재유도 검증)→자기검수→앞 절 정합]).
>
> 대상: `docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`(1965줄, head→tail 전문 정독), `docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex`
> (755줄, head→tail 전문 정독), `Anode_Fit_v1.0.12.py`(교차확인, `func_w`/`_width` L75-76·295-307).
> 출발점 = `results/process/V1011_P11_map_v10.md`(center·hys, 계승·독립 재검증), `results/process/V1010_LCO_STYLE_REPORT.md`
> §1(필요한 수식 사슬), `results/process/FABLE_REAUDIT_C4_note.md`(H-2 근거).

**실측 확인(전제 검증)**: v1.0.12 tex 의 sec:lco-center(L476-519)·sec:lco-hys(L696-720)·sec:lco-peak(L1220-1232)는
V1011 P11 map 이 제안한 (a)(b)(c)(d) 사슬이 **아직 편입되지 않은 원 줄글 상태**다(제안 문안과 실측 tex 를 직접 대조 —
글자 그대로 다름). sec:lco-decomp(L1715-1754)는 이미 박스(`eq:lco-decomp`)가 있으나 가산성 논거가 줄글이다. 전자항
plug-in(L1784-1788)·MSMR(L1767-1792)도 줄글/서술 위주다. 따라서 아래 6절 전부가 실질적 수식화 대상이다(추정 아님 —
줄 단위 대조 결과).

---

## 갈래 1 — LCO 6절 수식화

### 1. `sec:lco-center` (L476-519, 편입 대상 L477-494)

**정독**: 대상 절(L476-519) + 흑연 대응 절 `sec:center`(L411-467, 특히 `eq:eqcond` L440-443·`eq:Uj` L458-461·미분
논평 L463-467) 전문 재확인.

**편입 지시**: L476 헤더·L496-516 verifybox·L518-519 히스 다리 브리지는 **그대로 둔다**. 아래 블록이 **L477-494**
(현재 줄글 두 문단 + `eq:lco-dUdT` 정의)를 교체하며, `\label{eq:lco-dUdT}`를 **그대로 승계**한다(하류 `\eqref`
6곳: L493·498·505·1229·1790·1877 — 전수 grep 확인, 끊기면 안 됨).

```latex
\textbf{(a) 출발 — 전극-중립 골격의 세 진입.}
\S\ref{sec:center} 의 평형 중심 유도를 되짚으면 어느 단계에도 ``흑연''이라는 물질 고유 항이 들어가지 않는다:
(i) 실험조건 매핑 식~\eqref{eq:n0map} 의 방향 부호$\cdot$전류 환산은 삽입형 전극이면 종류를 가리지 않고,
(ii) 전기화학 평형 조건 식~\eqref{eq:eqcond}($\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U),\ \Delta G_j=-sFU_j$)는
삽입 반쪽반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 의 전기화학 평형(식~\eqref{eq:eqbalance})에서
나오며 host 의 화학 정체는 상수 $\mu^0$ 값으로만 흡수되고, (iii) 비배치 몫 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$
는 반응 종에 무관한 열역학 항등식(식~\eqref{eq:gibbsdef} $G\equiv H-TS$ 에서)이다. LCO 로 넘어갈 때 이 세 자리에
들어가는 것은 전이 집합과 입력값의 치환뿐이다: $j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}$,
$(\Delta H_{\rxn,j},\Delta S_{\rxn,j})\mapsto(\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat})$.

\textbf{(b) 연산 — 평형 조건에 반응 자유에너지 대입.}
전이 $j$ 의 비배치 반응 자유에너지 $\Delta G_j^\mathrm{cat}=\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}$
를 식~\eqref{eq:eqcond} 의 $\Delta G_j=-sFU_j$($s=+1$)에 넣으면
\[
\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}=-F\,U_j^\mathrm{cat}(T),
\]
곧 흑연 식~\eqref{eq:Ujmid} 과 글자 그대로 같은 식에 상첨자 $\mathrm{cat}$ 만 붙는다 — (a)의 세 자리 어디에도
host 항이 없었으므로 이 대입은 항등적으로 성립한다(치환일 뿐 새 유도가 아님).

\textbf{(c) 중간식 — 이항과 온도 미분의 이중 경로 교차검증.}
(b)를 $U_j^\mathrm{cat}$ 로 이항하면
\[
U_j^\mathrm{cat}(T)=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\Delta S_{\rxn,j}^\mathrm{cat}}{F}
\]
로 흑연 식~\eqref{eq:Uj} 와 같은 함수형이다. 그 온도 계수를 두 독립 경로로 검산한다.
\emph{경로 1(직접 미분)}: $\Delta H_{\rxn,j}^\mathrm{cat}$ 는 $T$ 무관 상수이므로 위 식을 그대로 $T$ 로 미분하면
$\partial U_j^\mathrm{cat}/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$.
\emph{경로 2(Gibbs 항등식 경유)}: 등압 Gibbs 항등식 $\partial\Delta G_j/\partial T|_P=-\Delta S_{\rxn,j}^\mathrm{cat}$
(식~\eqref{eq:gibbsdef} 에서)와, 식~\eqref{eq:eqcond} 의 $\Delta G_j=-FU_j^\mathrm{cat}$ 를 $T$ 로 미분한
$\partial\Delta G_j/\partial T=-F\,\partial U_j^\mathrm{cat}/\partial T$ 를 등치하면
\[
-F\,\frac{\partial U_j^\mathrm{cat}}{\partial T}=-\Delta S_{\rxn,j}^\mathrm{cat}
\ \Longrightarrow\
\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
두 경로가 같은 결과에 닿고, 어디에도 host 구분 항이 없다 — 이것이 ``전극 불문''의 수식적 의미다.

\textbf{(d) 박스 — LCO 양극 중심과 온도 계수.}
\begin{equation}
\boxed{\;
U_j^\mathrm{cat}(T)=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\Delta S_{\rxn,j}^\mathrm{cat}}{F},
\qquad
\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}
\quad(j\in\mathcal J_\mathrm{LCO})\;}
\label{eq:lco-dUdT}
\end{equation}
관계식은 흑연 식~\eqref{eq:Uj} 와 부호까지 1:1 이고 값만 바뀐다 — 양극의 높은 중심($\sim$3.9--4.2 V)은 분자
$-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양인 데서 오며(흑연의 $-\Delta H_{\rxn,j}$ 가 양이라 중심을 올리는 것과
같은 부호 메커니즘, \S\ref{sec:center} 미분 논평), $\Delta S_{\rxn,j}^\mathrm{cat}$ 는 \S\ref{sec:lco-decomp}
(식~\eqref{eq:lco-decomp})에서 config$\cdot$vib$\cdot$전자 세 성분으로 분해된다. 아래 verifybox 는 이 관계의
부호$\cdot$크기 sanity 를 대표 스케일로 검산한다.
```

**자기검수**:
- *부호*: $\Delta H_{\rxn,j}^\mathrm{cat}<0$(발열) $\Rightarrow-\Delta H^\mathrm{cat}>0$ 이 중심을 올림 — 흑연
  `eq:Uj` 미분 논평(L462-463)과 부호 메커니즘 동일, 값만 다름. 일치.
- *차원*: $[\Delta H]=$J/mol, $[\Delta S]=$J/(mol·K), $[F]=$C/mol $\Rightarrow[U]=$J/C=V. 일치.
- *극한/교차검증*: 경로 1(직접 미분)·경로 2(Gibbs 항등식 경유)가 같은 $\partial U_j^\mathrm{cat}/\partial T=\Delta
  S_{\rxn,j}^\mathrm{cat}/F$ 에 수렴 — 독립 재유도로 confirmed(둘 다 host 항 없음, "전극 불문" 주장의 수식적 근거).
- *이중계산*: 이 절은 $\Delta S_{\rxn,j}^\mathrm{cat}$ 를 한 덩이로만 다루고 내부 분해는 `sec:lco-decomp` 로 미룬다
  (앞으로 인용만, 여기서 재전개 안 함 — 이중계산 없음).
- *라벨*: `eq:lco-dUdT` 재사용 확정(신설 라벨 없음, 이 절에서는).

**원 줄글 대비**: 원문 L477-481 은 "유도에 전극 가정이 없다"를 결론으로 먼저 던지고 근거를 사후 설명하는 줄글이었다
(단정 → 이유, V1010 STYLE_REPORT "단정 비약" 지적과 일치하는 패턴). 위 (a)-(d) 는 같은 결론을 **eq:n0map·eq:eqbalance·
eq:eqcond·eq:gibbsdef 를 순서대로 밟아 도출**하고, 온도 미분은 원문의 "Gibbs 항등식과 잇는 것과 같다"는 괄호 한 줄
(L463-464 원 흑연 절의 논평을 LCO 절이 그대로 재인용)을 (c)에서 **두 독립 경로의 명시적 교차검증**으로 펼쳤다. 물리·
결과식·부호·수치는 원문과 완전히 동일(바뀐 것은 서술 밀도뿐).

---

### 2. `sec:lco-hys` (L696-720, 편입 대상 L697-719)

**정독**: 대상 절(L696-720) + 흑연 대응 절 `sec:hys`(L521-694, 특히 `eq:mu` L540·`eq:gxi` L546·`eq:gpp` L553·
`eq:spinodal` L560·`eq:Veq` L601·`eq:hyssub` L612·`eq:hysdiff` L622·`eq:dUhys` L630·`eq:Ubranch` L648) 재확인.

**편입 지시**: L696 헤더·L721 `sec:width` 경계는 그대로 둔다. 아래 블록이 L697-719 를 교체한다. 흑연 결과식(`eq:mu`
·`eq:gxi`·`eq:gpp`·`eq:spinodal`·`eq:Veq`·`eq:hysdiff`·`eq:dUhys`·`eq:Ubranch`)은 **재유도 없이 대입만** — 아래는
그 대입을 실제로 전개해 보인 것(V1011 map §2 골격을 독립 재검증 후 계승, 라벨 10종 전수 grep 재확인 — 충돌 0).

```latex
\textbf{(a) 출발 — LCO 세 전이를 같은 정규용액 자유에너지에.}
\S\ref{sec:hys} 의 격자기체$\cdot$정규용액 자유에너지(식~\eqref{eq:gxi})는 ``동등한 자리에 리튬이 차고 빈다''는
가정 하나만 쓰며, 이는 LCO $\mathrm{Li}_x\mathrm{CoO_2}$ 의 팔면체 리튬 자리에도 문자 그대로 성립한다. LCO 전이
집합
\begin{equation}
\mathcal J_\mathrm{LCO}=\{1:\mathrm{MIT},\ 2:\mathrm{OD}_a,\ 3:\mathrm{OD}_b\}
\label{eq:lco-J}
\end{equation}
의 각 전이 $j$ 에 진행률 $\xi_j$ 를 달면
\begin{equation}
g_j^\mathrm{cat}(\xi_j)=g_{0,j}^\mathrm{cat}
+RT\{\xi_j\ln\xi_j+(1-\xi_j)\ln(1-\xi_j)\}+\Omega_j^\mathrm{cat}\,\xi_j(1-\xi_j),
\label{eq:lco-gxi}
\end{equation}
로 식~\eqref{eq:gxi} 와 글자 그대로 같은 형태다 — 바뀌는 것은 전이별 입력값 $U_j^\mathrm{cat},\Omega_j^\mathrm{cat},
\gamma_j,h_{\eta,j}$ 뿐이다.

\textbf{(b) 연산 — 곡률과 spinodal 문턱.}
식~\eqref{eq:lco-gxi} 를 $\xi_j$ 로 두 번 미분하면(로그 몫 2계 미분 $RT/[\xi_j(1-\xi_j)]$, 상호작용 몫 2계 미분
$-2\Omega_j^\mathrm{cat}$ — 식~\eqref{eq:gpp} 와 동일 계산) 흑연 식~\eqref{eq:gpp} 에 전이별 $\Omega_j^\mathrm{cat}$
만 든 형태가 나온다:
\begin{equation}
\frac{\partial^2 g_j^\mathrm{cat}}{\partial\xi_j^2}=\frac{RT}{\xi_j(1-\xi_j)}-2\Omega_j^\mathrm{cat}.
\label{eq:lco-gpp}
\end{equation}
$g_j''=0$ 은 $\xi_j(1-\xi_j)=RT/(2\Omega_j^\mathrm{cat})$, 곧 $\xi_j^2-\xi_j+RT/(2\Omega_j^\mathrm{cat})=0$ 의
근의 공식으로
\begin{equation}
\xi_{s,j}^{\pm}=\tfrac12\big(1\pm u_j^\mathrm{cat}\big),\qquad
u_j^\mathrm{cat}=\sqrt{1-\frac{2RT}{\Omega_j^\mathrm{cat}}}\qquad(\Omega_j^\mathrm{cat}>2RT),
\label{eq:lco-spinodal}
\end{equation}
가 되어 흑연 식~\eqref{eq:spinodal} 과 동형이며, $\Omega_j^\mathrm{cat}\le2RT$ 면 $u_j^\mathrm{cat}$ 이 실수가
아니라 그 전이의 spinodal gap 은 없다(흑연 코드 분기 그대로).

\textbf{(c) 중간식 — LCO 전위 곡선에 spinodal 대입.}
LCO 전이 $j$ 의 평형 전위 곡선은 식~\eqref{eq:Veq}($s=+1$ 고정 규약, 표 L225 참조)에 $U_j^\mathrm{cat},
\Omega_j^\mathrm{cat}$ 를 넣어
\begin{equation}
V_{\eq,j}^\mathrm{cat}(\xi)=U_j^\mathrm{cat}
+\frac{RT}{F}\ln\frac{\xi}{1-\xi}+\frac{\Omega_j^\mathrm{cat}}{F}(1-2\xi),
\label{eq:lco-Veq}
\end{equation}
이고, 두 spinodal 끝점에서 식~\eqref{eq:hyssub} 와 같은 대입 $\dfrac{\xi}{1-\xi}\big|_{\xi_{s,j}^\pm}=\dfrac{1\pm
u_j^\mathrm{cat}}{1\mp u_j^\mathrm{cat}}$, $(1-2\xi)\big|_{\xi_{s,j}^\pm}=\mp u_j^\mathrm{cat}$ 를 쓰면(상수 중심
$U_j^\mathrm{cat}$ 는 차에서 상쇄, 로그 두 개가 부호 반대 같은 크기라 $-4\,\mathrm{artanh}\,u$ — 식~\eqref{eq:hysdiff}
와 같은 대수)
\[
\Delta U_{j}^{\hys,\mathrm{cat}}=V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^-)-V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^+)
=\frac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\operatorname{artanh}u_j^\mathrm{cat}\big].
\]

\textbf{(d) 박스 — LCO 전이별 gap 과 분기 중심.}
\begin{equation}
\boxed{\;
\Delta U_j^{\hys,\mathrm{cat}}(T)=
\begin{cases}
\dfrac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\operatorname{artanh}u_j^\mathrm{cat}\big],
& \Omega_j^\mathrm{cat}>2RT,\\[4pt]
0, & \Omega_j^\mathrm{cat}\le2RT,
\end{cases}
\quad u_j^\mathrm{cat}=\sqrt{1-\dfrac{2RT}{\Omega_j^\mathrm{cat}}}\;}
\label{eq:lco-dUhys}
\end{equation}
\begin{equation}
\boxed{\;
U_j^{\,d,\mathrm{cat}}=U_j^\mathrm{cat}
+\tfrac12\sigma_d h_{\eta,j}\gamma_j\,\Delta U_j^{\hys,\mathrm{cat}}(T)\;}
\label{eq:lco-Ubranch}
\end{equation}
흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 대입형이다 — ``같은 틀''은 $\Omega_j\mapsto\Omega_j^\mathrm{cat}$,
$U_j\mapsto U_j^\mathrm{cat}$, $j\in\mathcal J_\mathrm{LCO}$ 를 실제로 넣는다는 뜻이다.

\textbf{(T2$\cdot$T3) order--disorder — 대입.}
$j=2,3$ 을 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 넣으면
\[
u_j^\mathrm{cat}=\sqrt{1-\tfrac{2RT}{\Omega_j^\mathrm{cat}}},\quad
\Delta U_j^{\hys,\mathrm{cat}}=\tfrac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}
-2RT\operatorname{artanh}u_j^\mathrm{cat}\big],\quad
U_j^{\,d,\mathrm{cat}}=U_j^\mathrm{cat}+\tfrac12\sigma_d h_{\eta,j}\gamma_j\Delta U_j^{\hys,\mathrm{cat}}
\quad(j=2,3),
\]
로 T2($\sim$4.05 V, hex$\to$monoclinic)$\cdot$T3($\sim$4.17--4.20 V, monoclinic$\to$hex)가 열린다. 정렬의
charge-order 엔트로피 변화($\approx0.47$ J/(mol\,K)@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$
[tier A, Motohashi\cite{motohashi2009}])는 이 $\Omega_j^\mathrm{cat}$ 가 \emph{아니라} 표~\ref{tab:lco-staging}
·식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 슬롯에 들어간다 — 두 양은 척도가 다르므로(엔트로피
[J/(mol\,K)] vs 상호작용 에너지 [J/mol]) ``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 다리를 놓지 않는다.

\textbf{(T1) MIT 2상역 — 대입과 슬롯 분리.}
$j=1$ 을 넣으면
\[
u_1^\mathrm{cat}=\sqrt{1-\tfrac{2RT}{\Omega_1^\mathrm{cat}}},\quad
\Delta U_1^{\hys,\mathrm{cat}}=\tfrac{2}{F}\big[\Omega_1^\mathrm{cat}u_1^\mathrm{cat}
-2RT\operatorname{artanh}u_1^\mathrm{cat}\big],\quad
U_1^{\,d,\mathrm{cat}}=U_1^\mathrm{cat}+\tfrac12\sigma_d h_{\eta,1}\gamma_1\Delta U_1^{\hys,\mathrm{cat}}.
\]
MIT 고유의 전자 자유도는 이 히스 gap 에 새 항으로 섞이지 않는다 — 그 항은 이미 $\Delta S_{\rxn,1}^\mathrm{cat}=
\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}+\Delta S_{e,1}^\mathrm{mol}(x,T)$(식~\eqref{eq:lco-decomp})를
통해 $U_1^\mathrm{cat}(T)$ 의 온도 이동(식~\eqref{eq:lco-dUdT})에 들어간다. 두 몫이 다른 슬롯에 산다는 것을
식으로 못박으면
\begin{equation}
\boxed{\;
\underbrace{\Delta U_1^{\hys,\mathrm{cat}}\ (\text{구조적 2상역})\ \Leftarrow\ \Omega_1^\mathrm{cat}}_{\text{정규용액 히스 gap(이 절)}}
\quad\Big\|\quad
\underbrace{\partial U_1^\mathrm{cat}/\partial T\ \Leftarrow\ \Delta S_{e,1}^\mathrm{mol}(x,T)}_{\text{전자 엔트로피(\S\ref{sec:lco-electronic})}}\;}
\label{eq:lco-mit}
\end{equation}
이 분리가 config 2상역과 전자 엔트로피의 이중계산을 막는 경계다.

\textbf{도핑 보정 — $\Omega\to2RT^+$ 극한.}
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 정규용액 틀에서 $\Omega_j^\mathrm{cat,pure}\to\Omega_j^\mathrm{cat,dop}$(더
작은 값)로의 입력 변화다. 식~\eqref{eq:lco-dUhys} 의 문턱 극한을 흑연 식~\eqref{eq:dUhys} 의 Taylor 전개
($\operatorname{artanh}u=u+u^3/3+\cdots$)와 같은 방식으로 취하면 — $\Omega\to2RT^+$ 에서 $u\to0$ 이고
$\Omega-2RT\approx2RTu^2$(스피노달 정의 역전개)이므로 대괄호 $[\Omega u-2RT\operatorname{artanh}u]\approx
[(\Omega-2RT)u-\tfrac23RTu^3]\approx2RTu^3-\tfrac23RTu^3=\tfrac43RTu^3$ —
\begin{equation}
\Omega_j^\mathrm{cat,dop}\to2RT^+\ \Longrightarrow\
u_j^\mathrm{cat,dop}\to0,\quad
\Delta U_j^{\hys,\mathrm{cat,dop}}\to\frac{8RT}{3F}\big(u_j^\mathrm{cat,dop}\big)^3\to0,
\label{eq:lco-dope}
\end{equation}
이고, $\Omega_j^\mathrm{cat,dop}\le2RT$ 로 피팅되는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다 — 도핑에 따른
히스 축소$\cdot$peak smear 의 수식 표현이다.
```

**자기검수**:
- *부호*: $\Delta U_j^{\hys,\mathrm{cat}}\ge0$(극대$-$극소, $u\ge0$) — 흑연 S4 검산과 동일 부호 논리. 방전
  $+\tfrac12\sigma_d(\cdots)$/충전 $-\tfrac12\sigma_d(\cdots)$ 라 $U^{\dis}>U^{\chg}$, 일치.
- *차원*: $\Omega$[J/mol], $RT$[J/mol], $F$[C/mol] $\Rightarrow[\Delta U^\hys]=$V. 일치.
- *극한*: $\Omega_j^\mathrm{cat}\to2RT^+$ 에서 $u\to0$, $\Delta U^{\hys}\to(8RT/3F)u^3\to0$ — 독립 재전개로
  확인(위 도핑 문단에 전개 과정 명시, V1011 map 은 결과만 인용했던 지점을 재유도로 채움 — 개선점).
- *이중계산*: `eq:lco-mit` 박스가 구조적 2상역($\Omega_1^\mathrm{cat}$ 경유)과 전자 엔트로피($\Delta S_{e,1}$
  경유)를 슬롯 분리 — MIT 자유도 이중계산 없음.
- *혼동 가드*: config $\Delta S$(0.47/1.49, tier A)와 $\Omega_j^\mathrm{cat}$(상호작용 에너지)를 척도가 다른 양으로
  명시 분리 — 수치 날조 없음(둘 다 $\Omega_j$ 기호 유지, 값 대입 안 함).
- *라벨*: `eq:lco-J`·`eq:lco-gxi`·`eq:lco-gpp`·`eq:lco-spinodal`·`eq:lco-Veq`·`eq:lco-dUhys`·`eq:lco-Ubranch`·
  `eq:lco-mit`·`eq:lco-dope` 9종 신설 — 전수 grep 재확인(`No matches found`), `sec:lco-center` 의 `eq:lco-dUdT`
  와도 충돌 없음.

**앞 절 정합**: `eq:lco-dUdT`(§1 (d) 박스)의 $\partial U_1^\mathrm{cat}/\partial T$ 가 `eq:lco-mit`(본 절 (d)) 의
전자 슬롯과 정확히 같은 기호로 이어진다(§1 이 넘긴 "$\Delta S_{\rxn,j}^\mathrm{cat}$ 는 §lco-decomp 에서 분해"를
본 절이 MIT 슬롯 분리로 한 번 더 좁힘). 히스 중심 $U_j^{\,d,\mathrm{cat}}$ 가 다음 §3(peak)의 위치 인자로 그대로
들어간다.

**원 줄글 대비**: 원문 L697-719 는 "같은 정규용액 틀로... 그대로 적용된다"를 T2·T3/T1/도핑 세 문단에서 **각각
독립적으로 재서술**했으나 중간식(spinodal 대입·gap 유도)이 생략돼 있었다(V1010 STYLE_REPORT "HIGH×3" 판정과
일치). 위 (a)-(d) + 세 대입 문단은 흑연 §hys 의 8개 결과식을 실제로 LCO 파라미터로 밀어 넣어 매 단계를 보였고,
도핑 극한은 재전개로 새로 채웠다. 물리·부호·수치·$\Omega_j$ 기호는 원문과 동일.

---

### 3. `sec:lco-peak` (L1220-1232, 편입 대상 L1221-1232)

**정독**: 대상 절(L1220-1232) + 흑연 대응 절 `sec:eqpeak`(L1184-1218, 특히 `eq:belliden` L1198·`eq:eqpeak`
L1206-1209) 재확인. 이 절은 V1011 map 이 다루지 않은 신규 작성 대상(V1010 STYLE_REPORT "Major(★최약)" 판정).
**손대지 않음**: 다음 소절 `sec:broadening`(L1234-1412, N6 노드 본체 일부)은 편입 대상 밖 — 그대로 둔다.

**편입 지시**: L1220 헤더는 그대로 두고, 아래 블록이 L1221-1232 를 교체한다.

```latex
\textbf{(a) 출발 — 전극 불문의 평형 peak 식.}
식~\eqref{eq:eqpeak} $\big(\dd Q/\dd V\big)^\eq_j=Q_j\,\xi_{\eq,j}(1-\xi_{\eq,j})/w_j$ 는 전하 보존식의 직접
미분(\S\ref{sec:eqpeak} (a)(b)(c))에서 나왔고, 그 유도 어디에도 host 항이 없다 — \S\ref{sec:lco-center} (a)와
같은 논거다. 따라서 LCO 세 전이 $j\in\{\mathrm{T1,T2,T3}\}$ 에 그대로 적용된다.

\textbf{(b) 연산 — LCO 파라미터 대입(위치$\cdot$폭의 지위 확인).}
전이별로 중심 $U_j^{\,d,\mathrm{cat}}$(식~\eqref{eq:lco-Ubranch})$\cdot$용량 가중 $Q_j^\mathrm{cat}$$\cdot$폭
$w_j^\mathrm{cat}=n_j^\mathrm{cat}RT/F$(식~\eqref{eq:wbase} 형태 그대로, 값만 LCO)를 대입하면
\[
\Big(\frac{\dd Q}{\dd V}\Big)^{\eq,\mathrm{cat}}_j
=Q_j^\mathrm{cat}\,\frac{\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j^\mathrm{cat}}
\qquad(j=\mathrm{T1,T2,T3}).
\]
표~\ref{tab:lco-staging} 의 세 전이는 모두 $\Omega_j^\mathrm{cat}>2RT$(\S\ref{sec:lco-hys}) — 곧 세 폭
$w_j^\mathrm{cat}$ 은 \S\ref{sec:width} 이중지위의 \emph{두-상} 측이다: 식~\eqref{eq:wbase} 의 평형 예측이
아니라 \S\ref{sec:broadening} broadening 이 정하는 현상학적 자유 피팅 폭이다(흑연 두-상 두 전이와 같은 지위 —
단, \S\ref{sec:broadening}(b)-③(iii-a)(iii-b)의 흑연-특정 turbostratic 앙상블 근거는 옮기지 않고, LCO 는 일반
$\eta$ 산포로만 다룬다).

\textbf{(c) 중간식 — 세 봉우리의 위치$\cdot$순높이$\cdot$면적.}
식~\eqref{eq:eqpeak} 의 논평(위치 $=$ 중심, 순높이 $=Q_j/(4w_j)$[$\xi=\tfrac12$ 에서 $\xi(1-\xi)=\tfrac14$],
면적 $=Q_j$)을 그대로 세 전이에 대입하면
\[
\text{위치}_j=U_j^{\,d,\mathrm{cat}},\qquad
\text{순높이}_j=\frac{Q_j^\mathrm{cat}}{4w_j^\mathrm{cat}},\qquad
\text{면적}_j=Q_j^\mathrm{cat}
\qquad(j=\mathrm{T1,T2,T3}),
\]
이고 합산은 흑연과 \emph{같은} 식~\eqref{eq:sum} 위에 얹힌다(배경$\cdot$흑연 전이와 전압 구간이 겹치지 않으므로
—흑연 $\sim$0.085--0.21 V vs LCO $\sim$3.90--4.20 V— 선형 합에 교차항 없음).

\textbf{(d) 박스 — LCO 세 봉우리 합.}
\begin{equation}
\boxed{\;
\Big(\frac{\dd Q}{\dd V}\Big)^{\mathrm{cat}}(V)=\sum_{j\in\{\mathrm{T1,T2,T3}\}}
Q_j^\mathrm{cat}\,\frac{\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j^\mathrm{cat}},
\qquad
\begin{aligned}
&\text{T1: 위치}\approx3.90\text{ V (MIT)},\\
&\text{T2: 위치}\approx4.05\text{ V},\\
&\text{T3: 위치}\approx4.17\text{--}4.20\text{ V}
\end{aligned}\;}
\label{eq:lco-peak}
\end{equation}
T2$\cdot$T3 의 큰 $\Omega^\mathrm{cat}$(\S\ref{sec:lco-hys})가 spinodal gap 을 키워 두 봉우리를 흑연 두-상 전이보다
날카로운 한 쌍으로 만든다. T1 은 \S\ref{sec:lco-electronic} 의 전자항이 $\Delta S_{\rxn,1}^\mathrm{cat}$(식~
\eqref{eq:lco-decomp})을 통해 $U_1^\mathrm{cat}(T)$ 의 온도 이동에 기여하므로(식~\eqref{eq:lco-dUdT}), 다온도
$\dd Q/\dd V$ 에서 T1 봉우리의 \emph{이동률} $\partial U_1^\mathrm{cat}/\partial T$ 가 $T$ 에 선형으로 커지는
것이 관측 신호다($\Delta S_{e,1}\propto T$, \S\ref{sec:lco-Se} — 위치 자체가 아니라 이동률이 $T$-선형, 위치
이동은 식~\eqref{eq:U1T2} 대로 $\propto T^2$). 도핑은 \S\ref{sec:lco-hys} 대로 봉우리를 smear$\cdot$shift 시킨다.
```

**자기검수**:
- *부호*: $\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})\ge0$ 이라 peak 는 방향 불변 양수 — 흑연 S3 검산과
  동일 대수(전개 재확인, 새 물리 없음).
- *차원*: $Q_j$[C], $w_j$[V] $\Rightarrow$ peak 항 [C/V]$=\dd Q/\dd V$. 일치.
- *극한*: $\xi=\tfrac12$(중심)에서 $\xi(1-\xi)=\tfrac14$ 최대 — 순높이 공식의 근거, 흑연과 동일 극한.
- *이중계산*: 배경$\cdot$흑연 전이와 LCO 세 전이의 전압 구간이 분리돼(하프셀 범위, \S\ref{sec:lco-map}) 선형합
  `eq:sum` 에 교차항 없음 — 명시 확인.
- *라벨*: `eq:lco-peak` 1종 신설, 전수 grep 재확인(충돌 0).

**앞 절 정합**: 위치 인자 $U_j^{\,d,\mathrm{cat}}$ 는 §2 (d) `eq:lco-Ubranch` 를 그대로 받는다(새 기호 도입 없음).
폭의 두-상 지위 판정은 §2 에서 확정한 $\Omega_j^\mathrm{cat}>2RT$(표~\ref{tab:lco-staging} 전 전이)를 그대로 이어
받아 §1 로 순환하지 않는다(§1 은 중심만, §2 는 히스만, §3 은 그 둘을 조합한 peak 만 — 층위 분리 유지).

**원 줄글 대비**: 원문 L1221-1232 는 "그대로 적용된다"는 한 문장 결론 뒤에 위치$\cdot$순높이$\cdot$면적을 병렬
나열했을 뿐 합산 박스식이 없었다(V1010 STYLE_REPORT "LCO 3전이 합산 peak 박스식 없음" 지적과 정확히 일치). 위
(a)-(d) 는 그 세 값을 명시 대입 후 `eq:lco-peak` 박스로 닫았다. 물리·부호·수치·위치값(3.90/4.05/4.17-4.20 V)은
원문과 동일.

---

### 4. `sec:lco-decomp` (L1715-1754, 편입 대상 L1732-1741)

**정독**: 대상 절 전문(L1715-1754, 기존 박스 `eq:lco-decomp` L1719-1724 포함) + Ch2 `\S ssec:config`(파생 B,
L294-310, config 이중계산 금지 논거) 재확인 — Ch2 는 "손대지 말 것"에 없으나 대조용으로만 참조(수정 없음).

**중요 — 라벨 보존**: `eq:lco-decomp`(L1723)는 이미 존재하며 **8곳**(`L505,508,1040,1060,1738,1750,1761,1785,1879`
— 전수 grep 확인)에서 하류 참조된다. **이 박스는 손대지 않는다** — 그대로 둔다. 편입 대상은 그 박스 \emph{앞},
"config" 항목의 "(가) 가산성" 문단(L1732-1741)이며, 이 문단만 아래 (a)-(c)로 교체하고 (d) 자리에는 **기존
`eq:lco-decomp` 박스를 그대로 유지**한다(새 박스 만들지 않음 — 신설 라벨은 (a)-(c) 유도용 2개만).

```latex
\textbf{(a) 출발 — 두 자유도의 분배함수 인수분해 가정.}
config(리튬 자리 \emph{점유 배열})와 $\Delta S_{e,j}$(전도 전자 \emph{밴드 점유})는 서로 다른 자유도다. 두
부분계가 독립이라는 근사 아래 전체 분배함수는
\begin{equation}
Z_\mathrm{tot}=Z_\mathrm{config}\cdot Z_\mathrm{elec}
\label{eq:lco-Zfact}
\end{equation}
로 인수분해된다(정확한 독립이 아니라 \emph{근사적} 직교 — MIT 부근에서 리튬 정렬과 전자 밴드채움이 다소 결합하나,
그 교차 항은 선도 차수에서 무시된다).

\textbf{(b) 연산 — 자유에너지$\cdot$엔트로피의 로그 가산성.}
자유에너지 $F_\mathrm{tot}=-RT\ln Z_\mathrm{tot}=-RT\ln Z_\mathrm{config}-RT\ln Z_\mathrm{elec}=F_\mathrm{config}
+F_\mathrm{elec}$(로그가 곱을 합으로 바꾸는 항등식, 식~\eqref{eq:lco-Zfact} 대입). 엔트로피는 $S=-\partial
F/\partial T$ 이므로
\[
S_\mathrm{tot}=-\frac{\partial F_\mathrm{tot}}{\partial T}
=-\frac{\partial F_\mathrm{config}}{\partial T}-\frac{\partial F_\mathrm{elec}}{\partial T}.
\]

\textbf{(c) 중간식 — 엔트로피 가산.}
\begin{equation}
S_\mathrm{tot}=S_\mathrm{config}+S_\mathrm{elec}
\qquad(\text{교차항 }0\text{, 선도 차수}).
\label{eq:lco-Sadd}
\end{equation}
config$+$elec 를 단순히 더하는 것 자체는 이 (근사) 직교성으로 정당화된다. 그러나 이것이 보장하는 것은 ``더해도
되는가''(가산성)뿐이다 — ``과대 계상 없는가''(무초과)는 별개 조건이며, 아래 (d) 박스의 슬롯 규칙(config 슬롯에
봉우리 \emph{중심값}만, elec 슬롯에 MIT 게이트 \emph{골}만)이 그 무초과를 보장한다: 두 슬롯이 같은 조성 의존을
두 번 세지 않도록 정의역을 나눈다(★이중계산 금지, 아래 기존 박스 직후 문단 참조).

\textbf{(d) 박스 — 세 성분 분해(기존 유지).}
아래는 L1719-1724 의 기존 박스를 \textbf{그대로} 옮긴 것이다(수정 없음, 라벨 `eq:lco-decomp` 불변):
\begin{equation}
\boxed{\;\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=\underbrace{\Delta S_j^\mathrm{config}}_{\text{logistic }w=RT/F\text{ 가 담음}}
+\underbrace{\Delta S_j^\mathrm{vib}}_{\text{음의 baseline}}
+\underbrace{\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)}_{\text{MIT 게이트, 삽입 기준 }<0,\ \propto T}\;.}
\label{eq:lco-decomp}
\end{equation}
```

**자기검수**:
- *차원*: $Z_\mathrm{tot},Z_\mathrm{config},Z_\mathrm{elec}$ 모두 무차원(분배함수), $F_\mathrm{tot}=-RT\ln Z$ 는
  J/mol, $S=-\partial F/\partial T$ 는 J/(mol·K) — 기존 박스 우변 세 항과 차원 일치.
- *이중계산*: (c)에서 명시했듯 가산성(직교, `eq:lco-Zfact`)과 무초과(슬롯 규칙)를 **별개 조건으로 분리** — 원문이
  "직교성이 가산성을, 이중계산 금지 규칙이 무초과를 보장"이라 서술한 것(L1741, 원문 그대로 보존)을 이제
  `eq:lco-Zfact`→`eq:lco-Sadd`의 명시적 유도가 뒷받침한다.
- *정합(챕터 내부)*: T1 총합 부호 재확인 — \S\ref{sec:lco-center} verifybox 가 이미 계산한 "$\approx+80-46\approx
  +34>0$"(대표 스케일 $+80$ J/(mol·K) $-$ 전자항 골 $-46$ J/(mol·K))이 바로 이 `eq:lco-decomp` 세 항의 합(config
  $+$vib 몫이 대표 스케일 $+80$ 대부분을 차지, elec 몫이 $-46$)과 같은 산술이다 — 두 절이 같은 수치로 교차확인
  (새 계산 아님, §1 검산과의 정합 재확인).
- *신설 라벨*: `eq:lco-Zfact`·`eq:lco-Sadd` 2종, 전수 grep 재확인(충돌 0). `eq:lco-decomp` 는 **재사용**(변경 0).

**앞 절 정합**: §1 (d) 박스의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 가 이 절에서 처음으로 내부 분해되며, §2 (T1 문단)의
`eq:lco-mit` 슬롯 분리 박스가 이미 "config 2상역 vs 전자 엔트로피"를 예고했던 것을 이 절이 분배함수 수준에서
근거를 대준다(§2→§4 방향의 인계, orphan 없음).

**원 줄글 대비**: 원문 L1732-1741 은 "(가) 가산성"을 "두 부분계가 독립인 극한에서 전체 분배함수가 $Z=Z_\mathrm{config}
\cdot Z_\mathrm{elec}$ 로 인수분해되어 $S=S_\mathrm{config}+S_\mathrm{elec}$ 가... 가산된다"고 **괄호 안 한 문장**으로
압축 서술했다(줄글 검산, V1010 STYLE_REPORT "Moderate" 판정과 일치 — "박스는 있으나 가산성이 줄글"). 위 (a)-(c) 는
그 한 문장을 $Z_\mathrm{tot}=Z_\mathrm{config}Z_\mathrm{elec}$(신설 `eq:lco-Zfact`) $\to\log$ 가산 $\to S_\mathrm{tot}
=S_\mathrm{config}+S_\mathrm{elec}$(신설 `eq:lco-Sadd`)로 펼쳤을 뿐, 기존 박스 `eq:lco-decomp` 와 "(나) 무이중계산"
문단(L1738-1741 후반)은 **글자 그대로 보존**한다.

---

### 5. 전자항 plug-in (L1756-1765 예고 + L1784-1788 규칙, 편입 대상 L1784-1788 확장)

**정독**: `sec:lco-decomp` 말미 "★Ch2/P4 코드 구현 예고"(L1756-1765) + `sec:lco-code` 항목 (ii)(L1784-1788) +
표 `tab:lco-staging` 캡션의 "현 구현은 $\Delta S_e$ 를 $T_\mathrm{ref}$ 에서 동결한 상수 오프셋"(L333-335) 재확인
— 세 곳에 흩어진 서술을 하나의 forward 사슬로 모은다.

**편입 지시**: L1784-1788(항목 (ii))을 아래로 교체. L1756-1765 의 예고 문단은 (a)의 근거로 인용만 하고 그대로 둔다.

```latex
\textbf{(a) 출발 — 좌표 다리: $x=x(\xi_{\eq,1}(V,T))$.}
게이트 식~\eqref{eq:ggate}$\cdot$\eqref{eq:dSegate} 의 $\Delta S_{e,1}$ 는 조성 $x$ 의 함수이나, 코드 \code{dqdv}
는 전압 격자 위에서 돈다. T1 전이의 진행률 $\xi_{\eq,1}(V,T)$(식~\eqref{eq:xieq}, 중심 $U_1^{\,d,\mathrm{cat}}$)가
그 전이 구간의 정규화 조성에 대응하므로($\xi_{\eq,1}:0\to1$ 이 T1 구간의 $x:x_\mathrm{start}\to x_\mathrm{end}$
에 대응, 표~\ref{tab:lco-staging} T1 $x$ 범위 $0.94$--$0.75$), 가장 단순한 실현은 선형 매핑
\begin{equation}
x(\xi_{\eq,1})=x_\mathrm{start}-(x_\mathrm{start}-x_\mathrm{end})\,\xi_{\eq,1}(V,T),
\qquad x_\mathrm{start}\approx0.94,\ x_\mathrm{end}\approx0.75
\label{eq:lco-xmap}
\end{equation}
다(★주의 — 이 명시 선형형은 "정규화 조성 대응"의 가장 단순한 실현이며, 원문(L1756-1761)은 매핑의 \emph{존재}만
명시하고 구체 함수형을 못박지 않았다 — 비선형 매핑도 배제되지 않는다, tier 표기: 선형형 자체는 tier C 가정).

\textbf{(b) 연산 — 게이트 대입.}
식~\eqref{eq:lco-xmap} 을 식~\eqref{eq:dSegate} 의 $z=(x-x_\mathrm{MIT})/\Delta x_\mathrm{MIT}$ 에 넣으면 $\Delta
S_{e,1}$ 가 $(V,T)$ 의 합성함수가 된다:
\[
\Delta S_{e,1}(V,T)=-\frac{\pi^2}{3}k_B^2T\,\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\,
\sigma(z)[1-\sigma(z)]\Big|_{z=[x(\xi_{\eq,1}(V,T))-x_\mathrm{MIT}]/\Delta x_\mathrm{MIT}}.
\]

\textbf{(c) 중간식 — 자기순환 지점(논리 감사, ★load-bearing).}
식~\eqref{eq:lco-dUdT}$\cdot$\eqref{eq:lco-decomp} 를 통해 $\Delta S_{e,1}(V,T)$ 가 $\Delta S_{\rxn,1}^\mathrm{cat}(T)$
에 더해지고, 그 $\Delta S_{\rxn,1}^\mathrm{cat}(T)$ 가 다시 $U_1^\mathrm{cat}(T)$(따라서 $U_1^{\,d,\mathrm{cat}}$,
따라서 $\xi_{\eq,1}(V,T)$ 자체)를 정한다 — 곧 (a)의 $x(\xi_{\eq,1})$ 는 자신이 결정에 관여하는 $U_1^{\,d,\mathrm{cat}}$
에 순환 의존한다(고정점 구조, $U_1\to\xi_{\eq,1}\to x\to\Delta S_{e,1}\to\Delta S_{\rxn,1}\to U_1$). 표~
\ref{tab:lco-staging} 캡션이 이미 밝힌 대로, \emph{현재} 구현은 이 순환을 열어 $\Delta S_e$ 를 $T_\mathrm{ref}$
에서 \textbf{동결한 상수 오프셋}으로 넣어(단일-기준 근사, 자기순환 없음 — $x$ 를 매 $\xi_{\eq,1}$ 재평가에 되먹이지
않음) 봉우리를 목표 전위에 두며, 식~\eqref{eq:lco-xmap}--(b)의 전 $x$-의존 게이트를 되먹이는 다온도 자기일관
버전은 \S\ref{sec:lco-decomp} 예고(L1761-1765)의 "다온도 round-trip 피팅 단계의 과제"로 이미 분리돼 있다 — 아래
(d) 박스는 이 두 지위(현재=동결 상수, 설계 목표=전 사슬)를 함께 명시한다.

\textbf{(d) 박스 — 두 지위의 forward 사슬.}
\begin{equation}
\boxed{\;
\begin{aligned}
\text{[현재, 단일-기준]}\quad &\Delta S_{\rxn,1}^\mathrm{cat}(T)\approx\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^{\,\mathrm{mol}}(x_0,T_\mathrm{ref})\ (\text{상수 오프셋}),\\
\text{[설계 목표, 다온도 round-trip]}\quad &x=x(\xi_{\eq,1}(V,T))\to\Delta S_{e,1}(V,T)\to\Delta S_{\rxn,1}^\mathrm{cat}(V,T)
\ \big[\text{식~\eqref{eq:lco-decomp}}\big]\\
&\to U_1^\mathrm{cat}(T)\ \big[\text{식~\eqref{eq:lco-dUdT} 적분형, 식~\eqref{eq:U1T2}}\big]
\to\dd Q/\dd V\ \big[\text{식~\eqref{eq:lco-peak}}\big]
\end{aligned}\;}
\label{eq:lco-plugin}
\end{equation}
두 번째 줄은 (c)의 고정점을 자기일관(iterative 또는 root-finding)으로 풀어야 닫히는 사슬이며, 그 풂은 본 문건
범위 밖(다온도 round-trip 피팅 단계)이다 — 이는 P4 코드 구현 예고가 이미 인정한 공백이지 새 결함이 아니다.
```

**자기검수**:
- *차원*: `eq:lco-xmap` 는 무차원($x$,$\xi$ 모두 무차원), 게이트 대입은 §sec:lco-electronic 이미 검증한 차원
  그대로(변경 없음).
- *부호*: $\xi_{\eq,1}:0\to1$(탈리튬화 진행)이 $x:0.94\to0.75$(리튬 함량 감소)에 대응 — 방향 부호 일치(탈리튬화
  는 $x$ 감소, `eq:lco-xmap` 의 $-(x_\mathrm{start}-x_\mathrm{end})\xi_{\eq,1}$ 항이 그 감소를 만듦, 정합).
- *논리 감사(★이 절의 최약점, load-bearing)*: (c)에서 명시한 자기순환(고정점) 구조는 원문 세 곳(L1756-1765·
  L1784-1788·L333-335)에 흩어져 있을 때는 드러나지 않던 것을 한 사슬로 모으며 처음 명시적으로 드러났다 —
  \emph{추정이 아니라} 세 원문의 논리적 결합에서 직접 도출되는 구조적 사실이다(호출체인: $U_1\to\xi_{\eq,1}\to
  x\to\Delta S_{e,1}\to\Delta S_{\rxn,1}\to U_1$). 원문이 이미 "현재는 동결", "다온도 피팅은 별도 과제" 둘 다
  명시했으므로 이는 \emph{새 결함이 아니라} 기존 공백의 명시화이며, 메인 결과로 승격하지 않고 (c)(d)의 감사
  문단으로만 한정한다(코너케이스 승격 금지 원칙 준수).
- *이중계산*: (d) 첫 줄(현재)과 둘째 줄(목표)을 같은 식으로 섞지 않도록 괄호로 분리 — 혼동 방지.
- *신설 라벨*: `eq:lco-xmap`·`eq:lco-plugin` 2종, 전수 grep 재확인(충돌 0).

**앞 절 정합**: §4 의 `eq:lco-decomp` 를 그대로 받아 $x$-의존을 명시화했고, §3 의 `eq:lco-peak` 가 이 절의 (d)
사슬 마지막 항으로 이어진다(순서: §1→§2→§4(분해)→§5(plug-in)→§3(peak) 의 논리 의존이나, tex 상 절 순서는
§1→§2→§3(peak)→§4(decomp)→§5(plug-in) — §5 의 (d) 박스가 §3 `eq:lco-peak` 를 \emph{후방 참조}하는 것은 tex 원
순서(N6 앞, N9 뒤)와 일치하므로 문제 없음, orphan 아님).

**원 줄글 대비**: 원문 L1784-1788 은 "T1 전이의 $\Delta S_\rxn$ 평가에... 더하는 한 줄"로 plug-in 을 규칙으로만
서술했다(V1010 STYLE_REPORT "Major" 판정 — "결론"). 위 (a)-(d) 는 좌표 매핑(L1756-1761 예고를 명시 선형식으로
구체화)과 plug-in 규칙(L1784-1788)을 사슬로 연결하고, 그 과정에서 원문 세 곳에 흩어져 있던 "동결 상수" 서술
(L333-335)까지 합쳐 사슬을 완성했다 — 그리고 이 결합에서 드러나는 자기순환 구조를 감사 결과로 명시했다(신규
발견, 그러나 결함 아님 — 원문이 이미 인정한 공백의 재확인).

---

### 6. MSMR — `sec:lco-code` (L1767-1792, 편입 대상 L1774-1780)

**정독**: 대상 절 전문(L1767-1792, `eq:msmr` L1770-1773 포함) + `sec:width`(L722-797, 특히 `eq:xieq` L787·
`eq:belliden` L1198) 재확인.

**★편입 범위 — §5(plug-in)와의 경계 명시(중복 편집 방지)**: L1767 헤더·`eq:msmr`(L1770-1773)는 그대로 둔다.
아래가 교체하는 것은 **L1774-1780**(대응 서술 3문단 + "바뀌는 것은 단 둘이다" 리드인 문장)까지만이다 —
`\begin{enumerate}`(L1781) 이하 **항목 구조는 그대로 유지**하며, 항목 (i)(전이 파라미터 교체, L1782-1783)은
\textbf{불변}, 항목 (ii)(전자항 plug-in, L1784-1788)는 \textbf{§5 의 (a)-(d) 로 별도 교체}된다(편집 순서:
본 절 적용 → 항목 (i) 그대로 → 항목 (ii) 자리에 §5 삽입 → `\end{enumerate}`(L1789) → L1790-1792 마무리 문단
불변). 두 절의 편입 대상 줄 범위가 겹치지 않도록 이미 확정했다(§5 = L1784-1788, 본 절 = L1774-1780).

```latex
\textbf{(a) 출발 — MSMR 점유분율의 정규화.}
식~\eqref{eq:msmr} $x_j=X_j/(1+\exp[f(U-U_j^0)/\omega_j])$ 의 양변을 $X_j$ 로 나누면 무차원 정규화 점유분율
$y_j\equiv x_j/X_j\in[0,1]$ 이 남는다:
\begin{equation}
y_j(U)=\frac{1}{1+\exp[f(U-U_j^0)/\omega_j]}.
\label{eq:lco-msmrnorm}
\end{equation}

\textbf{(b) 연산 — 대응 대입 $f=-\sigma_d$.}
$f=-\sigma_d$, $U_j^0=U_j^{\,d,\mathrm{cat}}$, $\omega_j=w_j^\mathrm{cat}$(본문 대응표)를 식~\eqref{eq:lco-msmrnorm}
에 그대로 넣으면
\[
y_j(V)=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j^\mathrm{cat}]}.
\]

\textbf{(c) 중간식 — $\xi_{\eq,j}$ 와의 항등 확인.}
우변은 식~\eqref{eq:xieq} $\xi_{\eq,j}(V,T)=1/(1+\exp[-\sigma_d(V-U_j^{\,d})/w_j])$ 와 \emph{글자 그대로} 같은
식이다 — 곧 $y_j\equiv\xi_{\eq,j}^\mathrm{cat}$(항등, 근사 아님). \emph{방향 부호 자기검산}: $\sigma_d=+1$(방전)
일 때 $f=-1$ 이고, $y_j=1/(1+\exp[-(U-U_j^0)/\omega_j])$ 는 $U\!\uparrow\Rightarrow y_j\!\uparrow$ — 식~
\eqref{eq:xieq} 의 방전 규약($V\!\uparrow\Rightarrow\xi_\eq\!\uparrow$, \S\ref{sec:width} signbox)과 방향이
일치한다(재유도로 확인, 원문의 대응표 주장을 대입으로 검증).

\textbf{(d) 박스 — MSMR에서 LCO peak 박스로.}
$X_j$ 가 $Q_j^\mathrm{cat}$ 처럼 전이당 상수이므로 $\dd x_j=X_j\,\dd y_j=X_j\,\dd\xi_{\eq,j}^\mathrm{cat}$, 그
$V$-미분은 식~\eqref{eq:belliden}(종 항등식 $\dd\xi_\eq/\dd z=\xi_\eq(1-\xi_\eq)$)과 연쇄율로
\[
\frac{\dd x_j}{\dd V}=X_j\,\frac{\dd\xi_{\eq,j}^\mathrm{cat}}{\dd V}
=X_j\,\frac{\sigma_d\,\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j^\mathrm{cat}},
\]
곧 $X_j\leftrightarrow Q_j^\mathrm{cat}$ 대응 아래
\begin{equation}
\boxed{\;
X_j\Big|\frac{\dd\xi_{\eq,j}^\mathrm{cat}}{\dd V}\Big|
\;\equiv\;\Big(\frac{\dd Q}{\dd V}\Big)^{\eq,\mathrm{cat}}_j\ \big[\text{식~\eqref{eq:lco-peak}}\big]\;}
\label{eq:lco-msmrclose}
\end{equation}
가 MSMR$\to$Ch1 peak 사슬을 닫는다 — 대응표(용량 $X_j\leftrightarrow Q_j$, 중심 $U_j^0\leftrightarrow U_j^{\,d}$,
폭 $\omega_j\leftrightarrow w_j$, 방향 $f\leftrightarrow-\sigma_d$)가 단순 서술이 아니라 대입$\to$항등$\to$미분의
사슬로 확인됐다. 따라서 곡선 클래스(\code{func\_ksi\_eq}$\cdot$\code{func\_U\_j}$\cdot$합산 식~\eqref{eq:sum})는
\emph{구조 변경 0}으로 LCO 에 적용되며, 바뀌는 것은 \S\ref{sec:lco-code} 항목 (i)(전이 파라미터 교체)$\cdot$
(ii)(전자항 plug-in, \S 전자항 plug-in 절)뿐이다.
```

**자기검수**:
- *부호*: $f=-\sigma_d$ 대응의 방향 일치를 (c)에서 재유도로 확인(원문은 대응표 서술만, 이번에 대입 검산 추가 —
  개선점).
- *차원*: $\omega_j$ 는 $w_j$ 와 같은 [V] 차원(대응표), $X_j$ 는 $Q_j$ 와 같은 [C] 급 무차원/용량 가중(기존
  대응표 그대로, 변경 없음).
- *극한*: $U=U_j^0$(중심)에서 $y_j=X_j/2$, $\xi_{\eq,j}=1/2$ — 두 식 모두 중심에서 반 채움, 일치.
- *이중계산*: 이 절은 형식적 동형 증명만 하며 새 물리항을 더하지 않음 — 해당 없음.
- *신설 라벨*: `eq:lco-msmrnorm`·`eq:lco-msmrclose` 2종, 전수 grep 재확인(충돌 0).

**앞 절 정합**: (d)의 결론이 §3 `eq:lco-peak` 를 정확히 재도출 — 별도 물리를 만들지 않고 §3 결과와 \emph{같은
식}에 닿음을 독립 경로(MSMR 형식)로 재확인한 셈이라, §3-§6 사이의 교차검증이 성립한다(같은 답에 두 경로로 도달 —
§1 의 이중경로 교차검증과 같은 검증 패턴).

**원 줄글 대비**: 원문 L1774-1779 는 대응관계를 표$\cdot$서술로만 제시하고 "구조가 동형이다"라고 결론지었을 뿐,
`eq:msmr` 를 실제로 조작해 `eq:xieq`·`eq:eqpeak` 로 만드는 대수를 보이지 않았다(V1010 STYLE_REPORT "대응표는
좋으나 변환 사슬 미폐쇄" 지적과 일치). 위 (a)-(d) 는 그 변환을 실제로 닫았다(정규화$\to$대입$\to$항등$\to$미분).
물리·대응관계·부호는 원문과 동일.

---

## 갈래 2 — H-2 정정문안

**정독**: `docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex` §ssec:logistic keybox(L161-166) + §ssec:weff/파생 C
(L540-569) + §sec:revheat 종합식(L673-690) + 파생 A srcbox(L485-496, 수치검증) 전문 재확인 + `FABLE_REAUDIT_C4_note.md`
§2(원 근거, v1.0.11 기준) 대조 + `Anode_Fit_v1.0.12.py`(`func_w` L75-76, `_width` L304-307) 코드 교차확인.

**실측 확인(모순의 정확한 위치, 줄 단위)**:
1. §ssec:logistic keybox(L163-164): "logistic 폭 $w=RT/F$ 는... 임의 모수가 아니라 단일 자리 2-상태 분배함수
   ~\eqref{eq:Z1} 가 정하는 분포의 열적 폭이다" — **한정어 없이** 모든 전이(흑연 staging 포함)에 적용되는 것처럼
   읽힌다.
2. §ssec:weff(L544-557, 파생 C): "단상($\Omega<2RT$)... 봉우리 폭은 평형이 \emph{예측}하는 양이다" vs "두-상
   ($\Omega>2RT$, \textbf{흑연 staging 전이가 여기 속함})... 이 폭은 평형이 정하는 양이 \emph{아니라}... 현상학적
   자유 피팅 파라미터다" — **정확히 같은 흑연 staging 전이**에 대해 1의 "아니다(=아니라)" 주장과 반대되는 "폭은
   평형 예측이 아니다"를 명시한다.
3. §sec:revheat 종합식(L683-686): "흑연 staging 의 \emph{두-상} 전이($\Omega>2RT$)에서는 평형 예측 $nRT/F$ 가
   아니라... 현상학적 자유 폭이다"로 2 를 재확인.
4. 파생 A srcbox(L486-489): "Chapter 1 코드(`Anode_Fit_v1.0.12`)의 4-전이 흑연 staging 파라미터로... 완전식은
   175 점 전 범위에서 FD 와 \emph{부동소수점 정밀도}로 일치" — 이 수치일치는 `eq:dxidT`(L459-467)의 $\partial w/
   \partial T=R/F$ 항(=$w=n_jRT/F$ 의 열적 미분)을 완전식에 넣어야 성립하며, 그 항을 그대로 쓰려면 **네 흑연
   staging 전이 전부**(모두 $\Omega>2RT$, 두-상 — \S\ref{sec:width})에 대해 $w_j$ 가 실제로 $n_jRT/F$ 로 $T$-선형
   스케일한다는 전제가 필요하다. 이는 2$\cdot$3 이 "아니다"라 선언한 바로 그 전제다.
5. **코드 교차확인(추정 아님, 직접 확인)**: `Anode_Fit_v1.0.12.py` L75-76 `def func_w(T,n): return n*R*T/F`,
   L304-307 `_width`(`"""전이 폭 w [V] = nRT/F(=func_w)..."""`) — 상전이 여부($\Omega$ 값)를 가리는 분기가 코드에
   \emph{없다}. 모든 전이(흑연 staging 포함)가 무조건 $w=n_jRT/F$ 로 평가된다. 곧 4 의 "부동소수점 일치"는
   \emph{현재 코드가 두-상에도 같은 함수형을 강제하기 때문에} 성립하는 것이지, 그 함수형이 두-상에서 물리적으로
   옳다는 증거가 아니다 — 검증과 물리적 지위를 혼동하면 안 된다(이것이 FABLE_REAUDIT_C4_note.md CRITICAL §2 의
   핵심이며, v1.0.12 로 넘어오며 줄 번호만 이동했을 뿐 모순 자체는 정정되지 않았다).

**정정문안 — §ssec:logistic keybox 교체(L161-166)**:

```latex
\begin{keybox}
Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라 \emph{격자기체 점유 분포의 여집합}(탈리튬화
진행률 $=1-\theta$)이다. logistic 폭 $w=RT/F$ 는(자리당 $n_j{=}1$ 기준; 전이별 유효 폭 $w_j=n_jRT/F$ 는
\S\ref{sec:revheat}$\cdot$코드 \texttt{func\_w}) 단일 자리 2-상태 분배함수~\eqref{eq:Z1} 가 정하는 분포의 열적
폭이라는 서술은 \textbf{★단상($\Omega_j\le2RT$) 전이에 한정된다} — Chapter 1 폭 이중지위 절과 본 장 파생 C
(\S\ref{ssec:weff})가 명시하듯, \emph{두-상}($\Omega_j>2RT$, 흑연 staging 전이가 여기 속함) 전이의 $w_j$ 는 이
열적 유도가 정하는 양이 아니라 broadening 이 정하는 현상학적 자유 피팅 폭이며(Chapter 1 broadening 절), $n_jRT/F$
형태를 유지해야 할 물리적 필연은 없다. \S\ref{ssec:overlap} 파생 A 의 수치검증(완전식$=$FD 부동소수점 일치)은
\emph{현재 코드가 상전이 여부를 가리지 않고 모든 전이에 $w_j=n_jRT/F$ 를 강제 적용한다는 구현 전제}(\texttt{func\_w}
$\cdot$\texttt{\_width}, $\Omega$ 분기 없음) 위에서만 성립한다 — 그 전제가 성립하는 한 두-상 흑연 staging 전이에도
같은 함수형이 대입되어 검증식이 부동소수점까지 맞아떨어지는 것이지, 그것이 두-상 $w_j$ 의 \emph{물리적} 지위를
평형 열적 폭으로 바꾸는 것은 \emph{아니다}(파생 C 의 phenomenological 지위 판정과 상충하지 않는 이유 — 검증
premise 와 물리적 주장을 혼동하지 않는다). ★표기: $\theta=$ Li 점유율(만충서 1), $\xi=1-\theta=$ 탈리튬화
진행률(희박서 1); 둘은 같은 점유 분포의 두 이름이다. Chapter 2 는 이 분포를 결론이 아니라 출발점으로 삼아
엔트로피를 쌓는다.
\end{keybox}
```

**표기 규약 확인**: 위 문안의 `\S\ref{sec:revheat}`·`\S\ref{ssec:weff}`·`\S\ref{ssec:overlap}` 는 ch2.tex \emph{자체}
라벨(같은 문서 내 참조, 정상 컴파일)이고, "Chapter 1 폭 이중지위 절"·"Chapter 1 broadening 절"은 \emph{다른 문서}
(ch1.tex)이므로 `\ref` 를 쓰지 않고 평문으로 적었다 — 기존 ch2.tex 의 실제 관행(L554-556 "Chapter 1 의 broadening
절에서" 이미 평문 참조)과 일치시킨 것이며, 신규 관행 도입이 아니다.

**자기검수**:
- *물리 불변*: 원 결과("단상에서 $w=RT/F$ 는 검증 가능한 평형 예측이다")는 그대로 보존 — 바뀐 것은 그 주장의
  \emph{적용 범위}(단상 한정)와, 파생 A 검증의 \emph{전제 명시}뿐. 수치$\cdot$부호$\cdot$결과식 변경 0.
- *이중계산/혼동 방지*: "검증 premise"(코드가 두-상에도 같은 함수형을 씀)와 "물리적 주장"(두-상 $w_j$ 가 평형
  열적 폭이다)을 명시적으로 분리 — 이것이 FABLE C-4 CRITICAL §2 가 지적한 바로 그 혼동의 해소.
- *Ch1 이중지위와의 정합*: Ch1 §sec:width(L740-755, "★폭 $w_j$ 의 이중지위 — 같은 식, 다른 지위")이 이미 "단상=
  평형 예측, 두-상=broadening 이 정하는 현상학적 자유 피팅 폭"을 확립했고, 본 정정문안은 그 Ch1 언어("이중지위")
  를 그대로 차용해 Ch2 keybox 를 정합시켰다 — 새 개념 도입 없음, 기존 Ch1 프레임을 Ch2 에 적용만.
- *잔여 검토(승격하지 않음)*: `eq:dxidT`(L459-467)의 $w(T)$ 조각 자체(§ssec:overlap 파생 A 의 "완전식") 논리를
  더 깊이 보면 — 만약 향후 어떤 두-상 전이의 실측 $w_j(T)$ 가 실제로 $n_jRT/F$ 선형을 따르지 \emph{않는다고}
  피팅에서 드러나면, 파생 A 의 "완전식=FD" 일치는 \emph{그 전이에 한해} 깨질 수 있다(코드가 강제하는 것과 실측이
  다를 가능성) — 이는 코너케이스로만 언급하고 메인 결과로 승격하지 않는다(현재 코드/현재 데이터 상태에서는 검증
  premise 가 성립하므로 파생 A 결과 자체는 유효).

**출처 근거 확인**: `FABLE_REAUDIT_C4_note.md` §2(CRITICAL, "w_j 열적 스케일링 지위의 구조적 자기모순 — 코드로
확증")가 이 모순을 v1.0.11 기준으로 이미 확정했고(파이썬 재유도+시뮬레이션+코드 대조 3중 검증), 위 문안은 그
판정을 v1.0.12 의 실제 줄 번호(L161-166 키박스, L544-557 파생 C, L486-489 파생 A)에 맞춰 재확인 후 정정 문안으로
좁힌 것이다 — 새 결함 발견이 아니라 기 확정 결함의 v1.0.12 정정 반영.

---

## 5줄 요약

1. **수식화 커버**: LCO 6절(center·hys·peak·decomp·plug-in·MSMR) 전부 (a)출발→(b)연산→(c)중간식→(d)박스 사슬로
   재작성 — center·hys 는 V1011 P11 map 을 독립 재검증 후 계승(도핑 극한 Taylor 전개를 직접 재도출로 보강),
   peak·decomp·plug-in·MSMR 은 신규 작성(각 STYLE_REPORT 지적 갭을 명시 대입$\cdot$유도로 폐쇄).
2. **논리결함 발견 여부**: (i) H-2 — Ch2 §logistic vs §weff 의 $w_j$ 열적 스케일링 지위 모순을 실측 확인, 코드
   교차확인(`func_w`/`_width` 에 $\Omega$ 분기 없음)으로 "검증 premise ≠ 물리적 주장" 구분 문안으로 정정. (ii)
   전자항 plug-in 절에서 $x=x(\xi_{\eq,1}(V))$ 좌표매핑이 $U_1(T)$ 에 순환 의존하는 고정점 구조를 처음 명시(원문이
   이미 인정한 공백의 재확인, 새 결함 아님 — 코너케이스로 한정, 메인 승격 안 함).
3. **물리 불변 확인**: 6절 전부 결과식$\cdot$부호$\cdot$수치$\cdot$$\Omega_j$ 기호 불변 — 전개 형식만 줄글→수식.
   신규 개념(ρ/PSD 등) 도입 0. `eq:lco-dUdT`(6곳 참조)·`eq:lco-decomp`(8곳 참조) 라벨 재사용 확정, 신설 라벨
   16종(J·gxi·gpp·spinodal·Veq·dUhys·Ubranch·mit·dope·peak·Zfact·Sadd·xmap·plugin·msmrnorm·msmrclose) 전수 grep
   충돌 0.
4. **불가침 확인**: `sec:lco-map`·`sec:lco-Se`·`sec:lco-gate`·N0-N9 흑연 본체·전자엔트로피 절·`sec:broadening`·
   verifybox(L490-516)·M-10 가드(T² 적분 해석) 전부 미접촉.
5. **최약점**: 전자항 plug-in 절의 자기순환(고정점) 구조 명시화(§5 (c))가 이번 작성에서 가장 새로운 발견이자
   가장 확신도가 낮은 지점이다 — 원문이 "다온도 round-trip 피팅 단계의 과제"로 이미 분리해 둔 공백이므로 결함은
   아니나, 좌표매핑의 구체 함수형(선형 `eq:lco-xmap`)은 tier C 가정(원문 미명시, 가장 단순한 실현으로 내가 보완)
   이라 Fable master 편입 시 이 부분만은 "제안"으로 표시하고 확정 결과로 승격하지 않기를 권한다.
