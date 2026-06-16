# Chapter 1 v5 (수식-구동 / equation-driven) Plan

## Summary

**목표.** `graphite_ica_ch1_Opus_v4.tex` 의 **§1.1 ~ §1.17** 내용을, 산문(글귀)을 최소화하고 **논리 전개의 절대 다수를 수식 사슬(equation chain)이 운반**하도록 재표현한 신규 버전 `graphite_ica_ch1_Opus_v5.tex` 를 만든다. 독자가 **수식만 따라가도 전개를 이해**할 수 있어야 한다.

**왜.** v4 는 교과서 문체(완결 문장·동기 부여 산문·절간 다리)로 작성된 버전이다. 사용자는 이번에 **다른 장르** — 가정에 대한 산문 설명을 배제하고 물리·수식으로만 논리를 잇는 "수식 연속" 버전 — 을 요청했다. 이는 v4 의 엄밀성을 *낮추는* 것이 아니라, **산문이 담당하던 논리적 연결을 명시적 수식(중간 단계 포함)으로 승격**시켜 산문 없이도 사슬이 닫히게 만드는 작업이다.

**범위.** Chapter 1 의 §1.1(기호와 규약)~§1.17(코드)만. **§1.18(적층 준안정, sec:stacking)은 배제** — v4 의 미완성/확장 절. v5 는 v4 와 별개의 신규 파일이며 v4 는 불가침(원본 보존).

**운용.** master(본 세션) 중앙관리 + Agent 도구로 **최대 5 동시 서브세션**(초안·검수 단계). Workflow 도구 미사용(글로벌 헌법 — ultracode 'use Workflow' 기본값을 사용자 상시 지시가 상회). v5.tex 는 공유 가변상태이므로 **파일 쓰기는 master 직렬 통합**, 서브는 독립 드래프트 텍스트 생산 또는 검수만 수행.

## Current Ground Truth

**확인된 사실 (확정):**

- 원천 파일 = `Claude/docs/graphite_ica_ch1_Opus_v4.tex` (2912줄, XeLaTeX + kotex). 헤더: "Chapter 1 (v4 by Opus: Fable_v3 + [확장] 적층 준안정)".
- 절 번호 체계: `\renewcommand{\thesection}{1.\arabic{section}}` → `\section{}` 이 §1.1, §1.2 … 로 표시. 본문은 `\section`(절) + `\subsection`(소절) 구조.
- **§1.1 ~ §1.18 절 권위 목록** (label / v4 줄위치):

  | 절 | label | 제목 | v4 시작줄 |
  |---|---|---|---|
  | §1.1 | sec:notation | 기호와 규약 | 261 |
  | §1.2 | sec:rate | 근본식 — 활성화 장벽과 반응 속도 | 335 |
  | §1.3 | sec:thermo | (G, μ — 자유에너지의 언어) | 452 |
  | §1.4 | sec:fwdrev | (정·역 속도 → 평형 유도) | 665 |
  | §1.5 | sec:regsol | (정규용액 Ω, 상분리·spinodal) | 826 |
  | §1.6 | sec:charge | (전하 보존 → 내부 전위 V_n, 관측축) | 1049 |
  | §1.7 | sec:eqpeak | (평형 peak, logistic 미분) | 1189 |
  | §1.8 | sec:lag | (동역학 지연 → 꼬리) | 1267 |
  | §1.9 | sec:potbranch | (전위 가지 — 유효 장벽) | 1443 |
  | §1.10 | sec:tempbranch | (온도 가지 — Arrhenius) | 1526 |
  | §1.11 | sec:synth | (종합 — 닫힌식) | 1685 |
  | §1.12 | sec:overlap | (peak 겹침 — 합산) | 1834 |
  | §1.13 | sec:hys | (히스테리시스) | 1916 |
  | §1.14 | sec:hyspol | (분기 분극·중심) | 2077 |
  | §1.15 | sec:master | (통합 피팅식 + 알고리즘) | 2223 |
  | §1.16 | sec:falsify | (반증 조건) | 2523 |
  | §1.17 | sec:code | (Python 코드 = 식의 직역) | 2592 |
  | §1.18 | sec:stacking | [확장] 적층 준안정 — **배제** | 2744 |

