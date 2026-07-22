# v1.0.24 1차 피드백 리비전 Plan (F-01 ~ F-11)

> 작성 2026-07-22. 표준 11-section([[feedback_plan_template_11sections]]). cumulative step = **FB-계열 1부터**(반영 R-계열 1–27 종료 후 신규 캠페인 — reflect ledger 선례와 동일).
> 성격 = **리비전 계획서**(사용자 "1차 피드백 끝. 수정하여 1.0.24 리비전하라"). 대상 = **문건(.tex)만** — 코드 `.py` 무변경(피드백 11건 전부 문건 사안).
> 근거 원장 = `Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md`(F-01~F-11, 각 항목 `\label`·`file:line` 고정).
> 집행 = [[feedback_work_execution_methodology]](4-세션 분업·단위 구성 루프·N회 가변청크 검수·GO 후 무중단·Workflow X→Agent만).

---

## Summary

v1.0.24 문건(3챕터: ch1 흑연+Part T, ch2 LCO, ch3 Si·혼합)을 사용자 1차 정독 피드백 **F-01~F-11** 에 따라 리비전한다. 사용자 명시: 국소로 찝은 항목도 **문건 전체에 퍼진 문제의 표본**이므로 각 항목을 **전역 검토·수정**한다. 물리 내용·식·라벨은 보존하고 **표기·문체·용어·조판·배치**를 교과서/전공서적 기준으로 정리하며, **코드=부록 한정 규칙 위반(F-11)** 을 최우선 정리하고 재발 게이트를 건다. 결과 = v1.0.24 in-place 리비전(신 버전번호 없음), 회사 공개 전 마감 품질.

## Current Ground Truth

**확인한 지침(사용자 제공 압축파일 — 전수 확인 완료).**
- 원본 `/root/.claude/uploads/.../portable_claude_config.zip` → scratchpad `portable_config/` 전개. `global/CLAUDE.md`(최우선 헌법) + `global/memory/MEMORY.md` 인덱스 + `feedback_*` 33종.
- **전문 정독**: `feedback_plan_template_11sections`·`feedback_phase_execution_loop`·`feedback_gate_design_principle`·`feedback_work_execution_methodology`·`global/CLAUDE.md`·`MEMORY.md`. 인덱스로 33종 전건 커버 확인.
- 재확인된 상시 규칙: (a) 계획서 11절·cumulative step·챕터→Phase→step(**1챕터=1Phase 금지**)·섹션명 고정. (b) 5-stage 루프·Result 11항·Ledger 12-col·**result 저장은 다음 Phase 진입 절대 전제**. (c) gate=확인 가능 조건. (d) **Workflow 금지→Agent만**·GO 후 무중단·GO 전 편집 금지. (e) 문서 보호(이전 result/handover 덮어쓰기 X → Addendum/Correction). (f) **F-10 = 기존 상시 규칙**(`communication_style`: 본문 한글 prose + 학술/기술 용어 영어 원어·한글 번역 강요 X). (g) 원본 불가침·명시 선택을 효율 판단으로 대체 금지.

**과거 이력 확인.**
- 직전 계획서 = `Claude/plans/2026-07-19-v1024-si-2L-codex-reflection-plan.md`(반영 캠페인, 11절). 원장 = `docs/v1.0.24/results/V1024_REFLECT_EXECUTION_LEDGER.md`(R0–R5 = step 1–27, 전 PASS). 마감 = `HANDOVER_v24.md`·`MERGE_READINESS_v24.md`·`INDEX_v24.md`.
- 이번 세션 후속(비-ledger): SINTEF 피팅·전수 doc↔code 감사·CODE_GUIDE(.md/.html)·정독 피드백 적층 11건.

**현재 상태(직접 확인).**
- 빌드: ch1 91p·ch2 28p·ch3 20p, 0-err·undefined ref/cite 0(직전 확인). 코드 게이트 GREEN. git 4-ref 동일·tree clean.
- 피드백 위반 위치 대표 스캔 완료(원장에 file:line). **전역 확산 정확 범위 = FB0 인벤토리서 확정**(현재는 대표 표본만 — 미검독 표시).

