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

| 18 | 1.3 | R2 | G-follow + 산문바닥선 + 커넥터(2 sub, 전체통독) | v5.tex | v5 전체 | GREEN 40p | 3/3 (regression 복원) | G-follow / 전체통독 | R2 PASS | (커밋) | 17절 중 14 통과, 끊김 §1.5·§1.15 집중 |
| 19 | 1.3 | R3 | PDF 시각 렌더(2 sub, p1-20/21-40) | v5.pdf | 40p 이미지 | GREEN | 0 (v5 범위) | 시각 / 페이지 | R3 PASS | — | fig:chain 클린·코드·표·한글 정상; MED/LOW는 verbatim-v4 figure 미관(범위 밖) |
| 20 | 1.3 | R4 | 기호/xref + 물리 적대재유도 + 완결성/회귀(3 sub) | v5.tex | v5↔v4 / 척추식 | GREEN 40p | 2/2 (③ dangling·mosaic) | 물리재유도/기호/완결성 | R4 PASS | (커밋) | 척추 10식 물리정합 0결함 |

## Phase 1.3 R2 결과 (G-follow/산문)
- G-follow: 17절 중 14절 "수식만으로 따라가짐" 통과. §7.5 전부 보존·커넥터 0 misstatement·전보체 재발 0·97식 1:1 재확인.
- **수정(R2, 전부 v4 회귀 복원)**: ① §1.5 eq:gprime forward 참조에 "아래" 복원(v4는 "아래 식"으로 명시했음) ② §1.5 eq:gxi 도입에 떼는 1차몫 정체(기준 잔여 $-\mu^0\xi$+전기 일 몫 ∝ξ, eq:emu)·불변 근거 복원 ③ §1.6 다가성 문단 기울기 명시식·조건(<0)으로 압축. 새 numbered 식 추가 0(번호 정합 보존).

## Phase 1.3 R3 결과 (시각)
- p21–40 완전 PASS(fig:chain 6박스 클린, boxed 다줄식·표·Python 코드·한글·울타리 원문자 정상 렌더).
- p1–20: MED 1(fig:isofamily x축 라벨–곡선 근접) + LOW 2(fig:doublewell tick 근접·심볼표 단위 wrap) — **전부 verbatim-v4 figure**(R1에서 1:1 확인, v4 PDF render-verified·승인). 스펙 D3(figure verbatim) + R1 fidelity상 그림 TikZ 수정은 v4 이탈·범위 밖 → 조치 안 함(pre-existing 미관).

## Phase 1.3 R4 결과 (물리/기호/완결성)
- **R4b 물리 적대 재유도: 척추 10식(eyring→mu→logistic→weff/spinodal→Lq/tail→keff/LqV→arrhenius→hysdU→hysobsgap→areacons) 독립 재유도로 차원·극한·부호 전부 정합 — 결함 0.** eq:hysdU artanh 부호·eq:dHeff χ_d 흡수 검증.
- R4a: §1.18 잔재 0·코드 식번호 정합·부호 일관성 clean. b_j/u_j/T_*/ΔH_eff 심볼표 행 부재 = **v4 심볼표 그대로 물려받음**(v4도 없음, ref표(8)·정의지점에 존재) → verbatim-보존 스펙상 범위 밖, 조치 안 함.
- **수정(R4)**: ① §1.15 keybox에서 삭제했던 ③⑨⑩ 복원 — 본문 "울타리 ③"(§1.10) dangling 참조 해소 + ①~⑯ 완비(gap 제거). ② §1.5에 "공존 plateau는 단일 평균장 정지점이 아닌 다입자 앙상블이 받침" load-bearing 단서(v4 keybox에서 증발) 1문장 복원. 재빌드 GREEN.

| 21 | 1.3 | R5 | 신선 적대 완결성 + 회귀/응집 + P3 게이트(2 sub) | v5.tex | v5 전체 | GREEN 40p | 1/1 (문법 truncation) | 완결성/회귀/P3 | R5 PASS | (커밋) | 달성도 97%·R5b 회귀4+P3-5 전부 PASS |

## Phase 1.3 R5 결과 (완결성/회귀/P3)
- **R5b: 회귀·응집 4항목(R1 무번호화 5곳·§1.5 3중수정 응집·keybox ①~⑯ 완비·§1.6 다가성) 전부 PASS + 프로젝트 P3 게이트 5항목(V전위 구분·전하보존 중심식·순환 미분경로·기준식 사슬·ver.N 혼동) 전부 PASS. 확정 결함 0.**
- **R5a 신선 적대(달성도 97%)**: 물리·수치(25.7mV·55mV·gapT 9값·binodal/spinodal·0.07 등)·기호·식번호(97식 카운터 에뮬 1:1)·인용 전수 검산 통과. **수정 1건**: §1.2 prefactor 문장 "…때문이며(…)." 연결어미 truncation → v4 의도대로 완결 문장 복원("…때문이다 — 이 흡수가 … 전략의 근거다"). LOW 2건(코드주석 (1.43) 선택·§1.5 조사)은 verbatim-v4/방어가능이라 무수정.

| 22 | 1.3 | R6 | 라인단위 micro-sweep + 홀리스틱 ship-check(2 sub) | v5.tex | v5 전체 | GREEN 40p | 1/1 (코드주석 (v3) 정리) | 라인단위/배포적격 | R6 PASS | (커밋) | MED 0·ship-with-minor; 달성도 88~97% |

## Phase 1.3 R6 결과 (라인/배포)
- R6a 라인 단위: 확정 문법/오타/매크로/조사 결함 **0**(R5 truncation 봉합 확인, 동일 유형 0). LOW 3건은 표기 선택지로 무수정.
- R6b ship-check: **SHIP-with-minor-fixes**. §1.18 잔재 0·cross-ref 무결·orphan 0·§1.4 HIGH 승격 안착 확인. **수정 1건**: §1.17 코드 헤더 주석 `Ch.1 (v3) 식의 직역 … §1.17 본문` → `Ch.1 식의 직역 … 본 절 본문`(v5 내 "(v3)" 버전 혼동 + 자기참조 정리; 코드 로직·식별자 무변경, 주석만). 사용자 메모리(인라인 코드 버전 라벨 지양)와 부합.

| 23 | 1.3 | R7 | 2차식·수치·인용 재검 + 누적회귀(2 sub) | v5.tex | v5 전체 | GREEN 40p | 0/0 | 보조식/수치/인용/회귀 | **수렴** | (커밋) | R6+R7 연속 0-확정결함 |

## Phase 1.3 R7 결과 + 수렴 (Gate 1.3)
- R7a: 보조식 전부 재유도·본문 수치 전수 재계산(k0·w·gapT 9값·binodal/spinodal·forward·Lq·σ_lnL·fuse비 등)·인용 19키 적합·미인용 bibitem 0·차원 전부 — **결함 0**.
- R7b: 누적 11 수정 전부 현존·정확·응집 확인. 식번호 v4 정렬 .aux 확정(eq:logistic=1.27·eq:hysmaster=1.96), 코드 (1.x) 전수 일치. 빌드 클린. **MED+ 확정결함 0 — 수렴.**
- **수렴 판정**: R6(LOW 코드주석 1건 수정)·R7(확정결함 0) = 연속 0-확정결함. 7라운드·~21 sub-pass, 결함 감쇠 R1:5→R2:3→R4:2→R5:1→R6:1→R7:0. **Gate 1.3 PASS.**

## Next Step
Phase 1.4: 최종 결과문건(PHASE_V5_RESULT.md) + commit. v5 완성 — 사용자 검토 대기.

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
