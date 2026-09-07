# Phase069 Step103 — 재료별 데이터 요구와 식별성

## Summary / 현재 결정

CONTENT_VERIFIED_AWAITING_PUSH; PASS_P069_STEP103_MATERIAL_REQUIREMENTS. 이 문건은 기존 요구사항을 재료별 실행 조건으로 연결한다. 새 물리적 사실·자료 확보·모델 검증 완료가 아니다.
기준commit 7cc3d9522c084f198b4382b5bd9dacd35f894e19. 입력9개 identity는 Step103result에 동결했다.
Step102의 empirical/reduced/production 권위 구분을 유지하며 원본/기존 결과를 수정하지 않는다.

## 공통 데이터 축 — 여섯 재료군 모두 적용

각 축은 metadata를 확보하고 주장에 대한 필요성을 판정하라는 계약이다. 모든 모델에 모든 실험을 강제하지 않는다.
필요한 자료가 없으면 해당 claim의 제한을 명시한다. 다른 재료/claim의 독립 진행을 막는 전역 판정으로 바꾸지 않는다.

### 원자료·출처 (provenance)

저자/제공자, 원자료 위치·버전·license, 원 format/hash와 처리 recipe/hash를 분리한다. source-declared/reconstructed/saved-only/synthetic의 실제 의미를 확인하며 서로 자동 치환하지 않는다.
적용 주장: 모든 관측/모수/validation 주장. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 시료·전극 (specimen)

chemistry/조성·변형체·제조/형성 이력, cell/specimen 식별자, active/loading/binder/conductive fraction, 두께·공극률·입도/형태 등 주장에 필요한 정보를 기록한다. 미보고 항목은 UNKNOWN과 영향을 명시한다.
적용 주장: 물성·조성·열/수송·전극 전이. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 시간·전압·전류·초기상태 (protocol)

실제 time/V/I/Q/T의 chronology, 단위·부호·전압 reference와 half/full-cell 구분, lithiation/delithiation, 초기 조성·상태, cycle/formation/rest/reversal/pulse/cutoff 이력을 보존한다. 단순 단조전압 정렬로 이력을 덮지 않는다.
적용 주장: 평형/비평형·hysteresis·state transfer. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 용량과 질량 기준 (capacity_basis)

absolute/specific/areal 및 active material/전체전극/constituent 질량 분모, normalization 범위, 각 성분 가역·비가역 용량, finite-window 잔량·background를 구분한다. wt%를 capacity fraction으로 그대로 쓰지 않는다.
적용 주장: 용량 기여·혼합비·조성 좌표·peak area. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 온도 조건 (temperature)

측정 위치/실제 온도·시간 이력·안정화 조건·오차와 온도별 동일 조성/protocol 비교 가능성을 확인한다. ambient 설정값이나 생성 profile을 실측 온도 validation으로 바꾸지 않는다.
적용 주장: 온도 의존·entropy·kinetics·low-temperature 주장. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 율속과 전류 (rate)

실제 signed current/current density와 C-rate의 기준 용량, pulse/hold/rest 조건을 보존하고 비교 가능한 다율속 조건을 정의한다. 온도·상태·전극 차이를 rate 효과에 혼입하지 않도록 검사한다.
적용 주장: 수송/반응/경계 이동 및 유한전류 예측. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 휴지·평형 근거 (rest)

relaxation trace, hold duration/판정 기준, 잔류전류·drift와 이전 이력을 확인한다. GITT/pOCV/저율속/휴지 자료는 각각 protocol이 지지하는 근사만 부여하고 이름만으로 엄밀 평형으로 확정하지 않는다.
적용 주장: 평형 potential·상공존 vs kinetic hysteresis. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 독립 반복과 해상도 (replicate)