- "17절까지 / 18절 배제" = §1.1~§1.17 포함(서론 lines 83–129 포함), §1.18(2744–2912) 제외. git log 의 "sec 1.1-1.17 byte-identical to v3", "§1.18 placed AFTER code" 와 일치.
- 빌드 툴체인: `xelatex`(MiKTeX, PATH 확인), `latexmk` 존재. v4 PDF `graphite_ica_ch1_Opus_v4.pdf`(6-13 빌드) 존재 → 빌드 gate 실행 가능.
- 프로젝트 상시 지시: 버전 변경 시 자동 commit+push(내 작업물만 명시 스테이징, attribution 없음). 현재 브랜치 `rb-rebuild-2026-05-30`.

**기존 결정 / 직전 gate:**

- v4 는 §1.18 redo 까지 N-round 검수 수렴(c06fb81: "Convergence reached, gates 0/0/0") 완료. v4 본문은 검수 통과된 신뢰 원천.
- 최신 인계 = `HANDOVER_2026-06-11_ch1-v2-blank-rewrite.md`(v4 작업은 그 이후 commit 으로 진행, 별도 handover 부재).

**미확인 사항 (미검독 표시):**

- §1.2~§1.17 본문 전문(equation chain 의 세부) — 초안 단계에서 각 담당 서브가 head→tail 정독으로 확정. **현 시점 master 는 서론 + §1.1 + 절 지도까지만 정독, 절별 식 세부는 미검독.**
- v4 의 figure(TikZ) 목록·캡션 — 통합 단계에서 확정.

## Phase Range

| Phase | 이름 | Steps | 주체 |
|---|---|---|---|
| 1.0 | 설계 — 스타일 스펙·라벨 규약·절 변환 brief | 1–4 | master 직접 + 검수 1 |
| 1.1 | 병렬 초안 — 5 서브 독립 드래프트(텍스트) | 5–9 | 작업 sub ×5 (병렬) |
| 1.2 | 직렬 통합 — master 가 v5.tex 단위별 통합·빌드 | 10–16 | master 직렬 |
| 1.3 | N회 가변-청크 검수 (≥10R, 수렴 2×0) | 17–26+ | 검수 sub ×최대5 (병렬/R) + master 수정 |
| 1.4 | 최종 검수·결과문건·commit+push | 27–29 | master 직접 |

Step 번호는 phase 넘어가도 단조 누적. Phase 1.3 은 수렴 미달 시 step 을 늘려 라운드 추가([[feedback_step_granularity_flexibility]]).

## Non-goals

- **§1.18(적층 준안정) 변환 X** — 이번 범위 밖. v5 는 §1.17 에서 끝.
- **새 물리·새 유도·새 결론 추가 X.** v5 는 v4 §1.1~§1.17 의 **충실한 재표현**(equation chain 보존). 단, v4 가 *산문으로* 설명한 논리 단계는 v5 에서 *명시적 중간 수식*으로 승격 가능(누락 방지 목적, 새 내용 아님).
- **v4 파일 수정·덮어쓰기 X.** v5 는 신규 파일. v4(.tex/.pdf) 불가침.
- **Codex/ 산출물 read/write X** (프로젝트 경계). 비교 무결성 보존.
- **Chapter 2~5 손대지 않음.**
- 사용자 GO 전 서브세션 spawn·v5.tex 생성 X (기획 단계).

## Implementation Changes

생성/수정 산출물:

- **신규** `Claude/docs/graphite_ica_ch1_Opus_v5.tex` — v5 본체.
- **신규** `Claude/docs/graphite_ica_ch1_Opus_v5.pdf` — 빌드 산출물.
- **신규** `Claude/results/PHASE_V5_RESULT.md` — Phase 결과(11항목, [[feedback_phase_execution_loop]]).
- **신규** `Claude/results/PHASE_V5_EXECUTION_LEDGER.md` — 12-col ledger(단위·라운드 추이).
- **신규(작업 중)** `.session/v5/` — 서브 brief·드래프트·검수 로그(LOG_MANIFEST 포함).
- **수정 없음**: v4 및 기존 결과 문건 전부.
- commit 동반: `Codex/` 디렉토리(수정 X + 커밋 O, [[feedback_multi_agent_project_structure]]).

## Phase 1.0 — 설계 (스타일 스펙·라벨 규약·절 변환 brief)

