# Anode_Fit ↔ BDD 통합 Plan — 이론 양음극 곡선으로 셀 상태 추론

> 작성 2026-07-18. 표준 11-section 양식. cumulative step 단조.
> 근거 = BDD repo(lksz1412/batterydata_display) `99_Backend.py` `BatteryData_Matching` 실측 + Anode_Fit v1.0.23 + 사용자 맥락.
> 성격 = **계획서**(GO 대기). 여러 요청을 하나로 정리.

---

## Summary

**큰 그림(사용자 맥락)**: BDD는 풀셀(FC) dQ/dV·DVA를 **양극(CT)−음극(AN) 성분으로 분해**해 셀 열화를 해석한다(`BatteryData_Matching`, 9-파라미터 매칭). 그 분해는 **AN·CT 반쪽셀 곡선**을 입력으로 요구하는데, 실측(코인셀)은 **노이즈가 심해 처리 곤란**하다. 게다가 곡선이 **T·I·V에 매우 민감**하다. → 그래서 **Anode_Fit이 그 반쪽셀 곡선을 이론으로(깨끗·T/I/V 의존) 생성**하려는 것이다. 두 프로젝트는 **입력↔공급** 관계다.

**이 계획의 목표**: 사용자 요청 5건을 하나의 로드맵으로 정리한다 — ① BDD 9-파라미터 방향성 검토(제대로 잡았나) ② 열화 시 어느 파라미터가 움직이는지 조사(문헌+매핑) ③ 공개 데이터 확보 + Anode_Fit 검증 + 동역학(lag) 테스트 ④ Anode_Fit→BDD 통합 설계 ⑤ Anode_Fit 클래스별 상세 코드 가이드.

**핵심 논지**: Anode_Fit은 BDD가 지금 실측으로 얻는 노이즈 곡선을 대체할 뿐 아니라, BDD가 **ad-hoc으로 피팅하는 파라미터(M 전압신축·X·Y 후피크 신축)를 물리로 제약**할 수 있다(예: 반쪽셀 OCV는 재료 고유값이라 M≈1로 고정되어야 함 — 사용자 의심의 물리적 근거).

---

## Current Ground Truth

**확인된 사실.**
- **BDD 9-파라미터**(`99_Backend.py:1090` minimize docstring): `AN_M, AN_A, AN_B, CT_M, CT_A, CT_B, X, Y, Z`.
  - 매칭 모델(RMSE_1~4): FC = CT − AN, 공통 용량축 보간. 각 전극 변환: 용량 `Q→Q·A+B`, 전압 `V→누적차분×M 신축`, `dVdQ→dVdQ/A·M`. `Z`=AN 전압 이동. `X/Y`=마지막 AN dVdQ 피크(`point`) 이후 용량/전압 신축.
  - **staged fit**: `guess_initial_coefficient`(피크비 기하로 A·B 초기값) → RMSE_1(AN_M,CT_M) → RMSE_2(+CT_A,CT_B) → RMSE_3(AN_M,A,B·CT_M,A,B·Z) → RMSE_4(X,Y). bounds: M∈[0.8,1.2]·A∈[0.6,1.4]·B∈[0.4,1.6]·X,Y∈[0,2]·Z∈[−1,1].
  - 최적화기: `optuna_wrapper`(CMA-ES/GP) + `minimize_parallel`(Nelder-Mead 다중시작). RMSPE 잔차.
- **양음극 분리 위치**(사용자 지적): `Lib_LKS_BatteryData_99_Backend.py` (`BatteryData`, `BatteryData_Matching`, `BatteryData_Aging`).
- **BDD 기존 Anode_Fit 검토 존재**: `v1.2.1_20260707/정리본/S6_AnodeFit_review.md`·`S_AnodeFit_v1017_review.md`(미정독 — Phase 입력).
- **Anode_Fit v1.0.23**: forward 반쪽셀 dQ/dV(흑연/LCO/Si·블렌드)+열특성+동역학 lag. 병합 준비 완료. `CODE_GUIDE_v23.md` 6-레벨 존재.
- **사용자 제약**: 실측 데이터 전량 회사 귀속 → **반출 불가**. 공개 데이터 필요. 위치 모름.

