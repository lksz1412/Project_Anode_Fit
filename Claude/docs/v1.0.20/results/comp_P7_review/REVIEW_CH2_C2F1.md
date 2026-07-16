# REVIEW_CH2_C2F1 — v1.0.20 Ch2 + appendix 독립 검수 (검수자 C2F1)

> 검수 일시: 2026-07-16. 대상: `_sections/ch2_*.tex` 16종 + `appendix_phase_separation.tex`.
> 대조 구본: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.19/` 동명 파일 (read-only).
> 기준 문건: V1020_STYLE_RUBRIC.md · V1020_REFERENCE_LEDGER.md · V1020_CHANGE_LOG.md · V1020_P1_CITATION_BASELINE.md (4종 전문 정독 완료).
> 검수 3축: ① 신본 자체 결함 / ② v1.0.19 대비 regression / ③ 신설 다리(C-017·C-018·B-005·C-019·U9·U10) 물리·서지 정확성 + 교차 정합(Ch1 §N 리터럴 참조 전건).
> 다른 REVIEW_*.md 미열람 (독립성 준수).

## 발견 표 형식

| # | 위치(파일:행) | 심각도(H/M/L) | 축(①/②/③) | 발견 | 근거 | 제안 |

---
### ch2_sec00_intro.tex (전문 정독 완료, 68행)

- ② 구본 대비: `diff` 결과 **완전 동일** — regression 없음.
- ③ 교차 정합: L8 "Chapter 1 §3 의 평형 중심 전위" — Ch1 신본 절 번호 매핑(§3=ch1_sec03_center, TOC 1.3) 일치, 식 자체도 ch1_sec03:53 `\boxed{U_j(T)=(-\Delta H_{\rxn,j}+T\,\Delta S_{\rxn,j})/F}` 와 문자 일치. L61 "Chapter 1 §15" — §15=ch1_sec15_lcoelec(LCO 전자 엔트로피 항) 제목·내용 일치.
- ① refute 시도: L18–19 "SOC 에 따라 부호를 바꾸고($x$ 작을 때 양, 클 때 음)" — 이상 격자기체 $S_\config=-R\ln[\theta/(1-\theta)]$ 유래 $\partial U/\partial T$ 는 $\theta\to0$ 에서 $+$, $\theta\to1$ 에서 $-$ 로 정합(반박 실패 — 서술 옳음). L26 $\dot Q_\rev=-IT\,\partial U_\oc/\partial T$ 부호 규약은 §7 정독 시 재대조 예정.
- 발견: 없음 (컴파일 로그 미해결 참조 0 확인).

