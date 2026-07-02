
# V1012 Phase 4.3 — 작성 드래프트 S1

> 역할: Anode_Fit v1.0.12 Phase 4.3 작성 드래프트 **S1**(N=10 경쟁: 3 Sonnet + 3 Opus + 3 Codex + 1 Fable, 무통신 독립 작성). 본 문건은 **드래프트 supplement 뿐**이다 — `docs/v1.0.12/*.tex`·코드는 **미수정**(편입은 Fable master 전담). 절별 루핑 선형 작업(정독→수식 사슬→자기검수→앞 절 정합)으로 작성했다.
> 대상: `docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`(1848줄, head→tail 전문 정독) · `docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex`(710줄, head→tail 전문 정독) · `docs/v1.0.12/Anode_Fit_v1.0.12.py`(func_w/_width 교차확인만, L75-76·L304-307).
> 계승 자료: `results/process/V1011_P11_map_v10.md`(center·hys 체리픽, 8종 통합) · `results/process/V1010_LCO_STYLE_REPORT.md`(필요 수식 사슬 명세) · `results/process/FABLE_REAUDIT_C4_note.md`(H-2 근거).

---

## 0. 조립 전 확인 사실 (실측, 추정 없음)

### 0.1 라벨 인벤토리 (전수 grep, 충돌 검증)
- 현재 `graphite_ica_ch1_v1.0.12.tex` 의 기존 `eq:lco-*` 라벨은 **정확히 2개**: `eq:lco-dUdT`(L487 정의) · `eq:lco-decomp`(L1723 정의). 그 외 모든 `eq:lco-*` 신설명은 충돌 0(전수 grep `\label\{eq:lco-` 확인, 2건만 매치).
- `eq:lco-dUdT` 의 `\eqref` 참조 = **6곳**: L493·L498(verifybox)·L1229(sec:lco-peak)·L1750(sec:lco-decomp)·L1790(sec:lco-code)·L1877(표 tab:nodemap류 행). V1011 map 이 주장한 "6곳"(v1.0.11 기준)을 v1.0.12 실측으로 **독립 재확인** — 개수 일치, 줄 번호만 이동(+shift). ★따라서 이 라벨은 **재사용 필수**(신규 정의 금지).
- `eq:lco-decomp` 의 `\eqref` 참조 = **11곳**(L489·505·508·514·1040·1060·1729·1738·1761·1785·1879). 이 라벨도 **재사용 필수**.
- 본 드래프트가 신설하는 라벨 21개는 아래 §1–§6 각 표에 개별 grep 결과(`No matches found`)와 함께 기재한다 — 전부 `eq:lco-*` 프리픽스, 기존 2개와 겹치지 않음.

### 0.2 편입 위치 실측 (교체/보존 범위, v1.0.12 실측 줄번호)
| 절 | 헤더(보존) | 교체 범위 | 보존 범위 | 다음 경계(불변) |
|---|---|---|---|---|
| `sec:lco-center` | L476 | **L477–494** | **L496–516 verifybox** | L521 `\section{...}\label{sec:hys}` |
| `sec:lco-hys` | L696 | **L697–719** | — | L722 `\section{...}\label{sec:width}` |
| `sec:lco-peak` | L1220 | **L1221–1232** | — | L1234 `\subsection{...}\label{sec:broadening}`(★흑연 본체, 불가침) |
| `sec:lco-decomp` | L1715 | **L1716–1754**(재구성 삽입) | 개념(itemize 요지) 계승 | L1756 예고 문단 |
| 전자항 plug-in(예고 문단) | — | **L1756–1765** | — | L1767 `\subsection{...}\label{sec:lco-code}` |
| `sec:lco-code`(MSMR) | L1767 | **L1768–1792** | — | L1794 `\subsection{전체 입력 인자...}`(공통, 비-LCO 전용) |

★v1.0.11 기준 V1011 map 의 줄번호(L470–512·L684–708)와 본 드래프트의 v1.0.12 실측 줄번호(L476–516·L696–719)는 6~12줄 이동돼 있다 — 두 버전 사이 해당 절 자체의 문구는 "물리 불변" 원칙대로 사실상 동일하나(v1.0.12 헤더 코멘트 "물리·부호·식 불변"), **줄 번호는 절대 맹신하지 않고 본 드래프트가 직접 재실측**했다.

### 0.3 불가침 확인
`sec:lco-map`(L301)·`sec:lco-Se`(L965)·`sec:lco-gate`(L1082)·N0–N9 흑연 본체(`sec:notation`·`sec:pol`·`sec:center`·`sec:hys`·`sec:width`·`sec:eqpeak`·`sec:broadening`·`sec:lag`·`sec:tail`·`sec:sum`)·전자엔트로피 절(`sec:lco-electronic`, `sec:lco-why`, `sec:lco-Se`) 는 **읽기만 하고 손대지 않았다** — 아래 모든 수식 사슬은 이 절들의 기존 결과식을 **참조·대입**만 하며 재유도하지 않는다(★코너: `sec:broadening` 은 `sec:lco-peak` 바로 다음 절이라 인접 경계만 명시하고 내용은 미접촉).

### 0.4 M-10 가드·Ω 기호 유지 확인
- ★M-10 가드(L1068–1080, `eq:U1T2`: 전자항 $\Delta S_e\propto T$ → $U_1(T)$ 이동 $\propto T^2$, $T_\mathrm{ref}$ 적분 해석)는 `sec:lco-Se` 안에 있어 미접촉 — 본 드래프트의 center·plug-in 절은 이를 **인용만** 한다(§1.4·§5.4).
- `Ω_j` 기호는 전 절에서 **기호로만** 쓴다 — 수치 대입 0건. 0.47/1.49 J/(mol·K)(Motohashi, T2/T3)는 **config $\Delta S$**(엔트로피 값)이지 $\Omega_j$(상호작용 에너지, J/mol)가 아님을 §2.3에서 재확인·명시한다.
- 신규 개념(ρ(U_app)·PSD·유효반경 등) 0건 도입 — `sec:lco-peak`(§3)에서 LCO 세 전이 폭을 다룰 때도 흑연-특정 구조무질서 근거를 옮기지 않고 `sec:broadening`(불가침)을 참조만 한다.

---

## 1. `sec:lco-center` — LCO 평형 중심과 $\partial U_j/\partial T$

### 1.1 위치
**교체 L477–494**(전극-무관 단정 2문단 + `eq:lco-dUdT` 괄호 전보체 + 대표스케일 프로즈). L476 헤더·L496–516 verifybox 보존.

### 1.2 원 줄글 대비
원문(L477–494)은 "식~\eqref{eq:Uj} 는 유도에 전극 가정이 없다"·"온도 의존도 같은 미분이다"라고 **결론만 서술**하고, (i) 어느 유도 단계에도 전극-고유 항이 없는지, (ii) $\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$ 가 두 개의 독립 경로(직접 미분 vs Gibbs 항등식 경유)로 같은 값에 닿는지를 **보이지 않는다** — V1010 STYLE_REPORT 가 지목한 "괄호 전보체" 결함(§0.2 표)이다.

### 1.3 계승 방침
`V1011_P11_map_v10.md` §1 의 (a)–(d) 사슬을 **출발점으로 계승**하되, 아래 재유도(§1.4)로 독립 검증한 뒤 v1.0.12 실측 줄번호·라벨에 맞춰 재기술한다. 재검증 결과 원 사슬의 **대수·부호는 전부 정확**했고(맹신 없이 손으로 재확인), 유일하게 보강한 것은 (c)의 "이중 경로" 서술이 암묵적으로 깔고 있던 전제 — $\Delta S_{\rxn,j}^\mathrm{cat}$ 를 그 순간의 **상수로 대입**해 미분한다는 것(전자항처럼 $\Delta S$ 자체가 $T$ 의존이면 곱미분 항이 하나 더 생김) — 을 (d) 박스에 명시적으로 못박은 것이다(§1.4 말미).

### 1.4 수식 사슬 (재유도 검증 완료)

