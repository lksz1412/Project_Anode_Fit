# V1013_P21_draft_F1 — v1.0.13 P2.1 드래프트 (드래프터 F1)

- 역할: N=6 경쟁 드래프트 중 F1 (무통신 독립). **드래프트만 — tex/코드 무수정.**
- 원천 정독 범위(전문): `graphite_ica_ch1_v1.0.13.tex` L1–356(preamble·서론·N0·sec:lco-map), L411–520(sec:center·sec:lco-center 머리), L578–917(sec:hys·sec:lco-hys), L918–1139(sec:width·sec:dist), L1380–1489(sec:eqpeak·sec:lco-peak), L2085–2130(MSMR 사전) / `graphite_ica_ch2_v1.0.13.tex` L100–194(warnbox·sec:partition eq:Z1 절).
- figure 개형 전부 실제 식 평가로 생성(스크립트 3종 + PNG 3종, 아래 §4) — assert 검산 + 기존 문서 그림과 교차 일치(spinodal 0.2113/0.7887 = fig:doublewell, 극값 ±1.066 = fig:hysloop).
- 라벨 규약: 신설 = `eq:sm-*`/`sec:sm-*`(갈래 1), `sec:lco-intro`·`sec:lco-direction`·`sec:lco-preview`·`eq:lco-sigmaslot`(갈래 2). 기존 라벨 재사용은 본문에 매번 "(재사용 명시)" 로 표기.

---

## 1. 갈래 1 — Ch1 신설 Part 0 "통계역학 기초" LaTeX 전문

**배치 제안**: 서론(`\section*{서론 …}`) 뒤·`\section{기호와 규약 …}(N0)` 앞. Part 구조(`\part` 또는 절 번호 재조정)와 식 번호 밀림은 master 편입 시 결정 사항. 아래 전문은 ch1 preamble 의 기존 매크로(`\dd`·`\eq`·`\rxn`·`\hys`·`\code`·keybox/signbox 정리환경·tikz 라이브러리)만 사용한다.

