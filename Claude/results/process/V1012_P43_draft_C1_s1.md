# V1012 Phase 4.3 draft C1 — step 1/3 only (center/hys)

> 대상 원천: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`
> 대상 절: `sec:lco-center`(L476--519) 및 `sec:lco-hys`(L696--719)
> 출발점: `Claude/results/process/V1011_P11_map_v10.md`
> 산출물 성격: finalizer 편입용 supplement 초안. `.tex`/코드 수정 없음.

## 0. 확인 범위와 계승 판단

- `graphite_ica_ch1_v1.0.12.tex`는 1--1964행을 구간 분할로 확인했다. 도구 출력 생략이 의심된 구간은 241--320, 901--1240, 1611--1795를 좁혀 재확인했다.
- `V1011_P11_map_v10.md`는 1--319행 전체를 확인했다.
- 현 v1.0.12 위치는 v1.0.11 map의 위치보다 밀렸다: `sec:lco-center`는 L476, `sec:lco-hys`는 L696.
- `V1011_P11_map_v10.md`의 큰 골격, 즉 `center`의 (a)--(d) 사슬과 `hys`의 정규용액 대입 사슬은 계승한다.
- 개선: v1.0.11 map의 LCO용 Omega 상첨자 표기는 이번 지시의 `\Omega_j` 기호 유지와 현 tex 기호표(L241, L524 이하)에 맞지 않으므로 쓰지 않는다. LCO에서도 상호작용 에너지는 그대로 `\Omega_j`로 둔다.
- 불가침: `sec:lco-map`, `sec:lco-Se`, `sec:lco-gate`, 전자엔트로피 본유도, 코드, 수치값은 수정 제안하지 않는다.

## 1. `sec:lco-center` supplement

### 위치

- 헤더 보존: L476 `\subsection{LCO 평형 중심과 $\partial U_j/\partial T$ — 양극 부호}\label{sec:lco-center}`
- 교체 후보: L477--494의 줄글 및 단일 식 블록
- 보존: L496--516 `verifybox`, L518--519 다음 절 연결 문장
- 필수 라벨: `\label{eq:lco-dUdT}` 재사용. 현 파일에서 후속 참조가 L493, L498, L1229, L1750, L1790, L1877에 있으므로 라벨 삭제/변경 금지.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — 흑연 forward 식의 전극-중립 자리.}
\S\ref{sec:center} 의 중심 유도에서 물질 고유 정보가 들어가는 자리는 전이별
입력값뿐이다. 식~\eqref{eq:n0map} 의 방향 부호와 전류 환산은 삽입형 전극의
실험조건 매핑이고, 식~\eqref{eq:eqcond} 의
$\Delta G_j=-sF U_j$ 는 삽입 반쪽반응의 전기화학 평형에서 온다. 따라서 LCO 로
넘어갈 때 바꾸는 것은 전이 집합과 반응 열역학 입력값이다:
\begin{equation}
j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j})
\longmapsto
(\Delta H_{\rxn,j}^{\mathrm{cat}},\Delta S_{\rxn,j}^{\mathrm{cat}}).
\label{eq:lco-n0sub}
\end{equation}
여기서 $\sigma_d$ 는 방향 선택 슬롯에 남고, 평형 중심의 Gibbs 환산식에는
새 양극 부호가 끼지 않는다.

\textbf{(b) 연산 — 반응 자유에너지를 평형 조건에 대입.}
LCO 전이 $j$ 의 비배치 반응 자유에너지를
\[
\Delta G_j^{\mathrm{cat}}
=\Delta H_{\rxn,j}^{\mathrm{cat}}
-T\Delta S_{\rxn,j}^{\mathrm{cat}}
\]
로 두고, 식~\eqref{eq:eqcond} 의 $\Delta G_j=-sF U_j$ 에 $s=+1$ 을
대입하면
\begin{equation}
\Delta H_{\rxn,j}^{\mathrm{cat}}
-T\Delta S_{\rxn,j}^{\mathrm{cat}}
=-F\,U_j(T).
\label{eq:lco-Ujmid}
\end{equation}
흑연 식~\eqref{eq:Ujmid} 과 같은 연산이며, 상첨자 `cat'은 입력값의 출처만
표시한다.

