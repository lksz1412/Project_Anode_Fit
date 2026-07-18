# A23_REVIEW — v1.0.22 심층 검토 FR-A23 (Ch3 §3.4 mech + §3.5 code)

- 대상: `Claude/docs/v1.0.22/_sections/ch3v22_sec04_mech.tex`(§3.4 기계 히스테리시스 Larché–Cahn+GS-1, 112행) + `ch3v22_sec05_code.tex`(§3.5 R6 코드 요구명세, 67행). 소속 = `ch3_si_v1.0.22.tex` 빌드(xr → Ch1·Ch2).
- 검토 창: FR-A23 (보고 전용 — 본문 무수정·git 무조작·`Codex/` 무접근). 4관점(보완/논리/설명/수식화) 전부 적용. GS-1·GS-2 는 정직 공백 — 메우는 제안 없음(보강·정밀화만).
- 검증 방법: §3.4 전 수식 재유도·수치 재계산(Λ_σ 차원·크기, ΔU@Ω=4RT 닫힌꼴 재평가) · xr 라벨 전수 역추적(eq:sm-muV·eq:Ubranch·eq:dUhys 원문 대조 + Ch3 로컬 라벨 전건) · 코드 원본 `v1.0.21/Anode_Fit_v1.0.21.py`(R6 미착수 기준) 및 `v1.0.22/Anode_Fit_v1.0.22.py` 실명 대조(클래스·진입점·Cbg·GRAPHITE_STAGING_LIT) · 서지 원장(V1022/V1021 REFERENCE_LEDGER) 대조 · 서지·정량 주장은 하이쿠 서브에이전트 doi 실검증(§4).
- 상태: 진행 중(수시 저장 — 발견별 즉시 append).

---

## 0. 발견 색인 (등급순)

| ID | 파일:행 | 유형 | 등급 | 요지 |
|---|---|---|---|---|
| A23-H1 | ch3v22_sec05_code.tex:44–45 | 논리(오귀속·유령 서지명) | H | G2 대조 데이터 "(\S\ref{ssec:si-blend-gs2}: gautam/moyassari/chatzogiannakis)" — `moyassari` 는 ch3 빌드 서지·V1 원장에 부재(유령), `gautam` 은 GS-2 절이 아니라 §3.2 표 각주 e 소재. R5 W3 초안(s35_code.tex:47) 이월 중 §3.3 만 W1 계열로 교체되며 생긴 불일치 |
| A23-H2 | ch3v22_sec05_code.tex:46–47 | 논리(게이트 식 결함) | H | G3 "∫(dQ/dV)dV=Q" — eq:blend-dqdv 의 $C_\bg$ 항·§3.5 자신의 "Cbg 전극 1회 가산" 조항과 충돌: $C_\bg\ne0$ 이면 문자 그대로는 통과 불능(적분값 $=Q+\int C_\bg\,dV$). 배경 차감·검사 창·공차 명시 필요 |
| A23-H3 | ch3v22_sec05_code.tex:6–8 | 논리(판정 어휘 오귀속) | H | "재해석 노드(N2·N4·N6)" — tab:si-survival 규범 판정은 재해석 3(N1·N2·N4)·부분 2(N6·N7): N6 은 "부분". §3.1 ssec:si-guide 도 "재해석·부분(N1·N2·N4·N6·N7)" 병기 — §3.5 만 N6 을 재해석으로 오분류 |
| A23-M1 | ch3v22_sec04_mech.tex:72–74 | 논리(정밀화) | M | "순수 탄성 ⇒ σ_h 가 θ 의 단일값" 은 준정적 극한 조건부 — 유한 율속 확산 유기 탄성 응력은 가지별 상이(N8 분리 논법 자리와 접속해 조건 한 구절 명시) |
| A23-M2 | ch3v22_sec04_mech.tex:89–99 | 보완 | M | keybox 제목 "4분류" 인데 명시 진단은 2갈래 — §3.3 GS-2 불릿(3분류 소거 완비)과 양식 비대칭·P3-4 분리 진단 취지: 나머지 두 분류(수치해법·정의상 implicit) 소거 불릿 append |
| A23-M3 | ch3v22_sec04_mech.tex:62–68 | 보완 | M | verifybox "같은 v̄_Li" — 300% 만충 팽창에서 읽는 것은 평균 부분몰 부피, eq:si-lcmu 의 국소 ∂v/∂(Li) 와의 동일시는 규모 수준임을 명시(팽창 선형성은 본문 미접근 미검증 — 안전한 약형 제안) |
| A23-M4 | ch3v22_sec04_mech.tex:84–87 | 보완 | M | 구성식 세 갈래 중 첫 갈래(항복·유동 탄소성)만 무인용 — bower2011(JMPS 59, 804–828; DOI Crossref 검증) 앵커 후보 + 원장 등재 선행 |
| A23-M5 | ch3v22_sec04_mech.tex:56–59 | 보완 | M | (d) 방향 결론이 기대는 "리튬화=압축·탈리튬화=인장" 실측 입력이 (d) 시점 무인용 — sethuraman_stressevo2010 부착(수치 없이 배정 사실만) |
| A23-M6 | ch3v22_sec05_code.tex:11–14·20–21 | 보완 | M | bit-exact 실현 조건 미명세 — f_Si=0 단락 위임(0×NaN·−0.0·가산 순서 함정)·Cbg 는 흑연 인스턴스에 배치(진입점이 내부 가산: v1.0.21 L455–458·L529–533)·v1.0.21 LCO seam "byte 0-diff" 선례 계승 |
| A23-M7 | ch3v22_sec05_code.tex:24–29 | 보완(논리 정밀화) | M | 전극 공통 입력(σ_d·\|I\|·R_n·T) 공유 규정 부재(Cbg 만 규정) + "V_app 배열"↔"공통 V_n" 병치의 P3-1 다리(\|I\|→0 에서 V_n=V_app, eq:vn) 명시 |
| A23-M8 | ch3v22_sec05_code.tex:43–45 | 보완 | M | G2 "연속(불연속 점프 없음)" 판정 절차 부재(확인 가능한 조건 의무) + f_Si→0⁺ 끝점 수렴(eq:blend-limit "R6 게이트 이론짝") 이 게이트 사슬에서 누락 + 실측 대조와 연속성 검사 분리 |
| A23-M9 | ch3v22_sec05_code.tex:32–36 | 보완 | M | "값은 표 tab:si-cases 의 시연값" — 표는 케이스 집계뿐, GRAPHITE_STAGING_LIT 대응 리스트가 요구하는 전이별 {U,w,Q} 부재 → 집계 제약+§3.2 개형 사실 기반 구성 규칙 명시 |
| A23-M10 | ch3v22_sec05_code.tex:37–38·51–54 | 보완 | M | 공백 계승 기본값 정책 미명세 — Λ_σ 훅 수치 기본값 금지(None; §3.4 "확인 필요" 1:1 계승)·σ_h 입력 형태 규정·SiOx "placeholder 또는 None" 우선순위·provenance 주석 의무 |
| A23-L1 | ch3v22_sec04_mech.tex:38–40 | 설명 | L | "상수 덩이가 상쇄된다" — 상쇄 덩이 μ⁰(θ_eq)−μ^metal 은 θ 의존(V_eq⁰(θ)) — "무응력 몫" 으로 정밀화(ch1 (c) "상수 덩이(μ_metal)" 관용구의 오전이) |
| A23-L2 | ch3v22_sec04_mech.tex:27–28 | 설명 | L | 새 기호 문장이 Ω_j 무관만 밝힘 — 같은 절 (d) 에 병존하는 방향 부호 σ_d 와의 시각 유사(σ 공유·첨자 1자) 주의 한 구절 |
| A23-L3 | ch3v22_sec04_mech.tex:56–60 | 수식화 | L | (d) 부호 읽기 산문 사슬 → 함의 사슬 수식 1행 대체안(σ_d=∓1 ⇒ σ_h≶0 ⇒ Λ_σσ_h≶0 ⇒ V^dis>V^chg) |
| A23-L4 | ch3v22_sec04_mech.tex:8–9·94 (+ §3.3 동형) | 문체 | L | "§3.1 사실 vi"·"§3.2" 절 번호 하드코딩 — 같은 문서 안 \S\ref 혼용(sec05:60 은 \ref 사용) — \S\ref{sec:si-map}·\S\ref{sec:si-cases} 통일(장 전체 일괄은 마스터 몫) |
| A23-L5 | ch3v22_sec05_code.tex:5 | 설명 | L | "doc-leads 요구명세" 용어 첫 등장 무주해 — 괄호 주해(문서 선도 — 문서가 계약 확정·코드가 따름) |
| A23-L6 | ch3v22_sec05_code.tex:45·60 (+ notation:33) | 문체 | L | 조판 비일관 묶음 — "f$_\mathrm{Si}$"(수식 분절) vs $f_\mathrm{Si}$·본문 "($G1$)" 이탤릭 vs codebox \textbf{G1}·σ_h 첨자체(italic h ↔ upright h) 혼재 |
| A23-L7 | ch3v22_sec04_mech.tex:92–93 | 설명 | L | "(경로 의존·비가역, 비열역학)" — 소성 소산도 비평형 열역학 소관: "평형 열역학 밖" 으로 정밀화(같은 절 "평형 자유에너지 g(ξ) 로 적히는 양이 아니고" 와 정렬) |
<!-- IDX -->