실제 independent cell/specimen/반복 수와 batch·cycle 구조, 측정 해상도/불확도를 보고한다. 같은 trace의 점 수·같은 cell의 cycle 수를 독립 시료 수로 바꾸지 않는다. 충분성은 아래 수량 계약에 따라 판정한다.
적용 주장: 실용적 식별성·재현성·uncertainty. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 구조·상/조성 증거 (structure)

staging/phase/dopant site/전환 반응을 주장하는 경우 해당 조성·온도·history에 대응하는 독립 구조/화학 분석과 원문 exact anchor를 요구한다. 모든 empirical fit에 특정 장비를 일괄 의무화하지 않는다.
적용 주장: phase/gallery/site/반응 종 assignment. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 역학·형상 증거 (mechanics)

stress/strain/팽창·소성/파괴/활물질 손실 또는 confinement 해석을 주장할 때 대응 관측·경계 조건과 출처를 요구한다. 자료가 없으면 그 기여를 fit만으로 확정하지 않는다.
적용 주장: Si계 및 관련 응력/미세구조 해석. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 열·엔트로피 증거 (thermal)

entropy/열 기여를 주장하는 경우 held-variable과 전압 reference가 명확한 온도 의존 평형 자료 또는 적합한 열 측정을 연결한다. 반응/ohmic/reversible heat와 전극 단독/full-cell 관측을 구분한다.
적용 주장: 열역학 모수·electronic/configurational/vibrational 항. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 독립 검증·전이 (held_out)

calibration에 쓰지 않은 실제 condition/cell/specimen 및 주장에 맞는 조성·온도·rate·재료 전이 범위를 지정한다. 분할 단위를 기록하고 처리/모델 선택이 held-out을 이용하지 않게 한다. 인접 trace 점 분할만으로 독립 시료 전이를 주장하지 않는다.
적용 주장: 예측·production-physics 범위. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 관측·전처리·오차 (observation)

raw Q(V)/V(Q)/time signal, ICA/DVA 전처리·미분·보간·smoothing 및 grid/resolution을 물리 상태와 분리한다. full curve/peak/valley/area/background residual와 상관·이분산/처리 불확도를 함께 평가한다.
적용 주장: 관측 형상·width/center/area와 물리상태 연결. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

### 식별성·불확도 (identifiability)

정해진 방정식/변수/조건에서 structural symmetry/Jacobian 및 practical profile/covariance/condition/posterior 검사를 계획한다. priors/고정값/bounds의 영향을 분리하며 수치 최적화 성공을 고유 물성 식별로 읽지 않는다.
적용 주장: 모수 조합·hidden state·기전 및 예측 불확도. 현재 상태: REQUIRED_NOT_YET_VERIFIED.

## 데이터 요구량과 식별성 판정

보편 최소 시료 수·온도 수·율속 수·휴지 시간을 근거 없이 지정하지 않는다. 실제 값과 누락을 기록하고,
고정된 식·domain·오차/분해능에서 식별하려는 모수 조합과 필요한 독립 관측을 기준으로 충분성을 판정한다.
다온도/다율속 자료 자체도 식별성의 자동 증명이 아니다. 관측 분해능보다 미세한 해석을 정당화하지 않는다.
수치 최적화 성공·많은 trace 점·강한 prior/bound는 독립 실험 정보와 다르다.
구조적 식별성은 식과 symmetry/Jacobian 등으로, 실용적 식별성은 실제 오차·profile/조건수/불확도로 별도 검사한다.
이 문건의 confounding 항목은 검사해야 할 위험이며 특정 모델의 비식별성을 새로 증명했다는 뜻이 아니다.
자료가 부족하면 합성 가능 모수 또는 예측량의 범위를 보고하고 추가 관측/조건을 제안할 후속 책임을 남긴다.

## 재료별 계약

### Graphite

원 요구사항 P069-REQ-012; owner PHASE-077-GRAPHITE-CLOSURE; downstream 71/72/77/81/86. 공통14축 전부 적용.
staging/gallery/phase sequence, transition 조성 interval·capacity, disorder/particle size, hysteresis와 저온 kinetics를 보존한다. Four-transition/seven-component는 관측 분해 수이며 독립 phase 수를 뜻하지 않는다.

