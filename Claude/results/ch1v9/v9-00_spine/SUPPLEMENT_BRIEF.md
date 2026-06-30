# Ch1 v9 — 검토1 종합 + 9b 보완 브리프 (방향성-만, 구체 코드 X)

> 검토1 R1–R5 종합. 각 작가는 *자기 초안*을 방향성 따라 개선(독립·다른 초안 복사 금지). 구체 코드 제공 안 함 — 방향만.

## 검토1 종합 (5 차원)
- **R1 전자엔트로피**: 최선 v9-06(게이트 4항 정당화·∝T²)·v9-04(π²/3 명시 도출·단위 다리). v9-02/03 유도 약함.
- **R2 부호 ★확정**: ΔS_e = **삽입 기준 ∂S_e/∂x < 0**(Ch1 ΔS_rxn,j 슬롯=삽입 반응 엔트로피와 일관; 흑연 L212/L340/L1056 근거). 부호 정확=v9-02/03. **역부호(제거-positive >0) 결함=v9-01/04/06/08/09(HIGH 5)**. v9-05 box↔prose 모순.
- **R3 분포·B**: 분포 프레이밍 최선 v9-04(5단 유도). 이중계산 B 위반 0건. v9-03 분해 prose 자기모순(D1).
- **R4 보존·빌드**: 9/9 흑연 verbatim·빌드 0err. overfull=신규 LCO 표만(수정). lhead/title 미갱신(v9-06/07/08/09).
- **R5 인용 ★CRIT**: LCO bibitem 전면 부실 — 허위/엉뚱 논문/연도 오류. best-base 흐름=v9-06.

## ★공통 보완 방향 (전 9종)
1. **ΔS_e 부호 = 삽입 기준 ∂S_e/∂x < 0 으로 통일**. 너의 흑연 본문(인자 사전 "삽입 반응 엔트로피"·반응식 Li⁺+e⁻+[]⇌Li·stage 2→1 ΔS=−16→U=0.085 round-trip)을 확인해 ΔS_rxn 슬롯이 삽입 방향임을 자가검증한 뒤, ΔS_e 도 *같은 삽입 방향*으로(x↑ 삽입 시 metal→insulator·S_e↓ ⇒ ∂S_e/∂x<0). **명시 규약 문장** 1개 넣어라("삽입 기준, ΔS_rxn,j 와 일관; 물리적으로 탈리튬화 시 +0.18 kB/atom 방출"). +0.83 mV/K 은 config+vib 지배라 ΔS_e 부호 제약 안 함(sanity 오용 금지).
2. **LCO 참고문헌 전면 재구축**(카드에 *정확 ref 전부 있음* — `20_extraction/` 정독해 그대로 사용):
   - Reimers & Dahn, JES **139**, 2091 (1992) — 10.1149/1.2221184
   - Ménétrier, Delmas 외, J. Mater. Chem. **9**, 1135 (1999) — 10.1039/a900016j
   - Motohashi 외, "Electronic phase diagram of LixCoO2", **Phys. Rev. B 80, 165114 (2009)** — arXiv 0909.3556
   - **Xia, Lu, Meng, Ceder, JES 154(4), A337–A342 (2007) — 10.1149/1.2509021**(★9종 모두 누락·이게 정답)
   - Reynier, Graetz, … Yazami, Fultz, "Entropy of Li intercalation in LixCoO2", **JES 151, A422 (2004)** (동 그룹 **PRB 70, 174304 (2004)**) — ★"전자+config 가 MIT 서 comparable"(우리 설계 지지)
   - Wang, Reynier 외, JPS (2009) — S0378775309021119(단전극 ΔS·thermal mgmt)
   - Garikipati 그룹, "Bridging scales with ML … LixCoO2", **J. Mech. Phys. Solids 190, 105727 (2024)** — arXiv 2302.08991(★config 단독 MIT 2상역 재현 실패 = 전자항 필요 증명)
   ★허위 "internal note"·엉뚱 논문·연도 오류 0. 못 구한 건 정직 tier.
3. **LCO 표 overfull 수정**(폭 줄임/구조조정 — 흑연 표 건드리지 마라).
4. **흑연 VERBATIM 유지**(이미 PASS — 절대 훼손 금지). lhead/title 갱신(LCO 통합 반영).
5. 자체 재검수 후 xelatex 0-error 재확인.

## 개별 방향 (자기 것만)
- **v9-01**: 부호 역전 정정·ml2024 허위인용("internal note")→실제 논문·motohashi PRB80 2009·단위 다리 추가.
- **v9-02**: 전자엔트로피 유도 깊이 보강(π²/3 명시 도출)·xia2006→xia2007·부호는 유지(정확).
- **v9-03**: ★D1 정정(decomp prose 가 ΔS_j^0 을 "전체 중심값"으로 재정의→config 한 항으로 일관)·T3 상한 4.20 표기·ml2024 placeholder→실제 ref·부호 유지.
- **v9-04**: 부호 역전 정정(제거>0→삽입<0)·reynier2004 엉뚱논문 정정·우수한 유도/단위/분포 5단 유지.
- **v9-05**: box(+∂x)↔prose(>0) 모순 정정(삽입 ∂S_e/∂x<0 으로 통일)·σ_d 매핑틀 유지.
- **v9-06**: 부호 역전 정정·LCO 표 overfull 수정·bibitem 추가(dangling 제거)·게이트 정당화/흐름 유지.
- **v9-07**: 부호 삽입<0 확정·+0.83 단전극 검산 추가·인용 재구축·lhead 갱신.
- **v9-08**: 부호 역전 정정·+0.83 추가·인용 재구축·lhead 갱신.
- **v9-09**: 부호 역전 정정·LCO 표 overfull·인용 재구축·lhead 갱신.

## 산출
개선된 v9-0X.tex(같은 파일 갱신, xelatex 0-error). 짧은 노트(반영한 보완·부호 확정·인용 재구축·overfull 해소). 반환 8줄 이내.
