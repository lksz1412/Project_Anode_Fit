# Ch2 심도 검토·재작성 — 보강 + 인라인 정리 + 핸드오프 제거 + Ch1 정합 + 교과서체(정독 통합) Plan

**Date**: 2026-06-07 · **Author**: Claude · **챕터**: D2(Deep Ch2) · **Phase**: D2.0~D2.5
**대상**: `Claude/docs/graphite_ica_ch2.tex` (595줄·12p·GREEN) · **기준**: `graphite_ica_ch1.tex`(952줄·20p, 확정) + `Claude/work/oldtrack_src/graphite_ica_ch2_rebuilt.tex`(947줄, 누락 rigor 재료)
**트리거**: 사용자 — Ch2 \emph{부실}(논리 수식·해설 부족) · 줄글 사이 낀 \emph{인라인 수식 지저분} · 통합 배포 예정이라 \emph{Ch1에서 받는·Ch3로 넘기는 절 불필요}(앞뒤) · \emph{컨벤션 Ch1 그대로}(신규 컨벤션은 문건 초기 표로 정리, 통합 시 목차·컨벤션표 병합 염두) · \emph{구어체 잔재}(단 grep 별도 처리 금지 — 전문 정독·보강에 통합) · \emph{레퍼런스는 챕터별 별도}.

---

## Summary
Ch2 를 Ch1 수준의 \emph{밀도·엄밀성·교과서체}로 심도 재작성한다. \textbf{전문 정독을 한 번 하면서 보강·인라인 정리·Ch1 정합·교과서체를 \emph{동시에}} 수행한다(별도 grep 후처리 X — 읽을 때 같이 고쳐 완성도↑). 5축:
(1) \textbf{보강} — 누락 논리 수식·중간 유도·해설 prose 를 구-track 재료에서 \emph{무비약}으로 복원(Ch1 register).
(2) \textbf{인라인 정리} — 줄글에 낀 유도성 수식을 \emph{display 식}으로 승격, 자명 치환만 인라인.
(3) \textbf{핸드오프 제거} — ``Ch1 에서 받는 기준식''(C1~C6 등치 재서술)·``Ch3~5 로 전달'' 절 \emph{삭제}(통합 시 앞뒤). Ch1 결과 인용은 의미 참조(통합 시 \ref).
(4) \textbf{컨벤션} — Ch1 기호·부호 그대로 \emph{이어받고}(재정의 X), \emph{Ch2 신규 기호만} 문건 초기 ``기호와 규약'' 표로 정리(Ch1 §1 방식; 통합 시 Ch1 표와 \emph{병합 가능}하게 설계). \emph{전수 대조로 Ch1 과 0 불일치}.
(5) \textbf{교과서체} — 구어 잔재를 \emph{정독 중} 제거(grep 후처리 아님).
\emph{레퍼런스}: Ch2 자체 `thebibliography` 유지(챕터별 별도; 통합은 추후).
**방법**: 절별 \emph{전문 정독→보강·정리·register·정합 동시 적용} → Codex foreground 적대 → 판정 → 문제 0까지 → 이전 절·Ch1 정합 → 빌드 → result → 커밋. (이후 Ch3·4·5 동일 방식 반복.)

## Current Ground Truth
- Ch2 595줄·12p, Ch1(20p) 대비 \emph{얇음}. 줄글 인라인 수식 다수(예 ``$\dot n_j=I_j/(sF)$ [mol/s] 다''). inheritbox(C1~C6 등치)+신규기호표 1절 + ``Chapter 3~5 로 전달'' 1절 보유. 구-track Ch2(947줄)는 더 상세(무비약 유도·해설 풍부).
- 잔여 Codex Ch2 항목: B4(consistency 식 가정 명시)·σ_j k_eff·η 분해 등 — 본 심도 패스서 함께 해소.
- \emph{판정 보류}: ``인라인→display 승격'' 식별 기준(아래 §인라인 규칙).

## Phase Range
| Phase | 범위 | 핵심 |
|---|---|---|
| **D2.0** | 정독·인벤토리·구조 | Ch2 전문 + Ch1(정합 기준) + 구-track Ch2(rigor 재료) 정독. 구조 확정: inherit/transmit 제거 + ``기호와 규약(신규)'' 표 설계(병합 가능) |
| **D2.1~D2.k** | 절별 심도 재작성 | \emph{각 절 전문 정독하며 동시에}: 보강(무비약 유도·해설)+인라인 display 승격+구어 제거+Ch1 기호·부호·식 정합. 절 끝 Codex foreground→판정→문제 0→이전 절·Ch1 정합 확인 |
| **D2.final** | 횡단·빌드 | 전 문서 Ch1 정합 횡단(기호·부호 대조표 0 불일치) + 인라인 0 + 핸드오프 0 + 빌드 GREEN + Codex 전영역 + 커밋 |

**절별 게이트(한 절마다)**: G-substance(부실 해소: 논리 수식·해설 Ch1 밀도) · G-inline(유도성 인라인 0, display 정돈, overfull 0) · G-register(구어 0 — \emph{정독 중} 확인) · G-ch1consist(그 절의 기호·부호·식 Ch1 0 불일치) · G-build · G-review(Codex foreground→판정→반복) · G-recovery(§X).
**문서 게이트**: G-nohandoff(inherit/transmit 절 0) · G-convtable(Ch2 신규 기호 초기 표 존재·병합 가능) · G-ref(Ch2 자체 bib 유지).
**정지**: Decision Gate(중대 물리)/FAIL/사용자 stop/통제문서 모순.