```latex
\textbf{(a) 출발 — 전극-중립 골격의 세 진입.}
\S\ref{sec:center} 의 평형 중심 유도를 되짚으면 어느 다리에도 ``흑연''이라는 물질 고유 항이 들어가지
않는다: (i) 실험조건 매핑 식~\eqref{eq:n0map} 의 방향 부호$\cdot$전류 환산
$\sigma_d=\pm1,\ |I|=\code{c\_rate}\,Q_\cell$ 은 삽입형 전극이면 종류를 가리지 않고, (ii) 전기화학 평형
조건 식~\eqref{eq:eqcond}($\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U),\ \Delta G_j=-sFU_j$)는 삽입
반쪽반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 의 전기화학 평형
(식~\eqref{eq:eqbalance})에서 나오며 host 가 흑연인지 LCO 인지에 무관하고(host 의 화학 정체는 상수
$\mu^0$ 값으로만 흡수된다), (iii) 비배치 몫 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 은 반응
종에 무관한 열역학 항등식(식~\eqref{eq:Ujmid} 유도와 동일)이다. LCO 로 넘어갈 때 이 세 자리에 들어가는
것은 전이 집합과 입력값의 치환뿐이다:
\begin{equation}
j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j})\ \longmapsto\
(\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat}).
\label{eq:lco-n0sub}
\end{equation}
곧 $\sigma_d$ 는 방향 선택 슬롯에 남고, 평형 중심 $U_j(T)$ 의 Gibbs 환산식에는 새 양극 부호가 끼지 않는다.

\textbf{(b) 연산 — 평형 조건에 반응 자유에너지 대입.}
전이 $j$ 의 비배치 반응 자유에너지 $\Delta G_j^\mathrm{cat}=\Delta H_{\rxn,j}^\mathrm{cat}
-T\Delta S_{\rxn,j}^\mathrm{cat}$ 를 식~\eqref{eq:eqcond} 의 $\Delta G_j=-sFU_j$($s=+1$)에 넣으면
\[
\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}=-F\,U_j^\mathrm{cat}(T),
\]
곧 흑연 식~\eqref{eq:Ujmid} 과 글자 그대로 같은 식에 상첨자 $\mathrm{cat}$ 만 붙는다(host 가 유도 단계에
없었다는 (a)의 대입이 여기서 실현된다).

\textbf{(c) 중간식 — 중심과 온도 미분(이중 경로 교차검증).}
(b)를 $U_j^\mathrm{cat}$ 로 이항하면
\[
U_j^\mathrm{cat}(T)=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\Delta S_{\rxn,j}^\mathrm{cat}}{F}
\]
로, 흑연 식~\eqref{eq:Uj} 와 같은 함수형이다. 이 순간(고정 $T$)의 기울기는 두 독립 경로가 같은 값에 닿는다.
\emph{경로 1(직접 미분)}: 위 식에서 $\Delta H^\mathrm{cat}$·$\Delta S^\mathrm{cat}$ 를 그 $T$ 에서의 값으로
고정해 미분하면(식 자체가 $T$ 에 선형이라) $\partial U_j^\mathrm{cat}/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$.
\emph{경로 2(Gibbs 항등식 경유)}: 등압 Gibbs 항등식 $\partial\Delta G_j/\partial T|_P=-\Delta S_{\rxn,j}^\mathrm{cat}$
(식~\eqref{eq:gibbsdef} $G\equiv H-TS$ 의 $(\partial G/\partial T)_P=-S$ 로부터, $\Delta S$ 의 $T$-의존 여부와
\emph{무관}하게 항상 성립하는 정확한 열역학 항등식)와 식~\eqref{eq:eqcond} 의 $\Delta G_j=-FU_j$ 를 미분한
$\partial\Delta G_j/\partial T=-F\,\partial U_j^\mathrm{cat}/\partial T$ 를 등치하면
\[
-F\,\frac{\partial U_j^\mathrm{cat}}{\partial T}=-\Delta S_{\rxn,j}^\mathrm{cat}
\ \Longrightarrow\
\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
두 경로 어디에도 host 구분 항이 없다 — 이것이 ``전극 불문''의 수식적 의미다. \textbf{★경로 1 의 적용 범위.}
경로 1 은 그 $T$ 에서의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 값을 \emph{상수로 대입한} 순간 기울기다 — 만약
$\Delta S_{\rxn,j}^\mathrm{cat}(T)$ 자체가 $T$ 의 함수(전자항처럼 $\propto T$, \S\ref{sec:lco-Se})라면, 닫힌식
$U=(-\Delta H+T\Delta S(T))/F$ 를 \emph{기계적으로} 미분하면 $\Delta S(T)+T\,\dd\Delta S/\dd T$ 라는 여분 항이
생겨 경로 2 의 정확한 항등식과 어긋난다(경로 2 는 $\Delta S$ 의 $T$-의존과 무관하게 항상 성립하는 반면, 경로 1
의 "닫힌식 전체 미분" 버전은 $\Delta S$ 가 진짜 상수일 때만 경로 2 와 일치). 두 경로가 실제로 일치하는 것은
"그 온도에서의 순간 기울기"라는 좁은 의미에서다 — 온도에 따라 변하는 $\Delta S_{\rxn,j}^\mathrm{cat}(T)$ 아래
\emph{위치} $U_j^\mathrm{cat}(T)$ 를 구하려면 이 순간 기울기를 적분해야 한다(아래 (d) 말미).

\textbf{(d) 박스 — LCO 양극 중심과 온도 계수.}
\begin{equation}
\boxed{\;
U_j^\mathrm{cat}(T)=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\Delta S_{\rxn,j}^\mathrm{cat}}{F},
\qquad
\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}
\quad(j\in\mathcal J_\mathrm{LCO})\;}
\label{eq:lco-dUdT}
\end{equation}
관계식은 흑연 식~\eqref{eq:Uj} 와 부호까지 1:1 이고 바뀌는 것은 값뿐이다 — 양극의 높은 중심
($\sim$3.9--4.2 V)은 분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양인 데서 오고, $\Delta S_{\rxn,j}^\mathrm{cat}$
는 \S\ref{sec:lco-decomp}(식~\eqref{eq:lco-decomp})에서 config$\cdot$vib$\cdot$전자 세 성분으로 분해된다.
대표 단전극 계수 $\dd\phi/\dd T\approx+0.83$ mV/K 는 $F\times0.83\times10^{-3}\approx+80$ J/(mol\,K) 의
\emph{전체 단전극 스케일}[tier B]로 역산되며, 이는 표~\ref{tab:lco-staging} 의 \emph{전이별 성분}값
(config $\Delta S$ 등)과 서로 다른 층위의 양이라 직접 비교하지 않는다(층위 분리 시 T1 전자항의 소수 음의
보정과도 부호 충돌이 없다). \textbf{★다온도 전자항 주의(M-10 가드 인용).} $\Delta S_{e,j}(x,T)\propto T$ 인
항을 다온도 모델에 실제로 풀 때, 위 (c)의 정확한 순간 관계 $\partial U_j^\mathrm{cat}/\partial T=
\Delta S_{\rxn,j}^\mathrm{cat}(T)/F$ 를 \emph{그대로} 유지하면서 \emph{위치}는 기준온도에서 적분으로 얻어야
한다 — 이것이 \S\ref{sec:lco-Se} 의 식~\eqref{eq:U1T2}(★M-10 가드, $\tfrac12$ 인자 포함)가 이미 실행하는 바로
그 처방이며, 닫힌식을 기계적으로 재미분해 여분 항을 얻는 우를 범하지 않는다.
\[
U_j^\mathrm{cat}(T)=U_j^\mathrm{cat}(T_\mathrm{ref})+\frac1F\int_{T_\mathrm{ref}}^{T}\Delta S_{\rxn,j}^\mathrm{cat}(T')\,\dd T'.
\]
\textbf{(부호 좌표 고정.)} 아래 검산의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 는 반쪽반응을 \emph{삽입 방향}(Li$^+$
가 host 로 들어옴)으로 적은 반응 엔트로피이며(표~\ref{tab:staging} 흑연 삽입 규약과 동일 좌표), 단전극
potentiometric $\dd\phi/\dd T$ 의 부호는 측정 규약 의존이므로 아래 verifybox 는 그 대표 스케일을 삽입-반응
$\Delta S_{\rxn}^\mathrm{cat}$ 로 환산해 크기$\cdot$부호 sanity 만 확인한다.
```

### 1.5 자기검수 (재유도 근거)
| 검사 | 결과 |
|---|---|
| 부호 | $\Delta G_j=-FU_j$·$\Delta G=\Delta H-T\Delta S$ 대입 부호 재계산 일치, 발열/흡열 방향 확인 |
| 차원 | $[\Delta H]=$J/mol, $[T\Delta S]=$J/mol, $[F]=$C/mol $\Rightarrow[U]=$V. 전 항 일치 |
| 극한 | $T\to0$: $U_j^\mathrm{cat}\to-\Delta H^\mathrm{cat}/F$(순수 엔탈피 극한, 흑연과 동형) |
| 이중경로 일치 | 직접미분=Gibbs경유, 단 "$\Delta S$ 순간값 고정" 전제 하에서만(★위 (c) 말미로 명시 보강) |
| 이중계산 | 없음 — 이 절은 $U_j^\mathrm{cat}(T)$ 위치식만 다루고 $\Delta S^\mathrm{cat}$ 의 내부 분해는 §sec:lco-decomp 로 위임 |
| 앞 절 정합 | `eq:eqcond`·`eq:Ujmid`·`eq:Uj`(§sec:center, 불가침) 를 참조만 하고 값·부호 재유도 없이 그대로 인용 |
| M-10 가드 | 훼손 없음 — 인용만, `eq:U1T2` 정의는 `sec:lco-Se`(불가침)에 그대로 둠 |

### 1.6 신설 라벨
| 라벨 | 지위 | 충돌 검증 |
|---|---|---|
| `eq:lco-n0sub` | 신설 | grep `No matches found` |
| `eq:lco-dUdT` | **재사용(필수)** | 6개 `\eqref` 하류 참조(§0.1) — 라벨 변경 금지 |

---

## 2. `sec:lco-hys` — LCO order–disorder 와 MIT 2상역

### 2.1 위치
**교체 L697–719**. L696 헤더·L722 `sec:width` 인접 보존.

### 2.2 원 줄글 대비
원문(L697–719)은 "같은 정규용액 틀이 그대로 적용된다"를 T2·T3·T1·도핑 네 문단에서 **각각 서술로만** 반복한다 — $\mu(\theta)\to g''\to$ spinodal $\to\Delta U^\hys$ 의 흑연 유도 사슬(식~\eqref{eq:mu}–\eqref{eq:Ubranch})을 LCO 값으로 실제 대입한 중간식이 **한 줄도 없다**(V1010 STYLE_REPORT §1: "Ω_j spinodal 대입 중간식 전무").

### 2.3 계승 방침
`V1011_P11_map_v10.md` §2 골격을 계승·재검증한다. 독립 재유도(아래) 결과 spinodal 대수·$\Delta U^\hys$ 닫힌식은 **전부 정확**(부호까지 일치) — 채택. 원 map 의 "LCO 3/3 = 상분리 후보(고정 아님, 최종 판정은 피팅된 $\Omega_j^\mathrm{cat}>2RT$ 여부)" 완화 프레이밍도 재확인해 유지한다(도핑 시 $\Omega_j^\mathrm{cat}\le2RT$ 로 내려가는 케이스와 상충 없음).

### 2.4 수식 사슬 (재유도 검증 완료)

