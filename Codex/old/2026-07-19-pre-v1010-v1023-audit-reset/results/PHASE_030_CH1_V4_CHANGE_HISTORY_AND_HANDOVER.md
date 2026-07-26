# PHASE 030 - Chapter 1 V4 Change History and Handover

## 1. Canonical outputs

| 종류 | 경로 |
|---|---|
| Final Chapter 1 TeX candidate | `D:\Projects\Project_Anode_Fit\Codex\results\graphite_ica_ch1_codex_candidate_v4.tex` |
| 10-pass review | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_028_CH1_V4_10PASS_REVIEW.md` |
| Verification result | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_029_CH1_V4_VERIFICATION_RESULT.md` |
| Claude comparison | `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_031_CH1_V4_CLAUDE_COMPARISON.md` |
| PDF check output | `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_codex_ch1_v4\graphite_ica_ch1_codex_candidate_v4.pdf` |

## 2. Final TeX identity

- Lines: 945
- SHA256: `C1607A7E101B1D3BA4BD4CDF9D88D0C8AEDAFADCEA6BBFF1E525EC540C876517`
- Compile: XeLaTeX 3 passes, exit code 0/0/0
- Static checks: duplicate label 0, missing refs 0, missing cites 0, unused bibs 0

## 3. User requirements mapped

| 사용자 요구 | 반영 상태 |
|---|---|
| ICA peak tail, low T long tail / high T short tail | 서문, spectrum, falsification에 반영 |
| temperature barrier + electrode-potential-assisted effective barrier | `Delta G_eff=G-chi_j A_j` 및 Eyring/simple-fit에 반영 |
| step-function식 비약 금지 | Heaviside/step support 표현 제거, continuous barrier lowering으로 전개 |
| 용어는 영어 중심 병기 | `effective barrier`, `relaxation length`, `spectrum`, `falsification`, `identifiability` 등 유지 |
| 학부생 수준 무비약 전개 | variable definition, one-line derivation, boxed result, assumption ledger 유지 |
| Chapter 1만으로 simple fitting approximation 가능 | `sec:ch1_simplefit`에 `L`, `chi_j`, `Delta H_a` extraction order 제시 |
| 기존 문건은 참고하되 무비판 복붙 금지 | Claude 장점만 흡수, convention/logic 오류 수정 |
| 변경 이력은 본문에 넣지 않음 | 본 파일에 기록, TeX 본문에는 phase/change history 미삽입 |

## 4. Handover chain

1. Plan: `D:\Projects\Project_Anode_Fit\Codex\plans\2026-06-02-chapter1-v4-full-rebuild-10pass-plan.md`
2. Previous comparison base: `D:\Projects\Project_Anode_Fit\Codex\results\PHASE_026_CH1_CODEX_V3_REVIEW_AND_CLAUDE_COMPARISON.md`
3. Current review: `PHASE_028_CH1_V4_10PASS_REVIEW.md`
4. Current verification: `PHASE_029_CH1_V4_VERIFICATION_RESULT.md`
5. Current comparison: `PHASE_031_CH1_V4_CLAUDE_COMPARISON.md`

컨텍스트 압축 이후 이어갈 때는 이 handover chain을 먼저 열고, TeX 본문 자체보다 phase result와 ledger를 함께 확인해야 한다. 이전 세션 요약만 단독 근거로 삼지 않는다.

## 5. Next phase recommendation

사용자 검토 후 Chapter 1 V4가 승인되면 Chapter 2는 새 계획서로 시작한다. Chapter 2의 범위는 Chapter 1의 equilibrium/kinetic/tail convention을 바탕으로 reversible heat, entropy coefficient, `dV/dT`, and heat-related ICA extension을 전개하는 것이다. Chapter 2에서는 fitting code나 numerical solver 구축이 아니라 수식 논리 전개를 우선한다.
