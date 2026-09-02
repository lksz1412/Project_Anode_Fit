# plan_draft_v3 부록 A~C — handoff 노트 (11-section 마스터 플랜 밖)
> master 최종 저장(`Claude/plans/2026-09-02-v2-master-plan.md`, 2026-09-03) 시 FORMAT-12 에 따라 분리. 내용 = 통합·수정 에이전트 Decision Queue(A) · 미해결(B) · Read Coverage(C). 원문 = `wf/plan_draft_v3.md`:760–860 무수정 전사.

## 부록(11-section 밖 · handoff 전용 — master 가 `Claude/plans/` 최종 저장 시 work_log/handoff 노트로 분리한다; 마스터 플랜 본문에 12~14번째 절로 남기지 않는다)

### 부록 A. Decision Queue (통합·수정 에이전트 — 골격 이견·brief/v1 오류·판독 DQ 처리표)

> 결정은 master·사용자. 아래는 (A) 본 통합 에이전트(v2)와 수정 에이전트(v3)가 새로 올리는 항목과 (B) 판독 DQ 97건 + v1 DQ 17건의 처리 대응표다. 근거는 본문 §번호 또는 판독 문건 ID.

**(A) 통합 에이전트 신규 항목**

| ID | 종류 | 내용 | 근거 | 초안 처리 |
|---|---|---|---|---|
| DQ-I1 | brief/v1 정정 | v1.0.26 A/B 상태·v1.0.11 누락·v1.0.24 표현·SM2 집행 — §2.3·§2.5 에 정정 반영 | R2 §2.10·R1 DQ-3·R2 DQ-4·R3 B-7 | 반영 완료(Correction History) |
| DQ-I2 | 골격 규모(1h) | Step 수 40 → 50(챕터 1 +3·2 +5·3 +2). 골격(챕터·Phase·게이트 축)은 불변 | Correction History v2 (2) | 반영·master 확인 |
| DQ-I3 | 원천 간 상충 | 자산 태그 계열: v1 sub 실측 `[A-xxx]`159/`[E-xxx]`8 vs R3 grep 다계열 138건 — 두 실측의 패턴이 다르다고 추정. 2.1 Step 14 기계 추출로 확정 | §2.2 표 | 미해소 표시·2.1 이관 |
| DQ-I4 | 원천 간 상충 | display 집계: v1 230(+`\[` 38) vs R4a 169(범위, `\[` 포함) + R4b 84+7 — 합이 맞지 않음(범위·정의 차이 추정). T-4 정의 고정 후 재계수 | §2.2 표 | 2.1 이관 |
| DQ-I5 | 원천 간 상충 | P3 #8 base 위반 건수 3(R3) / 4(R4a) / +3(R4b sifr) — 토큰 정의 차이. DR-14 로 승격 | §2.4 | DR-14 |
| DQ-I6 | 검수 필요 | R4b G23 Λ_σ≈95–105 mV/GPa·R4a z_cut=4.357 정합·R4b binodal 수치예·R4b −46 J/(mol K)·f_Si 환산 — 판독 에이전트 산술이며 본 문서는 재계산하지 않음 | R4a §2.1 N5·R4b §3 #10·#19·#23·G23 | 2.2 검수 sub 재계산 대상 |
| DQ-I7 | attribution | 본 문서의 사용자 verbatim 인용은 전부 판독 문건이 "원천 큰따옴표" 로 옮긴 것을 재전사한 것 — 원천 실물 대조는 1.2 Step 6. 특히 v1.0.14 "별도 문건으로 그냥 놔두자"·6-11 Eyring 발화는 인계 문건 요지 표기(R1 DQ-10) | R1 DQ-10·R2 DQ-6·7 | DR-11·DR-16 에 등급 명기 |
| DQ-I8 | 범위 확인 | 판독 8본을 1.1 인벤토리에 "시드" 로 등재하되 immutable 원천으로 취급(정정은 등록부에서) — 판독 문건 자체를 고치지 않음 | Implementation Changes 불변 행 | 반영 |
| DQ-I9 | 경계 | R5 §5 (N) 32건과 R7 §4 X 48건이 상당수 겹친다(Langmuir·Lee–Yang·Bragg–Williams·Redlich–Kister·Frumkin·Onsager·Kramers·de Groot–Mazur 등) — 3.1 Step 35 통합 서지 표에서 중복 제거. R7 이 DOI 를 확인한 항목은 R5 "DOI 미검증" 표기를 덮는다 | R5 §5·R7 §4 | 3.1 Step 35 |
| DQ-I10 | 미열람(v2)→정독(v3) | `audit_checklist.md` 는 handoff **루트**에 있다(v2 는 `iter_1/` 로 오기 — 감사 FORMAT-11·LOGIC-16). v2 통합 시 열지 않았고 v3 fixer 가 전문 정독했다(1–48) — 검수 sub 지침이며 산출물이 아님 | Glob 실측 | 반영(경로 정정) |
| DQ-I11 | 추가 후보 | 판독 R6 §2 "Chapter 이름공간 넷" 에 후보 신구조까지 다섯을 Phase Range 표로 고정 — CLAUDE.md P3 #7 게이트(T-13 ⑦)를 "5축 표" 로 정의 | R6 DQ-11 | 반영 |
| DQ-I12 | 추가 후보 | 2.6 실행 경로에서 폐기 스크립트(`test_skew_regsol.py`·`out_skew/`)를 제외하고 `test_skew_regsol_v2.py`·`test_gallery_vs_regsol.py` 를 지정 — v1 §2.6 은 폐기분을 "준비 완료" 로 적었음(v1 DQ-7 정정) | R2 §2.10 | 반영 |
| DQ-I13 | v3 반영(fixer) | 감사 55건 전건 반영. 반영 방식 이견·부분 반영 4건 = SPEC-04(감사 "Claude 10·Codex 11" → 스냅샷 재계수 8·13) · LOGIC-02(산출물 ID `OUT-` 재명명 + 판독 ID 는 이름공간 표의 출처 규약으로 해소; 모든 인용에 접두를 기계적으로 붙이지는 않음 — 충돌 지점 R-1~R-4·P-n 만 `R2:` 접두) · LOGIC-10(v1 참조는 헤더에서 `iter_1/plan_draft.md` 로 정의하고 인라인 유지; brief 원천 코드는 §2.0 표로 재수록) · FORMAT-01(권고 (a) 채택 — Step 수 불변으로 각 Phase 마지막 Step 의 다음 조건에 Result 편입). 11-section 순서·이름 보존 및 Step 1–50 단조성 재검산 완료 | `fix_change_log.md` | master 확인 |
| DQ-I14 | 골격 확장(fixer) | 매 Phase Result(1.1~3.6 전건 + 4.x 이후) 추가 — brief §5 골격은 챕터 말 Result(1.5·2.7·3.7)만 명시했으나 brief §7 `PHASE_<id>_V2_<topic>_RESULT`·스킬 2b "매 Phase 종료 시 Result"·헌법 §0 "Result 생략 금지" 가 매 Phase 를 요구 → Step 수 불변으로 편입 | SKILL.md:150·165 · brief:188 | master 확인 |
| DQ-I15 | 범위 확장(fixer) | 1.4 Step 11 (i) 유실 자산 원문 정독 4건(Fable v2 tex·Opus v5/v6 §1.15·v3/v4/v5 §1.10·Opus v4 §1.18)은 brief §3-C 정독 범위 밖 — DR-15/16/17·DG-B 안건을 원문에 세우기 위한 확장; 부정 시 "원문 미정독" 표기로 진행 | R1 §2·§5 · 감사 SPEC-07 | master 판단 |
| DQ-I16 | 근거 미발견(fixer) | 판독 8본 병렬(2026-09-03)의 승인 출처(사용자 sign-off·Workflow 지목)가 본 문서 원천에 없다 — Implementation Interfaces 의 "유닛 계수 제외" 자기 선언은 삭제 | 감사 FORMAT-16 | master 기재 |
| DQ-I17 | 원천 오기(fixer 판정) | R6 R-2(:153)·DQ-3 "v1.0.15 [MODEL-1 선택]" — 정본은 6-30 radius 조사 [MODEL-1] → v1.0.11 Non-goals(R1 L-04·R3 B-1); 판독 문건은 immutable 이므로 등록부(OUT-REG3)에서 정정 | R1:136 · R3:185 · R6:153 | 1.4 Step 10 |
| DQ-I18 | 정직성(fixer) | 감사 3본 `wf/audit_spec.md`·`audit_format.md`·`audit_logic.md` 는 본 fixer 가 직접 열지 않고 master 전달본(55건 전문)으로 반영했다 | 부록 C | — |
| DQ-I19 | 검수 등급(fixer) | 등록부 3종·GAP REGISTER 를 통상으로 둔 것은 fixer 판단 — 사용자가 "전부 고가치" 를 택하면 1.5·2.7 도 10R + 6렌즈로 상향(DR-23 선택지 2) | 헌법 §3 | DR-23 |