```latex
% ====================================================================
\section{통계역학 기초 — 세는 것에서 전위까지 (P0)}\label{sec:sm-basics}
% ====================================================================
본 문건의 평형식은 전부 통계역학의 두 재료 — \emph{미시상태를 센다}$\cdot$\emph{저장조와
접촉시킨다} — 로 환원된다. 이 절은 통계역학을 수강하지 않은 독자를 위해 그 환원을 처음부터
닫는다: 등확률 원리에서 Boltzmann 인자와 분배함수(partition function)를 세우고
(\S\ref{sec:sm-boltzmann}), 화학퍼텐셜 $\mu$ 를 ``입자 1개 추가의 자유에너지 비용''으로 정의해
입자 교환 계의 grand canonical 앙상블(ensemble)로 확장한 뒤(\S\ref{sec:sm-mu}), 삽입 자리
하나(\S\ref{sec:sm-site})$\cdot$$M$ 개(\S\ref{sec:sm-lattice})$\cdot$상호작용
(\S\ref{sec:sm-meanfield})의 사다리로 격자기체(lattice gas)를 쌓고, 전위가 $\mu$ 를 조종하는
손잡이임을 이어(\S\ref{sec:sm-electro}) 거시 열역학 $G\equiv H-TS$ 와 Nernst 식으로 착지한다
(\S\ref{sec:sm-thermo}). 이 사다리의 각 칸이 본론에서 결과로 쓰이는
식~\eqref{eq:mu}$\cdot$\eqref{eq:gxi}$\cdot$\eqref{eq:xieq}$\cdot$\eqref{eq:Uj} 의 출처다 —
본론의 해당 절은 결과 사슬(코드 진행)을 유지하고, 배경 유도는 이 절이 담당한다(재접속은 각
절에 명시). 양자역학은 필요 없다 — 이하의 미시상태는 전부 ``어느 자리가 차 있는가''를 세는
문제다.

\subsection{미시상태와 Boltzmann 인자 — 등확률에서 지수 가중으로}\label{sec:sm-boltzmann}
\textbf{(a) 출발 — 미시상태$\cdot$거시상태$\cdot$등확률 원리.} 미시상태(microstate)는 계의 모든
자유도를 남김없이 지정한 배열 하나다 — 격자라면 ``자리 1 은 참, 자리 2 는 빔, $\dots$''의 목록
하나가 미시상태 하나다. 거시상태(macrostate)는 총 에너지$\cdot$총 입자수처럼 소수의 거시량만
지정하며, 하나의 거시상태에 다수의 미시상태가 속한다. 고립계(에너지 $E$ 고정)의 근본 가정은
\emph{등확률 원리}(principle of equal a priori probabilities) — 접근 가능한 미시상태는 모두 같은
확률 — 이고, 그 수 $\Omega_\mathrm{ms}(E)$ 가 엔트로피를 정의한다:
\begin{equation}
S(E)\;=\;k_B\ln\Omega_\mathrm{ms}(E).
\label{eq:sm-S}
\end{equation}
(기호 유의 — $\Omega_\mathrm{ms}$ 는 미시상태 수로, 본론의 상호작용 에너지 $\Omega_j$ 와
무관하다.) \textbf{(b) 연산 — 열저장조와 접촉한 부분계.} 관심 계(자리 하나여도 된다)가 온도 $T$
의 큰 열저장조(heat reservoir)와 에너지를 교환하고, 계$+$저장조 전체는 고립돼 총 에너지
$E_\mathrm{tot}$ 가 고정이라 하자. 계가 특정 미시상태 $i$(에너지 $E_i$)에 있을 확률은 — 등확률
원리를 전체에 적용하면 — 그때 저장조가 가질 수 있는 미시상태 수에 비례한다:
\begin{equation}
P_i\;\propto\;\Omega_\mathrm{res}(E_\mathrm{tot}-E_i)
\;=\;\exp\!\big[S_\mathrm{res}(E_\mathrm{tot}-E_i)/k_B\big].
\label{eq:sm-Pres}
\end{equation}
\textbf{(c) 중간식 — 저장조 엔트로피의 1차 전개.} 저장조가 크면 $E_i\ll E_\mathrm{tot}$ 라 Taylor
1차로 충분하고, 열역학적 온도의 정의 $\partial S/\partial E\equiv1/T$ 를 쓰면
\begin{equation}
S_\mathrm{res}(E_\mathrm{tot}-E_i)=S_\mathrm{res}(E_\mathrm{tot})-\frac{E_i}{T}+\mathcal O(E_i^2)
\quad\Longrightarrow\quad
P_i\;\propto\;e^{-E_i/k_BT}
\label{eq:sm-taylor}
\end{equation}
($i$-무관 인자 $e^{S_\mathrm{res}(E_\mathrm{tot})/k_B}$ 는 정규화로 흡수된다). \textbf{(d) 박스 —
Boltzmann 분포와 분배함수.} 정규화 상수가 곧 분배함수다:
\begin{equation}
\boxed{\;P_i=\frac{e^{-\beta E_i}}{Z},\qquad Z\equiv\sum_i e^{-\beta E_i},\qquad
\beta\equiv\frac{1}{k_BT}\;.}
\label{eq:sm-boltzmann}
\end{equation}
$e^{-\beta E_i}$ 가 Boltzmann 인자(Boltzmann factor)다 — 에너지가 $k_BT$ 만큼 높은 상태는
$e^{-1}$ 배 덜 나오는데, 그 까닭은 벌칙이 아니라 회계다: 계가 그만큼 에너지를 꾸어 오면
저장조가 그만큼 배열 수를 잃는다(식~\eqref{eq:sm-Pres}). 관측량 평균은
$\langle A\rangle=\sum_iA_iP_i$ 로 닫힌다. 온도의 두 극한이 분포의 두 얼굴이다 —
$\beta\to\infty$($T\to0$)면 최저 에너지 상태만 남고, $\beta\to0$($T\to\infty$)이면 등확률로
돌아간다(에너지 차가 값을 잃는다).

\subsection{화학퍼텐셜 $\mu$ 와 grand canonical — 입자 1개의 값어치}\label{sec:sm-mu}
\textbf{(a) 출발 — $Z$ 에서 자유에너지로, 자유에너지에서 $\mu$ 로.} 분배함수는 정규화 상수를
넘어 열역학 퍼텐셜의 생성함수다. Gibbs 엔트로피 $S=-k_B\sum_iP_i\ln P_i$ 에
식~\eqref{eq:sm-boltzmann} 을 넣으면 $\ln P_i=-\beta E_i-\ln Z$ 라
\begin{equation}
S=\frac{\langle E\rangle}{T}+k_B\ln Z
\quad\Longleftrightarrow\quad
F\;\equiv\;\langle E\rangle-TS\;=\;-k_BT\ln Z
\label{eq:sm-helmholtz}
\end{equation}
— 등온 계의 판정 퍼텐셜인 Helmholtz 자유에너지 $F$ 가 $\ln Z$ 한 줄로 나온다. 입자수 $N$ 을
고정한 계의 $F(T,N)$ 에서, 화학퍼텐셜은 \emph{입자 1개를 더 넣는 데 드는 자유에너지 비용}이다:
\begin{equation}
\mu\;\equiv\;F(T,N+1)-F(T,N)\;\simeq\;\frac{\partial F}{\partial N}\Big|_{T,V}
\label{eq:sm-mudef}
\end{equation}
(몰 단위의 등온$\cdot$등압 형이 본론의 $\mu=\partial G/\partial n|_{T,P}$,
식~\eqref{eq:mudef} — 두 정의의 차가 응축상에서 무시 가능함은 \S\ref{sec:sm-thermo} 에서
확인한다). 값어치라 부르는 까닭 — 두 곳의 $\mu$ 가 다르면 입자는 높은 $\mu$ 에서 낮은 $\mu$
로 옮아 전체 자유에너지를 낮추고, $\mu$ 일치가 입자 교환 평형이다.

\textbf{(b) 연산 — 입자 저장조까지 연 계.} 삽입 자리는 전해질을 통해 Li 저장조(상대극 Li
금속)와 \emph{입자}도 교환한다 — 에너지$\cdot$입자를 모두 여는 것이 grand canonical(대정준)
앙상블이다(그림~\ref{fig:sm-reservoir}). \S\ref{sec:sm-boltzmann}(b)(c)를 두 변수로 반복한다:
계가 (미시상태 $i$, 에너지 $E_i$, 입자수 $N_i$)일 때 저장조 엔트로피를 두 변수로 전개하고,
기본 관계 $\dd E=T\dd S+\mu\,\dd N$ 을 $\dd S$ 로 풀어 얻는 $\partial S/\partial E=1/T$,
$\partial S/\partial N=-\mu/T$ 를 쓰면
\begin{equation}
S_\mathrm{res}(E_\mathrm{tot}-E_i,\ N_\mathrm{tot}-N_i)
=S_\mathrm{res}(E_\mathrm{tot},N_\mathrm{tot})-\frac{E_i}{T}+\frac{\mu N_i}{T}+\cdots
\label{eq:sm-res2}
\end{equation}
\textbf{(c) 중간식 — Gibbs 인자.} 따라서 $P_i\propto e^{-\beta(E_i-\mu N_i)}$ — Boltzmann
인자의 $E_i$ 가 $E_i-\mu N_i$ 로 바뀐 것뿐이며, 이 지수 가중을 Gibbs 인자라 부른다.
\textbf{(d) 박스 — grand canonical 분배함수와 평균 입자수.}
\begin{equation}
\boxed{\;\Xi=\sum_i e^{-\beta(E_i-\mu N_i)},\qquad
P_i=\frac{e^{-\beta(E_i-\mu N_i)}}{\Xi},\qquad
\langle N\rangle=\frac{1}{\beta}\frac{\partial\ln\Xi}{\partial\mu}\;.}
\label{eq:sm-Xi}
\end{equation}
($\langle N\rangle$ 식 검산 — $\partial\ln\Xi/\partial\mu
=\sum_i\beta N_ie^{-\beta(E_i-\mu N_i)}/\Xi=\beta\langle N\rangle$.) 부호가 물리를 말한다 —
$\mu$ 가 높을수록 $e^{+\beta\mu N_i}$ 가 입자 많은 상태를 밀어 올려 계가 채워지고, $\mu$ 가
낮으면 계가 비워진다. 전기화학의 전부는 이 $\mu$ 를 전위로 조종하는 데 있다
(\S\ref{sec:sm-electro}).

\begin{figure}[t]
\centering
\begin{tikzpicture}[font=\scriptsize,
  box/.style={draw,rounded corners=2pt,align=center,inner sep=4pt},
  ar/.style={{Latex[length=1.5mm]}-{Latex[length=1.5mm]},thick}]
\node[box,minimum width=30mm,minimum height=16mm] (sys) {system\\insertion sites\\microstate $i$: $(E_i,\,N_i)$};
\node[box,minimum width=46mm,minimum height=16mm,fill=black!6,right=20mm of sys] (res)
  {reservoir: $T,\ \mu$ fixed\\Li metal counter electrode\\$+$ electrolyte};
\draw[ar] ([yshift=3.2mm]sys.east) -- ([yshift=3.2mm]res.west) node[midway,above] {energy $E$};
\draw[ar] ([yshift=-3.2mm]sys.east) -- ([yshift=-3.2mm]res.west) node[midway,below] {particles $N$ (Li)};
\end{tikzpicture}
\caption{grand canonical 구도(신규). 관심 계(삽입 자리들)는 상대극$\cdot$전해질이 이루는 큰
저장조와 에너지$\cdot$입자를 모두 교환하고, 저장조는 $T$ 와 $\mu$ 를 고정한다. 에너지만 열면
Boltzmann 인자(식~\eqref{eq:sm-boltzmann}), 입자까지 열면 Gibbs 인자
$e^{-\beta(E_i-\mu N_i)}$(식~\eqref{eq:sm-Xi}) — 지수의 자리가 하나 늘어날 뿐 논리는 같다.}
\label{fig:sm-reservoir}
\end{figure}

\subsection{단일 삽입 자리 — 2-상태 문제의 닫힌 점유}\label{sec:sm-site}
\textbf{(a) 출발 — 가장 작은 grand canonical 계.} 삽입 자리 하나를 떼면 미시상태는 단 둘이다 —
빈 자리($n=0$, 에너지 $0$)와 점유 자리($n=1$, 에너지 $\varepsilon_0$). 상태를 세는 것으로
충분하니 식~\eqref{eq:sm-Xi} 를 그대로 쓴다. \textbf{(b) 연산 — 두 항 합.}
\begin{equation}
\Xi_1=\sum_{n=0,1}e^{-\beta(\varepsilon_0-\mu)n}=1+e^{-\beta(\varepsilon_0-\mu)}
\label{eq:sm-Z1}
\end{equation}
— Chapter 2 의 단일 자리 분배함수(그 문건 식 (eq:Z1))$\cdot$본론 \S\ref{sec:dist} 의
식~\eqref{eq:partfn} 과 같은 식이다(재사용 명시 — 그 두 곳이 딛는 기초가 본 절이다).
\textbf{(c) 중간식 — 평균 점유.} 점유 상태의 확률 가중을 $\Xi_1$ 로 나누면(또는
식~\eqref{eq:sm-Xi} 의 로그 미분)
\begin{equation}
\theta\;\equiv\;\langle n\rangle
=\frac{0\cdot1+1\cdot e^{-\beta(\varepsilon_0-\mu)}}{\Xi_1}
=\frac{e^{-\beta(\varepsilon_0-\mu)}}{1+e^{-\beta(\varepsilon_0-\mu)}}.
\label{eq:sm-occmid}
\end{equation}
\textbf{(d) 박스 — 점유의 닫힌 꼴.} 분자$\cdot$분모를 $e^{-\beta(\varepsilon_0-\mu)}$ 로 나누면
\begin{equation}
\boxed{\;\theta(\mu,T)=\frac{1}{1+e^{\beta(\varepsilon_0-\mu)}}\;.}
\label{eq:sm-occ}
\end{equation}
본론 \S\ref{sec:dist} 의 식~\eqref{eq:fermifn} 그대로다(재사용 명시). Fermi--Dirac 분포와
동형인 것은 우연이 아니라 ``한 자리에 입자 0 또는 1''이라는 배타 점유의 공통 대수다 — 단
\emph{함수형 동형이지 물리량 동일이 아니다}: 여기 ``입자''는 Li 이고, 전자 준위 점유와의 다리는
\S\ref{sec:lco-electronic} 가 놓는다. 그림~\ref{fig:sm-occ}(좌)가 이 함수다 —
$\varepsilon_0=\mu$ 에서 정확히 $\theta=\tfrac12$(득실 균형), $T$ 가 낮을수록 계단, 높을수록
완만.

한 걸음 더 — $n\in\{0,1\}$ 라 $n^2=n$ 이므로 점유의 요동(분산)이 닫힌 꼴로 나온다:
\begin{equation}
\mathrm{var}(n)=\langle n^2\rangle-\langle n\rangle^2=\theta(1-\theta),
\qquad
\frac{\partial\theta}{\partial(\beta\mu)}=\theta(1-\theta)
\label{eq:sm-flucres}
\end{equation}
(둘째 식 검산 — 식~\eqref{eq:sm-occ} 을 $\mu$ 로 미분하면 $\partial\theta/\partial\mu
=\beta e^{\beta(\varepsilon_0-\mu)}/[1+e^{\beta(\varepsilon_0-\mu)}]^2=\beta\,\theta(1-\theta)$).
\emph{점유의 $\mu$-감도 $=$ 점유 요동} — 요동--응답(fluctuation--response) 관계의 최소
사례다. 본론 peak 모양 $\xi_\eq(1-\xi_\eq)$(식~\eqref{eq:belliden})의 통계적 정체가 바로 이
분산이다: $\dd Q/\dd V$ 봉우리는 ``점유가 가장 심하게 요동하는 전위''에서 선다
($\mu$ 가 $V$ 에 선형으로 묶이는 \S\ref{sec:sm-electro} 에서 이 문장이 식이 된다).

\subsection{$M$ 독립 자리 — lattice gas 와 섞임 엔트로피}\label{sec:sm-lattice}
\textbf{(a) 출발 — 독립 자리의 곱 구조.} 동등한 자리 $M$ 개가 서로 상호작용하지 않으면
미시상태는 자리별 점유의 목록 $(n_1,\dots,n_M)$ 이고, 에너지$\cdot$입자수는 합
$\sum_k\varepsilon_0n_k,\ \sum_kn_k$ 다. Gibbs 인자가 자리별 곱으로 갈라져 grand canonical 합이
인수분해된다:
\begin{equation}
\Xi_M=\sum_{n_1=0,1}\cdots\sum_{n_M=0,1}\ \prod_{k=1}^{M}e^{-\beta(\varepsilon_0-\mu)n_k}
=\big(\Xi_1\big)^M,
\qquad
\langle N\rangle=\frac{1}{\beta}\frac{\partial\ln\Xi_M}{\partial\mu}=M\theta
\label{eq:sm-ZM}
\end{equation}
— 자리 하나의 답(식~\eqref{eq:sm-occ})이 그대로 거시 점유율이 된다. 독립이라 분산도 더해져
$\mathrm{var}(N)=M\,\theta(1-\theta)$(식~\eqref{eq:sm-flucres} 의 합). ``동등한 자리에 입자가
차고 빈다''는 이 모형이 격자기체(lattice gas)이며, 본론 \S\ref{sec:hys} 가 흑연 staging 전이를,
\S\ref{sec:lco-hys} 가 LCO 팔면체 Li 자리를 이 모형으로 읽는다.

\textbf{(b) 연산 — 같은 답의 canonical 경로: 경우의 수 세기.} 입자수를 $N=M\theta$ 로
\emph{고정}하고(canonical) 자유에너지를 직접 세어도 같은 곳에 닿아야 한다 — 그 확인이 섞임
엔트로피를 준다. $N$ 개를 $M$ 자리에 놓는 경우의 수와 Stirling 근사($\ln m!\simeq m\ln m-m$)로
\begin{equation}
W=\binom{M}{N},\qquad
\ln W\simeq M\ln M-N\ln N-(M-N)\ln(M-N)
\label{eq:sm-W}
\end{equation}
(Stirling 의 1차 항 $-M+N+(M-N)$ 은 상쇄). $N=M\theta$ 를 넣고 $\ln M$ 몫을 정리하면 로그가
점유율의 두 몫으로 갈라진다:
\begin{equation}
S_\mathrm{mix}=k_B\ln W=-k_BM\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big].
\label{eq:sm-Smix}
\end{equation}
\textbf{(c) 중간식 — 자리 1몰당 자유에너지와 $\mu(\theta)$.} 자리 1몰($M=N_A$,
$N_Ak_B=R$) 기준의 자유에너지 밀도는 에너지 몫 $\varepsilon\theta$($\varepsilon\equiv
N_A\varepsilon_0$, 몰당 자리 에너지)와 $-TS_\mathrm{mix}$ 의 합이고, 화학퍼텐셜
정의~\eqref{eq:sm-mudef} 를 조성 미분으로 쓰면
\begin{equation}
\bar g_\mathrm{id}(\theta)=\varepsilon\theta+RT\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big],
\qquad
\mu(\theta)=\frac{\partial\bar g_\mathrm{id}}{\partial\theta}
=\varepsilon+RT\ln\frac{\theta}{1-\theta}
\label{eq:sm-muideal}
\end{equation}
(로그 몫 미분 $\ln\theta+1-\ln(1-\theta)-1=\ln[\theta/(1-\theta)]$).
\textbf{(d) 박스 — 두 경로의 일치.} 식~\eqref{eq:sm-muideal} 를 $\theta$ 로 풀면
\begin{equation}
\boxed{\;\mu(\theta)=\varepsilon+RT\ln\frac{\theta}{1-\theta}
\quad\Longleftrightarrow\quad
\theta(\mu)=\frac{1}{1+e^{(\varepsilon-\mu)/RT}}\;}
\label{eq:sm-logit}
\end{equation}
— 몰 언어($R$, $\varepsilon$ [J/mol])로 적힌 식~\eqref{eq:sm-occ} 그대로다(자리당
$k_B,\varepsilon_0$ ↔ 몰당 $R=N_Ak_B,\ \varepsilon=N_A\varepsilon_0$; 지수는 비라 환산에
불변). 입자수를 고정하고 세든(canonical) 저장조에 열든(grand canonical), 큰 $M$ 에서 같은
$\theta(\mu)$ 에 닿는다 — 앙상블 동등성(ensemble equivalence)의 이 문제에서의 구체 확인이다.
극한의 부호도 물리와 맞는다: $\theta\to0$ 이면 $\mu\to-\infty$(첫 입자는 섞임 엔트로피가 거저
끌어들인다), $\theta\to1$ 이면 $\mu\to+\infty$(마지막 빈자리를 채우는 값은 지수적으로 비싸다)
— 로그 몫이 채움의 양끝을 잠그는 이 구조가 뒤의 모든 등온선 꼬리를 만든다.
```