원 요구사항 수용 조건:

- primary diffraction/thermodynamic 자료로 transition/조성 interval/용량 기여를 연결한다.
- free-energy 후보의 convexification/critical limit/finite-width, disorder/particle size, hysteresis와 저온 kinetics를 유도·대조한다.
- four-transition/seven-component 분해는 evidence tier를 부여하고 multi-T/rate/equilibrium 자료의 식별성을 따로 검증한다.

#### staging와 용량 기여

관측: Q/V 및 ICA/DVA, 조성·상 분율 관측.
검토 모수/상태: transition composition intervals; 각 transition 용량 기여; staging/gallery assignment.
필요 독립 근거: matched specimen/protocol의 구조·열역학 자료와 capacity basis, equilibrium/relaxation 근거를 결합한다.
구분해야 할 영향: 겹친 peak·basis 선택·background·window가 transition 수/area와 혼동되는지 검사한다.
근거 부족 시: curve reconstruction은 EMPIRICAL_ONLY로 남기고 phase/gallery assignment는 UNVERIFIED.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### 평형·열과 분포 폭

관측: 조성 고정 조건의 온도 의존 potential·entropy 관련 관측과 width.
검토 모수/상태: free-energy/interaction 후보; 반응 entropy/enthalpy; particle/disorder distribution.
필요 독립 근거: 원문 가정·held-variable, 여러 온도 및 구조/분포 자료로 ideal/regular-solution/공존과 관측 broadening을 구분한다.
구분해야 할 영향: empirical width를 interaction/entropy로 직접 대입하거나 heterogeneity와 평형 폭을 동일시하는 해석을 검사한다.
근거 부족 시: 유도·대안은 source 범위에서 보존하되 해당 specimen의 열역학 모수는 미식별/미검증으로 제한.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### 저온·유한전류 및 이력

관측: time/current/voltage, rest/pulse/reversal과 temperature별 변화.
검토 모수/상태: diffusion/charge-transfer/phase-boundary 기여; hysteresis/history state.
필요 독립 근거: 동일 basis와 통제된 specimen의 다온도·다율속·휴지 관측, 필요한 크기/구조 조건 및 독립 held-out 조건을 요구한다.
구분해야 할 영향: 온도/전류/입도/초기상태/분해능 영향의 보상을 검사하고 peak 소멸을 특정 기전의 단독 증거로 보지 않는다.
근거 부족 시: 유효 관측 범위의 경험적 예측만 보고; 고유 기전 및 조건 외 전이는 CONDITIONAL.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

현재 근거 판정: DATA_REQUIREMENTS_DEFINED_NOT_DATA_VALIDATED; 현재 접근성: NOT_ASSESSED_STEP104.

### Doped high-voltage LCO

원 요구사항 P069-REQ-013; owner PHASE-078-LCO-CLOSURE; downstream 71/72/78/81/86. 공통14축 전부 적용.
dopant species/site/concentration, defect chemistry, cutoff/history, high-voltage oxygen redox/loss·surface/structure degradation과 kinetics/transport를 구분한다. Undoped LCO와 analytic surrogate는 이 재료의 직접 검증이 아니다.

원 요구사항 수용 조건:

- dopant species/site/concentration, defect chemistry, oxygen stability/redox/loss, phase degradation, cutoff, high-voltage kinetics/transport 근거를 연결한다.
- order–disorder/metal–insulator/coexistence, entropy·electronic contribution은 원전의 적용 범위 밖으로 일반화하지 않는다.
- graphite의 소프트웨어 구조 재사용을 같은 물리의 근거로 삼지 않고 doped held-out 조건을 요구한다.

#### 도펀트·상/전자 상태

