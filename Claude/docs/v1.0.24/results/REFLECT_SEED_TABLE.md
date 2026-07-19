# v1.0.24 반영 시드표 (R0) — @3·@5·LCO토글·#1·#7 의 확정 물리·값·근거

> R1(문건 저작)·R2(코드)의 사양 원천. 모든 값 = 이 세션 실검증 산출물 근거(파일 명기). 무근거 값 0.
> 원칙: v1.0.23 물리 서사·기존 식·라벨·변수명 보존(P5). 신규 = additive·폴백 bit-exact.

## 1. @3 — Si-host 정칙용액(Frumkin, Ω<2RT 고용체) 커널
| 항목 | 값·식 | 근거 |
|---|---|---|
| 물리 판정 | a-Si = **단일상 고용체**(sharp 두-상 아님) | `regsol_si.png`: 폭/(RT/F)=[1.45,2.74,1.09]≳1 (흑연 두-상 ≪0.12) |
| 커널 형태 | Frumkin 단일상 peak: `dQ/dV = Q·F / |RT/(θ(1−θ)) − 2Ω|`, Ω<2RT | 정칙용액 μ(θ)=μ°+RT ln[θ/(1−θ)]+Ω(1−2θ) |
| Ω_Si 시드 | Ω<2RT (δ물리캡시 바닥 0.2RT 지향 = 넓은 고용체); 피팅 위임(범위 시드) | `regsol_si` δ캡 결과·`regsol_si_result.json` |
| 개선효과 | 블렌드 R² +0.66%p(음극)·+1.25%p(LCO per-peak Ω) | `ablation_result.json`·`lco_ablation_result.json` |
| 서지 | Chevrier-Dahn 2009(JES156,A454)·Artrith 2018(JCP148,241711)·Verbrugge 2017(JES164,E3243 — ω 형식) | `lit_raw/03_graphite_si.md` |
| 코드 지점 | `equilibrium`/`dqdv` 의 Si-host 전이에 kernel 분기(`kernel:'regsol'`), 미지정=로지스틱 폴백(bit-exact) | `Anode_Fit` L538/624 |

## 2. @5 — 흑연 XRD 5-feature staging (stage-2L 포함)
| # | 전이 | ~V(리튬화) | Ω 성격 | ΔS_rxn 시드 | 근거 |
|---|---|---|---|---|---|
| 1 | dilute 1′↔4 | ~0.21 V | 두-상 sharp(Ω>2RT) | +29 J/mol/K(dilute 양수) | Dahn1991·`GRAPHITE_STAGING_XRD.md` |
| — | 4↔3 | ~0.14–0.20 V | **고용체 shoulder(Ω<2RT)** | ~0 | Dahn1991 예외(연속) |
| 2 | 3↔2L | ~0.13 V | 두-상 sharp(Ω>2RT) | **+15**(2L 분리쌍 고V) | T-split(Δ(ΔS)=29) |
| 3 | 2L↔2 | ~0.115 V | 두-상 sharp(Ω>2RT) | **−14**(2L 분리쌍 저V) | 〃 |
| 4 | 2↔1 | ~0.085 V | 두-상 최sharp | −16 | Dahn1991 |
- **Ω>2RT 실측 검증**: regsol2 Ω/RT=[4.06,2.02,3.55,4.07] 전부>2RT(두-상 확증). `regsol2.png`
- **T-분리**: 3↔2L·2L↔2 Δ(ΔS)=29 → 분리 0.30 mV/℃·병합~10℃·45℃ 2피크/25℃ 병합. `T_SPLIT_FINDING.md`(재현 0.271 mV/℃)
- **LCO @5**: H1/H2·x0.5 order-disorder·H1-3 미세구조 세분 → +1.90%p. `lco_ablation`
- **경계**: XRD 5-feature가 상한(Dahn). 6+ = curve-fitting(폐기 유지).

## 3. LCO 전자 엔트로피 = on/off 토글 (사용자 안 A)
| 항목 | 값 | 근거 |
|---|---|---|
| 현 상태 | ΔS_e≈−45.7 J/mol/K, `_effective_dS_rxn` LCO 서브클래스, T_ref 동결 | `Anode_Fit` L1005·L963 |
| 상온 영향 | **0**(dH가 ΔS_e 흡수, ∂U/∂T에만 작용 — 코드 L956 명시) | `LCO_DIAGNOSIS.md` |
| 반영 | 플래그 `include_electronic_entropy: bool=False`(기본) 추가. 커브=OFF(잉여)·∂U/∂T=ON옵션 | 회사 다온도 데이터로 영향 확인용 |
| bit-exact | 기본 OFF → 기존 커브 불변? **주의**: 현 코드는 ΔS_e 상시 ON. 토글 OFF가 dH 재기준 필요(U(298) 보존) — R2서 U(298) 불변 보장 | R2 게이트 |
| 챕터 | ch2 LCO 챕터 **남김**, 전자항 절에 "커브 불필요·∂U/∂T 선택" 명시 | 사용자 A |

## 4. #1 — C-rate/Eyring 단위계약 (bit-exact)
| 항목 | 값 | 근거 |
|---|---|---|
| 문제 | `func_L_q` `T_attempt=(I/Q_cell)·h/kB`, c_rate[1/h] vs k_0=k_BT/h[1/s] → 3600× 불일치 | `CODEX_REVIEW_VERIFICATION.md` #1 |
| 영향 | 곡선 무영향(dH_a tier-C에 흡수)·dH_a 물리해석만 ~20 kJ/mol 이동 | 〃 |
| 반영 | 단위계약 명시(주석+환산상수, `I` SI[A] or /3600). **곡선 bit-exact 보존**(max-diff=0) | R2 게이트 |

## 5. #7 — LCO Ω 문구 정정
| 항목 | 값 | 근거 |
|---|---|---|
| 지점 | ch2 LCO `eq:lco-...`(구 sec13:154) "Ω>2RT ⇔ x½ 질서상 안정" | `CODEX_REVIEW_VERIFICATION.md` #7 |
| 정정 | "Ω_j^cat = 유효 평균장 축약(전이당 진행좌표)·config 엔트로피 별도 슬롯" 명확화. 물리 유지·문구만 | 부분정타 |

## 6. Ref 6,7 (완료 — 재작업 불요)
- Ref6 = Lee 외, "Communication: Propagator for diffusive dynamics of an interacting molecular pair," JCP134,121102(2011). **DOI 10.1063/1.3565476** (bib 기록 완료).
- Ref7 = Son 외, JCP138,164123(2013). DOI 10.1063/1.4802584(기확정). 방법 = 부록 E(v1.0.23 반영).

## 반영 범위 (S/A 변경 분류)
- **A(augment)**: ch1 stage-2L 절·ch3 Si 고용체 절·ch2 LCO @3/@5 절 신규.
- **E(extension)**: 코드 regsol 커널·5-feature staging·전자항 토글·단위계약.
- **C(correction)**: #7 문구·bib ref6 DOI(완료).
- **보존**: 기존 4전이 폴백·로지스틱 폴백·f_Si=0 흑연 회수 전부 bit-exact.