```latex
\subsection{Mean-field 상호작용 $\Omega$ — $\mu(\theta)$ 와 정규용액 $g(\xi)$}\label{sec:sm-meanfield}
\textbf{(a) 출발 — 이웃 상호작용의 평균장 치환.} 실제 자리들은 독립이 아니다 — 점유된 이웃
쌍마다 상호작용 에너지 $u$ 가 붙는다($u<0$ 이 동종 인력). 배열마다 이웃 쌍 수가 달라 정확한
합은 닫히지 않으므로, 각 자리의 이웃 $z_c$ 개가 \emph{평균 점유율 $\theta$ 로} 차 있다고
치환하는 것이 mean-field(평균장; Bragg--Williams) 근사다. 점유 쌍 수 $\simeq(Mz_c/2)\theta^2$
(쌍 이중계산 방지의 $\tfrac12$)이라 자리 1몰당 상호작용 에너지는
\begin{equation}
\bar e_\mathrm{int}(\theta)=\frac{z_c\,u\,N_A}{2}\,\theta^2\;\equiv\;c\,\theta^2.
\label{eq:sm-eint}
\end{equation}
\textbf{(b) 연산 — $\theta^2$ 의 항등 분해.} $\theta^2=\theta-\theta(1-\theta)$ 로 가르면
\begin{equation}
c\,\theta^2=c\,\theta+\Omega\,\theta(1-\theta),\qquad
\Omega\equiv-c=-\frac{z_c\,u\,N_A}{2}
\label{eq:sm-omega}
\end{equation}
— 선형 몫 $c\theta$ 는 자리 에너지의 재정의($\varepsilon\mapsto\varepsilon+c$; 이하 그 재정의
상수를 본론 표기 $\mu^0$ 로 적는다)로 흡수되고, 조성에 비선형인 물리는 $\Omega\theta(1-\theta)$
하나에 남는다. 부호 사슬 — 동종 인력 $u<0\Rightarrow c<0\Rightarrow\Omega>0$: 인력이면 같은
종끼리 뭉치는 쪽(상분리)이 유리한데, 그것이 아래에서 혼합 조성을 위로 미는
$+\Omega\theta(1-\theta)$ 로 나타난다. \textbf{(c) 중간식 — 자유에너지와 $\mu(\theta)$.}
식~\eqref{eq:sm-muideal} 의 이상 몫에 얹으면
\begin{equation}
\bar g(\theta)=\mu^0\theta+RT\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big]
+\Omega\,\theta(1-\theta),
\label{eq:sm-gtheta}
\end{equation}
\begin{equation}
\mu(\theta)=\frac{\partial\bar g}{\partial\theta}
=\mu^0+RT\ln\frac{\theta}{1-\theta}+\Omega\,(1-2\theta)
\label{eq:sm-mu}
\end{equation}
($\theta(1-\theta)$ 의 미분 $=1-2\theta$). 식~\eqref{eq:sm-mu} 는 본론 \S\ref{sec:hys} 의
격자기체 화학퍼텐셜 식~\eqref{eq:mu} \emph{그 자체}다(재사용 명시 — 본론은 전이별 첨자
$\Omega_j$$\cdot$종 표기 $\mu_\mathrm{Li}$ 로 적으며, 그 절의 압축 유도가 딛는 전 단계들이 본
절이다). 그림~\ref{fig:sm-mu} 가 이 함수의 세 얼굴이다 — $\Omega=0$ 단조,
$\Omega=2RT$ 중심 평탄, $\Omega=4RT$ 비단조(한 $\mu$ 에 세 $\theta$).
\textbf{(d) 박스 — 진행률 좌표의 정규용액 자유에너지.} 진행률 $\xi=1-\theta$ 로 옮기면 로그
몫과 $\theta(1-\theta)=\xi(1-\xi)$ 몫이 자리바꿈에 대칭이라 조성 몫의 꼴이 불변이고,
직선(선형$+$상수) 몫을 $g^0$ 으로 묶으면
\begin{equation}
\boxed{\;g(\xi)=g^0+RT\big[\xi\ln\xi+(1-\xi)\ln(1-\xi)\big]+\Omega\,\xi(1-\xi)\;}
\label{eq:sm-gxi}
\end{equation}
— 본론 식~\eqref{eq:gxi} 다(재사용 명시). 섞임 엔트로피는 이상(ideal)으로 두고 에너지만 2차
평균장으로 넣은 이 최소 모형의 고전 이름이 정규용액(regular solution) 모형이다. 곡률이 문턱을
만든다 — $g''(\xi)=RT/[\xi(1-\xi)]-2\Omega$(본론 식~\eqref{eq:gpp})의 최솟값은 $\xi=\tfrac12$
에서 $4RT-2\Omega$ 이므로, $\Omega\le2RT$ 면 전 구간 볼록(단상 고용체)이고 $\Omega>2RT$ 면
가운데가 오목해져 이중웰이 된다(그림~\ref{fig:sm-gxi}). 오목 경계(spinodal)의 닫힌 근과
그것이 낳는 히스테리시스 gap 은 본론 \S\ref{sec:hys}
(식~\eqref{eq:spinodal}$\cdot$\eqref{eq:dUhys})가 닫는다 — Part 0 은 문턱 $\Omega=2RT$
까지만 세운다.

\begin{figure}[t]
\centering
\begin{tikzpicture}[x=9.6cm,y=6.4cm]
\draw[-{Latex[length=1.6mm]}] (-0.02,0) -- (1.06,0) node[below,font=\scriptsize] {$\xi$};
\draw[-{Latex[length=1.6mm]}] (-0.02,-0.76) -- (-0.02,0.13)
  node[above,font=\scriptsize] {$g_\mathrm{mix}(\xi)/RT$};
\foreach \xx in {0.25,0.5,0.75} {\draw (\xx,0.006) -- (\xx,-0.006) node[below,font=\scriptsize] {\xx};}
\draw (-0.014,-0.693) -- (-0.026,-0.693) node[left,font=\scriptsize] {$-\ln2$};
% Omega/RT = 0
\draw[thin] plot[smooth] coordinates {(0.005,-0.03148) (0.016,-0.08203) (0.027,-0.1242) (0.038,-0.1615) (0.049,-0.1956) (0.06,-0.227) (0.08,-0.2788) (0.12,-0.3669) (0.16,-0.4397) (0.2,-0.5004) (0.24,-0.5511) (0.28,-0.593) (0.32,-0.6269) (0.36,-0.6534) (0.4,-0.673) (0.44,-0.6859) (0.48,-0.6923) (0.52,-0.6923) (0.56,-0.6859) (0.6,-0.673) (0.64,-0.6534) (0.68,-0.6269) (0.72,-0.593) (0.76,-0.5511) (0.8,-0.5004) (0.84,-0.4397) (0.88,-0.3669) (0.92,-0.2788) (0.94,-0.227) (0.951,-0.1956) (0.962,-0.1615) (0.973,-0.1242) (0.984,-0.08203) (0.995,-0.03148)};
% Omega/RT = 1
\draw[densely dashdotted] plot[smooth] coordinates {(0.005,-0.0265) (0.016,-0.06629) (0.027,-0.09788) (0.038,-0.125) (0.049,-0.149) (0.06,-0.1706) (0.08,-0.2052) (0.12,-0.2613) (0.16,-0.3053) (0.2,-0.3404) (0.24,-0.3687) (0.28,-0.3914) (0.32,-0.4093) (0.36,-0.423) (0.4,-0.433) (0.44,-0.4395) (0.48,-0.4427) (0.52,-0.4427) (0.56,-0.4395) (0.6,-0.433) (0.64,-0.423) (0.68,-0.4093) (0.72,-0.3914) (0.76,-0.3687) (0.8,-0.3404) (0.84,-0.3053) (0.88,-0.2613) (0.92,-0.2052) (0.94,-0.1706) (0.951,-0.149) (0.962,-0.125) (0.973,-0.09788) (0.984,-0.06629) (0.995,-0.0265)};
% Omega/RT = 2 (threshold)
\draw[densely dashed] plot[smooth] coordinates {(0.005,-0.02153) (0.016,-0.05055) (0.027,-0.07161) (0.038,-0.08842) (0.049,-0.1024) (0.06,-0.1142) (0.08,-0.1316) (0.12,-0.1557) (0.16,-0.1709) (0.2,-0.1804) (0.24,-0.1863) (0.28,-0.1898) (0.32,-0.1917) (0.36,-0.1926) (0.4,-0.193) (0.44,-0.1931) (0.48,-0.1931) (0.52,-0.1931) (0.56,-0.1931) (0.6,-0.193) (0.64,-0.1926) (0.68,-0.1917) (0.72,-0.1898) (0.76,-0.1863) (0.8,-0.1804) (0.84,-0.1709) (0.88,-0.1557) (0.92,-0.1316) (0.94,-0.1142) (0.951,-0.1024) (0.962,-0.08842) (0.973,-0.07161) (0.984,-0.05055) (0.995,-0.02153)};
% Omega/RT = 3 (double well)
\draw[thick] plot[smooth] coordinates {(0.005,-0.01655) (0.016,-0.0348) (0.027,-0.04534) (0.038,-0.05187) (0.049,-0.05576) (0.06,-0.05777) (0.08,-0.05797) (0.12,-0.05012) (0.16,-0.03647) (0.2,-0.0204) (0.24,-0.00388) (0.28,0.01185) (0.32,0.02593) (0.36,0.03778) (0.4,0.04699) (0.44,0.05327) (0.48,0.05645) (0.52,0.05645) (0.56,0.05327) (0.6,0.04699) (0.64,0.03778) (0.68,0.02593) (0.72,0.01185) (0.76,-0.00388) (0.8,-0.0204) (0.84,-0.03647) (0.88,-0.05012) (0.92,-0.05797) (0.94,-0.05777) (0.951,-0.05576) (0.962,-0.05187) (0.973,-0.04534) (0.984,-0.0348) (0.995,-0.01655)};
% spinodal marks on Omega/RT=3
\fill (0.2113,-0.0157) circle (0.5pt) node[below left,font=\scriptsize] {$\xi_s^-$};
\fill (0.7887,-0.0157) circle (0.5pt) node[below right,font=\scriptsize] {$\xi_s^+$};
% curve labels
\node[font=\scriptsize] at (0.5,-0.645) {$\Omega/RT=0$};
\node[font=\scriptsize] at (0.5,-0.395) {$1$};
\node[font=\scriptsize] at (0.5,-0.150) {$2$ (threshold)};
\node[font=\scriptsize] at (0.5,0.095) {$3$ (double well)};
\end{tikzpicture}
\caption{정규용액 섞임 자유에너지 $g_\mathrm{mix}(\xi)/RT=\xi\ln\xi+(1-\xi)\ln(1-\xi)
+(\Omega/RT)\,\xi(1-\xi)$ 의 $\Omega$ 의존(식~\eqref{eq:sm-gxi}; 신규 — 좌표 전부 식 평가,
스크립트 \code{V1013\_P21\_fig\_F1\_sm\_gxi.py}). $\Omega=0$ 은 순수 섞임 엔트로피
(중심 $-\ln2$), $\Omega=2RT$ 가 볼록성 경계($g''(\tfrac12)=0$), $\Omega=3RT$ 는 이중웰 — 점이
spinodal $\xi_s^\pm=\tfrac12(1\pm\sqrt{1-2RT/\Omega})=0.211/0.789$
(본론 식~\eqref{eq:spinodal}$\cdot$그림~\ref{fig:doublewell} 과 일치). 이중웰의 결과(분기 gap)는
\S\ref{sec:hys} 가 닫는다.}
\label{fig:sm-gxi}
\end{figure}

\begin{figure}[t]
\centering
\begin{tikzpicture}[x=9.6cm,y=0.60cm]
\draw[-{Latex[length=1.6mm]}] (-0.02,0) -- (1.06,0) node[below,font=\scriptsize] {$\theta$};
\draw[-{Latex[length=1.6mm]}] (-0.02,-4.3) -- (-0.02,4.4)
  node[above,font=\scriptsize] {$(\mu-\mu^0)/RT$};
\foreach \xx in {0.25,0.5,0.75} {\draw (\xx,0.07) -- (\xx,-0.07) node[below,font=\scriptsize] {\xx};}
\foreach \yy in {-4,-2,2,4} {\draw (-0.014,\yy) -- (-0.026,\yy) node[left,font=\scriptsize] {\yy};}
% Omega/RT = 0
\draw[thin] plot[smooth] coordinates {(0.02,-3.892) (0.036,-3.288) (0.052,-2.903) (0.068,-2.618) (0.084,-2.389) (0.1,-2.197) (0.13,-1.901) (0.1689,-1.593) (0.2079,-1.338) (0.2468,-1.116) (0.2858,-0.9159) (0.3247,-0.7321) (0.3637,-0.5594) (0.4026,-0.3945) (0.4416,-0.2348) (0.4805,-0.07793) (0.5195,0.07793) (0.5584,0.2348) (0.5974,0.3945) (0.6363,0.5594) (0.6753,0.7321) (0.7142,0.9159) (0.7532,1.116) (0.7921,1.338) (0.8311,1.593) (0.87,1.901) (0.9,2.197) (0.916,2.389) (0.932,2.618) (0.948,2.903) (0.964,3.288) (0.98,3.892)};
% Omega/RT = 2 (threshold)
\draw[densely dashed] plot[smooth] coordinates {(0.02,-1.972) (0.036,-1.432) (0.052,-1.111) (0.068,-0.8898) (0.084,-0.7252) (0.1,-0.5972) (0.13,-0.421) (0.1689,-0.2689) (0.2079,-0.1692) (0.2468,-0.1029) (0.2858,-0.05908) (0.3247,-0.03103) (0.3637,-0.01415) (0.4026,-0.005038) (0.4416,-0.001072) (0.4805,-3.942e-05) (0.5195,3.942e-05) (0.5584,0.001072) (0.5974,0.005038) (0.6363,0.01415) (0.6753,0.03103) (0.7142,0.05908) (0.7532,0.1029) (0.7921,0.1692) (0.8311,0.2689) (0.87,0.421) (0.9,0.5972) (0.916,0.7252) (0.932,0.8898) (0.948,1.111) (0.964,1.432) (0.98,1.972)};
% Omega/RT = 4 (van der Waals loop)
\draw[thick] plot[smooth] coordinates {(0.02,-0.05182) (0.036,0.4244) (0.052,0.6809) (0.068,0.8382) (0.084,0.9388) (0.1,1.003) (0.13,1.059) (0.1689,1.055) (0.2079,0.9992) (0.2468,0.9097) (0.2858,0.7978) (0.3247,0.67) (0.3637,0.5311) (0.4026,0.3844) (0.4416,0.2326) (0.4805,0.07786) (0.5195,-0.07786) (0.5584,-0.2326) (0.5974,-0.3844) (0.6363,-0.5311) (0.6753,-0.67) (0.7142,-0.7978) (0.7532,-0.9097) (0.7921,-0.9992) (0.8311,-1.055) (0.87,-1.059) (0.9,-1.003) (0.916,-0.9388) (0.932,-0.8382) (0.948,-0.6809) (0.964,-0.4244) (0.98,0.05182)};
% extrema (= spinodal) on Omega/RT=4
\fill (0.1464,1.0657) circle (0.5pt) node[above,font=\scriptsize] {$\theta_s^-$};
\fill (0.8536,-1.0657) circle (0.5pt) node[below,font=\scriptsize] {$\theta_s^+$};
% curve labels
\node[font=\scriptsize] at (0.115,-3.05) {$\Omega=0$};
\node[font=\scriptsize] at (0.155,-1.55) {$\Omega=2RT$};
\node[font=\scriptsize] at (0.10,1.75) {$\Omega=4RT$};
\end{tikzpicture}
\caption{격자기체 화학퍼텐셜 $(\mu(\theta)-\mu^0)/RT=\ln[\theta/(1-\theta)]+(\Omega/RT)(1-2\theta)$
의 개형(식~\eqref{eq:sm-mu}; 신규 — 좌표 전부 식 평가, 스크립트
\code{V1013\_P21\_fig\_F1\_sm\_mu.py}). $\Omega=0$ 단조(로그 몫이 양끝을 잠금), $\Omega=2RT$
에서 중심 기울기 $0$(문턱), $\Omega=4RT$ 는 비단조 — 한 $\mu$ 에 세 $\theta$ 가 대응하는
van der Waals loop 이고 극값(점)이 spinodal $\theta_s^\pm=0.146/0.854$, 값 $\pm1.066$.
\S\ref{sec:hys} 그림~\ref{fig:hysloop} 의 $V_\eq(\xi)$ 곡선은 이 곡선의 $\theta=1-\xi\cdot$부호
반전 거울이라 같은 $\pm1.066$ 이 나타난다(식~\eqref{eq:eqcond} 의 $\mu\mapsto V$ 환산).}
\label{fig:sm-mu}
\end{figure}

\subsection{전기화학 연결 — 전위가 $\mu$ 를 조종한다: $\xi_\eq$ logistic}\label{sec:sm-electro}
\textbf{(a) 출발 — 전기화학 퍼텐셜과 삽입 평형.} 하전 입자의 값어치에는 전기 일이 더해진다 —
전하수 $z$ 인 종이 내부 전위 $\phi$ 인 상에 있으면 1몰당 값어치는
\begin{equation}
\tilde\mu\;\equiv\;\mu+zF\phi
\label{eq:sm-echem}
\end{equation}
(전기화학 퍼텐셜)가 균형의 대상이다. 삽입 반응
$\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\mathrm{host})}$ 의 평형은 양변 값어치
일치 $\tilde\mu_{\mathrm{Li}^+}+\tilde\mu_{e^-}=\tilde\mu_\mathrm{Li}$
(본론 식~\eqref{eq:eqbalance}; 재사용 명시)이고, 전자 항은 $z=-1$ 이라 측정 전위 $V$ 를 통해
$\tilde\mu_{e^-}=\mu_{e^-}^0-FV$ 로 들어온다. \textbf{(b) 연산 — 상수 덩이의 $U$ 흡수.}
좌변에서 전위 의존은 $-FV$ 뿐이고 나머지(Li$^+$ 활동도$\cdot$기준 퍼텐셜)는 주어진 $T$ 에서
상수라, 그 덩이를 $sFU$($s=+1$ — \S\ref{sec:notation} 의 유도 전용 고정 부호로, 방향 부호
$\sigma_d$ 와 별개)로 묶으면 평형 조건이
\begin{equation}
\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF\,(V-U)
\label{eq:sm-eqcond}
\end{equation}
— 본론 식~\eqref{eq:eqcond} 다(재사용 명시). 이 식이 손잡이의 교체다:
\S\ref{sec:sm-mu} 까지는 $\mu$ 가 손잡이였다면, 전지에서는 전위 $V$ 가 그 손잡이를 돌린다 —
$V$ 를 올리면 전자의 값어치가 내려가 삽입 Li 의 평형 값어치도 내려가고, 계는 Li 를 내놓는다
(탈리튬화). \textbf{(c) 중간식 — 이상 등온선의 등치.} 격자기체 쪽 값어치는
식~\eqref{eq:sm-mu} 가 준다. 먼저 $\Omega=0$(이상)에서 두 값어치를 등치하면(양변의 $\mu^0$
상쇄)
\begin{equation}
RT\ln\frac{\theta_\eq}{1-\theta_\eq}=-sF\,(V-U)
\quad\Longrightarrow\quad
\theta_\eq=\frac{1}{1+e^{+sF(V-U)/RT}},\qquad
\xi_\eq=1-\theta_\eq=\frac{1}{1+e^{-sF(V-U)/RT}}.
\label{eq:sm-isotherm}
\end{equation}
\textbf{(d) 박스 — logistic 평형 점유(이상 극한).} 열에너지의 전위 환산 $w\equiv RT/F$
($25.7$ mV @ $298$ K)로 묶으면
\begin{equation}
\boxed{\;\xi_\eq(V,T)=\frac{1}{1+\exp\!\big[-s\,(V-U)/w\big]},\qquad w\equiv\frac{RT}{F}\;.}
\label{eq:sm-xieq}
\end{equation}
본론의 작업식~\eqref{eq:xieq} 는 이 식의 세 자리 일반화다(재사용 명시 — 고정 부호 $s\mapsto$
방향 부호 $\sigma_d$ 는 \S\ref{sec:notation}, 중심 $U\mapsto$ 분기 중심 $U_j^{\,d}$ 는
\S\ref{sec:hys}, 폭 $w\mapsto w_j=n_jRT/F$ 는 \S\ref{sec:width} 소관) — Part 0 은 그 일반화를
재수록하지 않는다. grand canonical 경로와의 재확인 — 식~\eqref{eq:sm-occ} 에 몰 환산
($\beta(\varepsilon_0-\mu)\mapsto(\varepsilon-\mu)/RT$, 식~\eqref{eq:sm-logit})과 전이 중심 기준
$\varepsilon-\mu^0\equiv0$, 식~\eqref{eq:sm-eqcond} 를 넣으면 $(\varepsilon-\mu)/RT
=sF(V-U)/RT$ 라 같은 logistic 이다(Chapter 2 의 식 (eq:muV)$\to$(eq:logistic) 대응). 요동
다리도 닫힌다 — $\mu$ 가 $V$ 에 선형이라 $|\dd\xi_\eq/\dd V|=(F/RT)\,\xi_\eq(1-\xi_\eq)$, 곧
식~\eqref{eq:sm-flucres} 의 점유 분산이 그대로 $\dd Q/\dd V$ 종(본론 식~\eqref{eq:belliden})
이다. $\Omega\ne0$ 이면 등치가 닫힌 $\xi_\eq(V)$ 로 풀리지 않고 암시적 곡선 $V_\eq(\xi)$ 로
남는데, 그것이 본론 식~\eqref{eq:Veq} 이고 $\Omega>2RT$ 의 비단조성(그림~\ref{fig:sm-mu})이
히스테리시스의 씨앗이다(\S\ref{sec:hys}). 마지막으로 상보 경로 — 본론 \S\ref{sec:width} 는
같은 $\xi_\eq$ 를 속도식의 정지점(detailed balance, 식~\eqref{eq:db})에서 얻는다: 평형
통계역학(본 절)과 동역학 정지점이 같은 분포에 닿는 것이 \S\ref{sec:dist} 가 닫은 ``두
얼굴''이다. 그림~\ref{fig:sm-occ}(우)가 이 절의 결과다.

\begin{signbox}
\textbf{부호(Part 0).} $s=+1$: $V\!\uparrow\Rightarrow\mu_\mathrm{Li}\!\downarrow$
(식~\eqref{eq:sm-eqcond})$\Rightarrow\theta_\eq\!\downarrow,\ \xi_\eq\!\uparrow$ — 전위를
올리면 탈리튬화가 진행한다(본론 규약 일치). $V=U\Rightarrow\theta_\eq=\xi_\eq=\tfrac12$.
$T\to0$: 계단($w\to0$), $T\to\infty$: 완전 퍼짐($w\to\infty$). 방향 부호 $\sigma_d$ 의 세
작용처는 본론 \S\ref{sec:notation}$\cdot$\S\ref{sec:signcheck} 소관 — Part 0 은 $s=+1$ 고정.
\end{signbox}

\begin{figure}[t]
\centering
\begin{tikzpicture}
\begin{scope}[x=0.50cm,y=2.4cm]
% ---- (a) dimensionless single-site occupancy ----
\draw[-{Latex[length=1.6mm]}] (-6.6,0) -- (7.0,0)
  node[below,font=\scriptsize] {$(\varepsilon_0-\mu)/k_BT_0$};
\draw[-{Latex[length=1.6mm]}] (-6.6,0) -- (-6.6,1.18) node[above,font=\scriptsize] {$\theta$};
\foreach \xx in {-4,-2,2,4} {\draw (\xx,0.013) -- (\xx,-0.013) node[below,font=\scriptsize] {\xx};}
\draw (-6.54,1.0) -- (-6.66,1.0) node[left,font=\scriptsize] {1};
\draw (-6.54,0.5) -- (-6.66,0.5) node[left,font=\scriptsize] {0.5};
\draw[densely dotted,gray] (-6.6,0.5) -- (6.6,0.5);
% T = T0/2
\draw[thick,densely dotted] plot[smooth] coordinates {(-6,1) (-5,1) (-4,0.9997) (-3.5,0.9991) (-3,0.9975) (-2.5,0.9933) (-2,0.982) (-1.5,0.9526) (-1,0.8808) (-0.5,0.7311) (0,0.5) (0.5,0.2689) (1,0.1192) (1.5,0.04743) (2,0.01799) (2.5,0.006693) (3,0.002473) (3.5,0.0009111) (4,0.0003354) (5,4.54e-05) (6,6.144e-06)};
% T = T0
\draw[thick] plot[smooth] coordinates {(-6,0.9975) (-5.5,0.9959) (-5,0.9933) (-4.5,0.989) (-4,0.982) (-3.5,0.9707) (-3,0.9526) (-2.5,0.9241) (-2,0.8808) (-1.5,0.8176) (-1,0.7311) (-0.5,0.6225) (0,0.5) (0.5,0.3775) (1,0.2689) (1.5,0.1824) (2,0.1192) (2.5,0.07586) (3,0.04743) (3.5,0.02931) (4,0.01799) (4.5,0.01099) (5,0.006693) (5.5,0.00407) (6,0.002473)};
% T = 2T0
\draw[thick,densely dashed] plot[smooth] coordinates {(-6,0.9526) (-5.5,0.9399) (-5,0.9241) (-4.5,0.9047) (-4,0.8808) (-3.5,0.852) (-3,0.8176) (-2.5,0.7773) (-2,0.7311) (-1.5,0.6792) (-1,0.6225) (-0.5,0.5622) (0,0.5) (0.5,0.4378) (1,0.3775) (1.5,0.3208) (2,0.2689) (2.5,0.2227) (3,0.1824) (3.5,0.148) (4,0.1192) (4.5,0.09535) (5,0.07586) (5.5,0.06009) (6,0.04743)};
\node[font=\scriptsize,align=left] at (3.6,0.82)
  {dotted: $T=T_0/2$\\ solid: $T=T_0$\\ dashed: $T=2T_0$};
\node[font=\scriptsize] at (0,-0.30) {(a)};
\end{scope}
\begin{scope}[xshift=8.9cm,x=33cm,y=2.4cm]
% ---- (b) electrochemical dress: xi_eq(V), theta_eq(V) ----
\draw[-{Latex[length=1.6mm]}] (-0.006,0) -- (0.215,0) node[below,font=\scriptsize] {$V$ [V]};
\draw[-{Latex[length=1.6mm]}] (-0.006,0) -- (-0.006,1.18)
  node[above,font=\scriptsize] {$\xi_\eq,\ \theta_\eq$};
\foreach \xx in {0.05,0.1,0.15,0.2}
  {\draw (\xx,0.013) -- (\xx,-0.013) node[below,font=\scriptsize] {\xx};}
\draw[densely dotted] (0.085,0) -- (0.085,1.0);
\node[below,font=\scriptsize] at (0.085,-0.10) {$U$};
% xi_eq, T=268.15 K
\draw[thick,densely dotted] plot[smooth] coordinates {(0,0.02464) (0.008,0.03448) (0.016,0.04806) (0.024,0.06662) (0.032,0.09165) (0.04,0.1248) (0.048,0.1678) (0.056,0.2218) (0.064,0.2872) (0.072,0.3629) (0.08,0.4461) (0.088,0.5324) (0.096,0.6168) (0.104,0.6947) (0.112,0.7629) (0.12,0.8198) (0.128,0.8654) (0.136,0.9009) (0.144,0.9278) (0.152,0.9478) (0.16,0.9625) (0.168,0.9732) (0.176,0.9809) (0.184,0.9864) (0.192,0.9903) (0.2,0.9932)};
% xi_eq, T=298.15 K
\draw[thick] plot[smooth] coordinates {(0,0.03529) (0.008,0.04756) (0.016,0.06383) (0.024,0.08516) (0.032,0.1128) (0.04,0.1479) (0.048,0.1915) (0.056,0.2444) (0.064,0.3063) (0.072,0.3761) (0.08,0.4515) (0.088,0.5292) (0.096,0.6054) (0.104,0.6769) (0.112,0.7409) (0.12,0.7961) (0.128,0.8421) (0.136,0.8792) (0.144,0.9086) (0.152,0.9314) (0.16,0.9488) (0.168,0.962) (0.176,0.9719) (0.184,0.9792) (0.192,0.9847) (0.2,0.9887)};
% xi_eq, T=328.15 K
\draw[thick,densely dashed] plot[smooth] coordinates {(0,0.04716) (0.008,0.06163) (0.016,0.08017) (0.024,0.1037) (0.032,0.133) (0.04,0.1692) (0.048,0.2127) (0.056,0.2639) (0.064,0.3224) (0.072,0.3871) (0.08,0.4559) (0.088,0.5265) (0.096,0.596) (0.104,0.6619) (0.112,0.7221) (0.12,0.7752) (0.128,0.8206) (0.136,0.8586) (0.144,0.8896) (0.152,0.9145) (0.16,0.9342) (0.168,0.9496) (0.176,0.9615) (0.184,0.9707) (0.192,0.9778) (0.2,0.9832)};
% theta_eq = 1 - xi_eq, T=298.15 K
\draw[gray,thick] plot[smooth] coordinates {(0,0.9647) (0.008,0.9524) (0.016,0.9362) (0.024,0.9148) (0.032,0.8872) (0.04,0.8521) (0.048,0.8085) (0.056,0.7556) (0.064,0.6937) (0.072,0.6239) (0.08,0.5485) (0.088,0.4708) (0.096,0.3946) (0.104,0.3231) (0.112,0.2591) (0.12,0.2039) (0.128,0.1579) (0.136,0.1208) (0.144,0.09142) (0.152,0.06864) (0.16,0.05122) (0.168,0.03803) (0.176,0.02814) (0.184,0.02077) (0.192,0.0153) (0.2,0.01125)};
\node[font=\scriptsize] at (0.163,0.72) {$\xi_\eq$};
\node[gray,font=\scriptsize] at (0.033,0.70) {$\theta_\eq=1-\xi_\eq$};
\node[font=\scriptsize,align=left] at (0.175,0.30)
  {dotted: 268 K\\ solid: 298 K\\ dashed: 328 K};
\node[font=\scriptsize] at (0.1,-0.30) {(b)};
\end{scope}
\end{tikzpicture}
\caption{단일 자리 점유와 그 전기화학 옷(신규 — 좌표 전부 식 평가, 스크립트
\code{V1013\_P21\_fig\_F1\_sm\_occ.py}). (a) 식~\eqref{eq:sm-occ} 의 $\theta$ —
$\varepsilon_0=\mu$ 에서 $\tfrac12$, 낮은 $T$ 일수록 계단($\beta\to\infty$), 높은 $T$ 일수록
완만($\beta\to0$ 이면 $\tfrac12$ 로 퍼짐). (b) 식~\eqref{eq:sm-xieq} 의 $\xi_\eq(V)$
($U=0.085$ V, stage $2\!\to\!1$ 초기값) — 폭 $w=RT/F$ 가 $23.1/25.7/28.3$ mV
($268/298/328$ K)로 $T$ 에 비례해 열리고, 회색 $\theta_\eq=1-\xi_\eq$ 와 중심 $V=U$ 에서
교차한다($\tfrac12$).}
\label{fig:sm-occ}
\end{figure}

\subsection{거시 열역학 연결 — $G\equiv H-TS$$\cdot$$\Delta G_j=-sFU_j$$\cdot$Nernst}
\label{sec:sm-thermo}
\textbf{(a) 출발 — $F$ 에서 $G$ 로.} 통계역학이 준 퍼텐셜은 등온$\cdot$등적의
$F=-k_BT\ln Z$(식~\eqref{eq:sm-helmholtz})다. 전지 실험은 등온$\cdot$등압이라 판정 퍼텐셜은
Gibbs 자유에너지 $G\equiv H-TS=F+PV$(본론 식~\eqref{eq:gibbsdef}; 재사용 명시)이지만, 응축상
전극에서 두 퍼텐셜의 차 $P\Delta V$ 는 대기압$\times$몰부피 변화의 차수로 $\sim1$ J/mol
수준(차수 추정)이라 반응 스케일 수만 J/mol 앞에서 무시 가능하고, $G\simeq F$ 로 옮겨 탄다.
따라서 \S\ref{sec:sm-mu} 의 $\mu=\partial F/\partial N|_{T,V}$ 는 본론의
$\mu=\partial G/\partial n|_{T,P}$(식~\eqref{eq:mudef}; 재사용 명시)와 같은 값어치다.
\textbf{(b) 연산 — 반응 자유에너지와 $U_j$.} 전이 $j$ 의 비배치 몫 반응 자유에너지는
$G\equiv H-TS$ 의 반응 차 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 이고, 평형
조건~\eqref{eq:sm-eqcond} 의 상수 덩이 정의가 이를 전위로 환산한다:
\begin{equation}
\Delta G_j=-sF\,U_j
\label{eq:sm-dGU}
\end{equation}
(본론 식~\eqref{eq:eqcond} 우측 항의 재사용 — $U_j>0\Leftrightarrow\Delta G_j<0$, 전이가 자발
진행할 전위가 양의 중심이다). \textbf{(c) 중간식 — 온도 환산 다리.} 둘을 이으면
$\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}=-FU_j$($s=1$), 곧 본론
식~\eqref{eq:Ujmid}$\to$\eqref{eq:Uj} 의 $U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$ 와
온도 계수 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 가 그대로 나온다 — 박스 재수록 없이
\S\ref{sec:center} 로 넘긴다. \textbf{(d) 박스 — Nernst 형 등온선.} 식~\eqref{eq:sm-xieq} 를
$V$ 로 뒤집으면
\begin{equation}
\boxed{\;V(\xi)=U_j+\frac{RT}{sF}\,\ln\frac{\xi}{1-\xi}\;}
\label{eq:sm-nernst}
\end{equation}
— 활동도비의 로그를 갖는 교과서 Nernst 식의 격자기체 형이며, 본론 식~\eqref{eq:Veq} 의
$\Omega=0$ 극한(Chapter 2 의 식 (eq:Vxi))이다(재사용 명시). 로그 몫은 곡선맞춤이 아니라 섞임
엔트로피~\eqref{eq:sm-Smix} 의 부분몰 미분(식~\eqref{eq:sm-muideal})이다 — 미시상태
세기(\S\ref{sec:sm-boltzmann})가 거시 전위 곡선의 꼬리 모양까지 정한다는 것이 Part 0 전체의
착지점이다.

\begin{keybox}
\textbf{Part 0 사다리.} 등확률~\eqref{eq:sm-S} $\to$ Boltzmann$\cdot$$Z$~\eqref{eq:sm-boltzmann}
$\to$ $\mu\cdot$grand canonical~\eqref{eq:sm-Xi} $\to$ 단일 자리 $\theta$~\eqref{eq:sm-occ}
$\to$ lattice gas$\cdot$섞임 엔트로피~\eqref{eq:sm-Smix} $\to$ 평균장
$\Omega$~\eqref{eq:sm-mu}$\cdot$\eqref{eq:sm-gxi} $\to$ 전위 손잡이~\eqref{eq:sm-eqcond} $\to$
logistic~\eqref{eq:sm-xieq}$\cdot$Nernst~\eqref{eq:sm-nernst}. 본론이 결과로 쓰는 평형식
(식~\eqref{eq:mu}$\cdot$\eqref{eq:gxi}$\cdot$\eqref{eq:xieq}$\cdot$\eqref{eq:Uj})의 전 유도가 이
여덟 칸에 있다 — 이후 절은 같은 사다리를 결과 사슬(코드 진행 N0--N9) 순서로 다시 밟는다.
\end{keybox}
```

