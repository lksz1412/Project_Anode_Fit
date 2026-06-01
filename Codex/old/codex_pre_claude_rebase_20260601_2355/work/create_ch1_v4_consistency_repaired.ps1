$ErrorActionPreference = 'Stop'

$project = 'D:\Projects\Project_Anode_Fit\Codex'
$src = Join-Path $project 'results\graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex'
$out = Join-Path $project 'results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex'
$plan = Join-Path $project 'plans\2026-05-28-chapter1-v4-consistency-repair-plan.md'
$scriptCopy = Join-Path $project 'work\create_ch1_v4_consistency_repaired.ps1'

function Replace-Exact {
  param(
    [Parameter(Mandatory=$true)][string]$Text,
    [Parameter(Mandatory=$true)][string]$Old,
    [Parameter(Mandatory=$true)][string]$New,
    [Parameter(Mandatory=$true)][string]$Name
  )
  if (-not $Text.Contains($Old)) {
    throw "Replacement target not found: $Name"
  }
  return $Text.Replace($Old, $New)
}

function Insert-AfterExact {
  param(
    [Parameter(Mandatory=$true)][string]$Text,
    [Parameter(Mandatory=$true)][string]$Anchor,
    [Parameter(Mandatory=$true)][string]$Insert,
    [Parameter(Mandatory=$true)][string]$Name
  )
  if (-not $Text.Contains($Anchor)) {
    throw "Insertion anchor not found: $Name"
  }
  return $Text.Replace($Anchor, $Anchor + $Insert)
}

$text = Get-Content -LiteralPath $src -Raw -Encoding UTF8
$text = $text -replace "`r`n", "`n"

$planText = @'
# Chapter 1 v4 Consistency Repair Plan

Date: 2026-05-28

## Summary

This repair plan fixes the problems found in Phase 014 without overwriting prior artifacts. The target artifact is a new Chapter 1 candidate:

`D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex`

The repair keeps the manuscript-facing structure of v3, but restores the derivation consistency and explicit logic required by the user:

- LIB graphite anode ICA peak tail is the target phenomenon.
- Low temperature gives a longer post-peak tail; high temperature gives a shorter tail.
- Activation free-energy barrier is retained as a rate-determining quantity.
- A step-function or sudden `0 -> 1` completion model is forbidden.
- Electrode potential assistance smoothly lowers the effective barrier and shifts the relaxation-length spectrum.
- The manuscript remains theory/logic only, not a solver or fitting implementation.
- Korean prose is used, but academic terms remain in English.
- Undergraduate-followable derivation blocks must be present where logical gaps would otherwise occur.

## Current Ground Truth

- v3 is the active manuscript shell.
- Phase 014 found coordinate drift (`q` versus `Q`), state symbol drift (`theta` versus `xi`), derivation compression, external-only AL tags, and a later fitting section that leaned too strongly toward Plan A.
- The repair chooses normalized charge coordinate `q` as the primary coordinate.
- Dimensional charge coordinate `Q_ext` is retained only through explicit conversion:
  `L_Q = v_Q/k = Q_cell L_q`, `L_q = v_q/k = |I|/(Q_cell k)`.

## Phase Range

## Phase 015 — v4 consistency repair

Steps:

1. Create a new v4 artifact from v3 without overwriting v2 or v3.
2. Repair notation and coordinate consistency: `theta`, `q`, `L_q` are primary; `L_Q` is conversion-only.
3. Reinsert compact derivation blocks for lattice-gas target, charge-balance differential form, and forward/back rate relaxation.
4. Add a compact Assumption Ledger inside the `.tex` body.
5. Reframe Plan B as the always-available theoretical baseline and Plan A as a candidate analytic compression only after validation.
6. Run static LaTeX consistency checks and targeted content checks.
7. Save Phase 015 result/ledger/handover records.

## Non-goals

- Do not build a numerical solver.
- Do not implement fitting code.
- Do not claim Plan A/Fredholm closure is established before validation.
- Do not overwrite v2, v3, Claude outputs, original downloaded `.tex`, or user PDF files.
- Do not put phase history or audit metadata inside the manuscript body.

## Test Plan

- Check `\begin`/`\end` balance.
- Check brace balance.
- Check missing `\ref` labels and missing `\cite` bibitems.
- Search for forbidden or risky remnants: `\xi`, ambiguous `L=v_Q/k`, dimensional Plan B tail in `Q`, and implementation-colored fallback wording.
- Full-read the generated v4 file in recorded chunks before reporting.

## Assumptions

- `xelatex` is not available on PATH; PDF generation is outside this phase unless a TeX distribution is installed later.
- The repair is a consistency repair of v3, not a new scientific literature expansion.

## Correction History

- Supersedes neither v2 nor v3. v4 is a new candidate artifact created because Phase 014 identified repairable consistency defects in v3.
'@

Set-Content -LiteralPath $plan -Value ($planText -replace "`n", "`r`n") -Encoding UTF8