**예비 판정(9-파라미터 방향성 — Phase W1에서 정식화).**
- **AN_A·CT_A(용량 신축)** = 전극 활물질량 → **LAM**(활물질 손실) 프로브. **물리적으로 타당**(Dubarry/Birkl 정통).
- **AN_B·CT_B(용량 오프셋)** = 전극 슬리피지 → **LLI**(리튬 재고 손실) 프로브. **타당**.
- **Z(전압 이동)** = OCV 기준/영점 오프셋 흡수. 합리적.
- **AN_M·CT_M(전압축 신축)** = ⚠ **물리적 의문**. 반쪽셀 OCV vs Li는 재료 고유 곡선 — 열화로 "신축"하지 않는다. M을 자유변수로 두면 다른 곳에 귀속될 오차를 흡수해 **과적합·열화모드 오귀속** 위험. bound가 [0.8,1.2]로 좁아 피해는 제한적이나 방향성 재검토 대상. **사용자 의심의 근거가 여기 있음.**
- **X·Y(후피크 신축)** = ⚠ 마지막 AN 피크 이후(stage 1 평탄역) 곡선 형상 보정 — 물리 모드가 아닌 **형상 fudge**. Anode_Fit의 stage-1 평탄역 물리로 대체 가능성 검토 대상.

**미확인(추정 금지).**
- BDD의 M·X·Y가 실제로 개선을 주는지 vs 과적합인지 — 정량 미검증(Phase W1).
- 어느 공개 데이터가 **반쪽셀(또는 3전극) + 노화 시퀀스**를 함께 제공하는지 — 조사 필요(Phase W3).
- Anode_Fit forward가 실측 곡선 개형을 물리 파라미터로 재현하는지 — 미검증(Phase W3).
- BDD `S6_AnodeFit_review.md` 결론 — 미정독.

---

## Phase Range

| Phase | 이름 | Steps | 게이트 요지 | 상태 |
|---|---|---:|---|---|
| **W0** | 착수·BDD 정독 | 1-3 | BDD 매칭·리뷰문서·config 전수 read·Anode_Fit↔BDD 인터페이스 확정 | 대기 |
| **W1** | 9-파라미터 방향성 검토 | 4-9 | 각 파라미터 물리 귀속 판정·M/X/Y 과적합 정량 진단·식별성 | 대기 |
| **W2** | 열화모드 파라미터 조사 | 10-14 | LLI/LAM/RI ↔ 파라미터 이동 문헌(웹)·BDD/Anode_Fit 매핑표 | 대기 |
| **W3** | 공개데이터 + 검증 + 동역학 | 15-22 | 데이터셋 확보·Anode_Fit forward 실측 재현·T/I/V·lag 테스트 | 대기 |
| **W4** | Anode_Fit→BDD 통합 설계 | 23-27 | 이론곡선 공급 인터페이스·M/X/Y 물리제약 대체안 | 대기 |
| **W5** | 클래스별 상세 코드 가이드 | 28-31 | Anode_Fit 3클래스 각 상세 설명문(mermaid) | 대기(병렬 가능) |

> Phase 는 통합 캠페인 귀속. step 단조 누적. BDD측 집행은 **BDD repo 자체 규약**(다음 턴 로드될 CLAUDE.md/harness) 준수.

---

## Non-goals

- **Anode_Fit v1.0.23 문건 수정 X** — 완결·병합 준비 완료. 이 캠페인은 그 위에 응용(BDD 통합)·검증.
- **BDD 코드 즉시 수정 X** — W1은 **검토·진단**(수정 아님). 실제 BDD 수정은 별도 GO + BDD 규약 하에서.
- **회사 귀속 실측 데이터 사용 X** — 공개 데이터만. 사용자 데이터 반입 요청 안 함.
- **역문제 풀 솔버 즉시 구현 X** — W1~W3 식별성·검증 결과 본 뒤 필요만큼(과잉 방지).
- **전셀 재구현 X** — BDD가 이미 FC=CT−AN 분해 보유. Anode_Fit은 그 입력(반쪽셀 곡선) 공급에 집중.
- **사용자 승인 전 집행 X** — GO 대기.

---

## Implementation Changes

