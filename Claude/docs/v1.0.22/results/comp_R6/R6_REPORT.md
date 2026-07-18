# R6 코드 구현 리포트 — `BlendedAnodeDQDV` 증축 + 게이트 검증

- 산출 창: v1.0.22 R6 코드 구현(Opus)
- 대상 파일: `Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py`(클래스 증축) · `Claude/docs/v1.0.22/test_gates_v1022.py`(게이트 증축)
- 명세 원천: `_sections/ch3v22_sec05_code.tex`(§3.5) · `ch3v22_sec03_blend.tex`(§3.3) · `ch3v22_sec02_cases.tex`(§3.2) · `ch3v22_notation.tex`
- 규율 준수: git 조작 없음 · tex 소스 미수정 · `Codex/` 미접근 · **기존 코드 경로 무수정**(아래 §5 무결성 확인) · 코드 스타일 = 기존 파일 관행 준수
- 최종 게이트 실행: `PYTHONIOENCODING=utf-8 python test_gates_v1022.py` → **exit 0**(전건 GREEN)

---

## 1. 구현 요지

문건 §3.5 doc-leads 요구명세의 블렌드 합성 클래스 `BlendedAnodeDQDV(f_Si, si_case)`를 **합성(composition)** 으로 구현했다. 기존 흑연 클래스 `GraphiteAnodeDischargeDQDV`를 상속이 아니라 두 host 인스턴스로 감싸, 공통 전위 축(= 공통-μ 물리의 코드 표현) 위에서 더한다.

**핵심 설계 (한 문장): 흑연(다수) host 가 전극 배경 `C_bg`를 1회 싣고(`Cbg=Cbg`), Si host 는 `Cbg=0`으로 둔다.** `f_Si=0` 이면 Si 전이 용량이 통째로 0 이 되어 Si host 반환이 순수 0 배열이고, `배열 + 0.0 = 배열`(IEEE)이라 흑연 단독 경로와 부동소수점까지 동일해진다. 이 배경-담지 위치 선택은 **"`C_bg` 전극 1회 가산"과 "`f_Si=0` bit-exact"를 동시에 만족시키는 유일한 구성**이다(배경을 블렌드가 따로 더하면 부동소수 결합법칙이 깨져 bit-exact 불가).

구현 물리:

- **관측 dQ/dV (eq:blend-dqdv)**: `dQ/dV = C_bg + Σ_host Σ_j Q_j^host ξ_j^host(1−ξ_j^host)/w_j^host` — 두 host 의 표준 진입점(`equilibrium`·`dqdv`·`curve`)을 같은 V 배열에서 평가해 합산.
- **공통-μ 전하 보존 (중심식 eq:blend-balance)**: `solve_U_oc` 가 두 host 전이를 한 저장조(pooled)로 묶어 `Σ_host Σ_j Q_j^host ξ_{eq,j}^host(U_oc,T) = Q x̄` 를 수치 유일근으로 푼다. 흑연 단독 반전의 이중합 한 줄 일반화이며, `U_oc` 는 음함수(정의상 implicit formulation).
- **용량 배분 (ssec:code-synth)**: 흑연은 native 용량 `Q_gr0` 를 그대로 유지(재스케일 없음 → bit-exact 보존), Si 는 `Q_Si = [f_Si/(1−f_Si)]·Q_gr0` 로 절대 스케일 → `Q_Si/(Q_gr0+Q_Si) = f_Si` 성립(검산: R6-G1 에서 `Q_Si/Q=0.300000`).
- **wt% 진입점 (C-052 범위 좌표 규약)**: `from_wt(m_Si, q_Si, q_gr, ...)` 이 `f_Si = m_Si q_Si / [m_Si q_Si + (1−m_Si) q_gr]` 로 질량 분율(선언·스윕 좌표)을 용량 분율(내부 변수)로 환산. 검산: `m_Si=0.30`(sic, q_Si=3117·q_gr=372) → `f_Si=0.782`(문건 "wt%→f_Si≈0–0.7" 정합).
- **Si 케이스 셋 3종**: `SI_ELEMENTAL_LIT`·`SIOX_LIT`·`SIC_LIT` = 표 tab:si-cases 의 tier 명기 시연값(신뢰값 아님, 피팅 override 전제 — `LCO_MSMR_LIT` 와 동일 지위).

