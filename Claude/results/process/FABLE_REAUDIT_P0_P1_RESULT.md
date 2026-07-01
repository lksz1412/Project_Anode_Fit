# FABLE 재검 — P0(준비)·P1(이력 전수감사) RESULT

> 마스터 = `../../plans/2026-07-02-fable-reaudit-v12-master-plan.md` · 세부 = `2026-07-02-fable-reaudit-P0-P1-history-audit-plan.md`. 브랜치 main(phase마다 커밋+푸쉬).

## Phase 0.1 (Steps 1-2) ✅
- 밀린 푸쉬 검증: 커밋별 푸쉬는 실재했으나 전부 `rb-rebuild-2026-05-30` 브랜치행 — GitHub main은 14322e6에 정지 상태였음.
- **main 브랜치화**: origin/main이 HEAD 조상임을 확인 → `git checkout main && git merge --ff-only` → push. **원격 main = b26b6b1(ls-remote 검증), 신규 389 커밋 GitHub main 반영.** 이후 작업 = main.
- 스킬 개정(지시 ④): `Project_skills/competition-cherrypick-authoring/SKILL.md` — Fable 가용 시 N=10(3S+3O+3C+1F)·Fable 가중 3·체리픽 통합/최종본=Fable·검수 union+10차 변형. 전면 재개정 불요 판단(형식 적합). 커밋 817a21b(Project_skills).

## Phase 0.2 (Steps 3-4) ✅
- Step 3: `docs/Fable_점검/` 생성.
- Step 4: 인벤토리 확정 — **버전 tex 16 실물 전부 실재(누락 0)**:
  - Ch1: Fable_v3(200.4KB)·Opus_v4(213.3)·Opus_v5(150.0)·Opus_v6(152.5)·v7-11(63.9)·v8-11(87.1)·v9(132.5)·v10(158.6)·v1.0.10(167.7)·v1.0.11(167.7)
  - Ch2: v3(20.2)·v4(60.3)·v5(61.1)·v1.0.10(61.4)
  - 코드: v11_final(38.8)·v1.0.10(47.6)
  - 기록: plans 72·spine 11(BRIEF/DEFECTS/FIX_LIST/CHERRYPICK)·핸드오버 8.
- gate PASS(누락 버전 0).

## Phase 1.1-1.3 (Steps 5-12) — 진행

### Step 7 — master(Fable) 직접 정독 소견 (기록류 gap)
**정독 완료 목록(본 세션 누적)**: v8 AUTHOR_BRIEF/KNOWN_DEFECTS·v9 BRIEF/FIX_LIST·ch1v10 BRIEF/FIX_LIST/R1/R2/PHASE_RESULT·ch2v4 BRIEF·6-30 radius 핸드오버·RB_CHARTER·HANDOVER_RB_2026-05-31(grep)·**HANDOVER_RB_2026-06-02b**·**PHASE8_v7_FINAL_RESULT**·**HANDOVER_2026-06-10(TBR)**·**HANDOVER_2026-06-11(v2 백지)**·_FINAL_README.

**타임라인 재구성(확정)**:
1. **RB 트랙**(5-30~6-02): Ch1~6 학부-재유도 재구축 → Ch6 해체·Ch1 부록B 흡수 → **Ch1~5 통합본 107p**(cb17b70). "절별 fine 검수 = 절마다 1 agent"가 거친 3렌즈 누락 ~110결함 적발(방법론 원점).
2. **6-07~6-09**: ch2-5 야간 초안·장 재편(new Ch2=반속·Ch3=발열)·병합.
3. **★Fable 트랙**(6-10~6-11): TBR 50p(`graphite_ica_ch1_Fable.tex`) → 사용자 6대 피드백(★"모든 것이 **Eyring 식(1.21)에서 뻗어야** 하는데 들러리"·binodal/spinodal 뜬금·연습문제 불필요·억지분량 금지) → **백지 재작성 v2 = Eyring 근본식 척추**(39p, (1−r_a) 보존인자·round-trip PASS·24회 검수) → **Fable_v3(200KB, 마지막 Fable)**.
4. **Opus 인수**(~6-22): Opus_v4(213KB)·v5(150KB)·v5 재검 MASTER·**v6 = flowchart 재조립**(6-22).
5. **v7 재출발**(6-29): `Anode_Fit_v11_final.py` 코드 플로우차트(N0→N9)를 척추로 **의도적 17p 축소**("곡선에 필요한 식만" — 사용자 정합 기록). 9종 경쟁-체리픽 방법 최초 실증(스킬 기원). ★v7-11에 eq:weff 잔존(LOW 처리).
6. v8(유도확장·**broadening 제거 후퇴**·KNOWN_DEFECTS 6종) → v9(LCO) → 6-30 radius 조사(w_eff 버그 진단·[과제 V8-1] 복원 지시) → v10(broadening 복원·apparent-U/η) → v1.0.10(코드-문건 동기화) → v1.0.11(수식화, P1.1 중단).

