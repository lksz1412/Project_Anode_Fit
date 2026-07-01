# V1010_INSPECT_draft_C1

- 검수자: C1
- 역할/렌즈: LCO/전자엔트로피 물리, MSMR 동형, MIT 게이트
- 담당 구버전: `Claude/old/_archive/graphite_ica_ch1_Opus_v5.tex`
- 기준 지시: `inspect_base.txt` 전문 정독 후 적용
- 작업 성격: 검수 의견만. 코드/문건 수정 없음.

## 실제 확인 범위

- `C:/Users/lksz1/AppData/Local/Temp/claude/d--Projects/f45f576c-1efc-4f50-8591-1f84bb7d7f39/scratchpad/inspect_base.txt`: 전문 검독 완료.
- `Claude/plans/2026-07-05-v1010-problem-inspection-plan.md`: 전문 검독 완료.
- `Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py`: 1-850행 전문 검독 완료.
- `Claude/docs/v1.0.10/graphite_ica_ch1_v1.0.10.tex`: 1-1937행 전문 검독 완료.
- `Claude/docs/v1.0.10/graphite_ica_ch2_v1.0.10.tex`: 1-750행 전문 검독 완료.
- `Claude/docs/v1.0.10/FITTING_GUIDE.md`: 1-46행 전문 검독 완료.
- `Claude/old/_archive/graphite_ica_ch1_Opus_v5.tex`: 1-1883행 전문 검독 완료.
- 그래프 스크립트 `plot_dqdv.py`, `demo_lco_heat.py`, `graph_suite_p5.py`, `test_regression_graphite.py`: 전문 검독 완료.
- 저장 그래프 `anode_fit_v1_0_10_dqdv.png`, `P4_lco_heat_validation.png`, `P5_graph_suite.png`: 육안 판독 완료.
- radius 연구: `RADIUS_VERDICT.md`, `BAND_VERDICT.md`, `ORIGIN_VERDICT.md`, `CODE_w_check.md`만 회의적 참조. 확정 근거로 쓰지 않음.

## 그래프 직접 실행 및 판독 근거

직접 실행:

- `python Claude/docs/v1.0.10/Anode_Fit_v1.0.10.py`
- 별도 측정 스크립트로 `Anode_Fit_v1.0.10.py`를 import하여 v1.0.10 기본 파라미터의 dQ/dV, 개별 peak FWHM, area, local maxima를 계산하고 임시 PNG를 생성해 육안 판독.

주요 재현 수치:

- graphite full equilibrium: local peak 1개, `V=0.10025 V`, height `7.3001`, global FWHM `113.814 mV`, area `0.9480` against `Qsum=0.97` on `0-0.32 V`.
- graphite 개별 transition, 실제 코드 기본값 `n=1.0`: 모든 transition의 평가 폭 `w_eval=RT/F=25.691 mV`, logistic derivative FWHM `90.531 mV`.
- graphite transition 중심: `0.21088`, `0.13992`, `0.12032`, `0.08529 V`. 중심 간격은 약 `70.96`, `19.60`, `35.03 mV`라 FWHM보다 작거나 같은 규모.
- `n` 제거 후 `w` fallback 사용: local peak 2개 정도만 육안 분리. 네 staging peak 복구 아님.
- LCO equilibrium: local peak 2개, 약 `3.919 V`와 `4.037 V`. `4.17-4.20 V` T3 peak는 기본 dataset/그래프에 없음.
- LCO electronic entropy effective value: second transition에서 `x_center=0.50`, `x_MIT=0.50`, `dS_eff=-49.678 J mol^-1 K^-1`. `func_dSe_molar(0.50, 298.15, 13, 0.50, 0.05)=-45.678 J mol^-1 K^-1`.

## 문제 의견

### [HIGH] graphite 기본 dQ/dV가 4 staging transition을 한 개의 넓은 bell로 병합한다

