# W4 저작 NOTES — v1.0.24 R1 (concision + completeness 강조)

작업 sub W4. 초안 3소절(`gr_2L.tex`·`si_fr.tex`·`lco_omega.tex`)만 저작. 실제 문건·git 미변경. 아래는 근거·가정·불확실점·신규 서지·마스터 이관 사항.

## 0. W4 강조 반영 (최소 정확형)
- 문장 전부 load-bearing, filler·타 소절 recap 없음(모두 inline `\S\ref`/`\eqref`). 물리적으로 자기완결.
- 세 소절이 공유하는 핵(정규용액/Frumkin 커널 = `eq:eqpeak` 의 Ω-일반화)은 각 소절에서 **압축 유도**(복붙 recap X). 세 소절 동시 병합 시 중복 최소화 옵션은 §6 참조.

## 1. 읽은 원천 (행 근거)
- `results/AUTHOR_BRIEF.md`(전문), `results/REFLECT_SEED_TABLE.md`(전문 — 확정 물리·값·서지 최우선).
- 흑연: `_sections/ch1_sec05_width.tex`(폭 이중지위·`eq:wbase`·`eq:xieq`·`eq:eqpeak`↔), `ch1_sec06_eqpeak.tex`(평형 peak `eq:eqpeak`), `ch1_sec07_broadening.tex`(두-상/고용체 부류 `sec:broadening-class`·L20-26·three-source 폭예산), `ch1_sec10_sum.tex`(`tab:staging` L32-43: 4→3/3→2L/2L→2/2→1, ΔS=+29/0/−5/−16), `ch1_sec03_center.tex`(`eq:Uj`·∂U/∂T=ΔS/F), `ch1_sec02b_part0.tex`(`eq:mu`·`eq:gxi`), `ch1_sec04_hys.tex`(`eq:spinodal`·`eq:Veq`).
- LCO: `ch1_sec11_lcointro.tex`(`tab:lco-staging` L66-77: T1 3.90/T2 4.05/T3 4.17·`sec:lco-direction`·`eq:lco-sigmaslot`), `ch1_sec12_lcocenter.tex`(`eq:lco-dUdT`·`eq:lco-kirchhoff`), `ch1_sec13_lcohys.tex`(`eq:lco-gxi`·`eq:lco-spinodal`·`eq:lco-mit`·#7 대상 문구 L154 `eq:br-vanderven1998-1` + 혼동 가드 L169-178), `ch1_sec15_lcoelec.tex`(`eq:dSegate`·−45.7 J/mol/K·`eq:U1T2`·T_ref 동결·`sec:lco-Se-scale`), `ch1_sec16_lcopeak.tex`(`eq:lco-eqpeak`), `ch1_sec17_msmr.tex`(MSMR `eq:msmr`·ω↔w 흡수).
- Si: `_sections/ch3v22_sec02_cases.tex`(`tab:si-cases`·`ssec:si-elemental/siox/sic`·c-Li15Si4 결정화), `ch3v22_sec03_blend.tex`(`eq:blend-dqdv`·`ssec:si-blend-gs2`·`ssec:si-carry`), `ch3v22_notation.tex`(host 첨자 규약).
- 물리 확정 근거: `Claude/results/comp_v24/GRAPHITE_STAGING_XRD.md`(Dahn 5-feature·Ω 판정자·6+ 폐기), `T_SPLIT_FINDING.md`(stage-2L 0.30 mV/℃·재현 0.271·Schmitt 2022·코드 무결).
- preamble: `common_preamble_v1024.tex`(박스 keybox/verifybox/srcbox·매크로 \dd\eq\rxn\cat\kB\code), `ch1_preamble.tex`(keybox/verifybox 존재 — GR-2L 안전).
- 드라이버: `ch2_lco_v1.0.24.tex`(LCO 섹션 + `ch2v22_bib`), `ch3_si_v1.0.24.tex`(common_preamble + externaldocument ch1·ch2 + `ch3v22_bib`).

## 2. 라벨 규약 선택 (마스터 확인 요망)
- 브리프 §4 는 `ssec:` 예시이나 §2·§5 는 **장 관행 계승**을 요구 → 장별 관행을 따랐다:
  - ch1(흑연 GR-2L)·ch2(LCO Ω) 소절은 **`sec:`** 접두(ch1/ch2 subsection 관행: `sec:width-w`·`sec:lco-hys-od` 등).
  - ch3(Si FR) 소절은 **`ssec:`** 접두(ch3 관행: `ssec:si-elemental` 등).
- 신규 라벨(중복 0 확인): `sec:gr-staging2L`·`eq:gr2l-crit`·`eq:gr2l-tsplit` / `ssec:si-frumkin`·`eq:si-fr-V`·`eq:si-fr-dqdv` / `sec:lco-omega`·`eq:lco-omega-kernel`·`eq:lco-etoggle`.
- 배치: GR-2L = `\S\ref{sec:width}` 뒤(단, 내용상 `sec:broadening` 인접도 가능 — 마스터 판단). SI-FR = `sec:si-cases` 인접. LCO-Ω = `sec:lco-hys`·`sec:lco-electronic`·`sec:lco-peak` 인접.

## 3. 신규 `\cite` key (본문 임의 bibitem 금지 준수 — 아래를 해당 장 bib 에 추가)
기존 key 최대 재사용. 신규 2건:
- **`schmitt2022`** (ch1 bib, GR-2L). 서지 초안:
  `\bibitem{schmitt2022} J. Schmitt et al., "Graphite delithiation differential voltage analysis resolving the stage-2L feature," (2022). [탈리튬화 dV/dQ 에서 stage-2L 분리 재확인.]`
  ⚠ **tier/검증**: 출처 = `T_SPLIT_FINDING.md`(이 세션 확정 산출, "verifiable"로 등재)이나 정확한 **저널·권·쪽·DOI 는 seed 에 미기재** → 마스터가 서지 확정 필요(무근거 DOI 조작 금지 원칙으로 공란 둠). 물리 주장(방전-음극 2L 분리)은 Dahn 상도표로 이미 tier B 지지.
- **`artrith2018`** (ch3 bib, SI-FR). 서지 초안:
  `\bibitem{artrith2018} N. Artrith, A. Urban, G. Ceder, "Constructing first-principles phase diagrams of amorphous Li$_x$Si using machine-learning-assisted sampling with an evolutionary algorithm," \emph{J. Chem. Phys.} \textbf{148}, 241711 (2018). DOI: 10.1063/1.5017661.`
  ⚠ seed(`REFLECT_SEED_TABLE §1`)의 "Artrith 2018 JCP148,241711" 와 권·쪽 일치. DOI 는 최선 추정 → 마스터 1차 확인 권장(tier: 서지 A 후보, 미최종검증).

기존 재사용 key(전부 확인됨): GR-2L = `dahn1991·ohzuku1993·reynier2003`(ch1). SI-FR = `chevrier_dahn2009·obrovac_christensen2004·limthongkul2003·tu_blend2024`(ch3). LCO-Ω = `motohashi2009`(ch2). 나머지 근거는 인접 절 `\S\ref` 로 계승(중복 cite 회피 = W4 concision).

## 4. 사용 값·tier (시드표 근거, 임의 수치 0)
- GR-2L: Δ(ΔS)≈29 J/(mol·K)(Dahn 분리기울기 역산, **tier B** — 직접 열량계 아님) → 0.30 mV/℃; 재현 0.271(이 세션 `T_split.png`); T_m≈10℃(율/이력 의존 근사); seed 쌍 +15/−14(2L 시드, tier C — `tab:staging` 현 0/−5 placeholder 갱신용). Ω/RT>2 두-상 확증(이 세션 regsol fit, tier B).
- SI-FR: w/(RT/F)≈[1.5,2.7,1.1](이 세션 `regsol_si`, tier B) vs 흑연 두-상 ≪0.12; c-Li15Si4 ~50–60 mV(tier A `obrovac_christensen2004`); a-Si 경사 U(x)(tier A 함수형·Ω 값 tier C).
- LCO-Ω: ΔS_e≈−45.7 J/(mol·K) 골 깊이(`eq:dSegate`·`sec:lco-Se-scale` 검산값); +1.25%p per-peak Ω(이 세션 `lco_ablation`, tier B); R²=0.944≈흑연 0.940(이 세션 `LCO_DIAGNOSIS`, tier B). g_max=13·x_MIT=0.85 는 인접 절 계승(재기술 X).

## 5. 마스터 이관: 정직 공백·긴장(honest gaps)
1. **broadening-class 재분류 긴장 (중요).** 현 `ch1_sec07_broadening` `sec:broadening-class`(L15,L20-26)는 **3L→2L 을 연속 고용체 부류**로 넣는다. 그러나 Dahn XRD(GR-2L §1)는 **3↔2L 을 두-상**으로 확정한다(고용체 예외는 4↔3 뿐). GR-2L 은 XRD 확정 분류를 제시 → **`sec:broadening-class` 문구와 상충**. 마스터가 §7.1(3L→2L 귀속)을 XRD 분류로 정합화 필요. (물리 골격·`eq:eqpeak` 불변; 분류 라벨만.)
2. **`tab:staging` ΔS placeholder.** 현 표: 3→2L=0.0, 2L→2=−5.0(Δ=5→0.05 mV/℃, 미분리). stage-2L 분리 실현 시드 = +15/−14(Δ=29). GR-2L 은 이를 **피팅 시드**로 명기(표 실제 수정은 마스터 몫 — P5 값 보존).
3. **LCO feature 명명.** 브리프 LCO-Ω 는 "3.70V(O2)/3.90V(O3) 두-상 sharp"를 언급하나, 확정 `tab:lco-staging`(T1 3.90/T2 4.05/T3 4.17, `menetrier1999`·`reynier2004`)와 **전위·명명이 불일치**. P5·게이트 6(Chapter 1 기준식 정합) 준수 위해 **확정 T1/T2/T3 명명 유지**하고 브리프의 O2/O3 라벨은 미채택. 마스터가 O2/O3 도입 의도면 별도 지시 필요(현 표와 충돌 위험 명시).
4. **regsol2 Ω 벡터 모호성.** seed 의 Ω/RT=[4.06,2.02,3.55,4.07] 는 "전부>2RT 두-상 확증"이나, 4전이 **순서(4↔3 포함 여부)** 불명. 4↔3=고용체(Ω<2RT) 원칙과 충돌 소지 → GR-2L 은 벡터 미인용·정성("두-상 후보 Ω/RT>2")로만 처리. 마스터가 `regsol2.png` 로 전이 대응 확인 권장.
5. **#7 정정 지점.** 실제 대상 문구 = `ch1_sec13_lcohys` `eq:br-vanderven1998-1`(L154 "$\Omega_j^\mathrm{cat}>2RT\Leftrightarrow x\approx\tfrac12$ 질서상 안정") + 기존 혼동 가드(L169-178). LCO-Ω 의 keybox 가 **정정 문구**(Ω=상호작용 에너지·config=별도 슬롯). in-place 문구 교체는 마스터 편집 소관(초안만 제공, 물리 유지·문구만).
6. **전자항 토글 bit-exact 주의.** 기본 OFF 가 기존 커브 bit-exact 이려면 현 코드(ΔS_e 상시 ON)의 **ΔH 재기준(U(298) 보존)**이 R2 게이트에 필요 — LCO-Ω verifybox(i)에 명시. R2(코드) 반영 사항.

## 6. 병합 최적화 옵션 (마스터 재량)
- 세 소절 모두 Frumkin/정규용액 커널 = `eq:eqpeak` 의 Ω-일반화. 세 소절 동시 채택 시, GR-2L `eq:gr2l-crit`(판정자)를 정본으로 두고 SI-FR/LCO-Ω 이 이를 `\eqref` 하면 유도 1회로 축약 가능(현재는 각 소절 **독립 병합** 가능하도록 자체 유도 — 자기 신규 라벨 상호참조 회피). concision 우선이면 전자, 독립성 우선이면 현행 유지.
- 크로스참조는 전부 **확정 기존 라벨**(`eq:mu`·`eq:spinodal`·`eq:eqpeak`·`eq:blend-dqdv` 등, externaldocument 도달 확인)만 사용 — 신규 라벨 상호참조 0(파일별 독립 컴파일 안전).

## 7. 검증 수행
- 브레이스·`$`·`\begin/\end`·환경 균형: 3파일 전부 통과(각 boxed≥1, 전 식 라벨). 크로스참조 대상 라벨 14종 존재 확인. 박스 환경(keybox/verifybox/srcbox) 드라이버 preamble 가용 확인.
- 미수행(불가): 전체 xelatex 컴파일(드라이버 통합·bib 추가는 마스터 몫). 신규 bibitem 2건 추가 후 3-pass 필요.
