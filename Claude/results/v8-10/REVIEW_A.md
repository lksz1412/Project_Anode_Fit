# REVIEW_A — v8-10.tex 적대 재검수 (물리·부호·유도 수학 렌즈)

검수 sub. 리뷰 전용(수정·커밋 X). 대상 = `v8-10.tex`(1205행, 표기상 1199행 ≈ \end{document}까지 본문).
기준 정독 = `Anode_Fit_v11_final.py`(func_w/U_j/ksi_eq/L_q/dU_hys/U_branch/chi_d/dH_a_eff + dqdv L374-484 + _resolve_lag_length L307-351),
`v11_flowchart.md`, `KNOWN_DEFECTS.md`(D-PEAK·D-PEAK2·D-VEQ·D-DHEFF·D-WEFF·D-UBR).
모든 핵심 유도는 SymPy/NumPy 로 직접 재검산(가장 약한 곳 빈 통과 금지).

---

## 1. 부호 8항 — v11 코드 1:1 재대조 (PASS/FAIL)

| # | 항목 | 코드 정본 | 문건 식/행 | 판정 |
|---|------|-----------|-----------|------|
| S1 | $U_j=(-\Delta H+T\Delta S)/F$, $\Delta G=-FU$ | `func_U_j` L69 `(-dH_rxn+T*dS_rxn)/F` | eq:Uj(365)·eq:eqcond(348) | **PASS** |
| S2 | $\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$ | `func_ksi_eq` L86 `z=s*(V_n-U)/w` | eq:xieq(612) | **PASS** |
| S3 | $d\xi/dV=\sigma_d\xi(1-\xi)/w$, peak 양수 | L468 `ksi_eq*(1-ksi_eq)/w` | eq:eqpeak(744) | **PASS** |
| S4 | $\Delta U_\hys\ge0$, $\Omega\le2RT{\to}0$, 분기 $\pm\tfrac12\sigma_d$ | `func_dU_hys` L123-130, `func_U_branch` L138 `+0.5*sigma_d*h_eta*gamma*dU` | eq:dUhys(488)·eq:Ubranch(507) | **PASS** |
| S5 | $\chi_d$ 방전 $\chi$/충전 $1-\chi$; $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ | `func_chi_d` L160, `func_dH_a_eff` L152 | eq:chid(811)·eq:dHeff(820) | **PASS** |
| S6 | $\partial\ln L_q/\partial V$ 부호(동결 vs 동기) | `func_L_q` L96 `+dG_a/RT - x*A/RT` (A 컷 상수) | eq:Lqfull(837)·§논의(855-859) | **PASS** |
| S7 | 꼬리 충전 격자 역전 $\xi[::-1]\cdots[::-1]$, 충전=방전 거울(양수) | L474-477 `_causal_lowpass(ksi[::-1])[::-1]` | eq:reversal(968) | **PASS** |
| S8 | 분극 $V_n=V_\app-\sigma_d|I|R_n$, 방전 측정$>$내부 | L412 `V_in - sigma_d*I_abs*self.Rn` | eq:vn(285)·(289) | **PASS** |

**부호 8항 결과 = 8/8 PASS, FAIL 0.** 숨은 flip·자기모순 없음.
- S6 자기모순 점검(KNOWN_DEFECTS 경고 자리): 코드 `func_L_q` 는 A 를 컷 상수로 받으므로 실현 미분 $\partial\ln L_q/\partial V=0$ 이 맞고(전이당 1 스칼라), 부등식 $<0$ 은 컷 규칙 *동기*로만. 문건 S6(1156-1159)·R4(1180-1182)가 이 둘을 "한 단조성 공유"로 명시 분리 — **정직**. 수치로 $\partial\ln L_q/\partial A<0$ 확인(A=1→4RT 에서 lnLq_kin -0.81→-2.02).
- S8 부호: flowchart L88 의 2026-06-29 정정(방전 측정$>$평형)과 문건 (289)(1162) 일치. 과거 "관측 V 평형보다 낮음" 회귀 **없음**.

---

## 2. 11식 유도 사슬 G-derive 직접 검산

