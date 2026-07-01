# FABLE 재검 C-5 — 이전 세션 핵심 판정의 재판정 (판정의 판정)

> 감사 sub. 파일 수정 없음. 재검 방식 = 물리 독립 재유도(현행 v1.0.11 tex 직접 정독) + 코드 직접 실행
> (`docs/v1.0.11/Anode_Fit_v1.0.11.py`, numpy 2.4.3·scipy 1.17.1, 원본 무수정 importlib 로드) + 4-tier.
> refute 양방향·빈통과 금지. **뒤집기 위한 뒤집기 금지 — 각 반전/수정은 재검 근거 필수.**
> 대상 원판정: `results/process/V1010_INSPECT_verify10.md`(§③) · `docs/v1.0.10/V1010_HANDOVER_INTEGRITY_REPORT.md`(§2·§4) · `results/process/V1010_LCO_STYLE_REPORT.md`.
> 원 검수자 주장 원문: `results/process/V1010_INSPECT_draft_S3.md`(S3-01~08) · `V1010_INSPECT_draft_S2.md`(I-02) · `V1010_INSPECT_UNION.md`(클러스터 C).

---

## 판정 1 — "논리점핑 6건 = 오적발" (verify10 §③) → **[유지]** (6/6 FP 확정, 미세 caveat 2)

각 항을 현행 `docs/v1.0.11/graphite_ica_ch1_v1.0.11.tex`(+ ch2)에서 직접 정독·재유도. 절 라벨 줄번호가 v1.0.10 원판정과
거의 일치(center 470·hys 515·width 710·broadening 1218·tail 1564·lag 1394) → 현행 tex 가 재검 대상 절을 원형에 가깝게 보존.

| 항목 (원 주장) | 현행 tex 근거 | 재판정 |
|---|---|---|
| **C1** = S3-02: `peak_shape=(ξ_eq−ξ_lag)/L_V→dξ/dV` 극한 비약(Taylor/커널 극한 미제시) | L1564-1593: (a)(b)(c)(d) 출발=보존식 `dQ/dV=C_bg+ΣQ_j dξ_j/dV`, ξ_j=ξ_eq−r_j. **0/0 극한 명시(L1577-79)**: L_V→0 이면 ρ→0, ξ_lag→ξ_eq 라 분자·분모 동시 소멸=0/0 → 매끈 환원 아님, 이산 분기 스위치(eq:branch)가 담당. | **유지** (FP). 비약 아님 — 0/0 을 명시 처리. △caveat: "매끈한 미분 **dξ_eq/dV** 로 수렴" 문구는 엄밀히는 dξ_lag/dV(1차 저역통과 미분)라 미세 표현 헐거움(점핑 아님, LOW). |
| **C2** = S3-03: Maxwell 등면적 적분 없이 artanh 결과만 | L584-623: 유도는 **Maxwell 등면적 아님** — 두 spinodal 극값 전위차. ξ_s±=½(1±u)를 eq:Veq 에 대입(eq:hyssub)→극대−극소(eq:hysdiff)→artanh 은 두 로그 결합 `ln[(1−u)/(1+u)]−ln[(1+u)/(1−u)]=−4 artanh u`(L612-613)에서 **명시 등장**. (a)(b)(c)(d) 완결. | **유지** (FP). 검수자가 유도법(Maxwell)을 오인 → 실제는 spinodal 상한, 완전 유도. |
| **C3** = S3-01: 두-상 w 이중지위 "선언만", N4 인과 없음 | L716-743: 전용 소절 "★폭 w_j 의 이중지위 — 같은 식, 다른 지위". 단상(Ω≤2RT)=검증가능 평형 예측 / 두-상(Ω>2RT)=평형은 델타 예측이라 같은 w 가 broadening 현상학적 자유 피팅 폭. 지위는 코드 분기 아닌 Ω_j 값이 가름 + §broadening(a) 위임. 삽입점에서 선언+정당화 존재. | **유지** (FP). 검수자가 "차단 절 없음"이라 했으나 그 절이 바로 L728-743. |
| **C5** = S2 I-02: Ch2 ∂V/∂T|_ξ 체인룰 "셋째 항" `(RT/F)∂ln[ξ/(1−ξ)]/∂T` 소거 사유 미제시 | ch2 L232-244 eq:dVdT_config: `∂V/∂T|_ξ=ΔS/F+(R/F)ln[ξ/(1−ξ)]`. **고정 ξ 편미분 표기 |_ξ** + 주석 "w=RT/F 의 명시적 T 의존이 둘째 항을 낳음" → 셋째 항은 ξ 고정이라 항등적 0(결과에 부재). | **유지** (FP). △caveat: verify10 "검수자 지어냄"은 다소 과함 — 체인룰 항 자체는 형식상 존재하나 |_ξ 정의상 항등 소멸. 실질=LOW 교육적 nicety, HIGH 점핑 아님(검수자 오등급). |
| **S3-07**: detailed-balance→logistic 의 μ-정의 삽입 점프, Ch1(동역학)↔Ch2(통계) 동등성 미연결 | L748 구동력 A_j=sF(V_n−U_j)(Bazant 인용) · **eq:eqcond(L434-436) μ=μ⁰−sF(V−U) 정의** · **sec:dist(L858-904)** 이 (i)kinetic·(ii)thermo 두 경로를 grand-canonical 점유 분포 한 언어로 명시 통합(L881 이 eq:eqcond 을 단일자리에 적용). | **유지** (FP). 검수자가 sec:dist 를 통째 놓침 — μ-link·동등성 모두 명시 존재. |
| **z_cut=4.357** = S3-08: 4.357 재현 불가, 독립계산 4.394 | 독립 재유도: ξ(1−ξ)=0.05×0.25=0.0125 → ξ=(1−√0.95)/2=0.0126603 → z=ln[(1−ξ)/ξ]=**4.3565**. 코드 실행: 검수자 4.394 는 f′=0.01206=peak 의 4.82%(5% 아님). tex L1429·1434 의 4.357 정확. | **유지** (FP). S3 산술 오류 확정 — 4.357 이 정합. |

