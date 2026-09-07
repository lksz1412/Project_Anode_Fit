# Phase 069 Step100 — 사용자 요구사항 정식화

## Summary / 적용 범위

상태: 요구사항 정식화 검증 완료, CONTENT_VERIFIED_AWAITING_PUSH. 해당 이론·구현·자료 검증의 완료 선언이 아니다.
Step99 기준 commit: 8b27607e5d3f93bc71fee736819e2a2af90f0e85; 결과 포함 exact7/단일 parent/실제 push·live·clean 확인 완료.
활성 master: Codex/plans/2026-09-07-astra-canonical-completion-master-plan.md.
활성 detailed plan: Codex/plans/2026-09-08-phase069-canonical-audit-launch-detailed-plan.md.
정확한 8개 입력의 blob/raw·LF SHA/byte/line identity, 요구별 원천 행 범위는 PHASE_069_USER_REQUIREMENTS.json에 둔다.
요구 ID는 Step100 추적용이며 기존 carry obligation ID를 대체하거나 새 의무 개수를 더하지 않는다.

순서는 관측 → 열역학 → 동역학 → 전기화학 → 재료 → 피팅이다.
이 순서는 요구사항의 설명 순서이지 물리적 의존 관계나 최종 책 목차의 확정이 아니다.
문헌 진위·수식 유도·본문 경계·구현 충실성·3단 기록은 모든 영역에 적용되는 별도 공통 요건이다.
source-native 역사 지시와 현재 명시 지시를 구분하며, 직접 부록 예외 및 현재 작업 branch가 우선한다.
현재 요건은 모두 REQUIRED_NOT_YET_SATISFIED이다. Step106은 NOT_YET_EXECUTED, Step107은 NOT_SELECTED다.

## 관측

### P069-REQ-001 — 독립 좌표와 용량 기준

외부 누적 용량 q, 재료·상·host 조성/점유, 평형 전위·내부 전기화학 퍼텐셜, 과전압·동적 상태, 관측 cell voltage, 충전/방전/휴지 branch, 미분 부호·정규화를 서로 구분한다.

- 몰수·전하·absolute/specific/areal capacity와 Ah/C/time 변환을 가정·단위·부호까지 유도한다.
- wt%, mol fraction, active-material fraction, capacity fraction은 용량 source와 상태를 지정한 변환으로만 연결한다.
- 정의·독립변수·domain·extensive/intensive basis가 모든 관측식과 일치해야 한다.

