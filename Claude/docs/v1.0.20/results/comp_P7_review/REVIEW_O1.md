# REVIEW_O1 — v1.0.20 독립 검수 (검수자 O1)

- 담당: 독립 검수자 O1 (다른 창 O2/O3/F1 과 통신·참조 없음)
- 역할: Ch1 앞부분 청크 전문 정독 + 3축 검수(①신본 결함 ②v1.0.19 regression ③신설 다리 물리·서지)
- 담당 청크: ch1_sec00_intro · ch1_sec01_n0n1 · ch1_sec02a_part0 · ch1_sec02b_part0 · ch1_sec03_center · ch1_sec04_hys · ch1_sec05_width
- 신본: /home/user/Project_Anode_Fit/Claude/docs/v1.0.20/_sections/
- 구본(대조 read-only): /home/user/Project_Anode_Fit/Claude/docs/v1.0.19/_sections/
- 심각도: H=물리·수식 오류/오귀속 · M=유도 비약·정합 결손·regression · L=표기·문장·일관성
- 축: ①신본 자체 결함 · ②v1.0.19 대비 regression · ③신설 다리 물리·서지

---

### ch1_sec00_intro.tex (전문 정독 완료, 92행)

구본(v1.0.19) 대비 유일한 실질 변경 = line 24-25 MSMR 병기 소문자→대문자("Multi-Species, Multi-Reaction"). 이 외 전 행 자구 동일(figure/caption/자산 주석 포함). ③ 신설 다리 검증: 대문자 풀네임은 bakerverbrugge2018 원제("Multi-Species, Multi-Reaction Model for Porous Intercalation Electrodes...")·rubric C4·REFERENCE_LEDGER 운용메모와 정합 — **서지적으로 정확**. regression 없음.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O1-01 | ch1_sec00_intro:24 vs 7 | L? | ① | 두문자 병기 표기 대소문자 비대칭: MSMR 은 대문자 "Multi-Species, Multi-Reaction"(line 24)으로 확장하나, 같은 절 형제 두문자 ICA 는 소문자 "incremental capacity analysis"(line 7)로 확장. 절 내 병기 규범(C1) 시각 일관성이 어긋나 보일 수 있음. | line 7 "incremental capacity analysis(ICA)" 소문자 vs line 24 "Multi-Species, Multi-Reaction(MSMR)" 대문자. | 방어 가능(ICA=일반 방법명 common noun / MSMR=Baker–Verbrugge 명명 고유 프레임워크 proper noun 이므로 대문자 정당·C4 명시). 결함 아닐 수 있어 '?' 병기 — 유지하되 의도 확인용 기록. |
| O1-02 | ch1_sec00_intro:35-38 | L | ① | intro 통합 서술 "세 인자(T·전위·C-rate)는 모두 하나의 속도식 $k\simeq k_0\exp[-\Delta G_a/RT]$ 의 서로 다른 자리로 들어온다"는 T 의 평형측 진입(ΔH,ΔS,열폭 RT — 본론 N2/N4 에서 실제 사용)을 속도식 한 자리로 환원해 서술. 다만 직후 문장 "이 속도식이 …평형…을 …낳는다"로 평형=속도식 정지점(상세균형) 프레이밍이 명시돼 논리 공백은 없음. | line 35-38. 평형 중심 $U_j(T)$·열폭은 §N2·§N4 소관인데 intro 는 단일 Arrhenius 가지로 통합 서술. | 결함 아닌 교육적 통합 프레이밍(refute 결과 모순 없음) — L 로 기록만. 필요시 "평형과 지연 모두 이 한 식의 두 가지" 표현 유지 권장. |

### ch1_sec01_n0n1.tex (전문 정독 완료, 207행)