$text = Replace-Exact $text 'kernel ($L=v_Q/k$) 을 만든다. 관측 tail 은 barrier distribution $\rho_G$ 가 \emph{지수적' 'kernel ($L_q=v_q/k=|I|/(Q_\cell k)$) 을 만든다. 관측 tail 은 barrier distribution $\rho_G$ 가 \emph{지수적' 'abstract L coordinate'
$text = Replace-Exact $text 'Plan B만으로 Chapter 1의 물리 논리, 즉 low temperature 에서 large-$L$ weight가 커지고
potential assistance가 short-$L$ shift를 만든다는 설명은 유지된다.' 'Plan B만으로 Chapter 1의 물리 논리, 즉 low temperature 에서 large-$L_q$ weight가 커지고
potential assistance가 short-$L_q$ shift를 만든다는 설명은 유지된다.' 'abstract large/short L'
$text = Replace-Exact $text '하나의 mode 는 length $L=v_Q/k$ 의 \emph{단일 exponential kernel} 을 만든다.' '하나의 mode 는 normalized charge coordinate 에서 length $L_q=v_q/k=|I|/(Q_\cell k)$ 의 \emph{단일 exponential kernel} 을 만든다.' 'H4 Lq'
$text = Replace-Exact $text 'S7 & single-mode exponential kernel $L=v_Q/k$ & GROUNDED \AL{1} \\' 'S7 & single-mode exponential kernel $L_q=v_q/k=|I|/(Q_\cell k)$; $L_Q=Q_\cell L_q$ & GROUNDED \AL{1} \\' 'S7 Lq'
$text = Replace-Exact $text '\textbf{(H6)} $T$ 가 낮으면 spectrum 이 large-$L$ 로 이동해 tail 이 길어지고, $T$ 가
높거나 potential assistance 가 크면 short-$L$ 로 이동해 tail 이 짧아진다 (O2; \S\ref{sec:tailT}).' '\textbf{(H6)} $T$ 가 낮으면 spectrum 이 large-$L_q$ 로 이동해 tail 이 길어지고, $T$ 가
높거나 potential assistance 가 크면 short-$L_q$ 로 이동해 tail 이 짧아진다 (O2; \S\ref{sec:tailT}).' 'H6 Lq'
$text = Replace-Exact $text 'S11 & ICA mapping $dQ/dV_n$ & GROUNDED \AL{9} \\' 'S11 & ICA mapping $dQ_\ext/dV_n$ & GROUNDED \AL{9} \\' 'S11 dQext'
$text = Replace-Exact $text 'fitting solver 구현은 Chapter 1 범위 외 (P1).' 'quantitative fitting implementation 은 Chapter 1 범위 외 (P1).' 'remove solver wording'
$text = Replace-Exact $text '\textbf{Plan B}는 code route 가 아니라, local residual ODE 와 relaxation-length spectrum' '\textbf{Plan B}는 계산 절차가 아니라, local residual ODE 와 relaxation-length spectrum' 'remove code route abstract'

$agpAnchor = @'
\textbf{AGP.} 모든 assumption 은 AL-\# 인용. FLAGGED 는 established 로 사용 금지; BOUNDED
는 유효범위 병기. step-function·$0\!\to\!1$ 급점프·$\max$·$\min$·Heaviside·hard-switch
정의식 금지 (smooth only).
'@

$assumptionLedger = @'

\subsection{Compact Assumption Ledger}\label{sec:assumption_ledger}
\begin{longtable}{p{0.11\textwidth} p{0.17\textwidth} p{0.60\textwidth}}
\toprule ID & 상태 & 본 Chapter 에서의 의미 \\ \midrule \endhead
AL-1 & GROUNDED & transition-state / Eyring 관점: activation free-energy barrier 는 rate constant 를 정한다. \\
AL-2 & BOUNDED & BEP/Marcus small-driving-force 영역에서 electrode potential assistance 는 effective barrier 를 smooth 하게 낮춘다. \\
AL-3a & GROUNDED & equilibrium target 의 grounded 특수해는 lattice-gas / regular-solution chemical potential 에서 온다. \\
AL-3b & FLAGGED & erf/Gaussian-cumulative target 은 graphite thermodynamic derivation 이 확정되기 전까지 empirical ansatz 다. \\
AL-4 & GROUNDED & graphite staging transition 은 ICA peak 의 thermodynamic origin 이다. \\
AL-5 & BOUNDED & local mode 는 near-equilibrium first-order relaxation 으로 선형화할 수 있다. \\
AL-6 & BOUNDED & barrier distribution 에서 relaxation-length spectrum 으로 가는 역매핑은 non-unique 이므로 forward prediction 만 허용한다. \\
AL-7 & DQ & Refs 6/7 Fredholm / propagator / ratio-substitution method 는 Plan A candidate closure 이며, 적용성 검증 전에는 core assumption 이 아니다. \\
AL-8 & FLAGGED & low-$T$ long tail 과 potential-assisted short-$L_q$ shift 를 kinetic-spectrum signature 로 해석하는 부분은 novel hypothesis 이다. \\
AL-9 & GROUNDED & internal anode potential $V_n$ 은 charge conservation 의 implicit root 이며 외부 lookup 이 아니다. \\
AL-10 & METHOD & competing mechanisms, identifiability, and falsification protocol 을 통과해야 barrier-spectrum 귀속을 주장할 수 있다. \\
\bottomrule
\end{longtable}
'@

$text = Insert-AfterExact $text $agpAnchor $assumptionLedger 'compact assumption ledger'

