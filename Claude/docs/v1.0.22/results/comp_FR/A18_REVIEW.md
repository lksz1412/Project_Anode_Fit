# A18_REVIEW — v1.0.22 심층 검토 FR-A18 (신 Ch2 §2.2 lcocenter + §2.3 lcohys)

- 대상: `Claude/docs/v1.0.22/_sections/ch1_sec12_lcocenter.tex`(§2.2 LCO 평형 중심·Kirchhoff, 112행) + `ch1_sec13_lcohys.tex`(§2.3 LCO order–disorder·MIT 2상역, 219행)
- ★명칭 주의: 파일명 `ch1_sec12~13` 은 역사적 명칭 — 실제 소속은 **ch2_lco_v1.0.22.tex 빌드(Ch2 LCO)**, xr 로 Ch1(흑연) 라벨 참조.
- 검토 창: FR-A18 (BRIEF_FR_A.md 규율 준수 — 보고 전용·소스 수정 금지·git 조작 금지·`Codex/` 접근 금지)
- 검토 4관점: ①내용 보완(빡세게) ②논리 오류(재계산·재유도 검증) ③더 쉬운 설명 ④산문→수식 간결화
- 검증 방법: 참조 라벨 전수 역추적(흑연 xr 수신식·같은 빌드 내 LCO 절 원문 대조) · 전 수식 재유도/재계산(무발견 축에 명세) · 서지는 하이쿠 서브에이전트 DOI 실검증(§서치)
- 상태: 진행 중 (조기 저장 — 발견 1건 검증 완료 시마다 즉시 append)

---

## 0. 발견 색인 (등급순 — 상세는 §1, 현행 축자·제안 LaTeX 는 상세 블록에)

