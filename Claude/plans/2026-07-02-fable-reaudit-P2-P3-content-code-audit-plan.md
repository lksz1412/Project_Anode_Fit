# Fable 재검 — 챕터 2(내용 감사)·챕터 3(코드 적합성) 세부 계획서

> 마스터 = `2026-07-02-fable-reaudit-v12-master-plan.md`. Steps 13-24. result = `Claude/results/process/FABLE_REAUDIT_P2_P3_RESULT.md`. 감사 산출 = `docs/Fable_점검/FABLE_AUDIT_02_ch1ch2_content.md`·`FABLE_AUDIT_03_code_fitness.md`. 커밋+푸쉬 = phase 종료마다(main).

## ★챕터 1 교훈의 렌즈 주입 (전 감사자 공통)
1. **문건 서술 순응 금지** — 물리 자체를 독립 재유도로 검증(설계doc 순응 검수가 w_eff 오류를 2R 통과시킨 전례).
2. **실행 기반 렌즈 상설** — 수치로 확인 가능한 주장(폭·면적·극한·부호·계수)은 코드/스크립트 실행 실측.
3. **이전 판정 맹신 금지** — 기존 오적발/무결 판정도 재확인 대상(단 재검 근거 기록).
4. **코너케이스 과일반화 1급 렌즈** — 특정 극한 결과의 보편화 색출·단 코너 자체를 메인으로 끌어오지도 않기.

## Phase 2.1 — 기반 확정 (Step 13)
- 기반 = `docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex`(1821줄, v1.0.10과 byte 동일)·`graphite_ica_ch2_v1.0.11.tex`(750줄) + P1.1 supplement(`V1011_P11_map_v10.md`, 미편입 입력).

## Phase 2.2 — 내용 감사 실행 (Steps 14-18)
- 분산(무통신): C-1(Ch1 §서론~N3: 매핑·분극·중심·히스 + LCO center/hys)·C-2(Ch1 N4~N6: 폭·분포·broadening·전자엔트로피 + LCO gate/decomp)·C-3(Ch1 N7~N9+검산·LCO peak/code + supplement 대조)·C-4(Ch2 전체)·C-5(★이전 판정 재검: 오적발 6건·무결 판정의 재현성 — 독립 재유도) + **master(Fable) 직접 = 논리 spine 통독**(전 챕터 인과 사슬·Eyring 위상·비약/왜곡/연결 — CORE 판단).
- 렌즈: 물리 타당성(재유도)·논리 비약·왜곡·잘못된 연결·코너케이스 과일반화 + 위 교훈 4.
- Step 18: master 삼각검증(agent 적발 vs 실행 실측 vs 기록).

## Phase 2.3 — 문제 리스트 (Step 19)
- `docs/Fable_점검/FABLE_AUDIT_02_ch1ch2_content.md`: [등급]·위치(줄)·물리 근거·수정 방향·4-tier. gate = 전 절 coverage·항목별 재유도/실측 근거.

## Phase 3.1 — 코드 적합성 (Steps 20-23)
- C-6: Ch1/Ch2 결과식 ↔ `Anode_Fit_v1.0.11.py` **양방향 매핑표**(식→구현·구현→식) + 부호·차원·극한 실행 실측 + 문건-코드 갭(있으나 없는 것/없으나 있는 것). master 검증.

## Phase 3.2 — 코드 리스트 (Step 24)
- `docs/Fable_점검/FABLE_AUDIT_03_code_fitness.md`. gate = 양방향 완결·실행 로그 근거.

## 산출·규율
- 각 agent 출력은 `results/process/FABLE_REAUDIT_C{1..6}_note.md`(과정)·종합은 master가 docs/Fable_점검(영구). 원본 무수정. 커밋+푸쉬 phase말.
