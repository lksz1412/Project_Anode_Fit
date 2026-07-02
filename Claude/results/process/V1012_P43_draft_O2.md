# V1012 Phase 4.3 작성 드래프트 — ID=O2 (Opus, 독립·무통신)

> 대상: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex`(1848줄) · `graphite_ica_ch2_v1.0.12.tex`(710줄)
> 성격: 편입용 LaTeX 수식-사슬 supplement 드래프트. **`.tex`/코드 미수정**(편입은 Fable master). 허위 attribution 없음.
> 정독 근거: 두 tex 전문 정독(라벨-기반 실측 줄번호) + V1011_P11_map_v10.md(center·hys 계승 출발점) + V1010_LCO_STYLE_REPORT.md §1 + FABLE_REAUDIT_C4_note.md. 모든 수식 사슬은 **독립 재유도로 검증**하며 작성(부호·차원·극한·detailed balance·이중계산 자기검수).

---

## 0. 실측 기반 사실 (편입 위치·라벨·불가침)

### 0.1 v1.0.12 편입 위치 (라벨-기반 실측; base 근사줄과 대조)
| 절 | 헤더(보존) | 교체/삽입 범위(현행 줄글) | 인접 경계(불변) | base 근사 |
|---|---|---|---|---|
| `sec:lco-center` | L476 | **L477–494 교체**(전극무관 단정 + 대표스케일 프로즈. eq:lco-dUdT L483–488 포함) | L496–516 verifybox·L518–519 히스 다리 보존 | ≈L470 |
| `sec:lco-hys` | L696 | **L697–719 교체**(intro + T2·T3 + T1 MIT + 도핑, 4문단) | L722 `sec:width` 불변 | ≈L684 |
| `sec:lco-peak` | L1220 | **L1221–1232 교체**(전극무관 적용 + 세 봉우리 프로즈) | L1234 `sec:broadening` 불변 | ≈L1204 |
| `sec:lco-decomp` | L1715 | **L1718 뒤 (a)(b)(c) 삽입**(eq:lco-decomp L1719–1724 를 (d) 박스로 승계, 기존 itemize L1726– 보존) | L1767 `sec:lco-code` | ≈L1690 |
| `sec:lco-code`(plug-in+MSMR) | L1767 | **eq:msmr L1770–1773 주변 MSMR 사슬 + 전자항 plug-in 사슬 삽입** | L1794 입력인자 절 | ≈L1740 |

### 0.2 ★라벨 검증 (load-bearing — 실측 grep)
- v1.0.12 Ch1 의 **기존 `eq:lco-*` = {`eq:lco-dUdT`(L487), `eq:lco-decomp`(L1723)} 딱 2개**(전수 grep 확정). 따라서 그 2개 외 임의 `eq:lco-*` 신설명은 충돌 0.
- **`eq:lco-dUdT` 재사용 필수**: 정의(L487) 외 `\eqref` 참조 = **L493·L498(center verifybox)·L1229(lco-peak)·L1750·L1790(decomp·code)·L1877(nodemap N2′)** — 6곳 다운스트림. center (d) 박스가 `\label{eq:lco-dUdT}` 를 그대로 이어받아야 이 6참조가 안 깨진다.
- **`eq:lco-decomp` 재사용 필수**: 정의(L1723) 외 `\eqref` = **L505·L508(center verifybox)·L1040·L1060(전자엔트로피 절)·L1729·L1738·L1761(decomp 내부)·L1785(code)·L1879(nodemap N9′)** — 다수 다운스트림. decomp (d) 박스가 라벨 승계.
- 신설 후보 전부 개별 grep `No matches`(아래 §7 목록). 전부 `eq:lco-*` 프리픽스라 위 2개와 충돌 0.

### 0.3 불가침 확인
- 손대지 말 것(base): `sec:lco-map`(L301)·`sec:lco-Se`(L965)·`sec:lco-gate`(L1082)·N0–N9 흑연 본체·전자 엔트로피 절(L945–1181). → **미접촉. 참조·대입만.**
- 물리·결과식·부호·수치 불변, `Ω_j` 기호 유지(0.47/1.49 = **config ΔS**[J/(mol·K)], config ΔS 슬롯행이지 Ω_j[J/mol] 아님 — 수치 날조 금지). 신규 개념(ρ(U_app)/PSD/입자반경) 도입 0.
- **M-10 가드 유지**: T1 전자항 `ΔS_e∝T` → `∂U_1/∂T=ΔS_rxn^cat(T)/F` 는 유지할 관계, 위치는 `U_1(T)=U_1(T_ref)+(1/F)∫ΔS dT′`(기준온도 적분) — 기계 미분(ΔS+T∂_TΔS) 금지. Ch1 eq:U1T2(L1074) 정합.

### 0.4 v1.0.12 착지 상태 (V1011 대비 진척 — 재작업 중복 방지)
- center: eq:lco-dUdT(L487)·verifybox(L496–516)는 **이미 편입됨**. 빠진 것은 그 앞의 **(a)(b)(c) 유도 사슬**(현행 L477–478 은 "유도에 전극 가정 없다"는 프로즈 단정으로 대체). → 본 드래프트가 사슬 복원.
- hys: 현행은 **전부 프로즈**(spinodal 대입 중간식·gap 닫힌식·MIT 슬롯분리 박스 전무). → 사슬 신작.
- peak/decomp/code: 현행에 상당한 서술 有(특히 decomp itemize·code 두 변경). 그러나 **(a)→(d) forward 사슬은 미폐쇄**. → 사슬로 승격.

---

## 1. `sec:lco-center` — 평형 중심 forward 사슬 (계승·재검·개선)

**편입 지시**: **L477–494 를 아래 블록으로 교체**. L476 헤더·L496–516 verifybox·L518–519 다리 보존. (d) 박스가 `\label{eq:lco-dUdT}` 재사용(현행 L487 의 유일 정의를 이 박스로 이관 — 중복 정의 금지). 블록 말미 좌표-고정 문장이 보존 verifybox 로 자연 연결.

```latex
\textbf{(a) 출발 — 전극-중립 골격의 세 진입.} 식~\eqref{eq:Uj} 의 평형 중심 $U_j(T)$ 유도(\S\ref{sec:center})를
되짚으면 어느 다리에도 ``흑연''이라는 물질 고유 항이 없다: (i) 실험조건 매핑 식~\eqref{eq:n0map} 의 방향 부호$\cdot$
전류 환산($\sigma_d=\pm1,\ |I|=\code{c\_rate}\,Q_\cell$)은 삽입형 전극이면 종류 불문이고, (ii) 전기화학 평형 조건
식~\eqref{eq:eqcond}($\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U),\ \Delta G_j=-sFU_j$)는 삽입 반쪽반응
$\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 의 전기화학 평형(식~\eqref{eq:eqbalance})에서
나오며 host 의 화학 정체는 상수 $\mu^0$ 로만 흡수되고, (iii) 비배치 몫 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$
은 반응종에 무관한 열역학 항등식이다. LCO 로 넘어갈 때 이 세 자리에 들어가는 것은 전이 집합과 입력값의 치환뿐이다:
\begin{equation}
j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j})\ \longmapsto\ (\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat}).
\label{eq:lco-n0sub}
\end{equation}
곧 $\sigma_d$ 는 방향 선택 슬롯에 남고, 평형 중심의 Gibbs 환산식에는 새 양극 부호가 끼지 않는다.

\textbf{(b) 연산 — 평형 조건에 반응 자유에너지 대입.} 전이 $j$ 의 비배치 반응 자유에너지 $\Delta G_j^\mathrm{cat}
=\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}$ 를 식~\eqref{eq:eqcond} 의 $\Delta G_j=-sFU_j$
($s=+1$)에 넣으면
\[
\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}=-F\,U_j^\mathrm{cat}(T),
\]
곧 흑연 식~\eqref{eq:Ujmid} 과 글자 그대로 같은 식에 상첨자 $\mathrm{cat}$ 만 붙는다(host 가 유도 단계에 없었다는
(a)의 대입 확인).

