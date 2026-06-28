# REVIEW2 — v7-07b.tex 적대 검수 (검수 sub, 검토2)

> 대상 `v7-07b.tex` (776행) 식·부호사슬 단위 청크 전문 정독.
> 기준 전문 정독: `Anode_Fit_v11_final.py`(1–706) · `v11_flowchart.md`(1–90, 분극 정정본) · `AUTHOR_BRIEF.md`(1–75).
> 추가: `REVIEW1.md`·`NOTEb.md` 대조, `v7-07.tex`↔`v7-07b.tex` diff, 수치 재검산(math 모듈).
> ★리뷰 전용 — 무수정, 본 파일 1개만 생성.

---

## 1. REVIEW1 보완 반영 검증 (C1·C2·C3 + self-test)

### H1 보완 (C1) — **반영·정확 PASS**
- eq:Veq_v7(L396–399)에 `+` 복원 확인: `V_{eq,j}=U_j+(RT/F)ln[ξ/(1−ξ)]+(Ω_j/F)(1−2ξ)`.
- 유도 다리 신설(L403–433): eq:spinodalpm→eq:spinodalplus/minus→eq:Vspinplus/minus→eq:dUhysraw. 산문 도입·식 사슬 모두 연결, "산문-only→명시 중간식 승격"(BRIEF §4) 정확 충족.
- 수치 재검산: `+` 형으로 `V_eq(ξ_−)−V_eq(ξ_+)`(Ω=12000,298K)=**0.08668564 V** = 닫힌형 ΔU_hys 와 **완전 일치**(1e-12 내). spinodal 끝점 항등식(ln, 1−2ξ, artanh) 전부 정확. REVIEW1-H1 의 G-follow 단절 해소.

### H2 보완 (C2) — **반영·정확 PASS (게다가 잠복 결함 동시 수정)**
- eq:dbv7(L290–296) 재구성: 옛 `𝒜_j=σ_d F(V−U)`(V 의존, N7 컷 A 와 글자 충돌) **완전 제거** → 무차원 `z_j=σ_d(V−U)/w_j`. L290 산문이 "기호 A_j 는 N7 컷 affinity 에 예약" 명시 → 이중정의 해소.
- N7(L490–500): driving force `Φ_j(V)=σ_d F[V_n−U_j^d]`(eq:drivingphi) 도입, eq:Acut 를 boxed 로 격상하고 "A_j 는 전이당 상수·V_work 무관" 명문화. frozen-A 함정 해소.
- ★잠복 결함 동시 수정: 옛 `𝒜_j/RT=σ_d F(V−U)/RT` 는 n≠1 에서 코드 `func_ksi_eq`(z=s(V−U)/(nRT/F)) 와 **n_j 배 불일치**였음. 신형 z_j 는 코드와 1:1(n=2 재검산 0.58386 일치). 즉 C2 는 H2 표면뿐 아니라 n-factor 차원 불일치까지 정정.

### C3 (유도 단계화) — **반영·정확 PASS**
- ΔU_hys: 위 H1 사슬로 단계화.
- L_q: eq:Lqcode 를 단일 equation→3-단 align 으로 전개(L526–543). 각 단 대수 정확(역수→k_B T/h 약분→ΔG_a 전개), 코드 `func_L_q` 로그형 일치.
- causal lowpass: eq:lowpassode→eq:lowpasssolve→eq:lowpassderived 신설(L592–604). `α=exp(−ΔV/L_V)`, `ξ̄_i=αξ̄_{i−1}+(1−α)ξ_eq_i` 재귀 = 코드 L117 정확 일치(항등 재검산 PASS).
- memory integral `+` 복원(eq:memoryv7 L585) + forcing 항 의미 산문(L589) 확인.

### self-test verifybox 추가 (NOTEb) — **반영·정확 PASS**
- L752–765 신설 4조건 전부 코드와 정합: selftest1(V_app−V_n=+I R_n>0)·selftest2(U^d_dis−U^d_chg=h_η γΔU_hys>0)·selftest3(A_j 방향무관, code L335 σ_d 부재)·selftest4(curve(dis)≡dqdv(s=+1), code L512/L617). 허위 없음.

---

## 2. ★신규 회귀 적발 (Codex 보완분 한정)

### CRIT / HIGH — **없음**
보완 4건 모두 부호·다리·코드정합 무결. 새 부호 역전·새 다리 단절·새 코드 불일치 0건.

### LOW (신규)

**N-L1 [L293–294, eq:dbv7] 간격 명령 중복(미관).**
`\exp(z_j), \qquad \quad z_j=...` — C2 재작성 시 `\qquad` 뒤에 `\quad` 가 남아 이중 수평간격. 렌더 무해하나 잉여(옛 줄 삭제 잔재). 1글자급 정리 대상.

