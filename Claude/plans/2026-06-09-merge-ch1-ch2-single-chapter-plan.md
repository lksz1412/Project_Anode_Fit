# Ch1+Ch2 단일 챕터 병합·완결 계획 — 절 단위 순차 · 50p+ · keep/cut 확정

## Summary
박사님 지시(6-09): Ch1(평형·동역학 dQ/dV)과 Ch2(충방전 히스테리시스)를 \textbf{단일 챕터로 병합}하고, 댕글링 추가분을 keep/cut 확정대로 통합/제거하며, \textbf{거의 다시 쓰는 수준}으로 교과서화. 합본 \textbf{50p 이상}. 병합의 핵심 이득: (1) $1.x/2.x$ 교차인용이 \emph{내부 식번호}로 통합 → 진짜 단일문건, (2) \emph{정규용액 $\Omega_j$ 상호작용·상분리}가 \emph{평형 peak 모양}(이상 $\Omega=0$ 확장)과 \emph{히스테리시스}(분기) \emph{양쪽}에 쓰여 — Ch2 §2 "배경" 댕글링이 자연 해소, (3) 도착점이 \emph{하나의 통합 모델식}(방전 + 충방전). keep/cut = 권고표 확정: lever rule \textbf{CUT}, CNT식·과전압 3분해·Preisach \textbf{TRIM}, 나머지 KEEP+절 재작성. 방식 = 절 단위 순차 루프(절마다 빌드·앞 절 정합), 최대 effort, NO Workflow, master 손검, Codex, result/ledger, auto-commit. 박사님 "알아서 만들어와" = 본 권고대로 자율 진행.

## ★ 최우선 원칙 — 실질·무패딩 (박사님 6-09 명시)
- \textbf{50p+ 는 \emph{목표가 아니라 결과}다.} 통합 재작성·정규용액 통합·KEEP 깊이를 \emph{물리적 논리를 제대로 갖춰}(비약 0, 매 단계 정당화) 쓰면 자연히 도달하는 분량.
- \textbf{쓸모없는 내용으로 억지로 늘리는 것 절대 금지.} 동어반복·장식 box·맥락 없는 예제·disclaimer 적층·분량용 일반론 X. 모든 문장이 \emph{실질 물리}이고 뒤에서 \emph{쓰여야} 한다(완결성).
- 한 절이 짧아도 물리가 그만큼이면 그대로 둔다 — \emph{길이 맞추려 채우지 않는다}. 깊이는 \emph{진짜 유도·검산·worked·해석}으로만.

## Current Ground Truth
- `graphite_ica_ch1.tex`(24p)·`graphite_ica_ch2.tex`(11p) 완료·검증, 커밋 `2c35fa9`. git history가 원본 보존(별도 아카이브 불요).
- 병합 산출 = \textbf{새 단일 파일 `graphite_ica_ch1.tex`(재작성)}; 병합 완료·검증 후 구 `graphite_ica_ch2.tex`는 `old/`로 아카이브. (구조: 단일챕터 + 발열(구 Ch3) + 반속(구 Ch4).)
- 의존 트리(박사님 직접): 6-09 갱신 — \textbf{병합 Ch1(=구1+2) → 발열 → 반속}. 발열(Ch3)·반속(Ch4)의 인계 식번호는 병합 후 재대조.
- keep/cut 결정표 = `2026-06-09-ch1-ch2-integration-completeness-plan.md`(v2) 그대로 적용.

**불변:** 정확성 확인 유도·물리 보존. 단일문건 규율(이제 진짜 단일). NO Workflow. 챕터 통째 배치 X(절 단위). auto-commit+push.

