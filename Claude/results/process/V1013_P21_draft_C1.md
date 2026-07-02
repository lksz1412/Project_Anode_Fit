# V1013 P2.1 갈래 1 드래프트 — C1

- 작업 ID: C1
- 범위: 갈래 1만, Ch1 신설 Part 0 "통계역학 기초"
- 출력 성격: master 편입 전 독립 드래프트. `.tex`/코드 원본 수정 없음.
- 원천 전문 정독 범위:
  - `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` L411-L475 (`sec:center`)
  - `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` L578-L751 (`sec:hys`)
  - `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` L918-L1139 (`sec:width`, `sec:dist`)
  - `Claude/docs/v1.0.13/graphite_ica_ch2_v1.0.13.tex` L110-L180 (`sec:partition`, `eq:Z1`)

## 절별 루핑 기록

| Loop | 원천 범위 | 독립 재유도 초점 | 자체검수 초점 | 앞 절 정합 |
|---|---:|---|---|---|
| 0 | Ch1 L411-L475 | `G=H-TS`, `\mu=\partial G/\partial n`, 전기화학 평형, `\Delta G_j=-sFU_j` | 전위 부호, J/mol과 V 환산, `\partial U/\partial T=\Delta S/F` | Part 0의 거시 열역학 말단으로 배치 |
| 1 | Ch2 L110-L180, Ch1 L1066-L1099 | 단일 자리 대정준 분배함수 `Z_1`, 점유 `\theta`와 진행률 `\xi=1-\theta` | `\beta\to0,\infty`, `\theta`와 `\xi` 물리량 혼동 방지 | microscopic 출발점으로 배치 |
| 2 | Ch1 L578-L620 | `M` 독립 자리와 mixing entropy, regular solution 평균장 | `\Omega\to0`, `\Omega\to2RT^\pm`, spinodal 조건 | 단일 자리에서 격자기체로 확장 |
| 3 | Ch1 L647-L721, L918-L993 | `\mu_\mathrm{Li}=\mu^0-sF(V-U)`에서 ideal logistic 및 `\Omega` implicit 등온선 | 부호, 차원, detailed balance 정지점 | Ch1 `\xi_\eq`, `w_j`, `U_j^d`로 재접속 |
| 4 | Ch1 L953-L1064 | Eyring 속도비와 detailed balance가 같은 logistic을 주는지 대조 | `\chi` 상쇄, 정/역 flux 균형 | distribution route와 kinetic route 동일 결과로 닫음 |

## Part 0 LaTeX 전문

