# PHASE_DIAG RESULT — 사용자 의도 ↔ 기존 산출물 간극 진단

**Plan**: `Claude/plans/2026-05-29-intent-gap-diagnosis-consolidation-plan.md` (§00 GS-1~4 적용)
**대상**: (A) `Claude/docs/graphite_ica_chapter1.tex` (kernel-integral, Ch1 단독) · (B) 업로드 `graphite_ica_ch1_ch6_physical_v3_rechecked.tex` (전하보존 6장)
**Phase**: A(완독)·B(traceability)·C(keystone) 결과. D(salvage)=별도 ledger, E(roadmap)=별도 plan.
**일자**: 2026-05-29

---

## §0. ★ 완독 후 핵심 재평가 (예비진단 정정 — 정직성)

계획서 §6.5 는 (B) Ch3~6 미완독 상태의 **예비** 판정이었다. **이번에 (B) 전문(2911줄)을 완독**한 결과, 예비진단을 다음과 같이 정정한다 (GS-5 정직성).

1. **정정 — (B)는 의도 8고리를 구조적으로 "전부" 커버한다.** Ch1(열역학 charge-balance+유효배리어+tail 분해), Ch2(발열 연결), Ch3(forward/backward·BV·detailed balance), Ch4(entropy production 발열), Ch5(signed current·metastable branch·hysteresis), Ch6(DAE 수치해·STO-OCV/GITT/C-rate 검증). 예비진단의 "(A)✗/(B)잠정◑"은 **(B) 거의 전부 ◑~✅**로 상향.

2. **그렇다면 "AI마다 거리 있다"의 진짜 원인은?** (B)가 틀려서가 아니다. 완독 결과 원인은 **세 가지로 좁혀진다**:
   - **(원인-1) N-1 서사 부재**: (B)는 장마다 "이전 장 고정 기준 → 경계(하지 말 것) → 자체 검수표 → 결론"의 **물리 위생 매뉴얼(hygiene manual)** 형식이다. R_n≠R_ct≠R_n,eff, ΔV_obs≠ΔV_hys, double-counting 금지, cap 금지 등 **"무엇을 혼동하면 안 되는가"의 disclaimers 적층**이 매우 훌륭하나, **"저온 긴 꼬리 관찰 → 유효배리어 → 그래서 이 식"의 추진 서사(positive story)가 흐리다.** (Observation Anchor Test 적용 시 다수 절이 관찰로 ≤3단계 환원되지 않음.)
   - **(원인-2) N-2 피팅식 미조립**: 사용자 핵심 요구("피팅에 쓸 수 있는 논리식")가 **단일 닫힌 형태로 조립된 적이 없다.** Ch1은 chain-rule 조각, Ch6은 수치 recipe 로 흩어져 있고 "이 식에 T,|I| 넣으면 꼬리"가 본문 결과로 박혀 있지 않다.
   - **(원인-3) keystone 명명 모순(live)**: §C 참조. Ch1은 χ𝒜를 "배리어 낮춤"으로(`:289`), Ch3 Level A는 같은 항을 "ratio 안 바꾸는 relaxation mobility 증가"로(`:1298-1302`) 쓴다 — 용어-역할 불일치 잔존.

3. **(A)의 고유 가치 = tail 메커니즘의 깊이.** (B)는 tail을 "kinetic lag + ρ(g) 분포 수치적분(Ch6 g-grid)"으로 두지만 **왜 stretched 인지**는 설명 안 한다. (A)는 barrier→length **지수 매핑**(`L=(|I|/Q k_0)exp[(G−W_ψ)/RT]`)으로 작은 barrier 분산이 length 에서 지수 확대되어 stretched tail 이 됨을 보이고, Refs 6/7 로 self-consistent integral 을 닫는다. → **이것이 (B)에 없는, 합류로 이식해야 할 깊이.**

**한 줄**: (B)는 *폭과 물리 규율*은 충분하나 *추진 서사·피팅식 결과물·tail 깊이*가 없고, (A)는 *tail 깊이*는 있으나 *Ch1 단독*이다. "거리"는 **(B)의 결함이 아니라 (A)·(B) 미합류 + 서사/결과물 부재**다.

