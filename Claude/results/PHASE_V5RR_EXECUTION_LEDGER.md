# PHASE V5RR EXECUTION LEDGER (12-col)

> v5 전면 재검토. 기존 `PHASE_V5_EXECUTION_LEDGER.md` 불가침(별도).

| Step | Phase | Unit/Round | Action | Files | Read Range | Build | Defects(f/fx) | Lens/Chunk | Gate | Commit | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | R0 | baseline | overfull 2영역·§1.1 기호표·§1.4 spine 정독, §1.18 누출 grep | v5 | §1.1·§1.4·OF1·OF2 | err0/of2/undef0 40p | 0/0 (진단) | 구조·누출 | — | — | OF1/OF2 발견, 누출 0 |
| 2 | R0 | baseline | 매핑 sub: v5↔v3 식97 대응·★의존그래프·변동인벤토리 | v5,v3(read) | v5/v3 전범위 | — | 0/0 (매핑) | 대응·의존 | — | — | 97 verbatim, 약점3 지목 |
| 3 | R0 | baseline | baseline_map.md 작성 + §1.4 9edge spot-check | V5RR_baseline_map.md | — | — | 0/0 | 검증 | — | — | 그래프 본문 일치 ✓ |
| 4 | R0 | baseline | R0 result+ledger, Phase R0 commit | PHASE_V5RR_* | — | err0/of2/undef0 | 0/0 | — | R0 PASS | (본 커밋) | 미배정 0 |
| 5 | R1 | overfull | OF1 연쇄율식 분리·OF2 emergencystretch+분수분리 | v5.tex,preamble | §1.8·§1.17 | of2→0 | 2/2 | 빌드 | — | — | overfull 0 회복 |
| 6-10 | R1 | 절별 ×5 | 검수 sub A~E 병렬 head→tail(물리·화학·수리+보존+정합) | v5,v3(read) | §1.1~§1.17 전 | — | (지적 다수) | 절별 3렌즈 | — | — | 물리오류 0, 산문다리 손실만 |
| 11 | R1 | 삼각 | 확정수정 3: §1.8 dash→괄호·dHeff χ_d ref·Ifuse L_V ref. sub B L607 오타주장 기각 | v5.tex | §1.8·§1.15·§1.12 | 0/0/0 40p | 3/3 | 삼각검증 | — | — | false positive 1 거름 |
| 12 | R1 | gate | R1 result+ledger, Phase R1 commit | PHASE_V5RR_* | — | 0/0/0+15/15 | — | — | R1 PASS | (본 커밋) | — |
