# v8-04 자체검수 NOTE

> graphite_ica_ch1 v8-04 — v7-11 배치 보존 + 유도 과정 단계적 복원 교과서 확장판.
> 독립 작업(9건 경쟁 중 1건). 산출 = `v8-04.tex` (자족, xelatex 2-pass 통과) + `v8-04.pdf` (22p).

## 1. Read Coverage (전문 정독 행범위)

| 문건 | 경로 | 정독 행 | 비고 |
|---|---|---|---|
| AUTHOR_BRIEF_v8 | `Claude/results/v8-00_spine/AUTHOR_BRIEF_v8.md` | 1–64 (전문) | ★권위 사양. §3 11식 유도단계·§7 부호 8항 |
| v7-11.tex | `Claude/results/v7-11/v7-11.tex` | 1–890 (전문, 2창: 1–504·505–890) | ★배치 보존 대상. 절순서·박스·그림5·표4·부호절 |
| v5.tex (유도 원천) | `Claude/docs/graphite_ica_ch1_Opus_v5.tex` | 1–1882 (전문, 4창: 1–500·500–999·999–1478·1478–1882) | ★중간식 출처. Boltzmann→Eyring→Gibbs→μ→detailed balance→logistic→spinodal→ODE 적분인자→지수기억 |
| v11_final.py (코드 정본) | `Claude/results/v7-00_spine/Anode_Fit_v11_final.py` | 1–706 (전문) | 식·부호·식별자 1:1 대조 |
| v11_flowchart.md | `Claude/results/v7-00_spine/v11_flowchart.md` | 1–90 (전문) | 척추 N0→N9 + 부호규약(2026-06-29 분극 정정 반영) |

v6 = 미제공(브리프 §2 지시) → 보지 않음.

## 2. ★유도 사슬 복원 목록 (v7-11 이 점프한 중간단계 → v8 에서 메운 것)

v7-11 은 결과 박스는 옳으나 "대입하면 [박스]"로 점프했다. v8-04 가 각 박스 위에 [출발식→연산→중간식≥1→박스]를 복원:

| # | 박스 식 | v7-11 점프 | v8-04 복원한 중간 단계 (식 라벨) |
|---|---|---|---|
| 1 | U_j(T) (eq:Uj) | ΔG=ΔH−TΔS "넣어 풀면" | G≡H−TS(eq:gibbsdef)→μ≡∂G/∂n(eq:mudef)→전기화학 평형 μ=μ⁰−sF(V−U)·ΔG=−sFU(eq:eqcond)→대입→박스 |
| 2 | V_n (eq:vn) | 박스만 제시 | 출발식 V_app=V_n+σ_d|I|R_n(eq:vapp, 신규 명시)→이항→박스 |
| 3 | ξ_s± spinodal (eq:spinodal) | g″=0 "근의공식" 한 줄 | g(ξ)(eq:gxi)→2회 미분 항별 전개→g″(eq:gpp)→ξ²−ξ+RT/2Ω=0(eq:spinquad)→근의공식→박스 |
| 4 | ΔU_hys (eq:dUhys) | spinodal "대입하면 닫힌다" | V_eq(ξ)(eq:Veq)→극값=spinodal 확인(미분)→대입 logit 역수·(1−2ξ)=∓u(eq:hyssub)→극대−극소 3줄 align(eq:hysdiff)→artanh 정리→박스 + 임계극한 Taylor u³ |
| 5 | U_j^d 분기중심 (eq:Ubranch) | 평균=U_j "대칭" 선언 | 두 spinodal 평균=U_j 명시 계산(로그합 0·(1−2ξ)합 0)(eq:hyssym)→γ 축소→박스 |
| 6 | ξ_eq logistic (eq:xieq) | "detailed balance 로 닫힌다" 한 줄 | Eyring(eq:eyring)→정·역 BV 속도(eq:bv)→비=e^{A/RT}(χ상쇄, eq:db)→운동방정식(eq:relax)→정지점비(eq:stationary)→풀이(eq:logisticsolve)→박스 |
| 7 | 평형 peak (eq:eqpeak) | logistic 미분 "종 항등식" 점프 | 보존식(eq:charge)→궤적미분→관측식(eq:dQdV)→logistic 몫미분 종 항등식 dξ/dz=ξ(1−ξ)(eq:belliden)→연쇄율 dz/dV=σ_d/w(eq:dxidV)→박스 |
| 8 | ΔH_a^eff (eq:dHeff) | "흡수되어" 한 줄 | 꼬리 구동력 −Ω(1−2ξ) 분리→깊은꼬리 ξ→1(충전거울 ξ→0) 상수 +Ω 흡수→박스 |
| 9 | L_q/L_V (eq:Lqfull·lnLq·LV) | k_j "넣으면" | 운동방정식÷dq/dt→지연ODE·L_q 정의(eq:Lq)→정·역합 k_j=k⁺(1+e^{−A/RT}) detailed balance(eq:kuniv)→Eyring k⁺ 대입→L_q 전개(eq:Lqfull)→로그 4항(eq:lnLq)→|dV/dq| 곱(eq:LV) |
| 9b | 컷 affinity A·χ_d (eq:Acut·chid) | 박스 | χ+χ′=1 강제 유도(합-1)→방향 분기 χ_d |
| 10 | peak_shape 인과꼬리 (eq:peakshape) | "적분인자로 닫힌 해" 한 줄 | 적분인자 e^{q/L_q} 완전미분(eq:intfactor)→일반해 지수커널 합성곱(eq:memory)→이산 저역통과 ρ=e^{−Δgrid/L_V}(eq:lowpass)→박스 + 충전 격자역전(eq:reversal) |
| 11 | 합산 dQ/dV (eq:sum) | 박스 | 보존식 선형 ΣQ_jξ_j→궤적미분(eq:dQdV)→각 항 peak_shape→박스 |

