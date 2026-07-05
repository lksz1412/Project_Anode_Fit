# V1.0.15 P5 RESULT — 코드 점별 재아키텍처(격자 퇴출·dead 삭제·골든 검증 후 재정초)

> 마스터 = `../../plans/2026-07-05-v1015-code-doc-sync-master-plan.md`(rev.2) P5(Steps 20–27). 대상 = `docs/v1.0.15/Anode_Fit_v1.0.15.py`. 방법 = Serena(인덱스 미포함 → 직접 Read/Edit·단일 파일). 상태 = ✅ 완주(검증 후 재캡처).

## 1. 목표
Ch1 §1.9 가 확정한 점별 연속 메모리 적분을 코드에 반영: 균일 작업 격자(V_work)·리샘플·저역통과 점화식·np.interp 역보간·ν 분기 스위치를 **아키텍처에서 제거**하고 모든 dqdv 평가를 입력 전위 V_n 위에서 점별로. dead 삭제·격자 param 제거·골든 **검증 후** 재정초.

## 2. 변경 (Deliverable = Anode_Fit_v1.0.15.py)
- **`dqdv()` 점별 재작성**: V_work 격자·np.interp 역보간·`_causal_lowpass` 격자 저역통과·`ν·Δ_grid` 분기 스위치 전면 제거. 진행 방향 정렬(방전 오름·충전 내림, eq:reversal) → 전이별 ξ_eq → 인과 기억 적분 ξ_lag(점별) → `(ξ_eq−ξ_lag)/L_V`(eq:peakshape) → 배경 위 점별 합산·입력순서 복원. L_V→0 은 평형 종 ξ_eq(1−ξ_eq)/w(eq:tail-limit) 해석적 극한 = 분기 없음.
- **신설 `_causal_memory_pointwise(V_prog, ksi_eq, L_V)`**: 지수 커널 구간별 정확 적분(ξ_eq 선형 가정) `seg=ξ_i(1−e)−(Δξ/a)(1−(1+a)e)`, `ξ_lag[i]=e·ξ_lag[i−1]+seg`(a=h/L_V). 임의 간격 격자 성립(작업 격자 불요). `_causal_lowpass`(격자 전용) 대체.
- **dead 삭제**: `func_U_j_hys`(미호출 orphan)·`_causal_lowpass`(격자 아키텍처). 격자 param 5종 제거(`grid_pad_lo/hi`·`n_work_min`·`min_lag_grid_steps`·`v_span_floor`) — 생성자 시그니처·할당·docstring 참조 정리.
- **수치 가드(D6)**: 모듈 상수 `_LAG_RESOLVE_DECAY_CAP=40.0`. 커널이 한 격자점 안에서 소진되는 미해상(a=char_h/L_V>40) 또는 char_h≤0 에서만 평형 종 직접(0/0 회피). 이 상한에서 기억식(유한차분 Δξ/h)=평형 종이라 불연속 0. 물리 분기(제거된 eq:branch) 아님.

## 3. ★골든 검증 후 재캡처 (사용자 지침: 검사 없이 골든 처리 금지)
자립 검증 스크립트 6종 **전건 PASS** 후 재캡처:
- **A 평형 앵커 불변**: `equilibrium()`(격자 무관·미변경) 구 골든 **bit-exact**(maxdiff=0) — 안정 앵커.
- **B L_V→0 = 평형 종 연속(무스위치)**: 직접 L_V 스윕서 peak 이 평형 종으로 매끈히 단조 수렴(L_V=1e-9 rel<1e-3), tiny-L_V dqdv == `equilibrium()` 전 구간 maxdiff=0.
- **C 기억적분 해석검산**: 선형 ξ_eq → (ξ_eq−ξ_lag)/L=α(dξ/dV) rel 2e-9; 상수 ξ_eq → ξ_lag 상수. seg=지수커널 정확적분(brute-force 대조 max~1e-9).
- **D Δ→0 격자 세분 수렴**: 활성 꼬리 peak 이 격자 밀도↑에 수렴(연속 차 단조 감소).
- **E 면적 보존**: 전창 ∫eq=ΣQ_j ratio=1.000000; **활성 꼬리 dqdv 방·충 면적=1.000000=Q**(기억적분이 면적 보존). (유한창 [0.02,0.34] ratio 0.955는 절단 아티팩트 — equilibrium 도 동일이라 회귀 아님.)
- **F 방·충 mirror(γ=0)**: dqdv 방전=충전 maxdiff 4e-15(평형 종 방향 불변).
- **재캡처**: `test_regression_graphite.py capture`(13 arrays) → `verify` **PASS**. 구 골든 대비 dqdv 변화 = max_abs_diff 1.4e-5~3.9e-5(값 ~7-10, ~2e-6 상대) = 격자 interp 아티팩트 제거(점별이 더 정확), equilibrium_298 은 bit-exact 불변.

