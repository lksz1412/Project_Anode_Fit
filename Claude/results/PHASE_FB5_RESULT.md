# Phase FB5 — F-07 E.3 서지 off-page + F-09 식2.39 재확인 + 전역 overflow 픽셀-스캔 Result

## Summary
페이지-밖 overflow 전수 처리. **F-07**: 부록 E.3(sec:sc-p35)의 `\item[\textbf{①..⑤}]` 광폭 optional-label enumerate가 좌측 행잉 off-page → `itemize[label={}]` 본문 lead-in 전환. **F-09**: 식2.39(전자항 옵션 cases) FB1 해소 렌더 재확인 clean. **전역 픽셀-스캔**(149쪽 80dpi, 우측 여백 content 검출)으로 사용자 미지목 실 overflow 3건 추가 발견·수정: Table 11(코드 인자 `l l l l`), 식2.18(vib 주석 컷), 식2.36(광폭 사슬). 물리·식번호·label 불변.

## Step Range
cumulative **FB step 31–35**.

## Inputs
- `ch1_appE_selfconsistent.tex`(E.3 = §sec:sc-p35, 부록 E 3번째 소절).
- 픽셀-스캔 발견분: `ch1_appB_codemap.tex`(tab:inputs=Table 11)·`ch1_sec14_lcodecomp.tex`(식2.18 eq:lco-slots·식2.19 eq:lco-decomp)·`ch1_sec16b_lcoomega.tex`(식2.36 eq:lcoomega-kernel).
- 도구: `pdftoppm`(149쪽 렌더)·PIL 우측여백(x>90.5%W, 헤더/푸터 제외) dark-pixel 검출.

## Files Created
- 없음(스캔 산출 이미지는 scratchpad).

## Files Updated
- `ch1_appE_selfconsistent.tex`: **F-07** E.3 `enumerate`+`\item[\textbf{①..⑤}]`(5항) → `itemize[leftmargin=1.7em,itemsep=0.4em,label={}]`+`\item \textbf{①..⑤}`(볼드 lead-in을 본문으로 이동 → 좌측 행잉 제거). P3-5 5항 내용·`\cite` 전부 보존.
- `ch1_appB_codemap.tex`: **Table 11**(tab:inputs) 열지정 `{l l l l}`(자연폭·비줄바꿈) → `{@{}p{0.29}p{0.07}p{0.19}p{0.29}@{}\textwidth}`(줄바꿈 p-열) — 우측 컬럼 off-page 해소.
- `ch1_sec14_lcodecomp.tex`: **식2.18**(eq:lco-slots) vib 슬롯 주석에서 "--- Chapter 1 Part T Einstein 절"(직후 본문 중복) 제거 → 컷 해소. **식2.19**(eq:lco-decomp) 셋째 underbrace "몰당·\S\ref{sec:lco-electronic}"(인접 본문 존재) 축약.
- `ch1_sec16b_lcoomega.tex`: **식2.36**(eq:lcoomega-kernel) `equation` → `multline` 3줄 분할(곡률 / ⟹박스 / →극한) — 식번호 2.36·label·물리 불변.

## Read Coverage
- 렌더 정독: E.3(p91–92)·식2.39(ch2 p24)·Table 1 노테이션(p8)·LCO staging 표(ch2 p4)·식2.36(ch2 p23)·p38/p76 박스식(오탐 확인).
- 픽셀-스캔 전수: ch1 98 + ch2 30 + ch3 21 = 149쪽. 임계(dark>30·maxX>91.5%) 초과 = 수정전 6쪽 → 수정후 3쪽(전부 오탐).

## Execution Evidence
```
픽셀-스캔 수정전 flagged 6쪽: ch1 p86(98.3%·40행=Table11 실) · ch2 p13(98.3%=식2.18 실) · ch2 p23(98.3%=식2.36 실)
  + 오탐 3쪽: ch2 p24(식2.39 박스 여백내) · ch1 p76(식1.129 박스 여백내) · ch1 p38(식1.73 박스 여백내)
픽셀-스캔 수정후 flagged 3쪽: p24·p76·p38 (전부 오탐 — 박스식 여백 근접·off-page 아님, 렌더 확인)
실 overflow 3건 수정후 렌더 재확인: Table11 컬럼 wrap OK · 식2.18 vib줄 여백내 · 식2.36 multline 3줄 여백내(식번호 2.36 우하단)
Overfull \hbox 대형(585/200/110/99pt) = longtable/tabular 자연폭 측정 오경보(렌더 정상 — ch1 p8·ch2 p4 확인), 가시 overflow와 무관
빌드(3챕터): ch1 0-err/98p · ch2 0-err/30p · ch3 0-err/21p · undefined ref/cite 0
식번호 불변: eq:lco-slots=2.18 · eq:lco-decomp=2.19 · eq:lcoomega-kernel=2.36 (multline=단일 번호)
```

## Validation (게이트별)
- **F-07 E.3 off-page** — PASS(itemize 전환, p91–92 렌더 5항 전부 여백내·좌행잉 소거).
- **F-09 식2.39** — PASS(FB1 해소 재확인, p24 cases 박스 여백내).
- **전역 overflow 재스캔(FB2 조판 후)** — PASS(149쪽 픽셀-스캔; 실 overflow 3건 발견·수정, 잔여 3 flagged=오탐 렌더 확인).
- **빌드 GREEN** — PASS(98/30/21·undefined ref/cite 0).
- **식번호·label 불변(F1)** — PASS(2.18/2.19/2.36 불변; multline 단일 번호; label 키 보존).

## Gate
**PASS_FB5_OVERFLOW** (F-07·F-09 렌더 clean + 전역 픽셀-스캔 실 overflow 3건 소거 + 빌드 GREEN + 식번호 불변).

## Confirmed Non-Changes
- 코드 `.py` 무변경(sha256 f230f59b). 식번호·`\label` 키·물리 내용 불변.
- 식2.19 underbrace에서 `\S\ref{sec:lco-electronic}` 1개 제거는 **의도적 주석 축약**(대상 label 존치·인접 본문·식2.18 elec줄이 동일 ref 보유 → 상호참조 손실 0, 빌드 undefined 0).

## 비고
- **Overfull \hbox 경고 ≠ 가시 overflow**: 대형 hbox 경고(585pt 등)는 longtable 다중패스·tabular 자연폭 측정 산물로 렌더는 여백내(확인필). 사용자 지목 F-07/F-09는 역으로 hbox 경고 無. → GREEN 게이트(0-err·0-undef)가 hbox 경고 무시함은 타당. 가시 overflow는 픽셀-스캔이 정답 도구.
- **오탐 3쪽**(p24·p38·p76): `\boxed{}` 식이 우측 여백에 근접하나 텍스트폭 내. 조치 불요.
