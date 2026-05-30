# RB_LEDGER_CH1 — Chapter 1 재유도 (Phase 1.1~1.5, step 17–42)

> **장 목표(사용자 5-30)**: "최대한 심플한 열역학적 관점 베이스 + 극판 전위에 따른 배리어 낮아지는 현상 위주."
> **입력**: `graphite_ica_consolidated_ch1.tex`(886줄, 전수 정독), `_body_ch1_v2.tex`, `RB_CHARTER.md`, `RB_AL_MASTER.md`, `RB_REFERENCES_DOSSIER.md`.
> **상속 규약**: RB_CHARTER 1~5 ($s_\phi$/$V_{n,\drive}$/$n^\eff$/keystone/AL). **상속 가독 gate**: RB_AL_MASTER 3부.

---

# Phase 1.1 — 골격추출 (step 17–20)

## S1-a. 핵심식 흐름 (보존 대상 — 방향-2: 순서·역할 유지)

| 순서 | label | 식 | 역할 | 상속 AL |
|---|---|---|---|---|
| 1 | eq:charge_balance | $Q_\cell q=Q_\bg(V_n,T)+\sum_j Q_{j,\tot}\xi_j$ | ★무대: $V_n$ 을 결정하는 중심식 | AL-1 |
| 2 | eq:ocv_implicit | 평형서 $\xi_j=\xi_{\eq,j}$ → $V_{n,\OCV}$ | OCV=전하보존 평형 특수해(외부 lookup 아님) | AL-1 |
| 3 | eq:logistic | $\xi_{\eq,j}=[1+e^{-(V_n-U_j)/w_j}]^{-1}$, $w_j=RT/F$ | 평형 진행률(열역학 무대) | AL-2,4 |
| 4 | eq:dxidV | $\partial\xi_\eq/\partial V_n=\xi(1-\xi)/w_j$ | 저온서 $w\downarrow$→peak 좁아짐(평형이면 짧은 꼬리) | AL-2 |
| 5 | eq:Aj | $\mathcal A_j=s_{\phi,j}F(V_{n,\drive}-U_j)$ | 구동력(극판 전위 친화도) | AL-11, CHARTER1,2 |
| 6 | **eq:Geff** | $\Delta G_{\eff,j}=\Delta G_{a,j}-\chi_j\mathcal A_j$ | ★★극판 전위에 의한 배리어 낮춤(장 핵심) | AL-11 |
| 7 | eq:kact | $k_j^\mathrm{act}=\nu_j e^{-\Delta G_{\eff,j}/RT}$, $\nu_j=k_BT/h\cdot\kappa$ | Eyring 속도상수 | AL-10 |
| 8 | eq:dxidt/dxidq | $d\xi_j/dt=k_j(\xi_{\eq,j}-\xi_j)$ | 동역학 완화(꼬리 주역) | AL-12 |
| 9 | eq:single_kernel | $r(q)=r(q_a)e^{-(q-q_a)/L}$, $L=|I|/(Q_\cell k_j)$ | single-mode kernel; 저온·고율서 $L\uparrow$ | AL-12 |
| 10 | eq:L_of_G | $L(G)=(|I|/Q_\cell k_0)e^{(G-\chi\mathcal A)/RT}$ | ★barrier→length 지수 매핑(stretched 근원) | AL-13 |
| 11 | eq:spectrum | $A_L=\rho_G(G(L))(RT/L)A_0$ | barrier 분포→spectrum(변수변환 보존) | AL-13 |
| 12 | eq:kernel_integral | $d\Theta_\tail/dq=\int A_L(1/L)e^{-(q-q_a)/L}dL$ | 관측 tail = kernel integral | AL-14 |
| 13 | eq:dVndq_full | $dV_n/dq=[\dots]$ 전미분 | 관측 $dQ/dV_n,dV/dQ$ | AL-1 |
| 14 | 피팅식 S1–S5 | 평가순서 + falsification N1–N4 | ★최종 산출(피팅 가능 닫힌식) | — |

→ 인과 사슬: 관찰 → 무대($V_n$, eq1) → 평형(eq3) → 평형만으론 반대(eq4) → 동역학·배리어 낮춤(eq5–9) → spectrum(eq10–12) → 관측·피팅식(eq13–14). **이 흐름 전체 보존.**

