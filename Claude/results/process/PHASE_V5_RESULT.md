# PHASE V5 RESULT — Ch1 수식-구동(equation-driven) v5

> 계획서 = `Claude/plans/2026-06-17-ch1-v5-equation-driven-plan.md` · ledger = `PHASE_V5_EXECUTION_LEDGER.md` · 스타일 스펙 = `Claude/work/v5_session/v5_design_spec.md`

## 1. 목표·범위
v4(`graphite_ica_ch1_Opus_v4.tex`)의 **§1.1~§1.17**을 산문 최소화·논리를 수식 사슬이 운반하는 "수식-구동" v5(`graphite_ica_ch1_Opus_v5.tex`)로 재표현. **§1.18(적층 준안정) 배제**. v4 불가침(신규 파일).

## 2. 수행 단계
- Phase 1.0 설계: master v4 §1.1~§1.17 전문 정독 → 변환철학(산문 벗기기: 식·figure·코드 verbatim 보존, 산문→커넥터, 산문-only 유도단계만 명시 중간식 승격) 스펙 확정 → 설계검수 R0(dangling 등 적발).
- Phase 1.1 초안: Agent 도구 **5 서브세션 병렬**(그룹 A~E 독립 드래프트, 파일쓰기 X). Workflow 미사용(글로벌 헌법 준수).
- Phase 1.2 통합: master **직렬 통합**(공유 파일) — preamble(v5)+압축 서론+staging figure+§1.1~§1.17+bib(19). xelatex 2-pass GREEN.
- Phase 1.3 N회 검수: R1~R7, 매 라운드 청크·렌즈 전환, 검수 sub 병렬(refute) → master 삼각검증·직접수정. **R6+R7 연속 0-확정결함 → 수렴.**

## 3. Read Coverage
- master 직접 정독: v4 §1.1~§1.17 전 범위(줄 83–2743) + bib(2884–2910).
- 검수 sub 누적: v5 전체를 절별·전체통독·라인단위·시각(PDF)·물리재유도·기호·인용 등 다중 청크로 cover(coverage missing 0).

## 4. 산출물
- `Claude/docs/graphite_ica_ch1_Opus_v5.tex` (신규), `…v5.pdf` (40p).
- `Claude/results/PHASE_V5_EXECUTION_LEDGER.md`, 본 RESULT.
- 작업파일 `Claude/work/v5_session/v5_design_spec.md`(gitignore — 미커밋).

## 5. 빌드 결과
xelatex 2-pass exit 0, **undefined reference/citation 0, Overfull hbox 0, 40 페이지**. (한글 italic 폰트 shape 치환 경고만 — 무해.)

## 6. 검수 라운드 추이 (Phase 1.3)
| R | 렌즈 / 청크 | 확정 결함(수정) |
|---|---|---|
| R1 | 식 충실성 적대(6 sub, 절별) | 5 — 승격식 무번호화(v4 식번호 정렬 복원, 코드 (1.x) 정합) |
| R2 | G-follow+산문(2 sub, 전체) | 3 — §1.5 forward 명시·1차몫 정체·§1.6 다가성 압축(v4 회귀 복원) |
| R3 | 시각 렌더(2 sub, PDF) | 0(v5 범위; figure 미관은 verbatim-v4·범위 밖) |
| R4 | 물리재유도/기호/완결성(3 sub) | 2 — keybox ③⑨⑩ 복원(dangling 해소)·§1.5 mosaic 단서 |
| R5 | 완결성+회귀+P3 게이트(2 sub) | 1 — §1.2 문법 truncation 봉합 |
| R6 | 라인단위+ship-check(2 sub) | 1 — §1.17 코드주석 (v3) 정리 |
| R7 | 2차식·수치·인용+누적회귀(2 sub) | 0 — **수렴** |
감쇠 5→3→2→1→1→0. 물리 적대 재유도(R4b 척추 10식) 0결함, 식 충실성(R1) 1:1 verbatim 확정.

## 7. 확정 결함·수정 (4-tier: 확정)
누적 11건 수정 전부 적용·재빌드·R7b 검증. (목록 = ledger R1~R6 행.)

## 8. 미해결/추정/미검증 (4-tier)
- **근거 미발견(결함 아님)**: 물리오류·부호·차원·수치 비일관·식 누락·dangling — 전수 검산서 0.
- **추정(범위 밖, 무수정)**: verbatim-v4 figure 라벨 근접/단위 wrap(R3 MED/LOW) — 스펙 D3(figure verbatim) + v4 render-verified 승인. 심볼표 b_j/u_j/T_*/ΔH_eff 행 부재 — v4 그대로 물려받음(ref표(8)·정의지점에 존재).
- **미검증**: 실독자 reading-test 미수행(검수 sub 범위 밖).

## 9. v4 대비 보존 감사
v4 §1.1~§1.17의 numbered 식 97개·boxed·align·figure TikZ·Python 코드(문자 일치)·표(S0–S5/진단/참조표8/gap표) **1:1 verbatim 확정**(R1 6-sub + R7a). §1.18 누출 0(sec:stacking·ψ·eq:xistack 등 0건). 승격식 5개는 산문-only 유도단계 명시화(equation*, 무번호).

## 10. Decisions 반영
D1(§1.1~§1.17/§1.18 배제)·D2(코드 유지)·D3(figure 유지)·D4(식 사이 한 줄 커넥터)·D5(5 병렬+master 직렬) 전부 기본값대로. P3 게이트 5항목(V전위 구분·전하보존 중심식·순환 미분경로·기준식 사슬·ver.N 혼동) PASS.

## 11. Next Step
v5 완성. **사용자 검토 대기** — 추가 피드백(예: D2/D3/D4 강도 조정, 특정 절 추가 축약)이 있으면 그 위에서 증분 작업. Ch2~5는 본 작업 범위 밖.