## 병합 챕터 구조 (절 순서 — 50p+ 목표)
**PART A — 평형·동역학 dQ/dV (구 Ch1 골격, 정규용액 통합)**
1. 서론 (전체 arc: 평형 peak→동역학 꼬리→충방전 히스테리시스→통합 피팅식)
2. 기호와 규약 (구 Ch1+Ch2 기호 통합 표)
3. 전하 보존이 정하는 내부 전위 $V_n$
4. 평형 peak — 격자기체·logistic (이상 $\Omega=0$)
5. \textbf{[통합 신설] 정규용액 상호작용 $\Omega_j$ 와 상분리} — 구 Ch2 §2(g·$g''$·$T_c$·binodal/spinodal·핵생성)를 \emph{여기로} 이동: 구 Ch1 §4의 $\Omega=0$ 가정을 $\Omega\ne0$ 으로 확장(peak 비단조·상분리). vdW/Maxwell은 \emph{여기서 도구}로 도입. lever rule CUT, CNT 정성 TRIM.
6. 동역학 지연과 비대칭 꼬리
7. 전위에 의한 유효 배리어
8. 입자 분포 통계 도구
9. 배리어 분포와 중첩
10. 종합: 단일 전이(방전) 피팅식 · 3$\times$3 의존성
11. 다중 전이 겹침과 합산 분해
**PART B — 충방전 히스테리시스 (구 Ch2 골격, §5 배경 위에서)**
12. 비단조 평형 전위와 spinodal — 분기의 유도 (§5의 $\Omega$ 사용)
13. 충방전 분기와 히스테리시스 gap $\Delta U_j^\hys$
14. 분기별 평형 $\dd Q/\dd V$
15. 동역학 분극 — 율 의존(과전압 3분해 TRIM, lumped $R_n$)
16. 부분 cycle 과 기억 (Preisach TRIM → return-point+$h_j$, §18 보간 뒷받침)
**PART C — 통합**
17. \textbf{통합 종합 모델식} — 방전 단일식(eq:master)과 충방전 분기식(eq:hys\_master)을 \emph{한 절}로: 단상($\Omega\le2RT$) 환원·충방전 확장 일관.
18. 데이터에서 파라미터로, 그리고 예측 (저율 OCV·펄스·다율·다온도·충방전 gap → 전 파라미터; 예측)
19. 검증과 반증 (Ch1 진단표 + 히스 분리)

## Phase Range (cumulative step)
| Phase | 절 | Steps | 핵심 |
|---|---|---:|---|
| M0 | 골격 | 1–2 | 병합 preamble(통합 기호·식번호 단일) + 서론 |
| M1 | §2 기호 | 3–4 | 구1+2 기호 통합 표 |
| M2 | §3 전하보존 | 5–6 | 구 Ch1 §2 이식+다듬 |
| M3 | §4 평형 peak | 7–9 | 구 Ch1 §3(이상) |
| M4 | §5 정규용액·상분리 | 10–15 | 구 Ch2 §2 이동·통합(peak 확장)·lever cut·CNT trim·vdW 도구화 ★ |
| M5 | §6 동역학 지연 | 16–18 | 구 Ch1 §4 |
| M6 | §7 유효 배리어 | 19–21 | 구 Ch1 §5 |
| M7 | §8 통계 도구 | 22–24 | 구 Ch1 §6 |
| M8 | §9 분포·중첩 | 25–27 | 구 Ch1 §7 |
| M9 | §10 종합(방전)·3×3 | 28–31 | 구 Ch1 §8 + worked example 피팅 anchor 통합 |
| M10 | §11 겹침 | 32–34 | 구 Ch1 §9 + 융합 worked 절차 사용 |
| M11 | §12 spinodal 분기 | 35–37 | 구 Ch2 §4(§5 Ω 사용, 중복 배경 제거) |
| M12 | §13 ΔU_hys | 38–40 | 구 Ch2 §5 |
| M13 | §14 분기 dQ/dV | 41–43 | 구 Ch2 §6 |
| M14 | §15 동역학 분극 | 44–46 | 구 Ch2 §7(3분해 trim) |
| M15 | §16 부분 cycle | 47–49 | 구 Ch2 §8(Preisach trim) |
| M16 | §17 통합 종합식 | 50–53 | eq:master+eq:hys_master 한 절 통합 ★ |
| M17 | §18 데이터→예측 | 54–57 | 전 파라미터 피팅·예측 통합 |
| M18 | §19 검증·반증 | 58–60 | 진단표(falsify 본문 사용)+히스 분리 |
| M19 | 빌드·Codex·아카이브·커밋 | 61–64 | 50p+ 확인·orphan 0·구 ch2 아카이브 |

