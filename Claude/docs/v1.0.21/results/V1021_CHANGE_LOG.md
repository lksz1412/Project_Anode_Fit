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
| A-004 | Q3 | ch1_sec05_width.tex | **TST 배경 bgbox 신설**(§5.1 말미·fig:barrier 앞) + 본문 다리 1문장(orphan 방지) — (a)두 전제(준평형·재교차 무시) (b)k_BT/h 유도(m*·δ 상쇄, eq:partfn 위상공간 눈금 연결) (c)TST 속도식+ΔG_a 미시 식별(재정의 아님) (d)ΔS_a=R ln(q‡/q_R) boxed + Part 0 접속(eq:sm-sint 동일 연산)+ΔS_rxn 구분 가드+용량 q 각주 가드 + verifybox 4검산. 체리픽: q3o1 베이스+q3f1 다리/배치+q3f2 눈금+q3f3 식별 가드 | 라벨 +5(eq:tst-{qrc,freq,rate,dG,box})·eqblock +5(boxed 1)·자산 주석 V21-Q3-01~05 |
| A-005 | Q3 | ch1_sec08_lag.tex | eq:Lqmid2(ΔH−TΔS 갈라 적기) 직후 후방 연결 1문장 — §8은 갈래를 쓰고 §5 박스가 기원 | 없음(산문 1문장) |
| C-020 | Q3 | ch1_bib.tex | glasstone1941 등재(TST 단행본 원전 — 원장 V1, v1.0.20 P7 웹 검증 승계) | bib +1 |
| C-021 | Q3 | ch1_bib.tex | laidlerking1983 등재(TST 사적 리뷰 — 원장 V1) + 헤더 카운트 36→38종 | bib +1 |
| R-001 | Q4 | ch1_sec03_center.tex | fig:UjT 신규(U_j(T) 4직선 온도 지도 — FIGS_PICK N-3 베이스 FO3-4 그대로) + 본문 참조 1문장 | 라벨 +1(fig) |
| R-002 | Q4 | ch1_sec04_hys.tex | fig:hysgap 신규(무차원 gap·Taylor 함정 대조·T_c 소멸 2패널 — N-2 베이스 FF1-1) + 본문 참조 1문장. 캡션 sec:hys-gap 자기참조는 "본문 ★Taylor 전개의 함정"으로 재구 | 라벨 +1(fig) |
| R-003 | Q4 | ch1_sec10_sum.tex | fig:sumcurve 신규(합산 전체 곡선 268/328 K+기여 — N-5 베이스 FF3-3) + 본문 참조 문장(fig:UjT 연결) | 라벨 +1(fig) |
| R-004 | Q4 | ch2_sec08_synthesis.tex | fig:qrevsoc 신규(∂U_oc/∂T 완전vs단순+수준선+5점 / Q̇_rev/I 부호 교대 2패널 — N-1 베이스 FF2-1) + 본문 참조 문장 | 라벨 +1(fig) |
| R-005 | Q4 | ch2_sec04_einstein.tex | fig:svibid 신규(S_vib 닫힌형·두 극한 / 강제 영점·3θ_E 가족 2패널 — N-4 베이스 FF2-5) + 본문 참조 문장 | 라벨 +1(fig) |
| (Q4 비고) | Q4 | — | 그래프트 요소(FF2-2 staging 4점 등)와 B급 6건(N-6~N-10·R-1·C-1)은 좌표 재평가·과밀 검토가 필요해 Q4b 이월(FIGS_PICK §D 참조). 베이스 조각은 각 창의 컴파일·물리 검산 통과본 그대로(좌표 무수정 — 물리 가드) | — |
| N-001 | Q5(항법) | ch1_preamble.tex·ch2_preamble.tex·마스터 2본 | **전역 항법 토글 인프라**(D21-1): \ifnavaid(기본 꺼짐)·\NAVAID 감지·항법판 헤더/표제 변형·드라이버 2본(graphite_ica_ch{1,2}_v1.0.21_nav.tex — 단일 소스, 토글만) | 없음(조건부 — 미적용판 빌드 불변 70/26p 확인) |
| N-002 | Q5(항법) | _sections/ch1_appC_navaid.tex(신규) | **부록 C(항법판 전용)**: ①식 의존성 지도 fig:navmap(Part 0 사다리↔본론 N2–N9 2-레일·U_oc↔ξ_j 순환="정의상 implicit" 표기·Ch2 인계 파선 박스 — CLAUDE.md 검수 3·4항 직결) ②통합 기호 대응표 tab:navsymbols(동명이의 3건 ★: q 삼중·u_j·g 계열). 새 물리 주장 0(색인 전용 선언) | 라벨 +5(sec:appendix-nav·ssec 2·fig:navmap·tab:navsymbols)·eqblock ±0 |
| N-003 | Q5(항법) | ch1_sec00_intro.tex·ch2_sec00_intro.tex | **독자 경로 안내 keybox**(항법판 전용, ③): 피팅 실무 경로 vs 이론 유도 경로 + 부록 C 안내(Ch2 는 서술형 안내) | 없음(조건부 산문) |
| (Q5 비고) | Q5(항법) | 마스터 ch1 | 조건부 \input 은 3행 형태(행 선두 \input) — tools_check_structure 의 input-follow 정규식 호환. 체커는 appC 를 양 판 공통으로 스캔(라벨 완결성 검사 의도적) | — |
| A-006 | Q5(top3①) | ch1_sec10_sum.tex | **끝-대-끝 계산 예제 신설**(sec:sum-worked, fig:sumcurve 뒤) — V_n=0.085 V 한 점을 표 tab:staging+식 4개(eq:Uj·logisticsolve·eqpeak·sum)만으로 6.95 Q_cell/V 까지 완주. 수치는 마스터 손검산 + FF3-3 독립 python 좌표와 4/4 교차 일치(4.865/1.568/0.4408/0.0286). B-006 환산값 규약 재강조(표시 반올림 입력 금지 문장). 무번호 display 수식 3(eqblock 체계 밖 — 의도) | 라벨 +1(sec)·eqblock ±0 |
| N-004 | Q5(top3②·항법판) | _sections/ch1_appC_navaid.tex | **Ch1↔Ch2 로드맵 대응표 C.3**(tab:navroadmap — 교차 지점 11행·라벨 분리 주의 2건 명시). 배치 판단: 별도 컴파일 간 색인이라 항법판 소관(미적용판과의 차이 비교 자료) | 라벨 +2(ssec·tab) |
| A-007 | Q5(top3③) | ch1_sec01_n0n1.tex | **측정 원리 배경 bgbox 신설**(§1 말미) — (i)준평형 OCV=GITT 원전 (ii)전위차 엔트로피법+상전이 유형 해석 지도 (iii)가역열 열량 검증(Ch2 서술형). 스코프 한정 가드 명문("원리 대응만·기법 상세 범위 밖·모델 식은 측정 방식과 무관") — GENERAL 보고서 (v-1) 위험 완화 그대로 | 없음(산문 bgbox)·cite +4(weppner_huggins1977·baek_pilon2022 신규, reynier2003·swiderska2019 기존) |
| C-022 | Q5(top3③) | ch1_bib.tex | weppner_huggins1977 등재(GITT 원전, tier A — CrossRef 검증: DIRECTION_GENERAL_REPORT §(v-1)) | bib +1 |
| C-023 | Q5(top3③) | ch1_bib.tex | baek_pilon2022 등재(해석 지도 리뷰, tier B — 1차 병기 규약 비고 포함) + 헤더 카운트 38→40종 | bib +1 |
| A-008 | Q6(L1) | ch1_sec15_lcoelec.tex | **LCO 한 점 시연 소절 신설**(sec:lco-worked, §15 말미) — (a)슬롯 산술(ΔS_e=−45.7 → ΔS_eff/F=−0.411 mV/K) (b)반전·완전식 표(x̄=0.50/0.85: U_oc 3.9243/4.0095 V·계수 −0.312/−0.128 mV/K) (c)게이트 껐다 켜기(+0.160→−0.128 mV/K 부호 반전·U_oc −91 mV). **전 수치 = Anode_Fit_v1.0.21.py 실행 재현**(doc-leads). tier-C 시연·T_ref 동결 근사 명시(Si/LCO 보고서 §5 단서 그대로) | 라벨 +1(sec)·무번호 display 2 |
| A-009 | Q6(L6) | ch1_sec14_lcodecomp.tex | ★스코프 주의 문장 — Ch1 슬롯 분해(성분) vs Ch2 ΔS⁰_j(전이 전체 상수) 혼동 방지(INTERCHAPTER M-1) | 없음(산문 1문장) |
| (Q6 비고) | Q6(L7) | — | θ_E 지칭 정정(L-5)은 v1.0.20 B-007 로 기해소 확인(grep "vibrational" 0건) — 재집행 불요. L2(tier 실측)·L3(T-복원)·L4(q_irr)·L5(원전 재확인)는 실측/코드 연동 대기 — 이월 | — |
| A-010 | Q7 | _sections/ch1_appD_si.tex(신규)·마스터 | **Si 예비 지도 부록 신설**(sec:appendix-si, appB 뒤·항법 앞 — 양 판 공통 문자 안정) — 사실 8건(전건 검증 인용)·노드 생존 판정표 tab:simap(이월 2·구조 2·재해석 3·부분 2·새물리 1)·전하 보존 전극 중립성 Si 실증(eq:sm-mc-balance 앵커·verbrugge_lisi2016)·GS-1 기계 히스 공백 선언(충돌+미착수 분류·이론틀 후보 larchecahn1973/koebbing2024)·부분 적용 시연 자리(성분≠상전이 명시). 아키텍처 = 보고서 권고 (iii)→(ii) 단계화(D21-3 정련 — "Q1 후 재질문" 조항 이행) | 라벨 +6(sec+ssec 5·tab:simap) |
| C-024~037 | Q7 | ch1_bib.tex | Si 계열 서지 14건 등재(핵심 우선 — D6(b))·헤더 40→54종. 전건 원장 B″ 검증 근거 | bib +14 |
| N-005 | Q7 | ch1_appC_navaid.tex | 부록 문자 하드코드("C.1/C.2") 제거 — 중성 서술(부록 순서 변동 내성) | 없음 |
