# V1013 P2.1 갈래 1 draft C2

## 수행 범위와 원천 읽기 기록

| 항목 | 실제 확인 범위 | 지위 |
|---|---:|---|
| 작업 지시문 `v1013_p21_base.txt` | 1-27행 | 전문 정독 완료 |
| `graphite_ica_ch1_v1.0.13.tex` `sec:center` | 411-475행 | 지정 범위 전문 정독 완료 |
| `graphite_ica_ch1_v1.0.13.tex` `sec:hys` | 578-751행 | 지정 범위 전문 정독 완료 |
| `graphite_ica_ch1_v1.0.13.tex` `sec:width`, `sec:dist` | 918-1139행 | 지정 범위 전문 정독 완료 |
| `graphite_ica_ch2_v1.0.13.tex` `eq:Z1` 절 | 110-180행 | 지정 범위 전문 정독 완료 |
| `graphite_ica_ch2_v1.0.13.tex` 추가 문맥 | 181-220행 | 180행 문장 연결부와 Bragg--Williams 임계 문맥 확인 |

## Part 0 LaTeX 전문

```latex
% ====================================================================
\section{Part 0. 통계역학 기초: 점유 분포에서 평형 전위까지}\label{sec:sm-foundation}
% ====================================================================
이 절의 목적은 Chapter 1 이 뒤에서 쓰는 logistic 평형 종, regular-solution 항,
평형 중심 전위 $U_j(T)$ 가 모두 같은 평형 통계의 다른 투영임을 먼저 고정하는 것이다.
양자역학은 쓰지 않는다. 필요한 것은 미시상태, Boltzmann 인자, 분배함수, 화학퍼텐셜,
그리고 입자수를 저장고와 교환하는 grand-canonical ensemble 이다.

\subsection{Ensemble, 미시상태, Boltzmann 인자}

\textbf{(a) 출발.}
거시상태 $(T,V,N)$ 하나에는 많은 미시상태 $\alpha$ 가 대응한다. 미시상태의 에너지가
$E_\alpha$ 이면, 온도 $T$ 의 열저장고와 평형인 계에서 그 상태의 상대 확률은
\begin{equation}
P_\alpha \propto e^{-\beta E_\alpha},\qquad
\beta\equiv\frac{1}{k_B T}.
\label{eq:sm-boltzmann}
\end{equation}

\textbf{(b) 연산.}
확률을 1로 정규화하는 합이 canonical partition function 이다.
\begin{equation}
Z_N(T,V)=\sum_{\alpha\in N} e^{-\beta E_\alpha},\qquad
P_\alpha=\frac{e^{-\beta E_\alpha}}{Z_N}.
\label{eq:sm-ZN}
\end{equation}
입자수까지 저장고와 교환하면 미시상태의 입자수 $N_\alpha$ 도 바뀐다. 입자 1개를
계 안에 두는 자유에너지 비용을 reservoir chemical potential $\mu$ 로 읽으면,
grand-canonical 가중치는
\begin{equation}
P_\alpha=\frac{e^{-\beta(E_\alpha-\mu N_\alpha)}}{\Xi},\qquad
\Xi(T,V,\mu)=\sum_\alpha e^{-\beta(E_\alpha-\mu N_\alpha)}.
\label{eq:sm-grand}
\end{equation}

\textbf{(c) 중간식.}
$\mu$ 는 입자수 변화에 대한 자유에너지 기울기다. 몰수 $n$ 을 쓰는 등온ㆍ등압 전지에서는
기존 식~\eqref{eq:mudef} 처럼
\begin{equation}
G\equiv H-TS,\qquad
\mu=\left(\frac{\partial G}{\partial n}\right)_{T,P}.
\label{eq:sm-Gmu}
\end{equation}
따라서 $\mu$ 는 ``입자 1몰을 더 넣는 Gibbs free energy 비용''이다.

\textbf{(d) 박스.}
\begin{equation}
\boxed{\;
\text{grand-canonical 평형은 }E-\mu N\text{ 을 최소화하는 통계적 점유 문제다.}
\;}
\label{eq:sm-grand-box}
\end{equation}

\subsection{단일 삽입 자리: 2-상태 grand-canonical 분배함수}

\textbf{(a) 출발.}
삽입 자리 하나는 비어 있거나($n=0$) Li 하나가 점유한다($n=1$). 빈 자리의 에너지를
0, 점유 자리의 에너지를 $\varepsilon$ 로 잡는다.

\textbf{(b) 연산.}
두 미시상태를 grand-canonical 가중치로 더하면
\begin{equation}
\mathcal Z_1
=\sum_{n=0}^{1}\exp[-\beta(\varepsilon-\mu)n]
=1+\exp[-\beta(\varepsilon-\mu)].
\label{eq:sm-Z1}
\end{equation}

\textbf{(c) 중간식.}
평균 점유율은 점유 상태의 확률이다.
\begin{align}
\theta
&=\langle n\rangle
=\frac{0\cdot 1+1\cdot e^{-\beta(\varepsilon-\mu)}}{\mathcal Z_1}
\notag\\
&=\frac{e^{-\beta(\varepsilon-\mu)}}{1+e^{-\beta(\varepsilon-\mu)}}
=\frac{1}{1+e^{\beta(\varepsilon-\mu)}}.
\label{eq:sm-theta1}
\end{align}

\textbf{(d) 박스.}
\begin{equation}
\boxed{\;
\theta(\mu,T)=\frac{1}{1+\exp[\beta(\varepsilon-\mu)]}
\;}
\label{eq:sm-theta-box}
\end{equation}
이 식은 Fermi--Dirac 함수와 같은 대수형이다. 그러나 여기의 입자는 전자가 아니라 Li
삽입 자리의 배타 점유다. 함수형 동형은 물리량 동일을 뜻하지 않는다.

\subsection{$M$ 개 독립 자리: ideal lattice gas}

\textbf{(a) 출발.}
서로 독립인 동등한 자리 $M$ 개가 있으면 전체 grand partition function 은 단일 자리
분배함수의 곱이다.
\begin{equation}
\Xi_M=\mathcal Z_1^M
=\left(1+e^{-\beta(\varepsilon-\mu)}\right)^M.
\label{eq:sm-XiM}
\end{equation}

\textbf{(b) 연산.}
평균 점유수와 점유율은
\begin{equation}
\langle N\rangle
=\frac{1}{\beta}\frac{\partial \ln \Xi_M}{\partial \mu}
=M\theta,\qquad
\theta=\frac{\langle N\rangle}{M}.
\label{eq:sm-Navg}
\end{equation}
같은 결과는 조합수 $W=M!/[N!(M-N)!]$ 에 Stirling 근사
$\ln m!\simeq m\ln m-m$ 를 적용해 얻는 mixing entropy 로도 닫힌다.
자리 1몰 기준 ideal lattice-gas 자유에너지는
\begin{equation}
\bar g_{\rm id}(\theta)
=\mu^0\theta
 +RT\{\theta\ln\theta+(1-\theta)\ln(1-\theta)\}.
\label{eq:sm-gid}
\end{equation}

\textbf{(c) 중간식.}
부분몰 자유에너지, 곧 Li chemical potential 은
\begin{equation}
\mu_{\rm Li}^{\rm id}(\theta)
=\frac{\partial \bar g_{\rm id}}{\partial \theta}
=\mu^0+RT\ln\frac{\theta}{1-\theta}.
\label{eq:sm-mu-id}
\end{equation}

\textbf{(d) 박스.}
\begin{equation}
\boxed{\;
\frac{\theta}{1-\theta}
=\exp\!\left[\frac{\mu_{\rm Li}^{\rm id}-\mu^0}{RT}\right]
\;}
\label{eq:sm-logit-id}
\end{equation}
logistic 과 Nernst logarithm 은 같은 식의 정방향ㆍ역방향 표현이다.

\subsection{Mean-field 상호작용: regular solution}

\textbf{(a) 출발.}
실제 삽입 자리는 독립이 아니다. 평균장에서는 상호작용의 조성 의존 몫을
$\Omega\theta(1-\theta)$ 로 둔다. 그러면
\begin{equation}
\bar g(\theta)
=\mu^0\theta
 +RT\{\theta\ln\theta+(1-\theta)\ln(1-\theta)\}
 +\Omega_j\theta(1-\theta).
\label{eq:sm-gtheta-rs}
\end{equation}

\textbf{(b) 연산.}
$\theta$ 로 미분하면 기존 식~\eqref{eq:mu} 로 쓰이는 regular-solution chemical potential 이 나온다.
\begin{equation}
\mu_{\rm Li}(\theta)
=\mu^0+RT\ln\frac{\theta}{1-\theta}
 +\Omega_j(1-2\theta).
\label{eq:sm-mu-rs}
\end{equation}

\textbf{(c) 중간식.}
탈리튬화 진행률을 $\xi\equiv1-\theta$ 로 두면, 상수항과 공통 직선항을 떼어낸 조성 자유에너지는
기존 식~\eqref{eq:gxi} 와 같은 regular-solution 형이다.
\begin{equation}
g_j(\xi)
=g_j^0
 +RT\{\xi\ln\xi+(1-\xi)\ln(1-\xi)\}
 +\Omega_j\xi(1-\xi).
\label{eq:sm-gxi}
\end{equation}
곡률은
\begin{equation}
g_j''(\xi)
=\frac{RT}{\xi(1-\xi)}-2\Omega_j.
\label{eq:sm-gpp}
\end{equation}

\textbf{(d) 박스.}
spinodal 은 $g_j''=0$ 에서
\begin{equation}
\boxed{\;
\xi_{s,j}^{\pm}=\frac12(1\pm u_j),\qquad
u_j=\sqrt{1-\frac{2RT}{\Omega_j}},\qquad
\Omega_j>2RT.
\;}
\label{eq:sm-spinodal}
\end{equation}
$\Omega_j\le2RT$ 이면 실수 spinodal 이 없고 균질 단상이다. $\Omega_j>2RT$ 이면 가운데
곡률이 음수가 되는 구간이 생기며, 기존 \S\ref{sec:hys} 의 hysteresis gap 유도는 이
식의 두 끝점을 전위 곡선에 대입해 진행된다.

\subsection{전기화학 연결: 점유율에서 $\xi_{\eq}$ logistic 으로}

\textbf{(a) 출발.}
기존 식~\eqref{eq:eqcond} 의 평형 조건은
\begin{equation}
\mu_{\rm Li}(\theta_{\eq})
=\mu^0-sF(V-U_j).
\label{eq:sm-muV}
\end{equation}
여기서 $s=+1$ 은 Chapter 1 방전 규약이다. $F(V-U_j)$ 는 molar electric work 이므로
$RT$ 및 $\Omega_j$ 와 같은 J/mol 차원을 갖는다.

\textbf{(b) 연산.}
이상 격자기체에서는 식~\eqref{eq:sm-mu-id} 와 식~\eqref{eq:sm-muV} 를 같게 놓아
\begin{equation}
RT\ln\frac{\theta_{\eq}}{1-\theta_{\eq}}
=-sF(V-U_j).
\label{eq:sm-theta-logit-V}
\end{equation}
따라서
\begin{equation}
\theta_{\eq}(V,T)
=\frac{1}{1+\exp[sF(V-U_j)/RT]}.
\label{eq:sm-thetaV}
\end{equation}
탈리튬화 진행률 $\xi_{\eq}=1-\theta_{\eq}$ 는
\begin{equation}
\xi_{\eq}(V,T)
=\frac{1}{1+\exp[-sF(V-U_j)/RT]}.
\label{eq:sm-xiV-id}
\end{equation}

\textbf{(c) 중간식.}
폭 $w_j=n_jRT/F$ 와 방향별 중심 $U_j^{\,d}$ 를 쓰면 기존 식~\eqref{eq:xieq} 의 모양으로
\begin{equation}
\boxed{\;
\xi_{\eq,j}(V,T)
=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d})/w_j]},
\qquad
w_j=\frac{n_jRT}{F}.
\;}
\label{eq:sm-xieq}
\end{equation}
regular solution 에서는 닫힌 logistic 이 아니라 자기무모순 방정식이 된다.
\begin{equation}
RT\ln\frac{\xi_{\eq}}{1-\xi_{\eq}}
\Omega_j(1-2\xi_{\eq})
=sF(V-U_j).
\label{eq:sm-xi-implicit}
\end{equation}
$\Omega_j=0$ 을 넣으면 식~\eqref{eq:sm-xiV-id} 로 되돌아간다.

\textbf{(d) 박스.}
\begin{equation}
\boxed{\;
V_{\eq,j}(\xi)
=U_j+\frac{RT}{sF}\ln\frac{\xi}{1-\xi}
 +\frac{\Omega_j}{sF}(1-2\xi)
\;}
\label{eq:sm-Veq}
\end{equation}
이는 기존 식~\eqref{eq:Veq} 로 재사용되는 전위-조성 식이다. $s=+1$ 에서
$V>U_j$ 이면 $\theta_{\eq}$ 는 감소하고 $\xi_{\eq}$ 는 증가한다.

\subsection{거시 열역학 연결: $G$, Nernst, $\Delta G_j=-sFU_j$}

\textbf{(a) 출발.}
등온ㆍ등압 전지의 평형 기준은 Gibbs free energy 이다.
\begin{equation}
G=H-TS,\qquad
\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}.
\label{eq:sm-DG}
\end{equation}

\textbf{(b) 연산.}
삽입 반응의 전기화학 평형에서 전위 의존 항만 분리하면 기존 식~\eqref{eq:eqcond} 처럼
\begin{equation}
\mu_{\rm Li}(\theta_{\eq})=\mu^0-sF(V-U_j),\qquad
\Delta G_j=-sF U_j.
\label{eq:sm-eqcond}
\end{equation}

\textbf{(c) 중간식.}
$s=+1$ 이고 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 이면
\begin{equation}
\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}=-F U_j.
\label{eq:sm-Uj-mid}
\end{equation}

\textbf{(d) 박스.}
\begin{equation}
\boxed{\;
U_j(T)=\frac{-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j}}{F}
\;}
\label{eq:sm-Uj}
\end{equation}
또한 식~\eqref{eq:sm-xiV-id} 를 뒤집으면 ideal Nernst form 이다.
\begin{equation}
V=U_j+\frac{RT}{sF}\ln\frac{\xi_{\eq}}{1-\xi_{\eq}}.
\label{eq:sm-nernst-xi}
\end{equation}
따라서 Part 0 의 분배함수, Chapter 1 의 logistic 평형 종, regular-solution 전위 곡선,
그리고 $U_j(T)$ 의 열역학 환산은 하나의 사슬로 닫힌다.
```

