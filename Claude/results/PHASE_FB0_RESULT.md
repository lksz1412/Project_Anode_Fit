# Phase FB0 — 착수·결정확정·전역 인벤토리·베이스라인 Result

## Summary
v1.0.24 1차 피드백 리비전(F-01~F-11)의 착수 phase. 전 계보 이력·지배 문서 정독 근거 고정, 4 전역 인벤토리 작성, baseline(빌드 GREEN·코드 bit-exact 스냅샷·게이트) 확정, 결정 D1~D6 락. **tex·코드 무수정**(인벤토리·결과 문건만).

## Step Range
cumulative **FB-계열 step 1–5** (반영 R-계열 1–27 종료 후 신규 캠페인).

## Inputs
- **지배 문서**(정독): `docs/v1.0.15/CLOSING_v1.0.15.md`(헌법3종+D1-6+Part5)·`docs/v1.0.20/results/V1020_STYLE_RUBRIC.md`(A~G)·`results/process/V1013_TERMS_POLICY.md`·`results/process/V1014_TONE_AUDIT.md`(79)·`results/process/PHASE_R0_convention-lock_RESULT.md` + scratchpad `portable_config/global/{CLAUDE.md,memory/*}`(33).
- **이력 검토**: `comp_v24/HIST_{register,terminology,notation_code,layout_versionarc}.md`(4축 검토 sub).
- **피드백 원장**: `comp_v24/USER_FEEDBACK_v1024_READING.md`(F-01~F-11).
- **대상 원천**: `docs/v1.0.24/_sections/*.tex`(57)·`common_preamble_v1024.tex`·`Anode_Fit_v1.0.24.py`·3 빌드 로그.

## Files Created
- `comp_v24/INV_code_in_body.md` — 본문 코드언급 17행 + §3.5(F-11).
- `comp_v24/INV_overflow.md` — F-07·F-09 렌더-only + Tier2 로그 overfull(F-06/07/09).
- `comp_v24/TERM_DECISION_TABLE.md` — V1013 승계 + F-10 미결 6개어(검수 sub).
- `comp_v24/INV_register_titles_prose.md` — register offender ~94행(검수 sub).
- `comp_v24/HIST_*.md` 4종(이력 검토 sub, 전 커밋).
- scratchpad `FB0_code_baseline.sha256`(코드 bit-exact 기준).

## Files Updated
- 없음(tex·코드 무수정). ※`plans/2026-07-22-...plan.md` 는 FB0 착수 전 이력 반영으로 갱신(별도 커밋).

## Read Coverage
- 전문 정독: CLOSING_v1.0.15(1–106)·V1020_STYLE_RUBRIC(1–51)·plan_template·phase_execution_loop·gate_design·work_methodology·global CLAUDE.md·MEMORY.md·4 HIST 요약.
- 부분: V1013_TERMS_POLICY·V1014_TONE_AUDIT(검수 sub 경유 요약 + rubric C2 대조).
- grep+렌더: 코드토큰 전수·overfull 3로그·E.3 85쪽·식2.39 23쪽.
- **미검독(정직)**: INV_register 는 일부 대형 본문 파일(ch1_sec01/06/07/12/14·ch2_sec01/06/10·ch3v22_sec02/03/04)을 grep-sweep만 함 → **FB3 단위-루프서 전문 정독으로 보강**(저강도 은유·A1 전보체 추가 발견 가능).

## Execution Evidence
```
코드 bit-exact 기준: sha256 = f230f59bb10bcc49cdce9047c196530f857d2eda4d3b1be819ceb36ee6aaf680  Anode_Fit_v1.0.24.py
게이트: test_gates_v1024 → G1 PASS(module max|d|=0.0e+00, golden 4.3e-15, bit-exact=True)|G2|G3|n(T) PASS; R6 3/3 PASS
        test_gates_v1024_reflect → 4/4 ALL PASS
        test_gates_v1024_selfconsistent → 5/5 ALL PASS
빌드(3챕터): ch1 0-err/91p/undef-refcite 0 · ch2 0-err/28p/0 · ch3 0-err/20p/0 (3 'undefined'=한글-italic 폰트 fallback, ref/cite 아님)
```

## Validation (게이트별)
- **(1) 지침·이력 Read Coverage 기록** — PASS(위 Read Coverage + 4 HIST + plan Current Ground Truth).
- **(2) 4 인벤토리 존재·전수** — PASS(4 파일 생성; code 17행·overflow 2 tier·terms 6미결+승계·register ~94). ※register·term 은 "정밀 카운트는 편집 세션 재측정" caveat 명기(추정 tier).
- **(3) baseline 빌드 GREEN + 코드 bit-exact 스냅샷** — PASS(0-err·0-undef-refcite; sha256 고정; 게이트 3스위트 PASS).
- **(4) Decisions 표 완비** — PASS(D1~D6 아래 락).
- **(5) P4 착수 체크리스트 8항** — PASS(활성폴더·원천목록·전문vs부분·기존계획/ledger/handover·cumulative시작점·중단조건·검증명령·저장위치 전부 확정).

## Gate
**PASS_FB0_BASELINE** (조건: 4 인벤토리 + baseline GREEN + bit-exact 스냅샷 + Decisions 락 + Read Coverage).

## Confirmed Non-Changes
- `Anode_Fit_v1.0.24.py` 무변경(sha256 기준 고정, 이 캠페인 전체 무변경 대상).
- `_sections/*.tex`·preamble 무변경(FB1부터 편집).
- v1.0.23 이하·원본·Codex 무접촉.

## Open Issues / Decision Queue
**결정 D1~D6 락(사용자 "고"=GO, 기본값 진행 — [[feedback_user_decision_no_requery]]·[[feedback_plan_continuation_until_done]]). 사용자 조정 시 해당 항목 반영(stop 조건).**
- **D1**: v1.0.24 in-place·문건만·코드 bit-exact. **락.**
- **D2 (F-03)**: 소문자 f/s 유지 + 자리당 명시(각주/첫등장). 이력 정합(convention-lock·rubric B5). **락.**
- **D3 (F-05)**: 제목 N-태그 제거(그림·표 상호참조 유지). **락.**
- **D4 (F-01)**: §1.1.4 배경박스 압축·핵심 유지. **락.**
- **D5 (F-11)**: §3.5 코드명세절 부록 이전 + bib `\code` 평문화. **락.**
- **D6 (F-10 용어)**: `TERM_DECISION_TABLE` 기본 처분 락 — 요동→fluctuation·양성→positivity·음함수→implicit(병용 일관화)·섭동→perturbation·유일근→풀어쓰기·**준위→유지+병기**(축퇴 선례). 대정준/정준/분배함수·V1013 27+18 = **유지 확정**. 첫등장 병기·치환금지 5구역 준수. **락**(사용자 특정어 veto 가능).
- **정보성(재질의 아님)**: F-02 확률 P→p 는 rubric B5 "각주 가드" 선례와 갈리나 사용자 명시라 집행(1회 고지 완료). register honest-gap 은 FB3 전문 정독서 보강.

## Next
**FB1 — F-11 코드=부록 정리(전역·최우선), cumulative step 6.** 입력 = `INV_code_in_body.md`. 단위 = 파일 하나씩(gr2L→lcoomega→sifr→cases→blend Fig2→notation→§3.5→bib). 각 파일 정독→코드토큰 물리언어 치환/부록 이전→빌드→ledger. 재발 grep 게이트 신설.
