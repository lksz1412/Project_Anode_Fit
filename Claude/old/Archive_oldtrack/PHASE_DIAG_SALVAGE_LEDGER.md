# PHASE_DIAG SALVAGE LEDGER — KEEP / FIX / RETIRE (앞선 연구 재사용 지도)

**Plan**: `2026-05-29-intent-gap-diagnosis-consolidation-plan.md` §6.4 확정판
**RESULT**: `PHASE_DIAG_INTENT_GAP_RESULT.md`
**원칙**: 앞선 (A)(B) 모든 작업을 버리지 않는다. 각 요소를 정확히 한 분류에 배정(미분류 0). (B)는 *폭·물리규율*, (A)는 *tail 깊이* — **상보적**.
**일자**: 2026-05-29

---

## 1. KEEP — 그대로 합류 trunk·engine 으로 (수정 없이 재사용)

### 1.1 (B) 전하보존 6장 — 합류의 **서사 트렁크** (폭 + 물리 규율)
| 요소 | 출처(B) | 재사용 위치(합류) |
|---|---|---|
| charge-balance implicit V_n + 해존재/단조성 조건 | Ch1 `eq:charge_balance`,`eq:bg_slope_floor` | 합류 Ch1 중심식 |
| 전위 3분 `V_n/V_app/V_drive` + `eq:Vapp_def` | Ch1 | 전 장 공통 표기 |
| 온도 tail **3계층 분해**(평형열역학/동역학지연/전압축분극) | Ch1 §온도 tail | 합류 Ch1 tail 진단 골격 |
| C-rate 정확식 `eq:crate_dxidq_exact` (1/|I| × lag 경쟁) | Ch1/Ch3 | 합류 Ch1 N-3 |
| `dV_app/dT ≠ (∂V_OCV/∂T)_q` 금지 + 평형 온도계수 | Ch2 | 합류 Ch2 |
| forward/backward + detailed balance `ln(r+/r-)=(V_n−U)/w` | Ch3 `eq:ch3_phys_detailed_balance`,`db_width` | 합류 Ch3 (Level B) |
| `ξ_ss=r+/(r++r-) ≠ ξ_eq` 비평형 정상 target | Ch3 `eq:ch3_phys_xiss` | keystone 극한 일치 검증 |
| BV 계층 + `R_ct`, `R_n≠R_ct≠R_n,eff` | Ch3 | 합류 Ch3 |
| 전류 보존 → 강구동 saturation (임의 cap 아님) | Ch3 §전류 보존 | 합류 Ch3 |
| `TṠ_irr=J𝒜≥0`, transition entropy production(+log floor) | Ch4 `eq:ch4_phys_JA`,`transition_entropy_production` | 합류 Ch4 |
| 가역열 OCV/transition **두 basis 택일**(double-count 금지) | Ch4 | 합류 Ch4 |
| signed current·branch index·`q_state`, `ζ_j=1−ξ_j` 종속 | Ch5 | 합류 Ch5 |
| metastable branch target ≠ eq; `h_j` hysteresis state | Ch5 `eq:ch5_branch_target`,`h_dyn` | 합류 Ch5 |
| `ΔV_obs≠ΔV_hys` 분해; `Q̇_hys=J_hys𝒜_hys≥0` | Ch5 | 합류 Ch5 |
| full-cell 분해 + 중복계상 금지 | Ch5 | 합류 Ch5 |
| dynamic root vs OCV root 구분; index-1 DAE/BDF | Ch6 | 합류 Ch6 |
| g-grid reference solver; STO-OCV/GITT/C-rate 검증 protocol | Ch6 | 합류 Ch6 (N-4) |
| ★보유 데이터(반쪽셀 GITT, STO-OCV, 0.1/0.2/0.5/1.0C) | Ch6 §보유 데이터 | N-4 검증 자산 (핵심) |

### 1.2 (A) Kernel-integral — 합류 Ch1의 **tail-shape 엔진** (깊이)
| 요소 | 출처(A) | 재사용 위치(합류) |
|---|---|---|
| ★barrier→length **지수 매핑** `L(G)=(|I|/Q k_0)exp[(G−W_ψ)/RT]` | `eq:L_of_G` | 합류 Ch1 "왜 stretched tail" |
| ★relaxation-length spectrum kernel integral `dΘ_tail/dq=∫A_L(1/L)e^{−(q−q_a)/L}dL` | `eq:kernel_integral` | 합류 Ch1 tail 중심식 |
| ★Refs 6/7 ratio-substitution closure(Plan A) + Plan B numerical + M1-M5/ε governance | `eq:closed`, §closure | 합류 Ch1/Ch6 (self-consistent 닫기, 검증 tier) |
| Marcus bound (선형 lowering 유효범위) | `boundbox` | 합류 Ch1 (GS-4) |
| spectrum의 T/ψ shift `∂lnL/∂V_drive=−χs_φF/RT` | `eq:psi_shift` | 합류 Ch1 tail T/전위 의존 |
| non-uniqueness(Plonka) + forward-only ρ_G | §spectrum `boundbox`,§falsify | 합류 Ch1 falsification |
| χ-vs-η_ct co-linearity 경고 + null-result N1-N4 | §falsify | 합류 Ch1/Ch6 |
| Assumption Ledger grounding tier(AL-1~10 + DOI) | (A) 거버넌스 | 합류 전체 grounding(GS-3) |