$notationOld = @'
$q$ & --- & 정규화 진행 좌표 $q=Q_\ext/Q_\cell$ \\
$Q_\ext$ & C & 외부 누적 charge; $v_Q\equiv dQ_\ext/dt=|I|>0$ (scan speed) \\
$Q_\cell$ & C & 기준 cell capacity \\
'@

$notationNew = @'
$q$ & --- & 정규화 진행 좌표 $q=Q_\ext/Q_\cell$; 본 Chapter 의 primary coordinate \\
$Q_\ext$ & C & dimensional external charge; $v_Q\equiv dQ_\ext/dt=|I|>0$ \\
$Q_\cell$ & C & 기준 cell capacity; $q=Q_\ext/Q_\cell$ 의 scale \\
$v_q$ & 1/s & normalized scan speed $v_q\equiv dq/dt=v_Q/Q_\cell=|I|/Q_\cell$ \\
'@

$text = Replace-Exact $text $notationOld $notationNew 'notation q/Q rows'
$text = Replace-Exact $text '$L$ & --- & local relaxation length. $Q$-좌표서 $v_Q/k$; 정규화 $q=Q_\ext/Q_\cell$ 좌표서 $L=|I|/(Q_\cell k)$ (무차원) \\' '$L_q$ & --- & normalized local relaxation length in $q$ coordinate, $L_q=v_q/k=|I|/(Q_\cell k)$ \\
$L_Q$ & C & dimensional charge-axis relaxation length, $L_Q=v_Q/k=Q_\cell L_q$; dimensional $Q_\ext$ 식에서만 사용 \\' 'notation L rows'
$text = Replace-Exact $text '$A_L(L;T,\psi)$ & 1/L & relaxation-length spectral \emph{density} (in $L$; $\int A_L\,dL$ 가 weight) \\' '$A_L(\lambda;T,\psi)$ & 1 & relaxation-length spectral \emph{density} over normalized length variable $\lambda=L_q$; $\int A_L(\lambda)\,d\lambda$ 가 weight \\' 'notation AL row'

$chargeAnchor = @'
$\theta_j=\theta_{\eq,j}$ 이면 그 해를 $V_n=V_{n,\mathrm{OCV}}(q,T)$ 로 정의 — 외부 OCV
lookup 은 이 charge-balance 의 equilibrium 특수해다.
'@

$chargeInsert = @'

\textbf{Derivation D1b (differential charge balance).} 식~\eqref{eq:charge_balance} 를
solution path 를 따라 $q$ 로 미분하면
\begin{equation}
Q_\cell
=
C_\bg(V_n,T)\frac{\dd V_n}{\dd q}
+Q_p\frac{\dd\Theta}{\dd q},
\qquad
C_\bg\equiv \frac{\partial Q_\bg}{\partial V_n}.
\label{eq:charge_balance_differential}
\end{equation}
따라서
\begin{equation}
\frac{\dd V_n}{\dd q}
=
\frac{Q_\cell-Q_p\,\dd\Theta/\dd q}{C_\bg(V_n,T)}.
\label{eq:dvdq_charge}
\end{equation}
이 식은 later ICA mapping 의 출발점이며, $\dd\Theta/\dd q$ 에 tail contribution 이 들어간다.
'@

$text = Insert-AfterExact $text $chargeAnchor $chargeInsert 'charge differential insertion'

$eqOld = @'
\textbf{Grounded 특수해 (lattice-gas, \AL{3a}).} 명시적 형태가 필요하면, graphite
intercalation 의 grounded thermodynamics 인 lattice-gas / regular-solution chemical
potential \cite{mckinnon1983,bazant2013} 을 쓴다: $\mu(\theta)=\mu^0+RT\ln[\theta/(1-\theta)]
+\Omega_j(1-2\theta)$, electrochemical equilibrium $\mu=s_{\phi,j}F(V_n-U_j^0)$ 에서
($\Omega_j=0$ ideal limit)
\begin{equation}
\theta_{\eq,j}=\big[1+\exp(-s_{\phi,j}(V_n-U_j)/w_j)\big]^{-1},\qquad w_j=RT/F,
\label{eq:latticegas}
\end{equation}
즉 smooth logistic ($0\!\to\!1$ 급점프 아님). $\Omega_j\ne0$ 이면 width/형태 보정, smooth
유지.
'@

