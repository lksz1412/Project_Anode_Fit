# RB_LEDGER_CH4_FINE_REVIEW — Ch4 절별(fine) 적대검수 + 정정 Result (2026-06-02 자율)

> §절마다 1 agent(14 병렬, 9렌즈). 파일 `Claude/docs/graphite_ica_ch4_rebuilt.tex`. Ch4=entropy-production 발열 정량화. Ch2 결함의 Ch4 재발(consistency width·collapse·Q_rlx) + 신규 다수 적발.

## 적발 결함 (정정 대상 CRITICAL/HIGH/주요 MED)

### CRITICAL
- **C1 [616–621 §revxi] eq:ch4_consistency width 항 누락 거짓 등호(★Ch2 재발)**: agent 직접 미분 입증 — LHS |I|T(∂V_OCV/∂T)_q 는 (∂ξ_eq/∂T)_{V_n} 경유 width 온도계수 −(V_n−U_j)w'_j/w_j² 포함, RHS 는 ΔS_j(∝∂U_j/∂T)만 → 일반적으로 ≠. 준평형 caveat 도 width 항(완전평형서도 잔존) 못 막음. → C2(Ch2)와 동일 처방: BOUNDED "정합은 reaction-entropy 성분(∝∂U_j/∂T)에 한정; width(w'_j)·D_q 정규화는 OCV 고유 → 부분적으로만 동일정보; strict 등호 철회 또는 ∂w_j/∂T=0 명시 전제".
- **C2 [224·228 §inherit] eq:ch4_Ij 자기참조**: 본문이 "Ch3 \eqref{eq:ch4_Ij} 와 동일"이라며 바로 그 식(228)을 가리킴 → "식(N)은 식(N)과 동일" 동어반복 인쇄. → \eqref 자기참조 제거, "Ch3 (L2) kinetics 의 I_j 정의와 동일 — 본 장 재기입" prose 화.
- **C3 [446 §tr / 247 §eta_single] η 정의 s_φ 불일치 재발**: keybox eq:ch4_eta_def 는 η_j≡V_drive−V_eq,j(s_φ 무), boxed eq:ch4_affinity_eta(446)는 η_j=s_φ[V_drive−V_eq,j](s_φ 부착) → 같은 기호 2정의(충전서 부호 갈림), 라인 440 "1~3단계 s_φ 미포함" 자기진술과 모순. → 446 을 keybox 와 동일 η_j=V_drive−V_eq,j 로 통일하고 s_φ 는 𝒜_j scale 인자(η 밖) 또는 "방전 s_φ=+1 한정, 충전 Ch5" 명시.

