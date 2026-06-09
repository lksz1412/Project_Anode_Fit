# Ch1·Ch2 통합·완결성 계획 — 추가분 댕글링 해소 (앞 도입 + 뒤 사용)

## Summary
박사님 지적(6-09): Ch1$\cdot$Ch2 에 보강한 내용(worked example$\cdot$vdW$\cdot$lever rule$\cdot$CNT$\cdot$Preisach$\cdot$진단표 등)이 \emph{앞뒤 문맥에 안 물리고 standalone 으로 끼워져} "댕글링 본드처럼 덜렁" — 유용해 보이나 \emph{어디서도 도입$\cdot$사용 안 되어 쓸 수 없는 orphan}. 본 계획은 \textbf{양을 더 늘리지 않고}, 각 추가분이 \emph{(a) 앞이 도입(motivation) + (b) 뒤가 사용(downstream 인용$\cdot$대입$\cdot$환원)} 두 고리에 물리도록 엮어 **완결성(orphan 0)** 을 만든다. 두 고리를 못 채우는 진짜 orphan 은 \emph{trim}. 방식 = 절 단위$\cdot$챕터 단위 루프(절마다 빌드$\cdot$앞 절 정합), 최대 effort, NO Workflow, master 직접 손검, Codex 적대검수, result/ledger, auto-commit. spine = 각 챕터의 최종 피팅식(Ch1 eq:master, Ch2 eq:hys\_master)과 피팅 절차.

## Current Ground Truth
- Ch1 24p$\cdot$Ch2 11p, 빌드 clean, 직전 커밋 `aaa4de4`(브랜치 rb-rebuild-2026-05-30).
- 최근 보강(PHASE_CM·CM2·TXB·DEEP_REVIEW)으로 추가된 항목이 spine 미연결 의심.
- **댕글링 후보(audit 으로 확정):**
  - Ch1: §3/§8 worked example(FWHM·높이)·§8 3×3 칸별·§9 융합 worked·§11 경쟁기전 진단표 — 도입/사용 고리 점검.
  - Ch2: §2.2 lever rule$\cdot$common tangent·vdW Maxwell·§2.3 CNT 장벽식($\Delta G^\ast\propto\gamma_s^3/\Delta g^2$)·§2.4 Dreyer 풍선·§7 과전압 3분해·§8 Preisach/FORC — downstream 사용처 점검(특히 Preisach·CNT·lever rule 의심).
- 완결성 = \emph{모든} 추가분이 앞 도입 + 뒤 사용에 물림(`feedback_integrated_content_no_dangling`).

**기존 결정(불변):** 정확성 확인 유도·식·라벨·인계 번호 보존. 단일문건 규율. NO Workflow. 챕터 통째 배치 X.

## Phase Range
| Phase | 이름 | Steps | 산출 |
|---|---|---:|---|
| C0 | 댕글링 감사(Ch1·Ch2 전수) | 1–4 | 추가분별 (앞 도입?·뒤 사용?) 태그표 |
| C1.1~ | Ch1 절별 통합(댕글링 절만) | 5–14 | 앞 motivation·뒤 usage ref 엮기 / trim |
| C1.v | Ch1 빌드·정합·커밋 | 15–16 | |
| C2.1~ | Ch2 절별 통합(댕글링 절만) | 17–28 | 〃 |
| C2.v | Ch2 빌드·Codex·커밋 | 29–31 | |

## Non-goals
- \emph{새 내용 추가 금지}(통합 작업 — 연결 문장$\cdot$forward/back ref$\cdot$사용처 신설/이동, 또는 trim). 양 늘리기 아님.
- 정확성 확인 유도·식·식번호·인계 번호 변경 금지(연결만).
- 단일문건 규율(Chapter-N 0·인계/전달/결론 절 0) 유지. 챕터 통째 배치 X. NO Workflow.

## Implementation Changes
- 수정: `graphite_ica_ch1.tex`·`graphite_ica_ch2.tex`(절별 연결 Edit/trim). 빌드 pdf.
- Result: `PHASE_INTEG_RESULT.md`. Ledger: `PHASE_INTEG_LEDGER.md`(절별 댕글링→조치).

## Phase C0 — 댕글링 감사
- **Steps 1–4.** Ch1·Ch2 전수 정독, \emph{최근 추가분}(box/예제/배경 단락)마다 두 고리 태그: \textbf{앞 도입}(직전 맥락이 왜 필요한지 깔았나) / \textbf{뒤 사용}(뒤 절·최종식·피팅 절차·표가 인용$\cdot$대입$\cdot$환원하나). 각 항목 → {통합됨 / 앞만 / 뒤만 / orphan} 분류 + 조치(엮기 위치 또는 trim).
- **Gate GC0:** 추가분별 태그표(절·항목·앞?·뒤?·조치) 완성, orphan 목록 확정.

