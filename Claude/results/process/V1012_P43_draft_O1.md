# V1012 Phase 4.3 — LCO 6절 수식화 + H-2 정정문안 (드래프트 O1)

> 대상: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`(1964줄) · `graphite_ica_ch2_v1.0.12.tex`(755줄)
> 성격: **드래프트만**(.md supplement). `.tex`/코드 **미수정** — 편입은 Fable master. 허위 attribution 없음.
> 방식: 절별 루핑 선형 [해당 절 + 흑연 대응 절 전문 정독 → 재유도 검증 → 자기검수 → 앞 절 정합 → 다음 절].
> 출발점: center·hys 는 `results/process/V1011_P11_map_v10.md`(P1.1 체리픽) 계승·**재유도 검증**·개선; peak·decomp·plug-in·MSMR 신규.
> 스타일 기준: `results/process/V1010_LCO_STYLE_REPORT.md` §1 "필요한 수식 사슬". H-2 근거: `results/process/FABLE_REAUDIT_C4_note.md` §2.

---

## 0. 조립 전 확정 사실 (v1.0.12 실측 근거)

### 0.1 편입 위치 실측 (교체/삽입 범위, v1.0.12 줄번호)
| 절 | 헤더(보존) | 교체 범위(줄글) | 보존 범위 | 다음 경계(불변) |
|---|---|---|---|---|
| `sec:lco-center` | L476 | **L477–494**(전극무관 단정 + 현행 bare `eq:lco-dUdT` + 대표스케일 프로즈) | **L496–516 verifybox**, **L518–519 히스 다리** | L522 `\section{...}\label{sec:hys}` |
| `sec:lco-hys` | L696 | **L697–719**(intro + T2·T3 + T1 MIT + 도핑, 4문단) | — | L722 `\section{...}\label{sec:width}` |
| `sec:lco-peak` | L1220 | **L1221–1232**(eq:eqpeak 줄글 적용) | — | L1234 `\subsection{...}\label{sec:broadening}` |
| `sec:lco-decomp` | L1715 | **L1716–1724**(intro + `eq:lco-decomp` 박스) 앞에 (a)–(c) 삽입 + (d)에 무이중계산 박스 추가; itemize L1725–1748·Ch2예고 L1756–1765 보존 | L1725– itemize | L1767 `sec:lco-code` |
| 전자항 plug-in | `sec:lco-code` 内 item(ii) L1784–1788 (+ decomp 좌표매핑 L1757–1760) | 신규 forward 사슬 블록 삽입(L1792 뒤, `전체 입력 인자` L1794 앞) | enumerate 보존 | L1794 subsection |
| MSMR 동형 | `sec:lco-code` L1770–1780 (`eq:msmr` + 줄글 동형) | (a)–(d) 사슬로 augment | — | — |

### 0.2 ★현행 v1.0.12 상태 (V1011 대비 델타 — load-bearing)
- **center 는 부분 수식화됨**: v1.0.12 는 이미 `eq:lco-dUdT`(L484–488, $\partial U_j/\partial T=\Delta S^\mathrm{cat}_{\rxn,j}/F$)와 verifybox(L496–516)를 갖는다. 그러나 **(a)출발→(b)연산→(c)중간식 사슬이 없이** bare 식만 있고 앞뒤가 줄글이다. 본 드래프트는 그 (a)–(c) 유도를 채워 넣어 bare 식을 사슬의 (d)박스로 승격시킨다(`eq:lco-dUdT` 라벨 **재사용**).
- **hys 는 순수 줄글**(L697–719, 수식 사슬 0). V1011 의 (a)–(d) 사슬을 편입.
- **peak·decomp 는 흑연 forward 식을 줄글로 "적용"**만 함(peak 은 `eq:eqpeak` 인용, decomp 은 `eq:lco-decomp` 박스는 있으나 $Z$-인수분해·무이중계산이 줄글).

### 0.3 ★라벨 충돌 검증 (전수 실측)
- v1.0.12 ch1 의 기존 `eq:lco-*` = **{`eq:lco-dUdT`(L487), `eq:lco-decomp`(L1723)} 딱 2개**(Grep 전수 확정). 신설 `eq:lco-*` 는 이 둘만 피하면 충돌 0.
- **`eq:lco-dUdT` 재사용 필수**: `\eqref{eq:lco-dUdT}` 6곳 참조(L493·L498·L1229·L1750·L1790·L1877, Grep count=6). 교체 범위 L477–494 에 정의(L487)가 포함되므로, 새 (d)박스가 **반드시 `\label{eq:lco-dUdT}` 를 그대로 이어받아야** 6곳이 안 깨진다.
- **`eq:lco-decomp` 재사용**: 분해 박스 라벨. L505·L508·L1729·L1738·L1745·L1750·L1761·L1879 등에서 참조 → 유지.
- 교차참조 대상 기존 라벨 v1.0.12 실측 존재 확인: `eq:n0map`(206)·`eq:gibbsdef`(421)·`eq:eqbalance`(434)·`eq:eqcond`(442)·`eq:Ujmid`(455)·`eq:Uj`(460)·`eq:mu`(540)·`eq:gxi`(546)·`eq:gpp`(553)·`eq:spinodal`(560)·`eq:Veq`(601)·`eq:hyssub`(612)·`eq:hysdiff`(622)·`eq:dUhys`(630)·`eq:Ubranch`(648)·`eq:wbase`(733)·`eq:xieq`(788)·`eq:belliden`(1198)·`eq:eqpeak`(1209)·`eq:Se`(989)·`eq:dSe`(1028)·`eq:dSemolar`(1038)·`eq:gunit`(1046)·`eq:dSegate`(1105)·`eq:ggate`(1090)·`eq:U1T2`(1075)·`eq:msmr`(1772)·`eq:sum`(1682)·`tab:lco-staging`(336)·`tab:staging`(1697).

### 0.4 불가침 확인
`sec:lco-map`(301)·`sec:lco-Se`(965)·`sec:lco-gate`(1082)·`sec:lco-electronic`(945)·N0–N9 흑연 본체·verifybox(496–516) **미접촉**. 물리·결과식·부호·수치·`Ω_j` 기호 불변, 신규 개념(ρ(U_app)/PSD 등) 도입 0. supplement 의 **M-10 가드**(T1 전자항 $\Delta S\propto T$·선형 $U(T)$·$T_\mathrm{ref}$ 적분 해석)는 center (d)와 plug-in 에서 유지하고 `eq:U1T2` 로 못박는다.

---

## 1. `sec:lco-center` — LCO 평형 중심과 $\partial U_j/\partial T$

**편입 지시**: 아래 블록으로 **L477–494 를 교체**. L476 헤더·L496–516 verifybox·L518–519 다리는 그대로. (d)박스가 `\label{eq:lco-dUdT}` 를 **재사용**(현행 L487 정의 소멸 → (d)박스가 유일 정의). 블록 말미가 verifybox 로 자연 연결.

```latex
\textbf{(a) 출발 — 전극-중립 골격의 세 진입.}
\S\ref{sec:center} 의 평형 중심 유도를 되짚으면 어느 다리에도 ``흑연''이라는 물질 고유 항이 들어가지
않는다: (i) 실험조건 매핑 식~\eqref{eq:n0map} 의 방향 부호$\cdot$전류 환산은 삽입형 전극이면 종류를
가리지 않고, (ii) 전기화학 평형 조건 식~\eqref{eq:eqcond}($\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U),\
\Delta G_j=-sFU_j$)는 삽입 반쪽반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 의
전기화학 평형(식~\eqref{eq:eqbalance})에서 나오며 host 가 흑연인지 LCO 인지에 무관하고(host 의 화학
정체는 상수 $\mu^0$ 로만 흡수), (iii) 비배치 몫 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 은 반응
종에 무관한 열역학 항등식이다. LCO 로 넘어갈 때 이 세 자리에 들어가는 것은 전이 집합과 입력값의 치환뿐이다:
\begin{equation}
j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j})\ \longmapsto\
(\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat}).
\label{eq:lco-n0sub}
\end{equation}

\textbf{(b) 연산 — 평형 조건에 반응 자유에너지 대입.}
전이 $j$ 의 비배치 반응 자유에너지 $\Delta G_j^\mathrm{cat}=\Delta H_{\rxn,j}^\mathrm{cat}
-T\Delta S_{\rxn,j}^\mathrm{cat}$ 를 식~\eqref{eq:eqcond} 의 $\Delta G_j=-sFU_j$($s=+1$)에 넣으면
\[
\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}=-F\,U_j^\mathrm{cat}(T),
\]
곧 흑연 식~\eqref{eq:Ujmid} 과 글자 그대로 같은 식에 상첨자 $\mathrm{cat}$ 만 붙는다((a) 의 host-무관 확인).

