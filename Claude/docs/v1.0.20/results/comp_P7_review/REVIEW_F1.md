# REVIEW_F1 — v1.0.20 독립 검수 (검수자 F1)

> 담당 청크: `_sections/ch2_sec00_intro.tex` ~ `ch2_sec10_closing.tex` · `ch2_appA_traps.tex` · `ch2_appB_codemap.tex` · `ch2_bib.tex` · `ch2_preamble.tex` + `appendix_phase_separation.tex` (전문 정독).
> 검수 3축: ① 신본 자체 결함 · ② v1.0.19 대비 regression · ③ 신설 다리(P5 인용·B-005 중간식·교차 참조)의 물리·서지 정확성.
> 기준 문건 정독 완료: V1020_STYLE_RUBRIC.md · V1020_REFERENCE_LEDGER.md · V1020_CHANGE_LOG.md · V1020_P1_CITATION_BASELINE.md.
> 심각도: H=물리·수식 오류/오귀속 · M=유도 비약·정합 결손·regression · L=표기·문장·일관성. 축: ①/②/③.
> 다른 검수 창(O1/O2/O3) 산출물 미참조. 문서 파일 무수정(read-only) — 본 파일만 기록.

## 발견 목록

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|

### ch2_sec00_intro.tex (전문 정독 완료, 69행)
- ② regression: v1.0.19 와 바이트 동일(diff 무변경) — regression 없음.
- ③ 교차: L8 "Chapter 1 §3 의 평형 중심 전위" — Ch1 신본 `ch1_sec03_center.tex` eq:Uj(L53) $U_j(T)=(-\Delta H+T\Delta S)/F$ 와 문자 일치 확인. L61 "Chapter 1 §15" — Ch1 toc §1.15 = LCO 전자 엔트로피 항, 일치.
- refute 시도: L26 $\dot Q_\rev=-IT\,\partial U_\oc/\partial T=-(IT/F)\Delta S(x)$ — $\partial U_\oc/\partial T=\Delta S/F$(L49 사슬 박스)와 자기정합. 부호 규약의 실체 검증은 sec07 정독에서 수행(후술).

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| F1-01 | ch2_sec00_intro.tex:20–21 | L | ① | "상수 엔트로피는 SOC 축 위에서 봉우리·골·부호 반전을 만들 자유도 자체가 없다"는 동기 서술이 다전이 겹침 하에서는 과장 — 전이별 상수 $\Delta S_j$ 라도 부호가 다르면 겹침 가중 블렌드(본 장 파생 A 자신)만으로 SOC 축 부호 교대·계단형 요철은 재현 가능. 재현 불가한 것은 봉우리 내부 발산(config 부분몰 꼬리)과 비계단 연속 모양이다 | 파생 A(ch2_sec05) 자신이 $\sum_j w_j[\Delta S_j/F+\text{config}]$ 로 모양을 만듦 — config 항 없이도 $w_j$ 블렌드가 $x$-의존 생성. v1.0.19 동문(신규 결함 아님) | "봉우리 내부의 발산·연속 모양까지는 만들 수 없다" 수준으로 한정하는 후보(v1.0.21). 서론 동기 문단이므로 존치 가능 |
