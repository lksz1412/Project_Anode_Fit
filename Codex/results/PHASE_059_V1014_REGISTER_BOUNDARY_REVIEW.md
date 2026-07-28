# Phase 059 v1.0.14 register·본문 경계 재판정

정본일: 2026-07-28

판정: `CONDITIONAL_P059_V1014_PEDAGOGICAL_ASSET_WITH_THEORY_BOUNDARY_AND_WIDTH_ROLE_DEBTS`

## 결론

v1.0.14는 v1.0.13보다 분명히 나아졌다. Ch1은 단일 자리
대정준 유도를 내부 자유도 $q(T)$와 유효 자리 자유에너지까지
확장하고, broadening 폭 예산과 PSD/Gibbs--Thomson 배제 논리를
식으로 추가했다. 이것은 보존할 교재 자산이다.

그러나 “교재·리뷰 깊이·theory-only 경계를 완결했다”는 주장은
성립하지 않는다. Ch2의 순증은 18행이고 새
displayed equation은 0개다. 더 결정적으로 Ch1에 구현 대응 부록을
만들고도 제목·헤더·날짜·본문에 코드 진행, 현 코드, `dict`,
self-test가 남는다. 따라서 v1.0.14는 최종 정본이 아니라
`PRESERVE_ASSET + CORRECT_BOUNDARY` 대상이다.

## Exact diff 규모

| document | lines old→new | net | equations unchanged/changed/added | sequence ratio |
|---|---:|---:|---:|---:|
| Ch1 | 2934→3445 | +511 | 101/10/5 | 0.741 |
| Ch2 | 776→794 | +18 | 20/2/0 | 0.934 |

Ch1의 changed equation 10개 중 5개는 실제 통계역학 유도 변경,
5개는 code identifier를 추상 물리/연산 표기로 바꾼 경계 정리다.
신규 식 5개는 $\tilde\varepsilon$, 내부 자유도 엔트로피, 폭 예산,
PSD 적분, Gibbs--Thomson 이동이다. Ch2의 changed equation 2개는
$Z_1\to\Xi_1$ 대정준 표기와 같은 단일자리 bridge의 엄밀화다.

## Theory-only 경계

v1.0.14 Ch1의 구현 관련 rendered lines는 전용 구현 부록 안
97개다. 부록 밖 mention은
28개이고, 그중 전용 부록으로 보내는
navigation 5개를 제외한
boundary violation은 23개다.
Ch2에는 전용 구현 절이 없으며 violation
1개가 남는다.
v1.0.13의 두 장 합계 violation
230개에서
v1.0.14의 24개로
크게 줄인 것은 실제 개선이지만 0은 아니다. 아래 표는 comments와
TeX macro 정의를 제외한 rendered source만 센 것이다.

