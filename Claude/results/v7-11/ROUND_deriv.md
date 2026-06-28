# ROUND_deriv — 유도 다리 3건 적대 검산 (검수 sub, 식 단위 청크)

대상: `v7-11/v7-11.tex` §sec:width(L434–502)·§sec:eqpeak(L505–528)·§sec:lag(L531–615)
기준 코드(정독): `v7-00_spine/Anode_Fit_v11_final.py` func_w(L64-65)·func_ksi_eq(L84-87)·func_L_q(L90-97)

검산 규율: refute mandate(빈 통과 금지) — 각 유도가 *수학적으로 옳은가*, 코드 항을 정확히 재현하는가.

---

## ★ F2 — 완화 속도 $k_j$ 와 $(1+e^{-\mathcal A/RT})$ 분모 : **정확**

대상 서술: L546-547, L582 + eq:Lqfull(L584-589). 
"$k_j=k^++k^-=k^+(1+e^{-\mathcal A/RT})$ (선형 완화=정·역 합, detailed balance $k^-/k^+=e^{-\mathcal A/RT}$)", $L_q=|I|/(Q_\cell k_j)$.

### 적대 1 — detailed balance 부호·방향이 맞나
- affinity 정의(L457-458·L551): $\mathcal A_j=sF(V_n-U_j)=\sigma_d F(V_n-U_j)$.
- eq:xieq(L460) logistic 에서 평형 점유비 = $\xi_\eq/(1-\xi_\eq)=e^{z}$, $z=\sigma_d(V-U)/w$. 기본 폭 $w=RT/F$ 면
  $z=\sigma_d F(V-U)/RT=\mathcal A/RT$ → $\xi_\eq/(1-\xi_\eq)=e^{\mathcal A/RT}$.
- 평형 정지점 net rate 0: $k^+(1-\xi_\eq)=k^-\xi_\eq$ → $k^-/k^+=(1-\xi_\eq)/\xi_\eq=e^{-\mathcal A/RT}$. **텍스트와 정확히 일치(부호·방향 OK).**
  물리 정합: $\mathcal A>0$(정방향 우세)→$k^-/k^+<1$(역 느림), 옳음.

### 적대 2 — 코드 $-\ln(1+e^{-A/RT})$ 항을 정확히 재현하나
- $k_j=k^+(1+e^{-\mathcal A/RT})$, $k^+=k_0 e^{-(\Delta G_a^\eff-\chi_d\mathcal A)/RT}$, $k_0=k_BT/h$.
- $L_q=\dfrac{|I|}{Q_\cell k_j}=\dfrac{|I|}{Q_\cell}\dfrac{h}{k_BT}\dfrac{e^{+(\Delta G_a^\eff-\chi_d\mathcal A)/RT}}{1+e^{-\mathcal A/RT}}
  =\dfrac{T_*}{T}\dfrac{e^{\Delta G_a^\eff/RT}}{1+e^{-\mathcal A/RT}}e^{-\chi_d\mathcal A/RT}$, $T_*=|I|h/(Q_\cell k_B)$. = eq:Lqfull **정확**.
- 로그: $\ln L_q=\ln(T_*/T)-\ln(1+e^{-A/RT})+\Delta G_a^\eff/RT-\chi_d A/RT$.
  func_L_q L96: `ln(T_attempt/T) - ln(1+exp(-A/RT)) + dG_a/RT - x*A/RT`
  (`T_attempt=(I/Q_cell)h/kB=T_*`, `dG_a=dH_a-T*dS_a=ΔG_a^eff`, `x=chi_d`).
  **4항 term-by-term 완전 일치.** $-\ln(1+e^{-A/RT})$ 분모 항이 정확히 $k^-$ 의 정·역 합에서 발생함을 닫음.

판정: **정확.** 코드 정합 1:1. 잔존 비약 없음(아래 비고 1 = 정밀 표현 한계, 결함 아님).

---

## F1 — eq:wbase $w_j=n_jRT/F$ vs func_w, 옵션 weff 구분 : **정확**

- eq:wbase(L442) $w_j=n_jRT/F$. func_w(L65) `return n*R*T/F`. **일치.**
- L446 `'w'` 직접 주입 시 $n_j=w_jF/(RT)$ 역산(`_n_factor`) 서술 — 같은 식에 재투입, 일관.
- 옵션 eq:weff(L449) $w_j^\eff=(RT/F)(1-\Omega_j/2RT)$ 는 **별 박스·use_w_eff 게이트**(L452-454)로 명확히 분리:
  "이 좁힘은 use_w_eff 켤 때만, 기본은 $w_j=n_jRT/F$". 기본/옵션 경계 흐림 없음.
- 미세: weff 식에 $n_j$ 미포함(기본식과 다중도 처리 비대칭)이나, 이는 코드 func_w_eff 설계대로이고 본 라운드 검산 범위(추가 3다리의 수학 정확성) 밖 — 코드 정합은 유지.

판정: **정확.** 기본/옵션 구분 명확.

---

