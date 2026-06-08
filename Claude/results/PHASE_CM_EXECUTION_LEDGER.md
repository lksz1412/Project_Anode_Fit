# PHASE_CM Execution Ledger — Ch1·Ch2 연결고리 + 최종 피팅식 개정

Plan: `Claude/plans/2026-06-08-ch1-ch2-connective-masterequation-revision-plan.md`
Branch: `rb-rebuild-2026-05-30`. Start commit: 9f06579.

| Phase | Planned Steps | Actual Steps | Block | Purpose | Status | Result | Validation | Gate | Next Step |
|---|---:|---:|---|---|---|---|---|---|---:|
| 1.1 | 1-2 | 1-2 | ch1-intro | 서론 최종식 도착점 thread | PASS | PHASE_CM_ch1_RESULT.md | 서론 thread 반영·빌드 | G1.1 | 3 |
| 1.2 | 3-5 | 3-5 | ch1-eqpeak | forward-thread·loop-closure·8.314× | PASS | PHASE_CM_ch1_RESULT.md | 8.314× 표기·thread | G1.2 | 6 |
| 1.3 | 6-8 | 6-8 | ch1-lag | stretched 관측 동기(S2) | PASS | PHASE_CM_ch1_RESULT.md | stretched·§dist 예고 | G1.3 | 9 |
| 1.4 | 9-12 | 9-12 | ch1-barrier | §6 다리·disclaimer·keff 조건 | PASS | PHASE_CM_ch1_RESULT.md | keff 3RT·다리·prune | G1.4 | 13 |
| 1.5 | 13-16 | 13-16 | ch1-stattools | 도구막간·C2-1 길이식(S1·S4) | PASS | PHASE_CM_ch1_RESULT.md | 길이식 e^{(G−χ𝒜)/RT}·집단공통 | G1.5 | 17 |
| 1.6 | 17-18 | 17-18 | ch1-dist | stretched payoff(S2) | PASS | PHASE_CM_ch1_RESULT.md | §lag payoff 명시 | G1.6 | 19 |
| 1.7 | 19-23 | 19-23 | ch1-synth | 분포↔단일지수·메타·부록 | PASS | PHASE_CM_ch1_RESULT.md | 선택 명시·메타/부록 제거 | G1.7 | 24 |
| 1.8 | 24-28 | 24-28 | ch1-master | 신규 최종 종합식 절 sec:master | PASS | PHASE_CM_ch1_RESULT.md | eq:master 손검·4요소 | G1.8 | 29 |
| 1.9 | 29-31 | 29-31 | ch1-verify | 빌드·커밋(Codex 말미 일괄) | COND | PHASE_CM_ch1_RESULT.md | 빌드 0 undefined 21p; Codex 보류 | G1.9-build | 32 |
| 2.1 | 32-34 | 32-34 | ch2-notation | γ_j 정의역·서론 thread | PASS | PHASE_CM_ch2_RESULT.md | γ_j [0,1]·thread | G2.1 | 35 |
| 2.2 | 35-36 | 35-36 | ch2-staging | 일차성 보강 | PASS | PHASE_CM_ch2_RESULT.md | 일차성 기원 문장 | G2.2 | 37 |
| 2.3 | 37-39 | 37-39 | ch2-origins | 두 기원 중복 축약 | PASS | PHASE_CM_ch2_RESULT.md | §3 포인터화 | G2.3 | 40 |
| 2.4 | 40-41 | 40-41 | ch2-branch | ΔU_hys 로그 이중화 | PASS | PHASE_CM_ch2_RESULT.md | −4 artanh·2u 명시 | G2.4 | 42 |
| 2.5 | 42-44 | 42-44 | ch2-dQdV | w_j^b 근거·bare V→V_n | PASS | PHASE_CM_ch2_RESULT.md | V_n 통일·근거 | G2.5 | 45 |
| 2.6 | 45-46 | 45-46 | ch2-bib | reynier2004 orphan | PASS | PHASE_CM_ch2_RESULT.md | \cite 추가 | G2.6 | 47 |
| 2.7 | 47-51 | 47-51 | ch2-master | 신규 충방전 종합식 sec:hys_master | PASS | PHASE_CM_ch2_RESULT.md | eq:hys_master(_center) 손검 | G2.7 | 52 |
| 2.8 | 52-54 | 52-54 | ch2-verify | 빌드·Ch1정합·Codex·커밋 | PASS | PHASE_CM_ch2_RESULT.md | 빌드 0 undefined 9p; Codex B1·B2·S2·S4 시정 후 MAJOR 0 | G2.8 | done |

**Codex 교차검수(agent ade8faf5)**: Ch1 eq:master 정상(꼬리 게이트 underbrace 명시), §stattools C2-1 수정 정상(상수 오프셋 분산무관·eq:superpose 정합), 연결편집 모순 0. Ch2 B1(u_j 정의역)·B2(상분리 기준)·S2(분기폭)·S4(고용체 열역학 한정) 시정 완료. Ch1↔Ch2 인용(1.3/1.4/1.19) 원문 대조 일치.

## PHASE_CM2 (Ch2 내용 심화 + 표기) — plan `2026-06-08-ch2-content-deepening-plan.md`
| Phase | Planned | Actual | Block | Purpose | Status | Result | Gate | Next |
|---|---:|---:|---|---|---|---|---|---:|
| 3.1 | 55-58 | 55-58 | fmt | 절번호 2.x/1.x·식 2.12/2.13 다단·overfull0 | PASS | PHASE_CM2_ch2-deepening_RESULT.md | G3.1 | 59 |
| 3.2 | 59-63 | 59-63 | ch2-§2.2 | 정규용액 미시기원·g''·T_c·공통접선·vdW | PASS | 〃 | G3.2 | 64 |
| 3.3 | 64-68 | 64-68 | ch2-§2.3 | 세영역·핵생성 CNT·과주행·Dreyer | PASS | 〃 | G3.3 | 69 |
| 3.4 | 69-72 | 69-72 | ch2-§4 | vdW loop·Maxwell·g'' 참조 | PASS | 〃 | G3.4 | 73 |
| 3.5 | 73-76 | 73-76 | ch2-§5 | loop 일주·분기선택·U_j 중심 | PASS | 〃 | G3.5 | 77 |
| 3.6 | 77-81 | 77-81 | ch2-§7 | 과전압 3원·kinetic lag 정량·수치 | PASS | 〃 | G3.6 | 82 |
| 3.7 | 82-84 | 82-84 | ch2-§8 | Preisach·FORC·포락선 | PASS | 〃 | G3.7 | 85 |
| 3.8 | 85-87 | 85-87 | ch2-§6 | 수치 예제 박스 | PASS | 〃 | G3.8 | 88 |
| 3.9 | 88-90 | 88-90 | verify | 빌드 overfull0/undef0·Codex·커밋 | COND | 〃 | G3.9-build | done |