## 자체검수 기록

| 검수 항목 | 결과 |
|---|---|
| 부호 | Ch1 440-446의 `\mu_{\rm Li}=\mu^0-sF(V-U)`에서 독립 재유도했다. 이상 격자기체는 `RT ln[theta/(1-theta)] = -sF(V-U)`이므로 `s=+1`에서 `V↑ => theta↓, xi=1-theta↑`다. 이는 Ch2 147-153 및 Ch1 1060-1063과 정합한다. |
| 원천 긴장 | Ch1 1088-1098은 `\langle n\rangle`을 자리 점유 `theta`로 부르면서 지수 부호가 `xi` 증가식 쪽으로 적혀 있다. Part 0은 Ch1 440-446, Ch2 147-153을 기준으로 `theta`와 `xi`를 분리했다. 정정 제안: Ch1 `sec:dist` 편입 시 `\Delta\mu=sF(V-U_j)`로 두어 `\theta=1/(1+e^{+sF(V-U_j)/RT})`, `\xi=1-\theta`로 고친다. |
| 차원 | `RT`, `\Omega_j`, `F(V-U_j)`, `\Delta G_j`, `\Delta H_{\rxn}`은 모두 J/mol. `w_j=n_jRT/F`는 V. 지수 인자는 무차원. |
| `\beta\to0` | 단일 자리 식 `theta=1/(1+e^{\beta(\varepsilon-\mu)})`에서 `theta->1/2`. 고온에서는 두 상태가 같은 확률에 접근한다. |
| `\beta\to\infty` | `\varepsilon>\mu`이면 `theta->0`, `\varepsilon<\mu`이면 `theta->1`. 영온 극한은 step function 이다. |
| `\Omega\to0` | 식 `eq:sm-xi-implicit`이 ideal logistic `eq:sm-xiV-id`로 환원된다. |
| `\Omega\to2RT^\pm` | `\Omega\le2RT`에서는 실수 spinodal 이 없다. `\Omega\to2RT^+`에서 `u_j->0`이므로 기존 hysteresis gap 식의 시작점도 0으로 연속 소멸한다. |
| detailed balance | Ch1 953-993의 Eyring 경로와 양립한다. 장벽 분율 `\chi`는 속도비에서 상쇄되고, 정지점 `r^+(1-\xi)=r^-\xi`가 같은 logistic 을 준다. |
| 함수형 동형 가드 | Fermi--Dirac 꼴은 `한 자리 0/1 배타 점유`의 대수형 동형으로만 사용했다. Li 삽입 자리 점유를 전도 전자와 같은 물리량으로 동일시하지 않았다. |