```latex
% ====================================================================
\section{Part 0. 통계역학 기초 — 분배함수에서 $\xi_{\eq}$ 와 $U_j$ 까지}
\label{sec:sm-foundation}
% ====================================================================

이 절은 뒤의 평형 중심, 폭, 히스테리시스, peak 식이 기대고 있는 최소 통계역학을 먼저 세운다.
대상은 통계역학을 아직 체계적으로 배우지 않은 독자다. 핵심은 하나다. 평형에서 계가 어떤 상태를 택하는지는
각 미시상태의 Boltzmann 가중을 모두 더한 분배함수로 정해지고, 흑연 삽입 자리 하나는 ``빈 자리/찬 자리'' 두 상태만
가지는 대정준 격자기체다.

\subsection{앙상블, 미시상태, Boltzmann 인자, 분배함수}

\textbf{(a) 출발.} 미시상태 $\alpha$ 는 같은 거시조건 $(T,V,\mu)$ 아래에서 계가 실제로 가질 수 있는 하나의
구체적 배치다. 온도 $T$ 의 열저장고와 접촉하면 에너지가 높은 상태일수록 확률이 작아지고, 그 상대 가중은
\begin{equation}
  w_\alpha = \exp[-\beta E_\alpha],
  \qquad
  \beta \equiv \frac{1}{k_B T}
  \label{eq:sm-boltzmann}
\end{equation}
이다. \textbf{(b) 연산.} 모든 미시상태의 가중을 더하면 정규화 상수, 곧 분배함수다:
\begin{equation}
  Z = \sum_\alpha \exp[-\beta E_\alpha].
  \label{eq:sm-Z-canonical}
\end{equation}
상태 확률은 $p_\alpha=\exp[-\beta E_\alpha]/Z$ 이므로, $Z$ 하나가 평형 평균을 모두 정한다.

\textbf{(c) 중간식.} 입자수도 저장고와 교환하면 에너지 $E_\alpha$ 만이 아니라 입자수 $N_\alpha$ 도 바뀐다.
입자 1개를 추가할 때 저장고가 지불하거나 회수하는 자유에너지 비용이 화학퍼텐셜 $\mu$ 이다. 따라서 대정준
가중은
\begin{equation}
  w_\alpha^{(\mu)} =
  \exp[-\beta(E_\alpha-\mu N_\alpha)]
  \label{eq:sm-grand-weight}
\end{equation}
이고, 대정준 분배함수는
\begin{equation}
  \Xi = \sum_\alpha \exp[-\beta(E_\alpha-\mu N_\alpha)].
  \label{eq:sm-grand-Z}
\end{equation}
\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  p_\alpha =
  \frac{\exp[-\beta(E_\alpha-\mu N_\alpha)]}{\Xi},
  \qquad
  \Xi=\sum_\alpha \exp[-\beta(E_\alpha-\mu N_\alpha)]\; .}
  \label{eq:sm-grand-prob}
\end{equation}
흑연 삽입 문제에서 저장고는 전해질과 상대극이고, 고정되는 것은 Li 의 전기화학 퍼텐셜이다.

\subsection{단일 삽입 자리의 2-상태 대정준 분배함수}

\textbf{(a) 출발.} 한 삽입 자리 하나만 떼어 보자. 미시상태는 빈 자리 $n=0$ 과 Li 하나가 들어간 자리 $n=1$
뿐이다. 빈 자리 에너지를 기준 $0$, 점유 에너지를 $\varepsilon$ 라고 두면 상태 $(n)$ 의 대정준 가중은
$\exp[-\beta(\varepsilon-\mu)n]$ 이다.

\textbf{(b) 연산.} 두 상태를 더하면 단일 자리 분배함수다:
\begin{equation}
  Z_1
  = \sum_{n=0,1} \exp[-\beta(\varepsilon-\mu)n]
  = 1+\exp[-\beta(\varepsilon-\mu)] .
  \label{eq:sm-Z1}
\end{equation}
점유 확률, 곧 평균 점유 $\theta=\langle n\rangle$ 는 점유 상태의 가중을 $Z_1$ 로 나눈 값이다:
\begin{equation}
  \theta
  = \langle n\rangle
  = \frac{\exp[-\beta(\varepsilon-\mu)]}{1+\exp[-\beta(\varepsilon-\mu)]}.
  \label{eq:sm-occ-mid}
\end{equation}

\textbf{(c) 중간식.} 분자와 분모를 $\exp[-\beta(\varepsilon-\mu)]$ 로 나누면
\begin{equation}
  \theta
  = \frac{1}{1+\exp[\beta(\varepsilon-\mu)]}.
  \label{eq:sm-theta-fd}
\end{equation}
이 식은 Fermi--Dirac 함수와 같은 대수 꼴이다. 여기서 같은 것은 함수형이지 물리량 자체가 아니다. 전자 준위가
아니라 Li 삽입 자리의 배타 점유가 같은 ``0 또는 1'' 구조를 만들었을 뿐이다.

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  \theta_\eq
  = \frac{1}{1+\exp[\beta(\varepsilon-\mu)]},
  \qquad
  \xi_\eq \equiv 1-\theta_\eq\; .}
  \label{eq:sm-theta-xi}
\end{equation}
$\theta$ 는 Li 점유율이고, $\xi$ 는 탈리튬화 진행률이다. 이 둘을 같은 물리량으로 읽으면 부호가 뒤집힌다.

\subsection{$M$ 독립 자리 — 격자기체와 mixing entropy}

\textbf{(a) 출발.} 동등한 삽입 자리 $M$ 개가 서로 상호작용하지 않는다고 하자. 점유 자리 수가 $N=M\theta$ 이면
배치 수는
\begin{equation}
  W(M,N)=\frac{M!}{N!(M-N)!}.
  \label{eq:sm-W}
\end{equation}
\textbf{(b) 연산.} Stirling 근사 $\ln m!\simeq m\ln m-m$ 를 쓰면 배치 엔트로피는
\begin{equation}
  S_\mathrm{mix}
  = k_B\ln W
  = -k_B M\left[\theta\ln\theta+(1-\theta)\ln(1-\theta)\right].
  \label{eq:sm-Smix}
\end{equation}
몰 기준으로 쓰면 $k_BM$ 이 $R$ 과 자리 몰수로 바뀐다.

\textbf{(c) 중간식.} 자리 1몰당 자유에너지는 기준 점유 비용 $\mu^0\theta$ 와 mixing 자유에너지의 합이다:
\begin{equation}
  \bar g_\mathrm{id}(\theta)
  = \mu^0\theta
  +RT\left[\theta\ln\theta+(1-\theta)\ln(1-\theta)\right].
  \label{eq:sm-g-id}
\end{equation}
이를 $\theta$ 로 미분하면 Li 한 몰을 더 넣는 자유에너지 비용, 곧 Li 화학퍼텐셜이다:
\begin{equation}
  \mu_\mathrm{Li}^{\mathrm{id}}(\theta)
  = \frac{\partial \bar g_\mathrm{id}}{\partial\theta}
  = \mu^0+RT\ln\frac{\theta}{1-\theta}.
  \label{eq:sm-mu-id}
\end{equation}

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  \mu_\mathrm{Li}^{\mathrm{id}}(\theta)
  = \mu^0+RT\ln\frac{\theta}{1-\theta}\; .}
  \label{eq:sm-mu-id-box}
\end{equation}
단일 자리 분배함수의 logistic 과 mixing entropy 미분은 같은 이상 격자기체의 두 표현이다.

\subsection{평균장 상호작용 $\Omega$ 와 regular solution}

\textbf{(a) 출발.} 삽입 자리 사이 상호작용을 평균장으로 한 항만 더한다. 선형 항은 기준 $\mu^0$ 에 흡수하고,
조성 의존 초과 자유에너지를 $\Omega\theta(1-\theta)$ 로 둔다. 그러면
\begin{equation}
  \bar g(\theta)
  = \mu^0\theta
  +RT\left[\theta\ln\theta+(1-\theta)\ln(1-\theta)\right]
  +\Omega\theta(1-\theta).
  \label{eq:sm-g-theta-rs}
\end{equation}

\textbf{(b) 연산.} $\theta$ 로 미분하면
\begin{equation}
  \mu_\mathrm{Li}(\theta)
  = \mu^0
  +RT\ln\frac{\theta}{1-\theta}
  +\Omega(1-2\theta).
  \label{eq:sm-mu-rs}
\end{equation}
이는 기존 식~\eqref{eq:mu} 의 재유도다.

\textbf{(c) 중간식.} Ch1 의 진행률은 $\xi=1-\theta$ 이다. 진행률 좌표에서는 상수와 직선 항을 떼고 조성 의존부만
남기면
\begin{equation}
  g_j(\xi)
  = g_j^0
  +RT\left[\xi\ln\xi+(1-\xi)\ln(1-\xi)\right]
  +\Omega_j\xi(1-\xi),
  \label{eq:sm-gxi}
\end{equation}
이고 이는 기존 식~\eqref{eq:gxi} 의 재배치다. 두 번 미분하면
\begin{equation}
  g_j''(\xi)
  = \frac{RT}{\xi(1-\xi)}-2\Omega_j.
  \label{eq:sm-gpp}
\end{equation}
가운데 $\xi=1/2$ 에서 곡률은 $4RT-2\Omega_j$ 이므로, 비볼록 구간이 생기는 문턱은
\begin{equation}
  \Omega_j>2RT.
  \label{eq:sm-spinodal-threshold}
\end{equation}

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  \mu_\mathrm{Li}(\theta)
  =\mu^0+RT\ln\frac{\theta}{1-\theta}+\Omega_j(1-2\theta),
  \qquad
  g_j''(\xi)=\frac{RT}{\xi(1-\xi)}-2\Omega_j\; .}
  \label{eq:sm-regular-solution-box}
\end{equation}
$\Omega_j\le2RT$ 이면 균질 단상 등온선이고, $\Omega_j>2RT$ 이면 spinodal 과 히스테리시스 절로 넘어간다.

\subsection{전기화학 연결 — $\mu_\mathrm{Li}$ 에서 $\xi_\eq$ logistic 으로}

\textbf{(a) 출발.} Li 삽입 평형은 전기화학 퍼텐셜의 균형이다. 전위 의존 항을 중심 전위 $U_j$ 로 묶으면 기존
평형 조건은
\begin{equation}
  \mu_\mathrm{Li}(\theta_\eq)
  = \mu^0 - sF(V-U_j),
  \qquad
  \Delta G_j=-sFU_j.
  \label{eq:sm-eqcond}
\end{equation}
여기서 $s=+1$ 은 방전 규약이다.

\textbf{(b) 연산.} 이상 격자기체 식~\eqref{eq:sm-mu-id-box} 를 식~\eqref{eq:sm-eqcond} 에 넣으면
\begin{equation}
  RT\ln\frac{\theta_\eq}{1-\theta_\eq}
  = -sF(V-U_j).
  \label{eq:sm-theta-logit}
\end{equation}
따라서
\begin{equation}
  \theta_\eq
  = \frac{1}{1+\exp[sF(V-U_j)/RT]},
  \qquad
  \xi_\eq=1-\theta_\eq
  = \frac{1}{1+\exp[-sF(V-U_j)/RT]}.
  \label{eq:sm-xi-ideal}
\end{equation}

\textbf{(c) 중간식.} 폭 척도 $w_j=n_jRT/F$ 와 방향별 중심 $U_j^{\,d}$ 를 넣으면 Ch1 의 평형 종이 된다:
\begin{equation}
  \xi_{\eq,j}(V,T)
  =
  \frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d})/w_j]}.
  \label{eq:sm-xieq}
\end{equation}
이는 기존 식~\eqref{eq:xieq} 의 통계역학 출발점이다. 단상에서는 $w_j=n_jRT/F$ 가 평형 분포 폭의 예측이고,
두-상에서는 같은 함수형을 쓰더라도 실측 종 폭을 broadening 이 정하는 현상학적 폭으로 읽어야 한다.

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  \xi_{\eq,j}
  =
  \frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d})/w_j]},
  \qquad
  w_j=\frac{n_jRT}{F}\; .}
  \label{eq:sm-xieq-box}
\end{equation}
전위를 올릴 때 방전 규약 $\sigma_d=+1$ 에서는 $\xi_\eq$ 가 증가한다. 이것은 탈리튬화 진행률이 증가한다는 뜻이지,
Li 점유율 $\theta$ 가 증가한다는 뜻이 아니다.

\subsection{$\Omega$ 가 있을 때의 implicit 등온선}

\textbf{(a) 출발.} 평균장 상호작용을 유지하면 식~\eqref{eq:sm-mu-rs} 와 식~\eqref{eq:sm-eqcond} 를 함께 풀어야 한다.
\textbf{(b) 연산.} $\theta=1-\xi$ 를 넣고 양변에 $-1$ 을 곱하면
\begin{equation}
  RT\ln\frac{\xi}{1-\xi}+\Omega_j(1-2\xi)
  =
  sF(V_\eq-U_j).
  \label{eq:sm-Veq-implicit}
\end{equation}
\textbf{(c) 중간식.} 이를 전위로 풀면
\begin{equation}
  V_{\eq,j}(\xi)
  =
  U_j+\frac{RT}{sF}\ln\frac{\xi}{1-\xi}
  +\frac{\Omega_j}{sF}(1-2\xi),
  \label{eq:sm-Veq}
\end{equation}
기존 식~\eqref{eq:Veq} 로 재접속한다. $\Omega_j=0$ 에서는 명시적 logistic 으로 되돌아가고,
$\Omega_j>2RT$ 에서는 $V_{\eq,j}(\xi)$ 가 비단조가 되어 spinodal 분기 절의 출발점이 된다.

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  sF(V_{\eq,j}-U_j)
  =
  RT\ln\frac{\xi}{1-\xi}+\Omega_j(1-2\xi)\; .}
  \label{eq:sm-implicit-isotherm}
\end{equation}
따라서 상호작용이 있는 경우의 ``분포''는 단순 Fermi 함수가 아니라 자기무모순 평균장 분포다.

\subsection{detailed balance 경로 — 같은 logistic 의 동역학적 회수}

\textbf{(a) 출발.} 전이상태 이론에서 장벽을 넘는 속도는 Boltzmann 꼬리 $e^{-\Delta G_a/RT}$ 에 비례한다.
구동력 $\mathcal A_j=sF(V-U_j)$ 가 정방향 장벽을 $\chi\mathcal A_j$ 만큼 낮추고 역방향 장벽을
$(1-\chi)\mathcal A_j$ 만큼 높이면
\begin{equation}
  r_j^+=k_0e^{-(\Delta G_{a,j}-\chi\mathcal A_j)/RT},
  \qquad
  r_j^-=k_0e^{-(\Delta G_{a,j}+(1-\chi)\mathcal A_j)/RT}.
  \label{eq:sm-rates}
\end{equation}

\textbf{(b) 연산.} 비를 취하면 $k_0$ 와 공통 장벽이 없어지고 $\chi$ 도 상쇄된다:
\begin{equation}
  \frac{r_j^+}{r_j^-}
  =
  \exp\left[\frac{\mathcal A_j}{RT}\right].
  \label{eq:sm-db}
\end{equation}
\textbf{(c) 중간식.} 정방향 flux 는 찬 자리 비율 $(1-\xi)$ 에서, 역방향 flux 는 빈 자리 비율 $\xi$ 에서 출발하므로
\begin{equation}
  \frac{\dd \xi}{\dd t}
  =
  r_j^+(1-\xi)-r_j^-\xi.
  \label{eq:sm-flux-balance}
\end{equation}
정지점에서 $r_j^+(1-\xi_\eq)=r_j^-\xi_\eq$ 이고,
\begin{equation}
  \frac{\xi_\eq}{1-\xi_\eq}
  =
  \frac{r_j^+}{r_j^-}
  =
  \exp\left[\frac{sF(V-U_j)}{RT}\right].
  \label{eq:sm-db-logit}
\end{equation}

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  \xi_\eq
  =
  \frac{1}{1+\exp[-sF(V-U_j)/RT]}\; .}
  \label{eq:sm-db-xi}
\end{equation}
대정준 분포 경로와 detailed balance 경로는 같은 평형 점유 분포를 서로 다른 언어로 읽은 것이다.

\subsection{거시 열역학 연결 — $G$, Nernst, $U_j(T)$}

\textbf{(a) 출발.} 등온ㆍ등압 전지에서 자발성과 평형을 판정하는 퍼텐셜은
\begin{equation}
  G \equiv H-TS,
  \qquad
  \mu \equiv \frac{\partial G}{\partial n}\Big|_{T,P}.
  \label{eq:sm-G-mu}
\end{equation}
입자 교환 평형은 전기화학 퍼텐셜 $\tilde\mu=\mu+zF\phi$ 의 균형이다.

\textbf{(b) 연산.} Li 삽입 반응의 비배치 몫 자유에너지를 전위로 환산하면
\begin{equation}
  \Delta G_j=-sFU_j.
  \label{eq:sm-dG-U}
\end{equation}
또한 이상 등온선 식~\eqref{eq:sm-implicit-isotherm} 에서 $\Omega_j=0$ 을 두면 Nernst 꼴
\begin{equation}
  V_{\eq,j}
  =
  U_j+\frac{RT}{sF}\ln\frac{\xi}{1-\xi}
  =
  U_j+\frac{RT}{sF}\ln\frac{1-\theta}{\theta}
  \label{eq:sm-nernst}
\end{equation}
이 나온다.

\textbf{(c) 중간식.} 반응 자유에너지가
\begin{equation}
  \Delta G_j(T)=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}
  \label{eq:sm-dG-HS}
\end{equation}
이면 식~\eqref{eq:sm-dG-U} 와 결합해
\begin{equation}
  \Delta H_{\rxn,j}-T\Delta S_{\rxn,j}
  =
  -F U_j
  \qquad (s=+1)
  \label{eq:sm-Uj-mid}
\end{equation}
이다.

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  U_j(T)
  =
  \frac{-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j}}{F},
  \qquad
  \frac{\partial U_j}{\partial T}
  =
  \frac{\Delta S_{\rxn,j}}{F}\; .}
  \label{eq:sm-Uj}
\end{equation}
이 식이 평형 중심 절의 기존 식~\eqref{eq:Uj} 로 이어지고, 식~\eqref{eq:sm-xieq-box} 의 중심 $U_j^{\,d}$ 를 정하는
첫 입력이 된다.
```

