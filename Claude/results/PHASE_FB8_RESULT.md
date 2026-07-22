# Phase FB8 — 어조 강화: 차가운 교과서 register 최대화 Result

## Summary
사용자 직접 지시 **"이 차가운 교과서 적인 어조가 내 목표한 것이다. 더 강화해야 할 일이지 완화시키면 안 된다"** 에 따른 register **강화(maximization)** 패스. 앞선 v19·v23·v24 비교(FB 마감 후)에서 관찰된 "어투 평탄화"는 **의도된 목표**로 확정 — 음성 복원 후보 전량 철회. FB8 = 남은 은유·의인·구어·비형식 정의어를 물리량·중립 서술로 치환. **집행 = prose register 한정**(정의어 rename 20행 + 구 은유/구어 7건). **★ 장식 마커(55개)는 P5 기호-보존 조항 + load-bearing 상호참조 앵커 사유로 미집행·`추가 후보` 등재.** 물리·식번호·label·주석·코드 불변.

## Step Range
cumulative **FB step 47–51** (FB7 마감 후 사용자 재개 지시로 FB 계열 재기동).

## Inputs
- 사용자 지시(2026-07-22): 차가운 교과서 어조 = 목표 → 강화(완화 금지).
- 앞선 산출: `comp_v24/VERSION_COMPARISON_v19_v23_v24.md`(어투 평탄화 = 의도 확정).
- 문건 전수: `docs/v1.0.24/_sections/*.tex`(register offender 스캔).
- 게이트: F-04 register 정책·V1020_STYLE_RUBRIC·F1 식번호/label·주석 불변·코드 sha256 f230f59b.

## Files Created
- `PHASE_FB8_RESULT.md`(본 문서).

## Files Updated (12 tex)
**정의어 rename(은유/의인 제거 — 8 파일, 20행):**
- `생존 지도`(survival map) → `대응 지도`(correspondence/mapping) ·`생존 판정(표)` → `대응 판정(표)`
- `정직 공백`(honesty gap) → `미결 공백`(unresolved/pending)
- 파일: `ch1_appD_si`·`ch3v22_notation`·`ch3v22_sec00_intro`·`ch3v22_sec01_map`·`ch3v22_sec02_cases`·`ch3v22_sec03_blend`·`ch3v22_sec04_mech`·`ch3v22_sec05_code`.

**구 은유/구어 중립화(6 파일, 7 편집):**
| 파일:행 | old | new | 사유 |
|---|---|---|---|
| ch1_sec02b_part0:412 | 되밟는다 | 재현한다 | 걷기(tread) 은유 → "재현"(reproduce) |
| ch1_sec02b_part0:471 | 다시 밟는다 | 다시 따른다 | 걷기 은유 → "따른다"(follow the ladder) |
| ch1_sec07_broadening:291 | 되살리는 | 복원하는 | 의인(revive) → 복원(restore) |
| ch1_sec15_lcoelec:123 | 기여가 살아 | 기여가 남아 | 생명 은유(survive) → 남다(remain) |
| ch2_sec05_mixing:167 | 비틀어 | 조정해 | 구어/물리 은유(twist) → 조정(modify) |
| ch3v22_sec04_mech:77 | 값을 밟는다 | 값을 취한다 | 걷기 은유 → 값을 취한다(takes value, 물리 표준) |
| ch3v22_sec03_blend:231 | 정말 | 실제로 | 구어 강조(really) → 실제로(actually) |

- `V1024_FEEDBACK_EXECUTION_LEDGER.md`: FB8 행 PASS.

## Read Coverage
- register offender 전수 grep(은유/구어/simile 토큰): 되밟/밟/살아/살리/비틀/정말/마치/셈이다/그냥/진짜 등.
- ★ 마커 55개 전수 용법 분류(본문 lead-in 장식 vs 상호참조 앵커 vs % 주석).
- 정의어 rename 후 body/comment 분리 카운트(old body=0 검증).