---

## §A. Phase A — 장별 핵심식·역할 추출 (완독 근거; gate: 6장 누락 0)

### (B) 전하보존 6장 계열

**Ch1 — 방전기준 전하보존 상변이 동역학** (역할: 의도 ④의 열역학 무대 + 유효배리어 + tail 분해)
| 핵심식 | label | 의미 |
|---|---|---|
| `Q_cell q = Q_bg(V_n,T)+Σ Q_{j,tot}ξ_j` | `eq:charge_balance` | ★중심식 — V_n을 implicit 결정 |
| `ξ_eq=1/(1+exp[−(V_n−U_j)/w_j])` | `eq:xi_eq_logistic` | 평형 진행률(logistic) |
| `ΔG_eff,j=ΔG_a,j−χ_j𝒜_j` | `eq:Geff` | ★유효배리어; χ_j="배리어 낮춤 민감도"(`:289`) |
| `k_act=ν exp(−ΔG_eff/RT)`, `1/k_phys=1/k_act+1/k_lim` | `eq:k_act_physical`,`eq:k_phys_limited` | 속도상수 + 물리적 병목 직렬 |
| `dξ_j/dt=k_j(ξ_eq−ξ_j)`, `dξ_j/dq=(Q_cell/|I|)k_j(ξ_eq−ξ_j)` | `eq:dxidt`,`eq:dxidq` | 완화 동역학(시간/q좌표) |
| `dV_n/dq=[Q_cell−Σ Q_{j,tot}dξ_j/dq]/(∂Q_bg/∂V_n)`, ICA/DVA | `eq:dVdq_iso`,`eq:ica_final` | 관측식 |
| 온도 tail = 평형열역학·동역학지연·전압축분극 **3계층 분해** | §온도 의존 tail | tail 귀속 규율 |
→ 전달(Ch2): `dξ_j/dt`. **role 1문장**: 전하보존으로 V_n을 풀고 유효배리어 완화로 tail을 만든다.

**Ch2 — 발열 확장성 검토** (역할: 의도 ⑤)
| 핵심식 | label | 의미 |
|---|---|---|
| `dV_app/dT ≠ (∂V_OCV/∂T)_q` | `eq:ch2_forbid_app_dvdt_identity` | ★apparent 온도미분 가역열 금지 |
| 평형 온도계수 `(∂V_OCV/∂T)_q` (charge-balance 미분) | §평형 온도 계수 | reversible heat 기초 |
| heat 분해 후보(가역/비가역/relaxation) | §열원 분해 | Ch4로 위임 |
→ role: Ch1 상태변수로 가역/비가역열의 **차원·연결만** 정리, 확정은 Ch3-4로.

**Ch3 — 전기화학 반응속도론** (역할: 의도 ⑥ — ★keystone 장)
| 핵심식 | label | 의미 |
|---|---|---|
| `dξ_j/dt=r_j^+(1−ξ_j)−r_j^-ξ_j` | `eq:ch3_phys_forward_backward` | 일반 forward/backward |
| `r_j^+/r_j^-=ξ_eq/(1−ξ_eq)`, `ln(r+/r-)=(V_n−U_j)/w_j` | `eq:ch3_phys_detailed_balance`,`eq:ch3_phys_db_width` | ★detailed balance(logistic 의존) |
| split `r_j^+=k_phys ξ_eq, r_j^-=k_phys(1−ξ_eq)` | `eq:ch3_phys_consistent_split` | Ch1 완화 = forward/backward 축약 |
| `r_j^+∝exp[−(ΔG^{+‡}−β_j𝒜_j)/RT]`, `r_j^-∝exp[−(ΔG^{-‡}+(1−β_j)𝒜_j)/RT]` | `eq:ch3_phys_rplus_act`,`rminus_act` | ★Level B 비대칭 활성화 |
| `ξ_ss=r_j^+/(r_j^++r_j^-)` (≠ ξ_eq) | `eq:ch3_phys_xiss` | 비평형 정상 target |
| BV `j_n`, `R_ct=RT/(F A_eff j_0)` | `eq:ch3_phys_bv`,`rct` | 계면 kinetics 계층 |
| **Level A/B 명시 구분** + mdframed | `:1298–1302` | ★keystone 정의 위치 |
→ role: Ch1 완화 ODE가 forward/backward 축약형임을 보이고 Level A(mobility)/Level B(barrier) 분리. **여기서 χ𝒜 역할이 Ch1과 어긋남(§C).**

