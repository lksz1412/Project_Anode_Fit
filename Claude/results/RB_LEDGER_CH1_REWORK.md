# RB_LEDGER_CH1_REWORK — Ch1 §7+ 자기완결 재작업 Result (2026-06-01)

> 트리거: 사용자 검토 — Ch1 §7+ 부실(식 뜬금없이 등장·물리의미 불명·연결 부족·Ch1만으로 피팅 근사식 못 뽑음). 검수가 정확성만 보고 따라갈 수 있음/쓸 수 있음 못 봄. 계획서: `Claude/plans/2026-06-01-ch1-self-contained-rework-plan.md`.

## 1. 진단 (확정)
원천 consolidated_ch1 §7+(11절)의 실무·닫힌형 내용을 rebuilt 가 Ch6으로 이관·압축(4절) → Volterra 뜬금 등장(닫는 §closure 부재), fiteq 가 안 풀린 Volterra 의존, 심플 근사식 부재(0.2C 드롭). 단순 컴팩션 소실이 아니라 \*구조적 deferral\*.

## 2. 방법 (재발 방지)
절별 청크 작업 + **절별 청크 검수**(전체 tex 한 번에 검수 X — 이번 핵심 수정). 각 절 = 물리 동기 prose → display 식 + step → 변수·적분 의미 1줄 → 무비약 연결.

## 3. 재작성 (W1~W7, Ch1 662→795줄, 15p)
| W | 절 | 내용 |
|---|---|---|
| W1 | §kernel | A_L 물리 의미 명시("완화 길이별 꼬리 분해 분포") |
| W2 | §kernel/closure | Volterra 자기참조 동기(되먹임) + Θ_init 정의 + **Plan B(g-grid validator) + Plan A 닫힌형 eq:closed 복원**(선형화 b=−(Q_p/C_bg)∂Θ_eq/∂V_n → ratio ansatz → factor-out, 무결성 b→0 복귀). Fredholm↔Volterra 가정차 BOUNDED |
| W4 | §fiteq | S5 "Ch6" → 본 장 closure(Plan B/A)로 닫힘. dΘ/dQ=(1/Q_cell)dΘ/dq bridge 복원 |
| W5 | §ch1_simplefit(신설) | **single-mode 심플 근사식 eq:simplefit**(Θ=Θ_0(1−e^{−(q−q_a)/L}), L=|I|/(Q_cell k)) + **0.2C 기준식 eq:02c** + 데이터 피팅 절차(0단계 식별성 전제→L→유효엔탈피→χ) + EMG 초기값 |
| W6 | §falsify | 식별성 파라미터 제한 순서(저속OCV→펄스R_n→Arrhenius→전류χ→ρ_G독립) |
| W7 | §ch1_numeric(신설) | Ch6 수치 core 흡수(g-grid·index-1 DAE·근거기반 tolerance·ε_tol 검증·격자수렴). 전달노트 Ch6 해체 반영 |

## 4. 집중 적대검수 (§7+만 범위, 청크)
G-follow 대체로 PASS(원천보다 유도 동기 강화), **G-usable 초기 FAIL → 정정 후 PASS**. 발견·정정:
- **C1(CRITICAL)**: simplefit (2)"A_j→0 순수 ΔH_a" ↔ (3)"V_drive 흔들어 χ" 데이터영역 자기모순. → (2)는 \*유효\* 엔탈피 −(ΔH_a−χA)/R, 순수 ΔH_a는 A→0 외삽(별 영역), χ는 peak근방(유한 A) — 영역 분리 명시.
- **H1**: χ 추출 가로축 V_drive=V_n 은 비측정 내부전위 + R_n 공선형. → 0단계 식별성 전제(저속OCV·펄스R_n 선고정·V_app→V_n 환산) 박음. "본 장만으로"가 §falsify 식별성을 가리키게(여전히 Ch1 자족).
- **H2**: q_a 결정 절차 부재(L과 공선형). → q_a 먼저 고정(ICA peak/dξ_eq/dq 임계) 후 L 단일회귀 명시.
- **H3**: r(q_a) 공통값 흡수가 항등 아닌 가정. → L-의존 가능, BOUNDED 명시.
- **M2**: dΘ/dQ 좌표 bridge 복원.

## 5. 빌드·무결성
tex **795줄**, PDF **15p** → `Claude/results/graphite_ica_ch1_rebuilt.pdf`. env equation 29/29·begin-end 46/46. 진짜 undefined ref/cite 0, dup label 0, overfull 0, `!` 0. 신규 cite(jcp2017/lee2011/son2013) bibitem 추가·해소. 신규 label(eq:selfcoupling/eq:closed/eq:simplefit/eq:02c/sec:ch1_simplefit/sec:ch1_numeric) 충돌 0.