## S1-b. 가정 전수 목록 (grounding 감사 대상 — Phase 1.2)

기등재(RB_AL_MASTER): AL-1(전하보존)·AL-2(logistic 화학퍼텐셜)·AL-3(staging)·AL-4($w=RT/F$)·AL-10(Eyring)·AL-11(배리어 낮춤 $\chi\mathcal A$)·AL-12(1차 완화)·AL-13(지수 매핑·변수변환)·AL-14(stretched=연속합)·AL-15(Marcus bound)·AL-16(non-uniqueness).
Ch1 S2 에서 채울 여유번호: AL-5~9(= $Q_\bg$ chemical capacitance, 단조성 floor, $V_{n,\app}$ 분극 $R_n$, 해존재조건, keystone 2-state 선형화), AL-17~19.

## S1-c. ★ 심플화 대상 식별 (사용자 "최대한 심플" vs 방향-2 "흐름 보존" 긴장)

현재 886줄 Ch1 에서 \emph{핵심 인과 사슬과 무관한 부수적 복잡성}(GS-4 계산편의 비약과도 겹침) — 재유도 시 본문에서 덜거나 부록/각주로 강등 후보:

| # | 현재 요소 | 판정 | 처리(권고) |
|---|---|---|---|
| C-1 | eq:clamp ($\operatorname{sign}\cdot\min$ flux clamp, L381) | **GS-4 위반**(min 정의식, smooth 아님) + 부수 | 본문 제거. 유한전류 제약은 eq:kphys 의 $k_{j,\mathrm{current}}$ 직렬항으로 충분(smooth). |
| C-2 | eq:klim_comp 다중 병목 4항 나열(transport/site/diff/current, L358) | 부수(핵심은 "병목 존재") | 본문은 $1/k_\phys=1/k_\mathrm{act}+1/k_\mathrm{lim}$ 한 줄 + 병목 종류는 각주. |
| C-3 | mdframed "실무 팁"(softplus/capped, L387) | GS-4 경계(이미 "본문 아님" 표기) | 제거(피팅 실무는 Ch6 부록). |
| C-4 | eq:charge_balance_rel(상대 기준형, L193) + 총용량정합 §capmatch | 부수(피팅 실무) | Ch6 또는 각주로 강등. |
| C-5 | 준정상 닫힌형(L546) + eq:dVndq_full 완전형 분모 둘째항 | 부수(Ch6 수치와 중복) | 본문은 준정상 환원형, 완전형은 각주. |
| C-6 | $V_{n,\drive}\approx V_{n,\app}$ reduced(L308) boundbox | 부수 | 각주(기본 $V_\drive=V_n$ 만 본문). |

**보존(절대 — 장 핵심)**: 전하보존 무대 / logistic 평형 + 저온 거동 / **극판전위 배리어 낮춤 $\Delta G_\eff=\Delta G_a-\chi\mathcal A$** / Eyring rate / 1차 완화 + L / 지수매핑 + spectrum + kernel integral / 피팅식 S1–S5 / falsification.

## S1-d. 본 장 입력 결함(Phase A/B + 재유도 최우선 검증점)
1. **★ AL-14 stretched grounding 정밀도(Phase 0 Open Issue)**: "고정 barrier 분포 → T-의존 stretched"가 svare2000+johnston2006+lindsey1980 으로 \emph{완전히} 닫히는지 = 이 문서 핵심 물리. Phase 1.3 재유도서 직접 확인, 못 닫으면 FLAGGED.
2. closure 비선형성 귀속(Phase A Ch1 HIGH): Ch1 본문엔 closure 상세 없음(§kernel 까지). closure 는 Ch6. Ch1 은 kernel integral 까지만 — 단순.
3. $Q_p$ 단위 무차원 오기(Phase A MED) → notation 정정($Q_p$=C).
4. keystone(Level A) 한정 표현(CHARTER4): "배리어 낮춤"=Level B 함의 용어를 Ch1 결론식에 쓰지 않음(현재 keybox 가 이미 처리; 유지).
5. JCP2017(closure)는 Ch1 아닌 Ch6 — Ch1 refs 에서 제외.

