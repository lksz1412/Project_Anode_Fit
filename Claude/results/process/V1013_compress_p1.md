# V1.0.13 산문 압축 제안 — Part 1 (sec:lco-center · sec:lco-hys)

- 대상: `Claude/docs/v1.0.13/graphite_ica_ch1_v1.0.13.tex` L1964–2220 (두 subsection 전문 정독 완료).
- 성격: **제안서** — 원본 무수정. 각 항목 = [원문 verbatim] → [교체문] + 삭제 근거 + 물리 보존 선언.
- 원칙 준수: 수식 환경 전량 무변경(플레이스홀더 `[식 환경 무변경: ...]` 로 표기), 수치·부호·tier·가드·참조 전량 보존, 방향 규약 재설명은 \S sec:lco-direction 포인터로.
- 문장 셈 규약: 마침표 종결 산문 문장 1개 = 1문장(굵은 라벨 단독 문장 포함, display 수식을 걸치는 문장은 1문장). display 수식 자체는 셈 제외.

---

## A. sec:lco-center (L1964–2060) — 9쌍

### 쌍 1 — (a) 두 문장 병합 + host-무관 3중 중복 접기 (L1965–1973)

**원문:**
```
\S\ref{sec:center} 의 평형 중심 유도를 되짚으면 어느 다리에도 ``흑연''이라는 물질 고유 항이 들어가지
않는다: (i) 실험조건 매핑 식~\eqref{eq:n0map} 의 방향 부호$\cdot$전류 환산
$\sigma_d=\pm1,\ |I|=\code{c\_rate}\,Q_\cell$ 은 삽입형 전극이면 종류를 가리지 않고, (ii) 전기화학 평형
조건 식~\eqref{eq:eqcond}($\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U),\ \Delta G_j=-sFU_j$)는 삽입
반쪽반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 의 전기화학 평형
(식~\eqref{eq:eqbalance})에서 나오며 host 가 흑연인지 LCO 인지에 무관하고(host 의 화학 정체는 상수
$\mu^0$ 와 반응 몫 입력값으로 흡수된다), (iii) 비배치 몫 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 은 반응
종에 무관한 열역학 항등식이다. LCO 로 넘어갈 때 이 세 자리에 들어가는 것은 전이 집합과 입력값의 치환뿐이다:
```

**교체:**
```
\S\ref{sec:center} 의 평형 중심 유도에는 어느 다리에도 ``흑연''이라는 물질 고유 항이 없다 —
(i) 실험조건 매핑 식~\eqref{eq:n0map} 의 방향 부호$\cdot$전류 환산
$\sigma_d=\pm1,\ |I|=\code{c\_rate}\,Q_\cell$ 은 삽입형 전극이면 종류를 가리지 않고, (ii) 전기화학 평형
조건 식~\eqref{eq:eqcond}($\mu_\mathrm{Li}(\theta_\eq)=\mu^0-sF(V-U),\ \Delta G_j=-sFU_j$)는 삽입
반쪽반응 $\mathrm{Li}^++e^-+[\,]\rightleftharpoons\mathrm{Li}_{(\text{host})}$ 의 전기화학 평형
(식~\eqref{eq:eqbalance})에서 나와 host 의 화학 정체가 상수 $\mu^0$ 와 반응 몫 입력값으로 흡수되며,
(iii) 비배치 몫 $\Delta G_j=\Delta H_{\rxn,j}-T\Delta S_{\rxn,j}$ 은 반응 종에 무관한 열역학 항등식이라,
LCO 로 넘어갈 때 이 세 자리에 들어가는 것은 전이 집합과 입력값의 치환뿐이다:
```

- 삭제 근거: "되짚으면"(메타) 제거. "host 가 흑연인지 LCO 인지에 무관하고"는 문두 선언("물질 고유 항이 없다")·괄호("흡수된다")와 3중 중복 — 흡수 절만 존치. 2문장 → 1문장.
- 물리 보존: 세 진입 (i)(ii)(iii)·인라인 수식·반쪽반응식·참조 전량 유지. 사라진 물리 정보 0.

### 쌍 2 — (b) 재확인 괄호 삭제 (L1988–1989)

**원문:**
```
곧 흑연 식~\eqref{eq:Ujmid} 과 글자 그대로 같은 식에 상첨자 $\mathrm{cat}$ 만 붙는다(host 가 유도 단계에
없었다는 (a)의 대입 확인).
```

**교체:**
```
곧 흑연 식~\eqref{eq:Ujmid} 과 글자 그대로 같은 식에 상첨자 $\mathrm{cat}$ 만 붙는다.
```

- 삭제 근거: 괄호는 (a) 결론의 재진술(같은 명제가 쌍 1 교체문에 존치).
- 물리 보존: host-무관 명제는 (a)가 담당. 사라진 물리 정보 0.

### 쌍 3 — (c) 도입 두 문장 병합 (L1992–1994)

**원문:**
```
(b)를 $U_j^\mathrm{cat}$ 로 이항하면 $U_j^\mathrm{cat}(T)=(-\Delta H_{\rxn,j}^\mathrm{cat}
+T\Delta S_{\rxn,j}^\mathrm{cat})/F$ 로, 흑연 식~\eqref{eq:Uj} 와 같은 함수형이다. 온도 계수는 두 독립
경로가 같은 값에 닿는다.
```

