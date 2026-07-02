# V1013_P21_draft_F2 — Ch1 Part 0 「통계역학 기초」 신설 + Part II 「LCO 양극」 도입 절 (드래프트)

- 작성: 드래프트 F2 (N=6 경쟁, 무통신 독립). tex/코드 수정 없음 — 편입은 master.
- 원천 전문 정독 범위(생략 없음): `graphite_ica_ch1_v1.0.13.tex` L1–120(관례)·L120–355(서론·notation·sec:lco-map)·L357–410(sec:pol)·L411–575(sec:center·sec:lco-center)·L578–917(sec:hys·sec:lco-hys)·L918–1140(sec:width·sec:dist)·L1380–1494(sec:eqpeak·sec:lco-peak·broadening 서두)·L1875–1924(충전 격자 역전)·L2064–2143(sec:lco-code MSMR) + `graphite_ica_ch2_v1.0.13.tex` L95–204(eq:Z1 절 전문+주변).
- 모든 부호는 독립 재유도(교훈 ①) — 유도 근거는 §6 자체검수 기록에 단계 단위로 남긴다.
- 신설 라벨 = `eq:sm-*` / 기존 라벨 재사용(`eq:mu`·`eq:gxi`·`eq:xieq`·`eq:eqcond`·`eq:Uj`·`eq:Veq` 등)은 본문에 명시.

문서 목차: §1 Part 0 LaTeX 전문 / §2 재접속 표 / §3 물리 정정 제안 / §4 갈래 2 (Part II 도입 절) LaTeX / §5 figure 목록 / §6 물리 자체검수 기록 / §7 5줄 요약.

---

## 1. 갈래 1 — Ch1 신설 Part 0 「통계역학 기초」 LaTeX 전문

배치 제안: 서론과 `\tableofcontents` 뒤, `\S\ref{sec:notation}`(N0) 앞. 번호 체계는 master 선택 —
최소-diff 는 `\section` 하나(부제에 Part 0 명기)이며 아래 문안이 그 형태다. 문서 관례 승계:
`\dd`·`\eq` 매크로, theorem 박스(`keybox` 등), `\boxed`, (a)→(d) 단계 서술, 본문 한글 prose + 영어 원어.

