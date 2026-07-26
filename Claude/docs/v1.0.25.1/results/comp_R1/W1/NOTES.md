# W1 저작 NOTES — 근거·가정·불확실점 (comp_R1 R1 작업 sub, 강조=이론적 엄밀성)

> 산출물: `gr_2L.tex` · `si_fr.tex` · `lco_omega.tex` (각 자기완결 `\subsection`).
> 경계 준수: 실제 문건 파일 편집 X · git X · 신규 bibitem 본문 삽입 X · 시드값 임의 변경 X.
> 강조(W1): 전제→제일원리 유도 완결성. 모든 최종식 boxed, 식마다 라벨, (a)출발/(b)연산/(c)중간식/(d)박스 구조.

---

## 1. 읽은 원천 파일 (저작 근거)

| 파일 | 쓴 곳 | 핵심 계승분 |
|---|---|---|
| `results/REFLECT_SEED_TABLE.md` | 3개 전부 | 확정 물리·값·서지(최우선). @3 Si-host·@5 흑연 5-feature·LCO 전자항 토글·#7. |
| `results/comp_R1/AUTHOR_BRIEF.md` | 3개 전부 | 소절 사양·출력 규율·5 공통 규칙. |
| `_sections/ch1_sec02b_part0.tex` L34–64 | gr_2L·si_fr·lco_omega | `eq:mu`(정규용액 μ)·`eq:gxi`·`eq:sm-thresh`(g″≥0⇔Ω≤2RT, θ=½서 4RT). |
| `_sections/ch1_sec03_center.tex` L47–63 | gr_2L·lco_omega | `eq:Uj`·∂U/∂T=ΔS_rxn/F·`fig:UjT`(네 전이 기울기=ΔS/F). |
| `_sections/ch1_sec04_hys.tex` L27–120 | gr_2L·si_fr·lco_omega | `eq:gpp`·`eq:spinodal`·`eq:Veq`·`eq:dUhys`·`eq:hyssub`. |
| `_sections/ch1_sec05_width.tex` L264–319 | 3개 전부 | `eq:wbase`·`eq:xieq`·폭 이중지위(단상=평형예측 / 두-상=현상학). |
| `_sections/ch1_sec06_eqpeak.tex` L13–35 | 3개 전부 | `eq:belliden`(종 항등식)·`eq:eqpeak`(평형 peak). |
| `_sections/ch1_sec07_broadening.tex` L12–178 | gr_2L·si_fr | 전이별 분류(`sec:broadening-class`)·Maxwell·Dreyer·폭예산 FWHM=3.53w(`eq:widthbudget`). |
| `_sections/ch1_sec10_sum.tex` L20–43 | gr_2L | `tab:staging`(4전이 초기값: ΔS=+29/0/−5/−16·Ω=6000/8000/10000/13000). |
| `_sections/ch1_sec11_lcointro.tex` L51–78 | lco_omega | `tab:lco-staging`(T1~3.90V·T2~4.05V·T3~4.17–4.20V·전자항 T1 발현). |
| `_sections/ch1_sec13_lcohys.tex` 전체 | lco_omega | `eq:lco-gxi`·`eq:lco-spinodal`·`eq:lco-dUhys`·`eq:lco-mit`·#7 대상 문구(`eq:br-vanderven1998-1`)·혼동 가드. |
| `_sections/ch1_sec15_lcoelec.tex` 전체 | lco_omega | `eq:dSe`·`eq:dSegate`(−45.7 골 깊이)·`eq:U1T2`(T² 곡률)·T_ref 동결. |
| `_sections/ch1_sec16_lcopeak.tex` 전체 | lco_omega | `eq:lco-eqpeak`(LCO 3-peak)·MSMR 동형·폭 지위. |
| `_sections/ch3v22_sec02_cases.tex` L39–52 | si_fr | `ssec:si-elemental`(순환 a-Si=고용체 경사)·c-Li₁₅Si₄ ~50mV·`tab:si-cases`. |
| `_sections/ch3v22_sec03_blend.tex` L69–133 | si_fr | `eq:blend-balance`(공통-μ 반전)·`eq:blend-dqdv`(host 합)·`ssec:si-blend-gs2`(GS-2). |
| `_sections/ch3v22_notation.tex` | si_fr | 계승 2단 규약·host 첨자·`f_Si`. |
| `_sections/common_preamble_v1024.tex` | 3개 전부 | 매크로(`\dd·\eq·\rxn·\cat·\config·\hys·\kB·\code`)·box 환경(verifybox·srcbox·keybox·signbox). |
| `results/comp_v24/GRAPHITE_STAGING_XRD.md` | gr_2L | Dahn 1991 서열·Ω>2RT⇔두-상 판정·2-sublattice Ω_a=3.4kT(Ferguson·Guo)·Persson DFT. |
| `results/comp_v24/T_SPLIT_FINDING.md` | gr_2L | 2L 엔트로피 안정화·Δ(ΔS)=29→0.30 mV/℃·재현 0.271·병합 10℃·25℃병합/45℃분리. |

