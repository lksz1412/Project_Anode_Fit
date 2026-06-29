# REVIEW2 — v8-06b 적대 검수 2 (검수 sub, 리뷰 전용·최엄격·체리픽 1순위 후보)

> 대상 `v8-06b.tex` (1196행) 전문 정독(3청크 + D-PEAK·서지 자리 정밀 재독).
> 기준 직접 대조: `Anode_Fit_v11_final.py`(func_w/U_j/ksi_eq/L_q/_causal_lowpass/
> dU_hys/U_branch/chi_d/dH_a_eff + dqdv L406–484 분기·역전 본체), `v7-11.tex`,
> `AUTHOR_BRIEF_v8.md`(§3 11식·§7 부호 8항) 전문, REVIEW1.md(C1·C2 추적).
> 수학 직접 검산: D-PEAK ρ 두 극한·(ξ_eq−ξ_lag)/L_V 수렴·R1/R2/weff/U/z_cut 수치.
> 빌드: scratchpad 청정 3-pass xelatex 재실행(아래 §2 신규 회귀).
> refute mandate·가장 약한 3곳·빈 통과 금지 적용.

---

## ① 보완 반영 (REVIEW1 C1·C2 → v8-06b 마감 검증)

### ★C1 D-PEAK 정정 — **완전 해소·수학 정확(직접 검산)**
REVIEW1 이 ``틀림''으로 못박은 두 문장이 **둘 다 제거·재서술**됨:
- **fig:relaxode 캡션(L915–921)**: 오개념 제거됨. 신 캡션 = ``매끈한 차분이 미분으로 수렴하는 극한은 **오히려 L_V≫Δgrid(ρ→1)** '' + ``작은 L_V 평형 회복은 매끈한 차분의 극한이 아니라 **코드의 분기 스위치(eq:branch)** 가 담당해 평형 종(eq:eqpeak)으로 직접 떨어뜨린다''. → **그림이 오개념을 강화하던 REVIEW1 §6 핵심 감점 사유 소멸**(그림이 그리는 영역 = ρ→1 명시).
- **§peak_shape 본문(L934–939)**: ρ 두 극한을 부호 대비로 재서술 — L_V≫Δgrid ⇒ ρ→1(진짜 1차 저역통과, 평형 종+꼬리) / L_V→0 ⇒ ρ→0 ⇒ ξ_lag→ξ_eq(같은 칸, 한 칸 지연 아님) ⇒ **0/0 — 종으로 매끈히 환원 안 됨**. 작은 L_V 환원은 eq:branch(L_V<νΔgrid) 귀속. **자기모순 제거 확인**.

**수학 직접 검산(반증 시도)**: `_causal_lowpass` L105 `decay_per_step=exp(-grid_step/lag_length)` 코드 본체로 — L_V=1e-9 → ρ=0.0000(같은 칸), L_V=1e3 → ρ=1.0000. 또 logistic ξ_eq 에 점화식 저역통과 적용해 `(ξ_eq−ξ_lag)/L_V` 를 직접 계산: ρ↑(L_V↑)일수록 면적→~1(미분 적분과 일치), peak 최대가 중심에서 **고전위 쪽으로 이동(+0.0005→+0.038 V)** — 곧 ``평형 종+꼬리''(비대칭)이지 대칭 평형 종(eq:eqpeak)이 **아님**. 정정 문구 ``평형 종에 꼬리를 더한 모양''이 정확. **반증 실패 = 정정 PASS**.

### C2 orphan bib — **완전 해소**
`\cite` 5개소(L91 bloom/dubarry, L92 dahn/ohzuku, L385 dreyer2010, L580 eyring1935, L581 bazant2013) — 7키 전부 `\bibitem`(L1186–1192) 존재. 자리 의미 정합: dreyer2010=§hys 도입(히스 열역학 기원), eyring1935=Eyring 속도식 출발, bazant2013=eq:bv 비대칭 장벽 분해. `.aux` `\bibcite` 7키 전부, undefined citation 0. **orphan 0**.

### VEQ·DHEFF·WEFF·UBR·VN 유지 확인 — 전부 보존(회귀 없음)
- D-WEFF: L568 `sF dV_eq/dξ|_½=4RT−2Ω` ↔ `4Fw_eff` 등치 → eq:weff. **대수 직접 검산 일치** `(4RT−2Ω)/4F≡(RT/F)(1−Ω/2RT)`.
- D-VEQ(L452–456): eq:gxi 1계 미분서 V_eq 직접, forward 참조 없음 — 유지.
- D-DHEFF(L811–815): −Ω(1−2ξ)→깊은 꼬리 +Ω 흡수 중간식 → eq:dHeff — 유지.
- D-UBR(L499–502): 현상학적 한 자유도 매개변수화 명시 — 유지. D-VN(L266–280): (a)(b)(c) 이항 — 유지.