## 물리 자체검수 기록

| 항목 | 검수 | 판정 |
|---|---|---|
| 부호: `\mu_\mathrm{Li}=\mu^0-sF(V-U)` | `s=+1` 에서 `V` 상승은 `\theta` 감소, `\xi=1-\theta` 증가. Ch1 L444-L446, L1060-L1063과 정합. | PASS |
| 부호: `\Delta G_j=-sFU_j` | `s=+1`, `U_j>0` 이면 `\Delta G_j<0`; 기존 Ch1 L440-L445, L452-L460 재유도와 정합. | PASS |
| 차원 | `RT`, `\Omega`, `\Delta H`, `T\Delta S` 는 J/mol, `F(V-U)` 도 C/mol·V=J/mol. `w=RT/F` 는 V. | PASS |
| `\beta\to0` | 단일 자리 식에서 `e^{\beta(\varepsilon-\mu)}\to1`, `\theta\to1/2`, `\xi\to1/2`. 고온/무차별 점유와 정합. | PASS |
| `\beta\to\infty` | `\varepsilon>\mu` 이면 `\theta\to0`, `\varepsilon<\mu` 이면 `\theta\to1`. 2-상태 step limit. | PASS |
| `\Omega\to0` | `\mu` 와 `V_\eq` 에서 상호작용 항 소거, explicit logistic/Nernst로 환원. | PASS |
| `\Omega\to2RT^-` | `g''(\xi)=RT/[\xi(1-\xi)]-2\Omega` 의 최소값이 양수로 접근; spinodal 없음. | PASS |
| `\Omega\to2RT^+` | spinodal 두 점이 `\xi=1/2` 에서 갈라지기 시작; 기존 `u=\sqrt{1-2RT/\Omega}` 한계와 정합. | PASS |
| detailed balance | `r^+/r^-=\exp(\mathcal A/RT)` 에서 `\chi` 상쇄, 정지점 `\xi/(1-\xi)=r^+/r^-`; Ch1 L963-L979와 정합. | PASS |
| 함수형 동형 가드 | `\theta`, `\xi`, 전자 Fermi--Dirac은 같은 logistic 꼴일 수 있으나 물리량 동일로 쓰지 않도록 본문에 명시. | PASS |
| 두-상 폭 지위 | `w_j=n_jRT/F` 는 단상 평형 예측, 두-상에서는 broadening 현상학 폭이라는 기존 L936-L951, Ch2 L161-L175 구분 보존. | PASS |

