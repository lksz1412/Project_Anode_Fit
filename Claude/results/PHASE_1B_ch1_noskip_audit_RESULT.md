# Phase 1B — Ch1 무생략 감사 + Codex 교차검증 Result

> 사용자 지시(5-31): Ch1 PDF 수식에 "약간의 건너뜀" → 내용=리뷰논문 깊이 유지, 전개=학부 교재 무생략. + Codex 의견·작성 비교. + "수정 필요한 부분만 수정 → 다시 검수". + "분량 임의 축소 금지(내용 소실·환각 방지)".
> 4갈래 교차검증: 내 Agent 3(구간 A/B/C) + 워크플로 w37b88pni + 워크플로 w1c518wxb + Codex exec(b553mb9d7, 70,933 tok).

## Summary
Ch1(graphite_ica_ch1_rebuilt.tex 561줄) 유도 건너뜀(skip)을 학부 교재 기준 전수 식별. 4갈래 동일 skip 수렴. Codex 가 Claude 4갈래 누락 물리오류 2건 추가 적발. 결과식 전부 옳음 — 전개 단계만 보강(줄 추가, 삭제 X).

## 보강 확정 skip (전원 일치) — 수정 대상
1. eq:logistic 혼합엔트로피 (BIG): RT ln[ξ/(1-ξ)] = W=N!/(n!(N-n)!) → S=k_B ln W → Stirling → S_mix=-R[ξ ln ξ+(1-ξ)ln(1-ξ)] → μ_config=∂(-TS_mix)/∂n=RT ln[ξ/(1-ξ)]. +Ω항 ∂[Ω ξ(1-ξ)]/∂ξ=Ω(1-2ξ). +μ⁰→U_j 흡수(U_j=U_j⁰-μ⁰/(s_φ F)).
2. eq:single_kernel (BIG): r≡ξ_eq-ξ → dr/dq=dξ_eq/dq-dξ/dq, post-peak dξ_eq/dq≃0 → dr/dq=-(1/L)r → 변수분리 dr/r=-dq/L → 적분 → r=r(q_a)e^{-(q-q_a)/L}.
3. eq:Geff (BIG/MED): Marcus ΔG‡=(λ-A)²/(4λ)=λ/4-A/2+A²/(4λ) → 소구동력 1차 Taylor → χ=1/2(대칭)/일반 0≤χ≤1(비대칭 BEP·transfer coeff).
4. keystone k=r⁺+r⁻ (MED): ξ̇=r⁺-(r⁺+r⁻)ξ=(r⁺+r⁻)(ξ_eq-ξ) 인수분해(정상점·k 동시 산출). r± 국소상수면 "선형화" 아닌 정확 항등.
5. MINOR~MED: ξ풀이 4줄 / eq:dxidV 도함수 / 차원 A=C/s 치환 / eq:dxidq chain-rule / L_of_G 부호반전.

## Codex 추가 적발 물리오류 2건 (수정 대상)
1. eq:fiteq "동치" 주장 오류: "1-Q_p(dΘ/dQ)>0 가 eq:monotone 과 동치" → 틀림. C_bg=∂Q_bg/∂V_n>0(배경용량 국소 단조성)와 분모 1-Q_p(dΘ/dQ)>0(동역학 경로 dV_n/dQ>0)은 별개 조건 → "동치" 삭제, 두 조건 분리 서술.
2. eq:spectrum support 누락: G≥0 → L≥L_min=L_0 exp[-χA/RT], L<L_min 서 A_L=0(Heaviside H(L-L_min)). A_0 곱하면 확률밀도 보존 깨짐 → A_L^prob(정규화) vs A_L^amp=a(L)A_L^prob 명칭 분리.

## Codex 지적 중 기각 (Claude 판정 우위)
- ρ_G 단위 "mol/J" 기각 → 확률밀도(∫ρ_G dG=1 무차원)면 1/J 맞음(어제 정정 옳음). 유지. 단 "A_0 곱하면 보존 깨짐"은 옳아 명칭 분리만 채택.
- (추가 채택) eq:logistic μ⁰→U_j 흡수: U_j=U_j⁰-μ⁰/(s_φ F) 한 줄.

## Codex 비교 총평
수렴: skip 식별 양측 동일. Codex 우위: 물리오류 2건 추가검출(독립모델 교차 실효). Claude 우위: ρ_G 단위(1/J) Codex 오류 역검출. 결론: 양측 결합이 단일보다 우월.

