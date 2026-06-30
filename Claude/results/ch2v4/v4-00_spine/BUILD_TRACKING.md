# Ch2 v4 — 빌드 추적 (컴팩션-안전)

> Track 2. base = v3(265줄 Bernardi survey) → 통계열역학 챕터(분포 명시). Claude=알림 / Codex=폴링.

## Phase C 설계 ✅
- C.1 `research/CH2v4/41_statmech_spine.md`(분배함수→점유분포→config/vib/electronic).
- C.2 `research/CH2v4/40_mixing_term_design.md`(A 겹침가중·B 이중계산·C w_eff(Ω)·D 히스·I 극한).
- ★A 수치검증 `research/CH2v4/42_numerical_verification.md`: 완전식(겹침+config) FD 0.000 mV/K 일치(175점)·계단0·config 자동발산 = **PASS**.

## Phase D.2 9 작가
| 작가 | 모델 | job-id |
|---|---|---|
| v4-01 | Sonnet | a1b8027094167bfcc |
| v4-02 | Sonnet | a9dade0b4854ae26f |
| v4-03 | Sonnet | aab059357c3214bdc |
| v4-04 | Opus | a96543d7d381568e7 |
| v4-05 | Opus | aa162f0c84e1de5f4 |
| v4-06 | Opus | a514c1afd9aae7802 |
| v4-07 | Codex | task-mqzzdswt-ak3lwg |
| v4-08 | Codex | task-mqzze5a6-w9nykk |
| v4-09 | Codex | task-mqzzelda-fgmzlx |

## 다음 (D.3)
9종 → 커밋#5 → 검토1(분포유도·이중계산B·섞임수식·챕터충실도 렌즈) → 9b 보완 → 검토2 → 체리픽 v4-10 → adversarial → v4-11 최종+10회 → 커밋.
