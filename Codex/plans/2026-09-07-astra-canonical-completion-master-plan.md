# Astra 개정 마스터플랜 — v1.0.25.2 학술 정본 완결

정본일: 2026-09-07
상태: 사용자 요청에 따른 개정 계획; 과학 Gate 통과를 선언하지 않음.
활성 branch: codex/anode-fit-v1025_2-canonical-completion
책임 전환 checkpoint: aedfd408281b97699ba7f75884e7108965ecf547

## Summary

목표는 기존 Claude/Codex 성과를 원천과 대조하여 활용하고, 수식 유도와 검증된 1차 문헌에
근거한 대학원 교과서 형식·리뷰 논문 수준의 이론 문건, LaTeX에서 재빌드한 PDF,
별도 Implementation Companion, 재현 가능한 machine package를 완성하는 것이다.
현재 감사 단계가 학술 원고 완성으로 오인되지 않도록 두 진행 상태를 따로 보고한다.

이 개정은 사용자가 요청한 Astra 책임 전환과 작업 속도 개선을 반영한다.
과학 검독·원문 확인·누적 Step·스텝별 commit/push를 줄이지 않는다.
대형 이력을 여러 control 문건에 반복 전사하거나 같은 validator를 매 Step 새로 만드는 비용을 줄인다.
수식·자료 근거가 확보된 뒤에는 그 phase의 유도를 Codex/docs에 직접 축적하여,
Phase 087에서 처음 본문을 쓰기 시작하는 지연을 없앤다.

## Current Ground Truth

### 직접 확인한 현재 상태

- Step 93 저장 commit: 0b850ea9ffa33e04356d11b83190f9a7cfbea37c.
- Sol→Astra WIP checkpoint: aedfd408281b97699ba7f75884e7108965ecf547.
  정상 push 후 local HEAD=live origin, 단일 parent=Step 93, clean tree를 확인했다.
- 이 checkpoint는 기존 여섯 변경 파일과 새 전환 문건만 보존한다. Step 94 완료가 아니다.
- PHASE_068_U13_REGSOL_REDERIVATION.json은 checkpoint 시점에 없다.
  기존 Step 94 --content-only는 E_MATRIX_MISSING으로 실패했다.
- 후보 result/ledger의 PASS_PENDING_PERSISTENCE와 complete precommit은
  실행된 content PASS 증거가 아니다. 새 checkpoint와 이 계획이 현재 상태 해석을 정정한다.
- Step 94 수식/계산 소스는 존재한다. 실제 artifact 검증·정정 결과·완료 commit은 앞으로 수행한다.
- 현재 학술 정본 LaTeX/PDF 완성은 미달성이다. 감사 commit 수를 완성률로 환산하지 않는다.
- Sol→Astra는 사용자 지정 주 담당 전환이다. 과거에도 Astra 서브 검독이 있었으므로
  모든 이전 행을 오직 Sol이 작성했다는 모델별 저작 증명은 하지 않는다.

### 보호 및 역사적 기준선

- repository: https://github.com/lksz1412/Project_Anode_Fit
- protected Codex tip: fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71.
- current main observed tip: f0c381bd6dc315ac75cbffa93dd86ce83a37949b.
- frozen Claude review tip: e3e1a634f34b711aa4803fd190fe9120f1755f13.
- frozen Codex conformance tip: 11f90544865dd179739ca5bc5062b28c1078e504.
- frozen common ancestor: 3b5fd059ed09cdcdde38668c399cb35b8afbcca9.
- Claude의 학술 입력 directory는 Claude/docs/v1.0.25.2이며, v1.0.26A/B 피팅
  비교 실험 명칭을 새 학술 release로 취급하지 않는다.
- Phase 055–063 PASS, 064–067 CONDITIONAL은 이전 ledger의 저장된 판정이다.
  이번 계획 수립 때 전 phase의 과학 실행을 재수행한 것으로 보고하지 않는다.
- Ref. 7 원문, 원 optimizer state, specimen/protocol·held-out·재료/기전 근거,
  stale PDF, internal conformance 미해결 사항은 자동 해소되지 않는다.

### 읽은 계획과 복구 chain

- Codex/AGENTS.md 및 Codex/plans/phase_planning_operations_guide.md 전문.
- Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md 1–665 전문.
- Codex/plans/2026-09-07-phase068-claude-codex-fork-adjudication-detailed-plan.md 1–801 전문.
- Codex/results/PHASE_068_STEP_094_U13_REGSOL_REDERIVATION_RESULT.md 1–394 전문.
- Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md
  Phase 069 389–417행 직접 확인; 이번 재개에서 해당 파일 전체 검독으로 계수하지 않는다.
- 기존 두 ledger와 ACTIVE_HANDOVER_CANONICAL_COMPLETION.md는 역사 chain으로 보존한다.
- 전환 사실/실패 증거의 정본: Codex/results/PHASE_068_STEP_094_SOL_ASTRA_HANDOFF_CHECKPOINT.md.
- 현재 상태의 정본은 새 ASTRA_CANONICAL_COMPLETION_EXECUTION_LEDGER.md와
  ACTIVE_HANDOVER_ASTRA_CANONICAL_COMPLETION.md이다. 과거 marker를 현재 상태로 읽지 않는다.

## Phase Range

누적 번호는 기존 전체 1–351을 그대로 유지한다. 완료된 1–93을 다시 번호 매기지 않고,
다음 과학 실행은 미완료 94의 계속 작업이다. checkpoint/계획 activation은 새 정수 Step을 소비하지 않는다.
94–351을 병합·삭제하지 않는다. 세부계획을 실행 전 저장하고 각 Step 결과를 남긴다.

| Phase | Steps | 이름 / 상태 |
|---|---:|---|
| 055–063 | 1–63 | 기존 계보 감사 / 저장된 PASS, 이번 개정에서 실행 재승인 아님 |
| 064–067 | 64–90 | 기존 계보·코드 교차감사 / CONDITIONAL 유지 |
| 068 | 91–98 | fork 판정 / 91–93 persisted, 94 WIP, 95–98 pending |
| 069 | 99–107 | canonical audit와 launch decision / pending |

조건부 후속 phase의 범위와 산출물은 다음과 같다.