$eqNew = @'
\textbf{Grounded 특수해 (lattice-gas, \AL{3a}).} 명시적 형태가 필요하면, graphite
intercalation 의 grounded thermodynamics 인 lattice-gas / regular-solution chemical
potential \cite{mckinnon1983,bazant2013} 을 쓴다:
\begin{equation}
\mu_j(\theta_j,T)
=
\mu_j^0(T)
+RT\ln\frac{\theta_j}{1-\theta_j}
+\Omega_j(1-2\theta_j).
\label{eq:mu_regular_solution}
\end{equation}
equilibrium 에서는 electrochemical potential balance 가 성립하므로
\begin{equation}
\mu_j(\theta_{\eq,j},T)=s_{\phi,j}F\big(V_n-U_j^0(T)\big).
\label{eq:mu_equilibrium_condition}
\end{equation}
ideal limit $\Omega_j=0$ 에서 식~\eqref{eq:mu_equilibrium_condition} 을 $\theta_{\eq,j}$ 에 대해
풀면
\begin{equation}
\theta_{\eq,j}
=
\big[1+\exp(-s_{\phi,j}(V_n-U_j)/w_j)\big]^{-1},
\qquad
w_j=\frac{RT}{F},
\label{eq:latticegas}
\end{equation}
이고, 따라서
\begin{equation}
\frac{\partial\theta_{\eq,j}}{\partial V_n}
=
\frac{s_{\phi,j}}{w_j}\theta_{\eq,j}(1-\theta_{\eq,j}),
\qquad
\left|\frac{\partial\theta_{\eq,j}}{\partial V_n}\right|_\mathrm{max}
=
\frac{1}{4w_j}.
\label{eq:thetaeq_derivative}
\end{equation}
즉 homogeneous lattice-gas target 의 voltage width 는 $w_j=RT/F$ 로 temperature 에 비례한다.
저온에서는 equilibrium peak 가 더 좁아지는 방향이므로, 관측된 \emph{low-$T$ long tail} 을
homogeneous equilibrium width 만으로 설명할 수 없다. $\Omega_j\ne0$ 이면 width/형태가 보정되지만
target 은 여전히 smooth 이며 $0\!\to\!1$ 급점프가 아니다.
'@

$text = Replace-Exact $text $eqOld $eqNew 'equilibrium derivation block'

$d5Old = @'
\textbf{Derivation D5 (single-mode relaxation, \AL{5}).} 한 local mode 의 lag $r=\theta_\eq-\theta$.
forward/backward rate $r_+,r_-$ 의 net flux $\dot\theta=r_+(1-\theta)-r_-\theta$ 는 stationary
target $\theta_\eq=r_+/(r_++r_-)$ 근처에서 $\dot\theta=k(\theta_\eq-\theta)$, $k=r_++r_-$ 로
환원된다. 즉 $\theta_\eq$ 는 target, $k$ 는 그 target 으로 접근하는 mobility — 이 구분이
double counting 을 막는다 (target 과 mobility 를 동시에 자유 fitting 하지 않음).
'@

$d5New = @'
\textbf{Derivation D5 (single-mode relaxation, \AL{5}).} 한 local mode 의 lag 를
$r=\theta_\eq-\theta$ 로 둔다. forward/backward elementary rate constant 를 $k_+$, $k_-$ 라 쓰면
\begin{equation}
\dot\theta
=
k_+(1-\theta)-k_-\theta.
\label{eq:forward_backward_flux}
\end{equation}
stationary condition $\dot\theta=0$ 에서
\begin{equation}
\theta_\eq=\frac{k_+}{k_++k_-}.
\label{eq:thetaeq_rates}
\end{equation}
식~\eqref{eq:forward_backward_flux} 에 식~\eqref{eq:thetaeq_rates} 를 대입하면
\begin{equation}
\dot\theta
=
(k_++k_-)(\theta_\eq-\theta)
\equiv
k(\theta_\eq-\theta).
\label{eq:first_order_relaxation}
\end{equation}
즉 $\theta_\eq$ 는 thermodynamic target, $k$ 는 그 target 으로 접근하는 kinetic mobility 다.
이 구분이 target 과 mobility 를 동시에 자유 fitting 하는 double counting 을 막는다.
'@

$text = Replace-Exact $text $d5Old $d5New 'D5 detailed derivation'

$d6Old = @'
\boxed{\;r(q)\simeq r(q_a)\exp\!\Big[-\frac{q-q_a}{L}\Big],\qquad L=\frac{|I|}{Q_\cell\,k}.\;}
\label{eq:single_kernel}
\end{equation}
이것은 관측 tail 전체가 단일 exponential 이라는 뜻이 \emph{아니다} — \textbf{하나의 local
mode 가 만드는 exponential kernel} 이다. 차원: $L$ 은 무차원 ($q$ 단위). $|I|/(Q_\cell k)=$
A/(C$\cdot$1/s)$=$무차원. 일치.
'@

$d6New = @'
\boxed{\;r(q)\simeq r(q_a)\exp\!\Big[-\frac{q-q_a}{L_q}\Big],\qquad L_q=\frac{|I|}{Q_\cell\,k}=\frac{v_q}{k}.\;}
\label{eq:single_kernel}
\end{equation}
이것은 관측 tail 전체가 단일 exponential 이라는 뜻이 \emph{아니다} — \textbf{하나의 local
mode 가 만드는 exponential kernel} 이다. 차원: $L_q$ 은 무차원 ($q$ 단위). $|I|/(Q_\cell k)=$
A/(C$\cdot$1/s)$=$무차원. dimensional charge axis 로 쓰면 $L_Q=Q_\cell L_q=v_Q/k$ 이다.
'@

$text = Replace-Exact $text $d6Old $d6New 'D6 single kernel Lq'
$text = Replace-Exact $text 'transition 이 $dQ/dV_n$ 에 peak 를 남긴다 \cite{dahn1991,ohzuku1993,funabiki1999} (\AL{4}).' 'transition 이 $dQ_\ext/dV_n$ 에 peak 를 남긴다 \cite{dahn1991,ohzuku1993,funabiki1999} (\AL{4}).' 'staging dQext'