## 재접속 표

| 원천 위치 | Part 0 흡수 위치 | 이후 원천 절로의 재접속 |
|---|---|---|
| Ch2 110-139 `eq:Z1`, `eq:occ` | `eq:sm-Z1`, `eq:sm-theta1`, `eq:sm-theta-box` | 기존 Ch2 `sec:partition`의 단일 자리 분배함수 설명은 Part 0의 출발점으로 승격된다. |
| Ch2 140-159 `eq:muV`, `eq:logistic` | `eq:sm-muV`, `eq:sm-thetaV`, `eq:sm-xiV-id` | Ch1 `eq:xieq`의 부호를 먼저 고정한다. `theta` 감소와 `xi` 증가를 분리해 재사용한다. |
| Ch2 161-178 keybox | `eq:sm-xieq` 주변 설명 | `w_j`의 지위는 Part 0에서 `ideal 단상 예측`으로만 세우고, 두-상 현상학적 폭은 기존 broadening 절로 넘긴다. |
| Ch2 180-188 `eq:Vxi` | `eq:sm-nernst-xi` | Nernst 로그항이 곡선맞춤이 아니라 mixing entropy/점유분포에서 온다는 연결을 Part 0에 선행 배치한다. |
| Ch2 190-218 `eq:BW`, `eq:slope_BW` | `eq:sm-gtheta-rs`, `eq:sm-gpp`, `eq:sm-spinodal` | Bragg--Williams 평균장과 `\Omega=2RT` 임계는 Ch1 `sec:hys`의 spinodal 유도로 재접속된다. |
| Ch1 411-446 `sec:center` 평형 조건 | `eq:sm-Gmu`, `eq:sm-muV`, `eq:sm-eqcond` | 기존 `eq:gibbsdef`, `eq:mudef`, `eq:eqcond`는 Part 0 뒤에서 짧게 참조하는 식으로 줄일 수 있다. |
| Ch1 448-467 `U_j(T)` | `eq:sm-DG`, `eq:sm-Uj-mid`, `eq:sm-Uj` | 기존 `eq:Uj`는 Part 0의 거시 열역학 박스를 참조해 코드 환산 설명만 남길 수 있다. |
| Ch1 586-620 `eq:mu`, `eq:gxi`, `eq:gpp`, `eq:spinodal` | `eq:sm-mu-rs`, `eq:sm-gxi`, `eq:sm-gpp`, `eq:sm-spinodal` | 기존 `sec:hys`는 평균장 기초 재유도 대신 spinodal gap 계산으로 바로 들어가도록 재조직 가능하다. |
| Ch1 647-709 `eq:Veq`, `eq:dUhys`, `eq:Ubranch` | `eq:sm-Veq`, `eq:sm-spinodal` | Part 0은 `V_eq(\xi)`와 spinodal 위치까지만 공급한다. gap 닫힌꼴과 방향별 분기 중심은 기존 `sec:hys` 본문에 남긴다. |
| Ch1 918-951 `w_j` 이중지위 | `eq:sm-xieq`와 자체검수 `\Omega` 항목 | Part 0은 `w_j=n_jRT/F`의 이상 기원을 설명하고, 두-상 폭은 평형 예측이 아니라 모델 선택/피팅 폭이라는 경고를 기존 절에 재접속한다. |
| Ch1 953-993 detailed balance logistic | 자체검수 detailed balance, `eq:sm-xieq` | kinetic 정지점 유도는 Part 0 뒤에서 "같은 logistic 의 동역학적 회수"로 짧게 참조 가능하다. |
| Ch1 1066-1112 `sec:dist` | `eq:sm-Z1`부터 `eq:sm-xiV-id`까지 | 분포 관점은 Part 0으로 이동한다. 단, Ch1 1088-1098의 `theta/xi` 부호 긴장은 위 자체검수의 정정 제안을 적용해야 한다. |

