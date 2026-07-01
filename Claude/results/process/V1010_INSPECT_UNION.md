# v1.0.10 문제검수 — 9종 단점 UNION 종합 (10차 재검 입력)

> 9 검수(S1-3·O1-3·C1-3, 각 절별 루핑·그래프 직접 실행) 단점 **전부 합집합**(체리픽 X). 클러스터·dedup·근거 검수자. ★**오적발 후보(FP?)** 표기 = 10차 재검이 진짜 문제인지 판정할 대상. 등급은 검수자 원등급의 최댓값(union이므로).

## 클러스터 A — CORE: 폭 모델이 bell(spike 아님)·4 staging 병합 [CRIT, 만장일치 실측]
- **A1** `_width`(코드 L303-306)가 **Ω 완전 무시** + `GRAPHITE_STAGING_LIT` 4전이 `'n':1.0` 디폴트 → 폭 전부 RT/F=25.69mV → logistic 도함수 FWHM 90.5mV. 전이 간격(71/20/35mV) < FWHM → 평형 곡선 local max **1개**(V=0.100). Ω=10000·50000 무관 FWHM 동일(실측). [O1·O2·O3·S1·S2·S3·C1·C2·C3]
- **A2** per-transition `'w'`값(20/16/14/12mV)이 `_n_factor`의 'n' 우선으로 **silent 무시** → 저자 의도 폭 차등 사멸·독자가 'n' pop 안 하면 그래프 불변. [O2·C2·C3]
- **A3** Ω>2RT(1차 두-상, 흑연 4전이 전부 1.2-2.6배)면 Maxwell 작도상 평형 dQ/dV=near-delta 기대인데 코드는 단일자리 Nernstian bell 보편 적용. 문건 §width는 "현상학적 자유 피팅 폭"이라 옳게 서술하나 **디폴트 코드 미이행 = 서사-코드 계약 파기**(Ch1 L1255-1257 자인). [O1·O3·C1·S2] — 렌즈4 극한 과도일반화 정확 적중.
- **FP?**: "tier-C placeholder·피팅 시 변경" 명문화 → 은닉 아님. **단 10차 쟁점**: (a) 디폴트 release 그래프·커밋 3종이 물리 오형상을 baseline처럼 제시 (b) ★폭 모델이 구조적으로 두-상 near-delta 불가(n≈0.05 비물리) — 미피팅 placeholder를 넘는 구조 결함인가?

## 클러스터 B — kinetic 꼬리 default OFF [HIGH, C2 실측]
- **B1** 기본 흑연에서 `_resolve_lag_length` L_V(4.9e-7…4.8e-9)가 작업격자 문턱(3.9e-4)의 ≤0.0025배 → `dqdv`가 tail 분기 아닌 **평형 peak 분기**로 떨어짐. C-rate 변화가 finite-rate 꼬리 아니라 거의 ±I·Rn ohmic shift만(Rn=0이면 I 무관 동일). 문건·graph suite가 강조한 비대칭 꼬리 broadening이 디폴트서 미활성. [C2]

## 클러스터 C — 논리 점핑·왜곡 (유도) [CRIT-HIGH, S3·S2]
- **C1** `peak_shape=(ξ_eq−ξ_lag)/L_V → dξ_eq/dV` 극한 수렴 수학 비약(Taylor/convolution 커널 극한 미제시). [S3-02]
- **C2** Maxwell 등면적 적분 단계 없이 `ΔU_hys=(2/F)[Ωu−2RT·artanh u]` 결과만. [S3-03]
- **C3** 두-상 w 예외가 N4→N5→N6 흐름에 인과연결 없이 "이중지위 선언"만 → G-follow 불가. [S3-01·S2 I-02]
- **★C4 왜곡**: 충전 꼬리 방향 — 본문(Ch1 L1609-1610) "V 큰 쪽으로 늘어진다"(오) vs 캡션(L1640-41) "낮은 V 쪽"(정) **모순**. 코드·self-test는 낮은 V(정)와 일치 → 본문 1문장이 반대. 부호검산 S7이 이 모순 통과. [S3-04·C2] — 실 결함.
- **C5** 편미분 유도 비약(Ch2). [S2 I-02]

## 클러스터 D — LCO/전자 placeholder [MED, doc-labeled]
- **D1** LCO 전자항 `x_MIT=0.50`·`x_center=0.50`(중간 전이 3.880V)인데 Ch1 물리 anchor는 x_MIT≈0.85·MIT=T1(3.90V). 배정 위치 구조 불일치. [C1·O3·C3]
- **D2** LCO T3(4.17-4.20V) 코드 부재 → 실행 dQ/dV 2 peak(3.92·4.04)만, 문건 3-transition 미재현. [C1·C3]
- **D3** T_ref=298.15 동결 → Sommerfeld ΔS_e∝T·eq:U1T2 T² 곡률 미구현. [O3·C1·S3-05·S2 I-09]
- **FP?**: 전부 FITTING_GUIDE Phase D·tier-C로 라벨됨 → "알려진 미완성". 10차: "계획된 후속"이지 결함 아님인가, 아니면 release baseline 부적격인가.

