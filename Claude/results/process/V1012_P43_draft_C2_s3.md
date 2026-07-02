# V1012 Phase 4.3 draft C2 s3 — plug-in/MSMR/H-2 final supplement

대상:
- `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`
- `Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex`

범위:
- Ch1 `sec:lco-decomp` 말미 및 `sec:lco-code` 시작부(L1715--1792).
- Ch2 `ssec:logistic` keybox(L161--165)와 H-2 정정 근거.

출발점:
- `V1012_P43_draft_C2_s1.md`, `V1012_P43_draft_C2_s2.md` 형식과 금지선을 이어받았다.
- `FABLE_REAUDIT_C4_note.md` 1--68행 전체를 정독해 H-2 근거를 확인했다.

금지 준수:
- `.tex`/코드 수정 없음.
- 절별 루핑 선형 유지.
- 물리/결과식/부호/단위 불변.
- 신규 개념 추가 없음.
- `T^2` 가드, tier-C placeholder 라벨, round-trip 가드 유지.

읽은 범위:
- `FABLE_REAUDIT_C4_note.md`: 1--68행 전체.
- `graphite_ica_ch1_v1.0.12.tex`: L1028--1080, L1088--1112, L1670--1815 직접 확인; `rg`로 `MSMR`, `lco-code`, `lco-decomp`, `dSemolar`, `dSegate`, `ggate`, `T^2`, `tier-C` 참조 재대조.
- `graphite_ica_ch2_v1.0.12.tex`: L130--190, 파생 A/C 및 `revheat` 관련 `rg` 위치 직접 대조.

---

## 1. Ch1 `sec:lco-decomp` 말미 — 전자항 plug-in 사슬

### 위치

- 현재 헤더: L1715 `\subsection{LCO $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해 — config + vib + electronic}\label{sec:lco-decomp}`
- 현재 전자항/구현 예고 후보 범위: L1744--1765.
- 직접 근거: `eq:dSemolar` L1034--1038, `eq:U1T2` L1074--1075, `eq:ggate` L1088--1090, `eq:dSegate` L1101--1105, 기존 `eq:lco-decomp` L1719--1723.

### LaTeX 사슬

```latex
\textbf{(e) 전자항 plug-in — $V$ 격자 forward 경로.}
전자항은 새 peak 식을 만들지 않고 T1 의 $\Delta S_{\rxn,1}^\mathrm{cat}$ 슬롯에만 들어간다.
코드는 전압 격자 위에서 도는 반면 식~\eqref{eq:ggate}$\cdot$\eqref{eq:dSegate} 는 조성 $x$ 의 함수이므로,
T1 진행률을 먼저 조성 좌표로 보낸다:
\[
V \longmapsto \xi_{\eq,1}(V,T)
\longmapsto x=x\!\big(\xi_{\eq,1}(V,T)\big).
\]
그 조성을 MIT 게이트에 대입하면
\begin{equation}
\Delta S_{e,1}^{\,\mathrm{mol}}(V,T)
=\Delta S_{e,1}^{\,\mathrm{mol}}
\!\left(x\!\big(\xi_{\eq,1}(V,T)\big),T\right)
=N_A\,\Delta S_{e,1}
\!\left(x\!\big(\xi_{\eq,1}(V,T)\big),T\right).
\label{eq:lco-Se-plugin}
\end{equation}
여기서 마지막 등호는 자리당 식~\eqref{eq:dSegate} 를 몰당 식~\eqref{eq:dSemolar} 로 올리는 단위 다리다.
따라서 forward 슬롯은
\begin{equation}
\Delta S_{\rxn,j}^\mathrm{cat}(V,T)
=\Delta S_j^0+\Delta S_j^\mathrm{vib}
+\begin{cases}
\Delta S_{e,1}^{\,\mathrm{mol}}
\!\left(x\!\big(\xi_{\eq,1}(V,T)\big),T\right), & j=\mathrm{T1},\\
0, & j=\mathrm{T2},\mathrm{T3},
\end{cases}
\label{eq:lco-decomp-forward}
\end{equation}
로 평가된다. 이 값이 곧 중심 온도 이동식으로 전달된다:
\[
\Delta S_{e,1}^{\,\mathrm{mol}}(V,T)
\longrightarrow
\Delta S_{\rxn,1}^\mathrm{cat}(V,T)
\longrightarrow
U_1(T)
\longrightarrow
\left(\frac{\dd Q}{\dd V}\right)_{\mathrm{LCO}} .
\]

\textbf{(f) $T^2$ 가드와 round-trip 지위.}
식~\eqref{eq:dSemolar}$\cdot$\eqref{eq:dSegate} 에서 전자항은 $T$ 에 선형이므로
\[
\Delta S_{\rxn,1}^\mathrm{cat}(T)=\Delta S_0+a_eT
\]
로 읽히는 구간에서는 식~\eqref{eq:U1T2} 와 같이
\[
U_1(T)=U_1(T_0)
+\frac{\Delta S_0}{F}(T-T_0)
+\frac{a_e}{2F}(T^2-T_0^2)
\]
가 된다. 전자항의 식별 신호는 peak 위치를 단순 선형으로 외삽하는 것이 아니라
$\partial U_1/\partial T$ 가 $T$ 에 선형이고, 적분된 $U_1(T)$ 에 $T^2$ 곡률과 $\tfrac12$ 계수가 남는다는 점이다.
따라서 `LCO_MSMR_LIT`의 전자항 시연값과 게이트 초기값은 tier-C placeholder 로 유지하고,
T1 위치 $U_1(298)\approx3.90$ V 및 다온도 이동률을 round-trip 으로 맞춘 뒤에만 신뢰값으로 승격한다.
```

