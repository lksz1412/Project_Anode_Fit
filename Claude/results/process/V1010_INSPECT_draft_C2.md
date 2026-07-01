# V1010 INSPECT draft C2

- ID: C2
- Role lens: 코드 수치·차원·부호·면적보존 실측 검산
- 담당 비교 버전: `Claude/old/Ch1_v9/graphite_ica_ch1_v9.tex`
- 기준 지시: `inspect_base.txt` 전문 확인 후 수행. 계획서 `Claude/plans/2026-07-05-v1010-problem-inspection-plan.md` 참조.
- 수정 여부: 코드/문건 수정 없음. 본 파일만 신규 작성.

## 실제 확인 범위

- `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/inspect_base.txt`: 1-19행 전문 확인.
- `Claude/plans/2026-07-05-v1010-problem-inspection-plan.md`: 1-26행 전문 확인.
- `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py`: 1-851행 전문 확인. 핵심 위치: `_n_factor` 294-300행, `_width` 303-306행, `equilibrium` 372-389행, `dqdv` 392-502행, `entropy_coefficient` 544-578행, `reversible_heat` 580-588행, `GRAPHITE_STAGING_LIT` 680-709행.
- `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`: 1-1937행 전문 확인. 핵심 위치: 폭 이중지위 729-743행, broadening 1218-1384행, tail/reversal 1506-1644행, staging 표 설명 1663-1688행, self-check 1858-1909행.
- `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex`: 1-750행 전문 확인.
- `Claude/old/Ch1_v9/graphite_ica_ch1_v9.tex`: 1-1644행 전문 확인. v9의 `w_eff`/`use_w_eff` 계열 확인.
- 보조 확인: `plot_dqdv.py`, `graph_suite_p5.py`, `demo_lco_heat.py`, `test_regression_graphite.py`, `FITTING_GUIDE.md`, radius 관련 verdict 문건. Radius 연구는 회의적 참조로만 사용했고 확정 근거로 쓰지 않음.

## 실행 검산

- `python Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py`: overall OK True.
- `python Claude/docs/v1.0.10/test_regression_graphite.py verify`: bit-exact PASS. 단, 출력 면적 `trapz(eq)=0.908219`, `Qsum=0.970000`, `ratio=0.936308`.
- 직접 실행 스크립트로 FWHM, peak 위치, 면적, lag 길이, q_rev, LCO 면적 재계산.
- 그래프 직접 생성 및 육안 판독: `C:/Users/lksz1/AppData/Local/Temp/V1010_INSPECT_C2_graph_shape.png`.

## 문제 의견

### [HIGH] 기본 graphite staging dQ/dV가 네 전이로 분해되지 않고 단일 복합 봉우리로 병합됨

- 위치: `Anode_Fit_v1.0.10.py` 294-306행, 680-709행; `graphite_ica_ch1_v1.0.10.tex` 729-743행, 1663-1688행.
- 무엇이 틀렸나: `GRAPHITE_STAGING_LIT` 네 전이는 `w` 폴백 20/16/14/12 mV를 갖지만 동시에 `n=1.0`을 갖는다. `_n_factor()`가 `n`을 우선하므로 실제 폭은 네 전이 모두 `RT/F = 25.691 mV`가 된다. logistic derivative FWHM은 `3.52549*w`라서 네 전이 모두 FWHM 약 `90.57 mV`다.
- 왜 문제인가: 전이 중심은 0.21088, 0.13992, 0.12032, 0.08529 V이고, 특히 0.13992-0.12032 간격은 19.6 mV에 불과하다. 실측 결과 전체 평형 graphite 곡선은 local maximum이 하나뿐이며, peak는 0.10025 V, composite FWHM은 약 112-114 mV였다. 육안 그래프에서도 네 기준선은 보이지만 실제 곡선은 하나의 넓은 봉우리다.
- 실측 근거: 개별 전이 면적/Q는 약 0.99988로 면적식 자체는 보존되나, 전체 곡선은 네 staging transition의 식별성이 사라진다. `n`을 제거해 `w` 폴백을 쓰면 FWHM은 70.5/56.4/49.4/42.3 mV로 줄고 peak 높이도 달라진다.
- Refute: 문건은 해당 값이 신뢰값이 아니라 초기값이며 `n` 또는 `w`가 피팅 핸들이라고 밝힌다. 따라서 "피팅 전 placeholder"라면 코드 예외는 아니다. 그러나 v1.0.10의 기본 그래프·검증 산출이 graphite staging 물리 검증처럼 제시되는 한, 기본 곡선이 네 전이를 단일 bell로 병합하는 것은 release-level 물리 표시 결함이다.
- Lens: 그래프 물리, 수치/FWHM, 극단 일반화.

