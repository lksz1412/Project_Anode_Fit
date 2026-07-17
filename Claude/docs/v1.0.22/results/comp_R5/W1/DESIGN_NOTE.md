# DESIGN_NOTE — W1(이론 우선) 저작 설계 근거 (v1.0.22 R5, comp_R5/W1)

> 창 = W1 이론 우선. 강조축 = 이론 완결성(§3.3 공통-μ 대정준 일반화·§3.4 Larché–Cahn 유도 사슬).
> 전 절(패키지 6항) 저작 — 강조는 배분이지 생략이 아님. 산출 = s31_map·s32_cases·s33_blend·s34_mech·s35_code·notation .tex + 본 노트.

---

## 1. 설계 근거 (창별 강조축 반영)

- **§3.3·§3.4 최심(강조축).** 두 절에 완전 (a)→(d) 유도 사슬 + verifybox + keybox 를 배치.
  - **§3.3**: `eq:sm-mc-balance` 의 클래스곱을 host 곱으로 **한 줄 일반화**(`eq:blend-factor`→`eq:blend-occ`→`eq:blend-balance`). 핵심 논증 셋을 명시 이월/신설: (i) 요동 양성 유일근을 **재유도 없이** xr(`eq:sm-mc-fluc`) 인용하고 "host 추가 = 양의 분산 항 추가"로 한 줄 확장, (ii) `f_Si→0` **bit-exact 회수**(`eq:blend-limit`)를 `sec:sm-mc` 의 `N_p=1` 회수와 같은 정신으로 신설(R6 게이트의 이론짝), (iii) 부호 읽기 이월.
  - **§3.4**: Larché–Cahn 응력항을 골격 결과-사슬로 끌어와 **가역 화학역학 결합까지 실제로 닫음**(`eq:si-lcmu`→`eq:si-vshift`→`eq:si-coupling`, Λ_σ=v̄_Li/F). 부록 예비 지도(GS-1="충돌+유도 미착수")보다 **한 단계 전진** — 공백 위치를 "응력항의 존재"에서 "응력의 경로의존 구성식(`eq:si-plastic`)"으로 좁힘. 못 닫는 지점(소성 σ_h(이력))을 정확히 짚어 GS-1 선언.
- **전 절 완결.** §3.1(생존 지도 본문 승격)·§3.2(케이스 3종+열특성+파라미터 표)·§3.5(R6 요구명세 4항)도 전건 저작. 강조 절 대비 밀도만 낮춤.
- **중심식 지위 보존(P3-2).** `eq:blend-balance` 를 "전하 보존이 내부 전위를 결정하는 중심식"으로 유지 — OCV에서 읽는 흐름으로 회귀하지 않음. U_oc는 고정-함량 반전의 음함수(정의상 implicit).
- **이름·구조 보존(P5).** 계승 기호 재정의 0. 신규 기호는 도입 절 명시(σ_h·v̄_Li·Λ_σ = §3.4; host·f_Si·U_oc = §3.3). Ω_j(정규용액)와 v̄_Li(부분몰 부피) 충돌 회피 위해 부분몰 부피에 별도 기호 사용.

## 2. 공백 4분류 표 (P3-4 / Gate-2)

| # | 공백/구조 | 4분류 | 절·라벨 | 처리 |
|---|---|---|---|---|
| 1 | U_oc 음함수(블렌드 반전) | **정의상 implicit formulation** | §3.3 `eq:blend-balance` | 정당 — `eq:sm-mc-balance` 이월(대정준→정준 Legendre 반전). 공백 아님 |
| 2 | 다-host 유일근(N_p^gr+N_p^Si≥2 겹침) | **수치해법 필요** | §3.3 verifybox(i) | 요동 양성으로 유일성 보증(이월), 닫힌 역 없어 수치로 품 |
| 3 | GS-2: 공통-μ 완전 동시반응 | **물리 가정 충돌** | §3.3 `ssec:si-blend-gs2` | 평형은 정확·유한율속 비가산/host 전환은 1차 근사 편차. 구간별 전환 모델링 = 범위 밖 선언 |
| 4 | GS-1: 기계 히스(응력 경로의존) | **물리 가정 충돌** + 유도 미완결(범위 선언) | §3.4 `ssec:si-lc-gap` `eq:si-plastic` | 정규용액 이중웰≠소성 소산. 가역 결합은 닫힘·소성 구성식은 범위 밖 |
| — | **논리 공백** | (해당 없음) | — | GS-1·GS-2 모두 논리 공백 아님 명시(골격 무결·범위/가정 선언) |

