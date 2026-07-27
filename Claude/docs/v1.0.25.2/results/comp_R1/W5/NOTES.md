# W5 저작 노트 — v1.0.24 R1 (gr_2L · si_fr · lco_omega)

> 저작 sub **W5** (물리 기작·직관 강조). 초안만 작성 — 실제 문건 파일·bib·git 미편집.
> 산출: `gr_2L.tex` · `si_fr.tex` · `lco_omega.tex` (본 폴더). 아래는 저작 근거·가정·불확실점·master 결정 필요 항목.

---

## 0. 역할·경계 준수
- 3개 신규 **소절 초안**만 작성. `ch*_v1.0.24.tex`·`_sections/*.tex`·bib·git 미편집.
- 시드표(`REFLECT_SEED_TABLE.md`) 물리·값 **임의 변경 0**. 무근거 수치 0(모든 수치에 tier/출처 병기).
- 기존 기호·라벨·식 **계승**, 신규 라벨만 새 이름(중복 검사 완료 — 아래 §5).
- 형제 W 폴더(W1/2/3/6/7/8/9) **미열람**(독립 저작 무결성 보존).

## 1. 읽은 파일 (저작 전 정독)
| 파일 | 용도(핵심 계승) |
|---|---|
| `results/comp_R1/AUTHOR_BRIEF.md` | 임무·사양·출력 규율 |
| `results/REFLECT_SEED_TABLE.md` | 확정 물리·값·서지(최우선). @3 Si·@5 흑연·LCO 토글·#7 |
| `_sections/ch1_sec05_width.tex` | 폭 `w_j=n_jRT/F`(eq:wbase)·이중지위(sec:width-w)·logistic(eq:xieq,eq:logisticsolve)·eq:mu·평형종 |
| `_sections/ch1_sec06_eqpeak.tex` | 평형 peak eq:eqpeak·종 항등식 eq:belliden·전하보존 미분 |
| `_sections/ch1_sec07_broadening.tex` | 두-상/고용체 분류(sec:broadening-class)·Ω>2RT near-delta·폭 지위·Frumkin(leviaurbach1999) |
| `_sections/ch1_sec10_sum.tex` | 흑연 staging 표 `tab:staging`(4전이 U·ΔH·ΔS·Q·Ω 초기값)·합산 eq:sum |
| `_sections/ch1_sec12_lcocenter.tex` | LCO 중심 eq:lco-dUdT(∂U/∂T=ΔS/F)·Kirchhoff·swiderska2019 |
| `_sections/ch1_sec13_lcohys.tex` | 정칙용액 Ω(eq:lco-gxi/gpp/spinodal/Veq/dUhys)·#7 소재지(eq:br-vanderven1998-1)·Ω/config 가드 |
| `_sections/ch1_sec15_lcoelec.tex` | 전자항 ΔS_e(eq:Se,dSe,dSegate)·MIT 게이트 ggate·T² 곡률 eq:U1T2·slot 분리 eq:lco-mit |
| `_sections/ch1_sec16_lcopeak.tex` | LCO 평형 peak eq:lco-eqpeak/belliden/peakobs·T1 온도신호 |
| `_sections/ch1_sec11_lcointro.tex` | `tab:lco-staging`(T1/T2/T3)·양극 부호·σ_d 규약(eq:lco-sigmaslot) |
| `_sections/ch3v22_sec02_cases.tex` | 원소Si/SiOx/SiC 개형·`tab:si-cases`·a-Si 1차vs순환·Li15Si4·엔트로피 계수 |
| `_sections/ch3v22_sec03_blend.tex` | 공통-μ 반전 eq:blend-balance/dqdv·f_Si·가산중첩·GS-2 |
| `_sections/ch3v22_notation.tex` · `ch2v22_notation.tex` | 계승 2단 규약·host 첨자 |
| `_sections/common_preamble_v1024.tex` · `ch1_preamble.tex` | box 환경·매크로(v1.0.24 = common_preamble 사용, srcbox/warnbox/codebox 등 전부 가용) |
| `_sections/ch1v22_bib.tex`·`ch2v22_bib.tex`·`ch3v22_bib.tex` | 기존 cite 키 확인(신규/중복 필요 판별) |

