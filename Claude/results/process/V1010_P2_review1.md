# P2 Step2 — 검토1 (별도 세션 Opus, 적대적 교차검증) 결과

> 9 supplement(S1-3·O1-3·C1-3) vs Ch1.tex(1867줄)+P1 result+broadening_w_design+ORIGIN_VERDICT. 핵심 수치 직접 재산출 검증.

## A. 확정 사실 (9 드래프트 옳게 합의)
- A1. coverage: N0→N9+equilibrium = **12 closed-form 식 Ch1 박스식 1:1, 누락 0**(P1 §2-A 정합).
- A2. 다리 유도 무결(직접 재산출): RT/F=25.69mV · ΔU_hys(12000,298)=86.69mV · Sommerfeld ∫z²eᶻ/(1+eᶻ)²=π²/3=3.2899 · **O2 직접-엔트로피 ∫s(ζ)dζ=π²/3(9개 중 유일·정확)** · S_e/k_B(full)=1.106.
- A3. LCO 전자엔트로피 부호사슬: 삽입 x↑→metal→insulator→∂g/∂x<0→ΔS_e<0, 흑연 2→1 −16 슬롯 부호 일관 — 물리 무결.
- A4. broadening: apparent-U=U_j+η(분포=η 과전압·forward-only·사이즈 0) tex·ORIGIN 정합.
- A5. **T² 누적계수 ½**(O3·C1·C2·C3 3중 독립): U₁(T)=U₁(T₀)+(ΔS₀/F)(T−T₀)+(a_e/2F)(T²−T₀²). tex는 "∝T²"만 → ½ 명시 정당 보강.

## B. 정정 필요
- **B1 ★CRITICAL(물리 오류)**: S3 §3-2-4 `func_dS_e_mol` eV→J 변환 `dg_dx*eV_to_J` **틀림** — g[states/eV]→states/J는 **`/e_V`(나눗셈)**. 곱하면 차원 깨짐·~10¹⁵배 과소(전자항 침묵 무력화). → **C3 §4.2 `g_J=g_eV/e_V` 형으로 교체**, S3는 ΔS_e 닫힌식(서술)만 채택.
- **B2**: S2 LCO 절을 "★누락(코드 미구현)"으로 오분류 — 실제는 **과잉**(문건엔 있고 코드엔 없음). O1 "과잉-A(plug-in 예고 정당)" 채택.
- **B3**: S1 §2.5 GAP-E 면적보존 식 자기모순(0=0으로 꼬임) → S3 §2-3·C1 Bridge B·C2·C3(치환적분 ∫Q_j ξ(1−ξ)/w dV=Q_j+DC gain=1) 대체.
- **B4(문건측)**: tab:nodemap N1 줄근거 L412→**L408**(P1 V_n 확정). C1/C2/C3/O3 적발 — 본문 줄근거 보정(식 무관).

## C. 체리픽 가이드
| 섹션 | 최강 | 취할 요소 |
|---|---|---|
| coverage | **O1** | 5등급(충족/과잉-A/과잉-B/누락/부분), 死코드·docstring=올바른 비대응, 누락3=거동 설명 결손(식 아님). O2·O3 병용 |
| 다리 유도 | **S3+O3** | S3 4단 다리(2-1~2-4) + O3 grand-canonical Δμ=−sF(V−U) 부호·Sommerfeld U_e→C_e→S_e(3.1-3.5) |
| LCO 전자엔트로피 | **O2+O3** | O2 직접-엔트로피 경로(∫s=π²/3) + O3 Mott항/축퇴극한 경계(천이중심 Sommerfeld 최약) + O1 혼합차원 Rk_B 해설 |
| 단위 다리 | **C3+C2** | `g_J=g_eV/e_V`(정답 방향, S3 교체용) |
| fitting 실용 | **C1+C2** | Bridge A~G + decision-tree. C1 T² ½ 경고 |
→ 골격 O1 coverage→다리 S3/O3→LCO O2/O3/C3→실용 C1/C2. **S2 오분류·S3 코드 단위오류·S1 GAP-E 배제.**

## D. 보완 필요 (9 드래프트 전부 놓침)
- **D1 ★**: sec:dist ⟨n⟩=θ(자리 점유) vs ξ_eq=1−θ(진행률) 라벨 갭(L876~880) — σ_d가 부호 흡수하나 **θ↔ξ 화해 한 줄 없음**(타 전공 G-follow 함정). O3만 근접. → "⟨n⟩=θ_eq, ξ_eq=1−θ_eq logistic 동형(σ_d 부호 흡수)" 보강.
- **D2**: LCO T1 x↔V(SOC) 매핑 미설계(C1만 지적) — ΔS_e(x,T)는 조성 x 함수인데 dqdv는 V 격자 → x↔ξ_eq(V) 매핑 P4 설계 공백.
- **D3**: config 중심 표준값 ΔS_j⁰ 수치 출처(Motohashi 0.47/1.49)가 중심값인지 부분몰값인지 round-trip 미실증 → P4 피팅 가드.

## E. 가장 약한 1곳
S3 §3-2-4 코드 스니펫 eV→J(`*eV_to_J`) — 9개 중 유일 실행가능 물리 오류(P4 복사 시 전자항 10¹⁵배 과소 침묵). 곱→나눗셈 한 글자. **반드시 C3형 교체.**