- **핵심**: 논리 공백 0. 평형 골격(`eq:blend-balance`)은 옳게 닫혀 있고, 어긋나는 것은 그것을 유한율속(GS-2)·소성 히스(GS-1)에 직결하는 물리 가정이다. 두 GS는 "충돌+범위 밖"이지 "식의 결함"이 아니다.

## 3. "확인 필요" 목록 (수치 미확보 — 문헌/입력 공백, 위 4분류와 별개)

| # | 항목 | 위치 | 사유 |
|---|---|---|---|
| 1 | SiO_x 평균 전위(V) | §3.2 `tab:si-cases`·§3.5 케이스 셋 | 검증 세션 1차 문헌 원문 미확정(2차 리뷰 반복값 과잉귀속 금지) |
| 2 | 순수 SiO_x 단독 히스 절대 mV | §3.2 `ssec:si-siox` | 후보가 모두 블렌드 맥락 — 순수 SiO_x 단독 1차 문헌 미확보 |
| 3 | Λ_σ 정확값(mV/GPa 계산) | §3.4 verifybox | v̄_Li(Si 부분몰 부피) 수치가 검증 표 밖 입력 — 정성 규모 정합(O(100))까지만 tier-A 주장 |

**확인 필요 건수 = 3.** (원소 Si 평균 0.2–0.5 V는 tier B 원문 확인분이라 확인 필요에 미포함; Si–C 이론용량 "배합 의존"은 구조적 값 미배정으로 별도.)

## 4. 서지 채택 목록 (P3-5 / Gate-3 — V1 원장 vs comp_R4 검증 후보)

### 4a. V1 원장 키(Ch3 bib 14종 중 사용분 — 그대로 \cite)
`wen_huggins1981` · `limthongkul2003` · `li_dahn2007` · `obrovac_christensen2004` · `chevrier_dahn2009` · `beaulieu2001` · `sethuraman_stressevo2010` · `sethuraman_stresspot2010` · `liu_sizefracture2012` · `obrovac_chevrier2014` · `verbrugge_lisi2016` · `jiang_sihys2020` · `larchecahn1973` · `koebbing2024` (14/14 사용).

### 4b. comp_R4 검증 후보 키(전건 doi 실검증 완료 — 마스터 채택 시 원장+ch3v22_bib 등재 요망)
> 후보 키 = 저자_주제+연도 형으로 **제안**(원문 .md는 서지만 표기, 정식 key 미부여). 마스터가 채택분 확정 등재.

| 제안 key | 문헌(comp_R4 원천) | tier | 사용 절 |
|---|---|---|---|
| `miyachi_sio2005` | Miyachi+ 2005 JES SiO XPS 실리케이트 | A | §3.2 |
| `kitada_sio2019` | Kitada+ 2019 JACS SiO operando NMR | A | §3.2 |
| `zhang_sio2018` | Zhang+ 2018 JES SiO 용량감쇠(1710 mAh/g) | A | §3.2 |
| `yom_sio2016` | Yom+ 2016 JPS SiO ICE 58.52→82.12% | A | §3.2 |
| `andersen_sic2019` | Andersen+ 2019 Sci Rep 상용급 Si–C | A | §3.2 |
| `naboka_sic2021` | Naboka+ 2021 ACS Omega Si 10wt% 피크 분리 | A | §3.2 |
| `bohm_entropy2024` | Böhm+ 2024 Energies Si–C 엔트로피 계수 | A | §3.2 |
| `arnot_si2021` | Arnot+ 2021 JES Si 등온 열량 가역열 분리 | A | §3.2·§3.4 |
| `ai_blend2022` | Ai+ 2022 JPS 복합전극 반응전류 host 전환 | A | §3.3 |
| `chatzogiannakis_blend2025` | Chatzogiannakis+ 2025 B&S 30wt% 비가산 | A | §3.3 |
| `zhan_blend2026` | Zhan+ 2026 JES SiOx/Gr 전위 중첩·균열 | A | §3.3 |
| `tu_blend2024` | Tu+ 2024 JES MSMR 블렌드 ROM(Verbrugge 계보) | A | §3.3 |