**판정1 종합 = [유지].** 6/6 오적발 확정. **진짜 유도 비약 0건** — verify10 §③ 판정 옳음. 발견한 것은 caveat 2건(C1 문구 헐거움·C5 "지어냄" 표현 과장)뿐, 둘 다 FP 등급을 뒤집지 못하는 LOW 표현 문제. [확정]

---

## 판정 2 — "bell=의도 물리·R1 철회" (HANDOVER §2) → **[유지]** (재현 성공, 잔여 1)

코드 실행(n 스윕, `GRAPHITE_STAGING_LIT` equilibrium@298.15):

```
 n=1.0  w=25.69mV  #peaks=1  peakV=[0.10]               ← 단일 bell (기본값)
 n=0.5  w=12.85mV  #peaks=2
 n=0.2  w= 5.14mV  #peaks=3
 n=0.1  w= 2.57mV  #peaks=4  peakV=[0.085,0.12,0.14,0.211]  ← 4 near-delta 완전분리
 단일전이 FWHM: Ω=0/6000/13000/50000 전부 90.55mV (폭이 Ω 완전 무시)
```

- HANDOVER §2 핵심 주장("단일 bell 은 기본값 n=1.0 의 결과이지 구조적 무능이 아님 · n=0.1(w=2.57mV)→4 staging 완전분리")**정확히 재현**(peakV 까지 일치). → **R1 "폭 모델 구조결함(near-delta 생성 불가)" 철회는 타당** [확정]. 현행 tex 도 이 입장을 채택(L732-733 두-상=델타 예측, w=현상학적 자유 피팅 폭 "near-delta 낼 의무 없음"; L716-743 이중지위).
- **refute 반대편(잔여)**: 다만 verify10 §①(cluster A CRIT)이 지적한 실체 — **기본값 n=1 로 네 개의 진짜 두-상 전이가 단일 bell 로 병합되는 것은 비물리적 초기값/release 그래프 표시 문제**로 살아 있다(LiC6·LiC12 plateau 를 n=1 로 두는 건 fit 前 placeholder). 두 원판정의 실제 충돌은 "구조결함이냐"(verify10) vs "자유 피팅폭이냐"(handover)의 **해석 차이**이지 실측 차이가 아니며, 물리 재설계 불요라는 handover 결론이 옳다. cluster A 의 유효 핵은 "default/label" minor 로 강등되어 잔존(양 문서의 minor 항과 정합). → 반전 아님, **유지 + 잔여 1(default n=1 비물리 초기값=문서 라벨 사안)** [확정].

---

## 판정 3 — "면적 보존 정상(0.936=grid artifact)" → **[유지]** (실측 정확 재현)

코드 실행(equilibrium `∫dqdv dV` vs ΣQ=0.97):

```
 narrow [0.03,0.34] : area=0.908219  ratio=0.936308   ← 인용 0.936 정확 재현
 wide   [-0.5,1.0]  : area=0.970000  ratio=1.000000
 wide   [-1,2]      : area=0.970000  ratio=1.000000
 단일 Q=0.5 wide    : area=0.50000000 ratio=1.00000000
```

- 0.936 = narrow window 가 logistic 꼬리를 절단한 **grid/window artifact** 확정. wide window 에서 ∫dqdv dV=ΣQ **정확 보존**(peak_shape=Q·dξ/dV 라 −∞→∞ 적분=Q, 해석적으로도 자명). verify10 §③[FP]G1·handover §4 **옳음**. → **[유지]** [확정]. (인용 "0.979"는 단일전이/타 window 변형으로 추정 — 기제 동일, 미검증이나 wide=1.0 확인으로 무의미.)

---

## 판정 4 — "전자엔트로피 −45.68=Ch1 −46 정합"·"q_rev T 한 번" → **[유지]** (실측 정확 재현)

