# v1.0.25.2 계보 재감사 및 학술 정본 완결 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Steps use cumulative numbering across every phase and must never restart at 1.

**Goal:** 기존 v1.0.10–v1.0.25.2 계보 감사를 정확한 중단 지점에서 완결한 뒤, 검증된 1차 문헌·교재·공개 데이터와 완전한 수식 유도에 근거하는 대학원 교과서형·review-paper급 학술 정본, 별도 구현 companion, 재현 가능한 계산·검증 패키지와 최종 PDF를 만든다.

**Architecture:** Phase 059–069에서는 기존 감사 정본을 수정 없이 승계해 Claude/Codex 계보의 채택·정정·기각 근거를 닫는다. Phase 069가 `GO` 또는 `CONDITIONAL_GO`일 때만 Phase 070–090을 활성화하며, 학술 본문과 구현 companion을 물리적으로 분리하고 claim–source–equation–data–implementation–test 증거 사슬로 결합한다.

**Tech Stack:** Git/GitHub, Markdown/JSON evidence ledgers, Python/NumPy/SciPy 기반 독립 검산과 시험, XeLaTeX, Poppler 기반 PDF 전 페이지 렌더 검수, DOI resolver·출판사·원문 기반 문헌 검증.

---

정본일: 2026-08-25

활성 신규 브랜치: `codex/anode-fit-v1025_2-canonical-completion`

신규 브랜치 기준 commit: `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`

