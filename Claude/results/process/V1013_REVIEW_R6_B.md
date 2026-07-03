# V1.0.13 P5 검수 라운드 6 — 검수자 B (수식-주도 렌즈 + 압축 이월 판정)

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` **Part II(L1836–2951)** 전문 정독(1836→끝, coverage missing 0). 이월 판정을 위해 ch1 sec:dist(L1257–1292)·ch2(`graphite_ica_ch2_v1.0.13.tex` L578–608·L715–732)·압축 기록 p3/p4 전문·커밋 377b5e6/1bb914c/4f1ab12 diff 를 추가 정독.
- 원칙: 검수 의견만(tex/코드 수정 0). 모든 지적 = 현행 줄번호 + 원문 인용 + 수정문 전문. refute mandate 이행(말미 오적발 자기표시).
- 청크 스킴: 문단(산문 블록) 단위 — Part II 산문 블록 70개 전수. 렌즈 = ① 식 없는 3문장+ 문단 ② 재진술 잔존 ③ R1–R5 정정 재팽창 ④ 괄호 보충 전보체 ⑤ orphan-0 확인 후 삭제.

---

## 과업 1 — 수식-주도 판정 (지적 19건: MED 9 · LOW 10 · HIGH 0)

물리·부호·수치 결함은 0 — 아래는 전부 산문 중복·전보체·재팽창 결함이며, 사용자 원 지적 "LCO 는 말이 너무 많다"의 잔존 지점 재실측이다.

### F1 [MED·②] sec:lco-map 닫는 문단 첫 문장 = 도입문 재진술
- 위치: L1860. 원문: "이 골격이 LCO 양극에 걸리는 근거 목록이 위 다섯이다."
- 판정: L1847–1848 도입 "본론 사슬에서 host 물질이 들어가지 않는 식이 다섯이다"가 이미 같은 명제. enumerate 직후 동일 내용 재확인 — 재진술 잔존.
- 수정문: 해당 문장 삭제, 문단을 "흑연 서술은 한 줄도 바뀌지 않으며(모든 흑연 식$\cdot$표$\cdot$부호는 불변), …"로 시작. orphan: "근거 목록" 후방 참조 없음 — 안전.

### F2 [LOW·②] lco-map 부호 문단의 ∂U/∂T 선취 — lco-center (d)와 중복
- 위치: L1871–1872. 원문: "평형 중심의 온도 의존 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$(식~\eqref{eq:Uj} 미분)는 부호까지 흑연과 동일한 관계식이며, 부호의 \emph{값}만 전이별 $\Delta S_{\rxn,j}^\mathrm{cat}$ 가 정한다(\S\ref{sec:lco-center})."
- 판정: L2064 "관계식은 흑연 식~\eqref{eq:Uj} 와 부호까지 1:1 이고 바뀌는 것은 값뿐이다"가 본처. 맵 절의 선취는 식 재기입 없이 짧게 가능.
- 수정문: "평형 중심의 온도 의존은 관계식$\cdot$부호가 흑연과 동일하고 값만 전이별로 바뀐다(\S\ref{sec:lco-center})."

### F3 [MED·②] sec:lco-preview 가 "예고까지만" 헌장을 스스로 위반 — pairing 논증·가드 전문이 §lco-code 와 이중 존재 (Part II 최대 중복)
- 위치: L2004–2009. 원문(발췌): "방향 인자 대응 $f=+\sigma_d$ 는 같은 물리량끼리(점유$\leftrightarrow$점유$\cdot$진행률$\leftrightarrow$진행률) 짝짓는 pairing 하의 유일해로 확정된 판정이며, 그 판정이 딛는 가드가 ``\emph{함수형 동형 $\ne$ 물리량 동일}''이다 --- MSMR 의 $x_j/X_j$ 는 리튬화 분율(점유)이고 Ch1 의 $\xi$ 는 탈리튬화 진행률이라, 여집합을 무시하고 직접 등치하면 역부호 $f=-\sigma_d$ 가 나온다(평형 종은 그 교환에 불변이라 봉우리는 같지만 방향 서술이 갈라진다)."
- 판정: 동일 논증 전문이 L2677–2696(lco-code (c): "이제 \emph{같은 물리량끼리} 맞댄다 …", "★같은 logistic 이라는 것은 \emph{함수형 동형이지 물리량 동일이 아니다} — … 둘을 직접 등치하면 부호가 뒤집힌 $f=-\sigma_d$ 가 나온다…")에 완결 유도로 재등장. 재모수화 괄호(L2004)도 L2654–2658 과 중복. 절 스스로 "본 절은 예고까지만 하고"(L2009)라 선언 — 예고 절에 결론·가드·귀결까지 실려 이중화.
- 수정문(절 본문 전체 교체, 4문장→2문장): "multi-species, multi-reaction(MSMR) 모델은 양극 조성을 전위의 전이별 logistic 합으로 적는 표준 파라미터화라, Part II 종반에서 Ch1 곡선 클래스와 1:1 사전 --- $U\leftrightarrow V$, $U_j^0\leftrightarrow U_j^{\,d}$, $\omega_j\leftrightarrow w_j$, $X_j\leftrightarrow Q_j$, $f=+\sigma_d$ --- 으로 맞물린다($f$ 는 원계열의 $F/RT>0$ 를 폭에 흡수하고 지수에 남는 방향 부호 인자). 이 가운데 $f=+\sigma_d$ 는 같은 물리량끼리 짝짓는 pairing 하의 유일해이며, 그 유도와 가드(``함수형 동형 $\ne$ 물리량 동일'')$\cdot$박스는 \S\ref{sec:lco-code} 가 닫는다."
- orphan: 삭제분(여집합 오류→$f=-\sigma_d$ 귀결)은 L2691–2694 에 온전 — 0. \S\ref{sec:lco-preview} 참조(L1877)는 사전 예고 기능 유지로 무영향.

### F4 [MED·④] 문단 전체가 괄호 — 독립 괄호 문단(전보체)
- 위치: L1944–1945. 원문: "(LCO 의 $\Omega_j^\mathrm{cat}$·동역학 키가 배정되기 전에는 세 작용처 중 실질 활성이 분극뿐임은 \S\ref{sec:lco-hys} 의 two-phase calibration 지위 그대로다.)"
- 판정: 교과서 문체 규범(괄호 보충 전보체 금지 — 완결 문장으로) 위반. 내용은 유지 가치 있음.
- 수정문: "LCO 의 $\Omega_j^\mathrm{cat}$·동역학 키가 배정되기 전에는 세 작용처 중 실질 활성이 분극뿐이며, 이는 \S\ref{sec:lco-hys} 의 two-phase calibration 지위 그대로다."

### F5 [MED·②③] 층위 구분 문단 말미 = 같은 문단 첫 문장 + R4 삽입분(L1869–1871)의 3중 서술
- 위치: L1949–1950. 원문: "--- 두 서술은 층위가 달라 모순이 아니며, \S\ref{sec:lco-map} 는 라벨 의미론까지만 말하고 슬롯 배정은 이 절로 미룬다."
- 판정: "라벨 의미론/슬롯 배정" 구분은 이 문단 첫 문장이 이미 완전 서술했고, 맵 측 이월 선언은 R4 가 L1869–1871 에 심었다("$\sigma_d$ \emph{슬롯 배정}은 \S\ref{sec:lco-direction} 의 탈리튬화 규약…을 따른다"). R4·R5 가 양쪽에 각각 가드를 심으며 생긴 재팽창 — 말미 절만 절단해도 가드 2중화는 유지된다.
- 수정문: "--- 두 서술은 층위가 달라 모순이 아니다." (주의: R5 HIGH① 정정 문단이므로 가드 자체(첫 문장·규약 참조)는 절대 보존.)

### F5b [LOW] 같은 문단의 인용부호가 축약 paraphrase 를 감쌈 (R5 HIGH① 과 동일 클래스의 잔여 위험)
- 위치: L1947. 원문: "\S\ref{sec:lco-map} 의 ``셀 방전은 LCO 엔 리튬화'' 서술은" — 실제 맵 문면(L1867–1868)은 "셀 방전은 LCO 입장에서 \emph{리튬화}…". 겹따옴표가 verbatim 이 아닌 축약을 감싸고 있음.
- 수정문: 인용부호를 요지 표기로 완화 — "\S\ref{sec:lco-map} 의 `셀 방전 $=$ LCO 리튬화' 서술은" (또는 현행 문구 그대로 재인용).