\textbf{(c) 중간식 — 중심과 온도 미분의 이중 확인.}
식~\eqref{eq:lco-Ujmid} 를 $U_j$ 로 풀면
\[
U_j(T)=
\frac{-\Delta H_{\rxn,j}^{\mathrm{cat}}
+T\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}.
\]
직접 미분하면
\[
\frac{\partial U_j}{\partial T}
=\frac{\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}.
\]
같은 결과는 Gibbs 항등식으로도 닫힌다:
\[
\frac{\partial\Delta G_j}{\partial T}\Big|_P
=-\Delta S_{\rxn,j}^{\mathrm{cat}},\qquad
\Delta G_j=-F U_j
\]
이므로
\[
-F\,\frac{\partial U_j}{\partial T}
=-\Delta S_{\rxn,j}^{\mathrm{cat}}
\quad\Longrightarrow\quad
\frac{\partial U_j}{\partial T}
=\frac{\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}.
\]
두 경로 모두 host 구분 항 없이 같은 부호에 도달한다.

\textbf{(d) 박스 — LCO 중심과 온도 계수.}
\begin{equation}
\boxed{\;
U_j(T)=
\frac{-\Delta H_{\rxn,j}^{\mathrm{cat}}
+T\Delta S_{\rxn,j}^{\mathrm{cat}}}{F},
\qquad
\frac{\partial U_j}{\partial T}
=\frac{\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}
\quad(j\in\mathcal J_\mathrm{LCO})\;}
\label{eq:lco-dUdT}
\end{equation}
관계식은 흑연 식~\eqref{eq:Uj} 와 부호까지 1:1 이며, 바뀌는 것은
입력값뿐이다. 양극 중심이 $\sim$3.9--4.2 V 에 놓이는 것은
$-\Delta H_{\rxn,j}^{\mathrm{cat}}$ 가 크게 양인 입력값의 결과다.
LCO 의 $\Delta S_{\rxn,j}^{\mathrm{cat}}$ 는
\S\ref{sec:lco-decomp} 에서 config$\cdot$vib$\cdot$electronic 세 성분으로
분해된다. 대표 단전극 계수 $\dd\phi/\dd T\approx+0.83$ mV/K 는
$F\times0.83\times10^{-3}\approx+80$ J/(mol\,K) 의 전체 단전극
스케일[tier B]로만 읽고, 표~\ref{tab:lco-staging} 의 전이별 성분값과
직접 등치하지 않는다.
```

### 원문 대비

- 원문 L477--481의 "같은 식, 다른 입력" 결론을 유지하되, 흑연 forward 사슬의 어느 자리가 전극-중립인지 (a)에 명시했다.
- 원문 L483--488의 단일 미분식을 (b)--(d) 유도 사슬로 확장했다.
- `eq:lco-dUdT` 라벨은 기존 후속 참조를 위해 (d) 박스에 그대로 둔다.
- 원문 L489--494의 대표 스케일 문장은 박스 뒤 prose로 보존하되, `+80`은 전체 단전극 스케일이고 전이별 config/vib/electronic 성분과 직접 비교하지 않는다는 층위 분리를 분명히 했다.
- v1.0.11 map의 다온도 전자항 적분 가드는 이번 `center` 교체 블록에는 넣지 않았다. 현 v1.0.12의 `sec:lco-Se`/`sec:lco-gate` 쪽에 이미 별도 유도와 `T^2` 식이 있으므로, step 1 범위에서 새 설명을 중복 주입하지 않는 편이 불가침 조건에 더 맞다.

### 논리 감사

- 부호: `\Delta G=-FU_j`와 `\Delta G=\Delta H-T\Delta S`에서 `U_j=(-\Delta H+T\Delta S)/F`; 발열 `\Delta H<0`이면 중심 상승. 원문과 동일하다.
- 차원: `\Delta H`는 J/mol, `T\Delta S`도 J/mol, `F`는 C/mol이므로 `U_j`는 J/C = V. `\partial U/\partial T=\Delta S/F`는 J/(mol K) / C/mol = V/K.
- 극한: `\Delta S=0`이면 온도 계수 0. `\Delta H,\Delta S`를 흑연 입력으로 되돌리면 식~\eqref{eq:Uj}로 환원.
- 수치: `+0.83` mV/K 및 `+80` J/(mol K)는 원문 sanity scale 그대로 유지. 새 정밀값 없음.
- 불가침: verifybox, `sec:lco-decomp`, `sec:lco-Se`, `sec:lco-gate`의 내용은 건드리지 않는다.

## 2. `sec:lco-hys` supplement

### 위치

- 헤더 보존: L696 `\subsection{LCO order--disorder 와 MIT 2상역 — 같은 정규용액 틀}\label{sec:lco-hys}`
- 교체 후보: L697--719의 네 문단
- 다음 경계 보존: L722 `\section{폭과 평형 점유 ...}\label{sec:width}`
- 핵심 보존: 흑연 `sec:hys`의 식~\eqref{eq:mu}, \eqref{eq:gxi}, \eqref{eq:gpp}, \eqref{eq:spinodal}, \eqref{eq:Veq}, \eqref{eq:dUhys}, \eqref{eq:Ubranch}를 새 물리 없이 LCO 전이 집합에 대입한다.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — LCO 세 전이를 같은 정규용액 자유에너지에 대입.}
\S\ref{sec:hys} 의 격자기체$\cdot$정규용액 틀은 ``동등한 자리에
리튬이 차고 빈다''는 가정만 쓴다. LCO 의 리튬 층 자리도 한 자리의
점유가 0 또는 1 이므로, 표~\ref{tab:lco-staging} 의 세 전이를
\[
\mathcal J_\mathrm{LCO}=\{\mathrm{T1(MIT)},\mathrm{T2(OD)},\mathrm{T3(OD)}\}
\]
로 두고 같은 조성 몫을 쓴다:
\begin{equation}
g_j^{\mathrm{LCO}}(\xi)
=g_{0,j}^{\mathrm{LCO}}
+RT\big[\xi\ln\xi+(1-\xi)\ln(1-\xi)\big]
+\Omega_j\,\xi(1-\xi),
\qquad j\in\mathcal J_\mathrm{LCO}.
\label{eq:lco-gxi}
\end{equation}
새 상호작용 기호를 만들지 않는다. LCO 로 바뀌는 것은 $U_j$ 의 값,
$\Omega_j$ 의 전이별 입력값, 그리고 $\gamma_j,h_{\eta,j}$ 의 피팅값이다.

\textbf{(b) 연산 — 곡률과 spinodal 문턱.}
식~\eqref{eq:lco-gxi} 를 두 번 미분하면 흑연 식~\eqref{eq:gpp} 와 같은
곡률식에 도달한다:
\begin{equation}
\frac{\partial^2 g_j^{\mathrm{LCO}}}{\partial\xi^2}
=\frac{RT}{\xi(1-\xi)}-2\Omega_j.
\label{eq:lco-gpp}
\end{equation}
따라서 spinodal 은
\begin{equation}
\xi_{s,j}^{\pm}=\tfrac12(1\pm u_j),\qquad
u_j=\sqrt{1-\frac{2RT}{\Omega_j}},
\qquad(\Omega_j>2RT),
\label{eq:lco-spinodal}
\end{equation}
이고, $\Omega_j\le2RT$ 로 피팅되는 전이는 이 사슬 안에서 gap 이 0 으로 닫힌다.

\textbf{(c) 중간식 — 전위 곡선에 spinodal 대입.}
식~\eqref{eq:Veq} 의 전위 곡선을 LCO 전이 $j$ 에 그대로 쓰면
\begin{equation}
V_{\eq,j}^{\mathrm{LCO}}(\xi)
=U_j+\frac{RT}{F}\ln\frac{\xi}{1-\xi}
+\frac{\Omega_j}{F}(1-2\xi)
\label{eq:lco-Veq}
\end{equation}
이다($s=+1$ 정리형). 식~\eqref{eq:lco-spinodal} 을 대입하면
\[
\frac{\xi}{1-\xi}\bigg|_{\xi_{s,j}^{\pm}}
=\frac{1\pm u_j}{1\mp u_j},\qquad
(1-2\xi)\big|_{\xi_{s,j}^{\pm}}=\mp u_j,
\]
이므로 극대와 극소의 차에서 상수 중심 $U_j$ 는 상쇄되고
\[
\Delta U_j^\hys
=V_{\eq,j}^{\mathrm{LCO}}(\xi_{s,j}^-)
-V_{\eq,j}^{\mathrm{LCO}}(\xi_{s,j}^+)
=\frac{2}{F}\Big[\Omega_j u_j-2RT\,\mathrm{artanh}\,u_j\Big].
\]

\textbf{(d) 박스 — LCO 전이별 gap 과 방향별 중심.}
\begin{equation}
\boxed{\;
\Delta U_j^\hys(T)=
\begin{cases}
\dfrac{2}{F}\Big[\Omega_j u_j-2RT\,\mathrm{artanh}\,u_j\Big],
& \Omega_j>2RT,\\[4pt]
0, & \Omega_j\le2RT,
\end{cases}
\qquad
u_j=\sqrt{1-\dfrac{2RT}{\Omega_j}}\;}
\label{eq:lco-dUhys}
\end{equation}
\begin{equation}
\boxed{\;
U_j^{\,d}
=U_j+\tfrac12\sigma_d h_{\eta,j}\gamma_j\,\Delta U_j^\hys(T)\;}
\label{eq:lco-Ubranch}
\end{equation}
이는 흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 전이별
대입형이다. 방전($\sigma_d=+1$)은 분기 중심을 위로, 충전
($\sigma_d=-1$)은 아래로 옮긴다. $\gamma_j\to0$ 이면 분기가 사라지고,
$\Omega_j\to2RT^+$ 이면 $u_j\to0$ 이라
$\Delta U_j^\hys\to(8RT/3F)u_j^3\to0$ 으로 연속 소멸한다.

\textbf{(T2$\cdot$T3) order--disorder.}
$x\approx0.5$ 부근의 monoclinic 초격자 질서화는 위 정규용액
$\Omega_j>0$ 이 만드는 상분리의 LCO 사례다. T2($\sim$4.05 V,
hex$\to$monoclinic)와 T3($\sim$4.17--4.20 V, monoclinic$\to$hex)는
각각 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 를 받는다.
정렬의 charge-order 엔트로피 변화($\approx0.47$ J/(mol K)@$x=\tfrac12$,
$\approx1.49$ J/(mol K)@$x=\tfrac23$ [tier A, Motohashi\cite{motohashi2009}])
는 표~\ref{tab:lco-staging} 의 config $\Delta S$ 슬롯에 들어가는
엔트로피 초기값이지, spinodal 문턱을 정하는 상호작용 에너지
$\Omega_j$가 아니다. 따라서 $0.47/1.49$를 $\Omega_j$로 환산하지 않는다.

\textbf{(T1) MIT 2상역.}
T1($\sim$3.90 V, $x\approx0.94$--$0.75$)의 절연체$\to$금속 2상 공존도
같은 spinodal gap 과 분기 중심을 받는다. 다만 MIT 의 전자 자유도는
gap 식에 새 항으로 섞지 않는다. 전자항은
\[
\Delta S_{\rxn,1}^{\mathrm{cat}}
=\Delta S_1^{\mathrm{config}}
+\Delta S_1^{\mathrm{vib}}
+\Delta S_{e,1}^{\,\mathrm{mol}}(x,T)
\]
를 통해 식~\eqref{eq:lco-dUdT} 의 온도 계수 슬롯에 들어간다. 곧
구조적 2상역은 $\Omega_j\to\Delta U_j^\hys\to U_j^{\,d}$ 사슬,
전자 자유도는 $\Delta S_e\to\partial U_j/\partial T$ 사슬에 놓는다.
이 분리가 이중계산 방지의 경계다.

\textbf{도핑 보정(우리 시료).}
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox 와 전자항을 보존하되
order--disorder$\cdot$MIT 상전이를 억제한다. 정규용액 틀에서는 pure-LCO
초기값으로 둔 $\Omega_j$ 가 피팅에서 $2RT$ 쪽으로 낮아지는 입력 변화로
읽는다. 피팅된 $\Omega_j\le2RT$ 인 전이는 식~\eqref{eq:lco-dUhys} 의
둘째 줄로 가서 gap 이 0 이 되고, $\Omega_j\to2RT^+$ 에서는 위 Taylor
극한으로 히스가 연속적으로 줄어든다. 중심 전위의 미세 shift 는 같은
전이 dict 의 $U_j$ 피팅값 이동으로 따로 들어가며, $\Omega_j$ 하나가
gap 과 중심 이동을 동시에 만든다고 쓰지 않는다.
```

