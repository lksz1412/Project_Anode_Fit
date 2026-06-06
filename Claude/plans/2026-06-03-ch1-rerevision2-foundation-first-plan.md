# Chapter 1 재수정-2 (정밀판) — 규약 우선 + 절별 검수-후-진행 Plan

**Date**: 2026-06-03 · **Author**: Claude · **챕터**: R(Ch1 재수정) · **Phase**: R.0~R.5 · **Step**: 1~40
**상태**: 계획(정밀). 사용자 검토 후 R.0부터 실행. RR2 v1(`...signs-codex-plan.md`)을 supersede(그 문건은 보존, 본 계획이 대체).

---

## Summary

**목표**: `Claude/docs/graphite_ica_ch1.tex`(흑연 음극 dQ/dV 이론 Ch1)의 Codex 전영역 adversarial review(6 CRITICAL/21 HIGH/12 MEDIUM)에서 적출된 *근본 결함*을 교정한다. 핵심은 ξ_j 규약(Li 점유율 vs 방전 진행률) 모순(C1)으로, eq:mu→eqcond→logistic 부호 사슬과 동역학·종합까지 전파됐다.

**왜**: 학술 문서로서 한 번의 규약 실수가 문서 절반 이상을 다시 쓰게 만든 사고가 났다. 원인은 ① 규약을 *먼저 잠그고 검증*하지 않고 그 위에 쌓은 것, ② *절별 검수-후-진행*이 아니라 한 번에 쓰고 끝검증한 것, ③ 핵심 절에 *작업 중* 외부 적대 검토 게이트가 없던 것. 본 계획은 이 셋을 절차로 박는다.

**이번 범위**: Ch1 본문의 확정 결함 C1~C5 교정 + caveat C6~C11 보강 + 인용 보강. 충전 branch·Ch2~5·ρ_G 측정 프로토콜·ICA 데이터 워크플로 상세는 범위 밖(Non-goals).

**방법(3원칙)**: ① **foundation-first** — 규약·부호를 본문 손대기 전에 손유도+Codex로 잠근다(R.0). ② **verify-before-advance** — 모든 절은 5-게이트 통과 후에만 다음 절(한 번에 다 쓰고 끝검증 금지). ③ **작업 중 외부 적대 검토** — 규약·부호·동역학 절은 Codex 교차를 끝이 아니라 작업 중에.

---

## Current Ground Truth

**확인된 사실**:
- 대상: `Claude/docs/graphite_ica_ch1.tex` (~802줄, 17p, 컴파일 GREEN `!`0). 전체 1회 정독 완료(이전 세션). 단 정독 시 *결과 정합*만 확인하고 *유도 규약 모순*은 못 짚음 → 본 계획에서 R.0/R.1에 재정독·재검증.
- 참조(비복사): `Claude/docs/Archive_rebuilt/graphite_ica_ch1_rebuilt.tex`(구조·밀도 패턴만), `Claude/docs/graphite_ica_ch1_appendixB_fitting.tex`(피팅 부록).
- Codex review 산출: 7렌즈 6 CRITICAL/21 HIGH/12 MEDIUM. Claude triage 후 확정 C1~C5, caveat C6~C11, 과장 1건(L5-1, 빌드 GREEN이라 오류 아님).
- 프로젝트 구조: `Claude/{plans,results,docs}` + `Codex/` 거울([[feedback_multi_agent_project_structure]]). 커밋 시 Codex/ 동반(수정 X, 커밋 O).

**확정 결함(must-fix)**:
| ID | 결함 | 위치 | Codex |
|---|---|---|---|
| C1 | ξ_j↔θ_j 규약 모순(eq:mu가 ξ_j를 점유율로 다룸) → 부호 사슬 오염(뿌리) | eq:mu·eqcond·logistic·charge | L1-2·L3-1·L2-1·L7-2 (CRIT) |
| C2 | eq:dUdT 탈리튬화 엔트로피 부호 | eq:dUdT | L7-1·L1-3 (CRIT/HIGH) |
| C3 | eq:simplefit tail 진폭 r_a 누락 → 용량 비보존 | eq:simplefit | L1-6·L6-1 (CRIT) |
| C4 | S3/S4 식별 순서 순환(χ가 S4서 나오는데 S3 y(T)가 χ 필요) | 종합 절 | L6-3 (HIGH) |
| C5 | eq:tail \|V_n−V_a\| 양방향 → 단방향 방전 도메인 명시 | eq:tail | L7-3·L1-4 (HIGH) |