### F6 [MED·②] two-phase calibration 문단의 gap-0 선취 — 도핑 문단과 자구 중복
- 위치: L2130–2131. 원문: "(도핑 시 $\Omega_j^\mathrm{cat}\le2RT$ 로 내려가는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다, 아래 도핑 문단)"
- 판정: L2257–2258 "$\Omega_j^\mathrm{cat,dop}\le2RT$ 로 피팅되는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다"와 자구 수준 중복(본처 = 도핑 문단, 식~\eqref{eq:lco-dope} 직후).
- 수정문: "(도핑의 정량형은 아래 도핑 문단·식~\eqref{eq:lco-dope})"

### F7 [MED·②③] tab:lco-staging 캡션과 lco-code (ii)(c)의 동결-근사 이중 서술 (2-사이트 조정 필요)
- 위치 A(캡션): L1896–1898. 원문: "또한 현 구현은 $\Delta S_e$ 를 기준온도 $T_\mathrm{ref}$ 에서 동결한 상수 오프셋으로 넣어(단일-기준 근사) 봉우리를 목표 전위에 두며, 조성 좌표 $x{=}x(\xi_\mathrm{eq}(V))$ 매핑과 $\Delta S_e{\propto}T$ 의 다온도 $T^2$ 곡률(\S\ref{sec:lco-Se})은 다온도 round-trip 피팅 단계의 과제로 분리한다."
- 위치 B(본문): L2744–2748 "(단일-기준 근사, 표~\ref{tab:lco-staging} 캡션 — 조성도 $x{=}x_\mathrm{center}$ 로 동결해 $V$-무관 상수)으로 넣으므로 … (다온도 $T^2$ 곡률은 round-trip 피팅 단계 과제)."
- 판정: 같은 한정(동결 구현·$T^2$ 과제 분리)이 캡션과 본문에 각각 완전형으로 존재하고, 본문이 캡션을 상세처로 가리키는 분할-뇌 구조. 정본은 본문(lco-code (ii)(c))이 자연스럽다.
- 수정문: 캡션 말미를 "또한 현 구현은 $\Delta S_e$ 를 $T_\mathrm{ref}$ 에서 동결한 상수 오프셋으로 넣어(단일-기준 근사) 봉우리를 목표 전위에 둔다(조성 매핑$\cdot$다온도 $T^2$ 곡률 과제는 \S\ref{sec:lco-code})."로 축약, 본문 괄호는 "(단일-기준 근사 — 조성도 $x{=}x_\mathrm{center}$ 로 동결해 $V$-무관 상수)"로 캡션 포인터 제거. orphan: 상호 포인터 순환 해소 — 0.

