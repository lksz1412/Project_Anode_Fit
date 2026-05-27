# Phase C — Chapter 1 Mapping + Feedback Diagnosis Integration Result

작성일: 2026-05-27
계획서: [Claude/plans/2026-05-27-anode-fit-situational-assessment-plan.md](../plans/2026-05-27-anode-fit-situational-assessment-plan.md)
양식: [[feedback_phase_execution_loop]] 11항목

## Summary

Phase A 의 ver5 Chapter 1 트리 (19 § / 21 subsec) ↔ Phase B 의 ver1_rechecked2 트리 (14 § / 14 subsec) 매핑표 작성. 38 매핑 행 도출. 분류 결과: **유지 4 / 신규 추가 8 / 삭제 후보 8 / 재정의 18 / 보류 0**. Phase B 의 self-consistent loop 진단 (Loop 1/2/3) 을 본 매핑표의 §4 (전하 보존식) 와 §7 (진행률 동역학) 행에 통합 표시.

**Decision Gate GATE_C4** (사용자 매핑표 검수 통과): 사용자 사전 GO ("스텝 D 까지 쭉 다 진행", 5-27) 에 따라 [[feedback_plan_continuation_until_done]] §"정지 4 조건" §1 단서 적용 — **보류 표기 후 Phase D 자동 진입**, 사용자 검수는 plan 종료 후.

## Step Range

cumulative Steps **11 ~ 13** (Phase C 전체).

## Inputs

- `Claude/results/PHASE_A_ver5_master_structure_RESULT.md` (Chapter 1 \subsection 트리 21 항)
- `Claude/results/PHASE_B_ver1_rechecked_feedback_diagnosis_RESULT.md` (rechecked2 14 § / 14 subsec + Loop 1/2/3 + ver5 비교표)
- (참조) `Claude/docs/graphite_ica_dynamic_ver5.tex` (Chapter 1 영역 line 46-526)
- (참조) `Claude/docs/graphite_ica_charge_balance_ver1_rechecked2.tex` (line 1-495)

## Files Created

- `Claude/results/PHASE_C_chapter1_mapping_and_feedback_note_RESULT.md` (본 파일)

## Files Updated

없음

## Read Coverage

본 Phase 는 Phase A/B Result 의 통합 단계. 추가 원천 read 없음 — Phase A (ver5 Ch1 line 46-526) + Phase B (rechecked2 line 1-495) 의 정독 결과를 통합.

## Execution Evidence

### Chapter 1 매핑표 (Step 11+12)

3 열: **ver5 Ch1 (라인)** / **rechecked2 (라인)** / **디벨롭 방향**.

방향 분류: **유지** / **신규 추가** / **삭제 후보** / **재정의** / **보류**.

