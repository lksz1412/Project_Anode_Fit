# v8-02 NOTE — 흑연 음극 dQ/dV Chapter 1 (유도 확장판)

## 1. Read Coverage

| 파일 | 상태 | 범위 |
|------|------|------|
| `v8-00_spine/AUTHOR_BRIEF_v8.md` (64줄) | 전문 정독 | 전 절(§1-§9) — 사양·11식·부호·그림·빌드 지시 |
| `v7-11/v7-11.tex` (890줄) | 전문 정독 | 배치 보존 대상: preamble·명령·절 구조·박스·5 TikZ·4 표·참고문헌 |
| `docs/graphite_ica_ch1_Opus_v5.tex` (1883줄) | 부분 정독 | Lines 1–1199 — 유도 원천: 속도론·열역학·logistic·spinodal·ODE·인과꼬리 전 섹션 |
| `v7-00_spine/v11_flowchart.md` (90줄) | 전문 정독 | N0→N9 spine·부호 규약·노드↔식↔코드 매핑 |
| `v7-00_spine/Anode_Fit_v11_final.py` (706줄) | 부분 정독 | Lines 1–120 — 상수·핵심 함수 시그너처(func_w, func_U_j, func_ksi_eq, func_L_q, _causal_lowpass) |

---

## 2. 10-라운드 검수 이력 (G-derive 1급 포함)

| R | 청크 스킴 | 렌즈 | 발견 결함 → 조치 |
|---|-----------|------|------------------|
| 1 | 절별(서론·N0·N1) | 구조·논리 | preamble: setspace 누락 → 추가; 부호 규약 단락 위치 재정렬 |
| 2 | 절별(N2·N3) | G-derive(유도 한줄 점프) | Gibbs 정의→μ→전기화학 평형 3단계 추가; spinodal 근의공식 중간 2줄 복원 |
| 3 | 절별(N4·N5) | G-derive | logistic 유도: r⁺/r⁻=e^{A/RT} 단계·ξ 풀기 단계 보완 |
| 4 | 절별(N6) | G-usable(코드 1:1) | peak 모양 부호 방향 불변 명시 추가 |
| 5 | 식 단위(eq:dUhys 전) | G-derive | ΔU_hys artanh 항등식 전개 과정 1단계 명시; V_eq(ξ) 전시 |
| 6 | 절별(N7) | G-derive | L_q ODE 적분인자 도출·T* 정의·로그4항 분해 복원 |
| 7 | 절별(N8) | 인과 방향·부호 | 충전 격자역전 문구 명확화; peak_shape ≥ 0 증명 추가 |
| 8 | 표·박스(3종) | G-usable(code 1:1) | tab:staging 4건 초기값 v7-11 대조; codebox 코드 식별자 수정 |
| 9 | 부호검산(§10) | 부호 8항 전수 | S6 동결 vs 부등식 논리 보완; R4 추가(컷 상수 내용) |
| 10 | 전문 통독 | 완결성·고아 참조 0 | \label 누락 1건 보정; fig:lq_chain orphan 없음 확인 |

총 결함 발견·수정: 약 18건. 10라운드 수렴 기준(연속 2R 신규 결함 0) 달성.

---

## 3. 유도 복원 체인 (11식)

