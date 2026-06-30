# Codex Chapter 1 V4 검수의견 (Claude 측 독립 적대 10-pass) — 2026-06-02

> **대상**: `Codex/results/graphite_ica_ch1_codex_candidate_v4.tex` (945줄, Codex 측 Chapter 1 최종본, SHA256 C1607A7E…C876517).
> **방법**: Codex 가 정의·수행한 10-pass 전문 검수(P1 section-level → P10 full sweep, varied chunk, 매 pass 전 945줄 cover)를 **Claude 가 독립·적대(refute)로 재수행**. Codex 자체 10-pass(`Codex/results/PHASE_028_…10PASS_REVIEW.md`)는 PASS 선언 — 본 검수의 목적은 **그 자체검수가 놓친 결함 적발(cross-model adversarial)**. 각 pass = 전담 에이전트 1, 전 945줄 cover, refute + 최약점 + 빈통과금지.
> **권한**: 사용자 명시 지시로 Codex 산출물 read 수행(P2 경계 예외). Codex 파일 **무수정**(read-only 검수).

---

## 0. 종합 판정 — **조건부 PASS (수정 권고)**

Codex V4 는 \*자기인식이 강한\* 우수한 Chapter 1 이론 배경이다. 단일 인과 사슬(관찰→평형 기각→동역학→spectrum→Volterra→closure→fiteq→반증)이 닫혀 있고, 사용자 요건 (a)논문/특허 발전 가능 (b)학부 무비약 전개 (c)Ch1 단독 simple-fit 도출을 **대체로 충족**한다. **Codex 가 Claude base 의 여러 결함(특히 ★Eyring 부호)을 정확히 수정**한 것은 cross-model 검수의 실적이다.

그러나 **독립 10-pass 는 Codex 자체검수가 놓친 실결함을 적발**했다: 구조 CRITICAL 2 + 물리 CRITICAL 1 + HIGH 다수. 출판/특허 발전 전 보강 권고. **잔여 critical 0 이라는 Codex 자체 주장은 기각** — 아래 §3 참조.

| 차원 | 판정 |
|---|---|
| 빌드/정적 무결성 | PASS (undefined cite 0·미사용 bibitem 0·중복 label 0·`$$` 0; 단 §3-A AL 결번·`\pageref{LastPage}` 예외) |
| convention 일관성(χ_j≠β_j 등) | 대체로 PASS (Codex 개선 실적) — 단 χ_j=1/2 keystone 모순(§3-E) |
| 무비약(G-noleap) | 부분 — 압축 유도 생략 3곳(§3-F) |
| grounding(AL ledger·DOI) | 부분 — AL-8/9 결번(§3-A)·established over-reach(§3-J) |
| G-usable(비순환 피팅) | **미충족** — χ_j↔전류 prefactor 공선형(§3-D) |
| 물리 정합 | **1 CRITICAL** — stretched-tail ↔ single-L Eyring/N2 모순(§3-C) |

---

## 1. ★ Cross-model 핵심 결과 — Eyring 부호: **Codex 옳음 확정 + Claude 부호 오류 노출**

Codex V4(라인 786–791)는 유효 enthalpy 추출식을
`y(T)=ln[1/(LT)] − χ_j A_j/(RT)` 를 1/T 로 회귀 ⇒ 기울기 = −ΔH_a/R (**minus**)
로 두고, "ln(1/L) 안에 이미 +χ_j A_j/RT 가 있어 더하면 double-count" 라 설명한다.

**독립 재유도(Pass 5·Pass 9·검수자 직접, 3중 일치) — minus 가 옳다**:
- L=|I|/(Q_cell k_j), k_j=k_0(T)e^{−(G−χA)/RT}, k_0=(k_BT/h)κ
- ⇒ ln(1/(LT)) = const + ln κ − G/RT **+ χA/RT** (∵ −(G−χA)=−G+χA)
- G=ΔH_a−TΔS_a 대입 ⇒ ln(1/(LT)) = const + ΔS_a/R − ΔH_a/RT + χA/RT
- 순수 −ΔH_a/R 추출 → +χA/RT 항을 **빼야** 함 ⇒ y = ln(1/(LT)) **− χA/RT**, 기울기 −ΔH_a/R ✓

