$ErrorActionPreference = 'Stop'

$Root = 'D:\Projects\Project_Anode_Fit\Codex'
$Results = Join-Path $Root 'results'
$Work = Join-Path $Root 'work'
$Source = Join-Path $Results 'graphite_ica_chapter1_rebuilt_v4_consistency_repaired.tex'
$Target = Join-Path $Results 'graphite_ica_chapter1_rebuilt_v5_convention_safe_polish.tex'
$Encoding = [System.Text.UTF8Encoding]::new($false)

New-Item -ItemType Directory -Path $Results -Force | Out-Null
New-Item -ItemType Directory -Path $Work -Force | Out-Null

$script:Text = [System.IO.File]::ReadAllText($Source, $Encoding)
$script:Text = $script:Text -replace "`r`n", "`n"

function Replace-Exact {
    param(
        [Parameter(Mandatory=$true)][string]$Name,
        [Parameter(Mandatory=$true)][string]$Old,
        [Parameter(Mandatory=$true)][string]$New
    )
    if (-not $script:Text.Contains($Old)) {
        throw "Missing exact target: $Name"
    }
    $script:Text = $script:Text.Replace($Old, $New)
}

Replace-Exact -Name 'basis-interpretation-heading' -Old @'
\textbf{해석 정정 (사용자 2026-05-28).} (1) ``가우시안''은 \emph{sharp peak} 를 가리키는
예시이며 equilibrium 형태를 Gaussian 으로 확정한 것이 아니다 → 형태는 grounding 과 data
로 결정. (2) ``activation energy barrier''는 본 이론의 핵심으로 \emph{유지}하되, ``특정
지점을 넘으면 $0\!\to\!1$ 로 갑자기 점프''하는 step-function 식 \emph{비약은 금지} (모든
transition 은 smooth). 본 chapter 는 이 두 정정을 절대 기준으로 한다.
'@ -New @'
\textbf{기준 해석.} (1) ``가우시안''은 \emph{sharp peak} 를 가리키는
예시이며 equilibrium 형태를 Gaussian 으로 확정한 것이 아니다; 형태는 Assumption Ledger 와 data
로 결정한다. (2) ``activation energy barrier''는 본 이론의 핵심으로 \emph{유지}하되, ``특정
지점을 넘으면 $0\!\to\!1$ 로 갑자기 점프''하는 step-function 식 \emph{비약은 금지} (모든
transition 은 smooth). 본 chapter 는 이 두 기준을 절대 기준으로 한다.
'@

Replace-Exact -Name 'surmounting-barrier-language' -Old @'
\textbf{(H2)} 각 local mode 의 진행 속도는 activation barrier $\Delta G_{a}$ 를 통과하는
thermally activated 과정이다 (\AL{1}).
'@ -New @'
\textbf{(H2)} 각 local mode 의 진행 속도는 activation barrier $\Delta G_{a}$ 를 surmount 하는
thermally activated process 이다 (\AL{1}).
'@

Replace-Exact -Name 'refs67-validation-gate' -Old @'
chain 이며, Refs 6/7 은 이 core 를 편리하게 닫는 후보 방법으로만 둔다. \textbf{grounding 주의
(\AL{7})}: 그 기법은 \emph{Fredholm} integral equation of the second kind 를 대상으로
하므로, 본 형식이 \emph{Volterra} 인지 Fredholm 인지에 따른 적용성을 검증 대상(DQ-v3-2)
으로 둔다.
'@ -New @'
chain 이며, Refs 6/7 은 이 core 를 편리하게 닫는 후보 방법으로만 둔다. \textbf{Validation gate
(\AL{7})}: 그 기법은 \emph{Fredholm} integral equation of the second kind 를 대상으로
하므로, 본 형식이 \emph{Volterra} 인지 Fredholm 인지에 따른 적용성을 검증 대상(VG-2)
으로 둔다.
'@

Replace-Exact -Name 'agp-validation-rule' -Old '\textbf{AGP.}' -New '\textbf{Validation rule.}'

Replace-Exact -Name 's10-gated-status' -Old @'
S10 & ★ closure: Plan B (conservative theoretical formulation, 항상 보존) + Plan A (Refs 6/7 candidate analytic closure, gated) + R1-R5 governance & BOUNDED+DQ \AL{7} \\
'@ -New @'
S10 & ★ closure: Plan B (conservative theoretical formulation, 항상 보존) + Plan A (Refs 6/7 candidate analytic closure, gated) + R1-R5 governance & BOUNDED+GATED \AL{7} \\
'@

Replace-Exact -Name 'al7-gated-status' -Old @'
AL-7 & DQ & Refs 6/7 Fredholm / propagator / ratio-substitution method 는 Plan A candidate closure 이며, 적용성 검증 전에는 core assumption 이 아니다. \\
'@ -New @'
AL-7 & GATED & Refs 6/7 Fredholm / propagator / ratio-substitution method 는 Plan A candidate closure 이며, 적용성 검증 전에는 core assumption 이 아니다. \\
'@