| line | class | source excerpt |
|---:|---|---|
| 76 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `pdftitle={흑연 음극 + LCO 양극 dQ/dV 이론: 코드 진행을 따라가는 수식-구동 (유도 확장) — Chapter 1 (v1.0.14)}}` |
| 78 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `\lhead{흑연 음극 + LCO 양극 $dQ/dV$ 이론 — Ch.1 (v1.0.14, 통계역학-first + 코드 진행)}\rhead{\thepage/\pageref{LastPage}}` |
| 103 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `\title{\textbf{\LARGE Chapter 1}\\[0.35em]\Large 흑연 음극 + LCO 양극 $dQ/dV$ 이론: 한 곡선을 그리는 코드 진행을 따라가는 수식-구동판 — 유도 확장}` |
| 105 | OUTSIDE_DIRECT_IMPLEMENTATION_CONTENT | `\date{\normalsize 버전 1.0.14 \quad(코드 \texttt{Anode\_Fit 1.0.14} 와 동일 버전 · matched)}` |
| 141 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `합산식과, ``이 문건만 보고 같은 곡선을 재현하는 코드를 짤 수 있다''는 실행 가능성이다. 본론에 앞서 Part 0` |
| 156 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `펼치는 일이다. 코드 진행이 이 세 갈래를 차례로 닫는다.` |
| 230 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `c\_rate 는 시간 역수이므로 $Q_\cell$ 과 시간 단위를 맞춰 대입한다([1/h]$\cdot$[A\,h]$\to$[A]; 코드 규격화` |
| 289 | OUTSIDE_NAVIGATIONAL_REFERENCE_ALLOWED | `물리 기호와 구현 식별자의 대응은 부록~\ref{sec:appendix-code}(표~\ref{tab:symcode})에 정리한다.` |
| 930 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `쓰는 평형식의 전 유도가 이 사다리에 있다 --- 이후 절은 같은 사다리를 결과 사슬(코드 진행 N1--N9) 순서로` |
| 994 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `Part 0(\S\ref{sec:sm-ensemble}$\cdot$\S\ref{sec:sm-electro}$\cdot$\S\ref{sec:sm-macro})가 세웠다 — 이 절은 그 위에서 코드 입력` |
| 1054 | OUTSIDE_NAVIGATIONAL_REFERENCE_ALLOWED | `$U(298)=(13000-298.15\times16)/96485\approx0.0853$ V 로 목표 $0.085$ V 와 정합한다. 구현 대응은` |
| 1445 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `이 소절은 결과식$\cdot$부호$\cdot$코드는 그대로 두고 $\xi_\eq$ 의 통계역학적 정체만 밝혀,` |
| 1615 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `0.014 V($2\mathrm L\!\to\!2$)$\cdot$0.012 V($2\!\to\!1$)와 모순되지 않는다. 단 \emph{현재 코드의 staging` |
| 1974 | OUTSIDE_NAVIGATIONAL_REFERENCE_ALLOWED | `\emph{상수} 하나(대표 $T_\rep\cdot$대표 $n$)로 한 번만 평가된다. 구현 대응은` |
| 2159 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `override 하는 것이 전제) — 이 표가 있어 ``이 문건만으로 곡선 재현 코드를 짤 수 있다''.` |
| 2260 | OUTSIDE_DIRECT_IMPLEMENTATION_CONTENT | `★시연값($U{=}3.930/3.880/4.050$ V; 전자항은 T1$=$MIT dict 에` |
| 2263 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `별개라 round-trip 피팅으로 정합한다. 또한 현 구현은 $\Delta S_e$ 를 기준온도 $T_\mathrm{ref}$ 에서` |
| 2624 | OUTSIDE_DIRECT_IMPLEMENTATION_CONTENT | `같은 전이 dict 의 $U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로} 들어가며, $\Omega_j^\mathrm{cat}$ 하나가` |
| 2860 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `forward 코드는 전이 파라미터를 LCO 값으로 치환하고 이 항 하나를 추가하는 것만으로 LCO 에 적용된다(\S\ref{sec:lco-code}).` |
| 2923 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `흑연에서 합산식~\eqref{eq:sum} 의 $\Delta S_{\rxn,j}$ 는 평형 중심 $U_j(T)$ 를 통해 한 덩이로 작용했으나, LCO 양극에서는 이 한 덩이가 세 물리 성분(config=배치$\cdot$vib=격자진동$\cdot$electronic=전자)의 합임을 명시` |
| 2998 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `$x\!\leftrightarrow\!\xi_{\eq,1}(V)$ 매핑으로 좌표를 잇는다(구현식은 \S\ref{sec:lco-code} 식~\eqref{eq:lco-xmap}). \emph{(ii) round-trip 가드.} 식~\eqref{eq:lco-decomp} 의 config ` |
| 3002 | OUTSIDE_DIRECT_IMPLEMENTATION_CONTENT | `$U_1(298)\approx3.90$ V 와 $\partial U_1/\partial T$ 의 부호$\cdot$기울기(다온도 이동률)를 self-test 로 맞추어` |
| 3148 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `\subsection{전체 진행 요약}\label{sec:facade}` |
| 3152 | OUTSIDE_NAVIGATIONAL_REFERENCE_ALLOWED | `표~\ref{tab:nodemap} 가 노드와 식으로 정리하고, 구현 대응(진입점$\cdot$함수 이름)은` |
| 3159 | OUTSIDE_NAVIGATIONAL_REFERENCE_ALLOWED | `구현 식별자 대응은 부록~\ref{sec:appendix-code}(표~\ref{tab:nodecode}).}` |
| 3179 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `\multicolumn{3}{l}{\emph{\quad(N0$'$ 보강: 셀 라벨$\to$탈리튬화 부호 자동 환산 = 식~\eqref{eq:lco-sigmaslot}$\cdot$\S\ref{sec:facade})}}\\` |
| 3230 | OUTSIDE_DIRECT_IMPLEMENTATION_CONTENT | `R1--R3 은 구현 self-test 와 같은 양의 수기 재산출, R4 는 컷 규칙 정의 검사, R5 는 극한 논증,` |
| 3259 | OUTSIDE_GENERIC_IMPLEMENTATION_FRAMING | `R5 & 꼬리 극한의 방향(구판 감사 결함 코드 D-PEAK 의 회귀 가드): 한 칸 감쇠` |
| 791 | OUTSIDE_DIRECT_IMPLEMENTATION_CONTENT | `\bibitem{numverif2026} 본 연구 내부 수치 검증(Derivative A), \texttt{Anode\_Fit\_v1.0.14} 4-전이 흑연 staging 파라미터, 유한차분 vs.\ 가중식 비교 (2026). [내부 자료 — 표시 정밀도 일치 PASS, 본문 \S\r` |

