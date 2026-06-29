# REVIEW1 — v8-08 (Codex) 적대 검수

검수자: 검수 sub (리뷰 전용, 수정·커밋 없음). 대상 = `v8-08.tex` 전문 1181행 정독.
기준 = v11_final.py·v11_flowchart.md·AUTHOR_BRIEF_v8.md·KNOWN_DEFECTS.md(전수).

---

## 1. 확정 결함 (refute mandate — 빈 통과 금지)

### ★C1 [CRITICAL] D-PEAK 미수정 잔존 (수학적 오류·v7-11 상속·최우선)
- **위치**: L904. "$L_V$ 가 작으면 $\xi_\mathrm{lag}\to$ 한 칸 뒤처진 $\xi_\eq$ 라, 식~\eqref{eq:peakshape} 가 이산 미분 $\to\dd\xi_\eq/\dd V$ 의 종으로 환원된다 — 곧 평형 peak 식~\eqref{eq:eqpeak} 로 돌아간다."
- **L896 derivebox** 도 동일 오류: "$L_V\to0$ 에서는 저역통과가 한 격자 뒤의 평형 목표가 되어 이 식이 logistic 미분 종으로 환원된다."
- **왜 틀렸나**: $\rho=e^{-\Delta_{grid}/L_V}$. $L_V\to0\Rightarrow\rho\to0\Rightarrow\xi_{lag}\to\xi_{eq}$(같은 칸)$\Rightarrow$ peak$\to0$ (종 아님). $r/L_V\to d\xi_{eq}/dV$ 환원은 **반대 극한 $L_V\gg\Delta_{grid}$**($\rho\to1$, quasi-steady)에서만 성립. 작은 $L_V$ 평형 회복은 **eq:branch 스위치**(L909, $L_V<\nu\Delta_{grid}$)가 담당하는 *불연속* 분기지 매끈한 극한이 아님.
- KNOWN_DEFECTS §★D-PEAK 수정 지시(연속 정당화는 $L_V\gtrsim\Delta_{grid}$서, 작은 $L_V$는 eq:branch 스위치로 명시)를 **v8-08은 반영하지 못함** — 9종 공유 최우선 결함을 그대로 계승. 부호장(S부) 통과 자랑과 별개로 본 결함은 G-derive 1급 실패.

### C2 [HIGH] D-VEQ — eq:Veq 의 다리($sF(V_{eq}-U)=g'(\xi)$)가 §6 detailed balance로 forward-defer(순환)
- **위치**: L412/L433. 히스 절(§3)에서 평형 전위 곡선 $V_{eq,j}(\xi)=U_j+\frac{RT}{sF}\ln\frac{\xi}{1-\xi}+\frac{\Omega}{sF}(1-2\xi)$ 를 **유도 없이 결과로 투입**. 이 식의 $\ln$ 몫은 §5 logistic(L562~) detailed balance 결과를, $\Omega(1-2\xi)$ 몫은 정규용액 화학퍼텐셜을 전제하나, 그 다리(stationary $RT\ln[\xi/(1-\xi)]=\mathcal A=sF(V-U)$ + $\Omega$ 합류)를 §3에 inline 1줄로도 안 깔고 뒤 절에 의존. KNOWN_DEFECTS D-VEQ 지시(앞당기거나 inline 1줄) 미반영.

### C3 [MEDIUM] D-WEFF — eq:weff(L554) 중심기울기 다리 누락
- $w^\eff=(RT/F)(1-\Omega/2RT)$ 를 결과로만 제시. 중간식 $sF\,dV/d\xi|_{1/2}=4Fw$(이상 $4RT$↔일반 $4Fw^\eff$)가 없어 어디서 $\Omega/2RT$ 항이 나오는지 유도 박스가 없음. brief §3의 "결과식 위 출발→연산→중간식≥1" 의무 미충족(이 식만 derivebox 부재).

### C4 [LOW] D-UBR — eq:Ubranch(L470) ansatz 성격 부분 보완되었으나 $\gamma$ 보간이 "유도"로 위장
- L467 derivebox 가 "$\gamma_j$·$h_\eta$ 를 곱한다"를 현상학적 축소로 *명시*한 점은 KNOWN_DEFECTS D-UBR 지시("현상학적 매개변수화로 명시")를 **부분 충족**. 다만 derivebox 제목이 "분기 중심 유도 사슬"이라 $\gamma$ 도입이 유도의 일부처럼 읽힘 — "spinodal 상한 ±½ΔU_hys까지가 유도, $\gamma h_\eta$는 현상학적 보정"으로 라벨 분리 권장. (경미)