구본 대비 유일한 실질 변경 = line 90-92: 구본 "(문헌 기반, 표~\ref{tab:staging})" → 신본 "(문헌 기반\cite{dahn1991,ohzuku1993} --- 값의 확정과 tier 는 \S\ref{sec:sum} 표~\ref{tab:staging} 소관)". ② regression 판정: U1(P1_CITATION_BASELINE) 의도 인용 부여 — dahn1991(Li$_x$C$_6$ 상도표)·ohzuku1993 은 흑연 staging 초기값의 정전한 앵커·V1 키, tab:staging 참조 보존·의미 손실 0·**개선(regression 아님)**. 물리 재검산: $U_j=(-\Delta H_\rxn+T\Delta S_\rxn)/F$ (line 57) = $E=-\Delta G/F$ 부호 정합·차원 V 정합; $w=n_jRT/F$ (line 60) 차원 V 정합; $T_{c,j}=\Omega_j/2R$ (line 66) = 정규용액 스피노달/공용해 임계점($d^2f/d\theta^2=0,\ \theta=1/2 \Rightarrow \Omega=2RT_c$) 정합. 그림 peak 높이 $Q_j/(4w_j)$ 검산: $2\to1$ 0.50/(4·0.012)=10.42≈캡션 10.4 · $4\to3$ 0.10/0.08=1.25≈plot 1.247 — 일치.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O1-03 | ch1_sec01_n0n1:90-92 | L | ② | (커버리지·확인) U1 인용 부여는 의도 변경이며 서지·물리 정합. regression 없음 — 결함 아님, 확인분 기록. | CHANGE_LOG 무등재(서지·수식·부호 무관 표현 변경 → RESULT Files Updated 갈음, rubric F2 정합). dahn1991·ohzuku1993 = REFERENCE_LEDGER A 표 V1. | 유지. |
| O1-04 | ch1_sec01_n0n1:20-22 vs 29 | L? | ① | "방향 부호가 실제로 작용하는 자리는 셋뿐(N1·N3·N7·N8)"(line 20)이라 못박은 직후, line 29 에서 $\xi_\eq=\mathrm{logistic}[\sigma_d(V-U)/w]$ 로 N4/N5 에도 $\sigma_d$ 가 명시 등장 — 고학년 독자가 "넷 아닌가" 순간 마찰 가능(G-follow). | line 20 "셋뿐" vs line 29 $\sigma_d$ 노출. 해소 근거(평형 peak $\xi_\eq(1-\xi_\eq)$ 가 $\sigma_d\!\to\!-\sigma_d$ 아래 $\xi_\eq\!\to\!1-\xi_\eq$ 로 불변)는 line 22 "평형 종 자체는 방향 불변(아래 절들에서 식으로 회수)"로 예고만. | 결함 아님(문장이 이미 "그 밖에서 평형 종 방향 불변"으로 pre-empt·구본 v1.0.19 동일 문장, regression 아님). 심각도 '?'. 원하면 line 29 뒤 "(단 peak 은 $\xi_\eq(1-\xi_\eq)$ 대칭이라 방향 불변)" 반괄호 한 조각으로 마찰 제거 가능 — 실제 수정 말고 후보. |

### ch1_sec02a_part0.tex (전문 정독 완료, 349행)

이 창의 핵심 신설 지대(B-001 D7 2단 재배열 + B-002 bgbox). 구본(269행) 대비 §2.2(sec:sm-site)만 재배열·증설, §2.1·§2.3 은 자구 동일. **재배열 무결성 확인**: 기존 라벨 eq:partfn·eq:sm-occmid·eq:sm-epstilde·eq:fermifn·eq:sm-flucres·eq:sm-sint 전부 보존, 최종식(θ·⟨n⟩·μ) 불변, 신규 라벨 3종(eq:sm-baresum·eq:sm-baremid·eq:sm-bare)만 삽입 — CHANGE_LOG B-001 정합. **인용 자산 유실 0**: mckinnon1983 은 확장측(b')→원형(d) box(line 157)로 이동해 보존, hill1960·fowler1939 는 (d)·(b') 양쪽, mcquarrie1976 은 (b')·bgbox, ashcroftmermin1976 은 bgbox — 전부 REFERENCE_LEDGER V1. D7 4-스텝(원형박스→확장동기(a')→확장박스→q≡1 회수) 구조 충족.

