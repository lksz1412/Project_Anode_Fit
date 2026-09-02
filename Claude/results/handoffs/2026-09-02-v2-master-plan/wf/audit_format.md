# AUDIT — 양식·게이트 렌즈 [format] · 대상 `wf/plan_draft_v2.md` (초안 v2)

> 작성 = 검수 에이전트 [format](Fable 5.1), 2026-09-03. 렌즈 = plan-execution 스킬 양식·게이트 렌즈(checklist §2 담당). 기준 = `brief.md`(전문)·`audit_checklist.md`(전문)·`SKILL.md`+`references/record-formats.md`(전문)·판독 산출 R1~R7(전문). 초안은 수정하지 않았고 감사 로그만 남긴다. 4-tier = 확정 / 근거 미발견 / 추정 / 미검증. 확정에는 path+line 을 붙였다. 결정은 master·사용자 몫이며 본 문건의 판단은 전부 [format] 출처다.

---

## ① 판정

**CONDITIONAL.** 11-section 이름·순서, Phase ID `<챕터>.<n>`, cumulative step 단조성(1–50, 리셋·중복·건너뜀 0), Decisions Required 분리와 4-요소(내용·근거·기본값·선택지), 병렬 self-authorization 부재, 구조 맵·신규 경로, Assumptions 의 load-bearing 성격, "적절해 보임"류 정성 게이트 부재는 전부 확인된다. 그러나 (1) Phase 단위 Result 규범과 챕터 단위 Result 설계의 충돌이 초안 안에서 서로 모순된 채 표면화되지 않았고(FORMAT-01), (2) 챕터 2·3 Phase 14개 중 9개에 brief §9 가 요구한 중단 조건이 없으며, (3) 게이트의 정량 수치 여러 곳이 Phase Range 표·본문·판독 원천 사이에서 어긋난다(행 카운트 이중 계산, 청크 줄수 오기, 유도 대상 산술, 열 수 불일치). 이들은 골격 변경 없이 수치·문구 정정으로 닫히는 항목이라 FAIL 이 아니라 CONDITIONAL 로 둔다.

---

## ② 발견 목록