**교체:**
```
(b)를 $U_j^\mathrm{cat}$ 로 이항하면 $U_j^\mathrm{cat}(T)=(-\Delta H_{\rxn,j}^\mathrm{cat}
+T\Delta S_{\rxn,j}^\mathrm{cat})/F$ 로 흑연 식~\eqref{eq:Uj} 와 같은 함수형이고, 온도 계수는 두 독립
경로가 같은 값에 닿는다.
```

- 삭제 근거: 단순 병합(내용 삭제 없음). 2문장 → 1문장. 경로 1·경로 2 문장(순간값 한정어·"정확한 항등식" 한정어 포함)과 결구 "둘의 일치는 순간 기울기 의미 — 전극 불문의 수식적 의미" 문장은 **무변경 유지**.
- 물리 보존: 사라진 물리 정보 0.

### 쌍 4 — (d) 대표 스케일 문장 → verifybox 포인터 (L2018–2024)

**원문:**
```
관계식은 흑연 식~\eqref{eq:Uj} 와 부호까지 1:1 이고 바뀌는 것은 값뿐이다 — 양극의 높은 중심
($\sim$3.9--4.2 V)은 분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양인 데서 오고, $\Delta S_{\rxn,j}^\mathrm{cat}$
는 \S\ref{sec:lco-decomp}(식~\eqref{eq:lco-decomp})에서 config$\cdot$vib$\cdot$전자 세 성분으로 분해된다.
대표 단전극 계수 $\dd\phi/\dd T\approx+0.83$ mV/K 는 $F\times0.83\times10^{-3}\approx+80$ J/(mol\,K) 의
\emph{전체 단전극 스케일}[tier B]로 역산되며, 이는 표~\ref{tab:lco-staging} 의 \emph{전이별 성분}값
(config $\Delta S$ 등)과 서로 다른 층위의 양이라 직접 비교하지 않는다(층위 분리 시 T1 전자항의 창-국소 음의
보정과도 부호 충돌이 없다 — 정량은 아래 verifybox).
```

**교체:**
```
관계식은 흑연 식~\eqref{eq:Uj} 와 부호까지 1:1 이고 바뀌는 것은 값뿐이다 — 양극의 높은 중심
($\sim$3.9--4.2 V)은 분자 $-\Delta H_{\rxn,j}^\mathrm{cat}$ 가 크게 양인 데서 오고, $\Delta S_{\rxn,j}^\mathrm{cat}$
는 \S\ref{sec:lco-decomp}(식~\eqref{eq:lco-decomp})에서 config$\cdot$vib$\cdot$전자 세 성분으로 분해된다.
대표 단전극 스케일($\dd\phi/\dd T\approx+0.83$ mV/K $\to\approx+80$ J/(mol\,K)[tier B])의 역산과
전이별 성분값과의 층위 분리$\cdot$T1 전자항과의 부호 공존은 아래 verifybox 가 정량으로 닫는다.
```

- 삭제 근거: 둘째 문장의 역산 수치·층위 분리·부호 무충돌은 verifybox 본문(역산식 96485×0.83×10⁻³, ★공존 문단)과 완전 중복 — 본문엔 예고 포인터만 남김.
- 물리 보존: +0.83·+80·tier B 는 포인터에도 잔존하고 F 환산 수치식·"직접 비교하지 않는다" 가드·부호 무충돌 정량은 verifybox 에 전량 존치. 사라진 물리 정보 0.

### 쌍 5 — ★다온도 전자항 주의: Kirchhoff 문장 인라인 병합 (L2024–2035)

**원문:**
```
\textbf{★다온도 전자항 주의.} $\Delta S_{e,j}(x,T)\propto T$
인 항을 다온도 모델에 실제로 풀 때는 고정 $\Delta H$ 로 $U_j(T)=(-\Delta H+T\Delta S(T))/F$ 를 기계 미분하면
잉여항 $T\,\partial_T\Delta S$ 가 생기므로, 열역학적으로 유지할 불변식은 위 박스의
$\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}(T)/F$ 이고 위치는 기준온도에서
[식 환경 무변경: U_j^cat(T)=U_j^cat(T_ref)+(1/F)∫ΔS dT' 적분식]
로 해석해야 한다 — 전자항 $\propto T'$ 를 실제 적분한 닫힌 특수형이 \S\ref{sec:lco-Se} 의
식~\eqref{eq:U1T2}($\tfrac12(T^2-T_\mathrm{ref}^2)$ 곡률)다. 잉여항이 비물리인 열역학적 이유는 Kirchhoff
일관성이다: $\partial\Delta H/\partial T=\Delta C_p$ 이고 $T\,\partial\Delta S/\partial T=\Delta C_p$ 라
``$\Delta H$ 고정$\wedge\partial_T\Delta S\ne0$'' 가정 자체가 성립하지 않으며, 그 모순 없이 남는 불변식이
$\partial U/\partial T=\Delta S(T)/F$ 다.
```