\textbf{(c) 중간식 — 중심과 온도 미분(이중 경로 교차검증).}
(b)를 $U_j^\mathrm{cat}$ 로 이항하면 $U_j^\mathrm{cat}(T)=(-\Delta H_{\rxn,j}^\mathrm{cat}
+T\Delta S_{\rxn,j}^\mathrm{cat})/F$ 로 흑연 식~\eqref{eq:Uj} 와 같은 함수형이다. 온도 계수는 두 독립
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
\emph{전체 단전극 스케일}[tier B]로 역산되며, 이는 표~\ref{tab:lco-staging} 의 \emph{전이별 성분}값과 서로
다른 층위의 양이라 직접 비교하지 않는다(층위 분리 시 T1 전자항의 소수 음의 보정과도 부호 충돌이 없다).
\textbf{★다온도 전자항 주의(M-10).} $\Delta S_{e,j}(x,T)\propto T$ 인 항을 다온도 모델에 실제로 풀 때는
고정 $\Delta H$ 로 $U_j(T)=(-\Delta H+T\Delta S(T))/F$ 를 기계 미분하면 $\Delta S+T\,\partial_T\Delta S$ 가
생기므로, 열역학적으로 유지할 관계는 위 박스의 $\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}(T)/F$
이고 위치는 기준온도에서
\[
U_j^\mathrm{cat}(T)=U_j^\mathrm{cat}(T_\mathrm{ref})+\frac1F\int_{T_\mathrm{ref}}^{T}\Delta S_{\rxn,j}^\mathrm{cat}(T')\,\dd T'
\]
로 해석해야 한다(T1 의 $\Delta S_{\rxn,1}^\mathrm{cat}(T)=\Delta S_0+a_eT$ 인 경우의 닫힌형이
\S\ref{sec:lco-Se} 식~\eqref{eq:U1T2} 의 $T^2$ 항 $a_e(T^2-T_0^2)/2F$ 이며, 위 적분의 $\tfrac12$ 인자를
그대로 담는다). \textbf{(부호 좌표 고정.)} 아래 검산의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 는 반쪽반응을
\emph{삽입 방향}(Li$^+$ 가 host 로 들어옴)으로 적은 반응 엔트로피이며(표~\ref{tab:staging} 흑연 삽입 규약과
동일 좌표), 단전극 potentiometric $\dd\phi/\dd T$ 의 부호는 측정 규약 의존이므로 아래 verifybox 는 그
대표 스케일을 삽입-반응 $\Delta S_{\rxn}^\mathrm{cat}$ 로 환산해 크기$\cdot$부호 sanity 만 확인한다.
```

**원 줄글 대비 (v1.0.12 L477–494)**
- 원문: "식 (eq:Uj) 은 유도에 전극 가정이 없다 …입력 값만 바뀐다"(L477–481 단정) + bare `eq:lco-dUdT`(L484–488, "온도 의존도 같은 미분이다:" 한 줄 다리) + "대표 스케일 +0.83 mV/K → +80 J/(mol K)"(L489–494). → **(a) 세 진입의 host-무관 근거를 식으로, (b) `eq:eqcond` 대입 연산, (c) 이중경로(직접미분+Gibbs 항등식) 중간식, (d) 박스**로 승격. 물리 결론(전극불문·$\partial U/\partial T=\Delta S^\mathrm{cat}/F$·+80 스케일)은 불변, 유도 사슬만 채움.

**논리 감사 (재유도 근거)**
- **재유도 ✓**: $\Delta G_j^\mathrm{cat}=-FU_j^\mathrm{cat}$ 에서 $\Delta G=\Delta H-T\Delta S$ 대입 → $U^\mathrm{cat}=(-\Delta H^\mathrm{cat}+T\Delta S^\mathrm{cat})/F$. $T$ 미분(직접) $=\Delta S^\mathrm{cat}/F$. Gibbs 경유: $\partial_T\Delta G=-\Delta S$ 와 $\Delta G=-FU$ → $-F\partial_T U=-\Delta S$ → 동일. **두 경로 부호까지 일치**.
- **차원 ✓**: $[\Delta H/F]=$ J·mol⁻¹ / (C·mol⁻¹) = J/C = V. $[\Delta S/F]=$ J·mol⁻¹K⁻¹ / (C·mol⁻¹) = V/K. ✓
- **극한/부호 ✓**: 발열($\Delta H<0$) → 분자 $-\Delta H>0$ → 중심 상승(흑연 L462–463 규약과 동일). $\Delta S^\mathrm{cat}>0$ → 중심이 $T$ 에 상승. verifybox 의 $+80$ J/(mol K) → $+0.83$ mV/K 역산 정합(L497–500).
- **이중계산 ✓**: (d)는 중심 $U^\mathrm{cat}(T)$ 만 정의. config 봉우리 내부 항($R\ln[(1-\xi)/\xi]$)은 여기 없음 — logistic 이 별도로 담음(\S\ref{sec:dist}·\S\ref{sec:lco-decomp}). 이중계산 진입점 없음.
- **M-10 가드 ✓**: $\Delta S_e\propto T$ → $\partial_T U=\Delta S(T)/F$ 유지 + $T_\mathrm{ref}$ 적분 해석 보존, `eq:U1T2` 의 $\tfrac12$ 계수와 정합 명시(V1011 대비 개선: 일반 적분 → 구체 $T^2$ 항 링크).
- **앞 절 정합 ✓**: `eq:eqcond`(442)·`eq:Ujmid`(455)·`eq:Uj`(460) 모두 존재. `sec:lco-map`(L312) 의 $\partial U_j/\partial T=\Delta S/F$ 예고와 일치.
```

---

## 2. `sec:lco-hys` — LCO order–disorder 와 MIT 2상역

**편입 지시**: 아래 블록으로 **L697–719 를 교체**. L696 헤더 보존, L722 `sec:width` 불변. 흑연 `sec:hys` 결과식(`eq:mu`·`eq:gxi`·`eq:gpp`·`eq:spinodal`·`eq:Veq`·`eq:hyssub`·`eq:hysdiff`·`eq:dUhys`·`eq:Ubranch`)은 재유도 없이 **참조·대입만**.

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
solid-solution 이 된다(\S\ref{sec:width}$\cdot$\S\ref{sec:broadening}). LCO 는 pure-LCO 초기값에서
T1(MIT)$\cdot$T2$\cdot$T3(order--disorder) \emph{세 전이 전부}가 문턱을 넘는 상분리 후보다
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
($s=+1$)
\begin{equation}
V_{\eq,j}^\mathrm{cat}(\xi)=U_j^\mathrm{cat}
+\frac{RT}{F}\ln\frac{\xi}{1-\xi}+\frac{\Omega_j^\mathrm{cat}}{F}(1-2\xi),
\label{eq:lco-Veq}
\end{equation}
이고 두 spinodal 끝점에서 식~\eqref{eq:hyssub} 대로 $\dfrac{\xi}{1-\xi}\big|_{\xi_{s,j}^\pm}
=\dfrac{1\pm u_j^\mathrm{cat}}{1\mp u_j^\mathrm{cat}}$, $(1-2\xi)\big|_{\xi_{s,j}^\pm}=\mp u_j^\mathrm{cat}$
이므로 극대$-$극소 차는(흑연 식~\eqref{eq:hysdiff} 대입)
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
를 실제로 넣는다는 뜻이다. 방전($\sigma_d=+1$)은 분기 중심을 위로, 충전($\sigma_d=-1$)은 아래로 옮긴다.

\textbf{(T2$\cdot$T3) order--disorder.}
$x\approx0.5$ 부근 monoclinic 초격자(점유 Li 와 빈자리의 교대 정렬)를 이루는 T2($\sim$4.05 V,
hex$\to$monoclinic)$\cdot$T3($\sim$4.17--4.20 V, monoclinic$\to$hex)는 동종 이웃 인력 $\Omega_j^\mathrm{cat}>0$
이 만드는 상분리의 LCO 사례다. 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j=2,3$ 을 넣으면
T2$\cdot$T3 가 각각 열린다. \textbf{★$\Omega$ 와 config $\Delta S$ 의 구분(혼동 가드).} 정렬의
charge-order 엔트로피 변화($\approx0.47$ J/(mol\,K)@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$
[tier A, Motohashi\cite{motohashi2009}])는 \emph{엔트로피} 값으로 표~\ref{tab:lco-staging}$\cdot$
식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 슬롯(따라서 $U_j^\mathrm{cat}(T)$ 의 온도 이동)에
들어가지, spinodal 문턱을 정하는 \emph{상호작용 에너지} $\Omega_j^\mathrm{cat}$[J/mol]가 \emph{아니다} —
둘은 서로 다른 양이므로 ``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 식의 다리를 놓아선 안 되고
$\Omega_j^\mathrm{cat}$ 는 gap 을 정하는 별도 피팅 파라미터로 둔다.

\textbf{(T1) MIT 2상역.}
T1($\sim$3.90 V, $x\approx0.94$--$0.75$, 절연체$\to$금속)의 구조적 2상 공존도 같은 정규용액 문턱을 받아
식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j=1$ 을 넣어 열린다. MIT 고유의 전자 자유도는
이 히스 gap 에 새 항으로 섞지 않는다 — 그 항은 이미 $\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^\mathrm{config}
+\Delta S_1^\mathrm{vib}+\Delta S_{e,1}^\mathrm{mol}(x,T)$(식~\eqref{eq:lco-decomp})를 통해
$U_1^\mathrm{cat}(T)$ 의 온도 이동(식~\eqref{eq:lco-dUdT})에 들어간다. 곧 두 몫이 서로 다른 슬롯에 산다:
\begin{equation}
\boxed{\;
\underbrace{\Delta U_1^{\hys,\mathrm{cat}}\ \text{(구조적 2상역)}\ \Leftarrow\ \Omega_1^\mathrm{cat}}_{\text{정규용액 히스 gap (이 절)}}
\quad\Big\|\quad
\underbrace{\partial U_1^\mathrm{cat}/\partial T\ \Leftarrow\ \Delta S_{e,1}^\mathrm{mol}(x,T)}_{\text{전자 엔트로피 (\S\ref{sec:lco-electronic})}}\;}
\label{eq:lco-mit}
\end{equation}
이 분리가 config 2상역과 전자 엔트로피를 이중계산하지 않는 경계다(원 L710--713 의 ``두 몫을 분리''를
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
(흑연 식~\eqref{eq:dUhys} 아래 Taylor 극한 재사용, $\operatorname{artanh}u=u+u^3/3+\cdots$,
$T_{c,j}=\Omega_j^\mathrm{cat}/2R$)이고, $\Omega_j^\mathrm{cat,dop}\le2RT$ 로 피팅되는 전이는 같은 식 안에서
gap 이 0 으로 닫힌다 — 이것이 상전이 억제에 따른 히스 축소와 peak smear 의 수식 표현이며, 풀린 몫은
\S\ref{sec:broadening} 의 broadening 폭이 더 크게 담는다. \textbf{★슬롯 분리.} 중심 전위의 미세 shift 는
같은 전이 dict 의 $U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로} 들어가며, $\Omega_j^\mathrm{cat}$ 하나가
gap$\cdot$smear 와 중심 이동을 동시에 만든다고 쓰지 않는다.
```

**원 줄글 대비 (v1.0.12 L697–719)**
- 원문: intro "같은 정규용액 틀 그대로 적용, Ω_j 값만 정한다 · 세 전이 모두 상분리"(L697–699) + T2·T3 order-disorder 서술(L701–706) + T1 MIT 서술(L708–713) + 도핑(L715–719) — **수식 사슬 0, 대입 중간식 전무**. → 흑연 `sec:hys` 의 (a)`g_j`→(b)`g''`·spinodal→(c)`V_eq` 끝점→(d)`ΔU_hys`·`U^d` 박스를 LCO $\Omega_j^\mathrm{cat}$ 로 실제 대입. config ΔS↔Ω 혼동 가드·MIT 슬롯 분리 박스·도핑 Taylor 극한을 식으로.

**논리 감사 (재유도 근거 — V1011 계승 + O1 독립 재검산)**
- **spinodal 재유도 ✓**: $g_j''=RT/[\xi(1-\xi)]-2\Omega=0 \Rightarrow \xi(1-\xi)=RT/(2\Omega) \Rightarrow \xi^2-\xi+RT/(2\Omega)=0 \Rightarrow \xi_s^\pm=\tfrac12(1\pm u),\ u=\sqrt{1-2RT/\Omega}$. 흑연 `eq:spinodal`(560)과 동일. ✓
- **끝점 대입 재검산 ✓** (O1 손 재계산): $\xi_s^-=\tfrac12(1-u)\Rightarrow 1-2\xi_s^-=+u,\ \xi_s^-/(1-\xi_s^-)=(1-u)/(1+u)$; $\xi_s^+=\tfrac12(1+u)\Rightarrow 1-2\xi_s^+=-u,\ \xi_s^+/(1-\xi_s^+)=(1+u)/(1-u)$ — `eq:hyssub`(612)과 부호까지 일치.
- **ΔU_hys 재유도 ✓**: $V_\eq(\xi_s^-)-V_\eq(\xi_s^+)=(RT/F)[\ln\tfrac{1-u}{1+u}-\ln\tfrac{1+u}{1-u}]+(\Omega/F)[u-(-u)]=(RT/F)(-4\operatorname{artanh}u)+(\Omega/F)(2u)=\tfrac2F[\Omega u-2RT\operatorname{artanh}u]$. artanh$u=\tfrac12\ln\tfrac{1+u}{1-u}$ 사용. 흑연 `eq:dUhys`(630)과 동일. ✓
- **도핑 Taylor 극한 재검산 ✓** (O1 독립): $\Omega=2RT/(1-u^2)=2RT(1+u^2+\cdots)\Rightarrow\Omega u=2RT(u+u^3+\cdots)$; $2RT\operatorname{artanh}u=2RT(u+u^3/3+\cdots)$; 차 $=2RT(u^3-u^3/3)=\tfrac43RTu^3$; $\times\tfrac2F=\tfrac{8RT}{3F}u^3$. **8RT/3F 계수 확정** — V1011·흑연 L634 와 일치.
- **차원 ✓**: $[\Omega u/F]=$ J/mol / (C/mol) = V; $[RT\operatorname{artanh}u/F]=$ V. gap = V. ✓
- **극한/연속 ✓**: $\Omega\to2RT^+ \Rightarrow u\to0 \Rightarrow \Delta U^\hys\to0$(임계에서 매끄러운 소멸, $\propto(T_c-T)^{3/2}$). $\Omega\le2RT \Rightarrow$ gap$=0$(코드 `if Omega<=2RT: return 0.0` 분기).
- **부호 ✓**: 극대$>$극소 → $\Delta U^\hys\ge0$; $\sigma_d=+1$(방전) 중심 위, $-1$(충전) 아래 → $U^\dis>U^\chg$.
- **이중계산 가드 ✓**: `eq:lco-mit` 박스가 config 2상역(Ω_1 → gap)과 전자 엔트로피(ΔS_e,1 → ∂U_1/∂T)를 서로 다른 슬롯으로 분리. config ΔS(0.47/1.49)↔Ω_od 혼동 가드로 "엔트로피값→상호작용에너지" 잘못된 다리 차단. **★수치 날조 0** — Ω_j^cat 은 기호로만, 0.47/1.49 는 config ΔS 로만 인용.
- **앞 절 정합 ✓**: 모든 흑연 참조 라벨 v1.0.12 존재(§0.3). center (d) `eq:lco-dUdT` 와 `eq:lco-mit` 의 ∂U_1/∂T 연결 정합.
- **★v1.0.12 원문과의 정합 주의**: 원문 L698–699·lco-peak L1225 는 "세 전이 모두 두-상"으로 **단정**. 본 블록의 two-phase calibration 은 "pure-LCO 초기값에서 세 전이 전부 상분리 후보 + 최종 판정=피팅 Ω_j^cat>2RT"로 적어 물리 결론(초기 세 전이 상분리)은 보존하되 도핑 시 Ω≤2RT 케이스와의 모순을 제거(V1011 §2.6 개선 계승). 물리 불변, 프레이밍만 엄밀화.
```

---

## 3. `sec:lco-peak` — LCO dQ/dV peak (신규)

**편입 지시**: 아래 블록으로 **L1221–1232 를 교체**. L1220 헤더 보존, L1234 `sec:broadening` 불변. 흑연 `sec:eqpeak` 결과식(`eq:belliden`·`eq:eqpeak`)과 `eq:xieq`·`eq:lco-Ubranch`·`eq:lco-dUdT`·`eq:U1T2` 는 참조·대입만.

```latex
평형 peak 식~\eqref{eq:eqpeak} $(\dd Q/\dd V)^\eq_j=Q_j\,\xi_{\eq,j}(1-\xi_{\eq,j})/w_j$ 는 유도에 전극 가정이
없으므로(로그 미분 종 항등식~\eqref{eq:belliden} 과 전하 보존식만 씀), LCO 양극에도 그대로 적용된다. 흑연이
$\sim$0.085--0.21 V 에 네 봉우리를 남기듯 LCO 하프셀은 \emph{양극 전위 영역}에 세 봉우리를 남기며, 그 세 봉우리를
LCO 파라미터로 실제 대입해 닫는다.

\textbf{(a) 출발 — 전극-중립 평형 peak 에 LCO 전이 대입.}
LCO 전이 $j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}$ 는 분기 중심
$U_j^{\,d,\mathrm{cat}}$(식~\eqref{eq:lco-Ubranch})와 폭 $w_j^\mathrm{cat}=n_j RT/F$(식~\eqref{eq:wbase})를
가지므로, 평형 진행률은 흑연 식~\eqref{eq:xieq} 에 이들을 넣은
\begin{equation}
\xi_{\eq,j}^\mathrm{cat}(V,T)=\frac{1}{1+\exp\!\big[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j^\mathrm{cat}\big]}
\qquad(j\in\mathcal J_\mathrm{LCO})
\label{eq:lco-xieq}
\end{equation}
이다 — host 고유 항 없이 전이 집합$\cdot$입력값만 양극으로 치환된다.

\textbf{(b) 연산 — logistic 미분 종 항등식.}
$z_j\equiv\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j^\mathrm{cat}$ 로 식~\eqref{eq:belliden} 의 종 항등식
$\dd\xi/\dd z=\xi(1-\xi)$ 를 그대로 쓴다(전극 무관).

\textbf{(c) 중간식 — 연쇄율로 전위 미분.}
$\dd z_j/\dd V=\sigma_d/w_j^\mathrm{cat}$ 를 곱하면 전이 $j$ 의 평형 기울기가
\begin{equation}
\frac{\dd\xi_{\eq,j}^\mathrm{cat}}{\dd V}
=\frac{\sigma_d\,\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j^\mathrm{cat}}
\label{eq:lco-peakslope}
\end{equation}
로 닫힌다.

\textbf{(d) 박스 — LCO 세 봉우리의 합과 세 양.}
전하 보존식 미분($C_\bg+\sum_jQ_j\,\dd\xi_j/\dd V$)에 식~\eqref{eq:lco-peakslope} 를 넣으면 LCO 평형 dQ/dV 가
세 전이의 합으로 닫힌다:
\begin{equation}
\boxed{\;
\Big(\frac{\dd Q}{\dd V}\Big)^{\eq,\mathrm{cat}}
=C_\bg+\!\!\sum_{j\in\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\}}\!\!
Q_j\,\frac{\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j^\mathrm{cat}}
=C_\bg+\sum_j Q_j\Big|\frac{\dd\xi_{\eq,j}^\mathrm{cat}}{\dd V}\Big|\;}
\label{eq:lco-eqpeak}
\end{equation}
이며, 봉우리마다 세 양이 이 한 식에서 읽힌다:
\begin{equation}
\underbrace{V_{\mathrm{peak},j}=U_j^{\,d,\mathrm{cat}}}_{\text{위치}}
,\qquad
\underbrace{\Big(\frac{\dd Q}{\dd V}\Big)^{\eq}_{j,\max}=\frac{Q_j}{4\,w_j^\mathrm{cat}}}_{\text{순높이}(\xi=\tfrac12)}
,\qquad
\underbrace{\int(\dd Q/\dd V)^\eq_j\,\dd V=Q_j}_{\text{배경 차감 면적}(\int_0^1\dd\xi=1)}.
\label{eq:lco-peak3}
\end{equation}
곧 T1 은 $\sim$3.90 V(MIT plateau), T2 는 $\sim$4.05 V, T3 는 $\sim$4.17--4.20 V(T2 와 한 쌍의 좁은
order--disorder 봉우리)에 놓인다. 부호 — $\sigma_d$ 가 미분에 한 번 들어오나 peak 모양은 절댓값
$|\dd\xi/\dd V|=\xi(1-\xi)/w\ge0$ 로 양수이고 방향 불변이다(흑연 L1212--1213 와 동일).

\textbf{★두-상 폭의 지위.} LCO 세 전이가 모두 $\Omega_j^\mathrm{cat}>2RT$ 의 두-상이면, 그 폭 $w_j^\mathrm{cat}$
은 \S\ref{sec:width} 이중지위의 \emph{두-상} 측 — 평형 예측이 아니라 broadening 이 정하는 현상학적 자유 피팅
폭이다(\S\ref{sec:broadening}). order--disorder 의 큰 $\Omega_j^\mathrm{cat}$ 은 spinodal gap
(식~\eqref{eq:lco-dUhys})을 키워 T2$\cdot$T3 를 흑연보다 날카로운 좁은 한 쌍 peak 로 만든다.
\textbf{★T1 전자항의 온도 신호.} T1 의 위치 $V_{\mathrm{peak},1}=U_1^{\,d,\mathrm{cat}}(T)$ 는
\S\ref{sec:lco-electronic} 의 전자항이 $\Delta S_{\rxn,1}^\mathrm{cat}$ 를 통해 $U_1(T)$ 의 \emph{온도 이동}에
기여하므로(식~\eqref{eq:lco-dUdT}), 다온도 dQ/dV 에서 T1 봉우리의 \emph{온도 이동률} $\partial U_1/\partial T$
가 $T$ 에 선형으로 커지는 것이 전자항의 관측 신호다($\Delta S_{e,1}\propto T$, \S\ref{sec:lco-Se}) — 위치
자체가 $T$-선형이 아니라 \emph{이동률}이 $T$-선형, 곧 위치 이동은 $\propto T^2$(식~\eqref{eq:U1T2}). 도핑은
\S\ref{sec:lco-hys} 대로 봉우리를 smear$\cdot$shift 시킨다(식~\eqref{eq:lco-dope}).
```

**원 줄글 대비 (v1.0.12 L1221–1232)**
- 원문: "평형 peak 식 (eq:eqpeak) 은 전극 무관 → LCO 세 봉우리, 위치=U^d·순높이=Q/4w·면적=Q"(L1221–1224 줄글 열거) + "폭은 두-상 현상학적"(L1225–1227) + "T1 온도 이동률 T-선형, 위치 ∝T²"(L1228–1232). → **(a) LCO `ξ_eq^cat` 대입, (b) 종 항등식, (c) 연쇄율 기울기, (d) 세 봉우리 합 박스 + 세 양(위치·순높이·면적) 명시식**으로 승격. 물리(세 봉우리 위치·순높이·면적·두-상 폭·T1 신호)는 불변.

**논리 감사 (재유도 근거)**
- **종 항등식 재유도 ✓**: $\xi=(1+e^{-z})^{-1}\Rightarrow \dd\xi/\dd z=e^{-z}/(1+e^{-z})^2=\xi(1-\xi)$(흑연 `eq:belliden`(1198)). 연쇄율 $\dd z/\dd V=\sigma_d/w$ → `eq:lco-peakslope`. ✓
- **세 양 재검산 ✓**: 순높이 $\xi(1-\xi)|_{\xi=1/2}=\tfrac14 \Rightarrow Q_j/(4w_j)$; 면적 $\int Q_j\,\xi(1-\xi)/w\,\dd V=Q_j\int_0^1\dd\xi=Q_j$(치환 $\dd\xi=(\xi(1-\xi)/w)\dd V$, `eq:belliden` 종이 dξ 의 치환적분). 흑연 L1214–1215 와 동일. ✓
- **차원 ✓**: $[Q_j\,\xi(1-\xi)/w_j]=$ C / V = C/V(=dQ/dV). ✓ $[Q_j/(4w)]=$ C/V. ✓
- **부호/방향 불변 ✓**: peak $=|\dd\xi/\dd V|\ge0$, $\sigma_d$ 소거되어 방향 불변($\xi(1-\xi)\ge0$).
- **이중계산 없음 ✓**: peak 은 $U_j^{d,\mathrm{cat}}$·$w_j^\mathrm{cat}$·$Q_j$ 만 씀. 전자항은 peak 에 새 항으로 더하지 않고 오직 $U_1(T)$ 위치 이동으로만 들어옴(hys `eq:lco-mit` 슬롯 분리와 정합) — peak-내 전자항 이중계상 진입점 없음.
- **앞 절 정합 ✓**: 중심 $U_j^{d,\mathrm{cat}}$ = hys `eq:lco-Ubranch` 출력; T1 온도 이동 = center `eq:lco-dUdT`·`eq:U1T2`; 폭 두-상 지위 = `sec:width`·`sec:broadening`. 모두 앞 절 결과 재사용, 재유도 중복 없음.
- **★신규 개념 0**: ρ(U_app)/PSD/입자반경 도입 없음 — 두-상 폭 지위만 `sec:broadening` 참조로 인용.
```

---

## 4. `sec:lco-decomp` — $\Delta S_{\rxn,j}^\mathrm{cat}$ 분해 (신규 사슬)

**편입 지시**: intro **L1716–1718 을 아래 (a)(b) 블록으로 교체**하여 $Z$-인수분해 유도를 채우고, 기존 `eq:lco-decomp` 박스(L1719–1724)는 (c) 결과로 **그대로 유지**(재사용), 박스 직후에 (d) 무이중계산 박스 `eq:lco-noDC` 를 **삽입**한다. 이후 itemize(L1725–1748)·세 몫 합(L1750–1754)·Ch2예고(L1756–1765)는 보존. `eq:lco-decomp` 라벨 불변.

```latex
% ── (a)(b) 블록: L1716–1718 교체 ──
흑연에서 합산식~\eqref{eq:sum} 에 들어가는 $\Delta S_{\rxn,j}$ 는 평형 중심 $U_j(T)$ 를 통해 한 덩이로
작용했다. LCO 양극에서는 이 한 덩이가 세 물리 성분의 합임을 명시하되, 그 합이 왜 \emph{단순 덧셈}으로
정당한지를 분배함수의 인수분해에서 닫는다(식과 코드 경로는 그대로이고 $U_j(T)$ 의 $\Delta S$ \emph{내부
분해}만 더한다).

\textbf{(a) 출발 — 세 자유도, 세 분배함수.} 삽입 반응의 엔트로피는 세 자유도가 정한다 — 리튬 자리의 \emph{점유
배열}(config), 격자의 \emph{진동}(vib), 전도 전자의 \emph{밴드 점유}(electronic). 세 부분계가 선도 차수에서
독립이면 전체 분배함수는 곱으로 인수분해된다:
\begin{equation}
Z=Z_\mathrm{config}\cdot Z_\mathrm{vib}\cdot Z_\mathrm{elec}
\qquad(\text{선도 차수 독립, MIT 결합(교차)항은 선도에서 무시}).
\label{eq:lco-Zfact}
\end{equation}

\textbf{(b) 연산 — 곱 $\to$ 합.} 자유에너지 $F=-k_BT\ln Z$ 는 로그로 합이 되고($\ln Z=\ln Z_\mathrm{config}
+\ln Z_\mathrm{vib}+\ln Z_\mathrm{elec}$), 엔트로피 $S=-\partial F/\partial T$ 는 성분별 합이 된다:
$S=S_\mathrm{config}+S_\mathrm{vib}+S_\mathrm{elec}$(교차 엔트로피 항은 선도 차수에서 $0$). 삽입당
($\partial/\partial x$) 반응 엔트로피로 옮기면 세 성분의 합이다.

% ── (c) 결과 = 기존 eq:lco-decomp 박스(L1719–1724) 유지 ──
\begin{equation}
\boxed{\;\Delta S_{\rxn,j}^\mathrm{cat}(x,T)=\underbrace{\Delta S_j^\mathrm{config}}_{\text{logistic }w=RT/F\text{ 가 담음}}
+\underbrace{\Delta S_j^\mathrm{vib}}_{\text{음의 baseline}}
+\underbrace{\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)}_{\text{MIT 게이트, 삽입 기준 }<0,\ \propto T\ (\text{몰당 식~\eqref{eq:dSemolar}})}\;.}
\label{eq:lco-decomp}
\end{equation}