---

## 2. 재접속 표 — Part 0 신설 후 원천 절 유도의 흡수·참조 지도

| # | 원천(절·줄·라벨) | 내용 | Part 0 대응 | 처리 제안 (최소 diff) |
|---|---|---|---|---|
| 1 | ch1 §sec:center (a) L417–447: eq:gibbsdef·eq:mudef·eq:eqbalance·eq:eqcond | G·μ 정의, 전기화학 평형 조건 | P0.6 eq:sm-echem·eq:sm-eqcond / P0.7 (a) | **잔존**(N2 결과 사슬 진입점). (a) 머리에 1줄 추가: "두 정의와 평형 조건의 통계역학적 기원은 \S sm-mu·sm-electro·sm-thermo." 라벨·박스 이동 없음 |
| 2 | ch1 §sec:center U_j(T) L448–474: eq:Ujmid·eq:Uj | ΔG→U_j 온도 환산 | P0.7 (b)(c) 다리 | **잔존** — Part 0 은 박스 재수록 없이 전방 참조만 |
| 3 | ch1 §sec:hys (a) L586–597: eq:mu 도출부(Stirling·평균장 cθ²) | 격자기체 μ(θ) 압축 유도 | P0.4 eq:sm-Smix·eq:sm-muideal + P0.5 eq:sm-eint~eq:sm-mu (전 단계 전개) | **축약 가능(옵션)**: L587–593 압축 유도 문단을 "유도 전체는 \S sm-lattice·sm-meanfield" 1줄로 대체 가능. eq:mu 식·라벨은 원위치 유지(결과 사슬 보존). 미축약 시에도 모순 없음(중복 서술만) |
| 4 | ch1 §sec:hys L598–620: eq:gxi·eq:gpp·eq:spinodal | 정규용액 g(ξ)·곡률·spinodal | P0.5 eq:sm-gxi(=eq:gxi 재유도)·곡률 문턱(인라인, eq:gpp 참조) | **잔존** — spinodal 근·gap 닫힌꼴(eq:spinodal·eq:dUhys)은 sec:hys 전속. Part 0 은 문턱 Ω=2RT 까지만 세움(역할 분담 명시적) |
| 5 | ch1 §sec:width ξ_eq L953–993: eq:bv·eq:db·eq:logisticsolve·eq:xieq | detailed balance(동역학 정지점) 경로 | P0.6 이 평형 경로로 상보(같은 logistic) | **전량 잔존** — 동역학 경로는 Part 0 범위 밖. 절 머리에 1줄 추가 옵션: "평형 통계 경로의 배경은 \S sm-electro" |
| 6 | ch1 §sec:dist L1066–1112: eq:partfn·eq:fermifn | 단일 자리 grand canonical 점유 분포 | P0.3 eq:sm-Z1(=eq:partfn)·eq:sm-occ(=eq:fermifn) | **축약 가능(옵션)**: (a)(b) 유도 두 단계(L1073–1087)를 "\S sm-site 의 식 sm-Z1·sm-occ 재호출" 1–2줄로 대체 가능. (c)(d) 통합 서술·keybox(분포 다리)는 잔존 — sec:dist 의 고유 기여는 '두 경로의 통합'이지 유도가 아님 |
| 7 | ch2 §sec:partition L110–188: eq:Z1·eq:occ·eq:muV·eq:logistic·eq:Vxi | 단일 자리→logistic·Nernst (Ch2 자체 기초) | P0.3·P0.6·P0.7 과 동형 | **잔존(장 독립성 유지)** — Ch2 는 자체 완결 장. 도입에 1줄 참조 옵션: "확장 배경은 Ch1 Part 0". Ch2 keybox 의 폭 이중지위·두-상 한정 서술은 Part 0 과 무충돌(Part 0 은 단상·이상 극한만 박스) |
| 8 | ch1 §sec:eqpeak eq:belliden | 종 항등식 ξ(1−ξ) | P0.3 eq:sm-flucres(분산 정체)·P0.6 요동 다리 | **잔존** — Part 0 은 통계적 정체(분산=요동-응답)만 추가 제공, 식 재수록 없음 |

