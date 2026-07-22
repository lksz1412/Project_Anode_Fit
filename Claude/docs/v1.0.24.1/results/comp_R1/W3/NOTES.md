# W3 저작 NOTES — gr_2L · si_fr · lco_omega (comp_R1, 초안)

> 저작자: W3(작업 sub, pedagogy 강조: G-follow 전제부터·G-usable 소절 끝 닫힌식). 초안만 — 실제 문건 편집·git·commit 없음. master 확정 소관.

## 1. 읽은 파일과 근거 (저작 전 필독분 전부)
| 파일 | 이 초안에서 쓴 것 |
|---|---|
| `results/REFLECT_SEED_TABLE.md` (전체) | 확정 물리·값 최우선 원천. @3(Si Frumkin 커널·폭[1.45,2.74,1.09]·서지)·@5(흑연 5-feature·regsol2 Ω/RT[4.06,2.02,3.55,4.07]·T-split Δ(ΔS)=29·0.30 mV/℃·재현 0.271)·LCO 토글(ΔS_e≈−45.7·R²=0.944≈0.940·include_electronic_entropy)·#7 정정 문구. |
| `_sections/ch1_sec05_width.tex` | 폭 이중지위·$w_j=n_jRT/F$(eq:wbase)·logistic(eq:xieq,eq:logisticsolve)·중심 기울기 $sF/4RT$. GR-2L 배치 기준. |
| `_sections/ch1_sec06_eqpeak.tex` | 평형 peak 전하 보존 사슬(eq:eqpeak)·종 항등식(eq:belliden)·$dQ/dV=Q_j\xi(1-\xi)/w_j$. 세 소절 유도 골격. |
| `_sections/ch1_sec07_broadening.tex` | 전이별 분류(sec:broadening-class)·두-상/고용체·near-delta·현상학적 $w_j$. GR-2L·Si·LCO 두-상 측 정합. |
| `_sections/ch1_sec10_sum.tex` | tab:staging(4전이 초기값 U/ΔH/ΔS/Ω)·합산식(eq:sum)·$\partial U_j/\partial T=\Delta S/F$(eq:Uj). GR-2L 대응 근거. |
| `_sections/ch3v22_sec02_cases.tex` | a-Si 단일상 경사·케이스 개형·Li15Si4·1차 vs 순환·서지(chevrier_dahn2009 등). SI-FR 배치 인접. |
| `_sections/ch3v22_sec03_blend.tex` | 공통-μ 가산 중첩(eq:blend-dqdv,eq:blend-balance)·host 곱. SI-FR 블렌드 접속. |
| `_sections/ch3v22_notation.tex` | 계승 기호 2단 규약·host 첨자·$f_{Si}$. 기호 정합. |
| `_sections/ch1_sec13_lcohys.tex` | 정칙용액 Ω(eq:lco-gxi,gpp,spinodal,Veq,dUhys,Ubranch)·#7 정정 대상 문구·Van der Ven 대응·혼동 가드. LCO-Ω 핵심 근거. |
| `_sections/ch1_sec15_lcoelec.tex` | 전자 엔트로피 $\Delta S_e$·MIT 게이트·$T_{ref}$ 동결·$\propto T$·$-45.7$ J/molK·U1T2($T^2$ 곡률). 토글 근거. |
| `_sections/ch1_sec16_lcopeak.tex` | LCO 3-peak(eq:lco-eqpeak,charge,belliden,peakobs)·T1/T2/T3·폭 지위. LCO-Ω 커널 정합. |
| `_sections/ch1_sec11/12/14/17` | LCO 도입(T1/T2/T3 anchor·tab:lco-staging)·중심(eq:lco-dUdT,Kirchhoff)·삼분해(eq:lco-decomp,slots)·MSMR 동형(eq:lco-msmrpeak,U1V,SeV,plugin)·include_electronic 코드 지점. |
| `_sections/ch1_preamble.tex`·`common_preamble_v1024.tex` | 매크로·box 환경 확인(신규 패키지 X). |
| `ch1/2/3_*.tex`(드라이버)·`ch*_bib.tex` | 절 조립 순서·xr externaldocument 범위·기존 cite 키 전수. |

