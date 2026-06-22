# Ch1 v5 전면 재검토 (V5RR) — MASTER ROADMAP

> 본 문서 = **마스터 플랜(로드맵)**. 각 Phase 착수 시 별도 **상세 플랜**(`2026-06-22-ch1-v5RR-phaseR{n}-plan.md`)을 세우고, step 마다 result 저장, Phase 끝마다 commit+push. [[feedback_plan_template_11sections]] 11-section 양식.

## 1. Summary

사용자 지시(6-22, 출근 전 GO·무중단): 지금까지 진행된 **v4·v5 전 내용을 최고 공들여 재검토**한다. 핵심 4요건:

1. **기준 = v3(Fable, 비활성된 최고 등급 모델 작성본).** v3 §1.1~§1.17 = 진실 원천·동결.
2. **v4·v5 진행 중 변동된 부분을 물리·화학·수리적으로 최대한 빡세게 검토.**
3. **수식-구동 포팅본 v5 의 완성도 제고.** 검수는 **(a) 절별 청크 루핑** + **(b) ★수식별 루핑** 둘 다 — 식 N 이 *관련된 모든 선행식*(직전이 아니라 그 식이 의존하는 전 선행식)으로부터 물리·화학·수리적으로 타당하게 전개됐는지 집중 검증.
4. **§1.18(적층 준안정) 이번에도 배제.** 더 좋은 모델 재개방 시 별도.

편집 대상 = **v5.tex 만**(v3·v4 불가침). 재검토에서 발견한 확정 결함은 master 가 v5 에 직접 수정. **이전 V5 "수렴" 주장을 신뢰하지 않고 fresh 전면 재검증**(baseline 에서 이미 overfull 2 적발 — §6).

## 2. Current Ground Truth (6-22 직접 검증)

- HEAD `b680d04` (V5.R8), branch `rb-rebuild-2026-05-30`.
- 파일: `graphite_ica_ch1_Fable_v3.tex`(97 eq, 동결) · `graphite_ica_ch1_Opus_v4.tex`(103 eq = 97+§1.18 6, 불가침) · `graphite_ica_ch1_Opus_v5.tex`(97 eq, **편집 대상**).
- v5 절 지도(직접 grep 확정): §1.1 sec:notation(L233) / §1.2 sec:rate(286) / §1.3 sec:thermo(356) / §1.4 sec:fwdrev(499) / §1.5 sec:regsol(601) / §1.6 sec:charge(750) / §1.7 sec:eqpeak(836) / §1.8 sec:lag(884) / §1.9 sec:potbranch(998) / §1.10 sec:tempbranch(1056) / §1.11 sec:synth(1157) / §1.12 sec:overlap(1263) / §1.13 sec:hys(1319) / §1.14 sec:hyspol(1429) / §1.15 sec:master(1517) / §1.16 sec:falsify(1707) / §1.17 sec:code(1745). §1.18 **부재**(배제 정합).
- **v5 빌드 현황 = FAIL**: err 0 / **Overfull 2** / undef 0 / 40p. 위치 ① 본문 L979–981(§1.8 꼬리 영역) ② L1836–1840(§1.17 코드검증 표). comment_gate 15/15 ok.
- v3↔v4 diff: 버전마커(2/26/28) + §1.1 기호표 §1.18용 6행(323a) + §1.16 포인터(2572c) + §1.18 절(2735a) + bib 6(2755a). → **§1.1~§1.17 본문 식·논리는 v3≡v4**(§1.18 부속만 추가). 따라서 "v4 변동분"의 실체 = §1.18(배제) + v5 의 수식-구동 변환.
- 작업트리에 과거 중간 산출물(`_body_ch*_v2.tex`·`*_rebuilt.tex` 등) deletion 다수 미스테이징 — **내가 만든 것 아님 → 명시 경로 스테이징으로 회피, 손대지 않음.**

## 3. Phase Range

| Phase | 이름 | 핵심 산출 | 주체 |
|---|---|---|---|
| **R0** | Baseline & 의존 그래프 | (a) 빌드 결함 목록 (b) v5↔v3 식 97개 1:1 대응·변동표 (c) ★식 의존 그래프(각 식의 선행식 집합) (d) §1.18 누출 점검 (e) 변환 변동(승격 5식·산문제거·figure) 인벤토리 | master + 매핑 sub |
| **R1** | 절별 루핑 (절=청크) | §1.1~§1.17 절별 물리·화학·수리 건전성 + v5↔v3 보존 + 절내 정합(산문제거가 논리 안 끊음) | 검수 sub ×5(병렬) → master 삼각·수정 |
| **R2** | ★수식별 루핑 (식=청크) | 식 N 각각을 *관련 모든 선행식*에 대해 적대 재유도 — 물리·화학·수리 전개 타당성·부호·차원·극한. 의존 그래프 클러스터 분담 | 검수 sub ×최대6(병렬) + Codex 교차 → master 삼각·수정 |
| **R3** | N회 가변-청크 수렴 | 렌즈 로테이션(G-follow/시각/부호·차원/완결성·orphan/인용-사실/회귀) 연속 2R 0결함까지 | 검수 sub 병렬 → master |
| **R4** | 최종 게이트·결과·commit | build 0/0/0 + comment 15/15 + render + v3·v4·.py 무손상 + RESULT/ledger | master |

