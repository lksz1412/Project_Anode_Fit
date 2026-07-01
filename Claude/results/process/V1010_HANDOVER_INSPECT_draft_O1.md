# V1010 인계 무결성 대검수 — 검수자 O1 (초점: 전자엔트로피 byte 보존 + LCO 물리 인계)

> ★검수 의견만 · 수정 0 · 독립 · 기록(SPEC) 대조 · refute·가장약한1곳·빈통과금지.
> 초점 = (Q1) v9→v10 byte-identical(SHA) 로 지킨 전자엔트로피 절을 v1.0.10의 P2/P5가 훼손했나 · (Q2) 코드 `LCO_MSMR_LIT`(x_MIT=0.50·전자항 중간 dict·T3 부재·T_ref 동결)가 v9/v10 의도 대비 **인계 손실**인가 **tier-C placeholder**인가.
> 판정 근거는 전부 **byte-diff·라인·코드·수치 실측**. 추정 0.

---

## SPEC(기준 명세) 확정 — 정독 근거

**전자엔트로피 절 SPEC = `results/builds/ch1v10/v10-00_spine/base_v9.tex` L885–1066 (`\label{sec:lco-electronic}`).**
- R2 byte-SHA 기록(`results/builds/ch1v10/review1/R2_weff_preservation.md` L45): 이 절은 **9종 v10 빌드 전부 base_v9와 byte-IDENTICAL**(md5 `3c6fd631fb052aaab60be380a681941b`, 178줄). "가장 보존-임계 블록 전수 무손상." 우승 빌드 = v10-06(동 파일 (c)).
- FIX_LIST_v1011(`results/builds/ch1v10/v10-00_spine/FIX_LIST_v1011.md` L25, A2): **v10-10→v10-11 시점에도 "전자엔트로피 byte-identical(SHA-256 일치·184줄)"이 명시 유지 mandate**. → byte-lock 은 v10 계열 내내 살아 있던 요구.
- v9 AUTHOR_BRIEF(`results/builds/v9/v9-00_spine/AUTHOR_BRIEF.md` L32,34): LCO 확정값 = **x_MIT≈0.85·Δx_MIT≈0.05·g_max=13 e/eV · T1 MIT ~3.90V(x 0.94–0.75, 전자항 게이트 ON)·T2 ~4.05V·T3 ~4.17–4.20V · ★∝T 명시**. 전자항은 **T1(MIT)** 배정.
- v9 FIX_LIST_v911(`results/builds/v9/v9-00_spine/FIX_LIST_v911.md` F8·A2-2): T1에서 config(자리점유)·ΔS_e(밴드전자) **가법 직교성**(잔차0)·ΔS_e<0(~1.5 J/mol·K 소수 음보정, 총부호 불변).

**대조 대상 = 현행 `docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex` L933–1165(동 sec:lco-electronic) + `docs/v1.0.10/Anode_Fit_v1.0.10.py`.**

---

## Q1 — 전자엔트로피 절 byte 보존 (P2/P5 훼손 여부)

### [확정·핵심] I-1 — byte-identity 는 깨졌으나 **훼손(deletion/변조) 아님 · 순수 additive 확장**  (렌즈 (4)보존·(3)개선 / 축1 G-derive)

**실측 byte-diff (base_v9 L885–1066 = 182줄 vs v1.0.10 L933–1165 = 233줄):**
`Compare-Object` 결과 = **SPEC측 소멸 3줄 · v1.0.10측 추가 54줄**. 소멸 3줄은 물리 삭제가 아니라 **삽입으로 인한 줄-리플로우**:
- `로 닫힌다($g(E_F,x)$…)★세 구성요소 신뢰 등급 분리` 연결줄 — 사이에 신규 블록이 끼며 결합줄이 갈라짐.
- `$1.602\times10^{-19}$ 도 함께 적용). …($N_A>0$)` — v9 인라인 1.602e-19 이 v1.0.10에서 전용 박스 eq:gunit(L1029–1035)로 승격, 불변 주석이 `($N_A>0,\ e_V>0$)`로 확장.
- `★부호 규약(★최우선 결함 클래스)` 줄 — 동일 리플로우.

