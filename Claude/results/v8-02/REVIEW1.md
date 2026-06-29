# REVIEW1 — v8-02.tex 적대 검수 (검수 sub, v8-02)

> 대상 `Claude/results/v8-02/v8-02.tex` (1068행, 전문 정독). 기준 = `Anode_Fit_v11_final.py`(706줄)·`v11_flowchart.md`·`AUTHOR_BRIEF_v8.md`·`KNOWN_DEFECTS.md`(전수 점검).
> Read Coverage: v8-02.tex 1–1068 전행 / v11_final.py 1–706 전행 / 브리프·결함표·flowchart 전문.
> refute mandate·빈 통과 금지·가장 약한 1곳 명시 준수.

---

## 1. 확정 결함 {심각도 · 행 · 틀림 · 옳은 형}

### CRIT-1 · D-PEAK (★ v7-11 상속, 수학적 오류) · 행 863–864
- **틀림**: "$L_V$ 작으면 $\xi_\mathrm{lag}\to$ 한 칸 뒤처진 $\xi_\eq$ 라, 식~\eqref{eq:peakshape} 가 이산 미분 $\to\dd\xi_\eq/\dd V$ 의 종으로 환원된다 — 평형 peak 식~\eqref{eq:eqpeak} 로 돌아간다." → **KNOWN_DEFECTS ★D-PEAK 와 동일한 틀린 명제를 그대로 복원**. 점화식 $\xi_{lag,i}=\rho\xi_{lag,i-1}+(1-\rho)\xi_{eq,i}$, $\rho=e^{-\Delta_{grid}/L_V}$ 에서 $L_V\to0\Rightarrow\rho\to0\Rightarrow\xi_{lag,i}\to\xi_{eq,i}$(**같은 칸**, 한 칸 뒤가 아님)$\Rightarrow$ peak $=(\xi_\eq-\xi_\mathrm{lag})/L_V\to0$ — **종이 아니라 0**. $\to\dd\xi_\eq/\dd V$ 환원은 **반대 극한 $L_V\gg\Delta_{grid}$**($\rho\to1$)에서 성립.
- **자기모순 동반**: 바로 아래 eq:branch(865–872)는 $L_V<\nu\Delta_{grid}$ 를 **평형 종 스위치**(매끈한 극한 아님)로 올바로 라우팅 — 즉 본문이 자기 식과 충돌. 작은 $L_V$ 평형 회복은 *스위치*가 담당하지 매끈한 환원이 아님.
- **옳은 형**: (a) 연속 정당화 $r/L_V=\dd\xi_\eq/\dd V$(quasi-steady)는 $L_V\gtrsim\Delta_{grid}$ 에서만, (b) 작은 $L_V$ 평형 회복은 eq:branch 스위치($L_V<\nu\Delta_{grid}\Rightarrow\xi_\eq(1-\xi_\eq)/w$)로 명시. 863–864 문장 삭제·재서술 필요.
- **상태**: 상속 결함 **미수정**(verbatim 복원).

### HIGH-1 · D-DHEFF (유효 장벽 χ_d·Ω 점프) · 행 718–741
- **틀림**: derivebox 출발 $r_j^+=k_0 e^{-(\Delta G_{a,j}-\chi\mathcal A_j)/RT}$ 는 **χ·𝒜** 인데 박스 결과는 $\Delta H_a^\eff=\Delta H_a-\chi_d\,\Omega$ — **χ→χ_d 방향 분기 주입**과 **𝒜(affinity) 구동력 → 상수 Ω 장벽 흡수** 두 변환의 중간식이 없음. 730–731 의 "깊은 꼬리 $\xi\to1$ 에서 +Ω 흡수 … 충전 거울 $1-\chi$" 는 prose 단언뿐. "합-1 제약" 박스(727)는 $e^{\mathcal A/RT}\overset{!}{=}e^{\mathcal A/RT}$ 로 **공허**(아무것도 안 보임).
- **옳은 형**: KNOWN_DEFECTS 명시대로 중간식 $r^+=k_0 e^{-(\Delta H_a-T\Delta S_a-\chi_d\mathcal A)/RT}$ 를 보이고, 깊은 꼬리 극한에서 $\Omega(1-2\xi)\to+\Omega$ 상수 몫이 장벽으로 흡수되어 $-\chi_d\Omega$ 가 되는 단계를 1식 이상 전개.
- **상태**: D-DHEFF **미수정**.

### HIGH-2 · D-WEFF (유효 폭 유도 전무) · 행 556–561
- **틀림**: $w_j^\eff=\frac{RT}{F}(1-\frac{\Omega_j}{2RT})$(557–560)가 "상호작용이 종을 좁히는 유효 폭 옵션은" 한 줄 + 박스로 **유도 0**. 출발 식·연산·중간식 전무(G-derive 의무 위반).
- **옳은 형**: KNOWN_DEFECTS 명시 중간식 — 중심 기울기 $sF\,\dd V/\dd\xi|_{1/2}=4Fw$(이상 격자 $4RT$ ↔ 정규용액 일반 $4Fw^\eff$ 다리)에서 $g''$/$V_\eq(\xi)$ 의 $\xi=1/2$ 기울기 $\to w^\eff=(RT/F)(1-\Omega/2RT)$ 를 전개.
- **상태**: D-WEFF **미수정**.