## 재접속 표

| 신설 Part 0 위치 | 흡수/재조직한 원천 | 재접속 대상 | 처리 |
|---|---|---|---|
| `sec:sm-foundation` 첫 단락 | Ch2 L113-L118, Ch1 L1066-L1071 | Ch1 `sec:dist`, Ch2 `sec:partition` | 분배함수 언어를 Ch1 앞단으로 승격 |
| `eq:sm-Z1` | Ch2 L120-L127, Ch1 L1073-L1080 | 기존 `eq:Z1`, `eq:partfn` | 새 Part 0에서는 `eq:sm-Z1`; 편입 시 기존 Ch2는 참조/압축 후보 |
| `eq:sm-theta-fd` | Ch2 L128-L138, Ch1 L1081-L1087 | 기존 `eq:occ`, `eq:fermifn` | 점유 `\theta`와 진행률 `\xi` 구분을 먼저 고정 |
| `eq:sm-Smix` | Ch1 L587-L593 | 기존 `eq:mu` 유도 앞부분 | Stirling/mixing entropy 유도를 Part 0로 이동 |
| `eq:sm-mu-rs` | Ch1 L592-L597 | 기존 `eq:mu` | 결과는 동일, 본문에서는 기존 라벨 재사용 가능하나 드래프트 라벨은 `eq:sm-*` |
| `eq:sm-gxi`, `eq:sm-gpp` | Ch1 L598-L620 | 기존 `eq:gxi`, `eq:gpp`, `eq:spinodal` | 정규용액과 spinodal 문턱을 히스 절 앞 기초로 이동 |
| `eq:sm-eqcond` | Ch1 L417-L446 | 기존 `eq:eqcond` | 전기화학 부호와 `\Delta G=-sFU` 를 Part 0 말단과 중심 절 모두에서 참조 |
| `eq:sm-xieq-box` | Ch1 L953-L993, Ch2 L140-L159 | 기존 `eq:logisticsolve`, `eq:xieq`, Ch2 `eq:logistic` | logistic 평형 종의 통계역학 기원으로 재배치 |
| `eq:sm-implicit-isotherm`, `eq:sm-Veq` | Ch1 L647-L658, L1100-L1105 | 기존 `eq:Veq` | 상호작용이 있으면 명시 logistic이 아니라 implicit 평균장 등온선임을 연결 |
| `eq:sm-db`-`eq:sm-db-xi` | Ch1 L953-L979 | 기존 `eq:bv`, `eq:db`, `eq:logisticsolve` | kinetic detailed-balance 유도는 distribution 유도 뒤의 검증 경로로 재접속 |
| `eq:sm-Uj` | Ch1 L448-L467 | 기존 `eq:Ujmid`, `eq:Uj` | 거시 열역학과 중심 전위 계산식으로 재접속 |
| 두-상 폭 지위 문장 | Ch1 L924-L951, Ch2 L161-L175 | `sec:width`, `sec:broadening` | Part 0에서 단상/두-상 적용 한계를 먼저 경고 |

