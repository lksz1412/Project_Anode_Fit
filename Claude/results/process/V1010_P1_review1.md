# P1 Step2 — 검토1 (별도 세션 Opus, 적대적 교차검증) 결과

> 9 드래프트(S1-3·O1-3·C1-3) vs 코드 `Anode_Fit_v1.0.10.py`(ground truth). 코드 전문 정독 + 4 검산 스크립트로 contested 주장 독립 수치 확인. 모든 판정 줄 근거.

## A. 확정 사실 (9 드래프트 옳게 합의 — 코드 근거)
- **맵·물리식 9/9 정확**: func_w=nRT/F(74-75)·func_U_j=(−ΔH+TΔS)/F(78-79)·func_ksi_eq overflow-safe logistic z=s(V−U)/w(94-97)·func_L_q ln분해(100-107, I≤0→−inf)·_causal_lowpass 1차 IIR(110-128)·func_dU_hys (2/F)[Ωu−2RT artanh u], u=√(1−2RT/Ω)(133-140)·func_U_branch U+½σ_d h_η γ ΔU_hys(143-148)·func_dH_a_eff ΔH_a−χ_d Ω(152-155)·func_chi_d(158-163). dqdv 체인: 분극 V_n(408)→분기중심(444-450)→ξ_eq(455)→L_V(459-460)→peak=(ξ_eq−occ_lag)/L_V(475)→interp(479)·충전 격자역전(473). σ_d 다경로 일관 전파.
- **audit**: 흑연 음극 전용(LCO·발열 q_rev·전자엔트로피 dS_e 부재). 면적보존 = use_w_eff 제거(7·283)로 ξ_eq 폭·분모 w 정합 회복(평형 ∫≈0.97=ΣQ). func_U_j_hys 死코드. seed_L_V 진단·초기값 전용. 'w' 폴백 inert.

## B. 결함 진위 표 (8 주장 — 코드 확정)
| 주장 | 진위 | 근거 |
|---|---|---|
| func_U_j_hys 死코드 | 참 | 82-91 정의, 미호출. func_U_branch(447) 대체 |
| 'w' 폴백 inert('n':1.0 우선) | 참 | _n_factor 274 'n' 우선 반환 |
| z_cut docstring "ξ_eq 5%" 부정확 | 참 | 218 literal. 실제 = ξ(1−ξ)/0.25=5.00%(ξ_eq=98.73%·1−ξ=1.27%) → 정규화 미분 5%, 점유 아님 |
| D4 z_cut 항상 A_cap=4RT capped | 참(조건부) | A=min(4.357RT,4RT)=4RT(331). **n=1 & z_cut≥4 한정** inert; z_cut<4 또는 n≠1이면 binding |
| D5 χ=0.5→충방전 대칭 | 참 | func_chi_d(0.5,±1)=0.5 양쪽 → ΔH_eff 동일 |
| equilibrium U_j 사용(dqdv와 불일치) | 참 | 365 func_ksi_eq(T,V,U_j,n_j) 분기중심 미적용. γ=1,I→0서 eq peak@U_j=0.120 vs dqdv 0.163/0.077 |
| 비등온 T(V) 히스 스칼라 T_rep 근사 | 참 | 447 T_rep=mean(T_work)(426). U_j·w는 배열인데 ΔU_hys만 스칼라 |
| 면적보존 _causal_lowpass DC gain=1 | 참 | 계수 z=1서 (1−a)/(1−a)=1 |

**틀린 핵심 식 0·줄 오인 0**(전부 ±2줄 내).

## C. 정정 필요
1. S1 §2.2.1(161) "방향 불변 충족 + s=+1 미반영" 자기모순 → 배제. equilibrium 분기중심 미적용(dqdv 불일치)을 O3/S3 식으로 명확히.
2. z_cut docstring 부정확(C1만 적발, S1/S2/C 복창) → 정정.
3. D4 z_cut cap(O3만 적발) → 조건부 명시.
4. n≤0 미가드(NaN/음수) = C1/C2/C3 강하게 실증, O계열 약하게(LOW) → C 실증 채택.
5. C2/C3 서두 지시파일 경로 오기재(트랙 혼입, 내용은 유효).

## D. 체리픽 가이드
| 섹션 | 최강 | 취할 요소 |
|---|---|---|
| 맵 | **O1** | 24심볼 줄근거 표 + 데이터흐름 + 차원검산. S2 호출자 보강 |
| 맵(eq vs dqdv) | **O3 §1-G** | 7축 비교표(유일 명시) |
| audit | **O3** | §0 수치검산 표 + C1/D4/D5 결함ID. O2 차원검산 보강 |
| audit(피팅 실용) | **C1+C2** | n≤0·dVdq_qa silent·chi 범위·Cbg 미검. C3 피팅 4단계 |
| 인벤토리 | **O3 §3 + C3** | 2계층(주8/보조10) + 3등급(자유/조건부/고정) + 피팅순서. S 축 다이어그램 |
→ 종합: O3=audit·인벤토리 골격, O1=맵 골격, C1/C2=피팅 실용 결함, S=가독 다이어그램.

## E. 가장 약한 1곳
S2 = audit 최얕음(D4·D5·z_cut docstring·n≤0 가드 4건 누락). S1 §2.2.1 방향불변 행 자기모순.

## F. 보완 필요 (9 드래프트 전부 놓침)
1. func_U_j_hys(83) `s:int=1` vs func_U_branch(148) `sigma_d` 인자명·기본값 차이(외부 직접호출 부호 혼동).
2. equilibrium(350) T 스칼라 전용(352) — 배열 T(V) 미지원(dqdv만 지원).
3. n_work=max(min, V.size·2)(412) → seed_L_V sub-grid 접힘 임계가 사용자 V 점수 종속(해상도 의존).
4. self-test(567-703) 면적=Q assert 부재(plot_dqdv.py 외부 위임) — 면적 회귀가드 없음.
