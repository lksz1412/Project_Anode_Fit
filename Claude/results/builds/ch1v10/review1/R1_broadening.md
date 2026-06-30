# R1 — broadening 절 정합 검토 (검토1 sub, 9 빌드 교차비교)

> 전담 = v10-0X broadening 절의 (1)전이별 구분+Ω/two-phase 일관성 (2)size/PSD 절제 수위 (3)핵심 기작 (4)다입자/PSD 모델 0.
> Ground truth = `research/broadening_w_design.md`·`radius/ORIGIN_VERDICT.md`·`v10-00_spine/BUILD_TRACKING.md`(★calibration).
> ★calibration 결정: **two-phase = LiC₁₂(2L→2)·LiC₆(2→1) 2개만**(dilute·4L-3L=solid-solution), **size/PSD 절제**(현상학적 w 흡수·1문장·모델/추출 X), 핵심기작 = **L_V 단일입자 꼬리 + 내재 RT/F**, 코드 Ω 초기값(전부>2RT)=*거친 추정* 명시, 다입자/PSD 모델 0·forward-only·ill-posed·반경→평형U 무효.
> 검토 의견만(파일 수정 X). 작성 2026-06-30.

---

## (a) 9종 broadening 랭킹 — 전이별·size 절제·다입자 0 종합

| 순위 | 빌드 | 전이별 구분 | Ω/two-phase 일관성 | size 수위 | 기작 수 | 다입자0/forward/ill-posed | 형식 | 종합 |
|---|---|---|---|---|---|---|---|---|
| **1** | **v10-05 (O)** | A | ★**완전**: 표 Ω 초기값 전부>2RT를 *거친 출발점*으로 명시→피팅이 갈림(SS는 Ω<2RT 내려감) | **절제**(2기작) | 2 | 전부+tier 등급 | 비교그림+tier | ★Ω 거친추정 유일 명시. 통일+절제+완비 |
| **2** | **v10-06 (O)** | A | 완전: spinodal 문턱 Ω>2RT=LiC₁₂·LiC₆만. 코드 폭폴백(0.012-0.020V)·n_j<1 까지 reconcile | **절제**(2기작) | 2 | 전부 | keybox+비교그림+Maxwell | 물리 가장 정밀. 단 Ω 초기값 "거친추정" 라벨은 미사용(spinodal로 우회) |
| **3** | **v10-03 (S)** | A | 양호: 단상=Ω<2RT / 두-상=Ω>2RT 직접 병기. 코드 초기값 거친추정 언급 X | **절제**(size 미featured) | 2 | 전부 | keybox | 절제·간결·정합. Ω 초기값 caveat 없음 |
| 4 | v10-07 (Codex) | A | 양호: 두-상=강한1차=LiC₁₂·LiC₆. LCO까지 Ω>2RT 일관. 초기값 caveat X | **절제**(size 미언급) | 2 | 전부(keybox) | keybox·lean | 핵심 완비, 짧음·그림X·기작 DOI 분해X |
| 5 | v10-09 (Codex) | A | 양호(=07). 초기값 caveat X | **절제** | 2 | 전부(keybox) | keybox·lean | 07과 동급, 약간 얇음 |
| 6 | v10-08 (Codex) | A | 양호(=07). 초기값 caveat X | **절제** | 2 | 전부 | keybox·lean | 07과 동급, 가장 얇음 |
| 7 | v10-02 (S) | A | 양호: SS=Ω≤2RT / 두-상=Ω>2RT 병기. 초기값 caveat X | **경계**: size를 *scope 경고 bullet*에 "주요 기작 확인되었으나 구현X"로 둠(featured 아님) | 2 | 전부 | 절 4개 | size가 scope에 들어와 살짝 부각. 그래도 모델 X |
| 8 | v10-04 (O) | A | 양호: 두-상=Ω>2RT=LiC₁₂·LiC₆. 초기값 caveat X | ★**과다**: size kinetic τ∝r²을 (ii) "broadening의 주범"으로 **featured**(단 "모델 분리X·w 흡수" 명시) | **3** | 전부+그림 | 비교그림+X1-3 | 가장 길고 물리 풍부하나 **size featured=절제 위배** |
| 9 | v10-01 (S) | A | △**긴장 잔존**: 표 4건 전부 Ω>2RT라 **이중지위를 staging 4건 전체 적용**(두-상 2개로 좁히지 않음) | ★**과다**: size를 (b-ii) "[확정·강한지지]"로 **featured** | **3**(단 "두 기여"라 써놓고 "셋 다"+b-i/ii/iii 나열=**카운트 모순**) | 전부 | 절 3개 | size featured + Ω 미통일 + 기작 카운트 자기모순 |