### 원문 대비

- 원문 L697--699의 "같은 정규용액 틀, 값만 LCO"를 (a)--(d) 수식 사슬로 전개했다.
- 원문 L701--706의 T2/T3 설명은 유지하되, `config \Delta S`와 `\Omega_j`의 차원을 분리했다. `0.47/1.49` J/(mol K)는 엔트로피 값이고 `\Omega_j`는 J/mol 상호작용 에너지다.
- 원문 L708--713의 MIT 분리 문장은 슬롯 사슬로 명시했다: 구조적 2상역은 `\Omega_j` 경로, 전자항은 `\Delta S_e` 경로.
- 원문 L715--719의 도핑 보정은 `\Omega_j\to2RT^+` 극한과 `\Omega_j\le2RT` case를 보강했다.
- v1.0.11 map의 LCO용 Omega 상첨자 변형들은 쓰지 않는다. 현 v1.0.12 원문과 지시대로 `\Omega_j`를 유지한다.

### 논리 감사

- 부호: `\Delta U_j^\hys`는 극대-극소 차로 정의되어 nonnegative. `U_j^{\,d}=U_j+\tfrac12\sigma_d h_{\eta,j}\gamma_j\Delta U_j^\hys` 이므로 방전은 위, 충전은 아래로 이동한다. 흑연 식과 동일하다.
- 차원: `\Omega_j u_j`와 `RT\,\mathrm{artanh}\,u_j`는 J/mol, `2/F`를 곱하면 V. `U_j^{\,d}`의 세 항은 모두 V.
- 극한: `\Omega_j\le2RT`이면 실수 spinodal 없음 -> gap 0. `\Omega_j\to2RT^+`이면 `u_j\to0`, `\mathrm{artanh}u_j=u_j+u_j^3/3+\cdots`로 gap이 `\propto u_j^3`로 소멸. `\gamma_j\to0` 또는 `h_{\eta,j}\to0`이면 분기 중심은 `U_j`.
- 수치: T2/T3 전위, `0.47/1.49` J/(mol K), T1 조성 범위, `2RT\approx4958` J/mol@298 K 같은 기존 숫자는 새로 만들지 않고 원문/기존 절의 값만 유지했다. `\Omega_j` 수치값은 날조하지 않았다.
- 불가침: `sec:lco-map`, `sec:lco-Se`, `sec:lco-gate`, `sec:lco-decomp`는 참조만 하고 수정 대상으로 삼지 않는다.