| ID | 파일:행 | 유형 | 등급 | 요지 |
|---|---|---|---|---|
| A18-M1 | ch1_sec13_lcohys.tex:28–31 | 논리(과대·압축 왜곡) | M | two-phase calibration — (i) "피팅 후 유지하는 것은 두 개 뿐" = 피팅 결과 선취(흑연 §5·§7 은 "초기값 넷 다 문턱 위 + 두-상 지목 근거 = 실측 상평형" 으로 한정), (ii) dilute→stage4 영역(전이 아님·Ω 슬롯 없음)이 "Ω_j<2RT 로 피팅되는" 주어에 포함, (iii) L-접미 명명("4L→3L·3L→2L")과 표 행("4→3·3→2L") 대응 gloss 부재 |
| A18-M2 | ch1_sec13_lcohys.tex:215–217 | 논리(내적 일관) | M | "pure-LCO Ω_j^cat 가 **초기값**" ↔ 같은 절 §2.3.1(35–37행) "수치 열 없음·**초기값 미배정**·미배정 시 Ω=0" — 초기값 지위 충돌(수치 초기값 없음 vs 개념적 출발점) |
| A18-M3 | ch1_sec13_lcohys.tex:202–204 | 보완 | M | 도핑 억제 주장(절의 중심 물리) 무인용 + "전자항을 보존" 단순화 — Mg²⁺ 는 전하 보상 정공을 미리 심는 기작이라 §2.5 게이트 "(도핑 시 소폭 조정)" 과 정합 필요. 검증 후보: Tukamoto–West 1997·Ceder 1998(§서치 S-C) |
| A18-M4 | ch1_sec12_lcocenter.tex:68–73 | 수식화 | M | Kirchhoff 상쇄를 산문 괄호로만 서술 — 잉여항 T∂_TΔS 가 ΔH 드리프트(−ΔC_p)와 정확 상쇄됨을 한 줄 display 로 (신규 라벨 제안) |
| A18-M5 | ch1_sec12_lcocenter.tex:99–109 | 설명/수식화 | M | verifybox ★부호 공존 문단(11행 산문) — 층위(기저/전자항/총합) 표 1개로 보강하면 기계적으로 읽힘 |
| A18-M6 | ch1_sec13_lcohys.tex:166–175 | 수식화 | M | ★Ω vs config ΔS 혼동 가드(10행 산문) — 단위·슬롯·지위 대비 표 보강 |
| A18-M7 | ch1_sec13_lcohys.tex:188–191 | 보완/설명 | M | T1 Ω_1^cat 의 '유효 축약' 지위 문장 부재 — T2/T3 는 "유효 인력" 프레임 명시(112–113행)인데 T1 은 "구조적 2상역" 라벨만 있어 '기원=격자' 오독 여지 |
| A18-M8 | ch1_sec13_lcohys.tex:167–171 | 보완(서치 통합) | M | 0.47/1.49 원전 — 독립 Crossref/웹 서치(하이쿠, 2026-07-18)도 **NOT FOUND**: tier C 유지 지지 + NaxCoO₂ 오귀속 가설·kim_entropymetry2020 전문 확인 리드 |
| A18-L1 | ch1_sec12_lcocenter.tex:78–79 | 설명(포인터) | L | eq:U1T2 소절 포인터 — "\S\ref{sec:lco-Se}" 이나 실제 위치는 sec:lco-Se-units(§2.5.3) |
| A18-L2 | ch1_sec12_lcocenter.tex:102–103 | 설명(포인터) | L | "−46 vs 1.1 k_B 별개 척도" 포인터 "\S\ref{sec:lco-gate}" — '세 양의 구분' 실제 위치는 sec:lco-Se-scale(§2.5.5) |
| A18-L3 | ch1_sec13_lcohys.tex:58–63 | 수식화(반 줄) | L | eq:lco-Veq — 흑연 eq:Veq 는 s 명시 유지인데 대입형에서 s=+1 이 암묵 소멸(§1 규약 "boxed 식에서 s=1 대입 소멸" 과 정합하도록 반 줄 명시) |
| A18-L4 | ch1_sec13_lcohys.tex:211–212 | 문체 | L | 도핑 극한 문맥의 "T_{c,j}=Ω_j^cat/2R" — 도핑 후 임계온도는 Ω^cat,dop 기준임(또는 일반 정의임) 명시 |
| A18-L5 | ch1_sec13_lcohys.tex:10–12 | 설명 | L | "유일한 가정" — 평균장(Bragg–Williams) 축약은 흑연과 공유하는 모델 형이라 전이 시 새 가정이 아님을 반 줄 한정 |
| A18-L6 | ch1_sec12_lcocenter.tex:79–82 | 설명 | L | "config 는 실제로 엄밀하나" — 정규용액(평균장) 틀 안의 엄밀임 한정 + vib 잔여 곡률의 별도 모델링(Part T Einstein 절, 로그 곡률) xr 부재 |
| A18-L7 | ch1_sec13_lcohys.tex:146–153 | 문체 | L | srcbox 다리식의 "Ω>2RT ⟺ 질서상 안정" — 유도된 동치로 오독 여지, 대응 화살표로 완화 |
| A18-L8 | ch1_sec13_lcohys.tex:212–214 | 설명 | L | "풀린 몫은 §broadening 의 broadening 폭이 더 크게 담는다" — Ω≤2RT 로 닫힌 전이의 폭은 §5 이중지위의 '평형 예측' 쪽으로 복귀, 실측 초과 smear 는 §7 앙상블 몫 — 두 지위 분리 |
| A18-L9 | ch1_sec12_lcocenter.tex:89–91 | 보완 | L | verifybox 스케일 앵커 단일 출처(tier B) — 이미 V1 등재된 kim_entropymetry2020(x-분해 entropymetry)을 반 줄 병기해 '대표 스케일' 지위 보강 |

무발견(검토했으나 문제 없음) 축은 §2 검증 로그, 서치 결과는 §서치, 말미 4-tier 는 §4.

---

## 서치 절 (하이쿠 서브에이전트 위임 — DOI 실검증분만)

### S-V. 본문 인용 7키 DOI 검증 (하이쿠 서브 #1, Crossref API 실조회 — 2026-07-18)

| key | DOI | Crossref 조회 결과 | 판정 |
|---|---|---|---|
| reimers1992 | 10.1149/1.2221184 | "Electrochemical and In Situ X-Ray Diffraction Studies of Lithium Intercalation in LixCoO2", JES **139**, 2091–2097 (1992), Reimers & Dahn | **MATCH** (전 필드) |
| vanderven1998 | 10.1103/PhysRevB.58.2975 | "First-principles investigation of phase stability in LixCoO2", PRB **58**, 2975–2987 (1998), 저자 5인 일치 | **MATCH** (전 필드) |
| marianetti2004 | 10.1038/nmat1178 | "A first-order Mott transition in LixCoO2", Nat. Mater. **3**, 627–631 (2004), 저자 3인 일치 | **MATCH** (전 필드) |
| motohashi2009 | 10.1103/PhysRevB.80.165114 | "Electronic phase diagram of the layered cobalt oxide system LixCoO2 (0.0≤x≤1.0)", PRB **80**, 165114 (2009), 저자 8인 일치 | **MATCH** (전 필드) |
| reynier2004 | 10.1103/PhysRevB.70.174304 | "Entropy of Li intercalation in LixCoO2", PRB **70**, 174304 (2004), 저자 6인 일치 | **MATCH** (전 필드) |
| swiderska2019 | 10.1039/c8cp06638h | "Temperature coefficients of Li-ion battery single electrode potentials and related entropy changes – revisited", PCCP **21**, 2115–2120 (2019), 저자 3인 일치 | **MATCH** (비고: 전체 쪽범위 2115–2120 — bib 는 시작쪽 2115 만 표기, 관행상 무해) |
| ml2024 | 10.1016/j.jmps.2024.105726 | "Bridging scales with Machine Learning: … order–disorder transitions in LixCoO2", JMPS **190**, 105726 (2024), 저자 8인 일치 | **MATCH** (전 필드) |

