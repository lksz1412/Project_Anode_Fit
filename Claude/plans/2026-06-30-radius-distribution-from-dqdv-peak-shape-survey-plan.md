# 흑연 dQ/dV peak 형상 → U_j 분포 → 활물질 반경 분포 추산 가능성 — 학술 조사 Plan (조사 only, master + 서브 4 목적적 병렬)

> ★**조사 전용**(초안 .tex 없음 — 사용자 요청 = "학술적 조사를 통해 답변"). 산출물 = `Claude/research/radius/` 의 조사 카드 + 종합 답변 문건. **Ch1 v8-11(`v8-11.tex`)·`v11_final.py` = 토대**(전제·기호 정합). **병렬 = 목적적 4 서브**(독립 subtopic·공유 가변상태 없음·web search 위임). CORE 판단(전제 검증·종합·verdict)은 master 직접. **Workflow 금지·Agent만·팝업 0.** 본 계획 저장 후 바로 진행(GO 받음).

## Summary
**목표.** 사용자 추정 — "Ω≥2RT 일 때 단일 입자 dQ/dV peak 은 (유사) 델타 함수여야 하는데 실측 코인 하프셀은 *치우친 종모양*으로 나타난다 → 이 종모양은 단일 입자 델타가 **U_j(전이 중심 전위) 분포**로 퍼진 통계역학적 형상이며, 흑연 입자를 구형으로 가정하고 U_j 분포가 **오직 반경에만** 의존한다고 보면, **peak 형상 = U_j 분포 = 활물질 반경 분포**로 역변환해 반경 분포를 추산할 수 있지 않은가" — 가 **물리적으로 타당한지, 어떤 조건에서 성립하는지**를 1차 문헌 기반으로 엄밀히 조사·판정한다. 산출 = 조사 카드(축별) + 종합 verdict 문건(성립 조건·한계·경쟁 기작·필요 가정·실측 절차 권고).

**왜.** 이 추정은 (a) 단일 입자 1차 상전이의 평형 형상, (b) 다입자 ensemble(mosaic/many-particle) 평균화, (c) 크기 의존 삽입 열역학(반경→전이 전위 결합), (d) 역문제(peak→분포 deconvolution) 의 **4개 독립 분야**가 한 사슬로 엮여야 성립한다. 각 고리에 확립된 문헌과 **반례·경쟁 기작**(특히 Ch1 모델 자체가 보유한 *동역학 꼬리* = 유한 전류 lag 가 바로 "치우친 종모양"을 만드는 1차 후보)이 있어, 추측이 아닌 문헌 검증이 필수. **추측을 "조사 결과"로 제시 금지·DOI/링크 병기·불확실은 "모르겠다"**(헌법 Cowork §1·confirmed_items_policy).

**핵심 정합(이미 코드·문건에서 확인).**
- `v8-11.tex` §6 평형 peak = `Q_j·ξ_eq(1−ξ_eq)/w` = logistic 미분 종(폭 `w=nRT/F`, 중심 `U_j`, 면적 `Q_j`, 중심 순높이 `Q_j/4w`).
- `v8-11.tex` eq:weff·`v11_final.py:141-146` `func_w_eff = (RT/F)(1−Ω/2RT)`, floor `0.05·RT/F`(≈1.3 mV). ∴ **Ω→2RT 에서 w_eff→0**, Ω>2RT 면 음수→floor 클립 = 모델상 "최협(유사 델타)". 단 **기본 `use_w_eff=False`**(기본 폭은 `nRT/F`).
- Ω>2RT 는 eq:spinodal 의 상분리(히스테리시스) 문턱 = **단일 입자 1차 상전이** → Maxwell 평탄역 → dQ/dV 델타(물리적으로 사용자 전제와 정합. 조사로 확정).
- `v8-11.tex` §7–8 **동역학 꼬리**(N7/N8): 유한 전류 lag `(ξ_eq−ξ_lag)/L_V` = peak 을 *비대칭으로 늘이는* 기작이 **이미 모델에 내장**. ★사용자의 "치우친 종모양"의 경쟁 설명 = 이 kinetic 꼬리. 조사는 radius-분포 가설과 이 kinetic 가설을 **분리 판정**해야 함.

## Current Ground Truth
**버전(2026-06-30):** 관심 대상 = `Claude/results/v8-11/v8-11.tex`(Ch1 유도 확장 최종) + `versions/v11_final.py`(코드화). 둘 다 master 정독 완료(tex 1209행 핵심 절 §1·6·7·8·9 / 코드 `func_w`·`func_w_eff`·`func_ksi_eq`·peak 분기). 본 조사는 이 모델을 **수정하지 않고**, 그 위의 *해석 가설*(반경 분포 추산)을 문헌으로 검증.

