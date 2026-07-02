# V1012 Phase 4.3 Draft C3 — Step 1/3 supplement (center·hys only)

> 대상: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`
> 범위: `sec:lco-center`(L476--519) · `sec:lco-hys`(L696--719)
> 출력 성격: `.tex` 편입 전 supplement. **`.tex`/코드 수정 없음.**
> 출발점: `Claude/results/process/V1011_P11_map_v10.md` 계승. 단, v1.0.12 원문 줄번호·라벨·절 경계를 재확인해 재유도 검증 후 작성.

## 0. 확인 범위와 불가침

- 직접 확인한 v1.0.12 원문 범위:
  - `sec:center` 유도 및 `sec:lco-center`: L411--521.
  - `sec:hys` 유도 및 `sec:lco-hys`: L522--721.
  - 기존 초안 `V1011_P11_map_v10.md`: L1--319 전체.
- 라벨 실측:
  - 기존 `eq:lco-*` 라벨은 `eq:lco-dUdT`(L487), `eq:lco-decomp`(L1723) 두 개뿐.
  - `eq:lco-dUdT`는 정의 L487 외에 L493, L498, L1229, L1750, L1790, L1877에서 참조되므로 재사용 필수.
  - 신설 후보 `eq:lco-n0sub`, `eq:lco-J`, `eq:lco-gxi`, `eq:lco-gpp`, `eq:lco-spinodal`, `eq:lco-Veq`, `eq:lco-dUhys`, `eq:lco-Ubranch`, `eq:lco-mit`, `eq:lco-dope`는 v1.0.12에서 충돌 없음.
- 불가침:
  - `sec:lco-map`, `sec:lco-Se`, `sec:lco-gate`, `sec:lco-decomp`, verifybox 본문, 코드 본문은 수정 대상 아님.
  - 물리·결과식·부호·수치 불변. `\Omega_j` 계열은 기호로 유지하고 새 수치값을 만들지 않음.

---

## 1. `sec:lco-center`

### 1.1 위치

- 헤더 보존: L476 `\subsection{LCO 평형 중심과 ...}\label{sec:lco-center}`.
- 교체 후보: L477--488의 줄글 결론 및 단일 미분식.
- 보존 후보: L489--516 verifybox, L518--519 다음 절 연결 문장.
- 다음 경계: L522 `\section{히스테리시스 분기 중심 (N3)}\label{sec:hys}`.

### 1.2 LaTeX 사슬

```latex
\textbf{(a) 출발 — 흑연 forward식의 전극-중립 골격.}
\S\ref{sec:center} 의 평형 중심 유도는 host 물질명을 쓰지 않는다. 실험조건 매핑
식~\eqref{eq:n0map} 은 방향 부호 $\sigma_d$ 와 전류 크기 $|I|$ 를 정하는 슬롯이고,
전기화학 평형 식~\eqref{eq:eqcond} 은 삽입 반쪽반응의 비배치 자유에너지를
\[
\Delta G_j=-F\,U_j
\]
로 전위 중심에 묶는다($s=+1$ 규약). 여기에 들어가는 열역학 항등식
\[
\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}
\]
도 전극 종류를 가리지 않는다. LCO 로 넘어갈 때 바뀌는 것은 전이 집합과 입력값뿐이다:
\begin{equation}
j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j})
\longmapsto
(\Delta H_{\rxn,j}^{\mathrm{cat}},\Delta S_{\rxn,j}^{\mathrm{cat}}).
\label{eq:lco-n0sub}
\end{equation}
따라서 양극이라는 이유로 $U_j(T)$ 의 Gibbs 환산식에 새 부호를 넣지 않는다.

\textbf{(b) 연산 — LCO 반응 자유에너지를 평형 조건에 대입.}
LCO 전이 $j$ 의 비배치 반응 자유에너지를
\[
\Delta G_j^{\mathrm{cat}}
=\Delta H_{\rxn,j}^{\mathrm{cat}}-T\Delta S_{\rxn,j}^{\mathrm{cat}}
\]
로 두고, 식~\eqref{eq:eqcond} 의 $\Delta G_j=-F\,U_j$ 에 그대로 넣으면
\begin{equation}
\Delta H_{\rxn,j}^{\mathrm{cat}}
-T\Delta S_{\rxn,j}^{\mathrm{cat}}
=-F\,U_j^{\mathrm{cat}}(T).
\end{equation}
이는 흑연 식~\eqref{eq:Ujmid} 과 같은 연산이며, host 차이는 상첨자와 입력값에만 남는다.