- 위치: `Anode_Fit_v1.0.10.py` 293-306행 `_n_factor`, `_width`; 371-389행 `equilibrium`; 453-499행 `dqdv`; 680-709행 `GRAPHITE_STAGING_LIT`; `graphite_ica_ch1_v1.0.10.tex` 716-743행; 저장 그래프 `anode_fit_v1_0_10_dqdv.png`, `P4_lco_heat_validation.png`, `P5_graph_suite.png`.
- 무엇이 물리적으로 틀렸나: v1.0.10 기본 코드와 저장 그래프는 graphite staging을 네 개의 식별 가능한 transition으로 보여주지 못하고, 거의 한 개의 넓은 peak로 보여준다. 기본 dataset은 각 transition에 `w`를 넣지만 동시에 `n=1.0`을 넣어 `_width()`가 `w=RT/(nF)`를 우선 적용한다. 그 결과 실제 폭은 모두 `25.691 mV`, FWHM은 약 `90.531 mV`가 된다.
- 왜 문제인가: base 지시의 물리 기대치는 `U≈0.210, 0.140, 0.120, 0.085 V`의 네 staging transition이 구분되거나, 병합된 single bell이면 문제로 flag하라는 것이다. 직접 계산에서 full graphite dQ/dV의 local maximum은 1개뿐이었다. 특히 `0.140`과 `0.120 V` 사이 간격은 약 `19.6 mV`로 개별 FWHM `90.5 mV`보다 훨씬 작다. `0.120`과 `0.085 V`도 약 `35.0 mV`로 병합이 불가피하다. 이는 area 보존 문제가 아니라 형상 물리 검증 문제다.
- refute: Ch1 716-743행은 이 상태를 어느 정도 명시한다. 즉 `n=1`이면 실제 폭이 `RT/F≈25.7 mV`이고 `w` fallback은 `n` 제거 시에만 활성이라고 문서화되어 있으므로, 완전한 은닉 버그는 아니다. 그러나 v1.0.10의 대표 실행 결과와 저장 그래프가 여전히 이 병합 형상을 release baseline처럼 제시하므로, 검수상 문제는 남는다.
- 렌즈: graph shape, distortion, extreme-condition overgeneralization.

### [HIGH] Ω>2RT first-order 영역을 equilibrium broad bell로 실행해 plateau/delta 해석과 충돌한다

- 위치: `Anode_Fit_v1.0.10.py` 302-306행 `_width`; 371-389행 `equilibrium`; 680-709행 `GRAPHITE_STAGING_LIT`; `graphite_ica_ch1_v1.0.10.tex` 732-743행; `graphite_ica_ch2_v1.0.10.tex` 539-568행.
- 무엇이 물리적으로 틀렸나: 기본 graphite transition들은 모두 `Omega > 2RT`로 입력되어 있는데, 실행 모델은 `Omega`를 폭 계산에 쓰지 않고 모든 transition을 logistic bell로 만든다. Ch1/Ch2는 two-phase equilibrium에서는 sharp line 또는 delta적 응답이고, 실제 finite width는 kinetic, heterogeneity, edge, apparent-U 분포 등 phenomenological broadening으로 다루어야 한다고 정리한다.
- 왜 문제인가: 코드 메서드 이름과 그래프는 `equilibrium()` dQ/dV처럼 보이지만, 실제 형상은 two-phase equilibrium 해가 아니라 phenomenological bell이다. 이 구분이 흐려지면 사용자가 `Omega>2RT`의 first-order 물리를 broad thermal peak로 오해할 수 있다.
- refute: v1.0.10 문서는 구버전의 `w_eff=(RT/F)(1-Omega/2RT)`를 제거하고, two-phase `w`를 phenomenological fitting width로 낮춘다. 이 방향 자체는 구버전보다 맞다. 문제는 코드의 기본 실행 경로와 그래프가 equilibrium/phenomenological broadening의 경계를 충분히 분리하지 않는다는 점이다.
- 렌즈: extreme-condition overgeneralization, silent assumption, graph interpretation.

### [HIGH] LCO MIT gate가 물리 anchor가 아니라 tier-C placeholder `x_MIT=0.50`으로 실행된다

