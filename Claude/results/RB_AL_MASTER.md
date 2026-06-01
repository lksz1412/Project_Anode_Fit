# RB_AL_MASTER — 통합 Assumption Ledger + Notation Bible + 가독 Gate (Phase 0.3, step 13–16)

> **위치**: RB Phase 0.3 (Foundation 마지막). **입력**: `RB_CHARTER.md`(규약), `RB_REFERENCES_DOSSIER.md`(검증 DOI).
> **성격**: 골격(skeleton). 장별 가정은 각 장 5-stage 의 S2(grounding 감사)에서 본 ledger 에 \emph{추가}된다.
> 본 문서는 (1) 통합 AL 번호 체계 + 기등재 established 가정, (2) notation bible, (3) 학부-가독·무비약 gate 정의서 3부.

---

# 1부. 통합 Assumption Ledger (AL-#)

**규칙(RB_CHARTER step 5)**: 단일 연속 번호. tier = GROUNDED / BOUNDED / FLAGGED. 모든 본문 가정식이 AL-# 인용.
무근거 가정 = FLAGGED(established 사용 금지) + 방향-3 재작성 트리거.

**번호 배정(주제 그룹)**: AL-1~9 = 전하보존·평형 무대(Ch1) · AL-10~19 = 동역학·배리어·spectrum(Ch1) ·
AL-20~29 = 발열·entropy(Ch2) · AL-30~39 = 반응속도론(Ch3) · AL-40~49 = entropy production 발열(Ch4) ·
AL-50~59 = 히스테리시스(Ch5) · AL-60~69 = 수치·closure(Ch6). 그룹 내 여유번호는 장별 S2 에서 채움.