## 2. 소절별 물리 근거·boxed 식
### gr_2L.tex (Chapter 1 흑연, sec:width 뒤) — `\label{sec:gr-2L}`
- **XRD 5-feature**(eq:gr-xrdseq): dilute 1′↔4·**4↔3 고용체 shoulder**·3↔2L·2L↔2·2↔1 = 두-상 4 + 고용체 1. 근거 `dahn1991`(계승 키).
- **두-상 판정**(boxed eq:gr-criterion): μ(θ) eq:gr-mu(=eq:mu의 θ형)→ dμ/dθ|½=4RT−2Ω eq:gr-dmudtheta(=eq:gpp 곡률). Ω>2RT⇒miscibility gap(near-delta), Ω<2RT⇒고용체. 단상 유효폭 w_eff=(RT/F)(1−Ω/2RT) → sec:width-w 이중지위 정합.
- **stage-2L 엔트로피 안정화**(W5 핵심): 2L=면내 액체-유사(무질서) 고엔트로피 상 → G=H−TS 가 고온에서만 공통접선 아래. 분리쌍 ΔS +15/−14, 차 Δ(ΔS)≈29 (boxed eq:gr-dds). ∂U/∂T=ΔS/F → **분리 0.30 mV/℃·병합~10℃**(boxed eq:gr-split), 45℃ 2peak/25℃ 병합. 재현 0.271 mV/℃.
- 실측 다리(srcbox): `schmitt2022`(operando XRD: 43℃ 2L 뚜렷·0℃ 2L 없음 — Tmerge 확증)·`dahn1991`·`reynier2003`(ΔS 부호·스케일 anchor).
- 경계: 4 슬롯 = 두-상 4, 6전이+ = XRD 미지원 curve-fitting 폐기.

### si_fr.tex (Chapter 3 Si, sec:si-cases 인접) — `\label{ssec:si-frumkin}`
- **a-Si 단일상 기작**(W5 핵심): 무질서 host = 자리 에너지 연속 분포 + 초격자 부재 → 협동 상전이 없음 + Ω<2RT(screened) → 단일상 고용체·매끄러운 U(x). 근거 `chevrier_dahn2009`·`artrith2018`(비정질 LixSi 상도표).
- **폭 진단**: 폭/(RT/F)=[1.45,2.74,1.09]≳1 vs 흑연 두-상 ≪0.12 (~20–50×). 유일 두-상 = `obrovac_christensen2004`,`limthongkul2003` c-Li15Si4(1차 ~50–60mV, 순환 부재 `wang_asi2013`,`mcdowell_coreshell2013`).
- **Frumkin 커널**(boxed eq:si-fr-kernel): V(θ) eq:si-fr-V(=eq:lco-Veq 여집합형)→dV/dθ eq:si-fr-dVdtheta→ dQ/dV=QF/|RT/(θ(1−θ))−2Ω|, Ω<2RT. 3극한(sharpen Ω→2RT / 폴백 Ω→0 bit-exact / broaden Ω<0)·폭 이중지위 단상 첫째 지위(verifybox).
- 소수 broad gallery 이산화 → eq:blend-dqdv Si몫 커널 교체(regsol 분기, 폴백 bit-exact, **재정의 없음**). 가산중첩 `tu_blend2024`("clearly a superposition")·`naboka_sic2021`. ω 형식 `msmr_origin2017`·speciation `verbrugge_lisi2016`·Frumkin `leviaurbach1999`.

### lco_omega.tex (Chapter 2 LCO, sec:lco-hys/electronic/peak 정합) — `\label{sec:lco-omega}`
- **per-peak Ω**(boxed eq:lco-omega-kernel = 단상 반충전 순높이 Q/(4w)·1/|1−Ω/2RT|): T1(MIT ~3.90V) 두-상 sharp(Ω₁>2RT)·T2/T3(x≈½ order–disorder) 유효인력. 합산은 eq:lco-eqpeak 그대로. 흑연(eq:gr-criterion)·Si(eq:si-fr-kernel)와 같은 |1−Ω/2RT| 인자. ablation +1.25%p(per-peak Ω)/+1.90%p(H1-3 세분).
- **#7 정정**(boxed eq:lco-omega-hash7 + warnbox): Ω_j^cat = 진행좌표 ξ_j 의 **유효 평균장 쌍상호작용 축약(미시 질서구조 아님)**·config 엔트로피 ΔS_j^config 는 **별도 슬롯**. `vanderven1998`·`ml2024` 소관. 물리 유지·문구만. sec:lco-hys-od 가드 계승.
- **전자항 토글**(W5 핵심; boxed eq:lco-omega-toggle + codebox): ΔS_e(~−45.7 J/mol/K, ∝T)는 T_ref 동결로 **상온 커브 무영향**(U(T_ref)이 ΔH 흡수; eq:lco-omega-U1T=eq:U1T2). **∂U/∂T|_e=ΔS_e/F∝T** 가 유일 지문(config/vib 는 상수). 코드 `include_electronic_entropy=False` 기본 OFF(커브)·ON(∂U/∂T). 실측: plain MSMR R²=0.944≈흑연 0.940.