③ 신설 다리 재유도 검산(자족 재유도):
- eq:sm-baresum $\Xi_1^0=1+e^{-\beta(\varepsilon_0-\mu)}$ ✓ (n=0→1, n=1→e^{-β(ε0-μ)}); eq:sm-baremid $\langle n\rangle^0=P_1$ ✓; 로그미분 교차검증 $k_BT\partial_\mu\ln\Xi_1^0=1\cdot e^{-\beta(\varepsilon_0-\mu)}/(1+\cdot)=\langle n\rangle^0$ ✓; eq:sm-bare 분자분모 정리 $=1/(1+e^{+\beta(\varepsilon_0-\mu)})$ ✓ = FD 형 정합.
- verifybox 극한(i)β→∞ 계단·(ii)β→0→½·(iii)μ→±∞→1/0·부호읽기 모두 재현 ✓.
- bgbox 물리: 동일입자·교환대칭 2부류·정수/반정수 스핀↔대칭/반대칭(스핀-통계)·Pauli 배타·BE $1/(e^{\beta(E-\mu)}-1)$·FD $1/(e^{\beta(E-\mu)}+1)$ 전부 정확; "0/1 배타=기하(정전·입체 반발), 양자 아님" 가드 명시(line 182-185) + verifybox ★가드(line 256-259) 이중 — B-002 요건 충족. (포논을 스핀-통계 "예"로 든 것은 준입자라 다소 느슨하나 보손임은 명백·표준 관용 — 결함 아님.)
- q(T) 확장 eq:partfn $=1+q e^{-\beta(\varepsilon_0-\mu)}$ ✓, q≡1→eq:sm-baresum 회수 ✓; 조화 $q=\prod[2\sinh(\beta\hbar\omega_i/2)]^{-1}$·고전 $q=(k_BT/\hbar\omega_0)^3$ ✓; 영점에너지 두 규약 차 $e^{-\beta\hbar\omega/2}$ 가 $T\ln q$ 에 상수 $-\hbar\omega/2k_B$ 만 남겨 엔트로피 동일 ✓.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O1-05 | ch1_sec02a_part0:253-255 | **M** | ③① | 신설 (iv) q≡1 회수절의 반괄호 "($\mu_\mathrm{Li}$ 는 원형의 $\mu$ 와 같은 저장조 화학퍼텐셜의 **몰 표기**)"가 자체 모순. $\mu_\mathrm{Li}$ 는 eq:fermifn 의 $\Delta\mu=\tilde\varepsilon-\mu_\mathrm{Li}$·$\theta=1/(1+e^{+\beta\Delta\mu})$ 에서 $\beta=1/(k_BT)$(line 60, 입자당)·$\tilde\varepsilon=\varepsilon_0-k_BT\ln q$(입자당)와 짝하므로 **입자당(per-particle)** 이어야 무차원 $\beta\Delta\mu$ 성립. 동시에 "원형의 $\mu$(=eq:sm-bare 의 입자당 $\mu$)와 같다"고 하면서 "몰 표기(per-mole)"라 명명 — 같은 양을 입자당이자 몰당이라 함. v1.0.20 신규 도입(구본 회수절엔 이 반괄호 없음). | 구본 v1.0.19 line 180: "$q\to1$ 에서 $\tilde\varepsilon\to\varepsilon_0$ 으로 소박한 2-상태 결과를 회수" — "몰 표기" 문구 부재. 신본이 (iv)로 확장하며 삽입. 문건은 "몰"을 $\times N_A$ 로 일관 사용(line 275 "$\mu^0$ 는 $\tilde\varepsilon$ 의 몰 환산 $N_A\tilde\varepsilon$")하므로 "몰 표기"는 명백히 per-mole 의미. | "의 몰 표기" 삭제(→ "원형의 $\mu$ 와 같은 저장조 화학퍼텐셜")하거나 "입자당 표기"로 정정. 실제 몰 버전은 eq:sm-muideal 의 $\mu^0=N_A\tilde\varepsilon$ 에서 별도 등장하므로 여기 라벨만 오류 — 박스식 자체는 정확(H 아님). |
| O1-06 | ch1_sec02a_part0:149 vs 152-153,136 | L | ③① | (d) 원형 박스 단락 헤더 "두-상태 원형 $\Xi_1^{0}$·$\langle n\rangle$"(line 149)는 평균점유를 위첨자 없이 $\langle n\rangle$ 로 쓰나, 정작 박스식(line 152-153)과 자체 규약 선언(line 136 "평균 점유도 같은 표기 $\langle n\rangle^{0}$ 로 구분한다")은 $\langle n\rangle^{0}$. 헤더만 위첨자 누락 — 신설 표기 일관성 흠. | line 149 $\langle n\rangle$ vs line 136·152-153 $\langle n\rangle^{0}$. | 헤더를 $\langle n\rangle^{0}$ 로 통일(신규 텍스트 내부 일관성). |

