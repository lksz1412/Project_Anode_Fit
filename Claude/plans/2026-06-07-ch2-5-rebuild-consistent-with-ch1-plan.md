# Ch2~5 신규 트랙 재작성 — Ch1 정합 (발열·반응속도론·통합 상태방정식·히스테리시스) Plan

**Date**: 2026-06-07 · **Author**: Claude · **챕터**: H(Ch2~5 build) · **Phase**: H.0 + H2~H5
**대상(신규)**: `Claude/docs/graphite_ica_ch2.tex`~`ch5.tex` · **기준**: 확정된 `graphite_ica_ch1.tex`(952줄·20p, F·G 완료)
**source(물리 재료)**: `Claude/work/oldtrack_src/graphite_ica_ch[2-5]_rebuilt.tex`(구-track, 947/916/1004/999줄) — 물리 \emph{재료}로만; Ch1 형식으로 \emph{재작성}(Ch1 이 from-scratch 재작성이었던 것과 동일 방식).
**트리거**: 사용자 — Ch1 내용 방식·형식·작업방법 그대로 따와 Ch2~5 야간 자율 초안, Ch1 최대 정합. \emph{Ch2부터는 이전 챕터까지 함께 검토.}

---

## Summary
Ch1(흑연 음극 dQ/dV peak 물리)을 기준으로 Ch2~5 를 \emph{같은 형식·register·방법}으로 신규 작성한다. 각 챕터는 (i) 앞 챕터 \emph{기준식 전달(inherit)} 절로 열고, (ii) Ch1 의 변수·부호·박스·소제목 규약을 그대로 쓰며, (iii) 도출 정직(무비약)·교과서/리뷰체로 전개한다. 구-track Ch2~5 는 \emph{물리 재료}로 참고하되 Ch1 형식으로 재구성.
- **Ch2 발열**: OCV 온도계수 → reaction entropy → 가역/비가역 열 분해 → 온도 되먹임 → kinetic-lag 열 tail(ICA tail 의 열적 거울).
- **Ch3 반응속도론**: 전위·과전압·구동력 계층 → detailed balance → Ch1 relaxation ODE 정합(Level A=B) → BV·R_n≠R_ct≠R_eff 분해 → C-rate 재분해.
- **Ch4 통합 상태방정식**: η 기준 단일화 → flux-force entropy production → 비가역열 일반형 Σn_j^eff I_j η_j → 전기-열 coupling 순서.
- **Ch5 히스테리시스**: signed current·branch → 충전 부호 s_φ,j^b → metastable target → branch kinetics·ICA → loop-area 소산열 → full-cell.
**방법**: 절별 작성 → Codex foreground 적대 문제 0까지 → \emph{이전 절 + 이전 챕터} 정합 검토 → 빌드 → result → 커밋·푸쉬(버전마다).

## Current Ground Truth
- Ch1 확정: 변수(V_n·θ_j·ξ_j·U_j·w_j·k_j·r_j^±·A_j·χ·ρ_G·Q_j·C_bg·s·s_I), 부호(s=+1 방전), 핵심식(eq:charge·logistic·relax·eyring·bv·db·keff·LqV·closed·simplefit·dUdT·total), 박스 6종(핵심·유효 범위·비고·심화·검산·staging), register(질문 라벨 X·명사구 소제목·메타 X·도출 정직).
- 구-track Ch2~5 존재(물리 재료) + inherit/결론/가정원장(AL) 구조. 단 \emph{구 형식}(질문 라벨·Chapter 1 에서 전달받는 기준식 절 등) → Ch1 register 로 재작성.
- **Ch1 핸드오프(Ch2~5 가 받는 기준식)**: 전하 보존 V_n(eq:charge) · 평형 logistic ξ_eq(eq:logistic) · 완화 ODE(eq:relax) · Eyring/BV/detailed balance(eq:eyring·bv·db) · 유효 배리어 k_j^eff(eq:keff) · OCV 온도계수 ∂U_j/∂T=ΔS_j/(sF)(eq:dUdT) · 측정축 V_app(eq:vapp) · 다전이 합(eq:total).

## Phase Range
| Phase | 범위 | 핵심 |
|---|---|---|
| **H.0** | 정합 골격·설계 | Ch1 preamble/박스/macro 복제 + 변수·부호·핸드오프 glossary 확정 + 4챕터 절 구조 설계 + naming/inherit 규약 |
| **H2** | Ch2 발열 | inherit → OCV 온도계수 → reaction entropy → 가역/비가역 열 → 되먹임 → kinetic-lag 열 tail → 식별성 → 전달·결론 |
| **H3** | Ch3 반응속도론 | inherit → 전위 계층 → detailed balance → Ch1 ODE 정합(A=B) → BV·R 분해 → C-rate → 전달·결론 |
| **H4** | Ch4 통합 상태방정식 | inherit → η 단일화 → entropy production → 비가역열 일반형 → 가역열 → 전기-열 순서 → 전달·결론 |
| **H5** | Ch5 히스테리시스 | inherit → signed/branch → 충전 부호 → metastable target → branch kinetics·ICA → loop 소산열 → full-cell → 전달·결론 |

