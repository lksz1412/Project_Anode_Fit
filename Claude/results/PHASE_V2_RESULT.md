# Phase V2 — 흑연 평형 브로드닝(②③) 검증 + M-factor 제거 근거 Result

## Summary
흑연 반쪽셀 near-equilibrium 실측(Zenodo 20086298 pseudo-OCV ~C/50, 상온, 2셀)에 대해 **문건 출하 코드**(`Anode_Fit_v1.0.23.py` `GraphiteAnodeDischargeDQDV.equilibrium`)의 평형 브로드닝식을 정량 대조했다. 결과: **문건 §7 물리가 실측으로 확인**된다 — 실측 near-equilibrium 피크는 두-상 near-delta(FWHM 3.5–4.0 mV = 0.14–0.16·RT/F)이고, 문건의 자유폭 `w_j`(=②⊗③ 흡수)로 4피크 **위치·높이**를 단일 정합셋으로 재현(R²=0.951/0.946, 2셀 일치). 이는 **M-factor 제거 근거의 평형 부분을 실증**한다: dV/dQ 높이 불일치는 전위축 stretch(M)가 아니라 dQ/dV 폭 `w_j` 로 설명된다. 반면 **출하 기본값**(n=1 → w=RT/F≈25.7 mV)은 실측 대비 ~20× 과대폭이라 4스테이징을 한 봉우리로 뭉갠다(기본값=placeholder 규정 정합, 그러나 out-of-box 곡선은 비현실적으로 넓음 — 추가 후보).

## Step Range
Cumulative **8–12** (V1 5–7 이어).

## Inputs
- 실측: `zenodo_gr/gr_pocv_1d5628.parquet`·`gr_pocv_4ccc47.parquet`(스크래치, 원자료).
- 모델: `docs/v1.0.23/Anode_Fit_v1.0.23.py` — `GraphiteAnodeDischargeDQDV.equilibrium`(L528–545)·`func_ksi_eq`(L99–102)·`func_w`(L91–94)·`_width`/`_n_factor`(L360–389)·`GRAPHITE_STAGING_LIT`(L1027–1056).
- 근거 절: `_sections/ch1_sec07_broadening.tex`(두-상 near-delta·폭예산 σ_sym²·w_j 자유폭 규정).

## Files Created
- `results/comp_v24/v24_graphite_fit.py`(출하 equilibrium() 직접 호출 curve_fit — 4전이 U_j·w_j·Q_j+Cbg).
- `results/comp_v24/gr_fit.png`(real vs 문건-FIT vs shipped-default, 2셀×2패널).
- `results/comp_v24/gr_fit_result.json`(피팅 수치 2셀).
- `results/comp_v24/v24_graphite_dva.py`·`gr_dva_Mremoval.png`(DVA 관점 M 제거 직접 시연).
- (V1→V2 이월) `results/comp_v24/v24_graphite_firstlook.py`·`gr_firstlook.png`(육안 대조).

## Files Updated
- (없음 — 검증 phase. 코드·문건 무수정.)

## Read Coverage
- `equilibrium`·`func_ksi_eq`·`func_w`·`_width`·`_n_factor`·`GRAPHITE_STAGING_LIT` 전문 정독(피팅 대상 파라미터화 정확 반영: 'n' 미부여·'w'만 부여 → `_width`가 정확히 w_j 반환).
- 실측 2 parquet 로드·스테이징 창 점밀도(48.7 pts/mV) 확인.

## Execution Evidence
**(1) 실측 near-equilibrium 피크 직접 측정**(경량 savgol, delith):
| 피크 V | 높이(mAh/V) | FWHM | FWHM/(RT/F) | 귀속 |
|---:|---:|---:|---:|---|
| 0.104 | ~201 | 3.5 mV | 0.14 | 2→1 (LiC₁₂↔LiC₆) 두-상 |
| 0.1415 | ~98 | 4.0 mV | 0.16 | 3→2L 두-상 |
| 0.227 | ~16.5 | ~8 mV | ~0.31 | 4→3 (약) |
→ **두-상 전이는 near-delta**(FWHM ≪ RT/F). 문건 §7 예측과 정합. (점밀도 48.7 pts/mV → 해상은 데이터 아닌 평활 선택이 지배 = 실측 자체가 매우 sharp.)

