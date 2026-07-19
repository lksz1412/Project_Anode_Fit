# W6 저작 NOTES — [GR-2L]·[SI-FR]·[LCO-Ω] 초안 근거·가정·불확실점

> 저작 sub W6. **초안만** — 실제 문건 파일 편집·git·commit 없음. commit 권한 master.
> W6 강조 = **교차물질 통일**: @3(정칙용액 커널, per-peak Ω)와 Ω>2RT/Ω<2RT 판정자를
> 흑연(두-상)·Si(고용체)·LCO(혼합)를 관통하는 **하나의 틀**로 제시. 세 소절이 공통 판정자
> `eq:gr-classifier`(gr_2L.tex 에 정의) 하나를 가리킨다.

---

## 0. 산출물 (이 폴더에만)
- `gr_2L.tex` — 흑연 stage-2L·XRD 5-feature staging (ch1 §5 뒤 신규 subsection).
- `si_fr.tex` — Si-host Frumkin(Ω<2RT 고용체) 커널 (ch3 §3.2 인접 신규 subsection).
- `lco_omega.tex` — LCO per-peak Ω + 전자항 on/off 토글 (ch2 LCO 신규 subsection).
- `NOTES.md` — 본 파일.

## 1. 읽은 파일 (저작 근거)
- **최우선**: `results/REFLECT_SEED_TABLE.md` (@3·@5·LCO토글·#1·#7 확정 물리·값).
- 흑연: `_sections/ch1_sec05_width.tex`(폭 이중지위·eq:wbase·eq:xieq·eq:belliden), `ch1_sec06_eqpeak.tex`(eq:eqpeak),
  `ch1_sec04_hys.tex`(eq:gpp·eq:spinodal·eq:Veq·eq:hyssub·eq:dUhys·eq:Ubranch·eq:center), `ch1_sec03_center.tex`(eq:Uj·∂U/∂T=ΔS/F),
  `ch1_sec07_broadening.tex`(sec:broadening-class·두-상/고용체 분류·eq:widthbudget), `ch1_sec01_n0n1.tex`(fig:staging·V_n·기호표), `ch1_sec10_sum.tex`(tab:staging·eq:sum).
- Si: `_sections/ch3v22_sec02_cases.tex`(계열 개형·tier), `ch3v22_sec03_blend.tex`(eq:blend-dqdv·eq:blend-balance·GS-2), `ch3v22_notation.tex`(host 첨자·f_Si 계승규약).
- LCO: `_sections/ch1_sec13_lcohys.tex`(eq:lco-gxi·eq:lco-gpp·eq:lco-spinodal·eq:lco-dUhys·eq:lco-mit·혼동가드), `ch1_sec15_lcoelec.tex`(eq:dSe·eq:dSegate·eq:U1T2·−45.7), `ch1_sec16_lcopeak.tex`(eq:lco-eqpeak·eq:lco-peakobs), `ch1_sec11_lcointro.tex`(tab:lco-staging·eq:lco-sigmaslot·T1/T2/T3).
- preamble: `common_preamble_v1024.tex`·`ch1_preamble.tex`(박스 환경·매크로 — 신규 패키지 X 확인).
- bib(키 존재 확인): `ch1v22_bib.tex`·`ch2v22_bib.tex`·`ch3v22_bib.tex`.
- 서지 원천(신규 키 서지 확정용): `results/comp_v24/GRAPHITE_STAGING_XRD.md`·`T_SPLIT_FINDING.md`·`lit_raw/01_graphite.md`·`lit_raw/03_graphite_si.md`.

## 2. 계승(재정의 0) 확인
- 기호: V_n·ξ_j·w_j·Ω_j(^cat)·U_j(^cat)·ΔS_rxn(^cat)·Q_j(^cat)·C_bg·σ_d·host 첨자·f_Si·θ_j=1−ξ_j — **값·의미 불변**.
- 식 참조(재정의 X): eq:gxi·eq:mu·eq:gpp·eq:spinodal·eq:Veq·eq:dUhys·eq:Ubranch·eq:eqpeak·eq:xieq·eq:wbase·eq:sum·eq:Uj·eq:blend-dqdv·eq:blend-balance·eq:lco-gxi·eq:lco-gpp·eq:lco-spinodal·eq:lco-dUhys·eq:lco-eqpeak·eq:dSe·eq:dSegate·eq:U1T2·eq:lco-mit (전부 실재 라벨, grep 확인).
- 매크로: `\dd \eq \eff \rxn \cat \bg \cell \hys \code{} `·박스 `keybox verifybox codebox` 만 사용(신규 패키지·매크로 0).
  `config`는 기존 LCO 절 관행대로 `\mathrm{config}` 리터럴로 표기(공통 preamble 전용 `\config` 매크로 미사용 — ch1_preamble 미정의 대비).

## 3. 신규 라벨(중복 금지 — grep 대조 완료, 충돌 0)
- subsection: `ssec:gr-2L`·`ssec:si-frumkin`·`ssec:lco-omega` (+ subsubsection 하위 라벨 `ssec:gr-2L-*` 등).
- 식: `eq:gr-regsol-mu`·`eq:gr-dmudxi`·**`eq:gr-classifier`(공통 판정자, 정의처)**·`eq:gr-2L-dSsplit`·`eq:gr-2L-slope`
  ·`eq:si-fr-V`·**`eq:si-fr-peak`**·`eq:lco-omega-class`·`eq:lco-omega-slot`·`eq:lco-elec-toggle`.
- 표: `tab:gr-2L-xrd`·`tab:si-frumkin-contrast`.

## 4. ★교차 파일 의존성 (master 조립 시 주의)
- `si_fr.tex`·`lco_omega.tex` 가 **`\eqref{eq:gr-classifier}`(gr_2L.tex 정의)** 를 참조 → 세 파일이 한 문서로 조립되고
  ch2/ch3 가 ch1 을 `\externaldocument`(xr-hyper) 로 잇는 현행 구조(기존 eq:blend-dqdv↔ch1 참조와 동일 메커니즘)에서 해결됨.
- 물리 안전장치: 세 파일 각각 판정자 분모 `|RT/[ξ(1−ξ)]−2Ω|` 를 자체 재진술 → 크로스레프 미해결이어도 자기완결 유지.
- gr_2L 는 §5(sec:width) 뒤·§7(sec:broadening) 앞 삽입 전제. si_fr 는 §3.2 인접. lco_omega 는 ch2 LCO(sec:lco-peak 인접).

## 5. 신규 cite 키 — **서지 명기(본문 bibitem 금지, master 가 bib 에 등재)**
> 4-tier 병기. 아래 3키만 신규. 나머지는 기존 키 재사용(§6).
1. **`artrith2018`** (si_fr) — N. Artrith, A. Urban, G. Ceder, "Constructing first-principles phase diagrams of amorphous Li$_x$Si using machine-learning-assisted sampling with an evolutionary algorithm," *J. Chem. Phys.* **148**(24), 241711 (2018). DOI: 10.1063/1.5017661. [a-Li$_x$Si 매끈 고용체(형성E 연속) 근거. **tier A**. 출처 `lit_raw/03_graphite_si.md` A8.]
2. **`verbrugge2017`** (gr_2L·si_fr·lco_omega — 정칙용액 ω 형식의 교차물질 진입점) — M. W. Verbrugge, D. R. Baker, B. J. Koch, X. Xiao, W. Gu, "Thermodynamic Model for Substitutional Materials," *J. Electrochem. Soc.* **164**(11), E3243 (2017). DOI: 10.1149/2.0341708jes. [MSMR 정칙용액 ω 상호작용 형식 자체 = per-peak Ω 커널의 형식 원천. **tier A**. 출처 `lit_raw/03_graphite_si.md` (2차/보조).]
3. **`schmitt2022`** (gr_2L — stage-2L 탈리튬 재확인) — J. Schmitt 등, "Understanding the Influence of Temperature on Phase Evolution during Cycling …(operando XRD/dV/dQ)," *ChemElectroChem* **9** (2022). DOI: 10.1002/celc.202101342. [탈리튬화(방전 음극) 2L 분리 재확인. **★tier C — 정직 경고**: 원문 전문 유료(HTTP402) 미fetch, 정량 findings 미검증(`lit_raw/01_graphite.md` D절 명시). 본 소절에서 **보강 lead** 로만 인용(1차 XRD anchor 는 dahn1991, tier A). master 는 서지 정밀도(권/쪽/저자 전체)·DOI 를 Crossref 로 최종 확정 요망.]

## 5b. ★bib 등재 지침 (master — 장별 자기완결 bib, 공통키 타장 중복 = D22 의도)
> 각 소절이 부착되는 장의 bib 에 해당 키가 있어야 `\cite` 해결. 아래는 master 가 처리할 등재/중복 목록.
- **`verbrugge2017`(신규)** → **ch1v22_bib · ch2v22_bib · ch3v22_bib 세 곳 모두** (gr_2L·lco_omega·si_fr 에서 각각 인용 — D22 중복).
- **`artrith2018`(신규)** → ch3v22_bib (si_fr).
- **`schmitt2022`(신규, tier C)** → ch1v22_bib (gr_2L).
- **`leviaurbach1999`(기존 ch1v22 전용)** → **ch3v22_bib 로 중복 등재 필요** (si_fr 가 Frumkin 커널 원전으로 인용 — 현재 ch3 bib 미수록, D22 중복 대상).
- 그 외 재사용 키는 부착 장 bib 에 이미 존재(§6): gr_2L→dahn1991·ohzuku1993·leviaurbach1999·msmr_partII(ch1); si_fr→chevrier_dahn2009·obrovac_christensen2004·tu_blend2024(ch3); lco_omega→reimers1992·vanderven1998·motohashi2009·menetrier1999·marianetti2004·reynier2004·msmr_origin2017(ch2). 추가 중복 불요.

## 6. 재사용한 기존 키 (정체 확인 완료)
- `dahn1991` = Dahn, *PRB* **44**, 9170 (1991) "Phase diagram of Li$_x$C$_6$" (ch1v22_bib) — GR-2L XRD 정본.
- `reynier2003` = Reynier·Yazami·Fultz, *JPS* **119–121**, 850 (2003) (ch1v22_bib) — 시드의 "Reynier JPS119-121,850(2003)" 와 정확 일치, GR-2L T-split anchor.
- `ohzuku1993`(ch1v22) — GR-2L 교차확인. `leviaurbach1999`(ch1v22) = Frumkin 삽입 등온선 리뷰 — SI-FR 커널 원전.
- `chevrier_dahn2009`(ch3v22, JES156 A454)·`limthongkul2003`·`obrovac_christensen2004`(c-Li15Si4)·`naboka_sic2021`(ch3v22) — SI-FR.
- `tu_blend2024`(ch3v22) — SI-FR 블렌드 "clearly a superposition". **주의**: `lit_raw/03` 은 이 논문을 *JES* 171(5) **050520** 로, ch3v22_bib 는 **050539** 로 적음(동일 DOI 10.1149/1945-7111/ad4823). 동일 DOI → 동일 논문이나 아티클번호 표기 불일치 존재 → master 확인 권장(내 인용은 기존 키 `tu_blend2024` 그대로).
- `reimers1992`·`vanderven1998`·`motohashi2009`·`menetrier1999`·`marianetti2004`·`reynier2004`·`msmr_origin2017`(ch2v22_bib) — LCO-Ω.

## 7. 값의 tier·출처 (무근거 수치 0)
- **@5 흑연**: 5-feature staging·성격·ΔS 시드(+29/0/+15/−14/−16)·전위대 = 시드표 §2 그대로(Dahn1991 tier B~C). regsol2 Ω/RT=[4.06,2.02,3.55,4.07] = 시드표 §2 "★Ω>2RT 실측 검증"(본 문서 정칙용액 진단, 피팅 override 전제).
- **stage-2L T-split**: Δ(ΔS)≈29 J/mol/K → 0.30 mV/℃·T_2L~10℃·재현 0.271 mV/℃ = 시드표 §2 + `T_SPLIT_FINDING.md`. **tier C 명시**(Δ(ΔS)=29 는 Dahn 분리기울기 역산, 직접 열량계 값 아님 — 본문에 명기).
- **@3 Si**: 폭비 w_j/(RT/F)=[1.45,2.74,1.09] = 시드표 §1 `regsol_si.png` 진단(본 문서 커널 fit, 피팅 위임). "흑연 두-상 ≪0.12 대조·~20-50×" = 시드표 §1 표현을 "near-delta·자릿수급 대조"로 서술(정확 수치 대신 가지 대조로 완화 — 아래 8-③).
- **LCO per-peak Ω**: +1.25%p = 시드표 §1 `lco_ablation_result.json`(정칙용액 per-peak Ω ablation). ΔS_e≈−45.7 J/mol/K = 시드표 §3 + `ch1_sec15_lcoelec.tex` sec:lco-Se-scale 검산값(tier: 함수형 A·anchor A·연속곡선 없음 G2).
- **LCO R²=0.944≈흑연 0.940**: **출처 = AUTHOR_BRIEF §3 [LCO-Ω]** (시드표엔 미기재). tier B(보고된 피팅 품질)로 인용 → master 는 ablation JSON 으로 대조 확인 요망(8-④).

## 8. ★불확실점·정직 갭 (master 판단 요청)
1. **[가장 중요] 흑연 5-feature 분류 vs sec:broadening-class 텍스트 충돌.** 시드표 §2(=Dahn XRD)는 **3↔2L 을 두-상**(Ω>2RT)으로 분류.
   그러나 기존 `ch1_sec07_broadening.tex`(sec:broadening-class)는 "dilute→stage4·4L→3L·**3L→2L** 두 전이 = 연속 고용체", 두-상은 {2L→2, 2→1} 둘만으로 서술.
   → **3↔2L 가지 지목이 직접 상충**. 내 gr_2L 은 시드(XRD/regsol2 Ω/RT=2.02>2)를 따르되, 표~tab:gr-2L-xrd 각주·본문에서 "기존 4-전이 coarse-graining·경계 서술은 sec:broadening-class 소관"으로 정합 프레임하고 라벨은 불변 유지. **P3-6 게이트: master 가 두 절의 두-상/고용체 경계 서술을 최종 정합**(sec:broadening-class 문구 조정 or tab:gr-2L-xrd 각주 강화 중 택1).
2. **LCO feature anchor: 브리프 "3.70V(O2)/3.90V(O3)" vs 문건 T1(3.90 MIT)/T2(4.05)/T3(4.17-4.20).** 브리프 [LCO-Ω] 스펙과 기존 tab:lco-staging 이
   전이 집합·전위가 다름. 내 lco_omega 는 **정합 요구(ch1_sec13·15·16)에 맞춰 문건 T1/T2/T3 를 주 골격**으로 쓰고, "O2/O3 stacking 두-상"을 T1 과 같은 두-상 부류로 \emph{병기}(브리프 반영). → master 는 3.70/3.90 O2/O3 를 별 feature 로 추가할지, T1 로 흡수할지 결정 요망(내 초안은 per-peak Ω 판정자 구조가 어느 쪽이든 불변이도록 서술).
3. **Si "≪0.12" 수치.** 시드표 §1 "흑연 두-상 ≪0.12" 의 정의(어느 폭 규격)가 모호(w_eff/(RT/F) 로 읽으면 Ω>2RT 서 음수/near-delta). 허위정밀 회피 위해
   본문은 "near-delta·자릿수급 대조(~20-50×)"로 서술하고 정확 "0.12"는 표에 싣지 않음. master 가 원 정의 확인 시 수치 복원 가능.
4. **R²=0.944/0.940 출처.** AUTHOR_BRIEF 만의 값(시드표 부재). 본문 tier B 인용 → `ablation_result.json`/`lco_ablation_result.json` 로 재확인 요망.
5. **#7 정정 대상 지점.** 기존 `ch1_sec13_lcohys.tex` 의 식~eq:br-vanderven1998-1 "$\Omega_j^\cat>2RT\Leftrightarrow x{\approx}\tfrac12$ 질서상 안정" 이 정정 대상.
   내 lco_omega §ssec:lco-omega-guard 가 **정정된 프레이밍**(Ω=유효 평균장 축약≠미시 질서·config 별도 슬롯, eq:lco-omega-slot)을 신규 소절로 저작. **기존 sec13 문구 자체는 미편집**(master 가 문구만 정정 적용 — 물리 유지). 기존 sec13 에 이미 "★Ω 와 config ΔS 구분(혼동 가드)" 문단 존재 → 내 소절과 정합(중복 아닌 강화).
6. **schmitt2022 미검증**(§5-3): 전문 유료·findings 미검증 → 보강 lead 로만. 삭제/대체는 master 재량(1차 anchor dahn1991 로 GR-2L 물리는 자립).
7. **tu_blend2024 아티클번호 표기 불일치**(§6): 050520 vs 050539(동일 DOI). master 최종 확정.

## 9. P3 본프로젝트 검수 7항목 자기점검
1. V_n 구분 유지(gr_2L 판정자·si_fr 커널이 V_n/V 평가 — 계승 규약). ✅
2. 전하보존 중심식 유지: eq:eqpeak·eq:lco-eqpeak·eq:blend-dqdv 가 전하보존 미분 기원(OCV 읽기 회귀 X). ✅
3~4. 순환 의존: per-peak Ω 는 **피팅 파라미터**(자기정합 루프 아님)로 명시 — Ω_j 가 gap·폭·중심을 정하되 "피팅 override" 전제 반복 명기(4분류 = 정의상 implicit 아님, 피팅 위임). ✅
5. ref 6,7 = 완료(시드표 §6, 재작업 불요) — 본 소절 무관.
6. Chapter 1 기준식 vs 전달식 충돌 = **8-①에 명시 flag**(3↔2L 가지). master 정합. ⚠️
7. ver.N(역사명) vs Chapter/전이 라벨 혼동 방지: gr_2L "역사적 명칭 가드" 문단·tab:staging 불변 명기. ✅

## 10. 분량·register
- 각 소절 (a)출발→(b)연산→(c)중간식→(d)박스 전개·boxed 최종식 ≥1·식마다 라벨·한글 교과서 register·복붙/skim 없음.
- 표 2개(tab:gr-2L-xrd·tab:si-frumkin-contrast) 신규, TikZ 그림은 미포함(브리프 요구 = boxed 식·라벨·cite, 그림 비필수 — 필요 시 후속).