**(B) 판독·v1 DQ 처리 대응표(97건)**

| 출처 | 건수 | DR 승격 | Phase Step 흡수 | Decision Queue 잔류(master 판단) |
|---|---|---|---|---|
| v1 work_log DQ-1~17 | 17 | DQ-6→DR-6 · DQ-7→2.6 Step 31·DR-6 · DQ-8→Assumptions 7 | DQ-1·2·3·5·9·10·12·14·15·16·17 → 1.1/2.1/2.2/Non-goals/T-4/Phase Range 반영 | DQ-4(파일명 제안)·DQ-11(plans/INDEX 스테일 정정 별도)·DQ-13(A12:80 잔재) |
| R1 DQ-1~10 | 10 | DQ-7(S0–S5 본문 편입)→3.3/3.4 결정 후보·DR-16 인접 | DQ-1·2·3·4·5·6·8·9·10 → 1.2 Step 3·5·6·7·1.4 Step 10·11 | — |
| R2 DQ-1~12 | 12 | DQ-8→DR-10 | DQ-1→2.1 · DQ-2·3·4·11→1.1/1.2/§2.3 · DQ-5→2.6 Step 30 · DQ-6·7→1.2 Step 6 · DQ-9→1.2 · DQ-10→DR-4 · DQ-12→2.1 | — |
| R3 DQ-1~16 | 16 | DQ-1→DR-14 · DQ-2·4→DR-13 · DQ-3→DR-12 · DQ-7→DR-10 · DQ-13→DR-22/Assumptions 20 · DQ-14→DR-16 | DQ-5→2.4 Step 25 · DQ-6→1.1/2.1 · DQ-8·9→1.2 Step 4 · DQ-10·11→§2.5/2.1 · DQ-12→1.3 Step 9/4.4 · DQ-15·16→3.1 Step 33 | — |
| R4a DQ-1~10 | 10 | DQ-1→DR-22 · DQ-3→DR-21 · DQ-6→DR-8 | DQ-2→2.2 Step 20/3.4 Step 45 · DQ-4→2.4 Step 24 · DQ-5→3.4 Step 46 · DQ-7·8→§2.2/2.1 · DQ-9→2.2 Step 19 · DQ-10→4.x | — |
| R4b DQ-1~10 | 10 | DQ-1→DR-14 · DQ-2→DR-11 · DQ-6→DR-20 · DQ-7→DR-21 | DQ-3→2.1 Step 15/3.4 Step 45 · DQ-4·9→2.6 Step 30 · DQ-5→2.4 Step 24 · DQ-8→2.2 Step 16 · DQ-10→2.5 Step 29/4.0 | — |
| R5 DQ-1~12 | 12 | DQ-2→DR-10 · DQ-6→DR-18 · DQ-8→3.1 재판정(DR-17 인접) | DQ-1→1.4 Step 11 · DQ-3·9→3.1 Step 36/4.2 · DQ-4·10→3.4 Step 45/4.0 · DQ-5→4.4 · DQ-7→3.1 Step 35 · DQ-11→3.1 Step 34 · DQ-12→2.4 Step 24 | — |
| R6 DQ-1~12 | 12 | DQ-1→DR-11 · DQ-2→DR-18 · DQ-3→DR-15 · DQ-6→DR-8 · DQ-8→DG-B 패키지 | DQ-4·12→2.6 Step 31 · DQ-5→3.1 Step 35 · DQ-7→3.2 Step 39 · DQ-9→1.4 Step 11 · DQ-10→3.2 Step 39 · DQ-11→Phase Range | — |
| R7 DQ-1~15 | 15 | DQ-2·4·9→DR-19 · DQ-8→DR-8 · DQ-6→DR-12 | DQ-1·3·10·11·12→2.4 Step 24·25/5.1 · DQ-5→1.4 Step 11 · DQ-7·14→3.1 Step 35 · DQ-13→3.5 Step 48 · DQ-15→T-4 | — |

