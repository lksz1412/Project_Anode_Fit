# Phase A.1 — 식 줄나눔(가독) Result

**Date**: 2026-06-06 · **Plan**: `2026-06-06-ch1-sec6-statmech-accessibility-plan.md` · **Step Range**: 5–7

## Summary
사용자 지적 eq#29(=eq:superpose) PDF 잘림을 줄나눔으로 해결 + 잔여 overflow 디스플레이식 전수 교정. 전부 \emph{레이아웃만} 변경(수식 내용·라벨·번호 불변).

## Step Range
Steps 5–7 (A.1). 다음 = 8 (A.2).

## Files Updated (`graphite_ica_ch1.tex`) — 레이아웃 전용
- **eq:superpose(#29)**: 1줄 → `\boxed{\begin{aligned}}` 2줄(적분식 / L_V·r_a 정의). 85.9pt overflow → 0.
- §lag verifybox: 긴 인라인 적분 $r_j=r_j(q_a)\exp[-\!\int dq'/L_q]$ → `\[ \]` 디스플레이. 53.6pt → 0.
- eq:arrhenius(#32) y(T) 박스: → 2줄 aligned.
- §synth S4 `equation*`(ln L_q + T_* 정의): → `gathered` 2줄. 7.67pt → 0.
- 기호표 L158 단위셀: `\footnotesize`. 7.86pt → 0.

## 잔존(허용)
- L162 k_eff 표 행 **1.51pt**(≈0.05mm, 비가시) — 미세 표 셀, 식 잘림 아님. 미교정(과수정·risk 회피).

## Read Coverage
- §synth Arrhenius 영역(L755~776) 정독으로 overflow 식 \emph{정확 식별}(추정 X — equation*가 범인, 박스 #32 아님 확인). 편집부 재확인.

## Execution Evidence
- xelatex ×다회 → `!`0·undefined 0·**19p·887줄**. Overfull: 디스플레이 식 **0**(L162 1.51pt 표 셀만).
- .aux: **eq:superpose=29** 확정(사용자 식).

## Validation (4-tier)
- **확정**: 모든 디스플레이 식 잘림 0. 수식 내용 불변(eq:superpose 적분·도메인·정의 / arrhenius y(T)·ln L_q / verifybox 적분 — 글자 단위 보존, 줄바꿈만). 빌드 GREEN.
- **G-build** PASS. (레이아웃 전용이라 Codex 교차는 A.5 전영역 패스에 포함.)

## Gate
**PASS_A1_EQ_LINEBREAK**.

## Confirmed Non-Changes
- 수식 값·라벨·번호. §1~5 내용(notation footnotesize·verifybox display 는 레이아웃만).

## Next
A.2: §1~5 경량 확인(R.9 Codex DOCUMENT CLEAN + A.1 레이아웃 변경 content-preserving 확인; 교차모델 §1~5 는 A.5 전영역 패스가 커버). 이어 A.3 신규 절.