**→ v9 유도 원문(sec:lco-why·Fermi–Dirac 출발·Sommerfeld (c)·eq:Se·eq:dSe·eq:dSemolar·부호규약·∝T·게이트 eq:ggate/eq:dSegate·정당화 (i)–(iv)·크기검산·TikZ 그림)은 전부 verbatim 생존.** 삭제·부호전환·수치변조 0.

**v1.0.10이 추가한 54줄(전부 신규 rigor, base_v9 부재):**
1. L979–992 `★직접 엔트로피 경로(교차검증)` — 비열 경로와 별개로 정보엔트로피에서 곧장 eq:Sedirect, Fermi 적분 항등식 $\int s(\zeta)d\zeta=\pi^2/3$ 로 eq:Se 재도출·교차검증.
2. L993–998 `★Sommerfeld 동결의 유효 경계` — Mott 보정항 $\propto g'(E_F)(k_BT)^2$, 상대크기 $\mathcal O[(k_BT/E_F)^2]\sim0.03^2$, 천이중심서 가장 약함을 정직 명시.
3. L1029–1038 `★eV→J 단위 환산식`(eq:gunit) — $g_J=g_{eV}/e_V$, 곱하면 $1/e_V^2\approx4\times10^{37}$배 오류 경고(P4 코드 가드).
4. L1054–1066 `★T² 누적계수`(eq:U1T2) — $U_1(T)=U_1(T_0)+\frac{\Delta S_0}{F}(T-T_0)+\frac{a_e}{2F}(T^2-T_0^2)$, ½=∫a_eT'dT' 유래·단순곱 시 ½ 손실 경고.
5. L1123–1130 `★세 양의 구분` — 절대량 1.1k_B / 부분몰 0.18k_B / 게이트골 −46 J/mol·K 을 다른 척도로 못박아 상호검산 오용 방지.

**추가분 수치 전수 실측 검증(scratchpad/verify.py):**
- 게이트골 = **−45.66 J/(mol·K)** → tex "≈−46"·code docstring "−45.7"·V1010_PROBLEM_REPORT "−45.68" 전부 정합.
- $N_A k_B^2=R k_B$ 항등식 성립(단위 다리 정당).
- $1/e_V^2=3.90\times10^{37}$ → tex "≈4e37" 정확.
- 완전 metal $S_e/k_B=1.106$ → tex "≈1.1 k_B/atom" 정확.

**판정**: 추가분은 **오류·비약 0, 축1(G-derive) 강화**(교차검증 경로·유효경계 정직·단위 부호가드). P2 계획(`plans/2026-07-02-v1010-P2-ch1-textbook-plan.md` L8)이 "전자 엔트로피(Sommerfeld) 이론을 **교재급으로 정련**(완성도↑)"을 **명시 지시**했고, 그 산출이 바로 이 확장이다. **→ 물리 훼손 아님. P2/P5는 절을 깨뜨리지 않고 정련했다.**

### [MED·governance] I-2 — byte-lock mandate 와 "교재급 정련" 지시의 **내부 긴장**, 문서 미기재  (렌즈 (5)인계 / 축2 G-follow·프로세스 무결)

