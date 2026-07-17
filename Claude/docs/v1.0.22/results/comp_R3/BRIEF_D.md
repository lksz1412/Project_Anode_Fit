# BRIEF O-D — 신 Ch2(LCO) 이음매·추가 텀 정합 초안 (v1.0.22 R3)

## 공통 규칙 (R2 와 동일 — 위반 시 기각)
1. **초안 전용**: 기존 파일 수정 금지 — 산출물은 `comp_R3/D_seams/` 신규 파일만. git 조작·`Codex/` 접근 금지.
2. 서지 = `results/V1022_REFERENCE_LEDGER.md` V1 키만. 기호·라벨·수식·자산 임의 변경 금지.
3. 어조 = 기존 본문 동일(한국어 수식-구동 교과서체).
4. **전환표의 "현행" 열은 축자(verbatim) 인용 의무** — R2 에서 의역 38행이 기계 매칭 불발(교훈 1). 원문에서 복사하라.
5. 조기 저장(완성분 즉시 파일로).

## 맥락
`/home/user/Project_Anode_Fit/Claude/docs/v1.0.22/` 의 신 Chapter 2 = `ch2_lco_v1.0.22.tex` 가 조립하는 `_sections/ch2v22_sec00_intro·ch2v22_notation·ch1_sec11~17·ch2v22_bib`. 흑연 장(신 Ch1)은 R2 로 완성됐고(구획 전환 S-009·부록 C/D S-010·CLT/CNT A-011/012·다리 A-013 — `results/V1022_CHANGE_LOG.md` 참조), 신 Ch2 에는 R3 이월분이 남아 있다. Ch1 라벨은 xr(`\externaldocument`)로 live 해소된다.

## 작업 (산출 = `comp_R3/D_seams/`)
1. **`SEAM_PLAN_R3.md`** — 전환표(축자): 
   - W 9건(`results/comp_R2/A_seams/W_RULE.md` §2b 목록 그대로 — 본 장 8·본서 후보 1[`ch1_sec11:45` tier 등급: 3장 공통 규약인지 판정 포함]).
   - L1 1건: `ch1_sec15:319` "(Chapter 2 의 완전식과 같은 구조)" — 구 열특성 장 지칭 → "Chapter 1 Part T"(xr — 대상 식/절 라벨을 ch1 쪽에서 실확인해 live \S\ref/\eqref 로).
   - **신규 전수 재스윕**: 신 Ch2 구성 파일에서 `Chapter [12]|그 문건|본 문건|이 문건|별도 컴파일|Ch1|Ch2` 잔재 전수(주석 제외) — R1B 목록 밖 신규 검출 포함, [전환 대상/정당 지칭/정상] 분류.
2. **`INTRO_NOTATION_FINAL.md`** — `ch2v22_sec00_intro`(R1 초판)·`ch2v22_notation`(R1 초판) 확정판 초안: "Chapter 1 의 식 번호를 그대로 인용" 문구가 xr live 참조 체계와 정합한지, 기호표 계승 항목의 라벨(eq:Uj 등)이 실존하는지 전수 확인 + 필요한 최소 개정문.
3. **`ADDTERM_CHECK.md`** — "추가 텀만" 방식 정합 점검: `ch1_sec11~17` 각 절 서두가 흑연 결과를 받는 방식(xr 참조·서술)이 신 구조에서 자연스러운지 절별 판정표(개정 필요 시 축자 현행+개정안 — 대규모 재서술은 제안만).

## 게이트
전환표 전수·라벨 실확인(추측 0)·논지·수식 무변경. 완료 보고 = 산출 목록+건수 통계+판단 보류.