배치 전제: `gr_2L.tex`→Chapter 1(흑연, `\S\ref{sec:width}` 뒤), `lco_omega.tex`→Chapter 2(LCO),
`si_fr.tex`→Chapter 3(Si). (드라이버 확인: `ch2_lco_v1.0.24.tex` 가 LCO 절들을 input.)

---

## 2. 신규 `\cite` key (본문 bibitem 미삽입 — master 가 해당 章 bib 에 추가)

계승 key(이미 章 bib 존재, 재사용): `dahn1991`·`reynier2003`·`persson2010b`(Ch1) / `vanderven1998`(Ch2) /
`chevrier_dahn2009`·`obrovac_christensen2004`·`tu_blend2024`(Ch3). — 검증 완료(해당 章 bib 에 1건씩).

**신규 5건** (서지는 시드표·finding doc 근거; ★표는 정확 서지 필드 확인 필요):

| key | 대상 bib | 서지 | tier |
|---|---|---|---|
| `schmitt2022` | ch1v22_bib | ★Schmitt 외, 흑연 \emph{탈리튬화} dV/dQ 의 stage-2L 분리(고온 분해·상온 병합). *정확 volume/page/DOI 확인 필요* — 시드표·`T_SPLIT_FINDING.md` 만 근거. | B(현상 확정)/C(서지 필드) |
| `fergusonbazant2014` | ch1v22_bib | T. R. Ferguson, M. Z. Bazant, *Electrochim. Acta* **146**, 89 (2014). [흑연 2-sublattice 정규용액 fit] | A |
| `guo2016` | ch1v22_bib | Y. Guo, R. B. Smith, M. Z. Bazant, L. E. Brus, *J. Phys. Chem. Lett.* **7**, 2151 (2016). [면내 Ω_a=3.4kT·층간 Ω_b=1.4kT] | A |
| `artrith2018` | ch3v22_bib | N. Artrith 외, *J. Chem. Phys.* **148**, 241711 (2018). [ML 퍼텐셜 a-Li_xSi 연속 상도] | A |
| `verbrugge2017` | ch3v22_bib | M. W. Verbrugge 외, *J. Electrochem. Soc.* **164**, E3243 (2017). [ω-형 정규용액 MSMR 커널, Li-Si] | A |

주의: `schmitt2022` 는 finding doc 이 저자 성·연도·주제만 주고 권/쪽/DOI 를 안 줬다 → **서지 필드 확정은
master 검증 대상**. 본문은 이 key 로 ``현상(탈리튬 2L 분리)''만 인용했고 정량 앵커는 Dahn(0.30 mV/℃)이 준다.

---

## 3. 소절별 유도 골자 (엄밀성 강조 반영)

