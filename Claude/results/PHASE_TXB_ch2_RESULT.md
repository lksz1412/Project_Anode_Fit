# PHASE 5 (부분) — Ch2 이해도 보강 + Codex 시정 Result

## Summary
박사님 "Ch2 전체 난해" 수용 → 난해 핵심(전체 그림·부호반전·분기선택·진짜/가짜 gap)에 직관 anchor. **진행 방식 정정**: 앞서 절 편집은 순서대로 했으나 검수(빌드)를 챕터 끝에 몰아 함 = 완전한 절 단위 루프 아님. 박사님 지적 수용 후 \emph{절마다 편집→빌드→정합→다음}으로 전환(§서론·§4 Codex 시정·§3·§5 각각 독립 빌드).

## Step Range
Steps 111–120 부분(Phase 5.1–5.2 핵심 절). §6~§11 clarity 는 동일 루프로 후속.

## Inputs
- `graphite_ica_ch2.tex`. 계획 `2026-06-09-textbook-depth-expansion-plan.md`. Codex(agent af58e41a).

## Files Updated (절별 루프)
- §서론: 과냉각/과열 비유(큰 그림) + Codex 시정(spinodal 상한·γ_j caveat) → 빌드 clean.
- §2.3: binodal=어는점·spinodal=과냉각 한계·준안정=과냉각된 물 대응.
- §4: 이중우물→비단조 V_eq loop 직관 + Codex 시정("내리는 구간=불안정 영역, 양 끝 점이 spinodal") → 빌드 clean.
- §3: 진짜/가짜 gap 직관 → 빌드 clean(독립).
- §5: 과냉각→방전/충전 spinodal 한계 직관 → 빌드 clean(독립).

## Read Coverage
- §서론(57–95)·§2.3(195–235)·§3(236–258)·§4(260–312)·§5(313–340) 정독·보강.

## Execution Evidence
- 절별 빌드: §서론+§4 Codex(exit0 0/0 11p), §3(exit0 0/0), §5(exit0 0/0).

## Validation (4-tier)
- **확정 PASS** — Codex(af58e41a) 신규 보강 검증: Ch1 worked example 수치 전부 정상(FWHM 91/78mV·높이 4.9/5.6·꼬리 12×), 3×3 칸별·겹침·walkthrough·진단표 정상; Ch2 §2.3·§서론 비유 정상. 2건 시정(§서론 과열 범위 caveat, §4 spinodal 영역/점 용어).
- **확정 PASS** — 절별 빌드 각 clean.

## Gate
**PASS(부분)** — 핵심 절(서론·§2·§3·§4·§5) 루프 완료. §6~§11 clarity 동일 루프 후속.

## Confirmed Non-Changes
- 정확 유도·식·라벨 불변. 단일문건 규율 유지.

## Open Issues / Decision Queue
- §6(dQdV)·§7(pol)·§8(memory)·§9(param)·§10(fit)·§11(master) = Phase 3 depth 보유, clarity 미세 보강 후속(동일 절 단위 루프).

## Next
- Ch2 §6~§11 절 단위 루프 clarity → Codex → 종합. (Step 121~)