## Phase 1.1 Gate
- G-flow: 핵심식 14개 흐름 목록화 ✅
- 가정 전수 목록 + 심플화 대상 6건 + 입력 결함 5건 식별 ✅
- **PASS** (step 17–20). 다음: Phase 1.2 grounding 감사.

---

# Phase 1.2 — grounding 감사 (step 21–25)

**방법**: 워크플로 wf_f9602d7e-ada, 6 agent(영역 A/B/C 감사 3 + AL-14 닫힘 검증 3 렌즈), Ch1 886줄 전수 정독 + 직접 재유도. 31개 가정 판정.

## S2-a. 판정 요약 — 대부분 GROUNDED (논문 실인용 확인)
- **무대·평형(A)**: charge_balance(doyle1993/newman 실인용)·logistic(mckinnon1983/bazant2013, 무비약 재유도 통과: $RT\ln[\xi/(1-\xi)]=F(V_n-U)\Rightarrow$ logistic)·dxidV(수치 25.68/22.23 mV 검증)·ocv_implicit·solexist(IVT) = 전부 GROUNDED.
- **동역학·배리어(B)**: ★eq:Geff(극판전위 배리어 낮춤, 장 핵심; evanspolanyi1938 BEP + bazant2013 실인용)·kact(eyring1935, prefactor $k_BT/h$)·keystone 2-state 선형화(직접 재유도 통과: $k=r^++r^-$, $\chi\mathcal A$=mobility scale Level A 방향성X)·single_kernel·kphys·Marcus bound(BOUNDED) = GROUNDED.
- **spectrum·closure(C)**: L_of_G(지수매핑, 무비약)·spectrum(변수변환 밀도보존 $A_L dL=\rho_G dG$ 재유도 통과)·kernel_integral·xi_dist = GROUNDED.

## S2-b. ★ AL-14 핵심물리 닫힘 검증 (3 렌즈 전부 YES_BOUNDED)
| 렌즈 | claim | 결과 | 근거 |
|---|---|---|---|
| johnston2006 | kernel integral = 연속 지수합 → stretched | YES_BOUNDED | Laplace 변환형이 완전단조→stretched/power-law. $A_L=\delta$서 단일지수 복귀. $1/L$=진행률 도함수 출처(임의가중 아님) |
| svare2000 | 고정 $\rho_G$ + T-의존 지수매핑 → 저온 긴 꼬리 | YES_BOUNDED | 직접 재유도: $\ln L=\ln L_0+G/RT$ → 저온서 $\ln L$ spread $\propto\sigma_G/RT$ 확대 = stretched. svare2000 메커니즘과 정확 정합 |
| lindsey1980 | stretched ↔ 완화시간(length) 분포 등가 | YES_BOUNDED | KWW $\leftrightarrow\rho(\tau)$ 라플라스 등가의 $q$-좌표 instance |

→ **결론: Ch1 핵심 물리(관측 tail = relaxation-length spectrum kernel integral; 저온 긴 꼬리 = 고정 barrier 분포의 지수매핑) 는 닫힌다(BOUNDED).** FLAGGED 불필요. **gap(데이터 영역)**: $A_L$ 특정 형태→정확한 stretched 지수, 그리고 fast-ion/dielectric→graphite 적용이 본 작업 기여(BOUNDED). 이 gap 은 정직하게 본문에 BOUNDED 로 명시.

## S2-c. 무근거·HIGH 결함 5건 → Phase 1.3 재작성 조치
| # | 결함 | tier | 조치 |
|---|---|---|---|
| F-1 | **eq:clamp** ($\operatorname{sign}\cdot\min$ flux clamp, L381) | **UNFOUNDED_LEAP/HIGH** | **본문 제거**. 유한전류 제약 = $1/k_\phys=1/k_\mathrm{act}+1/k_\mathrm{current}$ 직렬항(smooth)만 (방향-4) |
| F-2 | softplus/capped 실무팁(L387) | UNFOUNDED_LEAP/MED | Ch1 제거 → Ch6(피팅 실무) |
| F-3 | ε_tol 수치근거 부재(L607) | FLAGGED/MED | Ch1 비포함 → Ch6서 데이터 noise 기반 또는 FLAGGED (Phase A Ch6 CRITICAL 과 동일 결함) |
| F-4 | **ledger 번호 불정합**(tex local AL ↔ master global AL) | FLAGGED/HIGH | **ch1_rebuilt 는 master global AL-# 단일체계** (장내 local 번호 폐기) |
| F-5 | Plan A 선형화+ratio closure(eq:selfcoupling/eq:closed) | BOUNDED/MED | **Ch6 이관**. Ch1 은 volterra 형태 + 이중계상 경고까지만(심플화) |

