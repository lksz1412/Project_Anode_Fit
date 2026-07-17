# RV1 — 신 Chapter 1 (흑연 곡선 + 열특성) 선행 검수 보고

> 창 = RV1 (Opus). **보고 전용** — 파일 수정·git·Codex 접근 없음.
> 대상 = `ch1_graphite_v1.0.22.tex` 조립 전 소스(_sections/): Part 0(ch1_sec00~02b)·Part I(sec03~10)·Part T(ch2_sec00~10)·§18(sec18)·부록 A/B/C/D(ch1_appA·ch1_appB·ch2_appA·ch2_appB)·bib(ch1v22_bib). **전 30본 전문 정독 완료.**
> 검수 축 = ①물리·수학 ②구획 재편 잔재 ③검수 7항목(P3) ④축소·왜곡 ⑤서지 내적 정합.
> R2 신규 삽입분(CLT bgbox·CNT 문단·srcbox 7본) 집중 검증.
> 로그 대조: undefined ref/cite = 0(전 \ref·\cite 해소). multiply-defined = 2건(swiderska2019·LastPage, 아래 L5).
> 범위 밖 확인: ch1_sec11~17(LCO)·ch1_appD_si(Si)는 graphite master 에 \input 되지 않아 미검수(각각 R3·R5 소관).

---

## 0. 총평 (먼저)

**물리·수학 하드 오류(H) = 0.** 부호 사슬·유도 사슬·수식-산문 정합이 전반적으로 매우 견고하다. 검증 가능한 수치 예제(sec10 끝-대-끝, ch2_sec08 계산 예제, 부록 A R1~R6)를 **전건 독립 재산출로 대조 — 전부 일치**(w=25.693 mV, U_j(298)=210.87/139.92/120.32/85.29 mV, 합산 6.95 Q_cell/V; 열특성 U_oc=74.4 mV·∂U/∂T=−0.204 mV/K·ΔS=−19.7·Q̇_rev/I=+60.8 mV; ΔU^hys(R1)=86.7 mV). R2 삽입분의 물리(CLT·CNT·다리 7본)는 대체로 정확하고 가드가 충실하다.

주의 요할 곳은 **① CLT bgbox 의 Dreyer 인용 범위(M1 — dreyer 다리의 가정차와 긴장)**, **② 구획 재편 잔재 2군(M2 "Part II"·M3 "Ch2 §2.x") — 낡은 장 지칭이 신 구조와 충돌**이다. 나머지는 표기·이음매 L급.

**주목할 부재(미검증)**: CLAUDE.md P1·P3-5 가 요구한 **사용자 JCP 147(14) 144111 (2017) ref.6·7 방법론**의 별도 sub-section(서지·본문 위치·수학 구조·변수 매핑·가정 차 4항)이 조립 graphite 문서에 **보이지 않는다**. 순환 의존성은 Part 0 §2.6 의 대정준 제약 반전(정의상 implicit)으로 자족 처리돼 있으나, ref.6·7 명시 반영 여부는 마스터 확인 필요(§3 P3-5).

---

## 1. 발견 목록 (등급순)

### H (물리 오류/오귀속) — 0건
없음.

### M (의미 훼손 가능) — 3건

