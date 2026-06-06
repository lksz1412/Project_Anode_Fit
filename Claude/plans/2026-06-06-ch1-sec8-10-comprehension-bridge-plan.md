# Ch1 §7→§8~끝 이해 보완(중간과정·해설·풀이 추가) Plan

**Date**: 2026-06-06 · **Author**: Claude · **챕터**: G(이해 Glue) · **Phase**: G.0~G.4
**대상**: `Claude/docs/graphite_ica_ch1.tex` (924줄·19p·GREEN; F 교과서화 완료)
**트리거**: 사용자 — "§7까지는 이해됨. §7→§8 전환부터 끝까지 연결이 안 됨. 중간과정·해설·풀이 보완해 이해하기 좋게." 방법은 기존 방식 그대로.

---

## Summary
§8(종합)~§10(반증) + 특히 §7→§8 전환의 \emph{논리 도약}을 메우는 \emph{설명·중간유도 추가}(내용 \emph{add}, 물리·수식 값 불변). 핵심 = (G1) §7 분포적분(eq:superpose) ↔ §8 닫힌식(eq:closed) \emph{연결 유도 명시}, (G2) §8 3×3 표·식별순서 S1~S4 해설 보강, (G3) §8→§9→§10 전환 bridge + §9·§10 풀이 보완.
**방법**: 기존 워크플로 — 절별 보완 → Codex foreground 적대+판정 → 문제 0까지 → 이전 절 연계 → 빌드 → result.

## Current Ground Truth (정독 확인)
- §7(dist) 끝: eq:superpose = 꼬리를 $\int\rho_G\,[r_a(G)/L_V]e^{-(V_n-V_a)/L_V}\dd G$ 로(꼬리 only, 단일 전이).
- §8(synth) §8.1: 갑자기 $\xi_j=\xi_{\eq,j}-\bar r_j$, $\bar r_j=\int\rho_G r_j(q;G)\dd G$ 도입 → eq:closed=평형 rise − 지연 꼬리. \emph{eq:superpose→eq:closed 연결("그 미분이 eq:superpose 꼬리")이 \textbf{한 줄 단언}만, 유도 생략}. ← \textbf{최대 도약}.
- §8.2 3×3 표: 칸마다 식 인용 빽빽, "어떻게 읽나" 해설 부족.
- §8.3 eq:simplefit(δ 극한)·$r_{a,j}$ 보존·식별순서 S1~S4(공선형 차단): 근거는 있으나 dense.
- §8→§9, §9→§10 \emph{전환문 없음}(절이 갑자기 시작).
- §9 eq:total·겹침 기준·OCV-anchored 절차 / §10 반증 지문·경쟁원 배제: 상대적으로 자족이나 도입 bridge 부재.

## Phase Range
| Phase | 범위 | 핵심 |
|---|---|---|
| **G.0** | 정독·설계 | (완료) §7~§10 정독 + 도약 지점 확정 + 보완 설계 |
| **G.1** | §7→§8 bridge | eq:superpose ↔ eq:closed \emph{연결 유도} 명시(per-group $r_j(q;G)$→$\bar r_j$→미분=꼬리→rise와 합=closed). 단일전이 꼬리(§7)와 전체 peak(§8) 관계 |
| **G.2** | §8 해설 | 3×3 표 "읽는 법" 도입문 + 행별 1줄 / 식별순서 S1~S4 "왜 이 순서(공선형 차단)" 풀이 보강 / eq:simplefit δ극한 1~2단계 |
| **G.3** | §9·§10 + 전환 | §8→§9·§9→§10 bridge 문장 + §9 겹침/분해 풀이·§10 반증 해설 경량 보완 |
| **G.4** | 교차모델·빌드 | Codex foreground 적대(연결·정합·논리) → 판정 → 반복 + 빌드 GREEN + 커밋·푸쉬 |