**⟹ Codex V4 의 부호(−)는 물리적으로 정확하다.** 동시에 이 검수는 **Claude 측 `graphite_ica_ch1_rebuilt.tex` 라인 780 이 `+χ_j A_j/RT`(plus) 로 \*반대 부호\*** 임을 노출했다 — 이는 χA 전위보조 항을 두 번 더하는 **확정 부호 오류**이며, 통합본 `full_rebuilt.tex` 에도 전파돼 있다. **Codex 의 Claude-base 검수(PHASE_022/026)가 이 버그를 정확히 진단·수정한 것**이고, Claude 측은 미수정 상태다. → 권고 §5-B.

(부수 확인: P5·P9 가 `ln κ(T)` 잔차가 slope 에 남는 점은 별개로 지적 — §3-H.)

---

## 2. Codex V4 가 Claude base 대비 정확히 수정한 것 (defused — 인정)

독립 검증 결과 \*실제로 개선\*된 항목(빈 칭찬 아님, refute 시도 후 통과):
- **Eyring 부호** minus 정정(§1) — 물리 정확, Claude 미수정 노출.
- **χ_j ≠ β_j 분리** — Level-A scalar relaxation sensitivity vs Ch.3 transfer coefficient 를 convention 절·keystone 에서 명시 분리(라인 110·136–138·369–370). Ch.1 결과 오염 없음(P9 확인).
- **C-rate 단일부호 과주장 제거** — prefactor / potential-assist / apparent-polarization 의 competition 으로 표현(라인 801–803·822–824). P9 통과.
- **ρ_G 역산 비유일** — forward-only 정직 표기(라인 529–533·N4). P8·P9 통과.
- **barrier-only 평균장** — AL-13 FLAGGED 로 협동적 staging 충돌 인정(라인 461–467). P9 통과.
- **메타데이터·placeholder bib 제거** — `RB 재구성본`·`CHARTER`·`Author/Date`·placeholder 0; bibitem 23 전부 실명·DOI(P4·P7 확인). ★Claude full 은 ch6_* appendix 137 라벨 유지 — Codex 의 lean scope 와 설계 차이.
- **정적 무결성** — undefined citation 0·미사용 bibitem 0·중복 label 0·인접 `$$` 0 (P7 static parse 재확인).

---

## 3. 적발 결함 (severity별, Pass 추적 — Codex 자체검수 blind spot)

### CRITICAL

**[C-A] AL-8·AL-9 결번 (P1·P4 독립 수렴, 최약점)** — AL ledger 가 AL-1~7 다음 곧장 AL-10 으로 점프, **AL-8·AL-9 가 ledger·본문 어디에도 부재**. GS-3("모든 가정=AL-# 인용") 자기선언과 정면 모순 → "닫힌 ledger·1:1 정합" 검증이 \*성립 불가\*(누락 8·9 가 무엇을 grounding 했어야 하는지 불명, orphan 가정 배제 불능). 단순 typo 아닌 판본 진화 중 ID 미정리. Codex 자체 10-pass 가 ledger \*내용\*은 봤어도 \*번호 연속성\*은 못 본 기계검증 가능 반례. **보완**: 8·9 채워 연속화하거나 `AL-8 (deprecated/Ch3 전용)` 명시 placeholder.

**[C-B] 기본 물리 상수 R·F·T·k_B·h 미정의 (P2)** — 기호표(§notation 96–122)에 보편상수 행 0, 첫 등장도 명명·정의 없음(F@109·R/T@215·k_B@221·h@347). "학부 무비약·중간 생략 금지"(GS-1) 헌장과 자기모순. **보완**: 기호표에 상수 블록 1개 추가.

**[C-C] stretched-tail spectrum ↔ single-L Eyring/N2 물리 모순 (P9, P10 echo — 가장 깊은 물리 결함)** — 문서 핵심 메커니즘(저온 긴 꼬리 = ρ_G 분포 spread σ_G/RT 증가, Svare 2000 stretched-exp)은 σ_G>0 을 \*요구\*한다. 그런데 §ch1_simplefit 단계(3)·반증 N2 는 **단일 L(T)** 에서 단일 ΔH_a 를 Arrhenius 직선 회귀로 뽑는다 — 단일 L 은 σ_G→0(δ-collapse) 극한에만 존재. 꼬리가 stretched 인 순간(=§spectrum 의 존재 이유) ln(1/L_eff) 는 1/T 에 \*곡선\*(Svare/Johnston 인용 결과)이 되어, **N2("직선 아니면 단일 활성화 기각")가 이론이 stretching 을 예측하는 바로 그 영역에서 이론 자신을 기각**한다. 라인 793 은 \*shape\* fit 붕괴만 인정하고 \*ΔH_a 추출\*의 동일 붕괴는 비껴가며, spectrum 영역 ΔH_a 추출 정의도 부재. **보완**: 단계(3)·N2 를 narrow-spectrum(σ_G/RT≲1) 게이트로 한정 + stretched 영역의 올바른 반증(ρ_G forward-예측 곡률) 별도 정의 + spectrum 영역 ΔH_a 정의(ρ_G 평균).

