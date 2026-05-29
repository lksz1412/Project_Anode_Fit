# 합류(Consolidation) 로드맵 — 단일 spine Chapter 1~6 (G-series 설계도)

**Date**: 2026-05-29 · **상태**: **로드맵(설계도) — G-series 본문 재작성은 별도 GO 대기.**
**입력**: `PHASE_DIAG_INTENT_GAP_RESULT.md`(진단), `PHASE_DIAG_SALVAGE_LEDGER.md`(salvage), `2026-05-29-intent-gap-diagnosis-consolidation-plan.md`(§00 GS-1~4, North Star N-1~N-5).
**지배 표준**: §00 GS-1~4 (학부 무비약 / 전문 깊이 / grounded 가정 / 과도가정 배제) — 매 식·매 절 적용.
**원칙**: 확장이 아니라 **(B) 폭 × (A) 깊이 합류 + N-1·N-2·keystone 보강**. 신규 물리 발명 최소화, 이식·정합·명명·서사가 주.

---

## §1. 합류 설계 한 장 요약

```
 트렁크 = (B) 전하보존 6장 (폭 + 물리 규율)
   └─ Ch1 ── ★(A) tail 엔진 이식 + ★keystone Level A 재명명 + ★피팅식(N-2) 박기 + ★서사 head(N-1)
   ├─ Ch2 ── 발열 연결 (Ch1 dξ/dt 그대로)
   ├─ Ch3 ── 반응속도론 (★keystone Level B = forward/backward, χ=β)
   ├─ Ch4 ── 발열 (Ch3 flux–force entropy production)
   ├─ Ch5 ── 충방전·히스테리시스 (Ch3 Level B branch 확장)
   └─ Ch6 ── 수치·검증 (★(A) Refs6/7 = 가속 검증 tier; 보유 데이터 N-4)
```
keystone 단일 결정(Ch1 Level A / Ch3 Level B)이 6장 전체에 무모순 전파(RESULT §C, plan §6.8).

---

## §2. 서사 척추 (N-1) — 관찰에서 출발하는 단일 인과 사슬

합류 문서 **머리(序)**에 박을 추진 서사 (각 장 서두 1문단으로 재호출 = Observation Anchor):

> (관찰) 저온일수록 dQ/dV peak 꼬리가 길어져 다음 peak와 겹친다.
> (가) 평형 열역학만으로는 안 된다 — 평형폭 `w=RT/F`는 저온서 **좁아져** 꼬리가 짧아질 것을 예측(관찰과 반대). [학부 chain: plan §6.2]
> (나) 따라서 꼬리는 **동역학**이다 — `k=k_0exp(−ΔG_a/RT)` 저온 감소 → lag↑ → `L=|I|/(Q_cell k)`↑ → 꼬리 길어짐(관찰 일치).
> (다) 그 배리어는 **극판 전위로 낮춰진다**(전류 인가 시 OCV와 다름) → C-rate 겹침. [Ch1 Level A 가속 / Ch3 Level B 방향성]
> (라) 이를 **전하보존으로 V_n을 풀어** 정량화하고(무대=열역학), 꼬리 깊이는 **relaxation-length spectrum**으로 설명(주역=동역학).
> (마) 결과 = **피팅 가능한 닫힌 논리식**(Ch1 말미). 이후 발열(Ch2,4)·히스테리시스(Ch5)·수치검증(Ch6)으로 확장.

→ **열역학 무대 + 동역학 주역.** 이 한 문장이 "거리"의 핵심(N-1)을 닫는다.

---

## §3. 합류 Chapter 별 설계 (salvage 출처 · N-조건 · GS gate)

### 합류 Ch1 — 전하보존 + 유효배리어 + tail 엔진 + 피팅식 (의도 ④; 가장 큰 작업)
- **trunk(KEEP-B)**: charge-balance V_n, 전위 3분, 온도 tail 3계층, C-rate 정확식.
- **engine 이식(KEEP-A)**: barrier→length 지수매핑 `eq:L_of_G`, kernel integral `eq:kernel_integral`, Marcus bound, spectrum T/ψ shift, χ-discriminator, non-uniqueness forward-only.
- **FIX**: F-1 keystone → χ𝒜 = **Level A mobility 가속**으로 명명("유효 배리어 낮춤" 표현은 Ch3로 이관 예고). F-2 서사 head. F-3 ★피팅식. F-4 flux clamp. F-5 ξ 통일.
- **★N-2 피팅식 (Ch1 말미 박스)**: 평가순서 inner→outer 명시
  `k(G,T,V_drive)=k_0(T)exp[−(ΔG_a−χ𝒜)/RT]` → `L(G)=|I|/(Q_cell k)` → `A_L(L)=ρ_G(G(L))·(RT/L)·A_0` → `dΘ_tail/dq=∫A_L(1/L)e^{−(q−q_a)/L}dL` → `dQ/dV_n=C_bg/(1−Q_p dΘ/dQ)`. 유효범위 `ΔG_eff≥0`(Marcus), `V_drive≈U_j+O(w)` 병기.
- **GS gate**: 각 식 prose-먼저+무생략(GS-1); 가정 AL 인용(GS-3); cap/clip 0, Marcus bound 병기(GS-4).
- **충족**: N-1 head, N-2 식, N-3 전위·전류, N-5 grounding.

### 합류 Ch2 — 발열 연결 (의도 ⑤)
- KEEP-B: `dV_app/dT≠(∂V_OCV/∂T)_q` 금지, 평형 온도계수, 가역/비가역/relaxation heat 차원 연결.
- keystone 전파: Ch1 Level A `k` 사용 → 가역열=thermo(ξ_eq), 비가역열=flux (이중계상 금지).
- GS gate: 모든 heat 항이 보존/entropy/affinity 근거(GS-3,4). 확정은 Ch4 위임.