**★v12 방향성 관련 1급 소견(master)**:
- (F-1) 사용자의 6-11 방향 지시 "**Eyring 근본식에서 모든 것이 뻗어야**"는 Fable_v2가 척추로 구현했으나, **v7 재출발이 척추를 '코드 플로우차트'로 교체** — 이후 계보(v8~v1.0.10)는 Eyring-척추 아키텍처를 계승하지 않음. v12 재작성 시 이 방향성 회복 여부가 핵심 결정 사항.
- (F-2) v7의 17p 축소는 당시 사용자 의도 정합("실제 표현에 필요한 수식만")으로 기록됨 — 단 그 후 v8~v1.0.10이 다시 확장(87→167KB)하면서 **v3/v4/v5의 자산을 선별 복원**(broadening은 v10에서, 그러나 Eyring-척추·분포 일반형 등은 미복원). "축소→재확장" 왕복에서 무엇이 영구 유실됐는지가 챕터 1 감사의 핵심.
- (F-3) 푸쉬 이력 해명: RB 시절 "main 직접 push 분류기 게이트" 차단 회피로 rb-rebuild 브랜치 운용이 시작됨(6-02b 기록) — 이번에 main ff-merge로 정상화(b26b6b1→827ee48).
- (F-4) v7 결과문건이 스킬 한계 자인: "Codex는 분량·유도 약함(역할 한정 권장)" — 이번 스킬 개정(Fable 가중 3)과 정합.