### F8 [MED·②] lco-electronic 절 도입이 §lco-why 의 "왜"를 선취
- 위치: L2268–2271. 원문: "— 흑연은 충방전 중 전자구조 변화가 미미해 전자항을 무시하지만, LCO 는 $x\!\downarrow$ 에서 절연체$\to$금속 전이(MIT)를 겪어 Fermi 준위 상태밀도 $g(E_F)$ 가 $0$ 에서 유한값으로 켜지므로 이 변화가 엔트로피에 들어온다."
- 판정: 직후 소절 \S\ref{sec:lco-why}(L2275–2282)가 같은 내용을 물리 근거($t_{2g}^6$·Co$^{4+}$ 정공·2상역 국소화)까지 완결 전개 — 도입의 상세 선취는 재진술.
- 수정문(도입 문단 교체): "지금까지 $\Delta S_{\rxn,j}$ 는 배치$\cdot$격자진동 두 몫이면 흑연에서 닫혔으나, LCO 양극은 전자(electronic) 엔트로피 몫이 하나 더 있다 — 까닭(MIT 로 $g(E_F)$ 가 켜짐)은 \S\ref{sec:lco-why} 가 연다. 이 절은 \S\ref{sec:dist} 의 점유 분포 언어를 전자 준위로 옮겨 Fermi--Dirac 분포에서 이 항을 유도하고, 1차 문헌에 없는 연속 곡선의 빈자리를 ★\emph{MIT-logistic 게이트}라는 모델 가정으로 메우되 그 가정을 물리로 정당화한다."

