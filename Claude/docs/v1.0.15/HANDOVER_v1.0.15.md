# HANDOVER v1.0.15 — 이산 전압 격자 완전 퇴출(점별 연속 아키텍처) + Ch2 발열 상세화 + Fable 물리 6종 검토

## ④ Chain 헤더 (거슬러 올라갈 위치)
- **본 handover** = `docs/v1.0.15/HANDOVER_v1.0.15.md` (v1.0.15 완결)
- 받은 handover = `docs/v1.0.14/HANDOVER_v1.0.15_KICKOFF.md` (Fable 작성, 킥오프)
  - ← `docs/v1.0.14/HANDOVER_v1.0.14.md` ← `docs/v1.0.13/HANDOVER_v1.0.13.md` ← `docs/v1.0.10/HANDOVER_v1.0.11.md` ← …
- 마스터 계획 = `Claude/plans/2026-07-05-v1015-code-doc-sync-master-plan.md`(rev.2, GO 2026-07-05). 레저 = `Claude/results/process/V1015_EXECUTION_LEDGER.md`. Phase 결과 = `V1015_P{1..7}_RESULT.md`.

## ① 본 세션 지시·작업 요약
**지시**(사용자): Fable 킥오프 2문건을 기준으로 v1.0.15 = 이산 전압 격자를 **아키텍처에서 완전 퇴출**하고 점별 연속 메모리 적분으로 전환. Ch1·Ch2·코드 3축 동등·양방향 동기("코드에 없는 내용 X + 문건 내용은 코드에 반영"). 세 최우선 = ①교과서 register ②논문 깊이 ③수식-주도. 격자 재작성 = 9종 체리피킹(9,9,1,1)·이전 버전(v1.0.14 Fable) 비교 베이스. Fable 물리 논리 = 기본 무수정·6종(Codex3+Opus3) union 검토→보고(Decision Gate). 그림 = 상한없이 콘텐츠 기반. 골든 = **검사 후** 재캡처. dead·격자 param 삭제. **끝까지 자동 완료**(팝업 없이).

**완주(P1–P7, 전건 커밋·push)**:
- **P1 앵커·증판**(8de5157): docs/v1.0.15 증판·baseline gate green·격자 맵·인벤토리.
- **P2 Fable 물리 6종 검토**(3e6a3ce): 3 Opus 전원 확정 CRIT/HIGH 물리결함 0(근접정답 확증). 물리오류 1(P2-1 Sommerfeld Mott 오귀속·Codex 발견)·완결성 갭 3(P2-2/3/4). Decision Gate 승인.
- **P3 Ch1 격자 퇴출**(2325321): 9종 드래프트 경쟁→체리픽. §1.3·§1.9 재작성, 신설 eq:memory/lag/tail-limit/reversal·제거 eq:branch/vwork/lowpass. P2-1/3/4(Ch1). 검수 2R(물리결함 4·D1 누출 4·정합/문체 8 수정→수렴). 58p.
- **P4 Ch2 발열 상세화**(da83d03): worked example 신설·P2-2·P2-4(Ch2). 검수 6결함 수정. (★worked example 수치는 P7 에서 코드-정합 정정 — 아래 ②.)
- **P5 코드 점별 재아키텍처**(03dab92): dqdv 점별화(V_work·역보간·_causal_lowpass·ν 스위치 제거)·신설 _causal_memory_pointwise·dead 삭제(func_U_j_hys·_causal_lowpass)·격자 param 5종 제거. **골든 6종 게이트 검증 후 재캡처**. 적대 리뷰 3결함 수정. 회귀·다운스트림 PASS.
- **P6 그림 좌표 재검산**(56a1116): fig:reversal·relaxode 점별 재산출(격자 아티팩트 제거). 개념 도식 정합.
- **P7 검수·마감**(본 커밋): **문건↔코드 sync 정정**(worked example)·3대 무결 게이트·HANDOVER·INDEX.

## ② 다음 세션 주의 (★중요)
1. **staging `'w'`+`'n'` 중복 키**: `GRAPHITE_STAGING_LIT` 각 전이가 `'w'`(12-20mV)와 `'n':1.0` 을 둘 다 가짐. 코드 `_n_factor` 는 `'n'` 우선 → **실제 폭 w=RT/F=25.7mV**(전 전이 동일), `'w'` 미사용. two-phase 협폭(12-20mV)이 의도라면 `'n'` 제거·`'w'` 활성 필요 — **물리 설계 결정·골든 영향**이라 무단 변경 X, 사용자 판단 대기. (P7 에서 worked example 을 코드 실제값 w=25.7mV·완전식으로 정정: U_oc 74.4mV·∂U/∂T −0.204·ΔS −19.7·q_rev +60.8.)
2. **골든 = 점별 산물**: `golden_graphite_ref.npz` 는 v1.0.15 점별 코드로 재캡처됨(equilibrium bit-exact 앵커·dqdv 는 interp 아티팩트 제거로 구판 대비 ~2e-5 변화). 코드 수정 시 검증 후 재캡처(6종 게이트: 평형앵커·L→0=평형·기억적분 해석검산·Δ→0·면적보존·방충 mirror).
3. **v1.0.14 동결·폴백**: 문제 시 v1.0.14 로 복귀(사용자 명시). 이력 전건 보존.
4. **수치 가드 `_LAG_RESOLVE_DECAY_CAP=40`**: dqdv 미해상(a>40) 시만 평형 극한(물리 분기 아님·D6). 기본 staging L_V~1e-8 이라 항상 평형(interp 없는 직접 평가).

## ③ 미완료/이월 (실데이터·후속 소관, v1.0.15 범위 밖)
- 다온도 $T^2$ 실측 곡률·two-phase 폭 $T$-의존 round-trip 확정(config 몫)·LCO $\Omega^\mathrm{cat}$/$\Delta H_a$ 실값·ν≳10 실측·서지 재확인. 전부 실데이터 필요(계획 §3 이월).
- staging 중복 키 정리(②-1, 사용자 판단).