```latex
\textbf{(a) 출발 — LCO 세 전이를 같은 정규용액 자유에너지에.}
\S\ref{sec:hys} 의 격자기체 화학퍼텐셜 식~\eqref{eq:mu} 와 자유에너지 식~\eqref{eq:gxi} 는 ``동등한
자리에 리튬이 차고 빈다''는 가정 하나만 쓴다 — 이 가정은 LCO $\mathrm{Li}_x\mathrm{CoO_2}$ 의 팔면체 리튬
자리에도 문자 그대로 성립한다(자리당 점유 0 또는 1). 따라서 LCO 전이 집합
\begin{equation}
\mathcal J_\mathrm{LCO}=\{1:\mathrm{MIT},\ 2:\mathrm{OD}_a,\ 3:\mathrm{OD}_b\}
\label{eq:lco-J}
\end{equation}
의 각 전이 $j$ 에 진행률 $\xi_j$ 를 달아 흑연과 같은 정규용액 몫을 쓴다:
\begin{equation}
g_j^\mathrm{cat}(\xi_j)=g_{0,j}^\mathrm{cat}
+RT\{\xi_j\ln\xi_j+(1-\xi_j)\ln(1-\xi_j)\}+\Omega_j^\mathrm{cat}\,\xi_j(1-\xi_j).
\label{eq:lco-gxi}
\end{equation}
새 물리는 넣지 않는다 — LCO 로 바뀌는 것은 전이별 입력값 $U_j^\mathrm{cat},\Omega_j^\mathrm{cat},
\gamma_j,h_{\eta,j}$ 뿐이다.

\textbf{★two-phase calibration.} 흑연에서 spinodal 문턱 $\Omega_j>2RT$($2RT\approx4958$ J/mol@298 K,
식~\eqref{eq:spinodal})를 피팅 후 유지하는 것은 네 staging 전이 중 $2\mathrm L\!\to\!2$(LiC$_{12}$)$\cdot$
$2\!\to\!1$(LiC$_6$) \emph{두 개}뿐이고, dilute$\to$stage4$\cdot$$4\mathrm L\!\leftrightarrow\!3\mathrm L$ 은
$\Omega_j<2RT$ 로 내려가 solid-solution 이 된다(\S\ref{sec:width}$\cdot$\S\ref{sec:broadening}). LCO 는 이와
달리 pure-LCO 초기값에서 T1(MIT)$\cdot$T2$\cdot$T3(order--disorder) \emph{세 전이 전부}가 문턱을 넘는
상분리 \emph{후보}다(표~\ref{tab:lco-staging}). 곧 흑연 ``4 중 2''$\leftrightarrow$LCO ``3 중 3(후보)''로
대응 전이 집합만 다르고 문턱 판정 식 $\Omega_j^\mathrm{cat}>2RT$ 자체는 동일하며, 각 전이의 실제 gap 유무는
최종적으로 \emph{피팅된} $\Omega_j^\mathrm{cat}$ 이 $2RT$ 를 넘는지가 정한다(도핑 시 $\Omega_j^\mathrm{cat}
\le2RT$ 로 내려가는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다, 아래 도핑 문단).

\textbf{(b) 연산 — 곡률과 spinodal 문턱.}
식~\eqref{eq:lco-gxi} 를 두 번 미분하면 흑연 식~\eqref{eq:gpp} 에 전이별 $\Omega_j^\mathrm{cat}$ 만 든다:
\begin{equation}
\frac{\partial^2 g_j^\mathrm{cat}}{\partial\xi_j^2}=\frac{RT}{\xi_j(1-\xi_j)}-2\Omega_j^\mathrm{cat}.
\label{eq:lco-gpp}
\end{equation}
따라서 spinodal 은
\begin{equation}
\xi_{s,j}^{\pm}=\tfrac12\big(1\pm u_j^\mathrm{cat}\big),\qquad
u_j^\mathrm{cat}=\sqrt{1-\frac{2RT}{\Omega_j^\mathrm{cat}}}\qquad(\Omega_j^\mathrm{cat}>2RT),
\label{eq:lco-spinodal}
\end{equation}
이고 $\Omega_j^\mathrm{cat}\le2RT$ 이면 $u_j^\mathrm{cat}$ 이 실수가 아니라 그 전이의 spinodal gap 은 없다
(흑연 코드 분기 \code{if Omega <= 2RT: return 0.0} 그대로 재사용).

\textbf{(c) 중간식 — LCO 전위 곡선에 spinodal 대입.}
LCO 전이 $j$ 의 평형 전위 곡선은 식~\eqref{eq:Veq} 에 $U_j^\mathrm{cat},\Omega_j^\mathrm{cat}$ 를 넣어
\begin{equation}
V_{\eq,j}^\mathrm{cat}(\xi)=U_j^\mathrm{cat}
+\frac{RT}{F}\ln\frac{\xi}{1-\xi}+\frac{\Omega_j^\mathrm{cat}}{F}(1-2\xi),
\label{eq:lco-Veq}
\end{equation}
이고 두 spinodal 끝점에서 $\dfrac{\xi}{1-\xi}\big|_{\xi_{s,j}^\pm}=\dfrac{1\pm u_j^\mathrm{cat}}{1\mp
u_j^\mathrm{cat}}$, $(1-2\xi)\big|_{\xi_{s,j}^\pm}=\mp u_j^\mathrm{cat}$ 이므로 극대$-$극소 차는(흑연
식~\eqref{eq:hysdiff} 의 대입 그대로)
\[
\Delta U_{j}^{\hys,\mathrm{cat}}=V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^-)-V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^+)
=\frac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\mathrm{artanh}\,u_j^\mathrm{cat}\big].
\]
상수 중심 $U_j^\mathrm{cat}$ 는 차에서 상쇄된다.

\textbf{(d) 박스 — LCO 전이별 gap 과 분기 중심.}
\begin{equation}
\boxed{\;
\Delta U_j^{\hys,\mathrm{cat}}(T)=
\begin{cases}
\dfrac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\mathrm{artanh}\,u_j^\mathrm{cat}\big],
& \Omega_j^\mathrm{cat}>2RT,\\[4pt]
0, & \Omega_j^\mathrm{cat}\le2RT,
\end{cases}
\quad u_j^\mathrm{cat}=\sqrt{1-\dfrac{2RT}{\Omega_j^\mathrm{cat}}}\;}
\label{eq:lco-dUhys}
\end{equation}
\begin{equation}
\boxed{\;
U_j^{\,d,\mathrm{cat}}=U_j^\mathrm{cat}
+\tfrac12\sigma_d h_{\eta,j}\gamma_j\,\Delta U_j^{\hys,\mathrm{cat}}(T)\;}
\label{eq:lco-Ubranch}
\end{equation}
흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 대입형이다 — ``같은 틀''은 식을 생략한다는 뜻이
아니라 $\Omega_j\mapsto\Omega_j^\mathrm{cat}$, $U_j\mapsto U_j^\mathrm{cat}$, $j\in\mathcal J_\mathrm{LCO}$
를 실제로 넣는다는 뜻이다. \textbf{★주의 — $\gamma_j,h_{\eta,j}$ 는 흑연에서와 마찬가지로 여기서도
\emph{유도되지 않는} 방향별 한 자유도의 현상학적 축소 인자다}(\S\ref{sec:hys} (b)(c) 의 원 서술과 동일
지위 — 두 endpoint 의 대칭 평균 $U_j^\mathrm{cat}$(식~\eqref{eq:hyssym} 형)까지는 엄밀히 유도되나, 그
너머 실측 분기를 한 자유도로 접는 것은 모델 가정이다). 방전($\sigma_d=+1$)은 분기 중심을 위로, 충전
($\sigma_d=-1$)은 아래로 옮긴다.

\textbf{(T2$\cdot$T3) order--disorder.}
$x\approx0.5$ 부근 monoclinic 초격자(점유 Li 와 빈자리의 교대 정렬)를 이루는 T2($\sim$4.05 V,
hex$\to$monoclinic)$\cdot$T3($\sim$4.17--4.20 V, monoclinic$\to$hex)는 동종 이웃 인력 $\Omega_j^\mathrm{cat}>0$
이 만드는 상분리의 LCO 사례다. 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j=2,3$ 을 넣으면
T2$\cdot$T3 각각 열린다. \textbf{★$\Omega$ 와 config $\Delta S$ 의 구분(혼동 가드).} 정렬의 charge-order
엔트로피 변화($\approx0.47$ J/(mol\,K)@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$
[tier A, Motohashi\cite{motohashi2009}])는 \emph{엔트로피} 값으로 표~\ref{tab:lco-staging}$\cdot$
식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 슬롯(따라서 $U_j^\mathrm{cat}(T)$ 의 온도 이동)에
들어가지, spinodal 문턱을 정하는 \emph{상호작용 에너지} $\Omega_j^\mathrm{cat}$[J/mol]가 \emph{아니다} —
둘은 단위(J/(mol K) vs J/mol)부터 다른 별개 양이므로 ``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 식의 다리를
놓아선 안 되고 $\Omega_j^\mathrm{cat}$ 는 gap 을 정하는 별도 피팅 파라미터로 \emph{기호로만} 둔다(수치 날조
금지).

\textbf{(T1) MIT 2상역.}
T1($\sim$3.90 V, $x\approx0.94$--$0.75$, 절연체$\to$금속)의 구조적 2상 공존도 같은 정규용액 문턱을 받는다
— $u_1^\mathrm{cat},\Delta U_1^{\hys,\mathrm{cat}},U_1^{\,d,\mathrm{cat}}$ 이 식~\eqref{eq:lco-dUhys}$\cdot$
\eqref{eq:lco-Ubranch} 에 $j=1$ 로 그대로 열린다. MIT 고유의 전자 자유도는 이 히스 gap 에 새 항으로 섞지
않는다 — 그 항은 이미 $\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^\mathrm{mol}(x,T)$(식~\eqref{eq:lco-decomp})를 통해 $U_1^\mathrm{cat}(T)$ 의 온도 이동
(식~\eqref{eq:lco-dUdT})에 들어간다. 곧 두 몫이 서로 다른 슬롯에 산다:
\begin{equation}
\boxed{\;
\underbrace{\Delta U_1^{\hys,\mathrm{cat}}\ \text{(구조적 2상역)}\ \Leftarrow\ \Omega_1^\mathrm{cat}}_{\text{정규용액 히스 gap (이 절)}}
\quad\Big\|\quad
\underbrace{\partial U_1^\mathrm{cat}/\partial T\ \Leftarrow\ \Delta S_{e,1}^\mathrm{mol}(x,T)}_{\text{전자 엔트로피 (\S\ref{sec:lco-electronic})}}\;}
\label{eq:lco-mit}
\end{equation}
이 분리가 config 2상역과 전자 엔트로피를 이중계산하지 않는 경계다(원문 "MIT 의 구조적 2상역은 정규용액
틀로, 전자 자유도는 별도 항으로" 서술을 슬롯 식으로 못박음).

\textbf{도핑 보정(우리 시료).}
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox$\cdot$전자항을 보존하되 order--disorder$\cdot$MIT 상전이를
억제한다 — 정규용액 틀에서 이는 pure-LCO 초기값 $\Omega_j^\mathrm{cat,pure}$ 를 도핑 피팅값
$\Omega_j^\mathrm{cat,dop}$ 로 낮추는 입력 변화다. 식~\eqref{eq:lco-dUhys} 의 문턱 극한은
\begin{equation}
\Omega_j^\mathrm{cat,dop}\to2RT^+\ \Longrightarrow\
u_j^\mathrm{cat,dop}\to0,\quad
\Delta U_j^{\hys,\mathrm{cat,dop}}\to\frac{8RT}{3F}\big(u_j^\mathrm{cat,dop}\big)^3\to0,
\label{eq:lco-dope}
\end{equation}
(흑연 식~\eqref{eq:dUhys} 아래 Taylor 극한의 재사용, $\mathrm{artanh}\,u=u+u^3/3+\cdots$, $T_{c,j}=
\Omega_j^\mathrm{cat}/2R$)이고, $\Omega_j^\mathrm{cat,dop}\le2RT$ 로 피팅되는 전이는 같은 식 안에서 gap 이
0 으로 닫힌다 — 이것이 상전이 억제에 따른 히스 축소와 peak smear 의 수식 표현이며, 풀린 몫은
\S\ref{sec:broadening} 의 broadening 폭이 더 크게 담는다. \textbf{★슬롯 분리.} 중심 전위의 미세 shift 는
같은 전이 dict 의 $U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로} 들어가며, $\Omega_j^\mathrm{cat}$ 하나가
gap$\cdot$smear 와 중심 이동을 동시에 만든다고 쓰지 않는다(흑연 \code{GRAPHITE\_STAGING\_LIT} 가 초기값이고
폭이 피팅 대상이었듯, pure-LCO $\Omega_j^\mathrm{cat}$ 가 초기값이고 폭$\cdot$shift 는 우리 데이터로 피팅).
```

