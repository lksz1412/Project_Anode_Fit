# FABLE_AUDIT note A3 — Ch1 이력 감사: v7 → v8(유도 확장) → v9(LCO 통합)

> 역할: Fable 재검 분석 sub A3. 담당 = Ch1 전환 v7→v8→v9. **파일 수정 없음(분석 노트 1개만).** 모든 판정은 줄 근거(4-tier: 확정/근거미발견/추정/미검증). 추정 금지.
> 정독 완료: `v7-11.tex`(894줄 전문)·`v8-11.tex`(1209줄 전문)·`graphite_ica_ch1_v9.tex`(1544줄 — 흑연부는 v8-11과 byte-동일 확인 후 신규 LCO 절 전문 정독) + v8 기록 7종 + v9 기록 13종 + v4/v5 archived 소스 grep(제거 물리 규모 산정).
> 작성: 2026-07-02.

---

## 0. 계보 한눈에 (분량·구조 규모)

| 판본 | 파일 | 줄수 | 절 구조 | 성격 |
|---|---|---:|---|---|
| v4 (Opus) | `old/_archive/graphite_ica_ch1_Opus_v4.tex` | ~2771 | §1.1–§1.18(적층 포함) | 통계역학 풀 유도 + 분포/broadening/mosaic/Marcus/적층/master 알고리즘 |
| v5 (Opus) | `old/_archive/graphite_ica_ch1_Opus_v5.tex` | 1883 | §1.1–§1.17 (§1.18 적층 제외, 헤더 L7) | v4 − 적층. 분포/KWW/lever·chord/mosaic 유지 |
| **v7-11** | `results/builds/v7/v7-11/v7-11.tex` | 894 | 서론+N0–N9(9절)+부호검산 | **코드 진행 수식-구동**(결과 박스 9식·그림 5·표 3). 중간 유도 압축 |
| **v8-11** | `old/Ch1_v8/v8-11.tex` | 1209 | v7-11 + (a)→(d) 유도 4단 | **유도 확장판**(그림 +4=9·G-derive). 배치·결과·부호 v7-11 보존 |
| **v9** | `old/Ch1_v9/graphite_ica_ch1_v9.tex` | 1544 | v8-11 흑연 byte-동일 + LCO 신규 절 | **흑연 음극 + LCO 양극 통합**(전자 엔트로피 항·분포 프레이밍·코드 일반화) |

핵심 서사: **v5(풀 물리) → v7(코드 진행으로 재편·물리 대폭 절삭) → v8(v7 배치 위에 유도만 복원) → v9(같은 forward 틀을 LCO로 확장).** v7 단계에서 일어난 물리 절삭이 v8·v9에 그대로 상속되며, 그것이 아래 §3-(4)·§4-(4)의 "후퇴" 실체다.

---

## 1. 전환 v7 → v8 (유도 확장판)

### (1) 이전 문제 — v7의 유도 압축 "대입하면 닫힌다"

**확정.** v7-11은 결과 박스는 옳으나 박스로 가는 중간 유도를 한 줄로 점프한다. 대표 사례(v7-11 줄 근거):

- **logistic ξ_eq**: v7-11 L457–458 — "detailed balance 로부터, 구동력 𝒜_j=sF(V_n−U_j)를 넣고 진행률에 대해 풀면 평형 등온선이 logistic 으로 닫힌다." → detailed balance 유도 자체(r⁺/r⁻ 비·χ 상쇄)를 생략하고 결과만 제시.
- **완화속도 k_j**: v7-11 L546 — "k_j=k⁺+k⁻=k⁺(1+e^{−𝒜/RT})" 를 괄호 detailed balance 각주 한 줄로 처리.
- **유효장벽 ΔH_a^eff**: v7-11 L572 — "역방향 장벽의 상수 몫이 같은 +Ω 로 흡수되는 것을 반영" (χ_d 계수가 어디서 오는지 중간식 없음).

**확정(사용자 트리거).** v8 plan L10·AUTHOR_BRIEF_v8 L12: 사용자 피드백(2026-06-29) = "식 배치·간결화는 잘됐다. 그러나 *유도 과정까지 있는 교과서적 문건*을 원했는데 중간 도출을 완전히 날렸다." 배포 목적 = 회사 동료 교육 + 신규 접근 근거 → 유도가 닫혀야 교과서(brief L13 "학부생이 손으로 따라갈 수 있어야").

