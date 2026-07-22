# W2 저작 NOTES — v1.0.24 R1 (author-sub W2, 강조 = 실측 근거 empirical grounding)

> 3개 신규 소절 초안: `gr_2L.tex`·`si_fr.tex`·`lco_omega.tex`. 초안만 — 실제 문건 파일 편집·git·commit 없음.
> W2 강조 = 이 세션 실검증치로 물리를 지지("데이터가 보이고 모델이 재현"), 검증 아티팩트를 본문에 명시 인용.

---

## 1. 읽은 파일 (근거)

**사양 원천 (최우선):**
- `results/comp_R1/AUTHOR_BRIEF.md` (전문) — 임무·사양·규칙.
- `results/REFLECT_SEED_TABLE.md` (전문) — 확정 물리·값·서지. 모든 수치의 1차 근거.

**표기·라벨·스타일 계승 (필독):**
- `_sections/ch1_sec05_width.tex` (전문) — 폭 $w_j=n_jRT/F$·이중지위(단상 평형예측/두-상 자유폭)·`eq:xieq`·`eq:wbase`·`sec:width-w`·2RT≈4958 J/mol.
- `_sections/ch1_sec06_eqpeak.tex` (전문) — 평형 peak `eq:eqpeak`·종 항등식 `eq:belliden`·감수율 읽기.
- `_sections/ch1_sec07_broadening.tex` (L1–90) — `sec:broadening-class` 두-상/고용체 분류·`tab:staging` 참조.
- `_sections/ch1_sec10_sum.tex` (tab:staging 정의부, L11–170) — 4전이 초기값 표(`4→3·3→2L·2L→2·2→1`, Ω=[6000,8000,10000,13000], ΔS=[+29,0,−5,−16]).
- `_sections/ch1_sec13_lcohys.tex` (전문) — 정칙용액 Ω·`eq:lco-gxi`·`eq:lco-gpp`·`eq:lco-dUhys`·`eq:lco-mit`·#7 대상 문구 `eq:br-vanderven1998-1`·혼동 가드.
- `_sections/ch1_sec15_lcoelec.tex` (전문) — 전자 엔트로피 `eq:dSe`·`eq:dSegate`·`eq:dSemolar`·`eq:U1T2`·ΔS_e≈−45.7 J/mol/K·T_ref 동결.
- `_sections/ch1_sec16_lcopeak.tex` (전문) — LCO 3-peak `eq:lco-eqpeak`·폭 지위·T1 온도신호.
- `_sections/ch1_sec17_msmr.tex` (MSMR 대응부) — `eq:lco-msmrpeak`·전자항 plug-in `eq:lco-SeV`·`sec:lco-code`.
- `_sections/ch1_sec14_lcodecomp.tex` (L1–55) — 삼분해 슬롯 규칙 `sec:lco-decomp`·`eq:lco-slots`.
- `_sections/ch3v22_sec02_cases.tex` (전문) — Si 케이스별·`tab:si-cases`·개형 서술.
- `_sections/ch3v22_sec03_blend.tex` (전문) — 공통-μ 반전 `eq:blend-balance`·합성식 `eq:blend-dqdv`·GS-2 `ssec:si-blend-gs2`.
- `_sections/ch3v22_notation.tex` (전문) — host 첨자·$f_\mathrm{Si}$·$Q_j^\mathrm{host}$·$\theta_j^\mathrm{host}$·$w_j^\mathrm{host}$ 계승 규약.
- `_sections/common_preamble_v1024.tex`·`ch1_preamble.tex` (전문) — 매크로·box 환경 확인(사용 매크로 전부 정의됨).
- `ch1v22_bib.tex`·`ch3v22_bib.tex`·`ch2v22_bib.tex` (bibitem key 목록) — 기존 key 재사용 vs 신규 판별.