**피드백 11건 분류.**
- 전역 스윕: **F-11**(코드=부록 위반·최우선)·**F-04**(문체 register)·**F-10**(용어)·**F-06**(조판).
- 국소(단, 동종 전역 확산 점검 동반): F-01(§1.1.4)·F-02(P 압력/확률)·F-03(f/s 자리당)·F-05(제목 N-태그)·F-07(E.3 좌측 넘침)·F-08(Ch2 도입 강조)·F-09(식 2.39 우측 넘침).

## Phase Range

| Phase | 이름 | Steps | 게이트 요지 | 상태 |
|---|---|---:|---|---|
| **FB0** | 착수·결정확정·전역 인벤토리·베이스라인 | 1–5 | 지침·이력 정독 근거·4 전역 인벤토리(코드/register/용어/overflow)·baseline 빌드 GREEN·코드 bit-exact 스냅샷·Decisions 확정 | 대기 |
| **FB1** | F-11 코드=부록 정리(전역, 최우선) | 6–11 | 본문(비부록) 코드토큰 0(grep)·부록 이전 무손실·빌드 GREEN·재발 게이트 신설 | 대기 |
| **FB2** | F-06 조판 전역 설정(preamble) | 12–14 | 줄/문단/여백/microtype 조정·전/후 렌더 비교·빌드 GREEN·페이지수 재기록 | 대기 |
| **FB3** | F-04+F-10 문체·용어 전역 스윕 | 15–24 | 제목·본문 register 교과서화·용어 결정표 적용·라벨 불변·빌드 GREEN | 대기 |
| **FB4** | F-02+F-03+F-05 노테이션 정리 | 25–30 | P→p 전수·f/s 자리당 명확화·제목 N-태그 처리·상호참조 무결·빌드 GREEN | 대기 |
| **FB5** | F-07+F-09+전역 overflow 스윕 | 31–35 | E.3·식2.39·잔여 overflow 0(grep+렌더)·빌드 GREEN | 대기 |
| **FB6** | F-01+F-08 국소 내용 | 36–39 | §1.1.4 처분·Ch2 도입 강조 재배치·orphan 0·빌드 GREEN | 대기 |
| **FB7** | 검증·N회 적대검수·마감 | 40–46 | 코드 bit-exact max\|d\|=0·본문코드0·overflow0·용어일관·N회 수렴(연속2R 0결함)·MERGE/HANDOVER/INDEX addendum·commit·push·4-ref | 대기 |

## Non-goals

- **코드 `Anode_Fit_v1.0.24.py` 변경 X** — 피드백 11건 전부 문건 사안. curve()/dqdv()/fit 수치 **bit-exact 보존**(FB7 게이트 max|d|=0). (F-11 도 부록↔본문 **문건** 정리이지 코드 로직 변경 아님.)
- **물리 내용·수식·`\label`·식 번호·물리 기호(V_n·ξ·Ω 등) 변경 X** — 표기(확률 P·자리당 f/s)·문체·용어·조판·배치만.
- **신 버전번호 X** — v1.0.24 in-place 리비전(사용자 "1.0.24 리비전").
- **v1.0.23 이하·원본 자료·Codex 산출물 수정 X**(원본 불가침).
- **사용자 GO 전 tex 편집 X**(기획 vs 실행). **Workflow·AskUserQuestion·자동 플랜모드 X**.
- 신규 물리·전이 증설·curve-fitting X(피드백 범위 밖).

## Implementation Changes

**수정(문건).**
- `docs/v1.0.24/_sections/*.tex`(다수) — 표기·문체·용어·overflow·국소.
- `docs/v1.0.24/_sections/common_preamble_v1024.tex`(+`ch1_preamble`·`ch2_preamble` 정합) — F-06 조판.
- 마스터 3(`ch1_graphite`·`ch2_lco`·`ch3_si`_v1.0.24.tex) — 필요 시 preamble 로드·구조.