관측: 조성/전압과 dopant·구조/전자 상태 관측.
검토 모수/상태: dopant/site별 효과; order–disorder/metal–insulator/coexistence 범위; interaction 후보.
필요 독립 근거: 도펀트 종·site·농도가 확인된 시료의 조성·구조/전자 근거 및 원문 적용 범위를 연결하고 가능한 대응 비교군 차이를 기록한다.
구분해야 할 영향: dopant/stoichiometry/defect/전극 이력 효과를 하나의 scalar interaction 또는 empirical peak에 몰아넣는지 검사한다.
근거 부족 시: 일반 LCO 또는 proxy 결과는 별도 참고 범위; doped-specific 해석은 UNVERIFIED.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### 고전압 가역·비가역 변화

관측: cutoff/hold/cycle별 Q/V·가역/비가역 용량 및 산소·표면/구조 변화.
검토 모수/상태: oxygen redox/loss 구분; structural/surface degradation 기여; high-voltage kinetics/transport.
필요 독립 근거: 전압 reference와 upper cutoff/hold/온도·cycle chronology, matching chemistry/structure evidence 및 독립 doped condition 검증을 요구한다.
구분해야 할 영향: capacity loss/polarization/oxygen pathways 및 상변화를 whole-curve fit 하나로 분리했다고 주장하지 않는지 검사한다.
근거 부족 시: 관측된 변화만 범위화하고 산소/표면 기전 attribution 및 전이는 CONDITIONAL.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### 열·전자 엔트로피

관측: 조성 고정 온도 의존 전압과 열/전자 자료.
검토 모수/상태: reaction entropy; electronic/vibrational/configurational 기여; metallic-regime DOS 관련 후보.
필요 독립 근거: held-variable와 reference를 맞춘 열역학 관측 및 electronic source/domain 근거를 요구한다. Sommerfeld 후보의 metallic 가정은 자료로 확인할 항목이다.
구분해야 할 영향: 곡률 또는 empirical peak를 독립 entropy 성분/DOS로 해석하거나 graphite와 동일 부호를 무검증 적용하는지 검사한다.
근거 부족 시: 전체 반응 entropy와 성분별 해석 권위를 분리하고 full-cell 열로의 변환은 후속 부호·보존 유도 전 미확정.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

현재 근거 판정: DATA_REQUIREMENTS_DEFINED_NOT_DATA_VALIDATED; 현재 접근성: NOT_ASSESSED_STEP104.

### Si

원 요구사항 P069-REQ-014; owner PHASE-079-SILICON-CLOSURE; downstream 71/72/79/81/86. 공통14축 전부 적용.
crystalline/amorphous 초기 상태·lithiation sequence, 큰 변형·stress-coupled potential, amorphization/crystallization, host interaction과 hysteresis를 독립 재료 계보로 다룬다.

원 요구사항 수용 조건:

- crystalline/amorphous lithiation sequence와 조성 좌표를 원문에 연결한다.
- 응력·팽창·plasticity/fracture/loss of active material의 관측 영향과 rate/temperature/size 의존을 구분한다.
- 문헌 case 값은 dataset seed이지 보편 default가 아니며 empirical component를 상으로 고정하지 않는다.

#### 상태·조성·가역 용량

관측: 초기 구조, cycle별 Q/V 및 구조/조성 변화.
검토 모수/상태: phase/amorphous state assignment; composition coordinate; 가역 용량·비가역 손실.
필요 독립 근거: 초기/형성 이력, voltage window, active mass와 대응 구조·조성 근거를 확보한다.
구분해야 할 영향: formation/비가역 손실과 가역 transition 또는 empirical seven-component 수를 혼동하는지 검사한다.
근거 부족 시: component는 EMPIRICAL_ONLY; 독립 상/조성 배정 미확정.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### chemo-mechanics