**교체:**
```
\textbf{★다온도 전자항 주의} — $\Delta S_{e,j}(x,T)\propto T$
인 항을 다온도 모델에 풀 때 고정 $\Delta H$ 로 $U_j(T)=(-\Delta H+T\Delta S(T))/F$ 를 기계 미분하면 생기는
잉여항 $T\,\partial_T\Delta S$ 는 Kirchhoff 일관성 위반($\partial\Delta H/\partial T=\Delta C_p$ 이고
$T\,\partial\Delta S/\partial T=\Delta C_p$ 라 ``$\Delta H$ 고정$\wedge\partial_T\Delta S\ne0$'' 가정 자체가
성립하지 않는다)의 비물리 항이므로, 유지할 불변식은 위 박스의
$\partial U_j/\partial T=\Delta S_{\rxn,j}^\mathrm{cat}(T)/F$ 이고 위치는 기준온도에서
[식 환경 무변경: 동일 적분식]
로 해석해야 한다 — 전자항 $\propto T'$ 를 실제 적분한 닫힌 특수형이 \S\ref{sec:lco-Se} 의
식~\eqref{eq:U1T2}($\tfrac12(T^2-T_\mathrm{ref}^2)$ 곡률)다.
```

- 삭제 근거: 불변식 ∂U/∂T=ΔS(T)/F 가 두 문장에서 2회 진술 — Kirchhoff 근거를 잉여항 서술 안에 괄호로 인라인해 1회로 통합. 라벨 마침표 → em-dash 접기. 3문장 → 1문장.
- 물리 보존: 기계 미분 잉여항·Kirchhoff 두 항등식·성립 불가 가정·불변식·적분 해석·U1T2 곡률 포인터 전부 존치. 사라진 물리 정보 0.

### 쌍 6 — (부호 좌표 고정) 라벨 접기 (L2035–2038)

**원문:**
```
\textbf{(부호 좌표 고정.)} 아래 검산의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 는 반쪽반응을
```

**교체:**
```
\textbf{(부호 좌표 고정)} — 아래 검산의 $\Delta S_{\rxn,j}^\mathrm{cat}$ 는 반쪽반응을
```

- 삭제 근거: 라벨 단독 문장을 본문 문장에 접합(이후 본문 무변경). 2문장 → 1문장.
- 물리 보존: 삽입-방향 좌표·표 tab:staging 동일 좌표·측정 규약 의존 한정어 전부 무변경. 사라진 물리 정보 0.

### 쌍 7 — verifybox 도입 라벨 접기 (L2041)

**원문:**
```
\textbf{LCO 중심 부호 검산($T=298.15$ K).} 대표 단전극 엔트로피 계수 $\dd\phi/\dd T\approx+0.83$ mV/K\cite{swiderska2019}
```

**교체:**
```
\textbf{LCO 중심 부호 검산($T=298.15$ K)} — 대표 단전극 엔트로피 계수 $\dd\phi/\dd T\approx+0.83$ mV/K\cite{swiderska2019}
```

- 삭제 근거: 라벨 접기(이후 역산 문장 — 96485×0.83×10⁻³≈+80, ∂U/∂T>0, 30 K 창 +25 mV — 무변경). 2문장 → 1문장.
- 물리 보존: 수치·tier B 한정어·인용 전부 무변경. 사라진 물리 정보 0.

### 쌍 8 — verifybox ★단전극 대 전셀: 범위 문장 병합 + 다온도 문장 병합 (L2045–2050)

**원문:**
```
\textbf{★단전극 대 전셀 혼동 금지.} 이 $+0.83$ mV/K 는 \emph{LCO 단일전극}(vs Li, 본 문건 범위) 값이다 — 같은 문헌의
\emph{전셀}(LCO$-$graphite) 엔트로피 계수는 SOC 에 따라 부호가 전환되며($-0.37$\,\textasciitilde$+0.1$ mV/K) 흑연 항이
합산된 다른 양이다. 본 문건은 하프셀 범위라 단전극 LCO 부호만 쓴다(전셀 합성은 후속). 또한 $\dd\phi/\dd T$ 의 부호$\cdot$
크기는 $x$(SOC)에 의존하므로 위 $+0.83$ 은 \emph{대표 스케일}일 뿐 전이별 정밀값이 아니다 — 전이별 $\Delta S_{\rxn,j}^\mathrm{cat}$
는 표~\ref{tab:lco-staging}$\cdot$식~\eqref{eq:lco-decomp} 의 초기값을 데이터로 피팅해 정한다(허위 정밀 금지, tier 병기).
다온도 LCO 피팅에서 온도마다 $U_j(T)$ 를 따로 읽어야 함은 흑연보다 더 분명하다.
```

