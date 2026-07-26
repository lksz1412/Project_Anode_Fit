# Phase 035 — Claude Ch1 Review Intake and V5 Gate

## Summary

사용자가 제공한 Claude 측 독립 적대 10-pass 검수의견을 Codex 작업 기준으로 편입했다. 이 결과로 이전 `Chapter 1 V4 residual critical 0 / PASS` 판단은 downstream 기준에서 취소한다. Chapter 1의 다음 canonical target은 `graphite_ica_ch1_codex_candidate_v5.tex`이다.

## Inputs

| Type | Path | Coverage |
|---|---|---|
| Claude review | `D:\Projects\Project_Anode_Fit\Claude\results\RB_CODEX_V4_CH1_REVIEW_CLAUDE_10PASS.md` | 132 lines, full read |
| Codex V4 | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v4.tex` | targeted line-range verification against Claude findings |
| New plan | `D:\Projects\Project_Anode_Fit\Codex\plans\2026-06-02-ch1-v5-repair-and-ch2-5-resume-plan.md` | created |

## Execution Drift Correction

직전 Codex 작업은 Claude 최종 통합본 전체 검수의견을 작성했으나, 사용자의 더 이전 장기 지시였던 “Chapter 끝까지 순차 작업”을 실제 작성 단계로 이어가지 못했다. 따라서 이번 phase에서 해당 drift를 명시하고, Chapter 1 V5 repair 후 Chapter 2--5로 재진입하는 계획을 새로 세웠다.

## Accepted Claude Findings

Critical:

- AL-8/AL-9 결번은 실제 결함으로 확인했다.
- 기본 상수와 practical fitting symbols 누락은 실제 결함으로 확인했다.
- stretched-tail spectrum과 single-L Eyring/N2를 같은 적용 범위로 둔 것은 실제 물리 논리 충돌로 확인했다.

High:

- `chi_j` extraction에서 current prefactor 공선성은 실제 결함으로 확인했다.
- symmetric Marcus derivation에서 일반 `chi_j in [0,1]`를 끌어오는 서술은 실제 논리 혼합으로 확인했다.
- Volterra/Plan A closure 일부 유도는 더 열어 쓸 필요가 있다고 판단했다.
- `Q_bg`의 equilibrium capacitance와 rate-dependent lag 역할 혼합은 실제 double-counting 위험으로 확인했다.

## Rejected Or Bounded Findings

- Claude 검수의 “Codex lean scope vs Claude Ch6 appendix” 지적은 구조 선택 문제다. 단, 사용자가 Chapter 1 단독 simple fitting approximation을 원했으므로 V5는 solver code 없이 theory-level Plan B validation principle만 유지한다.
- `chi_j`와 `beta_j`가 같은지 여부는 V5에서도 분리한다. Ch1 `chi_j`는 Level-A scalar mobility sensitivity, Ch3 `beta_j`는 Level-B directional transfer coefficient다.

## Gate

V4 is superseded for downstream use. Chapter 2 work must not inherit V4 without checking V5 interface.
