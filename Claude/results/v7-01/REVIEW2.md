# REVIEW2 — v7-01b.tex 보완본 검토2 (검수 sub, 리뷰 전용)

대상: `Claude/results/v7-01/v7-01b.tex` (854행, PDF 15p·빌드 에러 0 확인).
판정 정본: `Anode_Fit_v11_final.py` (706행, func_L_q L90–97) · `v11_flowchart.md` (분극 정정본) · `AUTHOR_BRIEF.md`.
방법: 식·부호사슬 단위 청크 정독(head→tail) + func_L_q 수치 재산출(code vs tex) + refute mandate + 가장 약한 1곳.
대조 기준선: REVIEW1(v7-01, 25/30, 항목6 FAIL).

---

## ① 보완 반영 {항목별 OK / 미흡}

| 보완 항목 | 판정 | 근거 |
|---|---|---|
| **N1: A 를 전위의존→전이당 상수 컷 `min(z_cut·n·RT, A_cap·RT)` 로 교정** | **OK** | §N7 「컷 affinity: 전이당 상수 $A_j$」(L497–507) 신설. eq:Aj 박스 + "전위 격자 $V_n$ 에 의존하지 않는다"(L507) 명시. REVIEW1 CRIT-1 의 옛 `A=sF(V−U)` 전제 제거 확인. 수치: `min(4.357·1·RT, 4·RT)=9915 J/mol` (cap 바인딩) — 코드 L335 정합. |
| **N1: `∂lnL_q/∂V` 는 동기로만 격하** | **OK** | L585–589 「$\partial\ln L_{q,j}/\partial V_n$ 의 물리적 해석」 paragraph 로 격하 + "코드 구현 내에서 $L_{q,j}$ 가 전위 격자별로 다르게 계산되는 것은 아니다" 명시. 체크리스트 항목6(L809–812)도 "코드에서 $L_{q,j}$ 는 전이당 한 번 계산되는 상수" 로 재정의. CRIT-1 RESOLVED. |
| **N2: 닫힌형 $L_q$ 에 −TΔS_a(ΔG_a) 정합** | **OK** | eq:dGeff(L538–540) `ΔG_a^eff = ΔH_a^eff − TΔS_a` 신설. eq:Lq 박스(L566–568)·eq:kuniv(L550)가 ΔG_a^eff 사용. 코드 L96 `dG_a=dH_a−T·dS_a` 와 1:1. **수치 재산출: ln L_q(code) = ln L_q(eq:Lq) = −15.3348 (dS_a=0), dS_a=20 에서도 일치(±1e-10).** REVIEW1 HIGH-1 RESOLVED. |
| **로그형 절편 b_j 정합 복원** | **OK** | eq:lnLq(L576–579) 절편 `b_j = −ΔS_a/R − ln(1+e^{−A/RT})`. **원본 v7-01 은 `+ln(1+...)` (부호 오류) → 코드와 불일치였는데 b 에서 `−ln(...)` 으로 정정**(code reconstruct 일치 확인). 닫힌형=로그형 자체모순 해소. |
| **부호 체크리스트 8항 재확인** | **OK** | L795–807 8항 전건 재서술, 항목6 재정의 반영. (단 ②의 신규 회귀 참조) |

→ **명시된 4개 보완은 전부 정확히 반영. CRIT-1·HIGH-1(REVIEW1) 모두 해소.**

---

## ② 신규 회귀 {심각도 / 위치 / 내용}

### NEW-HIGH-1 — S4 Arrhenius 식 eq:arrhenius 가 보완 과정에서 부호 2개 flip (regression)
- **위치**: eq:arrhenius (L784–786), §S4.
- **내용**: b 가 lnLq 절편 부호(−ln(1+e^{−A/RT}))를 정정하면서 **S4 로 일관 전파 못 해 부호가 깨짐**. 인쇄식:
  `y(T) ≡ ln(T*/(L_q T)) − (−χ_d A)/RT + ln(1+e^{−A/RT})` = `… + χ_d A/RT + ln(1+e^{−A/RT})`.
  eq:lnLq 에서 올바른 격리는 `y = ln(T*/(L_q T)) − χ_d A/RT − ln(1+e^{−A/RT})` (두 항 모두 반대 부호).