- **gr_2L**: (A) 정규용액 μ(θ)=μ°+RT ln[θ/(1−θ)]+Ω(1−2θ) → dμ/dθ=RT/[θ(1−θ)]−2Ω → **dμ/dθ|½=4RT−2Ω**
  (`eq:gr2l-judge`, boxed). Ω>2RT⇔비단조 μ⇔miscibility gap⇔near-delta; Ω<2RT⇔단조⇔고용체 broad; Ω=2RT
  발산. XRD 결선(고정 d-spacing 2개 vs 연속 이동). 2-sublattice 축약 srcbox. (B) 2L=엔트로피 안정화 상
  → ∂U/∂T=ΔS/F(`eq:gr2l-dUdT`) → 분리율 d(ΔU_split)/dT=Δ(ΔS)/F=29/F=**0.30 mV/K**(`eq:gr2l-tsplit`, boxed),
  병합 T*≈10℃, 분해⇔ΔU_split>3.53w. 열broadening 반증(부호 반대). keybox: 두-상4+고용체1=5, 6+ 폐기.
- **si_fr**: (B) V(θ)=U°−(RT/F)ln[θ/(1−θ)]−(Ω/F)(1−2θ)=`eq:Veq`의 점유좌표 표기 → dV/dθ=−(1/F)[RT/{θ(1−θ)}−2Ω]
  → 연쇄율 → **dQ/dV=Q·F/|RT/{θ(1−θ)}−2Ω|**(`eq:sifr-kernel`, boxed). 세 극한(Ω→2RT 발산·Ω=0 `eq:eqpeak`
  회수·Ω<0 broaden), w_eff=(RT/F)(1−Ω/2RT). (A) 단일상 판정 폭/(RT/F)=[1.45,2.74,1.09]≳1. (C) 소수 gallery
  이산화·유일 두-상 c-Li₁₅Si₄(첫 리튬화). (D) 블렌드 가산 중첩=`eq:blend-balance` 공통-μ, `tu_blend2024`.
- **lco_omega**: (A) per-peak 정규용액 커널(`eq:lcoom-kernel`, boxed)=`eq:lco-eqpeak`의 Ω^cat-확장, dual-status
  (`eq:lcoom-dual`, 같은 판정자 `eq:gr2l-judge`). (B) **#7 정정**: Ω^cat=진행좌표 유효 평균장 축약(미시 질서
  아님)·config ΔS 별도 슬롯(`eq:lcoom-guard`, boxed). (C) **전자항 토글**: T_ref 동결→ΔH 흡수→커브 불변,
  ∂U/∂T만 ΔS_e/F·U-이동∝T²(`eq:lcoom-utref`); `include_electronic_entropy` 기본 OFF(`eq:lcoom-toggle`, boxed).

---

## 4. 가정 (4-tier 명시)

1. **[확정]** 판정자 dμ/dθ|½=4RT−2Ω 와 Frumkin 커널 dQ/dV=Q·F/|RT/{θ(1−θ)}−2Ω| 는 정규용액 μ(`eq:mu`)에서
   대수적으로 유도되는 항등 결과. Ω=0 회수는 `eq:eqpeak`/`eq:lco-eqpeak` 와 bit-exact.
2. **[확정]** ∂U/∂T=ΔS_rxn/F(`eq:Uj`)와 분리율=Δ(ΔS)/F 는 열역학 항등. Δ(ΔS)에만 의존(절대 분배는 T* 앵커).
3. **[근거: 시드]** 흑연 2L 분리쌍 ΔS=+15/−14(Δ=29): 시드표 §2·`T_SPLIT_FINDING`. a-Si 폭/(RT/F)=[1.45,2.74,1.09]:
   `regsol_si.png`(tier B). LCO ΔS_e=−45.7: `eq:dSegate` 골 깊이(sec15 검산값).
4. **[추정/내부]** LCO plain MSMR R²=0.944≈흑연 0.940·per-peak Ω +1.25%p·@5 +1.90%p: 내부 ablation
   (`lco_ablation_result.json`), tier B — `\cite` 아닌 내부 산출로 인용(기존 절 관행과 동일).
5. **[미검증]** `schmitt2022` 정확 서지 필드(권/쪽/DOI) — master 확인 필요.

---

## 5. 정직한 공백·불확실점 (반드시 master 확인)