**실측 검증 아티팩트 (W2 강조 근거 — `Claude/results/comp_v24/`):**
- `GRAPHITE_STAGING_XRD.md` — Dahn 1991 XRD 5-feature 확정·Ω 판정자·6전이 폐기.
- `T_SPLIT_FINDING.md`·`T_split.png` — stage-2L 온도분리 재현 0.271 mV/℃·병합~10℃·25℃병합/45℃2피크.
- `regsol2_result.json` — 흑연 Ω/RT=[4.06,2.02,3.55,4.07]·r2 0.938→0.943·δ_mV≈[1.6,1.5,1.5,1.0].
- `regsol_si_result.json` — Si Ω/RT=[0.2,0.2,0.2]바닥·w_mV=[37.3,70.3,28.0]·r2_regsol 0.962 vs r2_logistic 0.9985.
- `ablation_result.json` — 블렌드 @3 +0.66%p(0.9871→0.9938)·@5 흑연 −0.44%p(0.9871→0.9827).
- `lco_ablation_result.json` — LCO O2 plain 0.9441·@3 +1.25%p·@5 +1.90%p·@3+@5 +2.13%p·흑연 ref 0.940.
- `LCO_DIAGNOSIS.md` — LCO=흑연 동형 확증·전자항 상온 무영향(∂U/∂T만)·T1 이동 −0.47 mV/℃.

## 2. 실측 폭비 산출 검산 (W2 핵심 수치)
- RT/F @298.15 K = 25.69 mV.
- Si 폭비 = si_w_mV / (RT/F): 37.34/25.69=**1.45**, 70.32/25.69=**2.74**, 27.97/25.69=**1.09** → 전부 ≳1 (단일상 고용체).
- 흑연 두-상 폭비 = regsol2 δ_mV / (RT/F): 1.60/25.69=0.062, 1.48/25.69=0.058, 1.55/25.69=0.060, 1.01/25.69=0.039 → 전부 ≪0.12 (near-delta). Si/흑연 폭비 ≈ 20–50×.
- T-split 기울기: Δ(ΔS)/F = 29/96485 = 3.01e-4 V/K = **0.30 mV/℃** (Dahn); 재현 0.271 mV/℃.

## 3. 신규 라벨 (중복 0 — `_sections/` 전수 대조 확인)
- 소절: `ssec:gr-stage2L`·`ssec:si-frumkin`·`ssec:lco-omega-toggle` (brief 지시대로 `ssec:` prefix).
- 식(GR-2L): `eq:gr2l-mu`·`eq:gr2l-judge`(boxed)·`eq:gr2l-2Lsplit`(boxed).
- 식(SI-FR): `eq:sifr-widthratio`·`eq:sifr-Vtheta`·`eq:sifr-kernel`(boxed)·`eq:sifr-peakheight`·`eq:sifr-blend`(boxed).
- 식(LCO-Ω): `eq:lcoom-perpeak`·`eq:lcoom-U1T`·`eq:lcoom-toggle`(boxed).
- 계승 라벨(참조만, 재정의 0): eq:mu·eq:gpp·eq:spinodal·eq:Veq·eq:eqpeak·eq:belliden·eq:blend-balance·eq:blend-dqdv·eq:lco-eqpeak·eq:lco-gpp·eq:lco-msmrpeak·eq:br-vanderven1998-1·eq:lco-mit·eq:dSegate·eq:dSemolar·eq:U1T2·eq:lco-SeV·tab:staging·tab:si-cases + sec:* 라벨. (전수 cross-ref 검사: 계승 라벨 전부 `_sections/`에 존재, dangling 0.)

## 4. 신규 서지 key (본문 임의 bibitem 금지 — master 가 bib 에 추가. 아래 서지 명기)
- **`schmitt2022`** (GR-2L): Schmitt et al., 흑연 탈리튬화(delithiation) dV/dQ 에서 stage-2L 분리 재확인 (2022).
  *정직 단서*: 시드표·T_SPLIT_FINDING 이 "Schmitt et al. 2022 (graphite delithiation dV/dQ stage-2L)" 로 표기.
  완전 서지(권·페이지) 미확보 — master 가 bib 확정 시 정확 서지 보완 필요 (**tier B**: 2차 경유 서지 확인).
