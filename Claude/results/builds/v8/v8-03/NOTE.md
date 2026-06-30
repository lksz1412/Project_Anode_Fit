# v8-03 NOTE

## Read Coverage

| 파일 | 읽은 행 범위 |
|------|-------------|
| `v7-11.tex` (890행) | 전문 정독 (1–890) |
| `AUTHOR_BRIEF_v8.md` (64행) | 전문 정독 (1–64) |
| `v11_flowchart.md` (90행) | 전문 정독 (1–90) |
| `graphite_ica_ch1_Opus_v5.tex` (1883행) | 380–500, 530–640 (핵심 유도 절) |

## 유도 사슬 복원 목록 (11식)

| 식 | 복원된 유도 단계 |
|----|----------------|
| **U_j(T)** | G≡H−TS → μ≡∂G/∂n → 삽입반응 전기화학 평형 → 상수 묶음 sFU^0 → ΔG=ΔH−TΔS 대입 → U=(-ΔH+TΔS)/F |
| **w_j=n_jRT/F** | 격자기체 g-bar → ∂/∂θ 미분 → logit 기울기 → 이상 극한 중심기울기 비교 → w=RT/F → 다중도 n_j |
| **w^eff** | 식 isotherm의 중심기울기 4RT−2Ω → 동치로 유효 폭 w^eff=RT/F·(1−Ω/2RT) |
| **ξ_eq logistic** | W=N!/n!(N-n)! → Stirling → S_mix → g-bar → ∂μ/∂θ → μ(θ)=[식 mu] → 운동방정식 dξ/dt=r+(1-ξ)-r-ξ → 정지점 → detailed balance r+/r-=e^{A/RT} → logit 풀이 → logistic |
| **평형 peak** | 전하보존 Q·q=Q_bg+ΣQ_jξ_j → q 미분 → dξ_eq/dz=ξ(1-ξ) 항등식 → 연쇄율 dz/dV=σ_d/w → Q_j·ξ(1-ξ)/w |
| **ΔU_hys** | g(ξ)=... → g''=RT/[ξ(1-ξ)]−2Ω → g''=0 → 근의공식 → ξ_s±=½(1±u) → V_eq(ξ_s±) 대입(logit역수·(1-2ξ)=∓u) → 전위차 계산 → artanh 정리 → (2/F)[Ωu−2RT·artanh u] |
| **U_j^d** | spinodal 두 끝점 평균=U_j(대칭 증명) → 방향별 한 자유도 → U_j+½σ_d·h_η·γ·ΔU_hys |
| **L_q ODE** | dξ/dt=k_j(ξ_eq−ξ) → 정전류 변환 dq/dt=|I|/Q_cell → r=ξ_eq−ξ → dr/dq=dξ_eq/dq−r/L_q |
| **적분인자 일반해** | 적분인자 e^{q/L_q} → d[e^{q/L_q}r]/dq=... → 적분 → 지수 커널 합성곱 r(q)=... |
| **k_j (Eyring+DB)** | Eyring k+=k_BT/h·e^{-(ΔG_a^eff−χ_dA)/RT} → detailed balance k-=k+e^{-A/RT} → k_j=k+(1+e^{-A/RT}) |
| **L_V** | L_q 표현 대입·분해 → 로그4항(T*/T·분모·ΔG_a^eff/RT·−χ_dA/RT) → L_V=|dV/dq|_{qa}·L_q |

## 10-라운드 자체 검수 결과

| R# | 청크 스킴 | 렌즈 | 결함 수 | 내용 |
|----|----------|------|---------|------|
| R1 | 통독 | G-derive (유도 완결성) | 1 | `\sstat` 미정의 → `\newcommand{\sstat}{\mathrm{ss}}` 추가 |
| R2 | 절별 | 부호 8항 | 0 | 전건 pass |
| R3 | 식 번호별 | G-follow (따라가짐) | 0 | 유도 흐름 연속 확인 |
| R4 | 유도 단계별 | G-usable (사용성) | 0 | 학부 수준 손계산 가능 확인 |
| R5 | 라인별 | 코드 식별자 1:1 | 0 | func_U_j/func_ksi_eq/func_L_q 등 전건 |
| R6 | 그림별 | orphan 0 | 0 | 모든 그림 앞 식 동기·본문 \ref 확인 |
| R7 | 표별 | 기본값 정합 | 0 | tab:staging/tab:inputs v7-11 보존 확인 |
| R8 | 부호 사슬 | S1-S8 전건 | 0 | 8/8 통과 |
| R9 | 수치 | R1-R4 self-test | 0 | 수치 계산 일치 |
| R10 | 빌드 | xelatex 2-pass 0-err | 0 | 18p PDF, LaTeX error 0 |

수렴: R5부터 연속 0결함 (조건 충족).

## 부호 8항 결과

| 항 | 결과 |
|----|------|
| S1: U_j(T)=(-ΔH+TΔS)/F | PASS |
| S2: ξ_eq=logistic[σ_d(V-U)/w] 방전 V↑→ξ↑ | PASS |
| S3: dξ/dV peak 양수·방향불변 | PASS |
| S4: ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d | PASS |
| S5: χ_d 방전χ/충전1-χ, ΔH_a^eff=ΔH_a-χ_dΩ | PASS |
| S6: ∂lnL_q/∂V<0 동기(운영 미분=0) | PASS |
| S7: 충전 격자역전, 충전 dQ/dV 양수 | PASS |
| S8: 분극 V_n=V_app-σ_d|I|R_n 방전 측정>내부 | PASS |

## 그림 목록

| 그림 | 유래 | 내용 |
|------|------|------|
| fig:spine | v7-11 유래 (보존) | 코드 진행 spine N0→N9 |
| fig:staging | v7-11 유래 (보존) | 흑연 staging 갤러리 채움 |
| fig:gxi | **완전 신규** | g(ξ) 이중웰: Ω=0 vs Ω=4RT, spinodal ξ_s± |
| fig:hysloop | v7-11 유래 (보존) | 비단조 V_eq(ξ) 과주행, ΔU_hys |
| fig:logistic | v7-11 유래 (보존) | logistic 곡선 + 종 미분 |
| fig:fluxcross | **완전 신규** | 정지점 유도: 정방향/역방향 플럭스 교점 |
| fig:memorykernel | **완전 신규** | 지수 기억 커널 e^{-(q-q')/L_q} |
| fig:reversal | v7-11 유래 (개선 캡션) | 인과 꼬리 방향: 방전 vs 충전 |

## 빌드 결과

- xelatex 3-pass (참조 안정화)
- LaTeX `!` error 수: **0**
- 출력: `v8-03.pdf` (18 pages)
- MiKTeX update nag (exit code 1): 실제 LaTeX 오류 아님, PDF 정상 생성
