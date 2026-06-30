# P3 Step2 — 검토1 (별도 세션 Opus, 적대적 교차검증) 결과

> 8 supplement(S1-3·O1-3·C1·C3; C2 stall) vs Ch2.tex(751줄)+Ch1(eq:Se L948-1077)+P1 result. 직접 검산. 판정 줄근거.

## A. 확정 사실 (refute 후 잔존)
1. **q_rev 발열식 무결**: `q_rev=−IT·∂U_oc/∂T=−(IT/F)ΔS`, **T 한 번** [W]. 유도 ΔG=−FU→ΔS=+F·∂U/∂T→q_rev=−IT(ΔS/F) (Ch2 srcbox L650-654·eq:qrev L645). ∂U/∂T를 ΔS/F로 **치환**(곱 아님). 8 드래프트 일치.
2. **T-이중곱 = 지시문 축약일 뿐 본문 부재**: O2·O3가 차원검산([W·K·J/(mol·K)]≠[W])으로 "본문 옳음" 확정. **본문 결함 보고 = 허위 적발(금지).**
3. **부호·흡발열 교대**: 방전 ΔS>0→흡열/ΔS<0(stage 2→1 −16)→발열. ξ→1 config→+∞·ξ=½→ΔS⁰_j·충전 부호반전. 극한표 전원 일치.
4. **코드 엔트로피항**: dS_rxn(L78=중심표준값 ΔS⁰_j) vs dS_a(L100=활성화/비가역). 가역열엔 dS_rxn만. q_rev·dS_e 부재=P4. P1 충돌 0.
5. **이중계산 직교 — 진짜 위험 아님**: ΔS⁰_j(중심 config=0) ⊥ config 분포항 R ln[ξ/(1−ξ)]. **위험은 P4 구현 시점만**(중심값에 config 재가산 시). Ch2 파생 B가 이미 직교 분해 명시 → 본문 결함 아님.
6. **v5 w_eff 제거 타당**: 두-상 broadening(델타화 아님). use_w_eff 제거(L7) 정합. w 이중지위.
7. **★전자엔트로피 중복 = 정합적 중복(모순 아님)**: Ch1 eq:Se(L971)≡Ch2 eq:Se(L391) byte 동일 Sommerfeld. Ch2 L394-396 명시 인계. 별도 컴파일이라 label 충돌 무해. (단 Ch2 단위다리 N_A 곱 약식 vs Ch1 N_A k_B²=R k_B 명기 — 보강 권고.)

## B. 정정 필요 (Ch2 본문 정밀도 — 소수만 적발)
- **[정정-1] Ch2 L479 "Σ Q_j g_j=∂x/∂U" Q-인자 부정확**(C3 단독): g_j[1/V]·Q_j[C]→Σ Q_j g_j[C/V]=**dQ/dV**, ∂x/∂U(x 무차원)=[1/V]. 둘은 Q배 차. → "Σ Q_j g_j=dQ/dV=Q·∂x/∂U" 또는 "∂x/∂U에 비례(Q배)". 가중평균식(eq:weighted) 자체는 Q 공통이라 **결과 불변·서술만 정정**.
- **[정정-2] 버전 라벨 시대착오**(O1·O3): "Chapter 1 v9"(L395)·"Anode_Fit_v11"(L485·L747) → 현행(v1.0.10). 물리 무해, 독자 추적 혼동.
- **[정정-3] occupation2019 tier 미병기**(O1): L250-251 본문에 bib 강등(방법수준·dilute 한정) tier 1줄 병기.

## C. 체리픽 가이드
- 매트릭스·중복 = **O3**(12행 삼각·verbatim 5단계 대조) · 발열 유도·round-trip = **O2**(또는 O3 §3.1) · 비가역 IR+η_ct+η_diff 분해·라벨·tier = **O1** · Σ Q_j g_j 정밀화 = **C3 단독** · 부호 convention box = **C1**(D항 하향 후).

## D. 보완·정정
- **[D-1] C1 full-cell "CRITICAL 충돌" 과대 → NOTE 하향**: algebra(E=U_p−U_n→음극몫 +IT·∂U_n/∂T) 정확하나 **Ch2 warnbox L102-107이 전셀 범위 밖 선언** → 내부 충돌 0. v3 50_report exo/endo 오류는 v3 결함. convention box **추가는 방어적 유익(채택)**, tier NOTE.
- **[D-2] vib 부분몰 닫힌식 비대칭**(공통 공백, 정직 기술): ΔS_vib 한 줄 전개하면 config와 대칭(LOW).
- **[D-3] eq:logistic w=RT/F가 n_j=1 무조건 표기**(O2 단독): 코드 func_w=n·RT/F. "n_j=1 기준, 일반 w=n_jRT/F" 1줄(MED, 오독 차단).
- **[D-4] T→0 극한 + config T-의존**(전원 ξ 고정 암묵): 결론 q_rev→0 불변, 엄밀성 공백 — P4 ξ(T) 평가 순서 주의(보고만).

## E. 가장 약한 1곳
Ch2 §revheat 부호 박스(L651-653) 서술 흐릿(`ΔS=−∂(ΔG)/∂T=−(IT/F)·T·ΔS/T=...` 중간형 불필요) → `ΔS=F·∂U/∂T` 바로 대입해 `−IT·∂U/∂T=−(IT/F)ΔS`로 닫기(G-follow 1급). 물리 오류 아님·가독성.

## 핵심 verdict
발열식 차원 무결 · 이중계산 직교(P4만 주의) · 전자엔트로피 정합적 중복. 실제 정정 = Σ Q_j g_j 차원·버전라벨·tier 3건 + C1 과대적발 하향 + 부호박스 가독성.