### MED-1 · D-VEQ (eq:Veq 다리 forward-defer/순환) · 행 435 (↔ 581–584)
- **틀림**: eq:Veq(435)가 다리 $g_j'(\xi)=sF(V_{\eq,j}-U_j)$ 를 **무유도 전제**로 도입. 그 정당화(detailed balance stationary $\xi/(1-\xi)=e^{\mathcal A/RT}$, $\mathcal A=\sigma_d F(V-U^d)$)는 §5(581–584)에 있어 §4(N3)보다 **뒤** — forward-defer/순환.
- **옳은 형**: 435 에 inline 1줄(stationary $RT\ln[\xi/(1-\xi)]=\mathcal A=sF(V-U)$ + 정규용액 $\Omega(1-2\xi)$ 합류) 추가하거나 §5 결과를 \ref 로 명시 인계.
- **상태**: D-VEQ **부분/미수정**(다리 노출 없음).

### MED-2 · D-UBR (분기 중심 ansatz 라벨 약함) · 행 485–486
- **틀림**: eq:Ubranch 는 "실측 분기 중심을 방향별 한 자유도로 적으면"(부분 현상학 인정)이나, **"유도가 아닌 현상학적 매개변수화"** 명시·γ 가 대칭 중심↔spinodal 한계 사이 **보간 인자**라는 설명 부재. KNOWN_DEFECTS 가 요구한 "spinodal 한계 ±½ΔU_hys 위 현상학적 매개변수화(유도 가장 금지)" 라벨 불충분.
- **옳은 형**: γ·h_η 도입이 유도가 아닌 매개변수화임을 1문장 명시 + γ∈[0,1] 보간 의미.
- **상태**: D-UBR **부분 완화**(상속 대비 일부 개선, 라벨 미달).

### LOW-1 · eq:Lqfull 유도 군더더기 곱셈 · 행 759
- $L_{q,j}$ 전개에서 $e^{0}\cdot e^{\chi_d\mathcal A/RT}\cdot e^{-\chi_d\mathcal A/RT}$ 라는 **상쇄용 더미 인수**를 그대로 노출 — 결과는 옳으나(코드 L96 ln 4항과 1:1) 교과서 가독성 저해. $\chi_d\mathcal A$ 항이 어디서 들어오는지 한 줄 설명으로 대체 권장. (수치·부호 영향 없음.)

### LOW-2 · 미인용(상속 LOW) · 본문 전반
- KNOWN_DEFECTS 의 eq:eyring·bazant2013·dreyer2010 미인용 지적 — v8-02 는 bibliography 에 항목은 두나(1060–1062) **본문 \cite 호출 0**(eyring/bazant2013/dreyer2010 미참조, Eyring 식 750·검산 등에서 인용 가능 지점 존재). hyperref unused-ref 경고 가능.

---

## 2. KNOWN_DEFECTS 보유표 (v8-02)

| 결함 | 등급 | v8-02 행 | 보유? | 비고 |
|---|---|---|---|---|
| ★D-PEAK | CRIT | 863–864 | **보유(미수정)** | verbatim 상속, 자기 eq:branch 와 모순 |
| D-VEQ | MED | 435↔581 | **보유(부분)** | 다리 forward-defer, inline/ref 없음 |
| D-DHEFF | HIGH | 718–741 | **보유** | χ→χ_d·𝒜→Ω 중간식 누락, 합-1 박스 공허 |
| D-WEFF | HIGH | 556–561 | **보유** | 유도 전무(한 줄+박스) |
| D-UBR | MED | 485–486 | **부분 완화** | 현상학 일부 인정, "유도 아님" 라벨 미달 |
| D-VN(minor) | LOW | 244–248 | 해소 | 248 에 이항·극한 서술 충분(자명) |
| fig:overshoot 식번호 오기 | LOW | 505–527(fig:hysloop) | 해소 | 캡션 식번호 정상(eq:dUhys/eq:Ubranch), 라벨 정상 |

---

## 3. 강점 3 · 약점 3

**강점**
1. **부호 사슬 8항 v11 1:1 정합**(§10, 1024–1039) — S1–S8 전건이 코드(L412·L84·L468·L123·L155·L335·L474·L412)와 일치, 특히 S6 의 "$\partial\ln L_q/\partial V=0$ 운영상 실현 / 부등식은 동기" 구분(779–784)을 KNOWN_DEFECTS 경고대로 정확히 처리 — 흐리지 않음.
2. **재현 가능 self-test 수치 고정**(verifybox R1–R4, 1044–1053): $\Omega=12000$ → $u=0.766$ → $\Delta U^\hys\approx86.7$ mV, 분기 ±43.4 mV — 코드 __main__(648–650)·func_dU_hys(L123)와 검산 가능(G-usable 1급).
3. **N0→N9 배치·결과 박스·식별자·표 보존**(v7-11 구조 유지): eq:Uj·eq:dUhys·eq:xieq·eq:eqpeak·eq:Lqfull·eq:reversal 결과식 모두 v11 코드와 일치, 식별자(func_*) 1:1, tab:staging(4건)이 GRAPHITE_STAGING_LIT(L535–564) 값과 정확히 일치.

