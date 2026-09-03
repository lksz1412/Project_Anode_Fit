# audit_checklist_r3 — Phase 1.1 Step 1 OUT-INV 검수 라운드 3 (iter_3b · 2026-09-03)

> master → 검수 sub(라운드 1·2 와 동일 sub). 대상 = **iter_3/3b OUT-INV**(`Claude/results/V1027_HISTORY_INVENTORY.md`, 1,675행 · 등재 730/110,253) + 마스터 플랜 v5.4(814행) + `iter_3/policy_check.txt` + Step 1 이력(`Claude/results/Step 1 — 인벤토리 파일 생성(OUT-INV).md`, 갱신본). 출력 = `iter_3/audit_log_r3.md` 1본. 5항목 고지·금지 = 라운드 1 지침 §0·§4 동일.

## 1. 렌즈(라운드 3 = regression · 완결성 · 적대검산(스크립트 재현))

- **regression** — iter_3/3b 변경 지점(OUT-INV §10.4 표 · (iv-c)·(vii-b)·(ix-b)·(xvii-b)·(xvii-c)·(viii-c) 6블록 · (i-b) 이동·귀속 통일 · (vii) 행 74 · §2·§3.1·§8.3 재생성 · §10.1 시제 · 계획서 v5.4 8곳)이 새 결함을 들였는가 — 표 서식 · 합계 산식(730/110,253 · 1,921/604,865) · 라운드 2 발견 10건 반영 O/X 대조 · 계획서 잔존 패턴 재 Grep(`지원 4본`·`91 계획서`·`INDEX 401`·`89행`·`ch1_appD_si.tex = orphan`·`722 파일`).
- **완결성·적대검산** — `iter_3/policy_check.txt` 를 **독립 재현**한다: (a)(c) 정규식 28종을 네가 TSV 에 다시 돌려 S(§1 집합 ∪ v1.0.25 tex 60) 대조 → 잔여 0 인지 · (b) 통제 문서 5본 토큰 추출 → TSV 해소 → S 대조 → 잔여 0 인지(제외 규칙이 정책 문안과 일치하는지 · 제외로 빠진 항목 중 "이력·결정 근거" 성격이 있는지 최약점으로 지목) · 정책 문안 (a)(b)(b′)(c) 가 §10.4·policy_check·(iv-c) 정의에서 동일 문자열인지 · 신규 등재 39본(iter_3 31 + iter_3b 8)의 버전 귀속·문서 종류 어휘·비고 근거 path:line 실물 대조(표본 ≥12, 특히 (xvii-c) 6본의 `docs/INDEX.md` 인용 행·(vii-b) CHARTER 인용 행·(viii-c) `INDEX_v25.md` 인용 행) · 버전 귀속 값 집합 이표기 잔존(라운드 2 의 2쌍 해소 여부 + 신규).
- **usable(경량)** — Step 2 배정표 입력으로서: DQ-16 후보 풀이 §8.3·§10.4 에 목록 수준으로 있는지 · 고유본/사본 열이 신규 39본에도 규칙대로인지(hash 동일 사본이 있는 (viii-c) 2본 표기).

## 2. 청크 경계(라운드 1·2 와 다르게)

역순 3청크: ⑦'=§8~§10(끝→앞) → ⑤'=§2~§7 → ①'=§0~§1(신규 블록 6개 우선, 그 다음 iter_1 표는 표본). 계획서 = v5.4 정정 지점 8곳 Read + 잔존 Grep.

## 3. 출력(`iter_3/audit_log_r3.md`)

헤더 · 발견 표(AUD-R3-nn · 심각도 · 4-tier · 위치 · 재현 · 제안) · 라운드 2 발견 10건 반영 대조 · policy_check 독립 재현 수치 표 · 계획서 잔존 grep 표 · 최약점 1곳 · Read Coverage · 판정(확정결함 n → "라운드 3 확정결함 0(수렴 1R)" / "master 수정 필요").