% ── (d) 무이중계산 박스: eq:lco-decomp 직후 삽입 ──
\textbf{(d) 박스 — 슬롯 정의(무이중계산).} 식~\eqref{eq:lco-Zfact} 의 인수분해는 ``더해도 되는가''(가산성)만
보장하고, ``과대 계상 없는가''(무초과)는 각 슬롯에 자기 자유도의 몫만 \emph{한 번씩} 넣어 보장한다:
\begin{equation}
\boxed{\;
\Delta S_{\rxn,j}^\mathrm{cat}\big|_\text{슬롯입력}
=\underbrace{\Delta S_j^0}_{\substack{\text{config 중심 표준값}\\ \xi_j=\tfrac12\text{ 서 config}=0}}
+\ \Delta S_j^\mathrm{vib}
+\underbrace{\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)}_{\text{MIT 게이트 골만}}
\ ,\qquad
\underbrace{\frac{R}{F}\ln\frac{1-\xi_j}{\xi_j}}_{\text{봉우리 내부 config = logistic 자동 생성}}\ \text{는 슬롯에 재입력 금지}\;}
\label{eq:lco-noDC}
\end{equation}
곧 config 슬롯에는 봉우리 \emph{중심 표준값} $\Delta S_j^0$ 만, elec 슬롯에는 MIT 게이트 \emph{골}만 넣는다 —
봉우리 \emph{내부}의 조성 의존 config 항은 logistic 점유 분포(\S\ref{sec:dist})가 이미 담으므로 두 번 더하면
이중계산이다(★이중계산 금지 B). 표~\ref{tab:lco-staging} 의 config 값은 이 중심 표준값 $\Delta S_j^0$ 로 읽는다.
```

**원 줄글 대비 (v1.0.12 L1716–1741)**
- 원문: intro "한 덩이가 세 성분의 합"(L1716–1718) + `eq:lco-decomp` 박스(L1719–1724) + itemize 안에 "$Z=Z_\mathrm{config}\!\cdot\!Z_\mathrm{elec}$ 인수분해 → $S=S_\mathrm{config}+S_\mathrm{elec}$"(L1734–1735 **줄글**) + (가)가산성/(나)무이중계산(L1732–1741 줄글 검산). → **(a) 세 분배함수, (b) 곱→합 연산, (c) 분해 박스(기존 재사용), (d) 무이중계산 슬롯 박스**로 승격. 줄글로만 있던 인수분해·슬롯 규칙을 식으로.

**논리 감사 (재유도 근거)**
- **인수분해→가산 재유도 ✓**: 독립 부분계 $Z=\prod_k Z_k \Rightarrow F=-k_BT\ln Z=\sum_k F_k \Rightarrow S=-\partial F/\partial T=\sum_k S_k$. 교과서 표준(교차항=상관, 독립 극한서 0). 원문 L1734–1738 의 주장과 동일, 식으로 명시.
- **무이중계산 재검산 ✓**: 측정 부분몰 config $=\Delta S_j^0+(R/F)\ln[(1-\xi)/\xi]$ 중, 슬롯엔 $\Delta S_j^0$(중심, $\xi=\tfrac12$ 서 $\ln 1=0$)만; 봉우리 내부 로그항은 logistic 이 `sec:config`/`sec:dist` 에서 자동 생성 → 슬롯 재입력 시 이중. `eq:lco-noDC` 가 이를 못박음. 중심에서 config$=0$ 이라 두 정의가 모순 없이 맞물림(파생 B 일관).
- **부호 ✓**: $\Delta S_{e,j}^\mathrm{mol}<0$(삽입 기준, `eq:dSemolar`·`eq:dSegate`); vib 음 baseline; config 중심값은 표~\ref{tab:lco-staging} 부호. 합의 대표 스케일 $+80$ J/(mol K)(center verifybox)과 T1 전자항 국소 골($\approx-46$)이 층위 분리로 공존(center L507–515 정합).
- **차원 ✓**: 세 항 모두 J/(mol K). `eq:dSemolar` 의 $N_A k_B^2=Rk_B$ 몰당 환산 후 정합(전자항 단위 다리는 `sec:lco-Se` 소관, 여기선 참조만).
- **가법성 한계 정직 ✓**: MIT 부근 config↔밴드 결합(교차)항은 선도 차수 무시(원 L1735–1738 유지) — "슬롯 분리가 교차항을 포착·한계짓는 게 아니라 선도서 무시"라는 정직 서술 보존, 과대주장 없음.
- **앞 절 정합 ✓**: `eq:dSemolar`(1038)·`eq:dSegate`(1105)·`eq:sum`(1682)·`tab:lco-staging`(336)·`sec:dist`(870) 존재. 세 몫 합→`eq:lco-dUdT`→`eq:sum` 경로(L1750–1751) 불변.
- **불가침 준수 ✓**: `sec:lco-Se`·`sec:lco-electronic`·`sec:lco-gate` 의 $S_e$ 유도는 **재유도 없이 참조만** — decomp 은 분해·슬롯만 다룸.
```

