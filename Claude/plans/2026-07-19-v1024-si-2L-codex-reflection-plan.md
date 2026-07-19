# v1.0.24 Plan — 음극 반영(@3 Si 고용체·@5 stage-2L) + Codex 정정 문건·코드화

> 작성 2026-07-19. 표준 11-section. cumulative step 단조(이전 V1024 검증 ledger 이어받아 R-스텝 신규).
> 성격 = **반영 계획서**(검증 아님). v1.0.23 → **v1.0.24 신 버전**(additive·물리서사 보존).
> 근거 산출물(전부 커밋됨): `comp_v24/ablation*.png/json`·`TAKE_VS_DISCARD.md`·`CODEX_REVIEW_VERIFICATION.md`·
>   `GRAPHITE_STAGING_XRD.md`·`T_SPLIT_FINDING.md`·`regsol_si*`·`lit_raw/`.

## 확정 (사용자 2026-07-19)
- **@3·@5 를 전 화학(흑연·블렌드·LCO) 반영**: **@3 = 정칙용액 커널**(Si 고용체 Ω<2RT / LCO per-peak Ω) · **@5 = staging
  세분**(흑연 stage-2L XRD 5-feature / LCO 미세구조). 근거 `LCO_DIAGNOSIS.md`(LCO plain R²=0.944≈흑연 0.940·@3/@5
  +1.25~2.13%p).
- **★LCO 전자 엔트로피 = 코드 on/off 토글**(사용자 안 A): 커브(dQ/dV) 산출 = **기본 OFF**(단일T서 dH 흡수=잉여);
  가역발열/∂U/∂T = **ON 옵션**(회사가 다온도 데이터로 영향 확인 후 유지/제거 결정). **챕터는 남기고**(MIT 물리 보존)
  코드에 **변수 하나 추가**. → Codex #5·#6 자연 해소(전자항 "커브 불필요·∂U/∂T 선택" 명시).
- **Codex 정정**: #1(단위계약·bit-exact)·#7(sec13:154 문구). #3 불요·#2/#4 선택.
- **Ref 6,7 = 이미 반영 완료(v1.0.23 부록 E)** — Lee2011(JCP134,121102)·Son2013(JCP138,164123) 확정·JCP147 ratio 방법
  동역학 lag 접목. **미결 = ref6·7 제목·DOI 원문대조뿐**(비차단). ※CLAUDE.md 원의도(전하보존 되먹임 I 적용)는 v1.0.23
  P1서 "적분핵 없어 lag II에만 성립"으로 판정 — 되먹임(I) 재검토 원하면 별도 항목(D7).
- **결과물 = v1.0.24 문건 + 코드**(둘 다 수정).
- 무응답 대기 아님 — 아래 D1~D7 기본값 확정 시 R0부터 5-stage 루프 집행.

---

## Summary

