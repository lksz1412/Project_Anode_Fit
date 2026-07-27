# Phase 057 사용자 방향 헌법

정본일: 2026-07-28  
기준선: v1.0.25.2 `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`  
상태: `AUDIT_CONSTITUTION_NOT_THEORY_CANON`

## 0. 이 문서의 권위와 한계

이 헌법은 v1.0.10–v1.0.25.2의 이론을 정본으로 채택하는 문서가 아니다.
새 이론식, 재료 상수, 코드 구조 또는 최종 목차를 확정하지 않는다.

이 문서가 확정하는 것은 다음 작업이 따라야 할 사용자 방향, 증거 규율,
금지 경계와 acceptance 구조다. Phase 058–069의 버전별 물리·코드 재감사와
문헌·데이터 조사가 끝나기 전에는 특정 model family를 최종 채택하지 않는다.

## 1. 기준선과 보존 경계

1. 과학 기준선은 v1.0.25.2의 commit `3b5fd05`다.
2. v1.0.26은 미완성·비권위 계열로 제외한다.
3. 원본, main, 기존 Claude/Fable/Codex 산출물을 수정하지 않는다.
4. 모든 새 작업은 `codex/lib-physics-endgame-v1025_2` branch에만 둔다.
5. 기존 후속 review fork는 Phase 068의 검토 입력이지 기준선에 자동 합류하지 않는다.
6. latest filename, handover의 “완결”, commit subject의 “PASS”는
   과학 권위의 충분조건이 아니다.

연결 결정: DEC-001–DEC-004.

## 2. 이론 문건의 성격

1. 최종 문건은 이공계 대학원 교재처럼 친절하고 상세해야 한다.
2. 동시에 review 논문처럼 핵심 원전, 경쟁 이론, 적용 범위와 한계를 깊게 다룬다.
3. 출발식→가정→연산→중간식→결과식→단위·부호·극한 검산의 다리를 생략하지 않는다.
4. 통계역학, 열역학, 상전이, 반응속도, 수송, 열과 관측량의 연결을
   독자가 문건만으로 추적할 수 있어야 한다.
5. 과거 버전, 작업 단계, 내부 오류 수정사, 방어적 자기평가를 본문 서사로 쓰지 않는다.
6. 코드 함수명, class, key, line number, gate, bit-exact, file map,
   implementation instruction은 theory manuscript에서 제외한다.
7. 필요한 구현 추적성은 별도 implementation/conformance companion에 둔다.
8. 이론 문건은 물리·화학의 권위이고, companion과 code는 그 하류 산출물이다.

연결 결정: DEC-005–DEC-009.  
해소된 충돌: 과거의 “문건–코드 유기성”은 내용 충실성으로 보존하고,
본문 code map 관행은 companion으로 이동한다.

## 3. 좌표와 관측량

최종 이론은 최소 다음 좌표를 구분하고 변환 관계를 명시해야 한다.

1. cell 외부의 누적 용량 좌표 \(q\)
2. 각 재료·상·host의 조성 또는 점유 좌표
3. 각 전극의 평형 전위와 내부 전기화학 퍼텐셜
4. 유한전류의 과전압과 동적 내부 변수
5. 관측 cell voltage
6. 충전·방전 및 휴지 protocol branch
7. ICA/DVA의 미분 방향, 부호와 정규화

전하 보존과 공통 cell voltage 제약을 먼저 세우고, 그 뒤 각 전극 응답과
관측 dQ/dV를 조립한다. wt%, mol fraction, active-material fraction,
capacity fraction을 서로 바꾸려면 capacity state와 변환식을 명시한다.

연결 결정: DEC-010, DEC-011.  
금지 계보: REJ-004.

## 4. 물리 계층

최종 model은 다음 계층을 하나의 latent-state 계보로 연결하되 섞지 않는다.

1. 보존법칙과 상태 변수
2. 재료별 자유에너지와 평형
3. 상공존, metastability와 nucleation/transition barrier
4. charge-transfer와 solid/electrolyte transport
5. strain, disorder, particle/host heterogeneity
6. hysteresis와 dissipative internal variables
7. 전극·cell observation map
8. sampling, voltage quantization, differentiation와 measurement uncertainty