| 식 | 검산 방법 | 결과 |
|----|-----------|------|
| eq:Uj | $(-\Delta H+T\Delta S)/F$, staging 표 4건 round-trip | **OK** (계산 vs 표: +0.88/-0.08/+0.32/+0.29 mV — 소수 반올림 내) |
| eq:logisticsolve (logistic) | detailed balance(eq:db) $\chi$ 상쇄 → 정지점 logit | **OK** ($\chi\mathcal A+(1-\chi)\mathcal A=\mathcal A$ 합-1 정확) |
| eq:dUhys (spinodal→artanh) | 2nd 미분 $g''=RT/[\xi(1-\xi)]-2\Omega$, spinodal $\xi^\pm=\tfrac12(1\pm u)$, gap | **OK** (SymPy: box==hysdiff(s=1) True; log step $\ln\frac{1-u}{1+u}-\ln\frac{1+u}{1-u}=-4\,\mathrm{artanh}\,u$ 수치 확인 4자리; 소u 전개 $\to\frac{8RT}{3F}u^3$ 정확) |
| eq:hyssub 대입 | $\xi/(1-\xi)|_{\xi_s^\pm}=\frac{1\pm u}{1\mp u}$, $(1-2\xi)|_{\xi_s^\pm}=\mp u$ | **OK** (4건 모두 SymPy True) |
| eq:Lqfull (분모 $1+e^{-A/RT}$, forward $e^{-\chi_d A/RT}$) | $k_j=r^+(1+e^{-\mathcal A/RT})$, $L_q=|I|/(Q_\cell k)$ → 코드 `ln_Lq` 1:1 | **OK** (코드 L96 `+dG_a/RT-x*A/RT` ↔ eq:Lqfull `exp[dG_a/RT]·e^{-χ_d A/RT}/(1+e^{-A/RT})` 부호·항 일치). $L_q\propto|I|$ 수치 확인(ratio=2.0000) → $|I|{\to}0\Rightarrow L_V{\to}0$ |
| eq:dHeff ($\chi_d\Omega$ 흡수) | $-\Omega(1-2\xi)\to+\Omega$ 깊은꼬리, $\chi_d$ 계수 | **OK** (코드 `func_dH_a_eff` L152 `dH_a-chi_d*Omega`; D-DHEFF 가 요구한 중간식 $r^+=k_0e^{-(\dots-\chi_d\mathcal A)/RT}$ = eq:bv(588)+eq:kuniv(785) 존재) |
| eq:Acut (꼬리 컷) | $\mathcal A=\min(z_\mathrm{cut}nRT,A_\mathrm{cap}RT)$, $\sigma_d$ 크기서 제외 | **OK** (코드 L335 일치; n=1 서 A_cap 바인드 9916 J/mol) |
| eq:memory/lowpass (꼬리 합산) | 1계 ODE 적분인자 $e^{q/L_q}$ → 이산 $\rho=e^{-\Delta/L_V}$ | **OK** (lfilter $[1-\rho]/[1,-\rho]$ = eq:lowpass 점화식) |
| eq:sum (합산) | 보존식 $Q_\cell q=Q_\bg+\sum Q_j\xi_j$ 직접 미분 | **OK** (가정 아님 명시, 서로소 자리 전제) |

소-u 임계 연속성($u^3\propto(T_c-T)^{3/2}$, $T_c=\Omega/2R$): eq:dUhys(495) 정확.

---

## 3. D-PEAK·D-PEAK2 검산

- **방향(D-PEAK)**: 문건 (922-925)(939-944)·R5(1183-1188)가 "$L_V\gg\Delta_\mathrm{grid}\Rightarrow\rho\to1\Rightarrow$ 매끈 미분 / $L_V\to0\Rightarrow\rho\to0\Rightarrow\xi_\mathrm{lag}\to\xi_\eq$(같은 칸) $0/0$, 종으로 매끈 환원 아님" — **정확**. v7-11 상속 오류("$L_V$ 작으면 종 환원") **삭제·반대 극한으로 정정 확인**.
- **eq:branch 인수(D-PEAK2)**: 작은 $L_V$ 평형 회복을 "꼬리식 극한"이 아니라 eq:branch 스위치($L_V<\nu\Delta_\mathrm{grid}$, $\nu$=2)가 담당으로 명시(944-945, 코드 L466-468 일치) — **정확**.
- **문턱 진폭 불연속**: (954-958)이 "매끈한 handoff 아니라 이산 모드 스위치, 문턱서 꼬리분기 진폭 ↔ 평형 종 진폭($\propto1/w$) 정확히 안 맞아 작은 불연속 가능" 으로 **정직 기술** — KNOWN_DEFECTS D-PEAK2 요구 충족. 과·소 주장 없음(불연속을 "있을 수 있다"로 한정, 호도 X).
- 범위 충돌(D-PEAK2 4번): eq:peakshape(B)를 무조건 $d\xi/dV\approx r/L$ 로 적고 뒤에서 large-L 한정하는 모순 — v8-10 은 한 곳(939)에서 "$L_V\gg\Delta$ 쪽이 수렴 극한"으로 조건 명시, **모순 없음**.

