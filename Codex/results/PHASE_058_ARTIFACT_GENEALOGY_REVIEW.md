# Phase 058 PDF/image 생성 계보 감사

정본일: 2026-07-28
범위: PDF 8개 + standalone PNG 8개
기계 근거:
`Codex/results/PHASE_058_ARTIFACT_GENEALOGY.json`

## 판정 원칙

artifact의 마지막 저장 commit과 대응 TeX, figure generator,
production model의 마지막 변경 commit을 연결했다.

- source가 artifact와 같은 commit이거나 artifact 이전 commit이면
  build ordering은 현재 상태로 분류한다.
- source가 artifact 뒤에 바뀌었으면 저장 artifact는 원칙적으로
  stale 후보이며, render-inert 변경임을 별도 확인한 경우만 예외로 둔다.
- build ordering이 현재라는 사실은 물리 타당성이나 실험 검증을
  뜻하지 않는다.
- matplotlib PNG의 byte hash는 font, backend, compression과 metadata에
  민감하므로 bit mismatch만으로 scientific curve 차이를 단정하지 않는다.

## PDF 8개

v1.0.10 Ch2, v1.0.11 Ch1/Ch2는 TeX와 PDF가 같은 commit에 있고,
v1.0.12와 v1.0.13의 PDF는 최종 TeX 변경 뒤 저장됐다.

v1.0.10 Ch1만 PDF 뒤에 TeX commit이 하나 더 있다. 앞선 PDF
전 페이지 감사에서 그 변경은 렌더되지 않는 source comment의
계보명 정정이고 35쪽 시각 내용에는 stale defect가 없음을 확인했다.
따라서
`SOURCE_AFTER_ARTIFACT_COMMENT_ONLY_VISIBLE_CURRENT`로 처분한다.

이 판정은 PDF 조판 계보만 닫는다. v1.0.10과 v1.0.11의 48쪽이
pixel-identical이라는 사실, 그리고 문건의 물리식·주장이 타당한지는
각각 별도 판정이다.

## PNG 8개

### 현재 build ordering인 6개

- v1.0.10 sample test
- v1.0.10 P5 graph suite
- v1.0.12 sample test
- v1.0.13 P4 LCO/heat
- v1.0.13 graph suite
- v1.0.13 sample test

이 6개는 저장 commit이 대응 generator와 model의 마지막 commit보다
같거나 뒤다. 다만 Step 28.2의 direction label, glyph, truncation,
rate-invariance와 외부 검증 부재 판정은 그대로 유지된다.

### stale provenance인 2개

1. `Claude/docs/v1.0.10/figs/P4_lco_heat_validation.png`

   저장 그림 commit `88ba428` 뒤에 generator `b611fd1`과 model
   `cbbb7a3`이 변경됐다. 특히 첫 후속 commit 자체가 factor-2 entropy
   correction을 기록한다. 최종 코드 상태의 검증 그림으로 사용할 수
   없으며 `STALE_PROVENANCE_MATERIAL_SOURCE_UPDATES`로 판정한다.

2. `Claude/docs/v1.0.10/figs/anode_fit_v1_0_10_dqdv.png`

   그림과 generator는 초기 commit `5d5cee6`에 머물지만 model은
   `cbbb7a3`까지 후속 변경됐다. model 변경 뒤 재생성되지 않았으므로
   `STALE_PROVENANCE_MATERIAL_MODEL_UPDATES`로 판정한다.

따라서 v1.0.10의 저장 그림 전부를 하나의 “최종 검증 suite”로
묶어 인용하면 안 된다.

## 격리 재실행 대조

8개 generator를 현재 대응 model과 byte-identical 임시 복사본에서
실행한 결과 8/8 PNG가 생성됐다. 저장 PNG와 bit-exact한 것은 0/8이다.
이는 현재 Linux/Agg/font 환경에서 생성한 PNG의 byte size와 hash가
원 저장 환경과 다르다는 뜻이다.

이 결과를 곧바로 8개 모두 stale이라고 해석하지 않는다. source
commit 선후관계가 실제로 stale인 것은 위 두 그림이다. 나머지 6개는
build ordering이 현재지만 render bit reproducibility가 없다.
향후 검증 그림은 다음을 함께 저장해야 한다.

1. source/model commit
2. dependency·font·backend lock
3. plot data의 수치 array와 hash
4. figure rendering과 분리된 physics assertions

## Git 부분 복제 한계

현재 worktree는 과거 Git blob 일부가 내려오지 않은 partial clone이다.
따라서 누락 old blob의 본문을 새로 fetch하지 않고 commit graph,
tree path, commit message와 현재 source/격리 실행 근거로 계보를
처분했다. 이는 stale 두 건의 commit 선후관계를 바꾸지 않지만,
과거 PNG의 pixel-level scientific curve delta는 `UNRESOLVED`로 남긴다.

## Step 28.3 판정

PDF/image 16/16의 artifact–source commit 관계와 image regeneration
hash를 처분했다. 판정은
`PROVENANCE_COMPLETE_WITH_2_STALE_IMAGES_AND_HISTORICAL_BLOB_LIMIT`다.

Step 28 전체는 완료됐다. 다음 Step 29에서 v1.0.10의 좌표·보존식,
평형 peak, kinetics/hysteresis, heat/LCO 식을 표준 이론에서 독립
재유도하고 source claim을 재판정한다.