## 5줄 요약

1. Part 0는 `Z_1 -> \theta -> \xi -> \mu(\theta) -> V_\eq(\xi) -> U_j(T)` 사슬로 작성했다.
2. `\theta`는 Li 점유율, `\xi=1-\theta`는 탈리튬화 진행률이며, logistic 동형을 물리량 동일로 취급하지 않게 가드를 넣었다.
3. `\Omega=0`에서는 explicit logistic, `\Omega>0`에서는 평균장 implicit 등온선, `\Omega>2RT`에서는 spinodal/히스테리시스 재접속으로 분리했다.
4. 기존 `eq:mu`, `eq:gxi`, `eq:xieq`, `eq:Uj` 결과는 보존하되 신설 드래프트 라벨은 `eq:sm-*` 로 작성했다.
5. 최약점: 편입 시 기존 Ch1/Ch2 중복 절을 얼마나 압축할지는 master 편입 단계의 구조 결정이 필요하다.

## 갈래 2

- 작업 ID: C1
- 범위: Part II "LCO 양극" 도입 절 일원화 문안
- 출력 성격: master 편입 전 독립 드래프트. `.tex`/원본 코드 수정 없음.
- 원천 전문 정독 범위:
  - `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` L301-L355 (`sec:lco-map`)
  - `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` L846-L854 (`sec:lco-hys` 의 "★분기 부호의 전극-중립 읽기(한정)" 문단)
  - `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` L1426-L1437 (`sec:lco-peak` 의 "★방향 부호의 전극-중립 읽기(적용 한정)" 문단)
  - `Claude/results/process/V1012_P43_verify10.md` L42-L85, L101-L115, L124-L136 (`f=+\sigma_d` 확정 판정과 실행문)