## 클러스터 E — 코드 robustness [MED]
- **E1** `irreversible_heat`가 q_irr≥0 무가드 → 음수 반환 실측(U_oc<V일 때). [O2 MED-5]
- **E2** `entropy_coefficient`가 전하보존 음함수(eq:implicit) 안 풀고 V축 직접 가중. **FP?** O2 자기표시 오적발 위험 중간. [O2 MED-4]
- **E3** 히스 분기 비대칭 미구현 / Ω=13000 hys gap 102.8mV 과대(γ=0이라 비활성). **FP?** γ=0 비활성이면 실害 없음. [S2 I-04·O2 MED-6]

## 클러스터 F — FITTING_GUIDE [HIGH-MED, C3·C1]
- **F1** guide Ω 하한 `>2RT`가 Ch1 solid-solution 기대(dilute→stage4·4L↔3L은 Ω<2RT)와 **충돌** → 피팅 단계서 전이별 물리 구분 봉쇄. [C3 HIGH]
- **F2** v5의 master algorithm(L1518-85)·실무 피팅 절차(L1590-1615)·hold-out 진단표(L1640-85)가 46줄 FITTING_GUIDE로 **미보존** → G-usable 실무 절차 약화. [C1 cross-version]

## 클러스터 G — 검증 artifact [LOW-MED, 대체로 FP]
- **G1** `test_regression_graphite.py`·graph suite V9가 면적 ratio 0.936/0.979 출력하며 PASS → "면적=Q assert" 명칭과 실제 gate(golden bit-exact) 불일치. **★FP 확정**: 면적 물리는 정상(넓은 window 0.9999·개별 전이 0.99988), 0.936/0.979는 **grid 절단 artifact**(O3·C1·C2·C3 공통). 결함은 물리 아닌 "검증 표시 오도". [C2·C1·C3·O3]
- **G2** P5 그래프 PNG 한글 글리프 깨짐 → 시각 판독성 저하. [C3]

## 클러스터 H — cross-version 손실 [HIGH-MED]
- **H1** v3/v4의 입자-장벽 분포형(ρ_G·superposition ∫ρ_G·exp(...)dG·σ_lnL=σ_G/RT·δ-극한 환원)이 v1.0.10 코드 forward에 미구현. **부분 반박**: Ch1 L1289-1351이 forward·역산금지·PSD배제는 복원 → "문구 삭제"보다 "경고는 남았으나 코드/디폴트가 검증가능 형태로 미구현". [S1 HIGH-3·C3]
- **H2** v4 isotherm-slope 단상(Ω<2RT) narrowing 정량화가 v1.0.10 tex에 흔적 0 → 단상 폭 예측 정밀도 손실. [O1]
- **H3** v5 실무 피팅 절차/hold-out(=F2). [C1]
- **정당 컷(누락 아님)**: use_w_eff/w_eff(Ω)=w(1−Ω/2RT) 제거 = Ω>2RT서 음수폭 버그·실측 반대방향 → 정정. [전원 합의]

## 무결 확인 (PASS — 보고서 "문제 아님" 절)
면적보존 물리(0.9999) · q_rev T¹(T² 없음) · 전자엔트로피 골 −45.68=Ch1 −46 · LCO seam 3경로·MIT 부호 · func_dU_hys 공식 · radius/PSD 배제·역산금지 정당(radius verdict 독립 타당) · use_w_eff 제거 정당 · PDF 렌더(대형 깨짐 없음).

## 10차 재검 쟁점 (진짜 문제 vs 오적발)
1. **클러스터 A 핵심**: 미피팅 placeholder인가 **구조 결함**인가(폭 모델이 두-상 near-delta 구조적 불가). ★최우선.
2. **클러스터 D**: doc-labeled "계획된 후속" → 결함 강등? release baseline 부적격은 유지?
3. **G1**: 면적 = FP 확정(물리 정상, 표시 오도만).
4. **E2·E3**: 오적발 위험(음함수 근사 타당성·γ=0 비활성).
5. **C4·F1**: 실 결함 확정 후보(본문-캡션 모순·guide-이론 충돌).
6. **H1**: "경고 복원됨" 반박 반영 — 문구 손실 아닌 구현 손실로 재분류.
