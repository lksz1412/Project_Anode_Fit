# A21_REVIEW — v1.0.22 심층 검토 FR-A21 (Ch3 Si 서두 + 기호표 + §3.1 생존 지도)

- 대상: `Claude/docs/v1.0.22/_sections/ch3v22_sec00_intro.tex`(서두, 13행) + `ch3v22_notation.tex`(기호표, 46행) + `ch3v22_sec01_map.tex`(§3.1 생존 지도, 131행)
- 검토 창: FR-A21 (보고 전용 — 본문 무수정·git 무조작·Codex 무접근). 4관점(보완/논리/설명/수식화) 전부 적용.
- 소속 빌드: `ch3_si_v1.0.22.tex`(Ch3 Si·혼합음극) — Ch1·Ch2 라벨은 xr 외부 참조.
- 규율: GS-1(소성 구성식 공백)·GS-2(블렌드 비가산 1차 근사)는 정직 공백 — 메우는 제안 금지(보강·정밀화만). tier 각주·"확인 필요"는 의도된 정직 표기 — 임의 수치 충전 제안 금지.
- 검증 방법: 참조 라벨 전수 역추적(Ch3 로컬 + Ch1/Ch2 aux 대조) · 수치 전건 재계산(Ω=4RT gap·RT/F·Λ_σ 환산) · 앞뒤 절(sec02–05) read-only 원문 대조 · 서지는 하이쿠 서브에이전트 검증(§서치).
- 상태: **본판 v1 (서치 절 통합 완료)** — 수시 저장 방식으로 축차 작성됨.

---

## 0. 발견 색인 (등급순) — 검증 완료분 즉시 추가

| ID | 파일:행 | 유형 | 등급 | 요지 |
|---|---|---|---|---|
| A21-H1 | ch3v22_sec01_map.tex:63–67·88–91 | 논리 | H | 판정 분류 자기모순 — 선언 "네 갈래" vs 표·캡션 "다섯 결"("구조 이월" 정의 없이 사용) |
| A21-M1 | ch3v22_sec00_intro.tex:7–8 | 보완 | M | "Si 분율 0–30%"가 용량 몫임 미명시 — wt% 오독 위험(f=0.3 ↔ 약 4–14 wt%, 재계산) |
| A21-M2 | ch3v22_sec01_map.tex:102–109 | 설명 | M | keybox "host 곱" vs 기호표 "host 합" — 두 층위(분배함수 곱/잔액식 합) 화해 괄호 부재 |
| A21-M3 | ch3v22_sec01_map.tex:79 | 논리(조건부 누락) | M | N3 행 "≈55 mV 로 수백 mV 못 담는다" — Ω 흑연 급(~4RT) 전제 생략(Ω≳10RT 면 식만으로 311 mV — 재계산) |
| A21-M4 | ch3v22_sec00_intro.tex:4–9 | 보완 | M | 서두에 GS-1·GS-2·§3.4·§3.5 도착점 예고 부재(장의 정직 공백 구조 미예고) |
| A21-M5 | ch3v22_notation.tex:9–10 | 보완 | M | "계승분은 값·의미를 바꾸지 않는다" vs 지도 재해석 판정("변수 의미 변경") — 층위 경계 미표시 |
| A21-M6 | ch3v22_notation.tex:32 | 설명 | M | v̄_Li 뜻풀이 "삽입 Li" — 장 테제("삽입 아님·합금화")와 용어 충돌 |
| A21-M7 | ch3v22_sec01_map.tex:116–121 | 보완 | M | "지도가 목차다" 동선에서 N0·N5·N8 누락 — N5 는 §3.2 가 스스로 실증 주장 |
| A21-L1 | ch3v22_notation.tex:33 | 수식화/설명 | L | σ_h 아랫첨자 italic/roman 불일치 + "(경로 의존)" 국면 미한정(탄성 시 단일값) |
| A21-L2 | ch3v22_notation.tex:26 | 보완 | L | ξ host 판 전거 이원화 — 기호표 eq:logisticsolve vs §3.3 eq:sm-logistic |
| A21-L3 | ch3v22_sec00_intro.tex:9 | 설명 | L | 로마자 "blend 합성" — 본문 표준 "블렌드"와 불일치(유일 1회) |
| A21-L4 | ch3v22_sec01_map.tex:88–91 | 보완(전거) | L | 캡션 "전부 이월+전자항 하나" 전거가 tab:lco-staging — 그 캡션에 없는 문구(원문은 §lco-code 제목) |

서지 정정 후보(대상 밖 파일 — §4.3·§7): bib limthongkul2003 DOI 사어(정정 DOI 확정)·ogata_nmr2014 논문번호 4217→3217(원장 동보정).

---

## 1. H 등급 (논리/물리 오류)

### A21-H1 — 판정 분류 자기모순: "네 갈래" 선언 vs 표·캡션의 "다섯 결"("구조 이월" 미정의 사용)
- 파일:행 = `ch3v22_sec01_map.tex:63–67`(선언)·`:81,84`(표의 구조 이월 행)·`:88–91`(캡션) · 유형 = 논리 · 등급 = **H**

현행(축자 — 선언부):
```latex
\subsection{네 판정과 생존 지도}\label{ssec:si-verdicts}
판정은 네 갈래다 --- \textbf{이월}(식$\cdot$부호 그대로) $\cdot$ \textbf{재해석}(형식 유지, 변수 의미
변경) $\cdot$ \textbf{새 물리}(골격에 없는 항 필요) $\cdot$ \textbf{부분}(일부 조건에서만). 이 네 갈래는
흑연$\to$LCO 의 순한 이월(``전부 이월 $+$ 전자항 하나'')보다 결이 많고, 그 다양함 자체가 저장 기작이
바뀔 때 무엇이 견디는지를 보여 준다. 표~\ref{tab:si-survival} 가 노드별 판정이다.
```
현행(축자 — 캡션 해당부):
```latex
\caption{골격 노드의 Si 생존 판정 --- 이월 2(N0$\cdot$N9)$\cdot$구조 이월 2(N5$\cdot$N8)$\cdot$재해석
3(N1$\cdot$N2$\cdot$N4)$\cdot$부분 2(N6$\cdot$N7)$\cdot$새 물리 1(N3). 흑연$\to$LCO 가 ``전부 이월 $+$
전자항 하나''(표~\ref{tab:lco-staging})였던 데 견주면, Si 는 판정이 다섯 결로 갈라진다 --- 저장 기작
전환의 대가다. 근거 문헌은 $\S\ref{ssec:si-stress}$.}
```

제안(완성 LaTeX — 선언부에 구조 이월 정의 문장 삽입, 기존 문구·소절 제목·캡션 보존):
```latex
\subsection{네 판정과 생존 지도}\label{ssec:si-verdicts}
판정은 네 갈래다 --- \textbf{이월}(식$\cdot$부호 그대로) $\cdot$ \textbf{재해석}(형식 유지, 변수 의미
변경) $\cdot$ \textbf{새 물리}(골격에 없는 항 필요) $\cdot$ \textbf{부분}(일부 조건에서만). 이월 중에서도
식의 \emph{형식}은 그대로 살되 미시 해석만 재해석 쪽으로 넘어가는 중간 결은 \textbf{구조 이월}로 따로
표기한다 --- 이월과 재해석 사이의 다섯째 결이며, 표$\cdot$캡션의 ``다섯 결''이 이것이다. 이 갈래들은
흑연$\to$LCO 의 순한 이월(``전부 이월 $+$ 전자항 하나'')보다 결이 많고, 그 다양함 자체가 저장 기작이
바뀔 때 무엇이 견디는지를 보여 준다. 표~\ref{tab:si-survival} 가 노드별 판정이다.
```