## 5줄 요약

1. Part 0은 grand-canonical 단일 자리 분배함수에서 `theta` logistic 을 먼저 얻고, `xi=1-theta`로 Ch1 `eq:xieq`를 재유도한다.
2. `V↑ => theta↓, xi↑` 부호는 Ch1 `eq:eqcond`와 Ch2 `eq:logistic`을 기준으로 고정했다.
3. `M` 독립 자리의 ideal lattice gas에서 mixing entropy와 Nernst 로그항이 나오고, 평균장 `\Omega`를 더하면 regular solution 및 `\Omega=2RT` spinodal 문턱이 나온다.
4. 거시 열역학은 `G=H-TS`, `\mu=(\partial G/\partial n)_{T,P}`, `\Delta G_j=-sFU_j`, `U_j=(-\Delta H_{\rxn}+T\Delta S_{\rxn})/F`로 닫았다.
5. 최약점: Ch1 1088-1098의 `theta/xi` 서술은 현 상태로는 부호 긴장이 있어, 편입 전 해당 문단 정정이 필요하다.

## 갈래 2

### 갈래 2 원천 읽기 기록

| 항목 | 실제 확인 범위 | 지위 |
|---|---:|---|
| 작업 지시문 `v1013_p21_base.txt` | 1-27행 | 전문 정독 완료 |
| `graphite_ica_ch1_v1.0.13.tex` `sec:lco-map` | 301-355행 | 지정 범위 전문 정독 완료 |
| `graphite_ica_ch1_v1.0.13.tex` `sec:lco-hys`의 `★분기 부호의 전극-중립 읽기(한정)` 문단 | 846-854행 | 지정 문단 전문 정독 완료 |
| `graphite_ica_ch1_v1.0.13.tex` `sec:lco-peak`의 `★방향 부호의 전극-중립 읽기(적용 한정)` 문단 | 1426-1437행 | 지정 문단 전문 정독 완료 |
| `graphite_ica_ch1_v1.0.13.tex` N0/N1/MSMR 보조 문맥 | 198-208, 357-374, 2073-2127행 | 부분 확인: 방향 작용처 식과 `f=+\sigma_d` 대응 확인 |
| `V1012_P43_verify10.md` | 42-85, 102-115, 124-132행 중심 | 부분 확인: `f=+\sigma_d` 확정 판정만 확인, 재론 없음 |

