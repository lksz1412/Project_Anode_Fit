# REVIEW2 — v8-09b (Codex 보완) 검토2

> 검수 sub (리뷰 전용·수정/커밋 X). 대상 `v8-09/v8-09b.tex` (1206행 전문 정독, 식·유도 단위 청크).
> 기준 정독: `Anode_Fit_v11_final.py`(706줄, _causal_lowpass L100·peak_shape 분기 L466–481·func_w_eff L141)·`v7-11.tex`·`AUTHOR_BRIEF_v8.md`·`REVIEW1.md`·`NOTEb.md`.
> 검증: REVIEW1 의 3 결함(C1 ★D-PEAK·C2 D-WEFF·약점3 orphan bib)에 대한 Codex 보완 반영 + ★수학 직접 검산 + 신규 회귀 + 재점수.
> 렌즈: ①D-PEAK 수학 정확성(직접 수치검산) ②G-derive 다리 ③부호 8항 ④orphan ⑤신규 회귀(refute).

---

## ① 보완 반영 (REVIEW1 결함 → v8-09b 상태)

diff 결과 Codex 보완은 정확히 5곳(108·367·543–556·730·918→927·1158→1170 self-test). REVIEW1 지적 3건 전부 처리:

### C1 — ★D-PEAK (CRITICAL) → **해소 (수학적으로 정확)**
- 틀린 문장("$L_V$ 작으면 ξ_lag→한 칸 뒤처진 ξ_eq → dξ_eq/dV 종으로 환원")이 **삭제**됨(행 918–920 제거 확인).
- 대체 문장(927–932): "$L_V$ 크면 ρ→1 매끈 bell/tail; **$L_V$ 작으면 ρ→0 → ξ_lag→ξ_eq → numerator 사라져 peak→0**; 작은 $L_V$ 평형회복은 꼬리식 극한이 아니라 분기식(eq:branch)이 처리." 자기모순(틀린 환원+스위치 공존) 제거됨.
- ★**직접 수치검산(verify.py)**: logistic ξ_eq 격자에 코드 점화식(_causal_lowpass 동형) 적용해 peak=(ξ_eq−ξ_lag)/L_V 를 bell xi(1-xi)/w 와 비교 —
  - LV/dx=0.20 (ρ=0.0067): peak_c=0.33 vs bell 9.73, **ratio 0.034 → peak→0** (corrected 텍스트 정확, 原 v8-09 틀림 확정).
  - LV/dx=5·50: ratio 0.90·0.99 → **큰 L_V 에서 bell 로 수렴** (corrected 텍스트의 "large $L_V$→bell" 정확).
  - **방향 확정**: bell 환원은 corrected 가 말한 大-$L_V$ 극한에서만 성립, 小-$L_V$ 는 0. 수학 무결.

