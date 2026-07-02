# V1012 Phase 4.3 — 작성 드래프트 O3 (LCO 6절 수식화 + H-2 정정문안)

> 역할: 경쟁 드래프트 O3 (Opus). ★드래프트만(.md supplement) — tex/코드 미수정. 편입은 Fable master.
> 대상 Ch1: `Claude/docs/v1.0.12/graphite_ica_ch1_v1.0.12.tex` (실측 정독 완료, head→tail)
> 대상 Ch2: `Claude/docs/v1.0.12/graphite_ica_ch2_v1.0.12.tex` (H-2 대상, §ssec:logistic·파생 A/C·sec:revheat 정독)
> 계승 출발점: `results/process/V1011_P11_map_v10.md`(center·hys) — 재유도 검증 후 계승, v1.0.12 실측 대조로 갱신.
> 참조: `V1010_LCO_STYLE_REPORT.md` §1 "필요한 수식 사슬" · `FABLE_REAUDIT_C4_note.md` §2(H-2 근거).
> 물리·결과식·부호·수치 불변(전개 형식 변환만), Ω_j 기호 유지(0.47/1.49 = config ΔS, 날조 없음), 신규 개념 0.

---

## 0. 조립 전 확정 사실 (v1.0.12 실측 근거)

### 0.1 v1.0.12 실측 위치 (v1.0.11 대비 라인 이동 확인)
| 절 | 헤더(보존) | 현재 상태 | 교체/삽입 대상(줄) | 다음 경계(불변) |
|---|---|---|---|---|
| `sec:lco-center` | L476 | eq:lco-dUdT(∂U/∂T만) + 프로즈 intro + verifybox | **L477–494**(프로즈 intro + eq:lco-dUdT 박스) 교체, **L496–516 verifybox 보존**·L518–519 다리 보존 | L522 `sec:hys` |
| `sec:lco-hys` | L696 | 프로즈 3문단((T2·T3)/(T1)/도핑), 수식 사슬 0 | **L697–719**(프로즈 전체) 교체 | L722 `sec:width` |
| `sec:lco-peak` | L1220 | 프로즈 (★최약), 봉우리 박스식 없음 | **L1221–1232**(프로즈 전체) 교체 | L1234 `sec:broadening` |
| `sec:lco-decomp` | L1715 | eq:lco-decomp 박스 有 + itemize(가산성 줄글 검산) | **L1719–1741**(박스 앞 다리 + config·직교 itemize) 앞에 (a)(b)(c) 사슬 삽입, eq:lco-decomp 박스는 유지·보강 | itemize 잔여·L1750~ |
| 전자항 plug-in | `sec:lco-code` L1784–1789 (ii) | 프로즈 "한 줄 더함" | (ii) 항 프로즈를 forward 사슬 박스로 교체 | (iii)/L1790 |
| MSMR 동형 | `sec:lco-code` L1767–1780 | eq:msmr + 대응표 프로즈 | eq:msmr 이후 대응 프로즈에 변환 사슬 박스 삽입 | (i)(ii) enumerate |

### 0.2 ★라벨 충돌 전수 검증 (load-bearing)
- v1.0.12 Ch1 의 **기존 `eq:lco-*` 라벨 전수 = {`eq:lco-dUdT`(L487), `eq:lco-decomp`(L1723)} 딱 2개**(grep 확정, L487·L1723). 그 2개를 뺀 임의의 `eq:lco-*` 신설명은 충돌 0.
- ★**`eq:lco-dUdT` 재사용 필수**(base 명시 "6곳 다운스트림"): 정의(L487) 외에 verifybox L498, `sec:lco-peak` L1229, `sec:lco-decomp` L1750, `sec:lco-code` L1790 등에서 `\eqref` 참조. center 교체 범위 L477–494 가 이 정의를 포함하므로, 새 (d) 박스가 **반드시 `\label{eq:lco-dUdT}` 를 이어받아야** 다운스트림 참조가 산다.
- ★**`eq:lco-decomp` 재사용 필수**: `sec:lco-center` L489(프로즈)·verifybox L505·L513·`sec:lco-electronic` L1060·`sec:lco-peak`·plug-in 이 참조. decomp 박스는 label 유지.
- 신설 후보 전원 새 이름(`eq:lco-n0sub`·`eq:lco-J`·`eq:lco-gxi`·`eq:lco-gpp`·`eq:lco-spinodal`·`eq:lco-Veq`·`eq:lco-dUhys`·`eq:lco-Ubranch`·`eq:lco-mit`·`eq:lco-dope`·`eq:lco-peak1`·`eq:lco-peaksum`·`eq:lco-Zfac`·`eq:lco-nodc`·`eq:lco-plugin`·`eq:lco-msmrmap`) — 위 2개와 문자열 상이, 충돌 0. (섹션 라벨 `sec:lco-peak` 와 `eq:lco-peak1` 은 다른 문자열이라 무관하나, 혼동 방지로 봉우리식은 `eq:lco-peak1`/`eq:lco-peaksum` 로 둠.)

### 0.3 불가침 확인
`sec:lco-map`(L301)·`sec:lco-Se`(L965)·`sec:lco-gate`(L1082)·N0–N9 흑연 본체·전자엔트로피 절·verifybox(L496–516) 미접촉. **M-10 가드 유지** = `eq:U1T2`(L1073–1075, T1 전자항 ∝T 의 T_ref 적분·T² 곡률)는 손대지 않고 center·peak·plug-in 에서 **참조만** 한다.

### 0.4 ★v1.0.12 프레이밍 갱신 반영 (V1011 대비 개선)
v1.0.12 `sec:width`(L740–755)는 흑연 4 staging 을 "**초기값에선 4 전이 전부 Ω>2RT(두-상), 피팅으로 override → dilute→stage4·4L↔3L 은 Ω<2RT 단상, 2L→2·2→1 만 두-상 유지**"로 재프레이밍했다. V1011 map 의 "흑연 4중2 = 확정" 서술은 이 갱신에 맞춰 "**흑연 4중4 초기 → 피팅 후 2중2**"로 갱신한다(아래 §2 two-phase calibration). LCO 는 v1.0.12 `sec:lco-peak` L1225·`sec:lco-hys` L698 대로 세 전이 전부 Ω>2RT(초기값), 최종 gap 은 피팅 Ω_j^cat 이 정하고 도핑은 일부를 2RT 로 내릴 수 있음.

---

## 1. `sec:lco-center` — LCO 평형 중심 (a→d 수식 사슬)

**편입 지시**: L477–494(프로즈 intro + 현 eq:lco-dUdT 박스)를 아래 블록으로 교체. L476 헤더·L496–516 verifybox·L518–519 다리 보존. (d) 박스가 **`\label{eq:lco-dUdT}` 를 이어받음**(중복 정의 금지 — 교체로 유일해짐). M-10 은 `eq:U1T2` 참조로 유지.