- **Step 1** — master: v4 §1.1~§1.17 전체 구조·equation chain 의존 그래프를 정독 확정(절별 입력식→출력식, figure 목록, eq label 목록). 산출: 절별 "변환 brief" 초안.
- **Step 2** — master: **v5 스타일 스펙** 확정(아래 Implementation Interfaces §A). 유지/삭제 경계, 커넥터 화이트리스트, 라벨 규약, 가정 표기법.
- **Step 3** — 검수 sub(1): 스타일 스펙 + 절 변환 brief 가 (a) 누락 위험(어떤 절의 산문이 사실은 유도 단계라 수식 승격 필요한지) (b) 라벨 충돌 가능성 (c) "수식만으로 follow" 달성 가능성 을 점검. refute mandate.
- **Step 4** — master: 검수 반영, brief 확정. **Gate 1.0**: 절별 brief 17개 모두 [입력식 번호 / 출력식 번호 / 보존할 v4 eq label / 삭제할 산문 유형 / 승격할 산문→수식 단계]를 명시 — 확인 가능 항목으로 채워졌는가(빈칸 0).

## Phase 1.1 — 병렬 초안 (5 서브 독립 드래프트)

5 작업 서브가 **독립 그룹**을 동시 드래프트. **파일 쓰기 X — 각자 v5 LaTeX 텍스트를 return.** (독립 드래프트라 공유상태 충돌 없음 → 병렬 정당.)

- **Step 5** — 작업 sub A: §1.1 + §1.2 + §1.3 (v4 261–664) 드래프트.
- **Step 6** — 작업 sub B: §1.4 + §1.5 (665–1048) 드래프트.
- **Step 7** — 작업 sub C: §1.6 + §1.7 + §1.8 (1049–1442) 드래프트.
- **Step 8** — 작업 sub D: §1.9 + §1.10 + §1.11 + §1.12 (1443–1915) 드래프트.
- **Step 9** — 작업 sub E: §1.13 + §1.14 + §1.15 + §1.16 + §1.17 (1916–2743) 드래프트.

각 sub 는 (i) 담당 v4 절 head→tail 정독 (ii) 스타일 스펙·라벨 규약 적용 (iii) v4 eq label 보존 + 신규 중간식 라벨 규칙 준수 (iv) §1.1 심볼표를 공유 참조로 받음. **Gate 1.1**: 각 드래프트가 [담당 절 전 식 보존 확인 / 산문→수식 승격 목록 / orphan(앞 도입·뒤 사용) 자가점검]을 동반하는가.

## Phase 1.2 — 직렬 통합 (master, v5.tex 단위별)

master 가 5 드래프트를 **단위(절)별 직렬 통합**(§2 단위 루프). 통째 배치 금지.

- **Step 10** — 프리앰블 + 서론(수식-구동 축약) + §1.1 통합 → v5.tex 생성 → 빌드.
- **Step 11** — §1.2~§1.3 통합 → 앞 단위 정합(eq label cross-ref) → 빌드.
- **Step 12** — §1.4~§1.5 통합 → 정합 → 빌드.
- **Step 13** — §1.6~§1.8 통합 → 정합 → 빌드.
- **Step 14** — §1.9~§1.12 통합 → 정합 → 빌드.
- **Step 15** — §1.13~§1.17 통합 → 정합 → 빌드.
- **Step 16** — 전체 2-pass 빌드 + cross-ref 해소 확인. **Gate 1.2**: `xelatex` 2-pass 후 (a) undefined reference 0 (b) 모든 `\eqref` 해소 (c) overfull hbox > 임계 0(또는 사유 기록) (d) §1.1 심볼표 ↔ 본문 사용 기호 1:1.

## Phase 1.3 — N회 가변-청크 검수 (≥10R, 수렴 2×0)

[[feedback_multiagent_review_chunking]] + 방법론 §3. **매 라운드 청크 스킴 + 렌즈 전환.** 검수 sub 병렬(refute + 가장 약한 1곳 필수 지목 + 빈 통과 금지) → master 삼각검증·직접 수정 → 빌드 → ledger 라운드 행 → commit+push.

라운드 로테이션 설계(예시, 수렴까지 연장):

- **R1 (Step 17)** — 청크=절별(17창→5서브 분담), 렌즈=**물리·수식 적대 검산**(재유도·극한·차원). v4 대비 식 보존·승격 정합.
- **R2 (Step 18)** — 청크=식·라벨 단위, 렌즈=**G-follow**(앞 식만으로 다음 식 따라가지나 / 산문 없이 끊기는 곳).
- **R3 (Step 19)** — 청크=전체 통독(2서브 분담), 렌즈=**흐름·완결성(orphan 0)**.
- **R4 (Step 20)** — 청크=절별, 렌즈=**G-usable**(절 끝 닫힌식으로 실데이터 대입·피팅 가능한가, §1.15/§1.17).
- **R5 (Step 21)** — 청크=라인 단위, 렌즈=**시각(PDF 렌더 판독, pdftoppm)** + 식 줄바꿈·overfull.
- **R6 (Step 22)** — 청크=도메인 그룹(열역학/속도/관측/꼬리/히스), 렌즈=**기호·부호·정의역 일관성**.
- **R7 (Step 23)** — 청크=v4↔v5 절별 대조, 렌즈=**내용 보존 감사**(v4 식·논리가 v5 에서 누락 0).
- **R8 (Step 24)** — 청크=절별, 렌즈=**직전 라운드 수정이 들인 새 결함**.
- **R9 (Step 25)** — 청크=전체 통독, 렌즈=**완결성 재확인 + 미수렴 잔결함**.
- **R10+ (Step 26+)** — 수렴(연속 2R 확정결함 0)까지 청크·렌즈 새로 배정해 연장.

