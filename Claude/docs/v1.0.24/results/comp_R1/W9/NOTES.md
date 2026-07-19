# NOTES — comp_R1 저자 sub **W9** (강조: adversarial completeness + honest limits)

> 3개 신규 소절 초안: `gr_2L.tex` · `si_fr.tex` · `lco_omega.tex`.
> 4-tier 표기: **확정**(1차/시드 확정) · **근거미발견** · **추정/시연(tier C)** · **미검증**.

---

## 0. 경계 준수 (self-check)
- 초안만 저작. 실제 문건(`_sections/*.tex`) **미편집**·git 미실행. 출력 = `results/comp_R1/W9/` 전용.
- 기존 라벨·기호·식 **재정의 0** (계승만). 신규 라벨은 `ssec:`/`eq:` prefix + 소절 고유 접두(`gr2l`/`sifr`/`lcoomega`)로 중복 회피.
- 물리 골격 불변: 전하 보존 중심식·`V_n` 구분·MSMR 동형 유지. 시드표 값 임의 변경 X.
- 경쟁 저작 무결성: 타 창(W1·W6 등) 산출물 **미열람** — 독립 초안.

## 1. 읽은 파일 (근거)
| 파일 | 용도 |
|---|---|
| `results/comp_R1/AUTHOR_BRIEF.md` | 임무·사양·규칙 |
| `results/REFLECT_SEED_TABLE.md` | **확정 물리·값·서지(최우선)** — @1 Si·@2 흑연5feature·@3 전자토글·#7 |
| `_sections/ch1_sec05_width.tex` (L264–319) | 폭 `w_j=n_jRT/F`·이중지위·Ω>2RT 두-상 규약·`eq:wbase`·`eq:xieq` |
| `_sections/ch1_sec06_eqpeak.tex` | 평형 peak `eq:eqpeak`·종 항등식 `eq:belliden` |
| `_sections/ch1_sec03_center.tex` | `eq:Uj`·`∂U/∂T=ΔS_rxn/F`·`fig:UjT`(4전이 ΔS=+29/0/−5/−16) |
| `_sections/ch1_sec10_sum.tex` (L20–62) | `tab:staging` 4전이 초기값(U·ΔH·ΔS·Ω·w) |
| `_sections/ch3v22_sec02_cases.tex` | Si 3계열 개형·`tab:si-cases`·`fig:si-cases-shape` |
| `_sections/ch3v22_sec03_blend.tex` | 공통-μ 블렌드 `eq:blend-dqdv`·`eq:blend-balance`·GS-2 |
| `_sections/ch3v22_notation.tex` | Si host 첨자·`f_Si`·기호 계승 규약 |
| `_sections/ch1_sec13_lcohys.tex` | 정칙용액 Ω·spinodal `eq:lco-gpp/spinodal`·**#7 정정 대상 문구**·혼동 가드·`eq:lco-dope` |
| `_sections/ch1_sec14_lcodecomp.tex` | ΔS 삼분해 `eq:lco-decomp`·슬롯 규칙·`eq:lco-dUdT` |
| `_sections/ch1_sec15_lcoelec.tex` | 전자항 `eq:dSegate/dSemolar`·`eq:U1T2`·게이트·−45.7 J/mol/K |
| `_sections/ch1_sec16_lcopeak.tex` | LCO 세 peak `eq:lco-eqpeak`·폭 지위·T1 온도신호 |
| `_sections/ch1_sec11_lcointro.tex` (L40–109) | `tab:lco-staging`·방향규약 `eq:lco-sigmaslot` |
| `_sections/common_preamble_v1024.tex`·`ch1_preamble.tex` | 매크로·박스환경(keybox/verifybox/signbox/warnbox/srcbox…) |
| `ch1v22_bib.tex`·`ch2v22_bib.tex`·`ch3v22_bib.tex` | 기존 `\cite` key 확인 |

## 2. 소절별 물리 근거 (시드 대응)

