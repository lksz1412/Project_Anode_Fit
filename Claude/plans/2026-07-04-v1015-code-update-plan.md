# v1.0.15 Plan — 이산 전압 격자 완전 퇴출(점별 평가 단일 아키텍처) + 다온도 전자항 정밀형 + 선택 Ch2 그림 보강

## Summary
**rev.3 확정(사용자 2026-07-04 지시): 이산 전압 격자를 완전 퇴출한다.** rev.2 의 "legacy 격자 경로 보존" 안을 폐기 — 이력 참조는 v1.0.14 이하 버전 폴더가 담당하고, v1.0.15 는 격자 없는 단일 아키텍처로 만든다. 모든 평가가 점별(pointwise): 사용자가 실측 극판 전압 배열을 그대로 기입하면 같은 좌표에서 dQ/dV 가 나온다. 평형부(중심·분기·폭·평형 종)는 닫힌꼴 직접 평가, 인과 꼬리는 연속 메모리 적분 $\xi_\mathrm{lag}(V)=\tfrac1{L_V}\int_{-\infty}^{V}\xi_\eq(u)\,e^{-(V-u)/L_V}\,du$ 의 점별 수치 적분. 이로써 작업 격자·리샘플·역보간·ν 스위치(및 그 23% 점프)·sub-grid 병리가 **아키텍처에서 원천 제거**된다($L_V\to0$ 은 해석적으로 평형 종에 매끈 환원). 함께: LCO 전자항 다온도 정밀형(eq:U1T2 T² 곡률, 옵트인)·x-매핑 고정점 수치 확인·(선택) Ch2 그림 보강 4매. 흑연 회귀는 점별 아키텍처 기준으로 **재정초**(신규 골든 캡처 — 의도적 기준선 교체, ledger 기록).

## Current Ground Truth
- v1.0.14 완주·사용자 검토 통과(fig15 정정·spinodal 별도 유지 확정). v1.0.14 는 동결 — 격자 구현의 이력 참조처.
- 현행 코드의 격자 기구(퇴출 대상): `dqdv` 내부 작업 격자 생성(eq:vwork — `grid_pad_lo/hi`·`n_work_min`·`v_span_floor`)·`_causal_lowpass` 격자 점화식·`min_lag_grid_steps`(ν) 분기 스위치(eq:branch)·`np.interp` 역보간. 이 중 `_causal_lowpass`·`func_L_q` 등은 **L74 사용자 원형 보존 구역("1바이트도 변조 X") 내부** — 삭제·수정 불가.
- 문건의 격자 서술(동기 개정 대상): ch1 §N1 작업 격자 절(eq:vwork)·§N8 이산 점화식(eq:lowpass)·분기 스위치(eq:branch)·ν 각주·부록 A R5(이산 병리 회귀 가드)·부록 B(격자 파라미터 행들)·가이드 §1 ν 행·keybox 6단계.
- Fable 사용 한도 소진 임박 — **본 계획의 실행은 차기 세션 소관**(본 세션은 계획 rev.3 + 핸드오버로 종료).

## Phase Range
P1.1(증판·동결)→P2.1(격자 퇴출 재아키텍처 ★1급)→P2.2(전자항 정밀형)→P2.3(고정점 검증)→P3.1(문건 대동기)→P4.1(검수 3회)→[P5.1 선택: Ch2 그림]→P6.1(마감). GO 후 무중단, Phase 별 커밋+푸쉬.

## Non-goals
- 격자 경로의 어떤 형태의 잔존도 없음(선택 플래그·legacy 모드 불가 — 사용자 확정).
- LCO Ω^cat·dH_a 실값 배정(실측 데이터 필요 — round-trip 단계 소관).
- 피팅 wrapper/Optuna 스키마 구현(사용자 워크플로 소관).
- spinodal 부록 편입(별도 문건 유지 — 확정).
- 사용자 원형 보존 구역(L74)의 삭제·수정 — 미호출(orphan) 지위로 존치·문서화만.

## Implementation Changes

### Phase 1.1 — 증판 준비 (Steps 1–2)
- **Step 1** `docs/v1.0.15/` 생성: v1.0.14 전 파일 복사·버전 계보 연장(→1.0.15)·잔재 0. v1.0.14 동결 선언(이후 정정은 Addendum).
- **Step 2** 기준선 게이트(구판 기준 마지막 확인): 회귀 13/13·tex 3종 0-err·suite/sample/demo PASS.