\textbf{(c) 중간식 — 중심과 온도 계수(이중 경로 교차검증).} (b)를 $U_j^\mathrm{cat}$ 로 이항하면
$U_j^\mathrm{cat}(T)=(-\Delta H_{\rxn,j}^\mathrm{cat}+T\Delta S_{\rxn,j}^\mathrm{cat})/F$ 로 흑연 식~\eqref{eq:Uj} 와
같은 함수형이다. 온도 계수는 두 독립 경로가 같은 값에 닿는다. \emph{경로 1(직접 미분)}: $\Delta H^\mathrm{cat}$ 는
$T$ 무관, $\partial(T\Delta S^\mathrm{cat})/\partial T=\Delta S^\mathrm{cat}$ 이라
$\partial U_j^\mathrm{cat}/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$. \emph{경로 2(Gibbs 항등식 경유)}: 등압 Gibbs
항등식 $\partial\Delta G_j/\partial T|_P=-\Delta S_{\rxn,j}^\mathrm{cat}$(식~\eqref{eq:gibbsdef} $G\equiv H-TS$ 에서)와
식~\eqref{eq:eqcond} 의 $\Delta G_j=-FU_j$ 를 미분한 $\partial\Delta G_j/\partial T=-F\,\partial U_j^\mathrm{cat}/\partial T$
를 등치하면
\[
-F\,\frac{\partial U_j^\mathrm{cat}}{\partial T}=-\Delta S_{\rxn,j}^\mathrm{cat}
\ \Longrightarrow\ \frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
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
관계식은 흑연 식~\eqref{eq:Uj} 와 부호까지 1:1 이고 바뀌는 것은 값뿐이다 — 양극의 높은 중심($\sim$3.9--4.2 V)은
분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양인 데서 오고, $\Delta S_{\rxn,j}^\mathrm{cat}$ 는
\S\ref{sec:lco-decomp}(식~\eqref{eq:lco-decomp})에서 config$\cdot$vib$\cdot$전자 세 성분으로 분해된다.
\textbf{★다온도 전자항 주의(T1).} $\Delta S_{e,j}(x,T)\propto T$ 인 항을 다온도 모델에 실제로 풀 때는, 고정
$\Delta H$ 로 $U_j(T)=(-\Delta H+T\Delta S(T))/F$ 를 기계 미분하면 $\Delta S+T\,\partial_T\Delta S$ 가 생기므로,
열역학적으로 유지할 관계는 위 박스의 $\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}(T)/F$ 이고 위치는
기준온도에서
\[
U_j^\mathrm{cat}(T)=U_j^\mathrm{cat}(T_\mathrm{ref})+\frac1F\int_{T_\mathrm{ref}}^{T}\Delta S_{\rxn,j}^\mathrm{cat}(T')\,\dd T'
\]
로 해석해야 한다(T1 의 $\propto T^2$ 누적은 식~\eqref{eq:U1T2}). \textbf{(부호 좌표 고정.)} 아래 검산의
$\Delta S_{\rxn,j}^\mathrm{cat}$ 는 반쪽반응을 \emph{삽입 방향}(Li$^+$ 가 host 로 들어옴)으로 적은 반응 엔트로피이며
(표~\ref{tab:staging} 흑연 삽입 규약과 동일 좌표), 단전극 potentiometric $\dd\phi/\dd T$ 의 부호는 측정 규약
의존이므로 아래 verifybox 는 그 대표 스케일을 삽입-반응 $\Delta S_{\rxn}^\mathrm{cat}$ 로 환산해 크기$\cdot$부호
sanity 만 확인한다.
```

**원 줄글 대비**: 현행 L477–482(전극무관 단정 프로즈) + L483–488(eq:lco-dUdT 단독) + L489–494(분해 예고·대표스케일 프로즈) → (a) 세 진입 명시 유도 + (b) eq:eqcond 앵커 대입 + (c) **이중경로**(직접미분 ∥ Gibbs 항등식) + (d) 박스(U_j^cat 과 ∂U/∂T 동시, eq:lco-dUdT 승계) + M-10 가드 + 좌표고정. **결과식·부호·수치(+0.83 mV/K·+80 J/(mol·K)) 불변** — verifybox 가 그대로 받는다.

**논리 감사(재유도)**:
- **부호/차원**: `∂U/∂T=ΔS/F`, [J/(mol·K)]/[C/mol]=[V/K] ✓. 큰 음 ΔH_rxn^cat → 분자 −ΔH>0 → 높은 중심 ✓.
- **이중경로 교차검증**: 경로1 직접미분 = ΔS^cat/F. 경로2 Gibbs: ∂ΔG/∂T=−ΔS 와 ΔG=−FU 미분 −F∂U/∂T 등치 → ∂U/∂T=ΔS/F. **두 경로 host 항 0, 동일값** ✓.
- **M-10(다온도)**: ΔS_e∝T 시 기계미분 오류(ΔS+T∂_TΔS) 회피, ∫ΔS dT′ 적분해석 유지 ✓ (eq:U1T2 정합).
- **불가침**: verifybox·eq:lco-dUdT 6참조·전자엔트로피 절 미접촉 ✓.

---

## 2. `sec:lco-hys` — 히스 분기 forward 사슬 (계승·재검·개선)

**편입 지시**: **L697–719 를 아래 블록으로 교체**. L696 헤더 보존, L722 `sec:width` 불변. 흑연 `sec:hys` 결과식(`eq:mu`·`eq:gxi`·`eq:gpp`·`eq:spinodal`·`eq:Veq`·`eq:hyssub`·`eq:hysdiff`·`eq:dUhys`·`eq:hyssym`·`eq:Ubranch`)은 재유도 없이 **참조·대입만**.

```latex
\S\ref{sec:hys} 의 격자기체$\cdot$정규용액 틀은 ``동등한 자리에 리튬이 차고 빈다''는 가정만 쓰므로, 그 가정이 서는
LCO 양극(팔면체 Li 자리, 자리당 점유 0/1)에도 그대로 성립한다 — 새 물리 없이 전이별 입력값
$U_j^\mathrm{cat},\Omega_j^\mathrm{cat},\gamma_j,h_{\eta,j}$ 만 갈아 끼운다.

\textbf{(a) 출발 — LCO 세 전이를 같은 정규용액 자유에너지에.} LCO 전이 집합
\begin{equation}
\mathcal J_\mathrm{LCO}=\{1:\mathrm{MIT},\ 2:\mathrm{OD}_a,\ 3:\mathrm{OD}_b\}
\label{eq:lco-J}
\end{equation}
의 각 전이 $j$ 에 진행률 $\xi_j$ 를 달아 흑연 식~\eqref{eq:gxi} 와 같은 정규용액 몫을 쓴다:
\begin{equation}
g_j^\mathrm{cat}(\xi_j)=g_{0,j}^\mathrm{cat}+RT\{\xi_j\ln\xi_j+(1-\xi_j)\ln(1-\xi_j)\}+\Omega_j^\mathrm{cat}\,\xi_j(1-\xi_j).
\label{eq:lco-gxi}
\end{equation}

\textbf{(b) 연산 — 곡률과 spinodal 문턱.} 식~\eqref{eq:lco-gxi} 를 두 번 미분하면 흑연 식~\eqref{eq:gpp} 에 전이별
$\Omega_j^\mathrm{cat}$ 만 든다:
\begin{equation}
\frac{\partial^2 g_j^\mathrm{cat}}{\partial\xi_j^2}=\frac{RT}{\xi_j(1-\xi_j)}-2\Omega_j^\mathrm{cat},
\qquad
\xi_{s,j}^{\pm}=\tfrac12\big(1\pm u_j^\mathrm{cat}\big),\ \
u_j^\mathrm{cat}=\sqrt{1-\frac{2RT}{\Omega_j^\mathrm{cat}}}\ \ (\Omega_j^\mathrm{cat}>2RT),
\label{eq:lco-spinodal}
\end{equation}
이고 $\Omega_j^\mathrm{cat}\le2RT$ 이면 $u_j^\mathrm{cat}$ 이 실수가 아니라 그 전이의 spinodal gap 은 없다(흑연
식~\eqref{eq:spinodal} 코드 분기 그대로).

\textbf{(c) 중간식 — 전위 곡선에 spinodal 대입.} LCO 전이 $j$ 의 평형 전위 곡선은 식~\eqref{eq:Veq} 에
$U_j^\mathrm{cat},\Omega_j^\mathrm{cat}$ 를 넣어
\begin{equation}
V_{\eq,j}^\mathrm{cat}(\xi)=U_j^\mathrm{cat}+\frac{RT}{F}\ln\frac{\xi}{1-\xi}+\frac{\Omega_j^\mathrm{cat}}{F}(1-2\xi),
\label{eq:lco-Veq}
\end{equation}
이고 두 spinodal 끝점에서(흑연 식~\eqref{eq:hyssub}) $\dfrac{\xi}{1-\xi}\big|_{\xi_{s,j}^\pm}=\dfrac{1\pm
u_j^\mathrm{cat}}{1\mp u_j^\mathrm{cat}}$, $(1-2\xi)\big|_{\xi_{s,j}^\pm}=\mp u_j^\mathrm{cat}$ 이므로 극대$-$극소 차는
(흑연 식~\eqref{eq:hysdiff} 대입, 상수 중심 $U_j^\mathrm{cat}$ 상쇄)
\[
\Delta U_j^{\hys,\mathrm{cat}}=V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^-)-V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^+)
=\frac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\operatorname{artanh}u_j^\mathrm{cat}\big].
\]

