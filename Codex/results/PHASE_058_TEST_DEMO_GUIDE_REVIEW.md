# Phase 058 test·demo·guide·handover 원문 감사

정본일: 2026-07-28  
기준 commit: `3b5fd059ed09cdcdde38668c399cb35b8afbcca9`  
범위: v1.0.10–v1.0.13의 unique test 5개, demo 6개,
implementation guide 3개, result/handover 4개

## 판정 경계

이 문건의 `COMPLETE`는 원문을 1행부터 EOF까지 읽었다는 뜻이다.
그림 생성, 유한값 출력, golden array의 bit-exact 일치와 같은
내부 실행 결과를 물리 타당성 또는 실험 예측 성공으로 승격하지 않는다.
실행 재현은 Step 27.3, 독립 물리 probe는 Step 27.4에서 별도로 판정한다.

## 테스트 5개

### sample test 3개

`sample_test_v1010.py`, `sample_test_v1012.py`,
`sample_test_v1013.py`는 물리 test라기보다 2×2 그림과 콘솔 보고서다.
v1.0.10은 87행, v1.0.12는 105행, v1.0.13은 106행에서
물리 assertion이 없다고 스스로 명시한다. 세 파일은 graphite transition의
`n`을 0.12로 바꿔 네 봉우리를 분리한다. 이는 fitting kernel의 자유도가
네 봉우리를 만들 수 있음을 보이지만, 그 폭이 2상 열역학이나 관측 장치의
분해능에서 유도됐음을 입증하지 않는다.

LCO C-rate panel은 default LCO transition dict에 `Omega`, `dH_a`,
`L_V`가 없기 때문에 속도 의존 동역학·히스테리시스 검증이 아니다.
통상 사용된 `Rn=0.01`의 lumped shift를 그리는 데 가깝고,
사용자 핵심 현상인 저온·유한전류 peak height 저하와 broadening을
검증하지 않는다.

### graphite regression 2개

두 regression script의 실제 gate는 13개 array의
`np.array_equal`이다
(v1.0.10 59–76행, v1.0.13 64–81행). 따라서 검증되는 것은
golden 생성 상태의 bitwise 불변성이다. 그 상태가 실험이나 독립 물리
기준에 맞는지는 검증되지 않는다.

두 파일의 `area_check` docstring은 “assert”라고 쓰지만
실제 함수는 area와 `Qsum`을 반환하고 최종적으로 값만 출력한다
(v1.0.10 43–50, 74–76행; v1.0.13 46–53, 79–81행).
허용오차 assertion이나 실패 exit가 없으므로 면적 보존 gate로 세지 않는다.

## demo 6개

`demo_lco_heat.py` 두 개와 `plot_dqdv.py` 두 개는 그림과 진단값을
생성한다. `graph_suite_p5.py`와 `graph_suite_v1013.py`도
V9 면적비를 출력하지만 실패 조건을 강제하지 않는다
(v1.0.10 87–104행, v1.0.13 120–137행).
V7은 두 버전 모두 LCO의 \(T^2\) 곡률이 미구현이라고 명시한다
(v1.0.10 79–85행, v1.0.13 111–118행).

동일 구현이 만든 \(U(T)\)를 동일 구현의 유한차분으로 되찾는
round-trip과 동일 kernel의 수치적분은 내부 수치 정합 검사에는 유용하다.
그러나 독립 calorimetry/entropy 자료나 holdout 데이터를 대조하지 않으므로
전자 엔트로피와 열 생성 모델의 외적 타당성을 보장하지 않는다.

## fitting guide 3개

v1.0.10 guide는 `nRT/F` 폭과 여러 tier를 “확정”으로 표시하고
그림·회귀를 PASS로 부른다. 현재 감사에서는 이 표현을 승계하지 않는다.
특히 fitted `n`은 empirical observation parameter일 수 있으나
일반적인 2상 평형 폭의 열역학 정본은 아니다.

v1.0.12–v1.0.13 guide의 S0–S5/GITT/AIC/holdout 구상은 보존할 가치가
있는 식별 전략이다(각 43–79행). 그러나 해당 version의 production code에는
데이터 ingest, fitting objective, uncertainty, AIC comparison,
holdout evaluation pipeline이 없다. 따라서 이는 구현된 능력이 아니라
향후 계획이다.

두 guide는 LCO에 `Omega`와 `dH_a`가 배정되지 않아 default
히스테리시스·kinetic tail이 비활성임을 정직하게 인정한다
(v1.0.12 8–10, 25–32행; v1.0.13 25–32행).
이 한계 표시는 보존하되, `x_MIT=0.85`라는 명칭만으로
“physical anchor”를 확정하지 않는다. composition mapping,
DOS normalization과 공개 측정치 대조가 필요하다.

## result·handover 4개

`V1010_PROBLEM_REPORT.md`의 최초 R1, 즉 분리 peak를 만들 수 없다는
진단은 `n≈0.1` 실행 결과로 철회됐다. 그 철회는 수치 kernel의 표현력을
복원하지만 fitted sub-thermal width의 물리 유도를 자동으로 복원하지 않는다.
따라서 “near-delta를 강제해야 한다”는 처방은 폐기하되,
equilibrium two-phase contribution과 measurement/heterogeneity
broadening을 개념적으로 분리해야 한다는 요구는 남는다.

동 problem report 20–22행의 kinetic tail default-off 진단은
production-code 검독과 일치한다. 반면 과거 handover가 이 문제를
`z_cut` 오적발과 묶어 닫은 것은 현 감사에서 물리 해결로 인정하지 않는다.
분자 Eyring prefactor의 전극 progress coarse-graining과
grid-dependent handoff도 독립 검증이 필요하다.

`HANDOVER_v1.0.13.md`는 “미완료 없음(계획 범위 내)”이라고 한 뒤
같은 문장에서 \(T^2\), LCO interaction/barrier, lag rebaseline,
composition fixed-point를 이월한다(17–18행). 이 네 항목은 사용자가
요구한 온도·전류·전위 의존 barrier와 고전압 LCO 설명의 핵심이므로
완료 주장으로 받아들일 수 없다.

## 현 단계 carry-forward

- 보존: transition-wise capacity accounting, electrode-aware direction
  correction in v1.0.13, 단계적 식별과 holdout 원칙, LCO kinetic
  defaults가 비어 있다는 정직한 scope 표시.
- empirical-only: fitted `n`/`w`, lumped `Rn`, frozen transition kernel,
  golden-output regression.
- 교정: C-rate–capacity unit contract, equilibrium/kinetic/observation
  broadening 분리, grid switch, barrier coarse-graining, LCO entropy
  composition/temperature closure.
- 누락: public experimental validation, Si와 graphite–Si blend,
  doped high-voltage LCO, uncertainty/identifiability, low-temperature
  transport and instrument convolution.

## 현 단계 결론

v1.0.10–v1.0.13은 다봉 empirical fit의 출발점과 여러 좋은 경고를
제공하지만, 사용자의 최종 연구 목표를 충족한 물리 정본이나 검증된
production fitter가 아니다. 특히 과거의 `PASS`는 대체로 source
보존·그림 생성·내부 일관성을 뜻했으며 external validity를 뜻하지 않는다.
이 판정은 이후 version에서 어떤 문제가 실제로 해결됐는지를 판별하는
baseline으로만 사용한다.
