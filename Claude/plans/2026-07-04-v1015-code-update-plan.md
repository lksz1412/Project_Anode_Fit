# v1.0.15 Plan — 코드 업데이트(점별 평가 경로·다온도 전자항 정밀형·고정점 검증) + 선택 Ch2 그림 보강

## Summary
v1.0.14 완주 후 코드-측 업데이트. **rev.2 핵심 재편(사용자 2026-07-04 지적)**: 작업 격자(균일 리샘플→점화식→재보간)는 물리가 아니라 구현 편의였고, 실측 피팅 워크플로에 변환·재변환 비용을 강제하며, ν 스위치·점프(23%)도 이산 점화식의 병리에서 파생된 것 — 연속(메모리 적분) 형식에서는 L_V→0 이 해석적으로 평형 종에 매끈 환원되어 스위치 자체가 불필요. 따라서 **①점별 평가 경로 `dqdv_points`(실측 V 직접 기입, 격자·재보간·ν 없음) 신설을 1급 과제로** 하고, ②LCO 전자항 다온도 정밀형(eq:U1T2 T² 곡률 — 옵트인) ③x-매핑 고정점 수치 확인 ④ν 는 legacy 격자 경로 전용 파라미터로 강등·기본 2.0 유지 확정(재베이스라인 불요 — 종전 Decision ① 자연 종결). 부속(선택): Ch2 그림 보강 4매. — **업데이트 필요 판정 유지**.

## Current Ground Truth
- 코드 `docs/v1.0.14/Anode_Fit_v1.0.14.py`: 회귀 13/13 bit-exact·검수 R1–R7 에서 코드 결함 0. 전자항 = `_effective_dS_rxn` 이 `T_ref=298.15` 동결 상수 오프셋(문건 §lco-code "동결 근사 — 다온도 T² 곡률은 round-trip 피팅 단계 과제" 명시). ν 기본 2.0(전이 기여 점프 ~23%).
- 문건: eq:U1T2(T² 곡률·½ 계수)·eq:lco-xmap(고정점)·되먹임 상한 14.3 mV 서술 실재. 가이드 Phase D 가 "T-스케일 복원·½ 적분 구현"을 명시.
- v1.0.14 는 사용자 검토 통과(fig15 간격 정정 완료·spinodal 부록 별도 유지 확정). 원본 보존: 코드 L74 "사용자 원형 보존(1바이트도 변조 X)" 구역 — v1.0.15 에서도 불가침.

## Phase Range
P1.1(증판)→P2.1(전자항 정밀형)→P2.2(고정점 검증)→P2.3(점별 평가 경로 ★1급)→P3.1(ν legacy 강등·문서 정합)→P4.1(검수 3회)→[P5.1 선택: Ch2 그림]→P6.1(마감). GO 후 무중단, Phase 별 커밋+푸쉬.

## Non-goals
- LCO Ω^cat·dH_a 실값 배정(실측 pair/rate 데이터 필요 — round-trip 단계 소관).
- 피팅 wrapper/Optuna 스키마 구현(사용자 워크플로 소관 — 가이드 지침으로 충분).
- 문건 대개정(v1.0.14 골격 유지 — §lco-code·가이드 Phase D 의 동결-근사 서술만 정밀형 반영 최소 동기).
- spinodal 부록 편입(별도 문건 유지 — 사용자 확정).

## Implementation Changes

### Phase 1.1 — 증판 준비 (Steps 1–2)
- **Step 1** `docs/v1.0.15/` 생성: v1.0.14 전 파일 복사·버전 문자열 계보 연장(1.0.13→1.0.14→1.0.15)·잔재 0 확인. v1.0.14 동결 선언.
- **Step 2** 기준선 게이트: 회귀 13/13·tex 3종 0-err·suite/sample/demo PASS.

### Phase 2.1 — 다온도 전자항 정밀형 (Steps 3–7, Fable 직접 — 물리 1급)
- **Step 3** 설계 확정: 옵트인 플래그 `exact_electronic_T`(생성자, 기본 **False** — 기본 경로 bit-exact 유지). True 시: (i) `func_dSe_molar` 에 실제 작업 온도 T 전달(Sommerfeld ∝T 복원) (ii) `_effective_dS_rxn`/`entropy_coefficient`/`dqdv` 의 U_1(T) 경로에 eq:U1T2 의 center−T_ref 별도 적분(½=a_e/2F 계수) 구현 (iii) 조성 동결(x_center) 해제 여부는 이번 판 범위 밖(동결 유지 — 문건 서술과 일치).
- **Step 4** 구현(신규 코드는 원형 보존 구역 밖·기존 시그니처 하위 호환 — 키워드 인자 추가만).
- **Step 5** 물리 검증: T∈{268,298,328} 에서 U_1(T) 곡률 = eq:U1T2 해석식과 수치 대조(허용 1e-10 상대)·플래그 OFF 시 전 출력 bit-exact(회귀+LCO demo 해시).
- **Step 6** 문건·가이드 최소 동기: ch1 §lco-code "동결 근사" 문단·가이드 Phase D 에 "정밀형 = exact_electronic_T 옵트인(기본 동결)" 1–2문(코드→문건 단방향 원칙 유지 — 문건은 물리·상태 서술만).
- **Step 7** gate: 회귀 bit-exact(OFF)·정밀형 해석 대조 PASS·tex 재빌드 0-err.

