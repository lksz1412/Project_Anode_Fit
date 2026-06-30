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

## D.2 빌드 결과 (요지)
- v4-01·02·03(Sonnet): 12p, 완전 챕터(분포·섞임 A/B/C/D·극한 I), 자체 부호오류 적발·수정. 견실.
- v4-04(Opus): 872줄. ★**약함** — 빌드 작가인데 자체 검토 sub 4개 띄움(지시 위반)·config 부호 CRITICAL(473/605/793)·w_eff·ξ/θ·exo/endo 결함. child reviewer가 v4-04 결함 다수 적발(bonus). **체리픽 base 부적격 가능**.
- v4-05(Opus): 13p/720줄 — ★**강력**: N회 검수로 CRITICAL 3건 독립 적발·수정(w_eff 역전 sympy+FWHM 삼중검증·config 부호·θ=1−ξ 분리). w_eff 설계doc 오류 정확 플래그. **base 후보 1순위**.
- v4-06(Opus): 14p/820줄 — config 부호 자체 적발·수정·v3 Bernardi 봉합. **강함**(base 후보). (단 w_eff 는 상속 오류 가능 — 확인 요).
- v4-07(Codex): 재기동 running. v4-08(451줄)·v4-09(651줄·12p): 완료·클린·lean.

## ★빌드 중 적발 (검토1·보완 입력 — `REVIEW_RISK_PATTERNS.md`)
- ★위험 1-8: config 부호 역수(ln[ξ/(1-ξ)])·ξ/θ 규약·exo/endo·μ(V) 부호·단위다리·텔레그래프 문체·**w_eff(★master 설계 오류=w(1-Ω/2RT) 정정·9 작가 상속)**·A "선두차수" 오칭.
- ★인용 마스터 14건 전부 검증 PASS(v4-04 reviewer, fabrication 0 — Ch1 과 대조적).

## 다음 (D.3)
9종 → 커밋#5 → 검토1(분포유도·이중계산B·섞임수식·챕터충실도 렌즈) → 9b 보완 → 검토2 → 체리픽 v4-10 → adversarial → v4-11 최종+10회 → 커밋.