---

## ② 신규 회귀 (보완 편집이 새로 만든 결함) — **N0 (내용)·N1 (빌드 위생, LOW)**

- **내용 회귀 0**: D-PEAK 정정·3 인용·R5 추가는 모두 가산(삭제·치환이 인접 식/번호/그림 깨뜨림 없음). eq 라벨 46개·fig 라벨 9개 전부 `\ref` 1:1(orphan 0). S1–S8·R1–R4 무변경 정합. 부호 8항 무회귀(③).
- **N1 (LOW, 빌드 위생)**: 동봉 `v8-06b.log`(반영본 빌드)는 **마지막 패스 tail 에 `Label(s) may have changed. Rerun to get cross-references right.` 1건 잔존** — 곧 *동봉 PDF 는 2-pass 산출로 교차참조 최종 정착 1패스 부족 가능*. 단, `.aux` `\newlabel` 69개·`\bibcite` 7키 모두 기록되어 ref/cite 자체는 정의됨. **청정 환경 3-pass 재빌드 직접 수행 → PASS 3 에서 ``Rerun'' 0건·undefined ref/cite 0·21p 수렴 확인**. 즉 문건은 3-pass 로 완전 청정하나, *동봉 로그가 3rd pass 를 캡처하지 못함*(NOTEb §6 ``+3rd'' 주장과 동봉 로그 불일치). 잔여 경고 = 한글 폰트 italic 폴백 3건(UnBatang/D2Coding, cosmetic). → **권고: 3-pass 로 재빌드해 PDF·log 교체**(내용 무관, 위생).

---

## ③ 부호 8항 (v11 1:1, 전수 PASS — 무회귀)

