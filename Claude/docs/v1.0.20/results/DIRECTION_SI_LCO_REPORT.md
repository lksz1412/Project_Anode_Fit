# DIRECTION_SI_LCO_REPORT — 실리콘(Si) 이론 접목 + LCO 심화 방향성 조사 (v1.0.21 기획 Q1, 읽기 전용)

> 담당: v1.0.21 기획 조사 Q1 — **Si 계열 음극의 이론적 접목** + **LCO 심화**. **읽기 전용 — 문건·코드 무수정.** 웹 검증 의무(기억 기반 서지 0).
> 배경(사용자 요청): "LCO 로의 확장, 그리고 전혀 다른 거동을 보이는 실리콘 계열의 이론적 접목." 확장은 **v1.0.21** 에서 진행(원본 v1.0.20 보존). 본 조사가 v1.0.21 마스터플랜 v2(Q6 LCO 장·Q7 Si 장)의 입력.
> 실집행 제안은 전부 **v1.0.21 소관** — 본 보고서는 조사·후보 제시까지이며 실수정은 사용자 GO 후 v1.0.21 에서만.
> 작성 진행: 과제 완료 시마다 즉시 append(조기 저장). 구조: §1 Si 사실 · §2 이론 계보 · §3 노드 매핑표 · §4 아키텍처 권고 · §5 LCO 심화 · §6 신규 서지 원장 후보 · §7 Q6/Q7 세부 계획 초안 · §8 사용자 결정 요청.

---

## 조사 전제 — 읽은 골격과 노드 사슬 확정

**정독한 v1.0.20 골격(읽기 전용):** ch1_sec00(N0~N9 사슬)·sec01(N0·N1)·sec03(N2 중심)·sec04(N3 히스/정규용액 spinodal)·sec05(N4 폭·N5 ξ_eq/Eyring)·sec06(N6 평형 peak)·sec07(N7 broadening 3출처)·sec11(전극-중립 골격·LCO 매핑)·sec13(LCO 히스/MIT 2상)·sec15(LCO 전자 엔트로피 MIT 게이트)·ch2_sec05(eq:implicit 전하보존 음함수)·ch2_sec08(종합식·worked example)·코드 Anode_Fit_v1.0.20.py(solve_U_oc·entropy_coefficient·MIT 게이트 seam)·results/V1020_REFERENCE_LEDGER·DIRECTION_STATMECH/GENERAL_REPORT·TRIAGE_P7·INTERCHAPTER_REPORT.

**노드 사슬(ch1_sec00 fig:spine 확인):**
| 노드 | 역할 | 기준식 | 전이 루프 |
|---|---|---|---|
| N0 조건 | 실험조건→모델 입력 | σ_d(방전+1/충전−1), \|I\|=c_rate·Q_cell (eq:n0map) | 루프 前 1회 |
| N1 분극 | 측정→내부 전위 | V_n=V_app−σ_d\|I\|R_n (eq:vn) | 루프 前 1회 |
| N2 평형 중심 | 열역학 중심 | U_j(T)=(−ΔH_rxn+TΔS_rxn)/F (eq:Uj) | 전이별 |
| N3 히스테리시스 | 정규용액 이중웰 분기 | ΔU_j^hys=(2/F)[Ω_j u_j−2RT·artanh u_j], u_j=√(1−2RT/Ω_j) (eq:dUhys); U_j^d=U_j+½σ_d h_η γ_j ΔU_j^hys (eq:Ubranch) | 전이별 |
| N4 폭 | 폭 척도 | w_j=n_j RT/F (eq:wbase) | 전이별 |
| N5 평형 종 | logistic 진행률 | ξ_eq=1/(1+exp[−σ_d(V−U_j^d)/w_j]) (eq:xieq) — Eyring detailed balance 정지점 | 전이별 |
| N6 peak | 평형 peak | (dQ/dV)_j^eq=Q_j·ξ(1−ξ)/w_j (eq:eqpeak), \|I\|→0 기준선 | 전이별 |
| N7 broadening | 두-상 델타→종 | 3출처: ①유한율속 꼬리(L_V,\|I\|→0 소멸)·②내재 RT/F 폭·③앙상블 η 산포 ρ(U_app), forward 평균(eq:ensavg) | 전이별 |
| N8 지연 | 인과 꼬리 | L_V∝\|I\|, (ξ_eq−ξ_lag)/L_V (eq:lag) | 전이별 |
| N9 합성 | 배경+합산·전하보존 | C_bg+Σ_j Q_j[·]_j; **전하보존 음함수 Σ_j Q_j ξ_eq,j(U_oc,T)=Q·x̄ (eq:implicit)** 가 내부 전위 결정 | 루프 後 1회 |

**중복 방지 확인:** DIRECTION_STATMECH_REPORT(통계역학 축)·DIRECTION_GENERAL_REPORT(worked example·가독성 축)·INTERCHAPTER_REPORT(기호 인계) 전건에 **Si 언급 0·Si 확장 제안 0**. LCO 확장 제안도 0(이 셋은 기존 v1.0.20 다듬기 축). 따라서 본 보고서의 Si·LCO 확장 제안은 **기존 방향 보고서와 중복 없음**. (겹치는 유일 접점 = GENERAL (iv-1) "Ch1 흑연 worked example" 과 본 §5 "LCO worked example" — 둘은 전극이 달라 대칭 보완 관계이지 중복 아님.)

---

## §1. Si 거동의 핵심 사실 정리 (각 사실 = 검증된 1차 문헌)

> 전 서지 WebSearch 로 실재·DOI 확인(기억 기반 0). 서지 상세·tier 는 §6 원장 후보에 재수록. tier 범례(본 문건 전역): **A**=1차 문헌 정량 확정값 · **B**=대표/부분 anchor 또는 2차 경유 · **C**=추정/placeholder.

