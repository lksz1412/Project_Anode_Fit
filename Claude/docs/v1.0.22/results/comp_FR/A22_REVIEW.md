# A22_REVIEW — FR-A22 심층 검토 (§3.2 케이스 3계열 · §3.3 블렌드 공통-μ)

- 검토 창: FR-A22 (v1.0.22 대공사) · 보고 전용(소스 수정 없음 · git 조작 없음 · Codex/ 접근 없음)
- 대상: `Claude/docs/v1.0.22/_sections/ch3v22_sec02_cases.tex` (101행) · `ch3v22_sec03_blend.tex` (179행)
- 검토 4관점: ①내용 보완(빡세게) ②논리 오류(재계산·재유도 검증) ③더 쉬운 설명 ④산문→수식 간결화
- 표기 규약: 발견별 1행 표(`| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |`) + **직후 `현행(축자)` 펜스 블록(개행 포함 원문 그대로 — 기계 매칭용)** + `제안(완성 LaTeX)` 펜스 블록. 표 셀 안은 미리보기, 축자 원문은 펜스 블록이 정본.
- 파일 약칭: S2 = ch3v22_sec02_cases.tex · S3 = ch3v22_sec03_blend.tex

---

## H 등급 (논리/물리 오류·오귀속)

### H-1 — wang_asi2013 두-상 상 표기 자기모순 (c-Si → a-Si)

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| H-1 | ch3v22_sec02_cases.tex:45-46 | 논리 | H | "나노 a-Si 는 첫 사이클만 두-상(c-Si$/$a-Li$_{2.5}$Si)" | c-Si → a-Si 정정 | 같은 문장 내 자기모순 + 인용 논문 제목이 "Amorphous Silicon" |

현행(축자):
```latex
\textbf{1차 vs 순환 안정.} 나노 a-Si 는 첫 사이클만 두-상(c-Si$/$a-Li$_{2.5}$Si)이고 이후 순환은
solid-solution 경사로 옮겨간다\cite{wang_asi2013}
```
제안(완성 LaTeX):
```latex
\textbf{1차 vs 순환 안정.} 나노 a-Si 는 첫 사이클만 두-상(a-Si$/$a-Li$_{2.5}$Si)이고 이후 순환은
solid-solution 경사로 옮겨간다\cite{wang_asi2013}
```
근거: (i) 주어가 "나노 **a-Si**"인데 두-상 쌍을 "**c-Si**/a-Li₂.₅Si"로 적음 — 비정질 출발 재료에 결정질 Si 상이 있을 수 없음(문장 내 자기모순, 문헌 무관 확정). (ii) 인용 문헌 `ch3v22_bib.tex:22` 제목 = "Two-Phase Electrochemical Lithiation in **Amorphous** Silicon"(Nano Lett. 13, 709) — 이 논문의 두-상 계면은 a-Si/a-Li~2.5Si. (iii) 오류 기원 = `results/comp_R4/SI_CASES.md:26` R4 전사행 자체가 "a-Si 나노구: 첫 사이클 2상(c-Si/a-Li₂.₅Si)"로 이미 자기모순 — R4 전사 오류가 본문으로 전파된 사례. 외부 재확인은 §서치 하이쿠 표 참조.

### H-2 — mcdowell_coreshell2013 인용 오귀속 (c-Si 코어/쉘 문장에 비정질 논문)

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| H-2 | ch3v22_sec02_cases.tex:40-41 | 논리 | H | c-Si 코어/비정질 껍질 문장에 \cite{...,mcdowell_coreshell2013} | mcdowell 를 a-Si 문장(45-46행)으로 이동 | 논문 제목 = "Amorphous Silicon Nanospheres" |