**확인된 사실(코드·문건 grounding — tier=확정):**
- 평형 단일 종 폭 = `nRT/F`(n=1 시 25.7 mV@25℃). w_eff 옵션은 Ω 로 좁힘(floor 존재 → 진짜 델타 아님).
- Ω>2RT ⇔ spinodal 실수근 ⇔ 상분리·히스. 이때 단일 입자 평형 등온선 비단조(van der Waals loop) → Maxwell 작도 시 평탄 plateau.
- 모델은 kinetic 꼬리로 실측 비대칭을 설명(현재 구조). U_j 분포(입자간 이질성)는 **현재 모델에 없음** — 사용자 가설은 이를 신규 도입하는 것.

**미확인(조사 표적):**
1. (전제) 단일 입자 Ω>2RT 가 실제로 dQ/dV 델타/극협 peak 을 주는가 — 1차 상전이 평형 형상·single-particle 실험(in-situ 단일 입자 전기화학) 근거.
2. (ensemble) 전이 전위 U_j 분포를 가진 다입자계가 *매�from*·*치우친* 평균 dQ/dV 를 주는가 — many-particle/mosaic/domino-cascade 모델(Dreyer·Bazant·Bai·Cogswell). 입자 **독립 vs 상호작용** 가정의 영향.
3. (결합) 입자 **반경**이 전이 전위 U_j 를 이동시키는가 — 기작(Gibbs–Thomson 표면에너지·coherency strain·miscibility-gap 억제·표면 재구성), **부호·크기**. LiFePO4 나노입자 정전 vs **흑연(마이크론) 정량 차이**.
4. (역문제) "peak→U_j 분포→반경 분포" 역변환의 **성립 조건·유일성·deconvolution**. 내재폭 ≪ 분포폭, 근평형(kinetic 무시), 단조·기지의 r→U_j 사상, 전이 격리, 반경이 U_j 이질성의 지배 원인.
5. (선례) dQ/dV·DVA·GITT·EIS·relaxation 으로 **입자 크기 분포를 실제 추출한 연구**·정확도·함정. OCV 를 site-energy density-of-states 로 보는 해석(McKinnon–Haering 등).
6. (경쟁·정량) 흑연 마이크론 입자에서 실측 치우침이 반경 분포 vs **kinetic dispersion·접촉저항 분포·조성 이질성·온도**중 무엇에 지배되는가 — 정량 규모 비교·분리 가능성.

## Phase Range
| Phase | 이름 | Steps | Gate | 주체 |
|---|---|---:|---|---|
| 0 | 연구질문·6축·검색전략·전제 1차검증 | 1–3 | `00_scope.md`(질문6·축·쿼리·기준·전제 판정) | master 직접 |
| 1 | 목적적 4 병렬 조사(축별 카드) | 4–7 | 4 카드(`10`~`13`) 출처폐쇄·4-tier·추측0 | master + 서브A/B/C/D 병렬 |
| 2 | 삼각검증·갭·경쟁가설 분리·역문제 조건 | 8–10 | `20_synthesis.md`(합의/논쟁/공백·사슬 커버맵) | master 직접 |
| 3 | 종합 verdict 문건(성립조건·한계·절차 권고) | 11–12 | `RADIUS_VERDICT.md`·요약·RESULT·ledger | master 직접 |

## Non-goals (주의점)
- ★**모델 수정·코드 작성·실데이터 피팅 *실행* 범위 외.** 본 조사 = *해석 가설의 타당성·조건* 판정 + 절차 *권고*. 실제 deconvolution 구현·피팅은 교수님 검토 후 별도.
- ★**Codex 산출물 read 금지**(`Codex/` tex 디벨롭 결과 등 — CLAUDE.md P2). 운용 지침 문건만 예외(이번 불요).
- 추측 인용·미검증 값 단정 X. seed 문헌은 *존재* 만 검색 확인, 값·방법은 정독 후 tier 확정.
- 범위 밖 확장 X(비-Li graphite·전고체·full-cell 부반응 등은 경계 표시만). 원본 불가침(`v8-11.tex`·`v11_final.py` 수정 X).
- ★**병렬은 목적적 4 서브만**(독립 subtopic). CORE 판단(전제·종합·verdict)은 master 직접. Workflow 금지·Agent만·단계 팝업 0.