기존 preamble 매크로만 사용: `\dd \eq \rxn \bg \cell \cat \hys \dis \chg \kB \code{} \config \vib \eff \app \avg{}`. box: `keybox verifybox signbox bgbox srcbox warnbox`. 신규 패키지·매크로 0.

## 2. 신규 라벨 (중복 검사 완료 — 기존 라벨 인벤토리 대조)
- **gr_2L.tex** (Ch1): `ssec:gr-2L`, `tab:gr2L-features`, `eq:gr2L-mu`, `eq:gr2L-dmu`, `eq:gr2L-class`(boxed), `eq:gr2L-dSsplit`, `eq:gr2L-Tsep`(boxed).
- **si_fr.tex** (Ch3): `ssec:si-frumkin`, `eq:sifr-iso`, `eq:sifr-dVdtheta`, `eq:sifr-kernel`(boxed).
- **lco_omega.tex** (Ch2): `ssec:lco-perpeak`, `eq:lcoom-frumkin`, `eq:lcoom-kernel`(boxed), `eq:lcoom-toggle`(boxed).
- 브리프 지시대로 각 소절 `\subsection{...}\label{ssec:...}` 로 시작. 각 소절 boxed 최종식 ≥1(gr:2·si:1·lco:2). 식마다 라벨. 기존 라벨·기호·식 재정의 0(계승만).

## 3. 서지 (`\cite{key}`) — 기존 키 재사용 + 신규 2건
### 3a. 기존 키(그대로 사용, 재정의 없음)
- GR-2L: `dahn1991`(Ch1)·`ohzuku1993`(Ch1)·`rsc2021`(Ch1). (reynier2003 는 본문 미인용 — 표 ΔS 계보는 seed 시드값으로 표기.)
- SI-FR: `chevrier_dahn2009`·`obrovac_christensen2004`·`wang_asi2013`·`mcdowell_coreshell2013`·`limthongkul2003`·`verbrugge_lisi2016`·`tu_blend2024`(전부 Ch3 bib).
- LCO-Ω: 본문 인용은 전부 기존 Ch2 식·절 교차참조로 해결(신규 cite 0). Van der Ven·Marianetti 등은 기존 절이 이미 인용.

### 3b. 신규 키 2건 — 서지 명기(본문 임의 bibitem 금지 규율 준수, 웹 확인)
1. **`schmitt2022`** (GR-2L stage-2L 온도 발현):
   ```
   \bibitem{schmitt2022} C. Schmitt, A. Kube, N. Wagner, K. A. Friedrich, ``Understanding the Influence of Temperature on Phase Evolution during Lithium-Graphite (De-)Intercalation Processes: An Operando X-ray Diffraction Study,'' \emph{ChemElectroChem} \textbf{9}, e202101342 (2022). DOI: 10.1002/celc.202101342.
   ```
   - 확인: 제목·저자·저널·DOI = Wiley/Crossref 확정. **권/e-locator(9, e202101342)는 사용 시 Crossref 최종 대조 권장**(출처별 표기 상이 — OUCI 는 issue 표기 흔들림). 내용 부합: 승온(~43℃)서 stage-2L 발현 뚜렷 — seed ``Schmitt 2022(탈리튬 2L)'' 정확 대응.
2. **`artrith2018`** (SI-FR 비정질 Li_xSi 상도표):
   ```
   \bibitem{artrith2018} N. Artrith, A. Urban, G. Ceder, ``Constructing first-principles phase diagrams of amorphous Li$_x$Si using machine-learning-assisted sampling with an evolutionary algorithm,'' \emph{J. Chem. Phys.} \textbf{148}(24), 241711 (2018). DOI: 10.1063/1.5017661.
   ```
   - 확인: 저자·저널·권·article·DOI = AIP/arXiv(1802.03548) 확정. seed @3 서지 ``Artrith JCP148,241711(2018)'' 정확 일치. **주의**: 본 초안 si_fr.tex 본문은 artrith2018 을 아직 직접 인용하지 않음(a-Si 단일상 근거는 chevrier_dahn2009·wang_asi2013·mcdowell_coreshell2013 로 충분). master 가 원하면 (a) 문단 ``제일원리 비정질 경로'' 근거로 `\cite{artrith2018}` 추가 가능 — 서지는 위대로 준비.

