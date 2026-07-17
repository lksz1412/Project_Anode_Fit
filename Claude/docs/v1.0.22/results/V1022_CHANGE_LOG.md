# V1022 CHANGE LOG — 변경 통제 대장

> ID: **S-###**(구조 재편 — 이동·조립·인프라) · A/R/C/E/B-### = v1.0.21 체계 연속. baseline = snapshot_v1022_r1.json.
> 재편 원칙: 이동이지 재작성 아님 — 산문 변경은 R2+ 소관, R1 은 조립·인프라만.

| ID | phase | 파일 | 내용 | 구조 영향 |
|---|---|---|---|---|
| S-001 | R1 | 마스터 3본(신규)·구 마스터 미복사 | 활물질별 재편: Ch1(흑연 곡선 §0~10+Part T 열특성[구 Ch2 전량]+§18 입력+부록 4본)·Ch2(LCO=구 Part II §11~17)·Ch3(Si=구 appD 승격) — 섹션 파일명 불변(자산·이력 보존) | 마스터 체계 교체 |
| S-002 | R1 | common_preamble_v1022.tex(신규) | preamble 통합(ch1∪ch2 — 내용 매크로 충돌 0 검증)·xr-hyper 로드·항법 토글 제거(D22-1) | 인프라 |
| S-003 | R1 | 드라이버 3본 | 장별 번호 N.x·xr 외부참조(Ch1↔Ch2 양방향[전방 참조 22곳 유지]·Ch3→Ch1/Ch2)·빌드 순서 규약(ch1→ch2→ch3→ch1 재패스) | 인프라 |
| S-004 | R1 | ch1v22_partT_divider(신규)·ch2_sec00_intro(TOC 제거)·ch1_sec00/ch2_sec00(구 nav 블록 제거) | Part T 구분면+다리 문단(R2 이음매 확정 대상)·중복 TOC 해소·항법 잔재 제거 | 산문 최소(다리 1문단) |
| S-005 | R1 | ch2v22_sec00_intro·ch3v22_sec00_intro·ch2v22_notation·ch3v22_notation(신규) | 장 서두 2본(추가 텀 방식 선언/생존 지도 개관)+계승 2단 기호표 초판 2본(재정의 금지 규약) | 신규 산문 4소절 |
| S-006 | R1 | ch{1,2,3}v22_bib.tex(신규)·구 bib 2본 미복사 | 장별 참고문헌 자동 분할(cite 스캔 — 39/14/14·누락 0)+구 bib 자산 주석 블록 복원(27 앵커) | bib 재편(자산 357/357) |
| S-007 | R1 | results/tools_check_structure.py | unresolved 판정을 전 마스터 라벨 합집합 기준으로 패치(장 간 xr 참조 설계 반영 — 헤더 기록) | 도구 |
| (R1 비고) | R1 | — | multiply 경고 화이트리스트 = LastPage·swiderska2019(xr 산물 — 장별 bib 중복 수록 의도). 병합 시 externaldocument 제거로 자연 해소(MERGE_READINESS 소관) | — |