### Phase 2.2 — x-매핑 고정점 수치 검증 (Steps 8–9)
- **Step 8** 검증 스크립트 `verify_xmap_fixedpoint.py`: 정밀형 ON 에서 ξ_eq↔U_1 반복 갱신(0회/1회/수렴까지)의 U_1 변화 추적 — 1회 갱신 잔차가 되먹임 상한(문건 14.3 mV 스케일) 내인지, 수렴 반복수·수렴값과 1회-갱신 근사의 차이 정량화.
- **Step 9** gate: 스크립트 PASS + 결과 수치를 문건 §lco-code 각주(1문) 반영 — "1회 갱신 잔차 실측 X mV(수렴값 대비)".

### Phase 2.3 — ★점별 평가 경로 신설 (Steps 10–15, Fable 직접 — 1급)
- **Step 10** 설계 확정: 신규 메서드 `dqdv_points(V_data, direction|s, T, ...)` — 실측 극판 전압 배열(비균일 허용·소인 순서 정렬만 요구)을 그대로 받아 같은 좌표의 dQ/dV 반환. 평형 중심·분기·폭·평형 종 = 닫힌꼴 직접 평가. 꼬리 = 연속 메모리 적분 $\xi_\mathrm{lag}(V)=\tfrac1{L_V}\int_{-\infty}^{V}\xi_\eq(u)e^{-(V-u)/L_V}du$ 의 점별 수치 적분(구간 $[V-40L_V,V]$ Gauss–Legendre 고정 패널+분할, 목표 상대오차 ≤1e-8; 충전은 방향 반전 적분). **작업 격자·재보간·ν 부재** — $L_V\to0$ 매끈 환원(해석 성질) 을 구현이 그대로 승계.
- **Step 11** 구현: 원형 보존 구역 밖 신규 코드만·기존 `dqdv`/`curve` 시그니처 불변(legacy 경로 무변경 — 회귀 bit-exact 유지). `curve_points` 상위 편의(facade 동형)도 함께.
- **Step 12** 등가 검증: (i) 미세 균일 격자(Δ→0) legacy vs pointwise 상대오차 수렴 확인 (ii) $L_V$ 스윕(sub-grid 포함 1e-6~1e-1 V)에서 pointwise 가 점프 없이 평형 종↔꼬리 연속 천이함을 수치 실증(legacy ν-점프 23% 와 대비 그림) (iii) 비균일 실측형 V 샘플(불규칙 간격) 직접 기입 데모.
- **Step 13** 성능 확인: 전형 피팅 조건(1000점×4전이)에서 목적함수 1회 평가 시간 측정 — 피팅 루프 실용성 판정(목표 <50 ms).
- **Step 14** 문건·가이드 동기: ch1 §N1(작업 격자)·§N8 에 "점별 평가 경로(연속 적분형 — 격자·ν 불요)" 물리 서술 1문단+가이드 §2 "실측 피팅 표준 경로 = `dqdv_points`(직접 기입)" 재작성, 부록 B 대응표 행 추가. ν 각주는 "legacy 격자 경로 한정" 명시.
- **Step 15** gate: 회귀 13/13 bit-exact(legacy 불변)·등가 수렴·연속 천이 실증·tex 0-err.

### Phase 3.1 — ν legacy 강등·문서 정합 (Steps 16–17) 【rev.2: 재베이스라인 논쟁 종결】
- **Step 16** ν 기본 2.0 유지 확정(legacy 전용) — 가이드 §1 ν 행·ch1 각주를 "pointwise 경로에는 해당 없음·legacy 격자 경로 한정" 으로 정합. 골든 재캡처 없음.
- **Step 17** gate: 회귀 불변·문서 3자(코드 docstring·가이드·ch1) 일치.

### Phase 4.1 — 축소 검수 3회 (Steps 18–20)
- **Step 18** R1: 신규 코드 재유도 검수(Fable — 메모리 적분 이산화 오차·적분 구간 컷 타당성·eq:U1T2 ½ 계수·플래그 경로 분기 전수).
- **Step 19** R2: 코드-문건 정합 스윕(Sonnet — 부록 B 대응표·가이드 수치·docstring eq 참조 갱신분).
- **Step 20** R3: 자유 사냥 1회(Fable). 수렴 = 확정 결함 0 라운드 1회(변경 국소성 반영).

