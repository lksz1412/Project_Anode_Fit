# V1.0.14 P4.1 R3 검수 — 검수자 A (용어 일관성 렌즈)

- 대상: `Claude/docs/v1.0.14/graphite_ica_ch1_v1.0.14.tex`(3229줄, 전문 정독) · `graphite_ica_ch2_v1.0.14.tex`(783줄, 전문 정독) · `appendix_phase_separation.tex`(482줄, 전문 정독)
- 렌즈: 용어 일관성 — ① 동일 개념·이표기 ② 영어 두문자어 첫 출현 원어 병기 ③ 파일 내 기호 충돌 ④ 세 파일 간 용어·기호 어긋남
- 방법: 전문 통독 1회 + 후속 표적 grep 교차검증(청크 스킴: 절 단위 통독 → 용어별 전수 검색). 파일 수정은 하지 않음(보고서만 신규 작성).
- 표기: 심각도 CRIT/HIGH/MED/LOW. 각 항목에 원문 인용 + 줄번호.

---

## 범주 ① 같은 개념이 다른 용어로 불리는 곳

### A1-1 [HIGH] "가역 기준선" vs "평형 기준선" — |I|→0 곡선의 명명 불일치 (물리적 함의 있음)

Ch1 §sec:eqpeak(N6)는 이 절의 대상을 처음부터 끝까지 **"평형 peak"·"기준선"·"평형 기준선"**으로 부른다:

- L1386(절 제목): `\section{평형 peak — $|I|\to0$ 기준선 (N6)}`
- L1389: "이것이 전류가 없을 때($|I|\to0$)의 기준선이며"
- L1605: "$\tau\propto r^2$ 분산은 $|I|\to0$ **평형 기준선**에서 항등적으로 소멸하며"
- L2683: "(b)를 (a)에 넣으면 양극 전위 영역의 **평형 기준선**이 닫히며"

그런데 같은 §sec:eqpeak 안, L1413-1415에서 저자는 이 baseline이 분기 인자 $\gamma_j$ 에 따라 갈린다는 것을 명시적으로 밝힌다:

> "이 값이 전이별로 합산되어 배경과 함께 $|I|\to0$ 극한을 이룬다 --- 단 $\gamma_j\ne0$ 이면 이 극한은 분기 중심 $U_j^{\,d}$ 에 남는 **히스테리시스 잔존 극한**이고, 분기 없는 **가역 기준선**($U_j$ 중심)과는 $\gamma_j\to0$ 에서만 일치한다(히스테리시스는 열역학적 --- \S\ref{sec:hys})."

즉 본문 스스로 "가역 기준선"이라는 표현을 **γ_j=0(분기 없음)인 특수한 경우**에만 한정해서 쓰고 있고, 일반적인 $|I|\to0$ 곡선(γ_j≠0 포함, 즉 코드의 `equilibrium()` 메서드가 실제로 계산하는 일반형)은 "히스테리시스 잔존 극한"이라고 못박아 "가역"이 아님을 분명히 한다.

그럼에도 부록(구현 대응표, §sec:appendix-code) L3069-3070은 코드 설명에서 이 구분을 놓치고 일반형을 그냥 "가역 기준선"이라 부른다:

> "$|I|\to0$ **가역 기준선**은 메서드 \code{equilibrium}(식~\eqref{eq:eqpeak} 만 합산)이다."

`equilibrium()`(= eq:eqpeak 합산)은 인자로 주어지는 중심(U_j 또는 U_j^{,d})을 그대로 쓰는 일반 함수이며, γ_j≠0 조건에서 히스테리시스 분기를 반영한 중심을 넣으면 §sec:eqpeak L1413-1415가 스스로 "가역이 아니다"라고 규정한 바로 그 대상이 된다. 부록의 "가역 기준선"은 본문이 신중하게 구분해 둔 개념(평형=|I|→0 일반 / 가역=γ=0 특수)을 다시 뭉개는 결과다 — 구현 설명을 읽는 독자는 `equilibrium()` 이 늘 히스테리시스 없는(가역) 곡선을 낸다고 오독할 위험이 있다.

**정정 제안**: L3070의 "가역 기준선"을 본문 지배 용법인 "평형 기준선"으로 바꾸거나, "(γ_j=0 이면 가역, γ_j≠0 이면 히스테리시스 잔존 — \S\ref{sec:eqpeak})" 같은 괄호 한정을 추가.

### A1-2 [MED] "peak"(영어) / "봉우리"(한글) — 동일 dQ/dV 피크 개념의 어휘 분할

