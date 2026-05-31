# HANDOVER — RB-series 재구성 (2026-05-30/31 세션)

> **Chain 헤더(누적)**: HANDOVER_RB_2026-05-31 (첫 RB 핸드오버) ← 직전 = 폰 통합본 8종 합류 + Phase A/B 적대 재검수 + Ch1 재구성.
> 복구 시 이 문서 + `RB_EXECUTION_LEDGER.md` 정독 후 이어받기.

---

## 1. 본 세션 지시·작업 요약

**사용자 핵심 지시(누적, 생략 없이)**:
1. 폰 브랜치 작업물 로컬로 끌어와 재검사. → 완료(`origin/claude/chapter-1-physics-logic-WD1R5` 합류).
2. **통합본 8종 기준 "논문 수준 논리를 학부생도 이해하게" 재구성. 수식 흐름 보존, 물리 타당성 검증하며 재유도. 모든 가정식 논문/교과서 근거. 계산편의 비약 배제. 근거 논문 필수. 챕터 하나씩.**
3. 방향-3 정정: 가정·논리 문제 발견 시 "멈춤"이 아니라 **논리 재작성**(필요 시 장 백지화).
4. 의존 트리: Ch1(심플 열역학+극판전위 배리어 낮춤) → Ch2(Ch1 이용, 가역 반응열) / Ch3(Ch1 기반, 반응속도론 일반화) → Ch4(Ch3 이용, 가역 반응열) / Ch5(Ch3 기반, 히스테리시스). Ch6=피팅 실무 부록(기존 내용 먼저 검토). +refs. = 내부 7종 + 합본 1종 = 8종.
5. 계획서 = 표준 11-section. **챕터 안 Phase 분할 → Phase 위해 step 분할 → step 전체 단조 누적.**
6. **매 Phase = result 문건 + ledger 갱신**(컴팩션 환각 방지). sub-agent 결과 대화에만 두지 말 것.
7. LaTeX 설치 + 한글 안깨짐 + PDF. → MiKTeX 설치·Ch1 PDF 빌드 완료.
8. **★ 미반영(다음 최우선)**: Ch1 PDF 보니 수식에 "약간의 건너뜀". **내용=리뷰논문 깊이 유지, 전개=학부 교과서 무생략 논리**. 유도 중간단계 전부.
9. **미착수**: Codex 스킬(`/codex:review`·`/codex:adversarial-review`) 의견 + 서브세션 `/codex:rescue` 로 Codex 작성 비교.

**완료 작업(디스크·커밋 확정, 마지막 커밋 7e238e9)**:
- RB Phase 0(step 1–16): `RB_CHARTER.md`·`RB_REFERENCES_DOSSIER.md`(DOI 30종 web검증; macdonald2000→svare2000 저자정정, funabiki ea+jes)·`RB_AL_MASTER.md`(AL-1~63).
- RB Phase 1(Ch1, step 17–42): `graphite_ica_ch1_rebuilt.tex`(562줄, 무결성 PASS). 적대검증 49 findings 전건 수정.
- MiKTeX 설치 + Ch1 PDF: `Claude/results/graphite_ica_ch1_rebuilt.pdf`(11p, 한글 OK, undefined ref 0).

## 2. 다음 세션 할 일 (우선순위)

**A. Ch1 무생략 감사 결과 회수** — 워크플로 `vt7ycbnsd`(run `wf_8f6d8c0c-d80`) = "Ch1 학부 무생략 감사"(구간 A/B/C 3 agent) 백그라운드로 띄웠음. 결과 회수 가능하면 회수, 안 되면 재실행. skip 후보(적대검증 LOW서 식별): Stirling 배열엔트로피(logistic), keystone 1차 선형화 대수, dr/dq ODE 적분, 차원 A=C/s 치환, L_of_G 지수부호 반전, spectrum 변수변환 미분.
**B. Ch1 무생략 보강** — A의 skip 을 본문에 채움(지시 8). 내용 깊이 유지, 중간단계 전부.
**C. Codex 교차검증(지시 9)** — `/codex:setup`→`/codex:review` or `/codex:adversarial-review`→서브세션 `/codex:rescue` 로 Codex 버전 작성·비교. Codex 산출물은 `Codex/` 영역, 비교용만.
**D.** Ch1 PDF 재빌드 → 사용자 검토 → Phase 2(Ch2, step 43).

## 3. 다음 세션 주의 (환경·복구)

- **작업 브랜치**: `rb-rebuild-2026-05-30`. main 머지·push 안 함(승인 전 금지).
- **계획서**: `Claude/plans/2026-05-30-undergrad-rederivation-rebuild-plan.md`(11-section, step 1–157).
- **복구 지점**: `RB_EXECUTION_LEDGER.md`. 컴팩션 시 이거+해당 result 직접 Read 후 작업(추정 금지).
- **LaTeX 빌드**: xelatex = `C:\Users\lksz1\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe`. AutoInstall ON. `-output-directory=Claude\work\build`, 2-pass. PDF는 `Claude/results/`로 복사해 링크. 한글=kotex+malgun(설치 불요). MiKTeX 업데이트 경고 무해.
- **5-30 경고**: 폰 작업물에 논문 미입각 가정 잠재 → grounding 감사 1차 임무, 폰 "통과" 자기보고 불신.
- **host 파싱 교훈**: 워크플로 JSON 을 cp949/요약잘림으로 오판 2회 → UTF-8 파일로 전건 파싱 후 집계.
- **어제 사고**: 5h 제한 직후 첫 핸드오버 Write 가 토큰 끊김으로 미저장(본 문서가 재작성판). Ch1 tex·PDF 실체는 무손상.

## 4. Chain 헤더 (누적)
- HANDOVER_RB_2026-05-31 — RB Phase 0~1 완료, Ch1 무생략 보강 + Codex 비교 대기.