## 6. 결과
**Ch1 자기완결 달성**: §7+ 가 물리 동기+무비약으로 따라가지고, §ch1_simplefit 에서 실데이터에 바로 대입하는 single-mode 닫힌식 + 0.2C + {L,ΔH_a,χ} 추출 절차가 나온다. Ch6 수치·피팅 내용 Ch1 흡수.

## 7. 2차 패스 — 절 분할 + 청크 검수 발견 정정 (사용자 "§7 이후 전부·잘게 쪼개·제대로" 재지적)
1차가 §8 등을 구조만 바꾸고 §7 본체·따라가짐을 덜 봤다는 지적. 2렌즈 청크 검수(따라가짐/정확성) 후 §7→끝 \*절 분할\* + 발견 전건 정정:
- **§7 spectrum**: dense 박스 → 3단계(자코비안 eq:spectrum_prob → 지지범위 → 진폭 A_0) 무비약 분해. A_0 측도불일치 정정(개수 ρ_G ≠ 용량가중 관측 Θ, 별개량 명시).
- **§8 kernel integral / §9 Volterra(신설 절) / §10 Plan B(신설) / §11 Plan A(신설)** 로 분할(빽빽함 해소, 사용자 "절 늘려도 됨"). **Volterra 를 single-mode ODE 상수변화법(eq:singlemode_integral)에서 유도** → "뜬금없이" 제거. **Plan A: Θ^(0) baseline 정의 신설 + ratio-substitution factor-out 한 줄 대수 명시 + b 부호 ∂Θ_eq/∂V_n>0(eq:dxidV) 근거.**
- **§13 simplefit**: (2)↔(3) 순환 읽힘 정정 — A_j 는 각 점 \*기지값\*(자유 X), (3)→(2) 비순환 순서 명시.
- **§14 falsify**: ★N5 비퇴화 discriminator 추가(검수 H-2, "이론의 가장 약한 지점") — tail scaling L∝|I|은 transport와 퇴화 → 전위의존 Arrhenius slope + GITT/pulse로 η_ct(R_ct) 분리 후에만 χ_j 귀속.
- **Ch6 미아 forward-ref 8곳 전부 장내 절(§planB/§planA/§ch1_simplefit/부록)로 재지정** (사용자 "끊긴 forward-ref" 지적).
- bibitem: lee2011 serial 124112→121102 정정, dubarry2022·fly2020 추가(N5 인용).
- 빌드: tex **859줄**, **17p**, env eq 31/31·eq* 1/1·begin/end 49/49, undefined 0, dup label 0, overfull 0, `!` 0.