구현 규모: `Anode_Fit_v1.0.22.py` **+348 줄**(순수 추가, 삭제 0) · `test_gates_v1022.py` **+201 줄**(R6 게이트 4종 + docstring/main 증축).

---

## 2. 게이트 실행 로그 (전문)

기존 게이트(G1 하위호환 · G2 B.2 회귀 · G3 θ_E bit-exact · n(T) 부록)는 **전건 GREEN 유지**되고, 그 위에 R6 블렌드 게이트 4종이 증축돼 전부 PASS 한다.

> ★번호계 주의(P3 항목 7 정합): 아래 로그의 `G1/G2/G3`(기존)과 `R6-G1/R6-G2/R6-G3`(신규 블렌드)은 **이름만 같을 뿐 별개 번호계**다. 기존 = v1.0.19 하위호환 / ch2_appB B.2 회귀 / θ_E bit-exact. 신규 = 문건 §3.5 codebox 의 블렌드 bit-exact / 스윕 연속성 / 용량 보존.

```
v1.0.19: /home/user/Project_Anode_Fit/Claude/docs/v1.0.19/Anode_Fit_v1.0.19.py
v1.0.22: /home/user/Project_Anode_Fit/Claude/docs/v1.0.22/Anode_Fit_v1.0.22.py
numpy 2.4.6, python 3.11.15
==========================================================================
G1: backward-compat  v1.0.22 vs v1.0.19  (new features all unspecified)
  compared arrays: 30  bit-exact(np.array_equal): True  max|diff|: 0.000e+00
  [aux] golden npz (13 arrays, other-machine capture): max|diff|=4.330e-15  bit-exact 1/13 (P0 env-noise ref 4.33e-15)
  G1 RESULT: PASS  (module-vs-module 0.000e+00 <= 1e-12; golden 4.330e-15 <= 1e-12)
==========================================================================
G2: regression reference values (ch2_appB B.2, display-precision match)
  U_oc [mV]                  value=+74.351141  display=74.4  doc=74.4  OK
  dU/dT complete [mV/K]      value=-0.203946  display=-0.204  doc=-0.204  OK
  dU/dT simple  [mV/K]       value=-0.133958  display=-0.134  doc=-0.134  OK
  dU/dT config  [mV/K]       value=-0.069988  display=-0.070  doc=-0.070  OK
  dS = F*dU/dT [J/mol/K]     value=-19.677727  display=-19.7  doc=-19.7  OK
  Qrev/I = -T*dU/dT [mV]     value=+60.806492  display=+60.8  doc=+60.8  OK
  round-trip [U(T+3)-U(T-3)]/6K = -0.203946 mV/K (display -0.204, doc -0.204); |FD-analytic| = 1.139e-05 uV/K (< 0.001) OK
  --- tab:worked per-transition intermediates (x=0.25, 298.15 K) ---
    sum Q_j g_j = 6.1771 /V (display 6.18, doc 6.18) OK
    j=0: xi=0.005(0.005) g=0.19(0.19) share=0.003(0.003) dS/F=+0.301(+0.301) config=-0.458(-0.458) OK
    j=1: xi=0.072(0.072) g=2.61(2.61) share=0.051(0.051) dS/F=+0.000(+0.000) config=-0.220(-0.220) OK
    j=2: xi=0.143(0.143) g=4.77(4.77) share=0.193(0.193) dS/F=-0.052(-0.052) config=-0.154(-0.154) OK
    j=3: xi=0.395(0.395) g=9.30(9.30) share=0.753(0.753) dS/F=-0.166(-0.166) config=-0.037(-0.037) OK
  --- tab:qrev 5-point (298.15 K, full columns) ---
    x=0.10: U_oc=43.5(43.5)  dU/dT=-0.307(-0.307)  dS=-29.6(-29.6)  Qrev/I=+91.5(+91.5)  OK
    x=0.25: U_oc=74.4(74.4)  dU/dT=-0.204(-0.204)  dS=-19.7(-19.7)  Qrev/I=+60.8(+60.8)  OK
    x=0.50: U_oc=109.0(109.0)  dU/dT=-0.089(-0.089)  dS=-8.6(-8.6)  Qrev/I=+26.6(+26.6)  OK
    x=0.75: U_oc=148.8(148.8)  dU/dT=+0.044(+0.044)  dS=+4.3(+4.3)  Qrev/I=-13.2(-13.2)  OK
    x=0.90: U_oc=195.2(195.2)  dU/dT=+0.218(+0.218)  dS=+21.0(+21.0)  Qrev/I=-64.9(-64.9)  OK
  --- derived A: 175-pt full-range complete vs FD + 3-boundary continuity ---
    complete vs FD: max=2.948e-07 mV/K  mean=4.290e-08 (gate <= 0.01 mV/K, display precision) OK
    [ref] simple vs FD: max=0.2273 mV/K (doc grid-max ~0.18; span-dep)
    [ref] config span: [-0.227, +0.139] mV/K (doc ~[-0.21,+0.14]; span-dep)
    boundary 1: x_mid=0.453  dU/dT=-0.1100 mV/K in (-0.166,-0.052)? True  local max step=2.3 uV/K (< 25.0) OK
    boundary 2: x_mid=0.643  dU/dT=-0.0207 mV/K in (-0.052,+0.000)? True  local max step=2.9 uV/K (< 25.0) OK
    boundary 3: x_mid=0.817  dU/dT=+0.1018 mV/K in (+0.000,+0.301)? True  local max step=6.2 uV/K (< 25.0) OK
    [ref] global max per-step change: 13.5 uV/K (175-pt grid; original 181-pt verification: max 13 uV/K/step)
  G2 RESULT: PASS
==========================================================================
G3: theta_E bit-exact  (unspecified path == pre-correction code)
  v1.0.22(no theta_E) vs pre-correction variant: arrays=30  bit-exact=True  max|diff|=0.000e+00  OK
  effectiveness: theta_E=700K on tr[3] -> T_ref outputs equal: True; T=318.15K max|diff|=2.374e-03 (>0) OK
    C-62 dDU_vib/dT @T=278.15: -3.7382 uV/K (display -3.74, doc -3.74) OK
    C-62 dDU_vib/dT @T=298.15: +0.0000 uV/K (display +0.00, doc +0.00) OK
    C-62 dDU_vib/dT @T=318.15: +3.7000 uV/K (display +3.70, doc +3.70) OK
    C-62 dDU_vib/dT @T=348.15: +9.1378 uV/K (display +9.14, doc +9.14) OK
  G3 RESULT: PASS
==========================================================================
APPENDIX: n(T)=n+n_T1*(T-T_ref) propagation evidence (ch1_appB)
  n_T1=0.0 == absent (value bit-exact) equilibrium_298: True
  n_T1=0.0 == absent (value bit-exact) dqdv_dis_0.2: True
  n_T1=0.0 == absent (value bit-exact) entropy_V: True
  n_T1=0.0 == absent (value bit-exact) Uoc_x: True
  n_T1=5e-4: dw/dT analytic=9.901445354e-05 V/K  centered-FD=9.901445354e-05  rel-diff=2.67e-14 (<1e-9) OK
  n_T1=5e-4 round-trip @x=0.25: FD=-0.214379 analytic=-0.214379 mV/K  |diff|=1.670e-05 uV/K (<1e-2) OK
  n(T) RESULT: PASS
==========================================================================
R6-G1 (blend): f_Si=0 bit-exact vs graphite-only  (eq:si-code-bitexact)
  equilibrium      array_equal=True  max|diff|=0.000e+00
  dqdv_dis_I0.02   array_equal=True  max|diff|=0.000e+00
  dqdv_dis_I0.2    array_equal=True  max|diff|=0.000e+00
  dqdv_dis_I1.0    array_equal=True  max|diff|=0.000e+00
  dqdv_chg_I0.02   array_equal=True  max|diff|=0.000e+00
  dqdv_chg_I0.2    array_equal=True  max|diff|=0.000e+00
  dqdv_chg_I1.0    array_equal=True  max|diff|=0.000e+00
  curve_dis_0.2C   array_equal=True  max|diff|=0.000e+00
  solve_U_oc       array_equal=True  max|diff|=0.000e+00
  effectiveness: f_Si=0.3 changes equilibrium (max|diff|=1.479e+00>0) & Q_Si/Q=0.300000(=0.3): True
  R6-G1 RESULT: PASS  (worst bit-diff=0.000e+00)
==========================================================================
R6-G2 (blend): m_Si sweep continuity on (0,0.30] wt%  (f_Si via C-052)
  f_Si range over m_Si∈(0,0.30]: [0.0404, 0.7822] (doc: wt%→f_Si≈0–0.7)
  finite curves: True
  adjacent sup-diff: max=2.9298e-01 mean=2.0759e-01 max/mean=1.41 (<5.0 no-jump): True
  refinement max-step: n=60:2.9298e-01 2n:1.4701e-01 4n:7.3637e-02  ratios=0.502,0.501 (~0.5 Lipschitz): True
  R6-G2 RESULT: PASS
==========================================================================
R6-G3 (blend): capacity conservation  int(dQ/dV - Cbg) dV = Q_gr + Q_Si
  f_Si=0.00: int=0.969999999 Q=0.970000000 (Q_gr=0.9700,Q_Si=0.0000) rel=1.48e-09 (<=1e-06; trunc<=2.1e-09) OK
  f_Si=0.10: int=1.077777778 Q=1.077777778 (Q_gr=0.9700,Q_Si=0.1078) rel=2.25e-10 (<=1e-06; trunc<=2.1e-09) OK
  f_Si=0.30: int=1.385714285 Q=1.385714286 (Q_gr=0.9700,Q_Si=0.4157) rel=6.74e-10 (<=1e-06; trunc<=2.1e-09) OK
  f_Si=0.50: int=1.939999998 Q=1.940000000 (Q_gr=0.9700,Q_Si=0.9700) rel=1.12e-09 (<=1e-06; trunc<=2.1e-09) OK
  R6-G3 RESULT: PASS
==========================================================================
R6 coverage: 3 si_case build/run + SiOx gap warning (no silent fabrication)
  si_case=elemental finite=True gaps=[] warned=False(expect False) OK
  si_case=siox      finite=True gaps=['평균 전위 U_avg (절대 mV 미확보 — 표 각주 c)', '히스테리시스 절대 mV (미확보 — 표 각주 f)'] warned=True(expect True) OK
  si_case=sic       finite=True gaps=[] warned=False(expect False) OK
  boundary plastic_hysteresis_loop() -> NotImplementedError: True
  boundary nonadditive_correction() -> NotImplementedError: True
  R6 coverage RESULT: PASS
==========================================================================
>>> SUMMARY: G1 PASS (module max|d|=0.0e+00, golden max|d|=4.3e-15, bit-exact=True) | G2 PASS | G3 PASS | n(T) PASS
>>> R6 BLEND (§3.5): R6-G1 PASS | R6-G2 PASS | R6-G3 PASS | coverage PASS
```