## Phase C1.x — Ch1 절별 통합 (댕글링 절만)
- **Steps 5–14.** GC0 의 Ch1 orphan/한쪽고리 항목을 절 순서대로 — 각 항목:
  - \emph{앞 도입 결핍}: 직전 단락에 "왜 지금 이걸 보는가" 한 줄(앞 결과에서 자연 연결).
  - \emph{뒤 사용 결핍}: 그 결과(수치·식·개념)를 \emph{실제로 쓰는} 자리 만들기 — 예) §8 worked example 의 수치를 \emph{최종식 파라미터 표/피팅 S1–S4} 가 인용하거나, 3×3 표 해석이 master 식 항으로 연결되게. 진단표→§falsify 본문 논리와 명시 연결.
  - \emph{진짜 orphan}: trim(내용 손실 아닌 중복/장식 제거).
  - 절마다 빌드 + 앞 절 정합.
- **Gate GC1.x:** 각 처리 항목이 앞 도입+뒤 사용 양 고리 충족(또는 trim) — grep/정독 확인, 라벨·식 보존, 빌드 clean.

## Phase C1.v — Ch1 빌드·정합·커밋
- **Steps 15–16.** 2-pass overfull 0·undefined 0; "추가분 orphan 0" 재확인; ch1 커밋·푸쉬.

## Phase C2.x — Ch2 절별 통합 (댕글링 절만)
- **Steps 17–28.** GC0 의 Ch2 항목 — 특히:
  - §2.2 \textbf{lever rule}: phase 분율 $f^+$ 를 뒤가 안 쓰면 — 두-상 구간 dQ/dV/용량 분배 설명에 연결하거나 trim.
  - §2.2 \textbf{vdW Maxwell}: §4 비단조 전위와 명시 연결(이미 일부) 강화, 안 쓰면 축약.
  - §2.3 \textbf{CNT 장벽식}: $\gamma_j$(축소 인자) 물리 근거로 §5 boundbox 가 \emph{명시 인용}하게(현재 정성만) — 또는 정성으로 축약.
  - §2.4 \textbf{Dreyer 풍선}: §5 다입자 평활$\cdot$$\gamma_j$ 분산에 연결.
  - §7 \textbf{과전압 3분해}: §파라미터/피팅이 $R_n$ 분해를 \emph{쓰는}지(식별 절에서 $R_n=R_\ohm+\dots$ 인용) — 안 쓰면 §pol 안에서 닫기.
  - §8 \textbf{Preisach/FORC}: §param/§fit 또는 부분 cycle 활용이 \emph{쓰지} 않으면 — major-loop 파라미터화와 연결(scanning=보간 근거)하거나 핵심만 남기고 trim.
  - 절마다 빌드 + 앞 절·Ch1 정합.
- **Gate GC2.x:** 각 항목 양 고리 충족/또는 trim, 단일문건 규율, 라벨·식·인계 보존, 빌드 clean.

## Phase C2.v — Ch2 빌드·Codex·커밋
- **Steps 29–31.** 2-pass 0/0; "추가분 orphan 0" 재확인; Codex foreground(통합이 물리 왜곡 0·연결 타당·orphan 0); result+ledger; ch2 커밋·푸쉬.

## Implementation Interfaces
- 처리 단위 = \emph{추가분 1개}. 각 처리에 두 고리 명시 기록(앞 도입 위치·뒤 사용 위치 또는 trim 사유).
- 연결 수단: 직전 단락 motivation 한 줄 / 뒤 절·식·표의 \eqref·\S\ref 인용 / 사용처 신설(예: 파라미터 표가 worked 수치 참조). 새 \emph{물리} 추가 X.
- Result 11항목·Ledger 12-col.

## Test Plan
- 빌드 2-pass overfull 0·undefined 0.
- **완결성 검수**: 추가분 태그표가 전부 {통합됨 또는 trim} — orphan 0. 각 항목의 앞 도입·뒤 사용 위치를 result 에 명시(정독 증명).
- 라벨·식번호·인계 번호 보존 grep. 단일문건 규율 grep. Codex foreground 1회(연결 타당·물리 무손상).

## Assumptions
- A1: "추가분"은 최근 보강 커밋(PHASE_CM/CM2/TXB/DEEP_REVIEW)에서 add 된 box/예제/배경. git diff 로 식별 가능.
- A2: trim 은 \emph{중복$\cdot$장식} 제거지 정확한 물리 손실 아님 — 경계 시 보존+연결 우선.
- A3: 완결성 우선이라 \emph{양은 줄 수도} 있음(orphan trim). 박사님 "양 늘린 건 좋다"는 \emph{유지하되 엮기} 의미로 해석(엮기 불가 orphan만 trim).

## Decisions Required
- D-1 (trim vs 엮기 경계): 진짜 orphan(어디에도 못 씀)은 trim 이 기본. 단 박사님이 특정 항목(예 Preisach·CNT)을 \emph{반드시 살려라} 하면 사용처를 신설해서라도 엮음. 기본 = 엮기 우선, 불가 시 trim. (audit 후 orphan 목록 제시 시 박사님 지정 가능)

## Correction History
- 2026-06-09 v1: 박사님 "추가분이 앞뒤 문맥 단절·댕글링·미사용, 제대로 쓸 수 있게 보완 최우선, 절별·챕터별 루프 완결성" 수용. 메모리 `feedback_integrated_content_no_dangling` 신설. 통합(연결/trim) 작업 — 새 내용 추가 아님. GC0 감사 후 GO 시 C1→C2 절별 연속.
