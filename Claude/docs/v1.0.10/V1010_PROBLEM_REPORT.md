# Anode_Fit v1.0.10 — 문제점 대검수 보고 문건 (v1.0.10 마무리)

> ★★★ **[정정 배너 — R1 철회]** 본 문건 §0·§1의 **R1 "폭 모델 구조 결함(near-delta 생성 불가, CRIT)"은 이후 인계 무결성 대검수(9종+10차, 기록 SPEC 대조 + 코드 직접 실행)에서 오판으로 확정·철회**됐다. bell/4전이 병합은 **의도된 apparent-U/η 물리**(폭을 좁히면 n=0.1→4 staging near-delta 완전분리·v11_final byte 동일·회귀 아님)이며, 두-상 w는 SPEC 명시 현상학적 자유 피팅폭이다. **"near-delta+broadening 2층 재설계"는 위험**(복원된 broadening 물리 붕괴). 유효 결론은 `V1010_HANDOVER_INTEGRITY_REPORT.md` + `HANDOVER_v1.0.11.md`(rev.2)를 따르라. 아래 §1 R1은 SUPERSEDED. ★★★
>
> 9종 절별 루핑 검수(3S·3O·3C, 각 그래프 직접 실행·개형 실측) → 단점 union → 10차 재검(코드 직접 실행·물리 재검산·오적발 필터). 이 검수가 v1.0.10의 마지막 단계. 개정은 v1.0.11 핸드오버(`HANDOVER_v1.0.11.md`). **v1.0.10 코드/문건 자체는 이 검수로 수정하지 않음(진단·동결).**
> 원자료: `../../results/process/V1010_INSPECT_draft_{S1-3,O1-3,C1-3}.md` · `V1010_INSPECT_UNION.md` · `V1010_INSPECT_verify10.md`.

## 0. 요지 (한 문단)
P1-P5 검수는 **코드↔문건 내부 정합**만 봐서 **실제 출력 그래프 개형의 물리 오류**를 놓쳤다. 근본 문제는 **단 하나의 뿌리** — 흑연 dQ/dV 폭 모델이 두-상(1차) staging 전이에 단일자리 Nernstian 폭 `w=nRT/F`를 보편 적용해 4 staging 전이가 뭉갠 단일 bell로 병합된다(구조 결함). 9종이 union으로 모은 다수 지적은 이 뿌리로 수렴하며, **오적발 비율이 상당**(유도 비약 6건·면적 3건 전부 오적발)해 10차 재검이 실효했다.

## 1. 확정 진짜 문제 (v1.0.11 개정 대상, 우선순위 순)

### [CRIT] R1 — 폭 모델 구조 결함 (두-상 near-delta 생성 불가·4 staging 병합)
- **증상(실측)**: 단일 전이 FWHM=90.57mV(=3.525·w, w=RT/F=25.69mV). 4 전이 중심(210·140·120·85mV) 간격(71/20/35mV) < FWHM → 평형 dQ/dV local max **1개**(V=100.3mV). 커밋 그래프 3종·회귀 golden 모두 단봉. Ω=0/6000/13000/50000 무관 폭 동일 → **폭이 상분리(Ω) 완전 무시**.
- **물리 근거(구조 결함 확정)**: 흑연 4 전이 전부 Ω>2RT(1.2-2.6배, 1차 두-상). Maxwell 공통접선상 두-상 평형 dQ/dV는 near-delta(spike). 이를 내려면 w≈2.6mV → **n≈0.10(sub-thermal 폭)** 필요 = 단일자리 regular-solution logistic이 물리적으로 정당화 불가(w<RT/F는 열보다 좁은 폭 = 비물리). 곧 **코드가 두-상 평형 개형을 열역학으로부터 생성 못 함** — near-delta+broadening 2층 구조 부재.
- **"placeholder라 OK" 방어**: 부분만 성립. Ch1 L736-743이 tier-C·`n` 우선·`w` 폴백 inert를 명시(은닉 아님)하나, 미피팅 문제가 아니라 **모델 구조가 두-상 개형을 담지 못함**이 근저. 디폴트 release 그래프가 물리 오형상을 baseline으로 제시하는 것도 별개 유지.
- **파생**: (a) per-transition `'w'`(20/16/14/12mV)이 `'n':1.0` 우선으로 silent 무시(A2, 하위 증상) (b) 폭이 kinetic·이질성 아닌 열역학 nRT/F에 앵커.
- 위치: `Anode_Fit_v1.0.10.py` `_width` L303-306·`_n_factor` L294-300·`GRAPHITE_STAGING_LIT` L680-709 · `graphite_ica_ch1_v1.0.10.tex` §width L729-743·broadening 절.

### [HIGH] R2 — kinetic 꼬리 default OFF (C-rate 그래프 = ohmic shift만)
- 실측: 디폴트 L_V(9.8e-9…4.7e-9) ≤ 작업격자 문턱(3.94e-4)의 0.00125배 → `dqdv`가 tail 분기 미진입, 평형 peak 분기로 떨어짐. Rn=0서 C-rate 0.0001-1.0 곡선 동일(꼬리 무영향), Rn=0.01서 split=순수 ±I·Rn(ohmic). 문건·graph suite가 강조한 비대칭 finite-rate 꼬리 broadening이 디폴트서 비활성. dVdq_qa=0.30 출고인데도 sub-grid.
- 위치: `dqdv` L392-502·`_resolve_lag_length` · graph_suite_p5.py.

