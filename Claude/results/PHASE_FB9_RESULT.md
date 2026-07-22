# Phase FB9 — ★ 장식 마커 전량 제거 (사용자 opt-a) Result

## Summary
FB8 에서 `추가 후보`로 남긴 **★ 장식 마커**를, 사용자 명시 지시 **"a로 진행"**(전량 제거)에 따라 집행. 사용자 지시로 P5 기호-보존 조항 해제. **본문 ★/$\bigstar$ 57개 전량 제거**(22 파일), **주석(`%`) 내 ★ 34행 전량 동결**(invariant). 핵심 설계: **균일 제거** → 앵커 3쌍(정의부↔참조부)이 동시에 ★를 잃어도 굵은 구(phrase) 헤더로 참조가 정합 유지되므로 별도 대체 참조어 불필요. 물리·식번호·label·주석·코드 불변.

## Step Range
cumulative **FB step 52–55**.

## Inputs
- 사용자 지시(2026-07-22): FB8 ★ 후보 옵션 (a) 전량 제거 승인.
- 대상: `docs/v1.0.24/_sections/*.tex` 본문 ★/$\bigstar$.
- 스크립트: `scratchpad/strip_stars.py`(주석 동결·(★ 공백 정리·bigstar thin-space 제거).
- 게이트: F1 식번호/label·주석 불변·코드 sha256 f230f59b.

## Files Created
- `PHASE_FB9_RESULT.md`(본 문서).

## Files Updated (22 tex — 본문 ★/$\bigstar$ 제거)
ch1: `appD_si`(2)·`sec02a_part0`(1)·`sec02b_part0`(1)·`sec04_hys`(2)·`sec05_width`(1)·`sec05b_gr2L`(1)·`sec07_broadening`(3)·`sec11_lcointro`(2)·`sec12_lcocenter`(3)·`sec13_lcohys`(5)·`sec14_lcodecomp`(7)·`sec15_lcoelec`(11)·`sec17_msmr`(2)·`ch1v22_bib`(1)
ch2: `sec01_partition`(2)·`sec02_config`(1)·`sec03_vibel`(1)·`sec04_einstein`(1)·`sec05_mixing`(6)·`sec06_limits`(1)·`sec07_revheat`(1)
ch3: `sec01_map`(2, $\bigstar$)
합계 **57 제거** / 22 파일.
- `V1024_FEEDBACK_EXECUTION_LEDGER.md`: FB9 행 PASS.

## Read Coverage
- ★ 전수 인벤토리: body 57(non-comment) vs comment 34(frozen) 분리, `\bigstar` 2건 포함, 물리 `\star`(⋆) = 0(배제 확인).
- 앵커 3쌍 정의부/참조부 매핑: hys 111↔219(Taylor 전개의 함정)·mixing 91↔87(수치 검증 박스)·sec14 71↔16(가법성 정당화)·sec14 70↔77(이중계산 금지)·vibel 99(이중계산 warnbox).
- 스페이싱 민감 케이스: einstein:80 `(★ $F_\vib$`·bib:40 `[★Chapter 1...]`·appD:48 `이월★`·map:79/85 `$\bigstar$\,\S\ref`.

## Execution Evidence
```
스크립트 규칙(비주석 행만): $\bigstar$\, 제거 → $\bigstar$ 제거 → "(★ "→"(" → "★" 제거
집행: body ★/bigstar 57 제거(22 파일) · comment stars before=36 after=36 (UNCHANGED)
게이트 1 body ★/bigstar 잔여 = 0
게이트 2 comment ★/bigstar 잔여 = 34행 (동결 확인)
게이트 3 invariant paired-token: \label/\eqref/\ref/\cite 키 변경 = 0 · % 주석 변경 = 0 · 식 환경 변경 = 0
게이트 4 spacing-artifact scan(추가행 double-space·"( "·"{ ") = 0
게이트 5 앵커 정합: def \textbf{Taylor 전개의 함정}↔ref 본문 Taylor 전개의 함정 · def \textbf{이중계산 금지}↔ref 위 이중계산 금지 · 전부 phrase 정합
게이트 6 스페이싱: einstein:80 "로 두면($F_\vib$ 는"(stray space 없음) · map:79 "& \S\ref{sec:si-mech}"(clean)
게이트 7 빌드 GREEN: ch1 0-err/97p · ch2 0-err/30p · ch3 0-err/21p · undefined ref/cite = 0
게이트 8 코드 불변: Anode_Fit_v1.0.24.py sha256 f230f59b
```

## 앵커 처리 방식 (설계 노트)
★는 `\label`/`\ref` 기제가 아니라 굵은 구(phrase) 헤더에 얹힌 장식이었다. 따라서:
- 정의부 `\textbf{★X}` → `\textbf{X}` (여전히 굵은 헤더 — 시각적 앵커 유지)
- 참조부 `본문/위/아래 ★X` → `본문/위/아래 X` (구 이름으로 헤더를 계속 가리킴)
→ **동시 제거가 자기정합**. 한쪽만 제거할 때만 참조가 깨지므로, 전량 균일 제거가 오히려 최안전. FB8 후보 노트의 "대체 참조어 병행"은 phrase 헤더가 그 역할을 이미 수행하므로 불요(중복 포인터 추가 안 함 = 최소 변경).

## Validation (게이트별)
- **body ★ = 0** — PASS.
- **주석 ★ 동결(34행)** — PASS(before=after).
- **invariant(키·주석·식환경 변경 0)** — PASS.
- **spacing-artifact 0** — PASS(einstein `(★ ` 케이스 clean).
- **앵커 3쌍 정합** — PASS(phrase 헤더 유지).
- **빌드 GREEN 97/30/21** — PASS(undefined ref/cite 0).
- **코드 bit-exact** — PASS(sha256 f230f59b).

## Gate
**PASS_FB9_STAR_REMOVAL** (본문 ★/$\bigstar$ 57 전량 제거 · body 잔여 0 · 주석 34행 동결 · invariant 4종 불변 · 앵커 3쌍 phrase 정합 · spacing-artifact 0 · 빌드 GREEN 97/30/21 · 코드 sha256 불변).

## Confirmed Non-Changes
- 코드 `.py` 무변경(sha256 f230f59b) — FB9 문건 한정.
- 식번호·`\label` 정의·`\eqref`/`\ref`/`\cite` 키·`%` 주석(★ 34행 포함)·식 환경 불변.
- 페이지수 97/30/21 불변(순수 인라인 마커 제거).
- Codex/ 영역 read/write 없음.
