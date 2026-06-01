# RB_LEDGER_CH5_FINE_REVIEW — Ch5 절별(fine) 적대검수 + 정정 Result (2026-06-02 자율)

> §절마다 1 agent(14 병렬, 9렌즈). 파일 `Claude/docs/graphite_ica_ch5_rebuilt.tex`. Ch5=충방전 히스테리시스. ★keystone(충전 부호 s_φ^b 유도) 독립 재유도=수학 정확(Phase 5 CRITICAL 정정 건재); 결함=prose/표기/미정의 기호·부호 자유도.

## 적발 결함 (정정 대상 CRITICAL/HIGH/주요 MED)

### CRITICAL
- **C1 [616·620·624 §fullcell] exact↔apparent 부호 모순 + full-cell DVA 양극 좌표 분리 부재**: exact V_cell^b=V_p^b−V_n^b−η_loss^b vs apparent V_cell,app^b=V_p,app^b−V_n,app^b(손실항 제거). 정합하려면 η_loss^b=ΔV_p,pol−ΔV_n,pol 인데 \*양극 분극 ΔV_p,pol 미정의\*(eq:ch5_vapp_branch 는 음극만). full-cell DVA dV_cell/dQ_s 에서 Q_s=음극 좌표인데 양극은 반대방향(dQ_p=−dQ_s) 환산 누락. → η_loss^b≡ΔV_p,pol^b−ΔV_n,pol^b 명시 + 양극 분극 부호 정의 + DVA 에 dQ_p=−dQ_s chain-rule. (HIGH: 619 η_loss 전체 누락 over-removal → 잔여 transport/lag 손실 η_loss,res 분리.)

### HIGH
- **H1 [188 §inherit] s_I 미정의**: V_app=V_n+s_I|I|R_n 의 s_I(전류방향 부호) 정의·기호표 부재(1회). → s_I=sgn(I_s)(+1 방전/−1 충전) 기호표 등재. (s^{b,conv} dangling·χ_j≡β_j·s_{h,j} 미정의도 정리: 사용처 명시 또는 삭제.)
- **H2 [298 §inherit·§chargesign] 방전 부호 prose 자가모순**: "전위가 낮아질수록(…) V_n 이 평형서 위로 구동" 한 괄호서 정반대. 실제 유도는 V_n>U_j ⇒ ξ_eq>1/2 ⇒ s_φ^dis=+1. → "전위가 낮아질수록" 삭제, "V_n 이 평형서 위로(V_n>U_j) 구동될수록 진행 촉진"으로 단일화.
- **H3 [248–249 §signed] q_stt=q "정확히 환원" 무조건 단정 vs 부반응 미흡수 자기모순**: q_stt(전류 적분)와 (L1) q(보존식 해)는 부반응 시 갈림인데 "정확히 환원" 단정 + 같은 절 240–241 "LLI/LAM 임의 흡수 안 함" 선언과 모순. → "이상 쿨롱효율(η_C=1)·dQ_bg=0 극한에서 q_stt−q_stt,ref→q"로 조건부 약화 + 일반 경우 부반응만큼 어긋남 명시.
- **H4 [443·442 §branch] dangling 평문 ref + 동일 식 논증역할 충돌(순환)**: keybox 가 "식~eq:ch3_xiss"(평문, \eqref 아님) 인용 + branch-local db(442 전제)로 ξ_ss^b=ξ_tar^b 도출이 eq:ch5_branch_db(524 정의) 재대입 순환. → cross-chapter ref 규약 명시(평문 ↔ 본장 \eqref 비일관 해소) + keybox 대수를 "정의 일관성 확인(항등)"으로 격하 + 실질 keystone 붕괴는 (a)/(b)/(c V_drive≠V_n) 조건 + L4 두 조건 1:1 대응으로.
- **H5 [502·531·704·717 미정의 기호 다발]**: h_tar,j^b(502, §hstate 동역학 구동항 미정의→ h_tar^b=s_φ^b 못박기) · n_j^{eff,b}(531·548 §kinetics 미정의→ n_j^{eff,b}≡RT/(Fw_j^b) 정의) · k_j^rst(704·709 §rest ξ 완화율 미정의→ 기호표+Ch1 k_j 동일/별개 명시) · λ_{j,rst}(717 vs λ_j^b → λ_j^{b=rst} 통일). 전부 기호표 등재 또는 첫출현 정의.
- **H6 [540·686·690 §kinetics/§branchheat 부호 사슬·자유도]**: (a) §kinetics 540 η_prog^b>0 ⇒ 충전 dξ/dt<0 의 affinity↔rate 부호 사슬(dξ/dt=(r^++r^-)(ξ_tar^b−ξ_j)) 미명시 → 1~2줄 삽입. (b) §branchheat 686 eq:ch5_branch_rev 가 dξ/dt(물리 부호)와 s_{rev,ξ}^{b,conv}(규약 부호) \*둘 다\* branch 의존 → 부호 이중계상/미정의. → 부호 책임 일원화(s^{b,conv} branch 무의존 단일 규약, branch 반전은 dξ/dt 가 유일 담당) + 690 "dξ/dt<0 ≡ I_j<0 ≡ q_stt 감소" 동치 1줄.
- **H7 [572 §apparent] 분해식 loop-폭(차) vs signed single-branch 혼합**: ΔV_obs=loop 폭(branch 차)인데 우변 ΔV_pol 은 signed single-branch(I_s R_n^b). → 각 성분 ΔV_X≡X^dis−X^chg(branch 차)로 일원화, ΔV_pol=ΔV_pol^dis−ΔV_pol^chg≈2|I_s|R_n>0 명시. (R_n^b vs R_ct 충돌→R_{n,pol}^b≡R_n^b+R_ct^b 개명. |I_s|→0 외삽이 ΔV_kin 못 제거 한정. ΔV_aging 기호표 등재.)
- **H8 [608·596 §icadva] dangling "식~eq:fiteq" + ICA 좌표식 0개**: 절 제목 ICA/DVA 인데 DVA 두 식만, ICA(dQ/dV) branch 좌표 부재. → \eqref{eq:fiteq}(또는 명시 번호) + branch ICA 식 (dQ_b/dV_app^b)_b·signed dQ_s/dV_n boxed 병기 + 충전 ICA 부호반전(Q_s 감소) 유도.
- **H9 [636 §hysheat] ∮V dQ 부호·≥0 가드 부재**: E_loop=∮V dQ 차원(J)만, ≥0·적분방향·polarity 무. → "가역 cycle ∮V dQ=0, 비가역 >0; 적분방향 q_stt 1주기 고정, 부호 s^{b,conv} 정렬; 미정렬 시 E_loop=|∮V dQ|" + 가역 극한 →0 한계검산.
- **H10 [727·738 §ident] 식별 scope + 양방향 GITT 완화종점 미명시**: s_φ^b(AL-53 유도 상수)·loop area(관측량)는 식별 대상 아님 — scope 명시; branch target U_j^b 를 polarization·kinetic lag 와 \*독립\* 고정하는 양방향 GITT 완화종점(각 SOC 충/방전 I=0 OCV) 미지목. → scope 1줄 + "양방향 GITT 완화종점으로 U_j^dis−U_j^chg=ΔV_hys 직접추출(lag 배제); |I_s|→0 외삽 단독은 hys/kin 미분리" + {k_j^b,λ_j^b,h_j} 3중 축퇴 실험축 매핑.
- **H11 [752 §admin] Y1 dangling 추적 불가**: "Y1→AL-50/51/55" 재지정의 \AL{Y1} 원천이 파일·master 부재. → consolidated_ch5 원천 명시 인용 또는 master Correction 주석 박기.

