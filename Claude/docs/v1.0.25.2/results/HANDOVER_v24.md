# HANDOVER — v1.0.24 (최근문헌+Codex 반영: @3 Si Frumkin·@5 stage-2L·LCO 전자항 토글·#7·#1)

## 1. 무엇을 했나 (R0~R4)

v1.0.23 을 승계해, 최근(2021–2026) 문헌 고도화 연구(LCO·흑연·흑연+Si 한정)와 Codex 지적 중 **실재 문제**만
가려, 사용자 선택 **@3(Si 고용체 Frumkin 커널)·@5(stage-2L 엔트로피 온도분리)** 를 중심으로 문건(신규 소절 3)과
코드(additive·bit-exact 4건)에 정직하게 반영했다. LCO 전자항은 사용자 안 A(챕터 유지 + on/off 토글)로 처리.

| Phase | Steps | 내용 | 결과 |
|---|---|---|---|
| R0 | 1–4 | v1.0.24 골격 복제·시드표·baseline GREEN | PASS |
| R2 | 5–9 | 코드 반영 @3 regsol·@5 5-feature·LCO 토글·#1 단위(전부 bit-exact 폴백) | PASS |
| R1 | 10–14 | 문건 저작 9창 경쟁→W9 base·master 재조정·3장 통합 빌드 GREEN | PASS |
| R3 | 15–17 | 반영 검증(게이트 4/4·T-split 근거)·통합 적대검수 3차원 CLEAN | PASS |
| R4 | 18– | MERGE_READINESS·HANDOVER·INDEX·commit·push | (본 문서) |

(R1 은 9창 병렬 저작이 R2 코드와 겹쳐 진행돼 step 번호가 R2 뒤에 온다 — 실제 순서 반영.)

## 2. 핵심 결과 (정직)

- **@5 stage-2L (흑연, §1.5.4)** = 진짜 두-상 stage-2L 의 **엔트로피 온도분리**. 가운데 쌍(3↔2L·2L↔2)의 반응
  엔트로피 차 Δ(ΔS)≈29 J/mol/K → `∂/∂T(U−U)=Δ(ΔS)/F`=**0.30 mV/℃**(재현 0.271, ~90%), 병합~10℃,
  45℃ 2피크/25℃ 병합. operando XRD 독립근거(Schmitt 2022: 43℃ 뚜렷·0℃ 부재).
  **★정직**: 이는 **상온 단일 곡선 R² 이득이 아니라 다온도 서명**이다(25℃엔 병합). 판정자 `dμ/dθ|½=4RT−2Ω`
  는 얹되 **두-상/고용체 분류는 §7(sec:broadening-class)+피팅 Ω 로 위임**(뒤집지 않음). 5-feature 세분은
  **선택 코드 시드**(`GRAPHITE_STAGING_XRD_v1024`)로 4-전이 기준을 대체하지 않음.
- **@3 Si Frumkin (§3.2.5)** = a-Si 는 폭 판정 `w/(RT/F)=[1.45,2.74,1.09]≳1`(흑연 두-상 20–50× 대조)로
  **단일상 고용체**. 커널 `dQ/dV=QF/|RT/[θ(1−θ)]−2Ω|`(Ω<2RT), Ω→0 로지스틱 **폴백 bit-exact**. 유일 두-상 =
  1차 c-Li₁₅Si₄. **★정직**: Ω_Si 는 **범위 시드(Ω<2RT)일 뿐 점-식별 안 됨**(피팅 위임).
- **LCO 전자항 토글 (§2.6.1)** = `include_electronic_entropy` **기본 False**(전자항 제외 — 사용자 "커브 구할
  땐 빼고"·AUTHOR_BRIEF "기본 OFF" 사양). **상온 커브(dQ/dV @T_ref)는 토글과 무관하게 불변**(전자항이 ΔH^eff
  로 흡수 — 값선택 무관 성립). 토글은 오직 `∂U/∂T`(가역열·다온도)를 가름. 회사가 **True 로 전자항 가역열 기여를
  켜서 정량화**해 유지/제거 결정. v1.0.19/v1.0.23 상시-ON 거동은 True 경로가 bit-exact 보존(G1 회귀가 ON 경로로
  검증). plain MSMR R²=0.944≈흑연 0.940(전자항 커브 무관 실증).