## S2-d. AL master 보강 (AL-5~9 등재 — 본 Phase 산출)
- AL-5 GROUNDED: chemical capacitance 단조성 $\partial Q_\bg/\partial V_n\ge\epsilon_Q>0$ (bazant2013; $\epsilon_Q$=수치 floor, BOUNDED).
- AL-6 GROUNDED: apparent 전위 분극 $V_{n,\app}=V_n+s_I|I|R_n$ (bardfaulkner/newman; 선형 $R_n$ BOUNDED 소과전압).
- AL-7 GROUNDED: 해 존재 조건 = charge balance 가해성(IVT).
- AL-8 GROUNDED: 총용량 정합 $Q_\cell$ = 시종점 전하 차분(charge balance).
- AL-9 GROUNDED: 전하보존이 $V_n$ 결정(외부 lookup 아님; doyle1993/newman) — tex 의 \AL{9} 와 동기화.

## Phase 1.2 Gate
- G-ground: 31 가정 전부 판정(AL+cite+DOI 또는 정직 FLAGGED) ✅
- G-noungrounded: 무근거 비약 5건 적발 + 재작성 조치 명시 ✅
- AL-14 핵심물리 닫힘 확정(BOUNDED, gap 명시) ✅
- **PASS** (step 21–25). 다음: Phase 1.3 무비약 재유도.

---

# Phase 1.3 — 무비약 재유도 (step 26–33)

**산출**: `Claude/docs/graphite_ica_ch1_rebuilt.tex` (529줄). 흐름 14식 보존 + 학부 무비약 + global AL-# + 심플화 반영 + 극판전위 배리어 낮춤 위주.

## S3-a. 재구성 주요 결정 (방향 반영)
- **logistic 무비약 유도 추가**: 화학퍼텐셜 $\mu=\mu^0+RT\ln[\xi/(1-\xi)]+\Omega(1-2\xi)$ → 평형조건 → ($\Omega=0$) 대수로 logistic 도출(원본은 결과만 제시, 재구성은 중간 단계 명시).
- **극판전위 배리어 낮춤(§rate) = 장 핵심으로 전진 배치**: eq:Geff $\Delta G_\eff=\Delta G_a-\chi\mathcal A$ 를 BEP/Butler-Volmer grounding(evanspolanyi1938/bazant2013)으로 무비약 + keystone(Level A=mobility, 방향성X) 한정 유지.
- **심플화(사용자 "최대한 심플", S2-c 6건 반영)**: eq:clamp(sign·min) **제거**(GS-4); softplus 실무팁·Plan A closed-form(eq:closed)·ε_tol·상대기준형·총용량정합 → **Ch6/각주 이관**. closure 는 §kernel 에 \emph{형태}(volterra + 이중계상 경고)까지만, \emph{푸는 방법}은 Ch6 명시.
- **AL global 단일번호**(F-4 해소): tex local \AL{n} 폐기, master AL-# 사용(charge_balance=AL-1·logistic=AL-2·staging=AL-3·w=AL-4·V_app=AL-6·Eyring=AL-10·Geff=AL-11·완화=AL-12·spectrum=AL-13·stretched=AL-14·Marcus=AL-15·비유일=AL-16).
- **AL-14 BOUNDED 정직 표기**: stretched grounding boundbox 에 svare2000/johnston2006/lindsey1980 + gap(특정 ρ_G→지수, fast-ion→graphite 적용)을 BOUNDED 명시.
- **부호 CHARTER 정합**: $\mathcal A_j=s_{\phi,j}F(V_{n,\drive}-U_j)$, $V_{n,\drive}=V_n$ 기본 명시, $n_j^\eff=RT/(Fw_j)$ 도입(Ch3/4 전달).
- **DOI 정정 반영**: bibliography 18종 = dossier 검증값(svare2000 저자 Svare/Martin/Borsa, funabiki ea+jes 둘, lindsey 440530, doyle/ohzuku 정정제목).

