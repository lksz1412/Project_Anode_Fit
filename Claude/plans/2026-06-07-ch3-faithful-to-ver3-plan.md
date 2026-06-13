# Ch3 보완 계획서 — 박사님 원천 ver.3 항목 충실 (v2, 이전 plan supersede)

> ★ 이 계획은 `2026-06-07-ch3-content-overhaul-plan.md`(v1)를 **폐기·대체**한다. v1은 Marcus·dQ/dV 지문·nucleation 등 **ver.3에 없는 내용을 Claude가 발명**한 잘못된 계획이었다.
> 권위 출처: 박사님 authored 원천 `Claude/docs/Archive_old/graphite_ica_dynamic_ver5.tex` **ver.3 (line 856–1118)** = Chapter 3 원안. + 현 트랙 합의 `RB_CHARTER.md`(s_φ/V_drive/n_eff/keystone) · `RB_LEDGER_CH3.md`.
> 원칙: **없는 내용 발명 금지.** 보완 대상 = 박사님이 ver.3에 제시한 항목 중 현재 Ch3에서 빠지거나 부실한 것의 복원·전개.

## 1. Summary

박사님 지적("Ch3 내용 부실 + 내가 제시한 항목으로")은 원천 ver.3 대조로 실체가 확인됐다. 현재 Ch3는 박사님 ver.3의 **구체 전기화학 항목(Tafel·대칭 BV sinh/asinh 역함수·교환전류 i₀(q,T) 조성의존·모델 선택)을 빠뜨린 채**, rebuild-framework 추상(n_eff·detailed balance·Level A/B keystone·generalized affinity·R_n 5분해·C-rate 𝓕)으로 부피만 키운 상태다. 즉 "부실"은 유도 깊이 이전에 **다루는 항목이 박사님 원안과 어긋난** 문제다. 본 계획은 (A) ver.3의 빠진 항목 복원, (B) ver.3의 부실 항목 전개, (C) ver.3에 없는 rebuild 추가물의 거취를 박사님 결정에 회부, (D) Claude 발명 토픽 전면 폐기로 Ch3를 **박사님 ver.3에 충실**하게 되돌린다.

## 2. 박사님 ver.3 항목 인벤토리 (권위 = 원천 line 856–1118)

원천이 명시한 Chapter 3 항목(절 단위):
1. **반응속도론 계층 도입** — 평형 위치(OCV 기준 ξ_eq)와 동역학 속도(𝒜_j 기준 k_j)의 \emph{분리} 원칙. (eq:v3_xieq_rule, v3_k_basic)
2. **전위 보조 구동력 일반화** — 𝒜_j=s_φF(V_app−U_j) (simple) → 𝒜_j=Fη_j (반응 과전압형), ΔG_eff=ΔG_a−χ_jFη_j. + 중복 반영 방지 note(reduced vs reaction-resolved).
3. **Butler–Volmer식과 η_j** — i_j=i_{0,j}[exp(α_jFη/RT)−exp(−(1−α_j)Fη/RT)].
   - 3a **저과전압 선형 근사** — i_j≈i_0 Fη/RT, R_ct,j=RT/(F i_{0,j}).
   - 3b **대칭 BV 역함수(sinh/asinh)** — i_j=2i_0 sinh(Fη/2RT), η=(2RT/F)asinh(i/2i_0), ΔG_eff=ΔG_a−2χ_jRT·asinh(i/2i_0).
   - 3c **Tafel 근사** — 큰 +η: η≈(RT/α_jF)ln(i/i_0); 큰 −η: i≈−i_0 exp(−(1−α)Fη/RT). branch·부호 convention 명시.
4. **교환전류밀도와 온도 의존성** — i_{0,j}(q,T)=i_{0,ref} f_{i,j}(q) exp[−E_{i,j}/R(1/T−1/T_ref)]; ν_j(T) 동형; i_0·ν·ΔG_a·χ 상관 경고.
5. **forward/backward rate** — dξ/dt=k⁺(1−ξ)−k⁻ξ; k±=ν±exp[−(ΔG_a±∓χ±𝒜)/RT]; relaxation form 환원 → ξ_eq=k⁺/(k⁺+k⁻), k_relax=k⁺+k⁻.
6. **전류 분배와 상변이 전류** — I_j=Q_{j,tot}dξ/dt, I=I_bg+ΣI_j.
7. **reaction-resolved vs reduced vs Hybrid 모델 선택** — 3-모델 표(구동력 표현·사용 상황). reduced 먼저, 잔차 체계적이면 reaction-resolved 확장.
8. **반응속도론 계층의 식별성** — 상관 파라미터 표(ν/ΔG_a, χ/R_n, i_0/η/χ, w/k, Q/ξ) + 권장 처리.
9. **ver.3 피팅 절차** — 6-step.
10. (ver.4 전달식·검수 체크리스트 = 계층 인계용, 단일 통합 문건에선 불요)

## 3. 현재 Ch3 ↔ ver.3 대조 (grep 검증)

