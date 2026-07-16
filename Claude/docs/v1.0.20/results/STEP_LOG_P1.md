# STEP_LOG P1 — 서지 원장 phase 스텝 이력

## Step 11 — P1 세부 계획서 저장
- `plans/PLAN_P1_references.md`. 커밋 9640703.

## Step 12 — 무인용 주장 확정 목록
- 어간 확장 재스캔(보고/관측/측정/알려/제안/실험적/문헌, ±3행 cite 부재) 실행 → 킥오프 목록과 병합·master 선별 → `V1020_P1_CITATION_BASELINE.md` U1–U12(담당 phase 배정) + 유지/기각/노이즈 분리. U12(sec01:170)는 P2 대상 정독에서 모델 부호 서술로 확인 — 기각 예정 기입.

## Steps 13–15 — 기존 42건 실재 검증 (sub-agent 단독·순차)
- 산출 `V1020_REFLEDGER_DRAFT_existing.md`(42행·Crossref/출판사 1차 대조). 집계: **V1 36 · V2 3 · FAIL 2 · 내부 1**.
- FAIL: ml2024(기재 DOI 가 실재 타 논문[JMPS 190,105727]을 가리킴 — 실제 105726·출판판 저자 순서 상이)·leviaurbach1999(1997 JEAC 논문 제목 + 1999 EA 리뷰 서지의 혼합).

## Step 16 — master spot-check (agent 자기보고 불신뢰 규율)
- 직접 재검증 5건: ml2024(JMPS 190,105726·Shojaei 제1저자 — 독립 확인)·leviaurbach1999(1999 EA 45,167–185 실제 제목 = Frumkin 리뷰 — 확인)·dreyer2010(NM 9,448–453·10.1038/nmat2730)·bernardi1985(JES 132(1),5–12·10.1149/1.2113792)·xia2007(JES 154(4),A337·10.1149/1.2509021). **5/5 초안과 일치.**

## (Step 16b — 계획 정정) bib 정정 P1 직접 반영
- 계획서 Non-goals 는 "bib 수정 X" 였으나, 서지 정정은 원장 확정과 원자적으로 묶이는 P1 소관으로 판단 변경(Correction — 담당 phase 분산 시 정합 위험). C-001~C-008 등재 후 ch1_bib(5건)·ch2_bib(3건) 반영. 커밋 b9951ab.

## Steps 17–18 — 신규 후보 검증 (sub-agent 단독·순차)
- 산출 `V1020_REFLEDGER_DRAFT_candidates.md`: 9/9 실재(V1 9·V2 1[safran1987 권 메타 충돌]·보너스 bakerverbrugge2018 V1). 확정: MSMR = "Multi-Species, Multi-Reaction"(2018 Baker–Verbrugge 가 명명 원전; 2017 Verbrugge 외 = 열역학 원전, byline 이니셜 없음)·kohlrausch1854 이중 권번호(Pogg. 91 = AdP 167, stretched-exp 는 2부 179–214)·ashcroftmermin1976 쪽수 인용 금지(장 수준만).

## Step 19 — 원장 확정 + spot-check 2건
- marianetti2004(NM 3,627–631·10.1038/nmat1178)·msmr_origin2017(JES 164(11),E3243·10.1149/2.0341708jes) 직접 재검증 — 일치. `V1020_REFERENCE_LEDGER.md` 확정(기존 42 + 신규 12, V1만 인용 가능 규칙 명문).

## Step 20 — baseline↔원장 정합
- U1–U12 전 항목에 해소 수단 배정 완료(기존 키 재인용 7·신규 키[dreyer2011/safran/vanderven 등] 병용 3·기각 후보 1·선택 1). P2~P5 에서 처리 결과 기입, P7 gate 가 전건 확인.

## Step 21 — 기록 저장
- 본 STEP_LOG·RESULT_P1·ledger P1 행.

## Step 22 — 커밋+푸시
- (커밋 해시는 커밋 후 ledger 에 기재.)