## 갈래 2 절별 루핑 기록

| Loop | 원천 범위 | 독립 재유도 초점 | 자체검수 초점 | 앞 절 정합 |
|---|---:|---|---|---|
| 0 | Ch1 L301-L355 | LCO 는 새 전극이 아니라 같은 삽입형 골격에 전이 집합과 입력값을 끼우는 사례 | 코인 하프셀 범위, 전셀 합성 제외, LCO `\Omega` 미배정 지위 | Part 0의 `\xi=1-\theta` 와 같은 탈리튬화 진행률로 연결 |
| 1 | Ch1 L846-L854 | 분기 중심의 `+\tfrac12` 가지는 전극명이 아니라 탈리튬화 가지 | LCO 충전이 탈리튬화이므로 모델 슬롯 `\sigma_d=+1` | 기존 `U_j^{d}=U_j+\tfrac12\sigma_d...` 구조 보존 |
| 2 | Ch1 L1426-L1437 | 방향 부호 작용처를 분극ㆍ분기ㆍ꼬리 3곳으로 한정 | 평형 logistic 자체는 `\xi\leftrightarrow1-\xi` 여집합 대칭으로 방향 불변 | `sec:lco-map` 의 셀 라벨 설명과 입력 슬롯 규칙을 층위 분리 |
| 3 | verify10 L42-L85, L101-L115 | MSMR 진행률 pairing 에서 `f=+\sigma_d` 판정 수용 | `f=-\sigma_d` 재론 금지, 점유=진행률 등치 금지 | Part II 말미의 MSMR 예고로만 배치 |

## 갈래 2 LaTeX 문안

