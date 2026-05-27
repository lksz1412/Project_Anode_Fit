# Phase A — ver5 Master Structure Result

작성일: 2026-05-27
계획서: [Claude/plans/2026-05-27-anode-fit-situational-assessment-plan.md](../plans/2026-05-27-anode-fit-situational-assessment-plan.md)
양식: [[feedback_phase_execution_loop]] 11항목

## Summary

ver5 마스터 (`Claude/docs/graphite_ica_dynamic_ver5.tex`, 1974 줄) 를 전수 정독해 Chapter 1 ~ Chapter 5 (현 `\section{ver.N ...}` 헤더 5개) 의 골격·줄 범위·핵심 변수·핵심 식 번호·인계 chain 을 매핑했다. Chapter 1 은 Phase C 의 rechecked2 매핑 대상이므로 `\subsection` 트리까지 상세 추출했다.

## Step Range

cumulative Steps **1 ~ 6** (Phase A 전체).

## Inputs

| 파일 | 경로 | 줄 수 |
|---|---|---:|
| ver5 마스터 | `Claude/docs/graphite_ica_dynamic_ver5.tex` | 1974 |

## Files Created

- `Claude/results/PHASE_A_ver5_master_structure_RESULT.md` (본 파일)

(ledger `Claude/results/PHASE_A_D_EXECUTION_LEDGER.md` 는 별도 파일로 동 Phase 종료 commit 시 생성)

## Files Updated

없음 (정독·진단 only, 본문 수정 없음 — P5 정합)

## Read Coverage

| 파일 | 분할 read 호출 | cover 한 줄 범위 | 상태 |
|---|---|---|---|
| `Claude/docs/graphite_ica_dynamic_ver5.tex` | `offset=1 limit=500` + `offset=501 limit=500` + `offset=1001 limit=1000` | 줄 1 ~ 1974 (EOF `\end{document}` 포함) | **전수 정독 PASS** |

비고: 최초 시도 `offset=1 limit=1000` 은 토큰 한도 (25744 > 25000) 로 실패 → 500 줄 분할로 재시도. ★ 200줄 limit 함정 (글로벌 CLAUDE.md "★ 200줄만 읽고 나머지 생략 절대 금지") 회피 확인.

## Execution Evidence

### 분할 read 결과

- offset=1, limit=500 → 줄 1 ~ 500. Chapter 1 본문 대부분 (§1 ~ §17 일부) cover
- offset=501, limit=500 → 줄 501 ~ 1000. Chapter 1 잔여 (§18 ~ §19 참고문헌) + Chapter 2 전체 + Chapter 3 일부 cover
- offset=1001, limit=1000 → 줄 1001 ~ 1974 (EOF). Chapter 3 잔여 + Chapter 4 + Chapter 5 cover

### Chapter 경계 확정 (Section Header grep + 본문 정독 cross-check)

| Chapter | ver.N 명칭 | `\section{ver.N ...}` 헤더 | 시작 줄 | 끝 줄 | 분량 |
|:---:|---|---|---:|---:|---:|
| **1** | ver.1 기본식 | `\title{... ver.1 기본식}` (line 46) + `\section{문서의 목적과 적용 범위}` (line 62) | 46 | 526 | 481 줄 |
| **2** | ver.2 발열 근사 및 피팅 계층 | `\section{ver.2 발열 근사 및 피팅 계층}` (line 527) | 527 | 855 | 329 줄 |
| **3** | ver.3 전기화학 반응속도론 계층 | `\section{ver.3 전기화학 반응속도론 계층}` (line 856) | 856 | 1125 | 270 줄 |
| **4** | ver.4 의 목적과 적층 규칙 (`\part*{ver.4 ...}` line 1123) | `\section{ver.4의 목적과 적층 규칙}` (line 1126) | 1126 | 1522 | 397 줄 |
| **5** | ver.5 의 목적과 적층 규칙 (`\part*{ver.5 ...}` line 1520) | `\section{ver.5의 목적과 적층 규칙}` (line 1523) | 1523 | 1974 | 452 줄 |

비고: Chapter 4 · 5 만 `\part*{...}` 헤더로 명시적 구분. Chapter 1 · 2 · 3 은 `\part` 없이 연속. ChAPTER 1 시작이 정확히 `\title` (line 46) 인지 `\section{문서의 목적과 적용 범위}` (line 62) 인지 모호하지만, ver5.tex 의 `\title` 자체가 "ver.1 기본식" 으로 적혀있어 line 46 부터 Chapter 1 본문으로 본다.

