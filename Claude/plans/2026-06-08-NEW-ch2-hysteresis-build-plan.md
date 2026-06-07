# 신규 Chapter 2 (충방전 히스테리시스: 완전 유도 → 피팅 방향 파라미터화) — Ch1 후속절

> 재편(6-08): 전기화학 반응속도론(BV) 장 → **Ch4**("미래 DFN 모듈"). 히스테리시스 → **새 Ch2**.
> ★ **Ch2 = Chapter 1 의 후속절.** Ch1(방전 한 방향) dQ/dV 모델을 충방전 양방향$\cdot$히스테리시스로 잇는다.
> ★ **두 단계 (순서 엄수):**
>  1) **전반부 = 비약 없는 완전한 수식 유도.** 충방전 히스테리시스의 \textbf{확정 수식}을 먼저 구한다 — $\Delta U_j^\hys$ 등은 \emph{현상론적 fitting 파라미터로 posit 하지 않고} 정규용액 $\Omega_j$ 열역학(비단조 $\mu$ → spinodal → metastable branch)에서 \textbf{유도}한다.
>  2) **후반부 = 파라미터화.** 확정 수식을 충방전$\cdot$히스테리시스 \textbf{피팅 및 활용 가능한 방향}으로 파라미터화한다. \textbf{억지 최소화 금지} — 꼭 필요하면 필요한 만큼 파라미터를 둔다.
> 전제: 참 히스테리시스 = 열역학 분기(I→0 잔존), BV/DFN 불필요. Ch1만 기반.

---

## A. 작업 방식 (기존 방식 — 매 절, 묻지 않고 완료까지 연속)

1. 계획서(본 문서) → GO 후 끝까지 자동.
2. **절 단위 루프(품질 granularity)**: 한 절 작성 → 검수(빌드/규율 grep)·Ch1 정합 → 곧바로 다음 절. **챕터 완료까지 멈추지 않음**(절마다 사용자 확인 X, 합리적 기본값으로 진행).
3. 완료 후 빌드 + Codex foreground 적대 검수(MAJOR 0) + auto-commit+push.
4. 통합 문건 규율: 기호규약에 이전 장 언급 X, 인계/recap/전달/결론 절 X. Ch1 식은 쓰이는 자리서 식번호 inline.
5. Ch1만 기반(BV/i₀/R_ct = Ch4), 발명 X, Ch1 라벨 불변, 수식번호 2.x.

## B. 재편·파일 (실행 step 0)

- 현 `graphite_ica_ch2.tex`(BV) → `graphite_ica_ch4.tex`, 제목·번호 Chapter 4·4.x (내용 보존).
- 새 `graphite_ica_ch2.tex` = 충방전 히스테리시스, 백지 신규. Ch1 무수정.

## C. 정체성·목표

- **정체성(Ch1 후속절)**: Ch1 평형 dQ/dV(전이별 logistic $+$ 정규용액 $\Omega_j$)의 충방전 branch 확장을 \textbf{완전 유도}로 닫고, 동역학 분극을 얹은 뒤, 피팅·활용 가능한 방향으로 파라미터화.
- **인계(Ch1만)**: logistic $\xi_{\eq,j}$ (1.11)·$U_j$·$w_j$·$Q_j$, \textbf{정규용액 화학퍼텐셜 $\mu_j(x)=\mu^0+RT\ln[x/(1-x)]+\Omega_j(1-2x)$}(Ch1 §평형 peak)·$\Omega_j$, 전하보존 (1.1)·$V_{n,\OCV}$, dQ/dV (1.4), 지연 $L_{q,j}$ (1.19)·$k_j$·$R_n$ (1.3), 온도계수 $\partial U_j/\partial T$ (1.15).
- **목표**: 확정 수식 → 충/방전 OCV $+$ 0.1C/0.2C$\times$15/23/45℃ 로 피팅·예측 가능한 파라미터화(필요한 만큼).

## D. 내용·구조

> 서사: Ch1 단일방향 dQ/dV 의 연속으로 충/방전 갈림(히스테리시스) → \textbf{전반부: 그 갈림의 확정 수식을 $\Omega_j$ 에서 완전 유도} → \textbf{후반부: 충방전 피팅·활용 방향 파라미터화}.