### (2) 개선 의도 — G-derive 복원

**확정.** v8 = "v7-11(배치·결과 박스·그림 보존) + v5(생략된 유도 원천) → 결과 박스 사이를 메운 교과서판"(plan L4·L6). 방법:

- 각 결과 박스 위에 **(a) 출발식/전제 → (b) 적용 연산 → (c) 중간식 ≥1 → (d) 박스** 4단(AUTHOR_BRIEF_v8 §3, L23). "대입하면/넣으면/정리하면 [박스]" 한 줄 점프 금지.
- 유도 원천 = `graphite_ica_ch1_Opus_v5.tex`(통계역학 전 유도). 11식 유도 사슬 사양이 plan L124–134·brief L26–36에 명세.
- 신규 그림 4개(활성화 장벽 `fig:barrier`·플럭스 교차 `fig:flux`·이중웰 `fig:doublewell`·완화 ODE `fig:relaxode`)로 유도 단계 시각화.
- 방법 = 9+9+1+1 competition-cherrypick(9 독립 → 검토1 → 방향성-만 보완9 → 검토2 → Opus 체리픽 v8-10(v6 합류) → adversarial 재검수 → v8-11 + 정식 10회).

### (3) 달성 여부 — G-derive 닫힘 + KNOWN_DEFECTS 6종 전부 정정

**확정(달성).** v8-11에서 11식 유도 4단이 실제로 구현됨(v8-11 줄 근거):

- eq:Uj: G≡H−TS(L331)→μ≡∂G/∂n(L336)→전기화학 평형 eq:eqbalance(L344)→ΔG=−sFU eq:eqcond(L351)→대입 eq:Ujmid(L363)→박스 eq:Uj(L370). v7-11의 "전자 항이 −FV로 들어오므로" 압축 완전 해소.
- eq:xieq(logistic): Eyring(L588)→비대칭 장벽 r± eq:bv(L592)→비 취해 detailed balance eq:db(L599, χ 상쇄 명시)→정지점 logit eq:logisticsolve(L608)→박스(L616). ★유도 원천이 여기 복원됨.
- eq:dUhys: ḡ(θ) Stirling(L403)→μ eq:mu(L408)→g(ξ) eq:gxi(L414)→g″ eq:gpp(L421)→spinodal 근의공식 eq:spinodal(L427)→V_eq 비단조 eq:Veq(L464)→spinodal 대입 eq:hyssub(L473)→극대−극소 차 eq:hysdiff(L481)→artanh 박스 eq:dUhys(L491). "가장 긴 유도인데 한 칸도 안 빠짐"(ROUND_usable L19).

**★D-PEAK 극한 오류 — 발생·처리 이력(4-tier 분리 필요, 과제 명시 항목).**

- **확정.** v7-11 *최종본*은 이미 **정확**하다: v7-11 L641–646이 "(ξ_eq−ξ_lag)/L_V가 dξ_eq/dV 종으로 수렴하는 극한은 L_V≫Δ_grid(ρ→1); 반대로 L_V→0이면 ρ→0이라 ξ_lag→ξ_eq(같은 칸)이고 0/0이라 종으로 매끈히 환원되지 *않는다*"를 이미 서술. 곧 "D-PEAK 오류가 v8에서 *처음 생겼다*"는 것은 근거 미발견 — v7-11 final은 이미 옳았다.
- **확정.** `KNOWN_DEFECTS.md` L5–10은 D-PEAK을 "★최우선·v7-11 상속"으로 등재하고, v8-04(9종 중 1종)의 자체 G-derive 감사가 선적발했다고 기록. 해석(추정): 9 작가가 *v5(유도 원천)*를 함께 받았고 v5 계열이 순진한 "L_V 작으면 종 환원" 서술을 담을 수 있어, **재유도 과정에서 오류가 재유입될 위험**이 D-PEAK의 실체다. KNOWN_DEFECTS는 그 위험을 전 9종에 전파-추적한 가드다.
- **확정(진짜 v8 신규 심화 = D-PEAK2).** v8이 v7보다 더 나아간 부분은 D-PEAK2다: `KNOWN_DEFECTS.md` L24–30 + v8-11 L958–962 — 문턱 ν=2에서 꼬리분기 진폭 vs 평형 종 진폭(∝1/w)이 정확히 안 맞아 "매끈한 handoff가 아니라 이산 *모드 스위치*, 문턱서 작은 진폭 점프 가능"으로 **정직 기술**. v8-07b의 적대 자체검수가 심화 적발.
- **확정(경화).** v8-11은 v7-11의 부호 회귀 self-test를 R1–R4(4항)에서 **R1–R5(5항)로 증분**하고, R5(v8-11 L1187–1192)에 "두 ρ 극한 부호를 뒤집으면 깨지는" falsifiable 회귀 가드를 신설. ROUND_sign L41·ROUND_usable L79 확인.