| ver.3 항목 | 현재 Ch3 상태 | 조치 |
|---|---|---|
| 1 평형/속도 분리 | 있음(§2·§3 변형) | 유지 |
| 2 𝒜_j=Fη_j·ΔG_eff·중복반영 note | 부분(𝒜_j 일반형은 n_eff형으로 대체됨) | ver.3 단순형과 정합 점검 |
| 3 BV식 | 있음(§6, eq:ch3_bv) | 유지 |
| **3a 저과전압 선형→R_ct** | 있음(§6.1, 전개됨) | 유지(강) |
| **3b 대칭 BV sinh/asinh 역함수** | ★**부재(sinh 0회)** | ★**복원** |
| **3c Tafel 근사** | ★**부재(언급 3회뿐, 유도 없음)** | ★**복원** |
| **4 교환전류 i₀(q,T) 조성의존 f_{i,j}(q)** | 부실(T-의존만, 조성 f_{i,j}(q) 없음) | ★**전개 복원** |
| 5 forward/backward + relaxation 환원 | 있음(§3·§4, 전개됨) | 유지(강) |
| 6 전류 분배 I=I_bg+ΣI_j | 있음(§8 current conservation) | 유지 |
| **7 reduced/reaction-resolved/Hybrid 모델 선택** | ★**사실상 부재(표 없음)** | ★**복원** |
| 8 식별성 표 | Ch6로 이관됨(D2b) | **DG2 결정**(Ch3 복귀 vs Ch6 유지) |
| 9 피팅 절차 | Ch6로 이관 | **DG2 결정** |

**현재 Ch3에 있으나 ver.3엔 없는 rebuild 추가물(거취 = DG3):**
- n_eff=RT/(Fw_j) 형식주의·detailed balance 정식 treatment·Level A/B keystone 한정 — CHARTER 합의 framework(s_φ/V_drive/n_eff/keystone). 유지 권장(합의됨)이나 ver.3 대비 비중 과다.
- generalized affinity 𝒜_n=Fη_n+𝒜_resid — ver.3 없음(ver.3은 𝒜_j=Fη_j까지). rebuild 확장.
- R_n 5-항 전기화학 분해 — ver.3 없음(ver.3은 중복반영 note 수준). rebuild 확장.
- C-rate 재분해 𝓕(·) 함수 — ver.3 없음. rebuild 발명(정의 없는 함수 = skeleton).

**Claude(나)가 v1 plan에서 발명한 것 — 전면 폐기(ver.3 무관):** Marcus-Hush/λ, dQ/dV·ICA/DVA 지문 표, nucleation/Avrami, 농도 과전압 신규 유도장, 극한영역 taxonomy, 그림 6종. **추가 안 함.**

## 4. 보완 접근 / 원칙

1. **발명 금지·복원 우선**: 새 토픽 도입 X. 보완은 ver.3 항목의 복원(3b·3c·4·7)과 present 항목의 ver.3 충실 전개에 한정.
2. **박사님 원천 식 그대로**: 복원 항목의 식은 ver.3 원식(sinh/asinh·Tafel·i₀(q,T) 등)을 기준으로, 현 Ch3 표기(s=+1, n_eff, 식번호 3.x, 𝒜_j=Fη_j)와 정합시켜 이식. 식별자·라벨 보존(P5).
3. **rebuild 추가물은 임의 삭제 X**: DG3에서 박사님이 "유지/축소/제거" 결정. 제거 결정 전엔 보존.
4. **식별성·피팅(8·9) 거취는 DG2**: 박사님 ver.3은 Ch3에 뒀음. 단 이후 "식별성=피팅장(Ch6) 분리" 결정(Ch1 부록 패턴)이 있었음 → 박사님 재확인.
5. **register는 현 Ch2/Ch3 교과서체 유지**. 형식(D2b)은 건드리지 않음.

## 5. 작업 항목 (DG 확정 후 확정)

- **W1 [복원] 대칭 BV 역함수(sinh/asinh)** → §6에 subsection: i=2i₀sinh(Fη/2RT) 유도(α=½ 특수형), η=(2RT/F)asinh, ΔG_eff=ΔG_a−2χRT·asinh. (ver.3 §대칭 BV 역함수)
- **W2 [복원] Tafel 근사** → §6에 subsection: 큰 ±η 극한 전개, η≈(RT/αF)ln(i/i₀), branch 부호 convention. (ver.3 §Tafel)
- **W3 [전개] 교환전류 i₀(q,T)** → §교환전류 subsection 복원: i₀(q,T)=i₀,ref f_{i,j}(q)exp[−E_i/R(1/T−1/T_ref)], 조성 활성도 f_{i,j}(q) 의미, i₀·ν·ΔG_a·χ 상관. (ver.3 §교환전류밀도와 온도 의존성)
- **W4 [복원] 모델 선택 표** → reduced/reaction-resolved/Hybrid 3-모델 표 + reduced 먼저 절차 원칙. (ver.3 §model 선택)
- **W5 [정합] 𝒜_j 단순형** → ver.3 𝒜_j=Fη_j·ΔG_eff=ΔG_a−χFη_j·중복반영 note가 현 n_eff형과 모순 없이 양립하는지 점검·정합.
- **W6 [present 전개]** → ver.3 항목 중 현재 thin한 곳(있으면) ver.3 깊이로 보완. (depth는 ver.3 기준, graduate-textbook 확장 아님.)
- (DG2 결정 시) **W7 식별성·피팅** Ch3 복귀 또는 Ch6 유지 정리.
- (DG3 결정 시) **W8 rebuild 추가물** 유지/축소/제거(특히 C-rate 𝓕 skeleton).