**절별 게이트**: G-consist1(Ch1 변수·부호·식 정합·핸드오프 정확) · G-prevch(이전 챕터 전체 정합 — Ch2부터) · G-honest(무비약 도출) · G-register(Ch1 교과서체·박스·소제목 규약) · G-build · G-review(Codex foreground→판정→반복) · G-recovery(§X 컴팩션 재정독).
**정지 조건**: Decision Gate(중대 물리 충돌)/FAIL/사용자 stop/통제문서 모순. 그 외 \emph{야간 끝까지 자율}.

## Non-goals
- Ch1 본문 수정(이미 확정; Ch2~5 가 inherit 만). 구-track 형식·라벨 그대로 복붙(재작성). 피팅 수치 Appendix B(별도). Workflow 도구.

## Implementation Changes
신규 `graphite_ica_ch2.tex`~`ch5.tex`(Ch1 preamble 복제) / `PHASE_H*_RESULT.md` + ledger / 본 계획. 구-track·Ch1·이전 result 보호.

## Phase 상세
- **H.0**: Ch1 L1~63 preamble(documentclass·packages·setstretch·박스 6 newtheorem·macro·fancyhdr) 복제해 ch2~5 헤더 통일. 제목 형식 `Chapter N` + 주제(Ch1 식). 변수·부호·핸드오프 glossary(§GL) 확정. 각 챕터 절 구조(아래 §ST) 확정.
- **H2~H5**: 각 챕터 = ① inherit 절(앞 챕터 기준식 명시 수령) → ② 물리 본문 절들(구-track 재료를 Ch1 register·무비약으로 재작성, 핸드오프 식과 정합) → ③ 식별성 → ④ 전달(다음 챕터로) → ⑤ 결론(+가정원장 AL 은 비고/유효 범위 박스로 흡수, 구 형식 AL 절 지양). 절별 Codex→문제 0→이전 절·이전 챕터 정합→빌드→result→커밋.

## Implementation Interfaces
**§GL 변수·부호 glossary(Ch1 그대로 + Ch2~5 신규)**: Ch1 전량 + Ch2 ΔS_j·반응 entropy·q̇_rev/q̇_irr·η_j·Bernardi · Ch3 R_ct·R_n,eff·n_j^eff·generalized affinity · Ch4 entropy production σ·flux-force · Ch5 s_φ,j^b·ξ_tar^b·loop area·signed q_stt. \emph{Ch1 기호 재정의 금지}.
**§ST 챕터 절 양식(Ch1 정합)**: 서론(짧은 동기, 질문 라벨 X) → inherit(기준식 박스/표) → 명사구 소제목 도출 절(정의→유도 무비약→\boxed 결과 → 의미/검산 박스) → 식별성/유효 범위 → 전달 → 결론(keybox). 박스 6종만.
**§X Anti-compaction**: 컴팩션·재개 직후 — 직전 result·ledger·작성 중 챕터 tex·Ch1 핸드오프 재정독.
**§R Result 11항목·Ledger 12-col**.

## Test Plan
- **Ch1 정합 grep**: 변수·부호(s=+1)·핸드오프 식 라벨이 Ch1 과 일치, 재정의 0. 각 챕터 inherit 식 = Ch1 실제 식과 대조.
- **이전 챕터 정합**(Ch2부터): 앞 챕터 전달 항목 ↔ 현 챕터 수령 항목 교차매핑, 충돌 0.
- **빌드 GREEN**: 각 ch2~5 `!`0·undefined 0·overfull 0(독립 컴파일; 상호 \ref 는 챕터 내 한정 또는 의미 인용).
- **Codex foreground**: 각 챕터 무비약·Ch1 정합·이전 챕터 정합 CLEAN.
- **register**: 질문 라벨·메타·구어 0(Ch1 기준 grep).

## Assumptions
- A1: 구-track 물리는 \emph{재료}(정확성은 재검증), Ch1 형식으로 재작성. A2: Ch1 기호·부호·식 불변(inherit). A3: 각 챕터 독립 컴파일(공유 preamble); 챕터 간 참조는 의미 인용 우선. A4: 가정원장(AL)은 박스로 흡수(구 형식 AL 절 신설 지양).

## Decisions Required (무응답 시 권고값 — 사용자 취침, 자율)
- **D-AL**: 구 가정원장 절 → Ch1엔 없음 → \emph{유효 범위/비고 박스로 흡수}. 권고: 흡수(Ch1 정합).
- **D-범위**: Ch2→Ch3→Ch4→Ch5 순차, 야간 최대 진척. 권고: 그대로. 완성 못한 챕터는 초안+handover.
- **D-naming**: `graphite_ica_ch{N}.tex`. 권고: 그대로.

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-06-07 (H v1) | Ch2~5 Ch1-정합 신규 작성 계획 — 발열/반응속도론/통합상태방정식/히스테리시스. inherit-first·Ch1 register·무비약·이전 챕터 정합. 구-track 물리 재료, Ch1 형식 재작성. 절별 Codex foreground iterate + 이전 절·챕터 정합 + 버전 커밋. |
