# RB_LEDGER_CH2_FINE_REVIEW — Ch2 절별(fine) 적대검수 + 정정 Result (2026-06-02 자율)

> 방법: §절마다 1 agent(13 병렬, 9렌즈 G-follow·G-usable 1급 + refute + 최약점 + 빈통과금지). 거친 3렌즈(물리/수학/정합)가 놓친 결함 적발. 파일: `Claude/docs/graphite_ica_ch2_rebuilt.tex`.

## 적발 결함 (severity별, 절별)

### CRITICAL
- **C1 [158·486·491·466] h_bg 단위/명칭 모순**: 기호표 158 이 h_bg 를 "entropy coefficient, V/K"로 명명 — 그러나 entropy coefficient=J/(mol·K), ∂V/∂T=V/K 는 nF 만큼 다름(Π_j 행 151 은 옳게 구분). h_bg 는 "background **전위** 온도계수(∂V_bg,eq/∂T)". 486 의 (∂V_bg,eq/∂T)_{bg state} 고정변수 무정의. → 158 의미칸 "background potential temperature coefficient(전위형)"로 교정 + 관계식 ΔS_bg=−F·h_bg(n=1) 1줄 + 486 고정변수 (·)_{Q_bg} 명시.
- **C2 [464–468] eq:ch2_consistency 거짓 등식(double-counting 차단 미닫힘)**: OCV 방식 LHS=s^conv|I|T(∂V_OCV/∂T)_q 의 분자는 (∂ξ_eq/∂T)_{V_n} 전항(U'_j 항 + width항 −(V_n−U_j)w'_j/w_j²)을 담고 분모 D_q 로 나뉨. entropy-basis RHS 는 ΔS_j∝U'_j 만 담아 width 항·D_q 정규화 누락 → 두 변 일반적으로 ≠. "같은 양" 등호 박스가 거짓. → eq:ch2_implicitT 엄밀 항등식에서 재유도하거나, **BOUNDED 명시**: ΔS_j(U'_j) 성분만 정합 대상, width(w'_j)·D_q 정규화는 OCV 방식 고유 → 두 방식은 \*부분적으로만\* 같은 정보(strict 등호 철회, double-counting 차단은 reaction-entropy 성분 한정).

### HIGH
- **H1 [137·145] χ_j 미정의(G-follow)**: (L5) χ_j A_j 의 mobility 가속 χ_j 정의·기호표 부재(137·368·732·879 사용만). → (L5) 직후 "χ_j∈[0,1] 무차원 mobility 가속 인자; Ch1 k_j∝exp(−(G−χ_j A_j)/RT) 지수 보정" 정의 + 기호표 등재.
- **H2 [209–233·255] ocvT box s_φ silent drop**: boxed eq:ch2_dVocvdT 는 일반 외양이나 닫는 eq:ch2_dxidV/dxidT·D_q>0 증명·물리해석이 전부 s_φ=+1 특수형. 충전(s_φ=−1) 혼재 시 부호 무너짐. → 박스 직전 BOUNDED "이하 logistic 분자·분모는 방전 s_φ=+1 특수형; 일반은 ξ(1−ξ)/w → s_φξ(1−ξ)/w" + 255 문장에 "방전 s_φ=+1 에서".
- **H3 [254–256] w'_j>0 가 ideal 한정인데 일반 결론에 사용(BOUNDED)**: → boundbox 안 "w'_j>0 은 ideal w=RT/F 한정; non-ideal 부호 미정 → 둘째항 부호반전 결론도 ideal 내 한정" 부등식으로 닫기.
- **H4 [344·357·362] Q_rlx 3항 Bernardi 오귀속+double-count**: eq:ch2_srcdecomp 가 q_rev+q_irr(CHARTER 2항)에 Q_rlx^cand 3항 추가, 357 이 이를 Bernardi balance 로 단정(오귀속). Q_rlx 가 q_irr 와 double-count 위험·차원[W] 미검산·부호 미정. → 357 "Bernardi(2항)+본 장 후보 확장항(hypothesis, \cite 없음)", Q_rlx 별개성 명시(휴지 floor=eq:ch2_qirrkin_ext 와의 관계), 분해식 항별 [W] 검산, 362 표 Q_rlx 부호 "sign-open".
- **H5 [379–383·393–402] revOCV per-transition→cell collapse 무비약(s^conv·|I| 환산 누락)**: eq:ch2_qrev(I_jΠ_j, 부호전류)→eq:ch2_revOCV(s^conv|I|T∂V_OCV/∂T) 의 ① 부호전류→s^conv|I| ② Σ_j I_jT∂U_j/∂T→|I|T∂V_OCV/∂T collapse 가 유도 없이 동시 발생. → 박스 직전 환산 등식 + 좌우 변환 근거 1줄(②=eq:ch2_dVocvdT 집계, ①=부호규약). 또는 BOUNDED "정전류·집계 OCV 하".
- **H6 [466·491·507] bg 항 /F 비대칭 + V_bg,eq↔Q_bg 좌표 미연결**: 정합식 bg 항 s·T·h_bg·Q̇_bg^prog 은 charge-rate(C/s) 기반, transition 항은 mole-flux(/F) 기반 → 물리기반 비대칭. h_bg(온도경로)와 Q̇_bg^prog(V_n 경로) 좌표 연결식 부재. → ∂Q_bg/∂T|_{V_n}=−(∂Q_bg/∂V_n)h_bg 류 항등식 1줄 + V_bg,eq vs V_n 관계 명시.
- **H7 [568] η 절댓값이 동부호 증명 무력화**: η=Σ(|J_{n,j}|F/|I|)|η_j| 의 절댓값이 538–548 의 J_{n,j}Fη_j≥0 동부호 증명을 우회, Σ|J|F≠|I| 시 q_irr=|I|η 항등 깨짐. → η=Σ(J_{n,j}F/I)η_j (절댓값 제거, 부호정합으로 ≥0 이미 닫힘) 또는 단일 우세 transition BOUNDED.
- **H8 [575] η_ohm=R_n 분극이 P3-1 위반**: η=η_kin+η_ohm+η_conc 의 η_ohm 을 R_n 분극에 귀속 — 그러나 619–629 P3-1 은 R_n≠heat resistance. → η_ohm → R_{n,eff} 분극(R_n 아님)으로 정정 + transition별↔메커니즘별 분해 동치/별개 1줄.
- **H9 [646–661] §rest under-claim(BOUNDED)**: 휴지 비가역 floor 가 eq:ch2_qirrkin_ext(609)로 이미 닫힘(r_j≠0,dξ/dt≠0 → ≥0 정량)인데 flagbox 가 "비가역 성분 존재만 보장·분리 미정"으로 강등. → eq:ch2_qirrkin_ext 휴지 좌표 재인용(q_irr,rlx,j=(Q/F)g''_j k_j r_j²≥0) + flagbox "near-eq floor 정량확정; Ch3–4 가 닫는 것은 가역 entropic 배분·비선형".
- **H10 [697·700·708·705] §thermal_tail 채널 equivocation**: 제목/도입의 "비가역열"(q_irr=|I|η)≠유도식 q_irr,kin(σ_j 채널). single-mode exp 형은 post-peak k_j·ξ_eq const 근사인데 미명시. calorimetry cross-check 시 ohmic/transport 선차감 누락. → 제목/도입 "kinetic-lag 성분"으로 한정 + exp 근사 명시 + flagbox 에 ohmic/transport 차감 추가.
- **H11 [754·757] §ident G-usable 끊김**: Q_bg/h_bg collinearity 를 "분리 곤란"으로 표시만 하고 해소 실험 미매핑(나머지 5쌍은 매핑됨). consistency 제약↔OCV series 측정 연결 누락. → 표/enumerate 에 Q_bg/h_bg 해소경로(OCV SOC 분해+bgsplit) + "OCV series 가 eq:ch2_consistency 좌변 고정" 1줄.
- **H12 [679·682] §feedback**: root-find self-consistency 가 P3-3 4분류(implicit/수치/논리공백/물리충돌) 중 무엇인지 미명시(실은 implicit 수치해법, 단조성 floor 로 유일). 계산순서 5)가 2항인데 분해식은 3항. → P3-3="implicit 비선형(수치해법=부록 B), D_q≥ε_Q>0 로 유일·수렴" 명시 + 5)에 Q_rlx 제외 명시.