검증(C·A·B·문헌)으로 **음극에서 실효·안정 개선 2건**이 확정됐다: **@3 Si 고용체**(블렌드 R² +0.66%p·2런 안정)와
**@5 stage-2L**(XRD 확증 상). 이 둘을 **물리 근거로** v1.0.24 문건·코드에 반영한다. 동시에 Codex(GPT-5.6)의
v1.0.23 검토 7건 중 **실제 정정 대상만**(코드측 #1 단위계약, 문건측 #7 문구) 반영하고, 나머지(#2·#3·#4)는
문서가 이미 투명해 불요, LCO 전자항(#5·#6)은 실 O3 데이터 부재로 **의도적 근사 라벨 강화만**(구현 보류).

**반영의 성격 = 물리 시드화**, curve-fitting 아님:
- **@3**: a-Si는 단일상 고용체(Chevrier-Dahn 2009·Artrith 2018) → Si-host를 **정칙용액(Frumkin, Ω<2RT) 커널**로.
  블렌드 잔차의 최대봉(Si 봉우리 0.43V)을 물리로 흡수(잔차 RMSE 1.23→0.86, 그림 `ablation_combo_resid.png`).
- **@5**: 흑연 staging을 **XRD 완전 5-feature**(Dahn 1991: 1′↔4·3↔2L·2L↔2·2↔1 두-상 4 + 4↔3 고용체 shoulder)로
  정합. stage-2L은 엔트로피 안정화 상(T-분리 재현 `T_SPLIT_FINDING.md`) → **Ω>2RT(sharp)/Ω<2RT(shoulder)
  기준으로 시드**해 자유피팅 불안정(개별런 −0.44~+0.27) 제거.
- **#1**: `func_L_q`의 C-rate[1/h] vs Eyring[초] 단위 불일치 → **단위계약 명시**(곡선 bit-exact 보존·dH_a 물리해석만 정정).

**핵심 원칙**: v1.0.23 물리 서사·기존 식·라벨·한글 표현 **보존**(P5). 신규는 **additive**(f_Si=0 흑연 회수·기존 4전이
폴백 bit-exact). 반영 후 **동일 블렌드·흑연 셋 재피팅으로 개선 재현**(회귀 게이트).

---

## Current Ground Truth

**검증 확정(반영 근거).**
| 항목 | 실측 결과 | 근거 파일 |
|---|---|---|
| @3 Si 고용체 | 블렌드 R² 0.987→0.994(+0.66%p)·잔차 RMSE 1.23→0.86·2런 안정 | `ablation*`,`regsol_si` |
| Si=고용체(두-상 아님) | 폭/(RT/F)=[1.45,2.74,1.09]≳1(흑연 두-상 ≪0.12) | `regsol_si.png` |
| @5 stage-2L 실재 | XRD(Dahn1991) 확증·T-분리 0.271 mV/℃≈Dahn 0.30·병합~10℃ 재현 | `T_SPLIT_FINDING.md` |
| 흑연 5-feature | 두-상 4(1′↔4·3↔2L·2L↔2·2↔1)+4↔3 고용체 shoulder | `GRAPHITE_STAGING_XRD.md` |
| @5 자유피팅 불안정 | 개별런 ΔR² −0.44~+0.27(국소최소) → **물리 시드 필수** | `ablation_combo_result.json` |
| Ω>2RT 시드 타당 | 흑연 두-상 Ω/RT=[4.06,2.02,3.55,4.07] 전부>2RT | `regsol2` |

**Codex 7지적 정정 대상 판정(`CODEX_REVIEW_VERIFICATION.md`).**
| # | 판정 | 이번 반영 |
|---|---|---|
| #1 C-rate 3600× 단위 | ✅ 맞음(dH_a 흡수·곡선무영향) | **정정: 단위계약 명시(코드)** |
| #7 sec13:154 Ω 혼동 문구 | ◐ 부분(혼동 실재·물리는 유효축약) | **정정: 문구 명확화(문건)** |
| #5 LCO x=0.85 한점 | ✅ 맞음·문서 P4 라벨 | **보류(실 O3 부재)·라벨 강화만** |
| #6 LCO T² vs 선형 | ✅ 맞음·문서 P4 라벨 | **보류(검증불가)·라벨 강화만** |
| #2·#4 | ◐ 부분·문서 투명 | 불요(선택 미세보강) |
| #3 Reynier 0.18 | ❌ 미지지 | 불요 |

**현 코드 구조(반영 지점).**
- `equilibrium`(L538)·`dqdv`(L624/759): `func_ksi_eq` 로지스틱 site-fraction. → **Si-host에 Frumkin 커널 분기 추가**(@3).
- `GRAPHITE_STAGING_LIT`(L1027): 4 전이(4→3·3→2L·2L→2·2→1). → **XRD 5-feature로 확장 + Ω 시드**(@5).
- `func_L_q`(L105): `T_attempt=(I/Q_cell)·h/kB`. → **단위계약 주석·환산 명시**(#1).
- `BlendedAnodeDQDV`(§3.5): 흑연host+Si host 가산. → Si host 커널 교체 시 f_Si=0 bit-exact 유지 필수.

---

## Phase Range

| Phase | 이름 | Steps | 게이트 요지 | 상태 |
|---|---|---:|---|---|
| **R0** | 착수·v1.0.24 골격복제·시드값 확정 | 32-35 | 골격 복제·Si Ω/흑연 5-feature U_j·ΔS·Ω 시드표·단위계약 스펙 확정 | 대기 |
| **R1** | 코드 반영 (@3·@5·#1) | 36-41 | Si Frumkin 커널·5-feature staging·단위계약 — f_Si=0/기존폴백 bit-exact + 게이트 실행 | 대기 |
| **R2** | 문건 반영 (@3·@5 절·#1·#7 정정) | 42-47 | Si 고용체 절·stage-2L 절·수식사슬·중간다리·서지·Codex 정정 | 대기 |
| **R3** | 반영 검증 (개선 재현·회귀·P3 게이트) | 48-51 | 블렌드 @3+@5 개선 재현·T-분리 재현·P3 7항목·빌드 GREEN | 대기 |
| **R4** | 적대 검수·마감(MERGE_READINESS·HANDOVER) | 52-55 | 치명0·코드↔문건 정합·서지 무결·bit-exact 계약 검증 | 대기 |

---

## Non-goals

- **LCO 전자항 T-의존(#5·#6) 구현 X** — 다온도 O3-LCO 실측 부재. **라벨 강화만.** (단 LCO **@3·@5 커널/staging 반영은 IN** — O2 실측 R² 개선 근거 `LCO_DIAGNOSIS.md`.)
- **@1(near-delta)·@2(비대칭)·@4(U 고정) 반영 X** — @1 무효(−0.02~−0.22)·불안정, @2 미미(+0.08), @4는 R²0(일관성용, 별도). 이번 선택 = **@3·@5만**.
- **near-delta(두-상 Maxwell) 커널 도입 X** — R² +0.5%만·무거움(regsol2). Si는 Ω<2RT(고용체)만.
- **전이 6+ 증설 X** — XRD 5-feature가 상한(Dahn). 그 이상은 curve-fitting.
- **곡선을 바꾸는 #1 수정 X** — 단위계약은 **bit-exact 보존**(dH_a 해석만 정정). curve()/dqdv() 수치 불변.
- **v1.0.23 물리 서사·기존 식·변수명·한글 훼손 X**(P5). 신규는 additive·폴백 보존.
- **사용자 GO 전 집행 X**.

---

## Implementation Changes

**신규/수정 파일.**
- `docs/v1.0.24/` — v1.0.23 복제 후 표적 수정(Si 고용체 절·stage-2L 절·Codex 정정·서지·검증 부록).
- `docs/v1.0.24/Anode_Fit_v1.0.24.py` — Si Frumkin 커널·5-feature staging·단위계약(bump).
- `Claude/results/PHASE_R{0..4}_RESULT.md`(11항) + `V1024_EXECUTION_LEDGER.md` 이어쓰기(12-col).
- `Claude/results/comp_v24/REFLECT_SEED_TABLE.md`(R0) — 반영 시드값(Ω·U_j·ΔS) 근거표.
- `Claude/results/comp_v24/REFLECT_VERIFY.md`(R3) — 반영 전후 재피팅·개선 재현·회귀.
- `Claude/results/comp_v24/MERGE_READINESS_v1024.md`·`HANDOVER`(R4).

**코드 변경 3건(요지).**
1. **@3 Si Frumkin**: Si-host 전이에 정칙용액(Ω<2RT) site-fraction 옵션 추가(`func_ksi_regsol` 또는 전이 dict `kernel:'regsol'` 플래그). 로지스틱=기본 폴백(bit-exact). Frumkin `dQ/dV = Q·F/|RT/(θ(1−θ))−2Ω|` 유한 broad peak.
2. **@5 stage-2L**: `GRAPHITE_STAGING_LIT` → XRD 5-feature(`GRAPHITE_STAGING_XRD_v1024`): 1′↔4·**4↔3(고용체 shoulder,Ω<2RT)**·3↔2L·2L↔2·2↔1. 각 전이 `Omega`(>2RT sharp/<2RT shoulder)·`dS_rxn`(2L 분리 Δ≈29) 물리 시드. 기존 4전이 리스트 = 하위호환 폴백 보존.
3. **#1 단위계약**: `func_L_q`·`curve()` — `I`는 SI[A], `c_rate`→`I` 환산(`I=c_rate·Q_cell/3600` 또는 `Q_cell`을 [C]로) 명시. 수치 결과 **bit-exact 보존**(주석+선택적 명시 상수), dH_a 물리해석 정합.

---

## Phase R0 — 착수·v1.0.24 골격복제·시드값 확정 (Steps 32-35)

- **Step 32**: `docs/v1.0.24/` = v1.0.23 복제(빌드 GREEN 확인) + `Anode_Fit_v1.0.24.py` = v1.0.23 복제(import·게이트 통과 확인). 시작점 bit-exact.
- **Step 33**: **시드표 확정** `REFLECT_SEED_TABLE.md` — (a) Si Frumkin: Ω_Si/RT(고용체, regsol_si δ캡 결과·Artrith/Braga 근거)·U_j. (b) 흑연 5-feature: 각 전이 U_j(XRD Dahn)·Ω(>2RT/<2RT)·ΔS(2L Δ≈29). 전부 **실측·문헌 앵커 명기**(무근거 값 금지).
- **Step 34**: **단위계약 스펙** — #1 정정 방식 확정(bit-exact 보존 경로: 주석+환산상수). curve()/dqdv() 수치 불변 증명 설계.
- **Step 35**: `PHASE_R0_RESULT` + ledger 초기화.
- **게이트**: (1)v1.0.24 골격 빌드/import GREEN·bit-exact. (2)시드표 전 값 문헌·실측 앵커 有. (3)단위계약이 곡선 불변 보장하는가 스펙 명시. (4)P4 착수 체크리스트 8항.

## Phase R1 — 코드 반영 (@3·@5·#1) (Steps 36-41)

- **Step 36**: **@3 Si Frumkin 커널** 구현 — `func_ksi_regsol`/전이 kernel 플래그. Ω<2RT 유한 broad peak. 로지스틱 폴백 bit-exact.
- **Step 37**: **@5 5-feature staging** — `GRAPHITE_STAGING_XRD_v1024` dict(5전이·Ω·ΔS 시드). 4↔3=고용체 shoulder(Ω<2RT). 기존 4전이 폴백 보존.
- **Step 38**: **#1 단위계약** — `func_L_q`/`curve()` 환산 명시. **bit-exact 회귀**(v1.0.23 vs v1.0.24 동일입력 곡선 max-abs-diff=0 확인).
- **Step 39**: **f_Si=0 흑연 회수 bit-exact** + **기존 4전이 폴백 bit-exact** 회귀 테스트.
- **Step 40**: 코드 게이트 실행(import·example·기존 검증 스위트 GREEN).
- **Step 41**: `PHASE_R1_RESULT`.
- **게이트**: (1)@3·@5·#1 구현 완료. (2)**bit-exact 3종**(f_Si=0·4전이폴백·단위계약) max-diff=0. (3)Si Frumkin·5-feature 곡선 물리 타당(연속·매끄러움·유한 peak). (4)게이트 스위트 GREEN.
- **중단 조건**: bit-exact 깨지면(신규가 기존경로 오염) 즉시 분기 격리 재설계.

## Phase R2 — 문건 반영 (@3·@5 절·#1·#7 정정) (Steps 42-47)

- **Step 42**: **Si 고용체 절** — Si-host 정칙용액(Frumkin Ω<2RT) 유도·`dQ/dV` 식·왜 두-상 아닌가(폭≳RT/F). 서지: Chevrier-Dahn 2009·Artrith 2018·Verbrugge 2017(ω 형식).
- **Step 43**: **stage-2L 절** — XRD 5-feature 상구조(Dahn 1991)·2L 엔트로피 안정화·T-분리(∂U/∂T=ΔS/F, Δ≈29)·Ω>2RT/<2RT 판정자. 서지: Dahn 1991·Schmitt 2022·Reynier 2004.
- **Step 44**: **중간다리** — 신규 두 절이 기존 §3(흑연)·§3.5(블렌드)·§7(브로드닝)과 충돌 없이 연결(전달식 정합).
- **Step 45**: **Codex 정정** — #1 단위계약 문건 명기(kinetic 절), #7 sec13:154 "Ω 유효 평균장 축약" 문구 명확화(#5·#6 LCO 근사 라벨 강화).
- **Step 46**: 전역 컨벤션·용어·기호(V_n 구분 등 P3-1)·어조 통일 + 빌드.
- **Step 47**: `PHASE_R2_RESULT`.
- **게이트(P3 적용)**: (1)V_n/V_{n,app}/V_{n,drive}/V_{n,OCV} 구분 일관(P3-1). (2)신규 절이 Chapter 기준식과 무충돌(P3-6). (3)ver.N↔Chapter 명칭 혼동 없음(P3-7). (4)서지 전건 실재·검증가능(무인용 금지). (5)빌드 GREEN.

## Phase R3 — 반영 검증 (개선 재현·회귀·P3) (Steps 48-51)

- **Step 48**: **개선 재현** — v1.0.24 코드로 동일 블렌드(sigr_aq1) 재피팅 → @3(Si Frumkin)+@5(5-feature) R² 개선이 ablation 값(+0.66/+0.9%p대)과 정합하나.
- **Step 49**: **T-분리 재현** — v1.0.24 5-feature+ΔS로 T_split(45℃ 2피크/25℃ 병합·0.30 mV/℃) 재현.
- **Step 50**: **회귀·안정성** — @5가 물리 시드로 **안정**(다런 편차 축소)한가. 흑연 단독·다중 블렌드셀 회귀.
- **Step 51**: `REFLECT_VERIFY.md` + `PHASE_R3_RESULT`.
- **게이트**: (1)블렌드 개선 재현(R² ablation 정합). (2)T-분리 재현. (3)@5 물리시드 안정성(자유피팅 대비 편차↓). (4)기존 검증(MSMR·M제거·블렌드가산) 무회귀.

## Phase R4 — 적대 검수·마감 (Steps 52-55)

- **Step 52**: 독립 적대적 검수(≥3창) — 코드↔문건 정합·bit-exact 계약·신규 서지 무결·물리 타당(Si 고용체·5-feature).
- **Step 53**: triage·치명/주요 집행·재빌드.
- **Step 54**: `MERGE_READINESS_v1024.md`·`HANDOVER`·INDEX.
- **Step 55**: `PHASE_R4_RESULT`·최종 커밋·푸시.
- **게이트**: 치명 0·빌드 GREEN·bit-exact 3종 검증·개선 재현 스크립트 커밋.

---

## Implementation Interfaces

- **Si Frumkin 커널**: `ξ_regsol(V;U,Ω,θ)` — 정칙용액 site-fraction(Ω<2RT 단일상). `dQ/dV=Q·F/|RT/(θ(1−θ))−2Ω|`. 전이 dict `{'kernel':'regsol','Omega':<2RT}`; 미지정=로지스틱(폴백).
- **5-feature staging**: `GRAPHITE_STAGING_XRD_v1024=[1′↔4, 4↔3(shoulder), 3↔2L, 2L↔2, 2↔1]`, 각 `{U,Omega,dS_rxn,Q,n}`. 기존 `GRAPHITE_STAGING_LIT`(4) = deprecated 폴백 보존.
- **단위계약**: `curve(c_rate,...)`: `I[A]=c_rate[1/h]·Q_cell[Ah]` → `func_L_q`의 `T_attempt`에 `/3600` 명시 or `Q_cell` [C] 규약. **결과 bit-exact**.
- **메트릭**: R²·RMSE(블렌드), T-분리 기울기(mV/℃)·병합온도, bit-exact max-abs-diff, 물리성(연속·C¹·유한 peak).
- **문서**: Result 11항·Ledger 12-col([[feedback_phase_execution_loop]]).

## Test Plan

- **bit-exact 3종**: (a)f_Si=0→흑연 v1.0.23 동일, (b)기존 4전이 폴백→v1.0.23 동일, (c)#1 단위계약 전후 곡선 동일. 전부 max-abs-diff=0.
- **@3 재현**: 블렌드 Si Frumkin 피팅 R² ≈ ablation(+0.66%p대).
- **@5 재현·안정**: 5-feature 피팅 R² + T-분리(0.30 mV/℃·병합~10℃) + 다런 편차 축소(물리시드 효과).
- **물리 타당성**: 신규 곡선 연속·매끄러움·미분가능·유한 peak(v1022/23 샘플이미지 기준 재적용).
- **무회귀**: MSMR 동형·M제거·블렌드 가산·U_j 일관 — 기존 검증 재통과.
- **서지 검증**: 신규 인용 전건 실재(무인용 금지).
- **재현성**: 반영 검증 스크립트·시드표 커밋.

## Assumptions

- Si Frumkin Ω_Si는 regsol_si(δ캡)+문헌(Artrith/Braga)로 **범위 시드** 가능(정확 fitted Ω_Si 단일 문헌 부재=D1 갭 → 범위·피팅위임).
- 흑연 5-feature U_j·ΔS는 Dahn 1991·우리 T-split로 앵커 가능(MCMB≠임의흑연 폭 차이는 자유 폭이 흡수).
- @5 물리 시드가 자유피팅 불안정을 제거(국소최소 탈출) — R3 Step50서 실증(실패 시 4전이 유지 폴백).
- #1 단위계약이 곡선 bit-exact 보존(dH_a는 tier-C placeholder라 재피팅서 재흡수).
- v1.0.23 빌드 툴체인 v1.0.24서 동일 동작.

## Correction History

- 직전(검증 campaign) → **반영 campaign 전환**: C·A·B·문헌 검증 완료 → 사용자 "가자"(@3·@5·Codex#1). 무수정 원칙 해제(v1.0.24 신 버전 한정).
- @5 재평가: 개별 ablation −0.44(불안정)였으나 **XRD 확증 상(2L)**·물리 시드 시 안정 → 사용자 선택 반영(자유피팅이 아니라 **물리 시드**로 구현하는 조건).
- Codex 정정 범위 축소: 7건 중 실제 반영 = #1(코드)·#7(문구)만. #5·#6은 실 O3 부재로 **라벨 강화**만(구현 보류) — 데이터 없이 손대면 검증 불가.
- LCO 반영 제외 확정: 실측 O3 numeric 부재(A트랙 확인) → 이번 스코프 밖.

---

## 확정 사항 (사용자 이미 결정 — 재질문 안 함, [[feedback_user_decision_no_requery]])

이 세션서 사용자가 명시 결정한 것 — 재질문 대상 아님. 그대로 집행:
1. **@3·@5 를 흑연·블렌드·LCO 전부 반영** (사용자 "3,5 최종 선택" + "@3·@5 LCO 동일 적용" 확인).
2. **@5 = XRD 5-feature 물리 시드**(자유 peak 아님) — Dahn1991·T-split 근거.
3. **LCO 전자항 = 코드 on/off 토글**(커브 OFF·∂U/∂T ON옵션·챕터 남김) — 사용자 안 A verbatim.
4. **#1 단위계약 = bit-exact 보존**(곡선 불변·dH_a 해석만 정정) — 사용자 "빼고 옵션" 취지 정합.
5. **#7 문구 정정** 반영·#5/#6 = 토글로 자연 해소·#3 불요.
6. **Ref 6,7 = 이미 반영(v1.0.23 부록 E)** + 이번에 Ref6 제목·DOI Crossref 확정(10.1063/1.3565476) → bib 기록 완료. Ref7(10.1063/1.4802584)은 기확정.
7. **버전 = docs/v1.0.24/ + Anode_Fit_v1.0.24.py** additive·v1.0.23 보존.

## 집행 방식 ([[feedback_work_execution_methodology]] 준수)
- **GO 후 무중단 자율** — 팝업 0·질문은 완료보고 일괄. 정지 5조건만.
- **4-세션 분업**: master(통합·commit) + 작업 sub(코드/문건 구성) + 검수 sub(정합·게이트) + 검토 sub(사양 대조). 단일 세션 자기검사 금지.
- **단위 구성 루프**: 절/함수/데이터블록 하나씩(통째 Write 금지)·정독 행범위·무수정도 사유 기록·orphan 0.
- **N회 가변-청크 검수**: 반영분에 렌즈 로테이션(구조/물리 적대검산/G-follow/G-usable/시각) 수렴까지.
- **원본 불가침**: v1.0.23 프리즈·v1.0.24 신 디렉토리서만 작업.

> **남은 유일 사용자 입력 = "R0 GO"** (또는 특정 항목 조정). GO 시 위 방식대로 R0(골격복제·시드표)부터 마감까지 무중단 집행.