### 원문 대비

- 현재 L1756--1761의 좌표 매핑 문장을 `V -> xi_eq,1 -> x -> Delta S_e` 사슬로 풀었다.
- 현재 L1784--1788의 plug-in 설명을 `eq:lco-Se-plugin`과 `eq:lco-decomp-forward`로 분리했다.
- `N_A` 몰당 환산, `eV -> J` 환산 방향, 삽입 기준 `<0` 부호는 원문 `eq:dSemolar`/`eq:dSegate`의 규칙을 그대로 따른다.
- 현재 L1068--1080의 `T^2` 가드는 별도 단락으로 유지했다. `a_e/(2F)`의 `1/2` 계수를 잃지 않는 것이 핵심이다.
- tier-C placeholder 및 round-trip 승격 조건은 표 `tab:lco-staging` caption의 L331--335와 L1761--1765의 지위를 유지한다.

### 논리 감사

- 루핑 선형성: `j=T1,T2,T3` 루프는 그대로이고, electronic 항만 T1 cases 분기로 0/nonzero를 선택한다.
- 물리 불변: 전자항은 peak 모양이나 합산식을 바꾸지 않고 `Delta S -> U(T)` 경로만 통과한다.
- 부호 불변: 삽입 기준 `Delta S_e<0`, 탈리튬화 방출 `|Delta S_e|>0` 규약을 뒤집지 않았다.
- 단위 불변: forward 슬롯은 J/(mol K)이므로 자리당 `Delta S_e`가 아니라 `N_A Delta S_e`를 넣는다.
- 신규개념 금지: 새 상태변수나 새 broadening 모델 없이 기존 `xi_eq`, `x(xi_eq)`, `eq:dSemolar`, `eq:dSegate`, `eq:ggate`만 사용했다.

---

## 2. Ch1 `sec:lco-code` — MSMR 동형 사슬

### 위치

- 현재 헤더: L1767 `\subsection{forward 코드의 LCO 일반화 — 파라미터 교체 + 전자항 plug-in (H)}\label{sec:lco-code}`
- 현재 MSMR 후보 범위: L1768--1779.
- 보존할 대응: `X_j <-> Q_j`, `U_j^0 <-> U_j^d`, `omega_j <-> w_j`, `f <-> -sigma_d`.

### LaTeX 사슬