**[M1 | `_sections/ch1_sec07_broadening.tex`:143–145 | M | 서지 |**
현행: "…$\eta$ 는 소인 시간척도에서 입자별로 정적(quenched)이라 식~(eq:ensavg) 는 quenched 앙상블 평균이며…, **다입자 앙상블 평형의 표준 그림\cite{dreyer2010,dreyer2011}에서 (iii-b) 입자간 $\eta$ 산포가 이 종으로 닫힌다.**"
문제: CLT bgbox 가 **(iii-b) 입자간 η 산포의 종형(broadening 층)**을 dreyer2010/2011 에 귀속하는 문장이다. 그러나 같은 절의 **dreyer 다리 srcbox(76–101, 특히 95–98 가정차)**는 "원 골격은 …단일입자 등온선이 갈림의 **유일 원천**이나, 본문은 그 위에 겉보기 전위 U_app=U_j+η 의 앙상블 이질성((iii-b) η 분포)을 **별도 broadening 층으로 얹고**"라고 명시 — 즉 **η-heterogeneity 는 Dreyer 골격 밖, 본문 고유 층**임을 못박는다. 또 절 서두(59행)는 "(iii-a)와 (iii-b)를 섞으면 '중심이 분포한다'는 잘못된 그림"이라고 경고한다. CLT box 의 인용은 이 (iii-a)/(iii-b) 분리 원칙과 긴장하며, Dreyer 가 하지 않은 η-종형을 Dreyer 에 얹은 것으로 **오독될 수 있다**(CLT 자체는 표준 정리 — 초안 헤더도 "무인용 관용"이라 적음).
등급 근거: 물리(CLT 수식)는 정확·4가드 완비. 그러나 서지 귀속 범위가 다리 가정차와 상충 — 의미(누가 무엇을 보였나) 훼손 가능. **오귀속 경계선이나 방어 가능(Dreyer=다입자 앙상블 '플랫폼'을 세운 것은 사실)이라 H 아닌 M.**
제안: (a) 해당 절에서 `\cite{dreyer2010,dreyer2011}` 를 빼거나(CLT 무인용 관용), (b) "다입자 앙상블(Dreyer 의 공통-μ 평형 플랫폼) **위에서** (iii-b) η 산포가 CLT 로 종에 닫힌다"처럼 Dreyer=플랫폼/CLT=종형-closure 를 문법으로 분리. 마스터 triage.

**[M2 | `ch1_sec01_n0n1.tex`:32,156 · `ch1_sec02b_part0.tex`:29 | M | 이음매(구획 재편 잔재) |**
현행:
- sec01:32 "이 규약은 \S(notation)–\S(sum) 과 **Part II 전건**에서 유지되며…"
- sec01:156 "이 골격의 두 번째 전극(LCO 양극) 일반화는 **Part II**(\S\ref{sec:lco-intro})가 연다."
- sec02b:29 "본론 표(tab:staging) 의 Ω_j 와 **Part II** 의 Ω_j^cat(…\S\ref{sec:lco-hys})…"
문제: 본 장의 내부 파트 구조는 sec00:25 가 명시하듯 **Part 0 → Part I → Part T** 뿐이고 "Part II" 는 없다. "Part II" = LCO 인데, v1.0.22 재편에서 LCO 는 **독립 Chapter 2**(ch2_lco)로 분리됐다. 실제로 **sec00:27·sec10:168·Part T 전역(ch2_sec00:61, ch2_sec03:77·89, ch2_sec05, ch2_sec09:20, §18:65)은 LCO 를 일관되게 "Chapter 2"로** 부른다. 곧 "Part II" 3곳은 구 결합-장(Part I=흑연/Part II=LCO) 시절의 낡은 지칭이 살아남은 것으로, 같은 문서 안에서 LCO 를 "Part II" 와 "Chapter 2" 두 이름으로 부르는 격 불일치다(P3-7 직격). \ref 자체는 xr 로 외부 Chapter 2 에 해소되므로 링크는 작동하나 **라벨이 틀렸다**.
제안: 3곳 "Part II" → "Chapter 2"(또는 "다음 장")로 통일. **주의**: LCO 장(ch2_lco)은 스스로도 "Part II 도입"(ch1_sec11:4 — 범위 밖)으로 자칭하므로, 최종 결정(LCO=Chapter 2 vs Part II)은 두 장에 걸친 마스터 정합 사안. RV1 은 graphite 쪽 3곳만 지목.

**[M3 | `ch1_appB_codemap.tex`:79,100 | M | 이음매(구획 재편 잔재) |**
현행:
- 79행(tab:inputs, `n_T1` 행) "…발효 시 폭·가역 발열 config 계수에 동반 전파(**Ch2 \S2.5** 폭 $T$-의존 일반화)"
- 100행(tab:inputs, `theta_E` 행) "Einstein 온도 θ_{E,j}[K]·기준온도 (**Ch2 \S2.4** Einstein 절)"
문제: "Ch2 §2.5"(폭 T-의존)·"Ch2 §2.4"(Einstein)가 가리키는 절은 각각 **Part T 의 mixing(ch2_sec05)·einstein(ch2_sec04)** — 즉 **바로 이 Chapter 1 의 Part T 안**이다. 재편 후 그 열특성 절들은 Chapter 1 소속이고(마스터 preamble `\thesection=1.\arabic{section}` 라 렌더 시 §1.14/§1.15 대), Chapter 2 는 LCO 다. 따라서 "Ch2 §2.4/§2.5" 는 **장(Ch2≠본장)·절번호(2.x≠1.x) 둘 다 stale** 한 하드코딩 텍스트 포인터로, 독자를 존재하지 않는 위치(LCO 장의 Einstein §2.4)로 오유도한다. (\ref 아닌 생 텍스트라 자동 해소도 안 됨.)
제안: `\S\ref{sec:mixing}`·`\S\ref{sec:einstein}` 또는 "Part T §…"로 교체. ※ 대응되는 ch2_appB(부록 D)는 이미 `\S\ref{sec:einstein}` 등 live 참조를 써서 정상 — ch1_appB 만 잔재.

### L (표기) — 7건

**[L1 | `ch1_sec02a_part0.tex`:172 | L | 표기/물리(경계선) |**
현행: mckinnon 다리 대응표 행 "$\tfrac{RT}{sF}\ln\tfrac{\xi}{1-\xi}$ 항 (eq:Veq) ↔ 배치 항 $\tfrac{kT}{e}\ln\tfrac{x}{1-x}$" (x 가드: "자리 점유율 — 본문 θ·ξ 에 해당").
문제: 두 로그항을 같은 선행부호로 나란히 두는데, 행 가드대로 x=θ=1−ξ 를 대입하면 $\ln[x/(1-x)]=\ln[(1-\xi)/\xi]=-\ln[\xi/(1-\xi)]$ 라 **두 항은 서로 음수**다. 실제 정합은 McKinnon 등온선이 config 항 앞에 **음부호**(V=E₀−(kT/e)ln[x/(1-x)]−…)를, 본문 eq:Veq 는 **양부호**(V=U_j+(RT/sF)ln[ξ/(1-ξ)]+…)를 갖고 ξ=1−x 가 그 부호차를 흡수하는 데서 온다(→ ch2_sec01 eq:Veq_BW 가 같은 등온선을 θ-형으로 적어 이 정합을 확증 — 검증 완료). 즉 **물리는 정확**하고 표는 "역할 대응(대응한다)"으로 읽으면 맞으나, 부호 사슬을 축자로 따지는 독자(P3-1 대상)가 "+ln[ξ/…] = +ln[x/…]" 로 오독할 여지.
제안: 이미 있는 R-4(bazant η)·R-5(mckinnon x) 글자 가드처럼, 이 행에 half-line "(원 등온선은 config 항 앞 −부호 — ξ=1−x 로 정합)" 추가. 물리 무변경.

**[L2 | `ch2_appA_traps.tex`:40,50 | L | 표기(구획 재편 잔재) |**
현행: 함정표(부록 C) 행 "$g_j(\xi)$(**Ch1** 조성 자유에너지)"(40), "$u_j$ vs **Ch1** $u_j$"(50).
문제: "Ch1" 이 가리키는 g_j(ξ)(sec:sm-mf, Part 0)·spinodal u_j(sec:hys, Part I)는 모두 **본 장(Chapter 1) 안**이다. 구 결합-장 시절 열특성=Ch2 관점에서 흑연 곡선=Ch1 이라 붙인 지칭이 남은 것. 본문 서술은 "앞 파트 \S\ref{sec:hys}"·"같은 문서 내"로 이미 갱신됐고 행 헤더 약칭만 stale.
제안: 행 헤더 "Ch1" → "Part I"/"Part 0"/"앞 파트". (S_e 행 68행은 이미 "Chapter 2"로 정상 표기 — 대비.)

**[L3 | `ch1_appB_codemap.tex`:5,134 · `ch1v22_bib.tex`:44 | L | 표기(버전 지칭) |**
현행: appB:5 "구현(`Anode_Fit_v1.0.19.py`)", appB:134 "(v1.0.19 additive…)", bib:44 numverif2026 "`Anode_Fit_v1.0.19` 4-전이…".
문제: 문서는 v1.0.22 이고 폴더에 `Anode_Fit_v1.0.22.py` 가 실재(69 KB, 07-17)하나 코드 지칭이 일관되게 **v1.0.19**. 일관적이라 (a)의도적 계보 앵커일 수도, (b)버전 미갱신 잔재일 수도.
제안: 마스터가 코드 파일 버전 의도 확인 후 v1.0.22 로 갱신하거나 계보 의도면 유지. (물리·서지 영향 0.)

**[L4 | `ch2_sec03_vibel.tex`:73–74(label eq:Se-ch2) | L | 표기(정보용) |**
현행: 자리당 Sommerfeld 식에 `\label{eq:Se-ch2}` — 자산주석 [C-65] "Ch1 eq:Se 와 라벨 충돌 회피 개명".
문제: "-ch2" 접미는 구 Chapter 2(열특성) 정체의 흔적. 현 분할에서 이 식은 Chapter 1 Part T 에 있고 LCO 장의 eq:Se 는 외부 문서라 **실충돌 없음**(로그에 eq:Se-ch2 중복정의 경고 없음 확인). 게다가 부록 C 함정표 66–69행이 "eq:Se-ch2(본 장) vs eq:Se(Chapter 2)" 를 **명시 문서화** — 의도적 처리.
제안: 조치 불요(정보 기록). 라벨은 임의 문자열이라 렌더 무영향.

**[L5 | 빌드 로그 | L | 표기(빌드 경고) |**
현행: `LaTeX Warning: Label 'swiderska2019' multiply defined.` · `Label 'LastPage' multiply defined.`
문제: bib 헤더가 밝힌 "공통 키의 타 장 중복 수록은 의도(D22)" + `\externaldocument{ch2_lco}` 로 xr 이 ch2 의 동명 bibitem/LastPage 라벨을 끌어와 생기는 **양성 경고**(로컬 \cite 는 자기 장 것으로 해소 — undefined citation 0 확인). 기능 결함 아님.
제안: 무해 기록. 정 없애려면 xr 라벨 접두 분리(과잉 — 권장 안 함).

**[L6 | `ch2_appA_traps.tex`:2 | L | 표기(비렌더 주석) |**
현행: 파일 상단 주석 "부록 A — 기호·부호 함정 검산표…" (렌더 섹션 제목은 "부록 C").
문제: CHERRYPICK Option 2 재번호(→부록 C, label sec:traps-thermal)는 본문에 반영됐으나 파일 헤더 주석은 "부록 A"로 잔존. 비렌더 코드 주석이라 출력 무영향.
제안: 주석 헤더 "부록 A" → "부록 C" (선택).

**[L7 | `ch1_sec06_eqpeak.tex`:8 · `ch1_sec02b_part0.tex`:347 · `ch1_sec10_sum.tex`:5 | L | 표기 |**
현행: 중심 전하 보존식 "$Q_\cell q=Q_\bg(V_n)+\sum_jQ_j\xi_j$" 에 배경 **전하** $Q_\bg$ 사용.
문제: 기호 마스터표(sec01:63)에는 배경 **미분용량** $C_\bg$[C/V]만 등재. $Q_\bg$(배경 전하, C — 미분하면 $C_\bg$)는 표에 없이 문맥으로만 쓰임. 자기정합(dQ_bg/dV=C_bg)이라 오류 아니나 중심식 기호가 표 밖. 재편 무관 선존 사안.
제안: 마스터표에 $Q_\bg$[C, 배경 저장 전하; $C_\bg=\dd Q_\bg/\dd V$] 한 행 추가하면 완결. 저우선.

---

## 2. R2 신규 삽입분 개별 판정 (집중 검증)

| 삽입 | 위치 | 물리 정확성 | 기존 본문 정합 | 판정 |
|---|---|---|---|---|
| **CLT bgbox** | ch1_sec07:130–151 | CLT 형상근거 정확·Lindeberg 조건·σ_η²=Σσ_k² 가법·4가드(forward-only/흑연두-상 한정/비-크기/②≠Gaussian→②⊗③=logistic⊗Gaussian) 완비 | eq:widthbudget·fig:widthbudget(정직한 10% 한계 명시)과 정합 | **채택 가(단 M1 인용 조정)** |
| **CNT 연결 문단** | ch1_sec04:253–265 | ΔG*·핵생성률∝exp(−ΔG*/k_BT)·binodal 근방 ΔG*발산 정확; "CNT=γ_j 근거지 예측식 아님" 과대주장 회피 | γ(계면E)≠γ_j·부록 ξ(점유)≠본문 ξ(진행률) 두 가드 명문; γ_j<1 조기이탈 그림 정합 | **채택** |
| srcbox weppner+baek(병합) | ch1_sec01:221–248 | GITT↔eq:vn 연속근사·∂U_oc/∂T=ΔS/F↔entropic potential 정확; 가정차(R_n 근사한계·tier B) 적정 | [V21-Q5-02] 앵커 뒤 삽입·bgbox 항(i)(ii) 정합 | **채택** |
| srcbox mckinnon1983 | ch1_sec02a:162–186 | 격자기체 등온선 대응 정확; R-5 x 가드 有 | eq:sm-bare·eq:Veq·eq:spinodal 라벨 실재 | **채택(L1 부호 half-line 권고)** |
| srcbox bazant2013 | ch1_sec05:120–150 | eq:br-bazant2013-1 차원항등(F/R=e/k_B) 정확; α 분할·I_0 조성의존 가정차 정확; R-4 η 가드 有 | TST bgbox 뒤 삽입(사슬 절단 회피, CHERRYPICK 조정대로) | **채택** |
| srcbox dreyer | ch1_sec07:76–101 | 결과-구조 대응·"부호만 대조"·"Ω>2RT 문턱 본문 고유" 과대주장 회피 | (iii-a) 문단 직후 | **채택**(M1 은 CLT box 쪽 문제이지 이 다리 아님) |
| srcbox bernardi1985 | ch2_sec07:27–45 | eq:qrev 항 대응 정확; ③(소거근거)는 22–25행 포인터로 축약(R-2 반영) | 두 전제 문단 직후 | **채택** |
| srcbox allart2018 | ch2_sec09:31–50 | ΔS^0_j=F dU_j/dT↔전극몫 ΔS(x); "중심값 부호·규모 수준, 점대점 아님" 한정 | procedurebox 직후 | **채택** |
| srcbox reynier2003 | ch2_sec03:35–45 | S_vib(BE)↔"second contribution" 음 baseline; 정성분해(tier B) vs 제일원리 가정차 정확 | jpcc2021 문장 직후 | **채택** |

**서지 내적 정합**: 위 9 다리의 \cite 키 전건 ch1v22_bib 수록 확인(bazant2013·dreyer2010/2011·mckinnon1983·weppner_huggins1977·baek_pilon2022·bernardi1985·allart2018·reynier2003·jpcc2021·numverif2026). 문장 주장과 bib 항목 성격 일치. 원문 미재현 3건(dreyer 식번호·mckinnon 단행본 장·bernardi 식번호)은 "결과/항 대응 수준" 어법 준수(단정 회피) — 규칙 준수 확인. ch2_sec02:140–142 의 msmr_partII "+3~4 mV/K vs +0.30 mV/K" 자릿수 불일치는 **[미검증] 각주로 정직 표기** — 모범적.

---

## 3. 검수 7항목(P3) 점검

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | V_n 계열 구분 일관 | **정합** | V_app(측정)/V_n(내부)/U_oc(준평형)/V_eq(등온선)/U_j(중심)/U_j^d(분기) 위계 전 장 일관. ※구 ver 의 V_{n,app/drive/OCV} 축자 표기는 부재(현 문서 자체 표기 일관이라 무방). 부록 A S1–S8·R1–R6 전수 검산 PASS. |
| 2 | 전하 보존 = 내부 전위 결정 중심식 | **정합(주의 1)** | eq:sm-mc-balance(sec02b:341)·eq:implicit(ch2_sec05:16)이 U_oc 를 보존식 음함수 유일근으로 세움. **단** Part I 곡선은 V_n(분극환산)에서 forward 점평가 — 보존식은 열특성/평형 역방향과 SM 기원으로 중심 유지(Part 0 §2.6·Part T 파생A 가 두 방향 명시 정합). "OCV 에서 읽는 회귀" 아님. |
| 3 | 순환 의존성 표기 | **정합** | sec02b:348–352 가 U_oc 음함수·자기정합성을 산문으로 명시 진단(대정준→정준 Legendre 켤레 반전). 전용 dependency-그래프/표는 없으나 서술 명료. |
| 4 | 공백 4분류 진단 | **정합** | sec02b:350–352 가 "**정의상 implicit formulation**"으로 명시 분류(4범주 중 하나 지정). 요동 양성→유일근 증명(verifybox)으로 "논리 공백" 아님을 별도 확정. |
| 5 | ref.6·7 방법론 4항 sub-section | **미검증/부재** | 사용자 JCP 147(14)144111(2017) ref.6·7 의 서지·본문위치·수학구조·변수매핑·가정차 별도 절이 **조립 graphite 문서에 없음.** 순환의존은 대정준 제약반전으로 자족 처리됐으나 ref.6·7 명시 반영은 미확인. **마스터 확인 요**(의도적 대체 vs 후속 phase 이월). |
| 6 | Ch1 기준식 ↔ 전달식 충돌 | **정합** | 기준식(eq:sm-mc-balance·eq:eqpeak·eq:qrev·eq:Ubranch)을 Part T(파생 D 는 eq:Ubranch 의 γ_jh_η=1 특수형 명시)·§18·Chapter 2 전방참조가 충돌 없이 되밟음. "ver.N 전달식" 절 제목은 조립본에 부재(구조 무해). |
| 7 | ver.N/Chapter·Part 명칭 혼동 | **잔재 有** | Part 0/I/T·Chapter 2/3 는 대체로 정연하나 **M2("Part II"=LCO 3곳)·M3("Ch2 §2.x"=Part T 2곳)·L2("Ch1"=본장 2곳)** 이 구 명칭 재유입. 비렌더 자산주석(% [C-xx], [V21-xx])의 "Ch1/Ch2" 다수는 출력 무영향(집계 제외). |

---

## 4. 4-tier 요약

**확정(재산출·라벨·로그로 검증):**
- 물리 하드오류 0; 수치 예제 3군(sec10·ch2_sec08·부록A R1~R6) 독립 재산출 전건 일치.
- R2 삽입 9본 물리·정합 채택 가(M1 인용 조정 1건 부수).
- undefined \ref/\cite = 0(로그). 전 30본 정독 완료.
- 부호 사슬(부록 A S1–S8·R1–R6)·이중계산 분리(파생 B)·라벨 층위 가드(방전 I>0 vs 탈리튬화)·기호 충돌 가드(s/σ_d, θ/ξ, θ/θ_E, x̄/x, g 4종, F_vib/F, u_j 2종, γ/γ_j) 전건 명문 — 매우 견고.

**추정(정황상 판단, 마스터 확정 필요):**
- M1 Dreyer 인용은 "플랫폼 인용"으로 방어 가능하나 다리 가정차·(iii-a)/(iii-b) 분리 원칙과 긴장 — 조정 권고(오귀속 경계선).
- M2 "Part II"·M3 "Ch2 §2.x": 재편 잔재로 판단(신 구조 Chapter 2·Part T 와 충돌). L2·L3 동류.
- L1 mckinnon 부호: 역할대응이라 물리 정확, 축자 독자 오독 여지 — half-line 가드 권고.

**미검증(RV1 범위 밖·확인 불가):**
- **P3-5 ref.6·7 방법론 4항 절의 부재** — 의도(대정준 반전으로 대체) vs 이월 여부 마스터 확인 요(가장 주목).
- L3 코드 버전(v1.0.19 vs 실재 v1.0.22.py) 의도.
- 서지 원장(V1022_REFERENCE_LEDGER) 대조는 지시대로 미수행(본문 내적 정합만 확인 — 이상 없음).
- ch1_sec11~17(LCO)·ch1_appD_si(Si)는 graphite master 밖이라 미검수(R3·R5 소관).

**총평**: 신 Chapter 1 은 물리·유도 품질이 높고 R2 증축·다리가 잘 통합됐다. triage 우선순위 = **M1(인용 범위) → M2·M3(재편 잔재 낡은 지칭) → P3-5 부재 확인 → L군(표기·부호 가드)**. 수정은 마스터 소관 — 본 보고는 지목까지.
