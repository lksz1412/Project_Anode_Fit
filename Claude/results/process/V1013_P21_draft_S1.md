# V1013 P2.1 — Part 0 통계역학 기초 + Part II 도입 드래프트 (__ID__ = S1)

> N=6 경쟁(무통신 독립) 중 S1. 아래는 draft 산출물 — tex·코드 무수정, 편입은 master 권한. 허위 attribution 0·추정 0(전부 원천 줄 근거 병기). 원천 전문 정독 완료: `graphite_ica_ch1_v1.0.13.tex` L1–260(기호·규약)·L301–355(sec:lco-map)·L411–475(sec:center)·L476–572(sec:lco-center)·L578–751(sec:hys)·L752–916(sec:lco-hys, ★분기 부호 문단 L846–854 포함)·L918–1139(sec:width·sec:dist)·L1395–1487(sec:lco-peak, ★방향 부호 문단 L1426–1437 포함) / `graphite_ica_ch2_v1.0.13.tex` L1–260(eq:Z1 절 전체) / `V1012_P43_verify10.md` 전문(§2, f=+σ_d 확정 판정).

---

## 0. 재유도 선언(교훈 카드 ① 준수)

이하 Part 0 의 모든 식은 원천 문서의 결과를 **베끼지 않고** grand canonical 앙상블(grand-canonical ensemble)의 1차 원리에서 다시 세운다. 도달하는 최종형(eq:sm-mutheta, eq:sm-xieq-ideal 등)이 기존 eq:mu·eq:xieq·eq:Z1·eq:occ·eq:fermifn 과 일치하는 것은 **같은 물리를 다른 경로로 검산했다는 뜻**이며(§6 대조표), 우연한 형식 일치가 아니라 grand canonical 평형이 유일하기 때문이다. 부호는 §sec:notation 의 기존 규약(s=+1 유도 고정 부호, 방향 부호 σ_d 는 응용 계층에서 후행 도입)을 그대로 쓰되, 그 규약 위에서 전개는 매 단계 독립적으로 다시 밟는다.

---

## 1. Part 0 — 통계역학 기초 (LaTeX 전문)

> 배치 권고: 서론(`서론 — 이 문건이 따라가는 것`) 뒤·`\S\ref{sec:notation}`(기호와 규약) 앞. 아래 절 번호는 자리표시자 "P0.n"이며 최종 numbering(1.\arabic{section} 승계 여부)은 master 편입 시 결정. 신설 라벨 프리픽스 `eq:sm-*` 전량 기존 라벨과 충돌 0(전수 grep 확인 완료 — 아래 §6).