### 게이트 판정 기준(명시)

| 게이트 | 판정 기준 | 실측 결과 |
|--------|-----------|-----------|
| **R6-G1** bit-exact | `f_Si=0` 에서 9 진입점(equilibrium·dqdv 6종(dis/chg×3 C-rate)·curve·solve_U_oc)이 흑연 단독과 `np.array_equal` | 전건 `max|diff|=0.0` + 발효(f_Si=0.3 이 곡선 변경·`Q_Si/Q=0.3`) |
| **R6-G2** 스윕 연속성 | `m_Si∈(0,0.30]` 균일 그리드에서 (i)전부 유한 (ii)인접 sup-편차 `max/mean<5`(점프 없음) (iii)그리드 2배 세분 시 최대 스텝 비 ∈[0.40,0.62](Lipschitz 연속의 수치 서명 ~0.5) | finite=True · max/mean=1.41 · 세분 비 0.502→0.501 |
| **R6-G3** 용량 보존 | `∫(dQ/dV−C_bg)dV = Q_gr+Q_Si`, 검사 창 = 전 전이 `U_j±20·w_j`, 상대 공차 ≤ 1e-6, 잘림 상한 `Σ Q_j e^{−20}` | rel ≤ 1.5e-9(전 f_Si; 잘림 지배) |
| **R6 coverage** | 3 케이스 구성·유한 실행 + SiOₓ 공백 경고 발효 + GS-1/GS-2 `NotImplementedError` | 전건 OK |