```latex
\textbf{(a) 출발 — MSMR logistic.}
MSMR 은 전이별 용량 몫을 중심 전위와 폭으로 나눈 logistic 합으로 쓴다:
\begin{equation}
x_j(U)=\frac{X_j}{1+\exp\!\left[f_j(U-U_j^0)/\omega_j\right]}.
\label{eq:msmr}
\end{equation}
이를 용량으로 나누어 정규화하면
\begin{equation}
\hat x_j(U)\equiv\frac{x_j(U)}{X_j}
=\frac{1}{1+\exp\!\left[f_j(U-U_j^0)/\omega_j\right]}.
\label{eq:msmr-normalized}
\end{equation}

\textbf{(b) 대응 대입 — Ch1 logistic 과 같은 지수 자리.}
Ch1 의 전이별 평형 진행률은
\begin{equation}
\xi_{\eq,j}(V,T)=
\frac{1}{1+\exp\!\left[-\sigma_d(V-U_j^{\,d})/w_j\right]}.
\label{eq:lco-code-xieq}
\end{equation}
식~\eqref{eq:msmr-normalized} 와 식~\eqref{eq:lco-code-xieq} 의 지수 자리를 항목별로 맞추면
\begin{equation}
\boxed{\;
X_j\leftrightarrow Q_j,\qquad
U_j^0\leftrightarrow U_j^{\,d},\qquad
\omega_j\leftrightarrow w_j,\qquad
f_j\leftrightarrow-\sigma_d
\;}
\label{eq:msmr-map}
\end{equation}
이다. MSMR 지수는 $+f_j(U-U_j^0)$ 이고 Ch1 지수는
$-\sigma_d(V-U_j^{\,d})$ 이므로, 같은 진행 방향을 가리키려면 부호 인자가
$f_j=-\sigma_d$ 로 대응해야 한다.

\textbf{(c) 중간식 — LCO 전이별 평형 종.}
따라서 LCO 의 세 전이는 MSMR 파라미터를 Ch1 전이 dict 로 옮긴 뒤 같은 평형 종을 만든다:
\begin{equation}
\xi_{\eq,j}^{\mathrm{LCO}}(V,T)
=\frac{1}{1+\exp\!\left[-\sigma_d(V-U_j^{\,d,\mathrm{cat}}(T))/w_j\right]},
\qquad
j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}.
\label{eq:lco-msmr-xieq}
\end{equation}
여기서 $U_j^{\,d,\mathrm{cat}}(T)$ 는 \S\ref{sec:lco-center}$\cdot$\S\ref{sec:lco-hys}$\cdot$
\S\ref{sec:lco-decomp} 의 중심, 히스 분기, 엔트로피 plug-in 을 통과한 중심이다.

\textbf{(d) 박스 — peak 로 닫히는 forward 사슬.}
\begin{equation}
\boxed{\;
\left(\frac{\dd Q}{\dd V}\right)_{\mathrm{LCO}}(V)
=C_\bg+
\sum_{j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}}
Q_j\frac{\xi_{\eq,j}^{\mathrm{LCO}}(1-\xi_{\eq,j}^{\mathrm{LCO}})}{w_j}
\;}
\label{eq:lco-msmr-peak}
\end{equation}
곧 MSMR 은 별도 forward 물리가 아니라, 정규화한 뒤 $f_j=-\sigma_d$ 를 대입하면
Ch1 logistic 종과 같은 peak 박스로 닫히는 파라미터 표현이다.
```

### 원문 대비

- 현재 L1768--1779의 MSMR 동형 설명을 `MSMR식 -> 정규화 -> 대응대입 -> xi_eq,j -> peak 박스` 순서로 선형화했다.
- 방향 인자 `f=-sigma_d`는 원문 L1776--1779의 부호 비교를 박스 대응식으로 고정했다.
- `sec:lco-code`의 결론인 “구조 변경 0, 파라미터 교체 + 전자항 plug-in”은 유지했다.
- 새 합산식은 기존 `eq:sum`과 `eq:eqpeak`의 LCO 제한형이다.

### 논리 감사

- 루핑 선형성: MSMR 각 종을 `j`별 logistic으로 정규화한 뒤 `sum_j Q_j peak_shape_j`로 더한다.
- 물리 불변: MSMR은 Ch1 logistic과 동형인 파라미터화로만 사용되며, 새 전극 물리나 새 반응속도식을 넣지 않는다.
- 부호 불변: 지수 비교에서 `+f(U-U0)`와 `-sigma_d(V-Ud)`가 같은 자리를 채우므로 `f=-sigma_d`다.
- 결과식 불변: 중심, 폭, 용량, peak 면적은 기존 `U_j^d`, `w_j`, `Q_j` 규칙을 따른다.
- 신규개념 금지: MSMR 정규화와 변수 대응만 썼고, 추가 MSMR 하위모델은 도입하지 않았다.

---

## 3. Ch2 H-2 — `ssec:logistic` 폭 지위 정정문안

### 위치

- 현재 헤더: L140 `\subsection{전기화학 퍼텐셜과 Chapter 1 logistic 의 기원}\label{ssec:logistic}`
- 현재 keybox 후보 범위: L161--165.
- 직접 근거: `FABLE_REAUDIT_C4_note.md` §2 전체, Ch2 파생 C L540--568, `sec:revheat` L683--685, 파생 A 수치검증 L486 부근.

### 정정 원칙

- 기존 keybox의 “logistic 폭 `w=RT/F` 및 `w_j=n_jRT/F`는 임의 모수가 아니다”라는 단정은 단상 격자기체 출발식에만 한정한다.
- 파생 C의 “흑연 staging 두-상 전이는 실측 폭이 평형 예측 `nRT/F`가 아니라 다온도 `dQ/dV` 피팅 폭”이라는 서술과 충돌하지 않게 일원화한다.
- 파생 A의 “완전식 = finite difference 부동소수점 일치” 검증은 `w_j(T)=n_jRT/F`, 즉 `partial w_j/partial T=n_jR/F`를 구현 전제로 둘 때의 검증이라고 명시한다.
- 이 정정은 폭의 지위 문안만 고치며, logistic 식 자체와 `Omega=2RT` 임계, 파생 A/B/C/D 수식의 결과값은 바꾸지 않는다.

