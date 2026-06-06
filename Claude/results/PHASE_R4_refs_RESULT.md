# Phase R.4 — caveat·인용 보강 Result

**Date**: 2026-06-03 · **Plan**: `2026-06-03-ch1-rerevision2-foundation-first-plan.md` · **Step Range**: 32–35

## Summary
C9 인용 보강 — 실제 공백 2건(Newman & Thomas-Alyea 보존·다공전극; Bloom DVA/ICA 기법)만 추가. 완화시간 분포는 기존 svare2000/johnston2006/lindsey1980 으로 충분(중복 회피). 새 DOI·서지는 웹 검증.

## Step Range
Steps 32–35 (R.4). 다음 = 36 (R.5).

## Files Updated (`graphite_ica_ch1.tex`)
- §intro ICA 정의에 `\cite{bloom2005,dubarry2012}` 추가.
- §stage 전하보존(다공전극 implicit μ)에 `newman2004` 추가.
- thebibliography: `newman2004`·`bloom2005` 2 bibitem 추가(총 17).

## 인용 검증 (웹, 출처 정확성)
- **bloom2005**: WebSearch 로 확정 — DOI **10.1016/j.jpowsour.2004.07.021** = "Differential voltage analyses of high-power, lithium-ion cells. 1. Technique and application"(단수), \emph{J. Power Sources} \textbf{139}, 295 (2005), Bloom·Jansen·Abraham et al.(Argonne). 초안 제목 복수("applications") 오기 → 단수 교정. vol/page/year/DOI 확정.
  - (구분: Part 2 = p304/DOI ...022 confirmed; Part 1 = p295/DOI ...021 confirmed — 혼동 방지.)
- **newman2004**: J. Newman & K. E. Thomas-Alyea, \emph{Electrochemical Systems}, 3rd ed., Wiley-Interscience (2004), ISBN 978-0-471-47756-3 — 표준 교재(확정).

## Read Coverage
- §intro·§stage 인용 삽입부 + thebibliography 전체 재확인.

## Execution Evidence
- 빌드: xelatex ×2 → `!`0·undefined ref/cite **0**(새 citation 2건 정상 resolve)·**18페이지**·837줄.

## Validation (4-tier)
- **G-build**: PASS — undefined 0(17 bibitem 전부 resolve).
- **출처 정확성**: 확정 — bloom2005 DOI/vol/page 웹 검증, 제목 오기 교정. newman2004 표준 교재.
- **G-grounding**: PASS — 보존(Newman)·ICA 기법(Bloom) 공백 메움.

## Gate
**PASS_R4_REFS**.

## Confirmed Non-Changes
- 기존 15 bibitem·본문 인용 위치: 보존. 완화시간 분포 인용 추가 안 함(기존 충분 — 중복 회피, 정직 판단).

## Open Issues / Decision Queue
- 없음. R.5 = 전영역 Codex 재리뷰 + 적대 재검증 + 사용자 Decision Gate.

## Next
R.5 (Steps 36–40): Codex 전영역 재리뷰(C1~C11 교정 확정결함 0 확인) + Claude 적대 재검증(청킹·G-follow/usable) + 최종 result + Decision Gate(4-tier).