**Ch4 — 반응속도론 기반 발열** (역할: 의도 ⑦)
| 핵심식 | label | 의미 |
|---|---|---|
| `TṠ_irr=Σ J_α X_α≥0`, `TṠ_irr,n=J_n𝒜_n≥0` | `eq:ch4_phys_flux_force_general`,`JA` | ★비가역열 = flux·force |
| `Q̇_irr,j^tr=(Q_{j,tot}/F)RT(𝒥^+−𝒥^-)ln(𝒥^+/𝒥^-)≥0` | `eq:ch4_phys_transition_entropy_production` | transition entropy production(+log floor) |
| `Q̇_rev^OCV ∝ |I|T(∂V_OCV/∂T)_q`; `≁ IT dV_app/dT` | `eq:ch4_phys_rev_ocv`,`forbid_app_dvdt` | 가역열 OCV basis |
| `Q̇_rev,ξ=Σ s T ΔS_j (Q_{j,tot}/F)dξ_j/dt` | `eq:ch4_phys_rev_xi` | 가역열 transition basis (A/B 택일, double-count 금지) |
→ role: Ch3 flux–force로 발열을 grounding; 두 가역열 basis 택일.

**Ch5 — 충방전·히스테리시스** (역할: 의도 ⑧)
| 핵심식 | label | 의미 |
|---|---|---|
| signed current `I_s`, branch index `b`, `dq_state/dt=I_s/Q_cell` | `eq:ch5_signed_current`,`qstate_dt` | 충/방전 통합 좌표 |
| `ζ_j=1−ξ_j` (종속), ξ_j state 유지 | `eq:ch5_zeta_def` | 독립 state 안 늘림 |
| `ξ_tar^b=1/(1+exp[−(V_n−U_j^b)/w_j^b])` (metastable≠eq) | `eq:ch5_branch_target` | branch target |
| `h_j∈[−1,1]`, `dh_j/dt=λ^b(h_tar−h_j)` | `eq:ch5_h_dyn` | hysteresis state |
| `ΔV_obs=ΔV_hys+ΔV_pol+ΔV_kin+ΔV_transport+ΔV_aging`, `ΔV_obs≠ΔV_hys` | `eq:ch5_voltage_gap_decomp`,`obs_not_hys` | ★voltage gap 분해 |
| `Q̇_hys=J_hys 𝒜_hys≥0` (loop area 전체 아님) | `eq:ch5_hys_flux_force` | hysteresis heat |
→ role: Ch3 구조 위에 signed/branch/hysteresis; "관측 gap≠hysteresis" 규율.

**Ch6 — 수치해·검증** (역할: 의도 ④의 solver/검증; P1으로 코드는 제외)
| 핵심식 | label | 의미 |
|---|---|---|
| dynamic root `F_cb^dyn(V_n;q,ξ)=0` vs OCV root `F_cb^OCV(V_n;q)=0` (미분 다름) | `eq:ch6_dynamic_root`,`ocv_root` | ★두 root 구분 |
| index-1 DAE / root-constrained ODE (BDF/Radau) | `eq:ch6_ode_phys`,`alg_phys` | 시간적분 |
| g-grid reference `ξ_j=Σ w_m ρ(g_m)ξ_j(g_m)` | `eq:ch6_grid_average` | ★기준 solver |
| Prony `K_j(t)≈Σ a_ℓ e^{−t/τ_ℓ}` (준정상); Fredholm/PAdé = 검증 가속 후보(F1–F5) | `eq:ch6_prony_kernel` | 축약(검증 종속) |
| 보유 데이터: 반쪽셀 GITT, STO-OCV, 0.1/0.2/0.5/1.0C | §보유 데이터 | ★N-4 검증 자산 |
→ role: 음극 방전·등온 1차 검증 pipeline. **사용자 실제 데이터 명시.**