| AL-# | 가정 진술 | tier | 근거 cite | 검증 DOI/ISBN | 사용(장·식) |
|---|---|---|---|---|---|
| **무대·평형 (Ch1)** | | | | | |
| AL-1 | 전하 보존: 외부 누적 전하 = 배경 + staging 진행 용량 (내부 $V_n$ 결정) | GROUNDED | doyle1993, newman | 10.1149/1.2221597 / ISBN 978-0-471-47756-3 | Ch1 charge_balance |
| AL-2 | 평형 진행률 logistic $\xi_\eq=[1+e^{-(V_n-U_j)/w_j}]^{-1}$ (lattice-gas/regular-solution chemical potential) | GROUNDED | mckinnon1983, bazant2013 | 10.1021/ar300145c | Ch1 xi_eq |
| AL-3 | 흑연 staging 전이($4\to3\to2L\to2\to1$), 관측 $N_p\approx3\sim4$ | GROUNDED | dahn1991, ohzuku1993, funabiki1999ea, funabiki1999jes | 10.1103/PhysRevB.44.9170; 10.1149/1.2220849; 10.1016/S0013-4686(99)00290-X; 10.1149/1.1391953 | Ch1 staging |
| AL-4 | 평형 전이폭 $w_j=RT/F$ (ideal); 일반 effective $w_j$ 는 $n_j^\eff=RT/(Fw_j)$ | GROUNDED | newman, bazant2013 | ISBN; 10.1021/ar300145c | Ch1·3·4 (CHARTER step3) |
| AL-5~9 | (Ch1 S2 에서 채움: $Q_\bg$ chemical capacitance, $V_{n,\app}$ 분극 등) | — | — | — | — |
| **동역학·배리어·spectrum (Ch1)** | | | | | |
| AL-10 | 활성화 자유에너지 $\Delta G_a=\Delta H_a-T\Delta S_a$, Eyring rate $k=k_0 e^{-\Delta G_a/RT}$, $k_0=(k_BT/h)\kappa$ | GROUNDED | eyring1935, evanspolanyi1938 | 10.1063/1.1749604; 10.1039/TF9383400011 | Ch1 rate |
| AL-11 | 극판 전위에 의한 유효배리어 낮춤 $\Delta G_\eff=\Delta G_a-\chi_j\mathcal A_j$ ($0\le\chi_j\le1$); BEP/transfer-coeff 류 | GROUNDED | evanspolanyi1938, bazant2013 | 10.1039/TF9383400011; 10.1021/ar300145c | Ch1 Geff (CHARTER step1,4) |
| AL-12 | 평형 근처 1차 완화 $d\xi_j/dt=k_j(\xi_{\eq,j}-\xi_j)$ (linear irreversible thermo) | GROUNDED | onsager1931, degrootmazur1962 | 10.1103/PhysRev.37.405 | Ch1 relax |
| AL-13 | barrier 분포 $\rho_G$ → relaxation-length spectrum $A_L$ (지수 매핑); 변수변환 밀도보존 | GROUNDED | (수학; baessler1993 disorder analogy) | 10.1002/pssb.2221750102 | Ch1 spectrum |
| AL-14 | ★ stretched tail = 지수 완화의 연속 합/분포 (kernel integral); 고정 barrier 분포 → T-의존 stretched (fast-ion) — \emph{이 문서 핵심 물리} | GROUNDED | **svare2000**, **johnston2006**, lindsey1980 | **10.1103/PhysRevB.61.228**; 10.1103/PhysRevB.74.184430; 10.1063/1.440530 | Ch1 kernel (svare2000 = 폰 macdonald2000 의 저자 오귀속 정정) |
| AL-15 | Marcus bound: 선형 $\chi\mathcal A$ 는 $|\mathcal A|$ 큰 영역(inverted)서 깨짐 → 유효범위 | BOUNDED | marcus1956 | 10.1063/1.1742723 | Ch1 Geff bound |
| AL-16 | non-uniqueness: stretched→$\rho_G$ 역매핑 비유일 (forward-only) | BOUNDED | baessler1993 (+plonka 미확인) | 10.1002/pssb.2221750102 | Ch1 spectrum caveat |
| AL-17~19 | (Ch1 S2 에서 채움) | — | — | — | — |
| **발열·entropy (Ch2)** | | | | | |
| AL-20 | 전지 에너지 balance: $q_\rev=s^\conv|I|T\,\partial U/\partial T$, $q_\irr=|I|\eta$ (Bernardi balance) | GROUNDED | bernardi1985, rao1997 | 10.1149/1.2113792; 10.1149/1.1837884 | Ch2·4 (CHARTER step1) |
| AL-21 | 평형 전위 온도계수 = reaction entropy ($\partial U/\partial T$); graphite 실측 | GROUNDED | reynier2004, thomasnewman2003 | 10.1149/1.1646152; 10.1149/1.1531194 | Ch2 entropy |
| AL-22 | $Q_\cell,Q_{j,\tot}$ 온도무관 기준용량 (OCV 온도미분서 상수 취급) | BOUNDED | thomasnewman2003 | 10.1149/1.1531194 | Ch2 eqbal·dVocvdT |
| AL-23 | graphite $U_j(T)$ 비단조 → OCV 온도계수 SOC 의존 부호반전(실측) | BOUNDED | reynier2004, thomasnewman2003 | 10.1149/1.1646152; 10.1149/1.1531194 | Ch2 dxidT |
| AL-24 | reaction entropy $\Delta S_\rxn$ ≠ activation entropy $\Delta S_a$ (대입 금지) | BOUNDED | eyring1935, bardfaulkner | 10.1063/1.1749604; ISBN 978-0-471-04372-0 | Ch2 eyring_entropy |
| AL-25 | OCV 온도계수(A 방식) = entropy-basis 가역열(B 방식) 정합 제약(double-counting 차단; 동일 heat-positive 규약) | GROUNDED | bernardi1985, thomasnewman2003 | 10.1149/1.2113792; 10.1149/1.1531194 | Ch2 consistency |
| AL-26 | $h_\bg$ background entropy coeff; progress vs 좌표 분리 | BOUNDED | rao1997, thomasnewman2003 | 10.1149/1.1837884 | Ch2 hbg·bgsplit |
| AL-27 | 비가역열 = flux×force(entropy production); 공액 force = $\eta_j$; 2법칙 $\ge0$ (기본형 $V_\drive=V_n$, $n^\eff=1$ 한정; 일반형 Ch3/Ch4) | GROUNDED | degrootmazur1962(book), onsager1931 | 10.1103/PhysRev.37.405 | Ch2 fluxforce·qirr |
| AL-28 | rate-affinity $\mathcal A_j$ ≠ heat-force $\eta_j$; $R_n\ne R_{n,\eff}\ne R_\ct$ (식별성) | BOUNDED | newman, bardfaulkner | ISBN | Ch2 fluxforce·i2r |
| AL-29 | near-eq entropy production $\sigma_j=(g''_j/T)k_j r_j^2\ge0$ ($g''_j>0$ 안정성); per-mode 열률 = $(Q_{j,\tot}/F)T\sigma_j$ [W]; 비가역열 tail = ICA tail 열적 거울(준독립 calorimetry 검정) | BOUNDED(σ) / FLAGGED(열적 tail novel) | degrootmazur1962, onsager1931, bazant2013 | 10.1103/PhysRev.37.405; 10.1021/ar300145c | Ch2 sigma·thermal_kernel |
| **반응속도론 (Ch3)** | | | | | |
| AL-30 | forward/backward kinetics + detailed balance $\ln(r^+/r^-)=(V_n-U)/w$ | GROUNDED | bardfaulkner, newman | ISBN 978-0-471-04372-0 | Ch3 db |
| AL-31 | Butler–Volmer; $R_n\ne R_\ct\ne R_{n,\eff}$ 계층 | GROUNDED | bardfaulkner, bazant2013 | 10.1021/ar300145c | Ch3 bv |
| AL-32 | 계면 과전압 $\eta_n=\phi_s-\phi_e-U_n$ ≠ reduced $\eta_{n,\drive}$ ≠ $V_{n,\app}$ (임의 동일시 금지; reference-electrode convention) | BOUNDED | bardfaulkner, newman | ISBN | Ch3 eta_standard·drive |
| AL-33 | forward/backward 장벽 선형 이동($\mp\beta_j\mathcal A_j$) = 소구동력 1차; $|\mathcal A_j|\sim\lambda$ 서 Marcus 곡률로 깨짐 | BOUNDED | marcus1956, bazant2013 | 10.1063/1.1742723; 10.1021/ar300145c | Ch3 rplus·rminus |
| AL-34 | detailed-balance 정합 $n_j^\eff=RT/(Fw_j)$; ratio $r^+/r^-$ 의 $\xi_j$-무관(대칭 split)이 keystone 닫힘 조건; $C_j$ 무의존 partition | GROUNDED(제약)/BOUNDED(partition) | bazant2013, newman | 10.1021/ar300145c | Ch3 neff·verifybox |
| AL-35 | 강구동 forward rate 제한 = 직렬 병목(cap 아님); 기본형 대칭 적용(DB 보존), forward-only 비대칭 → DB 이탈(Ch5) | GROUNDED/BOUNDED | newman, degrootmazur1962(book), onsager1931 | 10.1103/PhysRev.37.405 | Ch3 forward_limiter |
| AL-36 | generalized affinity $\mathcal A_n=F\eta_n+\mathcal A_\resid$; rate-affinity↔heat-force double-counting 금지 | BOUNDED | bazant2013, newman | 10.1021/ar300145c | Ch3 affinity |
| AL-37 | 전류 보존 $|I|=I_\bg^{\prog}+\sum_j I_j$ (전하보존식 시간미분; Ch2 coordinate/progress 정합) | GROUNDED | doyle1993, newman | 10.1149/1.2221597 | Ch3 current_decomp |
| AL-38 | $R_n$ apparent aggregate 분해(ohmic/ct/transport/film); 동시 자유피팅 금지(식별성) | BOUNDED | bardfaulkner, newman | ISBN | Ch3 Rn |
| AL-39 | kinetics Arrhenius 온도의존 + 식별성 chain($R_n,R_\ct,\chi$ 독립제약) | BOUNDED | bardfaulkner, bazant2013, fly2020 | 10.1021/ar300145c; 10.1016/j.est.2020.101329 | Ch3 T·ident |
| **entropy production 발열 (Ch4)** | | | | | |
| AL-40 | entropy production $T\dot S_\irr=\sum_\alpha J_\alpha X_\alpha\ge0$ (flux–force, 2법칙) | GROUNDED | degrootmazur1962, onsager1931, prigogine1967 | 10.1103/PhysRev.37.405 (onsager1931); ISBN — (degrootmazur1962/prigogine1967 books) | Ch4 fluxforce |
| AL-41 | transition-level entropy production = network/master-equation form. per-transition(단일 directed edge): $\dot s_j=k_B(\mathcal J^+-\mathcal J^-)\ln(\mathcal J^+/\mathcal J^-)\ge0$ (양방향 edge 이중합 $\tfrac12\sum_{\mathrm{edges}}$ 와 \emph{동일물의 다른 셈법} — 본 RB 는 단일-쌍 $\sum_j$ 라 $\tfrac12$ 부재); extensive 화 $\times(Q_{j,\tot}/F)RT$ ($N_A k_B=R$) | GROUNDED | schnakenberg1976 | 10.1103/RevModPhys.48.571 | Ch4 tr_entropy |
| AL-42 | 전기화학 반응 entropy production = molar reaction flux $J_n$ × reaction affinity $\mathcal A_n$ ($T\dot S_\irr=J_n\mathcal A_n\ge0$); $I_n\eta_n$ 은 부호 convention 종속 magnitude, $J_n\mathcal A_n$ 이 더 기본형 | GROUNDED | degrootmazur1962(book), prigogine1967(book), bazant2013 | 10.1021/ar300145c | Ch4 JA |
| AL-43 | transition chemical affinity $\mathcal A_j^{\mathrm{chem}}=RT\ln(\mathcal J_j^+/\mathcal J_j^-)$ (network thermo local affinity); $(\mathcal J^+-\mathcal J^-)\ln(\mathcal J^+/\mathcal J^-)\ge0$ 부호보조정리 (두 양수 차×로그비 $\ge0$) | GROUNDED | schnakenberg1976, prigogine1967(book) | 10.1103/RevModPhys.48.571 | Ch4 tr_entropy |
| AL-44 | ★ 미시=거시 정합: detailed balance($r^+/r^-{=}\xi_\eq/(1{-}\xi_\eq)$, AL-30)+$n_j^\eff{=}RT/(Fw_j)$(AL-34) 대입 시 $\mathcal A_j^{\mathrm{chem}}=n_j^\eff F\eta_j$, 따라서 $\dot{\mathcal Q}_{\irr,j}^{\tr}=\dot n_j\mathcal A_j^{\mathrm{chem}}=n_j^\eff I_j\eta_j$ (★ 두 전제: (i) $C_j\equiv0$=$r^+/r^-$ 의 $\xi_j$-무관(대칭 split, AL-34) — 없으면 $RT\,C_j$ 항 추가로 닫힘 깨짐; (ii) 기본형 $V_{n,\drive}=V_n$, CHARTER step2 η 이중정의 해소; $s_\phi{=}+1$ 방전, 충전 Ch5) | GROUNDED(전제 (i),(ii) 하; 미충족 시 BOUNDED) | schnakenberg1976, bazant2013, degrootmazur1962(book) | 10.1103/RevModPhys.48.571; 10.1021/ar300145c | Ch4 micro_macro |
| AL-45 | ★ 비가역열 일반형 $\dot{\mathcal Q}_\irr=\sum_j n_j^\eff I_j\eta_j$ + 부호 양정치 $\ge0$ (2법칙); Ch2 $\sum_j I_j\eta_j$ 는 $n^\eff{=}1$ ideal-width 특수해 (CHARTER step3 일반/특수 위계) | GROUNDED | degrootmazur1962(book), onsager1931, schnakenberg1976 | 10.1103/PhysRev.37.405; 10.1103/RevModPhys.48.571 | Ch4 micro_macro·qirr_general |
| AL-46 | Ch2 3-분해 → Ch4 4-분해 정련: $\dot{\mathcal Q}_{\irr,n}^{\mathrm{Ch2}}\supset\dot{\mathcal Q}_{\irr,n}^{\mathrm{Ch4}}+\dot{\mathcal Q}_{\transp,n}$ (계면반응 entropy production 과 transport dissipation 분리; 이중계상 금지) | BOUNDED | bernardi1985, rao1997 | 10.1149/1.2113792; 10.1149/1.1837884 | Ch4 decomp |
| AL-47 | transport/병목 발열 = flux–force $\sum_\ell J_\ell X_\ell$ (선형 near-eq 서 $I^2R_\transp$); Ch1 $R_n\ne R_{n,\eff}\ne R_\ct$ 유지, $R_{n,\eff}$ 는 독립 calorimetric/physical 제약 시만 | BOUNDED | degrootmazur1962(book), newman, bardfaulkner | ISBN 978-0-471-47756-3; 978-0-471-04372-0 | Ch4 transport·Rsep |
| AL-48 | 휴지 relaxation heat $\dot{\mathcal Q}_{\xi,\rlx}=\dot{\mathcal Q}_{\rev,\xi}^\rlx+\dot{\mathcal Q}_{\irr,\xi}^\rlx$; 외부 $I{=}0$ 라도 내부 transition flux $I_j{=}Q_{j,\tot}\dot\xi_j\ne0$ 의 dissipation $n_j^\eff I_j\eta_j$ 존재; 가역/비가역 정량분리는 독립 calorimetry 필요 (Ch2 AL-29 후보 확정) | BOUNDED | schnakenberg1976, degrootmazur1962(book) | 10.1103/RevModPhys.48.571 | Ch4 rest |
| AL-49 | log singularity ($\mathcal J^\pm\to0$) 는 coarse-graining resolution positive floor (numerical domain guard, heat fitting parameter 아님); $n_j^\eff I_j\eta_j$ 형은 평형서 $I_j\to0$ 로 매끄럽게 0 (발산 없음) | BOUNDED | schnakenberg1976 | 10.1103/RevModPhys.48.571 | Ch4 tr_entropy boundbox |
| **히스테리시스 (Ch5)** | | | | | |
| AL-50 | 삽입전지 히스테리시스 = metastable/다입자 열역학 기원 (loop area ≠ true hys) | GROUNDED | dreyer2010 | 10.1038/nmat2730 | Ch5 hys |
| AL-51 | disorder-driven first-order 전이의 hysteresis/hierarchy | GROUNDED | sethna1993 | 10.1103/PhysRevLett.70.3347 | Ch5 branch |
| AL-52~59 | (Ch5 S2 에서 채움; branch 부호 CHARTER step1) | — | — | — | — |
| **수치·closure (Ch6)** | | | | | |
| AL-60 | index-1 DAE / BDF·Radau 시간적분 (root-constrained ODE) | GROUNDED(이론) | brenan1996, hindmarsh2005 | 10.1137/1.9781611971224; 10.1145/1089014.1089020 | Ch6 dae |
| AL-61 | Plan A closure: Fredholm 2종 ratio-substitution (사용자 PhD) | BOUNDED | jcp2017, lee2011, son2013 | 10.1063/1.5000882; 10.1063/1.3565476; 10.1063/1.4802584 | Ch6 closure |
| AL-62 | ★ ratio ansatz broad-kernel 열화 = stretched-tail(저온) 영역서 부정확 → Plan B(g-grid) validator 필수, ε 측정 전 candidate | BOUNDED | jcp2017 (Eq.34 자기명시) | 10.1063/1.5000882 | Ch6 closure caveat |
| AL-63 | ICA(dQ/dV) rate-dependency / best-practice | GROUNDED | dubarry2022, fly2020 | 10.3389/fenrg.2022.1023555; 10.1016/j.est.2020.101329 | Ch6 validation |
| AL-64~69 | (Ch6 S2 에서 채움) | — | — | — | — |