관측: 전압 이력과 팽창/strain/stress·손상 관련 관측.
검토 모수/상태: stress-coupled chemical potential; 팽창/소성/파괴/active-material loss 기여.
필요 독립 근거: 입도/형상·기계 경계/confinement·cycle 조건과 해당 역학/용량 관측을 연결한다.
구분해야 할 영향: 평형/kinetic hysteresis와 stress/손상을 curve만으로 구분했다고 단정하는지 검사한다.
근거 부족 시: Larché–Cahn 등 후속 source/유도 요구 유지; 측정하지 않은 역학 모수·기전은 UNVERIFIED.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### rate/temperature/size 의존

관측: 다온도·다율속·rest/reversal과 size별 관측.
검토 모수/상태: reaction/transport 후보; state memory; 예측 불확도.
필요 독립 근거: 초기 상태와 basis를 맞춘 여러 조건 및 independent specimen/protocol held-out을 요구한다.
구분해야 할 영향: size/rate/T/기계 조건 동시 변경과 parameter compensation을 검사한다.
근거 부족 시: 문헌 case seed를 보편 default로 사용하지 않고 검증된 empirical 범위 외 전이를 제한.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

현재 근거 판정: DATA_REQUIREMENTS_DEFINED_NOT_DATA_VALIDATED; 현재 접근성: NOT_ASSESSED_STEP104.

### SiOx

원 요구사항 P069-REQ-015; owner PHASE-079-SILICON-CLOSURE; downstream 71/72/79/86. 공통14축 전부 적용.
oxide 조성 x와 초기 구조, conversion의 비가역 용량, active Si와 inactive matrix를 보존한다. Si와 공유하는 역학/이력 경로를 인정하되 SiOx를 Si로 합치지 않는다.

원 요구사항 수용 조건:

- oxide conversion의 화학·조성·비가역 용량과 이후 active phase의 가역 반응을 source/data에 연결한다.
- Si와 공유하는 chemo-mechanical/hysteretic 경로와 SiOx만의 차이를 구분한다.
- 공개 또는 사용자 specimen/protocol 근거가 없으면 해당 claim을 conditional로 남기고 재료 범위를 삭제하지 않는다.

#### conversion과 초기 손실

관측: 첫 cycle·후속 cycle의 Q/V, 가역·비가역 용량 및 조성/반응 생성물.
검토 모수/상태: oxide conversion contribution; active Si 생성/잔존; irreversible capacity accounting.
필요 독립 근거: oxide stoichiometry/초기 조성, formation/prelithiation 여부, charge balance·basis, 대응 화학/구조 근거를 요구한다.
구분해야 할 영향: oxide conversion·SEI/기타 side reaction·trapped lithium 손실의 분리가 자료로 가능한지 검사한다.
근거 부족 시: 원인별 손실 배정은 미확정; 관측 총 손실을 conversion 단독값으로 쓰지 않는다.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### 후속 가역 반응과 matrix

관측: formed state의 Q/V·가역 용량 및 active/inactive fraction 관측.
검토 모수/상태: active Si 용량; matrix의 역할; normalized capacity fractions.
필요 독립 근거: 현재 active/inactive 구성과 normalization/constituent 질량, cycle/voltage window를 명시한다.
구분해야 할 영향: Si 질량당·SiOx 질량당·전극 질량당 용량 및 첫 cycle/후속 cycle를 혼용하는지 검사한다.
근거 부족 시: 단독 Si parameter transfer는 CONDITIONAL이며 재료 범위를 삭제하지 않는다.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### matrix-coupled 역학·이력

관측: 형성 후 팽창/구조와 rate/T/rest·cycle 이력.
검토 모수/상태: stress/confinement; kinetic hysteresis; 상태·손상 영향.
필요 독립 근거: matrix 조성/구조와 필요한 역학·다조건·held-out specimen 자료를 연결한다.
구분해야 할 영향: matrix와 Si의 반응/역학 효과를 fit shape만으로 분리하는지 검사한다.
근거 부족 시: 해당 역학/transfer 해석을 UNVERIFIED로 두고 관측 curve의 제한된 경험적 가치는 보존.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

