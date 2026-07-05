# V1.0.15 P7 RESULT — 변경분 검수 + 문건↔코드 수치 대조 + 최종 마감

> 마스터 = `../../plans/2026-07-05-v1015-code-doc-sync-master-plan.md`(rev.2) P7(Steps 33–37). 상태 = ✅ 완주(3대 무결).

## 1. ★문건↔코드 수치 대조 (P7 핵심 발견·정정)
Ch2 worked example(P4) 을 코드 `entropy_coefficient` 와 대조하다 **불일치 발견**:
- **원인**: `GRAPHITE_STAGING_LIT` 는 `'w'`(0.020/0.016/0.014/0.012)와 `'n':1.0` 을 둘 다 가지며, 코드 `_n_factor` 는 `'n'` 우선 → **실제 폭 $w_j=RT/F=25.7$ mV**(전 전이 동일), `'w'` 폴백값은 미사용. 그런데 P4 worked example 은 폴백 폭(12-20mV)을 폭으로 써 코드와 어긋났다(폭·단순식/완전식 둘 다).
- **정정(코드 = ground truth)**: worked example 을 코드 실제값으로 재산출. $\bar x{=}0.25$: $U_\oc$ **82.4→74.4 mV**, $\partial U/\partial T$ **−0.152(단순식)→−0.204(완전식)** mV/K, $\Delta S$ **−14.7→−19.7** J/mol·K, $\dot Q_\rev/I$ **+45.4→+60.8** mV. 열적 폭 $n{=}1$ 이라 config 항 활성 → **완전식이 코드값**이고, **round-trip FD=완전식=−0.204**(파생 A 정합; 이전 P4 의 단순식/완전식 round-trip 혼선 해소). tab:worked(폭·config 열 갱신)·tab:qrev(5-SOC 코드값)·(a)-(e)·캡션 전면 정정. 단순식 −0.134 은 config-free 하한으로 병기.
- **검증**: 코드 `entropy_coefficient(U_oc)` = 해석 완전식 = 유한차분 FD = **−0.204**(3경로 일치, 0.000 μV/K). 부호(ΔS<0·방전 발열)·q_rev=−IT∂U/∂T·SOC 부호 교대 전건 코드 정합.

## 2. 3대 무결 최종 게이트 (검증 증거)
| 스트림 | 빌드/실행 | undefined | of>10pt | 규모 |
|---|---|---|---|---|
| Ch1 (graphite_ica_ch1) | xelatex 2-pass exit 0 | 0 | 0 | 58p |
| Ch2 (graphite_ica_ch2) | xelatex 2-pass exit 0 | 0 | 0 | 16p |
| appendix (phase_separation) | xelatex 2-pass exit 0 | 0 | 0 | 8p |
| 코드 (Anode_Fit_v1.0.15) | 회귀 verify | GRAPHITE 0-DIFF PASS | — | 13/13 + 게이트 6종 |
- 다운스트림 demo/sample/suite/plot 전부 exit 0(P5).

## 3. 변경분 검수 (P3–P6 통합 정합)
- **격자 퇴출 일관성**: Ch1(§1.9 점별 서술)·코드(dqdv 점별)·그림(reversal/relaxode 점별 재산출) 三者 정합. 격자 용어 렌더링 grep 0·live 코드 잔재 0.
- **P2 승인 수정**: P2-1(Ch1 Sommerfeld)·P2-3(verifybox +80)·P2-4(Ch1·Ch2 vib T-무관)·P2-2(Ch2 use-this caveat) 반영 확인.
- **문건↔코드 sync**: worked example(§1) 정정으로 Ch2 수치 = 코드. fig:reversal/relaxode(P6) 좌표 = 코드. Ch1 §1.9 식 = 코드 dqdv 알고리즘(eq:lag/tail-limit/reversal).
- **어투·D1**: changelog-메타·내부라벨(P6/구판/이전 판) 렌더링 잔재 0(P3·P4·P6 검수 누적).

## 4. 산출·마감
- **HANDOVER**: `docs/v1.0.15/HANDOVER_v1.0.15.md`(chain: HANDOVER_v1.0.15_KICKOFF ← v1.0.14 ←…).
- **INDEX**: `docs/INDEX.md` v1.0.15 행 갱신.
- **레저**: `results/process/V1015_EXECUTION_LEDGER.md` P1–P7 전건 ✅.

## 5. 미결/이월(실데이터·후속 소관)
- 다온도 $T^2$ 실측·two-phase 폭 $T$-의존 round-trip 확정(config 몫)·LCO $\Omega^\mathrm{cat}$/$\Delta H_a$ 실값·ν≳10 실측·서지 재확인 — 전부 실데이터 소관(v1.0.15 범위 밖, 계획 §3 이월).
- staging `'w'`+`'n'` 중복 키: 현재 `'n'` 우선(w=RT/F). two-phase 협폭(12-20mV) 의도라면 `'n'` 제거·`'w'` 활성 필요 — 물리 설계 결정이라 사용자 판단 대기(무단 변경 X, 골든 영향).

## 6. Read Coverage
- 코드 entropy_coefficient·GRAPHITE_STAGING_LIT 정독·실행 대조. Ch1/Ch2/appendix 빌드. worked example 재산출·3경로 검증.

## 7. 상태·커밋
✅ **P7 완주 = v1.0.15 완결**. 문건↔코드 sync 정정(worked example)·3대 무결 게이트·HANDOVER·INDEX. 커밋 = main·attribution 없음·명시 스테이징(Ch2 tex/pdf + P7 결과 + HANDOVER + INDEX + 레저).