**교체:**
```
\textbf{★단전극 대 전셀 혼동 금지} — 이 $+0.83$ mV/K 는 \emph{LCO 단일전극}(vs Li) 값이고 본 문건(하프셀
범위)은 이 단전극 부호만 쓴다(전셀 합성은 후속) — 같은 문헌의 \emph{전셀}(LCO$-$graphite) 엔트로피 계수는
SOC 에 따라 부호가 전환되며($-0.37$\,\textasciitilde$+0.1$ mV/K) 흑연 항이 합산된 다른 양이다. 또한
$\dd\phi/\dd T$ 의 부호$\cdot$크기는 $x$(SOC)에 의존하므로 위 $+0.83$ 은 \emph{대표 스케일}일 뿐 전이별
정밀값이 아니다 — 전이별 $\Delta S_{\rxn,j}^\mathrm{cat}$ 는 표~\ref{tab:lco-staging}$\cdot$식~\eqref{eq:lco-decomp}
의 초기값을 데이터로 피팅해 정하며(허위 정밀 금지, tier 병기), 다온도 피팅에선 온도마다 $U_j(T)$ 를 따로 읽는다.
```

- 삭제 근거: "본 문건 범위" 괄호와 "본 문건은 하프셀 범위라 ... 쓴다" 문장이 동일 내용 2회 — 첫 문장에 병합. "다온도 ... 흑연보다 더 분명하다" 단문은 피팅 문장 꼬리로 병합("흑연보다 더 분명" 수사 제거 — 비교 수사일 뿐 정량 아님). 라벨 접기. 5문장 → 2문장.
- 물리 보존: 단전극/전셀 구분·−0.37~+0.1 mV/K·SOC 의존·대표 스케일 한정어·허위 정밀 금지·tier 병기·온도별 U_j(T) 읽기 전부 존치. 사라진 물리 정보 0.

### 쌍 9 — verifybox ★부호 공존: 결구 재진술 병합 (L2051–2059)

**원문:**
```
\textbf{★전자항과의 부호 공존(오독 방지).} 이 $\Delta S_{\rxn}^\mathrm{cat}\!\approx\!+80$ J/(mol\,K)$>0$ 은
[... 중간 두 문장(−46 J/(mol K)·1.1 k_B/atom·+80−46≈+34>0 수치 문장) 무변경 ...]
한 가지 종류 혼동만
경계하면 된다 — 표~\ref{tab:lco-staging} 의 config$\cdot$vib 값은 \emph{전이별 부분몰} 성분이고 $+80$ 은 \emph{전체 계수}의
대표 스케일이라, 둘은 \emph{서로 다른 종류의 양}이다(\S\ref{sec:lco-decomp}). 곧 ``전체 계수의 $+80$''과
``T1 전자항 음수''(한 성분)는 모순이 아니라 서로 다른 층위에서 공존한다.
```

**교체:**
```
\textbf{★전자항과의 부호 공존(오독 방지)} — 이 $\Delta S_{\rxn}^\mathrm{cat}\!\approx\!+80$ J/(mol\,K)$>0$ 은
[... 중간 두 문장 무변경 유지 ...]
표~\ref{tab:lco-staging}
의 config$\cdot$vib 값은 \emph{전이별 부분몰} 성분, $+80$ 은 \emph{전체 계수}의 대표 스케일로 \emph{서로 다른
종류$\cdot$층위의 양}이라(\S\ref{sec:lco-decomp}) 둘의 공존은 모순이 아니다.
```

- 삭제 근거: 마지막 문장("곧 ...는 모순이 아니라 ... 공존한다")은 직전 문장의 순수 재진술 — "층위" 단어를 흡수해 1문장으로 통합. "한 가지 종류 혼동만 경계하면 된다" 도입구는 뒤 내용의 예고 중복. 라벨 접기. 5문장 → 3문장.
- 물리 보존: +80(합=config+vib+elec)·T1 전자항 음(삽입 기준)·−46·1.1 k_B/atom·+34>0·창 밖 소멸·부분몰 대 전체계수 종류 구분 전부 존치. 사라진 물리 정보 0.

**A 소계: sec:lco-center 산문 28문장 → 17문장 (−39.3%).**

---

## B. sec:lco-hys (L2062–2220) — 9쌍

### 쌍 10 — (a) 가정 문장과 번호 부여 문장 병합 (L2063–2066)

**원문:**
```
\S\ref{sec:hys} 의 격자기체 화학퍼텐셜 식~\eqref{eq:mu} 와 자유에너지 식~\eqref{eq:gxi} 는 ``동등한
자리에 리튬이 차고 빈다''는 가정 하나만 쓴다 — 이 가정은 LCO $\mathrm{Li}_x\mathrm{CoO_2}$ 의 팔면체 리튬
자리에도 문자 그대로 성립한다(자리당 점유 0 또는 1). 따라서 \S\ref{sec:lco-center} 의 LCO 전이 집합에 번호를 달아
```

**교체:**
```
\S\ref{sec:hys} 의 격자기체 화학퍼텐셜 식~\eqref{eq:mu} 와 자유에너지 식~\eqref{eq:gxi} 의 유일한
가정 ``동등한 자리에 리튬이 차고 빈다''는 LCO $\mathrm{Li}_x\mathrm{CoO_2}$ 의 팔면체 리튬 자리에도
문자 그대로 성립하므로(자리당 점유 0 또는 1), \S\ref{sec:lco-center} 의 LCO 전이 집합에 번호를 달아
```

- 삭제 근거: "가정 하나만 쓴다 — 이 가정은 ... 성립한다. 따라서 ..." 의 2단 전개를 인과 접속 1문장으로 병합(식 eq:lco-J 이하 무변경). 2문장 → 1문장.
- 물리 보존: 단일 가정 지위("유일한 가정")·팔면체 자리·0/1 점유 전부 존치. 사라진 물리 정보 0.

