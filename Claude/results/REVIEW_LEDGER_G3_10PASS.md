# 10-Pass 논리 검토 Ledger — 합류 G3(Ch5~6) + G1~G3 통합 점검

**대상**: `Claude/docs/graphite_ica_consolidated_ch5_ch6_G3.tex` (+ G1/G2 통합 정합).
**원칙**: 관점 달리 10회, 논리 검증 위주, 필요시 논문 검색. **일자**: 2026-05-29.

## Round 결과
| R | 관점 | 결과 |
|---|---|---|
| R1 | 차원/단위 ($\mathcal A^{b,th}$=J/mol, $\dot Q_\hys$=W, $dq_\state/dt$) | PASS |
| R2 | 논리 비약(GS-1): branch-local db, R3-1 적용 | PASS (LOW: $U_j^b\sim$ 정의는 sketch 명시) |
| R3 | keystone: 방전 true-eq 극한서 G1/G2 환원 | PASS |
| R4 | grounding + 검색 | **MED 발견 R4-G3**: Ch5 metastable hysteresis 무인용 → Dreyer 2010(Nat.Mater. 9,448) 추가 |
| R5 | self-consistency: signed 좌표·branch 전환 continuity | PASS |
| R6 | 부호: $I_s$, $d\xi/dt$ 충/방전, $\Delta U_\hys$, charge 가역열 | PASS |
| R7 | 극한: no-hysteresis($\Delta U_\hys\to0$)→G1/G2; Plan A δ baseline(F2) | PASS |
| R8 | 관찰 anchor + N-4 backbone(보유 데이터) | PASS |
| R9 | 전달/표기 | **MED 발견 R9-G3**: $k_{j,\mathrm{lim}}$ 가 Ch6서 3회 쓰이나 합류 세트(G1/G2) 정의 부재 → G1 §barrier 에 직렬식 `eq:kphys_series` 추가 |
| R10 | GS-4 + falsification: empirical branch 배제, Prony $a_\ell\ge0$, χ vs η_ct 분리 | PASS |

## 검색 보완
- **Dreyer 외 2010** "Thermodynamic origin of hysteresis in insertion batteries" (Nat. Mater. 9, 448):
  삽입전극 hysteresis = 다입자 metastability(non-monotone single-particle free energy) → Ch5 의
  ``hysteresis 는 metastable path 일 때만''원칙의 1급 grounding. (그래파이트 staging 에도 적용.)

## 조치 (적용 완료)
| # | 심각도 | 파일 | 조치 |
|---|---|---|---|
| R9-G3 | MED | G1 | `eq:kphys_series` $1/k_j=1/k_j^{act}+1/k_{j,lim}$ 정의 추가(병목 직렬, 임의 cap 아님) |
| R4-G3 | MED | G3 | Ch5 hysteresis 에 Dreyer 2010 grounding + bibitem |

## 상태
- CRIT 0. MED 2 반영. LOW 수용. 균형: G1 (k_lim 추가 후) / G2 / G3 재확인 필요.
- G1~G3 keystone 무모순 전파(P3-6) 유지. 다음: (a) 통합 문서 병합.
