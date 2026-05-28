$ErrorActionPreference = 'Stop'

$base = 'D:\Projects\Project_Anode_Fit'
$planPath = Join-Path $base 'Codex\plans\2026-05-28-chapter1-v3-canonical-merge-plan.md'
$outPath = Join-Path $base 'Codex\results\graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex'
$claudePath = Join-Path $base 'Claude\docs\graphite_ica_chapter1.tex'
$codexPath = Join-Path $base 'Codex\results\graphite_ica_chapter1_rebuilt_v2_dual_closure.tex'
$comparisonPath = Join-Path $base 'Codex\results\PHASE_012_LATEST_CLAUDE_CODEX_DUAL_CLOSURE_COMPARISON.md'

function Replace-Between {
    param(
        [string]$Text,
        [string]$Start,
        [string]$End,
        [string]$Replacement
    )
    $s = $Text.IndexOf($Start)
    if ($s -lt 0) { throw "Start marker not found: $Start" }
    $e = $Text.IndexOf($End, $s)
    if ($e -lt 0) { throw "End marker not found: $End" }
    $e2 = $e + $End.Length
    return $Text.Substring(0, $s) + $Replacement + $Text.Substring($e2)
}

$plan = @'
# Chapter 1 v3 Canonical Merge Plan

## Summary

사용자 결정에 따라 최신 Claude Chapter 1의 manuscript shell과 최신 Codex Chapter 1의 logic-only dual closure를 병합한다. 목표는 기존 파일을 덮어쓰지 않고 `Codex\results`에 새 canonical merge version을 생성하는 것이다.

## Current Ground Truth

- Active project: `D:\Projects\Project_Anode_Fit`.
- Codex workspace: `D:\Projects\Project_Anode_Fit\Codex`.
- Claude file is reference only and must not be modified.
- Latest comparison report: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_012_LATEST_CLAUDE_CODEX_DUAL_CLOSURE_COMPARISON.md`.
- Canonical direction: Claude publishable structure + Codex no-overclaim logic.
- Current Chapter 1 is theory/logic only. It must not become a solver, fitting workflow, direct numerical fallback, validator workflow, or code design document.

## Phase Range

| Phase | Name | Step Range | Output | Gate |
|---|---|---:|---|---|
| Phase 013 | Chapter 1 v3 canonical merge | 1-12 | `graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex` | `PASS_V3_CANONICAL_MERGE_REVIEWED` |

## Non-goals

- Do not modify `D:\Projects\Project_Anode_Fit\Claude`.
- Do not overwrite Codex v1 or v2 result files.
- Do not implement fitting code or a numerical solver.
- Do not make refs 6/7 load-bearing unless the Fredholm/variable mapping is verified.
- Do not describe Plan B as code fallback.

## Implementation Changes

Create:

- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v3_canonical_merge.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_013_CH1_V3_CANONICAL_MERGE_RESULT.md`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_013_CH1_V3_CANONICAL_MERGE_LEDGER.md`

Read without modification:

- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_chapter1.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_chapter1_rebuilt_v2_dual_closure.tex`
- `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_012_LATEST_CLAUDE_CODEX_DUAL_CLOSURE_COMPARISON.md`

## Phase 013 — Chapter 1 v3 canonical merge

- [ ] Step 1: Confirm latest source file paths and read coverage.
- [ ] Step 2: Use Claude file as structural shell only.
- [ ] Step 3: Replace abstract closure claim with logic-only Plan A/Plan B hierarchy.
- [ ] Step 4: Replace Refs 6/7 load-bearing wording with candidate analytic closure wording.
- [ ] Step 5: Replace S10 spine item with Plan A candidate + Plan B conservative theoretical formulation.
- [ ] Step 6: Replace self-consistent integral closure section with Codex logic-only closure section.
- [ ] Step 7: Preserve Claude strengths: user verbatim, H1-H6, S1-S14, AL tags, graphite staging, voltage bridge, falsification, DOI-rich bibliography.
- [ ] Step 8: Preserve Codex strengths: Plan B as theoretical base, not code fallback; refs 6/7 as method candidate; state/target/rate separation.
- [ ] Step 9: Remove direct-numerical/fallback/validator/switch/floor language from the manuscript body.
- [ ] Step 10: Run static TeX checks.
- [ ] Step 11: Run banned-term and missing-reference checks.
- [ ] Step 12: Save result and ledger.

