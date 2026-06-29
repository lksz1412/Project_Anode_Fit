# Ch2 v3 (가역 발열·엔트로피 계수) — 백지 재조사·초안 Plan (조사→draft, master + 서브 1~2)

> ★**Ch2 v3 = 완전 백지**(마지막 = v2, 2026-05-29 / v2·rebuilt·old·roadmap_v1 **미참고·선 긋기**). **Ch1 v8-11 은 토대**(가역 발열이 그 위에 섬). ★**병렬화 없음** = master + 서브 1~2(예전 4-세션 경량). 본 계획 업데이트 후 **바로 진행**(GO 받음).

## Summary
**목표.** Ch1(흑연 음극 dQ/dV forward 모델, v8-11)의 수식을 토대로, **가역 발열(reversible/entropic heat)과 엔트로피 계수 ∂U/∂T·∂V/∂T·ΔS(x)** 를 — 그리고 실데이터(다온도 dQ/dV) 피팅으로 그것을 추정하는 경로를 — **광범위·엄밀한 1차 문헌 조사로 백지부터 근거화**하고, 그 위에 **Ch2 v3 초안(draft)** 을 잡는다. v2(및 rebuilt/roadmap_v1)는 참고하지 않고 선을 긋는다(사용자 지시). 산출물 품질 목표 = Ch1(v8/v11)급이되, 이번 단계는 *조사 + 초안*(완본 아님 — 교수님 검토 후 v9 통합·심화).

**왜.** 이 주제(Ch1 수식↔발열, 가역 발열 추정)의 연구가 **매우 미진**했고(사용자 명시), v2 이후 진행 이력 없음. 1차 문헌을 제대로 조사·검증해 의도에 맞는 정보만 추려야 제대로 된 초안이 선다. **추측을 "조사 결과"로 제시 금지·DOI/링크 병기·불확실은 "모르겠다"**(헌법 Cowork §1·confirmed_items_policy).

**핵심 정합(이미 확인).** Ch1 의 $U_j(T)=(-\Delta H_{\rxn,j}+T\Delta S_{\rxn,j})/F$ ⇒ $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ = **전이별 엔트로피 계수**가 Ch1 에 이미 내장. 사슬: 다온도 dQ/dV 피팅 → 전이별 $U_j(T)$ 온도기울기 → $\Delta S_{\rxn,j}(x)$ → 가역 발열 $\dot Q_\mathrm{rev}=-I\,T\,\partial U_\mathrm{oc}/\partial T$(Bernardi). 조사가 이 사슬의 각 고리를 문헌으로 검증·정량·한계규정하고, 초안이 그것을 Ch1 위에 무비약으로 전개.

## Current Ground Truth
**버전 확인(2026-06-30):** 가역 발열 주제 Ch2 의 마지막 = **v2**(`graphite_ica_consolidated_ch2.tex` 헤더 "v2 / 2026-05-29"·`_body_ch2_v2.tex`·`graphite_ica_ch2_rebuilt.tex`·`MASTER_ROADMAP_CH2_v1.md`). 이후 6-07~6-09 ch2 작업은 반응속도론·히스테리시스로 재편됐다 전부 Ch1 으로 병합(v8-11 이 히스 보유). ∴ **이 주제 Ch2 = v2 이후 진행 이력 없음** → 신규 = **v3**, 백지.

**확인된 사실(2026-06-30 실시간 검색 grounding — *존재* 확인, 값·방법은 정독으로 *검증* 후 확정 tier):**
- 엔트로피 계수 ∂U/∂T(graphite): potentiometric 측정, ~+250→−100 µV/K, staging 상관(저SOC 큰 음수→stage4서 평탄→stage2(40–60%)서 넓은 peak).
- 가역 발열 & Bernardi: $\dot Q=I(U-V)-I\,T\,\partial U/\partial T$(비가역 joule + 가역 엔트로피); ΔS 부호 따라 흡열/발열·SOC 의존.
- staging 열역학: LiC6 ~−13.9·LiC12 ~−24.8 kJ/mol Li(calorimetric); ΔS 저x 양수(configurational)→고x 음수(vibrational), stage2→1(x=0.5) 이상거동. ★Ch1 GRAPHITE_STAGING_LIT 와 부분 정합·부분 상이(단위·기준 정규화 필요) — 조사 재검증.
- ICA↔열역학: peak=상전이; 부분몰 엔트로피·엔탈피로 occupation transition 해석(physically-informed model 선례).
- 추정 방법: MSMR 온도의존·system-ID·연속함수 OCV(T) 회귀.
- **Ch1 자산**: v8-11(유도 포함 교과서판)·v7-11·`Anode_Fit_v11_final.py`. ★가역(평형 ∂U/∂T) vs 비가역(히스·과전압·kinetic lag) 분리가 Ch1 에 이미 구조화.