```latex
% ====================================================================
\section*{Part 0 — 통계역학 기초}\label{part:sm}
\addcontentsline{toc}{section}{Part 0 --- 통계역학 기초}
% ====================================================================
이 장은 뒤따르는 모든 평형식 — 전이 중심 $U_j$, 히스테리시스 gap $\Delta U_j^\hys$, 평형 점유
$\xi_{\eq,j}$ — 이 어디서 오는지를 통계역학(statistical mechanics)의 가장 낮은 층위에서부터 쌓는다.
계는 줄곧 하나다 — 삽입 자리(intercalation site)에 리튬이 들고 나는 격자기체(lattice gas). 이
계에 앙상블(ensemble) 언어를 입히면, 이후 장들이 쓰는 모든 식이 가정이 아니라 결과로 나온다.
통계역학을 미리 배우지 않은 독자를 기준으로 쓰되, 산문은 다리에만 쓰고 본문은 식이 끈다.

% ====================================================================
\subsection*{P0.1 앙상블과 미시상태 — Boltzmann 인자가 나오는 곳}\label{sec:sm-ensemble}
% ====================================================================
\textbf{(a) 출발 — 등확률 원리.} 고립계(에너지 $E$ 고정)의 평형은 그 에너지를 갖는 모든 접근 가능한
미시상태(microstate)를 \emph{같은 확률로} 실현한다는 것이 통계역학의 근본 가정(등확률 원리)이다.
미시상태 수를 $\Omega(E)$ 라 하면 Boltzmann 엔트로피는 $S=k_B\ln\Omega(E)$($k_B$ = Boltzmann 상수)다.
주목하는 작은 계 하나만 고립시켜 두는 대신, 그 계를 훨씬 큰 저장조(reservoir, 열욕(heat bath))와
접촉시켜 계+저장조 전체를 고립계로 둔다 — 이렇게 하면 계는 특정 미시상태 $i$(에너지 $E_i$)에 있으면서도
저장조와 에너지를 주고받을 수 있다.

\textbf{(b) 연산 — 계가 저장조보다 훨씬 작다.} 전체 에너지 $E_\mathrm{tot}=E_i+E_R$ 는 고정이므로, 계가
미시상태 $i$ 에 고정된 채(계의 미시상태는 지정됐으므로 더 셀 것이 없다) 저장조가 가질 수 있는 미시상태
수만 세면 그것이 곧 "계가 상태 $i$ 에 있는" 전체 미시상태 수다:
\begin{equation}
P(i)\ \propto\ \Omega_R(E_\mathrm{tot}-E_i)\ =\ \exp\!\Big[\frac{S_R(E_\mathrm{tot}-E_i)}{k_B}\Big].
\label{eq:sm-boltzmann0}
\end{equation}
저장조가 계보다 훨씬 크므로($E_i\ll E_\mathrm{tot}$) $S_R$ 을 $E_i$ 에 대해 1차까지 전개하면
\begin{equation}
S_R(E_\mathrm{tot}-E_i)\ \approx\ S_R(E_\mathrm{tot})-E_i\frac{\partial S_R}{\partial E_R}
\ =\ S_R(E_\mathrm{tot})-\frac{E_i}{T}
\label{eq:sm-taylor0}
\end{equation}
($1/T\equiv\partial S/\partial E$ 가 열역학적 온도의 정의이며, 계와 저장조가 열평형이라 저장조 온도 $=$
계 온도 $T$). \textbf{(c) 중간식 — 지수화.} 식~\eqref{eq:sm-taylor0} 를 \eqref{eq:sm-boltzmann0} 에 넣으면
$P(i)\propto e^{S_R(E_\mathrm{tot})/k_B}\times e^{-E_i/(k_BT)}$ 인데 앞 인자는 $i$ 에 무관한 상수이므로
\begin{equation}
P(i)\ \propto\ e^{-\beta E_i},\qquad \beta\equiv\frac{1}{k_BT}
\label{eq:sm-boltzmann}
\end{equation}
— 이것이 Boltzmann 인자(Boltzmann factor)다. \textbf{(d) 박스 — 캐노니컬 분배함수.} 정규화($\sum_iP(i)=1$)하면
\begin{equation}
\boxed{\;P(i)=\frac{e^{-\beta E_i}}{Z},\qquad Z\equiv\sum_ie^{-\beta E_i}\;}
\label{eq:sm-canonical}
\end{equation}
$Z$ 가 캐노니컬 분배함수(canonical partition function)다 — 계의 모든 평형 열역학량이 이 한 함수의
미분으로 나온다는 것이 통계역학의 중심 결과이며, 다음 절은 이를 입자수까지 교환하는 문제로 넓힌다.

% ====================================================================
\subsection*{P0.2 화학퍼텐셜의 물리적 의미와 grand canonical 앙상블}\label{sec:sm-mu}
% ====================================================================
\textbf{(a) 출발 — 이미 아는 열역학적 정의.} 화학퍼텐셜(chemical potential) $\mu$ 는
$\mu\equiv\partial G/\partial n|_{T,P}$(1몰 첨가당 Gibbs 자유에너지 변화)로 정의된다. 통계역학이
이 정의에 주는 몸(body)은 하나다 — $\mu$ 는 \emph{입자 1개(1몰)를 계에 더하는 데 드는 자유에너지
비용}이다. 이 비용이 양이면 입자를 밀어내는 쪽으로, 음이면 끌어들이는 쪽으로 계가 반응한다.

\textbf{(b) 연산 — 계가 입자도 교환한다.} \S\ref{sec:sm-ensemble} 은 계+저장조가 \emph{에너지}만
교환했다. 이제 저장조가 \emph{입자}(리튬)도 내주는 저장조라 하고(입자 저장조는 화학퍼텐셜 $\mu$ 로
특성화된다), 전체(계+저장조)의 입자수 $N_\mathrm{tot}=N_i+N_R$ 도 고정이라 하자. \S\ref{sec:sm-ensemble}(b)
와 같은 논리로, 계가 미시상태 $i$(에너지 $E_i$, 입자수 $N_i$)에 있을 확률은 저장조 엔트로피를 이번엔
$E,N$ \emph{두 변수}로 1차 전개해서 얻는다:
\begin{equation}
S_R(E_\mathrm{tot}-E_i,\,N_\mathrm{tot}-N_i)\ \approx\ S_R(E_\mathrm{tot},N_\mathrm{tot})
-E_i\frac{\partial S_R}{\partial E_R}-N_i\frac{\partial S_R}{\partial N_R}
\ =\ S_{R,0}-\frac{E_i}{T}+\frac{\mu N_i}{T}
\label{eq:sm-taylor1}
\end{equation}
($\partial S/\partial N|_{E,V}=-\mu/T$ — 기본 열역학 항등식 $\dd S=\tfrac1T\dd E+\tfrac{P}T\dd V
-\tfrac\mu T\dd N$ 에서 바로 읽힌다). \textbf{(c) 중간식 — 지수화.}
\begin{equation}
P(i)\ \propto\ \exp\!\Big[-\frac{E_i-\mu N_i}{k_BT}\Big]\ =\ e^{-\beta(E_i-\mu N_i)}.
\label{eq:sm-taylor2}
\end{equation}
\textbf{(d) 박스 — grand canonical 분배함수.} 정규화하면
\begin{equation}
\boxed{\;P(i)=\frac{e^{-\beta(E_i-\mu N_i)}}{\Xi},\qquad
\Xi\equiv\sum_ie^{-\beta(E_i-\mu N_i)}\;}
\label{eq:sm-grand}
\end{equation}
$\Xi$ 가 대정준(grand-canonical) 분배함수다. 지수의 $e^{\beta\mu N_i}$ 인자가 "입자를 $N_i$ 개 가진
상태는 그만큼 Gibbs 인자가 부스트된다"는 뜻이고, 그 부스트의 크기를 정하는 것이 바로 (a)의 $\mu$ —
입자 1개 추가의 자유에너지 비용이 낮을수록($\mu$ 가 클수록) 그 상태가 더 잘 실현된다.

\begin{keybox}
\textbf{앙상블 사다리.} 고립계(등확률) $\to$ 계+열저장조(Boltzmann 인자, 캐노니컬) $\to$
계+열$\cdot$입자저장조(Gibbs 인자, 대정준). 삽입 전극의 리튬 자리는 전해질(리튬 저장조,
$\mu$ 로 특성화)$\cdot$외부회로(전자 저장조)와 둘 다 접촉하므로 마지막 층 — 대정준 — 이 맞는 앙상블이다.
\end{keybox}

% ====================================================================
\subsection*{P0.3 단일 삽입 자리 — 2-상태 grand canonical 분배함수}\label{sec:sm-site}
% ====================================================================
\textbf{(a) 출발 — 두 미시상태.} 삽입 자리 하나를 떼어 보자. 비어 있으면($E=0,N=0$) 미시상태 하나,
리튬 하나가 들어 있으면($E=\varepsilon_0,N=1$) 미시상태 하나 — 자리당 정확히 두 미시상태다.
\textbf{(b) 연산 — \eqref{eq:sm-grand} 대입.}
\begin{equation}
\Xi_1\ =\ \sum_{N=0,1}e^{-\beta(E-\mu N)}\ =\ 1+e^{-\beta(\varepsilon_0-\mu)}.
\label{eq:sm-Z1}
\end{equation}
\textbf{(c) 중간식 — 평균 점유.} 평균 입자수는 $\langle N\rangle\equiv\sum_iN_iP(i)$ 이므로
$\langle N\rangle=[0\cdot1+1\cdot e^{-\beta(\varepsilon_0-\mu)}]/\Xi_1$, 분모$\cdot$분자를 $e^{-\beta(\varepsilon_0-\mu)}$
로 나누면 \textbf{(d) 박스.}
\begin{equation}
\boxed{\;\theta\equiv\langle N\rangle=\frac{1}{1+e^{\beta(\varepsilon_0-\mu)}}\;}
\label{eq:sm-theta1}
\end{equation}
\begin{signbox}
\textbf{극한.} $\beta\to0$($T\to\infty$): $e^{\beta(\varepsilon_0-\mu)}\to1\Rightarrow\theta\to\tfrac12$
— 무한 온도는 에너지 편향을 지운다. $\beta\to\infty$($T\to0$): $\varepsilon_0>\mu\Rightarrow\theta\to0$,
$\varepsilon_0<\mu\Rightarrow\theta\to1$ — 바닥상태로 계단화. 이 계단화가 뒤에서 $w=RT/F\to0$(폭이
0으로 좁아짐)으로 다시 나온다.
\end{signbox}

% ====================================================================
\subsection*{P0.4 $N$ 개의 독립 자리 — 격자기체}\label{sec:sm-lattice}
% ====================================================================
실제 전극에는 자리가 $N$ 개(몰 단위) 있다. 자리끼리 \emph{상호작용이 없다고 가정}하면(다음 절에서 뗀다),
같은 저장조($\mu,T$ 공유)에 접촉한 독립 부분계들의 결합 확률은 각 부분계 확률의 곱이므로 분배함수도 곱이다:
\begin{equation}
\Xi_N=\prod_{k=1}^N\Xi_{1,k}=(\Xi_1)^N
\label{eq:sm-latticeM}
\end{equation}
(모든 자리가 동등해 $\Xi_{1,k}=\Xi_1$). 곱 구조이므로 자리당 평균 점유는 여전히 식~\eqref{eq:sm-theta1}
의 $\theta$ 그대로다 — $N$ 개를 모아도 자리 하나짜리 통계가 반복될 뿐이다. 이것이 \emph{이상(비상호작용)
격자기체(lattice gas)}다. 그러나 실제 격자에서는 한 자리의 점유가 이웃 자리의 삽입 에너지를 바꾼다(정전
반발$\cdot$탄성 변형$\cdot$전자 구조 변화) — 그러면 $\Xi_N\ne(\Xi_1)^N$ 이 되어 곱 구조가 깨진다. 다음
절이 이 상호작용을 평균장(mean-field)으로 다시 살린다.

% ====================================================================
\subsection*{P0.5 Mean-field 상호작용 — 정규용액 자유에너지와 임계 $\Omega$}\label{sec:sm-meanfield}
% ====================================================================
\textbf{(a) 출발 — 배치의 경우의 수는 상호작용과 무관하다.} $N$ 개 자리 중 $n=N\theta$ 개가 점유된
\emph{거시상태}를 만드는 자리 \emph{배치}의 경우의 수는 어느 자리가 찼는지만 세므로 상호작용 유무와
무관하게 $W(n,N)=N!/[n!(N-n)!]$ 다. Stirling 근사 $\ln m!\simeq m\ln m-m$ 으로
\begin{align}
\ln W&=\ln N!-\ln n!-\ln(N-n)!\notag\\
&\simeq N\ln N-N-\big[n\ln n-n\big]-\big[(N-n)\ln(N-n)-(N-n)\big]\notag\\
&=-N\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big]
\label{eq:sm-Wcomb}
\end{align}
($n=N\theta,\ N-n=N(1-\theta)$ 대입 후 $N\ln N$ 항들이 상쇄 — 부록 없이 한 줄로 닫히는 표준 전개).
자리 1몰당 배치 엔트로피(configurational entropy)는 $S_\mathrm{config}=k_B\ln W/N\big|_{N=N_A}$, 곧
\begin{equation}
S_\mathrm{config}(\theta)=-R\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big]\qquad(R=N_Ak_B).
\label{eq:sm-Sconfig}
\end{equation}

\textbf{(b) 연산 — 평균장 상호작용 에너지.} 점유-점유 이웃 쌍마다 에너지 $J$(배위수 $z$)를 매기고,
점유가 \emph{무작위로 섞여 있다}고 근사(mean-field, random-mixing 근사 — 실제 상관관계를 지우는
근사다)하면, 한 점유 자리의 $z$ 개 이웃 중 평균 $z\theta$ 개가 점유돼 있어 점유-점유 쌍의 총 수는
$\approx\tfrac12(n\cdot z\theta)=\tfrac{z}{2}N\theta^2$(반쪽 인자는 쌍의 이중 계산 방지). 자리 에너지
$\varepsilon_0$(몰 환산 $h_0\equiv N_A\varepsilon_0$)를 더한 자리 1몰당 평균 에너지는
\begin{equation}
e(\theta)=h_0\theta+c\,\theta^2,\qquad c\equiv\frac{N_AzJ}{2}.
\label{eq:sm-Eint}
\end{equation}

\textbf{(c) 중간식 — 최대항(안장점) 논증.} 대정준 분배함수는 이제
$\Xi_N=\sum_{n=0}^NW(n,N)\exp[-\beta(E(n)-\mu n)]$ 인데, 지수에 \eqref{eq:sm-Wcomb}$\cdot$\eqref{eq:sm-Eint}
를 넣으면 각 항이 $\exp[N\varphi(\theta)]$ 꼴로 쓰인다($\varphi$ 는 $\theta$ 만의 세기 함수). $N\to\infty$
(열역학적 극한)에서 이 합은 \emph{최대항이 전체를 지배}한다(합의 항 수는 $N{+}1$ 개뿐인데 각 항의 크기는
지수적으로 $N$ 에 비례하므로) — 곧 평형은 $\varphi(\theta)$ 를 최대화하는(그람-그랑 퍼텐셜 밀도
$\psi(\theta;\mu)\equiv e(\theta)-Ts_\mathrm{config}(\theta)-\mu\theta$ 를 \emph{최소화}하는) $\theta$ 에서
실현된다:
\begin{equation}
\frac{\partial\psi}{\partial\theta}=0
\;\Longrightarrow\;
\mu=\frac{\partial}{\partial\theta}\big[e(\theta)-Ts_\mathrm{config}(\theta)\big]\equiv\frac{\partial\bar g}{\partial\theta}.
\label{eq:sm-saddle}
\end{equation}
이 단계는 \emph{근사가 아니라} $N\to\infty$ 에서 정확하다 — 근사는 (b)의 평균장 가정 하나뿐이다(이 구분을
분명히 해 둔다: mean-field 는 물리적 근사, 최대항 논증은 그 근사 위에서의 엄밀한 극한).

\textbf{(d) 박스 — $\mu(\theta)$.} 식~\eqref{eq:sm-Eint}$\cdot$\eqref{eq:sm-Sconfig} 를
$\bar g(\theta)=e(\theta)-Ts_\mathrm{config}(\theta)=(h_0+c)\theta+RT[\theta\ln\theta+(1-\theta)\ln(1-\theta)]-c\theta^2+c\theta$
… 를 항등식 $c\theta^2=c\theta+\Omega\,\theta(1-\theta)$($\Omega\equiv-c=-N_AzJ/2$, 대수 검산:
우변$=c\theta-c\theta(1-\theta)=c\theta-c\theta+c\theta^2=c\theta^2$ ✓)로 다시 쓰면 선형몫 $c\theta$ 가
$h_0\theta$ 에 합쳐져 $\mu^0\equiv h_0+c$ 로 흡수되고
\begin{equation}
\bar g(\theta)=\mu^0\theta+RT\big[\theta\ln\theta+(1-\theta)\ln(1-\theta)\big]+\Omega\,\theta(1-\theta),
\label{eq:sm-gbar}
\end{equation}
이를 \eqref{eq:sm-saddle} 대로 $\theta$ 미분하면
\begin{equation}
\boxed{\;\mu(\theta)=\mu^0+RT\ln\frac{\theta}{1-\theta}+\Omega\,(1-2\theta)\;}
\label{eq:sm-mutheta}
\end{equation}
\textbf{물리적 의미 — $\Omega$ 의 부호.} $\Omega=-c=-N_AzJ/2$ 이므로 $J<0$(점유-점유가 서로 에너지를
낮추는 인력)이면 $\Omega>0$ — 동종 이웃 인력이 $\Omega>0$ 이라는 관례와 정확히 일치한다(부호 재확인,
독립 재유도로 얻은 결과).

\textbf{극한 검산 — $\Omega\to0$.} $J=0\Rightarrow c=0\Rightarrow\mu^0=h_0$ 이고
\eqref{eq:sm-mutheta}$\Rightarrow\theta=1/(1+e^{-(\mu-\mu^0)/RT})$. 몰 단위 환산
$\beta(\varepsilon_0-\mu_\mathrm{particle})=(h_0-\mu)/RT=(\mu^0-\mu)/RT$(입자당 $\to$ 몰당,
$k_BT\to RT$, 비 불변)를 \eqref{eq:sm-theta1} 에 넣으면 \emph{같은 식}이 나온다 — \S\ref{sec:sm-lattice}
(독립 자리, $\Omega=0$)와 \S\ref{sec:sm-meanfield}(평균장, $\Omega\to0$)가 정확히 합류한다. 이 합류는
우연이 아니라 $\Omega=0$ 이면 애초에 (b)의 상호작용 자체가 사라져 두 유도가 \emph{같은 문제}가 되기
때문이며, 독립적으로 밟은 두 경로가 같은 식으로 닫히는 것이 그 자체로 자체검수다.

\textbf{진행률 좌표 — 정규용액 $g(\xi)$.} $\theta\leftrightarrow1-\xi=\xi$ 치환 아래
$\theta\ln\theta+(1-\theta)\ln(1-\theta)$ 와 $\theta(1-\theta)$ 는 둘 다 $\theta\leftrightarrow1-\theta$
자리바꿈에 대칭인 우함수라 함수형이 그대로 유지되고, 남는 선형항 $\mu^0\theta=\mu^0(1-\xi)=\mu^0-\mu^0\xi$
는 상수$+$선형이라 이후 절이 쓰는 두 연산(볼록성 $g''$, 공통접선/1계 미분)에 무관하므로 기준
$g_j^0$ 로 흡수한다(1계 미분에 미치는 영향은 \S\ref{sec:hys}(a)의 우함수 대칭 인자가 별도로 처리 — 그
단계는 이 절의 범위 밖이라 참조로 남긴다). 곧
\begin{equation}
g_j(\xi)=g_j^0+RT\big[\xi\ln\xi+(1-\xi)\ln(1-\xi)\big]+\Omega_j\,\xi(1-\xi).
\label{eq:sm-gxi}
\end{equation}
두 번 미분하면
\begin{equation}
g_j''(\xi)=\frac{RT}{\xi(1-\xi)}-2\Omega_j,
\label{eq:sm-gpp}
\end{equation}
$\xi=\tfrac12$ 에서 $g_j''=4RT-2\Omega_j$ — 부호가 $\Omega_j=2RT$ 에서 뒤집힌다. $\Omega_j<2RT$ 는 어디서나
$g_j''>0$(볼록, 단일 우물, 안정 균질 고용체), $\Omega_j>2RT$ 는 중앙 구간에서 $g_j''<0$(오목, 이중 우물,
불안정 — 상분리$\cdot$히스테리시스의 씨앗)이 열린다. \textbf{★범위 경계.} 이 절은 여기서 멈춘다 — 두
변곡점(spinodal)의 실제 위치 $\xi_s^\pm$, 그 위의 전위 차 $\Delta U_j^\hys$, 방향별 분기 중심 $U_j^{\,d}$
는 전기화학 연결(\S\ref{sec:sm-echem})이 놓인 \emph{다음}에야 의미가 생기는 양이라 Part I \S\ref{sec:hys}
의 고유 전개로 남겨 둔다(중복 0 — 재접속 표 \S2 R4).

% ====================================================================
\subsection*{P0.6 전기화학 연결 — $\mu_\mathrm{Li}=\mu^0-sF(V-U)$ 와 $\xi_\eq$ logistic}\label{sec:sm-echem}
% ====================================================================
\textbf{(a) 출발 — 전기화학퍼텐셜의 균형.} 하전 입자가 전위 $\phi$ 인 곳에 있을 때 그 값어치는 화학적
몫 $\mu$ 에 전기적 일 $zF\phi$(1몰, $z$ = 하전수)가 더해진 전기화학퍼텐셜
$\tilde\mu\equiv\mu+zF\phi$ 다. 삽입 반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$
의 평형은 반응물$\cdot$생성물 전기화학퍼텐셜의 균형
$\tilde\mu_{\mathrm{Li}^+}+\tilde\mu_{e^-}=\tilde\mu_\mathrm{Li}$ 다.

\textbf{(b) 연산 — 전위 의존은 전자 항 하나뿐.} 전자의 하전 $z=-1$ 이라
$\tilde\mu_{e^-}=\mu_{e^-}^0-F\phi=\mu_{e^-}^0-FV$(측정 전위 $V$ 를 전자 저장조 전위로 식별). $\mathrm{Li}^+$
의 활동도$\cdot$기준 화학퍼텐셜은 주어진 $T$ 에서 상수다 — 균형식 우변 $\tilde\mu_\mathrm{Li}$ 은
자리 점유 $\mu_\mathrm{Li}(\theta_\eq)$(식~\eqref{eq:sm-mutheta}, host 는 전기적으로 중성이라
$\tilde\mu_\mathrm{Li}=\mu_\mathrm{Li}$)이므로, 균형식 전체에서 전위 의존은 $-FV$ 한 항뿐이다.

\textbf{(c) 중간식 — 나머지 상수를 중심 전위로.} 나머지 상수 덩이($\tilde\mu_{\mathrm{Li}^+}$ 의 상수부
$+\ \mu_{e^-}^0$)를 $sFU_j$ 로 정의해($s=+1$ — \S\ref{sec:notation} 의 유도 전용 고정 부호, 응용 계층의
방향 부호 $\sigma_d=\pm1$ 은 뒤에서 별도로 곱해진다) 묶으면
\begin{equation}
\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U_j),\qquad \Delta G_j\equiv-sFU_j.
\label{eq:sm-echem-mu}
\end{equation}
\textbf{(d) 박스 — 이상(理想) 극한의 $\xi_\eq$.} 상호작용이 없는 경우($\Omega_j=0$, \S\ref{sec:sm-lattice}
의 독립 자리)엔 식~\eqref{eq:sm-mutheta} 가 $\mu(\theta)=\mu^0+RT\ln[\theta/(1-\theta)]$ 로 줄고, 이를
\eqref{eq:sm-echem-mu} 와 등치하면
\[
RT\ln\frac{\theta_\eq}{1-\theta_\eq}=-sF(V-U_j)
\;\Longrightarrow\;
\theta_\eq=\frac{1}{1+e^{sF(V-U_j)/RT}}.
\]
진행률 $\xi_\eq=1-\theta_\eq$(\S\ref{sec:notation} 의 묶음)로 옮기고 폭 $w\equiv RT/F$ 로 적으면
\begin{equation}
\boxed{\;\xi_\eq(V,T)=\frac{1}{1+\exp[-s(V-U_j)/w]},\qquad w=\frac{RT}{F}\;}
\label{eq:sm-xieq-ideal}
\end{equation}
— 이것이 다음 장들이 쓰는 logistic 평형 종의 통계역학적 기원이다(다중도 $n_j$·방향 부호 $\sigma_d$·분기
중심 $U_j^{\,d}$ 로의 일반화는 \S\ref{sec:width}(d) 가 응용 계층에서 담당하며, 이 식과 형태가 1:1 이다).
$\Omega_j\ne0$ 인 일반 경우는 \eqref{eq:sm-mutheta} 전체를 \eqref{eq:sm-echem-mu} 에 넣어야 하고, 그때
$V(\xi)$ 는 더 이상 순수 logistic 의 역함수가 아니라 \S\ref{sec:hys} 가 여는 비단조 곡선(식~\eqref{eq:Veq})이
된다 — 이 절은 그 문턱(\S\ref{sec:sm-meanfield} 의 $\Omega_j=2RT$)까지만 놓고 넘긴다.

\begin{keybox}
\textbf{두 독립 경로의 수렴(detailed balance 교차검증).} 이 절은 \emph{평형 통계역학}(자유에너지 최소화)
경로로 $\xi_\eq$ 에 닿았다. Part I \S\ref{sec:width} 는 \emph{운동학}(Eyring 속도식 + 정$\cdot$역 flux
의 detailed balance)으로 \emph{독립적으로} 같은 식~\eqref{eq:sm-xieq-ideal}(그곳의 식~\eqref{eq:xieq})에 닿는다.
이 두 경로의 수렴은 우연이 아니다 — detailed balance 를 만족하는 어떤 미시적 동역학이든 그 정지 분포는
반드시 이 절의 grand-canonical Boltzmann 분포와 같다(이것이 detailed balance 의 정의 자체가 강제하는
결과다). 곧 "자유에너지가 최소인 곳"과 "정$\cdot$역 속도가 균형 잡힌 곳"은 같은 곳을 가리키는 두
언어이며, 두 장이 서로 다른 산문으로 같은 식에 도달한다는 사실 자체가 이 문건 전체의 내적 일관성
검산이다.
\end{keybox}

% ====================================================================
\subsection*{P0.7 거시 열역학 연결 — $G\equiv H-TS$, Nernst, $\Delta G_j=-sFU_j$}\label{sec:sm-macro}
% ====================================================================
\textbf{(a) 출발 — Gibbs 자유에너지의 정의.} \S\ref{sec:sm-mu}(a)의 $\mu\equiv\partial G/\partial n$ 이
쓰는 $G$ 자체는
\begin{equation}
G\equiv H-TS
\label{eq:sm-gibbsdef}
\end{equation}
로 정의된다($H$ 항과 $-TS$ 항이 경쟁하고 온도가 그 환율을 정한다) — 이것이 통계역학(미시, $\Xi\to\mu(\theta)$)
과 고전 열역학(거시, $\Delta H,\Delta S$ 표)을 잇는 마지막 다리다. \textbf{(b) 연산 — 반응 자유에너지 대입.}
전이 $j$ 의 비배치 몫 반응 자유에너지는 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$(식~\eqref{eq:sm-gibbsdef}
를 반응물$-$생성물 차에 적용) — 이를 \eqref{eq:sm-echem-mu} 의 정의 $\Delta G_j=-sFU_j$($s=+1$)에 대입하면
\[
\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}=-F\,U_j.
\]
\textbf{(c) 중간식 — $U_j$ 로 이항.}
\begin{equation}
U_j(T)=\frac{-\Delta H_{\rxn,j}+T\,\Delta S_{\rxn,j}}{F}.
\label{eq:sm-Uj}
\end{equation}
\textbf{(d) 박스 — Nernst 형과 닫힌 사슬.} 식~\eqref{eq:sm-echem-mu} 를 $V$ 에 대해 풀면(이상 극한,
$\Omega_j=0$) $V(\xi)=U_j+(RT/sF)\ln[\xi/(1-\xi)]$ — 표준 Nernst 식의 로그항이 \S\ref{sec:sm-meanfield}
식~\eqref{eq:sm-Sconfig} 의 배치 엔트로피에서 온 것임을 이 절이 보였다. 사슬 전체를 한 줄로:
\begin{equation}
\boxed{\;
\Xi\ \to\ \theta=\langle N\rangle\ \to\ \mu(\theta)\ \to\
\mu_\mathrm{Li}=\mu^0-sF(V-U_j)\ \to\ U_j(T)=\frac{-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j}}{F}
\;}
\label{eq:sm-chain}
\end{equation}
— 대정준 분배함수에서 출발해 미시(점유 확률)를 거쳐, \S\ref{sec:center}$\cdot$\S\ref{sec:hys}$\cdot$
\S\ref{sec:width} 가 쓰는 모든 거시 관측량($U_j,\ \Delta U_j^\hys,\ \xi_{\eq,j}$)의 \emph{기원}에
닿았다. 식~\eqref{eq:sm-Uj} 는 Part I 식~\eqref{eq:Uj} 와 부호까지 1:1 이다 — 다음 절부터는 이 사슬을 전이별
$(\Delta H_{\rxn,j},\Delta S_{\rxn,j})$ 로 구체화하고($\mathrm N2$), 상호작용 $\Omega_j$ 로 히스테리시스를
열고($\mathrm N3$), 폭 다중도 $n_j$ 와 방향 부호 $\sigma_d$ 로 이 logistic 을 응용 계층에 앉힌다
($\mathrm N4/N5$) — 그 구체화가 \S\ref{sec:notation} 부터 시작되는 나머지 Chapter 1 이다.
```