### 서론·기호
| 절 | 내용 |
|---|---|
| 서론 | Ch1 (방전) dQ/dV 에 이어 충/방전 히스테리시스로 확장. 로드맵: 완전 유도 → 파라미터화 (인계 ledger X) |
| §1 기호와 규약 | 새 기호 표만(branch $b\in\{\dis,\chg\}$, spinodal $x_{s,j}^\pm$, branch 전위 $U_j^b$, gap $\Delta U_j^\hys$, $w_j^b$, 기억 $h_j$, $\Delta V_\obs/\Delta V_\hys/\Delta V_\pol$). 이전 장 언급 0 |

### 전반부 — 완전 유도 (확정 수식, 비약 0)
| 절 | 내용 | Ch1 근거 |
|---|---|---|
| **§2 무엇을 유도할 것인가** | 충/방전 dQ/dV 갈림 관찰 → $\Delta V_\obs=\Delta V_\hys+\Delta V_\pol(+\Delta V_\kin)$, \textbf{$\Delta V_\obs\ne\Delta V_\hys$}. 본 장이 유도할 대상($\Delta V_\hys$=열역학, $\Delta V_\pol$=동역학)을 정의 | $R_n$·지연 |
| **§3 비단조 화학퍼텐셜과 상분리(유도 1)** | 정규용액 $\mu_j(x)$ 에서 $\dd\mu_j/\dd x=RT/[x(1-x)]-2\Omega_j$. $\Omega_j>2RT$ 면 비단조 → spinodal $x_{s,j}^\pm=\tfrac12\pm\tfrac12\sqrt{1-2RT/\Omega_j}$ 유도. 평형 전위 $U_j(x)=U_j^0-\mu_j(x)/(sF)$ 의 비단조성 | Ch1 $\mu_j$·$\Omega_j$ |
| **§4 metastable branch 와 $\Delta U_j^\hys$(유도 2)** | 충(리튬화)/방전(탈리튬화)이 각 metastable branch 를 spinodal 한계까지 따라감 → branch 전위 $U_j^\chg,U_j^\dis$ 와 히스테리시스 gap $\Delta U_j^\hys=U_j(x_{s,j}^-)-U_j(x_{s,j}^+)$(spinodal 기반; 다입자 plateau \cite{dreyer2010}). \textbf{가정(spinodal vs nucleation 한계)을 명시}해 비약 0 | Ch1 $U_j$·$\Omega_j$ |
| **§5 branch 별 평형 dQ/dV** | §4 유도 전위로 각 전이의 branch logistic $\xi_{\eq,j}^b(V;U_j^b,w_j^b)$ → 충/방전 dQ/dV$|^b$. branch 폭 $w_j^b$ 의 $\Omega_j$ 의존도 §3 에서 따라옴 | (1.4)/(1.11) |
| **§6 동역학 분극(율 의존)** | 각 branch 에 Ch1 지연 $L_{q,j}$·$R_n$ → 율·온도 의존 broadening/shift, \textbf{$I\to0$ 소멸}. $\Delta V_\pol$ 확정 → §2 분해 닫힘 | (1.19)/(1.3) |
| **§7 부분 cycle 과 기억** | 완전 충/방전=각 branch; 부분 cycle=branch 간 scanning, $h_j$(return-point memory). \emph{경계 1절} \cite{sethna1993} | 선택적 |
| → | \textbf{여기까지 = 충방전 히스테리시스 확정 수식.} 환원 검산: $\Omega_j\le2RT$($\Delta U^\hys\to0$)에서 Ch1 단일 dQ/dV, $k_j\to\infty$ 분극 소멸 | |

### 후반부 — 피팅·활용 방향 파라미터화 (★, 억지 최소화 X)
| 절 | 내용 |
|---|---|
| **§8 충방전 파라미터화** | §2–§7 확정 수식을 충방전$\cdot$히스테리시스 피팅·활용 가능한 파라미터 집합으로 정리. \textbf{필요한 만큼} — 전이별 $\{U_j,\Omega_j(\to\Delta U_j^\hys,x_s^\pm),w_j,Q_j,\partial U_j/\partial T,\ \text{동역학}\ k_j(\Delta G_{a,j},\chi),R_n\}$ 및 필요 시 branch 의존 항. 어떤 항이 독립이고 어떤 항이 한 양($\Omega_j$)에서 함께 따라오는지 명시(억지로 줄이지 않되, 유도가 묶어 주는 것은 묶음) |
| **§9 데이터→파라미터·예측 방향** | 충/방전 저율 OCV → $\{U_j,\Omega_j(\Delta U^\hys),w_j,Q_j,\partial U/\partial T\}$; 0.1C/0.2C$\times$15/23/45℃ → $\{k_j(\Delta G_a,\chi),R_n\}$. 이 집합으로 임의 율·온도 충방전 dQ/dV 예측. \emph{무엇이 어느 데이터서 닫히는가의 정방향}(상세 식별성·알고리즘은 피팅 장) |