**G2 "점프 없음" 판정 근거**: 참 불연속이라면 그리드를 세분해도 어떤 인접 쌍이 여전히 점프 전폭을 가로질러 최대 스텝이 안 줄어든다(비 ≈ 1.0). 연속(Lipschitz)이면 스텝이 그리드 간격에 비례해 2배 세분마다 절반이 된다(비 ≈ 0.5). 실측 0.502·0.501 → 연속 확정. 이 검사는 공통-μ 완전 동시반응 **1차 근사 안에서의** 연속성이다(유한 율속 비가산은 범위 밖 = GS-2).

---

## 3. 명세 대응표 (§3.5 조항 ↔ 코드 위치)

파일 `Anode_Fit_v1.0.22.py` 기준(행 번호는 본 산출 시점).

| 문건 조항 | 요구 | 코드 위치 | 검증 |
|-----------|------|-----------|------|
| eq:si-code-bitexact (§3.5 ssec:code-contract) | `f_Si=0 ⟹ Blend ≡ Graphite` bit-exact | 합성 설계(두 host 합·Si 0배열): `equilibrium`(L1237)·`dqdv`(L1246)·`curve`(L1258)·`solve_U_oc`(L1270) | R6-G1 |
| ssec:code-synth — 용량 배분 | `Q_Si=f_Si Q`·`Q_gr=(1−f_Si)Q` | `__init__` 용량 배분 블록(L1122~, "용량 배분" 주석) | R6-G1(Q_Si/Q=0.3)·R6-G3 |
| ssec:code-synth — 공통 V_n | 두 host 를 같은 전위 축에서 평가·합 | `equilibrium`/`dqdv`/`curve` 두 host 합(L1237–1268) | R6-G1/G3 |
| ssec:code-synth — `C_bg` 전극 1회 | host별 중복 가산 금지 | 흑연 host `Cbg=Cbg` / Si host `Cbg=0.0`(`__init__` "두 host 인스턴스" 블록) | R6-G3(배경 빼고 적분) |
| eq:blend-balance (§3.3, 중심식) | 공통-μ 이중합 전하 보존 → 음함수 `U_oc` | `solve_U_oc`(L1270) + pooled `_balance_host`(`__init__` "pooled host" 블록) | R6-G1(solve_U_oc bit-exact) |
| eq:blend-dqdv (§3.3) | `dQ/dV = C_bg + host 이중합` | `equilibrium`(L1237)·`dqdv`(L1246) | R6-G3 |
| eq:blend-limit (§3.3, f_Si→0 회수) | Si 이중합 통째 소거 | `si_scale=0.0 (f_Si==0)`(`__init__`) → Si Q 전부 0 | R6-G1 |
| ssec:code-caseset — `si_case` 셋 | `'elemental'`·`'siox'`·`'sic'` | `SI_ELEMENTAL_LIT`(L999)·`SIOX_LIT`(L1009)·`SIC_LIT`(L1021)·`SI_CASE_SETS`(L1033) | R6 coverage |
| ssec:code-caseset — SiOₓ 공백 계승 | 평균 전위·절대 히스 placeholder/None, 임의값 금지 | `SIOX_LIT`(L1009, ⚠ CAUTION 주석)·`SI_CASE_GAPS`(L1042)·생성 경고(`__init__`) | R6 coverage(warned=True) |
| §3.5 codebox G1/G2/G3 | 요구 게이트 3종 | `gate_R6_G1`(test L439)·`gate_R6_G2`(L485)·`gate_R6_G3`(L529) | 실행 로그 §2 |
| warnbox GS-1 (기계 히스) | 응력 결합은 오프셋 훅만·소성 폐합 미구현 | `si_stress_offset` 훅(`__init__`)·`plastic_hysteresis_loop`(L1298, NotImplemented) | R6 coverage |
| warnbox GS-2 (비가산) | 공통-μ 1차 근사까지·비가산 미구현 | `nonadditive_correction`(L1310, NotImplemented)·`dqdv` docstring GS-2 명시 | R6 coverage |
| §3.3 각주 C-052 (범위 좌표) | wt% 선언·스윕 ↔ 내부 f_Si 환산 | `from_wt`(L1203, `f_Si=m q_Si/[m q_Si+(1−m)q_gr]`) | R6-G2(wt% 스윕) |
| §3.2 tab:si-cases (tier 시연값) | tier 명기 시연값만·창작 금지 | `SI_*_LIT`(L999–1030, 출처·tier 주석)·`SI_SPECIFIC_CAPACITY`(L1051) | — |
| §notation (기호 계약) | `f_Si`·`m_Si`·`Q_gr/Q_Si/Q`·`C_bg`·`si_case` | 클래스 속성 `f_Si·Q_gr·Q_Si·Q·Cbg·si_case` + `from_wt(m_Si)` | — |

