# ROUND_sign — v7-11 부호 사슬 전수 재검 + Phase6 보완 6건 무회귀

검수 sub(리뷰 전용). 대상 `v7-11/v7-11.tex`(890행 전문 정독), 기준 `v7-00_spine/Anode_Fit_v11_final.py`(706행)·`v11_flowchart.md`.
청크 스킴 = 라인 + 부호사슬(S1–S8) 1:1 코드 대조. refute mandate·가장 약한 1곳·빈 통과 금지.

---

## 1. 부호 8항 PASS/FAIL (S1–S8) — v11 코드 1:1 재대조

| 항 | 명제 | tex 식·행 | 코드 근거 | 판정 |
|---|---|---|---|---|
| **S1** | $U_j=(-\Delta H+T\Delta S)/F$, $\Delta G=-sFU$, 발열→중심↑ | eq:Uj(L321)·eq:eqcond(L311), 검산 L837 | `func_U_j` L69 `(-dH_rxn+T*dS_rxn)/F` — 부호 동일. $\Delta H<0\Rightarrow -\Delta H>0$ 중심↑ | **PASS** |
| **S2** | $\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$, 방전 $V\!\uparrow\Rightarrow\xi\!\uparrow$ | eq:xieq(L460), 검산 L839 | `func_ksi_eq` L86 `z=s*(V_n-U)/func_w` — $\sigma_d$ 부호 동일. $z\ge0/z<0$ 분기 수학적 동일 | **PASS** |
| **S3** | $d\xi/dV=\sigma_d\xi(1-\xi)/w$, peak $=|d\xi/dV|\ge0$ 방향 불변 | eq:eqpeak(L514–518), 검산 L841 | L468 `ksi_eq*(1-ksi_eq)/w` — $\sigma_d$ 미분서 1회 들어오나 모양은 절댓값 양수. 정합 | **PASS** |
| **S4** | $\Delta U_\hys\ge0$, $\Omega\le2RT\to0$; 분기 $\pm\tfrac12\sigma_d$, $U^\dis>U^\chg$ | eq:dUhys(L370–372)·eq:Ubranch(L384), 검산 L843 | `func_dU_hys` L123–130 `(2/F)(Ω·u-2RT·artanh u)`, `Omega<=2RT→0.0`; `func_U_branch` L138 `+0.5*σ_d*h_eta*γ*ΔU` — 부호 동일 | **PASS** |
| **S5** | $\chi_d$ 방전 $\chi$/충전 $1-\chi$; $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ | eq:chid(L567)·eq:dHeff(L575), 검산 L845 | `func_chi_d` L160 `χ if σ_d>=0 else 1-χ`; `func_dH_a_eff` L152 `dH_a-chi_d*Omega` — 부호 동일 | **PASS** |
| **S6** | $\partial\ln L_q/\partial V<0$(물리 동기), 실현 미분 $=0$(컷 동결) | eq:Lqfull·eq:LV 논의 L600–606, 검산 L847 | `_resolve_lag_length` L335 `A=min(z_cut·n·RT, A_cap·RT)` — $\sigma_d$ 크기 밖(충전 음수상한 버그 정정 주석 L329–331). $L_q$ V-비의존 스칼라 | **PASS** |
| **S7** | 충전 격자 역전 $\xi[::-1]\cdots[::-1]$, 충전=방전 거울 양수 | eq:reversal(L658–662), 검산 L851 | L474–477 `σ_d>=0` 그대로 / `else lowpass(ksi[::-1])[::-1]` — 분기 동일. `(ksi_eq-occ_lagged)/L_V` 양수 | **PASS** |
| **S8** | $V_n=V_\app-\sigma_d|I|R_n$, 방전 측정$>$내부 | eq:vn(L269), 검산 L853 | L412 `V_n=V_in-sigma_d*I_abs*self.Rn` — 부호 동일. flowchart L88 정정(방전 V_app>V_n)과 일치 | **PASS** |