```latex
% ====================================================================
% ★ Part 0 신설(v1.0.13 P2.1, draft F2) — 통계역학 기초.
%   대상 독자 = 통계역학 미수강 석박사. 배치: 서론 직후, \S\ref{sec:notation} 이전.
%   신설 라벨 프리픽스 eq:sm-*; 기존 라벨 재사용은 각 위치에 명시.
% ====================================================================
\section{통계역학 기초 — 분배함수에서 Nernst 식까지 (Part 0)}\label{sec:sm-found}

본문(N0--N9)의 모든 평형식은 통계역학의 한 사슬에서 나온다. 이 Part 0 은 그 사슬을 처음부터 놓는다 —
통계역학을 수강하지 않았어도 이 절만으로 본문의 출발점들이 닫히도록, 각 단계를
(a) 출발 $\to$ (b) 연산 $\to$ (c) 중간식 $\to$ (d) 박스로 전개한다. 양자역학은 필요하지 않다. 사슬은
\[
\boxed{\;\text{미시상태·앙상블}\ \to\ Z,\Xi\ \to\ \theta=\frac{1}{1+e^{\beta(\varepsilon-\mu)}}
\ \to\ \text{lattice gas}\ \to\ \mu(\theta;\Omega)\ \to\ \xi_\eq\ \text{logistic}\ \to\ G,\ \text{Nernst}\;}
\]
이고, 도착점의 식들(\eqref{eq:mu}·\eqref{eq:gxi}·\eqref{eq:xieq}·\eqref{eq:Uj})이 본문 전이 루프의 입력이다.

\subsection{앙상블과 Boltzmann 인자, 분배함수, 화학퍼텐셜 $\mu$}\label{sec:sm-ensemble}
\textbf{(a) 출발 — 미시상태·앙상블과 두 공준.} \emph{미시상태}(microstate)는 계의 모든 자유도를 지정한
배치 하나이고, \emph{거시상태}(macrostate)는 에너지·부피·입자수 $(E,V,N)$ 같은 소수의 거시변수만 지정한
미시상태의 집합이다. 같은 거시 조건을 공유하는 미시상태들의 모음이 \emph{앙상블}(ensemble)이다. 통계역학은
두 공준으로 시작한다 — 고립계 평형에서 접근 가능한 $W$ 개 미시상태는 등확률이고(공준 1), 엔트로피는 그
경우의 수의 로그다(공준 2, Boltzmann):
\begin{equation}
S\;=\;k_B\ln W.
\label{eq:sm-S}
\end{equation}
열역학과의 접점은 근본 미분식 $\dd E=T\dd S-P\dd V+\mu\,\dd N$ 을 $S$ 에 대해 푼 형태다:
\begin{equation}
\dd S=\frac{1}{T}\,\dd E+\frac{P}{T}\,\dd V-\frac{\mu}{T}\,\dd N
\quad\Longrightarrow\quad
\frac{\partial S}{\partial E}\Big|_{V,N}=\frac1T,\qquad
\frac{\partial S}{\partial N}\Big|_{E,V}=-\frac{\mu}{T}.
\label{eq:sm-fund}
\end{equation}
여기서 $\mu$ 의 물리적 의미가 이미 보인다 — 입자 1개를 받아들일 때 엔트로피가 $\mu/T$ 만큼 \emph{감소}하는
값비쌈의 척도다. 두 계 1,2 가 입자를 교환하면 총 엔트로피 변화가
$\dd S_\mathrm{tot}=\big(\tfrac{\mu_2}{T}-\tfrac{\mu_1}{T}\big)\dd N_1\ge0$ 이므로 입자는 $\mu$ 가 높은 쪽에서
낮은 쪽으로 흐르고, 정지 조건은 $\mu_1=\mu_2$ — 화학퍼텐셜의 일치가 곧 입자 교환 평형이다.

\textbf{(b) 연산 — 저장조와 접촉한 작은 계.} 관심 계가 거대한 저장조(reservoir)와 에너지·입자를 교환한다.
계가 미시상태 $i$(에너지 $E_i$, 입자수 $N_i$)에 있을 확률은 공준 1 에 의해 그때 저장조가 가질 수 있는 경우의
수에 비례한다:
\begin{equation}
P_i\;\propto\;W_R(E_\mathrm{tot}-E_i,\,N_\mathrm{tot}-N_i)
\;=\;\exp\!\Big[\frac{S_R(E_\mathrm{tot}-E_i,\,N_\mathrm{tot}-N_i)}{k_B}\Big].
\label{eq:sm-resv}
\end{equation}
저장조가 계보다 훨씬 크므로 $S_R$ 을 1차에서 절단해 전개하면(식~\eqref{eq:sm-fund} 의 두 도함수 대입)
\begin{equation}
S_R(E_\mathrm{tot}-E_i,\,N_\mathrm{tot}-N_i)
= S_R(E_\mathrm{tot},N_\mathrm{tot})-\frac{E_i}{T}+\frac{\mu N_i}{T}+\mathcal O(E_i^2,N_i^2).
\label{eq:sm-taylor}
\end{equation}
\textbf{(c) 중간식 — Gibbs 인자와 canonical 특수형.} 식~\eqref{eq:sm-taylor} 을 \eqref{eq:sm-resv} 에 넣으면
상수 몫이 규격화로 빠지고
\begin{equation}
P_i\;\propto\;e^{-\beta(E_i-\mu N_i)},\qquad \beta\equiv\frac{1}{k_BT}
\label{eq:sm-gibbsfactor}
\end{equation}
— 이 지수가 \emph{Gibbs 인자}다. 입자 교환이 없으면($N_i$ 고정) $e^{-\beta E_i}$ 의 \emph{Boltzmann 인자}로
줄고, 그 규격화 합이 canonical 분배함수(partition function) $Z=\sum_ie^{-\beta E_i}$, 그 로그가 Helmholtz
자유에너지 $F=-k_BT\ln Z$ 다($\langle E\rangle=\partial(\beta F)/\partial\beta$·$S=-\partial F/\partial T$ 가
열역학 관계와 일치함이 이 명명의 근거다). 식~\eqref{eq:sm-fund} 의 $\mu$ 를 $F$ 로 옮기면
$\mu=\partial F/\partial N|_{T,V}$ — \emph{온도·부피를 고정한 채 입자 1개를 더 넣는 자유에너지 비용}이며,
이것이 본문 \S\ref{sec:center} 가 쓰는 거시 정의 $\mu=\partial G/\partial n|_{T,P}$ 와 같은 양임은
\S\ref{sec:sm-macro} 에서 닫는다.

\textbf{(d) 박스 — grand canonical 분배함수.} 입자수까지 교환하는 앙상블이
\emph{대정준}(grand canonical) 앙상블이고, 그 규격화 합과 평균 입자수는
\begin{equation}
\boxed{\;\Xi=\sum_i e^{-\beta(E_i-\mu N_i)},\qquad
P_i=\frac{e^{-\beta(E_i-\mu N_i)}}{\Xi},\qquad
\langle N\rangle=k_BT\,\frac{\partial\ln\Xi}{\partial\mu}\;}
\label{eq:sm-gc}
\end{equation}
($\partial\ln\Xi/\partial\mu=\beta\sum_iN_iP_i=\beta\langle N\rangle$ 로 셋째 식이 첫째·둘째에서 나온다).
극한 검산 — $\beta\to0$ 이면 $P_i\to$ 등확률(열적 규율 소실), $\beta\to\infty$ 면 $E_i-\mu N_i$ 최소 상태만
남는다. 삽입 전극이 정확히 이 설정이다 — 격자의 자리들이 전해질을 통해 Li 저장조(상대극 Li 금속)와 입자를
교환하므로 $\mu$ 가 고정된 대정준 문제이고, 다음 소절이 그 최소 단위(자리 하나)를 푼다.

\subsection{단일 삽입 자리 — 2-상태 대정준 점유}\label{sec:sm-site}
\textbf{(a) 출발 — 미시상태 2개.} 격자의 삽입 자리 \emph{하나}를 떼어 보자. 미시상태는 둘뿐이다 — 빈 자리
($n=0$, 에너지 $0$)와 Li 1개가 든 자리($n=1$, 에너지 $\varepsilon$; $\varepsilon$ 은 자리--리튬 결합이 정하는
자리당 삽입 에너지). 자리는 전해질 너머의 Li 저장조와 입자를 교환하므로 식~\eqref{eq:sm-gc} 의 대정준 설정
그대로다.

\textbf{(b) 연산 — 분배함수에 두 상태 대입.} 식~\eqref{eq:sm-gc} 의 합이 두 항으로 끝난다:
\begin{equation}
\Xi_1=\sum_{n=0,1}e^{-\beta(\varepsilon-\mu)n}
=1+e^{-\beta(\varepsilon-\mu)}.
\label{eq:sm-Z1}
\end{equation}
이 식이 본문 식~\eqref{eq:partfn}($Z=1+e^{-\beta\Delta\mu}$)와 Chapter 2 의 식 (eq:Z1) 그 자체다 — 두 곳 모두
여기서 세운 대정준 합의 재등장이다.

\textbf{(c) 중간식 — 점유 확률.} 점유 상태의 확률이 곧 평균 점유다:
\begin{equation}
\langle n\rangle=0\cdot P_0+1\cdot P_1=\frac{e^{-\beta(\varepsilon-\mu)}}{1+e^{-\beta(\varepsilon-\mu)}},
\label{eq:sm-occmid}
\end{equation}
그리고 식~\eqref{eq:sm-gc} 의 셋째 식으로 교차검증하면
$k_BT\,\partial\ln\Xi_1/\partial\mu=e^{-\beta(\varepsilon-\mu)}/(1+e^{-\beta(\varepsilon-\mu)})$ — 같은 결과다.

\textbf{(d) 박스 — 점유율 $\theta$.} 분모·분자를 $e^{-\beta(\varepsilon-\mu)}$ 로 나누면
\begin{equation}
\boxed{\;\theta\;\equiv\;\langle n\rangle\;=\;\frac{1}{1+e^{\beta(\varepsilon-\mu)}}\;.}
\label{eq:sm-theta}
\end{equation}
극한 검산 — $\beta\to\infty$(T$\to$0)에서 $\theta\to1$($\mu>\varepsilon$)/$0$($\mu<\varepsilon$)의 계단,
$\beta\to0$(T$\to\infty$)에서 $\theta\to\tfrac12$(엔트로피 지배), $\mu\to\pm\infty$ 에서 $\theta\to1/0$.
★함수형 가드 — 식~\eqref{eq:sm-theta} 는 Fermi--Dirac 함수와 \emph{동형}이지만 물리량은 다르다. 공유하는
것은 ``한 자리에 입자 0 또는 1''이라는 배타 점유의 대수 구조뿐이고, 여기의 입자는 전자가 아니라 Li 이온,
준위는 전자 준위가 아니라 삽입 자리다(같은 지적이 본문 \S\ref{sec:dist}·Chapter 2 에 있다). 배타성의 근거도
양자 통계가 아니라 자리 하나에 이온 하나라는 기하학적 사실이다.

\subsection{$M$ 개의 독립 자리 — lattice gas 와 섞임 엔트로피}\label{sec:sm-lattice}
\textbf{(a) 출발 — 동등·독립 자리의 집합.} 결정 안에 동등한 삽입 자리가 $M$ 개 있고 서로 상호작용하지
않는다고 하자 — 이 모형이 \emph{격자기체}(lattice gas)의 이상 극한이다. 미시상태는 점유 배열
$(n_1,\dots,n_M)$($n_k\in\{0,1\}$)이고 $E=\varepsilon\sum_kn_k$, $N=\sum_kn_k$ 다.

\textbf{(b) 연산 — 분배함수의 인수분해.} 자리들이 독립이라 대정준 합이 자리별 곱으로 갈라진다:
\begin{equation}
\Xi_M=\sum_{n_1=0,1}\!\cdots\!\sum_{n_M=0,1}\prod_{k=1}^{M}e^{-\beta(\varepsilon-\mu)n_k}
=\prod_{k=1}^{M}\Big[\sum_{n_k=0,1}e^{-\beta(\varepsilon-\mu)n_k}\Big]=\Xi_1^{\,M},
\label{eq:sm-factor}
\end{equation}
따라서 식~\eqref{eq:sm-gc} 의 셋째 식으로 $\langle N\rangle=k_BT\,\partial(M\ln\Xi_1)/\partial\mu=M\theta$ —
거시 점유율이 단일 자리 점유 확률 \eqref{eq:sm-theta} 와 같다.

\textbf{(c) 중간식 — 같은 결과의 셈법 경로(교차검증).} 이번엔 입자수 $n$ 을 고정하고 배치를 센다.
$M$ 자리에서 $n$ 자리를 고르는 경우의 수 $W=M!/[n!(M-n)!]$ 에 공준 2(식~\eqref{eq:sm-S})와 Stirling 근사
$\ln m!\simeq m\ln m-m$ 을 적용하면($\theta=n/M$)
\begin{equation}
S_\mathrm{mix}=k_B\ln W\simeq-k_BM\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big],
\label{eq:sm-Smix}
\end{equation}
자유에너지 $F(n)=n\varepsilon-TS_\mathrm{mix}$ 를 $n$ 으로 미분하면
\begin{equation}
\mu=\frac{\partial F}{\partial n}
=\varepsilon+k_BT\ln\frac{\theta}{1-\theta}.
\label{eq:sm-mucount}
\end{equation}
한편 식~\eqref{eq:sm-theta} 를 $\mu$ 에 대해 뒤집어도($e^{\beta(\varepsilon-\mu)}=(1-\theta)/\theta$) 같은
식~\eqref{eq:sm-mucount} 가 나온다 — 대정준 경로(자리 하나의 확률)와 셈법 경로(배치 수의 로그)가 같은
$\mu(\theta)$ 에 닿는 것이 앙상블 동등성이며, 본문 \S\ref{sec:dist} 가 말하는 ``kinetic·thermo 두 경로가 한
분포의 두 얼굴''의 평형 쪽 절반이 바로 이것이다.

\textbf{(d) 박스 — 몰 단위 이상 lattice gas 화학퍼텐셜.} 자리당 $k_B$·$\varepsilon$ 을 몰당
$R=N_Ak_B$·$\mu^0\equiv N_A\varepsilon$ 으로 환산하면
\begin{equation}
\boxed{\;\mu(\theta)=\mu^0+RT\ln\frac{\theta}{1-\theta}\qquad(\text{이상 lattice gas})\;.}
\label{eq:sm-muideal}
\end{equation}
부호·극한 검산 — $\theta\to0$ 에서 $\mu\to-\infty$(거의 빈 격자에 입자를 넣는 일은 섞임 엔트로피 이득 때문에
얼마든지 값싸다), $\theta\to1$ 에서 $+\infty$(마지막 빈자리는 무한히 비싸다), $\theta=\tfrac12$ 에서
$\mu=\mu^0$·자리당 $S_\mathrm{mix}$ 최대 $k_B\ln2$. 식~\eqref{eq:sm-muideal} 는 본문 식~\eqref{eq:mu} 의
$\Omega=0$ 특수형이고, 상호작용 몫 $\Omega(1-2\theta)$ 를 다음 소절이 더한다.

\subsection{평균장 상호작용 — 정규용액 $\Omega$ 와 이중웰 문턱}\label{sec:sm-mf}
\textbf{(a) 출발 — 이웃 상호작용의 평균장 근사.} 실제 격자에서 자리들은 독립이 아니다 — 점유된 이웃은 다음
Li 의 삽입 에너지를 바꾼다(정전 반발·탄성 변형·전자 구조). 점유 이웃 \emph{쌍}당 에너지를 $u$, 배위수를 $z$
라 하면 정확한 상호작용 에너지는 배치마다 다르지만, 각 자리의 이웃 점유를 평균 $\theta$ 로 대체하는
\emph{평균장}(mean-field, Bragg--Williams) 근사에서
\begin{equation}
E_\mathrm{int}\;\simeq\;\frac{Mz}{2}\,u\,\theta^2
\label{eq:sm-mf}
\end{equation}
($M\theta$ 개 점유 자리 각각의 $z\theta$ 개 점유 이웃, $\tfrac12$ 은 쌍 이중계수 방지).

\textbf{(b) 연산 — 항등 분해와 $\Omega$ 의 정의.} 자리 1몰당 상호작용 몫은 $\tfrac{z}{2}N_Au\,\theta^2$ 이고,
항등식 $\theta^2=\theta-\theta(1-\theta)$ 로 분해하면
\begin{equation}
\frac{z}{2}N_Au\,\theta^2
=\underbrace{\frac{z}{2}N_Au\,\theta}_{\text{선형 — }\mu^0\text{ 에 흡수}}
+\;\Omega\,\theta(1-\theta),
\qquad
\Omega\;\equiv\;-\frac{z}{2}N_A\,u,
\label{eq:sm-omega}
\end{equation}
곧 점유 이웃끼리 \emph{인력}($u<0$)이면 $\Omega>0$(같은 종이 뭉치려는 상분리 경향), 반발($u>0$)이면
$\Omega<0$(교대 정렬 경향)이다. 이 한 모수로 혼합 자유에너지를 적는 모형이
\emph{정규용액}(regular solution)이고, 본문 표의 $\Omega_j$·$\Omega_j^\mathrm{cat}$[J/mol]이 정확히 이 슬롯이다.

\textbf{(c) 중간식 — $g(\theta)$ 와 $\mu(\theta)$.} 자리 1몰당 자유에너지에 \eqref{eq:sm-Smix} 의 섞임 몫과
\eqref{eq:sm-omega} 의 상호작용 몫을 더하면
\begin{equation}
g(\theta)=\mu^0\theta+RT\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big]+\Omega\,\theta(1-\theta),
\label{eq:sm-gtheta}
\end{equation}
$\theta$ 로 미분하면(로그 몫 $RT\ln[\theta/(1-\theta)]$ — 식~\eqref{eq:sm-mucount} 와 같은 계산; 상호작용 몫
$\Omega(1-2\theta)$)
\[
\mu(\theta)=\mu^0+RT\ln\frac{\theta}{1-\theta}+\Omega\,(1-2\theta)
\]
— 본문 식~\eqref{eq:mu} 그 자체다(그림~\ref{fig:sm-mu}). 진행률 $\xi=1-\theta$ 로 옮기면 섞임 몫과
$\theta(1-\theta)=\xi(1-\xi)$ 몫이 모두 $\xi\leftrightarrow1-\xi$ 자리바꿈에 대칭(우함수)이라 조성 몫의 꼴이
불변이고, 선형·상수 몫만 $g_j^0$ 으로 재편된다 — 본문 식~\eqref{eq:gxi} 가 그 결과이며, 이 우함수 대칭이
\S\ref{sec:hys} 의 1계 미분 논거($f'(1-\xi)=-f'(\xi)$)의 뿌리다.

\textbf{(d) 박스 — 볼록성 상실의 문턱.} 식~\eqref{eq:sm-gtheta} 를 $\xi$ 좌표에서 두 번 미분하면(본문
식~\eqref{eq:gpp} 와 동일 계산) $g''(\xi)=RT/[\xi(1-\xi)]-2\Omega$ 이고, 첫 항의 최솟값이 $\xi=\tfrac12$ 에서
$4RT$ 이므로
\begin{equation}
\boxed{\;
g''(\xi)>0\ \ \forall\xi\ \Longleftrightarrow\ \Omega\le2RT\ \ (\text{단상·연속 고용체}),
\qquad
\Omega>2RT\ \Longleftrightarrow\ \text{이중웰}\ \ \Big(T_c=\frac{\Omega}{2R}\Big)\;.}
\label{eq:sm-thresh}
\end{equation}
$\Omega>2RT$ 면 가운데($g''<0$)가 언덕이 되어 두 골짜기가 생기고(그림~\ref{fig:sm-gxi}), 그 변곡점이 본문
식~\eqref{eq:spinodal} 의 spinodal $\xi_{s}^\pm=\tfrac12(1\pm u)$, 거기서 자라는 히스테리시스 gap 이
식~\eqref{eq:dUhys} 다 — 닫힌 꼴 유도는 \S\ref{sec:hys} 가 맡고, Part 0 은 문턱까지만 놓는다. 극한 검산 —
$\Omega\to0$: $g''\ge4RT>0$ 로 항상 단일 웰(\S\ref{sec:sm-lattice} 로 환원); $\Omega\to2RT^-$:
$g''(\tfrac12)\to0^+$ 로 바닥이 4차 항 수준까지 평탄해지되 아직 한 웰; $\Omega\to2RT^+$: 웰이 둘로 갈라지기
시작하고 $T_c=\Omega/2R$ 아래에서만 상분리가 산다.

\begin{figure}[t]
\centering
\begin{tikzpicture}[x=9.6cm,y=6.8cm]
\draw[-{Latex[length=1.6mm]}] (-0.02,-0.76) -- (-0.02,0.14) node[above,font=\scriptsize] {$f(\xi)/RT$ (mixing part)};
\draw[-{Latex[length=1.6mm]}] (-0.02,0) -- (1.06,0) node[below,font=\scriptsize] {$\xi$};
\foreach \xx in {0.5,1.0} {\draw (\xx,0.008) -- (\xx,-0.008) node[below,font=\scriptsize] {\xx};}
% Omega = 0 RT (ideal mixing)
\draw[black!45] plot[smooth] coordinates {(0.004,-0.0261) (0.020,-0.0980) (0.070,-0.2536) (0.118,-0.3625) (0.166,-0.4488) (0.213,-0.5183) (0.261,-0.5742) (0.309,-0.6182) (0.357,-0.6515) (0.404,-0.6748) (0.452,-0.6886) (0.500,-0.6931) (0.548,-0.6886) (0.596,-0.6748) (0.643,-0.6515) (0.691,-0.6182) (0.739,-0.5742) (0.787,-0.5183) (0.834,-0.4488) (0.882,-0.3625) (0.930,-0.2536) (0.980,-0.0980) (0.996,-0.0261)};
% Omega = 1 RT
\draw[black!45] plot[smooth] coordinates {(0.004,-0.0221) (0.020,-0.0784) (0.070,-0.1885) (0.118,-0.2586) (0.166,-0.3106) (0.213,-0.3505) (0.261,-0.3813) (0.309,-0.4047) (0.357,-0.4220) (0.404,-0.4339) (0.452,-0.4409) (0.500,-0.4431) (0.548,-0.4409) (0.596,-0.4339) (0.643,-0.4220) (0.691,-0.4047) (0.739,-0.3813) (0.787,-0.3505) (0.834,-0.3106) (0.882,-0.2586) (0.930,-0.1885) (0.980,-0.0784) (0.996,-0.0221)};
% Omega = 2 RT (threshold: flat bottom)
\draw[thick,black!70] plot[smooth] coordinates {(0.004,-0.0181) (0.020,-0.0588) (0.070,-0.1234) (0.118,-0.1547) (0.166,-0.1725) (0.213,-0.1827) (0.261,-0.1884) (0.309,-0.1913) (0.357,-0.1926) (0.404,-0.1930) (0.452,-0.1931) (0.500,-0.1931) (0.548,-0.1931) (0.596,-0.1930) (0.643,-0.1926) (0.691,-0.1913) (0.739,-0.1884) (0.787,-0.1827) (0.834,-0.1725) (0.882,-0.1547) (0.930,-0.1234) (0.980,-0.0588) (0.996,-0.0181)};
% Omega = 2.5 RT (double well)
\draw[densely dashed,thick] plot[smooth] coordinates {(0.004,-0.0161) (0.020,-0.0490) (0.070,-0.0909) (0.118,-0.1027) (0.166,-0.1034) (0.213,-0.0988) (0.261,-0.0919) (0.309,-0.0845) (0.357,-0.0778) (0.404,-0.0726) (0.452,-0.0693) (0.500,-0.0681) (0.548,-0.0693) (0.596,-0.0726) (0.643,-0.0778) (0.691,-0.0845) (0.739,-0.0919) (0.787,-0.0988) (0.834,-0.1034) (0.882,-0.1027) (0.930,-0.0909) (0.980,-0.0490) (0.996,-0.0161)};
% Omega = 3 RT (double well, humped)
\draw[thick] plot[smooth] coordinates {(0.004,-0.0141) (0.020,-0.0392) (0.070,-0.0583) (0.118,-0.0508) (0.166,-0.0343) (0.213,-0.0149) (0.261,0.0046) (0.309,0.0222) (0.357,0.0369) (0.404,0.0478) (0.452,0.0546) (0.500,0.0569) (0.548,0.0546) (0.596,0.0478) (0.643,0.0369) (0.691,0.0222) (0.739,0.0046) (0.787,-0.0149) (0.834,-0.0343) (0.882,-0.0508) (0.930,-0.0583) (0.980,-0.0392) (0.996,-0.0141)};
% spinodal markers on Omega=3RT: xi_s = 0.2113 / 0.7887, f/RT = -0.0157
\fill (0.2113,-0.0157) circle (0.5pt) node[below left,font=\scriptsize] {$\xi_s^-$};
\fill (0.7887,-0.0157) circle (0.5pt) node[below right,font=\scriptsize] {$\xi_s^+$};
% curve labels at xi = 0.5 (each just off its own curve)
\node[font=\scriptsize] at (0.5,0.095) {$\Omega=3RT$};
\node[font=\scriptsize] at (0.5,-0.115) {$2.5RT$};
\node[font=\scriptsize] at (0.5,-0.235) {$2RT$};
\node[font=\scriptsize] at (0.5,-0.40) {$1RT$};
\node[font=\scriptsize] at (0.5,-0.655) {$\Omega=0$};
\end{tikzpicture}
\caption{정규용액 조성 자유에너지의 섞임 몫 $f(\xi)/RT=\xi\ln\xi+(1-\xi)\ln(1-\xi)+(\Omega/RT)\,\xi(1-\xi)$
(신규 그림 — 스크립트 실계산 좌표, \texttt{V1013\_P21\_fig\_F2\_gxi\_doublewell.py}). $\Omega\le2RT$ 면 한 웰,
$\Omega=2RT$ 에서 바닥이 평탄해지고(문턱, 식~\eqref{eq:sm-thresh}), $\Omega>2RT$ 면 가운데가 언덕이 된 이중웰 —
$\Omega=3RT$ 곡선의 점이 spinodal $\xi_s^\pm$(본문 식~\eqref{eq:spinodal}, $0.2113/0.7887$)다. 본문
그림~\ref{fig:doublewell} 은 이 가족 중 $\Omega=3RT$ 한 장을 확대한 것이다.}
\label{fig:sm-gxi}
\end{figure}

\begin{figure}[t]
\centering
\begin{tikzpicture}[x=9.6cm,y=0.82cm]
\draw[-{Latex[length=1.6mm]}] (-0.02,-3.7) -- (-0.02,3.9) node[above,font=\scriptsize] {$(\mu-\mu^0)/RT$};
\draw[-{Latex[length=1.6mm]}] (-0.02,0) -- (1.06,0) node[below,font=\scriptsize] {$\theta$};
\foreach \xx in {0.25,0.5,0.75,1.0} {\draw (\xx,0.07) -- (\xx,-0.07) node[below,font=\scriptsize] {\xx};}
\draw[densely dotted,black!60] (-0.02,0) -- (1.0,0);
% Omega = 0 (ideal, monotone)
\draw[black!45] plot[smooth] coordinates {(0.030,-3.4761) (0.050,-2.9444) (0.080,-2.4423) (0.120,-1.9924) (0.160,-1.6582) (0.200,-1.3863) (0.240,-1.1527) (0.280,-0.9445) (0.320,-0.7538) (0.360,-0.5754) (0.400,-0.4055) (0.440,-0.2412) (0.480,-0.0800) (0.520,0.0800) (0.560,0.2412) (0.600,0.4055) (0.640,0.5754) (0.680,0.7538) (0.720,0.9445) (0.760,1.1527) (0.800,1.3863) (0.840,1.6582) (0.880,1.9924) (0.920,2.4423) (0.950,2.9444) (0.970,3.4761)};
% Omega = 2RT (threshold: flat inflection at 1/2)
\draw[thick,black!70] plot[smooth] coordinates {(0.030,-1.5961) (0.050,-1.1444) (0.080,-0.7623) (0.120,-0.4724) (0.160,-0.2982) (0.200,-0.1863) (0.240,-0.1127) (0.280,-0.0645) (0.320,-0.0338) (0.360,-0.0154) (0.400,-0.0055) (0.440,-0.0012) (0.480,-0.0000) (0.520,0.0000) (0.560,0.0012) (0.600,0.0055) (0.640,0.0154) (0.680,0.0338) (0.720,0.0645) (0.760,0.1127) (0.800,0.1863) (0.840,0.2982) (0.880,0.4724) (0.920,0.7623) (0.950,1.1444) (0.970,1.5961)};
% Omega = 3RT (non-monotone)
\draw[thick] plot[smooth] coordinates {(0.030,-0.6561) (0.050,-0.2444) (0.080,0.0777) (0.120,0.2876) (0.160,0.3818) (0.200,0.4137) (0.240,0.4073) (0.280,0.3755) (0.320,0.3262) (0.360,0.2646) (0.400,0.1945) (0.440,0.1188) (0.480,0.0400) (0.520,-0.0400) (0.560,-0.1188) (0.600,-0.1945) (0.640,-0.2646) (0.680,-0.3262) (0.720,-0.3755) (0.760,-0.4073) (0.800,-0.4137) (0.840,-0.3818) (0.880,-0.2876) (0.920,-0.0777) (0.950,0.2444) (0.970,0.6561)};
% extrema of Omega=3RT at theta_s -+ = 0.2113 / 0.7887, mu/RT = +-0.4151
\fill (0.2113,0.4151) circle (0.5pt) node[above,font=\scriptsize] {$\theta_s^-$};
\fill (0.7887,-0.4151) circle (0.5pt) node[below,font=\scriptsize] {$\theta_s^+$};
% labels
\node[right,font=\scriptsize] at (0.80,2.0) {$\Omega=0$};
\node[right,font=\scriptsize] at (0.86,0.9) {$2RT$};
\node[right,font=\scriptsize] at (0.88,-0.9) {$3RT$};
\end{tikzpicture}
\caption{평균장 화학퍼텐셜 $\mu(\theta)$(본문 식~\eqref{eq:mu}; 신규 그림 — 스크립트 실계산 좌표,
\texttt{V1013\_P21\_fig\_F2\_mu\_theta.py}). $\Omega\le2RT$ 면 단조(한 $\mu$ 에 한 $\theta$),
$\Omega=2RT$ 에서 $\theta=\tfrac12$ 기울기가 0(평탄 변곡), $\Omega>2RT$ 면 비단조 — 극값(점)이 spinodal
$\theta_s^\mp$ 이고 그 사이($g''<0$)에서 한 $\mu$ 에 세 $\theta$ 가 대응해 \S\ref{sec:hys} 의 히스테리시스가
자란다. $V_\eq(\xi)$ 그림~\ref{fig:hysloop} 가 이 곡선의 전위 번역이다.}
\label{fig:sm-mu}
\end{figure}

\subsection{전기화학 연결 — $\mu_\mathrm{Li}=\mu^0-sF(V-U)$ 와 평형 점유 logistic}\label{sec:sm-electro}
\textbf{(a) 출발 — 전기화학 퍼텐셜과 삽입 반응.} 하전 종은 화학 결합의 값어치에 정전 에너지가 더해진
\emph{전기화학 퍼텐셜}(electrochemical potential)로 평형을 판정한다:
\begin{equation}
\tilde\mu\;\equiv\;\mu+zF\phi
\label{eq:sm-emu}
\end{equation}
($z$ = 전하수, $\phi$ = 그 종이 있는 상의 정전 퍼텐셜). 삽입 반응
$\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\mathrm{host})}$ 의 평형은 양변 $\tilde\mu$ 합의 일치
— 본문 식~\eqref{eq:eqbalance} — 이고, host 안의 Li 는 중성이라 $\tilde\mu_\mathrm{Li}=\mu_\mathrm{Li}$ 다:
\begin{equation}
\big(\mu_{\mathrm{Li}^+}+F\phi_S\big)+\big(\mu_{e^-}-F\phi_M\big)=\mu_\mathrm{Li}(\theta)
\label{eq:sm-workbal}
\end{equation}
($\phi_S$ = 전해질, $\phi_M$ = 작동 전극의 정전 퍼텐셜; $z_{\mathrm{Li}^+}{=}+1$, $z_{e^-}{=}-1$).

\textbf{(b) 연산 — 기준전극으로 측정 전위를 결선.} 같은 전해질에 담긴 기준 Li 금속 전극도 자기 평형
$\mathrm{Li}^++e^-\rightleftharpoons\mathrm{Li}_{(\mathrm{metal})}$ 을 이룬다:
\begin{equation}
\big(\mu_{\mathrm{Li}^+}+F\phi_S\big)+\big(\mu_{e^-}-F\phi_\mathrm{ref}\big)=\mu_\mathrm{Li}^\mathrm{metal}.
\label{eq:sm-refbal}
\end{equation}
\eqref{eq:sm-workbal} 에서 \eqref{eq:sm-refbal} 을 빼면 전해질 몫($\mu_{\mathrm{Li}^+}+F\phi_S$)과 전자의
화학 몫이 통째로 상쇄되고, 측정 전위 $V\equiv\phi_M-\phi_\mathrm{ref}$(vs Li/Li$^+$)만 남는다:
\begin{equation}
\mu_\mathrm{Li}(\theta_\eq)-\mu_\mathrm{Li}^\mathrm{metal}=-F\,V.
\label{eq:sm-muV}
\end{equation}
전위를 올리면 host 안 Li 의 값어치가 정확히 $-FV$ 로 내려간다 — ``$V$ 를 올리면 탈리튬화''가 이 한 줄이다.

\textbf{(c) 중간식 — 상수 덩이를 $U$ 로 묶기.} 식~\eqref{eq:sm-muV} 의 상수 $\mu_\mathrm{Li}^\mathrm{metal}$
를 전이 중심 $U\equiv(\mu_\mathrm{Li}^\mathrm{metal}-\mu^0)/F$ 로 재포장하면($s=+1$ 유도 규약,
\S\ref{sec:notation} 표의 고정 부호)
\begin{equation}
\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF\,(V-U),
\qquad
\Delta G_j\equiv\mu^0-\mu_\mathrm{Li}^\mathrm{metal}=-sF\,U_j
\label{eq:sm-eqcond}
\end{equation}
— 본문 식~\eqref{eq:eqcond} 와 글자까지 같은 식이다($U_j>0\Leftrightarrow\Delta G_j<0$, 곧 그 전이가 자발일
전위 창이 양수라는 부호 읽기도 동일). Chapter 2 의 식 (eq:muV)도 같은 관계의 $\sigma_d{=}+1$ 고정 표기다.

\textbf{(d) 박스 — 평형 점유 logistic.} $\Omega=0$ 이면 \eqref{eq:sm-muideal} 를 \eqref{eq:sm-eqcond} 에 넣어
$RT\ln[\theta_\eq/(1-\theta_\eq)]=-sF(V-U)$, 로그를 풀면 닫힌 꼴이 나온다:
\begin{equation}
\boxed{\;\theta_\eq(V,T)=\frac{1}{1+e^{+sF(V-U)/RT}},\qquad
\xi_\eq(V,T)=1-\theta_\eq=\frac{1}{1+e^{-sF(V-U)/RT}},\qquad
w\equiv\frac{RT}{F}\;.}
\label{eq:sm-logistic}
\end{equation}
자리당 언어와의 일치 검산 — 식~\eqref{eq:sm-theta} 의 지수는 $\beta(\varepsilon-\mu_\mathrm{Li})$ 이고, 몰로
올리면 $(\mu^0-\mu_\mathrm{Li})/RT$, 여기에 \eqref{eq:sm-eqcond} 를 넣으면 $+sF(V-U)/RT$ — 정확히
\eqref{eq:sm-logistic} 의 $\theta_\eq$ 지수다(자리당 $k_BT\!\cdot\!e$ 가 몰당 $RT\!\cdot\!F$ 로 한꺼번에 환산).
점유 $\theta_\eq$ 는 $V$ 에 감소하고 탈리튬화 진행률 $\xi_\eq$ 는 증가하는 logistic — 그림~\ref{fig:sm-thetaV}
가 폭 $w=RT/F$ 의 온도 의존과 $T\to0$ 계단 극한을 보인다. 여기서 세 가지가 본문으로 이어진다.
\begin{enumerate}[label=(\roman*),leftmargin=2.2em,itemsep=1pt]
\item \textbf{일반화 = 본문 식~\eqref{eq:xieq}.} 고정 부호 $s$ 자리에 방향 부호 $\sigma_d$, 중심에 분기 중심
$U_j^{\,d}$, 폭에 다중도 $w_j=n_jRT/F$(식~\eqref{eq:wbase})를 넣은 것이 코드의 평형 점유다 — $\sigma_d$ 는
평형이 아니라 방향 라벨의 몫이라 \S\ref{sec:notation} 의 세 작용처로만 들어간다.
\item \textbf{동역학 경로와의 합류.} 같은 logistic 이 Eyring 속도식의 정지점(detailed balance,
식~\eqref{eq:db})에서도 나온다 — 평형비 $\xi_\eq/(1-\xi_\eq)=e^{sF(V-U)/RT}$ 가 \eqref{eq:sm-logistic} 와
\eqref{eq:logisticsolve} 에서 같으니, 통계(이 절)와 동역학(\S\ref{sec:width})은 한 분포의 두 유도다
(\S\ref{sec:dist} 의 명제를 Part 0 이 평형 쪽에서 선결).
\item \textbf{$\Omega\ne0$ 이면 닫힌 logistic 이 아니다.} \eqref{eq:sm-eqcond} 에 상호작용까지 든 식~\eqref{eq:mu}
를 넣고 $\xi$ 좌표의 우함수 대칭(\S\ref{sec:sm-mf})을 쓰면
$RT\ln[\xi/(1-\xi)]+\Omega(1-2\xi)=sF(V-U)$, 곧 본문 식~\eqref{eq:Veq} 의 암시적 등온선이 되고,
$\Omega>2RT$(식~\eqref{eq:sm-thresh})면 비단조 — 그 갈림의 처리(spinodal 과주행·분기 중심)가
\S\ref{sec:hys}, 실측 폭의 지위가 \S\ref{sec:width}·\S\ref{sec:broadening} 다.
\end{enumerate}

\begin{figure}[t]
\centering
\begin{tikzpicture}[x=2.55cm,y=3.0cm]
\draw[-{Latex[length=1.6mm]}] (-1.55,0) -- (1.62,0) node[below,font=\scriptsize] {$V-U$ [mV]};
\draw[-{Latex[length=1.6mm]}] (-1.55,0) -- (-1.55,1.10) node[above,font=\scriptsize] {$\theta_\eq$};
\foreach \xx/\lab in {-1.0/{-100},-0.5/{-50},0/0,0.5/{50},1.0/{100}} {\draw (\xx,0.012) -- (\xx,-0.012) node[below,font=\scriptsize] {\lab};}
\draw (-1.53,1.0) -- (-1.57,1.0) node[left,font=\scriptsize] {1};
\draw (-1.53,0.5) -- (-1.57,0.5) node[left,font=\scriptsize] {0.5};
\draw[densely dotted,black!60] (-1.55,0.5) -- (1.5,0.5);
% T -> 0 step limit
\draw[densely dashed] (-1.5,1.0) -- (0,1.0) -- (0,0) -- (1.5,0);
% T = 268.15 K
\draw[black!55] plot[smooth] coordinates {(-1.500,0.9985) (-1.250,0.9955) (-1.000,0.9870) (-0.875,0.9778) (-0.750,0.9625) (-0.625,0.9373) (-0.500,0.8970) (-0.375,0.8352) (-0.250,0.7469) (-0.125,0.6320) (0.000,0.5000) (0.125,0.3680) (0.250,0.2531) (0.375,0.1648) (0.500,0.1030) (0.625,0.0627) (0.750,0.0375) (0.875,0.0222) (1.000,0.0130) (1.250,0.0045) (1.500,0.0015)};
% T = 298.15 K
\draw[thick] plot[smooth] coordinates {(-1.500,0.9971) (-1.250,0.9923) (-1.000,0.9800) (-0.875,0.9679) (-0.750,0.9488) (-0.625,0.9193) (-0.500,0.8750) (-0.375,0.8115) (-0.250,0.7257) (-0.125,0.6193) (0.000,0.5000) (0.125,0.3807) (0.250,0.2743) (0.375,0.1885) (0.500,0.1250) (0.625,0.0807) (0.750,0.0512) (0.875,0.0321) (1.000,0.0200) (1.250,0.0077) (1.500,0.0029)};
% T = 328.15 K
\draw[black!55,densely dashdotted] plot[smooth] coordinates {(-1.500,0.9951) (-1.250,0.9881) (-1.000,0.9717) (-0.875,0.9567) (-0.750,0.9342) (-0.625,0.9012) (-0.500,0.8542) (-0.375,0.7902) (-0.250,0.7077) (-0.125,0.6087) (0.000,0.5000) (0.125,0.3913) (0.250,0.2923) (0.375,0.2098) (0.500,0.1458) (0.625,0.0988) (0.750,0.0658) (0.875,0.0433) (1.000,0.0283) (1.250,0.0119) (1.500,0.0049)};
\node[font=\scriptsize,align=left] at (0.95,0.78) {$T\to0$: step\\268 / 298 / 328 K:\\$w=23.1/25.7/28.3$ mV};
\end{tikzpicture}
\caption{단일 자리 평형 점유 $\theta_\eq=[1+e^{sF(V-U)/RT}]^{-1}$(식~\eqref{eq:sm-logistic}; 신규 그림 —
스크립트 실계산 좌표, \texttt{V1013\_P21\_fig\_F2\_theta\_single\_site.py}). 전위를 올리면 점유가 내려가고
(탈리튬화), 열적 폭 $w=RT/F$ 가 온도에 비례해 넓어지며($268/298/328$ K), $T\to0$ 에서 계단(파선)으로
수렴한다. 탈리튬화 진행률 $\xi_\eq=1-\theta_\eq$ 는 같은 곡선의 좌우 거울이고, 그 미분의 종이 본문
그림~\ref{fig:logistic} 이다.}
\label{fig:sm-thetaV}
\end{figure}

\subsection{거시 열역학으로 — $G\equiv H-TS$, $\Delta G_j=-sFU_j$, Nernst 식}\label{sec:sm-macro}
\textbf{(a) 출발 — 두 언어의 같은 $\mu$.} 본문 \S\ref{sec:center} 는 거시 정의에서 출발한다 — Gibbs
자유에너지 $G\equiv H-TS$(식~\eqref{eq:gibbsdef})와 $\mu\equiv\partial G/\partial n|_{T,P}$
(식~\eqref{eq:mudef}). 통계역학 쪽 정의는 \S\ref{sec:sm-ensemble} 의 $\mu=\partial F/\partial N|_{T,V}$ 였다.
둘의 다리는 $G=F+PV$ 다 — 응축상 격자에 이온 1몰을 넣을 때의 $P\Delta v$ 몫은 $RT$·전기 일($FV$) 스케일에
비해 무시되므로
\begin{equation}
\mu=\frac{\partial G}{\partial n}\Big|_{T,P}\;\simeq\;\frac{\partial F}{\partial n}\Big|_{T,V}
\qquad(\text{삽입 고체: }P\Delta v\ll RT\ll F\,V)
\label{eq:sm-mubridge}
\end{equation}
— \S\ref{sec:sm-lattice}--\S\ref{sec:sm-electro} 에서 세운 $\mu(\theta)$ 를 본문의 거시 $\mu$ 자리에 그대로
꽂아도 되는 근거가 이 한 줄이다.

\textbf{(b) 연산 — 반응 자유에너지의 $H,S$ 분해.} \eqref{eq:sm-eqcond} 의 비배치 몫
$\Delta G_j=\mu^0-\mu_\mathrm{Li}^\mathrm{metal}$ 은 온도의 함수이고, $G\equiv H-TS$ 를 반응 차분에 적용하면
$\Delta G_j(T)=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 다. \textbf{(c) 중간식 — 평형 중심의 온도 환산.}
이를 $\Delta G_j=-sFU_j$ 와 등치하면 $\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}=-FU_j(T)$($s{=}1$) — 본문
식~\eqref{eq:Ujmid} 이고, 이항한 결과가 결과 박스 식~\eqref{eq:Uj}
($U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$, $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$)다 — 박스는
\S\ref{sec:center} 의 것을 그대로 쓰고 여기 다시 적지 않는다.

\textbf{(d) 박스 — Nernst 식으로 마감.} 마지막으로 \eqref{eq:sm-logistic} 의 $\xi_\eq$ 를 전위에 대해
뒤집으면($\xi/(1-\xi)=e^{sF(V-U)/RT}$ 의 로그) 이상 극한($\Omega=0$)의 평형 전위 곡선이 닫힌다:
\begin{equation}
\boxed{\;
\Delta G_j=-sF\,U_j,
\qquad
V_\eq(\xi)=U_j+\frac{RT}{sF}\,\ln\frac{\xi}{1-\xi}
\qquad(\Omega=0,\ s=+1)\;.}
\label{eq:sm-nernst}
\end{equation}
로그 몫의 정체는 \eqref{eq:sm-Smix} 섞임 엔트로피의 부분몰 몫이다 — Nernst 식의 $\ln[\xi/(1-\xi)]$ 는
곡선맞춤이 아니라 배치 셈법에서 온다(Chapter 2 의 식 (eq:Vxi)가 같은 결론을 발열 관점에서 재사용한다).
극한·부호 검산 — $\xi=\tfrac12$ 에서 $V=U_j$(중심), $T\!\uparrow$ 이면 로그 몫의 기울기(폭 $w=RT/F$)가
비례해 커지고, $\Delta S_{\rxn,j}>0$ 이면 \eqref{eq:Uj} 로 중심이 온도에 오른다. 상호작용 몫
$\Omega(1-2\xi)/sF$ 를 더하면 본문 식~\eqref{eq:Veq} 로 확장되고, $\Omega>2RT$ 의 비단조가
\S\ref{sec:hys} 의 히스테리시스로 이어진다.

이로써 사슬이 닫혔다 — 등확률 공준에서 Gibbs 인자(\eqref{eq:sm-gc}), 자리 하나의 점유(\eqref{eq:sm-theta}),
lattice gas 의 $\mu(\theta)$(\eqref{eq:sm-muideal}·식~\eqref{eq:mu}), 전기화학 결선(\eqref{eq:sm-eqcond}),
평형 logistic(\eqref{eq:sm-logistic})과 Nernst(\eqref{eq:sm-nernst})까지가 전부 한 분포의 전개다. 본문은
이제 이 도착점들을 코드 진행 $\mathrm N0\to\mathrm N9$ 의 입력으로 쓴다 — 기호와 규약의 표에서 시작한다
(\S\ref{sec:notation}).
```