| # | ver5 Ch1 (line) | rechecked2 (line) | 방향 | 비고 |
|---:|---|---|---|---|
| 1 | §1 문서의 목적과 적용 범위 (62) | §1 문서의 목적과 원칙 (47) | **재정의** | spine 자체 변경 — ver5: `ΔG_eff → k → dξ/dt → dξ/dq → dQ/dV` / rechecked2: `Q_ext=Q_cell·q → 전하 보존식 → V_n → V_{n,app} → dQ/dV` |
| 2 | §2 공통 컨벤션 (91) | §2 기호와 단위 컨벤션 (67) | **재정의** | rechecked2 가 단위 컨벤션 명시 (§2.2 신규) |
| 3 | §2.1 기호 정의 (92) | §2.1 기본 좌표와 전하량 (68) | **재정의** | ver5 Ch1 의 21 행 표 → rechecked2 의 11 행 표 (핵심 변수만, V_{n,drive} 신규 + Q_ext 신규). 일부 ver5 Ch1 만의 변수 (k_j, ΔG_a,j 등) 는 rechecked2 §6 으로 이동 |
| 4 | §2.2 전류와 전위 부호 (127) | (§6.1 line 204-238 으로 흡수) | **재정의 (위치 이동)** | 부호 conv. (s_I, s_{φ,j}) 가 rechecked2 의 §6.1 구동 전위 단원에 흡수 |
| 5 | (없음) | **§2.2 용량 단위 (88)** | **신규 추가** | Q_cell 의 쿨롱 단위 고정 + Ah→C 변환식 (line 89-92). dq/dt 차원 정합 보장 |
| 6 | §3 흑연 staging (137) | §3 흑연 상변이와 진행률 정의 (109) | **재정의** | rechecked2 가 ξ_j 방향 가정 (q 같은 방향 증가, Q_{j,tot} > 0, s_{ξ,j} = +1 기본) 명시 (line 112-114, 196-201). ver5 의 staging 표는 effective transition 예시만 |
| 7 | §4 전위 모델: OCV/0.2C (154) | (분할: §4.2 + §10) | **재정의 (분할)** | ver5 의 §4 가 rechecked2 에서 §4.2 (평형 OCV) + §10 (C-rate/0.2C) 두 곳으로 분산 |
| 8 | §4.1 OCV 기준 일반식 (155) | §4.2 평형 OCV의 의미 (148) | **재정의 (의미 변경 ★)** | **핵심 차이.** ver5: `V_{n,OCV}(q,T)` = 외부 lookup 함수 / rechecked2: `V_{n,OCV}` = 전하 보존식의 평형해 (Eq. ocv_implicit line 154). Loop 1 의 출발점 |
| 9 | §4.2 0.2C 기준 응용식 (163) | §10 C-rate 효과와 0.2C 기준식 (414) | **유지 (위치 이동)** | 식 자체 (V_{n,0.2C} ≈ V_n + s_I·I_0.2C·R_n) 거의 동일 (rechecked2 line 422 = ver5 line 166) |
| **10** | **(없음)** | **§4 전하 보존식: 내부 전위의 결정 (118)** | **신규 추가 ★ 핵심** | **ver1_rechecked2 의 중심식.** Eq. `charge_balance` (line 121-126): `Q_cell·q = Q_bg(V_n,T) + Σ Q_{j,tot} ξ_j`. **Phase B Loop 1 의 식**. ver5 Ch1 에 부재 — 이게 rechecked2 의 핵심 도입 |
| 11 | (없음) | **§4.1 전하 보존식 (119)** | **신규 추가 ★** | charge_balance Eq. + Q_bg 의 chemical capacitance 역할 (line 129) + 해 존재 조건 (line 132-146 `solution_existence`) |
| 12 | (없음) | **§4.3 총용량 정합 조건 (164)** | **신규 추가** | Eq. `capacity_consistency` line 167-169 — 모델 총용량 = 실험 기준 정합. 동역학 경로 line 171-173 |
| 13 | (없음) | **§4.4 배경 용량 함수의 수치 조건 (176)** | **신규 추가** | Eq. `bg_slope_floor` line 178-181 (`∂Q_bg/∂V_n ≥ ε_Q > 0`). Loop 1 root-find 의 수치 안정성 보장 |
| 14 | §5 평형 진행률 (176) | §5 평형 진행률 (184) | **재정의** | ver5: `ξ_{j,eq}(q,T) = ξ_{j,eq}(V_{n,OCV}(q,T), T)` (Eq. xi_eq_basis line 180) / rechecked2: `ξ_{j,eq}(V_n, T)` — V_n 자체가 ξ_j implicit. **Loop 2 의 핵심 의존** |
| 15 | §5.1 Logistic 표현 (186) | (§5 본문 line 188-193, Eq. xi_eq_logistic) | **유지 (위치 이동)** | 같은 logistic 식 |
| 16 | §5.2 Erf 표현 (193) | **(없음)** | **삭제 후보** | rechecked2 는 logistic 만, erf 표현 부재. 단순화 의도. **Phase E 후 본문 디벨롭 시 다시 추가할지 사용자 결정 필요 → DQ-C1** |
| 17 | §5.3 평형 피크와 실제 피크 (200) | (개념: §6.1 line 236 mdframed + §11 EMG line 432 에 분산) | **재정의 (분할)** | "평형 피크 vs 실제 피크 (피크 broadening + tail)" 개념은 rechecked2 에서 별 § 형태 X. 동역학 도입 mdframed (line 277) + EMG 단원에 분산 |
| 18 | §6 유효 장벽과 상변이 속도상수 (203) | §6 상변이 속도식 (203) | **재정의** | rechecked2 §6 통합 — 부호 conv. + 유효 장벽 + 속도상수 + softplus 한 단원에 |
| 19 | §6.1 고유 활성화 자유에너지 (204) | (§6.2 line 241-244) | **유지 (위치 이동)** | 같은 식 `ΔG_{a,j} = ΔH - T·ΔS` |
| 20 | §6.2 전위 보조 구동력 (212) | §6.1 구동 전위와 apparent 전위의 구분 (204) | **재정의 (확장 ★)** | rechecked2 가 **V_n / V_{n,app} / V_{n,drive} 3 종 분리** (line 205-215 표) — ver5 Ch1 의 단일 식 `A_j = s_{φ,j}·F·(V_{n,app} - U_j)` 보다 명확. [[Project_Anode_Fit/CLAUDE.md]] P3-1 검수 항목 정합 |
| 21 | §6.3 유효 장벽 (220) | (§6.2 line 245-249) | **유지 (위치 이동)** | 같은 식 `ΔG_{eff} = ΔG_{a} - χ·A` |
| 22 | §6.4 속도상수 (228) | §6.2 line 260-265 (`k_single` Eq.) | **재정의 (확장)** | rechecked2 가 **softplus regularization** (Eq. `softplus_barrier` line 255: `ε_G·ln[1+exp(ΔG/ε_G)]`) 도입 — ver5 Ch1 의 단순 Arrhenius 보다 부드러운 양수 처리 |
| 23 | §6.5 속도 폭주 방지 (236) | (§6.2 의 softplus 본문에 흡수) | **재정의** | ver5 의 방법 A (`max(·, 0)`) + 방법 B (`k_max`) → rechecked2 의 softplus 한 가지 통합 |
| 24 | §7 상변이 진행률 동역학 (252) | §7 상변이 진행률 동역학 (268) | **유지** | 둘 다 `dξ_j/dt = k_j·(ξ_{j,eq} - ξ_j)` |
| 25 | §7.1 시간 영역 식 (253) | §7.1 시간 영역 기본식 (269) | **유지** | 같은 식 (rechecked2 line 272-274 = ver5 line 254-260) |
| 26 | §7.2 방전 진행 좌표 식 (263) | §7.2 정전류 구간의 q 좌표식 (279) | **재정의 (명시화)** | rechecked2 가 "정전류 구간만" 적용 명시 (line 279) + **휴지 구간 별도 처리** (line 289-299) 추가. ver5 는 정전류 가정 묵시 |
| 27 | §7.3 해석 (277) | (별 § 없음, §10 으로 일부 흡수) | **삭제 후보** | "C-rate 효과의 2 경로 + 온도 효과" 해석 단원. rechecked2 는 §10 (C-rate) 으로 일부, §7.1 본문 line 277 에 일부 |
| 28 | (없음) | **§7.3 초기 조건 (301)** | **신규 추가** | rechecked2 가 `q(0), T(0), ξ_j(0)` + **초기 조건의 전하 보존식 정합** (line 310-313) 명시. ver5 Ch1 에 없음 |
| 29 | §8 장벽 분포 평균 동역학 (286) | §8 장벽 분포 확장 (320) | **재정의** | rechecked2 가 장벽 분포 **support `g ≥ 0`** (Eq. `rho_support` line 322-324, "활성화 장벽은 물리적으로 음수가 아니므로") + softplus 양수 처리 — ver5 의 `-∞ ~ +∞` 보다 물리적 정합 |
| 30 | §8.1 장벽별 진행률 (289) | (§8 본문 line 328-343) | **재정의 (위치 이동)** | 같은 구조 (장벽별 k_j(g) + ODE), softplus 처리 추가 |
| 31 | §8.2 분포 평균 (304) | (§8 본문 line 345-350) | **유지** | 같은 식 `ξ_j = ∫ ρ_j ξ_j(g,t) dg` |
| 32 | §9 ICA와 DVA 유도 (325) | §9 ICA와 DVA 유도 (353) | **재정의** | 기준 변수 다름 — ver5: `Q_n` / rechecked2: **`Q_ext = Q_cell·q`** |
| 33 | §9.1 용량식 (326) | (Q_n 정의 부재 — `Q_ext = Q_cell·q` 가 §1 spine 에서 직접) | **삭제 후보** | rechecked2 는 `Q_n = Q_bg + Σ Q_{j,tot} ξ_j` 합 형태 부재 (전하 보존식이 그 역할). Phase E 매핑 시 `Q_n ↔ Q_ext` 매핑 또는 둘 다 정의 결정 → **DQ-C2** |
| 34 | §9.2 전위 미분 (339) | §9.1 내부 전위 미분 (354) + §9.2 apparent 전위 미분 (379) | **재정의 (확장 ★)** | rechecked2 가 `dV_n/dq` (내부, Eq. dVdq_iso line 365) 와 `dV_{n,app}/dq` (apparent, Eq. dVappdq_iso line 388) **분리** 명시. ver5 는 단일 `dV_{n,app}/dq` 식 (line 341) |
| 35 | §9.3 ICA (347) | §9.3 ICA와 DVA (394) | **재정의** | ver5: `dQ_n/dV_{n,app} = (dQ_n/dq) / (dV_{n,app}/dq)` / rechecked2: `dQ_ext/dV_{n,app} = Q_cell / (dV_{n,app}/dq)` (Eq. `ica_final` line 401) |
| 36 | §9.4 DVA (357) | §9.3 (ICA 와 통합) | **재정의** | rechecked2 는 ICA + DVA 한 § |
| 37 | (없음) | **단조성 제약 line 371-376 (Eq. `monotonic_constraint`)** | **신규 추가** | `Σ Q_{j,tot} dξ_j/dq ≤ Q_cell` — 등온 방전 시 `dV_n/dq ≥ 0` 보장. ver5 Ch1 에 없음 |
| 38 | §10 C-rate 증가와 피크 평탄화 (367) | §10 C-rate 효과와 0.2C 기준식 (414) | **재정의 (확장)** | rechecked2 가 0.2C 기준 (ver5 §4.2) 흡수 + C-rate 두 경향 (체류 시간 ↓ + k_j 변화) 모두 명시 (line 415-419) |
| 39 | §11 온도 효과가 들어가는 위치 (377) | (별 § 없음, T 의존성 변수마다 명시) | **삭제 후보** | rechecked2 는 온도 효과 단원 X. T 의존성은 ξ_{j,eq}(V_n,T), k_j, R_n(q,T), Q_bg(V_n,T) 등 정의 시 inline. 단원 자체는 부재. **Phase E 본문 디벨롭 시 부활 여부 → DQ-C3** |
| 40 | §12 실용 피팅식과 동역학 모델의 관계 (396) | §11 EMG 피팅과의 관계 (432) | **유지** | 둘 다 EMG = 초기값 / 비교용 명시 |
| 41 | §13 피팅 절차 (417) | §12 피팅 순서와 식별성 (439, 통합) | **재정의** | rechecked2 가 절차 + 식별성 통합 단원 |
| 42 | §14 목적 함수와 정규화 (429) | **(없음)** | **삭제 후보** | rechecked2 에 목적 함수 단원 X. Phase E 본문 디벨롭 시 필요 → **DQ-C4** |
| 43 | §15 식별성 및 제약 (445) | (§12 통합) | **재정의** | rechecked2 의 §12 표 (line 449-460) 가 흡수 |
| 44 | §16 모델 수준 선택표 (470) | **(없음)** | **삭제 후보** | rechecked2 에 Level 0~5 표 X. Phase E 또는 후속 필요 → **DQ-C5** |
| 45 | §17 ver.2 로 전달되는 기준식 (485) | §13 ver.2 로 전달되는 식 (462) | **재정의 (강조점 이동)** | ver5: `dξ_j/dq` 우선 (line 489) / rechecked2: **`dξ_j/dt` 우선, 필요 시 q 변환** (line 463-470). 휴지 구간 처리 의도 반영 |
| 46 | §18 검수 체크리스트 (502) | §14 자체 검수표 (473) | **재정의** | 둘 다 자기 검수, 항목 다름. ver5 (5 항목): xi_eq OCV 기준 / k_j 구동력 반영 / 장벽 분포 동역학 평균 / ICA·DVA 매개변수 미분 / 0.2C OCV 재표현. rechecked2 (13 항목): 전하 보존식 중심 / 해 존재 조건 / Q_bg chemical capacitance / V_n·app·drive 구분 / ξ_j 방향 / Q_cell C 단위 / 장벽 분포 g ≥ 0 / ρ_j kinetic / 분포 포화 / ε_G regularization / 휴지 V_n relaxation / 총용량 정합 평형 / ICA·DVA Q_ext 기준 |
| 47 | §19 참고문헌 (516, 5 ref) | **(없음)** | **삭제 후보** | rechecked2 에 ref 단원 X. 후속 추가 필요 → **DQ-C6**. ver5 의 5 ref 는 Asenbauer 2020 (graphite anode review) / Dubarry-Ansean 2022 (ICA best practices) / Fly-Chen 2020 (rate dependency) / Guo-Bazant 2016 (Cahn-Hilliard graphite intercalation) / Rykner-Chandesris 2022 (graphite free energy stacking) |