---

### 부록 B. 미해결 (v3 시점)

- DQ-I3·I4·I5 원천 간 상충(자산 태그 계열·display 집계·코드 토큰 건수) — 2.1/2.5 실물 재계수 전까지 미확정.
- 판독 path:line 근거의 실물 대조 — v2 통합 에이전트도 v3 fixer 도 원천 tex·md 를 열지 않았다(Assumptions 19).
- DR-1~DR-23 — 사용자 결정 대기. DG-A/B/C — 3.7 에서 정지.
- SymPy 설치·xelatex PATH·Crossref 지속 접근·신규 예정 파일 부재(Assumptions 22) — GO 전 1g 대조.
- 감사 3본(`wf/audit_*.md`) 원문 미열람(전달본 반영) · 판독 8본 병렬의 승인 출처(DQ-I16) · HANDOVER 건수 정본(1.1).
- master 삼각검증·통합 → `Claude/plans/2026-09-02-v2-master-plan.md` 저장(master 소관 — 부록 A~C 는 저장 시 분리).

---

### 부록 C. Read Coverage (통합 에이전트 v2 · 수정 에이전트 v3 — 파일·행 범위 전건)

**v3 fixer(2026-09-03) — 전문 정독(head→tail, Read 도구; 분할 read 는 합쳐 전 영역):**

