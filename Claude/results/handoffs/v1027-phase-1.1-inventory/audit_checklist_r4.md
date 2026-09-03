# audit_checklist_r4 — Phase 1.1 Step 1 OUT-INV 검수 라운드 4 (iter_4 · 2026-09-03) — 수렴 판정 라운드

> master → 검수 sub(라운드 1~3 동일 sub). 대상 = **iter_4 OUT-INV**(`Claude/results/V1027_HISTORY_INVENTORY.md`) + 마스터 플랜 v5.4(각주·수치 추기, 815행) + `iter_3/policy_check.txt`(iter_4 최종판) + Step 1 이력(갱신본). 출력 = `iter_4/audit_log_r4.md` 1본. 5항목 고지·금지 = 라운드 1 지침 §0·§4 동일. 라운드 3 이 확정결함 0 이었으므로 본 라운드가 확정결함 0 이면 **연속 2R 수렴**이다 — 그러나 refute mandate·최약점 1곳·빈 통과 금지는 그대로다.

## 1. 렌즈(라운드 4 = regression 집중 + 완결성 재현)

- **regression** — iter_4 변경 지점(OUT-INV §10.5 표: (xvii-c) 6행·(viii-c) 2행 비고 교체 · (iv-c) 행 18~21 :line · (ix-b) 행 1 4-tier · §0 규칙 2곳 · (iv-c) 정의 참조화 · §10.4 정책 문안 정본 교체 · (vii-c) 신설 8행 · §2 · §8.3 재생성 · §10.4 합계 문장 · §10.5 · 계획서 §2.8 각주·Assumptions 11·v5.4 행 추기 · Step 1 이력 갱신)이 새 결함을 들였는가 — 특히 `rep_note` 방식으로 교체한 12행의 표 열 수(7열/8열)·구분자 깨짐 · 라운드 3 발견 10건 반영 O/X.
- **완결성(재현)** — `policy_check.txt` iter_4 판을 독립 재현(28종 + FITTING_GUIDE hash 그룹 검사 + (b) 5본 → 잔여 0) · 합계 738/111,107 · 미등재 1,913/604,011 · (vii-c) 8본이 hash 4그룹 고유본 + 단독 4 와 일치하는지 §4 #1·#110·#132·#146 대조 · 정책 문안 3곳(§10.4·(iv-c) 참조·PC) 동일/참조 관계.
- **usable(경량)** — 버전 귀속·문서 종류 값 집합에 §0 규칙 밖 값이 남았는가(iter_4 규칙 추가 후) · 신규 표기 고유본/사본 정규식 파싱.

## 2. 청크 경계(라운드 1~3 과 다르게)

절 단위 랜덤 순서: §10 → (vii-c)·(xvii-c)·(viii-c)·(ix-b)·(iv-c) 변경 행 → §0 → §2·§8.3 → 나머지는 표본(iter_1 표 각 군 3행). 계획서 = 변경 3곳 Read + 잔존 grep 1회.

## 3. 출력(`iter_4/audit_log_r4.md`)

헤더 · 발견 표(AUD-R4-nn) · 라운드 3 발견 10건 반영 대조 · 재현 수치 표 · 최약점 1곳 · Read Coverage · 판정("라운드 4 확정결함 0 → 연속 2R 수렴" / "master 수정 필요").