| # | Si 핵심 사실 | 검증 1차 문헌 [DOI] | 흑연 골격 대비 함의 |
|---|---|---|---|
| S1 | **합금화 반응 · 평형 Li-Si 상.** 고온(415°C) 평형 coulometric titration 은 4개 중간상 Li₁₂Si₇·Li₇Si₃·Li₁₃Si₄·Li₂₂Si₅ 를 (좁은 균질역의) 계단 plateau 로 보인다. 삽입(intercalation)이 아니라 **합금화(alloying)** — 호스트 격자가 재구성된다. | Wen & Huggins 1981, *J. Solid State Chem.* 37(3), 271–278 [10.1016/0022-4596(81)90487-4] | 흑연 staging(고정 갤러리 자리)과 근본적으로 다름 — "동등한 자리 점유" 가정(N2·N5 의 격자기체 전제)이 상온 Si 에서 붕괴. |
| S2 | **1차 리튬화 = c-Si→a-Li_xSi 두-상 이동 전선.** 상온에서 결정질 Si 는 첫 리튬화 시 **전기화학적 고상 비정질화**로 비정질 Li_xSi 로 바뀌며, 반응은 원 결정질 코어와 비정질 껍질 사이 **날카로운 이동 경계(core–shell moving boundary)**로 진행(intra-particle 2상). | Limthongkul et al. 2003, *Acta Mater.* 51(4), 1103 [10.1016/S1359-6454(02)00515-4] · Li & Dahn 2007, *J. Electrochem. Soc.* 154(3), A156–A161 [10.1149/1.2409862] · Liu et al. 2012, *ACS Nano* 6(2), 1522–1531 [10.1021/nn204476h] | 흑연 N7 의 두-상은 **inter-particle 순차 전환(Dreyer)** — Si 는 **intra-particle 코어-쉘**. 두-상 개념은 살아나나 기하·기작이 다름. |
| S3 | **첫 리튬화 끝 · Li₁₅Si₄ 준안정 결정화.** 깊이 리튬화된 a-Li_xSi 는 ~50 mV 에서 갑자기 결정질 **Li₁₅Si₄** 로 결정화(준안정상). 이후 탈리튬화는 이 상을 다시 비정질화. | Obrovac & Christensen 2004, *Electrochem. Solid-State Lett.* 7(5), A93–A96 [10.1149/1.1652421] · (in situ NMR 확증) Ogata et al. 2014, *Nat. Commun.* 5, 4217 [10.1038/ncomms4217] | dQ/dV 에 **날카로운 특징 하나**(Li₁₅Si₄ 관련) — 이것만은 흑연식 "상전이=peak" 에 부합(N6). |
| S4 | **비정질 경로의 경사 전위(sloping potential).** 첫 사이클 이후(a-Si↔a-Li_xSi)는 plateau 없는 **완만한 경사 U(x)** — 흑연·LCO 의 평탄역과 정반대. DFT 로 이 전위-조성 곡선이 재현됨(비정질 합금의 연속 고용체적 거동). | Chevrier & Dahn 2009, *J. Electrochem. Soc.* 156(6), A454–A458 [10.1149/1.3111037] · Obrovac & Chevrier 2014, *Chem. Rev.* 114(23), 11444–11502 [10.1021/cr500207g] | N2("전이별 날카로운 중심")·N6("peak") 재해석 필요 — Si dQ/dV 는 넓고 특징 적음. |
| S5 | **~300% 부피 팽창.** Li₁₅Si₄(만충) 기준 부피 변화 ~280–300%. in situ AFM/광학으로 "colossal" 가역 부피 변화 직접 측정. | Beaulieu et al. 2001, *Electrochem. Solid-State Lett.* 4(9), A137 [10.1149/1.1388178] · Obrovac & Chevrier 2014 [10.1021/cr500207g] | 흑연 ~10%·LCO ~2% 와 자릿수 차 — 기계(응력) 자유도가 전위에 직접 개입(N1·N3). |
| S6 | **큰 전위 히스테리시스(수백 mV) · 그 기계적(응력) 몫.** 충·방전 전위 갈림이 수백 mV(흑연 수십 mV 대비 큼). in situ 응력 측정: 리튬화 시 압축, 탈리튬화 시 인장으로 **소성 유동(~−1.75 GPa)**, 그리고 **응력-전위 결합 ~100–120 mV/GPa** 직접 측정 — 히스테리시스의 상당 몫이 **기계적**(응력·소성 소산)이며 정규용액 이중웰이 아니다. | Sethuraman, Chon, Shimshak, Srinivasan, Guduru 2010, *J. Power Sources* 195(15), 5062–5066 [10.1016/j.jpowsour.2010.02.013] · Sethuraman, Srinivasan, Bower, Guduru 2010, *J. Electrochem. Soc.* 157(11) [10.1149/1.3489378] | **N3 의 핵심 쟁점.** 흑연 히스=열역학 이중웰(Ω>2RT, gap≲55 mV@Ω=4RT); Si 히스=**기계적**(수백 mV) — 골격 N3 로 담기지 않음. **새 물리 필요.** |
| S7 | **율속·입자크기 의존.** 임계 입자경 **~150 nm** — 이하는 첫 리튬화 시 균열 없음, 이상은 표면 인장 hoop 응력으로 균열. 코어-쉘 2상 경계 이동이 이 크기 의존을 만든다. | Liu, Zhong, Huang, Mao, Zhu, Huang 2012, *ACS Nano* 6(2), 1522–1531 [10.1021/nn204476h] · McDowell, Lee, Nix, Cui 2013, *Adv. Mater.* 25(36), 4966–4985 [10.1002/adma.201301795] | 흑연 §7(iii) 이 **입자 사이즈 채널을 마이크론 흑연에서 정량 배제**한 것과 정반대 — Si 는 사이즈가 1차 인자. broadening 범위 규정(N7 scope)이 Si 에서 뒤집힘. |
| S8 | **첫 사이클 a-Si 조차 두-상.** 비정질 Si 나노구는 첫 리튬화 시에도 날카로운 상경계(a-Si / a-Li_{~2.5}Si)를 보이는 **두-상** 거동(이후 사이클은 solid-solution 경사). in situ TEM 직접 관측. | Wang et al. 2013, *Nano Lett.* 13(2), 709–715 [10.1021/nl304379k] · McDowell et al. 2013, *Nano Lett.* 13(2), 758–764 [10.1021/nl3044508] | 두-상↔경사 전이가 사이클·조성에 의존 — 단일 "전이 집합" 정의가 조건 의존. |

**§1 소결 — Si 가 흑연 골격에 던지는 네 물음:**
1. **전이 집합의 정체**(S1·S4): staging 부재·연속 경사 → N2 의 "전이별 날카로운 중심 U_j" 는 무엇인가? (다전이 logistic 합의 유효성 = §3 N2·N5.)
2. **히스테리시스 기원**(S6): 정규용액 이중웰(Ω)이 아니라 **응력+소성 소산+비정질 경로 비대칭** → N3 의 Ω 프레임 지위 붕괴, 새 기계 항 필요.
3. **폭·broadening 재해석**(S4·S7): RT/F 열적 폭이 아니라 합금 조성폭이 지배, 사이즈 채널이 배제 아니라 지배.
4. **골격 최강 자산의 생존**(S 전건): 전하보존식(eq:implicit)의 전극-중립성은 Si 에서도 살아남는가? → **§3 N9 에서 YES 확인**(합금 반쪽전지도 전하보존 성립; Verbrugge–Baker MSMR-Si 가 실증).

---

## §2. 이론 계보 조사 (전건 웹 검증 서지 — DOI 확인)

> 각 문헌: [서지 확정 필드 · 무엇을 주는가 · tier]. **전건 WebSearch 실재·DOI 확인 완료.** 골격 접목 관점에서 "무엇을 주는가" 를 노드로 명시.

### (계보 A) 열역학·상 — Wen-Huggins → Obrovac-Chevrier
- **Wen & Huggins 1981** [*J. Solid State Chem.* 37(3), 271–278; 10.1016/0022-4596(81)90487-4] — 고온 평형 Li-Si 상도표(4 중간상). **무엇을 주는가:** N2 의 "평형 참조" 앵커(단 고온 결정상; 상온 비정질 경로와 구분해야 함). **tier A**(원 측정).
- **Obrovac & Chevrier 2014** [*Chem. Rev.* 114(23), 11444–11502; 10.1021/cr500207g] — 합금 음극 종합 리뷰(Si·Sn 등, 부피변화·Li₁₅Si₄·경사전위·히스 총람). **무엇을 주는가:** §1 전 사실의 리뷰 앵커(리뷰라 개별 정량은 원전 병기 필요, tier B). **tier B**(리뷰).

