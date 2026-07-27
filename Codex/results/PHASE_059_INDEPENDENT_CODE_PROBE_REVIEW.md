# Phase 059 독립 code 물리·수치 probe 검토

정본일: 2026-07-28

범위: v1.0.14–v1.0.18.2 production 계보, Step 34.4

상태: `CONDITIONAL_P059_CODE_CONFORMANCE`

## 판정 경계

이 gate는 frozen release module을 변조하지 않고 독립 검산
22건을 완주했다는 뜻이다. 알려진 결함을 재현한
`BLOCKER_CONFIRMED`를 과학적 PASS로 세지 않는다. release test/demo는
호출하지 않았고 실험 적합성도 부여하지 않는다.

verdict 집계:

| verdict | 수 |
|---|---:|
| PASS_IDENTITY | 10 |
| PASS_GUARD | 1 |
| BLOCKER_CONFIRMED | 8 |
| SCOPE_ABSENT_CONFIRMED | 2 |
| IDENTIFIABILITY_CAUTION | 1 |

## 보존된 수학

- v1.0.15 점별 recurrence는 불규칙 격자의 상수·선형 source를
  각각 최대 오차
  `5.551e-17`,
  `2.776e-17`로 재현했다.
- 넓은 창에서 평형/지연 면적은
  `1.000000000000`,
  `0.999999999997`로 \(Q=1\)을 보존했다.
  지연 peak는 `12.5`에서
  `10.8108`로 낮아지고 FWHM은
  `0.07048` V에서
  `0.08204` V로 넓어졌다.
- resolved \(L_V\) 감소열은 평형과의 오차가 단조 감소했다.
  대칭 단일 전이의 charge/discharge mirror 최대 오차는
  `0.000e+00`다.
- explicit \(n\), \(n(T)\), `w`-only의 폭 미분은 독립
  finite difference와 일치했다. \(n(T)\) 고정-state entropy chain
  오차는 `3.588e-15` V/K다.
- Einstein 보정은
  \(\partial\Delta U_\mathrm{vib}/\partial T=\Delta S_\mathrm{vib}/F\)
  및 \(U=F+TS\), 저·고온 asymptote를 만족했다.

## 확인된 구조적 결함

1. `dqdv`는 입력 전압을 정렬한다. 같은 좌표를 섞어도 원위치로
   복구한 출력 차이가
   `0.000e+00`다.
   실제 입력 순서를 따라간 memory와는
   `21.3296`
   차이가 난다. pulse/reversal/rest chronology를 표현하지 못한다.
2. direct `L_V`는 \(I=0\)과 \(I=1\) 출력이 완전히 같고,
   \(I=0\)에서도 평형과
   `3.90339`만큼 다르다.
3. \(Q_\mathrm{cell}=3600\) C, 1C에서 facade는 3600 A를 만들며,
   SI-consistent 1 A 대비 `func_L_q` 비가 정확히
   `3600.0`다.
4. `n`/`w`가 모두 없을 때 observable 폭은 \(RT/F\)인데
   entropy 경로 `_dwdT`는 0을 반환한다. 누락량은
   `8.616883e-05` V/K다.
5. `theta_E_Tref<=0`은 fail-fast 되지 않고 non-finite
   값을 반환한다.
6. LCO 전자 엔트로피는 240–360 K에서 range
   `0.000e+00` J mol⁻¹ K⁻¹로
   완전히 동결돼 있다. 기본 LCO는 \(R_n=0\)일 때 \(I=0\)과
   \(I=1\) 곡선 차이가
   `0.000e+00`다.
7. lag resolver에는 local voltage/affinity 인자가 없고 전이 중심
   U를 0.08 V에서 0.28 V로 바꿔도 lag 차이는
   `0.000e+00`다.

## 범위·식별성 판정

- `n`과 `w`를 함께 주면 `w`를 0.003 V에서 0.090 V로 바꿔도
  곡선 차이는 `0.000e+00`다.
  두 파라미터는 동시 fit 변수가 아니라 배타적 parameterization이다.
- graphite+LCO 기본 전이 7개에
  `theta_E`는 0개다. Einstein 항은 material validation이 없는 dormant
  capability다.
- 기본 LCO 최대 중심은
  `4.05` V이고 dopant,
  oxygen-loss, surface-reconstruction state는 없다. 고전압
  doped-LCO 설명 범위가 아니다.

## Step 34.4 결론

점별 지수 memory와 \(n(T)\), Einstein 보정의 일부 수학적 항등식은
보존된다. 그러나 사용자의 출발 가설을 실제 데이터에 적용하는 데
필수인 시간 순서, \(I\to0\), SI rate 단위, local
voltage-dependent barrier, LCO rate path와 고전압 도핑 상태는
닫히지 않았다. 따라서 판정은 **독립 probe 실행 PASS,
release 물리 정합 CONDITIONAL/REJECTED 항목 병존**이다.

다음 Step 34.5에서는 두 golden NPZ의 모든 key/shape/dtype/array를
재생성해 bit-exact와 tolerance match를 분리하고, v1.0.15 rebaseline이
무엇을 고정했고 무엇을 검사하지 못했는지 판정한다.
