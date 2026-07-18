# V1023 CHANGE LOG (S 구조·A 증축·C 정정·E 확장·B 빌드)

> 승계: v1.0.22 CHANGE_LOG(C-038~056·A-011~018·S-001~012) 종료 상태에서 출발. v1.0.23 신규 변경만 본 로그.
> 규칙: 전 변경 = 본 로그 ↔ 원장/스냅샷 1:1. boxed 수식·라벨 무변경 원칙(개정은 제안·검산 후 집행).

| ID | Phase | 파일 | 변경 | 규모 |
|---|---|---|---|---|
| S-013 | P0 | docs/v1.0.23/(전 골격) | v1.0.22→v1.0.23 골격 복제·버전 결합 갱신(common_preamble_v1023·externaldocument·드라이버 버전 문자열·test 코드 경로). 계보 주석(v1.0.21 등) 보존. 내용·수식·라벨 무변경 | 파일 복제·개명(신 물리 0) |
| A-019 | P2 | _sections/ch1_appE_selfconsistent.tex(신설) | 부록 E "자기일관 해법 --- ratio 닫힘과 전달함수"(letter E). E.1 lag 비선형 Volterra 자기일관+동결 0차(Prof convention 원형먼저) / E.2 1차 ratio 닫힘(사용자 Eq.34 이식·동결극한 정확회수) / E.3 P3-5 5항 / E.4 타당성 ε 부등식+(i)(ii)(iii) 매핑+열화 warnbox / E.5 전달함수 H=1/(1+iωL_V) / E.6 코드지도. 서두 warnbox=적용불가 I·III 명시 | 신설 부록 1본(+4p) |
| A-020 | P2 | _sections/ch1v22_bib.tex | bibitem 3종 추가: lee2017jcp(사용자 JCP147·DOI 확정)·lee2011jcp(Ref.6)·son2013jcp(Ref.7). Ref.6·7 제목·DOI 미확보 명기(날조 0) | +3 bibitem(39→42) |
| S-014 | P2 | ch1_graphite_v1.0.23.tex·ch1_sec08_lag.tex | 부록 input 1줄(\input ch1_appE)·본문 §8 말미 부록 E 포인터 1문장(코드 언급 0) | 조립+포인터(신 물리 0) |
| A-021 | P3 | Anode_Fit_v1.0.23.py | 부록 E 자기일관 옵션 구현: `_causal_memory_ratio`(1차 ratio 보정)·`_lag_ratio_geff`(g_eff=2χ_d·Ω/RT)·`transfer_apparent_from_equilibrium`(H=1/(1+iωL_V) FFT)·`__init__` 플래그 `lag_ratio_correction`(기본 False)·dqdv elif 분기·헤더 (E)(F). **기본 off = 동결 bit-exact(G1 max\|d\|=0)** | 신규 함수 2·메서드 1·플래그 1·분기 1 |
| B-001 | P3 | test_gates_v1023_selfconsistent.py(신설) | 자기일관 옵션 게이트 G-E1~E5(동결회수·dqdv bit-exact·차수이득 Picard·전달함수·liveness) 5/5 PASS | 신설 게이트 1본 |
| A-022 | P3 | _sections/ch1_appE_selfconsistent.tex | E.6 코드 지도 3행을 실 함수명으로 갱신(수식↔코드 1:1 정합 확정) | 표 3행 갱신(신 물리 0) |
| C-057 | P5 | _sections/ch1_appE_selfconsistent.tex | 적대검수(AUD-4) 수치 증거 정정: F-1 derivbox "~1e-8"(오귀속)→"정확히 0(항등)"·F-2 E.5 "1e-9"→커밋 게이트 G-E4 rel RMS 3.96e-6·F-3 warnbox "3–10×"→"2–10×"·F-4 "일치"→"정합(계수~1.5)"·F-6 충전 거울 1문장 | 수치문장 4정정+1추가(밑바탕 주장 불변) |
| C-058 | P5 | _sections/ch1_appB_codemap.tex·Anode_Fit_v1.0.23.py | stale 버전 라벨 정정(AUD-1 F-1): appB 코드파일명 v1.0.21→v1.0.23·코드헤더 release 1.0.21→1.0.23·test_gates_v1021→v1023·f_Si 라벨 0.7→0.8(주석만·로직 무변경, G1 bit-exact 재확인) | 문자열/주석 정정(로직 0) |
| B-002 | P5 | test_gates_v1023_selfconsistent.py | G-E4 허용오차 5e-3→1e-4(AUD-4 F-7·실측 3.96e-6 대비 회귀감지력 확보) | 게이트 임계 강화 |