### (계보 B) 제일원리 전위-조성 곡선 — Chevrier–Dahn (task 지목)
- **Chevrier & Dahn 2009** [*J. Electrochem. Soc.* 156(6), A454–A458; 10.1149/1.3111037] — DFT 로 비정질 Si 리튬화의 전위-조성 곡선·부피변화 재현. **무엇을 주는가:** N2("전이 중심")의 대체 = **연속 U(x) 의 미시 근거**. 흑연의 "전이별 ΔH_rxn/ΔS_rxn" 대신 조성 연속 자유에너지를 준다. **tier A**(계산, 실측 정합).

### (계보 C) 응력-전위 결합 실측 — Sethuraman 등 (task 지목, N3 핵심)
- **Sethuraman, Chon, Shimshak, Srinivasan, Guduru 2010** [*J. Power Sources* 195(15), 5062–5066; 10.1016/j.jpowsour.2010.02.013] — 박막 Si 응력 진화 in situ(소성 유동 ~−1.75 GPa). **tier A**.
- **Sethuraman, Srinivasan, Bower, Guduru 2010** [*J. Electrochem. Soc.* 157(11); 10.1149/1.3489378] — **응력-전위 결합 ~100–120 mV/GPa** 직접 측정. **무엇을 주는가:** **N3 의 새 물리** — 전위에 더해지는 기계 항 ∂U/∂σ_h(정규용액 Ω 이중웰이 못 주는 수백 mV 히스의 실측 근거). **tier A**. (쪽번호 최종 대조 필요 — §6.)

### (계보 D) 기계-전기화학(chemo-mechanics) — Cui/McDowell (task 지목)
- **McDowell, Lee, Nix, Cui 2013** [*Adv. Mater.* 25(36), 4966–4985; 10.1002/adma.201301795] — 25주년 리뷰(구조·부피·응력·파괴). **tier B**(리뷰).
- **Liu et al. 2012** [*ACS Nano* 6(2), 1522–1531; 10.1021/nn204476h] — 크기 의존 파괴(임계 ~150 nm)·코어-쉘 2상. **tier A**.
- **Wang et al. 2013** [*Nano Lett.* 13(2), 709–715; 10.1021/nl304379k] · **McDowell et al. 2013** [*Nano Lett.* 13(2), 758–764; 10.1021/nl3044508] — a-Si 두-상 in situ TEM. **tier A**. **무엇을 주는가:** N7 의 두-상 기작(intra-particle 코어-쉘)·N8 의 사이즈 의존 kinetics.

### (계보 E) 합금 전극 열역학·MSMR 적용 — Verbrugge–Baker 계열 (task 지목, N9 최강 자산 실증)
- **Verbrugge, Baker, Xiao, Zhang, Cheng 2015** [*J. Phys. Chem. C* 119(10), 5341–5349; 10.1021/jp512585z] — 대부피변화 전극의 실험·이론 특성화, Li-Si 적용(비가역 열역학 기반 확산·전하전달). **tier A**.
- **Verbrugge, Baker, Xiao 2016** [*J. Electrochem. Soc.* 163(2), A262–A271; 10.1149/2.0581602jes] — **Li-Si 전극의 다중 전기화학 반응·speciation formulation**(MSMR 계열의 Si 확장). **무엇을 주는가:** **N9 의 전하보존·다반응 합산 구조가 Si 합금에도 성립함을 실증** — 골격 최강 자산(전극-중립 eq:implicit)의 Si 대응. 기존 원장의 msmr_origin2017·bakerverbrugge2018 과 **동일 저자 계보** → 인용 연속성 확보. **tier A**.

### (계보 F) Si dQ/dV·히스테리시스 현상 모델 — 최근접 선행연구
- **Jiang, Offer, Jiang, Marinescu, Wang 2020** [*J. Electrochem. Soc.* 167(13), 130533; 10.1149/1945-7111/abbbba] — **Si 전압 히스테리시스 모델**(다단 상전이·결정화·비정질화 포함). **무엇을 주는가:** 본 문건 dQ/dV forward 골격의 **직접 비교 대상**(같은 문제를 다르게 푼 선행). Si 히스를 경로 분기로 현상학화 — 본 골격의 N3 대안 설계 참조. **tier A**(모델 논문).

### (계보 G) 상전이 실측 확증 — in situ NMR
- **Ogata et al. 2014** [*Nat. Commun.* 5, 4217; 10.1038/ncomms4217] — in situ ⁷Li NMR 로 Li-silicide 상전이·Li₁₅Si₄ 추적. **무엇을 주는가:** S3 의 독립 확증. **tier A**(측정; 전 저자 리스트 §6 에서 최종 대조).

### (계보 H — 미확보/추가 검증 대상, v1.0.21 에서 검증)
- **응력-조성 결합의 열역학 이론 원전(Larché–Cahn chemo-mechanics)** — Sethuraman 이 실측한 ∂U/∂σ 의 **이론 틀**(개방계 화학퍼텐셜의 응력 항). 본 조사에서 **서지 미검증 → '미확보'**. N3 새 물리를 1차 원리로 닫으려면 v1.0.21 에서 WebSearch 검증 후 등재.
- **소성 소산 히스테리시스의 정량 이론**(hysteresis loop 면적 = 소성 소산) — Jiang2020·Köbbing2024(Adv. Funct. Mater. 검색 중 등장, 미검증) 계열. **미확보** — v1.0.21 검증 대상.
- **Si 부분몰 엔트로피/∂U/∂T 실측**(LCO 대비 Si 발열/엔트로피 프로파일) — Ch2 발열 확장 연계 시 필요. 본 조사 범위 밖 → **미확보**, v1.0.21 Q7 에서 검증.

**§2 소결:** task 가 지목한 4 계보(Chevrier–Dahn·Sethuraman·Verbrugge–Baker·Cui/McDowell) **전건 실재·DOI 확인**. 특히 **Verbrugge–Baker 계보(계보 E)**가 기존 원장 저자(msmr_origin2017·bakerverbrugge2018)와 연속이라 **N9 최강 자산의 Si 대응을 같은 언어로 실증** — 접목의 이론적 교두보. 반면 **N3(히스) 의 1차원리 이론 틀은 '미확보'**(Larché–Cahn 계열 미검증) — 이것이 Si 접목의 최대 정직 공백(§4·§8).

---

## §3. 골격 노드 매핑표 (핵심 산출)

