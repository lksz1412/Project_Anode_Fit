# v1.0.24.1 — v1.0.24 피드백 리비전(FB0~FB9) 동결 아카이브

## 지위
**동결(frozen) · 아카이브 전용.** 본 폴더는 v1.0.24 가 사용자 1차 정독 피드백(F-01~F-11) + 어조 강화(FB8) +
★ 마커 제거(FB9)를 거친 **리비전 완료 상태**의 충실한 스냅샷이다. 이후 개발은 본 폴더가 아니라 `v1.0.24/`
(또는 후속 버전)에서 진행한다. 파일 내용은 수정하지 않는다.

## 출처(provenance)
- 원본 = `Claude/docs/v1.0.24/` (동일 커밋 시점).
- 리비전 캠페인 = `Claude/results/V1024_FEEDBACK_EXECUTION_LEDGER.md` (FB0~FB9 12-col 원장).
- phase 결과 = `Claude/results/PHASE_FB0_RESULT.md` ~ `PHASE_FB9_RESULT.md`.
- 버전 비교 감사 = `Claude/results/comp_v24/VERSION_COMPARISON_v19_v23_v24.md`.

## 리비전 요약 (v1.0.24 원판 → 본 동결본)
- **FB0~FB7 (F-01~F-11)**: §1.1.4 배경 압축·확률/압력 P 충돌 해소·식1.21 f 명료화·제목 N-태그 제거·register
  평서화·조판(여백/줄간/microtype)·E.3·식2.39 overflow 해소·LCO 서두 재균형·일본어투 용어 정리·**코드=부록 전용**.
- **FB8 (어조 강화)**: 은유·의인·구어 중립화(되밟다→재현·되살리다→복원·비틀다→조정 등) + 정의어 rename
  (생존 지도→대응 지도·정직 공백→미결 공백).
- **FB9 (★ 마커 제거)**: 본문 ★/$\bigstar$ 57개 전량 제거(주석 34행 동결), 앵커 3쌍 phrase 헤더 정합 유지.
- **불변**: 물리 골격·식 번호·`\label` 정의·`\eqref`/`\ref`/`\cite` 키·코드(`.py`) 무변경.

## 구성 (파일명 = v1.0.24 유지 · 동결 사본 방식)
- 마스터 3본: `ch1_graphite_v1.0.24.tex` · `ch2_lco_v1.0.24.tex` · `ch3_si_v1.0.24.tex`
- `_sections/` (56 .tex) · `appendix_phase_separation.tex`
- 코드: `Anode_Fit_v1.0.24.py` (sha256 `f230f59b…`) · `CODE_GUIDE_v24.{md,html}` · `FITTING_GUIDE.md` ·
  `test_gates_v1024*.py`
- 빌드본 PDF 3종(검토·게이트 통과본): `ch1_graphite_v1.0.24.pdf`(97p) · `ch2_lco_v1.0.24.pdf`(30p) ·
  `ch3_si_v1.0.24.pdf`(21p)
- `plans/` · `results/` (버전-로컬 마감 문서: MERGE_READINESS·HANDOVER·INDEX_v24 + FB addenda)
- **제외**: 빌드 중간산물(`*.aux`/`*.log`/`*.out`/`*.toc`/`__pycache__`) — 재빌드로 복원 가능.

## 무결성 검증 (동결 시점)
- `diff -rq v1.0.24 v1.0.24.1` (빌드산물 제외) = **IDENTICAL**.
- 코드 `sha256 = f230f59b…` (FB 캠페인 baseline 과 동일 — 문건 한정 리비전).
- 빌드 GREEN: 0-error · undefined ref/cite 0 · 97/30/21 페이지.
- 본문 ★ = 0 · 주석 ★ = 34(동결).

## 파일명 규약 주의
동결 사본 방식(사용자 결정)이라 **내부 파일명은 v1.0.24 를 유지**한다. 개정 식별자는 **폴더명 `v1.0.24.1`** 이
담당한다(정식 rename 스냅샷 아님). 서브버전 번호 규약은 `v1.0.18.1`/`v1.0.18.2` 선례를 따른다.