(§1 Part 0 LaTeX 전문 끝.)

---

## 2. 재접속 표 — 원천 절 유도의 흡수·참조 매핑

원칙: 기존 결과 박스·라벨은 재수록하지 않고(교훈 ④), Part 0 은 일반형(자리당→몰)을 eq:sm-* 로 세운 뒤
본문 도착점(eq:mu·eq:gxi·eq:xieq·eq:eqcond·eq:Uj·eq:Veq)을 참조로 회수한다. "단축 제안" 열은 master 의
편입 선택지 — 채택하지 않아도 Part 0 은 독립적으로 성립한다(참조 방향이 Part 0→본문으로도 닫혀 있음).

| # | 원천(절·줄·라벨) | 내용 | Part 0 대응 | 처리 제안 |
|---|---|---|---|---|
| R1 | sec:center L417–447, eq:gibbsdef·eq:mudef·eq:eqbalance·eq:eqcond | G·μ 거시 정의, 전기화학 평형 조건, 상수 덩이 sFU | §0.5(a) 가 정의를, §0.4(a)–(c) 가 평형 조건을 확장 재유도(기준전극 차감 단계 eq:sm-workbal→eq:sm-muV 명시 — 원문의 "상수 덩이" 한 문장을 두 단계로 전개) | sec:center 의 (a)(b)(c) 를 "Part 0 \S0.4–0.5 회수" 2–3문장으로 단축 가능. 라벨 4종은 sec:center 잔류(참조 무결) 또는 Part 0 이동 중 택1 — 이동 시 eq:sm-eqcond 와 eq:eqcond 는 한쪽만 남김 |
| R2 | sec:center L448–474, eq:Ujmid·eq:Uj·codebox | ΔG=ΔH−TΔS 대입·온도 환산·박스 | §0.5(b)(c) 가 다리만 재유도, 박스는 eq:Uj 참조 | 무변경 잔류(박스·codebox 그대로) |
| R3 | sec:hys L586–597, eq:mu | Stirling 섞임 + 평균장 cθ² 유도 | §0.2(eq:sm-Smix·eq:sm-mucount)·§0.3(eq:sm-mf·eq:sm-omega — 원문의 "c" 를 z·u 미시 정의로 전개, Ω≡−(z/2)N_A u) | sec:hys (a) 첫 유도 문단을 "Part 0 \S0.3 의 식 eq:mu 회수" 1–2문장으로 단축 가능. eq:mu 라벨 잔류 필수(참조 다수) |
| R4 | sec:hys L598–610, eq:gxi·eq:gpp | ξ 좌표 전환·우함수 대칭·2계 미분 | §0.3(c)(d) 가 대칭 논거와 곡률·문턱을 세움(문턱 박스 eq:sm-thresh 는 원문에 없던 신규 박스) | eq:gxi·eq:gpp 잔류. 중복 없음 — Part 0 은 g″ 식을 본문 eq:gpp 참조로 명기하고 문턱 진술만 박스 |
| R5 | sec:hys L611–751 (eq:spinodal 이후 gap·branch 전체) | spinodal 근·artanh gap·분기 중심 | Part 0 범위 밖 — §0.3(d)·§0.4(d)(iii) 에서 전방 참조만 | 무변경 잔류 |
| R6 | sec:width L924–951 (w 이중지위) · L953–1064 (kinetic logistic, eq:bv·eq:db·eq:logisticsolve·eq:xieq) | 폭 서식·Eyring→detailed balance→logistic | 동역학 경로는 Part 0 밖. §0.4(d)(ii) 가 평형비 일치로 합류점 명시 | sec:width (d) 끝에 "평형 경로 = Part 0 \S0.4" 1문장 추가 제안. 식·박스 무변경 |
| R7 | sec:dist L1066–1139, eq:partfn·eq:fermifn | 단일 자리 GC 분포·Fermi 동형·두 경로 통합 | §0.1 이 eq:partfn 를 eq:sm-Z1 로 선행 정초, §0.4 가 (c) 대입을 올바른 부호로 재유도(아래 정정 C-1) | sec:dist (a)(b) 를 "Part 0 \S0.1 회수" 로 단축하고 (c) 는 C-1 정정 반영. keybox(전자 엔트로피 다리)·(d) 통합 문단은 잔류(LCO 연결 고유 콘텐츠). eq:partfn↔eq:sm-Z1 은 한쪽으로 통합 권장 |
| R8 | ch2 L110–188, eq:Z1·eq:occ·eq:muV·eq:logistic·eq:Vxi | 격자기체 분배함수→점유→logistic→Nernst | Part 0 §0.1·§0.4·§0.5 와 완전 평행(독립 재유도로 일치 확인) | Ch2 는 별도 문서라 무변경 잔류. 서두에 "Ch1 Part 0 과 같은 유도의 발열-관점 재구성" 상호참조 1문장 + eq:muV 의 σ_d↔s 표기 각주 제안(아래 C-2) |
| R9 | 서론 사슬 박스(ch2 L98–100) | Z→⟨n⟩→S→∂U/∂T→Q̇_rev | Part 0 사슬 박스가 Ch1 쪽 전반부(Z→⟨n⟩→μ→logistic→Nernst)를 담당 | 무변경 — 두 사슬이 eq:Z1/eq:sm-Z1 에서 접속 |