**생성 문서(Anode_Fit `Claude/`).**
- 본 계획서 + phase별 `results/PHASE_W{0..5}_RESULT.md`(11항) + `results/W_EXECUTION_LEDGER.md`(12-col).
- `results/comp_bdd/BDD_9PARAM_AUDIT.md`(W1) — 9-파라미터 물리 귀속·과적합·식별성 판정.
- `results/comp_bdd/DEGRADATION_MODE_MAP.md`(W2) — 열화모드↔파라미터 문헌·매핑표.
- `results/comp_bdd/PUBLIC_DATA_SURVEY.md`(W3) — 공개 데이터셋 조사·선정.
- `results/comp_bdd/FORWARD_VALIDATION.md`(W3) — Anode_Fit 실측 재현·T/I/V·lag 테스트(그림 포함).
- `results/comp_bdd/INTEGRATION_DESIGN.md`(W4) — Anode_Fit→BDD 공급 인터페이스 설계.
- `docs/v1.0.23/CODE_GUIDE_Graphite.md`·`CODE_GUIDE_LCO.md`·`CODE_GUIDE_Blend.md`(W5) — 클래스별 상세.

**BDD측(검토만·수정 아님)**: `99_Backend.py` `BatteryData_Matching` 정독·리뷰문서 정독.

**검증 산출**: 공개데이터 로드·Anode_Fit fit 스크립트(scratchpad→comp_bdd 보존)·그림.

---

## Phase W0 — 착수·BDD 정독 (Steps 1-3)

- **Step 1**: BDD `99_Backend.py` `BatteryData_Matching`(858-1240) + `BatteryData_Aging`(1240~) 전수 정독. 9-파라미터·RMSE_1~4·staged fit·optuna 래퍼 확정.
- **Step 2**: BDD `정리본/S6_AnodeFit_review.md`·`S_AnodeFit_v1017_review.md`·`docs/CHANGELOG/03_Matching.md`·`04_Aging.md` 정독(기존 Anode_Fit↔BDD 인식 파악).
- **Step 3**: Anode_Fit↔BDD **인터페이스 확정** — BDD 매칭이 요구하는 반쪽셀 입력 포맷(V, Q, dVdQ 배열·피크 id) vs Anode_Fit `curve()`/`dqdv()` 출력 대조. `W_EXECUTION_LEDGER` 초기화.
- **게이트**: 9-파라미터·매칭 모델·리뷰문서·인터페이스 4항 확정. BDD 규약(CLAUDE.md) 반영 확인.

## Phase W1 — 9-파라미터 방향성 검토 (Steps 4-9)

- **Step 4**: 각 파라미터 물리 귀속표 — AN_A/CT_A↔LAM·AN_B/CT_B↔LLI/슬리피지·Z↔OCV오프셋·AN_M/CT_M↔(의문)·X/Y↔(후피크 fudge).
- **Step 5**: **M 전압신축 과적합 진단** — 합성 FC(Anode_Fit 이론 AN·CT로 생성)에 알려진 열화 주입 → BDD 매칭이 M을 어떻게 쓰나. M을 1로 고정(limits) vs 자유일 때 RMSPE·열화모드 복원 정확도 대조.
- **Step 6**: **X/Y 후피크 진단** — 동일 합성 실험. stage-1 평탄역 물리(Anode_Fit)로 대체 가능성.
- **Step 7**: **식별성** — 9-파라미터 야코비안/조건수·파라미터 상관(공선형). 어느 쌍이 축퇴(예: AN_M↔AN_A)인지.
- **Step 8**: staged fit(RMSE_1→4) 수렴 안정성·초기값 민감도 진단.
- **Step 9**: `BDD_9PARAM_AUDIT.md` + `PHASE_W1_RESULT.md`. **판정: 방향성 유지/부분수정/재설계 권고**(정직).
- **게이트**: 각 파라미터 정량 진단(과적합·식별성 수치)·M/X/Y 판정 근거 명시.
- **중단 조건**: 합성 실험이 물리 근거 못 세우면 "미확정"으로 정직 보고(과장 금지).

## Phase W2 — 열화모드 파라미터 조사 (Steps 10-14)

