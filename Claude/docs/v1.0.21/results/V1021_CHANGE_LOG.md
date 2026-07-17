# V1021 CHANGE LOG — 변경 통제 대장 (구조 diff 와 1:1)

> 규칙(승계): 매 phase 종료 시 `tools_check_structure.py diff` 의 라벨/eqblock/자산/서지 변화가 본 대장과 1:1 로 설명돼야 PASS. 무라벨 블록은 file:line 키 — 행 이동 시 ±로 보이므로 해시 동일성으로 판별.
> ID 체계: **A-###**(확장 신규 — 절·식·그림·표 추가) · **R-###**(그림 반영 — FIGS_PICK_JUDGMENT §D 집행) · **C-###**(서지 — v1.0.20 에서 연속, C-020부터) · **E-###**(ERRATA — v1.0.20 에서 연속, E-002부터; v1.0.20 동결 후 발견 결함 포함) · **B-###**(보강 — B-010부터).
> baseline = `snapshot_v1021_q0.json` (v1.0.20 final 과 구조 동일 — Q0 은 복제·버전 표기만, eqblock/라벨/자산 변화 0).

| ID | phase | 파일 | 내용 | 구조 영향(라벨/eqblock/자산/bib) |
|---|---|---|---|---|
| (Q0) | Q0 | 마스터 3본·preamble 2본·코드 2본 | 골격 복제·현행 버전 표기만 갱신(자산 태그 V20-* 이력 표지 보존) | 없음(±0) |
| A-001 | Q2 | ch1_sec02b_part0.tex | **다클래스 lattice gas 신설 소절**(sec:sm-mc, sec:sm-electro↔sec:sm-macro 사이) — (a)전이=자리 클래스 (b)클래스곱 인수분해 (c)용량가중 점유합 (d)전하 보존 음함수 식별 boxed + verifybox(요동 양성→유일근·N_p=1 회수·부호 읽기·이중웰 가드). 체리픽: q2f1 베이스+q2f2 유일근 완결형+q2o1 근사 경계. D21-5 요동–응답 축 합류(eq:sm-mc-fluc=eq:sm-flucres 거시판) | 라벨 +5(sec:sm-mc·eq:sm-mc-{factor,occ,balance,fluc})·eqblock +4(boxed 1)·자산 주석 V21-Q2-01~04 |
| A-002 | Q2 | ch1_sec02b_part0.tex | keybox "Part 0 사다리"에 다클래스 반전 계단 삽입(logistic→**다클래스 반전**→Nernst) | eqblock ~0(키박스는 비수식 환경) |
| A-003 | Q2 | ch2_sec05_mixing.tex·ch2_appB_codemap.tex | Ch2→Ch1 연결 문장 각 1(eq:implicit=대정준 제약 반전·solve_U_oc 유일근=요동 양성 보증; 서술형 참조 — 라벨 하드코딩 없음) | 없음(산문 2문장) |
