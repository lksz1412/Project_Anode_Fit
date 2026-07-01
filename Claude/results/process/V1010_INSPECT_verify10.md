# v1.0.10 문제검수 — 10차 재검 (진짜 문제 확정·오적발 필터) 결과

> union(클러스터 A-H) 각 문제를 별세션 Opus가 **코드 직접 실행**(numpy 2.4.3, 원본 무수정 import, 6 스크립트) + tex 줄 대조 + adversarial agent 2대 삼각검증으로 진짜/강등/오적발 3분류. 사용자 예측대로 오적발 다수 적발.

## ① 확정 진짜 문제 (v1.0.11 대상)
- **[CRIT] 클러스터 A — 폭 모델 구조 결함**: 단일전이 FWHM=90.570mV, Ω=0/6000/13000/50000 전부 동일(폭이 Ω 무시), 4-staging equilibrium peak 1개(V=100.3mV). ★구조 결함 확정: 두-상 near-delta(FWHM~mV)는 n≈0.10 sub-thermal 폭 요구 = 단일자리 regular-solution logistic이 물리적 정당화 불가 → 코드가 두-상 개형을 **열역학으로 생성 불가**. placeholder 방어 초과. 면적·위치·온도의존은 정상(결함은 "폭의 물리 기원"에 국한).
- **[HIGH] B1 — kinetic 꼬리 default OFF**: L_V(9.8e-9…4.7e-9) ≤ 격자문턱(3.94e-4)의 0.00125배 → tail 분기 미진입. Rn=0서 C-rate 무관 곡선 동일, Rn=0.01서 split=순수 ohmic ±I·Rn. 비대칭 꼬리 broadening 디폴트 비활성.
- **[HIGH] C4 — 충전 꼬리 방향 본문↔캡션 모순**: 실측 완벽 mirror(방전 +20.9mV/HIGHER, 충전 −20.9mV/LOWER). 캡션(b)·코드·self-test 정(LOWER), Ch1 본문 L1609-10 "V 큰 쪽"만 반대. 부호검산 S7 통과. 고립 1문장 오기.
- **[HIGH] F1 — FITTING_GUIDE Ω 하한 vs solid-solution 충돌**: guide L13 "Ω>2RT" 하한이 Ch1 L738-739 "dilute→stage4·4L↔3L은 Ω<2RT 기대"와 정면 충돌 → 전이별 구분 봉쇄.
- **[MED] H2 — v4 단상 narrowing prose 손실**: `w_eff=(RT/F)(1−Ω/2RT)`(Ω<2RT 단상 평형 예측)가 v1.0.10 tex 흔적 0. 코드 use_w_eff 제거는 정당 버그픽스(orthogonal), 단 prose 예측 정밀도 손실(각주 복원, 코드 미개입).
- **[MED] E1 — irreversible_heat q_irr≥0 무가드**: U_oc<V·I>0서 −0.02 반환. Ch2 eq:qrev는 q_irr≥0 boxed. docstring "caller 책임" 있음.

## ② 강등 (알려진 미완/계획된 후속 — 결함 아님, v1.0.11 이월)
- **클러스터 D 전부**(D1 x_MIT=0.50·D2 T3 부재·D3 T_ref 동결→T² 미구현): Ch1 L325-327·FITTING_GUIDE Phase D가 tier-C·후속으로 명문 라벨. 결함 아님. 단 그래프 placeholder 워터마크 권고.
- **H1**(ρ_G 분포형): v1.0.10 ρ(U_app)는 정정된 재유도(δ-극한·forward·역산금지·ill-posed 경고 전부 생존, Ch1 L1275-1338). 문구·구현 손실 아님. 이월 불요. (union "구현손실 재분류"는 과함.)
- **A2**(per-transition 'w' silent 무시): 클러스터 A 하위 증상, 코드 주석 명시, 독립 결함 아님.

## ③ 오적발 (판단오류·문제 아님·무조치)
- **[FP] G1 (면적)**: wide window[-1,2] ratio=**1.000000**·단일전이=0.50000000 실측. 0.936/0.979는 순수 grid 절단 artifact. 물리 완전 정상. ("면적=Q assert" 명칭↔gate 불일치는 별개 minor 문서.)
- **[FP] E2 (entropy_coefficient 음함수)**: implicit solve는 x축 relabeling뿐, dU/dT(V) 동치(matched V서 max|diff|=0.00e+00). 물리 동치.
- **[FP] E3 (히스 γ=0)**: 디폴트 γ=0이라 히스 완전 비활성(diff 3.4e-15), 공식 무결. release 무해.
- **[FP] S3-08 (z_cut=4.357)**: z_cut=logistic 도함수 5% 하락점(정밀 4.35654). S3 4.394 산술 오류. 자기정합.
- **[FP] 논리점핑 C1·C2·C3·C5·S3-07 전부**: 별세션 정독 — C1 0/0 극한 명시(L1573-79)·C2 유도는 Maxwell 아닌 spinodal 양끝(artanh L604-618)·C3 이중지위 삽입점 선언+§(a) 정당화·C5 "셋째 항" 자체 부재(검수자 지어냄)·S3-07 μ-link eq:eqcond 참조 존재. **진짜 유도 비약 0건**. 졸업생 독자 무보조 추종.
- **[PASS] q_rev T¹**(q/(−I·dU/dT)=298.15)·**전자엔트로피 골 −45.678**(Ch1 −46)·**seam·MSMR 부호**·func_dU_hys 공식·PDF 렌더 — 무결 재확정.
- 기타 저위: G2(글리프 깨짐)=물리 무관 시각 품질·I-05·부호규약=Ch2 명시로 대체로 FP.

## ⑤ 클러스터 A 구조결함 최종 결론
**구조 결함 확정.** w=nRT/F에서 두-상 near-delta 산출은 n≈0.10 sub-thermal 폭 요구(비물리). 코드는 near-delta+broadening 2층 구조 부재 → 두-상 평형 개형 구조적 생성 불가·Ω를 폭 채널 전혀 미반영. "미피팅 placeholder"는 표층, 근저는 모델 구조 한계.

## 핵심 한 줄
union 진짜 CRIT = **클러스터 A(폭 구조 결함) 단 하나** + 파생(B1). 논리점핑 6·G1·E2·E3·S3-08·H1 = **오적발**(검수자 과민·산술오류·물리동치 미인지). 클러스터 D = doc-labeled 강등. C4·F1·H2·E1 = 저비용 실 결함. 9종 다수 지적이 한 뿌리(A=코드-문건 계약 파기)로 수렴, 오적발 비율 상당 → 재검 실효.