- **`artrith2018`** (SI-FR): Artrith et al., "Constructing first-principles phase diagrams of amorphous Li_xSi
  using machine-learning-assisted sampling…," *J. Chem. Phys.* **148**, 241711 (2018). (a-Si 제일원리·ML 포텐셜, tier A 서지.)
- **`verbrugge2017`** (SI-FR): Verbrugge et al., 삽입전극 열역학의 ω(정규용액) 형식, *J. Electrochem. Soc.* **164**, E3243 (2017).
  (시드표 @3 서지 "Verbrugge 2017 JES164,E3243 — ω 형식". 저자 리스트 완전 확인은 master bib 확정 시. **tier B** 서지.)
- **LCO-Ω 신규 key 없음** — 전부 기존 재사용(reimers1992·vanderven1998·motohashi2009·marianetti2004·menetrier1999·reynier2004·ml2024).
- 기존 재사용 key (GR/SI): dahn1991·ohzuku1993·dahn1995·persson2010·reynier2003·limthongkul2003·chevrier_dahn2009·obrovac_christensen2004·naboka_sic2021·tu_blend2024.

## 5. 4-tier 분류 (주요 주장)
- **확정(tier A/seed)**: Ω>2RT 판정자 `dμ/dξ|½=4RT−2Ω`(정규용액 수학)·Frumkin 커널 `dQ/dV=QF/|RT/(θ(1−θ))−2Ω|`(유도)·전자항 T_ref 동결→상온무영향(코드 L956 명시)·실측치 전부(seed·아티팩트 근거).
- **근거미발견/미확보**: `schmitt2022` 완전 서지(권·페이지)·SiOₓ 절대전위·SiOₓ 히스 절대 mV (ch3 표 각주 c·f 공백 계승).
- **추정(tier C)**: Si gallery 폭·중심 배치값(피팅 override 전제)·stage-2L ΔS 시드 대칭배치 예시(+14.5/−14.5)·LCO Ω_j^cat 수치(미배정).
- **미검증**: 전자항 ∂U/∂T의 다온도 실측(O3 다온도 데이터 부재)·T-split 정량 fit(현 재현은 물리 시드 주입 데모).

## 6. 가정 (assumptions)
1. **빌드 preamble = `common_preamble_v1024.tex`** — ch1(흑연)도 srcbox 사용(ch1_sec05)이라 union preamble 로 빌드. 사용 box(verifybox·keybox·warnbox·srcbox)·매크로(\dd·\eq·\bg·\rxn·\code) 전부 정의 확인.
2. **삽입 위치**: GR-2L=§5(sec:width-w) 뒤·§7(broadening) 앞. SI-FR=§3.2(sec:si-cases) 인접. LCO-Ω=§(lco-hys·lco-electronic·lco-peak) 정합. master 가 최종 배치.
3. **라벨 prefix `ssec:`** = brief §4 명시 지시 따름(ch1 관행은 `sec:`이나 brief 우선; 중복 0 확인). master 가 장 관행으로 재조정 가능.
4. **검증 아티팩트 인용** = bib 아닌 세션 산출물이라 본문에 `\code{파일명}` 로 인용(기존 문건이 코드·결과 파일을 prose 에 `\texttt{}` 로 인용하는 관행 따름).
5. **Frumkin 커널 θ = Si-host 자리 Li 점유** — ξ=1−θ 여집합 불변($\theta(1-\theta)=\xi(1-\xi)$)이라 eq:blend-dqdv 종과 정합(부호·형태 계승).