### HIGH

**[H-D] χ_j 추출 비순환 깨짐 — 전류 prefactor 공선형 (P8, G-usable 1급)** — 단계(2) 가로축 V_drive 를 움직이는 실제 손잡이가 전류인데, ln L = ln|I| − ln(Q_cell k_0) + (G−χA)/RT 에서 `∂lnL/∂ln|I| = +1`(prefactor 항, 라인 801–802 자인)이 χ_j 와 공선형. "비순환 보장"(라인 778)은 ΔH_a 축만 방어하고 χ_j↔전류 prefactor 는 못 끊음. **보완**: 회귀를 `ln L − ln|I|`(=ln(1/(Q_cell k_j))) 를 V_drive 에 회귀하도록 명시(prefactor 차감), 또는 동일 |I| 내 V_n sweep 만 χ_j 에 사용.

**[H-E] χ_j=1/2 keystone 모순 (P5·P9·P10 수렴)** — Marcus 1차 대칭 전개는 χ_j=**1/2** 단일값만 유도(라인 326–335). 0≤χ_j≤1 일반화의 근거로 든 "곡률 비대칭 λ_f≠λ_b" 는 forward/backward 배리어 shift 를 불균등하게 만들어 **keystone(라인 356–376)의 대칭 common-mode 인수분해(r⁺/r⁻ 불변)를 깬다** — 즉 χ_j≠1/2 의 출처가 곧 Level-A "방향 없음" 전제를 위반(Level-B 누설). 자기모순. **보완**: (a) Level-A χ_j=1/2 엄격 고정 + χ≠1/2 는 Ch.3 로, 또는 (b) χ∈[0,1] 을 경험 BEP/BV 계수로만 출처화(λ_f≠λ_b 근거 철회)하고 Marcus 유도 불가 명시.