### ch1_sec02b_part0.tex (전문 정독 완료, 330행)

② regression: `diff` 결과 v1.0.19 와 **바이트 단위 완전 동일** — regression 없음. ① 자체 결함 검산(전 수식 재유도, 모두 통과): eq:sm-omega $\theta^2=\theta-\theta(1-\theta)$ 분해·$\Omega=-\tfrac{z}{2}N_Au$ 부호(인력 $u<0\Rightarrow\Omega>0$ 상분리) ✓; eq:mu $\mu=\mu^0+RT\ln[\theta/(1-\theta)]+\Omega(1-2\theta)$ ($g$ 미분) ✓; eq:sm-thresh $g''=RT/[\xi(1-\xi)]-2\Omega$·최솟값 $4RT$·$\Omega\le2RT$ 문턱 ✓; 그림 스피노달 재산출 — $\Omega=3RT$: $\xi(1-\xi)=1/6\Rightarrow\xi_s=0.2113/0.7887$ ✓(지시서 $u_j=\sqrt{1-2RT/\Omega}=\sqrt{1/3}$ 정합), $\Omega=4RT$: $\theta(1-\theta)=1/8\Rightarrow\theta_s=0.146/0.854$·값 $\pm1.066$ ✓; eq:sm-workbal→eq:sm-muV $-FV$ 뺄셈·eq:sm-eqcond $\Delta G_j=-sFU_j$·eq:sm-logistic·eq:sm-nernst 전부 ✓; $w=RT/F$ 캡션 값 268/298/328 K = 23.1/25.7/28.3 mV 재계산 일치 ✓.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O1-07 | ch1_sec02b_part0:41,177,194-196 (↔ sec02a:242,253-255) | L→**O1-05 교차확증** | ①③ | 기호 $\mu_\mathrm{Li}$ 는 sec02a eq:fermifn(line 242)에서 $\Delta\mu=\tilde\varepsilon-\mu_\mathrm{Li}$·$\beta=1/k_BT$ 로 **자리당(per-particle)**, sec02b eq:mu(line 41)·eq:sm-eqcond(line 177)에서는 $\mu^0+RT\ln[\cdot]$ 로 **몰당(molar)** — 동일 기호 이중 스케일. **핵심**: sec02b line 194-196 "일치 검산"이 "eq:fermifn 의 지수 $\beta\Delta\mu$ 를 몰로 올리면 $(\mu^0-\mu_\mathrm{Li})/RT$ … 자리당 쌍 $(k_BT,e)$ 가 몰당 $(RT,F)$ 로 환산"이라 **명시** — 즉 eq:fermifn 의 $\mu_\mathrm{Li}$ 는 자리당임을 문건 스스로 못박음. 이는 sec02a:253-255 신설 "$\mu_\mathrm{Li}$ … 몰 표기"(O1-05)와 정면 충돌. | sec02b 자체는 v1.0.19 동일(무변경). 이 이중 스케일 자체는 **pre-existing** 이고 line 194-196 다리로 관리됨(defensible). 단 v1.0.20 신설 sec02a "몰 표기" 라벨이 그 다리를 깨는 것 — O1-05 근거 강화. | O1-05 처리(라벨 삭제/입자당 정정)로 동시 해소. sec02b 는 무결. |

### ch1_sec03_center.tex (전문 정독 완료, 75행)