- ch2 bib 의 reynier2004 부기 "[동 그룹: *J. Electrochem. Soc.* **151**, A422 (2004)]" 도 실재 확인: DOI 10.1149/1.1646152, "Thermodynamics of Lithium Intercalation into **Graphites and Disordered Carbons**", JES 151(3) A422 (2004). **주의**: 이 동반 논문은 흑연/무질서 탄소 쪽이다(LCO 아님) — bib 부기는 "동 그룹" 사실 표기라 무해하나, LCO 수치 앵커로 오독하지 말 것.
- §2.2·§2.3 이 인용하는 7키 전건 서지 무결 — **서지 축 무발견**.

---

## 1. 발견 상세 (현행 = 원문 축자 복사, 행번호는 소스 파일 기준)

### A18-M1 — two-phase calibration 압축문의 피팅 결과 선취·비전이 영역 포함·명명 gloss 부재
- 파일:행: `ch1_sec13_lcohys.tex:28–31` | 유형: 논리(과대/압축 왜곡) | 등급: **M**
- 현행(축자):
```latex
흑연에서 spinodal 문턱 $\Omega_j>2RT$($2RT\approx4958$ J/mol@298.15 K, 식~\eqref{eq:spinodal})를 피팅 후
유지하는 것은 네 staging 전이 중 $2\mathrm L\!\to\!2$(LiC$_{12}$)$\cdot$$2\!\to\!1$(LiC$_6$) \emph{두 개}
뿐이고 dilute$\to$stage4 영역과 $4\mathrm L\!\to\!3\mathrm L\cdot3\mathrm L\!\to\!2\mathrm L$ 두 전이는 $\Omega_j<2RT$ 의
solid-solution 쪽으로 피팅되는(\S\ref{sec:width}$\cdot$\S\ref{sec:broadening}) 반면, LCO 는 pure-LCO
```
- 제안(완성 LaTeX — 대체; 기존 주장·참조 전부 보존 + 한정·gloss 추가):
```latex
흑연에서 spinodal 문턱 $\Omega_j>2RT$($2RT\approx4958$ J/mol@298.15 K, 식~\eqref{eq:spinodal})를 피팅 후
유지할 것으로 지목되는 것은 네 staging 전이 중 $2\mathrm L\!\to\!2$(LiC$_{12}$)$\cdot$$2\!\to\!1$(LiC$_6$)
\emph{두 개} 뿐이고 --- 초기값 $\Omega_j$ 로는 네 전이 모두 문턱 위이나 그 두-상 지목의 실제 근거는 실측
plateau$\cdot$staging 상평형이다(\S\ref{sec:broadening-class}) ---, dilute$\to$stage4 영역($\Omega$ 슬롯이
없는 연속 등온선 --- 전이 아님)과 $4\mathrm L\!\to\!3\mathrm L\cdot3\mathrm L\!\to\!2\mathrm L$ 두 전이(표~\ref{tab:staging}
의 $4\!\to\!3\cdot3\!\to\!2\mathrm L$ 행 --- L 접미는 \S\ref{sec:broadening-class} 의 문헌 명명)는 $\Omega_j<2RT$ 의
solid-solution 쪽으로 피팅될 것이 기대되는(\S\ref{sec:width}$\cdot$\S\ref{sec:broadening}) 반면, LCO 는 pure-LCO
```
- 근거: (1) 흑연 §5(`ch1_sec05_width.tex:310–314`)는 "네 전이는 초기값 Ω_j 가 모두 2RT 보다 커 출발점에선 전부 두-상 쪽 … 피팅 후 어느 전이가 어느 지위인지는 그 전이의 Ω_j 값이 가른다"며 **전이 실명 지목을 §7 로 위임**하고, §7(`ch1_sec07_broadening.tex:23–26`)은 "이 두-부류 분류를 Ω>2RT 문턱 자체가 가르는 것은 아니다 --- 초기값 Ω_j 로는 네 전이가 모두 문턱을 넘으므로, 두 전이만 두-상 plateau 로 지목하는 **실제 근거는 실측 plateau·staging 상도표의 상평형**"이라 명시 — 현행 압축문 "피팅 후 유지하는 것은 … 두 개 뿐이고 … 피팅되는"은 아직 일어나지 않은 피팅의 결과를 확정 서술(P5 "완료로 보고 X"·4-tier 확정/추정 구분 위반 소지). (2) dilute→stage4 는 표~tab:staging 의 4개 행에 없음(전이 인덱스 밖·Ω_j 부존재 — `ch1_sec01_n0n1.tex:24` N_p≈3–4, `ch1_sec10_sum.tex:32–43` 4행) — "Ω_j<2RT 로 피팅되는" 주어에 넣을 수 없음. (3) "4L→3L·3L→2L" 는 §7(15–16행)이 "(각각 표~tab:staging 의 4→3·3→2L 행)" gloss 로 동치 선언한 문헌 명명 — Ch2 독자가 표와 직접 대조할 수 있게 같은 gloss 반복이 안전(P3-7 명칭 혼동 가드).