### [HIGH] 기본 동역학 꼬리 broadening은 graphite graph 조건에서 사실상 꺼져 있고, C-rate 변화는 거의 Rn 분극 이동만 보임

- 위치: `Anode_Fit_v1.0.10.py` 392-502행; `graph_suite_p5.py` 21행 및 30행; `graphite_ica_ch1_v1.0.10.tex` 1232-1352행, 1396-1593행.
- 무엇이 틀렸나: 문건과 그래프 suite는 finite-rate asymmetric tail을 핵심 broadening 출처로 설명하지만, 기본 `GRAPHITE_STAGING_LIT` 조건에서 `_resolve_lag_length()`가 내는 `L_V`는 작업격자 문턱보다 수백-수백만 배 작다.
- 왜 문제인가: 직접 검산에서 `V=0.03-0.34`, `n_work=2000`일 때 grid step은 `1.9687e-4 V`, tail 분기 문턱은 `3.9375e-4 V`였다. 그러나 I=1.0에서도 전이별 discharge `L_V`는 `4.91e-7`, `1.47e-7`, `4.37e-8`, `4.75e-9 V`로 문턱의 최대 0.0025배뿐이다. 따라서 `dqdv()`는 tail 분기가 아니라 평형 peak 분기로 떨어진다.
- 실측 근거: `Rn=0`에서는 I=0, 0.02, 0.2, 1.0의 graphite 곡선 면적과 peak가 모두 동일했다. `Rn=0.01`에서는 I=1.0에서 discharge peak 0.11037 V, charge peak 0.09020 V로 갈라졌는데, 이는 평형 peak 0.10013 V에서 거의 `±I*Rn = ±0.01 V`만큼 이동한 값이다.
- Refute: `L_V`를 직접 지정하거나 fitting으로 동역학 파라미터를 바꾸면 tail은 켜질 수 있다. 그러나 release 기본 graph suite와 self-test가 "C-rate dependence"를 보여준다고 읽히는 현재 상태에서는, 그 변화가 finite-rate tail 검증이 아니라 주로 ohmic shift 검증이다.
- Lens: 코드 직접 실행, 차원/스케일, 그래프 물리.

### [MEDIUM] 면적보존 회귀가 PASS를 내면서도 검사 구간 면적 손실을 실패로 처리하지 않음

- 위치: `test_regression_graphite.py` 43-75행; `graph_suite_p5.py` 89-104행.
- 무엇이 틀렸나: `area_check()` docstring은 "면적=Q assert"라고 되어 있지만 실제로는 값을 반환하고 출력만 한다. `verify` 모드의 PASS/FAIL은 golden array bit-exact 여부에만 걸려 있고 면적 ratio는 gate가 아니다.
- 왜 문제인가: 실제 실행 결과 `test_regression_graphite.py verify`는 `AREA check(post): trapz(eq)=0.908219 Qsum=0.970000 ratio=0.936308`를 출력한 뒤 `GRAPHITE 0-DIFF: PASS`를 냈다. 회귀가 "현재 출력이 과거와 같은지"만 보장하고, 면적보존 물리 조건은 실패시켜도 막지 못한다.
- 추가 실측: graph suite의 V9 방식인 `V=0.0-0.4`에서도 `area=0.949645`, `Qsum=0.970000`, `ratio=0.979016`이었다. 반면 각 전이를 중심 ±0.25 V로 넓게 잡으면 area/Q는 약 0.99988 이상이었다.
- Refute: 유한 표시 창에서 logistic tail 일부가 잘리는 것은 수치적 버그가 아닐 수 있다. 문제는 "면적=Q assert"라는 회귀 명칭과 PASS 문구가 실제 gate와 맞지 않아, 면적 결함을 탐지하지 못하는 false pass 구조라는 점이다.
- Lens: 면적보존 회귀, 빈통과 방지.

### [LOW] 충전 tail 방향 설명에 본문-캡션 부호 충돌이 있음