### HIGH
- **H1 [336–337 §irr] 합≥0 ⇏ 항별≥0(무비약 위반)**: 2법칙은 합 Σ J_α X_α≥0 만 보장(cross-coupling 시 개별 항 음수 가능). "각 항 정렬→비음"을 일반 성립처럼 서술. → "합 비음(2법칙); 계면 transition 단일 공액쌍이라 항별 ≥0 은 §tr 부호 보조정리에서 별도 증명" 분리.
- **H2 [330 §irr] Onsager 약-귀속**: Tσ=ΣJX≥0 은 de Groot–Mazur/2법칙; onsager1931 은 reciprocal relations(L_αβ 대칭) — 본 식 근거 아님. → 본 식 근거 degrootmazur1962·prigogine1967 로 한정, Onsager 는 transport L_αβ 절(AL-47)로 재배치.
- **H3 [292·307·698 §decomp/§rest] Q_rlx "확정" over-claim + 기호 단절**: 4-분해 Q_rlx,n(292) 독립항·"확정 분해"(307) 주장 vs §rest flagbox "정량 분리 비율 미확정·calorimetry 전제" 후퇴 + §rest 기호 Q_{ξ,rlx}(698)와 Q_{rlx,n} 동일성 미명시. → "확정"을 "비가역 floor ≥0 확정, 정량 분리 비율 calorimetry 검증 전제"로 한정 + Q_{ξ,rlx}≡Q_{rlx,n} 명시 + §rest 가역성분 boxed 식 부여.
- **H4 [290 §decomp] Bernardi/Rao 오귀속**: 4-분해(network EP Σn^eff I_j η_j + Q_rlx)의 근거로 bernardi1985·rao1997 확대 부착 — 그들은 network EP·자유에너지 relaxation 분해 미보증. → "에너지수지 형식=bernardi/rao; network EP 형=degrootmazur·schnakenberg; Q_rlx=본 장 신규" 항별 분리.
- **H5 [515·506 §general] Ch2 특수형 3중 비등가 + 항별≥0 한정 누출**: 특수형을 |I|η(515)·ΣI_jη_j(520)·ΣJ_{n,j}Fη_j(L7) 세 형태로 호명, 위계식 환원점 불고정. 항별≥0 은 detailed-balance 기본형 한정인데 boxed 일반형 무조건 ≥0. → 특수형=Σ_j I_j η_j 로 고정(|I|η 는 단일 우세 transition ideal-width 극한 별도 라벨) + boxed 에 "detailed-balance 기본형 전제; 강구동 Ch5 BOUNDED".
- **H6 [583·576 §revOCV] per-transition→cell collapse 무비약(★Ch2 재발) + ṅ_j 부호인자 충돌**: verifybox 가 ΣI_jΠ_j=s^conv|I|T∂V_OCV/∂T 를 유도 0단계로 "정합" 선언; ṅ_j=I_j/(s_φF) 부호인자가 표 정의(ṅ_j=I_j/F)와 충돌·순환 상쇄. → "정합은 §revxi 준평형 극한 한정, reaction-entropy 정보 동일성만(cell 수치등식 §revxi)" + ṅ_j=I_j/F 로 두고 s_φ 는 ΔS_j 환산서만 → q_rev,j=s_φ I_j Π_j(방전 +1).
- **H7 [274·247 §eta_single] boundbox 기본형 의존 표기 + s_φ 단일화 미완**: 분해 𝒜_j/(n^eff F)=η_j+w_j ln[ξ/(1−ξ)] 는 V_drive 임의서 항등인데 "기본형 V_drive=V_n" 끼워 의존 인상 + keybox 부호 단일화 미해결. → 괄호를 "(분해는 V_drive 임의 항등; s_φ=+1 표기만 방전)"로, 진짜 의존(§tr 3단계)과 구분 + keybox 에 s_φ 지위 명시(C3 연동).
- **H8 [636·637 §bg] V_bg,eq 미정의 + /F 비대칭·명칭 충돌**: h_bg≡∂V_bg,eq/∂T 의 V_bg,eq 무정의(4전위에 없음); "background entropy coefficient" 명칭 vs V/K 단위 충돌(Ch2 잔재); bg 항만 차원검산 부재. → V_bg,eq 를 Q_bg(V_n,T) 평형 전위좌표로 정의 + 명칭 "background reversible-heat potential coefficient" + 637 차원검산 1줄(K·V/K·A=W; h_bg 가 per-charge 전위계수라 /F 내재).
- **H9 [663·666 §transport] transport 발열↔일반형 매핑 부재(double-count) + I²R_transp 미정의**: Q_transp 가 §general Σn^eff I_j η_j(계면 η_ohm/conc 흡수)와 별개인지 부분인지 미결 → ohmic 이중계상 위험; I/R_transp>0/≥0 미검산. → "Q_transp=전해질/고체상 transport 채널(계면 affinity 미흡수분, 비중복)" 1줄 + R_transp>0 가드 + I²R_transp≥0 부기.
- **H10 [738 §order] 계산순서가 dξ_eq,j/dt 미산출 → consistency option B 실행불가**: step4 는 dξ_j/dt 만, consistency 우변·가역열 B 는 dξ_eq,j/dt 필요. → step4 에 "dξ_eq,j/dt(chain rule, T·V_n 의존)도 계산" + P3-3=implicit(수치 solver, 논리공백 아님) 분류 명시.
- **H11 [764·772 §ident] k_{j,lim} orphan + R_ct 이중귀속 + calorimetry 부재 미식별 미명문**: k_{j,lim} 본 장 미정의(3회 사용); R_ct 가 pulse·EIS 양쪽 귀속(위계 소실); calorimetry 부재 시 미식별 클래스(절대 발열 스케일·가역/비가역 분리비·R_n,eff) 미진술. → k_{j,lim} 정의(Ch3 mobility floor)/제거 + EIS anchor→pulse 잔차 순서 + calorimetry 부재 미식별 3항 명문(FLAGGED).
- **H12 [921 §admin] thomasnewman2003 dangling bibitem**: 미인용(\cite 0). → AL-46/47(porous electrode thermal) 에 \cite 연결 또는 bibitem 삭제.

### MED
- M1 [181 §inherit] χ_j≡β_j 미정의·미사용 → 삭제(또는 출처 명시). M2 [186] q_rev,j 에 s^conv 병기. M3 [382 §tr] sign-lemma J^-→0 경계(0·∞→+∞≥0) 1줄. M4 [397 §tr] extensivation site 무상관(mean-field) 전제 명시. M5 [310 §decomp] ⊃→= (완전분할) 또는 잔차 0 명시. M6 [310 §order] step6↔9 대수 루프 explicit-lag/predictor-corrector 명시. M7 [552 §revOCV] dangling "식~의" 인용 채움. M8 [802 §admin] AL-44 tier 조건부(GROUNDED†) master 정렬. M9 [s_I·N_p·ρ_j 기호표 등재].

### 통과(빈통과 아님)
- DOI 귀속 clean(Onsager DOI 가 degrootmazur 책에 오귀속 0; schnakenberg=RevModPhys.48.571). AL-40~49 1:1·중복 0. 구 Ch6→Ch1 부록 B 잔존 0. η 단일화 keybox·micro=macro·≥0 본문 증명 실재(빈 자화자찬 아님). Ch2 §bg V/K vs J/mol·K 차원모순은 Ch4 가 해소(전위계수 V/K, 둘 다 W).

## 정정·빌드·커밋 (완료)
- 정정 적용: **CRITICAL 3(C1~C3) + HIGH 12(H1~H12) + MED 8(M1~M5·M7~M9)**. 기존 줄 BOUNDED/box/인자 추가·라벨/부호/단위/자기참조 교정 위주(식 재유도 0, 식별자 보존). M6·LOW 미적용.
- 검증(master 독립): xelatex 2-pass GREEN(`!` 0, undefined ref/cite 0, dup 0, 20p). 핵심 정정 실텍스트 확인 — C1 width BOUNDED(660–665 "width 온도계수 −(V_n−U_j)(∂w/∂T)/w² + D_q 정규화 OCV 고유, 부분적 동일정보")·C2 자기참조 제거(226 "Ch3 (L2) 정의와 동일 재기입")·C3 η 통일(466–467 η_j=V_drive−V_eq,j, s_φ는 𝒜_j scale)·H12 thomasnewman2003 cite 연결(730).
- tex **930→1004줄**(+74). 커밋·push(main+rb-rebuild).