## 4. 검수 (적대 코드 리뷰 + master 재유도)
- **코어 CONFIRMED 정확**(리뷰어 재유도·수치실증): seg 정확적분(1e-9)·재귀 prefactor·초기조건(−∞ 자연경계)·a→0/a→∞ 극한·충전 방향 반전(eq:reversal, dis/chg 거울 2.4e-13)·inv_order 왕복·면적 보존·격자 제거 완전(live 0).
- **확정 결함 3건 → 전건 수정**: **F1[MED]** 가드 `L_V<2·char_h`(a>0.5)가 해상 가능 꼬리도 버려 격자 세분 시 ~19% 불연속 → `L_V·40<char_h`(a>40, 미해상만)로 수정(불연속 해소 실증: N=25→800 peak 8.77→8.79 매끈). **F3[LOW]** char_h=0(전 V 동일) 꼬리분기 누수 0 반환 → 평형 fallback 포함(실증 9.73). **F4[LOW]** seg 둘째항 소상쇄 → 사다리꼴 임계 1e-8→1e-4 상향.
- **F2**(선단 BC ξ_lag[0]=ξ_eq[0]): 정당한 하한 −∞ 자연경계(docstring 명시) — 창이 전이 개시를 포함하도록 권고, 코드 수정 불요.

## 5. Gate (검증 명령·증거)
- **격자 제거 완전**: live 코드에 V_work·grid_step·np.interp 역보간·_causal_lowpass·격자 param 잔재 0(grep). 잔재는 헤더 changelog history 문자열뿐(L5 v1.0.15 removal 명시).
- **회귀 PASS**: `test_regression_graphite.py verify` 13/13(재캡처 골든 대비) + 검증 게이트 6종.
- **다운스트림 무결**: sample_test·graph_suite·demo_lco_heat·plot_dqdv 전부 exit 0(plot_dqdv: LiC6 area=0.4994≈Q=0.5·bell·방충 대칭·no spike).
- **cold import OK**(self-test 통과).

## 6. 문건↔코드 정합(P4 worked example 대조 = P7 게이트)
Ch2 worked example(entropy_coefficient·reversible_heat 종합식)은 dqdv 격자와 무관(음함수 풀이→가중→Bernardi). 재작성은 dqdv 경로만 — 발열 함수 무변경. 문건↔코드 수치 대조는 P7.

## 7. Read Coverage
- Anode_Fit_v1.0.15.py 전문 정독(module funcs·생성자·dqdv·헬퍼·self-test). Ch1 §1.9 명세 대조(eq:memory/lag/peakshape/tail-limit/reversal). 검증 스크립트 6종 + 적대 리뷰(코어 재유도) + master 삼각.

## 8. 미결/이월
- **P6**: 그림 9종 경연 — Ch1(spine·relaxode·reversal 데이터 = 이제 점별 코드로 recompute 가능) + Ch2 tab:qrev Q_rev(x̄) 곡선.
- **P7**: 변경분 검수 + 문건↔코드 수치 대조 + HANDOVER·INDEX + 최종 게이트.

## 9. 상태·커밋
✅ **P5 완주**. 격자 퇴출·점별 재작성·dead 삭제·골든 검증 후 재정초·리뷰 3결함 수정. 회귀·게이트·다운스트림 전건 PASS. 커밋 = main·attribution 없음·명시 스테이징(py + golden + P5 결과 + 레저).