## Execution Evidence
```
게이트 1 old 은유/정의어 BODY grep (% 주석 제외) = 0 (10 토큰 전부):
  되밟는다·다시 밟는다·되살리는·기여가 살아·비틀어·값을 밟는다·정말 공통·생존 지도·생존 판정·정직 공백 = 0
게이트 2 신규어 정착: 대응 지도=11·미결 공백=8·재현한다(신1+기존7)·다시 따른다=1·복원하는=1·값을 취한다=1·실제로 공통=1
게이트 3 invariant (paired-token diff): \label/\eqref/\ref/\cite 키 변경 = 0 · % 주석 변경 = 0 · 식 환경(equation/multline/align) 변경 = 0
게이트 4 빌드 GREEN: ch1 0-err/97p · ch2 0-err/30p · ch3 0-err/21p · undefined ref/cite = 0
  (undefined 3/2/3 = 전부 "Font shape TU/UnBatang·D2Coding /it undefined" italic fallback, 선재·무해)
게이트 5 주석 동결 sanity: ch1_appD_si:88 자산 "노드 생존 판정표" 주석 그대로 보존(본문만 대응 판정표)
게이트 6 코드 불변: Anode_Fit_v1.0.24.py sha256 f230f59b (FB8 = 문건 한정)
```

## ★ 장식 마커 — 추가 후보 (미집행, P5 governance)
차가운 교과서 register 관점에서 본문 `\textbf{★...}` 주의/lead-in 장식(★단위 환산·★부호 규약·★직접 엔트로피 경로 등)은 제거 후보다. **그러나 미집행 — 사유:**
1. **P5 조항** — "기존 변수명·함수명·기호·라벨·한글 표현은 사용자가 바꾸라고 하지 않으면 임의 변경 X". ★는 문건 전반에 일관 적용된 기존 저작 **기호(notation system)**.
2. **Load-bearing 상호참조 앵커** — 일부 ★는 장식이 아니라 비형식 참조 앵커: `ch1_sec04_hys:111 "★Taylor 전개의 함정"` ↔ `:219 "본문 ★Taylor 전개의 함정"` 역참조 · `ch1_sec14:77 "위 ★이중계산 금지"` · `ch2_sec03_vibel:99 "★이중계산 warnbox"`. 한쪽만 제거 시 참조 깨짐.
3. **규모·리스크** — 55개/20파일 대량 기계 변경(앵커 정합 회귀면 큼).
4. **성격** — ★는 prose register(은유/구어)가 아니라 **typographic 장식** — FB8 prose 강화 mandate와 경계가 다름.

→ **P5 "추가 개선 후보는 실제 수정하지 말고 `추가 후보`로 보고" 준수. 사용자 판단 대기.**
집행 시 옵션: (a) 전량 제거(앵커 3쌍은 대체 참조어 병행) · (b) 앵커만 유지·순수 장식만 제거 · (c) 현행 유지.
Note: `%` 주석 내 ★(자산 C-xx 다수)는 렌더 안 됨·invariant 보호 대상 → register와 무관·제외.

## Validation (게이트별)
- **old 은유/정의어 body 0** — PASS(10 토큰 grep=0).
- **invariant(키·주석·식 환경 변경 0)** — PASS(paired-token diff 0 · % 0 · eq env 0).
- **빌드 GREEN 97/30/21** — PASS(0-err · undefined ref/cite 0 · 페이지수 불변).
- **주석 동결** — PASS(appD:88 자산 주석 보존).
- **코드 bit-exact** — PASS(sha256 f230f59b).
- **★ P5 governance** — PASS(미집행·추가 후보 등재, 사용자 판단 경계 명시).

## Gate
**PASS_FB8_REGISTER_MAX** (구 은유/의인/구어 7건 + 정의어 rename 20행 중립화 · body old-term 0 · invariant 4종 불변 · 빌드 GREEN 97/30/21 · 코드 sha256 불변 · ★ 마커 P5 준수 미집행·후보 등재).

## Confirmed Non-Changes
- 코드 `.py` 무변경(sha256 f230f59b) — FB8 문건 한정.
- 식번호·`\label` 정의·`\eqref`/`\ref`/`\cite` 키·`%` 주석·식 환경 불변(paired-token diff 검증).
- 페이지수 97/30/21 불변(순수 어휘 치환, 길이 변동 없음).
- ★ 장식 마커 55개 불변(P5 추가 후보 — 미집행).
- Codex/ 영역 read/write 없음.