**★ macdonald2000 → svare2000 처리**: 폰의 저자 오귀속(Phase 0.2 G-1). DOI·제목·물리는 정확, 저자만 Macdonald→Svare/Martin/Borsa 정정. 키 `svare2000`(PRB 61,228). stretched-tail grounding = svare2000(fast-ion DAE→T-의존 stretched, 정확 부합) + johnston2006(continuous sum) + lindsey1980(KWW). 셋으로 "고정 barrier 분포 → T-의존 stretched exponent" 가 완전히 닫히지 않는 세부는 Ch1 S2 에서 FLAGGED 후보(방향-3). **plonka 논문 DOI·책 ISBN web 미확인 → 미확인 표기, 보조 근거로만.**

---

# 2부. Notation Bible

**역사적 명칭 매핑 (P3-7)**: (A) kernel-integral 계열 진행률 $\theta$ ≡ (B) 전하보존 계열 $\xi$. **본 RB 는 $\xi$ 로 통일.**
"ver.1~5"(파일 이력) ≠ "Chapter 1~6"(구조).

| 기호 | 단위 | 의미 | CHARTER 규약 |
|---|---|---|---|
| $q$ | — | 방전 진행 좌표 ($q=Q_\ext/Q_\cell$) | |
| $V_n$ | V | 내부 음극 전위 = 전하보존식 해 | step2 |
| $V_{n,\app}$ | V | 관측 전위 (분극 포함) | step2 |
| $V_{n,\drive}$ | V | 구동 전위; 기본 $=V_n$ | **step2 (기준)** |
| $V_{n,\OCV}$ | V | 평형 전하보존 해 | step2 |
| $\xi_j,\xi_{\eq,j}$ | — | transition $j$ 진행률·평형 진행률 | |
| $\mathcal A_j$ | J/mol | 구동력 $=s_{\phi,j}n_j^\eff F(V_{n,\drive}-U_j)$ | **step1** |
| $\eta_j$ | V | 과전압 $=V_{n,\drive}-V_{\eq,j}(\xi_j)$ | **step2** |
| $s_{\phi,j}$ | — | 방전 부호 인자 ($+1$ 기본; Ch5 branch $s^b$) | **step1** |
| $\chi_j(=\beta_j)$ | — | 배리어 낮춤 민감도 = Ch3 transfer coeff | **step4** |
| $n_j^\eff$ | — | $=RT/(Fw_j)$ (ideal $w=RT/F$ 서 $1$) | **step3** |
| $\Delta G_{a,j},\Delta H_{a,j},\Delta S_{a,j}$ | J/mol | 활성화 자유E·엔탈피·엔트로피 | AL-10 |
| $G,\rho_G$ | J/mol, mol/J | local barrier·분포 | AL-13 |
| $k_j,k_0,L,A_L$ | 1/s,1/s,—,1/L | mobility·prefactor·relaxation length·spectral density | AL-11~14 |
| $\Theta,Q_p$ | —,C | 전체 phase progress·용량 scale | |
| $q_\rev,q_\irr$ | W | 가역·비가역 열 ($q_\irr=|I|\eta\ge0$) | step1, AL-20 |