**재접속 원칙**(교훈 카드 ④ 준수): Part 0 은 배경 유도를 전담하고 본론 결과 사슬(N0–N9)의 어떤 박스·라벨도 이동·재수록하지 않는다. 표의 "축약 가능(옵션)" 두 곳(#3·#6)만이 실제 diff 후보이며, 적용 여부는 master 결정 — 미적용 시에도 물리 모순은 발생하지 않는다(중복 유도가 남을 뿐).

## 3. 갈래 2 — Part II "LCO 양극" 도입 절 LaTeX 문안

**일원화 대상**: 현행 §sec:lco-map(L301–355) 전문 + §sec:lco-hys 의 "★분기 부호의 전극-중립 읽기" 문단(L846–854) + §sec:lco-peak 의 "★방향 부호의 전극-중립 읽기" 문단·각주(L1426–1437). **배치 제안**: Part II(LCO 절 군)의 머리. LCO 절들의 물리적 이동 여부와 무관하게 단독 절로도 성립한다(참조는 전부 기존 라벨).

```latex
% ====================================================================
\section{Part II 도입 — LCO 양극: 전극-중립 골격과 방향 규약}\label{sec:lco-intro}
% ====================================================================
Part I(흑연)이 세운 forward 골격은 처음부터 전극을 가리지 않도록 설계되었다. 이 절은 그
골격을 두 번째 전극 $\mathrm{LiCoO_2}$(LCO) 양극에 걸기 전에, Part II 전체가 전제할 세 가지 —
무엇이 전극 무관인가(\S\ref{sec:lco-map}), 방향 부호를 어떻게 먹이는가
(\S\ref{sec:lco-direction}), 종반의 MSMR 동형은 어떤 모양으로 닫히는가
(\S\ref{sec:lco-preview}) — 를 한 곳에 고정한다. 이하 Part II 의 LCO 절들은 이 규약을
전제하고 각자의 자리에서 적용만 한다.

\subsection{전극-중립 골격 — 무엇이 전극 무관인가}\label{sec:lco-map}
골격의 전극-중립성은 다섯 곳에서 성립한다: (i) 실험조건 매핑 — 방향 부호$\cdot$전류 환산
식~\eqref{eq:n0map}; (ii) 전이 문법 — 인덱스 $j$$\cdot$진행률 $\xi_j$$\cdot$용량 가중
$Q_j$$\cdot$전하 보존 합산(\S\ref{sec:eqpeak}); (iii) 평형 중심의 Gibbs 환산
식~\eqref{eq:Uj} — 유도의 어느 다리에도 host 고유 항이 없다(\S\ref{sec:lco-center}(a) 의 세
진입 확인); (iv) 정규용액 틀 식~\eqref{eq:gxi} — 가정은 ``동등한 자리에 리튬이 차고 빈다''
하나(\S\ref{sec:lco-hys}); (v) logistic 평형 종 식~\eqref{eq:xieq} 과 그 미분의 종 항등식
식~\eqref{eq:belliden}. host 의 화학 정체는 상수 $\mu^0$ 와 전이별 입력값으로만 들어온다.

% ── 이하 4개 문단 + 표 = 기존 sec:lco-map(L302–355) 전문 이동(무수정) ──
% 조정 3곳만(전부 위치-정합용, 물리·수치·부호 무변경):
%   [조정1] 문두 "지금까지의"→"Part I 까지의",
%   [조정2] "(아래 모든 흑연 식·표·부호는 불변)"→"(모든 …)" — 흑연 식이 이제 위(Part I)에 있음,
%   [조정3] 말미 "다음 절들은 흑연으로 식을 세운 뒤 LCO 파라미터를 끼우는 순서로 간다"
%           →"Part I 은 흑연으로 식을 세웠고 Part II 의 절들은 LCO 파라미터를 끼워 넣는 순서로 간다".
Part I 까지의 기호와 매핑은 \emph{전극을 가리지 않는다} — 식~\eqref{eq:n0map} 의 방향
부호$\cdot$전류 환산, 전이 인덱스 $j$, 진행률 $\xi_j$, 평형 중심 $U_j$ 는 삽입형 전극이면
어디서나 같은 골격이다. 이 절은 같은 골격을 두 번째 사례인 $\mathrm{LiCoO_2}$(LCO) 양극에
\emph{건다}. 흑연 서술은 한 줄도 바뀌지 않으며(모든 흑연 식$\cdot$표$\cdot$부호는 불변), LCO 는
``파라미터를 갈아 끼우고 고유 항 하나를 더하는'' 두 번째 전극으로 들어온다. 본 문건이 다루는
범위는 \emph{코인 하프셀}(LCO vs Li metal) 단독이다 — 전셀 합성
($\partial U_\cell=\partial U_\mathrm{cat}-\partial U_\mathrm{an}$)은 범위 밖이며(후속), 단전극
부호와 전셀 부호를 섞지 않는다.

\textbf{양극 부호 규약(흑연과 1:1 대칭).} LCO 하프셀 전위는 vs Li/Li$^+$ 로 $\sim$3.9--4.2 V
영역에 있다 — 흑연 음극의 $\sim$0.1 V 와 달리 \emph{높은} 전위다. 그러나 부호 골격은 같다:
방전($\sigma_d=+1$)은 LCO 입장에서 \emph{리튬화}(Li$^+$ 가 LCO 로 들어와
Co$^{4+}\!\to$Co$^{3+}$ 환원, $x$ 증가, 전위 하강)이고, 충전($\sigma_d=-1$)은 \emph{탈리튬화}
($x$ 감소, 전위 상승)이다. 평형 중심의 온도 의존 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$
(식~\eqref{eq:Uj} 미분)는 부호까지 흑연과 동일한 관계식이며, 부호의 \emph{값}만 전이별
$\Delta S_{\rxn,j}^\mathrm{cat}$ 가 정한다(\S\ref{sec:lco-center}). 흑연에서 $\xi_j$ 가 탈리튬화
진행이었듯, LCO 양극에서 충전(탈리튬화)이 $\xi:0\!\to\!1$ 의 주 진행 방향이다 — 본 문건의
LCO 전이표는 그 충전(탈리튬화) 진행을 전위 오름차순으로 적는다.

흑연의 \code{GRAPHITE\_STAGING\_LIT}(표~\ref{tab:staging})에 대응하는 LCO 초기값 리스트를
\code{LCO\_MSMR\_LIT} 로 둔다 — 표~\ref{tab:lco-staging} 가 그 세 전이다. 흑연이 4 staging
전이를 남기듯, LCO 하프셀(코인, $\le$4.2--4.5 V)은 세 전이를 남긴다\cite{xia2007}: $\sim$3.90 V
의 절연체$\to$금속 천이(metal--insulator transition, MIT), $\sim$4.05 V 와 $\sim$4.17 V 의 한 쌍
order--disorder 전이다(고전압 $\sim$4.55 V 의 O3$\to$H1-3 는 하프셀 상한이 $\le$4.2--4.5 V 면
범위 밖이라 옵션으로 둔다). 이 값들은 흑연과 마찬가지로 \emph{신뢰값이 아니라 초기값}이며
(tier — 1차 문헌 Xia\cite{xia2007}$\cdot$Reynier\cite{reynier2004}$\cdot$
Motohashi\cite{motohashi2009} 에서 읽은 출발점), 우리 시료 데이터로 피팅해 override 하는
전제다.

% (표 tab:lco-staging — L325–348 원문 그대로 이동, 캡션·수치·라벨 무수정 전량 보존:)
\begin{table}[t]
\centering\footnotesize
\renewcommand{\arraystretch}{1.3}
\caption{LCO 하프셀 전이 초기값 \code{LCO\_MSMR\_LIT}(3건, vs Li metal) — 출발점, 피팅으로 override. $x$ 는
$\mathrm{Li}_x\mathrm{CoO_2}$ 의 리튬 함량. ``성격''은 상전이 유형, ``전자항''은 \S\ref{sec:lco-electronic} 의 MIT
게이트 발현 여부. 흑연 표~\ref{tab:staging} 와 같은 자리(전위$\cdot$성격$\cdot\Delta S$), 양극 부호.
★코드 \code{LCO\_MSMR\_LIT} 시연값($U{=}3.930/3.880/4.050$ V, $x_\mathrm{MIT}{=}0.50$, 전자항을 중간 dict 에 배정)은
\emph{tier-C placeholder} 로, 본 표의 물리 anchor(T1 MIT $\sim$3.90 V$\cdot x_\mathrm{MIT}{\approx}0.85\cdot$T3 $\sim$4.17 V)와 별개이며
round-trip 피팅으로 정합한다(피팅 시 전자항은 T1=MIT dict 로 재정렬). 또한 현 구현은 $\Delta S_e$ 를 기준온도 $T_\mathrm{ref}$ 에서
동결한 상수 오프셋으로 넣어(단일-기준 근사) 봉우리를 목표 전위에 두며, 조성 좌표 $x{=}x(\xi_\mathrm{eq}(V))$ 매핑과
$\Delta S_e{\propto}T$ 의 다온도 $T^2$ 곡률(식~\eqref{eq:U1T2})은 다온도 round-trip 피팅 단계의 과제로 분리한다.}
\label{tab:lco-staging}
\begin{tabular}{@{}p{0.155\textwidth} c p{0.085\textwidth} p{0.165\textwidth} p{0.255\textwidth} p{0.115\textwidth}@{}}
\toprule
전이 & $U_j$ [V] & $x$ 범위 & 성격 & $\Delta S_{\rxn,j}^\mathrm{cat}$ 초기값 & 전자항 \\
\midrule
T1 (MIT)              & $\sim$3.90        & 0.94--0.75 & insulator$\to$metal       & config $+\,\Delta S_e$ 게이트 ON & \textbf{발현(핵심)} \\
T2 (order--disorder a)& $\sim$4.05        & $\approx$0.55 & hex$\to$monoclinic 정렬 & config 주도($\approx$0.47 J/K\,mol) & off \\
T3 (order--disorder b)& $\sim$4.17--4.20  & $\approx$0.48 & monoclinic$\to$hex      & config($\approx$1.49 J/K\,mol) & off \\
\midrule
(T4)                  & $\sim$4.55        & $\approx$0.2 & O3$\to$H1-3              & --- & (고전압, 범위 밖) \\
\bottomrule
\end{tabular}
\end{table}

흑연이 \code{GRAPHITE\_STAGING\_LIT} 의 $(\Delta H_\rxn,\Delta S_\rxn,Q,\Omega,\Delta H_a,\dots)$
키를 전이별로 갖듯, LCO 전이도 같은 키 구조를 갖되 값만 표~\ref{tab:lco-staging} 의 양극
영역으로 바뀐다. 단 하나의 구조적 차이는 T1 에 흑연엔 없는 \emph{전자 엔트로피 항}
$\Delta S_e(x,T)$ 가 더해지는 것이며(MIT 고유), 이것이 \S\ref{sec:lco-electronic} 의 새 절이다.
그 전까지(N1--N5)는 흑연과 LCO 가 \emph{같은 식}을 공유하므로, Part I 은 흑연으로 식을
세웠고 Part II 의 절들은 LCO 파라미터를 끼워 넣는 순서로 간다.

\subsection{방향 규약 — $\sigma_d$ 입력 슬롯의 물리 내용은 탈리튬화 여부다}
\label{sec:lco-direction}
방향 부호 $\sigma_d$ 가 모델에 들어가는 작용처는 셋이다 — 분극(\S\ref{sec:pol}), 분기 중심
선택(\S\ref{sec:hys}), 꼬리 지지 방향(\S\ref{sec:tail}). 세 작용처 모두에서 이 부호의 물리
내용은 셀 방향 라벨이 아니라 \emph{탈리튬화(산화) 진행 $=+1$} 이다: 분기에서 $+\tfrac12$
가지(탈리튬화 가지가 위)$\cdot$$-\tfrac12$ 가지(리튬화 가지가 아래)는 이중웰 과주행 기하 —
탈리튬화는 상승 가지의 극대 $\xi_s^-$ 까지, 리튬화는 극소 $\xi_s^+$ 까지 밀린다
(그림~\ref{fig:hysloop}) — 가 전극과 무관하기 때문이고, 분극의 $V_\app>V_n$ 은 산화 방향에서
성립하며, 꼬리 인과의 시간 순서는 탈리튬화의 전위 오름차순과 겹친다. 흑연 음극 하프셀에서는
방전 라벨이 탈리튬화와 일치해 라벨$=$물리가 겹쳤지만(식~\eqref{eq:n0map} 그대로), LCO
하프셀에서는 \emph{충전}이 탈리튬화이므로 LCO 데이터에 모델을 걸 때 방향 인자는 탈리튬화
여부로 먹인다:
\begin{equation}
\boxed{\;\sigma_d=+1\ \Leftrightarrow\ \text{탈리튬화(산화, $\xi:0\!\to\!1$, 전위 상승 진행)}
\ :\quad \text{흑연 하프셀 — 방전}\mapsto+1,\quad \text{LCO 하프셀 — 충전}\mapsto+1\;.}
\label{eq:lco-sigmaslot}
\end{equation}
그림~\ref{fig:lco-direction} 이 이 대응이다. 이렇게 읽어야 ``탈리튬화 봉우리가 높은 전위
쪽''이라는 관측(흑연 $U^{\dis}>U^{\chg}$ 와 동일한 물리)이 LCO 에서도 1:1 로 유지된다.

\textbf{층위 구분(모순 아님).} \S\ref{sec:lco-map} 의 ``방전($\sigma_d=+1$)은 LCO 엔 리튬화''
서술은 셀 방향 \emph{라벨}의 의미론(어느 셀 동작이 어느 화학 방향인가)이고, 본 절의
규약~\eqref{eq:lco-sigmaslot} 은 모델 \emph{입력 슬롯}에 그 라벨이 아니라 탈리튬화 여부를
먹인다는 적용 규칙이다 — 두 서술은 층위가 달라 모순이 아니며, \S\ref{sec:lco-map} 는
무변경이다.

\textbf{평형 종의 불변(방향이 가르는 것과 가르지 않는 것).} 평형 종 자체는 이 선택에 불변이다
— 같은 중심$\cdot$폭에서 $1-\xi_\eq^{(\sigma_d)}=\xi_\eq^{(-\sigma_d)}$(여집합 교환,
식~\eqref{eq:lco-comp})이고 종 $\xi(1-\xi)$ 는 이 교환에 불변이라, 평형 봉우리는 어느 읽기로도
같다. 방향 읽기가 갈라놓는 것은 오직 세 작용처 — 분극$\cdot$분기$\cdot$꼬리 — 다. 이 구분이
Part II 전체의 부호 실수를 막는 가드다.

\subsection{MSMR 예고 — 같은 logistic, 같은 부호 규약}\label{sec:lco-preview}
multi-species, multi-reaction(MSMR) 모델은 양극 조성을 전위의 전이별 logistic 합으로 적는 표준
파라미터화라, Part II 종반(\S\ref{sec:lco-code})에서 Ch1 곡선 클래스와 1:1 사전
(식~\eqref{eq:lco-msmrmap})으로 맞물린다 — $U\leftrightarrow V$,
$U_j^0\leftrightarrow U_j^{\,d}$, $\omega_j\leftrightarrow w_j$, $X_j\leftrightarrow Q_j$,
$f=+\sigma_d$. 방향 인자 대응 $f=+\sigma_d$ 는 같은 물리량끼리(점유$\leftrightarrow$점유$\cdot$
진행률$\leftrightarrow$진행률) 짝짓는 pairing 하의 유일해로 확정된 판정이며, 그 판정이 딛는
가드가 ``\emph{함수형 동형 $\ne$ 물리량 동일}''이다 — MSMR 의 $x_j/X_j$ 는 리튬화 분율(점유)
이고 Ch1 의 $\xi$ 는 탈리튬화 진행률이라, 여집합을 무시하고 직접 등치하면 역부호
$f=-\sigma_d$ 가 나온다(평형 종은 그 교환에 불변이라 봉우리는 같지만 방향 서술이 갈라진다).
본 절은 예고까지만 하고, 대응 사전의 유도와 박스는 \S\ref{sec:lco-code} 가 닫는다.

\begin{figure}[t]
\centering
\begin{tikzpicture}[font=\scriptsize, ar/.style={-{Latex[length=1.8mm]},very thick}]
% invariant header
\node[draw,rounded corners=2pt,fill=black!8,align=center] at (4.35,1.25)
 {invariant (electrode-neutral): $\sigma_d=+1$ $=$ delithiation
  ($\xi:0\!\to\!1$, oxidation, $V\!\uparrow$ on own half-cell axis)\\
  $\sigma_d=-1$ $=$ lithiation};
% ---- graphite anode row ----
\draw[-{Latex[length=1.6mm]}] (0,0) -- (8.7,0);
\node[right,font=\scriptsize\itshape] at (8.7,0) {$V$};
\node[below,font=\scriptsize] at (4.35,-0.72)
  {graphite anode half-cell: $V\approx0.05$--$0.25$ V vs Li/Li$^+$};
\draw[ar] (1.7,0.40) -- (7.0,0.40)
  node[midway,above] {delithiation $=$ cell label \textbf{discharge} $\ \mapsto\ \sigma_d=+1$};
\draw[ar] (7.0,-0.40) -- (1.7,-0.40)
  node[midway,below] {lithiation $=$ cell label charge $\ \mapsto\ \sigma_d=-1$};
% ---- LCO cathode row ----
\begin{scope}[yshift=-2.65cm]
\draw[-{Latex[length=1.6mm]}] (0,0) -- (8.7,0);
\node[right,font=\scriptsize\itshape] at (8.7,0) {$V$};
\node[below,font=\scriptsize] at (4.35,-0.72)
  {LCO cathode half-cell: $V\approx3.7$--$4.2$ V vs Li/Li$^+$};
\draw[ar] (1.7,0.40) -- (7.0,0.40)
  node[midway,above] {delithiation $=$ cell label \textbf{charge} $\ \mapsto\ \sigma_d=+1$};
\draw[ar] (7.0,-0.40) -- (1.7,-0.40)
  node[midway,below] {lithiation $=$ cell label discharge $\ \mapsto\ \sigma_d=-1$};
\end{scope}
\end{tikzpicture}
\caption{충$\cdot$방전 라벨 $\leftrightarrow$ 탈리튬화 방향 $\leftrightarrow$ $\sigma_d$ 슬롯
대응도(신규, 개념도). 전극-중립 불변량은 ``탈리튬화 $=$ 자기 하프셀 축에서 전위 상승 진행
$=\sigma_d=+1$ 슬롯''이고(상단 상자), 셀 방향 \emph{라벨}은 전극에 따라 바뀐다 — 흑연
하프셀은 방전이, LCO 하프셀은 충전이 탈리튬화다(식~\eqref{eq:lco-sigmaslot}). 평형 종은 이
선택에 불변이고, 갈라지는 것은 분극$\cdot$분기$\cdot$꼬리 세 작용처다.}
\label{fig:lco-direction}
\end{figure}
```

**원위치 ★문단의 대체 포인터 문안**(일원화에 따른 최소 diff — master 적용 판단):

- §sec:lco-hys L846–854 "★분기 부호의 전극-중립 읽기(한정)" 문단 →
  > `\textbf{분기 부호.} 식~\eqref{eq:lco-Ubranch} 의 $\sigma_d$ 는 \S\ref{sec:lco-direction} 의 방향 규약(탈리튬화 $=+1$ — LCO 하프셀에선 충전, 식~\eqref{eq:lco-sigmaslot})을 받는다 — ``탈리튬화 가지가 위($+\tfrac12$)$\cdot$리튬화 가지가 아래($-\tfrac12$)''는 이중웰 과주행 기하(그림~\ref{fig:hysloop})가 전극을 가리지 않는 데서 오며, 이 읽기로 ``탈리튬화 봉우리가 높은 전위 쪽''(흑연 $U^{\dis}>U^{\chg}$ 와 동일 물리)이 LCO 에서도 1:1 유지된다.`
- §sec:lco-peak L1426–1437 "★방향 부호의 전극-중립 읽기(적용 한정)" 문단+각주 →
  > `\textbf{방향 부호.} 이후의 $\sigma_d$ 입력은 \S\ref{sec:lco-direction} 의 방향 규약(식~\eqref{eq:lco-sigmaslot})을 따른다 — LCO 데이터에선 충전(탈리튬화) 곡선이 $\sigma_d=+1$ 슬롯, 방전(리튬화$\cdot$전위 하강) 곡선이 $-1$ 슬롯이며, 평형 종은 (b)의 $\xi\leftrightarrow1-\xi$ 대칭으로 이 선택에 불변이라 방향 읽기가 갈라놓는 것은 분극$\cdot$분기$\cdot$꼬리 세 작용처뿐이다.`
  > (원 각주의 층위 구분 서술은 §sec:lco-direction 본문 "층위 구분" 문단으로 승격 — 각주 삭제 가능)

**보존 확인**: f=+σ_d 는 v1.0.12 확정 판정(V1012_P43_verify10) — 본 문안은 재론 없이 확정 사실로만 인용. Ω_j^cat 수치 미배정 지위·tab:lco-staging 의 tier-C placeholder 캡션·two-phase calibration 서술(§sec:lco-hys L771–785)은 전부 원위치 무변경(도입 절은 참조만).

---

## 4. Figure 목록 (목적 | 형식 | 배치 | 캡션 | 산출물)

| # | figure | 목적 | 형식 | 배치 | 캡션 | 스크립트/데이터 |
|---|---|---|---|---|---|---|
| 1 | `fig:sm-reservoir` | grand canonical 구도(계↔저장조의 에너지·입자 교환)를 통계역학 미수강 독자에게 시각 고정 | TikZ 개념도(곡선 없음 — 날조 이슈 없음) | P0.2 (d) 뒤 | §1 본문 수록 | — |
| 2 | `fig:sm-occ` | (a) 단일 자리 점유 θ 의 β-스케일링(계단↔퍼짐) (b) 전기화학 옷 ξ_eq(V)·θ_eq(V), 폭 w=RT/F 의 T-비례 | TikZ 2-panel, 좌표 = 실제 식 평가 | float — 소스 위치는 P0.6 signbox 뒤·첫 참조는 P0.3(좌 패널) | §1 본문 수록 | `V1013_P21_fig_F1_sm_occ.py` + `..._sm_occ.png`(시각 검증) |
| 3 | `fig:sm-gxi` | g_mix(ξ)/RT 의 Ω-가족: Ω=0 순수 엔트로피 → Ω=2RT 볼록성 경계 → Ω=3RT 이중웰+spinodal | TikZ, 좌표 = 실제 식 평가 | P0.5 (d) 뒤 | §1 본문 수록 | `V1013_P21_fig_F1_sm_gxi.py` + `..._sm_gxi.png` |
| 4 | `fig:sm-mu` | μ(θ) 개형의 Ω-가족: 단조 → 문턱 → van der Waals loop(한 μ 에 세 θ), spinodal=극값 | TikZ, 좌표 = 실제 식 평가 | P0.5 (c) 뒤 | §1 본문 수록 | `V1013_P21_fig_F1_sm_mu.py` + `..._sm_mu.png` |
| 5 | `fig:lco-direction` | 충·방전 라벨↔탈리튬화 방향↔σ_d 슬롯 대응(흑연 vs LCO 하프셀) | TikZ 개념도 | 갈래 2 §sec:lco-direction | §3 본문 수록 | — |

스크립트 경로(전부 존재·실행 통과): `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_F1_sm_{occ,gxi,mu}.py`. 각 스크립트는 TikZ 좌표 블록을 stdout 으로 출력(본 문안의 좌표는 그 출력 그대로)하고, 검증용 PNG 를 저장하며, 핵심 값 assert 를 포함한다(θ(U)=½·w(298 K)=25.7 mV·중심 기울기 F/4RT·spinodal 근·ξ↔1−ξ 대칭·gap 닫힌꼴 대조 등). 기존 문서 그림과의 정합: fig:doublewell 의 spinodal 0.2113/0.7887, fig:hysloop 의 극값 1.066 을 독립 재계산으로 재현.

---

## 5. 물리 자체검수 기록 (절별 루핑 결과)

각 절 [원천 정독 → 독립 재유도 → 자체검수 → 앞 절 정합] 순으로 수행. 검수 렌즈 = 부호·차원·극한(β→0/∞·Ω→0/2RT±)·detailed balance·기존 문서와의 교차검산.

| 절 | 검수 항목 | 결과 |
|---|---|---|
| P0.1 | ∂S/∂E=1/T>0 → 고에너지 상태 확률↓ 부호 사슬; βE 무차원; β→0 등확률 회복·β→∞ 바닥상태; Taylor 절단 전제(E_i≪E_tot) 명시 | PASS |
| P0.2 | dS=dE/T−(μ/T)dN 에서 ∂S/∂N=−μ/T 부호 재유도(dE=TdS+μdN 역산); Gibbs 엔트로피→F=−k_BT lnZ 대수 재검(S=⟨E⟩/T+k_BlnZ); ⟨N⟩=(1/β)∂lnΞ/∂μ 직접 검산; μ↑→고점유 가중↑ 물리 정합 | PASS |
| P0.3 | Ξ₁·⟨n⟩ 재유도 = ch2 eq:Z1/eq:occ·ch1 eq:partfn/eq:fermifn 와 일치(독립 유도 후 대조); var(n)=θ(1−θ)·∂θ/∂μ=βθ(1−θ) 미분 직접 검산; β→∞ 계단(ε₀≷μ)·β→0 → ½; Fermi–Dirac "함수형 동형≠물리량 동일" 가드 문장 포함 | PASS |
| P0.4 | Ξ_M=Ξ₁^M 인수분해; Stirling 대수 전개 직접 재계산(1차 항 상쇄·lnM 몫 상쇄 확인); 로그 몫 미분 ln[θ/(1−θ)]; 역변환 θ(μ) = P0.3 결과와 정확 일치(앙상블 동등성 = 앞 절 정합 검사 그 자체); θ→0/1 에서 μ→∓∞ 물리 서술 | PASS |
| P0.5 | 부호 사슬 독립 재유도: u<0(동종 인력)→c<0→Ω>0→+Ωθ(1−θ)(혼합 벌점)→상분리 — 원문 eq:mu 앞 "Ω≡−c" 관례와 일치; θ²=θ−θ(1−θ) 항등; (1−2θ) 미분; ξ↔1−ξ 대칭으로 eq:gxi 회수; g″ 최솟값 4RT−2Ω → 문턱 Ω=2RT(Ω→2RT⁻ 볼록 유지·2RT⁺ 이중웰·Ω→0 이상 회복·Ω<0 은 질서화 경향 언급만—한정어); spinodal 닫힌 근·gap 은 재수록 없이 sec:hys 참조(교훈 카드 ④) | PASS |
| P0.6 | eq:eqcond 재유도(전자 z=−1→μ̃_e=μ⁰−FV·상수 덩이 sFU 흡수·s=+1 고정—σ_d 와 구분 명시); 등치→logistic 대수 재검: θ_eq=1/(1+e^{+sF(V−U)/RT})·ξ_eq=1−θ (원문 eq:logisticsolve·ch2 eq:logistic 과 부호까지 일치); grand canonical 경로 재확인(몰 환산·ε−μ⁰≡0 기준); V↑→ξ_eq↑ 탈리튬화(signbox); V=U→½; T→0 계단; Ω≠0 → eq:Veq 암시형(θ→ξ 부호 반전 대수 직접 재검: RTln[(1−ξ)/ξ]+Ω(2ξ−1)=−sF(V−U) → ×(−1) → eq:Veq 정확 재현); detailed balance 경로(eq:db)와의 두-경로 일치 = sec:dist 서술과 정합; 요동 다리 \|dξ/dV\|=(F/RT)ξ(1−ξ) = eq:belliden 연쇄율 일치 | PASS |
| P0.7 | G=F+PV, PΔV~1 J/mol 차수 추정(한정어 "차수 추정" 부기, 수치 단정 아님); ΔG_j=−sFU_j 부호(U_j>0⇔자발) = sec:center (d) 일치; U_j(T)·∂U_j/∂T 는 참조만(재수록 0); Nernst 역변환 ξ/(1−ξ)=e^{sF(V−U)/RT}→V(ξ) 재검·dV/dξ>0 단조·ξ=½→V=U; ch2 eq:Vxi 와 동형 확인 | PASS |
| 갈래 2 | 이동 원문 3곳 조정만(문두 접속·"아래" 삭제·말미 절 지시 — 전부 위치-정합용) — 물리·수치·부호 무변경; σ_d 규약 박스는 두 ★문단의 공통 물리(탈리튬화=+1)를 재유도 근거(이중웰 기하·분극 산화방향·꼬리 인과)와 함께 일원화; ξ↔1−ξ 불변(eq:lco-comp) 인용; f=+σ_d 확정 판정 재론 없음; LCO Ω_j^cat 미배정 지위·tier-C placeholder 무변경; 층위 구분 문단으로 lco-map "방전=리튬화" 서술과의 표면 모순 해소(원문 각주 논리 승격) | PASS |
| figures | 3 스크립트 assert 전건 통과; PNG 시각 검증(계단화·볼록성 경계·이중웰·loop·교차점 ½); 기존 그림 교차: spinodal 0.2113/0.7887(fig:doublewell 좌표와 동일)·극값 ±1.0657(fig:hysloop 의 1.066)·ΔU_hys 닫힌꼴 (2/F)[Ωu−2RT artanh u] 과 극값 차 2.132 일치(eq:dUhys 독립 검산) | PASS |

**잔여 리스크(정직 표기)**: ① TikZ 좌표는 스크립트 stdout 을 그대로 옮겼으나 컴파일 후 라벨 겹침 등 시각 미세조정은 xelatex 빌드에서 확인 필요(드래프트 단계는 빌드 금지 범위라 미실행). ② P0.7 의 PΔV 차수는 문헌 인용 없는 표준 차수 논거(한정어 부기). ③ 재접속 표 #3·#6 의 축약 diff 는 옵션 제안 — 적용/미적용 어느 쪽도 무모순임을 확인했으나 최종 선택은 master.

---

## 6. 5줄 요약

1. **갈래 1**: Ch1 신설 Part 0 "통계역학 기초" 7개 소절(등확률→Boltzmann·Z→μ·grand canonical→단일 자리 θ→lattice gas·섞임 엔트로피→평균장 Ω·정규용액→전기화학 logistic→G·Nernst)을 전 단계 (a)–(d) 구조·신설 라벨 `eq:sm-*` 28개로 작성 — 기존 박스·라벨 재수록 0, 재사용 전부 명시.
2. **갈래 2**: Part II 도입 절(sec:lco-intro) — 전극-중립 골격 5-인벤토리 + sec:lco-map 전문 이동(위치-정합 조정 3곳) + 방향 규약 일원화 박스(σ_d=+1⇔탈리튬화; LCO 충전↦+1; 평형 종 ξ↔1−ξ 불변; 3작용처) + MSMR 예고(f=+σ_d 확정 인용, 재론 0) + 원위치 ★문단 대체 포인터 2건.
3. **figure**: 신규 5건(개념도 2 + 곡선 3) — 곡선 전부 실제 식 평가(스크립트 3종·assert·PNG), 기존 fig:doublewell/fig:hysloop 수치와 독립 재계산 교차 일치(0.2113/0.7887·±1.066).
4. **물리 검수**: 절별 부호·차원·극한(β→0/∞·Ω→0/2RT±)·detailed balance 상보성·앙상블 동등성(P0.3↔P0.4 두 경로 일치) 전건 PASS — 원천 유도에서 물리 결함 미발견(정정 제안 0건), 신규 기여는 요동–응답(ξ(1−ξ)=점유 분산) 다리 1건.
5. **최약점 자기표시**: TikZ 신규 그림의 컴파일 후 시각 겹침 미확인(빌드 금지 범위) + Part 0 ↔ 본론 중복 유도의 최종 봉합(재접속 표 #3·#6 축약 적용 여부)이 master 결정으로 열려 있음 — 물리 무모순은 확인했으나 문서 부피·중복의 최적점은 편입 시 판단 필요.