Step 번호 Phase 넘어가도 단조 누적. R3 수렴 미달 시 step 연장([[feedback_step_granularity_flexibility]]). Phase 끝마다 commit+push.

## 4. Non-goals

- **§1.18 변환·검토 X**(범위 밖). **v3·v4(.tex/.pdf) 수정 X**(동결·불가침). **Codex/ read·write X**(경계).
- **새 물리·새 유도·새 결론 추가 X** — v5 의 *완성도 제고*(보존 정합·결함 수정·식 사슬 닫힘)만. 단 v3 가 산문으로 운반하던 유도 단계가 v5 에서 누락됐으면 *명시 중간식 승격*(새 내용 아님, 누락 복원).
- **Ch2~5 손대지 않음.** 공유 코드 `graphite_ica_model.py` 는 v5 §1.17 verbatim 과 바이트 정합 유지(임의 수정 X — 변경 시 verbatim 재동기·diff 게이트).

## 5. Implementation Changes (산출물)

- **수정** `Claude/docs/graphite_ica_ch1_Opus_v5.tex`(+ 재빌드 `.pdf`) — 결함 수정 누적.
- **신규** `Claude/results/PHASE_V5RR_ROUNDS_RESULT.md`(11항목) · `PHASE_V5RR_EXECUTION_LEDGER.md`(12-col). **기존 PHASE_V5_* 불가침**(덮어쓰기 X — 별도 문건, [[feedback_document_protection_addendum_pattern]]).
- **신규** Phase 상세 플랜 5종 + `Claude/results/V5RR_baseline_map.md`(R0 의존 그래프·대응표).
- commit: 명시 경로만(v5.tex/pdf·results·plans). `Codex/` 동반 커밋(수정 X). attribution 없음.

## 6. Phase 개요 (상세는 Phase별 plan 에서 확정)

### Phase R0 — Baseline & 의존 그래프
master 가 v5 전문 head→tail 정독으로 다음을 확정: (a) 빌드 결함(overfull 2 위치·원인) (b) **식 대응표**: v5 식 97개 ↔ v3 식 97개 — verbatim/변형 표시, 변형이면 무엇이 바뀌었나 (c) **★식 의존 그래프**: 식마다 "이 식은 식 (1.a),(1.b),… 에서 나온다" 선행식 집합 — R2 수식 루핑의 입력 (d) §1.18 누출(ψ·B·κ·ξ_c·stacking 기호·sec:stacking 참조) 0 확인 (e) v5 변환 변동 인벤토리(승격 중간식 5개·삭제 산문 유형·figure 목록). **Gate R0**: 97 식 전부 대응·선행식 배정 완료(미배정 0), 빌드 결함 목록화.

### Phase R1 — 절별 루핑
17 절을 5 그룹으로 검수 sub 병렬 분담(절당 head→tail 정독). 렌즈 = **물리·화학·수리 건전성 + v5↔v3 보존(누락·왜곡 0) + 절내 정합**(산문 제거 후에도 도입·전개·닫힘 유지, orphan 0). refute+가장약한1곳+빈통과금지. master 삼각검증 → v5 직접 수정 → 빌드 → ledger. **Gate R1**: 절별 보존 감사 PASS + 빌드 GREEN(overfull 0).

### Phase R2 — ★수식별 루핑 (핵심)
R0 의존 그래프 기반. 식 97개를 의존 클러스터로 묶어 검수 sub(최대 6) + Codex 교차 분담. 식마다: **(i) 물리** — 이 전개가 물리적으로 옳은가(예: 방전 시 V_n↑→탈리 진행↑→배리어↓). **(ii) 화학** — 반쪽반응·화학퍼텐셜·활동도 정의 정합. **(iii) 수리** — 대수 한 단계씩 재유도, 부호·차원·극한·근사 정당성. **(iv) 선행식 정합** — 인용한 선행식들과 변수·가정 일치, 숨은 flip/순환 0. master 삼각 → 수정 → 빌드 → ledger. **Gate R2**: 97 식 전부 (i)~(iv) 판정 + 확정 결함 수정·재빌드.

### Phase R3 — N회 가변-청크 수렴
매 라운드 청크·렌즈 전환(전체통독/라인/도메인그룹/v5↔v3대조/시각PDF). 직전 라운드 수정의 새 결함 사냥 포함. 연속 2R 0결함 → 수렴. **Gate R3**: 2×0 + coverage missing 0 + 빌드 GREEN.

### Phase R4 — 최종
build_gate Opus_v5 0/0/0 · comment_gate 15/15 · 변경 그림·페이지 렌더 · v3·v4·.py 무손상 diff · run_example PASS. RESULT 11항목 + ledger. commit+push.

