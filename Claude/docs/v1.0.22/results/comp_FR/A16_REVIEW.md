# A16_REVIEW — §18 입력 규정 + 부록 A/B/C/D (ch1_graphite_v1.0.22 빌드)

- 검토 창: FR-A16 (BRIEF_FR_A.md 규율 준수 — 보고 전용·소스 수정 금지·git 조작 금지·Codex/ 접근 금지)
- 대상(전문 정독 완료):
  - `_sections/ch1_sec18_inputs.tex` (§18 전체 입력 인자와 피팅 준비, 69행)
  - `_sections/ch1_appA_signcheck.tex` (부록 A 부호 사슬 검산표, 89행)
  - `_sections/ch1_appB_codemap.tex` (부록 B 곡선 계산 구현 대응표, 157행)
  - `_sections/ch2_appA_traps.tex` (부록 C 열특성 기호·부호 함정 검산표, 75행)
  - `_sections/ch2_appB_codemap.tex` (부록 D 열특성 코드 요구명세, 75행)
- 검토 4관점: ①내용 보완 ②논리 오류(재계산·재유도 검증) ③더 쉬운 설명 ④산문→수식 간결화
- 상태: 진행 중 (조기 저장 — 발견 1건 검증 완료 시마다 즉시 append)

## 발견 표

| ID | 파일:행 | 유형 | 등급 | 현행(축자) | 제안(완성 LaTeX) | 근거 |
|----|---------|------|------|-----------|-----------------|------|