---

## 4. 미구현 / placeholder 목록 (정직 기록 — 조용한 날조 금지)

문건이 명시한 공백을 **코드도 침범하지 않는다**. 아래는 전건 정직 기록이다.

### 4-1. 명시적 코드 경계(요청 시 `NotImplementedError`)

| 항목 | 문건 근거 | 코드 표현 |
|------|-----------|-----------|
| **GS-1 소성 히스 폐합** | §3.5 warnbox·ssec:si-lc-gap | `plastic_hysteresis_loop()` → `NotImplementedError`. 응력 결합은 선택적 `si_stress_offset(=Λ_σ·σ_h [V])` 전이 중심 오프셋 훅으로만 노출(경로 의존 `σ_h` 는 사용자 입력). |
| **GS-2 유한 율속 비가산** | §3.5 warnbox·ssec:si-blend-gs2 | `nonadditive_correction()` → `NotImplementedError`. 합성은 공통-μ 완전 동시반응 1차 근사(평형 층)까지. 구간별 host 전환·비가산은 동역학 층(범위 밖). |

### 4-2. tier-C placeholder / 공백값(임의값 아님 — 계열 범위 앵커 + 경고)

| 케이스·항목 | 상태 | 처리 |
|-------------|------|------|
| **SiOₓ 절대 평균 전위** (`SIOX_LIT['U']`) | §3.2 표 각주 c "확인 필요"(순수 SiOₓ 1차 문헌 mV 미특정) | placeholder `0.300 V`(원소 Si 계열 범위 0.2–0.5 V 앵커) + ⚠ CAUTION 주석 + `SI_CASE_GAPS['siox']` 등재 + `f_Si>0` 생성 시 경고. 임의값 아님을 코드·주석에 명시. |
| **SiOₓ 히스테리시스 절대 mV** | §3.2 표 각주 f "확인 필요"(정성 저감만, 절대 mV 미확보) | Omega/gamma 미부여(히스 비활성) + `SI_CASE_GAPS['siox']` 등재 + 경고. |
| **Si–C tier-B 순환값** (lee_sic2025) | §3.2 ssec:si-sic "서지만 확정, 정량값 확인 필요" | demo 파라미터(U·w·Q)에 무관 → 경고 제외, `SIC_LIT` 주석으로만 기록. |
| **Si 계열 전이 중심·폭 절대값** | §3.2: 케이스 리스트 = 곡선 기술 성분(≠ 물리 상전이), tier-C 시연값 | `SI_*_LIT` 전건 "신뢰값 아님, 피팅 override 전제" 주석(= `GRAPHITE_STAGING_LIT`·`LCO_MSMR_LIT` 동일 지위). Si 열역학 엔트로피(dS_rxn)는 시연 셋에서 미부여(`entropy` Si 기여=0 — §3.2 thermal 공백 정합). |