$text = Replace-Exact $text '\textbf{Derivation D7 (barrier$\to$length 지수 매핑).} 식~\eqref{eq:rate} 와 $L=|I|/(Q_\cell k)$
에서' '\textbf{Derivation D7 (barrier$\to$length 지수 매핑).} 식~\eqref{eq:rate} 와 $L_q=|I|/(Q_\cell k)$
에서' 'D7 intro Lq'
$text = Replace-Exact $text '\boxed{\;L(G,T,\psi)=\frac{|I|}{Q_\cell\,k_0(T)}\exp\!\Big[\frac{G-W_\psi}{RT}\Big].\;}' '\boxed{\;L_q(G,T,\psi)=\frac{|I|}{Q_\cell\,k_0(T)}\exp\!\Big[\frac{G-W_\psi}{RT}\Big].\;}' 'D7 formula Lq'
$text = Replace-Exact $text '$G$ 의 작은 변화가 $L$ 에서 \emph{지수적으로 확대}된다 — 이것이 stretched tail 의 핵심
근원이다 (long tail 은 $\rho_G$ 자체가 길어서가 아니라 barrier$\to$length 매핑이 지수이기
때문일 수 있다). 역변환 $G(L)=W_\psi+RT\ln[Q_\cell k_0 L/|I|]$, Jacobian $|dG/dL|=RT/L$.
따라서 relaxation-length spectrum:' '$G$ 의 작은 변화가 $L_q$ 에서 \emph{지수적으로 확대}된다 — 이것이 stretched tail 의 핵심
근원이다 (long tail 은 $\rho_G$ 자체가 길어서가 아니라 barrier$\to$length 매핑이 지수이기
때문일 수 있다). 역변환 $G(L_q)=W_\psi+RT\ln[Q_\cell k_0 L_q/|I|]$, Jacobian $|dG/dL_q|=RT/L_q$.
따라서 relaxation-length spectrum:' 'D7 explanatory Lq'
$text = Replace-Exact $text 'A_L(L;T,\psi)=\rho_G\big(G(L,T,\psi);T,\psi\big)\,\frac{RT}{L}\,A_0(L;T,\psi),' 'A_L(\lambda;T,\psi)=\rho_G\big(G(\lambda,T,\psi);T,\psi\big)\,\frac{RT}{\lambda}\,A_0(\lambda;T,\psi),' 'spectrum formula lambda'
$text = Replace-Exact $text '$A_0$ 는 각 mode 의 initial residual amplitude·population weight·accessibility (무차원
per-mode factor). $A_L$ 의 $1/L$ 차원은 $RT/L$ Jacobian 에서 오며, $A_L$ 은 weight 가
아니라 $L$ 에 대한 \emph{density} 다 ($\int A_L\,dL=$ 총 weight).' '$A_0$ 는 각 mode 의 initial residual amplitude·population weight·accessibility (무차원
per-mode factor). $\lambda=L_q$ 는 무차원 integration variable 이며, $A_L(\lambda)$ 는
$\lambda$ 에 대한 \emph{density} 다 ($\int A_L(\lambda)\,d\lambda=$ 총 weight).' 'spectrum density explanation'

$kernelOld = @'
\boxed{\;\frac{d\Theta_\mathrm{tail}}{dq}\simeq\int_0^\infty A_L(L;T,\psi)\,\frac1L\,
\exp\!\Big[-\frac{q-q_a}{L}\Big]\,dL.\;}
'@

$kernelNew = @'
\boxed{\;\frac{d\Theta_\mathrm{tail}}{dq}\simeq\int_0^\infty A_L(\lambda;T,\psi)\,\frac1\lambda\,
\exp\!\Big[-\frac{q-q_a}{\lambda}\Big]\,d\lambda,\qquad \lambda=L_q.\;}
'@

$text = Replace-Exact $text $kernelOld $kernelNew 'kernel integral lambda'
$text = Replace-Exact $text 'single-
mode 식~\eqref{eq:single_kernel} 은 kernel 하나일 뿐이며, 관측 stretched tail 은 spectrum
$A_L$ 의 large-$L$ 영역이 결정한다.' 'single-
mode 식~\eqref{eq:single_kernel} 은 kernel 하나일 뿐이며, 관측 stretched tail 은 spectrum
$A_L$ 의 large-$L_q$ 영역이 결정한다.' 'kernel large Lq'
$text = Replace-Exact $text '\mathcal K(q,q'')=\int_0^\infty A_L(L;T,\psi)\,\frac1L\,\exp\!\Big[-\frac{q-q''}{L}\Big]\,dL,' '\mathcal K(q,q'')=\int_0^\infty A_L(\lambda;T,\psi)\,\frac1\lambda\,\exp\!\Big[-\frac{q-q''}{\lambda}\Big]\,d\lambda,' 'K_def lambda'
$text = Replace-Exact $text '(single-mode 식~\eqref{eq:single_kernel} 은 $A_L=\delta(L-L_0)$ 특수해로 항상 포함).' '(single-mode 식~\eqref{eq:single_kernel} 은 $A_L(\lambda)=\delta(\lambda-L_{q,0})$ 특수해로 항상 포함).' 'delta special case lambda'