\textbf{(d) 박스 — LCO 전이별 gap 과 분기 중심.}
\begin{equation}
\boxed{\;
\Delta U_j^{\hys,\mathrm{cat}}(T)=
\begin{cases}
\dfrac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\operatorname{artanh}u_j^\mathrm{cat}\big], & \Omega_j^\mathrm{cat}>2RT,\\[4pt]
0, & \Omega_j^\mathrm{cat}\le2RT,
\end{cases}
\quad u_j^\mathrm{cat}=\sqrt{1-\dfrac{2RT}{\Omega_j^\mathrm{cat}}}\;}
\label{eq:lco-dUhys}
\end{equation}
\begin{equation}
\boxed{\;U_j^{\,d,\mathrm{cat}}=U_j^\mathrm{cat}+\tfrac12\sigma_d h_{\eta,j}\gamma_j\,\Delta U_j^{\hys,\mathrm{cat}}(T)\;}
\label{eq:lco-Ubranch}
\end{equation}
흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 대입형이다 — ``같은 틀''은 식 생략이 아니라
$\Omega_j\!\mapsto\!\Omega_j^\mathrm{cat}$, $U_j\!\mapsto\!U_j^\mathrm{cat}$, $j\!\in\!\mathcal J_\mathrm{LCO}$ 를
실제로 넣는다는 뜻이다. 방전($\sigma_d{=}{+}1$)은 분기 중심을 위로, 충전($\sigma_d{=}{-}1$)은 아래로 옮긴다.

\textbf{(T2$\cdot$T3) order--disorder.} $x\approx0.5$ 부근 monoclinic 초격자(점유 Li 와 빈자리의 교대 정렬)를 이루는
T2($\sim$4.05 V, hex$\to$monoclinic)$\cdot$T3($\sim$4.17--4.20 V, monoclinic$\to$hex)는 동종 이웃 인력
$\Omega_j^\mathrm{cat}>0$ 이 만드는 상분리의 LCO 사례다 — 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에
$j=2,3$ 을 넣어 두 좁은 peak 로 열린다. \textbf{★$\Omega$ 와 config $\Delta S$ 의 구분(혼동 가드).} 정렬의
charge-order 엔트로피 변화($\approx0.47$ J/(mol\,K)@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$
[tier A, Motohashi\cite{motohashi2009}])는 \emph{엔트로피} 값이라 표~\ref{tab:lco-staging}$\cdot$
식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 슬롯(따라서 $U_j^\mathrm{cat}(T)$ 의 온도 이동)에 들어가지,
spinodal 문턱을 정하는 \emph{상호작용 에너지} $\Omega_j^\mathrm{cat}$[J/mol]가 \emph{아니다} — 둘은 서로 다른 양이라
``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 다리를 놓아선 안 되고 $\Omega_j^\mathrm{cat}$ 는 gap 을 정하는 별도 피팅
파라미터로 둔다.

\textbf{(T1) MIT 2상역 — 두 몫의 슬롯 분리.} T1($\sim$3.90 V, $x\approx0.94$--$0.75$, 절연체$\to$금속)의 구조적 2상
공존도 같은 정규용액 문턱을 받아 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j{=}1$ 로 열린다. MIT 고유의
전자 자유도는 이 히스 gap 에 새 항으로 섞지 않는다 — 그 항은 이미 $\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^\mathrm{config}
+\Delta S_1^\mathrm{vib}+\Delta S_{e,1}^{\,\mathrm{mol}}(x,T)$(식~\eqref{eq:lco-decomp})를 통해 $U_1^\mathrm{cat}(T)$ 의
온도 이동(식~\eqref{eq:lco-dUdT})에 들어간다. 곧 두 몫이 서로 다른 슬롯에 산다:
\begin{equation}
\boxed{\;
\underbrace{\Delta U_1^{\hys,\mathrm{cat}}\ \Leftarrow\ \Omega_1^\mathrm{cat}}_{\text{정규용액 히스 gap (이 절)}}
\quad\Big\|\quad
\underbrace{\partial U_1^\mathrm{cat}/\partial T\ \Leftarrow\ \Delta S_{e,1}^{\,\mathrm{mol}}(x,T)}_{\text{전자 엔트로피 (\S\ref{sec:lco-electronic})}}\;}
\label{eq:lco-mit}
\end{equation}
이 분리가 구조 2상역과 전자 엔트로피의 이중계산을 막는 경계다.

\textbf{두-상 문턱의 지위(피팅 판정).} pure-LCO 초기값(표~\ref{tab:lco-staging})에서는 T1$\cdot$T2$\cdot$T3 세 전이가
모두 $\Omega_j^\mathrm{cat}>2RT$ 후보이나, 흑연 staging 이 ``4 중 초기값 전부 두-상 $\to$ 피팅 후 두 전이만 잔존''
(\S\ref{sec:width}$\cdot$\S\ref{sec:broadening})이었듯 각 전이의 실제 gap 유무는 최종적으로 \emph{피팅된}
$\Omega_j^\mathrm{cat}$ 이 $2RT(\approx4958$ J/mol@298 K$)$ 를 넘는지가 정한다 — 문턱 판정 식
$\Omega_j^\mathrm{cat}>2RT$ 자체는 두 전극에서 동일하다.