## 3. 라벨 및 삽입 주의

- `eq:lco-dUdT`는 재사용 필수다.
- 신설 후보는 `eq:lco-n0sub`, `eq:lco-Ujmid`, `eq:lco-gxi`, `eq:lco-gpp`, `eq:lco-spinodal`, `eq:lco-Veq`, `eq:lco-dUhys`, `eq:lco-Ubranch`다.
- 현 tex의 기존 `eq:lco-*` 라벨은 `eq:lco-dUdT`, `eq:lco-decomp`만 확인됐다. 단, 실제 편입 전 finalizer가 한 번 더 `rg "\\label\\{eq:lco-"`로 충돌 확인해야 한다.
- `\Omega_j`는 상첨자 없이 유지한다. LCO 구분은 절 위치, `j\in\mathcal J_\mathrm{LCO}`, 또는 prose로 처리한다.

## 4. 3줄 요약

1. `center`는 흑연 `U_j=(-\Delta H+T\Delta S)/F`를 LCO 입력값으로 대입하고, 직접 미분과 Gibbs 항등식으로 `\partial U_j/\partial T=\Delta S_{\rxn,j}^{\mathrm{cat}}/F`를 재확인했다.
2. `hys`는 흑연 정규용액 spinodal 사슬을 LCO T1/T2/T3에 대입하되, `\Omega_j` 기호를 유지하고 `config \Delta S`와 `\Omega_j`를 분리했다.
3. `.tex`/코드 수정 없이 이 파일만 작성했으며, `sec:lco-map`, `sec:lco-Se`, `sec:lco-gate`, 전자엔트로피 본유도는 불가침으로 남겼다.