> 흑연 forward 사슬 N0~N9 를 Si 에 하나씩 대조. 판정 4범주: **[그대로 닿음]** = 식·부호 그대로 성립 · **[재해석]** = 식 형태 유지, 물리 내용/변수 의미 바뀜 · **[새 물리]** = 골격에 없는 항 필요 · **[닿지 않음]** = 대응 불가. 근거 = §1 사실(S#)·§2 계보.

| 노드 | 흑연 기준식 | Si 판정 | 무엇이 닿고 무엇이 깨지나 (근거) |
|---|---|---|---|
| **N0** 조건 | σ_d, \|I\|=c_rate·Q_cell | **[그대로 닿음]** | Si 는 흑연과 같은 저전위 음극(~0.05–0.5 V vs Li) — 탈리튬화=충전=σ_d 슬롯 +1(eq:lco-sigmaslot 규약 그대로). 전류·방향 환산 host-무관. **완전 재사용.** |
| **N1** 분극 | V_n=V_app−σ_d\|I\|R_n | **[재해석]** | IR(옴) 분극 벗기기는 성립. 그러나 벗긴 V_n 이 "순수 열역학 전위" 라는 전제가 깨짐 — Si 는 **응력-결합 전위 항**(∂U/∂σ_h~100–120 mV/GPa, S6)이 V_n 안에 남고 이는 \|I\|→0 에서도 안 사라짐(기계 히스). R_n 옴 항 외에 **기계 과전위 항** 추가 필요. |
| **N2** 평형 중심 | U_j(T)=(−ΔH_rxn+TΔS_rxn)/F | **[재해석]** (부분 [새 물리]) | **"전이 집합의 정체" 쟁점(S1·S4).** 상온 Si 는 이산 staging 대신 **연속 경사 U(x)** — "전이별 날카로운 중심" 부재. 두 길: (a) 다전이 logistic 합으로 경사 근사(MSMR-Si, Verbrugge–Baker 2016 실증 — 계보 E), (b) 연속 자유에너지 U(x)(Chevrier–Dahn, 계보 B). **∂U_j/∂T=ΔS_rxn/F 관계 자체는 생존**(합금 엔트로피). 이산 중심 대신 유효 logistic 성분/연속함수로 재해석. 단 Li₁₅Si₄ 결정화(S3)·1차 리튬화 2상(S2)만은 **진짜 이산 전이**. |
| **N3** 히스테리시스 | 정규용액 이중웰 Ω>2RT, spinodal, ΔU_j^hys≲55 mV(@Ω=4RT) | **[새 물리 필요]** ★핵심 | **Si 히스=수백 mV(S6)**, 흑연 spinodal gap 상한(~55 mV)의 **5–8배** — Ω 프레임으로 못 담음. 기원이 **기계적**(응력·소성 소산·비정질 경로 비대칭, Sethuraman 계보 C·Jiang 계보 F)이지 자유에너지 이중웰 아님. **Ω 프레임 지위:** 소수 몫으로 잔존 가능하나 **지배 항은 기계**. 새 항: 전위에 ±Δσ·(∂U/∂σ) 분기 + 소성 소산 loop. spinodal ΔU^hys 식은 비정질 Si 에 **비적용**(단 Li₁₅Si₄/1차 2상엔 부분 적용). **골격 최대 붕괴 지점.** |
| **N4** 폭 | w_j=n_j RT/F (단상=평형예측 / 두-상=현상학) | **[재해석]** | Si 경사 성분의 "폭" 은 **합금 조성폭**(수십 %)이지 RT/F 열적 폭(~26 mV) 아님 → n_j≫1(넓은 유효 전이). 폭의 이중지위(§5·§7)에서 Si 는 대부분 "현상학 자유 폭"쪽이나 그 기원이 **두-상 broadening 이 아니라 합금 열역학의 완만한 dU/dx**. RT/F 열적 broadening 은 소수 몫. |
| **N5** 평형 종 | ξ_eq=logistic (Eyring detailed balance 정지점) | **[그대로 닿음: 구조]** / **[재해석: 내용]** | **logistic 합 형식은 생존** — MSMR-Si(Verbrugge–Baker 2016)가 Si 를 logistic 반응 합으로 파라미터화(계보 E). detailed balance 유도(전기화학 구동력)는 전극-무관. **깨지는 것:** "동등한 격자 자리 점유" 미시 해석(S1, 비정질 합금엔 고정 자리 없음) → logistic 은 **미시 자리 통계가 아니라 유효 파라미터화**로 재해석(N2 와 동일 취지). |
| **N6** peak | (dQ/dV)_j^eq=Q_j ξ(1−ξ)/w_j | **[재해석]** | Si dQ/dV 는 **넓고 특징 적음**(경사전위, S4) — "상전이=날카로운 peak" 대응 약함. 실제 peak: Li₁₅Si₄ 탈리튬화(~0.43 V)·1차 리튬화 2상(S3·S2)만 뚜렷 → 이들만 흑연식 peak. 나머지는 넓은 hump. peak 문법은 유지되나 **소수의 진짜 전이에만** 날카롭게 적용. |
| **N7** broadening | 두-상 델타→종: ①꼬리 ②RT/F ③앙상블 η(inter-particle 순차, Dreyer); **사이즈 채널 배제**(마이크론 흑연) | **[부분 닿음 + 재해석]** | 두-상 broadening 틀은 **1차 리튬화·Li₁₅Si₄(S2·S8)**에 부분 적용. 그러나 (a) 기작이 **intra-particle 코어-쉘**(Dreyer inter-particle 순차와 다름), (b) **§7 의 "사이즈 채널 배제" 가 Si 에서 정반대로 뒤집힘** — 임계 ~150 nm(S7)로 사이즈가 **1차 인자**. §7(iii) 의 Gibbs–Thomson 배제 논증(마이크론 흑연 δU_PSD≪w)이 Si 에선 불성립. **scope 규정 재작성 필요.** |
| **N8** 지연 | L_V∝\|I\|, (ξ_eq−ξ_lag)/L_V, \|I\|→0 소멸 | **[그대로 닿음: 구조]** / **[확대: 내용]** | Eyring 유한율속 꼬리 = 전극-무관, 구조 생존. **확대:** Si kinetics 는 (a) 코어-쉘 반응율속(확산 아닌 계면 반응 제한, S2), (b) **응력-지연 확산**(Verbrugge–Baker 2015, 계보 E). 또 \|I\|→0 에서 **동역학 지연은 소멸하나 기계 히스는 안 소멸**(N3) — "꼬리"와 "평형 히스" 분리가 흑연보다 어려움. |
| **N9** 합성 | C_bg+Σ_j Q_j[·]_j; **전하보존 Σ_j Q_j ξ_j=Q·x̄ (eq:implicit)** | **[그대로 닿음]** ★최강 자산 | **전하보존식의 전극-중립성은 Si 에서 완전 생존.** 합금 반쪽전지도 Σ(반응 전하)=총 전하 성립 — **Verbrugge–Baker 2016(계보 E)이 Li-Si 다반응 speciation 을 정확히 이 구조로 실증.** task 예측(아마 YES) **확인 YES.** 골격의 최강 자산이 Si 로 그대로 이월 — 접목의 앵커. |

**§3 소결 — 매핑 10 노드 판정 집계:**
- **[그대로 닿음]:** N0(완전)·N9(완전, 최강 자산) — 2 노드
- **[그대로 닿음: 구조] / 내용 재해석:** N5(logistic=MSMR-Si)·N8(Eyring 꼬리) — 2 노드
- **[재해석]:** N1(응력 전위)·N2(전이 집합)·N4(폭)·N6(peak) — 4 노드
- **[새 물리 필요]:** **N3(기계 히스)** — 1 노드 ★
- **[부분 닿음 + scope 재작성]:** N7(두-상/사이즈) — 1 노드

**핵심 발견 3:**
1. **최강 자산 생존(N9).** 전하보존 eq:implicit 의 전극-중립성이 Si 합금에서도 성립하며 Verbrugge–Baker 2016 이 같은 언어로 실증 — **접목의 이론적 앵커는 확보**.
2. **최대 붕괴 지점(N3).** 히스테리시스 기원이 열역학 이중웰(Ω)→기계(응력/소성)로 근본 전환. 골격에 **없는 항**이 필요하고 그 1차원리 이론 틀은 현재 **'미확보'**(§2 계보 H).
3. **비대칭 사이즈 규정(N7).** 흑연이 "배제" 한 입자-사이즈 채널이 Si 에선 지배 — §7 scope 논증이 정반대로 뒤집힘.

**LCO 대비 Si 의 접목 난도(왜 LCO 는 쉬웠고 Si 는 어려운가):** LCO Part II 는 N1~N5 를 **한 식도 안 바꾸고**(전자 엔트로피 항 1개만 추가) 걸렸다(sec11). Si 는 N3 에 새 물리, N1·N2·N4·N6 재해석, N7 scope 재작성 — **골격 재사용률이 LCO 보다 현저히 낮다.** 이 비대칭이 §4 아키텍처 권고의 결정 근거다.

---

## §4. 접목 아키텍처 옵션 비교 및 권고

> 3 옵션: (i) Ch1 Part III · (ii) 독립 Chapter 3 · (iii) 예비 부록. 각 [분량·위험·골격 재사용률·정직 공백 처리].

| 옵션 | 분량 | 위험 | 골격 재사용률 | 정직 공백 처리 | 종합 |
|---|---|---|---|---|---|
| **(i) Ch1 Part III** (LCO Part II 처럼 흑연 챕터 내 3번째 전극) | 대(§11~17 급 7~10절) | **높음** | 중(N0/N9 완전·N5/N8 구조; N1/N2/N4/N6 재해석·N3 새물리) | **위험** — Ch1 안에 넣으면 "흑연·LCO 와 동급 유도 완결" 인상. Si 는 N3 기계항이 **1차원리 미유도('미확보')** 라 동급 rigor 위장 위험. LCO 는 N1~N5 무변경이었기에 Part II 가 정당했으나 Si 는 그 전제 불성립. | **비권장** |
| **(ii) 독립 Chapter 3** (Si 전용 챕터, 골격 명시 재사용 + 새 N3′) | 대(자기완결 1챕터) | 중 | 높음(명시적 재사용 선언 가능) | **최선(장기)** — 새 챕터라 "Si 는 골격 N0/N5/N8/N9 를 재사용하되 N3 는 기계항으로 교체" 를 정직하게 선언·유도 가능. 단 N3 기계 이론틀 검증(계보 H)·Si 데이터가 선행돼야 완결. | **장기 목표** |
| **(iii) 예비 부록** (노드 매핑표 + 전극-중립 재사용 실증 + 정직 공백 선언) | 소~중(1 부록, §3 표 + Verbrugge–Baker 다리 + 공백 목록) | **낮음** | — (재사용 "지도" 제시, 완결 유도 없음) | **최선(v1.0.21)** — 무엇이 이월되고(N0/N9) 무엇이 새 물리인지(N3) 정직 표로 선언. Li₁₅Si₄/1차 2상만 기존 N6/N7 로 시연. **rigor 위장 없이** 접목의 교두보 확보. | **v1.0.21 권장** |

**권고 = (iii) → (ii) 단계적.** **v1.0.21 은 (iii) 예비 부록**으로:
1. §3 노드 매핑표를 문건에 정식 수록(무엇이 전극-중립인가 = sec11 (1)~(5) 의 Si 확장).
2. **N9 전하보존 최강 자산의 Si 생존을 Verbrugge–Baker 2016 으로 실증**(1 절) — 접목의 앵커를 정직하게 못박음.
3. **N3 기계 히스를 '골격 밖 새 물리·1차원리 미확보' 로 명시 선언**(Gn 공백 방식 — 기존 문건의 G1~G3 공백 선언 관행 그대로).
4. Li₁₅Si₄ 결정화·1차 리튬화 2상만 **기존 N6/N7 로 시연**(진짜 이산 전이 = 골격 부분 적용 실증).

그 뒤 **N3 기계 이론틀 검증(계보 H)·Si 실측 데이터 확보 후 (ii) 독립 Chapter 3 로 승격.** 이 단계화는 문건의 "초기값→피팅·tier·Gn 공백" 정직 문화와 정합하며, (i) 의 rigor 위장 위험을 피한다.

**왜 (i) 아닌가(명시):** LCO 가 Part II 로 정당했던 유일 근거는 "N1~N5 무변경 + 항 1개 추가"(sec11) 였다. Si 는 이 전제가 **N3 에서 붕괴** — Ch1 안에 넣으면 흑연·LCO 와 동급 완결로 오독된다. 접목의 정직성이 아키텍처를 (iii)/(ii)로 민다.

---

## §5. LCO 심화 항목 확정

> 각 항목 [필요성·분량·위험·우선순위]. 출처: P4 이월 3건(RESULT_P4_lco "이월 3건")·TRIAGE_P7 §B(★=P8 HANDOVER 추가후보)·INTERCHAPTER §e(LCO 소관).

### ★ 코드 게이트 경로 지원 여부 — 확인 결과 **YES(지원됨)**
task 지목 확인 항목. Anode_Fit_v1.0.20.py 정독 결과 LCO worked example(∂U/∂T 한 점, MIT 게이트 포함) **계산 경로 전건 구현됨**:
- `solve_U_oc(x_bar, T)` (L711~) — 전하보존 음함수 eq:implicit 유일근 솔버(이분법).
- `entropy_coefficient(V_n, T)` (L634~) — ∂U_oc/∂T 완전식(eq:complete), `_effective_dS_rxn` seam 경유.
- `LCOCathodeDQDV._effective_dS_rxn` (L918~) — LCO 서브클래스가 MIT 전이('electronic')에 전자항 ΔS_e 가산.
- `func_dSe_molar` / `_electronic_dS_e` (L172~) — MIT 게이트 eq:dSegate, 게이트 중심 골 깊이 ≈ −45.7 J/(mol·K)(§15 검증값 −46 정합).
- `LCO_MSMR_LIT` (L868~) — T1(electronic:True, x_MIT=0.85, g_max_eV=13, dx_MIT=0.05)·T2·T3 데이터셋.

**단서(정직 표기 필수):** ① `LCO_MSMR_LIT` 는 **tier-C 시연 데이터셋**(round-trip 피팅 前 placeholder) → worked example 도 흑연판(tab:worked, staging 초기값)처럼 **tier-C 시연**으로 못박아야. ② 전자항이 코드에서 **T_ref 동결 상수 오프셋**(단일-기준 근사) — 단일 온도 ∂U/∂T 시연엔 충분하나 다온도 T² 곡률은 항목 3(T-복원)에 위임. **결론: 게이트 경로 지원 확인, worked example 즉시 계산 가능(tier-C 시연 표기 하에).**

### LCO 심화 항목표
| # | 항목 | 출처 | 필요성 | 분량 | 위험 | 우선순위 |
|---|---|---|---|---|---|---|
| L1 | **LCO worked example** — Ch2 §2.8 흑연판(tab:worked)의 LCO 대응. 한 x̄·한 T 에서 solve_U_oc→ξ_j→∂U/∂T 완주, **MIT 게이트 ∂S_e 골이 ∂U/∂T 에 들어가는 한 점 시연**(전이별 미니표). | 코드 확인(위)·GENERAL (iv-1) 대칭 | **높음** — Ch2 는 흑연 worked example 보유·LCO 미보유. MIT 전자항의 수치 감각(작지만 필수)을 한 점으로 실증. 문건 최강 신규성(MIT 게이트)의 이해 장치. | ~15–20행 + 미니표 | 낮음(코드 회귀값 대응). 단 **tier-C 시연·T_ref 동결 근사 명시 필수** | **높음(1순위)** |
| L2 | **tier 실측 앵커 강화** (LCO tier-2/3 실측) | P4 이월 | 중~높음 — 현행 LCO U_j/ΔS 는 tier-C 초기값(Xia/Reynier/Motohashi 경유 tier B). 1차 실측 OCV/엔트로피 앵커로 승격이 정직 문화에 부합. | 원장 추가 + tab:lco-staging 갱신(수식 무변경) | 낮음. 단 실측 데이터·round-trip 은 실집행 소관 | 중 |
| L3 | **다온도 T-복원** (∂S_e∝T·eq:U1T2 T² 곡률) | P4 이월 | 중 — 전자항 식별 신호(∂U/∂T 가 T 선형·U 이동 T²). 현행 코드 T_ref 동결 근사 해제. | 코드(seam T-의존화) + §15/§2.8 note | 중(다온도 데이터 round-trip 필요, "미구현" 라벨) | 중(피팅 단계 연동) |
| L4 | **q_irr(비가역 발열)** — 히스 gap ΔU^hys∝I 소산, ∂U/∂T(가역)와 별개 | P4 이월·Ch2 §2.5 warnbox(범위밖 선언) | 낮~중 | 신설 소절 | 중(경로의존 측정 불확실도 정량) | 낮 |
| L5 | **O3-#5: charge-order ΔS 값(T2/T3) 1차 원전 재확인** — 0.47/1.49 J/(mol·K)@x=½,⅔ 슬롯 배정 tier C(조성창 불일치) → 원전 재확인 후 tier 승격 | TRIAGE_P7 §B(★) | 중 — 정량값 tier 명료화 | 검증 + 원장/각주 | 낮 | 중 |
| L6 | **M-1: ΔS⁰_j 스코프 명시** — Ch1 §14 config-슬롯 중심 vs Ch2 §2.2 전체 중심(LCO 교차독해 시 혼동) | INTERCHAPTER §e M-1 | 낮~중 | 1문장(다리) | 낮(표현층) | 낮~중 |
| L7 | **L-5: θ_E 지칭 정정** — Ch1 §14·appB "Ch2 vibrational 절"→"Ch2 §2.4 Einstein 절" ×3 | INTERCHAPTER §e L-5·TRIAGE T-09 관련 | 낮(참조 정밀도) | 3곳 | 낮 | 낮 |

**§5 소결:** LCO 심화의 최우선은 **L1(worked example)** — 코드 지원 확인됨·이해 이득 최고·GENERAL 흑연 worked example 과 대칭. 그다음 **L2·L3·L5**(tier·T-복원·원전 재확인, 데이터/검증 연동). L4·L6·L7 은 저우선(범위·표현층). **주의:** 이 항목들은 v1.0.21 에서 **Si 확장(Q7)과 별개 트랙(Q6)** — Si 가 골격을 흔드는 반면 LCO 는 이미 걸린 골격의 심화·정직성 강화라 위험도가 훨씬 낮다.

---

## §6. 신규 서지 원장 등재 후보 일람 (V1 후보 — 필드 완비)

> V1020_REFERENCE_LEDGER 형식. **전건 WebSearch 실재·DOI 확인.** 기존 원장 42(기존)+12(신규)+5(appendix) 와 **키 충돌 없음**(신규 si_* / lco_* prefix). "★확인필요" = search 가 명시 안 준 필드(등재/피팅 시 Crossref 최종 대조) — 기억 기반 채움 금지 원칙 준수.

### A. Si 계열 (v1.0.21 Q7 예정 — 등재는 첫 인용 phase)
| key(제안) | 확정 서지 | DOI | tier | 예정 사용(노드) |
|---|---|---|---|---|
| wen_huggins1981 | C. J. Wen, R. A. Huggins, "Chemical diffusion in intermediate phases in the lithium-silicon system," *J. Solid State Chem.* 37(3), 271–278 (1981) | 10.1016/0022-4596(81)90487-4 | A | S1 평형 Li-Si 상(N2 참조) |
| obrovac_chevrier2014 | M. N. Obrovac, V. L. Chevrier, "Alloy Negative Electrodes for Li-Ion Batteries," *Chem. Rev.* 114(23), 11444–11502 (2014) | 10.1021/cr500207g | B(리뷰) | §1 총람 앵커 |
| chevrier_dahn2009 | V. L. Chevrier, J. R. Dahn, "First Principles Model of Amorphous Silicon Lithiation," *J. Electrochem. Soc.* 156(6), A454–A458 (2009) | 10.1149/1.3111037 | A | S4 경사전위·N2 연속 U(x) |
| limthongkul2003 | P. Limthongkul, Y.-I. Jang, N. J. Dudney, Y.-M. Chiang, "Electrochemically-driven solid-state amorphization in lithium-silicon alloys and implications for lithium storage," *Acta Mater.* 51(4), 1103 (2003) | 10.1016/S1359-6454(02)00515-4 | A | S2 전기화학적 비정질화 |
| li_dahn2007 | J. Li, J. R. Dahn, "An In Situ X-Ray Diffraction Study of the Reaction of Li with Crystalline Si," *J. Electrochem. Soc.* 154(3), A156–A161 (2007) | 10.1149/1.2409862 | A | S2 결정질 Si 2상 XRD |
| obrovac_christensen2004 | M. N. Obrovac, L. Christensen, "Structural Changes in Silicon Anodes during Lithium Insertion/Extraction," *Electrochem. Solid-State Lett.* 7(5), A93–A96 (2004) | 10.1149/1.1652421 | A | S3 Li₁₅Si₄ 결정화 |
| beaulieu2001 | L. Y. Beaulieu, K. W. Eberman, R. L. Turner, L. J. Krause, J. R. Dahn, "Colossal Reversible Volume Changes in Lithium Alloys," *Electrochem. Solid-State Lett.* 4(9), A137 (2001) | 10.1149/1.1388178 | A | S5 부피 팽창 |
| sethuraman_stresspot2010 | V. A. Sethuraman, V. Srinivasan, A. F. Bower, P. R. Guduru, "In Situ Measurements of Stress-Potential Coupling in Lithiated Silicon," *J. Electrochem. Soc.* 157(11), (2010) [★쪽 A1253~ 확인필요] | 10.1149/1.3489378 | A | **S6·N3 응력-전위 결합(핵심)** |
| sethuraman_stressevo2010 | V. A. Sethuraman, M. J. Chon, M. Shimshak, V. Srinivasan, P. R. Guduru, "In situ measurements of stress evolution in silicon thin films during electrochemical lithiation and delithiation," *J. Power Sources* 195(15), 5062–5066 (2010) | 10.1016/j.jpowsour.2010.02.013 | A | S6 소성 유동(−1.75 GPa) |
| mcdowell2013 | M. T. McDowell, S. W. Lee, W. D. Nix, Y. Cui, "25th Anniversary Article: Understanding the Lithiation of Silicon and Other Alloying Anodes for Lithium-Ion Batteries," *Adv. Mater.* 25(36), 4966–4985 (2013) | 10.1002/adma.201301795 | B(리뷰) | S7 기계-전기화학 총람 |
| liu_sizefracture2012 | X. H. Liu, L. Zhong, S. Huang, S. X. Mao, T. Zhu, J. Y. Huang, "Size-Dependent Fracture of Silicon Nanoparticles During Lithiation," *ACS Nano* 6(2), 1522–1531 (2012) | 10.1021/nn204476h | A | S7 임계 ~150 nm·N7 사이즈 채널 |
| wang_twophase2013 | J. W. Wang, Y. He, F. Fan, X. H. Liu, S. Xia, Y. Liu, C. T. Harris, H. Li, J. Y. Huang, S. X. Mao, T. Zhu, "Two-Phase Electrochemical Lithiation in Amorphous Silicon," *Nano Lett.* 13(2), 709–715 (2013) | 10.1021/nl304379k | A | S8 a-Si 2상(N7) |
| mcdowell_asitem2013 | M. T. McDowell, S. W. Lee, J. T. Harris, B. A. Korgel, C. Wang, W. D. Nix, Y. Cui, "In Situ TEM of Two-Phase Lithiation of Amorphous Silicon Nanospheres," *Nano Lett.* 13(2), 758–764 (2013) | 10.1021/nl3044508 | A | S8 a-Si 2상 TEM |
| verbrugge_lisi2015 | M. W. Verbrugge, D. R. Baker, X. Xiao, Q. Zhang, Y. T. Cheng, "Experimental and Theoretical Characterization of Electrode Materials that Undergo Large Volume Changes and Application to the Lithium–Silicon System," *J. Phys. Chem. C* 119(10), 5341–5349 (2015) | 10.1021/jp512585z | A | 계보 E·N8 응력-확산 |
| verbrugge_lisi2016 | M. W. Verbrugge, D. R. Baker, X. Xiao, "Formulation for the Treatment of Multiple Electrochemical Reactions and Associated Speciation for the Lithium-Silicon Electrode," *J. Electrochem. Soc.* 163(2), A262–A271 (2016) | 10.1149/2.0581602jes | A | **N9 전하보존 Si 실증(최강 자산 앵커)** |
| jiang_sihys2020 | Y. Jiang, G. Offer, J. Jiang, M. Marinescu, H. Wang, "Voltage Hysteresis Model for Silicon Electrodes for Lithium Ion Batteries, Including Multi-Step Phase Transformations, Crystallization and Amorphization," *J. Electrochem. Soc.* 167(13), 130533 (2020) | 10.1149/1945-7111/abbbba | A(모델) | N3 최근접 선행·비교 대상 |
| ogata_nmr2014 | K. Ogata et al. [★전 저자 리스트 확인필요], "Revealing lithium-silicide phase transformations in nano-structured silicon-based lithium ion batteries via in situ NMR spectroscopy," *Nat. Commun.* 5, 4217 (2014) | 10.1038/ncomms4217 | A | S3 상전이 NMR 확증(선택) |

### B. 미확보(추가 검증 대상 — v1.0.21 Q7 에서 WebSearch 검증 후 판정)
- **Larché–Cahn chemo-mechanics 원전**(응력-조성 화학퍼텐셜 결합 이론틀) — N3 새 물리의 1차원리 근거. **미확보** — 서지 미검증, 기억 기반 등재 금지.
- **소성 소산 히스테리시스 정량 이론**(Köbbing 2024 *Adv. Funct. Mater.* 계열 — 검색 중 등장했으나 본 조사 미검증). **미확보**.
- **Si 부분몰 엔트로피/∂U/∂T 실측**(Ch2 발열 확장 연계) — **미확보**.

**§6 소결:** Si 계열 **17건 전건 검증**(DOI 확인), 기억 기반 0. 2건에 "★확인필요" 필드(등재 시 Crossref 최종 대조) 정직 표기. 미확보 3건 별도 표기(N3 이론틀 포함 — 접목 최대 공백). 기존 원장 키 충돌 없음.

---

## §7. v1.0.21 Q6/Q7 세부 계획 초안 (phase step 스케치)

> **전건 v1.0.21 소관 — 실집행은 사용자 GO 후.** 본 절은 계획 스케치이지 실행 계획서(11 sections)가 아니다. cumulative step 번호·gate 상세는 v1.0.21 계획서(`Claude/plans/2026-...-v1021-...-plan.md`)에서 확정. 검수는 P3 프로젝트 전용 7항목 준용.

### Q6 — LCO 심화 (골격 유지·정직성 강화; 저위험 트랙)
| step | 작업 | 산출 | gate(P3 준용) |
|---|---|---|---|
| Q6.1 | **L1 LCO worked example** — solve_U_oc→ξ_j→∂U/∂T 완주(MIT 게이트 ∂S_e 포함), 코드 회귀값 산출, Ch2 §2.8 LCO 대응 절(또는 §15 말미) 초안. tier-C 시연·T_ref 동결 근사 명시. | LCO worked 미니표 + ~15–20행 | 7항목 中 ①(V_n/U_oc 구분)·⑥(Ch1↔Ch2 전달식 정합)·수치정합 가드(코드 대응) |
| Q6.2 | **L2 tier 앵커 강화** — LCO tier-2/3 실측 OCV/엔트로피 서지·데이터 확보 → 원장 등재 → tab:lco-staging tier 갱신. | 원장 +N건, 표 갱신 | ⑤(ref 방법론 4항목 기록)·tier 정직 |
| Q6.3 | **L5 원전 재확인** — charge-order ΔS(0.47/1.49) 슬롯 배정 tier 명료화. | 각주/원장 정정 | ⑤·tier |
| Q6.4 | **L6·L7 표현층** — M-1 ΔS⁰_j 스코프 1문장·L-5 θ_E 지칭 ×3. | 문장/지칭 정정 | 표현층(CHANGE_LOG 불요, RESULT Files Updated 갈음) |
| Q6.5(후속) | **L3 다온도 T-복원·L4 q_irr** — 다온도 데이터 round-trip 연동(미구현 라벨 유지 가능). | 코드+절 or 공백 유지 | ②(전하보존 중심식 유지)·④(순환의존 진단) |

### Q7 — Si 접목 (골격 확장·새 물리; 고위험 트랙, 아키텍처 (iii) 예비 부록)
| step | 작업 | 산출 | gate(P3 준용) |
|---|---|---|---|
| Q7.0 | **N3 이론틀 검증(선결)** — 미확보 3건(Larché–Cahn·소성 소산·Si 엔트로피) WebSearch 검증·DOI 확인 → 원장 등재 or '미확보' 확정. | 검증 결과·원장 후보 | 기억 기반 서지 0(전역 규칙) |
| Q7.1 | **Si 서지 원장 등재** — §6 A 17건 bib 반영, ★확인필요 필드 Crossref 대조. | ch1_bib/신규 bib | ⑤ |
| Q7.2 | **노드 매핑표 부록 초안** — §3 표 정식화(sec11 전극-중립 (1)~(5) 의 Si 확장; 무엇이 이월/재해석/새물리/부분). | Si 매핑 부록 §S.1 | ⑥·⑦(ver.N↔Chapter 명칭 혼동 금지) |
| Q7.3 | **N9 최강 자산 Si 실증 절** — 전하보존 eq:implicit 의 Si 생존을 Verbrugge–Baker 2016 다리로 못박음. | 부록 §S.2 | ②(전하보존 중심식 유지 — Si 에서도)·③(순환의존 그래프) |
| Q7.4 | **N3 기계 히스 Gn 공백 선언** — '골격 밖 새 물리·1차원리 미확보' 를 G-계열 공백으로 명시(기존 G1~G3 관행). Si 히스 수백 mV vs 흑연 spinodal ≲55 mV 대비 표. | 부록 §S.3 + 공백 선언 | ④(공백 4분류: '물리 가정 충돌'·'논리 공백' 분리 진단) |
| Q7.5 | **Li₁₅Si₄/1차 2상 시연** — 진짜 이산 전이만 기존 N6/N7 로 부분 적용 실증(경사 영역은 적용 밖 명시). | 부록 §S.4 | ①·⑥ |
| Q7.6 | **검증 gate** — P3 7항목 전수(특히 ③④ 순환의존/공백, ⑤ ref 매핑, ⑦ 명칭). 빌드·구조 PASS. | RESULT + ledger | 7항목 전건 |

**중단 조건(양 트랙 공통):** (a) Q7.0 에서 N3 이론틀 3건 모두 '미확보' 확정 시 → Q7 은 **공백 선언(§S.3)까지만** 하고 새 물리 유도는 후속(ii Chapter 3)으로 이월(중단, 사용자 보고). (b) LCO L2/Si Si-데이터 실측이 없으면 → tier-C 시연 유지·round-trip 은 "데이터 확보 후" 라벨(중단 아님, 정직 표기). (c) 아키텍처가 (iii) 밖으로 확대되면(사용자가 (ii) 즉시 요구) → 재계획.

**사용자 결정 경계(집행 전 필수 확인):** 아키텍처 (iii/ii) 선택 · Si 데이터 유무 · Q6/Q7 병렬 여부 · L1 tier-C 즉시 vs 실측 대기 — §8.

---

## §8. 사용자 결정 요청

> [[feedback_decision_request_clarity]] — 각 결정 [무엇을·선택지·권고·근거]. 집행은 결정 후 v1.0.21 에서만.

**D1. Si 접목 아키텍처.** 선택지: (i) Ch1 Part III · (ii) 독립 Chapter 3 · (iii) 예비 부록.
→ **권고: (iii) 예비 부록을 v1.0.21 로, (ii) 독립 Chapter 3 를 후속으로 단계화.** 근거: Si 는 N3 에 골격-밖 새 물리(기계 히스)가 필요하고 그 1차원리 틀이 '미확보'(§2 계보 H) — (i) 는 흑연·LCO 와 동급 rigor 위장 위험. LCO 가 Part II 로 정당했던 "N1~N5 무변경" 전제가 Si 에서 붕괴(§3·§4). (iii) 는 최강 자산(N9)의 Si 생존을 정직하게 못박고 새 물리를 공백 선언 — rigor 위장 없이 교두보 확보.

**D2. N3 기계 히스 이론틀 처리.** 선택지: (a) v1.0.21 에서 미확보 3건(Larché–Cahn 등) 검증 시도 후 가능하면 1차원리 유도 · (b) 검증 실패 시 공백 선언만(§S.3).
→ **권고: (a) 검증 시도 → 실패 시 (b) 로 자동 강등.** 근거: Q7.0 선결 step 으로 두되, 실패해도 접목(공백 선언·최강 자산 실증)은 진행. 기억 기반 서지 금지 원칙상 미검증 유도는 불가.

**D3. LCO L1 worked example 데이터 지위.** 선택지: (a) tier-C 시연 데이터(LCO_MSMR_LIT)로 즉시 집행 · (b) tier-2/3 실측(L2) 확보 후 실측 기반.
→ **권고: (a) 즉시 집행(tier-C 시연 명시)** — 흑연 worked example(tab:worked, staging 초기값)과 대칭이며 이해 이득이 크다. 실측 확보 시 (b) 로 갱신(L2 연동). **단 사용자 시료에 LCO 실측 dQ/dV 가 있으면 (b) 우선.**

**D4. Si 실측 데이터 유무.** 질문: 사용자 시료/원천 자료(임시저장소·_local_only)에 **Si 또는 Si-흑연 복합 음극 dQ/dV** 가 있는가? 
→ 있으면 Q7 이 시연에서 **실측 대조**로 승격(노드 매핑 검증 가능). 없으면 Q7 은 문헌 기반 매핑·공백 선언까지(정직 표기). **본 조사는 read 안 함(_local_only 원천은 사용자 명시 시에만).**

**D5. Q6(LCO)·Q7(Si) 집행 순서.** 선택지: (a) 병렬 · (b) Q6 먼저(저위험) → Q7 · (c) Q7 먼저.
→ **권고: (b) Q6 먼저.** 근거: Q6 은 골격 유지·저위험(worked example·tier·표현층)이라 빠른 이득; Q7 은 새 물리·미확보 검증이 걸려 위험이 크다. Q6 로 LCO 장을 완결한 뒤 Q7 로 Si 를 신중히 접목.

**D6. Si 서지 등재 범위.** 선택지: (a) §6 A 17건 전건 · (b) 핵심만(N9 앵커 verbrugge_lisi2016 + S1~S8 각 1건 ~10건).
→ **권고: (b) 핵심 우선, 확장 시 (a).** 근거: 예비 부록(iii) 규모엔 핵심 10건이면 노드 매핑·공백 선언에 충분. 독립 Chapter 3(ii) 승격 시 17건 전건.

---

## 부록 — 검증한 웹 출처(주요)
- Obrovac & Christensen 2004: https://iopscience.iop.org/article/10.1149/1.1652421
- Obrovac & Chevrier 2014: https://pubs.acs.org/doi/10.1021/cr500207g
- Sethuraman (stress-potential) 2010: https://iopscience.iop.org/article/10.1149/1.3489378
- Sethuraman (stress evolution) 2010: 10.1016/j.jpowsour.2010.02.013
- Chevrier & Dahn 2009: https://iopscience.iop.org/article/10.1149/1.3111037
- McDowell/Cui 2013: https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.201301795
- Li & Dahn 2007: https://iopscience.iop.org/article/10.1149/1.2409862
- Limthongkul 2003: https://www.sciencedirect.com/science/article/abs/pii/S1359645402005141
- Liu (size fracture) 2012: https://pubs.acs.org/doi/10.1021/nn204476h
- Verbrugge–Baker (JPCC) 2015: https://pubs.acs.org/doi/abs/10.1021/jp512585z
- Verbrugge–Baker (MSMR-Si) 2016: https://iopscience.iop.org/article/10.1149/2.0581602jes
- Wen & Huggins 1981: https://www.sciencedirect.com/science/article/abs/pii/0022459681904874
- Beaulieu 2001: https://iopscience.iop.org/article/10.1149/1.1388178
- Wang (a-Si 2phase) 2013: https://pubs.acs.org/doi/10.1021/nl304379k
- McDowell (a-Si TEM) 2013: https://pubs.acs.org/doi/10.1021/nl3044508
- Jiang (Si hysteresis model) 2020: https://iopscience.iop.org/article/10.1149/1945-7111/abbbba
- Ogata (in situ NMR) 2014: https://www.nature.com/articles/ncomms4217

## REPORT COMPLETE
- **Si 문헌 17건 검증**(DOI 확인, 기억 기반 0; ★확인필요 필드 2·미확보 3 정직 표기)
- **노드 매핑 10건**(그대로 닿음 N0·N9 / 구조 생존 N5·N8 / 재해석 N1·N2·N4·N6 / 새 물리 N3 / 부분 N7)
- **최강 자산 N9(전하보존) Si 생존 확인**(Verbrugge–Baker 2016) · **최대 붕괴 N3(기계 히스, 이론틀 미확보)**
- **아키텍처 권고: (iii) 예비 부록 → (ii) 독립 Chapter 3 단계화**((i) Part III 비권장)
- **LCO 심화 7항목**(코드 게이트 경로 지원 YES 확인 — L1 worked example 즉시 계산 가능)
- **사용자 결정 6건(D1~D6)** · **Q6/Q7 phase 스케치**(전건 v1.0.21 소관)