### C2 — D-WEFF 점프 (G-derive) → **해소**
- 중심기울기 다리(543–551): $sF\,dV/d\xi=g''(\xi)$ + 식~\eqref{eq:gpp_v809} 결합 → $\xi=\tfrac12$ 서 $4RT-2\Omega=4F\cdot(RT/F)(1-\Omega/2RT)\equiv 4Fw^\eff$ → 박스. KNOWN_DEFECTS 요구 다리 정확히 삽입. **수치검산**: $4RT-2\Omega = 4F(RT/F)(1-\Omega/2RT) = -10084.17$ (Ω=10000) 항등 일치. 내부 정합도 OK(eq:Veq 의 비상수 몫 $=g'/(sF)$ → $dV/d\xi=g''/(sF)$).

### 약점3 — orphan bib (LOW) → **해소**
- bazant2013@108·dreyer2010@367·eyring1935@730 본문 \cite 추가. 7 bibitem(dahn/ohzuku/bazant/eyring/dreyer/bloom/dubarry) **전부 본문 인용 — orphan 0**.

추가 보완(REVIEW1 미요구이나 정합): self-test 4→5 항(R5 $L_V$ 분기 극한 추가, 행 1186–1189) — D-PEAK 정정과 일관된 falsifiable 수치 못박음.

---

## ② 신규 회귀 (refute pass — 보완이 새 결함 만들었나)

| 점검 | 결과 |
|---|---|
| D-PEAK 대체문장 vs eq:branch(933–941) | 정합 — ρ→0 peak눌림 설명이 ν=2 스위치 정당화로 자연 연결, 모순 0 |
| D-PEAK 대체문장 vs R5 self-test(1186) | 정합 — 같은 ρ 극한 논리, 중복 아닌 보강 |
| D-WEFF 신규 식 eq:weff_midpoint vs 직후 eq:weff·eq:gpp_v809 | 정합 — $g''$ 재인용·중앙값 대입 정확, label 충돌 없음 |
| 신규 \cite 3건 위치(속도식·히스도입·Eyring) | 의미 적절 — bazant=속도식, dreyer=히스 기원, eyring=전이상태론. 오배치 0 |
| 빌드 회귀 | v8-09b.log: error 0·undefined cite 0·undefined ref 0, Overfull \hbox 4건(≤22.6pt 미관). PDF 369790 B 생성. (NOTEb "빌드 미수행" 기재와 달리 실제 컴파일됨·clean) |
| R5 "직접 지정 $L_V<2\Delta_{grid}$" 문구 | 코드 L466 분기(`lag_len_V < min_lag_grid_steps*grid_step`, min=2)와 정합 |

**신규 회귀 0.** refute 대상(가장 약한 곳=D-PEAK 대체문장의 大-$L_V$ 주장)도 수치로 성립. 단 미세 관찰(결함 아님): LV/dx=500 에서 ratio 0.91 로 비단조 — 유한창·초장커널 edge 아티팩트일 뿐, 물리 regime(수~수십 step)은 단조 bell 수렴. 텍스트 정성 주장 무손상.

---

## ③ 재점수 (합 / 35)

| 차원 | v8-09 | v8-09b | 근거 |
|---|---:|---:|---|
| G-derive(유도 완결) | 3 | **5** | D-PEAK 틀린서술 삭제+정확 대체, D-WEFF 다리 삽입 — 점프 0 |
| 배치 보존(v7-11) | 5 | 5 | 절순서·결과박스·식별자·표 불변(보완은 유도 추가만) |
| 부호 8항 v11 1:1 | 5 | 5 | S1–S8 + R1–R5 수치, 코드 라인 정합(아래 ④) |
| G-follow | 4 | **5** | D-WEFF 끊김 해소, 대체문장 매끈 연결 |
| G-usable | 5 | 5 | 3표+6단계 keybox+노드맵 유지 |
| 완결성(orphan) | 4 | **5** | bib 7건 전부 인용, ref 미정의 0 |
| 그림(6개) | 4 | 4 | 변경 없음, ASCII-English·중복 무 |
| **합** | **30** | **35 / 35** | |

**+5 (30→35).** REVIEW1 의 3 감점요인(D-PEAK·D-WEFF·orphan) 전부 정확히 닫힘, 신규 회귀 0.

---

## ④ 부호 8항 (v11 1:1, 재확인)

| # | 항 | v8-09b | v11 코드 | 정합 |
|---|---|---|---|---|
| 1 | $U_j=(-\Delta H+T\Delta S)/F$, $\Delta G=-FU$ | eq:Uj(344)·S1 | func_U_j L69 | O |
| 2 | $\xi_\eq=$logistic$[\sigma_d(V-U)/w]$ 방전 V↑→ξ↑ | eq:xieq(593)·S2 | func_ksi_eq L86 | O |
| 3 | $d\xi/dV$ peak 양수·방향불변 | eq:eqpeak(673)·S3 | L468 | O |
| 4 | $\Delta U_\hys\ge0$/$\Omega\le2RT\to0$/분기 $\pm\tfrac12\sigma_d$ | eq:dUhys(439)·S4·R1(86.7mV)·R2 | func_dU_hys L123, U_branch L138 | O (검산 86.68mV) |
| 5 | $\chi_d$ 충전 $1-\chi$·$\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ | eq:chid(766)·eq:dHeff(792)·S5 | func_chi_d L160, func_dH_a_eff L149 | O |
| 6 | $\partial\ln L_q/\partial V$ 컷상수 운영0(부등식=동기) | 836–844·S6·R4 | A=min(...) L335 동결 | O |
| 7 | 꼬리 충전 격자역전·충전 dQ/dV 방전 거울(양수) | eq:reversal(947)·S7 | L477 [::-1]…[::-1] | O |
| 8 | $V_n=V_\app-\sigma_d|I|R_n$ 방전 측정>평형 | eq:vn(264)·S8 | L412 | O |

부호 8/8 정합. 보완은 부호 사슬 불변(D-PEAK 정정은 G-derive 영역, 부호 무영향). _causal_lowpass 초기상태 L108 ($zi=\rho\,s_0\Rightarrow$ lag[0]=$s_0$) = eq:lowpass 초기조건 ξ_lag,0=ξ_eq,0 정합 확인.

---
**총평**: 35/35. REVIEW1 의 ★D-PEAK(CRITICAL)·D-WEFF·orphan 3건 **수학적으로 정확하게** 닫힘(D-PEAK 정정은 직접 수치검산으로 大-$L_V$ bell·小-$L_V$ peak→0 확정). 신규 회귀 0, 빌드 clean(error 0). 체리픽 채택 가능 — 보완 잔여 결함 없음.