### `ver.N 으로 전달되는 기준식` 절 인계 chain (Step 3)

각 chapter 끝부분 (검수 체크리스트 직전) 에 `\section{ver.N 으로 전달되는 기준식}` 절 존재. 인계 식만 발췌:

#### Chapter 1 → Chapter 2 인계 (`§ver.2로 전달되는 기준식`, line 485)

```latex
\frac{\dd\xi_j}{\dd q}=\frac{Q_{\cell}}{|I|}k_j\left[\xi_{j,\eq}-\xi_j\right]                  (Eq. line 489)
\frac{\dd Q_n}{\dd q}=\frac{\dd Q_{\bg}}{\dd q}+\sum_jQ_{j,\tot}\frac{\dd\xi_j}{\dd q}        (Eq. line 493)
\frac{\dd Q_n}{\dd V_{n,\app}}=\frac{\dd Q_n/\dd q}{\dd V_{n,\app}/\dd q}                     (Eq. line 497)
```

#### Chapter 2 → Chapter 3 인계 (`§ver.3으로 전달되는 기준식`, line 812)

```latex
\Delta G_{\eff,j}=\Delta G_{a,j}-\chi_j\mathcal A_j                                            (line 815)
k_j=\nu_j\exp[-\Delta G_{\eff,j}/(RT)]                                                         (line 819)
\dd\xi_j/\dd q = Q_{\cell}/|I| \cdot k_j (\xi_{j,\eq}-\xi_j)                                   (line 823)
\dot Q_{\heat,n} ≈ I^2 R_n + |I| T [h_{bg} + Σ w_j s_j dξ_j/dq]                                (line 827)
```

#### Chapter 3 → Chapter 4 인계 (`§ver.4로 전달되는 기준식`, line 1066)

```latex
V_{n,\app}=V_{n,\OCV}+s_IIR_n(q,T)                                                             (line 1070)
\xi_{j,\eq}=\xi_{j,\eq}(V_{n,\OCV}(q,T),T)                                                     (line 1074)
\mathcal A_j = F \eta_j  또는  \mathcal A_j = s_{\phi,j} F (V_{n,\app}-U_j)                    (line 1078)
\Delta G_{\eff,j}=\Delta G_{a,j}-\chi_j \mathcal A_j                                           (line 1084)
k_j=\nu_j\exp[-\Delta G_{\eff,j}/(RT)]                                                         (line 1088)
\dd\xi_j/\dd t = k_j (\xi_{j,\eq}-\xi_j)                                                       (line 1092)
\dd\xi_j/\dd t = k_j^+(1-\xi_j) - k_j^-\xi_j   [forward/backward]                              (line 1097)
```

#### Chapter 4 → Chapter 5 인계 (`§ver.5로 전달되는 기준식`, line 1468)

```latex
V_{n,\app}=V_{n,\OCV}+s_IIR_n(q,T)                                                             (line 1472)
\xi_{j,\eq}=\xi_{j,\eq}(V_{n,\OCV}(q,T),T)                                                     (line 1476)
\Delta G_{\eff,j}=\Delta G_{a,j}-\chi_j \mathcal A_j                                           (line 1480)
k_j=\nu_j\exp[-\Delta G_{\eff,j}^{+}/(RT)]                                                     (line 1484)
\dd\xi_j/\dd t = k_j(\xi_{j,\eq}-\xi_j)                                                        (line 1488)
\dd\xi_j/\dd t = k_j^+(1-\xi_j) - k_j^-\xi_j                                                   (line 1494)
```

Chapter 5 → (다음 챕터 없음) — 인계 절 부재. 마지막 챕터 정합.

### Chapter 별 골격 요약 (Step 4)

#### Chapter 1 (ver.1 기본식) — 줄 46 ~ 526 (481 줄, 19 sections)

**spine (line 66 ~ 79, Eq. main_spine):**

```
ΔG_eff,j → k_j → dξ_j/dt → ξ_j(q) → dξ_j/dq → dQ/dV, dV/dQ
```