### 2.5 자기검수 (재유도 근거)
| 검사 | 결과 |
|---|---|
| 대수 재유도 | $g_j''=0\Rightarrow\xi(1-\xi)=RT/2\Omega\Rightarrow\xi_s^\pm=\tfrac12(1\pm u)$ 직접 재계산, 흑연 §sec:hys 결과와 정확 일치 |
| $\Delta U^\hys$ 대입 | $\xi_s^\pm$ 두 값을 $V_\eq^\mathrm{cat}(\xi)$ 에 넣어 차분 → $-4RT/F\cdot\mathrm{artanh}\,u+2\Omega u/F$ 재도출, artanh 항등식($\mathrm{artanh}\,u=\tfrac12\ln\tfrac{1+u}{1-u}$) 사용 확인 |
| 부호 | $\Delta U^\hys\ge0$(극대>극소), $\Omega\to2RT^+$ 에서 $u\to0\Rightarrow\Delta U^\hys\to0$(연속) 확인 |
| 차원 | $\Omega_j^\mathrm{cat}$[J/mol], $u_j^\mathrm{cat}$ 무차원, $\Delta U^\hys$[V] — 전 항 일치 |
| 이중계산 | eq:lco-mit 박스로 히스 gap(구조 2상)과 전자 엔트로피(온도이동) 슬롯 분리 명시 — 겹침 없음 |
| Ω↔configΔS 혼동 | 단위(J/mol vs J/(mol·K))로 재확인, 0.47/1.49 는 config ΔS 로만 사용(수치 날조 0) |
| 근사 정직성 | $\gamma_j,h_{\eta,j}$ 는 "유도"가 아니라 "모델 가정"으로 명시(원 흑연 절과 동일 지위 유지 — 과대 승격 방지) |
| 앞 절 정합 | §1 의 `eq:lco-dUdT`·`eq:lco-decomp` 참조와 모순 없음(eq:lco-mit 이 그 경계를 명시) |

### 2.6 신설 라벨
| 라벨 | 충돌 검증 |
|---|---|
| `eq:lco-J` | grep `No matches found` |
| `eq:lco-gxi` | grep `No matches found` |
| `eq:lco-gpp` | grep `No matches found` |
| `eq:lco-spinodal` | grep `No matches found` |
| `eq:lco-Veq` | grep `No matches found` |
| `eq:lco-dUhys` | grep `No matches found` |
| `eq:lco-Ubranch` | grep `No matches found` |
| `eq:lco-mit` | grep `No matches found` |
| `eq:lco-dope` | grep `No matches found` |

---

## 3. `sec:lco-peak` — LCO dQ/dV peak (세 봉우리)

### 3.1 위치
**교체 L1221–1232**. L1220 헤더 보존, L1234 `sec:broadening`(★흑연 본체, 불가침) 인접 경계만 확인.

### 3.2 원 줄글 대비
원문은 "평형 peak 식은 전극을 가리지 않으므로 LCO 에도 그대로 적용된다"고 서술하고 T1/T2/T3 위치를 **말로 열거**할 뿐, 세 전이를 실제로 합산한 **박스식이 없다**(V1010 STYLE_REPORT: "LCO 3전이 합산 peak 박스식 없음", 등급 "Major(★최약)"). $j$ 를 일반 기호로 두고 "전극 무관"이라 적는 것과, $j\in\{\mathrm{T1,T2,T3}\}$ 를 \emph{실제로 대입}해 셋을 합한 식을 보이는 것은 다르다 — 후자가 빠져 있었다.

### 3.3 수식 사슬 (신규 작성)

```latex
\textbf{(a) 출발 — 전극-무관 평형 peak 식.}
\S\ref{sec:eqpeak} 의 식~\eqref{eq:eqpeak}
$\big(\dd Q/\dd V\big)^\eq_j=Q_j\,\xi_{\eq,j}(1-\xi_{\eq,j})/w_j$
는 전하 보존식의 직접 미분(§sec:eqpeak (a)–(d))이며 어느 단계도 흑연 고유가 아니다 — 들어가는 것은
$\xi_{\eq,j}(V,T)$(식~\eqref{eq:xieq})와 $w_j$(식~\eqref{eq:wbase})뿐이고, 이 둘은 \S1–\S2 에서 이미
LCO 값 $U_j^{\,d,\mathrm{cat}},w_j^\mathrm{cat}$ 로 채워졌다.

\textbf{(b) 연산 — LCO 세 전이 대입.}
$j\in\{\mathrm{T1,T2,T3}\}=\mathcal J_\mathrm{LCO}$(식~\eqref{eq:lco-J})를 넣으면 각 전이의 평형 점유는
\[
\xi_{\eq,j}^\mathrm{cat}(V,T)=\frac{1}{1+\exp\!\big[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j^\mathrm{cat}\big]},
\qquad j=\mathrm{T1,T2,T3},
\]
이고(§1–§2 에서 채운 $U_j^{\,d,\mathrm{cat}}$·$w_j^\mathrm{cat}$ 를 그대로 대입), 종 항등식
$\dd\xi_{\eq,j}^\mathrm{cat}/\dd V=\sigma_d\,\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})/w_j^\mathrm{cat}$
(식~\eqref{eq:belliden} 그대로)이 각 전이에 독립적으로 성립한다.

\textbf{(c) 중간식 — 전이별 봉우리.} 보존식 미분에 넣으면 전이별 평형 peak 이
\begin{equation}
\Big(\frac{\dd Q}{\dd V}\Big)^{\eq,\mathrm{cat}}_j
=Q_j\,\frac{\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j^\mathrm{cat}},
\qquad j=\mathrm{T1,T2,T3},
\label{eq:lco-peakj}
\end{equation}
이고, 각 전이에서 위치$=U_j^{\,d,\mathrm{cat}}$, 순높이$=Q_j/(4w_j^\mathrm{cat})$($\xi=\tfrac12$ 에서 최대),
면적$=Q_j$ 로 읽힌다(§sec:eqpeak (d) 말미의 "세 양" 논증을 셋에 각각 적용).

\textbf{(d) 박스 — LCO 세 봉우리 합산.}
\begin{equation}
\boxed{\;
\Big(\frac{\dd Q}{\dd V}\Big)^{\mathrm{LCO},\eq}
=\sum_{j\in\{\mathrm{T1,T2,T3}\}}Q_j\,\frac{\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j^\mathrm{cat}}
\;}
\label{eq:lco-peaksum}
\end{equation}
이것이 ``LCO 하프셀은 양극 전위 영역에 세 봉우리를 남긴다''는 서술의 실제 닫힌식이다 — T1 의 $\sim$3.90 V
(MIT plateau), T2 의 $\sim$4.05 V, T3 의 $\sim$4.17--4.20 V(T2 와 한 쌍의 좁은 order--disorder 봉우리).

\textbf{폭의 지위.} 식~\eqref{eq:lco-peaksum} 의 $w_j^\mathrm{cat}$ 은 흑연과 같은 $w_j=n_jRT/F$
(식~\eqref{eq:wbase})이나, T1$\cdot$T2$\cdot$T3 모두 pure-LCO 초기값에서 $\Omega_j^\mathrm{cat}>2RT$ 의
두-상 \emph{후보}이므로(\S2 two-phase calibration) \S\ref{sec:width} 이중지위의 \emph{두-상} 측 —
평형 예측이 아니라 broadening 이 정하는 현상학적 자유 피팅 폭이다(\S\ref{sec:broadening}, 불가침 절 참조만
— 흑연-특정 구조무질서 근거는 옮기지 않고 LCO 는 일반 $\eta$ 분포로만 다룬다는 그 절 자신의 scope 제한을
그대로 받는다). order--disorder 의 큰 $\Omega_j^\mathrm{cat}$ 가 spinodal gap 을 키워 T2$\cdot$T3 의 분기를
흑연보다 날카롭게(좁은 한 쌍 peak 로) 만든다.

\textbf{T1 의 온도 이동 신호.} T1 의 위치는 \S\ref{sec:lco-electronic} 의 전자항이
$\Delta S_{\rxn,1}^\mathrm{cat}$ 를 통해 $U_1^\mathrm{cat}(T)$ 의 \emph{온도 이동}에 기여하므로
(식~\eqref{eq:lco-dUdT}), 다온도 식~\eqref{eq:lco-peaksum} 에서 T1 봉우리의 \emph{온도 이동률}
$\partial U_1^\mathrm{cat}/\partial T$ 가 $T$ 에 선형으로 커지는 것이 전자항의 관측 신호다
($\Delta S_{e,1}\propto T$, \S\ref{sec:lco-Se} — 위치 자체가 아니라 \emph{이동률}이 $T$-선형, 위치 이동은
$\propto T^2$, 식~\eqref{eq:U1T2}). 도핑은 \S2 대로 봉우리를 smear$\cdot$shift 시킨다.
```

### 3.4 자기검수 (재유도 근거)
| 검사 | 결과 |
|---|---|
| 전극-무관성 | eq:eqpeak 유도(§sec:eqpeak (a)–(d))를 재추적 — 전하보존 미분·종 항등식(eq:belliden) 어디에도 흑연 고유 입력 없음, LCO 대입 정당 |
| 합산 정당성 | eq:sum(§sec:sum, 불가침)의 "서로소 자리 분해" 전제와 동일 논리 — 세 전이가 서로 다른 조성창(T1: 0.94–0.75, T2: ≈0.55, T3: ≈0.48)에 있어 분해 전제 위반 없음 |
| 차원 | $[Q_j]=$C, $[w_j]=$V, $[\xi(1-\xi)]=$무차원 → $[\dd Q/\dd V]=$C/V 일치 |
| 극한 | $\xi_{\eq,j}\to0,1$ 에서 각 전이 기여 $\to0$(봉우리 양끝 소멸) — eq:belliden 종 모양 그대로 |
| 신규개념 금지 | ρ(U_app)·PSD 등 미도입 — 폭 지위는 §sec:broadening(불가침) 참조만, 재유도 X |
| 앞 절 정합 | §1(center)·§2(hys)의 $U_j^{\,d,\mathrm{cat}},w_j^\mathrm{cat}$ 를 입력으로만 받고 재정의하지 않음 |