근거(검증):
1. 선언부는 판정을 **넷**으로 못박는데(소절 제목 "네 판정"·본문 "판정은 네 갈래다"), 표는 N5·N8 행에 다섯째 범주 **"구조 이월"** 을 정의 없이 사용하고, 캡션은 스스로 "판정이 **다섯 결**로 갈라진다"고 센다(이월 2·구조 이월 2·재해석 3·부분 2·새 물리 1 = 10 노드, 합계는 정확). 같은 절 안에서 선언(4)과 사용(5)이 정면 충돌 — 문서 내부 논리 모순.
2. "구조 이월"은 세 대상 파일 어디에도 선행 정의가 없다(첫 등장 = 표 N5 행). N5 행 자신이 "형식은 생존 — 단 미시 해석은 소멸, 유효 파라미터화로 재해석"이라 적으므로, 이월(식·부호 그대로)과 재해석(의미 변경) 사이의 **중간 결**임이 내용상 분명 — 제안은 그 내용을 선언부에서 명시 정의해 4↔5 충돌을 해소한다(소절 제목 "네 판정"은 기저 4분류로 살아남音 — P5 이름 보존).
3. 참고: §3.1.1 말미(:19–20)의 3분류 예고(산다/재해석/새 물리)는 개괄 프레이밍이라 충돌 아님(부분·구조 이월은 세분) — 수선 불요로 판단.

---

## 2. M 등급 (의미·이해 실질 개선)

### A21-M1 — 서두의 "Si 분율 0–30%"가 용량 몫임을 미명시 (wt% 오독 방지 장치 부재)
- 파일:행 = `ch3v22_sec00_intro.tex:7–8` · 유형 = 보완 · 등급 = M

현행(축자):
```latex
그 위에서 활물질 케이스(원소 Si$\cdot$SiO$_x$$\cdot$Si--C 복합)와 혼합 음극(흑연 다수에
Si 분율 $f_\mathrm{Si}$ 0--30\%)의 검토 틀을 세운다.
```

제안(완성 LaTeX):
```latex
그 위에서 활물질 케이스(원소 Si$\cdot$SiO$_x$$\cdot$Si--C 복합)와 혼합 음극(흑연 다수에
Si 분율 $f_\mathrm{Si}$ 0--30\% --- \emph{용량 몫} $Q_\mathrm{Si}/Q$ 기준, 질량분율 아님: Si 비용량이
흑연의 수 배라 같은 wt\% 보다 용량 몫이 훨씬 크다)의 검토 틀을 세운다.
```

근거(재계산): $f_\mathrm{Si}$ 정의는 용량 몫 $Q_\mathrm{Si}/Q$(기호표 :29·`ch3v22_sec03_blend.tex:73` 동일). 그러나 블렌드 문헌 관행은 wt\% 이고 본문 자신도 wt\% 실측(§3.3: "Si $10$ wt\%"·"고-Si 함량(30 wt\%)")을 인용하므로, 독자가 $f_\mathrm{Si}{=}0.3\leftrightarrow$ "Si 30 wt\%" 로 등치할 위험이 실재. 환산 재계산 — $f=\dfrac{x\,c_\mathrm{Si}}{x\,c_\mathrm{Si}+(1-x)\,c_\mathrm{gr}}$($x$=질량분율, $c_\mathrm{gr}{=}372$ mAh/g): $f{=}0.3$ 은 $c_\mathrm{Si}{=}1000$(표~tab:si-cases 1차 가역)이면 $x{=}13.8$ wt\%, $c_\mathrm{Si}{=}3579$(Li$_{15}$Si$_4$ 이론)이면 $x{=}4.3$ wt\% — 곧 창 $[0,0.3]$ 은 wt\% 로는 약 $0$–$4\sim14$\% 에 불과하고, 역으로 30 wt\% 실측 블렌드는 $f_\mathrm{Si}\approx0.5$ 이상($c_\mathrm{Si}$ 가정에 따라 0.53–0.81)으로 창 밖이다. 이 구분이 세 파일 어디에도 없다(§3.3 도 무설명 병치 — A22 소관 참고). 서두 한 줄이면 독자 질문("30\% 면 상용 고-Si 급인가?")이 차단된다.

### A21-M2 — keybox "host 곱" vs 기호표 "host 합" — 두 층위 화해 괄호 부재
- 파일:행 = `ch3v22_sec01_map.tex:102–109`(keybox) ↔ `ch3v22_notation.tex:24` · 유형 = 설명 · 등급 = M

현행(축자 — keybox):
```latex
\begin{keybox}
\textbf{접목의 앵커.} 내부 전위를 결정하는 \emph{중심 구조}는 흑연$\cdot$LCO$\cdot$Si 에 공통이다 ---
고정 전하에서 반응별 평형 진행률의 용량가중 합을 뒤집어 $U_\oc$ 를 푸는
반전~\eqref{eq:sm-mc-balance}. Si 접목에서 바뀌는 것은 이 구조에 \emph{들어가는 성분}(전이
집합$\cdot$폭$\cdot$히스 항)이지 구조 자체가 아니다. 그래서 $\S\ref{sec:si-blend}$의 혼합 음극도, 두
활물질이 같은 전위 손잡이($\mu$ 하나)를 공유한다는 이 앵커의 \emph{host 곱 한 줄 일반화}로 닫힌다 ---
새 식이 아니라 같은 반전의 한 겹 확장이다.
\end{keybox}
```
현행(축자 — 기호표 host 행):
```latex
$\mathrm{host}\in\{\mathrm{gr},\mathrm{Si}\}$ & \S\ref{ssec:si-blend-derive} & 혼합 음극의 두 활물질 첨자 --- 반전에 얹는 host 합 한 겹. \\
```

제안(완성 LaTeX — keybox 문장에 화해 괄호 삽입, 나머지 불변):
```latex
그래서 $\S\ref{sec:si-blend}$의 혼합 음극도, 두
활물질이 같은 전위 손잡이($\mu$ 하나)를 공유한다는 이 앵커의 \emph{host 곱 한 줄 일반화}로 닫힌다
(분배함수 층은 클래스곱$\to$host 곱, 전하 잔액식 층은 단일 합$\to$host 이중 합 --- 같은 한 줄의 두
층위, \S\ref{ssec:si-blend-derive}) --- 새 식이 아니라 같은 반전의 한 겹 확장이다.
```

근거: 독서 순서상 독자는 기호표에서 "반전에 얹는 **host 합** 한 겹"(:24)을 먼저 만나고, 두 쪽 뒤 keybox 에서 같은 확장이 "**host 곱** 한 줄 일반화"로 불리는 것을 만난다. 해소는 §3.3 에서야 온다 — `ch3v22_sec03_blend.tex:29–46`(eq:blend-factor $\Xi=\prod_\mathrm{host}\prod_j$ = 분배함수 **곱**)과 `:76–77`("다클래스 반전에서 단일 합 $\sum_j$ 를 이중 합 $\sum_\mathrm{host}\sum_j$ 로 바꾼 한 줄" = 잔액식 **합**). 두 용어 모두 §3.3 원문 그대로이므로(P5 보존 — "host 곱"은 §3.3.1 소절 제목이기도 함) 어느 쪽도 바꾸지 않고, 충돌 지점(keybox)에 두-층위 괄호 하나로 전방 화해시키는 제안이다.