```latex
식~\eqref{eq:Uj} 의 $U_j(T)$ 유도에는 \emph{전극 가정이 한 단계도 없다}(\S\ref{sec:lco-map} 가 세운 전극-중립
골격). LCO 양극으로의 확장은 새 물리가 아니라 세 진입 자리의 \emph{입력 치환}일 뿐이므로, 흑연 forward 사슬을
그대로 되짚어 LCO 중심과 그 온도 계수를 닫는다.

\textbf{(a) 출발 — 전극-중립 세 진입과 host$\to$cat 치환.} $U_j$ 로 가는 세 자리 어디에도 ``흑연''이라는 물질 고유
항이 없다: (i) 실험조건 매핑 식~\eqref{eq:n0map}(방향 부호$\cdot$전류 환산)은 삽입형 전극 공통, (ii) 전기화학 평형
조건 식~\eqref{eq:eqcond}($\Delta G_j=-sFU_j$)는 삽입 반쪽반응 식~\eqref{eq:eqbalance} 에서 나오며 host 의 화학
정체는 상수 $\mu^0$ 로만 흡수되고, (iii) 비배치 몫 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 은 반응종에
무관한 열역학 항등식이다. LCO 로 넘어갈 때 이 세 자리에 들어가는 것은 전이 집합과 입력값의 치환뿐이다:
\begin{equation}
j\in\mathcal J_\mathrm{LCO}=\{\mathrm{T1},\mathrm{T2},\mathrm{T3}\},\qquad
(\Delta H_{\rxn,j},\Delta S_{\rxn,j})\ \longmapsto\
(\Delta H_{\rxn,j}^\mathrm{cat},\Delta S_{\rxn,j}^\mathrm{cat}).
\label{eq:lco-n0sub}
\end{equation}

\textbf{(b) 연산 — 평형 조건에 반응 자유에너지 대입.} 전이 $j$ 의 비배치 반응 자유에너지 $\Delta G_j^\mathrm{cat}
=\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}$ 를 식~\eqref{eq:eqcond} 의 $\Delta G_j=-sFU_j$
($s=+1$)에 넣으면
\[
\Delta H_{\rxn,j}^\mathrm{cat}-T\Delta S_{\rxn,j}^\mathrm{cat}=-F\,U_j^\mathrm{cat}(T)
\]
로, 흑연 식~\eqref{eq:Ujmid} 과 글자 그대로 같은 식에 상첨자 $\mathrm{cat}$ 만 붙는다((a)의 host-무관 대입 확인).

\textbf{(c) 중간식 — 중심 이항과 $\partial U/\partial T$ 의 이중경로.} (b)를 $U_j^\mathrm{cat}$ 로 이항하면 흑연
식~\eqref{eq:Uj} 와 같은 함수형이다. 온도 계수는 두 독립 경로가 같은 값에 닿는다. \emph{경로 1(직접 미분)}:
$\Delta H^\mathrm{cat}$ 는 $T$ 무관, $T\Delta S^\mathrm{cat}$ 의 미분이 $\Delta S^\mathrm{cat}$ 이라
$\partial U_j^\mathrm{cat}/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}/F$. \emph{경로 2(Gibbs 항등식)}: 등압
$\partial\Delta G_j/\partial T|_P=-\Delta S_{\rxn,j}^\mathrm{cat}$(식~\eqref{eq:gibbsdef} $G\equiv H-TS$)와
식~\eqref{eq:eqcond} 의 $\Delta G_j=-FU_j$ 미분을 등치하면
\[
-F\,\frac{\partial U_j^\mathrm{cat}}{\partial T}=-\Delta S_{\rxn,j}^\mathrm{cat}
\ \Longrightarrow\
\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}.
\]
두 경로 어디에도 host 구분 항이 없다 — 이것이 ``전극 불문''의 수식적 의미다.

\textbf{(d) 박스 — LCO 양극 중심과 온도 계수.}
\begin{equation}
\boxed{\;
U_j^\mathrm{cat}(T)=\frac{-\Delta H_{\rxn,j}^\mathrm{cat}+T\,\Delta S_{\rxn,j}^\mathrm{cat}}{F},
\qquad
\frac{\partial U_j^\mathrm{cat}}{\partial T}=\frac{\Delta S_{\rxn,j}^\mathrm{cat}}{F}
\quad(j\in\mathcal J_\mathrm{LCO})\;}
\label{eq:lco-dUdT}
\end{equation}
흑연 식~\eqref{eq:Uj} 와 부호까지 1:1 이고 바뀌는 것은 값뿐이다 — 양극의 높은 중심($\sim$3.9--4.2 V)은 분자
$-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양인 데서 오고, $\Delta S_{\rxn,j}^\mathrm{cat}$ 는
\S\ref{sec:lco-decomp}(식~\eqref{eq:lco-decomp})에서 config$\cdot$vib$\cdot$전자 세 성분으로 분해된다.
\textbf{★다온도 해석(M-10).} 전자항 $\Delta S_{e,j}(x,T)\propto T$ 인 T1 은 $\Delta S_{\rxn,j}^\mathrm{cat}$ 가
$T$ 의존이라, 고정 $\Delta H$ 로 $U_j(T)=(-\Delta H+T\Delta S(T))/F$ 를 기계 미분하면 $\Delta S+T\,\partial_T\Delta S$
가 생긴다. 열역학적으로 유지할 관계는 위 박스의 $\partial U_j^\mathrm{cat}/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}(T)/F$
이고, 위치는 기준온도 $T_\mathrm{ref}$ 적분
\[
U_j^\mathrm{cat}(T)=U_j^\mathrm{cat}(T_\mathrm{ref})+\frac1F\int_{T_\mathrm{ref}}^{T}\Delta S_{\rxn,j}^\mathrm{cat}(T')\,\dd T'
\]
로 해석한다 — config$\cdot$vib($T$ 무관)는 이 적분이 $\Delta S_0(T-T_\mathrm{ref})/F$ 로 선형이고, T1 전자항
($\propto T$)만 곡률을 만들어 식~\eqref{eq:U1T2} 의 $T^2$ 항으로 닫힌다(\S\ref{sec:lco-Se}).
```

**원 줄글 대비**: 현행 L477–483 은 "식~\eqref{eq:Uj}… 유도에 전극 가정 없다… 바뀌는 것은 입력값뿐"의 **단정 프로즈**로 (a)출발→(b)연산→(c)중간식 forward 구조 없이 곧장 eq:lco-dUdT(∂U/∂T 만) 박스로 점프. STYLE_REPORT §1 "center HIGH×2: 전극무관 단정 비약·Gibbs 다리 없는 괄호 전보체"를 (a)(b)(c) 사슬 + 이중경로 유도로 해소.

**논리 감사(재유도 근거)**:
- 차원: $[\Delta H]/[F]=$ J·mol⁻¹ / C·mol⁻¹ $=$ J/C $=$ V ✓; $[\Delta S]/[F]=$ J·mol⁻¹K⁻¹/C·mol⁻¹ $=$ V/K ✓.
- 부호: 발열 $\Delta H^\mathrm{cat}<0$ → 분자 $-\Delta H^\mathrm{cat}>0$ 이 중심을 올림(양극 3.9–4.2 V) ✓ (흑연 L462–463 동일 논리).
- 이중경로: 경로1(직접미분)=경로2(Gibbs)= $\Delta S^\mathrm{cat}/F$ 독립 재유도 일치 ✓.
- detailed balance/이중계산: center 는 detailed balance 무관(그건 §xi_eq), ΔS 3성분 이중계산은 §4 decomp 가드가 담당.
- M-10 정합: 기계 미분 함정($\Delta S+T\partial_T\Delta S$) 명시 + `eq:U1T2` 참조로 T² 곡률 위임 — 전자엔트로피 절 미접촉 ✓.
- 앞 절 정합: (a)가 `sec:lco-map`(L301) 전극-중립 골격을 재유도 없이 참조 → 중복 서술 제거(V1011 map 대비 개선).

---

## 2. `sec:lco-hys` — LCO order–disorder·MIT 정규용액 사슬 (a→d)

