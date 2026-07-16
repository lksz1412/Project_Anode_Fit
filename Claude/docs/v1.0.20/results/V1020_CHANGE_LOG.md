# V1020 변경 통제 로그 — 물리적 변경(보강·ERRATA) 전수 등재부

> 규칙([D11′], 마스터플랜 §2): **물리 내용에 닿는 모든 변경은 편집 전 여기 등재.** 스냅샷 diff(eqblocks ±~)의 전 항목이 본 로그와 1:1 대응해야 gate PASS. 표현·문장 다리·인용 부여는 phase RESULT 의 Files Updated 로 갈음(여기 등재 X — 단 수식·수치·부호에 닿으면 등재).
> 종류: **보강**(신규 식·유도·배경 추가 — 기존 물리 불변) / **ERRATA**(기존 물리 오류 정정 — 코드 영향 판정 필수) / **서지정정**(bibliography 필드 정정 — 물리 무관).

## 등재부

| ID | 종류 | 위치(파일:라벨) | 구판 요지 | 신판 요지 | 근거(재유도/문헌) | 코드 영향 | Phase |
|---|---|---|---|---|---|---|---|
| C-001 | 서지정정 | ch1_bib:ml2024 | JMPS 190, **105727**·DOI …105727·Teichert 제1저자(arXiv판 순서) | **105726**·DOI 10.1016/j.jmps.2024.105726·출판판 저자 순서(Faghih Shojaei 제1) — 기재 DOI 는 실재하는 타 논문을 가리키던 위험 유형 | Crossref 105726/105727 대조 + master 독립 재검증(WebSearch) | 무 | P1 |
| C-002 | 서지정정 | ch1_bib:leviaurbach1999 | 제목이 별개 논문(JEAC 421, 79, 1997)의 것과 혼합 | 제목을 실제 1999 리뷰("Frumkin intercalation isotherm — a tool …: a review")로 교체·쪽 167–185 보완(서지·DOI 는 원래 리뷰 것 유지 — 인용 취지[내재 평형 폭·Frumkin] 부합 정정안 a) | Crossref + master 독립 재검증 | 무 | P1 |
| C-003 | 서지정정 | ch1_bib:ohzuku1993 | 제목 무표시 절단 | 출판 제목 전문 복원("…and Their Application as a Negative Electrode for a Lithium Ion (Shuttlecock) Cell") | Crossref | 무 | P1 |
| C-004 | 서지정정 | ch1_bib:msmr2024 | 제목 "(MSMR)" 삽입·Part I 표기 | 출판 표기 복원(Part 1·삽입어구 제거)·병기 Part II 권·아티클 103505 보완 | Crossref | 무 | P1 |
| C-005 | 서지정정 | ch2_bib:msmr_partI | 아티클번호 미기재 | 023502 보완 | Crossref | 무 | P1 |
| C-006 | 서지정정 | ch2_bib:msmr_partII | 제목 "MSMR" 축약·구두점 상이·아티클 미기재 | 출판 제목 전문·103505 보완 | Crossref | 무 | P1 |
| C-007 | 서지정정 | ch2_bib:hysteresis2018 | 쪽 미기재 | 179–184 보완 | Crossref | 무 | P1 |
| C-008 | 서지정정 | ch1_bib 헤더 주석 | "서지 — 24종"(stale) | "28종" + 검증 원장 참조 | 실측 카운트 | 무 | P1 |

## ERRATA 요약 (P8 코드 영향 판정 원장)
- (없음 — P0 시점)
