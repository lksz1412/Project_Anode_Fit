# Phase 059 production-code source review

이 문건은 Step 34.1 정적 소스 감사다. runtime test, test adequacy,
theory conformance와 실험 타당성 판정은 후속 단계다.

## 계보

- unique production blobs: 4
- occurrence paths: 6
- fully read lines: 3704
- v1.0.16, v1.0.17, v1.0.18.1은 동일 Git blob이다.

| Pair | Lines | Functions added | Functions removed | Functions source-changed |
|---|---:|---|---|---:|
| code_v1014_to_v1015 | 904→895 | _causal_memory_pointwise | _causal_lowpass, func_U_j_hys | 4 |
| code_v1015_to_v1016 | 895→930 | GraphiteAnodeDischargeDQDV._dwdT | — | 4 |
| code_v1016_to_v1018_2 | 930→975 | GraphiteAnodeDischargeDQDV._S_vib, GraphiteAnodeDischargeDQDV._vib_dS, GraphiteAnodeDischargeDQDV._vib_dU, GraphiteAnodeDischargeDQDV._vib_theta | — | 3 |

## 정적 판정

| ID | Severity | Disposition | Finding | Source anchors |
|---|---|---|---|---|
| P059-CODE-001 | INFO | PRESERVE | Pointwise grid removal is source-confirmed | Anode_Fit_v1.0.15.py:105 |
| P059-CODE-002 | CRITICAL | CORRECT | Voltage sorting destroys supplied trajectory order | Anode_Fit_v1.0.18.2.py:517 |
| P059-CODE-003 | HIGH | CORRECT | Finite-window initial state is forced to equilibrium | Anode_Fit_v1.0.18.2.py:122 |
| P059-CODE-004 | CRITICAL | CORRECT | Direct L_V override has no zero-current limit | Anode_Fit_v1.0.18.2.py:412; Anode_Fit_v1.0.18.2.py:418 |
| P059-CODE-005 | CRITICAL | REJECT | Local voltage-dependent barrier is frozen at one cutoff affinity | Anode_Fit_v1.0.18.2.py:430 |
| P059-CODE-006 | CRITICAL | CORRECT | C-rate and Q_cell unit contract is ambiguous | Anode_Fit_v1.0.18.2.py:599; Anode_Fit_v1.0.18.2.py:615 |
| P059-CODE-007 | HIGH | CORRECT | Default thermal width and default dwdT disagree | Anode_Fit_v1.0.18.2.py:314; Anode_Fit_v1.0.18.2.py:332 |
| P059-CODE-008 | HIGH | CORRECT | Lag kinetics collapses local T(V) to one mean temperature | Anode_Fit_v1.0.18.2.py:525; Anode_Fit_v1.0.18.2.py:565 |
| P059-CODE-009 | MEDIUM | CORRECT | Einstein reference temperature is finite but not positive | Anode_Fit_v1.0.18.2.py:369 |
| P059-CODE-010 | HIGH | EMPIRICAL_ONLY | LCO electronic entropy is frozen at 298.15 K | Anode_Fit_v1.0.18.2.py:794 |
| P059-CODE-011 | CRITICAL | CORRECT | High-voltage doped LCO scope is absent from defaults | Anode_Fit_v1.0.18.2.py:730; Anode_Fit_v1.0.18.2.py:748 |
| P059-CODE-012 | INFO | COPY_FORWARD | v1.0.16 through v1.0.18.1 is one code blob | Anode_Fit_v1.0.16.py:1 |
| P059-CODE-013 | HIGH | INTERNAL_CAPABILITY_ONLY | Einstein capability is inactive in shipped defaults | Anode_Fit_v1.0.18.2.py:344; Anode_Fit_v1.0.18.2.py:804 |

## 핵심 결론

1. v1.0.15의 작업격자 퇴출과 점별 memory helper 추가는 exact code
   diff로 확인된다.
2. 그러나 입력 전위를 정렬하므로 실제 protocol chronology가
   사라지고, 첫 상태를 평형으로 강제한다. 현재 memory는 일반적인
   reversal/pulse/history model이 아니다.
3. local potential-dependent barrier 요구는 구현되지 않았다.
   affinity는 전이당 한 cutoff 값으로 동결되고, 비등온 trace의
   kinetics도 평균온도 하나로 축약된다.
4. direct `L_V`는 $I=0$보다 먼저 반환되어 zero-current limit를
   위반할 수 있고, C-rate/Q-cell 단위는 3600배 모호하다.
5. v1.0.16의 default width와 `_dwdT` fallback은 서로 다른
   temperature semantics를 갖는다.
6. v1.0.18.2 Einstein 경로는 내부적으로 추가됐지만 기본 dataset에서
   비활성이다. LCO electronic 항은 298.15 K에 동결돼 있고,
   doped high-voltage LCO scope는 없다.

정적 gate:
`PASS_P059_PRODUCTION_CODE_INDEX`,
`PASS_P059_PRODUCTION_CODE_EXACT_DIFF`.
