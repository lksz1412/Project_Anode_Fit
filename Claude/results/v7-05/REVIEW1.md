# REVIEW1 — v7-05.tex 적대 검수 (검수 sub, 리뷰 전용)

대상: `Claude/results/v7-05/v7-05.tex` (752행, 전문 정독 1–752).
판정 기준: `v7-00_spine/Anode_Fit_v11_final.py` (707행) · `v11_flowchart.md` · `AUTHOR_BRIEF.md` (전문 정독).
방식: 렌즈별 적대 검수 + refute mandate + 가장 약한 1곳 강제 + 빈 통과 금지. 수치 주장은 직접 재계산.

---

## A. 확정 결함 {심각도 · 행 · 무엇이 틀렸나 · 옳은 형}

### HIGH-1 (consistency / G-follow) — 분극 부호의 *물리 서술*이 spine 과 정반대
- 행: 235, 240 (vs `v11_flowchart.md` L88).
- 틀림: 본 tex 는 "방전(σ_d=+1)은 분극이 측정 전위를 내부보다 **올린다**" → 방전 시 $V_\app>V_n$ (측정이 평형보다 **높게** 읽힘). 그러나 spine flowchart L88 은 "방전 시 관측 V 가 평형보다 **낮음** 보정"이라 적는다. 동일 식 $V_n=V_\app-\sigma_d|I|R_n$ 을 두 문서가 **정반대 물리**로 해설한다.
- 판정: 식 자체(eq:vn)는 코드 L412 `V_n = V_in - sigma_d*I_abs*self.Rn` 와 **1:1 일치**하므로 ★부호 8항의 FAIL 은 아니다(아래 §C-8 PASS). 그러나 학부생 G-follow 관점에서 두 통제문서가 충돌하므로 HIGH. 물리적으로 옳은 쪽: 방전(산화·탈리튬화)에서 IR drop 은 음극 측정 전위를 평형보다 **올린다**(과전압이 산화를 더 밀려면 더 높은 V 필요) — 즉 본 tex 의 서술이 통상 관례에 맞고 flowchart 가 거꾸로 쓰였을 개연. 그래도 **본 장 내부 통제문서와의 표면 모순**이 남으므로 결함으로 등재. 옳은 형: tex 가 옳다면 무해하나, 최소한 "spine 의 '낮음' 표현과의 차이"를 1줄 각주로 닫거나 flowchart 정정 권고.

### MEDIUM-1 (물리 rigor) — $\partial\ln L_q/\partial V_n$ 를 `=` 로 단정 (코너 케이스에서만 등호)
- 행: 560 (boundbox).
- 틀림: "$\partial\ln L_{q,j}/\partial V_n=-\chi_d\sigma_dF/RT$" 를 등호로 적음. 그러나 eq:lnLq(524)에는 $-\ln(1+e^{-A/RT})$ 항도 $V$ 의존이라 정확한 미분은 $\frac{\sigma_dF}{RT}\big[-\chi_d+\frac{e^{-A/RT}}{1+e^{-A/RT}}\big]$. 둘째 항을 누락.
- 완화: 컷에서 $A=z_\mathrm{cut}nRT\approx4.357RT$ 로 고정되어 $e^{-A/RT}\approx0.013$ 이라 무시 가능 — 부호 결론($\le0$)은 불변. 따라서 결함은 "등호의 과단정"뿐(부호 사슬 6번 결론 자체는 옳음). 옳은 형: `≈`(깊은 컷 근사) 표기 또는 둘째 항 명시 후 소거 사유.

### LOW-1 (G-usable 미세) — N3↔N6 절 순서가 코드 루프 순서와 어긋남(의도된 재배열, 그러나 독자 혼선 여지)
- 행: 절 배치 §N4–N6(310–419) → §N3(425–490).
- 사실: 코드 루프(L435–481)는 전이당 N2→**N3(center)**→N4–N5→N6→N7→N8 순. tex 는 "방전 본론 먼저"라며 N6 을 N3 앞에 둠. 위상 선언(307·427)과 환원식(669)으로 정합을 닫았고 flowchart 의 "절 순서 = 노드 순서" 권고에 대한 *명시적 예외 처리*가 되어 있어 결함 아님에 가깝다. 다만 brief §3 "순서는 고정"에 대한 일탈이라 LOW 로 기록(작가가 도입/마무리 다리로 정당화함 — 수용 가능).

---

## B. 강점 3 · 약점 3 (가장 약한 1 표시)

강점:
1. ★부호 8항 전부 코드 식별자와 1:1 (eq:vn/logistic/dxidV/hysdU/hyscenter/chid/dHeff/lnLq → L412/L86/L391형/L130/L138/L160/L152/L96). 수치 검산(z_cut 4.357→bell/0.25=0.05·xi=0.987, U(298)=0.0853, dU_hys(4RT)=54.8mV·2.13RT/F, 순높이 10.4) **전부 재계산 일치**.
2. G-usable 닫힘: 표 tab:staging 가 GRAPHITE_STAGING_LIT 와 1:1(U·dH_rxn·dS_rxn·Q·Omega·dH_a·dVdq_qa 전 8행), verifybox(692)가 생성→조건→N1→전이루프→N9 재현 절차를 식 참조까지 닫음. STAGING 정합 OK.
3. 완결성 orphan 0: fig:staging/logistic/branch/reversal/flow·tab:staging 전부 \ref 로 본문에서 사용, 그림 내부 라벨 영어 ASCII 전용(한글 0), 캡션만 한글. 절마다 도입·"넘김" 다리 존재.