- **Step 10**: 웹 문헌 조사 — 열화모드 정의(LLI·LAM_PE·LAM_NE·RI·kinetic degradation) + ICA/DVA 진단(Dubarry·Birkl·Anseán·Marmatakis 등).
- **Step 11**: 각 모드가 **어느 곡선 특징**을 움직이나(피크 위치 이동=슬리피지/LLI·피크 면적 감소=LAM·피크 둔화/이동=RI·kinetic).
- **Step 12**: → **BDD 9-파라미터 매핑**(어느 param이 어느 모드): A↔LAM·B↔LLI·M/폭↔RI/kinetic 등.
- **Step 13**: → **Anode_Fit 파라미터 매핑**(Q_j↔LAM·정렬↔LLI·R_n·L_V↔RI/kinetic).
- **Step 14**: `DEGRADATION_MODE_MAP.md` + `PHASE_W2_RESULT.md`. 무날조 서지.
- **게이트**: 문헌 근거 각 매핑 1:1·tier 표기.

## Phase W3 — 공개데이터 + 검증 + 동역학 (Steps 15-22)

- **Step 15**: 공개 데이터셋 조사·선정 — 후보: Oxford Degradation·NASA PCoE·CALCE(Maryland)·Sandia·Stanford/Toyota(Severson)·RWTH Aachen·batteryarchive.org 등. **반쪽셀/3전극 + 노화 + 율/온도** 보유 우선.
- **Step 16**: 선정 데이터 로드·전처리(V-Q → 평활 dQ/dV, Savitzky-Golay). `PUBLIC_DATA_SURVEY.md`.
- **Step 17**: **Anode_Fit forward 실측 재현** — 흑연(또는 NMC) 반쪽셀 실측 dQ/dV를 Anode_Fit 파라미터로 피팅, 물리적 파라미터로 개형 재현되나.
- **Step 18**: **T 민감도** — 온도 다른 실측 곡선을 Anode_Fit 열특성/T-의존으로 재현.
- **Step 19**: **I(율) 민감도 + 동역학 lag 테스트** — rate 다른 실측(예: fly2020류)에서 peak 이동·둔화를 Anode_Fit lag(L_V·ratio)로 재현. **QA서 발견한 휴면 문제**(1C서 L_V~1e-7) 실 파라미터로 재보정 필요성 확정.
- **Step 20**: **V(전위창) 민감도** — 전위창 다른 곡선 재현.
- **Step 21**: 재현 정확도·물리 타당성 정량(RMSPE·파라미터 범위 타당성). 그림.
- **Step 22**: `FORWARD_VALIDATION.md` + `PHASE_W3_RESULT.md`. **판정: forward 신뢰성**.
- **게이트**: 실측 1건+ 재현·T/I/V 각 1건+·lag 스케일 정합(또는 재보정안).
- **중단 조건**: 데이터 확보 실패 시 후보·접근경로 정직 보고 후 사용자 결정.

## Phase W4 — Anode_Fit→BDD 통합 설계 (Steps 23-27)

- **Step 23**: 공급 인터페이스 — Anode_Fit `curve()` 출력 → BDD `BatteryData` 입력 어댑터(V, Q, dVdQ, 피크 id).
- **Step 24**: **M/X/Y 물리제약 대체안** — W1 판정 기반. 이론곡선 사용 시 M을 1 고정, X/Y를 stage-1 물리로 대체하는 축소 파라미터 셋 제안.
- **Step 25**: 열화 추론 파이프라인 설계 — 이론 AN/CT(clean) → BDD 매칭 → LAM/LLI/RI 상태 추출.
- **Step 26**: 식별성 개선 확인(W1 대비 축퇴 감소).
- **Step 27**: `INTEGRATION_DESIGN.md` + `PHASE_W4_RESULT.md`.
- **게이트**: 어댑터 명세·축소 파라미터 셋·파이프라인 다이어그램.

## Phase W5 — 클래스별 상세 코드 가이드 (Steps 28-31, 병렬 가능)

- **Step 28**: `GraphiteAnodeDischargeDQDV` 상세(메서드별 로직·식·호출관계 mermaid).
- **Step 29**: `LCOCathodeDQDV` 상세(상속+seam).
- **Step 30**: `BlendedAnodeDQDV` 상세(합성).
- **Step 31**: mermaid 렌더 검증 + `PHASE_W5_RESULT.md`.
- **게이트**: 3클래스 각 상세·mermaid 렌더 통과.

---

## Implementation Interfaces