**확정(KNOWN_DEFECTS 6종 전부 정정).** adversarial 재검수 REVIEW_A(SymPy/NumPy 직접 재검산)·REVIEW_B(PDF 렌더 판독) 결론:
- 부호 8/8 PASS(REVIEW_A §1, 코드 `Anode_Fit_v11_final.py` 1:1).
- 11식 G-derive 전부 통과(REVIEW_A §2).
- D-PEAK·D-PEAK2·D-WEFF·D-VEQ·D-DHEFF·D-UBR 6종 전부 해소·정확(REVIEW_A 결론 L112).
- CRITICAL/HIGH 물리·부호·유도 결함 0. 잔존 = LOW/NOTE 가독 3–5건(W1–W3, B1–B3)뿐, v8-11 폴리시 5 hunk로 흡수(ROUND_sign §A: 수식·박스·부호 라인 1바이트도 안 바뀜).

### (4) ★우수 구조 보존 — v3/v4/v5의 broadening/분포 물리 제거(후퇴)의 실체·규모

**확정(제거된 물리 — v4/v5 archived 소스 줄 근거).** v7이 "코드 진행"으로 재편하며 절삭한 물리 계열:

1. **입자·장벽 분포 broadening + KWW stretched-exponential(★핵심 "분포 물리").**
   - v5 L1057 §sec:tempbranch "온도 가지 — Arrhenius 와 입자 분포", v5 L1116 "입자 분포 — 같은 온도가 산포를 키운다": 장벽 밀도 ρ_G(G)·집단 평균 지연 ⟨r⟩·분포 일반형 eq:superpose(v5 L1160).
   - v4 L1648 stretched exponential `e^{−(x/L_KWW)^β}` — Kohlrausch–Williams–Watts, 인용 johnston2006(v5 L1875)·svare2000(v5 L1876). β(T) 온도 의존이 "고정 장벽 분포"의 **반증 가능 진단**(v4 L1654–1656).
   - broadening을 **유한 peak 폭의 기원**으로 명시: v5 L882 "실측의 유한 폭은 평형이 아니라 broadening(입자 분포·동역학) 기원"; v4 L1257·L2086–2088 동일.
2. **lever/chord/cotangent binodal 공통접선 2상**(v5 L669/676/682, v4 L924/932/939) — v7/v8/v9의 히스는 spinodal gap만.
3. **다입자 mosaic(Dreyer)**(v5 L1357/1406, v4 L1966/L2035) — v7/v8/v9는 dreyer2010을 히스 "구조적 분기" 선언에만 인용, mosaic 전선 물리는 제거.
4. **Marcus 2차 항(λ)**(v5 L253/L1048, v4 L295/L1506) — v7/v8/v9는 선형 χ 전달계수만.
5. **적층 준안정 §1.18**(v4 L2744 §sec:stacking, ψ order parameter) — 이미 v5 헤더 L7에서 제외.
6. **master 알고리즘 S0–S5 + 진단/반증 표**(v4 §sec:master L2223·§sec:falsify L2523).

**확정(규모).** 절 구조 ~17–18절/~2771줄(v4)·§1.1–1.17/1883줄(v5) → 9절/894줄(v7). **코드 진행 재편이 물리 콘텐츠의 대략 절반을 절삭.** v8은 이 절삭 위에 *유도만* 복원했을 뿐(그림 +4·G-derive) 절삭된 물리를 되살리지 않았다.

