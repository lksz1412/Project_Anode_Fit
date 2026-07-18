# INDEX — v1.0.23 아티팩트 색인 (P5 마감)

## 문건 (docs/v1.0.23/)
- `ch1_graphite_v1.0.23.tex` (+ .pdf, **87p**) — Chapter 1 마스터: 흑연 dQ/dV + Part T 열특성 + 부록 A·B·C·D·**E**
- `ch2_lco_v1.0.23.tex` (+ .pdf, 25p) — Chapter 2 LCO
- `ch3_si_v1.0.23.tex` (+ .pdf, 17p) — Chapter 3 Si/블렌드
- `appendix_phase_separation.tex` — 독립 standalone 초안(미편입·어느 마스터에도 \input 안 됨)
- `_sections/*.tex` — 53개 섹션(v1.0.22 52개 + **ch1_appE_selfconsistent.tex** 신규)

### 신규 (v1.0.23 델타)
- `_sections/ch1_appE_selfconsistent.tex` (212행) — 부록 E "자기일관 해법: ratio 닫힘과 전달함수"
- `_sections/ch1_sec08_lag.tex` — 말미 부록 E 포인터 1문장(수정)
- `_sections/ch1v22_bib.tex` — bibitem 3종 추가(lee2017jcp·lee2011jcp·son2013jcp)
- `_sections/ch1_appB_codemap.tex` — 코드파일명 v1.0.23 정정(P5)

## 코드 (docs/v1.0.23/)
- `Anode_Fit_v1.0.23.py` (1585행) — 구현. 신규: `_causal_memory_ratio`·`transfer_apparent_from_equilibrium`·`_lag_ratio_geff`·플래그 `lag_ratio_correction`(기본 False)·dqdv elif 분기
- `test_gates_v1023.py` — 기존 게이트(G1 bit-exact·G2·G3·n(T)·R6)
- `test_gates_v1023_selfconsistent.py` — **신규** 자기일관 게이트(G-E1~E5)

## 계획서 (Claude/plans/)
- `2026-07-18-v1023-ratio-and-advanced-methods-plan.md` — 11-section 마스터 계획

## Phase 결과·원장 (docs/v1.0.23/results/)
- `PHASE_P1_RESULT.md` — 조건검수(11항)
- `PHASE_P2_RESULT.md` — 부록 E 저작(11항)
- `PHASE_P3_RESULT.md` — 코드 적용(11항)
- `PHASE_P5_RESULT.md` — 마감·적대검수(11항)
- `V1023_EXECUTION_LEDGER.md` — 12-col ledger(P0~P5)
- `V1023_CHANGE_LOG.md` — 변경 로그(S-013~014·A-019~022·B-001)
- `V1023_REFERENCE_LEDGER.md` — 서지 원장
- `MERGE_READINESS_v23.md` · `HANDOVER_v23.md` · `INDEX_v23.md` — 마감 3종

## 검수·분석 (docs/v1.0.23/results/comp_v23/)
- `COND_AUDIT.md` — P1 조건검수 정본(10절·P3-5 5항)
- `p1_ratio_check.py` — P1 수치 검산 스크립트(커밋)
- `AUD_REPORT_v23.md` — P5 코드↔문건 적대검수 5창 종합
- (서베이 원본 `SURV1-4_*.md`·`SURV_SYNTHESIS.md` = `docs/v1.0.22/results/comp_v23/`)

## 상태
- 빌드: 3장 err0·undef0(87/25/17p). 게이트: 기존 exit0(G1 bit-exact)·신 5/5.
- 검수: 코드↔문건 5창 치명 0·중대2 정정. parity 순수 additive.
- **다음**: 양 버전 샘플 이미지 QA(연속·매끄러움·미분가능성) → 사용자 요청.