### A18-M2 — "pure-LCO Ω_j^cat 가 초기값" ↔ 같은 절 "초기값 미배정" 충돌
- 파일:행: `ch1_sec13_lcohys.tex:215–217` | 유형: 논리(내적 일관) | 등급: **M**
- 현행(축자):
```latex
같은 전이 파라미터 집합의 $U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로} 들어가며, $\Omega_j^\mathrm{cat}$ 하나가
gap$\cdot$smear 와 중심 이동을 동시에 만든다고 쓰지 않는다(흑연의 네 staging 전이 초기값이 그러했듯,
pure-LCO $\Omega_j^\mathrm{cat}$ 가 초기값이고 폭$\cdot$shift 는 우리 데이터로 피팅).
```
- 제안(완성 LaTeX — 대체; 괄호 정밀화):
```latex
같은 전이 파라미터 집합의 $U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로} 들어가며, $\Omega_j^\mathrm{cat}$ 하나가
gap$\cdot$smear 와 중심 이동을 동시에 만든다고 쓰지 않는다(흑연 네 전이가 표~\ref{tab:staging} 의 \emph{수치}
초기값에서 출발했던 것과 달리 LCO $\Omega_j^\mathrm{cat}$ 는 수치 초기값 미배정이므로(\S\ref{sec:lco-hys-gxi}),
pure-LCO 상도표 물리는 피팅 배정 시의 \emph{개념적 출발점}이고 폭$\cdot$shift 는 우리 데이터로 피팅).
```
- 근거: 같은 절 §2.3.1(35–37행)이 "표~tab:lco-staging 는 LCO Ω_j^cat 의 수치 열을 싣지 않으며(흑연 표와 달리 **초기값 미배정**), 미배정 시 Ω=0" 으로 선언(코드도 `Anode_Fit_v1.0.22.py:436` `transition.get('Omega', 0.0)` 로 일치 확인). Part 0(`ch1_sec02b_part0.tex:29–30`)도 "Chapter 2 의 Ω_j^cat(표 밖 --- **피팅 배정 전제**)". 현행 괄호는 흑연(수치 초기값 존재)과의 유비로 "Ω_j^cat 가 초기값"이라 적어 §2.3.1 과 정면 충돌 — '개념적 출발점'(상분리 후보 지위) vs '수치 초기값'(미배정)의 층위를 가르면 해소.

