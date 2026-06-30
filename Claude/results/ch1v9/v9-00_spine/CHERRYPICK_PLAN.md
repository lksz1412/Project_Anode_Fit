# Ch1 v9 — 체리픽 플랜 (검토1 누적 → Opus 체리픽 입력)

> 검토1 R1–R5 의 차원별 체리픽 추천·결함을 누적. master 삼각검증 후 v9c 조립 지침.

## ★확정 사항 — ΔS_e 부호 (master 직접 삼각검증, R1↔R2 충돌 판정)
**확정: ΔS_e ≡ ∂S_e/∂x < 0 (삽입 기준)** — Ch1 ΔS_rxn,j 슬롯과 일관.
- **근거(base_v8-11.tex 직접 검증)**: ① L340 반응식 = 삽입(리튬화) Li⁺+e⁻+[]⇌Li_(흑연) ② L1056 U=(−ΔH+TΔS)/F, stage 2→1 ΔS=−16 → U=(13000−298.15·16)/96485=0.0853V ✓(삽입 기준 음수) ③ L212 사전 "삽입 반응 엔트로피". ⇒ dS_rxn 슬롯=삽입 기준. LCO 전자항도 삽입 기준: x↑(삽입) 시 metal→insulator·g(E_F)↓·S_e↓ ⇒ **∂S_e/∂x<0**.
- **R1 vs R2 판정 = R2 채택**: R1 의 "ΔS_e<0 이 +0.83 mV/K 와 충돌" 은 **전제 오류** — +0.83 은 config+vib 지배(ΔS_e 는 0.18 kB/atom 소량)라 ΔS_e 부호에 **agnostic**(R2 가 정확히 반박). R1 의 v9-02 CRIT 판정은 무효화.
- **★경쟁이 부호-기준 오류 적발**: 유도 최고인 **v9-04·v9-06·v9-01·v9-08·v9-09 가 ΔS_e=−∂S_e/∂x>0(제거-positive)로 주입 = 삽입 슬롯에 역부호(HIGH 5건)**. v9-02·v9-03 이 부호 정확. v9-05 box(+∂x)↔prose(>0) 모순(HIGH).
- ★**체리픽 합성**: 최고 유도(v9-06 게이트·∝T² + v9-04 π²/3·단위다리·분포 5단) 골격에 **정확 삽입 부호(ΔS_e=∂S_e/∂x<0, v9-03/02 규약)** 적용 + 명시 규약 문장("삽입 기준, ΔS_rxn,j 와 일관; 탈리튬화 시 +0.18 kB/atom 방출"). v9-04 Δμ=+sF(V−U) 는 옳음(별개·검증됨).

## 차원별 체리픽 (검토1)
### R1 전자 엔트로피 절 ✅
- **best**: v9-06(1위·MIT 게이트 4항 물리정당화·U-이동∝T² 명시) / v9-04(2위·완전 Fermi 적분 π²/12→π²/3 명시 도출·★단위 다리 eq:dSemolar 자리당 k_B→몰당 R N_A — 9종 단독).
- **조립**: v9-06 골격(게이트 정당화+∝T²) + v9-04 유도(π²/3 도출)·★단위 다리 + v9-03 decomp 박스(이중계산 금지). 부호 −∂S_e/∂x>0. v9-08 좌표분리 2식 = 보조 각주.
- **결함**: v9-02 CRIT(ΔS_e<0 음의 기여), v9-03 HIGH(자기모순), 공통 LOW(단위 다리 v9-04 단독 — 나머지 N_A 단위오류 잠재).