## Test Plan

- Check file existence.
- Check begin/end count.
- Check brace count.
- Check labels/refs.
- Check cites/bibitems.
- Search for implementation-colored terms: `direct numerical`, `fallback`, `validator`, `switch criterion`, `single-mode floor`.
- Confirm Claude file unchanged by path policy.

## Assumptions

- This phase is a manuscript-level canonical merge, not final literature validation.
- Refs 6/7 remain candidate closure methods until exact equation-class and variable mapping are verified.
- PDF build is optional because xelatex may not be installed in the current environment.

## Correction History

- Supersedes Phase 012 comparison decision by implementing the recommended canonical merge.
'@
Set-Content -LiteralPath $planPath -Value $plan -Encoding UTF8

$tex = Get-Content -LiteralPath $claudePath -Raw -Encoding UTF8
$docStart = $tex.IndexOf('\documentclass')
if ($docStart -lt 0) { throw 'documentclass not found' }
$tex = $tex.Substring($docStart)
$tex = $tex.Replace('Graphite ICA tail — Ch.1 (v4 synthesis)', 'Graphite ICA tail — Chapter 1')
$tex = $tex.Replace('Graphite ICA tail — Ch.1 (v5 merged canonical)', 'Graphite ICA tail — Chapter 1')
$tex = $tex.Replace('pdftitle={Graphite ICA tail: barrier-spectrum kernel-integral theory (Ch.1 v4)}', 'pdftitle={Graphite ICA tail: barrier-spectrum kernel-integral theory}')
$tex = $tex.Replace('pdftitle={Graphite ICA tail: barrier-spectrum kernel-integral theory (Ch.1 v5)}', 'pdftitle={Graphite ICA tail: barrier-spectrum kernel-integral theory}')
$tex = $tex.Replace('pdftitle={Graphite ICA tail: barrier-spectrum kernel-integral theory (Ch.1 v5 merged canonical)}', 'pdftitle={Graphite ICA tail: barrier-spectrum kernel-integral theory}')
$tex = $tex.Replace('Chapter 1 (v4 synthesis, 2026-05-28)', 'Chapter 1')
$tex = $tex.Replace('Chapter 1 (v5 merged canonical, 2026-05-28)', 'Chapter 1')
$tex = $tex.Replace('\date{2026-05-28}', '\date{}')

