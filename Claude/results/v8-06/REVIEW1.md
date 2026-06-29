# REVIEW1 — v8-06 적대 검수 (검수 sub, 리뷰 전용)

> 대상 `v8-06.tex` (1182행) 전문 정독(3청크: 1–502 / 503–1004 / 1005–1182).
> 기준 정독: `Anode_Fit_v11_final.py`(func_U_j/func_w/func_ksi_eq/func_dU_hys/func_U_branch/
> func_chi_d/func_dH_a_eff/func_L_q/_causal_lowpass/dqdv L412–483 직접 대조),
> `v11_flowchart.md`, `AUTHOR_BRIEF_v8.md`, `KNOWN_DEFECTS.md`(전수).
> refute mandate·가장 약한 1곳·빈 통과 금지 적용.

---

## 1. 확정 결함

### ★ C1 (CRITICAL) — D-PEAK 미수정·상속 (KNOWN_DEFECTS 최우선 결함 그대로)
KNOWN_DEFECTS 가 ``틀림''으로 명시한 문장이 v8-06 에 **두 곳** 잔존:
- **L916** (fig:relaxode 캡션): ``$L_V$ 가 작으면 $\xi_\mathrm{lag}$ 이 한 칸 뒤처진 $\xi_\eq$ 라 평형 종(eq:eqpeak)으로 환원''
- **L931–932** (§peak\_shape 본문): ``$L_V$ 가 작으면 $\xi_\mathrm{lag}\to$ 한 칸 뒤처진 $\xi_\eq$ 라, eq:peakshape 가 이산 미분 $\to d\xi_\eq/dV$ 의 종으로 환원''

수학: 점화식 L890 eq:lowpass $\xi_{lag,i}=\rho\xi_{lag,i-1}+(1-\rho)\xi_{eq,i}$, $\rho=e^{-\Delta_{grid}/L_V}$ 를 v8-06 이 **스스로 적어 두고도**, $L_V\to0\Rightarrow\rho\to0\Rightarrow\xi_{lag}\to\xi_{eq}$(같은 칸, ``한 칸 뒤처진''이 아님)$\Rightarrow$ peak$\to0$ 임을 놓침. 매끈한 $d\xi_{eq}/dV$ 환원은 **반대 극한 $L_V\gg\Delta_{grid}$**($\rho\to1$). 작은 $L_V$ 평형 회복의 *진짜* 담당은 L936 eq:branch 스위치($L_V<\nu\Delta_{grid}$)인데, 본문이 그 스위치를 옳게 제시(L932–941)하면서 동시에 틀린 ``매끈한 환원''을 병기해 **자기모순**. 수정: L916·L931 두 문장 삭제→(a) 연속 정당화는 $L_V\gtrsim\Delta_{grid}$, (b) 작은 $L_V$ 평형 회복은 eq:branch 스위치로 귀속.

### C2 (LOW) — eq:eyring·bazant2013·dreyer2010 미인용 잔존
서지에 bazant2013/eyring1935/dreyer2010 등재(L1174–1176)되나 본문 `\cite` 없음(Eyring 식 L578, 정규용액·히스 등 도입 자리에서 미인용). KNOWN_DEFECTS fig:overshoot 항의 LOW 결함과 동류 — graphite_ica 흐름엔 dahn/ohzuku/bloom/dubarry 만 cited.

---

## 2. KNOWN_DEFECTS 보유 여부 표 (9종 중 v8-06 적용 가능 항 전수)

| 결함 | 내용 | v8-06 상태 |
|---|---|---|
| ★D-PEAK | "L_V 작으면 종 환원" 틀림 | **보유(미수정)** — C1, L916·L931 |
| D-VEQ | eq:Veq 다리 §5 forward-defer 순환 | **수정됨** — L451–456 eq:Veq 가 eq:gxi 1계 미분서 직접 유도(inline), forward 참조 없음 |
| D-DHEFF | χ_d 계수 누락 점프 | **수정됨** — L810–814 −Ω(1−2ξ)→+Ω 흡수 중간식 제시 후 eq:dHeff |
| D-WEFF | 중심기울기 4Fw 다리 누락 | **수정됨** — L566–569 $sF\,dV/d\xi|_{1/2}=4RT-2\Omega$ ↔ $4Fw^\eff$ 등치 명시 |
| D-UBR | eq:Ubranch ansatz(γ·h_η 유도 아님) | **부분 수정** — L498–502 "실측 분기 중심을 방향별 한 자유도로 적으면"으로 현상학적 매개변수화 명시(유도 가장 안 함). KNOWN_DEFECTS 권고 충족 |
| D-VN(minor) | eq:vn 이항 중간식 | **수정됨** — L266–280 (a)(b)(c) 이항 단계 명시 |
| fig:overshoot 오기 | 식번호·분기라벨·byte중복 | **해당 없음/개선** — v8-06 fig:hysloop(L543) 캡션 정상, 신규 fig:doublewell 별도. byte중복 아님(좌표 상이) |
| eyring/bazant/dreyer 미인용 | LOW | **보유** — C2 |

요약: ★D-PEAK 1종 미수정(CRITICAL), 인용 LOW 1종 잔존, 나머지 D-VEQ/DHEFF/WEFF/UBR/VN 전부 수정 확인.

---

## 3. 강점 3 / 약점 3