## S3-b. 정적 검증 (python check_tex.py)
- 환경 balance: document/equation(21)/longtable(2)/enumerate(3)/boundbox(4)/groundingbox/flagbox/keybox/quote/thebibliography 전부 균형 ✅
- label 31 / ref 21: **undefined ref 0**, unused label 10(eq:Aj/Geff/dVdV 등 boxed — LaTeX 무해, 추적성; Phase 1.5서 일부 \eqref 보강 검토)
- cite 18 / bibitem 18: **undefined cite 0, uncited bibitem 0** ✅
- **GS-4 leak: `\max`(L258)·`\min`(L288) 2건 = 정의식 아님, "이런 절단 쓰지 않는다"는 \emph{금지 서술}** (false positive, GS-4 준수 문장). eq:clamp 제거 확인 ✅
- ε_tol 0, macdonald 잔재 0, svare2000 인용 3 ✅

## Phase 1.3 Gate
- G-flow(흐름 14식 보존)·G-latex(정적 통과)·G-noconvleap(정의식 0, 금지서술만)·G-cross(CHARTER 규약) 정적 PASS.
- G-undergrad·G-noleap·G-ground 는 Phase 1.4 적대검증서 확정.
- **PASS(정적)** (step 26–33). 다음: Phase 1.4 적대검증(워크플로 w388rbnzf).

---

# Phase 1.4 — 적대검증 (step 34–38)

