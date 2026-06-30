# Phase G — §7→§8~끝 이해 보완(중간과정·해설 추가) Result

**Date**: 2026-06-07 · **Plan**: `2026-06-06-ch1-sec8-10-comprehension-bridge-plan.md` · **챕터**: G(이해 Glue)
**트리거**: 사용자 — "§7까지 이해 OK. §7→§8 전환부터 끝까지 연결 안 됨 → 중간과정·해설·풀이 보완."

## Summary
§8(synth)~§10(falsify) + 특히 §7→§8 \emph{논리 도약}에 \emph{설명·중간유도 추가}(add only, 물리·수식 값 불변). Codex foreground **OVERALL CLEAN**(연결 유도 수학 전 단계 CORRECT). 빌드 GREEN 19→20p(설명 add 로 증가).

## Files Updated (`graphite_ica_ch1.tex`) — add only
- **G.1 §7→§8 연결 유도(최대 도약 해소)**: §8.1 앞에 삽입 — ① §7 eq:superpose 는 \emph{꼬리(1전이)}만 줬음 → 전체 peak=rise+꼬리로 묶음, ② 가중평균 지연 $\bar r_j(q)=\int\rho_G\,r_j(q;G)\dd G$(per-group eq:rsol 을 §7 분포로 평균), ③ $\xi_j=\xi_{\eq,j}-\bar r_j$, ④ \emph{중간 무번호식}: $-Q_j\,\dd\bar r_j/\dd V_n$ 전개 = $Q_j\int\rho_G(r_a/L_V)e^{-(V_n-V_a)/L_V}\dd G$ = \emph{eq:superpose 재현}(분포 적분 = $\bar r_j$ 미분의 다른 표기), ⑤ 그러므로 eq:closed. → \emph{§7 분포적분 ↔ §8 닫힌식 연결이 한 줄 단언에서 명시 유도로}.
- **G.2 §8 해설**: 3×3 표 앞 "읽는 법"(행=위치·너비·높이 / 열=$T$·$|I|$·$V$ / 칸=어느 식 어느 항·부호 / 평형↔동역학 상충 칸=관찰 해소 핵심) + 식별순서 S1~S4 앞 "공선형 한 겹씩 벗기기" 전체 원리.
- **G.3 전환 bridge**: §8→§9("단일 전이 닫음 → 여러 전이 겹침, $N_p\approx3\sim4$") · §9→§10("예측식 세움 → 반증 가능해야") 도입 연결문.

## Read Coverage
- §7 끝~§10 + 참고문헌 전 구간 정독(L660~924) + §8.1 직접 재유도(부호·연쇄율 검증).

## Execution Evidence
- 빌드: xelatex ×3 → `!`0·ref/cite undefined 0·**20페이지**(19→20, 설명 add)·overfull 0·952줄(924→+28). 38식·48라벨 보존(add only).
- **Codex foreground 검증**(287s): A(연결 유도 수학) \emph{전 단계 CORRECT}(부호·연쇄율·$L_V$ 치환·지수 변환·post-peak $\dd\xi_{\eq}/\dd q\approx0$ 명시) · B 정합 CLEAN · C 흐름 SMOOTH(§7→§8 도약 해소, 잔존 도약 0) · D 참조 CLEAN(48라벨·150 ref undefined 0). **OVERALL CLEAN**.

## Validation (4-tier)
- **확정**: §7→§8 연결 유도 명시(수학 Codex 검증)·§8 표/식별순서 해설·§9·§10 전환 추가. 흐름 SMOOTH. 물리·수식 값·라벨 불변(add only).
- **추정/미검증**: 없음.

## Gate
**PASS_G** — Codex OVERALL CLEAN + 빌드 GREEN + add only(수식·라벨 불변) + §7→끝 흐름 해소.

## Next
사용자 검토. (남은 후보: Appendix B 별도 챕터화 — F.9b, 사용자 결정 대기.)