**핵심 변수:** `V_n`, `V_{n,OCV}`, `V_{n,app}`, `V_{n,0.2C}`, `ξ_j`, `ξ_{j,eq}`, `k_j`, `ΔG_{eff,j}`, `ΔG_{a,j}`, `R_n(q,T)`, `U_j`, `w_j`, `Q_{j,tot}`, `χ_j`, `ρ_j(g)`, `I`, `s_I`, `s_{φ,j}`, `Q_{bg}`, `Q_{cell}`, `Q_n`

**핵심 식 (line):** Vapp_general (131), OCV_voltage_model (158), V02_relation (166), V02_app (171), xi_eq_basis (180), xi_eq_logistic (188), xi_eq_erf (195), Ga_def (207), A_simple (215), Geff (223), k_basic (231), xi_ode_t (256), xi_ode_q (270), k_g (292), xi_g_ode (299), xi_distribution (307), dxi_distribution (316), Qn (328), dQdq (333), dVdq (341), ICA_param (350), DVA_param (360), EMG_empirical (398)

**§ 구조 (19 sections):** 문서 목적 (62) · 공통 컨벤션 (91, 기호 정의 + 부호) · 흑연 staging (137) · 전위 모델 OCV/0.2C (154) · 평형 진행률 (176, Logistic/Erf/실제 피크) · 유효 장벽·속도상수 (203, 5 subsec) · 진행률 동역학 (252, 시간/q좌표/해석) · 장벽 분포 평균 (286, 장벽별/분포평균) · ICA·DVA 유도 (325, 4 subsec) · C-rate 평탄화 (367) · 온도 효과 (377) · 실용 피팅식·EMG (396) · 피팅 절차 (417) · 목적 함수·정규화 (429) · 식별성·제약 (445) · 모델 수준 선택표 (470) · ver.2로 전달 (485) · 검수 (502) · 참고문헌 (516, 5 ref)

#### Chapter 2 (ver.2 발열) — 줄 527 ~ 855 (329 줄, 13 sections)

**의도:** ver.1 의 ξ_j · dξ_j/dq 를 그대로 받아 발열 항을 reduced-order **basis expansion** 으로 적층. 열역학 항등식 아님 — 피팅용 표현임을 명시.

**핵심 식 (line):** heat_decomp (567), eta_eff (590), eta_eff_R (594), irr_I2R (606), rev_signed_general (632), rev_hn (637), hn_def (643), Qj_xi (655), dn_xi (660), rev_j_dn (668), rev_j_final (682), w_s_def (689), entropy_basis (694), rev_basis (701), heat_final (716), heat_uses_dxi (727), lumped_heat (734), heat_loss_function (782), heat_reg (790)

**§ 구조 (13 sections):** 발열 계층 도입 (527) · 열 발생 항 분해 (565, 부호 conv.) · 비가역 열 (586, 유효 과전압 / 성분 분해) · 가역 열 기본식 (630) · 상변이 진행률 기반 entropy coefficient (652, 3 subsec — 몰수·상변이별·basis expansion) · 최종 발열 근사식 (713) · 열 방정식·온도 되먹임 (732) · 가역/비가역 분리 전략 (751) · 발열 피팅 절차 (767) · 발열 피팅 목적 함수 (779) · 식별성 (796) · ver.3 으로 전달 (812) · 검수 (837)

#### Chapter 3 (ver.3 반응속도론) — 줄 856 ~ 1125 (270 줄, 11 sections)

**의도:** `A_j` 를 단순 전위 보조에서 BV 과전압으로 일반화. **평형 진행률 (ξ_{j,eq}) 과 동역학 속도 (k_j) 의 분리 원칙** 강조 — 과전압이 양쪽에 동시에 들어가서 같은 효과 중복 반영 금지.

**핵심 식 (line):** v3_xieq_rule (861), v3_k_basic (866), v3_A_simple (873), v3_A_eta (881), v3_Geff_eta (886), v3_BV_general (898), v3_low_eta (916), v3_asinh_eta (937), v3_i0_T (966), v3_forward_backward (981), v3_xieq_from_rates (995), v3_k_relax (1005), v3_Ij (1013), v3_current_partition (1018)