## 3. 신규 bib 키 (본문 `\cite` 사용 — master 가 bib 등재; 임의 bibitem 미작성)
1. **`schmitt2022`** (gr_2L): J. Schmitt et al., "Understanding the Influence of Temperature on Phase Evolution during Lithium-Graphite (De-)Intercalation Processes: An Operando X-ray Diffraction Study," *ChemElectroChem* (2022). **DOI: 10.1002/celc.202101342**.
   - 근거 확인(WebSearch): 43℃ 탈리튬 2L 뚜렷·0℃ 2L 없음 — 시드 "Schmitt 2022(탈리튬 2L)" 정확 대응.
   - ⚠ 저자 전체 리스트·권/호/페이지는 Crossref 최종 대조 필요("et al." 표기).
2. **`artrith2018`** (si_fr): N. Artrith, A. Urban, G. Ceder, "Constructing first-principles phase diagrams of amorphous Li$_x$Si using machine-learning-assisted sampling with an evolutionary algorithm," *J. Chem. Phys.* **148**(24), 241711 (2018). **DOI: 10.1063/1.5017661** (arXiv:1802.03548).
   - 근거 확인(WebSearch): 비정질 LixSi 상도표 = "a-Si 단일상 고용체" 직접 지지. 시드 "Artrith 2018(JCP148,241711)" 정확 대응. ⚠ DOI Crossref 최종 대조 권장.

## 4. 장간 bib 중복 등재 필요 (D22 "공통 키 타 장 중복 수록은 의도")
- **`msmr_origin2017`** (Verbrugge 2017, JES 164, E3243 — 시드 @3 "ω 형식"): **ch2v22_bib 에 존재**, si_fr(Ch3)에서 인용 → **ch3v22_bib 에 중복 등재 필요**.
- **`leviaurbach1999`** (Frumkin isotherm): **ch1v22_bib 에 존재**, si_fr(Ch3)에서 인용 → **ch3v22_bib 에 중복 등재 필요**.
- (LCO-Ω 은 신규/중복 키 없음 — reimers1992·vanderven1998·marianetti2004·menetrier1999·motohashi2009·reynier2004·ml2024 전부 ch2v22_bib 존재.)

## 5. 신규 라벨 (중복 검사 완료 — 기존과 충돌 0)
- 소절: `sec:gr-2L`(Ch1 관행 sec:) · `ssec:si-frumkin`(Ch3 관행 ssec:) · `sec:lco-omega`(Ch2 관행 sec:).
- 식: gr-{xrdseq,mu,dmudtheta,criterion,dds,split} · si-fr-{V,dVdtheta,kernel} · lco-omega-{kernel,hash7,U1T,toggle}.
- ⚠ **라벨 prefix 선택**: 브리프 출력 예시는 `\label{ssec:...}`로 통일 표기했으나, 필독 규칙 "신규 라벨은 **장 관행** 따라"에 우선순위를 두어 장별 관행(Ch1/Ch2=sec:, Ch3=ssec:)을 따랐다. master 가 통일 원하면 일괄 치환 가능.

