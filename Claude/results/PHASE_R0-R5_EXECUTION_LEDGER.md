# Ch1 재수정-2 (R.0–R.5) Execution Ledger

**Plan**: `Claude/plans/2026-06-03-ch1-rerevision2-foundation-first-plan.md`
**대상**: `Claude/docs/graphite_ica_ch1.tex`

| Phase/Subphase | Planned Steps | Actual Steps | Block | Purpose | Status | Plan | Result | Machine Artifacts | Validation | Gate | Next Step |
|---|---:|---:|---|---|---|---|---|---|---|---|---:|
| R.0 | 1–5 | 1–5 | convention-lock | ξ_j↔θ_j 규약 잠금·부호사슬 검증(Codex 교차) | PASS | `plans/...foundation-first-plan.md` | `results/PHASE_R0_convention-lock_RESULT.md` | — | 손유도 flip 0 + Codex 합치; U_j 부호 Codex 반증 | PASS_CONVENTION_LOCK | 6 |
| R.1 | 6–14 | 6–14 | thermo | §notation θ_j·§stage·§eqpeak 유도 정직화(C1·C2) | PASS | 〃 | `results/PHASE_R1_thermo_RESULT.md` | `docs/graphite_ica_ch1.pdf`(17p) | G-build/local/flow/convention + Codex Q1-3 PASS | PASS_R1_THERMO | 15 |
| R.2 | 15–22 | 15–22 | kinetics | §lag·§barrier(relax 라벨·tail 도메인 C5·C6·C7·C10·C11) | PASS | 〃 | `results/PHASE_R2_kinetics_RESULT.md` | `pdf`(17p,821줄) | Codex Q1-3 PASS, Q4·Q5 적발→수정→CLOSED | PASS_R2_KINETICS | 23 |
| R.3 | 23–31 | 23–31 | synth | §dist·§synth·§overlap·§falsify(C3·C4·C8·superpose) | PASS | 〃 | `results/PHASE_R3_synth_RESULT.md` | `pdf`(18p,835줄) | Codex C3/C4/C8 + I-1·I-2·I-3 CLOSED; 분량무결성 검사 PASS | PASS_R3_SYNTH | 32 |
| R.4 | 32–35 | 32–35 | refs | caveat·인용 보강(C9)+전 문서 재빌드 | PASS | 〃 | `results/PHASE_R4_refs_RESULT.md` | `pdf`(18p) | undefined 0; bloom2005 DOI 웹검증·제목교정 | PASS_R4_REFS | 36 |
| R.5 | 36–40 | 36–40 | verify | Codex 재리뷰+적대 재검증+Decision Gate | PASS | 〃 | `results/PHASE_R5_verify_RESULT.md` | `pdf`(18p,854줄) | 4검수자 HIGH6+MED6 교정→Codex CLOSED; 부호사슬 NORMAL 3중 재확인 | PASS_R5_VERIFY | 41 |
| R.6 | 41–50 | 41–50 | section-converge | 절별 fresh 적대 검토(사용자 Decision Gate 지적: batch→절별 사전검출) | PASS | 〃 | `results/PHASE_R6_section-convergence_RESULT.md` | `pdf`(19p,867줄) | G1~G5 fresh Codex; 확정결함 3(LqV·arrhenius·falsify) 절별 적발·교정 | PASS_R6_SECTION_CONVERGENCE | 51 |
| R.7 | 51–62 | 51–62 | iterate-clean | 절별 iterate-until-clean(2차 지적: 문제 안 나올 때까지 반복)+절간 비약+횡단 정합 | PASS | 〃 | `results/PHASE_R7_iterate-until-clean_RESULT.md` | `pdf`(19p,876줄) | G1~5 각 Codex CLEAN 도달+횡단 GLOBALLY CONSISTENT; k_lim/k_{j,act} cascade 봉합; overreach 1 거부 | PASS_R7_ITERATE_CLEAN | 63 |
| R.8 | 63–68 | 63–68 | final-adv | Claude self 재정독 + fresh 독립 3인 적대 병행 | PASS | 〃 | `results/PHASE_R8_final-adversarial_RESULT.md` | `pdf`(19p,878줄) | 전원 CLEAN; weakest 2건 반영; Codex 인증만료로 대기 | PASS_R8_FINAL_ADVERSARIAL | 69 |
| R.9 | 69–74 | 69–74 | codex-crossmodel | Codex 교차모델 적대 + Codex↔Claude 반복 수렴 | PASS | 〃 | `results/PHASE_R9_codex-crossmodel_RESULT.md` | `pdf`(19p,879줄) | 재인증 후 Codex k_j충돌 적발→Claude valid 판정→교정→≈전파 3곳→Codex "DOCUMENT CLEAN"; Claude+Codex 동시 확정결함 0 | PASS_R9_CODEX_CROSSMODEL | 완료 |

**Notes**: R.0 에서 C1(근본)·C3 CONFIRM, C2·C5 라벨/범위 정밀화, eq:relax 라벨·eq:superpose r_a(G) 추가 확정. Codex 의 U_j=+μ⁰/(sF) 주장은 Claude 재유도로 반증(불채택). 최종 logistic·peak 공식 보존, 유도 정직화만 수행.