같은 대상(전이별 dQ/dV 종 모양)을 가리키는 데 Ch1은 영어 "peak"를 압도적으로 쓰고(§서론 L148-150, §sec:eqpeak 제목·본문 L1386-1422, §sec:tail L1841-1933, 표~tab:nodemap L2957-2961, 부호검산표 L2998-3052, 부록 코드표 L3070/3166), Ch2는 거의 전부 한글 "봉우리"를 쓴다(§sec:config L272·307·313·344, §ssec:overlap L467-473·497-516·555-567, §ssec:weff L571-664 등 30여 곳; "peak"는 L468 "Chapter 1 의 peak" 단 1회, 이것도 Ch1을 가리키는 상호참조).

문제는 Ch1 **내부**에서도 이 갈림이 재현된다는 점이다 — N-노드 골격(§sec:eqpeak, §sec:tail, §sec:sum, 부호검산·구현대응 부록)은 "peak"를 쓰는 반면, 같은 챕터의 broadening 절(§sec:broadening, 예: L1498 "좁은 봉우리", L1631-1642 keybox)과 LCO 절(§sec:lco-electronic L2522·2558·2573·2638·2640, §sec:lco-peak 제목·본문 L2648-2705, §sec:lco-decomp L2731)은 "봉우리"로 바뀐다. 동일 문서 안에서 같은 물리량(예: T1 MIT 봉우리, 흑연 staging peak)을 가리키는 표현이 절에 따라 언어가 바뀌는 것은 지배적 용법(Ch1=peak, Ch2=봉우리)과 이탈 지점(Ch1의 broadening/LCO 군집)이 뚜렷이 갈린다는 뜻이며, 특히 Ch2 L468이 "Chapter 1 의 peak"라고 상호참조할 때 그 대상이 이제 Ch1 안에서도 "봉우리"로 더 많이 불리는 절(broadening)일 수 있어 상호참조의 표면적 일관성도 흔들린다.

**정정 제안**: 문서/챕터 단위로 한 용어를 지배어로 선언(예: 코드 식별자·수식 참조가 걸린 Ch1은 "peak" 고정, 순수 서술 문장은 "봉우리" 허용하되 같은 절 안에서 혼용 금지) — 최소한 §sec:broadening·§sec:lco-electronic·§sec:lco-peak의 "봉우리"를 §sec:eqpeak·§sec:tail과 통일.

---

## 범주 ② 영어 두문자어 첫 출현 원어 병기

각 파일 독립 검사 결과, 대다수 두문자어는 규칙을 지킨다(첫 출현에 영어 원어 병기):

- Ch1: `ICA`(L133, 이미 v1.0.13 이전부터 확립), `OCV`(L258, open circuit voltage), `MSMR`(L143, multi-species, multi-reaction), `DFT`(L1982, density functional theory), `GITT`(L1472, galvanostatic intermittent titration technique), `OCP`(L1473-1474, open circuit potential — OCV와의 관계까지 명시), `PSD`(L1569, particle size distribution), `MIT`(L2032, insulator-to-metal transition), `SOC`(L1981, state of charge) — 전부 정상.
- Ch2: `MIT`(L326), `OCV`(L602), `SOC`(L78), `MSMR`(L740-741, Multi-Species, Multi-Reaction), `MCMB`(L334, mesocarbon microbead) — 전부 정상.

### A2-1 [LOW] `FWHM` 미병기 (Ch1, 유일 출현)

Ch1 L1523-1524 (§sec:broadening widthbudget 각주, 최근 폭-예산 삽입 문단):

> "logistic 미분 종~\eqref{eq:belliden} 은 규격화하면 scale $w_j$ 의 logistic 분포 그 자체라 분산이 $\pi^2w_j^2/3$, 반높이 전폭은 $\mathrm{FWHM}=2\ln(3+2\sqrt2)\,w_j\approx3.53\,w_j$ 다"

"반높이 전폭"이라는 한글 의역은 주어지지만, 문서의 다른 모든 두문자어(위 목록)가 따르는 "(영어 원어)" 괄호 병기 — 예: "GITT(galvanostatic intermittent titration technique)" — 형식은 `FWHM`에서 유일하게 빠져 있다(본 문서 전체에서 `FWHM`은 이 한 곳에만 등장). 사소하지만 문서 자신의 확립된 병기 컨벤션과 어긋난다.

**정정 제안**: "반높이 전폭(full width at half maximum, FWHM)"으로 보강.

