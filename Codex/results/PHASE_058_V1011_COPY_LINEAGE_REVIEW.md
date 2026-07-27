# Phase 058 v1.0.11 copy lineage 재판정

정본일: 2026-07-28

대상: Phase 058 Step 30.1

기계 matrix:
`Codex/results/PHASE_058_V1011_COPY_LINEAGE_MATRIX.json`

## 결론

v1.0.11은 새 물리·코드·시험 버전이 아니다. commit
`d86e00849a019463b6535df8322d6e8afc07b93a`에서 만든
v1.0.10 baseline의 증판 작업이며, 대응 text 8개 3,965행은 전부
byte-identical이다. PDF 2개는 build timestamp 때문에 file hash가
다르지만 48/48 pages가 pixel-identical이다.

판정:

`V1011_IS_A_BYTE_IDENTICAL_TEXT_BASELINE_COPY_AND_RENDER_IDENTICAL_PDF_REBUILD`

## 대응 text

| 역할 | v1.0.10 ↔ v1.0.11 | 행 | 판정 |
|---|---|---:|---|
| production code | `Anode_Fit_v1.0.10.py` ↔ `Anode_Fit_v1.0.11.py` | 851 | filename-only relabel, byte-identical |
| fitting guide | `FITTING_GUIDE.md` ↔ same | 46 | byte-identical |
| LCO/heat demo | `demo_lco_heat.py` ↔ same | 72 | byte-identical |
| Chapter 1 | `graphite_ica_ch1_v1.0.10.tex` ↔ `...v1.0.11.tex` | 1,937 | filename-only relabel, byte-identical |
| Chapter 2 | `graphite_ica_ch2_v1.0.10.tex` ↔ `...v1.0.11.tex` | 750 | filename-only relabel, byte-identical |
| dQ/dV plot | `plot_dqdv.py` ↔ same | 135 | byte-identical |
| sample test | `sample_test_v1010.py` ↔ `sample_test_v1011.py` | 94 | filename-only relabel, byte-identical |
| regression | `test_regression_graphite.py` ↔ same | 80 | byte-identical |

파일명에 v1.0.11을 붙였어도 내부 header, version label, import logic와
물리 내용은 바뀌지 않았다. 이는 version-only content claim도 아니다.
더 정확히는 “새 경로에 동일 blob을 놓은 baseline copy”다.

## PDF

| PDF | file hash | render |
|---|---|---|
| Chapter 1, 35 pages | 다름 | 35/35 pixel-identical |
| Chapter 2, 13 pages | 다름 | 13/13 pixel-identical |

두 pair는 제목·producer·page geometry가 같고 CreationDate만
2026-07-01에서 2026-07-02로 바뀌었다. v1.0.10 Ch2 p.10의 right-edge
clipping도 v1.0.11에 pixel-identical하게 복사됐다. 따라서 rebuild는
artifact 생성 재현이지 조판 수정이나 새 이론 검증이 아니다.

## 복사되지 않은 v1.0.10 자료

v1.0.10의 problem/integrity/handover 세 보고서, graph suite와 저장
PNG 네 개는 v1.0.11 docs에 복사되지 않았다. 반대로 새로 생긴 유일한
기록성 자료는 docs 밖의
`Claude/results/process/V1011_EXECUTION_LEDGER.md`다.

그 원장은 Phase 0.1 baseline copy만 완료했고, LCO 수식화·인계 minor·
default 사용성·최종 점검은 각각 진행 중 또는 미착수로 남긴다.
따라서 “v1.0.11에서 LCO 수식화가 완료됐다”는 해석은 원장 자체와
모순된다.

## 물리 계보에서의 의미

v1.0.11에는 다음 변화가 0개다.

- scientific source change
- production execution-path change
- default/parameter change
- test assertion change
- new experimental validation

따라서 v1.0.10에서 확인한 factor-3600, equilibrium/free-energy 혼합,
default current invariance, grid switch, frozen barrier, entropy-width,
heat sign과 LCO scope 결함이 모두 그대로 계승된다.

v1.0.11의 가치는 새 모델이 아니라 “v1.0.12 작업 전 baseline을
동결한 provenance checkpoint”에 한정한다. 다음 Step 30.2에서
v1.0.12 patch만 실제 정정 후보로 판정한다.