**caveat(보강)**: C6 k_0=k_BT/h 현상론적 prefactor 명시 / C7 eq:relax 단일모드·BEP ansatz 격상 / C8 반쪽전지 범위·dQ/dV_n vs dV_cell / C9 인용 보강(Newman&Thomas-Alyea, Bloom, 완화시간 분포) / C10 q_a 조작적 정의 / C11 lag r_j ↔ 속도 r_j± 기호 충돌(lag→ℓ_j).

**미확인(P0 통과 전 추정 금지)**: C1 교정의 정확한 부호 닫힘 형태(θ_j 켤레 유도). → R.0에서 손유도+Codex로 확정. *추정으로 본문 수정 금지*.

**과장(교정 불요)**: L5-1 "\textbf{$...$}→컴파일 오류": 빌드 GREEN이라 오류 아님. 렌더만 확인.

**git 상태**: 실행 시점 `git rev-parse`로 확인. 리포지토리면 작업/검토 commit 페어, 아니면 result+audit-result 문건 페어로 audit 워크플로 유지([[feedback_phase_audit_workflow]]).

---

## Phase Range

| Phase | 이름 | Steps | 교정 ID | 5-stage 루프 |
|---|---|---:|---|---|
| **R.0** | 규약 잠금·전제검증(foundation-first) | 1–5 | (규약) | plan→exec(손유도+Codex)→result→validation→ledger |
| **R.1** | 무대·열역학 재유도(절별) | 6–14 | C1·C2 | 〃 |
| **R.2** | 동역학 재유도(절별) | 15–22 | C5·C6·C7·C10·C11 | 〃 |
| **R.3** | 유효배리어·분포·종합·겹침·반증(절별) | 23–31 | C3·C4·C8 | 〃 |
| **R.4** | caveat·인용 보강 + 전 문서 재빌드 | 32–35 | C9 | 〃 |
| **R.5** | Codex 재리뷰(전영역)+적대 재검증+Decision Gate | 36–40 | (검증) | 〃 |

**5-게이트(절별, Implementation Interfaces §G에 정의)**: 모든 절은 G-local·G-flow·G-convention·G-build·G-review 통과 후에만 다음 절. *한 번에 다 쓰고 끝검증 금지.*

**정지 5조건([[feedback_plan_continuation_until_done]])**: GO 후 R.5까지 연속. 단 ① Decision Gate 도달 ② 새 의존성 출현 ③ gate FAIL ④ 사용자 stop ⑤ 두 통제문서 모순(→더 제한적 채택) 중 하나면 정지·평문 보고.

---

## Non-goals

- **발췌패치 금지**: 절별 편집 후 *전 문서 재빌드 + 앞 절 재대조*. excerpt만 보고 수정 금지([[feedback_full_file_read_required]]).
- **한 번에 다 쓰고 끝검증 금지**: 이번 사고의 직접 원인. 절별 verify-before-advance.
- **기존본 표현 옮겨심기(transplant) 금지**([[feedback_execute_explicit_choice_not_judgment]]).
- **사용자 코드 소유권·범위 보존**([[feedback_code_ownership_scope]]): 사용자가 잠근 기호·식별자(s, s_I, U_j, w_j, χ 등)·정수/문자 인코딩 보존. criteria 확대해석 과수정 금지. 지정 범위(C1~C11) 외 임의수정 X — 필요 시 묻고 GO 대기.
- **범위 밖**: 충전 branch, Ch2~5, ρ_G 측정 프로토콜·ICA 데이터 처리 워크플로 상세(피팅 부록 소관, 본문은 단서 1줄).
- **도구**: Workflow 등 권한팝업 도구 금지([[feedback_flow_interruption]]). 멀티에이전트는 Agent 도구. Codex/ tex 읽기/쓰기 금지(리뷰 의견만).

---

## Implementation Changes

| 종류 | 경로 | 의도 |
|---|---|---|
| 수정 | `Claude/docs/graphite_ica_ch1.tex` | C1~C11 교정(절별) |
| 신규 | `Claude/results/PHASE_R0_convention-lock_RESULT.md` … `PHASE_R5_...RESULT.md` | Phase별 result 11항목([[feedback_phase_execution_loop]]) |
| 신규 | `Claude/results/PHASE_R0-R5_EXECUTION_LEDGER.md` | 12-col ledger(장기작업, phase≥3·step≥20) |
| 신규 | `Claude/results/PHASE_R*_*_AUDIT.md` | 10차원×3-Pass audit 보고(작업/검토 페어) |
| 계획 | `Claude/plans/2026-06-03-ch1-rerevision2-foundation-first-plan.md` | 본 계획(11-section) |
| 동반 | `Codex/` 거울 | 커밋 시 동반(수정 X, 커밋 O) |

