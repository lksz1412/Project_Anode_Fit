# REVIEW_B — v8-10 적대 재검수 (검수 sub, 리뷰 전용)

대상: `Claude/results/v8-10/v8-10.tex` (1205행) + `v8-10.pdf` (21p, A4, 200/100dpi 렌더 판독).
기준: `v8-00_spine/AUTHOR_BRIEF_v8.md` · `v7-00_spine/Anode_Fit_v11_final.py` · `v7-11/v7-11.tex`.
방식: 절 단위 전문 정독 + 9 그림 PDF 렌더 시각 판독 + v7-11 배치 1:1 대조 + 빌드 log 검사.
**자세: refute mandate — "한 번에 OK" 거부. 빈 통과 금지.**

---

## 0. 빌드/형식 사실 (확정)
- xelatex(MiKTeX) 빌드 PASS, 21p PDF 생성. **Overfull hbox 0**(log `grep -c` 확인), undefined/multiply-defined ref **0**, rerun 불요.
- 잔존 경고는 폰트 italic 대체(UnBatang.ttf/D2Coding italic 미정의)뿐 — 한글 italic fallback, ASCII 그림 텍스트 무영향. 결함 아님.
- 그림 9개 \ref↔\label 1:1 (spine 102 / staging 224 / doublewell 427 / hysloop 465 / barrier 585 / flux 601 / logistic 695 / relaxode 901 / reversal 975). **orphan 0**.
- 그림 내부 텍스트 전수 영어 ASCII(렌더 확인) — 한글 깨짐 0. 소스 주석 한글 무해.
- tab:inputs 기본값 ↔ v11 py 대조: z_cut=4.357, A_cap_RT=4.0, w_eff_floor_frac=0.05, grid_pad=0.15, n_work_min=2048, min_lag_grid_steps=2.0, seed_T/I/Q=298.15/0.1/1.0 — **전부 일치**.

## 1. 배치 보존 (G-lens 2) — PASS
v7-11 대조: 결과 박스 11식(eq:vn·Uj·dUhys·Ubranch·wbase·weff·xieq·eqpeak·Lq/Lqfull·LV·dHeff·Acut·chid·peakshape·reversal·sum), 식별자, 부호, 표 4종(staging/inputs/nodemap+symbol longtable), 절 순서 N0→N9, 부호검산 S1–S8 — **변형/누락 0, 유도만 추가**. tab:staging 수치(U/dH/dS/Q/Ω/dH_a/dVdq) v7-11 과 행 단위 동일. eq 번호 1.1–1.x 단조. **이식금지 회귀(D-PEAK 재정정·D-WEFF ¼·s_F orphan) 부재 확인**(s_F 는 헤더 주석에만, 본문 0).

## 2. G-usable 닫힘 (G-lens 3) — PASS (closed)
6단계 재현 박스(keybox L1100) + tab:staging(4전이 전인자) + tab:inputs(기본값) + tab:nodemap(식↔코드) 조합으로 v11 곡선 재현 경로 **닫힘**. 빠진 인자·기본값 오류 미발견. 분기 문턱 ν=2, |I|=c_rate·Q_cell, 충전 격자역전까지 박스에 명시. (참고: 컷점 q_a 의 |dV/dq| 는 표에서 0.30 V 고정값 제공 — 재현 가능.)

## 3. 확정 결함 (심각도·행·내용)