### A21-M3 — N3 행 "spinodal gap 상한 ≈55 mV 로 수백 mV 못 담는다" — Ω 앵커 조건 누락(큰 Ω 반론 미차단)
- 파일:행 = `ch3v22_sec01_map.tex:79` · 유형 = 논리(조건부 누락) · 등급 = M

현행(축자):
```latex
N3 히스 & \textbf{새 물리} & $\bigstar$\,\S\ref{sec:si-mech}. spinodal gap 상한(\eqref{eq:dUhys}: $\Omega_j{=}4RT$ 에서 $\approx55$ mV, 그림~\ref{fig:hysgap})으로 수백 mV 를 못 담는다. \\
```

제안(완성 LaTeX):
```latex
N3 히스 & \textbf{새 물리} & $\bigstar$\,\S\ref{sec:si-mech}. spinodal gap 상한(\eqref{eq:dUhys}: 흑연 급 $\Omega_j{\sim}4RT$ 에서 $\approx55$ mV, 그림~\ref{fig:hysgap})으로 수백 mV 를 못 담는다 --- 식만으로 담으려면 $\Omega_j\gtrsim10RT$ 가 필요한데, 실측이 보이는 기작은 이중웰이 아니라 소성$\cdot$응력 결합이다(사실 vi). \\
```

근거(재계산·원문 대조):
1. 수치 검증 — eq:dUhys 무차원형 $g(\hat\Omega)=2[\hat\Omega u-2\,\mathrm{artanh}\,u]$, $u=\sqrt{1-2/\hat\Omega}$($\hat\Omega=\Omega/RT$): $g(4)=2\times(2.8284-1.7629)=2.131$ → $\times RT/F(25.693$ mV$)=54.8\approx55$ mV ✓(Ch1 `fig:hysgap` 자신이 "점 $(4,\,2.131)$" 명기 — `ch1_sec04_hys.tex:219` 정확 일치).
2. 그러나 같은 식은 $\Omega$ 만 키우면 수백 mV 도 낸다: $g(8)=8.59$ → $220.7$ mV, $g(10)=12.11$ → $311$ mV. 곧 "spinodal gap 상한으로 수백 mV 를 못 담는다"는 **$\Omega_j$ 가 흑연 급(~4RT)에 머문다는 전제** 하에서만 성립하는 조건부 명제인데 현행 행은 그 전제를 생략 — "Ω 를 키우면 되지 않나"는 반론이 열려 있다.
3. "흑연 급 $\sim4RT$" 앵커의 근거: 코드 흑연 데모 $\Omega{=}10000$ J/mol $=4.03RT$(`Anode_Fit_v1.0.22.py:1036`)·Ch1 시연 전반이 $\Omega_j{=}4RT$ 기준(fig:hysloop·fig:hysgap). 진짜 배제 논리는 §3.4 원문(`ch3v22_sec04_mech.tex:7–9` "in situ 측정이 보이는 것은 자유에너지 이중웰이 아니라 소성 유동과 응력--전위 결합")처럼 **기작 증거**이므로, 행 안에 그 한 구를 옮겨와 반론을 닫는 제안. 표 행 분량 제약상 한 문장 추가로 처리.

### A21-M4 — 서두에 장의 정직 공백 구조(GS-1·GS-2)와 §3.4·§3.5 도착점 예고 부재
- 파일:행 = `ch3v22_sec00_intro.tex:4–9` · 유형 = 보완 · 등급 = M

현행(축자 — 문단 말미):
```latex
혼합 음극의 앵커는 전하 보존의 전극
중립성이다 --- 두 활물질이 같은 전위 손잡이를 공유하는 전하 보존 반전이 blend 합성의 중심식이 된다.
```

제안(완성 LaTeX — 문단 말미에 한 문장 추가, 기존 문구 불변):
```latex
혼합 음극의 앵커는 전하 보존의 전극
중립성이다 --- 두 활물질이 같은 전위 손잡이를 공유하는 전하 보존 반전이 blend 합성의 중심식이 된다.
닫는 곳과 닫지 못하는 곳은 서두에서 갈라 둔다: 골격 밖 새 물리(기계 히스테리시스)는 Larch\'e--Cahn
결합이 닫히는 데까지만 유도하고(\S\ref{sec:si-mech}), 소성 구성식(GS-1)과 블렌드 비가산(GS-2)은 정직
공백으로 선언하며(\S\ref{ssec:si-lc-gap}$\cdot$\S\ref{ssec:si-blend-gs2}), 살아남은 전부는
\S\ref{sec:si-code} 의 코드 합성 규칙($f_\mathrm{Si}$ 토글)로 모인다.
```

근거: 현행 서두는 지도(§3.1)·케이스(§3.2)·블렌드(§3.3)까지만 예고하고 장의 나머지 절반 — 새 물리 §3.4 와 코드 §3.5, 그리고 이 장의 서명인 두 정직 공백(GS-1·GS-2) — 을 언급하지 않는다. GS 공백은 §3.3.2·§3.4.2 가 각각 4분류까지 갖춰 선언하는 이 장의 핵심 구조물이므로(공백을 **메우는** 것이 아니라 **예고를 보강**하는 제안 — GS 규율 준수), 서두에서 독자에게 "무엇이 닫히고 무엇이 안 닫히는 장인가"를 미리 주면 §3.1 bgbox 의 범위 선언과도 정합한다. 라벨 4종(sec:si-mech·ssec:si-lc-gap·ssec:si-blend-gs2·sec:si-code) 전부 실재 확인.

### A21-M5 — 기호표 "계승분은 값·의미를 바꾸지 않는다" vs 생존 지도의 재해석 판정 — 경계 미표시
- 파일:행 = `ch3v22_notation.tex:9–10` · 유형 = 보완 · 등급 = M

현행(축자):
```latex
(적용 한계는 생존 지도 \S\ref{sec:si-map} 참조)$\cdot$합산식~\eqref{eq:sum}$\cdot$MSMR 대응
(\S\ref{sec:lco-code-msmr}). 이 계승분은 본 장에서 값$\cdot$의미를 바꾸지 않는다.
```

제안(완성 LaTeX):
```latex
(적용 한계는 생존 지도 \S\ref{sec:si-map} 참조)$\cdot$합산식~\eqref{eq:sum}$\cdot$MSMR 대응
(\S\ref{sec:lco-code-msmr}). 이 계승분은 본 장에서 값$\cdot$의미를 바꾸지 않는다(계승 $=$ 형식 정의
기준 --- host 첨자판을 Si 에 적용할 때 폭$\cdot$중심$\cdot$진행률의 \emph{미시 해석}이 옮겨가는 것은
재정의가 아니라 생존 지도 \S\ref{sec:si-map} 의 재해석$\cdot$구조 이월 판정으로 다룬다).
```

