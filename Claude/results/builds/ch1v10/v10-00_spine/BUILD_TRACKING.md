# Ch1 v10 — 빌드 추적 (컴팩션-안전)

> v10 = v9 정정·통합(broadening 복원 + w 이중지위 + w_eff 제거 + 기존 LCO/분포 보존). base=v9(1644줄). Claude=알림 / Codex=폴링.

| 작가 | 모델 | job-id |
|---|---|---|
| v10-01 | Sonnet | aa4ffc955ce80162c |
| v10-02 | Sonnet | a5c772e102423da0e |
| v10-03 | Sonnet | a567fa5155ba27b03 |
| v10-04 | Opus | a9b6b5b7a89e90cd6 |
| v10-05 | Opus | a65379dcddff7f145 |
| v10-06 | Opus | ae779eaa8b2800a0f |
| v10-07 | Codex | task-mr0qcg7x-s50ads |
| v10-08 | Codex | task-mr0qcw0x-ehda1a |
| v10-09 | Codex | task-mr0qcxw1-b35hen |

## 핵심 검토 렌즈 (검토1·adversarial)
★broadening 전이별 정합·현상학적 w·**다입자/PSD 모델 0**(설명만)·forward-only·ill-posed·반경=평형U 무효·apparent-U=U_j+η · w 이중지위 · **w_eff 잔존 0** · 기존 LCO/전자엔트로피/분포 보존 · G-derive·부호.

## ★검토 calibration (빌드 중 포착)
- **size/PSD kinetic 분산(τ∝r²) 절제 수위**: v10-01 이 이를 *named mechanism* 으로 포함. 사용자가 radius/size 각도를 "의미없음"으로 평가 → 체리픽서 size 분산은 **현상학적 w 흡수 수준 언급**(featured mechanism·모델 X)으로 절제할지 calibrate. 핵심(L_V 단일입자 꼬리 + 내재 RT/F → 현상학적 w)은 유지. 작가별 수위 비교.

## 빌드 결과
- v10-01(S): 32p·broadening·w 이중지위·w_eff 제거(3곳·경고·코드토글 잔존)·다입자 모델 0·기존 보존·0-err. ★size/PSD를 *featured mechanism*으로 포함(과다·calibrate).
- v10-02(S): 32p·broadening(기작 L_V+내재)·w 이중지위·w_eff 텍스트 제거(코드토글 잔존)·다입자 0·기존 보존·0-err. size B-ii 가볍게.
- v10-03(S): 32p·broadening(기작 2개 L_V+내재, **size 미featured**)·w 이중지위·★**w_eff 완전 제거**(eq:weff·use_w_eff·func_w_eff 텍스트 전부, 잔존 0)·다입자 0·기존 보존·0-err. → **사용자 의도 최적합**(w_eff 제거·size 절제).
- v10-06(O): ★**강력** 33p — 기작 L_V+내재 RT/F(현상학적 w, **다입자 긍정항 0**·size 미featured)·w_eff **완전 제거**(body 0)·w 이중지위(Ω 수치검증 6000-13000>4958)·범위경고 3중·기존 보존(preservation agent)·그림 추가·0-err. (sub 3 spawn=경미 일탈, 산출 강함.) flag: park2021 맥락.
- v10-05(O): 강력 33p — broadening+fig·w 이중지위(sec:wdual)·w_eff 완전제거(라벨 set-diff 검증 잔존 0)·다입자 0·기존 91/92 byte-identical·0-err. ★**Ω/two-phase 일관성 결함 적발·재정합**.
- ★★**Ω/two-phase 일관성 (체리픽 필수)**: w 이중지위 "두-상=staging 4전이 전부"(코드 Ω 초기값 전부>2RT) vs per-transition "4L-3L=solid-solution(단상)" **모순**. **정답 = two-phase는 LiC₁₂(2L→2)·LiC₆(2→1) 2개만**, dilute·4L-3L은 solid-solution(피팅 시 Ω<2RT). 코드 Ω 초기값(전부>2RT)은 *거친 추정*으로 명시. (내 design doc 도 동일 긴장 — 체리픽서 통일.)
- ★calibration 결론: 기작 = L_V 단일입자 꼬리 + 내재 RT/F(현상학적 w), **size/PSD 절제**, w_eff **완전 제거**, ★**two-phase=2개(LiC₁₂·LiC₆)로 통일**. → **base 3강 = v10-03·v10-05·v10-06**(절제·완전제거; v10-05·06 가 Ω 일관성 처리).