\textbf{도핑 보정(우리 시료).} Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox$\cdot$전자항을 보존하되
order--disorder$\cdot$MIT 상전이를 억제한다 — 정규용액 틀에서 이는 pure-LCO $\Omega_j^\mathrm{cat,pure}$ 를 도핑
피팅값으로 낮추는 입력 변화다. 식~\eqref{eq:lco-dUhys} 의 문턱 극한은(흑연 식~\eqref{eq:dUhys} 아래 Taylor
$\operatorname{artanh}u=u+u^3/3+\cdots$, $T_{c,j}=\Omega_j^\mathrm{cat}/2R$ 재사용)
\begin{equation}
\Omega_j^\mathrm{cat,dop}\to2RT^+\ \Longrightarrow\ u_j^\mathrm{cat}\to0,\quad
\Delta U_j^{\hys,\mathrm{cat}}\to\frac{8RT}{3F}\big(u_j^\mathrm{cat}\big)^3\to0,
\label{eq:lco-dope}
\end{equation}
이고 $\Omega_j^\mathrm{cat}\le2RT$ 로 피팅되는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다 — 상전이 억제에 따른
히스 축소와 peak smear 의 수식 표현이며, 풀린 몫은 \S\ref{sec:broadening} 의 broadening 폭이 담는다.
\textbf{★슬롯 분리.} 중심 전위의 미세 shift 는 같은 전이 dict 의 $U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로}
들어가며, $\Omega_j^\mathrm{cat}$ 하나가 gap$\cdot$smear 와 중심 이동을 동시에 만든다고 쓰지 않는다.
```

**원 줄글 대비**: 현행 L697–699(intro) + L701–706(T2·T3 프로즈) + L708–713(T1 MIT 프로즈, 슬롯분리 언급만) + L715–719(도핑 프로즈) → (a) `eq:lco-J`→`g_j^cat` + (b) `g″`→spinodal + (c) `V_eq` 끝점 대입 중간식 + (d) `ΔU_hys`·`U^d` 박스 + T2/T3 혼동가드 + **T1 MIT 슬롯분리 박스(eq:lco-mit)** + 두-상 피팅판정 + 도핑 Ω→2RT⁺ Taylor 극한 박스. **현행 "세 전이 모두 대응"(L698–699)은 "pure 초기값 후보 + 피팅 판정"으로 정밀화**(도핑 시 Ω≤2RT gap 0 케이스와 정합; 현행 L715–719 도핑 서술과 모순 없음).

**논리 감사(재유도)**:
- **g″ 재유도**: RT[ξlnξ+(1−ξ)ln(1−ξ)]″=RT/[ξ(1−ξ)]; [Ωξ(1−ξ)]″=−2Ω ✓. spinodal ξ²−ξ+RT/2Ω=0 근의공식 → ½(1±u) ✓.
- **끝점 대입 재유도**: ξ_s^±=½(1±u) → 1−2ξ_s^±=∓u ✓; ξ_s^±/(1−ξ_s^±)=(1±u)/(1∓u) ✓.
- **ΔU_hys 재유도(손계산)**: V(ξ_s^−)=U+(RT/F)(−2artanh u)+(Ω/F)(+u); V(ξ_s^+)=U+(RT/F)(+2artanh u)+(Ω/F)(−u); 차=(RT/F)(−4artanh u)+(Ω/F)(2u)=**(2/F)[Ωu−2RT artanh u]** — 흑연 eq:dUhys(L628)와 정확 일치 ✓. 상수 U 상쇄 ✓.
- **Taylor 극한 재유도**: Ω−2RT=Ωu²(u²=1−2RT/Ω에서), (Ω−2RT)u−(2RT/3)u³=Ωu³−(2RT/3)u³→Ω≈2RT 근방 (2RT−2RT/3)u³=(4RT/3)u³; ΔU_hys=(2/F)(4RT/3)u³=**(8RT/3F)u³→0** ✓ (흑연 L634 일치).
- **이중계산(MIT)**: Ω_1→히스 gap 슬롯, ΔS_e,1→∂U/∂T 슬롯 — **직교 분리** ✓ (원 L710–713 "두 몫 분리" 를 박스로 못박음).
- **혼동가드**: 0.47/1.49 = config ΔS[J/(mol·K)] 슬롯, Ω_j[J/mol] 아님 — 수치 날조 0, `Ω_j` 기호 유지 ✓.
- **불가침**: 흑연 sec:hys 8식 재유도 없이 참조·대입만 ✓.

---

## 3. `sec:lco-peak` — 세 봉우리 forward 사슬 (★최약 절, 신작)

**편입 지시**: **L1221–1232 를 아래 블록으로 교체**. L1220 헤더 보존, L1234 `sec:broadening` 불변. 흑연 `eq:eqpeak`(L1209)·`eq:belliden`(L1198)은 참조·대입만.

```latex
평형 peak 식~\eqref{eq:eqpeak}($Q_j\,\xi_\eq(1-\xi_\eq)/w_j$)는 전극을 가리지 않으므로 LCO 양극에 그대로 적용된다.
LCO 하프셀은 흑연의 네 봉우리 대신 \emph{양극 전위 영역}에 세 봉우리를 남긴다.

\textbf{(a) 출발 — 세 전이 평형 점유.} 각 전이 $j\in\mathcal J_\mathrm{LCO}$ 의 평형 점유는 흑연 식~\eqref{eq:xieq} 에
LCO 분기 중심 $U_j^{\,d,\mathrm{cat}}$(식~\eqref{eq:lco-Ubranch})와 폭 $w_j$ 를 넣은
$\xi_{\eq,j}(V,T)=\{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]\}^{-1}$ 다.

\textbf{(b) 연산 — 종 항등식과 연쇄율.} $z_j\equiv\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j$ 로 흑연 종 항등식
$\dd\xi_{\eq,j}/\dd z_j=\xi_{\eq,j}(1-\xi_{\eq,j})$(식~\eqref{eq:belliden})에 연쇄율 $\dd z_j/\dd V=\sigma_d/w_j$ 를
곱하면 $\dd\xi_{\eq,j}/\dd V=\sigma_d\,\xi_{\eq,j}(1-\xi_{\eq,j})/w_j$.

\textbf{(c) 중간식 — 보존식 미분에 대입.} 전하 보존 $Q_\cell q=Q_\bg+\sum_{j}Q_j\xi_j$ 를 $V$ 로 미분하면 전이별
평형 peak 이 나오고(식~\eqref{eq:eqpeak}), 세 전이 합으로

\[
\Big(\frac{\dd Q}{\dd V}\Big)^\eq_\mathrm{LCO}
=C_\bg+\sum_{j\in\{\mathrm{T1,T2,T3}\}}Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}.
\]

\textbf{(d) 박스 — LCO 세 봉우리와 세 양.}
\begin{equation}
\boxed{\;
\Big(\frac{\dd Q}{\dd V}\Big)^\eq_\mathrm{LCO}
=C_\bg+\sum_{j\in\mathcal J_\mathrm{LCO}}Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j},
\quad
\begin{cases}
\text{위치}=U_j^{\,d,\mathrm{cat}},\\
\text{순높이}=Q_j/(4w_j),\\
\text{면적}=Q_j,
\end{cases}\;}
\label{eq:lco-peak}
\end{equation}
세 봉우리는 T1 $\sim$3.90 V(MIT plateau)$\cdot$T2 $\sim$4.05 V$\cdot$T3 $\sim$4.17--4.20 V(T2 와 한 쌍의 좁은
order--disorder)다. 폭은 흑연과 같은 $w_j=n_jRT/F$ 이고, LCO 세 전이는 pure 초기값에서 모두 $\Omega_j^\mathrm{cat}>2RT$
후보라 그 폭은 \S\ref{sec:width} 이중지위의 \emph{두-상} 측 — 평형 예측이 아니라 broadening 이 정하는 현상학적
피팅 폭이다(\S\ref{sec:broadening}). order--disorder 의 큰 $\Omega$ 가 spinodal gap 을 키워 T2$\cdot$T3 분기를
흑연보다 날카롭게 만든다.