② regression: `diff` 결과 v1.0.19 와 **완전 동일** — regression 없음. ① 재검산(통과): eq:eqcond·eq:Uj $U_j=(-\Delta H+T\Delta S)/F$ 부호(발열 $\Delta H<0\Rightarrow$ 중심↑) ✓; $\partial U_j/\partial T=\Delta S/F$ = Gibbs 항등식 $\partial\Delta G/\partial T=-\Delta S$·$\Delta G=-FU$ 정합 ✓; 수치 $U(298)=(13000-298.15\times16)/96485=0.0853$ V ≈ 목표 0.085 V ✓(sec01 그림 $2\to1$ 초기값과 자기정합); $\partial U/\partial T\approx0.17$ mV/K·30 K→수 mV ✓.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O1-08 | ch1_sec03_center:5-6 vs 63-64 | L | ① | 절 도입(line 5-6)과 절 말미(line 63-64)가 "$U_j(T)$ 는 입력 $(\Delta H,\Delta S)$ 주어지면 식 eq:Uj 로 계산·주어지지 않으면 $U$ 직접 취한다"를 거의 동일 문장으로 두 번 진술 — 경도 중복. | line 5-6 "…식~\eqref{eq:Uj}로 계산되거나, 주어지지 않으면 $U$ 값을 직접 취한다" ↔ line 63-64 동일 골자. | 결함 아님·구본 동일(pre-existing). 도입=간략 예고 / 말미=전극별 $\Delta S$·LCO 전자 엔트로피·수치까지 확장이라 rubric A3(도입/마무리 다리) 관용 범위. 기록만. |

### ch1_sec04_hys.tex (전문 정독 완료, 213행)

② regression: `diff` 결과 세 P3 추가만 삽입·나머지 전 행 동일 — (1)line 11-19 계보 문단(dreyer2010·dreyer2011), (2)line 134-135 (d) 부호 문장 dreyer2010 재인용(구본 "방전 전위가 충전보다 높다는 관측 일치"→신본 "탈리튬화 가지가 높은 전위에 남는다는 영전류 극한의 실측 갈림\cite{dreyer2010}"), (3)line 137-142 γ/h_η 지위 문단. 셋 다 U2(CITATION_BASELINE)·CHANGE_LOG(C-010) 의도 변경. **의미 약화·자산 유실 0**(오히려 (2)는 전극상대적 "방전/충전"→전극중립 "탈리튬화 가지"로 정밀화). ③ 재검산 통과(위 응답 요약). ③ 서지: dreyer2010(Nat. Mater. 9, 448, 2010 — 히스 열역학 기원·영전류 지속)·dreyer2011(CMT 23, 211, 2011 — many-particle) 정확 귀속·V1. 핵심 유도 eq:spinodal·eq:dUhys·★Taylor 함정·fig 수치 전건 재유도 일치.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O1-09 | ch1_sec04_hys:11 vs 14-17 | L? | ③① | 신설 계보 문단 서두 "이 분기의 물리적 계보와 **두 용어**를 놓는다"(line 11)라 예고하나, 이어 괄호 정의가 셋 등장: 준안정 가지(metastable branch, line 14)·과주행(overshoot, line 15)·spinodal(line 16-17 "자유에너지 곡률이 0 이 되는 안정성 한계"). 용어 수를 세는 독자에 순간 불일치. | line 11 "두 용어" vs line 14-17 세 괄호 정의. | 방어 가능: spinodal 은 Part 0(§2 fig:sm-gxi·용어표)에서 이미 정의된 **회수**이고 신규 두 용어는 준안정 가지·과주행이라 "두 용어"가 맞음. '?' 병기. 원하면 line 16 spinodal 을 "(앞서 §2 의 spinodal)"로 회수 표시해 마찰 제거 — 후보. |
| O1-10 | ch1_sec04_hys:134-135 | L | ③ | (검증·확인) (d) 부호 재인용이 dreyer2010(LiFePO$_4$=양극 연구)으로 흑연 "탈리튬화 가지 높은 전위" 부호를 뒷받침 — 인용된 사실(탈리튬화 가지 상위·영전류 지속)은 spinodal/준안정 그림의 **일반** 열역학 귀결이고 본문이 eq:Veq 비단조로 자체 유도하므로 인용은 보강용·정당. 재질(LiFePO$_4$≠흑연) 차이는 원리 인용이라 문제 아님. | dreyer2010 대상=LiFePO$_4$. 본문 유도(§4.2 eq:Veq 극대=탈리튬화 가지)로 부호 독립 확립·인용은 corroboration. | 결함 아님 — 확인분 기록(③ 서지 정확). 유지. |

