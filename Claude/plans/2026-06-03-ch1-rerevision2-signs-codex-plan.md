# 재수정-2 계획서 — Chapter 1 (그림 제거 + 부호 전수 감사 + Codex 리뷰)

**Date**: 2026-06-03 · **Author**: Claude · **상태**: 계획 + 실행(사용자 "계획서 수립부터 내용 보완까지 진행").
**대상**: `Claude/docs/graphite_ica_ch1.tex` (재수정 후 17p·830줄 GREEN).
**원칙**: 발췌패치 금지(매 편집 후 전 문서 재빌드 + 줄별 정합). 부호는 \*전수\* 감사(한 곳 고치면 사슬 전체 재확인).

---

## §0. 사용자 지시 (이번)

1. **그림 제거**: TikZ staging 모식도 — 크게 도움 안 되고 공간만 차지 → 빼기. (staging \emph{요약 박스}는 작고 유용하니 유지, 그림 참조만 제거.)
2. **부호 전수 재감사**: "조금 이상해 보이는 부호" 가 있음 — 전 문서 signed 양 일관성 점검·교정.
3. **Codex 리뷰**: `/codex:adversarial-review`·`/codex:review` 류로 독립 검토 받기.
방향성: 계획 수립 → 그림 제거 → 부호 감사 + Codex 리뷰 → 교정 → 검증.

## §1. ★ 부호 감사 대상 (전수)

\textbf{선행 발견(Claude 자체)}: \textbf{eq:eqcond ((iii) 전기화학 평형조건)에 부호 사슬 불일치 의심.}
$\xi_j$="방전(탈리튬화) 진행률"인데 eq:mu $\mu(\xi_j)=\mu^0+RT\ln[\xi_j/(1-\xi_j)]$ 를 \emph{리튬화} 반응
$\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}$(전자 일 $-FV_n$)의 평형 $\mu(\xi_{\eq})=\tilde\mu_{\mathrm{Li}^+}
+\tilde\mu_{e^-}$ 에 등치 → $\mu_\mathrm{Li}\propto-FV_n$(감소)인데 좌변 목표는 $+sF(V_n-U_j^0)$(증가). 즉 $\xi_j$(탈리튬화)
의 켤레는 $-\mu_\mathrm{Li}$ 인데 직접 $\mu_\mathrm{Li}$ 에 등치해 \emph{숨은 부호 뒤집기}를 "$s$ 를 붙여"로 가림.
최종 eq:logistic($\xi_{\eq}$ 가 $V_n$ 증가, $s=+1$)은 표준·정확하나 \emph{유도 사슬}이 어긋남. → 교정: 반쪽반응을
\emph{탈리튬화(방전)} 방향으로 쓰거나, $\mu(\xi_j)=-\mu_\mathrm{Li}+$const 임을 명시해 부호를 정직하게.

\textbf{전수 점검 목록(각 부호·일관성 확인)}:
- $s$(방전 $+1$)·$s_I$(전류) 정의와 전 식 일관(eq:vapp $V_\app=V_n+s_I|I|R_n$, eq:affinity $\mathcal A_j=sF(V_\drive-U_j)$).
- eq:eqcond $\mu=sF(V_n-U_j^0)$ ↔ eq:mu ↔ eq:logistic 부호 사슬(위 의심 핵심).
- eq:dxidV $\dd\xi_\eq/\dd V_n=s\,\xi(1-\xi)/w_j$ 의 $s$.
- eq:dUdT $\partial U_j/\partial T=\Delta S_j/(sF)$ — $\Delta G_j=-sFU_j$ 가정 부호.
- eq:bv 정/역 지수 $-(\Delta G_a-\chi\mathcal A)$, $-(\Delta G_a+(1-\chi)\mathcal A)$; eq:db $r^+/r^-=e^{+\mathcal A/RT}$.
- eq:keff $k_j\simeq r^+$, $\mathcal A_j>0$(꼬리 $V_n>U_j$); eq:LqV $\partial\ln L_q/\partial V_\drive=-\chi sF/RT<0$.
- eq:tail 지수 부호·$|V_n-V_a|$; 3×3 표 부호(분극 $+s_I|I|R_n$·$L_V$ 방향).
- 겹침 절 eq:total·부등식 부호.

## §2. 그림 제거

`\begin{figure}...fig:staging...\end{figure}` 블록 삭제. stagebox 의 "(그림~\ref{fig:staging})" 참조 제거.
preamble `\usepackage{tikz}` 제거(미사용). dangling 0 확인(fig:staging 참조 stagebox 1곳만 → 동시 제거).

## §3. Codex 리뷰 (사용자 명시)

`codex:rescue`(또는 `/codex:review`·`/codex:adversarial-review`)로 \*부호 정확성 중심 adversarial review\* 위임.
입력: 현재 tex + §1 부호 의심 1건. 출력: Codex 의 부호·물리·무비약 독립 판정. → Claude 자체 감사와 \*교차\* 후 교정.
(Codex 산출물은 `Codex/` 미수정 원칙 — 리뷰 의견만 수령.)

## §4. 교정 + 검증

Codex + Claude 부호 감사 합치 → 확정 결함 교정(부호 사슬 정합화, 그림 제거). 전 문서 재빌드 GREEN + 적대
재검증(부호·정합·무비약) + dangling 0. result 기록.

## Phase / Gate
- RR2.1 그림 제거 + 빌드 / RR2.2 Codex 리뷰 + Claude 부호 전수 감사(교차) / RR2.3 교정 + 재빌드 + 검증.
- Gate: 부호 사슬 전 식 일관(숨은 flip 0)·빌드 GREEN·dangling 0·Codex+Claude 합치 결함 0.

## Decisions (무응답 시 권고값)
- D-반쪽반응 표기: eq:eqcond 를 \*탈리튬화(방전) 방향\* 반쪽반응으로 재서술(부호 정직). 권고: 그대로.
- D-stagebox: 그림만 빼고 staging 요약 박스 유지. 권고: 그대로(작고 유용).

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-06-03 (RR2 v1) | 그림 제거·부호 전수 감사(eq:eqcond 부호사슬 의심 선적발)·Codex 리뷰 위임 계획. 발췌패치 금지. |