### 3c. 타 장 bib 이월 필요(장 자기완결 규약 — 기존 키이나 해당 장 bib 미수록)
- **`leviaurbach1999`** (Frumkin isotherm 리뷰): si_fr.tex(Ch3)가 인용. 현재 **Ch1 bib 에만** 수록. Ch3 bib 이월 필요. (전문: Levi & Aurbach, Electrochim. Acta 45, 167 (1999). DOI 10.1016/S0013-4686(99)00202-9.)
- **`msmr_origin2017`** (Verbrugge 2017 JES164 E3243 — ω 형식): si_fr.tex(Ch3)가 인용. 현재 **Ch2 bib 에만** 수록. Ch3 bib 이월 필요. (seed @3 서지 ``Verbrugge 2017(JES164,E3243)'' = 이 키.)
- 규약 근거: bib 파일 헤더 ``공통 키의 타 장 중복 수록은 의도(D22)''. 이월은 master/bib 소관(초안은 표기만).

## 4. 물리 가정·시드값 tier
- GR-2L: 5-feature staging = XRD 확정(Dahn) tier A 골격. ΔS 시드(+29/+15/−14/−16)·regsol2 Ω/RT·0.30 mV/K·T*≈10℃·재현 0.271 = seed/T_SPLIT_FINDING 내부 산출(전이별 정밀값 아님 — **tier C 시드**, round-trip override). 표에 명기.
- SI-FR: a-Si 단일상 = tier A(chevrier_dahn2009 등). 폭[1.45,2.74,1.09] = regsol_si 내부 피팅(**tier C 초기값**). 커널 형태(eq:sifr-kernel) = tier A(Frumkin 표준, leviaurbach1999). Li15Si4 ~50–60mV = tier A(obrovac_christensen2004).
- LCO-Ω: 커널 동형·per-peak Ω = tier A(정칙용액 표준). ΔS_e≈−45.7 J/molK = 게이트 골 깊이(seed/ch1_sec15 산출, **tier C**). R²=0.944/0.940 = 내부 ablation(**tier C**, 곡선 품질 대조용). #7 정정 = 물리 유지·문구만(seed §5).
- 무근거 수치 0. seed 값 임의 변경 0.