### F9 [MED·②] lco-peak ★방향 슬롯 문단 — (b) 말미와 완전 중복
- 위치: L2509–2510. 원문: "\textbf{★방향 슬롯.} 이후 $\sigma_d$ 는 \S\ref{sec:lco-direction} 의 규약(식~\eqref{eq:lco-sigmaslot})을 그대로 따르며, 평형 종은 (b)의 $\xi\leftrightarrow1-\xi$ 대칭으로 이 선택에 불변이다."
- 판정: 불변 진술은 (b) 말미 L2524–2525("봉우리 모양은 방향 불변$\cdot$양수이며, $\xi\leftrightarrow1-\xi$($\sigma_d$ 뒤집기)에 대칭이다")가 식으로 닫음. 남는 정보는 규약 포인터뿐.
- 수정문: 문단 삭제, (b) 첫 문장에 포인터 흡수 — "…흑연 식~\eqref{eq:xieq} 에 분기 중심 $U_j^{\,d,\mathrm{cat}}$(식~\eqref{eq:lco-Ubranch})을 넣은($\sigma_d$ 는 \S\ref{sec:lco-direction} 규약~\eqref{eq:lco-sigmaslot}) $\xi_{\eq,j}=\{1+\exp[-\sigma_d(V-U_j^{\,d,\mathrm{cat}})/w_j]\}^{-1}$ 이고, …" orphan: "★방향 슬롯" 후방 참조 없음 — 0.

### F10 [MED·②] lco-code (c) 안에서 여집합 불변 진술 3회
- 위치: L2677("종 $\xi(1-\xi)$ 는 이 교환에 불변이다(\S\ref{sec:lco-peak}(b))"), L2690–2691("MSMR 평형 등온선 자체는 방향이 없는 양이라 $\sigma_d$ 는 훑는 방향의 해석만 정하고 평형 종은 여집합 교환(식~\eqref{eq:lco-comp})에 불변이다"), L2693–2694("종 $\xi(1-\xi)$ 는 이 교환에 불변이라 관측 peak 은 어느 쪽으로도 같으나").
- 판정: 한 소절 내 3회 — 1·3회째는 각각 항등식 직독·가드 내부 귀결로 기능이 있으나 2회째의 불변 재진술은 잉여.
- 수정문(L2690–2691): "원계열의 $f=F/RT>0$ 는 이 규약에서 탈리튬화 진행($\sigma_d=+1$ 슬롯)에 대응하며, MSMR 평형 등온선 자체는 방향이 없는 양이라 $\sigma_d$ 는 훑는 방향의 해석만 정한다." (식~\eqref{eq:lco-comp} 는 L2669–2675 에 본체+L2677 문맥이 남아 orphan 0.)

### F11 [LOW·②] T1 온도 신호 문단의 괄호가 주절을 재설명
- 위치: L2557–2560. 원문: "($\Delta S_{e,1}\propto T$, \S\ref{sec:lco-Se} — 위치 자체가 아니라 \emph{이동률}이 $T$-선형, 곧 위치 이동은 $\propto T^2$, 식~\eqref{eq:U1T2})"
- 판정: 주절이 이미 "T1 봉우리의 \emph{온도 이동률} $\partial U_1/\partial T$ 가 $T$ 에 선형"이라 말함 — "위치 자체가 아니라 이동률이 $T$-선형"은 즉시 재진술.
- 수정문: "($\Delta S_{e,1}\propto T$ — 위치 이동은 $\propto T^2$, 식~\eqref{eq:U1T2}$\cdot$\S\ref{sec:lco-Se})"