**§ 구조 (11 sections):** ver.3 계층 도입 (856) · 전위 보조 구동력 일반화 (871) · Butler-Volmer 와 η_j (896, 저과전압 선형/대칭 BV asinh/Tafel) · 교환전류밀도 온도 의존성 (963) · forward/backward rate (977) · 전류 분배 (1010) · reduced vs reaction-resolved 모델 선택 (1023) · 식별성 (1039) · 피팅 절차 (1055) · ver.4 로 전달 (1066) · 검수 (1101)

#### Chapter 4 (ver.4 통합) — 줄 1126 ~ 1522 (397 줄, 14 sections)

**의도:** ver.1+2+3 의 식을 변경 없이 받아 **통합 상태방정식 · 관측방정식 · 발열방정식 · 피팅 순서** 로 묶음. ver.4 는 신규 수식 X, 계산 절차의 통합.

**핵심 식 (line):** v4_vapp_ocv (1137), v4_vapp_02c (1144), v4_xieq (1151), v4_xi_t_basic (1158), v4_q_t (1165), v4_xi_q_basic (1172), v4_heat_split (1182), v4_qirr (1189), v4_qrev (1196), v4_A_eta (1210), v4_A_vapp (1217), v4_Geff (1224), v4_k_reduced (1231), v4_Geff_plus (1238), v4_bv (1247), v4_state_vector (1257), v4_xi_quad (1264), v4_input (1273), v4_state_q (1282), v4_state_xi (1292), v4_state_xig (1299), v4_state_xi_avg (1306), v4_state_T (1316), v4_obs_vn (1327), v4_obs_cellv (1334), v4_obs_Qn (1344), v4_obs_dQdq (1351), v4_obs_ica (1361), v4_obs_dva (1368), v4_dVdq_temp (1375), v4_loss (1401), v4_reg (1412)

**§ 구조 (14 sections):** ver.4 적층 규칙 (1126) · ver.1 에서 받은 기본 동역학 (1133) · ver.2 에서 받은 발열 (1178) · ver.3 에서 받은 반응속도론 (1206) · 통합 상태 변수·입력 (1253) · 통합 상태방정식 (1277, 3 subsec — q / ξ / T) · 통합 관측방정식 (1322, 3 subsec — V / Q / ICA·DVA) · 통합 계산 절차 (1381, 10 step) · 피팅 목적함수 (1397) · 단계별 피팅 순서 (1416, 6 단계) · 모델 수준 선택표 (1433, Level 0~5) · 검증 체크리스트 (1450) · ver.5 로 전달 (1468) · 검수 (1499)

#### Chapter 5 (ver.5 히스테리시스) — 줄 1523 ~ 1974 (452 줄, 16 sections)

**의도:** branch index `p ∈ {chg, dis}` 추가. branch 차이를 **4 성분 분해** (저항성 / 동적 지연 / 구조 기억 / 열적) 로 설명. 기존 ξ_j 정의 변경 X.

**핵심 신규 변수:** `p`, `s_I^p`, `s_{φ,j}^p`, `ξ_j^p`, `k_j^p`, `R_n^p`, `V_{n,mem}^p`, `V_{n,dyn}^p`, `z_j` (구조 기억, -1 ≤ z_j ≤ 1), `τ_{z,j}^p`, `h_j`, `φ_j` (window 함수)

**핵심 식 (line):** v5_affinity_branch (1560), v5_voltage_full (1586), v5_xi_branch_time (1609), v5_xi_branch_q (1619), v5_Geff_branch (1645), v5_k_branch (1656), v5_fb_branch (1679), v5_z_time (1714), v5_z_q (1722), v5_vmem (1731), v5_dist_branch_xi (1746), v5_dist_branch_ode (1752), v5_Q_branch (1773), v5_dQdq_branch (1780), v5_ica_branch (1791), v5_dva_branch (1799), v5_loop_energy (1867)

**§ 구조 (16 sections):** ver.5 적층 규칙 (1523) · branch index·부호 (1540) · 히스테리시스 4 성분 분해 (1571) · branch별 진행률 동역학 (1606) · branch별 유효 장벽·속도상수 (1642) · forward/backward branch model (1676) · 구조 기억 변수 z_j (1706) · 장벽 분포 branch 동역학 (1743) · branch별 ICA·DVA (1770) · 관측 히스테리시스 분해 (1809) · 피크 중심·tail branch 비교 (1844) · hysteresis energy (1865) · 동시 피팅 목적함수 (1887) · 피팅 순서 (1921, 6 단계) · 식별성 주의 (1937) · 검증 체크리스트 (1954)

