# Phase 058 PDF 전 페이지 렌더 감사

정본일: 2026-07-28  
범위: v1.0.10–v1.0.13 PDF 8개, 총 215 pages  
기계 근거:
`Codex/results/PHASE_058_PDF_RENDER_METRICS.json`,
`Codex/results/PHASE_058_PDF_VISUAL_REVIEW.json`

## 절차

PDF skill 절차에 따라 Poppler로 96 dpi PNG를 전 페이지 생성했다.
17개 contact sheet에서 215쪽을 모두 시각 검독했고, raster edge-touch
후보 4쪽은 full-resolution page로 다시 확인했다. 동시에 pypdf와
`pdffonts`로 page count, text extraction, replacement glyph,
media/crop box와 font embedding을 검사했다.

첫 실행에서 v1.0.10 Ch1 p.17의 중간 PNG가 truncated였으나
단일 페이지 재렌더가 정상 통과했다. 전체 clean rerun에서는 215/215
PNG가 정상 해석됐으므로 PDF source 결함이 아니라 transient renderer
artifact로 처분했다.

## 전체 결과

| 항목 | 결과 |
|---|---:|
| PDF | 8/8 |
| PDF pages | 215 |
| 정상 렌더 page | 215/215 |
| contact sheet 시각 검독 | 17/17 |
| blank candidate | 0 |
| U+FFFD replacement character | 0 |
| media/crop box mismatch | 0 |
| font embedding | 전 font embedded |
| 확인된 clipping defect | 4 pages |

Computer Modern math-extension font 일부에는 ToUnicode map이 없지만
font 자체는 embedded이고, 렌더에서 black square·missing glyph·깨진
수식은 보이지 않았다. 이 문제는 검색/복사 접근성의 제한이지 현재
시각 glyph 누락은 아니다.

## 확인된 조판 결함

1. v1.0.10 Ch2 p.10: Table 2의 우측 rule과 마지막 열 문장이
   page boundary까지 나가 잘린다.
2. v1.0.11 Ch2 p.10: 위 결함의 pixel-identical copy다.
3. v1.0.12 Ch1 p.37: 긴 boxed forward-flow 식의 오른쪽이 잘린다.
4. v1.0.12 Ch2 p.11: Table 2 마지막 열이 오른쪽 margin을 넘어 잘린다.

v1.0.13에서는 같은 Ch2 table이 조정되어 edge-touch 후보에서
사라졌다. 이는 조판 개선이지 해당 표의 과학 내용이 검증됐다는 뜻은
아니다.

## PDF 계보 관찰

v1.0.10과 v1.0.11은 Ch1 35/35, Ch2 13/13 pages가
pixel-identical이었다. PDF file hash가 다른 것은 embedded font subset
식별자나 build metadata 차이이며, 시각 내용은 동일하다. TeX source도
동일 blob이므로 v1.0.11을 새 이론 또는 새 PDF 검증으로 세지 않는다.

v1.0.10 Ch1 PDF의 마지막 commit 뒤에 TeX 1행이 바뀌었지만
변경 내용은 source comment의 코드 계보명 교정뿐이었다. 렌더되는
본문에는 영향이 없어 visible-stale defect로 판정하지 않는다.
v1.0.12와 v1.0.13 PDF는 각각 최종 TeX 변경 뒤 별도 final-build
commit에서 저장됐다.

## 범위 경계

이 감사가 확인하는 것은 page rendering과 시각 전달 상태다.
잘 렌더됐다는 사실은 이론식, 인용, 물성값 또는 code conformance의
타당성을 뜻하지 않는다. source-level 과학 판정은 Phase 058
Steps 29–32에서 별도로 수행한다.

## Step 28.1 판정

8개 PDF 215쪽의 전 페이지 렌더·시각 검독은 완료했다.
문서는 전반적으로 읽을 수 있으나 clipping 4쪽 때문에
`LAYOUT_PASS_WITH_4_RECORDED_DEFECTS`로 판정한다.

## Standalone image 감사

8개 standalone PNG를 저장 원해상도로 각각 열어 축, 단위, 범례,
조건, sign/direction, peak morphology와 glyph를 전수 검독했다.
파일·generator hash, 크기와 raster metric은
`Codex/results/PHASE_058_STANDALONE_IMAGE_AUDIT.json`,
파일별 판정은
`Codex/results/PHASE_058_STANDALONE_IMAGE_REVIEW.md`에 보존했다.

주요 결과는 다음과 같다.

- 8/8 image와 generator가 존재하고, 8개는 서로 다른 nonblank blob이다.
- v1.0.10 P5 graph suite의 한글 glyph가 tofu square로 깨진다.
- v1.0.13 P4 panel (c)의 긴 제목이 subplot 오른쪽에서 잘린다.
- LCO C-rate 곡선은 sample/P4 전반에서 거의 겹쳐 current broadening을
  검증하지 않는다.
- 저온 graph는 더 높고 좁은 평형 peak를 보여 사용자의 finite-current
  저온 관측을 설명하지 않는다.
- LCO 방향 표기는 v1.0.13 code/demo 일부에서 고쳤지만
  `sample_test_v1013.png`에는 `discharge`가 남아 같은 버전 안에서도
  일관되지 않다.
- 8개 모두 model-generated output이며 public experiment,
  uncertainty, residual 또는 holdout overlay가 없다.

## Step 28.2 판정

판정은 `VISUAL_COMPLETE_SCIENTIFIC_VALIDATION_ABSENT`다.
PDF/image render가 완료됐다는 사실을 물리 validation으로 승격하지
않는다. 다음 Step 28.3에서 저장 artifact와 generator/source의 Git
commit 및 격리 재실행 hash를 연결해 stale 여부를 확정한다.

## Step 28.3 생성 계보 판정

PDF 8개와 PNG 8개의 저장 commit을 TeX, generator와 model commit에
연결했다. 상세 기계 기록과 판정은 다음에 보존했다.

- `Codex/results/PHASE_058_ARTIFACT_GENEALOGY.json`
- `Codex/results/PHASE_058_ARTIFACT_GENEALOGY_REVIEW.md`

v1.0.10 P4 LCO/heat 그림은 factor-2 정정 및 model 변경 전 artifact,
v1.0.10 dQ/dV overview는 최종 model 변경 전 artifact다. 두 그림은
최종 코드 상태의 증거에서 제외한다. 나머지 6개 PNG의 build ordering은
현재지만 격리 재실행과 bit-exact한 그림은 0/8이었다. PNG hash는
rendering environment에 민감하므로 commit ordering과 plot-data
assertion을 함께 보존해야 한다.

Step 28 판정은
`PROVENANCE_COMPLETE_WITH_2_STALE_IMAGES_AND_HISTORICAL_BLOB_LIMIT`다.