근거: 기호표는 "계승분은 값·의미 불변"(:10)·"host 첨자는 재정의 아님"(:17 캡션)이라 선언하는데, 곧이어 §3.1 표는 N2(중심 $U_j$ — "이산 staging 중심 부재")·N4(폭 — "열적 $RT/F$ 가 아님")·N5(진행률 — "미시 해석 소멸")에 **"변수 의미 변경"**(재해석 정의) 판정을 내린다. 두 서술은 층위가 다르므로(형식 정의 계승 vs Si 판 미시 해석) 양립하지만, 그 층위 구분이 명시되지 않아 "의미를 바꾸지 않는다더니 바뀐다는 표가 바로 나온다"는 독자 걸림이 예상된다. 히스 gap 항목에만 있는 헤지("적용 한계는 생존 지도 참조")를 계승 선언 전체로 일반화하는 한 괄호 제안. (구조 이월 용어는 A21-H1 채택 시 정의됨 — 미채택 시 "재해석 판정"으로만 적어도 성립.)

### A21-M6 — 기호표 v̄_Li 뜻풀이 "삽입 Li 부분몰 부피" — 장 테제("삽입 아님·합금화")와 용어 충돌
- 파일:행 = `ch3v22_notation.tex:32` · 유형 = 설명 · 등급 = M

현행(축자):
```latex
$\bar v_\mathrm{Li}$ & \S\ref{ssec:si-lc-derive} & 삽입 Li 부분몰 부피(응력--조성 결합, 골격 밖). \\
```

제안(완성 LaTeX):
```latex
$\bar v_\mathrm{Li}$ & \S\ref{ssec:si-lc-derive} & Li 부분몰 부피 $\partial v/\partial(\text{Li 함량})$(응력--조성 결합, 골격 밖). \\
```

근거: 장 첫 문장이 "실리콘은 **삽입이 아니라 합금화**로 리튬을 저장하므로"(sec00:4–5)이고 §3.1 도 같은 대비를 두 번 반복하는데(:16 "Si 는 삽입이 아니라 \emph{합금화}로"·사실 i "합금화(삽입 아님)"), Si 전용 신규 기호의 뜻풀이가 "삽입 Li"로 적혀 있어 장 자신의 핵심 구분과 정면 충돌 — 주의 깊은 독자가 반드시 걸린다. 제안은 논쟁적 단어를 떼고 §3.4 원문의 정의식($\bar v_\mathrm{Li}\equiv\partial v/\partial(\text{Li 함량})$, `ch3v22_sec04_mech.tex:20`)을 그대로 옮겨 자기완결화한다. 참고(대상 밖 — A23·마스터): §3.4:20 자신도 "Li 삽입의 부분몰 부피"라 쓰므로 채택 시 동보정 후보.

### A21-M7 — §3.1.5 읽는 순서("지도가 목차다")에서 N0·N5·N8 의 동선 누락 — 특히 N5 는 §3.2 가 스스로 실증을 주장
- 파일:행 = `ch3v22_sec01_map.tex:116–121` · 유형 = 보완 · 등급 = M

현행(축자):
```latex
지도의 판정이 곧 이 장의 동선이다. \textbf{재해석$\cdot$부분}으로 표시된 노드(N1$\cdot$N2$\cdot$N4$\cdot$N6$\cdot$N7)는
$\S\ref{sec:si-cases}$의 케이스별 활물질(원소 Si$\cdot$SiO$_x$$\cdot$Si--C 복합)이 실증한다 --- 곡선 개형과
평균 전위, 1차 비가역, 성분 $\ne$ 상전이의 자리.
```

제안(완성 LaTeX — 인용부 뒤에 한 문장 삽입, 이후 문장 불변):
```latex
지도의 판정이 곧 이 장의 동선이다. \textbf{재해석$\cdot$부분}으로 표시된 노드(N1$\cdot$N2$\cdot$N4$\cdot$N6$\cdot$N7)는
$\S\ref{sec:si-cases}$의 케이스별 활물질(원소 Si$\cdot$SiO$_x$$\cdot$Si--C 복합)이 실증한다 --- 곡선 개형과
평균 전위, 1차 비가역, 성분 $\ne$ 상전이의 자리. \textbf{구조 이월}(N5$\cdot$N8)과 나머지
\textbf{이월}(N0)은 별도 절 없이 처리된다 --- N5 는 같은 $\S\ref{sec:si-cases}$의 유효 성분 실증에
얹히고(성분 $=$ 곡선 기술의 실측 근거), N8 은 표~\ref{tab:si-survival} 의 판정 서술로 완결되며, N0 은
$\S\ref{sec:si-code}$ 의 흑연 단독 회수 계약($f_\mathrm{Si}{=}0$)에 흡수된다.
```

근거: "지도의 판정이 곧 이 장의 동선"이라는 강한 주장 아래 현행 동선은 10 노드 중 7(N1·N2·N4·N6·N7 → §3.2, N9 → §3.3, N3 → §3.4)만 배정하고 N0·N5·N8 을 누락한다. 특히 N5 는 §3.2 원문이 "이것이 생존 지도 N5(성분$=$곡선 기술)의 실측 근거다"(`ch3v22_sec02_cases.tex:46–47`)라며 **스스로 실증을 주장하는 노드**라 누락이 두드러진다. N8 은 Ch3 어느 절도 다루지 않으므로(전 절 grep 무출현) "표의 판정 서술로 완결"이 정직한 배정이고, N0 은 §3.5 의 $f_\mathrm{Si}{=}0$ bit-exact 계약(`ch3v22_sec05_code.tex:10–21`)이 흑연 규약 그대로를 보존함으로써 소화된다.

---

## 3. L 등급 (문체·소소)

### A21-L1 — 기호표 σ_h 행: 아랫첨자 조판 불일치(italic h) + "(경로 의존)" 뜻풀이의 국면 미한정
- 파일:행 = `ch3v22_notation.tex:33` · 유형 = 수식화/설명 · 등급 = L

현행(축자):
```latex
$\sigma_h$ & \S\ref{ssec:si-lc-derive} & 정수압(평균) 응력 $\tfrac13\mathrm{tr}\,\bm\sigma$(경로 의존). \\
```

제안(완성 LaTeX):
```latex
$\sigma_\mathrm{h}$ & \S\ref{ssec:si-lc-derive} & 정수압(평균) 응력 $\tfrac13\mathrm{tr}\,\bm\sigma$(소성 시 경로 의존 --- \S\ref{ssec:si-lc-gap}). \\
```

근거: (i) 같은 표 :35 행($\sigma_\mathrm{h}^{\dis}$)·기호표 말미 :41($\sigma_\mathrm{h}$)·§3.4 전문(eq:si-lcmu~eq:si-plastic 전부 $\sigma_\mathrm{h}$)이 로마체 아랫첨자인데 이 행만 이탤릭 $\sigma_h$ — 같은 기호의 두 조판이 인쇄된다. (ii) "(경로 의존)"은 정의 속성이 아니라 국면 속성: §3.4 원문이 "변형이 순수 탄성이라면 $\sigma_\mathrm{h}$ 가 $\theta$ 의 단일값 함수"(`ch3v22_sec04_mech.tex:72–73`)라 명시하므로 경로 의존은 **소성일 때**(GS-1 국면)의 성질이다. 국면 한정 + GS-1 소절 포인터로 정밀화.

### A21-L2 — 기호표 ξ 행의 계승 전거가 §3.3 인용 전거와 이원화(eq:logisticsolve vs eq:sm-logistic)
- 파일:행 = `ch3v22_notation.tex:26` · 유형 = 보완 · 등급 = L