- 위치: `graphite_ica_ch1_v1.0.10.tex` 1607-1610행, 1639-1641행; 코드 `dqdv()` 492-497행.
- 무엇이 틀렸나: 본문 1609-1610행은 충전 꼬리가 "`V`가 큰 쪽"으로 늘어진다고 쓰지만, 그림 캡션 1640-1641행은 충전은 `V`가 낮은 쪽으로 꼬리가 간다고 쓴다. 코드의 충전 분기는 `ksi_arr[::-1]`로 뒤집어 필터 후 복원한다.
- 왜 문제인가: self-test 출력은 직접 L_V 조건에서 discharge peak 0.134 V, charge peak 0.106 V로 충전 쪽이 낮은 V 방향으로 이동함을 보여준다. 즉 캡션/코드/self-test는 낮은 V 방향과 맞고, 본문 한 문장이 반대다.
- Refute: "진행 방향 뒤쪽"이라는 표현을 시간축 기준으로 해석하면 작성 의도는 맞을 수 있다. 하지만 바로 뒤의 전압 방향 문구가 캡션과 반대라, 부호 검산자가 읽으면 혼동 지점이다.
- Lens: 부호/방향 서술.

## Cross-version 판단: v9(old/Ch1_v9) 대비

- v9에는 `w_eff = (RT/F)(1 - Omega/(2RT))`, `func_w_eff`, `use_w_eff`, `w_eff_floor_frac` 계열이 남아 있었다. 확인 위치: `Claude/old/Ch1_v9/graphite_ica_ch1_v9.tex` 682-699행, 1497행 전후.
- v1.0.10은 `w_eff` 경로를 제거했고, 코드 주석도 `ξ_eq` 폭과 분모 불일치로 면적보존이 깨지는 버그였다고 적는다. 이 제거 자체는 회귀가 아니라 정당한 절단으로 판단한다.
- 단, v9의 결함을 제거한 뒤 현재 기본값은 `n=1` 우선으로 모두 `RT/F` 폭이 되어 graphite 전이 네 개를 병합한다. 따라서 "v9의 `w_eff`를 되살려야 한다"가 아니라, v1.0.10 기본 graph/fitting 초기값이 staging 식별성 및 tail 검증을 충분히 대표하지 못한다는 쪽이 더 약한 고리다.
- v1.0.10은 v9에 없던 broadening 설명을 추가했으므로 broadening 절 자체가 누락된 것은 아니다. 문제는 현재 기본 코드 실행에서 그 broadening tail이 사실상 활성화되지 않는다는 점이다.

## 가장 약한 1곳

가장 약한 곳은 `GRAPHITE_STAGING_LIT`의 `n=1` 우선권과 기본 graph suite의 해석이다. 코드 주석과 Ch1은 `w` 폴백이 inert임을 정직하게 밝히지만, 실제 release graph를 실행하면 네 staging transition이 아니라 하나의 넓은 bell만 보인다. 게다가 finite-rate tail은 기본 조건에서 sub-grid라 꺼져 있어, C-rate 그래프는 tail broadening 검증이 아니라 거의 Rn shift 검증이다. 즉 수식 개별 항은 대체로 맞아도, 기본 실행물이 "graphite ICA 물리"를 보여준다는 주장에는 가장 큰 실측 공백이 있다.

## 확정 / 근거 미발견 / 미검증

- 확정: `n=1` 우선으로 실제 폭이 네 전이 모두 `25.691 mV`가 되는 것.
- 확정: 전체 graphite 평형 곡선이 기본값에서 local maximum 1개만 갖는 것.
- 확정: 기본 graphite 동역학 `L_V`가 graph suite 격자 문턱보다 훨씬 작아 tail 분기가 켜지지 않는 것.
- 확정: 회귀 `verify`는 면적 ratio 0.936308을 출력하면서도 PASS 처리하는 것.
- 근거 미발견: radius/particle-size 분포가 현 v1.0.10 결함의 확정 원인이라는 근거. 관련 문건은 회의적 참조로만 남김.
- 미검증: 실제 실험 데이터에 fitting한 뒤 `n`, `L_V`, `Omega`가 어떤 값으로 수렴하는지. 본 검수는 release 기본값과 문서/코드 정합만 확인했다.

## 5-line summary

1. v1.0.10 기본 graphite 곡선은 네 staging peak가 아니라 단일 복합 peak로 보인다.
2. 원인은 `n=1` 우선으로 `w` 폴백이 inert가 되고 모든 전이 FWHM이 약 90.57 mV가 되는 구조다.
3. finite-rate tail broadening은 기본 graphite 조건에서 `L_V`가 sub-grid라 사실상 꺼져 있다.
4. 면적보존 회귀는 ratio 0.936308을 출력하면서도 PASS하므로 물리 gate가 아니다.
5. v9의 `w_eff` 제거는 정당하지만, 그 이후 기본 실행물이 staging 식별성·tail 검증을 대표하지 못하는 문제가 남았다.