**부호 8/8 PASS — FAIL 0.** 기준 명제(방전 $V\!\uparrow$→탈리튬화↑, 충전=방전 거울 양수)와 전건 정합.

---

## 2. Phase6 보완 6건 무회귀 (부호 사슬 무손상)

### F1 — eq:wbase 신설 + 재참조 (옳은 자리만 가리키나)
- 신설 eq:wbase(L441–444) `w_j=n_jRT/F (기본 폭)` = `func_w` L65 `n*R*T/F`. **코드 정합.**
- 재참조 3곳 검증: ① 본문 L463 logistic 분모 설명 "식 eqref{eq:wbase}의 $w_j=n_jRT/F$" — 기본 폭 자리, 옳음. ② tab:nodemap N4(L820) `w_j=n_jRT/F (w^eff)` → `eqref{eq:wbase}(eqref{eq:weff})` — 기본 eq:wbase, 옵션 eq:weff 괄호 분리, 옳음. ③ tab:inputs(L763) `w 또는 n` 행 → `eqref{eq:wbase}` / 재현박스 6단계 (3)(L795) → `폭 w_j eqref{eq:wbase}`.
- **기본 폭 vs 옵션 weff 혼동 해소 확인**: eq:weff(L449)는 별도 번호로 분리, `use_w_eff` 켤 때만(L453, 코드 `_width` L285–288 동일). 재참조 어디에도 기본 폭 자리에 eq:weff를 잘못 가리킨 곳 없음. **무회귀.**

### F2 — $L_q$ 분모 $1/(1+e^{-A/RT})$ 유도(완화속도=정·역 합) ★최약 검증 지점
- 새 문장 L546–547: $k_j=k^++k^-=k^+(1+e^{-\mathcal A/RT})$ (detailed balance $k^-/k^+=e^{-\mathcal A/RT}$), $k^+\simeq k_0\exp[-(\Delta G_a^\eff-\chi_d\mathcal A)/RT]$, $k_0=k_BT/h$.
- 손유도 검산: $L_q=|I|/(Q_\cell k_j)=\frac{|I|h}{Q_\cell k_BT}\cdot\frac{e^{(\Delta G_a^\eff-\chi_d A)/RT}}{1+e^{-A/RT}}=\frac{T_*}{T}\cdot\frac{e^{\Delta G_a^\eff/RT}e^{-\chi_d A/RT}}{1+e^{-A/RT}}$ ($T_*=|I|h/Q_\cell k_B$).
- 코드 `func_L_q` L96: `log(T_attempt/T) - log(1+e^{-A/RT}) + dG_a/RT - x*A/RT`, `x=chi_d`, `dG_a=dH_a_use-T·dS_a`. **항별 1:1 일치** — 분모 $1/(1+e^{-A/RT})$가 정확히 `-log(1+e^{-A/RT})`, $-\chi_d A/RT$가 `-x*A/RT`.
- eq:Lqfull(L585) tex 표기도 동일. **새 $k^+(1+e^{-A/RT})$가 결과 부호·크기와 정합** — A>0이라 $e^{-A/RT}\in(0,1)$, 인자 $\in(1,2)$ 물리적. 분모가 $L_q$를 줄이는 방향(완화 빨라짐)으로 부호 정합. **무회귀, 부호 사슬 무손상.**

### F3 — logistic 폭 다중도 $n_j$ 전파
- L463 "폭 다중도 $n_j$는 eq:wbase의 $w_j=n_jRT/F$로 logistic 인자 분모에 들어간다" — `func_ksi_eq(T,V_n,U,n,s)` L86 `func_w(T,n)` 분모에 $n$ 전파, 코드 동일(`_n_factor` L274–280). S2 부호 무영향(분모 양수). **무회귀.**