### A18-M3 — 도핑 억제 주장 무인용 + "전자항을 보존" 단순화
- 파일:행: `ch1_sec13_lcohys.tex:202–204` | 유형: 보완 | 등급: **M**
- 현행(축자):
```latex
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox$\cdot$전자항을 보존하되 order--disorder$\cdot$MIT 상전이를
억제한다 --- 정규용액 틀에서 이는 pure-LCO 상도표 물리\cite{reimers1992,vanderven1998} 의 $\Omega_j^\mathrm{cat,pure}$ 를 도핑 피팅값
$\Omega_j^\mathrm{cat,dop}$ 로 낮추는 입력 변화다.
```
- 제안(완성 LaTeX — 대체 + 보강; 신규 키는 제안 표기 — V1 원장 [검증→등재→인용] 절차 전제, §서치 S-C 검증분):
```latex
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox 와 전자항 \emph{슬롯}을 보존하되(게이트 파라미터
$g_{\max}\cdot x_\mathrm{MIT}\cdot\Delta x_\mathrm{MIT}$ 는 도핑 시 소폭 조정 여지 --- \S\ref{sec:lco-gate}(i);
특히 Mg$^{2+}$ 치환은 전하 보상 정공을 $x{=}1$ 에서 미리 심는 기작\cite{tukamoto1997}이라 절연 끝점 쪽
게이트가 움직일 수 있다) order--disorder$\cdot$MIT 상전이를 억제한다\cite{tukamoto1997,ceder1998} ---
정규용액 틀에서 이는 pure-LCO 상도표 물리\cite{reimers1992,vanderven1998} 의 $\Omega_j^\mathrm{cat,pure}$ 를 도핑 피팅값
$\Omega_j^\mathrm{cat,dop}$ 로 낮추는 입력 변화다.
```
- 근거: (1) 이 절 제목이 "(우리 시료; 갭 G3)" — G3(도핑 shift)는 §2.4(128–131행)가 "1차 문헌 공백"으로 선언한 갭이라, 억제 **현상 자체**의 1차 앵커와 **정밀값 부재**를 갈라 적을 때 가장 단단해짐(현상 앵커는 존재: Mg 정공 도핑 = Tukamoto–West JES 144, 3164 (1997), DOI 10.1149/1.1837976 [Crossref 검증]; Al 치환 제일원리 = Ceder 등 Nature 392, 694 (1998), DOI 10.1038/33647 [Crossref 검증] — §서치 S-C). (2) "전자항을 보존"은 §2.5 게이트 (i) "(초기값으로 고정, **도핑 시 소폭 조정**)"(`ch1_sec15_lcoelec.tex:271`)과 긴장 — 슬롯 보존(항이 남음)과 파라미터 불변(값 유지)을 가르면 정합. Mg²⁺→Co³⁺ 치환의 전하 보상이 정공을 만드는 것은 Tukamoto–West 의 전도도 향상 기작 그 자체라, 절연 끝점( x=1 )이 이미 도핑된 시료에서 MIT 게이트 위치·발현이 움직일 수 있음은 물리적으로 예상됨 — 이 여지를 명시해야 "Ω 만 낮춘다"는 단일-슬롯 서술이 과대 주장이 안 됨. (3) 도핑 시 dQ/dV peak 소멸의 직접 실측 문헌은 하이쿠 서치에서 미확보(EXCLUDED — §서치) — 그래서 제안문도 '억제한다' 의 앵커를 기작(정공 도핑)·이론(제일원리 치환) 수준으로 한정.

### A18-M4 — Kirchhoff 상쇄의 한 줄 수식화 (산문→수식)
- 파일:행: `ch1_sec12_lcocenter.tex:68–73` | 유형: 수식화 | 등급: **M**
- 현행(축자):
```latex
\textbf{★다온도 전자항 주의 --- 기계 미분이 낳는 비물리 잉여항.} $\Delta S_{e,j}(x,T)\propto T$
인 항(전자항, \S\ref{sec:lco-electronic})을 다온도 모델에 풀 때 고정 $\Delta H$ 로 $U_j(T)=(-\Delta H+T\Delta S(T))/F$ 를 기계 미분하면 생기는
잉여항 $T\,\partial_T\Delta S$ 는 Kirchhoff 일관성 위반($\partial\Delta H/\partial T=\Delta C_p$ 이고
$T\,\partial\Delta S/\partial T=\Delta C_p$ 라 ``$\Delta H$ 고정$\wedge\partial_T\Delta S\ne0$'' 가정 자체가
성립하지 않는다)의 비물리 항이므로, 유지할 불변식은 식~\eqref{eq:lco-dUdT} 의
$\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}(T)/F$ 이고 위치는 기준온도에서
```
- 제안(완성 LaTeX — 보강; 현행 문장 유지, 직후에 display 1행 추가. 신규 라벨 제안 `eq:lco-kirchcancel`):
```latex
% (현행 문장 그대로 두고, "성립하지 않는다)의 비물리 항이므로" 뒤에 다음 display 를 삽입)
곧 $\Delta H(T)\cdot\Delta S(T)$ 를 함께 미분하면 잉여항은 $\Delta H$ 드리프트와 정확히 상쇄된다:
\begin{equation}
\frac{\partial U_j^\mathrm{cat}}{\partial T}
=\frac1F\Big[-\underbrace{\partial_T\Delta H_{\rxn,j}^\mathrm{cat}}_{=\,\Delta C_{p,j}}
+\ \Delta S_{\rxn,j}^\mathrm{cat}
+\underbrace{T\,\partial_T\Delta S_{\rxn,j}^\mathrm{cat}}_{=\,\Delta C_{p,j}}\Big]
=\frac{\Delta S_{\rxn,j}^\mathrm{cat}(T)}{F}
\label{eq:lco-kirchcancel}
\end{equation}
--- 고정-$\Delta H$ 기계 미분은 이 상쇄 짝($-\Delta C_p$ 와 $+\Delta C_p$)의 반쪽만 남긴 것이다.
```
- 근거: 재유도 확인 — U=(−ΔH(T)+TΔS(T))/F 전미분 = [−∂_TΔH+ΔS+T∂_TΔS]/F; 등압에서 ∂_TΔH=ΔC_p, T∂_TΔS=ΔC_p 라 두 항이 소거되어 정확히 ΔS(T)/F (경로 2 와 합치). 현행은 "가정이 성립하지 않는다"까지만 산문으로 말하고 **왜 불변식이 살아남는지**(상쇄)는 독자 몫 — 한 줄 display 가 잉여항의 정체(상쇄 짝의 반쪽)를 식 자체로 보여 §2.2 의 가드 의도를 완성. 기존 자산 무삭제(순수 보강).