**편입 지시**: L697–719(프로즈 3문단)를 아래 블록으로 교체. L696 헤더·L722 `sec:width` 보존. 흑연 결과식(eq:mu·eq:gxi·eq:gpp·eq:spinodal·eq:Veq·eq:hyssub·eq:hysdiff·eq:dUhys·eq:Ubranch)은 재유도 없이 **참조·대입만**.

```latex
\S\ref{sec:hys} 의 격자기체$\cdot$정규용액 자유에너지 식~\eqref{eq:gxi} 는 ``동등한 자리에 리튬이 차고 빈다''는
가정 하나만 쓴다 — 이 가정은 $\mathrm{Li}_x\mathrm{CoO_2}$ 의 팔면체 리튬 자리(자리당 점유 0/1)에도 문자 그대로
성립한다. 새 물리는 없고, 흑연 사슬에 LCO 전이별 입력값 $U_j^\mathrm{cat},\Omega_j^\mathrm{cat},\gamma_j,h_{\eta,j}$
만 끼운다.

\textbf{(a) 출발 — LCO 세 전이를 같은 정규용액 몫에.} LCO 전이 집합
\begin{equation}
\mathcal J_\mathrm{LCO}=\{1:\mathrm{MIT},\ 2:\mathrm{OD}_a,\ 3:\mathrm{OD}_b\}
\label{eq:lco-J}
\end{equation}
의 각 $j$ 에 진행률 $\xi_j$ 를 달아 흑연 식~\eqref{eq:gxi} 와 같은 몫을 쓴다:
\begin{equation}
g_j^\mathrm{cat}(\xi_j)=g_{0,j}^\mathrm{cat}
+RT\{\xi_j\ln\xi_j+(1-\xi_j)\ln(1-\xi_j)\}+\Omega_j^\mathrm{cat}\,\xi_j(1-\xi_j).
\label{eq:lco-gxi}
\end{equation}
\textbf{★two-phase calibration.} 흑연 staging 은 \emph{초기값}에선 네 전이 $\Omega_j$ 가 모두 $2RT
(\!\approx\!4958$ J/mol@298 K, 식~\eqref{eq:spinodal})를 넘어 전부 두-상 후보이나, 피팅으로 override 되면
dilute$\to$stage4$\cdot$$4\mathrm L\!\leftrightarrow\!3\mathrm L$ 은 $\Omega_j<2RT$ 단상(solid-solution),
$2\mathrm L\!\to\!2\cdot2\!\to\!1$ 만 $\Omega_j>2RT$ 두-상으로 갈린다(\S\ref{sec:width}). LCO 는
표~\ref{tab:lco-staging} 의 초기값에서 T1(MIT)$\cdot$T2$\cdot$T3(order--disorder) \emph{세 전이 전부}가 문턱을 넘는
상분리 후보다. 곧 문턱 판정식 $\Omega_j^\mathrm{cat}>2RT$ 자체는 두 전극에서 동일하고, 각 전이의 실제 gap 유무는
\emph{피팅된} $\Omega_j^\mathrm{cat}$ 이 $2RT$ 를 넘는지가 최종 결정한다(도핑 시 $\Omega_j^\mathrm{cat}\le2RT$ 로
내려가는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다, 아래 도핑 문단).

\textbf{(b) 연산 — 곡률과 spinodal 문턱.} 식~\eqref{eq:lco-gxi} 를 두 번 미분하면 흑연 식~\eqref{eq:gpp} 에
전이별 $\Omega_j^\mathrm{cat}$ 만 든다:
\begin{equation}
\frac{\partial^2 g_j^\mathrm{cat}}{\partial\xi_j^2}=\frac{RT}{\xi_j(1-\xi_j)}-2\Omega_j^\mathrm{cat},
\label{eq:lco-gpp}
\end{equation}
곧 spinodal 은
\begin{equation}
\xi_{s,j}^{\pm}=\tfrac12\big(1\pm u_j^\mathrm{cat}\big),\qquad
u_j^\mathrm{cat}=\sqrt{1-\frac{2RT}{\Omega_j^\mathrm{cat}}}\qquad(\Omega_j^\mathrm{cat}>2RT),
\label{eq:lco-spinodal}
\end{equation}
$\Omega_j^\mathrm{cat}\le2RT$ 이면 $u_j^\mathrm{cat}$ 이 실수가 아니라 그 전이의 spinodal gap 은 없다(흑연 코드
분기 그대로).

\textbf{(c) 중간식 — LCO 전위 곡선에 spinodal 대입.} LCO 전이 $j$ 의 평형 전위 곡선은 식~\eqref{eq:Veq} 에
$U_j^\mathrm{cat},\Omega_j^\mathrm{cat}$ 를 넣어
\begin{equation}
V_{\eq,j}^\mathrm{cat}(\xi)=U_j^\mathrm{cat}
+\frac{RT}{sF}\ln\frac{\xi}{1-\xi}+\frac{\Omega_j^\mathrm{cat}}{sF}(1-2\xi)\qquad(s=+1),
\label{eq:lco-Veq}
\end{equation}
이고 두 spinodal 끝점에서(흑연 식~\eqref{eq:hyssub} 대입) $\dfrac{\xi}{1-\xi}\big|_{\xi_{s,j}^\pm}
=\dfrac{1\pm u_j^\mathrm{cat}}{1\mp u_j^\mathrm{cat}}$, $(1-2\xi)\big|_{\xi_{s,j}^\pm}=\mp u_j^\mathrm{cat}$ 이므로
극대$-$극소 차는(상수 중심 $U_j^\mathrm{cat}$ 상쇄, 흑연 식~\eqref{eq:hysdiff} 와 동형)
\[
\Delta U_{j}^{\hys,\mathrm{cat}}=V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^-)-V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^+)
=\frac{2}{F}\big[\Omega_j^\mathrm{cat}u_j^\mathrm{cat}-2RT\,\mathrm{artanh}\,u_j^\mathrm{cat}\big].
\]

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
흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 대입형이다. 방전($\sigma_d=+1$)은 분기 중심을 위로,
충전($\sigma_d=-1$)은 아래로 옮긴다.

\textbf{(T2$\cdot$T3) order--disorder.} $x\approx0.5$ 부근 monoclinic 초격자(점유 Li 와 빈자리의 교대 정렬)를
이루는 T2($\sim$4.05 V)$\cdot$T3($\sim$4.17--4.20 V)는 동종 이웃 인력 $\Omega_j^\mathrm{cat}>0$ 이 만드는 상분리의
LCO 사례로, 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j=2,3$ 을 넣어 각각 열린다.
\textbf{★$\Omega$ 와 config $\Delta S$ 의 구분(혼동 가드).} 정렬의 charge-order 엔트로피 변화($\approx0.47$ J/(mol\,K)
@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$ [tier A, Motohashi\cite{motohashi2009}])는 \emph{엔트로피}
값으로 표~\ref{tab:lco-staging}$\cdot$식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 슬롯(따라서 $U_j^\mathrm{cat}(T)$
온도 이동)에 들어가지, spinodal 문턱을 정하는 \emph{상호작용 에너지} $\Omega_j^\mathrm{cat}$[J/mol]가 \emph{아니다}
— 둘은 서로 다른 양이므로 ``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 다리를 놓아선 안 되고, $\Omega_j^\mathrm{cat}$ 는
gap 을 정하는 별도 피팅 파라미터로 둔다.

\textbf{(T1) MIT 2상역.} T1($\sim$3.90 V, $x\approx0.94$--$0.75$, 절연체$\to$금속)의 구조적 2상 공존도 식
~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j=1$ 을 넣어 같은 문턱을 받는다. MIT 고유의 전자 자유도는
이 히스 gap 에 새 항으로 섞지 않는다 — 그 항은 이미 $\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^\mathrm{config}
+\Delta S_1^\mathrm{vib}+\Delta S_{e,1}^\mathrm{mol}(x,T)$(식~\eqref{eq:lco-decomp})를 통해 $U_1^\mathrm{cat}(T)$ 의
온도 이동(식~\eqref{eq:lco-dUdT})에 들어간다. 두 몫이 서로 다른 슬롯에 산다:
\begin{equation}
\boxed{\;
\underbrace{\Delta U_1^{\hys,\mathrm{cat}}\ \Leftarrow\ \Omega_1^\mathrm{cat}}_{\text{정규용액 히스 gap (이 절)}}
\quad\Big\|\quad
\underbrace{\partial U_1^\mathrm{cat}/\partial T\ \Leftarrow\ \Delta S_{e,1}^\mathrm{mol}(x,T)}_{\text{전자 엔트로피 (\S\ref{sec:lco-electronic})}}\;}
\label{eq:lco-mit}
\end{equation}
이 분리가 config 2상역과 전자 엔트로피를 이중계산하지 않는 경계다.

\textbf{도핑 보정(우리 시료).} Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox$\cdot$전자항을 보존하되
order--disorder$\cdot$MIT 상전이를 억제한다 — 정규용액 틀에서 이는 pure-LCO 초기값 $\Omega_j^\mathrm{cat,pure}$ 를
도핑 피팅값 $\Omega_j^\mathrm{cat,dop}$ 로 낮추는 입력 변화다. 식~\eqref{eq:lco-dUhys} 의 문턱 극한은(흑연
식~\eqref{eq:dUhys} 아래 Taylor $\mathrm{artanh}\,u=u+u^3/3+\cdots$ 재사용, $T_{c,j}=\Omega_j^\mathrm{cat}/2R$)
\begin{equation}
\Omega_j^\mathrm{cat,dop}\to2RT^+\ \Longrightarrow\
u_j^\mathrm{cat,dop}\to0,\quad
\Delta U_j^{\hys,\mathrm{cat,dop}}\to\frac{8RT}{3F}\big(u_j^\mathrm{cat,dop}\big)^3\to0,
\label{eq:lco-dope}
\end{equation}
곧 $\Omega_j^\mathrm{cat,dop}\le2RT$ 로 피팅되는 전이는 gap 이 0 으로 닫혀 히스 축소$\cdot$peak smear 로 나타나며,
풀린 몫은 \S\ref{sec:broadening} 의 broadening 폭이 더 크게 담는다. \textbf{★슬롯 분리.} 중심 전위의 미세 shift
는 같은 전이 dict 의 $U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로} 들어가며, $\Omega_j^\mathrm{cat}$ 하나가
gap$\cdot$smear 와 중심 이동을 동시에 만든다고 쓰지 않는다.
```