**확정(고의적·근거 있는 절삭).** v8 plan Non-goals L37·brief §4 L40이 이 재유입을 명시 금지: "곡선에 필요한 11식의 유도만. v5의 무관 일반론(lever/chord/cotangent 상평형 세부·적층·ch2+ 주제) 끌어오지 말 것 — 과확장 분노 전례(6-29 '너무 과한 확장이었다')." v8-06 헤더 L18–19도 "무관 일반론(lever/chord·Marcus·KWW·적층·master 알고리즘 S0-S5)은 결과 박스로 수렴하지 않으므로 재유입 안 함" 명문.

**후퇴의 물리적 실체(문제점).** v7/v8/v9는 peak 폭을 **평형 logistic w=nRT/F**(v8-11 eq:wbase L571)로, 꼬리를 **단일 L_V 지수 기억**(eq:peakshape)으로 닫는다. 그러나 v4/v5는 실측 ICA peak 폭이 *평형이 아니라 broadening(입자·장벽 분포) 지배*라고 명시했다(v5 L882). 곧:
- v7/v8/v9는 분포-broadening을 유효 n(폭) 또는 L_V(꼬리)에 흡수시켜 **평형 폭과 분포 broadening을 혼동**할 수 있다.
- KWW β(T)의 온도-의존 진단(고정 장벽 분포 반증)이 사라져 **다온도 피팅의 falsifiable 신호 하나를 잃음**.
- 이는 *교과서·재현 문건*으로선 정당한 스코프 축소이나, *피팅 물리*로선 실측 broadening의 미시 기원을 단일 파라미터에 뭉갠 손실이다.

### v7→v8 장점 / 단점 / 문제점

- **장점(확정):** ① G-derive 닫힘(11식 학부생 추적 가능, ROUND_usable "치명 비약 0"). ② 코드 1:1 유지(모든 기호=코드 식별자, 결과 박스·부호 v7-11 byte-보존, ROUND_usable §3). ③ KNOWN_DEFECTS 전파-추적 + R5 falsifiable 회귀 가드로 D-PEAK류 재유입 차단. ④ competition-cherrypick가 系統 결함(D-VEQ 순환·D-DHEFF χ_d 누락·D-WEFF ¼)을 단일 문건이면 놓쳤을 자리에서 적발.
- **단점(확정):** ① 분포/broadening/KWW/mosaic/Marcus 물리 부재가 v7에서 상속되어 v8도 그대로(§3-(4)). ② eq:weff 유도만 11식 중 유일하게 1줄 압축 잔존(ROUND_usable "가장 약한 1곳", v8-11 L577). ③ z_cut=4.357 닫힌 출처 없이 "선택값"(REVIEW_A 약점2·REVIEW_B B3).
- **문제점(추정):** peak 폭=평형 logistic이라는 프레이밍이, 실측 broadening을 흡수한 피팅에서 물리 오귀속을 유발할 수 있음(위 후퇴 실체). v8은 이를 "결과 박스 스코프"로 정당화했으나 문건 어디에도 "실측 폭은 broadening 지배"라는 v4/v5의 경고가 남아있지 않다 — **정직성 관점의 공백**.

---

## 2. 전환 v8 → v9 (LCO 양극 통합)

### (1) 이전 문제 — v8은 흑연 음극 전용(양극 부재)

**확정.** v9 plan L13·L6: Ch1 현재(v8-11)는 "유도 확장 교과서판, **흑연 음극 only**". 가역 발열은 전셀=양극−음극이라 양극(LCO) 정량이 선행돼야 함(사용자 지시). 또한 v8은 ξ_eq를 kinetic/thermo 두 경로로 유도하되 그 둘이 *하나의 분포*임을 명시하지 않아, LCO 전자(Fermi–Dirac) 엔트로피로 가는 다리가 없었다(plan L96 "1점 보강" 근거).

### (2) 개선 의도 — LCO 통합 + 전자 엔트로피 + 분포 프레이밍