**미확인(조사 표적):** 값들의 원전·측정조건·불확도 / Ch1 staging 값↔문헌 정합 / dQ/dV(T)로 ∂U/∂T 추출 실증 선례·정확도 / configurational↔vibrational 분해 모델 / 히스테리시스 하 "가역" 경계 / 반응 엔트로피 ΔS_rxn vs 활성화 엔트로피 ΔS_a 혼동 주의.

## Phase Range
| Chapter | Phase | 이름 | Steps | Gate | 주체 |
|---|---|---|---:|---|---|
| A 범위 | 0.1 | 연구질문·6축·검색전략 | 1–4 | 질문 7±·6축·쿼리셋·기준 확정 | master |
| B 조사 | 1.1 | 6축 문헌 수집·선별 | 5–9 | 축별 후보·중복제거·선별표 | master + 서브1(수집 deep 위임) |
| C 정독·추출 | 2.1 | 핵심 문헌 정독·추출카드 | 10–16 | 추출카드(출처 폐쇄·추측 0) | master + 서브1(축 분담 순차) |
| C | 2.2 | Ch1 정합 대조 | 17–20 | Ch1↔문헌 전이별 정합/괴리표 | master |
| D 종합 | 3.1 | 종합·삼각검증·갭·의도매핑 | 21–25 | 합의/논쟁/공백·사슬 커버맵·4-tier | master |
| E 초안 | 4.1 | Ch2 v3 초안 작성(절별 루프) | 26–33 | xelatex 0-err·무비약 유도·출처 닫힘·Ch1 정합 | master 작성 + 서브2(검수) |
| F 보고 | 5.1 | 종합 RESULT·교수님 요약 | 34–36 | RESULT·ledger·요약·다음(v9) 권고 | master |

## Non-goals (주의점)
- ★**v2·rebuilt·old·roadmap_v1 미참고**(선 긋기 — 사용자 지시). 백지 조사·작성. 단 **Ch1 v8-11/`Anode_Fit_v11_final.py` 는 토대로 참조**(가역 발열이 그 위에 섬·식별자·부호 정합).
- ★**병렬화·경쟁(9종)만 없음 — 품질 기법은 그대로 유지.** master + 서브 1~2(순차). competition-cherrypick(다종 경쟁) 미적용. 단, ★**절별 단위 구성 루프·N회 가변-청크 검수·렌즈 로테이션(G-derive/G-follow/G-usable/부호)·무비약 유도·orphan 0 는 그대로 가져온다**(사용자 명시 — 병렬 아니어도 절별 루핑 등 기법 유지). 즉 *어떻게(품질 루프)* 는 동일, *몇 마리로(병렬도)* 만 축소. Workflow 금지(Agent만). 단계마다 사용자 팝업 0.
- 이번 단계 = **조사 + 초안까지.** 완본·v9 통합·실데이터 피팅 *실행*은 범위 외(교수님 검토 후). 피팅은 *방법론·선례 조사*만.
- 원본 불가침(Ch1 문건·코드·v2 산출 수정 X). 추측 인용·미검증 값 단정 X. 범위 밖 주제(비-Li graphite·전고체) 확장 X.

## Implementation Changes
신규(`Project_Anode_Fit/Claude/`):
- `Claude/research/CH2_v3/` : `00_scope_taxonomy.md` · `10_sources_master.md` · `20_extraction/<key>.md`(문헌별) · `22_ch1_vs_literature.md` · `30_synthesis_gap.md`.
- **초안**: `Claude/docs/graphite_ica_ch2_v3.tex`(+pdf) — Ch2 v3 draft.
- 종합: `Claude/research/CH2_v3/PHASE_CH2v3_RESULT.md` · `CH2_v3_LEDGER.md`(12-col) · `50_report.md`(교수님 요약).
- `.session/ch2v3/` : 서브 brief·work_log·review(4-세션 로그 규약).