### Phase 2.1 — ★격자 완전 퇴출 재아키텍처 (Steps 3–9, Fable 직접 — 1급)
- **Step 3** 설계 확정: `dqdv(V, s, T, ...)` 본체를 점별 평가로 재구현 — 입력 V 는 스칼라 또는 임의 배열(비균일 허용·소인 순서 정렬 요구), 출력은 같은 좌표의 dQ/dV. 분극(eq:vn)→전이 루프(닫힌꼴 평형부)→꼬리(메모리 적분: 구간 $[V_i-40L_V,\,V_i]$ 고정 Gauss–Legendre 패널 분할, 목표 상대오차 ≤1e-8; 충전은 방향 반전 적분 = eq:reversal 의 연속형)→합산. `curve` facade 시그니처 유지(환산만, eq:n0map). **스위치 없음** — 전 $L_V>0$ 에서 꼬리식 단일 경로($L_V\to0$ 수치 안정화는 적분형 자체가 보장, 필요 시 $L_V<\varepsilon_\mathrm{machine}$ 급만 해석 극한 dξ_eq/dV 로 대체하는 수치 가드 1줄 — 물리 스위치 아님).
- **Step 4** 파라미터 제거: `grid_pad_lo/hi`·`n_work_min`·`v_span_floor`·`min_lag_grid_steps` 를 생성자·전이 dict 에서 제거(잔존 입력 시 명시적 경고 후 무시 — silent 아님). `np.interp` 역보간 제거. 원형 보존 구역의 `_causal_lowpass` 는 미호출 orphan 으로 존치(구역 불가침 — `func_U_j_hys` 와 동일 지위, 부록 B 에 orphan 명기).
- **Step 5** `equilibrium()`·`entropy_coefficient()`·`reversible_heat()` 점별 정합 확인(이미 pointwise 성격 — 격자 의존 잔재 소거).
- **Step 6** 회귀 재정초: 신규 골든 캡처 — 좌표 = 구 골든과 동일한 V_n 입력(비교 가능성), 값 = 점별 아키텍처 출력. 재정초 사유·구판 대비 차이 정량(등가 검증: 미세 균일 격자 구판 결과 ↔ 점별 결과 수렴 대조, 꼬리 활성 케이스 포함)을 ledger 에 기록. 구 골든 파일은 v1.0.14 폴더에 그대로(이력).
- **Step 7** 등가·연속성 실증: (i) Δ→0 구판 수렴 대조 (ii) $L_V$ 스윕(1e-6~1e-1 V)에서 점프 없는 연속 천이(구판 ν-점프 23% 와 대비 수치) (iii) 비균일 실측형 V 직접 기입 데모 (iv) 성능: 1000점×4전이 목적함수 1회 <50 ms 목표.
- **Step 8** demo·sample·graph_suite 를 점별 API 로 이식·재실행(산출 png 갱신).
- **Step 9** gate: 신규 골든 self-verify·등가 수렴·연속 천이·suite/sample/demo PASS.

### Phase 2.2 — 다온도 전자항 정밀형 (Steps 10–13)
- **Step 10** `exact_electronic_T`(기본 False — 신규 골든 기준 불변) 옵트인: `func_dSe_molar` T 전달(Sommerfeld ∝T)·U_1(T) 의 eq:U1T2 ½ 적분 구현. 조성 동결(x_center)은 유지(문건 서술 정합).
- **Step 11** 해석 대조: 3온도 U_1(T) 곡률 vs eq:U1T2 닫힌식 상대오차 <1e-10, 플래그 OFF bit-exact.
- **Step 12** 문건·가이드 최소 동기(§lco-code·Phase D).
- **Step 13** gate: 회귀 불변(OFF)·해석 대조 PASS.

### Phase 2.3 — x-매핑 고정점 수치 검증 (Steps 14–15)
- **Step 14** `verify_xmap_fixedpoint.py`: 정밀형 ON 에서 ξ_eq↔U_1 반복 갱신 수렴성 — 1회-갱신 잔차 vs 되먹임 상한(14.3 mV 스케일) 정량.
- **Step 15** gate: PASS + 문건 §lco-code 각주 1문 반영.

### Phase 3.1 — 문건 대동기(격자 서술 개정) (Steps 16–19)
- **Step 16** ch1 개정: §N1 작업 격자 절 → 점별 평가 서술(eq:vwork 폐지 또는 "구판 이력" 각주화)·§N8 이산 점화식 → 연속 적분형 본문(eq:lowpass 를 적분형으로 재정의, 이산형은 구판 이력 각주)·eq:branch 스위치 제거(L_V→0 연속 환원 서술로 대체)·ν 각주 삭제·keybox 6단계 갱신.
- **Step 17** 부록 A/B 개정: R5 행(이산 병리 가드) → "구판(≤1.0.14) 격자 구현의 이력 항목" 재분류 또는 연속형 검산으로 대체·부록 B 격자 파라미터 행 제거·`dqdv` 점별 시그니처 반영·orphan 2건(_causal_lowpass·func_U_j_hys) 명기.
- **Step 18** FITTING_GUIDE 개정: ν 행 삭제·"실측 V 직접 기입" 표준 워크플로·S-사슬/진단표의 격자 언급 소거·문턱 수치(70–74 kJ/mol — ν·Δ 기반이었음) 재산출·재기재.
- **Step 19** gate: tex 3종 0-err·ref 0·of 0·격자 용어 잔존 grep 0(이력 각주 제외).