### 쌍 11 — ★two-phase calibration: 4중2/3중3 재진술 문장 흡수 (L2081–2095)

**원문:**
```
\textbf{★two-phase calibration.}
흑연에서 spinodal 문턱 $\Omega_j>2RT$($2RT\approx4958$ J/mol@298 K, 식~\eqref{eq:spinodal})를 피팅 후
유지하는 것은 네 staging 전이 중 $2\mathrm L\!\to\!2$(LiC$_{12}$)$\cdot$$2\!\to\!1$(LiC$_6$) \emph{두 개}
뿐이고, dilute$\to$stage4$\cdot$$4\mathrm L\!\leftrightarrow\!3\mathrm L$ 은 $\Omega_j<2RT$ 로 내려가
solid-solution 이 되는 쪽으로 피팅된다(\S\ref{sec:width}$\cdot$\S\ref{sec:broadening}). LCO 는 이와 달리 pure-LCO
초기값에서 T1(MIT)$\cdot$T2$\cdot$T3(order--disorder) \emph{세 전이 전부}가 문턱을 넘는 상분리 후보다
(표~\ref{tab:lco-staging}). 곧 흑연 ``4 중 2''$\leftrightarrow$LCO ``3 중 3''로 대응 전이 집합만 다르고
문턱 판정 식 $\Omega_j^\mathrm{cat}>2RT$ 자체는 동일하며, 각 전이의 실제 gap 유무는 최종적으로
\emph{피팅된} $\Omega_j^\mathrm{cat}$ 이 $2RT$ 를 넘는지가 정한다(도핑 시 $\Omega_j^\mathrm{cat}\le2RT$
로 내려가는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다, 아래 도핑 문단).
```

**교체:**
```
\textbf{★two-phase calibration} —
흑연에서 spinodal 문턱 $\Omega_j>2RT$($2RT\approx4958$ J/mol@298 K, 식~\eqref{eq:spinodal})를 피팅 후
유지하는 것은 네 staging 전이 중 $2\mathrm L\!\to\!2$(LiC$_{12}$)$\cdot$$2\!\to\!1$(LiC$_6$) \emph{두 개}
뿐이고 dilute$\to$stage4$\cdot$$4\mathrm L\!\leftrightarrow\!3\mathrm L$ 은 $\Omega_j<2RT$ 의
solid-solution 쪽으로 피팅되는(\S\ref{sec:width}$\cdot$\S\ref{sec:broadening}) 반면, LCO 는 pure-LCO
초기값에서 T1(MIT)$\cdot$T2$\cdot$T3(order--disorder) \emph{세 전이 전부}가 같은 문턱
$\Omega_j^\mathrm{cat}>2RT$ 를 넘는 상분리 후보다(표~\ref{tab:lco-staging}). 각 전이의 실제 gap 유무는 최종적으로
\emph{피팅된} $\Omega_j^\mathrm{cat}$ 이 $2RT$ 를 넘는지가 정한다(도핑 시 $\Omega_j^\mathrm{cat}\le2RT$
로 내려가는 전이는 같은 식 안에서 gap 이 0 으로 닫힌다, 아래 도핑 문단).
```

- 삭제 근거: "곧 흑연 4중2↔LCO 3중3로 대응 전이 집합만 다르고 문턱 판정 식 자체는 동일하며"는 앞 두 문장의 요약 재진술 — 문턱 동일성("같은 문턱 Ω>2RT")을 병합문에 흡수하고 대비는 "반면" 접속이 담당. 라벨 접기. 이 인용 범위 4문장 → 2문장. 이후의 "다만 그 후보 지위는 아직 서술 층위다 …" 및 "따라서 본 절의 … 발효된다" 두 가드 문장은 **무변경 유지**.
- 물리 보존: 2RT≈4958 J/mol·흑연 2개/LCO 3개 대비·피팅 최종 판정·도핑 극한 포인터·Ω 미배정=Ω=0 폴백 가드·발효 조건 가드 전부 존치. 사라진 물리 정보 0.

### 쌍 12 — (c) 상쇄 문장과 대칭점 검산 병합 (L2126–2129)

**원문:**
```
상수 중심 $U_j^\mathrm{cat}$ 는 차에서 상쇄된다. \emph{대칭점 검산}: 두 끝점의 \emph{평균}은 로그 몫과
$(1-2\xi)$ 몫이 각각 부호 반대로 상쇄되어 $\tfrac12[V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^-)
+V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^+)]=U_j^\mathrm{cat}$(흑연 식~\eqref{eq:hyssym} 과 동일 대수) —
분기가 $U_j^\mathrm{cat}$ 대칭이라는 성질이 LCO 에도 host-무관하게 성립한다.
```

