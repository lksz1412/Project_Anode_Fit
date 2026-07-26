# 2026-06-02 Claude Final Full 10-Pass Review Plan

## Summary

Claude 병렬 최종 작업물 전체를 Codex Chapter 1 V4 검수와 같은 10-pass 방식으로 검수하고, 수정이 아니라 검수의견을 작성한다. 대상은 Claude handover가 최종본으로 지정한 `graphite_ica_ch1_rebuilt.tex`~`graphite_ica_ch5_rebuilt.tex`, `graphite_ica_full_rebuilt.tex`, `graphite_ica_refs_rebuilt.tex`이다. Ch6는 별도 파일이 삭제되고 Ch1 부록 B로 흡수된 상태이므로 독립 chapter로 검수하지 않는다.

## Current Ground Truth

- Claude handover `HANDOVER_RB_2026-06-02b.md`는 Ch6 해체, Ch2~5 fine review, 통합본 concat 완료를 주장한다.
- Codex의 직전 기준은 Chapter 1 V4에서 `chi_j`와 `beta_j` 동일시 금지, Heaviside/step-function형 support 표현 배제, amplitude-bearing single-mode, Eyring 보정 minus sign, phase/change history 본문 삽입 금지이다.
- 이번 작업은 Claude 폴더를 수정하지 않고, Codex 결과 폴더에 검수의견만 저장한다.

## Phase Range

| Phase | Name | Steps | Output |
|---|---|---:|---|
| 032 | Scope and source freeze | 1-8 | target table, hashes, line counts |
| 033 | 10-pass audit | 9-35 | coverage table, findings by pass |
| 034 | Verification and opinion | 36-50 | compile/static check, review opinion report |

## Non-goals

- Claude TeX 파일 수정 금지.
- Claude results/ledger 수정 금지.
- Codex Chapter 1 V4 재수정 금지.
- 실제 피팅 코드, solver, numerical implementation 작성 금지.

## Source Files

- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch1_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch2_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch3_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch4_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_ch5_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_full_rebuilt.tex`
- `D:\Projects\Project_Anode_Fit\Claude\docs\graphite_ica_refs_rebuilt.tex`

## Test Plan

1. line count/hash/mtime 고정.
2. section map 추출.
3. 10-pass coverage를 서로 다른 chunk scheme으로 수행하고 `missing=0` 확인.
4. label/ref/cite/bib consistency 검사.
5. risk pattern scan: `chi_j=beta_j`, `Heaviside`, `A_L=delta`, `$$`, `CHARTER`, metadata, placeholder refs, stale Ch6 labels.
6. XeLaTeX 3-pass compile fresh verification.
7. severity별 검수의견 작성.

## Assumptions

- `graphite_ica_full_rebuilt.tex`는 5개 chapter body를 포함하는 최종 통합본이므로 본문 논리 검수의 주 원천으로 둔다.
- 개별 chapter 파일은 preamble/title/meta 오염과 standalone consistency 확인용으로 함께 검사한다.