### 3.5 신설 라벨
| 라벨 | 충돌 검증 |
|---|---|
| `eq:lco-peakj` | grep `No matches found` |
| `eq:lco-peaksum` | grep `No matches found` |

---

## 4. `sec:lco-decomp` — $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해 (config+vib+electronic)

### 4.1 위치
**교체 L1716–1754**(개념·수치·박스 라벨 `eq:lco-decomp` 계승, 유도만 형식화). L1715 헤더 보존.

### 4.2 원 줄글 대비
원문은 박스(`eq:lco-decomp`)는 이미 있으나, "왜 세 항을 단순히 더해도 되는가"(가산성)와 "왜 이중계산이 안 되는가"(무초과)를 **줄글 논증**으로만 편다(V1010 STYLE_REPORT: 등급 Moderate — 6개 중 가장 양호하나 "Z=Z_config·Z_elec→슬롯 정의→이중계산 금지식 박스"의 형식 유도가 없음). 본 절은 그 줄글 논증을 실제 분배함수 인수분해에서 출발하는 (a)–(d) 사슬로 형식화한다 — **박스 자체(`eq:lco-decomp`)의 물리·값·부호는 바꾸지 않는다.**

### 4.3 수식 사슬 (신규 형식화, 기존 박스 계승)

```latex
\textbf{(a) 출발 — 세 자유도의 (근사) 독립성.}
삽입 반응의 전체 엔트로피는 세 자유도의 결합계다 — Li 배열(config)$\cdot$격자 진동(vib)$\cdot$전도 전자
(electronic). 세 부분계가 \emph{근사적으로 독립}(선도 차수에서 결합 없음)이면 전체 분배함수는 곱으로
인수분해된다:
\begin{equation}
Z_\mathrm{total}(\beta,\mu)\;\approx\;Z_\mathrm{config}(\beta,\mu)\cdot Z_\mathrm{vib}(\beta)\cdot Z_\mathrm{elec}(\beta,\mu),
\label{eq:lco-Zfact}
\end{equation}
이 근사(★"$\approx$"이지 등호가 아님)의 타당성은 물리적 근거를 갖는다 — config(리튬 자리 \emph{배열}의
자유도)와 elec(전도 전자 \emph{밴드 점유}의 자유도)는 서로 다른 힐베르트 공간에 사는 자유도라 MIT 부근을
제외하면 결합이 작다(리튬 정렬과 전자 밴드채움이 다소 결합하나, 이 교차항은 선도 차수에서 무시된다 — 아래
(d)에서 재확인).

\textbf{(b) 연산 — 로그와 온도미분으로 자유에너지$\cdot$엔트로피의 합.}
식~\eqref{eq:lco-Zfact} 의 로그를 취하면 자유에너지가 합으로 갈라진다($F=-RT\ln Z$, 몰당):
$F_\mathrm{total}=F_\mathrm{config}+F_\mathrm{vib}+F_\mathrm{elec}$. 엔트로피는 자유에너지의 온도미분
($S=-\partial F/\partial T$, \S\ref{sec:lco-Se} (b)에서 이미 쓴 것과 같은 항등식)이므로 이 합도 그대로 넘어간다:
\begin{equation}
S_\mathrm{total}=S_\mathrm{config}+S_\mathrm{vib}+S_\mathrm{elec}.
\label{eq:lco-Sfact}
\end{equation}

\textbf{(c) 중간식 — 부분몰(삽입당) 미분과 슬롯 정의.}
삽입 1몰당 미분 $\Delta S_{\rxn,j}^\mathrm{cat}\equiv\partial S_\mathrm{total}/\partial x|_{T,j}$ 을 취하면
식~\eqref{eq:lco-Sfact} 이 그대로 세 부분몰 항의 합이 된다. 각 항에 \emph{슬롯 정의}를 매긴다 — 이것이
가산성(``더해도 되는가'')과 별개로 무이중계산(``과대 계상 없는가'')을 보장하는 규칙이다:
\begin{itemize}[leftmargin=1.4em,itemsep=1pt]
\item config 슬롯 $\Delta S_j^\mathrm{config}$ 에는 봉우리 \emph{중심 표준값}만 넣는다 — 봉우리
\emph{내부}의 조성 의존 $R\ln[(1-\xi)/\xi]$ 은 logistic 점유식(\S\ref{sec:dist})이 \emph{이미 자동
생성}하므로 슬롯에 또 넣지 않는다(Chapter 2 파생 B 와 동일 원리, \S\ref{ssec:overlap}·\S\ref{ssec:overlap}
경유 \S\ref{ssec:config}).
\item vib 슬롯 $\Delta S_j^\mathrm{vib}$ 는 고-$x$ phonon 음의 baseline 으로, 흑연과 동형 상수(별도 식 변화
없음).
\item elec 슬롯 $\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)$ 는 \S\ref{sec:lco-electronic} 의 몰당 닫힌식
(식~\eqref{eq:dSemolar}$\cdot$\eqref{eq:dSegate})을 그대로 대입 — MIT 창(T1)에만 국소.
\end{itemize}

\textbf{(d) 박스 — 세 성분의 합(기존 박스, 재확인).}
\begin{equation}
\boxed{\;\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=\underbrace{\Delta S_j^\mathrm{config}}_{\text{logistic }w=RT/F\text{ 가 담음}}
+\underbrace{\Delta S_j^\mathrm{vib}}_{\text{음의 baseline}}
+\underbrace{\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)}_{\text{MIT 게이트, 삽입 기준 }<0,\ \propto T}\;.}
\label{eq:lco-decomp}
\end{equation}
\textbf{가산성 vs 무이중계산(재확인, 두 종류의 다른 보장).} 식~\eqref{eq:lco-Zfact}--\eqref{eq:lco-Sfact}
의 (근사) 독립 인수분해가 ``더해도 되는가''(가산성)를 정당화하고, (c)의 슬롯 정의(각 항이 자기 자유도의
\emph{몫만} 채움)가 ``과대 계상 없는가''(무이중계산)를 보장한다 — 이 둘은 \emph{서로 다른 질문에 대한
서로 다른 보장}이다: 가산성이 성립해도 슬롯을 잘못 정의하면(예: config 슬롯에 봉우리 내부 항까지 또 넣으면)
이중계산이 생기고, 반대로 슬롯이 옳아도 세 자유도가 강하게 결합해 있으면(교차항이 크면) 단순 합 자체가
틀린다. 본 절은 두 조건이 \emph{둘 다} MIT 를 제외한 대부분의 조성 창에서 성립함을(교차항 선도차수 무시,
슬롯 정의 명시) 근거로 삼는다 — MIT 창 안에서 리튬 정렬$\cdot$전자 밴드채움의 결합이 완전히 0 은 아니나,
그 잔차는 통제(제거)되는 것이 아니라 \emph{선도 차수에서 무시}되며, 이는 정밀 round-trip 피팅 단계에서
잔차로 남을 수 있는 공백으로 정직하게 열어 둔다(허위 정밀 금지).
```

### 4.4 자기검수 (재유도 근거)
| 검사 | 결과 |
|---|---|
| 근사 정직성(★핵심) | (a)의 $Z\approx Z_\mathrm{config}Z_\mathrm{vib}Z_\mathrm{elec}$ 를 **등호가 아니라 근사**로 명시 — 원문의 "근사적으로 직교" 서술을 삭제·과장(등호)하지 않고 그대로 보존, MIT 결합 잔차를 정직하게 남김 |
| 두 보장의 구분 | 가산성(독립 인수분해)과 무이중계산(슬롯 정의)을 명시적으로 분리 — 원문의 "(가)(나)" 논증 구조를 형식 유도 안에 흡수 |
| 차원 | 세 항 전부 J/(mol·K), 합산 후 단위 불변 |
| 부호 | config: 봉우리 양끝 $\pm\infty$/중심 0(§sec:dist 로부터), vib: 고-x 음, elec: MIT 국소 음(삽입기준) — 원 서술과 완전 일치, 수치 변경 없음 |
| 박스 값 불변 | `eq:lco-decomp` 수식·라벨·물리 내용 **원문 그대로 재사용** — 유도만 앞에 형식화해 붙임 |
| 앞 절 정합 | §1 의 `eq:lco-dUdT`(온도미분 관계)·§2 의 `eq:lco-mit`(전자항 슬롯 분리 경계)와 모순 없음 — 오히려 eq:lco-mit 의 슬롯 분리를 §sec:lco-Se 표기로 재확인 |

### 4.5 신설 라벨
| 라벨 | 지위 | 충돌 검증 |
|---|---|---|
| `eq:lco-Zfact` | 신설 | grep `No matches found` |
| `eq:lco-Sfact` | 신설 | grep `No matches found` |
| `eq:lco-decomp` | **재사용(필수)** | 11개 `\eqref` 하류 참조(§0.1) — 라벨·물리 내용 불변 |

---

## 5. 전자항 plug-in — 좌표 매핑 ($x\leftrightarrow\xi_{\eq,1}(V)$) forward 사슬

### 5.1 위치
**교체 L1756–1765**("★Ch2/P4 코드 구현 예고" 문단 전체). L1755·L1766 공백줄 경계.

