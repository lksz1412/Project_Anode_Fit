# Ch1 v10 — AUTHOR_BRIEF (9종 경쟁 빌드 입력)

> competition-cherrypick 스킬. base = `base_v9.tex`(1644줄 = 현 Ch1 v9: 흑연 forward + LCO 전자 엔트로피 + ξ_eq 분포). 9 작가(무통신) 동일 배포. ★v10 = v9 정정·업데이트 통합본 — broadening 복원 + w 이중지위 + w_eff 제거.

## 목표 (한 줄)
현 v9 의 **모든 것(흑연 forward·LCO 전자 엔트로피·ξ_eq 분포·통계역학·부호) 보존** + ★**v8/v9 가 덜어낸 종모양 broadening 설명 복원** + **w 이중지위 명시** + **w_eff 제거**. "전부 때려박기".

## ★먼저 정독 (전부 `Claude/`)
- `results/research/broadening_w_design.md` (★P2 설계 — broadening 절 내용·전이별·현상학적 w·범위경고·w 이중지위·w_eff 제거 전부)
- `results/research/radius/ORIGIN_VERDICT.md`·`DOCS_say_about_distribution.md` (물리 근거·v4/v5 verbatim)
- 네 `v10-0X/v10-0X.tex` (편집 대상 = v9 base)

## ★추가 (P2 설계대로)
1. **broadening 절**(신규, 평형 peak 절 부근): (a) 전이별 출발 — dilute·4L↔3L = solid-solution 이라 *이미 종*(broadening 불요) / 2L→2(LiC₁₂)·2→1(LiC₆) = two-phase = 평형 *델타에 가까움*. (b) two-phase 델타→실측 유한 종 = **유한율속 비대칭 꼬리(모델 L_V) + 내재 RT/F 폭** → ★**$w_j$(두-상) = 현상학적 자유 피팅 폭, 평형 예측 아님**(apparent-U=U_j+η, 분포는 η). (c) ★범위 경고 = **평형 U_j·반경 분포 peak 추출 안 함**(반경→평형U 마이크론서 무시·GITT 상수)·**dQ/dV→분포 역산 ill-posed(forward-only)**·★**다입자/PSD convolution 모델 안 만든다**(입자 heterogeneity 는 현상학적 w 에 흡수로만 언급).
2. **w 이중지위**(N4/N5 폭 절 보강): 단상 Ω<2RT = $nRT/F$ 평형 예측 / 두-상 Ω>2RT(staging 4개 전부) = 현상학적 자유 피팅 폭. 명시 문장.
3. **w_eff 제거**: 현 v9 에 $w_\eff(\Omega)$ "종 좁힘→델타" 류 자취 있으면 제거(two-phase 실측은 종이지 델타 아님; narrowing 반대). 종폭은 §1(b) broadening 이 설명.

## ★보존 (불가침)
- v9 의 흑연 4전이·LCO 전이·**전자 엔트로피 절**(Fermi-Dirac→Sommerfeld·MIT 게이트·ΔS_e 삽입<0)·ξ_eq 분포 프레이밍·부호 사슬·인용·그림 **전부 보존**. broadening·w 는 *추가/보강*만.

## 품질 렌즈 (자체 10회·청크/렌즈 회전)
- ★**broadening 정합**: 전이별 구분 정확? two-phase 만 broadening 필요? **현상학적 w**(평형 아님) 명시? ★**다입자/PSD 모델 0**(설명만)? forward-only·ill-posed·반경=평형U 무효 경고? apparent-U=U_j+η?
- ★**w_eff 잔존 0**: $w_\eff$ narrowing 그림 완전 제거?
- **w 이중지위** 명시·코드(use_w_eff=False 기본)와 정합.
- G-derive·부호(흑연/LCO/전자 ΔS_e 삽입<0 1:1)·기존 LCO/분포/전자엔트로피 보존·orphan-0·인용 정확·tier 정직.

## 빌드
xelatex(kotex/D2Coding) 0-error(`cd v10-0X && xelatex -interaction=nonstopmode v10-0X.tex` 2회·페이지참조 3회). ★증분 Edit/insert(거대 Write 금지). 그림: 기존 보존 + (선택) 평형 델타 vs 실측 종 broadening 시각화(TikZ 영어 ASCII).

## 산출 (작가별)
`results/builds/ch1v10/v10-0X/v10-0X.tex`(xelatex 0-err) + 노트(broadening 절·w 이중지위·w_eff 제거·기존 보존·자체 10회). 9 작가 = v10-01–03 Sonnet·04–06 Opus·07–09 Codex(단계구동·관찰). ★sub commit/push 금지.