**방법**: 워크플로 wf_c41f2c89-236, 7 agent(5렌즈 리뷰 + 적대 재검증). all_findings 49건(OK 16 / MEDIUM 14 / LOW 17 / HIGH 2; 5렌즈 중복 포함). dedup 후 고유 결함 정리.
**★ host 정정 이력(GS-5)**: 첫 파싱서 요약 잘림 + cp949 인코딩 에러로 "MEDIUM 1"로 오판하고 성급히 커밋 시도 → 그 커밋이 취소됐고, JSON 전건 재파싱으로 정확 집계. (적대검증 agent 자신도 finding #34 에서 "도구결과 수신 전 성급 판정" 자기적발 — 같은 실패 양식.)

## S4 결과 — dedup 후 실결함
| # | 심각도 | 위치 | 결함 |
|---|---|---|---|
| 손상-1 | 컴파일차단 | §charge OCV (L186-191) | `\begin{equation}\textbf{}` + 고아 `\end{equation}을 잘못 닫지` + 인라인 누출 → OCV 식 통째 깨짐 |
| 손상-2 | 컴파일차단 | keystone (L256-257) | `\chi_j\mathcal A_j$` 여는 `$` 누락 + "방향은 열역학 전담하고 χ_j가 정한다"(논리 꼬임) |
| 손상-3 | 빌드결함 | notation 표 (L117-127) | ρ_G·A_L·L 행 중복(각 3~5회) — host 전수정독 추가 적발(워크플로 미포착) |
| #20 | HIGH | fiteq (L414-420) | 유도 연결 끊김: dQ=Q_cell dq 미명시·역수 단계 생략·Q_p 정의 끊김 → 학부 재현 불가 |
| #14 | MED | Geff (L233) | 선형 배리어 낮춤 -χA 의 "선형" 출처(Marcus 접선) 미명시 |
| #15 | MED | kact (L247) | Eyring prefactor k_BT/h 학부 범위 밖 — 비-기반 충분성 분리 필요 |
| #18 | MED | spectrum (L355) | A_0 가 변수변환 산물 아닌 별도 가중임 미분리 |
| #19 | MED | kernel (L367/373) | r(q_a) 흡수 비약 + 1/L 두 출처(kinematic vs Jacobian) 미구분 |
| #21 | MED | fiteq (L424) | Θ/Q_p 이중정의(§8 적분량 vs §9 ΣQξ) 일치 미명시 |
| #28 | MED | charge (L177) | eq:solexist 치역 조건(well-posedness) 누락 |
| #37 | MED | spectrum/notation | ρ_G 단위 mol/J vs 정규화 ∫ρ_G dG=1 충돌 |
| #39/#45 | MED | keystone | Level A=Level B "detailed-balance 극한/ξ_ss→ξ_eq" 한정어 미명시(CHARTER step4) |
| #40 | MED | eq:Aj | n_eff forward-ref(ideal n^eff=1; 일반형 Ch3) 누락 |
| s_φ | MED | logistic/dxidV | 평형조건엔 s_φ 있으나 logistic 최종형·dxidV 에서 탈락(적대검증 confirmed) |
| (LOW 다수) | LOW | — | 이중계상 box ξ*/Θ_0·저온 ideal한정·L 무차원 extent·AL-14 cite 3종 병기·차원주석 A=C/s 등 |

(비결함: finding #34 메타 "BLOCKED 오보고 자기정정" = 에이전트 자기수정, 실파일 결함 아님.)

# Phase 1.5 — 수정·재작성 + Decision Gate (step 39–42)

## S5 수정 적용 (ch1_rebuilt.tex, 13건 Edit)
1. **손상-1**: OCV 식 정상 복구(eq:ocv_implicit) + solexist 치역조건(#28) 신설.
2. **손상-2**: keystone `$` 복구 + 논리 정정("방향은 열역학 전담, χA는 방향없는 속도scale") + r± 국소상수 전제(#11) + 한정어(#39/#45).
3. **손상-3**: notation 중복 행 제거(ρ_G·A_L·L 각 1회) + ρ_G 단위 mol/J→1/J(#37) + L 무차원 extent 명시.
4. **#20 HIGH**: fiteq 유도 연결 — Θ/Q_p 선제정의(#21), dQ=Q_ext=Q_cell dq, 역수 단계, 분모 유효범위(#9).
5. **#14**: Geff 선형성 = Marcus 포물면 꼭지점 접선(소구동력 1차) 유도 추가.
6. **#15**: Eyring — Boltzmann 인자만으로 충분(L 비로 k_0 상쇄), prefactor k_BT/h는 TST 인용으로 분리.
7. **#18/#19**: A_0=물리적 가중(변수변환 산물 아님) + 1/L 두 출처(kinematic vs Jacobian RT/L) 구분.
8. **#36**: stretched 근거 3종(svare2000+johnston2006+lindsey1980) 병기 + BOUNDED 연결.
9. **#40**: eq:Aj 직후 n_eff=RT/(Fw)=1 ideal 기본 + 일반형 Ch3 forward-ref.
10. **s_φ**: logistic 균형식·eq:logistic·eq:dxidV 에 s_φ 보존(eq:Aj 부호 일관) + 저온 ideal 한정.
11. **Volterra box**: ξ*→Θ_0 통일 + q→∞ 수렴 명시.

## S5 최종 무결성 (python final_check, 13 수정 후)
환경 balance NONE mismatch · undefined ref 0 · undefined cite 0 · uncited bibitem 0 · **duplicate label 0** · **깨진 텍스트 0(잘못닫지/footnotetext/broken-keystone 전부 0)** · **notation 중복 제거(ρ_G·L 행 각 1)** · ρ_G mol/J 잔재 0 · s_φ logistic boxed 반영 · ocv_implicit 복구 · macdonald 0 · svare2000 2(cite+bibitem) · 542줄.

## Phase 1 종합 Gate
- G-flow ✅(14식 보존) · G-noleap ✅(Marcus접선·Eyring·fiteq 유도 보강) · G-undergrad ✅(fiteq 재현 가능화) · G-ground ✅(AL+DOI, stretched 3종) · G-noungrounded ✅(무근거 0, AL-14 BOUNDED) · G-dim ✅ · G-noconvleap ✅(정의식 leak 0; max/min은 금지서술) · G-cross ✅(CHARTER s_φ·V_drive·n_eff·keystone 한정어) · G-latex ✅(컴파일차단 3 손상 해소, 균형·resolve) · G-honest ✅(3-tier, host 오판 정정 기록)
- **PASS** (step 34–42). → **Decision Gate: 사용자 검토 대기.**