1. **tab:staging 2L-pair ΔS 갱신 필요(gr_2L).** 현행 `tab:staging` 은 3→2L=**0**, 2L→2=**−5**(Δ=5→0.05 mV/K,
   전 온도 병합)라 stage-2L 온도 분리를 못 보인다. gr_2L 은 물리(Δ(ΔS)≈29→0.30 mV/K)만 확정했고 **표를 편집하지
   않았다**(경계 준수). 실제 분리 재현은 이 두 ΔS 를 분리쌍 시드(+15/−14 또는 +14.5/−14.5@T*=10℃)로 갱신해야
   하며 → **R2/master 소관**. 소절 verifybox 에 이 사실을 명시했다.
2. **LCO feature 라벨 매핑(lco_omega).** 브리프 §3 은 ``3.70V(O2)/3.90V(O3) 두-상 sharp''로 적었으나, 확정
   문건(`tab:lco-staging`)의 앵커는 T1(~3.90V MIT)·T2(~4.05V)·T3(~4.17–4.20V)다. 미검증 전위값/상 라벨 도입을
   피하려 **보수적으로 문건의 T1/T2/T3 앵커에 매핑**하고, per-peak Ω 판정(sharp Ω>2RT / broad Ω<2RT)은
   feature-일반으로 서술했다. O2/O3 대 T-라벨 정합은 master 판단 대상.
3. **#7 정정의 적용 범위(lco_omega).** 물리 유지·문구만. 나는 **신규 소절에서 정정된 읽기를 권위 있게 제시**했고
   기존 `ch1_sec13_lcohys.tex`의 `eq:br-vanderven1998-1` 문구를 **직접 편집하지 않았다**(경계). sec13 원문구도
   함께 패치할지는 master 결정(권장: `eq:lcoom-guard` 로 계승 표시).
4. **cross-chapter 참조 의존성.** `eq:gr2l-judge`·`\S\ref{ssec:gr-stage2l}`(Ch1 정의)를 si_fr(Ch3)·lco_omega(Ch2)
   에서 참조했다. 이는 기존 Si/LCO 절이 이미 Ch1 라벨(`eq:mu` 등)을 `xr-hyper externaldocument` 로 참조하는
   것과 같은 경로이며, **gr_2L 이 Ch1 에 배치되고 章 간 external 참조가 유지**되면 해석된다(전 라벨 union 대조서
   MISSING 0 확인). 배치가 바뀌면 이 두 참조만 조정 필요.
5. **Ω_Si·gallery 수(si_fr).** Ω_Si 는 고정값이 아니라 넓은 고용체 쪽 범위 시드(δ-캡 바닥 ~0.2RT). gallery
   절대 수·Ω_Si 값은 데이터 피팅 위임(tier C)으로 명시.
6. **figure 미작성.** 새 TikZ 그림은 저작하지 않았다(이론 유도 범위·좌표 오류 위험). 기존 그림·식(`fig:UjT`·
   `eq:widthbudget` FWHM 등)을 참조로만 활용. 필요 시 figure 는 별도 요청.

---

## 6. 규율 자기점검 (기각 항목 대조)

- [x] 시드값 임의 변경 X (Δ(ΔS)=29·−45.7·[1.45,2.74,1.09]·R²=0.944 모두 원천 그대로).
- [x] 기존 라벨·기호·식 재정의 X (신규 라벨만: ssec:*·eq:gr2l-*·eq:sifr-*·eq:lcoom-*; 전 ref MISSING 0).
- [x] 물리 골격 불변 (전하보존 중심식·V_n 구분·MSMR 동형 유지; Ω=0서 `eq:eqpeak`/`eq:lco-eqpeak` 회수).
- [x] boxed 최종식 ≥1 (gr_2L:2·si_fr:1·lco_omega:3), 식마다 라벨, 신규 bibitem 본문 삽입 X(NOTES 명기).
- [x] 한글 교과서 register·전제부터 전개·(a)(b)(c)(d) 구조·verifybox·srcbox·keybox.
- [x] 환경 balance·brace·`\code{}` underscore escape 검증 통과.