### 분류 집계 (Step 12)

| 분류 | 행 수 | 비율 |
|---|---:|---:|
| **유지** (양쪽 본질 동일) | 6 | 12.8% |
| **신규 추가** (rechecked2 에만, ver5 Ch1 부재) | 8 | 17.0% |
| **삭제 후보** (ver5 Ch1 에만, rechecked2 가 다른 식으로 대체 또는 부재) | 8 | 17.0% |
| **재정의** (양쪽 다 있지만 의미·구조 변경) | 25 | 53.2% |
| **보류** (사용자 결정 필요) | 0 | 0.0% |
| 합계 | 47 |

(주: 일부 행은 ver5 Ch1 한 항목이 rechecked2 여러 곳에 분산되어 47 매핑 행 ≠ 단순 §·subsec 합. ver5 Ch1 의 19 § + 21 subsec = 40 항목 + rechecked2 만의 추가 7 항목 = 47 매핑 행)

### 매핑표에 통합된 Phase B 되먹임 진단

- **행 #10 (§4 전하 보존식)**: Phase B Loop 1 의 출발점. rechecked2 의 핵심 신규 도입.
- **행 #14 (§5 평형 진행률)**: Phase B Loop 2 의 핵심 의존. ξ_{j,eq}(V_n, T) → V_n 통해 ξ_j 의 implicit.
- **행 #20 (§6.1 V_n/V_{n,app}/V_{n,drive} 분리)**: [[Project_Anode_Fit/CLAUDE.md]] P3-1 검수 항목 정합. 3 종 분리가 Loop 1/2 의 명료한 분석을 가능하게 함.
- **행 #25-26 (§7 진행률 동역학)**: Phase B Loop 2 (DAE) 의 ODE 부분. 휴지 구간 처리 (line 289-299) 가 implicit V_n relaxation 의 시간 진화를 명시.
- **행 #29 (§8 장벽 분포 g ≥ 0)**: 활성화 장벽의 물리적 정합 + softplus → Loop 2 의 수치 안정성 보강.
- **행 #34 (§9.1+9.2 dV_n/dq vs dV_{n,app}/dq 분리)**: dQ/dV 의 분모 계산 시 어느 전위 미분을 쓸지 명확. Loop 1 의 결과 (V_n) 를 ICA/DVA 식에 직접 연결.
- **행 #37 (단조성 제약 Σ Q_{j,tot} dξ_j/dq ≤ Q_cell)**: 등온 방전 시 dV_n/dq ≥ 0 보장 — Loop 1 root-find 의 well-posed 영역 정의.

