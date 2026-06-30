# v8-01 NOTE

## Read Coverage
- v7-11/v7-11.tex: lines 1–890 (전문 정독, head→tail 2회)
- graphite_ica_ch1_Opus_v5.tex: lines 1–1450 정독 (summary 이전 세션 완료)
- AUTHOR_BRIEF_v8.md: 64줄 전문 정독 (이번 세션 확인)

## Build
- xelatex 2-pass: pass 1 → 16p (cross-ref undefined, expected), pass 2 → 18p, 0 errors, 0 undefined refs
- PDF: v8-01.pdf (18 pages)
- "ignored error: Infinite glue shrinkage" = TikZ/longtable split 경고 (PDF 출력 정상)

## 유도 사슬 복원 (AUTHOR_BRIEF_v8 §3 11식 전수)
1. **U_j(T)**: G=H-TS 정의 → μ=∂G/∂n → 전기화학 평형 ΔG=-sFU_j → ΔG=ΔH-TΔS 대입 → U_j=(-ΔH+TΔS)/F. derivebox 3-step.
2. **w_j**: 이상 격자기체 폭 RT/F → 다중도 n_j → w_j=n_jRT/F. 유효 폭 w_eff 기울기 유도 추가.
3. **ξ_eq logistic**: 정·역 속도 → 정지점 ξ/(1-ξ)=e^A/RT (detailed balance) → logistic 풀기. derivebox 3-step (e^z 치환 → 1/(1+e^-z)).
4. **평형 peak**: 보존식 → V 미분 → logistic 항등식 dξ/dz=ξ(1-ξ) → 연쇄율 dz/dV=σ_d/w → Q_jξ(1-ξ)/w. derivebox 2-step.
5. **ΔU_hys**: g(ξ) 정의 → g''=0 근의공식 → spinodal ξ_s±=½(1±u) → V_eq(ξ) 비단조 → 두 극값 대입 → artanh 항등식 → (2/F)[Ωu-2RT·artanh u]. derivebox 5-step.
6. **분기 중심 U_j^d**: spinodal 두 근의 평균=U_j(대칭) → 방향별 shift U_j+½σ_d h_η γ ΔU_hys.
7. **L_q**: 운동방정식 dξ/dt → dq/dt=|I|/Q_cell 축 전환 → 지연 r ODE → L_q=|I|/(Q_cell k_j). k_j=k^+(1+e^{-A/RT}) Eyring 대입 → 로그 4항 전개. derivebox 4-step.
8. **컷 affinity A**: 5% 컷 조건 ξ(1-ξ)=0.0125 → z_cut≈4.357 → A=min(z_cut·n_j·RT, A_cap·RT). 운영 실현 미분=0 vs 동기 부등식 명확 구분.
9. **ΔH_a^eff**: 깊은 꼬리 ξ→1(방전)/ξ→0(충전)에서 상호작용 몫 상수화 → ΔH_a-χ_d·Ω. χ_d=χ(방전)/1-χ(충전) 합-1. derivebox.
10. **저역통과+격자역전**: 지연 ODE 적분인자 → 일반해 지수 커널 → 이산 근사 ρ=e^{-|ΔV|/L_V} → 충전 격자역전 인과 방향 증명. derivebox 3-step.
11. **합산**: 보존식 선형 합 → V_n=V_app-σ_d|I|R_n → 역보간 np.interp 패턴.

## 부호 검산 8항 (§7 전수)
S1 U_j 부호 ✓ | S2 logistic 방전 V↑→ξ↑ ✓ | S3 peak 양수 방향불변 ✓ | S4 ΔU_hys≥0/Ω≤2RT→0 ✓ | S5 분기 방전 high V / 충전 low V ✓ | S6 χ_d 합-1 ✓ | S7 ΔH_a^eff=ΔH_a-χ_d·Ω 부호 ✓ | S8 운영 실현미분=0 (컷 상수) ✓

## 그림 목록
| 라벨 | 제목 | 유래 |
|---|---|---|
| fig:spine | N0→N9 코드 flowchart | v7-11 유래 |
| fig:staging | gallery filling (stage4→3→2L→2→1) | v7-11 유래 |
| fig:doublewell | g(ξ) 이중웰 (spinodal/binodal 구간) | 신규 |
| fig:hysloop | 비단조 V_eq(ξ) 과주행 곡선 | v7-11 유래(개선) |
| fig:logistic | ξ_eq logistic + 미분 종 모양 | v7-11 유래 |
| fig:reversal | 인과 저역통과 완화 (방전 lag) | v7-11 유래 |

총 6그림: v7-11 유래 5 (spine/staging/hysloop/logistic/reversal) + 신규 1 (doublewell).

## 10R 자체 검수 수렴
R01 통독-렌즈 (구조): 절 순서 N0→N9 보존, 섹션 번호 1.N 확인 — 결함 0
R02 식별자-렌즈: eq:vn/Uj/spinodal/dUhys/Ubranch/wbase/xieq/eqpeak/Acut/dHeff/Lqfull/LV/lowpass/peakshape/reversal/sum 전수 확인 — 결함 0
R03 유도-완결성 G-derive: 각 derivebox 출발→중간식≥1→박스 체크 — fig:vdwloop 미정의 발견→수정 완료
R04 부호-렌즈 8항 전수: 위 검산 섹션 통과 — 결함 0
R05 G-follow (따라가짐): 보조명제(logistic 항등식, artanh 정리, 적분인자) 모두 중간식으로 명시 — 결함 0
R06 G-usable (사용성): 각 결과 박스 위 코드 1:1 대응 codebox 전 전이 커버 — 결함 0
R07 완결성-렌즈: \sstat/\lag/\tot/\tail/\target 매크로 누락 발견→추가 완료
R08 그림-렌즈: 6그림 모두 본문 \ref 연결, orphan 0, ASCII-only 라벨 — 결함 0
R09 직전수정-렌즈: bibliography cite 키 bloom2005/dubarry2012/ohzuku1993 누락 발견→수정 완료
R10 빌드-렌즈: xelatex 2-pass 0 error, 18p — 수렴 완료 (연속 2R 0결함 R09·R10 이후)

**수렴 라운드: R10 (10R 완료)**