\textbf{★T1 봉우리의 전자항 온도 신호.} T1 위치는 \S\ref{sec:lco-electronic} 의 전자항이 $\Delta S_{\rxn,1}^\mathrm{cat}$
를 통해 $U_1^\mathrm{cat}(T)$ 의 \emph{온도 이동}에 기여하므로(식~\eqref{eq:lco-dUdT}), 다온도 dQ/dV 에서 식별 신호는
\emph{위치 자체가 $T$-선형}이 아니라 \emph{이동률} $\partial U_1/\partial T$ 가 $T$ 에 선형으로 커지는 것이다
($\Delta S_{e,1}\propto T$, \S\ref{sec:lco-Se}) — 곧 위치 이동은 $\propto T^2$(식~\eqref{eq:U1T2}). 도핑은
\S\ref{sec:lco-hys} 대로 봉우리를 smear$\cdot$shift 시킨다.
```

**원 줄글 대비**: 현행 L1221–1232(전극무관 적용 서술 + 세 위치 프로즈 열거 + 두-상 폭 지위 + T1 온도이동 + 도핑) → (a) `ξ_eq,j` + (b) 종 항등식·연쇄율 + (c) 보존식 미분 합 + (d) **세 봉우리 합산 박스(eq:lco-peak) + 위치/순높이/면적 세 양**. V1010 스타일리포트 §1 이 지정한 "ξ_eq,j→dξ/dV→ΣQ_j peak_shape→center/height/area box (j∈{T1,T2,T3})" 완결.

**논리 감사(재유도)**:
- **종 항등식**: dξ/dz=e^{−z}/(1+e^{−z})²=ξ(1−ξ) ✓ (흑연 eq:belliden). 연쇄율 dz/dV=σ_d/w_j ✓.
- **세 양 재유도**: 순높이 ξ=½ 에서 ξ(1−ξ)=¼ → Q_j/(4w_j) ✓; 면적 ∫₀¹dξ=1 → Q_j ✓; 위치 z=0 → V=U_j^{d,cat} ✓.
- **차원**: Q_j[C]/w_j[V]=[C/V]=dQ/dV ✓. σ_d 는 |dξ/dV| 절댓값으로 흡수, peak 양수·방향 불변 ✓.
- **T1 신호(M-10)**: ∂U_1/∂T ∝ T(선형), 위치이동 ∝ T²(비선형) — 식별신호 = 이동률의 T-선형(위치 T-선형 아님) ✓ (eq:U1T2·eq:lco-dUdT 정합, 새 항 도입 0).
- **불가침**: eq:eqpeak·eq:belliden 재유도 없이 참조 ✓; broadening 절(L1234–)·전자엔트로피 절 미접촉 ✓.

---

## 4. `sec:lco-decomp` — 분배함수 인수분해 forward 사슬 (신작; (d)=eq:lco-decomp 승계)

**편입 지시**: **L1718 뒤(현행 eq:lco-decomp 박스 L1719–1724 앞)에 아래 (a)(b)(c) 삽입**. eq:lco-decomp 박스를 (d) 로 승계(라벨·내용 불변). 기존 itemize(L1726–1749, config/vib/electronic 슬롯 역할 + 이중계산 금지 + 가법성 정당화)·요약(L1750–1754)·Ch2/P4 예고(L1756–1765)는 **그대로 보존**(본 사슬이 그 앞에 유도 골격을 깔 뿐).

```latex
\textbf{(a) 출발 — 세 자유도의 엔트로피 합.} 삽입 반응의 전체 엔트로피 변화는 세 자유도의 합이다 — 리튬 자리 점유
\emph{배열}(config), 격자 \emph{진동}(vib), 전도 전자 \emph{준위 점유}(electronic). 흑연은 셋째가 0 이라 두 몫으로
닫혔고(표~\ref{tab:staging}), LCO 는 T1 의 MIT 에서 셋째가 켜진다(\S\ref{sec:lco-electronic}).

\textbf{(b) 연산 — 분배함수 인수분해로 가법성.} config(리튬 자리 배열)와 electronic(밴드 점유)은 서로 다른 자유도라,
두 부분계가 독립인 극한에서 전체 분배함수가 인수분해된다:
\begin{equation}
Z=Z_\mathrm{config}\cdot Z_\mathrm{vib}\cdot Z_\mathrm{elec}
\ \Longrightarrow\
S=k_B\ln Z=S_\mathrm{config}+S_\mathrm{vib}+S_\mathrm{elec}
\label{eq:lco-Zfac}
\end{equation}
($\ln$ 이 곱을 합으로 풀어 교차항(잔차)이 선도 차수에서 0). MIT 부근에서 리튬 정렬과 밴드 채움이 다소 결합하나 그 교차
몫은 선도 차수에서 무시되며, 그 차수에서 분해의 가산성이 성립한다.

\textbf{(c) 중간식 — 삽입 미분으로 반응 엔트로피.} 각 몫을 삽입 방향($x\!\uparrow$)으로 미분해 전이당(삽입당) 반응
엔트로피로 옮기면 $\Delta S_{\rxn,j}^\mathrm{cat}=\partial S/\partial x|_{T}=\Delta S_j^\mathrm{config}
+\Delta S_j^\mathrm{vib}+\Delta S_{e,j}^{\,\mathrm{mol}}(x,T)$ 이고, 셋째 몫은 \S\ref{sec:lco-electronic} 의 몰당
게이트형(식~\eqref{eq:dSemolar}$\cdot$\eqref{eq:dSegate})이 그대로 들어간다.

\textbf{(d) 박스 — config + vib + electronic 분해.}
```
*(→ 현행 eq:lco-decomp 박스 L1719–1724 가 이 (d) 자리에 그대로 온다. 라벨 `eq:lco-decomp` 승계, 내용·부호·`∝T` 주석 불변. 이어 기존 itemize 가 슬롯 역할·이중계산 금지(B)·가법성 vs 무이중계산 구분을 상술.)*

```latex
% (d) 박스 뒤, 기존 itemize 로 자연 연결. 이중계산 금지의 수식 핵을 한 줄로 못박아 두면:
\emph{★이중계산 금지(수식 핵).} config 슬롯에는 봉우리 \emph{중심 표준값} $\Delta S_j^0$ 만 넣는다 — 봉우리 내부
조성 의존 $R\ln[(1-\xi_j)/\xi_j]/F$ 는 이미 Ch1 logistic(격자기체 점유 분포, \S\ref{sec:dist})이 담고 있어
$\Delta S_j^0$ 에 또 더하면 두 번 센다(Ch2 파생 B 와 동치). 곧 (가) \emph{가산성}은 식~\eqref{eq:lco-Zfac} 의 (근사)
직교성이, (나) \emph{무이중계산}은 이 중심값-전용 규칙이 각각 보장한다.
```

**원 줄글 대비**: 현행 decomp 는 eq:lco-decomp 박스(L1719–1724) + itemize(가법성 정당화 L1732–1741 이 이미 `Z=Z_config·Z_elec` 인수분해를 프로즈로 서술) → (a) 세 자유도 합 + (b) **분배함수 인수분해 → S 가산(eq:lco-Zfac)** + (c) 삽입 미분 → 반응 엔트로피 + (d) 기존 eq:lco-decomp 박스 승계. 스타일리포트 §1 지정 "Z=Z_config·Z_elec→슬롯 정의→이중계산 금지식 박스" 완결. **박스·부호·수치 불변, 신규 개념 0**(인수분해는 기존 프로즈의 수식화).

**논리 감사(재유도)**:
- **인수분해 재유도**: 독립 부분계 Z=∏Z_k → S=k_B ln Z=Σk_B ln Z_k=ΣS_k ✓ (교차항 선도차수 0). 현행 L1734 "Z=Z_config·Z_elec 로 인수분해되어 S=S_config+S_elec" 와 정확 일치.
- **삽입 미분 부호**: ∂S/∂x|_T, 전자항 삽입기준 <0(∂g/∂x<0, MIT 에서 삽입 시 금속→절연체 g 감소) — eq:dSe(L1027)·eq:dSegate(L1104) 부호와 일관 ✓.
- **이중계산 금지(B)**: config 중심값 ΔS_j^0 만, 내부 R ln[(1−ξ)/ξ] 은 logistic 이 자동 — Ch2 파생 B(eq:single_config L529)·Ch1 현행 L1729–1731 과 동치 ✓.
- **가법성 vs 무이중계산 분리**: 직교성=더해도 되는가, 금지규칙=과대계상 없는가 — 현행 L1738–1741 정합 ✓.
- **차원**: 몰당 ΔS_e^mol=N_A ∂S_e/∂x[J/(mol·K)] (eq:dSemolar) — 자리당 아님 ✓.
- **불가침**: 전자엔트로피 절(eq:dSe·dSemolar·dSegate) 재유도 없이 참조 ✓.

---

## 5. `sec:lco-code` — 전자항 plug-in + MSMR 동형 forward 사슬 (신작)

### 5A. MSMR 동형 → peak 사슬
**편입 지시**: **eq:msmr(L1770–1773) 주변**을 (a)→(d) 사슬로. 현행 동형 대응 서술(L1774–1780, `f=−σ_d` 도출)은 (c) 로 흡수·보존.

```latex
\textbf{(a) 출발 — MSMR 종별 logistic.} multiphase species reaction(MSMR)\cite{msmr2024}은 양극 전위를 전이별
logistic 합으로 적는다: $x_j=X_j/\{1+\exp[f(U-U_j^0)/\omega_j]\}$(식~\eqref{eq:msmr}).