---

## 2. 재접속 표 (기존 절 → Part 0 편입 후 처리)

| 원천(범위) | 다루는 물리 | Part 0 대응 | 편입 후 처리 권고 |
|---|---|---|---|
| R1. Ch1 sec:center (a) `eq:gibbsdef`·`eq:mudef` (L417–427) | $G\equiv H-TS$·$\mu\equiv\partial G/\partial n$ 정의 | §sec:sm-mu(a)·§sec:sm-macro(a) | 정의 재사용(중복 아님, 재확인) — sec:center 는 정의 재인용만 하고 (b)로 직행 |
| R2. Ch1 sec:center (b)(c)(d) 전기화학평형·`eq:eqbalance`·`eq:eqcond` (L428–446) | $\tilde\mu$ 균형 → $\mu_\mathrm{Li}=\mu^0-sF(V-U)$·$\Delta G_j=-sFU_j$ | §sec:sm-echem 전체(eq:sm-echem-mu) | **완전 흡수** — sec:center 는 이 유도를 삭제하고 "\S\ref{sec:sm-echem} 참조"로 대체, 곧바로 "$U_j(T)$ 온도 환산"으로 진입 |
| R3. Ch1 sec:center "U_j(T) 온도 환산" `eq:Ujmid`·`eq:Uj` (L448–467) | $\Delta G=\Delta H-T\Delta S$ 대입 → $U_j(T)$ 일반형 | §sec:sm-macro(b)(c)(d)(eq:sm-Uj) | 일반형은 흡수, sec:center 는 전이별 수치 대입(N2 코드 대응, `func_U_j` 예시 계산)만 남김 — **물리 손실 0**(수치 예시는 Part 0 범위 밖) |
| R4. Ch1 sec:hys (a) 격자기체 $\mu(\theta)$ `eq:mu` (L586–597) | mean-field 상호작용 몫 → $\mu(\theta)$ | §sec:sm-meanfield(d)(eq:sm-mutheta) | **완전 흡수**(독립 재유도로 재확인) — sec:hys 는 결과 인용만 하고 (b)로 직행 |
| R5. Ch1 sec:hys (b) $g(\xi)$ 변환 `eq:gxi` (L598–604) | $\theta\to\xi$ 좌표 변환, 대칭성 | §sec:sm-meanfield 말미(eq:sm-gxi) | **완전 흡수** |
| R6. Ch1 sec:hys (c)(d) $g''$·spinodal·$\Delta U_j^\hys$·$U_j^{\,d}$ (L605–722) | 볼록성 반전·spinodal 값·gap 닫힌꼴·분기중심 | §sec:sm-meanfield 는 `eq:sm-gpp` 로 임계 $\Omega=2RT$ \emph{문턱만} 제시, 그 이상은 명시적 범위 밖 | **비흡수(의도적)** — spinodal 좌표·$\Delta U_j^\hys$ 닫힌식·$U_j^{\,d}$ 분기 공식은 전기화학 연결(Part 0 §sec:sm-echem) \emph{이후}에야 의미가 생기는 Part I 고유 전개이므로 sec:hys 에 그대로 유지, Part 0 는 forward 참조만 |
| R7. Ch1 sec:width "폭 $w_j$" `eq:wbase` (L924–951) | 이상 극한 폭 $w=n_jRT/F$ | §sec:sm-echem(d)(eq:sm-xieq-ideal 의 $w=RT/F$) | 이상극한 $n_j{=}1$ 도출은 흡수, sec:width 는 폭의 **이중지위**(단상/두-상 구분·broadening 지위 분기) 고유 서술만 남기고 도출은 참조 |
| R8. Ch1 sec:width "Eyring/detailed balance" `eq:bv`·`eq:db`·`eq:logisticsolve`·`eq:xieq` (L954–993) | 운동학적(kinetic) $\xi_\eq$ 재유도 | §sec:sm-echem keybox 가 forward 예고 | **비흡수(의도적, 독립 경로 보존)** — 물리적으로 다른 경로(속도론)이므로 중복이 아니라 교차검증 자산. sec:width 서두에 "\S\ref{sec:sm-echem} 의 평형 통계역학 경로와 독립적으로, 여기서는 운동학으로 같은 식에 다시 닿는다" 다리 문장 추가 권고(편입 시 1문장) |
| R9. Ch1 sec:dist 전체 (L1066–1139) | "$\xi_\eq$ = 격자기체 점유 분포" — 단일자리 grand canonical 재유도 + kinetic·thermo 두 경로 통합 서술 | §sec:sm-site·§sec:sm-echem keybox | **거의 완전 흡수** — Part 0 가 이 내용을 \emph{먼저} 확립하므로 sec:dist 의 (a)–(d) 유도(L1073–1105)는 삭제 후보, "이미 Part 0 \S\ref{sec:sm-site}–\S\ref{sec:sm-echem} 에서 확립됨" 1문장 요약 + LCO 전자엔트로피 다리 keybox(L1107–1112, "분포 다리")만 잔존 |
| R10. Ch2 sec:partition 전체 `eq:Z1`·`eq:occ`·`eq:muV`·`eq:logistic`·keybox (L110–178) | 단일 자리 대정준 분배함수 → logistic, 폭의 평형예측/현상학 지위 keybox | §sec:sm-site(eq:sm-Z1·sm-theta1)·§sec:sm-echem(eq:sm-xieq-ideal) | **거의 완전 흡수** — Ch2 는 "\S\ref{part:sm} 에서 이미 유도"라는 요약 문단(2–3문장)으로 대체하고, keybox 의 "단상/두-상 두 지위 구분" 논지(Chapter 2 고유 확장 — Chapter 1 broadening 절과의 연결)는 **잔존**(Part 0 범위 밖 — Part 0 는 지위 구분을 다루지 않음) |
| R11. Ch2 ssec:BW `eq:BW`·`eq:Veq_BW`·`eq:slope_BW` (L190–218) | Bragg–Williams $g(\theta)$·$V_\eq(\theta)$·임계 $\Omega=2RT$ | §sec:sm-meanfield(전체)·§sec:sm-meanfield 말미(eq:sm-gpp) | **완전 흡수**(같은 결과, Part 0 가 조합론+평균장 1차 원리에서 재유도해 더 이른 지점에서 제공) — Ch2 는 참조로 대체 |
| R12. Ch2 sec:config `eq:Sconfig`·`eq:dSconfig`·`eq:dVdT_config` (L221–260+) | 배치 엔트로피·부분몰 미분·발산 봉우리 | §sec:sm-meanfield(a)(eq:sm-Sconfig) 는 $S_\mathrm{config}$ 자체만 흡수 | **부분 흡수** — $S_\mathrm{config}(\theta)$ 정의는 Part 0 가 먼저 제공(참조 대체), \emph{부분몰} 미분(`eq:dSconfig`)과 그로부터의 "봉우리 내부 발산" 결론은 Chapter 2 고유 확장(가역 발열 서사)이라 **잔존**, 도입부만 "\S\ref{sec:sm-meanfield} 의 $S_\mathrm{config}$ 를 부분몰량으로 미분하면"으로 다리 교체 |