현재 근거 판정: DATA_REQUIREMENTS_DEFINED_NOT_DATA_VALIDATED; 현재 접근성: NOT_ASSESSED_STEP104.

### Si–C

원 요구사항 P069-REQ-016; owner PHASE-079-SILICON-CLOSURE; downstream 71/72/79/86. 공통14축 전부 적용.
active Si/active carbon, inactive carbon/binder/conductive matrix의 역할과 용량 basis를 구분한다. 구조·기계 효과와 Si 단독값 전이는 독립 근거를 요구한다.

원 요구사항 수용 조건:

- active/inactive matrix와 용량 basis를 명시하고 Si 단독 값의 전이를 검증한다.
- large strain/stress/phase sequence/host interaction의 필요한 근거와 held-out specimen을 지정한다.
- 문헌 seed나 fit component를 보편 물성 또는 phase identity로 승격하지 않는다.

#### active/inactive 용량 분해

관측: 복합체/constituent Q/V·질량 분율과 가역 용량.
검토 모수/상태: Si와 electrochemically active carbon 기여; inactive matrix 분모; capacity partition.
필요 독립 근거: Si/carbon chemistry·구조, fraction/loading·basis와 가능한 matched constituent 관측을 요구한다.
구분해야 할 영향: 모든 carbon을 inactive로 고정하거나 wt%를 capacity fraction으로 대체하는지 검사한다.
근거 부족 시: active contribution이 구별 안 되면 aggregate curve만 보고 component별 물성을 확정하지 않는다.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### 구조·기계 효과

관측: architecture/particle size와 팽창·strain·손상·cycle 변화.
검토 모수/상태: confinement/stress; host interaction; phase sequence 및 loss contribution.
필요 독립 근거: 구조·기계 경계, formation/사이클 이력과 해당 구조·역학 근거를 요구한다.
구분해야 할 영향: architecture·전도·kinetics·stress 효과의 보상과 단독 Si 가정 전이를 검사한다.
근거 부족 시: Si와 공유하는 이론은 조건부; composite 고유 모수는 source/data 없으면 UNVERIFIED.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### 전이·조건 의존

관측: 동일 복합체의 다rate/T/rest 및 독립 specimen 관측.
검토 모수/상태: reaction/transport 및 history 후보; 단독 Si→복합체 전이오차.
필요 독립 근거: basis·초기 상태·matrix를 명시한 calibration과 independent specimen/protocol held-out을 요구한다.
구분해야 할 영향: 서로 다른 carbon 구조/함량·batch의 fit 결과를 동일 재료로 풀링하는지 검사한다.
근거 부족 시: 문헌 seed/empirical component는 보편 물성·phase identity가 아니며 미검증 전이는 제한.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

현재 근거 판정: DATA_REQUIREMENTS_DEFINED_NOT_DATA_VALIDATED; 현재 접근성: NOT_ASSESSED_STEP104.

### Graphite+Si blend

원 요구사항 P069-REQ-017; owner PHASE-080-BLEND-CLOSURE; downstream 72/80/81/86. 공통14축 전부 적용.
constituent별 질량·가역 용량·lithiation fraction, 공통 전압과 charge conservation, finite-rate current sharing, hysteresis·initial state를 함께 보존한다.

원 요구사항 수용 조건:

- wt%→capacity fraction은 constituent별 capacity source와 lithiation state를 명시한 변환으로만 수행한다.
- 단순 가중합, common-potential equilibrium, porous-electrode current sharing의 성립/실패 조건을 구분한다.
- 단독 소재 calibration과 blend transfer/held-out composition·rate·temperature 검증을 분리한다.

#### 혼합비·용량 회계