### F12 [LOW·②] "문헌 초기값+데이터 피팅" 철학 3회째 재진술
- 위치: L2634–2635. 원문: "— 흑연 ``문헌 초기값 + 데이터 피팅'' 철학 그대로이며, 허위 정밀을 피해 tier 를 병기한다."
- 판정: L2399–2400(lco-gate)에서 이미 명시 적용, L2816–2817 도 동취지. 3회째는 tier 병기 지시만 남기면 됨.
- 수정문: "…round-trip 피팅해 식별한다(허위 정밀 금지 — tier 병기)."

### F13 [LOW·④] 한 문장 내 "충전(탈리튬화)" 병기 2회
- 위치: L1873–1874. 원문: "…LCO 양극에서 충전(탈리튬화)이 $\xi:0\!\to\!1$ 의 주 진행 방향이다 — 본 문건의 LCO 전이표는 그 충전(탈리튬화) 진행을 전위 오름차순으로 적는다."
- 수정문: 두 번째를 "그 충전 진행을"로.

### F14 [LOW·④] 괄호가 명사구를 분단
- 위치: L1876–1878. 원문: "흑연의 \code{GRAPHITE\_STAGING\_LIT}(표~\ref{tab:staging})에 대응하는 LCO(MSMR — multi-species, multi-reaction 파라미터화, 상세 \S\ref{sec:lco-preview}$\cdot$\S\ref{sec:lco-code}) 초기값 리스트를 \code{LCO\_MSMR\_LIT} 로 둔다"
- 판정: "LCO(…) 초기값 리스트"로 괄호가 수식어와 피수식어를 갈라 판독 저해.
- 수정문: "흑연의 \code{GRAPHITE\_STAGING\_LIT}(표~\ref{tab:staging})에 대응하는 LCO 초기값 리스트를 \code{LCO\_MSMR\_LIT} 로 둔다(MSMR — multi-species, multi-reaction 파라미터화, 상세 \S\ref{sec:lco-preview}$\cdot$\S\ref{sec:lco-code})"

### F15 [LOW·용어] "리액션·DFT 값" — 음차·불명 용어
- 위치: L2816. 원문: "리액션$\cdot$DFT 값은 신뢰 상한이 아니라 \emph{출발점}이므로 소폭 자유도를 권한다."
- 판정: "리액션"이 $\Delta H_\rxn\cdot\Delta S_\rxn$(반응 열역학 초기값)을 가리키는 것으로 읽히나 음차 단독 표기는 문체 규범(학술 용어 영어 원어/정식 한글)에 어긋나고 모호.
- 수정문: "반응 열역학($\Delta H_\rxn\cdot\Delta S_\rxn$)$\cdot$DFT 값은 신뢰 상한이 아니라 \emph{출발점}이므로 소폭 자유도를 권한다."

### F16 [LOW·②] MSMR 원어 병기 3회 (L1876–1877 첫 출현, L2001, L2647)
- 판정: 약자 정책상 첫 출현 병기 — 후속 2곳은 "MSMR 모델"로 충분. F3 채택 시 L2001 은 preview 첫 문장이라 병기 유지·L2647 만 축약해도 됨(파트 단위 재병기 관행을 취하면 반려 가능 — master 재량).
- 수정문(L2647): "이 통합의 실용적 결론 — ``같은 코드가 LCO 를 그린다'' — 의 근거는 \emph{MSMR 동형}이다: MSMR 모델\cite{msmr2024}이 양극 \emph{조성}을 전위의 전이별 logistic 합으로 적기 때문이다."