### Phase 5.1 — (선택) Ch2 그림 보강 (Steps 21–24) 【Decision ③ 종속】
- **Step 21** 대상 선정 브리프(Fable): 후보 4매 — ①vib/config/elec 세 엔트로피 성분의 x-분해 개형(eq:dSconfig·eq:Svib_mode·eq:Se 수치 평가) ②q_rev 부호 4-사분면(I≷0×ΔS≷0, eq:qrev) ③파생 A 겹침 가중(g_j(x) 봉우리 비중·완전식 vs 단순식) ④w 이중지위 도식(단상 예측 vs 두-상 현상학 — ch1 fig:widthbudget 와 상보). 전부 "좌표=식 수치 평가" 원칙.
- **Step 22–23** 제작: 경연 없이 **승자 작성자 재기용**(opus2 노선 2매·sonnet3 노선 2매 — v1.0.14 경연 결과 근거) + master 캡션 전수 검증.
- **Step 24** gate: ch2 재빌드 0-err·캡션-본문 정합·라벨 무교차.

### Phase 6.1 — 마감 (Steps 25–27)
- **Step 25** 최종 게이트(전 빌드·회귀·suite·sample·demo·xmap·pointwise 등가 스크립트).
- **Step 26** V1015_RESULT·ledger·INDEX(v1.0.15 승격)·CODE_MAP 갱신.
- **Step 27** HANDOVER_v1.0.15(Chain 연장)·최종 커밋+푸쉬.

## Implementation Interfaces
- **`dqdv_points(V_data, s|direction, T, ...) -> np.ndarray`** — 실측 V 직접 기입 점별 평가(비균일 허용·격자/재보간/ν 없음). `curve_points` facade 동형.
- `GraphiteAnodeDischargeDQDV.__init__(..., exact_electronic_T: bool = False)` — LCO 서브클래스 승계. OFF = 현행 bit-exact.
- `func_dSe_molar(..., T)` — T 명시 전달(기존 호출은 T_ref 기본값으로 하위 호환).
- `verify_xmap_fixedpoint.py`·`verify_pointwise_equiv.py` — 독립 실행, exit 0/1.

## Test Plan
- 흑연 회귀 13/13 bit-exact(플래그 OFF — 전 Phase 상시 게이트).
- 정밀형 해석 대조: U_1(T)−U_1(T_ref) = a_e/(2F)·(T²−T_ref²)+선형항, 3온도 수치 vs 닫힌식 상대오차 <1e-10.
- 플래그 ON/OFF 경로 분기 커버: LCO demo 양 경로 실행·유한성.
- (B안 시) 신규 골든 캡처 후 즉시 verify 13/13 재확인.

## Assumptions
- 사용자 실측 다온도 데이터는 아직 없음 — 정밀형은 해석 대조로 검증(실데이터 피팅은 round-trip 단계).
- eq:U1T2 의 a_e(전자항 계수) 정의는 v1.0.14 문건 확정본 기준.

## Decisions Required (GO 시 기본값으로 진행)
1. **점별 경로의 지위**: `dqdv_points` 를 실측 피팅의 표준 경로로 가이드에 명기(legacy 격자 경로는 회귀·suite 호환용 보존). **기본값 채택**. (ν 재베이스라인 결정은 rev.2 로 소멸 — legacy 전용·기본 2.0 유지 확정.)
2. **정밀형 활성화**: 옵트인 플래그(기본 OFF, bit-exact 보존). **기본값 채택**.
3. **Ch2 그림 보강(P5.1)**: 채택 여부. **기본값 채택**(4매·경연 없이 승자 노선 재기용).
4. **문건 동기 범위**: 코드 상태 서술 동기(§N1/§N8 점별 경로 1문단·§lco-code·가이드 Phase D·부록 B 대응표). **기본값 채택**.

## Correction History
- rev.1 (2026-07-04): 초안 — v1.0.14 완주 직후 사용자 지시("최종 코드 업데이트 필요 판단→계획서")에 따른 신규 작성. 필요 판정 근거 = 문건 내 코드-과제 약속 3건(eq:U1T2 동결 근사·고정점·ν)·Ch2 그림 2장 관찰.
- rev.2 (2026-07-04): ★구조 재편 — 사용자 지적("이산 격자 강제·변환/재변환 비효율·스위치 오프의 필요성 의문") 수용. 진단: 작업 격자는 lfilter 벡터화라는 구현 편의였고, ν 스위치·23% 점프·재보간은 전부 그 파생물. 연속 메모리 적분 형식에서는 L_V→0 이 평형 종으로 해석적 매끈 환원(스위치 원천 불요). 조치: P2.3 점별 평가 경로(`dqdv_points`) 를 1급 신설(Steps 10–15), 구 P3.1 ν 결정(A/B안)은 "legacy 전용·기본 2.0 유지" 로 종결·문서 정합만 잔존(Steps 16–17), 이후 Phase/Step 재번호(총 27). Decision ① 을 ν 재베이스라인→점별 경로 지위로 교체.