Part 0 신설 라벨 총목록: `sec:sm-found`·`sec:sm-ensemble`·`sec:sm-site`·`sec:sm-lattice`·`sec:sm-mf`·`sec:sm-electro`·`sec:sm-macro` / `eq:sm-S`·`eq:sm-fund`·`eq:sm-resv`·`eq:sm-taylor`·`eq:sm-gibbsfactor`·`eq:sm-gc`·`eq:sm-Z1`·`eq:sm-occmid`·`eq:sm-theta`·`eq:sm-factor`·`eq:sm-Smix`·`eq:sm-mucount`·`eq:sm-muideal`·`eq:sm-mf`·`eq:sm-omega`·`eq:sm-gtheta`·`eq:sm-thresh`·`eq:sm-emu`·`eq:sm-workbal`·`eq:sm-refbal`·`eq:sm-muV`·`eq:sm-eqcond`·`eq:sm-logistic`·`eq:sm-mubridge`·`eq:sm-nernst` / `fig:sm-gxi`·`fig:sm-mu`·`fig:sm-thetaV`. 기존 라벨 재사용(참조만): eq:mu·eq:gxi·eq:gpp·eq:spinodal·eq:dUhys·eq:Veq·eq:xieq·eq:wbase·eq:db·eq:logisticsolve·eq:gibbsdef·eq:mudef·eq:eqbalance·eq:eqcond·eq:Ujmid·eq:Uj·eq:partfn·fig:doublewell·fig:hysloop·fig:logistic.