**N-L2 [L401 vs L589] 자기참조형 메타 산문 2회.**
"여기서 두 항 사이의 $+$ 는 중요하다 … 누락되면 …"(L401), "식 …의 $+$ 는 … 빠지면 …"(L589) — 보완 의도(REVIEW1-H1/C3 동기)를 본문에 직접 노출. 교과서 prose 로는 다소 메타(검수 반응을 본문에 박음)이나, 물리 의미("forcing 이 지연 생성") 자체는 정확·유익. 경미 문체 감점.

> 신규 회귀는 위 2건(LOW)뿐. **보완이 결함을 만들지 않았고, 기존 HIGH 2건을 정확히 닫았다.**

---

## 3. 미해소 이월(REVIEW1, v7-07b 미터치 — diff 확인)

- **M1 [L102·315·454] 그림 내부 math 텍스트 깨짐 — 미해소.** `$V_app$`·`$sigma_d (V-U)/w$`·`$h eta gamma Delta U hys$` 가 첨자·그리스 아닌 이탤릭 변수곱으로 렌더. (BRIEF §5 ASCII 규약은 지켰으나 math 모드라 의미 전달 저해.)
- **M2 [L362] `^{net}` 위첨자 orphan — 미해소.** 본문 정의 없이 1회 등장.
- **L1 [L188] `2|V_n|` 표기 — 미해소.** `size(V_n)·2` 를 `|·|` 로 적어 노름 오독 여지.
- **L2 [bib] Anniés/Thinius 미인용 — 미해소.**
- 신규 라벨 11개(spinodalpm 등) `\ref` 0 — **orphan 아님**(유도 사슬 중간식·self-test, 직후 단계가 위치 소비). BRIEF "orphan 0"(prose 참조 figure/table/개념) 위반 아님. 빌드 로그 undefined/multiply-defined 0.

---

## 4. 재점수 (6 × /5 = /30)

| 차원 | v7-07 | v7-07b | 근거(Δ) |
|---|---|---|---|
| 1. 척추 정합 (N0→N9) | 5 | 5 | 변동 없음, 노드 커버 유지 |
| 2. 부호 사슬 (§8 8항) | 5 | 5 | 8항 PASS 유지(아래 §5) |
| 3. G-follow (유도 따라감) | 3 | **5** | H1 다리 복원(+ 사슬)·H2 z_j 재구성으로 두 단절 모두 해소. 재검산 일치 |
| 4. G-usable (재현·STAGING) | 4 | **5** | frozen-A 명문화·driving Φ 분리·self-test 4조건 추가 → 재현자 오구현 함정 제거 |
| 5. 완결성 (orphan) | 4 | 4 | 신규 사슬식 orphan 아님. M2 net·L1 표기 이월 −1 |
| 6. 형식 (수식주도·다리) | 4 | 4 | L_q/lowpass 단계화로 수식주도 강화. M1 그림·N-L2 메타 prose 이월/신규 −1 |
| **합** | **25/30** | **28/30** | **+3 (G-follow·G-usable 각 +2 / +1 회복, M1·M2·L1 잔존으로 5·6 유보)** |

> 28/30 미달 2점 = 전적으로 REVIEW1 미터치 이월분(M1 그림 math·M2 net·L1 표기). 보완이 대상으로 한 H1·H2 는 만점 회복.

---

## 5. 부호 8항 PASS/FAIL (코드 v11 재대조 · 보완 후)

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | U_j=(−ΔH+TΔS)/F | **PASS** | eq:UjT(L227)=code L69. U(298,4→3)=0.21088 재검산 |
| 2 | ξ_eq=logistic[σ_d(V_n−U)/w] | **PASS** | eq:dbv7/xieq(L294·307)=func_ksi_eq L86. z_j 신형이 n≠1 까지 코드 일치(개선) |
| 3 | dξ/dV=σ_d ξ(1−ξ)/w, peak>0 | **PASS** | eq:dxidVv7(L345)·eqpeakv7(L351). 1/(4w) 최대높이 재검산 |
| 4 | ΔU_hys≥0, U^d=U+½σ_d h_η γ ΔU_hys | **PASS** | eq:dUhysraw(L429) 유도 사슬 복원·재검산 0.08669. selftest2 dis>chg |
| 5 | χ_d=χ 방전/1−χ 충전, ΔH_a^eff | **PASS** | eq:chid(L511)=func_chi_d L160 |
| 6 | ∂lnL_q/∂V<0 | **PASS(부호+유도)** | eq:dlnLdV(L562)<0. driving Φ_j 분리·frozen-A 명문화로 REVIEW1-H2 유도결함 **해소** |
| 7 | 충전 격자역전 ξ[::-1]…[::-1], 거울 양수 | **PASS** | eq:chglowpass(L621)=code L477 |
| 8 | 분극 V_n=V_app−σ_d|I|R_n | **PASS** | eq:polarization(L168)=code L412. 서론 L76 "산화" 보강 |

**8항 전건 PASS (FAIL 0). 6항은 v7-07 의 유도결함(H2)까지 보완 후 완전 PASS 로 승격.**