- **#7 문구정정** = `Ω_j^cat` 은 **유효 평균장 쌍상호작용 축약**(미시 질서상 아님), config 엔트로피는 **별도 슬롯 직교**. 물리 유지·문구만.
- **#1 단위계약** = `func_L_q` 의 c-rate[1/h] vs Eyring[1/s] 3600× 불일치를 **주석으로 명시**(dH_a^phys=dH_a**+**RT·ln3600 ≈ dH_a+20.3 kJ/mol; ★감사서 부호 −→+ 정정·수치실증), **값 bit-exact 무변경**.

## 3. 코드 사용법 (회사 피팅)

- **@3 regsol**: Si-host 전이 dict 에 `'kernel':'regsol'`+`'Omega'`(<2RT) 추가 → Frumkin 커널. 미지정 = 로지스틱(bit-exact).
- **@5 5-feature**: `GraphiteAnodeDischargeDQDV(GRAPHITE_STAGING_XRD_v1024, ...)` (선택·additive; 기본은 `GRAPHITE_STAGING_LIT` 4-전이 유지).
- **LCO 전자항**: 기본 **False**(전자항 제외·상온 커브 불변). `LCOCathodeDQDV(..., include_electronic_entropy=True)` 로 가역열(∂U/∂T)에 전자항 활성(회사 다온도 확인용).
- 빌드: `xelatex -interaction=nonstopmode` 3-pass, **ch1 먼저**(xr 외부참조), 그다음 ch2·ch3.

## 4. 검수 상태

- 빌드 3장 **0-error** 91/28/20p·undefined ref/cite **0**·STRUCTURE_CHECK PASS(dup/unresolved/cite-undef/bib-uncited/env 전부 0).
- 코드 게이트: G1 bit-exact max|d|=**0**·selfconsistent 5/5·반영게이트 4/4.
- 통합 적대검수(R3, 인라인): doc↔code·물리유도·장간정합 **3차원 CLEAN**, blocker 0. 코드상수 U(298) 자기정합.
- **부수 복구**: R0 에서 구조검증 도구 JSON 이 덮어써 커밋됐던 `ch1_graphite_v1.0.24.tex` 마스터를 v1.0.23 셸+빌드로그로 재구성.

## 5. 정직한 한계 (회사 데이터 위임 — 문건 warnbox 명시분)

1. stage-2L 정량(0.30 mV/℃·병합 10℃): **다온도 데이터 없이 미검증**(tier B). Schmitt 2022 은 부호·경향 독립근거이나 0.30 원저 값 아님(저자 전체·권쪽 Crossref 최종대조 권장).
2. Ω_Si·Ω_j^cat **점값 미식별**(범위 시드·피팅 위임).
3. O3-LCO 전자항 온도의존 **미검증**(연속 g(E_F,x) tier 없는 모델 게이트).
4. tab:staging ΔS(+15/−14)는 **초기값(0/−5)의 피팅 갱신 대상**(표 미편집·P5).