현행(축자):
```latex
$\xi_{\eq,j}^{\mathrm{host}}$ & \S\ref{ssec:si-blend-derive} & host 의 전이 $j$ 평형 진행률(\eqref{eq:logisticsolve} 의 host 판). \\
```

제안(완성 LaTeX):
```latex
$\xi_{\eq,j}^{\mathrm{host}}$ & \S\ref{ssec:si-blend-derive} & host 의 전이 $j$ 평형 진행률(\eqref{eq:logisticsolve}$\cdot$\eqref{eq:sm-logistic} 의 host 판). \\
```

근거: 기호표는 host 진행률의 원형을 eq:logisticsolve(Ch1 §1.5 — detailed balance 유도판, `ch1_sec05_width.tex:37`)로, §3.3(d) 본문은 eq:sm-logistic(Ch1 Part 0 — 결선 유도판, `ch1_sec02b_part0.tex:192`)로 각각 건다. 두 식은 같은 bare logistic 이라 오류는 아니나(내용 대조 완료 — 동형), 독자가 기호표→§3.3 를 오가며 전거가 갈리는 것을 보게 된다. 두 라벨 병기로 일원화(대안: §3.3 쪽을 eq:logisticsolve 로 통일 — A22 소관이라 기호표 쪽 병기를 제안).

### A21-L3 — 서두의 로마자 "blend 합성" — 본문 표준 표기 "블렌드"와 불일치
- 파일:행 = `ch3v22_sec00_intro.tex:9` · 유형 = 설명(표기 통일) · 등급 = L

현행(축자):
```latex
중립성이다 --- 두 활물질이 같은 전위 손잡이를 공유하는 전하 보존 반전이 blend 합성의 중심식이 된다.
```

제안(완성 LaTeX):
```latex
중립성이다 --- 두 활물질이 같은 전위 손잡이를 공유하는 전하 보존 반전이 블렌드 합성의 중심식이 된다.
```

근거: 세 대상 파일 + §3.3 전체에서 로마자 "blend"는 이 1회뿐(grep 확인 — sec00:4 "혼합(블렌드) 음극"·§3.3:5 "혼합(블렌드) 음극"·기호표 :30 "블렌드 배경" 등 나머지 전부 "블렌드"). 표기 통일.

### A21-L4 — 캡션의 스케어 인용 "전부 이월 + 전자항 하나"의 전거 배치 — 그 문구는 tab:lco-staging 캡션에 없음
- 파일:행 = `ch3v22_sec01_map.tex:88–91`(캡션) · 유형 = 보완(전거 정밀) · 등급 = L

현행(축자):
```latex
\caption{골격 노드의 Si 생존 판정 --- 이월 2(N0$\cdot$N9)$\cdot$구조 이월 2(N5$\cdot$N8)$\cdot$재해석
3(N1$\cdot$N2$\cdot$N4)$\cdot$부분 2(N6$\cdot$N7)$\cdot$새 물리 1(N3). 흑연$\to$LCO 가 ``전부 이월 $+$
전자항 하나''(표~\ref{tab:lco-staging})였던 데 견주면, Si 는 판정이 다섯 결로 갈라진다 --- 저장 기작
전환의 대가다. 근거 문헌은 $\S\ref{ssec:si-stress}$.}
```

제안(완성 LaTeX):
```latex
\caption{골격 노드의 Si 생존 판정 --- 이월 2(N0$\cdot$N9)$\cdot$구조 이월 2(N5$\cdot$N8)$\cdot$재해석
3(N1$\cdot$N2$\cdot$N4)$\cdot$부분 2(N6$\cdot$N7)$\cdot$새 물리 1(N3). 흑연$\to$LCO 가 ``전부 이월 $+$
전자항 하나''(\S\ref{sec:lco-code} 요약 --- 파라미터 대응은 표~\ref{tab:lco-staging})였던 데 견주면,
Si 는 판정이 다섯 결로 갈라진다 --- 저장 기작 전환의 대가다. 근거 문헌은 $\S\ref{ssec:si-stress}$.}
```

근거: "전부 이월 $+$ 전자항 하나"는 Ch2 어디에도 축자 부재(Ch2 전 파일 grep 0건 — 본 장이 만든 압축 표어). 반면 괄호 전거가 표~tab:lco-staging 로 걸려 있어 그 캡션에 이 문구가 있는 것으로 오독된다 — 실제 캡션 문구는 "흑연 표~\ref{tab:staging} 와 같은 자리(전위$\cdot$성격$\cdot\Delta S$), 양극 부호"(`ch1_sec11_lcointro.tex:56`)로 **파라미터 슬롯 대응**만 말한다. 표어의 실질 원문은 §\ref{sec:lco-code} 제목 괄호 "(파라미터 교체 $+$ 전자항 추가)"(`ch1_sec17_msmr.tex:4`)이므로 전거를 그쪽에 앵커하고 표는 파라미터 대응 보조로 강등하는 제안. (:65–66 첫 사용부는 전거 괄호가 없어 스케어 표어로 읽힘 — 수선 불요 판단.)

---

## 4. 서치 절 — 하이쿠 서브에이전트 서지 검증 (기억 서지 금지·검증분만)

방법: 하이쿠 서브 2기(H-A = 사실 i–v 7키 / H-B = 사실 vi–viii·계보 7키) — doi.org 리졸브 + Crossref API 필드 대조 + 초록(Crossref 노출분) 수준 내용 대조. 하이쿠가 보고한 이상 2건(ogata 번호 불일치·limthongkul 404)은 본 창이 Crossref 직접 재조회로 재확인·정정 DOI 탐색까지 수행. **아래 표는 실제 리졸브·대조된 검증분만** 싣는다.

### 4.1 H-A 결과 (사실 i–v 의 7키)

| key | DOI 리졸브 | 필드 대조 | 내용 주장 확인 수준 | 판정 |
|---|---|---|---|---|
| wen_huggins1981 | ✓ | JSSC **37**(3) 271–278 (1981) 전 필드 일치 | 제목("intermediate phases in the lithium-silicon system")이 중간상 titration 주장 지지 — "네 중간상" 수는 초록 밖(미검증분) | 일치 |
| limthongkul2003 | **인쇄 DOI 404**(하이쿠 보고 → 본 창 재확인: doi.org·Crossref 공히 실패) | Crossref 서지 검색으로 진짜 DOI 확정: **10.1016/S1359-6454(02)00514-1** = "Electrochemically-driven solid-state amorphization in lithium-silicon alloys and…", *Acta Materialia* **51**(4) 1103–1113 (2003), doi.org **200** 리졸브 — 제목·저널·권·호·쪽·연도가 bib 여타 필드와 전건 일치 | 제목이 고상 비정질화 주장 직접 지지 | **bib DOI 오기 확정**(`ch3v22_bib.tex:7` 의 `10.1016/S1359-6454(02)00515-4` → `00514-1` 정정 후보 — 대상 밖 파일이라 발견표 아닌 본 절+§7 이관) |
| li_dahn2007 | ✓ | JES **154**(3) A156 (2007) 일치 | 제목(in situ XRD, crystalline Si)이 두-상 반응 지지 — "날카로운 이동 경계" 문구는 제목 수준 | 일치 |
| obrovac_christensen2004 | ✓ | ESSL **7**(5) A93 (2004) 일치 | 제목 수준(구조 변화) — "≈50 mV"·Li$_{15}$Si$_4$ 명명은 초록 밖(미검증분) | 일치(수치는 미검증분) |
| ogata_nmr2014 | ✓(DOI 10.1038/ncomms4217 정상) | 제목·권(5)·연도(2014) 일치 — 단 **Crossref article-number = 3217**(본 창 직접 재확인: volume 5·article-number 3217·issued 2014-02-03) vs bib "5, 4217" | 제목(in situ NMR, lithium-silicide phase transformations)이 operando 추적 주장 지지 | **bib 논문번호 오기 확정**(`ch3v22_bib.tex:24` "5, 4217"→"5, 3217" 정정 후보 — Nat. Commun. 이 시기는 DOI 접미사(ncomms4217)와 논문 번호(3217)가 다른 체계. `V1022_REFERENCE_LEDGER.md:13` 에도 동일 오기 전파 — §7) |
| chevrier_dahn2009 | ✓ | JES **156**(6) A454 (2009) 일치 | 제목(First Principles, Amorphous Silicon Lithiation)이 지지 — "plateau 없는 경사 재현" 문구는 제목 수준 | 일치 |
| beaulieu2001 | ✓ | ESSL **4**(9) A137 (2001) 일치 | 제목("Colossal Reversible Volume Changes")이 거대 부피 변화 지지 — "~300%" 수치는 초록 밖(미검증분) | 일치(수치는 미검증분) |