현행(축자):
```latex
\textbf{곡선 개형.} 첫 리튬화는 결정질 Si$\to$비정질 Li$_x$Si 의 두-상 경사이며, 결정 코어/비정질 껍질의
이동 경계로 진행한다\cite{limthongkul2003,li_dahn2007,mcdowell_coreshell2013}.
```
제안(완성 LaTeX — 인용 재배치만; 45-46행의 wang 문장에 병기):
```latex
\textbf{곡선 개형.} 첫 리튬화는 결정질 Si$\to$비정질 Li$_x$Si 의 두-상 평탄역이며, 결정 코어/비정질 껍질의
이동 경계로 진행한다\cite{limthongkul2003,li_dahn2007}.
```
(45-46행 측: `...옮겨간다\cite{wang_asi2013,mcdowell_coreshell2013}` 로 병기 — H-1 적용본과 동시 적용 가능)
근거: `ch3v22_bib.tex:23` 제목 = "In Situ TEM of Two-Phase Lithiation of **Amorphous** Silicon Nanospheres"(Nano Lett. 13, 758) — 결정질 Si 의 코어/쉘 이동 경계 근거로는 부적합(그 근거는 limthongkul2003·li_dahn2007 로 충분), 45-46행의 a-Si 두-상 서술의 동반 근거(Wang 709 와 자매 논문)로 이동해야 정귀속. 오류 기원 = `comp_R4/SI_CASES.md:43` ("c-Si 코어·a-Li_xSi 껍질" — 제목과 모순되는 R4 전사). ※ 위 제안 블록은 H-3(경사→평탄역)를 함께 반영한 형태 — 인용만 고치려면 "두-상 경사" 유지.

### H-3 — "두-상 경사" 물리 용어 충돌 (두-상 = 평탄역)

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| H-3 | ch3v22_sec02_cases.tex:40 | 논리 | H | "결정질 Si→비정질 LixSi 의 두-상 경사이며" | "두-상 평탄역이며" | 두-상 공존 = 불변 μ = plateau — 문서 자체 peak 문법·§3.2 내 Si–C 서술과 충돌 |

현행(축자): H-2 블록과 동일(40-41행).
제안(완성 LaTeX): H-2 제안 블록에 포함("두-상 평탄역이며").
근거(재유도): 고정 T·P 의 이성분 두-상 공존은 μ_Li 불변 ⟹ 전위 평탄역(plateau) ⟹ dQ/dV 날카로운 peak — Ch1 골격과 본 장 자체가 쓰는 문법. 내부 대조 3건: (i) §3.1 tab:si-survival N6 행 "날카로운 peak 문법은 ... **1차 리튬화 두-상**(사실 ii·iii)에만"(ch3v22_sec01_map.tex:82) — 두-상 = 날카로운 peak = 평탄역. (ii) §3.2:69 같은 물리(저-밀링 Si–C 첫 리튬화)를 "$\sim$0.1 V **뚜렷한 평탄역**"으로 기술. (iii) §3.1:46 "평탄역 부재의 경사 전위"는 **첫 사이클 이후** 비정질 경로에 배정 — 첫 리튬화가 "경사"면 이 구분이 무너짐. 피팅 파급: 평탄역→좁은 $w_j$, 경사→큰 $n_j$ 폭 — 초기값 시딩 방향이 갈림. 기원 = `comp_R4/SI_CASES.md:15` 특징명 "2상 진행·경사 전위"의 병렬 표기가 본문에서 한 단어로 융합된 것으로 추정. (실측 곡선의 미세 기울기를 남기려면 "두-상 평탄역(유한 율속에서 완만한 기울기로 관측)" 병기 대안.)

### H-4 — f_Si ∈ [0,0.3] (용량 분율) 와 wt% 기반 tier-A 앵커의 범위 충돌

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| H-4 | ch3v22_sec03_blend.tex:69-75 (연동: ch3v22_notation.tex:29·ch3v22_sec05_code.tex:44) | 논리 | H | boxed 중심식 내 $f_\mathrm{Si}=Q_\mathrm{Si}/Q\in[0,0.3]$ | 질량↔용량 분율 환산 각주 신설(+범위 재선언은 사용자 결정) | 용량 분율 독법에서는 본 장의 실측 접점(10–30 wt%)이 전부 범위 밖 |

