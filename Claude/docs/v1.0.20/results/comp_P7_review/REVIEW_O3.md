# REVIEW_O3 — v1.0.20 독립 검수 (검수자 O3)

- 담당: 독립 검수자 O3 (다른 창 O1/O2/F1 과 통신·산출물 참조 없음)
- 역할: Ch1 LCO 청크(§11–§17) + ch1_bib 전문 정독 + 3축 검수(①신본 결함 ②v1.0.19 regression ③신설 다리 물리·서지)
- 담당 청크: ch1_sec11_lcointro · ch1_sec12_lcocenter · ch1_sec13_lcohys · ch1_sec14_lcodecomp · ch1_sec15_lcoelec · ch1_sec16_lcopeak · ch1_sec17_msmr · ch1_sec18_inputs · ch1_bib
- 신본: /home/user/Project_Anode_Fit/Claude/docs/v1.0.20/_sections/
- 구본(대조 read-only·불가침): /home/user/Project_Anode_Fit/Claude/docs/v1.0.19/_sections/
- 심각도: H=물리·수식 오류/오귀속 · M=유도 비약·정합 결손·regression · L=표기·문장·일관성
- 축: ①신본 자체 결함 · ②v1.0.19 대비 regression · ③신설 다리 물리·서지

---

<!-- 파일별 발견분을 정독 완료 즉시 append -->

### ch1_sec11_lcointro.tex (전문 정독 완료, 173행)

구본(173행)과 신본은 **두 곳의 인용 추가만** 차이: (i) L42 `세 전이를 남긴다\cite{xia2007}` (구본 무인용) (ii) L165 `MSMR 모델\cite{msmr_origin2017,msmr2024}` (구본 무인용). 둘 다 P4 의도된 인용 부여(RESULT_P4 "sec11 MSMR cite")·원장 V1 키(xia2007=A·msmr_origin2017=B·msmr2024=A). regression 없음.

물리·부호 검산: σ_d=+1⟺탈리튬화(산화·ξ:0→1·전위↑) 프레임이 흑연(방전↦+1)/LCO(충전↦+1) 양 전극에서 일관. 3작용처(분극 V_app>V_n·분기 탈리튬화=상가지·꼬리 적분방향) 부호 1:1 유지 — 모순 없음. w_j=n_jRT/F 차원 [V] 정합. 표 tab:lco-staging: T1(MIT ~3.90V·x0.94–0.75·center 0.85)·T2/T3(order–disorder, x≈0.55/0.48 = x=0.5 단사정 왜곡 좌우)·전위 오름차순(탈리튬화 x↓→V↑) 정합.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 1 | ch1_sec11:42 | L | ③ | "세 전이를 남긴다\cite{xia2007}" — MIT+order–disorder 2종의 전이 **동정(同定)** 은 고전적으로 Reimers–Dahn1992·Ohzuku·Menetrier 계보인데 이 문장엔 xia2007 단건만 부여 | L48 각주는 Xia·Reynier·Motohashi 3종으로 넓히나, L42 문장 자체는 xia2007 단건. 원장상 xia2007=V1 유효키라 오류는 아님 | (선택) L42 전이 동정 문장에 reimers1992 병기 검토 — 현행도 각주가 보완하므로 결함 아님 |
| 2 | ch1_sec11:165 | L | ③ | MSMR "표준 파라미터화" 명명 주장에 `msmr_origin2017,msmr2024` 인용 — "MSMR" **명명** 원전 bakerverbrugge2018 은 여기 미포함 | §17 계보 3단에서 명명 원전 별도 부여 예정(원장 B·CHANGE_LOG C-016). preview 성격상 원전+온도판 인용은 허용 범위 | 결함 아님(§17 에서 명명 원전 처리 확인 요) |