## 7. Implementation Interfaces

### §A. 검수 sub prompt 표준 머리말 (4-세션 고지)
① 역할(검수 전담) ② 경계: **파일쓰기·commit·메모리 X — 결함 목록만 return**(master 가 통합·수정) ③ 범위밖 금지(§1.18·v3/v4/Codex 수정·새 물리 X) ④ 허위 attribution 금지 ⑤ self-contained(담당 절/식 줄범위·v3 대응 줄범위·의존 그래프 발췌). + refute mandate·가장약한1곳 필수·빈통과금지.

### §B. 의존 그래프 형식 (R0 산출)
`식번호 | label | 한줄 의미 | 선행식 집합 {(1.a),…} | v3 대응(verbatim/변형) | 도메인`. R2 가 이 행을 식별 단위로 소비.

### §C. ledger row (12-col, [[feedback_phase_execution_loop]])
`| Step | Phase | Unit/Round | Action | Files | Read Range | Build | Defects(f/fx) | Lens/Chunk | Gate | Commit | Note |`

### §D. RESULT 11항목
목표/범위 · 수행단계 · Read Coverage(절·식별) · 산출물 · 빌드 · 검수 라운드 추이 · 확정 결함·수정 · 4-tier(미해결/추정/미검증) · v3 대비 보존 감사 · Decisions · Next Step.

### §E. 모델·도구 매핑 ([[feedback_multi_session_orchestration]])
master = Opus(본 세션, 통합·수정·commit 전용). 검수 sub = general-purpose/Explore(Opus·Sonnet). 교차 적대 재유도 = Codex(`codex:codex-rescue`). **Fable 비활성** — 교차검증 = Codex + Claude sub. Workflow 미사용(문서작업·Agent 도구만 — [[feedback_flow_interruption]]).

## 8. Test Plan

- 빌드: `xelatex` 2-pass → build_gate Opus_v5 err/overfull/undef=0.
- 식 대응: v5 식 ↔ v3 식 1:1(97/97), 변형 식은 변동 사유 명시.
- 수식 루핑 판정: 식별 (i)물리/(ii)화학/(iii)수리/(iv)선행식 정합 yes/no + 끊기는 지점.
- 보존 감사: v3 의 numbered 식·boxed·표·figure·코드가 v5 에서 누락·왜곡 0(§1.18 부속 제외).
- 시각: `pdftoppm` 식 페이지 렌더(잘림·겹침 0).
- 무손상: v3·v4 `.tex` git diff 0, `graphite_ica_model.py` ↔ v5 §1.17 verbatim 정합.

## 9. Assumptions

- A1. "v4·v5 변동 검토" 실체 = §1.18 배제 하에 **v5 의 수식-구동 변환**(v3≡v4 §1.1~§1.17 확정). v3 가 물리 기준.
- A2. 편집은 v5 만. v3·v4 동결. v5 §1.1~§1.17 의 물리는 v3 기준으로 판정(v3 자체 오류 발견 시 4-tier "추정"으로 보고, 임의 수정 X — Decision).
- A3. "최고 공들여·빡세게" = N회 검수 수렴까지 + 수식별 전수. GO 무중단(팝업 0).
- A4. 코드 동작·수치 불변. v5 PDF 재빌드는 산출물 갱신(정상).

## 10. Decisions Required

> 추천 기본값 — 별도 지시 없으면 기본값으로 무중단 진행.

- **D1 — overfull 2 수정 범위.** 기본값: **R1 에서 즉시 수정**(식 줄바꿈·박스 폭 조정, 내용 불변). 근거: 게이트 GREEN 이 모든 라운드 전제.
- **D2 — v3 자체의 물리 결함을 발견하면?** 기본값: **v5 에 그대로 보존 + 4-tier "추정/미검증"으로 보고**(v3 동결·기준이므로 임의 정정 X). 사용자 확인 후 별도. 단 v5 *변환 과정에서 새로 생긴* 결함은 즉시 수정.
- **D3 — 승격 중간식 5개 처리.** 기본값: **무번호 equation* 유지**(식 번호 1:1 보존). 단 선행식과 논리 정합·orphan 0 은 R2 에서 전수 검증.
- **D4 — figure 처리.** 기본값: **v4 verbatim 유지**(범위 밖). 단 캡션 식 참조·라벨 충돌은 R3 시각 라운드에서 점검.

## 11. Correction History

- (최초) 본 마스터 플랜은 직전 V5(R1~R8)·V4R 트랙 **위에서** v5 의 전면 재검증 트랙을 연다. 직전 V5 "R7 수렴·overfull 0" 주장은 **현재 거짓**(R8 이 게이트 재확인 없이 overfull 2 유입) — 본 트랙이 fresh 재검증으로 재수립. 기존 PHASE_V5_* result/ledger 는 불가침(별도 PHASE_V5RR_* 신설).