```latex
% ====================================================================
\section{Part II. LCO 양극 — 전극-중립 골격과 방향 슬롯}
\label{sec:lco-partii-intro}
% ====================================================================

Part II 는 흑연에서 세운 식을 버리고 새 양극 이론을 시작하는 장이 아니다.
삽입형 전극이면 유지되는 전극-중립 골격을 먼저 고정하고, LCO 에서만 바뀌는 입력값과 방향 슬롯을 그 위에 건다.
이 절의 목적은 세 곳에 흩어진 LCO 부호 설명을 한 곳에서 닫아, 뒤의 중심ㆍ분기ㆍpeakㆍMSMR 절이 같은 규약을 쓰게 하는 것이다.

\subsection{전극-중립 골격}

\textbf{(a) 출발.}
전극-중립으로 남는 것은 네 가지다. 첫째, 실험조건은 방향 슬롯과 전류 크기로 들어간다. 둘째, 전이 인덱스 $j$ 와
진행률 $\xi_j$ 는 용량 보존식에 들어간다. 셋째, 평형 중심 $U_j$ 와 폭 $w_j$ 는 logistic 종을 정한다.
넷째, 히스테리시스가 켜지면 같은 정규용액 spinodal 식이 분기 중심을 만든다.

\textbf{(b) 연산.}
LCO 에서는 전이 집합과 파라미터만 양극 값으로 치환한다:
\begin{equation}
  \mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\},
  \qquad
  j\in\mathcal J_\mathrm{LCO},
  \label{eq:lco-intro-J}
\end{equation}
\begin{equation}
  (U_j,Q_j,\Omega_j,\Delta H_{\rxn,j},\Delta S_{\rxn,j},\Delta H_{a,j})
  \longmapsto
  (U_j^\mathrm{cat},Q_j^\mathrm{cat},\Omega_j^\mathrm{cat},
  \Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat},
  \Delta H_{a,j}^\mathrm{cat}).
  \label{eq:lco-intro-param-map}
\end{equation}
따라서 전하 보존식은
\begin{equation}
  Q_\cell q
  =
  Q_\bg+\sum_{j\in\mathcal J_\mathrm{LCO}}Q_j^\mathrm{cat}\xi_j,
  \qquad
  \frac{\dd Q}{\dd V}
  =
  C_\bg+\sum_{j\in\mathcal J_\mathrm{LCO}}Q_j^\mathrm{cat}\frac{\dd\xi_j}{\dd V}.
  \label{eq:lco-intro-charge}
\end{equation}

\textbf{(c) 중간식.}
평형 종의 함수형도 host 이름을 보지 않는다:
\begin{equation}
  \xi_{\eq,j}^\mathrm{cat}
  =
  \frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]},
  \qquad
  U_j^{\,d,\mathrm{cat}}
  =
  U_j^\mathrm{cat}
  +\frac12\sigma_d h_{\eta,j}\gamma_j\Delta U_j^{\hys,\mathrm{cat}}.
  \label{eq:lco-intro-xi-branch}
\end{equation}
단, 이 식은 LCO 의 $\Omega_j^\mathrm{cat}$ 가 이미 배정됐다는 뜻이 아니다. 현 LCO 초기값과 코드는 $\Omega$ 키가
미배정이면 $\Omega=0$ 으로 닫아 분기와 gap 을 비활성한다. 식~\eqref{eq:lco-intro-xi-branch} 의 분기 항은
round-trip 피팅에서 $\Omega_j^\mathrm{cat}>2RT$ 로 배정되는 전이에 한해 작동한다.

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  \text{LCO 도입의 기본 연산}
  =
  \text{전극-중립 식}
  +
  \{j,U,Q,\Omega,\Delta H,\Delta S,\Delta H_a\}_\mathrm{cat}
  +
  \Delta S_e\ \text{gate}\; .}
  \label{eq:lco-intro-skeleton-box}
\end{equation}
흑연 식과 부호를 바꾸는 것이 아니라, 같은 슬롯에 LCO 전이표와 MIT 전자 엔트로피 항을 추가한다.

\subsection{셀 라벨과 모델 방향 슬롯}

\textbf{(a) 출발.}
이 절부터 모델 입력 슬롯의 방향 부호 $\sigma_d$ 는 셀 라벨이 아니라 물리 진행 방향을 뜻한다:
\begin{equation}
  \sigma_d=
  \begin{cases}
  +1, & \text{탈리튬화(산화) 진행},\\
  -1, & \text{리튬화(환원) 진행}.
  \end{cases}
  \label{eq:lco-intro-sigma}
\end{equation}
흑연 음극 하프셀에서는 방전 라벨이 탈리튬화와 겹치므로 라벨과 물리가 우연히 일치한다. LCO 하프셀에서는 그렇지 않다.

\textbf{(b) 연산.}
LCO 는 충전 때 Li 가 빠지고 Co 가 산화되며 전위가 올라간다:
\begin{equation}
  \mathrm{LCO\ charge}:\quad
  x\downarrow,\quad V\uparrow,\quad \xi:0\to1,\quad \sigma_d=+1.
  \label{eq:lco-intro-charge-slot}
\end{equation}
방전 때는 Li 가 들어가고 전위가 내려간다:
\begin{equation}
  \mathrm{LCO\ discharge}:\quad
  x\uparrow,\quad V\downarrow,\quad \xi:1\to0,\quad \sigma_d=-1.
  \label{eq:lco-intro-discharge-slot}
\end{equation}
따라서 \S\ref{sec:lco-map} 의 ``LCO 방전은 리튬화''는 셀 동작 라벨의 뜻이고, 식에 넣는
$\sigma_d$ 는 그 라벨 자체가 아니라 탈리튬화 여부다.

\textbf{(c) 중간식.}
평형 종은 이 슬롯 선택에 대해 여집합만 바뀐다. $L(z)\equiv(1+e^{-z})^{-1}$, $u=(V-U)/w$ 로 두면
\begin{equation}
  \xi_{+}(u)=L(u),\qquad
  \xi_{-}(u)=L(-u)=1-L(u)=1-\xi_+(u).
  \label{eq:lco-intro-complement}
\end{equation}
미분 peak 모양은
\begin{equation}
  \left|\frac{\dd\xi_{\eq,j}}{\dd V}\right|
  =
  \frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
  \label{eq:lco-intro-peak-invariant}
\end{equation}
이므로 $\xi\leftrightarrow1-\xi$ 교환에 불변이다. 방향 규칙이 갈라놓는 것은 평형 봉우리 자체가 아니라
아래 세 작용처다.

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  \begin{array}{lll}
  \text{분극} &:& V_n=V_\app-\sigma_d|I|R_n,\\[2pt]
  \text{분기} &:& U_j^{\,d}=U_j+\tfrac12\sigma_d h_{\eta,j}\gamma_j\Delta U_j^\hys,\\[2pt]
  \text{꼬리} &:& \text{causal memory is taken along the } \sigma_d \text{ progress direction.}
  \end{array}
  \;}
  \label{eq:lco-intro-three-slots}
\end{equation}
LCO 충전 곡선은 이 세 작용처에 $\sigma_d=+1$ 로 걸고, LCO 방전 곡선은 $\sigma_d=-1$ 로 건다.
그래야 탈리튬화 가지가 높은 전위 쪽, 리튬화 가지가 낮은 전위 쪽이라는 이중웰 기하가 전극 이름과 무관하게 유지된다.

\subsection{MSMR 예고 — 같은 물리량끼리 pairing}

\textbf{(a) 출발.}
MSMR(multi-species, multi-reaction)과 본 문건의 logistic 은 함수형이 닮았다는 이유만으로 연결하면 안 된다.
점유율은 점유율끼리, 탈리튬화 진행률은 탈리튬화 진행률끼리 맞대야 한다.

\textbf{(b) 연산.}
전압 폭으로 재모수화한 MSMR 항을
\begin{equation}
  \theta_j^\mathrm{MSMR}
  =
  \frac{1}{1+\exp[+\sigma_d(V-U_j)/\omega_j^{(V)}]},
  \qquad
  \xi_j^\mathrm{MSMR}=1-\theta_j^\mathrm{MSMR}
  =
  \frac{1}{1+\exp[-\sigma_d(V-U_j)/\omega_j^{(V)}]}
  \label{eq:lco-intro-msmr-pair}
\end{equation}
로 쓰면, 진행률끼리의 지수는 식~\eqref{eq:lco-intro-xi-branch} 와 같은 부호를 가진다.

\textbf{(c) 중간식.}
따라서 MSMR 방향 인자 대응은 이미 확정된
\begin{equation}
  \boxed{\;f=+\sigma_d\;}
  \label{eq:lco-intro-msmr-sign}
\end{equation}
이다. 이 절은 이 판정을 재론하지 않는다. $f=-\sigma_d$ 는 점유율을 탈리튬화 진행률에 직접 등치할 때 생기는
여집합 뒤바꿈이며, Part II 의 방향 슬롯 규약에서는 사용하지 않는다.

\textbf{(d) 박스.}
\begin{equation}
  \boxed{\;
  \text{LCO Part II 규약: }
  \mathrm{charge}\mapsto\sigma_d=+1,\quad
  \mathrm{discharge}\mapsto\sigma_d=-1,\quad
  f=+\sigma_d,\quad
  \left|\dd\xi/\dd V\right|\ \text{is unchanged by }\xi\leftrightarrow1-\xi\; .}
  \label{eq:lco-intro-rule-box}
\end{equation}
``전극-중립''은 셀 라벨을 무시한다는 뜻이 아니다. 전극에 따라 셀 라벨과 탈리튬화 방향의 대응이 달라지므로,
식에는 라벨이 아니라 탈리튬화 방향을 넣는다는 뜻이다.
```

