# REVIEW1 — v8-07 (Codex 20번째) 적대 검수

> 검수 sub. 대상 `v8-07.tex`(1158행) 전문 정독. 기준: v11_final.py·v11_flowchart.md·AUTHOR_BRIEF_v8·KNOWN_DEFECTS(전수). refute mandate·빈통과금지.

## 1. 확정 결함 (CONFIRMED)

| ID | 위치 | 결함 | 심각도 |
|---|---|---|---|
| **D-PEAK(★상속·미수정)** | L890–891 | KNOWN_DEFECTS 최우선 ★결함이 **그대로 남음**. "$L_V$ 작으면 $\xi_\mathrm{lag}\to$ 한 칸 뒤처진 $\xi_\eq$ → 식(peakshape)이 이산미분 $\to d\xi_\eq/dV$ 종으로 환원"은 수학적 오류. $\rho=e^{-\Delta_{grid}/L_V}$ 에서 $L_V\to0\Rightarrow\rho\to0\Rightarrow\xi_\mathrm{lag}\to\xi_\eq$(같은 칸)$\Rightarrow$ peak$\to0$(종 아님). 종 환원은 코드의 eq:branch 스위치(L466–468 `L_V<\nu\Delta_{grid}\Rightarrow\xi_\eq(1-\xi_\eq)/w`)가 담당하지 매끈한 극한이 아님. KNOWN_DEFECTS 수정안(연속정당화는 $L_V\gtrsim\Delta_{grid}$, 작은 $L_V$는 스위치)을 **반영하지 않음**. | CRITICAL |
| D-PEAK 부분완화 | L892–900 | 직후 eq:branch(식)를 명시한 것은 옳으나, L890–891 의 틀린 "매끈 환원" 문장과 **논리 충돌**(같은 절에서 환원 메커니즘 2개 주장). 틀린 문장 삭제 필요. | HIGH |
| D-UBR(상속·미수정) | L444–462, eq:Ubranch | KNOWN_DEFECTS 지적대로 $\gamma\cdot h_\eta$ 도입이 유도 아닌 ansatz. L453–454 가 "조기 핵생성·mosaic 평균을 $\gamma$로 축소"로 *언어적* 정당화는 하나, "현상학적 매개변수화(유도 아님)"라는 **명시 라벨 없음** — 유도 가장 위험 잔존. | MEDIUM |
| 미세 | L582, L715 | $z_\mathrm{cut}=4.357$ 근을 "$0.05/4$ 로 정해지는 양의 근"으로 제시(L715). 수치 round-trip 검증 본문에 없음(brief가 요구하는 "코드 작성 가능 수준"엔 부합하나 자체 재산출 부재). | LOW |

## 2. KNOWN_DEFECTS 보유표 (전수)

| 결함 | v8-07 보유? | 근거 |
|---|---|---|
| ★D-PEAK | **보유(미수정)** | L890–891 틀린 환원 문장 잔존 |
| D-VEQ(Veq 다리 forward-defer 순환) | **해소** | L410–411 에 $V_\eq(\xi)=U+\frac{RT}{sF}\ln\frac{\xi}{1-\xi}+\frac{\Omega}{sF}(1-2\xi)$ inline 제시(§3, §5 전). detailed balance 도 §5 본유도(L548–581)로 닫힘 |
| D-DHEFF($\chi_d$ 중간식 점프) | **해소** | L744–768 에 $r^+/r^-=\exp[(\chi+\chi')\mathcal A/RT]$·$\mathcal A_\mathrm{reg}=\sigma_dF(V-U)-\Omega(1-2\xi)$ 중간식 보임 |
| D-WEFF(중심기울기 $4Fw$ 다리) | **부분** | eq:weff(L539–545) 유도는 detailed balance 다리(L520–531)로 닫으나, KNOWN_DEFECTS 가 요구한 $sF\,dV/d\xi\|_{1/2}=4Fw$ 중심기울기 다리는 **없음**(다른 경로로 유도—허용 가능하나 지적 경로 미충족) |
| D-UBR(ansatz) | **보유(라벨만 약화)** | 위 표 참조 |
| D-VN(자명) | 해소 | L264–276 이항 중간식 명시 |
| fig 식번호 오기·곡선중복 | 해소 | fig:hysloop(L477–503)·fig:overshoot 별도 미존재(v8-07은 hysloop 단일), 내부 식번호 오기 없음 |

## 3. 강점 3 / 약점 3

**강점:** ① D-VEQ·D-DHEFF·D-VN 등 KNOWN_DEFECTS 6종 중 다수를 실제 중간식으로 해소(유도 사슬 11식 대부분 단계 보임). ② 부호 8항 v11 1:1 정합(아래 §5 전건 ✓)·결과 박스 식 전부 코드 식별자와 일치(func_U_j/func_w/func_ksi_eq/func_L_q/func_dU_hys/func_U_branch/func_chi_d/func_dH_a_eff 직접 대조). ③ 그림 5개 모두 영어 ASCII 라벨·\ref 연결·캡션 "신규" 표기, verifybox(R1–R4) 수치 회귀로 falsifiable 못박음.

**약점:** ① ★D-PEAK 미수정(최우선 결함 잔존)이 단독 치명. ② D-UBR ansatz 라벨 미부착. ③ L890–891 vs L892–900 절 내부 논리 충돌(같은 환원을 두 메커니즘으로).

## 4. 차원 점수 (합 /35)

| 차원 | 점수 | 비고 |
|---|---|---|
| G-derive(유도 완결성) | 4/5 | 11식 다수 단계화, but D-PEAK 환원 틀림·D-WEFF 지적경로 미충족 |
| 배치 보존(v7-11 N0→N9·박스·표·그림) | 5/5 | 절 순서·결과식·표 4종·그림 5개 보존 |
| 부호 8항 v11 1:1 | 5/5 | 전건 ✓(§5) |
| G-follow/G-usable/완결성 | 5/5 | 6단계 재현 박스(L1059–1067)·tab:inputs·tab:nodemap, orphan 0 |
| 그림(5개·혼란·ASCII·\ref) | 5/5 | ASCII·\ref·캡션 정상, fig 중복/식번호 오기 없음 |
| KNOWN_DEFECTS 반영 | 2/5 | ★D-PEAK·D-UBR 미수정, D-WEFF 부분 |
| 정확성·코드정합 | 5/5 | 결과식·기본값(tab) 코드 대조 0오류 |
| **합** | **31/35** | |

## 5. 부호 8항 (v11 대조)

1. $U_j=(-\Delta H+T\Delta S)/F$, $\Delta G=-FU$ — L348/L69 ✓
2. $\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$ 방전 $V\uparrow\to\xi\uparrow$ — L579/L86–87 ✓
3. $d\xi/dV$ peak 양수·방향불변 — L657–664 ✓
4. $\Delta U_\hys\ge0$, $\Omega\le2RT\to0$, 분기 $\pm\frac12\sigma_d$ — L434/L75–81·L138 ✓
5. $\chi_d$ 충전 $1-\chi$, $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ — L746/L160·L152 ✓
6. $\partial\ln L_q/\partial V$: 컷상수라 실현미분 0, 부등식은 동기 — L820–826 ✓(v7系 함정 회피 명시)
7. 꼬리 충전 격자역전·충전 dQ/dV 방전거울(양수) — L906–917/L474–477 ✓
8. $V_n=V_\app-\sigma_d|I|R_n$, 방전 측정$>$내부 — L274/L412, flowchart 2026-06-29 정정과 정합 ✓

**부호 결함 0/8.**
