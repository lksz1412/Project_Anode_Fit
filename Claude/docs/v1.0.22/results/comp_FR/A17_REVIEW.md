# A17_REVIEW — FR-A17 심층 검토 (Ch2 LCO 서두·기호표·§2.1)

- 검토 창: FR-A17 (v1.0.22 대공사, BRIEF_FR_A.md 규율 준수 — 보고 전용)
- 검토일: 2026-07-18
- 대상(전문 정독):
  - `Claude/docs/v1.0.22/_sections/ch2v22_sec00_intro.tex` (Ch2 서두, 12행)
  - `Claude/docs/v1.0.22/_sections/ch2v22_notation.tex` (Ch2 기호표, 15행)
  - `Claude/docs/v1.0.22/_sections/ch1_sec11_lcointro.tex` (§2.1 Part II 도입 — 역사적 파일명, Ch2 빌드 소속, 176행)
- 검토 4관점: ①내용 보완 ②논리 오류(재계산·재유도) ③더 쉬운 설명 ④산문→수식 간결화
- 참조 확인(read-only): Ch1 라벨 원문(xr 대상), 빌드 파일, V1022_REFERENCE_LEDGER.md
- 명칭 주의: `ch1_sec11` 파일명은 역사적 명칭이며 실제 소속은 Ch2 LCO 빌드. §제목 "Part II 도입"은 P5 보존 대상(기지 이슈 — 개정 제안만).

## 발견 표 (검증 완료분 즉시 append)