**확정(v9 목표, plan L6·AUTHOR_BRIEF §목표):**
- v8-11 흑연 서술·식·부호·그림을 **byte-보존**하고, LCO 양극(코인 하프셀 vs Li)이 필요한 곳에만 절·식을 *추가*한 단일 통합본.
- ★**전자(electronic) 엔트로피 항**: LCO metal–insulator transition(MIT @x≈0.85)·order–disorder(@x≈0.5) → Sommerfeld S_e=(π²/3)k_B²T·g(E_F) → 부분몰 ΔS_e(x). Ch1 본문에 삽입(반응 엔트로피의 한 성분), Ch2(가역 발열)로 확장이 순서(plan L6).
- ★**ξ_eq 분포 프레이밍 1점 보강**: ξ_eq = 평형 점유 확률 분포(Z=1+e^{−βΔμ}, Fermi-함수형) — kinetic·thermo 두 경로를 *분포* 한 언어로 통합 + LCO 전자 Fermi–Dirac로 가는 다리(brief §추가 3).
- forward 코드 LCO 일반화(MSMR 동형)·도핑 보정.
- 방법 = 동일 competition-cherrypick 9종.

### (3) 달성 여부 — LCO 통합 완결 + 부호 규약 충돌의 경쟁 적발·정정

**확정(달성, v9 tex 줄 근거):**
- **흑연 byte-보존**: R4 §(a) 9종 verbatim PASS(핵심 literal 9종 대조), V1 §(b)·FIX_LIST A2 "흑연 byte-동일(diff 제거 0·헤더 4줄만 치환)". 필자 직접 확인: v9 N6–N9·tab:inputs·6단계 keybox(v9 L1525–1533)가 v8-11과 동일.
- **분포 프레이밍**: v9 §sec:dist(L814–856) 신설. 단일 자리 grand-canonical Z=1+e^{−βΔμ}(eq:partfn L825)→평균 점유 ⟨n⟩ Fermi-함수형(eq:fermifn L832)→logistic 일치(L840)→kinetic/thermo 통합(L844). keybox(L851): "ξ_eq = 평형 점유 확률 분포 … LCO 전자 Fermi–Dirac와 동형."
- **전자 엔트로피 절**: v9 §sec:lco-electronic(L885–1066). Fermi–Dirac f(E)(eq:fd L909)→Sommerfeld 적분 π²/3(L921)→C_e→S_e(eq:Se L928)→부분몰 ΔS_e(eq:dSe L947)→몰당 단위 다리 N_A(eq:dSemolar L956)→MIT-logistic 게이트(eq:ggate L984)→닫힌식 eq:dSegate(L997). ★세 등급 분리(함수형 tier A / anchor tier A / 연속곡선=갭 G2, L931–940).
- **코드 일반화(H)**: v9 §sec:lco-code(L1453–1478). MSMR eq:msmr(L1457) ↔ eq:xieq 동형(방향인자 f=−σ_d, L1462–1464), "구조 변경 0 + 파라미터 교체 + 전자항 plug-in 한 줄".

**★KNOWN_DEFECTS류 — v9에서 생긴 결함·정정 이력(경쟁이 적발한 것, 확정):**
1. **ΔS_e 부호 규약 충돌(HIGH 5건).** CHERRYPICK_PLAN L9·R2·V1 §(a): 유도 최고 초안 v9-04/06/01/08/09가 ΔS_e를 *제거-positive*(−∂S_e/∂x>0)로 삽입 슬롯에 역부호 주입(HIGH 5). v9-02/03만 정확. master가 base_v8-11 흑연 본문 3중 검산(반응식 L341 삽입 forward·인자 사전 L212 "삽입 반응"·round-trip ΔS=−16→U=0.0853V)으로 **삽입 기준 ΔS_e=∂S_e/∂x<0** 확정(R2 §a). v9 최종은 전 위치 통일(v9 eq:dSe L948·decomp L1442·verifybox L470 "전자항 ΔS_e<0, 총 부호 불변" 오독 방지). **경쟁+적대검수 없이 단일 문건이면 역부호로 출하됐을 자리.**
2. **인용 fabrication/오귀인(CRITICAL·HIGH).** CHERRYPICK L41·R5·V2: v9-03이 ml2024 저자 "R. Aronson" **생성(fabrication)**; v9-01/02/06/07/08/09가 +0.83 mV/K를 reynier2009/wang2009로 **6종 오귀인**(정답=Świderska-Mocek 2019); MSMR 구버전 3종. V2가 검증 8건 마스터 bibitem 구축(reimers1992·menetrier1999·motohashi2009·xia2007·reynier2004·swiderska2019·msmr2024·ml2024=Teichert et al.). A3 adversarial: v9-10 인용 8건 전부 V2 마스터와 1:1 정확, fabrication 0(A3 §1).
3. **w_eff 역수 오류(Ch2 트랙, 참고).** PHASE_2TRACK_RESULT §3: master 설계 doc가 w/(1−Ω/2RT) 역수 오류 → adversarial+v9-05 독립 삼중검증 적발·정정. (본 A3 담당인 Ch1 v9엔 직접 영향 없음, 방법 가치 근거로만.)

