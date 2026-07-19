# Phase R1 — 문건 저작(9창 경쟁·체리픽·master 통합) Result

## Summary
9창 경쟁 저작(W1–W9) → **W9 를 3소절 공통 base 로 체리픽** → master 재조정 후 3장에 통합. 신규 소절 3개
(@5 stage-2L·@3 Si Frumkin·@3 LCO per-peak Ω+#7+전자항 토글)를 `_sections/` 신규 파일로 저작·`\input` 배선,
신규 인용 3건 등재. **빌드 0-error·STRUCTURE_CHECK PASS**. 부수 성과: R0 에서 JSON 으로 덮여 커밋된
`ch1_graphite_v1.0.24.tex` **마스터 손상을 복구**(v1.0.23 셸 + 로그 확인 순서로 재구성).

## Step Range
cumulative R-step 10–14 (R2 = 5–9 이어받음).

## Inputs
- 경쟁 저작 9창 `results/comp_R1/{W1..W9}/{gr_2L,si_fr,lco_omega}.tex`+`NOTES.md`. base = **W9**(전 소절 전독·정합·정직한계 최강).
- 사양: `REFLECT_SEED_TABLE.md`(@3/@5/토글/#7 확정 물리·서지).
- 기존 문건(정합 대상 전독): `ch1_sec07_broadening`(sec:broadening-class 분류)·`ch1_sec10_sum`(tab:staging 4전이)·`ch1_sec04_hys`(eq:gpp/spinodal)·`ch1_sec03_center`(eq:Uj/fig:UjT)·`ch1_sec05_width`·LCO `sec13–16`·`ch3v22_sec02_cases`·3장 bib.
- 서지 웹검증: schmitt2022 = ChemElectroChem **9, e202101342 (2022)** DOI 10.1002/celc.202101342(탈리튬 operando XRD: stage-2L 43℃ 뚜렷·0℃ 부재).

## Files Created / Updated
- **신규 소절 3**: `_sections/ch1_sec05b_gr2L.tex`(§5 뒤)·`_sections/ch1_sec16b_lcoomega.tex`(ch2 §16 뒤)·`_sections/ch3v22_sec02b_sifr.tex`(ch3 §3.2 뒤).
- **마스터 복구/배선**: `ch1_graphite_v1.0.24.tex`(**손상 JSON→LaTeX 셸 재구성** + sec05b `\input`)·`ch2_lco_v1.0.24.tex`(+sec16b)·`ch3_si_v1.0.24.tex`(+sec02b).
- **서지 등재**: `ch1v22_bib.tex`(+`schmitt2022`)·`ch3v22_bib.tex`(+`artrith2018` JCP 148,241711(2018)·+`verbrugge2017` JES 164,E3243(2017)). ch2 신규 키 0(기존 재사용).
- 빌드 산출 `ch{1,2,3}_*.pdf` 갱신(89/27/19 p).

## Read Coverage
- W9 `gr_2L`·`si_fr`·`lco_omega` 전독 + `NOTES.md`. W1/W3/W4/W5/W6/W7/W8 요약(정직 플래그 교차 확인 — 분류 충돌·ΔS·toggle 기본값 만장일치 지적).
- `test_gates_v1024.py`(G1 LCO 경로 = **298 단독**·`lco_entropy`(∂U/∂T)@298 이 ΔS_e 포함 → 토글 기본 ON 필수 확인).
- 라벨 실재 확인(grep): eq:gpp/spinodal/gxi/Uj/fig:UjT/eqpeak/wbase/xieq/tab:staging/sec:broadening-class(흑연)·LCO 15종·ch3 6종 전부 존재.

## Execution Evidence
- **빌드**(xelatex 3-pass×2라운드, ch1→ch2→ch3): **ch1 0-err 89p / ch2 0-err 27p / ch3 0-err 19p**(각 +2p = 소절 1개분).
- **undefined ref/cite = 0** (로그의 'undefined' 3줄/장은 전부 한글폰트 italic shape 경고 — benign·기존). 신규 eq 라벨 aux 등록: gr2l-{disc,split,box,mu}·lcoomega-{kernel,hash7,Tref,toggle}·sifr-{width,kernel,V,dVdtheta,blend}. 신규 cite `bibcite` 해소: schmitt2022·artrith2018·verbrugge2017.
- **STRUCTURE_CHECK PASS**: 3장 labels dup**0**·refs unresolved**0**·cite-undef**0**·bib-uncited**0**·env-pairing**0**(ch1 43 bibitems·ch2 15·ch3 36).
- `swiderska2019`·`LastPage` multiply-defined = xr `\externaldocument` 교차 aux 산물(D22 의도적 장간 중복·기존, 내 신규 아님 — 각 bib 1회 확인).

## Validation
- PASS_R1_DOC: (1)3장 빌드 0-err [확정] (2)undefined ref/cite 0 [확정] (3)STRUCTURE_CHECK 5항 PASS [확정] (4)신규 소절 3·인용 3 해소 [확정] (5)마스터 손상 복구·기존 셸 정합 [확정].

## Gate
**PASS_R1_DOC = PASS.**

## Confirmed Non-Changes (master 재조정 — 정합 우선)
- **분류 불변(핵심)**: gr_2L 은 §7(sec:broadening-class)의 두-상/고용체 분류를 **뒤집지 않음**. W9 초안의 "4 두-상+1 고용체"(dilute/3→2L 두-상 재분류)는 §7 이 같은 Dahn1991 로 "dilute·4→3·3→2L = 고용체"라 한 것과 **직접 충돌** → master 가 판정자+stage-2L 온도서명만 얹고 분류는 §7+피팅 Ω 로 **위임**(P5·gate-6·gate-7). 5-feature 세분은 **추가 후보**(선택 코드 시드)로만.
- **tab:staging 미편집**(P5): 중앙쌍 ΔS(+15/−14, Δ=29)는 초기값(0/−5)을 **피팅으로 갱신하는 대상**으로 서술, 표 수치 무변경.
- **토글 기본값 = 코드 정합**: 문건을 W9 초안 "기본 False"→**"기본 True(완전 모델·G1 bit-exact)·False 옵션"**으로 정정. 상온 커브는 토글 무관 불변(사용자 "커브 구할땐 빼고" = 값선택 무관 성립), 토글은 ∂U/∂T(가역열)만 가름.
- **역사적 명칭 보존**(gate-7): stage 라벨·ver.N/Chapter N 구분 명시. 코드 미변경(R2 확정분 유지).

## Open Issues / Decision Queue (R3·회사 피팅 위임 — 실수정 X)
- stage-2L 정량(0.30 mV/℃·병합~10℃): 다온도 데이터 없이 미검증(tier B). schmitt2022 는 부호·경향 독립 근거이나 0.30 정량 원저 값 아님.
- Ω_Si·Ω_j^cat 점값: 범위 시드(피팅 위임). schmitt2022 저자 전체·권쪽 = 사용 시 Crossref 최종 대조.
- 5-feature 세분·per-peak Ω 는 기준(4전이·균일폭) 대비 additive 후보 — R3 적대검수 대상.

## Next
R3(반영 검증: T-split 재현·bit-exact 재확인 + 9창 union 적대검수) → R4(MERGE_READINESS·HANDOVER·INDEX·commit·push). 다음 cumulative step 15.