### 4.2 H-B 결과 (사실 vi–viii·계보의 7키)

| key | DOI 리졸브 | 필드 대조 | 내용 주장 확인 수준 | 판정 |
|---|---|---|---|---|
| sethuraman_stressevo2010 | ✓ | JPS **195**(15) 5062–5066 (2010) 전 필드 일치 | 제목(in situ stress evolution, lithiation/delithiation) 지지 — "$\sim-1.75$ GPa" 수치는 초록 미노출(미검증분) | 일치(수치는 미검증분) |
| sethuraman_stresspot2010 | ✓ | JES **157**(11) 2010 일치·Crossref 시작쪽 **A1253** 확보(끝쪽 페이월 미확인) — bib 자신이 "쪽 범위는 사용 시 Crossref 최종 대조"로 정직 표기, 원장 잔여 확인필요(쪽) 항목의 시작쪽은 이번에 확보 | 제목(Stress-Potential Coupling) 지지 — "$\sim$100–120 mV/GPa" 수치는 초록 미노출(미검증분) | 일치(수치·끝쪽은 미검증분) |
| liu_sizefracture2012 | ✓ | ACS Nano **6**(2) 1522–1531 (2012) 전 필드 일치 | 제목(Size-Dependent Fracture) 지지 — "$\sim$150 nm" 는 초록 미노출(미검증분) | 일치(수치는 미검증분) |
| verbrugge_lisi2016 | ✓ | JES **163**(2) A262–A271 (2016) 전 필드 일치(Crossref 온라인 2015/인쇄 2016) | 제목이 "Multiple Electrochemical Reactions and Associated Speciation … Lithium-Silicon Electrode" — 사실 viii 문구 직접 지지. **저자 Verbrugge·Baker·Xiao 확인** → §3.1.4 "MSMR 대응과 같은 저자 계보" 주장 성립(msmr_origin2017 저자와 3인 공통) | **일치(강)** |
| obrovac_chevrier2014 | ✓ | Chem. Rev. **114**(23) 11444–11502 (2014) 전 필드 일치 | 제목(Alloy Negative Electrodes) — 총람 리뷰 인용 위치 적절 | 일치 |
| koebbing2024 | ✓ | AFM **34**(7) 2308818, 온라인 2023-11/인쇄 2024-02 — 원장 해소 기록과 정합 재확인 | **Crossref 초록에서 직접 지지**: "plastic deformation of the stiff, inorganic SEI"·"visco-elastoplastic behavior" — 본문 "소성$\cdot$SEI 점탄소성 모델" 문구와 정확 정합 | **일치(강)** |
| jiang_sihys2020 | ✓ | JES **167**(13) 130533 (2020) 전 필드 일치 | **Crossref 초록에서 직접 지지**: "multi-step phase transformations, crystallization and amorphization … during cycling" — 본문 "다단 상전이 경로분기 모델" 문구와 정확 정합 | **일치(강)** |

### 4.3 종합
- 14키 전건: DOI 리졸브 13건 성공 + 1건(limthongkul2003)은 **인쇄 DOI 자체가 사어**(정정 DOI 는 200 리졸브·전 필드 정합 확인). 신규 문헌 등재 필요 없음(세 파일의 서지 수요는 기존 bib 키로 충족 — 원장 규율상 신규 키 불요).
- **확정 정정 후보 2건(대상 밖 파일 — 마스터 이관)**: ① `ch3v22_bib.tex:7` limthongkul2003 DOI `…00515-4` → `…00514-1` ② `ch3v22_bib.tex:24` ogata_nmr2014 "5, 4217" → "5, 3217"(+ `V1022_REFERENCE_LEDGER.md:13` 동보정).
- 본문 수치 주장 5건($-1.75$ GPa·100–120 mV/GPa·150 nm·$\approx$50 mV·$\sim$300%)은 제목/초록 수준 방향 일치까지 — 원문 본문 수치의 직접 대조는 페이월로 미검증분(4-tier 분리). 이는 본문·bib 가 이미 tier 표기로 다루는 지위와 상충 없음.

---

## 5. 무발견 축 (검토했으나 문제 없음 — 검증 방법 명세)