**교체:**
```
상수 중심 $U_j^\mathrm{cat}$ 는 차에서 상쇄되고, \emph{대칭점 검산}으로 두 끝점의 \emph{평균}은 로그 몫과
$(1-2\xi)$ 몫이 각각 부호 반대로 상쇄되어 $\tfrac12[V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^-)
+V_{\eq,j}^\mathrm{cat}(\xi_{s,j}^+)]=U_j^\mathrm{cat}$(흑연 식~\eqref{eq:hyssym} 과 동일 대수) —
분기가 $U_j^\mathrm{cat}$ 대칭이라는 성질이 LCO 에도 host-무관하게 성립한다.
```

- 삭제 근거: 단문+콜론 전보체를 접속 병합(내용 삭제 없음). 2문장 → 1문장.
- 물리 보존: 상쇄·평균=U·hyssym 동일 대수·host-무관 전부 존치. 사라진 물리 정보 0.

### 쌍 13 — (d) "같은 틀" 메타 문장 흡수 (L2149–2151)

**원문:**
```
흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 의 LCO 대입형이다. ``같은 틀''은 식을 생략한다는 뜻이
아니라 $\Omega_j\mapsto\Omega_j^\mathrm{cat}$, $U_j\mapsto U_j^\mathrm{cat}$, $j\in\mathcal J_\mathrm{LCO}$
를 실제로 넣는다는 뜻이다.
```

**교체:**
```
흑연 식~\eqref{eq:dUhys}$\cdot$\eqref{eq:Ubranch} 에 $\Omega_j\mapsto\Omega_j^\mathrm{cat}$,
$U_j\mapsto U_j^\mathrm{cat}$, $j\in\mathcal J_\mathrm{LCO}$ 를 실제로 넣은 대입형이다.
```

- 삭제 근거: "같은 틀은 식 생략이 아니라"는 집필 방침 메타 서술 — 치환 사상 3개를 대입형 문장에 직접 실으면 같은 내용이 남는다. 2문장 → 1문장. 직후 ★주의(γ_j·h_η,j 현상학적 지위 가드)는 **무변경 유지**.
- 물리 보존: 세 치환 사상 전부 존치. 사라진 물리 정보 0.

### 쌍 14 — ★분기 부호: sec:lco-direction 포인터화 (L2156–2159)

**원문:**
```
\textbf{★분기 부호.} 식~\eqref{eq:lco-Ubranch} 의 $\sigma_d$ 슬롯은 \S\ref{sec:lco-direction} 의 전극-중립
규약(식~\eqref{eq:lco-sigmaslot} --- 탈리튬화 $=+1$, LCO 하프셀에선 충전)을 받는다: 탈리튬화 가지가 위
($+\tfrac12$)$\cdot$리튬화 가지가 아래($-\tfrac12$)이고, 그 읽기로 ``탈리튬화 봉우리가 높은 전위 쪽''
(흑연 $U^{\dis}>U^{\chg}$ 와 동일한 물리)이 LCO 에서도 유지된다.
```

**교체:**
```
\textbf{★분기 부호} — 식~\eqref{eq:lco-Ubranch} 의 $\sigma_d$ 슬롯은 \S\ref{sec:lco-direction} 의 전극-중립
규약(식~\eqref{eq:lco-sigmaslot} --- 탈리튬화 $=+1$, LCO 하프셀에선 충전)을 받고, 가지 배치(탈리튬화
$+\tfrac12$ 위$\cdot$리튬화 $-\tfrac12$ 아래)와 ``탈리튬화 봉우리가 높은 전위 쪽'' 읽기는 같은 절 (b) 항과
동일하게 유지된다.
```

- 삭제 근거: 원칙 ④ — 가지 배치·봉우리 읽기·"흑연 $U^{\dis}>U^{\chg}$ 와 동일한 물리"는 \S sec:lco-direction (b) 항(L1889–1892)의 verbatim 재설명이라 포인터로 대체. 라벨 접기. 2문장 → 1문장.
- 물리 보존: σ_d 규약 내용(탈리튬화 +1, LCO=충전)·±½ 배정·봉우리 높낮이 읽기는 본문에 잔존, U^dis>U^chg 동치는 포인터 대상 절에 원문 그대로 존치. 사라진 물리 정보 0.

### 쌍 15 — (T2·T3): 라벨 접기 + 대입 문장 병합 (L2161–2174)

**원문:**
```
\textbf{(T2$\cdot$T3) order--disorder.}
$x\approx0.5$ 부근 monoclinic 초격자(점유 Li 와 빈자리의 교대 정렬)를 이루는 T2($\sim$4.05 V,
hex$\to$monoclinic)$\cdot$T3($\sim$4.17--4.20 V, monoclinic$\to$hex)는, 1차 전이의 2상 공존을 전이
진행률 $\xi_j$ 좌표의 정규용액으로 접을 때 나타나는 \emph{유효 인력} $\Omega_j^\mathrm{cat}>0$(미시
기원은 Li$\cdot$빈자리의 정렬 상호작용이고, 이중웰을 만드는 것은 이 유효 좌표의 볼록성 상실이다)이
만드는 상분리의 LCO 사례다. 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j=2,3$ 을 넣으면
[\[…\] 무변경: u_j·ΔU_j^hys·U_j^d 대입 3식]
로 T2$\cdot$T3 각각 열린다.
```