**원 줄글 대비**: 현행 L697–719 는 "같은 정규용액 틀 그대로 적용" 서술 3회((T2·T3)/(T1)/도핑)에 Ω_j spinodal 대입 중간식 전무(STYLE_REPORT §1 "hys HIGH×3"). 흑연 sec:hys 의 μ(θ)→g″→spinodal→ΔU_hys 사슬을 LCO Ω_j^cat 로 (a)→(d) 재전개해 해소.

**논리 감사(재유도 근거)**:
- gap 유도 독립 재검산: $V_{\eq}(\xi_s^-)=U+\tfrac{RT}{F}\ln\tfrac{1-u}{1+u}+\tfrac{\Omega}{F}u$, $V_{\eq}(\xi_s^+)=U+\tfrac{RT}{F}\ln\tfrac{1+u}{1-u}-\tfrac{\Omega}{F}u$ → 차 $=\tfrac{2\Omega}{F}u-\tfrac{4RT}{F}\mathrm{artanh}\,u=\tfrac{2}{F}[\Omega u-2RT\,\mathrm{artanh}\,u]$ ✓(흑연 eq:hysdiff L621 일치).
- 문턱 극한 재검산: $\Omega\to2RT^+$ 에서 $\Omega=2RT/(1-u^2)$ 대입 → $\Omega u-2RT\,\mathrm{artanh}\,u=2RT(u+u^3+\cdots)-2RT(u+u^3/3+\cdots)=\tfrac{4RT}{3}u^3$ → $\Delta U_{\hys}\to\tfrac{8RT}{3F}u^3\to0$ ✓(흑연 L634 일치, 부호 양).
- 차원: $[\Omega u]/[F]=$ J/mol / (C/mol) $=$ V ✓; artanh·u 무차원 ✓.
- 부호: 극대 $>$ 극소 → $\Delta U^\hys\ge0$; $\sigma_d=+1$(방전) 중심 up ✓.
- 이중계산: T1 히스 gap(Ω_1) ∥ 전자 엔트로피(∂U/∂T) 슬롯 분리 박스(eq:lco-mit) — config 2상역과 전자항 무중복 ✓.
- 수치 날조 0: Ω_j^cat 기호 유지, 0.47/1.49 는 config ΔS 로 명시(Ω 아님) ✓.
- ★v1.0.12 정합: two-phase calibration 을 "흑연 4중4 초기→피팅 후 2중2"로 갱신(§0.4) — L747–755 서술과 모순 0(V1011 map "4중2 확정" 대비 개선).

---

## 3. `sec:lco-peak` — LCO 세 봉우리 평형 peak (a→d) [★최약 보강]

**편입 지시**: L1221–1232(프로즈)를 아래 블록으로 교체. L1220 헤더·L1234 `sec:broadening` 보존. 흑연 eq:eqpeak·eq:belliden·eq:xieq·eq:sum 은 참조·대입만.