### (A) Kernel-integral 계열 (Ch1 단독) — 요약 (이미 완독, 본 세션 1차)
| 핵심식 | label | 의미 |
|---|---|---|
| `Q_cell q=Q_bg+Q_p Θ` → implicit V_n | `eq:charge_balance` | (B)와 동일 골격 |
| `ΔG_eff=ΔG_a−χ𝒜=G−W_ψ`, Marcus-bounded | `eq:Geff` | (B)와 동일 + Marcus bound |
| `k=k_0 exp[−(G−W_ψ)/RT]`, 단일 모드 kernel `L=|I|/(Q_cell k)` | `eq:rate`,`single_kernel` | (B)와 동일 |
| ★`L(G)=(|I|/Q k_0)exp[(G−W_ψ)/RT]` barrier→length **지수 매핑** | `eq:L_of_G` | ★(B)에 없는 깊이 |
| ★`dΘ_tail/dq=∫A_L(L)(1/L)e^{−(q−q_a)/L}dL` kernel integral | `eq:kernel_integral` | ★stretched tail 중심식 |
| ★Refs 6/7 ratio-substitution closure `Θ_A` (Plan A) + Plan B numerical + M1-M5/ε | `eq:closed` | ★self-consistent 닫기 |
| `∂lnL/∂V_drive=−χ s_φ F/RT` spectrum shift | `eq:psi_shift` | tail 의 T/ψ 의존 |
| χ-vs-η_ct co-linearity 경고 + null-result N1-N4 | §falsify | falsification 깊이 |
→ role: tail을 relaxation-length spectrum kernel integral로 설명(왜 stretched인가) + Refs 6/7 closure.

---

## §B. Phase B — Intent↔Artifact Traceability (완독 근거, de-hedged)

판정: ✅구현 / ◑부분(서사·결과물 약) / ⚠표류 / ✗누락 / ✖모순

| # | 의도 고리 (§0.2) | (A) | (B) | 판정 | 근거(파일·식) |
|---|---|---|---|---|---|
| 1 | 저온 긴 꼬리/고온 짧음 = 관찰 | ◑(O2) | ✅ Ch1 §온도 tail 3계층 | **◑** | (B) §온도 분해; 단 N-1 서사로는 미연결 |
| 2 | OCV 평형 ≠ 전류 시 전위 | ✅`eq:psi_shift` | ✅ `V_n/V_app/V_drive`,`eq:Vapp_def` | ✅ | 양 계열 전위 3분 명확(P3-1) |
| 3 | C-rate 무조건 적용 | ◑(`L∝|I|`) | ✅ Ch1 §C-rate `eq:crate_dxidq_exact`, Ch3 재분해 | ✅ | (B) 우세 |
| 4 | Ch1: 열역학→유효배리어→**피팅식** | ◑(closure, 식 P1밖) | ◑(조각·수치, 단일식 미조립) | **◑→원인-2** | N-2 미충족 (양쪽) |
| 5 | Ch2: 발열 단초 | ✗ | ✅ Ch2(+Ch4) | ✅(B) | (A) Ch1 단독 |
| 6 | Ch3: 반응속도론 확장 | ✗ | ✅ Ch3 forward/backward·BV | ✅(B) | ★keystone 모순 지점(§C) |
| 7 | Ch4: 발열(반응속도론 기반) | ✗ | ✅ Ch4 entropy production | ✅(B) | flux–force grounding |
| 8 | Ch5(~6): 충전확장→히스테리시스 | ✗ | ✅ Ch5(+Ch6 수치) | ✅(B) | metastable branch 규율 |

**Traceability 결론**: 폭(고리 5~8)은 **(B)가 전적으로 커버**(예비진단의 "잠정"을 ✅로 확정). 결핍은 **세로축**에 있다 — 고리 1·4가 ◑인 이유가 N-1(서사)·N-2(피팅식)이며, 이는 (B)의 *형식*(hygiene manual) 문제이지 *내용* 부재가 아니다. (A)는 고리 1·4의 **깊이**(tail why-stretched, kernel closure)를 보유.

---

## §C. Phase C — Keystone χ𝒜 (Level A vs B) 정밀 진단 (완독 줄근거 확정)

