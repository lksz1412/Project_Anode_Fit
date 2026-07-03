# V1.0.13 RESULT — 통계역학-first 재구조화 + LCO 후방 통합 + 문건-코드 루프 + Fable 10회 검수

> 기준 커밋: 292f10e (P5 R10 마감). 마스터플랜 = `../plans/2026-07-02-v1013-restructure-master-plan.md`(rev.4).
> 진행 상세 = `process/V1013_EXECUTION_LEDGER.md`(라운드별 append-only 로그). 본 문건은 Result 11항목 표준.

## 1. Phase·범위
- P1.1 설계 → P2.1 Part 0 신설(N=6 경쟁+체리픽) → P2.2/P3.1 재배열·압축 → P3.2 코드 루프 B → P4.1 용어·overfull → **P5 Fable 단독 10회 가변-청크 검수(R1~R10, 라운드마다 3기 병렬+master 삼각검증+게이트+커밋)** → P6.1 마감.
- 대상: `docs/v1.0.13/` = ch1 tex(50p)·ch2 tex(14p)·Anode_Fit_v1.0.13.py·FITTING_GUIDE·demo/plot/test/sample 스크립트·figs.

## 2. 목표(사용자 지적 7건)
① 흑연 완결 후 LCO 후방 몰기 ② v6 "수식만 읽어도 대부분 이해" 회복 ③ 식 1.85/1.86 overfull ④ 약자 원어 병기+일본식 번역어 제거(한글 서술 베이스 유지) ⑤ 통계역학에서 시작해 거시로 확장 ⑥ 코드에 없어도 필요한 개념 서술 ⑦ 문건-코드 양방향 루프. 우선순위(GO): 물리 논리 > 논리 비약 > 수식-주도.

## 3. 수행 요약
- **Part 0 신설**: 공준→Gibbs 인자→Ξ→θ→요동-응답→lattice gas(Stirling 두 경로)→평균장 Ω·이중웰 문턱→기준전극 2-평형 차감→ξ_eq logistic→Nernst. 라벨 eq:sm-* 24 신설+이동 4(중복 0), TikZ 4종 신설.
- **Part II 단일 우산**: 도입 3소절(전극-중립 5-인벤토리·방향 규약 eq:lco-sigmaslot·MSMR 예고)+이동 6절. fig:lco-dirmap 신설.
- **코드 루프 B**: `_delith_is_discharge` 전극 인지(흑연 True/LCO False, curve 라벨→탈리튬화 부호 자동 환산)·LCO 전자항 T1(x_MIT=0.85) 재정렬·dict dH 코드 F 재역산(−391016.1/−375554.4)·config 계수 n_jR/F 일반화(R2)·스칼라 퇴화 스팬 평형 강제(R10)·'w'-단독 config 게이트(R10).
- **P5 10회 검수**(라운드별 청크 스킴 로테이션): R1 통독→R2 절(★n_j 물리 정정)→R3 전 식 재유도(물리 붕괴급 0 확정)→R4 부호 창 39창(부호 반전 0)→R5 참조·라벨·경계(기계 감사 깨끗)→R6 수식-주도(재팽창 52곳+압축 이월 4쌍)→R7 용어(병기 역전·g_j 충돌)→R8 그림·표(456점 재계산 일치)→R9 상호충실도(가이드 방향 처방 오류)→R10 자유 사냥+flag 49건 처분.

## 4. 산출물
- `docs/v1.0.13/`: graphite_ica_ch1_v1.0.13.tex(+pdf 50p) · graphite_ica_ch2_v1.0.13.tex(+pdf 14p) · Anode_Fit_v1.0.13.py · FITTING_GUIDE.md · demo_lco_heat.py · plot_dqdv.py · sample_test_v1013.py(+png) · test_regression_graphite.py(+golden npz) · graph_suite_v1013.py(P6.1 이식) · figs/.
- `results/process/`: V1013_REVIEW_R{1..10}_{A,B,C}.md(30건) · V1013_EXECUTION_LEDGER.md · V1013_STRUCTURE_MAP/TERMS_POLICY/PROSE_BUDGET/CODE_MAP(+ADDENDUM_R10) · P21 드래프트·체리픽 맵.