| ID | 파일:행 | 유형 | 등급 | 현행(축자) | 제안(완성 LaTeX) | 근거 |
|----|---------|------|------|-----------|------------------|------|
| A17-H1 | ch2v22_notation.tex:8 | 논리(오귀속) | H | `$\xi_{\eq,j}$~\eqref{eq:logisticsolve}` | `$\xi_{\eq,j}$~\eqref{eq:xieq}` | 계승 기호표의 앵커 오귀속. eq:logisticsolve(ch1_sec05_width.tex:37)는 유도 중간의 bare logistic — 첨자 없는 $\xi_\eq$·고정 부호 $s$·폭 $RT/F$·중심 $U_j$ 형태로, 계승 대상인 $j$-첨자·$\sigma_d$-일반·$w_j$ 폭·분기 중심 $U_j^{\,d}$ 의 확정 박스식은 eq:xieq(ch1_sec05_width.tex:284)다. D22 규약("정의는 Chapter 1 해당 위치가 유일 기준")과 충돌하고, Ch2 본문 자신도 §2.1(ch1_sec11:21 "평형 진행률 logistic 식~\eqref{eq:xieq}")·§2.6(ch1_sec16 (b) "흑연 식~\eqref{eq:xieq}")에서 eq:xieq 를 앵커로 쓴다. 기호표의 다른 앵커(eq:Uj·eq:dUhys·eq:Ubranch·eq:sm-mc-balance·eq:sum)는 전부 결과 박스식 — 이 항만 유도 중간식을 가리킴. |
| A17-M1 | ch2v22_notation.tex:12 | 논리(부분 오귀속) | M | `질서상$\cdot$MIT 2상역 파라미터(\S\ref{sec:lco-hys-od})` | `질서상$\cdot$MIT 2상역 파라미터(\S\ref{sec:lco-hys-od}$\cdot$\S\ref{sec:lco-hys-mit})` | 신규 기호의 도입-절 포인터("각 도입 절이 정의 기준")가 절반만 맞음. §lco-hys-od(ch1_sec13:105)는 T2·T3 질서상 전용이고, MIT 2상역 파라미터($\Omega_1^\mathrm{cat}$ 대입형·구조/전자 슬롯 분리 eq:lco-mit)는 §lco-hys-mit(ch1_sec13:177)이 도입한다. |
| A17-M2 | ch2v22_notation.tex:10 | 보완 | M | `합산식~\eqref{eq:sum}.` | `합산식~\eqref{eq:sum}·두 전위 $V_\app$/$V_n$ 와 분극~\eqref{eq:vn}·배경 $C_\bg$·셀 용량 $Q_\cell$ 와 전류 환산~\eqref{eq:n0map}·반응 엔탈피 $\Delta H_{\rxn,j}$~\eqref{eq:Uj}·활성화 키 $\Delta H_{a,j},\Delta S_{a,j},\chi_d$(\S\ref{sec:lag}).` | 계승 목록 누락 보강. §2.1 자신이 쓰는 계승 기호가 표에 없음: `\|I\|=c_rate·Q_cell`(ch1_sec11:15)·배경 $C_\bg$(:22)·$V_\app>V_n$(:101·그림)·파라미터 묶음 $(\Delta H_\rxn,\dots,\Delta H_a,\dots)$(:80). P3-1(V 위계 일관) 관점에서도 두 전위의 정의 위치(eq:vn) 명시가 방어적. 삭제 없음 — 말미 추가만. |
| A17-M3 | ch2v22_notation.tex:13-14 | 보완 | M | `슬롯 분해`(개행)`$\Delta S^\mathrm{config/vib/e}_j$(\S\ref{sec:lco-decomp}).` | `슬롯 분해 $\Delta S^\mathrm{config/vib/e}_j$(\S\ref{sec:lco-decomp}), 리튬 함량 $x$ 와 전이 라벨 T1--T3(표~\ref{tab:lco-staging}; $\xi\to x$ 조성 매핑은 \S\ref{sec:lco-code} 식~\eqref{eq:lco-xmap})·양극 상첨자 $(\cdot)^\mathrm{cat}$(\S\ref{sec:lco-center} 식~\eqref{eq:lco-n0sub})·게이트 폭 $\Delta x_\mathrm{MIT}$(\S\ref{sec:lco-electronic}).` | 신규 목록 누락 보강. Ch2 전용 신규 기호 중 표에 없는 것: 리튬 함량 $x$(본 장 도처 — $x$ 범위 열·$x_\mathrm{MIT}$·$g(E_F,x)$·$\Delta S_e(x,T)$; Part 0 가 "★$\bar x$ 는 Li 함량 $x$ 와 배향이 반대다"(ch1_sec02b:329)로 혼동 주의까지 둔 좌표)·전이 라벨 T1--T3·양극 상첨자 $^\mathrm{cat}$(ch1_sec12 eq:lco-n0sub 도입)·게이트 폭 $\Delta x_\mathrm{MIT}$(eq:lco-SeV). $x$ 정의 실재 확인: 표 캡션(ch1_sec11:54-55)·조성 매핑 eq:lco-xmap(ch1_sec17:125). |
| A17-M4 | ch1_sec11_lcointro.tex:83 | 논리(과소 주장) | M | `N1--N5 구간에서 흑연과 LCO 는 \emph{같은 식}을 공유하므로` | `N0--N9 전 사슬에서 흑연과 LCO 는 \emph{같은 식}을 공유하므로` | 자기 절의 전극-중립 5식 목록(:12-24)이 이미 N0 매핑(eq:n0map)·N6 평형 peak(eq:eqpeak)·N9 합산(eq:sum)까지 포함하고, (c)항(:107-109)은 N8 꼬리(eq:reversal)의 전극 무관 처리를 명시 — N1--N5 로 좁히면 자기 목록과 불일치(N 노드 대응: N0·N1=sec01, N2=sec03, N3=sec04, N4·N5=sec05, N6=sec06, N7=sec08, N8=sec09, N9=sec10 — 전 노드 식 공유 확인). 직전 문장의 "단 하나의 구조적 차이 = T1 전자 엔트로피 항" 단서는 그대로 유효. |
| A17-M5 | ch1_sec11_lcointro.tex:97-98 | 보완(가드) | M | (아래 축자 블록 — 개행 포함) | (아래 제안 블록 — 문장 1개 추가) | 흑연 하프셀 '방전' 라벨의 이중 관례 함정이 무가드. Ch1 N0(eq:n0map, ch1_sec01:14)의 방전$\mapsto+1$=탈리튬화는 풀셀 역할 라벨(음극 산화=방전)인데, 흑연‖Li 코인 하프셀의 사이클러 관례는 반대(셀 전압 하강=방전=흑연 리튬화)다. LCO 는 두 읽기가 일치("충전"=탈리튬화=전압 상승)하나 흑연 줄은 갈리므로, 실측 데이터 열의 문자열을 그대로 슬롯에 넣는 오배정 위험이 박스 바로 옆에 있음. 본 절의 슬롯 규약 자체가 이 혼동 방지 장치이므로 함정을 명명하면 가드가 완성됨. |
| A17-M6 | ch1_sec11_lcointro.tex:168 | 논리(서지 범위 오귀속) | M | `MSMR 모델\cite{msmr_origin2017,msmr2024}은 양극 조성을 전위의 전이별 logistic 합으로 적는 표준` | `MSMR 모델\cite{msmr_origin2017,msmr2024}은 삽입 전극 조성(원계열 적용례는 흑연$\cdot$스피넬$\cdot$인산철$\cdot$층상 산화물)을 전위의 전이별 logistic 합으로 적는 표준` | 인용 서지와 서술 범위 불일치: msmr_origin2017 은 흑연 포함 4계 공통 틀(sec17:7-8 이 자인 — "흑연·스피넬·인산철·층상 산화물에 한 틀로"), msmr2024 는 MCMB **흑연** 파라미터화(bib 부기). "양극 조성"으로 좁히면 모델 일반성이 과소 — 전극-중립 골격과 짝지어지는 근거(사실상 본 절의 논지)도 약화됨. 주의: ch1_sec17:6 에 동일 표현 존재(A20 관할 — 채택 시 양쪽 동시 정합 필요). |
| A17-M7 | ch1_sec11_lcointro.tex:42 | 보완(서지) | M | `세 전이를 남긴다\cite{xia2007}:` | `세 전이를 남긴다\cite{xia2007,reimers1992}:` | 4.05/4.17 V order--disorder 쌍·monoclinic 질서상의 1차 원전은 Reimers--Dahn in situ XRD(reimers1992 — V1 키 기존 등재, ch1_sec13:108 이 같은 취지로 인용). 하이쿠 서브 검증: reimers1992 의 x≈1/2 monoclinic 질서상·2상 창 0.75≤x≤0.93 확인, ~4.07 V feature 부분 확인. xia2007 은 4.55 V O3→H1-3 만 초록 수준 확인(3.90/4.05/4.17 은 전문 접근 제약으로 미확인)이라 병기가 앵커를 실질 보강. 신규 등재 불요(기존 V1 키). |
| A17-M8 | ch1_sec11_lcointro.tex:27-28 | 수식화(표기 정밀) | M | `전셀 합성`(개행)`($\partial U_\cell=\partial U_\mathrm{cat}-\partial U_\mathrm{an}$)은 범위 밖이며(후속)` | `전셀 합성($U_\cell=U_\mathrm{cat}-U_\mathrm{an}$ 및 그 미분들, 예: $\partial U_\cell/\partial T=\partial U_\mathrm{cat}/\partial T-\partial U_\mathrm{an}/\partial T$)은 범위 밖이며(후속)` | 벌거벗은 $\partial U$ 등식은 무엇에 대한 미분인지 미지정 — 표준 표기 아님. 부호 혼동 가드 문장(하프셀 vs 전셀)에 놓인 식이라 정밀성이 특히 중요(P3-1 취지). sec12 의 전셀 가드(swiderska2019 전셀 엔트로피 계수 언급)와도 정합: 전위 자체와 $T$-미분 둘 다 전극차로 합성됨을 한 번에 보임. |
| A17-L1 | ch2v22_notation.tex:7 | 문체(일관) | L | `폭 $w_j=n_jRT/F$·평형 진행률` | `폭 $w_j=n_jRT/F$~\eqref{eq:wbase}·평형 진행률` | 계승 목록의 타 기호는 전부 식 번호 앵커 부착 — $w_j$ 만 값 인라인·앵커 부재. eq:wbase(ch1_sec05:269) 병기로 일관화. |
| A17-L2 | ch1_sec11_lcointro.tex:107 | 설명 | L | `꼬리는 진행의 시간상 뒤쪽으로 늘어지므로` | `꼬리는 진행상 나중에 지나는 전위 쪽으로 늘어지고 인과 기억은 이미 지나온 과거를 훑으므로` | "시간상 뒤쪽"은 과거로 오독될 여지. Ch1 원문(ch1_sec09:189-190 "꼬리는 진행상 나중에 지나는 전위 쪽으로 늘어진다")의 명확한 표현으로 정렬 + 적분(과거)과 꼬리(미래 쪽 번짐)의 관계를 한 호흡에 — 뒤따르는 하한 $-\infty$/상한 $+\infty$ 설명의 인과 논리가 자립함. |
| A17-L3 | ch1_sec11_lcointro.tex:12-13 | 문체 | L | `본론 사슬에서 host 물질이 들어가지 않는 식이`(개행)`다섯이다:` | `본론 사슬에서 host 물질이 들어가지 않는 식 묶음이 다섯이다:` | 항목 (4)=eq:xieq+eq:wbase, (5)=eq:eqpeak+합산 — 두 항목이 각 2개 식 묶음이라 "식이 다섯"은 셈이 어긋남. |
| A17-L4 | ch1_sec11_lcointro.tex:31 | 문체(정밀) | L | `LCO 하프셀 전위는 vs Li/Li$^+$ 로 $\sim$3.9--4.2 V 영역에 있다` | `LCO 하프셀의 전이(peak) 전위는 vs Li/Li$^+$ 로 $\sim$3.9--4.2 V 영역에 있다` | 만방전($x\to1$) 부근 하프셀 전위는 $\sim$3.0 V 대까지 하강 — 3.9--4.2 V 는 본 장이 다루는 세 전이의 창. 한 단어 한정으로 정밀화. |
| A17-L5 | ch1_sec11_lcointro.tex:4 (+본문 "Part II" 7회) | 문체(★기지 이슈 연장 — 사용자 결정 대기) | L | `\section{Part II 도입 --- 전극-중립 골격과 방향 규약 (N0$'$)}\label{sec:lco-intro}` | (정합화 결정 시) `\section{Chapter 2 도입 --- 전극-중립 골격과 방향 규약 (N0$'$)}\label{sec:lco-intro}` + 본문 "Part II" 7곳 → "본 장(Chapter 2)" 계열 | RESUME_FR §5 기지 이슈("Part II 도입" 절 제목 P5 보존 vs 정합화 — 사용자 결정 대기)의 범위 확정 정보: "Part II" 자칭은 Ch2 빌드에서 sec11 에만 7회(다른 절 sec12--17·ch2v22 서두·기호표 = 0회), 반면 "Part I"·"Part 0"·"Part T" 는 Ch1 문서 내부 층 명칭으로 현행 유효(ch1_sec00:22-25 — sec12 도 "Part I" 사용)해 치환 대상 아님. P5 준수 — 제안만, 집행은 사용자 결정 후. |
| A17-L6 | ch1_sec11_lcointro.tex:47-48 | 설명 | L | `(tier --- 1차 문헌`(개행)`Xia\cite{xia2007}$\cdot$Reynier\cite{reynier2004}$\cdot$Motohashi\cite{motohashi2009} 에서 읽은 출발점)` | `(tier 는 항목별 --- 전위$\cdot$조성 anchor 는 1차 문헌 Xia\cite{xia2007}$\cdot$Reynier\cite{reynier2004}$\cdot$Motohashi\cite{motohashi2009} 에서 읽은 출발점, 개별 등급은 캡션 ★실측 근거 참조)` | "(tier ---" 가 등급 미지정 채 끊겨 독자가 "무슨 tier?"에서 멈춤. 실제 등급은 항목별(조성창 tier A·config 수치 tier C — 캡션 ★실측 근거(L2)가 관리)이므로 등급을 새로 단정하지 않고 캡션으로 위임하는 형태가 안전. |
| A17-L7 | ch2v22_sec00_intro.tex:7-8 | 보완 | L | `LCO 가 새로 요구하는 것 --- 방향 규약의 재배선, order--disorder 와`(개행)`MIT 2상역, 그리고 흑연에 없는 전자 엔트로피 항 --- 이 본 장의 본문이다.` | `LCO 가 새로 요구하는 것 --- 방향 규약의 재배선, order--disorder 와 MIT 2상역, 그리고 흑연에 없는 전자 엔트로피 항과 그 슬롯 분해 --- 이 본 장의 본문이며, 종반의 MSMR 동형이 대응을 닫는다.` | 서두 3항목이 기호표 신규 4단(σ_d 재배선·질서상/MIT 파라미터·전자항 게이트·슬롯 분해)과 어긋남 — 슬롯 분해(§lco-decomp N9')와 종결부 MSMR 동형(§lco-code)이 목차 예고에서 빠짐. 형제 서두 파일 간 정합. |

## 개행 포함 축자·제안 전문 블록 (기계 매칭용)

### A17-M5 — ch1_sec11_lcointro.tex:97-98 (현행 축자, 개행 그대로)
```latex
흑연도 LCO 도 탈리튬화에서 하프셀 전위가 \emph{오른다}(흑연 $\sim$0.08$\to$0.21 V, LCO
$\sim$3.9$\to$4.2 V)는 사실이 이 규약을 전극-중립으로 만들고, 그림~\ref{fig:lco-dirmap} 이 이 대응이다.
```
제안(위 두 행 바로 뒤에 가드 문장 1개 추가 — 기존 문장 무변경):
```latex
흑연도 LCO 도 탈리튬화에서 하프셀 전위가 \emph{오른다}(흑연 $\sim$0.08$\to$0.21 V, LCO
$\sim$3.9$\to$4.2 V)는 사실이 이 규약을 전극-중립으로 만들고, 그림~\ref{fig:lco-dirmap} 이 이 대응이다.
이때 흑연 줄의 ``방전''은 Ch1 N0(식~\eqref{eq:n0map})의 풀셀 역할 라벨(음극 산화 $=$ 방전)임에 주의하라
--- 흑연$\|$Li 코인 하프셀을 사이클러 표기로 읽으면(셀 전압 하강 $=$ 방전 $=$ 흑연 \emph{리튬화}) 라벨이
반대로 붙으므로, 데이터 열의 충$\cdot$방전 문자열이 아니라 \emph{작동 전극의 탈리튬화 여부}로 $\sigma_d$ 를
배정해야 한다(LCO 는 두 읽기가 일치해 이 함정이 없다).
```

### A17-M8 — ch1_sec11_lcointro.tex:27-29 (현행 축자, 개행 그대로)
```latex
두 번째 전극으로 들어온다. 본 장이 다루는 범위는 \emph{코인 하프셀}(LCO vs Li metal) 단독이다 --- 전셀 합성
($\partial U_\cell=\partial U_\mathrm{cat}-\partial U_\mathrm{an}$)은 범위 밖이며(후속), 단전극(하프셀) 부호와 전셀
부호를 섞지 않는다.
```
제안:
```latex
두 번째 전극으로 들어온다. 본 장이 다루는 범위는 \emph{코인 하프셀}(LCO vs Li metal) 단독이다 --- 전셀 합성
($U_\cell=U_\mathrm{cat}-U_\mathrm{an}$ 및 그 미분들, 예: $\partial U_\cell/\partial T
=\partial U_\mathrm{cat}/\partial T-\partial U_\mathrm{an}/\partial T$)은 범위 밖이며(후속), 단전극(하프셀) 부호와 전셀
부호를 섞지 않는다.
```

### A17-L3 — ch1_sec11_lcointro.tex:12-13 (현행 축자, 개행 그대로)
```latex
Part I 까지의 기호와 매핑은 \emph{전극을 가리지 않는다} --- 본론 사슬에서 host 물질이 들어가지 않는 식이
다섯이다:
```
제안:
```latex
Part I 까지의 기호와 매핑은 \emph{전극을 가리지 않는다} --- 본론 사슬에서 host 물질이 들어가지 않는 식 묶음이
다섯이다:
```

### A17-L6 — ch1_sec11_lcointro.tex:44-49 (현행 축자 — 각주 축약 표시, 실제 치환 대상은 괄호부만)
```latex
에 둔다(상세 \S\ref{sec:lco-preview}$\cdot$\S\ref{sec:lco-code}). 흑연이 4 staging 전이를 남기듯, LCO
... (tier --- 1차 문헌
Xia\cite{xia2007}$\cdot$Reynier\cite{reynier2004}$\cdot$Motohashi\cite{motohashi2009} 에서 읽은 출발점), 우리 시료 데이터로
피팅해 override 하는 전제다.
```
제안(괄호부 치환):
```latex
(tier 는 항목별 --- 전위$\cdot$조성 anchor 는 1차 문헌
Xia\cite{xia2007}$\cdot$Reynier\cite{reynier2004}$\cdot$Motohashi\cite{motohashi2009} 에서 읽은 출발점, 개별 등급은
캡션 ★실측 근거 참조), 우리 시료 데이터로
피팅해 override 하는 전제다.
```

### A17-L7 — ch2v22_sec00_intro.tex:6-8 (현행 축자, 개행 그대로)
```latex
의 식 번호를 그대로 인용하며, LCO 가 새로 요구하는 것 --- 방향 규약의 재배선, order--disorder 와
MIT 2상역, 그리고 흑연에 없는 전자 엔트로피 항 --- 이 본 장의 본문이다.
```
제안:
```latex
의 식 번호를 그대로 인용하며, LCO 가 새로 요구하는 것 --- 방향 규약의 재배선, order--disorder 와
MIT 2상역, 그리고 흑연에 없는 전자 엔트로피 항과 그 슬롯 분해 --- 이 본 장의 본문이며, 종반의
MSMR 동형이 대응을 닫는다.
```

### A17-M3 — ch2v22_notation.tex:13-14 (현행 축자, 개행 그대로)
```latex
게이트 $g(E_F,x)$$\cdot$게이트 중심 $x_\mathrm{MIT}$(\S\ref{sec:lco-electronic}), 슬롯 분해
$\Delta S^\mathrm{config/vib/e}_j$(\S\ref{sec:lco-decomp}).
```
제안:
```latex
게이트 $g(E_F,x)$$\cdot$게이트 폭 $\Delta x_\mathrm{MIT}$$\cdot$게이트 중심 $x_\mathrm{MIT}$(\S\ref{sec:lco-electronic}), 슬롯 분해
$\Delta S^\mathrm{config/vib/e}_j$(\S\ref{sec:lco-decomp}), 리튬 함량 $x$ 와 전이 라벨 T1--T3(표~\ref{tab:lco-staging};
$\xi\to x$ 조성 매핑은 \S\ref{sec:lco-code} 식~\eqref{eq:lco-xmap}), 양극 상첨자
$(\cdot)^\mathrm{cat}$(\S\ref{sec:lco-center} 식~\eqref{eq:lco-n0sub}).
```

## 등급별 정리

- **H (1건)**: A17-H1 — 기호표 계승 앵커 오귀속(ξ_eq,j → eq:logisticsolve ≠ 확정 박스 eq:xieq). Ch2 본문(sec11:21·sec16)과도 불일치라 기계 치환 1토큰으로 정합 회복.
- **M (8건)**: 기호표 포인터·목록 2건(M1 MIT 파라미터 도입 절 절반 누락 / M2·M3 계승·신규 목록 누락), 본문 논리·범위 3건(M4 "N1–N5" 과소 — 자기 5식 목록과 불일치 / M6 MSMR "양극 조성" 서지 범위 과소 / M8 ∂U 표기 비표준), 가드·서지 보강 2건(M5 흑연 '방전' 라벨 이중 관례 함정 명명 / M7 reimers1992 병기 — 기존 V1 키).
- **L (7건)**: 문체·정밀 5건(L1 w_j 앵커 일관·L2 꼬리 문장·L3 "식 다섯" 셈·L4 전이 전위 창 한정·L6 "(tier ---" 미완 괄호), 서두 정합 1건(L7), 기지 이슈 연장 1건(L5 "Part II" — 사용자 결정 대기, 범위 정보만 추가).

## §서치 — 하이쿠 서브 문헌 검증 (Agent 위임, DOI 실검증분만)

서브에이전트(model: haiku)가 Crossref API·저널 랜딩·arXiv 로 실검증한 결과 통합. **기억 서지 배제 — 실제 fetch 확인분만**. DOI 는 7건 전건 Crossref 해소 확인.

| 검증 항목 | 결과 | 본 검토 반영 |
|---|---|---|
| reynier2004 (10.1103/PhysRevB.70.174304) — x=1/2 **와 x=5/6** 질서상 | **확인** ("ordered structures exist at lithium concentrations of x=1/2 and x=5/6") | 캡션 :63 "O3 질서상 조성(x=½·⅚)" 귀속 **정당** — 무발견 확정 |
| reynier2004 — 엔트로피 삼분해(config/vib/electronic) | **확인** ("Three contributions to the entropy of lithiation…") | 캡션 "엔트로피 삼분해 tier-A" 귀속 정당 |
| menetrier1999 (10.1039/a900016j) — 2상 창 0.75≤x≤0.94 + **XRD 포함 여부** | **확인** (2상 창 명시·기법 "X-ray diffraction, electrical measurements and 7Li MAS NMR") | 캡션 :62-63 "tier-A 실측(XRD·NMR)" 귀속 정당 — 무발견 확정 |
| reimers1992 (10.1149/1.2221184) — 2상 0.75≤x≤0.93·x≈1/2 monoclinic·4.05/4.18 쌍 | 2상·monoclinic **확인**, 4.05/4.18 쌍은 부분 확인(~4.07 V feature) | A17-M7(병기 제안) 근거 |
| xia2007 (10.1149/1.2509021) — 3.90/4.05/4.17/4.55 V | 4.55 V O3→H1-3 **확인**(초록 "plateaus at approximately 4.55 V and 4.62 V"), 3.90/4.05/4.17 은 전문 접근 제약으로 **미확인** | :42-43 귀속은 미검증 잔여(반증 아님) — 4-tier 미검증 란 기재, M7 병기가 보강 |
| kim_entropymetry2020 (10.1039/C9EE02964H) — OD 엔트로피 서명·수치 | 서명 **확인**(monoclinic 중간상이 ΔS 기울기 반전), 수치(0.47/1.49)는 접근 불가 | 원장 기존 판정("서명 tier A/수치 미확보")과 일치 — 무발견 |
| motohashi2009 (10.1103/PhysRevB.80.165114) — 전자 상도표 | **확인**(arXiv 초록 "electronic phase diagram… established"; CoO2 끝점 = non-correlated metal) | :48 출발점 문헌 지위 정당(g_max=13 값 검증은 본 창 대상 밖 — sec15/A19 관할) |
| 후보 서치 — 0.47/1.49 J/(mol K)의 1차 원전 | 문헌상 x=0.50→0.47·x=0.67→1.49 로 반복 인용됨은 확인되나 **1차 원전 DOI 미확정** | 신규 등재 후보 **없음**(DOI 실검증 불가분은 후보 표 등재 금지 규율) — 본문 tier C 유지 판단과 정합. sec13 의 "x=⅔ anchor 조성 재배정 검토"와도 일치 |

신규 서지 등재 제안: **0건** (M7 은 기존 V1 키 reimers1992 의 인용 위치 추가라 등재 불요).

## 검증 로그 (축별)

### 축② 논리 오류 — 재계산·재유도 (14건 전수, 발견 2건 외 전건 통과)
1. **σ_d 슬롯 규약 ⇔ Ch1 N0 정합**: eq:n0map(ch1_sec01:13-18) σ_d=+1 방전 + "방전 시 ξ 0→1 = 탈리튬화"(:24) ⇒ 흑연 방전↦+1=탈리튬화 ✓; LCO 충전=탈리튬화↦+1 은 동일 물리 내용의 재배선 ✓ (eq:lco-sigmaslot 모순 없음 — 단 M5 의 라벨 관례 함정은 무가드).
2. **(a) 분극 부호**: eq:vn(ch1_sec01:181-183) V_n=V_app−σ_d|I|R_n ⇒ σ_d=+1 에서 V_app=V_n+|I|R_n>V_n ✓ "산화 전류에서 V_app>V_n" 재확인(작동 전극 산화=양극성 과전위) ✓.
3. **(b) 분기 부호·기하**: eq:Ubranch(ch1_sec04:239) U_j^d=U_j+½σ_d h_η γ ΔU^hys ⇒ 탈리튬화 가지 +½(위)·리튬화 −½(아래) ✓; U^dis>U^chg 문구 = ch1_sec04:243 축자 대응 ✓.
4. **spinodal 초과주행 기하**: eq:Veq 미분 dV/dξ=(1/sF)[RT/(ξ(1−ξ))−2Ω]=0 ⇒ ξ_s^±=½(1±u), 극대=ξ_s^−(작은 근)·극소=ξ_s^+ 재유도 ✓ — "탈리튬화는 상승 가지 극대 ξ_s^− 까지, 리튬화는 극소 ξ_s^+ 까지" = ch1_sec04:78-79·fig:hysloop(0.146/0.854, u=√½) 정합 ✓.
5. **(c) 꼬리 적분 방향**: eq:reversal(ch1_sec09:169-179) σ_d=+1: ∫_{−∞}^{V}, σ_d=−1: ∫_{V}^{+∞} ✓ — "하한 −∞ 그대로/상한 +∞ 반전" 서술 정확 ✓.
6. **여집합 교환 재유도**: 1−1/(1+e^{−z})=1/(1+e^{+z}) ⇒ 1−ξ_eq^(σ)=ξ_eq^(−σ) ✓ (eq:xieq 의 z=σ_d(V−U^d)/w 지수 부호 반전 그 자체 ✓); 종 ξ(1−ξ) 불변 ✓; eq:lco-comp(sec17:75-80)와 동형 ✓.
7. **x_MIT=0.85 anchor**: (0.75+0.94)/2=0.845≈0.85 ✓ Ménétrier 2상 창 중점과 정합.
8. **시연값 코드 대조**: Anode_Fit_v1.0.22.py:876/882/886 — U=3.930/3.880/4.050, electronic=True·x_MIT=0.85 는 T1 dict 에만 ✓ 캡션 축자 일치; "전이 구성·순서가 물리 anchor 와 다른 데모"(#2 가 3.880<3.930, #3=곁가지 x≈0.35) ✓.
9. **흑연 전위 창**: tab:staging(ch1_sec10:37-40) 0.085–0.210 V ⇒ "~0.08→0.21 V"·그림 헤더 ✓.
10. **MSMR 5-쌍 대응·유일해**: eq:lco-msmrmap(sec17:87-91) U↔V·U_j^0↔U_j^d·ω_j↔w_j·X_j↔Q_j·f=+σ_d ✓ 미리보기와 1:1; "pairing 하의 유일해" = 계수비교 f/ω_j=σ_d/w_j(sec17:92-95) ✓; "F/RT 를 폭에 흡수" = sec17:18-22·44-51 ✓; 가드 "함수형 동형≠물리량 동일" 실재(sec17:59-60·96-98) ✓.
11. **§lco-center 전달**: eq:lco-dUdT — U_j^cat(T) 함수형·∂U/∂T=ΔS^cat/F 흑연과 동일, 값만 교체 ✓ (:36 서술 정합).
12. **T2/T3 성격·조성**: sec13:105-107 (T2 ~4.05 hex→mono·T3 ~4.17–4.20 mono→hex, x≈0.5 부근) = 표 행 ✓; 0.47@x=½·1.49@x=⅔ tier C·조성 불일치 기록 = 캡션 "값·배정 tier C"·"혼동 가드" 상호 정합 ✓.
13. **ΔS_e 동결 상수 오프셋**: sec17:150-154 "동결 근사 — 선형 U(T), 다온도 T² 곡률은 round-trip 과제" = 캡션 :60-62 ✓; T² 곡률의 물리(S_e∝T ⇒ 자유에너지 −(γ/2)T²) 정합 ✓.
14. **발견으로 귀결**: M4(N1–N5 과소 — N 노드 전수 매핑으로 확인), M8(∂U 표기). 그 외 논리·부호·수치 재계산 **전건 통과**.

### 축① 내용 보완 (빡세게)
- 검토 질문 리스트: 독자가 물을 곳 — (i) "사이클러의 방전 버튼과 이 문서의 '방전'이 같은가?"(흑연 하프셀 — 다름) → **M5**; (ii) "질서상에서 자리 동등·무작위 혼합 가정이 깨지지 않나?" → sec13 §lco-hys-gxi·srcbox(평균장 축약·ECI 대응)가 담당 — §2.1 은 forward-ref(\S\ref{sec:lco-hys-od}) 경유로 도달 가능해 보완 불요 판단(경계 존중 — sec13 은 A18 관할); (iii) "4.05/4.17 쌍의 원전은?" → **M7**; (iv) 기호표 누락 → **M2·M3**; (v) 서두 예고 vs 실제 구성 → **L7**. 4.2 V 컷오프 시 T3(4.17–4.20) 이 상한에 걸린다는 미세 논점은 본문 "$\le$4.2--4.5 V" 범위 표기가 이미 흡수 — 추가 후보로만 기록(집행 제안 아님).
- GS-1/GS-2(정직 공백)는 Ch3 관할 — 본 창 대상 절에 해당 없음. 0.47/1.49 tier C 는 공백 메우기 제안 금지 취지 존중 — 서브 서치도 1차 원전 미확정으로 종결(신규 등재 0건), 본문 현행 유지 지지.
- bgbox 증축분(제거 용이 블록): 대상 3본에 bgbox 없음 — 독립성 이슈 해당 없음.

### 축③ 더 쉬운 설명
- 막힘 후보 전수 점검: "시간상 뒤쪽"(→**L2**), "(tier ---" 미완 괄호(→**L6**), "식이 다섯"(→**L3**), 층위 구분 단락(:114-117 — 이미 명료, 무발견), 평형 종 불변 단락(:119-123 — 식 병기로 자립, 무발견), 그림 캡션(:160-163 — 무발견).

### 축④ 산문→수식 간결화
- 대상 3본은 이미 박스식·표·enumerate 중심 구성 — 산문으로 길게 풀린 유도 없음. 유일 후보 = 전셀 합성 괄호식 정밀화(**M8**). 그 외 **무발견**(축 자체 무발견 아님 — M8 1건).

## 무발견 축 명시 (검토했으나 문제 없음)

| 파일 | 무발견 확정 축 |
|---|---|
| ch2v22_sec00_intro.tex | 논리(재계산 대상 없음·인용 구조 정합)·설명·수식화 — 발견은 보완 L7 뿐 |
| ch2v22_notation.tex | 설명(문장 명료)·수식화 — 발견은 앵커/목록 계열(H1·M1·M2·M3·L1) 뿐 |
| ch1_sec11_lcointro.tex | fig:lco-dirmap TikZ(라벨→탈리튬화→슬롯 화살표 사슬·음영 슬롯 배정·작용처 3항 요약 전수 대조 — 무발견)·표 tab:lco-staging 수치(전 셀 문헌·코드 대조 — 기지 tier C 외 무발견)·여집합/종 불변 수학·세 작용처 부호 전건 |

## P3 게이트 관점 확인 (본 창 대상 범위)

- P3-1(전위 위계): 대상 절은 V_app·V_n 2단만 사용, 위계 일관 ✓ (기호표 계승 누락은 M2 로 보강 제안).
- P3-2(전하 보존 중심식): §2.1 (5)항·eq:sm-mc-balance 계승·sec16 eq:lco-charge 로 중심식 지위 유지 ✓ (OCV 읽기 회귀 없음).
- P3-6(전달식 충돌): sec12(eq:lco-dUdT)·sec13(대입형)·sec16(eq:lco-eqpeak)·sec17(eq:lco-msmrmap) 대조 — §2.1 예고와 충돌 없음 ✓.
- P3-7(명칭): 대상 절에 ver.N 표기 없음 ✓; "Part II" 자칭은 기지 이슈(L5 — 범위 정보 추가, 결정 대기).

## 말미 4-tier

- **확정**(원문 대조·재계산·재유도로 검증): A17-H1, M1, M2, M3, M4, M8, L1, L3 — 및 검증 로그 축② 1~13 전건.
- **추정**(정당 근거 있는 판단 — 채택은 문체·위험 평가 취향 개입): A17-M5(관례 충돌의 실독자 위험 평가), M6(서지 범위 서술의 적정 폭), M7(병기 위치 선택), L2, L4, L6, L7.
- **미검증**(접근 제약 잔여 — 반증 아님): xia2007 전문 내 3.90/4.05/4.17 V 수록 여부(초록 확인 불가 — M7 병기가 보강책); kim_entropymetry2020 수치·motohashi2009 g_max=13(각각 원장 기지·타 창 관할); reimers1992 의 정확 "4.05/4.18" 쌍 표기(~4.07 V feature 까지 확인).
- **기지 이슈**(신규 발견 아님 — 상태 확인만): L5 "Part II" 절 제목(RESUME §5 사용자 결정 대기 — 본 창은 자칭 분포 7회/타 절 0회 범위 정보만 추가); config ΔS 0.47/1.49 tier C(본문 자기 기록·sec13 혼동 가드·원장 정합 — 서브 재서치로도 1차 원전 미확정 재확인).

— 이상. FR-A17 검토 종료 (보고 전용 — 소스 무수정·git 무조작·Codex 미접근 준수).