한 개의 width, lag, background 또는 convolution이 여러 계층을 동시에
대신하지 않는다. 같은 symbol을 서로 다른 free-energy, barrier,
fit-kernel 역할에 재사용하지 않는다.

연결 결정: DEC-012–DEC-016.  
금지 계보: REJ-007–REJ-009, REJ-017.

## 5. 연구의 핵심 현상

새 이론과 code가 설명해야 하는 출발 관찰은 다음과 같다.

1. 온도가 낮아질수록 dQ/dV peak가 낮아지고 broadening되는 경향
2. 무전류·충분한 휴지 상태보다 정전류 상태에서 peak가 낮아지고 broadening되는 경향
3. 조건에 따른 peak 위치 이동, 비대칭, valley와 background 변화
4. 상전이 장벽과 전이율의 온도, 전극 전위·조성, 과전압 의존

전류 \(I\)를 근거 없이 독립적인 barrier knob로 삽입하지 않는다.
전류의 영향은 전하 보존, 과전압, 반응속도, 수송, 열과 protocol을 통해
내부 상태와 장벽에 전달돼야 한다. 직접 \(I\)-dependence가 필요하면
그것을 만드는 비평형 열역학 또는 stochastic driving의 유도를 제시한다.

연결 결정: DEC-013–DEC-015.

## 6. 재료별 책임

### Graphite

- staging과 phase coexistence를 curve basis/gallery 수와 구분한다.
- diffraction/thermodynamic evidence와 ICA feature assignment를 연결하되
  fit component만으로 phase를 정하지 않는다.
- regular-solution 또는 다른 free-energy candidate의 convexification,
  critical limit와 finite-width mechanism을 다시 유도한다.

### Doped high-voltage LCO

- 일반 LCO surrogate와 doped high-voltage cathode model을 구분한다.
- dopant species/concentration, defect chemistry, oxygen stability,
  phase degradation, cutoff와 high-voltage kinetic/transport limitation을
  문헌·데이터와 연결한다.
- graphite software 구조를 재사용했다는 이유로 같은 물리를 가정하지 않는다.

### Si, SiOx, Si-C

- large strain, chemo-mechanics, stress-coupled chemical potential,
  amorphization/crystallization, hysteresis와 host interaction을 별도 계보로 둔다.
- literature case 값은 dataset seed이지 보편 default가 아니다.

### Graphite+Si blend

- 각 constituent의 보존법칙과 공통 전압을 명시한다.
- wt%를 capacity fraction으로 바꾸는 capacity source와 상태를 기록한다.
- 단순 가중합, common-potential equilibrium과 실제 porous-electrode
  current sharing의 적용 범위를 구분한다.

연결 결정: DEC-012, DEC-017.  
필수 보류 계보: REJ-014, REJ-015.

## 7. 열역학과 경험적 형상의 경계

1. entropy와 reversible heat는 승인된 Gibbs/free-energy model의
   온도 미분에서 유도한다.
2. empirical skew, gallery basis, smoothing은 상태함수에 직접 들어가지 않는다.
3. skew-logistic의 면적 보존은 center, variance, susceptibility,
   entropy 보존을 뜻하지 않는다.
4. regular-solution free energy는 theory candidate로 검토할 수 있지만,
   패배한 curve fit의 Ω를 phase 판정으로 이전하지 않는다.
5. alpha, width, lag, gallery, background가 포화·축퇴하면
   material constant로 보고하지 않는다.

연결 결정: DEC-016, DEC-018–DEC-020.

## 8. 데이터와 검증

필수 데이터 범위:

1. graphite, Si, graphite+Si
2. doped high-voltage LCO
3. 복수 온도
4. 복수 전류·율속과 휴지/equilibrium 조건
5. independent cell/specimen
6. raw 또는 재현 가능한 preprocessing provenance

검증은 calibration fit과 분리해 다음 축을 갖는다.