\textbf{(c) 중간식 — 중심과 온도 계수.}
위 식을 $U_j^{\mathrm{cat}}$ 로 풀면
\[
U_j^{\mathrm{cat}}(T)
=\frac{-\Delta H_{\rxn,j}^{\mathrm{cat}}
+T\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}.
\]
온도 미분은 두 경로가 같은 결과에 닿는다. 직접 미분하면
\[
\frac{\partial U_j^{\mathrm{cat}}}{\partial T}
=\frac{\Delta S_{\rxn,j}^{\mathrm{cat}}}{F},
\]
이고, Gibbs 항등식 경로로도
\[
\frac{\partial\Delta G_j^{\mathrm{cat}}}{\partial T}
=-\Delta S_{\rxn,j}^{\mathrm{cat}},\qquad
\Delta G_j^{\mathrm{cat}}=-F\,U_j^{\mathrm{cat}}
\]
이므로
\[
-F\,\frac{\partial U_j^{\mathrm{cat}}}{\partial T}
=-\Delta S_{\rxn,j}^{\mathrm{cat}}
\quad\Longrightarrow\quad
\frac{\partial U_j^{\mathrm{cat}}}{\partial T}
=\frac{\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}.
\]

\textbf{(d) 박스 — LCO 평형 중심과 $\partial U/\partial T$.}
\begin{equation}
\boxed{\;
U_j^{\mathrm{cat}}(T)
=\frac{-\Delta H_{\rxn,j}^{\mathrm{cat}}
+T\Delta S_{\rxn,j}^{\mathrm{cat}}}{F},
\qquad
\frac{\partial U_j^{\mathrm{cat}}}{\partial T}
=\frac{\Delta S_{\rxn,j}^{\mathrm{cat}}}{F}
\quad(j\in\mathcal J_\mathrm{LCO})\;.}
\label{eq:lco-dUdT}
\end{equation}
관계식은 흑연 식~\eqref{eq:Uj} 와 부호까지 1:1 이고, 양극의 높은 중심
($\sim$3.9--4.2 V)은 LCO 입력에서 $-\Delta H_{\rxn,j}^{\mathrm{cat}}$ 가 크게 양으로
들어오기 때문에 생긴다. $\Delta S_{\rxn,j}^{\mathrm{cat}}$ 는
\S\ref{sec:lco-decomp} 에서 config$\cdot$vib$\cdot$electronic 성분으로 분해되는 같은 슬롯이며,
아래 verifybox 의 대표 단전극 계수 검산은 이 박스의 부호와 크기만 확인한다.
``전체 단전극 계수''와 ``전이별 성분''을 직접 동일시하지 않는다.
``T1 전자항 음수''도 전체 엔트로피 계수와 다른 층위의 성분이므로 이 박스와 충돌하지 않는다.
```

### 1.3 원문 대비

- 원문 L477--481의 결론인 "식은 전극 가정이 없고 LCO에도 그대로 성립"을 (a) 출발식으로 분해했다.
- 원문 L483--488의 단일 미분식을 (b) 대입, (c) 직접 미분 및 Gibbs 항등식 교차검증, (d) 박스식으로 확장했다.
- 원문 L489--516 verifybox의 수치 검산과 전자항 공존 설명은 보존 대상으로 남겼다. 이 supplement의 마지막 문장은 verifybox로 자연스럽게 이어지도록 층위 분리만 반복한다.
- 기존 C/P11 초안의 `eq:n0map` 부재 의심은 v1.0.12 실측상 오판이다. 실제 `eq:n0map`은 L206에 존재하므로 방향·전류 슬롯 참조는 가능하다.

### 1.4 논리 감사

- 부호: `\Delta G=-F U`와 `\Delta G=\Delta H-T\Delta S`를 결합하면 `U=(-\Delta H+T\Delta S)/F`. 따라서 `\partial U/\partial T=\Delta S/F`이고, 양극이라는 이유로 추가 마이너스가 생기지 않는다.
- 차원: `\Delta H`, `T\Delta S`는 J/mol, `F`는 C/mol이므로 `U`는 J/C = V. `\Delta S/F`는 J/(mol K) 나누기 C/mol = V/K.
- 극한: `\Delta S=0`이면 중심은 온도에 대해 움직이지 않는다. `\Delta H<0`의 큰 발열 입력은 `-\Delta H>0`로 중심을 올린다. verifybox의 `+0.83` mV/K 및 `+80` J/(mol K) 스케일은 새 값이 아니라 원문 검산값이다.

---

## 2. `sec:lco-hys`

### 2.1 위치

- 헤더 보존: L696 `\subsection{LCO order--disorder 와 MIT 2상역 ...}\label{sec:lco-hys}`.
- 교체 후보: L697--719의 줄글 결론.
- 다음 경계: L722 `\section{폭과 평형 점유 ...}\label{sec:width}`.
- `sec:lco-map`, `sec:lco-Se`, `sec:lco-gate`는 참조만 가능하고 본문 접촉 없음.

### 2.2 LaTeX 사슬

```latex
\textbf{(a) 출발 — LCO 전이를 흑연과 같은 정규용액 자유에너지에 얹기.}
\S\ref{sec:hys} 의 격자기체$\cdot$정규용액 유도는 ``동등한 자리에 리튬이 차고 빈다''는
가정에서 시작한다. 이 가정은 LCO $\mathrm{Li}_x\mathrm{CoO_2}$ 의 리튬 자리에도 같은 방식으로
쓸 수 있으므로, LCO 전이 집합을
\begin{equation}
\mathcal J_\mathrm{LCO}
=\{1:\mathrm{MIT},\ 2:\mathrm{OD}_a,\ 3:\mathrm{OD}_b\}
\label{eq:lco-J}
\end{equation}
로 두고 각 전이의 진행률 $\xi_j$ 에 대해
\begin{equation}
g_j^{\mathrm{cat}}(\xi_j)
=g_{0,j}^{\mathrm{cat}}
+RT\{\xi_j\ln\xi_j+(1-\xi_j)\ln(1-\xi_j)\}
+\Omega_j^{\mathrm{cat}}\,\xi_j(1-\xi_j)
\label{eq:lco-gxi}
\end{equation}
를 쓴다. 새 물리를 더하지 않고, 흑연 식~\eqref{eq:gxi} 의
$U_j,\Omega_j,\gamma_j,h_{\eta,j}$ 슬롯에 LCO 전이별 입력을 넣는 치환이다.
pure-LCO 초기값에서는 T1(MIT), T2, T3가 모두 상분리 후보지만, 실제 gap 유무는 최종 피팅된
$\Omega_j^{\mathrm{cat}}$ 가 $2RT$ 를 넘는지로 판정한다.