**교체:**
```
\textbf{(T2$\cdot$T3) order--disorder} —
$x\approx0.5$ 부근 monoclinic 초격자(점유 Li 와 빈자리의 교대 정렬)를 이루는 T2($\sim$4.05 V,
hex$\to$monoclinic)$\cdot$T3($\sim$4.17--4.20 V, monoclinic$\to$hex)는, 1차 전이의 2상 공존을 전이
진행률 $\xi_j$ 좌표의 정규용액으로 접을 때 나타나는 \emph{유효 인력} $\Omega_j^\mathrm{cat}>0$(미시
기원은 Li$\cdot$빈자리의 정렬 상호작용이고, 이중웰을 만드는 것은 이 유효 좌표의 볼록성 상실이다)이
만드는 상분리의 LCO 사례로, 식~\eqref{eq:lco-dUhys}$\cdot$\eqref{eq:lco-Ubranch} 에 $j=2,3$ 을 넣으면
[\[…\] 무변경: 동일 3식]
로 T2$\cdot$T3 각각 열린다.
```

- 삭제 근거: 라벨 접기 + "사례다. 식…" 2단을 "사례로, 식…" 연속문으로 병합(display 수식 무변경). 3문장 → 1문장.
- 물리 보존: 4.05 V·4.17–4.20 V·hex↔monoclinic·유효 인력 미시 기원·볼록성 상실 전부 존치. 사라진 물리 정보 0.

### 쌍 16 — ★Ω 와 config ΔS 구분: 단위 재진술 인라인화 (L2174–2180)

**원문:**
```
\textbf{★$\Omega$ 와 config $\Delta S$ 의 구분(혼동 가드).} 정렬의 charge-order
엔트로피 변화($\approx0.47$ J/(mol\,K)@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$
[tier A, Motohashi\cite{motohashi2009}])는 \emph{엔트로피} 값으로 표~\ref{tab:lco-staging}$\cdot$
식~\eqref{eq:lco-decomp} 의 $\Delta S_j^\mathrm{config}$ 슬롯(따라서 $U_j^\mathrm{cat}(T)$ 의 온도 이동)에
들어가지, spinodal 문턱을 정하는 \emph{상호작용 에너지} $\Omega_j^\mathrm{cat}$[J/mol]가 \emph{아니다} —
둘은 단위부터 다른 양(J/(mol\,K) 대 J/mol)이므로 ``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 식의 다리를
놓아선 안 되고 $\Omega_j^\mathrm{cat}$ 는 gap 을 정하는 별도 피팅 파라미터로 둔다.
```

**교체:**
```
\textbf{★$\Omega$ 와 config $\Delta S$ 의 구분(혼동 가드)} — 정렬의 charge-order
엔트로피 변화($\approx0.47$ J/(mol\,K)@$x{=}\tfrac12$, $\approx1.49$ J/(mol\,K)@$x{=}\tfrac23$
[tier A, Motohashi\cite{motohashi2009}])는 표~\ref{tab:lco-staging}$\cdot$식~\eqref{eq:lco-decomp} 의
$\Delta S_j^\mathrm{config}$ 슬롯($U_j^\mathrm{cat}(T)$ 의 온도 이동)에 들어가는 \emph{엔트로피}[J/(mol\,K)]이지
spinodal 문턱을 정하는 \emph{상호작용 에너지} $\Omega_j^\mathrm{cat}$[J/mol]가 \emph{아니므로},
``$0.47/1.49\to\Omega_j^\mathrm{cat}$'' 식의 다리를 놓지 말고 $\Omega_j^\mathrm{cat}$ 는 gap 을 정하는
별도 피팅 파라미터로 둔다.
```

- 삭제 근거: "둘은 단위부터 다른 양(J/(mol K) 대 J/mol)" 재진술을 두 양의 단위 태그 [J/(mol K)]·[J/mol] 인라인 병기로 흡수. 라벨 접기. 2문장 → 1문장.
- 물리 보존: 0.47/1.49 수치·x 조성·tier A·인용·양 단위 모두·금지 다리·별도 피팅 파라미터 지위 전부 존치. 사라진 물리 정보 0.

### 쌍 17 — (T1) MIT 2상역: 라벨 접기 + 슬롯 문장 병합 + 메타 괄호 삭제 (L2182–2202)

**원문:**
```
\textbf{(T1) MIT 2상역.}
T1($\sim$3.90 V, $x\approx0.94$--$0.75$, 절연체$\to$금속)의 구조적 2상 공존도 같은 정규용액 문턱을 받아
[\[…\] 무변경: u_1·ΔU_1^hys·U_1^d 대입 3식]
MIT 고유의 전자 자유도는 이 히스 gap 에 새 항으로 섞지 않는다 — 그 항은 이미
$\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^\mathrm{mol}(x,T)$(식~\eqref{eq:lco-decomp})를 통해 $U_1^\mathrm{cat}(T)$ 의 온도 이동
(식~\eqref{eq:lco-dUdT})에 들어간다. 곧 두 몫이 서로 다른 슬롯에 산다:
[식 환경 무변경: eq:lco-mit 박스]
이 분리가 config 2상역과 전자 엔트로피를 이중계산하지 않는 경계다(원 서술의 ``두 몫을 분리''를
슬롯 식으로 못박음).
```

