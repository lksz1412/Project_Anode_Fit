# Phase 6.1 — v7-10 adversarial 재검수 종합 (한 번에 OK 거부)

> 2 Opus 적대 검수(A=물리·부호·코드정합·인자표, B=G-follow·G-usable·그림·이음새). 개별 = `v7-10/REVIEW_A.md`·`REVIEW_B.md`. 빈 통과 아님 — 보완점 6건.

## 확인된 강점 (회귀 아님)
- ★**부호 사슬 8/8 PASS**(A) — S1–S8 전건 v11 코드 1:1, 숨은 flip·자기모순 0. 수치 86.69mV·u=0.766·U(298) 4건 재산출 일치.
- ★**신규 tab:inputs 기본값 0오류**(A) — 14 생성자 기본값 + 전이 키 전 칸 코드 일치(z_cut 4.357·A_cap 4.0·floor 0.05·pad 0.15·n_work 2048·min_lag 2.0·v_span 1e-6·seed 298.15/0.1/1.0·x 0.5·use_dH True·use_w False·h_eta 1.0). staging 표·6단계 박스 오류 0.
- **그림 6개 혼란 0**(B) — 전부 신규 TikZ·렌더 영어전용·\ref·식 정합. 기존 그림 문제 재발 없음.

## v7-11 보완점 (확정 결함 → 수정)
| # | 심각 | 위치 | 무엇이 틀림 | 옳은 형태(v7-11) |
|---|---|---|---|---|
| F1 | HIGH | §sec:width L429·tab:inputs·tab:nodemap·6단계 박스 | 기본 폭 $w=n_jRT/F$ 가 무번호 산문, 표·박스 3곳이 *옵션* eq:weff 참조 → 재현 함정(use_w_eff=False 인데 narrowing 가리킴) | 기본폭 번호식 eq:wbase 신설, 3곳 참조를 eq:wbase 로 |
| F2 | HIGH | §sec:lag L530·566 (L_q 유도) | 완화속도 forward 극한만 → eq:Lqfull 의 $1/(1+e^{-\mathcal A/RT})$ 분모 미유도(유도 다리 끊김; 결과·코드는 정합) | $k_j=k^++k^-=k^+(1+e^{-\mathcal A/RT})$(선형 완화=정·역 합·detailed balance) 다리 추가 |
| F3 | MED | §sec:width 유도 | logistic detailed-balance 가 $w=RT/F$($n{=}1$)만 닫는데 박스는 $n_jRT/F$ | 폭 다중도 $n_j$ 가 eq:wbase 로 분모에 들어감 명시 |
| F4 | LOW | §sec:lag L535 | "$z_\mathrm{cut}{=}4.357$ 이 $\xi_\eq$ 의 5% 컷" 오기(실제 ξ=0.987; 5%는 미분) | "원천 미분 $\dd\xi_\eq/\dd q$ 의 5% 컷" |
| F5 | LOW | §sec:hys L357 | "$(1-2\xi)=\mp u$" 부호순 모호 | $(1-2\xi_s^-)=+u$, $(1-2\xi_s^+)=-u$ 명시 |
| F6 | build | — | 2-pass 페이지참조 미수렴(헤더 16/15) | 3-pass 빌드 |

★수정 범위 = **유도 다리·참조 정확성·표기**뿐. 검증된 결과 박스·부호 사슬·코드 정합·인자표 값은 불가침.

## Gate
PASS_REVIEW_V10 — adversarial 재검수 완료(빈 통과 거부·보완 6건·부호 8/8·인자표 0오류 확인). 다음 = Phase 7.1(v7-11 최종 + 정식 10회, step 34).