**강점**
1. 부호 8항 v11 1:1 완벽 — func 본체(L412 V_n, L84 ksi_eq, L96 ln_Lq, L335 A=min, L155 chi_d, L477 charge reversal)와 박스식·signbox·S1–S8 검산이 전부 일치. A=min 의 σ_d 제거+방향은 χ_d 주입(L796–799)까지 코드 주석(L329–331 "원본 버그 정정")과 정합.
2. G-derive 사슬 우수 — 각 박스 (a)출발→(b)연산→(c)중간식≥1→(d)박스 형식 일관. 특히 eq:dUhys(L470–485 artanh 합치는 두 로그 전개)·logistic(L586–603 detailed balance 비)·L_q(L821–835 T_* 묶기)는 학부생 follow 가능(G-follow 1급).
3. G-usable 강함 — L1083 "한 곡선 재현 6단계" keybox + tab:staging(L1026 수치 U=(−ΔH+TΔS)/F 정합 확인 가능)+tab:inputs+tab:nodemap 3표로 "이 문건만으로 코드 작성" 실증. verifybox R1–R4 falsifiable 수치(ΔU_hys=86.7mV @ Ω=12000) 못박음.

**약점**
1. ★C1 D-PEAK 자기모순(최우선) — 본문이 옳은 eq:branch 스위치와 틀린 "매끈한 환원"을 병기.
2. L848–852 ∂lnL_q/∂V 논의가 길고 두 번 반복(§N7 L847–855 + S6 L1139 + R4 L1163) — G-usable 엔 도움이나 약간 장황(중복).
3. C2 인용 누락(LOW).

---

## 4. 차원 점수 (합/35)

| 차원 | 점수/5 | 근거 |
|---|---|---|
| G-derive(유도 완결성) | 4 | 사슬 단계적·우수하나 D-PEAK 환원 논리 1곳 틀림 |
| 배치 보존(v7-11 N0→N9·박스·표) | 5 | 절 순서·결과 박스 9식·식별자·표 3종 보존 확인 |
| 부호 8항 v11 1:1 | 5 | func 본체 전수 대조 완전 일치 |
| G-follow(따라가짐) | 5 | (a)–(d)·중간식·그림 동기 명확 |
| G-usable(재현 가능성) | 5 | 6단계 keybox+3표+falsifiable 수치 |
| 완결성(orphan 0) | 4 | 그림·식 앞도입·뒤사용 양호, 인용 orphan(C2) 감점 |
| 그림(9개·ASCII·\ref) | 3 | 아래 §6 |
| **합** | **31/35** | |

---

## 5. 부호 8항 (v11 1:1, 전수 PASS)

1. U_j=(−ΔH+TΔS)/F, ΔG=−FU — L360 box / py L69 `(-dH_rxn+T*dS_rxn)/F` ✓
2. ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ — L606 / py L86–87 ✓
3. dξ/dV peak 양수·방향불변 — L736 |dξ/dV|=ξ(1−ξ)/w / py L468 ✓
4. ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d — L482/L501 / py L123–138 ✓
5. χ_d 충전 1−χ, ΔH_a^eff=ΔH_a−χ_dΩ — L806/L814 / py L155–159·L149–152 ✓
6. ∂lnL_q/∂V 컷상수라 운영 0(부등식=동기) — L847–852 / py L335 A=min(전이당 상수) ✓ (구분 흐리지 않음, 브리프 §8 준수)
7. 충전 격자역전 ξ[::-1]…[::-1], 충전 dQ/dV 방전거울 양수 — L951 / py L477 ✓
8. V_n=V_app−σ_d|I|R_n, 방전 V_app>V_n — L280 / py L412 ✓ (flowchart 2026-06-29 정정과 일치)

부호 결함 0. (S6 의 "운영 미분 0 vs 부등식 동기" 구분이 v7 계통 결함을 정확히 피함 — 브리프 §3 #8 강조점 충족.)

---

## 6. 그림 평가 (9개)

- 9개 = v7-11 유래 5(spine·staging·hysloop·logistic·reversal) + 신규 4(doublewell·barrier·flux·relaxode), 캡션에 유래 표기됨(브리프 §5 준수).
- 영어 ASCII: 확인 — 내부 라벨 전부 ASCII(filled site/transition state/discharge overshoot 등), 한글 0. 캡션만 한글(허용).
- \ref: 9개 전부 본문 \ref 됨(fig:spine L97, doublewell L421, hysloop L458, barrier L579, flux L595, logistic L689, relaxode L895, reversal L958, staging L219). orphan 0.
- **혼란 위험**: fig:relaxode(L897) 캡션이 C1 의 틀린 "매끈한 환원" 서술을 담아 *그림이 오개념을 강화* — 점수 3 의 주원인. 나머지 8개는 명료. fig:doublewell·fig:barrier·fig:flux 는 유도 동기를 잘 도움(신규 가치 높음).

---

## 7. 체리픽(v8-10) 적합도 — **강후보(조건부), 1순위급**

근거: 부호 8항 완전 1:1, D-VEQ/DHEFF/WEFF/UBR/VN 5종 수정 완료, G-follow·G-usable 최상, 신규 그림 4개 가치. 31/35 로 v8 군 상위 추정.

**조건(체리픽 전 반드시)**: ★C1 D-PEAK 두 문장(L916·L931) 수정. KNOWN_DEFECTS L22 가 "체리픽·최종은 D-PEAK 포함 전부 수정한 유도로"를 명령하므로, **미수정 상태로는 체리픽 불가**. 단 결함이 *국소 2문장*이고 올바른 eq:branch 스위치를 이미 보유하므로 수정 비용 극소 — 수정 후엔 32/35 급 1순위. C2(인용)는 동반 처리 권장.

엄격 판정: 강후보지만 D-PEAK 미수정으로 *현 상태 그대로는 부적합* — "수정 전제 강후보".