**D-PEAK / D-PEAK2 = 정확.**

---

## 4. D-WEFF 다리 검산

- eq:weff 다리(572-575): "$sF\,dV_\eq/d\xi|_{1/2}=4RT-2\Omega_j$ 와 $4Fw^\eff_j$ 를 같다 → $w^\eff=(RT/F)(1-\Omega/2RT)$".
- SymPy 재검산: $sF\,dV_\eq/d\xi|_{1/2}=4RT-2\Omega$ **참**; 일반 폭 logistic 중심기울기 $d\xi/dV|_{1/2}=s/(4w)\Rightarrow sF\,dV/d\xi=4Fw$ **참**; $4Fw^\eff=4RT-2\Omega$ 풀면 $w^\eff=RT/F-\Omega/(2F)=(RT/F)(1-\Omega/2RT)$ **참**(코드 `func_w_eff` L144 일치).
- **¼ 인수 오류 없음 · 차원오류(stray F) 없음 · orphan 기호(s_F) 없음.** v8-02/03(¼)·v8-07(s_F orphan) 회귀 자리는 v8-10 에서 **클린**. grep `s_F`/`stray` → 헤더 주석(5행) 외 본문 0건.
- 중간식(D-WEFF 가 요구한 "$4RT\leftrightarrow4Fw^\eff$ 다리")은 (565)에서 이상 극한 $d\xi_\eq/dV|_{1/2}=sF/(4RT)$ → 폭척도 $RT/F$ 정의로 명시 — 한줄점프 아님.

**D-WEFF = 정확.**

---

## 5. 극한·staging 표값 v11 일치

- $\Omega\le2RT\Rightarrow\Delta U_\hys=0$: R2 수치 $2RT=4958$ J/mol(문건 4958), $u=0\Rightarrow0$ — 코드 `if Omega<=two_RT: return 0.0` 일치. **OK**
- $|I|\to0$: $L_q\propto|I|\Rightarrow L_V\to0\Rightarrow$ eq:branch 평형 종, $\sigma_d$ 불변(R3) — 코드 L466 일치. **OK**
- staging 표(tab:staging) U·ΔH·ΔS·Q·Ω·ΔH_a·dVdq: 코드 `GRAPHITE_STAGING_LIT` 값과 round-trip U 정합(§5 위). **OK**
- R1(86.7 mV), R2(4958), R4(동결), N2 codebox(0.0853 V) 전부 재산출 일치.

---

## 확정 결함 (심각도·행/식·틀림·옳은형)

| ID | 심각도 | 행/식 | 틀림 | 옳은 형 |
|----|--------|-------|------|---------|
| (없음 — CRITICAL/HIGH 물리·부호·유도 결함 0) | — | — | 적대 검수에서 부호·유도 사슬 무결, 코드 1:1 정합 | — |
| W1 | LOW | eq:Veq 다리 458행 | $g_j'(\xi)=sF(V_\eq-U_j)$ 를 §1.4 "출발"로 단언하되, $g'(\xi)=\mu(\xi)-(\text{선형몫})$ ↔ eq:eqcond `$\mu=\mu^0-sF(V-U)$` 연결 한 줄이 괄호 안 압축(eq:mu→eq:gxi→eq:eqcond 잇는 명시 부재) | 458행 괄호에 "eq:eqcond 의 $\mu-\mu^0=-sF(V-U)$ 와 eq:gxi 의 $g'(\xi)=\mu-g^{0\prime}$ 를 합류"한 1줄 추가(D-VEQ 가 §detailed balance 로 forward-defer 안 한 건 **잘 됨** — 단 다리 가시화만 보강) |
| W2 | LOW | (302-303) `n_work=max(2048, 2|V_n|)` | 문건 표기 $2\,|V_n|$ 는 `V_n.size*2`(점 수)인데 절댓값 기호 $|\cdot|$ 가 크기로 오독 가능 | $2\,N_{V_n}$ 또는 "$2\times\text{len}(V_n)$"로 표기 |
| W3 | NOTE | (657)(685)(719) 등 신규 그림 캡션 "내부 텍스트 ASCII" 반복 | 결함 아님(빌드 제약 주석) — 일부 캡션엔 있고 일부 없어 비일관 | 통일 또는 서문 1회로 이전(미적) |