같은 P2 계획 L21(주의)은 "원본 Ch1 정정은 통합 시 master 직접(**전자엔트로피 절 등 byte-보존 확인**)"을 요구한다. 즉 **L8(정련=추가) ↔ L21(byte-보존) 이 한 계획서 안에서 상충**한다. v1.0.10은 이를 "원문 verbatim 유지 + 신규 삽입"으로 해소했으나 — 이 해소(byte-SHA 는 의도적으로 깨되 내용은 보존+증강)가 **어느 result·ledger에도 명문 기록되지 않았다.** FIX_LIST_v1011 A2가 "byte-identical·SHA 일치"를 계속 mandate로 걸어둔 채인데, v1.0.10 절은 SHA 불일치(178→233줄)다.
- **왜 문제**: 다음 세션이 "전자엔트로피 절 = SHA-locked" 규범을 문자 그대로 적용하면 v1.0.10의 정당한 확장을 "회귀/훼손"으로 오판할 수 있다(실제로 이번 검수 초점이 그 우려에서 발). 인계 무결성 = 결정의 **명문 승계**인데, "byte-lock 을 정련으로 대체" 결정이 인계 문서에 없다.
- **권고(진단만)**: v1.0.11 핸드오버 또는 ledger에 "전자엔트로피 절: v10까지 SHA-lock → v1.0.10 P2에서 additive 정련으로 전환(원문 verbatim 보존, +54줄 신규 rigor, 수치검증 완료)" 1줄 명기. **결함 등급은 MED(문서 정합)** — 물리·내용 손실은 0.

---

## Q2 — LCO 물리 인계: 코드 `LCO_MSMR_LIT` 어긋남 = 인계 손실 vs tier-C placeholder

### [강등·placeholder 확정] I-3 — 코드 어긋남은 **명문 라벨된 tier-C placeholder**, 인계 손실 아님  (렌즈 (4)보존·(5)인계 / 축1·축2)

**코드 실측(`Anode_Fit_v1.0.10.py` L623–640 `LCO_MSMR_LIT`):**
- dict1: U=3.930V(x≈0.75–0.95) — 전자항 없음.
- dict2: U=3.880V, **`'electronic':True, 'x_center':0.50, 'x_MIT':0.50, 'g_max_eV':13.0, 'dx_MIT':0.05`** — 전자항을 **중간 dict**에 **x_MIT=0.50**로 배정.
- dict3: U=4.050V(x≈0.35) — 전자항 없음.
- **T3(~4.17V) 부재**(3전이만).
- `_effective_dS_rxn`(L657–673): 전자항을 **T_ref=298.15서 동결한 상수 오프셋**으로 가산 → dS_eff T-무관 → ∝T·T² 곡률 미구현.

**이는 SPEC(x_MIT≈0.85·전자항 T1(MIT, U~3.90)·T3 존재·∝T)와 정면으로 어긋남.** 물리적으로 x=0.50은 order–disorder이지 MIT가 아니고, MIT는 코드 dict1(U=3.930, x 0.75–0.95)에 해당한다. 전자항이 **틀린 전이**에 붙어 있다.

**그러나 v9/v10 물리 인계는 tex에서 온전 생존:**
- `graphite_ica_ch1_v1.0.10.tex` 표 `tab:lco-staging`(L319–342): **T1(MIT) ~3.90 · x 0.94–0.75 · config+ΔS_e 게이트 ON · 전자항 "발현(핵심)" / T2 ~4.05 / T3 ~4.17–4.20 · 전자항 off** — SPEC 그대로.
- 게이트 절 eq:ggate(L1074–1075)·정당화(L1103)·그림(L1151)·분해(L1721) 전부 **x_MIT≈0.85·전자항 T1** 유지.

**코드 어긋남은 tex가 명문으로 격리·라벨:**
- 표 캡션 L325–329: "★코드 `LCO_MSMR_LIT` 시연값(U=3.930/3.880/4.050·**x_MIT=0.50·전자항을 중간 dict에 배정**)은 **tier-C placeholder**로, 본 표의 물리 anchor(T1 MIT~3.90·x_MIT≈0.85·T3~4.17)와 **별개**이며 round-trip 피팅으로 정합(피팅 시 전자항은 **T1=MIT dict로 재정렬**). 또한 현 구현은 ΔS_e를 T_ref서 동결…∝T의 T² 곡률(eq:U1T2)은 다온도 round-trip 단계 과제로 분리."
- 코드 주석도 이중 라벨: L621–622 "tier-C 시연 기본값 — round-trip 前 placeholder(실측 신뢰값 아님)" · L661–666 "전자항 T_ref 동결(단일-기준 근사)… Sommerfeld T-스케일·eq:U1T2 별도적분은 **P4 미구현·라벨**."

