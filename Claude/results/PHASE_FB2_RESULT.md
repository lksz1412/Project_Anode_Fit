# Phase FB2 — F-06 조판 전역 설정 (preamble) Result

## Summary
문서 밀도 완화(F-06). 3 마스터 공통 `common_preamble_v1024.tex` 단일 소스에서 여백·줄간격·문단간격을 **약간씩** 넓히고 `microtype`(protrusion) 도입. 물리·내용 불변, 조판만.

## Step Range
cumulative **FB step 12–14**.

## Inputs
- `_sections/common_preamble_v1024.tex`(전문 정독 1–84). 3 마스터가 공통 \input(ch1_graphite:8·ch2_lco:6·ch3_si:6). ※`ch1_preamble`·`ch2_preamble`는 v1.0.24 미사용 레거시(마스터 미입력) — 미접촉.
- `INV_overflow.md`(조판 레버).

## Files Created
- 없음.

## Files Updated
- `_sections/common_preamble_v1024.tex`: (1)여백 `margin=22mm`→`25mm`(텍스트폭 166→160mm·행길이 단축) · (2)`\setstretch{1.12}`→`{1.16}`(줄간격) · (3)`\parskip 0.45em`→`0.55em`(문단간격) · (4)`\usepackage[protrusion=true,expansion=false]{microtype}` 신설(XeLaTeX=protrusion만).

## Read Coverage
- 전문 정독: `common_preamble_v1024.tex`(1–84).
- 렌더: ch1 20쪽 전/후 비교(`fb2_before/after-20.png`·`fb2_compare.png`).

## Execution Evidence
```
빌드(3챕터, FB2 후): ch1 0-err/98p · ch2 0-err/30p · ch3 0-err/21p · undefined ref/cite 0
페이지수 변동(밀도↓ 대가): ch1 91→98(+7)·ch2 28→30(+2)·ch3 20→21(+1)
전/후 렌더: fb2_compare.png (좌 22mm/1.12/0.45 | 우 25mm/1.16/0.55+microtype) — 여백·줄간 완화 육안 확인, 사용자 전달
```

## Validation (게이트별)
- **(1) 빌드 GREEN** — PASS(3챕터 0-err·undefined ref/cite 0).
- **(2) 전/후 렌더 밀도 감소** — PASS(비교 이미지 생성·사용자 전달; 여백·줄간·문단 완화 시각 확인).
- **(3) 신규 overflow 유발** — FB5 재스캔 이월(여백 축소로 일부 overfull 변동 가능 — INV_overflow 는 FB2 후 재작성).
- **(4) 3 마스터 preamble 정합** — PASS(단일 공통 소스라 자동 정합).

## Gate
**PASS_FB2_TYPESET** (빌드 GREEN + 전/후 렌더 밀도↓ + 단일 소스 정합).

## Confirmed Non-Changes
- 코드 `.py` 무변경(sha256 f230f59b). 물리·식·`\label`·내용 불변.
- `ch1_preamble`·`ch2_preamble`(레거시 미사용) 무접촉. 그림 규약(외부이미지 금지·TikZ) 불변.

## Open Issues / Decision Queue
- **값 조정 여지**: 25mm/1.16/0.55em 은 "약간씩" 기본값. 사용자가 더/덜 원하면 재조정(전달한 비교 이미지 기준).
- **페이지수 변동 → 하류 갱신**: HANDOVER/INDEX/MERGE_READINESS 페이지 참조는 **FB7 마감서 새 페이지수(98/30/21 — FB3~6 후 재확정)로 갱신**.
- **overflow 재스캔**: 여백 변경으로 넘침 landscape 변동 → **FB5서 재빌드 후 재스캔**(INV_overflow 갱신).

## Next
**FB3 — F-04+F-10 문체·용어 전역 스윕, cumulative step 15.** 입력 = `INV_register_titles_prose.md`(offender ~94)·`TERM_DECISION_TABLE.md`·`V1020_STYLE_RUBRIC`(A~G)·`V1014_TONE_AUDIT`(79). 제목 스윕 → 본문 register+용어 단위 루프(챕터별). 최대 phase.
