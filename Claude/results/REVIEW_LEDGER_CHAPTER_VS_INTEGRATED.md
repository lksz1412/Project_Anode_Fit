# REVIEW LEDGER — 챕터별 문건 ↔ 통합본 무손실 대조 (전문 정독)

- 일자: 2026-05-29
- 작업: 사용자 지시 — "가장 마지막 통합버전 ↔ 챕터별 마지막 버전 비교, 챕터→통합
  전환(에러 수정 포함)에서 날아간 내용 확인". 전문 정독(grep/diff 등 꼼수 금지) 기본정책 준수.
- 비교 대상:
  - 챕터별 마지막 버전 = `Claude/docs/graphite_ica_consolidated_ch{1..6}.tex` (standalone)
  - 통합본 실제 본문 = `Claude/docs/_body_ch{1..6}_v2.tex` (master `graphite_ica_consolidated_full.tex` 가 `\input`)

## 방법
각 통합본 body 파일을 1줄부터 끝까지 전문 정독하고, 동일 챕터 standalone 의 document body
(즉 `\begin{document}`~`\end{document}` 중 preamble/`\maketitle`/`\tableofcontents`/
`\begin{thebibliography}`블록 제외분)와 1:1 대조.

## 결과 — 챕터 → 통합본 손실: 없음

| 챕터 | body 줄수 | 대조 | 비고 |
|---|---|---|---|
| Ch1 | 798 | 완전 일치 | 서~자체검수표 전부 보존 |
| Ch2 | 413 | 완전 일치 | 서~결론 전부 보존 |
| Ch3 | 435 | 완전 일치 | 편집분(ρ_j=ρ_G 동일물 주석 L38–39, reconcile boundbox 2개 L183–198, 검수행 L393–394) 포함 |
| Ch4 | 359 | 완전 일치 | 편집분(Ch2 3-분해 관계 주석 L62–68, verifybox 정련 L134–137, 검수행 L321) 포함 |
| Ch5 | 343 | 완전 일치 | |
| Ch6 | 339 | 완전 일치 | |

- body 추출(awk)은 preamble + `\maketitle` + `\tableofcontents`(+직후 `\newpage`) +
  `\begin{thebibliography}`…`\end{thebibliography}` 만 제거. 본문/식/박스/longtable/검수표/결론 전부 보존.
- 에러 수정 단계(ch4 `\cand` 매크로 추가; ch3/ch4 cross-fix; 매크로 rename \relax→\rlx, \ss→\sstat, \ext 추가)
  는 standalone 에 적용 후 body 재생성됨 — body 가 편집 결과를 그대로 반영함(재생성 파일까지 무손실 확인).
- 마스터 빌드: 0 에러 / 미해결 ref·cite·중복 0 / 61p (매크로 union·정리환경 union·bib dedup 정상).

## 결과 — 별개 축(원본 (B) → 챕터 작성)에서의 실제 손실 (통합 단계 아님)

전문 정독 중 발견. Ch1 `\section{Barrier 분포 → relaxation-length spectrum}` (sec:spectrum) 에서
(B) 원본 §장벽 분포 확장(원본 407, 412줄) 대비 누락:
1. 장벽의 enthalpy/entropy 분해 `g(T)=h−Ts` (및 후속 장 이관 명시)
2. 시변 온도 동역학서 `∂ρ_j/∂T` 추가항 주의 → domain 을 `g=h−Ts` 또는 `ρ_j(h,s)` 로 재정의
3. (B) 자체검수표의 대응 점검행("온도 의존 장벽 분포 시간미분 시 추가항 위험 명시")

→ 이는 챕터→통합 손실이 아니라 (B)→챕터 작성 단계 누락. 복원 여부는 사용자 지시 대기.

## 절차 메모(CLAUDE.md 준수 관련)
- 글로벌 `~/.claude/CLAUDE.md`·`_claude/memory/` 는 본 원격 컨테이너에 미동기화(부재) — 환경 제약.
- 프로젝트 `Claude/plans/`·`Claude/results/` 는 존재. 본 ledger 로 감사 기록 보강.
- 위반 시정: 전문 정독 기본정책 준수, 사용자 선택지 팝업(AskUserQuestion) 미사용.