| Phase | Steps | 이름 | 핵심 산출물 |
|---|---:|---|---|
| 070 | 108–115 | post-audit 기준선 동결 | source freeze, requirement register |
| 071 | 116–127 | 문헌·DOI truth audit | claim–source evidence ledger |
| 072 | 128–139 | 데이터 provenance·feasibility | public-data registry |
| 073 | 140–149 | 정본 이론 아키텍처 | equation dependency graph |
| 074 | 150–159 | 좌표·보존·관측 기초 | common foundation derivation |
| 075 | 160–173 | 평형·상공존·상장 | equilibrium/phase-field derivation |
| 076 | 174–187 | 비평형 kinetics·transport | protocol-aware dynamic derivation |
| 077 | 188–199 | Graphite closure | staging material chapter |
| 078 | 200–211 | doped high-voltage LCO closure | LCO material chapter |
| 079 | 212–223 | Si/SiOx/Si–C closure | silicon material chapter |
| 080 | 224–233 | Graphite+Si blend closure | common-voltage blend chapter |
| 081 | 234–245 | 열·관측·식별성·불확도 | inference and validation chapter |
| 082 | 246–255 | 정본 방정식 freeze | independent derivation audit |
| 083 | 256–267 | 이론–구현 contract | implementation companion design |
| 084 | 268–281 | alpha reference implementation | TDD reference model |
| 085 | 282–293 | 구조·기본값 고정 | stable model/API structure |
| 086 | 294–307 | 실제 데이터 calibration | held-out material validation |
| 087 | 308–319 | 학술 원고 조립 | monograph + companion sources |
| 088 | 320–331 | independent red-team | repairs and scientific gate |
| 089 | 332–341 | LaTeX·PDF release QA | rebuilt verified PDFs |
| 090 | 342–351 | clean-clone release | reproducibility and handover |

## Non-goals and Scope Guards

- Phase 069 GO/CONDITIONAL_GO 전에 070–090을 실행하거나 최종 model family,
  목차, material default, 구현 구조를 확정하지 않는다. NO_GO이면 repair addendum으로 돌아간다.