**확정(품질 게이트 통과).** PHASE_2TRACK_RESULT §4: Ch1 v9 = 흑연 byte-동일·ΔS_e 삽입<0 6앵커·인용 8건 검증(fabrication 0)·xelatex 0-err·30p. A3 adversarial: CRITICAL/HIGH 0, 잔존 = Overfull 22.6pt 1건(LOW) + 미인용 중간식/절 라벨(구조상 정상).

### (4) ★우수 구조 보존 — 분포 물리 "재등장"의 성격(후퇴 미회복)

**확정(중요 뉘앙스).** v9는 §sec:dist에서 "분포(distribution)" 언어를 되살린다 — 그러나 이는 v4/v5가 제거당한 **입자·장벽 분포 broadening(KWW)이 아니다.** v9의 분포는 *단일 자리 평형 점유 확률 분포*(Z=1+e^{−βΔμ}, Fermi-함수형, v9 L825·L841)로, 기존 logistic ξ_eq를 통계역학적으로 *재해석*한 것이며 LCO 전자 Fermi–Dirac로 가는 다리로 쓰인다. 곧:
- v4/v5의 **분포 물리 = 여러 입자/장벽에 걸친 ρ_G 적분(broadening·KWW 꼬리)** — peak 폭·꼬리 모양의 미시 기원.
- v9의 **분포 = 한 자리의 0/1 배타 점유 분포** — 이미 있던 평형 폭의 재프레이밍.
- **결론(확정):** §3-(4)의 후퇴(broadening/KWW/mosaic/Marcus)는 v9에서도 **회복되지 않았다.** "분포"라는 단어는 돌아왔으나 물리 계열이 다르다. v9는 오히려 *또 하나의 단일-자리 분포*(전자 준위 Fermi–Dirac)를 추가했을 뿐, 다입자 broadening은 여전히 부재.

### v8→v9 장점 / 단점 / 문제점

- **장점(확정):** ① 흑연 byte-보존 하 LCO 통합(단일 프레임, 부록 아님) — R4/V1 verbatim PASS. ② 전자 엔트로피 절이 Fermi–Dirac→Sommerfeld→부분몰→MIT 게이트로 완전 유도(tier 정직 3분리·갭 G2 명시). ③ 분포 프레이밍이 흑연 리튬-자리 점유 ↔ LCO 전자-준위 점유를 한 통계로 묶어 Ch2 확장 다리 확보. ④ 경쟁+adversarial이 ΔS_e 역부호 5건·인용 fabrication을 적발·정정(단일 문건이면 출하됐을 결함).
- **단점(확정):** ① 분포-broadening/KWW/mosaic 후퇴 미회복(§4). ② 연속 g(E_F,x)·ΔS(x)·도핑 shift·MSMR LCO 파라미터가 1차 문헌 부재(갭 G1–G5) → round-trip 피팅 위임(정직 표기했으나 문건 단독 정량 불가). ③ 전자항 크기 0.18 k_B/atom = config(>½ 지배)보다 작아 "게이트로만 필수"(v9 L1026–1031) — 실측 분리 신호가 ∝T 온도 의존 하나뿐(피팅 식별성 취약).
- **문제점(추정):** ① 9종 초안 중 5종이 ΔS_e 역부호를 주입한 사실은, forward 부호 규약(삽입 기준)이 유도자에게 직관적이지 않음을 보여줌 — v12에서 규약 문장을 더 전면화하지 않으면 재발 위험. ② 인용 fabrication이 여러 초안에서 반복(R. Aronson·+0.83 오귀인)된 것은 LLM 작가의 구조적 위험 — 체리픽 인용 마스터 대조가 필수 방어선임이 재확인.