---

## 5. 전자항 plug-in — $x{=}x(\xi_{\eq,1}(V))\to\Delta S_{e,1}\to\Delta S_{\rxn,1}\to U_1(T)\to$ dQ/dV (신규 사슬)

**편입 지시**: `sec:lco-code` 의 (i)(ii) enumerate(L1781–1789) 직후, `전체 입력 인자` subsection(L1794) **앞에 아래 블록을 삽입**한다. decomp 의 Ch2예고 (i) 좌표 매핑(L1757–1760)은 이 사슬의 (a)(b)와 정합하므로 보존(중복 아님 — 예고 ↔ 여기 실제 사슬). `eq:dSemolar`·`eq:dSegate`·`eq:ggate`·`eq:lco-xieq`·`eq:lco-decomp`·`eq:lco-dUdT`·`eq:U1T2`·`eq:lco-eqpeak` 참조만.

```latex
\textbf{전자항 plug-in 의 forward 사슬(좌표 다리 포함).} 항목 (ii) 의 ``T1 $\Delta S_\rxn$ 에 몰당 식을 더하는 한
줄''을 실제 코드 좌표에서 닫는다. 걸림돌은 하나 — 전자항은 \emph{조성} $x$ 의 함수인데(게이트 인자
$z=(x-x_\mathrm{MIT})/\Delta x_\mathrm{MIT}$), 코드 \code{dqdv} 는 \emph{전압} 격자 위에서 돈다.

\textbf{(a) 출발 — 조성 함수 전자항.} 몰당 게이트 닫힌식(식~\eqref{eq:dSegate}$\cdot$몰당 환산~\eqref{eq:dSemolar})
$\Delta S_{e,1}^{\,\mathrm{mol}}(x,T)=-\tfrac{\pi^2}{3}R\,(k_BT/e_V)\,(g_{\max}/\Delta x_\mathrm{MIT})\,
\sigma(z)[1-\sigma(z)]$ 는 $x$ 의 함수다.

\textbf{(b) 연산 — 좌표 다리 $x=x(\xi_{\eq,1}(V))$.} T1 전이의 평형 진행률 $\xi_{\eq,1}(V)$
(식~\eqref{eq:lco-xieq})이 그 전이 구간의 정규화 조성에 대응하므로, 게이트 인자에 조성을 진행률로 잇는다:
\begin{equation}
x=x\big(\xi_{\eq,1}(V,T)\big)\ \Longrightarrow\
z(V,T)=\frac{x(\xi_{\eq,1}(V,T))-x_\mathrm{MIT}}{\Delta x_\mathrm{MIT}}
\label{eq:lco-xmap}
\end{equation}
로 $V$ 격자 위에서 $\Delta S_{e,1}$ 를 평가한다(별도 상태변수 없이 T1 진행률 매핑).

\textbf{(c) 중간식 — 슬롯 합성 후 중심 온도 이동.} 전압 격자 위 전자항을 T1 슬롯에 무이중계산으로 합성
(식~\eqref{eq:lco-noDC})하면
$\Delta S_{\rxn,1}^\mathrm{cat}(V,T)=\Delta S_1^0+\Delta S_1^\mathrm{vib}+\Delta S_{e,1}^{\,\mathrm{mol}}(x(\xi_{\eq,1}(V)),T)$
이고, 이 합이 식~\eqref{eq:lco-dUdT} 를 통해 중심 온도 이동에 들어간다. 전자항이 $\propto T$ 이므로(M-10)
$\Delta S_{\rxn,1}^\mathrm{cat}(T)=\Delta S_0+a_eT$ 형이고, $\partial U_1/\partial T=\Delta S_{\rxn,1}^\mathrm{cat}(T)/F$
를 기준온도에서 적분한 위치는 식~\eqref{eq:U1T2} 의 $T^2$ 닫힌형
$U_1(T)=U_1(T_0)+\tfrac{\Delta S_0}{F}(T-T_0)+\tfrac{a_e}{2F}(T^2-T_0^2)$ 다($\tfrac12$ 계수 보존).

\textbf{(d) 박스 — 한 항이 위치를 옮기고, 나머지는 흑연 그대로.}
\begin{equation}
\boxed{\;
\Delta S_{e,1}^{\,\mathrm{mol}}(x,T)\ \xrightarrow{\ \eqref{eq:lco-dUdT}\ }\ U_1^{\,d,\mathrm{cat}}(T)\
\xrightarrow{\ \eqref{eq:lco-xieq}\ }\ \xi_{\eq,1}^\mathrm{cat}(V,T)\
\xrightarrow{\ \eqref{eq:lco-eqpeak}\ }\ \Big(\frac{\dd Q}{\dd V}\Big)^{\eq,\mathrm{cat}}\;}
\label{eq:lco-plugin}
\end{equation}
곧 전자항은 dQ/dV 에 \emph{새 가산 항}으로 들어가지 않고 오직 T1 중심 $U_1(T)$ 의 \emph{온도 이동}으로만 발현한다
— 구조 변경 0, ``파라미터 교체 + 한 항''이 코드 측 결론이다. \textbf{★단위 가드.} 슬롯 $\Delta S_{\rxn,1}$ 는
J/(mol\,K) 라 \emph{몰당} 식~\eqref{eq:dSemolar}($N_A$ 곱)을 넣어야 하며, 자리당 식~\eqref{eq:dSe}
($k_B^2\,g$)를 그대로 넣으면 $N_A(\approx6\times10^{23})$ 배 과소다($e_V$ 환산은 식~\eqref{eq:gunit}
\emph{나눗셈} 형). \textbf{★round-trip 가드.} T1 위치 $U_1(298)\approx3.90$ V 와 $\partial U_1/\partial T$ 의
부호$\cdot$기울기(다온도 이동률)를 self-test 로 맞춰 초기값을 신뢰값으로 승격한다(흑연 $\Delta S_\rxn$
round-trip 절차와 동격).
```