```latex
평형 peak 식~\eqref{eq:eqpeak} 은 전극을 가리지 않으므로, LCO 세 전이의 봉우리를 같은 forward 사슬로 닫는다 —
새 물리 없이 $j\in\mathcal J_\mathrm{LCO}$ 로 합산 범위만 바뀐다.

\textbf{(a) 출발 — 전하 보존식의 LCO 합산.} 보존식 $Q_\cell q=Q_\bg(V_n)+\sum_{j\in\mathcal J_\mathrm{LCO}}
Q_j\xi_j$ 를 궤적으로 미분하면 흑연 식~\eqref{eq:sum} 과 같은 선형 합 $\dd Q/\dd V_n=C_\bg+\sum_jQ_j\,\dd\xi_j/\dd V_n$
이 된다(서로소 자리 분해 전제).

\textbf{(b) 연산 — LCO 평형 종.} 각 전이의 평형 점유는 식~\eqref{eq:xieq} 에 LCO 중심$\cdot$폭을 넣은
$\xi_{\eq,j}^\mathrm{cat}=\{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]\}^{-1}$ 이고, 종 항등식
식~\eqref{eq:belliden}($\dd\xi_\eq/\dd z=\xi_\eq(1-\xi_\eq)$)에 연쇄율 $\dd z/\dd V=\sigma_d/w_j$ 를 곱하면
\begin{equation}
\frac{\dd\xi_{\eq,j}^\mathrm{cat}}{\dd V}
=\frac{\sigma_d\,\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j}.
\label{eq:lco-peak1}
\end{equation}

\textbf{(c) 중간식 — 세 봉우리 합산.} 이를 보존식 미분에 넣으면 LCO 하프셀 평형 dQ/dV 가 세 전이의 종의 합으로
닫힌다:
\[
\Big(\frac{\dd Q}{\dd V}\Big)^\eq_\mathrm{LCO}
=C_\bg+\sum_{j\in\{\mathrm{T1,T2,T3}\}}Q_j\,\frac{\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j}.
\]

\textbf{(d) 박스 — 봉우리별 세 양과 합.}
\begin{equation}
\boxed{\;
\Big(\frac{\dd Q}{\dd V}\Big)^\eq_j
=Q_j\,\frac{\xi_{\eq,j}^\mathrm{cat}(1-\xi_{\eq,j}^\mathrm{cat})}{w_j}
=Q_j\Big|\frac{\dd\xi_{\eq,j}^\mathrm{cat}}{\dd V}\Big|,\quad
\begin{cases}
\text{위치}=U_j^{\,d,\mathrm{cat}}\\[2pt]
\text{순높이}=Q_j/(4w_j)\\[2pt]
\text{면적}=Q_j
\end{cases}
\;}
\label{eq:lco-peaksum}
\end{equation}
흑연 식~\eqref{eq:eqpeak} 과 동형이라 위치$=$중심 $U_j^{\,d,\mathrm{cat}}$, 순높이$=Q_j/(4w_j)$($\xi=\tfrac12$
에서 $\xi(1-\xi)=\tfrac14$), 배경 차감 면적$=Q_j$($\int_0^1\dd\xi=1$)의 세 양이 그대로 읽힌다. 흑연이
$\sim$0.085--0.21 V 에 네 봉우리를 남기듯 LCO 하프셀은 양극 영역에 세 봉우리를 남긴다 — T1 $\sim$3.90 V(MIT),
T2 $\sim$4.05 V, T3 $\sim$4.17--4.20 V. 폭은 흑연과 같은 $w_j=n_jRT/F$ 이고, LCO 세 전이는 모두 $\Omega_j^\mathrm{cat}
>2RT$ 의 두-상이라 그 폭은 \S\ref{sec:width} 이중지위의 \emph{두-상 측}(평형 예측이 아니라 broadening 이 정하는
현상학적 피팅 폭, \S\ref{sec:broadening})이다. order--disorder 의 큰 $\Omega^\mathrm{cat}$ 가 spinodal gap 을 키워
T2$\cdot$T3 를 좁은 한 쌍 peak 로 가른다.

\textbf{★T1 봉우리의 온도 이동 신호.} T1 위치의 온도 이동률은 전자항을 통해 $\partial U_1^\mathrm{cat}/\partial T
=\Delta S_{\rxn,1}^\mathrm{cat}(T)/F$(식~\eqref{eq:lco-dUdT})이며, 전자항 $\Delta S_{e,1}\propto T$(식~\eqref{eq:dSe})
이므로 \emph{이동률이 $T$ 에 선형}이고 봉우리 \emph{위치}의 이동은 그 적분이라 $\propto T^2$(식~\eqref{eq:U1T2}) —
``$\partial U_1/\partial T$ 가 $T$ 선형''이 식별 신호이지 ``위치가 $T$ 선형''이 아니다. 도핑은 \S\ref{sec:lco-hys}
대로 봉우리를 smear$\cdot$shift 시킨다.
```

**원 줄글 대비**: 현행 L1221–1232 는 "평형 peak 식 전극무관 적용"·T1/T2/T3 위치 줄글 열거로 **봉우리 박스식 없음**(STYLE_REPORT §1 "★최약 Major"). ξ_eq,j→dξ/dV→ΣQ_j peak_shape→center/height/area 박스(j∈{T1,T2,T3})로 폐쇄.

**논리 감사(재유도 근거)**:
- 종 항등식 재검산: $\dd\xi_\eq/\dd z=e^{-z}/(1+e^{-z})^2=\xi_\eq(1-\xi_\eq)$ ✓(eq:belliden L1198 일치).
- 세 양 재검산: 순높이 $=Q_j\cdot\tfrac14/w_j=Q_j/(4w_j)$ ✓; 면적 $=\int Q_j|\dd\xi/\dd V|\dd V=Q_j\int_0^1\dd\xi=Q_j$ ✓(치환적분, eq:eqpeak L1214–1215 일치).
- 부호: $\sigma_d$ 미분에서 한 번 들어오나 peak 모양 $=|\dd\xi/\dd V|=\xi(1-\xi)/w\ge0$ 방향 불변 ✓.
- 차원: $Q_j/w_j=$ C/V $=$ dQ/dV ✓.
- T1 신호: 위치 이동 $\propto T^2$ 는 `eq:U1T2`(M-10) 참조만 — 전자엔트로피 절 미접촉 ✓. (V1011 map 은 eq:U1T2 이전이라 일반 ∫만; 여기선 구체 T² 링크로 개선.)
- 앞 절 정합: 폭 이중지위(§sec:width)·broadening(§sec:broadening) 두-상 측 참조 — L1225–1226 서술과 일치.

---

## 4. `sec:lco-decomp` — ΔS 3성분 분해 (분배함수 인수분해 사슬 보강)

**편입 지시**: L1719–1724 의 eq:lco-decomp 박스는 **label 유지·존치**. 박스 \emph{앞}(L1718 다리 뒤)에 아래 (a)(b)(c) 인수분해 사슬을 삽입하고, 박스 \emph{뒤} 이중계산 가드에 no-double-count 식 `eq:lco-nodc` 를 추가(현행 L1729–1741 의 줄글 검산을 식으로 승격). itemize(config/vib/electronic)·L1750~ 는 보존.

```latex
\textbf{(a) 출발 — 세 자유도.} 삽입 반응 엔트로피는 ``리튬 자리 배열''(config)$\cdot$``격자 진동''(vib)$\cdot$
``전자 준위 점유''(electronic) 세 자유도의 합이다(\S\ref{sec:lco-why}). 세 자유도가 서로 다른 상태공간에 살면
전체 미시상태는 곱 상태공간이다.

\textbf{(b) 연산 — 분배함수 인수분해.} config 부분계와 electronic 부분계가 (선도 차수에서) 독립이면 전체 분배함수는
곱으로 인수분해된다:
\begin{equation}
Z=Z_\mathrm{config}\cdot Z_\mathrm{vib}\cdot Z_\mathrm{elec}
\quad\Longrightarrow\quad
S=k_B\ln Z=S_\mathrm{config}+S_\mathrm{vib}+S_\mathrm{elec}.
\label{eq:lco-Zfac}
\end{equation}
$S=k_B\ln Z$ 가 곱 분배함수에서 합으로 떨어지는 것이 세 몫 \emph{가산성}의 통계역학적 근거다(교차/잔차 항은
MIT 부근 리튬 정렬--밴드채움 결합에서 0 이 아니나 선도 차수에서 무시).

\textbf{(c) 중간식 — 삽입 미분과 슬롯 배정.} 식~\eqref{eq:lco-Zfac} 를 조성으로 미분($\partial/\partial x$, 삽입
기준)하면 전이당 반응 엔트로피가 세 슬롯으로 갈린다 — config 슬롯에는 봉우리 \emph{중심 표준값} $\Delta S_j^0$
(봉우리 내부 $x$-의존은 logistic 이 자동 생성, \S\ref{sec:dist}), vib 슬롯에는 음의 baseline, elec 슬롯에는 MIT
게이트의 몰당 값 $\Delta S_{e,j}^\mathrm{mol}$(식~\eqref{eq:dSemolar})이 들어간다. 이 배정이 (d) 박스다.
```