**절별 게이트**: G-bridge(도약 메움·중간유도 명시) · G-flow(이전 절 연계·비약 0) · G-invariant(물리·수식 값·라벨 불변, \emph{add only}) · G-build · G-review(Codex foreground→판정→반복) · G-recovery(§X 컴팩션 재정독).
**정지 조건**: Decision Gate/FAIL/사용자 stop/통제문서 모순.

## Non-goals
- 수식 \emph{값}·물리 결론·라벨·식번호 변경(설명 add 만; 새 보조식은 무번호 또는 신규 라벨 허용). §1~6 본문(이미 이해 OK). Appendix B 이식(F.9b: 별도). Workflow 도구.

## Implementation Changes
`graphite_ica_ch1.tex`(§7 끝~§10 설명 add) / `PHASE_G*_RESULT.md` + ledger / 본 계획. 문건 보호.

## Phase 상세
- **G.1**: §8.1 앞/안에 \emph{연결 문단+중간식} 삽입 — ① §7은 꼬리(1전이)를 분포적분으로 줬음을 받아, ② 전체 peak = 평형 rise + 지연 꼬리임을 명시, ③ $\bar r_j(q)=\int\rho_G\,r_j(q;G)\dd G$ 가 §4 eq:rsol 의 per-group 지연을 §7 분포로 평균한 것, ④ $-Q_j\,\dd\bar r_j/\dd V_n$ 을 전개하면 eq:superpose 적분이 \emph{나옴}을 1~2단계로, ⑤ 상승부와 합쳐 eq:closed. \emph{무번호 보조식 사용}.
- **G.2**: 표 앞 "각 칸 = {위치·너비·높이}가 {T·|I|·V} 에 대해 \emph{어느 식 어느 항}이 지배" 도입 + 너무 압축된 칸 1~2개 풀어쓰기. 식별순서: enumerate 앞 "전체 논리 = 뒤 단계와 공선형인 양을 먼저 고정→뒤 단계 기지화" 1문단.
- **G.3**: §8 끝→§9 "단일 전이를 닫았으니 여러 전이 겹침으로 확장" / §9 끝→§10 "예측식을 세웠으니 어떻게 틀리는지 검증" bridge. §9 겹침 기준 (i)(ii)·OCV-anchored 절차에 1줄씩 직관, §10 반증 지문에 "보정 전/후" 대비 명료화.
- **G.4**: Codex foreground 전 구간(§7→끝 연결·논리·정합) → 판정 → 반복 → 빌드 GREEN(페이지 \emph{증가} 정상=설명 add) → 커밋·푸쉬.

## Test Plan
- **연결 점검**: §7→§8 eq:superpose↔eq:closed 유도가 명시됐는지·§8 표/식별순서 해설·전환문 존재 횡단 확인.
- **불변 점검**: 38식·11절·48라벨·물리 값 불변(add only) — grep + 빌드 ref/cite undefined 0.
- **빌드 GREEN**: `!`0·overfull 0(신규 보조식 폭 점검). 페이지 증가 정상.
- **Codex foreground**: §7→끝 CLEAN(연결·논리). **연계**: 절별 G-flow.

## Assumptions
- A1: 설명 add 만, 수식 값·물리 결론 불변. A2: 신규 보조식은 무번호 우선(필요 시 신규 라벨). A3: §1~6 무수정.

## Decisions Required (무응답 시 권고값)
- **D-범위**: §7→§8 bridge(최우선) + §8 해설 + §9·§10 전환·풀이. 권고: 그대로.
- **D-보조식 번호**: 신규 중간식은 무번호(논리 흐름용). 권고: 무번호(기존 라벨 보존).

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-06-06 (G v1) | §7→§8~끝 이해 보완 계획 신설 — eq:superpose↔eq:closed 연결 유도 명시 + §8 표/식별순서 해설 + §9·§10 전환·풀이. add only, 절별 Codex foreground iterate + 이전 절 연계. |
