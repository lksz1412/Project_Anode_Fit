# PHASE_RADIUS_RESULT — dQ/dV peak→U_j 분포→반경 분포 추산 타당성 조사 (Result 11항목)

1. **Phase/범위**: 단일 조사 트랙(Phase 0 scope → Phase 1 4축 병렬 조사 → Phase 2 종합·삼각검증 → Phase 3 verdict). 계획서 = `Claude/plans/2026-06-30-radius-distribution-from-dqdv-peak-shape-survey-plan.md`.
2. **목표**: 사용자 추정("Ω≥2RT 단일입자 델타 → 실측 치우친 종모양 = U_j 분포 → 반경 분포 역산")의 물리 타당성·성립 조건을 1차 문헌으로 판정. 모델 수정·피팅 실행은 범위 외.
3. **수행**: master 가 `v8-11.tex`(핵심 절)·`v11_final.py`(func_w/w_eff/ksi_eq/peak) 정독으로 전제 grounding → 4축 general-purpose 서브 병렬 조사(web search + 카드 Write) → master 4카드 전수 정독·삼각검증 → `20_synthesis.md`·`RADIUS_VERDICT.md`.
4. **산출물**: `00_scope.md`·`10`·`11`·`12`·`13`(축별 카드)·`20_synthesis.md`·`RADIUS_VERDICT.md`·본 RESULT·`RADIUS_LEDGER.md`·`50_report.md`.
5. **핵심 결과(4-tier)**:
   - [확정] 단일입자 Ω>2RT 평형 = Maxwell plateau → dQ/dV 델타(사용자 전제 맞음, 평형 극한). 고전류·일부 전이(4L-3L)는 예외.
   - [확정] 역변환 peak→분포 = 1종 Fredholm ill-posed(DRT 동형), 정규화/형태가정 필수.
   - [추정·1/r 확정] ★마이크론 흑연 반경→U_j ≈ 0.01–0.05 mV ≪ peak 폭(수십 mV) → "U_j 분포=반경 분포" 마이크론서 정량 무효. 큰 효과는 나노(<~50nm)만.
   - [확정] 실측 치우침은 kinetic 분극(~70 mV, C-rate 의존)이 지배 — 반경 분포는 GITT 잔여 폭 상한 안에서만.
   - [근거미발견] 흑연 staging 전위의 평형 입경 의존 직접 측정·dQ/dV→PSD 직접 역변환 선례.
6. **판정**: **부분 타당·조건부.** 직관(델타의 ensemble 퍼짐)은 옳으나, 반경 고리가 마이크론서 무효 + 역문제 ill-posed + kinetic 지배. 현 형태(마이크론·반경단독·직접 deconvolution)로는 불성립. 6개 성립조건(근평형·나노·입자독립·반경지배·전이격리·정규화+독립PSD) 동시 충족 시 부분 의미.
7. **검증/Gate**: 4카드 master 직접 정독(sub 요약 비신뢰)·핵심 주장 ≥2 독립 삼각검증·역문제 사슬 5고리 충족/미충족 정직 판정·경쟁가설 매트릭스 분리신호(C-rate) 제시·핵심 정량(반경 mV·kinetic mV·임계반경) 출처 검증.
8. **한계**: Nature/Springer 본문·ScienceDirect 403 다수 abstract/snippet-only(해당 카드 tier 강등 명시). 흑연 평형 입경 의존·흑연 γ 실측·잔여폭 분해는 공백(열린 문제). 본 조사 = 해석 타당성 판정, 실데이터 분리 실측은 미수행.
9. **사용자 의도 정합**: "타당한가·어떤 조건서 맞나" 직접 답(verdict §1·§3). research/radius 폴더 작성 완료. 글로벌 CLAUDE.md(병렬 목적적·Workflow 금지·4-tier·추측 0·DOI 병기)·11-section 계획·project CLAUDE.md(Codex read 회피·원본 불가침) 준수.
10. **다음 단계 권고**: (실측) C-rate 사다리+GITT 로 kinetic/잔여 분리 → 독립 PSD 상관 검정 → 단일입자 dQ/dV 상한. (모델) 분포 항 도입 시 반경 단독 아닌 일반 U_j 이질성 + C-rate 식별구속(교수님 검토 후, 범위 외).
11. **상태**: 조사·종합·verdict 완료. 미해결 = 열린 문제 4종(흑연 평형 입경의존·δ⊛분포 직접피팅·dQ/dV→PSD 선례·반경→U_j mV 환산) — 전부 "근거미발견"으로 정직 분류, 추정으로 메우지 않음.