*(refute 시도: "반높이 전폭"이 이미 의미상 충분한 번역이라 원어 병기가 불필요하다고 볼 수도 있으나, 문서 자신이 OCP·GITT 등 이미 뜻이 짐작되는 약어에도 예외 없이 원어를 병기해 온 선례가 있어 이탈로 판단 — 생존.)*

---

## 범주 ③ 한 파일 안에서 같은 기호가 다른 의미로 쓰이는 곳

### A3-1 [HIGH] `$s$` 기호 충돌 — "유도 전용 고정 부호"(항상 +1) vs "logistic scale 파라미터"

Ch1 N0 기호표 L227:

> "$s$ & --- & 유도 전용 고정 부호 — 항상 $+1$(\S\ref{sec:center}$\cdot$\S\ref{sec:hys} 의 $U_j$ 정의 관례); 방향에 따라 $\pm1$ 로 바뀌는 $\sigma_d$ 와 별개, 본론 결과-사슬 boxed 식에서 $s{=}1$ 대입돼 소멸(Part 0 의 박스는 $s$ 를 명시 유지)"

이 $s$는 문서 전역(eq:muV, eq:sm-eqcond, eq:eqcond, eq:Uj, eq:sm-nernst, eq:Veq, eq:hysdiff, eq:dUhys, eq:Ubranch 등 수십 곳)에서 반복 사용되는 핵심 기호이며, 각주 L156-158은 "$s$와 $\sigma_d$를 헷갈리면 여집합 오류가 생긴다"고 **★최우선 결함 클래스**로 지정할 만큼 민감하게 다룬다.

그런데 §sec:broadening widthbudget 각주 L1526(위 A2-1과 같은 문단, 최근 삽입 폭-예산 설명)은 같은 기호 $s$를 완전히 다른 뜻 — logistic 분포의 **scale 파라미터** — 로 재사용한다:

> "logistic scale $s$ 와는 $\sigma=\pi s/\sqrt3$ 로 환산된다"

문제는 이 문장이 나오기 바로 한 문장 전(L1523)에서 저자 스스로 이미 "scale $w_j$"라고 정확히 명명해 두었다는 점이다("규격화하면 scale $w_j$ 의 logistic 분포 그 자체라"). 즉 같은 단락 안에서 동일한 물리량(logistic 분포의 scale = $w_j$)을 한 문장 뒤에서 굳이 새 기호 $s$로 다시 부른 것이며, 그 결과 (a) 표기가 불필요하게 이중화되고 (b) 그 새 기호가 하필 문서가 ★최우선 결함 클래스로 지정한 부호 기호 $s$와 정확히 충돌한다.

**정정 제안**: 새 기호를 도입하지 말고 그냥 "$\sigma=\pi w_j/\sqrt3$"로 쓴다(이미 L1523에서 scale=$w_j$라 명명했으므로). 통계학적 관용 표기를 살리고 싶다면 $s$ 대신 $\ell$이나 $\varsigma$ 등 문서 내 미사용 기호를 쓸 것.

### A3-2 [MED] `$\sigma_\mathrm{int}$` — 정의 없이 사용된 파생 기호

같은 widthbudget 블록에서 eq:widthbudget(L1515-1522)은 "내재(logistic 분산)" 성분을 언더브레이스 라벨로만 표시한다:

> $\underbrace{\frac{\pi^2}{3}\Big(\frac{n_jRT}{F}\Big)^{\!2}}_{\text{② 내재(logistic 분산)}}$

이 항에 $\sigma_\mathrm{int}$라는 기호를 정식으로 대응시키는 문장은 어디에도 없다. 그런데 곧바로 이어지는 산문(L1527)과 그림 캡션(L1549, L1558)은 이 기호가 이미 정의된 것처럼 사용한다:

- L1527: "$\sigma_\mathrm{sym}/\sigma_\mathrm{int}=\sqrt{1+(\sigma_\eta/\sigma_\mathrm{int})^2}$"
- L1549(그림 fig:widthbudget 라벨): "$\sigma_\eta=1.25\,\sigma_\mathrm{int}$, 유효 scale $1.6\,w_j$"
- L1558: "$\sigma_\mathrm{sym}=\sqrt{1+1.25^2}\,\sigma_\mathrm{int}\approx1.6\,\sigma_\mathrm{int}$"

독자는 "② 내재" 라벨의 제곱근이 $\sigma_\mathrm{int}$라고 스스로 추론해야 한다(즉 $\sigma_\mathrm{int}\equiv\pi n_jRT/(F\sqrt3)$). 이는 문서의 다른 곳(예: 파생 B의 $\Delta S^0_j$ keybox, Ch2 L312-314)이 새 기호를 도입할 때마다 "$X\equiv Y$" 형태로 명시적으로 정의하는 관례와 어긋난다.