## Implementation Changes
신규(`Project_Anode_Fit/Claude/research/radius/`):
- `00_scope.md` : 연구질문·6축·쿼리셋·포함/제외·전제(Ω>2RT→델타) 1차 판정.
- `10_single_particle_and_ensemble.md`(서브A) : 단일입자 1차 상전이 형상 + many-particle/mosaic ensemble 평균화.
- `11_size_dependent_thermo.md`(서브B) : 반경→전이 전위 결합 기작·부호·크기(LiFePO4 정전·흑연 정량).
- `12_inverse_problem_PSD.md`(서브C) : 전기화학 신호→입자크기분포 추출 선례·DOS/site-energy 해석·deconvolution.
- `13_competing_broadening_graphite.md`(서브D) : kinetic dispersion·접촉저항·조성 이질성·온도 경쟁 기작·흑연 마이크론 정량.
- `20_synthesis.md` : 삼각검증·갭·경쟁가설 분리·역문제 성립조건 사슬 커버맵·4-tier.
- `RADIUS_VERDICT.md` : ★종합 답변(타당성 판정·성립 조건·한계·필요 가정·실측 절차 권고·열린 문제).
- `PHASE_RADIUS_RESULT.md`(11항목)·`RADIUS_LEDGER.md`(12-col)·`50_report.md`(사용자 1–2p 요약).
- `.session/radius/` : 서브 brief·return 로그.

## Phase 0 — 연구질문·6축·전제 1차검증 (Steps 1–3) [master 직접]
- **Step 1** 연구질문 6축 확정(= Current Ground Truth 미확인 1–6). 각 축 = 1 서브 또는 master.
- **Step 2** 쿼리셋·DB(Google Scholar·CrossRef·arXiv·publisher)·포함(peer-review 1차·리뷰=진입점)/제외(예측 prepost·비관련 화학) 기준. seed 문헌 후보 열거(존재 확인용·조사결과 아님).
- **Step 3** **전제 1차 판정**: "Ω>2RT → 단일 입자 dQ/dV 델타" 를 모델 식(eq:Veq 비단조·Maxwell·spinodal)·기초 열역학으로 master 가 *논리적으로* 검증해 1차 tier 부여(문헌 보강은 Phase1 서브A). **Gate**: `00_scope.md` 저장.

## Phase 1 — 목적적 4 병렬 조사 (Steps 4–7) [master + 서브 A/B/C/D 병렬]
4 general-purpose 서브를 **동시 dispatch**(독립 subtopic·공유 가변상태 없음·각자 web search·각자 카드 파일 직접 Write·return 요약). 4-세션 고지 머리 필수(아래 Interfaces).
- **Step 4** 서브A → `10_single_particle_and_ensemble.md` : 미확인 1·2.
- **Step 5** 서브B → `11_size_dependent_thermo.md` : 미확인 3.
- **Step 6** 서브C → `12_inverse_problem_PSD.md` : 미확인 5 + 4(역문제 수학).
- **Step 7** 서브D → `13_competing_broadening_graphite.md` : 미확인 6 + 4(경쟁기작 정량).
- **Gate**: 4 카드 디스크 저장·각 항목 출처(DOI/URL)·4-tier·추측0·정독범위 명시(abstract-only 강등 표기).

## Phase 2 — 삼각검증·갭·경쟁분리·역문제 조건 (Steps 8–10) [master 직접 — CORE]
- **Step 8** 4 카드 master 정독 → 합의/논쟁/공백 분류·핵심 주장 ≥2 독립 삼각검증.
- **Step 9** ★**경쟁가설 분리**: 실측 "치우친 종모양" 을 (i) 반경 분포 (ii) kinetic 꼬리(Ch1 내장) (iii) 접촉저항/조성 이질성 (iv) 온도 — 로 분해, 각 **식별 신호**(C-rate 의존성·GITT 근평형·온도 의존·완화)와 **흑연 마이크론 정량 규모** 대조.
- **Step 10** ★**역문제 성립조건 사슬 커버맵**: 단일입자 델타 → U_j 분포 합성곱 → r→U_j 단조사상 → 분포 역변환, 각 고리 *충족/미충족/조건부* 판정. **Gate**: `20_synthesis.md`(4-tier).