**(d) 박스 = 기존 `eq:lco-decomp`(L1719–1724) 유지**. 그 뒤 이중계산 가드에 다음 식 삽입(현행 L1729–1741 "★이중계산 금지(B)"·"가법성 정당화" 줄글의 식 승격):

```latex
\textbf{★무이중계산(식으로).} config 슬롯은 봉우리 중심($\xi_j=\tfrac12$, config$=0$)의 표준값만, 봉우리 내부
분포 항은 logistic 이 담으므로, 실제 온도 계수는
\begin{equation}
\frac{\partial U_j^\mathrm{cat}}{\partial T}
=\frac1F\Big[\underbrace{\Delta S_j^0}_{\text{중심 표준(config+vib+elec 중심값)}}
+\underbrace{R\ln\frac{1-\xi_j}{\xi_j}}_{\text{봉우리 내부 config, logistic 자동}}\Big]
\label{eq:lco-nodc}
\end{equation}
로 한 번씩만 센다 — config 를 $\Delta S_j^0$ 에 또 더하면 이중계산이다(중심에서 config$=0$ 이라 두 정의가
모순 없이 맞물린다). Ch2 파생 B$\cdot$식~\eqref{eq:single_config} 와 정확히 같은 분리다.
```

**원 줄글 대비**: 현행은 eq:lco-decomp 박스는 있으나 "Z=Z_config·Z_elec→S=S_config+S_elec 가산·중심표준값·무이중계산"이 줄글 검산(STYLE_REPORT §1 "Moderate"). (b) 인수분해식(eq:lco-Zfac) + (d) 무이중계산식(eq:lco-nodc)으로 승격.

**논리 감사(재유도 근거)**:
- 인수분해 재검산: 독립 부분계 $Z=\prod Z_k$ → $S=k_B\ln\prod Z_k=\sum k_B\ln Z_k=\sum S_k$ ✓(표준 통계역학).
- 무이중계산: 중심 $\xi=\tfrac12$ 에서 $R\ln[(1-\xi)/\xi]=R\ln1=0$ → 표준값에 내부항 무중복 ✓(Ch2 파생 B L533–538·eq:single_config L529 일치).
- 부호: 삽입 기준 $\Delta S_{e,j}<0$(MIT, eq:dSe L1027) — decomp 슬롯 규약과 일관, 부호 뒤집기 없음 ✓.
- 직교성 vs 무초과 구분 유지: (b)는 "더해도 되는가"(가산성), eq:lco-nodc 는 "과대계상 없는가"(무초과) — 현행 L1738–1741 구분 보존 ✓.
- 라벨: eq:lco-decomp 재사용(6+곳 참조 유지), eq:lco-Zfac·eq:lco-nodc 신설(충돌 0) ✓.

---

## 5. 전자항 plug-in — forward 사슬 (sec:lco-code (ii))

**편입 지시**: L1784–1789 의 (ii) 항 프로즈("한 줄 더함")를 아래 forward 사슬 박스로 교체. eq:dSegate/dSemolar/lco-decomp/lco-dUdT/U1T2/sum 은 참조만(전자엔트로피 절 미접촉).

```latex
\item \textbf{전자 엔트로피 항 plug-in (좌표 매핑 포함 forward 사슬).} 전자항은 \emph{조성} $x$ 의 함수인데 코드는
\emph{전압} 격자 위에서 도므로, T1 진행률로 좌표를 이어 한 사슬로 닫는다:
\begin{equation}
\boxed{\;
\underset{\text{(1) 좌표}}{x=x\big(\xi_{\eq,1}(V)\big)}
\ \to\
\underset{\text{(2) 게이트}}{\Delta S_{e,1}^\mathrm{mol}(V,T)=N_A\,\frac{\pi^2}{3}k_B^2T\,\frac{\partial g(E_F,x)}{\partial x}}
\ \to\
\underset{\text{(3) 슬롯}}{\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^0+\Delta S_{e,1}^\mathrm{mol}}
\ \to\
\underset{\text{(4) 중심}}{U_1^\mathrm{cat}(T)}
\ \to\
\underset{\text{(5) 곡선}}{\frac{\dd Q}{\dd V}}
\;}
\label{eq:lco-plugin}
\end{equation}
곧 (1) T1 전이 진행률 $\xi_{\eq,1}(V)$ 을 정규화 조성 $x$ 에 대응시켜 게이트 인자 $z=(x-x_\mathrm{MIT})/\Delta x_\mathrm{MIT}$
를 $V$ 격자 위에서 평가하고, (2) 게이트 닫힌식~\eqref{eq:dSegate}(몰당 환산 식~\eqref{eq:dSemolar}, eV$\to$J
나눗셈 식~\eqref{eq:gunit})로 $\Delta S_{e,1}^\mathrm{mol}(V,T)<0$ 를 얻어, (3) 식~\eqref{eq:lco-decomp} 의 T1
슬롯에 \emph{한 줄}로 더하고, (4) 식~\eqref{eq:lco-dUdT}$\cdot$\eqref{eq:U1T2} 로 $U_1^\mathrm{cat}(T)$ 의 온도
이동(전자항이 $T^2$ 곡률 기여)에 태운 뒤, (5) 흑연과 \emph{같은} 합산식~\eqref{eq:sum} 으로 dQ/dV 에 들어간다.
\textbf{★단위 주의} — 슬롯 $\Delta S_{\rxn,j}$ 는 J/(mol\,K) 라 자리당 식~\eqref{eq:dSe}($k_B$ 차원)가 아니라
$N_A$ 를 곱한 몰당 식~\eqref{eq:dSemolar} 를 넣어야 한다($N_A$ 누락 시 $\sim10^{23}$ 배 과소; eV$\to$J 는 곱이
아니라 나눗셈, 식~\eqref{eq:gunit}).
```

**원 줄글 대비**: 현행 (ii)(L1784–1789)는 "T1 ΔS_rxn 에 몰당 전자항 더하는 한 줄" + 단위 주의 프로즈(STYLE_REPORT §1 "Major"). x=x(ξ_eq,1(V))→ΔS_e,1(V,T)→ΔS_rxn,1(V,T)→U_1(T)→dQ/dV 5단계 forward 사슬 박스로 폐쇄(좌표 매핑을 사슬 첫 고리로 명시).

**논리 감사(재유도 근거)**:
- 좌표 매핑: 게이트는 x-함수, dqdv 는 V-격자 → x=x(ξ_eq,1(V)) 로 잇는 것이 유일 정합 경로 ✓(현행 L1756–1760 서술과 일치, 사슬화만).
- 단위 다리: $N_Ak_B^2=Rk_B$ → 자리당 $k_B$ → 몰당 $R$ ✓(eq:dSemolar L1032). eV→J 나눗셈(eq:gunit L1044) 곱 시 $1/e_V^2$ 오차 가드 유지 ✓.
- 부호: $\partial g/\partial x<0$(삽입 x↑ → g 감소) → $\Delta S_{e,1}<0$ 삽입 기준 슬롯 일관 ✓(eq:dSe·dSegate L1056·L1107).
- ∝T / T²: 이동률 ∝T(eq:dSe), 위치 ∝T²(eq:U1T2) — M-10 가드 참조 유지, 절 미접촉 ✓.
- 이중계산: (3) 슬롯 = 중심 $\Delta S_1^0$ + elec, config 내부항은 logistic(§4 eq:lco-nodc) — 무중복 ✓.

---

## 6. MSMR 동형 — 변환 사슬 폐쇄 (sec:lco-code)

**편입 지시**: L1774–1780(eq:msmr 이후 대응 프로즈)에 아래 변환 사슬 박스 삽입. eq:msmr·eq:xieq·eq:eqpeak 참조.