**Gate 1.3**: 연속 2 라운드 확정 결함 0 + 매 라운드 전수 정독(coverage missing=0) + 각 라운드 빌드 GREEN.

## Phase 1.4 — 최종 검수·결과·commit

- **Step 27** — master 최종 통합 검수: 스타일 목표("수식만 따라가도 이해") 달성 자가평가 + Decisions 반영 확인 + 빌드 최종.
- **Step 28** — `PHASE_V5_RESULT.md`(11항목) + `PHASE_V5_EXECUTION_LEDGER.md`(12-col) 작성.
- **Step 29** — `git add` 명시 경로(v5.tex/pdf, results, .session) → descriptive commit → `git push origin HEAD`. (Codex/ 동반 커밋.)

## Implementation Interfaces

### §A. v5 스타일 스펙 (실행자가 그대로 따를 규칙)

**유지(KEEP):**
- §1.1 심볼·단위·부호 규약 표(수식 follow 의 사전 — 필수). 단 설명 칸은 식·기호 위주로 축약.
- 모든 v4 식과 그 논리 순서. 절 제목(번호 체계 `1.N` 유지).
- figure(TikZ) — 시각적 수식으로 follow 보조(아래 Decision D3 확정 따름).
- 절 끝 닫힌 피팅식·알고리즘(G-usable, §1.15/§1.17).
- 적용 한계가 **수식 조건**으로 표현되는 것(예 `Ω > 2RT`, `[ξ_open, ξ_close] ⊂ [0,1]`).

**삭제(DROP):**
- 동기 부여 산문, 직관 설명 문단, 절간 "다음 절은 …" 다리 산문, worked-example 내러티브 서술.
- 가정에 대한 *산문 설명*(가정 자체는 수식 조건/주석 한 줄로 남김).
- 괄호 보충 전보체 류 — 산문 자체를 줄이므로 자연 소거.

**승격(PROMOTE):** v4 가 산문으로만 설명한 유도 단계 → v5 에서 **명시적 중간 수식**으로. (예: "정·역 속도가 같아지는 정지점" 산문 → `r_j^+ = r_j^-` 식을 명시하고 거기서 `ξ_eq` 유도.) 누락 방지가 목적 — 식 수는 늘 수 있고 산문은 준다.

**커넥터 화이트리스트(허용 최소 한글 — 식 사이 한 줄):** "식~\eqref{} 에 대입:", "정지점 조건:", "극한 …→…:", "양변 미분:", "정리하면:", "여기서 …는 \eqref{} 로 정의." 그 외 서술 문단 금지.

### §B. 라벨 규약
- v4 에서 가져온 식: **v4 의 `\label{eq:...}` 이름 그대로 보존**(cross-ref 자동 해소). §1.18 전용 라벨(eq:gcoupled/xistack/dvstack/gapsplit/psieq 등)은 미사용.
- 신규 중간식: `\label{eq:v5-<seckey>-<n>}` (예 `eq:v5-fwdrev-1`). 충돌 시 master 가 통합 단계에서 재명명.
- 절 라벨 `\label{sec:...}` v4 그대로(§1.18 제외).

### §C. ledger row (12-col, [[feedback_phase_execution_loop]])
`| Step | Phase | Unit/Round | Action | Files | Read Range | Build | Defects(found/fixed) | Lens/Chunk | Gate | Commit | Note |`

### §D. 서브 prompt 표준 머리말 (4-세션 고지 의무)
각 sub prompt 첫머리: ① 역할(작업/검수) ② 분업 경계(작업=드래프트 텍스트 return·파일쓰기/commit X; 검수=audit·수정 X·decision queue 등록만) ③ 범위 밖 자의작업 금지(§1.18·새 물리·새 파일·commit·메모리 X) ④ 허위 attribution 금지. + self-contained 컨텍스트(담당 v4 줄범위·스타일 스펙·심볼표·라벨 규약).