1. U_j=(−ΔH+TΔS)/F, ΔG=−FU — L360/L1137 ↔ py L69 ✓ (수치: staging 4행 U_tab↔computed <3mV 전부 일치)
2. ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ — L607/L1139 ↔ py L86–87 ✓
3. dξ/dV peak |·|≥0 방향불변 — L737/L1141 ↔ py L468 ✓
4. ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d — L482/L502/L1143 ↔ py L78–81·L127–130 ✓ (R1 수치 86.68mV↔doc 86.7 ✓, R2 2RT=4957.9↔4958 ✓)
5. χ_d 충전 1−χ, ΔH_a^eff=ΔH_a−χ_dΩ — L807/L815/L1145 ↔ py L160·L152 ✓
6. ∂lnL_q/∂V 컷상수라 운영 0(부등식=동기) — L848–853/L1147 ↔ py L335 A=min(전이당 상수) ✓ (v7 계통 결함 회피 — 브리프 §3#8 충족)
7. 꼬리 충전 격자역전 ξ[::-1]…[::-1], 충전 dQ/dV 방전 거울(양수) — L959/L1151 ↔ py L477 ✓
8. V_n=V_app−σ_d|I|R_n, 방전 측정>내부 — L280/L1153 ↔ py L412 ✓

**부호 결함 0.** S6 ``운영 미분 0 vs 부등식 동기'' 구분 유지 — 정확.

---

## ④ 잔여 결함 전수 (체리픽 베이스 최엄격 — 약한 3곳 명시)

| # | 위치 | 등급 | 내용 |
|---|---|---|---|
| W1 | 동봉 `v8-06b.log`/PDF (빌드 위생) | LOW | 동봉 로그 tail ``Rerun'' 잔존 = 2-pass 캡처. 3-pass 재빌드 시 청정(직접 확인). PDF·log 교체 권고. **내용 무결**. |
| W2 | L934 본문 문구 | LOW(polish) | ``이 차분이 매끈한 미분 dξ_eq/dV 로 수렴'' → 엄밀히는 ξ_lag(비대칭 인과 커널)의 차분이라 *평형 종+꼬리*(비대칭, 검산: peak 고전위 이동)로 가지 대칭 dξ_eq/dV 종이 아님. L936 이 ``평형 종에 꼬리를 더한 모양''으로 바로 보정하므로 오류는 아님. 한 문장 안 ``미분 수렴''과 ``종+꼬리'' 병기가 미세 압축. |
| W3 | L848–855 + L1147 + L1172 (∂lnL_q/∂V) | LOW | REVIEW1 약점2 잔존 — 같은 ``운영 0 vs 동기'' 논의 3회 반복(N7·S6·R4). G-usable 엔 도움이나 약간 장황. 결함 아님. |

**부호 8항·G-derive 11식·G-usable·그림 9개에서 CRITICAL/HIGH 0.** D-PEAK 정정으로 REVIEW1 의 유일 CRITICAL(C1) 소멸. C2 소멸.

### G-derive 11식 (a→b→c→d 사슬) 전수 — 전부 충족
U_j(eq:Uj)·w_j(eq:wbase)·ξ_eq logistic(eq:xieq, detailed balance 비)·평형 peak(eq:eqpeak, 종 항등식)·ΔU_hys(eq:dUhys, spinodal→artanh)·분기중심(eq:Ubranch)·L_q(eq:Lqfull, T_* 묶기)·컷 𝒜(eq:Acut)·ΔH_a^eff(eq:dHeff)·L_V/인과 꼬리(eq:peakshape, 적분인자 일반해→이산 저역통과)·합산(eq:sum). **점프(``대입하면 박스'') 없음.** z_cut=4.357 검산: 5%-of-deriv-peak 컷에서 z=4.357 정확 재현(반증 실패).

### G-usable — 최상 유지
L1091 ``한 곡선 재현 6단계'' keybox + tab:staging(수치 정합 검산 가능)·tab:inputs·tab:nodemap 3표 + verifybox R1–R5 falsifiable 수치. R5 신규(D-PEAK 회귀)가 ρ 두 극한 부호 대비를 반증 가능 항으로 못박아 회귀 방어.

### 그림 9개 — orphan 0·ASCII·정합. **fig:relaxode 재평가 = 정상화**
9개(v7-11 유래 5 + 신규 4) 전부 `\label`+`\ref` 1:1. 내부 라벨 ASCII(캡션만 한글). REVIEW1 의 fig:relaxode 오개념 강화 문제 **해소** — 캡션이 이제 그리는 영역(L_V≫Δgrid)을 정확히 명시하고 작은 L_V 는 분기 스위치로 귀속. → **그림 차원 3→4 상향**.

---

## 재점수 /35

| 차원 | REVIEW1 | REVIEW2 | 근거 |
|---|---|---|---|
| G-derive(유도 완결성) | 4 | **5** | D-PEAK 환원 논리 정정 — 11식 사슬 전부 정확(수치 검산 통과) |
| 배치 보존(N0→N9·박스·표) | 5 | 5 | 무변경 보존 |
| 부호 8항 v11 1:1 | 5 | 5 | 전수 대조 일치(무회귀) |
| G-follow | 5 | 5 | (a)–(d)·중간식·그림 동기 명확 |
| G-usable | 5 | 5 | 6단계+3표+R1–R5 falsifiable(R5 신규) |
| 완결성(orphan 0) | 4 | **5** | 인용 orphan(C2) 해소 — eq/fig orphan 0 |
| 그림(9개) | 3 | **4** | fig:relaxode 오개념 제거(정상화). W1 빌드위생 −1 보류 |
| **합** | **31/35** | **34/35** | |

(그림 5점 유보 사유 = 폰트 italic 폴백 cosmetic 잔존만; 내용은 만점급.)

---

## ⑤ 체리픽 베이스 적합도 + 잔여 보완점

**판정: 체리픽 1순위 — 적합(무조건). 34/35, v8 군 최상위 추정.**

근거: REVIEW1 의 유일 차단 사유였던 ★C1 D-PEAK(CRITICAL) **수학적으로 정확히 정정**(직접 검산 통과·반증 실패), C2 orphan **해소**, VEQ/DHEFF/WEFF/UBR/VN 5종 **회귀 없이 유지**, 부호 8항 v11 1:1 **무회귀**, G-derive 11식 전부 점프 없이 검산 통과, G-usable 최상(R5 회귀 추가로 강화), 신규 그림 4개 가치, fig:relaxode 정상화. KNOWN_DEFECTS L22 ``체리픽·최종은 D-PEAK 포함 전부 수정'' 조건 **충족** — 현 상태 그대로 체리픽 가능.

**잔여 보완점(체리픽 채택 시 권장, 전부 LOW·비차단)**:
1. **W1 (위생)**: 동봉 PDF·log 를 3-pass 재빌드본으로 교체(``Rerun'' 잔존 제거 — 내용 무관). 가장 우선.
2. **W2 (polish)**: L934 ``매끈한 미분 dξ_eq/dV 로 수렴'' 한 마디를 ``평형 종+꼬리(비대칭)로 수렴''로 다듬으면 L936 과 완전 일치(미세).
3. **W3 (간결)**: ∂lnL_q/∂V 3회 반복(N7·S6·R4) 중 R4 를 한 줄로 축약 가능(선택).

세 항 모두 내용 무결성·체리픽 적합 판정에 영향 없음 — 체리픽 후 정리 권장 수준.