Replace-Exact -Name 'al10-satisfy-language' -Old @'
AL-10 & METHOD & competing mechanisms, identifiability, and falsification protocol 을 통과해야 barrier-spectrum 귀속을 주장할 수 있다. \\
'@ -New @'
AL-10 & METHOD & competing mechanisms, identifiability, and falsification protocol 을 만족해야 barrier-spectrum 귀속을 주장할 수 있다. \\
'@

Replace-Exact -Name 'smooth-only-convention-note' -Old @'
는 이를 채택하지 않는다 (사용자 2026-05-28; AGP-3). 단위: $\Delta G$ J/mol, $\Delta G/RT$
'@ -New @'
는 이를 채택하지 않는다 (smooth-only convention). 단위: $\Delta G$ J/mol, $\Delta G/RT$
'@

Replace-Exact -Name 'remove-codex-process-parenthetical' -Old @'
이것이 본 Chapter 의 중심식이다 (Codex 산출물과의 대조에서 채택한 spectrum 관점). single-
'@ -New @'
이것이 본 Chapter 의 중심식이다. single-
'@

Replace-Exact -Name 'falsification-satisfy-language' -Old @'
hypothesis 가 \S\ref{sec:falsify} 의 N3/N4 falsification 을 통과한다는 전제} 하에서다
'@ -New @'
hypothesis 가 \S\ref{sec:falsify} 의 N3/N4 falsification criteria 를 satisfy 한다는 전제} 하에서다
'@

Replace-Exact -Name 'explicit-kernel-chain' -Old @'
\Delta G_\eff \rightarrow k \rightarrow L_q \rightarrow A_L \rightarrow
\int A_L(\lambda)K_\lambda\,d\lambda \rightarrow \text{ICA tail}.
'@ -New @'
\Delta G_\eff \rightarrow k \rightarrow L_q \rightarrow A_L(\lambda;T,\psi) \rightarrow
\int_0^\infty A_L(\lambda;T,\psi)\lambda^{-1}
\exp[-(q-q_a)/\lambda]\,d\lambda \rightarrow \text{ICA tail}.
'@

Replace-Exact -Name 'plan-a-criteria-language' -Old @'
Plan A가 Chapter 1의 analytic closure로 승격되려면 최소한 다음 조건을 통과해야 한다.
'@ -New @'
Plan A가 Chapter 1의 analytic closure로 승격되려면 최소한 다음 criteria 를 satisfy 해야 한다.
'@

Replace-Exact -Name 'tail-falsification-status-language' -Old @'
(O2) 와 \emph{강하게 시사(consistent)} 됨을 보이며, \emph{확정}은 falsification 통과 전제.
'@ -New @'
(O2) 와 \emph{강하게 시사(consistent)} 됨을 보이며, \emph{확정}은 falsification criteria 만족 전제.
'@

Replace-Exact -Name 'plan-a-gated-language' -Old @'
Plan A는 Refs 6/7 ratio-substitution structure 가 M1--M5 와 limiting-case check 를 통과할 때,
'@ -New @'
Plan A는 Refs 6/7 ratio-substitution structure 가 M1--M5 와 limiting-case check 를 satisfy 할 때,
'@

Replace-Exact -Name 'summary-validation-table' -Old @'
\section{종합·grounding 감사·참고문헌}\label{sec:summary}
% ====================================================================
\subsection{결과 요약}
\begin{enumerate}[label=\textbf{(R\arabic*)}]
\item charge conservation 으로 $V_n$ implicit (S1, \AL{9}).
\item equilibrium target 일반형(smooth); lattice-gas grounded 특수해, 형태 data 결정 (S2, \AL{3a}).
\item ★ effective barrier $\Delta G_\eff=\Delta G_a-\chi\mathcal A=G-W_\psi$, Marcus-bounded (S5, \AL{2}).
\item single-mode relaxation + exponential kernel $L_q=|I|/(Q_\cell k)$ and dimensional conversion $L_Q=Q_\cell L_q$ (S6/S7, \AL{1},\AL{5}).
\item ★ barrier distribution $\to$ 지수 매핑 $\to$ relaxation-length spectrum $A_L$ (S8, \AL{6}).
\item ★ 관측 tail = spectrum kernel integral (S9); closure hierarchy = \textbf{Plan B baseline (local residual ODE + spectrum kernel, 항상 보존) + Plan A candidate analytic compression (Refs 6/7, M1-M5+$\varepsilon$ gated) +
  R1-R5 governance} (S10, \AL{7}, DQ-v3-2).
\item ★ stretched tail 의 $T/\psi$ 의존 = spectrum shift (novel; S12, \AL{8}); homogeneous-equilibrium 으로 설명 불가, kinetic-spectrum 강하게 시사 (확정은 falsification 전제).
\item ★ falsification protocol + 비퇴화 discriminator + $\rho_G$ non-unique 역산 회피 (S13, \AL{10}).
\item later fitting interface + identifiability + validation (S14).
\end{enumerate}