부록을 참조한다는 일반 문장은 탐색성을 위해 허용할 수 있다. 그러나
코드-first 제목, 현재 구현의 parameter state, `dict`, self-test와
내부 code artifact를 물리 근거처럼 쓰는 문장은 최종 이론 본문에서
제거해야 한다.

## 폭 예산의 판정

새 식의
$\sigma_\mathrm{sym}^2=\pi^2w_\mathrm{int}^2/3+
\sigma_\eta^2$는 독립 대칭 convolution의 분산 가법으로 타당하고,
logistic 분포의 $\sigma=\pi w/\sqrt3$, FWHM
$=2\ln(3+2\sqrt2)w$도 맞다.

문제는 같은 $w_j$를 두 역할로 쓴다는 점이다.

1. 식 안에서는 $w_j=n_jRT/F$인 내재 열폭이다.
2. 이어지는 문장에서는 fitted $w_j$가 내재폭과 ensemble 폭을 이미
   함께 흡수하는 관측 유효폭이다.

둘을 동시에 쓰고 $\sigma_\eta$를 다시 더하면 이중계산 가능성이
생긴다. 최종 이론은 $w_\mathrm{int}$, $\sigma_\mathrm{ens}$,
$L_V$, $w_\mathrm{obs}$를 분리하고 observation operator에서
한 번만 합성해야 한다.

## 판정표

| ID | topic | disposition | finding |
|---|---|---|---|
| V1014-36.1-01 | textbook_register | PRESERVE_ASSET_NOT_FINAL_AUTHORITY | The single-site derivation now exposes the grand partition function, internal q(T), effective site free energy, limiting cases, and the Ch1/Ch2 bridge; this is a real pedagogical gain. |
| V1014-36.1-02 | review_depth | PARTIAL | Ch1 adds broadening mechanisms, a variance budget, PSD forward integration, and Gibbs-Thomson exclusion, but Ch2 changes only 18 net lines and no new equation. |
| V1014-36.1-03 | theory_only_boundary | FAIL_REQUIRES_CORRECTION | A dedicated implementation appendix was created, yet rendered title/header/date and body prose still contain code-first framing, current-code state, dict, and self-test language. |
| V1014-36.1-04 | one_way_theory_to_code | PARTIAL | Moving identifier tables and snippets into one appendix is structurally correct, but the main text still explains itself through implementation state rather than only physical logic. |
| V1014-36.1-05 | width_budget | CORRECT_ROLE_SPLIT_REQUIRED | Variance addition and the logistic variance/FWHM identities are mathematically coherent under independent convolution. However w_j is first the intrinsic nRT/F scale and later the fitted effective width that already absorbs intrinsic plus ensemble broadening, so adding sigma_eta can double count. |
| V1014-36.1-06 | scientific_validation | UNVERIFIED | The source contains internal numerical-validation and measurement-grade language but this diff supplies neither external experimental overlays nor uncertainty. |

## 다음 단계

Step 36.2에서 v1.0.14 phase-separation appendix의 regular solution,
spinodal, Cahn--Hilliard, gradient coefficient와 mobility 식을
독립 재유도해 단위·안정성·선형화·경계조건을 검산한다.