## Non-goals
- 정확성 확인 유도·식·물리 변경 금지(통합·재배치·재작성으로 \emph{흐름}만). 발명 금지.
- 단일문건 규율(이제 내부 식번호; 인계/전달/결론 절 0). NO Workflow. 챕터 통째 배치 금지(절 단위 빌드).
- keep/cut: lever rule CUT, CNT식/과전압3분해/Preisach TRIM(권고표). KEEP은 뒤 사용처 신설로 완전 통합.

## Implementation Changes
- 재작성: `graphite_ica_ch1.tex`(단일 병합 챕터). 빌드 pdf. 완료 후 `graphite_ica_ch2.tex`→`old/` 아카이브.
- Result: `PHASE_MERGE_RESULT.md`. Ledger: `PHASE_MERGE_LEDGER.md`(절별·keep/cut·앞뒤 고리).

## Phase 본문 (각 M.x 공통 규율)
각 절: 구 원문 이식 → \emph{통합 재작성}(병합 맥락의 앞 도입·뒤 사용; 내부 식번호로 교차인용 전환) → keep/cut 적용 → worked/배경이 \emph{뒤에서 쓰이게} → 빌드 → 앞 절 정합. \textbf{M4·M16이 핵심}(정규용액 통합·통합 master).

## Implementation Interfaces
- 식번호: 단일 시퀀스 `\arabic{equation}`(1.x/2.x 폐지, 챕터 내부 번호). \thesection 단일.
- 통합 master(§17): 방전 $\dd Q/\dd V_\app=C_\bg+\sum_j Q_j[\text{rise}+\text{tail}]$ 과 충방전 분기 $|^b$, $U_j^{\dis/\chg}=U_j\pm\tfrac12\gamma_j\Delta U_j^\hys$ 를 한 박스로; $\Omega\le2RT$ 단상 환원이 §4 logistic 으로.
- "뒤 사용" 실체 = 통합 master·파라미터 표·피팅 단계·진단·환원검산이 인용. Result 11항목·Ledger 12-col.

## Test Plan
- 절마다 빌드 2-pass(overfull 0; undefined는 미작성 forward-ref 허용, 최종 0). 최종 \textbf{50p+} 확인.
- 결정표 전 항목 {KEEP-통합 검증/CUT-제거 검증}, 각 KEEP 앞·뒤 위치 result 명시(완결성). 식번호 단일·내부 인용 grep. 단일문건 규율 grep. Codex foreground 1회(통합 물리 무손상·orphan 0). 발열(구 Ch3)·반속(구 Ch4)의 구 1.x/2.x 인계 번호 → 병합 후 재대조(별 phase 또는 후속).

## Assumptions
- A1: 병합 = 구 Ch1+Ch2만(발열·반속은 별 챕터 유지). 발열/반속의 인계 식번호는 병합 후 갱신(후속 작업).
- A2: 50p+ 는 통합 재작성+keep 깊이로 자연 도달(인위 패딩 X).
- A3: keep/cut 권고표 확정(박사님 "알아서"); 추후 특정 항목 살리라면 사용처 신설.

## Correction History
- 2026-06-09: 병합 결정. integration plan v2(keep/cut)를 \textbf{단일 챕터 병합 + 50p+}로 격상. 박사님 "알아서 만들어와·단일 챕터·50p+". 구 Ch1+Ch2 → 단일 `graphite_ica_ch1.tex`, 정규용액 통합(§5)·통합 master(§17) 핵심. M0부터 절별 순차 연속, git이 원본 보존.
