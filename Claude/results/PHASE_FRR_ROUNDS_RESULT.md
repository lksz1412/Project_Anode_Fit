# PHASE_FRR 재검토 라운드 누적 Result (R.1~)

각 라운드 = 3챕터(_Fable) 절별 전문 정독 재검수(Agent 병렬, refute·빈통과 금지, 물리+해설 렌즈) → master 삼각검증 → 수정 → 빌드 0/0 → 커밋+푸쉬. 수렴까지(최소 10회).

## R.1 (steps 50–51)
**검수**: 4창(ch1 전반/후반·ch3·ch4) 전문 정독. 적발 확정 결함 — ch1 전반 7·후반 7·ch3 8·ch4 7 = **29건**(빈통과 0).
**핵심 수정**(master 삼각검증 후 전부 적용):
- ★**ch3 가역열 부호 오류**: 전극 단독형은 $q_\rev=+IT\,\partial V^\rev/\partial T$ — 엔트로피 수지($q_{out}=T\dot\sigma-T\dot S_{sys}$)로 재유도, 풀셀 검산($E=U_{cat}-U_{an}$ 음극 몫 부호반전→표준 Bernardi 복원), 질서 plateau 탈리튬화=흡열 물리검산 — 3중 확인 후 6곳 부호 연쇄 수정(3.1·3.6·3.15·prose·worked×2) + 전극단독형 유도 해설 추가. h_balance 예제 54mV→비가역 24mV+가역 ±30 재계산(ΔT∞ 0.24K, master 예제와 정합).
- ch3: q_hys 첫 등식 Σ|I_j|(충전 부호)·q_pol=|I|η·eq:h_dVdT에 Q_j 가중+C_bg(전하보존 음함수 미분)·η_hys=유효(에너지) 과전압 명시·"|I|→0 히스만 남음"→가역(교환·상쇄)/히스(소산) 구분·(1.6) 몰형 인용·단열≠runaway·헤더 주석.
- ch1: §synth boundbox(i) 병합 전 잔재("본 장 밖"→§hys_branch/§master 내부) ★·ξ_ss=ξ_eq 증명 이상극한 한정+Ω≠0 일반화 주석·vdW "양의 압축률"→압축률 음(κ_T<0)·∂g/∂θ=μ−μ⁰·이중우물 "정확히 둘"=오목구간 유일성 귀속(대칭은 배치만)·μ 단조 단상한정·분산/표준편차 3곳·hys_branch 식별주의 gap-1차로 통일(표·S5 정합) ★·충방전 "둘만 더하면"=중심·분극 한정(충전 꼬리 S3′·S4′ 별도)+keybox 동단서·γ 평탄 조건 물리 방향 정정(빠른 핵생성=작은 과주행 고정, spinodal 아님) ★·gap–|I| 곡률 방향(ln 포화=아래로 오목; 위로=확산/γ(|I|))·가정⑥ 온도무관 추가·T_c 수치=하한(>2RT_room)+절편 기울기 사전판별·DVA(ii) vs-Q 좌표 직독.
- ch4: 제목 Chapter 4→**Chapter 2**(식두 2.x·의존트리 결정 정합; 파일명 불변)·η_j=A_net/F 기본형 한정(표)·기본형 전제 boundbox 신설·C_j 방향의존 조건 본문 명시(상수면 U_j 흡수=평형 동치)·Ṡ_irr 닫기식(Σ(Q_j/F)(J⁺−J⁻)A_net/T, W/K 차원 검산)·eyring/evanspolanyi 인용 부착·α "anodic"→forward 한정.
**빌드**: ch1 35p·ch3 10p·ch4 6p 전부 0/0. ch1 인계번호 불변(전수 대조).
**검산 통과(수렴 증거)**: 4창 보고의 통과 목록 — logistic 사슬·FWHM·ΔU_hys 유도·54mV·u³ 극한·eq:arrhenius 이항·superpose 재현·loop 면적 등가·Duhamel·안정성·BV 선형화·i₀ 유도·ξ=α 극대·전류분배.
