# v7-06 자체검수 로그 (NOTE)

> 산출 = `v7-06.tex` (자족, v5 계열 preamble) + `v7-06.pdf` (15p). 독립 작업(9건 경쟁 중 1건).
> 절 순서 = v11_flowchart spine N0→N9. 수식 주도(v5 형식)를 v11_final.py 코드 진행에 arrange.

## ① Read Coverage (전문 정독 행범위)

| 입력 | 행범위 | 정독 |
|---|---|---|
| `v7-00_spine/AUTHOR_BRIEF.md` | 1–75 (전문) | head→tail, 권위 사양 |
| `v7-00_spine/v11_flowchart.md` | 1–90 (전문) | head→tail, spine·부호규약·노드매핑 |
| `v7-00_spine/Anode_Fit_v11_final.py` | 1–706 (전문) | head→tail. 핵심: func_w(64)·func_U_j(68)·func_U_j_hys(72)·func_ksi_eq(84)·func_L_q(90)·_causal_lowpass(100)·func_dU_hys(123)·func_U_branch(133)·func_w_eff(141)·func_dH_a_eff(149)·func_chi_d(155)·_resolve_lag_length(307)·equilibrium(354)·dqdv(374)·curve(487)·GRAPHITE_STAGING_LIT(535) |
| `docs/graphite_ica_ch1_Opus_v5.tex` | 1–1883 (전문, 4구간) | head→tail. 형식·유도깊이·eq 라벨 출처. v6 미사용(브리프 지시). |

## ② 라운드별 결함 추이 (자체 10R, 청크·렌즈 전환)

| R | 청크 스킴 | 렌즈 | 발견·조치 |
|---|---|---|---|
| 빌드0 | 통독 | 컴파일 | `\func{}` 오타 2건(L380 U_branch·L446 w) → `\code{...}`/inline math 로 수정 |
| 빌드0b | 통독 | 렌더 폰트 | `✓` 8건 lmroman 미보유 → `$\checkmark$`(amssymb) 치환 |
| R1 | 통독 | 구조·spine 정합 | 절 순서 §1(N0)→§9(N9)→§10 부호검산 = flowchart N0→N9 일치. 결함 0 |
| R2 | 식별 (식-by-식) | 물리·부호 적대검산 (코드 대조) | func_L_q(L90–97) ↔ eq:Lqfull 전 항 일치(T_attempt=T_*, dG_a=ΔH^eff−TΔS, −x·A/RT). 결함 0 |
| R3 | 라인 | ∂lnL_q/∂V 부호 | S6: V↑→A↑→장벽↓→꼬리↓. 코드는 A 컷-상수 동결이나 물리 부호 명제 유지(N7 codebox 명시). 결함 0 |
| R4 | 도메인 (재현성) | G-usable (피팅 코드 시뮬) | 재현 상수 전수: z_cut=4.357·A_cap=4.0·grid_pad=0.15·n_work_min=2048·min_lag=2·w_eff_floor=0.05·staging 표·lowpass 점화식·역전. 결함 0 |
| R5 | 절 | 완결성·orphan | 그림 5/표 2 전부 \ref(orphan 0). 중간식 5건(spinodal·gxi·center·lowpass·branch) \eqref 추가로 사슬 연결. equilibrium() 진술 코드(L354–371) 대조 일치 |
| R6 | 그림 | 시각·PDF | 5 TikZ 전부 렌더 확인(p1 spine·p5 staging·p8 hysloop·p10 logistic·p13 reversal). 효과적·동기·사용 짝. 결함 0 |
| R7 | 식별 | N0·N9 경계 | |I|=c_rate·Q_cell(L509) ↔ eq:n0map; dqdv_work+=Q·peak_shape, np.interp(L481–483) ↔ eq:sum. 결함 0 |
| R8 | 직전수정 | 새 결함 | 추가 \eqref 5건 빌드 정상(refs 31→36). flow 재정독 깨짐 없음. 결함 0 |
| R9 | 표 (수치) | 재유도·정합 | staging 표 7열 × 4행 ↔ GRAPHITE_STAGING_LIT(L536–562) 전수 일치. U(298) stage2→1=(13000−298.15·16)/96485=0.0853≈0.085 검산. 결함 0 |
| R10 | 도메인 | 표기·부호 일관 | σ_d(런타임)=s(열역학 규약)=+1 방전, §1 에서 명시 등치. 부호 §8 전건 §10 검산. 결함 0 |