**문건 보호([[feedback_document_protection_addendum_pattern]])**: 이전 result·ledger·handover·RR2 v1 plan·Codex 산출물 *덮어쓰기 금지*. 정정은 Addendum/Supersession/Correction 별도 문건.

---

## Phase R.0 — 규약 잠금·전제검증 (foundation-first)

본문 한 줄도 손대기 전에 규약을 잠그고 *독립 검증*한다. **여기서 틀리면 전 문서가 다시 틀린다.**

- **Step 1** 전제 인벤토리 대조([[feedback_plan_premise_verification]]): 현재 tex의 ξ_j/θ_j·s/s_I·V_* 정의 실제 위치를 재정독해 Codex 지적과 1:1 대조. load-bearing 전제("ξ_j가 진행률") 확인.
- **Step 2** 규약 확정안 작성(Implementation Interfaces §C): θ_j=Li 점유율, ξ_j=1−θ_j=방전 진행률; lattice-gas μ_Li는 θ_j 켤레; 반쪽반응 탈리튬화 방향; 전위 4종(V_n/V_app/V_drive/V_n,OCV) + 반쪽전지 기준.
- **Step 3** *손유도*: 확정 규약으로 eq:mu→eqcond→logistic 부호 사슬을 숨은 flip 0으로 닫히게 손으로 유도(중간 단계 0 생략). eq:dUdT 부호도.
- **Step 4** **Codex 교차(G-review)**: 손유도 결과를 `codex:codex-rescue`(Agent 도구)로 독립 검증 — 부호 닫힘·규약 정합 확정.
- **Step 5** result(`PHASE_R0_..._RESULT.md`) + ledger.
- **입력**: ch1.tex(규약·열역학 절), Codex review 의견. **산출**: 확정 규약표 + 손유도 + Codex 확인.
- **gate(G-convention 확정)**: 손유도 부호 사슬 flip 0 + Codex 합치. **중단**: Codex와 손유도 불일치 시 정지·평문. **다음 조건**: 규약표 확정·result 저장.

## Phase R.1 — 무대·열역학 재유도 (절별)

R.0 규약으로 §notation→§stage→§eqpeak 재유도. C1·C2.

- **Step 6** §notation: θ_j/ξ_j 분리 도입 + 기호표 갱신(C1 기반).
- **Step 7** §stage 전하균형 eq:charge: θ_j/ξ_j 정합 재서술. → G-local·G-flow·G-convention·G-build.
- **Step 8** eq:mu(lattice-gas, θ_j 켤레) 재유도. **Step 9** eq:eqcond(탈리튬화 반쪽반응 평형) 부호 정직화. **Step 10** eq:logistic 도출(숨은 flip 0). **Step 11** eq:dxidV 부호 확인.
- **Step 12** eq:dUdT 부호 교정(C2): ΔG°_delith=+sF U_j → ∂U_j/∂T 정합.
- **Step 13** §eqpeak 정점식 — 앞 절(eq:logistic·dxidV) 정합 확인(G-flow).
- **Step 14** **G-review(Codex)** 규약·부호 절 + result + ledger + 10차원×3-Pass audit.
- **gate**: 절마다 5-게이트. eq:mu→...→dUdT 부호 사슬 일관·빌드 GREEN. **다음 조건**: result 저장·audit PASS.

## Phase R.2 — 동역학 재유도 (절별)

§lag→§barrier 일부(eyring·relax·Lq·tail). C5·C6·C7·C10·C11. 각 절 R.1 결과와 정합(G-flow).

- **Step 15** §lag 기호 충돌 해소(C11): lag r_j→ℓ_j. **Step 16** eq:relax 단일모드·BEP를 명시 ansatz로 격상(C7).
- **Step 17** eq:eyring + k_0=k_BT/h 현상론적 prefactor 명시(C6, L_q 비로 상쇄 강조).
- **Step 18** eq:Lq·eq:LqV 부호 확인. **Step 19** eq:tail 단방향 도메인 s(V_n−V_a)≥0 명시(C5).
- **Step 20** q_a 조작적 정의(C10). **Step 21** §lag/§barrier 앞 흐름 정합 재대조(G-flow).
- **Step 22** **G-review(Codex)** 동역학 절 + result + ledger + audit.
- **gate**: 절마다 5-게이트. **다음 조건**: result·audit PASS.

