# W8 저작 NOTES — v1.0.24 R1 (강조: 표기·라벨 seamless 통합)

> 작업 sub W8. 초안만 저작(실제 문건 편집·git·commit 금지). 결과는 본 폴더에만.
> 강조점: 기존 기호·라벨 규약 정확 계승, 이식점 비가시화(그래프트 invisible).

산출물: `gr_2L.tex` · `si_fr.tex` · `lco_omega.tex` (+ 본 NOTES).
검증: 세 파일 모두 env/brace 균형 OK · boxed 최종식 ≥1(1/2/1) · 모든 `\ref/\eqref` 해소(58건) · 각 파일 self-contained(교차-산출물 ref 0) · 신규 cite key는 아래 §5에만.

---

## 1. 읽은 파일(저작 근거)

**최우선 시드**
- `results/REFLECT_SEED_TABLE.md`(전문) — @3 Si-Frumkin·@5 흑연 5-feature·LCO 전자항 토글·#7 확정 물리·값·서지.
- `results/comp_R1/AUTHOR_BRIEF.md`(전문) — 임무·사양·규율.

**흑연(GR-2L 근거)**
- `_sections/ch1_sec05_width.tex`(전문) — 폭 이중지위·`eq:wbase`·`eq:xieq`·`sec:width-w` "(1−Ω/2RT) 배 유효 폭"·`tab:staging` 참조 관행.
- `_sections/ch1_sec06_eqpeak.tex`(전문) — `eq:belliden`·`eq:eqpeak` 평형 peak 유도.
- `_sections/ch1_sec07_broadening.tex`(L1–70) — `sec:broadening-class` 두-부류·두-상 문턱·L 접미 명명.
- `_sections/ch1_sec10_sum.tex`(L1–60) — `tab:staging` 4전이 초기값(U·ΔH·ΔS·Q·Ω·ΔH_a)·`eq:sum`.
- `_sections/ch1_sec02b_part0.tex`(L30–60) — `eq:mu`(μ(θ)=μ°+RT ln[θ/1−θ]+Ω(1−2θ))·`eq:gxi`.
- `_sections/ch1_sec03_center.tex`·`ch1_sec04_hys.tex`(라벨 위치) — `eq:Uj`·`eq:center`·`eq:gpp`·`eq:spinodal`·`eq:Veq`·`eq:dUhys`·`eq:Ubranch`.
- `results/comp_v24/GRAPHITE_STAGING_XRD.md`(전문) — Dahn 1991 XRD 5-feature 서열·Ω 판정자·4↔3 고용체 예외·6+ 폐기.
- `results/comp_v24/T_SPLIT_FINDING.md`(전문) — stage-2L 엔트로피 안정화·Δ(ΔS)=29→0.30 mV/℃·Tm≈10℃·45℃분리/25℃병합·재현 0.271·Schmitt 2022.

**Si(SI-FR 근거)**
- `_sections/ch3v22_sec02_cases.tex`(전문) — `sec:si-cases`·`ssec:si-elemental/siox/sic/thermal`·`tab:si-cases`·케이스 개형.
- `_sections/ch3v22_sec03_blend.tex`(전문) — `sec:si-blend`·`eq:blend-dqdv`·`eq:blend-balance`·`eq:blend-limit`·`ssec:si-blend-gs2`·공통-μ 가산.
- `_sections/ch3v22_notation.tex`(전문) — host 첨자·`Q_j^host`·`w_j^host`·`θ_j^host`·`f_Si`·`m_Si`·`C_bg`(전극 단위) 계승 규약.