## F3 — logistic 분모 $w_j=n_jRT/F$ 가 func_ksi_eq 와 정합 : **정확**

- 서술 L463: "폭 다중도 $n_j$ 는 $w_j=n_jRT/F$ 로 logistic 인자 분모에 들어간다 … $z=\sigma_d(V_\work-U_j^d)/w_j$, 폭은 func_w(T,n)".
- func_ksi_eq L86: `z = s*(V_n - U)/func_w(T,n)`, func_w(T,n)=`n*R*T/F`.
  → $z=\sigma_d(V_n-U)/(n_jRT/F)=\sigma_d(V-U)/w_j$, $w_j=n_jRT/F$. **정확히 일치.**
- $s\leftrightarrow\sigma_d$, `V_n` 인자 자리에 $V_\work$ 주입(L466-468 명시) — 호출 규약도 코드와 정합.
- eq:xieq 박스(L460)·부호 박스(L471-476: 방전 $V\uparrow⇒\xi\uparrow$, 중심 ½, $w=RT/F=25.7$mV)도 logistic·func_ksi_eq 의 `np.where` 2-갈래(오버플로 가드, 수학적 동일)와 모순 없음.

판정: **정확.** func_ksi_eq 의 $z$ 정의와 1:1.

---

## F4 — 새 문장이 기존 결과 박스(코드 정합)로 *이어지나* : **연결됨(모순 없음)**

- eq:xieq → eq:eqpeak(L513-520): 연쇄율 $d\xi_\eq/dz=\xi(1-\xi)$, $dz/dV=\sigma_d/w_j$ →
  $(\dd Q/\dd V)^\eq_j=Q_j\xi(1-\xi)/w_j$. 코드 `peak_shape=ksi_eq*(1-ksi_eq)/w` 와 일치. 새 유도(F1·F3)가 이 박스로 무모순 진입.
- eq:Lq(L540-543) $L_{q,j}=|I|/(Q_\cell k_j)$ → F2 전개 → eq:Lqfull(코드 func_L_q 박스). 새 다리가 결과 박스로 연속.
- eq:Acut(L553-557) $\mathcal A=\min(z_\mathrm{cut}n_jRT,A_\mathrm{cap}RT)$: $\mathcal A$ 는 $n_jRT$ 스케일(폭 $w_j=n_jRT/F$ 의 $F$배) — F3 의 $w_j$ 와 다중도 $n_j$ 를 공유하므로 일관(컷 affinity 와 폭이 같은 $n_j$ 로 묶임). 모순 아님.

판정: 유도가 결과로 **이어짐**, 기존 코드-정합 박스와 모순 0.

---

## 비고(결함 아님 — 정밀/표현)

1. F2 의 $k^+\simeq k_0\exp[-(\Delta G_a^\eff-\chi_d\mathcal A)/RT]$ 에서 $\chi_d\mathcal A$ 가 정방향 장벽을 낮추는 BV-형 분배 — eq:dHeff 의 $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ 와 **별개의 $\chi_d$ 사용처**(전자는 affinity 분배 $-\chi_d\mathcal A$, 후자는 장벽 흡수 $-\chi_d\Omega$). 코드 func_L_q 는 둘을 분리 인자(`A` 와 `dH_a`)로 받아 정확히 구현. 텍스트도 L592-595 에서 "$\Delta H_a^\eff$ vs $-\chi_d\mathcal A$" 두 경로를 분리 명시 → 혼동 없음. **정확.**
2. eq:weff 의 $n_j$ 부재(F1 미세)는 옵션 경로 한정·코드 설계대로 — 추가 3다리 정확성에 영향 없음.

---

## 반환 6줄
1. F1(eq:wbase vs func_w): **정확** — $w_j=n_jRT/F$ = `n*R*T/F`, weff 옵션은 use_w_eff 게이트로 명확 분리.
2. F2(완화속도 $k_j$·$(1+e^{-A/RT})$ 분모): **정확** — detailed balance $k^-/k^+=e^{-\mathcal A/RT}$ 부호·방향 옳고, func_L_q L96 의 $-\ln(1+e^{-A/RT})$ 항을 4-항 term-by-term 재현.
3. F3(logistic 분모 $w_j$ vs func_ksi_eq): **정확** — $z=\sigma_d(V-U)/(n_jRT/F)$ 가 `s*(V_n-U)/func_w(T,n)` 와 1:1.
4. 코드 정합: 3 다리 모두 func_w·func_ksi_eq·func_L_q 와 1:1 일치(eq:Lqfull 로그가 func_L_q 4항 완전 재현).
5. 잔존 결함: **없음**(refute 시도 후에도 수학·부호·코드 항 모두 통과). 비고 2건은 정밀/표현(결함 아님).
6. 가장 약한 1곳: eq:weff(eq:wbase 와 달리 $n_j$ 미포함 → 다중도 처리 비대칭). 단 옵션 경로·코드 설계대로라 본 라운드 정확성 판정엔 무해 — 향후 weff 사용 시 $n_j$ 일반화 명시 권고(advisory).
