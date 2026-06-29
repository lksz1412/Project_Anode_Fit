# Phase 6.1 — v8-10 adversarial 재검수 종합 (한 번에 OK 거부)

> 2 Opus 적대 검수(A=물리·부호·유도수학, B=G-derive 가독·G-usable·그림·이음새). 개별 = `v8-10/REVIEW_A.md`·`REVIEW_B.md`. 빈 통과 아님 — 단 확정 CRIT/HIGH = 0, LOW 폴리시만.

## 확인된 무결 (재검수 후에도)
- ★**부호 8항 8/8 PASS**(A) — v11 코드 1:1, 숨은 flip·자기모순 0. S6 운영0/동기 분리·S8 분극 정정 일치.
- ★**11식 G-derive 전수 통과**(A·SymPy/NumPy 검산) — eq:dUhys artanh 사슬·spinodal 대입·L_q 분모 $1/(1+e^{-A/RT})$·dHeff 흡수·staging round-trip 전부.
- ★**D-WEFF 정확**(A) — $w^\eff$ 다리 ¼ 인수·stray F·s_F orphan **전무**(v8-02/03/07 회귀 자리 클린, 베이스 v8-06b 통과 재확인).
- ★**D-PEAK/D-PEAK2 정확**(A) — 방향 정정 + 문턱 진폭 불연속 "작은 점프 가능" 정직 기술(과·소 주장 없음).
- **배치 보존·G-usable 닫힘·그림 9개 혼란 0·렌더 ASCII·overfull 0**(B).

## v8-11 보완점 (전부 LOW 폴리시 → 미세 보강)
| # | 출처 | 위치 | 내용 | v8-11 조치 |
|---|---|---|---|---|
| P1 | A | eq:Veq(L458 부근) | $g'(\xi)=sF(V_\eq-U)$ 출발 다리가 괄호로 압축(D-VEQ 순환은 해소·가시성만 약함) | eq:mu→eq:gxi→eq:eqcond 연결 1줄 가시화 |
| P2 | B | fig:relaxode 캡션(L915 부근) | D-PEAK2 반직관 논증 4문장 압축·그림이 핵심 시각화 못 함 | 캡션 간결화(논증은 본문, 캡션은 도식 설명) |
| P3 | B | eq:weff | $s$-흡수(부호) 무언 | 1구 명시 |
| P4 | B | z_cut=4.357 | "유도"처럼 단언(실제 = 미분 5% 컷의 *선택* 파라미터) | "선택값(미분 5% 컷)" 명시 |

★수정 범위 = 가독·다리 가시성·표현 정밀화뿐. 검증된 결과 박스·부호·유도 수학·코드 정합·그림은 불가침.

## Gate
PASS_REVIEW_V10 — adversarial 재검수(빈통과 거부)·확정 CRIT/HIGH 0·LOW 폴리시 4건·부호 8/8·11식 G-derive 통과. 다음 = Phase 7.1(v8-11 최종 + 정식 10회, step 34).