총 11 식(브리프 §3 의 11) 전부 단계 복원. "한 줄 점프" 0건.

## 3. 부호 사슬 8항 체크리스트 (브리프 §7, v11 코드 대조 — 전건 PASS)

1. U_j(T)=(−ΔH+TΔS)/F, ΔG=−FU : 발열 ΔH<0→중심↑. ✓ (eq:Uj/eqcond)
2. ξ_eq=logistic[σ_d(V−U)/w], 방전 V↑→ξ↑ : ✓ (eq:xieq)
3. dξ/dV=σ_d ξ(1−ξ)/w, peak=|·| 양수·방향불변 : ✓ (eq:dxidV/eqpeak)
4. ΔU_hys≥0, Ω≤2RT→0, 분기 ±½σ_d : 극대>극소, u→0 연속, U_dis>U_chg. ✓ (eq:dUhys/Ubranch)
5. χ_d 방전 χ/충전 1−χ, ΔH_a^eff=ΔH_a−χ_dΩ : 합-1 거울. ✓ (eq:chid/dHeff)
6. ∂lnL_q/∂V : 컷 상수라 운영 실현미분=0, 부등식 <0 은 컷규칙 동기. ✓ (eq:lnLq/LV)
7. 꼬리 충전 격자역전 ξ[::-1]…[::-1], 충전 dQ/dV 방전 거울(양수) : ✓ (eq:reversal)
8. 분극 V_n=V_app−σ_d|I|R_n, 방전 측정>내부 : ✓ (eq:vn/vapp; 2026-06-29 정정본 일치)

수치 self-test 재산출(코드 __main__ 대조): ΔU_hys(Ω=12000)=86.7 mV·u=0.766 / Ω=2RT=4958 J/mol→0 / ΔU_hys(4RT)=54.8 mV(v5 ~55) / U(298)2→1=0.0853 V(목표 0.085). 전부 일치.

## 4. 그림 목록 (8개; ASCII-only 내부텍스트 0 Hangul 확인)

| # | label | 유래 | 내용 |
|---|---|---|---|
| 1 | fig:spine | v7-11 유래(그대로) | 코드 진행 N0→N9 척추 |
| 2 | fig:staging | v7-11 유래(그대로) | 흑연 staging 갤러리 채움 |
| 3 | fig:overshoot | ★신규 | V_eq(ξ) 극값=spinodal(g″=0) 근거 |
| 4 | fig:doublewell | ★신규 | g(ξ) 이중웰 + spinodal/준안정 띠 |
| 5 | fig:hysloop | v7-11 유래(그대로) | 비단조 V_eq 과주행·ΔU_hys |
| 6 | fig:logistic | v7-11 유래(그대로) | ξ_eq logistic + 종 미분 |
| 7 | fig:relax | ★신규 | 지연 ODE 일반해 완화(추종 vs 기억꼬리) |
| 8 | fig:reversal | v7-11 유래(그대로) | 인과 꼬리 방향·충전 격자역전 |

유래 5(v7-11 그대로 채택) + 신규 3. 검증 스크립트로 8개 tikzpicture 전부 내부텍스트 Hangul=0 확인.
v3–v6 그림 재사용 0. orphan: 모든 fig \ref 본문 존재 + 도입 동기 선행.

## 5. 보존 확인 (v7-11 → v8-04)

- 절 순서 N0→N9 + 부호검산절 : 동일.
- 결과 박스 식 11개·식별자·부호 : v7-11·v11 코드와 1:1 (변경 0, 유도만 추가).
- 표 4종(staging·inputs·nodemap; longtable 기호표) : 값·기본값 그대로.
- 범위: 곡선 11식 유도만. 무관 일반론(lever/chord/cotangent 상평형 세부·적층·ch2+·Arrhenius 회귀·피팅 알고리즘 S0–S5) 미유입(과확장 0).

## 6. 빌드 결과

- 엔진: xelatex (MiKTeX), `-interaction=nonstopmode`, 2-pass(clean rebuild).
- 결과: **exit 0 · LaTeX `!` 에러 0 · undefined ref/cite 0 · Overfull hbox 0 · 22 페이지 PDF(391 KB)**.
- 잔여 경고: (i) kotex italic Hangul 폰트 fallback(UnBatang, cosmetic) (ii) longtable 페이지분할 "infinite glue shrinkage" 무해 note(출력 정상). 둘 다 렌더 영향 없음.
- 라벨 69(중복 0)·ref 61(missing 0)·cite 5(bib 전부 존재)·boxed 11·numbered eq 48.

## 7. 10R 검수 추이 (가변 청크·렌즈)

| R | 청크 | 렌즈 | 결함 발견 | 조치 |
|---|---|---|---|---|
| 1 | N3 통독 | G-derive 유도완결성 | ΔU_hys 부호(극대-극소 logit 역수) 재검 → v5 verbatim-equiv 일치 확인(거짓경보) | 무수정(검산 PASS) |
| 2 | 식블록 | 부호 8항 | 분극 V_n 부호 2026-06-29 정정본 일치 확인 | 무수정 |
| 3–5 | (Agent) 전문 | G-derive 11박스 재유도 | (대기) | (대기) |
| 6–7 | (Agent) 전문 | 코드 1:1 + 박스=v7-11 | (대기) | (대기) |
| 8–9 | (Agent) 전문 | 그림 orphan/ASCII/다리 | (대기) | (대기) |
| 10 | N4/N5·N6 logistic | G-usable 가독·다리 | logistic 사슬 완결·코드매핑 확인, 수치 self-test 4건 재산출 일치 | 무수정 |

(3–9 Agent 결과 반영 후 갱신)