**가장 약한 1곳(sec11)**: L42 xia2007 단건 부여(#1). 각주가 보완하므로 결함 아님 — 빈 통과 방지 L급.

### ch1_sec12_lcocenter.tex (전문 정독 완료, 112행)

구본(112행) 대비 신본 차이는 **L94 `\cite{swiderska2019}` 1건 추가**(구본 "같은 문헌의 전셀…" → 신본 "같은 문헌\cite{swiderska2019} 의 전셀…"). U8 의도 부여(baseline ✅)·원장 A 유효키. regression 없음.

수식·수치 검산 전건 PASS: (i) U_j^cat=(-ΔH+TΔS)/F·∂U/∂T=ΔS/F 이중경로(직접미분 vs Gibbs 항등식) 일치·차원 [V],[V/K] 정합. (ii) Kirchhoff 가드(L68–73): ΔH 고정∧∂_TΔS≠0 은 ΔH'=ΔC_p=TΔS' 와 모순 — 정확. 불변식 ∂U/∂T=ΔS(T)/F·적분형 eq:lco-kirchhoff 정합, ΔS_e∝T→∫∝½(T²-T_ref²) 곡률(eq:U1T2) 정합. (iii) verifybox: F·0.83e-3=80.1≈+80 J/(mol K)·30K→+25mV 정확. (iv) **교차검증**: 전자항 창중심 -46 J/(mol K) ↔ 적분방출 1.1 k_B/atom — 46/8.314×(창폭 0.94-0.75=0.19)≈1.05 k_B ≈ 1.1, **정합**. ΔS_e<0(삽입=금속→절연체, 전자엔트로피 감소) 부호 정확.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 3 | ch1_sec12:99–109 | L | ① | verifybox "★전자항과의 부호 공존" 논거가 +80(전체계수 대표스케일)과 -46(전이별 전자항)의 **층위 다른 두 양을 직접 가감**("+80-46≈+34")한 뒤 곧바로 "서로 다른 층위"라 부정 — 독자에게 가감 가능/불가능이 한 문단서 진동 | L103 가감 → L107–109 "서로 다른 종류·층위" 부정. 논지(공존≠총부호 확정)는 정확히 hedge 됨 | 결함 아님(hedge 충분). 밀도 높아 오독 여지만 L급 지목 |

**가장 약한 1곳(sec12)**: L99–109 verifybox 의 교차층위 가감 서술 밀도(#3) — 물리는 정확, 가독성만.

### ch1_sec13_lcohys.tex (전문 정독 완료, 176행)

구본(169행) 대비 신본 신설: (i) L32 "문헌 물리"→"**상도표 물리**"·L33 `\cite{reimers1992,vanderven1998,motohashi2009}` 부여(U5) (ii) L107–111 **OD 계보 다리 신설**(XRD reimers1992→제일원리 vanderven1998→통계역학·연속체 ml2024) (iii) L135–137 **T1 MIT 실측+기작 다리 신설**(in situ 회절 reimers1992·전자 상도표 motohashi2009·불순물 Mott marianetti2004→§15.1) (iv) L160 "문헌 물리"→"pure-LCO 상도표 물리"·`\cite{reimers1992,vanderven1998}`(U6). 구본 원문장 전량 보존(계보문은 기존 "유효 인력" 문장 앞 삽입·"구조적 2상 공존" 어구 이동만) — 자산 유실 없음.

수식 검산 전건 PASS: eq:lco-gpp/spinodal/Veq/dUhys/Ubranch 흑연 대입형 정합·대칭중심=U_j^cat 정합·도핑 극한 ΔU→(8RT/3F)u³(artanh=u+u³/3 전개로 독립 재유도 일치)·T_c=Ω/2R 정확. eq:lco-mit 슬롯분리(구조 2상역 Ω_1 ∥ 전자 ΔS_e,1 → ∂U/∂T) = 이중계산 방지 경계, 물리 정확. Ω[J/mol] vs config ΔS[J/(mol K)] 단위·슬롯 혼동 가드(L124–132) 정확.

서지·귀속 검산: reimers1992=in situ XRD(정확)·motohashi2009="전자 상도표"(원제 "Electronic phase diagram of LixCoO2" 와 문자 일치)·marianetti2004=불순물 준위 Mott(host 띠 아님 — 하드가드 부합, §15.1 위임)·vanderven1998=제일원리 상도표(정확).

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 4 | ch1_sec13:110–111 | ~~M~~→해소 | ③ | OD 계보 3단째 "통계역학–연속체 스케일 브리징 계산이 같은 order–disorder 전이를 연속 조성축 위에서 재확인"을 ml2024 에 귀속 — **웹 확인으로 정확 확인**: ml2024 제목+초록이 정확히 "order–disorder transitions in Li_xCoO₂" 의 first-principles 통계역학→연속체 phase-field 스케일브리징. **귀속 정확·과대귀속 아님** | 웹: sciencedirect S0022509624001923·arXiv 2302.08991 — "study order–disorder transitions in LCO". 서지 필드도 원장 char 일치 | **해소(결함 아님)** — sec13 OD 계보 다리는 물리·서지 정확 |
| 5 | ch1_sec13:121–123 | L | ①/② | charge-order 엔트로피 0.47@x=½·1.49@x=⅔ 를 motohashi2009 tier A 귀속(구본서도 동일 — 신설 아님). motohashi2009 는 "전자 상도표" 논문이라 charge-order 엔트로피 정량값의 원출처인지 약함 | 구본 L121–123 동일(regression 아님). 슬롯배정 tier C·최종 피팅 위임으로 hedge 됨 | 기존 자산 — P4 소관 아님. 값 출처 원논문 재확인은 향후 |

**가장 약한 1곳(sec13)**: #4(ml2024 OD)는 웹 확인으로 해소. 잔여 최약 = L121–123 charge-order 엔트로피 0.47/1.49 의 motohashi2009("전자 상도표" 논문) tier-A 귀속(#5) — 구본 동일·슬롯배정 tier C hedge 로 완화, P4 소관 아님.

### ch1_sec14_lcodecomp.tex (전문 정독 완료, 100행)

구본(100행)과 신본 **byte 동일**(무변경 — RESULT_P4 "sec14 무변경" 확인). regression 원천 없음.

엔트로피 삼분해 재검산 PASS: Z_j=Z^config Z^vib Z^elec e^{-F^×/RT}(F^×≈0 독립극한)·F=-RT lnZ→로그 가법→S=-∂F/∂T 선형→가법 정합. config 분리 ∂S^config/∂x=ΔS^0(중심표준)+R ln[ξ/(1-ξ)](혼합, ξ=½서 0) 정확. 슬롯규칙(config←중심값만·혼합은 w_j·재기입 금지 / vib←중심 흡수 / elec←N_A∂S_e/∂x) = 이중계산 식화 방지, 정확. N_A∂S_e/∂x 차원 [J/(mol K)] 정합. "가산성(직교→Z 인수분해) vs 무이중계산(중심값·게이트골 한정)은 별개 질문" 분리 = 정확·명료.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 6 | ch1_sec14:68–73 ↔ ch1_sec15:45–50 | M | ① | §14 "가산성"은 config⊥elec(리튬 배열 vs 밴드 점유 근사 직교, Z 인수분해)에 근거하나, §15.1(신설) Marianetti 기작은 정공이 **Li 빈자리에 속박된 불순물 준위**(=전자 국재가 config[빈자리 위치]에 종속)라 MIT 창에서 config–elec **결합**을 함의 — 두 절 사이 정합 seam. §14 는 "MIT 부근 결합 선도차수 무시"로, §15 는 게이트 g(E_F,x) 의 x-의존·Δx_MIT(결함 분산)로 각각 흡수하나, **둘을 잇는 명시 문장 부재** | §14 L72 hedge + §15.1 L50–55 게이트 현상학화 — 양쪽 self-aware 이나 "불순물 결합이 게이트 x-의존/Δx_MIT 로 흡수돼 §14 직교가 조대격자 수준서 성립"이라는 연결 문장이 없음 | §14 또는 §15.1 에 1문장 다리(불순물 결합→게이트 x-의존 흡수) 추가 검토. 물리 오류 아님·hedge 존재라 soft M |

**가장 약한 1곳(sec14)**: L68–73 config⊥elec 직교 가정과 §15.1 불순물 준위 결합의 정합 seam(#6) — 양쪽 hedge 되나 연결 문장 부재.

### ch1_sec15_lcoelec.tex (전문 정독 완료, 290행 — 이 창 핵심)

구본(250행) 대비 신본 변경: **§15.1 전면 교체(B-004, L12–59)** + 자산주석 L288 `[V20-003]` 추가. **§15.2–§15.5(신본 L61–286)는 구본(L22–247)과 verbatim 동일** — 유도·수식·수치·그림 무변경, regression 없음.

**§15.1 B-004 구본 내용요소 항목별 보존 대조(축②)** — 전건 보존/개선:
| 구본 §15.1 요소 | 신본 위치 | 판정 |
|---|---|---|
| 3자유도(config·vib·elec)·흑연 셋째 몫 작음 | L13–15 | 보존 |
| x=1=Co³⁺ t₂g⁶ low-spin 닫힌껍질=전기 절연체 g(E_F)≈0 | L16–18 | 보존+정밀화(밴드 절연체·결정장 t₂g/e_g·띠간극) |
| 탈리튬화 x<0.94→Co⁴⁺ 정공→t₂g→금속, `menetrier1999,motohashi2009` | L19–20 | 보존(인용 유지) |
| MIT x≈0.75–0.94 2상역·§13 T1·국소 | L20–22 | 보존 |
| "게이트는 MIT 직접 결과" | L22 | 보존 |
| 인용 menetrier1999·motohashi2009 | L20,L40,L48 | 유실 없음 |

**하드 가드 3항 재검증(축③) — 전건 충족**:
- (i) 밴드 절연체(Mott 아님): L17–18·L39–41("Mott 절연체와 공유하는 것은 '절연' 결과뿐, 여기 절연은 상관 아니라 가득 찬 띠")·L48–50. ✅
- (ii) Marianetti 귀속 "설명/제시" 수준: L44 "그 까닭을 제시했다"·L47–48 "…설명한다"·L48 "(계산은 x≳0.95 절연·x≲0.75 금속 재현)". 과대 귀속("확정 유일 기작") 없음. ✅
- (iii) host 띠 Mott 아님: L49–50 "상관 물리 무대는 host t₂g 띠가 아니라…불순물 준위…Mott 물리는 불순물 띠 소관". ✅
- U·t vs U_j 가드: L36 인라인 "여기의 U 와 t 는…전극 전위 U_j 와 별개인 상관 물리 관용 기호". ✅(PICK_JUDGMENT 지정 인라인 형식)
- G-follow: bgbox 자족(밴드/Mott/MIT 정의→LCO 적용→퍼즐→Marianetti 해소→게이트 다리) — 학부 고학년 자족. ✅

**Sommerfeld 사슬 자체 재유도·차원 검산(전건 PASS)**:
- C_e=(π²/3)k_B²T g(E_F) 표준 결과·S_e=∫C_e/T'dT'=(π²/3)k_B²T g(E_F)(eq:Se). 직접경로 eq:Sedirect: ∫ŝ(ζ)dζ=π²/3 항등식으로 동일 — 두 경로 자기일관(∫ŝdζ=π²/3 는 두 표준결과 등치서 강제됨, 독립 확인). 차원 S_e/k_B=(π²/3)(k_BT)g 무차원 정합.
- Sommerfeld 동결 보정 O(T³)(ŝ 짝함수→g' 항 ∫ζŝdζ=0 상쇄, 첫 보정 g''(k_BT)³) 정확·"O(T²) Mott 항은 thermopower 소관" 정확.
- 단위환산 N_A k_B²=R k_B 정확·eV→J 는 /e_V(eq:gunit)·역(×e_V)시 1/e_V²≈4×10³⁷ 배 정합.
- 부호사슬: 삽입 x↑→금속→절연체→g 감소→∂g/∂x<0→ΔS_e=+∂S_e/∂x<0(삽입기준)·|ΔS_e|>0 탈리튬화 방출. 정확.
- eq:U1T2 ½인자: ∫a_e T'dT'=(a_e/2)(T²-T_ref²) 정확.
- eq:dSegate: ∂g/∂x=-(g_max/Δx)σ(1-σ)(σ'=σ(1-σ) 연쇄율) 정확.
- **수치 3중 검산**: (α) S_e=3.29×0.0259eV×13/eV≈1.108 k_B/atom ✅ (β) 게이트 골 |ΔS_e^mol|=(π²/3)R(k_BT/e_V)(g_max/Δx)·¼=3.29×8.314×0.0259×260×0.25≈46 J/(mol K) ✅ (γ) ∫|ΔS_e^mol|dx=(π²/3)R(k_BT/e_V)g_max=9.2 J/(mol K)=1.1 k_B/atom=완전 metal 끝점 S_e **항등** ✅. 게이트 3초기값(g_max=13 anchor·x_MIT=0.85=(0.94+0.75)/2·Δx=0.05→±2Δx=0.2≈창폭 0.19) 정합.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 7 | ch1_sec15:241 | **M** | ① | "전자항 없으면 config 단독으론 **MIT 2상역** 엔트로피 거동 재현 못함"을 ml2024 **tier A** 로 귀속 — **웹 확인 결과 ml2024 는 순수 배치(order–disorder) 스케일브리징이며 전자 엔트로피·MIT 를 다루지 않음**(초록: config free energy only, 전자·MIT 스코프 밖). 즉 order–disorder(x≈0.5·T2/T3) 논문을 MIT(x≈0.85·T1) 전자 엔트로피 불충분 주장의 tier-A 근거로 쓴 **스코프 불일치 인용** | 웹: arXiv 2302.08991 초록 "configurational free energy density…order–disorder transitions" — 전자/MIT 미포함. **구본 L202 동일(신설 아님·P4 regression 아님)**. 주장 자체("config 단독 MIT 불가")는 참이나 ml2024 는 그 tier-A 출처가 아님 | (선택) L241 ml2024 인용을 "config 전용 모델의 예시"로 격하하거나, MIT-전자 불충분의 직접 근거로는 tier 재검토. pre-existing 이라 P4 필수 아님 |
| 8 | ch1_sec15:34 | L | ③ | bgbox Mott 정의 "띠가 **부분적으로만** 차 있어" — 정준 Mott 절연체는 특히 **반충전(자리당 1개)**. "자리마다 하나씩 국재"가 뒤따라 보정하나 "부분적"은 약간 느슨 | L34–36. 후속 "자리마다 하나씩 국소화"가 반충전 함의 | (선택) "반쯤 찬" 뉘앙스 보강 — 오류는 아님, G-follow 정밀도만 |

**가장 약한 1곳(sec15)**: L241 ml2024 tier-A 스코프 불일치(#7·M·웹 확인) — 하드가드·유도·수치 전건 통과라, 유일한 실질 결함은 order–disorder 논문(ml2024)을 MIT-전자 엔트로피 불충분의 tier-A 근거로 쓴 인용. **단 pre-existing(§15.2–15.5 verbatim·P4 신설 아님)** — B-004 신설분(§15.1 bgbox) 자체는 무결.

### ch1_sec16_lcopeak.tex (전문 정독 완료, 68행)

구본(67행) 대비 신본 신설: **L52–53 U7 anchor 인용 문장**("세 전위 창의 실측 계보는 표 anchor 문헌\cite{xia2007,reynier2004,motohashi2009} 그대로다"). 원장 A 유효키 3종. L62–64 "∂U_1/∂T 선형 관측 신호"는 eq:U1T2 참조 有 = 모델 예측(U7 baseline "기각[확정]" 판정과 일치, 문헌 주장 아님) — 무인용 정당.

수식 검산 PASS: 전하보존 Q_cell q=Q_bg+ΣQ_j^cat ξ_j → dQ/dV=C_bg+ΣQ_j^cat dξ/dV(P2 핵심식) 정합. Bell 항등식 dξ/dV=σ_d ξ(1-ξ)/w_j 정확. peak 3관측량: V_peak=U_j^d·(dQ/dV)_max=Q_j/(4w_j)(ξ(1-ξ)|_½=¼)·면적=Q_j(∫dξ=1) 전건 정확. box eq:lco-eqpeak 정합.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 9 | ch1_sec16:57 | L | ②/① | "pure-LCO **문헌 물리**에서 세 전이 모두 Ω>2RT 두-상" — sec13(L32·L160)은 U5/U6 로 동일 개념을 "**상도표 물리**"로 정밀화했는데 sec16 은 "문헌 물리" 잔존. 형제 절 간 용어 불일치 | sec16 L57 구본 L56 과 동일(regression 아님). U5/U6 스코프는 sec13 한정이라 sec16 미전파 | (P6 스윕 후보) sec16 도 "상도표 물리"로 통일 검토 — 결함 아님·일관성 |

**가장 약한 1곳(sec16)**: L57 "문헌 물리" 잔존(#9) — sec13 정밀화가 형제 절에 미전파된 용어 drift.

### ch1_sec17_msmr.tex (전문 정독 완료, 137행 — MSMR 계보 소관)

구본(133행) 대비 신본 신설: **L6–10 MSMR 계보 3단 문단**. 구본은 L6 "MSMR 모델\cite{msmr2024}이…" 인라인 1건 → 신본은 계보 문장으로 재구성(msmr2024 유실 없이 계보 말미로 이동 + 원전·명명 2종 추가).

**계보 3단 서지 귀속 대조(축③) — 원장과 문자 일치**:
- 원전 `msmr_origin2017`: "치환 격자 열역학 모델을 Verbrugge 등이 흑연·스피넬·인산철·층상 산화물에 한 틀로" = 원장 제목("Thermodynamic Model for Substitutional Materials: …Lithiated Graphite, Spinel Manganese Oxide, Iron Phosphate, and Layered NMC") 문자 대응 ✅. 원장 주의사항("제목에 MSMR 없음")도 준수 — 명명을 이 논문에 귀속 안 함.
- 명명 `bakerverbrugge2018`: "Baker–Verbrugge 다공 전극 정식화가 multi-species, multi-reaction(MSMR) 명명" = 원장 제목("Multi-Species, Multi-Reaction Model for Porous Intercalation Electrodes: Part I") 대응 ✅.
- 온도 `msmr2024`: "엔트로피·온도 의존 파라미터화가 뒤따랐다" — bib 제목 대조는 ch1_bib 소관(하단).

수식 검산 PASS: eq:msmr(f=F/RT·무차원 ω_j) 표준 MSMR 정합. 재모수화(F/RT→폭 흡수·f=±1)·w_j=n_jRT/F 동형 정합. 여집합 항등식·f=+σ_d 유일해(계수비교 f/ω_j=σ_d/w_j) 정확. "함수형 동형≠물리량 동일" 가드(직접 등치 시 f=-σ_d) 정확. eq:lco-xmap(ξ=0↔x=0.94·ξ=1↔x=0.75·ξ=½↔x=0.845=x_MIT) 정합. **고정점 순환 처리**: ξ_eq,1↔U_1 순환을 명시·동결 근사는 무순환·정밀형 1회 갱신, 되먹임 |ΔS_e^mol|/F×30K=0.47mV/K×30=14mV≲w_1 재확인 — self-consistent loop 진단 완결(P3 gate 3·4 취지 충족).

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 10 | ch1_sec17:10 | ~~L~~→해소 | ③ | msmr2024 "엔트로피·온도 의존 파라미터화" 특성화 — **ch1_bib 제목 확인으로 정확 확인**: bib 신본 제목 "Quantifying the **Temperature Dependence** of the Multi-Species, Multi-Reaction Model. Part 1: Parameterization…" = 온도 의존 파라미터화 문자 부합 | ch1_bib L31 msmr2024 제목(C-004 정정판) | **해소(결함 아님)** — 계보 3단 온도단 귀속 정확 |

**가장 약한 1곳(sec17)**: 계보 3단·유도·고정점 처리 전건 통과. 최약은 msmr2024 특성화(#10)였으나 bib 대조로 해소 — 잔여 최약 없음(L급: L6 인라인 "MSMR 모델" 무인용→계보문이 즉시 인용 회수, 문제 아님).

### ch1_sec18_inputs.tex (전문 정독 완료, 69행)

구본(69행)과 신본 **byte 동일**(무변경). regression 없음. tab:nodemap N5+ (ΔS_e^mol=N_A(π²/3)k_B²T ∂g/∂x<0) = eq:dSemolar 정합·노드 매핑 일관. keybox 6단계는 흑연 기저곡선 재현 절차(LCO 는 N0'–N9' 확장).

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 11 | ch1_sec18:16–22 | L | ① | keybox "한 곡선 재현(6단계)"는 흑연 tab:staging 4전이 기준 절차만 서술 — LCO 3전이+전자항 재현 절차는 tab:nodemap 으로 분리(keybox 자체엔 LCO 언급 없음) | 무변경 자산·node 표가 LCO 담당. 결함 아님 | (선택) keybox 말미 "LCO 는 N0'–N9'" 한 줄 참조 — 불요 |

**가장 약한 1곳(sec18)**: keybox 가 흑연 전용(#11) — node 표가 LCO 를 담아 결함 아님. 빈 통과 방지 L급.

### ch1_bib.tex (전문 정독 완료, 46행 / 36 bibitem)

구본(28 bibitem, 헤더 stale "24종") 대비 신본 36 bibitem·헤더 "36종". **추가 8종**: P2 ashcroftmermin1976(C-009)·P3 dreyer2011(C-010)·**P4 신규 6종**(mott1968·imada1998·marianetti2004·vanderven1998·msmr_origin2017·bakerverbrugge2018 = C-011~016). 구본 28종 전건 신본에 보존(유실 0).

**P4 신규 6종 원장 문자 대조(축③) — 전건 EXACT 일치**:
| key | 위치 | 저자·제목·저널·권·쪽·연·DOI vs 원장 | 판정 |
|---|---|---|---|
| mott1968 | L21 | RMP 40, 677–683 (1968)·10.1103/RevModPhys.40.677 | ✅ char 일치 |
| imada1998 | L22 | RMP 70, 1039–1263 (1998)·10.1103/RevModPhys.70.1039 | ✅ |
| marianetti2004 | L23 | Nat. Mater. 3, 627–631 (2004)·10.1038/nmat1178·"Li 빈자리 정공 불순물 준위 Mott" 주석 | ✅ |
| vanderven1998 | L20 | PRB 58, 2975–2987 (1998)·10.1103/PhysRevB.58.2975 | ✅ |
| msmr_origin2017 | L29 | JES 164(11), E3243–E3253 (2017)·10.1149/2.0341708jes·"제목에 MSMR 없음·byline 이니셜 없음" 주석(원장 주의 준수) | ✅ |
| bakerverbrugge2018 | L30 | JES 165(16), A3952–A3964 (2018)·10.1149/2.0771816jes·"MSMR 명명 원전" 주석 | ✅ |

**서지정정 regression 대조(구본→신본)**: 모두 CHANGE_LOG 대응 — ohzuku1993 제목 전문복원(C-003)·leviaurbach1999 제목 Frumkin 리뷰 교체·167–185(C-002)·**ml2024 저자순서 Teichert→Faghih Shojaei 제1·105727→105726·DOI …105727→…105726(C-001 — 구 DOI 가 실재 타논문 지목 위험 정정)**·msmr2024 제목 출판표기(Part 1·(MSMR) 제거)·Part II 171(10) 103505 보완(C-004)·헤더 24→36+원장 참조(C-008). 무단 변경·유실 없음.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| 12 | ch1_bib(전역) | — | ③ | 신규 6종 char-EXACT·구본 28종 보존·변경 전건 CHANGE_LOG 대응 — **독립 결함 없음**. 잔여 이슈는 bib 자체 아니라 인용처 sec15 L241(#7) | 상단 대조표 | bib clean pass |

**가장 약한 1곳(ch1_bib)**: bib 필드 자체는 무결(6종 char 일치·정정 전건 로그 대응). 최약은 bib 밖 인용처(#7 sec15 L241) — bib 소관 아님.

---

## 웹 재확인 종합 (독립 1차 대조)
- **ml2024**(arXiv 2302.08991 / ScienceDirect S0022509624001923 초록): "first-principles statistical mechanics → continuum phase-field, **order–disorder transitions in Li_xCoO₂**", **configurational free energy only** — 전자 엔트로피·MIT·vib 스코프 밖. ⇒ sec13 OD 계보 귀속 **정확**(#4 해소), sec15 L241 MIT-전자 tier-A 귀속 **스코프 불일치 확정**(#7·M).
- **msmr2024**(ch1_bib 제목·C-004): "Quantifying the **Temperature Dependence** of MSMR Model. Part 1" ⇒ sec17 온도단 특성화 **정확**(#10 해소).
- 6 신규 bib 필드: 원장(master 7건 spot-check 포함)과 char 일치 — 독립 재대조로도 서지 형식 무모순.

---

## REVIEW COMPLETE — 발견 총 12건 (H 0 / M 2 / L 8 / 해소·무결 2)

- **H(물리·수식 오귀속) 0건.** LCO 청크 전 유도(평형중심 이중경로·spinodal/gap/Taylor·엔트로피 삼분해·Sommerfeld C_e/S_e 이중경로·게이트 닫힌식·MSMR f=+σ_d·고정점 순환)·수치(−46 J/(mol K) 3중검산·1.1 k_B/atom 항등·80 J/(mol K)·14mV≲w_1) 전건 재유도·검산 PASS.
- **M 2건**: #6(sec14 config⊥elec 직교 ↔ §15.1 불순물-Mott 결합 정합 seam·연결문 부재·양쪽 hedge), #7(sec15 L241 ml2024 order–disorder 논문을 MIT-전자 불충분 tier-A 근거로 인용 = 스코프 불일치·웹 확인·**pre-existing**).
- **L 8건**: #1 sec11 xia2007 단건·#2 sec11 MSMR 명명원전 preview 미포함(§17서 처리)·#3 sec12 verifybox 교차층위 밀도·#5 sec13 charge-order motohashi tier-A(구본 동일)·#8 sec15 Mott "부분적" 뉘앙스·#9 sec16 "문헌물리" 용어 drift·#11 sec18 keybox 흑연전용·#12 ch1_bib clean(무결 명시).
- **해소 2건**: #4·#10 (웹/bib 대조로 정확 확인).
- **하드 가드 3항(§15.1 MIT bgbox) 전건 충족**·U·t↔U_j 인라인 가드 충족·B-004 구본 §15.1 내용요소 전건 보존/개선·§15.2–15.5 verbatim·신규 6종 bib char 일치·U5~U8·U11 처리 확인.
- **regression 0건**: sec14·sec18 byte 동일, 나머지 변경 전건 CHANGE_LOG(C·B) 또는 baseline(U) 의도 대응, 자산 주석 불변.

## 가장 약한 1곳 (담당 청크 전체)
**#7 — ch1_sec15:241** `\cite{ml2024}(tier A)` 를 "config 단독으로는 MIT 2상역 엔트로피 거동 재현 못함" 주장에 부여. 웹 확인 결과 ml2024 는 **순수 배치(order–disorder) 스케일브리징 논문으로 전자 엔트로피·MIT 를 다루지 않음** — 즉 T2/T3(order–disorder, x≈0.5) 소관 문헌을 T1(MIT, x≈0.85) 전자 엔트로피 불충분의 tier-A 근거로 쓴 스코프 불일치 인용. 주장 자체("전자항 없으면 MIT 못 그림")는 문서 내 유도로 참이나, 그 tier-A 서지 근거로 ml2024 는 부적합. **단 §15.2–15.5 는 v1.0.19 verbatim 이라 이 창의 P4 신설분(§15.1 bgbox·계보·bib) 무결성과는 별개의 pre-existing 항목**이며, 신설분 자체는 하드 가드·유도·서지 전건 통과.
(차약 = #6 §14↔§15.1 직교/불순물-결합 정합 seam — 연결 문장 1개 추가로 해소 가능·물리 오류 아님.)