| # | 심각도 | 행 | 내용 |
|---|--------|-----|------|
| B1 | LOW | 920–925, 939–958 | **fig:relaxode 캡션 과적·반직관 미해소.** 캡션이 "차분→미분 수렴 극한은 오히려 L_V≫Δgrid(ρ→1)"이라는 D-PEAK2 반직관 주장을 본문 발췌해 4문장 압축 — 물리적으론 옳고 본문(L939-958)과 정합하나, 그림은 그 영역만 그려 *반대 극한(작은 L_V)이 왜 종으로 안 가는지*는 시각화 못 함. 첫 독자 혼란 위험(혼란 *유발*은 아님, 텍스트로 방어됨). v8-11 권고: 캡션을 "이 그림은 L_V≫Δgrid 영역" 한 줄로 줄이고 반직관 논증은 본문에만. |
| B2 | LOW | 565, 572–573 | **eq:wbase·eq:weff 유도 다리의 s 흡수 무언(silent).** L565 "중심 기울기 dξ_eq/dV|_½=sF/(4RT)"·L573 "sF·dV_eq/dξ|_½=4RT−2Ω 와 4Fw^eff 를 같다고" — 검산상 대수 정확(s=σ=+1 흡수). 그러나 logistic 측 "4Fw^eff"가 어떻게 sF·4w^eff 인지(s=1 흡수)를 명시 안 해, 학부생이 s 인자 추적에서 1회 비약 느낌. (b)(c) 중간식 1줄 추가 권고. |
| B3 | NOTE | 793–796 | **z_cut=4.357 의 "5% 컷" 유도가 (b)(c)에서 서술로만.** "logistic 미분 종의 5% 폭이 중심에서 ±z_cut·RT/F 규모라 𝒜=z_cut·n·RT" — 수치 4.357 이 5%에서 어떻게 나오는지(ln 역산)는 닫지 않고 단언. 브리프 §3-8 은 이 식을 "전이당 상수"로만 요구(유도 의무 아님)하므로 결함 미만이나, G-derive 완결성 관점 가장 약한 유도 한 곳. |

**부호 사슬 8항 + 회귀 5항(R1–R5): 전건 PASS.** R5(D-PEAK 꼬리 극한 ρ 부호)·R4(L_q 동결 vs 부등식) 신규 falsifiable 항 정합. ∂lnL_q/∂V 3회 등장(L855 본문 실질 + S6 + R4)은 검산절 설계상 정당 layering — **중복 서술 아님**(브리프 우려 회피됨).

## 4. 그림 9개 시각 판독 (G-lens 4) — 혼란 그림 무

- **신규 4개 식-정합 확인**: doublewell(p9, Ω=3RT: ξ_s=0.2113/0.7887 ↔ u=√(1/3)=0.577 정합, 이중웰·g''<0 음영 정확) / barrier(p12, (a)등높이 (b)peak down by χA·ΔG_a−χA·A 화살표 정합 eq:bv) / flux(p13, r⁺(1−ξ)↓·r⁻ξ↑ 교점 ξ_eq=2/3@A>0·½@A=0 정확) / relaxode(p16, target/lagged/r 갭 명확). **혼란 유발 그림 없음**(기존 v3–v6 문제 그림 재사용 0 확인).
- 기존 5개(v7-11 유래) 보존: spine/staging/hysloop/logistic/reversal — 캡션에 "v7-11 유래" 정직 표기.

## 5. 이음새·시각 (G-lens 5) — PASS
체리픽 이음새(v8-06b 베이스 + 신규 4그림 + D-PEAK2) 텍스트 단절 없음. 절 도입/마무리 다리 존재(예 L313-314·L382-383·L755-756). 수식 주도·괄호 전보체 회피 양호. 표 오버플로 0(longtable·tabular 모두 페이지 내). 헤더 \thepage/\pageref{LastPage} 21/21 수렴.

---

## 가장 약한 3곳 (refute 우선순위)
1. **fig:relaxode 캡션(B1)** — 반직관 D-PEAK2 논증을 캡션에 과적, 그림이 그 핵심(작은 L_V 비수렴)을 못 보여줌. 9그림 중 유일한 "텍스트가 그림을 앞지른" 자리.
2. **z_cut=4.357 유도(B3)** — 9 유도 사슬 중 닫힘이 가장 약함(수치 역산 미제시, 서술 단언).
3. **eq:weff s-흡수 다리(B2)** — logistic↔비단조 등온선 기울기 매칭의 s=1 흡수가 무언.

## v8-11 보완 권고
- (권장) B1: relaxode 캡션 2–3문장으로 축약, 반직관 논증은 본문 L939-958 에 일임.
- (선택) B3/B2: z_cut 5%→4.357 1줄 역산, eq:weff 의 4Fw^eff=sF·4w^eff(s=1) 중간식 1줄.
- 위 3건 모두 **LOW/NOTE** — 정확성·배치·G-usable·부호·빌드에 결함 없음. v8-11 은 정확성 수정이 아니라 *가독 다듬기* 성격.

**판정: 확정 결함 0(HIGH/CRITICAL), LOW 2 + NOTE 1. 한 번에 OK 가능하나, B1 1건은 v8-11 가독 보완 가치 있음.**
