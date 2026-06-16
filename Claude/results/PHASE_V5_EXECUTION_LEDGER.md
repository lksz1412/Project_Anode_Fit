# PHASE V5 EXECUTION LEDGER — Ch1 수식-구동 v5

> 계획서 = `Claude/plans/2026-06-17-ch1-v5-equation-driven-plan.md`. 원천 = `graphite_ica_ch1_Opus_v4.tex` §1.1~§1.17. 산출 = `graphite_ica_ch1_Opus_v5.tex`. 스타일 스펙 = `Claude/work/v5_session/v5_design_spec.md`.

| Step | Phase | Unit/Round | Action | Files | Read Range | Build | Defects(found/fixed) | Lens/Chunk | Gate | Commit | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.0 | 정독 | master v4 §1.1~§1.17 전문 정독 | v4.tex | 83–2743 (전 범위) | — | — | 구조·equation chain | 절 지도 18절 확정 | — | §1.1~§1.17 포함, §1.18 배제 확정 |
| 2 | 1.0 | 설계 | 스타일 스펙 작성(prose-strip+verbatim 식) | v5_design_spec.md | — | — | — | — | KEEP/DROP/PROMOTE 규칙 | — | 변환철학=산문벗기기 |
| 3 | 1.0 | 검수 | 설계 검수 sub(refute) | spec + v4 §1.4·§1.15 | 665–825·2223–2522 | — | 6/— (C1·H2·M3) | 설계 적대 | dangling ref 적발 | — | sub a7687f18 |
| 4 | 1.0 | 확정 | 검수 반영 — 스펙 §7.5 추가 | v5_design_spec.md | — | — | 6/6 (반영) | — | Gate 1.0 PASS | — | 보존·승격 항목 명시 |

| 5–9 | 1.1 | 초안 | 5 작업 sub 병렬 드래프트(그룹 A~E) | (drafts→master) | A:261–664·B:664–1048·C:1048–1442·D:1442–1915·E:1915–2743 | — | 승격 6(A:1→inline 환원, D:5) | 식 verbatim+산문 strip | Gate 1.1 PASS | — | 5 sub opus, §7.5 특별항목 처리 |
| 10–15 | 1.2 | 통합 | master 직렬 통합(preamble+서론+staging+§1.1~§1.17+bib 19) | v5.tex | — | — | eq:v5-notation-1 중복 inline 환원 | 절별 직렬 | — | — | 공유파일 직렬 쓰기 |
| 16 | 1.2 | 빌드 | xelatex 2-pass | v5.tex→v5.pdf | — | GREEN 40p | undefined 0·overfull 0 | cross-ref 해소 | **Gate 1.2 PASS** | (커밋) | 17절 확인·§1.18 누출 0 |

## Next Step
Phase 1.3: N회 가변-청크 검수(R1~, 수렴 2×0). 매 라운드 청크·렌즈 전환. 검수 sub 병렬→master 삼각검증·직접수정.

| 17 | 1.3 | R1 | 식 충실성 적대 검산(6 sub, 절별) | v5.tex | v5 전체↔v4 §1.1~§1.17 | GREEN 40p | 식오류 0 / 승격식 5 무번호화·참조 2 inline | 식 1:1 / 절별 | R1 PASS | (커밋) | 코드주석 (1.x) 정합 복원·검증 |

## Phase 1.3 R1 결과 (식 충실성)
- 6 sub 전원: 전 numbered 식·boxed·align·figure TikZ·Python 코드(문자 일치)·표(S0–S5/진단/참조표8/gap표) **v4와 1:1 verbatim 확정**. 식 변형·부호·첨자·누락 **0**.
- §1.18 누출 0(sec:stacking grep 0), dangling 종속절 삭제 확인, 심볼표 §1.18 5행 삭제 확인.
- §7.5 특별항목 전부 반영: eq:affinity 이중계상 논거·eq:chisum ∀𝒜 양화·두경로 verifybox·(3')M4 수치(5%/3RT/w/3/+0.07→+0.03)·울타리 ①–⑯(③⑨⑩ 삭제) 보존.
- keybox 전면 삭제 = 의도된 설계(스펙 §1, 핵심 결론은 식 흐름에 보존) — 결함 아님.
- **수정(R1)**: 승격식 5개(eq:v5-*) 무번호화(equation*) → v5 식번호 v4 정렬 복원 → §1.17 코드 주석 하드코딩 (1.x) 유효 유지(9/9 검증: vapp=1.45·logistic=1.27·chisum=1.21·affinity=1.19·cbg=1.43·lnLq=1.69·simplefit=1.79·hysdU=1.88·hyscenter=1.91·hysmaster=1.96). 미참조 label 문제 동시 소거. 재빌드 undefined ref 0·overfull 0.

## Phase 1.2 Gate 1.2 결과 (확정)
- xelatex 2-pass exit 0, 40 페이지.
- undefined reference/citation **0** (전 \eqref·\ref·\cite 해소).
- Overfull \hbox **0**.
- 절 수 = **17**(§1.1 notation ~ §1.17 code), §1.18(sec:stacking) 배제 확인(본문 누출 0, preamble 주석만 범위 명시).
- 승격 식 5개(eq:v5-overlap-1/potbranch-1/potbranch-2/synth-1/tempbranch-1) — 전부 앞 도입·뒤 사용.

## Phase 1.0 결함 요약 (검수 R0)
- C1: §1.16 줄 2579 `\S\ref{sec:stacking}` dangling → sub5 종속절 삭제 (스펙 §7.5).
- H2: §1.4 eq:affinity 이중계상 논거 산문-only → 승격 (스펙 §7.5).
- H3: eq:chisum ∀𝒜 양화 산문-only → 식 조건 보존 (스펙 §7.5).
- M5: §1.15 (3')·M4 수치 G-usable → 보존 의무 (스펙 §7.5).
- M6: keybox ①–⑯ 보존/축약/삭제 분류 채택 (스펙 §7.5).