## 6. master 결정 필요 (정직 공백·긴장)
1. **gr_2L 분리쌍 ΔS vs tab:staging**: 시드 분리쌍 +15/−14(차 29)는 `tab:staging` 초기값(3→2L: 0.0, 2L→2: −5.0, 차 5)과 **다르다**. 견고량 = 차 Δ(ΔS)≈29(T_SPLIT_FINDING 재현 0.271 mV/℃). 본문은 tab:staging **미편집**, 분리쌍을 "대표값·차가 견고량·round-trip 피팅 정합"으로 제시. → master: tab:staging ΔS 열 갱신 or 각주 정합 여부 결정.
2. **gr_2L 최고전위 슬롯 재식별**: 시드는 tab:staging 최고전위 행(현 "4→3", 0.21V, ΔS+29)을 XRD 상 **"dilute 1′↔4"**로 재식별(4↔3 은 별도 고용체 shoulder). 본문은 이를 **해석 층위**로 제시(값 미변경). → master: tab:staging 라벨 재배정 채택 여부(**추가 후보**, 본 초안은 미편집).
3. **#7 원소재지 편집**: 정정 문구는 lco_omega(eq:lco-omega-hash7+warnbox)에 반영했으나, 원 문장 `ch1_sec13_lcohys.tex` eq:br-vanderven1998-1 근처(≈L154 "Ω_j^cat>2RT ⇔ x≈½ 질서상 안정")는 **미편집**. → master: 원소재지 문구를 "⇔" → "상분리 가지 진입(질서상 안정성은 제일원리 소관)"로 완화.
4. **LCO feature 명명(O2/O3 vs T1/T2/T3)**: 시드 @3 "3.70V(O2)/3.90V(O3) 두-상 sharp"를 기존 T1(MIT 3.90)/T2/T3 틀에 매핑(P5 라벨 보존). "3.70V" 하드값 미도입. → master: O2/O3 feature set 이 T1/T2/T3 와 별개 의도면 tab:lco-staging 확장 필요.
5. **`tu_blend2024` 아티클 번호**: 시드 "Tu-Dao-Verbrugge-Koch JES171,**050520**(2024)"; 기존 ch3v22_bib `tu_blend2024`=JES171,**050539**. 동반 논문/오타 가능 — 본문은 기존 키 인용. → master: "clearly a superposition" 인용 원문이 050520(별개 논문)이면 신규 키 필요.
6. **내부 수치 검증값(bibitem 없음)**: regsol2 Ω/RT=[4.06,2.02,3.55,4.07]·regsol_si 폭[1.45,2.74,1.09]·ablation +1.25/1.90%p·R²=0.944/0.940 = REFLECT_SEED_TABLE 근거 산출물(regsol2.png·regsol_si·ablation_result.json·lco_ablation_result.json). 본문 "내부 수치 검증, tier B"로 표기(임의 bibitem 미작성). → master: `numverif2026` 류 내부자료 키로 형식화 여부.

## 7. 장간(소절간) 상호참조 — 통일 웹 (master 통합 시 확인)
W5 세 소절은 "같은 정규용액 커널의 서로 다른 Ω 점"을 명시하려 서로 참조한다(장간 xr-hyper \externaldocument 로 해소 — 기존 ch3→ch1 참조와 동일 패턴):
- si_fr → `eq:gr-dmudtheta`·`eq:gr-criterion`·`sec:gr-2L` (Ch1)
- lco_omega → `sec:gr-2L`(Ch1)·`ssec:si-frumkin`·`eq:si-fr-kernel`(Ch3)·`eq:gr-criterion`(Ch1)
→ 세 소절 통합 시 라벨 유지되면 자동 해소. gr_2L 만 단독 통합/타 라벨이면 위 참조 재지정 필요.

## 8. 가정 (명시)
- 2L = 면내 액체-유사(무질서) stage-2(표준 흑연 staging 명명). "엔트로피 안정화" 서술은 Schmitt2022 온도 의존과 정합하는 물리 프레임(미시 면내구조는 forward 축약).
- a-Si Ω 부호: 단상측 Ω<2RT 제시. 폭>RT/F 는 n>1 및/또는 Ω<0 로 귀속(시드 "범위 시드·피팅 위임"). 시드 "δ캡 바닥 0.2RT"는 하드코딩 안 함(피팅 위임).
- 전자항 토글: 현 코드 ΔS_e 상시 ON 전제 → OFF 전환은 U(298) 보존 위한 ΔH 재기준 필요(시드 4행 "R2 게이트"). codebox 에 명시.
- 물리 골격 불변: 전하보존 중심식(eq:sum/eqpeak/blend-balance)·V_n 구분·MSMR 동형 전부 유지, 신규는 additive.

## 9. 남은 불확실점 (honest)
- schmitt2022 저자 전체·권/호/페이지 미확정(DOI 만 확정). artrith2018 DOI 표기값 Crossref 미대조.
- 분리쌍 개별 +15/−14 는 tier C(차 29 가 tier B 견고량). LCO ablation %p·R² 는 내부 산출(tier B, 1차문헌 아님).
- LCO "3.70V(O2)" feature 는 본문 미반영(기존 T1/T2/T3 정합 우선) — 시드 의도가 별 feature 면 후속.
- 시드표 이외 원천 데이터(json/png) 원본 미열람(시드표 요약값만 사용) — 값 재검증은 master/검수 소관.