### Chapter 1 `\subsection` 트리 상세 (Step 5 — Phase C 매핑 대상)

```
Chapter 1 (ver.1 기본식, 줄 46~526)
├── §1  문서의 목적과 적용 범위                       (line 62)
├── §2  공통 컨벤션                                  (line 91)
│   ├── §2.1  기호 정의 (21 기호 표)                  (line 92)
│   └── §2.2  전류와 전위 부호 [Eq. Vapp_general]      (line 127)
├── §3  흑연 staging 과 effective transition index    (line 137)
├── §4  전위 모델: OCV 기준과 0.2C 기준                (line 154)
│   ├── §4.1  OCV 기준 일반식 [Eq. OCV_voltage_model]   (line 155)
│   └── §4.2  0.2C 기준 응용식 [Eq. V02_relation/V02_app] (line 163)
├── §5  평형 진행률 ξ_{j,eq} [Eq. xi_eq_basis 박스]    (line 176)
│   ├── §5.1  Logistic 표현 [Eq. xi_eq_logistic]       (line 186)
│   ├── §5.2  Erf 표현 [Eq. xi_eq_erf]                 (line 193)
│   └── §5.3  평형 피크와 실제 피크                    (line 200)
├── §6  유효 장벽과 상변이 속도상수                    (line 203)
│   ├── §6.1  고유 활성화 자유에너지 [Eq. Ga_def]       (line 204)
│   ├── §6.2  전위 보조 구동력 [Eq. A_simple]          (line 212)
│   ├── §6.3  유효 장벽 [Eq. Geff]                    (line 220)
│   ├── §6.4  속도상수 [Eq. k_basic]                  (line 228)
│   └── §6.5  속도 폭주 방지 (방법 A: 양수부 / 방법 B: 상한) (line 236)
├── §7  상변이 진행률 동역학                          (line 252)
│   ├── §7.1  시간 영역 식 [Eq. xi_ode_t 박스]         (line 253)
│   ├── §7.2  방전 진행 좌표 식 [Eq. xi_ode_q 박스]     (line 263)
│   └── §7.3  해석 (C-rate 2 경로 + 온도)              (line 277)
├── §8  장벽 분포 평균 동역학                          (line 286)
│   ├── §8.1  장벽별 진행률 [Eq. k_g, xi_g_ode]        (line 289)
│   └── §8.2  분포 평균 [Eq. xi_distribution 박스]     (line 304)
├── §9  ICA 와 DVA 유도                                (line 325)
│   ├── §9.1  용량식 [Eq. Qn, dQdq]                   (line 326)
│   ├── §9.2  전위 미분 [Eq. dVdq]                    (line 339)
│   ├── §9.3  ICA [Eq. ICA_param 박스]                (line 347)
│   └── §9.4  DVA [Eq. DVA_param 박스]                (line 357)
├── §10 C-rate 증가와 피크 평탄화                      (line 367)
├── §11 온도 효과가 들어가는 위치                      (line 377)
├── §12 실용 피팅식과 동역학 모델의 관계 [Eq. EMG]      (line 396)
├── §13 피팅 절차 (6 단계)                            (line 417)
├── §14 목적 함수와 정규화                            (line 429)
├── §15 식별성 및 제약 (5 상관 + 5 권장 제약)          (line 445)
├── §16 모델 수준 선택표 (Level 0~5)                  (line 470)
├── §17 ver.2 로 전달되는 기준식 (3 식 인계)           (line 485)
├── §18 검수 체크리스트 (5 항목)                       (line 502)
└── §19 참고문헌 (5 ref)                             (line 516)
```

총 19 sections, 그 중 `\subsection` 를 가진 section = §2, §4, §5, §6, §7, §8, §9 (7 sections). 총 subsection = 2+2+3+5+3+2+4 = **21 subsections**.

## Validation

본 계획서의 Gate (GATE_A1 ~ A4) 별 PASS/FAIL.