## Phase 0.1 — 연구질문·6축·검색전략 (Steps 1–4) [master 직접]
- **Step 1** 연구질문 확정: (Q1) 흑연 ∂U/∂T(x)·ΔS(x) 측정 프로파일·불확도? (Q2) staging 전이별 ΔH·ΔS 정량·조건? (Q3) 가역 발열 정의·Bernardi·calorimetry 검증? (Q4) dQ/dV(T)→∂U/∂T 추출 선례·정확도·함정? (Q5) configurational↔vibrational 분해? (Q6) 히스 하 가역/비가역 경계? (Q7) Ch1 staging 값 정합? (Q8) 반응 ΔS_rxn vs 활성화 ΔS_a 구분?
- **Step 2** 6축: ①엔트로피 계수 측정 ②가역 발열·Bernardi·열모델 ③ICA/dQ-dV 열역학 ④Li-graphite staging 열역학(실험·DFT) ⑤파라미터 추정(MSMR·system-ID·OCV(T) 회귀) ⑥교과서/리뷰(Newman 등).
- **Step 3** 쿼리셋·DB(Scholar·CrossRef·arXiv·publisher·교과서)·포함/제외 기준.
- **Step 4** **Gate**: `00_scope_taxonomy.md` 저장(질문·축·쿼리·기준).

## Phase 1.1 — 6축 수집·선별 (Steps 5–9) [master + 서브1 수집 위임]
- **Step 5–8** master 가 축별 검색 주도(WebSearch). 분량 큰 축/심층 수집은 **서브1(작업 sub)** 에 *순차* 위임(4-세션 고지: 역할=수집 작업 sub·경계=수집·선별만·범위밖 금지·허위 attribution 금지). 후보 = {제목·저자·연도·DOI/URL·축·1줄 적합성}.
- **Step 9** 중복제거·선별(1차 출처·peer-review 우선·리뷰=진입점). **Gate**: `10_sources_master.md`.

## Phase 2.1 — 핵심 문헌 정독·추출 (Steps 10–16) [master + 서브1 순차]
- **Step 10–15** 핵심 문헌 **전문 정독**(WebFetch/접근분; 불가분 abstract+2차인용 명시·tier 강등). 축별로 master 또는 서브1(순차) 가 **추출카드** 작성: {방법·지배식(verbatim)·정량값(값·단위·조건·불확도)·타당/한계·의도 관련성·★출처·정독범위·tier}. ★추측 0·미검증 단정 0.
- **Step 16** **Gate**: 핵심 추출카드 완비·출처 닫힘.

## Phase 2.2 — Ch1 정합 대조 (Steps 17–20) [master 직접 — CORE 판단]
- **Step 17–19** Ch1 `GRAPHITE_STAGING_LIT`(전이별 ΔH_rxn·ΔS_rxn·U·Ω·ΔH_a)·U_j(T) ↔ 문헌 정량값 대조(전이/stage 매핑·단위 정규화 per molLi↔per transition↔per F). 부호·규모 정합/괴리.
- **Step 20** **Gate**: `22_ch1_vs_literature.md`(전이별 정합/괴리·신뢰등급).

## Phase 3.1 — 종합·삼각검증·갭·의도 매핑 (Steps 21–25) [master 직접]
- **Step 21–24** 합의/논쟁/공백 분류·★사슬(dQ/dV(T)→∂U/∂T→가역 발열) 각 고리 문헌 커버맵·삼각검증(≥2 독립)·함정(DFT 신뢰성·히스 가역성·ΔS_rxn vs ΔS_a).
- **Step 25** **Gate**: `30_synthesis_gap.md`(4-tier).

## Phase 4.1 — Ch2 v3 초안 작성 (Steps 26–33) [master 작성 + 서브2 검수]
- **Step 26–31** master 가 **절별 단위 구성 루프**(절/식 하나씩: 정독→구성→자체검수→앞단위·Ch1 정합→빌드→사유, 통째 배치 X·복붙≠완료·orphan 0)로 `graphite_ica_ch2_v3.tex` 초안 작성(백지·Ch1 v8-11 토대): ①서(발열의 자리·Ch1 승계) ②가역/비가역 발열 정전(Bernardi·∂U/∂T·ΔS) ③Ch1 $U_j(T)$ → $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 전이별 엔트로피 계수 유도 ④흑연 측정 프로파일·staging 값(출처·Ch1 대조) ⑤다온도 dQ/dV → ∂U/∂T 추정 경로·방법론(선례·함정) ⑥가역 발열 합산·한계·검증법 ⑦반응 ΔS_rxn vs 활성화 ΔS_a 구분(혼동 금지). 모든 정량 = 출처. 무비약(G-derive)·수식 주도·그림 필요시 신규(영어 ASCII).
- **Step 32** ★**N회 가변-청크 검수(순차·비병렬)**: 초안 완성 후 동일 방식 N회 재검수(기본 10·연속 2R 0결함 수렴) — 매 라운드 청크 스킴(통독/절/식/라인)·렌즈(출처 폐쇄·무비약 G-derive·Ch1 정합·부호·완결성·시각) 전환. 라운드별 **서브2(검수 sub)** 가 refute+가장 약한 1곳+빈통과 금지로 검수(4-세션 고지: 검수 sub·변경 X·decision queue) → master 삼각검증·직접 수정. master↔서브2 max_iter 5/라운드.
- **Step 33** **Gate**: xelatex 0-err·유도 무비약·출처 닫힘·Ch1 식별자/부호 정합·v2 미참고 확인.