현행(축자):
```latex
\begin{equation}
\boxed{\;\sum_{\mathrm{host}\in\{\mathrm{gr},\mathrm{Si}\}}\ \sum_{j=1}^{N_p^\mathrm{host}}
Q_j^\mathrm{host}\,\xi_{\eq,j}^\mathrm{host}\bigl(U_\mathrm{oc},T\bigr)=Q\,\bar x,
\qquad
Q=Q_\mathrm{gr}+Q_\mathrm{Si},\quad f_\mathrm{Si}=\frac{Q_\mathrm{Si}}{Q}\in[0,0.3]\;.}
\label{eq:blend-balance}
\end{equation}
```
제안(완성 LaTeX — 식 무변경 + 직후 문단(76행 "이 식은..." 문장)에 각주 부착; 범위 자체의 재선언 여부는 사용자 결정 경계):
```latex
%% 76행 "...바뀐 것은 지표의 범위뿐이고," 뒤 적절한 위치에:
\footnote{$f_\mathrm{Si}$ 는 \emph{용량} 분율이다(표기표) --- 질량 분율 $m_\mathrm{Si}$ 와는
$f_\mathrm{Si}=m_\mathrm{Si}\,q_\mathrm{Si}\,/\,[\,m_\mathrm{Si}\,q_\mathrm{Si}+(1-m_\mathrm{Si})\,q_\mathrm{gr}\,]$
($q$ $=$ 비용량)로 환산되고, $q_\mathrm{Si}\gg q_\mathrm{gr}$ 라 wt\% 수치보다 훨씬 크게 앉는다 --- 예로
\S\ref{ssec:si-sic} 의 Si 10 wt\% 시료(복합 가역 $\sim$565 mAh/g)는 흑연 몫을 빼면
$f_\mathrm{Si}\approx0.4$ 안팎이다. 곧 $[0,0.3]$ 은 wt\% 가 아니라 용량 분율의 스윕 범위이며,
\S\ref{ssec:si-blend-gs2}$\cdot$\S\ref{sec:si-code} 의 wt\% 기반 실측 앵커와 대조할 때는 이 환산을
거쳐야 한다.}
```
근거(재계산): $f_\mathrm{Si}^{\mathrm{cap}}=m_\mathrm{Si}q_\mathrm{Si}/[m_\mathrm{Si}q_\mathrm{Si}+(1-m_\mathrm{Si})q_\mathrm{gr}]$, $q_\mathrm{gr}=372$. (a) naboka 10 wt%(§3.3:117-119 가 "실측 접점"으로 지목): R4 `SIC_CASES.md:15` 복합 가역 565 mAh/g — 흑연·탄소 ~80-90 wt% 몫 298-335 를 빼면 Si 몫 230-267 ⟹ f_cap ≈ 0.41-0.47 > 0.3. (b) 30 wt%(chatzogiannakis, GS-2 인용): q_Si~1000-2000 에서 f_cap ≈ 0.54-0.73. (c) gautam Si15Gr75: f_cap ≈ 0.35-0.62. 즉 **용량 분율 독법(표기표 ch3v22_notation.tex:29 "용량 몫"으로 고정)에서는 [0,0.3] 이 본 장의 tier-A 앵커 전부를 배제** — 범위의 출처인 R4 `BLEND_UP.md`(5-30%)는 전부 **wt%** 스윕이라 정의 전환 과정에서 단위가 어긋난 것. 제거 없는 최소 봉합 = 위 환산 각주(Option A). 근본 해소 = 범위를 wt% 로 재정의하거나 용량 분율 상한을 ~0.7 로 재선언(Option B — 중심식·G2 게이트·표기표 3곳 연동, **사용자 결정 경계**).

### H-5 — §3.5 G2 게이트의 출처 지목 stale (§3.3 GS-2 에 없는 gautam·moyassari 지목, moyassari 는 원장 미등재)

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| H-5 | ch3v22_sec05_code.tex:44-45 (§3.3 검증 중 발견 — 인접 절 소재) | 논리 | H | "(\S\ref{ssec:si-blend-gs2}: gautam/moyassari/chatzogiannakis, tier-A)" | 실제 소재·등재 상태에 맞춘 재지목 | ssec:si-blend-gs2 에는 chatzogiannakis 만 존재; gautam 은 §3.2 표 각주; moyassari 는 ch3 서지·원장 부재 |