## Phase R.3 — 유효배리어·분포·종합·겹침·반증 (절별)

§barrier(나머지)→§dist→§synth→§overlap→§falsify. C3·C4·C8.

- **Step 23** eq:bv·eq:db·eq:keff 부호 R.0/R.2 정합 확인. **Step 24** §dist ρ_G(본문 단서, 상세 부록).
- **Step 25** §synth 3×3 종합 + S3/S4 식별 순서 순환 제거(C4): χ 먼저→Arrhenius.
- **Step 26** eq:simplefit tail 진폭 r_a 추가(C3): 용량보존 ∫dQ/dV=Q_j.
- **Step 27** eq:closed·eq:total 정합. **Step 28** §overlap 다전이 겹침 부등식 부호.
- **Step 29** C8 반쪽전지 범위·dQ/dV_n vs dV_cell 단서 1줄. **Step 30** §falsify 반증 절 앞 흐름 정합.
- **Step 31** **G-review(Codex)** 종합·분포 절 + result + ledger + audit.
- **gate**: 절마다 5-게이트. **다음 조건**: result·audit PASS.

## Phase R.4 — caveat·인용 보강 + 전 문서 재빌드

- **Step 32** C9 인용 보강(Newman & Thomas-Alyea, Bloom, 완화시간 분포) bibitem 추가·DOI 확인.
- **Step 33** 잔여 caveat 본문 반영 점검. **Step 34** 전 문서 재빌드 GREEN + dangling ref 0 + dup label 0.
- **Step 35** result + ledger.
- **gate**: G-build(최종 GREEN)·dangling 0. **다음 조건**: 빌드 GREEN·result 저장.

## Phase R.5 — Codex 재리뷰(전영역) + 적대 재검증 + Decision Gate

- **Step 36** **Codex 전영역 재리뷰**(`codex:codex-rescue`, Agent): C1~C11 교정 확정결함 0 확인.
- **Step 37** Claude 적대 재검증 — 멀티에이전트 청킹(~500줄/창) + 렌즈 G-physics·G-noleap·G-consistency·**G-follow·G-usable**·G-sign(Implementation Interfaces §L). refute mandate + 최약1곳 + 빈통과금지.
- **Step 38** Codex+Claude 합치 결함 triage. **Step 39** 잔여 결함 교정(있으면 해당 Phase 루프 재진입).
- **Step 40** 최종 result + ledger + 사용자 Decision Gate 보고(4-tier: 확정/근거미발견/추정/미검증).
- **gate**: G-codex(재리뷰 확정결함 0)·G-claude(적대 재검증)·G-build. **중단**: Decision Gate(사용자 판단 필요) 도달 시 정지·평문.

---

## Implementation Interfaces

**§C 규약표(R.0 확정 대상)**:
| 기호 | 정의 | 방전 시 |
|---|---|---|
| θ_j | 전이 j 부격자 Li 점유율 | 감소 |
| ξ_j=1−θ_j | 방전(탈리튬화) 진행률 | 증가(0→1) |
| μ_Li(θ_j) | =μ^0+RT ln[θ_j/(1−θ_j)]+Ω(1−2θ_j) (lattice-gas, **θ_j 켤레**) | — |
| 반쪽반응 | Li_(graphite) → Li⁺ + e⁻ + [ ] (탈리튬화=방전) | s=+1 |
| V_n/V_app/V_drive/V_n,OCV | 내부/측정(분극)/구동/평형해, 반쪽전지 기준 | — |
> eq:mu→eqcond→logistic 부호 닫힘은 R.0 손유도+Codex로 확정 후 본문 반영(추정 금지).

**§E 교정 식 인터페이스(확정 후)**: C2 ∂U_j/∂T=ΔS°_delith/(sF) (ΔG°_delith=+sFU_j) / C3 ∫(main+tail)dV=Q_j, tail 진폭 r_a,j 도입·main 진폭 보정 / C5 eq:tail 도메인 s(V_n−V_a)≥0 / C4 식별 순서 χ→ΔG_a.