**신규(결과·원장·산출).**
- `Claude/results/PHASE_FB{0..7}_RESULT.md`(11항).
- `Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md`(12-col, FB-계열).
- `Claude/results/comp_v24/INV_code_in_body.md`·`INV_register_titles_prose.md`·`INV_overflow.md`·`TERM_DECISION_TABLE.md`(F-10 결정표) — FB0 인벤토리.
- 전/후 렌더 비교 PNG(F-06·F-07·F-09) — scratchpad.

**갱신(정정 문건 — 덮어쓰기 X, [[feedback_document_protection_addendum_pattern]]).**
- `docs/v1.0.24/results/HANDOVER_v24.md` → `HANDOVER_v24_FEEDBACK_ADDENDUM.md`(리비전 요약·페이지수 갱신).
- `INDEX_v24.md`(신규 산출 행 추가) · `MERGE_READINESS_v24.md` → 리비전 Correction.
- **재발 방지 규칙 명문화**: 프로젝트 `CLAUDE.md` P-절에 "코드 언급=부록 한정(본문·그림·캡션·표·제목 금지)" 불변 규칙 + FB7 grep 게이트(F-11 근본 교정).

## Phase FB0 — 착수·결정확정·전역 인벤토리·베이스라인 (Steps 1–5)

- **Step 1**: 지침·이력 정독 근거를 result 에 Read Coverage 로 고정(본 계획 Current Ground Truth 근거). 활성 폴더·원천 목록 확정([[feedback_plan_template_11sections]] §5 7단계).
- **Step 2**: **4 전역 인벤토리** 생성(Agent 분업 — 독립 대용량 격리 읽기):
  - `INV_code_in_body.md`: 본문(비부록) 렌더 코드토큰 전수(`\code`/`\texttt`/함수·클래스·플래그·`.py`), 파일:행·부록 이전 대상 분류.
  - `INV_register_titles_prose.md`: 제목·본문 essayistic/구어/물음형/수필체 전수(F-04).
  - `TERM_DECISION_TABLE.md`: 의심 용어(요동·양성·정준·대정준·음함수·섭동 등) 빈도·일본식 calque 의심·제안·**사용자 결정 열**(F-10).
  - `INV_overflow.md`: 빌드 로그 overfull 전수 + 렌더 좌/우 넘침(E.3·식2.39 포함, F-06/07/09).
- **Step 3**: **baseline** — 3챕터 빌드 GREEN 재확인(페이지수 기록)·코드 import·게이트 GREEN·**코드 bit-exact 스냅샷**(dqdv 표준입력 곡선 해시 저장 → FB7 비교 기준).
- **Step 4**: **Decisions 확정** — 아래 `## Decisions Required` D1~D6 을 사용자 GO 시 기본값으로 락(조정 시 반영).
- **Step 5**: `PHASE_FB0_RESULT` + `V1024_FEEDBACK_EXECUTION_LEDGER` 초기화.
- **게이트**: (1)지침·이력 Read Coverage 기록됨. (2)4 인벤토리 각 파일 존재·전수(grep 카운트 = 인벤토리 행수 대조). (3)baseline 빌드 err0·ref0 + 코드 bit-exact 스냅샷 파일 생성. (4)Decisions 표 완비. (5)P4 착수 체크리스트 8항.
- **중단 조건**: 인벤토리가 대표 스캔과 크게 어긋나 범위 재산정 필요 시 Decision Gate.

## Phase FB1 — F-11 코드=부록 정리 (전역·최우선) (Steps 6–11)