1. **참조 라벨 무결성(전수)**: 세 파일의 \ref/\eqref 대상 전수 역추적 — Ch3 로컬 10종(sec:si-cases·tab:si-cases·sec:si-blend·ssec:si-blend-derive·sec:si-mech·ssec:si-lc-derive·eq:si-coupling·ssec:si-lc-gap·sec:si-code·ssec:code-caseset)은 `ch3v22_sec02~05.tex` 에 전부 정의(중복 없음), xr 18종(eq:sm-mc-balance·eq:sm-mc-fluc·eq:logisticsolve·sec:width·sec:center·eq:dUhys·eq:sum·sec:pol·sec:sum·sec:eqpeak·sec:broadening·sec:lag·sec:tail·sec:sm-mc·fig:hysgap = Ch1 aux 각 1회 / sec:lco-code-msmr·sec:lco-code·tab:lco-staging = Ch2 aux 각 1회)은 소속 장 정확·중복 없음. `ch3_si_v1.0.22.log` undefined reference 0건(폰트 warning 제외). si_case 도입 절 표기(\S ssec:code-caseset = sec05:31 "Si 케이스 셋 --- si\_case 선택자")·응력 기호군 도입 절(ssec:si-lc-derive = sec04:15) 배정 정확.
2. **기호표 신규 행 전건 원문 대조(§3.3·§3.4·§3.5 정의부와 1:1)**: $Q_j^{\mathrm{host}}\equiv(F/N_A)M_j^{\mathrm{host}}$(= sec03:62 축자)·$Q{=}Q_\mathrm{gr}{+}Q_\mathrm{Si}$(= sec03:63,73)·$f_\mathrm{Si}{=}Q_\mathrm{Si}/Q\in[0,0.3]$(= sec03:73·sec05:24 배분식 정합)·$C_\bg$ 전극당 1회 가산(= sec03:119–120 "host 별 중복 가산 금지" 동일 규약)·\code{si\_case} 3값(= sec05:32 동일)·$\Lambda_\sigma\equiv\partial V/\partial\sigma_\mathrm{h}=\bar v_\mathrm{Li}/F$·$\Delta V^\mathrm{mech}=\Lambda_\sigma(\sigma_\mathrm{h}^{\dis}{-}\sigma_\mathrm{h}^{\chg})$(= eq:si-coupling 축자) — 전건 일치. $\sim$100–120 mV/GPa 괄호는 §3.4 verifybox 의 tier-A 실측 범위 인용과 동일(§3.4 가 $\bar v_\mathrm{Li}$ 수치 산출을 "확인 필요"로 남긴 규율도 침해 없음 — 본 보고 제안 중 그 공백을 수치로 메우는 것 없음).
3. **계승 선언 원문 대조(Ch1/Ch2 원형 확인)**: 전하 보존 반전(eq:sm-mc-balance = $\sum_jQ_j\xi_{\eq,j}(U_\mathrm{oc},T)=Q\bar x$)·요동 유일근(eq:sm-mc-fluc = $\partial\langle N\rangle/\partial\mu=\beta\sum M_j\theta_j(1-\theta_j)>0$)·평형 진행률 logistic(eq:logisticsolve — detailed balance 정지점 유도, `ch1_sec05_width.tex:25–45`)·폭 $RT/F$ 척도(동 파일 — N4 행 "$\sim$26 mV" = 25.69 mV@298.15 K 재계산 일치)·$\partial U_j/\partial T=\Delta S_{\rxn,j}/F$(`ch1_sec03_center.tex:60,92,100` 동형 — 기호표는 $j$ 생략 표기이나 관계식 동일)·합산식 eq:sum·MSMR 대응 sec:lco-code-msmr — 전부 원형 확인, 재정의 없음 확인(2단 규약 준수).
4. **§3.1.4 앵커 서술의 원문 정합**: "반응 몫의 합 $=$ 통과 전하"(map:97) = sm-mc(d) 원문 "$Q\bar x=\sum_jQ_j\xi_j$"·"통과 전하($\bar x$)를 고정하고 그에 맞는 전위를 푼다" 정확 대응. "같은 저자 계보의 Si 판"(map:100) = verbrugge_lisi2016 저자(Verbrugge·Baker·Xiao) ∩ MSMR 원전(msmr_origin2017: Verbrugge·Baker·Koch·Xiao·Gu) — Verbrugge·Baker·Xiao 3인 공통, 계보 주장 성립. "진짜 이산 전이는 둘뿐"(map:113–114) = 사실 ii(1차 리튬화 두-상)·iii(Li$_{15}$Si$_4$) 및 §3.2 케이스 서술(sec02:39–47)과 정합, §3.5 도 같은 경고를 코드 주석 요구로 수신(sec05:35–36).
5. **N0–N9 노드 명명·사슬 대응(P3-7 계열)**: Ch1 원전 확인 — "한 번만 실행되는 두 노드 N0·N1 … 전이 루프 N2–N9"(`ch1_sec00_intro.tex:15–16`). §3.1.1 의 10항 나열(조건 규약~합산)이 N0~N9 와 1:1, 표 행 명칭(N0 조건·N1 분극·N2 중심·N3 히스·N4 폭·N5 $\xi_\eq$·N6 peak·N7 broadening·N8 지연·N9 합산)과 캡션 집계(2+2+3+2+1=10) 상호 일치. "ver.N" 역사 명칭은 세 파일에 등장하지 않음 — 혼동 없음.
6. **"N1–N5 구간에서 같은 식 공유"(map:12–13)**: Ch2 원문 축자 대조 — `ch1_sec11_lcointro.tex:83` "N1--N5 구간에서 흑연과 LCO 는 \emph{같은 식}을 공유하므로" 그대로 수신 ✓. "같은 식, 파라미터만 교체, 전자 엔트로피 항 하나 추가"(map:10–11)는 §sec:lco-code 제목 괄호 "(파라미터 교체 $+$ 전자항 추가)"(`ch1_sec17_msmr.tex:4`)의 충실 의역 ✓. tab:lco-staging 캡션 인용(map:11–12 "흑연 표와 같은 자리(전위$\cdot$성격$\cdot\Delta S$), 양극 부호")은 원문(`ch1_sec11_lcointro.tex:55–56` "흑연 표~\ref{tab:staging} 와 같은 자리…")에서 표 지시 "~\ref{tab:staging}" 만 생략한 실질 축자 — 인쇄상 "표 1.N 와"→"표와" 차이뿐이라 무해 판정(별건 없음; 캡션 전거 배치 문제는 A21-L4 로 분리).
7. **N3 행 수치 재계산(무차원 gap)**: $g(\hat\Omega)=2[\hat\Omega u-2\,\mathrm{artanh}\,u]$ 재유도 — $g(4)=2.131$(Ch1 fig:hysgap 명기점 "(4, 2.131)"과 소수 3자리 일치), $\times25.693$ mV $=54.8\approx55$ mV ✓. eq:dUhys 원형(`ch1_sec04_hys.tex:96`: $-\tfrac{4RT}{sF}\mathrm{artanh}\,u_j+\tfrac{2\Omega_j}{sF}u_j$)과 코드 구현(`Anode_Fit_v1.0.22.py:144–147`: `(2/F)*(Omega*u - two_RT*arctanh(u))`) 삼중 일치. "spinodal 상한" 용어도 Ch1 확립 용어(`ch1_sec04_hys.tex:80,245`) ✓ (조건부 서술 누락만 A21-M3).
8. **N4·N5·N7·N8 행의 Ch1 귀속 정확성**: N4 — $RT/F$ 폭 척도·$w_j=n_jRT/F$ 다중도 일반화는 §1.5 원문 그대로. N5 — "(detailed balance 전극 무관)" = eq:logisticsolve 실제 유도 경로(`ch1_sec05_width.tex` "열역학은 detailed balance 한 곳으로만 들어왔고") 정확 귀속 ✓. N7 — "입자 간 순차"(Dreyer 순차 전환, `ch1_sec07_broadening.tex:70` "순차로 한 입자씩 전환")·"흑연에서 정량 배제됐던 입자-크기 채널"(동 파일 :106 "입자 크기$\cdot$전극 형상과 무관한 상수로 주므로 … 산포 $\approx0$") 전건 원문 확인 ✓. N8 — "꼬리 소멸" = `ch1_sec09_tail.tex:143`($|I|\to0\Rightarrow L_{V,j}\to0$), "잔여 갈림 $=$ 평형 분기" 논법 = `ch1_sec06_eqpeak.tex:30–32`($\gamma_j\ne0$ 이면 $|I|\to0$ 극한은 분기 중심에 남는 히스 잔존 극한) — 축자 문구는 아니나 스케어 인용으로 읽히는 실질 논법이 Ch1 에 실재 ✓; Si 에서 기계 히스가 $|I|\to0$ 에 잔존해 그 논법이 약해진다는 판정도 소성(율속 무관·경로 의존) 성질과 정합 ✓.
9. **사실 (i)–(viii) ↔ 노드 대응의 내적 정합**: 각 사실의 노드 화살(i→N2·N5, ii→N6·N7, iii→N6, iv→N2, v→N1·N3, vi→N3, vii→N7, viii→N9)이 표 판정·§3.1.4–3.1.5 서술과 모순 없음. 사실 vi 의 수치 조합 자기일치 재계산 — 결합 ~0.10–0.12 V/GPa × 응력 스윙 $|{-}1.75|+O(1)$ GPa ≈ 0.3 V = "수백 mV" 주장과 규모 정합 ✓.
10. **혼합·코드 예고의 하위 절 정합**: 서두·keybox·guide 의 blend 예고(공통-$\mu$·host 확장·GS-2 한계)가 §3.3 실제 구조(eq:blend-factor/occ/balance/limit/dqdv·verifybox 3건·GS-2 4분류)와, guide 의 §3.5 예고(f_Si 토글)가 sec05 게이트(G1 bit-exact·G2 스윕·G3 용량 보존)와 전건 일치. GS-1/GS-2 는 세 파일 어디서도 "메워질 수 있는 것"으로 서술되지 않음 — 정직 공백 지위 보존 확인(본 보고의 전 제안도 공백 충전 없음 — M4 는 예고 보강일 뿐).
11. **P3 게이트 관점**: P3-1(V 위계) — 세 파일의 전위 기호는 $V_n$(N1 행)·$U_\oc$(keybox)·$U_j$ 뿐, $V_{n,\mathrm{app}}$/$V_{n,\mathrm{drive}}$ 층위 혼용 없음 ✓. P3-2(전하 보존 중심식 유지) — keybox·N9 행·서두 전부 반전 중심 서술, OCV 읽기 회귀 없음 ✓. P3-3(순환 의존) — 새 순환 도입 없음(반전의 implicit 지위는 §3.3 이 "정의상 implicit formulation"으로 분류 — 4분류 준수) ✓. P3-6(전달식 충돌) — 계승 목록·생존 판정 간 충돌 없음(층위 미표시 걸림만 A21-M5) ✓.
12. **조판·매크로**: \oc·\eq·\bg·\rxn·\dis·\chg·\hys·\code 매크로 전부 `common_preamble_v1022.tex` 정의 확인($U_\oc$=$U_\mathrm{oc}$ 동일 렌더 — §3.3 표기와 실질 일치). bgbox/keybox 환경 사용 적법. 기호표 tabular 열 합계 0.185+0.115+0.60=0.90\textwidth — 오버플로 없음(빌드 log 심각 경고 0). σ_h 이탤릭 1건만 예외(A21-L1).