### MED (정정 권장)
- M1 [286·299] s_φF=(부호 s_φ)×(n^eff=1)×F 분해 1줄(일반형 s_φ n^eff F).
- M2 [326] Eyring "Arrhenius intercept"가 k_BT/h 의 약한 T의존 무시 시만 — "온도무관 인자 e^{ΔS_a/R}"로 표현 정정.
- M3 [294–297] Gibbs-Helmholtz 적용 3전제(정압·준평형 OCV·∂ΔG/∂T≡−ΔS 정의동치) 명시.
- M4 [604·585] flux 기호 충돌: J_j≡dξ_j/dt[1/s] vs J_{n,j}=Q_{j,tot}(dξ/dt)/F[mol/s] 단위 구분 1줄.
- M5 [462·430] 정합 제약 평형경로 한정 + 비평형선 entropy basis 만 유효 명시 / s^conv_{rev,ξ,j} 부호정의(s_φ,j·heat-positive).
- M6 [360] ΔS_j → ΔS_{rxn,j} 첨자 통일.
- M7 [690] 되먹임 boundbox 흡열(q_rev<0) 반대분기 추가.
- M8 [763·767] ident: ∂U_j/∂T 분해는 SOC 분리 필요(AL-23) 위계화 + calorimetry 부재 한계(가역/비가역 분해 불가) 거울 1줄.

### LOW (ledger 기록, 선택)
- L: ε_Q [C/V] 단위(130), q_rev,j/q_rev 첨자규칙(148), V_eq,j 닫힌식 기호표 병기(153), Π_j "Peltier-type" 한정어, w_j>0 명시(543), ISBN-13 통일·degrootmazur "(book)" (782·900), 검수표 FLAGGED "통과" 라벨 명확화(804·821), AL-20/21 최초등재 위치(773).

## 정정·빌드·커밋 (완료)
- 정정 적용: **CRITICAL 2(C1·C2) + HIGH 12(H1~H12) + MED 5(M1·M2·M4·M6·M8)**. 전부 기존 줄에 BOUNDED/명시 추가 또는 라벨·부호·단위 교정(식 본체 재유도 0, 식별자·라벨 보존). LOW + M3/M5/M7 은 ledger 기록(선택, 미적용).
- 검증(master 독립): xelatex 2-pass GREEN(`!` 0, undefined ref/cite 0, 21p). 민감 정정 4개 실텍스트 확인 — C2 BOUNDED(485–489행 "reaction-entropy 성분 한정")·H4 Q_rlx(367 "Bernardi 2항+후보 확장항 hypothesis")·H7 η(595행 절댓값 제거 η=Σ(J_{n,j}F/I)η_j≥0)·C1 h_bg(전위 온도계수 교정).
- tex **909→947줄**(+38). 커밋·push(main+rb-rebuild).
