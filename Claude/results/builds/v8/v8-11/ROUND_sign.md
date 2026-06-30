# ROUND_sign — v8-11 검수 (부호 8항 무결 + Phase6 폴리시 4건 무회귀)

검수자: 검수 sub (리뷰 전용, 수정·커밋 없음)
대상: `v8-11/v8-11.tex` (1210줄 전문 정독)
기준: `v7-00_spine/Anode_Fit_v11_final.py` (707줄 정독), `v8-00_spine/KNOWN_DEFECTS.md`
검수 청크: (a) v8-10↔v8-11 라인 diff (폴리시 격리 증거), (b) 식별 식 청크 8종 1:1 코드 대조, (c) 부호 8항 라인 청크, (d) 폴리시 4건 SymPy/손계산 재검산.

---

## A. 폴리시 격리 증거 (무회귀의 1차 근거)

`diff v8-10.tex v8-11.tex` = 정확히 5 hunk. 식 본체·boxed 결과·부호 진술 0건 변경:

| hunk | 위치 | 종류 | 판정 |
|---|---|---|---|
| 헤더 주석 | L2–6 | 메타데이터 추가 | 무해 |
| P1 | L462 (eq:Veq (a) 출발) | 다리 문장 **추가** (eq:eqcond 참조) | 가시화만 |
| P3 | L578 (eq:weff 유도) | "($s$ 부호 양변 공통이라 상쇄)" **삽입** | 명시만 |
| P4 | L804 (eq:Acut) | "$z_\mathrm{cut}$ 는 미분 5% 컷의 선택값" **삽입** | 명시만 |
| P2 | L930 (fig:relaxode 캡션) | "내부 텍스트 ASCII" 작가메모 제거 → 논증 포인터로 교체 | 정리만 |

→ 모든 변경이 국소 첨가/문구 정리. **수식·박스·부호·코드 정합 라인은 1바이트도 안 바뀜.** 폴리시가 부호/유도를 깰 표면적이 구조적으로 없음.

---

## B. 부호 8항 (S1–S8) 전건 v11 1:1 재대조

기준 명제: 방전 $V\uparrow\Rightarrow$ 탈리튬화$\uparrow$, 충전 $dQ/dV$ = 방전 거울(양수).

| # | 진술 (tex) | 코드 정본 (py) | 판정 |
|---|---|---|---|
| S1 | $U_j=(-\Delta H+T\Delta S)/F$, $\Delta G=-sFU$ (eq:Uj·eqcond) | `func_U_j` L69 `(-dH_rxn+T*dS_rxn)/F` | **PASS** — 발열 $\Delta H<0\Rightarrow -\Delta H>0$ 중심↑ 일치 |
| S2 | $\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$, 방전 $V\uparrow\Rightarrow\xi\uparrow$ (eq:xieq) | `func_ksi_eq` L86–87 `z=s*(V_n-U)/w` | **PASS** |
| S3 | $d\xi/dV=\sigma_d\xi(1-\xi)/w$, peak $=|\cdot|\ge0$ 방향불변 (eq:eqpeak) | L370/L468 `ksi_eq*(1-ksi_eq)/w` | **PASS** — $\sigma_d$ 미분 1회 들어오나 모양은 절댓값 양수 |
| S4 | $\Delta U_\hys\ge0$, $\Omega\le2RT\to0$, 분기 $\pm\tfrac12\sigma_d$ (eq:dUhys·Ubranch) | `func_dU_hys` L123–130, `func_U_branch` L138 `+0.5*sigma_d*h_eta*gamma*dU` | **PASS** — 방전 $+$/충전 $-\Rightarrow U^{dis}>U^{chg}$ |
| S5 | $\chi_d$: 방전 $\chi$/충전 $1-\chi$; $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ (eq:chid·dHeff) | `func_chi_d` L160 `chi if sd>=0 else 1-chi`, `func_dH_a_eff` L152 | **PASS** — 합-1 거울 대칭 |
| S6 | $\partial\ln L_q/\partial V$: 실현 미분 $=0$(컷 동결), 부등식 $<0$은 컷 규칙 동기 | `_resolve_lag_length` L335 $A=\min(z_\mathrm{cut}n RT,\dots)$ 전이당 상수 | **PASS** — 동결/부등식 자기모순 정정 일관 (D-VEQ 후속) |
| S7 | 꼬리 충전 격자 역전 $\xi[::-1]\cdots[::-1]$; 충전 $dQ/dV$ 방전 거울 양수 (eq:reversal) | L474–477 `if sigma_d>=0 ... else lowpass(ksi[::-1])[::-1]` | **PASS** |
| S8 | $V_n=V_\app-\sigma_d|I|R_n$, 방전 측정$>$내부 (eq:vn) | L412 `V_n=V_in-sigma_d*I_abs*self.Rn` | **PASS** |

**부호 8항: 8/8 PASS — FAIL 0.** 부호 회귀 self-test(R1–R5, verifybox L1171–1196)도 손계산 재현 일치(R1: $\Delta U_\hys=86.7$ mV·$u=0.766$; R2: $\Omega=2RT\Rightarrow0$; R5 두 $\rho$ 극한 반대 — D-PEAK 회귀 가드).

---

## C. 폴리시 4건 무회귀 정밀 검수