**정정 제안**: eq:widthbudget 직후에 "$\sigma_\mathrm{int}^2\equiv\dfrac{\pi^2}{3}\Big(\dfrac{n_jRT}{F}\Big)^2$" 한 줄을 명시적으로 추가.

### A3-3 [MED] `$\gamma$` 기호 재사용 — "분기 축소 인자"(무차원, 0–1) vs "계면 에너지"[J/m²]

Ch1 N0 기호표 L244:

> "$\gamma_j$ & --- & 분기 축소 인자 $0\le\gamma_j\le1$($0$ 이면 분기 없음)"

이 $\gamma_j$는 히스테리시스 분기 진폭을 줄이는 무차원 인자로 §sec:hys 전역(eq:Ubranch, eq:center 등)에서 쓰인다. 그런데 §sec:broadening (c)-(i) 입자 반경(PSD) 논의, L1579(eq:gibbsthomson 정의 문단)는 같은 그리스 문자를 완전히 다른 물리량에 쓴다:

> "$\Delta U(r)\;=\;\dfrac{2\gamma V_m}{F\,r}$ ($\gamma$ = 계면 에너지[J/m$^2$], $V_m$ = 삽입상 몰부피)"

이후 L1585-1601에서 "$\gamma\sim0.1$--$1$ J/m$^2$", "상한 $\gamma=1$", "$\gamma$ 의 정확값" 등으로 여러 차례 반복된다. 두 $\gamma$는 항상 아래첨자 유무(γ_j vs γ)로 구별은 가능하지만, 문서가 다른 기호 재사용(예: $g$ — Ch2 L473-474, 격자 grid vs lattice — Ch1 L918)에는 매번 "★기호 주의" 박스로 명시적 disclaimer를 붙이는 반면, 이 $\gamma$/$\gamma_j$ 쌍에는 그런 disclaimer가 없다. 같은 N7 인접 절(폭·히스테리시스·broadening)이 밀집된 구역에서 재사용되는 만큼 착오 여지가 있다.

**정정 제안**: 계면 에너지 쪽을 $\gamma_s$ 또는 $\gamma_\mathrm{int}$(단, A3-2와 충돌하므로 $\gamma_\mathrm{surf}$ 등)로 바꾸거나, 최소한 §sec:broadening (c)-(i) 첫 등장에 "(분기 인자 $\gamma_j$ 와 무관)" 한 줄을 추가.

*(대조: $g$ 기호의 4중 사용 — $g_j(\xi)$ 조성 자유에너지[Ch1]·$g(\theta)$ BW 자유에너지[Ch2]·$g_j(x)$ 봉우리 가중[Ch2]·$g(E_F)$ 상태밀도[Ch1·Ch2] — 는 Ch2 L473-474 "★기호 주의" 박스로 이미 명시적으로 해소되어 있어 별도 결함으로 세지 않음. "결정 lattice vs 작업 격자(grid)"도 Ch1 L918에서 "(수치 grid --- 결정 lattice 와 무관)"으로 이미 해소.)*

---

## 범주 ④ 세 파일 사이 용어·기호 어긋남 (ξ=θ 배향 주의 제외)

### A4-1 [MED] 혼합 자유에너지 기호 — 본문 `$g$` vs 부록 `$f$`, 대응 관계 미명시

Ch1·Ch2는 정규용액(regular solution)/격자기체 혼합 자유에너지를 항상 $g$로 명명한다 — Ch1 eq:gxi(L614-616) "$g_j(\xi)=g_j^0+RT[\ldots]+\Omega_j\xi(1-\xi)$", Ch1 eq:sm-gtheta(L600-601) "$g(\theta)=\mu^0\theta+RT[\ldots]+\Omega_j\theta(1-\theta)$", Ch2 eq:BW(L200-202) "$g(\theta)=g_0+RT[\ldots]+\Omega\theta(1-\theta)$". 세 곳 모두 상수/선형 항까지 포함한 하나의 기호 $g$ 안에 다 담는다(Ch1 L611-612: "$g_j^0$(상수와 $\xi$-직선 몫의 묶음)").

반면 부록은 같은 물리량을 **두 기호로 쪼갠다** — L104-107(eq:app-fxi):

> "몰당 혼합 자유에너지는 $\boxed{f(\xi)=RT[\xi\ln\xi+(1-\xi)\ln(1-\xi)]+\Omega\xi(1-\xi)}$ 이다. 전체 자유에너지는 순수 성분의 기준 항을 더한 $g(\xi)=(1-\xi)g_A^0+\xi g_B^0+f(\xi)$ 이지만"