### F4 — z_cut 미분 5% 표기
- L551–552 "원천 $d\xi_\eq/dq$가 정점의 ~5%로 떨어지는 좌표, $z_\mathrm{cut}=4.357$이 그 미분 5% 컷에 대응 — 점유 $\xi_\eq$ 자체가 아니라 **미분 기준**". 코드 주석 L327–328 `dξ_eq/dq가 정점의 ~5%(z_cut=4.357)` 와 일치. 부호 무관 표기 정밀화. **무회귀.**

### F5 — spinodal 부호순 명시
- L368: $(1-2\xi_{s,j}^-)=+u_j$, $(1-2\xi_{s,j}^+)=-u_j$, "극대에서 극소를 빼면 $U_j$ 상쇄". eq:spinodal(L355) $\xi_s^\pm=\tfrac12(1\pm u)$이라 $1-2\xi_s^-=1-(1-u)=+u$, $1-2\xi_s^+=1-(1+u)=-u$ — **부호순 정확.** 극대($\xi_s^-$, 방전 상승 가지 끝)$>$극소($\xi_s^+$)라 $\Delta U^\hys\ge0$(eq:dUhys), S4와 정합. fig:hysloop(L412–414)도 $\xi_s^-$ 상단/$\xi_s^+$ 하단 일치. **무회귀.**

**6 보완 전건 무회귀 — 부호 사슬 무손상.** R1–R4 self-test(L861–874) 수치도 코드 `__main__`(L641–669)과 같은 양: R1 $\Delta U^\hys$=86.7 mV($u$=0.766) — 코드 L648 `func_dU_hys(298.15,12000)` 동일량, R2 $\Omega=2RT$→0, R3 $|I|\to0$ 환원, R4 동결.

---

## 3. 잔존 결함 (심각도·행)

부호·6보완 관련 **CRITICAL/HIGH 결함 0.** 아래는 LOW(선택, 부호·무회귀 무관):

- **L587/L591 (LOW·표기)**: eq:Lqfull에서 $T_*\equiv|I|h/(Q_\cell k_B)$ 정의, 본문은 $T_\mathrm{attempt}=(I/Q_\cell)h/k_B=T_*$로 환산 — 코드 L94 `T_attempt=(I/Q_cell)*h/kB` 동일. 단 $T_*$가 "온도 차원 attempt"임은 명시 안 됨(코드 변수명 `T_attempt`만). 부호·결과 무영향, 가독성 LOW.
- **L546 (LOW·엄밀성)**: $k^+\simeq k_0\exp[-(\Delta G_a^\eff-\chi_d\mathcal A)/RT]$의 `≃`(근사) — BV/Eyring 전이상태 근사임을 §8.3 $\chi_d$ 흡수 논의(L571–572)가 받쳐 모순 없음. 결함 아님(표기 주의만).
- **검산 S6/R4 (정성→정량 정합 확인)**: $\partial\ln L_q/\partial V=0$(실현)·$<0$(동기) 이중 진술 — L600–606·L847–850·L871–873 세 곳 동일 논리로 일관, 자기모순 0. (직전 버전 회귀 우려 지점이었으나 본 최종본에서 정합.)

가장 약한 1곳 적대검증 = **F2 $L_q$ 분모 유도** → 손유도·코드 항별 대조 결과 **정합**(결함 없음). 빈 통과 아님: $T_*$ 차원 표기(LOW)·`≃` 근사 명시를 잔존으로 적출했으나 부호·무회귀와 무관.

---

## 반환 요약
- 부호 8/8 PASS, **FAIL 없음**.
- Phase6 보완 6건(F1–F5) **전건 무회귀** — 부호 사슬 무손상.
- F2 새 유도($k_j=k^+(1+e^{-A/RT})$)·F5 부호순 모두 코드 결과식과 정합.
- 잔존 결함 CRITICAL/HIGH = 0, LOW = 2건(L587 $T_*$ 차원 표기·L546 `≃` 근사 명시, 부호 무관).