- **실증(수치)**: 인쇄식 y_tex 와 우변 `−ΔH_a^eff/R·(1/T)+ΔS_a/R` 의 차 = **정확히 +4.0363 상수**(258/298/318 K 전부 동일). 올바른 격리식은 차=0(일치).
- **심각도 근거 (CRIT 아님)**: A/RT 가 전위·온도 무관 상수(A=A_cap·RT)이므로 오프셋이 T 무관 → **기울기 −ΔH_a^eff/R 는 여전히 정확히 복원**(절편만 어긋남). 다만 **인쇄된 등식이 우변과 대수적으로 거짓**이고, 원본 v7-01 의 오프셋(~0.018, ln(1+e^{−A/RT}) 만큼)보다 **~200배 악화**됨 → 보완이 직접 깬 회귀. brief §8·G-usable: 이 문건만으로 χ_d A 보정량을 빼는 독자가 부호 틀린 식으로 절편을 오산.
- **옳은 형태**: `y(T) ≡ ln(T*/(L_q T)) − χ_d A_j/RT − ln(1+e^{−A_j/RT}) = −ΔH_a^eff/R·(1/T) + ΔS_a/R`.

### NEW-MED-1 (경계: reorg 가 노출) — S3 χ 식별식 eq:S3chi 가 기본 데이터셋에서 무력
- **위치**: eq:S3chi (L774–776), §S3 「전이별 꼬리에서 χ 식별」.
- **내용**: χ-경로 재정리로 도입된 `ln(L_Vj/L_Vj') = (ΔH_eff 차)/RT − χ_d(A_j−A_j')/RT + const`. 그러나 GRAPHITE_STAGING_LIT 4전이 전부 `n_j=1`·전역 z_cut/A_cap → **A_j 가 전 전이 동일(9915 J/mol)** → `A_j−A_j'=0` → **χ_d 항 소멸 → χ 식별 불가**. 전이별 `n_j` 또는 per-tr z_cut/A_cap 가 달라야만 식별됨(문건은 이 전제를 명시 안 함).
- **심각도 근거**: 순수 부호 오류 아님(G-usable 갭). 보완(A=전이당 상수)의 부산물로 노출 — 완전 신규는 아니나 χ-경로 재정리가 직접 건드린 곳.
- **옳은 형태**: "전이별 n_j 또는 z_cut 가 다를 때만 S3 로 χ 분리 가능; 동일 A_j 데이터셋에선 S3 불가, S4 절편 또는 비대칭 gap 으로" 전제 명시.

### 신규 회귀 아님(확인): 부호 flip·orphan 신설·유도 다리 끊김·인접식 모순
- **부호 flip**: N7 핵심 사슬 eyring→kuniv→relaxq→Lq→lnLq 재검산 — kuniv 의 `e^{−(ΔG_eff−χ_d A)/RT}` 와 L_q=|I|/(Q·k) 의 역수 부호 flip, (1+e^{−A/RT}) 의 곱↔나눗 전환 모두 일관(코드 정합). **사슬 내 신규 부호 flip 0.**
- **orphan 신설**: 신규 eq:dGeff·eq:Aj 모두 앞 동기(eq:eyring/eq:dHeff)·뒤 사용(eq:Lq/L_q box)으로 연결. \ref 미사용 라벨은 전부 section 라벨(ToC/hyperref 사용) + 번호 본문인용 eq → dangling/orphan 0. 빌드 undefined ref 0.
- **유도 다리 끊김**: 절 도입·마무리 다리 유지. N7 신설 절(컷 affinity)도 앞(eyring)·뒤(χ_d/장벽) 연결.
- **인접식 모순**: 닫힌형 eq:Lq ↔ 로그형 eq:lnLq 이제 일치(원본 자체모순 해소). verifybox(L289–291) 산술 재검(8229.6/96485=0.0853) 정확.