### R2 부호 규약 ✅ (→ 위 ★확정 사항)
- 확정 = 삽입 기준 ΔS_e=∂S_e/∂x<0(흑연 본문 3중 근거). 부호 정확 초안 = **v9-03**(삽입 규약 정확 호명·물리/코드 부호 분리)·v9-02(자기검산 투명). 부호 역전 결함 = v9-01/04/06/08/09(HIGH 5). v9-05 box↔prose 모순.
- 체리픽 부호 = v9-03 규약틀 + **v9-05 의 σ_d 라벨 매핑**(forward 사슬 byte-불변·견고) + v9-06 단전극-전셀 검산. v9-04 Δμ=+sF(V−U) 옳음(검증).
### R3 분포·전이·B ✅
- **분포 프레이밍 최선 = v9-04**(단일자리 Z=1+e^{−βΔμ}→⟨n⟩ Fermi→ξ_eq 5단 (a)-(e) 유도·Ω=0 극한·3-view boxed·전자 Fermi–Dirac 다리). 9종 전부 분포 프레이밍 보유.
- ★**이중계산 B 위반 0건**. 단 v9-03 HIGH(D1): boxed ΔS_j^0=config인데 prose 가 "전체 반응 엔트로피 중심값"으로 재정의→자기모순. **v9-03 분해 prose 이식 금지**.
- 전이표 9/9 GT 일치(v9-03 만 T3 상한 4.20 미표기 LOW).
- 체리픽: **base v9-04 강추**(세 항목 1급), 분해 라벨 v9-05(ΔS^{config,0}) 참고.
- 메타: 추출 "ABSENT" 4건 거짓음성(grep miss) — 랭킹 master 직접 정독 근거.
### R4 흑연 보존·빌드 — (대기)
### R5 G-usable·인용·best-base ✅
- ★**best-base = v9-06(Opus)** — 일반→흑연→LCO 흐름·전자엔트로피 C_e→S_e→부분몰 순서·MIT 게이트 자기일관성·갭 정직·코드 plug-in 최선. (단 LCO bibitem 전무·dangling — 인용 이식 필수.)
- 쟁점1 해소: **v9-05 방식**(ξ=탈리튬화 진행률 고정·σ_d 라벨 매핑) 권고.
- ★★**인용 CRITICAL 전면 재구축**: 9종 LCO bibitem 부실 — v9-01 ml2024="(Tier G) Internal note"(허위), v9-04 reynier2004=엉뚱한 논문, **9종 모두 Xia 2007 올바른 bibitem 없음**, motohashi 연도 오류(PRB 80 2009가 정답). v9-03 ml2024 placeholder 표기가 가장 정직.
- G-usable/tier 정직 최선 = v9-06·v9-05.

## ★체리픽 필수 액션 — LCO 참고문헌 전면 재구축 (R5)
추출카드(`20_extraction/`)·`10_sources_master.md` 의 검증 DOI 로 LCO bibitem 새로 작성(작가들 부실 bibitem 폐기):
- Reimers & Dahn 1992, JES 139, 2091 — 10.1149/1.2221184
- Ménétrier & Delmas 1999, J. Mater. Chem. — 10.1039/a900016j
- Motohashi 2009, **PRB 80**, arXiv 0909.3556(전자 상도)
- Xia/Ceder 2007(dQ/dV) — 추출카드 `xia_ceder_2007_dqdv.md` 정확 ref 확인
- Reynier/Yazami 2004(entropy)·Reynier thermal 2009(JPS S0378775309021119) — 카드 확인
- ML order–disorder 2024 = **G. H. Teichert, S. Das, M. Faghih Shojaei, J. Holber, T. Mueller, L. Hung, V. Gavini, K. Garikipati, "Bridging scales with Machine Learning … LixCoO2", J. Mech. Phys. Solids 190, 105727 (2024)**, DOI 10.1016/j.jmps.2024.105727, arXiv 2302.08991. ★**저자 확정**(WebSearch 검증) — v9-03 의 "R. Aronson"은 **fabrication**(폐기). 체리픽은 Teichert et al. 사용.