---

## 3. v12 교훈 (담당 구간 종합)

1. **분포·broadening 물리의 선택적 복원 검토(최우선).** v7이 절삭한 입자·장벽 분포 broadening + KWW stretched-exponential(v4/v5 §sec:tempbranch·eq:superpose·johnston2006/svare2000)은 실측 ICA peak 폭·꼬리의 *미시 기원*이자 β(T) falsifiable 진단이었다. v8·v9는 이를 미회복. v12가 "피팅 물리"를 지향한다면, 최소한 **"실측 폭은 평형 logistic이 아니라 broadening 지배"라는 v4/v5의 경고 1–2문장**을 되살려 정직성 공백을 메우고, 선택적으로 ρ_G 분포 적분을 use-옵션(w_eff처럼)으로 노출하는 것이 정당. 무관 일반론(lever/chord·mosaic·Marcus·적층·master 알고리즘)까지 다 되살릴 필요는 없다(v8 스코프 판단 유지) — **broadening/KWW만 표적 복원.**

2. **KNOWN_DEFECTS 전파-추적 + falsifiable 회귀 self-test는 유지·강화.** D-PEAK(v7-11 final은 이미 옳았으나 재유도 재유입 위험)·D-PEAK2(문턱 진폭 불연속 정직 기술)·ΔS_e 역부호(v9 5건)가 모두 이 가드로 잡혔다. v12도 R-항(수치 못박은 회귀 테스트)을 계승하고, **부호 규약(삽입 기준)을 유도자 프롬프트 머리에 못박아** ΔS_e 류 역부호 재발을 차단.

3. **인용 fabrication은 구조적 위험 — 체리픽 인용 마스터 대조 필수.** v9에서 R. Aronson 생성·+0.83 6종 오귀인·MSMR 구버전이 다수 초안에 발생. v12 신규 인용은 반드시 추출카드/검증 DOI 마스터(V2형)와 대조 후 채택.

4. **G-derive 잔존 약점 마감.** eq:weff 1줄 압축(v8-11 L577, 11식 중 유일)·z_cut=4.357 닫힌 출처 부재는 v8·v9에 그대로 상속. v12에서 (b)(c) 중간식 1줄로 마감.

5. **byte-보존 + 델타-확장 패턴은 성공적.** v8(v7 배치 위 유도만)·v9(v8 흑연 위 LCO만)의 "불가침 base + 신규 델타" 방식이 회귀 0으로 검증됨(R4/V1/ROUND). v12(교수님 피드백·전셀)도 이 패턴 계승 권장.

---

### 근거 파일 색인 (절대경로)
- tex: `D:\Projects\Project_Anode_Fit\Claude\results\builds\v7\v7-11\v7-11.tex` · `...\Claude\old\Ch1_v8\v8-11.tex` · `...\Claude\old\Ch1_v9\graphite_ica_ch1_v9.tex`
- 제거 물리 소스: `...\Claude\old\_archive\graphite_ica_ch1_Opus_v4.tex`(L1057/1116/1648/924·2744) · `...\graphite_ica_ch1_Opus_v5.tex`(L7/882/1116/1160/1875-76)
- v8 기록: `...\Claude\plans\2026-06-29-ch1-v8-derivation-expanded-9x9x1x1-plan.md` · `...\Claude\results\builds\v8\v8-00_spine\{AUTHOR_BRIEF_v8,KNOWN_DEFECTS}.md` · `v8-10\REVIEW_A.md`·`REVIEW_B.md` · `v8-11\ROUND_{sign,usable,visual}.md`
- v9 기록: `...\Claude\plans\2026-06-30-ch1v9-LCO-ch2v4-mixing-2track-9x9x1x1-plan.md` · `...\Claude\results\process\PHASE_2TRACK_RESULT.md` · `...\Claude\results\builds\v9\v9-00_spine\{AUTHOR_BRIEF,CHERRYPICK_PLAN,FIX_LIST_v911,REVIEW_NOTES}.md` · `review1\{R1_electronic_entropy,R2_sign_convention,R4_preservation_build,R5_usable_citations}.md` · `review2\{A3_adversarial_build,V1_sign_regression,V2_citations_master}.md`
