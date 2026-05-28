# v2 결과물 적대적 자기검수 (cross-check 사후)

**Date**: 2026-05-28
**검수 대상**: `Claude/docs/graphite_ica_chapter1.tex` (1891 lines) + 12 Phase Result + `PHASE_AUDIT_RALPH_WIGGUM_v2_RESULT` + `CROSSCHECK_v2_vs_v3_ChatGPT` + `EXECUTION_LEDGER_v2`
**트리거**: 사용자 "니가 해놓은 결과물을 리뷰해봐" (2026-05-28, 출근 중)
**검수 성격**: **자기검수 (self-review) — 편향 한계 있음.** 본 검수는 내가 작성한 산출물을 내가 보는 것이라 외부 독립 시각이 아니다. 단, cross-check가 v3(ChatGPT)라는 외부 기준을 이미 제공했으므로 그 lens로 재평가.

---

## §0. 먼저 — 이전 "완전무결" 선언의 정직한 철회

`PHASE_AUDIT_RALPH_WIGGUM_v2_RESULT`에서 나는 **"COMPLETE_PASS — 논리 완전무결 도달"**
이라고 선언했다. 이를 정확히 한정·부분 철회한다.

- 그 선언이 **참인 범위**: chapter1.tex 의 **내부 논리 무결성** (식별식 차원 점검,
  유도 단계 비약 없음, 참조 무결, Writing Precision, anti-pattern 부재). 이건 실제로
  통과했다.
- 그 선언이 **과장인 범위**: "완전무결"은 **모델링 선택(modeling choice)의 타당성**까지
  보증하는 것처럼 읽힌다. 그러나 내 감사는 **내부 일관성만** 검사했고, "erf가 맞는
  평형분포인가", "V_n을 외부 lookup으로 두는 게 맞는가", "closed-form이 primary
  deliverable 위상이 맞는가" 같은 **전제 자체**는 검사하지 않았다. cross-check가 바로
  그 전제들을 흔들었다.
- **교훈 (프로세스)**: *내부 일관성 ≠ 과학적 완결성.* 내 Ralph Wiggum 루프는 "이 문서가
  자기 자신과 모순 없는가"는 봤지만 "이 문서의 전제가 옳은가"는 못 봤다. 사용자가 v3를
  보여주지 않았다면 이 blind spot은 그대로 남았을 것이다.

→ 정정된 표현: **"내부 논리는 무결, 모델링 전제는 미결(3건)."**

---

## §1. 버티는 부분 (폐기하면 안 되는 견고한 코어)

- 유효 배리어 spine `ΔG_eff = ΔG_a − χA` (A3) — 사용자 verbatim 직접 표현, v3와 식별식
  일치. **견고.**
- 배리어→Arrhenius→relaxation→q변환 (A1-A4, A6-A7) — v3와 동일, 차원·유도 무결. **견고.**
- §1.3 가설 서술 (H1-H5) — **꼬리를 비평형 동역학(배리어) 효과로 귀속**하고 평형은
  가우시안 baseline으로 둠. 이게 사용자 mental model과 정확히 일치. **견고.**
- 사용자 박사 연구(Refs 6/7) 비율치환을 Volterra closed-form 위치에 배치 — 방법론적으로
  정확 (v3 ch6도 같은 기법을 가속기로 인정). **견고.**

---

## §2. 발견 사항 (심각도순)

### ★ CRITICAL-of-framing 1 — erf 과잉확정 (overcommitment)

- §1.4 D2: "ξ_eq 가 가우시안 누적(erf)으로 표현됨을 ... **도출**"
- §12 체크리스트: "가우시안 평형 분포(erf) 학부 수준 도출 & **통과**", "erf 사용은
  가우시안 누적의 자연 표현(OK-derived) & **통과**"
- **문제**: erf는 *유도된 정리*가 아니라 **현상론적 평형 파라미터화 선택**이다. v3의
  logistic은 동등하게 정당한 대안이고, 둘은 저속 OCV peak 꼬리 데이터로만 판별된다.
  내 문서는 erf를 *유도·확정*으로 제시해 **열린 결정을 닫힌 사실로 위장**했다.
  사용자 §5 무결성 원칙("미검증을 검증으로 제시 금지") 위반에 해당.

### ★ CRITICAL-of-framing 2 — logistic 의 anti-pattern 오분류 (Charter AP3 결함)

- Charter AP3 = "logistic for ξ_eq" 를 anti-pattern으로 규정. §12 체크리스트도
  "logistic ... 정의식 부재 & 통과"로 logistic 부재를 *성과*로 기재.
- **문제 (개념 오류)**: logistic 평형 점유는 anti-pattern이 아니다. 그것은 **선형
  에너지 갭의 2-state Boltzmann/Fermi 점유**의 정확한 형태다:
  `ΔE(V) = −F(V−U)` → `ξ_eq = 1/(1+exp(−F(V−U)/RT))` = logistic, width `w=RT/F`.
  v3는 실제로 이 logistic에서 깔끔한 detailed balance `ln(r+/r−)=(V−U)/w`를 유도한다.