### 4-3. 본 R6 범위 밖(§3.5 미요구 — 후속)

- 블렌드 `entropy_coefficient`/`reversible_heat`(발열) 진입점: §3.5 는 dQ/dV 합성·전하 보존만 요구. Si 열역학 dS 가 공백이라 블렌드 발열은 미구현(흑연 단독 경로는 기존대로 유효). 필요 시 pooled `_balance_host` 재사용으로 확장 가능.
- 구간별 host 전환·반응전류 배분 모형(ai_composite2022 계열): 마스터플랜 Non-goals(후속 버전).

---

## 5. 배포 루틴 (code-style 스킬 2-4)

### 5-1. 변경 구획 목록

| 파일 | 구획 | 변경 | 사유 |
|------|------|------|------|
| `Anode_Fit_v1.0.22.py` | `# R6 블렌드 음극 확장`(L975~) | **신규 추가**(+348) | §3.5 요구명세 구현. `GRAPHITE_STAGING_LIT` 뒤·`__main__` 앞 삽입. |
| `test_gates_v1022.py` | 모듈 docstring | 증축 | R6 게이트 3종 서술 추가(별개 번호계 명시). |
| `test_gates_v1022.py` | 상수 블록 + `_trapz` 별칭 | 신규 추가 | R6 게이트 상수·numpy 2.0 `trapezoid` 호환. |
| `test_gates_v1022.py` | `gate_R6_G1/G2/G3`·`gate_R6_coverage`(L439~) | 신규 추가(+201) | R6 게이트 하네스. |
| `test_gates_v1022.py` | `main()` 요약·exit | 최소 수정 | R6 게이트 호출·전건 AND exit 반영. |