즉 부록의 $g(\xi)$(선형 기준항 포함, 본문 $g_j(\xi)$와 구조상 대응)와 부록의 $f(\xi)$(선형항 제외, "섞임 몫"만)는 서로 다른 대상인데, 부록 L111은 "섞임 몫" $f(\xi)$ 쪽을 "본문의 자유에너지와 동일"이라고 진술한다:

> "식~\eqref{eq:app-fxi} 는 본문 Part 0 의 자유에너지와 동일하며"

그러나 본문 $g_j(\xi)$는 (L611-612에 따라) 상수+선형 묶음 $g_j^0$를 **이미 포함**하고 있어, 엄밀히는 부록의 총합 $g(\xi)=(1-\xi)g_A^0+\xi g_B^0+f(\xi)$ 쪽이 본문 $g_j(\xi)$에 대응하고, 부록의 "섞임 몫" $f(\xi)$는 본문 $g_j(\xi)$에서 $g_j^0$를 뺀 것에 해당한다(2계 미분 등 안정성 판정에는 차이가 없다는 부록 자신의 논증(L108-110)은 맞지만, "동일"이라는 서술은 부정확). 부록의 ξ=θ 배향 주의처럼 "본문의 $g$ ↔ 본 부록의 $f$(선형항 제외)"라는 명시적 대응 문장이 없어, 세 파일을 오가는 독자가 두 기호를 바로 등치할 위험이 있다.

**정정 제안**: 부록 L111 근처에 "본문 $g_j(\xi)$는 상수$\cdot$선형 몫 $g_j^0$까지 포함하므로, 본 부록의 $f(\xi)$는 본문 $g_j(\xi)-g_j^0$(섞임$\cdot$상호작용 몫만)에 대응한다" 식의 한 줄을 추가.

### A4-2 [정보/이미 해소 — 결함 아님] 확인 목록

아래는 세 파일 간 잠재적 어긋남으로 보였으나 본문 자체가 이미 명시적으로 해소해 둔 것으로 확인되어 결함으로 세지 않음(coverage 기록용):

- $\xi$(appendix, B성분 자리 분율=본문 θ) vs $\xi$(본문, 탈리튬화 진행률=1−θ) — 부록 L6-8, L54-60에서 배향까지 명시(지시문에서 이미 처리된 사안으로 지정).
- $g$의 4중 사용(조성 자유에너지·BW 자유에너지·봉우리 가중·상태밀도) — Ch2 L473-474 "★기호 주의" 박스로 해소.
- OCV vs OCP — Ch1 L1473-1474에서 "OCP(...) — 본 문건의 OCV 와 같은 반쪽전지 준평형 전위, 문헌 표기 따름"으로 명시적으로 등치.
- "격자"의 결정격자(lattice) vs 수치 격자(grid) 중의성 — Ch1 L918 "(수치 grid --- 결정 lattice 와 무관)"으로 해소.
- $\Omega$ 부호·임계값(2RT) 관례 — Ch1·Ch2·부록 세 파일 모두 "$\Omega>0$=인력/상분리 경향, 임계 $\Omega=2RT$" 로 일관.

---

## 요약

| # | 위치 | 내용 | 심각도 |
|---|------|------|--------|
| A1-1 | Ch1 L1414 vs L3070 | "가역 기준선" vs "평형 기준선" 혼용 — γ_j 조건 누락 | HIGH |
| A3-1 | Ch1 L1526 | 기호 $s$ 재사용(고정 부호 vs logistic scale) | HIGH |
| A1-2 | Ch1/Ch2 전역 | "peak" vs "봉우리" 어휘 분할 | MED |
| A3-2 | Ch1 L1515-1558 | $\sigma_\mathrm{int}$ 정의 없이 사용 | MED |
| A3-3 | Ch1 L244/L1579 | $\gamma_j$(분기 인자) vs $\gamma$(계면 에너지) 무disclaimer 재사용 | MED |
| A4-1 | Ch1/Ch2 vs 부록 | 혼합 자유에너지 $g$(본문) vs $f$/$g$(부록) 대응 미명시 | MED |
| A2-1 | Ch1 L1523-1524 | FWHM 원어 미병기(문서 자체 컨벤션 이탈) | LOW |

범주별 근거 0건 없음(①②③④ 모두 최소 1건 이상 실 결함 + coverage 목적의 "이미 해소" 목록 병기). 가장 약한 항목은 A2-1(FWHM)로 명시.