\textbf{(b) 연산 — 용량 정규화.} 양변을 $X_j$ 로 나누면 종별 점유 분율 $x_j/X_j=\{1+\exp[f(U-U_j^0)/\omega_j]\}^{-1}$
로 순수 logistic 이 된다.

\textbf{(c) 중간식 — 대응 대입 $f=-\sigma_d$.} 용량 가중 $X_j\!\leftrightarrow\!Q_j$, 중심 $U_j^0\!\leftrightarrow\!U_j^{\,d,\mathrm{cat}}$,
폭 $\omega_j\!\leftrightarrow\!w_j$, 방향 인자 $f\!\leftrightarrow\!-\sigma_d$ 를 1:1 대입한다. MSMR 지수는 $+f(U-U_j^0)$,
Ch1 식~\eqref{eq:xieq} 지수는 $-\sigma_d(V-U_j^{\,d})$ 로 같은 자리를 채우므로 부호 비교에서 $f=-\sigma_d$ 가
강제되고, 이로써 탈리튬화/리튬화 진행 방향이 두 모델에서 일관된다.

\textbf{(d) 박스 — MSMR 종 = Ch1 평형 점유, 곧 같은 peak.}
\begin{equation}
\boxed{\;\frac{x_j}{X_j}\Big|_{f=-\sigma_d}=\frac{1}{1+\exp[-\sigma_d(U-U_j^{\,d,\mathrm{cat}})/w_j]}=\xi_{\eq,j}(U,T)
\ \Longrightarrow\ \Big(\frac{\dd Q}{\dd V}\Big)^\eq_j=Q_j\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}\;}
\label{eq:lco-msmr}
\end{equation}
곧 MSMR 종은 Ch1 의 전이별 평형 점유와 \emph{동형}이라, 곡선 클래스(\code{func\_ksi\_eq}$\cdot$\code{func\_U\_j}$\cdot$
합산~\eqref{eq:sum})가 \emph{구조 변경 0} 으로 LCO 에 적용된다.
```

### 5B. 전자항 plug-in 사슬 (좌표 매핑 → dQ/dV)
**편입 지시**: 두 변경 중 (ii) 전자 엔트로피 plug-in(현행 L1784–1788)을 아래 (a)→(d) 사슬로. 현행 좌표매핑 예고(decomp L1756–1760 의 $x\!\leftrightarrow\!\xi_{\eq,1}$)와 정합.

```latex
\textbf{(a) 출발 — 좌표 매핑 $x=x(\xi_{\eq,1}(V))$.} 전자항 $\Delta S_{e,1}$ 은 \emph{조성} $x$ 의 함수인데
(게이트 인자 $z=(x-x_\mathrm{MIT})/\Delta x_\mathrm{MIT}$), 코드 \code{dqdv} 는 \emph{전압} 격자 위에서 돈다. T1
진행률 $\xi_{\eq,1}(V)$ 이 그 전이 구간의 정규화 조성에 대응하므로 게이트 인자에 $x=x(\xi_{\eq,1}(V))$ 를 대입해
$V$ 격자 위에서 $\Delta S_e$ 를 평가한다.

\textbf{(b) 연산 — 몰당 전자항 평가.} 게이트 닫힌식(식~\eqref{eq:dSegate})에 몰당 환산(식~\eqref{eq:dSemolar},
$\Delta S_{e,1}^{\,\mathrm{mol}}=N_A\,\partial S_e/\partial x$; eV$\to$J 는 식~\eqref{eq:gunit} 나눗셈형)을 적용해
$\Delta S_{e,1}^{\,\mathrm{mol}}(V,T)<0$ 을 얻는다($N_A$ 누락 시 $\sim10^{23}$ 배 과소 — 단위 주의).

\textbf{(c) 중간식 — 반응 엔트로피와 온도 이동.} 이를 식~\eqref{eq:lco-decomp} 의 T1 슬롯에 더하면
$\Delta S_{\rxn,1}^\mathrm{cat}(V,T)=\Delta S_0+a_e T$($\Delta S_0=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}$
는 $T$ 무관, $a_e<0$ 는 전자 기울기)이고, 식~\eqref{eq:lco-dUdT} 로 온도 이동을 정해 기준온도 적분(식~\eqref{eq:U1T2})
\[
U_1^\mathrm{cat}(T)=U_1^\mathrm{cat}(T_0)+\frac{\Delta S_0}{F}(T-T_0)+\frac{a_e}{2F}(T^2-T_0^2)
\]
로 T1 중심을 옮긴다($\tfrac12$ 인자 = $\int a_eT'\dd T'$; 기계 곱 금지).