**서지 규율**: 기억 서지 0. 수치는 comp_R4 표 원문 확인분만(tier 명기). 위 후보는 전건 tier A(검증 완료). tier B 후보(yamada_sio2012·lee_sic2025·zhang_prismatic2024·garrick_msmr2024·bohm_thermal2025·thomas_lisi2013·mertin_entropy2023·wojtala_entropy2022 등)는 정량 미확보라 본 창 본문 수치에 미사용(§3.2 열특성의 wojtala류 정성 서술은 미인용 처리).

## 5. 신규 식·라벨 인벤토리

- **신규 식(번호식)**: `eq:blend-factor`·`eq:blend-occ`·`eq:blend-balance`·`eq:blend-limit`(§3.3) · `eq:si-lcmu`·`eq:si-lcbal`·`eq:si-vshift`·`eq:si-coupling`·`eq:si-plastic`(§3.4) · `eq:si-code-sum`(§3.5) = **10식**.
- **신규 절/표 라벨**: `sec:si-map`·`tab:si-survival`+본문 4소절(§3.1) · `sec:si-cases`·`tab:si-cases`+5소절(§3.2) · `sec:si-blend`+2소절(§3.3) · `sec:si-mech`+2소절(§3.4) · `sec:si-code`+4소절(§3.5) = 절 5·표 2·소절 17.
- **xr live 인용(Ch1/Ch2 — 라벨 실확인분만)**: `eq:sm-mc-balance`·`eq:sm-mc-factor`·`eq:sm-mc-occ`·`eq:sm-mc-fluc`·`eq:sm-logistic`·`eq:sm-workbal`·`eq:sm-muV`·`eq:sm-eqcond`·`eq:sm-gc`·`eq:dUhys`·`eq:Ubranch`·`eq:sum`·`eq:eqpeak`·`sec:sm-mc`·`sec:sm-electro`·`sec:sm-lattice`·`sec:hys`·`sec:sum`·`sec:lco-code`·`tab:staging`·`tab:lco-staging` (전건 grep 실확인).
- **자산 앵커 신설**: `[V22-R5-01]`~`[V22-R5-26]` (절 말미 `% 자산:` 관행).

## 6. 검수 7항(P3) 자기점검

1. V_n/V_n,app/… 구분: 본 창은 U_oc(공통 평형 전위)·V_n(내부 전위)를 §3.3·§3.5에서 일관 사용, 혼동 0.
2. 전하 보존 중심식: `eq:blend-balance` 를 중심식으로 유지(OCV 읽기 회귀 X). ✓
3. 순환 의존성 표시: U_oc 음함수·다-host 유일근을 §2 표에 위치·분류. ✓
4. 4분류 분리 진단: §2 표(정의상 implicit/수치해법/충돌/논리공백 없음). ✓
5. ref 방법론 도입 4항: Larché–Cahn(§3.4)은 원장 V1 서지·유도 구조(가역 결합)·변수 매핑(σ_h·v̄_Li·Λ_σ)·가정 차이(이중웰≠소성)를 절 내 명시. ✓
6. Ch1 기준식 vs 전달식 충돌: `eq:sm-mc-balance`→`eq:blend-balance` 는 일반화(충돌 X), 부호 규약(`eq:Ubranch`와 동방향) 정합. ✓
7. ver.N/Chapter 혼동: 본 창은 Chapter 3 신 구조 명칭만 사용, 역사적 절 제목 미차용. ✓

## 7. 마스터 체리픽 참고(창 특성)
- **강점**: §3.3 일반화 논증의 엄밀성(요동 이월·f_Si→0 회수의 R6 게이트 이론짝화)·§3.4 유도 실착수(부록 대비 공백 1단계 좁힘)·논리 공백 0의 정직 분리.
- **의도적 배분**: §3.2 케이스 수치는 실측 우선 창(W2)이 더 촘촘할 수 있음 — 본 창은 tier·확인필요 규율과 파라미터 표 구조에 집중. 그래프팅 시 §3.3·§3.4를 본 창에서, §3.2 실측 밀도를 타 창에서 취하는 조합 가능.