$newAbstract = @'
\begin{center}\begin{minipage}{0.93\textwidth}
\small \textbf{Abstract.} 리튬이온전지 graphite anode 의 incremental capacity analysis
(ICA), $dQ/dV$ 곡선에서 staging transition peak 뒤의 \emph{post-peak tail} 은 temperature
가 낮을수록 길게 늘어지고(stretched) 높을수록 짧게 끝난다. 본 Chapter 1 은 이 tail 을
\textbf{단일 relaxation length 가 아니라 relaxation-length spectrum 의 kernel integral}
로 해석한다. 출발점은 \textbf{activation free-energy barrier 가 state 를 $0\!\to\!1$ 로
점프시키는 threshold 가 아니라 rate constant 를 정하는 hidden variable} 이라는 점이다.
각 local mode 는 effective barrier $\Delta G_\eff = \Delta G_a-\chi\mathcal A$ 가 정하는
Eyring-type rate 로 equilibrium target 을 향해 smooth relaxation 하며, 하나의 exponential
kernel ($L=v_Q/k$) 을 만든다. 관측 tail 은 barrier distribution $\rho_G$ 가 \emph{지수적
barrier$\to$length 매핑}을 통해 만드는 relaxation-length spectrum $A_L$ 에 대한 kernel
integral 이다. Self-consistent integral closure 는 물리 core 와 분리한다. \textbf{Plan A}는
사용자 박사 연구의 Refs~\cite{lee2011,son2013}에서 온 Fredholm / propagator / ratio-substitution
method가 현재 graphite ICA 구조에 정합할 때만 쓰는 candidate analytic closure 이다.
\textbf{Plan B}는 code route 가 아니라, local residual ODE 와 relaxation-length spectrum
kernel integral로 구성되는 conservative theoretical formulation 이다. Plan A가 검증되지 않아도
Plan B만으로 Chapter 1의 물리 논리, 즉 low temperature 에서 large-$L$ weight가 커지고
potential assistance가 short-$L$ shift를 만든다는 설명은 유지된다. Equilibrium target 의 함수
형태는 특정하지 않고, grounded lattice-gas를 특수해로 둔다. $V_n$ 은 외부 lookup 이 아니라
charge conservation 으로 implicit 결정된다. 모든 assumption 은 Assumption Ledger (AL-\#)로
위치를 표시하고, tail 을 effective barrier에 귀속하기 전에 polarization, transport,
heterogeneous width, charge-transfer co-linearity를 분리하는 falsification protocol을 둔다.
\end{minipage}\end{center}
'@
$tex = Replace-Between $tex '\begin{center}\begin{minipage}{0.93\textwidth}' '\end{minipage}\end{center}' $newAbstract

$tex = $tex.Replace('설명하는 \emph{fitting 가능한 closed-form 논리식}(spectrum kernel integral, Refs 6/7 로
closure)을 도출한다.', '설명하는 \emph{논리식}(spectrum kernel integral 과 conservative theoretical formulation)을 도출한다.')
$tex = $tex.Replace('1안 Refs 6/7 closed-form + 2안 direct (validator) + floor', '1안 Refs 6/7 candidate analytic closure + 2안 conservative theoretical formulation')
$tex = $tex.Replace('★ closure: Plan B (reduced-theory core, 항상 보존) + Plan A (Refs 6/7 closed-form, gated) + R1-R5 governance', '★ closure: Plan B (conservative theoretical formulation, 항상 보존) + Plan A (Refs 6/7 candidate analytic closure, gated) + R1-R5 governance')
$tex = $tex.Replace('사용자 박사 연구의 위치 (Refs 6/7) = kernel integral 의 closure', '사용자 박사 연구의 위치 (Refs 6/7) = candidate analytic closure')
$tex = $tex.Replace('spectrum kernel integral 과 self-consistent relaxation 은 미지 함수가 적분 안팎에 동시에
나타나는 integral equation 을 만든다. 사용자 박사 연구 \cite{lee2011,son2013} 의
\emph{propagator / ratio-substitution} 기법은 이런 적분방정식을 closed-form 으로 닫는
도구이며 (\S\ref{sec:closure}), 본 Chapter 의 load-bearing 수단이다.', 'spectrum kernel integral 과 self-consistent relaxation 은 미지 함수가 적분 안팎에 동시에
나타나는 integral equation 을 만든다. 사용자 박사 연구 \cite{lee2011,son2013} 의
\emph{propagator / ratio-substitution} 기법은 이런 적분방정식에 대해 Plan A candidate analytic
closure 를 제공할 수 있는 수학적 도구다. 그러나 본 Chapter 의 load-bearing 물리 core 는
activation barrier $\to$ rate constant $\to$ relaxation length $\to$ spectrum kernel integral
chain 이며, Refs 6/7 은 이 core 를 편리하게 닫는 후보 방법으로만 둔다.')
$tex = $tex.Replace('본 Chapter 의 load-bearing 수단이다.', '본 Chapter 의 candidate analytic closure 수단이다.')
$tex = $tex.Replace('closure = \textbf{dual-track} (1안 Refs 6/7
  closed-form / 2안 direct numerical validator+fallback / single-mode floor)', 'closure = \textbf{dual-track} (1안 Refs 6/7 candidate analytic closure / 2안 conservative theoretical formulation)')
$tex = $tex.Replace('사용자 PhD Refs 6/7 = kernel closure 1안 (기법 grounded; 적용성은 measured-switch 로 강등, exact 주장 X)', '사용자 PhD Refs 6/7 = Plan A candidate analytic closure (기법은 grounded; 적용성은 equation-class 및 variable mapping 검증 전 exact 주장 X)')

$newClosure = @'
\section{Self-consistent integral 의 closure hierarchy — Plan A / Plan B}\label{sec:closure}
% ====================================================================
\textbf{왜 필요한가.} 식~\eqref{eq:kernel_integral} 은 $A_L$ 을 알면 forward 평가 가능하지만,
$\theta_j$ 와 $V_n$ 이 charge balance (식~\eqref{eq:charge_balance}) 로 결합되어 있어 일반적으로
$\Theta$ 가 적분 안팎에 동시에 나타나는 \emph{self-consistent integral equation} 이 된다.
시간 또는 charge coordinate 적분형은 schematic하게
\begin{equation}
\Theta(q)=\Theta_0+\int_0^q \mathcal K(q,q')\,[\Theta_\eq(q')-\Theta(q')]\,dq'
\label{eq:volterra_self}
\end{equation}
처럼 쓸 수 있다. 여기서 $\mathcal K(q,q')$ 는 식~\eqref{eq:K_def} 의 spectrum kernel 이다.
적분 상한이 $q$ 이므로 원형은 causal memory 를 갖는 Volterra-type second-kind structure 이다.
또한 $\mathcal K$, $\Theta_\eq$, $k$, $A_L$ 은 $V_n$ 에 의존하고, $V_n$ 은 charge balance 로
$\Theta$ 와 다시 연결된다. 이 self-consistency 는 논리 결함이 아니라 graphite ICA 문제의
자연스러운 implicit closure 이다.

\subsection{Closure layer 와 physical core 의 분리}\label{sec:closure_core}
본 장에서 반드시 보존해야 하는 core 는 mathematical shortcut 이 아니라 다음 물리 chain 이다.
\[
\Delta G_\eff \rightarrow k \rightarrow L \rightarrow A_L \rightarrow
\int A_L K_L\,dL \rightarrow \text{ICA tail}.
\]
따라서 closure layer 는 두 가지 역할로 분리한다.
\begin{enumerate}[label=\textbf{I\arabic*.}]
\item \textbf{Physical tail formation.} Activation barrier distribution 이 rate constant
  distribution 으로, 다시 relaxation-length spectrum 으로 바뀌고, 그 spectrum 이 local
  exponential kernel 을 중첩해 observed tail 을 만든다.
\item \textbf{Analytic closure.} $V_n$, $\Theta_\eq$, $k$, $A_L$, $\Theta$ 가 서로 의존하므로,
  paper 또는 later fitting expression 에서 self-consistent integral 을 얼마나 간단한 analytic
  expression 으로 닫을 수 있는지 검토한다.
\end{enumerate}
I1이 Chapter 1의 load-bearing physical logic 이다. I2는 analytic convenience 이며, 특정 closure
method가 성립하지 않아도 I1은 무너지지 않아야 한다. 이 원칙 때문에 본 장은 Plan A와 Plan B를
병기한다.

\begin{center}
\fbox{\parbox{0.92\textwidth}{
\textbf{Plan A.} Fredholm / propagator / ratio-substitution closure 가 현재 graphite ICA
integral structure 에 정합함을 보이면, Refs~\cite{lee2011,son2013} method 를 candidate analytic
closure 로 사용한다.

\textbf{Plan B.} 그 정합성이 증명되지 않거나 Chapter 1 본문에서 analytic closure 를 쓰기 어렵다면,
Refs 6/7 closure 를 핵심식으로 채택하지 않고 local residual ODE + relaxation-length spectrum
kernel integral 을 conservative theoretical formulation 으로 유지한다.
}}
\end{center}

\subsection{Plan A: Refs 6/7 as candidate analytic closure}\label{sec:track1}
사용자의 JCP 2017 paper에서 refs. 6 and 7은 Fredholm integral equation of the second kind를
효율적으로 다루는 propagator / ratio-substitution 계열의 source로 쓰인 것으로 확인되어 있다
\cite{lee2011,son2013}. 이 method가 주는 중요한 guardrail은 다음이다.
\[
\text{self-referential integral equation}
\rightarrow
\text{unknown-function ratio 를 명시}
\rightarrow
\text{controlled approximation of that ratio}
\rightarrow
\text{limiting-case or independent check}.
\]
즉 unknown function 을 조용히 cancel하거나 circular substitution 으로 없애면 안 된다. 어떤 ratio를
어떤 reference solution으로 닫는지, 그 approximation이 어떤 limit에서 유효한지 밝혀야 한다.

Plan A가 Chapter 1의 analytic closure로 승격되려면 최소한 다음 조건을 통과해야 한다.
\begin{enumerate}[label=\textbf{M\arabic*.}]
\item Charge-balance feedback 과 barrier spectrum 을 fixed-domain Fredholm-type second-kind
  equation 으로 재정식화할 수 있어야 한다.
\item Unknown function 이 integral 안팎에 같은 function class 로 나타나야 한다.
\item Ratio-substitution ansatz 가 $\xi_j(s)/\xi_j(Q)$, $r_j(s)/r_j(Q)$, 또는
  $\Theta(s)/\Theta(Q)$ 중 어느 대상에 적용되는지 명시되어야 한다.
\item Single-mode limit 에서 식~\eqref{eq:single_kernel} 의 exponential kernel 로 돌아와야 한다.
\item Closure expression 이 Plan B의 local ODE limit 과 같은 limiting behavior 를 가져야 한다.
\end{enumerate}

이 조건이 성립할 때만, 어떤 effective unknown $Y(Q)$에 대해
\begin{equation}
Y(Q)=Y_0+\int_{\mathcal D}K(Q,S)\,\Phi[Y](S)\,\dd S
\label{eq:closure_general}
\end{equation}
를
\begin{equation}
Y_{\mathrm A}(Q)=
\mathcal C_{\mathrm{ratio}}\!\left[K,\Phi,Y^{\mathrm{ref}}\right](Q)
\label{eq:plan_a_closure}
\end{equation}
와 같은 candidate analytic closure 로 쓸 수 있다. 여기서 $\mathcal C_{\mathrm{ratio}}$ 는
specific ratio-closure operator 이고, 그 detailed form은 graphite ICA의 integral equation class와
variable mapping이 확정된 뒤에만 본문식으로 승격한다. 따라서 Refs 6/7 은 battery-specific
physical assumption 이 아니라 self-consistent integral을 닫는 mathematical method candidate다.

\subsection{Plan B: conservative theoretical formulation}\label{sec:track2}
Plan A의 Fredholm 정식화가 성립하지 않아도 Chapter 1의 physical core는 유지된다. Plan B는
구현상 예비 경로나 code procedure가 아니라, Chapter 1이 항상 보존해야 하는 논리적 기준식이다.
그 구성은 다음 세 식이다.
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
첫 번째 식은 local state 가 equilibrium target 을 finite rate 로 따라가는 residual equation 이다.
두 번째 식은 activation barrier 와 potential assistance 가 relaxation length 로 바뀌는 exponential
mapping 이다. 세 번째 식은 여러 local kernel 의 spectrum mixture 이다. 이 세 식만으로도
\emph{low $T$에서 large-$L$ weight가 커져 tail이 길어지고, positive potential assistance가
short-$L$ shift를 만들어 tail을 줄인다}는 Chapter 1의 핵심 설명은 완결된다.

Plan B가 closed analytic shortcut 을 주지 않는다고 해서 물리 논리가 부족한 것은 아니다. Chapter 1에서
필요한 것은 solver가 아니라 state/target/rate/spectrum 의 logical separation 이다. Plan B는 그
separation을 보존하는 baseline theory 이며, Plan A는 이 baseline 위에 얹히는 candidate analytic
compression 이다.

\subsection{Canonical decision rule}\label{sec:closure_decision}
본 장의 canonical rule은 다음과 같다.
\begin{enumerate}[label=\textbf{R\arabic*.}]
\item Plan A는 validated analytic closure가 될 수 있지만, 검증 전에는 core assumption이 아니다.
\item Plan B는 항상 남는 conservative theoretical base다.
\item 논문 본문에서 Plan A를 사용하더라도 appendix 또는 methods section에는 Plan B derivation과
  limiting-case consistency를 함께 제시한다.
\item Plan A와 Plan B가 같은 limiting cases를 주지 않으면, Chapter 1의 core 논리로는 Plan B
  formulation만 채택한다.
\item 이 dual hierarchy는 coding fallback이 아니라 논리적 책임 분리다.
\end{enumerate}
'@
$closureStartCandidates = @(
    '\section{Self-consistent integral 의 closure — Plan B (core) + Plan A (gated) + governance}\label{sec:closure}',
    '\section{Self-consistent integral 의 closure — dual-track (1안/2안)}\label{sec:closure}'
)
$closureStart = $null
foreach ($candidate in $closureStartCandidates) {
    if ($tex.IndexOf($candidate) -ge 0) {
        $closureStart = $candidate
        break
    }
}
if ($null -eq $closureStart) { throw 'No supported closure section marker found' }
$tex = Replace-Between $tex $closureStart '\section{ICA mapping}\label{sec:ica}' ($newClosure + "`r`n\section{ICA mapping}\label{sec:ica}")

$replacements = @{
    'analytic closed-form' = 'candidate analytic closure'
    'closed-form 논리식' = '논리식'
    'closed-form' = 'analytic closure'
    'direct numerical integration' = 'Plan B theoretical formulation'
    'direct numerical' = 'Plan B theoretical'
    'direct integral' = 'Plan B formulation'
    'direct (validator)' = 'Plan B theoretical formulation'
    'validator' = 'consistency reference'
    'fallback' = 'Plan B'
    'single-mode floor' = 'single-mode limiting case'
    'measured switch' = 'applicability check'
    'switch criterion' = 'applicability criterion'
    '회귀' = '채택'
}
foreach ($key in $replacements.Keys) {
    $tex = $tex.Replace($key, $replacements[$key])
}

$tex = $tex.Replace('fitting 논리식 + identifiability + validation', 'later fitting interface + identifiability + validation')
$tex = $tex.Replace('Fitting 모델, identifiability, validation', 'Later fitting interface, identifiability, validation')
$tex = $tex.Replace('fitting model + identifiability + validation', 'later fitting interface + identifiability + validation')
$tex = $tex.Replace('coding Plan B', 'coding route')
$tex = $tex.Replace('Plan B (reduced-theory
  core, 항상 보존)', 'Plan B (conservative theoretical formulation, 항상 보존)')
$tex = $tex.Replace('solver 구현은 범위 외', 'solver 구현은 Chapter 1 범위 외')
$tex = $tex.Replace('\eqref{eq:closed}', '\eqref{eq:plan_a_closure}')

Set-Content -LiteralPath $outPath -Value $tex -Encoding UTF8

$meta = [ordered]@{
    plan = $planPath
    output = $outPath
    claude_source = $claudePath
    codex_source = $codexPath
    comparison = $comparisonPath
    created = (Get-Date).ToString('s')
}
$meta | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $base 'Codex\results\PHASE_013_CH1_V3_CANONICAL_MERGE_ARTIFACT.json') -Encoding UTF8

Write-Output "PLAN=$planPath"
Write-Output "OUTPUT=$outPath"