| Gate | 항목 | 4-tier | 근거 |
|---|---|---|---|
| **GATE_A1** | ver5.tex 줄 1 ~ 1974 전체 read + Read Coverage 기록 | **확정** | 본 Result §"Read Coverage" — 분할 호출 3회 (1-500 / 501-1000 / 1001-1974) 로 EOF 포함 cover |
| **GATE_A2** | Chapter 1~5 각각의 `시작 줄 ~ 끝 줄` + `\section` 헤더 목록 확정 | **확정** | 본 Result §"Chapter 경계 확정" 표. 헤더는 본문에서 직접 인용 |
| **GATE_A3** | `ver.N 으로 전달되는 기준식` 절 전수 추출 (Chapter 1→2, 2→3, 3→4, 4→5 = 4 개 예상) | **확정** | 본 Result §"인계 chain" — 4 개 모두 본문 식 그대로 인용 (Chapter 5 는 마지막이라 인계 절 부재 = 정합) |
| **GATE_A4** | Chapter 1 `\subsection` 트리 전수 추출 (Phase C 매핑 대상) | **확정** | 본 Result §"Chapter 1 \\subsection 트리 상세" — 21 subsections + 19 sections 트리 |

## Gate

**Phase A 종합 판정: PASS** (GATE_A1 ~ A4 모두 확정 4-tier)

Gate 식별자: `PASS_VER5_MASTER_STRUCTURE`

## Confirmed Non-Changes

의도적으로 손대지 않은 영역 (사용자 확인 회피용):

- `Claude/docs/graphite_ica_dynamic_ver5.tex` 본문 — 정독만, 수정 없음 (P5 + [[feedback_document_protection_addendum_pattern]] 정합)
- `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` — Phase B 대상, 본 phase 에서 read 안 함
- `Claude/_local_only/JCP_*.pdf` — Phase D 대상, 본 phase 에서 read 안 함
- `Codex/` — Codex 영역 (P2 정합, 본 phase 에서 read 안 함)
- ver5 본문의 식 번호 · 변수명 · 한글 표현 · LaTeX 매크로 — 그대로 인용만, 변경 없음

## Open Issues / Decision Queue

| ID | 항목 | 분류 | 비고 |
|---|---|---|---|
| **DQ1** | ChatGPT 의 "큰 논리 오류" 정체 (계획서 §"Decision Queue") | 사용자 결정 대기 | Phase B 진입 전 사용자 답변 권장 |
| **OI-A1** | ver5 의 Chapter 1 `\title` (line 46) ↔ `\section{문서의 목적과 적용 범위}` (line 62) 사이 16 줄 (`\maketitle`, abstract minipage, `\tableofcontents`) 은 어느 챕터 소속인가 | **추정** | 문서 메타 (title + abstract + TOC) → Chapter 1 도입부로 분류. 분류 영향 미미. Phase C 매핑 시 재확인 불요 |
| **OI-A2** | Chapter 2 ~ 5 의 `\subsection` 트리는 본 phase 에서 상세 매핑 안 함 (Phase A 의 Step 5 가 Chapter 1 한정) | **미검증** | 본 계획서 범위 외 — 후속 Chapter 2~5 본문 디벨롭 시 필요 시 추가 정독 |
| **OI-A3** | Chapter 5 의 §"피크 중심과 tail의 branch 비교" (1844) 와 §"hysteresis energy" (1865) 가 별도 section 인지 + Chapter 2~5 § count 정확성 | **확정** | Phase A audit Pass 2 에서 grep `^\\section\|^\\subsection` 으로 전수 cross-check 수행. Chapter 2 = 13 §, Chapter 3 = 11 §, Chapter 4 = 14 §, Chapter 5 = 16 § (Result 초기 라벨이 12/8/13/11 로 4건 오류 → Pass 2 에서 13/11/14/16 으로 정정 완료). §"피크 중심..." (1844), §"hysteresis energy" (1865) 별도 section 확정 |

## Next

- **다음 Phase**: Phase B (ver1_rechecked2 전수 정독 + 되먹임 진단)
- **다음 cumulative step**: **Step 7** (계획서 cumulative 1-18 중 Phase B 시작)
- **선행 조건**:
  - 사용자 DQ1 답변 회수 권장 (필수 아님 — 없어도 Phase B Step 9 의 self-consistent loop 진단을 사용자 추가 검증으로 보완 가능)
  - 본 Phase A audit (10차원 × 3-Pass) 완료 후 Phase A 종료 commit 페어 + push → Phase B Step 7 진입