관측: constituent 및 blend Q/V, 질량·basis·가역 용량.
검토 모수/상태: mass→capacity fraction; constituent lithiation state; total/finite-window capacity partition.
필요 독립 근거: matched constituent capacity source, active mass/fraction와 조성/상태·window를 명시한다.
구분해야 할 영향: mass fraction/capacity fraction/normalized derivative denominator와 background·잔량을 혼용하는지 검사한다.
근거 부족 시: 분모가 불명확하면 constituent 물성/분담 해석 보류; aggregate empirical fit과 별도로 표시.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### 공통전압·유한전류 분담

관측: blend의 I/V/time과 rest/reversal·rate/T, 가능한 constituent state/독립 제약.
검토 모수/상태: common-potential equilibrium; constituent internal potential/current sharing; history-dependent state.
필요 독립 근거: 전극 구조/constituent 조건 및 kinetics/transport에 대한 독립 제약과 상태 관측을 주장 범위에 맞춰 요구한다.
구분해야 할 영향: 단순 weighted sum이 finite-rate host/current-sharing 증거인지, 여러 hidden-state 분해가 같은 terminal curve를 설명하는지 검사한다.
근거 부족 시: in-sample whole curve는 유한율속 기전의 증거가 아니며 current partition은 미검증.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

#### constituent→blend transfer

관측: 단독 소재 calibration 후 독립 blend composition/rate/T 관측.
검토 모수/상태: constituent parameter transfer; blend interaction/coupling 후보; prediction uncertainty.
필요 독립 근거: constituent 보정과 blend 보정을 구분하고 held-out composition/rate/T와 specimen 범위를 기록한다.
구분해야 할 영향: 각 dataset에서 재보정한 값을 parameter transfer 성공으로 읽거나 Si/SiOx/Si–C 조성을 몰래 치환하는지 검사한다.
근거 부족 시: 대상 constituent chemistry 밖으로 일반화하지 않으며 공개/사용자 근거 미확보 claim은 CONDITIONAL.
구조적 식별성 NOT_ASSESSED_REQUIRES_FROZEN_EQUATIONS; 실용적 식별성 NOT_ASSESSED_REQUIRES_MATCHED_DATA.

현재 근거 판정: DATA_REQUIREMENTS_DEFINED_NOT_DATA_VALIDATED; 현재 접근성: NOT_ASSESSED_STEP104.

## 기록된 데이터의 현재 권위 상한

아래는 새 자료 조사 결과가 아니라 history/H44가 불변066–069 기록에서 확인한 범위다.
전체 원행·owner·수용 조건·origin·unknowns는 동반JSON history_data_evidence에 보존한다.

- C16: REAL_DATA_1_RECONSTRUCTED_6_SAVED_ONLY_5; IN_SAMPLE_ONLY. 재구성 자료를 자동 synthetic로,
  source-declared 자료를 specimen/protocol까지 확인된 측정값으로 분류하지 않는다.
- C19: SOURCE_DECLARED_DATASET; EXACT SPECIMEN_AND_PARQUET_BINDING_GNF.
  P066-OBL-0086와 Phase072 provenance 조건이 남는다.
- C20: IN_SAMPLE_WHOLE_CURVE_FIT_IS_NOT_FINITE_RATE_HOST_PROOF.
  P065-OBL-0054/P066-OBL-0120의 source-owned bounded 상태와 Phase080 조건을 유지한다.
- 066 profile16routes=9온도의존/7온도독립이나 multi-temperature experimental authority는0이다.
  held-out NOT_TESTED 여섯 행을 여섯 재료군에 일대일 대응시키지 않는다.
- 12-start 실행과 성공/수렴,36profile 생성 성공,과거25state 재현은 별개의 문제다.
  068의51실행49PASS/2hashFAIL는 외부 검증 또는 suitePASS가 아니다.
- Ah/C·시간 단위·C-rate 기준과 질량/용량 분모의 구분을 유지한다.
  과거 선택 입력의 내부 환산 예시는 실제 blend 조성 측정 또는 재료 default가 아니다.