| # | 파일 | 행 범위 | 방식 |
|---|---|---|---|
| F0 | `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md` | 1–219(전문) | Read |
| F1 | `…/wf/plan_draft_v2.md` | 1–118 · 119–298 · 299–388 · 389–478 · 479–638 · 639–784(전문, 6분할 합쳐 전 영역) | Read |
| F2 | `…/audit_checklist.md`(루트) | 1–48(전문) | Read |
| F3 | `…/wf/R1_version_register_v3_to_v1019.md` | 1–91 · 92–206(전문) | Read |
| F4 | `…/wf/R2_version_register_v1020_to_v1026.md` | 1–130 · 131–300(전문) | Read |
| F5 | `…/wf/R3_binding_decisions_and_lost_directions.md` | 1–223 · 224–398(전문) | Read |
| F6 | `…/wf/R4a_diagnosis_scope_ch1_partT.md` | 1–363(전문) | Read |
| F7 | `…/wf/R4b_diagnosis_scope_ch2_ch3_appendix.md` | 1–287 · 288–431(전문) | Read |
| F8 | `…/wf/R5_theory_candidates_thermo_statmech.md` | 1–156 · 157–291 · 292–426(전문) | Read |
| F9 | `…/wf/R6_theory_candidates_kinetics_hys_heat.md` | 1–163 · 164–289 · 290–415(전문) | Read |
| F10 | `…/wf/R7_reference_master_map.md` | 1–254 · 255–394 · 395–534(전문) | Read |
| F11 | `C:\Users\lksz1\.claude\skills\skill_LKS_original_plan-execution\SKILL.md` | 1–239(전문 — FORMAT-01·13·20 근거 :150·:165·:100·:210 확인) | Read |
| F12 | 세션 시작 git status 스냅샷(시스템 제공) | untracked 21 = Claude 8 + Codex 13 재계수 | 읽기 |
| F13 | `…/` 폴더 목록(Glob) | `audit_checklist.md` 루트 위치·`wf/audit_*.md` 3본 존재 확인 | Glob |

