# PHASE 4.1–4.5 — Ch1 §8~§11 교과서 깊이 보강 Result

## Summary
박사님 "Ch1 §1~§7 충분, §8 이후 부실" 수용. §8 종합·§9 겹침·§10 종합모델식·§11 검증반증을 직관·worked example·진단표로 교과서 깊이 보강. §1~§7 불변(충분 판정 존중). Ch1 21p→24p.

## Step Range
Steps 91–110 (Phase 4.1–4.5).

## Inputs
- `graphite_ica_ch1.tex`(§8~§11). 계획 `2026-06-09-textbook-depth-expansion-plan.md`. 직전 d1925d0.

## Files Updated
- `graphite_ica_ch1.tex`:
  - [4.1] §8: 3×3 표 \emph{칸별 기전} 단락(위치/너비/높이 행 각 3칸 why)·Worked example 박스(Q_j=0.5Q_cell→FWHM 91mV·높이 4.9, −15℃ 78mV·5.6, 꼬리 12× → 저온 넓고 낮음).
  - [4.2] §9: 융합 개시 Worked example 박스(ΔU=100mV·FWHM 91mV 겨우 분리 → L_V~100mV서 융합, 저온 더 낮은 전류).
  - [4.3] §10: \emph{데이터→예측 walkthrough} 소절(S1~S4 1·2·3·4 + 외삽 검증 시험).
  - [4.4] §11: 경쟁 기전(배리어낮춤/확산/전하전달) 구별 \emph{진단표} + "반증의 칼날=보정 후 남는 전위 의존".

## Read Coverage
- ch1.tex §8(751–891)·§9(913–953)·§10(963–1016)·§11(1019–1043) 정독·보강.

## Execution Evidence
- 빌드 2-pass: exit0, overfull 0, undefined 0, 24p(21→24).

## Validation (4-tier)
- **확정 PASS** — G4.1~G4.4 보강 요소 grep 존재·빌드 clean.
- **확정 PASS** — worked example 수치 손검: FWHM=3.53×25.7=90.7≈91mV, 높이 0.5/(4·0.0257)=4.86≈4.9, −15℃ 22.2mV→78mV·5.6, 융합 ΔU 100mV vs FWHM 91mV. 전부 재현.
- **미검증** — Codex 교차검수: Ch2 보강까지 마친 뒤 일괄 foreground.

## Gate
**CONDITIONAL PASS** — 빌드·손검 PASS. Codex 말미 일괄.

## Confirmed Non-Changes
- §1~§7 본체 불변. 기존 식·라벨·식번호 불변(신규 verifybox/표/walkthrough만 add).

## Open Issues / Decision Queue
- 없음.

## Next
- Phase 5(Ch2 전반 clarity 보강) → 빌드 → Codex(Ch1·Ch2 일괄) → 종합 보고.