\textbf{(b) 연산 — 곡률과 spinodal 문턱.}
식~\eqref{eq:lco-gxi} 를 두 번 미분하면
\begin{equation}
\frac{\partial^2 g_j^{\mathrm{cat}}}{\partial \xi_j^2}
=\frac{RT}{\xi_j(1-\xi_j)}-2\Omega_j^{\mathrm{cat}}.
\label{eq:lco-gpp}
\end{equation}
따라서 spinodal 조건은 흑연 식~\eqref{eq:spinodal} 과 같은 구조로
\begin{equation}
\xi_{s,j}^{\pm}
=\tfrac12(1\pm u_j^{\mathrm{cat}}),\qquad
u_j^{\mathrm{cat}}
=\sqrt{1-\frac{2RT}{\Omega_j^{\mathrm{cat}}}}
\qquad(\Omega_j^{\mathrm{cat}}>2RT).
\label{eq:lco-spinodal}
\end{equation}
$\Omega_j^{\mathrm{cat}}\le2RT$ 이면 $u_j^{\mathrm{cat}}$ 가 실수가 아니므로 그 전이의 spinodal gap 은
0으로 닫힌다.

\textbf{(c) 중간식 — LCO 평형 전위 곡선과 두 끝점 차.}
흑연 식~\eqref{eq:Veq} 에 $U_j^{\mathrm{cat}}$ 와 $\Omega_j^{\mathrm{cat}}$ 를 넣으면
\begin{equation}
V_{\eq,j}^{\mathrm{cat}}(\xi)
=U_j^{\mathrm{cat}}
+\frac{RT}{F}\ln\frac{\xi}{1-\xi}
+\frac{\Omega_j^{\mathrm{cat}}}{F}(1-2\xi).
\label{eq:lco-Veq}
\end{equation}
spinodal 끝점에서
\[
\frac{\xi}{1-\xi}\bigg|_{\xi_{s,j}^{\pm}}
=\frac{1\pm u_j^{\mathrm{cat}}}{1\mp u_j^{\mathrm{cat}}},
\qquad
(1-2\xi)\big|_{\xi_{s,j}^{\pm}}=\mp u_j^{\mathrm{cat}},
\]
이므로 상수 중심 $U_j^{\mathrm{cat}}$ 는 극대$-$극소 차에서 상쇄되고
\[
\Delta U_j^{\hys,\mathrm{cat}}
=V_{\eq,j}^{\mathrm{cat}}(\xi_{s,j}^{-})
-V_{\eq,j}^{\mathrm{cat}}(\xi_{s,j}^{+})
=\frac{2}{F}
\left[
\Omega_j^{\mathrm{cat}}u_j^{\mathrm{cat}}
-2RT\,\operatorname{artanh}u_j^{\mathrm{cat}}
\right].
\]
이는 흑연 식~\eqref{eq:hysdiff}--\eqref{eq:dUhys} 의 LCO 대입형이다.