**교체:**
```
\textbf{(T1) MIT 2상역} —
T1($\sim$3.90 V, $x\approx0.94$--$0.75$, 절연체$\to$금속)의 구조적 2상 공존도 같은 정규용액 문턱을 받아
[\[…\] 무변경: 동일 3식]
MIT 고유의 전자 자유도는 이 히스 gap 에 새 항으로 섞지 않는다 — 그 항은 이미
$\Delta S_{\rxn,1}^\mathrm{cat}=\Delta S_1^\mathrm{config}+\Delta S_1^\mathrm{vib}
+\Delta S_{e,1}^\mathrm{mol}(x,T)$(식~\eqref{eq:lco-decomp})를 통해 $U_1^\mathrm{cat}(T)$ 의 온도 이동
(식~\eqref{eq:lco-dUdT})에 들어가, 두 몫이 서로 다른 슬롯에 산다:
[식 환경 무변경: eq:lco-mit 박스]
이 분리가 config 2상역과 전자 엔트로피를 이중계산하지 않는 경계다.
```

- 삭제 근거: 라벨 접기, "들어간다. 곧 두 몫이 …" 를 "들어가, 두 몫이 …" 로 병합, 결구의 "(원 서술의 …를 슬롯 식으로 못박음)"은 집필 이력 메타 — 삭제. 5문장 → 3문장.
- 물리 보존: 3.90 V·x 범위·절연체→금속·gap 에 새 항 불가 가드·ΔS 3성분 분해식·온도 이동 경로·이중계산 방지 경계 전부 존치. 사라진 물리 정보 0.

### 쌍 18 — 도핑 보정 + ★슬롯 분리: 라벨 2개 접기 (L2204–2220)

**원문:**
```
\textbf{도핑 보정(우리 시료).}
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox$\cdot$전자항을 보존하되 order--disorder$\cdot$MIT 상전이를
억제한다 — 정규용액 틀에서 이는 pure-LCO 초기값 $\Omega_j^\mathrm{cat,pure}$ 를 도핑 피팅값
$\Omega_j^\mathrm{cat,dop}$ 로 낮추는 입력 변화다.
[... 문턱 극한 문장 + 식 환경(eq:lco-dope) 무변경 ...]
\textbf{★슬롯 분리.} 중심 전위의 미세 shift 는
같은 전이 dict 의 $U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로} 들어가며, ...
```

**교체:**
```
\textbf{도핑 보정(우리 시료)} —
Al$^{3+}$/Mg$^{2+}$ 비-redox 치환은 Co redox$\cdot$전자항을 보존하되 order--disorder$\cdot$MIT 상전이를
억제한다 — 정규용액 틀에서 이는 pure-LCO 초기값 $\Omega_j^\mathrm{cat,pure}$ 를 도핑 피팅값
$\Omega_j^\mathrm{cat,dop}$ 로 낮추는 입력 변화다.
[... 문턱 극한 문장 + 식 환경(eq:lco-dope) 무변경 ...]
\textbf{★슬롯 분리} — 중심 전위의 미세 shift 는
같은 전이 dict 의 $U_j^\mathrm{cat}$ 피팅값 이동으로 \emph{따로} 들어가며, ...
```

- 삭제 근거: 두 라벨 단독 문장을 각 본문 문장에 접합. 본문(Taylor 극한 8RT/3F·artanh 전개·T_c=Ω/2R·broadening 이관·GRAPHITE_STAGING_LIT 유비 괄호 포함)은 **전부 무변경**. 5문장 → 3문장.
- 물리 보존: 사라진 물리 정보 0(순수 접합).

---

## C. 절별 문장 수 전/후 셈

| 절 | 블록 | 전 | 후 | 감축 수단 |
|---|---|---|---|---|
| sec:lco-center | (a) | 3 | 2 | 쌍 1 |
| | (b) | 1 | 1 | 쌍 2(괄호만) |
| | (c) | 5 | 4 | 쌍 3 |
| | (d) 본문 | 2 | 2 | 쌍 4(포인터화) |
| | ★다온도 | 3 | 1 | 쌍 5 |
| | (부호 좌표) | 2 | 1 | 쌍 6 |
| | verifybox | 12 | 6 | 쌍 7·8·9 |
| **소계** | | **28** | **17** | **−39.3%** |
| sec:lco-hys | (a) | 3 | 2 | 쌍 10 |
| | (b) | 2 | 2 | — |
| | ★two-phase | 6 | 4 | 쌍 11 |
| | (c) | 3 | 2 | 쌍 12 |
| | (d) 본문 | 3 | 2 | 쌍 13 |
| | ★분기 부호 | 2 | 1 | 쌍 14 |
| | (T2·T3)+가드 | 5 | 2 | 쌍 15·16 |
| | (T1) | 5 | 3 | 쌍 17 |
| | 도핑+★슬롯 | 5 | 3 | 쌍 18 |
| **소계** | | **34** | **21** | **−38.2%** |

셈 규약: 마침표 종결 산문 문장(굵은 라벨 단독 포함, display 걸침 문장 = 1문장). display 수식·표·verifybox 환경 자체는 셈 제외. 수식 환경 변경 0건.