**§G 5-게이트 정의(절별 필수)**:
| 게이트 | 검사 |
|---|---|
| G-local | 그 절 식·가정·유도가 (a)물리정확(차원·부호·극한·근사유효) (b)무비약(중간단계 0생략) (c)grounded(인용) |
| G-flow | *앞서 이어진 모든 절*의 결과·규약·기호와 정합·빈틈수용·비약 0 (앞 절 재정독 대조) |
| G-convention | 모든 기호·부호가 §C 규약과 일치 |
| G-build | 그 절까지 누적 컴파일 GREEN |
| G-review | 핵심 절(규약·부호·동역학)은 Codex/적대 독립 검토 통과 |

**§L 적대 검토 렌즈·청킹([[feedback_multiagent_review_chunking]])**: 분량 절은 ~500줄/창 분할 전담 위임. 렌즈 = 정확성(물리·수학·정합) + **1급 렌즈 G-follow(학부생이 앞 식+본문만으로 따라가나)·G-usable(절 끝 실데이터 대입 닫힌식 있나)** + G-sign. agent 프롬프트: refute mandate + 최약1곳 필수지목 + 빈통과금지.

**§R Result 11항목·Ledger 12-col**: result=Summary/Step Range/Inputs/Files Created/Files Updated/**Read Coverage**/Execution Evidence/Validation/Gate/Confirmed Non-Changes/Open Issues+Next([[feedback_phase_execution_loop]]). ledger 12-col = Phase/Planned/Actual/Block/Purpose/Status/Plan/Result/Artifacts/Validation/Gate/NextStep.

---

## Test Plan

- **LaTeX 빌드**: 절별 누적 + 최종 `latexmk`/`pdflatex` GREEN(`!`0·undefined 0·dup label 0·dangling ref 0).
- **부호 사슬 검수**: eq:mu→eqcond→logistic→dxidV→dUdT→bv→db→keff→LqV→tail 전 식 부호 손유도 대조(숨은 flip 0).
- **Codex 교차**: R.0·R.5에서 `codex:codex-rescue` 독립 판정과 합치 확인.
- **Read Coverage 대조**: 각 result에 실제 읽은 파일·행 범위 명시(정독 사후 증명).
- **논리 의존성·무비약**: 절별 G-flow — 각 절이 앞 절 결과만으로 도출되는지(외부 비약 0).
- **용량보존**: C3 ∫dQ/dV=Q_j 수치 확인.
- **4-tier 보고**: 확정/근거미발견/추정/미검증 분리([[feedback_confirmed_items_policy]]).

---

## Assumptions

- A1: C1 교정 방향(θ_j 켤레·탈리튬화 반쪽반응)이 옳다 — *임시 가정*, R.0 손유도+Codex로 확정 전 본문 미반영.
- A2: L5-1(\textbf{$}) 비오류 판정 유지(빌드 GREEN). R.4 렌더 확인서 재검.
- A3: ρ_G/ICA 워크플로 상세=부록 소관(D-범위 무응답 시 권고값).
- A4: Anode_Fit git 리포 여부는 실행 시 확인 — audit 페어 형태(commit vs 문건) 그에 맞춤.

---

## Decisions Required (평문, 무응답 시 권고값 실행)

- **D-범위**: ρ_G 측정·ICA 워크플로 = 본문 단서 1줄 + 상세는 피팅 부록. **권고: 그대로.**
- **D-규약표기**: θ_j(점유율)/ξ_j=1−θ_j(진행률) 분리, lattice-gas는 θ_j 켤레. **권고: 그대로.**
- **D-진행**: R.0 규약 잠금(+Codex) 통과 후 R.1~R.5 절별 5-게이트로 연속(정지 5조건 외 무중단). **권고: 그대로.**

---

## Correction History

| 일자 | 변경 |
|---|---|
| 2026-06-03 (RR2 v1) | 그림 제거·부호 전수 감사(eq:eqcond 의심 선적발)·Codex 리뷰 위임 계획. `...signs-codex-plan.md`. |
| 2026-06-03 (RR2 정밀판 a) | Codex 7렌즈(6 CRIT) 반영. 절별 검수·흐름정합·규약우선 실행규율 신설. **단 11-section 표준 양식 미준수**(§0~§7 임의 양식). |
| 2026-06-03 (RR2 정밀판 b, 본판) | **표준 11-section 양식으로 재작성** + 누락 지침 보완: Phase 5-stage 루프·Result 11항목·Ledger 12-col·10차원×3-Pass audit·청킹 ~500줄 G-follow·G-usable 렌즈·문건보호·정지 5조건·cumulative step(1~40)·전제검증·Read Coverage·Codex 동반·코드 소유권/범위 보존. 사용자 지적사항(절별=5게이트·흐름=G-flow·규약=R.0)은 양식 안에 보존. |