**LCO(LCO-Ω 근거)**
- `_sections/ch1_sec13_lcohys.tex`(전문) — `eq:lco-gxi`·`eq:lco-gpp`·`eq:lco-spinodal`·`eq:lco-dUhys`·`eq:lco-mit`·`sec:lco-hys-od` 혼동 가드·`eq:br-vanderven1998-1`(#7 정정 대상 문구 소재지).
- `_sections/ch1_sec15_lcoelec.tex`(전문) — `eq:Se`·`eq:dSe`·`eq:dSegate`·`eq:dSemolar`·`eq:U1T2`·`eq:ggate`·T_ref 동결·−45.7 J/(mol K)·부호 규약.
- `_sections/ch1_sec16_lcopeak.tex`(전문) — `eq:lco-charge`·`eq:lco-belliden`·`eq:lco-eqpeak`·T1/T2/T3 전위(3.90/4.05/4.17–4.20 V).
- `_sections/ch1_sec17_msmr.tex`(전문) — `eq:msmr`·`eq:lco-msmrmap`·`eq:lco-msmrpeak`·`eq:br-msmr-1`·`sec:lco-code(-msmr)`·전자항 plug-in·`eq:lco-U1V`·`eq:lco-SeV`.
- `_sections/ch1_sec12_lcocenter.tex`(라벨) — `eq:lco-dUdT`·`eq:lco-n0sub`. `ch1_sec14_lcodecomp.tex`(라벨) — `sec:lco-decomp` 삼분해.
- `_sections/ch2v22_notation.tex`(전문) — Ch2(LCO) 계승 2단 규약.

**preamble/규약**
- `_sections/common_preamble_v1024.tex`·`ch1_preamble.tex`(전문) — 매크로(`\dd·\eq·\rxn·\cat·\bg·\cell·\oc·\kB·\config·\code`)·박스 환경(bgbox·srcbox·verifybox·signbox·warnbox·keybox…)·`xr-hyper` 교차장 참조.
- 三 bib(`ch1v22_bib`·`ch2v22_bib`·`ch3v22_bib`) — 90개 bibitem key 대조(신규 key 판별용).

**독립성**: 경쟁 저작 sub(W1·W6 등)의 산출물은 읽지 않음(독립 산출물 비교 무결성 보존).

---

## 2. 계승한 기존 라벨 (내가 참조한 것 전부)

세 파일이 참조하는 기존 정의 라벨 — 전부 실재 확인·해소됨(재정의 0):

- **gr_2L.tex(12)**: `eq:mu` · `eq:gpp` · `eq:spinodal` · `eq:Uj` · `sec:center` · `sec:hys` · `sec:width` · `sec:width-w` · `sec:broadening` · `sec:broadening-class` · `tab:staging` · `fig:staging`.
- **si_fr.tex(17)**: `eq:mu` · `eq:Veq` · `eq:lco-Veq` · `eq:eqpeak` · `eq:gpp` · `eq:blend-dqdv` · `eq:blend-limit` · `eq:br-msmr-1` · `sec:eqpeak` · `sec:width-w` · `sec:broadening` · `sec:si-cases` · `sec:si-blend` · `sec:lco-code-msmr` · `ssec:si-elemental` · `ssec:si-sic` · `ssec:si-blend-gs2` · `ssec:weff`.
- **lco_omega.tex(24)**: `eq:mu` · `eq:lco-gxi` · `eq:lco-gpp` · `eq:lco-spinodal` · `eq:lco-eqpeak` · `eq:lco-msmrpeak` · `eq:lco-mit` · `eq:br-vanderven1998-1` · `eq:dSegate` · `eq:dSemolar` · `eq:U1T2` · `eq:lco-dUdT` · `eq:lco-U1V` · `eq:lco-SeV` · `sec:lco-peak` · `sec:lco-code` · `sec:lco-code-msmr` · `sec:lco-hys-gap` · `sec:lco-hys-od` · `sec:lco-hys-dope` · `sec:lco-decomp` · `sec:lco-electronic` · `sec:lco-Se-scale` · `sec:broadening`.

계승한 기호(재정의 없이 그대로): `V_n·U_j·U_j^{\,d}·U_j^\cat·\Omega_j·\Omega_j^\cat·w_j=n_jRT/F·\xi_{\eq,j}·\theta_j·\sigma_d·Q_j·Q_j^\mathrm{host}·Q_j^\cat·C_\bg·\Delta S_\rxn·\Delta S_{\rxn,j}^\cat·\Delta S_{e,1}^\mathrm{mol}·\Delta S_j^\config·f_\mathrm{Si}·T_\mathrm{ref}·2RT 문턱`. 매크로도 preamble 정의분만 사용(신규 매크로·패키지 0).

---

## 3. 신규 라벨 (내가 도입한 것 전부 — 중복 0 확인)

장 관행에 맞춘 prefix·충돌 검사 통과(문서 전역 380 라벨과 대조):

- **gr_2L.tex**(ch1 흑연, `sec:`/`eq:`/`tab:` 관행): `sec:staging-2L` · `tab:staging-xrd` · `eq:staging-mujudge` · `eq:staging-2Lsplit`.
- **si_fr.tex**(ch3 Si, `ssec:`/`eq:` 관행): `ssec:si-frumkin` · `eq:si-frumkin-V` · `eq:si-frumkin` · `eq:si-frumkin-blend`.
- **lco_omega.tex**(LCO, `sec:lco-*`/`eq:lco-*` 관행): `sec:lco-omega` · `eq:lco-omega-perpeak` · `eq:lco-etoggle`.

**★라벨 prefix 결정(seamless 근거)**: AUTHOR_BRIEF §4 는 "`\label{ssec:...}` 로 시작"을 일괄 지시하나, §2 는 "라벨 prefix 그대로 계승·장 관행 따라"를 지시한다. 두 지시가 상충할 때 W8 강조점(이식점 비가시화)에 따라 **실제 장 관행**을 택했다:
- ch1 흑연·LCO native subsection 은 전부 `sec:`(예 `sec:width-w`·`sec:dist`·`sec:lco-hys-od`) → gr_2L·lco_omega 도 `sec:` 사용. `ssec:` 를 쓰면 `sec:` 뿐인 장 안에서 그래프트가 가시화됨.
- ch3 Si native subsection 은 전부 `ssec:`(예 `ssec:si-elemental`) → si_fr 만 `ssec:` 사용.
→ 각 파일이 이웃 절과 동일 prefix라 이식점이 비가시. 이 편차는 의도적이며 audit/review 가 §4 문자와 대조할 수 있게 여기 명시.

---

## 4. 각 소절 사양 대응 (시드→저작)

**gr_2L (GR-2L)** — XRD 5-feature staging(`tab:staging-xrd`: 두-상 4 + 고용체 shoulder 1, Dahn/Ohzuku) · Ω 판정자 `eq:staging-mujudge`(dμ/dθ|½=4RT−2Ω, 고정 d-간격 공존 ⇔ Ω>2RT) · stage-2L 온도 분리 boxed `eq:staging-2Lsplit`(Δ(ΔS)/F≈0.30 mV/K·Tm≈10℃·45℃분리/25℃병합·재현 0.271) · 기존 4전이가 두-상을 이미 담음(3→2L·2L→2 별도 명명 = 상 추가 아님)·6+ XRD 미지원 curve-fitting 폐기.

**si_fr (SI-FR)** — a-Si 단일상 고용체 근거(폭/(RT/F)≈[1.45,2.74,1.09]≳1 vs 흑연 두-상 ≪0.12·20–50배) · Frumkin 커널 boxed `eq:si-frumkin`(dQ/dV=Q F/|RT/[θ(1−θ)]−2Ω|·Ω<2RT) 유도(`eq:si-frumkin-V`) · Ω=0 이상 회수·Ω→2RT 임계 발산·Ω<0 broaden · (1−Ω/2RT) 배 유효폭이 `sec:width-w` 단상 예고의 Si 판 · 소수 broad gallery·c-Li₁₅Si₄ 유일 두-상 · 블렌드 가산중첩 `eq:si-frumkin-blend`(Tu 2024 "superposition"·C_bg 전극 단위).

**lco_omega (LCO-Ω)** — per-peak Ω^cat boxed `eq:lco-omega-perpeak`(전이별 g''|½=2RT−Ω^cat·T1 두-상/T2·T3 배분·+1.25%p) · **#7 정정** warnbox(Ω_j^cat = 진행좌표 ξ_j 의 유효 평균장 축약·미시 질서구조 아님·config ΔS 별도 슬롯·`sec:lco-hys-od` 가드 계승·물리 불변 문구만) · 전자항 토글 boxed `eq:lco-etoggle`((dQ/dV)^ON_Tref=(dQ/dV)^OFF_Tref 커브 중립·∂U/∂T=ΔS_e^mol/F ON에서만·R²0.944≈0.940·include_electronic_entropy 기본 OFF).

---

## 5. 신규 cite key (본문 `\cite` 만·bibitem 미삽입 — 서지 여기 명기)

§4 규율대로 신규 key 는 본문에 `\cite{}` 로만 두고 bibitem 은 master 가 해당 bib 에 추가한다.

- **`schmitt2022`** (gr_2L) — Schmitt 등, 흑연 **탈리튬화 dV/dQ** 에서 stage-2L 분리 재확인(delithiation-특이적). 서지 실재는 시드 검증분(`T_SPLIT_FINDING.md` §2·§서지, `GRAPHITE_STAGING_XRD.md` 계보)으로 확인됨. ★**정밀 서지(저널·권·페이지) 미확보** — 시드의 `lit_raw/` 원문에서 master 가 확정 필요. tier: 서지 실재(시드 확인)·정밀 좌표 미확보.
- **`artrith2018`** (si_fr) — N. Artrith 등, 비정질 Li$_x$Si 상도표·기계학습 퍼텐셜 표본화, **J. Chem. Phys. 148, 241711 (2018)**(좌표는 AUTHOR_BRIEF §3 SI-FR·REFLECT_SEED_TABLE §1 명시). tier: 서지 좌표 브리프/시드 명시.

기존 key 로 충당한 브리프 서지: Dahn PRB44,9170(1991)=`dahn1991` · Reynier JPS119–121,850(2003)=`reynier2003` · Ohzuku JES140,2490(1993)=`ohzuku1993` · Chevrier–Dahn JES156,A454(2009)=`chevrier_dahn2009` · **Verbrugge 2017 JES164,E3243(ω 형식)=`msmr_origin2017`**(브리프 서지의 Verbrugge 2017 = 문서의 MSMR 원 논문 key로 확인) · Tu–Dao–Verbrugge–Koch JES171,050520(2024)=`tu_blend2024` · Van der Ven 1998=`vanderven1998` · Reimers 1992=`reimers1992` · Motohashi 2009=`motohashi2009` · ML/스케일브리징=`ml2024` · Ménétrier 1999=`menetrier1999` · c-Li₁₅Si₄=`obrovac_christensen2004` · NMR=`ogata_nmr2014` · a-Si 단일상=`wang_asi2013`·`mcdowell_coreshell2013` · 첫사이클 두-상=`limthongkul2003`.

---

## 6. 가정·판단(honest)

1. **LCO feature 명명 = 확정 문서 기준(T1/T2/T3)**. 브리프 §3 LCO-Ω 은 "3.70V(O2)/3.90V(O3)"를 언급하나, 확정 문건(`ch1_sec13/16`)은 **T1(MIT,3.90V)·T2(4.05V)·T3(4.17–4.20V)** 이고 시드표 §2 도 H1/H2·x0.5 order-disorder·H1-3 로 적는다. 3.70V·O2 는 확정 문건·시드표에 없어(무근거 수치 X·P5) **채택하지 않고** T1/T2/T3 로 저작. → §7 gap.
2. **stage-2L 는 새 상 아님**. 시드/브리프대로 3↔2L·2L↔2 를 두-상 분리쌍으로 저작. 이는 `tab:staging` 이 이미 별도 명명한 두 전이의 ΔS 차(Δ≈29) 설명이지 전이 추가가 아님(6+ 폐기와 근본 구분). 전이별 분류(어느 것이 두-상/고용체)의 최종 판정은 `sec:broadening-class`·피팅된 Ω 에 위임(내 소절이 실명 분류를 강제하지 않음).
3. **Δ(ΔS)=29 배분(+15/−14)은 tier-C 배치**. 분리 기울기 0.30 mV/K 에서 역산한 **차**만 확정(tier B, 직접 열량계 아님)·개별 절대값은 분리쌍 평균 기준 배치(T_SPLIT 의 ±14.5 대칭 앵커도 동가). 절대 엔트로피는 round-trip 피팅 몫으로 명기.
4. **Frumkin 커널의 골격 정합 검증(내 손계산)**: V(θ)=U°−(RT/F)ln[θ/1−θ]−(Ω/F)(1−2θ) ⟹ dQ/dV=Q F/|RT/[θ(1−θ)]−2Ω| 가 (i) Ω=0 에서 `eq:eqpeak` 이상 종과 글자까지 일치, (ii) 중심 분모 4RT−2Ω=4RT(1−Ω/2RT) 라 `sec:width-w` 의 "(1−Ω/2RT) 배 유효폭"과 정확 정합, (iii) Ω→2RT 임계 발산·`eq:gpp` 문턱과 동일 2RT. → 브리프 커널식과 항등(무모순).
5. **개선% · R² · regsol 폭은 시드 검증값 인용**(재유도 아님): +1.25%p(per-peak Ω)·+1.90%p(@5)·R²0.944/0.940·폭[1.45,2.74,1.09]·Ω/RT[4.06,2.02,3.55,4.07] — 근거는 시드표(ablation/LCO_DIAGNOSIS/regsol). tier 는 시드 등급 계승.
6. **전자항 토글의 "커브 중립"에 조건 명기**: 무조건 아니라 **U_j(T_ref) 보존** 하에서만. 현 코드는 ΔS_e 상시 ON 이라 OFF 시 dH 재기준 필요(U(298) 보존) — 이 보장은 **R2(코드) 게이트 소관**임을 verifybox 에 정직 명기(과대주장 방지).
7. **각 소절 self-contained**: 교차-산출물 참조(lco_omega→Si·si_fr→gr_2L) 제거 → master 가 세 소절을 **독립적으로/임의 순서로** 배치해도 미해소 ref(`??`) 무발생. 커널 통일성("흑연·Si·LCO 같은 한 커널") 관찰은 같은-장 `eq:mu`·`eq:gpp` 앵커 + Chapter 3 서술 언급으로 보존.

---

## 7. 정직 gap·불확실점 (master/audit/review 판단 필요)

1. **[문건 정합] `ch1_sec07_broadening` 3→2L 분류 상충.** 현 `sec:broadening-class` 산문은 3→2L 을 **고용체** 부류로 묶으나(L15), XRD 문건(Dahn)·시드·본 GR-2L 은 3↔2L 을 **두-상**(2L 분리쌍)으로 읽는다. 나는 시드/브리프대로 두-상으로 저작하되 실명 분류는 `sec:broadening-class` 로 위임(강제 relabel 안 함). → `ch1_sec07` 산문 조정은 master 편집·audit 판정 사항(나는 실파일 미편집).
2. **[표 정합] `tab:staging` ΔS 초기값.** 표는 3→2L:0.0·2L→2:−5.0(Δ=5)이나 stage-2L 시드는 +15/−14(Δ=29). 또 T-split 병합앵커(Tm=10℃ 중심 일치)를 반영하면 25℃ 중심 간격이 표의 0.140/0.120(20 mV)보다 훨씬 좁아진다(≈4.5 mV). 나는 **메커니즘(분리율·병합)만** 저작하고 절대 중심값은 손대지 않음. 표 수치 갱신(Δ→29·중심 재앵커)은 master 편집·피팅 몫.
3. **[서지] `schmitt2022` 정밀 좌표 미확보**(§5). 시드 `lit_raw/` 에서 저널/권/페이지 확정 필요.
4. **[구조 명칭] ver.N vs Chapter N.** LCO 산출물의 파일명은 `ch1_sec1X`(역사적)이나 새 구조에선 Chapter 2(LCO). 라벨은 `sec:lco-*`(불변)라 seamless 는 라벨 기준으로 처리했고, "Chapter 2/3" 서술 명칭은 기존 본문 관행(ch1 이 "Chapter 2" 명명)을 따름. 최종 챕터 번호 매핑은 master 조립 시 확정.
5. **[브리프 §4 문자 편차] 라벨 prefix.** ch1 소절에 `sec:` 사용(§3 근거) — §4 의 일괄 "ssec:" 문자와 다름. 의도적·seamless 근거 명시. review 가 §4 문자 준수를 요구하면 gr_2L·lco_omega 의 `sec:`→`ssec:` 일괄 치환은 자명(라벨·`\ref` 동시 갱신, 단 그 경우 이웃 절과 prefix 불일치가 생김).
6. **[범위] 코드 관련 서술은 개념 수준만.** `include_electronic_entropy` 플래그·`kernel:'regsol'` 폴백·U(298) bit-exact 보장은 R2(코드) 구현·게이트 소관. 내 LaTeX 는 물리·규약만 적고 구현 확정은 안 함(codebox 남발 없이 verifybox 로 조건만 명기).
7. **[추가 후보·미수정]** LCO H1-3 미세구조 더 세분(@5 +1.90%p 의 잔여)은 lco_omega 말미에 **추가 후보**로만 표기(실제 세분 전이 미도입 — P5 "추가 후보로 보고"). SiO_x 절대전위·Si 저온 ΔS(T) 등 §3.2 기존 "확인 필요" 공백은 그대로 존중(placeholder 개형만 유효).

---

## 8. 검수 7항목(P3) 자기점검 요약
- (1) V_n 구분: 계승 기호 그대로, 신규 전위기호 도입 0. (2) 전하보존 중심식: si_fr `eq:si-frumkin-blend`·lco 는 `eq:lco-eqpeak` 계승(OCV 회귀 아님). (3)(4) 순환의존: 해당 없음(내 소절은 평형 종·per-peak Ω·토글이라 self-consistent loop 신설 없음). (5) ref 방법론: Van der Ven(#7)·MSMR(Verbrugge)·Dahn 은 기존 srcbox 계보 계승(신규 srcbox 는 gr_2L Schmitt/Dahn 다리만, 4항목 형식 준수). (6) Chapter 1 기준식 정합: 세 소절 모두 `eq:mu·eq:eqpeak·eq:sum` 골격 위에서 파생(충돌 0). (7) ver/Chapter 명칭: §7.4 에 매핑 명시.