**원 줄글 대비 (v1.0.12 L1757–1760 + L1784–1789)**
- 원문: decomp 예고 "(i) 좌표 매핑 $x\!\leftrightarrow\!\xi_{\eq,1}(V)$"(L1757–1760 줄글) + lco-code (ii) "T1 $\Delta S_\rxn$ 에 몰당 식 더하는 한 줄 + 단위 주의 $N_A$"(L1784–1788 줄글). → **(a) 조성 함수, (b) 좌표 다리 식, (c) 슬롯 합성·$T^2$ 중심 이동, (d) forward 사슬 박스**로 승격. 물리(좌표 매핑·몰당 환산·전자항이 위치 이동으로만 발현)는 불변.

**논리 감사 (재유도 근거)**
- **forward 방향 정합 ✓**: $\Delta S_{e,1}\to U_1(T)\to\xi_{\eq,1}\to$ dQ/dV — 각 화살표가 기존 박스(`eq:lco-dUdT`→`eq:lco-xieq`→`eq:lco-eqpeak`) 재사용. 역산 없음(forward-only).
- **좌표 다리 자기일관 ✓**: $\xi_{\eq,1}(V)$ 는 $U_1^{d,\mathrm{cat}}$ 에 의존하고 $U_1$ 은 다시 $\Delta S_{e,1}(x(\xi_{\eq,1}))$ 에 의존 → **암시적 자기참조**. 이는 코드가 $T_\mathrm{ref}$ 동결 근사(현행 tab:lco-staging L333–335: $\Delta S_e$ 를 $T_\mathrm{ref}$ 에서 상수 오프셋)로 1-pass 평가하거나 다온도 round-trip 에서 self-consistent 로 푸는 문제로, 원문 L333–335·L1756–1765 의 "단일-기준 근사 → 다온도 피팅 과제 분리"와 정합. **과대주장 회피**: (b)는 좌표 다리만 세우고 self-consistency 는 피팅 단계로 위임(원문 스코프 보존).
- **M-10 가드 ✓**: $\Delta S_e\propto T$ → 선형 $U(T)$ 아니라 $T^2$ 곡률, `eq:U1T2` $\tfrac12$ 계수 명시 재사용. center (d)와 동일 해석.
- **단위 재검산 ✓**: 자리당→몰당 $N_A$ 곱(`eq:dSemolar`, $N_Ak_B^2=Rk_B$), eV→J 는 `eq:gunit` 나눗셈. $N_A$ 누락 시 $\sim10^{23}$ 과소(원 L1787 정합).
- **이중계산 없음 ✓**: 전자항은 T1 슬롯(`eq:lco-noDC`)에만 1회, dQ/dV 에 별도 가산 항 없음(hys `eq:lco-mit`·peak 슬롯 분리와 삼중 정합).
- **앞 절 정합 ✓**: `eq:dSe`(1028)·`eq:dSemolar`(1038)·`eq:dSegate`(1105)·`eq:ggate`(1090)·`eq:gunit`(1046)·`eq:U1T2`(1075) 모두 `sec:lco-Se`/`sec:lco-gate` 에 존재 — **재유도 없이 참조만**(불가침 준수).
```

---

## 6. MSMR 동형 — `eq:msmr` $\to$ 정규화 $\to$ $f{=}{-}\sigma_d$ 대입 $\to$ $\xi_{\eq,j}$ $\to$ peak (신규 사슬)

**편입 지시**: `sec:lco-code` 의 `eq:msmr`(L1770–1772) 직후 줄글 동형 서술(L1774–1780)을 아래 (a)–(d) 사슬로 **augment**(대체 아님 — eq:msmr 박스 유지, 줄글 대응표를 대입 사슬로 승격). `eq:msmr`·`eq:xieq`·`eq:lco-eqpeak` 참조.

```latex
\textbf{(a) 출발 — MSMR 종 분율.} MSMR 식~\eqref{eq:msmr}
$x_j=X_j/\{1+\exp[\,f(U-U_j^0)/\omega_j\,]\}$ 는 양극 전위를 전이별 logistic 의 합으로 적는다.