$text = Replace-Exact $text '\Delta G_\eff \rightarrow k \rightarrow L \rightarrow A_L \rightarrow' '\Delta G_\eff \rightarrow k \rightarrow L_q \rightarrow A_L \rightarrow' 'core chain Lq'
$text = Replace-Exact $text '\int A_L K_L\,dL \rightarrow \text{ICA tail}.' '\int A_L(\lambda)K_\lambda\,d\lambda \rightarrow \text{ICA tail}.' 'core chain integral lambda'
$text = Replace-Exact $text 'Ratio-substitution ansatz 가 $\xi_j(s)/\xi_j(Q)$, $r_j(s)/r_j(Q)$, 또는
  $\Theta(s)/\Theta(Q)$ 중 어느 대상에 적용되는지 명시되어야 한다.' 'Ratio-substitution ansatz 가 $\theta_j(s)/\theta_j(q)$, $r_j(s)/r_j(q)$, 또는
  $\Theta(s)/\Theta(q)$ 중 어느 대상에 적용되는지 명시되어야 한다.' 'Plan A ratio theta q'
$text = Replace-Exact $text '이 조건이 성립할 때만, 어떤 effective unknown $Y(Q)$에 대해' '이 조건이 성립할 때만, 어떤 effective unknown $Y(q)$에 대해' 'Plan A Y q intro'
$text = Replace-Exact $text 'Y(Q)=Y_0+\int_{\mathcal D}K(Q,S)\,\Phi[Y](S)\,\dd S' 'Y(q)=Y_0+\int_{\mathcal D}K(q,s)\,\Phi[Y](s)\,\dd s' 'Plan A closure general q'
$text = Replace-Exact $text 'Y_{\mathrm A}(Q)=' 'Y_{\mathrm A}(q)=' 'Plan A YA q'
$text = Replace-Exact $text '\mathcal C_{\mathrm{ratio}}\!\left[K,\Phi,Y^{\mathrm{ref}}\right](Q)' '\mathcal C_{\mathrm{ratio}}\!\left[K,\Phi,Y^{\mathrm{ref}}\right](q)' 'Plan A C q'

$planBOld = @'
\begin{align}
\frac{\dd r_j}{\dd Q}+\frac{k_j}{v_Q}r_j
&=
\frac{\dd\xi_{\eq,j}}{\dd Q},
\label{eq:planb_residual}
\\
L(G,T,\psi)
&=
\frac{v_Q}{k_0(T)}
\exp\!\left[\frac{G-W_\psi}{RT}\right],
\label{eq:planb_length}
\\
\mathcal T_j(Q;T,\psi)
&=
\int_0^\infty
A_{L,j}(L;T,\psi)\frac{1}{L}
\exp\!\left[-\frac{Q-Q_{a,j}}{L}\right]\dd L.
\label{eq:planb_tail}
\end{align}
'@

$planBNew = @'
\begin{align}
\frac{\dd r_j}{\dd q}+\frac{Q_\cell k_j}{|I|}r_j
&=
\frac{\dd\theta_{\eq,j}}{\dd q},
\label{eq:planb_residual}
\\
L_q(G,T,\psi)
&=
\frac{|I|}{Q_\cell k_0(T)}
\exp\!\left[\frac{G-W_\psi}{RT}\right],
\label{eq:planb_length}
\\
\mathcal T_j(q;T,\psi)
&=
\int_0^\infty
A_{L,j}(\lambda;T,\psi)\frac{1}{\lambda}
\exp\!\left[-\frac{q-q_{a,j}}{\lambda}\right]\dd \lambda,
\qquad \lambda=L_q.
\label{eq:planb_tail}
\end{align}
'@

$text = Replace-Exact $text $planBOld $planBNew 'Plan B q theta Lq'
$text = Replace-Exact $text '첫 번째 식은 local state 가 equilibrium target 을 finite rate 로 따라가는 residual equation 이다.
두 번째 식은 activation barrier 와 potential assistance 가 relaxation length 로 바뀌는 exponential
mapping 이다. 세 번째 식은 여러 local kernel 의 spectrum mixture 이다. 이 세 식만으로도
\emph{low $T$에서 large-$L$ weight가 커져 tail이 길어지고, positive potential assistance가
short-$L$ shift를 만들어 tail을 줄인다}는 Chapter 1의 핵심 설명은 완결된다.' '첫 번째 식은 $q$-coordinate 에서 local state 가 equilibrium target 을 finite rate 로 따라가는 residual equation 이다.
두 번째 식은 activation barrier 와 potential assistance 가 normalized relaxation length 로 바뀌는 exponential
mapping 이다. 세 번째 식은 여러 local kernel 의 spectrum mixture 이다. 이 세 식만으로도
\emph{low $T$에서 large-$L_q$ weight가 커져 tail이 길어지고, positive potential assistance가
short-$L_q$ shift를 만들어 tail을 줄인다}는 Chapter 1의 핵심 설명은 완결된다.' 'Plan B prose Lq'
$text = Replace-Exact $text 'Plan B가 closed analytic shortcut 을 주지 않는다고 해서 물리 논리가 부족한 것은 아니다. Chapter 1에서
필요한 것은 solver가 아니라 state/target/rate/spectrum 의 logical separation 이다. Plan B는 그
separation을 보존하는 baseline theory 이며, Plan A는 이 baseline 위에 얹히는 candidate analytic
compression 이다.' 'Plan B가 compact analytic expression 을 주지 않는다고 해서 물리 논리가 부족한 것은 아니다. Chapter 1에서
핵심은 state/target/rate/spectrum 의 logical separation 이다. Plan B는 그
separation을 보존하는 baseline theory 이며, Plan A는 이 baseline 위에 얹히는 candidate analytic
compression 이다.' 'remove solver closed shortcut'
$text = Replace-Exact $text '구현상 예비 경로나 code procedure가 아니라, Chapter 1이 항상 보존해야 하는 논리적 기준식이다.' '분석상 예비 경로나 계산 절차가 아니라, Chapter 1이 항상 보존해야 하는 논리적 기준식이다.' 'remove code procedure'
$text = Replace-Exact $text '\item 이 dual hierarchy는 coding route이 아니라 논리적 책임 분리다.' '\item 이 dual hierarchy는 계산 절차가 아니라 논리적 책임 분리다.' 'remove coding route'