- **BDD 반쪽셀 입력**: `BatteryData` 객체(`Volt`, `Capa`, `dVdQ` 배열 + `peak_points_fin` + `ids`). Anode_Fit 어댑터가 이 포맷 생성.
- **9-파라미터 진단 실험**: 합성 FC = Anode_Fit(AN 이론) − Anode_Fit(CT 이론) + 알려진 열화 주입 → BDD 매칭 복원율.
- **식별성**: 야코비안 J=∂(FC곡선)/∂params, cond(JᵀJ)·상관행렬.
- **문서 양식**: Result 11항·Ledger 12-col([[feedback_phase_execution_loop]]).
- **BDD 코드 규약**: 다음 턴 로드될 BDD CLAUDE.md/`.harness` 준수(BDD측 작업 시).

## Test Plan

- **9-파라미터 진단**: 합성 실험 복원 정확도·M 고정 vs 자유 RMSPE·조건수.
- **공개데이터 재현**: RMSPE·물리 파라미터 범위 타당성·T/I/V 각 조건.
- **lag 스케일**: fly2020류 peak 이동(mV)을 Anode_Fit이 물리 파라미터로 내나.
- **식별성**: cond(JᵀJ) 임계·파라미터 상관 |ρ|.
- **문헌 대조**: 열화모드 매핑 서지 무날조·tier.
- **mermaid**: 클래스 가이드 렌더 검증.

## Assumptions

- BDD 매칭 모델(FC=CT−AN)이 Anode_Fit 반쪽셀 곡선을 입력으로 그대로 받을 수 있다(포맷 어댑터로 해소 — W0 확인).
- 공개 데이터 중 최소 1건이 Anode_Fit 검증에 충분한 반쪽셀/노화/율·온도 정보를 가진다(W3 확인·실패 시 사용자 결정).
- BDD의 M/X/Y가 이론곡선 사용 시 축소 가능하다(W1 진단으로 확정).
- 사용자 목표 = 이론 곡선으로 노이즈 실측을 대체해 셀 상태(LAM/LLI/RI) 추론.

## Correction History

- 신규 계획서(직전본 없음). 사용자 다건 요청(9-파라미터 검토·열화조사·공개데이터/동역학 테스트·클래스가이드·통합)을 단일 11-section 로드맵으로 정리.
- 초기 오해 정정: `_신규9_구현_STATUS.md`의 "9"는 **파일 9개**(BDW 웹판)이지 9-파라미터 아님. 9-파라미터는 `99_Backend.py:1090`.
- 서지 정정: Ref.6·7은 사용자 논문 아닌 **연구실(교수·선배) 원 방법론**(lee2017jcp가 적용).

---

## Decisions Required (GO 전)

- **D1 — 착수 범위.** 기본값(권고) = **W0(BDD 정독)+W1(9-파라미터 검토) 먼저** 착수. 사용자 최대 관심사(방향성 검토)에 즉효.
  - 대안: W3(공개데이터) 먼저(데이터 확보가 병목이면).
- **D2 — 공개데이터 우선순위.** 어느 화학(흑연/graphite half-cell? NMC/LCO?)·어느 용도(노화 추론 vs 단순 forward 검증) 우선? 기본값 = **흑연 반쪽셀 + NMC/LCO 풀셀 노화 데이터 함께** 있는 셋 우선 조사.
- **D3 — BDD 코드 수정 권한.** W1은 검토만. 수정 권고가 나오면 **별도 GO + BDD repo 규약** 하에서. 기본값 = **이번엔 검토·설계까지, 수정은 다음**.
- **D4 — 클래스 가이드(W5) 타이밍.** 독립적이라 병렬 가능. 기본값 = **W1~W3 뒤 또는 요청 시 즉시**(가벼움).
- **D5 — 모델 배분.** 조사(W2·W3 데이터)=하이쿠/소넷 병렬, 진단·설계·검산=Opus 마스터.

> **어느 Phase부터 GO 줄지** 말씀 주시면 그 Phase부터 5-stage 루프로 실행. 무응답 시 D1 기본값(W0+W1)으로 대기.

> ⚠ SUPERSEDED_BY 2026-07-18-anodefit-MASTER-plan.md — BDD 통합 phase 나열본. 9-파라미터 판정(잘못된 선택·M=브로드닝 fudge)은 마스터로 승계. BDD 작업은 스코프에서 제외(사용자 결정).