담당: PHASE-074-FOUNDATION. 후속 Phase: 073, 074, 080.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:45–63 [section 3]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:26–26 [UDIR-06]; 2026-09-07-astra-canonical-completion-master-plan.md:371–385 [## Phase 074 — 좌표·보존·관측 기초].

### P069-REQ-002 — 측정 연산과 물리 상태의 분리

Q(V), dQ/dV 및 dV/dQ를 상태와 관측 연산으로 연결하고 sampling·voltage quantization·differentiation·noise의 영향을 별도 계층으로 둔다.

- Jacobians, singularities, 부호 및 적분 용량 대응을 중간식과 극한으로 확인한다.
- smoothing/interpolation/differentiation의 bias·해상도·uncertainty·상관 잔차를 숨기지 않는다.
- peak 높이·폭·위치·면적·비대칭·valley·background·전체 곡선을 함께 평가하고 면적 보존을 center/variance/susceptibility/entropy 보존으로 승격하지 않는다.

담당: PHASE-081-INFERENCE-UNCERTAINTY. 후속 Phase: 074, 081.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:45–63 [section 3]; PHASE_057_USER_INTENT_CONSTITUTION.md:64–83 [section 4]; PHASE_057_USER_INTENT_CONSTITUTION.md:84–99 [section 5]; PHASE_057_USER_INTENT_CONSTITUTION.md:134–147 [section 7]; PHASE_057_USER_INTENT_CONSTITUTION.md:148–176 [section 8]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:30–30 [UDIR-10]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:32–32 [UDIR-12]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; 2026-09-07-astra-canonical-completion-master-plan.md:490–506 [## Phase 081 — 열·관측·식별성·불확도].

### P069-REQ-003 — 저온·유한전류 관찰의 범위

사용자가 기록한 저온 및 충분한 휴지 대비 정전류에서의 peak lowering/broadening을 설명·재현해야 할 조건부 연구 관찰로 유지한다.

- 실제 specimen/protocol/전압 구간에서 온도·rate·rest와 peak shift/asymmetry/valley/background를 대조한다.
- 보편적 단조 법칙, 모든 재료의 필수 반응 또는 강제 fitting constraint로 가정하지 않는다.
- 관찰과 상충하는 데이터·대안 기전을 감추거나 shaping으로 제거하지 않는다.

담당: PHASE-076-NONEQUILIBRIUM. 후속 Phase: 072, 076, 077, 078, 079, 080, 086.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:84–99 [section 5]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:30–30 [UDIR-10]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:31–31 [UDIR-11]; 2026-09-07-astra-canonical-completion-master-plan.md:405–423 [## Phase 076 — 비평형 Kinetics·Transport].

## 열역학

### P069-REQ-004 — 자유에너지·상공존의 독립 근거

보존법칙/상태 변수와 재료 자유에너지, 평형, 상공존, metastability, nucleation/transition barrier의 관계를 근거 있는 식으로 유도한다.

- 원전 변수·가정·domain을 연결하고 convexification/common-tangent/binodal/spinodal/critical·희석·포화 극한을 적용범위 안에서 구분한다.
- regular-solution은 후보일 뿐 역사적 구현 삭제가 이론 검토 금지는 아니며 특정 family를 지금 채택하지 않는다.
- 경쟁하는 정당한 이론은 대안으로 보존한다; 내부 수학 검사나 fit 승패는 재료상 선택 증거가 아니다.

담당: PHASE-075-EQUILIBRIUM-PHASE. 후속 Phase: 071, 073, 075, 077, 078, 079, 082.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:7–15 [section 0]; PHASE_057_USER_INTENT_CONSTITUTION.md:64–83 [section 4]; PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_USER_INTENT_CONSTITUTION.md:134–147 [section 7]; PHASE_057_USER_INTENT_CONSTITUTION.md:229–245 [section 12]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:26–26 [UDIR-06]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:37–37 [UDIR-17]; 2026-09-07-astra-canonical-completion-master-plan.md:386–404 [## Phase 075 — 평형·상공존·상장].

### P069-REQ-005 — 엔트로피와 열의 상태함수 유도

entropy와 reversible heat를 채택 자유에너지의 온도 미분 및 반응 좌표로부터 유도하며 물리 기여를 분리한다.

- configurational/vibrational/electronic/elastic/mixing 기여와 적용 가능한 경우의 가정을 명시한다.
- 전극 entropy coefficient와 full-cell 가역열을 동일 부호·control-volume·capacity 기준으로 연결한다.
- 경험적 skew/gallery basis/smoothing은 상태함수로 넣지 않는다; 내부 fit width를 entropy로 해석하지 않는다.

담당: PHASE-081-INFERENCE-UNCERTAINTY. 후속 Phase: 074, 075, 078, 081, 082.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:64–83 [section 4]; PHASE_057_USER_INTENT_CONSTITUTION.md:134–147 [section 7]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:26–26 [UDIR-06]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:27–27 [UDIR-07]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:28–28 [UDIR-08]; 2026-09-07-astra-canonical-completion-master-plan.md:490–506 [## Phase 081 — 열·관측·식별성·불확도].

### P069-REQ-006 — 형상 모수의 물리적 권위 제한

alpha/width/lag/gallery/background 및 regular-solution interaction 값을 곡선 형상, 상태함수, 재료상 또는 상수로 혼동하지 않는다.

- 포화·축퇴한 모수는 material constant로 보고하지 않는다.
- 패배한 curve fit의 interaction 값을 phase 판정으로 전이하지 않는다.
- skew-logistic 면적 보존의 제한을 유지하며 물리적 지위 변경은 원문·유도·외부 자료가 함께 지지해야 한다.

담당: PHASE-082-EQUATION-FREEZE. 후속 Phase: 075, 077, 079, 081, 082.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:134–147 [section 7]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:36–36 [UDIR-16]; 2026-09-07-astra-canonical-completion-master-plan.md:507–521 [## Phase 082 — Canonical Equation Freeze].

## 동역학

### P069-REQ-007 — 장벽·전이율의 T/전위/조성/과전압 의존

상전이 활성화 장벽과 전이율에 대한 온도·내부 전위·조성·과전압 의존을 반응/수송/전하 보존과 연결한다.

- 출발 반응식, affinity, detailed balance, forward/reverse rate 및 coarse-graining 가정을 유도한다.
- 전류를 근거 없는 독립 barrier knob로 넣지 않는다. 직접 I 의존은 이를 만드는 비평형 열역학 또는 stochastic driving 유도가 있을 때만 검토한다.
- 전위·온도·전류의 효과가 구분 가능한지를 데이터 요구와 연결한다.

담당: PHASE-076-NONEQUILIBRIUM. 후속 Phase: 071, 076, 081.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:64–83 [section 4]; PHASE_057_USER_INTENT_CONSTITUTION.md:84–99 [section 5]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:31–31 [UDIR-11]; 2026-09-07-astra-canonical-completion-master-plan.md:405–423 [## Phase 076 — 비평형 Kinetics·Transport].

### P069-REQ-008 — 시간·휴지·반전·유한 창 상태 보존

충방전·휴지·반전·pulse·비단조 protocol의 순서와 초기/최종 상태를 보존하는 동적 표현을 요구한다.

- signed time/capacity evolution, state transfer, finite-window remaining capacity/tail/exhaustion을 검산한다.
- I→0, frozen-state, fast-relaxation, transport-free 및 필요한 입자 크기 극한을 분리한다.
- 시간/길이/grid 규칙으로 물리 branch가 몰래 바뀌지 않아야 하며 C13/C14/C15 carry의 원래 acceptance를 유지한다.

담당: PHASE-076-NONEQUILIBRIUM. 후속 Phase: 076, 083, 084, 088.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:45–63 [section 3]; PHASE_057_USER_INTENT_CONSTITUTION.md:64–83 [section 4]; PHASE_057_USER_INTENT_CONSTITUTION.md:84–99 [section 5]; PHASE_057_USER_INTENT_CONSTITUTION.md:177–190 [section 9]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:31–31 [UDIR-11]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:32–32 [UDIR-12]; 2026-09-07-astra-canonical-completion-master-plan.md:405–423 [## Phase 076 — 비평형 Kinetics·Transport].

### P069-REQ-009 — 기전 및 비균질성의 분해

charge transfer, solid/electrolyte transport, strain/disorder/particle-host heterogeneity, nucleation 및 hysteresis/dissipative internal variables를 한 latent-state 계보로 연결하되 구분한다.

- 한 개 width/lag/background/convolution이 모든 계층을 대신하지 않게 하고 기전별 characteristic scale과 필요한 증거를 제시한다.
- 동일 symbol을 서로 다른 자유에너지·장벽·fit-kernel 의미로 재사용하지 않는다.
- 단일 exponential tail 또는 reduced law의 실패 범위와 구별할 수 없는 기전은 명시한다.

담당: PHASE-076-NONEQUILIBRIUM. 후속 Phase: 073, 076, 077, 078, 079, 080, 081.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:64–83 [section 4]; PHASE_057_USER_INTENT_CONSTITUTION.md:84–99 [section 5]; PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:31–31 [UDIR-11]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; 2026-09-07-astra-canonical-completion-master-plan.md:405–423 [## Phase 076 — 비평형 Kinetics·Transport].

## 전기화학

### P069-REQ-010 — 전하 보존과 공통 전압

전하 보존과 공통 cell voltage 제약을 먼저 세우고 각 전극·constituent의 내부 응답과 관측 전압을 조립한다.

- half-cell/full-cell, lithiation/delithiation, signed current 및 equilibrium/terminal voltage를 구분한다.
- 내부 퍼텐셜을 결정하는 보존 관계와 과전압·저항·수송 분해를 중간식으로 연결한다.
- 전하·용량·에너지 및 thermal 결합 단위/부호를 독립 검산한다.

담당: PHASE-074-FOUNDATION. 후속 Phase: 074, 076, 080, 081.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:45–63 [section 3]; PHASE_057_USER_INTENT_CONSTITUTION.md:64–83 [section 4]; PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:26–26 [UDIR-06]; 2026-09-07-astra-canonical-completion-master-plan.md:371–385 [## Phase 074 — 좌표·보존·관측 기초].

### P069-REQ-011 — 반응·수송·열을 통한 전류 영향

전류의 영향은 보존, charge transfer, solid/electrolyte/porous transport, 열 및 protocol이 내부 상태에 전달하는 경로로 설명한다.

- 교환전류·active area·조성·온도·diffusion/charge-transfer/phase-boundary scale의 source 가정과 유도 경계를 보존한다.
- electrode equilibrium과 finite-rate current sharing의 차이를 유지하며 필요한 coupling 수준은 자료 확보 후 선택한다.
- 정적 call graph는 실제 dynamic dispatch 또는 runtime call order 증거가 아니며 C03 원조건을 남긴다.

담당: PHASE-076-NONEQUILIBRIUM. 후속 Phase: 076, 080, 081, 083, 088.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:64–83 [section 4]; PHASE_057_USER_INTENT_CONSTITUTION.md:84–99 [section 5]; PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_USER_INTENT_CONSTITUTION.md:229–245 [section 12]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:31–31 [UDIR-11]; 2026-09-07-astra-canonical-completion-master-plan.md:405–423 [## Phase 076 — 비평형 Kinetics·Transport].

## 재료

### P069-REQ-012 — Graphite

graphite staging/gallery occupation/phase coexistence를 ICA feature와 연결하되 curve basis/gallery/component 수를 실제 phase 수로 가정하지 않는다.

- primary diffraction/thermodynamic 자료로 transition/조성 interval/용량 기여를 연결한다.
- free-energy 후보의 convexification/critical limit/finite-width, disorder/particle size, hysteresis와 저온 kinetics를 유도·대조한다.
- four-transition/seven-component 분해는 evidence tier를 부여하고 multi-T/rate/equilibrium 자료의 식별성을 따로 검증한다.

담당: PHASE-077-GRAPHITE-CLOSURE. 후속 Phase: 071, 072, 077, 081, 086.
재료 범위: graphite.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:29–29 [UDIR-09]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; 2026-09-07-astra-canonical-completion-master-plan.md:424–440 [## Phase 077 — Graphite Material Closure].

### P069-REQ-013 — Doped high-voltage LCO

일반 LCO surrogate와 doped high-voltage LCO를 구분하고 도펀트별 화학·구조·전자·산소 및 열역학 경로를 보존한다.

- dopant species/site/concentration, defect chemistry, oxygen stability/redox/loss, phase degradation, cutoff, high-voltage kinetics/transport 근거를 연결한다.
- order–disorder/metal–insulator/coexistence, entropy·electronic contribution은 원전의 적용 범위 밖으로 일반화하지 않는다.
- graphite의 소프트웨어 구조 재사용을 같은 물리의 근거로 삼지 않고 doped held-out 조건을 요구한다.

담당: PHASE-078-LCO-CLOSURE. 후속 Phase: 071, 072, 078, 081, 086.
재료 범위: doped_high_voltage_LCO.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:29–29 [UDIR-09]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; 2026-09-07-astra-canonical-completion-master-plan.md:441–457 [## Phase 078 — Doped High-voltage LCO Closure].

### P069-REQ-014 — Si

Si의 큰 변형, chemo-mechanics, stress-coupled chemical potential, amorphization/crystallization, hysteresis 및 host interaction을 독립 재료 계보로 다룬다.

- crystalline/amorphous lithiation sequence와 조성 좌표를 원문에 연결한다.
- 응력·팽창·plasticity/fracture/loss of active material의 관측 영향과 rate/temperature/size 의존을 구분한다.
- 문헌 case 값은 dataset seed이지 보편 default가 아니며 empirical component를 상으로 고정하지 않는다.

담당: PHASE-079-SILICON-CLOSURE. 후속 Phase: 071, 072, 079, 081, 086.
재료 범위: Si.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:29–29 [UDIR-09]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; 2026-09-07-astra-canonical-completion-master-plan.md:458–474 [## Phase 079 — Si/SiOx/Si–C Closure].

### P069-REQ-015 — SiOx

SiOx를 Si에 몰래 통합하지 않고 irreversible conversion, active Si와 inactive matrix의 용량 회계를 유지한다.

- oxide conversion의 화학·조성·비가역 용량과 이후 active phase의 가역 반응을 source/data에 연결한다.
- Si와 공유하는 chemo-mechanical/hysteretic 경로와 SiOx만의 차이를 구분한다.
- 공개 또는 사용자 specimen/protocol 근거가 없으면 해당 claim을 conditional로 남기고 재료 범위를 삭제하지 않는다.

담당: PHASE-079-SILICON-CLOSURE. 후속 Phase: 071, 072, 079, 086.
재료 범위: SiOx.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_USER_INTENT_CONSTITUTION.md:148–176 [section 8]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:29–29 [UDIR-09]; 2026-09-07-astra-canonical-completion-master-plan.md:458–474 [## Phase 079 — Si/SiOx/Si–C Closure].

### P069-REQ-016 — Si-C

Si–C composite의 active phases, carbon/binder/conductive matrix 및 구조·기계 효과를 구분한다.

- active/inactive matrix와 용량 basis를 명시하고 Si 단독 값의 전이를 검증한다.
- large strain/stress/phase sequence/host interaction의 필요한 근거와 held-out specimen을 지정한다.
- 문헌 seed나 fit component를 보편 물성 또는 phase identity로 승격하지 않는다.

담당: PHASE-079-SILICON-CLOSURE. 후속 Phase: 071, 072, 079, 086.
재료 범위: Si-C.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_USER_INTENT_CONSTITUTION.md:148–176 [section 8]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:29–29 [UDIR-09]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; 2026-09-07-astra-canonical-completion-master-plan.md:458–474 [## Phase 079 — Si/SiOx/Si–C Closure].

### P069-REQ-017 — Graphite+Si blend

각 constituent의 보존법칙·공통 전압·용량 배분과 finite-rate current sharing을 결합한다.

- wt%→capacity fraction은 constituent별 capacity source와 lithiation state를 명시한 변환으로만 수행한다.
- 단순 가중합, common-potential equilibrium, porous-electrode current sharing의 성립/실패 조건을 구분한다.
- 단독 소재 calibration과 blend transfer/held-out composition·rate·temperature 검증을 분리한다.

담당: PHASE-080-BLEND-CLOSURE. 후속 Phase: 072, 080, 081, 086.
재료 범위: graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:45–63 [section 3]; PHASE_057_USER_INTENT_CONSTITUTION.md:100–133 [section 6]; PHASE_057_USER_INTENT_CONSTITUTION.md:148–176 [section 8]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:29–29 [UDIR-09]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; 2026-09-07-astra-canonical-completion-master-plan.md:475–489 [## Phase 080 — Graphite+Si Blend Closure].

## 피팅

### P069-REQ-018 — 실제 피팅 가치와 모델 계층

기존에 데이터에서 작동한 empirical fitting 능력을 보존하되 empirical/reduced-physics/production-physics를 별개 권위로 유지한다.

- 보존할 경험적 성공분은 EMPIRICAL_ONLY와 적용 범위로 표시하거나 검증된 물리 계층에 연결한다.
- R², naive BIC, in-sample figure, fit 성공만으로 phase/gallery/성분/물리상수·기전·최종 모델을 정하지 않는다.
- v1.0.21–v1.0.23 Fable보다 나은 결과라는 목표는 이름/모델 명성 대신 실제 유도·자료·검증으로 판단한다.

담당: PHASE-086-MATERIAL-VALIDATION. 후속 Phase: 069, 081, 083, 086.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:134–147 [section 7]; PHASE_057_USER_INTENT_CONSTITUTION.md:148–176 [section 8]; PHASE_057_USER_INTENT_CONSTITUTION.md:191–206 [section 10]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:35–35 [UDIR-15]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:36–36 [UDIR-16]; 2026-09-07-astra-canonical-completion-master-plan.md:575–593 [## Phase 086 — 실제 데이터 Calibration과 Validation].

### P069-REQ-019 — 실제 자료·provenance와 부족한 근거

모든 재료군에 실제 공개 자료를 우선 조사하며 multi-T, multi-current/rate, rest/equilibrium, independent cell/specimen과 raw/preprocessing provenance를 요구한다.

- 현재 접근 가능·후보지만 미확인·사용자 자료 필요·unavailable·synthetic-only를 구분하고 접근을 추측하지 않는다.
- specimen/chemistry/loading/capacity basis/protocol/replicate/uncertainty/license·원자료 hash를 확보한 자료만 해당 validation에 쓴다.
- synthetic parameter recovery는 내부 대수/구현 시험이며 외부 재료 증거가 아니다. 부족함은 claim/material별 UNVERIFIED/CONDITIONAL로 남긴다.

담당: PHASE-072-DATA-FEASIBILITY. 후속 Phase: 069, 072, 081, 086.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:148–176 [section 8]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:29–29 [UDIR-09]; 2026-09-07-astra-canonical-completion-master-plan.md:331–351 [## Phase 072 — 데이터 Provenance와 Feasibility].

### P069-REQ-020 — 식별성·불확도와 독립 검증

calibration과 validation을 분리하고 보존/단위/부호/극한/모수회복/식별성/전체곡선/외부 구조 증거를 함께 요구한다.

- structural/practical identifiability, profile/covariance 및 필요한 Jacobian/posterior/condition 검사로 모수 조합·축퇴를 확인한다.
- peak/valley/area/background/full-curve residual, preprocessing uncertainty·residual correlation을 평가한다.
- held-out condition/cell/material transfer와 independent structural/thermodynamic evidence를 요구한다; 공개 자료 부족은 explicit limitation이다.

담당: PHASE-081-INFERENCE-UNCERTAINTY. 후속 Phase: 072, 081, 086, 088.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:148–176 [section 8]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:29–29 [UDIR-09]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; 2026-09-07-astra-canonical-completion-master-plan.md:490–506 [## Phase 081 — 열·관측·식별성·불확도].

### P069-REQ-021 — 정당한 수치 방법과 숨은 조작 금지

invalid domain/NaN/nonphysical input의 명시적 실패와 수치 오차 제어는 허용하되 물리값을 조용히 바꾸는 cap/clip/clamp/softplus/threshold/grid guard/사후 smoothing은 금지한다.

- adaptive error control/event detection/conservative integration/domain-preserving parameterization을 우선 검토한다.
- 필요 regularization은 목적·bias·convergence·제거 극한을 기록하고 fixed grid가 물리 branch를 선택하지 않게 한다.
- default 시험 전에 그 default를 다른 값으로 바꾸지 않는다. legacy bit-exact regression과 새 physics acceptance, conformance와 physical validity를 분리한다.

담당: PHASE-083-IMPLEMENTATION-CONTRACT. 후속 Phase: 076, 083, 084, 085, 088.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:177–190 [section 9]; PHASE_057_USER_INTENT_CONSTITUTION.md:191–206 [section 10]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:32–32 [UDIR-12]; 2026-09-07-astra-canonical-completion-master-plan.md:522–538 [## Phase 083 — Theory–Implementation Contract].

## 공통 문헌·문서·구현·작업 규율

### P069-REQ-022 — 진짜 문헌과 load-bearing 근거

사용자가 우려한 가짜 논문·DOI를 금지하고 실재성 확인과 실제 claim support를 독립 검증한다.

- 논문/교재의 저자·제목·연도·출판 정보·DOI 및 correction/retraction은 실제 record로 확인한다.
- load-bearing 주장·수식·모수는 확보한 원문 hash와 page/section/equation/figure/table anchor, 변수 mapping, 불가 가정까지 기록한다.
- metadata/abstract/secondary citation/internal consistency는 원문 support를 대신하지 않는다. 미확보 Ref7 및 undefined citation은 UNVERIFIED/GROUND_NOT_FOUND이지 invented repair가 아니다.
- review/textbook은 배경·종합, 구체적 물리/데이터 주장은 primary source 중심으로 범위를 분리한다.

담당: PHASE-071-REFERENCE-TRUTH. 후속 Phase: 071, 082, 088.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:28–44 [section 2]; PHASE_057_USER_INTENT_CONSTITUTION.md:246–255 [section 13]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:28–28 [UDIR-08]; 2026-09-07-astra-canonical-completion-master-plan.md:310–330 [## Phase 071 — 문헌·DOI Truth Audit].

### P069-REQ-023 — 대학원 교재이면서 리뷰 논문 수준

독자가 문건만으로 통계역학→열역학→상전이→반응속도→수송→열→관측량의 연결을 따라갈 수 있게 상세히 전개한다.

- 화학식·수식 중심으로 출발식→정의/가정→연산→중간식→결과→단위/부호/domain/극한/보존을 생략하지 않는다.
- 비유나 설명만으로 유도 다리를 대체하지 않고 경쟁 이론·적용 범위·한계를 원전 깊이로 검토한다.
- load-bearing 식은 Phase082 독립 재유도와 Phase088 전체 검독을 통과해야 한다.

담당: PHASE-082-EQUATION-FREEZE. 후속 Phase: 074, 075, 076, 077, 078, 079, 080, 081, 082, 087, 088.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:28–44 [section 2]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:27–27 [UDIR-07]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:28–28 [UDIR-08]; 2026-09-07-astra-canonical-completion-master-plan.md:507–521 [## Phase 082 — Canonical Equation Freeze].

### P069-REQ-024 — 본문 경계와 지정 예외

학술 본문·caption·footnote·visible heading에 코드/함수/class/key/file/API/test/branch/commit/phase/step/작업 이력 및 방어적 자기평가를 넣지 않는다.

- 구현 설명은 지정 implementation appendix OR separate companion에만 둔다. 이전057 companion-only 표현은 이 예외를 축소하지 않는다.
- 수식 유도 부록을 구현 설명을 숨기는 통로로 쓰지 않고 순수 유도와 지정 구현 예외의 경계를 명확히 한다.
- lexical scan과 전문 의미 검독을 모두 수행하며 작업 날짜·audit·commit hash는 본문/주석 대신 별도 결과서·ledger에 둔다.

담당: PHASE-087-MANUSCRIPT-ASSEMBLY. 후속 Phase: 069, 073, 083, 087, 088, 089.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:28–44 [section 2]; PHASE_057_USER_INTENT_CONSTITUTION.md:207–228 [section 11]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:25–25 [UDIR-05]; 2026-09-07-astra-canonical-completion-master-plan.md:594–610 [## Phase 087 — 학술 원고 조립]; 2026-09-07-astra-canonical-completion-master-plan.md:156–157 [designated implementation appendix OR separate companion].

### P069-REQ-025 — 이론에서 구현으로의 완전한 추적

이론이 물리·화학의 권위이며 implementation companion과 code는 하류다. 코드를 맞추기 위해 이론을 사후 변경하지 않는다.

- 모든 계산 가능한 채택식에 claim/equation ID와 가정·unit/domain/limit/required data/consumer 연결을 둔다.
- 모든 physical branch는 채택 claim으로 역추적되고 code-only physical knob/default/branch를 금지한다.
- 미구현 채택식을 THEORY_ONLY로 숨겨 acceptance에 포함시키지 않는다. conformance test와 physical-validity test는 구분한다.
- empirical component는 EMPIRICAL_ONLY 범위로 보존하며 arbitrary implementation default를 선택하지 않는다.

담당: PHASE-083-IMPLEMENTATION-CONTRACT. 후속 Phase: 073, 082, 083, 084, 085, 088.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:28–44 [section 2]; PHASE_057_USER_INTENT_CONSTITUTION.md:191–206 [section 10]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:26–26 [UDIR-06]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:36–36 [UDIR-16]; 2026-09-07-astra-canonical-completion-master-plan.md:522–538 [## Phase 083 — Theory–Implementation Contract].

### P069-REQ-026 — 기준선·계보·fork 보존

v1.0.10–v1.0.25.2 이력/의도를 감사한 범위와 미검증을 보존하고 v1.0.26A/B 실험 labels를 승인된 새 학술 release로 취급하지 않는다.

- latest filename/handover 완결/PASS commit subject/AI selfapproval/모델 명성은 채택 권위가 아니다.
- historical codex/lib-physics-endgame-v1025_2는 현재 protected; 작업은 codex/anode-fit-v1025_2-canonical-completion에서만 수행한다.
- Claude/main/보호·frozen refs/과거 계획·완료 결과·원문은 덮어쓰지 않으며 채택/수정은 이후 Codex-owned tree에서 file/equation별로 수행한다.
- Step106에서1520paths/862 baseline 또는 증거로 정정한 denominator의 실제 전체 coverage를 판단한다.

담당: PHASE-070-POST-AUDIT-FREEZE. 후속 Phase: 069, 070, 090.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:7–15 [section 0]; PHASE_057_USER_INTENT_CONSTITUTION.md:16–27 [section 1]; PHASE_057_USER_INTENT_CONSTITUTION.md:207–228 [section 11]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:21–21 [UDIR-01]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:22–22 [UDIR-02]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:23–23 [UDIR-03]; 2026-09-07-astra-canonical-completion-master-plan.md:293–309 [## Phase 070 — Post-audit 기준선 동결].

### P069-REQ-027 — 과거 국소 지시와 현재 승인 구분

저장된 DIRECT_CURRENT는 과거 시점의 지시 해석 기록이지 이번 사용자의 축어 발언이나 새로운 승인이 아니다.

- v1.0.25 local patch 범위·원본 파일명 유지·regsol 구현 삭제는 해당 역사로 남기며 endgame 설계의 영구 금지로 자동 승계하지 않는다.
- 과거 theory=regsol/fitting=logistic 승인은 현 100% 이론–구현 단일 논리의 최종 architecture 승인이 아니다.
- 기존 사용자 변수/함수/파일명은 임의 변경하지 않는다. 새로운 Codex-owned 설계가 필요하면 현재 허용 범위와 후속계획을 따로 적용한다.
- 헌법 변경은 직접 후속 지시, 원전/자료/재유도의 오류 입증, 또는 양립 불가 requirement의 사용자 선택에만 근거하고 원문을 지우지 않은 supersession 기록을 남긴다.

담당: PHASE-069-LAUNCH-INTEGRATION. 후속 Phase: 069, 070, 073.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:16–27 [section 1]; PHASE_057_USER_INTENT_CONSTITUTION.md:229–245 [section 12]; PHASE_057_USER_INTENT_CONSTITUTION.md:246–255 [section 13]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:37–37 [UDIR-17]; 2026-09-07-astra-canonical-completion-master-plan.md:256–277 [## Phase 069 — 전체 종합·새 작업 착수 게이트].

### P069-REQ-028 — 3단 계획·누적 Step·컴팩션 복구

작업 전 master, phase 시작 전 detailed plan, Step 완료 후 result를 저장하고 phase와 관계없이 누적 번호를 이어간다.

- Codex/plans에는 두 계획, Codex/results에는 Step/phase result·검수·ledger·handover, Codex/docs에는 학술 LaTeX/PDF·companion을 둔다. Codex/work는 실행 보조만이다.
- 매 Step 입력/실제 read 범위/변경 파일/명령·runtime·exit·outputs/검증/미확인/다음 조건을 기록한다.
- 컴팩션·교체·중단 후 master와 current detailed plan과 직전 result를 1–EOF 재독하고 WIP/control/Git 상태를 대조한다.
- 읽지 않은 source/미실행 test를 PASS로 쓰지 않고 원천 변경 시 stale evidence를 final source 검증으로 갱신한다.
- 삭제·재배치·수정마다 원래 claim/asset, 변경 이유와 대체 위치를 기록한다. 기존 완료 계획·결과를 덮어쓰지 않고 새 addendum/supersession으로 관계를 보존한다.

담당: ROOT-EXECUTION-CONTROLLER. 후속 Phase: 069, 070, 071, 072, 073, 074, 075, 076, 077, 078, 079, 080, 081, 082, 083, 084, 085, 086, 087, 088, 089, 090.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:207–228 [section 11]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:34–34 [UDIR-14]; 2026-09-07-astra-canonical-completion-master-plan.md:181–232 [## Execution and Compaction Recovery Protocol].

### P069-REQ-029 — Step별 결과 포함 commit·push와 역할 유지

각 Step 결과를 포함한 exact path commit과 active branch push 후 live origin=HEAD·단일 parent·clean tree를 확인하고 다음 Step으로 간다.

- 계획 승인/재개를 반복 질문하지 않고 현재 승인 범위는 연속 실행한다; 기존 세션/agent 역할을 임의로 섞지 않는다.
- root가 최종 통합/쓰기/Git 책임을 가지며 독립 검독은 병렬화하되 source/범위/금지/실제read를 명시한다.
- 외부 원문/데이터 부족은 claim별 제한으로 기록하고 독립 가능한 작업을 진행한다. 아래 일곱 hard-stop 조건이 발생하면 사실과 필요한 결정을 보고한다.
- 큰 반복 validator/불변 자료 재검사를 새 근거 없이 늘리지 않되 필수 원전·수식·PDF·clean-clone gates를 삭제하지 않는다.
- 중단 조건 1: protected branch에 예상하지 못한 변경이 발생한 경우.
- 중단 조건 2: active remote branch가 local 예상과 다른 방향으로 이동한 경우.
- 중단 조건 3: 동일 원인의 push가 세 차례 연속 실패한 경우.
- 중단 조건 4: 비공개·유료 원문 또는 자격 증명이 전체 다음 단계의 필수 입력이 된 경우.
- 중단 조건 5: 상충하는 사용자 지시를 대안 병기로도 보존할 수 없는 경우.
- 중단 조건 6: 근거 없이 material model 또는 parameter를 정본으로 골라야만 진행 가능한 경우.
- 중단 조건 7: validator 실패가 과학 결과 변경인지 환경 부채인지 세 번의 독립 조사 후에도 분리되지 않는 경우.

담당: ROOT-EXECUTION-CONTROLLER. 후속 Phase: 069, 070, 071, 072, 073, 074, 075, 076, 077, 078, 079, 080, 081, 082, 083, 084, 085, 086, 087, 088, 089, 090.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:207–228 [section 11]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:24–24 [UDIR-04]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:34–34 [UDIR-14]; 2026-09-07-astra-canonical-completion-master-plan.md:181–232 [## Execution and Compaction Recovery Protocol]; 2026-09-07-astra-canonical-completion-master-plan.md:711–720 [## Hard Stops]; 2026-09-07-astra-canonical-completion-master-plan.md:703–710 [## Autonomous Decision Policy].

### P069-REQ-030 — LaTeX/PDF와 최종 전달

학술 PDF는 LaTeX 원천에서 생성하고 검증된 유도를 Codex/docs에 증분 축적한다. 감사 완료와 흑연 장/전체 release 완료를 구분한다.

- 순수본문/유도 부록/구현 예외·companion 경계를 지키며 문헌·식·그림/표 cross-reference를 검사한다.
- clean multi-pass build, citation/reference/glyph 오류, page별 render·전 페이지 시각검독·밀집식/페이지전환 original-resolution 검독, source/PDF hash 대응을 수행한다.
- 최종 clean-clone에서 시험·재현·PDF rebuild 후 source/PDF/companion/evidence·manifest·limitations를 ZIP으로 전달한다.
- 18–30시간 graphite/40–80시간 전체 등의 기존 추정은 조건부 과거 snapshot이지 보장 마감 또는 현재완료 선언이 아니다.

담당: PHASE-090-RELEASE-CONTROLLER. 후속 Phase: 073, 074, 075, 076, 077, 078, 079, 080, 081, 087, 088, 089, 090.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:28–44 [section 2]; PHASE_057_USER_INTENT_CONSTITUTION.md:207–228 [section 11]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:27–27 [UDIR-07]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:28–28 [UDIR-08]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:35–35 [UDIR-15]; 2026-09-07-astra-canonical-completion-master-plan.md:643–657 [## Phase 090 — Clean-clone Release와 Handover]; 2026-09-07-astra-canonical-completion-master-plan.md:21–60 [## Estimated Remaining Work and Delivery Criteria]; 2026-09-07-astra-canonical-completion-master-plan.md:628–642 [## Phase 089 — LaTeX·PDF Release QA]; 2026-09-07-astra-canonical-completion-master-plan.md:278–292 [## Phase 070–090 — 단계별 원문 과제 승계와 증분 원고 작성].

### P069-REQ-031 — 미확정 선택과 순차 착수 gate

최종 model family·material state/closure·stochastic/deterministic kinetics·porous coupling·noise likelihood·software architecture·장 번호/분량·defaults는 필요한 증거와 승인된 단계 전에 확정하지 않는다.

- Step106 fullcoverage와107 GO/CONDITIONAL_GO 전070–090 실행을 금지한다. NO_GO는 scoped repair addendum으로 되돌린다.
- 과학적으로 가능성이 여러 개면 대안군을 유지하며 사용자가 없는 동안 arbitrary canonical model/default를 택하지 않는다.
- 헌법상 아직 결정하지 않은 graphite/LCO/Si/kinetics/transport/observation/package/book/defaults 9영역을 모두 보존한다.
- model 선택의 실질 과학 차이가 근거로 좁혀진 뒤에도 필요한 사용자 선택은 명확한 영향·이유와 함께 요청한다.

담당: PHASE-069-LAUNCH-INTEGRATION. 후속 Phase: 069, 070, 071, 072, 073, 082.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:7–15 [section 0]; PHASE_057_USER_INTENT_CONSTITUTION.md:229–245 [section 12]; PHASE_057_USER_INTENT_CONSTITUTION.md:246–255 [section 13]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:35–35 [UDIR-15]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:37–37 [UDIR-17]; 2026-09-07-astra-canonical-completion-master-plan.md:256–277 [## Phase 069 — 전체 종합·새 작업 착수 게이트].

### P069-REQ-032 — 미해결 원조건과 사용자 우려 보존

현재316 registered carry와 C03/C06의 별도 기존 source predicates 및 여덟 OPEN_USER_CONCERN을 완료로 승격하지 않는다.

- 222inherited+94new와655dispositions의 원 ID/type/owner/acceptance/origin/relations를 유지하고 zero inherited closure를 지킨다.
- C03 실제 runtime order/dynamic dispatch는 Phase083, C06 required dual-runtime test/demo 실행 또는 owner-bound withholding은 Phase088의 원 acceptance를 유지한다.
- C03/C06 exact316route NOT_FOUND를 narrower owner match로 대신하거나 새 obligation ID/318 distinct denominator로 변경하지 않는다; Step105에서 launch inputs로 명시 연결한다.
- Ref7/fulltext, rawarrays/original optimizer, specimen/protocol/held-out/material authority, body/PDF, incomplete internal predicates를 분리하고 Step107까지 사용자 우려를 OPEN으로 남긴다.

담당: PHASE-069-LAUNCH-INTEGRATION. 후속 Phase: 069, 071, 072, 074, 076, 077, 078, 079, 080, 081, 083, 086, 088, 089.
재료 범위: graphite, doped_high_voltage_LCO, Si, SiOx, Si-C, graphite+Si_blend.
근거: PHASE_057_USER_INTENT_CONSTITUTION.md:7–15 [section 0]; PHASE_057_USER_INTENT_CONSTITUTION.md:207–228 [section 11]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:21–21 [UDIR-01]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:26–26 [UDIR-06]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:29–29 [UDIR-09]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:30–30 [UDIR-10]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:31–31 [UDIR-11]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:33–33 [UDIR-13]; PHASE_057_CURRENT_USER_DIRECTION_REGISTER.md:34–34 [UDIR-14]; 2026-09-07-astra-canonical-completion-master-plan.md:256–277 [## Phase 069 — 전체 종합·새 작업 착수 게이트].

## 지시·우려·헌법의 역추적

| 원천 방향 | 요구 ID |
|---|---|
| UDIR-01 | P069-REQ-026, P069-REQ-032 |
| UDIR-02 | P069-REQ-026 |
| UDIR-03 | P069-REQ-026 |
| UDIR-04 | P069-REQ-029 |
| UDIR-05 | P069-REQ-024 |
| UDIR-06 | P069-REQ-001, P069-REQ-004, P069-REQ-005, P069-REQ-010, P069-REQ-025, P069-REQ-032 |
| UDIR-07 | P069-REQ-005, P069-REQ-023, P069-REQ-030 |
| UDIR-08 | P069-REQ-005, P069-REQ-022, P069-REQ-023, P069-REQ-030 |
| UDIR-09 | P069-REQ-012, P069-REQ-013, P069-REQ-014, P069-REQ-015, P069-REQ-016, P069-REQ-017, P069-REQ-019, P069-REQ-020, P069-REQ-032 |
| UDIR-10 | P069-REQ-002, P069-REQ-003, P069-REQ-032 |
| UDIR-11 | P069-REQ-003, P069-REQ-007, P069-REQ-008, P069-REQ-009, P069-REQ-011, P069-REQ-032 |
| UDIR-12 | P069-REQ-002, P069-REQ-008, P069-REQ-021 |
| UDIR-13 | P069-REQ-002, P069-REQ-004, P069-REQ-006, P069-REQ-009, P069-REQ-012, P069-REQ-013, P069-REQ-014, P069-REQ-016, P069-REQ-017, P069-REQ-018, P069-REQ-020, P069-REQ-032 |
| UDIR-14 | P069-REQ-028, P069-REQ-029, P069-REQ-032 |
| UDIR-15 | P069-REQ-018, P069-REQ-030, P069-REQ-031 |
| UDIR-16 | P069-REQ-006, P069-REQ-018, P069-REQ-025 |
| UDIR-17 | P069-REQ-004, P069-REQ-027, P069-REQ-031 |

| 미해결 사용자 우려 | 요구 ID | 상태 |
|---|---|---|
| OPEN_USER_CONCERN-1 | P069-REQ-026, P069-REQ-032 | OPEN_USER_CONCERN |
| OPEN_USER_CONCERN-2 | P069-REQ-018, P069-REQ-019, P069-REQ-020, P069-REQ-025 | OPEN_USER_CONCERN |
| OPEN_USER_CONCERN-3 | P069-REQ-003, P069-REQ-007, P069-REQ-008, P069-REQ-009 | OPEN_USER_CONCERN |
| OPEN_USER_CONCERN-4 | P069-REQ-007, P069-REQ-011, P069-REQ-020 | OPEN_USER_CONCERN |
| OPEN_USER_CONCERN-5 | P069-REQ-013, P069-REQ-019, P069-REQ-020 | OPEN_USER_CONCERN |
| OPEN_USER_CONCERN-6 | P069-REQ-006, P069-REQ-012, P069-REQ-014, P069-REQ-017, P069-REQ-018 | OPEN_USER_CONCERN |
| OPEN_USER_CONCERN-7 | P069-REQ-018, P069-REQ-020, P069-REQ-021, P069-REQ-025, P069-REQ-031 | OPEN_USER_CONCERN |
| OPEN_USER_CONCERN-8 | P069-REQ-024, P069-REQ-030 | OPEN_USER_CONCERN |

헌법 section0–13의 전체 번호 조항·sub-bullet은 각 요구의 원천 범위와 JSON constitution_coverage로 역추적한다.
원문은 축어 대화록이 아니므로 DIRECT_CURRENT라는 과거 표기를 이번 발언의 직접 인용 또는 새 승인으로 표시하지 않는다.

## 현재 결정과 미결 경계

지정 implementation appendix OR separate companion 예외는 유지한다. 일반 구현 section을 새 예외로 만들지 않는다.
기존 역사 branch는 보호하며 codex/anode-fit-v1025_2-canonical-completion이 유일한 현재 쓰기 branch다.
316개 등록 carry는222inherited+94new, inherited closure0이다. C03/C06은 별도 기존 원조건이고318개의 독립 의무라고 합산하지 않는다.
Step105가 두 조건을 launch inputs로 연결해야 하며 source-native owner/acceptance를 바꾸지 않는다.
원 optimizer 실행은 성공/수렴이 아니며 candidate51실행=49PASS+2historicalhashFAIL 상태를 유지한다.
내부 검산, bounded C1/정규화/header 판단, metadata DOI 및 synthetic/자기일치 결과는 material/원전/phase 권위가 아니다.

Step101은 본문/구현 경계,102는 모델 권위 계층,103은 재료별 데이터·식별성,104는 공개/사용자 자료 가능성,
105는 launch inputs,106은 전체 검독 coverage,107은 착수 판정을 각각 따로 수행한다.
이 문건으로 후속 Step의 실제 완료를 선기록하지 않는다. 108–351 및 모든 재료 범위를 유지한다.