### §E. PHASE_V5_RESULT.md 11항목
목표/범위, 수행 단계, Read Coverage(절별 줄범위), 산출물, 빌드 결과, 검수 라운드 추이, 확정 결함·수정, 미해결/추정/미검증(4-tier), v4 대비 보존 감사, Decisions 반영, Next Step.

## Test Plan

- **빌드**: `xelatex -interaction=nonstopmode graphite_ica_ch1_Opus_v5.tex` 2-pass → `.log` 에서 `Undefined`/`Overfull`/`LaTeX Warning: ... undefined` 검색, undefined ref 0.
- **수식 검수**: 각 절 식 재유도(적대 검산) — 부호·차원·극한 일치. v4 식 ↔ v5 식 1:1 대조표(보존 감사 R7).
- **심볼 1:1**: §1.1 표 기호 집합 ⊇ 본문 사용 기호 집합(누락 기호 0, 미사용 표 항목 0 또는 사유).
- **G-follow 판정**: 검수 sub 가 "앞 식만으로 다음 식 도달 가능한가"를 절별 yes/no + 끊기는 지점 보고.
- **G-usable 판정**: §1.15 통합식 + §1.17 코드가 실데이터 대입·실행 가능 닫힌 형태인가(필요 시 round-trip 설계 검토).
- **시각**: `pdftoppm` 로 식 페이지 렌더 판독(잘림·겹침 0).
- **읽은 범위 대조**: 각 sub Read Coverage 가 담당 절 전 범위 cover(미검독 0).

## Assumptions

- A1. "17절까지 / 18절 배제" = §1.1~§1.17 / §1.18(stacking) — 절 번호 체계로 확정(Current Ground Truth 표). **확정에 가까우나 Decision D1 로 1줄 확인.**
- A2. v5 파일명 = `graphite_ica_ch1_Opus_v5.tex`(_Opus_v4 → _v5 컨벤션). 변경 시 Decision.
- A3. v4 §1.1~§1.17 본문은 검수 수렴된 신뢰 원천(재검증 불요, 재표현만). 변환 중 v4 오류 발견 시 decision queue 등록(임의 수정 X).
- A4. 서론(intro)은 v5 에도 축약 형태로 둔다(문건 전체 지도 — 수식 follow 의 출발점). DROP 대상 산문이지만 "읽는 경로" 안내는 최소 유지.

## Decisions Required

> 모두 **추천 기본값**을 두었다. 별도 지시 없으면 기본값으로 GO 후 진행(질문 일괄). 항목당 내용·근거·기본값 명시.

- **D1 — 절 범위 확인.** §1.1(기호와 규약)~§1.17(코드) 포함, §1.18(적층 준안정) 배제. (근거: `\thesection=1.N` 체계 + git log "sec 1.1-1.17", "§1.18 placed after code".) **기본값: 이대로.**
- **D2 — §1.17 코드 절 처리.** §1.17 은 Python 코드(식의 직역)다. "17절까지"에 포함되나 수식이 아니다. **기본값: 코드 유지(범위 내 + 식의 실현·G-usable), 주변 산문만 축약.** 대안: 코드 절도 배제하고 §1.16(반증)에서 종료.
- **D3 — figure 처리.** v4 의 TikZ 그림(장벽도·등온선·이중우물 등). **기본값: 유지(시각적 수식, follow 보조), 캡션은 식 위주 축약.** 대안: 전부 제거(순수 수식만).
- **D4 — 산문 바닥선(prose floor).** **기본값: §A 커넥터 화이트리스트 수준(식 사이 한 줄 연결구만)** — 서술 문단 0. 더 강하게(연결구도 기호 화살표 `⟹` 로) 또는 더 약하게(절 도입 1~2문장 허용) 조정 가능.
- **D5 — 5 동시 세션.** 사용자 명시대로 초안/검수 단계에서 최대 5 서브 병렬. **단 v5.tex 쓰기는 master 직렬**(공유 가변상태 충돌·equation chain 일관성 보호 — 글로벌 헌법 "공유 가변상태→직렬"). 드래프트·검수는 독립이라 5 병렬 정당. (이 분업이 "5세션 구동 + master 중앙관리" 요청과 헌법을 동시 충족.)

## Correction History

- (최초 작성) 직전 계획 없음. v4 §1.18 redo(c06fb81) 가 직전 완료 작업이며 본 계획은 그 위에 신규 v5 트랙을 연다. v4 는 불가침 원천으로만 사용.