- v10-07·08·09(Codex): lean(~1670줄, +25-30) — broadening 마커 14-16·**w_eff 잔존 0**·다입자=경고문맥. PDF·내용 OK(companion result fetch 실패=job registry, 산출물 정상). 짧지만 핵심 보유.
- v10-04(Opus): ✅ 33p — 기작 **3개**(size kinetic τ∝r² "주범" 복원·모델 안 함)·w_eff 완전제거·w 이중지위·다입자 모델 0·기존 보존(3 검수 agent)·0-err. ★size featured(v10-01과 동류).

## ★기작 수위 split (체리픽 calibration 결정)
- **size featured**(3 기작, τ∝r² 명시): v10-01·v10-04.
- **size 절제**(2 기작 L_V+내재, size 흡수): v10-03·v10-05·v10-06.
- ★**결정 = 절제 채택**(사용자 "다입자 빼·radius 의미없음"). size kinetic 분산은 *현상학적 w 흡수·1문장 언급·모델/추출 X(ill-posed)*로. 핵심 기작 = L_V 단일입자 꼬리 + 내재 RT/F.
- ★two-phase = LiC₁₂·LiC₆ 2개로 통일(코드 Ω 초기값 전부>2RT=거친 추정). w_eff 완전제거.
- **base = v10-06**(polish·preservation·Ω 수치검증) + v10-05(Ω 재정합·라벨 검증) graft.

## ★★사용자 2차 명확화 (calibration 재정정 — 빌드 후)
- "다입자 = 파티클 *사이즈* 효과 빼라"(τ∝r²·반경·PSD 크기분산 전부 제외).
- "입자 여럿의 집합적 *통계역학*은 반영돼야"(앙상블 ρ(U_j) 전이전위 분포 = 비-크기 heterogeneity·구조무질서·Dahn1995·Dreyer 다입자). → forward 통계평균만.
- ★**기작 3 = 집합 다입자 통계역학(비-크기)** = 사용자 요구. broadening = L_V 율속꼬리 + 내재 RT/F + **집합 통계역학(ρ(U_j), 비-크기)**. 사이즈 동역학만 제외.
- ★**9종 모두 결여**: 강한 초안(05/06/03)은 size 빼며 2기작만(집합 통계역학 없음). featured 초안(01/04)은 *사이즈* 다입자(틀린 종류). → **체리픽서 기작 3 신규 저작** 필수. 설계 정정 = `research/broadening_w_design.md` §(b)-3·(c).

## R1 검토 ✅ (구 calibration)
- two-phase 2개 통일=v10-05·06·03·07·08·09. size 절제=동일 6종. Ω 모순=v10-01. base=v10-06+v10-05 Ω graft.

## R3 검토 ✅ (구 calibration)
- fabrication: v10-09 cogswell DOI 오류(nl300563u→nn204177u) CRIT. fly2020 저자(E.Schaltz)·권(vol.29) 오류 다수. 문체 PASS·TikZ 한글 0·빌드 9종 PDF.
- ★인용 정정(새 calibration): **드롭 = yang2023(size τ∝r²)·cogswell2012(반경)** — 사이즈 각도 제외. **추가 = Dahn1995(10.1126/science.270.5236.590 구조무질서)·Dreyer2010(10.1038/nmat2730 다입자)** — 집합 통계역학. fly2020(E.Schaltz vol.29)·Levi&Aurbach1999·RSC2021 유지.

## ★체리픽 스펙 (확정 — 새 calibration 적용)
- **base = v10-06**(w_eff 완전제거·preservation·비교그림·2기작 broadening).
- **broadening 3기작 재구성**: ①L_V 단일입자 율속꼬리(fly2020) ②내재 RT/F(Levi&Aurbach1999) ③★**집합 다입자 통계역학**(앙상블 ρ(U_j) 전이전위 분포·비-크기 구조무질서·Dahn1995·Dreyer2010·forward 통계평균 ∫ρ·응답). ρ→δ 환원. forward-only.
- ★**사이즈 효과 전면 제외**: τ∝r²·PSD 크기분산·yang2023 드롭.
- Ω/two-phase=LiC₁₂·LiC₆ 2개(v10-05 Ω 거친추정 note). w 이중지위. w_eff 완전제거. v9 보존(LCO·전자엔트로피·분포·부호·인용).

## 다음(P5)

## 다음
9종 → 검토1 → 보완 → 검토2 → 체리픽 v10c → adversarial → v10 최종 → docs/Ch1_v10/. 그 다음 P6(Ch2 v5)·P7(코드 v12)·P8.