## 5. 게이트 결과(최종)
- ch1: 0-err · 50p · ref/citation 경고 0 · overfull>10pt 0(sub-10pt 6건 기록 — 게이트 기준 밖). ch2: 0-err · 14p · 0 · 0.
- 흑연 회귀: verify **13/13 bit-exact PASS**(v1.0.13 코드 ↔ v1.0.10 golden — 전 라운드·전 커밋에서 유지). demo·sample 재실행 정상(dS_e 골 −45.68).
- 물리 불변 확정 판정: f=+σ_d(pairing 유일해)·C-1 Δμ=+sF(V−U)·H-1 BW 부호·이중계산 가드 — 10라운드 전부 PASS.

## 6. Read Coverage
- 검수자 coverage 선언 의무(창 분할·missing 0) 라운드 전건 이행: ch1 2,930여 줄·ch2 780여 줄·py 883줄 — 통독/절/식(재유도 전수)/80줄 부호 창/참조 536건/문단/용어 51클래스/그림 18종·표 9종/코드 인용 36단위/flag 49건의 상보적 스킴으로 각각 100% cover. 압축·리뷰 근거는 R 보고서 30건에 줄번호·원문 인용으로 잔존.

## 7. 발견·정정 통계
- 총 정정 ≈ 260곳(R1 30·R2 20+hotfix2·R3 31·R4 22·R5 35·R6 52·R7 40·R8 30·R9 20·R10 12).
- **물리 실결함 정정 3건**: ①config 항 계수 n_jR/F(R2 — 문건+코드, n=1 에서 bit-exact 무영향) ②스칼라+동역학 침묵 오차 −6.9%(R10 — 평형 강제 가드) ③'w'-단독 config 오가산 +0.057 mV/K(R10 — 'n' 게이트). 그 외 물리·부호 결함 0(9라운드 연속).
- 잠복 부호 함정 봉쇄 다수: Ch2 파생 D ±½ 무명시·LCO 라벨 층위(문단·주석·가이드 처방·데모 라벨)·f=−σ_d 역부호 가드 등.

## 8. 미해결·이월(P6.1 처분 후 잔여)
- 실데이터 round-trip 단계 소관: 다온도 T² 곡률(동결 해제)·LCO Ω^cat/dH_a 배정·ν 상향 재베이스라인·x-매핑 순환 수치 확인.
- 선택 위생(존치 판정): sub-10pt overfull 2건(5.87/7.22pt)·py T_ref/eps 원칙 문구·barrier 가장자리 4점.

## 9. 결정 사항(기본값·근거는 ledger)
- LCO 산문 목표 −35%: 실측 −23.3%이나 신설 3절(+29문장 상당) 포함 — 이월 콘텐츠 기준 사실상 도달(165 vs 161), 물리 우선 서열로 강제 삭감 안 함.
- "(신규)"·"(v7-11 유래)" 귀속 태그: 15/16 그림 대칭 체계로 존치 확정.
- overfull 게이트 = >10pt(계획 선언 기준) — 전체 카운트는 별도 기록.

## 10. 리스크·주의
- 코드 동작 변경 2건(R10)은 퇴화·코너 입력 전용 — 배열 스윕·'n' 데이터셋 경로는 bit-exact 불변 실증. 단 v1.0.12 대비 스칼라 호출 결과가 (옳게) 달라짐 — 외부 사용자 있으면 공지 필요.
- FITTING_GUIDE 구판(v1.0.12)의 "direction=+1" 처방은 v1.0.13 에서 금지 — 구판 가이드 재사용 금지.

## 11. 다음 단계
- 실데이터(코인 하프셀 dQ/dV rate/온도 시리즈) 확보 → S0-S5 식별 사슬로 round-trip 피팅(가이드 5-Phase) → 이월 4건 해소 → v1.0.14.