### A18-M5 — verifybox ★부호 공존 문단의 층위 표 보강
- 파일:행: `ch1_sec12_lcocenter.tex:99–109` | 유형: 설명/수식화 | 등급: **M**
- 현행(축자):
```latex
\textbf{★전자항과의 부호 공존(오독 방지)} --- 이 $\Delta S_{\rxn}^\mathrm{cat}\!\approx\!+80$ J/(mol\,K)$>0$ 은
대표 SOC(MIT 창 \emph{밖}, 전자항 $\approx\!0$)에서 읽은 config$+$vib 기저 계수의 \emph{대표 스케일}이며,
T1 의 전자항 $\Delta S_{e,j}<0$(삽입 기준, \S\ref{sec:lco-electronic})과 모순되지 않는다 --- 전자항은 MIT 게이트의
$x$-\emph{국소 골}로, 창 중심에서 몰당 $\approx\!-46$ J/(mol\,K)(부분몰 골 \emph{깊이} --- $x$ 적분 게이트 총 방출 $\approx\!1.1\,k_B$/atom 과는 별개 척도,
\S\ref{sec:lco-gate}), 창 밖에서 $\approx\!0$ 이다. 창 중심에서 이 $-46$ 이 config$+$vib 기저에 더해질 때, \emph{기저가 대표 스케일($+80$)이면} 총합이 $\approx\!+80-46\approx\!+34>0$ 으로
양이 유지되고 창 밖에선 보정이 소멸해 $\approx\!+80$ 만 남는다. 다만 이 기저 $+80$ 은 대표 스케일(tier B)이고
전이별 기저는 $x$(SOC)-의존이라, 창 중심의 실제 기저가 작으면(예: 코드 시연의 T1 config 기여) $-46$ 이 이겨 총부호가
음이 될 수도 있다 --- 곧 창 중심 총부호의 양/음 판정 자체가 round-trip 피팅 대상이다(위 공존 논거는 ``$+80$
기저 $\ne$ 전자항 $-46$ 이 서로 다른 층위의 양''이라는 것이지, 총부호가 반드시 양이라는 주장은 아니다). 표~\ref{tab:lco-staging}
의 config 값(그리고 \S\ref{sec:lco-decomp} 의 vib 슬롯)은 \emph{전이별 부분몰} 성분, $+80$ 은 \emph{전체 계수}의 대표 스케일로 \emph{서로 다른
종류$\cdot$층위의 양}이라(\S\ref{sec:lco-decomp}) 둘의 공존은 모순이 아니다.
```
- 제안(완성 LaTeX — 보강; 산문 전체 보존, 문단 말미(verifybox 내부)에 요약 표 추가):
```latex
층위를 한 표로 요약하면:
\begin{center}\footnotesize
\begin{tabular}{@{}llll@{}}
\hline
양 & 종류(층위) & 대표값 & 유효 범위 \\
\hline
기저(config$+$vib) & \emph{전체 계수}의 대표 스케일(tier B) & $\approx+80$ J/(mol\,K) & MIT 창 밖 대표 SOC \\
전자항 $\Delta S_{e,1}^{\,\mathrm{mol}}$ & \emph{전이별 부분몰} 골 깊이 & $\approx-46$ J/(mol\,K) & MIT 창 중심(창 밖 $\approx0$) \\
총합(창 중심) & 기저가 대표 스케일일 때의 예시 & $\approx+34$ J/(mol\,K) & 실제 기저가 작으면 음일 수도 --- 피팅 대상 \\
\hline
\end{tabular}
\end{center}
```
- 근거: 문단이 한 호흡 11행 산문으로 세 층위(전체 계수 대표 스케일 / 전이별 부분몰 골 / 조건부 총합)를 오가 독자가 "+80 과 −46 을 같은 슬롯 값으로 합산해도 되는가"에서 걸림 — 수치 자체는 전건 재계산 일치(80.08·−45.7~−46.0·+34, §2 검증 로그 5번). 표는 산문의 주장을 하나도 바꾸지 않고 층위만 정렬(순수 보강·verifybox 독립성 유지).