### ch1_sec05_width.tex (전문 정독 완료, 299행)

② regression: `diff` v1.0.19 = **바이트 단위 완전 동일**(출력 0) — regression 없음. ③ 신설 다리 소관: CHANGE_LOG 에 sec05 무등재(P2~P6 편집 대상 아님) + diff 무변경 = **정상**(무변경이어야 옳고 실제 무변경) → 이 파일 발견은 전부 축① pre-existing 자체 결함/일관성. ① 자족 재유도(전 수식·전 그림 수치 손검산, **H 0·자체 M 0**): eq:bv 비대칭 장벽 → eq:db $r^+/r^-=e^{\mathcal A/RT}$($k_0e^{-\Delta G_a/RT}$ 약분·$\chi{+}(1{-}\chi){=}1$) → 운동식 $\dot\xi=r^+(1{-}\xi)-r^-\xi=k_j(\xi_\eq-\xi)$·정지점 $\xi_\eq=r^+/(r^++r^-)$ → eq:logisticsolve $\xi_\eq/(1{-}\xi_\eq)=e^{sF(V_n-U_j)/RT}\Rightarrow\xi_\eq=1/(1+e^{-sF(V_n-U_j)/RT})$ → 중심기울기 $sF/(4RT)$(logistic 중심 $\xi(1{-}\xi){=}\tfrac14$ × $sF/RT$) → 폭척도 $RT/F$ → **eq:wbase $w_j=n_jRT/F$**(차원 [J/mol]/[C/mol]=[V] ✓·역산 $n_j=w_jF/RT$ ✓) → $s\to\sigma_d$·$U_j\to U_j^{\,d}$·$RT/F\to w_j$ 일반화 → eq:xieq. $\partial w_j/\partial T=(R/F)(n_j+T\dd n_j/\dd T)$ 곱미분 ✓. 그림 전수 일치: **fig:barrier**($G_\mathrm{base}=0.1+0.9\sin^2[\pi(x{-}1)/4]$·$\Delta G_a{=}0.9$·구동 도착골 $-0.5$·정점 $-0.25$·정방향 $0.65$/역방향 $1.15$ 재현), **fig:flux**($r^+/r^-=e^{\mathcal A/RT}=1,2,4\Rightarrow\xi_\eq=\tfrac12,\tfrac23,\tfrac45$), **fig:logistic**($w=nRT/F$ @268/298/328 K$=23.09/25.68/28.26$ mV·정점 $1/(4w)=10.83/9.74/8.85$ /V·FWHM $2\ln(3{+}2\sqrt2)w=3.5255w=90.5$ mV·half-max $\pm45.27$ mV) — 전건 "식 그대로" 수치 정확. §5.3 몰환산 사슬($\Delta\mu^{몰}=\mu^0-\mu_\mathrm{Li}=sF(V-U)$·$\langle n\rangle=\theta_\eq$·여집합 $\xi_\eq=1-\langle n\rangle$·부호 $-\Omega(1{-}2\xi)=+\Omega(1{-}2\theta)$ [eq:mu]) 부호까지 정합. 단상 유효폭 $(1-\Omega_j/2RT)$ 배 검산: $g''$ 를 $\theta{=}\tfrac12$ 에서 $=4RT-2\Omega=4RT(1-\Omega/2RT)\Rightarrow w_\mathrm{eff}=w_0(1-\Omega/2RT)$(좁아짐, $\Omega\to2RT$ 에서 $\to0$) 정합. 실질 신규 지적은 표기·정합 L 급뿐.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| O1-11 | ch1_sec05_width:88,96-97 (fig:barrier) | L(→M) | ① | fig:barrier 주석·캡션이 §5 밖 기호를 **정의·전방 포인터 없이** 심음: (a) $\Delta H_a^\eff{=}\Delta H_a{-}\chi_d\Omega$ 의 $\chi_d$ 는 §5 미정의이고, 같은 캡션이 쓰는 장벽위치 $\chi{=}\tfrac12$(line 87·94)와 시각 충돌; (b) 본문 유도는 전부 Gibbs $\Delta G_a$ 인데 이 주석만 엔탈피 $\Delta H_a$ 로 갈아탐; (c) $L_q$(line 97)도 §5 미정의 전방 기호. | line 88 node `$\Delta H_a^\eff{=}\Delta H_a{-}\chi_d\Omega$` + line 96 캡션 동문 + line 97 "logistic·$L_q$ 의 공통 출발점". 본문 $\chi$=Butler–Volmer 위치분율(line 16·18-19)·$\Delta G_a$(line 13-19,78,82) 일관. $z$ 충돌은 각주(line 174-175)로 가드하나 $\chi$/$\chi_d$ 는 무가드. | 방어: fig 를 logistic 경로와 $L_q$(운동학) 경로의 "공통 출발점"으로 공유하려는 의도적 전방 심기(plant). 단 무포인터라 G-follow 마찰. 후보: 캡션에 "($\chi_d$·$L_q$ 는 §운동학에서 정의)" 반괄호 포인터 1조각. 실제 수정 말 것. |
| O1-12 | ch1_sec05_width:196-197 | L | ① | "$2RT(\approx 4958$ J/mol $@298$ K$)$" 의 수치–온도 라벨 불일치: 4958 J/mol 은 **298.15 K**(=25°C) 값이고, 명시 라벨 "@298 K" 정확대입은 $2{\times}8.314{\times}298=4955$ J/mol. ~3 J/mol(0.06%) 어긋남. | $2RT{=}4955.1$ J/mol(298 K)·$4957.6\approx4958$(298.15 K). 같은 파일이 기준온도를 line 182 "$25^\circ$C"·fig "298 K" 혼용. | 방어: "298 K"를 25°C 관용 통칭으로 쓴 것(≈ 표기 有). 후보: "@298.15 K" 또는 값 4955 로. 극경미. |
| O1-13 | ch1_sec05_width:106 (fig:flux 주석) | L | ① | TikZ 주석 "A/RT=2RT ln2" 에 잉여 "RT" — $\mathcal A/RT{=}2\ln2$($=\ln4\Rightarrow r^+/r^-{=}4$)여야 함. 앞 두 항 "A/RT=0"·"A/RT=ln2" 와 열($=\mathcal A/RT$) 불일치($\mathcal A{=}2RT\ln2$ 를 $\mathcal A/RT$ 칸에 오기). | line 106 vs 렌더 캡션 line 144 "$\mathcal A/RT=0,\ln2,2\ln2$"(정확). | **비렌더 주석**(독자 무영향) — 최저 우선. 후보: 주석을 "A/RT=2 ln2" 로. |
| O1-14 | ch1_sec05_width:271-277 (↔ sec02a:253-255) | 확인분→**O1-05 교차확증**(M연동) | ③① | sec05 line 273 이 eq:fermifn 을 $\langle n\rangle=1/(1+e^{+\beta\Delta\mu})$·$\Delta\mu\equiv\tilde\varepsilon-\mu_\mathrm{Li}$ 로 **받아** $\beta{=}1/k_BT$ 와 짝지음 → 여기 $\mu_\mathrm{Li}$ 는 **자리당(per-particle)**. 몰버전은 line 274-277 이 $N_A\tilde\varepsilon{=}\mu^0$·"$k_BT{\to}RT,e{\to}F$ 한꺼번에 환산"으로 별도 유도. 즉 sec05 도 eq:fermifn 의 $\mu_\mathrm{Li}$=자리당임을 실증 — sec02a:253-255 신설 "$\mu_\mathrm{Li}$ … 몰 표기"(O1-05)와 충돌하는 **세 번째 증인**(O1-07 sec02b:194-196 에 이음). | line 271-273 $e^{\pm\beta\Delta\mu}$ 자리당 vs line 275 $\mu_\mathrm{Li}=\mu^0-sF(V-U)$ 몰당 — sec05 는 line 277 명시 환산으로 내부 정합(결함 아님, 증인). | sec05 무결(무변경·자체 정합). O1-05 처리(sec02a "몰 표기" 라벨 삭제/자리당 정정)로 세 파일 동시 정합. |
| O1-15 | ch1_sec05_width:169 vs 34,175 (P3 검수①) | L? | ① | 결과 박스 eq:xieq 는 인자를 맨 $V$ 로 쓰나($\xi_{\eq,j}(V,T)$), 직전 유도 eq:logisticsolve(line 34)는 $V_n$ 명시. 본 프로젝트 P3 검수 1항목($V_n$/$V_{n,app}$/$V_{n,drive}$/$V_{n,OCV}$ 일관)의 엄격 적용 시, Chapter 2+ 가 import 하는 boxed 식이 맨 $V$ 를 실으면 하류 오용 여지. | line 169 $V$ vs line 34 $V_n$·line 175 "여기서 평가 전위는 §pol 의 내부 전위 $V_n$". | 방어: line 175 가 즉시 "$V{=}V_n$" 핀 고정 → 정합. 평형 등온선을 일반 전위 $V$ 로 쓰는 관용. 후보: eq:xieq 인자를 $V_n$ 로. 결함 경계 — '?'. |