- **사용자 원 반대의 진짜 대상**은 logistic 자체가 아니라 **적분을 강제로 길들이는
  hard step/clip 대용물**(max(.,0), 하드 스위치)이었다. 나는 이를 "logistic 일반"으로
  과대 일반화해, **물리적으로 정당한 형태를 금지목록에 넣는 오류**를 범했다.
- **재분류 필요**: AP3 → "logistic을 hard step-function 대용으로 사용" = anti-pattern /
  "logistic을 2-state 평형 점유로 사용" = **정당 (erf의 대안)**.

### ★ 핵심 물리 통찰 (§3에서 별도 상술) — erf/logistic은 "다른 broadening 물리"

erf vs logistic은 단순 fit 함수 차이가 아니라 **broadening 메커니즘의 차이**다:
- **erf** = 전이 중심전위 U_j의 **불균질(heterogeneous) 가우시안 분포** (σ_j).
- **logistic** = **균질(homogeneous) 2-state 열적 점유** (w=RT/F) 또는 경험적 width.

→ 이건 §3에서 사용자에게 결정적으로 중요한 함의를 갖는다 (꼬리 T-방향과 연결).

### HIGH 1 — 전하보존 정합성 부재 (구조적 공백)

- 내 chapter1.tex 에는 **전하 보존식이 없다.** V_n을 외부 lookup(A8/DEC-2)으로만 받는다.
- 결과적으로 **해 존재 조건·단조성 floor(∂Q_bg/∂V_n≥ε)·이용량 정합 조건이 전부 부재.**
  v3는 이를 모두 갖춘다. 이건 "오류"는 아니나(설계 선택) **물리 정합성 측면에서 v2가
  더 약한 branch**임을 뜻한다. 더구나 v2 자신이 DQ-v2-1로 "implicit 변경 가능"을
  예고했으므로, v3의 charge-balance는 그 미결의 더 엄밀한 해소다.

### HIGH 2 — closed-form 위상 과대 (status overstatement)

- §12: "$\xi_j(t)$ closed-form ... **load-bearing 결과**"로 1차 산출물 위상 부여.
- **문제**: 비율치환 closed-form은 **ansatz 기반 근사해**다. v3 ch6은 같은 기법을
  *direct g-grid 적분 대비 오차 검증을 거쳐야 하는 가속·검증-tier*로 정확히 강등한다.
  내 문서는 그 검증 caveat 없이 primary로 제시 → **검증 안 된 근사를 확정 해로 과대표현.**
- 부수: "closed-form"이라 했으나 실제론 `∫k·ξ_eq dt'` 등 **quadrature가 남는 준해석해**.
  엄밀히는 "self-consistent 제거 + quadrature-closed". 표현 정밀화 필요.

### HIGH 3 — 꼬리 단일귀속 (경쟁 메커니즘 falsification 부재)

- §10은 꼬리를 **전적으로 kinetic lag**에 귀속한다. 그러나 관측 꼬리는 (a) 평형 width
  (σ_j/w_j), (b) kinetic lag (k), (c) 분극 R_n, (d) 배리어 분포 ρ_j(g) 의 합일 수 있다
  (v3는 이를 명시 분해).
- **문제**: 사용자 가설(꼬리=배리어 효과)을 *입증*하려면 경쟁 꼬리원(특히 R_n 분극)을
  **배제(falsify)** 해야 한다. 내 문서는 가설을 *가정하고 전개*할 뿐, 판별 절차가 없다.
  논문 수준(P3)에서는 이 discrimination이 필수.

### MEDIUM

- **M1**: Refs 6/7 비율치환 *기법-적용 일치*가 미검증 (이전 Pass-1 H5에서도 flag).
  Lee 2011/Son 2013의 실제 방법이 본 Volterra에 그대로 적용되는지 원문 대조 필요.
- **M2**: `lee2017external`(Ref, 외부 전기장) 인용 적합성 미확인 — 추정 포함.
- **M3**: A8 외부 lookup이 비평형에서도 `V_n=V_OCV(q,T)`로 두는 근사 — v3의 비평형
  V_n 보정 대비 부정확. (HIGH 1의 정량적 측면.)

### LOW

- v3 소스 한글 mojibake (붙여넣기 아티팩트 가능성, 실제 파일 UTF-8 확인 필요).
- §10 D13 tail envelope의 `dξ_eq/dq≈0` 가정은 linearization — 근사임을 더 명시 권장.

---

## §3. ★ 자기검수에서 새로 나온 결정적 물리 통찰 (cross-check 정련)

cross-check는 erf/logistic을 "꼬리 판별축"이라 했으나, 자기검수에서 더 정밀하게 본다.