### 5.2 원 줄글 대비
원문은 "T1 전이의 진행률 $\xi_{\eq,1}(V)$ 이 그 전이 구간의 정규화 조성에 대응하므로, 게이트 인자에
$x=x(\xi_{\eq,1}(V))$ 를 대입해 $V$ 격자 위에서 $\Delta S_e$ 를 평가한다"고 **서술만** 한다 — 실제 매핑
함수 $x(\xi)$ 의 닫힌식이 없다(V1010 STYLE_REPORT: "필요한 수식 사슬 = $x=x(\xi_{\eq,1}(V))\to
\Delta S_{e,1}(V,T)\to\Delta S_{\rxn,1}(V,T)\to U_1(T)\to$ dQ/dV forward 사슬", 등급 Major).

### 5.3 수식 사슬 (신규 작성)

```latex
\textbf{(a) 출발 — 좌표 불일치.} 전자 게이트(식~\eqref{eq:ggate}$\cdot$\eqref{eq:dSegate})는 조성 $x$ 의
함수이나, forward 코드의 $\xi_{\eq,j}(V,T)$ 는 전위 $V$ 격자 위에서 산다(\S\ref{sec:width}). $\Delta S_e$
를 실제로 $V$ 격자 위에서 평가하려면 $x\leftrightarrow V$ 다리가 필요하다.

\textbf{(b) 연산 — T1 구간의 조성-진행률 아핀 사상.} 표~\ref{tab:lco-staging} 의 T1 조성 구간은
$x_\mathrm{hi}=0.94$(진행 시작, $\xi_{\eq,1}=0$)에서 $x_\mathrm{lo}=0.75$(진행 끝, $\xi_{\eq,1}=1$)로
줄어든다(탈리튬화 방향, \S\ref{sec:lco-map} 의 ``LCO 충전$=\xi:0\to1$'' 규약과 일치). T1 \emph{한 전이}
내부는 단일 반응 진행이므로, 그 구간 안에서 조성과 진행률을 \emph{선형}으로 잇는 것이 가장 단순한 사상이다
(★이는 \emph{모델 가정}이지 유도된 결과가 아니다 — 실제 $x$-$\xi$ 관계가 그 좁은 2상 창 안에서 정확히
선형이라는 독립 근거는 없다; 아래 (d) 말미에서 다시 명시):
\begin{equation}
x(\xi_{\eq,1})=x_\mathrm{hi}-(x_\mathrm{hi}-x_\mathrm{lo})\,\xi_{\eq,1}(V,T)
=0.94-0.19\,\xi_{\eq,1}(V,T).
\label{eq:lco-xmap}
\end{equation}

\textbf{(c) 중간식 — 게이트 인자의 합성.} 식~\eqref{eq:lco-xmap} 을 게이트 인자 $z=(x-x_\mathrm{MIT})/
\Delta x_\mathrm{MIT}$(식~\eqref{eq:ggate})에 대입하면 $z$ 가 $(V,T)$ 의 명시 함수가 된다:
\begin{equation}
z(V,T)=\frac{x\big(\xi_{\eq,1}(V,T)\big)-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}},
\label{eq:lco-zmap}
\end{equation}
이를 닫힌식~\eqref{eq:dSegate} 에 넣으면
\begin{equation}
\Delta S_{e,1}(V,T)=-\frac{\pi^2}{3}k_B^2T\,\frac{g_\max}{\Delta x_\mathrm{MIT}}\,
\sigma\!\big(z(V,T)\big)\big[1-\sigma\!\big(z(V,T)\big)\big],
\label{eq:lco-Se1VT}
\end{equation}
이제 $\Delta S_{e,1}$ 이 $V$ 격자 위의 값으로 평가 가능하다(코드 구현은 별도 상태 변수 없이 이미 계산된
$\xi_{\eq,1}(V,T)$ 를 재사용하는 것으로 충분 — 신규 자유도 0).

\textbf{(d) 박스 — plug-in forward 사슬 닫기.} 식~\eqref{eq:lco-Se1VT} 의 $\Delta S_{e,1}(V,T)$ 를
몰당 환산($N_A$ 배, 식~\eqref{eq:dSemolar})해 식~\eqref{eq:lco-decomp} 의 T1 슬롯에 더하고, 그 합을
식~\eqref{eq:lco-dUdT}(§1)의 $\Delta S_{\rxn,1}^\mathrm{cat}$ 자리에 넣어 $U_1^\mathrm{cat}(T)$ 의 온도
이동에 plug-in 하면, 식~\eqref{eq:lco-peaksum}(§3)의 T1 봉우리가 그 이동을 반영한다:
\begin{equation}
\boxed{\;
x\big(\xi_{\eq,1}(V,T)\big)\ \xrightarrow{\eqref{eq:lco-zmap}}\ z(V,T)
\ \xrightarrow{\eqref{eq:lco-Se1VT}}\ \Delta S_{e,1}(V,T)
\ \xrightarrow{N_A,\ \eqref{eq:lco-decomp}}\ \Delta S_{\rxn,1}^\mathrm{cat}(V,T)
\ \xrightarrow{\eqref{eq:lco-dUdT}}\ U_1^\mathrm{cat}(T)
\ \xrightarrow{\eqref{eq:lco-peaksum}}\ \Big(\frac{\dd Q}{\dd V}\Big)^{\mathrm{LCO},\eq}_\mathrm{T1}
\;}
\label{eq:lco-plugin}
\end{equation}
이 사슬이 ``전자 엔트로피 항 plug-in''의 전체 forward 경로다 — 새 자유도(별도 상태변수)를 늘리지 않고
기존 $\xi_{\eq,1}(V,T)$ 를 좌표로 재사용한다는 것이 (b)의 요지다.

\textbf{★round-trip 가드(확인 가능한 조건).} 식~\eqref{eq:lco-decomp} 의 config 중심 표준값 $\Delta S_j^0$
(Motohashi\cite{motohashi2009} $\approx0.47/1.49$ J/(mol\,K), T2/T3)은 아직 round-trip 으로 실증되지 않은
\emph{초기값}이다(신뢰값 아님, tier A 는 출처 문헌 값에 대해서만 — 우리 시료에서의 재현은 미확인). 흑연
$\Delta S_\rxn{=}-16$ J/(mol\,K) 의 round-trip 절차(\S\ref{sec:center} \code{codebox})와 동격의 확인 가능한
조건으로 명시하면:
\[
\big|U_1^\mathrm{cat}(T_0{=}298.15\text{K})_\mathrm{model}-3.90\text{ V}\big|<\epsilon_U
\quad\text{그리고}\quad
\mathrm{sign}\Big[\frac{\partial U_1^\mathrm{cat}}{\partial T}\Big]_\mathrm{model}
=\mathrm{sign}\big[\Delta S_{\rxn,1}^\mathrm{cat}(T_0)\big]_\mathrm{fit}
\]
가 성립해야 표~\ref{tab:lco-staging}$\cdot$식~\eqref{eq:lco-decomp} 의 초기값이 신뢰값으로 승격된다
($\epsilon_U$ 는 피팅 허용오차, 사용자 지정). 이 검증 전에는 config 표준값을 결과 해석의 근거로 쓰지
않는다(허위 정밀 금지).
```

### 5.4 자기검수 (재유도 근거)
| 검사 | 결과 |
|---|---|
| 좌표 매핑 방향 | $\xi_{\eq,1}=0\to x=0.94$(절연체 시작), $\xi_{\eq,1}=1\to x=0.75$(금속 쪽 끝) — §sec:lco-map 의 "LCO 충전=탈리튬화=ξ:0→1" 규약, §sec:lco-why 의 "탈리튬화로 x가 0.94 아래로 내려가면 금속" 서술과 방향 일치 재확인 |
| 모델 가정 정직성(★핵심) | (b)의 선형 사상은 **유도가 아니라 가정**임을 (b)·(d) 두 곳에서 명시 — 코너케이스를 메인으로 승격하지 않음(원칙 준수) |
| 신규 자유도 | 0 — $x(\xi_{\eq,1})$ 는 이미 계산된 $\xi_{\eq,1}(V,T)$ 의 재표현일 뿐, 별도 상태변수 도입 없음(원문 "별도 상태 변수 또는 전이 진행률 매핑" 중 후자를 명시적으로 채택) |
| M-10 가드 정합 | plug-in 사슬의 (d) 는 $\Delta S_{\rxn,1}^\mathrm{cat}(V,T)$ 를 §1 `eq:lco-dUdT`(순간 관계)에 넣는다고만 적고, \emph{위치} $U_1(T)$ 계산은 §1 (d) 말미가 지정한 적분형(eq:U1T2)에 위임 — 기계적 재미분 오류를 이 사슬도 반복하지 않음 |
| round-trip 가드 | "적절해 보임" 류 정성 판단이 아니라 확인 가능한 부등식·부호일치 조건으로 서술(게이트 설계 원칙 부합) |
| 앞 절 정합 | §1(eq:lco-dUdT)·§2(eq:lco-mit)·§3(eq:lco-peaksum)·§4(eq:lco-decomp) 를 전부 참조하는 통합 사슬 — 순서·라벨 충돌 없음 |

### 5.5 신설 라벨
| 라벨 | 충돌 검증 |
|---|---|
| `eq:lco-xmap` | grep `No matches found` |
| `eq:lco-zmap` | grep `No matches found` |
| `eq:lco-Se1VT` | grep `No matches found` |
| `eq:lco-plugin` | grep `No matches found` |

---

## 6. `sec:lco-code` — MSMR 동형 재유도 + 전이 파라미터 교체

### 6.1 위치
**교체 L1768–1792**. L1767 헤더 보존, L1794 `\subsection{전체 입력 인자...}`(공통 절, 비-LCO 전용) 경계 확인.

### 6.2 원 줄글 대비
원문은 MSMR 식(eq:msmr)과 Ch1 logistic(eq:xieq)의 대응표($X_j\leftrightarrow Q_j$ 등)를 제시하고 "구조가
동형이다"라고 **선언**하지만, 그 동형성을 실제로 대입해 두 식이 \emph{같은 식}이 됨을 보이는 단계가 없다
(V1010 STYLE_REPORT: "MSMR→ξ_eq,j→eqpeak 변환 사슬 미폐쇄", 등급 Moderate). 대응표는 "이런 사전이 있다"이지
"이 사전을 넣으면 두 식이 항등이 된다"가 아니다 — 아래 사슬이 그 간극을 닫는다.

### 6.3 수식 사슬 (신규 작성 — 동형성의 실제 증명)

```latex
\textbf{(a) 출발 — 두 논문의 평행한 logistic.} multiphase species reaction(MSMR) 모델\cite{msmr2024}은
양극 전위를 전이별 logistic 의 합으로 적는다:
\begin{equation}
x_j=\frac{X_j}{1+\exp[\,f(U-U_j^0)/\omega_j\,]},
\label{eq:msmr}
\end{equation}
이는 Ch1 의 전이-logistic 식~\eqref{eq:xieq}
($\xi_{\eq,j}=1/(1+\exp[-\sigma_d(V-U_j^{\,d})/w_j])$)와 겉보기 구조가 같다. 아래는 이 ``겉보기 동형''을
\emph{대입해 실제로 같은 식이 되는지}까지 닫는다.

\textbf{(b) 연산 — MSMR 을 $X_j$ 로 정규화.} 식~\eqref{eq:msmr} 의 양변을 $X_j$ 로 나누면 순수 logistic
(치역 $[0,1]$)이 된다 — $\xi_{\eq,j}$ 와 같은 정의역에 놓기 위한 필수 단계다:
\begin{equation}
\frac{x_j}{X_j}=\frac{1}{1+\exp[\,f(U-U_j^0)/\omega_j\,]}.
\label{eq:lco-msmrnorm}
\end{equation}

\textbf{(c) 중간식 — 항별 대응과 부호의 \emph{강제}.} 식~\eqref{eq:lco-msmrnorm} 을 $\xi_{\eq,j}=
1/(1+\exp[-\sigma_d(V-U_j^{\,d})/w_j])$ 와 같은 축($U=V$) 위에서 항등이 되도록 요구하면, 중심$\cdot$폭이
같을 때($U_j^0=U_j^{\,d}$, $\omega_j=w_j$) 두 지수가 \emph{모든} $U$ 에서 같아야 하므로
\[
\frac{f(U-U_j^0)}{\omega_j}\overset{!}{=}\frac{-\sigma_d(U-U_j^0)}{w_j}
\quad\text{(항등, }\omega_j=w_j\text{)}
\quad\Longrightarrow\quad f=-\sigma_d,
\]
가 \emph{유일}하게 결정된다(비교가 아니라 항등식이 강제하는 유일해 — 원문의 "부호 비교" 서술을 등식으로
못박음). 이로써 네 대응 $X_j\leftrightarrow Q_j$, $U_j^0\leftrightarrow U_j^{\,d}$, $\omega_j\leftrightarrow
w_j$, $f\leftrightarrow-\sigma_d$ 를 전부 넣으면 $x_j/X_j=\xi_{\eq,j}$, 곧
\begin{equation}
x_j=Q_j\,\xi_{\eq,j}(V,T)
\label{eq:lco-msmriso}
\end{equation}
— MSMR 의 종별 반응 진행량 $x_j$ 가 Ch1 의 $Q_j$-스케일 진행률과 \emph{글자 그대로 같은 양}이다(구조가
비슷한 게 아니라 같은 식의 다른 표기).

\textbf{(d) 박스 — 동형성을 미분해 peak 로 닫기.} 식~\eqref{eq:lco-msmriso} 를 $V$ 로 미분하면(종 항등식
eq:belliden 의 연쇄율, §sec:eqpeak (b)(c) 그대로)
\begin{equation}
\boxed{\;
\frac{\dd x_j}{\dd V}=Q_j\,\frac{\dd\xi_{\eq,j}}{\dd V}
=Q_j\,\frac{\sigma_d\,\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
\quad\Longrightarrow\quad
\Big|\frac{\dd x_j}{\dd V}\Big|=Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
=\Big(\frac{\dd Q}{\dd V}\Big)^\eq_j
\;}
\label{eq:lco-msmrderiv}
\end{equation}
— MSMR 의 종별 미분(전위에 대한 반응진행 변화율)이 Ch1 의 평형 peak 식~\eqref{eq:eqpeak} 과 \emph{항등}
이다. 이것이 ``MSMR 동형''의 실제 내용이다: 대응표가 주는 사전을 넣으면 두 모델은 서로 다른 두 식이 아니라
\emph{같은 식의 두 표기}이고, 그 항등성이 $x_j$ 정의(eq:lco-msmriso)에서 그 미분(eq:lco-msmrderiv)까지
끊김 없이 이어진다.

Ch1 의 곡선 클래스(\code{func\_ksi\_eq}$\cdot$\code{func\_U\_j}$\cdot$합산~\eqref{eq:sum})는 \emph{구조
변경 0}으로 LCO 에 적용되며, 바뀌는 것은 단 둘이다:
\begin{enumerate}[label=(\roman*),leftmargin=2.2em,itemsep=1pt]
\item \textbf{전이 파라미터 교체} — \code{GRAPHITE\_STAGING\_LIT} $\to$ \code{LCO\_MSMR\_LIT}
(표~\ref{tab:lco-staging}): $(\Delta H_\rxn,\Delta S_\rxn,Q,\Omega,\Delta H_a,\dots)$ 값을 양극 영역으로.
코드의 전이 dict 키 구조는 동일하다(식~\eqref{eq:lco-msmriso} 가 이 교체의 정당성 — $Q_j$ 자리에 어떤
값을 넣어도 항등식 자체는 안 바뀐다).
\item \textbf{전자 엔트로피 항 plug-in} — \S5 의 사슬(식~\eqref{eq:lco-plugin})이 정확히 이 자리에서
실행된다: T1 전이의 $\Delta S_{\rxn}$ 평가에 몰당 식~\eqref{eq:dSemolar} 의 $\Delta S_{e,j}^{\,\mathrm{mol}}
(x,T)=N_A\,\partial S_e/\partial x$(좌표는 §5 의 $x=x(\xi_{\eq,1}(V))$)를 더하는 한 줄
(식~\eqref{eq:lco-decomp}). \textbf{★단위 주의} — forward 슬롯 $\Delta S_{\rxn,j}$ 는 J/(mol\,K) 라, 자리당
식~\eqref{eq:dSe}($k_B^2\,g$ 인자 형태)가 아니라 \emph{$N_A$ 를 곱한} 몰당 식~\eqref{eq:dSemolar} 를 넣어야
한다($N_A$ 배 누락 시 전자항이 $\sim10^{23}$ 배 과소). $g(E_F,x)$ 는 식~\eqref{eq:ggate} 의 게이트로,
초기값 3개($g_\max,x_\mathrm{MIT},\Delta x_\mathrm{MIT}$)가 피팅 인자로 노출된다.
\end{enumerate}
$\partial U_j/\partial T\leftarrow\Delta S_{\rxn,j}^\mathrm{cat}/F$ 의 경로(식~\eqref{eq:lco-dUdT})는 흑연과
동일하다 — 곧 ``파라미터 $+1$ 항'' 외에 구조 변경이 없다. 이것이 ``흑연 forward 교과서가 LCO 양극까지 한
틀로 닫힌다''의 코드 측 증거이며, 본 챕터가 두 전극을 한 프레임으로 통합한 까닭이다.
```

### 6.4 자기검수 (재유도 근거)
| 검사 | 결과 |
|---|---|
| 항등 강제(★핵심) | $f=-\sigma_d$ 가 "부호를 맞춰보니 비슷하다"가 아니라 **모든 $U$ 에서 두 지수가 일치해야 한다는 항등식의 유일해**임을 명시 — 원문의 느슨한 "부호 비교" 서술을 실제 대수적 필연으로 강화(재유도로 검증한 진짜 개선점) |
| 사슬 폐쇄(★핵심) | 정의(eq:lco-msmriso: $x_j=Q_j\xi_{\eq,j}$) → 미분(eq:lco-msmrderiv: $\lvert dx_j/dV\rvert=$eq:eqpeak) 까지 끊김없이 연결 — style report 가 지적한 "미폐쇄" 간극을 실제로 닫음 |
| 차원 | $X_j\leftrightarrow Q_j$[C], $U_j^0\leftrightarrow U_j^{\,d}$[V], $\omega_j\leftrightarrow w_j$[V], $f,\sigma_d$ 무차원 — 전 대응 일치 |
| 부호 | $f=-\sigma_d$ — 방전(σ_d=+1)↔f=-1, 충전(σ_d=-1)↔f=+1 (부호 반대가 두 규약의 관례 차이일 뿐 물리 모순 아님, 원문 결론과 동일) |
| 물리 불변 | 파라미터 교체(i)·plug-in(ii) 두 항목·기존 수치·부호 전부 원문 유지, 신규 도입은 (a)–(d) \emph{유도 형식}뿐 |
| 앞 절 정합 | (ii) 항목이 §5 `eq:lco-plugin` 사슬을 직접 인용 — 중복 재유도 없이 참조 |

### 6.5 신설 라벨
| 라벨 | 충돌 검증 |
|---|---|
| `eq:lco-msmrnorm` | grep `No matches found` |
| `eq:lco-msmriso` | grep `No matches found` |
| `eq:lco-msmrderiv` | grep `No matches found` |

---

## 갈래 2 — H-2 정정문안 (Ch2 §ssec:logistic ↔ 파생 C 모순 일원화)

### H-2.1 위치
**주 수정**: `docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex` §ssec:logistic 의 keybox, **L161–166 교체**(L140 헤더·L154 `eq:logistic`·L168 이하 불변). **보조 수정(선택, 대칭 교차참조)**: §ssec:weff(파생 C, L540–569) 의 두-상 불릿(L547–557) 말미에 한 문장 추가(아래 H-2.4).

### H-2.2 모순의 실측 근거
- **주장 A**(§ssec:logistic keybox, L161–166, 현행): "logistic 폭 $w=RT/F$ 는 ... **임의 모수가 아니라** 단일 자리 2-상태 분배함수가 정하는 분포의 열적 폭이다" — **조건 없는 전칭 명제**로 적혀 있다.
- **주장 B**(§ssec:weff 파생 C, L540–557, 현행): "두-상($\Omega>2RT$, **흑연 staging 전이가 여기 속함**): ... 실측 폭은 평형이 정하는 양이 **아니라** ... **현상학적 자유 피팅 파라미터**다."
- 두 주장은 **같은 흑연 staging 전이**(2L→2, 2→1)를 놓고 정반대로 서술한다 — `FABLE_REAUDIT_C4_note.md` §2(CRITICAL, 코드로 확증)가 독립 감사로 이미 확정한 구조적 모순이다.
- ★코드 교차확인(본 드래프트 재확인, 추정 아님): `Anode_Fit_v1.0.12.py` L75–76 `func_w(T,n)=n*R*T/F`, L304–307 `_width`(주석: "폭 $w$: 자유 피팅 파라미터: $w|n$ 직접 지정, 없으면 $n{=}1$") — **모든 전이**(두-상 포함)에 이 $T$-선형 형을 강제 적용한다. `Ω_j` 값에 따라 이 함수형을 바꾸는 코드 경로는 없다.
- ★`파생 A`(§ssec:overlap srcbox, L485–496)의 수치검증("완전식=FD 부동소수점 일치")은 4개 흑연 staging 전이(두-상 2개 포함) \emph{전부}에 이 $T$-선형 $w_j(T)=n_jRT/F$ 를 실제로 대입해서만 성립한다 — `FABLE_REAUDIT_C4_note.md` §2 의 독립 시뮬레이션(Case 1 vs Case 2)이 이를 재확인했다: $w_j(T)=n_jRT/F$(열적 스케일)일 때 완전식이 FD 와 부동소수점급 일치(오차 $\sim10^{-9}$ V/K)하고 단순식은 체계 오차(최대 $\sim0.3$ mV/K)를 내지만, $w_j$ 를 기준온도에서 동결($T$-무관 — 파생 C 가 묘사하는 순수 현상학적 폭에 더 가까운 가정)하면 **일치 관계가 정확히 뒤집힌다**(단순식이 FD 와 일치, "정답"으로 제시된 완전식이 오차를 냄).

### H-2.3 정정 논리 (일원화 방침)
1. 주장 A 의 범위를 **단상($\Omega_j\le2RT$)** 으로 명시 한정한다 — 이 구간에서는 평형 등온선이 단조이고(§ssec:BW, `eq:Veq_BW`), $w_j=n_jRT/F$ 가 그 등온선이 \emph{직접 예측}하는 검증 가능한 양이므로 "임의 모수 아님"이 **문자 그대로** 성립한다.
2. 두-상($\Omega_j>2RT$)에서는 "임의 모수 아님"의 근거(단일 자리 분배함수가 예측하는 열적 폭)가 **적용되지 않는다** — 단일 입자 평형 자체가 그 구간에서 델타에 가깝기 때문이다(파생 C 의 서술 그대로, 손대지 않음). 그러나 \emph{현재 코드}는 두-상에서도 같은 $T$-선형 함수형을 계속 쓴다 — 이는 물리적 필연이 아니라 \textbf{코드 구현의 사실}이며, 파생 A 수치검증이 "성공"하는 것은 바로 이 사실 때문이다. 이를 명시하지 않으면 독자는 파생 A 의 성공을 "두-상도 평형이 예측한 폭"이라는 잘못된 결론으로 오독한다.
3. 이 단상/두-상 갈림은 **이미 Chapter 1 §sec:width(``이중지위'')·§sec:broadening 가 정확히 이렇게 선언**하고 있다 — Ch2 §ssec:logistic 만 그 한정을 빠뜨린 채 무조건 명제로 남아 있었다. 정정은 Ch2 를 Ch1 의 기존 선언에 맞추는 것이지, 새 물리를 도입하는 것이 아니다.

### H-2.4 정정 텍스트 (LaTeX, §ssec:logistic keybox 교체안)

```latex
\begin{keybox}
Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라 \emph{격자기체 점유 분포의 여집합}
(탈리튬화 진행률 $=1-\theta$)이다. \textbf{단, 이 ``임의 모수 아님'' 지위는 \emph{단상}($\Omega_j\le2RT$,
균질 고용체) 전이에 \emph{한정}된다} — 이 구간에서는 평형 등온선(\S\ref{ssec:BW}, 식~\eqref{eq:Veq_BW})이
단조이고 logistic 폭 $w=RT/F$(자리당 $n_j{=}1$ 기준; 전이별 유효 폭 $w_j=n_jRT/F$)가 단일 자리 2-상태
분배함수~\eqref{eq:Z1} 로부터 \emph{직접 예측$\cdot$검증 가능한} 열적 폭이다(Chapter 1 \S\ref{sec:width}
의 이중지위 선언과 정확히 일치).

\emph{두-상}($\Omega_j>2RT$, 흑연 staging $\mathrm{LiC_{12}}\cdot\mathrm{LiC_6}$ 이 여기 속함) 전이에서는
사정이 다르다 — 단일 입자 평형은 plateau \emph{안에서} 거의 델타이므로(\S\ref{ssec:weff} 파생 C), $w_j=
n_jRT/F$ 를 ``평형이 예측하는 값''으로 검증할 단일-입자 평형 대상 자체가 없다. \textbf{★파생 A 수치검증의
전제.} 그럼에도 \emph{현재 코드}(\texttt{func\_w}$(T,n)=nRT/F$, \texttt{\_width} — Chapter 1
\S\ref{sec:width}$\cdot$\S\ref{sec:broadening})는 $\Omega_j$ 값과 무관하게 \emph{모든} 전이에 같은
$T$-선형 함수형을 강제 적용하고, 자유도는 진폭 $n_j$(또는 기준온도의 $w$)뿐이다 — \S\ref{ssec:overlap}
srcbox 의 ``완전식 $=$ FD 부동소수점 일치'' 검증은 두-상 두 개를 포함한 4 개 흑연 staging 전이 \emph{전부}에
이 $T$-선형형을 실제로 대입해서 얻은 결과다. 만약 대신 $w_j$ 를 기준온도에서 동결($T$-무관, 파생 C 가
묘사하는 순수 현상학적 폭에 더 가까운 가정)하면 그 일치는 \emph{정확히 뒤집힌다}(단순식이 FD 와 일치하고
완전식이 빗나감 — 독립 재검 시뮬레이션 확인). 곧 파생 A 의 검증은 ``두-상 전이도 코드 안에서 $T$-선형으로
계산된다''는 \emph{구현의 사실}을 전제로 할 뿐, 이를 ``두-상 전이가 단상과 같은 방식으로 평형이 예측한
폭을 갖는다''는 \emph{물리적 주장}으로 되읽어서는 안 된다. 두-상의 $w_j$ 는 여전히 \S\ref{ssec:weff} 파생
C 가 정하는 \emph{현상학적 자유 피팅 폭}이며 — 그 피팅이 실제로 도는 함수형이 (코드 제약상) 단상과 같은
$n_jRT/F$ 골격이라는 것이 이 문단의 전부다. Chapter 2 는 이 분포를 결론이 아니라 출발점으로 삼아 엔트로피를
쌓되, 이 \emph{단상/두-상 이중지위}(Chapter 1 \S\ref{sec:width})를 항상 전제한다.

★표기: $\theta=$ Li 점유율(만충서 1), $\xi=1-\theta=$ 탈리튬화 진행률(희박서 1); 둘은 같은 점유 분포의
두 이름이다.
\end{keybox}
```

### H-2.5 보조 정정 (선택, 파생 C 쪽 대칭 교차참조 — §ssec:weff L556 뒤 삽입 제안)

```latex
(★\S\ref{ssec:logistic} 키박스의 ``임의 모수 아님''은 \emph{단상} 전이에 한정된다는 점을 그 절 자신이
명시하도록 정정했다 — 본 절의 두-상 서술과 그 절의 단상 서술은 이제 모순이 아니라 Chapter 1
\S\ref{sec:width} 이중지위의 두 절반이다.)
```

### H-2.6 자기검수
| 검사 | 결과 |
|---|---|
| 모순 실측 확인 | §ssec:logistic(L161-166)·§ssec:weff(L540-557) 원문을 직접 대조 — 동일 전이(흑연 staging 두-상 2건)에 대한 상반 서술 확인(추정 아님) |
| 코드 근거 확인 | `Anode_Fit_v1.0.12.py` L75-76(`func_w`)·L304-307(`_width`) 직접 읽어 "모든 전이에 T-선형 강제" 확인(추정 아님, 파일·줄 인용) |
| FABLE 근거 인용 | `FABLE_REAUDIT_C4_note.md` §2 의 Case1/Case2 수치(오차 크기·방향 전환)를 정확히 인용, 새 수치 날조 없음 |
| 물리 변경 없음 | 결과식(`eq:logistic`·`eq:Z1`·`eq:Veq_BW`·파생 A/C 의 결론)은 **전혀 수정하지 않음** — 오직 §ssec:logistic keybox 의 \emph{서술 범위}만 한정 |
| Ch1 정합 | Ch1 §sec:width(이중지위 원문 L740-755)·§sec:broadening(b)(L1266-1273, "현재 코드 n_j=1 고정 → 실폭 RT/F≈25.7mV, 'w' 폴백은 'n' 제거 시 활성" 서술)와 교차 확인 — 정정문안이 이 두 서술과 완전히 정합 |
| 과잉수정 경계 | ssec:weff·ssec:BW·eq:Veq_BW 등 파생 C/BW 본문은 **미수정**(원문 그대로) — H-2 의 정정은 오직 §logistic 쪽 한정어 추가로 국한, 파생 C 쪽은 선택적 1문장 교차참조만 제안 |

---

## 최종 5줄 요약

1. **수식화 커버**: LCO 6절 전부 작성 — `sec:lco-center`(§1, `eq:lco-dUdT` 재사용)·`sec:lco-hys`(§2, 신설 9라벨)·`sec:lco-peak`(§3, 신설 2라벨, 3봉우리 합산 박스 신규)·`sec:lco-decomp`(§4, `eq:lco-decomp` 재사용 + 형식 유도 신설 2라벨)·전자항 plug-in(§5, 좌표매핑 신설 4라벨)·`sec:lco-code` MSMR(§6, 동형성 실제 증명 신설 3라벨) = 신설 20라벨 + 재사용 2라벨, 전수 grep 충돌 0. H-2(Ch2 §logistic↔파생C) 정정문안 완료.
2. **논리결함 발견 여부**: 원 결과식·부호·값 자체에서 새 결함은 발견되지 않았다(center·hys 는 V1011 map 재유도로 전부 확인). 다만 (i) center §1.4(c)에서 "이중경로 교차검증"이 $\Delta S$ 순간값 고정을 전제한다는 것을 명시적으로 보강했고, (ii) decomp §4에서 $Z\approx Z_\mathrm{config}Z_\mathrm{elec}$ 인수분해가 \emph{근사}(등호 아님)임을 재확인해 과장을 막았으며, (iii) MSMR §6 에서 "부호 비교"였던 원문을 "항등식이 강제하는 유일해"로 강화하고 $x_j=Q_j\xi_{\eq,j}\to$ peak 사슬을 실제로 폐쇄했다(원문 갭 해소) — H-2 는 FABLE 감사가 이미 확정한 CRITICAL 모순의 정정문안이다.
3. **물리 불변 확인**: 전 절에서 $\Omega_j$ 는 기호로만 사용(수치 대입 0), 0.47/1.49 J/(mol·K)는 config $\Delta S$ 로만 표기, 신규 개념(ρ(U_app)·PSD 등) 도입 0, `eq:lco-dUdT`·`eq:lco-decomp` 두 재사용 라벨의 물리·값·부호 불변, M-10 가드(T² 적분 해석) 매 참조 지점에서 준수, 불가침 절(`sec:lco-map`·`sec:lco-Se`·`sec:lco-gate`·N0-N9·전자엔트로피) 미접촉.
4. **최약점**: §5 의 좌표 매핑 $x(\xi_{\eq,1})$ 아핀 사상은 유도가 아니라 \emph{모델 가정}(그 자체로 명시했으나 T1 구간 내부 조성-진행률 관계의 실제 비선형성 여부는 미검증)이고, config 중심 표준값(0.47/1.49 J/(mol·K))은 round-trip 미실증 tier-A(출처)/미확인(우리 시료) 초기값이라는 점이 이 드래프트 전체에서 가장 남는 공백이다 — round-trip 가드 조건(§5.3 말미)을 통과해야 신뢰값으로 승격 가능.
5. **작성 방식 준수**: 절별 루핑 선형(정독→사슬→자기검수→앞 절 정합)으로 작성, 통째 배치 없음. tex/코드 미수정, 허위 attribution 없음(모든 재유도는 본 드래프트 직접 수행 표시), 추정 없이 전 줄번호·라벨·코드 인용을 grep/직접 읽기로 실측.