**[H-F] 압축 유도 생략 3곳 (P3 — Claude 945 vs 1627 압축의 증상)** — ① eq:closed(라인 668–671) Plan A 닫힌형 분모 인수분해 한 줄(`Θ[1−J/Θ⁰]=c → Θ=c/(1−J/Θ⁰)`) 부재 — 사용자가 \*명시 요구\*한 클라이맥스 대수. ② a(q') 절편식(라인 643) Θ⁰ 둘레 전개→상수 재정리 중간형 부재. ③ 동차항 Θ_init 적분화(라인 590–591) mode별 동차해 중첩 유도 부재(단정). **보완**: 각 한 줄 중간식 삽입.

**[H-G] Plan B 선언 vs Plan A 종착 불일치 (P6·P10)** — "Plan B 우선(항상 보존)·Plan A 보조" 라 \*선언\*하나, 실 deliverable(fiteq·simplefit 의 닫힌형 dQ/dV)은 전부 Plan A 계열이고 Plan B(수치해)는 fiteq 에 대입할 해석식을 못 줌. 저온 stretched(closure 가장 필요)에서 Plan A 가장 부정확(라인 681–682 자인) → 위계 선언과 실제 산출물 의존 충돌. **보완**: 저온/넓은-spectrum 은 fiteq 의 dΘ/dQ 를 Plan B 수치미분으로 \*강제\*, Plan A 는 고온/narrow 한정 — 그래야 lean §numeric("solver 코드 범위 밖")과 결합해 저온 정량 피팅의 실행가능 경계가 명확.

**[H-H] Eyring slope 에 ln κ(T) 잔차 (P5)** — y(T)=const+**ln κ(T)**−ΔH_a/RT+ΔS_a/R 이라, 기울기=−ΔH_a/R 은 d(ln κ)/d(1/T)=0 일 때만 엄밀. 라인 790 은 ΔH_a≳40 kJ/mol 게이트로 단정(유도 아님) — k_BT/h 의 lnT 오염은 1급 보정으로 다루면서 수학적으로 동형인 κ(T) 오염은 각주로 강등(비대칭). **보완**: y 에 ln κ(T) 명시 + κ-평탄 가정의 정량 부등식.

**[H-I] Q_bg 이중역할 (P9)** — Q_bg 가 한편 "잔류 chemical capacitance"(C_bg=∂Q_bg/∂V_n, self-coupling b·fiteq 분모), 다른편 "ξ 지연 흡수자"(라인 188–190, rate/lag 의존)로 충돌. lag 부분이 background 에 섞이면 C_bg 가 Θ 물리를 double-count, ε_Q>0 well-posedness 미보장. **보완**: Q_bg=Q_bg^eq+Q_bg^lag 분해, C_bg 에는 eq 부분만.

**[H-J] established over-reach + AL mode-mixing (P4)** — ① 라인 485 "저온 긴 꼬리 메커니즘 established(svare2000)" 가 AL-13(협동성 FLAGGED)을 우회해 독립완화 권위를 빌려옴. ② AL-11 단일 ID 에 BEP(경험)+BV+Marcus(이론) 혼합 — χ 일반범위는 BEP 출처인데 Marcus/BV 권위 전이. **보완**: established 적용 전제를 문장에 박고 AL-11 을 established/empirical 분리.

**[H-K] kernel 정의 전환 + L-분리 무증명 (P6 — CRITICAL로 분류, 보수적으로 HIGH)** — eq:kernel_integral(잔차 도함수 중첩)과 eq:volterra(목표에 kernel 곱)가 \*다른 양\*에 작용하는데 단조 일반화인 척 전환; boundbox(라인 603) 스스로 잔차형을 금지 경고. eq:volterra 의 L-적분 분리는 r̄-균일 근사(라인 543)를 암묵 상속하면서 "유도"라 주장(근사를 유도로 위장). **보완**: kernel_integral 을 post-peak 시각화용으로 강등 + fiteq 입력 dΘ_tail/dq 를 eq:volterra/closed 미분으로 유일 지정 + 분리의 두 가정(Θ_eq g-독립 AND r L-독립) 명시.

**[H-L] 단계(3) R_n/C_bg 온도의존 누락 + single-mode L circular (P8)** — (3)이 여러 T 의 L 을 쓰는데 L_φ 환산의 C_bg(V_n,T)·R_n(T) 온도의존을 (0)단계가 저속 1회만 고정 → ΔH_a 오염; 각 T 재고정 단계 부재. (1)단계 단일지수 회귀가 저온 stretched 에서 window 의존 인공 L 을 주고 (2)(3)에 전파, single-mode↔spectrum 전이 정량기준 부재. **보완**: (0)을 T별 반복 + (1)에 stretched 종료조건.

### MEDIUM (요지)
- A_L convention amplitude/A_0·Θ_0 규격 화해 미명시(P1·P2·P5) · q_a 기호표 누락(P1) · w_j ideal RT/F vs effective 이중(P1) · C_bg 정의-사용 역순+기호표 누락(라인 647 vs 651, P7) · ξ_ss,j 정의없는 forward-ref(라인 374, P7) · κ·s_I·η_ct·D 미정의(P2) · N5 판별이 OCV vs operando 전위 불일치(P9) · dahn1991 역할 오귀속(상도표 vs ICA peak, P4) · Marcus bound 부등식(G−χA≥0) AL-15 절에 미명시 정성판단(P4) · b(q') 평형도함수=동역학경로 동일시 부분순환(P6) · flagbox "평형형태 무관" 과주장(q_a·amplitude 는 isotherm 의존, P9).

### LOW
- theorem box 라벨 한/영 혼용 · dangling label 6건(eq:Geff 등 \eqref 0회) · section 제목 언어혼용 · `\pageref{LastPage}` static "undefined"(패키지 auto-label, 컴파일 통과) · L "length"(무차원) 명칭.

---

## 4. 10-pass coverage (실제 수행)

| Pass | 초점 | chunk | 핵심 적발 |
|---|---|---|---|
| P1 | 구조·메타·convention | section-level | ★AL-8/9 결번(C-A)·q_a/w_j 기호표 |
| P2 | 변수 도입·의미 | 70줄 | ★R/F/T/k_B/h 미정의(C-B)·κ/s_I/η_ct/D |
| P3 | 수식 연쇄 무비약 | 90줄 offset | ★eq:closed/a(q')/동차항 압축 생략(H-F) |
| P4 | 물리가정·grounding | 120줄 | AL-8/9(C-A)·established over-reach·AL-11 mixing(H-J) |
| P5 | 단위·차원·부호 | 55줄 | ★Eyring minus 확정(§1)·ln κ 잔차(H-H)·χ=1/2(H-E) |
| P6 | 논리 의존 사슬 | dependency | kernel 정의전환·L-분리 무증명(H-K)·Plan B/A 불일치(H-G) |
| P7 | 역순 forward-ref | 95줄 역순 | C_bg 역순정의·ξ_ss,j 미아·정적무결성 재확인 |
| P8 | 피팅 사용성·비순환 | usability | ★χ_j↔전류 prefactor 공선형(H-D)·R_n(T) 누락(H-L) |
| P9 | 적대 물리 | adversarial | ★stretched↔single-L Eyring 모순(C-C)·Q_bg 이중역할(H-I) |
| P10 | 최종 sweep·요건 | full 1청크 | 조건부 PASS·HIGH 3 우선(Plan A 저온·평균장·χ_j 해석) |

---

## 5. 권고

**A. Codex V4 보강 우선순위 (출판/특허 발전 전)**
1. **물리 CRITICAL [C-C]** — stretched 영역 ΔH_a 추출·N2 반증 재정의(이론 자기기각 제거). \*최우선\*.
2. **구조 [C-A·C-B]** — AL-8/9 결번 정리 + 기본상수 등재(기계검증 가능, 즉시).
3. **G-usable [H-D]** — χ_j 추출 prefactor 차감 명시(Ch1 단독 비순환 피팅의 전제).
4. **[H-E·H-K·H-F·H-G·H-I]** — χ_j=1/2 정합·kernel 정의·압축 유도·Plan B/A 위계·Q_bg 분해.

**B. Claude 측 동반 조치 (본 검수가 노출)**
- ★ **Claude `graphite_ica_ch1_rebuilt.tex` 라인 780 부호 오류**(`+χ_j A_j/RT`→`−`) 수정 + `full_rebuilt.tex` 전파분 동시 수정. Codex V4 부호(minus)가 정답이므로 Claude 가 Codex 를 따라야 함. (Claude Ch2~5 검수서 이미 Arrhenius 유효엔탈피를 다뤘으나 Ch1 부호는 미정정 잔존.)
- [C-C](stretched↔single-L)·[H-D](전류 prefactor)·[H-I](Q_bg)·[H-E](χ_j=1/2)는 \*Claude Ch1 도 동일 lineage\*라 \*공유 결함\* 가능성 높음 — Claude Ch1 simplefit/falsify 도 동일 점검 권장.

**C. 설계 차이(부록 B) 판정** — Codex lean(Ch1=이론+simple-fit+최소 numeric, solver 범위 밖) vs Claude(구 Ch6 부록 B 흡수, 1627줄). 사용자 (a)(b)(c) 요건엔 \*양쪽 다 가능\*; Codex 는 Ch1 가독·scope 명료, Claude 는 실무 피팅 self-contained. 단 [H-G]대로 저온 정량 피팅이 Plan B(수치) 의존인데 Codex 는 solver 를 범위 밖으로 밀어 **저온 실행가능성이 Ch1 단독으로 안 닫힘** — 이 점은 Claude 의 부록 B(수치 상세)가 보완 우위.

---

## 6. 메타 — Codex 자체 10-pass 가 놓친 패턴 (cross-model 가치)
Codex 자체 10-pass 는 "잔여 critical 0" 선언했으나 독립 적대 검수가 **기계검증 가능 구조 결함(AL 결번·상수 미정의)과 자기참조 물리 모순(stretched↔single-L)을 적발**. 패턴: 자체검수는 \*자기가 자신있는 물리\*(Eyring 부호·χ_j convention — 실제로 옳게 고친 부분)에 집중하느라, ① ledger 번호 연속성 같은 \*형식 무결성\*, ② "물리적으로 자명"으로 간주한 \*기본 상수 정의\*, ③ 자기 이론의 두 부분(spectrum stretched vs simplefit single-L)이 \*서로 모순\*되는 교차지점을 사각으로 남겼다. 이는 Claude Ch2~5 절별 검수가 거친 3렌즈의 사각을 적발한 것과 동형 — \*독립 적대 다중 pass\* 의 구조적 이점.

---
**검수자**: Claude (Opus 4.8 1M) · 독립 적대 10-pass · Codex 파일 무수정 · 2026-06-02.
