# Phase Result — Ch1 v10 (v9 정정·broadening 복원·w_eff 제거) [P5 완료]

> plan = `plans/2026-06-30-rework-broadening-restore-weff-fix-reorg-plan.md`. 9종 competition-cherrypick. 최종 = `docs/Ch1_v10/graphite_ica_ch1_v10.tex`(34p).

## 1. 목표·달성
현 Ch1 v9 를 정정·업데이트 → v10: ★v8/v9 가 덜어낸 **종모양 broadening 설명 복원** + **w 이중지위** + **w_eff 제거**, 기존 LCO 전자엔트로피·분포 보존.

## 2. broadening 절 (신규, 사용자 2차 명확화 반영)
- **전이별**: dilute·4L↔3L = solid-solution(이미 종) / **LiC₁₂·LiC₆ 2개만 two-phase**(코드 Ω 초기값 전부>2RT=거친 추정·피팅 시 갈림).
- **3기작**: ① 단일입자 유한율속 비대칭 꼬리(L_V·skew) ② 내재 RT/F 폭 ③ ★**집합 다입자 통계역학**: (iii-a) Dreyer 평형 통계역학 = plateau 구조(앙상블 순차전환) + (iii-b) plateau→실측 종 = **apparent-U=U_j+η 앙상블 분포**(★U_j 중심=입자 무관 상수·분포는 η=과전압·국소환경, **비-크기**). forward 통계평균 eq:ensavg ∫ρ(U_app)·단일응답 dU_app·ρ→δ 환원·역산 X.
- → ★**w_j(두-상)=현상학적 자유 피팅 폭**(평형 예측 아님).
- ★**사이즈 효과 전면 제외**(사용자 명시): τ∝r²·반경→U_j·PSD 크기 convolution = 배제 경고만(유도·인용 0). 집합 통계역학은 *비-크기* 전이전위·η 분포로만.

## 3. w 이중지위 + w_eff 제거
- 단상 Ω<2RT = nRT/F 검증가능 평형 예측 / 두-상 = 현상학적 자유 피팅 폭(코드 use_w_eff=False 정합).
- w_eff(Ω)→델타 narrowing 절·식·코드참조 **완전 제거**(본문 잔존 0, 헤더 changelog inert만).

## 4. 방법·품질 (competition-cherrypick)
- 9종 빌드 → 검토1(R1 broadening·R2 w_eff/보존·R3 인용) → 체리픽 v10-10(base v10-06 + 기작3 신규저작·calibration 정정) → adversarial(A1 기작③ CRIT·A2 견고·A3 fig orphan) → finalizer v10-11(정정·10회 수렴).
- ★품질: 전자엔트로피 절 **byte-identical**(SHA 687ba7e6·9종 검증)·w_eff 본문 0·사이즈 cite 0·Ω/two-phase 2개·xelatex 0-error·34p·fabrication 0.

## 5. ★경쟁+adversarial 적발 (method value)
- 빌드: size featured(01/04) vs 절제(03/05/06) split → 사용자 명확화로 *제거* 확정.
- adversarial A1: ★기작③ ρ(U_j) "중심 분포" ↔ "중심 상수" **자기모순(CRIT)** 적발 → ρ(U_app=U_j+η)·중심 상수·분포 η 로 재정초(ORIGIN 정합).
- ★radius 조사 인용(fly2020·rsc2021) 자체가 ORIGIN 서술과 실제 논문 불일치 — finalizer Crossref 증거우선 교정·tier 정직(★박사님 확인 항목).

## 6. 잔여(확인 요)
- fly2020(10.1016/j.est.2020.101329 = A.Fly·R.Chen)·rsc2021(Onuma, K-graphite) — ORIGIN 의도 인용과 다를 가능성(증거우선 교정함).
- 집합 통계역학③ LCO 적용 = 일반 η 분포(tier-C 가정 명기).

## 7. 산출
- 최종: `docs/Ch1_v10/graphite_ica_ch1_v10.tex`(+pdf, 34p).
- 빌드: `results/builds/ch1v10/v10-01..11/`·`v10-00_spine/`·`review1/`·`review2/`. 설계: `results/research/broadening_w_design.md`.