\subsection{Grounding 감사 (AGP self-check)}
\begin{longtable}{p{0.6\textwidth} p{0.32\textwidth}}
\toprule 항목 & 상태 \\ \midrule \endhead
모든 본문 assumption 이 AL-\# 인용 & 통과 \\
FLAGGED(AL-3b erf, AL-7 적용성, AL-8 tail) established 미사용 & 통과 \\
BOUNDED(AL-2 Marcus,5 near-eq,6 non-unique) 유효범위 병기 & 통과 \\
step-function/$0\!\to\!1$ 급점프 정의식 부재 & 통과 (smooth only) \\
activation barrier 유지 (사용자 2026-05-28) & 통과 (\S\ref{sec:barrier}) \\
``가우시안''을 형태 확정으로 쓰지 않음 & 통과 (\S\ref{sec:equilibrium}) \\
tail 귀속을 ``확정'' 아닌 ``시사+protocol'' & 통과 (\S\ref{sec:tailT},\ref{sec:falsify}) \\
$\rho_G$ non-unique 역산 회피 (forward only) & 통과 (\S\ref{sec:spectrum},\ref{sec:falsify}) \\
사용자 PhD Refs 6/7 = Plan A analytic closure (M1-M5+ε gated; Plan B core 항상 보존; exact 주장 X) & 통과 (\S\ref{sec:closure}) \\
\bottomrule
\end{longtable}
'@ -New @'
\section{종합·validation status·참고문헌}\label{sec:summary}
% ====================================================================
\subsection{결과 요약}
\begin{enumerate}[label=\textbf{(R\arabic*)}]
\item charge conservation 으로 $V_n$ implicit (S1, \AL{9}).
\item equilibrium target 일반형(smooth); lattice-gas grounded 특수해, 형태 data 결정 (S2, \AL{3a}).
\item ★ effective barrier $\Delta G_\eff=\Delta G_a-\chi\mathcal A=G-W_\psi$, Marcus-bounded (S5, \AL{2}).
\item single-mode relaxation + exponential kernel $L_q=|I|/(Q_\cell k)$ and dimensional conversion $L_Q=Q_\cell L_q$ (S6/S7, \AL{1},\AL{5}).
\item ★ barrier distribution $\to$ 지수 매핑 $\to$ relaxation-length spectrum $A_L$ (S8, \AL{6}).
\item ★ 관측 tail = spectrum kernel integral (S9); closure hierarchy = \textbf{Plan B baseline (local residual ODE + spectrum kernel, 항상 보존) + Plan A candidate analytic compression (Refs 6/7, M1-M5+$\varepsilon$ gated) +
  R1-R5 governance} (S10, \AL{7}, VG-2).
\item ★ stretched tail 의 $T/\psi$ 의존 = spectrum shift (novel; S12, \AL{8}); homogeneous-equilibrium 으로 설명 불가, kinetic-spectrum 강하게 시사 (확정은 falsification criteria 만족 전제).
\item ★ falsification protocol + 비퇴화 discriminator + $\rho_G$ non-unique inversion 회피 (S13, \AL{10}).
\item later fitting interface + identifiability + validation (S14).
\end{enumerate}

\subsection{Assumption and validation status}
\begin{longtable}{p{0.58\textwidth} p{0.34\textwidth}}
\toprule 검증 항목 & 현재 상태 \\ \midrule \endhead
모든 본문 assumption 이 AL-\# 에 연결됨 & documented \\
FLAGGED(AL-3b erf, AL-7 applicability, AL-8 tail) 를 established result 로 쓰지 않음 & controlled as hypothesis \\
BOUNDED(AL-2 Marcus, AL-5 near-equilibrium, AL-6 non-unique inversion) 의 유효범위 병기 & bounded with stated scope \\
step-function/$0\!\to\!1$ 급점프 정의식 부재 & excluded by smooth-only convention \\
activation barrier 유지 & retained as core mechanism (\S\ref{sec:barrier}) \\
``가우시안''을 equilibrium shape 확정으로 쓰지 않음 & treated as descriptive peak-shape example (\S\ref{sec:equilibrium}) \\
tail 귀속을 established result 가 아니라 consistency + falsification protocol 로 둠 & stated as hypothesis with tests (\S\ref{sec:tailT},\ref{sec:falsify}) \\
$\rho_G$ non-unique inversion 회피 & forward model only (\S\ref{sec:spectrum},\ref{sec:falsify}) \\
사용자 PhD Refs 6/7 = Plan A analytic closure candidate & gated by M1-M5+$\varepsilon$; Plan B core preserved (\S\ref{sec:closure}) \\
\bottomrule
\end{longtable}
'@

Replace-Exact -Name 'vg1-label' -Old 'DQ-v3-1' -New 'VG-1'

if ($script:Text -match 'DQ-v3|K_\\lambda|Codex|AGP|2026-05-28') {
    throw 'A targeted process/shorthand marker remains after replacement.'
}

[System.IO.File]::WriteAllText($Target, $script:Text, $Encoding)
Copy-Item -LiteralPath $MyInvocation.MyCommand.Path -Destination (Join-Path $Work 'create_ch1_v5_convention_safe_polish.ps1') -Force

Write-Output "WROTE $Target"
