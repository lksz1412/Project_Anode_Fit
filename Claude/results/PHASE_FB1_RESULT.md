# Phase FB1 — F-11 코드=부록 정리 (전역·최우선) Result

## Summary
본문(비부록)에 노출된 코드 언급(함수·클래스·플래그·상수)을 **전량 물리 언어로 치환하거나 부록으로 이전**. 규칙 = 헌법①·rubric A5(코드 함수명 본문 0·부록 전용). §3.5 코드 요구명세절을 부록으로 이전(D5), bib 코드 인용 평문화(D5). **부수 성과**: lcoomega 토글 박스 재구성으로 **식2.39 overflow(F-09)도 동시 해소**.

## Step Range
cumulative **FB step 6–11**.

## Inputs
- `comp_v24/INV_code_in_body.md`(본문 코드언급 17행 + §3.5).
- 대상: `ch1_sec05b_gr2L`·`ch1_sec16b_lcoomega`·`ch3v22_sec02b_sifr`·`ch3v22_sec02_cases`·`ch3v22_sec03_blend`·`ch3v22_notation`·`ch3v22_sec05_code`·`ch1v22_bib`·마스터 `ch3_si_v1.0.24.tex`. 각 전문/영역 정독.
- gate: `V1020_STYLE_RUBRIC.md` A5·`V1014_CODE_MENTION_AUDIT`(선례).

## Files Created
- 없음(정리 phase).

## Files Updated
- `_sections/ch1_sec05b_gr2L.tex`: `\code{GRAPHITE_STAGING_*}` 6곳 → 물리 언어("4-전이 기준선"·"5-feature 시드"·"XRD 사다리"). 해상도 사다리 물리 불변.
- `_sections/ch1_sec16b_lcoomega.tex`: `\code{include_electronic_entropy}` 3곳 제거. **토글 박스(식2.39) 재구성** — 코드플래그=cases → "전자항 옵션" 물리 표기(간결화로 우측 overflow 해소). 뒤 문단 boolean False/True→off/on 일관화.
- `_sections/ch3v22_sec02b_sifr.tex`: `\code{_regsol_dqdv}`·`\code{_regsol_binodal_xa}` 2곳 제거.
- `_sections/ch3v22_sec02_cases.tex`: `\texttt{BlendedAnodeDQDV.host_contributions}` → "블렌드 모델의 Si-host 기여".
- `_sections/ch3v22_sec03_blend.tex`: **Fig 2(`fig:blend-family`) 캡션** 물리 재작성(코드 클래스·메서드·인자 제거) + `host_contributions`·`elemental`·"코드판" 3곳 정리.
- `_sections/ch3v22_notation.tex`: `\code{si_case}` 표 행 → "Si 케이스(원소 Si·SiO_x·SiC)"; `f_Si` "코드 토글" 제거.
- `_sections/ch3v22_sec05_code.tex`: 제목의 `\code{BlendedAnodeDQDV(...)}`·"예고" 제거 → "블렌드 합성 코드 요구명세"(D5 부록 이전 정합).
- `ch3_si_v1.0.24.tex`(마스터): sec04_mech 뒤 `\appendix` 삽입 → §3.5 코드 요구명세절이 **부록**으로 이전(D5).
- `_sections/ch1v22_bib.tex`: `\code{Anode_Fit_v1.0.19}` → 평문 `Anode\_Fit v1.0.19`(D5, 내부 데이터 출처 유지).

## Read Coverage
- 전문 정독: `ch1_sec05b_gr2L`(1–197)·`ch1_sec16b_lcoomega`(90–159 + 편집영역)·`ch3v22_sec03_blend`(201–224 캡션)·`ch3v22_notation`(24–37)·`ch3v22_sec05_code`(1–8 헤더)·마스터 입력부.
- 부분: sifr·cases 편집 행 문맥.
- 부록 codemap(ch1_appB) staging 상수 미수록 확인 → 코드↔사다리 대응은 CODE_GUIDE_v24 소관(본문 0으로 A5 충족).

## Execution Evidence
```
빌드(3챕터, FB1 후): ch1 0-err/91p · ch2 0-err/28p · ch3 0-err/20p · undefined ref/cite 0 (sec05_code 부록 이전 참조 무결)
본문 코드토큰 grep(부록·주석·매크로정의 제외): 0건 (FB1 게이트 PASS)
식2.39(eq:lcoomega-toggle) 23쪽 렌더: 박스 여백 내 완전 수렴(잘림 0) — F-09 해소
코드 sha256: f230f59b… (무변경 — .py 미접촉)
```

## Validation (게이트별)
- **(1) 본문 코드토큰 0** — PASS(grep 공집합, 출력 인용). 부록(ch1/ch2 appB·§3.5 이전분) 외 0.
- **(2) 부록 이전 무손실** — PASS(§3.5 → 부록 A, `\ref{sec:si-code}`·`\ref{ssec:code-caseset}` 무결 = undefined 0).
- **(3) 빌드 GREEN** — PASS(0-err·0-undef-refcite·페이지수 baseline 유지 91/28/20).
- **(4) Fig 2 캡션 코드 부재** — PASS(렌더 캡션 물리만; line 178 히트는 `%` 주석 비렌더).
- **부수: F-09** — 식2.39 overflow 해소(렌더 확인).

## Gate
**PASS_FB1_CODE_TO_APPENDIX** (본문 코드토큰 0 + 부록 이전 무결 + 빌드 GREEN + 캡션 물리).

## Confirmed Non-Changes
- 코드 `.py` 무변경(sha256 f230f59b).
- 물리 내용·식·`\label`·식번호 불변(코드명 문구만 치환/이전). 해상도 사다리·토글 물리·블렌드 물리 전부 보존.
- 부록 파일(ch1_appB 등) 기존 코드 수록분 불변.

## Confirmed Non-Changes 보강(경계)
- gr2L 등 `%` 소스 주석 내 "코드" 표현은 비렌더라 미접촉(F-11=렌더 대상). 
- lcoomega 판번호(v1.0.19/v1.0.23)·gate 라벨(G1·R2)·"브리프"·"★적대적 검토 대응" 수사문답은 **register(FB3) 소관** — FB1서 미접촉.

## Open Issues / Decision Queue
- **§3.5(현 부록) 잔여 process 언어**: "R6 코드가 구현할…"·"doc-leads"·"N9 이월"·"GS-1/GS-2" 등 개발 프로세스·작업 라벨이 부록 본문에 다수. 부록이라 코드=허용이나, **회사 공개 관점에서 register(FB3) 정리 또는 절 전체 존폐**는 추가 판단 대상(사용자 결정 여지 — 현재는 D5 "부록 이전"만 집행).
- "코드"라는 **단어**(코드 합성 규칙 등, sec01_map:125)는 코드 \emph{식별자}가 아니라 prose framing → **FB3 register** 소관으로 이월.

## Next
**FB2 — F-06 조판 전역 설정(preamble), cumulative step 12.** `common_preamble_v1024` 여백 22→26mm·줄간 1.12→1.18·문단 0.45→0.6em·microtype 도입. 전/후 렌더 비교. FB2 후 overflow 재스캔(FB5).