### A18-M6 — ★Ω vs config ΔS 가드의 단위·슬롯 대비 표
- 파일:행: `ch1_sec13_lcohys.tex:166–175` | 유형: 수식화 | 등급: **M**
- 현행(축자):
```latex
\textbf{★$\Omega$ 와 config $\Delta S$ 의 구분(혼동 가드)} --- 정렬의 charge-order
엔트로피 변화($\approx0.47$ J/(mol\,K)@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$
[값 원전 재확인 중 --- 종전 귀속처는 전자$\cdot$자기 상도표 논문\cite{motohashi2009}으로 이 $\Delta S$ 값의
1차 원전이 아닌 것으로 확인되어 \emph{값도 배정도} tier C 다. 실측 질서상 조성은
$x{=}\tfrac12$$\cdot$$\tfrac56$\cite{reynier2004} 이어서 $x{=}\tfrac23$ anchor 는 조성 재배정 검토 대상이고 T2/T3
조성 창($x\approx0.55/0.48$)과의 불일치도 그대로다 --- 최종 귀속은 피팅 위임])는 표~\ref{tab:lco-staging}$\cdot$\S\ref{sec:lco-decomp} 의
$\Delta S_j^\mathrm{config}$ 슬롯($U_j^\mathrm{cat}(T)$ 의 온도 이동)에 들어가는 \emph{엔트로피}[J/(mol\,K)]이지
spinodal 문턱을 정하는 \emph{상호작용 에너지} $\Omega_j^\mathrm{cat}$[J/mol]가 \emph{아니므로},
``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 로 직접 연결하지 않고, $\Omega_j^\mathrm{cat}$ 는 gap 을 정하는
별도 피팅 파라미터로 둔다.
```
- 제안(완성 LaTeX — 보강; 가드 산문·괄호 캐비앳 전부 보존, 직후 대비 표 추가):
```latex
\begin{center}\footnotesize
\begin{tabular}{@{}lll@{}}
\hline
 & charge-order $\Delta S_j^\mathrm{config}$ & 유효 인력 $\Omega_j^\mathrm{cat}$ \\
\hline
단위(종류) & J/(mol\,K) --- 엔트로피 & J/mol --- 상호작용 에너지 \\
들어가는 슬롯 & $U_j^\mathrm{cat}(T)$ 온도 이동(식~\eqref{eq:lco-dUdT}) & spinodal gap(식~\eqref{eq:lco-dUhys}) \\
현재 지위 & tier C 초기값(원전 재확인 중) & 수치 미배정 --- 별도 피팅 파라미터 \\
상호 환산 & \multicolumn{2}{l}{없음 --- ``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 직접 연결 금지} \\
\hline
\end{tabular}
\end{center}
```
- 근거: 가드의 명제 구조가 (값 캐비앳 5행 괄호)를 문장 한가운데 안은 채 "엔트로피이지 에너지가 아니므로 연결하지 않는다"로 이어져, 정작 기계적으로 지켜야 할 두 슬롯 대응이 산문에 묻힘. 표는 단위·슬롯·지위·환산금지 네 축을 분리 명시(P3-3 의 의존 관계 표 표시 취지와 동형). 기존 자산 무삭제.

