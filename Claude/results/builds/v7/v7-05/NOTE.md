# v7-05 작업 노트 (graphite_ica_ch1 v7, 1편)

산출 = `v7-05.tex` (자족, v5 계열 preamble) + `v7-05.pdf` (17 페이지, xelatex 2-pass, 에러 0).
방식 = v5 형식(수식 주도)을 v11_final.py 코드 진행(N0→N9)에 맞게 어레인지. 절 순서 = 플로우차트 노드 순서.

---

## ① Read Coverage (전문 정독 행범위)

| 입력 | 행범위 | 정독 |
|---|---|---|
| `AUTHOR_BRIEF.md` | 1–76 (전문) | head→tail 1회 |
| `v11_flowchart.md` | 1–90 (전문) | head→tail 1회 |
| `Anode_Fit_v11_final.py` | 1–706 (전문) | head→tail 1회. 식별자·부호·진행 정본 |
| `graphite_ica_ch1_Opus_v5.tex` | 1–1883 (전문) | 5개 창(1–470 / 470–950 / 950–1429 / 1429–1659 / 1659–1883)으로 head→tail. ★v6 미사용(v5만) |

코드 핵심 매핑 정독 확인: `func_w`(L64), `func_U_j`(L68), `func_U_j_hys`(L72), `func_ksi_eq`(L84), `func_L_q`(L90-97), `_causal_lowpass`(L100-118), `func_dU_hys`(L123), `func_U_branch`(L133), `func_w_eff`(L141), `func_dH_a_eff`(L149), `func_chi_d`(L155), `_resolve_lag_length`(L307-351), `dqdv`(L374-484, 전이루프 L435-484), `curve`(L487-512), `_direction_to_sigma`(L514), `GRAPHITE_STAGING_LIT`(L535-564).

---

## ② 라운드별 결함 추이 (자체 10R, 가변 청크·렌즈)

본작업(통독 작성) 후 10라운드. 청크 스킴·렌즈 매 라운드 전환. 연속 2R 0결함으로 수렴.

| R | 청크 스킴 | 렌즈 | 발견 결함(수정) |
|---|---|---|---|
| R1 | 절별(N0–N5) | 구조·spine 정합 | 0 (절 순서 = 플로우차트 N0→N9, 도입·넘김 다리 전부 존재) |
| R2 | 식별자·부호 사슬 전건 | 물리·부호 적대검산(§8 체크리스트) | 0 (부호 8항 전건 코드 대조 일치 — 아래 ③) |
| R3 | 식·식별자 1:1 (agent) | G-usable / 코드 fidelity | 0 (39식·6상수·32표셀·4수치 전부 코드 일치) |
| R4 | 통독 (agent) | G-follow / orphan·완결성 | 6 (fig:branch·fig:reversal 본문 미참조 / eq:lnLq 괄호인자 무유도 / k_j 선정의 / 재타이핑 eqref 3건 / 미인용 bibitem 4건) |
| R5 | 그림 5개 (agent, PDF 시각) | 그림 효과·시각 | 0 (overflow·collision·Hangul-in-figure 0; 캡션 정합) |
| R6 | 식 재유도 (agent) | 물리 적대 재유도·극한 | 1 (eq:Acut "5%" 문구 모호 — bell-height 기준임을 명시) |
| R7 | 라인-레벨 (N7 수정부) | 직전 수정 새 결함(regression) | 1 (5.1pt overfull — 문구 단축 흡수) |
| R8 | 식별자·ref 무결성 (스크립트) | 완결성 orphan | 0 (refs→missing 0 / cites→missing 0 / unused bibitem 0 / fig Hangul 0) |
| R9 | 환원·극한 전건 | 물리 극한·반례 | 0 (\|I\|→0→equilibrium / Ω≤2RT→ΔU_hys=0 / γ=0→방·충 합치 / L_V<2g_step→평형종 — 4 환원 전부 본문 명시·코드 정합) |
| R10 | 통독(빌드 PDF) | 시각·최종 정합 | 0 (수렴) |

R4·R6·R7 의 결함 8건 전부 직접 수정 후 재빌드 유지. R9–R10 연속 0결함 = 수렴.

---

## ③ 부호 사슬 체크리스트 결과 (§8 전건, 코드 v11 대조)