**독립 대조 — 선행 라운드도 동일 결론:** `docs/v1.0.10/V1010_PROBLEM_REPORT.md` §2(강등) = "클러스터 D: D1(x_MIT=0.50 배정)·D2(T3 부재)·D3(T_ref 동결→∝T 미구현) … Ch1 L325–327·FITTING_GUIDE Phase D가 tier-C·후속으로 **명문 라벨 → 결함 아님**." §3 = "전자엔트로피 골 −45.68(Ch1 −46) PASS 재확정."

**독립 대조 — 개정 계획도 정확한 SPEC 값으로 수리 예약:** `docs/v1.0.10/HANDOVER_v1.0.11.md` Phase 4.1(Step 21–25, L62–63) = "클러스터 D — LCO 실측 round-trip 피팅(**x_MIT=0.85·전자항 T1=MIT 재정렬·T3 4.17 추가**)·T_ref 동결 해제(func_dSe_molar T 전달·eq:U1T2 center-T_ref 별도적분 ½=a_e/2F)."

**판정**: 코드 어긋남은 (1) tex 캡션·코드 주석에 **in-line 이중 명문 라벨**, (2) 선행 검수가 **결함 아닌 강등**으로 분류, (3) 개정 계획이 **정확한 SPEC 값으로 수리 예약** — 3중으로 관리된 **tier-C placeholder**다. **인계 손실 아님**: v9 물리 anchor(x_MIT 0.85·T1·T3·∝T)는 tex 표·산문·그림·분해에 **손실 0으로 생존**. 코드는 피팅 前 시연 stub일 뿐이며 그 격차가 정직 공개돼 있다. **오적발 주의 대상**(코드 dict만 보고 "물리 인계 붕괴"라 결론하면 오판 — tex anchor·라벨·수리계획을 못 본 것).

### [MED·정직성 미세] I-4 — 코드↔tex ∝T 서술 잠재 모순은 **공개되어 무해**  (렌즈 (5)인계 / 축2)

tex 본문(L1047–1052·L1721)은 전자항 "유일하게 ∝T·다온도 분리식별"을 (정당하게) 서술하나, 코드는 T_ref 동결로 ∝T를 실제로 끄고 있다. 순수 코드↔문건 정합만 보면 모순이나 — I-3의 캡션 L327–329·코드주석 L665–666·분해절 예고 L1729–1738이 "현 구현=T_ref 동결 단일기준, ∝T·T²는 P4 과제"를 **명시 공개**한다. **→ 은닉된 text↔code 모순 없음.** tex의 ∝T는 *이론*(정확), 코드 동결은 *구현 단순화*(공개·수리예약). 축2(G-follow) 저하 없음(독자가 격차를 안내받음). 등급 MED이나 실질 무해, 별도 조치 불요(수리는 이미 Phase 4.1 예약).

---

## 무결 영역 (정독 근거 남김 — 빈통과 아님)

- **가법 직교성(v9 F8) 인계·강화**: tex L1707–1715가 v9 한 문장 F8을 (가)가산성($Z=Z_{config}Z_{elec}$ 인수분해·잔차0) + (나)무이중계산(중심표준값만/게이트골만) 2단으로 **확장 서술**. MIT 결합 몫도 정직 명시. → 축1 강화, 훼손 0. (base_v9 대응 절과 대조: 원 문장 보존 + 정련.)
- **ΔS_e<0 삽입기준 부호사슬**: eq:dSe/eq:dSegate leading −(L1015·1090)·박스·그림 파선·분해(L1718–1720) 전부 삽입기준 음부호 일관 — v9 A2-2 부호공존 규약 보존.
- **Sommerfeld 유도 (a)→(b)→(c)→(d)**: Fermi–Dirac 출발→정보엔트로피 합→열폭 동결(F1 가정 명시, L965–968)→C_e→S_e 적분, base_v9와 verbatim + eq:Sedirect 교차검증 추가. 유도 비약 0.
- **단위 다리(자리당 k_B→몰당 R)**: eq:dSemolar(L1022–1027) 보존 + eV→J 박스(신규) — F3(몰당 정정) 정신 계승·강화.
- **func_dSe_molar 코드**(L170–185): tex eq:dSegate 그대로 구현(÷EV_TO_J·leading −·몰당 R·k_B), docstring이 tex 검증값(−45.7≈−46) 상호참조. tex↔코드 함수형 정합.