### A18-M7 — T1 Ω_1^cat 의 '유효 축약' 지위 한 문장
- 파일:행: `ch1_sec13_lcohys.tex:188–191` | 유형: 보완/설명 | 등급: **M**
- 현행(축자):
```latex
MIT 고유의 전자 자유도는 이 히스 gap 에 새 항으로 섞지 않는다 --- 그 항은 이미
$\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^\mathrm{mol}(x,T)$(\S\ref{sec:lco-decomp} 의 분해식)를 통해 $U_1^\mathrm{cat}(T)$ 의 온도 이동
(식~\eqref{eq:lco-dUdT})에 들어가, 두 몫이 서로 다른 슬롯에 존재한다:
```
- 제안(완성 LaTeX — 보강; 현행 문장 앞에 한 문장 삽입):
```latex
$\Omega_1^\mathrm{cat}$ 역시 T2$\cdot$T3 와 같은 지위의 \emph{유효} 쌍상호작용이다 --- 1차 MIT 의
자유에너지 비볼록성을 미시적으로 만드는 것은 전자(불순물 Mott)$\cdot$격자 결합(\S\ref{sec:lco-why})이고
그 전부를 진행률 좌표의 $\Omega_1^\mathrm{cat}$ 하나로 접으며, ``구조적''은 회절로 실측되는 2상
공존\cite{reimers1992} 을 가리키는 라벨이지 기원이 격자만이라는 주장이 아니다.
MIT 고유의 전자 자유도는 이 히스 gap 에 새 항으로 섞지 않는다 --- (이하 현행 그대로)
```
- 근거: T2/T3 는 112–113행에서 "유효 인력 … (미시 기원은 Li·빈자리의 정렬 상호작용이고, 이중웰을 만드는 것은 이 유효 좌표의 볼록성 상실이다)"로 유효-축약 지위를 명시하는데, T1 은 "이 구조적 2상 공존도 같은 정규용액 문턱을 받아"(181행)와 eq:lco-mit 의 "(구조적 2상역) ⇐ Ω_1^cat" 라벨만 있어, sec15 가 세운 MIT 미시 기작(전자 기원)과 나란히 읽는 독자가 "gap 은 격자 기원, 전자는 온도 이동 기원"으로 **기원 층위**를 오독할 수 있음. 슬롯 분리(이중계산 가드)는 파라미터 층위 주장임을 한 문장으로 고정 — eq:lco-mit 의 가드 의도(199행 "이중계산하지 않는 경계")를 훼손하지 않고 보강.

### A18-M8 — 0.47/1.49 원전: 독립 서치도 NOT FOUND (tier C 유지 지지 + 리드 2건)
- 파일:행: `ch1_sec13_lcohys.tex:167–171` (같은 값: `ch1_sec11_lcointro.tex:72–73`·`ch1_sec14_lcodecomp.tex:137`) | 유형: 보완(서치 통합) | 등급: **M**
- 현행(축자 — 괄호 캐비앳 부분):
```latex
[값 원전 재확인 중 --- 종전 귀속처는 전자$\cdot$자기 상도표 논문\cite{motohashi2009}으로 이 $\Delta S$ 값의
1차 원전이 아닌 것으로 확인되어 \emph{값도 배정도} tier C 다. 실측 질서상 조성은
$x{=}\tfrac12$$\cdot$$\tfrac56$\cite{reynier2004} 이어서 $x{=}\tfrac23$ anchor 는 조성 재배정 검토 대상이고 T2/T3
조성 창($x\approx0.55/0.48$)과의 불일치도 그대로다 --- 최종 귀속은 피팅 위임])는
```
- 제안(완성 LaTeX — 선택적 보강; 캐비앳 괄호 안 "1차 원전이 아닌 것으로 확인되어 \emph{값도 배정도} tier C 다." 문장 뒤에 삽입):
```latex
독립 서지 스윕(Crossref$\cdot$웹, 2026-07)에서도 이 두 수치의 1차 원전은 나오지 않았다 ---
Na$_x$CoO$_2$ 질서 문헌 유래(오귀속) 가능성과 entropymetry 실측\cite{kim_entropymetry2020} 전문
대조가 남은 추적 경로다.
```
- 근거: 하이쿠 서브 S4 서치(§서치) 결과 — LixCoO2 의 x=1/2·2/3 질서 엔트로피 0.47/1.49 J/(mol K) 수치의 1차 원전은 Crossref·웹에서 **미발견**(정직 NOT FOUND; 검토 후보 Kawaji 2002 저온 열용량은 x=1 조성이라 부적합 판정). 이는 본문 tier C 판정·"원전 재확인 중" 스탠스를 **독립적으로 지지**하는 부정 결과이므로 캐비앗에 반영할 가치가 있음(선택 — 반영 없이 현상 유지도 정합). kim_entropymetry2020 은 V1 원장 기등재 키(정량 ΔS 는 "전문 미접근 — 수치 미확보"로 원장에 기록)라 인용 규율 위반 없음.
