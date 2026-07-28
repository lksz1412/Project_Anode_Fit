# Phase 059 v1.0.16 결합 식별성 판정

정본일: 2026-07-28

판정: `FAIL_P059_V1016_JOINT_IDENTIFIABILITY_WITHOUT_MULTI_TEMPERATURE_RATE_SERIES_AND_INDEPENDENT_ELECTRONIC_VIBRATIONAL_PRIORS`

## 결론

요구 데이터 없이 네 계열을 동시에 여는 것은 구조적으로 불가능하다.
이는 optimizer 성능 문제가 아니라 서로 다른 파라미터가 같은
관측 조합으로만 들어가는 rank deficiency다.

## 수치 rank

- 단일 온도 \(n_0,n_1\): 200개 voltage point를 늘려도 rank
  1/2다. 관측되는 것은 \(n(T_k)\) 하나다.
- 단일 온도, 4 rate의 activation:
  \((\Delta H_a,\Delta S_a,\log|dV/dq|)\) rank
  1/3이다. rate는 알려진
  \(\log I\)만 바꾸고 파라미터 민감도 행을 바꾸지 않는다.
- 세 온도와 4 rate를 써도 activation rank는
  2/3이다.
  \(\Delta S_a\)와 prefactor/\(dV/dq\) 사이에 정확한 null vector가
  남으므로 하나를 독립 측정·동결해야 한다.
- 현 LCO electronic gate의
  \((\Delta S_\mathrm{base},g_\max,x_\mathrm{MIT},\Delta x)\)는
  300개 synthetic voltage weight를 줘도 rank
  1/4다. 코드가 전자항을
  \(x_\mathrm{center},298.15\) K의 한 상수로 평가하기 때문이다.
- vibrational 잔여항은 forward parameter가 없어 rank 0이다.

## 데이터가 해야 하는 일

상수-n → per-T width → 필요 시 n(T)로 가는 guide의 단계적 방향은
보존한다. 다만 완료된 식별이 아니라 필요한 데이터의 순서를 말한
것이다. 최소 계약은 다음과 같다.

1. 폭은 \(T_\mathrm{ref}\) 양쪽의 다온도 peak와 uncertainty,
   domain-wide positivity bound가 필요하다.
2. activation은 각 온도의 rate-series, 독립 OCV \(dV/dq\),
   current-interruption/transport 진단이 필요하다.
3. LCO electronic은 올바른 Li-reference entropy, composition-resolved
   \(x(V,T)\), 충분한 온도 곡률, DOS/phase-coexistence prior가 필요하다.
4. vibrational은 명시 forward term과 phonon/heat-capacity prior가
   있어야 한다. 그렇지 않으면 electronic \(T^2\) 신호에 vib 잔여가
   섞이는 것을 분리할 수 없다.

synthetic round-trip은 주어진 파라미터에서 코드가 자기 출력을
재생한다는 증거일 뿐 noise, parameter covariance, model discrepancy
아래의 statistical identifiability 증거가 아니다.

따라서 v1.0.16에는 실제 graphite/LCO/Si 데이터 피팅 권위가 없고,
특히 doped high-voltage LCO와 Si 경로는 부재한다.

## 다음 단계

Step 38.1에서 v1.0.17의 doc-only·citation 정정을 exact diff와
1차 출처로 판정한다.

원본 `Claude/`, `main`은 수정하지 않았다.