```latex
MSMR 식~\eqref{eq:msmr} 이 Ch1 곡선 클래스와 \emph{같은 peak 을 낸다}는 것을 대응$\to$변환 사슬로 닫는다.
\begin{equation}
\boxed{\;
\underset{\text{(1) MSMR}}{x_j=\frac{X_j}{1+e^{f(U-U_j^0)/\omega_j}}}
\ \xrightarrow[\text{정규화}]{\ \tilde x_j\equiv x_j/X_j\ }\
\underset{\text{(2) 대응}}{\tilde x_j=\frac{1}{1+e^{f(U-U_j^0)/\omega_j}}}
\ \xrightarrow[f=-\sigma_d,\ U_j^0\to U_j^{\,d},\ \omega_j\to w_j]{}\
\underset{\text{(3) 동형}}{1-\xi_{\eq,j}}
\;}
\label{eq:lco-msmrmap}
\end{equation}
곧 (1) MSMR 종별 분율을 (2) 용량 $X_j$ 로 정규화하면 지수 하나만 남은 logistic 이 되고, (3) 방향 인자 대응
$f=-\sigma_d$(두 지수 $+f(U-U_j^0)$ 와 $-\sigma_d(V-U_j^{\,d})$ 가 같은 자리이므로)를 넣으면 $\tilde x_j$ 는 점유형
$\theta_{\eq,j}=1-\xi_{\eq,j}$ 와 같은 식~\eqref{eq:xieq} 이다. 봉우리는 미분에서 닫힌다 —
\[
\Big|\frac{\dd x_j}{\dd U}\Big|=\frac{X_j}{\omega_j}\,\tilde x_j(1-\tilde x_j)
\ \longleftrightarrow\
Q_j\,\frac{\xi_{\eq,j}(1-\xi_{\eq,j})}{w_j}\quad(\text{식~\eqref{eq:eqpeak}}),
\]
용량 가중 $X_j\!\leftrightarrow\!Q_j$, 폭 $\omega_j\!\leftrightarrow\!w_j$ 대응으로 MSMR 의 dQ/dV$=\sum_j|\dd x_j/\dd U|$
가 Ch1 평형 peak 합산과 \emph{같은 종의 합}이다. 따라서 Ch1 코드가 구조 변경 0 으로 LCO(MSMR 초기값)를 그린다.
```

**원 줄글 대비**: 현행 L1774–1780 은 대응표(X_j↔Q_j 등)는 좋으나 "MSMR→ξ_eq,j→eqpeak 변환 사슬 미폐쇄"(STYLE_REPORT §1 "Moderate"). MSMR→정규화→대응대입(f=−σ_d)→ξ_eq,j→peak 박스로 폐쇄.

**논리 감사(재유도 근거)**:
- 방향 인자 재검산: 지수 $+f(U-U_j^0)$ vs $-\sigma_d(V-U_j^d)$ 동일 자리 → $f=-\sigma_d$ ✓(현행 L1776–1778 일치).
- 정규화: $\tilde x_j=x_j/X_j\in[0,1]$ → 점유형 logistic → $\theta_{\eq,j}=1-\xi_{\eq,j}$ ✓.
- peak 동형: $|\dd x_j/\dd U|=(X_j/\omega_j)\tilde x_j(1-\tilde x_j)$ ↔ $Q_j\xi_\eq(1-\xi_\eq)/w_j$ 종 항등식 공유 ✓(eq:belliden·eq:eqpeak).
- 물리 불변: 새 개념 0, 대응은 기호 치환뿐 ✓.

---

## 7. H-2 정정문안 (Ch2 §ssec:logistic keybox 일원화)

**근거**: `FABLE_REAUDIT_C4_note.md` §2 (CRITICAL — w_j 열적 스케일링 지위 구조적 자기모순). **실측 상태**(v1.0.12 Ch2):
- eq(2.11) BW 부호는 이미 정정됨(`eq:Veq_BW` L191–193 = 정정형, FABLE §1 해소). H-1 처리 완료 — **손대지 않음**.
- 파생 C(`ssec:weff` L540–569)는 이미 "단상 평형 예측 vs 두-상 현상학적 피팅 폭" 이중지위로 재작성됨(FABLE §2 방향과 정합).
- **잔존 모순 = §ssec:logistic keybox(L161–166)** 만이 "logistic 폭 $w_j=n_jRT/F$ … 임의 모수가 아니라 분배함수가 정하는 열적 폭"을 **한정 없이 단정**(두-상 폭까지 평형 예측처럼 읽힘) ↔ 파생 C 두-상 서술과 충돌. 파생 A(`ssec:overlap` L485–496)의 "완전식=FD 부동소수점 일치" 검증은 코드 `func_w`=n·R·T/F 가 \emph{모든} 전이에 강제하는 $w_j(T)=n_jRT/F$ 스케일을 전제로 성립.

**편입 지시**: L162–165 keybox 본문(★표기 문장 앞까지)을 아래로 교체. eq:Z1 참조·표기 문장(L164–165)·srcbox 파생 A 는 보존.

```latex
Chapter 1 의 평형 종 $\xi_\eq$ 는 \emph{현상학적 곡선맞춤}이 아니라 \emph{격자기체 점유 분포의 여집합}(탈리튬화
진행률 $=1-\theta$)이다. logistic 폭의 \emph{함수형} $w_j=n_jRT/F$(자리당 $n_j{=}1$ 이면 $w=RT/F$)는 임의 모수가
아니라 단일 자리 2-상태 분배함수~\eqref{eq:Z1} 가 정하는 \emph{열적 스케일}이다 — 지수가 $\beta F(V-U_j)
=(V-U_j)/(RT/F)$ 라 폭이 $T$ 에 선형($\partial w_j/\partial T=n_jR/F$)인 것이 분배함수의 직접 결과이며, 코드
\texttt{func\_w}$(T,n)=nRT/F$ 가 \emph{모든} 전이(단상$\cdot$두-상 공통)에 이 열적 스케일을 강제한다. 아래 파생 A
(\S\ref{ssec:overlap})의 ``완전식$=$FD 부동소수점 일치''도 바로 이 $w_j(T)=n_jRT/F$ 스케일을 전제로 성립한다
(만약 $w_j$ 를 $T_\mathrm{ref}$ 에서 동결하면 단순식과 완전식의 우열이 뒤바뀐다). \textbf{단, 그 \emph{값}(진폭
$n_j$, 또는 $T_\mathrm{ref}$ 의 $w$)의 지위는 전이 종류로 갈린다} — \emph{단상($\Omega\le2RT$, 균질 고용체)}
에서는 $w_j$ 가 평형 등온선이 예측하는 \emph{검증 가능한 평형 폭}이지만, \emph{두-상($\Omega>2RT$, 흑연 staging)}
에서는 평형이 델타를 예측하므로 $w_j$ 는 broadening 이 정하는 \emph{현상학적 자유 피팅 폭}이다(파생 C
\S\ref{ssec:weff}; 이는 Chapter 1 폭 이중지위 절과 챕터 간 정합이다). 곧 분배함수가 못박는 것은 폭의 \emph{열적
함수형}이고, 두-상 폭의 \emph{절댓값}은 피팅이 정한다.
```