---

## 1. H 등급 (논리/물리 오류·오귀속)

### A23-H1 — G2 대조 데이터의 유령 서지명(moyassari)·오지시(gautam)
- 파일:행 = `ch3v22_sec05_code.tex:44–45` · 유형 = 논리(오귀속·유령 서지명) · 등급 = **H**

현행(축자):
```latex
$\cdot$ \textbf{G2 스윕 연속성}: $f_\mathrm{Si}\in(0,0.3]$ 에서 곡선이 $f_\mathrm{Si}$ 에 연속(불연속 점프 없음)
--- 대조 데이터는 f$_\mathrm{Si}$ 스윕 실측(\S\ref{ssec:si-blend-gs2}: gautam/moyassari/chatzogiannakis, tier-A).
```

제안(완성 LaTeX — 두 경로 중 마스터 택1):

경로 A(최소 수정 — 현존 자산만으로 재지시, 45행 대체):
```latex
--- 대조 데이터는 $f_\mathrm{Si}$ 스윕 실측(5--20 wt\%: \cite{gautam_blend2024}[표~\ref{tab:si-cases} 각주 $e$]$\cdot$30 wt\%: \cite{chatzogiannakis_blend2025}[\S\ref{ssec:si-blend-gs2}], tier-A).
```

경로 B(보강 — R5 W3 자산 [V22-R5-17 f_Si 0~30% 스윕 커버] 복원; `moyassari_blend2022` 의 V1 원장 등재가 선행 조건):
```latex
--- 대조 데이터는 $f_\mathrm{Si}$ 스윕 실측(\cite{gautam_blend2024}: 5--20$\cdot$\cite{moyassari_blend2022}: 0--20$\cdot$\cite{chatzogiannakis_blend2025}: 30 wt\%, tier-A --- $[0,0.3]$ 전 구간 커버).
```
경로 B 의 bib 추가분(`ch3v22_bib.tex` — comp_R4 검증 서지 그대로, DOI 는 본 창 하이쿠 재검증 완료 §4-A5):
```latex
\bibitem{moyassari_blend2022} E. Moyassari, T. Roth, S. K\"ucher, C.-C. Chang, S.-C. Hou, F. B. Spingler, and A. Jossen, ``The Role of Silicon in Silicon-Graphite Composite Electrodes Regarding Specific Capacity, Cycle Stability, and Expansion,'' \emph{J. Electrochem. Soc.} \textbf{169}(1), 010504 (2022). DOI: 10.1149/1945-7111/ac4545. [Si 0--20 wt\% 스윕 딜라토메트리$\cdot$전기화학 동시 실측.]
```