## 6. Steps (cumulative; 이전 S64 이후)

- S65: DG1~DG3 박사님 확정 (실행 전).
- S66: W5 정합 점검(𝒜_j 단순형 ↔ n_eff형) → 충돌 시 Correction.
- S67: W1·W2 (sinh/asinh + Tafel) §6 복원·이식.
- S68: W3 (i₀(q,T) 조성의존) 복원.
- S69: W4 (모델 선택 표) 복원.
- S70: (DG2/DG3 결과) W7·W8.
- S71: 빌드 + Codex foreground 검수(ver.3 정합·부호·식 이식 정확성) until clean.
- S72: 커밋·푸쉬 + result ledger.

## 7. Gates (확인 가능 조건)

- G-fidelity: ver.3 §3b·§3c·§4·§7 항목이 Ch3 본문에 복원됨 — grep(sinh≥1, Tafel 유도 블록, f_{i,j}(q), 3-모델 표) 확인.
- G-source-eq: 복원식이 ver.3 원식과 일치(sinh/asinh·Tafel·i₀(q,T) 형태) — 식별자별 대조.
- G-consistency: W5 𝒜_j 단순형↔n_eff형 충돌 0 (충돌 시 Correction History).
- G-no-invent: Marcus/dQ-signature/nucleation/그림 등 ver.3 외 토픽 본문 부재 — grep 0.
- G-build: xelatex 2-pass exit 0, undefined ref 0, overfull 0.
- G-preserve: 기존 라벨·식번호·present 완전유도식 불변.
- G-codex: Codex 물리/부호/ver.3 정합 검수 MAJOR 0.

## 8. Decision Gates (박사님 결정 — 실행 전)

- **DG1 (보완 범위)**: ① ver.3 빠진 항목 복원만(W1~W4, **권장** — "내가 제시한 항목" 충실) / ② 복원 + present 항목 ver.3 깊이 전개(W1~W6) / ③ 복원 + rebuild 추가물 정리까지(W1~W8, 전면 재정렬).
- **DG2 (식별성·피팅, ver.3 §8·§9)**: ① Ch6 유지(현재, 식별성=피팅장 분리 패턴) / ② Ch3로 복귀(ver.3 원안대로). 박사님이 Ch1에서 "식별성 따로 빼라" 하신 것과의 정합 확인 필요.
- **DG3 (rebuild 추가물 거취)**: n_eff/detailed-balance/Level A·B keystone(CHARTER 합의) = 유지 기본. generalized affinity 𝒜_resid · R_n 5-분해 · C-rate 𝓕(·) = ① 유지 / ② 축소 / ③ 제거(특히 정의 없는 𝓕 skeleton). 박사님 판정.
- **DG4 (Ch4·Ch5도 동일 대조 필요?)**: Ch4(ver.4)·Ch5(ver.5)도 ver.N 원안 대비 동일 이탈 가능성. Ch3 확정 후 동일 대조를 Ch4·Ch5에 적용할지.

## 9. Risks

- R1(식 이식 오류): ver.3 원식을 현 표기(s_φ, n_eff, 식번호)로 옮길 때 부호·계수 오류 → 매 식 ver.3 대조 + Codex(S71).
- R2(rebuild 추가물 임의 제거): DG3 미확정 상태 제거 금지(보존 기본).
- R3(또 발명): 복원 과정서 graduate-textbook 토픽 재유입 → G-no-invent grep으로 차단.
- R4(중복): 현 Ch3에 BV/R_ct 이미 있음 → W1·W2는 그 절(§6)에 이어 붙여 중복 회피.

## 10. Validation

각 W 직후 G-fidelity·G-source-eq 부분 점검. S71서 전 Gate + Codex MAJOR 0 + ver.3 대조 전수. 통과 전 커밋 금지.

## 11. Correction History

- 2026-06-07 v2: 최초 작성. v1(`...content-overhaul-plan.md`) **폐기** — v1은 박사님 ver.3을 확인 않고 Marcus·dQ/dV 지문·nucleation 등 발명. 박사님 지적("내가 제시한 챕터 구조 찾아라, 발명 말고") 수용. 권위 = 원천 ver.3(line 856–1118) 전문 정독 + 현재 Ch3 grep 대조. 범위/식별성거취/rebuild추가물은 DG1~DG3 박사님 확정 대기. **본 계획 GO 전, 실행하지 않음.**