### F17 [LOW·②] "폭의 지위" 괄호 — 피팅-판정 논지 3회째
- 위치: L2552–2554. 원문: "(\S\ref{sec:broadening}; 어느 지위인지의 최종 판정은 피팅된 $\Omega_j^\mathrm{cat}$ 이 정하며, 도핑으로 $\Omega_j^\mathrm{cat}\le2RT$ 로 닫히는 전이는 단상 측의 평형 예측 지위로 넘어간다 — \S\ref{sec:lco-hys} two-phase calibration)"
- 판정: two-phase calibration 문단(L2129–2131)·도핑 문단(L2257–2258)에 이어 3회째.
- 수정문: "(\S\ref{sec:broadening}; 최종 지위 판정은 피팅된 $\Omega_j^\mathrm{cat}$ — \S\ref{sec:lco-hys} two-phase calibration)"

### F18 [LOW·비계] 위치 안내 비계
- 위치: L2496. 원문: "(\S\ref{sec:lco-decomp} — 사이의 \S\ref{sec:lco-peak} 을 지나 두 소절 뒤)"
- 판정: "두 소절 뒤" 류 항행 안내는 recap 비계 — inline 참조만으로 충분.
- 수정문: "(\S\ref{sec:lco-decomp})"

---

## 과업 2 — 압축 이월 4쌍 처리 판정

**식별 근거(확정)**: 커밋 1bb914c 메시지 "p4 … 10/12 적용(잔여 2쌍 = 생략부 인용 — R6 이월)" + ledger L22 "압축 처분 기록: p3 signcheck 콜론계 기각·p3 잔여 2쌍(생략부 인용)·p4 2쌍 R6 이월". p3 26개·p4 12개 교체 쌍 전수를 현행 tex(및 압축 직전 4f1ab12·직후 377b5e6)와 대조한 결과: **p3 미적용-비기각 = 2-7·4-2 정확히 2쌍, p4 미적용 = 1-7·2-2 정확히 2쌍** (signcheck 3-1/3-2/3-3 은 기각 처분 — 재제안하지 않음). [추정 1건] p3 4-2 의 anchor 는 생략부가 아니라 개행 걸친 전문 인용 — "생략부 인용" 라벨은 2-7 에는 자구로, 4-2 에는 느슨하게 부합(소거법상 이 2쌍 외 후보 없음).

### 쌍 1 — p3 2-7 (ch1, lco-code (ii)(c) 동결 근사 연결어) : **유효 — 적용 권고**
- (i) 소재: ch1 **L2747–2748**. 현행 원문: "…의 \emph{선형} $U(T)$ 가 된다 — 코드의 선형 거동은 이 동결 근사의 결과로 읽는다(다온도 $T^2$ 곡률은 round-trip 피팅 단계 과제)."
- (ii) 유효성: **유효**. R 라운드가 같은 문장 앞부분에 "(단일-기준 근사, 표~\ref{tab:lco-staging} 캡션 — 조성도 $x{=}x_\mathrm{center}$ 로 동결해 $V$-무관 상수)"를 삽입해 인과("넣으므로 … 가 된다")가 더 명시화 — "코드의 선형 거동은 … 결과로 읽는다"는 이제 명백한 재진술이라 압축 취지가 오히려 강화됨. 수치·한정어 변경 0.
- (iii) 적용문(현행 문구 기준 전문): "…의 \emph{선형} $U(T)$ 가 된다(동결 근사의 결과 — 다온도 $T^2$ 곡률은 round-trip 피팅 단계 과제). 평가 순서 주의 — …"
  - 참고: F7(캡션-본문 조정)과 독립 — 병행 적용 가능.