**미편입 확인**: R6·R8·R12(부분)는 의도적 비흡수 — 물리 손실이 아니라 Part 0 의 "기초"라는 scope 경계(전기화학 응용·운동학적 교차검증·Chapter 2 고유 서사)를 지키기 위한 경계선이다. 이 경계는 마스터 플랜 Non-goals("Ch2 대개편 X — Part 0 참조화·용어 정책·참조 갱신만")와 정합한다.

---

## 3. 갈래 2 — Part II "LCO 양극" 도입 절 (LaTeX 문안)

> 원천 3편(sec:lco-map L301–355 전문·sec:lco-hys ★분기 부호 문단 L846–854·sec:lco-peak ★방향 부호 문단 L1416–1437) 을 하나로 일원화. f=+σ_d 는 `V1012_P43_verify10.md` §2 확정 판정(재유도·재론 금지) — 아래는 그 판정을 **인용**만 하고, "무엇이 전극-중립인가"와 "방향 인자를 어떻게 먹이는가"를 한 곳에서 닫는 신설 절이다. 신설 라벨 프리픽스 `sec:p2-*`.

```latex
% ====================================================================
\section{Part II 도입 — 두 번째 전극, 전극-중립 골격과 방향 규약}\label{sec:p2-intro}
% ====================================================================
Part I 은 흑연 음극 하나로 \S\ref{sec:notation}–\S\ref{sec:sum} 의 전 골격(기호$\cdot$평형 중심$\cdot$
히스테리시스$\cdot$폭$\cdot$peak$\cdot$동역학 꼬리)을 세웠다. Part II 는 같은 골격을 \emph{두 번째
사례}인 $\mathrm{LiCoO_2}$(LCO) 양극에 건다 — 흑연 서술은 한 줄도 바뀌지 않으며, LCO 는 파라미터를
갈아 끼우고 고유 항(전자 엔트로피) 하나를 더하는 두 번째 전극으로 들어온다. 이 절은 그 전에 반드시
합의해야 할 것 둘 — \emph{무엇이 전극과 무관한가}, \emph{방향 인자를 어떻게 먹이는가} — 을 한 곳에서
닫는다(이하 \S\ref{sec:lco-map}$\cdot$\S\ref{sec:lco-hys}$\cdot$\S\ref{sec:lco-peak} 에 산재했던 서술의
일원화). 범위는 \emph{코인 하프셀}(LCO vs Li metal) 단독이다 — 전셀 합성은 범위 밖(후속).

\subsection{전극-중립 골격 — 무엇이 전극을 가리지 않는가}\label{sec:p2-neutral}
\textbf{(a) 실험조건·색인 계층.} \S\ref{sec:notation} 의 방향 부호$\cdot$전류 환산(식~\eqref{eq:n0map}),
전이 인덱스 $j$, 진행률 $\xi_j$, 점유 $\theta_j=1-\xi_j$ 는 정의 자체에 "흑연"이 들어가지 않는다 — 삽입형
전극이면 종류를 가리지 않는 색인 계층이다. \textbf{(b) 열역학 계층.} \S\ref{sec:sm-echem}$\cdot$
\S\ref{sec:sm-macro} 가 세운 전기화학 평형 조건 $\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U)$,
$\Delta G_j=-sFU_j$, $U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$ 도 삽입 반쪽반응
$\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 에서 나오며 host 가 흑연인지 LCO
인지에 무관하다 — host 의 화학 정체는 상수 $\mu^0$ 와 반응 몫 입력값($\Delta H_{\rxn,j},\Delta S_{\rxn,j}$)
으로만 흡수된다. \textbf{(c) mean-field 계층.} \S\ref{sec:sm-meanfield} 의 $\mu(\theta)$·$g(\xi)$·spinodal
문턱 $\Omega_j=2RT$ 도 "동등한 자리에 리튬이 차고 빈다"는 가정 하나만 쓰므로 LCO 의 팔면체 리튬 자리에
문자 그대로 성립한다. 곧 LCO 로 넘어갈 때 이 세 계층에 들어가는 것은 전이 집합과 입력값의 \emph{치환}뿐이다:
\begin{equation}
j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1,T2,T3}\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j},\Omega_j)\ \longmapsto\
(\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat},\Omega_j^\mathrm{cat}).
\label{eq:p2-neutral}
\end{equation}
\textbf{LCO 하프셀 부호.} LCO 전위는 vs Li/Li$^+$ 로 $\sim$3.9–4.2 V(흑연의 $\sim$0.1 V 와 달리 높은
영역)이지만 부호 골격은 같다: 방전($\sigma_d{=}{+}1$)은 LCO 입장에서 \emph{리튬화}
(Co$^{4+}\!\to$Co$^{3+}$, $x$ 증가, 전위 하강)이고, 충전($\sigma_d{=}{-}1$)은 \emph{탈리튬화}($x$ 감소,
전위 상승)이다 — \textbf{흑연과 정반대다}: 흑연 방전 $=$ 탈리튬화, LCO 방전 $=$ 리튬화. 이 비대칭이 다음
소절의 방향 규약을 강제한다. 하프셀($\le$4.2–4.5 V)은 세 전이를 남긴다\cite{xia2007}: $\sim$3.90 V MIT(T1),
$\sim$4.05 V·$\sim$4.17 V 의 order--disorder 한 쌍(T2·T3) — 값은 초기값(tier, 피팅 override 전제)이며
표$\cdot$세부는 \S\ref{sec:lco-map} 를 승계한다(무변경).

\subsection{방향 인자 $\sigma_d$ — 무엇을 먹이는가}\label{sec:p2-direction}
\textbf{물리 내용.} \S\ref{sec:sm-meanfield} 의 이중웰 기하(그림~\ref{fig:doublewell})는 \emph{전극과
무관}하다 — 과주행 그림(그림~\ref{fig:hysloop})에서 \emph{탈리튬화} 가지는 상승(극대 $\xi_s^-$ 까지),
\emph{리튬화} 가지는 하강(극소 $\xi_s^+$ 까지)이라는 사실은 이중웰의 기하 그 자체이지 어느 셀 동작이
탈리튬화인지와 무관하다. 곧 $\sigma_d$ 가 실제로 실어 나르는 물리 내용은 셀 라벨이 아니라
\begin{equation}
\boxed{\;\sigma_d=+1\ \Longleftrightarrow\ \text{탈리튬화(산화) 진행}\;}
\label{eq:p2-direction}
\end{equation}
이며, 이 부호는 방향 의존적인 \emph{세 작용처} — 분극(\S\ref{sec:pol}, $V_\app>V_n$ 는 산화 방향)$\cdot$
분기(\S\ref{sec:hys}, 탈리튬화 가지가 $U_j$ 위)$\cdot$꼬리(\S\ref{sec:tail}, 인과 시간 순서 $=$ 산화
진행 방향) — 전부에서 같은 내용으로 들어간다. \textbf{흑연.} 방전 라벨이 탈리튬화와 일치해 라벨 $=$
물리가 겹치므로 $\sigma_d{=}{+}1$(방전)이 그대로 식~\eqref{eq:p2-direction} 의 $+1$ 이다. \textbf{LCO.}
\S\ref{sec:p2-neutral} 의 부호대로 \emph{충전}이 탈리튬화이므로, LCO 데이터에 모델을 걸 때 방향 인자는
셀 방향 라벨이 아니라 \emph{탈리튬화 여부}로 준다:
\begin{equation}
\text{LCO 충전 곡선}\ \longmapsto\ \sigma_d=+1\ (\text{탈리튬화 슬롯}),\qquad
\text{LCO 방전(리튬화)}\ \longmapsto\ \sigma_d=-1.
\label{eq:p2-lcoslot}
\end{equation}
이렇게 읽어야 분극$\cdot$분기$\cdot$꼬리 세 부호가 흑연과 1:1 로 유지된다 — 그림~\ref{fig:p2-directionmap}
가 이 대응을 한눈에 닫는다.\footnote{\S\ref{sec:p2-neutral} 의 ``방전($\sigma_d{=}{+}1$)은 LCO 엔 리튬화''
서술은 셀 방향 \emph{라벨}의 의미론(어느 셀 동작이 어느 화학 방향인가)이고, 이 소절의 규칙은 모델
\emph{입력 슬롯}에 그 라벨이 아니라 탈리튬화 여부를 먹인다는 적용 규칙이다 — 두 서술은 층위가 달라
모순이 아니다.}

\textbf{평형 종은 방향에 불변.} 평형 점유 $\xi_\eq(V,T)$ 자체(식~\eqref{eq:sm-xieq-ideal}·일반형은
\S\ref{sec:width})는 $\xi\leftrightarrow1-\xi$ 자리바꿈에 대칭이라 두 읽기 중 어느 쪽으로도 같은 봉우리를
준다 — 방향 읽기가 갈라놓는 것은 위 세 작용처뿐이고, 이 잠복성(봉우리는 맞아 보이지만 방향 의존 물리는
틀어질 수 있음)이 셀 라벨 오적용을 특히 위험하게 만든다(FITTING\_GUIDE \S0 진단표 대응).

\begin{keybox}
\textbf{확정 판정 인용(재론 금지).} MSMR(multi-species, multi-reaction) 모델과의 대응에서 이 방향 인자가
$f=+\sigma_d$ 로 닫힌다는 것은 \texttt{V1012\_P43\_verify10.md} \S2 가 원계열 부호 규약(외부 실측)과
제1원리 pairing 재유도(같은 물리량끼리 — 점유$\leftrightarrow$점유$\cdot$진행률$\leftrightarrow$진행률)
로 \textbf{확정}한 판정이다 — 본 절은 이를 그대로 승계하며 재론하지 않는다. 상세 pairing 대응표
(식~\eqref{eq:lco-msmrmap})는 \S\ref{sec:lco-decomp} 에서 MSMR 모델을 실제로 도입할 때 예고된다.
\end{keybox}
```