\textbf{(b) 연산 — 용량 가중으로 정규화.} 양변을 $X_j$ 로 나누면 순수 logistic 이 드러난다:
\begin{equation}
\frac{x_j}{X_j}=\frac{1}{1+\exp[\,f(U-U_j^0)/\omega_j\,]}.
\label{eq:lco-msmrnorm}
\end{equation}

\textbf{(c) 중간식 — 대응 대입과 방향 부호($f{=}{-}\sigma_d$).} Ch1 식~\eqref{eq:xieq} 의 지수는
$-\sigma_d(V-U_j^{\,d})/w_j$, MSMR 지수는 $+f(U-U_j^0)/\omega_j$ 다. 같은 자리(같은 $U{=}V$)를 채우므로 네 대응
\[
X_j\leftrightarrow Q_j,\quad U_j^0\leftrightarrow U_j^{\,d},\quad \omega_j\leftrightarrow w_j,\quad f\leftrightarrow-\sigma_d
\]
을 넣으면 지수 부호가 정확히 맞아($+f=-\sigma_d\Rightarrow f=-\sigma_d$)
\begin{equation}
\frac{x_j}{X_j}\ \xrightarrow{\ (X,U^0,\omega,f)\mapsto(Q,U^d,w,-\sigma_d)\ }\
\frac{1}{1+\exp[-\sigma_d(V-U_j^{\,d})/w_j]}=\xi_{\eq,j}
\label{eq:lco-msmrmap}
\end{equation}
곧 MSMR 종 분율(정규화)이 Ch1 의 전이별 logistic 평형 진행률 식~\eqref{eq:xieq} \emph{그 자체}다 — 탈리튬화/
리튬화 진행 방향이 두 모델에서 $f=-\sigma_d$ 로 일관되게 맞춰진다.

\textbf{(d) 박스 — 같은 코드가 LCO 를 그린다.} 식~\eqref{eq:lco-msmrmap} 을 $V$ 로 미분하면 종 항등식으로 곧장
LCO 평형 peak 식~\eqref{eq:lco-eqpeak} 이 나온다:
\begin{equation}
\boxed{\;
x_j/X_j\ \equiv\ \xi_{\eq,j}\ (\text{식~\eqref{eq:xieq}})
\ \Longrightarrow\
\Big(\frac{\dd Q}{\dd V}\Big)^{\eq,\mathrm{cat}}=C_\bg+\sum_{j}Q_j\,\frac{\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j^\mathrm{cat}}\;}
\label{eq:lco-msmrpeak}
\end{equation}
따라서 Ch1 의 곡선 클래스(\code{func\_ksi\_eq}$\cdot$\code{func\_U\_j}$\cdot$합산~\eqref{eq:sum})는 \emph{구조 변경
0}으로 LCO 에 적용되며, 바뀌는 것은 단 둘 — (i) 전이 파라미터 교체(\code{GRAPHITE\_STAGING\_LIT}$\to$
\code{LCO\_MSMR\_LIT}), (ii) T1 전자항 plug-in(식~\eqref{eq:lco-plugin})이다. 이것이 ``흑연 forward 교과서가
LCO 양극까지 한 틀로 닫힌다''의 코드 측 증거다.
```

**원 줄글 대비 (v1.0.12 L1774–1780)**
- 원문: `eq:msmr` 박스 + "구조가 동형이다 — $X_j\!\leftrightarrow\!Q_j$, $U_j^0\!\leftrightarrow\!U_j^d$, $\omega_j\!\leftrightarrow\!w_j$, $f\!\leftrightarrow\!-\sigma_d$; 두 지수 비교로 $f=-\sigma_d$"(L1774–1780 줄글 대응표). → **(a) MSMR 종분율, (b) $X_j$ 정규화, (c) 대응 대입 + 부호 맞춤 $f{=}{-}\sigma_d$, (d) 미분→peak 박스**로 승격. 결론(동형·구조변경0·둘만 바뀜)은 불변.

**논리 감사 (재유도 근거)**
- **정규화 재유도 ✓**: $x_j=X_j/(1+e^{f(U-U_j^0)/\omega_j})\Rightarrow x_j/X_j=1/(1+e^{f(U-U_j^0)/\omega_j})$ — 순수 logistic.
- **부호 맞춤 재검산 ✓**: 두 지수 $+f(U-U_j^0)/\omega_j$ vs $-\sigma_d(V-U_j^d)/w_j$ 가 같은 함수이려면 $f/\omega_j\cdot(U-U_j^0)=-\sigma_d/w_j\cdot(V-U_j^d)$; $U{=}V$·$U_j^0{=}U_j^d$·$\omega_j{=}w_j$ 대응 하에서 $f=-\sigma_d$. 원 L1776–1778 과 일치, $f{=}\pm1$·$\sigma_d{=}\pm1$ 정합.
- **peak 도출 ✓**: $x_j/X_j=\xi_{\eq,j}$ 를 $V$ 미분 → `eq:belliden` 종 → `eq:lco-peakslope`·`eq:lco-eqpeak`. §3 결과 재사용(중복 유도 없음).
- **차원/방향 ✓**: $x_j/X_j$ 무차원 = $\xi$ 무차원. peak $\ge0$ 방향 불변(§3 정합).
- **앞 절 정합 ✓**: `eq:msmr`(1772)·`eq:xieq`(788)·`eq:sum`(1682) 존재. peak 박스는 §3 `eq:lco-eqpeak` 와 동일식 재확인 — 상호 정합.
- **★유의**: MSMR $x_j$ 는 종 \emph{분율}(리튬 함량 몫), Ch1 $\xi$ 는 \emph{탈리튬화 진행률} — 정규화 $x_j/X_j$ 와 $\xi$ 가 같은 logistic 이라는 것은 \emph{함수형 동형}이지 물리량 동일이 아니다(부호 인자 $f=-\sigma_d$ 가 진행 방향을 흡수). 이 구분을 (c)에서 "같은 자리를 채운다"로 명시해 오독 방지.
```