- charge/capacity conservation
- 단위와 부호
- analytic/numerical limiting cases
- synthetic parameter recovery
- identifiability/profile/covariance
- peak, valley, area, background와 full-curve residual
- preprocessing uncertainty와 residual correlation
- held-out condition/cell/material transfer
- independent structural/thermodynamic evidence

R², naive BIC와 in-sample figure는 calibration signal이다.
phase mechanism이나 endgame acceptance의 단독 증거가 아니다.

연결 결정: DEC-017, DEC-018, DEC-022.  
금지 계보: REJ-019, REJ-020.

## 9. 수치 구현 원칙

1. invalid domain, NaN과 nonphysical input은 명시적으로 실패시킨다.
2. 물리값을 조용히 cap, clip, clamp 또는 softplus로 바꾸지 않는다.
3. fixed grid의 해상도에 따라 물리 branch가 바뀌지 않게 한다.
4. adaptive error control, event detection, conservative integration,
   domain-preserving parameterization을 우선한다.
5. 수치 regularization이 필요하면 목적, bias, convergence와 제거 극한을 기록한다.
6. legacy bit-exact regression과 새 physics acceptance를 다른 gate로 둔다.
7. default를 검증하는 시험은 시험 시작 전에 그 default를 다른 값으로 바꾸지 않는다.

연결 결정: DEC-021, DEC-022.  
금지 계보: REJ-001–REJ-003, REJ-012, REJ-013.

## 10. 이론–코드 100% 반영의 의미

100% 반영은 같은 수식을 문건과 코드에 복사했다는 뜻만이 아니다.

1. theory의 모든 계산 가능한 채택식은 stable claim/equation ID를 가진다.
2. implementation companion은 식, 가정, 단위, domain, limit,
   required data와 code consumer를 연결한다.
3. code의 모든 물리 branch는 채택된 claim에 역추적돼야 한다.
4. code에만 존재하는 physical knob, default 또는 branch를 금지한다.
5. theory에만 있고 code가 소비하지 않는 채택식은 `THEORY_ONLY`로
   숨기지 않고 acceptance에서 제외한다.
6. conformance test와 physical-validity test를 분리한다.
7. empirical component는 `EMPIRICAL_ONLY` label과 적용 범위를 가진다.

연결 결정: DEC-007, DEC-008, DEC-022.

## 11. 작업 기록과 변경 통제

각 phase는 다음 사슬을 지킨다.

```text
master plan
→ phase detailed plan
→ step execution record
→ machine evidence
→ phase result and gate
→ execution ledger
→ active handover
→ intentional commit
→ remote push verification
```

- 읽지 않은 source와 실행하지 않은 test를 PASS로 쓰지 않는다.
- 완료 선언에는 검증 범위와 미검증 범위를 같이 적는다.
- source freeze 뒤 변경되면 stale 결과를 폐기하고 final source에서 재실행한다.
- 삭제·재배치·수정은 원래 claim/asset, 이유와 대체 위치를 기록한다.
- commit subject는 주장이고 patch가 증거다.

## 12. 아직 사용자 결정을 요구하지 않는 미확정 영역

다음은 현재 감사가 끝나기 전에 확정하지 않는다.

1. 최종 graphite free-energy model family
2. LCO dopant별 state variables와 closure
3. Si chemo-mechanical model의 상세 차수
4. kinetic/nucleation stochastic vs deterministic formulation
5. porous-electrode transport의 포함 수준
6. observation/noise likelihood family
7. 최종 software package architecture
8. 최종 책의 장 번호와 분량
9. material parameter defaults

Phase 058–069의 증거가 선택지를 좁힌 뒤, 과학적 결과가 달라지는
실질 선택만 사용자에게 제시한다.

## 13. 헌법 변경 조건

이 헌법의 항목은 다음 중 하나가 있을 때만 변경한다.

1. 사용자의 직접 후속 지시
2. 1차 문헌·데이터·재유도가 물리적 오류를 입증
3. 서로 양립할 수 없는 requirement가 발견되어 사용자의 선택이 필요

변경 시 이전 문장을 삭제하지 않고 supersession 이유, 적용 범위와
새 evidence를 decision genealogy에 남긴다.