### Part II LCO 도입 절 LaTeX 문안

```latex
% ====================================================================
\section{Part II. LCO 양극: 전극-중립 골격과 방향 슬롯}\label{sec:lco-partII-intro}
% ====================================================================
이 절의 목적은 앞 절들에 흩어진 LCO 도입, 분기 부호, peak 방향 부호를 하나의 규약으로 먼저 닫는 것이다.
닫아야 할 것은 전극 종류가 아니라 \emph{진행률의 물리 방향}이다. 이후 LCO 절은 흑연 식을 다시 쓰지 않고,
전극-중립 골격에 LCO 파라미터와 MIT 전자항을 건다.

\subsection{전극-중립 골격: 같은 식, 다른 전극 파라미터}

\textbf{(a) 출발.}
삽입형 하프셀에서 공통인 것은 네 가지다: 방향 환산, 전이 인덱스 $j$, 탈리튬화 진행률 $\xi_j$,
평형 중심 $U_j$ 이다. 따라서 LCO 하프셀도
\begin{equation}
j\in\{1,2,3\},\qquad
\theta_j=1-\xi_j,\qquad
U_j\mapsto U_j^{\mathrm{cat}},\qquad
Q_j\mapsto Q_j^{\mathrm{cat}}
\label{eq:lco-intro-skeleton}
\end{equation}
로 같은 골격에 들어간다. 흑연 식의 기호 구조는 보존하고, LCO 전이표의 수치와 MIT 전자 엔트로피 항만
양극 고유 입력으로 붙인다.

\textbf{(b) 연산.}
코인 하프셀 LCO vs Li metal 에서 셀 동작 라벨과 화학 진행 방향은 다음처럼 갈라진다.
\begin{equation}
\begin{array}{c|c|c|c}
\text{cell label} & \text{LCO chemistry} & V\ \text{trend} & \xi_j\ \text{trend}\\
\hline
\text{charge} & \text{delithiation/oxidation} & \uparrow & 0\to1\\
\text{discharge} & \text{lithiation/reduction} & \downarrow & 1\to0
\end{array}
\label{eq:lco-intro-label}
\end{equation}
식~\eqref{eq:n0map} 의 셀 라벨 의미론은 여기까지다. 방향 의존 식에 넣는 모델 슬롯은 이후
\begin{equation}
\boxed{\;
\sigma_d=+1\ \Longleftrightarrow\ \text{delithiation/oxidation},\qquad
\sigma_d=-1\ \Longleftrightarrow\ \text{lithiation/reduction}.
\;}
\label{eq:lco-intro-slot}
\end{equation}
로 읽는다. 그러므로 LCO 데이터 적용에서는 충전 곡선이 $\sigma_d=+1$ 슬롯, 방전 곡선이
$\sigma_d=-1$ 슬롯이다. 이것은 \S\ref{sec:lco-map} 의 ``방전 라벨은 LCO 에서 리튬화''라는 문장과
모순되지 않는다. 그 문장은 셀 라벨의 의미이고, 식~\eqref{eq:lco-intro-slot} 은 방향 의존 모델 슬롯의 입력
규칙이다.

\textbf{(c) 중간식.}
평형 종 자체는 이 슬롯 선택에 불변이다. 같은 중심과 폭에서
\begin{equation}
\xi_{\eq,j}^{(\sigma_d)}(V)
=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j^{\mathrm{cat}}]},
\label{eq:lco-intro-xi}
\end{equation}
이므로
\begin{equation}
\xi_{\eq,j}^{(-\sigma_d)}(V)=1-\xi_{\eq,j}^{(\sigma_d)}(V),\qquad
\xi_{\eq,j}^{(-\sigma_d)}(1-\xi_{\eq,j}^{(-\sigma_d)})
=\xi_{\eq,j}^{(\sigma_d)}(1-\xi_{\eq,j}^{(\sigma_d)}).
\label{eq:lco-intro-complement}
\end{equation}
따라서 peak magnitude 는
\begin{equation}
\left|\frac{\dd\xi_{\eq,j}^{(\sigma_d)}}{\dd V}\right|
=\frac{\xi_{\eq,j}^{(\sigma_d)}(1-\xi_{\eq,j}^{(\sigma_d)})}{w_j^{\mathrm{cat}}}
\label{eq:lco-intro-peakinv}
\end{equation}
로 여집합 교환에 불변이다. 방향 읽기가 바꾸는 것은 평형 종의 모양이 아니라 방향 의존 작용처다.

\textbf{(d) 박스.}
\begin{equation}
\boxed{\;
\text{LCO 의 충전 라벨은 탈리튬화이므로, 방향 의존 슬롯에서는 }\sigma_d=+1\text{ 로 넣는다.}
\;}
\label{eq:lco-intro-mainbox}
\end{equation}

\subsection{방향 의존 세 작용처}

\textbf{(a) 출발.}
방향 부호가 실제로 들어가는 곳은 세 군데뿐이다. 평형 logistic 의 여집합 표기는 그 자체로 관측 peak 모양을
바꾸지 않는다.

\textbf{(b) 연산.}
첫째, 분극은 내부 전위 환산이다.
\begin{equation}
V_n=V_\app-\sigma_d |I|R_n.
\label{eq:lco-intro-pol}
\end{equation}
LCO 충전은 산화/탈리튬화 진행이므로 $\sigma_d=+1$ 슬롯에서 $V_\app>V_n$ 으로 읽는다.
둘째, 히스테리시스 분기 중심은
\begin{equation}
U_j^{\,d,\mathrm{cat}}
=U_j^{\mathrm{cat}}
+\frac12\sigma_d h_{\eta,j}\gamma_j\Delta U_j^{\hys,\mathrm{cat}}(T).
\label{eq:lco-intro-branch}
\end{equation}
여기서 $+\tfrac12$ 가지는 전극 불문 탈리튬화 가지다. LCO 에서도 탈리튬화 봉우리가 높은 전위 쪽이라는
읽기가 유지된다. 셋째, 꼬리는 진행 방향의 인과 순서다.
\begin{equation}
p_j(V)=\frac{\xi_{\eq,j}(V)-\xi_{\mathrm{lag},j}(V)}{L_{V,j}},
\label{eq:lco-intro-tail}
\end{equation}
이며 충전/탈리튬화 슬롯은 전위 오름차순, 방전/리튬화 슬롯은 전위 내림차순의 기억을 쓴다.

\textbf{(c) 중간식.}
따라서 방향 규약은 다음 한 줄로 닫힌다.
\begin{equation}
\boxed{\;
\sigma_d\ \text{acts on N1 polarization, N3 branch, and N8 causal tail; }
\xi_{\eq}\leftrightarrow1-\xi_{\eq}\ \text{does not change the peak magnitude.}
\;}
\label{eq:lco-intro-three-slots}
\end{equation}

\subsection{MSMR 예고: 같은 물리량끼리 맞대기}

\textbf{(a) 출발.}
MSMR 의 종별 변수는 리튬화 분율이다. LCO 문맥에서는
\begin{equation}
\theta_j^{\mathrm{MSMR}}\equiv\frac{x_j}{X_j}
=\frac{1}{1+\exp[+f(U-U_j^0)/\omega_j]},\qquad
\xi_j^{\mathrm{MSMR}}\equiv1-\theta_j^{\mathrm{MSMR}}
=\frac{1}{1+\exp[-f(U-U_j^0)/\omega_j]}.
\label{eq:lco-intro-msmr}
\end{equation}

\textbf{(b) 연산.}
점유는 점유와, 진행률은 진행률과 맞댄다. 그러면
\begin{equation}
U\leftrightarrow V,\qquad
U_j^0\leftrightarrow U_j^{\,d,\mathrm{cat}},\qquad
\omega_j\leftrightarrow w_j^{\mathrm{cat}},\qquad
X_j\leftrightarrow Q_j,\qquad
f=+\sigma_d.
\label{eq:lco-intro-msmrmap}
\end{equation}
이 대응은 v1.0.12 verify10 에서 확정된 판정이며 여기서 재론하지 않는다. $f=-\sigma_d$ 는 점유와
탈리튬화 진행률을 직접 등치하는 여집합 뒤바꿈이다.

\textbf{(c) 박스.}
\begin{equation}
\boxed{\;
Q_j\left|\frac{\dd\theta_j^{\mathrm{MSMR}}}{\dd U}\right|
=Q_j\frac{\theta_j^{\mathrm{MSMR}}(1-\theta_j^{\mathrm{MSMR}})}{\omega_j}
\equiv
Q_j\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j^{\mathrm{cat}}}.
\;}
\label{eq:lco-intro-msmrpeak}
\end{equation}
따라서 MSMR 은 새 peak 물리를 더하는 것이 아니라, 같은 용량-가중 logistic 종을 LCO 문헌의 점유 변수에서
Chapter 1 의 탈리튬화 진행률 변수로 옮기는 사전이다.
```