### 5-2. 무결성 확인 (기존 코드 경로 무수정 원칙)

- `Anode_Fit_v1.0.22.py`: **삭제 0줄**(git diff 확인) — `GraphiteAnodeDischargeDQDV`·`LCOCathodeDQDV`·기존 함수·`GRAPHITE_STAGING_LIT`·`LCO_MSMR_LIT`·`__main__` 자기검증 전부 byte-불변. 모듈 `__main__` 자기검증 실행 = `overall OK: True`(exit 0).
- `test_gates_v1022.py`: 기존 게이트 함수(`gate_G1`·`gate_G2`·`gate_G3`·`check_nT`·`output_set`·`compare_sets`·`golden_outputs`·`load`) 로직 불변, 삭제 콘텐츠 없음. `main()` 만 R6 호출·요약·exit 증축.
- **불가피한 기존 경로 수정: 없음.** 게이트는 전부 신규 경로만으로 GREEN 달성.
- 테스트 백박스 접근: `gate_R6_G3` 이 창 산정에 `bl._balance_host._n_factor(...)` 사용(폭 `w=n(T)·RT/F` 복원용). 테스트 한정 화이트박스이며 코드 모듈은 불변.

### 5-3. 10회 검증 결과 요약 (이상 없음)

고정 5: (1)문법·구문 = 두 파일 `py_compile` OK·전 게이트 실행. (2)상태 마커 정합 = ⚠ CAUTION(SiOₓ placeholder·GS-1/GS-2)·★(설계 계약)이 실제 구현 상태와 일치(공백은 실제 공백, 경계는 실제 미구현). (3)후속 구획 연쇄 = 기존 클래스 시그니처 무변경(순수 추가). (4)문서화 완결 = 클래스+전 메서드 docstring·데이터셋 출처/tier 라벨·placeholder 주석 완비. (5)인터페이스 호환 = 기존 API 불변(diff 삭제 0).

가변 5(본 작업 위험 초점): (6)**부동소수 결합법칙 bit-exact** = R6-G1 9진입점 `max|diff|=0.0`(두 host 합+Cbg 담지 위치 설계). (7)용량 회계 = `Q_Si/Q=0.300000`·G3 rel≤1.5e-9. (8)데이터 미변조 = Si 셋 얕은 복사 후 스케일·`SI_*_LIT`/`GRAPHITE_STAGING_LIT` 원본 불변. (9)공백 정직성 = SiOₓ 경고 발효·GS-1/GS-2 `NotImplementedError`(coverage 게이트). (10)수치 강건성 = `f_Si∈[0,1)` 가드(1/(1−f_Si) 발산 차단)·Si 무동역학 → `0.0×finite=0.0`(0×inf 없음)·전 곡선 유한.

### 5-4. 후속 작업 안내(사용자·후속 버전)

- Si 케이스 시연값은 **피팅 override 전제**(round-trip). 실측 피팅 시 `SI_*_LIT` 또는 생성자 `si_transitions=` 로 교체.
- SiOₓ 절대 평균 전위·히스 mV 확보 시 placeholder 대체(현재 경고로 표식).
- 블렌드 발열·구간별 host 전환은 §3.5 범위 밖(후속) — 필요 시 별도 phase.

---

## 6. 재현

```bash
cd /home/user/Project_Anode_Fit/Claude/docs/v1.0.22
PYTHONIOENCODING=utf-8 python test_gates_v1022.py   # exit 0 (기존 4 + R6 4 전건 GREEN)
PYTHONIOENCODING=utf-8 python Anode_Fit_v1.0.22.py   # 모듈 자기검증 overall OK: True
```