\textbf{(d) 박스 — 한 줄 plug-in 이 dQ/dV 에 남기는 것.}
\begin{equation}
\boxed{\;\Delta S_{\rxn,1}^\mathrm{cat}\ \mathrel{+}=\ \Delta S_{e,1}^{\,\mathrm{mol}}(x(\xi_{\eq,1}(V)),T)
\ \Longrightarrow\ U_1^\mathrm{cat}(T)\ (\propto T^2)\ \Longrightarrow\
\Big(\frac{\dd Q}{\dd V}\Big)_\mathrm{T1}\text{ 봉우리의 다온도 이동}\;}
\label{eq:lco-plugin}
\end{equation}
구조 변경은 없다 — \emph{파라미터 교체 + 이 한 항}이 전부이며, 관측 신호는 T1 봉우리의 $\partial U_1/\partial T$ 가
$T$ 에 선형으로 커지는 것(위치 이동 $\propto T^2$)이다.
```

**원 줄글 대비**: 현행 code 절은 eq:msmr(L1770–1773) + 동형 대응 프로즈(L1774–1780) + 두 변경(param 교체·전자항 한 줄, L1781–1789) → 5A MSMR (a)→(d)(정규화·`f=−σ_d`·동형 박스 eq:lco-msmr) + 5B plug-in (a)→(d)(좌표매핑 `x=x(ξ_eq,1(V))`→몰당 평가→ΔS_rxn,1→U_1(T² 적분)→dQ/dV, 박스 eq:lco-plugin). 스타일리포트 §1 지정 "MSMR식→정규화→대응대입(f=−σ_d)→ξ_eq,j→peak box" + "x=x(ξ_eq,1(V))→ΔS_e,1(V,T)→ΔS_rxn,1(V,T)→U_1(T)→dQ/dV" 둘 다 완결.

**논리 감사(재유도)**:
- **MSMR f=−σ_d 재유도**: 지수 +f(U−U_j^0) vs −σ_d(V−U_j^d), 같은 자리 → f=−σ_d → x_j/X_j=1/(1+exp[−σ_d(U−U_j^d)/w_j])=**ξ_eq,j(eq:xieq)** 정확 일치 ✓ (현행 L1776–1778 정합).
- **좌표매핑**: x=x(ξ_eq,1(V)) — 현행 decomp L1758–1760 예고와 동일 ✓.
- **T² 적분(M-10)**: ∫_{T_0}^T a_e T′dT′=(a_e/2)(T²−T_0²), ½ 인자 유지, 기계 곱 금지 ✓ (eq:U1T2 L1074 정확 일치).
- **단위 가드**: N_A 곱 몰당(eq:dSemolar), eV→J 나눗셈(eq:gunit) — 누락 시 10²³·1/e_V² 배 오류 회피 ✓ (현행 L1785–1787 정합).
- **부호**: ΔS_e,1<0(삽입기준), a_e<0 → 고온 U_1 외삽이 선형보다 낮음(곡률 식별신호) ✓.
- **불가침**: eq:msmr·dSegate·dSemolar·gunit·U1T2 재유도 없이 참조·대입만 ✓; 구조 변경 0 유지 ✓.

---

## 6. 갈래 2 — H-2 정정문안 (Ch2 §ssec:logistic ↔ 파생 C 챕터-내부 모순 일원화)

### 6.1 현행 상태 실측 (v1.0.12 Ch2 — FABLE C-4 대비 진척)
FABLE_REAUDIT_C4_note.md 의 CRITICAL 2건 중 **사인 오류(#1)는 v1.0.12 에서 이미 정정**됨(eq:Veq_BW L191–193 이 `V_eq=U_j−(RT/F)ln[θ/(1−θ)]−(Ω/F)(1−2θ)` 로 eq:muV 와 정합). **w_j 지위 모순(#2=H-2)도 대부분 해소**됨:
- 파생 C(ssec:weff L540) 제목 = "폭 $w$ 의 지위: **단상 평형 예측 vs. 두-상 현상학적 피팅 폭**" — 이중지위 명시.
- ssec:BW L205–206 괄호 + sec:mixing intro L436–438 괄호 + revheat 종합식 keybox L681–686 = 모두 "두-상 $w_j$ = 현상학적 자유 폭(파생C·Ch1 broadening)" 로 **한정어 이미 병기**.
- 파생 A srcbox(L485–496) = 완전식이 FD 와 부동소수점 일치(단순식만 최대 0.18 mV/K 빗나감). eq:dxidT(L461–467)에 `∂w/∂T=R/F`(`w(T)` 조각) **명시 포함**.

**남은 H-2 갭 = 단 한 곳 + 전제 명시 한 줄**:
1. **§ssec:logistic keybox(L161–166)**: "logistic 폭 $w=RT/F$ 는(...전이별 $w_j=n_jRT/F$ 는 §sec:revheat·코드 func_w) **임의 모수가 아니라** ... 분포의 열적 폭이다." — **무한정 단정**(두-상 흑연 staging 포함 전 전이에 걸림). 파생 C·revheat 종합식·ssec:BW 괄호가 모두 한정한 것을 이 keybox 만 한정 없이 남겨 챕터 내부에서 홀로 어긋난다.
2. **파생 A srcbox(L485–496)**: 부동소수점 검증이 **모든 전이에 `w_j(T)=n_jRT/F` 열적 스케일(코드 func_w)을 강제한다는 전제** 위에서 성립함이 미명시 — 이 전제가 파생 C(두-상=현상학 자유폭)와 파생 A(부동소수점 일치)를 화해시키는 load-bearing 고리(FABLE 지적: Case 2 로 $w$ 동결 시 완전식/단순식 오차가 자리바꿈).

### 6.2 일원화 원리 (Ch1 이중지위와 챕터 간 정합)
Ch1 §sec:width(L740–755) "★폭 $w_j$ 의 이중지위 — 같은 식, 다른 지위" 가 정확한 화해틀을 이미 준다: **함수형** `w_j=n_jRT/F`(코드 func_w 가 전 전이에 균일 적용, 열적 기울기 `∂w/∂T=n_jR/F`)와 **진폭 `n_j`(또는 기준온도의 `w_j`)의 지위**를 분리하라 —
- 단상(Ω≤2RT): `n_j` 가 \emph{평형 예측}(n_j≈1, w=RT/F 검증가능). keybox 단정이 전폭 성립.
- 두-상(Ω>2RT, 흑연 staging): `n_j`(진폭)는 \emph{현상학적 자유 피팅}(broadening 이 정함, 파생C·Ch1 broadening)이나, 코드는 여전히 `n_jRT/F` \emph{열적 스케일 함수형}을 유지(Ch1 L1271–1273: staging 출발값 n_j=1 고정, 실평가 폭 RT/F).

곧 파생 C 의 "두-상 ≠ 평형 예측 nRT/F" 는 \emph{진폭의 지위}(평형 고정 아님)를 부정한 것이지 \emph{열적 스케일 함수형}을 폐기한 게 아니며, 파생 A 의 부동소수점 검증은 그 함수형(코드 func_w)을 전제로 겹침식의 자기무모순을 확인한 것이다. 세 서술(logistic keybox·파생C·파생A)이 이 [함수형 ∥ 진폭 지위] 분리로 완전 정합한다.

### 6.3 정정 문안 (편입 지시)

**(H-2a) §ssec:logistic keybox(L163) — 단상 한정어 삽입.** 현행 문장 "logistic 폭 $w=RT/F$ 는(...) **임의 모수가 아니라** 단일 자리 2-상태 분배함수~\eqref{eq:Z1} 가 정하는 분포의 열적 폭이다." 를 아래로 교체:

```latex
logistic 폭 $w=RT/F$ 는(자리당 $n_j{=}1$ 기준; 전이별 유효 폭 $w_j=n_jRT/F$ 는 \S\ref{sec:revheat}$\cdot$코드
\texttt{func\_w}) \emph{단상 전이($\Omega\le2RT$)에서} 임의 모수가 아니라 단일 자리 2-상태 분배함수~\eqref{eq:Z1} 가
정하는 분포의 \emph{검증 가능한 평형 예측}(열적 폭)이다. \textbf{두-상 전이($\Omega>2RT$, 흑연 staging 이 여기 속함)}
에서는 코드가 같은 $n_jRT/F$ \emph{열적 스케일 함수형}(\texttt{func\_w}, $\partial w/\partial T=n_jR/F$)을 그대로 쓰되,
그 \emph{진폭} $n_j$(또는 기준온도의 $w_j$)의 지위는 평형 예측이 아니라 broadening 이 정하는 \emph{현상학적 자유 피팅}
파라미터로 바뀐다(파생 C \S\ref{ssec:weff}; Chapter 1 폭 이중지위$\cdot$broadening 절). 곧 ``함수형은 전 전이 공통,
진폭의 지위는 $\Omega_j$ 가 가른다''가 본 keybox 단정의 정확한 적용 범위다.
```

**(H-2b) 파생 A srcbox(L489–491 부근) — 검증 전제 한 줄 삽입.** "완전식은 175 점 ... 부동소수점 정밀도로 일치" 뒤에 아래를 덧댄다:

```latex
\emph{이 부동소수점 일치는} 현행 코드(\texttt{func\_w})가 네 흑연 staging 전이 \emph{전부}에 대해
$w_j(T)=n_jRT/F$ 열적 스케일($\partial w/\partial T=n_jR/F$, 식~\eqref{eq:dxidT} 의 $w(T)$ 조각)을 균일하게 강제한다는
\emph{전제} 위에서 성립한다 — 곧 이 검증이 확인하는 것은 그 \emph{열적 스케일 함수형을 주었을 때} 겹침 가중식의
자기무모순이지, 두-상 전이의 폭이 \emph{평형에서} $nRT/F$ 로 예측된다는 정리가 아니다(그 진폭 지위는 파생 C 가
한정한다). 만약 $w_j$ 를 기준온도에서 동결해 $T$-무관으로 두면 단순식과 완전식의 오차 크기가 자리를 바꾸므로,
어느 공식이 옳은지는 전적으로 이 열적 스케일 전제에 달려 있다.
```

**(H-2c) 챕터 간 정합 확인(문안 아님, 편입 검증 게이트)**: (H-2a)(H-2b) 삽입 후, ssec:logistic keybox·파생 C(L540)·revheat 종합식 keybox(L681–686)·ssec:BW 괄호(L205–206)·sec:mixing intro 괄호(L436–438)·Ch1 §sec:width 이중지위(L740–755)가 **모두 "함수형 공통 ∥ 진폭 지위는 Ω_j 판정"** 로 일치하는지 확인(현재 남은 유일한 홀로-어긋남 = keybox 무한정 단정을 (H-2a)가 제거).

**논리 감사(재유도)**:
- **FABLE C-4 #2 화해 재확인**: [함수형 w=n_jRT/F(∂w/∂T=n_jR/F, 균일·코드 강제) ∥ 진폭 n_j 지위(단상=평형예측/두-상=자유피팅)] 분리 → 파생C·파생A·logistic keybox 3자 무모순 ✓. FABLE Case2(w 동결→오차 자리바꿈)는 (H-2b)가 "열적 스케일 전제"로 흡수 ✓.
- **Ch1 정합**: §sec:width L746 "어느 지위인지는 코드 분기가 아니라 Ω_j 값이 가르며, 같은 식이 두 경우 모두에 쓰인다" + L1271–1273 "코드 staging 출발값 n_j=1 고정" 과 (H-2a) 정확 일치 ✓.
- **부호/물리 불변**: 결과식·수치 무변경, 한정어·전제 명시만 추가(base "H-2 한정어" 범위 준수) ✓.
- **범위 준수**: eq:Veq_BW 사인(이미 정정)·다른 CRITICAL 미접촉, H-2(w_j 지위)만 정정 ✓.

---

## 7. 신설/재사용 라벨 목록 + 충돌 검증

| 라벨 | 절 | 지위 | 충돌 검증 |
|---|---|---|---|
| `eq:lco-n0sub` | center (a) | 신설 | grep 0 (기존 lco-* 2개 열거 확정) |
| `eq:lco-dUdT` | center (d) | **재사용(필수)** | 기존 L487, 6개 `\eqref`(L493·498·1229·1750·1790·1877) 유지 위해 승계 |
| `eq:lco-J` | hys (a) | 신설 | grep `No matches` |
| `eq:lco-gxi` | hys (a) | 신설 | 기존 `eq:gxi` 와 별개 |
| `eq:lco-spinodal` | hys (b) | 신설 | 기존 `eq:spinodal` 와 별개 |
| `eq:lco-Veq` | hys (c) | 신설 | 기존 `eq:Veq` 와 별개 |
| `eq:lco-dUhys` | hys (d) | 신설 | 기존 `eq:dUhys` 와 별개 |
| `eq:lco-Ubranch` | hys (d) | 신설 | 기존 `eq:Ubranch` 와 별개 |
| `eq:lco-mit` | hys T1 | 신설 | grep `No matches` |
| `eq:lco-dope` | hys 도핑 | 신설 | grep `No matches` |
| `eq:lco-peak` | peak (d) | 신설 | 기존 `eq:eqpeak` 와 별개 |
| `eq:lco-Zfac` | decomp (b) | 신설 | grep `No matches` |
| `eq:lco-decomp` | decomp (d) | **재사용(필수)** | 기존 L1723, 다수 `\eqref`(L505·508·1040·1060·1729·1738·1761·1785·1879) 유지 위해 승계 |
| `eq:lco-msmr` | code 5A (d) | 신설 | 기존 `eq:msmr` 와 별개 |
| `eq:lco-plugin` | code 5B (d) | 신설 | grep `No matches` |

- **신설 = 13개(전부 `eq:lco-*`), 재사용 = 2개(`eq:lco-dUdT`·`eq:lco-decomp`)**. 기존 `eq:lco-*` 는 이 2개뿐이라 신설 13 전원 충돌 0. finalizer 는 번호 흐름에 맞춰 신설명을 조정해도 되나 **두 재사용만은 불변**(다운스트림 `\eqref` load-bearing).

## 8. finalizer 편입 체크리스트
1. center: L477–494 삭제 → §1 블록. `eq:lco-dUdT` 가 (d) 박스에 **유일** 존재 확인(현행 L487 정의 제거, 중복 금지). L493·498 verifybox 참조가 새 (d) 박스를 가리키는지 확인.
2. hys: L697–719 삭제 → §2 블록. L696 헤더·L722 `sec:width` 인접 확인.
3. peak: L1221–1232 삭제 → §3 블록. L1220 헤더·L1234 `sec:broadening` 인접. L1229 의 `eq:lco-dUdT` 참조 보존.
4. decomp: L1718 뒤 (a)(b)(c) 삽입, eq:lco-decomp 박스(L1719–1724) (d) 승계, 기존 itemize 보존.
5. code: eq:msmr 주변 5A + 전자항 5B 삽입. L1785 의 `eq:lco-decomp` 참조 보존.
6. Ch2: (H-2a) keybox L163 문장 교체, (H-2b) 파생 A srcbox L489–491 뒤 전제 한 줄, (H-2c) 정합 게이트.
7. 매크로 확인: `\operatorname{artanh}`·`\code`·`\rxn`·`\eq`·`\dd`·`\bg`·`\hys`·`\cell`·`\avg`·verifybox·codebox·keybox·srcbox 는 두 tex 기존 사용 계열.
8. 빌드 후 `eq:lco-dUdT`·`eq:lco-decomp` 미해결 참조 0, 물리·부호·수치·`Ω_j`·verifybox·전자엔트로피 절·`sec:lco-map/Se/gate` 불변 확인.

---

## 9. 5줄 요약
1. **수식화 커버**: 갈래1 = center·hys(V1011 계승·재유도 재검·v1.0.12 줄번호 재mapping·두-상 피팅판정으로 개선) + peak·decomp·plug-in·MSMR(신작) 6절 전부를 (a)출발→(b)연산→(c)중간식→(d)박스 forward 사슬로 폐쇄; 신설 라벨 13 + 재사용 2. 갈래2 = H-2 3-part 문안(keybox 단상한정어 + 파생A 열적스케일 전제 + 챕터간 정합 게이트).
2. **논리결함 발견여부**: 대상 6절 유도에서 물리 오류 **0**(center 이중경로·hys ΔU_hys/Taylor·peak 세양·decomp 인수분해·MSMR f=−σ_d·plug-in T² 전부 손계산 재유도로 흑연 원식과 정확 일치). 챕터-내부 모순은 이미 알려진 H-2 잔여 1건(logistic keybox 무한정 단정)뿐 — 본 문안이 [함수형 ∥ 진폭 지위] 분리로 일원화.
3. **물리 불변 확인**: 결과식·부호·수치(+0.83 mV/K·+80·0.47/1.49 config ΔS·8RT/3F·¼·1.1 k_B) 무변경, `Ω_j` 기호 유지(날조 0), 신규 개념(ρ/PSD/입자반경) 도입 0, M-10 가드(∫ΔS dT′·T² 적분) 유지, 불가침 절(map/Se/gate/N0-N9/전자엔트로피/verifybox) 미접촉 — 전개 형식만 줄글→수식.
4. **v1.0.12 진척 반영**: FABLE C-4 #1 사인오류·#2 대부분(파생C 제목·revheat 종합식·괄호들) 이미 정정 확인 → 재작업 중복 회피, H-2 잔여 최소 델타(keybox 1문장 + srcbox 1줄)만 제안.
5. **최약점**: (i) peak/decomp/code 신작은 현행 v1.0.12 에 이미 상당 서술이 있어 finalizer 가 "사슬 승격 vs 기존 프로즈 보존" 경계를 조율해야 함(본 드래프트는 기존 itemize·부호규약 보존 전제로 (a)(b)(c) 골격만 추가). (ii) two-phase "3 중 3 후보→피팅 판정" 개선은 현행 L698–699 "세 전이 모두 대응" 강프레이밍을 완화하는 것이라, finalizer 가 tab:lco-staging 캡션(pure-LCO 초기값)과의 톤 정합을 최종 확인 요망. (iii) H-2b 는 파생 A `\cite{numverif2026}` 검증 문맥 안이라, 편입 시 srcbox 내부 흐름과의 문장 접합만 다듬으면 됨.

**출력 파일: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1012_P43_draft_O2.md`**