**수렴**: R9·R10 연속 0결함 → 수렴 달성(하한 10R 충족).

## ③ 부호 사슬 체크리스트 결과 (브리프 §8, 코드 v11 대조)

전 8건 PASS (문건 §10 `부호 사슬 전수 검산`에 수록):
1. U_j(T)=(−ΔH+TΔS)/F, ΔG=−FU (func_U_j) — ΔH<0 발열 중심↑. PASS
2. ξ_eq=logistic[σ_d(V−U)/w] (func_ksi_eq) — 방전 V↑→ξ↑. PASS
3. dξ/dV peak=|ξ(1−ξ)/w| 양수·방향불변. PASS
4. ΔU_hys≥0, Ω≤2RT→0 (func_dU_hys); 분기 ±½σ_d (func_U_branch) U^dis>U^chg. PASS
5. χ_d 방전χ/충전1−χ (func_chi_d); ΔH_a^eff=ΔH_a−χ_dΩ (func_dH_a_eff). PASS
6. ∂lnL_q/∂V<0 (func_L_q 물리). PASS
7. 충전 격자역전 ξ[::-1]…[::-1] (_causal_lowpass 호출); 충전 dQ/dV=방전 거울(양수). PASS
8. 분극 V_n=V_app−σ_d|I|R_n (dqdv L412). PASS

## ④ 그림 목록 (전부 신규 TikZ, 내부 영어 ASCII만 — 한글 0 검증됨)

| # | 라벨 | 위치(노드) | 왜 필요(앞 동기·뒤 사용) |
|---|---|---|---|
| 1 | fig:spine | 서론 | 코드 진행 N0→N9 한눈 — 전체 절 순서의 지도. per-tr 루프 점선상자. |
| 2 | fig:staging | §1(N0) | staging 갤러리 채움 — 전이 4건·방향(방전)의 물리 그림, staging 표 동기. |
| 3 | fig:hysloop | §4(N3) | 비단조 V_eq·과주행 — ΔU_hys 가 두 spinodal 차임을 시각화(eq:dUhys 동기). |
| 4 | fig:logistic | §5(N5) | ξ_eq logistic·미분 종 — N6 평형 peak 모양의 시각 짝. |
| 5 | fig:reversal | §8(N8) | ★충전 격자역전 — 방전/충전 꼬리 거울(부호 §8-7 의 시각 증명). |

ASCII 검증: 5 tikzpicture 블록 내 Hangul 0 (스크립트 확인). 캡션 prose 만 한글(허용).

## ⑤ Decision Queue

- D1: v5 의 §1.x 광범위 유도(Stirling·lever rule·binodal cotangent 등)는 곡선 N2–N9 에 직접 안 물려 **최소 인용**만(브리프 §3 범위 밖 orphan 0 원칙). N3 에서 spinodal·gap 닫힌식만 결과로 사용 — 의도적 범위 결정.
- D2: `equilibrium()` 메서드는 N6 절에서 "|I|→0 기준선·히스 미반영"으로 1문단 인용(별도 절 안 둠 — spine 노드 아님, 기준선 성격).
- D3: per-transition override(z_cut·A_cap·use_w_eff·use_dH_eff)·가드(_finite류)·facade 의 방향문자열 파싱은 곡선 물리가 아니라 인터페이스라 표/codebox 수준으로만 언급(수식 주도 본문 비대화 방지). 필요 시 master 가 확장 판단.

## ⑥ 빌드 결과

- 명령: `xelatex -interaction=nonstopmode v7-06.tex` ×2 (2-pass).
- 결과: **EXIT=0, 에러 0, Undefined control sequence 0, Missing character 0, Undefined reference 0.**
- PDF: **15 페이지**, 309 KB 생성.
- Overfull hbox: 0 (\emergencystretch 흡수). Underfull: 10 (장식적, v5 동급, 무해).
- 폰트 경고(UnBatang/D2Coding italic shape 대체): 무해(kotex 치환, v5 동급).
- preamble: v5 계열(documentclass[11pt,a4paper]{article}, kotex, D2Coding mono, amsmath/amssymb/mathtools/bm, booktabs, tikz+positioning+arrows.meta+fit+backgrounds, hyperref). 자족(외부 \input 0).