## 5. 정직한 공백·불확실점 (master/검수 판단 요망)
1. **[GR-2L 분류 긴장 — 최중요]** seed @5 의 두-상/고용체 배정(두-상 4={1'↔4,3↔2L,2L↔2,2↔1}·고용체 1={4↔3})과 **기존 `ch1_sec07_broadening`(sec:broadening-class)의 배정**(두-상 2={2L→2,2→1}·고용체={dilute→4,4→3,3→2L})이 **3↔2L·1'↔4 에서 불일치**. 본 초안은 충돌을 본문에서 단정하지 않고, (i) seed 5-feature 를 제시하되 (ii) ``최종 판정은 피팅된 Ω_j''(양 문건 공통 원칙)로 봉합, (iii) regsol2 의 3↔2L=2.02(문턱 근접)를 ``경계 feature''로 정직 표기. **master 가 seed 배정으로 ch1_sec07 을 갱신할지, 초안 표현을 유지할지 결정 필요.** P5(baseline 보호)·P3 gate #6(Ch1 기준식 충돌 금지) 위반 회피 위해 초안은 재작성하지 않고 플래그만.
2. **[GR-2L ΔS 재배정]** 2L 쌍 ΔS(+15/−14, Δ=29)는 seed T-split 재배정으로 **기존 tab:staging(3→2L=0·2L→2=−5, Δ=5)과 수치 다름**. 본 초안 tab:gr2L-features 는 seed 값을 시드로 싣고 tab:staging 은 ``모델 초기값''으로 대응 표기 — 두 표의 ΔS 열이 다른 것은 T-split 반영 여부 차이. master 가 tab:staging 갱신 여부 결정.
3. **[LCO O2/O3 vs T1/T2/T3 라벨]** 브리프 LCO-Ω 사양은 ``3.70V(O2)/3.90V(O3) 두-상 sharp''로 적으나, **기존 문건(ch1_sec11/13/16)은 T1(MIT~3.90V)/T2(~4.05V)/T3(~4.17–4.20V)** 골격. 본 초안은 ``정합'' 지시(브리프 §1.3)에 따라 **기존 T1/T2/T3 를 채택**하고 O2/O3 stacking 은 언급하지 않음(ch1_sec11 은 O3→H1-3 를 4.55V T4 범위밖으로만 둠). 3.70V(O2) feature 는 기존 3-전이 골격에 없음 — master 가 O2/O3 도입 원하면 별도 결정(하프셀 상한·stacking 상 추가는 범위 판단 요).
4. **[교차참조 경계]** ch2(LCO)는 ch1 만 externaldocument(ch3 미포함). 따라서 lco_omega.tex 는 **Si 커널(eq:sifr-kernel, ch3)을 `\eqref` 로 참조 불가** — ``Chapter 3 Si-host 와 같은 정칙용액 커널''로 서술만(라벨 참조 X). 세 소절이 같은 Frumkin 커널을 공유하나 라벨 상호참조는 장 순서(ch1→ch2→ch3) 제약 준수.
5. **[R² 출처]** 0.944(LCO)/0.940(흑연)은 seed·LCO_DIAGNOSIS 내부 ablation 값으로 **외부 서지 없음** — verifybox 에 ``내부 ablation''으로 표기. 실제 수치 재현은 R2(코드) 게이트 소관.
6. **[전자항 bit-exact 주의]** eq:lcoom-toggle 의 ``OFF=커브 불변''은 $U_j(298)$ 보존을 위한 ΔH 재기준 전제(seed §3: 현행 코드는 ΔS_e 상시 ON). 본 초안은 이 전제를 본문·주의로 명기했으나 **실제 bit-exact 보장은 R2 코드 게이트**(문건은 규약만).
7. **[reynier2003 미인용]** GR-2L 표 ΔS 계보를 seed 시드로 표기하며 reynier2003(흑연 삽입 엔트로피 anchor)을 본문 직접 인용하지 않음 — master 가 ΔS 부호·스케일 anchor 로 `\cite{reynier2003}`(Ch1 기존 키) 보강 원하면 (c) 문단에 추가 가능.

## 6. P3 검수 7항목 자기점검(초안 수준)
1. V_n·V 구분: 평가 전위는 기존 관행대로 $V$(내부 $V_n$ 은 §pol 소관) — 신규 소절이 $V_n$ 재정의 안 함. OK.
2. 전하 보존 중심식: 세 소절 모두 $dQ/dV$ 를 전하 보존 사슬(eq:eqpeak/lco-charge 형)로 유도 — OCV 직독 회귀 없음. OK.
3. 순환 의존성: 신규 소절은 forward(Ω·w→peak) — self-consistent loop 신설 없음. LCO 전자항 되먹임은 기존 eq:lco-U1V 참조(신설 X).
4. 4분류: GR-2L 분류 긴장(§5.1)은 ``피팅이 정함''(정의상 implicit/수치해법 아님, 물리 가정 정합)으로 봉합 — 논리 공백 아님 명기.
5. ref 6,7: 본 세 소절 범위 밖(자기무모순 부록 소관) — 건드리지 않음.
6. Ch1 기준식 충돌: GR-2L 은 ch1_sec07 분류와 잠재 충돌 → 본문 단정 회피·플래그(§5.1). Si·LCO 는 기존 커널 계승(충돌 없음).
7. ver.N vs Chapter N: 신규 소절은 Chapter 골격·라벨만 사용, ver.1~5 역사명칭 미혼용. OK.