### 갈래 2 자체검수 기록

| 검수 항목 | 결과 |
|---|---|
| 전극-중립 골격 | `sec:lco-map` 301-355행의 골격을 유지했다. 전이 인덱스, `xi_j`, `U_j`, `Q_j`는 공통 슬롯이고, LCO 고유성은 전이표 값과 T1 MIT 전자항으로만 분리했다. |
| 라벨/슬롯 분리 | `eq:n0map` 198-206행의 셀 라벨 의미론과 `sec:lco-peak` 1426-1437행의 모델 입력 슬롯을 분리했다. LCO 충전은 탈리튬화라 `sigma_d=+1` 슬롯으로 넣는다. |
| 평형 종 불변 | `xi_{-sigma}=1-xi_sigma`, `xi(1-xi)` 불변, `|dxi/dV|=xi(1-xi)/w`를 명시했다. peak magnitude는 방향 선택으로 바뀌지 않는다. |
| 3작용처 | 분극 `V_n=V_app-sigma_d|I|R_n`, 분기 `U_j^d=U_j+0.5 sigma_d h_eta gamma Delta U_hys`, 꼬리 `(xi_eq-xi_lag)/L_V`만 방향 의존으로 제한했다. |
| MSMR 대응 | `V1012_P43_verify10.md`의 확정 판정대로 `f=+sigma_d`만 예고했다. 재론하지 않았고, `f=-sigma_d`는 여집합 뒤바꿈이라고만 위치시켰다. |
| 수치 날조 방지 | LCO `Omega_j^cat` 값은 새로 배정하지 않았다. 분기식은 기존처럼 `Omega/gamma/h_eta`가 있을 때의 조건부 슬롯으로만 남겼다. |
| 최약점 | 기존 본문은 `sigma_d`를 셀 라벨과 모델 슬롯에 모두 쓰므로, 편입 단계에서는 `sigma_d` 단일 기호 유지 + 각주, 또는 `sigma_label/sigma_slot` 분리 중 하나를 선택해야 한다. |

