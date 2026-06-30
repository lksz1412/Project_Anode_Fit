# REVIEW1 — v7-07.tex 적대 검수 (검수 sub, v7-07)

> 대상 `v7-07.tex` (703행) 전문 정독(1–703, head→tail). 판정 기준 전문 정독:
> `Anode_Fit_v11_final.py`(1–706) · `v11_flowchart.md`(1–89) · `AUTHOR_BRIEF.md`(1–75).
> 수치 검산 = 별도 파이썬(func_L_q·U(298)·ΔU_hys 스피노달 끝점·dξ/dz).
> ★리뷰 전용 — 본 .tex/코드 **무수정**. 본 파일 1개만 생성.

---

## 1. 확정 결함 {심각도 · 행 · 틀린 것 · 옳은 형}

### CRIT — 없음
부호 8항·척추 N0→N9 순서·핵심 boxed 식은 모두 v11 과 1:1. 치명적 부호 역전·노드 누락 없음.

### HIGH

**H1 [행 397–401, eq:Veq_v7] 연산자 누락 — 유도 중간식 malformed.**
- 틀림: `V_{eq,j}(ξ)=U_j + (RT/F)ln[ξ/(1−ξ)] **(연산자 없음)** (Ω_j/F)(1−2ξ)`.
  두 분수항이 연산자 없이 병치 → 렌더 시 `(RT/F)ln[…]·(Ω_j/F)(1−2ξ)` 곱처럼 읽히는 잘못된/모호한 식.
- 옳은 형: `V_{eq,j}(ξ)=U_j + (RT/F)ln[ξ/(1−ξ)] **+** (Ω_j/F)(1−2ξ)`.
- 검산 근거: `+` 부호로 둘 때 `V_eq(ξ_s⁻)−V_eq(ξ_s⁺)`(Ω=12000,298K)=0.08669 V = 직후 닫힌형 eq:dUhysraw `ΔU_hys=(2/F)[Ωu−2RT·artanh u]`=0.08669 V 와 정확 일치. `−`/곱 형은 불일치.
- 영향: ΔU_hys(eq:dUhysraw)를 *유도*하는 단 하나의 load-bearing 다리식이 깨짐. 닫힌형 결과는 코드와 맞지만, "유도 사슬"이 그 결과로 이어지지 않아 G-follow 단절(BRIEF §4 수식 주도·유도 의무 위반).

**H2 [행 294 vs 473 · 511–516] 기호 `A` 이중정의 + 코드 불일치 사인 유도.**
- eq:dbv7(L294)는 `𝒜_j=σ_d F(V−U)`(running affinity, V 의존). eq:Acut(L473)는 `A_j=min{z_cut·n_jRT, A_cap_RT·RT}`(전이당 **고정** 컷). 같은 글자 A 가 두 다른 양 — 충돌 미고지.
- eq:dlnLdVraw(L511) 유도는 "방전 기준 A=σ_d F(V−U)" 로 **다시** A 를 V 의존으로 취급해 `∂lnL_q/∂V=−χ_dσ_dF/RT` 를 얻음.
- 그러나 코드(L335·L463 "전이당 상수")는 L_q 에 **고정** 컷 A 를 넣고 lag_len_V 를 전이당 1회 상수로 산출 — 실제로 L_q 는 V 에 의존하지 않음.
- 결론: §8-6 의 부호 *물리*(전위↑→장벽↓→꼬리↓)는 옳으나, 그 유도가 코드 구현(frozen-A)과 정합하지 않고 A 기호 충돌을 숨김. G-follow·G-usable(재현자가 A 를 V 함수로 오구현 유발) 결함.

### MEDIUM

**M1 [그림 fig:spine, 행 102] 그림 내부 라벨 LaTeX 문법 노출.**
`$V_n=V_app-sigma_d |I| R_n$` — TikZ 노드에서 `V_app`(밑줄 첨자 아님)·`sigma_d`(그리스 아님) 가 그대로 ASCII 로 박힘. BRIEF §5 "그림 내부 영어 ASCII 만"은 지켰으나, math 모드 안에서 `app`·`sigma_d` 가 이탤릭 변수곱으로 깨져 렌더됨(의미 전달 저해). 다른 그림들(fig:logistic `sigma_d (V-U)/w`, fig:hysbranch `h eta gamma Delta U hys`)도 동일 — 그리스/첨자가 평문 단어로 렌더.

**M2 [행 363, eq:eqprops] 최대높이 라벨 표기.**
`(dQ/dV)_{max,j}^{net}=Q_j/(4w_j)` 는 수치적으로 맞음(검산 0.25/(4w)). 다만 "net" 위첨자가 본문에 정의 없이 1회 등장(orphan 용어) — peak_shape_eq 자체가 net 인지 배경 제외인지 모호. 경미.

### LOW

**L1 [행 188, eq:nwork]** `2|V_n|` 표기 — 코드 `V_n.size*2`(원소 개수)를 `|·|`(절댓값/노름 기호)로 적어 "전압 노름의 2배"로 오독 가능. `2\,\mathrm{size}(V_n)` 류가 명확.