### P1 — eq:Veq 출발 다리 가시화 (D-VEQ 해소 보강)
- 추가 문장: "평형 조건 eq:eqcond ($\mu=\mu^0-sF(V-U)$, 배치 몫 자유에너지 기울기 = 전기화학 구동력)에 의해 … $g_j'(\xi)=RT\ln[\xi/(1-\xi)]+\Omega(1-2\xi)=sF(V_\eq-U_j)$."
- **순환 없음**: eq:eqcond는 §sec:center(L350–354, 상류)에서 이미 확립. eq:Veq(L466)는 하류 §sec:hys. 앞→뒤 단방향 참조, forward-defer 아님. KNOWN_DEFECTS D-VEQ가 지적한 "§5로 forward-defer(순환)"이 **역방향으로 해소**됨.
- **수학 정합**: $g'(\xi)=sF(V_\eq-U)$를 $V_\eq$로 풀면 eq:Veq 형태 정확 산출(손검산 일치). s는 양변 동일 부호라 logit·$\Omega$ 항에 $1/(sF)$로만 진입 — 부호 모순 없음.

### P2 — fig:relaxode 캡션 정리 (작가메모 제거)
- 변경: 캡션 말미 "내부 텍스트 ASCII"(작가 빌드 메모) 제거 → "(문턱 진폭 불연속·자세한 논증은 본문 §sec:tail)" 포인터로 교체.
- **본문 중복/모순 없음**: 문턱 진폭 불연속 논증은 본문 L959–963(eq:branch 직후)이 정본. 캡션은 이제 결론 요약 + 본문 inline 참조만 — D-PEAK2(KNOWN_DEFECTS L24–30)의 "매끈한 handoff 호도 금지" 정직 기술이 본문에 보존됨. 캡션이 본문보다 약하게/다르게 말하지 않음.

### P3 — eq:weff s-상쇄 명시 (D-WEFF 해소 보강)
- 추가: "($s$ 부호는 양변 공통이라 상쇄)".
- **수학 검산 PASS**: $sF\,dV_\eq/d\xi|_{1/2}=4RT-2\Omega$ (LHS, eq:Veq 중심 기울기) = $4Fw^\eff$ (RHS). 양변 모두 $sF$ 또는 $F$ 계수 — $s$는 LHS에만 1회, 등식 정리 시 $s^2=1$(s=±1 공히)로 소거. 수치 3점 확인: Ω=0/5000/≈2RT에서 $4RT-2\Omega = 4Fw^\eff$ 완전 일치. 진술 옳음.

### P4 — z_cut "미분 5% 컷 선택값" 명시
- 추가: "$z_\mathrm{cut}$ 는 미분 5% 컷의 선택값".
- **본문 정합**: §sec:lag L798–800이 이미 "원천 $d\xi_\eq/dq$가 정점의 약 5%로 떨어지는 좌표 … 점유 $\xi_\eq$ 자체가 아니라 미분 기준"으로 상술. P4는 그 결론을 박스(eq:Acut)에 재확인 — "선택값(=자유 파라미터)"임을 명시해 코드 기본값 4.357(py L216/225)이 유도된 상수가 아님을 정직 표기. 코드 `min(z_cut*n_safe*R*T, A_cap*R*T)`(L335)와 정합.

**폴리시 4건: 무회귀 4/4. 새 비약·모순·순환 유입 0.**

---

## D. D-PEAK/D-PEAK2·D-WEFF·11식 G-derive 무결 재확인

- **D-PEAK**(eq:peakshape): 본문 L944–949가 $L_V\gg\Delta_\mathrm{grid}$($\rho\to1$)에서만 미분 수렴, $L_V\to0$은 $0/0$이라 종 환원 아님 — eq:branch 스위치가 담당. 정정 방향 정확. 폴리시 무영향.
- **D-PEAK2**(eq:branch 문턱 불연속): 본문 L959–963가 "매끈한 handoff 아니라 이산 모드 스위치, 문턱서 작은 진폭 점프 가능" 정직 기술. P2가 캡션을 본문 포인터로 정렬해 오히려 강화.
- **D-WEFF**: 중심 기울기 다리 $sF\,dV_\eq/d\xi|_{1/2}=4RT-2\Omega \leftrightarrow 4Fw^\eff$ 본문(L577–578) 명시 + P3로 s-상쇄까지 닫음.
- **11식 G-derive**: eq:vn·Uj·dUhys·Ubranch·weff·xieq·eqpeak·dHeff·Lqfull·LV·peakshape·sum — 코드 한 줄씩 대응(§B 표 + tab:nodemap L1126–1141) 전건 일치. 폴리시 후에도 (a)출발→(b)연산→(c)중간식→(d)박스 4단 구조 보존.

---

## 최종 판정

- **부호 8항: 8/8 PASS, FAIL 0.**
- **폴리시 4건 무회귀: 4/4.** P1 다리 수학 정합·비순환, P3 s-상쇄 진술 옳음(s²=1), P2 캡션-본문 무모순, P4 본문 정합.
- **잔존 결함: 0건** (확정 CRIT/HIGH/MEDIUM 0).

### 가장 약한 1곳 (refute mandate — LOW, 회귀 아님)
**fig:doublewell 캡션(L456) "내부 텍스트는 ASCII."**, **fig:barrier 본문 L660 등 figure 내부 영어 라벨** — P2가 fig:relaxode에서만 작가메모성 "ASCII" 문구를 제거했고, 동일 성격 문구가 fig:doublewell 캡션에 1건 잔존(헤더 주석 L22 "내부 텍스트 영어 ASCII"의 도식 라벨 정책이 캡션에 노출). 일관성 관점에서 P2를 fig:doublewell에도 적용하면 완결. **단 이는 빌드/물리/부호와 무관한 순수 문체 LOW이며 무회귀·부호 무결 판정에 영향 없음** — 폴리시 스코프(4건 한정)를 넘지 않으므로 결함 아닌 관찰로 보고.