## figure

| 그림 | 목적 | 형식 | 배치 | 캡션 | 산출 |
|---|---|---|---|---|---|
| LCO direction slot logistic | LCO 충전이 `sigma=+1` 탈리튬화 슬롯이고 방전이 `sigma=-1` 리튬화 슬롯임을, 같은 logistic 식 평가로 보인다. `xi_{-}=1-xi_{+}` 이지만 `xi(1-xi)/w` peak magnitude는 동일하다는 점을 그림으로 확인한다. | matplotlib 스크립트 + PNG. 모든 figure label은 영어/ASCII만 사용. | `Part II. LCO 양극` 도입 절의 방향 슬롯 박스 직후 또는 MSMR 예고 직전. | `Direction-slot logistic for an LCO half-cell. The two traces are complements in the progress variable, while the peak magnitude xi(1-xi)/w is invariant; therefore direction affects polarization, branch, and tail slots, not the equilibrium peak magnitude.` | 스크립트: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_C2_lco_direction_slots.py`; PNG: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_C2_lco_direction_slots.png` |

### figure 생성 검증

```text
python Claude\results\process\V1013_P21_fig_C2_lco_direction_slots.py
wrote D:\Projects\Project_Anode_Fit\Claude\results\process\V1013_P21_fig_C2_lco_direction_slots.png
complement_error=1.613e-16
peak_error=4.496e-15
```