---

## 3. 물리 정정 제안 (독립 재유도 근거 동반)

**C-1 (sec:dist L1088–1092 — Δμ 부호와 ⟨n⟩↔ξ 동일시 슬립; 심각도 MED, 최종 결과식 무영향).**
현행: "1몰 기준으로 $\Delta\mu=-sF(V-U_j)$ … 식 eq:fermifn 은 $\langle n\rangle=1/(1+e^{-s(V-U_j)/w_j})$ 곧
식 eq:logisticsolve·eq:xieq 의 $\xi_\eq$ 와 같은 식이다."
독립 재유도: eq:partfn 의 정의는 $\Delta\mu\equiv\varepsilon_\mathrm{occ}-\mu_\mathrm{Li}$ 이고, eq:eqcond 의
$\mu_\mathrm{Li}=\mu^0-sF(V-U)$ 와 기준 $\varepsilon_\mathrm{occ}=\mu^0$(전이 중심 기준) 아래에서
$\Delta\mu=\mu^0-\mu_\mathrm{Li}=\boldsymbol{+}sF(V-U_j)$ 다. 따라서
$\langle n\rangle=1/(1+e^{+\beta\Delta\mu})=1/(1+e^{+sF(V-U)/RT})=\theta_\eq$(V 에 감소 — "V 를 올리면
탈리튬화" 부호 검산 통과)이고, $\xi_\eq$ 는 그 여집합 $1-\langle n\rangle$ 로서 eq:logisticsolve 와 일치한다.
현행 서술은 (i) $\Delta\mu$ 부호가 정의와 반대이고 (ii) 점유 $\langle n\rangle$ 을 진행률 $\xi_\eq$ 와 직접
"같은 식"으로 동일시하며, L1095 의 "방향 부호 $\sigma_d=s$ 가 그 부호 차이를 흡수" 봉합은 $s$ 가 고정 $+1$
유도 부호(§sec:notation 표)라 성립하지 않는다. Ch2 (eq:occ→eq:logistic, L152)는 이미 올바른 부호
($\theta_\eq$ 지수 $+(V-U)/w$)로 적혀 있어 현재 두 장이 불일치 상태다. 제안: sec:dist (c) 를 Part 0
\S0.4(d)의 유도(eq:sm-logistic 도출부)로 대체 또는 위 부호로 정정. eq:xieq·eq:logisticsolve·코드는 무영향.

**C-2 (표기 조화 — 오류 아님, LOW).** ch2 eq:muV 는 평형 관계에 방향 부호 $\sigma_d$ 를 쓰고
"($\sigma_d{=}+1$ 평형 규약)" 으로 고정하는데, Ch1 은 같은 자리에 고정 부호 $s$ 를 쓰고 $\sigma_d$ 를 세
작용처(분극·분기·꼬리) 전용으로 예약한다(§sec:notation 표 L224–225). Part 0 편입 시 ch2 서두 각주 1개로
"eq:muV 의 $\sigma_d$ 는 Ch1 의 $s$ 에 해당" 조화를 제안(두 문서 모두 식 변경 불요).

---

## 4. 갈래 2 — Part II 「LCO 양극」 도입 절 LaTeX 문안

배치 제안: 현행 `sec:lco-map`(L301–355) 자리를 이 절이 대체·확장한다. 기존 `\ref{sec:lco-map}` 참조
(sec:lco-peak 각주 등)가 깨지지 않도록 `\label{sec:lco-intro}\label{sec:lco-map}` 를 병기한다.
표 `tab:lco-staging`(L325–348)은 **내용 무변경으로 이 절 안에 그대로 이동**한다(아래 문안의 `[표 이동]`
표시 위치; 재수록 diff 방지를 위해 본 드래프트에는 원문 재인쇄 생략). 일원화 대상 원문 = sec:lco-map 전문
+ sec:lco-hys ★분기 부호 문단(L846–854) + sec:lco-peak ★방향 부호 문단·각주(L1426–1437).

```latex
% ====================================================================
% ★ Part II 도입 절 신설(v1.0.13 P2.1, draft F2) — 현행 sec:lco-map 대체·확장.
%   산재한 전극-중립·방향 규약 서술(sec:lco-map / sec:lco-hys ★ / sec:lco-peak ★)의 일원화.
% ====================================================================
\subsection{Part II 도입 — 두 번째 전극 LCO: 전극-중립 골격과 방향 규약}\label{sec:lco-intro}\label{sec:lco-map}

지금까지의 기호와 매핑은 \emph{전극을 가리지 않는다}. 이 절은 그 전극-중립 골격이 정확히 무엇인지 한 번에
못박고, 그 골격을 두 번째 사례인 $\mathrm{LiCoO_2}$(LCO) 양극에 건다. 흑연 서술은 한 줄도 바뀌지 않으며,
LCO 는 ``파라미터를 갈아 끼우고 고유 항 하나를 더하는'' 두 번째 전극으로 들어온다. 본 문건이 다루는 범위는
\emph{코인 하프셀}(LCO vs Li metal) 단독이다 — 전셀 합성
($\partial U_\cell=\partial U_\mathrm{cat}-\partial U_\mathrm{an}$)은 범위 밖이며(후속), 단전극 부호와 전셀
부호를 섞지 않는다.

\textbf{(i) 전극-중립 골격 — 무엇이 전극 무관인가.}
본문 사슬에서 host 물질이 들어가지 않는 식이 다섯이다:
\begin{enumerate}[label=(\arabic*),leftmargin=2.2em,itemsep=1pt]
\item 실험조건 매핑 식~\eqref{eq:n0map} — 방향 부호 $\sigma_d$·전류 환산 $|I|=\text{c\_rate}\cdot Q_\cell$;
\item 삽입 평형 조건 식~\eqref{eq:eqcond} — 반쪽반응
$\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\mathrm{host})}$ 의 전기화학 평형은 host 의 화학
정체를 상수 $\mu^0$ 와 입력값으로만 담는다(Part 0 \S\ref{sec:sm-electro} 의 유도에 host 항이 없다);
\item 정규용액 조성 자유에너지 식~\eqref{eq:gxi} — ``동등한 자리에 리튬이 차고 빈다''는 가정 하나만 쓰며,
이는 LCO 의 팔면체 리튬 자리에도 문자 그대로 성립한다;
\item 평형 점유 logistic 식~\eqref{eq:xieq} 와 폭 서식 $w_j=n_jRT/F$(식~\eqref{eq:wbase});
\item 전하 보존식과 평형 peak 식~\eqref{eq:eqpeak} —
$\dd Q/\dd V=C_\bg+\sum_jQ_j\,\xi_{\eq,j}(1-\xi_{\eq,j})/w_j$(배경 $C_\bg$ 포함 완비형).
\end{enumerate}
전극이 들어오는 자리는 딱 두 곳이다 — (가) 전이 집합과 입력값
$j\in\mathcal J,\ (\Delta H_{\rxn,j},\Delta S_{\rxn,j},Q_j,\Omega_j,\Delta H_{a,j},\dots)$, $C_\bg$, $R_n$;
(나) 방향 라벨(충전/방전)을 $\sigma_d$ 슬롯에 먹이는 \emph{사전}(아래 (iii)). 이 둘만 바꾸면 같은 코드가
다른 전극을 그린다.

\textbf{(ii) LCO 하프셀 전이 지도 — 파라미터 교체.}
LCO 하프셀 전위는 vs Li/Li$^+$ 로 $\sim$3.9--4.2 V 영역에 있다 — 흑연 음극의 $\sim$0.1 V 와 달리 \emph{높은}
전위이나, (i) 의 골격은 그대로다. 흑연의 \code{GRAPHITE\_STAGING\_LIT}(표~\ref{tab:staging}) 4 전이에
대응하는 LCO 초기값 리스트를 \code{LCO\_MSMR\_LIT} 로 두며, 하프셀(코인, $\le$4.2--4.5 V)은 세 전이를
남긴다\cite{xia2007}: $\sim$3.90 V 의 절연체$\to$금속 천이(metal--insulator transition, MIT), $\sim$4.05 V 와
$\sim$4.17 V 의 한 쌍 order--disorder 전이다(고전압 $\sim$4.55 V 의 O3$\to$H1-3 은 하프셀 상한이
$\le$4.2--4.5 V 면 범위 밖이라 옵션으로 둔다). 이 값들은 흑연과 마찬가지로 \emph{신뢰값이 아니라 초기값}이며
(tier — 1차 문헌 Xia\cite{xia2007}$\cdot$Reynier\cite{reynier2004}$\cdot$Motohashi\cite{motohashi2009} 에서
읽은 출발점), 우리 시료 데이터로 피팅해 override 하는 전제다.

[표 이동 — 현행 표~\ref{tab:lco-staging}(L325–348)를 캡션까지 무변경으로 이 위치에 둔다.]

흑연이 전이별 $(\Delta H_\rxn,\Delta S_\rxn,Q,\Omega,\Delta H_a,\dots)$ 키를 갖듯 LCO 전이도 같은 키 구조를
갖되 값만 표~\ref{tab:lco-staging} 의 양극 영역으로 바뀐다. 단 하나의 구조적 차이는 T1 에 흑연엔 없는
\emph{전자 엔트로피 항} $\Delta S_e(x,T)$ 가 더해지는 것이며(MIT 고유), 그것이 \S\ref{sec:lco-electronic} 의
새 절이다. $\Omega_j^\mathrm{cat}$ 는 아직 수치 미배정이다 — 표에도 코드 \code{LCO\_MSMR\_LIT} 에도 값이
없고, 미배정 시 구현은 $\Omega=0$ 폴백으로 히스 분기를 비활성한다(\S\ref{sec:lco-hys} two-phase
calibration). 따라서 $\Omega_j^\mathrm{cat}$·동역학 키가 round-trip 피팅으로 배정되기 전에는, 아래 세 방향
작용처 중 실질 활성은 분극뿐이다.

\textbf{(iii) ★방향 규약 — $\sigma_d$ 슬롯의 물리 내용(전극-중립 읽기의 일원화).}
평형 중심$\cdot$폭$\cdot$평형 종은 방향과 무관하고, $\sigma_d$ 는 세 작용처 — 분극(\S\ref{sec:pol})$\cdot$
분기(\S\ref{sec:hys})$\cdot$꼬리(\S\ref{sec:tail}) — 로만 들어간다. 그 슬롯이 실어 나르는 물리 내용은 셀
방향 라벨이 아니라 다음 한 줄이다:
\begin{equation}
\boxed{\;\sigma_d=+1\ \Longleftrightarrow\ \text{작동 전극의 \emph{탈리튬화}(산화, $\xi:0\to1$, 전위 오름 진행)}\;}
\label{eq:lco-dirconv}
\end{equation}
— 흑연도 LCO 도 탈리튬화에서 하프셀 전위가 \emph{오른다}(흑연 $\sim$0.08$\to$0.21 V, LCO
$\sim$3.9$\to$4.2 V)는 사실이 이 규약을 전극-중립으로 만든다. 셀 라벨과의 사전은 전극마다 다르다:
흑연 음극 하프셀은 \emph{방전}이 탈리튬화라 방전 곡선이 $\sigma_d=+1$ 슬롯(라벨과 물리가 겹침)이고, LCO
하프셀은 \emph{충전}이 탈리튬화($x$ 감소·전위 상승)라 \textbf{충전 곡선이 $\sigma_d=+1$ 슬롯, 방전(리튬화·
전위 하강) 곡선이 $\sigma_d=-1$ 슬롯}이다(그림~\ref{fig:lco-dirmap}). 셀 라벨의 의미론(방전은 LCO 엔
Li$^+$ 유입·Co$^{4+}\!\to$Co$^{3+}$ 환원·$x$ 증가·전위 하강) 자체는 그대로 참이다 — 라벨 의미론과 모델
입력 슬롯 규칙은 층위가 다르며, 본 절의 규칙은 후자다. 이렇게 읽으면 세 작용처의 부호가 흑연과 1:1 로
유지된다:
\begin{enumerate}[label=(\alph*),leftmargin=2.2em,itemsep=1pt]
\item \emph{분극}(식~\eqref{eq:vn}) — $\sigma_d=+1$(산화 전류)에서 $V_\app>V_n$: 흑연 방전과 LCO 충전이
같은 부호로 성립;
\item \emph{분기}(식~\eqref{eq:Ubranch}·\eqref{eq:lco-Ubranch}) — 탈리튬화 가지가 위($+\tfrac12$),
리튬화 가지가 아래($-\tfrac12$): 과주행 기하(그림~\ref{fig:hysloop} — 탈리튬화는 상승 가지 극대
$\xi_s^-$ 까지, 리튬화는 극소 $\xi_s^+$ 까지)가 전극 무관한 이중웰 성질이라, ``탈리튬화 봉우리가 높은
전위 쪽''(흑연 $U^{\dis}>U^{\chg}$ 와 동일한 물리)이 LCO 에서도 유지된다;
\item \emph{꼬리}(식~\eqref{eq:reversal}) — 꼬리는 진행의 시간상 뒤쪽으로 늘어지므로, $\sigma_d=+1$
(진행 $=$ 전위 오름)은 격자 오름차순이 곧 시간 순서라 역전이 불요하고 $\sigma_d=-1$ 은 격자를 뒤집어
필터한다: LCO 충전이 흑연 방전과, LCO 방전이 흑연 충전과 같은 처리를 받는다.
\end{enumerate}
평형 종 자체는 이 선택에 불변이다 — 여집합 항등식 $1-\xi_{\eq}^{(\sigma_d)}=\xi_{\eq}^{(-\sigma_d)}$
(식~\eqref{eq:lco-comp})와 $\xi(1-\xi)$ 의 $\xi\leftrightarrow1-\xi$ 대칭 때문에 어느 방향 읽기로도 같은
봉우리가 나오고, 방향 읽기가 갈라놓는 것은 위 세 작용처뿐이다.

\textbf{(iv) MSMR 예고 — 같은 골격의 양극 표준어.}
이 logistic 골격은 양극 문헌의 표준 모델인 multi-species, multi-reaction(MSMR) 모델\cite{msmr2024}과
1:1 사전으로 맞물린다 — $U\leftrightarrow V$, $U_j^0\leftrightarrow U_j^{\,d}$,
$\omega_j\leftrightarrow w_j$, $X_j\leftrightarrow Q_j$, 그리고 방향 인자 $f=+\sigma_d$
(식~\eqref{eq:lco-msmrmap}; 같은 물리량끼리 짝짓는 진행률$\leftrightarrow$진행률 pairing 의 유일해).
★같은 logistic 이라는 것은 \emph{함수형 동형이지 물리량 동일이 아니다} — MSMR 의 $x_j/X_j$ 는 점유
(리튬화 분율), 본 문건의 $\xi$ 는 탈리튬화 진행률이라 서로 여집합이며, 이를 직접 등치하면 부호가 뒤집힌다.
유도·변환 폐쇄·코드 대응은 \S\ref{sec:lco-code} 가 닫는다. 그 전까지(N1--N5)는 흑연과 LCO 가 \emph{같은
식}을 공유하므로, 다음 절들은 흑연으로 식을 세운 뒤 LCO 파라미터를 끼우는 순서로 간다.

\begin{figure}[t]
\centering
\begin{tikzpicture}[
  node distance=3.2mm and 4.5mm,
  lab/.style={draw,rounded corners=2pt,minimum height=6.6mm,minimum width=21mm,inner xsep=4pt,font=\scriptsize,align=center,fill=black!4},
  slotP/.style={lab,fill=black!14,thick},
  slotM/.style={lab,fill=black!4},
  hdr/.style={font=\scriptsize\itshape,align=center},
  ar/.style={-{Latex[length=1.6mm]},thick}]
% ---- graphite anode half-cell ----
\node[hdr] (gh) {graphite anode half-cell ($\sim$0.08--0.21 V vs Li)};
\node[lab,below=4.5mm of gh,xshift=-24mm] (gd) {label: discharge};
\node[lab,below=of gd] (gc) {label: charge};
\node[lab,right=of gd] (gdd) {delithiation\\$\xi:0\to1$, $V\uparrow$};
\node[lab,right=of gc] (gcc) {lithiation\\$\xi:1\to0$, $V\downarrow$};
\node[slotP,right=of gdd] (gp) {$\sigma_d=+1$};
\node[slotM,right=of gcc] (gm) {$\sigma_d=-1$};
\draw[ar] (gd)--(gdd); \draw[ar] (gdd)--(gp);
\draw[ar] (gc)--(gcc); \draw[ar] (gcc)--(gm);
% ---- LCO cathode half-cell ----
\node[hdr,below=17mm of gc,xshift=24mm] (lh) {LCO cathode half-cell ($\sim$3.9--4.2 V vs Li)};
\node[lab,below=4.5mm of lh,xshift=-24mm] (lc) {label: charge};
\node[lab,below=of lc] (ld) {label: discharge};
\node[lab,right=of lc] (lcc) {delithiation\\$x\downarrow$, $\xi:0\to1$, $V\uparrow$};
\node[lab,right=of ld] (ldd) {lithiation\\$x\uparrow$, $\xi:1\to0$, $V\downarrow$};
\node[slotP,right=of lcc] (lp) {$\sigma_d=+1$};
\node[slotM,right=of ldd] (lm) {$\sigma_d=-1$};
\draw[ar] (lc)--(lcc); \draw[ar] (lcc)--(lp);
\draw[ar] (ld)--(ldd); \draw[ar] (ldd)--(lm);
% ---- action sites ----
\node[hdr,below=16mm of ld,xshift=24mm] (ah) {direction acts only at three sites (equilibrium peak shape is invariant)};
\node[lab,below=4mm of ah,minimum width=96mm,align=center] (act)
 {$\sigma_d=+1$: polarization $V_\app>V_n$ (oxidation) $\cdot$ branch $+\tfrac12$ (upper) $\cdot$ tail: no grid reversal\\
  $\sigma_d=-1$: mirror of all three};
\end{tikzpicture}
\caption{충$\cdot$방전 라벨과 탈리튬화 방향의 대응(신규 그림). $\sigma_d$ 슬롯의 물리 내용은 셀 라벨이
아니라 ``작동 전극의 탈리튬화 $=+1$''(식~\eqref{eq:lco-dirconv})이다 — 흑연 하프셀은 방전이, LCO 하프셀은
충전이 $\sigma_d=+1$ 슬롯(음영 상자)에 간다. 방향은 분극$\cdot$분기$\cdot$꼬리 세 작용처에만 작용하고
평형 종은 $\xi\leftrightarrow1-\xi$ 교환에 불변이다(식~\eqref{eq:lco-comp}).}
\label{fig:lco-dirmap}
\end{figure}
```

### 4b. 잔여 원문 대체 문안(일원화 후 단축)

- **sec:lco-hys ★분기 부호 문단(L846–854) →** 다음 1문장으로 대체:
  「\textbf{★분기 부호.} 식~\eqref{eq:lco-Ubranch} 의 $\sigma_d$ 슬롯은 \S\ref{sec:lco-intro} 의 전극-중립
  규약(식~\eqref{eq:lco-dirconv})을 따른다 — 탈리튬화 가지가 위($+\tfrac12$)$\cdot$리튬화 가지가
  아래($-\tfrac12$)이고, LCO 하프셀에서는 충전이 탈리튬화라 충전 곡선이 $\sigma_d=+1$ 슬롯이다.」
- **sec:lco-peak ★방향 부호 문단+각주(L1426–1437) →** 다음 1–2문장으로 대체:
  「\textbf{★방향 슬롯.} 이후의 $\sigma_d$ 는 \S\ref{sec:lco-intro}(iii) 의 규약대로 세 작용처(분극$\cdot$
  분기$\cdot$꼬리) 모두에서 ``탈리튬화 진행 $=+1$''로 먹인다 — LCO 데이터에서는 충전 곡선에
  $\sigma_d=+1$, 방전 곡선에 $\sigma_d=-1$. 평형 종은 이 선택에 불변이다(식~\eqref{eq:lco-comp}).」
- 두 대체 모두 기존 라벨·식·표는 건드리지 않는다. `\label{sec:lco-map}` 는 신설 절에 병기되므로
  기존 참조(sec:lco-peak 각주의 `\S\ref{sec:lco-map}` 등)는 자동으로 신설 절을 가리킨다 — 각주 자체가
  대체 문안으로 흡수되므로 잔존 참조는 코드 docstring(`Ch1 sec:lco-peak 방향 슬롯 한정`) 쪽 표현만
  master 확인 대상이다.

---

## 5. figure 목록 (전부 실제 식 평가로 생성 — 날조 0)

| # | 라벨 | 목적 | 형식 | 배치 | 생성 스크립트 / 좌표 근거 |
|---|---|---|---|---|---|
| F-1 | `fig:sm-gxi` | 정규용액 f(ξ)/RT 의 Ω-가족: 단일 웰→평탄(Ω=2RT)→이중웰, spinodal 점 | TikZ(§1 본문 내장, 좌표 = 스크립트 실계산) + 검증 PNG | Part 0 §0.3 (d) 옆 | `Claude\results\process\V1013_P21_fig_F2_gxi_doublewell.py` (+`..._gxi_tikz.txt`, `..._gxi_doublewell.png`) |
| F-2 | `fig:sm-mu` | μ(θ) 개형: Ω≤2RT 단조 / Ω=2RT 평탄 변곡 / Ω>2RT 비단조(극값=spinodal) | TikZ(내장) + 검증 PNG | Part 0 §0.3 (d) 옆 | `V1013_P21_fig_F2_mu_theta.py` (+`..._mu_tikz.txt`, `..._mu_theta.png`) |
| F-3 | `fig:sm-thetaV` | 단일 자리 점유 θ_eq(V−U): 열적 폭 RT/F 의 T-의존(268/298/328 K)·T→0 계단 극한 | TikZ(내장) + 검증 PNG | Part 0 §0.4 (d) 옆 | `V1013_P21_fig_F2_theta_single_site.py` (+`..._theta_tikz.txt`, `..._theta_single_site.png`) |
| F-4 | `fig:lco-dirmap` | 충·방전 라벨↔탈리튬화 방향↔σ_d 슬롯 대응도(흑연/LCO 두 하프셀) + 3작용처 요약 | TikZ 도식(곡선 없음 — 개형 평가 불요) | 갈래 2 도입 절 (iii) 옆 | §4 fence 내장 (스크립트 불요) |

캡션은 각 figure 환경 안에 포함(§1·§4 참조). 캡션·본문 라벨 전부 문서 관례(내부 텍스트 영어 ASCII·한글 캡션) 준수.
조판 검증: 문서 preamble 재현 래퍼로 xelatex 2-pass 시험 조판(8쪽, hard error 0) 후 전 페이지 육안 확인 —
그림 4종 렌더 정상, fig:sm-gxi 라벨 혼잡 1건 발견·수정 후 재조판 확인.

---

## 6. 물리 자체검수 기록 (절별 루핑 — 각 단위 작성 직후 수행)

**§0.0 (앙상블·Z·μ·GC)**
- 부호: `∂S/∂N|_{E,V}=−μ/T` — dE=TdS−PdV+μdN 직접 이항으로 재유도. Gibbs 인자 `+βμN` — μ 큰 저장조가 입자를 계로 밀어 N 큰 상태 가중↑, 입자 흐름 방향(고μ→저μ) 재유도 일치.
- 차원: βE·βμN 무차원. ⟨N⟩ 식 지수 미분 재계산(∂lnΞ/∂μ=β⟨N⟩) 통과.
- 극한: β→0 등확률·β→∞ 바닥상태 명기.
- 정합: ch2 L113–116 의 대정준 설정 서술과 일치.

**§0.1 (단일 자리)**
- eq:sm-Z1 = ch1 eq:partfn(L1077) = ch2 eq:Z1(L124) 삼중 일치 확인(정의 Δμ=ε−μ 기준).
- θ 극한: β→∞ 계단(μ−ε 부호별 1/0)·β→0 → ½·μ→±∞ → 1/0 — 4개 코너 전부 손계산.
- 교차검증: ⟨n⟩ 를 확률 가중 평균과 ∂lnΞ₁/∂μ 두 경로로 계산해 일치.
- 가드 ②(함수형 동형≠물리량 동일): Fermi–Dirac 대수 공유·물리량 상이 명기. 양자역학 미도입(배타성=기하).

**§0.2 (lattice gas)**
- Stirling: lnW=MlnM−nlnn−(M−n)ln(M−n) → −M[θlnθ+(1−θ)ln(1−θ)] 대입 재계산.
- μ=∂F/∂n: F=nε+k_BT[nln n−nlnM+(M−n)ln(M−n)−(M−n)lnM] 미분 → ε+k_BT ln[θ/(1−θ)] (ln M 항 상쇄 확인).
- GC 역산 경로와 일치(e^{β(ε−μ)}=(1−θ)/θ). 두 경로 합치 = 앙상블 동등성 서술.
- 극한: θ→0/1 에서 μ→∓∞·θ=½ 에서 μ⁰·S_mix 최대 k_Bln2 (−2×½ln½=ln2 재계산).

**§0.3 (mean-field Ω)**
- 평균장 에너지: (Mθ)×(zθ)×u×½=(Mz/2)uθ² — 이중계수 ½ 명시.
- 항등 분해 θ²=θ−θ(1−θ) 전개 재계산. Ω≡−(z/2)N_A u: u<0(인력)⇔Ω>0(상분리) — ch1 L590–591(Ω≡−c)·ch2 eq:BW 부호 서술과 삼중 일치.
- μ(θ) 미분: 로그 몫 RT ln[θ/(1−θ)](±1 상쇄)·상호작용 몫 Ω(1−2θ) — eq:mu 와 자구 일치.
- 우함수 대칭 f(1−ξ)=f(ξ) → f′(1−ξ)=−f′(ξ): sec:hys L649–654 의 1계 미분 논거와 정합.
- 문턱: min RT/[ξ(1−ξ)]=4RT(ξ=½) → Ω≤2RT ⇔ g″≥0 전역, Ω>2RT ⇔ 이중웰. T_c=Ω/2R — L691 일치.
- 극한 Ω→0(이상 환원)·Ω→2RT∓(평탄 변곡/웰 분리) 명기.
- 수치: f(0.5)/RT=0.0569·f(0.07)/RT=−0.0583 (Ω=3RT) — 기존 fig:doublewell 좌표(0.057/−0.058)와 일치. spinodal 0.2113/0.7887 = eq:spinodal 해석해. μ/RT 극값 ±0.4151 손계산(ln0.2679=−1.317, 3×0.5774=1.732) 일치.

**§0.4 (전기화학 연결)**
- 기준전극 차감: (μ_{Li+}+Fφ_S) 상쇄·−F(φ_M−φ_ref)=−FV — z 부호(Li⁺:+1, e⁻:−1) 각각 대입 재유도.
- U 재포장: μ_Li=μ⁰−F(V−U), ΔG=μ⁰−μ_Li^metal=−FU — eq:eqcond·"U_j>0⇔ΔG<0" 부호 읽기와 일치.
- logistic: θ=1/(1+e^{+sF(V−U)/RT}) → V↑⇒θ↓(탈리튬화) 부호 검산. ξ=1−θ=1/(1+e^{−sF(V−U)/RT}) = eq:logisticsolve = ch2 eq:logistic. 자리당 지수 β(ε−μ_Li) 몰 환산 = +sF(V−U)/RT 일치(→ C-1 정정 근거).
- detailed balance: ξ_eq/(1−ξ_eq)=e^{sF(V−U)/RT}=e^{A/RT}(A=sF(V−U)) — eq:db 와 평형비 일치(동역학 경로 무손상).
- Ω≠0: 우함수 대칭 경유 RT ln[ξ/(1−ξ)]+Ω(1−2ξ)=sF(V−U) → eq:Veq 자구 일치. Ω>2RT 비단조 → sec:hys 인계.
- 극한: T→0 계단·T↑ 폭 비례(w=23.1/25.7/28.3 mV @268/298/328 K — 스크립트 수치)·V≫U ξ→1.

**§0.5 (거시 열역학)**
- G=F+PV 다리: PΔv(≈1 J/mol@1 atm·10 cm³) ≪ RT(2.5 kJ/mol) ≪ FV(8.2 kJ/mol@0.085 V) 스케일 부등식 수치 확인.
- ΔG(T)=ΔH−TΔS → eq:Ujmid → eq:Uj 참조(박스 재수록 없음 — 교훈 ④).
- Nernst 역산: ln[ξ/(1−ξ)]=sF(V−U)/RT 이항 — ch2 eq:Vxi 와 일치. ξ=½⇒V=U·∂U/∂T=ΔS/F>0(ΔS>0) 부호 — sec:lco-center verifybox 방향과 정합.

**갈래 2 (Part II 도입 절)**
- 전극-중립 5식: 보존식 출발·C_bg 완비형으로 eq:eqpeak 인용(교훈 ③).
- σ_d=+1⇔탈리튬화⇔전위 오름 진행: 흑연(0.08→0.21 V)·LCO(3.9→4.2 V) 두 전극에서 성립 확인 — 규약의 전극-중립성 근거.
- 3작용처: (a) 분극 — 산화 전류에서 V_app>V_n(ch1 L370–371·L1431) (b) 분기 — 탈리튬화 가지 +½(L846–854, 과주행 기하) (c) 꼬리 — eq:reversal 의 σ_d≥0 무역전/σ_d<0 역전과 "진행=전위 오름⇔격자 오름차순=시간순" 재유도 일치.
- f=+σ_d: 확정 판정(V1012_P43_verify10) 지위 그대로 인용 — 재론·재유도 없음(eq:lco-msmrmap 참조만). 가드 ② 문장 유지.
- Ω_j^cat 수치 미배정 지위 유지(교훈 ⑥) — "분기 비활성·실질 방향 의존=분극" 은 ch1 L780–785 + FITTING_GUIDE L10 근거, "배정되기 전에는" 한정어 동반.
- 라벨 무결: \label{sec:lco-map} 병기로 기존 \ref 보존. 표 tab:lco-staging 무변경 이동.
- 흑연 서술 무변경(sec:lco-map 원칙 승계) — 대체 문안 2건 모두 참조 축약형.

**교차 정합(전 단위)**
- Part 0 → 본문 도착점 회수 라벨: eq:mu·eq:gxi·eq:xieq·eq:eqcond·eq:Uj·eq:Veq·eq:db — 각 위치에 재사용 명시.
- artanh·Ω_j^cat 표기 승계(교훈 ⑤ — Part 0 은 artanh 미사용 구간, 갈래 2 는 기존 식 참조로만 등장).
- 신설 eq:sm-* 25건·fig 4건 — orphan 0(각 라벨은 후속 참조 또는 (d) 박스 수렴 흐름 내 사용).
- xelatex 시험 조판 2-pass: hard error 0·8쪽 완주·전 페이지 육안 확인(내부 sm-* 상호참조 해소; 본문 라벨 ?? 는 래퍼 고립 탓으로 정상).

---

## 7. 5줄 요약

1. Part 0 「통계역학 기초」 6개 소절(앙상블→단일 자리→lattice gas→평균장 Ω→전기화학 logistic→거시 열역학·Nernst)을 (a)–(d) 단계·eq:sm-* 25개 라벨·신규 박스 6개로 작성 — 기존 박스 재수록 0, 도착점은 eq:mu·eq:gxi·eq:xieq·eq:eqcond·eq:Uj 참조 회수.
2. 갈래 2: 현행 sec:lco-map 를 대체·확장하는 Part II 도입 절을 신설 — 전극-중립 5식 골격, σ_d 규약 박스(eq:lco-dirconv: 탈리튬화=+1·LCO 충전↦+1), 방향 3작용처, MSMR 예고(f=+σ_d 확정 지위 유지), ★문단 2건의 참조 축약 대체 문안 포함.
3. figure 4종 전부 실제 식 평가 좌표로 제작(스크립트 3본 + TikZ 내장 4본), 문서 preamble 재현 래퍼로 xelatex 시험 조판·육안 검증까지 완료.
4. 물리 정정 제안 2건 — C-1: sec:dist 의 Δμ 부호(+sF(V−U) 가 정의와 일치; 현행 −부호는 ⟨n⟩↔ξ 여집합 슬립, ch2 와도 불일치) [MED, 결과식 무영향] / C-2: ch2 eq:muV 의 σ_d↔s 표기 조화 [LOW].
5. ★최약점 자기표시: (i) C-1 은 독립 재유도 근거를 달았으나 원문 저자의 관용적 ⟨n⟩ 표기 의도와의 삼각검증은 master 몫, (ii) Part 0 의 절 번호 체계("0장" 카운터 처리)와 TikZ figure 의 실문서 페이지 흐름 배치는 래퍼 검증만 거쳐 실편입 시 재확인 필요, (iii) 재접속 표 R1·R7 의 라벨 이동/잔류 선택은 참조 무결성에 민감해 편입 시 grep 전수 확인을 전제로 했다.