★ A = 전이별 구분 정확(SS=dilute·4L-3L / two-phase=LiC₁₂·LiC₆). **9종 모두 전이별 구분 자체는 정확** — 차이는 Ω 일관성 처리·size 수위·완비도.

---

## (b) ★체리픽 추천

- **base 골격 = v10-06** — 물리 가장 정밀(Maxwell 공통접선·plateau 내부/양끝 분리·n_j<1로 폭폴백 reconcile), 2기작 절제, keybox+비교그림, 다입자0 완비. spine 의 base=v10-06 결정과 일치.
- **graft (필수) = v10-05 의 Ω 단락** — v10-06 이 유일하게 안 한 것 = "표 Ω 초기값 4건 전부>2RT는 *거친 출발점*이고 피팅으로 SS는 Ω<2RT 내려가 갈린다"는 명시(v10-05 line 1177-1181). 이걸 v10-06 (a)에 이식하면 ★calibration "코드 Ω 초기값=거친 추정 명시" 요건 충족 + v10-01 의 긴장(4건 전체 적용)이 정면 해소됨.
- **graft (선택) = v10-05 의 tier 등급 단락**(line 1261-1265, "절대 mV는 1차문헌 부재=열린문제→초기값+피팅") — 4-tier 규율·radius 조사 결론과 직접 정합. v10-03 keybox 의 간결 요약도 보조 채택 가능.
- **버릴 것**: v10-04·v10-01 의 size featured 단락(τ∝r² 주범) — 절제 결정 위배. v10-04 비교그림은 v10-05/06 것이 더 깔끔하니 불채택.

→ **체리픽 v10c = v10-06 골격 + v10-05 Ω거친추정·tier 단락 graft + size는 (c) scope 안에서 1문장 "현상학적 w 흡수"로만**.

---

## (c) 결함표 (refute 우선·★ = calibration 직격)

| # | 빌드 | 결함 | 심각도 | 근거/수정 |
|---|---|---|---|---|
| D1 | ★v10-01 | Ω 미통일: 표 4건 전부 Ω>2RT라 **이중지위를 staging 4건 전체에 적용**(line 1150-1152) — 두-상 2개로 좁히는 calibration 위배. "거친 추정→피팅이 갈린다" 처리 없음 | HIGH | v10-05 line 1177-1181 식으로 재정합 필요 |
| D2 | ★v10-01 | size를 (b-ii)로 featured(line 1163-1168) — 절제 위배 | HIGH | scope 1문장 흡수로 강등 |
| D3 | v10-01 | 기작 카운트 자기모순: line 1155 "두 기여가 합성된다" → 직후 "셋 다"+b-i/b-ii/b-iii 나열 | MED | "세 기여"로 정정 or 2기작으로 절제 |
| D4 | ★v10-04 | size kinetic τ∝r²을 (ii) "broadening의 주범"으로 featured(line 1178-1185, 3기작 §제목 "동역학·입자분산·내재폭") — 절제 위배. (단 "모델로 분리X·w 흡수" 명시는 있어 모델 0 요건은 충족) | HIGH | 기작은 2개(L_V+내재RT/F)로, size는 scope 흡수 |
| D5 | v10-02 | size가 scope 경고 bullet(line 1182-1185)에 "주요 기작으로 확인되었으나 구현X"로 등장 — featured 아니나 절제 best 대비 살짝 부각 | LOW | 허용 범위. "입자 heterogeneity 흡수" 한 문장으로 더 줄이면 best |
| D6 | v10-05·06·03·07·08·09 | 코드 Ω 초기값=거친추정 명시 = **v10-05 만 함**. 06/03/07/08/09 는 미명시(긴장 자체는 안 만들지만 calibration 명시요건 미충족) | MED | base에 v10-05 Ω단락 graft로 일괄 해소 |
| D7 | v10-05 | line 1175 "LCO T1·T2·T3 두-상도 해당" — 흑연 two-phase=2 와 별개로 LCO 두-상 확장은 **정확**(모순 아님). 단 흑연 two-phase=2 메시지가 LCO 언급에 흐려지지 않게 문장 경계 유지 권고 | LOW | 결함 아님·주의만 |
| D8 | v10-07/08/09 | lean — 비교그림·기작별 DOI 분해·Ω거친추정 단락 부재. 핵심 정합은 완비라 base론엔 부적합하나 **graft 검증용 교차참조로 유효** | LOW | base는 06, 이들은 cross-check |

★공통 양호(9종 전부 PASS): forward-only·ill-posed(1종 Fredholm)·반경→평형U 무효(Cogswell 22nm·~0.01mV)·다입자/PSD convolution 모델 0·apparent-U=U_j+η(분포=η)·평형 U_j=GITT 입자무관 상수(Park 2021). **이 4번 요건은 9종 모두 충족** — 차별점은 Ω 일관성과 size 수위뿐.