$icaOld = @'
background storage $dQ_\bg=C_\bg(V_n,T)\,dV_n$ 와 phase progress $Q_p\,d\Theta$ 의 합
$dQ=C_\bg dV_n+Q_p d\Theta$ 에서
\begin{equation}
\boxed{\;\frac{dQ}{dV_n}=\frac{C_\bg(V_n,T)}{1-Q_p\,(d\Theta/dQ)}.\;}
\label{eq:ica}
\end{equation}
식~\eqref{eq:kernel_integral} 의 tail 기여가 $d\Theta/dQ$ 에 들어가 ICA tail 로 나타난다.
'@

$icaNew = @'
background storage $dQ_\bg=C_\bg(V_n,T)\,dV_n$ 와 phase progress $Q_p\,d\Theta$ 의 합은
\[
dQ_\ext=C_\bg(V_n,T)\,dV_n+Q_p\,d\Theta,
\qquad dQ_\ext=Q_\cell\,dq
\]
이다. 식~\eqref{eq:charge_balance_differential} 과 동치로 정리하면
\begin{equation}
\boxed{\;\frac{dQ_\ext}{dV_n}=Q_\cell\frac{dq}{dV_n}
=
\frac{C_\bg(V_n,T)}
{1-(Q_p/Q_\cell)\,(d\Theta/dq)}.\;}
\label{eq:ica}
\end{equation}
식~\eqref{eq:kernel_integral} 의 tail 기여가 $d\Theta/dq$ 에 들어가 ICA tail 로 나타난다.
dimensional charge coordinate 로 바꾸어 읽어야 할 때는 $d\Theta/dQ_\ext=(1/Q_\cell)d\Theta/dq$ 와
$L_Q=Q_\cell L_q$ 를 사용한다.
'@

$text = Replace-Exact $text $icaOld $icaNew 'ICA mapping q'
$text = Replace-Exact $text 'half-cell 측정이면 $V_{n,\app}$ 를 직접 보고, full-cell 이면 식~\eqref{eq:vapp_bridge} 로
anode 기여를 분리해야 한다. voltage-axis tail scale 은 $L_\varphi\simeq|dV_n/dQ|_{q_a}L$.' 'half-cell 측정이면 $V_{n,\app}$ 를 직접 보고, full-cell 이면 식~\eqref{eq:vapp_bridge} 로
anode 기여를 분리해야 한다. voltage-axis tail scale 은 normalized coordinate 에서
$L_\varphi\simeq|dV_n/dq|_{q_a}L_q$ 이며, dimensional coordinate 로는
$L_\varphi\simeq|dV_n/dQ_\ext|_{q_a}L_Q$ 이다.' 'voltage tail scale Lq'

$text = Replace-Exact $text '에 대해 $L$ 이 커진다 $\Rightarrow$ $A_L$ weight 가 large-$L$ 로 이동 $\Rightarrow$' '에 대해 $L_q$ 이 커진다 $\Rightarrow$ $A_L$ weight 가 large-$L_q$ 로 이동 $\Rightarrow$' 'tailT low Lq'
$text = Replace-Exact $text '\item \textbf{High $T$}: $RT$ 증가로 $L$ 이 작아져 $A_L$ 이 short-$L$ 로 이동 $\Rightarrow$' '\item \textbf{High $T$}: $RT$ 증가로 $L_q$ 이 작아져 $A_L$ 이 short-$L_q$ 로 이동 $\Rightarrow$' 'tailT high Lq'
$text = Replace-Exact $text '\item \textbf{Potential assistance}: $W_\psi=\chi_j\mathcal A_j$ 증가 시 $L$ 감소,' '\item \textbf{Potential assistance}: $W_\psi=\chi_j\mathcal A_j$ 증가 시 $L_q$ 감소,' 'tailT assistance Lq'
$text = Replace-Exact $text '\frac{\partial\ln L}{\partial V_{n,\dimedrive}}=-\frac{\chi_j s_{\phi,j}F}{RT}<0\ (\text{forward}),' '\frac{\partial\ln L_q}{\partial V_{n,\dimedrive}}=-\frac{\chi_j s_{\phi,j}F}{RT}<0\ (\text{forward}),' 'tailT derivative Lq'
$text = Replace-Exact $text '즉 potential 이 spectrum 을 short-$L$ 로 shift $\Rightarrow$ tail 단축.' '즉 potential 이 spectrum 을 short-$L_q$ 로 shift $\Rightarrow$ tail 단축.' 'tailT short Lq'
$text = Replace-Exact $text 'tail length scaling 만으로는 부족하다: $L\propto|I|$ 는' 'tail length scaling 만으로는 부족하다: $L_q\propto|I|$ 는' 'falsification Lq proportional'
$text = Replace-Exact $text '$\chi_j$ 를 통해 short-$L$ 로 shift 한다.' '$\chi_j$ 를 통해 short-$L_q$ 로 shift 한다.' 'falsification short Lq'