---

## REVIEW COMPLETE — 발견 총 15건 (O1 본대 6파일 + 보충 1파일)

- 본대(O1-01~O1-10, 6파일): sec00_intro·sec01_n0n1·sec02a_part0·sec02b_part0·sec03_center·sec04_hys.
- 보충(O1-11~O1-15, sec05_width): L(→M) 1건(O1-11)·L 3건(O1-12·O1-13·O1-15)·확인분/교차확증 1건(O1-14). 그중 O1-13 은 비렌더 주석, O1-15 는 '?' 방어우세.
- **심각도 분포**: H 0 · M 1(O1-05, 유일 실오류) · L·L?·확인분 14. sec05 는 축② regression 0(바이트 동일)·축③ 무변경 정상·축① H·자체 M 0(전 수식·전 그림 수치 재유도 무결) — 실질 신규 지적은 L 급 표기·정합뿐.

## 가장 약한 1곳

**선정: O1-05 = ch1_sec02a:253-255 신설 반괄호 "$\mu_\mathrm{Li}$ 는 원형의 $\mu$ 와 같은 저장조 화학퍼텐셜의 **몰 표기**"** (sec05 발견 O1-14 로 보강).

근거:
1. **유일한 실제 자기모순.** 같은 $\mu_\mathrm{Li}$ 를 eq:fermifn 의 $\beta\Delta\mu$(=$1/k_BT$·자리당)이면서 동시에 "몰 표기(per-mole)"라 명명 — 한 양을 입자당이자 몰당이라 함. 나머지 발견(O1-01~04·06·08~15)은 표기·마찰·비렌더·방어우세로 '결함 아닐 수 있음'이나, 이 한 곳만 정의 충돌.
2. **v1.0.20 편집이 들여온 결함(축③ 성격).** 구본 v1.0.19 회수절엔 이 반괄호가 없음(sec02a diff). 무변경이어야 할 자리가 아니라 신설 (iv)절에 삽입되며 생김.
3. **삼중 독립 증인.** O1-05(sec02a 직접)·O1-07(sec02b:194-196 이 "eq:fermifn 지수를 자리당→몰로 올린다"고 명시)·O1-14(sec05:273 이 eq:fermifn 을 $\beta\Delta\mu$ 자리당으로 받아 씀) — 세 파일이 독립적으로 "eq:fermifn 의 $\mu_\mathrm{Li}$=자리당"을 확증. 즉 sec02a "몰 표기" 라벨만 세 곳과 어긋남.
4. **저비용·고효과 수렴.** "의 몰 표기" 4자 삭제(또는 "입자당 표기"로 정정) 한 번이면 sec02a·sec02b·sec05 세 파일이 동시 정합. 박스식 자체는 정확(H 아님)이라 물리 위험 없이 국소 정정 가능 — 문건 전체에서 고칠 가치가 가장 분명한 단일 지점.