**L2 [참고문헌]** Anniés(코드 주석 dH_a 출처)·Thinius(L555·L562 LiC12/LiC6 활성화 근거) 미인용. 표 tab:staging 초기값의 DFT 출처가 bib 에 없음(G-usable 경미 — 값 자체는 표에 있음).

---

## 2. 강점 3 · 약점 3 (가장 약한 1)

**강점**
- S1. 부호 8항 전건이 v11 과 1:1 (logistic σ_d 위치·U_branch ½σ_d·χ_d 충전 1−χ·격자역전·분극 −σ_d 모두 정확). 검수 핵심 클래스 무결함.
- S2. 척추 N0→N9 완전 커버, 절 도입/마무리 다리 일관(각 절 끝 "N_ 의 출력은 …, N_ 은 …"). keybox 재현 7단계 + tab:codeids 가 G-usable 닫음.
- S3. boxed 핵심식이 코드 식별자(func_*) 와 명시 1:1 표기, func_L_q 수치 재현 rel-diff 1e-15.

**약점**
- W1 (가장 약한 1곳). **eq:Veq_v7 연산자 누락(H1)** — 유도 주도 문건에서 ΔU_hys 로 가는 유일한 다리식이 깨짐. 결과식은 맞아 "정확성"만 보면 통과하나, BRIEF §4 "산문-only/병치 단계를 명시 중간식으로 승격·수식 주도 유도" 의무를 정면 위반. 한 글자(`+`) 누락이지만 N3 유도의 논리 연결을 끊는 1급 결함.
- W2. 기호 A 이중정의 + frozen-A 코드 불일치(H2) — 재현자가 L_q 를 V 의존으로 오구현할 함정.
- W3. 그림 내부 수식 텍스트가 ASCII 평문으로 깨져 렌더(M1) — 시각 보조 효과 반감.

---

## 3. 차원 점수 (6 × /5 = /30)

| 차원 | 점수 | 근거 |
|---|---|---|
| 1. 척추 정합 (N0→N9 순서·커버) | 5 | 전 노드 커버, 절 순서 = spine, 다리 일관 |
| 2. 부호 사슬 (§8 8항 v11 대조) | 5 | 8항 전건 PASS(아래 §4) — 핵심 무결함 |
| 3. G-follow (유도 따라감) | 3 | H1 연산자 누락 + H2 기호 A 충돌이 두 핵심 유도 다리 단절 |
| 4. G-usable (재현·STAGING) | 4 | keybox 7단계+tab 닫힘·func_L_q 1e-15 재현. H2 frozen-A 함정 −1 |
| 5. 완결성 (orphan) | 4 | 식·그림·표 \ref 전부 사용, orphan 0. M2 "net"·L1 표기 경미 감점 |
| 6. 형식 (수식주도·전보체·다리) | 4 | 수식주도·절 다리 양호. H1 병치(승격 실패)·M1 그림 텍스트 −1 |
| **합** | **25/30** | |

---

## 4. 부호 8항 PASS/FAIL (코드 v11 대조)

| # | 항목 | 판정 | 근거(행·코드) |
|---|---|---|---|
| 1 | U_j=(−ΔH+TΔS)/F, ΔG=−FU | **PASS** | eq:UjT(L227)=code L69. U(298,4→3)=0.211=verifybox |
| 2 | ξ_eq=logistic[σ_d(V_n−U)/w] | **PASS** | eq:xieq(L306)=func_ksi_eq L86 (z=s(V−U)/w) |
| 3 | dξ/dV=σ_d ξ(1−ξ)/w, peak>0 | **PASS** | eq:dxidVv7(L346)·eq:eqpeakv7(L351). dξ/dz=xi(1−xi) 검산 일치 |
| 4 | ΔU_hys≥0, U_j^d=U+½σ_d h_η γ ΔU_hys | **PASS** | eq:Ubranch(L414)=func_U_branch L138. ΔU_hys≥0·Ω≤2RT→0(eq:dUhyszero) |
| 5 | χ_d=χ 방전/1−χ 충전, ΔH_a^eff | **PASS** | eq:chid(L480)=func_chi_d L160 |
| 6 | ∂lnL_q/∂V<0 (V↑→장벽↓→꼬리↓) | **PASS(부호)** / 유도결함(H2) | 부호 결론 옳음(eq:dlnLdV<0). 단 A 이중정의·frozen-A 코드 불일치는 유도 결함(점수3 반영, 부호 자체는 FAIL 아님) |
| 7 | 충전 격자역전 ξ[::-1]…[::-1], 거울 양수 | **PASS** | eq:chglowpass(L562)=code L477. fig:tailreverse+verifybox 거울 양수 |
| 8 | 분극 V_n=V_app−σ_d|I|R_n | **PASS** | eq:polarization(L168)=code L412. 충전 +|I|R_n verifybox |

**8항 모두 부호 자체는 PASS (FAIL 0).** §8-6 은 부호 결론 PASS 이나 유도경로에 H2 결함.

---

## 5. 분량 평가
짧지 않음. 곡선 식 누락·유도 생략 없음 — N2 Gibbs·N4 detailed balance logistic·N3 spinodal·N7 Eyring/BV·N8 1차완화 합성곱 모두 *유도*. 분량 결함 아님. (단 H1 으로 N3 유도가 명목상만 완결.)
