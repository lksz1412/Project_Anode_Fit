# Phase 057BA — Git document genealogy result

정본일: 2026-07-28
세부 Step: 20.1
상태: `PASS_P057_GIT_GENEALOGY`

## Outputs

- generator:
  `Codex/work/v1010_v1025_2_reaudit/generate_phase057_git_genealogy.py`
- machine genealogy:
  `Codex/results/PHASE_057_GIT_DOCUMENT_GENEALOGY.json`
- genealogy SHA-256:
  `64c5f5c7536ac8d6dddeaa43df28b5c36d06823a73037c14b7b00dfc4d0c780b`

generator를 두 번 실행해 같은 SHA-256이 나오는 것을 확인했다.

## Result

```text
unique intent-document blobs                   271
version occurrence paths                       406
path events                                    673
unique commits                                 229
ADD events                                     406
MODIFY events                                  267
commit subjects with completion markers        102
documents whose path-add commit != current blob 81
documents with any post-introduction event      118
current blobs copied to multiple paths           42
maximum exact-blob occurrences                    9
```

`completion marker`는 commit subject에 `PASS`, `GREEN`, `완료`,
`완결`, `정본`, `bit-exact`, `무변경`, `전건`, `merge-ready`,
`마감` 중 하나가 있다는 뜻일 뿐, 주장의 참을 뜻하지 않는다.

## Genealogy Correction

기존 queue의 `introduction`은 generator 정의상
`representative_path`의 최초 `ADD` commit이다. 이는 현재
document blob의 최초 등장 commit과 같은 개념이 아니다.

- 156문건은 path-add commit에서 현재 blob이 바로 등장했다.
- 81문건은 path가 먼저 생기고 후속 commit에서 현재 blob으로
  수정됐다.
- 34문건은 같은 blob이 다른 version path에 먼저 존재한 뒤
  representative path로 복제됐다.

따라서 `introduction`은 앞으로 `path_introduction`으로 읽고,
machine genealogy의 `first_exact_blob_event`를 내용 계보에
사용한다. 기존 queue는 immutable read order 기록으로
유지하며 의미를 소급 변경하지 않는다.

## Why This Matters

- 같은 파일명이 한 버전 안에서도 draft→final로 바뀌었으므로
  최초 ADD만 읽으면 최종 내용을 잘못된 commit에 귀속한다.
- 동일 blob이 최대 9개 version path에 복제돼 version number만
  보고 새 판단으로 세면 중복 과대계상된다.
- 118문건에 path 생성 뒤 수정이 있으므로 handover의 완료
  서술과 실제 final blob 사이의 시점을 분리해야 한다.
- completion marker가 있는 commit이 102개이므로 `PASS` 문자열
  검색만으로 과학적 완결을 인정할 수 없다.

## Validation Boundary

이 step은 각 문건의 path event, 전·후 Git blob, commit subject,
parent, date와 현재 exact blob occurrence를 연결했다. commit
subject가 주장한 구체적 범위와 전체 patch의 실제 변경 경로가
일치하는지는 아직 판정하지 않았다.

## Next

Step 20.2:
229개 관련 commit의 subject claim과 실제 full patch path/stat을
대조하고, 문건 밖 코드·시험·PDF·결과 변경까지 포함한
commit claim matrix를 만든다.