**갈래 2 배치 권고**: `sec:lco-map`(L301) 자리에 이 신설 절을 대체 삽입하고, 기존 `sec:lco-map` 본문은 \S\ref{sec:p2-neutral}(a)(b)(c)로 압축 편입(표 `tab:lco-staging` 자체는 무변경 이동). `sec:lco-hys` ★분기 부호 문단(L846–854)과 `sec:lco-peak` ★방향 부호 문단(L1416–1437, 각주 포함)은 본 신설 절 §sec:p2-direction 이 포괄하므로 원 위치에서는 "\S\ref{sec:p2-direction} 의 방향 규약을 이 국소 맥락(분기 중심 / peak 유도)에 적용하면"으로 1문장 압축 — **삭제가 아니라 압축 다리**(교훈 카드 ④, 재수록 금지).

---

## 4. Figure 목록 (제작 + 체리픽용)

| # | 목적 | 형식 | 배치 | 스크립트/코드 경로 | 실행 확인 |
|---|---|---|---|---|---|
| SM-1 | 단일자리 grand-canonical 점유 $\xi_\eq(V)$ — $\Omega{=}0$, 다중 $T$ 로 폭 $w{=}RT/F$ 가 $T$ 에 넓어짐을 실제 식 평가로 시각화 | matplotlib PNG | §sec:sm-echem(d), eq:sm-xieq-ideal 박스 직후 | `V1013_P21_fig_S1_theta_V_multiT.py` → `V1013_P21_fig_S1_theta_V_multiT.png` | 실행 완료. 수치 자체검수 stdout: $T{=}298.15$ K 에서 $w{=}25.693$ mV(문서 기존 signbox 값 25.7 mV 와 일치, L1063) · 모든 $T$ 에서 $\xi_\eq(V{=}U){=}0.5$·$\xi_\eq(V{=}U{+}2w){=}0.880797$(무차원 형태 불변, 자기유사성 검증) |
| SM-2 | 정규용액 $g(\xi)$ 이중웰의 $\Omega$ 의존 — $\Omega/RT\in\{0,1,2,3,4\}$, 임계값 $2$ 표시, spinodal 점을 실제 좌표로 마킹 | matplotlib PNG | §sec:sm-meanfield 말미, eq:sm-gxi/eq:sm-gpp 직후 | `V1013_P21_fig_S1_gxi_doublewell.py` → `V1013_P21_fig_S1_gxi_doublewell.png` | 실행 완료. 수치 자체검수 stdout: $g''(1/2)/RT=4-2(\Omega/RT)$ — $\Omega/RT{=}2$ 에서 정확히 $0.000$, $<2$ 는 양(+2.0/+4.0), $>2$ 는 음($-2.0/-4.0$) — eq:sm-gpp 와 1:1 일치 |
| SM-3 | mean-field $\mu(\theta)$ 의 van der Waals 형 loop — 같은 $\Omega/RT$ 계열, $\theta{=}1/2$ 대칭점 실측 | matplotlib PNG | §sec:sm-meanfield, eq:sm-mutheta 박스 직후(SM-2 와 나란히) | `V1013_P21_fig_S1_mu_theta_vdw.py` → `V1013_P21_fig_S1_mu_theta_vdw.png` | 실행 완료. 수치 자체검수 stdout: 전 $\Omega/RT$ 값에서 $\mu(1/2)-\mu^0=+0.000000\,RT$(정확히 0, eq:sm-mutheta 의 $(1-2\theta)$ 인자가 $\theta{=}1/2$ 에서 소멸하는 대수와 일치) |
| P2-1 | 충$\cdot$방전 셀 라벨 ↔ 탈리튬화 방향 대응도(흑연 vs LCO 2단 비교, $\sigma_d$ 슬롯 규칙 시각화) | TikZ(문서 tikzpicture 관례 — `positioning`·`arrows.meta` 라이브러리, 기존 ch1 프리앰블과 동일) | §sec:p2-direction 말미, eq:p2-lcoslot 직후 | `V1013_P21_fig_S1_direction_map.tex`(인라인 코드, §3 갈래 2 문안에 `\label{fig:p2-directionmap}` 로 이미 삽입) | TikZ 컴파일은 미실시(개별 컴파일 환경 부재 — xelatex+kotex 조합은 master 편입 빌드에서 전체 문서와 함께 검증 권고). 좌표$\cdot$논리는 표~eq:p2-lcoslot·§sec:p2-direction 본문과 1:1 대조 완료(손그림 개형 아님 — 논리적 대응관계의 다이어그램이라 "실제 식 평가"가 아닌 "본문 대응표와의 1:1 대조"로 검산, 정성적 개념도이므로 수치 날조 대상 자체가 없음) |