### 쌍 2 — p3 4-2 (ch1, sec:dist (a)(b) Part 0 재수용) : **유효 — 적용 권고(대안 병기)**
- (i) 소재: ch1 **L1263–1266**. 현행 원문: "\textbf{(a)(b) --- Part 0 회수.} 단일 자리 분포는 Part 0 이 이미 닫았다 --- 두 미시상태의 grand-canonical 분배함수 $Z=1+e^{-\beta\Delta\mu}$(식~\eqref{eq:partfn})와 평균 점유 $\langle n\rangle=1/(1+e^{+\beta\Delta\mu})$(식~\eqref{eq:fermifn}, $\Delta\mu\equiv\varepsilon-\mu_\mathrm{Li}$)를 그대로 받는다."
- (ii) 유효성: **유효**. 이 구간은 R1–R5 정정 무접촉(압축 직전 4f1ab12 과 자구 동일 확인). "두 미시상태의"는 $Z$ 가 두 항 합으로 자체 표시(장식), 삭제분 정보 손실 0. 단 "그대로"는 Part 0 무수정 수용(재유도 금지 자산)의 강조 — 삭제해도 "Part 0 이 이미 닫았다"가 같은 기능을 하므로 압축안 유지 판정. 참조(\eqref{eq:partfn}·\eqref{eq:fermifn})·정의($\Delta\mu$) 전량 보존.
- (iii) 적용문(전문): "\textbf{(a)(b) --- Part 0 회수.} 단일 자리 분포는 Part 0 이 이미 닫았다 --- grand-canonical 분배함수 $Z=1+e^{-\beta\Delta\mu}$(식~\eqref{eq:partfn})와 평균 점유 $\langle n\rangle=1/(1+e^{+\beta\Delta\mu})$(식~\eqref{eq:fermifn}, $\Delta\mu\equiv\varepsilon-\mu_\mathrm{Li}$)를 받는다."

### 쌍 3 — p4 1-7 (ch2, revheat keybox 입력 목록) : **유효 — 적용 권고**
- (i) 소재: ch2 **L723–724**. 현행 원문: "$\dot Q_\rev=-IT\,\partial U_\oc/\partial T$. \emph{입력} = $\{\Delta S^0_j,\,Q_j,\,U_j,\,w_j\}$ 와 Ch1 의 $\xi_j(V,T)$(식~\eqref{eq:logistic})." (p4 기록의 "eq~\eqref{…}"는 용어 패스에서 "식~\eqref{…}"로 바뀜 — anchor 변화 확인.)
- (ii) 유효성: **유효**. keybox 원칙(문장 병합만·내용 무삭제) 준수, 후속 정정(R2 의 $n_jR/F$ config 항 수정은 위 식 내부)과 무충돌. $\dot Q_\rev$ 식·입력 집합·참조 전량 보존.
- (iii) 적용문(현행 문구 기준 전문): "$\dot Q_\rev=-IT\,\partial U_\oc/\partial T$ 로 얻으며, \emph{입력}은 $\{\Delta S^0_j,\,Q_j,\,U_j,\,w_j\}$ 와 Ch1 의 $\xi_j(V,T)$(식~\eqref{eq:logistic})다."

### 쌍 4 — p4 2-2 (ch2, weff 두-상 항목 병합) : **유효 — 적용 권고**
- (i) 소재: ch2 **L587–589**. 현행 원문: "…평형은 폭을 거의 0 으로 예측한다. 그런데 \emph{실측} $dQ/dV$ 봉우리는 유한 폭의 \emph{종}이다. 이 폭은 평형이 정하는 양이 \emph{아니라}, 다음 세 broadening 출처가 정하는 \emph{현상학적 자유 피팅 파라미터}다: (i) …" (항목 표제는 R 정정으로 "흑연 staging 의 두-상 전이 $2\mathrm L\!\to\!2\cdot2\!\to\!1$ 가 여기 속함"으로 바뀌었으나 — ch1 two-phase calibration 과 정합 — 병합 대상 두 문장은 원형 유지.)
- (ii) 유효성: **유효**. (i)(ii)(iii) 세 출처·모든 판정어("평형 델타"·"현상학적 자유 피팅 파라미터") 무접촉, 문장 경계만 접속화. 후속 정정과 무충돌.
- (iii) 적용문(현행 문구 기준 전문): "…평형은 폭을 거의 0 으로 예측한다. 그런데 \emph{실측} $dQ/dV$ 봉우리는 유한 폭의 \emph{종}이며, 이 폭은 평형이 정하는 양이 \emph{아니라} 다음 세 broadening 출처가 정하는 \emph{현상학적 자유 피팅 파라미터}다: (i) …" ((i) 이하 자구 불변)

