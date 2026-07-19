# W7 저작 NOTES — v1.0.24 R1 (산업 방어력 emphasis)

> 작업-sub W7. **초안만** 저작(실제 `_sections/*.tex` 편집·git·commit 없음). 결과는 본 폴더에만.
> 산출물: `gr_2L.tex`(GR-2L) · `si_fr.tex`(SI-FR) · `lco_omega.tex`(LCO-Ω) · 본 NOTES.
> W7 강조축: **회사 리뷰어가 신뢰할 피팅 파라미터** — 물리적 의미·일관성(Ω=DFT/XRD 정박·U_j 화학불변),
> 믿을 수 있는 feature(sharp 두-상) vs 불확실 feature 분리, 전자항 토글로 회사 다온도 데이터 위임, 한계 정직.

---

## 0. 저작 근거 (읽은 파일·행)

필독(AUTHOR_BRIEF §2) 전부 정독:
- `results/REFLECT_SEED_TABLE.md` — 확정 물리·값·서지(최우선). §1 Si Frumkin·§2 흑연 5-feature·§3 LCO 전자항 토글·§5 #7.
- 흑연: `_sections/ch1_sec05_width.tex`(폭 이중지위 sec:width-w·eq:wbase·eq:xieq), `ch1_sec06_eqpeak.tex`(eq:eqpeak·eq:belliden),
  `ch1_sec03_center.tex`(eq:Uj·∂U/∂T=ΔS_rxn/F·fig:UjT), `ch1_sec04_hys.tex`(eq:mu·eq:gxi·eq:gpp·eq:spinodal),
  `ch1_sec07_broadening.tex`(sec:broadening-class 두-상/고용체 분류·eq:widthbudget FWHM=3.53w), `ch1_sec10_sum.tex`(tab:staging).
- Si: `_sections/ch3v22_sec02_cases.tex`(ssec:si-elemental·tab:si-cases), `ch3v22_sec03_blend.tex`(eq:blend-dqdv·sec:si-blend),
  `ch3v22_notation.tex`(계승 규약).