### MED
- M1 [202 §inherit] ξ_tar^b="Ch3 ξ_ss^b" → "branch-local Ch3 형식(본 장 §branch 구성)". M2 [327·338 §chargesign] U_j vs U_j^b 표기 통일(부호 유도 단계는 U_j, center 분기는 §branch 이연). M3 [343] q_irr 출처 Ch2/Ch4/CHARTER 단일화. M4 [444 §branch] keystone (ii) V_drive=V_n 암묵 명시. M5 [494 §hstate] U_j^hys≡U_j^b 동일성 1줄. M6 [707 §rest] ξ-target↔h 후보 2짝 결합(교차조합 점근) 명시. M7 [719 §rest] state 연속 vs 구동(s_φ^b) 불연속 구분. M8 [642·645 §hysheat] 가역극한 0·J↔W 연결. M9 [677 §branchheat] 표 I_j↔식 dξ/dt 변수 병기. M10 [627 §fullcell] transport=η_loss 부분집합. M11 [admin] AL-52 ISBN·AL-55 mobility master 증분 반영.

### 통과(빈통과 아님)
- ★keystone 충전 부호 s_φ^b 독립 재유도=정확(음×음=양, V_eq^b=U^b+s_φ^b w^b ln[ξ/(1−ξ)], s_φ^chg=−1, q_irr≥0 유지). DOI 귀속 clean(dreyer2010=nmat2730·sethna1993=PhysRevLett.70.3347·onsager1931=PhysRev.37.405·schnakenberg=RevModPhys.48.571; Onsager↔degrootmazur 오귀속 0). AL-50~59 1:1·중복 0. 구 Ch6→Ch1 부록 B 잔존 0. 이중계상 금지 boundbox 물리 타당.

## 정정·빌드·커밋 (완료)
- 정정 적용: **CRITICAL 1(C1, exact↔apparent 부호 + DVA 양극 좌표 + 잔여손실) + HIGH 11(H1~H11) + MED 10(M1~M10)**. 기존 줄 BOUNDED/box/인자 추가·라벨/부호/미정의기호 교정 위주(★keystone s_φ^b 유도 불변, 식 재유도 0, 식별자 보존). M11(master 증분=별도파일)·LOW 미적용.
- 검증(master 독립): xelatex 2-pass GREEN(`!` 0, undefined ref/cite 0, dup 0, 21p, in-chapter \eqref 29/29). 핵심 정정 실텍스트 확인 — C1(678 eq:ch5_etaloss_def·680 양극 분극 ΔV_p,pol=I_s R_p^b·624 DVA dQ_p=−dQ_s)·H2(자가모순 prose 0)·H5(208 h_tar=s_φ^b·212/555 n^{eff,b}≡RT/Fw^b·211/783 k_j^rst 정의)·H8(653 eq:ch5_branch_ica).
- H8 eq:fiteq 는 cross-chapter(Ch1) 라벨이라 standalone undefined 방지 위해 평문 유지(결합 빌드서 해소; fixer 판단 타당).
- tex **899→999줄**(+100). 신규 라벨 eq:ch5_etaloss_def·eq:ch5_branch_ica. 커밋·push(main+rb, 분리 실행).
