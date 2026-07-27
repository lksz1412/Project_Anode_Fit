# Phase 059 golden NPZ·v1.0.15 rebaseline 감사

정본일: 2026-07-28

상태: `CONDITIONAL_P059_GOLDEN_NPZ`

## 결론

6개 release의 golden occurrence는 내용 기준 2개뿐이다.
v1.0.14 golden과 v1.0.15–v1.0.18.2 공통 golden이다. v1.0.15
pointwise-memory code 변경 commit `03dab9221d9b`에서
code와 NPZ가 함께 바뀌었고 regression harness 자체는 바뀌지 않았다.
따라서 rebaseline은 임의 파일 교체가 아니라 새 architecture의
내부 출력 snapshot을 의도적으로 다시 잡은 기록이다.

그러나 이 사실은 새 architecture의 물리적 정당성을 검증하지 않는다.
같은 harness가 자기 출력을 `capture`하고 다시 `verify`하므로 golden은
독립 oracle이 아니다.

## 두 unique golden의 전수 비교

- key/order/shape/dtype은 13/13 동일하다.
- unchanged arrays 2/13:
  `V, equilibrium_298`.
- changed arrays 11/13:
  `dqdv_dis_I0.02, dqdv_dis_I0.2, dqdv_dis_I1.0, dqdv_chg_I0.02, dqdv_chg_I0.2, dqdv_chg_I1.0, dqdv_T258, dqdv_T298, dqdv_T318, dqdv_TV, curve_dis_02C`.
- 최대 변화는 `3.911078294e-05`다.
- 저장된 golden delta와 현재 환경에서 직접 계산한
  v1.0.14→15 output delta의 최대 불일치는
  `4.330e-15`다.

즉 좌표와 298 K 평형 curve는 그대로이고, 유한전류·온도·T(V)·facade
11개 curve가 새 pointwise architecture 출력으로 재정초됐다.

## 현재 runtime 재생성

| version | bit-exact | atol=1e-12 |
|---|---:|---:|
| v1.0.14 | 1/13 | 13/13 |
| v1.0.15 | 1/13 | 13/13 |
| v1.0.16 | 1/13 | 13/13 |
| v1.0.17 | 1/13 | 13/13 |
| v1.0.18.1 | 1/13 | 13/13 |
| v1.0.18.2 | 1/13 | 13/13 |

전체 최대 절대차는 `4.330e-15`다. 따라서 현
`np.array_equal` gate 실패는 수 \(10^{-15}\) 규모의 runtime/library
부동소수 차이이며, 저장된 architecture delta
\(\sim10^{-5}\)와 구분된다. bit-exact 이식성은 REJECT지만
`rtol=0, atol=1e-12` 내부 회귀는 모두 성립한다.

v1.0.15와 v1.0.16/17/18.1/18.2가 이 13개 legacy output에서
각각 13/13 exact identical인 것은 후속 additive feature가 default
off라는 뜻일 뿐, 그 feature가 검증됐다는 뜻이 아니다.

## golden이 검사하지 않는 것

6개 harness 전체 token count는 `n_T1=0`,
`theta_E=0`, `LCOCathodeDQDV=0`,
direct `L_V=0`,
`nonmonotone=0`, `reversal=0`,
`pulse=0`, `3600=0`다.

따라서 다음은 golden 권위 밖이다.

- 입력 chronology, reversal, pulse, rest와 초기 state
- direct \(L_V\)의 \(I\to0\) 극한과 SI C-rate/Ah/C 환산
- \(n(T)\), default \(\partial w/\partial T\), entropy와 heat
- Einstein 입력·reference guard와 material calibration
- LCO rate dependence, 전자 온도의존, doped high-voltage state
- 공개 실험값, optimizer state, covariance와 불확도

NPZ의 evidence class는 `DERIVED_MODEL_OUTPUT_SNAPSHOT`이다.
실험 데이터나 저장된 fit/optimizer 재현 상태로 읽으면 안 된다.

## v1.0.15 rebaseline 판정

- 보존: 새 architecture가 의도한 13개 legacy output을 고정한
  internal regression snapshot이라는 기록.
- 정정: “13/13 bit-exact gate green”은 runtime-independent
  과학 검증이 아니다.
- 한계: rebaseline은 chronology sorting, 단위, local barrier,
  LCO와 후속 \(n(T)\)/Einstein branch를 검사하지 않아 해당 결함을
  발견하거나 배제할 수 없다.

Step 34 code/test/demo/golden 감사는 이로써 끝났다. 다음 Step 35.1은
18개 PDF 492쪽의 전 페이지 render·기계/시각 검독이다.