## Phase 5.1 — 종합·요약 (Steps 34–36) [master]
- **Step 34–35** `PHASE_CH2v3_RESULT.md`(11항목)·`CH2_v3_LEDGER.md`·`50_report.md`(교수님 1–2p: 발견·갭·초안 상태·v9 통합 권고).
- **Step 36** **Gate**: RESULT·ledger·요약 완료. 토픽 종료 시 master commit(푸쉬 정책 준수).

## Implementation Interfaces
**(1) 서브 prompt 머리(4-세션 고지·필수)**: 역할(수집/정독-추출 작업 sub 또는 검수 sub)·분업 경계(작업=수집·추출만/검수=audit만·변경 X·commit 은 master)·범위 밖 자의작업 금지(새 문건·표준·메모리 X·decision queue 등록만)·허위 attribution 금지·self-contained(본 대화 컨텍스트 없음·경로·기준 prompt 에).
**(2) 추출카드 schema**: `key|저자·연도·DOI|축|방법|지배식(verbatim)|정량값(값·단위·조건·불확도)|타당/한계|의도 관련성|정독범위|tier`.
**(3) Ch1 정합표 schema**: `전이/stage|Ch1 값|문헌 값(출처)|단위정규화|정합도|비고`.
**(4) 핵심 사슬(검증·작성 표적)**: $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ → 다온도 dQ/dV 피팅 → $\Delta S_{\rxn,j}(x)$ → $\dot Q_\mathrm{rev}=-I\,T\,\partial U_\mathrm{oc}/\partial T$. 각 고리 근거·정확도·함정.
**(5) seed 문헌(검증된 출발점, 정독·확장 대상 — 조사 결과 아님)**: Reynier/Yazami JPS 2003(S0378775303002854)·Potentiometric model JES 2018(10.1149/2.1251802jes)·JPS 2005 anomalies(S0378775305007500)·Standardised Potentiometric reversible heat JES 2024(10.1149/1945-7111/ad4918)·Transitions of Li occupation physically-informed Electrochim.Acta 2019(S0013468619316457)·Differential Analysis Chem.Mater.2022(acs.chemmater.2c01976)·LiC6/LiC12 calorimetry Chem.Mater.2015(acs.chemmater.5b00235)·DFT vibrational+config JPC C 2021(acs.jpcc.1c08992)·MSMR entropy coeff JES 2024(10.1149/1945-7111/ad70d9)·System-ID JES 2025(10.1149/1945-7111/adfe1f)·Unifying Thermodynamics arXiv 2507.10677. 교과서: Newman&Thomas-Alyea *Electrochemical Systems*.
**(6) Result 11항목·Ledger 12-col·보고 4-tier** = 헌법 양식.

## Test Plan
- 출처 폐쇄(모든 정량·방법 DOI/URL+페이지·출처없는 단정 0)·삼각검증(핵심 ≥2 독립)·단위정규화 검산·Ch1 사슬 커버맵(공백 정직)·4-tier 무결·정독 증명(추출카드 페이지/행, abstract-only 명시).
- (초안) xelatex 0-err·유도 무비약(G-derive)·Ch1 식별자/부호 1:1·v2 텍스트 미유입(백지 확인).

## Assumptions
- 1차 문헌 다수 접근 가능(불가분 2차인용·tier 강등). Ch1 $U_j(T)$ 구조가 문헌 staging-엔트로피와 매핑 가능(Phase 2.2 검증·불일치 시 갭). 가역 발열=평형 ∂U/∂T(Bernardi 가역항)·히스/경로의존은 비가역(조사로 경계 확정). master+서브 1~2 순차로 충분(병렬 불요·사용자 지시).

## Correction History
- 2026-06-30 1차본(조사-only)을 사용자 지시로 업데이트: (a) **Ch2 v3 백지**(마지막=v2 확인·v2/rebuilt/old/roadmap_v1 미참고·선 긋기) (b) **조사→초안**까지(완본·피팅·v9 통합 제외) (c) ★**병렬화·경쟁 제거 → master + 서브 1~2 순차**(예전 4-세션 경량·competition-cherrypick 미적용) (d) Ch1 v8-11 토대 명시.
- 추측 방지: seed 는 검색으로 *존재* 확인, 값·방법은 정독 후 확정 tier.
- ★본 계획 업데이트 후 **바로 진행**(사용자 "업데이트해서 저장해두고 바로 진행"). Phase 0.1→5.1 무중단(정지 5조건만).