| # | 식 | 복원 단계 | 해당 절 |
|---|----|-----------|----|
| 1 | U_j(T) | G=H-TS → μ=∂G/∂n → ΔG=-sF(V-U) → ΔG=ΔH-TΔS 대입 → 풀기 | §3 (N2) |
| 2 | w_j | 이상격자 μ 로그몫 → g'=sF(V-U) → dξ/dV=sF·ξ(1-ξ)/RT → z=sF(V-U)/RT 기울기 → w=n_j RT/F | §5 (N4) |
| 3 | ξ_eq logistic | r⁺(1-ξ)=r⁻ξ 정지점 → r⁺/r⁻=e^{A/RT} detailed balance → ξ/(1-ξ)=e^{z} → 풀기 | §5 (N5) |
| 4 | 평형 peak | Q_cell q=Q_bg+ΣQ_jξ_j 보존식 → q 미분 → V 미분 → 연쇄율 dξ_eq/dV=σ_d ξ(1-ξ)/w → Q_j ξ(1-ξ)/w | §6 (N6) |
| 5 | ΔU_hys | g(ξ)=g⁰+RT[ξlnξ+(1-ξ)ln(1-ξ)]+Ωξ(1-ξ) → g''=RT/ξ(1-ξ)-2Ω → g''=0 근의공식 → ξ_s±=½(1±u) → V_eq(ξ) 대입 → artanh 정리 → 닫힌 식 | §4 (N3) |
| 6 | 분기 중심 | spinodal 평균=U_j(대칭) → 방향 자유도 1 → U_j^d=U_j+½σ_d h_η γ ΔU_hys | §4 (N3) |
| 7 | L_q | ODE dr/dq=dξ_eq/dq-r/L_q → 적분인자 e^{q/L_q} → 일반해 memory 합성곱 → k_j=r⁺(1+e^{-A/RT}) → Eyring → L_q=|I|/(Q_cell k_j) 로그4항 | §7 (N7) |
| 8 | cut A | dξ_eq/dq 정점의 5% 컷 → A=z_cut·n_j RT, z_cut=4.357, 상한 A_cap·RT — ∂lnL_q/∂V<0 은 동기이지 운영상 미분 아님 | §7 (N7) |
| 9 | ΔH_a^eff | 꼬리 구동력에서 상호작용 몫 분리 → 깊은꼬리 상수 Ω 흡수 → ΔH_a-χ_d Ω | §7 (N7) |
| 10 | L_V·인과꼬리 | L_V=|dV/dq|·L_q → ODE 일반해 지수 커널 → 이산 저역통과 ρ=exp(-Δgrid/L_V) → peak=(ξ_eq-ξ_lag)/L_V → 충전 격자역전 | §8 (N8) |
| 11 | 합산 | 보존식 선형 합 → C_bg+ΣQ_j[peak_shape] → V_n 역보간 | §9 (N9) |

---

## 4. 부호 8항 체크리스트

| # | 항목 | 결과 |
|---|------|------|
| S1 | U_j(T): ΔG=-sF(V-U) 부호, 발열→중심↑ | PASS |
| S2 | ξ_eq logistic: σ_d=+1, V↑→ξ_eq↑ | PASS |
| S3 | dξ/dV 부호: 절댓값, 방향 불변(양수) | PASS |
| S4 | ΔU_hys ≥ 0, Ω→2RT→0 연속; 방전 +/충전 - | PASS |
| S5 | χ_d 방전 χ/충전 1-χ, 합=1 제약, ΔH_a^eff=ΔH_a-χ_d Ω | PASS |
| S6 | ∂lnL_q/∂V<0 은 동기; 운영상 실현 미분=0 (컷 상수, 전이당 스칼라) | PASS |
| S7 | 꼬리 충전 격자역전; peak_shape=(ξ_eq-ξ_lag)/L_V>0 양수 | PASS |
| S8 | 분극 V_n=V_app-σ_d|I|R_n; 방전 측정>내부 | PASS |

전건 PASS — 부호 결함 0.

---

## 5. 그림 유래 / 신규 목록 (8개)

| label | 제목 | 유래 |
|-------|------|------|
| fig:spine | 코드 진행(spine) flowchart | v7-11 유래(구조 보존) |
| fig:staging | staging 갤러리 채움 | v7-11 유래(개선: 방향 화살표 명시) |
| fig:hysloop | 비단조 V_eq(ξ) + 과주행 경로 | v7-11 유래(축 레이블 영어 ASCII로 수정) |
| fig:logistic | logistic + ξ(1-ξ) 종 | v7-11 유래(축 레이블 영어 ASCII) |
| fig:reversal | 인과 꼬리 방향(방전/충전 패널) | v7-11 유래(보존) |
| fig:gxi_derive | g(ξ) 이중웰·spinodal·공통접선 | **신규** — ΔU_hys 유도 보조 |
| fig:lq_chain | L_q→L_V 사슬 개요 | **신규** — N7 사슬 의존도 시각화 |
| fig:fluxcross | (fig:hysloop 에 통합) | 병합 — v5 유래 플럭스 교점 내용 hysloop 주석으로 흡수 |

그림 내부 텍스트(레이블·축·범례) 전건 영어 ASCII. 한국어 캡션 본문만 허용(fig 환경 \caption).

---

## 6. 빌드 결과

| 단계 | 결과 |
|------|------|
| xelatex 1-pass | 17페이지, 경고만(cross-ref, lastpage — 정상) |
| xelatex 2-pass | 18페이지, 에러 0, 경고(font shape substitution, MiKTeX 업데이트 권고)만 |
| PDF 크기 | 343,778 바이트 |
| 빌드 엔진 | MiKTeX XeLaTeX (Windows), kotex + D2Coding |
| log 에러(!행) | 0건 |

---

*v8-02, 2026-06-29*