---

## 7. H-2 정정문안 (Ch2 챕터 내부 모순 일원화)

**대상**: `graphite_ica_ch2_v1.0.12.tex`. **근거**: `FABLE_REAUDIT_C4_note.md` §2(CRITICAL — $w_j$ 열적 스케일링 지위의 구조적 자기모순). **성격**: 물리·결과식·부호·수치 **불변**, H-2 한정어만 추가(식 변경 0).

### 7.1 모순 진단 (v1.0.12 실측 3지점)
1. **§ssec:logistic keybox(L161–166)**: "logistic 폭 $w=RT/F$ 는(자리당 $n_j{=}1$ 기준; 전이별 유효 폭 $w_j=n_jRT/F$ 는 §sec:revheat·코드 `func_w`) **임의 모수가 아니라** 단일 자리 2-상태 분배함수~\eqref{eq:Z1} 가 정하는 분포의 열적 폭이다." — $w_j=n_jRT/F$ 를 **평형이 확정한 형태**로 단정.
2. **§ssec:weff/파생 C(L547–557)** + **§sec:revheat 종합식 keybox(L683–685)**: "두-상($\Omega>2RT$, **흑연 staging 전이가 여기 속함**)…평형 예측 $nRT/F$ 가 **아니라** 다온도 $dQ/dV$ 로 피팅하는 현상학적 자유 폭이다." — 같은 흑연 staging 전이에 대해 $n_jRT/F$ 를 **명시 부정**.
3. **파생 A 수치검증 srcbox(L485–496)**: "Chapter 1 코드의 4-전이 흑연 staging 파라미터"로 완전식=FD 부동소수점 일치 검증. 이 검증은 $w_j(T)=n_jRT/F$(곧 $\partial w_j/\partial T=n_jR/F$ 열적 스케일)를 **전제**해야 성립(코드 `func_w=n*R*T/F` 가 모든 전이에 강제). → §ssec:logistic 편만 실현, §ssec:weff 편은 텍스트로만 주장.

### 7.2 일원화 원리 (모순 해소의 축)
두 서술은 **폭의 서로 다른 두 측면**을 말한다 — 섞여서 모순처럼 보였다:
- **T-의존 함수형(열적 스케일 $w_j\propto T$, 기울기 $n_jR/F$)**: 단일 자리 분배함수~\eqref{eq:Z1} 가 정하고, 코드 `func_w` 가 **모든 전이(두-상 포함)에 공통으로 두는 모델 선택**. → §ssec:logistic·파생 A 가 의존하는 것.
- **폭의 진폭(다중도 $n_j$, 곧 기준온도의 $w$ 값)**: 단상은 평형이 예측(검증 가능), **두-상은 평형이 델타를 예측하므로 진폭이 broadening 이 정하는 현상학적 자유 피팅값**. → §ssec:weff 가 부정한 것은 "진폭이 평형 예측"이라는 주장이지 열적 함수형이 아니다.

곧 **분배함수가 정하는 것 = 폭의 열적 함수형**, **두-상에서 자유 피팅되는 것 = 그 진폭**. 코드에는 열적 함수형을 벗어난(T-동결) 폭을 실현할 경로가 없으므로(`func_w` 유일), 파생 A 의 "완전식=FD" 는 **그 열적-스케일 함수형 가정 하의 조건부 검증**이다(FABLE 시뮬레이션: T-동결 가정이면 단순식이 FD 와 일치하고 완전식이 ~0.3 mV/K 빗나가 두 오차가 자리바꿈).

### 7.3 정정문안 (finalizer 편입용)

**(A) §ssec:logistic keybox 교체 (L161–166)** — "단상 한정" 한정어 + 두-상 진폭/함수형 분리:
```latex
\begin{keybox}
Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라 \emph{격자기체 점유 분포의 여집합}(탈리튬화
진행률 $=1-\theta$)이다. logistic 폭 $w=RT/F$ 는 \emph{단상($\Omega\le2RT$, 연속 고용체) 전이에 한해} 임의
모수가 아니라 단일 자리 2-상태 분배함수~\eqref{eq:Z1} 가 정하는 분포의 열적 폭이다(검증 가능한 평형 예측).
\emph{두-상($\Omega>2RT$, 흑연 staging 전이가 여기 속함)} 전이에서는 폭의 \emph{진폭}(다중도 $n_j$, 곧
기준온도의 $w$ 값)이 평형 예측이 아니라 broadening 이 정하는 \emph{현상학적 자유 피팅 파라미터}이며(파생 C
\S\ref{ssec:weff}$\cdot$Chapter 1 broadening 절), 다만 그 \emph{$T$-의존 함수형}(열적 스케일
$w_j=n_jRT/F$, 곧 $\partial w_j/\partial T=n_jR/F$)은 코드 \texttt{func\_w} 가 모든 전이에 공통으로 두는 모델
선택이다. 곧 분배함수~\eqref{eq:Z1} 가 정하는 것은 폭의 \emph{열적 함수형}이고, 두-상에서 자유 피팅되는 것은
그 \emph{진폭}이다 — 이 이중지위는 Chapter 1 \S\ref{sec:width} 의 폭 이중지위와 일치한다. ★표기: $\theta=$ Li
점유율(만충서 1), $\xi=1-\theta=$ 탈리튬화 진행률(희박서 1); 둘은 같은 점유 분포의 두 이름이다. Chapter 2 는
이 분포를 결론이 아니라 출발점으로 삼아 엔트로피를 쌓는다.
\end{keybox}
```

**(B) 파생 A srcbox 전제 명시 (L485–496)** — 검증 전제(코드 열적 스케일 강제)를 srcbox 앞머리에 추가:
```latex
% srcbox 첫 문장 앞에 삽입:
★\textbf{검증 전제.} 이 수치 검증은 코드 \texttt{func\_w}$=n_jRT/F$ 가 \emph{모든} 전이(두-상 흑연 staging
포함)에 강제하는 열적 스케일($\partial w_j/\partial T=n_jR/F$) 하에서 수행된다 — 코드에는 이 함수형을 벗어난
$T$-동결 폭을 실현할 경로가 없다. 따라서 아래 ``완전식$=$FD 부동소수점 일치''는 그 \emph{열적-스케일 함수형
가정에 조건부}이며, ``완전식이 무조건 옳다''가 아니라 ``코드가 실현하는 열적-스케일 폭 하에서 봉우리 내부
config 항이 완전식을 FD 로 닫는다''를 검증한다(만약 두-상 폭이 $T_\mathrm{ref}$ 에서 동결된 $T$-무관
현상학적 폭이라면 오히려 \emph{단순식}이 FD 와 일치하고 완전식이 $\sim0.3$ mV/K 빗나가 두 formula 오차가
자리바꿈한다).
```
그리고 srcbox 직후 warnbox 추가(선택, 정합 강화):
```latex
\begin{warnbox}
\textbf{$w_j$ 지위와 검증 범위.} 파생 A 는 폭의 \emph{함수형}(열적 스케일)을 코드대로 고정한 채 봉우리 내부
config 항의 기여를 검증한 것이고, 두-상 폭의 \emph{진폭}이 현상학적 피팅이라는 파생 C \S\ref{ssec:weff} 의
지위와 모순되지 않는다 — 진폭(자유)과 함수형(고정)은 다른 층위다. 진폭이 실제로 $T$ 에 선형인지(=열적 스케일이
물리적으로 옳은지)의 실측 확정은 다온도 $dQ/dV$ round-trip 피팅의 과제로 남는다(공백으로 명시).
\end{warnbox}
```

**(C) 챕터 간 정합 문장 (§sec:revheat 종합식 keybox L683–685 보강, 선택)** — 이미 "단상 평형 예측 / 두-상 현상학적 피팅"으로 적혀 있어 (A)(B)와 정합. 한 구절만 추가 권장: "여기서 '현상학적 자유 폭'은 폭의 \emph{진폭}을 뜻하며, 그 $T$-의존 함수형($w_j=n_jRT/F$)은 §ssec:logistic·코드 `func_w` 가 고정한다(파생 A 검증 전제)."