약점:
1. **(가장 약한 1곳)** 분극 부호 *물리 서술*이 spine flowchart 와 정반대(HIGH-1). 식은 맞으나 두 통제문서 충돌이 미봉.
2. boundbox $\partial\ln L_q/\partial V$ 등호 과단정(MEDIUM-1).
3. N6-앞-N3 재배열이 brief "순서 고정"의 경계선(LOW-1, 정당화는 됨).

---

## C. ★부호 8항 — PASS/FAIL + 근거 (v11 대조)

1. $U_j=(-\Delta H+T\Delta S)/F$ — **PASS**. eq:Uj(297)=code L69. dH_rxn 전부 음수(발열), 서술 "발열 삽입"(303) 정확. ΔG=−FU(281) 일치.
2. $\xi_\eq=\mathrm{logistic}[\sigma_d(V_n-U)/w]$, 방전 V↑→ξ↑ — **PASS**. eq:logistic(332)=code L86–87(z=s(V_n−U)/w, np.where 안전형까지 서술 336). 부호검산(339) 옳음.
3. $d\xi/dV=\sigma_d\xi(1-\xi)/w$ → peak 양수 — **PASS**. eq:dxidV(391), $\sigma_d^2=1$ 소거(399) → 항상 양수(394).
4. $\Delta U_\hys\ge0$, $\Omega\le2RT\to0$, 분기중심 $\pm\tfrac12\sigma_d$ — **PASS**. eq:hysdU(450)=code func_dU_hys L130 + $\Omega\le2RT$ 명시분기. eq:hyscenter(460)=code L138 `U_j+0.5*sigma_d*h_eta*gamma*dU`. 방전 +/충전 − (463) 일치, $U_j^\dis-U_j^\chg=\gamma\Delta U^\hys>0$ 옳음.
5. $\chi_d$: 방전 χ/충전 1−χ, $\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ — **PASS**. eq:chid(541)=code func_chi_d L160(`chi if sigma_d>=0 else 1-chi`). eq:dHeff(546)=code func_dH_a_eff L152.
6. $\partial\ln L_q/\partial V<0$ — **PASS(결론)** / 단 등호 과단정(MEDIUM-1). 부호 ≤0 결론은 옳음(컷 $A$ 고정 시 둘째항 무시 가능).
7. 꼬리 충전 격자 역전, 충전=방전 거울(양수) — **PASS**. eq:reversal(600–603)=code L474–477(`_causal_lowpass(ksi[::-1],...)[::-1]`). min_lag 환원조건 $L_V<2g_\mathrm{step}$(595)=code L466 `min_lag_grid_steps*grid_step`(기본2.0). lowpass 식 eq:lowpass(583)=code L105·L109 계수 1:1.
8. $V_n=V_\app-\sigma_d|I|R_n$ — **PASS(식)**. eq:vn(237)=code L412. ※물리 *서술*은 spine 과 충돌(HIGH-1) — 식 부호 자체는 무결.

→ **부호 8항 FAIL = 0** (전 항 식·코드 1:1). 잔여는 서술 충돌(HIGH-1)·등호 과단정(MEDIUM-1)뿐.

---

## D. 차원 점수 (6×5 = /30)

| 차원 | 점수 | 근거 |
|---|---|---|
| 1. spine 정합(N0–N9 순서·노드 커버) | 5 | 9절이 N0–N9 전 노드 커버. N6↔N3 재배열은 명시 위상선언·환원식으로 정당화(brief 예외처리). |
| 2. ★부호 사슬(8항 적대검산) | 5 | 8항 전부 코드 1:1·수치 재계산 일치. FAIL 0. (HIGH-1 은 서술층 충돌이지 식 FAIL 아님 — 차원5 로 반영) |
| 3. G-follow(따라가짐) | 3 | 유도 사슬·다리 양호하나 분극 물리서술이 spine 과 정반대라 학부생이 교차참조 시 혼선(HIGH-1). |
| 4. G-usable(재현·STAGING) | 5 | tab:staging↔LIT 1:1, verifybox 재현 절차 식참조까지 닫힘, 전역기본값·컷·역보간 명시. |
| 5. 완결성(orphan·그림 규약) | 5 | \ref orphan 0, 그림 내부 영어 ASCII 전용, 캡션 한글, 신규 TikZ, 각 그림 앞식 동기·뒤 사용. |
| 6. 형식(수식주도·전보체·절 다리) | 4 | 수식주도·절 도입/넘김 다리 충실. boundbox 등호 과단정(MEDIUM-1) 1건으로 −1. |
| **합** | **27/30** | |

---

## E. 빌드/그림 메모 (비차단)
- PDF 미생성(빌드 미실행 — 본 검수는 리뷰 전용, 빌드는 작업 sub/master 영역). \ref·\label·\cite 키 정합은 소스 정독으로 확인(미정의 참조 0, thebibliography 13키 전부 본문 인용).
- 그림 5종(staging/logistic/branch/reversal/flow) + 표 2종(longtable 기호사전·tab:staging) 모두 본문 \ref 사용.

---

## 반환 요약 (10줄 이내)
- 합점수: **27/30**.
- CRIT 0, HIGH 1 (분극 부호 *물리 서술*이 spine flowchart 와 정반대 — 식 eq:vn 은 코드 1:1 무결, 서술층 충돌).
- MEDIUM 1 ($\partial\ln L_q/\partial V$ 등호 과단정, 컷 근사에선 무해), LOW 1 (N6-앞-N3 재배열, 정당화됨).
- ★부호 8항: **FAIL 0** — 8항 전부 v11 코드·수치(z_cut 4.357·U298 0.085·dU_hys 54.8mV·순높이 10.4) 재계산 일치.
- 가장 약한 1곳: **분극 부호 물리 서술(행 235·240) vs flowchart L88 모순** — 식은 맞으나 두 통제문서가 정반대 해설, 1줄 각주로 닫거나 flowchart 정정 권고.