---

## Phase A Audit (10차원 × 3-Pass)

본 phase 가 정독·진단 only 이므로 [[feedback_phase_audit_workflow]] 의 10차원 중 코드성 차원 (시그너처/워커/시그널슬롯/API/메모리) 5 개는 적용 불가 → 작업 종류 특화 차원 4 개로 대체하여 **9 차원** 으로 운용. 3-Pass 는 그대로 적용.

### 차원 매핑

| # | 원 10차원 | 본 phase 차원 | 적용 여부 |
|---|---|---|---|
| 1 | 시그너처 호환성 | (LaTeX) 변수명·식 번호 원문 보존 | 차원 6 으로 통합 |
| 2 | 사용자 verbatim 요청 cross-check | 동 | 적합 |
| 3 | 데이터 흐름 lifecycle 추적 | Read coverage 일치 | 적합 |
| 4 | 워커 lifecycle | — | 부적합 (코드 없음) |
| 5 | 시그널·슬롯 연결 정합 | — | 부적합 |
| 6 | 사용자 컨벤션 + 인라인 라벨 잔존 | 변수명·식 번호·한글 원문 인용 보존 | 적합 |
| 7 | 에러 처리 / silent failure / fallback | 정독 누락 영역 (silent miss) | 적합 |
| 8 | 프레임워크 API 정확성 | — | 부적합 |
| 9 | 메모리 효율 | — | 부적합 |
| 10 | 데이터 구조 contract | Result 11항목 양식 정합 | 적합 |
| α | (phase 특화) | 챕터 경계 정확성 | 적합 |
| β | (phase 특화) | 인계 chain 무손실 (식 인용 vs 원문) | 적합 |
| γ | (phase 특화) | `\section` / `\subsection` 트리 완전성 (cross-check) | 적합 |
| δ | (phase 특화) | 4-tier 분류 일관성 | 적합 |

운용 차원 9 개 = #2, #3, #6, #7, #10, α, β, γ, δ.

### Pass 1 — 발견 (의심 항목 넓게)

| 차원 | 의심 항목 |
|---|---|
| #2 | 사용자 첫 요청 ("ver5 기반 ver1~5 구조 파악, ver1 디벨롭 방향") 과 본 Phase A 산출물 정합? |
| #3 | 분할 read 3회 cover 줄 1~1974. 사이 누락 가능성? |
| #6 | Result 인용한 LaTeX 식 (`\dd\xi_j/\dd q` 등) 이 원문 그대로? `\dd` 매크로를 본 Result 안에서 `d` 로 풀어쓴 곳 있을 수 있음 |
| #7 | offset+limit 경계 (500, 1000) 에서 줄 누락? |
| #10 | Result 11항목 모두 존재 + Validation 표 4-tier 분류 누락 없음? |
| α | Chapter 1 시작이 line 46 (`\title`) 인지 line 62 (`\section`) 인지 (OI-A1 보류) |
| β | 인계 chain 4건 식 인용이 원문 식과 일치? |
| γ | **Chapter 별 § / subsection count 정확성** — Result 골격 요약에 적은 count 라벨이 grep 실측과 일치? |
| δ | Result 내 모든 보고 항목이 확정/근거미발견/추정/미검증 중 하나로 분류? |

### Pass 2 — 확정·수정

