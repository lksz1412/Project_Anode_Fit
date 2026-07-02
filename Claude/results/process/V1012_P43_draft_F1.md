# V1012 Phase 4.3 — 작성 드래프트 F1 (Fable)

> 대상: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex` (1965줄) · `graphite_ica_ch2_v1.0.12.tex`
> 성격: **드래프트만(.md supplement)** — `.tex`/코드 미수정(편입은 Fable master). 갈래 1 = LCO 6절 수식화((a)출발→(b)연산→(c)중간식→(d)박스), 갈래 2 = H-2 정정문안.
> 근거: Ch1·Ch2 **전문 정독**(head→tail, 부분 read 로 전 영역 cover) + `V1011_P11_map_v10.md`(P1.1, 계승·재검증) + `V1010_LCO_STYLE_REPORT.md` §1 + `FABLE_REAUDIT_C4_note.md`. 모든 유도는 본 드래프트에서 **독립 재유도**로 검증했다(각 절 "논리 감사" 블록). 추정 없음 — 줄·식 근거 병기.

---

## 0. 조립 전 확정 사실 (v1.0.12 실측)

### 0.1 편입 위치 실측 (v1.0.11→v1.0.12 줄 이동 반영)

| 절 | 헤더(보존) | 교체 범위(줄글) | 보존 범위 | 다음 경계(불변) |
|---|---|---|---|---|
| `sec:lco-center` | L476 `\subsection{...}\label{sec:lco-center}` | **L477–494** (전극무관 단정 프로즈 + `eq:lco-dUdT` L484–488 괄호 전보체) | **L496–516 verifybox**, **L518–519 히스 다리** | L521–522 `\section{...}\label{sec:hys}` |
| `sec:lco-hys` | L696 | **L697–719** (intro + T2·T3 + T1 MIT + 도핑, 4문단) | — | L721–722 `\section{...}\label{sec:width}` |
| `sec:lco-peak` | L1220 | **L1221–1232** (전극무관 적용 + 세 봉우리 줄글 열거) | — | L1234 `\subsection{...}\label{sec:broadening}` |
| `sec:lco-decomp` | L1715 | **L1716–1765** (분해 박스 `eq:lco-decomp` L1719–1724 + bullet + ★Ch2/P4 예고) — 박스 식·라벨은 **원문 그대로 재사용 승계** | — | L1767 `\subsection{...}\label{sec:lco-code}` |
| plug-in·MSMR (`sec:lco-code`) | L1767 | **L1768–1792** (`eq:msmr` L1770–1773 포함 — 라벨 재사용 승계) | — | L1794 `\subsection{전체 입력 인자...}` |

### 0.2 ★라벨 인벤토리 (전수 grep, v1.0.12)

- 기존 `eq:lco-*` 전수 = {`eq:lco-dUdT`(L487), `eq:lco-decomp`(L1723)} **딱 2개** — 그 외 임의 `eq:lco-*` 신설명 충돌 0.
- **`eq:lco-dUdT` 재사용 필수**: `\eqref` 참조 6곳 = L493·L498·L1229·L1750·L1790·L1877. L493 은 교체 범위(L477–494) 안이라 소멸 → **잔존 5곳**(verifybox L498 + 후속 절 3 + nodemap 표 1)이 깨지지 않으려면 새 (d) 박스가 `\label{eq:lco-dUdT}` 를 이어받아야 한다(P1.1 §0.3 판단과 동일, 줄번호만 갱신).
- **`eq:lco-decomp` 재사용 필수**: 참조 = L505·L508·L1729·L1738·L1785 등 + 본 supplement center 블록 자체. decomp 절 재작성 블록 안에서 박스 식 내용·라벨을 원문 그대로 둔다.
- **`eq:msmr` 재사용**: 참조 L1774·L1879(tab:nodemap). `eq:lco-*` 프리픽스 규약은 **신설** 라벨에만 적용 — 기존 라벨 승계는 예외(load-bearing).
- 교차참조에 쓰는 기존 라벨 존재 확인: `eq:n0map`(206)·`eq:gibbsdef`(421)·`eq:eqbalance`(434)·`eq:eqcond`(442)·`eq:Ujmid`(455)·`eq:Uj`(460)·`eq:mu`(540)·`eq:gxi`(546)·`eq:gpp`(553)·`eq:spinodal`(560)·`eq:Veq`(601)·`eq:hyssub`(612)·`eq:hysdiff`(622)·`eq:dUhys`(630)·`eq:Ubranch`(648)·`eq:center`(663)·`eq:wbase`(733)·`eq:xieq`(788)·`eq:belliden`(1198)·`eq:eqpeak`(1209)·`eq:sum`(1682)·`eq:dSe`(1028)·`eq:dSemolar`(1038)·`eq:gunit`(1046)·`eq:ggate`(1090)·`eq:dSegate`(1105)·`eq:U1T2`(1075)·`tab:lco-staging`(336)·`tab:staging`(1697). ★v1.0.12 신규 자산 `eq:U1T2`(T² 적분 닫힌형)는 P1.1 시점(v1.0.11)에 없던 라벨 — center T² 가드가 이제 이 라벨을 직접 참조할 수 있다(개선 1건).

### 0.3 불가침 확인

`sec:lco-map`(L301)·`sec:lco-Se`(L965)·`sec:lco-gate`(L1082)·전자엔트로피 절(L945–1181)·N0–N9 흑연 본체·verifybox(L496–516) 미접촉. 물리·결과식·부호·수치·$\Omega_j$ 기호 불변(0.47/1.49 = config $\Delta S$, $\Omega$ 아님). 신규 개념($\rho$/PSD 등) 도입 0. M-10 가드(T1 전자항 $\propto T$·현행 코드 $T_\mathrm{ref}$ 동결 선형 $U(T)$ — 적분 해석) 유지.

---

## 1. `sec:lco-center` — P1.1 계승 + 재검증 + 개선

**편입 지시**: 아래 블록으로 **L477–494 교체**. L476 헤더·L496–516 verifybox·L518–519 다리 보존. (d) 박스가 `\label{eq:lco-dUdT}` 승계.

### 1.1 LaTeX 수식 사슬

```latex
\textbf{(a) 출발 — 전극-중립 골격의 세 진입.}
\S\ref{sec:center} 의 평형 중심 유도를 되짚으면 어느 다리에도 ``흑연''이라는 물질 고유 항이 들어가지
않는다: (i) 실험조건 매핑 식~\eqref{eq:n0map} 의 방향 부호$\cdot$전류 환산
$\sigma_d=\pm1,\ |I|=\code{c\_rate}\,Q_\cell$ 은 삽입형 전극이면 종류를 가리지 않고, (ii) 전기화학 평형
조건 식~\eqref{eq:eqcond}($\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U),\ \Delta G_j=-sFU_j$)는 삽입
반쪽반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 의 전기화학 평형
(식~\eqref{eq:eqbalance})에서 나오며 host 가 흑연인지 LCO 인지에 무관하고(host 의 화학 정체는 상수
$\mu^0$ 값으로만 흡수된다), (iii) 비배치 몫 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 은 반응
종에 무관한 열역학 항등식이다. LCO 로 넘어갈 때 이 세 자리에 들어가는 것은 전이 집합과 입력값의 치환뿐이다:
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
없었다는 (a)의 대입 확인).