## Phase 3 — 종합 verdict (Steps 11–12) [master 직접]
- **Step 11** `RADIUS_VERDICT.md` 작성: (1) 추정 타당성 판정(전체/부분/조건부/반증) (2) **성립 조건 목록**(근평형·내재폭≪분포폭·단조 r→U_j·전이 격리·반경 지배·입자 독립 등) (3) 각 조건의 흑연 현실 충족도·정량 (4) 한계·반례(kinetic 혼입·마이크론 표면에너지 미약 등) (5) **실측 절차 권고**(절차로 조건을 만족시키는 법: 저율 GITT·다온도·다C-rate 교차·독립 PSD 측정 검증) (6) 열린 문제. 모든 정량 = 출처. 4-tier.
- **Step 12** `PHASE_RADIUS_RESULT.md`(11항목)·`RADIUS_LEDGER.md`·`50_report.md`. **Gate**: 저장 완료. 토픽 종료 시 master commit(푸쉬 정책 — 미요청 시 commit 만).

## Implementation Interfaces
**(1) 서브 prompt 머리(4-세션 고지·필수)**: 역할=조사 작업 sub(web search + 카드 1개 Write)·경계=배정 축만·CORE 판단/verdict/종합 금지(master 전담)·범위 밖 자의작업 금지(모델·코드·메모리 수정 X·다른 카드 X)·허위 attribution 금지·self-contained(본 대화 컨텍스트 없음 — 경로·기준·schema 를 prompt 에 명기).
**(2) 조사 카드 schema(각 항목)**: `주장 | 근거문헌(저자·연도·DOI/URL) | 지배식/정량값(값·단위·조건·불확도) | 흑연 적용성 | 타당/한계 | 본 가설 관련성 | 정독범위(full/abstract-only) | tier(확정/근거미발견/추정/미검증)`.
**(3) 핵심 사슬(검증 표적)**: 단일입자 1차상전이 델타 → [입자 ensemble U_j 분포 합성곱] → [r→U_j 단조·기지 사상] → [분포 deconvolution] → 반경 분포. 각 고리 근거·조건·함정.
**(4) 경쟁가설 매트릭스**: 행=치우침 후보(반경분포·kinetic 꼬리·접촉저항분포·조성이질성·온도), 열=식별신호·정량규모(흑연)·문헌·분리가능성.
**(5) seed 문헌(검색 *존재* 확인용 출발점 — 조사결과 아님, 정독·확장 대상)**: Dreyer et al. *Nat. Mater.* 2010 (many-particle hysteresis, 10.1038/nmat2730) · Bazant *Acc. Chem. Res.* 2013 (10.1021/ar300145c) · Cogswell & Bazant *ACS Nano* 2012 / *Nano Lett.* 2013 (size-dependent phase diagram) · Meethong et al. *Adv. Funct. Mater.* 2007 (strain·size miscibility gap) · Wagemaker et al. (size effects) · McKinnon & Haering (lattice-gas/site-energy isotherm) · graphite staging 1차상전이(Dahn 1991·Ohzuku 1993) · single-particle electrochemistry(Uchida·graphite single particle). DVA/ICA 진단 리뷰. **전부 정독으로 검증 후 tier.**
**(6) Result 11항목·Ledger 12-col·보고 4-tier** = 헌법 양식.

## Test Plan
- 출처 폐쇄(모든 정량·기작 DOI/URL+가능시 페이지·출처없는 단정 0)·삼각검증(핵심 주장 ≥2 독립)·정독 증명(카드에 페이지/섹션, abstract-only 명시·tier 강등)·4-tier 무결.
- ★전제·역문제 사슬 각 고리 **충족/미충족/조건부** 정직 판정(공백을 충족으로 위장 X).
- ★경쟁가설(kinetic vs radius) **분리 신호** 제시(분리 불가면 그렇게 보고).
- 흑연 마이크론 vs LiFePO4 나노 **정량 규모 구분**(표면에너지 1/r shift 의 mV 규모 추정).

## Assumptions
- 1차 문헌 다수 접근 가능(불가분 시 abstract+2차인용 명시·tier 강등). Ch1 모델(평형 종+kinetic 꼬리)이 조사 기준선(사용자 가설은 그 위 신규 해석층). 사용자 "구형 입자·반경만이 U_j 결정" 은 *검증 대상 가정*이지 기정사실 아님(조사가 그 성립 범위를 규정). master + 4 서브 병렬로 충분(축 독립).

## Correction History
- 2026-06-30 1차본. 사용자 요청("v8 문건 + v11_final.py 관심·Ω≥2RT peak 형상=U_j 분포=반경 분포 추산 타당성 조사·research/radius 작성·글로벌 CLAUDE.md·메모리 준수 계획→조사")을 11-section 양식으로 구성. 조사 전용(.tex 초안·피팅 실행 제외). 병렬=목적적 4 서브(독립 축)·CORE 판단 master 직접·Workflow 금지·팝업 0. seed 는 검색 *존재* 확인용(값·방법 정독 후 tier). 본 계획 저장 후 바로 진행(GO).
