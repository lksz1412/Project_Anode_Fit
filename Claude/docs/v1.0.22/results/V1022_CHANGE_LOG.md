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
| S-008 | RA/R1b | ch1_sec00_intro·ch1_sec10_sum(×2)·ch1_sec14_lcodecomp·ch1_sec18_inputs·ch2_appA_traps(×2) | 구획 전환 명백 오문 7곳 정정(재편 산물 — R1b 스윕 검출): ①서론 세 층 서술 신 구조화(Part 0→I→T+Ch2/Ch3 안내) ②§10 말미 Part T 예고+LCO=Ch2 ③④appA "별도 컴파일 객체" 2곳→같은 문서/별개 장 사실 정정 ⑤§14 스코프 "Chapter 2 가"→"Chapter 1 Part T 가" ⑥§18 말미 흑연 장 결과 사슬+LCO 행 지위 ⑦§10 verifybox "Chapter 2 의 계산 예제"→"Part T 의 계산 예제(\S\ref{ssec:worked})". 잔여 분류 = results/R1B_SWEEP_LIST.md(T1 20·T2 53·T3 5·L1 1 → R2/R3 본안·W 29 어휘) | 산문 정정 7곳(수식·라벨 무변경) — 재빌드 GREEN·aux 불변·구조 PASS |
| S-009 | R2 | _sections 19파일(Part I·Part T·부록·divider) | **구획 전환 집행**(SEAM_PLAN 78행 + W 20행 — O-A 초안·마스터 집행): T1 20(구 "Chapter 2" 열특성 지칭→Part T live \S\ref/\eqref)·T2 53(구 "Chapter 1"→Part 0/I live·자기 구지칭→본 파트)·T3 5(구 Ch1 LCO 절→**Chapter 2 xr** 장 간 참조)·서술형 "(eq:…)"→\eqref 7·W 어휘 20(본 장 18·본 파트 1·본서 1[doc-leads]) + ch2_sec00_intro/ch2_sec10_closing 장→파트 격 개작(제목 "서/Part T 맺음"·§18 다리 문장— 자산 C-1~8·C-117~119 보존)+divider 다리 확정(폭 서식 live 참조). 재현 선언 3곳 "본 장" 동치 판정(W_RULE §4 — 곡선 재현 자기완결 근거) | 산문 지칭 계층 ~100곳(논지·수식 무변경)·소절 제목 2·캡션 3(TOC/LoF/LoT 갱신) — 잔존 스윕 clean(Chapter 1/그 문건/본 문건 0·Chapter 2 잔존 9 전건 정당) |
| S-010 | R2 | ch2_appA_traps·ch2_appB_codemap·ch1_appA/appB(제목)+파급 5곳 | **부록 letter 충돌 해소**(MISC Option 2): 열특성 부록 하드코딩 "부록 A/B"→**부록 C/D**(중복·프로세 오도 해소)+라벨 신설(sec:traps-thermal·sec:codemap-thermal, \phantomsection)+내부 B.1~B.4→D.1~D.4+파급 정정 5곳(sec04 ×2·sec07·sec08·ch1_appB:135[SEAM 보류 #1 해소])+곡선 부록 제목 "곡선" 접두 분업 | TOC 표기·부록 체계(내용 무변경) |
| A-011 | R2 | ch1_sec07_broadening | **CLT 종형 bgbox**(O-C 채택 — DIRECTION (iii)): eq:ensavg 문단 뒤, ρ(η) Gaussian 형상의 중심극한정리 근거+분산 가법 σ_η²=Σσ_ηk² 재유도+Lindeberg 한정+quenched/annealed 구분+회수 검산(m=1·ρ→δ)+가드 4종(forward-only·흑연 두-상 한정·비-크기·②≠Gaussian). 무라벨 식 2(식번호 재배열 0) — **제거 용이 독립 블록**(D22 유보 대응). cite=dreyer2010/2011(기존) | bgbox 1(신규 산문 ~12행·새 파라미터 0) |
| A-012 | R2 | ch1_sec04_hys | **CNT 핵생성 연결 문단**(O-C 채택 — DIRECTION (iv) 경량안): γ_j 지위 문단 뒤 5문장 — 과주행 조기 이탈의 미시 기작=상분리 부록 CNT(ΔG* 지수 억제·binodal 근방 발산) 서술형 참조(부록은 독립 컴파일 — 절 제목 텍스트로, 절번호 stale 회피)+γ_j 현상학 지위 불변 가드+γ(계면)/γ_j·부록 ξ/본문 ξ 기호 가드. 신규 식·라벨·서지 0 — 제거 용이 | 산문 1문단 |
| A-013 | R2 | ch1_sec01·ch1_sec02a·ch1_sec05·ch1_sec07·ch2_sec03·ch2_sec07·ch2_sec09 | **인용 다리 흑연분 7 삽입점**(O-B 8건 채택 — D22-5 양식 3요소[변수 대응표/등치식·방법 요지 1문장·가정 차 1문장], srcbox): ①bazant2013→eq:bv χ-분할(등치식 eq:br-bazant2013-1 신설·arXiv 원문 식[7][26][27][29] 대조·η 글자 가드) — TST bgbox 뒤 ②dreyer2010/2011→(iii-a)·eq:dUhys(결과 구조 대응 — 식 재현 없음"확인 필요"3건 규약) ③mckinnon1983→eq:sm-bare/eq:Veq(x↔θ·ξ 가드) ④**weppner_huggins1977+baek_pilon2022 병합**(R-1 — 단일 "측정 원전" srcbox·[V21-Q5-02] 앵커 뒤·baek 대응표 트림 R-3·tier B 1차병기) ⑤bernardi1985→eq:qrev(항별 대응표·가정 차→본문 포인터 트림 R-2) ⑥allart2018→ΔS⁰_j 검증(수치 재현 금지 — 부호·규모 수준) ⑦reynier2003→ΔS_vib 음 baseline. 인용 키 10종 전건 원장 V1 | srcbox 7(라벨 +1: eq:br-bazant2013-1 — §5 이하 식번호 +1 이동)·신규 서지 0 |