\textbf{(c) 중간식 — 중심과 온도 미분(이중 경로 교차검증).}
(b)를 $U_j^\mathrm{cat}$ 로 이항하면 $U_j^\mathrm{cat}(T)=(-\Delta H_{\rxn,j}^\mathrm{cat}
+T\Delta S_{\rxn,j}^\mathrm{cat})/F$ 로, 흑연 식~\eqref{eq:Uj} 와 같은 함수형이다. 온도 계수는 두 독립
경로가 같은 값에 닿는다. \emph{경로 1(직접 미분)}: $\Delta H^\mathrm{cat}$ 는 $T$ 무관, $T\Delta S^\mathrm{cat}$
의 미분이 $\Delta S^\mathrm{cat}$ 이라 $\partial U_j^\mathrm{cat}/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$.
\emph{경로 2(Gibbs 항등식 경유)}: 등압 Gibbs 항등식 $\partial\Delta G_j/\partial T|_P=-\Delta S_{\rxn,j}^\mathrm{cat}$
(식~\eqref{eq:gibbsdef} $G\equiv H-TS$ 에서)와 식~\eqref{eq:eqcond} 의 $\Delta G_j=-FU_j$ 를 미분한
$\partial\Delta G_j/\partial T=-F\,\partial U_j^\mathrm{cat}/\partial T$ 를 등치하면
\[
-F\,\frac{\partial U_j^\mathrm{cat}}{\partial T}=-\Delta S_{\rxn,j}^\mathrm{cat}
\ \Longrightarrow\
\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
두 경로 어디에도 host 구분 항이 없다 — 이것이 ``전극 불문''의 수식적 의미다.

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
보정과도 부호 충돌이 없다 — 정량은 아래 verifybox). \textbf{★다온도 전자항 주의.} $\Delta S_{e,j}(x,T)\propto T$
인 항을 다온도 모델에 실제로 풀 때는 고정 $\Delta H$ 로 $U_j(T)=(-\Delta H+T\Delta S(T))/F$ 를 기계 미분하면
잉여항 $T\,\partial_T\Delta S$ 가 생기므로, 열역학적으로 유지할 불변식은 위 박스의
$\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}(T)/F$ 이고 위치는 기준온도에서
\[
U_j^\mathrm{cat}(T)=U_j^\mathrm{cat}(T_\mathrm{ref})+\frac1F\int_{T_\mathrm{ref}}^{T}\Delta S_{\rxn,j}^\mathrm{cat}(T')\,\dd T'
\]
로 해석해야 한다 — 전자항 $\propto T'$ 를 실제 적분한 닫힌 특수형이 \S\ref{sec:lco-Se} 의
식~\eqref{eq:U1T2}($\tfrac12(T^2-T_\mathrm{ref}^2)$ 곡률)다. 잉여항이 비물리인 열역학적 이유는 Kirchhoff
일관성이다: $\partial\Delta H/\partial T=\Delta C_p$ 이고 $T\,\partial\Delta S/\partial T=\Delta C_p$ 라
``$\Delta H$ 고정$\wedge\partial_T\Delta S\ne0$'' 가정 자체가 성립하지 않으며, 그 모순 없이 남는 불변식이
$\partial U/\partial T=\Delta S(T)/F$ 다. \textbf{(부호 좌표 고정.)} 아래 검산의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 는 반쪽반응을
\emph{삽입 방향}(Li$^+$ 가 host 로 들어옴)으로 적은 반응 엔트로피이며(표~\ref{tab:staging} 흑연 삽입 규약과
동일 좌표), 단전극 potentiometric $\dd\phi/\dd T$ 의 부호는 측정 규약 의존이므로 아래 verifybox 는 그
대표 스케일을 삽입-반응 $\Delta S_{\rxn}^\mathrm{cat}$ 로 환산해 크기$\cdot$부호 sanity 만 확인한다.
```

### 1.2 원 줄글 대비

- 원문 L477–482: "유도에 전극 가정이 없다"를 **단정 프로즈**로만 선언 → (a) 가 세 진입 지점(`eq:n0map`·`eq:eqcond`·비배치 항등식)을 식별하고 치환식 `eq:lco-n0sub` 로 닫음.
- 원문 L483–488: $\partial U_j/\partial T=\Delta S^\mathrm{cat}/F$ 를 **괄호 전보체**("식 eq:Uj 의 T 미분, 전극 불문")로 처리 → (c) 이중 경로(직접 미분 + Gibbs 항등식) 교차검증으로 다리를 놓고 (d) 박스로 승격.
- 물리·부호·수치 불변: $+0.83$ mV/K·$+80$ J/(mol K)·층위 분리·삽입 기준 좌표 전부 원문 그대로. verifybox(L496–516) 무접촉.

### 1.3 논리 감사 (재유도 근거)

- **재유도**: $\Delta G=-FU$ ⇒ $U=(-\Delta H+T\Delta S)/F$; 경로 1 직접 미분과 경로 2($G\equiv H-TS$ ⇒ $\partial G/\partial T|_P=C_p-S-C_p=-S$ ⇒ $\partial\Delta G/\partial T=-\Delta S$) 합치 확인 — 손 재계산 PASS.
- **차원**: $[\Delta H]/F=$ J/mol ÷ C/mol = V ✓; $[\Delta S]/F=$ V/K ✓.
- **수치 검산**: $F\times0.83\times10^{-3}=96485\times0.00083=80.1$ J/(mol K) ✓ (원문 $\approx+80$ 재현).
- **T² 가드 정합**: $\int_{T_\mathrm{ref}}^{T}(\Delta S_0+a_eT')\dd T'/F=\Delta S_0(T-T_\mathrm{ref})/F+a_e(T^2-T_\mathrm{ref}^2)/(2F)$ — `eq:U1T2`(L1074, $T_0\equiv T_\mathrm{ref}$)와 항등 일치 ✓. Kirchhoff: $\partial\Delta H/\partial T=\Delta C_p=T\,\partial\Delta S/\partial T$ — 잉여항 상쇄 근거 신규 명시(물리 불변·근거 보강).
- **P1.1 대비 변경 2건**: ① T² 가드에 `eq:U1T2` 교차참조 + Kirchhoff 한 줄(v1.0.12 신규 라벨 활용 — v1.0.11 엔 이 라벨이 없었음). ② 층위 분리 문장 말미 "정량은 아래 verifybox"(v1.0.12 verifybox 가 $-46$ vs $+80$ 정량을 이미 보유 — 중복 서술 방지 포인터). 나머지는 P1.1 문안 계승(검증 후 이상 없음).
- **이중계산**: 전자항은 `eq:lco-decomp` 분해 슬롯으로만 진입 — 이 절은 $\Delta S^\mathrm{cat}$ 한 덩이로 취급, 겹침 없음 ✓.

---

## 2. `sec:lco-hys` — P1.1 계승 + 재검증 + 개선

**편입 지시**: 아래 블록으로 **L697–719 교체**. L696 헤더 보존, L721–722 `sec:width` 불변. 흑연 `sec:hys` 결과식(`eq:mu`·`eq:gxi`·`eq:gpp`·`eq:spinodal`·`eq:Veq`·`eq:hysdiff`·`eq:dUhys`·`eq:Ubranch`)은 재유도 없이 **참조·대입만**.

### 2.1 LaTeX 수식 사슬

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

\textbf{★two-phase calibration.}
흑연에서 spinodal 문턱 $\Omega_j>2RT$($2RT\approx4958$ J/mol@298 K, 식~\eqref{eq:spinodal})를 피팅 후
유지하는 것은 네 staging 전이 중 $2\mathrm L\!\to\!2$(LiC$_{12}$)$\cdot$$2\!\to\!1$(LiC$_6$) \emph{두 개}
뿐이고, dilute$\to$stage4$\cdot$$4\mathrm L\!\leftrightarrow\!3\mathrm L$ 은 $\Omega_j<2RT$ 로 내려가
solid-solution 이 된다(\S\ref{sec:width}$\cdot$\S\ref{sec:broadening}). LCO 는 이와 달리 pure-LCO
초기값에서 T1(MIT)$\cdot$T2$\cdot$T3(order--disorder) \emph{세 전이 전부}가 문턱을 넘는 상분리 후보다
(표~\ref{tab:lco-staging}). 곧 흑연 ``4 중 2''$\leftrightarrow$LCO ``3 중 3''로 대응 전이 집합만 다르고
문턱 판정 식 $\Omega_j^\mathrm{cat}>2RT$ 자체는 동일하며, 각 전이의 실제 gap 유무는 최종적으로
\emph{피팅된} $\Omega_j^\mathrm{cat}$ 이 $2RT$ 를 넘는지가 정한다(도핑 시 $\Omega_j^\mathrm{cat}\le2RT$
로 내려가는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다, 아래 도핑 문단).

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
(흑연 코드 분기 그대로).

\textbf{(c) 중간식 — LCO 전위 곡선에 spinodal 대입.}
LCO 전이 $j$ 의 평형 전위 곡선은 식~\eqref{eq:Veq} 에 $U_j^\mathrm{cat},\Omega_j^\mathrm{cat}$ 를 넣어
\begin{equation}
V_{\eq,j}^\mathrm{cat}(\xi)=U_j^\mathrm{cat}
+\frac{RT}{F}\ln\frac{\xi}{1-\xi}+\frac{\Omega_j^\mathrm{cat}}{F}(1-2\xi),
\label{eq:lco-Veq}
\end{equation}
이고 두 spinodal 끝점에서 $\dfrac{\xi}{1-\xi}\Big|_{\xi_{s,j}^\pm}=\dfrac{1\pm u_j^\mathrm{cat}}{1\mp
u_j^\mathrm{cat}}$, $(1-2\xi)\big|_{\xi_{s,j}^\pm}=\mp u_j^\mathrm{cat}$ 이므로(흑연 식~\eqref{eq:hyssub}
과 같은 대입) 극대$-$극소 차는(흑연 식~\eqref{eq:hysdiff} 의 전개 재사용)
\[
\Delta U_{j}^{\hys,\mathrm{cat}}=V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^-)-V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^+)
=\frac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\operatorname{artanh}u_j^\mathrm{cat}\big].
\]
상수 중심 $U_j^\mathrm{cat}$ 는 차에서 상쇄된다.

\textbf{(d) 박스 — LCO 전이별 gap 과 분기 중심.}
\begin{equation}
\boxed{\;
\Delta U_j^{\hys,\mathrm{cat}}(T)=
\begin{cases}
\dfrac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\operatorname{artanh}u_j^\mathrm{cat}\big],
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
흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 대입형이다. ``같은 틀''은 식을 생략한다는 뜻이
아니라 $\Omega_j\mapsto\Omega_j^\mathrm{cat}$, $U_j\mapsto U_j^\mathrm{cat}$, $j\in\mathcal J_\mathrm{LCO}$
를 실제로 넣는다는 뜻이다. \textbf{★분기 부호의 전극-중립 읽기(한정).} 식~\eqref{eq:lco-Ubranch} 의
$\sigma_d$ 가 갈라놓는 물리 내용은 전극 불문 ``\emph{탈리튬화} 가지가 위($+\tfrac12$)$\cdot$\emph{리튬화}
가지가 아래($-\tfrac12$)''다 — 과주행 그림(그림~\ref{fig:hysloop})에서 탈리튬화는 상승 가지의 극대
$\xi_s^-$ 까지, 리튬화는 극소 $\xi_s^+$ 까지 밀리는 것이 전극과 무관한 이중웰 기하이기 때문이다. 흑연
음극 하프셀에서는 방전 라벨이 탈리튬화와 일치해 $\sigma_d=+1$(방전)이 곧 $+\tfrac12$ 가지였으나, LCO
하프셀에서는 \emph{충전}이 탈리튬화이므로 이 슬롯의 부호는 셀 방향 라벨이 아니라 \emph{탈리튬화 여부}로
먹인다(상세와 근거는 \S\ref{sec:lco-peak} 의 방향 슬롯 한정) — 그렇게 읽어야 ``탈리튬화 봉우리가 높은
전위 쪽''이라는 관측(흑연 $U^{\dis}>U^{\chg}$ 와 동일한 물리)이 LCO 에서도 1:1 로 유지된다.

\textbf{(T2$\cdot$T3) order--disorder.}
$x\approx0.5$ 부근 monoclinic 초격자(점유 Li 와 빈자리의 교대 정렬)를 이루는 T2($\sim$4.05 V,
hex$\to$monoclinic)$\cdot$T3($\sim$4.17--4.20 V, monoclinic$\to$hex)는 동종 이웃 인력 $\Omega_j^\mathrm{cat}>0$
이 만드는 상분리의 LCO 사례다. 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j=2,3$ 을 넣으면
\[
u_j^\mathrm{cat}=\sqrt{1-\tfrac{2RT}{\Omega_j^\mathrm{cat}}},\quad
\Delta U_j^{\hys,\mathrm{cat}}=\tfrac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}
-2RT\operatorname{artanh}u_j^\mathrm{cat}\big],\quad
U_j^{\,d,\mathrm{cat}}=U_j^\mathrm{cat}+\tfrac12\sigma_d h_{\eta,j}\gamma_j\Delta U_j^{\hys,\mathrm{cat}}
\quad(j=2,3),
\]
로 T2$\cdot$T3 각각 열린다. \textbf{★$\Omega$ 와 config $\Delta S$ 의 구분(혼동 가드).} 정렬의 charge-order
엔트로피 변화($\approx0.47$ J/(mol\,K)@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$
[tier A, Motohashi\cite{motohashi2009}])는 \emph{엔트로피} 값으로 표~\ref{tab:lco-staging}$\cdot$
식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 슬롯(따라서 $U_j^\mathrm{cat}(T)$ 의 온도 이동)에
들어가지, spinodal 문턱을 정하는 \emph{상호작용 에너지} $\Omega_j^\mathrm{cat}$[J/mol]가 \emph{아니다} —
둘은 서로 다른 양이므로 ``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 식의 다리를 놓아선 안 되고
$\Omega_j^\mathrm{cat}$ 는 gap 을 정하는 별도 피팅 파라미터로 둔다.

\textbf{(T1) MIT 2상역.}
T1($\sim$3.90 V, $x\approx0.94$--$0.75$, 절연체$\to$금속)의 구조적 2상 공존도 같은 정규용액 문턱을 받아
\[
u_1^\mathrm{cat}=\sqrt{1-\tfrac{2RT}{\Omega_1^\mathrm{cat}}},\quad
\Delta U_1^{\hys,\mathrm{cat}}=\tfrac{2}{F}\big[\Omega_1^\mathrm{cat}u_1^\mathrm{cat}
-2RT\operatorname{artanh}u_1^\mathrm{cat}\big],\quad
U_1^{\,d,\mathrm{cat}}=U_1^\mathrm{cat}+\tfrac12\sigma_d h_{\eta,1}\gamma_1\Delta U_1^{\hys,\mathrm{cat}}.
\]
MIT 고유의 전자 자유도는 이 히스 gap 에 새 항으로 섞지 않는다 — 그 항은 이미
$\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^\mathrm{mol}(x,T)$(식~\eqref{eq:lco-decomp})를 통해 $U_1^\mathrm{cat}(T)$ 의 온도 이동
(식~\eqref{eq:lco-dUdT})에 들어간다. 곧 두 몫이 서로 다른 슬롯에 산다:
\begin{equation}
\boxed{\;
\underbrace{\Delta U_1^{\hys,\mathrm{cat}}\ \text{(구조적 2상역)}\ \Leftarrow\ \Omega_1^\mathrm{cat}}_{\text{정규용액 히스 gap (이 절)}}
\quad\Big\|\quad
\underbrace{\partial U_1^\mathrm{cat}/\partial T\ \Leftarrow\ \Delta S_{e,1}^\mathrm{mol}(x,T)}_{\text{전자 엔트로피 (\S\ref{sec:lco-electronic})}}\;}
\label{eq:lco-mit}
\end{equation}
이 분리가 config 2상역과 전자 엔트로피를 이중계산하지 않는 경계다(원 서술의 ``두 몫을 분리''를
슬롯 식으로 못박음).

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
(흑연 식~\eqref{eq:dUhys} 아래 Taylor 극한 재사용, $T_{c,j}=\Omega_j^\mathrm{cat}/2R$)이고,
$\Omega_j^\mathrm{cat,dop}\le2RT$ 로 피팅되는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다 — 이것이
상전이 억제에 따른 히스 축소와 peak smear 의 수식 표현이며, 풀린 몫은 \S\ref{sec:broadening} 의
broadening 폭이 더 크게 담는다. \textbf{★슬롯 분리.} 중심 전위의 미세 shift 는 같은 전이 dict 의
$U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로} 들어가며, $\Omega_j^\mathrm{cat}$ 하나가 gap$\cdot$smear 와
중심 이동을 동시에 만든다고 쓰지 않는다(흑연 \code{GRAPHITE\_STAGING\_LIT} 가 초기값이고 폭이 피팅
대상이었듯, pure-LCO $\Omega_j^\mathrm{cat}$ 가 초기값이고 폭$\cdot$shift 는 우리 데이터로 피팅).
```

### 2.2 원 줄글 대비

- 원문 L697–714: "같은 정규용액 틀 그대로 적용" 서술 3회(T2·T3/T1/총론) + $\Omega_j$ spinodal 대입 중간식 전무 → (a)~(d) 가 $g^\mathrm{cat}\to g''\to$ spinodal $\to V_\eq$ 끝점 대입 $\to\Delta U^\hys\cdot U^d$ 박스를 LCO 기호로 실제 전개.
- 원문 L710–713 "두 몫을 분리한다는 점만 못박는다"(줄글) → `eq:lco-mit` 슬롯 분리 박스로 식화.
- 원문 L715–719 도핑(줄글) → `eq:lco-dope` 문턱 Taylor 극한으로 식화. 물리·부호·수치(0.47/1.49 = config $\Delta S$) 불변.

### 2.3 논리 감사 (재유도 근거)

- **재유도(전 사슬 손 재계산)**: ① 2계 미분 $RT[1/\xi+1/(1-\xi)]=RT/[\xi(1-\xi)]$, $-2\Omega$ ✓. ② $g''=0\Rightarrow\xi^2-\xi+RT/2\Omega=0\Rightarrow\xi_s^\pm=\tfrac12(1\pm u)$ ✓, 실근 조건 $\Omega>2RT$ ✓. ③ 끝점 대입: $\xi_s^-=(1-u)/2$ 에서 $(1-2\xi)=+u$·logit $=(1-u)/(1+u)$; $\xi_s^+$ 에서 $-u$·역수 ✓. ④ 차: $-(4RT/F)\operatorname{artanh}u+(2\Omega/F)u=(2/F)[\Omega u-2RT\operatorname{artanh}u]$ ✓. ⑤ 극대/극소 판별: $\xi<\xi_s^-$ 에서 $g''>0\Rightarrow\dd V/\dd\xi>0$ — $V(\xi_s^-)$ 극대·$V(\xi_s^+)$ 극소, 차 $\ge0$ ✓.
- **부호·양수성**: $u/(1-u^2)=u+u^3+\cdots>\operatorname{artanh}u=u+u^3/3+\cdots$ ⇒ $\Delta U^\hys>0$ ($0<u<1$) — 급수 비교로 확정 ✓.
- **극한(연속성)**: Taylor — $\Omega=2RT/(1-u^2)$ 대입 시 $\Omega u-2RT\operatorname{artanh}u=2RT[u(1+u^2)-u-u^3/3]+\mathcal O(u^5)=\tfrac{4RT}{3}u^3$ ⇒ $\Delta U^\hys\to\tfrac{8RT}{3F}u^3$ — 원문(흑연 L634–635) 계수와 정확 일치 ✓. $2RT@298.15\,\mathrm K=2\times8.314\times298.15=4958$ J/mol ✓.
- **차원**: $[\Omega u]/F=$ J/mol ÷ C/mol = V ✓; $RT\operatorname{artanh}u$ 동일 ✓.
- **이중계산**: `eq:lco-mit` 가 $\Omega$(gap 슬롯) ↔ $\Delta S_e$($\partial U/\partial T$ 슬롯) 분리를 식으로 못박음 — Ch1 L710–713 의 "이중계산 방지의 출발" 선언과 정합 ✓.
- **P1.1 대비 변경 1건**: (d) 뒤의 "방전은 위로, 충전은 아래로"(P1.1 문장)를 **★분기 부호의 전극-중립 읽기** 문단으로 대체 — LCO 하프셀에서 충전=탈리튬화이므로 셀 라벨 그대로 $\sigma_d=-1$ 을 먹이면 탈리튬화 가지가 \emph{아래}로 가 이중웰 과주행 기하(탈리튬화 가지=극대 쪽)와 반대가 된다. 이는 결과식 변경이 아니라 **적용 규칙의 한정**(발견 상세 = §3.4)이다.

---

## 3. `sec:lco-peak` — 신규 수식화 (STYLE_REPORT ★최약 지점)

**편입 지시**: 아래 블록으로 **L1221–1232 교체**. L1220 헤더 보존, L1234 `sec:broadening` 불변. 흑연 대응 절 = `sec:eqpeak`(L1184–1218; `eq:belliden`·`eq:eqpeak`) — 결과식 재유도 없이 참조·대입.

### 3.1 LaTeX 수식 사슬

```latex
\textbf{(a) 출발 — 전하 보존식을 LCO 전이 집합으로.} 흑연 \S\ref{sec:eqpeak} 의 출발점인 전하 보존식은
전극을 가리지 않으므로, 전이 집합만 $\mathcal J_\mathrm{LCO}$(식~\eqref{eq:lco-J})로 바꿔 그대로 적는다:
\begin{equation}
Q_\cell\,q=Q_\bg(V_n)+\sum_{j\in\mathcal J_\mathrm{LCO}}Q_j^\mathrm{cat}\,\xi_j
\;\Longrightarrow\;
\frac{\dd Q}{\dd V}=C_\bg+\sum_{j=1}^{3}Q_j^\mathrm{cat}\,\frac{\dd\xi_j}{\dd V}.
\label{eq:lco-charge}
\end{equation}
\textbf{★방향 부호의 전극-중립 읽기(적용 한정).} 이후의 $\sigma_d$ 는 네 작용처(분극 \S\ref{sec:pol}$\cdot$
분기 \S\ref{sec:hys}$\cdot$logistic 인자$\cdot$꼬리 \S\ref{sec:tail}) 모두에서 물리 내용이 ``\emph{탈리튬화
(산화) 진행 $=+1$}''인 부호다. 흑연 음극 하프셀에서는 방전 라벨이 탈리튬화와 일치해 라벨$=$물리가 겹쳤지만,
LCO 하프셀에서는 \emph{충전}이 탈리튬화(전위 상승 진행)이므로, LCO 데이터에 모델을 걸 때 방향 인자는 셀
방향 라벨이 아니라 탈리튬화 여부로 준다 — 충전 곡선에 $\sigma_d=+1$ 슬롯, 방전(리튬화$\cdot$전위 하강)
곡선에 $\sigma_d=-1$ 슬롯. 이렇게 읽으면 분극($V_\app>V_n$ 는 산화 방향에서 — LCO 충전서 성립)$\cdot$분기
(탈리튬화 봉우리가 위)$\cdot$꼬리 인과(시간 순서 $=$ 전위 오름차순, 격자 역전 불요) 세 부호가 흑연과 1:1 로
유지된다. 평형 종 자체는 아래 (b) 대로 이 선택에 불변이라($\xi\leftrightarrow1-\xi$ 대칭) 어느 읽기로도
같은 봉우리를 준다 — 방향 읽기가 갈라놓는 것은 비평형 두 자리(분기$\cdot$꼬리)뿐이다.

\textbf{(b) 연산 — 평형 추종과 logistic 미분의 종 항등식.} 평형 추종이면 $\dd\xi_j/\dd V$ 에 평형 기울기가
들어간다. LCO 전이 $j$ 의 평형 점유는 흑연 식~\eqref{eq:xieq} 에 분기 중심 $U_j^{\,d,\mathrm{cat}}$
(식~\eqref{eq:lco-Ubranch})을 넣은
$\xi_{\eq,j}=\{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]\}^{-1}$ 이고,
$z_j\equiv\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j$ 로 종 항등식~\eqref{eq:belliden}
($\dd\xi_\eq/\dd z_j=\xi_\eq(1-\xi_\eq)$)과 연쇄율 $\dd z_j/\dd V=\sigma_d/w_j$ 를 곱하면
\begin{equation}
\frac{\dd\xi_{\eq,j}}{\dd V}=\frac{\sigma_d\,\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
\;\Longrightarrow\;
\Big|\frac{\dd\xi_{\eq,j}}{\dd V}\Big|=\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
\qquad(j\in\mathcal J_\mathrm{LCO}),
\label{eq:lco-belliden}
\end{equation}
— $\xi(1-\xi)\ge0$ 라 봉우리 모양은 방향 불변$\cdot$양수이며, $\xi\leftrightarrow1-\xi$($\sigma_d$ 뒤집기)
에 대칭이라 (a)의 방향 읽기 선택에도 불변이다.

\textbf{(c) 중간식 — 봉우리의 세 관측량.} 식~\eqref{eq:lco-belliden} 하나에서 전이 $j$ 봉우리의 위치$\cdot$
순높이$\cdot$면적이 전부 읽힌다:
\begin{equation}
V_{\mathrm{peak},j}=U_j^{\,d,\mathrm{cat}}\ (z_j{=}0),\qquad
\Big(\frac{\dd Q}{\dd V}\Big)^{\eq}_{j,\max}=\frac{Q_j^\mathrm{cat}}{4w_j}\ \Big(\xi_\eq(1{-}\xi_\eq)\big|_{1/2}{=}\tfrac14\Big),\qquad
\int\Big(\frac{\dd Q}{\dd V}\Big)^{\eq}_{j}\dd V=Q_j^\mathrm{cat}\ \Big(\textstyle\int_0^1\dd\xi=1\Big).
\label{eq:lco-peakobs}
\end{equation}
\textbf{(d) 박스 — LCO 하프셀 3-전이 평형 dQ/dV.} (b)를 (a)에 넣으면 양극 전위 영역의 평형 기준선이 닫힌다:
\begin{equation}
\boxed{\;\Big(\frac{\dd Q}{\dd V}\Big)^{\eq}_\mathrm{LCO}(V,T)
=C_\bg+\sum_{j=1}^{3}Q_j^\mathrm{cat}\,
\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j},
\qquad \xi_{\eq,j}=\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]}\;.}
\label{eq:lco-eqpeak}
\end{equation}
흑연이 $\sim$0.085--0.21 V 에 네 봉우리를 남기듯, 이 식은 표~\ref{tab:lco-staging} 의 입력으로 세 봉우리를
남긴다 — T1 의 $\sim$3.90 V(MIT plateau), T2 의 $\sim$4.05 V, T3 의 $\sim$4.17--4.20 V(T2 와 한 쌍의 좁은
order--disorder 봉우리)이며, order--disorder 의 큰 $\Omega_j^\mathrm{cat}$ 가 spinodal gap
(식~\eqref{eq:lco-dUhys})을 키워 T2$\cdot$T3 의 분기를 흑연보다 날카롭게(좁은 한 쌍 peak 로) 만든다.

\textbf{폭의 지위.} 폭은 흑연과 같은 $w_j=n_jRT/F$(식~\eqref{eq:wbase}) 서식이되, pure-LCO 초기값에서 세
전이 모두 $\Omega_j^\mathrm{cat}>2RT$ 의 두-상 측에 놓이므로 그 폭은 \S\ref{sec:width} 이중지위의
\emph{두-상} 측 — 평형 예측이 아니라 broadening 이 정하는 현상학적 피팅 폭이다(\S\ref{sec:broadening};
어느 지위인지의 최종 판정은 피팅된 $\Omega_j^\mathrm{cat}$ 이 정하며, 도핑으로 $\Omega_j^\mathrm{cat}\le2RT$
로 닫히는 전이는 단상 측의 평형 예측 지위로 넘어간다 — \S\ref{sec:lco-hys} two-phase calibration).

\textbf{T1 의 온도 신호.} T1 의 위치는 \S\ref{sec:lco-electronic} 의 전자항이 $\Delta S_{\rxn,1}^\mathrm{cat}$
를 통해 $U_1(T)$ 의 \emph{온도 이동}에 기여하므로(식~\eqref{eq:lco-dUdT}), 다온도 dQ/dV 에서 T1 봉우리의
\emph{온도 이동률} $\partial U_1/\partial T$ 가 $T$ 에 선형으로 커지는 것이 전자항의 관측 신호다
($\Delta S_{e,1}\propto T$, \S\ref{sec:lco-Se} — 위치 자체가 $T$-선형이 아니라 \emph{이동률}이 $T$-선형,
곧 위치 이동은 $\propto T^2$, 식~\eqref{eq:U1T2}). 도핑은 \S\ref{sec:lco-hys} 대로 봉우리를
smear$\cdot$shift 시킨다($\Omega$ 는 gap$\cdot$smear 슬롯, $U_j^\mathrm{cat}$ 이동은 별도 슬롯).
```

### 3.2 원 줄글 대비

- 원문 L1221–1224: "평형 peak 식은 전극을 가리지 않으므로 그대로 적용된다 — 세 양이 LCO 전이로 읽힌다" **줄글 단정** + T1/T2/T3 위치 **열거** → (a)~(d) 가 보존식→종 항등식→관측 3량(`eq:lco-peakobs`)→3-전이 합산 박스(`eq:lco-eqpeak`)로 실제 전개. STYLE_REPORT 요구 사슬("ξ_eq,j→dξ/dV→ΣQ_j peak_shape→center/height/area 박스, j∈{T1,T2,T3}") 전량 커버.
- 원문 L1225–1227 "LCO 의 세 전이도 모두 Ω_j>2RT 의 두-상이라": **"pure-LCO 초기값에서 두-상 측(최종 판정=피팅)"** 으로 표현 정합화 — 물리 변경이 아니라, 같은 챕터의 흑연 처리(L747–749 "'전부 두-상'은 초기값 상태일 뿐")·`sec:lco-hys` 도핑 문단(도핑 시 $\Omega\le2RT$ 가능, L716–719)·P1.1 two-phase calibration 과의 챕터 내 일관화다.
- 원문 L1228–1232 T1 온도 신호·도핑: 주장 전량 보존(이동률 $T$-선형·위치 $\propto T^2$ — v1.0.12 M-가드 문안 그대로) + `eq:U1T2` 참조 1건 추가.

### 3.3 논리 감사 (재유도 근거)

- **재유도**: $\dd\xi/\dd z=e^{-z}/(1+e^{-z})^2=\xi(1-\xi)$ 손 재계산 ✓(`eq:belliden` 재현). 연쇄율 $\sigma_d/w_j$ ✓. 높이: $\xi(1-\xi)|_{\xi=1/2}=\tfrac14\Rightarrow Q_j/(4w_j)$ ✓. 면적: $\int\xi(1-\xi)/w\,\dd V=\sigma_d\!\int\dd\xi$ 치환적분 $=1$(방전 규약; 크기 $Q_j$) ✓ — 흑연 L1213–1215 와 동일 결과.
- **차원**: $Q_j^\mathrm{cat}$[C]$/w_j$[V] = C/V = $\dd Q/\dd V$ ✓.
- **극한**: $|I|\to0$ 기준선(흑연 `sec:eqpeak` 의 사용 조건과 동일 — $L_V$ 작으면 코드가 이 종 직접 사용); $\gamma_j\to0$ 이면 $U^{\,d,\mathrm{cat}}\to U^\mathrm{cat}$ 로 분기 소멸 ✓.
- **방향 불변**: $\xi(1-\xi)$ 는 $\xi\leftrightarrow1-\xi$ 대칭 ⇒ 봉우리 모양이 $\sigma_d$ 라벨 선택에 불변 — (a) 한정과 자기일관 ✓.
- **이중계산**: 배경 $C_\bg$ 1회(루프 전)·전이별 $Q_j$ 서로소 분해(흑연 `eq:sum` 전제 승계) ✓.

### 3.4 ★신규 발견 — 방향 라벨↔$\sigma_d$ 매핑의 잠재 결함 (한정어로 처리, 결과식 불변)

- **발견**: Ch1 의 $\sigma_d$ 규약(L203: 방전 $+1$/충전 $-1$)은 네 작용처(분극 `eq:vn`·분기 `eq:Ubranch`·logistic `eq:xieq`·꼬리 `eq:reversal`)에서 실질적으로 "**탈리튬화(산화)$=+1$**" 물리를 인코딩한다 — 흑연 음극에선 방전$=$탈리튬화라 라벨과 물리가 겹쳐 문제가 없다. 그러나 LCO 하프셀은 **충전$=$탈리튬화$\cdot$전위 상승**(sec:lco-map L310–311 자체 서술)이므로, 셀 라벨 그대로 $\sigma_d$ 를 먹이면: ① 분기 — LCO 충전(탈리튬화)에 $-\tfrac12$ 가지가 걸려 탈리튬화 봉우리가 \emph{아래}로 감(이중웰 과주행 기하 — 탈리튬화는 상승 가지 극대 $\xi_s^-$ 까지, 곧 $+\tfrac12$ 쪽 — 와 정반대); ② 꼬리 — 충전 분기가 격자를 뒤집어 "시간$=$전위 내림"으로 필터하는데 LCO 충전은 시간$=$전위 \emph{오름}이라 비인과(미래 기억) 신호가 됨; ③ 분극 — $V_n=V_\app-\sigma_d|I|R_n$ 도 산화 방향에서 $V_\app>V_n$ 이어야 하므로 동일 슬롯. **평형 종·MSMR 대응은 $\xi\leftrightarrow1-\xi$ 대칭으로 불변이라 이 결함이 드러나지 않고, 기존 문안 어디에도 LCO 용 $\sigma_d$ 값이 명시된 적이 없어(전수 정독 확인) 기존 본문과 모순되는 정정이 아니라 "미지정 슬롯의 한정"이다.**
- **처방(본 드래프트 반영)**: `sec:lco-peak`(a) 에 ★전극-중립 읽기 문단, `sec:lco-hys`(d) 에 분기 부호 한정 문단 — 결과식·부호·수치 일절 불변, 적용 규칙 한 곳만 못박음. 코너케이스의 메인 승격 아님(기존 흑연 규약·식 전부 유지).
- **P4 코드 함의(보고)**: LCO 확장 시 `_direction_to_sigma` 가 전극 타입을 받아 탈리튬화 부호로 환산하거나, LCO 호출 규약(충전↦`s=+1`)을 docstring 에 못박아야 함.

---

## 4. `sec:lco-decomp` — 신규 수식화 (최소 diff 설계)

**편입 지시(3건 — 통째 교체가 아니라 좁은 diff)**:
① **L1716–1718(도입 3줄) 교체** → 아래 (a)(b)(c) 사슬 블록(콜론으로 끝나 L1719 박스로 직결).
② **L1719–1724 박스 `eq:lco-decomp` 무변경**(식 내용·라벨 원문 그대로 재사용 승계 — 참조 5곳+ load-bearing).
③ **L1729 부호 정정 1건**(아래 4.2) — 그 외 L1725–1765(bullet·closing·★Ch2/P4 예고) 불변.

### 4.1 LaTeX 수식 사슬 (L1716–1718 교체 블록)

```latex
흑연에서 합산식~\eqref{eq:sum} 에 들어가는 $\Delta S_{\rxn,j}$ 는 평형 중심 $U_j(T)$ 를 통해 한 덩이로
작용했다. LCO 양극에서는 이 한 덩이가 세 물리 성분의 합임을 명시한다 — 식과 코드 경로는 그대로이고
($U_j(T)$ 에 들어가는 $\Delta S$ 의 \emph{내부 분해}만 더한다). 분해가 ``더해도 되는'' 근거부터 식으로
놓는다. \textbf{(a) 출발 — 분배함수의 인수분해.} 전이 $j$ 창의 한 미시상태는 (리튬 자리 배열)$\times$
(포논 들뜸)$\times$(전자 준위 점유) 세 자유도의 곱집합이고, 세 자유도가 독립인 극한에서 분배함수가
인수분해된다:
\begin{equation}
Z_j\;=\;Z_j^\mathrm{config}\,Z_j^\mathrm{vib}\,Z_j^\mathrm{elec}\;\times\;e^{-F_j^{\times}/RT},
\qquad F_j^{\times}\approx0\ \ (\text{선도 차수 — MIT 부근 결합 잔차는 무시}),
\label{eq:lco-Zfact}
\end{equation}
($F_j^{\times}$ 는 자유도 간 결합의 잔차 자유에너지 — 리튬 정렬과 전자 밴드채움의 결합 몫으로, 아래
bullet (가) 대로 슬롯 분리로 통제되는 것이 아니라 선도 차수에서 무시된다). \textbf{(b) 연산 — 로그
가법성에서 부분몰 가법성으로.} $F_j=-RT\ln Z_j$ 에 식~\eqref{eq:lco-Zfact} 를 넣으면 로그가 합으로
갈라지고, $S=-\partial F/\partial T$ 가 선형이라 엔트로피도 갈라진다. 삽입 조성 $x$ 로 미분한 부분몰도
같은 세 갈래다:
\begin{equation}
S_j=S_j^\mathrm{config}+S_j^\mathrm{vib}+S_j^{e}\ (+\,S_j^{\times}\!\approx\!0)
\;\Longrightarrow\;
\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=\frac{\partial S_j^\mathrm{config}}{\partial x}
+\frac{\partial S_j^\mathrm{vib}}{\partial x}
+\frac{\partial S_j^{e}}{\partial x}.
\label{eq:lco-Sadd}
\end{equation}
\textbf{(c) 중간식 — 슬롯 정의(이중계산 금지의 식화).} 셋째 항은 몰당 게이트 골
(식~\eqref{eq:dSemolar}$\cdot$\eqref{eq:dSegate})로 이미 닫혔고, 첫째 항은 두 몫으로 갈라진다 —
질서화(charge-order 초격자) 등 봉우리 \emph{중심의 표준} config 몫과, 격자기체 혼합의 \emph{내부 분포}
몫이다:
\begin{equation}
\frac{\partial S_j^\mathrm{config}}{\partial x}
=\underbrace{\Delta S_j^{0,\mathrm{config}}}_{\text{중심 표준값(질서화 등)}}
+\underbrace{R\ln\frac{\xi_j}{1-\xi_j}}_{\substack{\text{혼합 분포항(삽입 기준)}\\ \text{— }w_j(T)=n_jRT/F\text{ 서식이 자동 생성}}},
\qquad
\Big[R\ln\frac{\xi_j}{1-\xi_j}\Big]_{\xi_j=\frac12}=0.
\label{eq:lco-configsplit}
\end{equation}
이로부터 세 슬롯의 기입 규칙이 식으로 못박힌다 — 각 물리 성분이 정확히 한 슬롯에 한 번씩만 들어간다:
\begin{equation}
\Delta S_j^\mathrm{config}\ \leftarrow\ \Delta S_j^{0,\mathrm{config}}\ \text{만}
\ (\text{혼합 분포항은 }w_j\text{ 가 담음 — 재기입 금지}),\quad
\Delta S_j^\mathrm{vib}\ \leftarrow\ \text{창 내 완만 몫의 중심 흡수치},\quad
\Delta S_{e,j}^{\,\mathrm{mol}}\ \leftarrow\ N_A\,\frac{\partial S_e}{\partial x}\ \big(\text{게이트 골, 창 밖}\approx0\big).
\label{eq:lco-slots}
\end{equation}
이 규칙 아래 식~\eqref{eq:lco-Sadd} 의 세 항을 슬롯값으로 적은 것이 분해 박스다:
```

*(→ 이어서 L1719–1724 박스 `eq:lco-decomp` 원문 그대로.)*

### 4.2 ★부호 정정 1건 (L1729, config bullet 내부)

- **원문(L1728–1729)**: "봉우리 중심의 표준값 $\Delta S_j^0$ 에 봉우리 내부 항 $R\ln[(1-\xi)/\xi]$ 가 격자기체 점유 분포(\S\ref{sec:dist})에서 따라 나온다"
- **정정문안**: "봉우리 중심의 표준값 $\Delta S_j^0$ 에 봉우리 내부 항 $+R\ln[\xi/(1-\xi)]$(삽입 기준, 식~\eqref{eq:lco-configsplit})가 격자기체 점유 분포(\S\ref{sec:dist})에서 따라 나온다"
- **근거(독립 재유도 + 극한 + 챕터 간 대조)**: 삽입은 점유 $\theta$ 를 늘리므로 부분몰 config 는 $\partial S_\mathrm{config}/\partial\theta=-R\ln[\theta/(1-\theta)]$, $\theta=1-\xi$ 대입 시 $-R\ln[(1-\xi)/\xi]=+R\ln[\xi/(1-\xi)]$. **극한 검산**: 희박($\xi\to1$, Li-poor)에서 삽입 자리 선택지 폭증 → $+\infty$ 여야 함 — $+R\ln[\xi/(1-\xi)]\to+\infty$ ✓, 원문 표기 $R\ln[(1-\xi)/\xi]\to-\infty$ ✗(부호 반전). **Ch2 대조**: Ch2 `eq:dVdT_config`(L237–239)·파생 B(L299)·C-4 감사 §5 독립 재유도가 전부 $+R\ln[\xi/(1-\xi)]$(삽입 기준) — Ch1 L1729 만 홀로 역부호였다. 국소적(같은 절의 박스·슬롯 규칙·다른 절에 전파 없음 — `(1-\xi)/\xi` 표기는 Ch1 전체에서 이 한 곳뿐임을 정독으로 확인).

### 4.3 원 줄글 대비

- 원문 도입 L1716–1718: "세 성분의 합임을 명시한다"(합산 근거 없는 선언) → (a)(b) 가 $Z$ 인수분해→로그 가법→부분몰 가법으로 근거를 유도 사슬화. STYLE_REPORT 요구("Z=Z_config·Z_elec→슬롯 정의→이중계산 금지식 박스") 커버.
- 원문 bullet 의 ★이중계산 금지(B)·(가) 가산성·(나) 무이중계산(L1729–1741, 줄글 검산) → `eq:lco-configsplit`·`eq:lco-slots` 로 식화하되 **bullet 원문은 보존**(prose 가 식의 해설로 기능; (가)의 "슬롯 분리는 과대계상만 막을 뿐 교차항을 포착·한계짓지 않는다" 주장은 (a)의 $F_j^\times$ 정의와 정확히 정합 — $F^\times$ 는 슬롯 밖 잔차로 명시).
- `eq:lco-decomp` 박스·vib/electronic bullet·closing·★Ch2/P4 예고: **무변경**. (MINOR 제안 1건 — 박스 config 항의 underbrace 주석 "logistic $w{=}RT/F$ 가 담음"은 bullet B 규칙("슬롯엔 중심 표준값만")과 얼핏 충돌하게 읽힘: "중심 표준값(내부 분포는 $w$ 가 담음)"으로의 주석 교정을 master 옵션으로 제안 — 식 자체 불변이므로 채택은 선택.)

### 4.4 논리 감사 (재유도 근거)

- **가법성 재유도**: $Z=\prod Z_i\Rightarrow F=-RT\ln Z=\sum F_i\Rightarrow S=-\partial_TF=\sum S_i$ — 로그·미분 둘 다 선형 연산이라 정확 ✓. 결합 시 $Z\ne\prod Z_i$ 의 잔차를 $F^\times$ 한 자리에 격리(기존 (가) 주장을 기호화한 것 — 새 물리 0, 잔차를 "선도 차수 무시"로 두는 원문 처방 그대로).
- **혼합 분포항 재유도**: $S_\mathrm{config}=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$ ⇒ $\partial_\theta S=-R\ln[\theta/(1-\theta)]$ ⇒ 삽입 기준 $+R\ln[\xi/(1-\xi)]$ ✓(4.2). 중심 $\xi=\tfrac12$ 에서 0 ✓ — 슬롯 규칙의 무모순 접합점(Ch2 파생 B 와 동일 논거).
- **차원**: 전 슬롯 J/(mol K) — 전자항은 몰당 `eq:dSemolar`(자리당 $k_B$→몰당 $R$) 경유 ✓.
- **이중계산**: `eq:lco-slots` 가 성분당 1회 기입을 식으로 강제; 게이트 창 밖 $\Delta S_e\approx0$·중심 혼합항 $=0$ — 두 소멸 조건이 슬롯 간 겹침 0 을 보장 ✓.
- **극한**: MIT 창 통과 적분 $\int|\partial_xS_e|\dd x\approx1.1\,k_B$/atom(완전 metal 끝점 $S_e$ 와 항등, L1130–1132)은 무변경 유지 — 본 사슬과 독립 ✓.

---

## 5–6. `sec:lco-code` — MSMR 동형 사슬(§5) + 전자항 plug-in 사슬(§6), 통합 교체 블록

**편입 지시**: 아래 블록으로 **L1768–1792 교체**. L1767 헤더 보존, L1794 다음 소절 불변. `eq:msmr` 라벨·식 재사용 승계(참조 L1774→블록 내부·L1879 nodemap). item (i) 파라미터 교체 문안·closing 문장(L1790–1792)은 원문 그대로 블록 말미에 포함.

### 5.1 LaTeX 수식 사슬 (교체 블록 전문)

```latex
이 통합의 실용적 결론은 ``같은 코드가 LCO 를 그린다''이다. 그 근거는 \emph{MSMR 동형}이다 —
multi-species, multi-reaction(MSMR) 모델\cite{msmr2024}은 양극 전위를 전이별 logistic 의 합으로 적는다.
\textbf{(a) 출발 — MSMR 종별 점유식.}
\begin{equation}
x_j=\frac{X_j}{1+\exp[\,f(U-U_j^0)/\omega_j\,]},
\label{eq:msmr}
\end{equation}
여기서 $X_j$ 는 종(전이) $j$ 의 용량 분율, $U_j^0$ 는 종 중심 전위다. 원문 MSMR 의 지수 인자는
$f=F/RT$(항상 양)와 무차원 폭 $\omega_j$ 이며, 본 문건 표기는 $F/RT$ 를 폭에 흡수해
($\omega_j\mapsto\omega_jRT/F$, 전압 차원) 방향 부호 인자 $f=\pm1$ 만 지수에 남긴 재모수화다 — 폭 슬롯의
대응이 흑연 식~\eqref{eq:wbase} 의 $w_j=n_jRT/F$($n_j\leftrightarrow$무차원 $\omega_j$)와 정확히 같은
구조임을 이 재모수화가 드러낸다. \textbf{(b) 연산 — 정규화.} 식~\eqref{eq:msmr} 을 종 용량으로 나누면
종별 \emph{점유율}(리튬화 분율)과 그 여집합(탈리튬화 진행률)이 나온다:
\begin{equation}
\theta_j^{\mathrm{MSMR}}\equiv\frac{x_j}{X_j}=\frac{1}{1+e^{+f(U-U_j^0)/\omega_j}},\qquad
\xi_j^{\mathrm{MSMR}}\equiv1-\frac{x_j}{X_j}=\frac{1}{1+e^{-f(U-U_j^0)/\omega_j}},
\label{eq:lco-msmrnorm}
\end{equation}
이고 총 조성은 $\sum_jX_j\theta_j^{\mathrm{MSMR}}$ — 용량 가중 $X_j\!\leftrightarrow\!Q_j$ 로 읽으면
\S\ref{sec:lco-peak} 의 전하 보존식~\eqref{eq:lco-charge} 과 같은 구조다. \textbf{(c) 중간식 — 여집합
항등식과 방향 인자 대응.} Ch1 logistic 서식은 여집합에 대해 닫혀 있다 — 같은 중심$\cdot$폭에서
\begin{equation}
1-\xi_{\eq,j}^{(\sigma_d)}(V)
=\frac{1}{1+e^{+\sigma_d(V-U_j^{\,d})/w_j}}
=\xi_{\eq,j}^{(-\sigma_d)}(V),
\label{eq:lco-comp}
\end{equation}
곧 점유와 진행률은 방향 인자 부호 하나로 오가고, 종 $\xi(1-\xi)$ 는 이 교환에 불변이다(평형 내용은 방향
선택에 무관 — \S\ref{sec:lco-peak}(b)). 이제 식~\eqref{eq:lco-msmrnorm} 의 점유형 지수 $+f(U-U_j^0)/\omega_j$
를 Ch1 서식 식~\eqref{eq:xieq} 의 지수 $-\sigma_d(V-U_j^{\,d})/w_j$ 와 같은 자리에 맞대면, 슬롯별로
\begin{equation}
U\leftrightarrow V,\qquad U_j^0\leftrightarrow U_j^{\,d},\qquad
\omega_j\leftrightarrow w_j,\qquad X_j\leftrightarrow Q_j,\qquad
f=-\sigma_d
\label{eq:lco-msmrmap}
\end{equation}
가 1:1 로 읽힌다 — 방향 인자 대응 $f=-\sigma_d$ 는 식~\eqref{eq:lco-comp} 의 여집합 항등식 그 자체다
(MSMR 점유형 $=$ 반대 방향 인자로 평가한 $\xi$-서식). 이로써 탈리튬화/리튬화 진행 방향이 두 모델에서
일관되게 맞춰진다($U_j^0\leftrightarrow U_j^{\,d}$ 대응은 방향분해 파라미터화로 읽으며, 순정 MSMR 평형
등온선은 $\gamma_j{=}0$ 의 $U_j$ 대응이 기본형이다). \textbf{(d) 박스 — MSMR$\to$평형 peak 변환 폐쇄.}
사전~\eqref{eq:lco-msmrmap} 아래에서 MSMR 종별 미분용량과 Ch1 평형 peak 은 같은 식이다:
\begin{equation}
\boxed{\;Q_j\Big|\frac{\dd(x_j/X_j)}{\dd U}\Big|
=Q_j\,\frac{\theta_j^{\mathrm{MSMR}}(1-\theta_j^{\mathrm{MSMR}})}{\omega_j}
\;\equiv\;Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}
\quad(\text{식~\eqref{eq:lco-eqpeak} 의 피가수})\;,}
\label{eq:lco-msmrpeak}
\end{equation}
($|f|=1$; $\theta(1-\theta)=\xi(1-\xi)$ — 여집합 불변). 따라서 Ch1 의 곡선 클래스
(\code{func\_ksi\_eq}$\cdot$\code{func\_U\_j}$\cdot$합산~\eqref{eq:sum})는 \emph{구조 변경 0}으로 LCO 에
적용되며, 바뀌는 것은 단 둘이다:
\begin{enumerate}[label=(\roman*),leftmargin=2.2em,itemsep=1pt]
\item \textbf{전이 파라미터 교체} — \code{GRAPHITE\_STAGING\_LIT} $\to$ \code{LCO\_MSMR\_LIT}(표~\ref{tab:lco-staging}):
$(\Delta H_\rxn,\Delta S_\rxn,Q,\Omega,\Delta H_a,\dots)$ 값을 양극 영역으로. 코드의 전이 dict 키 구조는 동일하다.
\item \textbf{전자 엔트로피 항 plug-in} — T1 전이의 $\Delta S_{\rxn}$ 평가에 몰당 전자항을 더하는 한 줄.
그 ``한 줄''이 실제로 평가하는 forward 사슬을 조성 좌표에서 dQ/dV 까지 닫는다.
\textbf{(a) 출발 — 좌표 매핑의 닫힌 꼴.} 게이트(식~\eqref{eq:ggate})는 조성 $x$ 의 함수인데 코드는 전압
격자 위에서 돌므로, T1 창의 $x$ 범위(표~\ref{tab:lco-staging}: $x_{\mathrm{hi},1}{\approx}0.94$,
$x_{\mathrm{lo},1}{\approx}0.75$)를 T1 진행률로 선형 보간해 잇는다:
\begin{equation}
x\big(\xi_{\eq,1}(V)\big)=x_{\mathrm{hi},1}-\big(x_{\mathrm{hi},1}-x_{\mathrm{lo},1}\big)\,\xi_{\eq,1}(V)
\label{eq:lco-xmap}
\end{equation}
($\xi_{\eq,1}$ 은 탈리튬화-형 진행률 — 방향 슬롯 읽기는 \S\ref{sec:lco-peak}(a); $\xi{=}0$ 에서
$x{=}0.94$, $\xi{=}1$ 에서 $x{=}0.75$, $x_\mathrm{MIT}{\approx}0.85$ 가 창 내부에 놓인다). \textbf{(b) 연산 —
게이트 대입.} 식~\eqref{eq:lco-xmap} 를 게이트 인자에 넣고 몰당 나눗셈 형
(식~\eqref{eq:dSegate}$\cdot$\eqref{eq:gunit}$\cdot$\eqref{eq:dSemolar})으로 적으면 전압 격자 위의
전자항이 닫힌다:
\begin{equation}
\Delta S_{e,1}^{\,\mathrm{mol}}(V,T)
=-\frac{\pi^2}{3}\,R\,\frac{k_BT}{e_V}\,\frac{g_{\max}}{\Delta x_\mathrm{MIT}}\,
\sigma\!\big(z_e(V)\big)\big[1-\sigma\!\big(z_e(V)\big)\big],
\qquad z_e(V)=\frac{x(\xi_{\eq,1}(V))-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}}.
\label{eq:lco-SeV}
\end{equation}
\textbf{(c) 중간식 — 슬롯 합과 온도 적분.} 이를 분해식~\eqref{eq:lco-decomp} 의 셋째 슬롯에 넣고
(★단위 주의 — forward 슬롯 $\Delta S_{\rxn,j}$ 는 J/(mol\,K) 라, 자리당 식~\eqref{eq:dSe} 가 아니라
$N_A$ 를 곱한 몰당 식~\eqref{eq:dSemolar} 를 넣어야 한다; $N_A$ 배 누락 시 전자항이 $\sim10^{23}$ 배
과소), 온도 계수 관계~\eqref{eq:lco-dUdT} 를 기준온도에서 적분하면 T1 중심의 온도 이동이 닫힌다:
\begin{equation}
\Delta S_{\rxn,1}^\mathrm{cat}(V,T)=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^{\,\mathrm{mol}}(V,T),\qquad
U_1(V,T)=U_1(T_\mathrm{ref})+\frac1F\int_{T_\mathrm{ref}}^{T}\Delta S_{\rxn,1}^\mathrm{cat}(V,T')\,\dd T'.
\label{eq:lco-U1V}
\end{equation}
전자항이 $\propto T'$ 라 이 적분의 닫힌형이 식~\eqref{eq:U1T2} 의 $T^2$ 곡률이고, \emph{현행 구현}은
$\Delta S_e$ 를 $T_\mathrm{ref}$ 에서 동결한 상수 오프셋(단일-기준 근사, 표~\ref{tab:lco-staging} 캡션)
으로 넣으므로 $U_1(T)\approx U_1(T_\mathrm{ref})+[\Delta S_{\rxn,1}^\mathrm{cat}(V,T_\mathrm{ref})/F]
(T-T_\mathrm{ref})$ 의 \emph{선형} $U(T)$ 가 된다 — 코드의 선형 거동은 이 동결 근사의 결과로 읽는다
(다온도 $T^2$ 곡률은 round-trip 피팅 단계 과제). 평가 순서 주의 — 식~\eqref{eq:lco-xmap} 이
$\xi_{\eq,1}$ 을, $\xi_{\eq,1}$ 이 $U_1$ 을 참조하는 고정점 구조이나, 동결 구현은 순환이 없고, 정밀형도
전자항 제외 중심으로 $\xi_{\eq,1}^{(0)}$ 을 먼저 평가해 1회 갱신하면 충분하다(되먹임 이동
$|\Delta S_e^{\,\mathrm{mol}}|/F\times|T-T_\mathrm{ref}|\approx0.48\,\mathrm{mV/K}\times30\,\mathrm K
\approx14$ mV $\lesssim w_1$ — 폭 이하 스케일). \textbf{(d) 박스 — plug-in forward 사슬.}
\begin{equation}
\boxed{\;x\big(\xi_{\eq,1}(V)\big)\ \xrightarrow{\eqref{eq:lco-SeV}}\ \Delta S_{e,1}^{\,\mathrm{mol}}(V,T)
\ \xrightarrow{\eqref{eq:lco-U1V}}\ U_1(T)\ \xrightarrow{\eqref{eq:lco-Ubranch}}\ U_1^{\,d,\mathrm{cat}}
\ \xrightarrow{\eqref{eq:xieq}}\ \xi_{\eq,1}\ \xrightarrow{\eqref{eq:lco-eqpeak}}\
\Big(\frac{\dd Q}{\dd V}\Big)_{\!1}=Q_1\frac{\xi_{\eq,1}(1-\xi_{\eq,1})}{w_1}\;}
\label{eq:lco-plugin}
\end{equation}
$g(E_F,x)$ 는 식~\eqref{eq:ggate} 의 게이트로, 초기값 3개$(g_{\max},x_\mathrm{MIT},\Delta x_\mathrm{MIT})$
를 피팅 인자로 노출.
\end{enumerate}
$\partial U_j/\partial T\leftarrow\Delta S_{\rxn,j}^\mathrm{cat}/F$ 의 경로(식~\eqref{eq:lco-dUdT})는 흑연과 동일하다 —
곧 ``파라미터 +1 항'' 외에 구조 변경이 없다. 이것이 ``흑연 forward 교과서가 LCO 양극까지 한 틀로 닫힌다''의 코드 측
증거이며, 본 챕터가 두 전극을 한 프레임으로 통합한 까닭이다.
```

### 5.2 원 줄글 대비

- **MSMR(원문 L1768–1779)**: "두 지수가 같은 자리를 채우므로 부호 비교에서 $f=-\sigma_d$"(자리 맞춤 선언) → (b) 정규화(`eq:lco-msmrnorm`)·(c) 여집합 항등식(`eq:lco-comp`)으로 $f=-\sigma_d$ 를 **유도**하고, (d) 에서 MSMR→peak 변환 사슬을 `eq:lco-msmrpeak` 로 폐쇄(STYLE_REPORT "MSMR 식→정규화→대응대입(f=−σ_d)→ξ_eq,j→peak 박스" 전량). 대응 사전·$f=-\sigma_d$ 결과 **불변**.
- **★M-정정 1건(귀속)**: 원문 L1769 "multiphase species reaction(MSMR)" → "multi-species, multi-reaction(MSMR)" — 자기 서지(`msmr2024` bibitem, L1954)의 정식 명칭과 불일치했던 두문자 풀이 교정. 아울러 "MSMR 의 $f$ 는 종별 부호 인자 $\pm1$" 단정 → "원문 $f=F/RT$·무차원 $\omega_j$ 를 재모수화해 부호 인자만 남긴 표기"로 귀속 정확화(대응 관계 자체는 불변 — 오히려 $\omega_j\leftrightarrow n_j$ 폭 구조 일치가 드러남).
- **plug-in(원문 L1784–1788)**: "몰당 식을 더하는 한 줄"(결론 선언) → (a)~(d) 가 $x$ 매핑(`eq:lco-xmap`)→게이트 대입(`eq:lco-SeV`)→슬롯 합·적분(`eq:lco-U1V`)→forward 사슬 박스(`eq:lco-plugin`)로 전개(STYLE_REPORT "x=x(ξ_eq,1(V))→ΔS_e,1(V,T)→ΔS_rxn,1(V,T)→U_1(T)→dQ/dV" 전량). ★단위 주의($N_A$, $10^{23}$)·게이트 초기값 3개 노출 문안 **원문 보존**. M-10 가드(동결 선형 $U(T)$=단일-기준 근사) — `eq:lco-U1V` 아래 명문 유지.
- item (i)·closing(L1780–1783·L1790–1792) 원문 그대로.

### 5.3 논리 감사 (재유도 근거)

- **여집합 항등식**: $1-[1+e^{-\sigma z'}]^{-1}=e^{-\sigma z'}/(1+e^{-\sigma z'})=[1+e^{+\sigma z'}]^{-1}$ ($z'=(V-U^d)/w$) — 손 재계산 ✓. 이것이 $f=-\sigma_d$ 의 유일한 수학적 내용임을 확인(원문 결과 재현, 이제 유도 근거 있음).
- **MSMR 미분**: $\theta=[1+e^{+f(U-U^0)/\omega}]^{-1}\Rightarrow\dd\theta/\dd U=-(f/\omega)\theta(1-\theta)$, $|f|=1\Rightarrow|\dd\theta/\dd U|=\theta(1-\theta)/\omega$ ✓; $\theta(1-\theta)=\xi(1-\xi)$ ✓ ⇒ `eq:lco-msmrpeak` 항등 성립.
- **좌표 매핑**: 아핀형 $x=x_\mathrm{hi}-(x_\mathrm{hi}-x_\mathrm{lo})\xi$ — 끝점 검산 $\xi{=}0\mapsto0.94$·$\xi{=}1\mapsto0.75$ ✓, $x_\mathrm{MIT}{=}0.85\in(0.75,0.94)$ ✓, 탈리튬화(충전)에서 $\xi\uparrow\Rightarrow x\downarrow$ ✓(물리 방향). 이는 기존 예고문(L1759–1761 "정규화 조성에 대응")의 수학적 폐쇄이지 신규 개념이 아니다.
- **닫힌식 대입**: `eq:lco-SeV` = 기존 몰당 나눗셈 닫힌식(L1048–1050)에 $z_e(V)$ 만 합성 — 계수·부호(leading $-$) 불변 ✓. 골 깊이 재검산: $-\tfrac{\pi^2}{3}\times8.314\times(0.0259/1)\times(13/0.05)\times\tfrac14$ … eV 환산 포함 $\approx-46$ J/(mol K) — 원문 L1144 와 일치 ✓.
- **되먹임 수치**: $46/96485=4.8\times10^{-4}$ V/K $=0.48$ mV/K; $\times30$ K $=14.3$ mV $<w_1\approx25.7$ mV($n_1{=}1$) ✓ — 고정점 0차+1회 갱신 논거는 코너 검토(메인 승격 아님).
- **차원**: `eq:lco-SeV` — $R\cdot(k_BT/e_V)\cdot(1/\Delta x)$: $k_BT/e_V$ 는 eV 단위 열에너지(무차원 비 $\times$ eV/eV), 전체 J/(mol K) ✓(기존 검증 계승). `eq:lco-plugin` 사슬 — V→J/(mol K)→V→V→무차원→C/V ✓.
- **detailed balance/이중계산**: 전자항은 $U_1(T)$ 온도 이동 슬롯로만 진입(`eq:lco-mit` 분리 준수), 히스 gap·폭에 재기입 없음 ✓.

---

## 7. 갈래 2 — H-2 정정문안 (Ch2 `graphite_ica_ch2_v1.0.12.tex`)

**모순의 실체(FABLE_REAUDIT_C4 §2, 재확인)**: §`ssec:logistic` keybox(L161–166)가 $w_j=n_jRT/F$ 를 **전이 무차별로** "임의 모수가 아니라 …열적 폭"이라 단정하고 그 근거로 §`sec:revheat`·`func_w` 를 지목 ↔ 파생 C(§`ssec:weff` L540–569)·종합식 keybox(L681–690)는 **같은 흑연 두-상 전이**에 대해 평형 예측 $nRT/F$ 를 명시 부정(현상학적 자유 피팅 폭). 파생 A 의 "부동소수점 일치" 수치검증(L485–496)은 현행 코드가 모든 전이에 강제하는 열적 서식 하에서만 성립(감사 Case 2: $w$ 를 $T$-동결하면 단순식/완전식의 오차가 정확히 자리바꿈, $\sim$0.3 mV/K 급). 일원화 원리 = **Ch1 이중지위**(sec:width L740–755): 같은 식 $w_j=n_jRT/F$ 의 **값 서식**은 하나, **지위**는 $\Omega_j$ 가 가른다.

### 7.1 정정 ① — §`ssec:logistic` keybox **L161–166 교체**

```latex
\begin{keybox}
Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라 \emph{격자기체 점유 분포의 여집합}(탈리튬화
진행률 $=1-\theta$)이다. logistic 폭 $w=RT/F$ 는(자리당 $n_j{=}1$ 기준; 전이별 유효 폭 서식 $w_j=n_jRT/F$ 는
\S\ref{sec:revheat}$\cdot$코드 \texttt{func\_w}) \emph{단상 전이($\Omega\le2RT$, 균질 고용체)에 한해} 임의
모수가 아니라 단일 자리 2-상태 분배함수~\eqref{eq:Z1} 가 정하는 분포의 열적 폭 — 곧 측정 폭으로 검증
가능한 \emph{평형 예측} — 이다. \emph{두-상 전이}($\Omega>2RT$; 흑연 staging 의
$2\mathrm L\!\to\!2\cdot2\!\to\!1$ 가 피팅 후에도 여기 남는 전이다)에서는 같은 서식 $w_j=n_jRT/F$ 가 평형
예측이 아니라 broadening 이 정하는 \emph{현상학적 자유 피팅 폭}의 그릇으로 쓰인다(파생 C
\S\ref{ssec:weff}$\cdot$Chapter 1 의 폭 이중지위$\cdot$broadening 절) — 어느 지위인지는 코드 분기가 아니라
그 전이의 $\Omega_j$ 값이 가른다. ★표기: $\theta=$ Li 점유율(만충서 1), $\xi=1-\theta=$ 탈리튬화
진행률(희박서 1); 둘은 같은 점유 분포의 두 이름이다. Chapter 2 는 이 분포를 결론이 아니라 출발점으로 삼아
엔트로피를 쌓는다.
\end{keybox}
```

- **핵심 장치**: "임의 모수가 아니라" 단정 앞에 \emph{단상($\Omega\le2RT$) 한정} 삽입 + 두-상 반대 지위를 같은 박스 안에서 즉시 선언(같은 서식·다른 지위) → §`ssec:weff`·`sec:revheat` 종합식과의 챕터 내 모순 소멸, Ch1 sec:width 이중지위 문안("같은 식, 다른 지위 — $\Omega_j$ 가 가른다")과 챕터 간 1:1 정합. `func_w` 포인터는 "유효 폭 **서식**"으로 강등해 유지(코드 실체와 정합 — 코드는 서식 제공자이지 지위 판정자가 아님).

### 7.2 정정 ② — 파생 A srcbox **L495 문장 뒤(= `\end{srcbox}` 직전) 삽입**

```latex
★\textbf{전제 명시(검증의 조건부).} 이 검증의 $w_j(T)$ 는 현행 코드(\texttt{func\_w}/\texttt{\_width})가
\emph{모든} 전이(흑연 두-상 staging 포함)에 강제하는 열적 서식 $w_j=n_jRT/F$
($\partial w_j/\partial T=n_jR/F$) 하에서 평가된 것이다 — 자유 피팅되는 것은 진폭 $n_j$(또는 기준온도의
$w$)뿐이고 $T$-의존의 함수형은 고정이다. 따라서 완전식의 부동소수점 일치는 그 서식이 낳는 $w(T)$ 조각
(식~\eqref{eq:dxidT} 둘째 항)까지 포함한 \emph{해석 미분 사슬의 자기일관성} 검증이지, 두-상 전이의
물리적 폭이 실제로 $n_jRT/F$ 로 스케일한다는 \emph{실측 검증이 아니다}(만일 실측 $w_j$ 가 $T$-동결에
가깝다면 단순식/완전식의 우열이 뒤집히는 $\sim$0.3 mV/K 급 차이가 남는다). 두-상 $w_j$ 의 지위(현상학적
자유 폭)는 파생 C \S\ref{ssec:weff} 가, 그 $T$-의존 함수형까지 자유화할지는 다온도 실데이터 round-trip
(\S\ref{sec:revheat} 한계 (1))과 코드 후속 과제가 확정한다.
\end{srcbox}
```

*(삽입 방식: 기존 `\end{srcbox}` 를 위 블록의 `\end{srcbox}` 로 대체 — 곧 L495 뒤에 ★문단 추가.)*

- **핵심 장치**: (i) 검증의 전제(코드 강제 서식)를 명시해 파생 A 가 §logistic 편만 실현한다는 감사 지적을 해소 — 검증의 주장 범위를 "해석 사슬 자기일관성"으로 정확히 한정. (ii) 감사 Case 2 의 정량($\sim$0.3 mV/K 자리바꿈)을 반증 가능 형태로 병기. (iii) "함수형 자유화 = 후속 과제" 로 코드-문건 정합의 현재 상태를 정직 선언(M-10 문화와 동일 패턴).

### 7.3 무변경 확인 (정합 검산)

- §`ssec:BW` L205–206("두-상 실측 폭은 현상학적 피팅") · §`sec:mixing` 도입 L436–438 · 파생 C 본문 L540–569 · warnbox L562–569 · tab:limits L618 행 · 종합식 keybox L681–690 — **이미 정정 ① 과 같은 편**이라 무변경. 정정 ①② 후 챕터 내 $w_j$ 지위 서술 전수(전문 정독으로 7곳 확인)가 한 방향으로 정렬된다.
- 파생 D(L587–590)·H-1 BW 부호(L191)·M-9 고온 코너(L620)는 v1.0.12 에서 기정정 — 접촉 없음.

---

## 8. 신설 라벨 총괄 + 충돌 검증

| 라벨 | 절 | 지위 | 검증 |
|---|---|---|---|
| `eq:lco-n0sub` | center (a) | 신설(P1.1 계승) | 기존 `eq:lco-*` 전수={dUdT, decomp} → 충돌 0 |
| `eq:lco-dUdT` | center (d) | **재사용 승계(필수)** | 잔존 참조 5곳(L498·1229·1750·1790·1877) + supplement 내부 |
| `eq:lco-J`·`eq:lco-gxi`·`eq:lco-gpp`·`eq:lco-spinodal`·`eq:lco-Veq`·`eq:lco-dUhys`·`eq:lco-Ubranch`·`eq:lco-mit`·`eq:lco-dope` | hys | 신설(P1.1 계승, 9개) | 충돌 0 |
| `eq:lco-charge`·`eq:lco-belliden`·`eq:lco-peakobs`·`eq:lco-eqpeak` | peak | **신설(F1, 4개)** | 충돌 0 |
| `eq:lco-Zfact`·`eq:lco-Sadd`·`eq:lco-configsplit`·`eq:lco-slots` | decomp | **신설(F1, 4개)** | 충돌 0 |
| `eq:lco-decomp` | decomp (d) | **재사용 승계(무변경 박스)** | 참조 L505·508·1729·1738·1785 등 유지 |
| `eq:msmr` | code (a) | **재사용 승계** | 참조 L1879(nodemap) 유지 |
| `eq:lco-msmrnorm`·`eq:lco-comp`·`eq:lco-msmrmap`·`eq:lco-msmrpeak` | code MSMR | **신설(F1, 4개)** | 충돌 0 |
| `eq:lco-xmap`·`eq:lco-SeV`·`eq:lco-U1V`·`eq:lco-plugin` | code plug-in | **신설(F1, 4개)** | 충돌 0 |

신설 = P1.1 계승 10 + F1 16 = **26개**(전부 `eq:lco-*`), 재사용 = 3개(`eq:lco-dUdT`·`eq:lco-decomp`·`eq:msmr`). 기존 `eq:lco-*` 2개뿐이므로 신설 전원 충돌 0(전수 열거 §0.2). 절간 의존: peak→hys(`eq:lco-J`·`eq:lco-Ubranch`), code→peak(`eq:lco-eqpeak`·`eq:lco-charge`)·decomp(`eq:lco-decomp`) — **편입 순서는 center→hys→peak→decomp→code** 를 권장(전방 참조 최소화; LaTeX 2-pass 라 필수는 아님).

## 9. 논리 감사 총괄 — 발견 결함 목록 (본 드래프트 처리 vs 범위 밖 보고)

| # | 위치 | 내용 | 등급 | 처리 |
|---|---|---|---|---|
| F-1 | Ch1 L1729 (`sec:lco-decomp` config bullet) | 봉우리 내부 config 항 $R\ln[(1-\xi)/\xi]$ — 삽입 기준 **부호 반전**(옳은 형 $+R\ln[\xi/(1-\xi)]$; 희박 극한·Ch2 `eq:dVdT_config`·C-4 감사 재유도 3중 근거). 국소적(전파 0) | HIGH | 정정문안 §4.2 (드래프트 반영) |
| F-2 | Ch1 LCO 전반 (N3·N8 적용) | 방향 라벨↔$\sigma_d$ 매핑이 음극 서사에 결박 — LCO 하프셀에 셀 라벨 그대로 적용 시 분기 부호·꼬리 인과가 물리와 반대(충전=탈리튬화·전위 상승). 기존 본문은 LCO 용 $\sigma_d$ 값 미지정이라 모순 아닌 **미지정 슬롯** | HIGH(잠재) | ★전극-중립 읽기 한정어 §2.1(d)·§3.1(a) + P4 코드 함의 보고 §3.4 |
| F-3 | Ch2 §logistic ↔ 파생C ↔ 파생A | $w_j$ 지위 챕터 내 모순(H-2, 지정 과업) | CRITICAL(기지) | 정정문안 §7.1–7.2 |
| F-4 | Ch1 L1634–1635 (`sec:tail` N8, **흑연 본체 — 불가침 범위 밖**) | 본문 괄호 "(꼬리가 진행 방향 뒤쪽, 곧 충전에서는 $V$ 가 큰 쪽으로 늘어진다)" ↔ 자기 그림 fig:reversal(b) 캡션(L1665–1666) "꼬리가 낮은 $V$ 쪽으로 — 방전의 거울" 이 정면 모순. 재유도: 저역통과 지연의 잔차 $(\xi_\eq-\xi_\mathrm{lag})$ 감쇠 꼬리는 시간상 나중에 지나는 전위 쪽 — 충전(진행 $V\downarrow$)에선 **낮은** $V$ (같은 문장의 "방전의 거울상" 자체도 낮은 $V$ 를 함의; 그림 (b) 좌표열도 낮은 $V$ 쪽 상승 확인) | MODERATE | **보고만**(흑연 본체 무접촉 원칙) — master 의 M-fix 후보: "곧 충전에서는 $V$ 가 낮은 쪽으로 늘어진다" |
| F-5 | Ch1 L1769·L1776–1777 | MSMR 두문자 풀이 오기("multiphase species reaction") + "$f$ 는 종별 부호 인자 $\pm1$" 귀속 부정확(원문 $f{=}F/RT$) | M | 교체 블록 내 정정 §5.1–5.2 |
| F-6 | Ch1 L1720 `eq:lco-decomp` underbrace | config 항 주석 "logistic $w{=}RT/F$ 가 담음"이 bullet B 규칙과 얼핏 상충하게 읽힘 | MINOR | 옵션 제안만(식 불변) §4.3 |

**검증 완료(결함 없음) 커버리지**: center 이중 경로·Kirchhoff 정합, hys 전 사슬(2계 미분→spinodal→끝점 대입→artanh 전개→Taylor $\tfrac{8RT}{3F}u^3$→양수성 급수 비교), peak 종 항등식·3량·면적 치환적분, decomp 가법성·슬롯 소멸 조건, plug-in 골 깊이 $-46$ J/(mol K) 재검산·되먹임 14 mV·$N_A$/eV 단위 사슬, MSMR 여집합 항등식·미분 — 전부 독립 재유도 PASS(각 절 논리 감사 블록).

---

## 10. 5줄 요약

1. **수식화 커버**: LCO 6절 전량 — center·hys 는 P1.1 계승+재검증(개선 3건: `eq:U1T2` 참조·Kirchhoff 근거·분기 부호 한정), peak(`eq:lco-eqpeak` 외 4)·decomp(`eq:lco-Zfact`→`eq:lco-slots`, 최소 diff 설계)·plug-in(`eq:lco-xmap`→`eq:lco-plugin`)·MSMR(`eq:lco-comp`→`eq:lco-msmrpeak`) 신규 작성 — STYLE_REPORT §1 "필요한 수식 사슬" 6행 전부 (a)→(d) 폐쇄, 신설 라벨 26(충돌 0)+재사용 3.
2. **논리결함 발견**: 6건(§9) — L1729 config 내부항 부호 반전(HIGH, 정정문안), LCO 방향 슬롯 잠재 결함(HIGH, 한정어), H-2(지정), N8 꼬리 방향 본문↔그림 모순(MODERATE, 범위 밖 보고), MSMR 귀속 2건(M), decomp 주석(MINOR).
3. **H-2 일원화**: §logistic keybox 에 단상($\Omega\le2RT$) 한정 + 두-상 반대 지위 병기(L161–166 교체) + 파생 A 에 "현행 코드 열적 서식 강제" 전제 명시(L495 뒤 삽입) — 파생 C·revheat 종합식·Ch1 이중지위와 챕터 내·챕터 간 전수 정렬(무변경 7곳 정합 확인).
4. **물리 불변 확인**: 결과식·부호·수치($0.47/1.49$=config $\Delta S$·$\Omega_j$ 기호·$-46$·$1.1k_B$·$+80$)·불가침 절(lco-map·lco-Se·lco-gate·N0–N9·verifybox) 전부 무접촉; 변경은 전개 형식 변환+한정어+근거 있는 부호·귀속 정정 2건뿐, M-10 가드(T_ref 동결 선형 $U(T)$ 적분 해석) 유지.
5. **최약점**: `eq:lco-xmap` 아핀 조성 매핑은 표의 $x$ 범위 초기값(0.94/0.75, tier-C placeholder 코드값과 미정합)에 걸려 있어 round-trip 피팅 시 재보정 필요 — 그리고 F-2 방향 슬롯 한정은 문안 정합까지만 확보(코드 실행 검증은 P4 몫).