---

## 가장 약한 1곳 (자기지목)

**I-2 (byte-lock↔정련 전환의 미기록).** 물리·수치로는 전자엔트로피 절이 무손상·강화됐음이 확정이나, **"v10까지 SHA-lock 이던 절을 v1.0.10 P2에서 additive 정련으로 전환"이라는 결정이 인계 문서에 명문화되지 않은 것**이 이 초점의 유일한 실질 인계-무결성 흠이다. FIX_LIST_v1011 A2의 "byte-identical" mandate가 문자 그대로 살아 있어, 미래 세션의 오판 위험(정당한 확장을 회귀로 착각)을 남긴다. 등급 MED·저비용(핸드오버 1줄)·물리 손실 0.

## 버전전환별 인계 판정 (초점 = 전자엔트로피 + LCO 물리)

- **v8→v9**: 전자엔트로피 절 **신규 도입(개선)** — Sommerfeld 유도·MIT 게이트·x_MIT 0.85·T1/T2/T3·∝T·F8 직교성. LCO 물리 SPEC 성립. (본 초점 = 도입 라운드, 보존 대상 이전.)
- **v9→v10**: 전자엔트로피 절 **byte-identical 보존(PASS·SHA 3c6fd631)** + broadening 복원(타 초점). LCO 물리 anchor 무손상. **보존.**
- **v10→v1.0.10**: 전자엔트로피 절 **additive 정련(내용 보존+강화, byte-SHA는 의도적 파기·미기록 = I-2 MED)** · LCO tex anchor **보존** · LCO 코드는 **tier-C placeholder(x_MIT0.50·T3부재·T_ref동결, 3중 명문라벨·수리예약 = I-3 강등, 결함 아님)**. **보존+개선**(단 governance 1건 MED).
- **→ v1.0.10 인계 판정**: 본 초점 = **인계 성공**. 물리·유도·수치 손실 0, 결함 CRIT/HIGH 0, MED 2(I-2 문서정합·I-4 무해), 강등 1(I-3).

## 5줄 요약

1. **초점** = 전자엔트로피 byte 보존 + LCO 물리 인계(x_MIT·T1/T3·∝T·직교성).
2. **인계 결함 수** = CRIT 0·HIGH 0·**MED 2**(I-2 byte-lock↔정련 전환 미기록 / I-4 코드-tex ∝T 모순은 공개되어 무해)·강등 1(I-3).
3. **최중대** = I-2 — 전자엔트로피 절이 v10 SHA-lock→v1.0.10 additive 정련(원문 verbatim+54줄 신규rigor, 수치 −45.66/1.106/4e37 전수검증 통과)으로 전환됐으나 그 결정이 인계 문서에 미기재(FIX_LIST A2는 여전히 byte mandate) → 미래 오판 위험. 물리 손실 0.
4. **두 축 유지** = 축1(G-derive) **강화**(교차검증·유효경계·직교성 2단·단위 부호가드) · 축2(G-follow) **유지**(코드-tex 격차 전부 명문 공개). degradation 없음.
5. **오적발 자기표시** = 코드 `LCO_MSMR_LIT`(x_MIT0.50·T3부재·T_ref동결)를 "물리 인계 붕괴"로 격상하지 **않음** — tex 표 anchor(x_MIT0.85·T1·T3)·캡션/주석 tier-C 라벨·HANDOVER Phase4.1 수리예약 3중 대조로 **tier-C placeholder(강등)** 확정. "종모양=결함 아님"류 오적발은 본 초점 밖(타 검수자 소관)이라 미판정.
