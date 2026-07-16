# REVIEW_O3 — v1.0.20 독립 검수 (검수자 O3)

- 담당: 독립 검수자 O3 (다른 창 O1/O2/F1 과 통신·산출물 참조 없음)
- 역할: Ch1 LCO 청크(§11–§17) + ch1_bib 전문 정독 + 3축 검수(①신본 결함 ②v1.0.19 regression ③신설 다리 물리·서지)
- 담당 청크: ch1_sec11_lcointro · ch1_sec12_lcocenter · ch1_sec13_lcohys · ch1_sec14_lcodecomp · ch1_sec15_lcoelec · ch1_sec16_lcopeak · ch1_sec17_msmr · ch1_sec18_inputs · ch1_bib
- 신본: /home/user/Project_Anode_Fit/Claude/docs/v1.0.20/_sections/
- 구본(대조 read-only·불가침): /home/user/Project_Anode_Fit/Claude/docs/v1.0.19/_sections/
- 심각도: H=물리·수식 오류/오귀속 · M=유도 비약·정합 결손·regression · L=표기·문장·일관성
- 축: ①신본 자체 결함 · ②v1.0.19 대비 regression · ③신설 다리 물리·서지

---

<!-- 파일별 발견분을 정독 완료 즉시 append -->

### ch1_sec11_lcointro.tex (전문 정독 완료, 173행)

구본(173행)과 신본은 **두 곳의 인용 추가만** 차이: (i) L42 `세 전이를 남긴다\cite{xia2007}` (구본 무인용) (ii) L165 `MSMR 모델\cite{msmr_origin2017,msmr2024}` (구본 무인용). 둘 다 P4 의도된 인용 부여(RESULT_P4 "sec11 MSMR cite")·원장 V1 키(xia2007=A·msmr_origin2017=B·msmr2024=A). regression 없음.

물리·부호 검산: σ_d=+1⟺탈리튬화(산화·ξ:0→1·전위↑) 프레임이 흑연(방전↦+1)/LCO(충전↦+1) 양 전극에서 일관. 3작용처(분극 V_app>V_n·분기 탈리튬화=상가지·꼬리 적분방향) 부호 1:1 유지 — 모순 없음. w_j=n_jRT/F 차원 [V] 정합. 표 tab:lco-staging: T1(MIT ~3.90V·x0.94–0.75·center 0.85)·T2/T3(order–disorder, x≈0.55/0.48 = x=0.5 단사정 왜곡 좌우)·전위 오름차순(탈리튬화 x↓→V↑) 정합.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 1 | ch1_sec11:42 | L | ③ | "세 전이를 남긴다\cite{xia2007}" — MIT+order–disorder 2종의 전이 **동정(同定)** 은 고전적으로 Reimers–Dahn1992·Ohzuku·Menetrier 계보인데 이 문장엔 xia2007 단건만 부여 | L48 각주는 Xia·Reynier·Motohashi 3종으로 넓히나, L42 문장 자체는 xia2007 단건. 원장상 xia2007=V1 유효키라 오류는 아님 | (선택) L42 전이 동정 문장에 reimers1992 병기 검토 — 현행도 각주가 보완하므로 결함 아님 |
| 2 | ch1_sec11:165 | L | ③ | MSMR "표준 파라미터화" 명명 주장에 `msmr_origin2017,msmr2024` 인용 — "MSMR" **명명** 원전 bakerverbrugge2018 은 여기 미포함 | §17 계보 3단에서 명명 원전 별도 부여 예정(원장 B·CHANGE_LOG C-016). preview 성격상 원전+온도판 인용은 허용 범위 | 결함 아님(§17 에서 명명 원전 처리 확인 요) |



