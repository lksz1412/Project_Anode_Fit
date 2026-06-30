# Ch2 v3 — 가역 발열·엔트로피 계수 조사→초안 RESULT (Phase 0.1–5.1)

> plan = `Claude/plans/2026-06-30-ch2-reversible-heat-entropy-survey-plan.md`. ★최종 산출 = `Claude/docs/graphite_ica_ch2_v3.tex`(초안, 5p). master + 서브 1~2(병렬 없음). 푸쉬 정책 준수.

## Summary
Ch2(가역 발열·엔트로피 계수) **v3 백지 재작성**(마지막=v2 확인·미참고). Ch1 v8-11 토대 위에서, Ch1 평형 전위 $U_j(T)$ → 전이별 엔트로피 계수 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ → 가역 발열 $\dot Q_\rev=-IT\,\partial U/\partial T$(Bernardi) 사슬을, **광범위 1차 문헌 조사**로 근거화하고 초안을 잡았다. 병렬·경쟁 없이 **master + 서브 1~2 순차**(품질 기법=절별 루프·검수 렌즈는 유지).

## Step Range
Phase 0.1(범위)→1.1(수집)→2.1(정독·추출, 서브1)→2.2(Ch1 정합)→3.1(종합·갭)→4.1(초안+검수, 서브2)→5.1(종합). step 1–36.

## Inputs
- Ch1: `v7-00_spine/Anode_Fit_v11_final.py`(GRAPHITE_STAGING_LIT·U_j(T))·v8-11/v7-11(읽기 전용 토대).
- 문헌: WebSearch/WebFetch 12+ 검색, ★ 10문헌 추출(4 full-text·6 abstract/snippet tier 강등).

## Files Created
- 조사: `research/CH2_v3/{00_scope_taxonomy, 10_sources_master, 20_extraction/(10카드)+_SUMMARY, 22_ch1_vs_literature, 30_synthesis_gap}.md`.
- 초안: `docs/graphite_ica_ch2_v3.tex`(+pdf, 5p). 검수: `docs/REVIEW_ch2_v3.md`.
- 본 RESULT·`CH2_v3_LEDGER.md`·`50_report.md`(교수님).

## Read Coverage
- v11_final.py(GRAPHITE_STAGING_LIT·U_j(T)) master 정독. 문헌 4건 full-text(Standardised 2024·MSMR I/II·Allart 2018)·6건 abstract(tier 명시). 추출카드에 정독범위 기록.

## Execution Evidence
- ★**부호 규약 확정**(삼각: Bernardi·Newman·MSMR Part I Eq.27/28): $\Delta S=+nF\,\partial U/\partial T$·$\dot Q_\rev=-IT\,\partial U/\partial T$. −부호 추출 1건은 추출오류로 폐기.
- ★**Ch1 정합(정량)**: Ch1 $\Delta S_{\rxn,j}$ $+29\to0\to-5\to-16$ = 문헌 흑연 $\Delta S(x)$(Allart full-text) 양 끝 정확 일치(+29·−16)·중간 범위 정합(해상도 차이 각주 명시).
- **사슬 커버맵**: ①$\partial U_j/\partial T=\Delta S/F$·③가역 발열=확정준함; ②다온도 dQ/dV 직접 추출=MSMR template 위 신규 각(지난 미진 지점).
- **초안 검수(서브2)**: 확정 결함 2(MED 1·LOW 1)·과장/날조 0·부호 FAIL 0·cite 11/11·xelatex 0-err. MED(tab:ds 중간 region 매핑)→각주 정정 완료.

## Validation
- xelatex 3-pass 0-error·ref/cite undefined 0·5p. cite-closure 11/11. 부호 사슬 v11 1:1. Ch1 정합 정량(각주로 해상도 차이 정직). 백지(v2/rebuilt 미유입) 확인. 모든 정량 출처+tier.

## Gate = PASS (조사→초안 완료)

## Confirmed Non-Changes
v2/rebuilt/old Ch2·roadmap_v1 미참고·미수정. Ch1 문건·코드·원본 무수정. 실데이터 피팅·완본·v9 통합 미실행(범위 외).

## Open Issues / Decision Queue
1. Electrochim.Acta 2019(dQ/dV→ΔS prototype) full-text 미확보(403) — 식·절대값 갭(방법만 인용).
2. Reynier 2003 절대 dE/dT·JPS 2018 히스 불확실도 정량 미확보.
3. ΔH 형성↔전이별 환산식 미작성(범위 외).
4. ②(dQ/dV(T) 직접 추출) 정확도 = 실데이터 round-trip 후속 실증 필요.
5. v8 점프 잔존(교수님 검토 후 v9서 Ch1 심화 가능).

## Next
- 교수님 검토 입력(`50_report.md`) → v9(Ch1+2 통합)·실데이터 피팅 방향 결정.
- 결정 시: ② 경로 prototype 식 확보 + 실데이터 다온도 dQ/dV round-trip(competition-cherrypick 스킬 적용 가능).