- **Step 6**: `INV_code_in_body` 기반 본문 코드 언급 처리 방침 확정(단위=파일). 각 건: (a) 삭제(물리 언어로 대체) / (b) 부록 코드맵(appB) 이전. **단위 구성 루프**(파일 하나씩 정독→수정→검수→정합→빌드→ledger).
- **Step 7**: Ch1 신규 절(`ch1_sec05b_gr2L`·`ch1_sec16b_lcoomega`) 본문 코드토큰 제거 — `GRAPHITE_STAGING_*`·`include_electronic_entropy` 등을 **물리 개념어**로("전자항 on/off 옵션") 치환, 코드명은 부록으로.
- **Step 8**: Ch3(`ch3v22_sec02_cases`·`sec02b_sifr`·`sec03_blend` **Fig 2 캡션**·`ch3v22_notation` 코드 열) 정리 — 캡션은 물리/식만 서술.
- **Step 9**: `include_electronic_entropy` 토글식(F-09 식2.39, `ch1_sec16b_lcoomega`) 본문 코드플래그 제거(FB5 overflow 수정과 연계).
- **Step 10**: **Decisions 반영** — D5(§3.5 `ch3v22_sec05_code` 부록 이전 여부·bib 코드 인용) 집행.
- **Step 11**: `PHASE_FB1_RESULT`. **재발 게이트 신설**: `grep` 본문(비부록) 코드토큰 = 0 스크립트 커밋.
- **게이트**: (1)**본문 코드토큰 0** — 부록 파일 제외 grep 결과 공집합(출력 인용). (2)이전분이 부록 코드맵에 무손실 수록(대조). (3)빌드 GREEN·물리 서사 불변(라벨·식 참조 무결). (4)Fig 2 캡션에 코드 메서드 부재(렌더 확인).
- **중단 조건**: 부록 이전이 물리 서사 훼손·라벨 깨짐 유발 시 격리 재설계.

## Phase FB2 — F-06 조판 전역 설정 (Steps 12–14)

- **Step 12**: `common_preamble_v1024` 조판 레버 조정(Decisions D-조판 기본값): 줄간격 1.12→~1.18·문단간격 0.45→~0.6em·여백 22→~26mm·`microtype`(protrusion) 도입. `ch1/ch2_preamble` 정합.
- **Step 13**: 전/후 **샘플 페이지 렌더 비교**(대표 3–4쪽)로 밀도 개선 시각 확인. 페이지수 변동 기록.
- **Step 14**: `PHASE_FB2_RESULT`.
- **게이트**: (1)빌드 GREEN(err0·ref0). (2)전/후 렌더 PNG 존재·밀도 감소 육안 확인. (3)신규 overflow 유발 여부 로그 확인(→FB5 로 이월). (4)3 마스터 preamble 정합(동일 설정).
- **중단 조건**: 여백 확대가 그림·표 레이아웃 파손 시 값 재조정.

## Phase FB3 — F-04+F-10 문체·용어 전역 스윕 (Steps 15–24)

- **Step 15**: 제목 스윕 — `INV_register_titles_prose` 의 제목 16+건을 명사구 표제로(라벨 불변, 물음형·수필형·구어 제거). 예 "거시 열역학으로"→"거시 열역학적 유도" 등.
- **Steps 16–22**: 본문 산문 register+용어 **단위 구성 루프**(챕터·절 단위, 하나씩): 구어 축약·서술 삽입구·수사 제거 + `TERM_DECISION_TABLE` 승인 용어 치환(첫 등장 영문 병기 규약). Ch1(16–18)·Ch2(19–20)·Ch3(21)·부록(22).
- **Step 23**: 전역 일관성 — 용어·기호 표기 통일(도메인 일관성), 첫 등장 병기 누락 0.
- **Step 24**: `PHASE_FB3_RESULT` + 빌드.
- **게이트**: (1)제목 essayistic 0(재스캔). (2)`TERM_DECISION_TABLE` 승인분 전수 적용(grep 잔존 확인). (3)`\label`·식번호·물리기호 불변(diff 확인). (4)빌드 GREEN. (5)본문 register = 교과서(샘플 절 G-follow 렌즈 검수).
- **중단 조건**: 용어 치환이 코드↔문건 정합(부록 코드맵) 깨뜨리면 해당 용어 보류·Decision.

## Phase FB4 — F-02+F-03+F-05 노테이션 정리 (Steps 25–30)