## Non-goals
- Ch2 물리 \emph{결론} 변경(보강은 유도·해설 추가; 오류만 정정). Ch1 본문 수정. Ch3·4·5(별도 라운드). 통합 master·목차·컨벤션표 병합(추후, 단 \emph{병합 가능하게} 설계만). \emph{grep 기반 register 후처리}(금지 — 정독 통합). Workflow.

## Implementation Changes
`graphite_ica_ch2.tex` / `PHASE_D2*_RESULT.md` + ledger / 본 계획. Ch1·구-track·이전 result 보호.

## Phase 상세
- **D2.0**: Ch2 전문 정독(부실·인라인·구어 위치 — 단 별도 목록화보다 절별 작업서 즉시 처리) + Ch1 정독(기호·부호·식 정합 기준 + §1 notation 표 \emph{형식} 참조) + 구-track Ch2 정독(복원할 무비약 유도·해설 재료; 구 메타 X). 구조 확정: (a) inheritbox·transmit 절 제거, (b) 문건 초기 ``기호와 규약'' 절을 \emph{Ch2 신규 기호만}으로(Ch1 표 열 구조 동일 = 통합 시 병합 가능), (c) 서론 짧게 동기 유지, (d) Ch2 bib 유지.
- **D2.1~D2.k(절별)**: 한 절을 \emph{정독하면서 동시에} — (i) 생략 중간 대수 복원(무비약), (ii) ``왜 이 식인가''·물리 해석 prose 보강, (iii) 줄글 인라인 유도식 → display 승격, (iv) 구어→교과서체, (v) 기호·부호 Ch1 정합($\mathcal A_j$ 일반형 $s n_j^{\eff}F$ 포함). 절 끝 Codex foreground 적대 → Claude 판정 → 문제 0까지 → 이전 절 흐름·Ch1 정합 확인 → 절 result.
- **D2.final**: 기호·부호 전수 대조표(Ch2↔Ch1) 0 불일치 + 인라인·핸드오프·구어 0 횡단 + Codex 전영역 → 빌드 GREEN(분량 \emph{증가}=보강 정상) + 커밋·푸쉬.

## Implementation Interfaces
**§컨벤션 정합**: Ch1 변수·부호(s=+1)·핵심식 = 유일 권위, Ch2 재정의 금지·이어받음. Ch2 \emph{신규} 기호만 초기 표(열: 기호/단위/의미 — Ch1 §1 동일 구조 → 병합 가능).
**§인라인 규칙**: display 승격 = (유도 한 단계 / \boxed 후보 / 2줄↑ / 비에 로그·미분·적분). 인라인 유지 = (단위 명시 / 자명 치환 / 단일 기호 정의 / 짧은 조건).
**§핸드오프**: ``Ch1 에서 받는''·``Ch3~5 로 전달'' 절 0. Ch1 인용 = 의미 참조(통합 시 \ref). 통합 전제지만 \emph{현 separate-doc 도 독립 컴파일 유지}.
**§X Anti-compaction**: 재개 직후 직전 result·ledger·Ch2 작업 절·Ch1 정합 기준 재정독.
**§R Result 11항목·Ledger 12-col**.

## Test Plan
- **부실 해소**: 절별 논리 수식·해설이 Ch1 밀도 근접(정독 판단). 분량 증가.
- **인라인**: 유도성 인라인 잔존 0(절별 정독 확인). overfull 0.
- **핸드오프 0**: inheritbox·transmit 절 부재. ``기호와 규약(신규)'' 표 존재·Ch1 열 구조(병합 가능).
- **Ch1 정합**: 기호·부호·식 대조 0 불일치(정독 + 최종 횡단).
- **교과서체**: \emph{정독 중} 구어 제거(별도 grep 패스 X).
- **레퍼런스**: Ch2 자체 bib 컴파일·undefined cite 0.
- **Codex foreground**: 절별·전영역 CLEAN. **빌드 GREEN**.

## Assumptions
- A1: 물리 결론 불변(보강=유도·해설 추가; 오류만 정정). A2: 통합 전제 — inherit/transmit 제거, Ch1 인용 의미 참조; 단 \emph{컨벤션 표는 통합 병합 가능}하게(Ch1 열 구조). A3: register 교정은 \emph{전문 정독 작업에 통합}(grep 후처리 금지 — 불완전·완성도↓). A4: 레퍼런스 챕터별 별도(Ch2 bib 유지). A5: 구-track = rigor 재료(정확성 재검증, 구 메타 X).

## Decisions Required (무응답 시 권고값)
- **D-handoff**: inherit(C1~C6 등치)·transmit 절 \emph{제거}; Ch1 인용 의미 참조. 권고: 제거. [사용자 확정]
- **D-convtable**: Ch2 \emph{신규} 기호만 문건 초기 표(Ch1 §1 열 구조 = 통합 병합 가능); Ch1 기호는 이어받아 재정의 X. 권고: 그대로. [사용자 지시]
- **D-register-method**: 구어 교정을 \emph{절별 전문 정독에 통합}(grep 후처리 금지). 권고: 그대로. [사용자 지시]
- **D-ref**: Ch2 자체 thebibliography 유지(챕터별 별도). 권고: 그대로. [사용자 지시]
- **D-inline**: §인라인 규칙. 권고: 그대로.

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-06-07 (D2 v1) | Ch2 심도 재작성 계획 — 보강+인라인 display 승격+inherit/transmit 제거+Ch1 정합+교과서체. |
| 2026-06-07 (D2 v2) | 사용자 보강: \emph{구어 교정 grep 금지→절별 정독에 통합} · \emph{신규 컨벤션은 문건 초기 표(Ch1 §1 구조, 통합 병합 가능), Ch1 컨벤션은 이어받음} · \emph{레퍼런스 챕터별 별도}. register 단독 phase 제거, 절별 게이트에 통합. D2.0 구조에 ``기호와 규약(신규)'' 표 추가. |
