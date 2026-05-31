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

---

## 실행 완료 Addendum 2 (2026-05-31 — 사용자 선택 B: Ch1 적대 재검수 후 완성)

> 사용자 지시: "B로 일단 챕터1 먼저 완성하고 보자. 이게 흔들리면 그 뒤 전부 따라 흔들린다." → 신규 보강분 독립 적대 재검수 1패스 후 발견 정정.

### 적대 재검수 (3렌즈 병렬 sub-agent, 각 반증 임무 / read-only)
① 물리 타당성 ② 수학 무생략·대수오류 ③ 내부정합·컨벤션. 세 에이전트 독립 컨텍스트, 각 tex 전문 + AL_MASTER/REFERENCES/CHARTER/CLAUDE.md(P3) 정독.
- **CRITICAL(식 자체 오류) 0건** — 보강 결과식 대수·부호 전부 옳음(2번 에이전트 sympy로 8개 항등식 교차검증).
- **3 에이전트 만장일치 #1 = ρ_G 단위.**

### ★ 확정 뒤집힘 — ρ_G 단위 1/J → **mol/J** (Codex가 옳았음; PHASE_1B 판정이 판단오류)
- 본 result 상단 §"Codex 지적 중 기각"의 "ρ_G=1/J 유지, mol/J 기각"은 **틀린 판정이었다.** (환각 아님 — "확률밀도면 1/J"가 적분변수 G가 J일 때만 성립하는데, 본 문서 G=J/mol을 놓침.)
- 차원 증명: G=ΔG_a 가 본문 전체 J/mol(`exp[−ΔG_eff/RT]`의 RT 몰당 → 필연). ∫ρ_G dG=1 무차원 → ρ_G=1/[G]=mol/J. 교차검산 `A_L^prob=ρ_G·(RT/L)` 무차원 ⇔ ρ_G=mol/J(1/J면 1/mol로 깨짐). 상위 정본 `RB_AL_MASTER.md` line 81도 이미 mol/J → tex가 정본과 충돌하던 것.
- 정정: tex 기호표 line 127 `1/J → mol/J`. **[[feedback_confirmed_items_policy]] 확정 사항 정정 — 근거(차원증명) 명시 후 뒤집음.**

### 발견·정정 (8 edits, 삭제 0 / 단위 1건만 정정 + 나머지 유도단계 삽입)
| 등급 | 위치 | 정정 |
|---|---|---|
| CRIT-인접 | 기호표 ρ_G | 1/J→mol/J (+ A_0/A_L^prob/A_L^amp/L_0/L_min 등재 + U_j 재정의 주석) |
| HIGH | eq:L_of_G | 닫힌 지수매핑이 활성화 지배 극한(k_eff≈k_j, eq:kphys k_lim→∞) 전제임 명시. 꼬리영역 정당화 + 병목 유효시 Ch6 |
| HIGH | eq:single_kernel | L이 일반적으로 q-함수(k_j의 A 지수의존)이나 가정(나)dA/dq≃0이 L상수를 **귀결**로 함의 → 적분 밖 추출 근거 명시 |
| MED | eq:mu_mix | ∂G_mix/∂ξ=μ_config 근거(per-site intensive, ∂/∂n=(1/N)∂/∂ξ, N 상쇄) 한 줄 |
| MED | eq:Geff | χ=½(대칭 Marcus 1차 정확값) vs 0≤χ≤1(곡률 비대칭 λ_f≠λ_b / BEP 경험 기울기) 출처 분리 |
| MED | keystone | "정확 항등"이 r±=상수 가정 위에서만 정확(ξ-의존이면 국소선형화) 명확화 + common-mode가 Marcus 비대칭 이동(λ∓A)의 대칭 평균 모형선택임 명시 |
| FLAGGED | eq:xi_dist | 독립 평행 1차 완화 = 평균장 ansatz. staging은 협동적 1차 상전이(nucleation, funabiki AL-3)라 mode간 결합 무시 → FLAGGED(Ch3·Ch6 검증) |

### 적대 발견 중 미정정 (사유 명시)
- 298 K vs 298.15 K(25°C): 수치(25.68/22.23 mV) 자기일관, 0.15 K 무해 — 유지.
- kernel_integral r(q_a)→A_0 흡수: 이미 "post-peak 공통값 근사"로 명시됨(근사 표기 충분) — 유지.

### 빌드·무결성 (재빌드)
- tex **662줄**(641→662, +21). xelatex 2-pass. PDF **13p** → `Claude/results/graphite_ica_ch1_rebuilt.pdf` 갱신.
- env: equation 25/25, begin/end 41/41(flagbox +1). 진짜 undefined ref/cite **0**, "undefined references"/"may have changed" 경고 **0**, **Overfull hbox 0**, `!` 에러 0.

### 현재 = 사용자 최종 검토 (Ch1 완성판)
적대검수 정정까지 반영한 Ch1 완성판. GO 시 Phase 2(Ch2, step 43). main 머지·push 승인 전 금지.