**확정 사실** (GS-1 학부 무비약 chain은 plan §6.3 참조):
- **(B) Ch1 `:289`**: "χ_j≥0는 … 𝒜_j가 **활성화 장벽을 낮추는** 민감도" → **Level B(방향성 barrier lowering) 언어**.
- **(B) Ch3 `:1298–1302`** mdframed + 본문: "k_phys는 … relaxation **mobility**로 해석. 𝒜_j에 의한 barrier lowering은 forward/backward ratio를 직접 바꾸는 항이 아니라, 평형 target으로 향하는 relaxation **mobility를 증가**시키는 항으로 작동" → **Level A(방향성 없음)**.
- **모순**: 동일 항 `χ_j𝒜_j`를 Ch1은 Level B 언어("배리어 낮춤")로, Ch3 Level A는 mobility scale로 사용. (A)도 동형(`D3` BEP grounding ↔ `D5`+`eq:rate` 총 mobility 사용).

**진단 (4-분류)**: **물리 가정 충돌** (plan §6.6). loop의 5 edge 중 유일 실제 충돌.

**해소 = reconciliation (발명 아님)**: (B) Ch3가 이미 Level A/B를 정의·`ξ_ss`(`eq:ch3_phys_xiss`)까지 분리해 둠. 따라서:
1. **Ch1**: χ𝒜를 **mobility 가속(Level A)**으로 재명명 ("효과적 배리어 낮춤" → "전위 의존 relaxation mobility 가속"); ratio는 thermodynamic ξ_eq 전담.
2. **Ch3**: forward/backward 비대칭(`eq:ch3_phys_rplus_act/rminus_act`)에서 χ=β transfer coefficient로 **Level B** 도입; `r_+/r_-=exp(𝒜/RT)` 와 detailed balance 정합.
3. **전파(§6.8 trace)**: Ch2(가역열=thermo, 비가역=flux), Ch4(Level B flux–force), Ch5(branch=Level B β·landscape 차이), Ch6(Level A↔B 수치 limiting-case 일치)로 일관.
**유일 검증점**: Ch1 Level A = Ch3 Level B의 `ξ_ss→ξ_eq` 극한 일치 (G-series에서 수식 확인).

---

## §D. Salvage 요약 (상세: `PHASE_DIAG_SALVAGE_LEDGER.md`)
- **KEEP**: (B) 6장 전 골격(charge-balance·forward/backward·detailed balance·entropy production·signed branch·DAE/검증) + (A) tail 깊이(kernel integral·barrier→length 지수매핑·Refs 6/7 closure·Marcus·χ-discriminator) + T-방향 kinetic 논증.
- **FIX**: keystone 명명(§C); N-1 서사 head; N-2 피팅식 조립; flux→rate clamp(리뷰 #2).
- **RETIRE/강등**: "열역학 only" 프레이밍; closed-form primary 과대위상; 관찰 미연결 형식 절.

---

## §E. North Star(N-1~N-5) 현 충족 상태 (G-series 목표 대비)
| | 조건 | (A) | (B) | 합류 목표 |
|---|---|---|---|---|
| N-1 | 단일 서사(관찰→…→히스테리시스) | △(Ch1 abstract) | ✗(hygiene 적층) | **신설 head + 장별 1문단 anchor** |
| N-2 | 피팅식 본문 결과 | ◑(closure 식, P1밖) | ✗(조각·수치) | **Ch1 말미 단일 닫힌식 박기** |
| N-3 | 전위·전류 내장(C-rate 겹침) | ✅ | ✅ | 유지 |
| N-4 | 검증 가능(falsify+데이터) | ✅(χ-discriminator) | ✅(STO-OCV/GITT/C-rate) | **두 계열 통합 protocol** |
| N-5 | grounding·정직성 | ✅(AL tier) | ✅(검수표·경계) | 유지 + keystone 미결→해소 기록 |

**진단 총평**: 합류의 핵심 작업은 **새 물리 발명이 아니라 (B) 폭 × (A) 깊이의 결합 + N-1(서사)·N-2(피팅식)·keystone(명명) 보강** 세 가지다. 이 셋이 "AI마다 거리 있다"의 실제 내용이다.