모든 matplotlib 스크립트는 `D:\Projects\Project_Anode_Fit\Claude\results\process\` 에 위치하며, 실행 커맨드는 각 스크립트 상단 docstring 그대로(`python <script>.py`, 같은 디렉터리에서 실행하면 PNG 가 같은 디렉터리에 생성). 라벨$\cdot$범례 전부 ASCII/영어(glyph 0), 좌표는 실제 물리상수($R=8.314462618$ J/(mol K), $F=96485.33212$ C/mol)로 평가했다 — 손그림 좌표 없음.

---

## 5. 물리 자체검수 기록

| # | 항목 | 방법 | 결과 |
|---|---|---|---|
| V1 | 차원 | $\mu,\mu^0,RT,\Omega,sFV$ 전부 J/mol 로 통일 확인(eq:sm-mutheta·eq:sm-echem-mu 각 항) | PASS |
| V2 | 부호 — $\Omega$ 물리 의미 | $\Omega\equiv-c=-N_AzJ/2$, $J<0$(인력)$\Rightarrow\Omega>0$ — 독립 재유도 결과가 기존 "Ω>0=동종 이웃 인력" 관례(L604)와 일치 | PASS |
| V3 | 극한 $\beta\to0$ | eq:sm-theta1 에서 $\theta\to1/2$(무한온도, 에너지 편향 소멸) | PASS |
| V4 | 극한 $\beta\to\infty$ | $\varepsilon_0\gtrless\mu\Rightarrow\theta\to0/1$(바닥상태 계단화, $w\to0$ 예고와 정합) | PASS |
| V5 | 극한 $\Omega\to0$ — 교차검증 | §sec:sm-meanfield 의 mean-field 결과가 §sec:sm-lattice/§sec:sm-site 의 독립자리 결과와 대수적으로 정확히 합류(본문 "극한 검산" 문단, 몰↔입자 단위 환산 명시) | PASS(독립 두 경로 수렴) |
| V6 | 극한 $\Omega\to2RT^\pm$ — 임계 | $g''(1/2)=4RT-2\Omega$ 부호 전환점 $=2RT$, SM-2 스크립트 stdout 수치로 실측 확인($\Omega/RT{=}2$ 에서 $0.000$) | PASS |
| V7 | 대칭 — $\mu(\theta{=}1/2)=\mu^0$ | SM-3 스크립트 stdout 전 $\Omega$ 값에서 $+0.000000\,RT$ | PASS |
| V8 | detailed balance 교차검증 | §sec:sm-echem keybox — 평형(자유에너지 최소화) 경로와 Part I sec:width 의 운동학(Eyring+정$\cdot$역 flux 균형) 경로가 독립적으로 같은 eq:sm-xieq-ideal 에 도달함을 논증(우연이 아니라 detailed balance 의 정의가 강제하는 결과로 근거 제시) | PASS |
| V9 | 최종형 대조 — 기존 라벨과 1:1 | eq:sm-mutheta ↔ eq:mu(L595) · eq:sm-gxi ↔ eq:gxi(L601) · eq:sm-Z1 ↔ eq:Z1(ch2 L124) · eq:sm-theta1 ↔ eq:occ(ch2 L130)·eq:fermifn(ch1 L1084) · eq:sm-xieq-ideal ↔ eq:logistic(ch2 L152)·eq:xieq(ch1 L983, $n_j{=}1,\Omega{=}0$ 특수형) · eq:sm-Uj ↔ eq:Uj(ch1 L459) — 전 항목 부호까지 일치, 함수형만 같고 물리량이 다른 사례 0건(교훈 카드 ②) | PASS |
| V10 | "함수형 동형 ≠ 물리량 동일" 가드 | Part 0 안에서 $\theta$(점유)와 $\xi$(진행률)를 매 절 명시적으로 구분해 사용(§sec:sm-meanfield "진행률 좌표" 문단이 치환의 근거를 대칭성으로 명시) — 두 양을 직접 등치하는 실수 없음 | PASS(자기점검) |
| V11 | 보존식/경계 | Part 0 는 신설 절이라 $C_\bg$ 등 기존 보존식 접촉 없음(교훈 카드 ③ 은 이 절에 해당 사항 없음 — 재접속 표 R6 이 경계를 명시) | N/A(해당 없음, 명시) |
| V12 | 수치 날조 | Part 0·Part II 문안 어디에도 새 피팅값 없음. 사용한 모든 수치는 물리상수(R,F)이거나 이미 문서에 있는 값(25.7 mV, 4958 J/mol)의 재확인. 그림의 $\Omega/RT\in\{0,\dots,4\}$ 는 명시적으로 무차원 illustrative 값(범례에 "critical" 한정어로 $\Omega/RT{=}2$ 를 다른 값과 구분) | PASS |

---

## 6. 라벨 충돌 전수 확인

`eq:sm-*`(19개: boltzmann0·taylor0·boltzmann·canonical·taylor1·taylor2·grand·Z1·theta1·latticeM·Wcomb·Sconfig·Eint·saddle·gbar·mutheta·gxi·gpp·echem-mu·xieq-ideal·gibbsdef·Uj·chain, 실제 22개)와 `sec:sm-*`(7개: ensemble·mu·site·lattice·meanfield·echem·macro), `sec:p2-*`(3개: intro·neutral·direction), `eq:p2-*`(2개: neutral·direction·lcoslot, 실제 3개) — 기존 ch1/ch2 라벨 전수(grep 결과, `eq:sm-`·`sec:sm-`·`eq:p2-`·`sec:p2-` 패턴)와 대조해 **충돌 0건** 확인. `fig:p2-directionmap` 도 기존 `fig:*` 라벨(9종)과 충돌 0건.

---

## 7. 5줄 요약 (최약점 자기표시 포함)

1. Part 0(7개 소절, `sec:sm-*`)이 앙상블→Boltzmann 인자→grand canonical→단일자리→격자기체→평균장(정규용액)→전기화학 연결→거시 열역학까지 (a)(b)(c)(d) 형식으로 완결 재유도했고, 최종형이 기존 eq:mu·eq:gxi·eq:xieq·eq:Z1·eq:occ·eq:Uj 와 부호까지 1:1 일치함을 §5 V9 에서 대조 확인했다.
2. 재접속 표(§2, 12행)로 Ch1 sec:center/sec:hys/sec:width/sec:dist 와 Ch2 sec:partition/ssec:BW 전량의 편입 후 처리(완전 흡수/부분 흡수/의도적 비흡수)를 명시했다 — 특히 Ch2 eq:Z1 절이 거의 전량 Part 0 로 흡수돼 마스터 플랜의 "Ch2 중복 0" 목표를 충족한다.
3. Part II 도입(§3, `sec:p2-intro`)이 sec:lco-map·sec:lco-hys ★분기 부호 문단·sec:lco-peak ★방향 부호 문단 셋을 일원화했고, f=+σ_d 는 재유도하지 않고 verify10 확정 판정을 키박스로 **인용만** 해 재론 금지 지시를 지켰다.
4. Figure 4종(SM-1/2/3 matplotlib 실제 식 평가 + 실행 완료·수치 stdout 자체검수 / P2-1 TikZ 논리 대응도)을 제작했고, 스크립트·PNG 경로는 §4 표에 명시했다.
5. **최약점 자기표시**: (i) §sec:sm-meanfield(a)(b)의 "조합론적 배치수 + 평균장 쌍상호작용 에너지 + 최대항(안장점) 논증"은 원천 문서가 쓰지 않는 제 나름의 독립 유도 경로라(원천은 정규용액 자유에너지를 직접 postulate) 물리적으로는 3중 교차검증(§5 V5·V6·V9)까지 마쳤으나, master 가 더 간결한 대안 경로(원천처럼 자유에너지 ansatz 직접 제시)를 선호할 경우 이 부분이 가장 먼저 압축 대상이 될 것으로 예상한다. (ii) §sec:sm-echem(a)–(c)의 전기화학퍼텐셜 균형 논증은 물리적으로 sec:center 원문과 같은 표준 구조를 필연적으로 공유하므로(전기화학 평형의 유일한 표준 경로), "독립 재유도"의 엄밀도를 더 요구한다면 이 절이 두 번째 압축/재작업 후보다.

---

## 8. 산출물 경로 요약

- 본 드래프트: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_draft_S1.md`
- Figure 스크립트: `V1013_P21_fig_S1_theta_V_multiT.py` · `V1013_P21_fig_S1_gxi_doublewell.py` · `V1013_P21_fig_S1_mu_theta_vdw.py` · `V1013_P21_fig_S1_direction_map.tex`(전부 같은 `results\process\` 디렉터리)
- Figure PNG: `V1013_P21_fig_S1_theta_V_multiT.png` · `V1013_P21_fig_S1_gxi_doublewell.png` · `V1013_P21_fig_S1_mu_theta_vdw.png`(같은 디렉터리, 300 dpi)