---

# 3부. 학부-가독·무비약 Gate 정의서 (방향-1·2·4 집행)

각 장 S4(적대검증)·S5(gate)에서 적용. "확인 가능한 조건"으로만 기술.

- **G-flow**: 골격 핵심식이 전부 존재 + 인과 사슬 순서 보존. (dossier 흐름 표 대조)
- **G-noleap**: 모든 유도 단계가 명시 근거(앞 식 번호 / AL-# / 표준 대수)로 따라온다. **"자명하다 / clearly / 보일 수 있다 / 쉽게 / obviously" 0건** (전수 scan).
- **G-undergrad**: 독립 재유도 agent 가 \emph{외부지식 없이} 본문 전제(앞 식·AL·학부 기본)만으로 각 boxed 결과를 재현. (agent 재현 테스트)
- **G-ground**: 모든 본문 가정식이 AL-# 인용 + 근거 cite + 검증 DOI(또는 정직 FLAGGED). 무태그 established 0건. (대조)
- **G-noungrounded(5-30)**: 논문/교과서 근거 없는 무리한 가정 0건. 발견 시 방향-3 재작성 기록. macdonald류 오귀속 0건. (대조)
- **G-dim**: 모든 식 차원 정합. (검산)
- **G-noconvleap**: cap/clip/softplus/step/$\max$/$\min$/Heaviside 정의식 0; 근거없는 수치 임계값 0; solver 구현 0(P1). (scan)
- **G-cross**: $s_\phi$·$V_{n,\drive}$·$n^\eff$·keystone·AL번호 가 RB_CHARTER 규약 1~5 와 일치. (대조)
- **G-latex**: 컴파일 무결(eqref/cite/label resolve, 중복 0, 환경 balance). (검산)
- **G-honest**: 검수표 3-tier(통과/조건부/미확정), 보고-파일 일치. (대조)

**학부 전제 기준선(G-undergrad 의 "외부지식 없음" 정의)**: 학부 2~3학년 — 화학열역학($G,H,S$, 화학퍼텐셜, $\Delta G=-RT\ln K$), 전기화학(Nernst, 전극전위, Faraday), 미적분(전미분·치환적분·Taylor 1차), 선형대수(고유값 불요), 기초 통계(분포·평균). 그 이상(Fredholm/DAE/network thermo)은 본문에서 \emph{전제부터 도입}해야 함.

## 다음
Phase 0 (Foundation) 완료. → **Phase 1.1 (Ch1 골격추출, step 17)**. Ch1 = 최대한 심플(열역학 무대 + 극판전위 배리어 낮춤). AL-1~16 기등재분을 S2 에서 확정·보강.