- 위치: `Anode_Fit_v1.0.10.py` 617-640행 `LCO_MSMR_LIT`; 657-673행 `_effective_dS_rxn`; `graphite_ica_ch1_v1.0.10.tex` 319-342행, 1068-1096행, 1729-1738행; `FITTING_GUIDE.md` 20행, 28행, 44-45행; `P5_graph_suite.png` V6.
- 무엇이 물리적으로 틀렸나: v1.0.10 실행 dataset은 LCO electronic term을 second transition에 두고 `x_center=0.50`, `x_MIT=0.50`으로 계산한다. 그러나 Ch1과 fitting guide는 물리 anchor를 `x_MIT≈0.85`로 둔다. 즉 코드 실행 그래프의 MIT entropy gate 위치가 문서의 물리 anchor와 다르다.
- 왜 문제인가: C1 렌즈에서 MIT gate 위치는 단순 표시값이 아니라 electronic entropy contribution이 어느 LCO transition에 붙는지를 결정한다. 직접 실행 결과에서도 second transition의 effective entropy만 `-49.678 J mol^-1 K^-1`로 크게 바뀌며, `P5` V6은 `x_MIT=0.50`과 `0.85`의 위치 차이를 시각적으로 보여준다. 현재 기본 실행값은 LCO 물리 검증용 baseline으로 쓰기 어렵다.
- refute: `graphite_ica_ch1_v1.0.10.tex`와 `FITTING_GUIDE.md`는 이 값을 tier-C placeholder로 분명히 경고하고, fitting 단계에서 T1=MIT로 재정렬해야 한다고 쓴다. 따라서 이론 문서가 MIT anchor를 모르는 것은 아니다. 다만 release code와 graph validation은 placeholder를 실제 산출물로 실행하고 있으므로 결함 또는 최소한 강한 제한사항으로 남는다.
- 렌즈: LCO electronic entropy physics, MIT gate, MSMR mapping.

### [MED] LCO electronic entropy의 T 의존성이 frozen constant로 축소되어 T^2 전압 곡률을 검증할 수 없다

- 위치: `Anode_Fit_v1.0.10.py` 657-673행 `_effective_dS_rxn`; 544-588행 `entropy_coefficient`, `reversible_heat`; `graphite_ica_ch1_v1.0.10.tex` 1047-1066행, 1123-1130행; `FITTING_GUIDE.md` 28행; `P5_graph_suite.png` V7.
- 무엇이 물리적으로 틀렸나: Ch1은 electronic entropy가 `T`에 비례하고 전압 항은 `T^2-T0^2` 형태의 curvature를 가진다고 전개한다. 그러나 코드의 `_effective_dS_rxn()`은 electronic term을 `T_ref=298.15 K`에서 한 번 계산한 상수로 고정한다.
- 왜 문제인가: 이 구조에서는 LCO MIT electronic entropy의 핵심 signature인 temperature curvature를 multi-temperature graph나 fitting에서 검증할 수 없다. `P5` V7도 frozen approximation이 linear이며 `T^2` curvature가 unimplemented라고 보여준다.
- refute: fitting guide가 이 문제를 Phase D 정정 사항으로 명시하므로, v1.0.10의 알려진 미완성으로 볼 수 있다. 하지만 C1 기준에서는 현행 executable이 전자엔트로피 물리를 구현했다고 보기 어렵다.
- 렌즈: LCO electronic entropy physics, temperature validation.

### [MED] LCO MSMR homology는 문서상 구조만 있고, 기본 dataset/그래프는 T1/T2/T3 peak 구성을 재현하지 않는다

- 위치: `Anode_Fit_v1.0.10.py` 617-640행 `LCO_MSMR_LIT`; `graphite_ica_ch1_v1.0.10.tex` 311-317행, 1740-1765행; 저장 그래프 `P4_lco_heat_validation.png`, `P5_graph_suite.png`.
- 무엇이 물리적으로 틀렸나: Ch1은 LCO transition anchor로 대략 `3.90`, `4.05`, `4.17-4.20 V`를 둔다. 하지만 실행 dataset은 `3.930`, `3.880`, `4.050 V`만 갖고, `4.17-4.20 V` T3 성분이 없다. 직접 계산한 LCO dQ/dV local peak도 약 `3.919 V`, `4.037 V` 두 개뿐이다.
- 왜 문제인가: MSMR homology 자체는 parameter replacement로 가능하더라도, 현재 release graph는 문서가 말하는 LCO 3-transition 구조를 보여주지 않는다. 특히 electronic term이 `3.88 V` placeholder에 붙어 있어 T1/T2/T3 mapping이 실제 물리 anchor와 어긋난다.
- refute: 이 역시 문서와 guide가 placeholder라고 밝히므로, 이론 전체의 오류라기보다는 실행 baseline과 validation graph의 약점이다.
- 렌즈: MSMR homology, LCO mapping, graph validation.