### gr_2L.tex — 흑연 stage-2L·XRD 5-feature (**시드 @2**)
- **확정**: XRD 5-feature(dilute 1′↔4·4↔3 고용체 shoulder·3↔2L·2L↔2·2↔1 = 두-상4+고용체1), Dahn1991.
- **판정자** `dμ/dθ|½ = 4RT−2Ω` (`eq:gr2l-disc`) 유도 = `eq:lco-gpp`(=`eq:gpp`) 대칭점 회수. `μ(θ)=μ°+RT ln[θ/(1−θ)]+Ω(1−2θ)`.
- **확정(우리 진단)**: regsol2 `Ω_j/RT=[4.06,2.02,3.55,4.07]` 전부>2 (두-상 확증). 경계값 2.02(3↔2L) 민감 지점 명기.
- **stage-2L T-split**: `Δ(ΔS)≈29 J/mol/K` → `0.30 mV/℃` 분리(`∂/∂T(U−U)=Δ(ΔS)/F`), 병합~10℃·45℃ 2peak/25℃ 병합. 재현 **0.271 mV/℃**.
- **honest 핵심**: 물리를 지는 양은 **차 Δ(ΔS)=29** 이지 절대값(+15/−14)이 아님. `tab:staging` 초기값(0/−5, 차=5)은 분해 못 냄 → 분리 서명은 그 초기값을 Δ(ΔS) 축으로 갱신하는 **피팅 대상**(표 미편집).
- **6+ 전이 폐기**: 기존 4전이 = 두-상4 에 1:1 대응, 6+는 XRD 미지원 curve-fitting.

### si_fr.tex — Si-host Frumkin 단일상 (**시드 @1**)
- **확정(우리 진단)**: `w_j^Si/(RT/F)=[1.45,2.74,1.09]≳1` (regsol_si) vs 흑연 두-상 ≪0.12 → ~20–50× 대조 = 단일상.
- **커널 유도**(`eq:sifr-V→dVdtheta→kernel`): `dQ/dV = QF/|RT/(θ(1−θ))−2Ω|`, Ω<2RT. Ω→2RT sharpen/발산·Ω=0 로지스틱 폴백(bit-exact)·Ω<0 broaden. `V(θ)=U°−(RT/F)ln[θ/(1−θ)]−(Ω/F)(1−2θ)`.
- **유일 두-상** = 1차 c-Li₁₅Si₄ (~50–60 mV plateau), 순환 a-Si 부재.
- **블렌드 가산중첩**(`eq:sifr-blend`, 공통-μ): Tu 2024 "clearly a superposition". 평형 유효·유한율속 편차=GS-2.
- **honest 핵심 (Ω_Si 식별성)**: 물리는 **영역**(Ω<2RT 단일상)만 고정, **점값 미식별** → 범위 시드(δ캡 바닥 0.2RT)·피팅 위임. 넓은 종은 Ω 민감도 낮음.

### lco_omega.tex — LCO per-peak Ω + 전자항 토글 (**시드 @3·#7**)
- **per-peak Ω_j^cat 커널**(`eq:lcoomega-kernel`) = `eq:lco-gpp/spinodal` 재사용. sharp/broad = 피팅된 Ω_j^cat 의 2RT 초과 여부. 개선 **+1.25%p** (우리 ablation).
- **#7 정정**(`eq:lcoomega-hash7`): "Ω>2RT ⇔ x½ 질서상 안정" → "**Ω_j^cat = 유효 평균장 쌍상호작용 축약(미시 질서구조 아님)·config 엔트로피 ⊥ Ω(별도 슬롯 `ΔS_j^config`)**". 물리 유지·문구만. 혼동 가드 계승.
- **전자항 토글**(`eq:lcoomega-Tref`·`eq:lcoomega-toggle`): `ΔS_e(≈−45.7 J/mol/K)` T_ref 동결 → 상수 오프셋 `T_ref·ΔS_e`가 `ΔH^eff`로 흡수 → **상온 커브 무영향**(U(298) bit-exact), `∂U/∂T`(가역열)에만 작용(∝T, U-이동∝T²). `include_electronic_entropy` 기본 **False**.
- **확정(우리 진단)**: LCO plain MSMR `R²=0.944 ≈ 흑연 0.940` (전자항 커브 무관).
- **honest 핵심**: O3-LCO 온도 의존은 **다온도 데이터 없이 미검증**(연속 g(E_F,x)=갭 G2 tier 없음). 골 깊이 −45.7 = T_ref 동결 시연값.