상위 감사 기준 commit: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`

승계 계획: `Codex/plans/2026-07-28-v1010-v1025_2-full-lineage-intent-reaudit-master-plan.md`

승계 실행 위치: Phase 059 Step 38.5

전체 계획 범위: Phase 055–090, cumulative Steps 1–351

이 문건의 신규 예약 범위: Phase 070–090, cumulative Steps 108–351

## Summary

이 계획은 기존 Claude 또는 Codex 브랜치를 직접 수정하거나, 최신이라는 파일명만으로 과학 정본을 선택하는 계획이 아니다. 현재 가장 진전된 Codex 감사 브랜치의 clean HEAD에서 신규 브랜치를 분기하고, 기존 Phase 059 Step 38.5부터 Phase 069 Step 107까지 먼저 닫는다.

Phase 069 전에는 최종 model family, 재료별 기본 parameter, 최종 목차, 최종 구현 구조를 확정하지 않는다. Phase 069의 canonical audit가 제공하는 `ADOPT`, `CORRECT`, `REWRITE`, `REFERENCE_ONLY`, `REJECT`, `UNVERIFIED` 판정을 Phase 070의 유일한 설계 입력으로 사용한다.

최종 산출물은 다음 세 층으로 분리한다.

1. 코드·함수·파일·API·작업 이력을 언급하지 않는 단일 canonical theory monograph와 PDF.
2. 구현 계약, 식–구현 mapping, API, 피팅 절차와 시험을 담는 별도 Implementation Companion.
3. 검산 코드, reference implementation, 시험, 데이터 provenance와 재현 절차를 담는 machine package.

## Current Ground Truth

### Git과 브랜치

- 보호 대상 기존 Codex branch: `codex/lib-physics-endgame-v1025_2`.
- 보호 branch tip: `fc5f1776cfe1de5cb5d8336a74b05f35e3f95d71`.
- 최신 Claude branch: `claude/version-1026-regsol-review-kl88j7`.
- 최신 Claude branch tip: `e3e1a634f34b711aa4803fd190fe9120f1755f13`.
- 최신 Claude 학술 작업 directory: `Claude/docs/v1.0.25.2/`.
- `v1.0.26A-regsol`, `v1.0.26B-gallery`는 정본 LaTeX release가 아니라 피팅 비교 실험이다.
- `main` tip `4069cb36a8a52b1b88c29d68aa54dcbe915b1618`은 이번 과학 기준선이 아니다.
- 기존 branch, `main`, `Claude/` 원본은 수정하지 않는다.

### 현재 감사 상태

- Phase 055 Steps 1–8: `PASS_P055_SOURCE_FREEZE`.
- Phase 056 Steps 9–17: `PASS_P056_COMPLETE_MANIFEST`.
- Phase 057 Steps 18–25: `PASS_P057_INTENT_RECOVERY`.
- Phase 058 Steps 26–32: `PASS_P058_LINEAGE_A`.
- Phase 059 Steps 33.1–38.4: 실행 완료, Phase 자체는 `IN_PROGRESS`.
- 정확한 다음 실행 단위: Phase 059 Step 38.5.
- Step 38.5 뒤 Step 39.1–39.6으로 Phase 059를 닫는다.
- Phase 060은 Step 40부터 시작하고 Phase 069는 Step 107에서 끝난다.
- Phase 070은 Phase 069 launch gate 통과 후 Step 108부터 시작한다.

### 현재 확인된 중대 부채

- v1.0.25.2 directory의 PDF 3개는 v1.0.25.1 PDF와 동일 Git blob이므로 v1.0.25.2 변경을 반영한 build evidence가 아니다.
- current three-document LaTeX 구조는 장간 external reference가 순환한다.
- Ch1의 code-map appendix는 루트에서 `\appendix` 경계가 명확하지 않다.
- 루트 연결 본문 section의 기계 후보 검색에서 코드·구현 언급 후보가 다수 확인됐으나 아직 각 section의 의미론적 전문 판정은 완료되지 않았다.
- 수동 `thebibliography`는 cite-key 완결성만 맞고 DOI resolver 및 원문 지원 범위 검증이 없다.
- 동일 DOI가 서로 다른 제목에 연결된 충돌 후보, abstract-tier 항목, 내부 검증 자료가 학술 참고문헌에 섞인 사례가 있다.
- current kinetics에는 3,600 단위계, frozen affinity, chronology, direct-lag zero-current, finite-window state blocker가 있다.
- current temperature-width와 Einstein capability에는 parameter contract, positivity, persistent regression, material identifiability blocker가 있다.
- graphite/Si/blend/doped high-voltage LCO의 다온도·다율속·독립 specimen 기반 외부 검증이 없다.

### Baseline Validator Portability Debt

Debt ID: `KNOWN_VALIDATOR_PORTABILITY_DEBT_001`

`validate_phase059_v1018_2_einstein_fullpath.py`는 입력 누락을 보완한 Windows worktree에서 과학·수치 check를 통과하지만 deterministic rerun은 플랫폼 의존 값 때문에 실패한다.

- source hash가 Git blob bytes가 아니라 checkout bytes를 사용해 `core.autocrlf=true`에서 LF/CRLF에 따라 달라진다.
- relative path가 `Path`의 OS separator를 그대로 JSON에 기록한다.
- 기존 결과의 source hash는 Git blob LF bytes와 정확히 일치한다.
- 신규 validator는 Git blob hash와 POSIX path를 canonical representation으로 사용해야 한다.
- 이 부채 때문에 과거 canonical JSON을 Windows 표현으로 덮어쓰지 않는다.

## Phase Range

### 승계 범위

| Phase | Steps | 상태 | 목적 |
|---|---:|---|---|
| 055 | 1–8 | PASS | 기준선·보존 경계 |
| 056 | 9–17 | PASS | 전체 manifest·중복 지도 |
| 057 | 18–25 | PASS | 사용자 의도·결정 계보 |
| 058 | 26–32 | PASS | v1.0.10–v1.0.13 재감사 |
| 059 | 33–39 | IN_PROGRESS | v1.0.14–v1.0.18.2 재감사 |
| 060 | 40–45 | PENDING | v1.0.19 재감사 |
| 061 | 46–51 | PENDING | v1.0.20 재감사 |
| 062 | 52–57 | PENDING | v1.0.21 재감사 |
| 063 | 58–63 | PENDING | v1.0.22 재감사 |
| 064 | 64–69 | PENDING | v1.0.23 재감사 |
| 065 | 70–75 | PENDING | v1.0.24–v1.0.24.1 재감사 |
| 066 | 76–81 | PENDING | v1.0.25–v1.0.25.2 재감사 |
| 067 | 82–90 | PENDING | 코드·시험·피팅 계보 교차감사 |
| 068 | 91–98 | PENDING | Claude/Codex fork 재판정 |
| 069 | 99–107 | PENDING | canonical audit와 launch gate |

### 조건부 신규 범위

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

- Phase 069 전 새 정본 이론식, 최종 TOC, 최종 model family 또는 material default를 확정하지 않는다.
- 기존 Claude/Codex branch에 commit, merge, rebase 또는 overwrite하지 않는다.
- Claude source를 현재 신규 branch에서도 직접 수정하지 않는다. 채택 source는 Phase 069 이후 Codex-controlled canonical tree로 복제·재작성한다.
- v1.0.26A/B의 BIC 우세를 물리적 phase identity 또는 정본 모델 권위로 승격하지 않는다.
- synthetic fit, golden roundtrip, internal self-consistency를 외부 재료 타당성으로 승격하지 않는다.
- 문헌 metadata 또는 DOI 존재만으로 본문 claim support를 확정하지 않는다.
- 원문을 읽지 못한 문헌의 내용을 추정하지 않는다.
- 데이터가 없을 때 합성 데이터를 실제 validation으로 대체하지 않는다.
- fitting component를 phase, gallery, material identity로 자동 해석하지 않는다.
- 과학적 근거 없는 cap, clip, clamp, smoothing, threshold, fallback을 물리 항으로 승격하지 않는다.
- 메인 학술 본문, caption, footnote, visible heading에는 코드, 함수, 파일, class, key, API, test, commit, phase, step 또는 작업 이력을 언급하지 않는다.
- 성능 최적화는 방정식·보존법칙·검증 기준선이 동결되기 전에 시작하지 않는다.

## Implementation Changes and Canonical Files

### 계획·운영 파일

- Create: `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`
- Create: `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.json`
- Create: `Codex/plans/2026-08-25-phase059-resume-closure-detailed-plan.md`
- Create per phase: `Codex/plans/YYYY-MM-DD-phaseNNN-<topic>-detailed-plan.md`

### 결과·복구 파일

- Create: `Codex/results/PHASE_059_090_CANONICAL_COMPLETION_EXECUTION_LEDGER.md`
- Create: `Codex/results/ACTIVE_HANDOVER_CANONICAL_COMPLETION.md`
- Create: `Codex/results/PLAN_ACTIVATION_CANONICAL_COMPLETION_RESULT.md`
- Create per executed unit: `Codex/results/PHASE_NNN_STEP_NNN[_SUBSTEP]_<TOPIC>_RESULT.md`
- Create machine evidence beside each human-readable result when calculations, coverage or gate state exist.

### 최종 산출물 후보

Phase 069 이후 Phase 073에서 실제 경로를 고정한다. 현재 책임 경계는 다음과 같다.

- canonical theory source: 단일 LaTeX root와 재료·이론별 section tree.
- implementation companion source: code mapping, APIs, fitting, tests, reproducibility 전용 별도 root.
- evidence ledger: claim, source, equation, data, implementation, test linkage.
- reference implementation: 이론식의 최소 명시 구현과 독립 limit/conservation tests.
- final PDFs: canonical theory PDF와 implementation companion PDF를 구분한다.

## Execution Protocol

각 실제 Step 또는 substep 종료 시 아래 순서를 강제한다.

1. 마스터플랜 전문 또는 현재 작업에 필요한 전체 section을 재확인한다.
2. 활성 Phase detailed plan을 처음부터 끝까지 확인한다.
3. 직전 Step result와 대응 machine artifact를 확인한다.
4. `git status --short --branch`, HEAD, 원격 tip을 확인한다.
5. 해당 Step의 입력을 전문 검독하고 read coverage를 기록한다.
6. 계획 범위 안의 작업만 수행한다.
7. human-readable Step result를 `Codex/results`에 작성한다.
8. machine evidence와 validator를 작성·실행한다.
9. 실행 ledger와 active handover를 갱신한다.
10. 변경 파일·이유·검증·미확인 사항을 대조한다.
11. 해당 Step의 작업이력과 산출물을 함께 하나의 atomic commit으로 만든다.
12. 신규 branch에 push한다.
13. `git ls-remote`와 local HEAD를 비교해 원격 commit 일치를 확인한다.

push가 실패하면 동일 원인을 확인하며 최대 세 번까지만 재시도한다. 세 번째에도 원격 복구점이 만들어지지 않으면 실패 원인과 local HEAD를 handover에 기록하고 hard stop한다.

## Compaction and Recovery Protocol

컨텍스트 압축, 모델 교체, 재개 또는 handover 뒤에는 다음 순서를 따른다.

1. `Codex/plans/2026-08-25-v1025_2-canonical-completion-master-plan.md`를 전문 재독한다.
2. 현재 Phase detailed plan을 전문 재독한다.
3. 직전 Step result를 전문 재독한다.
4. execution ledger의 마지막 완료 Step과 첫 미완료 Step을 확인한다.
5. active handover의 canonical chain과 exact next step을 확인한다.
6. local HEAD, branch, clean/dirty state와 remote tip을 확인한다.
7. 직전 validator를 재실행하거나 플랫폼 부채가 있으면 정규화된 독립 검증으로 대체하고 이유를 기록한다.
8. 세 기록과 Git 상태가 일치할 때만 다음 Step으로 진입한다.

대화 요약, 이전 에이전트 자기보고 또는 기억은 완료 근거로 사용하지 않는다.

## Phase 059–069 — Existing Reaudit Completion

Phase 059–069의 Steps 33–107, 산출물, gate와 stop condition은 승계 master plan과 각 Phase detailed plan을 정본으로 사용한다. 이 신규 master plan은 번호와 과학적 판정을 다시 쓰지 않는다.

Phase 059 재개에서는 신규 detailed addendum이 기존 계획과 실제 Steps 33.1–38.4를 연결하며, Step 38.5와 Step 39.1–39.6의 파일명·검증·commit boundary를 구체화한다.

Phase 060–069 진입 전에는 각각 신규 branch용 detailed plan을 `Codex/plans`에 먼저 저장하고, 바로 앞 Phase result와 gate를 입력으로 명시한다.

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

## Correction History

- 2026-08-25: 사용자 승인에 따라 기존 branch를 보존하는 신규 branch와 Step별 작업이력–commit–push–원격 확인 규칙을 정본화했다.
- 2026-08-25: 최신 Claude branch 이름과 실제 최신 학술 directory v1.0.25.2를 분리했다.
- 2026-08-25: v1.0.25.2 PDF가 v1.0.25.1과 동일 blob인 stale artifact임을 release gate에 반영했다.
- 2026-08-25: Windows sparse worktree 기준 validator 재현에서 발견한 LF/CRLF hash와 path separator portability debt를 기록했다.
- 2026-08-25: Phase 059 Step 38.5를 정확한 재개 위치로, Phase 070 Step 108을 post-audit 신규 작업 시작점으로 고정했다.