## 갈래 2 물리 자체검수 기록

| 항목 | 검수 | 판정 |
|---|---|---|
| 전극-중립 골격 | `Q_bg+\sum Q_j\xi_j`, logistic, spinodal, peak 식은 host 이름이 아니라 삽입 자리와 진행률 정의만 요구한다. | PASS |
| LCO 방향 슬롯 | LCO 충전은 `x↓, V↑, \xi↑` 이므로 탈리튬화 슬롯 `\sigma_d=+1`; LCO 방전은 리튬화 슬롯 `\sigma_d=-1`. | PASS |
| `sec:lco-map` 표면 충돌 | 기존 "방전 `\sigma_d=+1`" 표현은 셀 라벨 의미론, 새 도입 절은 모델 입력 슬롯 의미론으로 분리했다. | PASS |
| 평형 종 불변 | `L(-u)=1-L(u)` 이므로 `\xi\leftrightarrow1-\xi`; `\xi(1-\xi)` peak 모양은 방향 불변. | PASS |
| 방향 의존 3작용처 | 분극 `V_n`, 분기 `U_j^d`, 꼬리 인과 방향만 `\sigma_d` 슬롯이 물리 방향으로 필요하다. | PASS |
| LCO `\Omega` 지위 | LCO `\Omega_j^\mathrm{cat}` 미배정 및 코드 폴백 `0` 지위를 본문에 명시해 히스 분기 활성처럼 쓰지 않았다. | PASS |
| MSMR 부호 | `V1012_P43_verify10.md` 확정 판정대로 `f=+\sigma_d`; 재론하거나 `f=-\sigma_d`를 대안으로 열지 않았다. | PASS |
| 함수형 동형 가드 | MSMR 점유율과 Ch1 진행률을 직접 등치하지 않고, 점유↔점유ㆍ진행률↔진행률 pairing 으로 제한했다. | PASS |
| 수치 날조 방지 | LCO 미배정 `\Omega`, gap, 실제 peak 전위 수치를 새로 만들지 않았다. figure도 무차원 logistic 식만 평가했다. | PASS |

## figure

| Figure | 목적 | 형식 | 배치 | 캡션 |
|---|---|---|---|---|
| `fig:lco-direction-slot` | LCO에서 셀 라벨과 모델 방향 슬롯이 분리됨을 시각화하고, `\xi_-(u)=1-\xi_+(u)` 및 peak shape 불변을 보여준다. | matplotlib 생성 스크립트 + PNG. 실제 평가식은 `\xi_+(u)=1/(1+e^{-u})`, `\xi_-(u)=1/(1+e^{u})`, `\xi(1-\xi)`. | Part II 도입 절의 `셀 라벨과 모델 방향 슬롯` subsection 뒤. | `LCO direction slot. The equilibrium species for opposite slots are complements, so the peak shape is unchanged; direction-dependent effects enter polarization, branch, and tail.` |

- 스크립트: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_C1_lco_direction_slot.py`
- PNG: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_C1_lco_direction_slot.png`
- 라벨: 영어/ASCII 만 사용. 생성 후 PNG 렌더에서 글자 깨짐 없음 확인.
- 수치 지위: 실제 LCO 전이 수치나 미배정 `\Omega_j^\mathrm{cat}` 를 넣지 않고, 방향 슬롯 설명에 필요한 무차원 logistic 식만 평가했다.

```latex
\begin{figure}[t]
\centering
\includegraphics[width=0.78\linewidth]{V1013_P21_fig_C1_lco_direction_slot.png}
\caption{LCO direction slot. The two model slots evaluate the same logistic species in complementary coordinates,
so $\xi_-(u)=1-\xi_+(u)$ and $\xi(1-\xi)$ is unchanged. The direction choice is therefore applied to
polarization, hysteresis branch, and tail memory, not to invent a new equilibrium peak.}
\label{fig:lco-direction-slot}
\end{figure}
```

## 최종 5줄 요약

1. 갈래 2는 LCO Part II 도입 절을 `전극-중립 식 + LCO 파라미터 치환 + 방향 슬롯` 구조로 일원화했다.
2. 핵심 부호는 `\sigma_d=+1`을 탈리튬화 진행으로 정의하는 것이며, LCO 충전 곡선은 이 슬롯에 들어간다.
3. 평형 종은 `\xi\leftrightarrow1-\xi` 여집합 대칭으로 peak shape 이 불변이고, 방향 의존은 분극ㆍ분기ㆍ꼬리 3작용처에 한정된다.
4. `f=+\sigma_d` 는 `V1012_P43_verify10.md` 확정 판정으로만 사용했고, LCO `\Omega` 미배정 상태를 새 수치로 메우지 않았다.
5. 최약점: `sec:lco-map` 의 기존 셀 라벨 서술과 새 입력 슬롯 규칙을 master 편입 때 같은 기호 `\sigma_d` 로 계속 둘지, 별도 라벨 기호를 둘지 편집 결정이 필요하다.