**약점**
1. **(가장 약한 1곳)** **D-PEAK 상속 미수정**(863–864) — 이번 작업의 ★최우선 결함이자 자기 eq:branch 와 직접 모순. 브리프 §3 G-derive·KNOWN_DEFECTS 1순위를 정면으로 위반.
2. **유도 의무 미달 식 2개**(eq:weff 유도 전무·eq:dHeff χ_d/Ω 점프) — 브리프 §3 "한 줄 점프 금지" 위반. 11 식 중 #2(w_eff)·#9(ΔH_eff) 사슬 불완전.
3. **forward-defer/순환**(eq:Veq 다리가 §5 결과에 의존하나 §4 에 위치) — 단계적 유도 흐름(G-follow)의 국소 단절.

---

## 4. 차원 점수 (7 × 5 = /35)

| 차원 | 점수/5 | 근거 |
|---|---|---|
| ①★G-derive(유도 완결) | 2 | D-PEAK(틀린 극한)·D-WEFF(유도 0)·D-DHEFF(점프)·D-VEQ(forward) 4건 잔존. eq:Uj·eq:dUhys·eq:xieq·eq:Lq·eq:lowpass 등은 단계 충실하나 핵심 4식 미달. |
| ②배치 보존(v7-11) | 5 | 절 순서 N0–N9·결과 박스·식별자·부호·표 4종 그대로, 결과식 변경 0. |
| ③★부호 8항 v11 1:1 | 5 | S1–S8 전건 PASS, 코드 대조 일치. FAIL 0. |
| ④G-follow·G-usable·완결성 | 3 | self-test·worked example 우수(G-usable), 그러나 D-VEQ forward·D-PEAK 모순이 follow 단절. orphan 식 미발견. |
| ⑤그림(유래/신규·ASCII·\ref) | 4 | 8개(v7-11 유래 5: spine·staging·hysloop·logistic·reversal / 신규 3: gxi_derive·lq_chain·fluxcross→실제는 lq_chain·gxi_derive 확인, fluxcross 헤더 언급되나 본문 미발견 가능성). 라벨 영어 ASCII·\ref 정상. **주의**: 파일 헤더(7–8행)가 fig:fluxcross 를 약속하나 본문에 해당 그림 부재 — 헤더-본문 불일치 1건(LOW). |
| ⑥실용(재현 가능성) | 4 | "이 문건만으로 6단계 재현" keybox(984–992)·tab:inputs(954–982) 완비, 코드 식별자 매핑 명확. D-PEAK 오서술이 N8 이해 저해. |
| ⑦직전 수정의 새 결함 | 3 | eq:Lqfull 더미 곱셈(759) 노출, 헤더 fig:fluxcross 약속-부재. 치명 아님. |
| **합** | **26/35** | |

---

## 5. 부호 8항 (브리프 §7, v11 대조)

| # | 항목 | 판정 | 행/코드 |
|---|---|---|---|
| 1 | $U_j(T)=(-\Delta H+T\Delta S)/F$, $\Delta G=-FU$ | ✓ | 318/L68 |
| 2 | $\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$ 방전 $V\uparrow\to\xi\uparrow$ | ✓ | 594/L84 |
| 3 | $\dd\xi/\dd V$ peak 양수·방향 불변 | ✓ | 660/L468 |
| 4 | $\Delta U_\hys\ge0$ / $\Omega\le2RT\to0$ / 분기 $\pm\tfrac12\sigma_d$ | ✓ | 473/L123,138 |
| 5 | $\chi_d$ 충전 $1-\chi$ · $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ | ✓ | 733/L155,149 |
| 6 | $\partial\ln L_q/\partial V$ 컷상수라 운영 0(부등식=동기) | ✓ | 779/L335 |
| 7 | 꼬리 충전 격자 역전 · 충전 $dQ/dV$ 방전 거울(양수) | ✓ | 878/L474–477 |
| 8 | 분극 $V_n=V_\app-\sigma_d|I|R_n$(방전 측정 $>$ 평형) | ✓ | 245/L412 |

**부호 8항 전건 PASS — 부호 FAIL 0.**

---

## 6. 종합

- 부호·배치는 1급(②③ 만점). **유도 완결(①)이 미달** — KNOWN_DEFECTS 5종 중 ★D-PEAK(CRIT 상속 미수정)·D-DHEFF·D-WEFF(HIGH) 3종이 실질 잔존, D-VEQ·D-UBR(MED) 부분. 이는 v8-02 가 "유도 확장판" 목표의 핵심 사슬 4식에서 브리프 §3 "한 줄 점프 금지"를 못 지킨 결과.
- 체리픽·최종(v8-10/11)이 이 4식을 채택할 경우 위 5개 결함 전부 수정 필요.