### C5 [LOW] fig 내부 식번호·중복 — KNOWN_DEFECTS fig:overshoot 항 점검 결과
- v8-08은 fig:hysloop(L492~)로 통합, 별도 fig:overshoot 없음 → 식번호 오기·라벨 뒤바뀜 결함은 **해소**. fig:hysloop 캡션 \ref(eq:dUhys,eq:Ubranch) 정상. 단 eq:eyring 인용 누락은 잔존(L1174 eyring1935 정의되었으나 본문 \cite 0회 — bazant2013·dreyer2010도 동일 미인용, LOW).

---

## 2. KNOWN_DEFECTS 보유표 (전수)

| 결함 | 지시 | v8-08 상태 |
|---|---|---|
| ★D-PEAK | 작은 $L_V$ 종환원 삭제→eq:branch 스위치 명시 | **미수정(보유)** L896·L904 |
| D-VEQ | eq:Veq 다리 앞당김/inline | **미수정(보유)** L412·L433 |
| D-DHEFF | $\chi_d$ 계수 점프 중간식 | **수정** L766~770 중간식 $\Delta G_a-\chi_d\sigma_dF(V-U)+\chi_d\Omega(1-2\xi)$ 명시 |
| D-WEFF | $4Fw$ 중심기울기 다리 | **미수정(보유)** L554 derivebox 없음 |
| D-UBR | ansatz→현상학 명시 | **부분수정** L467(라벨 모호) |
| D-VN | 이항 중간식(자명) | 수정 L293~ derivebox |
| fig:overshoot | 식번호·라벨·중복 | 해소(통합) |
| 인용(eyring/bazant/dreyer) | LOW | 보유(미인용) |

---

## 3. 강점 3 / 약점 3

**강점**: (1) 부호 8항(S1~S8)+수치 회귀(R1~R4) self-test 절이 v11 1:1·falsifiable — 부호 클래스는 탄탄. (2) D-DHEFF·$L_q$ 4항 로그·$L_V$ 환산·인과 합성곱(적분인자→이산화) 유도는 단계적·G-follow 양호. (3) 코드 식별자·결과 박스·절 순서·표 v7-11/v11 배치 보존 완전(eq:vn~eq:sum 식별자 1:1, nodemap 정합).

**약점**: (1) ★최우선 D-PEAK 미수정 — 9종 공유 치명 결함 계승(연속/이산 극한 혼동). (2) D-VEQ·D-WEFF 두 유도 박스 부재로 G-derive 의무 부분 미달(Codex 유도 깊이 약점 노출). (3) eq:Veq를 §3서 결과 투입 후 §5/§6서 뒷받침 — 읽는 순서 순환(forward-reference 의존, G-follow 저해).

---

## 4. 차원 점수 (합/35)

| 차원 | 점수/5 | 근거 |
|---|---|---|
| ①G-derive(유도 완결성) | 2 | D-PEAK 오류+D-VEQ·D-WEFF 박스 부재 |
| ②배치 보존 | 5 | 절순서·박스·표·식별자 v7-11/v11 완전 보존 |
| ③부호 8항 v11 1:1 | 5 | S1~S8+R1~R4 전건 코드 대조 정합 |
| ④G-follow·G-usable·완결성 | 4 | 6단계 재현 keybox·nodemap 우수, eq:Veq 순환만 감점 |
| ⑤그림(6개·ASCII·\ref) | 4 | spine/derivechain/staging/hysloop/logistic/reversal 6개·내부 영어ASCII·\ref orphan0. fig:derivechain "charge balance" 라벨이 평형peak(N6)인지 모호(혼란 경미) |
| 형식·빌드 자족 | 4 | preamble 자족·전보체 회피 양호(빌드 미실행은 미검증) |
| 직전수정 새결함 | 3 | D-DHEFF 수정은 양호하나 D-PEAK 방치가 동급 결함 |

**합 = 27/35**

---

## 5. 부호 8항 v11 1:1 (★)
S1 $U_j=(-\Delta H+T\Delta S)/F$,$\Delta G=-FU$ ✓(func_U_j L69) · S2 $\xi_\eq=$logistic$[\sigma_d(V-U)/w]$ ✓(func_ksi_eq L86) · S3 $d\xi/dV$ peak 양수·방향불변 ✓(L468) · S4 $\Delta U_\hys\ge0$,$\Omega\le2RT\to0$,$\pm½\sigma_d$ ✓(func_dU_hys/U_branch L130·138) · S5 $\chi_d$ 충전 $1-\chi$,$\Delta H_a^\eff=\Delta H_a-\chi_d\Omega$ ✓(func_chi_d L160·func_dH_a_eff L152) · S6 $\partial\ln L_q/\partial V$ 컷상수라 운영0·부등식은 동기 ✓(L833~·코드 L335 동결) · S7 충전 격자역전 $\xi[::-1]\cdots[::-1]$·충전 거울 양수 ✓(L477) · S8 $V_n=V_\app-\sigma_d|I|R_n$ 방전 측정>내부 ✓(L412, flowchart L88 2026-06-29 정정과 일치). **부호 결함 0 — 확정.**