- LCO: `_sections/ch1_sec11_lcointro.tex`(tab:lco-staging·방향 규약), `ch1_sec12_lcocenter.tex`(eq:lco-dUdT·Kirchhoff),
  `ch1_sec13_lcohys.tex`(eq:lco-gxi·eq:lco-spinodal·eq:lco-dUhys·#7 대상 문구·혼동 가드), `ch1_sec15_lcoelec.tex`(eq:dSe·eq:dSegate·eq:U1T2·전자항),
  `ch1_sec16_lcopeak.tex`(eq:lco-eqpeak).
- 매크로/박스: `common_preamble_v1024.tex`(bgbox·srcbox·verifybox·keybox·warnbox·signbox / \dd·\eq·\rxn·\cat·\config·\bg·\cell·\hys·\kB·\code 등 — **신규 매크로·패키지 0 사용**).

확정 수치의 원천(본 세션 산출 JSON, `Claude/results/comp_v24/`):
- `regsol_si_result.json`: Si 폭 `[37.34, 70.32, 27.97] mV` → `/(RT/F=25.68)=[1.45,2.74,1.09]`(≳1 고용체);
  `si_Omega_over_RT=[0.2,0.2,0.2]`(δ물리캡 바닥); `graphite_Omega_over_RT=[4.06,2.02,3.55,4.07]`(전부>2RT 두-상 확증).
- `ablation_result.json`(블렌드 단일셀 baseline R²=0.9871): @3 Si Frumkin=**+0.67%p**; @5 stage-2L=**−0.44%p**(핵심 정직점).
- `lco_ablation_result.json`: LCO O2 plain=0.9441·@3=0.9565(**+1.25%p**)·@5=0.9630(+1.90%p); `graphite_plain_ref=0.94`.
- `T_SPLIT_FINDING.md`: Δ(ΔS)≈29 J/mol/K → 0.30 mV/℃·병합 ~10℃·25℃ 병합/45℃ 분리·재현 0.271 mV/℃·두-상 폭 w≈1.6 mV.
- `GRAPHITE_STAGING_XRD.md`: Dahn 1991 XRD 5-feature(두-상 4 + 4↔3 고용체 shoulder)·판정자 Ω vs 2RT·6+ 폐기.

**경쟁 저작 무결성**: 형제 폴더 `comp_R1/W1`·`W6`(타 저자-sub 독립 초안)은 **읽지 않음**(9창 경쟁 저작 독립성 보존, CLAUDE.md 정합).

---

## 1. 소절별 저작 요지·근거 매핑

### GR-2L (`gr_2L.tex`, ssec:gr-2L — ch1 흑연, ch1_sec05_width 뒤)
- **XRD 5-feature 표 tab:gr2l-xrd**: Dahn 1991\cite{dahn1991}·Ohzuku\cite{ohzuku1993} — dilute1′↔4·**4↔3 고용체 shoulder**·3↔2L·2L↔2·2↔1.
- **판정자 boxed eq:gr2l-verdict**: μ(θ)=μ°+RT ln[θ/(1−θ)]+Ω(1−2θ)(eq:gr2l-mu, 계승 eq:mu), dμ/dθ|½=4RT−2Ω(eq:gr2l-dmu, 계승 eq:gpp·eq:spinodal). **XRD(고정 d-간격 공존)이 판정자·dQ/dV 폭 아님** 강조(W7 정박). DFT 교차검증 persson2010/2010b.
- **stage-2L 온도 분리 boxed eq:gr2l-tsplit·eq:gr2l-resolve**: 2L=엔트로피 안정화(>~10℃), Δ(ΔS)≈29→∂U/∂T(eq:Uj)로 0.30 mV/℃·병합 T_m≈283K·45℃ 2피크/25℃ 병합(FWHM=3.53w, eq:widthbudget). schmitt2022(탈리튬 특이)·reynier2003(2L만 T-민감).
- **산업 방어 keybox·warnbox**: 5-feature=XRD 상한(6+ 폐기)·2L=새 상 아님(기존 3→2L·2L→2)·**분리는 다온도 신호**(단일 25℃ 등온선 @5 = −0.44%p, 자유도만 늘고 정보 없음)→회사 다온도 매트릭스로 검증.

### SI-FR (`si_fr.tex`, ssec:si-frumkin — ch3 Si, ch3v22_sec02_cases 인접)
- **폭 판정 eq:sifr-widthtest**: w/(RT/F)=[1.45,2.74,1.09]≳1(흑연 두-상 ≪0.12의 20–50배)·chevrier_dahn2009·artrith2018. **회사가 dQ/dV 폭으로 직접 검증** 강조.
- **Frumkin 커널 boxed eq:sifr-kernel**: V(θ)(eq:sifr-V, 계승 eq:Veq)·dV/dθ(eq:sifr-dVdtheta)→dQ/dV=QF/|RT/(θ(1−θ))−2Ω|. 세 극한: Ω=0→흑연 종(eq:eqpeak·eq:belliden) 정확 회수·Ω→2RT⁻ sharpen·Ω<0 broaden. leviaurbach1999(Frumkin 원전)·msmr_origin2017(ω 형식).
- **소수 broad gallery boxed eq:sifr-gallery**: 다수 narrow staging 아님(비물리 상 주입)·유일 두-상=c-Li₁₅Si₄ 1차 심리튬(순환 부재). 블렌드 중첩=eq:blend-dqdv(sec:si-blend)·tu_blend2024 위임.
- **정직 공백 D1 warnbox**: Ω_Si 단일 문헌값 없음→**범위 시드**(δ캡 0.2RT)·피팅 위임. 믿을 것=폭≳RT/F 판정(tier A)·맡길 것=범위 내 Ω_Si값. 개선 +0.67%p.

### LCO-Ω (`lco_omega.tex`, ssec:lco-omega — ch2 LCO, sec:lco-hys/electronic/peak 정합)
- **동형 MSMR (a)**: eq:lco-eqpeak=eq:eqpeak, plain R²=0.944≈흑연 0.940(전자항 무관, 확정).
- **per-peak Ω (b)**: 전이당 독립 Ω_j^cat(eq:lco-gxi·eq:lco-spinodal·eq:lco-dUhys), reimers1992·vanderven1998·motohashi2009, +1.25%p.
- **#7 명확화 boxed eq:lcoom-slotsep**: "Ω>2RT ⇔ x½ 질서상 안정"(sec:lco-hys 느슨 표기, eq:br-vanderven1998-1) → **Ω_j^cat=유효 평균장 문턱(미시 질서구조 아님)·config ΔS는 별도 슬롯(U_j(T) 이동, sec:lco-decomp)**. 물리 유지·표기만 정밀화(각주로 #7 명시). 혼동 가드(sec:lco-hys-od) 계승.
- **전자항 토글 boxed eq:lcoom-toggle**: ΔS_e≈−45.7 J/mol/K(eq:dSegate) T_ref 동결→U_j(T_ref) 보존·상온 dQ/dV 불변; ON=∂U/∂T의 T-선형·U₁∝T² 곡률(eq:U1T2·eq:lco-dUdT). 기본 OFF(plain 0.944 잉여)·회사 다온도로 ON 결정. motohashi2009(g_max=13)·menetrier1999(MIT 0.75–0.94).
- **3-tier 정직 warnbox**: tier A(동형·plain·per-peak·전자 상온무영향) / tier A anchor + G2 곡선 부재(g(E_F,x)) / tier C(config 0.47/1.49·원전 재확인). 골 깊이 −45.7 vs O3 부분몰 0.18 k_B = 척도 다른 양(sec:lco-Se-scale).

---

## 2. 서지 key — master 통합 조치 (본문 bibitem 금지 준수·서지 여기 명기)

각 소절은 목적지 장 bib 에 대해 다음을 요구한다. **신규 2건 + 교차장 2건**의 정확한 서지:

| key | 상태 | 목적지 bib | 정확한 서지 |
|---|---|---|---|
| `schmitt2022` | **신규**(구 v4 archive 에만 존재) | ch1v22_bib(GR-2L) | C. Schmitt, A. Kube, N. Wagner, K. A. Friedrich, "Understanding the Influence of Temperature on Phase Evolution during Lithium-Graphite (De-)Intercalation Processes: An Operando X-ray Diffraction Study," *ChemElectroChem* **9**, e202101342 (2022). DOI: 10.1002/celc.202101342. |
| `artrith2018` | **신규**(lit_raw/03_graphite_si.md A8) | ch3v22_bib(SI-FR) | N. Artrith, A. Urban, G. Ceder, "Constructing first-principles phase diagrams of amorphous Li$_x$Si using machine-learning-assisted sampling with an evolutionary algorithm," *J. Chem. Phys.* **148**(24), 241711 (2018). DOI: 10.1063/1.5017661. |
| `leviaurbach1999` | 교차장(ch1v22_bib 존재) | ch3v22_bib 에 복사 필요(SI-FR) | M. D. Levi, D. Aurbach, "Frumkin intercalation isotherm...," *Electrochim. Acta* **45**, 167–185 (1999). DOI: 10.1016/S0013-4686(99)00202-9. |
| `msmr_origin2017` | 교차장(ch2v22_bib 존재) | ch3v22_bib 에 복사 필요(SI-FR) | M. Verbrugge, D. Baker, B. Koch, X. Xiao, W. Gu, *J. Electrochem. Soc.* **164**(11), E3243–E3253 (2017). DOI: 10.1149/2.0341708jes. (= 시드의 "Verbrugge 2017 JES164,E3243 ω 형식") |

- **LCO-Ω 는 교차장 조치 불요**: reimers1992·vanderven1998·motohashi2009·menetrier1999 전부 ch2v22_bib(LCO 인용 스코프)에 존재.
- **GR-2L 기타 인용**: dahn1991·ohzuku1993·persson2010·persson2010b·reynier2003 전부 ch1v22_bib 존재. schmitt2022만 추가.
- **정직 단서(schmitt2022)**: 메타(제목/venue/DOI)는 검증됨. 전문 유료(HTTP402)라 정량 온도계수 값은 lead 급 — 본 소절은 **정성 사실**("탈리튬 특이·고온 분리·상온 병합")만 인용하고 정량 0.30 mV/℃는 dahn1991에 정박.

---

## 3. 가정 (assumptions)

1. **cross-subsection ref**: si_fr(ch3)가 gr_2L(ch1)의 eq:gr2l-verdict를 \eqref 로 교차 참조 — 기존 ch3→ch1 xr-hyper 관행(예: eq:logisticsolve·eq:sum 참조) 동일 메커니즘 전제. 두 소절이 같은 빌드에 배치됨을 가정.
2. **stage-2L T-split 부호**: 고V ②(3↔2L, ΔS≈+15)·저V ③(2L↔2, ΔS≈−14)로 Δ(ΔS)=ΔS②−ΔS③=29>0, 분리=U②−U③ (eq:gr2l-tsplit, 부호 검증 완료).
3. **전자항 OFF 경로의 U(298) 불변**: 현 코드 ΔS_e 상시 ON → 토글 OFF는 dH 재기준으로 U_j(298) 보존(시드 §3 bit-exact 주의). 이는 **코드층(R2) 게이트 불변식**으로 본문에 명시만 하고 구현은 R2 위임.
4. **LCO 폴리타입**: 기존 문건(O3 LCO: T1 MIT 3.90V·T2/T3 order-disorder)을 기준으로 서술. 시드 §3 LCO-Ω 의 "3.70V(O2)/3.90V(O3)"는 폴리타입 뉘앙스로, 본 소절은 기존 tab:lco-staging anchor(T1/T2/T3)에 정합시키고 per-peak Ω 원리로 일반화(개별 값은 피팅 위임).

## 4. 불확실점·정직 공백 (uncertainties / honest gaps)

1. **GR-2L 분류 vs sec:broadening-class 불일치(중요)**: 시드 §2 XRD 표는 {1′↔4, 3↔2L, 2L↔2, 2↔1} 두-상 + {4↔3} 고용체(두-상 4). 기존 §7 sec:broadening-class 는 {dilute→4, 4L→3L, 3L→2L} 고용체 + {2L→2, 2→1} 두-상(두-상 2). **두 분류가 다름**. 해소: 본 소절은 XRD 서열(5 경계)로 **feature 개수**를 정박하고, **각 전이의 최종 두-상/고용체 지위는 피팅된 Ω_j 가 정함**(regsol2: 네 슬롯 전부 Ω/RT>2 → XRD 두-상 4와 정합)이라 명시해 §7 과 **원리 수준(Ω-판정)에서 합치**시켰다. 명칭↔행 매핑은 §7 역사 명명 따름(P3 #7). 이 불일치의 최종 조정(§7 문구 갱신 여부)은 master 판단 — 본 소절은 §7 을 **부정하지 않고** 정박·위임으로 봉합.
2. **tab:staging 2L-쌍 ΔS 초기값**: 현 0/−5는 Δ(ΔS)=29 를 과소예측. 정합엔 예: +15/−14 재배정 필요. **실제 수정 안 함 — 초기값 갱신 후보로만 보고**(P5). Δ(ΔS)=29 자체가 Dahn 분리기울기 역산값(직접 열량계 아님, tier B/C).
3. **si_fr 커널 부호 규약**: 리튬화 기준 V(θ)=U°−(RT/F)ln[θ/(1−θ)]−(Ω/F)(1−2θ)(시드 §1). 흑연 eq:Veq(탈리튬 ξ, +부호)와 ξ=1−θ·부호 반전으로 정합 — dQ/dV 는 절댓값이라 방향 불변(eq:sifr-kernel).
4. **tu_blend2024 article 번호 불일치**: 시드/LIT_SYNTHESIS 는 "Tu-Dao-Verbrugge-Koch JES171,**050520**(2024) 'clearly a superposition'". 기존 ch3v22_bib `tu_blend2024`=JES171,**050539**(동일 저자·동일 저널·연도, 컴패니언 논문 가능성). **충돌 신규 bibitem 도입 안 함** — 기존 key 사용·"명백한 중첩" 인용은 기존 blend 축소모형(eq:blend-dqdv)에 정박. 050520/050539 조정은 master 위임.
5. **#7 실적용 범위**: #7 정정 대상 문구는 sec:lco-hys 본문(eq:br-vanderven1998-1 축약 표기)에 있음. 본 소절은 **파라미터 의미 층위 명확화(eq:lcoom-slotsep + 각주)**로 제시 — 실제 sec:lco-hys 편집은 안 함(초안 경계). 기존 §13 은 이미 부분 정정(혼동 가드) 상태라 본 명확화가 그와 무모순.
6. **@5 stage-2L 의 R² 부호(정직 핵심)**: LCO @5=+1.90%p지만 **블렌드 단일셀 @5=−0.44%p**. 곧 stage-2L 세분은 다온도에서 물리적이나 단일 상온 곡선에선 식별 불가(오히려 자유도 penalty). W7 서사의 중추로 warnbox 에 명시.

## 5. P3 프로젝트 검수 7항목 자기점검

1. V_n 구분: 평가 전위는 내부 전위 V_n(계승 eq:xieq·eq:eqpeak 규약), dQ/dV 표기 유지. ✔
2. 전하 보존 중심식: GR/Si/LCO 모두 eq:eqpeak/eq:blend-dqdv/eq:lco-eqpeak(전하 보존 미분)에 정박. ✔
3. 순환 의존성: 본 소절들은 forward 평형 종만 다뤄 self-consistent loop 미도입(피팅 위임 명시). ✔
4. 순환 분류: 해당 없음(신규 loop 없음). Ω_Si·config ΔS·g(E_F,x)는 "피팅 위임" 명시. ✔
5. ref 방법론: vanderven1998(eq:br-vanderven1998-1)·marianetti 계보는 기존 §13/§15 srcbox 계승·본 소절은 그 매핑 재인용만. ✔
6. Ch1 기준식↔전달식 무충돌: GR-2L=eq:mu/eq:Uj/eq:eqpeak, Si=eq:Veq/eq:blend-dqdv, LCO=eq:lco-eqpeak — 전부 계승·재정의 0. ✔
7. ver.N↔Chapter 명칭: 역사 명명(stage 4→3 등)은 §7 관행 따름·표 캡션에 P3 명시. ✔

## 6. 최종 자기검증
- 신규 매크로·패키지 0(preamble 매크로만). boxed 최종식: GR-2L 2·SI-FR 2·LCO-Ω 2. 식마다 라벨(신규 라벨 중복 0). $ 균형·환경 균형 확인.
- 시드값 임의 변경 0·무근거 수치 0(전 수치 JSON/시드/문헌 정박, tier 병기). 기존 라벨·기호·식 재정의 0(계승).