### 합류 Ch3 — 반응속도론 (의도 ⑥; ★keystone Level B 장)
- KEEP-B: forward/backward, detailed balance `ln(r+/r-)=(V_n−U)/w`, `ξ_ss`, BV, `R_n≠R_ct≠R_n,eff`, 전류 보존 saturation.
- **FIX F-1**: χ=β transfer coefficient로 **Level B** = forward `−β𝒜` / backward `+(1−β)𝒜` (`eq:ch3_phys_rplus_act/rminus_act`). "barrier lowering = ratio 변경"은 **여기에만**.
- **★키 검증**: Ch1 Level A = Ch3 Level B의 `ξ_ss→ξ_eq` 극한 일치(수식). detailed balance가 logistic 의존(`eq:ch3_phys_db_width`)임을 명시(erf 시 일반화는 FLAGGED).
- GS gate: Level A↔B 극한 일치 무비약 유도(GS-1); detailed balance 정합(GS-3).

### 합류 Ch4 — 반응속도론 기반 발열 (의도 ⑦)
- KEEP-B: `TṠ_irr=J𝒜≥0`, transition entropy production(+log floor=domain guard), 가역열 두 basis 택일.
- keystone 전파: Level B `r±`로 entropy production ≥0 (Ch3 detailed balance가 ln 부호 보장).
- GS gate: 발열=flux–force/entropy/온도계수 근거(GS-3); 임의 heat term 0(GS-4).

### 합류 Ch5 — 충방전·히스테리시스 (의도 ⑧)
- KEEP-B: signed current, branch index, metastable branch target(≠eq), `h_j`, `ΔV_obs≠ΔV_hys`, `Q̇_hys=J_hys𝒜_hys`, full-cell 분해.
- keystone 전파: branch 비대칭 = Level B의 `β·landscape` 차이 → Ch3 확정에 종속.
- GS gate: hysteresis는 metastable/nucleation/memory 근거 시에만 본문(GS-4); loop area≠true hys.

### 합류 Ch6 — 수치·검증 (의도 ④ solver/검증; 코드 P1 제외)
- KEEP-B: dynamic vs OCV root, index-1 DAE/BDF, g-grid reference, STO-OCV/GITT/C-rate protocol, **보유 데이터**.
- KEEP-A: Refs 6/7 = Fredholm/Padé **검증 가속 후보**(F1–F5), Plan B g-grid = reference(validator).
- **★N-4 통합 검증 backbone**: STO-OCV→평형골격 / GITT→polarization·relaxation signature / 0.1·0.2C→peak 위치·폭 / 0.5·1.0C→tail·broadening·transport stress / 잔차→ρ_G·k_lim·R_n. ★χ-discriminator(전위 의존 Arrhenius slope) + χ vs η_ct 분리(GITT)로 사용자 핵심 주장 falsify 설계.
- GS gate: 축약(Prony/Padé) = reference 대비 오차 검증 후만(GS-4).

---

## §4. G-series Phase (별도 GO 시)
| Phase | 산출 | Gate(요지) | 선행 |
|---|---|---|---|
| G0 | 합류 charter + ξ 기호·명명 매핑표(ver↔Chapter, θ↔ξ) | 매핑 0 누락(P3-7) | D1,D2 |
| G1 | 합류 Ch1 (engine 이식 + Level A 명명 + 피팅식 + 서사 head) | N-1,N-2 충족 + GS-1 무비약 0-FAIL + 피팅식 평가순서 | G0 |
| G2 | 합류 Ch2~Ch4 (발열·반응속도론·entropy heat) | keystone 전파 무충돌(P3-6) + Level A↔B 극한 일치 수식 | G1 검수 |
| G3 | 합류 Ch5~Ch6 (충전·hysteresis·수치검증) | branch=Level B 정합 + N-4 protocol + 보유데이터 매핑 | G2 검수 |
| G4 | xelatex 빌드 + 사용자 PDF 검수 | 0 error + 사용자 승인(Decision Gate) | G3 |

각 G phase = 작업 commit + 10차원×3-Pass 검토 commit 페어; 매 식 GS-1~4 gate; P3 7항목 self-check.

---

## §5. 결정경계 (사용자 확인 — 글로, 무응답 시 권고값)
- **D1**=(B)트렁크+(A)엔진 (권고, RESULT가 정량 지지). **D2**=Ch1 Level A/Ch3 Level B (권고, RESULT §C reconciliation). **D3**=erf/logistic dual-track(logistic baseline) 유지. **D4**=진단까지 완료 → **G-series 진입 여부가 다음 GO**.
- 추가 사용자 입력 유용: (b) Refs 6/7 원문 위치(P3-5 (b)) 위해 `_local_only` 논문 PDF 제공 여부.

## §6. 위험
- R1: G1 피팅식 조립 시 self-consistent(V_n↔ξ) 닫기가 Plan A(Refs6/7)로 안 되면 → Plan B g-grid reference로 fallback(이미 설계). 정지 아님.
- R2: keystone 극한 일치(Ch1 Level A=Ch3 Level B ξ_ss→ξ_eq)가 수식 검증서 깨지면 → D2 재검토(사용자 보고). **유일한 hard 검증점.**
- R3: erf/logistic은 데이터 대기 — dual-track으로 진행, 정지 아님.

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-05-29 | Phase E 산출. (B)트렁크×(A)엔진 합류 spine Ch1~6 + N-1 서사 head + N-2 피팅식 위치 + keystone 전파 + N-4 검증 backbone(보유 데이터). G0~G4 phase. **G-series 본문 재작성 별도 GO 대기.** |
