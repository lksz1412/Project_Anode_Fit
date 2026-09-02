# R5 — 열역학·통계역학 진보 후보 카탈로그 (v2.0.0 마스터 플랜 작업 챕터 3.1 입력)

> 작성 = 판독·등록부 초안 에이전트 [theory_thermo] (Fable 5.1), 2026-09-03. 지위 = **후보 카탈로그 초안**(실행 없음·문건 무수정). master 가 통합·commit 한다.
> 원천 = `brief.md`(§2 사용자 verbatim·§4 Ground Truth·§5 골격) + 기존 서베이 5본(전문) + 현행 v1.0.25.1 절 12본(배정분 전문) + 보조 정독 8본(부록 상분리·vib·Einstein·LCO Ω·LCO hys 일부·Part T 극한·종합·서지 3본·regsol 인계). 전건 행 범위는 말미 「Read Coverage」.
> 표기 규약 — 등급: **A 필수 / B 강권 / C 선택 / D 기각**. 보유 상태: **있음 / 부분 / 없음** + `파일:행`. 서지 tier: **(V1)** 현행 bib 보유 · **(S)** 기존 서베이가 검증 표기한 승계 서지 · **(N)** 신규 후보 — DOI 는 원천에 적힌 것만 옮기고 그 밖은 "DOI 미검증". 경로는 `D:\Projects\Project_Anode_Fit\Claude\` 기준, `_sections` 는 `docs\v1.0.25.1\_sections\`.
> 이 문건에서 "사용자 결정·지적"으로 적은 것은 brief §2 verbatim 과 원천 문건에 사용자 발화로 기록된 항목뿐이며, 그 밖의 판정은 전부 본 에이전트의 판단이다.

---

## 0. 요지

사용자 기준 5)(최대 일반식을 세우고 레퍼런스가 확실한 가정으로 간소화)를 축으로 열역학·통계역학 후보를 전수 조사한 결과는 다음과 같다. 첫째, 기존 서베이 5본이 제안한 통계역학 심화 후보 SM2-A·B·C 는 brief §4.5 의 "집행 여부 미확정" 표기와 달리 **세 건 모두 v1.0.22 에서 집행되어 현행 문건에 실재**한다(§6 감수율 bgbox·§2.5 앙상블 동등성 bgbox·§2.7 켤레 쌍 bgbox — 근거 행은 §1 표). 둘째, ROADMAP 제안 1(vib Einstein)과 제안 5(PSD 보편형+배제)는 집행됐고, 제안 2(Ω(ξ))·제안 3(Cahn–Hilliard→γ_j)은 미집행이며, IMPROVEMENT 4순위(정칙용액 자유에너지 + 공통접선)와 LIT_ADVANCE 헤드라인(정칙용액+Maxwell ⊗ kinetic)은 **이론은 Part 0·§4·독립 부록에 흩어져 있으나 두-상 dQ/dV 를 실제로 생성하는 사슬(Maxwell 델타 + 단상 꼬리 + 폭 합성)은 문건 어디에도 식으로 닫혀 있지 않고**, v1.0.25 가 regsol 커널을 삭제한 뒤 v1.0.26 재검증이 실행 차단으로 미완이다. 셋째, 현행 Part 0 의 "일반식" 정점은 독립 자리 격자기체 + 평균장 한 단계이며, 그 위에 있어야 할 **일반 격자기체 Hamiltonian(cluster expansion 형식)·다중 부분격자(staging)·비정칙 초과 자유에너지(Redlich–Kister)·일반 포논 DOS·일반 엔트로피 수지** 가 전부 비어 있거나 언급 수준이다 — 기준 5 가 요구하는 "일반→특수" 사다리의 위쪽 절반이 문건에 없다는 뜻이다.

이에 따라 **A 필수 6건**(일반 격자기체 정점·정칙용액+Maxwell 두-상 생성 사슬·Redlich–Kister 비정칙→α 승격·상분리 부록 본문 승격·일반→특수 대조표·기호 통합표), **B 강권 10건**(평균장 감수율 통일·Frumkin 계보 서지·다중 부분격자 staging 일반식·Daumas–Hérold/Safran 배경·CNT/Cahn–Hilliard→γ_j 함수형·Maxwell 관계 2계 항등·세 분포 분리 가정 명시·포논 DOS 일반→Einstein/Debye·일반 엔트로피 수지→Bernardi→소산·Kirchhoff ΔC_p 일반 U(T)), **C 선택 11건**, **D 기각 12건(기존 기각군 전량 승계 + 신규 0)** 으로 정리했다. A·B 16건 중 피팅 파라미터를 늘리는 것은 Redlich–Kister L_1(전이당 +1, α_j 와 축퇴 가드 필요) 하나뿐이고 나머지는 모델 차원 0(설명·재배열·일반식 회수)이다. 가장 침습도가 높은 것은 정칙용액+Maxwell 사슬(§5·§6·§7 재배열)과 부록 승격(기호 배향 ξ↔θ 통일)이다. 결정 대기 항목 12건은 말미 「Decision Queue」에 근거와 기본값을 붙여 두었다.

---

## 1. 기존 서베이 승계 — 집행 완료군·기각군·미집행군 (재조사 0)

기존 서베이 5본을 전문 정독해 각 항목의 **현재 상태**를 현행 문건 실물로 대조했다. 이 표가 승계의 정본이며, 아래 §3 후보는 이 표의 "미집행·부분" 항목과 정독 중 새로 발견한 공백만을 다룬다.

### 1.1 집행 완료군 (재제안 금지 — 현행 문건 실물 확인)

| 서베이 항목 | 원 제안 위치 | 현행 문건 실물 (파일:행) | 판정 |
|---|---|---|---|
| SM2-A 평형 peak = 등온 입자수 감수율 | `SM2_SURVEY.md:62-78` | `ch1_sec06_eqpeak.tex:74-118` bgbox "평형 peak 은 등온 감수율" + 자산 `[V22-SM2-A]` :119 | **집행됨** |
| SM2-B 앙상블 동등성 = 상대 요동 1/√M 소멸 | `SM2_SURVEY.md:80-88` | `ch1_sec02b_part0.tex:387-408` bgbox + 자산 `[V22-SM2-B]` :409 | **집행됨** |
| SM2-C 한 자유에너지의 두 응답(∂_V↔∂_T 켤레) | `SM2_SURVEY.md:90-98` | `ch2_sec07_revheat.tex:74-94` bgbox + 자산 `[V22-SM2-C]` :95 | **집행됨** |
| SM2 축 D annealed/quenched | `SM2_SURVEY.md:47-48` | `ch1_sec07_broadening.tex:142-144` CLT bgbox 문장 | 집행됨 |
| DIRECTION (i)~(iv) (대정준 전하보존·TST·CLT·CNT) | `SM2_SURVEY.md:18-23` | `ch1_sec02b_part0.tex:282-419`·`ch1_sec05_width.tex:46-121`·`ch1_sec07_broadening.tex:130-151`·`ch1_sec04_hys.tex:254-266` | 집행됨 |
| ROADMAP 제안 1 vib Einstein 양자보정 | `ROADMAP_future_physics.md:3,10` | `ch2_sec04_einstein.tex` 전체(eq:Svib-einstein :33-37·eq:dUvib :96-102) | 집행됨 |
| ROADMAP 제안 5 PSD 컨볼루션 — 보편형 + 실조건 배제 | `ROADMAP_future_physics.md:37-41` | `ch1_sec07_broadening.tex:253-304` eq:psdconv·eq:gibbsthomson·수치 배제 | **부분 집행**(보편형·배제만; 나노 확장은 범위 밖 선언) |
| IMPROVEMENT #1 전이 4→5/6 opt-in | `IMPROVEMENT_DIRECTIONS.md:39-44` | `ch1_sec05b_gr2L.tex:151-192` 해상도 사다리 {4·5·6·7} | 집행됨(opt-in) |
| IMPROVEMENT #2 비대칭 폭 | `IMPROVEMENT_DIRECTIONS.md:46-49` | `ch1_sec06_eqpeak.tex:37-72` skew-logistic α_j opt-in(eq:skewpeak·eq:skewapex) | 집행됨 — 단 **양측 폭이 아니라 거듭제곱 재모수화**로 구현(원 제안 w^L≠w^R 와 함수형이 다름) |
| LIT_ADVANCE G4 stage-2L doublet 명시 | `LIT_ADVANCE_SYNTHESIS.md:62` | `ch1_sec05b_gr2L.tex:106-147` | 집행됨 |
| LIT_ADVANCE L1·L2 LCO 3 feature·doublet, per-peak Ω | `LIT_ADVANCE_SYNTHESIS.md:70-71` | `ch1_sec16b_lcoomega.tex:18-57` eq:lcoomega-kernel | 집행됨(단상 곡률 커널 — Maxwell 없음, 아래 §3 TH-2.1 참조) |
| SURV Tier1 #0 Fredholm ratio·Laplace 전달함수 | `SURV_SYNTHESIS.md:11-17` | 부록 E(`ch1_appE_selfconsistent.tex`, brief A14) — 동역학 축 소관 | 집행됨(본 카탈로그 범위 밖) |
| SURV Tier3 cusp 3/2 지수 | `SURV_SYNTHESIS.md:28` | `ch1_sec04_hys.tex:110-111` (T_c−T)^{3/2}·`ch1_sec05b_gr2L.tex:65-73` FWHM λ^{3/2} | 집행됨(각주 수준·Landau 전개 형식화는 §3 TH-8.5) |
| SM2 (v) 단상 w_eff 각주 | `SM2_SURVEY.md:32-35` "보류" | `ch1_sec05b_gr2L.tex:54-83` v1.0.25 정정 — 높이 지표로만 허용·폭 읽기 금지 | **부분 해소**(보류 판정의 우려였던 C-2/C-87 혼동은 "높이/폭 분리"로 처리됨 — `ch2_sec05_mixing.tex:196-203`) |

### 1.2 기각군 (D 승계 — 재조사하지 않는다)

| 기각 항목 | 원 판정 위치 | 승계 사유 |
|---|---|---|
| Wiener–Hopf·WKB·다중척도·중심다양체·Langevin·Preisach 연산자 채택 | `SURV_SYNTHESIS.md:34` | 붙을 문제 부재·Einstein 이미 exact·등온 per-curve·축약 대상 부재·1/√M 벌크 자멸·차원폭발 |
| Kubo 동적 χ(ω) 채택 | `SURV_SYNTHESIS.md:35` | 구동 lag L_V∝|I| ≠ 평형 상관시간 — 형식 유비만(경고 필수) |
| Tikhonov·MaxEnt 역산 | `SURV_SYNTHESIS.md:36` | forward-only 선언과 충돌 — 별도 역문제 문건 |
| SM2 축 C Jarzynski/Crooks 히스 소산 | `SM2_SURVEY.md:44-45` | Part T [C-92] 경계(`ch2_sec05_mixing.tex:230-238`) — 경로의존 정량 범위 밖 |
| IMPROVEMENT #3 최근접 stage 결합 λ_{j,j+1} 피팅 | `IMPROVEMENT_DIRECTIONS.md:31-35,51-53` | 1-D 곡선에서 U_j 이동·w_j 재척도로 흡수 — 식별 불가 |
| G6 전이 6+ 별개 물리 상 증설 | `LIT_ADVANCE_SYNTHESIS.md:64`·`ch1_sec05b_gr2L.tex:171-172` | XRD 미지원 curve-fitting(gallery≠상) |
| G7 DFT 결합에너지를 Ω 로 직접 대입 | `LIT_ADVANCE_SYNTHESIS.md:65` | 면내 bare 는 반발(ordering) — 유효 Ω 는 창발(~2.5RT) |
| L7 diffthermo LCO 파라미터 그대로 | `LIT_ADVANCE_SYNTHESIS.md:76` | O2 폴리타입(우리 O3 아님) — 방법만 |
| L8 double-Gaussian 경험식 | `LIT_ADVANCE_SYNTHESIS.md:77` | 열역학 근거 없음 |
| M6 Bazant/Dreyer PDE 를 dQ/dV 생성기로 | `LIT_ADVANCE_SYNTHESIS.md:97` | 무거운 PDE 회피 — 물리 정당화 인용만(선형 안정성 R(k) 는 부록에 이미 있어 별개) |
| M7 흑연 비대칭 폐형 커널의 "문헌 근거" 주장 | `LIT_ADVANCE_SYNTHESIS.md:98` | 미발표(창시 = 우리 몫) |
| S6 블렌드 역학 결합 | `LIT_ADVANCE_SYNTHESIS.md:87` | 평형 dQ/dV 스코프 밖 — Ch3 Larché–Cahn 시도 절이 이미 공백 GS-1 로 명시(`ch3v22_sec04_mech.tex:4-10`) |

### 1.3 미집행·보류·선검증군 (본 카탈로그가 다시 다루는 것)

| 항목 | 원 위치 | 원 판정 | 현행 상태 | 본 카탈로그 |
|---|---|---|---|---|
| ROADMAP 제안 2 Ω(ξ)=Ω₀+Ω₁(2ξ−1) | `ROADMAP_future_physics.md:18-23` | 차기 후보 1순위 | 미집행 — v1.0.25 는 대신 현상학 α_j 를 채택하며 "물리적 동기는 조성 의존 Ω(x) 류"라 자기 고백(`ch1_sec06_eqpeak.tex:69-71`) | **TH-3.1 (A)** |
| ROADMAP 제안 3 Cahn–Hilliard→γ_j | `ROADMAP_future_physics.md:25-29` | 로드맵(고난이도) | 부분 — CNT 근거 문단만(`ch1_sec04_hys.tex:254-266`), γ_j 현상학 유지 | **TH-5.2 (B)** |
| IMPROVEMENT #4·LIT G3/M1 정칙용액+Maxwell ⊗ kinetic | `IMPROVEMENT_DIRECTIONS.md:55-57,65-68`·`LIT_ADVANCE_SYNTHESIS.md:15-23,100-113` | 4순위 최물리 / ◐선검증 | 부분 — 이론 조각은 있으나 두-상 생성 사슬 미폐합; regsol 커널 v1.0.25 삭제·v1.0.26 재검증 미완(`HANDOVER_regsol_investigation.md:42-45`) | **TH-2.1 (A)** |
| LIT G5 dilute 농도의존 보정(Mercer vs Azizi 상충) | `LIT_ADVANCE_SYNTHESIS.md:63` | ◐선검증 | 없음 | TH-3.2 (C) |
| LIT M4 U_j(T)·ω_j 온도의존 단일셋 | `LIT_ADVANCE_SYNTHESIS.md:95` | ◐선검증 | 부분 — n_j(T) 선택 확장(`ch2_sec05_mixing.tex:57-68`) | TH-2.3 (C) 에 흡수 |
| SM2 축 B staging 상관함수·구조인자 | `SM2_SURVEY.md:41-42` | 범위 밖(집행 비권장) | 없음 | **재개방 후보 TH-4.1~4.3** — 원 판정은 서브 에이전트 판단이며 사용자 결정 기록 아님 → DQ-8 |
| SM2 flow-1 사다리↔결과 1:1 대조표 / flow-3 기호 충돌표 | `SM2_SURVEY.md:50-54` | flow 성(별도 창) | 없음(keybox 참조 목록만 `ch1_sec02b_part0.tex:463-472`; 기호 충돌은 국소 각주 다수) | **TH-9.1·9.2 (A)** — v2.0.0 기준 1·2 에서 필수로 격상 |
| SURV Tier3 Legendre–Fenchel 볼록쌍대 / FPT–Kramers 노트 / Landau cusp 형식화 | `SURV_SYNTHESIS.md:25-31` | 부록 노트 후보 | 없음 | TH-5.5·TH-8.5 (C) |
| Einstein 경화형(ΔC_p<0) 잔여·두-θ 차분형 | `ch2_sec04_einstein.tex:51-58` (문건 자체 "추가 후보") | — | 없음 | **TH-7.2 (B)** |
| Part T 상호작용 엔트로피 ∂Ω/∂T | `ch2_sec05_mixing.tex:193-194` (문건 자체 "범위 밖") | — | 없음 | TH-2.3 (C) |

---

## 2. "일반→특수" 사다리 골격 (열역학·통계역학 축) — 현행 식의 회수 위치

기준 5 를 한 장으로 만들면 아래 사다리가 된다. 각 단은 **일반식 → 가정(레퍼런스) → 회수되는 현행 식(라벨·행)** 의 세 칸으로 적었다. 굵은 단이 현행 문건에 **없는** 단이고, 이것이 §3 후보의 골격 좌표다.

| 단 | 일반식 | 가정(간소화)과 그 레퍼런스 | 회수되는 현행 식 |
|---|---|---|---|
| L0 통계역학 공준 | S=k_B ln W · Gibbs 앙상블 · Ξ(T,μ)=Σ e^{−β(E−μN)} | 등확률·저장조 1차 전개(Hill 1960 (V1)·McQuarrie (V1)) | eq:sm-S·eq:sm-gc (`ch1_sec02a_part0.tex:26-29,75-80`) — **있음** |
| **L1 일반 격자기체 Hamiltonian** | **H=Σ_i ε_i n_i + ½Σ_{ij}J_{ij}n_in_j + Σ_{ijk}… (cluster expansion·ECI)**, n_i∈{0,1} | 점유 변수의 완전 전개(Sanchez–Ducastelle–Gratias 1984 (N)); Ising 동치(Lee–Yang 1952 (N)) | **없음** — LCO 절이 "다체 클러스터 전개의 평균장 축약"이라 언급만(`ch1_sec13_lcohys.tex:147-166`·`ch1_sec16b_lcoomega.tex:63-79`) → TH-1.1 |
| L1′ 내부 자유도 | Ξ_1=1+q(T)e^{−β(ε₀−μ)}, ε̃=ε₀−k_BT ln q | 국소화 흡착 표준(Hill·Fowler–Guggenheim (V1)) | eq:partfn·eq:sm-epstilde·eq:fermifn (`ch1_sec02a_part0.tex:241-288`) — 있음 |
| **L2a 다중 부분격자 평균장** | **g({θ_k})=Σ_k[RT s(θ_k)+Ω_∥θ_k(1−θ_k)]+Σ_{k<l}J_⊥^{kl}θ_kθ_l** (gallery k) | 층별 무작위 혼합 + 층간 결합(Safran 1980 (S)·Cordoba–Chandesris–Plapp 2024 (S)·Guo–Smith–Bazant 2016 (S)) | **없음** — J_⊥→0 이면 독립 클래스곱 eq:sm-mc-factor(`ch1_sec02b_part0.tex:303-316`) 회수 → TH-4.1 |
| **L2b 준화학/CVM** | 쌍 상관 명시 근사(Fowler–Guggenheim (V1)·Kikuchi 1951 (N)) | 무작위 혼합 극한 → 평균장 | **없음** → TH-2.2 (C) |
| L2c 평균장(Bragg–Williams) 정칙용액 | g(ξ)=g⁰+RT[ξlnξ+(1−ξ)ln(1−ξ)]+Ωξ(1−ξ) | 이웃 점유를 평균 θ 로 대체(Bragg–Williams 1934 (N)·Huggins 2009 (V1)·Bazant 2013 (V1)) | eq:sm-mf~eq:gxi (`ch1_sec02b_part0.tex:10-52`)·eq:BW (`ch2_sec01_partition.tex:113-117`) — 있음 |
| **L2d 비정칙 초과 자유에너지** | **g^E=ξ(1−ξ)Σ_k L_k(1−2ξ)^k (Redlich–Kister)** | 초과 자유에너지의 다항 전개(Redlich–Kister 1948 (N)·Hillert 2008 (부록 [A4])) ; k=0 절단 → L2c | **없음** → TH-3.1 (A). α_j skew(`ch1_sec06_eqpeak.tex:42-47`)는 이 단의 현상학적 대리 |
| **L2e 온도 의존 상호작용** | Ω(T)=Ω_H−TΩ_S | 상호작용 엔트로피 무시 → Ω 상수 | **없음**(범위 밖 선언 `ch2_sec05_mixing.tex:193-194`) → TH-2.3 (C) |
| L3a 전기화학 결선 | μ_Li=μ⁰−sF(V−U) | 기준전극 평형·접촉전위 흡수 | eq:sm-emu~eq:sm-eqcond (`ch1_sec02b_part0.tex:143-183`)·eq:eqcond (`ch1_sec03_center.tex:35-39`) — 있음 |
| L3b 단상 등온선(Ω≤2RT) | V_eq(ξ)=U+(RT/F)ln[ξ/(1−ξ)]+(Ω/F)(1−2ξ) 음함수 | 볼록성 유지 | eq:Veq (`ch1_sec04_hys.tex:74-77`)·판정자 eq:gr2l-disc (`ch1_sec05b_gr2L.tex:39-44`)·LCO 커널 eq:lcoomega-kernel (`ch1_sec16b_lcoomega.tex:24-31`) — 있음(세 곳에 같은 곡률식이 따로 있음 → TH-1.2 통일) |
| L3c 이상 극한(Ω→0) | ξ_eq=logistic, w=RT/F | 상호작용 0 | eq:sm-logistic (`ch1_sec02b_part0.tex:190-195`)·eq:xieq (`ch1_sec05_width.tex:282-285`)·eq:eqpeak (`ch1_sec06_eqpeak.tex:22-29`) — 있음 |
| **L3d 두-상(Ω>2RT) 평형 dQ/dV** | **볼록 포락(convex hull)·공통접선 → U*(Maxwell) → ξ(V)=ξ_b^− ‖ 계단 ‖ ξ_b^+ → (dQ/dV)^eq=Q_j(ξ_b^+−ξ_b^−)δ(V−U*)+단상 꼬리** | 계면 무시(부록 §A.2-3, Porter–Easterling [A3]) | **부록에만**(eq:app-ct·eq:app-binodal·eq:app-maxwell `appendix_phase_separation.tex:185-218,372-391`) — 본문은 "델타에 가깝다"(`ch1_sec07_broadening.tex:20-23`) 서술뿐 → TH-2.1 (A)·TH-5.1 (A) |
| L3e spinodal·히스 상한 | g''=0 → ξ_s^±, ΔU^hys | 준안정 가지 과주행 = spinodal 상한(Dreyer 2010/2011 (V1)) | eq:gpp·eq:spinodal·eq:dUhys (`ch1_sec04_hys.tex:27-37,101-106`) — 있음 |
| **L3f 준안정 이탈(핵생성)** | **J=J₀exp(−ΔG*(ξ)/k_BT), ΔG*=16πγ³/(3Δg_v²) → 이탈점 ξ* → γ_j** | 구형 핵·계면 에너지 상수(CNT, Porter–Easterling [A3]·Balluffi [A5]) | 부록 eq:app-cnt·eq:app-rstar (`appendix_phase_separation.tex:411-422`) + 본문 CNT 근거 문단(`ch1_sec04_hys.tex:254-266`) — γ_j 는 현상학(`:246-252`) → TH-5.2 (B) |
| L4 비균일계 | F[ξ]=∫[f(ξ)+κ|∇ξ|²]dV, ∂ξ/∂t=M∇²μ | 구배 벌칙 최저차(Cahn–Hilliard 1958 [A1]·Cahn 1961 [A2]) | 부록 eq:app-ch-F·eq:app-ch-R (`appendix_phase_separation.tex:434-449`) — 부록에만 → TH-5.1 |
| L5a 대정준 일반 요동 항등 | var(N)=k_BT ∂⟨N⟩/∂μ = Σ_{ij}⟨δn_iδn_j⟩ (정적 구조인자 S(q→0)) | 임의 H 에서 성립(McQuarrie (V1)) | 독립 자리 특수형만 eq:sm-flucres·eq:sm-mc-fluc (`ch1_sec02a_part0.tex:306-311`·`ch1_sec02b_part0.tex:361-366`) → TH-1.2 (B) |
| L5b 앙상블 동등성 | √var(N)/⟨N⟩~1/√M | 자리 독립(강상관 창 예외 가드) | SM2-B bgbox (`ch1_sec02b_part0.tex:387-408`) — 있음 |
| L5c 켤레 응답 | ∂_V ↔ ∂_T 한 자유에너지 | 가역 응답 한정 | SM2-C bgbox (`ch2_sec07_revheat.tex:74-94`) — 있음; **2계 Maxwell 관계 미명시** → TH-6.3 (B) |
| **L6a 일반 엔트로피 분해** | **S=−k_B Tr ρ ln ρ ; ρ≈ρ_config⊗ρ_vib⊗ρ_e (약결합 가정)** | 하위계 분리 가능(Landau–Lifshitz vol.5 (N)) | 선언만(`ch2_sec03_vibel.tex:96-102` keybox) → TH-7.1 (B) |
| **L6b 일반 포논 엔트로피** | **S_vib=R∫g(ω)[(1+n)ln(1+n)−n ln n]dω** | DOS 를 델타(Einstein)/ω² 절단(Debye)으로 근사(Einstein 1907·Debye 1912 (N)·Ashcroft–Mermin (V1)) | 모드합 형식 eq:Svib_mode (`ch2_sec03_vibel.tex:23-26`)·Einstein 단일 모드 eq:Svib-einstein (`ch2_sec04_einstein.tex:33-37`) — **Debye 없음·DOS 적분 없음** → TH-7.2 (B) |
| L6c 전자 엔트로피 | S_e=−k_B∫g(E)[f ln f+(1−f)ln(1−f)]dE → Sommerfeld | 축퇴 극한 k_BT≪E_F | eq:Se_start·eq:Se-ch2 (`ch2_sec03_vibel.tex:60-75`) — 있음(고온 코너 경계 `ch2_sec06_limits.tex:26-28`) |
| **L6d 일반 U(T)** | **U(T)=−[ΔH(T_ref)−TΔS(T_ref)+∫ΔC_p dT′−T∫(ΔC_p/T′)dT′]/F** | ΔC_p=0 → 직선 U(T) ; ΔC_p=C_E(θ_E/T) → Einstein 보정 | eq:Uj (`ch1_sec03_center.tex:54-57`)·eq:dUvib (`ch2_sec04_einstein.tex:96-102`) — 두 특수형만, 일반형 없음(Kirchhoff 언급 `:106-108`) → TH-7.5 (B) |
| **L7 일반 엔트로피 수지** | **dS/dt=Ṡ_e+σ, σ=Σ J_iX_i≥0 (de Groot–Mazur (N))** → Bernardi 1985 일반 에너지 수지 (V1) → Rao–Newman 1997 삽입 전극 (N) | 준평형 저율·상변화 열 흡수 → 단일활물질 | eq:qrev (`ch2_sec07_revheat.tex:15-20`) + 두 전제(`:21-25`) — 축약형만; 히스 소산은 "별개" 선언(`ch2_sec05_mixing.tex:230-238`) → TH-7.4 (B) |

---

## 3. 후보 카탈로그 (축별)

각 후보는 **무엇 / 현행 보유 상태 / 사다리 위치 / 새 유도 단계 / 필요 레퍼런스 / 모델 차원·침습도 / 등급·근거 / v2.0.0 배치(brief §5 작업 챕터 4.x 기준·구조 (b) 가정)** 의 순서로 적는다. "새 유도 단계"의 수식 스케치는 본 에이전트가 정독 중 손으로 놓은 것이며 문건 저작 시 SymPy 재검산 대상이다(추정 표기).

### 축 1 — lattice gas · 대정준 (Part 0 의 정점 일반화)

**TH-1.1 일반 격자기체 Hamiltonian(cluster expansion 형식)을 Part 0 정점에 놓기 — [A 필수]**
- 무엇: 자리 점유 변수 n_i∈{0,1} 의 완전 전개 H=Σ_iε_in_i+½Σ_{ij}J_{ij}n_in_j+Σ_{ijk}J_{ijk}n_in_jn_k+… (유효 클러스터 상호작용, ECI) 를 최상위 일반식으로 세우고, 현행 Part 0 의 세 단 — 독립 자리(J≡0), 평균장 정칙용액(최근접 쌍만 + 무작위 혼합), 다클래스 독립곱(클래스 간 J≡0) — 이 이 Hamiltonian 의 어떤 절단·근사인지를 명시 회수한다. Ising 스핀 s_i=2n_i−1 동치(Lee–Yang)로 상분리·질서화가 강자성·반강자성에 대응함을 한 줄로 잇는다.
- 현행 보유: **부분**. 독립 자리·평균장은 있음(`ch1_sec02a_part0.tex:341-355`·`ch1_sec02b_part0.tex:5-31`); 일반 Hamiltonian 은 없음. 클러스터 전개는 LCO 절 srcbox 가 "Van der Ven 다체 클러스터 전개의 최근접 쌍 몫 평균장 축약"으로 언급(`ch1_sec13_lcohys.tex:147-166` eq:br-vanderven1998-1; `ch1_sec16b_lcoomega.tex:63-79` eq:lcoomega-hash7) — 곧 재료 절에서 "위에서 내려온 것"으로 말하면서 Part 0 에 그 "위"가 없다.
- 사다리: L1 → (J_{ijk}=0, 최근접 쌍 J) → (무작위 혼합, 평균장) L2c → (J→0) L3c. 회수 식: eq:sm-factor·eq:sm-mf·eq:sm-omega·eq:sm-mc-factor.
- 새 유도: (i) Ξ=Σ_{n}exp[−β(H−μN)] 를 일반형으로 적고, (ii) 최근접 쌍 절단 후 ⟨n_in_j⟩≈θ² 평균장 대체가 eq:sm-mf 를 주며 Ω≡−(z/2)N_Au 가 J 의 몰 환산임을 보인다(현행 `ch1_sec02b_part0.tex:17-31` 그대로 회수), (iii) 클래스 간 J_⊥ 항을 남기면 TH-4.1 의 다중 부분격자식이 되고 J_⊥→0 에서 eq:sm-mc-factor 로 접힌다는 것을 명시한다(현행 `ch1_sec02b_part0.tex:309-316` 의 "근사 경계 (ii)" 가 이 회수 문장이 된다), (iv) 이 절단이 왜 정당한지의 레퍼런스(ECI 수렴·Persson 2010b (V1) 흑연 클러스터 전개)를 붙인다.
- 레퍼런스: Hill 1960·McQuarrie 1976·Fowler–Guggenheim 1939 (V1); Van der Ven 1998·Persson 2010b (V1); Sanchez–Ducastelle–Gratias, *Physica A* 128, 334 (1984) (N, DOI 미검증); Lee–Yang, *Phys. Rev.* 87, 410 (1952) (N, DOI 미검증); Chandler, *Introduction to Modern Statistical Mechanics* (1987) (N, 교과서).
- 모델 차원 0(설명·회수). 침습도 **중** — Part 0 §2.3~2.5 앞에 소절 1개 신설·keybox 사다리 개정·LCO srcbox 의 "위" 참조를 Part 0 라벨로 교체.
- 등급 A. 근거: 기준 5 가 요구하는 "최대 일반식"이 열역학 축에서 바로 이것이며, 없으면 TH-3.1·TH-4.1 이 매달릴 정점이 없다. 새 물리 없음·bit-exact 무관.
- 배치: 4.1 열역학·통계역학 기초(일반식).

**TH-1.2 대정준 요동 항등의 일반형과 평균장 감수율의 통일 — [B 강권]**
- 무엇: var(N)=k_BT∂⟨N⟩/∂μ 는 임의 H 에서 성립하는 일반 항등이고, 상관이 있으면 var(N)=Σ_{ij}⟨δn_iδn_j⟩(정적 구조인자 S(q→0)) 이다. 평균장에서 ∂θ/∂μ=1/[RT/(θ(1−θ))−2Ω] 이므로 감수율은 **판정자 eq:gr2l-disc 의 역수이자 LCO 커널 eq:lcoomega-kernel 의 분모**이며, Ω→2RT 에서 발산(임계 감수율, Ornstein–Zernike 형)한다. 현재 세 절에 따로 놓인 같은 곡률식을 "감수율 하나"로 묶는다.
- 현행 보유: **부분**. 독립 자리 특수형 eq:sm-flucres(`ch1_sec02a_part0.tex:306-311`)·다클래스 eq:sm-mc-fluc(`ch1_sec02b_part0.tex:361-366`)·SM2-A 항등(`ch1_sec06_eqpeak.tex:74-118`, verifybox (iii) 가 "Ω≠0 이면 근사"라 한정만)·판정자(`ch1_sec05b_gr2L.tex:39-44`)·LCO 커널(`ch1_sec16b_lcoomega.tex:24-31`). 이들을 잇는 식은 없다.
- 사다리: L5a 일반 → 평균장 특수형 → 독립 자리(Ω=0) 특수형.
- 새 유도: (i) 평균장 μ(θ) 를 θ 로 풀어 ∂⟨N⟩/∂μ=M/[RT/(θ(1−θ))−2Ω] (몰 환산), (ii) 이를 SM2-A 항등에 넣으면 (dQ/dV)^eq=(F²/N_ART)·var(N) 이 Ω≠0 에서도 "평균장 var(N)" 으로 정확히 성립함을 보이고 verifybox (iii) 의 "근사" 문구를 "평균장 정확·상관 보정은 S(q) 몫" 으로 정직화, (iii) Ω→2RT^− 발산 = 두-상 델타의 감수율 언어(TH-2.1 과 접속), (iv) 강상관 창의 S(q→0) 발산이 SM2-B 가드(`ch1_sec02b_part0.tex:403-407`)의 정량 표현임을 잇는다.
- 레퍼런스: McQuarrie (V1); Chandler 1987 (N); Callen–Welton, *Phys. Rev.* 83, 34 (1951) (N, DOI 미검증); Kubo, *Rep. Prog. Phys.* 29, 255 (1966) (N, DOI 미검증) — 정적 감수율에 한해 인용(동적 χ(ω) 채택은 D 승계).
- 모델 차원 0. 침습도 **낮음~중** — §2.5 verifybox 확장 1 + §6 bgbox 문장 정정 + §5b·§16b 에 "감수율" 상호참조.
- 등급 B. 근거: 같은 곡률식이 세 곳에 독립 유도돼 있어 기준 1(비약 없는 유도)과 기준 2(교재 일관성)에 직결; 새 물리 0.
- 배치: 4.1(일반 항등) + 4.2(평형 열역학 회수).

**TH-1.3 대정준 퍼텐셜 Ω_GC=−k_BT ln Ξ 와 Legendre 구조의 명시 — [C 선택]**
- 무엇: 현행은 "대정준→정준 Legendre 반전"이라 부르면서(`ch1_sec02b_part0.tex:353-357,390`) 대정준 퍼텐셜 자체와 ⟨N⟩=−∂Ω_GC/∂μ·S=−∂Ω_GC/∂T 를 적지 않는다. 이 한 쌍이 TH-6.3 의 Maxwell 관계와 TH-1.2 의 감수율을 한 퍼텐셜의 1계·2계 미분으로 묶는 형식 골격이다.
- 현행 보유: 없음(명명만). 사다리: L0 의 형식층. 새 유도: 표준 열역학 관계 3줄. 레퍼런스: Callen, *Thermodynamics and an Introduction to Thermostatistics*, 2nd ed. (1985) (N, 교과서). 차원 0·침습 낮음(bgbox 1). 등급 C — 교육 이득은 있으나 결과식 변화 없음; TH-6.3 을 채택하면 그 안에서 자동 도입된다. 배치: 4.1.

**TH-1.4 내부 분배함수 q(T) 의 조성 의존 → Ω 의 엔트로피 몫 — [C 선택]**
- 무엇: 점유 이온의 진동수 ω_i 가 이웃 점유에 의존하면 ε̃ 의 상호작용 몫이 온도 의존을 갖고, 이것이 Ω(T)=Ω_H−TΩ_S 의 미시 기원이다(TH-2.3 의 통계역학 쪽 근거).
- 현행 보유: 없음(`ch1_sec02a_part0.tex:239-260` 은 q(T) 를 자리 독립으로 둠). 사다리: L1′×L2e. 새 유도: q_i(T;{n_j}) 를 최근접 평균으로 전개해 Ω_S∝∂ln q/∂θ 를 보이는 한 문단. 레퍼런스: Hill 1960 (V1). 차원 +0(설명) 또는 +1(Ω_S 피팅). 침습 낮음. 등급 C — 다온도 데이터 없이는 tier C 이며 Part T 가 "범위 밖"으로 명시한 항(`ch2_sec05_mixing.tex:193-194`) — 개방 여부는 DQ-6 과 함께 결정. 배치: 4.4.

### 축 2 — 정칙용액 (Frumkin / Bragg–Williams)

**TH-2.1 정칙용액 + 공통접선(Maxwell) → 두-상 평형 dQ/dV 생성 사슬의 폐합 — [A 필수]**
- 무엇: Ω>2RT 전이의 평형 dQ/dV 를 "델타에 가깝다"는 서술이 아니라 **식**으로 닫는다: 볼록 포락 → Maxwell 전위 U* → 등온선 ξ(V)=ξ_b^−(V<U*)‖ξ_b^+(V>U*) 계단 + 바깥 단상 가지 → (dQ/dV)^eq_j=Q_j(ξ_b^+−ξ_b^−)δ(V−U*)+Q_j·F/[RT/(ξ(1−ξ))−2Ω_j]·𝟙_{ξ∉(ξ_b^−,ξ_b^+)}. 이것이 §7 의 "② 내재 RT/F 폭(plateau 양끝 단상 꼬리)"을 정량화하고(꼬리 무게 2Q_jξ_b^−, 형상은 단상 곡률식), 관측 종 = δ⊗(②꼬리)⊗(③ρ_η)⊗(①kinetic) 의 합성 순서를 폭 예산 eq:widthbudget 에 식으로 연결한다. LIT_ADVANCE 헤드라인(G3/M1)·IMPROVEMENT 4순위·regsol 정정판(Ω>2RT+Maxwell)의 문건 측 정본이다.
- 현행 보유: **부분(조각 분산·사슬 미폐합)**. 정칙용액·문턱: `ch1_sec02b_part0.tex:32-73`; spinodal·gap: `ch1_sec04_hys.tex:20-120`; 공통접선·binodal·Maxwell 등면적: 독립 부록 `appendix_phase_separation.tex:169-226,360-391`(본문 라벨 미연결·독립 컴파일); 두-상 "델타" 서술: `ch1_sec07_broadening.tex:20-32`; 단상 곡률 커널(Maxwell 없음·spinodal 발산): `ch1_sec16b_lcoomega.tex:24-31`; §5b 는 "판정자가 2RT 를 넘는 순간 Maxwell 공존평탄으로 불연속하게 갈아탄다"(`ch1_sec05b_gr2L.tex:78-82`)고 적으나 그 평탄역의 dQ/dV 식은 없다. dQ/dV 생성 커널은 v1.0.25 에서 삭제(brief §4.4 "regsol 은 dQ/dV 커널만 삭제") 후 v1.0.26 skew-regsol 결합 커널 vs GITT 평형 데이터 판정이 실행 차단으로 미완(`HANDOVER_regsol_investigation.md:27-30,42-45`). regsol2 진단값 Ω_j/RT=[4.06,2.02,3.55,4.07](`LIT_ADVANCE_SYNTHESIS.md:106`·`ch1_sec05b_gr2L.tex:85-86`)은 문건에 인용돼 있다.
- 사다리: L2c → L3d(Ω>2RT) / L3b(Ω≤2RT) / L3c(Ω→0). 회수: Ω→0 에서 eq:eqpeak, Ω≤2RT 에서 eq:lcoomega-kernel, Ω→2RT^+ 에서 델타 무게 (ξ_b^+−ξ_b^−)→0 으로 단상 종에 연속 접속(무게는 (T_c−T)^{1/2} 로 소멸 — 추정, 재검산).
- 새 유도: (i) 부록 eq:app-ct·eq:app-maxwell 을 본문 좌표(진행률 ξ=1−θ, 부호 반전)로 옮겨 U*=U_j(대칭 정칙에서 자동) 확인, (ii) 계단 등온선의 미분으로 델타 항 + 단상 가지 미분(TH-1.2 감수율식) 의 합, (iii) ξ_b(Ω/RT) 를 eq:app-binodal 로 수치화해 꼬리 무게·폭 표(Ω/RT=2.5,3,4 예시) — 규범 수치는 저작 시 산출, (iv) 합성 순서 δ⊗②⊗③(⊗①) 을 eq:ensavg·eq:widthbudget 에 접속하고 "두-상 w_j 는 ②⊗③ 합성 폭" 이라는 현행 서술(`ch1_sec07_broadening.tex:173-178`)을 식으로 대체, (v) Dreyer 순차 전환(값=Maxwell·경로=순차, `ch1_sec07_broadening.tex:28-32,68-74`)과의 관계를 "N→∞ 앙상블의 평균 등온선 = 이 계단" 으로 한 문장 연결.
- 레퍼런스: Levi–Aurbach 1999·Dreyer 2010/2011·Bazant 2013·Verbrugge 2017 (V1); Porter–Easterling·Hillert (부록 [A3]·[A4]); Yao–Viswanathan, *JPCL* 15, 1143 (2024) (S — LIT_ADVANCE 검증 표기; 공통접선 미분 관통 방법); Cordoba–Chandesris–Plapp arXiv:2401.13108 (S — Ω_a≈2.5RT 앵커); Frumkin 1925 (N, TH-2.4).
- 모델 차원: 문건 이론으로는 0(Ω_j 는 이미 tab:staging 슬롯 `ch1_sec10_sum.tex:42-51`); 커널로 채택하면 규제 파라미터 δ_j(LIT_ADVANCE 표 B 의 δ_j) 가 붙을 수 있음 — 코드는 non-goal. 침습도 **높음** — §5 이중지위·§6·§7 의 서술 재배열, 부록 승격(TH-5.1)과 동시 수행 필수.
- 등급 A. 근거: (a) `HANDOVER_regsol_investigation.md:12` 에 사용자 발화로 기록된 "두상으로 분리되는 걸 표현하려면 regsol이 들어가야 한다"(그 문서의 규약상 큰따옴표=verbatim)와 doc↔code 모순 지적; (b) LIT_ADVANCE 4 스트림 독립 수렴(`:15-23`); (c) 기준 1·5 — 현행은 델타를 말로만 놓아 유도 사슬에 비약이 있다. 단 R² 이득은 미미(+0.5%p, `LIT_ADVANCE_SYNTHESIS.md:109`)하므로 채택 가치는 파라미터 물리성·일관성이며 이를 문건이 정직하게 적어야 한다.
- 배치: 4.2 평형 열역학(중심·폭·상분리·정칙용액) — Part I 일반 절 + 4.6 흑연 적용에서 Ω_j 값.

**TH-2.2 준화학(quasi-chemical)·CVM 중간 사다리 — [C 선택]**
- 무엇: 무작위 혼합(평균장) 위의 한 단 — 최근접 쌍 상관을 명시하는 준화학 근사(Guggenheim)·Bethe 격자·CVM(Kikuchi)이 T_c 를 평균장보다 낮게 주고 등온선 곡률을 바꾼다. 사다리에서 "왜 평균장이 특수인가"를 보이는 교육 단.
- 현행 보유: 없음. 사다리: L2b. 새 유도: 준화학 등온선 닫힌 꼴(Fowler–Guggenheim 표준형) 1식 + 평균장 회수 극한 + T_c 비교 한 줄(정확값 대비 과대 방향만 서술). 레퍼런스: Fowler–Guggenheim 1939 (V1, 이미 보유); Guggenheim, *Mixtures* (Oxford 1952) (N); Kikuchi, *Phys. Rev.* 81, 988 (1951) (N, DOI 미검증). 차원 0(같은 Ω·z). 침습 낮음(bgbox 1). 등급 C — 흑연 dQ/dV 정량 개선 근거는 미발견(근거 미발견 tier)이며, 기준 5 의 사다리 완결성만 이득. 배치: 4.1.

**TH-2.3 상호작용의 온도 의존 Ω(T)=Ω_H−TΩ_S 와 M4(U_j(T)·ω_j 단일셋) — [C 선택]**
- 무엇: 정칙 가정 "Ω 상수"를 초과 자유에너지 g^E(ξ,T) 일반형에서 회수하는 단. ∂Ω/∂T 는 ∂U_oc/∂T 에 (1−2ξ)Ω_S/F 몫을 더한다.
- 현행 보유: 없음 — 명시 배제(`ch2_sec05_mixing.tex:193-194` "2차 항 … 본 장 범위 밖"); n_j(T) 선택 확장(`:57-68`)이 폭의 잔여 T-의존만 담음. 사다리: L2e. 새 유도: g^E=ξ(1−ξ)(Ω_H−TΩ_S) → μ, ∂μ/∂T 의 추가 항 → eq:dxidT 에 세 번째 조각 → 종합식 eq:complete 에 전파. 레퍼런스: Hillert 2008 ([A4]); Paul 2024 *JES* 171, 103505 (V1 msmr_partII — ω_j(T) 실측). 차원 +1/전이(Ω_S). 침습 중(Part T 파생 A·종합식). 등급 C — 다온도 데이터(Task #38, Non-goal) 없이는 tier C; LIT_ADVANCE M4 ◐ 판정 승계. 배치: 4.4(열특성) 각주/opt-in. DQ-6 연동.

**TH-2.4 Frumkin 등온선 원전·계보 서지 정리 — [B 강권]**
- 무엇: "우리 ξ_eq 는 g=0 Frumkin 등온선"이라는 문헌 정합(`LIT_ADVANCE_SYNTHESIS.md:20`)을 리뷰급 서지로 닫는다 — Langmuir 1918 → Frumkin 1925 → Fowler–Guggenheim 1939 → McKinnon–Haering 1983 → Levi–Aurbach 1999 → Verbrugge 2017(MSMR ω) 의 계보를 srcbox 1개로.
- 현행 보유: 부분 — McKinnon–Haering·Levi–Aurbach·Verbrugge 는 있음(`ch1_sec02a_part0.tex:162-186`·`ch1v22_bib.tex:16,24,49`); Frumkin·Langmuir 원전 없음. 새 유도 없음(서지). 레퍼런스: Langmuir, *JACS* 40, 1361 (1918) (N, DOI 미검증); Frumkin, *Z. Phys. Chem.* 116, 466 (1925) (N, DOI 없음/미검증). 차원 0·침습 낮음. 등급 B — 기준 3(리뷰급 레퍼런스). 배치: 4.2 + 작업 챕터 5.

### 축 3 — Ω(ξ) · Redlich–Kister 비정칙

**TH-3.1 Redlich–Kister 초과 자유에너지 → 비대칭 등온선·spinodal·gap 일반화, α_j 의 열역학 승격 — [A 필수]**
- 무엇: g^E(ξ)=ξ(1−ξ)[L_0+L_1(1−2ξ)+L_2(1−2ξ)²+…] 를 일반식으로 두고 k≤1 절단(subregular)에서 (i) μ=g′ 의 새 항 L_1(1−6ξ+6ξ²), (ii) 등온선 V_eq(ξ) 비대칭, (iii) g″=RT/[ξ(1−ξ)]−2L_0+6L_1(2ξ−1)=0 의 근이 ξ≠½ 로 이동(3차 방정식, 두 spinodal 비대칭), (iv) ΔU^hys 의 비대칭 일반화(eq:dUhys 는 L_1=0 회수), (v) 공통접선이 수평이 아니게 되어 U*≠U_j (Maxwell 전위 이동), (vi) 이상 극한(L_0=L_1=0)에서 로지스틱 회수. 이어 현행 α_j skew(eq:skewpeak)의 정점 이동 σ_dw_j ln α_j 와 L_1 이 주는 정점 이동을 1차에서 대응시켜 **α_j 를 tier C 현상학에서 L_1 의 근사 표현으로 회수**한다(ROADMAP 제안 2 의 복귀).
- 현행 보유: **없음** — ROADMAP 로드맵 상태(`ROADMAP_future_physics.md:18-23`); v1.0.25 는 α_j 를 채택하며 "물리적 동기는 order–disorder 엔트로피 스텝·조성 의존 Ω(x) 류"(`ch1_sec06_eqpeak.tex:69-71`)라 적어 이 단의 부재를 자인; α_j 는 w_j·L_V 와 식별 축퇴(`ch1_sec06_eqpeak.tex:64-66`·`ch1_sec07_broadening.tex:239-242`).
- 사다리: L2d → (L_1=0) L2c → (Ω=0) L3c. 회수 식: eq:gxi·eq:Veq·eq:spinodal·eq:dUhys·eq:eqpeak.
- 새 유도: 위 (i)~(vi) 여섯 단계 — 전부 초등 대수·3차 근(닫힌 꼴 가능). 추가로 (vii) L_1 의 물리 기원 두 갈래를 srcbox 로: 흑연 = 층간 staging 질서의 조성 비대칭(TH-4.1 과 접속), LCO = Li·빈자리 정렬(x=½ 비국소, ROADMAP 제안 2 문제 (ii)); (viii) 식별 가드 — α_j 와 L_1 동시 자유화 금지(§18 입력 가드 갱신).
- 레퍼런스: Redlich–Kister, *Ind. Eng. Chem.* 40, 345 (1948) (N, DOI 미검증); Hillert 2008 ([A4]); Lukas–Fries–Sundman, *Computational Thermodynamics: The Calphad Method* (2007) (N, 교과서); Yao–Viswanathan 2024 (S — RK 초과항 + 음함수 미분 관통 방법의 근접 선례); Zhu 2023 *Adv. Mater.* adma.202304666 (S — 양측 폭 일반화 로지스틱, 현상학 대조); Reynier 2004 (V1 — LCO order–disorder 엔트로피 스텝); Van der Ven 1998 (V1).
- 모델 차원 **+1/전이(L_1)** — 단 α_j 를 대체하면 순증 0. 침습도 **높음** — Part 0 §2.4 확장·§4 spinodal/gap 일반화(opt-in 분기)·§6 skew 절의 지위 개정·§18 식별 가드.
- 등급 A. 근거: 열역학 축에서 "평형 비대칭"의 유일한 레퍼런스 확실한 일반식이며, 기준 5(일반식→가정 절단)와 F-계열 tier 승격 요구를 동시에 만족. ROADMAP 이 "차기 후보 1순위"로 지정한 항목. 위험 = ROADMAP 이 적은 "회귀 재정초 위험"(`:22`) — v2.0.0 이 새 폴더라 bit-exact 제약이 완화되나 코드 non-goal 이므로 문건은 opt-in 분기로 적는다.
- 배치: 4.2(일반) + 4.5(히스 일반화) + 4.6/4.7 적용.

**TH-3.2 dilute 극한 농도 의존 보정(G5) — [C 선택]**
- 무엇: 1′→4 희박 영역의 비선형(Mercer 2019 (V1 occupation2019)) vs 상수(Azizi 2025, LIT 서지 raw) 상충 미해소 → 하드코딩 금지 승계. 현행: 없음(§7 은 dilute 를 고용체로 분류만 `ch1_sec07_broadening.tex:13-19`). 사다리: L2d 의 희박 극한 특수형. 차원 +1. 등급 C — LIT G5 ◐ 판정 승계·상충 해소 전 문건은 "공백" 표기. 배치: 4.6 warnbox.

**TH-3.3 DFT 결합에너지 → Ω 직접 대입 — [D 기각 승계]** (`LIT_ADVANCE_SYNTHESIS.md:65`). 단 TH-1.1 의 srcbox 에서 "bare J 와 유효 Ω 의 차이(창발)"를 한 문장으로 설명하는 데는 쓴다.

### 축 4 — sublattice · staging (Daumas–Hérold · Safran · transfer matrix)

**TH-4.1 다중 부분격자 정칙용액 → staging 자유에너지 일반식 — [B 강권]**
- 무엇: gallery k 마다 점유 θ_k, 층내 Ω_∥, 층간 결합 J_⊥ 를 갖는 g({θ_k})=Σ_k[RT s(θ_k)+Ω_∥θ_k(1−θ_k)]+Σ_{k<l}J_⊥^{kl}θ_kθ_l 를 세우고, (i) J_⊥→0 에서 현행 다클래스 독립곱(eq:sm-mc-factor)이 회수되며 (ii) J_⊥≠0 의 Hessian 안정성이 θ_1≠θ_2 의 stage-2 질서 분기를 주고 (iii) 순차 채움의 전이 중심 간격 U_j−U_{j+1} 이 J_⊥ 로 결정됨(현행은 U_j 가 입력)을 보인다. "왜 staging 은 비등간격인가"(ROADMAP 제안 2 문제 (i))의 열역학 답.
- 현행 보유: **부분(언급만)** — `ch1_sec05b_gr2L.tex:95-104` srcbox "단일 Ω_j 는 다중-부분격자 staging 질서의 평균장 축약 … 전이별 면내·층간 Ω 분해는 회사 피팅 단계로 위임"; `ch1_sec02b_part0.tex:314-316` "클래스 사이의 상관 — staging 결합 — 은 이 곱에서 빠진다". 식은 없다.
- 사다리: L1 → L2a → (J_⊥→0) L2c 다클래스. 회수: eq:sm-mc-factor·eq:sm-mc-occ·eq:sm-mc-balance.
- 새 유도: 2-부분격자 최소 모형에서 (i) μ_k=∂g/∂θ_k 두 식·공통 μ 조건, (ii) 대칭해 θ_1=θ_2 의 안정성 조건 det H>0 → J_⊥ 문턱, (iii) 비대칭해(stage-2)로의 분기와 그 전위, (iv) N 층 일반화의 개요(Safran 장거리 형식은 배경 박스 TH-4.2 로 넘김). **피팅 파라미터화는 하지 않는다**(IMPROVEMENT #3 의 식별 불가 판정 D 승계) — 이 후보는 "U_j 간격의 열역학 기원" 설명·회수용이다.
- 레퍼런스: Safran, *PRL* 44, 937 (1980) (S — IMPROVEMENT 부록 서지; DOI 미검증); Cordoba–Chandesris–Plapp 2024 (S); Guo–Smith–Bazant, *JPCL* 7 (2016) (S — IMPROVEMENT 서지, DOI 미검증); Dahn 1991·Persson 2010b (V1); Chandesris–Caliste–Jamet–Pochet, *J. Phys. Chem. C* 123 (2019) "staging 열역학·동역학" (N, DOI 미검증); Derosa–Balbuena, *JES* 146, 3630 (1999) 흑연 격자기체 (N, DOI 미검증); Gavilán-Arriazu–Mercer–Hoster–Leiva 계열 흑연 GCMC (N, 서지 미검증).
- 모델 차원 0(설명; 피팅 확장은 D). 침습도 **중** — Part 0 신설 소절 1 + §5b srcbox 대체 + §2.5 근사 경계 (ii) 를 회수 문장으로.
- 등급 B. 근거: 흑연 물리의 정체(staging = 층간 결합 현상, `IMPROVEMENT_DIRECTIONS.md:25-29` 이 "물리적으로 옳다"고 확인)를 일반식 층에 두는 것이 기준 5 의 요구이며, 현행은 자기 축약을 고백만 하고 상위식을 보이지 않는다. A 가 아닌 이유: dQ/dV 결과식은 바뀌지 않고(설명층) 데이터 판정 근거가 없다. SM2 축 B 의 "범위 밖" 판정과 충돌 → DQ-8.
- 배치: 4.1(일반) + 4.6 흑연 적용(U_j 간격 해석).

**TH-4.2 Daumas–Hérold 도메인 모형·Safran 층간 상호작용 배경 박스 — [B 강권, TH-4.1 에 흡수 가능]**
- 무엇: staging 의 미시 기원(층간 정전·탄성 장거리 반발, 도메인 교대 충전)을 리뷰급 배경 bgbox 로 정리하고, 왜 평균장 단일 Ω_j 로 내려오는지의 가정 사슬을 명시. 현행: 언급 1건(`ch1_sec05b_gr2L.tex:98` "Daumas–Hérold 교대충전" + persson2010b 인용). 새 유도: 없음(개념·형식 개요). 레퍼런스: Daumas–Hérold, *C. R. Acad. Sci. Paris C* 268, 373 (1969) (N, DOI 없음·미검증); Safran 1980 (S); Safran–Hamann *PRL* 42, 1410 (1979) (N, DOI 미검증); Kirczenow, *PRL* 55, 2810 (1985) 도메인 모형 (N, DOI 미검증); Dresselhaus–Dresselhaus, *Adv. Phys.* 30, 139 (1981) 리뷰 (N, DOI 미검증). 차원 0·침습 낮음. 등급 B(서지·기준 3). 배치: 4.6.

**TH-4.3 transfer matrix — 층간 1D 사슬의 정확 해와 평균장의 필요성 — [C 선택]**
- 무엇: 층간 결합만 남긴 1D Ising 사슬 Z=Tr T^N(Kramers–Wannier)로 정확 자유에너지·상관 길이를 닫고, 1D 에서는 유한 T 장거리 질서가 없으므로 실제 staging 질서는 면내 2D 응축+층간 결합(Daumas–Hérold 도메인)이 필요함을 보이는 교육 박스 — 사다리에서 "정확 해가 있는 특수 극한"의 자리.
- 현행 보유: 없음. 사다리: L1 의 1D 정확 해 갈래. 새 유도: T 행렬 2×2 고유값 λ_± 1식·상관 길이 1식. 레퍼런스: Kramers–Wannier, *Phys. Rev.* 60, 252 (1941) (N, DOI 미검증); Baxter, *Exactly Solved Models in Statistical Mechanics* (1982) (N, 교과서). 차원 0·침습 낮음(bgbox 1). 등급 C — 교육 이득 중·결과식 무관; SM2 축 B 스코프 판정(DQ-8) 종속. 배치: 4.1 bgbox.

### 축 5 — Cahn–Hilliard / phase-field (부록 승격)

**TH-5.1 독립 부록 「상분리의 열역학」의 Part I 본문 승격 — [A 필수]**
- 무엇: `appendix_phase_separation.tex`(497줄; 혼합 자유에너지→현의 기하→공통접선·binodal→spinodal→Maxwell→핵생성 vs spinodal 분해→본문 연결)를 v2.0.0 Part I 평형 열역학 절의 정본으로 편입한다. 현행은 (a) 독립 컴파일 문서라 본문 라벨을 못 쓰고(`:10`), (b) 기호 배향이 본문과 반대(부록 ξ=점유=본문 θ, `:8-9,57-63`), (c) spinodal 식이 본문 §4 와 중복(`:246-252` vs `ch1_sec04_hys.tex:33-37`), (d) 본문 §4.3 이 부록을 "독립 문서"라 지칭(`ch1_sec04_hys.tex:254-255`).
- 현행 보유: **있음(부록)·본문 미연결**. 사다리: L3d·L3f·L4 전부 이 부록에 있음.
- 새 유도: 없음(전부 있음). 새 작업 = 기호 배향 통일(ξ↔θ, 1계 미분 부호 반전 처리)·라벨 A.x→본문 번호·정본 1곳 원칙(spinodal 은 §4 또는 승격 절 중 한 곳만)·그림 fig:app-tangent·fig:app-phasediag 편입·[A1]~[A5] 서지를 V1 원장에 등재(Cahn–Hilliard 1958 DOI 10.1063/1.1744102·Cahn 1961 DOI 10.1016/0001-6160(61)90182-1 은 부록에 기재됨).
- 레퍼런스: 부록 [A1]~[A5] 그대로(Cahn–Hilliard 1958; Cahn 1961; Porter–Easterling 1992; Hillert 2008; Balluffi–Allen–Carter 2005).
- 모델 차원 0. 침습도 **높음(구조)** — 새 절 1개(약 500줄)·기호 대량 치환·xr.
- 등급 A. 근거: 구조 결정 3.3(b)(Part I 일반 이론)와 기준 2(교재 형식)에서 상분리 열역학은 필수 절이며 TH-2.1·TH-5.2 가 이 절의 식에 매달린다. ROADMAP 제안 3 의 "부록→본문 승격"(`:26,28`) 그대로.
- 배치: 4.2.

**TH-5.2 CNT + Cahn–Hilliard 선형 성장률 → γ_j 의 함수형 유도 — [B 강권]**
- 무엇: 준안정 가지 위에서 접선 구동력 Δg_v(ξ) 를 정칙용액 식으로 닫고 ΔG*(ξ)=16πγ³/(3Δg_v²) → 핵생성률 J(ξ)=J₀exp(−ΔG*/k_BT) → 소인 중 이탈 조건 J(ξ*)·τ_sweep~1 → γ_j=[V_eq(ξ*)−U_j]/[½ΔU_j^hys] 의 **함수형**을 얻는다(γ[J/m²]·J₀ 는 tier C 상수로 남음). spinodal 안쪽에서는 R(k_m) 이 이탈 시간척도를 준다. ROADMAP 제안 3 의 문건 측 정본.
- 현행 보유: **부분** — CNT 근거 문단(`ch1_sec04_hys.tex:254-266`, "CNT 는 γ_j 의 근거이지 예측식이 아니다")·부록 eq:app-cnt·eq:app-rstar·eq:app-ch-R(`appendix_phase_separation.tex:411-449`). γ_j∈[0,1] 는 현상학(`ch1_sec04_hys.tex:246-252`).
- 사다리: L3e(spinodal 상한 γ_j=1) ← L3f(핵생성 이탈 γ_j<1) ← L4(CH 성장률). 회수: J₀→0(핵생성 억제) 에서 γ_j→1 spinodal 상한 eq:Ubranch.
- 새 유도: (i) Δg_v(ξ;Ω) 닫힌 꼴(부록 `:405-407` 정의에 eq:gxi 대입), (ii) ΔG*(ξ) 와 binodal 근방 발산, (iii) 이탈 조건과 γ_j 의 스캔율·온도 의존 함수형, (iv) Dreyer 다입자 그림에서 "최초 이탈 입자"가 앙상블 gap 을 정한다는 연결(`ch1_sec07_broadening.tex:92-100` srcbox 확장). 동역학 축과의 경계: 열역학 축은 ΔG*(ξ) 함수형까지, 이탈 시점(율속 의존)은 동역학 축 — DQ-11.
- 레퍼런스: Cahn–Hilliard 1958·Cahn 1961·Porter–Easterling·Balluffi ([A1][A2][A3][A5]); Dreyer 2010/2011·Cogswell–Bazant 2012 (V1); Bai–Cogswell–Bazant, *Nano Lett.* 11, 4890 (2011) 상분리 억제 (N, DOI 미검증); Turnbull–Fisher, *J. Chem. Phys.* 17, 71 (1949) 응축계 핵생성률 (N, DOI 미검증).
- 모델 차원: 0(함수형) 또는 −1(γ_j 를 γ·J₀ 로 대체 시 재모수화). 침습도 **중** — §4.3 확장 + 부록 승격 절 접속.
- 등급 B. 근거: γ_j 현상학 제거 = 예측력(ROADMAP `:27`); 그러나 γ·J₀ 미지·데이터 부재로 함수형까지가 정직한 상한 → A 가 아님.
- 배치: 4.5 히스테리시스.

**TH-5.3 Bazant/Dreyer PDE 를 dQ/dV 생성기로 — [D 기각 승계]** (`LIT_ADVANCE_SYNTHESIS.md:97`·`SURV_SYNTHESIS.md`). 선형 안정성 R(k) 와 균일 극한 회수는 TH-5.1/5.2 안에서 허용.

**TH-5.4 PSD·Gibbs–Thomson 나노 확장 — [C 선택·현행 유지]** 현행 보편형+배제(`ch1_sec07_broadening.tex:253-304`)를 승계하고 나노 영역은 Non-goal warnbox 로 남긴다. 유한 크기 spinodal 축소(Burch–Bazant, *Nano Lett.* 9, 3795 (2009) (N, DOI 미검증))는 서지 노트만. 배치: 4.2 warnbox.

**TH-5.5 Legendre–Fenchel 볼록 포락 = 공통접선의 일반 형식 — [C 선택]** SURV Tier3 승계. 공통접선·Maxwell 등면적을 "볼록 포락(convex envelope) g**=g 의 이중 켤레" 로 한 줄 일반화하는 bgbox — TH-2.1 의 일반식 층. 레퍼런스: Rockafellar, *Convex Analysis* (1970) (N, 교과서); Callen 1985 (N). 차원 0·침습 낮음. 배치: 4.2 bgbox.

### 축 6 — 요동–응답 (SM2-A/B/C) · 앙상블 동등성

**TH-6.1~6.2 SM2-A·SM2-B — 집행됨, 승계.** 일반화는 TH-1.2. 근거 행은 §1.1 표.

**TH-6.3 Maxwell 관계(2계 혼합 미분)의 명시 — 전하 감수율의 온도 미분 = 엔트로피 계수의 전위 미분 — [B 강권]**
- 무엇: SM2-C 가 세운 켤레 쌍(∂_V↔∂_T)을 한 단 올려 ∂/∂T(∂ξ/∂V)|_V=∂/∂V(∂ξ/∂T)|_T 의 적분 가능 조건을 명시한다. 이것은 Part T 파생 A 가 eq:gj(∂ξ/∂U|_T)와 eq:dxidT(∂ξ/∂T|_U)를 연쇄율로 쓸 때 암묵적으로 전제한 항등이며, 검증 가능한 실측 항등(dQ/dV 곡선의 온도 미분 ↔ 엔트로피 계수 곡선의 전위 미분)으로 제시할 수 있다.
- 현행 보유: **없음(암묵)** — SM2-C bgbox(`ch2_sec07_revheat.tex:74-94`)는 1계 쌍만; eq:gj·eq:dxidT(`ch2_sec05_mixing.tex:38-54`)는 각각 유도.
- 사다리: L5c 의 2계. 새 유도: 대정준 퍼텐셜(TH-1.3)에서 ∂²Ω_GC/∂μ∂T 대칭 → 결선 → 위 항등 1식 + 로지스틱 특수형 검산(양변 닫힌 꼴 일치). 레퍼런스: Callen 1985 (N). 차원 0·침습 낮음(bgbox 1). 등급 B — 기준 1(연쇄율의 전제 명시)·자기검증 가능. 배치: 4.4.

**TH-6.4 Jarzynski/Crooks — [D 승계]**, **TH-6.5 Kubo χ(ω) 채택 — [D 승계·경고 유지]**, **TH-6.6 Langevin — [D 승계]** (§1.2).

### 축 7 — 엔트로피 분해(config · vib Einstein/Debye · 전자) · 가역 발열

**TH-7.1 일반 Gibbs 엔트로피에서 세 분포 합으로 — 분리 가정의 명시 — [B 강권]**
- 무엇: S=−k_B Tr ρ ln ρ 에서 ρ≈ρ_config⊗ρ_vib⊗ρ_e(하위계 약결합·단열 분리)일 때만 S=S_config+S_vib+S_e 가 성립함을 명시하고, 결합이 남는 경우(전자–포논, 점유–진동수 = TH-1.4)가 어디로 가는지(중심값 흡수·δS 잔차) 를 사다리로 적는다.
- 현행 보유: **선언만** — `ch2_sec03_vibel.tex:96-102` keybox "세 분포가 한 전극의 엔트로피를 이룬다"; 분해식 `ch2_sec02_config.tex:112-132` warnbox. 가정 명시 없음.
- 사다리: L6a → (분리) 현행 3항 합. 새 유도: 곱 상태의 엔트로피 가법성 2줄 + 결합 잔차의 정의 1줄. 레퍼런스: Landau–Lifshitz, *Statistical Physics Part 1* (N, 교과서); McQuarrie (V1). 차원 0·침습 낮음. 등급 B — 기준 5(가정 명시). 배치: 4.4.

**TH-7.2 일반 포논 DOS 적분 → Einstein·Debye 특수화 + 경화형 잔여·두-θ 차분형 — [B 강권]**
- 무엇: S_vib=R∫g(ω)s(ω/T)dω 를 일반식으로 두고, g(ω)=δ(ω−ω_E)(Einstein, 현행)·g∝ω² 절단(Debye, 음향 모드; 흑연 층간 저주파 모드에 물리적으로 더 적합)·실측/제일원리 DOS(Haruyama 2021 (V1)) 의 세 특수화를 놓는다. 이어 문건 자신이 "추가 후보"로 남긴 (a) 경화형 ΔC_p<0 잔여를 담는 부호 있는 진폭, (b) 생성/반응 두-θ_E 차분형(`ch2_sec04_einstein.tex:51-58`)을 일반식 안에서 닫는다.
- 현행 보유: **부분** — 모드합 형식(`ch2_sec03_vibel.tex:23-29`)·Einstein 닫힌 꼴(`ch2_sec04_einstein.tex:33-49`)·round-trip eq:dUvib(`:96-102`)·3온도점 식별(`:112-125`). Debye 없음(grep 0건)·DOS 적분 없음.
- 사다리: L6b → Einstein/Debye. 회수: 고전 극한 R[1+ln(T/θ_E)] (`:38-42`)·저온 동결.
- 새 유도: (i) DOS 적분식과 두 특수화의 닫힌 꼴(Debye 함수 D(θ_D/T) — 저작 시 재검산), (ii) 두-θ 차분형 ΔS_vib=S_vib(T;θ_E^{prod})−S_vib(T;θ_E^{react}) 와 그 부호, (iii) round-trip eq:dUvib 가 두 특수화에 그대로 적용됨(ΔF_vib 만 교체)을 확인, (iv) 식별 3온도점 논리의 Debye 판.
- 레퍼런스: Einstein, *Ann. Phys.* 22, 180 (1907) (N, DOI 미검증); Debye, *Ann. Phys.* 39, 789 (1912) (N, DOI 미검증); Ashcroft–Mermin (V1); Haruyama 2021 jpcc2021 (V1); Reynier 2003 (V1).
- 모델 차원 0(일반식) / +1(두-θ 시 θ_E 하나 추가) — opt-in. 침습 중(§2.4 확장). 등급 B — 문건 자기 명시 후보 + 기준 5; 다온도 데이터 없이는 파라미터 tier C(warnbox). 배치: 4.4. DQ-5.

**TH-7.3 전자 엔트로피 비축퇴 극한 서술 — [C 선택]** 현행 Sommerfeld(`ch2_sec03_vibel.tex:64-75`)와 고온 코너 경계(`ch2_sec06_limits.tex:26-28`)를 승계하고, 일반 FD 적분 eq:Se_start 에서 축퇴 조건이 어디서 들어가는지 한 문단 명시. 차원 0·침습 낮음. 배치: 4.4.

**TH-7.4 일반 엔트로피 수지 → Bernardi → 삽입 전극 → 단일활물질, 히스 소산의 위치 — [B 강권]**
- 무엇: 비평형 열역학의 국소 엔트로피 수지 ρ ds/dt=−∇·J_s+σ, σ=Σ_iJ_iX_i≥0(de Groot–Mazur) 를 일반식으로 세우고 Bernardi 1985 일반 에너지 수지·Rao–Newman 1997 삽입 전극 수지를 거쳐 현행 단일활물질 축약 eq:qrev 를 회수한다. 소산 함수 σ 에 (i) 반응 과전압 I(U_oc−V)/T, (ii) 확산·혼합(고율 부활 항), (iii) **히스 소산 — U_oc 를 분기 평균 eq:hys_rev 로 정의하면 사이클당 ∮(V−U_oc^rev)dQ≈Q_cycle·ΔU^hys 가 같은 σ 의 항**임을 보여 Part T [C-92] 의 "별개" 선언을 "같은 수지의 다른 항" 으로 정직화한다. brief §5 4.4 "entropy production" 항목의 정본.
- 현행 보유: **부분** — eq:qrev + 두 전제 소거(`ch2_sec07_revheat.tex:15-45`); 히스 소산 "별개"(`ch2_sec05_mixing.tex:230-238`); 반응 vs 활성화 엔트로피 경계(`ch2_sec03_vibel.tex:104-109`).
- 사다리: L7 → Bernardi → 단일활물질. 회수: eq:qrev·eq:hys_rev.
- 새 유도: (i) σ 의 삽입 전극 특수형 3항, (ii) 준평형 저율에서 (ii)항 소거 조건의 정량(Thomas–Newman 혼합열), (iii) 히스 사이클 적분과 eq:hys_rev 의 관계 1식(선형화 근사 `ch2_sec05_mixing.tex:224-229` 그대로), (iv) 가역/비가역 분리가 σ≥0 에서 어떻게 보장되는지.
- 레퍼런스: Bernardi 1985·Newman 2004 (V1); de Groot–Mazur, *Non-Equilibrium Thermodynamics* (Dover 1984) (N, 교과서); Rao–Newman, *JES* 144, 2697 (1997) (N, DOI 미검증); Thomas–Newman, *J. Power Sources* 119–121, 844 (2003) 혼합열 (N, DOI 미검증); Latz–Zausch, *J. Power Sources* 196, 3296 (2011) 열역학 정합 수송 (N, DOI 미검증); Zilberman 2018 hysteresis2018 (V1).
- 모델 차원 0. 침습 중(§2.7 확장 + Part T 파생 D warnbox 문구 개정). 등급 B — 기준 5·열 축 일반식; A 가 아닌 이유는 결과식(eq:qrev·종합식)이 불변. 배치: 4.4. DQ-6(C-92 경계 개정).

**TH-7.5 Kirchhoff ΔC_p 를 포함한 일반 U(T) — eq:Uj 와 Einstein 보정의 공통 상위식 — [B 강권]**
- 무엇: ΔG(T)=ΔH(T_ref)−TΔS(T_ref)+∫_{T_ref}^TΔC_p dT′−T∫_{T_ref}^T(ΔC_p/T′)dT′ 에서 U(T)=−ΔG/F 를 세우면 ∂U/∂T=ΔS(T)/F 가 임의 ΔC_p 에서 정확히 성립하고(현행 `ch2_sec04_einstein.tex:106-108` 의 언급), ΔC_p=0 이면 eq:Uj 의 직선, ΔC_p=C_E(θ_E/T) 이면 eq:dUvib 가 그대로 회수된다. 두 특수형이 한 일반식의 절단임을 보이는 단.
- 현행 보유: 부분(두 특수형 + 언급). 사다리: L6d. 새 유도: 위 2식 + 두 회수 검산(SymPy). 레퍼런스: Newman 2004 (V1); 표준 열역학(무인용 관용 또는 Callen). 차원 0·침습 낮음(§3 확장 문단 + §2.4 상호참조). 등급 B — 기준 1·5. 배치: 4.2(중심) + 4.4.

**TH-7.6 config 부분몰 엔트로피·이중계산 금지 — 있음, 승계.** (`ch2_sec02_config.tex:14-45,112-132`)

### 축 8 — 상분리 (binodal / spinodal / Maxwell / CNT)

**TH-8.1 binodal·Maxwell·CNT 본문화 — TH-5.1 과 동일 항목(중복 계상 않음).**

**TH-8.2 비대칭(L_1≠0) 하의 binodal·spinodal·Maxwell 일반화 — TH-3.1 의 따름(등급 종속).** 공통접선 비수평·등면적 비대칭·U*≠U_j.

**TH-8.3 유한 크기 miscibility gap 축소 — [D, Non-goal]** 나노 한정(brief §6·`ch1_sec07_broadening.tex:298-301`). 서지 노트만(TH-5.4).

**TH-8.4 Dreyer 다입자 순차 전환 — 있음(`ch1_sec07_broadening.tex:68-101`), 승계.** 일반화 연결은 TH-2.1 (v)·TH-5.2 (iv).

**TH-8.5 Landau 전개로 cusp 3/2 두 결과의 통일 — [C 선택]**
- 무엇: f=a(T−T_c)η²+bη⁴ 형 Landau 전개에서 gap∝(T_c−T)^{3/2}(`ch1_sec04_hys.tex:110-111`)와 단상 FWHM∝λ^{3/2}(`ch1_sec05b_gr2L.tex:65-73`)가 같은 평균장 지수의 두 얼굴임을 bgbox 로 닫는다(SURV Tier3 승계; RG caveat 1줄). 레퍼런스: Landau–Lifshitz vol.5 (N). 차원 0·침습 낮음. 등급 C. 배치: 4.2 bgbox.

**TH-8.6 Preisach — [D 승계]**; 명명 노트 각주만 C(SURV Tier3).

### 축 9 — 구조·형식 자산 (열역학 축이 요구하는 문서 장치)

**TH-9.1 "일반→특수" 사다리 1:1 대조표(flow-1) — [A 필수]** §2 의 표를 문건 안 표(정의·가정·레퍼런스·회수 식·유효범위·tier)로 두고, 각 boxed 식에 "사다리 좌표"를 달아 작업 챕터 3.2 게이트("기존 boxed 64 식이 사다리 어디서 회수되는지 매핑")의 문건 측 실물로 삼는다. 현행: keybox 참조 목록만(`ch1_sec02b_part0.tex:463-472`). 차원 0·침습 중(전 절 태그). 배치: 4.0/4.1.

**TH-9.2 기호 통합표(flow-3) — [A 필수]** 현행 국소 각주로 흩어진 충돌: g 4종(`ch2_sec05_mixing.tex:42-44`), q 3종(`ch1_sec02a_part0.tex:250`·`ch1_sec05_width.tex:107-108`), u_j 2종(`ch2_sec04_einstein.tex:20-22`), γ 2종(`ch1_sec04_hys.tex:264-266`·`ch1_sec07_broadening.tex:267-268`), F 2종(`ch1_sec02a_part0.tex:66-68`), z 2종(`ch1_sec05_width.tex:288`), ξ↔θ 배향(부록 `:8-9,57-63`), Ω 부호 규약(부록 Ω≡zN_AΔw vs 본문 Ω≡−(z/2)N_Au — `appendix_phase_separation.tex:100-102` vs `ch1_sec02b_part0.tex:24`; 둘 다 Ω>0=상분리로 일관하나 정의식이 다름). 부록 승격 시 이 표가 없으면 오독이 확실하다. 배치: 4.0 기호표.

**TH-9.3 tier A/B/C 규약 — 있음(`ch1_sec07_broadening.tex:64` 각주), 승계.**

---

## 4. 등급 종합표 (권고 실행 순서 포함)

| ID | 후보 | 등급 | 모델 차원 | 침습도 | 새 서지(N) 건수 | v2.0.0 배치 | 선행 의존 |
|---|---|---|---|---|---|---|---|
| TH-1.1 | 일반 격자기체 Hamiltonian 정점 | **A** | 0 | 중 | 3 | 4.1 | — |
| TH-2.1 | 정칙용액+Maxwell 두-상 dQ/dV 사슬 | **A** | 0(문건) | 높음 | 1 | 4.2·4.6 | TH-5.1·TH-1.2 |
| TH-3.1 | Redlich–Kister → α 승격 | **A** | +1/전이(α 대체 시 0) | 높음 | 2 | 4.2·4.5·4.6·4.7 | TH-1.1 |
| TH-5.1 | 상분리 부록 본문 승격 | **A** | 0 | 높음(구조) | 0(부록 5건 원장 등재) | 4.2 | TH-9.2 |
| TH-9.1 | 일반→특수 대조표 | **A** | 0 | 중 | 0 | 4.0/4.1 | 전체 |
| TH-9.2 | 기호 통합표 | **A** | 0 | 중 | 0 | 4.0 | — |
| TH-1.2 | 감수율 일반형·판정자·LCO 커널 통일 | B | 0 | 낮~중 | 3 | 4.1·4.2 | TH-1.1 |
| TH-2.4 | Frumkin 계보 서지 | B | 0 | 낮음 | 2 | 4.2·챕터 5 | — |
| TH-4.1 | 다중 부분격자 staging 일반식 | B | 0(설명) | 중 | 3 | 4.1·4.6 | TH-1.1, DQ-8 |
| TH-4.2 | Daumas–Hérold/Safran 배경 | B | 0 | 낮음 | 5 | 4.6 | TH-4.1 |
| TH-5.2 | CNT/CH → γ_j 함수형 | B | 0 또는 −1 | 중 | 2 | 4.5 | TH-5.1, DQ-11 |
| TH-6.3 | Maxwell 관계 2계 | B | 0 | 낮음 | 1 | 4.4 | TH-1.3(선택) |
| TH-7.1 | 세 분포 분리 가정 | B | 0 | 낮음 | 1 | 4.4 | — |
| TH-7.2 | 포논 DOS 일반→Einstein/Debye | B | 0/+1 opt-in | 중 | 2 | 4.4 | — , DQ-5 |
| TH-7.4 | 일반 엔트로피 수지→Bernardi→소산 | B | 0 | 중 | 4 | 4.4 | DQ-6 |
| TH-7.5 | Kirchhoff 일반 U(T) | B | 0 | 낮음 | 0 | 4.2·4.4 | — |
| TH-1.3 | 대정준 퍼텐셜·Legendre 형식 | C | 0 | 낮음 | 1 | 4.1 | — |
| TH-1.4 | q(T) 조성 의존 → Ω_S | C | 0/+1 | 낮음 | 0 | 4.4 | DQ-6 |
| TH-2.2 | 준화학/CVM | C | 0 | 낮음 | 2 | 4.1 | — |
| TH-2.3 | Ω(T)·M4 | C | +1/전이 | 중 | 0 | 4.4 | DQ-6 |
| TH-3.2 | dilute G5 | C | +1 | 낮음 | 0 | 4.6 | 상충 해소 |
| TH-4.3 | transfer matrix 1D | C | 0 | 낮음 | 2 | 4.1 | DQ-8 |
| TH-5.4 | PSD 나노 | C(유지) | 0 | 0 | 1 | 4.2 | — |
| TH-5.5 | Legendre–Fenchel 볼록 포락 | C | 0 | 낮음 | 1 | 4.2 | — |
| TH-7.3 | 전자 비축퇴 서술 | C | 0 | 낮음 | 0 | 4.4 | — |
| TH-8.5 | Landau cusp 통일 | C | 0 | 낮음 | 1 | 4.2 | — |
| TH-8.6 | Preisach 명명 노트 | C(각주) | 0 | 0 | 1 | 4.5 | — |
| D군 12건 | §1.2 표 + TH-3.3·5.3·6.4·6.5·6.6·8.3 | D | — | — | — | Non-goal 명시 | — |

권고 순서(본 에이전트 판단): **TH-9.2 → TH-1.1 → TH-5.1 → TH-1.2 → TH-2.1 → TH-3.1 → TH-9.1** 을 저작 4.1~4.2 의 골격으로 먼저 놓고, B 군은 4.4·4.5·4.6 절 저작 시 절 단위 루프 안에서 흡수한다. 이유: A 군은 서로 의존(정점 → 부록 승격 → 감수율 통일 → 두-상 사슬 → 비정칙 확장)이라 이 순서를 어기면 라벨·기호를 두 번 고친다.

---

## 5. 필요 레퍼런스 원장 초안 (서지 tier 별)

**(V1) 현행 bib 보유·그대로 재사용(주요)**: hill1960·fowler1939·mcquarrie1976·ashcroftmermin1976·mckinnon1983·dahn1991·ohzuku1993·bazant2013·dreyer2010·dreyer2011·leviaurbach1999·verbrugge2017·cogswell2012·bernardi1985·newman·huggins2009·reynier2003·reynier2004·allart2018·jpcc2021·persson2010b·vanderven1998·msmr_partII·hysteresis2018·occupation2019·larchecahn1973 (`ch1v22_bib.tex`·`ch2v22_bib.tex`·`ch3v22_bib.tex`).

**(부록 등재·원장 미등재)**: Cahn–Hilliard 1958 (DOI 10.1063/1.1744102)·Cahn 1961 (DOI 10.1016/0001-6160(61)90182-1)·Porter–Easterling 1992·Hillert 2008·Balluffi–Allen–Carter 2005 (`appendix_phase_separation.tex:484-495`) → 승격 시 V1 키 부여.

**(S) 기존 서베이 검증 표기 승계**: Safran *PRL* 44, 937 (1980); Guo–Smith–Bazant *JPCL* 2016; Cordoba–Chandesris–Plapp arXiv:2401.13108 (2024); Yao–Viswanathan *JPCL* 15, 1143 (2024); Zhu *Adv. Mater.* 2023 adma.202304666; Rykner–Chandesris *JPCC* 126, 5457 (2022); Paul *JES* 171, 020507 (2024) (`IMPROVEMENT_DIRECTIONS.md:77-86`·`LIT_ADVANCE_SYNTHESIS.md:127-129`). DOI 문자열이 서베이에 없는 건은 "DOI 미검증"으로 등재.

**(N) 신규 후보 — 전건 DOI 미검증·Crossref 대조 필요(작업 챕터 5 / DR-6 종속)**: Sanchez–Ducastelle–Gratias 1984; Lee–Yang 1952; Chandler 1987; Callen 1985; Callen–Welton 1951; Kubo 1966; Guggenheim 1952; Kikuchi 1951; Langmuir 1918; Frumkin 1925; Redlich–Kister 1948; Lukas–Fries–Sundman 2007; Daumas–Hérold 1969; Safran–Hamann 1979; Kirczenow 1985; Dresselhaus–Dresselhaus 1981; Chandesris et al. 2019; Derosa–Balbuena 1999; Gavilán-Arriazu 계열; Kramers–Wannier 1941; Baxter 1982; Bai–Cogswell–Bazant 2011; Turnbull–Fisher 1949; Burch–Bazant 2009; Rockafellar 1970; Landau–Lifshitz vol.5; Einstein 1907; Debye 1912; de Groot–Mazur 1984; Rao–Newman 1997; Thomas–Newman 2003; Latz–Zausch 2011 — 약 32건. 서지 필수 게이트(기준 3)에서 이 목록이 챕터 2.4 "리뷰급 주제별 필수 문헌 체크리스트"의 열역학·통계역학 항이 된다.

**서지 결함 발견 1건(챕터 2.4 입력)**: `ch1v22_bib.tex:49` verbrugge2017 과 `ch2v22_bib.tex:17` msmr_origin2017 이 **같은 DOI 10.1149/2.0341708jes 에 서로 다른 제목**("… Silicon, and Their Alloys" vs "… Iron Phosphate, and Layered Nickel-Manganese-Cobalt Oxide")으로 등재돼 있다. 둘 중 하나가 오기이며 확정은 Crossref 대조 필요(미검증).

---

## 6. 4-tier 보고

**확정(근거 path+line)**
1. SM2-A·B·C 세 후보는 v1.0.22 에서 집행되어 현행 문건에 있다 — `ch1_sec06_eqpeak.tex:74-119`, `ch1_sec02b_part0.tex:387-409`, `ch2_sec07_revheat.tex:74-95`. brief §4.5 의 "집행 여부 미확정" 은 이로써 해소.
2. ROADMAP 제안 1 집행됨(`ch2_sec04_einstein.tex`), 제안 5 부분 집행(`ch1_sec07_broadening.tex:253-304`), 제안 2·3 미집행(TH-3.1·TH-5.2 항 근거 행).
3. 두-상 평형 dQ/dV 의 델타+꼬리 식은 본문 어디에도 없고 부록 Maxwell 절도 본문 미연결(`appendix_phase_separation.tex:10,383-391`·`ch1_sec07_broadening.tex:20-23`); LCO 커널은 단상 곡률형(`ch1_sec16b_lcoomega.tex:24-31`).
4. Part 0 정점은 독립 자리+평균장이며 일반 Hamiltonian·다중 부분격자·Redlich–Kister·Debye·일반 엔트로피 수지는 문건에 없다(§2 표의 굵은 단; grep 0건 확인: Redlich/Kister/Debye/Onsager/transfer matrix/Kikuchi/Bethe/Ising/Preisach/Kramers/Jarzynski).
5. 같은 평균장 곡률식 RT/[ξ(1−ξ)]−2Ω 가 세 절에 독립 유도돼 있다(`ch1_sec04_hys.tex:27-30`·`ch1_sec05b_gr2L.tex:39-44`·`ch1_sec16b_lcoomega.tex:24-31`).
6. 부록과 본문의 Ω 정의식이 다르다(`appendix_phase_separation.tex:100-102` Ω≡zN_AΔw vs `ch1_sec02b_part0.tex:24` Ω≡−(z/2)N_Au) — 부호 방향은 일관.
7. v1.0.26 skew-regsol vs GITT 판정 미완(`HANDOVER_regsol_investigation.md:27-30,45`).

**근거 미발견**
- 준화학/CVM(TH-2.2)·transfer matrix(TH-4.3)가 흑연 dQ/dV 정량을 개선한다는 문헌 근거 — 미발견(교육·사다리 완결성만).
- L_1(Redlich–Kister) 의 흑연 실측값 — 미발견(LIT_ADVANCE 가 "독립 전이별 Ω-in-RT 없음" 이라 적은 것과 동급 `:119`).

**추정(본 에이전트 판단·재검산 대상)**
- TH-2.1 (v) Ω→2RT^+ 에서 델타 무게 (ξ_b^+−ξ_b^−)∝(T_c−T)^{1/2} 로 연속 소멸한다는 점, 그리고 그것이 §5b 의 "불연속하게 갈아탄다" 서술(`ch1_sec05b_gr2L.tex:78-82`)과 어떻게 양립하는지(함수형 불연속 vs 무게 연속) — 저작 시 명문화 필요.
- TH-3.1 의 g″·spinodal 3차식·정점 이동 대응은 손 스케치 — SymPy 재검산 대상.
- TH-7.2 Debye 닫힌 꼴은 표준식이나 본 문건에서 재검산 후 기재.

**미검증**
- (N) 서지 32건의 DOI·권·쪽 전부. Safran 1980 등 (S) 서지도 DOI 문자열은 미검증.
- verbrugge2017/msmr_origin2017 제목 불일치의 정오.

---

## 7. Decision Queue (골격 이견·brief 정정·추가 후보 — 근거와 기본값)

- **DQ-1 [brief 정정]** brief §4.5 "SM2-A/B/C 집행 여부 미확정 → 챕터 1.4 에서 확인" → **확정 집행됨**(§6 확정 1). 챕터 1.4 등록부에서 "재개방 후보 아님·승계"로 기재하고 3.1 후보 목록에서 제외 요청.
- **DQ-2 [TH-2.1 범위]** 정칙용액+Maxwell 을 (a) 문건 이론(델타+꼬리 일반식과 특수화 회수)까지만 넣을지, (b) dQ/dV 생성 커널(규제 δ_j 포함)까지 문건에 적을지. (b)는 코드 non-goal(brief §6)과 doc-leads 정합 문제를 낳고, v1.0.26 실험(skew-regsol vs GITT)이 미완이다. **기본값 제안 = (a)**, 커널 채택은 2.6/3.1 데이터 판정 후 별도 결정(DR-1 과 연동).
- **DQ-3 [TH-3.1 vs α_j]** v2.0.0 에서 α_j(tier C)를 유지하고 L_1 을 상위 일반식으로 두어 α_j 를 그 1차 근사로 "회수"할지(둘 다 보존·동시 자유화 금지), 아니면 α_j 를 L_1 로 대체할지. **기본값 제안 = 둘 다 보존·회수 표기**(자산 무유실 원칙 brief §4.4).
- **DQ-4 [TH-5.1 기호]** 부록 승격 시 부록 ξ(=점유)를 본문 θ 로 전면 치환할지, 부록 기호를 두고 매핑표로 갈지. **기본값 제안 = 전면 치환**(기준 2 교재 일관성; TH-9.2 표 선행).
- **DQ-5 [TH-7.2 Debye]** 다온도 데이터 없이 Debye 특수화를 본문 식으로 넣을지(파라미터화는 Einstein 유지). **기본값 제안 = 일반 DOS 적분식 + Einstein·Debye 두 특수화 식 제시, 피팅 파라미터는 Einstein 만(opt-in)**.
- **DQ-6 [Part T 경계 개정]** TH-7.4(히스 소산을 일반 σ 안에 위치)·TH-2.3/1.4(∂Ω/∂T)는 현행 Part T 의 "별개/범위 밖" 선언(`ch2_sec05_mixing.tex:193-194,230-238` [C-92])을 개정한다. 챕터 1.3 등록부에서 이 두 선언을 "v1.0.25 한정·개정 가능" 으로 분류할지 사용자 확인 필요(선언 자체는 서브 저작이며 사용자 결정 기록은 원천에서 미발견).
- **DQ-7 [서지 검증 비용]** (N) 32건 + (S) 7건의 Crossref 대조는 DR-6(외부 접근) 승인에 종속. 미승인 시 문건에 "DOI 미검증" 표기로 등재하는 것을 기본값으로.
- **DQ-8 [스코프 재개방]** SM2 축 B(staging 미시화 "스코프 밖", `SM2_SURVEY.md:41-42`)는 서브 에이전트 판단이었고 사용자 결정 기록이 아니다. 기준 5 는 TH-4.1~4.3 의 재개방을 지지한다. **기본값 제안 = TH-4.1·4.2 는 설명층으로 재개방(B), TH-4.3 은 C**.
- **DQ-9 [IMPROVEMENT #2 함수형]** 원 제안은 양측 폭 w^L≠w^R 이었고 v1.0.25 는 거듭제곱 α 로 구현했다(§1.1 표). TH-3.1 채택 시 둘 다 L_1 의 근사로 회수 가능한지 저작 중 검산 — 결과에 따라 α 의 지위 문구 개정.
- **DQ-10 [Ω 정의식 통일]** 부록 Ω≡zN_AΔw 와 본문 Ω≡−(z/2)N_Au 는 같은 물리(Ω>0=상분리)이나 정의가 다르다. 승격 시 본문 정의로 통일하고 부록 유도(쌍 에너지 w_AA,w_BB,w_AB)를 본문 §2.4 (a)-(b) 에 흡수하는 것을 기본값으로.
- **DQ-11 [동역학 축과 경계]** TH-5.2(γ_j 함수형)와 TH-2.1 (iv)(δ⊗kinetic 합성)는 동역학 후보 카탈로그와 겹친다. 경계 제안: 열역학 축 = ΔG*(ξ)·Maxwell·binodal 함수형, 동역학 축 = 이탈 시점(율속)·L_V 합성. 두 카탈로그 통합 시 master 가 한 번 정리.
- **DQ-12 [서지 결함]** verbrugge2017/msmr_origin2017 동일 DOI·상이 제목(§5) — 챕터 2.4 서지 감사 입력으로 등록 요청.

---

## 8. Read Coverage (파일·행 범위 전건)

배정 원천(전문):
- `results\handoffs\2026-09-02-v2-master-plan\brief.md` 1–219 (전문)
- `docs\v1.0.18.2\ROADMAP_future_physics.md` 1–50 (전문)
- `results\comp_v24\IMPROVEMENT_DIRECTIONS.md` 1–87 (전문)
- `results\comp_v24\LIT_ADVANCE_SYNTHESIS.md` 1–130 (전문)
- `docs\v1.0.22\results\comp_SM2\SM2_SURVEY.md` 1–136 (전문)
- `docs\v1.0.22\results\comp_v23\SURV_SYNTHESIS.md` 1–45 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec02a_part0.tex` 1–391 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec02b_part0.tex` 1–475 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec03_center.tex` 1–122 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec04_hys.tex` 1–337 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec05_width.tex` 1–425 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec05b_gr2L.tex` 1–239 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec06_eqpeak.tex` 1–132 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec07_broadening.tex` 1–376 (전문)
- `docs\v1.0.25.1\_sections\ch2_sec01_partition.tex` 1–150 (전문)
- `docs\v1.0.25.1\_sections\ch2_sec02_config.tex` 1–191 (전문)
- `docs\v1.0.25.1\_sections\ch2_sec05_mixing.tex` 1–256 (전문)
- `docs\v1.0.25.1\_sections\ch2_sec07_revheat.tex` 1–103 (전문)

보조 정독(배정 밖·보유 상태 확인용):
- `docs\v1.0.25.1\appendix_phase_separation.tex` 1–498 (전문)
- `docs\v1.0.25.1\_sections\ch2_sec03_vibel.tex` 1–119 (전문)
- `docs\v1.0.25.1\_sections\ch2_sec04_einstein.tex` 1–208 (전문)
- `docs\v1.0.25.1\_sections\ch2_sec06_limits.tex` 1–54 (전문)
- `docs\v1.0.25.1\_sections\ch2_sec08_synthesis.tex` 1–239 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec16b_lcoomega.tex` 1–161 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec13_lcohys.tex` 125–174 (부분 — 클러스터 전개 srcbox 만)
- `docs\v1.0.25.1\_sections\ch1v22_bib.tex` 1–57 · `ch2v22_bib.tex` 1–22 · `ch3v22_bib.tex` 1–45 (전문)
- `results\comp_v26_data\HANDOVER_regsol_investigation.md` 1–56 (전문)
- `docs\v1.0.25.1\_sections\ch1_sec10_sum.tex` 42–51 (Grep — tab:staging Ω 초기값 행만)

기계 확인: `_sections` 전체 Grep(키워드 Daumas|Safran|sublattice|부분격자|transfer matrix|Redlich|Kister|Cahn|Debye|Onsager|entropy production|Preisach|cluster expansion|quasi-chemical|Kikuchi|Bethe|Ising|Legendre|Jarzynski|Kramers|Gibbs-Thomson) — 결과는 §6 확정 4·5 에 반영. 이 Grep 은 정독 대체가 아니라 "없음" 판정의 보강이다.

미정독(본 카탈로그 범위 밖·판정에 불요): `ch1_sec08_lag`·`ch1_sec09_tail`·`ch1_appE_selfconsistent`(동역학 축)·`ch1_sec11~17` LCO 나머지·Ch3 절·`ch1_sec00_intro`·`ch1_sec01_n0n1`·`ch1_sec18_inputs`·부록 A/B/C/D·`Codex\` 일체(무접근).