---

## 6. 말미 4-tier 분류

- **확정**(재계산·원문 대조·실조회로 닫힘): A21-H1(선언 4 vs 사용 5 — 세 파일 내 자기충돌·"구조 이월" 무정의 첫 사용), A21-M3 의 수치부($g(4){=}2.131{=}54.8$ mV — Ch1 그림 명기점·코드 구현과 삼중 일치; $g(10){=}12.11{=}311$ mV), A21-M1 의 환산부($f{=}0.3\leftrightarrow4.3$–$13.8$ wt\%), A21-L1 의 조판 사실(동일 기호 두 조판), A21-L3(로마자 1회 유일), A21-L4 의 사실부("전부 이월…" 문구 Ch2 전 파일 grep 0건·tab:lco-staging 실제 캡션 문구 확인), 서지 정정 2건(limthongkul 인쇄 DOI 404 + 정정 DOI 200·전 필드 정합 / ogata Crossref article-number 3217), 무발견 축 1–12 전건.
- **추정**(개선 이득 판단에 주관 — 채택은 마스터 몫): A21-M1·M2·M4·M5·M6·M7 의 보강 필요성과 문안, A21-L1 의 "(소성 시)" 한정 문안, A21-L2 병기안, A21-M3 의 행내 한 문장 추가가 표 폭에 주는 부담(대안: 각주화), A21-H1 의 수선 위치(선언부 정의 방식 — 캡션 쪽 수선 대안도 가능하나 선언부가 최소 침습).
- **미검증**(접근 한계 — 정직 표기): (i) 수치 주장 5건($-1.75$ GPa·100–120 mV/GPa·$\sim$150 nm·$\approx$50 mV·$\sim$300%)의 원문 본문 수치 직접 대조(제목/초록 방향 일치까지만 — 본문·bib 의 tier 표기 지위와 상충 없음), (ii) wen_huggins1981 의 "네 중간상" 개수의 원문 대조(제목 수준), (iii) sethuraman_stresspot2010 끝쪽(A1261 여부 — 시작쪽 A1253 은 확보), (iv) verbrugge_lisi2016 본문 수식 구조(반응별 logistic 용량가중 합)의 식 단위 대조(제목·저자 수준 강지지까지).
- **무발견 축**: §5 의 1–12(각 항목에 검토 방법 명기 — xr 라벨 전수·기호표 전 행 원문 1:1·N0–N9 명명·N1–N5 인용 축자·수치 삼중 재계산·P3 게이트 관점·GS 공백 존중 전건).

---

## 7. 부수 관찰 (대상 밖 — 마스터·담당 창 참고용, 발견표 밖)

1. **`ch3v22_bib.tex:7`(limthongkul2003)**: 인쇄 DOI `10.1016/S1359-6454(02)00515-4` 는 doi.org·Crossref 공히 404(사어). 정정 DOI = `10.1016/S1359-6454(02)00514-1`(*Acta Materialia* **51**(4) 1103–1113, 2003 — doi.org 200·전 필드 bib 여타 표기와 일치). v1.0.21 원장 V1 승계분(`V1021_REFERENCE_LEDGER.md:32`)이라 원장 계보에도 소급 메모 요망.
2. **`ch3v22_bib.tex:24`(ogata_nmr2014)**: "Nat. Commun. **5**, 4217" → 논문번호는 **3217**(Crossref article-number; DOI 접미사 ncomms4217 과 다른 것이 이 시기 Nat. Commun. 정상 체계). `V1022_REFERENCE_LEDGER.md:13` 의 "5 4217 (2014)"도 동일 오기 — 동보정 후보.
3. **`ch3v22_sec05_code.tex:7`**: "재해석 노드(N2$\cdot$N4$\cdot$N6)" — 표~tab:si-survival 판정은 N6 $=$ **부분**(재해석은 N1·N2·N4). A23 창 소관 확인 요망(코드 절이 N6 를 재해석으로 오분류 — 본 절 H1 계열의 여파 점검 겸).
4. **`ch3v22_sec04_mech.tex:20`**: "Li 삽입의 부분몰 부피" — A21-M6 채택 시 동보정 후보(A23 소관).
5. **`ch3v22_sec03_blend.tex:66–67`**: ξ host 판 전거가 eq:sm-logistic — A21-L2 의 통일 대안 지점(A22 소관).
6. **GS-2 실측 창 대비**: §3.3 GS-2 srcbox 의 "고-Si 함량(30 wt\%)" 실측은 용량 몫으로 $f_\mathrm{Si}\approx0.5$ 이상(비용량 가정 따라 0.53–0.81) — 모델 창 $[0,0.3]$ 밖의 증거로 쓰이고 있음(공백 선언 근거로는 유효하나, A22 검토 시 창 안팎 구분 한 줄 여지 — A21-M1 과 같은 계열).

---

**상태: 본판 v1 완성** — 검토 4관점 전부 적용·발견 12건(H1·M7·L4) + 서지 정정 후보 2건(대상 밖)·무발견 축 12·서치 절 통합(하이쿠 2기 + 본 창 재검 2건). 보고 전용 규율 준수: 소스 무수정·git 무조작·Codex 무접근·GS-1/GS-2 충전 제안 없음·"확인 필요" 수치 충전 제안 없음.