## 7. 정직 공백·불확실점 (honest gaps)
1. **@5 흑연 상온 −0.44%p vs LCO +1.90%p (프레이밍 필수).** stage-2L 5-feature 는 XRD-실재이나 **상온 단일-온도 곡선 $R^2$ 이득으로 나타나지 않음** — 25℃서 2L 병합이라 5전이 강제 시 오히려 −0.44%p. 이득은 (i) Ω>2RT 확증·(ii) 온도분리 재현·(iii) LCO 상온 분해(+1.90%p)에서 발효. gr_2L 의 warnbox 로 명시. **과대주장 방지: 5-feature 를 상온 곡선맞춤 이득으로 팔면 안 됨.**
2. **regsol2 Ω/RT[0]=4.06 vs XRD 4↔3 shoulder — framing 차이.** regsol2 는 모델 4-sharp-peak {4→3,3→2L,2L→2,2→1} 에 피팅해 전부 Ω>2RT. 시드표는 이를 "두-상 확증" 으로 확정. 그러나 XRD(Dahn)는 4↔3 를 고용체 shoulder(Ω<2RT)로 판정 — sharp 4-봉우리 피팅은 저·broad shoulder 를 분리하지 않으므로 **모순 아니라 다른 framing** (shoulder 는 XRD 가 가름). gr_2L verifybox 에 "framing 주의" 로 명시. **P3 #7(역사적 전이명 혼동 금지) 대응 지점 — audit 확인 요망.**
3. **Si: 순수 Si 는 logistic(자유 w)이 이미 우수(R²=0.9985) > regsol standalone(0.962).** Frumkin Ω 커널의 실작동은 sharpen 이 아니라 **단일상 가드**(Ω<2RT) + 블렌드 구조 이득(+0.66%p). Si 넓음은 Ω 아니라 폭 다중도 n_j>1(gallery 이산화)에서 옴. si_fr verifybox 에 명시. **과대주장 방지: Si Frumkin 이득을 "sharpen" 으로 팔면 안 됨.**
4. **전자항 상온 무영향 = 현 코드 재기준 조건부.** 기본 OFF 가 기존 커브 보존하려면 토글 OFF 가 U(T_ref) 불변 보장 필요(현 코드는 ΔS_e 상시 ON — OFF 전환 시 ΔH 재기준으로 U(298) 보존). = R2 코드 게이트 소관. lco_omega 박스에 명시(bit-exact 보장은 코드 몫).
5. **`schmitt2022`·`verbrugge2017` 완전 서지 미확보.** 권·페이지·저자 리스트는 시드표/2차 경유 표기 수준(tier B). master bib 확정 시 1차 서지 보완 필요.
6. **stage-2L ΔS 시드는 예시 배치.** +14.5/−14.5(T_m=10℃ 앵커)는 T_SPLIT 데모 값; 실 ΔS 정밀값은 entropic profiling 실측/피팅 위임(tier C). tab:staging default (0,−5) 갱신 후보로만 제시(실제 수정 안 함 — P5 "추가 후보").

## 8. P3 검수 7항목 자기점검 (본 초안 한정)
- (1) V_n 구분: 신규식은 평형 등온선/dQ/dV 라 V(=V_n) 사용, V_{n,app}/drive 미도입(범위 밖) — 일관.
- (2) 전하보존 중심식: GR/SI/LCO 커널 전부 전하 보존식 미분(eq:eqpeak·eq:blend-dqdv·eq:lco-eqpeak) 계승, OCV 직독 회귀 없음.
- (3) 순환의존: 신규 커널은 평형 종(음함수 반전은 eq:blend-balance 계승, 신규 순환 미도입). 전자항 고정점(eq:lco-SeV)은 기존 sec:lco-code 소관 — 참조만.
- (4) 순환 분류: 해당 없음(신규 순환 미도입). 전자항 동결근사=기존 "정의상 implicit/동결" 계승.
- (5) ref 6,7: 본 3소절 범위 밖(seed §6 완료). 미언급.
- (6) Chapter1 기준식 정합: GR 커널=흑연 §5·§6 계승·SI=블렌드 §3.3 host 판·LCO=§16 동형 — 전달식 충돌 없음.
- (7) ver.N vs Chapter 혼동: 역사적 전이명(4→3 등) 사용 시 XRD framing 명시(gap #2). ver.N 명칭 미사용.

## 9. 미해결/master 결정 경계
- 신규 bib key 3건 완전 서지 확정(master).
- `ssec:` vs `sec:` prefix 최종(master 장 관행).
- gr_2L 인라인 5-feature 표를 tab:staging 확장으로 승격할지(현재는 인라인 소표 — 초기값 표 중복 회피).
- @5 흑연 상온 −0.44%p 의 본문 노출 수위(warnbox 유지 vs 각주 강등) — audit/review 판단.