| ID | 심각도 | 위치(초안 v2 절·행) | 내용 | 근거(4-tier · path+line) | 권고 |
|---|---|---|---|---|---|
| FORMAT-01 | **HIGH** | Phase 1.1~1.4·2.1~2.6·3.1~3.6 의 "다음 조건" 행(L276·L292·L301·L311·L327·L341·L351·L361·L371·L380·L409·L420·L429·L437·L444·L450) vs Implementation Interfaces L502 · Implementation Changes S-2 L253 · Test Plan T-14 L532 | 초안은 Result 를 챕터 단위 Phase(1.5·2.7·3.7, L315·L384·L454)에서만 생성하고, 1.1→1.2 같은 Phase 전이는 "Step 이력 파일 저장"만을 다음 조건으로 둔다. 반면 같은 문서의 운용 절은 "매 Phase 종료 시 Result 12항목 + Ledger(Result 없이 다음 Phase 금지)", S-2 는 "각 Phase 종료", T-14 는 "Result md+json 쌍 — 매 Phase" 라 적어 자기모순이다. 1.1~1.4 를 별도 Phase(ID `<챕터>.<n>`)로 선언한 이상 스킬 규범은 Phase 마다 Result 를 요구한다. brief §5 골격(L142·L153·L164)이 Result 를 독립 Phase 로 배치한 것이 기원이지만 초안은 이 충돌을 DQ 에 올리지 않았다 | **확정** — `SKILL.md`:150 "매 Phase 종료 시 Result 12항목(md+json 쌍) + Ledger 갱신. Result 없이 다음 Phase 진입 금지" · :161 "금지: 결과 저장 없이 다음 phase 진입" · :165 (2b) `PHASE_<phase-id>_<topic>_RESULT.md` · CLAUDE.md §0 "Result 생략 금지" · 초안 L502·L253·L532 vs L276 등 | (a) 1.1~3.6 각 Phase 의 다음 조건에 `PHASE_<1.1 등>_V2_<topic>_RESULT.md`+`.json`(12항목, 경량이라도) 을 넣고 1.5/2.7/3.7 은 챕터 통합 Result 로 재정의하거나, (b) 챕터 단위 Result 를 유지하려면 그것이 스킬 규범의 의도적 이탈임을 Decisions Required 에 사용자 결정 항목으로 올리고 L502·L253·L532 문구를 맞춘다. [format] 권고 = (a) |
| FORMAT-02 | MED | Phase 1.1 L266 · Step 2 L273 · Phase Range 1.1 행 L193 · DR-7 L616–619 · Non-goals L232 | DR-7 기본값 라벨은 "전문 정독 전부" 인데, 실제 배정 규칙(L273)은 "기정독 = 검수 sub 근거 행 대조 / 미정독 = 작업 sub 전문 정독 + 검수 대조" 다. 곧 판독 8본이 읽은 약 60본은 본 arc 안에서 어느 세션도 head→tail 로 다시 읽지 않고 인용 행만 대조한다. 이는 Non-goals L232 "판독 시드가 있어도 정독 배정을 줄이지 않는다" 와 brief 1.1 게이트 "전문 정독 = 전부 — 효율 이유로 축약하지 않음" 과 어긋나며, 라벨이 실제 하한을 가린다 | **확정** — 초안 L273·L232·L618 · `brief.md`:138 · CLAUDE.md 전문 정독 조항(부분 read 는 모든 영역 합쳐 cover) | DR-7 를 (i) 기정독분 포함 전건 arc 내 재정독(작업 sub head→tail) (ii) 기정독분은 검수 sub 근거 행 대조만 — 두 옵션으로 명시하고 기본값 라벨을 실제 규칙대로 적는다. 1.1 게이트에 "arc 내 정독 주체·행 범위" 열을 추가해 Read Coverage 가 판독 커버리지를 재사용하는지 드러낸다 |
| FORMAT-03 | MED | Phase 2.3 L351 · 2.4 L361 · 2.5 L371 · 2.6 L380 · 2.7 L385 · 3.3 L429 · 3.4 L437 · 3.5 L444 · 3.6 L450 | 챕터 2·3 Phase 14개 중 9개에 "중단 조건" 행이 없다(2.1·2.2·3.1·3.2 는 "없음" 이라도 명시). brief §9 는 챕터 2·3 에 "Phase·Step 범위·게이트·중단 조건·다음 조건" 을 요구하고 초안 머리말 L4 도 그렇게 자기 선언한다 | **확정** — `brief.md`:210 · 초안 L4 · 위 9개 절 본문 | 각 Phase 에 "**중단 조건.** 없음(발견은 GAP·정지 아님)" 또는 구체 조건을 한 줄씩 추가 |
| FORMAT-04 | MED | Phase Range 1.2 행 L194 · Phase 1.2 본문 L282 · 게이트 1.2 L292 · Implementation Changes R-2 L245 | "필수 31/31 + 병기 7" 에서 필수 30 안에 이미 RB·Fable v2 가 있고, 병기 7 에 "S1 구트랙 RB"·"S4 6-11 v2 백지" 가 다시 들어 있다. R1 의 S1 행이 곧 구트랙 RB, S4 행이 곧 Fable v2 백지 재작성이므로 두 행이 이중 계산돼 38 은 실제 36 이다. 이 수치가 게이트의 합격 조건이다 | **확정** — 초안 L282(필수 열거에 RB·Fable v2 포함, 병기에 S1·S4 포함) · `R1`:32(S1 구트랙 RB) · `R1`:35(S4 Fable v2 백지 재작성) | 행 집합을 한 번만 정의: 필수 31(brief 30 + v1.0.11) + 병기 5(S2·S3·E1·E3·계획 전용) = 36, 또는 RB·Fable v2 를 병기 쪽에서 제거. 게이트를 "36/36" 으로 |
| FORMAT-05 | MED | Phase 2.2 Step 17 L336 "2,705줄" · Step 18 L337 "2,853줄 · boxed 14 + N/A 2" | Ch1 곡선 사슬(sec00~sec10) 줄수는 R4a §1 표 합산 3,428 이고, Part T + §18 + 부록 A/B/E 는 2,073(+bib 57 = 2,130) 이다. 초안의 2,705/2,853 은 합(5,558)만 맞고 분할이 틀렸다. 그 결과 Step 17 "청크 ≤500 × 6" 은 7 이 돼야 한다. 또 N/A 2 중 하나(sec02a:12 로드맵 박스)는 Step 17 범위이므로 Step 18 의 "boxed 14 + N/A 2" 는 N/A 를 이중 계상한다(27+14 = 41 로 이미 전건) | **확정** — `R4a`:19–31 합산 3,428 · :32–47 합산 2,073 · :48 총계 5,558 · :63(N/A #2 = ch1_sec02a_part0:12) · :89(N/A #28 = ch2_sec00_intro:47) | Step 17 = 3,428줄·청크 7, Step 18 = 2,130줄·청크 5 로 정정; N/A 는 Step 17 에 1·Step 18 에 1 |
| FORMAT-06 | MED | Summary 표 기준 1 행 L18 | "boxed 64 중 유도 대상 57 = 사슬 완비 36·부분 18·없음 1·비유도 7" — 나열 항목 합은 62 이고 57 은 어느 조합과도 맞지 않는다(N/A 2 를 유도 대상에 넣으면 57 이나 그러면 36+18+1 = 55 ≠ 57). 같은 문서 §2.6 L117 은 36·18·1·9(=64) 로 정확하다 | **확정** — 초안 L18 vs L117 · `R4a`:104(있음 22·부분 16·없음 1·N/A 2) · `R4b`:138(완결 14·부분 2·비유도 7) | L18 을 "boxed 64 = 완결 36·부분 18·없음 1·비유도/N-A 9 → 유도 대상 55" 로 정정 |
| FORMAT-07 | MED | Phase Range 표 vs Phase 본문: 1.4(L196 "4열" vs L307·L311 "6열") · 3.1(L205 "평가 열 7" vs L406·L409 "8") · 3.3(L207 "각 6항목" vs L429 "각 8항목" vs Step 42 L426 나열 ≥10) | 같은 게이트의 정량 수치가 표와 본문에서 다르다. 열·항목 수는 "빈 셀 0" 게이트의 분모이므로 하나로 고정해야 검사가 가능하다 | **확정** — 위 행 | 각 게이트의 열·항목을 이름으로 열거하고(예: 1.4 = 원 지시 시점·유실 시점·현행 상태·재개방 여부·근거·시드 출처 = 6) 표와 본문을 동일 수치로 |
| FORMAT-08 | MED | §2.2 L60 "빌드 세트 60 tex 한정" · Step 14 L324 · Test Plan T-4 L522 "빌드 세트 tex 한정" | boxed 64 에는 독립 부록(마스터 미편입) 3 이, `\label` 429 에는 orphan `ch1_appD_si`(빌드 미포함, 라벨 7)가 들어 있다. "빌드 세트" 를 문자대로(마스터 `\input` 집합 = 58 파일) 적용하면 boxed 61·label ≠ 429 가 되어 T-4 의 "brief §4.2 전건 일치" 가 정의상 FAIL 한다. Step 14 가 "정의를 먼저 문서화" 를 요구해 완화되지만 라벨 자체가 오도한다 | **확정** — 초안 L65(독립 부록 3 포함)·L59(orphan)·L533(T-15 orphan 1 + 독립 1) · `R4b`:63–66 | "60 tex 전체(빌드 미포함 2 포함)" 로 명명하고, T-4 에 "카운트 집합 = 60 tex 전체 / 빌드 세트 58 별도 열" 을 명시 |
| FORMAT-09 | MED | Phase 1.5 L315 · 2.7 L384 · Implementation Interfaces 검수 강도 L506 | 등록부 3종·GAP REGISTER·THEORY BLUEPRINT 를 "A1·A2 통상 산출물 등급(1R 이상 + 연속 2R 수렴)" 으로 초안이 자체 판정했다. THEORY BLUEPRINT 는 DG-A/B/C 사용자 결정(L454)과 챕터 4 저작 전부의 유일한 근거라 reference 성격이 강하고, 헌법은 애매하면 고가치로 취급하라 한다. 등급 판정이 사용자·master 결정 없이 본문에 고정됐다 | **확정**(문면) — 초안 L315·L384·L506·L454 · CLAUDE.md §3 "고가치·reference 여부가 애매하면 고가치로 취급" | 검수 등급을 Decisions Required(또는 Assumptions)로 올리고 기본값은 최소 THEORY BLUEPRINT 를 고가치(10R + 렌즈 6종)로; 통상 등급을 유지하려면 근거를 명시 |
| FORMAT-10 | LOW | Correction History L571 · Decision Queue L718·L737 | "판독 DQ 총 97건(v1 17 + R1 10 + R2 12 + R3 16 + R4a 10 + R4b 10 + R5 12 + R6 12 + R7 15)" — 괄호 합은 114 이고 97 은 R1~R7 만의 합이다. (B) 표 머리 "97건" 도 같은 오기 | **확정** — 산술 · 각 R 문건 DQ 개수 실측(R1 10·R2 12·R3 16·R4a 10·R4b 10·R5 12·R6 12·R7 15 = 97) | "판독 DQ 97 + v1 17 = 114" 로 정정 |
| FORMAT-11 | LOW | 구조 맵 L152 · DQ-I10 L733 · 미해결 L759 | `audit_checklist.md` 를 `iter_1\` 아래로 적었으나 실물은 handoff 루트 `…/2026-09-02-v2-master-plan/audit_checklist.md` 다 | **확정** — Glob 실측(`iter_1/` = plan_draft.md·work_log.md 2건, `audit_checklist.md` 는 루트) | 경로 정정 |
| FORMAT-12 | LOW | L716 Decision Queue · L753 미해결 · L764 Read Coverage | 11-section 뒤에 절 3개가 더 붙어 있다. brief §9/§10 은 DQ·Read Coverage 를 work_log 소관으로 둔다. 본 파일이 그대로 `Claude/plans/` 마스터 플랜이 되면 12~14번째 절이 된다(11-section 순서 자체는 보존) | **확정** — `brief.md`:209·218 · 초안 L716 이하 | master 최종 저장 시 세 절을 handoff 노트/work_log 로 분리하거나 "부록(비-section)" 임을 표제에 명시 |
| FORMAT-13 | LOW | Assumptions L544–564 · 구조 맵 신규 예정 L158 | 스킬 1g 는 "없다/신규 작성" 전제 파일의 실물 부재를 Glob 로 확인하라 하는데, Assumptions 는 `Claude/docs/v2.0.0/` 부재(4)만 싣고 `Claude/plans/2026-09-02-v2-master-plan.md`·`PHASE_1-6_V2_EXECUTION_LEDGER.md`·`V2_*` 등록부 파일의 부재 전제가 없다 | **확정** — `SKILL.md`:100 · 초안 L158 vs L547 | "신규 예정 파일 전건 부재(GO 전 Glob)" 1항 추가 |
| FORMAT-14 | LOW | Test Plan T-2 L520 · T-1 L519 | T-2 명령 `PYTHONIOENCODING=utf-8 python …` 은 bash 환경변수 접두 구문이라 PowerShell 에서 그대로 실행되지 않고, T-1 `xelatex` 는 PATH 를 전제하나 Assumption 1(L544)은 PATH 미검증·전체 경로만 확인이라 적었다. 3a 의 "명령(실행 가능)" 조건이 환경 기준으로 약하다 | **확정** — 초안 L519·L520·L544 · CLAUDE.md Windows 도구 조항 | PowerShell 형(`$env:PYTHONIOENCODING='utf-8'; python …`)과 xelatex 전체 경로(또는 Bash 도구 사용 명시)를 병기 |
| FORMAT-15 | LOW | DR-6 기본값 L612 vs Implementation Interfaces 정지 조건 L503 | 기본값 "(iii) 는 2.6 진입 시 재확인" 은 3.7 외의 중간 확인 지점을 만드는데 정지 조건 목록에는 없고, 세 응답 선택지 어느 것과도 정확히 대응하지 않는다 | **확정** — 초안 L612·L613·L503 | (iii) 를 지금 결정 항목으로 두거나 "미승인 시 기확보 CSV 만으로 진행·DQ 기록(정지 아님)" 으로 명시 |
| FORMAT-16 | LOW | Implementation Interfaces L498 | "판독 단계의 8 에이전트 병렬은 본 arc 이전의 사전 조사이며 본 계획의 유닛 계수에 넣지 않는다" — 그 병렬의 승인 근거(사용자 sign-off·Workflow 지목)가 인용되지 않은 채 자기 선언으로 제외된다 | **근거 미발견** — 초안·brief 어디에도 판독 병렬의 승인 출처 기재 없음 | 승인 출처를 한 줄로 인용하거나 문장을 삭제(유닛 계수 규범은 헌법 §1-병렬) |
| FORMAT-17 | LOW | L18·L117·L339·L420·L526 "비박스 결과식 14" | R4a N1~N8 = 8, R4b 의 박스 우선순위 역전 후보는 라벨 7건(lco-kirchhoff·lco-SeV·lco-U1V·blend-dqdv·si-vshift·app-spinodal·app-maxwell)을 6 항목으로 묶은 것이라, 판정 "행" 을 라벨 단위로 세면 15 다 | **확정** — `R4b`:140 · `R4a`:108–117 | 판정 행 단위(라벨)를 명시하고 14 또는 15 로 고정 |
| FORMAT-18 | LOW | Phase 4.x 표 게이트 L466·L467·L473 vs L468·L470·L471·L472 | boxed 회수 게이트가 4.4(10)·4.6(27)·4.7(16)·4.8(4) = 57 만 수치화돼 있고 나머지 7(부록 E 4·독립 부록 3)은 4.2/4.3/4.9 에 수치 게이트가 없다. T-4 는 "boxed 64 회수표 100%" 를 요구한다 | **확정** — 초안 L65 분포(27/10/4/3/16/4) · L466–473 | 4.2 에 "독립 부록 3/3", 4.3 또는 4.9 에 "부록 E 4/4" 추가 |
| FORMAT-19 | LOW | Non-goals L230 vs §2.5 L106 · DQ 표 L742 | Non-goals 기각군에 "S0–S5 피팅 방법론" 이 있고, 같은 문서는 S0~S5 를 미계승 지속(§2.5)·R1 DQ-7 을 3.3/3.4 결정 후보로 두어 열려 있다. 닫힌 항목인지 열린 항목인지 독자가 구분할 수 없다 | **확정** — 초안 L230·L106·L742 · `R6`:323 | "피팅 알고리즘(Optuna 등) = Non-goal" 과 "역방향 식별 사슬의 본문 서술 여부 = 1.4/3.x 판정" 을 분리 표기 |
| FORMAT-20 | LOW | Implementation Interfaces git L504 | 스킬 3c 의 "매 phase = [작업 commit] + [검토·정정 commit] 페어" 가 빠져 있다(각 Step/Phase 종료 commit 만) | **확정** — `SKILL.md`:210 · 초안 L504 | 페어 규약 1줄 추가 |
| FORMAT-21 | LOW | §2.1 L54 · §2.3 L86 · Assumptions 19 L562 | v1.0.26 상태를 R2(실물 근거)로 정정했으나, 같은 날 판독 R5·R6 은 여전히 "실행 차단·미완" 을 확정으로 적는다. Assumption 19 의 판독 간 상충 목록에 이 항목이 없다 | **확정** — `R5`:12 · `R6`:224 vs `R2`:182–192 | 상충 목록에 추가하고 "R2 실물 근거 우선" 을 명기 |
| FORMAT-22 | LOW | 게이트 1.3 L301 "D21-1~6 = 6 행" | 초안이 시드로 삼은 R3 A-6 은 D21-1·2·3·5·6′ 다섯 행만 두고 D21-4 는 없다. 6 행이 실물(HANDOVER_v1.0.20 L32–44 의 D21-1~6 표, R2 §2.1)에는 있을 수 있으나 초안의 근거 사슬로는 5 다 | **미검증**(원천 실물 미열람) — `R3`:125–129 · `R2`:52 | Step 9 정독 후 확정하되 게이트 수치의 출처를 R2 원천으로 명시 |

---

## ③ 최약점 1곳

**FORMAT-01 — Result 단위의 자기모순.** 초안은 스킬·헌법이 절대 조항으로 두는 "Phase 종료마다 Result(md+json) → 다음 Phase" 를 운용 절·Test Plan·산출물 대장에 그대로 옮겨 놓고, 정작 Phase 본문은 1.1→1.2, 2.1→2.2, 3.1→3.2 전이를 Step 이력만으로 넘긴다. 실행에 들어가면 첫 Phase 전이에서 곧바로 T-14("Result md+json 쌍 — 매 Phase")와 L502 의 금지 조항에 걸리고, Ledger 1.1~1.4 행의 Result 열은 비게 된다. brief 골격이 기원이라 초안 저자가 재설계하지 않은 것은 경계 준수이지만, 이 충돌을 Decision Queue 에 올리지 않은 것은 감사 관점에서 가장 큰 공백이다. 다른 발견(수치 불일치·중단 조건 누락)은 국소 정정으로 닫히지만 이것은 실행 골격의 게이트 정의를 바꾼다.

---

## ④ 기준 1)~6) ↔ Phase/게이트 추적표

해당 없음 — spec 렌즈 담당. 참고로 초안 Summary 표(L16–23)가 이미 기준 1~6 각각을 진단 축·설계·게이트·검수 렌즈에 1:1 로 매핑해 두었으므로 spec 렌즈는 그 표를 출발점으로 삼을 수 있다.

---

## ⑤ Read Coverage (파일·행 범위 전건 — head→tail)

| # | 파일 | 행 범위 | 방식 |
|---|---|---|---|
| 0 | `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md` | 1–219(전문) | Read |
| 1 | `…/audit_checklist.md` | 1–48(전문) | Read |
| 2 | `…/wf/plan_draft_v2.md`(대상) | 1–118 · 119–228 · 229–338 · 339–448 · 449–560 · 561–672 · 673–784(전문, 7분할 합쳐 전 영역) | Read |
| 3 | `C:\Users\lksz1\.claude\skills\skill_LKS_original_plan-execution\SKILL.md` | 1–239(전문) | Read |
| 4 | `…\references\record-formats.md` | 1–42(전문) | Read |
| 5 | `…/wf/R1_version_register_v3_to_v1019.md` | 1–91 · 92–206(전문) | Read |
| 6 | `…/wf/R2_version_register_v1020_to_v1026.md` | 1–75 · 76–150 · 151–300(전문) | Read |
| 7 | `…/wf/R3_binding_decisions_and_lost_directions.md` | 1–200 · 201–398(전문) | Read |
| 8 | `…/wf/R4a_diagnosis_scope_ch1_partT.md` | 1–120 · 121–240 · 241–363(전문) | Read |
| 9 | `…/wf/R4b_diagnosis_scope_ch2_ch3_appendix.md` | 1–110 · 111–220 · 221–330 · 331–431(전문) | Read |
| 10 | `…/wf/R5_theory_candidates_thermo_statmech.md` | 1–110 · 111–220 · 221–330 · 331–426(전문) | Read |
| 11 | `…/wf/R6_theory_candidates_kinetics_hys_heat.md` | 1–110 · 111–220 · 221–330 · 331–415(전문) | Read |
| 12 | `…/wf/R7_reference_master_map.md` | 1–110 · 111–220 · 221–330 · 331–440 · 441–534(전문) | Read |
| 13 | `…/2026-09-02-v2-master-plan/` 폴더 | 파일 목록만(14건) | Glob |

안 읽은 것(미검독 — 추정 금지): `iter_1/plan_draft.md`·`iter_1/work_log.md`(초안 v1 — 대상 밖) · `wf/R7_reference_master_map.json` · 원천 실물 전부(`_sections/*.tex`·`docs/**`·`plans/**`·PDF·코드 — 본 감사의 path:line 은 판독 산출과 초안이 기록한 것을 대조한 것이며 실물 재대조는 1.1~1.2·2.1 소관) · `CLAUDE.md`(시스템 주입본으로만) · `Codex/`(금지). 산출 파일 = 본 파일 1건. 기존 파일 생성·수정·삭제 0 · git 명령 미실행 · Codex 무접근.

---

## Decision Queue ([format] — 골격 이견·추가 후보, 결정은 master·사용자)

- **DQ-F1** FORMAT-01 의 처리 방향(Phase 마다 Result vs 챕터 단위 Result 유지·사용자 결정 승격). 근거 = SKILL.md:150·161·165. 기본값 제안 = Phase 마다 Result.
- **DQ-F2** FORMAT-02 — DR-7 의 옵션 재정의(기정독분 재정독 여부). 근거 = brief:138·초안 L232·L273.
- **DQ-F3** FORMAT-09 — THEORY BLUEPRINT 의 검수 등급을 결정 항목으로 승격할지. 근거 = 초안 L454·L506.
- **DQ-F4** FORMAT-12 — 최종 저장본에서 Decision Queue·미해결·Read Coverage 세 절의 위치(work_log 분리 vs 부록 표기).
- **DQ-F5** FORMAT-16 — 판독 8본 병렬의 승인 출처 인용 여부.