\textbf{(d) 박스 — LCO gap 과 방향별 분기 중심.}
\begin{equation}
\boxed{\;
\Delta U_j^{\hys,\mathrm{cat}}(T)
=
\begin{cases}
\dfrac{2}{F}\left[
\Omega_j^{\mathrm{cat}}u_j^{\mathrm{cat}}
-2RT\,\operatorname{artanh}u_j^{\mathrm{cat}}
\right],
& \Omega_j^{\mathrm{cat}}>2RT,\\[4pt]
0, & \Omega_j^{\mathrm{cat}}\le2RT,
\end{cases}
\quad
u_j^{\mathrm{cat}}
=\sqrt{1-\dfrac{2RT}{\Omega_j^{\mathrm{cat}}}}\;}
\label{eq:lco-dUhys}
\end{equation}
\begin{equation}
\boxed{\;
U_j^{\,d,\mathrm{cat}}
=U_j^{\mathrm{cat}}
+\tfrac12\sigma_d h_{\eta,j}\gamma_j
\Delta U_j^{\hys,\mathrm{cat}}(T)\;}
\label{eq:lco-Ubranch}
\end{equation}
방전($\sigma_d=+1$)은 중심을 위로, 충전($\sigma_d=-1$)은 아래로 옮긴다.

\textbf{T2$\cdot$T3 order--disorder.}
$x\approx0.5$ 부근의 monoclinic 초격자 전이 T2($\sim$4.05 V,
hex$\to$monoclinic)와 T3($\sim$4.17--4.20 V, monoclinic$\to$hex)는
식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 각각 $j=2,3$ 을 넣어 적는다.
charge-order 엔트로피 변화($\approx0.47$ J/(mol\,K)@$x=\tfrac12$,
$\approx1.49$ J/(mol\,K)@$x=\tfrac23$, tier A)는
$\Delta S_j^{\mathrm{config}}$ 슬롯에 들어가는 엔트로피 값이지,
spinodal 문턱을 정하는 상호작용 에너지 $\Omega_j^{\mathrm{cat}}$ 가 아니다.
따라서 이 수치들로 $\Omega_j^{\mathrm{cat}}$ 를 산출하지 않는다.

\textbf{T1 MIT 2상역.}
T1($\sim$3.9 V, $x\approx0.75$--$0.94$)의 구조적 2상 공존도 같은
$\Omega_1^{\mathrm{cat}}$ 문턱과 분기식을 받는다. 다만 MIT 의 전자 자유도는 이 히스 gap 에
새 항으로 더하지 않고, 식~\eqref{eq:lco-decomp} 의
$\Delta S_{e,1}^{\mathrm{mol}}(x,T)$ 를 통해 $U_1^{\mathrm{cat}}(T)$ 의 온도 이동 슬롯으로 들어간다:
\begin{equation}
\boxed{\;
\underbrace{\Delta U_1^{\hys,\mathrm{cat}}
\ \Leftarrow\ \Omega_1^{\mathrm{cat}}}_{\text{정규용액 구조 gap}}
\quad\Big\|\quad
\underbrace{\partial U_1^{\mathrm{cat}}/\partial T
\ \Leftarrow\ \Delta S_{e,1}^{\mathrm{mol}}(x,T)}_{\text{전자 엔트로피 슬롯}}\;}
\label{eq:lco-mit}
\end{equation}
이 분리가 구조적 2상역과 전자 엔트로피 항의 이중계산을 막는 경계다.