## 6. 차기(옵션, 미실행)
- 유한율속 `dqdv()` 에 regsol 커널 확장(현 equilibrium 한정 — 감사 F-2 로 스코프 명시됨) = 추가 후보.
- 회사 다온도 반쪽셀 데이터 확보 후 stage-2L 0.30 mV/℃·Ω 점값·전자항 게이트 round-trip 확정(Task #38 미완).
- 모델 개선 후보(랭크·실측검증 완료, `comp_v24/IMPROVEMENT_DIRECTIONS.md`): #1 흑연 전이 4→5–6(+0.2–0.4%)·#2 비대칭 폭(+~1%)·#4 정칙용액 자유에너지(R²≈0.96 천장=MSMR 두-상 near-delta 한계의 진짜 해법, Ch2–3 열역학 과제). 전부 P5 선택.

## 7. 마감(R4) 후 강화 — 이 세션 추가 (최종 커밋 709d9e9)

R4 마감 이후 다음을 추가 수행했다(전부 반영·검증·커밋·main 동기화):

- **공개 실측 피팅 검증** (`comp_v24/FIT_CHECK_v1024.md`·`final_fit_sintef.png`·`sintef_data/` CSV 영구보존): SINTEF Zenodo 20086298(CC-BY-4.0) 실측 pOCV 를 **@3/@5 실제 코드경로**로 피팅 — 흑연 @5 5-feature 0.9525→**0.9731**·실리콘 @3 Frumkin regsol **0.9944**(Ω/RT 이 문건 분류 자발 재현: a-Si 고용체 + c-Li₁₅Si₄ 두-상)·흑연+Si 블렌드 **0.9848**(f_Si≈0.75). (초판이 실수로 기본 로지스틱으로 피팅한 것을 regsol 실경로로 정정.)
- **sifr Ω>2RT binodal 정합**: 문건 sifr warnbox(v)가 "Ω>2RT 커널 유효범위 밖" 이라 적었으나 코드 `_regsol_dqdv` 는 `_regsol_binodal_xa` 의 Maxwell 공존으로 실제 처리 → 문건을 코드에 맞춰 정정.
- **★전수 doc↔code 정합 감사** (`comp_v24/AUDIT_v1024_DOC_CODE.md`, 6 병렬 에이전트 + 마스터 수치 재검증): **곡선·피팅 정확성 BUG 0**. 잠재 코드버그 1건 수정(`_regsol_dqdv` 용량 +0.063% → `wi=Q/xg.size`, 재검증 area=1.000000·로지스틱 bit-exact 불변) + 주석/문서 불일치 다수 정정(func_L_q dH_a^phys 부호 −→+·regsol 스코프 equilibrium 전용 고지·XRD "두-상4"→§7 위임·토글 "ON(기본)"→기본OFF·헤더 "부록E만·무변경" 정정·z_cut clamp·stale 파일명 등). 문건 3건 정정(lcoomega 토글 True 선형화·gr2L §5b(d)(iii) 재유도 사다리·§10 반올림).
- **최종 검증**: 게이트 전건 GREEN(G1 bit-exact 0.0·reflect **4/4**·self-consistent **5/5**·R6 **3/3**) · 빌드 GREEN(ch1 91p·ch2 28p·ch3 20p·0 err·0 undefined ref). **코드=문건=주석 전면 정합.**

- **흑연 6-gallery 고분해능 opt-in 추가 (IMPROVEMENT #1)**: 문헌 6-gallery MSMR(`GRAPHITE_STAGING_MSMR6_LIT`, ad2061 ω_j·U0_j)를 **additive opt-in** 으로 추가 — 기본 4전이 bit-exact 무변경(G1 0.0 보존). 해상도 사다리 {4-전이(기본)·5-feature XRD·6-gallery MSMR}. 문건 §5b 에 gallery≠물리상 구분 명시(6+ 별개 상은 XRD 미지원 폐기·gallery 표현은 정당). 검증: 전이6·유한·비음·ω 검산 정확·게이트 전건 GREEN.

---

## 6. FB 1차 정독 피드백 리비전 (FB0~FB7, 2026-07-22)

R4 마감 후 사용자 1차 정독 피드백(F-01~F-11)을 **문건 한정**으로 리비전(코드 bit-exact 무변경). 상세 = `Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md`.

- **FB1(F-11)** 코드=부록: 본문 코드 함수명 → 부록 전용(grep **0**). → CLAUDE.md P3-8 게이트 명문화(재발 방지).
- **FB2(F-06)** 조판: 여백 25mm·줄간 1.16·문단 0.55em·microtype.
- **FB3(F-04·05·10)** register+제목+용어: 수필체·survival 술어·판번호·자기-diff·정직 형용사 평서화; 제목 N-태그 제거(~33); **요동/양성→영문**(body 0)·**음함수/섭동/준위→국문+첫 병기**·유일근→"유일한 근".
- **FB4(F-02·03)** 노테이션: 확률 **P→소문자 p**(압력 P 유지·Part T 소문자 p 와 정합)·f_int 자리당 vs Helmholtz F 가드.
- **FB5(F-07·09)** overflow: E.3 서지 리스트 off-page(itemize 전환)·식2.39 재확인·**전역 픽셀-스캔 149쪽**으로 실 overflow 3건 추가 수정(Table11 `l l l l`→p{}·식2.18 주석 축약·식2.36 multline).
- **FB6(F-01·08)** 내용: §1.1.4 배경 박스 압축(~50%↓·인용 5종 보존)·LCO장 서두+제목 **차이-선도**(σ_d·order-disorder·전자항) 재균형.
- **빌드**: ch1 **97p**·ch2 **30p**·ch3 **21p**(0-err·undefined ref/cite 0). 코드 sha256 **f230f59b** 불변. **물리·식번호·label 정의 불변**(P→p 개명·식2.36 multline도 식번호 보존).
- **적대 검수**(FB7): 3창 병렬(피드백완전성·register/용어·물리/label) — 결과 `PHASE_FB7_RESULT.md`.