### LaTeX 문안

```latex
\begin{keybox}
Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{격자기체 점유 분포의 여집합}(탈리튬화
진행률 $=1-\theta$)이다. 단, 폭의 지위는 상영역별로 구분한다. 단상 또는 균질 고용체 영역
($\Omega\le2RT$)에서는 logistic 폭 $w=RT/F$ 가 단일 자리 2-상태 분배함수~\eqref{eq:Z1} 가
정하는 열적 폭이며, 전이별 유효 폭을 $w_j=n_jRT/F$ 로 쓰는 것은 이 단상 평형 예측의
폭 다중도 표기다. 반면 흑연 staging 처럼 두-상 plateau 가 생기는 전이($\Omega>2RT$)의
실측 peak 폭은 파생 C(\S\ref{ssec:weff})처럼 평형 등온선 하나가 정하는 값이 아니라
다온도 $dQ/dV$ 로 피팅되는 현상학적 폭이다.

따라서 본 장의 파생 A 수치 검증과 코드 경로에서 $w_j=n_jRT/F$ 를 사용할 때의 의미는
``두-상 폭이 원리적으로 항상 $nRT/F$ 로 확정된다''가 아니라, 해당 forward 구현이 채택한
열적 스케일링 전제($\partial w_j/\partial T=n_jR/F$) 아래에서 겹침가중 완전식이 finite
difference 검증과 일치한다는 것이다. $\theta=$ Li 점유율(만충서 1),
$\xi=1-\theta=$ 탈리튬화 진행률(희박서 1); 둘은 같은 점유 분포의 두 이름이다.
Chapter 2 는 이 분포를 결론이 아니라 출발점으로 삼아 엔트로피를 쌓는다.
\end{keybox}
```

### 원문 대비

- 현재 L162--164의 “현상학적 곡선맞춤이 아니라 ... 임의 모수가 아니다” 단정을 삭제하지 않고, 적용 범위를 `Omega <= 2RT` 단상/균질 고용체로 제한했다.
- 파생 C L544--560 및 `sec:revheat` L683--685의 두-상 폭 지위와 같은 문장 안에서 연결했다.
- `FABLE_REAUDIT_C4_note.md`가 지적한 모순, 즉 keybox는 `w_j=n_jRT/F`를 확정하고 파생 C는 같은 흑연 staging에 대해 이를 부정하는 충돌을 해소한다.
- 파생 A 검증은 `w_j(T)=n_jRT/F` 구현 전제에서의 검증이라고 못박았다. 따라서 그 검증을 두-상 폭의 보편 열역학 결론으로 읽지 않는다.

### 논리 감사

- 단상 한정: `Omega <= 2RT`에서는 평형 등온선이 단조이므로 logistic/평형 폭 설명과 모순이 없다.
- 두-상 보존: `Omega > 2RT`에서는 파생 C의 “실측 폭은 현상학적 피팅 폭” 결론을 유지한다.
- 파생 A 전제 명시: 검증 PASS의 조건을 `w_j(T)=n_jRT/F`로 분리해, 코드 구현 검증과 물리 일반명제를 혼동하지 않는다.
- 물리 불변: `xi_eq`, `theta`, `Omega=2RT`, 파생 C의 폭 지위, 파생 A의 수치검증 결과를 바꾸지 않는다.
- 신규개념 금지: 새 폭 모델을 만들지 않고, 기존 단상/두-상 구분과 구현 전제만 명시했다.

---

## 3줄 요약

1. Ch1 전자항 plug-in은 `x=x(xi_eq,1(V)) -> Delta S_e,1(V,T) -> Delta S_rxn,1(V,T) -> U_1(T) -> dQ/dV` 사슬로 정리했고, `T^2` 적분 가드와 tier-C/round-trip 지위를 유지했다.
2. Ch1 MSMR은 `MSMR식 -> 정규화 -> f=-sigma_d 대응 -> xi_eq,j -> peak 박스`로 닫아, MSMR을 새 물리가 아니라 Ch1 logistic forward의 동형 파라미터화로 정리했다.
3. Ch2 H-2는 `w=RT/F`, `w_j=n_jRT/F` 단정을 `Omega <= 2RT` 단상 평형 예측으로 한정하고, 파생 A 검증은 `w_j(T)=n_jRT/F` 구현 전제에서만 성립한다고 명시해 파생 C와의 모순을 일원화했다.