| # | 항목 | 본문 식 | 결과 |
|---|---|---|---|
| 1 | U_j(T)=(−ΔH+TΔS)/F, ΔG=−FU | eq:Uj, eq:eqcond | PASS (ΔH_rxn<0→U>0; stage2→1 U(298)≈0.085 V 검산) |
| 2 | ξ_eq=logistic[σ_d(V_n−U)/w], 방전 V↑→ξ↑ | eq:logistic | PASS |
| 3 | dξ/dV=σ_d·ξ(1−ξ)/w, peak 양수(방향 불변) | eq:dxidV, eq:eqcontrib | PASS (σ_d²=1) |
| 4 | ΔU_hys≥0, Ω≤2RT→0; 분기중심 ±½σ_d… | eq:hysdU, eq:hyscenter | PASS (U^dis>U^chg) |
| 5 | χ_d: 방전 χ/충전 1−χ; ΔH_a^eff=ΔH_a−χ_d·Ω | eq:chid, eq:dHeff | PASS |
| 6 | ∂lnL_q/∂V<0 (V↑→장벽↓→꼬리↓) | boundbox | PASS (−χ_d σ_d F/RT≤0) |
| 7 | 꼬리 충전 격자역전; 충전 dQ/dV=방전 거울(양수) | eq:reversal | PASS |
| 8 | 분극 V_n=V_app−σ_d\|I\|R_n | eq:vn | PASS (방전 V_n<V_app) |

전건 코드 일치. G-usable agent 가 39식·상수·표·수치 독립 재계산으로 0결함 확인. Physics-adversarial agent 가 8항 SymPy/수치 재유도로 전건 PASS 확인.

---

## ④ 그림 목록 (전부 신규 TikZ, 내부 영어 ASCII만)

| 그림 | 위치(절) | 왜 필요한가 | 본문 참조 |
|---|---|---|---|
| fig:staging | 서론 | staging 갤러리 채움 = 4 전이의 물리적 그림(표 tab:staging 와 연결) | ✓ |
| fig:logistic | N4–N5 | ξ_eq logistic 과 그 미분 종(dξ/dV) — 평형 peak 의 부호·중심·폭 시각화 | ✓ |
| fig:branch | N3 | 히스 분기 중심 σ_d 별 ±이동(방전 위/충전 아래) — 부호 사슬 4 | ✓ |
| fig:reversal | N8 | 인과 지연 + 충전 격자역전(방전 꼬리 고전위/충전 저전위) — 부호 사슬 7 | ✓ |
| fig:flow | N9 | N0→N9 전체 계산 진행 한눈 — 절 순서 = 이 흐름 1:1 | ✓ |

5 그림 전부 본문 \ref 됨(orphan 0). 그림 내부 텍스트·축·노드·범례 = 영어 ASCII만(스크립트로 Hangul-in-figure 0 확인). 캡션 prose 만 한글.

---

## ⑤ Decision Queue (발견 의문·결정)

- D1. 절 순서: 브리프 §3 가 N4,N5→N6→N3 순(분기를 평형 peak 뒤로)을 명시. 코드 루프는 N2→N3→N4→N5 순이나, 방전 본론을 먼저 닫고 히스를 확장으로 얹는 브리프 골격을 채택. N2 끝·N3 머리에서 이 순서 역전을 명시 신호(G-follow agent 확인: followability 안 깨짐).
- D2. `U_j` 직접 지정 vs 열역학 환산: 코드는 `U` 키 우선, 없으면 func_U_j. 본문은 열역학 환산(func_U_j)을 유도하고 `U` 직접은 폴백으로 명시. tab:staging 은 둘 다 수록(U 와 dH_rxn/dS_rxn 정합).
- D3. eq:lnLq 의 χ_d 두 등장(forward −χ_d·A/RT + ΔH_a^eff 내 −χ_d·Ω): 둘 다 코드 `func_L_q`·`_chi_and_dH_eff` 에 실재. 재구현자가 한쪽 누락·중복 가능한 유일 지점이라 본문에 명시 분리. (의문 아님 — 코드 정합 확인됨.)
- 결정 대기 항목 없음. 작업 중단 없이 진행.

---

## ⑥ 빌드 결과

- 명령: `xelatex -interaction=nonstopmode v7-05.tex` × 2-pass (MiKTeX-XeTeX 4.16, D2Coding 폰트 설치 확인).
- **에러 0** (`grep '^! '` = 0). PDF **17 페이지**, 349 KB.
- 미해결 ref/cite **0** (스크립트: refs→missing 0, cites→missing 0, unused bibitem 0). "Rerun" 경고 0.
- 잔여 경고: 폰트 shape fallback 3건(TU/UnBatang it, TU/D2Coding it — 이탤릭 한글/모노 upright 대체, cosmetic, 렌더 정상). overfull hbox 최대 1.56pt(emergencystretch 흡수, 내용 불변).
- 정량 무결성: 식 39·그림 5·표 1, 부호 8항 PASS, 코드 1:1 fidelity 0결함.

자체 10R 수렴(연속 2R 0결함). 빌드 통과·에러 0·PDF 생성 확인.
