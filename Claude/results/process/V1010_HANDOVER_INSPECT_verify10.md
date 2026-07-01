# v1.0.10 인계 무결성 — 10차 재검 (R1 오판 반전·진짜결함 확정) 결과

> union 각 항목을 별세션 Opus가 **v1.0.10·v11_final 코드 직접 실행**(numpy 2.4.3, r1_test.py) + SPEC 기록(6-30 핸드오버·broadening_w_design)·tex 실측으로 재검. 파일 수정 0.

## ① ★R1 오판 반전 확정 (내 이전 V1010_PROBLEM_REPORT·HANDOVER_v1.0.11이 오판)
- **직접 실행**: 현상학적 폭 축소 → 병합 bell이 **분리 near-delta 다봉으로 갈라짐**. n=1.0(25.7mV)→local max 1 · n=0.5→2 · n=0.2→3 · **n=0.1(2.57mV)→4개 완전분리**. live 'w'=5mV도 4개. → **모델은 near-delta·다봉 생성 가능. 단일 bell = 기본값 n=1.0의 결과, "생성 불가 구조결함" 아님.**
- 폭 Ω-무관 = SPEC 명시 설계(두-상 폭=평형예측 아닌 현상학적 자유 피팅폭, Ω 반영 의무 없음). 결함 아님.
- v1.0.10 vs v11_final max_abs_diff=**0.000e+00**(bell v11_final부터 동일·회귀 아님)·wide-window 면적=**0.970000**=ΣQ(보존).
- 물리 재검: R1 "near-delta는 n≈0.10 sub-thermal=비물리" 반론은 w를 단일자리 평형예측으로 볼 때만 성립. 두-상 w=현상학적 피팅폭(broadening_w_design §1b·Ch1 L1304-07). 문서 L1255-57이 선제 반박("RT/F는 n=1 척도, 하한 아님").
- **★v1.0.11 "near-delta+broadening 2층 재설계" 위험 高**: 문서가 **이미** 그 2층을 서술(L1259-1297·keybox L1341-52·fig:broadening 패널b: 평형 near-delta 파선→측정 bell 실선)하되 코드차원 0 단일 w에 흡수(L1334-38 PSD/다입자 convolution 명시 금지). v1.0.11이 실제 convolution 구현 시 SPEC(D3)·6-30·Ch1 (c)(iii)가 ill-posed·forward-only로 배제한 ρ(U_app)/PSD 역산 부활 → **복원 broadening 물리 붕괴**.
- **bell 권고**: 정상 물리 → 유지(재설계 금지). 실개선 = default 표시(n=1이 4 staging 미표시 → 기본 initial-value 분리폭 조정 or 릴리스 그래프 "n=1 초기값·w 제거 시 분리" 라벨). G-usable 개선일 뿐 모델 변경 아님.

## ② H-3 ρ_G — 강등(모델 scope-out 의도) + 잔여 MED(진단 prose)
- 모델 차원(ρ_G/PSD 기계장치 부재) = 6-30 [과제 MODEL-1, 선택]·broadening_w_design("다입자/ρ_G 모델 안 가져옴·설명만 복원") **의도 컷 확정**(grep: ρ_G/σ_G/stretched는 헤더 L46 1줄만).
- 잔여 = v5의 σ_G/RT stretched-tail **온도의존 진단 prose**("반로그 꼬리 처짐→ρ_G 넓음") 미대체 = 교과서 진단 안내 얇아짐(모델 손실 아님). **판정: 강등 + MED 진단-prose 이월(모델 복원 X, "후속 kinetic-barrier 장 소관" 예고로만)**.

## ③ H-1~H-8 판정
| ID | 판정 | 등급 |
|---|---|---|
| H-1 byte-identical claim stale | 진짜(기록오류) | MED |
| H-2 버전라벨 stale(Ch1 v9·Ch2 v5, PDF header/meta) | 진짜(user-visible) | MED |
| H-3 ρ_G 진단 | 강등+잔여 | MED |
| H-4 전자항 magnitude trail(forward-ref 없음) | 진짜(약함) | LOW |
| H-5 코드헤더 w^eff 잔재 | 진짜(경미) | LOW |
| H-6 A3-1 overfull | 미검증(LaTeX 부재) | LOW |
| H-7 Ch1§broadening↔Ch2파생C 위임 | 진짜(제약) | 제약 |
| H-8 LCO placeholder | 강등(라벨됨·Phase 4.1) | 강등 |

**오적발 확정(v1.0.11 쫓지 말 것)**: bell/병합(의도·v11_final부터)·면적 ratio 0.936(grid-truncation, wide=1.000000)·use_w_eff 제거(회귀0·byte동일)·radius 배제·Ch2 w_eff supersession·논리점핑 6·E2/E3/z_cut.

## ④ 확정 실 인계결함(v1.0.11 이월·전부 minor)
MED: H-1 byte 기록정정·H-2 버전라벨·H-3 진단prose 예고 / 제약: H-7 동반개정 / LOW: H-4 forward-ref·H-5 주석잔재·H-6 overfull 재확인 / 강등: H-8 placeholder 경고강화.

## ⑤ v1.0.11이 R1 대신 담을 것 (물리 재설계 X)
1. **R1 철회·재framing**: "구조결함 CRIT"·"2층 재설계" 삭제. bell=의도 물리, 병합=default n=1 표시문제. Non-goals에 "broadening 물리 재설계·ρ(U_app)/PSD convolution 구현 금지".
2. minor 정합(④).
3. H-3: 모델 복원 X, stretched-tail 진단만 "후속장 예고" prose.
4. default 사용성: 기본 initial-value 4 staging 분리 or 릴리스 그래프 라벨(모델 불변)·kinetic 꼬리 default OFF 정직 라벨.
5. radius/w_eff/역산금지 계승 유지.

## ⑥ 가장 약한 1곳
H-3 진단-prose 등급 경계. 모델 scope-out 의도는 확정이나 진단 prose 이월 여부는 SPEC 미판정(C1만 HIGH). 안전 처리 = MED 이월하되 "후속장 예고 prose"로 한정 — "진단 복원"이 "모델 복원"으로 미끄러지면 ①의 붕괴 위험과 합류하므로 경계 명문화.
