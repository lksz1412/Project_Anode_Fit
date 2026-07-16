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