> 4-tier: **확정 결함(물리·부호·유도) = 0**. W1-W3 은 가독·표기 LOW/NOTE(반증 가능 회귀 아님). 빈 통과 방지를 위해 가장 약한 3곳을 아래 refute 로 별도 제시.

---

## 가장 약한 3곳 (refute mandate)

1. **eq:Veq 출발 다리(458행)** — 가장 약함. `g'(ξ)=sF(V_eq−U)` 가 §1.4 첫 줄에 전제로 등장. refute 시도: "eq:db(kinetic, §1.6)에 forward-defer 한 순환 아닌가?" → **방어됨**: 이 다리는 eq:eqcond(열역학 평형, §1.3, 이미 유도됨)에서 나오며 eq:db 와 독립. 따라서 KNOWN_DEFECTS D-VEQ(순환)는 **해소**. 다만 eq:mu(403)→eq:gxi(409)→eq:eqcond(348) 를 잇는 한 줄이 괄호로 압축되어 G-derive 가시성만 약함(W1).
2. **eq:Acut 컷 z_cut=4.357 의 "5%" 정당화(793-796)** — refute: "$z_\mathrm{cut}=4.357$ 이 미분 $d\xi_\eq/dq$ 의 5% 컷에 대응" 이 ansatz 위장 아닌가? → 부분 방어: logistic 미분 종의 꼬리에서 $\xi(1-\xi)/[\xi(1-\xi)]_{max}=0.05\Rightarrow$ 중심서 $z=\pm$수 RT 규모는 정성 맞으나, $4.357$ 정확값의 닫힌 산출(예 $\mathrm{sech}^2$ 5% 점)이 본문에 없음. 결함은 아님(코드 기본값·피팅 override 명시)이나 "약한 유도" 자리. 권고: v8-11 에 $4.357=2\,\mathrm{arccosh}(\sqrt{20})$ 류 닫힌 출처 1줄 또는 "경험 컷 상수"로 격하 표기.
3. **eq:dHeff 깊은꼬리 $-\Omega(1-2\xi)\to+\Omega$ 흡수(816-818)** — refute: "$\xi\to1$(방전)·$\xi\to0$(충전) 거울에서 $(1-2\xi)\to\mp1$ 라 $-\Omega(1-2\xi)\to\pm\Omega$ 인데 본문은 둘 다 $+\Omega$?" → 방어됨: 방전 꼬리는 $\xi\to1\Rightarrow-\Omega(1-2)= +\Omega$; 충전 꼬리는 $\xi\to0\Rightarrow-\Omega(1-0)=-\Omega$ 이나 충전은 *역방향* 장벽에 들어가 $\chi_d=1-\chi$ 가 받으므로 부호가 $\chi_d\Omega$ 로 흡수(코드 `dH_a-chi_d*Omega` 가 방향별 $\chi_d$ 로 자동 처리). 본문 (816) "역방향 장벽의 상수 몫이 같은 $+\Omega$ 로 흡수" 는 *방전 기준 서술*이라 충전 거울 1줄이 암묵 — 약하나 코드는 정확. 권고: "충전은 $\chi_d=1-\chi$ 로 부호가 따라간다" 1줄 명시.

---

## v8-11 보완 권고 (전부 LOW/가독 — 물리 수정 불요)

1. **W1**: eq:Veq(458) 괄호에 eq:mu→eq:gxi→eq:eqcond 합류 1줄(G-derive 다리 가시화). D-VEQ 순환은 이미 해소이므로 식 변경 X, 설명만.
2. **W2**: $n_\work=\max(2048,2|V_n|)$ 의 $|V_n|$ → $\text{len}(V_n)$ 표기 정정.
3. **약점2**: eq:Acut $z_\mathrm{cut}=4.357$ 닫힌 출처 1줄 또는 "경험 상수" 격하.
4. **약점3**: eq:dHeff 충전 거울($\chi_d=1-\chi$ 부호 추종) 1줄.
5. **W3**: 캡션 "ASCII" 주석 일관화(미적, 선택).

---

## 결론

v8-10 은 부호 8/8 PASS, 11식 유도 사슬 전부 G-derive 직접 검산 통과(SymPy/NumPy),
D-PEAK·D-PEAK2·D-WEFF·D-VEQ·D-DHEFF·D-UBR(KNOWN_DEFECTS 6종) **전부 해소·정확**.
물리/부호/유도 CRITICAL·HIGH 결함 0. 잔존은 LOW/NOTE 가독·다리 가시화 3-5건뿐.
"한 번에 OK" 가 아니라 적대 검수를 거친 결과로도 무결 — v8-11 은 W1-W3 미세 보강만 권고.