### Phase 4.1 — 축소 검수 3회 (Steps 20–22)
- **Step 20** R1(Fable): 신규 아키텍처 재유도 — 메모리 적분 이산화 오차·적분 컷(40L_V) 타당성·충전 방향 반전 적분 부호·수치 가드 경계.
- **Step 21** R2(Sonnet): 코드-문건 정합 스윕(부록 B·가이드 수치·docstring eq 참조 — 특히 재산출된 문턱 수치).
- **Step 22** R3(Fable): 자유 사냥. 수렴 = 확정 결함 0 라운드 1회.

### Phase 5.1 — (선택) Ch2 그림 보강 (Steps 23–26) 【Decision ③】
- **Step 23** 브리프: 4매 — ①config/vib/elec x-분해 개형 ②q_rev 4-사분면 ③파생 A 겹침 가중 ④w 이중지위 도식. 좌표 = 식 수치 평가.
- **Step 24–25** 제작(경연 없이 승자 노선 재기용: opus2 2매·sonnet3 2매)+master 캡션 전수 검증.
- **Step 26** gate: ch2 0-err·정합.

### Phase 6.1 — 마감 (Steps 27–29)
- **Step 27** 최종 게이트(전 빌드·신규 회귀·suite·sample·demo·xmap·등가 스크립트).
- **Step 28** V1015_RESULT·ledger·INDEX(v1.0.15 승격)·CODE_MAP 갱신.
- **Step 29** HANDOVER_v1.0.15(Chain 연장)·최종 커밋+푸쉬.

## Implementation Interfaces
- `dqdv(V: scalar|array, s, T, ...) -> 같은 좌표 dQ/dV` — 점별 단일 경로(비균일 허용). `curve` facade 시그니처 유지.
- 제거: `grid_pad_lo/hi`·`n_work_min`·`v_span_floor`·`min_lag_grid_steps`(잔존 입력 = 명시 경고).
- `exact_electronic_T: bool = False`(생성자·LCO 승계).
- `verify_pointwise_equiv.py`·`verify_xmap_fixedpoint.py` — 독립 실행 exit 0/1.
- 신규 골든: `golden_graphite_ref.npz` 재캡처(v1.0.15 폴더 — 구판 골든은 v1.0.14 폴더 이력).

## Test Plan
- 신규 골든 13/13 self-verify(점별 기준) — 전 Phase 상시 게이트.
- 구판 등가: 미세 균일 격자(Δ→0) 구판 출력 ↔ 점별 출력 수렴(꼬리 활성 케이스 포함, 상대오차 목표 <1e-6).
- $L_V$ 연속 천이: 스윕 전 구간 점프 0(구판 23% 대비 수치 실증).
- 정밀형 해석 대조 <1e-10·OFF bit-exact(신규 골든 기준).
- 성능: 1000점×4전이 <50 ms.

## Assumptions
- 실측 다온도·rate 데이터는 아직 없음 — 등가·해석 대조로 검증.
- 신규 골든 좌표 = 구판과 동일 V_n 입력(버전 간 비교 가능성 유지).
- 원형 보존 구역은 orphan 존치로 규약과 양립.

## Decisions Required (GO 시 기본값으로 진행)
1. ~~격자 퇴출 여부~~ — **사용자 확정(완전 퇴출)**. 결정 소멸.
2. **정밀형 활성화**: 옵트인 플래그(기본 OFF). **기본값 채택**.
3. **Ch2 그림 보강(P5.1)**: 채택 여부. **기본값 채택**(4매·승자 노선 재기용).
4. **신규 골든 좌표 규약**: 구판 동일 V_n 입력으로 캡처(비교 가능성). **기본값 채택**.
5. **eq:vwork·eq:lowpass(이산형)·eq:branch 의 처리**: 본문 삭제+구판 이력 각주 vs 부록 이동. **기본값 = 본문은 연속형으로 재서술, 이산 구현 이력은 각주 1개**(문건 간결성 우선 — 상세는 v1.0.14 참조 지시).

## Correction History
- rev.1 (2026-07-04): 초안 — 코드 과제 3건(eq:U1T2 동결·고정점·ν)+Ch2 그림 관찰.
- rev.2 (2026-07-04): 점별 경로 `dqdv_points` 1급 신설(legacy 격자 보존 병행안)·ν 재베이스라인 결정 소멸.
- rev.3 (2026-07-04): ★사용자 확정 지시 반영 — **이산 격자 완전 퇴출**(legacy 병행안 폐기, 이력은 v1.0.14 이하 폴더가 담당). `dqdv` 본체를 점별 단일 아키텍처로 재구현, 격자 파라미터 제거, 회귀 신규 골든 재정초(Step 6), 문건 대동기 Phase 3.1 신설(격자 서술 개정 — eq:vwork/eq:lowpass 이산형/eq:branch/ν/R5/부록 B/가이드), 원형 보존 구역은 orphan 존치. Steps 재번호(총 29). Decision ① 소멸·⑤(구판 식 처리) 신설. ※실행은 차기 세션(본 세션 Fable 한도 소진 — 계획+핸드오버로 종료).