### [LOW] graph suite의 area 보존 검증은 tail truncation에 민감하다

- 위치: `graph_suite_p5.py` 87-93행; `P5_graph_suite.png` V9.
- 무엇이 물리적으로 틀렸나: V9는 graphite dQ/dV area ratio를 약 `0.9790`으로 보여준다. 별도 측정에서도 integration window를 `0-0.32 V`로 두면 full graphite area가 `0.9480`으로 `Qsum=0.97`보다 낮게 나온다. 넓은 logistic tail 때문에 finite window 선택에 민감하다.
- 왜 문제인가: area 보존은 MSMR/ICA 구현의 중요한 sanity check인데, 현재 graph validation은 finite voltage window truncation 효과를 충분히 분리하지 않는다. 형상 문제보다 약하지만, PASS/FAIL 게이트로 쓰기에는 취약하다.
- refute: 오차 규모는 HIGH급 물리 결함은 아니다. 더 넓은 window를 쓰거나 analytic area를 같이 제시하면 쉽게 해소될 가능성이 높다.
- 렌즈: numerical validation, graph gate.

## cross-version omission judgement

- 구버전 v5의 `w_eff=(RT/F)(1-Omega/2RT)` 계열 전개는 v1.0.10에서 의도적으로 제거된 것으로 판단한다. v5 자체도 `Omega>2RT`에서 phase separation/plateau line 문제가 있음을 말하고, v1.0.10 Ch1/Ch2는 two-phase width를 phenomenological fitting width로 재정의한다. 따라서 이 제거는 결함이 아니라 정정에 가깝다.
- 다만 v5 1518-1585행의 master algorithm, 1590-1615행의 실무 fitting 절차, 1640-1685행의 hold-out prediction/diagnostic table은 v1.0.10의 46행짜리 `FITTING_GUIDE.md`로는 충분히 보존되지 않았다. 이는 LCO 전자엔트로피 자체의 구버전 누락은 아니지만, v1.0.10을 G-usable fitting package로 만들 때 실무 절차가 약해진 cross-version omission이다.
- v5는 graphite 중심 문서라 LCO/MIT/electronic entropy가 없었다. 따라서 "v5의 LCO 물리가 v1.0.10에서 누락되었다"는 식의 결론은 근거 미발견이다.

## 가장 약한 1곳

- 가장 약한 지적: `[LOW] graph suite의 area 보존 검증은 tail truncation에 민감하다`.
- 약한 이유: area ratio `0.9790`은 이미 꽤 근접하고, integration window만 넓히면 개선될 수 있는 numerical presentation 문제다. graphite peak 병합, LCO MIT gate placeholder, electronic T^2 미구현처럼 물리 결론을 직접 흔드는 문제보다 우선순위가 낮다.

## 5-line summary

1. C1 focus에서는 graphite graph shape, LCO MIT gate, electronic entropy temperature dependence가 핵심 결함 후보로 확인됐다.
2. 문제 의견 수: HIGH 3건, MED 2건, LOW 1건.
3. 가장 심각한 문제는 v1.0.10 기본 graphite dQ/dV가 네 staging transition을 한 개의 broad bell로 병합하는 점이다.
4. 그래프 직접 실행 및 육안 판독 결과, graphite는 4 peak가 아니라 1 peak이고 LCO는 문서상 T1/T2/T3 구조가 아니라 2 peak placeholder에 가깝다.
5. false-positive self-label: LCO placeholder와 `n=1` 폭 문제는 문서가 이미 경고한 부분이므로, "은닉 오류"가 아니라 "release/demo baseline으로 쓰면 안 되는 알려진 미완성"으로 낮춰 읽어야 한다.