현행(축자):
```latex
$\cdot$ \textbf{G2 스윕 연속성}: $f_\mathrm{Si}\in(0,0.3]$ 에서 곡선이 $f_\mathrm{Si}$ 에 연속(불연속 점프 없음)
--- 대조 데이터는 f$_\mathrm{Si}$ 스윕 실측(\S\ref{ssec:si-blend-gs2}: gautam/moyassari/chatzogiannakis, tier-A).
```
제안(완성 LaTeX):
```latex
$\cdot$ \textbf{G2 스윕 연속성}: $f_\mathrm{Si}\in(0,0.3]$ 에서 곡선이 $f_\mathrm{Si}$ 에 연속(불연속 점프 없음)
--- 대조 데이터는 f$_\mathrm{Si}$ 스윕 실측(\cite{gautam_blend2024}[표~\ref{tab:si-cases} 각주 $e$]$\cdot$
\cite{chatzogiannakis_blend2025}[\S\ref{ssec:si-blend-gs2}], tier-A; Si 0--20 wt\% 딜라토메트리 스윕
moyassari\_blend2022 는 원장 미등재 --- V1 등재 후 추가).
```
근거: (i) §3.3 GS-2 srcbox(ch3v22_sec03_blend.tex:135-146)의 인용 = ai_composite2022·chatzogiannakis_blend2025·zhan_siox2026·tu_blend2024 — gautam·moyassari 없음. gautam_blend2024 의 실제 소재 = §3.2 표 각주 e(ch3v22_sec02_cases.tex:24). (ii) moyassari_blend2022 는 `ch3v22_bib.tex` 부재·`V1022_REFERENCE_LEDGER.md` 부재(grep 0건) — R4 `upgraded/BLEND_UP.md:23`(#4, tier A, DOI 10.1149/1945-7111/ac4545)의 **미채택 후보**가 §3.5 에 남은 stale 지목. 원장 규칙("본문 \cite 는 원장 V1 키만")상 게이트 대조 데이터로 지목하려면 등재 선행 필요. 기원 = `BLEND_UP.md:48` R6 매핑 권고("문헌 3·4·5")의 직전사. ※ f_Si 범위 (0,0.3] 자체는 H-4 와 연동.
<!-- H-END -->

---

## M 등급 (의미·이해 실질 개선)

### M-1 — 표 평균 전위 열의 방향(리튬화/탈리튬화) 무표기

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| M-1 | ch3v22_sec02_cases.tex:19-20 (표 30-34행 연동) | 보완 | M | 각주 b: "원소 Si 평균 전위 0.2–0.5 V 는 리뷰 경유..." | 각주 b 에 "탈리튬화 평균 기준" 명시 | R4 원표는 방향 명시("탈리튬화: 0.2–0.5 V") — 수백 mV 히스 계에서 방향 없는 평균은 ±0.2 V 급 모호 |

현행(축자):
```latex
$^b$원소 Si 평균 전위 $0.2$--$0.5$ V 는 리뷰 경유\cite{obrovac_chevrier2014}(B, 1차 정량
아님) --- Si--C $\sim$0.4 V\cite{andersen_sic2019}(A)와 계열 정합.
```
제안(완성 LaTeX):
```latex
$^b$평균 전위 열은 \emph{탈리튬화} 평균 기준(수백 mV 히스 계라 방향 명기 필수 --- 리튬화 평균은 그만큼
낮다): 원소 Si $0.2$--$0.5$ V 는 리뷰 경유\cite{obrovac_chevrier2014}(B, 1차 정량
아님) --- Si--C $\sim$0.4 V\cite{andersen_sic2019}(A, 평균 탈리튬화)와 계열 정합.
```
근거: R4 `SI_CASES.md:18` 원표 = "완전충전(Li₁₅Si₄): ~0 V vs Li/Li⁺; **탈리튬화**: 0.2–0.5 V" — 방향이 원표에 있었으나 표 전사에서 탈락. andersen 값도 본문(§3.2:75)·R4(`SIC_CASES.md:14`) 공히 "평균 **탈리튬화** 전위 ~0.4 V". 본 장이 §3.4 로 넘기는 수백 mV 히스(§3.2:50-52) 때문에 방향 무표기 평균 전위는 피팅 초기값으로 ±0.2 V 급 계통 모호 — 표만 방향이 없다.

### M-2 — 각주 d: 1710 mAh/g 의 화학량론 지위 보강(실리케이트 격리 반영 가역 이론값)

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| M-2 | ch3v22_sec02_cases.tex:21-22 | 보완 | M | "$^d$SiO 이론 용량 $1710$ mAh/g(A)." | 불균화 화학량론 정합 주석 병기(원문 귀속은 확인 필요 마커) | 재계산: 4SiO→Li₄SiO₄+3Si 후 Li₃.₇₅Si ⟹ 2.8125 Li/SiO ⟹ 1709.9 mAh/g — 정확 재현 |

현행(축자):
```latex
$^d$SiO 이론 용량 $1710$
mAh/g\cite{zhang_sio2018}(A).
```
제안(완성 LaTeX):
```latex
$^d$SiO 이론 용량 $1710$
mAh/g\cite{zhang_sio2018}(A) --- 이 값은 불균화 $4\,\mathrm{SiO}\to\mathrm{Li_4SiO_4}+3\,\mathrm{Si}$ 후
잔여 Si 의 Li$_{3.75}$Si 가역 몫($2.81$ Li/SiO)과 정확히 정합하는 \emph{실리케이트 격리를 이미 반영한}
가역 이론값이다(화학량론 귀속은 원문 확인 필요).
```
근거: 산술(로그-②c): 2.8125 × 26801.4/44.085 = 1709.9 ⟹ 1710 정확 재현 — 표의 1710 과 §3.2.2 의 실리케이트 비가역 서사(Li₄SiO₄ 계)가 같은 화학량론의 두 얼굴임을 잇는 실질 보강(왜 "이론"인데 가역 열에 있는지도 해소). 단 zhang_sio2018 이 이 화학량론을 명시하는지 미확인 → "확인 필요" 마커 필수(과잉 귀속 방지, R4 규율 승계). 하이쿠 검증 §서치 위임.

### M-3 — Si–C 히스 절대 mV 공백의 마커·공백 목록 누락 (공백 표기 일관성)

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| M-3 | ch3v22_sec02_cases.tex:34·92-95 | 보완 | M | 표 Si–C 히스 셀 "기계 기원"(마커 없음)·srcbox 공백 목록 "이 넷" | 셀에 "(mV 확인 필요)" + 목록에 Si–C 히스 추가("이 다섯") | SiOx 히스는 각주 f 마커·목록 등재 — 같은 미확보인 Si–C 만 무마커 |

현행(축자 — 표 행):
```latex
Si--C 복합    & $3117$(1차 충전)     & $\sim$0.4          & $82^{\,e}$       & 기계 기원          & andersen\_sic2019 (A) \\
```
현행(축자 — srcbox):
```latex
필요}(공백)로 남긴 것: SiO$_x$ 절대 평균전위$\cdot$SiO$_x$ 히스 절대 mV$\cdot$Si 저온 $\Delta S(T)$
정량$\cdot$tier B 정량값(yamada\_sio2012$\cdot$lee\_sic2025 등) --- 이 넷은 표에 수치로 싣지 않고 명시적
공백으로 표기했다.
```
제안(완성 LaTeX):
```latex
Si--C 복합    & $3117$(1차 충전)     & $\sim$0.4          & $82^{\,e}$       & 기계 기원(mV 확인 필요) & andersen\_sic2019 (A) \\
```
```latex
필요}(공백)로 남긴 것: SiO$_x$ 절대 평균전위$\cdot$SiO$_x$ 히스 절대 mV$\cdot$Si--C 히스 절대 mV$\cdot$Si
저온 $\Delta S(T)$
정량$\cdot$tier B 정량값(yamada\_sio2012$\cdot$lee\_sic2025 등) --- 이 다섯은 표에 수치로 싣지 않고 명시적
공백으로 표기했다.
```
근거: R4 `SIC_CASES.md` 에 Si–C 히스 절대 mV 부재·본문(§3.2:67-78)에도 없음 — SiOx(각주 c·f "확인 필요")와 동일한 미확보 상태인데 표기만 비대칭. "은폐 없이"(§3.2:9-10) 원칙의 자기 일관 — 수치 충전이 아니라 마커 추가.

### M-4 — Li₁₅Si₄ "날카로운 dQ/dV 특징"의 방향(탈리튬화) 무표기

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| M-4 | ch3v22_sec02_cases.tex:41-43 | 보완/설명 | M | "약 50 mV 에서 ... 결정화해 날카로운 dQ/dV 특징을 남기고" | "이후 탈리튬화에" 방향 명시 | 결정화(리튬화 말단 ~50 mV)와 그 서명(탈리튬화 두-상 피크)의 전위·방향이 다름 |

현행(축자):
```latex
깊은 리튬화 끝(약 $50$
mV)에서 준안정 Li$_{15}$Si$_4$ 가 결정화해 날카로운 dQ/dV 특징을 남기고\cite{obrovac_christensen2004},
```
제안(완성 LaTeX):
```latex
깊은 리튬화 끝(약 $50$
mV)에서 준안정 Li$_{15}$Si$_4$ 가 결정화해 \emph{이후 탈리튬화에} 날카로운 dQ/dV 특징을
남기고\cite{obrovac_christensen2004},
```
근거: 현행 독법은 날카로운 특징이 ~50 mV(리튬화)에 있는 것으로 읽힘 — 실제 서명은 결정질 Li₁₅Si₄ 의 두-상 탈리튬화 피크. 내부 근거: §3.1 tab:si-survival N6 행 "날카로운 peak 문법은 Li$_{15}$Si$_4$ \textbf{탈리튬화}$\cdot$1차 리튬화 두-상에만"(ch3v22_sec01_map.tex:82) — 본문 §3.2 만 방향 무표기. 정확 피크 전위(~0.4 V대) 병기는 하이쿠 검증(§서치) 확정 후 선택 — 본 제안은 수치 없이 방향만(임의 수치 충전 회피).

### M-5 — "자릿수가 벌어지는" 과대 표현 (4.2배 — 각주 a 의 "~4배"와 내부 충돌)

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| M-5 | ch3v22_sec02_cases.tex:48-49 | 논리 | M | "만충 조성 이론 ~4200 mAh/g 과 자릿수가 벌어지는 것은" | "~4배 벌어지는" | 4200/1000 = 4.2 < 10 — 자릿수(한 자릿수) 미달; 각주 a 는 "~4배"로 옳게 적음 |

현행(축자):
```latex
초기 비가역 손실 $25$--$30\%$\cite{limthongkul2003} --- 만충 조성 이론 $\sim$4200 mAh/g\cite{wen_huggins1981}
과 자릿수가 벌어지는 것은 조성 도달 한계와 첫 사이클 SEI$\cdot$비정질화 소모 때문이다(표 각주 $a$).
```
제안(완성 LaTeX):
```latex
초기 비가역 손실 $25$--$30\%$\cite{limthongkul2003} --- 만충 조성 이론 $\sim$4200 mAh/g\cite{wen_huggins1981}
과 $\sim$4배 벌어지는 것은 조성 도달 한계와 첫 사이클 SEI$\cdot$비정질화 소모 때문이다(표 각주 $a$).
```
근거(재계산): 4200/1000 = 4.2 — 한 자릿수(10×) 미만. 같은 문장이 가리키는 각주 a 자체가 "$\sim$4배"로 옳게 정량(내부 충돌). 문서의 "자릿수" 용법 대조: §3.1:48 사실 v "~300% vs ~10% — 자릿수가 달라"(30×, 옳음) — 48행만의 슬립.

### M-6 — "만충 조성" 4200 의 고온 평형 조건 무표기(상온 상한 Li₁₅Si₄ 와 구분)

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| M-6 | ch3v22_sec02_cases.tex:17-19 | 보완 | M | 각주 a "이론 용량 ~4200 mAh/g(만충 조성, A)" | 고온 평형 기준·상온 상한 Li₁₅Si₄ 명시(수치는 검증 후) | wen_huggins1981 = 고온 용융염 titration — §3.1 사실 i 는 "고온 평형" 명기, 각주 a 만 무조건 |

현행(축자):
```latex
$^a$이론 용량 $\sim$4200 mAh/g(만충 조성\cite{wen_huggins1981}, A)는 1차 가역 $\sim$1000
mAh/g\cite{limthongkul2003}(A)의 $\sim$4배 --- 초기 비가역$\cdot$조성 도달 한계 반영, 표는 1차 가역을
대표값으로.
```
제안(완성 LaTeX — 상온 상한의 수치(≈3579) 병기는 §서치 검증 확정 후 선택):
```latex
$^a$이론 용량 $\sim$4200 mAh/g(만충 조성 Li$_{4.4}$Si --- \emph{고온 용융염 평형}
기준\cite{wen_huggins1981}, A; 상온 도달 상한 상은 Li$_{15}$Si$_4$)는 1차 가역 $\sim$1000
mAh/g\cite{limthongkul2003}(A)의 $\sim$4배 --- 초기 비가역$\cdot$조성 도달 한계 반영, 표는 1차 가역을
대표값으로.
```
근거: §3.1:38(사실 i) "\textbf{고온 평형}은 네 중간상...계단 plateau\cite{wen_huggins1981}" — 같은 문헌을 §3.1 은 고온으로 조건화, 각주 a 는 무조건 "만충 조성"이라 4200 이 상온 이론치로 오독될 여지(상온 전기화학 상한은 Li₁₅Si₄, ≈3579 mAh/g — 로그-②c 산술·§서치 검증 대기). 가중 사유: R4 근거행 `SI_CASES.md:35` 가 "**Li₁₅Si₄** 이론 용량: ~4200"으로 상 이름을 뒤바꾼 오기 — 본문은 "만충 조성"으로 피해갔으나 tier-A 계보의 원행이 오염되어 있어 구분 명시가 방어선.

### M-7 — kitada NMR 방법 표기: ²⁹Si 는 ex situ (in situ 로 오귀속)

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| M-7 | ch3v22_sec02_cases.tex:56-57 | 논리 | M | "(in~situ $^7$Li/$^{29}$Si NMR)" | "(in~situ $^7$Li $\cdot$ ex~situ $^7$Li/$^{29}$Si NMR)" | 논문 제목: "in Situ ⁷Li **and ex Situ** ⁷Li/²⁹Si" |

현행(축자):
```latex
특유의 이산 상전이 없이 \emph{연속적 비정질 Li$_x$Si 형성/분해}로 진행한다(in~situ $^7$Li/$^{29}$Si
NMR)\cite{kitada_sio2019}
```
제안(완성 LaTeX):
```latex
특유의 이산 상전이 없이 \emph{연속적 비정질 Li$_x$Si 형성/분해}로 진행한다(in~situ $^7$Li $\cdot$
ex~situ $^7$Li/$^{29}$Si NMR)\cite{kitada_sio2019}
```
근거: `ch3v22_bib.tex:26` 제목 원문 = "...by Combining **in Situ $^{7}$Li and ex Situ $^{7}$Li/$^{29}$Si** Solid-State NMR Spectroscopy" — ²⁹Si 관측은 ex situ. 방법 오귀속은 "operando 직접 추적" 급 주장 강도에 영향(²⁹Si 까지 operando 로 읽힘).

### M-8 — "소비 Li 의 ~40%가 실리케이트/Li₂O" 전액 귀속 — 같은 문장의 82.1% 와 산술 충돌

| ID | 파일:행 | 유형 | 등급 | 현행(요약) | 제안(요약) | 근거 |
|---|---|---|---|---|---|---|
| M-8 | ch3v22_sec02_cases.tex:59-61 | 논리 | M | "58.5%, 처리 시 82.1% — 소비 Li 의 ~40%가 1차 실리케이트/Li₂O 로 간다는 직접 수치다" | 소거분(~24%p)과 잔존분(~18%, SEI 등) 분리 서술 | 재계산: 전액 실리케이트면 처리 후 잔존 비가역 17.9% 를 설명 못함 |

현행(축자):
```latex
로 정량된다: 미처리 SiO $58.5\%$, Li 분말 고상반응 처리 시 $82.1\%$\cite{yom_sio2016} --- 소비 Li 의
$\sim$40\%가 1차 실리케이트/Li$_2$O 로 간다는 직접 수치다.
```
제안(완성 LaTeX):
```latex
로 정량된다: 미처리 SiO $58.5\%$, Li 분말 고상반응 처리 시 $82.1\%$\cite{yom_sio2016} --- 미처리 비가역
$\sim$41.5\% 가운데 사전 고상반응으로 소거되는 $\sim$24\%p 가 실리케이트/Li$_2$O 몫에 대응하고, 잔여
$\sim$18\%(SEI 등)는 처리 후에도 남는다는 직접 수치다.
```
근거(재계산): 100−58.5 = 41.5(총 비가역) · 82.1−58.5 = 23.6%p(사전 처리 소거분 = 사전 형성 가능한 실리케이트/Li₂O 몫) · 100−82.1 = 17.9%(처리 후 잔존 = SEI 등 비실리케이트 몫). "~40% 전액 = 실리케이트/Li₂O" 독법은 같은 문장이 제시한 82.1% 와 충돌(전액이면 처리 후 비가역 ≈ 0 이어야). 기원 = R4 `SIOX_CASES.md:18` 요약("~40% 가 실리케이트/Li₂O 형성에 불가역 소모")이 총 비가역과 실리케이트 몫을 융합. 원 논문이 40% 전액 귀속을 명시하는지는 §서치 하이쿠 확인 — 명시 시 "원문 주장" 꼬리표로 보존하는 대안도 가능.
<!-- M-END -->

---

## L 등급 (문체·경미)

<!-- L-END -->

---

## §서치 — 하이쿠 서브에이전트 문헌 후보 (doi 실검증분만)

<!-- SEARCH-END -->

---

## 검증 로그 (축별 append)

**[로그-②a | §3.3 수식 재유도 검증 — 완료]** eq:blend-factor: 단일 자리 $\Xi_1=\sum_{n=0,1}e^{-\beta(\tilde\varepsilon-\mu)n}=1+e^{-\beta(\tilde\varepsilon-\mu)}$ ⟹ 독립 자리 곱 = (host,j) 이중곱 — **재유도 일치**. eq:blend-occ: $k_BT\,\partial_\mu\ln\Xi_1=1/(1+e^{+\beta(\tilde\varepsilon-\mu)})=\theta$ — **일치**(Fermi 형, ch1 eq:sm-mc-occ 의 host 판 그대로). eq:blend-balance 항등: $\sum Q_j^h(1-\theta_j^h)=(F/N_A)(M_{\rm tot}-\langle N\rangle)=Q\bar x$ (정의 $\bar x=1-\langle N\rangle/M_{\rm tot}$ 대입) — **항등 성립**. 요동: $\partial_\mu\theta=\beta\theta(1-\theta)$ ⟹ $\partial_\mu\langle N\rangle=\beta\sum M\theta(1-\theta)=\beta\,{\rm var}(N)>0$ — **양성·가법 성립**(host 간 독립 전제 하). 극한: $s=+1$ 결선(ch1 eq:sm-eqcond 원문 대조)에서 $V\!\to\!-\infty\Rightarrow\xi\to0$, $V\!\to\!+\infty\Rightarrow\xi\to1$ ⟹ 좌변 $0/Q$ — "$U_{\rm oc}\to\mp\infty$ 에서 $0/Q$" 표기 **정합**(ch1:366 과 동일 표기). f_Si→0 회수: $Q_j^{\rm Si}\to0$ ⟹ Si 이중합 소거·$\bar x$ 정의 잘 정의 유지 ⟹ eq:sm-mc-balance 로 축자 회귀 — **성립**. eq:blend-dqdv: $d\xi/dV=\xi(1-\xi)/w$ (eq:sm-logistic 미분·eq:eqpeak 원문 대조) ⟹ $C_\bg+\sum\sum Q\xi(1-\xi)/w$ — **차원·계수 일치**. 부호 읽기(iii): $V\uparrow\Rightarrow\mu\downarrow\Rightarrow\theta\downarrow\Rightarrow\xi\uparrow$ — ch1 signbox 와 **동일 방향**. 이월 주장 축자 대조: eq:sm-mc-factor/occ/balance/fluc·"가드(Ω>2RT)"·"N_p=1 회수" 문구 모두 ch1_sec02b_part0.tex:280-380 원문과 **정합**(과대 인용 없음).

**[로그-②b | §3.3 논리 축 발견분]** H-4(f_Si 범위·단위 충돌 — 재계산 3건 첨부)·M-12(세 실측 오계수)·M-11(eq:sum host 판 과대)·M-13(원장 상태 stale)·L-5(≥2 근거 과잉)·L-6(포갠다) — 본문 표 참조. GS-2 4분류(물리 가정 충돌) 판정 자체는 **타당**(논리 공백·수치해법·정의상 implicit 배제 논증 각각 확인 — P3-4 정합).

**[로그-②c | §3.2 수치 재계산 검증 — 완료]** ICE 정합: 3117/3801 = 0.8200 ⟹ "≈82%" **일치**. 70–75% = 100−(25–30) **일치**. 4200/1000 = 4.2 ⟹ "~4배"(각주 a) 일치 / "자릿수"(48행) **불일치** → M-1. yom: 100−58.5 = 41.5, 82.1−58.5 = 23.6, 100−82.1 = 17.9 ⟹ "~40% 전액 실리케이트/Li₂O" 과대 귀속 → M-3. 엔트로피 계수 범위 포락 40–105 ⊇ (40–95)∪(45–105) **일치**. SiO 이론 1710: 화학량론 4SiO+4Li→Li₄SiO₄+3Si 후 3Li₃.₇₅Si ⟹ 2.8125 Li/SiO × (26801.4/44.085) = 1709.9 ⟹ **1710 정확 재현**(M-16 보강 제안 근거). Li 당 환산치: Li₃.₇₅Si = 3.75×26801.4/28.086 = 3578.6(≈3579)·Li₄.₄Si = 4199.2(≈4200) — M-2 근거 산술.
<!-- LOG-END -->

---

## 무발견 축 (검토했으나 문제 없음)

<!-- NOFIND-END -->

---

## 말미 4-tier 정리 (확정/추정/미검증)

<!-- TIER-END -->
