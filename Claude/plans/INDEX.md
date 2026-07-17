# plans/ INDEX (MOC) — 계획서 항해 진입점

> 컴팩션 복구·항해용. **현재 활성 마스터부터 읽는다.** 과거 계획은 시대별 그룹으로 묶음(날짜순 파일명 = 1차 정렬). result/ledger 는 `../results/process/`.

## ★ 현재 활성 — v1.0.22 (활물질별 챕터 재편 — GO 대기)
| 파일 | 역할 | 상태 |
|---|---|---|
| **`2026-07-17-v1022-master-plan.md`** | ★MASTER v3 — 3챕터 재편(흑연+열 / LCO+열[추가 텀] / Si·혼합 0~30%)+인용 다리 12곳+통계역학 증축+블렌드 토글+장별 기호표/레퍼런스. **운용 구성 명문화 = 3+1/3+1/1/1**(저작 O3+F1 / 검수 O3+F1 / 서지 저비용1+승급 / 코드 마스터1). **R0·R1·RA·R1b 완료**(재편 77/23/5/8p·자산 357/357 + 계보 감사 ③미로그=0건 + 구획 스윕 118건 분류·오문 7 정정 S-008), R2(흑연 장 이음매·인용 다리·증축)부터 잔여. 병합 빌드 금지(사용자 별도 세션) | GO·진행 중 |
| `../docs/v1.0.22/plans/PLAN_RA_lineage_audit.md` | RA 계보 무결 감사(v19→v22 — 자산 정체성·라벨·해시 계보·총량·표적 병독) + R1b 구획 점검 계획서 — **집행 완료·전 gate PASS** | done |

## 직전 — v1.0.21 (확장판, Q0~Q8 완료 — Q9/Q10 은 v1.0.22 R0 에 흡수)
| 파일 | 역할 | 상태 |
|---|---|---|
| `2026-07-16-v1021-master-plan.md` | MASTER v2 — 통계역학 2건·항법 이원판(→v22 폐기 예정)·top3·LCO 시연·Si 예비 부록·그림 A급 5본 | Q0~Q8 done |

## 완주 — v1.0.20 (품질 정정판, 동결 2026-07-17; 계획·이력 위치가 본 폴더가 아님 — 사용자 2026-07-16 위치 규약)
| 파일 | 역할 | 상태 |
|---|---|---|
| `../docs/v1.0.20/plans/2026-07-16-v1020-master-plan.md` | MASTER — 서지 무결·중간다리·컨벤션 통일 증판(P0~P8 전 PASS). phase별 세부 계획 = 같은 폴더 `PLAN_P*.md`. 인계 = `../docs/v1.0.20/HANDOVER_v1.0.20.md` | done |

> 참고: v1.0.16~v1.0.19 마스터플랜(본 폴더 2026-07-06~07-08 파일들)은 완주 — 직전 완결 = `2026-07-08-v1019-ch1-fable-rewrite-plan.md`(v1.0.19, done).

## 과거 활성 (v1.0.15 교재 증판본 — 이산 격자 퇴출 점별 아키텍처 + Ch2 발열 상세화)
| 파일 | 역할 | 상태 |
|---|---|---|
| **2026-07-05-v1015-code-doc-sync-master-plan.md** | ★**MASTER** — 순차 7-페이즈(P1 앵커·증판 → P2 Ch1 이론교정[격자 퇴출·eq:memory 승격·R5 재유도] → P3 Ch2 발열 상세화 → P4 코드 점별 재아키텍처+dead 삭제+골든 검증 → P5 그림 경연[상한X] → P6 N회 검수 → P7 마감). theory-first·문건↔코드 양방향 동기·dead 삭제. | 사용자 검토·GO 대기 |
| 2026-07-04-v1015-code-update-plan.md | (superseded ← 위 마스터) Fable rev.3 "코드 재아키텍처+문건 사후 동기" 프레이밍. 이력 보존(삭제 X) | superseded |

## 과거 활성 (v1.0.10~v1.0.14 완주 — 코드↔문건 동기화 6-페이즈 = v1.0.15 검증 모델)
| 파일 | 역할 | 상태 |
|---|---|---|
| **2026-07-01-v1010-code-doc-sync-bdd-fitting-plan.md** | ★**MASTER**(검증 모델) — 순차 6-페이즈(1 코드 → 2+3 Ch1 → 4 Ch2 → 5 코드개정 → 6 최종점검). LCO·발열 코드구현=P4. v1.0.10~1.0.14 이 궤도로 완주. | done |
| 2026-07-01-graph-verify-code-doc-unify-v1010-plan.md | (완료) 코드 정상 종개형 검증 + 1.0.10 버전 통일 | done |
| 2026-06-30-rework-broadening-restore-weff-fix-reorg-plan.md | (완료) broadening 복원·w_eff 제거·구조 재정리 | done |
- 실행 ledger·result: `../results/process/V1010_EXECUTION_LEDGER.md`, `V1010_P{n}_*_RESULT.md`, `GRAPH_VERIFY_RESULT.md`, `PHASE_REWORK_RESULT.md`.

## 마스터/로드맵 (역대)
- `MASTER_ROADMAP_v3.md` · `MASTER_ROADMAP_CH2_v1.md` · `2026-06-22-ch1-v5-comprehensive-rereview-MASTER.md` · `2026-06-22-ch1-v6-flowchart-reassembly-MASTER.md`

## 역사 계획 (시대별 그룹 — 날짜순)
- **05-29~05-30 통합·재유도 기획**: consolidation-roadmap·intent-gap-diagnosis·undergrad-rederivation-rebuild.
- **06-01~06-03 Ch1 자기완결·논리사슬 재구축**: self-contained·blank-page-clean-spine·FINAL-logical-chain·intersection-bridge·peak-physics-derivation·rerevision(2·signs).
- **06-06~06-08 Ch1 교과서형·레지스터 + Ch2 신설(반속/발열/히스 기획)**: register-revision·sec6/sec8-10·textbook-form / ch2-5-rebuild·ch2-deep·ch2-textbook-overhaul·NEW-ch2-kinetics·NEW-ch2-hysteresis·connective-masterequation. (⚠️이때 Ch3=발열 4장 기획 = 이후 supersede)
- **06-09~06-13 통합·깊이확장·Ch1 v2~v4 패스**: integration-completeness·ch3-heat-build·merge-single-chapter·textbook-depth / ch1 v2(blank/rewrite/proofread/tone/figures)·v3(equation-selfcontained/w4/x-pass)·v4(stacking-redo).
- **06-17~06-22 Ch1 v5/v6 + v5RR 라운드**: v5-equation-driven·v5RR(R0~R3)·v6-flowchart.
- **06-29~06-30 Ch1 v7/v8 9x9x1x1 + v9 LCO·Ch2 v4 2track + 조사**: v7-codeflow·v8-derivation-expanded·ch1v9-LCO-ch2v4-mixing-2track·ch2-reversible-heat-survey·radius-distribution-survey.
- **06-30~07-01 rework·v1.0.10**: (위 ★현재 활성 참조).

## 규약 (지침 — [[feedback_plan_template_11sections]]·[[feedback_phase_execution_loop]])
- 마스터 계획 + 페이즈별 세부 계획 = **plans/ 에만** 차곡차곡. 페이즈마다 **result** 를 results/process 에 저장(다음 페이즈 전제·컴팩션 복구점), **ledger** 갱신. 문서 추가 시 같은 턴에 본 INDEX 갱신.