## 9. 3차 패스 — 절별(fine) 청크 검수 8 agents + 발견 전건 정정 (사용자 "2청크는 너무 거칠다·잘게 쪼개" 재지적)
2차의 2렌즈(따라가짐/정확성) 검수가 \*전체 묶음 2청크\*라 거칠다는 지적 → §7~§15 를 \*절마다 1 agent\* (8 병렬, §14+§15 합본)로 적대 재검수. **거친 2청크가 못 본 ~25 결함 적발**(CRITICAL 1·HIGH ~10·MED ~10·LOW). 전건 정정(본 패스 = tex 859→923줄, 17→18p):
- **§7 spectrum**: [HIGH] 단계3 A_0 도입이 Σ→∫ 측도전개 없이 단정 → \*단계3 측도변환 무비약 유도\* 신설(Θ=Q_p⁻¹ΣQ_mξ_m → ∫Q(L)ξA_L^prob dL, A_0≡Q/Q̄=Radon–Nikodym 가중). "측도 불일치 아님" 오기 정정. [MED] G(L) 역변환 출처(eq:L_of_G→G풀이) 명시·L_min 단계1→단계2 선후 정리. [LOW] σ_G=ρ_G 표준편차 정의.
- **§8 kernel**: [HIGH-1] r(q_a;L) 흡수 \*한 줄 대수\*(r̄ factor-out→A_L 재흡수) + L-의존 편향부호(감소함수→꼬리앞 가팔라짐, Plan B 대조). [HIGH-2] eq:kernel_integral(q_a 자유감쇠)↔§9 Volterra(q' 목표구동) 역할 \*봉합\* 한 문장. [MED] single-mode δ(L−L\*) (L\*=실제 길이, L_0 prefactor 와 구별). [MED] 실효 하한 L_min>0, 1/L 발산 차단 명시.
- **§9 Volterra**: [MED] 무결성점검이 single-mode δ-collapse 한정임 명시 — 분포 A_L 의 q→∞ = (∫A_L dL)Θ_0, A_0≡1 일때만 Θ_0. [LOW] (ii) 일반화서 Θ_eq L-무관(ξ_eq,j g-무관) 전제 명시. [LOW] Θ_0 기호중복 → 초기 mode 진행 Θ_init,0(L) 로 분리.
- **§10 Plan B**: [HIGH] 평균식 정규화 봉합 — Σw_mρ_G(g_m)=∫ρ_G dg=1 (새 가중 아닌 적분 이산화) display 추가, 비균일 격자 정규화 재계산. [MED] validator ε 정량정의(‖Θ_A−Θ_B‖/‖Θ_B‖) 본문화. [MED] "물리결론 성립" 완화 closure 전제 재명시.
- **§11 Plan A**: [HIGH] a(q') 미정의 → a=Θ_eq(V_n(Θ⁰))−bΘ⁰ (Taylor 절편) 명시. [HIGH] C_bg/Q_p forward-ref → eq:selfcoupling 전에 Q_pΘ≡ΣQ_jtotξ_j·C_bg≡∂Q_bg/∂V_n 정의(상세 §fiteq). [MED] ratio ansatz 정당화(|b| 섭동→형상 baseline 지배, b→0 정확).
- **§12 fiteq**: [HIGH] L_φ 미유도·미정의 → 환산 유도(post-peak dV_n/dq 상수근사→eq:Lphi 신설) + 기호표 L_φ[V] 등재. [MED] eq:dVdq↔eq:dQsplit 동일식 명시(C_bg 곱·dq=dQ/Q_cell). [MED] post-peak bridge 적용영역 본문화(peak 영역 dΘ/dq→dΘ_eq/dq) + Θ_A 미분대입 명시.
- **§13 simplefit**: [CRITICAL] step(2) Arrhenius 기울기에 k_0(T)=(k_BT/h)κ Eyring prefactor T-의존 누락 → ln(1/(LT)) 회귀(prefactor 보정) + U_j(T) 비선형 혼입 점별 제거(종속변수 y(T)=ln(1/LT)+χA_j(T)/RT 회귀→−ΔH_a/R). prefactor 무시 BOUNDED(ΔH_a/RT≫1). [HIGH] Θ_0 nuisance amplitude 명시(모델 y=Ae^{...}+baseline, ICA꼬리≈(Q_p/C_bg)(Θ_0/L)e^{...}, 분모≈1). [MED] (0) V_app→V_n eq:Vapp 직접역산(루프 아님). [MED] 0.2C anchor→(3) χ 회귀 가로축 정렬 연결.
- **§14 falsify**: [HIGH] ★N5 (a) signature 가 D(ξ) 확산율속(thermodynamic factor 경유 전위의존 유효엔탈피)과 \*여전히 퇴화\* → (a)·(b) AND 조건 + k_{j,lim} 전위무관 가정 위에서만 + GITT relaxation transient(√t Cottrell vs 지수)로 확산율속 배제. [MED] "(eq:simplefit (2))" 참조혼동 → "(eq:simplefit; 추출 §ch1_simplefit 절차(2))". [MED] forward-only 헤더 과일반화 → "forward-prediction 검정; 역산 금지". [LOW] spectrum shift 부등호 χ_j≥0 전제.
- **§15 numeric**: [MED] 격자수렴 비정량 gate → ‖Θ_{Ng}−Θ_{2Ng}‖/‖Θ_{2Ng}‖≤ε_disc 정량 종료조건(ε_tol 체인 봉합). 전달노트 Plan A/B closure ref §kernel→§planB/§planA 정정.
- 빌드: tex **923줄**, **18p**, xelatex 2-pass EXIT 0, undefined 0, `!` 0, dup label 0, rerun 0, overfull 4(전부 <20pt cosmetic). PDF → `Claude/results/graphite_ica_ch1_rebuilt.pdf`.

## 10. Next (잔여)
- Ch6 파일 해체(삭제) + full_rebuilt/refs 재생성(Ch1 재작업본 + eq:Lphi/Θ_init,0/측도유도 반영) + Ch2~5 "Ch.6" 참조 정리.
- 같은 절별(fine) 따라가짐/사용성 청크 검수를 Ch2~5 후반 절에 적용(deferral·압축 가능성).
