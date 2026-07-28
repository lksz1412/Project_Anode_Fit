# Phase 059 PDF·image·golden 생성 계보 감사

정본일: 2026-07-28

판정: `CONDITIONAL_P059_ARTIFACT_GENEALOGY_WITH_PDF_DEPENDENCY_BLOCK_AND_NON_BIT_EXACT_REGENERATIONS`

## 범위와 판정 경계

PDF 18개, PNG
24 occurrence/10 unique,
golden NPZ 6 occurrence/
2 unique의 current blob, 최초 도입
commit, 마지막 변경 commit, 대응 TeX/generator/model/test commit을
연결했다.

commit 선후관계와 재생성 hash는 artifact의 생성 계보만 판정한다.
물리식, 재료 identity, parameter, 문헌 또는 실험 타당성을 승인하지
않는다.

## PDF 계보와 재빌드 한계

- 18 PDF는 byte hash로는 모두 다르다. 그러나 v1.0.15와 v1.0.16
  appendix는 TeX가 exact-identical이고 8개 rendered page signature도
  동일하며, v1.0.16 표지에는 `버전 1.0.15 초안`이 남아 있다.
- 모든 PDF–TeX commit 관계를 기록했다. source-after-artifact PDF는
  0개다.
- XeLaTeX probe는 `DEPENDENCY_BLOCKED_MISSING_KOTEX_AND_D2CODING`다. engine은
  `XeTeX 3.141592653-2.6-0.999995 (TeX Live 2023/Debian)`이지만 `kotex.sty`가 없고 D2Coding
  요청은 `DejaVu Sans`로 fallback된다.
- 이 공통 dependency preflight 실패 뒤 18개를 반복 실패시키지
  않았다. 그러므로 저장 PDF의 bit-exact 재현은
  `UNTESTED_DEPENDENCY_BLOCKED`이며, 저장 PDF가 현재 TeX의
  재빌드 산출물이라는 주장도 이 환경에서는 승인하지 않는다.

## PNG copy-forward와 현재 generator

- 24 path occurrence는 10 unique blob으로 수렴한다. 14 occurrence는
  이전 blob의 exact copy-forward다.
- filename의 version token이 현재 directory와 다른 것은
  11개다. 여기에는
  v1.0.16 title/generator 그림이 `v1_0_14` 이름으로 네 release에
  남은 경우와 old graph-suite filename의 후속판 복제가 포함된다.
- 각 occurrence를 그 version의 current generator와 production
  model에 다시 연결했다. source-after-artifact 후보는
  5개다:
- `Claude/docs/v1.0.16/figs/P4_lco_heat_validation.png`
- `Claude/docs/v1.0.16/figs/graph_suite_v1015.png`
- `Claude/docs/v1.0.16/figs/anode_fit_v1_0_14_dqdv.png`
- `Claude/docs/v1.0.16/figs/graph_suite_v1016.png`
- `Claude/docs/v1.0.16/sample_test_v1016.png`
- Step 34.3의 disposable rerender 24개와 저장 PNG를 대조하면
  bit-exact는 0/24이다.
  환경·font·backend·metadata에
  민감한 PNG byte mismatch만으로 curve 차이를 단정할 수 없다.
  반대로 plot-data array/hash가 저장되지 않았으므로 scientific
  curve equality도 입증할 수 없다.

## Golden NPZ 계보

- v1.0.14 한 blob과 v1.0.15 이후 다섯 경로의 한 blob, 총 2 unique다.
  후속 4 occurrence는 v1.0.15 golden의 byte-identical copy-forward다.
- generator test 또는 model이 artifact 뒤에 바뀐 후보는
  2개다:
- `Claude/docs/v1.0.14/golden_graphite_ref.npz`
- `Claude/docs/v1.0.16/golden_graphite_ref.npz`
- 현재 재계산은 모든 version에서 key 13/13과
  `rtol=0, atol=5e-15` 13/13이 일치하지만 bit-exact array는
  1/13뿐이다. 따라서 golden은 현재 model의 byte-exact 재현물이
  아니라 historical, tolerance-level internal snapshot이다.
- 특히 v1.0.15 이후 같은 golden blob의 반복은 새 물리 검증 또는
  새 실험 증거가 아니다.

## 권위 판정

1. PDF: build ordering은 기록됐으나 현재 환경 재빌드는 한글 TeX/font
   dependency 부재로 막혔다.
2. PNG: 14 exact copy-forward, 0/24 bit-exact rerender이며 plot-data가
   없어 byte mismatch와 scientific curve delta를 분리할 수 없다.
3. Golden: 4 exact copy-forward, 재계산 13/13 tolerance pass이나
   1/13 array exact다.
4. 세 artifact 계열 모두 내부 consistency/provenance evidence일 뿐
   사용자가 요구한 저온×전류, Si/blend, doped high-voltage LCO
   실험 타당성을 제공하지 않는다.

## 다음 단계

Step 36.1에서 v1.0.14의 textbook register, derivation restructuring,
width budget와 theory-only 본문 경계를 v1.0.13과 exact diff로
재판정한다.