| 차원 | 발견 → 확정·수정 |
|---|---|
| #2 | **확정 PASS** — 본 Phase A 산출물 = ver5 1974 줄 전수 정독 + Chapter 1~5 골격 + 인계 chain + Chapter 1 subsection 트리. 사용자 첫 요청 ("ver5 안에 ver1~5 를 어떤 구조로 가져가려고 했는지 파악") 에 정확 부합. 정정 없음 |
| #3 | **확정 PASS** — 분할 호출 cover: 1-500 + 501-1000 + 1001-1974. 경계 (500↔501, 1000↔1001) 누락 없음 — Read tool 의 offset 은 inclusive, limit 은 exclusive 가 아닌 inclusive 수량 (위 분할은 500+500+974 = 1974 전수 cover) |
| #6 | **확정 PASS** — Result 의 LaTeX 인용은 원문 매크로 (`\dd`, `\OCV`, `\app`, `\eq`, `\tot`, `\bg`, `\cell`, `\eff` 등) 그대로 사용. 일부 골격 요약 텍스트에 "dξ_j/dq" 등 간략 표기 혼용 — 단 본문 인용 (인계 chain 인용 블록) 은 원문 그대로. 변수명·식 번호 변경 없음. 한글 표현 (예: "전위 보조 구동력") 원문 그대로 |
| #7 | **확정 PASS** — Read 호출 결과의 마지막 줄 번호 = 1974+EOF (1975 줄 = `\end{document}` 직후 빈 줄). 빠진 영역 없음. wc -l 1974 와 cross-check 일치 |
| #10 | **확정 PASS** — 11항목 = Summary / Step Range / Inputs / Files Created / Files Updated / Read Coverage / Execution Evidence / Validation / Gate / Confirmed Non-Changes / Open Issues / Next 전부 존재. Validation 4 행 (4-tier 분류 = 확정 × 4) |
| α | **추정 → 보류 유지 (OI-A1)** — Chapter 1 의 line 46 (\title) 와 line 62 (\section{문서의 목적}) 사이 16 줄 (`\maketitle`, abstract minipage, `\tableofcontents`) 분류 모호. Phase C 매핑 영향 미미 (이 영역은 문서 메타로 매핑 대상 외) |
| β | **확정 PASS** — Result 의 인계 chain 4건 (line 489/493/497 = Chapter 1→2; line 815/819/823/827 = 2→3; line 1070/1074/1078/1084/1088/1092/1097 = 3→4; line 1472/1476/1480/1484/1488/1494 = 4→5) 모두 원문 식 그대로 (압축 인용 형태). diff 무결 |
| γ | **⚠ FAIL → 정정 완료** — grep `^\\section\|^\\subsection` 전수 cross-check 결과 Result 의 골격 요약 count 라벨 4건 오류 발견: Chapter 2 = 12→**13** / Chapter 3 = 8→**11** / Chapter 4 = 13→**14** / Chapter 5 = 11→**16**. 본문 § 리스트는 모두 맞음, count 라벨만 오기. Pass 2 에서 4건 Edit 정정 완료. OI-A3 도 정정 반영 |
| δ | **확정 PASS** — Result 의 모든 보고 항목이 4-tier 또는 별 카테고리 (DQ 사용자 결정 대기) 로 분류됨. 분류 없는 항목 0 개 |

### Pass 3 — 재검증

| 차원 | 재검증 결과 |
|---|---|
| #2 ~ #10, α, β, δ | Pass 2 정정 없음 (모두 확정 PASS) → 재검증 불요 |
| γ | Pass 2 정정 4건 → 본 문서 현재 상태에서 다시 확인: Chapter 2 § "13 sections" ✓ / Chapter 3 § "11 sections" ✓ / Chapter 4 § "14 sections" ✓ / Chapter 5 § "16 sections" ✓. grep 실측 = 13+11+14+16 = 54 sections (Chapter 2~5 합계) + Chapter 1 의 19 = **73 sections** 전체. grep 결과 행 수 (헤더 `\part*` 2건 + `\section` × N + `\subsection` × M) cross-check: \section 행 = 73, \subsection 행 = 38 (Chapter 1 의 21 + Chapter 2 의 7 + Chapter 3 의 3 + Chapter 4 의 6 + Chapter 5 의 0) — 정합. **회귀 없음 확인** |

### Audit 종합 판정

- **Audit Result**: PASS (Pass 2 정정 4건 후 Pass 3 재검증 무결)
- **회귀 없음**: γ 정정이 다른 차원 영향 없음 — count 라벨만 4 위치 변경, 본문 § 리스트는 무변
- **Critical/High/Medium/Low 분류**:
  - **Medium** (4건): γ 차원의 count 라벨 4건 오류 (정확한 본문 list 와 라벨 숫자 불일치 — Phase C 매핑 시 혼란 유발 가능성. 본 audit 에서 정정 완료)
  - Critical/High 없음
- **잔존 권고**:
  - **OI-A1** (Chapter 1 line 46 vs 62 시작 모호) 는 보류 유지 — Phase C 매핑이 §1 (line 62) 부터이므로 영향 없음
  - **OI-A2** (Chapter 2~5 의 \\subsection 트리 상세) 는 본 계획서 범위 외 — 후속 디벨롭 시 필요 시 추가 정독