$fitOld = @'
\textbf{Deliverable.} ICA tail 의 analytic closure 논리식 (평가 순서 inner$\to$outer):
$k(G,T,\psi)$ (식~\eqref{eq:rate}) $\to$ $L(G)$ (식~\eqref{eq:L_of_G}) $\to$ spectrum
$A_L$ (식~\eqref{eq:spectrum}) $\to$ kernel integral $d\Theta_\mathrm{tail}/dq$
(식~\eqref{eq:kernel_integral}, Refs 6/7 closure 식~\eqref{eq:plan_a_closure}) $\to$ $dQ/dV_n$
(식~\eqref{eq:ica}). \textbf{유효범위}: $\Delta G_\eff\ge0$ (Marcus bound), tail 영역
$V_{n,\dimedrive}\approx U_j+O(w_j)$.
'@

$fitNew = @'
\textbf{Deliverable.} Chapter 1이 later quantitative use 로 넘기는 기준식은 먼저 Plan B
baseline 이다:
\[
k(G,T,\psi)\ \xrightarrow{\eqref{eq:rate}}\ 
L_q(G,T,\psi)\ \xrightarrow{\eqref{eq:L_of_G}}\ 
A_L(\lambda;T,\psi)\ \xrightarrow{\eqref{eq:spectrum}}\ 
\mathcal T_j(q;T,\psi)\ \xrightarrow{\eqref{eq:planb_tail}}\ 
\frac{d\Theta_\mathrm{tail}}{dq}\ \xrightarrow{\eqref{eq:ica}}\ 
\frac{dQ_\ext}{dV_n}.
\]
Plan A는 Refs 6/7 ratio-substitution structure 가 M1--M5 와 limiting-case check 를 통과할 때,
self-consistent layer 를 더 compact 하게 쓰는 candidate analytic compression 이다. 따라서 later
fitting expression 은 Plan B baseline 을 항상 보존하고, Plan A는 검증 후 선택적으로 치환한다.
\textbf{유효범위}: $\Delta G_\eff\ge0$ (Marcus bound), tail 영역
$V_{n,\dimedrive}\approx U_j+O(w_j)$.
'@

$text = Replace-Exact $text $fitOld $fitNew 'fitting interface Plan B primary'
$text = Replace-Exact $text '\item single-mode relaxation + exponential kernel $L=|I|/(Q_\cell k)$ (S6/S7, \AL{1},\AL{5}).' '\item single-mode relaxation + exponential kernel $L_q=|I|/(Q_\cell k)$ and dimensional conversion $L_Q=Q_\cell L_q$ (S6/S7, \AL{1},\AL{5}).' 'summary Lq'
$text = Replace-Exact $text '\item ★ 관측 tail = spectrum kernel integral (S9); closure = \textbf{Plan B (conservative theoretical formulation, 항상 보존) + Plan A (Refs 6/7 instantiated analytic closure, M1-M5+$\varepsilon$ gated) +
  R1-R5 governance} (S10, \AL{7}, DQ-v3-2).' '\item ★ 관측 tail = spectrum kernel integral (S9); closure hierarchy = \textbf{Plan B baseline (local residual ODE + spectrum kernel, 항상 보존) + Plan A candidate analytic compression (Refs 6/7, M1-M5+$\varepsilon$ gated) +
  R1-R5 governance} (S10, \AL{7}, DQ-v3-2).' 'summary Plan B primary'

# Remove residual ambiguous generic length phrases outside A_L symbol contexts.
$text = $text.Replace('$L(G)$', '$L_q(G)$')
$text = $text.Replace('large-$L$ 영역', 'large-$L_q$ 영역')
$text = $text.Replace('large-$L$ weight', 'large-$L_q$ weight')
$text = $text.Replace('short-$L$ shift', 'short-$L_q$ shift')

Set-Content -LiteralPath $out -Value ($text -replace "`n", "`r`n") -Encoding UTF8
Copy-Item -LiteralPath $PSCommandPath -Destination $scriptCopy -Force

$hash = (Get-FileHash -LiteralPath $out -Algorithm SHA256).Hash
$lineCount = (Get-Content -LiteralPath $out -Encoding UTF8).Count
"WROTE $out"
"LINES $lineCount"
"SHA256 $hash"
"PLAN $plan"
"SCRIPT $scriptCopy"
