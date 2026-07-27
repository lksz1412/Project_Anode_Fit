# Phase 058 R1 철회 cross-artifact 재판정

정본일: 2026-07-28

대상: Phase 058 Step 30.3

기계 matrix:
`Codex/results/PHASE_058_R1_WITHDRAWAL_CONSISTENCY_MATRIX.json`

## 결론

R1 철회는 좁은 의미에서 맞다. 이 kernel은 네 peak를 만들 수 있다.
그러나 그 사실로 apparent-potential broadening 물리 전체가 검증됐다는
확장 결론은 source, code, test와 figure를 함께 놓으면 성립하지 않는다.

최종 판정:

`R1_WITHDRAWAL_IS_CONSISTENT_ONLY_FOR_NUMERICAL_FLEXIBILITY_NOT_FOR_PHYSICAL_CLOSURE`

## 수치 표현력

v1.0.12 production을 원본 수정 없이 계산하면 298.15 K에서

| 설정 | \(w\) | local maxima |
|---|---:|---:|
| shipped \(n=1\) | 25.691 mV | 1 |
| demo \(n=0.12\) | 3.083 mV | 4 |

이다. 따라서 최초 R1의 “구조적으로 분리 peak 생성 불가”는
기각해야 한다.

하지만 shipped transition 네 개는 여전히 모두 `n=1`이고, dict에
같이 든 `w=0.020/0.016/0.014/0.012 V`는 `n` 우선순위 때문에
사용되지 않는다. 즉 v1.0.12는 default를 고친 버전이 아니라,
sample에서 fit handle을 바꿔 표현력을 보여 준 버전이다.

## theory source의 상태

좋아진 점은 분명하다. Chapter 1은 두-상 평형 near-delta와
관측 broadening을 구분하고

\[
 \left\langle\frac{dQ}{dV}\right\rangle
 =
 \int \rho(U_{\rm app})
 \left(\frac{dQ}{dV}\right)^{\rm single}_{U_{\rm app}}
 dU_{\rm app}
\]

라는 forward ensemble 식을 쓴다. unconstrained inverse
\(\rho\) 또는 PSD 역산을 금지한 것도 타당하다.

그러나 같은 절 안에 모순이 남는다.

- 본문: 유한전류 ①은 \(w_j\)에 넣지 않고 \(L_V\)로 별도 처리
- keybox: ①·②·③ “셋을 한꺼번에 흡수”하는 것이 \(w_j\)

또 원고는 explicit \(\rho(U_{\rm app})\) 적분을 설명하지만 code는
이를 계산하지 않고 단일 logistic `w` 한 개로 대체한다. 따라서
conceptual layer는 생겼어도 theory–code 100% conformance는 아니다.

## code와 default current behavior

`n` 또는 `w`를 바꿔 curve를 만드는 것은 가능하다. 그러나 이것은
fit flexibility다. phase assignment나 broadening provenance는
parameter value만으로 나오지 않는다.

더구나 `Rn=0`의 shipped default에서 \(I=0\)과 1 A curve의 최대
차이는 정확히 0이다. R1 sample의 좁은 peak 시연은 사용자의
유한전류 peak suppression/broadening을 검증하지 않는다.

## test와 figure

v1.0.12 sample source와 PNG는 같은 commit에 있어 provenance는
현재다. 그림도 `default n=1 = merged`, `fitted n=0.12 = four
resolved`를 정직하게 표시한다. 이 부분은 보존한다.

그러나 sample은 스스로 `report only; no physics assertion`이라 쓰고
peak count가 틀려도 실패하지 않는다. Python `assert`는 0개다.

더 심각하게 v1.0.12 regression은 byte-identical copy라 아직도
`v1.0.10/Anode_Fit_v1.0.10.py`를 hardcode한다. 그 test는
v1.0.12 module이나 R1 peak separation을 gate하지 않으며, area도
출력만 한다.

따라서 현재 evidence chain은 다음에서 끝난다.

\[
 \text{code can draw four peaks}
 \quad\text{and}\quad
 \text{stored figure shows them}.
\]

다음으로 넘어가지 못한다.

\[
 \cancel{
 \text{the fitted width is identified as equilibrium/heterogeneity/kinetics}
 }
\]

## 최종 방향

near-delta를 항상 별도 convolution으로 강제하거나 measured peak에서
\(\rho\)를 역산하는 처방은 채택하지 않는다. 하지만 “재설계 금지”도
기각한다.

후속 canonical model은 최소한 다음 forward hierarchy를 분리해야 한다.

1. phase-specific equilibrium free energy
2. current-, temperature-, potential- and state-dependent kinetics
3. electrode/particle heterogeneity distribution
4. instrument and numerical observation kernel

각 층을 전부 자유화하지 않고, quasi-equilibrium, rate series,
multi-temperature, rest/GITT와 instrument metadata로 순차 식별한다.
이것이 R1 최초 오판과 전면 철회의 양쪽 과장을 피하는 결론이다.

Step 30은 완료됐다. 다음 Step 31.1에서 v1.0.13의 partition function,
occupancy, chemical potential, Nernst/logistic와 multi-transition 합을
표준 통계역학에서 다시 유도한다.
