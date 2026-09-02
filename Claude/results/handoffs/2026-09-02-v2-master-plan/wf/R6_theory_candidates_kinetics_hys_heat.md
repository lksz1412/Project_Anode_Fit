# R6 — 동역학·전기화학·히스테리시스·비가역 발열 진보 후보 카탈로그

> 작성 = 판독·등록부 초안 에이전트 [theory_kinetics], 2026-09-03. 수신 = master(v2.0.0 마스터 플랜 통합 초안). 위치 = 마스터 플랜 골격의 작업 챕터 3.1(후보 이론 조사·평가)·3.2(일반→특수 사다리)의 **시드 문건**이며, 결정을 확정하지 않는다.
> 원천 = brief §3 배정분 가운데 동역학·히스·열 축 문건 19본(말미 「Read Coverage」에 파일·행 범위 전건). 경로는 전부 `D:\Projects\Project_Anode_Fit\Claude\` 기준.
> 표기 규약 = 4-tier: **[확정]**(path:line 근거) / **[근거 미발견]** / **[추정]**(본 에이전트 판단) / **[미검증]**(원문 미대조·서지 미등재). "사용자 결정"이라 적은 항목은 brief §2 verbatim 또는 원천에 사용자 결정으로 기록된 것뿐이다.

---

## 0. 요지

현행 v1.0.25.1 문건은 동역학·히스테리시스·열의 세 축에서 **결과식·닫힌형·검산을 거의 전부 자력 보유**하고 있다 — Eyring/TST 속도식과 그 분배함수 기원, detailed balance 에서 유도된 logistic, 1계 완화 ODE 와 인과 기억 적분·평형 극한·방향 반전, 컷 동결 지연 길이, 참 비선형 Volterra 자기일관과 1차 ratio 닫힘·타당성 부등식·전달함수, 정규용액 이중웰의 spinodal gap 닫힌형과 임계 소멸, LCO 대입형, Larché–Cahn 가역 결합, Bernardi 수지의 가역 항, 상분리 열역학 자족 부록(binodal·spinodal·Maxwell·CNT·Cahn–Hilliard). 기존 고등수학 서베이 4창(SURV1~4)은 이 성숙도를 "A 등급 후보가 거의 없다"는 정직한 감가 경고로 이미 기록했고, 본 카탈로그는 그 기각군을 그대로 승계한다.

그럼에도 사용자 기준 ⑤("최대한 일반화된 식을 유도하고 거기서 필요한 방향으로 간소화")와 CLAUDE.md P1 원구상(Chapter 2 발열·3 반응속도론·4 통합 상태방정식·5 히스테리시스) 대비로 보면 **세 종류의 공백**이 남아 있다. 첫째, **배열 공백** — Eyring 척추(사용자 6-11 지시, FABLE 감사 §4 "미계승")가 내용으로는 존재하되 §5 배경 박스와 N7 내부에 흩어져 있어, 일반 rate 식이 평형·지연·온도 의존을 낳는 **순서**로 문건이 조직돼 있지 않다. 둘째, **사다리 최상단 공백** — 비평형 열역학의 일반 상태식(entropy production σ=ΣJX≥0·affinity·flux–force)이 문건에 없어(grep 0건), Bernardi 비가역 항 I(U_oc−V)·히스 소산·동역학 지연 소산이 **한 뿌리에서 갈라져 나오는 유도**가 부재하다. 셋째, **비가역 발열 공백** — 원구상 Chapter 2 의 절반(가역 발열)만 Part T 로 실현됐고, 비가역 항은 "유지"라는 한 줄과 "범위 밖" warnbox 로만 존재한다.

본 카탈로그의 판정 요지는 다음과 같다. **A 등급(사다리 필수·P3 게이트 직결·모델 차원 0)** = K-1 Eyring 척추 재배열 · T-1 entropy production 일반 상태식 · S-1/S-2 자기일관 부록 E 승계와 refs 6/7 5항 완결 · S-5 순환 의존 dependency graph · H-2 정규용액→로지스틱 사다리 rung · Q-1 비가역 발열 분해. **B 등급(조건부 — 데이터 판정·범위 결정·서지 등재·모델 차원 +1↑)** = E-1 조성 의존 교환전류 · E-4 농도 분극 · T-2 선형 flux–force 회수창 · R-1 master equation→OU/Kramers · R-2 KWW/장벽분포 · R-3 Watson 전개 · R-4 확산 제한 커널 · H-1 CNT/Cahn–Hilliard γ_j 유도 · H-5 Si 분리 branch · Q-2 히스 소산 정식화. **C 등급(명명·각주·가정 등록)** = K-2 투과계수 · E-2 Marcus · S-3 Kubo 정적 극한 · S-4 Neumann 오차 · H-3 Preisach 노트 · H-4 cusp 지수 · Q-3 Bernardi 소거 항 부활 조건. **D(기각 승계)** = Wiener–Hopf · WKB · 다중척도 · 중심다양체 · Langevin · Preisach 연산자 · 동적 Kubo 승격 · 경로의존 소산 정량 · 소성 구성식 · Bazant/Dreyer PDE 생성기 · 비등온 T(V) 되먹임.

사다리 "일반 비평형 열역학 상태식 → 준평형 → 평형(정칙용액→로지스틱) · 동역학 일반(TST) → lag → 동결"은 **실현 가능하다**고 판정한다(§5). 여섯 rung 가운데 넷(평형·TST·lag·동결)은 현행 자산의 재배열로 닫히고, 둘(일반 상태식·준평형)은 모델 차원 0 의 신규 유도 절 1~2개로 닫힌다. 단 두 가지 정직 조건이 붙는다 — (i) 문건 동역학은 컷 affinity 𝒜=4RT 로 Onsager 선형 영역 밖이므로 선형 flux–force 는 "소개하되 회수하지 않는" 노드로 표기해야 하고, (ii) 평형 rung 의 두-상 커널(정규용액+Maxwell delta vs 로지스틱)은 v1.0.26 미완 데이터 판정에 종속된다.

---

## 1. 판정 규약

각 후보는 다음 일곱 열로 적는다.

- **무엇** — 후보 이론·기법의 내용.
- **현행 보유 상태** — v1.0.25.1 에서 무엇이 어디까지 있는가(파일:행). 없으면 [확정] grep 0건 또는 [근거 미발견].
- **사다리 위치** — "일반식 → 가정 → 회수 식": 어느 일반식에서 출발해 어떤 가정을 걸면 현행 boxed 식이 회수되는가.
- **새 유도 단계** — v2.0.0 이 새로 써야 하는 (a)출발→(b)연산→(c)중간→(d)박스 사슬의 단계 목록.
- **레퍼런스** — 문건 서지 원장(`_sections/ch1v22_bib.tex`·`ch2v22_bib.tex`·`ch3v22_bib.tex`, 부록 [A1]~[A5])에 **이미 등재된 키만 확실**로 적고, 그 밖은 [미검증](등재 필요·DR-6 종속)으로 표기한다. 기억에 의존한 DOI 는 적지 않는다.
- **모델 차원·침습도** — 모델 차원 = 새 피팅 파라미터 수. 침습도 = 낮(박스·각주 1개) / 중(절 1개 신설 또는 절 내 재구성) / 높(다절 재배열·N-노드 변경·커널 변경·부록→본문 승격).
- **등급** — **A** = 사다리 필수 노드 또는 P3 게이트 직결·회수 조건 명확·모델 차원 0·서지 확실(3.2 설계에 채택 권고) / **B** = 진보 가치 있으나 조건부(데이터 판정·범위 결정 해제·서지 신규 등재·모델 차원 +1↑; 3.7 DG-B 결정 대상) / **C** = 명명·각주·가정 등록 수준(모델 차원 0·분량 ≤ 박스 1) / **D** = 기각(기존 서베이 기각군 승계 또는 스코프 벽).

등급은 본 에이전트의 판단[추정]이며, 기존 서베이가 준 등급을 승계할 때는 그 출처를 병기한다.

---

## 2. CLAUDE.md P1 원구상(Chapter 1~5) ↔ 현행 재료별 3장 ↔ brief 작업 챕터 4 대응

P3 #7 이 요구하는 명칭 분리를 먼저 고정한다. 이 문건에는 **네 개의 "Chapter" 이름공간**이 공존한다 — (i) 역사적 `ver.1~ver.5`(`graphite_ica_dynamic_ver5.tex` 적층), (ii) CLAUDE.md P1 **원구상 Chapter 1~5**(전하 보존·발열·반응속도론·통합 상태방정식·히스테리시스), (iii) 현행 v1.0.25.1 **재료별 Chapter 1~3**(흑연·LCO·Si), (iv) brief §5 **작업 챕터 1~6**(이력·진단·설계·저작·서지·검수). brief 는 3축을 말하지만 P1 원구상까지 세면 넷이다 — 통합 초안의 Phase Range 표 상단 주석에 이 넷을 모두 적을 것을 제안한다(Decision Queue DQ-11).

| P1 원구상 | 원구상 내용(`CLAUDE.md` §P1 — 본 에이전트는 시스템 주입본으로 읽어 행 번호 미기재) | 현행 v1.0.25.1 실물 위치 [확정] | 보유 판정 | brief 작업 챕터 4 대응(§5 골격) |
|---|---|---|---|---|
| Chapter 1 전하 보존식 기반 내부 전위 결정 | 전하 보존식이 내부 전위를 정하는 중심식; self-consistent 되먹임은 refs 6/7 방법론 확인 뒤 반영 | Part 0 §2b 대정준 전하보존 반전 `eq:sm-mc-balance`(`_sections/ch1_sec02b_part0.tex:348`)·요동 양성 유일근 `eq:sm-mc-fluc`(:365) · N1 분극 `eq:vn`(`ch1_sec01_n0n1.tex:183`) · N9 합산 `eq:sum`(`ch1_sec10_sum.tex:12`) · 블렌드 이중합 반전 `eq:blend-balance`(`ch3v22_sec03_blend.tex:74`) · 부록 E 적용 범위 warnbox가 이 반전을 "적분핵 없는 대수 근찾기"로 분류(`ch1_appE_selfconsistent.tex:19-27`) · refs 6/7 5항 `sec:sc-p35`(:113-135) | **보유·분산** — 중심식은 있으나 원구상이 요구한 "내부 전위 결정 흐름"으로 한 절에 모이지 않음. 5항 중 ②(위치)가 "원문 대조로 확정" 미완(:120-121) | 4.1 기초 + 4.2 평형(반전) + 4.9 부록(자기일관) |
| Chapter 2 발열 | 열역학적 발열 계층 | Part T 전체 = `ch2_sec00~10`: 분배함수→config/vib/전자 분포→가역 발열 `eq:qrev`(`ch2_sec07_revheat.tex:15-20`) — 가역 항만 전개, 비가역 항 I(U_oc−V)는 "유지"(:36)·히스 소산은 범위 밖 warnbox(`ch2_sec05_mixing.tex:230-238`) | **절반** — 가역 발열 완성, 비가역 발열 미전개 | 4.4 열특성(엔트로피 분해·가역 발열·entropy production) |
| Chapter 3 반응속도론 | 동역학 계층 | §5.1 Eyring→BV→detailed balance→logistic(`ch1_sec05_width.tex:11-44`) · TST 분배함수 bgbox `eq:tst-box`(:46-121) · Bazant 대응 srcbox(:123-153) · N7 `eq:Lq`·`eq:kuniv`·`eq:Lqfull`·`eq:LV`(`ch1_sec08_lag.tex:14-127`) · N8 `eq:memory`·`eq:lag`·`eq:tail-limit`·`eq:reversal`(`ch1_sec09_tail.tex:14-188`) · 부록 E 자기일관(전문) | **보유·분산** — 내용 100%, 척추 아님(FABLE §4:47 "미계승") | 4.3 동역학(TST/Eyring·BV·lag·tail·Fredholm ratio·전달함수) |
| Chapter 4 통합 상태방정식 | 통합 상태방정식 계층 | 명시적 "상태방정식" 절 [근거 미발견](본 에이전트 grep 미실시 — 미검증). 실질 대응 = N9 합산 `eq:sum` + Part T 계산용 종합식(`ch2_sec08_synthesis.tex:13-22`) + Part 0 사다리 "분배함수→…→Nernst"(`ch1_sec02a_part0.tex:14`) | **부분** — 곡선(∂_V)과 열(∂_T)이 "한 자유에너지의 두 응답"으로 묶임(`ch2_sec07_revheat.tex:74-94`)은 통합 상태식의 씨앗 | 3.2 사다리 자체 + 4.1/4.2 |
| Chapter 5 히스테리시스 | 히스테리시스 계층 | N3 §4 spinodal gap `eq:dUhys`(`ch1_sec04_hys.tex:101-106`)·분기 중심 `eq:Ubranch`(:240)·γ_j/h_η 현상학(:246-252)·CNT 근거(:254-266) · LCO 대입형 `eq:lco-dUhys`(`ch1_sec13_lcohys.tex:80-90`) · Si Larché–Cahn `eq:si-coupling`(`ch3v22_sec04_mech.tex:50-55`)·GS-1 공백(:71-105) · 상분리 부록(`appendix_phase_separation.tex` 전문, 독립 컴파일 :13, 본문 편입 미결 :7) · Dreyer 다입자 plateau(`ch1_sec07_broadening.tex:68-92`, grep) | **보유·재료별 분산** — 열역학 분기(흑연·LCO)와 소산 분기(Si)가 다른 장에 있음 | 4.5 히스테리시스(일반) + 4.6~4.8 재료 적용 |

이 표의 결론은 원구상 Chapter 2~5 의 **내용**은 현행에 대부분 있으나, **계층 순서**(일반 → 재료)로 배열돼 있지 않다는 것이다 — 곧 brief 3.3 (b)안(Part I 일반 이론 + Part II 재료 적용)은 원구상 Chapter 2~5 를 Part I 의 네 장으로 되살리는 것과 같다[추정].

---

## 3. 현행 동역학·히스·열 척추의 실물 지도

카탈로그의 "현행 보유 상태" 열이 참조하는 사슬을 한 번에 적는다(전부 [확정]).

**동역학 사슬.** 서론이 "세 인자(T·전위·C-rate)는 모두 하나의 속도식 k≃k₀exp[−ΔG_a/RT] 의 서로 다른 자리로 들어온다 … 본 장의 유도는 줄곧 이 한 식의 가지를 펼치는 일"(`ch1_sec00_intro.tex:37-40`)이라고 선언하지만, 실제 조직 원리(spine 그림 :42-88)는 코드 노드 N0→N9 다. Eyring 식은 §5.1 (a)에서 처음 등장해(`ch1_sec05_width.tex:13-21` `eq:bv`) 비를 취해 detailed balance(`eq:db` :24-28), 운동방정식 dξ/dt=r⁺(1−ξ)−r⁻ξ=k_j(ξ_eq−ξ)(:30), 정지점 logit→logistic(`eq:logisticsolve` :33-38)으로 닫히고, 배경 박스가 k₀=k_BT/h 의 미시 기원(`eq:tst-qrc`·`eq:tst-freq`·`eq:tst-rate`·`eq:tst-dG`·`eq:tst-box` :57-96)과 두 전제(안장점 준평형·재교차 무시 κ=1, "변분 TST·터널링 보정은 범위 밖" :52-55)를 세운다. Bazant 2013 대응 srcbox 는 교환전류의 조성 의존을 "조성무관 상수 k₀e^{−ΔG_a/RT} 로 흡수(이상 교환속도)"한 가정 차를 명시한다(:149-152). N7 은 완화율 k_j=r⁺+r⁻(`eq:kuniv` `ch1_sec08_lag.tex:27-31`), 컷 affinity 𝒜=min(z_cut n_j RT, A_cap RT)(`eq:Acut` :43-47, 기본 상태 실효 z=4.0 :48-50), 방향별 χ_d 와 유효 장벽 ΔH_a^eff=ΔH_a−χ_dΩ(`eq:chid`·`eq:dHeff` :59-75), L_q 완전형(`eq:Lqfull` :114-119), 전압축 환산(`eq:LV` :124-127), "실현 미분 ∂lnL_q/∂V=0"의 동결(:128-133)을 닫는다. N8 은 적분인자→기억 합성곱(`eq:memory` `ch1_sec09_tail.tex:21-25`)→자연 경계(`eq:memory-Vaxis` :36-39)→지연 진행률 박스(`eq:lag` :58-61)→peak shape(`eq:peakshape` :109-112)→지배수렴 평형 극한(`eq:tail-limit` :143-148)→충전 반전(`eq:reversal` :178-188)이다. 부록 E 는 동결 0차(`eq:sc-frozen`·`eq:sc-ref` `ch1_appE_selfconsistent.tex:32-42`)를 "가해 기준"으로 놓고 상호작용 몫을 복원한 참 문제 κ(ξ)=κ₀exp[−2χ_d(Ω/RT)(1−ξ)](`eq:sc-true` :51-55)·Volterra 정확해(`eq:sc-volterra-eq` :62-65)·1차 ratio 닫힘(`eq:sc-ratio` :86-90, 국소형 :92-95)·동결극한 정확 회수 derivbox(:104-111)·refs 6/7 5항(:113-135)·타당성 ε=2χ_d(Ω/RT)Δξ_supp≪1(`eq:sc-valid` :149-153, Picard 수축률 정합 :154-156, 열화 조건 ε≳0.5 warnbox :171-178)·전달함수 H(ω)=1/(1+iωL_V)(`eq:sc-transfer` :183-188)를 닫는다. 부록 E 서두 warnbox 는 전하보존 U_oc 반전과 배경 자기일관을 "적분핵이 없는 대수 근찾기 … 이 기법의 대상이 아니다"로 명시 배제한다(:19-27).

**히스테리시스 사슬.** Part 0 정규용액 `eq:mu`·`eq:gxi`·문턱 `eq:sm-thresh`(`ch1_sec02b_part0.tex:42·51·63`) → §4 2계 미분 `eq:gpp`(`ch1_sec04_hys.tex:27-30`) → spinodal 근 `eq:spinodal`(:33-37) → 비단조 `eq:Veq`(:74-77) → gap 닫힌형 `eq:dUhys`(:101-106) 와 임계 소멸 (8RT/3F)u³·Taylor 함정(:107-120) → 대칭 `eq:hyssym`(:233-236) → `eq:Ubranch`(:239-242) → γ_j·h_η 의 지위("현상학 인자 … 값은 피팅이 정하며 spinodal gap 은 상한" :246-252) → CNT 근거("γ_j 의 근거이지 예측식이 아니다" :254-266). LCO 는 같은 틀의 대입형(`ch1_sec13_lcohys.tex:80-96`, γ_j·h_η "여기서도 유도되지 않는" :98-101, MIT config/전자 슬롯 분리 `eq:lco-mit` :195-201, 도핑 극한 `eq:lco-dope` :208-213). Si 는 Larché–Cahn 응력항 `eq:si-lcmu`(`ch3v22_sec04_mech.tex:22-26`)→`eq:si-coupling`(:50-55)까지 닫고 소성 구성식을 GS-1 공백(물리 가정 충돌 + 유도 미완결 범위 선언 :89-99)으로 선언한다. 상분리 부록은 격자 모형 `eq:app-fxi`(`appendix_phase_separation.tex:106-109`)·현/볼록성 `eq:app-convex`·`eq:app-gain`(:145-162)·공통접선 `eq:app-ct`·binodal `eq:app-binodal`(:185-218)·spinodal `eq:app-spinodal`(:246-251)·Maxwell 등면적 `eq:app-maxwell`(:372-375, 삽입 전극 의미 keybox :386-391)·CNT `eq:app-cnt`·`eq:app-rstar`(:411-422)·Cahn–Hilliard `eq:app-ch-F`·`eq:app-ch-R`(:434-449)·본문 연결(:469-481)을 자족적으로 유도하되, `\documentclass` 독립 문서(:13)이며 "본문(Ch1) 편입 여부는 사용자 검토 후 결정"(:7)으로 남아 있다.

**열 사슬.** Bernardi 수지 축약 `eq:qrev` Q̇=I(U_oc−V)[Q̇_irr≥0]+(−IT∂U_oc/∂T)[Q̇_rev](`ch2_sec07_revheat.tex:15-20`), 두 전제(혼합 엔탈피 항 = 준평형 저율 소거·상변화 항 = U_oc(x) 흡수·고율 잔여 :21-25), 항별 대응표(:31-42; 과전압 소산 "유지"), 부호·라벨 층위(:47-60), 분포 재배열 해석(:62-72), "한 자유에너지의 두 응답" bgbox(:74-94, 가드 "히스 gap 의 비가역 소산은 ∂_T 응답이 아니라 별개" :92-93). 히스 분기 평균 `eq:hys_rev`(`ch2_sec05_mixing.tex:219-223`)와 [C-92] warnbox("히스 gap 자체는 비가역 과정으로 ∝IΔU^hys 의 소산율 … entropy production 열 … 경로의존 측정 불확실도의 정량은 본 장 범위 밖" :230-238). Onsager·flux–force·entropy production 정식화는 본문에 없다 — `_sections` 전건 grep 에서 "온사거"는 부록 E 의 Onsager 척도 r_c 비유(:127·:164)뿐이고 "Marcus·Nernst-Planck·Warburg·KWW·Kohlrausch·Fokker·master equation·Langevin·Kramers·Preisach" 는 0건이다[확정, grep 2026-09-03].

---

## 4. 후보 카탈로그

### 4.1 축 K — 절대 속도론(Eyring/TST) 척추 회복

**K-1 Eyring/TST 일반 rate 식을 동역학 장의 첫 식으로 두는 재배열 — 등급 A.**
무엇: 일반 TST 식 k=(k_BT/h)(q‡/q_R)e^{−ΔE₀/RT}(`eq:tst-rate`)를 Part I 동역학 장의 (a)출발식으로 두고, 그 가지로 (i) 전기화학 구동력 하의 장벽 분할(`eq:bv`), (ii) detailed balance 와 평형 정지점(`eq:db`·`eq:logisticsolve`), (iii) 선형 완화율 k_j(`eq:kuniv`), (iv) 활성화 엔트로피의 분배함수 기원(`eq:tst-box`), (v) 온도·전위·C-rate 세 인자의 자리(서론 :37-40 의 선언), (vi) L_q·L_V·동결을 **순서대로** 배열한다.
현행 보유: 내용 100% [확정 — §3 동역학 사슬]. 배열은 코드 spine N0→N9(`ch1_sec00_intro.tex:42-88`); Eyring 은 §5.1 (a)와 §5 bgbox·N7 내부. FABLE 감사 §4 "★모든 것이 Eyring 식에서 뻗어야(6-11) … 현행 코드 플로우차트 척추, Eyring 은 L_q 절 내부 — 미계승 — v12 척추 결정 필요(F-1)"(`docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md:47`) [확정]. 같은 감사 §5-2 "배열(코드 정합)과 깊이(전 유도)는 독립 축 — 동시 희생 불요(v6 실증)"(:58) [확정].
사다리 위치: 일반식 = TST 속도식(안장점 준평형·κ=1) → 가정 = 단일 반응좌표·조성무관 교환속도·χ 분할 → 회수 식 = `eq:bv`→`eq:db`→`eq:xieq`(평형)·`eq:kuniv`→`eq:Lqfull`(지연).
새 유도 단계: 신규 유도 0. 재배열 + 각 가지의 (a)~(d) 사슬 재점검 + 서론 선언(:37-40)을 장 구조로 승격.
레퍼런스: eyring1935·glasstone1941·laidlerking1983·mcquarrie1976·bazant2013 — 전부 원장 등재 [확정, `ch1v22_bib.tex:8-14`].
모델 차원 0 · 침습도 **높**(Part I 동역학 장 재배열; boxed 식·라벨 불변이면 자산 무유실).
등급 근거: 사용자 방향 지시 미계승 항목의 회복이며 기준 ⑤(일반식→간소화)의 동역학 측 정본. 모델·값 불변이라 위험은 구조뿐. 3.3 (b)안과 정합[추정].

**K-2 투과계수 κ·변분 TST·재교차 보정 — 등급 C.**
무엇: 일반식에 κ 를 명시적으로 두고(k=κ(k_BT/h)…), κ=1·터널링 무시·1D 자유 병진 반응좌표를 **가정 사다리의 등록 항목**으로 적는다.
현행 보유: "투과계수 κ=1 … 변분 TST·터널링 보정은 범위 밖"(`ch1_sec05_width.tex:52-55`) [확정]. SURV2 #4 WKB 는 D("조화=이미 exact·홉핑/CNT=열활성·터널 아님" `docs/v1.0.22/results/comp_v23/SURV2_asymptotic_pert.md:90-100`) [확정].
사다리 위치: 일반식 = κ 포함 TST → 가정 κ=1 → 회수 = 현행 `eq:tst-box`.
새 유도 단계: 없음(가정 등록 1행·각주 1개).
레퍼런스: laidlerking1983 [확정 등재].
모델 차원 0 · 침습도 낮. 등급 근거: 기준 ⑤ 가정 명시 이득만; 실제 보정은 범위 밖 유지(SURV2 D 승계).

### 4.2 축 E — Butler–Volmer·Marcus·농도 분극

**E-1 조성 의존 교환전류(일반화 Butler–Volmer)와 부록 E κ(ξ) 의 통일 — 등급 B.**
무엇: Bazant 2013 의 일반형(교환전류에 농축용액 활동도계수·전이상태 활동도계수 γ‡ 포함, srcbox 대응 "식[29]")에서 출발해, 정규용액 활동도(a_ξ∝ξ e^{Ω(1−ξ)²/RT} 형 — [추정] 형태·부호는 유도 시 확정)로 r^± 의 전치인자 조성 의존을 명시하고, 현행 (i) 조성무관 상수 흡수(`eq:bv`)와 (ii) 부록 E 의 상호작용 몫 κ(ξ)=κ₀exp[−2χ_d(Ω/RT)(1−ξ)](`eq:sc-true`)가 **같은 일반형의 두 절단**임을 보인다.
현행 보유: `eq:bv` 조성무관 상수 [확정 :17-21]; 가정 차 명시 "원 논문의 교환전류 I₀(식[29])는 … 조성 의존이나, 식 eq:bv 는 이를 조성무관 상수로 흡수하고 조성 의존을 전부 구동력 𝒜_j 와 logistic 로만 받는다"(`ch1_sec05_width.tex:149-152`) [확정]; 부록 E 는 affinity 의 상호작용 몫 −Ω_j(1−2ξ_j)를 통해 지연 길이가 점유의 함수임을 이미 복원(`ch1_appE_selfconsistent.tex:46-56`) [확정].
사다리 위치: 일반식 = 활동도 기반 일반 BV(r^±∝a_R^{1−χ}a_O^{χ}/γ‡) → 가정 = γ‡ 상수·전해질 활동도 상수 → 회수 = `eq:bv`; 가정 = 전이상태 activity 만 상수, 격자 활동도는 정규용액 → 회수 = `eq:sc-true` 의 κ(ξ).
새 유도 단계: (a) Bazant 일반형 → (b) 정규용액 활동도 대입 → (c) 지수 정리로 r^+ 에 Ω(1−2ξ) 항 노출 → (d) 두 절단의 박스 + 부록 E 와의 항등 검산. 3~4 식.
레퍼런스: bazant2013·leviaurbach1999·huggins2009 [확정 등재]. Bazant 식 번호 대응은 문건 srcbox 가 이미 적었으나 본 에이전트는 원문 미대조[미검증].
모델 차원 0(γ‡ 를 Ω 로 묶으면) / +1(γ‡ 독립 시) · 침습도 중(§5 srcbox 확장 + 부록 E 참조 1개).
등급 근거: 사다리 "일반 BV → 이상 교환속도" 회수를 명시하는 기준 ⑤ 이득이 뚜렷하고, 부록 E 의 κ(ξ) 를 BV 일반형에서 **유도**하게 되어 자기일관 절의 출발식이 상단 일반식에 접속된다. B 인 이유 = 활동도 형태 선택(정규용액 vs 다른 excess)이 모델 가정이고, LIT G5 "dilute 1′↔4 농도의존 보정 — Mercer 2019 vs Azizi 2025 상충 → 해소 전 하드코딩 X"(`results/comp_v24/LIT_ADVANCE_SYNTHESIS.md:63`)와 인접해 데이터 판정이 필요[추정].

**E-2 Marcus(–Hush–Chidsey) 전하전달 커널 — 등급 C(사다리 상단 일반형으로만).**
무엇: 재조직 에너지 λ 를 가진 Marcus 속도 k(η)∝exp[−(λ±Fη)²/4λRT] (전극 상태밀도 적분형 = Marcus–Hush–Chidsey)를 BV 의 상위 일반형으로 소개하고, |Fη|≪λ 에서 BV 회수·대칭인자 χ=½+Fη/(4λ) 를 보인다.
현행 보유: grep "Marcus" 0건 [확정]. χ 는 상수 입력(기본 ½, `ch1_sec08_lag.tex:86-87`) [확정].
사다리 위치: 일반식 = Marcus/MHC → 가정 = λ≫|𝒜|(컷 affinity 4RT≈0.1 eV 대비 λ 가 충분히 크다 — λ 값은 [미검증]) → 회수 = `eq:bv` 와 상수 χ.
새 유도 단계: (a) Marcus 포물선 자유에너지 → (b) 교차점 장벽 → (c) 소-η 전개 → (d) BV 회수·χ 식. 3 식 + 각주.
레퍼런스: bazant2013 은 제목상 전하전달 일반론이라 Marcus 절을 포함할 가능성이 높으나 본 에이전트 원문 미대조[미검증]; Marcus 원저·Chidsey 는 원장 부재[미검증, 신규 등재 필요].
모델 차원 +1(λ) 도입 시 / 0(회수 조건만 적을 시) · 침습도 낮(박스 1).
등급 근거: 흑연 삽입의 관심 영역(|𝒜|≤A_cap RT=4RT)에서 Marcus 곡률이 실효를 갖는지 근거가 없고(문건 내 λ 없음), brief 3.1 축 목록이 Marcus 를 들고 있으므로 "일반형 소개 + 회수 조건 + 채택 안 함"이 정직한 처리[추정]. DQ-10.

**E-3 농도 분극 층 — Nernst–Planck 확산층·Warburg·Nernst shift(ROADMAP 제안 4) — 등급 B.**
무엇: N1 lumped R_n 을 R_ct(활성화)+농도 과전압으로 가르고, 전해질 확산층 c_s/c_∞=1−|I|/i_L 에서 Nernst shift ΔU=(RT/F)ln(c_s/c_∞) 를 얻어, 고율 dQ/dV 꼬리 비대칭의 동역학(L_V) 몫과 열역학(Nernst) 몫을 분리한다.
현행 보유: N1 `eq:vn` V_n=V_app−σ_d|I|R_n(`ch1_sec01_n0n1.tex:183`) [확정]; GITT srcbox "식 eq:vn 은 … 상수-저항 R_n 모형으로 근사 제거하므로(R_n 의 조성·전류 의존 무시) GITT 만큼 완전하지 않은 연속 근사"(:235-236) [확정]; ROADMAP 제안 4 "현상태 lumped R_n … 개선 방향 BV i₀ 활동도 + Nernst–Planck 확산층 … R_n→R_ct+Warburg … 난이도 중·침습도 높음(N1 신규 layer) · 선행 데이터 EIS·율속 series"(`docs/v1.0.18.2/ROADMAP_future_physics.md:31-35`) [확정]; LIT L6 "R_n(x) SOC 의존 ◐선검증"(:75) [확정].
사다리 위치: 일반식 = Nernst–Planck 플럭스 J=−D∇c−(zF/RT)Dc∇φ + 연속식 → 가정 = 정상 확산층(두께 δ)·전기중성·지지전해질 → 중간 = 한계전류 i_L=FDc_∞/δ 와 농도 과전압 → 가정 = i_L→∞ → 회수 = lumped R_n(`eq:vn`).
새 유도 단계: (a) NP 플럭스 → (b) 정상 확산층 선형 프로파일 → (c) c_s/c_∞ 와 Nernst shift → (d) V_n=V_app−σ_d|I|R_ct−σ_d(RT/F)ln(1−|I|/i_L) 박스 + i_L→∞ 회수. 4~5 식. Warburg 는 주파수영역(EIS) 대응 각주로 한정.
레퍼런스: newman(Electrochemical Systems) [확정 등재, 장 미지정]; ROADMAP [확정]. Warburg 원저 [미검증].
모델 차원 +1(i_L 또는 δ/D) ~ +2(R_ct 분리 시) · 침습도 높(N1 신규 layer).
등급 근거: 기준 ⑤ 일반화(내부 전위 결정 흐름 = P1 Chapter 1 의 정합)에 직결되고 표준 전기화학이라 서지 위험 낮음. B 인 이유 = 데이터 의존(EIS·율속)·모델 차원 증가·Non-goal(회사 데이터 정량) 경계 — 도입 시 warnbox·tier 로 정직 표기 필요. DQ-8.

### 4.3 축 T — 선형 비가역 열역학(Onsager flux–force·affinity·entropy production)

**T-1 일반 비평형 열역학 상태식: 국소 Gibbs 관계 → 엔트로피 수지 → entropy production σ=ΣJ_kX_k≥0 — 등급 A(사다리 최상단).**
무엇: 등온·균일 삽입 전극에 대해 σ = Σ_j J_j𝒜_j/T + I·η_ohm/T (+ 열류·확산 항) 를 세우고, 플럭스(전이별 반응 속도 J_j=Q_j dξ_j/dt·전류 I)와 힘(affinity 𝒜_j·과전압)을 짝지어, Bernardi 의 Q̇_irr=I(U_oc−V)≥0 이 **Tσ 의 적분**임을 유도한다.
현행 보유: 부재 [확정 — §3 grep]. affinity 𝒜_j 는 이미 "구동력"으로 명명·사용(`ch1_sec01_n0n1.tex:75-77` 기호표; `ch1_sec05_width.tex:15`; `ch1_sec08_lag.tex:66`) [확정]. [C-92] 가 "entropy production" 이라는 말을 쓰되 정식화하지 않음(`ch2_sec05_mixing.tex:232-233`) [확정]. Bernardi 첫 항은 "2법칙상 항상 발열"로만 서술(`ch2_sec07_revheat.tex:21-22`) [확정].
사다리 위치: 일반식 = 국소 Gibbs 관계 T ds = du − Σμ_k dn_k 와 엔트로피 수지 ∂s/∂t+∇·J_s=σ → 가정 (i) 등온·균일(열류·농도 구배 항 소거 = Bernardi 두 전제와 동일) → σ_rxn=Σ_jJ_j𝒜_j/T + I²R_n/T → 가정 (ii) 반응 속도의 Marcelin–de Donder 형 J=k⁺(1−e^{−𝒜/RT}) → 회수 = 문건의 r⁺(1−ξ)−r⁻ξ 와 detailed balance(`eq:db`); 적분 → Q̇_irr 회수.
새 유도 단계: (a) 국소 Gibbs 관계 → (b) 엔트로피 수지와 σ 의 이중선형형 → (c) 등온·균일 절단, 반응 항·옴 항 분리 → (d) σ≥0 박스와 Q̇_irr=Tσ 회수. 이어 T-2·Q-1·Q-2 가 이 박스에서 갈라진다. 5~6 식·신규 절 1개.
레퍼런스: bernardi1985·bazant2013(비평형 열역학 기반 전하전달 — 문건 srcbox 가 "Bazant 는 알짜 속도를 전이상태 excess 화학퍼텐셜 기준 반응물·생성물 화학퍼텐셜의 지수차(식[7])로 적고" :147-148 로 이미 인용) [확정 등재]. de Groot–Mazur·Prigogine·Onsager 1931·de Donder 는 원장 부재 — SURV3 서지 메모가 "현 원장에 … 볼록해석 인용 전무 … 코퍼스는 Dreyer·Levi–Aurbach·hill1960·mcquarrie1976 등 통계역학/전기화학 계열만"(`SURV3_convex_inverse.md:116`)이라 적은 사실과 정합[확정]; 신규 등재 필요[미검증]. DQ-5.
모델 차원 0 · 침습도 중(신규 절 1 + Part T 재배열).
등급 근거: 사용자 기준 ⑤ 의 "최대한 일반화된 식"이 이 축에서 가리키는 것은 정확히 이 상태식이고, brief 3.2 사다리의 첫 rung 이며, 원구상 Chapter 2 비가역 발열과 Chapter 4 통합 상태방정식의 공통 뿌리다. 값·모델 불변. 위험 = 서지 신규 등재와 회수창(T-2) 정직 표기.

**T-2 선형 flux–force(Onsager 계수·상반성)와 비선형 반응 속도론의 관계 — 등급 B.**
무엇: 반응 플럭스 J=k⁺(1−e^{−𝒜/RT}) 의 𝒜≪RT 전개 J≈(k⁺/RT)𝒜 로 Onsager 계수 L_rxn=k⁺/RT 를 정의하고, 문건 동역학이 어디서 선형 영역을 벗어나는지를 컷 affinity 로 정량한다.
현행 보유: 부재 [확정]. 컷 affinity 기본 실효 z=4.0(`eq:Acut` `ch1_sec08_lag.tex:44-50`) [확정] — 곧 꼬리는 𝒜≈4RT 에서 평가되어 선형 영역 밖. SURV1 #6 이 같은 범주의 경고("구동 lag L_V∝|I| ≠ 평형 상관시간 … 동적 승격은 물리 가정 충돌" `SURV1_integral_transform.md:142-146`) [확정].
사다리 위치: 일반식 = σ=ΣJX 의 선형 구성관계 J=ΣLX(Onsager) → 가정 = 𝒜≪RT → 회수 = **없음**(문건은 이 회수를 쓰지 않는다 — 비선형 지수형을 그대로 유지). 곧 "소개하되 회수하지 않는 노드".
새 유도 단계: (a) 지수형 플럭스 → (b) 소-𝒜 전개 → (c) L_rxn 정의·상반성 언급 → (d) 문건 작동창(𝒜_cut=4RT·GITT 준평형 𝒜→0)의 두 극단을 한 표로. 2 식 + 표 1.
레퍼런스: bazant2013 [확정 등재]; Onsager 1931 [미검증].
모델 차원 0 · 침습도 낮(T-1 절 안의 소절).
등급 근거: 사다리 완결성(orphan 0)에 필요하나 회수 식이 없어 A 는 아니다. 정직 표기가 없으면 "Onsager 를 넣었다"는 과장이 되므로 warnbox 필수[추정].

### 4.4 축 R — 완화 동역학(master equation/Fokker–Planck·KWW/장벽분포·인과 기억 적분)

**R-1 자리 점유 master equation → 평균 점유의 1계 완화 ODE 회수·Fokker–Planck/OU·Kramers 극한 — 등급 B.**
무엇: 독립 자리 M 개의 점유 master equation 에서 평균 ⟨ξ⟩ 가 정확히 dξ/dt=r⁺(1−ξ)−r⁻ξ 를 따름을 보이고(Ω=0 정확, Ω≠0 평균장 닫힘), 요동은 1/√M 로 소멸(SM2-B)함을, 그리고 같은 Fokker–Planck 의 두 극한이 §8 완화(웰 바닥 OU)와 CNT 핵생성(장벽 탈출 Kramers)임을 잇는다.
현행 보유: 완화 ODE 는 §5.1 (b)에서 "운동 방정식은 정방향이 찬 자리(1−ξ)에서, 역방향이 빈 자리(ξ)에서 출발하므로"로 **서술 도입**(`ch1_sec05_width.tex:28-30`) [확정] — master equation 유도는 없음. 부록 CNT 율 ∝exp(−ΔG*/k_BT) 는 "단언"(`appendix_phase_separation.tex:423-424`) [확정]. SURV4 #4 FPT/Kramers B("부록이 주장한 것을 유도 + 완화↔핵생성 = 한 FP 의 두 극한" `SURV4_bifurcation_stochastic.md:75-81`), #6 Langevin D(#4 로 병합·SM2B 1/√M 벌크 자멸 :90-95), #3 중심다양체 D(:68-73) [확정].
사다리 위치: 일반식 = master equation(이산 점유) → 가정 = 자리 독립·M→∞(평균장·결정론) → 회수 = 완화 ODE(`eq:kuniv` 형) ; 가정 = 연속 극한·고장벽 → Kramers → 회수 = 부록 CNT 율.
새 유도 단계: (a) master equation → (b) 1차 모멘트 방정식 → (c) Ω=0 닫힘·Ω≠0 평균장 절단 → (d) 완화 ODE 박스; 별도로 (a′) FP → (b′) 고장벽 MFPT → (d′) CNT 율 박스. 4~5 식.
레퍼런스: 표준 정리(무인용 관용 — SURV4 :127 규약); 부록 [A3] Porter–Easterling·[A5] Balluffi [확정 등재]; Kramers 1940 [미검증].
모델 차원 0 · 침습도 중(동역학 장 도입 소절 + 부록 각주).
등급 근거: 사다리 "동역학 일반 → 결정론 ODE" 의 가정(자리 독립·M→∞)을 명시하는 기준 ⑤ 이득이 있고, SURV4 가 B 로 승인한 명명·연결을 유도로 격상한다. A 가 아닌 이유 = 값·곡선 불변, 이미 SM2-B 가 요동 소멸을 닫아 신규 능력 0.

**R-2 KWW/장벽분포 꼬리 일반형 — 지수 커널의 Laplace 중첩(유실 항목 회복) — 등급 B.**
무엇: 단일 장벽 ΔH_a 를 분포 ρ(ΔH_a)(따라서 ρ(L_V))로 일반화해 기억 커널 K(Δ)=∫ρ(L)(1/L)e^{−Δ/L}dL 을 세우고, 특수 경우로 stretched exponential exp[−(Δ/τ)^β] 와 β→1(ρ=δ) 회수를 보인다. 큐뮬런트 = 평균 ⟨L⟩·분산 ⟨L²⟩+var(L) 로 폭 예산 ① 항을 확장.
현행 보유: 부재 [확정 grep 0]. FABLE §4 "KWW/장벽분포 꼬리 일반형(v3/v4/v5) — v7 절삭·v10 은 apparent-U/η 로 부분 대체(6-30 [MODEL-1 선택] scope-out) — 의도적 scope-out, 단 진단 prose gap(기록됨)"(`FABLE_AUDIT_01_history_v3-v1011.md:52`) [확정]; §5-8 "Phase 4.1 명시 결정 항목: … KWW 진단 prose"(:64) [확정]. 부록 E 는 지수핵이 "rank-1(Markov)이라 등가 국소형이 1계 ODE"(`ch1_appE_selfconsistent.tex:70`) [확정] — 커널 일반화는 이 성질을 잃는다.
사다리 위치: 일반식 = 장벽 분포 위 지수 커널 중첩 → 가정 = ρ=δ(단일 장벽) → 회수 = `eq:memory`·`eq:lag`.
새 유도 단계: (a) 앙상블 평균 커널 → (b) Laplace 변환 관점(K̂=∫ρ(L)/(1+iωL)dL = H 의 일반화) → (c) 큐뮬런트와 widthbudget ① 확장 → (d) ρ=δ 회수 박스 + KWW 특수형. 4 식 + 부록 E 커널 변경 시 rank-1 상실 warnbox.
레퍼런스: Kohlrausch·Williams–Watts [미검증, 원장 부재]. SURV2 #1 큐뮬런트 검산(mean L_V·var L_V²·왜도 2, `SURV2_asymptotic_pert.md:38-45`) [확정].
모델 차원 +1(β 또는 σ_L) · 침습도 중~높(N8 커널 + 부록 E ODE 등가 붕괴 → Volterra 직접 적분 비용).
등급 근거: 사용자 방향 지시의 유실 항목이자 기준 ⑤ 일반화(단일 장벽 → 분포)에 정면이나, v1.0.15 [MODEL-1 선택] scope-out 결정이 존재해 재개방은 사용자 결정 사항. DQ-3.

**R-3 인과 기억 적분의 Watson 전개·초기층 명명(SURV2 #1 B+ 승계) — 등급 B(승계).**
무엇: `eq:tail-limit-sub` ∫₀^∞e^{−t}ξ′_eq(V−L_Vt)dt 의 Watson 전개 r/L_V=ξ′−L_Vξ″+L_V²ξ‴−… 와 인과 커널 큐뮬런트(평균 이동 +L_V·분산 +L_V²·왜도 2)로 폭 예산 ① 의 평균이동·왜도를 제1원리로 닫는다.
현행 보유: 준비형 존재(`ch1_sec09_tail.tex:127-129`) [확정]; 전개 자체는 부재. SURV2 #1 B+ "6 기법 중 유일하게 명백히 가산적 … 배경 박스 1개 … 기본상태 L_V/w∼10⁻⁸ 휴면 조건 각주"(`SURV2_asymptotic_pert.md:30-52`, 검산 :139-145) [확정].
사다리 위치: 일반식 = 인과 합성곱 → 가정 = L_V≪w → 회수 = 평형 종 `eq:tail-limit`(0차) + 1차 보정.
새 유도 단계: (a) Watson 보조정리 적용 → (b) 큐뮬런트 → (c) widthbudget ① 재진술 → (d) 휴면 조건. 박스 1.
레퍼런스: 표준(무인용 관용). 모델 차원 0 · 침습도 낮.
등급 근거: SURV2 판정 승계. R-2 를 채택하면 R-3 의 큐뮬런트가 그 특수형이 되어 자연 통합.

**R-4 고체상 확산 제한 완화(반응+확산 직렬) — 등급 B.**
무엇: 현행 지연은 표면 반응 제한(k_j) 단일 완화다. 구형 입자 Fick 확산의 1차 모드(τ_D=r²/π²D)를 직렬로 두어 유효 완화율 k_eff=(1/k_j+1/k_D)⁻¹ 를 얻고, Biot 수(반응/확산 비)로 두 극한을 가른다.
현행 보유: 부재 [확정]. 지연 정의 L_q=|I|/(Q_cell k_j) "요구와 공급의 비"(`ch1_sec08_lag.tex:24`) [확정]. 원장에 흑연 GITT 확산계수 park2021(D_Li≈10⁻¹¹–4×10⁻¹⁰ cm²/s, `ch1v22_bib.tex:28`)·persson2010(:30-31) 등재 [확정].
사다리 위치: 일반식 = 표면 반응 + 내부 확산 결합(경계조건) → 가정 = 확산 빠름(Bi≪1) → 회수 = 현행 L_q; 가정 = 1차 모드 근사 → 같은 1계 ODE 에 k_eff.
새 유도 단계: (a) 구형 확산 PDE 와 표면 플럭스 경계조건 → (b) 1차 고유모드 절단 → (c) 직렬 합성 k_eff → (d) L_q 박스 갱신 + Bi 극한. 4 식.
레퍼런스: park2021·persson2010·weppner_huggins1977 [확정 등재]; 확산 1차 모드 근사(표준) [무인용 관용].
모델 차원 +1(τ_D) · 침습도 중(N7 소절).
등급 근거: 기준 ⑤(단일 완화 → 결합 완화의 특수형)에 정합하고 GITT 서지가 이미 있으나, 데이터(율속 series)로 반응/확산 지배를 가려야 하므로 B. E-3 와 함께 "율속 의존" 패키지로 판정하는 것이 자연스럽다[추정].

### 4.5 축 S — 자기일관(Volterra·Fredholm ratio·전달함수·순환 의존)

**S-1 부록 E 의 3층(완전 비선형 Volterra ← 1차 ratio ← 동결 0차)을 사다리 "lag → 동결" rung 으로 승계 — 등급 A(위치는 DQ).**
무엇: `eq:sc-true`(참 문제)→`eq:sc-ratio`(1차)→`eq:sc-frozen`(동결) 사슬과 타당성 부등식 `eq:sc-valid`·열화 조건을 그대로 v2.0.0 동역학 장의 마지막 두 rung 으로 쓴다. 본문 승격 여부만 결정한다.
현행 보유: 부록 E 전문 [확정 — §3]. 정직 프레임 "계산 절감 아님 · 분석적 1차 닫힘 + 타당성 증명서 + 사용자 방법의 문건 내 시연"(`ch1_appE_selfconsistent.tex:137-143`) [확정].
사다리 위치: 일반식 = `eq:sc-volterra-eq`(비선형 Volterra) → 가정 = ε≪1 → 1차 ratio → 가정 = Ω→0 또는 깊은 꼬리 → 동결(정확 회수 derivbox :104-111).
새 유도 단계: 신규 0. 재배치 + E-1 채택 시 κ(ξ) 의 출발식을 일반 BV 로 접속.
레퍼런스: lee2017jcp·lee2011jcp·son2013jcp(Crossref 확정 주석, `ch1v22_bib.tex:45-47`) [확정 등재].
모델 차원 0 · 침습도 낮(부록 유지)/높(본문 승격).
등급 근거: P1 핵심·자산 무유실 원칙 직결. DQ-1.

**S-2 refs 6/7 도입 기록 5항의 완결(② 위치·⑤ 가정 차 대조) — 등급 A(A3급 정형 작업).**
무엇: P3 #5 의 다섯 항 가운데 ②(사용자 논문 내 사용 위치 page·paragraph)를 채우고, ⑤(가정 차)를 dossier 4건과 부록 E 4건으로 교차 대조해 확정한다.
현행 보유: 부록 E ② "페이지·문단 세부는 원문 대조로 확정 — 본 판은 방법 구조 기준"(`ch1_appE_selfconsistent.tex:120-121`) [확정 미완]. dossier ② "Sec. I p.144111-1 우단 2번째 문단 … Sec. II p.144111-4 Eq.(32) 직후"(`old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md:14-17`) [확정 — 단 dossier 는 "임시 열람 후 삭제(2026-05-29)" 표기(:3)이고 brief §4.1 은 현재 `Claude/JCP_147(14)_144111_(2017)….pdf`+`jcp_extract.txt` 소장을 실측(brief:102) — 재대조 가능]. ⑤ 대조: dossier (e)-1 Fredholm vs Volterra ↔ 부록 E ⑤(1) 종이 다름 [일치]; (e)-2 broad-kernel 열화 = stretched-tail 정면 충돌 ↔ 부록 E ⑤(3) 소파라미터·warnbox ε≳0.5(고전류·강 Ω) [부분 일치 — dossier 는 "closure 가 가장 필요한 저온·stretched tail 영역에서 가장 부정확할 수 있다"를 load-bearing 으로 명시(:42)하나 부록 E 는 고전류 축으로만 적음; R-2 채택 시 이 충돌이 되살아난다]; (e)-3 V_n 전하보존 비선형 결합 ↔ 부록 E 서두 warnbox 의 대수 근 배제 [일치·처리 방식 다름]; (e)-4 solvable baseline ↔ 동결해 = 가해 기준 [일치].
사다리 위치: 해당 없음(기록 완결).
새 유도 단계: 없음. 원문 대조 + 표 1.
레퍼런스: 위 3건 [확정 등재]. refs 6/7 원문 미소장(brief:102) [확정].
모델 차원 0 · 침습도 낮.
등급 근거: P3 #5 게이트 직결·CLAUDE.md P1 "실제 확인한 뒤 반영" 요구. DQ-6(PDF 재대조 vs dossier 채택), DR-8 과 연동.

**S-3 전달함수 H(ω) 와 Kubo 정적 극한 명명·동적 승격 경고(SURV1 #2 A·#6 B 승계) — 등급 C(잔여만).**
무엇: H(ω)=1/(1+iωL_V) 는 이미 집행(`ch1_appE_selfconsistent.tex:180-197`) [확정]. 잔여 = SM2-A 감수율을 "ω→0 Kubo 정적 극한"으로 1줄 명명 + 동적 χ(ω)=χ₀H(ω) 는 "구동 lag 이라 평형 FDT 아님·형식 유비" 경고 각주(`SURV1_integral_transform.md:134-147`) [확정 권고].
현행 보유: 명명 집행 여부 — `ch1_sec06_eqpeak.tex` 미독[미검증].
사다리 위치: T-1 σ 의 선형응답 극한 노드(T-2 와 짝).
모델 차원 0 · 침습도 낮. 등급 근거: SURV1 승계·명명뿐.

**S-4 Neumann/resolvent 오차 부등식(SURV1 #4b 보류 승계) — 등급 C.**
무엇: Fredholm-2 의 resolvent 전개로 ratio 치환의 명시 오차 부등식을 적는 것. SURV1 은 "#0/ref.6·7 확인 후 보강 후보"로 보류(:116-118) [확정]. 부록 E 는 이미 ε 를 Picard 수축률로 정량(:154-156)하고, Volterra 는 준멱영이라 Neumann 이 항상 수렴(SURV1 :116) [확정].
판정: dossier 로 논문 구조가 확인된 지금도 문건 문제는 Volterra 라 이득이 작다. 각주 1 이상 금지[추정].
모델 차원 0 · 침습도 낮.

**S-5 순환 의존 dependency graph 와 4분류 진단표(P3 #3·#4) — 등급 A.**
무엇: ξ_j·Q_bg·dQ/dV·dV/dQ·L_V·V_n·U_oc 의 순환 의존을 한 표(또는 그래프)로 적고 각 순환을 「정의상 implicit / 수치해법 필요 / 논리 공백 / 물리 가정 충돌」로 분류한다.
현행 보유: 분류 재료는 흩어져 존재 — 부록 E warnbox(전하보존 반전·배경 자기일관 = 대수 근, 유일성 = 요동 양성 :19-27; 지연 = 비선형 Volterra :60-65) [확정]; U_oc 음함수 `eq:implicit`·`eq:implicit_diff`(`ch2_sec05_mixing.tex:243` 자산 주석) [확정]; SURV1 #1 "3종 적분방정식 대조 keybox — Volterra-2(lag)/Fredholm-1(앙상블)/Fredholm-2(#0)"(:49-62) [확정 권고, 집행 여부 미검증]; SURV3 "두 '역'을 혼동하면 안 된다 — 반전은 well-posed·broadening 역산은 ill-posed"(`SURV3_convex_inverse.md:40`) [확정]. 단일 통합 표는 [근거 미발견].
사다리 위치: 해당 없음(구조 게이트).
새 유도 단계: 없음. 표 1(행 = 순환, 열 = 관여 식·변수·종·분류·해법·유일성 근거).
모델 차원 0 · 침습도 낮.
등급 근거: P3 #3·#4 게이트를 확인 가능하게 만드는 유일한 산출물이며 비용이 표 하나.

### 4.6 축 H — 히스테리시스(spinodal 과주행·CNT·Cahn–Hilliard·Preisach·분리 branch)

**H-1 γ_j 의 예측식화 — CNT/Cahn–Hilliard 승격(ROADMAP 제안 3) — 등급 B.**
무엇: 준안정 가지 이탈 조건 "핵생성률×체류시간∼1"에서 과주행 전위 V_ov(|I|,T)를 유도해 γ_j=ΔV_ov/ΔU^hys 를 γ(계면 에너지)·v_m·시도 빈도·소인 속도의 함수로 닫고, spinodal 상한(γ_j=1)과 Maxwell(γ_j→0)을 극한으로 회수한다. 불안정 영역은 Cahn–Hilliard 성장률 R(k) 로 꼬리 길이 근거.
현행 보유: γ_j·h_η "값은 피팅이 정하며 … spinodal gap 은 그 피팅값이 넘을 수 없는 열역학 상한"(`ch1_sec04_hys.tex:250-252`); "CNT 는 γ_j 의 근거이지 예측식이 아니다 — γ_j 는 전이당 한 계수로 남는 현상학 인자(모델 차원 불변)"(:262-264) [확정]. 부록 `eq:app-rstar`·`eq:app-ch-R` [확정]. ROADMAP 제안 3 "현상학 인자 제거 … 난이도 고·침습도 높음(부록→본문 승격) … 외부 위임 ★★☆"(`ROADMAP_future_physics.md:25-29`) [확정]. cogswell2012 는 "본 문건 γ 수치의 출처 아님(스케일 상정은 tier C)"(`ch1v22_bib.tex:27`) [확정 — 입력 미보유].
사다리 위치: 일반식 = 자유에너지 범함수 F[ξ]+보존 동역학 ∂ξ/∂t=M∇²μ(CH) → 가정 = 균일(∇→0) → 평균장 g(ξ)·spinodal(현행) ; 가정 = 준안정 + 유한 핵 → CNT 율 → 가정 = 이탈 조건 → γ_j 예측식 → 극한 회수(γ_j=1 spinodal, γ_j→0 Maxwell).
새 유도 단계: (a) CH/CNT 출발 → (b) 이탈 조건(율×시간) → (c) V_ov 음함수 → (d) γ_j 박스 + 두 극한. 5~6 식·부록 두 절 본문 승격.
레퍼런스: 부록 [A1] Cahn–Hilliard 1958·[A2] Cahn 1961·[A3]·[A5]·dreyer2010·dreyer2011·cogswell2012 [확정 등재].
모델 차원: γ_j(전이당 1) → (γ_surf, ν₀ 전역 2)로 **감소 가능**하나 입력값 미보유 시 tier C · 침습도 높.
등급 근거: 세 축 가운데 예측력 이득이 가장 크고 원구상 Chapter 5 의 "계층" 요구에 정면이나, 계면 에너지·시도 빈도 등 수치 입력이 없고(Non-goal 회사 데이터·신규 다운로드 DQ) 부록→본문 승격이 사용자 결정 사항이라 B. DQ-1·DQ-4 연동.

**H-2 평형 rung 의 정본: 정규용액 등온선 → Ω>2RT Maxwell(두-상 delta·Dreyer plateau) / Ω→0 logistic — 등급 A(사다리)·커널 채택은 조건부.**
무엇: brief 3.2 의 "평형(정칙용액→로지스틱)" rung 을 현행 자산으로 실현한다 — Part 0 g(ξ)·μ(θ) → `eq:Veq`(음함수 등온선) → Ω>2RT 에서 Maxwell 등면적(부록 `eq:app-maxwell`)이 단일 plateau 전위와 delta 형 dQ/dV 를 주고 Dreyer 다입자 순차 전환이 그 경로를 준다(§7 (iii-a)) → Ω→0 에서 `eq:xieq` logistic 회수. 커널로 채택할 경우 LIT 헤드라인 "로지스틱을 정칙용액(Frumkin)으로 최소일반화 … Ω>2RT + Maxwell ⊗ kinetic 폭"(`LIT_ADVANCE_SYNTHESIS.md:15-23`) 이 그 실현이다.
현행 보유: 등온선·spinodal·Maxwell·Dreyer 전부 보유 [확정 — §3 히스 사슬; `ch1_sec07_broadening.tex:28-30`("Maxwell 공통접선의 값과 Dreyer 순차전환의 경로는 양립") grep]. 폭 w_j 의 이중지위 — 두-상에서는 "평형이 예측하는 것이 폭이 아니라 날카로운 선(델타)이므로 같은 w_j 가 … broadening 이 정하는 현상학적 자유 피팅 폭"(`ch1_sec05_width.tex:308-311`) [확정]. regsol dQ/dV 커널은 v1.0.25 에서 삭제되되 "Ω 물리 전량 유효"(brief §4.4:120) [확정]. regsol2 실검증 R² 0.943 vs 0.938, Ω_j/RT=[4.06,2.02,3.55,4.07] 전부 >2RT·"R² 개선 미미(+0.5%) … 진짜 가치 = 파라미터 물리성·일관성"(`LIT_ADVANCE_SYNTHESIS.md:100-113`) [확정]. v1.0.26 A/B(물리 4전이 vs gallery 7전이) 실행 차단·미완(brief §4.3:112·A7) [확정].
사다리 위치: 일반식 = 정규용액 g(ξ)(Part 0) → 가정 Ω>2RT = 두-상(Maxwell delta ⊗ kinetic/앙상블 폭) / 가정 Ω≤2RT·Ω→0 = 단상 logistic(폭 n_jRT/F). 두 가지가 같은 Ω_j 로 갈리므로 "전이별 분류의 물리 근거"(`ch1_sec05_width.tex:313-320`)와 정합.
새 유도 단계: (a) `eq:Veq` → (b) Maxwell 조건(부록 재사용) → (c) 두-상 평형 dQ/dV = Q_jδ(V−U_j^Maxwell) 와 Dreyer 유한-N plateau → (d) 극한 회수 박스(Ω→0 logistic·Ω→2RT⁺ 연속). 커널 채택 시 추가 (e) ⊗ kinetic 합성(전달함수 H 와 앙상블 Gaussian).
레퍼런스: leviaurbach1999·verbrugge2017·dreyer2010·dreyer2011·huggins2009·mckinnon1983·msmr_partII(Paul 2024 ω 스펙트럼) [확정 등재]. Yao–Viswanathan 2024·Cordoba 2024·Fujimoto 2022·Flores 2021 은 LIT 가 "전부 실검증"(:127-129)이라 적었으나 원장 미등재[미검증].
모델 차원 0(Ω_j 기존) · 침습도 높(N4/N5/N6 평형층 커널·w_j 지위).
등급 근거: 사다리 rung 자체는 자산 재배열이라 A. 두-상 **커널 채택**(delta ⊗ kinetic vs 로지스틱 자유폭)은 2.6 판정(GITT 평형 데이터·v1.0.26)에 종속 — 조건부. DQ-4.

**H-3 Preisach 분류 노트(SURV4 #2 B) — 등급 C. 연산자·연속 밀도·FORC 채택 — D.**
무엇: "전이 하나 = 릴레이 히스테론 하나(α_j,β_j=U_j±½γ_jhΔU^hys), 모델 = 원자적 밀도 극한, h_η = minor-loop 를 스칼라로 접은 것" 1~2문장 명명.
현행 보유: 부재 [확정 grep 0]. SURV4 판정(:49-66) 과 스코프 벽 [C-92] [확정].
사다리 위치: 없음(분류 노트). 모델 차원 0 · 침습도 낮.
등급 근거: SURV4 승계. 연산자 채택은 "차원 폭발 + 경로의존 스코프 위반" D 승계.

**H-4 cusp 보편 지수 각주(SURV4 #1 B) — 등급 C.**
무엇: (T_c−T)^{3/2} 소멸이 cusp 파국의 보편 fold-분리 지수임을 1~2문장(SURV4 검산 1.4987 vs 1.5000, :44-47) [확정]. SURV2 #3 RG "3/2 는 평균장 지수 — 실계는 임계 근방서 둥글며 그 편차는 γ_j 가 흡수" caveat 1줄(:71-86) [확정]. 모델 차원 0 · 침습도 낮.

**H-5 Si 히스테리시스 — 분리 branch 파라미터화(LIT S4 ◐)와 Larché–Cahn 가역 결합 승계·소성 구성식 Non-goal 유지 — 등급 B(분리 branch)/D(소성 구성식).**
무엇: Si-host 에 리튬화/탈리튬화 분리 U_j branch(준정적 offset)를 두고, 가역 결합 `eq:si-coupling` 을 "응력이 만드는 전위 이동의 일반식", 탄성 극한(히스 0)과 소성 경로 의존(GS-1)을 그 두 가정으로 배열한다.
현행 보유: `ch3v22_sec04_mech.tex` 전문 [확정]; LIT S4 "Si 히스테리시스 = 분리 U_j branch ◐선검증 — Köbbing 2024; 우리 L_V lag 는 잔여 율의존만"(:85) [확정]; GS-1 4분류(물리 가정 충돌 + 유도 미완결 범위 선언 :89-99) [확정].
사다리 위치: 일반식 = 응력 실은 μ(Larché–Cahn) → 가정 탄성 = 단일값 σ_h(θ) → 히스 0 회수 ; 가정 소성 = 경로 의존 → 분리 branch 현상학(ΔV^mech 를 전이당 상수로).
새 유도 단계: (a)~(d) 기존 유지 + 분리 branch 박스 1.
레퍼런스: larchecahn1973·sethuraman_stressevo2010·sethuraman_stresspot2010·koebbing2024·jiang_sihys2020·beaulieu2001 [확정 등재].
모델 차원 +1/Si 전이(branch offset) · 침습도 낮(Ch3 소절).
등급 근거: 사다리 정합·서지 확실·데이터 판정 필요(◐). 소성 구성식은 Non-goal("유사 유도로 소성 구성식을 지어내지 않는다" :98) D 승계.

**H-6 히스테리시스의 비평형 열역학 언어 — 준안정 가지 위 affinity 잔여 → 소산 — 등급: Q-2 로 이관.**

**H-7 경로 의존(minor loop·wiping-out)·h_η 정량 — 등급 D(스코프 벽 [C-92]·SM2 축 C 승계).**

### 4.7 축 Q — 비가역 발열(Bernardi·flux–force)

**Q-1 Q̇_irr=I(U_oc−V) 의 분해 — 분극 소산 I²R_n + 동역학 지연 소산 + 히스 분기 소산 — 등급 A.**
무엇: U_oc−V_app=(U_oc−V_n)+(V_n−V_app) 로 갈라 (i) N1 옴 소산 I²R_n, (ii) N7/N8 지연의 국소 과전압 소산 I·η_kin(ξ_lag 대 ξ_eq 의 affinity 차 — (RT/F)ln 형), (iii) N3 분기 이동 ½σ_dh_ηγ_jΔU^hys 의 소산을 각각 닫고, |I|→0(L_V→0)·γ_j→0 에서 소멸함을 회수한다. T-1 의 σ 항별 대응.
현행 보유: 첫 항 "유지"만(`ch2_sec07_revheat.tex:36`); "과전압 소산(2법칙상 항상 발열, Part I 의 동역학 꼬리·분극이 만드는 소산)"(:21-22) [확정 — 서술뿐]. 원구상 Chapter 2 의 미실현 절반(§2 표).
사다리 위치: 일반식 = Tσ(T-1) → 가정 등온·균일 → Q̇_irr → 항별 분해 → 회수 = Bernardi 첫 항·평형 극한 0.
새 유도 단계: (a) 과전압 분해 → (b) 각 항의 표현(R_n·L_V·ΔU^hys 입력만) → (c) 부호·양성 검산(σ≥0) → (d) 박스 + 극한. 4~5 식·신규 절 1(Part T 또는 4.4).
레퍼런스: bernardi1985·newman [확정 등재].
모델 차원 0(입력 전부 기존) · 침습도 중.
등급 근거: 사용자 기준 ⑤ 와 원구상 Chapter 2 완성·모델 차원 0·서지 확실. 열 사슬에서 유일하게 "새 식이 나오는" 후보.

**Q-2 히스 gap 소산의 entropy production 정식화(사이클당 W_diss,j=Q_jγ_jh_ηΔU^hys) — 등급 B(범위 선언 해제 조건부).**
무엇: [C-92] 가 "∝IΔU^hys 소산율·사이클당 ∝Q_cycleΔU^hys" 로 서술만 한 것을 T-1 의 σ 항으로 정식화한다 — 준안정 가지 위 affinity 잔여 F(V_branch−V_Maxwell) 와 반응 플럭스의 곱. 완전 cycle 한정이면 경로의존 정량 없이 닫힌다.
현행 보유: warnbox(`ch2_sec05_mixing.tex:230-238`) "경로의존 측정 불확실도의 정량은 본 장 범위 밖, 공백으로 명시" [확정]; SURV4 스코프 벽 "[C-92] warnbox — 히스 gap 소산은 비가역·∂/∂T 와 별개·경로의존 정량은 범위 밖으로 명시 선언 / SM2 축 C — Jarzynski/Crooks 범위 밖"(:28-31) [확정].
사다리 위치: T-1 σ → 가정 완전 cycle·선형화(ΔU^hys≪w_j, `eq:hys_rev` 의 근사와 동일 :224) → 회수 = [C-92] 의 비례식.
새 유도 단계: (a) σ 의 반응 항에 분기 affinity 대입 → (b) 사이클 적분 → (c) 선형화 → (d) 박스. 3 식.
레퍼런스: dreyer2010·hysteresis2018 [확정 등재].
모델 차원 0 · 침습도 낮~중.
등급 근거: 값 있는 신규 식이나 "범위 밖" 선언(경로의존)과의 경계를 완전 cycle 로 명시 재설정해야 한다 — DQ-2. 부분 cycle(h_η)의 소산은 여전히 밖.

**Q-3 Bernardi 소거 항(혼합 엔탈피·상변화)의 부활 조건 등록 — 등급 C.**
무엇: 두 전제(:21-25)를 가정 사다리의 명시 노드로 등록하고, E-3 채택 시 혼합 엔탈피 항이 확산층 농도 프로파일로 되살아나는 조건을 각주로.
현행 보유: 전제 서술 [확정]. 모델 차원 0 · 침습도 낮. 등급 근거: 기준 ⑤ 가정 명시 이득만; 실제 유도는 E-3 종속.

**Q-4 비등온 T(V) 되먹임(자기발열 → U_j(T)·동역학) — 등급 D(승계).**
SURV2 #6 "진짜 비등온 T(V) 는 모델에 부재 … 등온-per-curve 설계 … 조건부 미래 후보로만"(:120-132) [확정]. T-1 의 열류 항 소거 가정으로만 등록(DQ-7).

---

## 5. 사다리 실현 가능성 판정 — "일반 비평형 열역학 상태식 → 준평형 → 평형(정칙용액→로지스틱) · 동역학 일반(TST) → lag → 동결"

| rung | 일반식 | 내려가는 가정 | 회수 식(현행 자산) | 현행 보유 | 신규 유도 | 실현 판정 |
|---|---|---|---|---|---|---|
| L0 일반 비평형 열역학 상태식 | 국소 Gibbs 관계 + 엔트로피 수지 σ=ΣJX≥0 (T-1) | 등온·균일(열류·농도 구배 소거 = Bernardi 두 전제·SURV2 #6 등온-per-curve) · 전이당 단일 반응좌표 | Q̇_irr=I(U_oc−V)(`eq:qrev` 첫 항) · 반응 항 J_j𝒜_j | 부재 [확정] | 절 1(5~6 식) | **가능** — 모델 차원 0·표준 유도. 조건 = 서지 신규 등재(DQ-5)·선형 flux–force 는 회수 없는 노드로 표기(T-2) |
| L1 준평형 | 반응 플럭스 J=k⁺(1−e^{−𝒜/RT})(Marcelin–de Donder 형) | 𝒜→0(|I|→0) → 플럭스 소멸·U_oc 준평형(GITT) | `eq:vn` 의 |I|→0 극한 V_n=V_app · `eq:db` detailed balance | 부분(GITT srcbox `ch1_sec01_n0n1.tex:220-240`·detailed balance) [확정] | 소절 1(2 식 + 표) | **가능** — 정식화만. 정직 조건 = 문건 작동창(𝒜_cut=4RT)이 선형 영역 밖임을 표에 명시 |
| L2 평형(정규용액 → 로지스틱) | Part 0 g(ξ)·μ(θ) → `eq:Veq` 음함수 등온선 | Ω>2RT: Maxwell 공통접선(delta ⊗ 폭) / Ω≤2RT: 단상 / Ω→0: logistic | `eq:xieq`·`eq:eqpeak`·`eq:dUhys`·부록 `eq:app-maxwell` | 90% [확정] — 결손 = 두-상 평형 커널의 dQ/dV 형태 채택 여부 | (a)~(d) 1 사슬(4 식) + 커널 채택 시 합성 1 | **가능** — 단 두-상 커널은 2.6 데이터 판정 종속(DQ-4). 채택 여부와 무관하게 rung 자체(극한 회수)는 닫힌다 |
| L3 동역학 일반(TST) | `eq:tst-rate` k=(k_BT/h)(q‡/q_R)e^{−ΔE₀/RT} | 안장점 준평형·κ=1(K-2)·χ 분할(E-1/E-2 회수)·조성무관 교환속도 | `eq:bv`·`eq:db`·`eq:kuniv`·`eq:tst-box` | 100% [확정] | 0(재배열 K-1) | **가능** — 재배열만. 침습도 높(구조) |
| L4 lag | 완화 ODE(R-1 master equation 극한) → 인과 기억 `eq:memory` → 참 자기일관 `eq:sc-true` | 자리 독립·M→∞(결정론) · 단일 장벽 ρ=δ(R-2) · 반응 제한 Bi≪1(R-4) | `eq:Lq`·`eq:lag`·`eq:reversal`·`eq:tail-limit` | 100% [확정] | R-1 소절 1; R-2/R-4 옵션 | **가능** — 핵심은 승계. 옵션 채택 시 모델 차원 +1 씩 |
| L5 동결 | 비선형 Volterra `eq:sc-volterra-eq` | ε≪1 → 1차 ratio → 깊은 꼬리/Ω→0 → 컷 동결 `eq:Acut`·`eq:LV` | 부록 E 3층 + `eq:sc-valid` | 100% [확정] | 0(S-1 재배치) | **가능** — 자산 그대로. 위치(부록/본문) DQ-1 |
| 교차 | 평형 ← 동역학 정지점(`eq:db`)·분포 관점(`sec:dist` `ch1_sec05_width.tex:389-422`) | — | 두 경로 통합 | 100% [확정] | 0 | 사다리 두 갈래(열역학·동역학)를 잇는 기존 자산 |

**종합 판정(추정).** 사다리는 실현 가능하다. 여섯 rung 가운데 넷(L2·L3·L4·L5)은 boxed 식·라벨·검산을 그대로 두고 배열만 바꾸는 승계이고, 둘(L0·L1)은 모델 차원 0 의 신규 절 1~2개(T-1·T-2·Q-1·Q-2 가 그 안에서 갈라진다)로 닫힌다. 자산 무유실 기준(v1.0.22 계보 감사 ③=0건, brief §4.4)은 boxed 64 식이 전부 위 표의 "회수 식" 열에 자리를 가지므로 원리상 충족 가능하다 — 실제 매핑(boxed 64 각각 → rung)은 작업 챕터 2.1 자산 지도가 낸 목록으로 3.2 에서 수행해야 하며 본 카탈로그는 그 매핑을 대신하지 않는다.

**정직 조건 네 가지.** (1) L0→L1 의 선형 flux–force 는 문건이 회수하지 않는 노드다 — "Onsager 를 넣었다"는 서술은 과장이 되므로 T-2 의 작동창 표와 warnbox 가 필수. (2) L2 두-상 커널은 2.6 판정 없이는 "극한 회수까지만" 닫힌다 — regsol 삭제 결정(v1.0.25 F1)과 w_j 이중지위(`ch1_sec05_width.tex:299-311`)와의 정합을 커널 채택 시 재설계해야 한다. (3) L4 의 옵션(R-2 KWW·R-4 확산·E-3 농도 분극)은 각각 모델 차원 +1 이고 부록 E 의 rank-1 ODE 등가를 잃을 수 있어(R-2) 자기일관 절의 비용이 오른다 — 3.7 DG-B 에서 묶어 결정. (4) L0 의 등온·균일 가정은 SURV2 #6 등온-per-curve 설계와 같은 결정이며, 비등온 되먹임(Q-4)은 D 로 남는다.

---

## 6. 기각군 승계 목록(재조사 0)

| 항목 | 출처·등급 | 기각 근거(원문) |
|---|---|---|
| Wiener–Hopf | SURV1 #3 D | "커널이 초등(지수)이라 이미 닫힘 … 인과 deconvolution 은 문건이 명시 금지" (`SURV1_integral_transform.md:98-104`) |
| Green 함수 독립 절 | SURV1 #5 C→흡수 | "적분인자 해가 곧 Green 함수 — 순수 재명명" (:122-130) |
| 동적 Kubo χ(ω) 승격 | SURV1 #6 경고 | "구동 lag L_V∝|I| ≠ 평형 상관시간 — 범주 오류" (:142-146) |
| WKB/준고전 | SURV2 #4 D | "조화=이미 exact·홉핑/CNT=열활성" (`SURV2_asymptotic_pert.md:90-100`) |
| 다중척도(비등온) | SURV2 #6 C/D | "T(V) 동역학장 부재 … 등온-per-curve 설계" (:120-132) |
| RG 장치 | SURV2 #3 C−/D | "spinodal 훼손·비임계 작동창·γ_j 이중계산" (:71-86) |
| 안장점 독립 절·CLT-via-saddle | SURV2 #2 B−/D | "교과서 bloat" (:56-67) |
| 중심다양체 | SURV4 #3 D | "축약 대상·동역학 분기 부재" (`SURV4_bifurcation_stochastic.md:68-73`) |
| Langevin/SDE 독립 | SURV4 #6 D | "SM2B 1/√M 벌크 자멸·#4 로 병합" (:90-95) |
| Preisach 연산자·연속 밀도·FORC | SURV4 #2 D | "차원 폭발 + 경로의존 스코프 위반" (:61-65) |
| 대편차(LDT) 절 | SURV4 #5 C(1문장 상한) | "무거운 기계·payoff 0·Ω>2RT 독립-자리 붕괴" (:83-88) |
| Tikhonov 역합성곱·MaxEnt 역용도 | SURV3 #2·#3 C(별도 역문제 버전) | "forward-only 선언과 충돌" (`SURV3_convex_inverse.md:54-68`) — brief Non-goal(역문제) |
| 볼록최적화 전역해 보증 | SURV3 #6 C(D-근접) | "목적함수 비볼록 — 표제 이득 불성립" (:86-92) |
| Bazant/Dreyer PDE 생성기 | LIT M6 ✗ | "무거운 PDE(회피대상)·물리 정당화로만 인용" (`LIT_ADVANCE_SYNTHESIS.md:97`) |
| 흑연 비대칭 폐형 커널의 "문헌 근거" 주장 | LIT M7 ✗ | "미발표(창시=우리 몫)" (:98) |
| 전이 6+ 증설·DFT 결합E→Ω 대입 | LIT G6·G7 ✗ | (:64-65) |
| 블렌드 역학 결합(Si 팽창→흑연 shift) | LIT S6 ✗ | "평형 dQ/dV 스코프 밖" (:87) |
| Si 소성 구성식 창작 | ch3 GS-1 Non-goal | "유사 유도로 소성 구성식을 지어내지 않는다" (`ch3v22_sec04_mech.tex:98`) |
| 경로의존 소산 정량·Jarzynski/Crooks | [C-92]·SM2 축 C | (`ch2_sec05_mixing.tex:230-238`; SURV4 :28-31) |
| 역방향 식별 사슬 S0–S5 복원 | FABLE §4:50 미계승 | 피팅 방법론 = brief Non-goal(역문제·코드 동기) — 본 카탈로그 범위 밖, 작업 챕터 1.4 등록만 |

---

## 7. 등급 요약과 우선순위(3.2 설계 입력용)

| ID | 후보 | 등급 | 모델 차원 | 침습도 | 조건·게이트 |
|---|---|---|---|---|---|
| K-1 | Eyring/TST 척추 재배열 | A | 0 | 높 | 3.3 구조 결정(DG-A)과 동시 |
| T-1 | entropy production 일반 상태식 | A | 0 | 중 | 서지 신규 등재(DQ-5) |
| S-1 | 부록 E 3층 승계 | A | 0 | 낮/높 | 위치(DQ-1) |
| S-2 | refs 6/7 5항 완결 | A | 0 | 낮 | PDF 재대조(DQ-6·DR-8) |
| S-5 | 순환 의존 dependency graph·4분류 표 | A | 0 | 낮 | P3 #3·#4 게이트 |
| H-2 | 정규용액→로지스틱 rung(극한 회수) | A / 커널 채택 조건부 | 0 | 높 | 2.6 판정(DQ-4) |
| Q-1 | Q̇_irr 분해(옴·지연·분기) | A | 0 | 중 | — |
| E-1 | 조성 의존 교환전류 ↔ κ(ξ) 통일 | B | 0/+1 | 중 | 활동도 형태·LIT G5 상충 |
| E-3 | 농도 분극(NP·Warburg·Nernst shift) | B | +1~2 | 높 | 데이터(EIS·율속)·DQ-8 |
| T-2 | 선형 flux–force 회수창 | B | 0 | 낮 | warnbox 필수 |
| R-1 | master equation→OU·Kramers | B | 0 | 중 | — |
| R-2 | KWW/장벽분포 커널 | B | +1 | 중~높 | scope-out 재개방(DQ-3) |
| R-3 | Watson 전개·큐뮬런트 | B(승계) | 0 | 낮 | 휴면 조건 각주 |
| R-4 | 확산 제한 완화 | B | +1 | 중 | 율속 데이터 |
| H-1 | γ_j 예측식(CNT/CH) | B | −1~+1 | 높 | 계면 에너지 입력·DQ-1 |
| H-5 | Si 분리 branch | B/D | +1/Si | 낮 | ◐ 데이터 |
| Q-2 | 히스 소산 entropy production | B | 0 | 낮~중 | [C-92] 해제(DQ-2) |
| K-2 | κ·변분 TST 가정 등록 | C | 0 | 낮 | — |
| E-2 | Marcus 일반형·BV 회수 | C | 0/+1 | 낮 | λ 근거 부재·DQ-10 |
| S-3 | Kubo 정적 극한 명명 | C | 0 | 낮 | sec06 집행 여부 미검증 |
| S-4 | Neumann 오차 각주 | C | 0 | 낮 | — |
| H-3 | Preisach 노트 | C | 0 | 낮 | 연산자 D |
| H-4 | cusp 지수 각주 | C | 0 | 낮 | — |
| Q-3 | Bernardi 소거 항 조건 | C | 0 | 낮 | E-3 종속 |
| Q-4·H-7·§6 전건 | 기각 | D | — | — | 승계 |

우선순위 제안[추정]: 3.2 사다리 설계는 A 7건을 골격으로 하고, B 가운데 **모델 차원 0** 인 T-2·R-1·R-3·Q-2 를 기본 채택 후보로, 모델 차원 +1↑ 인 E-3·R-2·R-4·H-1·H-5 를 "율속·상분리 데이터 패키지"로 묶어 3.7 DG-B 에서 일괄 결정하는 것이 자산 무유실·기준 ⑤·Non-goal(회사 데이터) 셋을 동시에 지킨다.

---

## 8. Decision Queue

- **DQ-1 부록 E·상분리 부록의 본문 승격.** 상분리 부록은 독립 문서이며 "본문 편입 여부는 사용자 검토 후 결정"(`appendix_phase_separation.tex:7`)으로 남아 있고, 부록 E 는 v1.0.24 신설 부록이다. 3.3 (b)안(Part I 일반 이론)을 택하면 두 부록의 핵심(Maxwell·CNT·CH·자기일관 3층)이 4.2·4.3·4.5 본문 rung 이 된다. 기본값 제안 = (b) 시 본문 승격, (a) 시 부록 유지·본문 참조 강화. 사용자 결정.
- **DQ-2 [C-92] "히스 소산·경로의존 정량은 범위 밖" 선언의 부분 해제.** Q-2 는 완전 cycle 한정으로 경로의존 없이 닫히지만, 선언 문구가 "히스 gap 소산 자체"를 범위 밖으로 읽히게 한다. 제안 = "완전 cycle 소산은 범위 안, 부분 cycle(h_η)·경로의존 불확실도는 범위 밖"으로 재설정. 사용자 결정.
- **DQ-3 KWW/장벽분포(R-2) 재개방.** v1.0.15 [MODEL-1 선택] scope-out 결정(FABLE §4:52)이 존재한다. 재개방 시 모델 차원 +1·부록 E rank-1 등가 상실. FABLE §5-8 이 "Phase 4.1 명시 결정 항목"으로 지정한 사안. 사용자 결정.
- **DQ-4 L2 두-상 평형 커널 채택 = 2.6 판정.** regsol 삭제(v1.0.25 F1)·Ω 물리 유효(brief §4.4)·regsol2 R² 미미 개선(LIT §6)·v1.0.26 미완이 겹친다. 본 카탈로그는 "rung(극한 회수)은 무조건, 커널은 데이터 판정 후"로 분리 제안. 골격 2.6 과 정합하므로 이견 아님 — 등록만.
- **DQ-5 신규 서지 등재(DR-6 종속).** T-1·T-2·R-1·R-2·E-2 가 요구하는 de Groot–Mazur·Prigogine·Onsager 1931·de Donder·Kramers 1940·Kohlrausch/Williams–Watts·Marcus/Chidsey 는 원장 부재[미검증]. 기억 서지 금지 규약상 Crossref 검증 없이는 인용 불가 → 외부 접근 허용 여부에 종속.
- **DQ-6 refs 6/7 ② 위치 항목의 근거 선택.** dossier 는 page·paragraph 를 적었으나 "임시 열람 후 삭제" 표기(dossier:3)이고, brief §4.1 은 현재 PDF·추출 텍스트 소장을 실측했다. 제안 = 소장 PDF 로 ② 재대조 후 부록 E ② 갱신(dossier 는 교차 근거). 이 불일치(삭제 기록 vs 현 소장) 자체를 작업 챕터 1.3 등록부에 표면화 요망.
- **DQ-7 등온-per-curve 유지 확인.** L0 의 열류 항 소거 가정과 Q-4 D 판정은 같은 결정이다. 기본값 = 유지(Non-goal Task #38 과 정합). 확인만.
- **DQ-8 E-3 농도 분극 층 도입.** 모델 차원 +1~2·N1 신규 layer·EIS/율속 데이터 의존. 기준 ⑤ 일반성 이득 vs Non-goal(회사 데이터 정량) — 도입하되 tier·warnbox 정직 표기하는 안이 기본값 제안. 사용자 결정.
- **DQ-9 brief §4.5 "SM2-A/B/C 집행 여부 미확정".** 본 에이전트는 `ch1_sec06_eqpeak.tex`·`ch1_sec02b_part0.tex` 전문을 정독하지 않아 판정하지 않는다(S-3 미검증 표기). 작업 챕터 1.4 확인 항목으로 유지.
- **DQ-10 brief 3.1 축 목록의 "Marcus".** 문건 관심 영역(|𝒜|≤4RT)에서 Marcus 곡률의 실효 근거가 없고 λ 값이 문건에 없다. 제안 = 사다리 상단 일반형으로 소개 + BV 회수 조건 명시 + 채택 안 함(C). 골격 이견이 아니라 등급 처리 제안.
- **DQ-11 "Chapter" 이름공간 넷.** brief §5 는 3축(작업 챕터·문건 Chapter 1~3·ver.1~5)을 말하나 CLAUDE.md P1 원구상 Chapter 1~5 가 네 번째다. 통합 초안 Phase Range 표 상단 주석에 4축 대응(§2 표)을 두기를 제안.
- **DQ-12 brief §4.4 "gallery ≠ 상(XRD 상 수 불변)" 과 H-2 두-상 커널.** 정규용액 커널을 gallery 별로 두면(LIT 경로 (ii)) gallery 7전이 vs 물리 4전이 논점(v1.0.26 A/B)과 얽힌다. 2.6 정식화 시 "커널 단위 = 상 전이(4)"를 기본값으로 둘 것을 제안. 사용자 결정.

---

## 9. Read Coverage(파일·행 범위 전건)

전문 정독(head→tail, 생략 없음):

| # | 파일(`D:\Projects\Project_Anode_Fit\Claude\` 기준) | 행 범위 |
|---|---|---|
| 1 | `results/handoffs/2026-09-02-v2-master-plan/brief.md` | 1–219 |
| 2 | `docs/v1.0.18.2/ROADMAP_future_physics.md` | 1–50 |
| 3 | `results/comp_v24/LIT_ADVANCE_SYNTHESIS.md` | 1–130 |
| 4 | `docs/v1.0.22/results/comp_v23/SURV_SYNTHESIS.md` | 1–45 |
| 5 | `docs/v1.0.22/results/comp_v23/SURV1_integral_transform.md` | 1–179 |
| 6 | `docs/v1.0.22/results/comp_v23/SURV2_asymptotic_pert.md` | 1–164 |
| 7 | `docs/v1.0.22/results/comp_v23/SURV3_convex_inverse.md` | 1–125 |
| 8 | `docs/v1.0.22/results/comp_v23/SURV4_bifurcation_stochastic.md` | 1–135 |
| 9 | `docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` | 1–73(§4 포함 전문) |
| 10 | `old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md` | 1–50 |
| 11 | `docs/v1.0.25.1/_sections/ch1_appE_selfconsistent.tex` | 1–218 |
| 12 | `docs/v1.0.25.1/_sections/ch1_sec01_n0n1.tex` | 1–245 |
| 13 | `docs/v1.0.25.1/_sections/ch1_sec04_hys.tex` | 1–337 |
| 14 | `docs/v1.0.25.1/_sections/ch1_sec05_width.tex` | 1–425 |
| 15 | `docs/v1.0.25.1/_sections/ch1_sec08_lag.tex` | 1–149 |
| 16 | `docs/v1.0.25.1/_sections/ch1_sec09_tail.tex` | 1–254 |
| 17 | `docs/v1.0.25.1/_sections/ch1_sec13_lcohys.tex` | 1–224 |
| 18 | `docs/v1.0.25.1/_sections/ch3v22_sec04_mech.tex` | 1–111 |
| 19 | `docs/v1.0.25.1/appendix_phase_separation.tex` | 1–498 |
| 20 | `docs/v1.0.25.1/_sections/ch1_sec00_intro.tex` (배정 외 보강 — 척추 정의 확인) | 1–95 |
| 21 | `docs/v1.0.25.1/_sections/ch2_sec07_revheat.tex` (배정 외 보강 — Bernardi 항 확인) | 1–103 |

부분 확인(전문 정독 아님 — 인용 행만 근거로 사용):

| 파일 | 행 범위·방법 |
|---|---|
| `docs/v1.0.25.1/_sections/ch2_sec05_mixing.tex` | 215–244 Read([C-92] warnbox·`eq:hys_rev`) |
| `docs/v1.0.25.1/_sections/ch1v22_bib.tex`·`ch2v22_bib.tex`·`ch3v22_bib.tex` | `\bibitem` 행 전건 grep(등재 키 확인용) |
| `docs/v1.0.25.1/_sections/*.tex` 전건 | 키워드 grep(Bernardi·Onsager·Marcus·Nernst-Planck·Warburg·KWW·Kohlrausch·Fokker·master equation·Langevin·Kramers·Preisach·Cahn·Larché·Butler·Redlich·Dreyer·Bragg·가역 발열) 및 라벨 위치 grep(`eq:eqpeak`·`eq:sm-mc-fluc`·`eq:skewpeak`·`eq:widthbudget`·`eq:ensavg`·`eq:sm-thresh`·`eq:gxi`·`eq:mu`·`eq:eqcond`·`eq:sm-mc-balance`·`eq:Uj`·`eq:sum`·`eq:belliden`·`eq:hys_rev`·`eq:sm-nernst`·`eq:sm-muV`·`eq:fermifn`·`eq:partfn`·`eq:sm-sint`·`eq:msmr`·`eq:blend-balance`) — 결과 행 번호를 §2·§3 의 path:line 근거로 사용 |

미정독(본 카탈로그가 판정을 보류한 원천): `ch1_sec02a/02b_part0.tex`·`ch1_sec06_eqpeak.tex`·`ch1_sec07_broadening.tex`(grep 행만)·`ch2_sec08_synthesis.tex`·`results/comp_v26_data/HANDOVER_regsol_investigation.md`·`docs/v1.0.22/results/comp_SM2/SM2_SURVEY.md`·`results/comp_v24/IMPROVEMENT_DIRECTIONS.md`(brief 3-B B2·B5 — 본 에이전트 배정 밖). `Codex/` 무접근. git 명령 무실행. 기존 파일 생성·수정·삭제 0(본 파일 신규 1건).