## 3. 신규 `\cite` key (본문 임의 bibitem 금지 — master 가 해당 장 bib 에 등재) 
> 기존 key 는 그대로 계승 사용: `dahn1991·ohzuku1993·reynier2003·persson2010(b)`(ch1) / `chevrier_dahn2009·limthongkul2003·obrovac_christensen2004·obrovac_chevrier2014·ogata_nmr2014·verbrugge_lisi2016·tu_blend2024`(ch3) / `reimers1992·vanderven1998·marianetti2004·menetrier1999·motohashi2009·reynier2004·ml2024`(ch2).

**신규 3건** (시드 @1·@2 의 "실재" 서지 — 본문에서 `\cite` 만 사용):

1. **`schmitt2022`** — 탈리튬 stage-2L 흑연 구조 실측. 시드 @2 서지("Schmitt 2022(탈리튬 2L)").
   - **미검증(서지 확정 필요)**: 시드가 "실재"로 지목했으나 권·페이지 미기재. 통합 전 master 가 정확 serial 확정 요망. (후보: J. Schmitt 외, 흑연 탈리튬 stage 구조 논문, 2022 — 저널/권 확인 필요.)

2. **`artrith2018`** — a-Li$_x$Si 제일원리/ML 상도표. **JCP 148, 241711 (2018)** (시드 @1 확정 serial).
   - 후보 정식: N. Artrith, A. Urban, G. Ceder, "Constructing first-principles phase diagrams of amorphous Li$_x$Si using machine-learning-assisted sampling with an evolutionary algorithm," *J. Chem. Phys.* **148**, 241711 (2018). DOI: 10.1063/1.5017661. (저자·DOI 최종 확인 권장.)

3. **`verbrugge2017`** — substitutional 열역학(ω-형식) MSMR. **JES 164, E3243 (2017)** (시드 @1 확정 serial).
   - 후보 정식: M. W. Verbrugge, D. R. Baker, B. J. Koch, X. Xiao, W. Gu, "Thermodynamic Model for Substitutional Materials: Application to Lithiated Graphite, Spinel Manganese Oxide, Silicon, and Their Alloys," *J. Electrochem. Soc.* **164**(11), E3243–E3253 (2017). DOI: 10.1149/2.0341708jes. (저자·DOI 최종 확인 권장.)

## 4. 가정·불확실점 (요약)
- **가정**: 세 소절은 v1.0.24 3챕터가 `common_preamble_v1024.tex` 매크로/박스(srcbox·warnbox 포함)를 공유한다는 전제로 작성(ch1_sec05 가 srcbox 사용 확인). 신규 패키지 0.
- **교차참조**: 삽입 대상 챕터의 기존 라벨(`eq:gpp·eq:spinodal·eq:xieq·eq:eqpeak·eq:Uj·eq:lco-gpp·eq:lco-spinodal·eq:dSegate·eq:U1T2·eq:lco-eqpeak·eq:blend-dqdv·tab:staging·tab:lco-staging·sec:width·sec:broadening-class·sec:lco-hys·sec:lco-electronic·ssec:si-blend-gs2` 등)을 `\eqref`/`\ref` 로 사용 — **통합 시 유효**, 단독 컴파일 시 undefined(정상).
- **불확실점(미검증/tier C 명시분)**: (a) stage-2L 병합 온도(~10℃)·25/45℃ 분해는 다온도 데이터 없이 미검증. (b) Ω_Si 점값 미식별(범위 시드). (c) O3-LCO 전자항 온도 의존 미검증(연속 g(E_F,x) tier 없음). (d) config ΔS 수치 0.47/1.49 tier C(원전 재확인 중). (e) `schmitt2022` 서지 serial 미확정.
- **추가 후보(실제 수정 안 함 — 보고만)**:
  - `fig:UjT`(ch1_sec03) 및 `tab:staging` 의 가운데 분리쌍 ΔS 초기값(0/−5, Δ=5)과 stage-2L T-split 서명(Δ=29)의 정합 — 표 수치 갱신이 아니라 Δ(ΔS) 축 피팅 self-test 로 흡수 권고. **master 결정 경계**: 표 초기값을 그대로 두되 stage-2L 절이 Δ(ΔS)=29 를 피팅 목표로 명시할지, 표 각주로 상호참조를 달지.
  - LCO feature 미시 stacking 명명(O2/O3 vs H1/H2)이 원자료(시드 @2 H1/H2 vs brief O2/O3)에서 불일치 → 소절은 미시 라벨을 특정하지 않고 상성격(MIT 두-상 / order–disorder)만 서술(honest scoping). 명명 확정은 master.