**원 줄글 대비**: 현행 keybox 는 "$w_j=n_jRT/F$ … 임의 모수 아님"을 **함수형과 값 구분 없이 무한정 단정** → 두-상 폭도 분배함수가 정하는 것처럼 읽혀 파생 C 와 챕터 내부 충돌. 정정문안은 (1) **함수형**(열적 스케일 $\partial w/\partial T=n_jR/F$, 분배함수 결과, 모든 전이 공통·파생 A 전제)과 (2) **값**(진폭)의 이중지위(단상=평형 예측, 두-상=현상학적 피팅)를 갈라, "임의 모수 아님"을 함수형에는 유지하고 값에는 **단상(Ω≤2RT) 한정**을 붙여 일원화.

**논리 감사(재유도 근거)**:
- 함수형이 분배함수 결과임 재검산: $Z_1=1+e^{-\beta\Delta\mu}$, $\Delta\mu=-F(V-U_j)$(몰당) → 지수 $(V-U_j)/(RT/F)$ → 폭 $=RT/F$, $\partial w/\partial T=R/F$(n_j 배로 $n_jR/F$) ✓ — 열적 스케일은 수학적 필연, "임의 모수 아님" 정당.
- 두-상 값이 현상학적임 재검산: 두-상 평형 단일입자=델타(plateau), 실측 유한폭=broadening(①②③) → 값은 피팅 ✓(파생 C L547–559).
- 파생 A 전제 명시 근거: FABLE §2 Case 1(열적 스케일)=완전식 PASS / Case 2(T_ref 동결)=단순식·완전식 우열 역전 → 검증은 코드-강제 $w=n_jRT/F$ 를 전제(FABLE 확증) ✓. 정정문안에 이 전제를 1문장으로 명시.
- 챕터 간 정합: Ch1 §sec:width 이중지위(단상 평형/두-상 피팅, L740–755) ↔ Ch2 파생 C ↔ 정정 keybox — 삼자 일치 ✓.
- 불변: eq(2.11) 정정형·파생 C 본체 미접촉, keybox 표기 문장·srcbox 보존, 물리 결론(두-상 폭=피팅) 불변 ✓.

---

## 8. 신설/재사용 라벨 목록 + 충돌 검증

| 라벨 | 절 | 지위 | 충돌 검증 |
|---|---|---|---|
| `eq:lco-n0sub` | center (a) | 신설 | v1.0.12 전수 {dUdT,decomp}와 상이 → 0 |
| `eq:lco-dUdT` | center (d) | **재사용(필수)** | 기존 L487, 다운스트림 ≥6 참조 유지 위해 label 승계 |
| `eq:lco-J` | hys (a) | 신설 | 0 |
| `eq:lco-gxi` | hys (a) | 신설 | 기존 `eq:gxi`와 별개 문자열 → 0 |
| `eq:lco-gpp` | hys (b) | 신설 | 기존 `eq:gpp`와 별개 → 0 |
| `eq:lco-spinodal` | hys (b) | 신설 | 기존 `eq:spinodal`와 별개 → 0 |
| `eq:lco-Veq` | hys (c) | 신설 | 기존 `eq:Veq`와 별개 → 0 |
| `eq:lco-dUhys` | hys (d) | 신설 | 기존 `eq:dUhys`와 별개 → 0 |
| `eq:lco-Ubranch` | hys (d) | 신설 | 기존 `eq:Ubranch`와 별개 → 0 |
| `eq:lco-mit` | hys T1 | 신설 | 0 |
| `eq:lco-dope` | hys 도핑 | 신설 | 0 |
| `eq:lco-peak1` | peak (b) | 신설 | 섹션 `sec:lco-peak`와 별개 문자열 → 0 |
| `eq:lco-peaksum` | peak (d) | 신설 | 0 |
| `eq:lco-Zfac` | decomp (b) | 신설 | 0 |
| `eq:lco-decomp` | decomp (d) | **재사용(필수)** | 기존 L1723, 다운스트림 참조 유지 |
| `eq:lco-nodc` | decomp 가드 | 신설 | 0 |
| `eq:lco-plugin` | code (ii) | 신설 | 0 |
| `eq:lco-msmrmap` | code MSMR | 신설 | 0 |

- **신설 15개 + 재사용 2개(`eq:lco-dUdT`,`eq:lco-decomp`)**. 전부 `eq:lco-*` 프리픽스. 기존 `eq:lco-*` 는 {dUdT,decomp} 2개뿐이라 신설 15개 전원 충돌 0(0.2 전수확정).
- finalizer 는 번호 흐름에 맞춰 신설 라벨명을 조정해도 되나, **`eq:lco-dUdT`·`eq:lco-decomp` 재사용은 불변**(다운스트림 `\eqref` load-bearing).

---

## 9. 5줄 요약

1. **수식화 커버**: 6절 전부 흑연 forward (a)출발→(b)연산→(c)중간식≥1→(d)박스 사슬로 재작성 — center(이중경로 ∂U/∂T + M-10 T² 링크)·hys(eq:lco-J→gxi→gpp→spinodal→Veq→dUhys/Ubranch + T1 MIT 슬롯분리 + 도핑 Taylor)·peak(★최약 보강: ξ_eq→dξ/dV→Σ3전이 center/height/area 박스)·decomp(Z=Z_config·Z_elec 인수분해 + 무이중계산식)·plug-in(x=x(ξ_eq,1)→ΔS_e→ΔS_rxn→U_1→dQ/dV 5고리)·MSMR(정규화→f=−σ_d→ξ_eq→peak 동형). H-2 = keybox 함수형/값 분리 일원화.
2. **논리결함 발견여부**: LCO 재적용 절에 신규 물리 결함 **없음**(모든 사슬 독립 재유도로 흑연 결과식과 부호·차원·극한 일치). 발견한 것은 서술 형식 결함(줄글 결론)뿐이며 수식화로 해소. Ch2 H-2 는 이미 파생 C·eq(2.11) 정정 완료, **잔존은 §logistic keybox 무한정 단정 1건**으로 국소.
3. **물리 불변 확인**: 결과식·부호·수치·Ω_j 기호 전부 불변(전개 형식만 줄글→수식). 0.47/1.49=config ΔS(Ω 아님) 유지, 수치 날조 0, 신규 개념(ρ/PSD 등) 0, verifybox·전자엔트로피 절·map·gate·N0-N9 불가침. M-10(eq:U1T2 T² 곡률)은 참조만.
4. **챕터 간 정합**: two-phase calibration 을 v1.0.12 갱신("흑연 4중4 초기→피팅 2중2")에 맞춰 조정(V1011 map "4중2 확정" 대비 개선); Ch1 폭 이중지위 ↔ Ch2 파생 C ↔ 정정 keybox 삼자 일치. eq:lco-dUdT·eq:lco-decomp 재사용으로 다운스트림 참조 무손상.
5. **최약점**: (i) center (d) 박스가 eq:lco-dUdT 재사용이라 현행 verifybox(L498 참조)와의 label 유일성을 finalizer 가 편입 시 반드시 확인해야 함(중복 정의 시 빌드 실패). (ii) MSMR 대응 $\tilde x_j\leftrightarrow1-\xi_{\eq,j}$ 는 MSMR 종별 부호 관례($f$ 정의)에 의존 — 코드 `LCO_MSMR_LIT` 구현의 실제 $f$ 부호로 round-trip 확인 권장(본 드래프트는 tex 서술 기준). (iii) decomp 인수분해 (b)의 교차항 무시는 "선도 차수" 가정이라 MIT 중심에서 가장 약함(현행 L1736 서술과 동일 한계, 신규 위험 아님).

**출력 파일**: `D:\Projects\Project_Anode_Fit\Claude\results\process\V1012_P43_draft_O3.md`
**ID: O3 (Opus, 무통신 독립 드래프트)**