v3 가 열지 않은 것: `wf/audit_spec.md`·`audit_format.md`·`audit_logic.md`(감사 원문 — master 전달본으로 반영) · `iter_1/plan_draft.md`·`iter_1/work_log.md`(v2 가 정독; v3 는 v2 본문의 인용으로만) · `R7_reference_master_map.json` · 원천 실물 전부(tex·md·PDF·코드) · `Codex/`(금지). v3 산출 = `wf/plan_draft_v3.md`·`wf/fix_change_log.md` 2건 + 휘발 스크래치 스크립트 3본; 기존 파일 수정·삭제 0(v2 는 그대로) · git 명령 미실행 · Codex 무접근.

**v2 integrator(2026-09-03) — 전문 정독:**

| # | 파일 | 행 범위 | 방식 |
|---|---|---|---|
| 0 | `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md` | 1–219(전문) | Read |
| S1 | `C:\Users\lksz1\.claude\skills\skill_LKS_original_plan-execution\SKILL.md` | 1–239(전문) | Read |
| S2 | `…\skill_LKS_original_plan-execution\references\record-formats.md` | 1–42(전문) | Read |
| V1 | `…/iter_1/plan_draft.md` | 1–266 · 267–421 · 422–576(전문, 3분할 합쳐 전 영역) | Read |
| V2 | `…/iter_1/work_log.md` | 1–120(전문) | Read |
| R1 | `…/wf/R1_version_register_v3_to_v1019.md` | 1–91 · 92–206(전문) | Read |
| R2 | `…/wf/R2_version_register_v1020_to_v1026.md` | 1–130 · 131–215 · 216–300(전문) | Read |
| R3 | `…/wf/R3_binding_decisions_and_lost_directions.md` | 1–223 · 224–398(전문) | Read |
| R4a | `…/wf/R4a_diagnosis_scope_ch1_partT.md` | 1–363(전문) | Read |
| R4b | `…/wf/R4b_diagnosis_scope_ch2_ch3_appendix.md` | 1–287 · 288–431(전문) | Read |
| R5 | `…/wf/R5_theory_candidates_thermo_statmech.md` | 1–156 · 157–291 · 292–426(전문) | Read |
| R6 | `…/wf/R6_theory_candidates_kinetics_hys_heat.md` | 1–163 · 164–289 · 290–415(전문) | Read |
| R7 | `…/wf/R7_reference_master_map.md` | 1–254 · 255–394 · 395–534(전문) | Read |

**v2 가 안 읽은 것(미검독 — 추정 금지)**: 원천 실물 전부(CLAUDE.md 는 시스템 주입본으로만·tex·md·PDF·코드) · `R7_reference_master_map.json` · `audit_checklist.md`(루트 — v3 에서 정독) · `Codex/`(금지). v2 산출 파일 = `wf/plan_draft_v2.md` 1건 + 휘발 스크래치 청크 7본(세션 스크래치패드). 기존 파일 생성·수정·삭제 0 · git 명령 미실행 · Codex 무접근.