```
 func_dSe_molar(x=0.5, T=298.15, g=13, x_MIT=0.5, dx=0.05) = -45.6783 J/mol/K   ← verify10 "-45.678" 정확 일치
 (T=298 docstring 값: -45.6553 ≈ -45.7)      Ch1 gate -46 과 2-sig rounding 내 정합
 q_rev/(-I·dUdT) : min=max=298.150000        ← T 한 번(=298.15) 정확
 q(2T)/q(T) = 2.0000                          ← T 선형 = T¹ 확정(T² 아님)
 seam: electronic tr dS_eff = -4 + (-45.6783) = -49.6783   ← 전자항 seam 주입 일관
```

- 전자엔트로피 골 −45.678 재현(코드 라인 185 Sommerfeld·π²/3·÷e_V·R·kB 단위 3중 가드 정확). Ch1 −46 과 정합. [확정]
- q_rev(code L588 `−I·T·entropy_coefficient`)에서 T **정확히 한 번**(entropy_coefficient 가 이미 [V/K]) → q/(−I·dUdT)=298.15, 2T→2× 선형. verify10 [PASS] **옳음**. → **[유지]** [확정].

---

## 판정 5 — "LCO 산문 6절" (LCO_STYLE_REPORT) → **[유지]** (표본 재확인: 과적발·누락 0)

현행 tex 표본 정독(플래그 절 3 + 정상 절 대조):

- **sec:lco-center**(L470-513, 원등급 HIGH×2): U_j 전극무관을 eq:eqcond 참조로 **단정**(L471-475), ∂U/∂T=ΔS/F 를 "(식 T 미분, 전극 불문)" 괄호 전보체(L477-482)로 처리. 산문 재적용 맞음 → **식별 정확**. △단 eq:lco-dUdT + 정량 verifybox(dφ/dT≈+0.83mV/K→ΔS≈+80, 부호 공존 검산) 보유 → HIGH×2 **severity 다소 공격적**(순 산문 아님).
- **sec:lco-peak**(L1204-1216, 원등급 Major·최약): eq:eqpeak 전극무관 적용 + 위치/순높이/면적 **산문 인라인**, T1/T2/T3 위치 줄글 열거, **LCO 3전이 합산 peak 박스식 부재**. → 최약 판정 **정확**(과적발 아님).
- **sec:lco-hys**(L684-707, 원등급 HIGH×3): "같은 정규용액 틀 그대로 적용"을 order-disorder·MIT·도핑 **3회** 서술, eq:gxi/spinodal/dUhys/Ubranch **참조만** 하고 LCO Ω_j 대입 중간식·gap 수치 **전무**(0.47/1.49 J/K·mol 은 인용만). → 식별 **정확**.
- **정상 절 대조**: sec:lco-Se(953, Fermi-Dirac→Sommerfeld 완전유도)·sec:lco-gate(1068, 모델가정 정직선언)·sec:lco-map(295, 도입절)의 "정상" 분류 **타당**(신규물리 유도는 수식-주도). 모든 LCO 하위절이 6-flag/3-clear 로 커버 → **누락(under-detection) 0**.

**판정5 종합 = [유지].** 6절 식별에 과적발·누락 없음 — 6개 모두 진짜 산문 재적용(흑연 forward (a)→(d) 밀도 미달), 정상 3개 정당. 다만 이는 **G-derive 문체/교육 기준**이지 물리 오류가 아님(보고서 §4 도 "물리·결과식·부호 불변, 전개형식만" 명시). severity 라벨(HIGH)은 방어가능하나 다소 공격적. [확정 — 식별/ 추정 — severity 캘리브레이션]

---

## 종합 (5줄)

1. **판정 1(논리점핑 6건=오적발) → [유지].** C1·C2·C3·C5·S3-07·z_cut 6/6 을 현행 tex 독립 재유도로 FP 확정 — 진짜 유도 비약 0건. z_cut=4.357 은 ξ(1−ξ)=0.0125 → z=4.3565 로 재계산 일치(검수자 4.394 는 4.82% 산술오류). caveat 2건(C1 "dξ_eq/dV" 문구 헐거움·C5 "지어냄" 표현 과장)은 LOW, FP 불변.
2. **판정 2(bell·R1 철회) → [유지].** n 스윕 실측 재현(n=1→단일 bell, n=0.1/w=2.57mV→4 near-delta 완전분리, peakV 일치) — 구조결함 아님, R1 철회 타당. 잔여 1: 기본 n=1 이 두-상 전이엔 비물리 초기값(=default/label minor).
3. **판정 3(면적보존) → [유지].** narrow ratio=0.9363(인용 0.936 정확)·wide=1.000000·단일=1.0 — 0.936 은 grid 절단 artifact 확정.
4. **판정 4(−45.68·q_rev T¹) → [유지].** dSe=−45.678 정확 일치·q/(−I·dUdT)=298.15·2T→2× 선형 = T 한 번 확정.
5. **판정 5(LCO 산문 6절) → [유지].** 표본 재확인 과적발·누락 0(center/peak/hys 진짜 산문 재적용, Se/gate/map 정상 정당) — 단 문체(G-derive) 기준이지 물리오류 아니며 severity 라벨은 다소 공격적. **전 판정 반전 0·수정 0(유지 5/5)·미세 caveat 4건**(전부 원판정 결론 불변).
