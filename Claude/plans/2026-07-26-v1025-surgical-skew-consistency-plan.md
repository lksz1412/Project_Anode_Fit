# v1.0.25 Plan — 국소 수정판 (@2 비대칭 opt-in + 문건↔코드 정합 6건)

> **성격**: 전문 재작성 아님. **수정될 부분만 국소 수정 + 그 수정에 연계돼 바뀌어야 할 파트만 찾아 보완**하는 국소 버전업.
> **원천**: 이번 세션 실측 검증(SINTEF Zenodo 20086298 gr/si/sigr + 독립셀 gr_B·gr_Dhold·si_A·si_Chold + O'Regan/MJ1 후보) · 검수의견 4건(A~E) · @1~@5 재검증.
> **양식**: [[feedback_plan_template_11sections]]. **게이트 = 확인 가능 조건** ([[feedback_gate_design_principle]]).
> **집행 주체**: 본 계획서대로의 수정은 **Fable 5.0 서브세션**이 수행(사용자 지시 2026-07-26). 본 세션(Opus)은 계획·게이트·검수만.

---

## 확정 (사용자 2026-07-26)

- **D-A**: **@2 비대칭 커널을 넣는다** — 단 **opt-in**(전이 dict `alpha` 키, 부재=1.0=현행 bit-exact). 기본 곡선 무변경.
- **D-B**: **갤러리(gallery)는 opt-in 유지** — 기본 전이 수 승격 X(골든 bit-exact 보존). `GRAPHITE_STAGING_MSMR6_LIT` 존치 + Si opt-in 셋 추가.
- **D-C**: **regsol/@1/@3/@4 커널 배제** — @3 는 gallery 세분에 열등(실측). regsol 평형커널 경로는 **코드에서 완전 삭제**(DG-1(b) 확정 — 아래). 문건의 해석적 유도(`eq:sifr-kernel`·`eq:sifr-blend`)는 유효 물리로 **보존**하되 "미채택·코드 미구현" 지위를 명기. Ω 파라미터 자체는 히스테리시스/장벽·§7 상성격 판정용으로 **전량 존치**.
- **D-D**: **국소 수정 원칙** — 물리 골격·식 번호·`\label`·변수명·한글 표현 불변. 신규는 전부 additive·부재 시 bit-exact.
- **DG-1 확정 = (b) 완전 삭제** (사용자 2026-07-26 "regsol 삭제"). 상세 = §10.
- **DG-2 확정 = (a) 파일명 유지** (사용자 2026-07-26 "파일명을 왜 바꿔? 버전명만 바꿔주면 되는거 아니냐?"). 상세 = §10.

---

## Summary

v1.0.24.1 은 물리·수치가 매우 견고하나(검수: 그림·표 수치 재현 전건 일치, 게이트 4종 GREEN), **문건이 boxed 식으로 선언한 것을 코드가 다르게 계산하는 정합 결함 4건**과, **실측이 뒤집은 판단 2건**이 있다. v1.0.25 는 이를 **국소 수정**한다:

1. **@2 비대칭 종(skew-logistic)** 을 opt-in 으로 추가 — 실측에서 흑연 R² 0.97702→0.98078, 벨리역 RMSE 0.640→0.518. `alpha` 부재=현행 bit-exact.
2. **B: 인과 기억 적분 하한을 −∞ 로 복원** — 문건 `eq:lag` 이 유도한 자연 경계가 코드에서 격자 시작점에 묶여 있어 평가창 의존(100%)이 생김. 5·$L_V$ pad 로 0.001%.
3. **C: 물리 상수 SI 통일** — 문건 25.693 mV vs 코드 25.691 mV.
4. **E: §5b 의 $w_\mathrm{eff}$ "델타로 수렴·연속화" 문장 정정** — FWHM 은 $\lambda$ 가 아니라 $\lambda^{3/2}$(수치 확인, 최대 30배 과대). 코드의 binodal 불연속 전환과도 어긋남.
5. **@3/regsol 강등** — Ch3 boxed `eq:sifr-kernel`·`eq:sifr-blend` 를 "추가 후보"로. gallery 세분이 같은 개형을 더 물리적으로 설명(전이 세분 시 @3 순효과 +0.97%p→−0.53%p 역전).
6. **배경·데이터 정직화** — $C_\bg$ = 창-국소 상수 근사 명기. 레포 데이터의 프로토콜 혼용(`gr.csv`=p-ocv, `si.csv`=p-ocvhold) 정정.

**연계 보완의 핵심 = @2**: 커널 한 줄이 아니라 §5(peak 식)·§7(broadening 3출처 분해)·§18(α↔$L_V$ 식별)·Ch3 §3.2b(envelope 비대칭 서술)·부록 B(코드맵)까지 연쇄한다. 이 연쇄를 빠짐없이 잇는 것이 본 버전의 실질 작업이다.

---

## Current Ground Truth (이번 세션 실검증 — 무근거 값 0)

**게이트·정합**
- v1.0.24.1 코드 = `v1.0.24/` 와 byte-identical, LF sha256 `f230f59b…`(ARCHIVE_NOTE 주장 확인). 식 맞음.
- 게이트 전건 GREEN: `test_gates_v1024`(G1 골든 bit-exact max|d|=0) · `_reflect` 4/4 · `_selfconsistent` 5/5.
- **A/B 패치 시제품**(scratchpad, 원본 미변경)으로 게이트 전건 재통과 확인 — 골든 bit-exact 0.0 유지.

**@1~@5 재검증(흑연 gr.csv 300점, 피크·벨리 개형 지표)**
| 조합 | R² | 피크역 RMSE | 벨리역 RMSE | 판정 |
|---|---|---|---|---|
| 기준 5전이 로지스틱 | 0.97090 | 4.851 | 0.788 | — |
| @5 7전이(gallery) | 0.97702 | 4.708 | 0.640 | ✅ |
| @5 9전이 | 0.97890 | 4.639 | 0.560 | ✅ |
| @1 near-delta(regsol) | 0.97436 | 4.772 | 1.063 | ❌ 무익·느림 |
| @3 regsol(혼합/전역) | 0.95~0.97 | ↑ | +34%(벨리) | ❌ 악화 |
| @4 U 고정 | **0.93215** | **8.004** | 0.800 | ❌ 유해 |
| **@2 비대칭3(skew)** | **0.98078** | **4.527** | 0.518 | ✅ 최대 이득 |
| @2+광폭배경 | 0.98178 | 4.542 | **0.422** | ✅ |

**@3 역전 규명(블렌드 sigr)**
- 전이 수 고정(흑연4+Si3, v1.0.24 당시 조건): @3 순효과 **+0.97%p** (원 `ablation_result.json` 재현).
- 전이 수 승격(흑연7+Si7): @3 순효과 **−0.53%p**. → @3 이득은 "전이 수 부족의 우회"였고 gallery 세분과 중복. gallery 가 이김.

**전이 세분 = gallery(곡선 표현)이지 상(phase) 아님**
- 7·9전이 피팅 U 가 전부 기존 3피크 위치(105·141·227 mV)에 ΔU<12mV 근축퇴 쌍으로 붙음(문헌 ad2061 MSMR gallery 관용 = 한 물리 peak 을 폭 다른 두 로지스틱으로).
- 조건 의존성 실측: 실리콘 0.43–0.46 V feature 가 p-ocv 엔 없고 hold 엔 2개(c-Li₁₅Si₄ 결정화). 흑연 검출 피크 수 prominence 따라 3→4→5. **XRD 상 수(4 staging, 두-상 2)는 불변**.

**배경**
- 4셀·2프로토콜 전건에서 dQ/dV 가 0.3–0.9 V 에서 단조 감쇠(평균의 230%, 셀 간 일치). 상수 아님·선형도 부족(곡률).
- 단 광폭항 단독 대체는 흑연 악화(0.97702→0.97415, 감쇠구간이 피팅 창 밖). **@2 와 함께일 때만 이득**.

**데이터**
- 레포 `gr.csv`=gr_A(**p-ocv**), `si.csv`=si_Dhold(**p-ocvhold**) — 프로토콜 혼용. 같은 7전이로 p-ocv 0.9770 → p-ocvhold 0.9945, 피크역 RMSE 4.708→2.701 → 불일치의 상당 부분이 데이터의 비평형 잔여.
- 독립 재현성 양호: gr_B 0.9770(레포와 동일), si_A/si_Chold 0.998–0.999.

---

## Phase Range (chapter→Phase→step, cumulative)

| Phase | 이름 | Steps | 주체 |
|---|---|---|---|
| P0 | v1.0.25 골격 복제·baseline GREEN·변경대장 확정 | 1–4 | Fable |
| P1 | 코드 국소 수정(C1 @2·C2 pad·C3 상수·C5 regsol 강등 라벨·C6 Si gallery opt-in) + 게이트 신설 | 5–12 | Fable |
| P2 | 문건 1차 국소 수정(@2 연계: §5·§7·§18 / E: §5b·Part T / C_bg wording) | 13–20 | Fable |
| P3 | 문건 2차 연계 보완(Ch3 @3 강등·cross-ref·부록 B·마감문서·검증문서) | 21–27 | Fable |
| P4 | 통합 검증(게이트 전건·빌드 GREEN·실측 재현·doc↔code 감사) + MERGE_READINESS·HANDOVER | 28–31 | Fable→Opus 검수 |

---

## Non-goals (절대 하지 않는다)

- ★**전문 재작성 X**. 물리 서사·유도 사슬·식 번호·`\label`·`\eqref/\ref/\cite` 키·변수명·한글 표현 불변.
- ★**기본 전이 수 승격 X** — gallery 는 opt-in 유지(D-B). 기본 데이터셋(`GRAPHITE_STAGING_LIT`·`SI_*_LIT`·`LCO_MSMR_LIT`) 무변경 → 골든 bit-exact 보존.
- ★**@2 를 "새 물리·새 상"으로 주장 X** — 아래 §Assumptions 의 정직 프레임(phenomenological·envelope 대안·tier-C) 준수.
- **regsol/@1/@3/@4 를 채택식으로 승격 X**. Ω 파라미터 자체(히스 gap·$\Delta H_a^\eff$)는 존치.
- **다입자/PSD convolution·dQ/dV→분포 역산 X**(v1.0.24 Non-goal 승계).
- **LCO 전자항 T-의존·다온도 정량 X**(회사 데이터 위임, Task #38).
- **새 공개 데이터셋 상시 편입 X** — 본 세션 검증분(gr_B·gr_Dhold·si_A·si_Chold)은 `FIT_CHECK` 근거로만 등재, 상시 피팅 파이프라인 증설 아님.

---

## Implementation Changes — 변경 대장(Change Ledger)

각 변경 = **primary edit + 연계(cascade) 보완 + 게이트**. 이것이 "수정될 부분 + 연계 보완"의 전부이며, 이 표 밖은 건드리지 않는다.

| ID | Primary edit (코드/문건) | 연계 보완(cascade) | 게이트 |
|---|---|---|---|
| **C1** @2 비대칭 | 코드: `func_dxi_eq(z,α,w)` 신설 = 실제 미분 종; `alpha` 전이키(부재=1.0); `equilibrium`·`dqdv`·`entropy_coefficient`·`solve_U_oc` 의 peak/g_j 를 `func_dxi_eq` 경유로 통일 | 문건 §5: skew peak boxed 식 신규(`eq:skewpeak`, α=1→`eq:eqpeak` 회수 명기)·§7: broadening 3출처 분해에 "α=평형 비대칭(전류·η 무관)" 축 추가+① 과 구분·§18: α↔$L_V$ 식별 축퇴 가드·Ch3 §3.2b: "비대칭=envelope 전용" 서술을 "envelope 또는 α(파라미터 효율 대안)"로 완화·부록 B `tab:symcode`/`tab:inputs`: `alpha` 행 | G-α1 bit-exact·G-α2 면적·G-α3 C¹·G-α4 축퇴 |
| **C2** 인과기억 pad(B) | 코드: `_causal_pad(V,L)` 신설; `dqdv` 로지스틱·ratio·regsol 세 경로 모두 진행방향 5·$L_V$ pad 후 절단 | 문건 §1.4·§9: "점별 평가"의 꼬리항 한정 각주(꼬리는 이력 적분이라 진행방향 과거를 pad)·부록 E 코드맵: `_causal_pad` 행 | G-창 불변성·면적·C¹·골든 bit-exact |
| **C3** 상수 SI(C) | 코드: `R_SI=8.314462618`·`F_SI=96485.33212` + `use_si_constants()` **opt-in**. 기본은 레거시 `R=8.314`·`F=96485.0` 유지 — ★**집행 정정**: 계획 원안의 "즉시 교체"는 골든 bit-exact 게이트(G1 max\|d\|=0)와 **수학적으로 양립 불가**(상수가 바뀌면 모든 값이 바뀜)라 opt-in 으로 집행 | 문건: 회귀 기준 수치(25.693·74.4mV·−0.204 등) 재평가 후 표시 정밀도 내 정합 확인 + **opt-in 지위 각주**. SI 발효 시 −0.204/−0.134/−0.070 mV/K·+60.8 mV·25.693 mV **불변**, `U_oc(x̄=0.25)` raw 74.3511→74.3497 mV(−1.4 µV·물리 불변)이나 `.1f` 표시가 74.4→74.3 으로 뒤집힘(74.35 반올림 절벽 인공물) → worked-example 에 병기 | G-SI(`test_gates_v1025.py`) |
| **C4** = 위 C3 에 흡수(별도 없음) | — | — | — |
| **C5** $w_\mathrm{eff}$ 문장(E) | 문건 §5b:53: "$w_\mathrm{eff}{\to}0$ 델타로 수렴 / 이 한 식으로 연속화" **삭제** + FWHM$\propto\lambda^{3/2}$ 병기(peak 높이 $1/(4w_\mathrm{eff})$ 는 정확) | §5(sec:width-w) 이중지위 wording·Part T warnbox: "$w_\eff(\Omega)$ 금지" 를 **두-상 한정**으로 좁혀 §5·§5b·Ch3 단상 해석과 공존·Ch3 sifr 정합 | G-금지(grep 표 등록) |
| **C6** regsol **완전 삭제**(D-C·DG-1(b)) | 코드: `_REGSOL_XG`·`_regsol_binodal_xa`·`_regsol_dqdv` 함수 3종 + `equilibrium()` 의 `if tr.get('kernel')=='regsol'` 분기 **전부 제거**(−40줄, 1957→1917). 커널 계통 = **로지스틱 단일계**. `'kernel'` 키가 남은 legacy 전이 dict 은 **무시**되어 로지스틱 경로를 탄다(하위호환 무해). **보존**: Ω 코드 전량(`func_dU_hys`·`func_dH_a_eff`·§7 상성격 판정 — regsol 무관)·데이터셋 전량 | 문건 Ch3 `eq:sifr-kernel`·`eq:sifr-blend` **식·라벨 보존**(해석적 유도는 유효 물리) + 지위 warnbox "미채택·**코드 미구현**"·`REFLECT_SEED_TABLE`·`FIT_CHECK`: @3 근거 철회 + 코드 삭제 등재 | **G-R3 재작성**(reflect): 심볼 부재 3/3 + `'kernel'` 키 무시(legacy==로지스틱 `array_equal`) + 면적=Q. 4/4 유지 |
| **C7** gallery opt-in(D-B) | 코드: `GRAPHITE_STAGING_MSMR6_LIT` 존치 + `SI_MSMR7_LIT`(0.433·0.456 feature 포함) opt-in 추가 | 문건 §5b 해상도 사다리(4·5·6·7): "gallery≠상" 재강조·XRD 상 수(4 staging·두-상 2) 불변 명기 | G: opt-in additive·기본 bit-exact |
| **C8** 배경(정직) | 문건 §6·§7·§10: `$C_\bg$` = **창-국소 상수 근사**·넓은 창은 광폭 종 1개 필요(@2 동반 시만 이득) 명기 | — | — |
| **C9** 데이터 정직 | 문건/검증문서: 레포 프로토콜 혼용(gr=p-ocv·si=hold) 정정·`SOURCES.md` 프로토콜 라벨·p-ocvhold 권고·독립셀 재현성 등재 | `DATA_REGISTRY`·`FIT_CHECK` | — |
| **G0** 게이트 신설 | 코드: `test_gates_v1025.py` — G-α1~4·G-창·G-금지·G-극단(파라미터 범위) | — | self |

---

## Phase P0 — 골격 복제·baseline·변경대장 (Steps 1–4)

- **Step 1**: `docs/v1.0.25/` = `docs/v1.0.24.1/` 복제(빌드산물 제외). 코드 파일명 **유지**(`Anode_Fit_v1.0.24.py`) + 내부 헤더 버전 문자열만 `1.0.25` 로 표기(§10 결정 대기 — 파일명 규약).
- **Step 2**: baseline 게이트 전건 실행 → GREEN 스냅샷 기록(변경 전 골든).
- **Step 3**: 위 변경대장(C1~C9·G0)을 `results/V1025_CHANGE_LEDGER.md` 로 고정(12-col ledger, [[feedback_phase_execution_loop]]).
- **Step 4**: 빌드 GREEN 확인(ch1·ch2·ch3 xelatex 3-pass, 0-err·undefined ref/cite 0).
- **Gate P0**: v1.0.25 복제 무결(diff = 헤더 버전 1줄) · baseline 게이트 골든 기록 · 변경대장 확정 · 빌드 GREEN.

## Phase P1 — 코드 국소 수정 + 게이트 (Steps 5–12)

- **Step 5 (C1 커널)**: `func_dxi_eq(T,V,U,n,s,alpha=1.0)` 신설 — 미분 종 = $(\alpha/w)\,\sigma^{\alpha}(1-\sigma)$, $\sigma=\mathrm{logistic}[s(V-U)/w]$. `alpha=1.0` 에서 $\sigma(1-\sigma)/w$ 와 **부동소수점까지 동일**(bit-exact 요구). 진행좌표 $\xi_\eq=\sigma^{\alpha}$ 도 함께 반환(단조 0→1 — lag·solve_U_oc 브래킷 보존).
- **Step 6 (C1 경유 통일)**: `equilibrium`·`dqdv`(평형종·peak_shape)·`entropy_coefficient`(g_j)·`solve_U_oc`(누적 ξ) 의 `ksi_eq*(1-ksi_eq)/w` 를 `func_dxi_eq` 로 치환. `alpha` 전이키 판독(부재→1.0). **부재 시 전 경로 bit-exact**.
- **Step 7 (C2 pad)**: `_causal_pad(V_prog,L)` 신설(진행방향 과거로 $5L_V$, coarse 격자 $\le L/20$, 상한 4000점). `_causal_memory_pointwise`·`_causal_memory_ratio`·(존치 시)regsol 경로에 pad 적용 후 절단.
- **Step 8 (C3 상수)**: ★**집행 정정** — `R_SI`·`F_SI` 상수 + `use_si_constants()` **opt-in** 추가(기본은 레거시 유지). 원안의 즉시 교체는 골든 bit-exact 와 양립 불가. 회귀 기준(74.4/−0.204/−0.134) SI 발효 시 재평가 → G-SI 로 증빙.
- **Step 9 (C6 regsol 삭제)** ★**DG-1(b) 확정으로 갱신**: `_REGSOL_XG`·`_regsol_binodal_xa`·`_regsol_dqdv` + `equilibrium()` 의 `'kernel'` 분기 **삭제**(−40줄). `test_gates_v1024_reflect` **G-R3 을 "삭제 확인" 게이트로 재작성**(심볼 부재 + `'kernel'` 키 무시 `array_equal` + 면적=Q) → 게이트 붕괴 없이 4/4 유지. Ω 코드·데이터셋은 **불가침**.
- **Step 10 (C7 Si opt-in)**: `SI_MSMR7_LIT`(7 gallery, 0.433/0.456 명시) 상수 추가(additive). 기본 `SI_*_LIT` 무변경.
- **Step 11 (G0 게이트)**: `test_gates_v1025.py` 작성 — G-α1(alpha 부재 bit-exact) · G-α2(면적 $\int dQ/dV=Q$, α∈[0.25,4]) · G-α3(C¹: 격자 반감 시 max|Δy′|/max|y| 비≈0.5) · G-α4(α·$L_V$ 동시 자유화 경고) · G-창(평가창 불변) · G-극단($L_V/w\in[0.1,3]$·$\alpha\in[0.25,4]$ 에서 유한·비음·면적) · G-금지("재도입 금지"/"쓰지 않는다" 선언 표 grep=위반0).
- **Step 12**: 기존 게이트 전건 재실행 — `test_gates_v1024`(G1 골든 **max|d|=0**)·`_reflect` 4/4·`_selfconsistent` 5/5 + `test_gates_v1025` 전건.
- **Gate P1**: (1) `alpha`/pad/상수/regsol-라벨/Si-opt-in 구현 완료. (2) **골든 bit-exact max|d|=0**(alpha 부재·pad 무영향 영역). (3) 신·구 게이트 전건 GREEN. (4) @2 유효성(alpha=2 등에서 곡선 실제 변화·면적 보존·C¹).

## Phase P2 — 문건 1차 국소 수정(@2 연계 + E + C_bg) (Steps 13–20)

- **Step 13 (§5 skew 식)**: `sec:eqpeak` 또는 `sec:width-w` 에 skew peak boxed 식 `eq:skewpeak` 신규 — $(\dd Q/\dd V)_j=Q_j(\alpha_j/w_j)\sigma^{\alpha_j}(1-\sigma)$, "**$\alpha_j=1$ 이면 `eq:eqpeak` 로 정확 회수**·면적 불변·$C^\infty$" 명기. **기존 `eq:eqpeak` 삭제 X**(추가만).
- **Step 14 (§7 broadening)**: `sec:broadening-sources` 의 3출처(①$L_V$·②$RT/F$·③$\eta$)에 **평형 비대칭 축 α** 추가. ① 은 전류 의존·전이 소멸, α 는 전류 무관 평형 잔여로 **명시 구분**(이중계산 가드). ②⊗③ 대칭 전제 완화 서술.
- **Step 15 (Ch3 §3.2b 완화)**: "비대칭은 오직 여러 종 envelope 에서만 온다" → "envelope **또는** 단일 gallery α(파라미터 효율 대안); 어느 쪽도 새 상 아님" 로 완화. gallery↔α 상호 대안 관계 1문장.
- **Step 16 (§18 식별)**: `sec:inputs` 에 "정적 단일 T 곡선에서 α·$L_V$·gallery 세분은 서로 축퇴 — α 만 열고 $L_V=0$, gallery 세분과 α 동시 자유화 지양; 율속 스윕이 ①($\propto|I|$)만 가름" 지침.
- **Step 17 (C5 §5b·Part T)**: `ch1_sec05b_gr2L.tex:53` "$w_\mathrm{eff}\to0$ 델타로 수렴/연속화" 삭제 + "FWHM$\propto\lambda^{3/2}$, peak 높이 $1/(4w_\mathrm{eff})$ 는 정확" 병기. `ch2_sec05_mixing` warnbox 의 $w_\eff(\Omega)$ 금지를 **"두-상 폭에 한정"** 으로 수정.
- **Step 18 (C8 배경)**: §6·§7·§10 의 $C_\bg$ 를 "창-국소 상수 근사(넓은 창은 광폭 종 필요·@2 동반 시만 이득)" 로 한정 명기.
- **Step 19**: 신규 `\label`(eq:skewpeak 등) 정의·기존 키 불변 확인(grep).
- **Step 20**: ch1 재빌드 GREEN(0-err·undefined ref/cite 0).
- **Gate P2**: 신규 식 α=1 회수 명기 · §7 α↔① 구분 · Ch3 envelope 완화 · §5b·Part T 문장 정정 · 기존 label/식번호 불변 · 빌드 GREEN.

## Phase P3 — 문건 2차 연계 보완 (Steps 21–27)

- **Step 21 (C6 Ch3 지위)** ★**DG-1(b) 로 갱신**: `eq:sifr-kernel`·`eq:sifr-blend` 는 **식·label 보존**(해석적 유도는 유효 물리 — 문건 자산 삭제 금지)하되 지위 warnbox 를 "**미채택·코드 미구현**(v1.0.25 삭제)"으로 쓴다. @3 = gallery 세분과 중복·역전(+0.97→−0.53%p)임을 그 warnbox 1개로. Ω 파라미터 존치를 같은 박스에서 명시(삭제된 것은 dQ/dV **커널**뿐).
- **Step 22 (부록 B 코드맵)**: `tab:symcode`·`tab:inputs`·`tab:nodecode` 에 `alpha`(`func_dxi_eq`)·`_causal_pad` 행 추가. `func_ksi_eq`↔`func_dxi_eq` 관계 각주.
- **Step 23 (C7 gallery)**: §5b 해상도 사다리에 "7-gallery(Si)" 병기·"gallery≠상, XRD 상 수 불변" 재강조.
- **Step 24 (C9 데이터)**: `results/comp_v24` 하위 `FIT_CHECK`·`DATA_REGISTRY`·`SOURCES.md` — 프로토콜 혼용 정정·p-ocvhold 권고·전이세분 우위·@3 철회·독립셀 재현성 등재.
- **Step 25 (마감문서)**: `results/V1025_CHANGE_LEDGER.md`·`HANDOVER_v25.md`·`MERGE_READINESS_v25.md`·`INDEX_v25.md`.
- **Step 26**: ch2·ch3 재빌드 GREEN.
- **Step 27**: 전 3장 cross-ref(xr 외부참조 포함) undefined 0 재확인.
- **Gate P3**: Ch3 강등 prose(식 불변) · 부록 B 코드맵 정합 · 데이터 정직화 · 마감문서 4종 · 3장 빌드 GREEN·cross-ref 0.

## Phase P4 — 통합 검증·마감 (Steps 28–31)

- **Step 28**: 게이트 전건(구 4종 + `v1025`) GREEN·골든 max|d|=0 재확인.
- **Step 29 (실측 재현)**: `alpha` opt-in 으로 흑연 R² 0.977→0.981(±) 재현·면적 보존·C¹. 기본(alpha 부재) 곡선이 v1.0.24.1 과 bit-exact.
- **Step 30 (doc↔code 감사)**: 변경대장 C1~C9 각각 문건 서술 = 코드 거동 1:1 확인(특히 `eq:skewpeak`↔`func_dxi_eq`·`eq:tail-limit`↔pad·regsol 강등 grep).
- **Step 31**: MERGE_READINESS 판정 + Opus 검수 인계.
- **Gate P4**: 게이트 GREEN·골든 bit-exact · alpha 재현 · doc↔code 1:1 · 빌드 GREEN · P3 7항 승계.

---

## Implementation Interfaces

- **파일**: `docs/v1.0.25/`(v1.0.24.1 복제). 코드 = 헤더 버전만 1.0.25(파일명 §10). 신규 게이트 `test_gates_v1025.py`.
- **추가만(additive)**: `func_dxi_eq`·`_causal_pad`·`SI_MSMR7_LIT`·`alpha`/`theta_E` 류 전이키·신규 `\label`. 기존 함수·상수·데이터셋·식번호·label 불변.
- **skew 수학**(코드·문건 공통): $\sigma=\mathrm{logistic}[\sigma_d(V-U^d)/w]$, $\xi_\eq=\sigma^{\alpha}$, $\dd Q/\dd V=Q(\alpha/w)\sigma^{\alpha}(1-\sigma)$. $\int_0^1 \dd\xi_\eq=1$(면적 보존). $\alpha=1$ → $\sigma(1-\sigma)/w$(bit-exact).
- **pad**: 진행방향 과거로 $5L_V$(coarse 격자), 계산 후 원 격자만 반환. 기본 $L_V\!\sim\!10^{-8}$V 라 pad<격자 → 항등(골든 보존).
- **집행**: **Fable 5.0 서브세션**이 P0~P4 수행. Opus 는 게이트·doc↔code 감사·MERGE 판정만. 커밋/푸시는 사용자 결정 전 금지.

---

## Test Plan (전부 확인 가능 조건)

- **골든 bit-exact**: `test_gates_v1024` G1 module·golden max|d| = **0.0** (alpha 부재·pad 무영향). = 국소 수정이 기본 경로를 안 건드림의 증명.
- **G-α1**: alpha 부재 == 현행, `np.array_equal` True.
- **G-α2**: $\alpha\in\{0.25,0.5,1,2,4\}$ 에서 $|\int(\dd Q/\dd V)\dd V - Q|/Q \le 10^{-6}$.
- **G-α3**: skew peak 격자 반감 시 max|Δy′|/max|y| 비 ≈0.5(C¹, kink 0).
- **G-α4**: α·$L_V$ 동시 자유화 조건에서 경고 발생.
- **G-창**: 같은 물리점이 $V_\mathrm{app}$ 시작점 무관(원본 100% → ≤1%).
- **G-금지**: "재도입 금지"/"쓰지 않는다" 선언 표 등록 후 본문 grep = 위반 0.
- **G-극단**: $L_V/w\in[0.1,3]$·$\alpha\in[0.25,4]$ 전역 유한·비음·면적.
- **빌드**: ch1·ch2·ch3 xelatex 3-pass 0-err·undefined ref/cite 0.
  - ★**환경 제약(2026-07-26 실측)**: 본 PC 에는 **TeX 배포판이 설치되어 있지 않다**(`xelatex`·`pdflatex`·`latexmk`·`lualatex` 전부 부재 — PATH·`C:\texlive`·`MiKTeX` 경로 탐색 확인). 따라서 **실제 컴파일 게이트는 이 환경에서 집행 불가**이며, 대체 게이트로 리포 자체 도구 `results/tools_check_structure.py check` 를 쓴다: 라벨 중복 0·미해소 `\ref/\eqref` 0(전 마스터 라벨 합집합 기준 — 장간 xr 반영)·`cite`-undef 0·`bibitem`-uncited 0·`\begin/\end` 짝 오류 0 → `STRUCTURE_CHECK: PASS`. 이는 **"undefined ref/cite 0" 부분만** 대체하며 **TeX 문법·매크로 정의·조판 오류는 커버하지 못한다** — 실제 빌드는 TeX 가 있는 환경에서 **머지 전 필수 잔여 게이트**로 남긴다(MERGE_READINESS 에 미해결로 등재).
  - baseline(문건 편집 전) `STRUCTURE_CHECK` = **PASS** (ch1 라벨 263·ref 1064·cite 138/bibitem 44 / ch2 82·355·77/15 / ch3 44·190·86/36 / 부록 30·41 — 전부 dup 0·unresolved 0·env 오류 0).
- **실측 재현**: alpha opt-in 흑연 ΔR²≈+0.004(gr.csv), 기본 bit-exact.
- **doc↔code**: C1~C9 각 1:1.

---

## Assumptions (정직 프레임 — 반드시 문건에 명기)

- **@2 는 현상학적 형상 파라미터**이지 새 물리·새 상이 아니다. 물리적 동기 = order–disorder 엔트로피 스텝(Reynier·Yazami·Fultz 2004)·조성 의존 $\Omega(x)$. tier-C, 피팅 결정.
- **@2 는 gallery 세분과 부분 중복**: 단일 gallery α = 여러 gallery envelope 의 파라미터 효율 대안. **α 로 잡히는 비대칭을 gallery 로도 잡을 수 있고 그 역도 성립** → 둘 동시 자유화 시 축퇴(§18 가드). 문건 Ch3 §3.2b 의 "envelope 전용" 서술을 이 관계로 완화하는 것이 정직.
- **@2·gallery 어느 것도 XRD 상 수를 바꾸지 않는다** — 상은 §7 대로(흑연 4 staging·두-상 2), gallery/α 는 곡선 표현 해상도.
- **@3(regsol) 강등의 근거는 실측**(전이 세분 시 −0.53%p 역전)이지 물리 오류가 아니다 — v1.0.24 판단은 그때 조건(저해상 gallery)에서 옳았고 조건이 바뀌어 무효가 됨.
- **배경 감쇠는 실재**(4셀 일치)이나 피팅 창 안에서는 상수 근사가 실용적 — 창 확장 시에만 광폭 종 필요.
- **회사 다온도/다율속 데이터 위임분 불변**: stage-2L 0.30 mV/℃·LCO 전자항 T-의존·α↔$L_V$ 분리(율속) = Task #38.

---

## Decision Gate (§10 — ★2건 모두 사용자 결정 완료·닫힘)

- **DG-1 regsol 배제 방식** → ★**(b) 완전 삭제 확정** (사용자 2026-07-26 "regsol 삭제").
  - 원 권고는 (a) 강등이었고 근거는 "G-R3 게이트 붕괴 회피"였다. **집행 시 그 우려는 해소됨** — G-R3 을
    삭제하는 대신 **"삭제 확인" 게이트로 재작성**(심볼 부재 3/3 + `'kernel'` 키가 남은 legacy dict 이 로지스틱과
    `array_equal` + 면적 $=Q$)해서 게이트 수 4/4 를 유지하고, 오히려 *부재*를 증빙하는 더 강한 가드를 얻었다.
  - 삭제 범위: `_REGSOL_XG`·`_regsol_binodal_xa`·`_regsol_dqdv` + `equilibrium()` 의 `'kernel'` 분기(−40줄).
    **불가침으로 보존**: 모든 Ω 코드(`func_dU_hys`·`func_dH_a_eff`·§7 상성격 판정)·모든 데이터셋·문건의
    `eq:sifr-kernel`·`eq:sifr-blend` 식·라벨(해석적 기록으로 존치).
- **DG-2 코드 파일명** → ★**(a) 파일명 유지 확정** (사용자 2026-07-26 "파일명을 왜 바꿔? 버전명만 바꿔주면
  되는거 아니냐?"). `Anode_Fit_v1.0.24.py` 유지 + 내부 release 문자열만 1.0.25. 문건 쪽도 파일명·`\input`
  경로·`\externaldocument` 키 전부 불변, 사람이 읽는 표시 버전(pdftitle·lhead·`\date`)만 1.0.25.

> 그 외(D-A~D-D)는 사용자 확정 — 재질문 없이 baked ([[feedback_user_decision_no_requery]]).

---

## Correction History

- 2026-07-26 v1: 검수 4건(A~E) + @1~@5 재검증 + 배경·데이터·@3역전·gallery≠상 실측 확정 → **국소 수정판**으로 프레이밍. @2 opt-in·gallery opt-in 유지·regsol 강등·상수/pad/w_eff 정정. 집행 = Fable 5.0 서브세션, 검수 = Opus. DG-1(regsol 방식)·DG-2(파일명) 만 open.
- 2026-07-26 v2 **(집행 완료 반영)**: DG-1=**(b) 삭제**·DG-2=**(a) 파일명 유지** 확정으로 §10 닫힘.
  집행과 원안이 갈린 **3건**을 본문에 반영 —
  ① **C3**: "상수 즉시 교체" → **opt-in**(`use_si_constants()`). 이유 = 상수 교체는 모든 값을 바꾸므로 골든
     bit-exact 게이트(G1 `max|d|`$=0$)와 **수학적으로 양립 불가**. 대신 G-SI 로 SI 발효 시 표시 정합을 증빙.
  ② **C6**: "강등" → **완전 삭제** + G-R3 재작성(위 DG-1).
  ③ **신규 라벨 1개 예정 → 3개**: `eq:skewpeak`(계획분) + `eq:skewapex`·`eq:gr2l-fwhm`(집행 중 승격 —
     각각 α≠1 의 정점 이동·높이 재척도, 단상 FWHM 닫힌형. 둘 다 문건의 정량 정정에 필요해 식으로 올림).
  **모델 배분(사용자 지시 2026-07-26, 이번 판 한정)**: 코드 C1·C2·C3·C7 = Fable 5.0 서브 /
  **문건 T1~T12(물리·화학 논리) = 마스터 Opus 5.0 직접** / T13·T14·마감문서 = Opus 4.8 서브.
  **환경 제약**: TeX 배포판 부재 → 실제 빌드 게이트는 이 환경에서 집행 불가(§Test Plan 참조).
  정적 대체 게이트 전건 통과(`STRUCTURE_CHECK: PASS` · 자체 엄격검사 ALL PASS · doc↔code 감사 30/30 PASS)
  및 코드 게이트 전건 GREEN(골든 `max|d|`$=0$ · reflect 4/4 · selfconsistent 5/5 · v1025 8/8 · `__main__` OK).
  **잔여**: LaTeX 3-pass 빌드(머지 차단) · "흑연 물리 두-상 4 vs 2" 선행 표기 불일치(사용자 확인 요청, 비차단).