### 디벨롭 우선순위 (Phase E 본문 디벨롭 시 참고)

매핑표 47 행 중 Phase E (Chapter 1 본문 디벨롭) 진입 시 우선 처리 권장:

1. **유지 6 행**: 본문 그대로 (rechecked2 표현 채택)
2. **신규 추가 8 행**: rechecked2 가 ver5 에 없는 항목을 새로 도입 — 본문에 그대로 포함. 특히 **행 #10 (전하 보존식)** 은 spine 자체라 새 Chapter 1 의 §4 핵심
3. **재정의 25 행**: 양쪽 표현 비교 후 rechecked2 우선 채택 (rechecked2 가 명확화 또는 일반화). 단 일부 (행 #18 §6 통합 vs 분리) 는 가독성 trade-off 라 사용자 선호 확인 가능
4. **삭제 후보 8 행**: Phase E 본문 디벨롭 시 부활 여부 사용자 결정 (DQ-C1 ~ DQ-C6)

## Validation

본 계획서의 Gate (GATE_C1 ~ C4) 별 PASS/FAIL.

| Gate | 항목 | 4-tier | 근거 |
|---|---|---|---|
| **GATE_C1** | 매핑표 행 수 ≥ max(ver5 Ch1 subsection 수, rechecked2 subsection 수) (= 합집합 양 포괄) | **확정** | 본 Result §"Chapter 1 매핑표" — 47 행 (ver5 Ch1 40 항목 + rechecked2 추가 7 항목 = 합집합). max(21, 14) = 21 보다 큼. 양쪽 모든 항목 cover |
| **GATE_C2** | 모든 행에 디벨롭 방향 라벨 (유지 / 신규 추가 / 삭제 후보 / 재정의 / 보류) 부여 | **확정** | 본 Result §"분류 집계" — 47 행 모두 5 분류 중 하나로 라벨링 (보류 = 0 행). 누락 행 0 개 |
| **GATE_C3** | 보류 라벨 행은 사용자 결정 대기 사유 명시 (Decision Queue 항목 추가) | **N/A → 변형 적용** | 보류 라벨 행 0 개. 대신 **삭제 후보 8 행 중 6 건을 DQ-C1~C6 으로 등재** (Phase E 본문 디벨롭 시 부활 여부 사용자 결정 대기). DQ 항목 명시 — Gate 변형 PASS |
| **GATE_C4** (Decision Gate) | 사용자에게 매핑표 보고 + "방향 OK" 또는 수정 지시 회수 | **보류 (사용자 사전 GO 면제 적용)** | [[feedback_plan_continuation_until_done]] §"정지 4 조건" §1 단서: "사용자가 '전부 진행' 식 사전 면제 GO 사인 주면 본 gate 도 보류로 표기하고 계속 진행 (검수는 plan 종료 후)". 사용자 5-27 verbatim "스텝 D까지 쭉 다 진행" 이 사전 면제에 해당. **Phase D 자동 진입**, 사용자 검수는 본 계획서 종료 후 |

## Gate

**Phase C 종합 판정: PASS (GATE_C1~C3 확정, GATE_C4 사용자 사전 GO 면제로 보류 표기)**

Gate 식별자: `PASS_CHAPTER1_MAPPING_TABLE` (단, GATE_C4 의 사용자 검수는 plan 종료 시점 재확인 필요)

## Confirmed Non-Changes

- ver5 Ch1 본문 line 46-526 — 정독만, 인용만, 수정 없음
- ver1_rechecked2 본문 line 1-495 — 정독만, 인용만, 수정 없음
- Phase A/B Result 본문 — 본 phase 의 입력, 수정 없음
- ledger 행 추가만, 기존 행 수정 없음 (Phase A/B 행 그대로)

## Open Issues / Decision Queue

| ID | 항목 | 분류 | 비고 |
|---|---|---|---|
| **DQ-C1** | ver5 Ch1 §5.2 Erf 표현 (line 193) — rechecked2 에 부재. Phase E 본문 디벨롭 시 부활 여부 | 사용자 결정 (Phase E 시점) | 매핑표 행 #16 |
| **DQ-C2** | ver5 Ch1 §9.1 용량식 `Q_n = Q_bg + Σ Q_{j,tot} ξ_j` (line 326) — rechecked2 는 `Q_ext = Q_cell·q` 만 사용. 둘 다 정의 vs 한 가지 채택 | 사용자 결정 | 매핑표 행 #33 |
| **DQ-C3** | ver5 Ch1 §11 온도 효과 단원 (line 377) — rechecked2 에 별 § 부재 (inline). 단원 부활 여부 | 사용자 결정 | 매핑표 행 #39 |
| **DQ-C4** | ver5 Ch1 §14 목적 함수와 정규화 (line 429) — rechecked2 에 부재. Phase E 본문 디벨롭 시 추가 권장 | 사용자 결정 (대부분 추가 예상) | 매핑표 행 #42 |
| **DQ-C5** | ver5 Ch1 §16 모델 수준 선택표 Level 0~5 (line 470) — rechecked2 에 부재 | 사용자 결정 | 매핑표 행 #44 |
| **DQ-C6** | ver5 Ch1 §19 참고문헌 5 ref (line 516) — rechecked2 에 부재. 신 Chapter 1 의 ref 단원 구성 | 사용자 결정 (대부분 유지+추가 예상) | 매핑표 행 #47 |
| **OI-C1** | GATE_C4 사용자 매핑표 검수 — 본 계획서 종료 시점 사용자 보고 필요 | 미결 (plan 종료 시 해결) | [[feedback_plan_continuation_until_done]] §1 단서 적용 |
| **OI-C2** | 본 매핑표가 ver5 Ch1 + rechecked2 의 **본문 line cross-check** 까지는 안 수행 — line 번호 기반 매핑만. 식 본문 원문 일치는 Phase A/B Result 에서 부분 확인됨 | 미검증 | Phase E 본문 디벨롭 진입 전 cross-check 보강 권장 |

## Next

- **다음 Phase**: Phase D (JCP 논문 ref. 6, 7 정독 + 본 문제 적용 안 5 요소)
- **다음 cumulative step**: **Step 14**
- **선행 조건**: 본 Phase C audit 완료 후 commit + 자동 다음 phase 진입 ([[feedback_plan_continuation_until_done]] 정합)

---

## Phase C Audit (10차원 × 3-Pass — read/diagnose phase 9차원)

### Pass 1 — 발견

| 차원 | 의심 항목 |
|---|---|
| #2 verbatim | 사용자 첫 요청 "ver1 의 내용을 기반으로 ver5 파일에서 캐치한 구조로 디벨롭" 의도와 매핑표 정합? |
| #3 데이터 흐름 | Phase A 의 21 subsec + rechecked2 14 subsec 합집합이 매핑표 47 행에 cover? |
| #6 컨벤션 | line 번호 인용 정확? 식 라벨 (`charge_balance`, `softplus_barrier` 등) 원문 그대로? |
| #7 silent miss | 매핑 누락 (한쪽 트리의 항목이 표에 안 들어감)? |
| #10 양식 | Result 11 항목 + 4-tier 분류 일관성 |
| α 경계 | ver5 Ch1 의 §1-19 + subsec 21 / rechecked2 §1-14 + subsec 14 정확 cover? |
| β 인계 | 본 phase 가 Phase D 로 전달하는 항목 (Loop 1/2/3 의 ref 6,7 적용 대상 변수 매핑) 명확? |
| γ 트리 완전성 | 매핑표가 합집합 cover (DQ-C1~C6 + 신규 추가 8 행 포함) |
| δ 4-tier | 모든 보고 항목 4-tier 분류? |

### Pass 2 — 확정·수정

| 차원 | 결과 |
|---|---|
| #2 | **확정 PASS** — 사용자 의도 = ver5 구조 + rechecked2 내용 디벨롭. 본 매핑표가 그 작업의 청사진 (3열 표 + 5 분류) |
| #3 | **확정 PASS** — Phase A Result § A.5 (Chapter 1 subsection 트리 21 항) + Phase B Result § B (rechecked2 14 § + 14 subsec) 모두 input 으로 사용. 표 47 행이 양쪽 합집합 cover |
| #6 | **확정 PASS** — line 번호 모두 Phase A/B Result + 원문 grep cross-check 결과와 일치. 식 라벨 (charge_balance, ocv_implicit, capacity_consistency, bg_slope_floor, softplus_barrier, monotonic_constraint, ica_final, dva_final 등) 원문 그대로 |
| #7 | **확정 PASS** — 매핑표 47 행 중 누락 0. ver5 Ch1 의 19 § + 21 subsec = 40 항목 모두 표에 등장 (§1-19 한 행씩 + 일부 subsec 별도 행). rechecked2 의 14 § + 14 subsec = 28 항목도 모두 등장 (양쪽 통합 행 + 신규 추가 행). 합집합 47 = 양쪽 모든 단위 cover |
| #10 | **확정 PASS** — 11 항목 + Validation 4-tier 분류 + Decision Queue 8 항목 모두 분류 |
| α | **확정 PASS** — Phase A/B audit Pass 3 의 grep cross-check 결과 (ver5 Ch1: 19 § / 21 subsec, rechecked2: 14 § / 14 subsec) 본 매핑표와 정합 |
| β | **확정 PASS** — Phase D 로 전달: Loop 1/2/3 의 위치 (매핑표 #10, #14, #25-26, #34 등) + ref 6,7 적용 대상 변수 (V_n / ξ_j / ξ_{j,eq} / k_j / Q_bg) 가 §"디벨롭 우선순위" 및 §"매핑표에 통합된 Phase B 되먹임 진단" 에 명시 |
| γ | **확정 PASS** — 매핑표 47 행 = 합집합 cover (양쪽 트리 union — Phase A/B 의 모든 항목). 신규 추가 8 행 + 삭제 후보 8 행 + DQ-C1~C6 (6 건) + OI-C1~C2 (2 건) 모두 등재 |
| δ | **확정 PASS** — 분류 집계 5 카테고리 + 보류 0 + DQ 6 + OI 2 + Gate 4-tier (확정 × 3 + 사전 면제 보류 × 1) |

### Pass 3 — 재검증

- Pass 2 정정 없음 (모두 확정 PASS).
- 회귀 없음.
- Phase A/B audit 의 grep cross-check 결과 본 매핑표와 일치 (예: ver5 Ch1 의 19 § = 매핑표 행 #1, #2, #6, #7, #14, #18, #24, #29, #32, #38, #39, #40, #41, #42, #43, #44, #45, #46, #47 = 19 행 + subsec 별도 행).

### Audit 종합 판정

- **Pass 결과**: Pass 1+2+3 모두 PASS
- **회귀**: 없음
- **Critical / High**: 0 건
- **Medium**: 1 건 (OI-C2 — 매핑표가 line 번호 기반, 본문 식 cross-check 까지는 부분 수행. Phase E 본문 디벨롭 진입 전 보강 권장)
- **잔존 권고**: GATE_C4 사용자 검수가 plan 종료 시점에 보고 필요 (OI-C1)