- **Step 25**: **F-02** 확률 P→p 전수(`ch1_sec02a_part0` §1.2.1 `eq:sm-fund`↔`eq:sm-resv`·대정준 박스 `eq:sm-gc`·하류 전건). 압력 P(통상 표기) 유지. 소문자 p 타 양 충돌 재검.
- **Step 26**: **F-03** 자리당 f_int/s_int 명확화(Decisions D2) — 첫 등장 "자리당(per-site) …, 총량 F/S 와 구분" 명시 or 선택 스킴. 총량 F/S 구분 보존.
- **Step 27**: **F-05** 제목 N-태그 처리(Decisions D3) — 기본 = 제목에서 (N2) 등 제거, 절 첫 문장/노드맵 표로 상호참조(spine 그림·`tab:nodemap`·`tab:nodecode` 정보 보존).
- **Step 28**: 상호참조 무결 — `\ref`/`\eqref` 깨짐 0(빌드 undefined 0).
- **Step 29**: 전역 노테이션 일관(검수 7항목 #1: V_n/V_{n,app}/… 구분 유지).
- **Step 30**: `PHASE_FB4_RESULT` + 빌드.
- **게이트**: (1)확률 P 잔존 0(grep, 압력 P 제외 규칙 명시)·대정준 박스 반영. (2)f/s 자리당 명시·총량 F/S 구분 유지(원문 대조). (3)N-태그 제목 제거 후 상호참조 무손실(노드맵 표 대조). (4)undefined ref/cite 0. (5)빌드 GREEN.

## Phase FB5 — F-07+F-09+전역 overflow 스윕 (Steps 31–35)

- **Step 31**: **F-07** E.3(`ch1_appE_selfconsistent` `\item[\textbf{..}]` 5건) — 볼드 리드인 or `description` 행걸이로 좌측 넘침 제거.
- **Step 32**: **F-09** 식2.39(`ch1_sec16b_lcoomega` `cases`) — 설명을 수식 밖으로/`p{}` 열로 우측 넘침 제거(FB1 Step9 코드플래그 제거와 합류).
- **Step 33**: `INV_overflow` 잔여 전건(ch1_appB 568pt longtable·ch2 revheat/traps 등) 처리 — FB2 신규 발생분 포함.
- **Step 34**: **전역 렌더 점검** — 3챕터 재빌드 후 좌/우 넘침 0(자동 스캔 + 대표 페이지 렌더).
- **Step 35**: `PHASE_FB5_RESULT`.
- **게이트**: (1)E.3·식2.39 렌더 넘침 0(전/후 crop 대조). (2)빌드 로그 overfull(텍스트) 실질 0 or 문서화된 잔여만. (3)빌드 GREEN. (4)물리·라벨 불변.
- **중단 조건**: 표 구조 변경이 값·정합 훼손 시 보류·Decision.

## Phase FB6 — F-01+F-08 국소 내용 (Steps 36–39)

- **Step 36**: **F-01** §1.1.4(`sec:pointwise`) 처분(Decisions D4) — 기본 = 측정원리 bgbox/srcbox 배경 압축(또는 부록 강등), load-bearing 점별원칙+keybox 유지. `\ref{sec:pointwise}` 역참조 정리.
- **Step 37**: **F-08** Ch2 도입(`ch1_sec11_lcointro`) 강조 재배치 — 공유("전극 무관 식5" `sec:lco-map`·"같은 logistic" `sec:lco-preview`) 압축, σ_d(다른 점)·전자항(추가된 점) 부각. 전극무관 논거는 **삭제 아닌 한 줄 포인터 압축**(재사용 자격 보존).
- **Step 38**: orphan 0 확인(추가·이동분 앞 도입·뒤 사용).
- **Step 39**: `PHASE_FB6_RESULT` + 빌드.
- **게이트**: (1)§1.1.4 처분 후 역참조·라벨 무결. (2)Ch2 도입서 σ_d·전자항 선행·공유 서술 축소(전/후 분량·순서 대조). (3)전극무관 논거 존치(재사용 자격 문장 유지). (4)빌드 GREEN·orphan 0.

## Phase FB7 — 검증·N회 적대검수·마감 (Steps 40–46)

- **Step 40**: **코드 bit-exact 검증** — dqdv 표준입력 곡선 vs FB0 스냅샷 max|d|=0(코드 무변경 증명).
- **Step 41**: **자동 게이트 배치** — 본문 코드토큰 0(grep)·확률 P 0·overflow 0·undefined 0·용어표 잔존 0.
- **Step 42**: **N회 가변-청크 적대검수**([[feedback_multiagent_review_chunking]]) — Agent 병렬, 라운드마다 청크 스킴·렌즈(구조/물리 적대/G-follow/G-usable/시각/직전수정 새결함) 전환, **연속 2라운드 확정결함 0** 까지(기본 ≥ 실질 수렴). master 삼각검증·직접 수정.
- **Step 43**: 최종 빌드 GREEN(3챕터 페이지수 기록) + 대표 렌더 시각 확인.
- **Step 44**: 마감 문서 — `HANDOVER_v24_FEEDBACK_ADDENDUM`·`INDEX_v24` 갱신·`MERGE_READINESS` 리비전 Correction. **CLAUDE.md 코드=부록 규칙 명문화**(F-11 재발방지).
- **Step 45**: commit(단위별 누적)·push·**main ff-merge·4-ref 동일** 확인.
- **Step 46**: `PHASE_FB7_RESULT`·ledger 마감·최종 보고.
- **게이트**: (1)코드 bit-exact max|d|=0. (2)자동 게이트 5종 전부 0/PASS(출력 인용). (3)N회 검수 연속 2R 0결함 수렴. (4)빌드 GREEN·overflow 0·본문코드 0. (5)4-ref 동일·마감 문서 존재. (6)물리·식·라벨 불변 diff.

## Implementation Interfaces

- **인벤토리 행 양식**: `파일:행 | 유형 | 현재 | 제안 | (결정)`.
- **TERM_DECISION_TABLE 열**: `용어 | 현재 한글 | 빈도 | 일본식 calque 의심 | 제안(영문/음차/표준유지) | 사용자 결정`.
- **de-code-ify 규칙**: 본문에서 코드 식별자 → 물리/모델 언어. 필요 시 부록 `tab:nodecode`(appB) 행 추가. 캡션 = 그린 대상(물리·식)만.
- **register 재작성 규칙**: 명사구 표제·평서·수사/구어 제거. `\label` 불변(제목 문구만 교체). 첫 등장 영문 병기.
- **overflow 수정 패턴**: 좌(커스텀 라벨)→리드인/description; 우(math cases 내 텍스트)→수식 밖 or `p{}` 열.
- **Result 11항·Ledger 12-col** = [[feedback_phase_execution_loop]] 양식. **Gate = 확인 가능 조건**([[feedback_gate_design_principle]]).
- **보고 4-tier**([[feedback_confirmed_items_policy]]): 확정/근거 미발견/추정/미검증.

## Test Plan

- **빌드**: `xelatex` 3챕터 0-err·undefined ref/cite 0(로그 인용).
- **코드 bit-exact**: dqdv 표준입력 곡선 max|d|=0(FB0 스냅샷 대조) — 코드 무변경 증명.
- **본문 코드 0**: 부록 제외 grep 공집합(출력 인용).
- **overflow 0**: 빌드 로그 overfull 텍스트 실질 0 + 렌더 좌/우 넘침 시각 0(전/후 crop).
- **용어/표기**: `TERM_DECISION_TABLE` 승인분 전수 적용·확률 P 잔존 0(grep).
- **register**: 제목 essayistic 재스캔 0 + 대표 절 G-follow/G-usable 렌즈.
- **상호참조·라벨**: undefined 0·`\label` diff 불변.
- **N회 검수**: 라운드별 결함 수 추이(연속 2R 0 수렴).
- **재현**: 인벤토리·결정표·게이트 스크립트·전후 렌더 커밋.

## Assumptions

- 물리·식·라벨 불변이므로 **코드 bit-exact 유지 가능**(피드백 전건 문건).
- register/용어/표기 변경이 식·`\label`·상호참조를 깨지 않음(제목 문구만 교체·기호 표기만 조정).
- Decisions 기본값으로 진행 가능(사용자 조정 시 해당 step 반영).
- 조판 레버 "약간씩" 조정이 그림·표 레이아웃을 파손하지 않음(FB2서 실증, 실패 시 값 재조정).
- 정독 피드백 원장(F-01~11)이 전역 확산의 대표 표본 — 정확 범위는 FB0 인벤토리서 확정.

## Correction History

- **직전**: 정독 피드백 적층 캠페인(F-01~F-11, `USER_FEEDBACK_v1024_READING.md`) → 사용자 "1차 피드백 끝. 수정하여 1.0.24 리비전하라. 작업 계획서부터." → **적층 모드 종료·리비전 실행 모드 전환**.
- **내 프로세스 실패 2건 기록·교정**:
  1. **F-11(코드=부록 위반)**: v1.0.24 신규 절(gr2L·lcoomega·sifr) 저작 시 기존 규칙("함수명은 부록에만", ch2_appB) 미승계 → 본문 코드 언급 다수. 교정 = FB1 전역 정리 + FB7 grep 게이트 + CLAUDE.md 명문화.
  2. **세션 초 "지침 없음" 오판**: 사용자 제공 `portable_claude_config.zip`(scratchpad 전개)을 확인 안 하고 `_claude/memory/` 만 보고 "메모리 없음"·"이력 확인 불가"로 단정. 교정 = 압축파일·과거 이력 전수 확인 후 본 계획 작성(Current Ground Truth 근거 고정).

---

## Decisions Required (기본값 有 — "GO" 시 기본값대로 진행, 특정 항목만 조정 가능)

> [[feedback_flow_interruption]]·[[feedback_execute_explicit_choice_not_judgment]]: 팝업 없이 평문+기본값. 이미 방향 주신 항목(F-02 확률 P→p·F-08 강조 방향)은 재질의 X — 그대로 집행.

- **D1 (범위·버전)**: v1.0.24 **in-place** 리비전(신 버전번호 X), 대상 **문건만**·코드 bit-exact. — *기본값: 그대로.*
- **D2 (F-03 f/s 자리당)**: 소문자 f_int/s_int **유지 + 첫 등장에 "자리당(per-site)·총량 F/S 와 구분" 명시**(총량 대문자와 충돌 방지). 대안: `f_site`/`\tilde F` 등 명시 기호. — *기본값: 유지+명시(최소 침습, 규약 보존).*
- **D3 (F-05 제목 N-태그)**: 절 **제목에서 (N0)~(N9)·(Part 0)·(N2′) 등 코드 제거**, spine 그림·노드맵 표로만 상호참조. 대안: 제목 유지. — *기본값: 제목에서 제거(전공서적 표제 순수성; 정보 손실 0).*
- **D4 (F-01 §1.1.4)**: 측정원리 **배경 박스(bgbox·srcbox) 압축**(또는 부록 강등), 점별원칙 본문+keybox 유지. 대안: 절 전체 삭제 / 유지. — *기본값: 배경 압축·핵심 유지.*
- **D5 (F-11 §3.5 코드명세절·bib 코드 인용)**: `ch3v22_sec05_code`(본문 §3.5 코드 명세) **부록으로 이전**; 서지 `\code{Anode_Fit_v1.0.19}` 인용은 **평문화(내부 데이터 출처로 유지, `\code` 제거)**. 대안: §3.5 현상 유지. — *기본값: 부록 이전 + bib 평문화.*
- **D6 (F-10 용어)**: FB0서 `TERM_DECISION_TABLE` 제시 → **승인분만 치환**. 기본 제안: 요동→fluctuation(첫 병기)·양성→positivity·음함수→implicit function·섭동→perturbation; **정준/대정준/분배함수 = 국내 교과서 표준이라 유지**. 전건 사용자 최종 확정. — *기본값: 표 제안대로, 단 표는 GO 후 FB0서 확정 제시.*

> **남은 유일 사용자 입력 = "GO"**(또는 D1~D6 중 조정). GO 시 FB0(인벤토리·baseline·결정표)→FB7(마감)까지 [[feedback_work_execution_methodology]] 대로 무중단 집행. 단 **D6 용어 결정표는 FB0서 작성해 확인받고 FB3서 적용**(치환 규모 큼).