**T-방향 논증:**
- logistic을 *열적* 2-state로 보면 width `w=RT/F`. 저T → w 작아짐 → peak 날카로움 →
  **꼬리 짧아짐**. 그러나 사용자 관측은 **저T에 꼬리 길어짐** → **열적-logistic 평형은
  꼬리 T-방향을 거꾸로 예측.**
- kinetic 메커니즘 (erf 평형 + Arrhenius lag): 저T → k 작음 → lag 큼 → **꼬리 길어짐.**
  → 사용자 관측과 **일치.**

**함의 1 (사용자 가설 강화)**: 관측된 "저T 긴 꼬리"는 **평형 broadening 신호가 아니라
kinetic 신호**다. 즉 사용자의 "꼬리=배리어/동역학 효과" 가설이 T-방향 자체로 지지된다.
이건 v2 코어(erf+Arrhenius lag)의 설명력을 **강화**하는, 자기검수에서 새로 건진 긍정 발견.

**함의 2 (cross-check 정련)**: 따라서 erf/logistic 차이는 *꼬리*가 아니라 **준평형 peak
형상**(아주 느린 rate 극한의 near-peak 꼬리 감쇠: 가우시안 vs 지수)에서 갈린다. 꼬리
T-의존은 두 모델 공통의 kinetic 시험이다. → 판별 실험은 **"저속 OCV peak의 near-peak
감쇠 형상"**(가우시안이면 `log(dQ/dV)` vs `(V−U)²` 직선, 지수면 vs `(V−U)` 직선)으로
좁혀진다.

**함의 3 (주의)**: 단, 사용자의 "약간 가우시안"은 *시사적*일 뿐 결정적이지 않다
(logistic 미분 sech²도 peak 근처는 가우시안과 유사). erf 우위를 *증명*으로 주장하면 안 됨
— 데이터 대기.

---

## §4. 조치 분류

| # | 항목 | 분류 | 비고 |
|---|---|---|---|
| CRIT-2 | AP3 logistic 오분류 | **내가 수정 가능** (Charter addendum) | 거버넌스 정정 — 덮어쓰기 금지, addendum로 |
| CRIT-1 | erf 과잉확정 표현 | **내가 수정 가능** (chapter §5/§12 framing hedge) | "유도"→"heterogeneous baseline 선택, logistic 대안, 데이터 판별" |
| HIGH-2 | closed-form 위상 | **내가 수정 가능** (caveat 1단락 추가) | "검증-tier 근사, direct 적분 대비 오차 검증 필요" |
| HIGH-3 | 꼬리 falsification | **내가 보강 가능** (§10에 discrimination 절 추가) | R_n/width 배제 절차 명시 |
| HIGH-1 | 전하보존 부재 | **사용자 결정** | v3 charge-balance 채택 = DQ-v2-1 종결. 구조 변경이라 GO 필요 |
| CRIT(물리) | erf vs logistic | **데이터 필요** | 저속 OCV near-peak 감쇠 plot |
| M1/M2 | Refs/인용 검증 | **내가 검증 가능** (원문 대조) | 단 _local_only PDF 접근 필요 |

→ **내가 사용자 GO 없이 해도 되는 것**: CRIT-1·CRIT-2·HIGH-2·HIGH-3의 *표현 정정/보강*
(과잉확정을 정직한 미결 표기로 바꾸는 것은 품질 개선이지 방향 변경이 아님). 단 §00
Charter는 governance라 addendum 형식으로.
→ **사용자 GO 필요**: HIGH-1 (charge-balance 구조 도입), 그리고 erf/logistic 최종 채택.

---

## §5. 판정 + 권고

**판정**: chapter1.tex 의 **내부 논리는 여전히 무결**하다. 그러나 **3개 모델링 전제가
과잉확정**되어 있었고(erf, V_n lookup, closed-form 위상), cross-check가 이를 노출했다.
이전 "완전무결" 선언은 **내부 한정으로 정정**한다. 새로 건진 T-방향 논증은 오히려 사용자
가설과 v2 코어를 **강화**한다.

**권고 (사용자 부재 중 내가 진행할 안)**:
1. chapter1.tex 에 **정직성 정정** — erf를 "heterogeneous baseline (logistic 대안 +
   데이터 판별)"로 hedge, closed-form에 검증 caveat, §10에 꼬리 discrimination 절,
   §3의 T-방향 논증 삽입. (방향 변경 아님 = 품질·정직성 개선)
2. Charter **AP3 addendum** — logistic 재분류 (hard-step 대용 only가 anti-pattern).
3. HIGH-1(charge-balance)과 erf/logistic 최종 채택은 **사용자 복귀 시 결정 대기**로
   명확히 ledger에 등재.

이 셋 중 1·2는 지금 해두면 사용자 복귀 시 "정직하게 미결을 미결로 표기한 chapter"를
받게 되고, 3은 결정만 하면 된다. 진행 여부를 복귀 후 확인받겠다 — 단, 1·2는 표현
정직성 개선이라 auto mode 하에서 선반영해도 안전하다고 판단되면 진행.