**의도적 배제**: Butler--Volmer·$i_0$·$R_\ct$·flux-force(=Ch4 DFN), Marcus 정식 전개, dQ/dV 지문 표 임의 추가.

## E. Gates (확인 가능)

- **G-derive(전반부 핵심)**: $\Delta U_j^\hys$·spinodal·branch 전위가 \textbf{$\Omega_j$ 에서 비약 없는 유도}로 확정(중간 단계 명시), \emph{현상론 posit 아님}. 가정(spinodal/nucleation 한계) 명시.
- **G-true-hys**: $\Delta U_j^\hys$=$I\to0$ 잔존(열역학)/$\Delta V_\pol$=$I\to0$ 소멸(동역학) 분리, $\Delta V_\obs\ne\Delta V_\hys$.
- **G-ch1-reduction**: $\Omega_j\le2RT$($\Delta U^\hys\to0$)·$k_j\to\infty$ 에서 Ch1 dQ/dV 환원 — 본문 검산.
- **G-param(후반부)**: §8 파라미터 집합 + §9 데이터원 매핑 + 충방전 예측 경로 닫힘. \textbf{억지 최소화 안 함}(필요한 만큼), 유도가 묶는 항만 묶음(근거 명시).
- **G-ch1-only**: 본문 Chapter 1/인계/전달/recap/결론 0, BV/$i_0$/$R_\ct$ 0 (grep).
- **G-build/codex**: 빌드 clean, undefined 0, Codex MAJOR 0(특히 §3·§4 유도 비약·부호·spinodal 대수).
- **G-no-invent**: BV/Marcus/dQ지문 0.

## F. Steps (cumulative; 절 단위 멈춤 없이 연속)

- S0: 파일 재편(현 ch2→ch4 이동·제목 4.x).
- S1: 골격 + §1 기호와규약.
- S2~S7: §2 정의 / §3 비단조 μ·spinodal 유도 / §4 branch·$\Delta U_\hys$ 유도 / §5 branch dQ/dV / §6 동역학 분극 / §7 부분cycle·기억. (전반부 확정 수식)
- S8~S9: §8 파라미터화 / §9 데이터→파라미터·예측. (후반부)
- S10: 서론 + 전체 서사·정합·환원검산 패스.
- S11: 빌드 + Codex until MAJOR 0.
- S12: commit·push + ledger.

## G. Risks
- R1(ΔU_hys 현상론 posit): G-derive — $\Omega_j$ 유도 강제, posit 금지. R2(억지 최소화): G-param — 필요한 만큼 허용, 유도가 묶는 것만 묶음. R3(BV/DFN 유입): G-no-invent. R4(참/분극 혼동): $I\to0$ 분리. R5(절마다 멈춤): 완료까지 연속. R6(Ch1 이탈): branch=Ch1 $\mu_j$·$\Omega_j$ 확장만.

## H. 참고 (예정 인용)
dreyer2010(열역학 히스테리시스·다입자), sethna1993(return-point memory), reynier2004($\partial U/\partial T$). Ch1 refs 정합.

## I. Correction History
- 2026-06-08 v1: 작성(재편·열역학 분기).
- 2026-06-08 v2: 2부 구조(전반 검토/후반 파라미터화) 명문화.
- 2026-06-08 v3: ★ 박사님 정정 반영 — (1) **억지 최소화 폐기**(필요한 만큼 파라미터), (2) **$\Delta U_\hys$ 는 fitting posit 아니라 $\Omega_j$ spinodal 에서 비약 없는 완전 유도** 후 확정 수식 먼저 → 그 다음 파라미터화. 전반부 §3·§4 를 \emph{유도 절}로 승격, §8 "최소"→"필요한 만큼", G-derive 신설. GO 후 S0부터 절 단위 멈춤 없이.