## 수정 원칙 (사용자 5-31 명시)
- 분량 임의 축소 금지. 기존 본문 한 글자도 삭제·축약 X(물리오류 2건의 틀린 문장만 정정). 보강 = 식 사이 유도 단계 끼워넣어 늘림.
- 한 식씩 Edit → 줄수 증가 확인 → 다음. 통째 재작성(Write) 금지.

## Next
수정(skip 5 + 물리오류 2, ρ_G 1/J 유지) → 사용자 3대 검토: ① 컨벤션 통일 ② 물리 논리 전개 ③ 리뷰논문 내용을 교재 수준 상세함으로 설명했는지. → PDF 재빌드.

---

## 실행 완료 Addendum (2026-05-31 재개 세션 — HANDOVER_RB 복구 후)

> 위 분석은 보존. 본 addendum = 위 "Next" 의 보강 실행 결과 기록(append-only).

### 적용 경위 (분할 실행)
- 직전 세션(토큰 끊김 전): 보강 4영역 선적용 — ① eq:logistic 혼합엔트로피 무비약 유도(Stirling→S_mix→μ_mix, Ω항 곱미분, μ⁰→U_j 흡수, ξ_eq 풀이 4줄) ② eq:dxidV 저온거동 연쇄법칙 ③ eq:Geff Marcus 1차 Taylor ④ keystone k=r⁺+r⁻ 정확 인수분해. (561→616줄, 미커밋 상태로 중단)
- 본 재개 세션: 잔여 6건 적용 완료. tex 616→641줄(+25, 삭제 0).

### 본 세션 적용 6건 (한 식씩 Edit, 삭제·축약 X)
| # | 식 | 보강 내용 | 종류 |
|---|---|---|---|
| 1 | eq:single_kernel | r≡ξ_eq−ξ → dr/dq=dξ_eq/dq−dξ/dq, post-peak dξ_eq/dq≃0 → dr/dq=−(1/L)r → 변수분리 dr/r=−dq/L → 적분 → r=r(q_a)e^{−(q−q_a)/L} (L 일정 가정 명시) | skip BIG |
| 2 | eq:dxidq | 연쇄법칙 dξ/dq=(dξ/dt)(dt/dq), dt/dq=Q_cell/|I|, eq:dxidt 대입 | skip |
| 3 | 차원 | A=C/s, k=s⁻¹, Q_cell=C 치환 → (C/s)/(C·s⁻¹)=1 무차원 명시 | skip |
| 4 | eq:L_of_G | L=|I|/(Q_cell k_j)에 k_j=k_0 e^{−ΔG_eff/RT} 대입 → 1/k_j=(1/k_0)e^{+ΔG_eff/RT} 지수 부호반전 명시 | skip |
| 5 | eq:fiteq | **Codex 물리오류 정정**: "1−Q_p dΘ/dQ>0 ⟺ eq:monotone(C_bg>0)" 동치 주장 삭제 → C_bg>0(정적 배경 단조성)와 분모>0(동역학 경로 dV_n/dQ>0, dV_n/dQ=(1−Q_p dΘ/dQ)/C_bg)은 별개·둘 다 필요로 분리 서술 | Codex |
| 6 | eq:spectrum | **Codex 물리오류 정정**: G≥0 → L≥L_min=L_0 e^{−χA/RT}, L<L_min서 A_L=0 (Heaviside H(L−L_min)) support 추가. + 명칭분리: A_L^prob=ρ_G(G(L))(RT/L)H (정규화, ∫=1) vs A_L^amp=A_0·A_L^prob (진폭, 비정규화). 이하 kernel의 A_L≡A_L^amp 선언. ρ_G 단위는 1/J 유지(Codex의 mol/J 지적 기각). | Codex |

### 빌드·무결성 (PDF 재빌드)
- xelatex 2-pass, `-output-directory=Claude/work/build`, PDF → `Claude/results/graphite_ica_ch1_rebuilt.pdf` 복사.
- **13페이지**(보강 전 11p). env balance: equation 25/25, begin/end 40/40, document 1/1.
- 진짜 undefined ref/cite **0**(pass2서 "undefined references"/"Label(s) may have changed" 경고 소거). `!` 에러 0.
- undefined 4건 = 전부 한글 폰트 italic/bold-italic shape 대체 경고(UnBatang/UnDotum, 무해). macdonald 오귀속 잔존 0, svare2000 3.

### 사용자 Decision Gate 대기 (3대 검토)
① 컨벤션 통일 ② 물리 논리 전개(무생략 여부) ③ 리뷰논문 내용을 교재 수준 상세함으로 설명했는지. → GO 시 Phase 2(Ch2, step 43) 진입. main 머지·push 는 승인 전 금지.