C16/C17/C19/C20/C21의 NO_PHASE067_CLOSURE_ACTION_REQUIRED_WITHIN_RECORDED_AUTHORITY_CEILING은
과거067의 좁은 gate 결정이며 후속 근거 부채를 종료해도 된다는 뜻이 아니다.
현재 접근성과 재료별 정확한 dataset/specimen/protocol/replicate/uncertainty 수치는 이번 추출에서 UNKNOWN이다.
이를 자료가 세상에 존재하지 않는다는 결론으로 바꾸지 않는다.

## 원천·이력 연결 / 미완료 범위

동반JSON carry_evidence에 원천 분담 검독의 전체 논리값을 보존했다. 101개는
36 P065 + 37 P066 + 28 P068이며 98 OPEN_CARRY / 2 OPEN_CARRY_EXPLICITLY_BOUNDED_P067 /
1 PRESERVED_ACTIVE이다. 나머지215개도 유지하여 현재316/655 및 closure0은 변하지 않는다.
P065-OBL-0092의 bounded Sommerfeld 보존 상태는 재료 상수 승인이 아니다.
상속73개의 원의미는057의35개·066의38개 기록과 연결되며, 신규28개는068의68개 고유 처분 행을 가리킨다.

재료 태그는 요구와의 관련성이지 실제 자료·시료·기전 확보의 증거가 아니다. Graphite16/LCO7/Si5/blend17은
중복 태그를 포함하며 실제 material-tagged 고유42개 + cross_material59개 =101개다.
원천 key graphite_Si_blend는 그대로 보존하고 정본 key graphite+Si_blend와 명시적으로 연결한다.
LCO7개 중 doped high-voltage가 원문에 명시된 것은 P066-OBL-0075 하나다. 나머지6개는
일반LCO/proxy/관련 protocol 요구이므로 도핑 시료 근거로 승격하지 않는다.
SiOx·Si–C 및 구체적 역학 자료의 carry-specific 직접 연결은 GROUND_NOT_FOUND이다.
P069-REQ-015/016과 이번 역학 요구는 그대로 유지한다. 새 의무를 꾸며내거나 실제 자료 부재로 일반화하지 않는다.

source_original_meaning에는 과거의 긍정형 주장도 포함되지만 accepted fact가 아니며
WITHHOLD/GROUND_NOT_FOUND와 현재 수용 조건을 함께 읽는다. 원래 owner/phase/state/acceptance/relations를 유지한다.
PHASE068_DISPOSITION_TARGETS의 source_proposition/truth_status/authority_ceiling이 null인 경우는
좁게 추출한 구조화 필드에 값이 없다는 뜻이다. 원자료 자체나 근거가 없다는 뜻이 아니다.
68개 중 bounded_content는 JSON object 형식10개·plain text58개다. 전체 bounded_content/rationale/evidence와
prohibited_promotion은 정확한 native full-row pointer와 canonical SHA로 보존되며, 이 문건이 전부 전사했다고 주장하지 않는다.
숫자·식·원문 자체의 진위와 full source/PDF 검독은 이 연결 검증으로 대체하지 않는다.

현재 접근 가능·후보미확인·사용자자료필요·unavailable·synthetic-only 분류는 Step104에서 실제 접근 근거로 판정한다.
자료 부족이 모든 재료의 부재를 뜻하지 않으며 source-declared/reconstructed/saved-only도 자동 synthetic로 바꾸지 않는다.
현재316carry/655dispositions, C03/C06 원조건과 다른 미결 의무는 그대로 보존한다. 새 ID/re-owner/closure 없음.
Step106 NOT_YET_EXECUTED; Step107 NOT_SELECTED. 070+는107 positive/persisted 이전에 시작하지 않는다.
이 감사문건 자체는 학술 본문이 아니다. 학술 본문의 코드·이력 금지는 지정 구현 부록 또는 별도 companion 예외와 함께 유지한다.
