# Phase V3 — 유한율속 브로드닝(source ①)·분극 공개데이터 검증 Result

## Summary
공개 **율속 시리즈**(Zenodo 20323533, DLR 흑연-SiOx 음극 반쪽셀, delith I∝1:2:5:10:20 = 5수준)로 문건 유한율속 물리를 검증했다. ⚠상용 harvested 음극(흑연≠SINTEF)이라 '경향' 검증. 결과: 문건의 **두 유한율속 기제가 실측에 모두 나타남** — (1) source ① 브로드닝: 전류↑ → 스테이징 피크 **broaden·lower**(높이 191→3, ~10mA서 완전 washout); (2) **분극 shift**: 피크가 고전위로 선형 이동(**20 mV/mA, 선형 R²=0.86**) = 문건 `V_n=V_app−|I|·Rn`(Rn≈20Ω). 정성·반정량 확인. 정량 `L_V∝|I|` 는 상용 SiOx confound(농도분극·harvested)로 단순 피크추적 불가 → 출하 `dqdv()` 전체 피팅이 정식 검증(다음 단계).

## Step Range
Cumulative **23–25** (V2c 16–22 이어).

## Inputs
- 실측: `dlr/rate_delith.csv`(Zenodo 20323533, 흑연-SiOx 음극 delith 율속, latin-1 CSV). 컬럼 V/I/Capacity/Cycle/StepCapacity/AmbientT.
- 모델 근거: §7 source ①(L_V∝|I| 비대칭 꼬리)·eq:vn 분극(`V_n=V_app−σ_d|I|R_n`)·`func_L_q`(L105–112).

## Files Created
- `comp_v24/v24_rate_broadening.py`·`rate_broadening.png`(3패널: 율속 overlay·높이 vs|I|·위치 shift vs|I|)·`rate_broadening_result.json`.

## Files Updated
- (없음)

## Read Coverage
- `func_L_q`(L_V∝|I| 확인)·§7 브로드닝 3출처·eq:vn 분극. rate CSV 5수준 전수 스캔.

## Execution Evidence
| I(mA) | 피크 V | 높이 | 상태 |
|---:|---:|---:|---|
| 1.0 | 0.111 | 190.6 | near-eq sharp |
| 2.0 | 0.165 | 138.1 | broaden+shift |
| 5.1 | 0.204 | 99.2 | broaden+shift |
| 10.2 | (0.21) | 16.4 | **washout** |
| 20.4 | (0.21) | 3.0 | **washout** |
- **① 브로드닝**: 높이 191→3(20× 전류) 단조 감소, ~10mA서 스테이징 피크 소멸 = L_V 가 peak 폭 초과 → 문건 ① 정성 확인.
- **분극**: 피크 위치 = 0.105 + 20.2 mV/mA·I (선형 R²=0.86) → `V_n=V_app−|I|Rn`(Rn≈20Ω) 확인.
- **의의(M-factor)**: 사용자 코인셀은 유한율속 → ①(peak 낮아짐)+분극이 dV/dQ 높이 왜곡의 실제 원인. 평형(V2)+유한율속(V3) 둘 다 문건이 설명 → M 불필요 논거의 유한율속 절반 실증(정성).

## Validation
| 게이트(V3) | 판정 | 근거 |
|---|---|---|
| ① 브로드닝 방향 | PASS | 높이 단조↓·washout(정성) |
| 분극 shift | PASS | 20mV/mA 선형 R²=0.86 (V_n=V−|I|Rn) |
| 정량 L_V∝|I| | **DEFER** | 상용 SiOx confound → 출하 dqdv() 전체 피팅 필요(다음) |

## Gate
**PASS(정성·반정량).** 문건 유한율속 2기제(① 브로드닝·분극) 공개데이터 확인. 정량 L_V∝|I| 는 V3-정량(dqdv() 피팅)으로 이월.

## Confirmed Non-Changes
- 코드·문건 무수정. 원자료 미변조.

## 추가 후보
1. **V3-정량**: 출하 `dqdv(V_app,T,I_abs,Q_cell,s)` 로 5율속 동시 피팅(Rn+L_V 공유) → L_V∝|I| 정량 검증. 더 깨끗한 순수흑연 율속셋 있으면 우선.
2. **온도축**: O'Regan 2022(Zenodo 5171874) dU/dT 엔트로피 → 문건 ∂U_j/∂T=ΔS_rxn/F·발열 검증(공개 온도의존, 별 phase).