### Step 5-6 — 버전×문건 매핑(골격)
| 버전 | 계획서 | 산출물 | 검수기록 | 인계 |
|---|---|---|---|---|
| RB Ch1~5 | 2026-05-30 undergrad-rederivation | docs/*_rebuilt(107p) | RB_LEDGER_CH*_FINE | HANDOVER_RB 3종 |
| Fable(50p) | 2026-06-10 textbook-rewrite | ch1_Fable.tex | PHASE_TBR_* | HANDOVER_06-10 |
| Fable_v2 | 2026-06-10 blank-rewrite-v2 | ch1_Fable_v2.tex(39p) | PHASE_V2_*(24회) | HANDOVER_06-11 |
| Fable_v3 | (기록 추적중 — A1) | ch1_Fable_v3.tex(200KB) | V3_W4_PHYSICS_AUDIT | — |
| Opus_v4/v5 | 2026-06-22 v5-rereview 등 | Opus_v4/v5.tex | COMPARISON_* | — |
| v6 | 2026-06-22 flowchart-reassembly | Opus_v6.tex | PHASE_V6_* | — |
| v7 | 2026-06-29 codeflow 9x9x1x1 | v7-11(17p) | PHASE2/4/6/8·LEDGER | PHASE8 RESULT |
| v8 | 2026-06-29 derivation-expanded | v8-11(21p) | REVIEW·ROUND·KNOWN_DEFECTS | — |
| v9 | 2026-06-30 2track | v9(30p) | v9 spine review1/2 | — |
| v10 | 2026-06-30 rework-broadening | v10(34p) | ch1v10 R1-R3·A1-A3 | 6-30 핸드오버 |
| v1.0.10 | 2026-07-01 code-doc-sync | v1.0.10(35p)+코드 742줄 | V1010_* 다수 | HANDOVER_v1.0.11 |
| v1.0.11 | 2026-07-02(파일명 07-07) | 증판+P1.1 supplement | V1011_* | (본 재검으로 supersede) |

### Step 8-12 — 전환 분석 5기 완료 + 종합 (Phase 1.2-1.3 ✅)
- 5기 전부 완료: A1(Fable, v3→v5)·A2(v5→v7)·A3(v7→v9)·A4(v9→v1.0.11)·A5(Ch2·코드). 노트 = `docs/Fable_점검/FABLE_AUDIT_note_A1~A5`.
- **종합 감사 문건 = `docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md`** — 계보(권위기록 경고 포함)·전환별 장단점/문제점 표·관통 패턴 6·★방향성 유실 표(Eyring 척추 미계승 F-1·S0-S5 절삭·§1.18 park·KWW scope-out)·v12 교훈 9·4-tier.
- 핵심 확정: v3→v6 자산 보존 양호(v4=순수추가·v5=식 verbatim·v6=손실0) / v7 의도적 재-스코핑이 왕복의 기점 / w_eff 오류가 설계doc 순응 검수 2R을 통과, 실행 실측이 반증(프로세스 1급 교훈) / LCO 산문은 v9 기원 / v1.0.11 byte 동일.
- gate PASS: 전 버전 커버(누락 0)·판정 줄근거(노트 인용)·문건 완결. INDEX 3행 추가(A2·A3·종합).
- (minor housekeeping) INDEX의 docs 구조 서술이 구구조(Ch1_v1.0.10/ 폴더식) — 현 docs/v1.0.10/ 통합 구조와 불일치. 챕터 4 정리 시 일괄 갱신 예정.

**챕터 1 종료. → 챕터 2(내용 감사) 착수.**

---

# 챕터 2·3 진행 (세부계획 = P2-P3 plan, 감사 6기 + master spine 통독)

## master(Fable) 직접 spine 통독 소견 (Step 14-18 CORE)
- 정독 구간(본 세션 누적): L100-295(서론·기호·매핑)·L295-513(lco-map·pol·center·lco-center)·**L515-683(hys 본체)**·L1204-1216·L1690-1765·**L1393-1537(N7 L_q·N8 꼬리)** + Ch2 다수.
- **M-1 [적발 후보·왜곡]**: fig:staging 하단 화살표 라벨(L286) "delithiation (discharge): ξ_j: **1→0**" ↔ 기호 규약(L206) "방전 시 ξ_j **0→1** 증가" **모순** — θ_j 자리에 ξ_j 오기 추정. C-1 교차확인 대기.
- **M-2 [무결]**: hys 유도 사슬(μ→g″→spinodal→ΔU_hys→U^d) 손검산 전 단계 통과(근의공식·logit 역수·artanh·평균대칭·부호방향). 압축점 2곳(평균장 cθ² 한 줄·θ→ξ 1차몫)은 G-follow 경미.
- **M-3 [무결]**: N7-N8 — z_cut=4.357 독립 재계산 일치(1/(4cosh²(z/2))=0.0125→z=4.357)·L_q 사슬(eq:Lq→kuniv→Acut→chid→dHeff→Lqfull→LV) 대입 검산 정합·"컷 동결=운영 미분 0·부등식=동기" 정직 서술 유지·적분인자→이산 저역통과 정합.
- **★M-4 [F-1 정련·CORE]**: 서론 L147-150 = "세 인자(T·전위·C-rate)가 모두 **하나의 속도식 k≈k₀exp[−ΔG_a/RT]** 의 서로 다른 자리로... 유도는 줄곧 이 한 식의 가지를 펼치는 일" — **Eyring-중심 서사는 서론에 계승돼 있음**. 6-11 지시의 미계승분은 정확히는 **구조적 배열**(Fable_v2의 식-first 전개 vs 현행 코드-순 N0→N9 배치). → v12 Decision Gate 항목 정정: "Eyring 척추 전면 회복" → "서사 유지 확인 + 구조 재배열(식-first) 여부 결정".


