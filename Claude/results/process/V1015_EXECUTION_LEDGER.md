# V1.0.15 EXECUTION LEDGER — 이산 격자 완전 퇴출(점별 연속 아키텍처) + Ch2 발열 상세화 + Fable 물리 논리 6종 검토

> 마스터 = `../../plans/2026-07-05-v1015-code-doc-sync-master-plan.md`(rev.2, GO 2026-07-05). 방법론 = 검증 모델(코드→문건→코드·theory-first) + 스킬 `competition-cherrypick-authoring`. Fable 불가 → master·체리픽·최종·재검 = Opus·경쟁 N=9. v1.0.14 동결(037d859~8012a72) — 증판 = docs/v1.0.15/. 체리픽 비교 베이스 = v1.0.14(근접 정답). 상태 ⬜/🔄/✅.

| Phase | 이름 | Steps | 산출 | Gate | 상태 |
|---|---|---|---|---|---|
| P1 | 앵커·증판 | 1–4 | docs/v1.0.15·격자 맵·인벤토리 | 회귀 13/13·tex 0-err·demo/sample/suite | ✅ |
| P2 | Fable 물리 논리 6종 검토·보고 | 5–8 | V1015_P2_PHYSICS_REVIEW | union·단독 재검·보고(Decision Gate) | 🔄 보고완료·박사님 결정 대기 |
| P3 | Ch1 격자 퇴출 修正(theory-first) | 9–14 | ch1 연속형·R5 재유도 | 재검산·격자 grep 0·빌드 | ✅ 완주·수렴 |
| P4 | Ch2 발열 상세화(additive) | 15–19 | worked example·vib/elec·그림 위치 | 발열 완결·정합·빌드 | ✅ 완주 |
| P5 | 코드 개정(점별·dead 삭제·골든) | 20–27 | dqdv 점별·신규 골든 | 등가 3종·연속 천이·회귀 재정초 | ✅ 완주 |
| P6 | 그림 경연(9종·master=Opus) | 28–32 | 편입 그림 | 좌표 재검산·정합 | ⬜ |
| P7 | 검수(변경분)+최종 마감 | 33–37 | RESULT·HANDOVER·INDEX | 3대 무결·최종 게이트 | ⬜ |

## 진행 로그 (append-only)
- **2026-07-05 P2 검토·보고(Steps 5–8)**: 6종 독립 검토(Opus 3 R-O1/O2/O3 + Codex 3 R-C2/R-C3b/R-C1b, Agent 무통신·전문 정독 missing 0). Codex 3 중 2건 async→foreground 재기동으로 회수. **세 Opus 전원 확정 CRIT/HIGH 물리 결함 0**(재유도 전건 통과 — 박사님 "근접 정답" 확증). 교차합의 triage → **확정 물리 오류 1건**(P2-1 LOW: eq:Se Sommerfeld 보정 "g′(k_BT)² Mott" 오귀속 = 짝핵 패리티로 g′ 상쇄·첫 보정 g″(k_BT)³ — Codex 단독 발견·master 재유도 확정·Opus 3 미검) + **문서 완결성 갭 3건**(P2-2 MED two-phase config caveat 미전파[3종 공통]·P2-3 verifybox +80 라벨 모순[2종]·P2-4 vib T-무관 전제 미명시[2종]) + 공개 불확실 1(P2-5)·단독 강등/기각 3(R-C3b-1 major→LOW·R-C1b-2 P4 advisory·R-O2-2 기각). 산출 `V1015_P2_PHYSICS_REVIEW.md`(4-tier). **Decision Gate: P2-1~P2-4 수정 여부 박사님 결정 대기(기본 무수정).**
- **2026-07-05 GO**: 사용자 계획 rev.2 승인("계획서가 필시 지침 따랐을 것으로 믿는다. 시작하라") + 체리픽 비교 베이스 = v1.0.14 추가 지시 반영(rev.2 §6·P6). Fable 불가 확정.
- **2026-07-05 P1 완주(Steps 1–4)**: **S1** 증판 = docs/v1.0.14 소스 14개 → docs/v1.0.15 복제(빌드산물·HANDOVER 제외)·버전 태그 rename·기능적 경로 패치(v1.0.15 자립)·버전 문자열 정밀 패치(현행 선언만 1.0.15·이력 전건 보존, py 23·tex 14 literal 타깃). **S2 baseline gate green**: 회귀 13/13 bit-exact·ch1 0-err/57p/of>10 0·ch2 0-err/14p·appendix 0-err/8p·demo/sample/suite DONE(figs 재생성). **S3** 격자 의존 전수 맵(코드 4구역·문건 Ch1 10지점+가이드, 처분 초벌) = RESULT §6. **S4** dead(_causal_lowpass·func_U_j_hys) + essential 22 + 피팅 파라미터 인벤토리·제거 격자 param 4 = RESULT §7. 노트: appendix \date 편입문구 stale(P7 판단). 산출 = `V1015_P1_anchor_RESULT.md`. Gate 전 green. **커밋 예정**.
