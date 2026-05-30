# RB-series Execution Ledger (누적 복구 지점)

> **용도**: 컴팩션·세션교체·재개를 위한 복구 좌표. 매 Phase 종료 시 갱신.
> 계획서: `Claude/plans/2026-05-30-undergrad-rederivation-rebuild-plan.md`
> 규칙: 챕터 안 Phase 분할, step 전체 단조 누적. result 없는 Phase 진입 금지.

| Phase | Planned Steps | Actual | Block | Purpose | Status | Plan | Result | Gate | Next Step |
|---|---|---|---|---|---|---|---|---|---|
| (pre) Phase A | — | — | audit | 폰 통합본 8종 장별 적대 재검수 | PASS | RB plan §CGT | `PHASE_A_consolidated_adversarial_review_RESULT.md` | PASS_AUDIT_A | — |
| (pre) Phase B | — | — | audit | 장간 정합 + 통합본 빌드 검수 | PASS | RB plan §CGT | `PHASE_B_crosschapter_build_review_RESULT.md` | PASS_AUDIT_B | 1 |
| 0.1 | 1–5 | 1–5 | foundation | cross-chapter 규약 동결 | PASS | RB plan Phase 0 | `RB_CHARTER.md` | PASS_CHARTER | 6 |
| 0.2 | 6–12 | 6–12 | foundation | references dossier + DOI 검증(30종+보강) | PASS | " | `RB_REFERENCES_DOSSIER.md` | PASS_DOSSIER | 13 |
| 0.3 | 13–16 | 13–16 | foundation | 통합 AL 체계 + notation + 가독gate | PASS | " | `RB_AL_MASTER.md` | PASS_AL_SKELETON | 17 |
| (Phase 0 종합) | 1–16 | 1–16 | foundation | Foundation 완료 | PASS | RB plan Phase 0 | `PHASE_0_foundation_RESULT.md` | PASS_FOUNDATION | 17 |
| 1.1 | 17–20 | 17–20 | Ch1 | 골격추출(핵심식 14 + 가정목록 + 심플화 6건 + 입력결함 5건) | PASS | RB plan Phase 1 | `RB_LEDGER_CH1.md`(S1) | PASS_CH1_SKELETON | 21 |
| 1.2 | 21–25 | 21–25 | Ch1 | grounding 감사(31가정, 무근거 5건, AL-14 닫힘) | PASS | RB plan Phase 1 | `PHASE_1_2_ch1_grounding_RESULT.md` + `RB_LEDGER_CH1.md`(S2) | PASS_CH1_GROUNDING | 26 |
| 1.3–1.5 | 26–42 | — | Ch1 | 무비약 재유도→적대검증→수정·gate | PENDING(다음) | RB plan Phase 1 | `ch1_rebuilt.tex`(예정) | — | 26 |
| 2.1–2.5 | 43–62 | — | Ch2 | (Ch1) 가역 반응열, 5-stage | PENDING | RB plan Phase 2 | (예정) | — | 43 |
| 3.1–3.5 | 63–88 | — | Ch3 | (Ch1) 반응속도론 일반화, 5-stage | PENDING | RB plan Phase 3 | (예정) | — | 63 |
| 4.1–4.5 | 89–110 | — | Ch4 | (Ch3) 가역 반응열, 5-stage | PENDING | RB plan Phase 4 | (예정) | — | 89 |
| 5.1–5.5 | 111–132 | — | Ch5 | (Ch3) 히스테리시스, 5-stage | PENDING | RB plan Phase 5 | (예정) | — | 111 |
| 6.1–6.3 | 133–146 | — | Ch6 | 기존 내용 검토→Gate→(조건부)재유도 | PENDING | RB plan Phase 6 | (예정) | — | 133 |
| 7.1–7.3 | 147–157 | — | 통합 | refs + full + 정합·빌드 | PENDING | RB plan Phase 7 | (예정) | — | 147 |

## 현재 위치
- **마지막 완료**: Phase 0 전체(Foundation, step 1–16). `RB_CHARTER.md` + `RB_REFERENCES_DOSSIER.md` + `RB_AL_MASTER.md` + `PHASE_0_foundation_RESULT.md`.
- **★ 핵심 발견(5-30 경고 적중)**: 폰 `macdonald2000` = \emph{저자} 오귀속(DOI·물리 유효, 저자 Macdonald→Svare/Martin/Borsa) → `svare2000` 정정·유효 사용 + johnston2006 보강. funabiki title↔locator 혼합 → ea+jes 둘 등재(D7). lee2011/son2013/lindsey1980 DOI 정정. plonka 미확인(FLAGGED). AL-1~63 기등재.
- **마지막 완료**: Phase 1.2 Ch1 grounding 감사(step 21–25, PASS). 31 가정 판정, 무근거 5건(clamp HIGH·softplus·ε_tol·ledger번호 HIGH·Plan A) → Phase 1.3 재작성. AL-5~9 등재.
- **★ AL-14 핵심물리 닫힘 확정**: svare2000+johnston2006+lindsey1980 으로 3렌즈 YES_BOUNDED. FLAGGED 불필요. gap(데이터영역·적용)은 BOUNDED 명시.
- **다음 진입**: **Phase 1.3 — Ch1 무비약 재유도 (step 26).** `graphite_ica_ch1_rebuilt.tex` 작성.
- **Ch1 재작성 방침**: 흐름 14식 보존 + 학부 무비약 + global AL-# 통일 + 심플화(clamp 제거; softplus·ε_tol·Plan A closure → Ch6 이관) + 극판전위 배리어 낮춤 위주 + AL-14 BOUNDED 명시.
- **결정**: D1 해소. D7(funabiki 둘다등재) 권고. D2~D6 권고값 진행.

## Phase 1 최종 상태 (Ch1 완결)
- `graphite_ica_ch1_rebuilt.tex` **558줄, 무결성 PASS** (env balance·dup label 0·undefined ref/cite 0·GS-4 정의식 leak 0·macdonald 0·svare2000 3).
- 적대검증 49 findings → 실결함(컴파일차단 3 + HIGH 1 + MEDIUM 다수 + LOW) 전건 수정. host 2회 오판(MEDIUM 1 / 잔여 4) 정정 후 재확인.
- **다음**: 사용자 Decision Gate(Ch1 검토) → GO 시 Phase 2.1 (step 43).

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-05-30 | Ledger 신설. Phase A/B result 소급 기록 반영. RB Phase 0~7 / step 1–157 등록. |
| 2026-05-30 | Phase 0~1 완료. Ch1 재구성본 558줄 무결성 PASS. host 결함파싱 2회 오판(cp949/요약잘림) 정정 — JSON 전건 재파싱 후 전건 수정. Decision Gate. |