**(2) 문건 출하식 정량 피팅**(2셀 일치):
| 전이 | U_fit(V) | w_fit(mV) | w/(RT/F) | 높이(fit) | 높이(real) |
|---|---:|---:|---:|---:|---:|
| A | 0.227 | 1.6 | 0.06 | 17.5 | 16.5 |
| B | 0.1415 | 0.9 | 0.036 | 90.6 | 98 |
| C | 0.104 | 0.8 | 0.031 | 209 | 201 |
| D(shoulder) | 0.140 | 18.4 | 0.72 | 11.3 | — |
- R² = **0.951**(cell_1d5628) / **0.946**(cell_4ccc47). 두 셀 U_fit·w_fit 거의 동일(재현성 강).
- 두-상 3피크 w/(RT/F)=0.03–0.06(near-delta) + solid-solution shoulder 1개 w/(RT/F)=0.64–0.72. **폭 예산 σ_sym² 의 두 극한(두-상 sharpening vs 열적 nRT/F)이 실측에 공존**.

**(3) M-factor 제거(DVA 관점)**:
- dV/dQ 골(valley) 깊이 = 1/(dQ/dV 피크 높이). 문건-FIT dV/dQ(**M 없음**)가 실측 dV/dQ 골 위치·깊이(최저 ~5 mV/mAh)를 재현.
- 출하 기본(w=RT/F, 과대폭)은 dQ/dV 피크가 낮아(~17) dV/dQ 골이 ~54 mV/mAh 로 **~11× 부풀음** = 사용자가 M 넣던 상황 재현.
- **결론(평형 한정)**: dV/dQ 높이 불일치 = dQ/dV 폭 문제. 올바른 w_j 로 맞추면 M 불필요.

## Validation
| 게이트(V2) | 판정 | 근거 |
|---|---|---|
| 실측 두-상 near-delta 확인(§7) | PASS | FWHM 3.5–4 mV = 0.14–0.16·RT/F 직접 측정 |
| 출하식 위치·높이 재현(단일 정합셋) | PASS | R²=0.95, 높이 209/90.6/17.5 ≈ real 201/98/16.5 |
| 2셀 재현성 | PASS | U_fit·w_fit 셀간 일치(<3% 편차) |
| M 제거 근거(평형) | PASS | FIT dV/dQ(M無)가 real 골 재현·default는 11× 부풀음 |
| 폭 예산 두 극한 공존 | PASS | 두-상 w/RTF 0.03–0.06 + shoulder 0.64–0.72 |
| 출하 **기본값** 현실성 | **CONDITIONAL** | n=1(w=RT/F) out-of-box 곡선 ~20× 과대폭(placeholder 규정 정합이나 오도 소지 — 추가 후보) |

## Gate
**PASS.** 흑연 평형 브로드닝(②③) 검증 완료 — 문건 §7 물리·M 제거 근거(평형 부분) 실측 확인. 한계: 공개데이터=상온·C/50 → **율①·다온도 축은 미검증**(사내 필요, V3 이후).

## Confirmed Non-Changes
- 코드·문건 무수정(검증 phase만). v1.0.23 불가침·bit-exact 보존.
- 원자료 원본 미변조(읽기 전용).
- 피팅은 출하 `equilibrium()` **직접 호출**(재구현 프록시 아님) — 문건 코드 자체를 검증.

## 추가 후보 (실행 X — 사용자 결정 대상)
1. **기본값 현실성**(CONDITIONAL 게이트): `GRAPHITE_STAGING_LIT` 는 `'n':1.0`+`'w'`(폴백) 병기 → 실제 사용폭 = w=RT/F 로 ~20× 과대. (a) 두-상 전이에 피팅형 seed(w≈1–2 mV) 를 기본화, (b) 두-상(near-delta)/solid-solution(nRT/F) 구분 플래그 도입, (c) 문건에 "기본 w=RT/F=상한 placeholder, 실사용 시 w_j 피팅 필수" 경고 강화. 셋 다 사용자 결정.
2. **평형 피크 비대칭**: 실측 피크에 약한 비대칭 잔차(R² 0.95↔0.99 격차). 문건의 L_V 비대칭 꼬리는 유한율 항(평형=0)이라 평형에선 미가용 → 평형 비대칭 파라미터 신설은 L_V 와 물리 중복 위험 → 도입 시 사용자 결정.
3. **율①·다온도 검증**: 공개데이터 부재. V3(율 시리즈)·V4(T/I/V 통합)은 사내 실행 스크립트 패키지로 준비(반출 불가 준수).
4. **히스/방향**: 실측 delith 0.104 vs lith 0.077(~27 mV 히스) 관측 — 문건 U^d 분기중심(σ_d) 대상. 평형 폭과 분리 검증 항목(V4).