- 보호 branch, main, Claude/**, 기존 계획서·완료 결과서·원문 PDF를 덮어쓰지 않는다.
  채택 source의 수정은 이후 Codex-owned 학술 tree에서만 수행한다.
- whole-commit cherry-pick/merge, model 이름만으로 정본 선택, BIC 우세로 phase identity 인정 금지.
- synthetic fit/golden roundtrip/internal consistency를 외부 재료·기전·held-out 증거로 승격하지 않는다.
- DOI 실재 여부와 원문 claim support를 분리한다. 구체 DOI와 실제 논문·교재 원문
  page/section/equation을 확인하지 못하면 UNVERIFIED로 남긴다. 인용·수식·데이터를 꾸며내지 않는다.
- 근거 없는 cap/clip/clamp/smoothing/threshold/fallback을 물리 법칙으로 승격하지 않는다.
- 본문·caption·footnote·visible heading에 코드/함수/class/파일/key/API/test,
  commit/branch/phase/step/작업 이력 언급 금지. 지정 구현 부록 또는 별도 companion만 예외다.
- 이론은 비유로 유도를 대체하지 않는다. 정의→가정→보존/열역학 관계→중간식→극한→관측량 순서를 따른다.
- 원문을 읽지 않은 검독, 실행하지 않은 시험, 렌더만 한 PDF 시각검수는 완료라고 보고하지 않는다.
- 성능 최적화는 equation/structure/검증 기준선 확정 뒤에만 한다. 알파→구조 고정→가속화 순서를 유지한다.

## Implementation Changes

| Surface | 경로 / 책임 | 변경 종류 |
|---|---|---|
| Master plan | Codex/plans/2026-09-07-astra-canonical-completion-master-plan.md | 신규; 기존 master 보존 |
| Current detailed plan | Codex/plans/2026-09-07-phase068-astra-continuation-detailed-plan.md | 신규; 94–98 절차 명시 개정 |
| Future detailed plans | Codex/plans/YYYY-MM-DD-phaseNNN-<topic>-detailed-plan.md | phase 진입 전 신규 |
| Step results | Codex/results/PHASE_NNN_STEP_NNN_<TOPIC>_RESULT.md | 매 Step 신규; 과거 결과는 addendum으로 정정 |
| Machine evidence | Codex/results, 해당 결과 옆 | 계산/coverage/gate 재현에 필요할 때 생성 |
| Current index | Codex/results/ASTRA_CANONICAL_COMPLETION_EXECUTION_LEDGER.md | 신규 후 현재 행 갱신 |
| Recovery handover | Codex/results/ACTIVE_HANDOVER_ASTRA_CANONICAL_COMPLETION.md | 신규 후 현재 포인터 갱신 |
| Scholarly deliverables | Codex/docs | theory LaTeX/PDF, 별도 companion; 실제 tree는 Phase 073에서 확정 |
| Auxiliary tools | Codex/work | 기존 검산·공통 검증 재사용, 필요한 최소 보조 도구 |
| Final package | Codex/results/release | Phase 090에서 source/PDF/companion/재현 자료 zip |

사용자 지정 3단 구조의 주 자료 저장 위치는 Codex/{plans,results,docs}이다.
Codex/work는 실행 보조 도구일 뿐 계획·이력·학술 원고를 대신 저장하는 우회 경로가 아니다.
기존 artifacts를 이 구조에 맞춘다는 이유로 이동/재작성하지 않는다.

## Execution and Compaction Recovery Protocol

### 본격 실행 전

1. 이 master와 해당 phase detailed plan을 먼저 저장한다.
2. detailed plan에 입력 파일 목록/전문 범위, step별 실행, 산출물, 검증, 중단 조건을 고정한다.
3. 직전 result와 ledger의 마지막 완료/첫 미완료 Step, HEAD/branch/dirty/원격을 대조한다.
4. 의존 gate가 충족된 현재 Step만 실행한다. scope 밖 개선은 추가 후보로 남긴다.

### 매 Step 종료

1. 실제 입력·읽은 범위·생성/수정 파일·명령·실행 결과·판단·미결·다음 조건을 결과서에 쓴다.
2. 계산·coverage·gate에 필요한 원 숫자/표, 입력 identity, runtime/명령/exit/stdout/stderr를 보존한다.
   digest만 남기고 원 실행 근거를 버리지 않는다. 재현 가능한 결정적 본체와 runtime receipt를 분리한다.
3. result-first/JSON-last는 source/control identity 수집이 필요한 감사에서 유지한다.
   최종 report hash를 그 report 자체가 담아야 하는 자기참조 검증은 만들지 않는다.
4. 기존/phase 공통 검증기를 재사용한다. 새 predicate가 있을 때만 검증을 추가한다.
   단순 기록 단계마다 독립 수천 행 validator를 제작하지 않는다.
5. 변경된 과학/코드에 실제 관련된 검증과 독립 검토를 수행한다. 발견된 문제를 고치면 같은 검증을 재실행한다.
6. compact ledger에는 한 row와 canonical result/artifact 포인터를 갱신한다. handover에는 현재 두 계획,
   직전 결과, 첫 미완료 Step, 열린 경계만 갱신한다. 과거 전문을 여러 곳에 재전사하지 않는다.
7. exact path allowlist, 변경 이유, 검증 결과/미확인, Git diff/mode를 확인한다.
8. Step 결과·산출물을 포함해 active branch에 commit하고 push한다. live origin=local HEAD,
   예상 단일 parent/pathset, clean tree를 확인한 뒤에만 다음 Step으로 간다.
9. precommit 결과는 CONTENT_VERIFIED_AWAITING_PUSH로 표시할 수 있다.
   PERSISTED는 실제 Git 확인 뒤에만 부여한다. 같은 commit의 hash를 미리 예언하지 않는다.

### 컴팩션 / 모델 교체 / 중단 후 재개

1. 활성 master plan을 1행부터 EOF까지 직접 다시 읽는다.
2. 현재 phase detailed plan을 1행부터 EOF까지 직접 다시 읽는다.
3. 직전 Step result를 1행부터 EOF까지 직접 다시 읽는다. WIP이면 최신 checkpoint/result도 읽는다.
4. compact ledger와 active handover에서 canonical chain, 완료/미완료, 조건을 대조한다.
5. 필요한 판단의 원문/result/machine artifact를 직접 열고 hash/범위를 확인한다.
6. HEAD/branch/dirty/live origin을 확인하고 Git 증거와 기록이 일치할 때만 재개한다.
7. 불일치나 미확인 내용을 요약·이전 자기보고로 메우지 않는다.

같은 연속 세션의 다음 Step에서는 변경하지 않은 대형 역사 ledger 전부를 반복 재독하지 않는다.
새 Step의 명시 입력·직전 결과는 읽고 변경된 내용/의존 판단을 확인한다.
이 조항은 컴팩션 후 3종 전문 재독 의무를 면제하지 않는다.
전문 검독은 실제 1–EOF coverage로 계수하며, 해시로 확인한 이전 read 재사용은 fresh read와 분리한다.

### 검증 비용의 종료 기준

- 실제 과학 predicate, source identity, schema, 선언된 I/O/환경/Git 경계, 관련 regression을 검사한다.
- 임의 AST 공격 변종에 대한 범용 Python sandbox 개발을 이 연구의 필수 과제로 확대하지 않는다.
- 같은 불변 코드에 대한 반복 검수는 새 concrete finding이 없으면 종료한다.
- Phase 082 독립 재유도, 088 전체 scientific red-team, 089 전 페이지 PDF 시각검독,
  090 clean-clone 재현은 삭제하거나 간단한 hash 확인으로 대체하지 않는다.
- 외부 근거가 없는 항목은 한 claim/material의 UNVERIFIED/CONDITIONAL로 한정한다.
  이를 전역 PASS로 위장하거나 읽을 수 있는 독립 범위를 함께 중단하지 않는다.

## Phase 068 — Fork Adjudication Continuation

91–93은 이미 persisted된 과거 실행이다. 94의 후보를 새 작업처럼 재작성하지 않고 증분 검산한다.

94. 기존 U13 binodal/중앙질량 대체/좌우 미분 유도를 검산하고 8개 원천,
    수치 재현·고정 kernel 가정·정규화 2배 결함을 별도 판정한다.
    missing matrix와 오래된 시험 수치를 정정 addendum으로 닫는다.
95. frozen conformance_model 11 paths와 tests 10 paths, empirical artifact와 대응 원고식을 전문 검독하고,
    scientific authority / implementation value / duplication 세 축을 독립 판정한다.
96. 두 fork의 모든 claim을 conflict/compatible/superseded/open으로 연결한다.
    source object/range, 변수·가정·domain 차이, 근거와 미결 owner를 보존한다.
97. 모든 file/issue/claim에 ADOPT/REWRITE/REFERENCE_ONLY/REJECT/UNVERIFIED 중 하나를 부여하고,
    inherited/resolved/new carry delta와 owner/수용 조건을 누락 없이 연결한다.
98. file/issue-specific downstream adoption plan과 phase report를 닫는다.
    두 fork의 commit/edge/path/read/claim/판정 coverage를 모두 확인한 경우에만
    PASS_P068_FORK_ADJUDICATION을 부여한다. 그 외 NOT_ACHIEVED이며 069로 가지 않는다.

산출물: 기존 상세계획의 Step 94–98 과학 evidence/결과서 및 신규 continuation addendum.
Git 관련 상세계약 변경은 별도 current detailed plan에 명시한다.
Claude 2 commits/2 edges/3 net paths, Codex 5/6/135 events/69 net paths,
merge 두 parent, 별도 main planning drift를 혼합하지 않는 게이트를 그대로 보존한다.
과학 Gate와 persistence는 별개이며 WIP checkpoint로 과학 Gate를 통과시킬 수 없다.

## Phase 069 — 전체 종합·새 작업 착수 게이트

### Steps 99–107

99. Phase 057–068의 결정·결함·보존 항목을 하나의 canonical audit로 통합한다.
100. 사용자 목표를 관측–열역학–동역학–전기화학–재료–피팅 순서로 다시 정식화한다.
101. 이론 본문에 남길 내용과 외부 구현 계약으로 이동할 내용을 확정한다.
102. empirical, reduced-physics, production-physics 모델 계층을 분리한다.
103. graphite, high-voltage doped LCO, Si, graphite+Si별 데이터 요구량과 식별 가능성을 확정한다.
104. 공개 데이터만으로 검증 가능한 주장과 사용자 데이터가 필요한 주장을 분리한다.
105. 새 이론·코드 완결 계획의 입력 요구사항과 선행 문헌 조사 목록을 확정한다.
106. read coverage, manifest, ledger, open issue 및 모든 phase gate를 재검증한다.
107. GO, CONDITIONAL_GO, NO_GO 중 하나로 새 작업 착수 여부를 판정한다.

산출물: canonical audit, requirements/carry register, launch decision, phase result.
PASS_P069_REAUDIT_COMPLETE의 원래 조건을 유지한다:
1,520 paths 처분, 862 기준 blobs 또는 Phase 056 정정 분모 전체 검독,
고유 text 전문/PDF 전 페이지/그림 시각/binary 비파괴/관련 실제 commit diff coverage,
사용자 의도 원천 연결, 미확인과 PASS 분리, 기존 원천 미수정.
숫자는 historical baseline이며 실제 corrected manifest와 대조한다.
필수 coverage 공백 또는 근거 없는 정본 선택이 필요하면 NO_GO/repair이고 070을 시작하지 않는다.

## Phase 070–090 — 단계별 원문 과제 승계와 증분 원고 작성

아래 Step 108–351의 numbered action과 phase Gate는 기존 2026-08-25 master에서
원문 그대로 승계했다. 요약표만으로 세부 조건을 대체하지 않는다.
보조 validator는 위 공통 규칙에 따라 재사용할 수 있으나 검증 predicate는 유지한다.
각 phase의 입력은 직전 gate/result 및 해당 번호가 지정한 원문·데이터이며,
산출물과 exact path는 진입 전 상세계획에서 확정한다.
필수 gate 실패 시 그 의존 작업은 중단한다. 이는 아래 모든 phase의 공통 stop/entry 규칙이다.

Astra의 authoring 변경: Phase 073에서 Codex/docs tree를 결정하고,
074–081의 검증된 유도를 해당 LaTeX section에 직접 작성한다.
Phase 087 Steps 308–319는 이미 쓴 내용을 재사용·조립·교차대조하는 단계이며,
앞선 작성으로 그 번호들을 선행 완료 처리하거나 skip하지 않는다.
미검증 이론을 원고로 선제 확정하는 권한은 아니다.

## Phase 070 — Post-audit 기준선 동결

### Steps 108–115

108. Phase 069 canonical audit와 launch decision을 전문 재독하고 모든 조건을 입력 register로 변환한다.
109. main, Claude latest, protected Codex, active branch의 commit hash와 tree boundary를 source-freeze manifest에 기록한다.
110. Phase 069의 채택·정정·기각·미검증 판정을 claim, equation, implementation, data 영향으로 분해한다.
111. 기존 master, ledger, handover의 stale pointer와 현재 신규 chain을 non-destructive supersession으로 정리한다.
112. canonical theory, implementation companion, evidence ledger, reference implementation, data registry의 책임 경계를 확정한다.
113. claim/source/equation/data/implementation/test ID schema와 상호 참조 규칙을 확정한다.
114. Python, XeLaTeX, fonts, Poppler, PDF extraction, clean-clone에 필요한 환경 기준선을 조사한다.
115. source freeze, schema, environment와 Phase 069 condition을 검증하고 `PASS_P070_POST_AUDIT_FREEZE` 여부를 판정한다.

### Gate

Phase 069의 조건이 누락 없이 추적되고 보호 branch diff가 0이며 artifact 책임과 ID schema가 고정될 때만 Phase 071로 진입한다.

## Phase 071 — 문헌·DOI Truth Audit

### Steps 116–127

116. 기존 세 장 bibliography와 본문 citation occurrence를 전수 manifest로 만든다.
117. 저자, 제목, 저널, 연도, 권, 호, 페이지·article number, DOI를 정규화한다.
118. DOI resolver와 출판사 record에서 metadata 실재성과 correction/retraction 상태를 검증한다.
119. load-bearing claim별 필요한 원 논문·교재 원문 목록을 확정한다.
120. 확보한 원문을 page/section/equation/figure/table 단위로 전문 검독하고 file hash를 기록한다.
121. 원문 변수와 Project_Anode_Fit 변수의 mapping 및 적용 불가 가정을 기록한다.
122. review paper와 textbook은 배경·종합 범위로, 1차 논문은 구체적 물리·데이터 근거로 분리한다.
123. abstract-only, metadata-only, 내부 검증, secondary citation 항목을 load-bearing 근거에서 제외한다.
124. 동일 DOI/다른 제목, 오기 DOI, article number 누락, 실제 scope 충돌을 판정한다.
125. 각 claim을 `CONFIRMED`, `PARTIAL`, `CONFLICTING`, `UNVERIFIED`, `REJECTED_SOURCE`로 분류한다.
126. 모든 equation·material parameter에 최소 source tier와 exact anchor가 있는지 검증한다.
127. DOI·원문·claim linkage validator를 실행하고 `PASS_P071_REFERENCE_TRUTH` 여부를 판정한다.

### Gate

원문 미확인 claim은 정본 근거로 사용하지 않는다. load-bearing claim 전부가 exact source anchor 또는 명시적 `UNVERIFIED` 처분을 가져야 한다.

## Phase 072 — 데이터 Provenance와 Feasibility

### Steps 128–139

128. graphite, Si, graphite+Si, doped high-voltage LCO의 공개 dataset 후보를 조사한다.
129. 원자료 URL, license, specimen, chemistry, electrode loading, capacity basis와 protocol metadata를 기록한다.
130. temperature, rate, rest/equilibrium, voltage window, sampling resolution과 replicate 수를 기록한다.
131. raw file hash, 다운로드 시점, 원본 format과 비파괴 보존 경로를 정한다.
132. ICA/DVA 계산에 필요한 smoothing, interpolation, differentiation 전처리 후보를 원자료와 분리한다.
133. 측정 분해능과 reported uncertainty가 peak width·shift 식별성에 미치는 하한을 계산한다.
134. 다온도·다율속·독립 specimen·held-out 조건 충족 여부를 재료별로 판정한다.
135. equilibrium GITT, pOCV+hold, calorimetry, entropy coefficient, structural characterization 필요성을 연결한다.
136. fitting에 사용할 수 있는 데이터와 문헌의 qualitative illustration만 가능한 데이터를 분리한다.
137. 공개 데이터가 없는 주장과 사용자 전용 데이터가 필요한 주장을 분리한다.
138. data provenance와 preprocessing recipe를 deterministic registry로 만든다.
139. data feasibility validator를 실행하고 `PASS_P072_DATA_FEASIBILITY` 또는 조건부 범위를 판정한다.

### Gate

원자료 provenance와 protocol이 없는 CSV는 최종 validation에 사용하지 않는다. 데이터 부족은 claim을 conditional로 제한하되 다른 재료의 진행을 막는 전역 PASS로 위장하지 않는다.

## Phase 073 — 정본 이론 Architecture

### Steps 140–149

140. Phase 069–072의 확정 claim, source, data feasibility를 이론 요구사항으로 통합한다.
141. observable, conservation, equilibrium thermodynamics, nonequilibrium kinetics, transport, microstructure와 measurement 층을 분리한다.
142. external capacity, composition, reaction extent, internal potential, terminal voltage와 time 좌표를 정의한다.
143. 모든 핵심 식에 stable Equation ID와 dependency를 부여한다.
144. 식마다 assumptions, dimensions, sign, independent variables, domain, limits와 data prerequisite를 기록한다.
145. graphite, LCO, Si와 blend의 공통 인터페이스와 재료별 확장 경계를 정의한다.
146. empirical observation kernel, reduced-physics model, production-physics model의 권위를 분리한다.
147. 단일 canonical book driver, section tree, derivation appendix와 companion tree를 설계한다.
148. 순환 external reference와 legacy label을 안전하게 mapping하는 migration table을 작성한다.
149. equation DAG와 document topology validator를 실행하고 `PASS_P073_THEORY_ARCHITECTURE` 여부를 판정한다.

### Gate

모든 하위 물리식이 보존법칙과 관측식으로 연결되고, 코드 구조가 이론 선택을 역으로 지배하지 않을 때만 본문 유도로 진입한다.

## Phase 074 — 좌표·보존·관측 기초

### Steps 150–159

150. 전극 반응 진행방향, lithiation/delithiation, half-cell/full-cell 전압과 signed current convention을 유도한다.
151. 조성, 몰수, 전하, 누적 용량과 specific/areal/absolute capacity basis의 변환을 유도한다.
152. 전하 보존으로 내부 전극전위 또는 공통 화학퍼텐셜을 결정하는 음함수계를 유도한다.
153. equilibrium potential와 terminal voltage의 과전압·저항·수송 분해를 유도한다.
154. (Q(V)), (dQ/dV), (dV/dQ) 변환과 Jacobian singularity를 유도한다.
155. 유한 측정 grid, differentiation, smoothing과 observation operator를 물리 상태식에서 분리한다.
156. peak area, height, width, shift와 asymmetry가 보존하는 양과 보존하지 않는 양을 유도한다.
157. 전극 단독 entropy coefficient와 full-cell reversible heat 조합 부호를 유도한다.
158. 단위·부호·좌표·zero-current·equilibrium limit 독립 검산을 수행한다.
159. 기초 장과 validator를 닫고 `PASS_P074_FOUNDATION` 여부를 판정한다.

## Phase 075 — 평형·상공존·상장

### Steps 160–173

160. ideal lattice-gas grand partition과 occupation을 유도한다.
161. Nernst/logistic potential, ICA kernel, area·height·FWHM을 유도한다.
162. degeneracy와 internal partition function의 center/entropy 영향을 유도한다.
163. regular-solution free energy와 chemical potential를 유도한다.
164. spinodal, binodal, common tangent와 Maxwell construction을 유도한다.
165. nonconvex free energy의 equilibrium convexification과 metastable branch를 구분한다.
166. coherency elasticity와 stress-free chemical spinodal의 적용 경계를 유도한다.
167. gradient energy를 molar-volume/site-density convention으로 차원 폐쇄한다.
168. Cahn–Hilliard chemical potential, flux, mobility와 mass conservation을 유도한다.
169. no-flux, periodic, natural boundary condition과 free-energy decay를 검증한다.
170. classical nucleation barrier, Gibbs–Thomson shift와 particle size 영향을 유도한다.
171. phase fraction, lever rule와 observable voltage/ICA mapping을 유도한다.
172. equilibrium peak width와 ensemble heterogeneity/observation width를 분리한다.
173. 독립 대수·차원·극한·경계 검산 후 `PASS_P075_EQUILIBRIUM_PHASE` 여부를 판정한다.

## Phase 076 — 비평형 Kinetics·Transport

### Steps 174–187

174. electrochemical affinity와 forward/reverse detailed balance를 정의한다.
175. Butler–Volmer와 generalized charge-transfer kinetics를 동일 부호계에서 유도한다.
176. exchange current의 composition, temperature와 active-area 의존성을 유도한다.
177. Arrhenius/Eyring rate와 mesoscopic phase-fraction mobility의 coarse-graining 경계를 유도한다.
178. solid diffusion과 electrolyte/porous-electrode polarization의 characteristic scale을 유도한다.
179. phase-boundary motion, nucleation delay와 local barrier를 분리한다.
180. signed time/capacity state evolution과 initial/final state contract를 유도한다.
181. rest, reversal, pulse와 nonmonotone protocol chronology를 보존하는 state equation을 정의한다.
182. finite-window remaining state와 tail capacity accounting을 유도한다.
183. nonisothermal local temperature/current path와 heat coupling을 정의한다.
184. (I\to0), frozen-state, fast-relaxation, small-particle와 transport-free limits를 검증한다.
185. low-temperature finite-current peak suppression, shift, broadening과 disappearance의 경쟁 scale을 유도한다.
186. 단일 exponential tail의 적용 범위와 식별 불가능한 mechanism을 명시한다.
187. protocol solver theory와 validator를 닫고 `PASS_P076_NONEQUILIBRIUM` 여부를 판정한다.

## Phase 077 — Graphite Material Closure

### Steps 188–199

188. graphite staging, gallery occupation과 phase sequence의 primary-source evidence를 확정한다.
189. 각 transition의 composition interval과 capacity contribution을 보존법칙에 연결한다.
190. ideal/regular-solution/phase-coexistence model의 transition별 적용 근거를 판정한다.
191. configurational, vibrational, electronic entropy의 반응 차이를 유도한다.
192. hysteresis의 equilibrium metastability, nucleation와 protocol memory 기여를 분리한다.
193. particle-size distribution, disorder와 electrode heterogeneity를 observation layer에 연결한다.
194. 저온 diffusion/charge-transfer/phase-boundary scale과 ICA 변화를 연결한다.
195. four-transition, seven-component와 기타 empirical decomposition의 권위를 분리한다.
196. graphite equilibrium·multi-temperature·multi-rate dataset mapping을 확정한다.
197. transition parameter의 prior, identifiability와 uncertainty 요구를 기록한다.
198. graphite chapter 전체를 독립 수식·문헌·데이터 검독한다.
199. `PASS_P077_GRAPHITE_CLOSURE` 또는 conditional 범위를 판정한다.

## Phase 078 — Doped High-voltage LCO Closure

### Steps 200–211

200. LCO composition, half-cell voltage와 phase-region 좌표를 확정한다.
201. order–disorder, metal–insulator transition와 two-phase coexistence 근거를 원문으로 판정한다.
202. configurational, electronic, vibrational와 reaction entropy를 유도한다.
203. Sommerfeld 항의 metallic-regime 가정과 DOS evidence tier를 제한한다.
204. composition-resolved entropy와 temperature-dependent voltage curvature를 유도한다.
205. high-voltage oxygen redox/loss, surface reconstruction와 structural transition을 분리한다.
206. dopant site, chemistry와 oxygen/structure/electronic 효과를 scalar interaction 하나로 축약하지 않고 분류한다.
207. graphite와 LCO reversible heat를 full-cell 부호계에서 조합한다.
208. per-peak interaction과 MSMR/reduced component mapping의 권위를 판정한다.
209. doped high-voltage dataset, structural evidence와 parameter prior를 연결한다.
210. LCO chapter 전체를 독립 수식·문헌·데이터 검독한다.
211. `PASS_P078_LCO_CLOSURE` 또는 conditional 범위를 판정한다.

## Phase 079 — Si/SiOx/Si–C Closure

### Steps 212–223

212. crystalline/amorphous Si lithiation sequence와 composition coordinate evidence를 확정한다.
213. SiOx irreversible conversion, active Si와 inactive matrix의 capacity accounting을 유도한다.
214. Si–C composite에서 active phases와 binder/conductive matrix의 역할을 분리한다.
215. regular-solution/Frumkin reduced model의 적용 범위와 실패 범위를 판정한다.
216. amorphization, phase separation와 hysteresis의 thermodynamic/kinetic 기여를 분리한다.
217. Larché–Cahn chemical potential와 stress coupling을 유도한다.
218. particle expansion, plasticity, fracture와 loss of active material의 관측 영향을 분리한다.
219. particle size와 rate/temperature dependence를 transport·mechanics scale에 연결한다.
220. empirical seven-component decomposition과 물리 phase identity를 분리한다.
221. Si/SiOx/Si–C dataset, equilibrium proxy와 mechanical evidence를 연결한다.
222. silicon chapter 전체를 독립 수식·문헌·데이터 검독한다.
223. `PASS_P079_SILICON_CLOSURE` 또는 conditional 범위를 판정한다.

## Phase 080 — Graphite+Si Blend Closure

### Steps 224–233

224. constituent mass, capacity와 lithiation fraction basis를 정의한다.
225. 공통 terminal voltage와 constituent internal potential의 coupled equilibrium을 유도한다.
226. total charge conservation과 constituent capacity partition을 유도한다.
227. equilibrium additivity가 성립하는 조건과 실패 조건을 판정한다.
228. finite-rate current sharing, impedance와 transport coupling을 유도한다.
229. constituent hysteresis와 initial state가 blend ICA/DVA에 미치는 영향을 유도한다.
230. normalized derivative와 absolute capacity denominator의 계약을 검산한다.
231. graphite/Si 단독 dataset과 blend dataset의 parameter transfer protocol을 정의한다.
232. blend chapter 전체를 독립 수식·문헌·데이터 검독한다.
233. `PASS_P080_BLEND_CLOSURE` 또는 conditional 범위를 판정한다.

## Phase 081 — 열·관측·식별성·불확도

### Steps 234–245

234. Helmholtz/Gibbs free energy, internal energy, entropy와 voltage temperature derivative 관계를 정리한다.
235. configurational, vibrational, electronic, elastic와 mixing entropy를 분리한다.
236. reversible, reaction, ohmic, charge-transfer와 mixing heat를 부호·control-volume별로 유도한다.
237. full-cell calorimetry와 electrode entropy coefficient의 관측 차이를 유도한다.
238. ICA/DVA differentiation, interpolation와 smoothing의 noise propagation을 유도한다.
239. resolution limit, heteroscedastic residual과 correlated error를 모델링한다.
240. structural identifiability를 Jacobian rank와 symmetry로 판정한다.
241. practical identifiability를 condition number, profile likelihood와 posterior/covariance로 판정한다.
242. BIC/AIC와 residual model 가정, bootstrap/held-out 판정의 적용 범위를 명시한다.
243. 구별 불가능한 parameter combination과 필요한 실험 설계를 도출한다.
244. uncertainty가 phase identity와 material conclusion에 전파되는 방식을 기록한다.
245. `PASS_P081_INFERENCE_UNCERTAINTY` 여부를 판정한다.

## Phase 082 — Canonical Equation Freeze

### Steps 246–255

246. Phase 074–081의 모든 Equation ID와 dependency를 전수 수집한다.
247. 각 식의 가정, 기호, 차원, 부호, 독립변수, domain와 source anchor를 대조한다.
248. 두 번째 독립 경로로 load-bearing 식을 재유도한다.
249. analytic limit와 dimensionless group을 독립 계산한다.
250. conservation, monotonicity, convexity, energy dissipation와 continuity를 검증한다.
251. material-specific parameter와 universal constant의 evidence tier를 검증한다.
252. 서로 경쟁하는 정당한 model은 대안군으로 남기고 arbitrary default를 금지한다.
253. `ADOPT`, `CORRECT`, `ALTERNATIVE`, `EMPIRICAL_ONLY`, `REJECT`, `UNVERIFIED`를 최종 부여한다.
254. canonical equation registry와 hash를 동결한다.
255. 독립 검토 gate를 통과한 경우에만 `PASS_P082_EQUATION_FREEZE`를 부여한다.

## Phase 083 — Theory–Implementation Contract

### Steps 256–267

256. canonical Equation ID마다 implementation consumer와 required input/output을 정의한다.
257. units, shapes, scalar/array, state, sign와 failure behavior를 정의한다.
258. equilibrium solver와 protocol state solver의 경계를 정의한다.
259. material parameter schema와 source/evidence tier를 정의한다.
260. observation operator와 raw physical state를 별도 interface로 정의한다.
261. empirical/reduced/production model family를 별도 namespace와 authority로 분리한다.
262. numerical method가 물리를 바꾸지 않는 tolerance·convergence contract를 정의한다.
263. cap/clip/fallback 사용 시 mathematical limit와 diagnostic visibility를 요구한다.
264. conservation, limit, derivative, sign, unit와 state continuity test matrix를 설계한다.
265. claim–equation–implementation–test trace matrix를 만든다.
266. implementation companion의 장 구조와 code-allowed 경계를 확정한다.
267. `PASS_P083_IMPLEMENTATION_CONTRACT` 여부를 판정한다.

## Phase 084 — Alpha Reference Implementation

### Steps 268–281

268. 실패하는 equation-registry schema test를 작성하고 실행한다.
269. 최소 schema loader를 구현해 test를 통과시킨다.
270. 실패하는 coordinate/unit/sign contract test를 작성하고 실행한다.
271. 최소 common coordinate layer를 구현해 test를 통과시킨다.
272. 실패하는 equilibrium/conservation/convexification test를 작성하고 실행한다.
273. 최소 equilibrium solver를 구현해 test를 통과시킨다.
274. 실패하는 protocol state/rest/reversal/current-limit test를 작성하고 실행한다.
275. 최소 nonequilibrium state solver를 구현해 test를 통과시킨다.
276. 실패하는 material graphite/LCO/Si/blend contract test를 작성하고 실행한다.
277. 최소 material adapters를 구현해 test를 통과시킨다.
278. 실패하는 entropy/heat/observation derivative test를 작성하고 실행한다.
279. 최소 thermal/observation layers를 구현해 test를 통과시킨다.
280. 전체 analytic-limit, conservation와 deterministic test suite를 실행한다.
281. 구현과 Step별 이력을 검독하고 `PASS_P084_ALPHA_REFERENCE` 여부를 판정한다.

## Phase 085 — 구조와 기본값 고정

### Steps 282–293

282. alpha에서 발견된 contract 결함을 우선순위와 evidence로 분류한다.
283. 범용 coordinate/state/material interface를 수정하고 regression을 실행한다.
284. model family와 material adapter 책임을 고정한다.
285. dimension-bearing input과 units representation을 고정한다.
286. state serialization과 reproducible initialization을 고정한다.
287. parameter provenance와 evidence-tier validation을 고정한다.
288. default는 데이터와 문헌이 식별한 값에만 허용하고 나머지는 explicit input으로 둔다.
289. public API와 error contract를 고정한다.
290. performance baseline을 측정하되 결과를 바꾸는 최적화는 금지한다.
291. 전체 regression, property와 clean-import test를 실행한다.
292. frozen structure와 equation traceability를 독립 검토한다.
293. `PASS_P085_STRUCTURE_FREEZE` 여부를 판정한다.

## Phase 086 — 실제 데이터 Calibration과 Validation

### Steps 294–307

294. raw data registry hash와 preprocessing recipe를 재검증한다.
295. smoothing·differentiation hyperparameter를 training data 밖 규칙으로 고정한다.
296. graphite equilibrium 조건을 먼저 calibration한다.
297. graphite multi-temperature/multi-rate held-out 조건을 검증한다.
298. LCO equilibrium·thermal·high-voltage 조건을 calibration한다.
299. doped LCO held-out chemistry 또는 조건을 검증한다.
300. Si/SiOx/Si–C equilibrium proxy와 mechanical/kinetic 조건을 calibration한다.
301. silicon held-out specimen 또는 protocol을 검증한다.
302. constituent 고정 후 graphite+Si blend를 calibration한다.
303. blend held-out composition/rate/temperature를 검증한다.
304. residual structure, heteroscedasticity와 conservation error를 진단한다.
305. bootstrap/profile/posterior 방식으로 parameter·prediction uncertainty를 산출한다.
306. empirical, reduced와 production model을 동일 외부 기준에서 비교한다.
307. 재료별 `PASS`, `CONDITIONAL`, `FAIL`을 분리해 `P086` gate를 판정한다.

## Phase 087 — 학술 원고 조립

### Steps 308–319

308. 단일 canonical LaTeX driver와 front matter를 작성한다.
309. 공통 통계열역학·전기화학·관측 기초 Part를 작성한다.
310. Graphite Part를 수식 유도와 source anchor로 작성한다.
311. Doped high-voltage LCO Part를 작성한다.
312. Si/SiOx/Si–C와 blend Part를 작성한다.
313. 열·식별성·실험 설계·불확도 Part를 작성한다.
314. 긴 유도, 부호·단위와 self-consistent closure appendix를 작성한다.
315. 본문·caption·footnote·label의 코드/작업이력 후보를 lexical scan한다.
316. 모든 section을 전문 의미 검독해 구현 서술을 companion으로 이동한다.
317. 별도 Implementation Companion을 작성한다.
318. claim–source–equation–figure/table cross-reference를 전수 검증한다.
319. `PASS_P087_MANUSCRIPT_ASSEMBLY` 여부를 판정한다.

## Phase 088 — Independent Red-team Review

### Steps 320–331

320. 전체 학술 본문을 section별로 독립 전문 검독한다.
321. 모든 load-bearing 식의 유도 누락과 논리 비약을 찾는다.
322. 단위, 부호, boundary, limit와 conservation을 재검산한다.
323. 모든 load-bearing citation을 원문 exact anchor와 재대조한다.
324. DOI·제목·저자·article number·correction 상태를 재검증한다.
325. material claim이 데이터와 evidence tier를 초과하는지 검독한다.
326. fitting component와 phase/material identity 혼동을 검독한다.
327. 메인 본문의 코드·구현·작업이력 금지 위반을 의미론적으로 검독한다.
328. implementation companion과 canonical equation의 conformance를 검독한다.
329. 모든 발견을 severity와 disposition으로 분류하고 수정한다.
330. 수정 후 동일 red-team checks를 다시 실행한다.
331. open load-bearing blocker가 없을 때만 `PASS_P088_SCIENTIFIC_REDTEAM`을 부여한다.

## Phase 089 — LaTeX·PDF Release QA

### Steps 332–341

332. XeLaTeX, kotex, D2Coding, fonts와 build dependency를 동결한다.
333. stale v1.0.25.1-derived PDF를 release input에서 격리한다.
334. canonical theory를 clean build directory에서 최소 3-pass build한다.
335. implementation companion을 clean build directory에서 최소 3-pass build한다.
336. undefined citation/reference, multiply-defined label, missing glyph와 build error를 0으로 만든다.
337. overfull/underfull과 수식·표·그림 layout warning을 위치별로 판정·수정한다.
338. 모든 PDF 페이지를 PNG로 렌더하고 contact sheet를 전수 검독한다.
339. 수식 밀집, 표, figure, appendix boundary와 페이지 전환을 원해상도로 검독한다.
340. PDF text extraction으로 코드 금지 본문과 citation/reference completeness를 재검증한다.
341. source/PDF hash 대응과 `PASS_P089_PDF_RELEASE_QA` 여부를 판정한다.

## Phase 090 — Clean-clone Release와 Handover

### Steps 342–351

342. 신규 빈 directory에서 release branch를 clone한다.
343. 문헌·데이터 provenance manifest와 필수 공개 입력을 검증한다.
344. environment bootstrap과 모든 automated tests를 실행한다.
345. reference implementation과 validation pipeline을 처음부터 재실행한다.
346. canonical theory와 companion PDF를 처음부터 재빌드한다.
347. 재생성 machine artifact와 release artifact의 hash/tolerance를 비교한다.
348. 보호 branch diff, 신규 branch commit chain과 Step별 작업이력 연결을 검증한다.
349. known limitation, conditional material claim과 unavailable data를 final limitations에 통합한다.
350. 최종 ledger, release manifest와 active handover를 작성한다.
351. 모든 gate를 재검증하고 `PASS_P090_RELEASE_COMPLETE`, `CONDITIONAL_RELEASE` 또는 `NO_RELEASE`를 판정한다.

## Test and Validation Plan

### 기록·Git gate

- 계획·result·machine artifact·ledger·handover의 경로 존재와 상호 링크를 검증한다.
- Step 번호가 1–351에서 phase 경계에 걸쳐 단조 증가하는지 검증한다.
- Step 종료 commit에 해당 Step result가 포함됐는지 확인한다.
- local HEAD와 remote branch tip 일치를 `git ls-remote`로 확인한다.
- protected branch tip과 tree가 변하지 않았는지 phase boundary마다 확인한다.

### 문헌 gate

- DOI syntax가 아니라 resolver와 publisher metadata를 검증한다.
- 원문 위치 없는 load-bearing claim을 FAIL 처리한다.
- 동일 DOI 충돌, title mismatch, correction/retraction을 검사한다.
- 원문 full text를 읽지 않은 경우 `UNVERIFIED`를 강제한다.

### 수식 gate

- 각 Equation ID의 assumption, unit, sign, independent variable와 domain을 검사한다.
- symbolic/analytic derivation과 independent numerical finite-difference를 교차한다.
- equilibrium, zero-current, fast/slow, dilute, high/low-temperature와 size limits를 검사한다.
- charge, capacity, mass와 free-energy dissipation을 검사한다.

### 코드·구현 gate

- 기능 또는 bugfix는 TDD red–green–refactor 순서로 수행한다.
- scalar/array, units, state, sign, error, initialization와 serialization을 검사한다.
- equation registry와 implementation consumer가 완전 연결되는지 검사한다.
- fallback이나 stabilization이 결과의 물리 의미를 바꾸면 FAIL 처리한다.

### 데이터·피팅 gate

- raw hash와 preprocessing hash를 분리한다.
- training/validation/held-out 조건을 분리한다.
- residual, uncertainty, identifiability와 conservation을 함께 보고한다.
- synthetic data는 algebra/implementation test에만 사용하고 external validity에는 사용하지 않는다.

### LaTeX·PDF gate

- build exit 0, undefined citation/reference 0, missing glyph 0을 요구한다.
- 모든 페이지 render와 육안 검독 coverage를 기록한다.
- 메인 본문의 코드 언급은 lexical scan과 전문 의미 검독을 모두 통과해야 한다.
- PDF와 TeX source hash 대응을 release manifest에 기록한다.

## Autonomous Decision Policy

- 근거가 충분하고 선택이 유일하면 계속 진행한다.
- 복수 모델이 과학적으로 가능하면 대안군을 유지하고 임의 정본화를 하지 않는다.
- 원문 미확보는 `UNVERIFIED`, 데이터 미확보는 `CONDITIONAL`로 기록하고 독립 가능한 다른 작업을 계속한다.
- 서지·수식·데이터 충돌은 숨기지 않고 `CONFLICTING`으로 보존한다.
- 사용자가 없는 동안도 Step별 result, commit, push와 remote verification을 계속한다.

## Hard Stops

- protected branch의 예상치 못한 변경.
- active remote branch가 local 예상과 다른 방향으로 이동한 경우.
- 동일 원인의 push가 세 차례 연속 실패한 경우.
- 비공개·유료 원문 또는 자격 증명이 전체 다음 단계의 필수 입력이 된 경우.
- 상충하는 사용자 지시를 대안 병기로도 보존할 수 없는 경우.
- 근거 없이 material model 또는 parameter를 정본으로 골라야만 진행 가능한 경우.
- validator 실패가 과학 결과 변경인지 환경 부채인지 세 번의 독립 조사 후에도 분리되지 않는 경우.

## Assumptions

- Phase 055–069의 기존 산출물은 과거 완료를 자동 승인하는 권위가 아니라 재실행·대조할 입력이다.
- Phase 069가 `NO_GO`이면 Phase 070–090을 실행하지 않고 blocker repair addendum을 먼저 작성한다.
- Phase 069가 `CONDITIONAL_GO`이면 조건을 각 하위 Phase gate의 필수 입력으로 전달한다.
- 공개 데이터와 원문 접근 범위에 따라 일부 material conclusion은 최종적으로도 conditional일 수 있다.
- review-paper급이라는 표현은 citation 수가 아니라 load-bearing claim의 원문 깊이, 적용 범위와 충돌 검토 수준을 뜻한다.


## Implementation Interfaces

- 각 phase detailed plan은 Summary / Current Ground Truth / Phase Range / Non-goals /
  Implementation Changes / numbered Steps / Interfaces / Test Plan / Assumptions / Correction History를 유지한다.
- 결과서는 Step Range, Inputs, Files Created/Updated, Read Coverage(파일·행/페이지·fresh/reused),
  Execution Evidence(명령·runtime·exit·stdout/stderr), Validation, Gate, Confirmed Non-Changes,
  Open Issues/Decision Queue, Next를 갖는다.
- ledger row는 Phase, Plan Steps, Status, Canonical Report, Machine Artifact, Gate Result, Next Step을 갖는다.
- Equation record는 정의/중간 유도/가정/차원/부호/독립변수/domain/극한/보존/source anchor를 갖는다.
- Source record는 실제 DOI·publisher metadata와 원문 support를 별도 필드로 둔다.
- Material record는 specimen/protocol/data provenance/training/held-out/불확도/조건부 한계를 갖는다.
- 검증기는 새 임의 표준을 만드는 대신 위 contract와 실제 과학 오류를 검출한다.

## Plan Validation and Assumptions

- Step 94–351의 모든 integer가 정확히 한 numbered action으로 존재하고 단조 증가함을 검사한다.
- Step 108–351 원문 action/기존 Gate가 이전 master와 byte-text 기준으로 일치하는지 검사한다.
- docs 경계/3종 복구/누적 번호/스텝별 결과 포함 push/본문 코드 금지/문헌 진위 규칙을 직접 대조한다.
- 계획 activation은 과학 Step 완료가 아니다. 현재 content 미완료를 COMPLETE로 바꾸지 않는다.
- user의 이번 지시는 계획 개정과 계속 실행을 승인한다. 동일 실행 승인 질문을 반복하지 않는다.
- 전체 문헌·실험 자료 접근을 보장할 수 없다. 부족한 근거의 영향과 범위를 구체적으로 기록한다.
- 전체 완료 시간이나 완료율을 commit 수, 모델 이름 또는 effort 이름만으로 계산하지 않는다.

## Correction History and Supersession

- 2026-09-07: 사용자 지정 Sol→Astra 책임 전환 checkpoint aedfd408281b97699ba7f75884e7108965ecf547을 기준으로 신규 작성.
- 기존 master를 덮어쓰지 않는다. 본 계획은 현재 상태·운영 절차·docs 경계·원고 축적 시점을 갱신한다.
- 기존 Phase 068 상세계획의 매 unit 대형 controls 전문 재독, exact-seven/eight 경로,
  duplicated bespoke validator와 고정 parent 규칙의 후속 변경은 새 continuation detailed plan에 한정한다.
- 기존 91–93 증거/결과는 역사적 계약을 유지하며 새 기준으로 소급 PASS/FAIL 재분류하지 않는다.
- 94–351 범위/번호, 과학 게이트, 문헌/재료 권위 경계, protected/Claude 보존은 약화하지 않는다.
- harness-core와 프로젝트 운영지침의 기록·복구 구조를 적용했다.
  글로벌 runtime/hooks/watchers/memory/config/스킬 파일은 수정하지 않는다.