## ★인용 정정 — 9b 검증서 적발 (체리픽 확정 인용)
- **+0.83 mV/K 단전극 LCO** = Reynier 아님 → **Świderska-Mocek et al., Phys. Chem. Chem. Phys. 21, 2115 (2019), 10.1039/c8cp06638h**(추출카드 reynier_thermal_2009 의 오기 — v9-05 웹검증). 체리픽은 Świderska-Mocek 사용.
- **MSMR Part I** = JES 아님 → **ECS Advances 3, 042501 (2024)**(Paul/Wolfe/Verbrugge 외)(v9-05 검증). [Part II 는 JES 2024 ad70d9 — 카드 확인]
- **Reynier 2004**(0.18 kB/atom·Sommerfeld·config 지배) = **PRB 70, 174304 (2004)**(JES 151 A422 companion). 이건 유지.
- ml2024 = **Teichert et al., JMPS 190, 105727 (2024)**, 10.1016/j.jmps.2024.105727, arXiv 2302.08991.
→ ★체리픽 인용 마스터: Reimers&Dahn(10.1149/1.2221184)·Ménétrier&Delmas JMC9 1135(10.1039/a900016j)·Motohashi PRB80 165114(arXiv 0909.3556)·Xia/Lu/Meng/Ceder JES154 A337(10.1149/1.2509021)·Reynier PRB70 174304·**Świderska-Mocek PCCP21 2115(10.1039/c8cp06638h)**·**MSMR ECS Adv3 042501**·Teichert JMPS190 105727.

## ★검토2 V2 — 인용 마스터 확정 (체리픽은 이걸 그대로 사용)
- **검증된 LCO bibitem 8건 완성형** = `review2/V2_citations_master.md`. 인용 최정확 보완본 = **v9-05**(여기서 인용부 graft).
- DOI 확정: Reynier PRB70 174304 = 10.1103/PhysRevB.70.174304 · MSMR ECS Adv3 042501 = 10.1149/2754-2734/ad7d1c · Świderska-Mocek = 10.1039/c8cp06638h.
- ★체리픽 필수: v9-03 ml2024 "R.Aronson" 폐기→Teichert. +0.83 mV/K 6종 오귀인→Świderska-Mocek. MSMR 구버전 3종→ECS Adv.

## ★주의 — 인용 fabrication 감시 (9b 보완 중 발견)
9b 보완 작가들이 인용 재구축 시 *저자명·연도를 임의 생성*할 위험(v9-03 "R. Aronson" 사례). 체리픽 시 **모든 LCO 인용을 추출카드(full-text 정독분)·확정 ref 와 대조** 후 채택. 확정 ref: Teichert(위)·Xia/Lu/Meng/Ceder 2007·Motohashi/Ono/Sugimoto PRB80·Reimers/Dahn·Ménétrier/Delmas·Reynier/Graetz/…/Yazami/Fultz 2004.

## ★조립 스펙 확정 (검토2 V1·V2)
- **base = v9-06**(부호 PASS·흐름·단/전셀 분리·∝T²·4항 게이트 1위).
- **graft map**: 규약문=v9-03 / 유도rigor+단위다리+게이트 닫힌식=v9-04 / 분포 5단·3-view=v9-04 / decomp(이중계산B)=v9-03 / σ_d 매핑=v9-05 / **★LCO 참고문헌 통째=v9-05**(`review2/V2_citations_master.md` 마스터 8건) / 부호 self-test=v9-02.
- **★이식 금지(do-not-port)**: v9-03 bibitem(Aronson fabrication·CRIT)·v9-04 bibitem(dangling)·v9-06 익명 ml2024·v9-01 캡션.
- **조립 후 정정**: v9-01 캡션 "양봉우리"→"음봉우리"(혹시 graft 시)·v9-07 부등식 명시·v9-08 오타 — base=v9-06 라 대부분 무관, graft 시만 주의.
- 절차: v9-06 복사 → 위 graft → V2 마스터 인용 8건 삽입(작가 bibitem 폐기) → ΔS_e=∂S_e/∂x<0 전수 확인 → 이중계산 B 확인 → xelatex 0-error → 정식 10회 → v9-11.