### 1.3 결정적 통찰 (문서 외 결과물)
| 요소 | 출처 | 재사용 |
|---|---|---|
| 저온-긴-꼬리 = **kinetic 신호**(평형폭 w=RT/F는 저온서 좁아짐) T-방향 논증 | `SELF_REVIEW §3` | 합류 Ch1 **N-1 서사 head** |
| (A)·(B) 코어 SAME 8 / RECONCILABLE 3 / CONTRADICTORY 1 대조 | `CROSSCHECK` | 합류 정합 근거 |

---

## 2. FIX — 재사용 전 수정 필요 (수정 후 KEEP)

| # | 항목 | 현 문제 | 수정 방향 | 연결 |
|---|---|---|---|---|
| F-1 | ★keystone χ𝒜 명명 | Ch1 "배리어 낮춤"(Level B 언어) ↔ Ch3 Level A mobility 사용 | Ch1=mobility 가속(Level A) 재명명 / Ch3=forward·backward(Level B); 전파 trace | RESULT §C, D2 |
| F-2 | ★N-1 서사 | 장별 hygiene manual, 추진 서사 부재 | 합류 head + 각 장 서두 "관찰→이 장" 1문단 (Observation Anchor) | N-1 |
| F-3 | ★N-2 피팅식 | 단일 닫힌식 미조립 | 합류 Ch1 말미에 `(dQ/dV)(V_n,T,|I|; ξ_eq,ΔG_a,χ,ρ_G,R_n)` 평가순서와 함께 박기 | N-2 |
| F-4 | flux→rate clamp | (B) `eq:current_rate_limit_ch1` 평형근처 발산·부호 | 발산·부호 없는 clamp `dξ/dt=sign(ξ_eq−ξ)min(k|ξ_eq−ξ|, I_max/Q_tot)` | 리뷰 #2 |
| F-5 | 기호 θ↔ξ | (A) θ, (B) ξ | 트렁크 (B) `ξ` 통일 + (A) `θ` 매핑표(P3-7) | DQ-DIAG-3 |
| F-6 | 자체 검수표 | keystone Level A/B 확정 항목 부재 | Ch1·Ch3 검수표에 "χ𝒜 Level 확정" 행 추가 | 리뷰 #3 |

---

## 3. RETIRE / 강등 — 합류 시 제거 또는 각주화

| 항목 | 사유 | 처리 |
|---|---|---|
| "열역학 only" 프레이밍 | 관찰 주역은 동역학(RESULT §0-2, SELF_REVIEW §3) | "열역학 무대 + 동역학 주역"으로 교체 |
| closed-form "primary deliverable" 위상 | ansatz 근사(검증 tier) | Plan A=검증 tier로 강등(이미 v5 반영) 유지 |
| 관찰로 ≤3단계 환원 안 되는 형식 절 | Observation Anchor Test 실패 | 각주/appendix 이동 또는 삭제 |
| 피팅 편의 cap/softplus/clip 옹호 표현 | GS-4 위반 | 이미 양 계열이 "실무 팁"으로 격하 — 유지 |
| erf primary 강제 | graphite 열역학 유도 부재(FLAGGED) | logistic baseline + erf FLAGGED 옵션 (DQ-v3-1, 데이터 대기) |

---

## 4. 분류 완결성 체크 (gate: 미분류 0)
- (B) 6장 핵심식 그룹 17개 → KEEP 17 (일부 FIX 중첩: F-1 Ch1/Ch3, F-4 Ch1, F-6 Ch1/Ch3).
- (A) 핵심식 그룹 8개 → KEEP 8 (F-5 기호 통일 대상).
- 통찰 2개 → KEEP.
- 프레이밍/위상 5개 → RETIRE/강등.
→ **미분류 0. 모든 앞선 작업이 합류 trunk(B) 또는 engine(A) 또는 grounding 으로 재배치된다.** 폐기되는 *물리*는 없다 (폐기 대상은 프레이밍·과대위상·미환원 형식뿐).