### [HIGH] R3 — 충전 꼬리 방향 본문↔캡션 모순 (왜곡, 저비용)
- Ch1 본문 L1609-10 "충전에서는 V가 큰 쪽으로 늘어진다"(오) vs 캡션(b) L1640-41 "낮은 V 쪽"(정). 실측 완벽 mirror(방전 skew +20.9mV/HIGHER, 충전 −20.9mV/LOWER) → 캡션·코드·self-test가 정, 본문 1문장이 반대. 부호검산 S7이 이 모순 통과.

### [HIGH] R4 — FITTING_GUIDE Ω 하한 vs solid-solution 충돌
- FITTING_GUIDE L13 tier-2 Ω 하한 "Ω>2RT(≈4958)"·제약 "Ω>2RT(spinodal)"가 Ch1 L738-739 "dilute→stage4·4L↔3L은 Ω<2RT로 피팅 기대"와 정면 충돌. guide를 따르면 첫 두 전이를 단상으로 못 보내 문건이 회복하려는 전이별 구분을 알고리즘이 봉쇄.

### [MED] R5 — v4 단상 narrowing 유도 prose 손실 (cross-version)
- v4 `w_eff=(RT/F)(1−Ω/2RT)`(isoslope 매칭, Ω<2RT 단상의 검증가능 평형 예측)가 v1.0.10 tex 흔적 0. 코드 `use_w_eff` 제거는 정당 버그픽스(Ω>2RT서 음수폭, orthogonal)이나, **단상 폭 Ω-narrowing prose 예측이 사라짐**(v1.0.10은 단상 w=nRT/F flat 단언). 각주 복원(코드 미개입).

### [MED] R6 — irreversible_heat q_irr≥0 무가드
- `I·(U_oc−V)` bare lumped, U_oc<V·I>0서 −0.02 반환. Ch2 eq:qrev L643 q_irr≥0 boxed·L648 "2법칙상 항상 발열". docstring "caller 책임" 있으나 부호 가드 또는 계약 강화 권고.

### [문서 minor] R7 — 검증 표시·시각 품질
- `test_regression_graphite.py`·V9의 "면적=Q assert" 명칭이 실제 gate(golden bit-exact)와 불일치(면적 ratio 0.936/0.979 출력만) → 명칭↔gate 정합. P5 그래프 PNG 한글 글리프 깨짐 → 폰트.

## 2. 강등 (알려진 미완/계획된 후속 — 결함 아님, v1.0.11 이월만)
- **클러스터 D (LCO placeholder)**: D1(x_MIT=0.50 배정)·D2(T3 4.17-4.20 부재, 실측 2 peak)·D3(T_ref 동결→Sommerfeld ∝T·T² 곡률 미구현). Ch1 L325-327·FITTING_GUIDE Phase D가 tier-C·후속으로 명문 라벨 → 결함 아님. 단 그래프에 placeholder 표기 권고.
- **H1 (ρ_G 분포형)**: v1.0.10 ρ(U_app)는 정정된 재유도(δ-극한·forward-only·역산금지·ill-posed 경고 전부 생존, Ch1 L1275-1338). 문구·구현 손실 아님 — 이월 불요.

## 3. 오적발 (판단오류·문제 아님 — v1.0.11이 쫓지 말 것)
> 사용자 예측대로 9종이 판단오류로 문제 지목한 케이스. 10차 재검이 코드 실행·정독으로 기각.
- **[FP] 면적 (G1)**: wide window[-1,2] ratio=**1.000000**·단일전이=0.50000000 실측. 0.936/0.979는 grid 절단 artifact. 물리 완전 정상.
- **[FP] 논리 점핑 6건 (C1·C2·C3·C5·S3-02·S3-07)**: 인용 줄 정독 결과 유도 단계 실재 — 0/0 극한 명시·spinodal 양끝(Maxwell 아님)·이중지위 삽입점 선언·**C5는 없는 "셋째 항"을 지어냄**·μ-link eq:eqcond 참조. **진짜 유도 비약 0건**, 졸업생 독자 무보조 추종.
- **[FP] entropy_coefficient 음함수 (E2)**: implicit solve는 x축 relabeling뿐, dU/dT(V) 동치(max|diff|=0.00e+00).
- **[FP] 히스 γ=0 (E3)**: 디폴트 γ=0 완전 비활성(diff 3.4e-15), 공식 무결.
- **[FP] z_cut=4.357 (S3-08)**: logistic 도함수 5% 하락점(정밀 4.35654), 검수자 산술 오류.
- **[PASS 재확정]**: q_rev T¹·전자엔트로피 골 −45.68(Ch1 −46)·LCO seam·MSMR 부호·func_dU_hys·PDF 렌더·radius 배제·use_w_eff 제거 정당.

## 4. 결론
- v1.0.10의 **유일한 CRIT = R1(폭 구조 결함)** + 파생 R2. C4/F1/H2/E1(R3-R6)은 저비용 실 결함. 나머지 다수는 오적발(과민·산술오류·물리동치 미인지) 또는 doc-labeled 강등.
- **radius 연구는 회의적 참조로만** 사용 — verdict의 "마이크론 반경→U_j 무의미"는 독립 타당하나 폭 문제의 확정 원인 아님(폭 병합은 코드 실행으로 독립 확인). radius 배제·역산금지는 정당.
- v1.0.10은 이 진단으로 마무리. 개정 = `HANDOVER_v1.0.11.md`.