수식 평가:
\[
\xi_\sigma(V)=\frac{1}{1+\exp[-\sigma(V-U)/w]},\qquad
\mathrm{peak}_\sigma(V)=\frac{\xi_\sigma(1-\xi_\sigma)}{w}.
\]
그림은 `U=4.00 V`, `w=0.035 V`의 임의 시각화 파라미터로 식을 평가한 것이며, LCO 전이 수치를 새로 배정하지 않는다.

## 5줄 요약(갈래 2 + figure)

1. 갈래 2는 LCO Part II 도입을 `전극-중립 골격 → 셀 라벨/모델 슬롯 분리 → 평형 여집합 불변 → 방향 의존 3작용처 → MSMR 예고` 순서로 일원화했다.
2. 물리 자체검수 핵심은 LCO 충전이 탈리튬화/산화이므로 방향 의존 모델 슬롯에서 `sigma_d=+1`, LCO 방전은 리튬화/환원이므로 `sigma_d=-1`이라는 점이다.
3. 평형 logistic은 `xi_{-sigma}=1-xi_sigma`라 peak magnitude `xi(1-xi)/w`가 불변이고, 방향 부호는 분극·분기·꼬리에만 작용하도록 제한했다.
4. figure는 실제 logistic 식을 평가해 여집합 오차 `1.613e-16`, peak 오차 `4.496e-15`를 확인했으며, LCO `Omega_j^cat`나 새 전이 수치를 날조하지 않았다.
5. 최약점: 현재 원문은 `sigma_d`가 셀 라벨과 모델 슬롯을 겸하므로, 최종 편입 때는 단일 기호+명시 각주 또는 label/slot 기호 분리 중 하나를 선택해야 한다.