\textbf{도핑 보정(우리 시료).}
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox 와 전자항을 보존하되
order--disorder$\cdot$MIT 상전이를 억제할 수 있다. 정규용액 틀에서는 이를
pure-LCO 초기값 $\Omega_j^{\mathrm{cat,pure}}$ 에서 도핑 피팅값
$\Omega_j^{\mathrm{cat,dop}}$ 로 낮아지는 입력 변화로 둔다. 문턱 접근 극한은
\begin{equation}
\Omega_j^{\mathrm{cat,dop}}\to2RT^+
\quad\Longrightarrow\quad
u_j^{\mathrm{cat,dop}}\to0,\qquad
\Delta U_j^{\hys,\mathrm{cat,dop}}
\to\frac{8RT}{3F}\big(u_j^{\mathrm{cat,dop}}\big)^3\to0.
\label{eq:lco-dope}
\end{equation}
$\Omega_j^{\mathrm{cat,dop}}\le2RT$ 로 피팅되는 전이는 같은 박스식에서 gap 이 0이 된다.
중심 전위의 미세 shift 는 $U_j^{\mathrm{cat}}$ 피팅값 이동으로 따로 들어가며,
$\Omega_j^{\mathrm{cat}}$ 하나가 gap 축소와 중심 이동을 동시에 만든다고 쓰지 않는다.
```

### 2.3 원문 대비

- 원문 L697--699의 "같은 정규용액 틀" 결론을 (a) `\mathcal J_\mathrm{LCO}`와 `g_j^{\mathrm{cat}}` 출발식으로 명시했다.
- 원문 L701--706의 T2·T3 설명은 보존하되, `0.47/1.49` J/(mol K)를 `\Omega_j^{\mathrm{cat}}`로 바꾸지 않는 혼동 가드를 추가했다.
- 원문 L708--713의 T1 MIT 설명은 구조 gap 슬롯과 전자 엔트로피 슬롯을 분리하는 박스식으로 바꿨다. `sec:lco-Se`와 `sec:lco-gate` 본문은 건드리지 않는다.
- 원문 L715--719의 도핑 보정은 `\Omega_j^{\mathrm{cat,dop}}\to2RT^+` 극한과 `U_j^{\mathrm{cat}}` shift 슬롯 분리로 수식화했다.
- 기존 C/P11 초안의 "LCO 3/3" 강한 확정 표현은 v1.0.12의 도핑 억제 문단과 충돌하지 않도록 "pure-LCO 초기값의 세 전이 후보, 최종 판정은 피팅된 `\Omega_j^{\mathrm{cat}}>2RT`"로 완화했다.

### 2.4 논리 감사

- 부호: `\Delta U_j^{\hys,\mathrm{cat}}=V(\xi_s^-)-V(\xi_s^+)`로 정의하면 흑연 식과 같이 비음수가 된다. `U_j^{d,\mathrm{cat}}=U_j^{\mathrm{cat}}+\frac12\sigma_d h_{\eta,j}\gamma_j\Delta U`이므로 방전 `\sigma_d=+1`은 위, 충전 `\sigma_d=-1`은 아래로 이동한다.
- 차원: `RT`와 `\Omega_j^{\mathrm{cat}}`는 J/mol, `u`와 `\operatorname{artanh}u`는 무차원이다. 대괄호 전체를 `F`로 나누면 V. `U_j^{d,\mathrm{cat}}`도 V.
- 극한: `\Omega_j^{\mathrm{cat}}\le2RT`에서는 `u`가 실수가 아니므로 gap 0. `\Omega_j^{\mathrm{cat}}\to2RT^+`에서는 `u\to0`이고 `\operatorname{artanh}u=u+u^3/3+\cdots`라 `\Delta U\to(8RT/3F)u^3\to0`. `\gamma_j\to0` 또는 `h_{\eta,j}\to0`이면 분기 중심은 `U_j^{\mathrm{cat}}`로 돌아간다.

---

## 3. 3줄 요약

1. Step 1/3은 v1.0.12의 `sec:lco-center`와 `sec:lco-hys`만 다뤘고, `.tex`/코드는 수정하지 않았다.
2. `center`는 `\Delta G=-FU`와 `\Delta G=\Delta H-T\Delta S`에서 `U_j^{\mathrm{cat}}`, `\partial U/\partial T` 박스까지 재유도했다.
3. `hys`는 `g_j^{\mathrm{cat}}`→곡률→spinodal→`V_\eq`→`\Delta U^\hys`·`U^d` 박스로 닫고, `\Omega_j` 계열은 기호 유지·피팅 판정으로 남겼다.