근거:
1. `moyassari` 는 ch3 빌드 어디에도 실체가 없다 — `ch3v22_bib.tex` 전수(14+19종)에 \bibitem 부재, `V1022_REFERENCE_LEDGER.md` V1 목록 부재(전수 grep), ch3 다섯 절 본문 \cite 부재. 유일한 실체는 결과물 작업 파일(comp_R4/upgraded/BLEND_UP.md #4, comp_R5/W2·W3)뿐.
2. `gautam_blend2024` 는 실존·V1 이나 인용 위치는 §3.2 표~tab:si-cases 각주 $e$(Si15Gr75 블렌드 ICE) — 지시된 \S\ref{ssec:si-blend-gs2}(GS-2 srcbox)의 인용은 ai/chatzogiannakis/zhan/tu 넷뿐. 괄호의 절 지시가 두 이름에 대해 틀린다.
3. 계보 추적: 채택본 §3.5 는 comp_R5/W3/s35_code.tex:47 을 사실상 축자 이월("gautam/moyassari/chatzogiannakis" 동일) — 그러나 W3 에서는 s33_blend.tex 가 moyassari 를 GS-2 에 실제 인용했고, 채택본 §3.3 은 W1 기반이라 moyassari·gautam 이 탈락. 절간 짝이 깨진 채 §3.5 만 남았다.
4. 원장 규칙("본문 \cite 는 본 원장 V1 키만") — 경로 B 채택 시 등재 선행 필수. moyassari DOI·서지·"0–20 wt%" 스윕 범위는 본 창 하이쿠 서브가 Crossref 실검증(§4-A5 — 초록에서 "silicon contents ranging from 0 wt% to 20 wt%" 확인).

### A23-H2 — G3 용량 보존식이 자기 명세의 $C_\bg$ 조항과 충돌
- 파일:행 = `ch3v22_sec05_code.tex:46–47` · 유형 = 논리(게이트 식 결함) · 등급 = **H**

현행(축자):
```latex
$\cdot$ \textbf{G3 용량 보존}: $\int(\dd Q/\dd V)\,\dd V=Q=Q_\mathrm{gr}+Q_\mathrm{Si}$ 가 $f_\mathrm{Si}$
전 구간에서 성립(host 합이 총용량을 정확히 재현).
```

제안(완성 LaTeX):
```latex
$\cdot$ \textbf{G3 용량 보존}: 평형 산출에서 배경을 뺀 적분
$\int\bigl(\dd Q/\dd V-C_\bg\bigr)\,\dd V=Q=Q_\mathrm{gr}+Q_\mathrm{Si}$ 가 $f_\mathrm{Si}$
전 구간에서 성립(host 합이 총용량을 정확히 재현 --- 식~\eqref{eq:blend-dqdv} 에서 용량을 나르는 것은
host 이중합 몫뿐). 검사 창은 전 전이를 덮게 잡고(모든 $U_j^\mathrm{host}$ 에서 $k\,w_j^\mathrm{host}$
이상 여유, 잘림 오차 상한 $\sum_{\mathrm{host},j}Q_j^\mathrm{host}e^{-k}$), 구적$\cdot$잘림 합산 상대
공차는 R6 이 명시해 고정한다(제안 예: $k{=}20$, $|\Delta|/Q\le10^{-6}$).
```

근거(재계산):
1. 식~eq:blend-dqdv 는 $\dd Q/\dd V|_{U_\mathrm{oc}}=C_\bg+\sum_\mathrm{host}\sum_j Q_j\xi(1-\xi)/w_j$ — host 몫만 적분하면 $\int Q_j\,|\dd\xi_j/\dd V|\,\dd V=Q_j[\xi]_0^1=Q_j$(logistic 에서 $\xi(1-\xi)/w_j=|\dd\xi_j/\dd V|$, 치환적분), 합 $=Q$ 재유도 일치. 그러나 반환 배열 전체를 적분하면 $Q+\int C_\bg\,\dd V$ — $C_\bg\ne0$ 이면 현행 등식은 항상 깨진다(v1.0.21 데모부터 `Cbg=0.05` 비영·코드는 `equilibrium`/`dqdv` 안에서 배경을 내부 가산: L455–458·L529–533).
2. §3.5 자신이 24–29행에서 "Cbg 는 전극 단위로 한 번만 더한다" 고 배경 가산을 명시 — 곧 게이트가 자기 명세의 산출물 정의와 모순. "확인 가능한 조건" 게이트 원칙상 문자 그대로 실행하면 영구 FAIL 인 식은 게이트로 무효.
3. 유한 창 잘림: logistic 꼬리 질량은 중심에서 $k\,w$ 밖에 $\approx Q_je^{-k}$ — $k{=}10$ 이면 $4.5\times10^{-5}$ 상대라 공차 $10^{-6}$ 과 비정합, $k{=}20$ 이면 $2\times10^{-9}$ 로 정합(제안 수치는 물리값 아닌 코드 QA 파라미터 — R6 확정 소관).
4. $Q$ 의 정의 대조: eq:blend-balance 는 $Q\equiv\sum_\mathrm{host}Q^\mathrm{host}$(배경 불포함) — 따라서 등식 우변에 배경 몫이 들어올 여지도 없음(배경 차감이 유일한 정합 방향).

### A23-H3 — "재해석 노드(N2·N4·N6)" 가 생존 지도 판정과 상충
- 파일:행 = `ch3v22_sec05_code.tex:6–8` · 유형 = 논리(판정 어휘 오귀속) · 등급 = **H**

현행(축자):
```latex
\emph{코드는 생존 지도를 실행 가능하게 만든 것}이다: N9(이월)는 $f_\mathrm{Si}{=}0$ bit-exact
게이트로, 재해석 노드(N2$\cdot$N4$\cdot$N6)는 Si 케이스 셋 파라미터로, 새 물리$\cdot$비가산 공백
(GS-1$\cdot$GS-2)은 \emph{명시적 코드 경계}로 들어간다(조용히 날조하지 않는다).
```

제안(완성 LaTeX — 최소 치환):
```latex
\emph{코드는 생존 지도를 실행 가능하게 만든 것}이다: N9(이월)는 $f_\mathrm{Si}{=}0$ bit-exact
게이트로, 재해석$\cdot$부분 노드 중 케이스 성분이 담는 셋(N2$\cdot$N4$\cdot$N6)은 Si 케이스 셋 파라미터로, 새 물리$\cdot$비가산 공백
(GS-1$\cdot$GS-2)은 \emph{명시적 코드 경계}로 들어간다(조용히 날조하지 않는다).
```

근거:
1. 규범 = 표~tab:si-survival(§3.1) 캡션의 집계: "재해석 3(N1·N2·N4)·부분 2(N6·N7)" — N6(peak)의 판정은 **부분**("날카로운 peak 문법은 Li$_{15}$Si$_4$ ... 두-상에만"), 재해석이 아니다.
2. §3.1 ssec:si-guide 는 정확히 병기한다: "\textbf{재해석$\cdot$부분}으로 표시된 노드(N1·N2·N4·N6·N7)는 §3.2 의 케이스별 활물질이 실증한다" — §3.5 도입만 N6 을 "재해석" 으로 승격시켜 장 내 판정 어휘가 갈라진다(P3-7 의 명칭 혼동 금지 규율과 같은 계열).
3. 다만 내용 선정 자체는 타당 — 케이스 전이 리스트가 실제로 담는 것은 중심(N2)·폭(N4)·이산 peak 유무(N6)다(N1 은 Rn, N7 은 기작이라 리스트 파라미터가 아님). 오류는 판정 라벨뿐이므로 최소 치환으로 잡는다(P5 보존).
<!-- H -->

---

## 2. M 등급 (의미·이해 실질 개선)

### A23-M1 — "순수 탄성 ⇒ σ_h 단일값" 은 준정적 한계에서만 성립
- 파일:행 = `ch3v22_sec04_mech.tex:72–74` · 유형 = 논리(정밀화) · 등급 = **M**

현행(축자):
```latex
식~\eqref{eq:si-coupling} 은 \emph{가역} 결합이다: 만약 변형이 순수 탄성이라면 $\sigma_\mathrm{h}$ 가
$\theta$ 의 단일값 함수이므로 닫힌 사이클에서 $\sigma_\mathrm{h}^{\dis}=\sigma_\mathrm{h}^{\chg}$ 가 되어
$\Delta V^\mathrm{mech}=0$ --- 히스테리시스가 없다.
```

제안(완성 LaTeX):
```latex
식~\eqref{eq:si-coupling} 은 \emph{가역} 결합이다: 만약 변형이 순수 탄성이라면 준정적 극한(농도 구배가
풀린 $|I|\to0$ --- 본 절의 평형 문법)에서 $\sigma_\mathrm{h}$ 가
$\theta$ 의 단일값 함수이므로 닫힌 사이클에서 $\sigma_\mathrm{h}^{\dis}=\sigma_\mathrm{h}^{\chg}$ 가 되어
$\Delta V^\mathrm{mech}=0$ --- 히스테리시스가 없다(유한 율속의 확산 유기 \emph{탄성} 응력은 농도 場을
따라 가지별로 다르지만, 꼬리처럼 $|I|\to0$ 에서 소멸하는 몫이라 잔여 갈림이 아니다 --- §3.1 N8 행의
분리 논법과 같은 자리).
```

근거(재유도): 탄성이라도 유한 율속에서는 농도 구배가 만드는 확산 유기 응력이 존재하고 그 부호가 가지별로 다르다(리튬화 = 표면 Li 과잉 → 표면 압축 / 탈리튬화 = 표면 인장) — 곧 "순수 탄성 ⇒ $\sigma_\mathrm{h}(\theta)$ 단일값" 은 무조건 참이 아니라 농도 場이 풀린 준정적 극한에서 참. 이 극한에서는 균일 $\theta$·고정 경계조건으로 $\sigma_\mathrm{h}$ 가 상태함수가 되어 원문 결론이 정확히 성립. 본 장의 히스 논의가 겨냥하는 것도 $|I|\to0$ 잔여 갈림(§3.1 N8 행: "꼬리는 소멸해도 기계 히스는 남아")이므로 한 구절의 조건 명시로 논증이 무결해진다. 전문 독자가 바로 반문할 지점(확산 유기 응력 히스테리시스와의 구분)을 선제 차단하는 실질 이득.

### A23-M2 — GS-1 keybox "4분류" 가 2분류만 명시 — 나머지 두 분류 소거 부재
- 파일:행 = `ch3v22_sec04_mech.tex:89–99` · 유형 = 보완 · 등급 = **M**

현행(축자 — keybox 전문 중 구조 해당부):
```latex
\textbf{GS-1 공백 4분류.}
$\cdot$ \textbf{물리 가정 충돌} --- 골격의 히스 gap(식~\eqref{eq:dUhys})은 정규용액 이중웰($\Omega_j>2RT$)이라는
\emph{열역학 쌍안정}에서 온다. Si 갈림은 소성 \emph{소산}(경로 의존$\cdot$비가역, 비열역학)에서 온다. 두
기작이 물리적으로 다르므로, ``히스테리시스 $=$ 평형 자유에너지 분기'' 라는 골격 가정이 Si 지배 기작과
충돌한다(§3.1 N3$\cdot$§3.2 열 서명 정합).
$\cdot$ \textbf{유도 미완결(범위 선언, 논리 공백 아님)} --- 가역 결합(식~\eqref{eq:si-coupling})은
닫혔다. 닫히지 않는 것은 $\sigma_\mathrm{h}(\theta,\text{이력})$ 의 구성식(식~\eqref{eq:si-plastic})이며,
이는 소산 역학 하위 모형으로 본 장 범위 밖이다(마스터플랜 Non-goals: 1차원리 기계 히스는 Larché--Cahn
접속이 닫히는 범위까지만 --- 못 닫으면 정직 공백 유지). 유사 유도로 소성 구성식을 날조하지 않는다.
```

제안(완성 LaTeX — 둘째 불릿 뒤 append, 기존 두 불릿 무변경):
```latex
$\cdot$ \textbf{나머지 두 분류 소거} --- \emph{수치해법 필요} 아님(가역 결합~\eqref{eq:si-coupling} 은
닫힌 꼴이고, 반전의 수치 지위는 블렌드 중심식 쪽 소관 그대로 \S\ref{sec:si-blend}), \emph{정의상
implicit formulation} 도 아님(공백은 어느 식의 음함수 지위가 아니라
$\sigma_\mathrm{h}(\theta,\text{이력})$ 구성식의 \emph{부재} 자체다). 곧 GS-1 $=$ 물리 가정 충돌 $+$
범위 밖 하위 모형(범위 선언).
```

근거: (i) 박스 제목이 "4분류" 인데 명시 판정은 두 갈래뿐 — 독자가 나머지 두 분류(수치해법 필요·정의상 implicit)의 판정을 스스로 메워야 한다. (ii) 짝 절인 §3.3 GS-2 불릿은 완전 소거를 수행한다("논리 공백(식의 결함)도, 수치해법 문제(유일근은 이미 보증됨)도, 정의상 implicit(그것은 $U_\mathrm{oc}$ 자체의 지위)도 아니다") — 같은 장 안 두 공백 선언의 진단 양식이 비대칭. (iii) P3-4 의 "4 분류 중 무엇인지 **분리 진단**" 규율의 취지(전 분류 대조) 정합. 기존 자산 무삭제 — 순수 append.

### A23-M3 — Λ_σ 크기 검산의 "같은 v̄_Li" 다리: 평균 부분몰 부피임을 명시
- 파일:행 = `ch3v22_sec04_mech.tex:62–68` (연계 19–21) · 유형 = 보완 · 등급 = **M**

현행(축자):
```latex
크기 검산(정성) --- 식~\eqref{eq:si-coupling} 의 $\Lambda_\sigma=\bar v_\mathrm{Li}/F$ 는 실측
응력--전위 결합 $\sim100$--$120$ mV/GPa 그 자체다(tier A\cite{sethuraman_stresspot2010}). 같은
$\bar v_\mathrm{Li}$ 가 Si 의 $\sim300\%$ 만충 팽창을 부르는 부피이므로(tier A\cite{beaulieu2001}), 두
tier-A 실측(팽창 크기와 결합 기울기)은 $\bar v_\mathrm{Li}$ 를 통해 서로 정합하며 $\Lambda_\sigma$ 가
$O(100\ \mathrm{mV/GPa})$ 규모임이 자연스럽다.
```

제안(완성 LaTeX — 둘째 문장 치환):
```latex
같은
$\bar v_\mathrm{Li}$ 가 Si 의 $\sim300\%$ 만충 팽창을 부르는 부피이므로(tier A\cite{beaulieu2001} ---
여기서 읽는 것은 만충 팽창 부피를 삽입 Li 량으로 나눈 \emph{평균} 부분몰 부피의 규모이며, 정의
\eqref{eq:si-lcmu} 의 국소 $\partial v/\partial(\text{Li 함량})$ 와는 규모 수준에서 동일시한다), 두
tier-A 실측(팽창 크기와 결합 기울기)은 $\bar v_\mathrm{Li}$ 를 통해 서로 정합하며 $\Lambda_\sigma$ 가
$O(100\ \mathrm{mV/GPa})$ 규모임이 자연스럽다.
```

근거: (i) $\Lambda_\sigma=\partial V/\partial\sigma_\mathrm{h}$ 의 $\bar v_\mathrm{Li}$ 는 정의상 해당 $\theta$ 에서의 **국소** 기울기 $\partial v/\partial(\text{Li 함량})$ — 300\% 만충 팽창에서 읽히는 것은 **평균** 몫(총팽창/총삽입량). 두 값의 동일시는 팽창의 Li 함량 근사 선형성이 있어야 정확해지는데, 그 선형성 명제는 본 창 접근 범위에서 미검증(beaulieu2001 초록은 "strains approaching or exceeding 100\%" 까지만 공개 — §4-A3, 본문 미접근). 따라서 검증 없이도 참인 "평균 규모로 읽는다" 명시가 안전한 보강이며, 이는 현행 "정성 정합(규모 일치)까지만" 선언과도 정확히 일치. (ii) 규모 자체는 본 창이 재계산으로 확인: $\bar v_\mathrm{Li}\approx3\times12.06/3.75\ \mathrm{cm^3/mol}=9.65\times10^{-6}\ \mathrm{m^3/mol}$ ⇒ $\Lambda_\sigma=\bar v/F=1.00\times10^{-10}$ V/Pa $=100$ mV/GPa — 실측 100–120 mV/GPa(§4-A1 에서 초록 수치 재확인)와 정합. 이 수치는 검증 표 밖 입력(Si 몰부피·만충 조성)을 쓰므로 본문 충전은 제안하지 않음(현행 "정확값은 확인 필요" 존중 — 로그 기록만). (iii) 대안(팽창 선형성을 명시하는 강한 판)은 beaulieu2001 본문 확인 후에만 — 추가 후보로 부수 관찰에 기재.

### A23-M4 — 소성 구성식 세 갈래 중 첫 갈래(탄소성)만 무인용
- 파일:행 = `ch3v22_sec04_mech.tex:84–87` · 유형 = 보완 · 등급 = **M**

현행(축자):
```latex
이며, 이 $\Delta V^\mathrm{mech}$ 를 예측하려면 $\sigma_\mathrm{h}(\theta,\text{이력})$ 의 \emph{구성식}
--- 항복 응력$\cdot$유동 법칙의 탄소성, 또는 입자$\cdot$SEI 점탄소성\cite{koebbing2024}, 또는 다단
상전이$\cdot$결정화 경로 분기의 현상학\cite{jiang_sihys2020} --- 이 필요하다.
```

제안(완성 LaTeX — V1 원장 등재 선행 조건):
```latex
이며, 이 $\Delta V^\mathrm{mech}$ 를 예측하려면 $\sigma_\mathrm{h}(\theta,\text{이력})$ 의 \emph{구성식}
--- 항복 응력$\cdot$유동 법칙의 탄소성\cite{bower2011}, 또는 입자$\cdot$SEI 점탄소성\cite{koebbing2024}, 또는 다단
상전이$\cdot$결정화 경로 분기의 현상학\cite{jiang_sihys2020} --- 이 필요하다.
```
bib 추가분(`ch3v22_bib.tex` — DOI 하이쿠 Crossref 검증 완료 §4-B6):
```latex
\bibitem{bower2011} A. F. Bower, P. R. Guduru, and V. A. Sethuraman, ``A finite strain model of stress, diffusion, plastic flow, and electrochemical reactions in a lithium-ion half-cell,'' \emph{J. Mech. Phys. Solids} \textbf{59}(4), 804--828 (2011). DOI: 10.1016/j.jmps.2011.01.003. [Si 음극 탄소성(항복$\cdot$유동) 구성식 결합 원전 계열.]
```

근거: (i) 세 갈래 병렬 나열에서 뒤의 두 갈래는 앵커(koebbing2024·jiang_sihys2020)가 있는데 첫 갈래만 무인용 — §3.1 말미 총람 문장("기계 히스의 모델 계보는 ... 이 준다")도 같은 두 키만 들어, 탄소성 갈래는 장 전체에서 서지 앵커가 없다. (ii) 후보는 본문이 이미 인용하는 sethuraman 실측 계열의 같은 그룹 이론편(Bower–Guduru–Sethuraman, JMPS 2011)이라 계보 정합 — DOI·서지 Crossref 실검증 완료(§4-B6). (iii) 이것은 GS-1 을 메우는 제안이 아니다: 공백(구성식 접속)은 그대로 두고, 나열된 갈래의 서지 병렬성만 완결한다. 등재는 원장 규칙대로 [검증→등재→인용] 선행.

### A23-M5 — (d) 의 "리튬화=압축·탈리튬화=인장" 방향 입력이 무인용
- 파일:행 = `ch3v22_sec04_mech.tex:56–59` · 유형 = 보완 · 등급 = **M**

현행(축자):
```latex
리튬화(충전 라벨, $\sigma_d{=}-1$)는 압축($\sigma_\mathrm{h}<0$)이라 전위를 아래로, 탈리튬화(방전 라벨,
$\sigma_d{=}+1$)는 인장 쪽이라 위로 옮긴다 --- 곧 탈리튬화 가지가 높은 전위에 남아
$V^{\dis}>V^{\chg}$ 로, 흑연 분기 식~\eqref{eq:Ubranch} 의 부호($U_j^{\dis}>U_j^{\chg}$)와 \emph{같은}
방향이다(기원은 다르나 부호 규약은 일관).
```

제안(완성 LaTeX):
```latex
리튬화(충전 라벨, $\sigma_d{=}-1$)는 압축($\sigma_\mathrm{h}<0$)이라 전위를 아래로, 탈리튬화(방전 라벨,
$\sigma_d{=}+1$)는 인장 쪽이라 위로 옮긴다(가지별 압축/인장 배정은 in~situ 응력 실측이 직접
보인다\cite{sethuraman_stressevo2010}) --- 곧 탈리튬화 가지가 높은 전위에 남아
$V^{\dis}>V^{\chg}$ 로, 흑연 분기 식~\eqref{eq:Ubranch} 의 부호($U_j^{\dis}>U_j^{\chg}$)와 \emph{같은}
방향이다(기원은 다르나 부호 규약은 일관).
```

근거: (d) 의 방향 결론($V^{\dis}>V^{\chg}$)은 순수 이론이 아니라 "리튬화 가지=압축, 탈리튬화 가지=인장" 이라는 **실측 입력**에 기댄다 — 그런데 이 입력의 인용은 §3.4 안에서 소성 문단(75–77행, 압축 측)에만 있고 (d) 시점·인장 측은 무인용이며, §3.1 사실 vi 도 인장 배정을 명시하진 않는다. 같은 tier-A 실측 논문이 두 가지 응력 이력을 모두 보고하는 것으로 v1.0.21 원장에서 검증·승계된 앵커이므로 인용 1개 부착이 자연스럽다. 단 인장 측 정량(예: $\sim+1$ GPa)의 본문 수치 확인은 본 창 접근 한계로 미검증(§4-A2 — 초록 미접근·메타데이터만 확정) — 제안은 수치 없이 "배정" 사실만 걸므로 이 한계와 무충돌.
### A23-M6 — bit-exact 계약의 실현 조건 미명세(단락 위임·Cbg 배치)
- 파일:행 = `ch3v22_sec05_code.tex:11–14·20–21` · 유형 = 보완 · 등급 = **M**

현행(축자):
```latex
신규 클래스 \code{BlendedAnodeDQDV(f\_Si, si\_case)}(제안)는 기존 흑연 클래스
\code{GraphiteAnodeDischargeDQDV} 를 \emph{합성}으로 감싼다 --- 두 host 인스턴스(흑연$\cdot$Si)를 각각
표준 진입점(\code{curve}$\cdot$\code{dqdv}$\cdot$\code{equilibrium})으로 평가하고, 공통 전위 축에서
합친다. 최우선 계약은 하위호환이다:
```
```latex
--- 식~\eqref{eq:blend-balance} 의 검산 (ii)($Q_\mathrm{Si}{=}0$ 회수)의 코드판이다. Si 합이 통째로
사라지므로 반환 배열이 흑연 단독 경로와 부동소수점까지 동일해야 한다(회귀 게이트).
```

제안(완성 LaTeX — 21행 뒤 append):
```latex
bit-exact 의 실현 조건도 요구에 넣는다: (i) $f_\mathrm{Si}=0$ 에서는 Si 인스턴스를 \emph{평가하지
않고} 흑연 인스턴스 산출을 그대로 반환한다(단락 위임 --- $0\times$배열 가산 방식은
$0\times\mathrm{NaN}=\mathrm{NaN}$$\cdot$$-0.0$ 부호 소실$\cdot$가산 순서 재결합으로 bit 동일성을 깨뜨릴
수 있다); (ii) 전극 배경 \code{Cbg} 는 흑연 인스턴스에 실어 전달하고 Si 인스턴스는 \code{Cbg}$=0$ 으로
생성한다 --- 표준 진입점이 배경을 인스턴스 내부에서 가산하므로, 이렇게 해야 $f_\mathrm{Si}=0$ 경로의
부동소수점 \emph{가산 순서}까지 흑연 단독과 같아지고 \S\ref{ssec:code-synth} 의 전극 단위 1회 가산도
동시에 만족된다(전례 $=$ v1.0.21 LCO seam 의 ``흑연 곡선 byte 0-diff 보장 --- 가산$\cdot$부동소수점 연산
자체가 없음'' 설계). 계약~\eqref{eq:si-code-bitexact} 은 세 표준 진입점 모두에 적용된다.
```

근거(코드 대조): (i) 코드 원본 확인 — `GraphiteAnodeDischargeDQDV.equilibrium`(v1.0.21:451–468)·`dqdv`(:471~, 배경 :529–533)는 **인스턴스별 Cbg 를 내부에서 가산**한다. 래퍼가 전극 Cbg 를 자기 수준에서 더하면 흑연 단독 $(C_\bg+\sum\mathrm{tr})$ 와 블렌드 $((0+\sum\mathrm{tr})+C_\bg)$ 의 가산 순서가 달라 부동소수점 비결합성으로 bit-exact 가 일반적으로 깨진다. (ii) $0\times$Si 가산 방식은 Si 평가가 NaN/inf 를 내는 파라미터에서 NaN 전파, $-0.0$ 케이스에서 비트 불일치 가능. (iii) 선례 실존 — v1.0.21:630 주석 "흑연 곡선 byte 0-diff 보장(가산·부동소수점 연산 자체가 없음)": LCO seam 이 같은 원리로 설계됨 — 요구명세가 이 선례를 계승 조건으로 명시하면 G1 이 구현 재량에 좌우되지 않는다. 현행 "Si 합이 통째로 사라지므로 ... 동일해야 한다" 는 결과 요구만 있고 실현 경로가 열려 있어, 자연스러운 구현(가중합)이 게이트에 걸리는 함정이 남는다.

### A23-M7 — 전극 공통 입력(σ_d·|I|·R_n·T) 공유 규정 부재 + V_app/V_n 위계 다리(P3-1)
- 파일:행 = `ch3v22_sec05_code.tex:24–29` · 유형 = 보완(논리 정밀화 포함) · 등급 = **M**

현행(축자):
```latex
용량은 $f_\mathrm{Si}$ 로 배분되고(식~\eqref{eq:blend-balance} 의 정의: $Q_\mathrm{Si}{=}f_\mathrm{Si}Q$,
$Q_\mathrm{gr}{=}(1{-}f_\mathrm{Si})Q$), host 내부 전이 배분 $\{Q_j^{\mathrm{host}}\}$ 은 각 host 케이스
리스트가 정한다. dQ/dV 는 두 host 평형 종의 합~\eqref{eq:blend-dqdv} 을 \emph{같은} $V_\app$ 배열
위에서 평가해 얻는다 --- 공통 $V_n$ 이란 두 host 가 하나의 전위 축을 공유한다는 뜻이고, 이는 두 host 가
$\mu$ 하나를 공유한다는 물리(\S\ref{ssec:si-blend-derive})의 코드 표현이다. 배경 미분용량 \code{Cbg} 는
전극 단위로 한 번만 더한다(host 별 중복 가산 금지).
```

제안(완성 LaTeX — 셋째 문장부터 치환):
```latex
dQ/dV 는 두 host 평형 종의 합~\eqref{eq:blend-dqdv} 을 \emph{같은} $V_\app$ 배열
위에서 평가해 얻는다 --- 평형 합성이므로 $|I|\to0$ 에서 $V_n=V_\app$(식~\eqref{eq:vn})라 두 이름은 같은
축이고, 유한 율속 진입점(\code{dqdv}$\cdot$\code{curve})을 태울 때의 분극 환산
$V_n=V_\app-\sigma_d|I|R_n$ 은 \emph{전극 단위 1회}다: $\sigma_d\cdot|I|\cdot T\cdot R_n$ 는 두 host
인스턴스가 같은 값을 공유하는 전극 공통 입력이며(한 집전체$\cdot$한 전류), host 별로 다른 $R_n$ 을 주어
전위 축을 둘로 가르는 구현은 계약 위반이다. 공통 $V_n$ 이란 두 host 가 하나의 전위 축을 공유한다는
뜻이고, 이는 두 host 가 $\mu$ 하나를 공유한다는 물리(\S\ref{ssec:si-blend-derive})의 코드 표현이다.
배경 미분용량 \code{Cbg} 는 전극 단위로 한 번만 더한다(host 별 중복 가산 금지 --- 배치 규칙은
\S\ref{ssec:code-contract} 의 실현 조건 (ii)).
```

근거: (i) P3-1(전위 위계): Ch1 규범은 "평형 열역학이 사는 전위는 $V_n$"(ch1_sec01:164·202–203)이고 eq:blend-dqdv 의 평가점은 $U_\mathrm{oc}$ — 현행 문장은 "$V_\app$ 배열 위에서 평가" 와 "공통 $V_n$" 을 다리 없이 병치한다. 평형 합성 범위에서는 $|I|\to0\Rightarrow V_n=V_\app$(ch1_sec01:187 "두 전위가 일치")로 무모순이므로 그 등식 한 줄이면 위계가 닫힌다. (ii) 유한 율속 재량 공백: 표준 진입점 시그니처(`dqdv(V_app, T, I_abs, Q_cell, s)`·`curve(..., c_rate, ...)`)는 host 인스턴스마다 다른 $R_n$(생성자 인자)·$|I|$·$T$ 주입을 허용한다 — 같은 전극의 두 활물질이 다른 축을 갖는 비물리 구성인데, 명세는 Cbg 만 전극 단위로 규정하고 이 넷은 무규정. G1(f_Si=0 만)·G2(연속성)·G3(용량 보존은 중심 이동에 불변) 어느 게이트도 이 오류를 잡지 못하므로 명세 문장이 유일한 방어선.

### A23-M8 — G2 "연속" 이 판정 절차 없는 게이트 + f_Si→0⁺ 끝점 수렴 누락
- 파일:행 = `ch3v22_sec05_code.tex:43–45` · 유형 = 보완 · 등급 = **M**

현행(축자):
```latex
$\cdot$ \textbf{G2 스윕 연속성}: $f_\mathrm{Si}\in(0,0.3]$ 에서 곡선이 $f_\mathrm{Si}$ 에 연속(불연속 점프 없음)
--- 대조 데이터는 f$_\mathrm{Si}$ 스윕 실측(\S\ref{ssec:si-blend-gs2}: gautam/moyassari/chatzogiannakis, tier-A).
```

제안(완성 LaTeX — 판정문 치환; 대조 데이터 괄호는 A23-H1 제안 적용 전제):
```latex
$\cdot$ \textbf{G2 스윕 연속성}: $f_\mathrm{Si}\in[0,0.3]$ 스윕에서 곡선이 $f_\mathrm{Si}$ 에 연속 ---
판정 가능한 형태로: 스윕 격자 $\Delta f_\mathrm{Si}$ 의 인접 곡선 차가
$\max_V|\Delta(\dd Q/\dd V)|\le C\,\Delta f_\mathrm{Si}$ 로 유계(상수 $C$ 는 R6 이 격자 반분 수렴으로
고정)이고, 특히 $f_\mathrm{Si}\to0^{+}$ 끝점이 G1 의 흑연 단독 곡선으로 수렴한다
(식~\eqref{eq:blend-limit} 의 코드짝). 실측 스윕 개형과의 대조는 연속성 게이트와 별개 검증 항목으로
분리한다
```

근거: (i) gate 설계 원칙(확인 가능한 조건 의무): "연속(불연속 점프 없음)" 은 유한 스윕에서 판정 절차가 정의되지 않음 — 어떤 격자·어떤 노름·어떤 문턱인지 없이는 PASS/FAIL 을 기계 판정할 수 없다. 합성식이 $f_\mathrm{Si}$ 에 선형(용량 가중)이므로 Lipschitz 유계 검사가 자연스럽고 저비용. (ii) 끝점 수렴: §3.3 검산 (ii)는 eq:blend-limit 를 "§3.5 코드의 `f_Si=0 → bit-exact` 게이트의 \emph{이론적 짝}" 으로 명시(자산 [V22-R5-14 "R6 게이트 이론짝"])하는데, 게이트 사슬에서 G1 은 $f_\mathrm{Si}=0$ 한 점, G2 는 개구간 $(0,0.3]$ 내부만 검사해 **극한 접속 자체는 어느 게이트도 검사하지 않는다** — 이월된 이론 검산의 코드 대응이 비어 있다. (iii) 실측 대조 분리: 연속성은 순수 수치 성질이고 실측 스윕과의 개형 비교는 모델 검증 — 한 불릿에 섞이면 G2 의 exit 판정이 모호해진다.

### A23-M9 — si_case 리스트 "값은 표 tab:si-cases 의 시연값" 이 축자로는 구성 불능
- 파일:행 = `ch3v22_sec05_code.tex:32–36` · 유형 = 보완 · 등급 = **M**

현행(축자):
```latex
\code{si\_case} 는 세 서브케이스를 고른다 --- \code{'elemental'}$\cdot$\code{'siox'}$\cdot$\code{'sic'}.
각 케이스는 흑연 \code{GRAPHITE\_STAGING\_LIT} 에 대응하는 Si 전이 초기값 리스트(제안 명:
\code{SI\_ELEMENTAL\_LIT}$\cdot$\code{SIOX\_LIT}$\cdot$\code{SIC\_LIT})를 갖고, 값은 표~\ref{tab:si-cases}
의 tier 명기 시연값이다(신뢰값 아님 --- round-trip 피팅 override 전제).
```

제안(완성 LaTeX — 마지막 절 치환):
```latex
값은 표~\ref{tab:si-cases}
의 tier 명기 시연값을 \emph{집계 제약}으로 삼아 구성한다(신뢰값 아님 --- round-trip 피팅 override
전제): 표가 주는 것은 케이스 수준 집계(용량$\cdot$평균 전위$\cdot\eta_\mathrm{ICE}\cdot$히스 규모)이므로,
전이별 $\{U_j,w_j,Q_j\}$ 리스트는 R6 이 \S\ref{sec:si-cases} 의 개형 사실로 배치한다 --- 성분 중심들이
표의 평균 전위 구간을 덮고, $\sum_jQ_j^\mathrm{Si}=Q_\mathrm{Si}$ 로 정규화되며, 경사 성분은
$n_j\!\gg\!1$ 의 넓은 폭(N4 재해석), 좁은 이산 peak 는 \code{'elemental'} 의 Li$_{15}$Si$_4$ 자리에만
둔다. 각 성분의 tier 는 표 각주를 계승해 코드 주석으로 남긴다.
```

근거(코드·표 대조): (i) `GRAPHITE_STAGING_LIT`(v1.0.21:942–971)는 **전이별** dict 리스트(`U`·`w`·`Q`·`Omega`·열역학·동역학 키) — "대응하는" Si 리스트도 같은 스키마를 요구한다. (ii) 그러나 표~tab:si-cases 의 열은 케이스 수준 집계(가역 용량·평균 전위·$\eta_\mathrm{ICE}$·히스 규모·앵커)뿐 — 전이별 $\{U_j,w_j,Q_j\}$ 가 표에 존재하지 않아 "값은 표의 시연값이다" 를 축자로 이행할 수 없다. (iii) 명세가 구성 규칙(집계 제약 + §3.2 개형 사실)을 명시하지 않으면 R6 이 임의 재량으로 전이값을 지어내게 되어, §3.5 도입의 "조용히 날조하지 않는다" 와 긴장. 제안은 표의 지위(시연값·override 전제)를 그대로 두고 다리만 놓는다.

### A23-M10 — 공백의 코드 계승 기본값 정책 미명세(Λ_σ 수치·SiOx placeholder 우선순위)
- 파일:행 = `ch3v22_sec05_code.tex:37–38·51–54` · 유형 = 보완 · 등급 = **M**

현행(축자):
```latex
SiO$_x$ 의 두 공백(평균 전위$\cdot$절대 히스, \S\ref{ssec:si-siox})은 코드에서도 tier-C placeholder
또는 명시적 \code{None}(공백)으로 계승하고, 임의값으로 메우지 않는다.
```
```latex
(i) \textbf{GS-1(기계
히스)}: \code{BlendedAnodeDQDV} 는 Si 히스테리시스를 1차원리로 합성하지 않는다. 응력 결합 항
\eqref{eq:si-vshift} 은 선택적 $\Lambda_\sigma\!\cdot\!\sigma_\mathrm{h}$ 오프셋 훅으로만 노출하고(경로 의존 $\sigma_h$
는 사용자 입력), 소성 폐합은 구현하지 않는다(\S\ref{ssec:si-lc-gap} 범위 선언).
```

제안(완성 LaTeX — 각각 치환):
```latex
SiO$_x$ 의 두 공백(평균 전위$\cdot$절대 히스, \S\ref{ssec:si-siox})은 코드에서도 명시적
\code{None}(공백) 계승을 기본으로 하고, 시연 목적의 tier-C placeholder 를 쓸 때는 출처$\cdot$tier 주석을
값 옆에 의무로 남긴다 --- 어느 쪽이든 임의값으로 메우지 않는다(§3.2 srcbox 의 ``표에 수치로 싣지 않고
명시적 공백'' 정책의 코드판).
```
```latex
(i) \textbf{GS-1(기계
히스)}: \code{BlendedAnodeDQDV} 는 Si 히스테리시스를 1차원리로 합성하지 않는다. 응력 결합 항
\eqref{eq:si-vshift} 은 선택적 $\Lambda_\sigma\!\cdot\!\sigma_\mathrm{h}$ 오프셋 훅으로만 노출하고(경로
의존 $\sigma_\mathrm{h}$ 는 사용자 입력 --- 가지당 스칼라 또는 $V$ 격자 길이 배열; $\Lambda_\sigma$ 의
수치 기본값은 두지 않는다[\code{None} --- \S\ref{ssec:si-lc-derive} 검산 박스의 ``정확값은 확인 필요''
계승]), 소성 폐합은 구현하지 않는다(\S\ref{ssec:si-lc-gap} 범위 선언).
```

근거: (i) §3.4 verifybox 는 $\Lambda_\sigma$ 의 정확값을 명시적 "확인 필요" 로 남겼다 — 코드 훅이 수치 기본값(예: 100 mV/GPa)을 가지면 문서가 거부한 수치 충전을 코드가 수행하게 되어, warnbox 자신의 "코드가 낼 수 있는 것과 못 내는 것의 경계가 문건 공백과 1:1" 원칙을 위반한다. 기본 \code{None}(미지정 시 훅 비활성)이 1:1 을 보존. (ii) $\sigma_\mathrm{h}$ "사용자 입력" 은 형태 무규정 — eq:si-plastic 의 $\sigma_\mathrm{h}(\theta,\text{이력})$ 는 상태 의존이므로 가지당 스칼라(1차 시연)와 격자 배열(이력 프로파일) 중 무엇을 받는지에 따라 훅 설계가 갈린다. (iii) SiOx 쪽 "tier-C placeholder **또는** None" 은 우선순위가 없어, §3.2 srcbox 의 "표에 수치로 싣지 않고 명시적 공백으로 표기" 정책과 코드 기본값이 어긋날 여지 — 기본 None·placeholder 는 provenance 주석 의무로 정렬. (iv) 표기 정합 부수: 현행 51–54행의 `$\sigma_h$` 는 §3.4 본문 표기 `$\sigma_\mathrm{h}$` 와 첨자체가 다름(제안문에서 함께 정렬 — L6 참조).
<!-- M -->

---

## 3. L 등급 (문체)

### A23-L1 — "상수 덩이" 는 여기선 상수가 아님
- 파일:행 = `ch3v22_sec04_mech.tex:38–40` · 유형 = 설명 · 등급 = **L**

현행(축자):
```latex
이고, 무응력 극한($\sigma_\mathrm{h}{=}0$)의 평형 전위를
$-FV_\eq^{0}\equiv\mu_\mathrm{Li}^{0}(\theta_\eq)-\mu_\mathrm{Li}^\mathrm{metal}$ 로 정의해 빼면 상수
덩이가 상쇄된다.
```

제안(완성 LaTeX):
```latex
이고, 무응력 극한($\sigma_\mathrm{h}{=}0$)의 평형 전위를
$-FV_\eq^{0}\equiv\mu_\mathrm{Li}^{0}(\theta_\eq)-\mu_\mathrm{Li}^\mathrm{metal}$ 로 정의해 빼면 무응력
몫이 상쇄된다.
```

근거: 상쇄되는 덩이 $\mu^{0}(\theta_\eq)-\mu^\mathrm{metal}$ 는 $\theta$ 의존 — 식 (c) 자신이 $V_\eq^{0}(\theta)$ 로 적는다. Ch1 Part 0 (c) 의 "상수 덩이를 $U$ 로 묶기"(ch1_sec02b:173)는 진짜 상수($\mu^\mathrm{metal}$)가 대상이라 정확 — 같은 관용구가 여기선 대상이 달라 오전이. 대수 자체는 무결(재유도 §5-축1).

### A23-L2 — σ_h 도입부에 σ_d 와의 구분 한 구절
- 파일:행 = `ch3v22_sec04_mech.tex:27–28` · 유형 = 설명 · 등급 = **L**

현행(축자):
```latex
--- 새 기호 셋($\sigma_\mathrm{h}$ 평균 응력$\cdot$$\bar v_\mathrm{Li}$ 부분몰 부피$\cdot$뒤의 $\Lambda_\sigma$
결합 계수)은 본 절 도입이며 골격의 $\Omega_j$(정규용액 상호작용 [J/mol])와 무관하다.
```

제안(완성 LaTeX):
```latex
--- 새 기호 셋($\sigma_\mathrm{h}$ 평균 응력$\cdot$$\bar v_\mathrm{Li}$ 부분몰 부피$\cdot$뒤의 $\Lambda_\sigma$
결합 계수)은 본 절 도입이며 골격의 $\Omega_j$(정규용액 상호작용 [J/mol])와 무관하다($\sigma_\mathrm{h}$
의 첨자는 hydrostatic --- 방향 부호 $\sigma_d$ 와도 별개 기호).
```

근거: 같은 절 (d) 한 문장 안에 $\sigma_d$ 와 $\sigma_\mathrm{h}$ 가 병존("충전 라벨, $\sigma_d{=}-1$)는 압축($\sigma_\mathrm{h}<0$)") — 같은 σ 몸통·첨자 한 글자 차이라 속독 독자의 혼동 지점. 기호표(tab:si-notation)는 구분해 싣지만 본문 도입부에서 한 구절이면 자족.

### A23-L3 — (d) 부호 읽기의 산문 사슬 수식화(선택)
- 파일:행 = `ch3v22_sec04_mech.tex:56–60` · 유형 = 수식화 · 등급 = **L**

현행(축자): (A23-M5 의 현행과 동일 — 56–59행)

제안(완성 LaTeX — M5 인용 부착과 독립·병행 가능한 압축 대안):
```latex
부호 사슬로 요약하면 $\sigma_d{=}-1$(리튬화)$\;\Rightarrow\;\sigma_\mathrm{h}<0\Rightarrow
\Lambda_\sigma\sigma_\mathrm{h}<0$(아래로), $\sigma_d{=}+1$(탈리튬화)$\;\Rightarrow\;\sigma_\mathrm{h}>0
\Rightarrow\Lambda_\sigma\sigma_\mathrm{h}>0$(위로) $\;\Rightarrow\;V^{\dis}>V^{\chg}$ --- 흑연 분기
식~\eqref{eq:Ubranch} 의 부호($U_j^{\dis}>U_j^{\chg}$)와 \emph{같은} 방향이다(기원은 다르나 부호 규약은 일관).
```

근거: 4관점-④(산문→수식): 두 가지·세 단계의 인과가 산문으로 늘어져 있어 함의 사슬 한 줄이 더 검산 친화적. 현행 유지도 무방(문체 선호) — 채택 시 M5 의 인용 괄호와 결합 가능.

### A23-L4 — 절 번호 하드코딩("§3.1"·"§3.2") ↔ \S\ref 혼용
- 파일:행 = `ch3v22_sec04_mech.tex:8–9·94` (동형: ch3v22_sec03_blend.tex:9 등) · 유형 = 문체 · 등급 = **L**

현행(축자, 8–9행):
```latex
이중웰이 아니라 소성 유동과 응력--전위 결합이다(§3.1 사실 vi) --- 열 쪽 실측도 이를 뒷받침한다(가역열이
발열 3성분 중 최소, §3.2 \cite{arnot_calorimetry2021}).
```

제안(완성 LaTeX):
```latex
이중웰이 아니라 소성 유동과 응력--전위 결합이다(\S\ref{sec:si-map} 사실 vi) --- 열 쪽 실측도 이를 뒷받침한다(가역열이
발열 3성분 중 최소, \S\ref{ssec:si-thermal} \cite{arnot_calorimetry2021}).
```

근거: 지시 내용 자체는 전건 정확(§3.1 사실 vi = 기계 기원 히스·§3.2 열특성 소절의 "가역열 ... 셋 중 가장 작고" — 원문 대조 §5-축2). 그러나 같은 두 절 안에서도 \S\ref 사용처(sec05:60 "\S\ref{sec:si-map}"·sec04 의 ssec 참조들)와 하드코딩이 혼재 — 절 재배열 시 하드코딩만 깨진다. 특히 "§3.2" 는 절 수준 지시라 소절 라벨(ssec:si-thermal)로 좁히면 독자 탐색도 준다. 장 전체 일괄 통일은 마스터 트리아지 몫(P5 — 본 창은 제안만).

### A23-L5 — "doc-leads" 용어 무주해
- 파일:행 = `ch3v22_sec05_code.tex:5` · 유형 = 설명 · 등급 = **L**

현행(축자):
```latex
본 절은 R6 코드가 구현할 블렌드 합성의 doc-leads 요구명세다(구현은 R6 소관).
```

제안(완성 LaTeX):
```latex
본 절은 R6 코드가 구현할 블렌드 합성의 doc-leads(문서 선도 --- 문서가 계약을 확정하고 코드가 따르는)
요구명세다(구현은 R6 소관).
```

근거: 프로젝트 내부 용어의 본문 첫 노출 — 문서만 읽는 독자(코드 계보 무접근)에게 무정의. 한 괄호로 자족.

### A23-L6 — 조판 비일관 묶음(f_Si 분절·G1 표기·σ_h 첨자체)
- 파일:행 = `ch3v22_sec05_code.tex:45·60` (+ ch3v22_notation.tex:33) · 유형 = 문체 · 등급 = **L**

현행(축자, 45행):
```latex
--- 대조 데이터는 f$_\mathrm{Si}$ 스윕 실측(\S\ref{ssec:si-blend-gs2}: gautam/moyassari/chatzogiannakis, tier-A).
```
현행(축자, 60–61행):
```latex
이 요구명세로 R6 는 흑연 단독 회귀를 깨지 않으면서($G1$) 블렌드 곡선을 $f_\mathrm{Si}$ 하나로 토글하고
($G2$$\cdot$$G3$), 두 정직 공백을 코드 경계로 보존한다
```

제안: ① `f$_\mathrm{Si}$` → `$f_\mathrm{Si}$`(문자 f 가 수식 밖으로 나가 upright 로 찍히는 분절 — H1/M8 제안문에는 이미 반영). ② 본문 게이트 지칭 `$G1$`(수학 이탤릭) 을 codebox 의 `\textbf{G1}` 과 정합하게 `G1`(로만) 또는 `\textbf{G1}` 로 통일. ③ `$\sigma_h$`(notation:33·sec05:53, italic h) ↔ `$\sigma_\mathrm{h}$`(sec04 전체, upright h) 첨자체 통일 — 기호표가 전건이므로 표 쪽을 본문 표기(\mathrm{h})로 맞추는 방향 제안.

근거: 렌더 결과가 실제로 다른 글리프(수식 분절 f 는 본문체·h 는 이탤릭/업라이트 상이) — 검색·축자 치환(마스터 기계 매칭)에도 걸림. 의미 무영향이라 L.

### A23-L7 — "비열역학" 표현의 정밀화
- 파일:행 = `ch3v22_sec04_mech.tex:92–93` · 유형 = 설명 · 등급 = **L**

현행(축자):
```latex
\emph{열역학 쌍안정}에서 온다. Si 갈림은 소성 \emph{소산}(경로 의존$\cdot$비가역, 비열역학)에서 온다. 두
```

제안(완성 LaTeX):
```latex
\emph{열역학 쌍안정}에서 온다. Si 갈림은 소성 \emph{소산}(경로 의존$\cdot$비가역 --- 평형 열역학 밖)에서 온다. 두
```

근거: 소성 소산은 비평형 열역학(2법칙 소산)의 소관이라 "비열역학" 은 과축약 — 의도는 "평형 자유에너지로 적히지 않는다" 이고, 같은 절 87행("평형 자유에너지 $g(\xi)$ 로 적히는 양이 \emph{아니고}")·GS-2 의 "평형/율속 층 분리" 어휘와 정렬하면 정확해진다.
<!-- L -->

---

## 4. 서치 절 (하이쿠 서브 위임 — doi 실검증분만·기억 서지 배제)
<!-- SEARCH -->

---

## 5. 검증 로그 (축별 — 완료 즉시 append)
<!-- VLOG -->

---

## 6. 무발견 축 (검토했으나 문제 없음)
<!-- NOFIND -->

---

## 7. 말미 4-tier 분류
<!-- TIER -->

---

## 8. 부수 관찰 (대상 밖 — 마스터 참고용, 제안 아님)
<!-- MISC -->