---

## 말미 선언

**가장 약한 1곳**: **sec:lco-preview(L2000–2009) — F3.** "예고까지만"을 선언한 절이 $f=+\sigma_d$ 유일해 판정·"함수형 동형 ≠ 물리량 동일" 가드·역부호 귀결까지 전문을 싣고, §lco-code (c)가 같은 논증을 완결 유도로 반복 — 사용자 원 지적("LCO 는 말이 많다")의 현존 최대 잔존 지점.

**물리 불변 확인**: 지적 19건 + 이월 적용문 4건 전부 산문·참조 재배치 — 식·부호·수치·tier 한정어·이중계산 가드 변경 0. 특히 eq:lco-sigmaslot/eq:lco-dUdT/eq:dSegate/eq:lco-msmrmap/eq:U1T2 및 −46 J/(mol K)·1.1 k_B·+80 J/(mol K)·13 e/eV/atom·0.85/0.05 등 전 수치 비접촉. 부호 사슬(S1–S8·R1–R5) 비접촉.

**Coverage 선언**: Part II 산문 블록 **70개** 전수 판정(절별: intro 1·map 5·direction 6·preview 1·center 5·hys 9·electronic 14·peak 7·decomp 8·code 6·입력 3·facade 1·signcheck 4) — 결함 19(MED 9·LOW 10)·통과 51. 이월 4쌍 처분: 4/4 소재 확정·4/4 유효·적용문 4건 제시(기각 0). p3/p4 잔여 쌍 식별은 26+12쌍 전수 대조(커밋 3개 교차)로 수행 — missing 0.

**과잉 판정 자기표시(refute — 검토 후 반려한 후보)**: ① signcheck 콜론계(p3 3-1/3-2/3-3) 재제안 — master 기각 확정 사안이라 불채택. ② lco-hys 의 T2·T3/T1 대입 display 3벌 — 수식이며 대입 실증 역할, 산문 아님 → 반려. ③ −46·1.1 k_B 수치의 다지점 반복 — 각 자리가 검산 anchor/캡션 자립 관행 → 반려. ④ lco-center verifybox 3★ 블록·★부호 규약 장문 — 부호 경고·혼동 가드 예외 클래스 → 통과. ⑤ facade 3문장 무식(無式) 문단 — G-usable(코드 사용 규약) 기능 → 통과. ⑥ F5 는 R5 HIGH① 정정 문단 접촉이라 확신도 한 단계 낮춤(가드 보존 조건부). ⑦ F7·F16 은 캡션 자립/파트 재병기 관행과 상충 소지 — master 재량 표시.

**5줄 요약**
1. 물리·부호·수치 결함 0 — R6 잔존 결함은 전부 산문 중복·전보체(MED 9·LOW 10, 수정문 전문 제시).
2. 최대 잔존 중복 = sec:lco-preview 가 §lco-code 의 pairing 논증·가드를 전문 선취(F3, 4문장→2문장 축약안).
3. 이월 4쌍 = p3 2-7(ch1 L2747)·p3 4-2(ch1 L1263)·p4 1-7(ch2 L723)·p4 2-2(ch2 L587) — 4/4 유효, 현행 문구 기준 적용문 제시(후속 정정과 충돌 0).
4. 식별은 커밋 377b5e6/1bb914c/4f1ab12 대조 + 38쌍 전수 census 로 확정; 단 p3 4-2 의 "생략부 인용" 라벨 부합은 [추정](소거법상 유일 후보).
5. 오적발 가능 지점 자기표시: F5(R5 정정 문단 접촉)·F7(캡션 자립 관행)·F16(파트 재병기 관행) — 3건은 master 재량 판단 권고.