### 미해소 carry-over (신규 아님, 추적용)
- REVIEW1 MED-1(equilibrium()=eq:eqpeak 동일시의 U_j vs U_j^d): L470 V_peak=U_j^d·L476 동일시 그대로 — 미수정.
- REVIEW1 MED-2(spinodal 과주행 방향 vs v5 정본 반대, L328–330): 그대로 — 미수정. (코드 영향 0.)

---

## ③ 재점수 (각 /5, REVIEW1 대비 Δ)

| 차원 | v7-01 | v7-01b | 근거 |
|---|---|---|---|
| ① 척추 정합 | 5 | 5 | N0–N9 절 대응·flowchart·코드 라인 1:1 유지. |
| ② 물리·부호 | 3 | **4** | CRIT-1(전위의존)·HIGH-1(−TΔS_a) 해소로 +1. 단 NEW-HIGH-1(S4 부호 2-flip)로 만점 불가. |
| ③ G-follow | 4 | **4** | 컷 affinity 절·물리적 동기 격하로 코드 오인 제거(개선), 그러나 S4 식 부호 거짓이 따라가는 독자 오도(상쇄). |
| ④ G-usable | 3 | **3** | 박스식 −TΔS_a·항목6 정합으로 재현성 개선(+), 그러나 S4(NEW-HIGH-1) 부호 거짓 + S3(NEW-MED-1) χ 식별 무력으로 피팅 절차 결함(−) → 순증 0. |
| ⑤ 완결성(orphan) | 5 | 5 | 신규식 앞동기·뒤사용, dangling 0, 빌드 undefined 0. |
| ⑥ 그림 | 5 | 5 | TikZ 4종 렌더 라벨 ASCII(한글은 `%` 주석뿐, 렌더 무관)·\ref 사용·빌드 15p 에러0. |
| **합** | **25/30** | **26/30** | 보완으로 +2(②③ 물리), NEW-HIGH-1 S4 회귀로 −1 환원 → 순 +1. |

---

## ④ 부호 체크리스트 8항 PASS/FAIL (brief §8 · 코드 대조)

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | U_j=(−ΔH+TΔS)/F, ΔH<0→U_j>0 | PASS | eq:Uj+verifybox(0.0853V) 코드 L68 정합. |
| 2 | ξ_eq=logistic[σ_d(V−U)/w] | PASS | eq:ksi_eq 코드 L84·L459 정합. |
| 3 | dξ/dV=σ_d·ξ(1−ξ)/w 양수 | PASS | eq:dxidV w 분모 약분 정확. |
| 4 | ΔU_hys≥0, Ω≤2RT→0 | PASS | eq:dUhys 코드 L123 정합(Ω=2RT→0 수치확인). |
| 5 | χ_d 방전χ/충전1−χ, ΔH_a^eff=ΔH_a−χ_dΩ | PASS | eq:chid·eq:dHeff 코드 L149·L155 정합. |
| 6 | A_j=min(z_cut·n·RT, A_cap·RT) 전이당 상수; L_q 전위독립 | **PASS** | **재정의 후 코드 정합**(원본 FAIL → 해소). L504·L581·L804 + 동기 격하 paragraph. ★보완 핵심 성과. |
| 7 | 충전 격자역전 후 dQ/dV 양수 | PASS | eq:reverse + verbatim L652–655 코드 정합. |
| 8 | 분극 V_n=V_app−σ_d|I|R_n | PASS | eq:vn 박스 코드 L412 정합. ★분극 방향 서술(L222–224 "방전 V_n<V_app")이 flowchart 정정본(L88)과 동일 — 정합. |

**부호 FAIL 유무: 8항 전건 PASS (REVIEW1 항목6 FAIL → 해소).**
**단, 식 수준 신규 부호 결함 1건(NEW-HIGH-1 eq:arrhenius)** — 8항 체크리스트(평형·꼬리 사슬) 밖의 S4 회귀식이라 항목 판정엔 안 잡히나 별도 HIGH 결함으로 계상.

---

## 반환 요약
- 8항 체크리스트 전건 PASS, eq:arrhenius 1건 식-부호 회귀(체리픽 전 정정 권장).