### 7.4 H-2 논리 감사
- **일원화 정합 ✓**: (A)(B)(C) 세 지점이 이제 한 결론(함수형=분배함수 고정, 진폭=두-상 자유 피팅)을 가리킨다. §ssec:logistic("임의 아님")과 §ssec:weff("현상학적 자유")가 각각 함수형·진폭으로 층위 분리되어 더는 충돌 안 함.
- **파생 A 조건부성 명시 ✓**: FABLE §2 의 "어느 공식이 옳은지는 $w_j$ 가 실제 $T$-선형인지에 달림(두 오차 자리바꿈 ~0.3 mV/K)" 을 검증 전제 + warnbox 로 정직 노출. 코드 `func_w` 유일 경로도 명시.
- **물리 불변 ✓**: 식 변경 0(eq:logistic·eq:Z1·eq:weighted·종합식 모두 불변), 임계 $\Omega=2RT$ 불변, 부호·수치 불변 — **한정어만 추가**(task "H-2 한정어" 준수).
- **Ch1 정합 ✓**: Ch1 §sec:width(L740–755) 이중지위(단상=평형 예측·두-상=피팅) + broadening 절과 (A) 의 "이중지위 일치" 명시가 챕터 간 다리를 놓음.
- **스코프 준수 ✓**: FABLE 가 지적한 다른 결함(§1 eq(2.11) BW 부호·§3 파생 D 히스 근사·§4 극한표 고온 코너)은 **H-2 범위 밖**이라 본 문안에서 손대지 않음(task 는 H-2 일원화만 지시). 별건으로 기록만.

---

## 8. 신설 라벨 목록 + 충돌 검증

| 라벨 | 절 | 지위 | 충돌 검증 (v1.0.12 실측) |
|---|---|---|---|
| `eq:lco-n0sub` | center (a) | 신설 | 기존 `eq:lco-*`={dUdT,decomp} 전수 → 충돌 0 |
| `eq:lco-dUdT` | center (d) | **재사용(필수)** | 기존 L487; `\eqref` 6곳(L493·498·1229·1750·1790·1877) load-bearing |
| `eq:lco-J` | hys (a) | 신설 | 충돌 0 |
| `eq:lco-gxi` | hys (a) | 신설 | 기존 `eq:gxi`(546)와 별개, 충돌 0 |
| `eq:lco-gpp` | hys (b) | 신설 | 기존 `eq:gpp`(553)와 별개, 충돌 0 |
| `eq:lco-spinodal` | hys (b) | 신설 | 기존 `eq:spinodal`(560)와 별개, 충돌 0 |
| `eq:lco-Veq` | hys (c) | 신설 | 기존 `eq:Veq`(601)와 별개, 충돌 0 |
| `eq:lco-dUhys` | hys (d) | 신설 | 기존 `eq:dUhys`(630)와 별개, 충돌 0 |
| `eq:lco-Ubranch` | hys (d) | 신설 | 기존 `eq:Ubranch`(648)와 별개, 충돌 0 |
| `eq:lco-mit` | hys T1 | 신설 | 충돌 0 |
| `eq:lco-dope` | hys 도핑 | 신설 | 충돌 0 |
| `eq:lco-xieq` | peak (a) | 신설 | 기존 `eq:xieq`(788)와 별개, 충돌 0 |
| `eq:lco-peakslope` | peak (c) | 신설 | 충돌 0 |
| `eq:lco-eqpeak` | peak (d) | 신설 | 기존 `eq:eqpeak`(1209)와 별개, 충돌 0 |
| `eq:lco-peak3` | peak (d) | 신설 | 충돌 0 |
| `eq:lco-Zfact` | decomp (a) | 신설 | 충돌 0 |
| `eq:lco-decomp` | decomp (c) | **재사용** | 기존 L1723; 참조 다수 → 유지 |
| `eq:lco-noDC` | decomp (d) | 신설 | 충돌 0 |
| `eq:lco-xmap` | plug-in (b) | 신설 | 충돌 0 |
| `eq:lco-plugin` | plug-in (d) | 신설 | 충돌 0 |
| `eq:lco-msmrnorm` | MSMR (b) | 신설 | 충돌 0 |
| `eq:lco-msmrmap` | MSMR (c) | 신설 | 충돌 0 |
| `eq:lco-msmrpeak` | MSMR (d) | 신설 | 충돌 0 |

- **신설 = 21개**(전부 `eq:lco-*` 프리픽스), **재사용 = 2개**(`eq:lco-dUdT`·`eq:lco-decomp`). 기존 `eq:lco-*` 는 그 2개뿐이라 신설 21개 전원 충돌 0(전수 확정).
- finalizer 는 번호 흐름에 맞춰 신설 라벨명 조정 가능하나 **`eq:lco-dUdT`(6곳)·`eq:lco-decomp` 재사용은 불변**(load-bearing `\eqref`).
- H-2 신설: `eq:lco-msmrnorm` 는 ch1, H-2 warnbox/keybox 는 ch2 텍스트(라벨 신설 없음 — 기존 keybox/srcbox 교체·보강).

## 9. finalizer 편입 체크리스트
1. center: **L477–494 교체** → §1 블록. (d)박스가 `eq:lco-dUdT` 유일 정의인지 확인(중복 금지). verifybox(496–516)·다리(518–519) 인접 유지.
2. hys: **L697–719 교체** → §2 블록. L696 헤더·L722 `sec:width` 인접.
3. peak: **L1221–1232 교체** → §3 블록. L1234 `sec:broadening` 인접.
4. decomp: **L1716–1718 교체(a,b)** + `eq:lco-decomp` 박스(1719–1724) 유지(c) + 직후 `eq:lco-noDC` 삽입(d). itemize(1725–1748)·Ch2예고(1756–1765) 보존.
5. plug-in: `sec:lco-code` enumerate(1789) 뒤 §5 블록 삽입(1794 앞).
6. MSMR: `eq:msmr`(1772) 뒤 줄글(1774–1780)을 §6 (a)–(d)로 augment.
7. H-2: ch2 keybox(161–166) 교체(A) + 파생A srcbox(485–496) 전제+warnbox(B) + revheat keybox(683–685) 한 구절(C).
8. 매크로 확인: `\operatorname{artanh}`·`\code`·`\rxn`·`\eq`·`\cat`·`\dd`·`\oc`·`\hys`·`verifybox`·`keybox`·`warnbox`·`srcbox` preamble 존재(기존 문서 사용 매크로 계열).
9. 빌드 후 `eq:lco-dUdT` 참조 6곳 미해결 0, 신설 라벨 미참조 경고만(정의처는 존재) 확인. 물리·부호·수치·`Ω_j` 기호 불변, 불가침 절(map/Se/gate/electronic/verifybox) 미접촉 확인.

## 10. 5줄 요약
1. **수식화 커버**: 지시 6개 절 전부 흑연 forward (a)→(b)→(c)→(d) 사슬로 — center·hys 는 V1011 계승+독립 재유도 검증(spinodal·ΔU_hys·8RT/3F Taylor 손 재검산 일치), peak·decomp(Z-인수분해)·plug-in(좌표다리+T² M-10)·MSMR($f{=}{-}\sigma_d$) 신규. 신설 라벨 21 + 재사용 2(`eq:lco-dUdT` 6곳·`eq:lco-decomp`).
2. **H-2 일원화**: §ssec:logistic 에 "단상(Ω≤2RT) 한정" + 두-상 진폭(자유 피팅)/함수형(코드 고정) 층위 분리, 파생A 검증을 "열적-스케일 함수형 가정 조건부"로 전제 명시(코드 `func_w` 유일 경로·오차 자리바꿈 ~0.3 mV/K), Ch1 §sec:width 이중지위와 정합 — 식 변경 0, 한정어만.
3. **논리결함 발견**: Branch1 유도에서 새 물리결함 0(모든 재유도 부호·차원·극한·이중계산·detailed balance 통과). Branch2 는 FABLE §2 모순이 v1.0.12 keybox 의 "(자리당 n_j=1 기준…)" 완화로도 **미해소 잔존**(w_j 에 "임의 아님" 여전 + 파생A 전제 미명시) 확인 → 본 문안이 해소.
4. **물리 불변 확인**: 결과식·부호·수치·`Ω_j` 기호·0.47/1.49(config ΔS) 전부 불변, 신규 개념(ρ/PSD/입자반경) 0, 불가침 절 미접촉, M-10 가드(ΔS_e∝T·T² `eq:U1T2`) 유지. 전개 형식 변환 + H-2 한정어만.
5. **최약점**: plug-in 좌표다리 `eq:lco-xmap` 의 $x{=}x(\xi_{\eq,1})$↔$U_1(\Delta S_e(x))$ **암시적 자기참조** — 코드가 $T_\mathrm{ref}$ 동결 1-pass 인지 다온도 self-consistent 인지에 따라 평가가 갈리며, 본 드래프트는 원문 스코프대로 "단일-기준 근사 → 다온도 round-trip 위임"으로 두어 self-consistency 완결식을 세우지 않음(finalizer 가 코드 구현 확인 후 확정 필요). 차약점: decomp $Z$-인수분해의 MIT 교차항 "선도 차수 무시"가 정량 한계 미제시(원문 정직 서술 계승, 정량화는 범위 밖).

**출력 파일: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1012_P43_draft_O1.md`**
