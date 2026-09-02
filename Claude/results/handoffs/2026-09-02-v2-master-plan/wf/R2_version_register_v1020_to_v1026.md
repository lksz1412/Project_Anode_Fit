# R2 — 버전별 변경점 등록부 후반 (v1.0.20 → v1.0.26)

> 작성 = 판독·등록부 초안 에이전트 [hist_late](Fable 5.1), 2026-09-03. 성격 = **초안**(master 통합·commit 대상). 범위 = Claude 측 이력 중 v1.0.20 부터 v1.0.26 A/B 까지.
> 원천 = brief §3 가 배정한 18 문건 전문 + 사실 검증을 위해 추가로 읽은 v1.0.26 실물 6건(말미 Read Coverage). brief 요약과 원천이 어긋난 곳은 원천을 정본으로 적고 「Decision Queue」에 표면화했다.
> 경로는 특별한 표기가 없으면 `D:\Projects\Project_Anode_Fit\Claude\` 기준 상대경로이며, `L숫자` 는 그 파일의 행 번호다.

---

## 0. 읽기 규약

이 등록부는 세 가지 명칭 축을 섞지 않는다. 첫째, **작업 Phase 명**(P0~P8·Q0~Q10·R0~R9·FB0~FB7 등)은 각 버전 사이클의 작업 단위 이름이다. 둘째, **문건 구조 명칭**(Chapter 1 흑연·Chapter 2 LCO·Chapter 3 Si·혼합, Part 0·Part I·Part T)은 v1.0.22 재편 이후의 문건 골격이다. 셋째, **역사적 명칭**(`ver.1`~`ver.5`, 구 Ch1/Ch2 2챕터 체제)은 파일명·본문 이력에 남은 이름이다. 아래에서 "Ch2" 라고 쓰면 v1.0.22 이후의 LCO 장을, "구 Ch2" 라고 쓰면 v1.0.21 까지의 열특성 장을 뜻한다. 파일명과 소속이 반전된 곳(`ch2_sec*`= Ch1 Part T, `ch1_sec11~17`= Ch2)은 `docs\v1.0.22\results\HANDOVER_v1.0.22.md` L45 가 경고한 그대로다.

보고 등급은 네 단계로 나눈다. **확정** = 원천 문건에 그렇게 기록돼 있고 path+line 을 붙일 수 있는 것. **근거 미발견** = 배정 원천 안에서 그 사실을 뒷받침하는 기록을 찾지 못한 것. **추정** = 원천의 여러 기록을 이어 붙여 판단한 것(내 판단이며 원천 기록이 아니다). **미검증** = 원천에 주장은 있으나 실물로 확인하지 않은 것.

「사용자 결정 verbatim」 열의 큰따옴표는 **원천 문건이 큰따옴표로 기록한 발화**만 옮긴 것이다. 원천이 "요지" 라고 표시한 항목은 여기서도 요지로 표시하고 verbatim 으로 승격하지 않았다. 같은 발화가 두 문건에 서로 다른 표기로 남은 경우(v1.0.20 의 확장 분리 지시)는 두 표기를 병기하고 정본 선택은 master 에 넘긴다(DQ-6).

날짜는 원천 문건이 적은 날짜를 그대로 쓴다. 페이지 수는 각 인계 문서가 적은 빌드 결과(aux LastPage 또는 인계 문서 기재)이며, 빌드가 없는 버전은 그 사실을 적는다.

---

## 1. 총괄 등록부 표

| 버전 | 날짜 | 구조 | 물리·식 | 코드 | 게이트·빌드 | 사용자 결정 verbatim | 유실·park·미결 | 근거 path |
|---|---|---|---|---|---|---|---|---|
| **v1.0.20** 품질 정정판 | 지시 2026-07-15~17 · 확장 분리 결정 07-16 | 2챕터 체제 유지(Ch1 흑연+LCO+Part 0 / 구 Ch2 열특성) · 66p/25p/부록 8p · 자산 336/21 · Part 0 양자통계 배경(Ξ 대정준·q(T) 재배열) · 흑연 §3~§10 중간다리 · LCO §11~§17 수식사슬 대보강 | 물리 골격 무변경 · bgbox 수식화 +3식(`eq:sm-exch`·`eq:sm-fdbe`·`eq:lco-mottcrit`) · 첫 ERRATA E-001(ch2_sec00 과일반화) · B-006 U_j 평가 규약((−ΔH+TΔS)/F 환산값) · B-008 자립성 스윕 6곳 | `Anode_Fit_v1.0.20.py` = v1.0.19 구현 matched 이월(변경 함수 0·헤더만) | 3본 err0·undef0 · 구조 PASS(dup0·미해소0) · G1 bit-exact·G2 회귀(U_oc=74.4 mV·−0.204/−0.134/−0.070 mV/K·tab:qrev 5점·175점 2.9e-07 mV/K)·G3·n(T) PASS · 서지 원장 V1 키만 인용(42키 검증+12키) · P7 물리 오류 H 0 · CHANGE_LOG↔diff 1:1 | "확장 전건은 v1.0.21로 분리 — 원본(v1.0.20)을 살린다." · "v1.0.20 마무리 잘 짓고 v1.0.21로 이어가자." · "이번 건(v1.0.21 저작)은 Fable 마스터 세션 단독 작업" · "이 문서만 보고 이해되는 교과서" · bgbox "말로만" · D-1~D-5·D21-1~6 표 | 추가 후보 5건(TRIAGE_P7 §B·REVIEW_FINAL 최약점·keybox "셋"·appB 파일명·그림 후보군) 미집행 · V2 safran1987 보류 · 실측 데이터 부재 = 구조적(D-1) | `docs\v1.0.20\HANDOVER_v1.0.20.md` L4-L74 · `plans\2026-07-16-v1021-master-plan.md` L3·L25 |
| **v1.0.21** 확장판 | 계획 v2 확정 2026-07-17 · 마감 07-17 주간 | 2챕터 유지 · 기본판 76/26p + 항법판 78/26p(`\ifnavaid` 이원 빌드) · 신설 = 다클래스 대정준 소절 `sec:sm-mc` · TST bgbox · 그림 A급 5본 · 끝-대-끝 worked example(흑연 §10·LCO §15) · 로드맵 표 · 측정 원리 bgbox · Si 예비 지도 부록(tab:simap·GS-1) · 서지 54종 | 전하 보존식의 대정준 유도(Ξ=Π_j Ξ_{1,j}^{M_j} → ⟨N⟩=Σ M_jθ_j = `eq:implicit` 식별 · ∂⟨N⟩/∂μ=β var(N)>0 유일근) · 요동–응답 축(dQ/dV = 감수율) 합류 · TST `eq:tst-box`(k_BT/h 기원·ΔS_a=R ln(q‡/q_R)) · LCO 게이트 시연 +0.160→−0.128 mV/K 부호 반전 · GS-1 = 가정 충돌+유도 미착수 | matched 판정(게이트 exit 0) | 기본판·항법판 전건 err0 · 서지 54종 검증·미인용 0 · Q9 축약 스폿 검수만(전수 검수는 v1.0.22 R8 이월) | "항법 어쩌구 적용한 버전 안한버전 둘다 작업해줘"(D21-1) · "이번 건은 페이블 마스터 세션 즉 이 세션에서 단독 작업"(D21-6′) · "굳이 B급 교체 불필요"(D-6) · D-7 항법판 폐기 · D22 전건 | **항법 3종 중 식 의존성 지도·독자 경로 안내·로드맵 표 = 폐기**(D22-1, 기호표만 장별 기호표로 흡수) · B급 그림 6건 취소(기록 보존) · Q1 조사 §7~§8 미완 · DIRECTION_GENERAL 17건 중 14건 대기 · STATMECH 후보 (v) 단상 폭 Ω 재규격화 보류 · Ω(ξ)·Cahn–Hilliard 이월 | `docs\v1.0.21\HANDOVER_v1.0.21.md` L4-L24 · `plans\2026-07-16-v1021-master-plan.md` L5-L76 · `plans\2026-07-17-v1022-master-plan.md` L24 |
| **v1.0.22** 활물질별 3챕터 재편 | 계획 v2·GO 2026-07-17 · R9 초안 07-18 | ★**3챕터 체제 확립**: Ch1 흑연+열특성(Part 0 + Part I §0~10 + Part T = 구 Ch2 전량 + 부록 4본) / Ch2 LCO(구 Part II §11~17 승격, "추가 텀만") / Ch3 Si·혼합음극 신설(원소 Si/SiO_x/Si–C + 블렌드 f_Si 0~30 wt%) · 83/25/17p · 라벨 241/77/38 · bibitem 39/15/33 · 장별 기호표(계승 2단)·장별 참고문헌 · 항법판 제거 · xr 교차참조 · 독립 `appendix_phase_separation` | 인용 다리 수식화(집행 확정 = 흑연 7·LCO 4 · 계획 범위 ~12곳) · 통계역학 증축(CLT broadening·CNT 연결·블렌드 공통-μ 대정준 Σ_host Σ_j Q_j ξ_eq,j = Q x̄ · Larché–Cahn 시도) · SM2 3본(susceptibility·ensemble·two-responses) · FR 대공사 H 29 전건 집행(C-040~049)·M/L 정정형 38 집행 · f_Si wt% 전환(C-052) · "Chapter 2 도입"(C-055) · L5 charge-order ΔS tier-C 유지 | `Anode_Fit_v1.0.22.py` + `test_gates_v1022.py`: `BlendedAnodeDQDV`(+348줄) · Si 케이스 셋 · GS-1/GS-2 `NotImplementedError` · SiO_x placeholder+경고 | 3장 GREEN err0·미해소0·구조 PASS · 게이트 exit 0(G1~G3·n(T) + R6-G1 f_Si=0 bit-exact 9진입점 max\|d\|=0 · R6-G2 Lipschitz 0.502 · R6-G3 용량 보존 rel≤1.5e-9) · **RA 계보 감사 v19→v22: 미로그 축소·생략·왜곡 0** · 병합 빌드 금지(D22-8) | D22-1~8(항법판 폐기·v1.0.22·Si–C·서지 저비용+승급·인용 다리 ~12·통계역학 증축 GO[사후 제거 조항]·무응답→(a)·병합 시험 금지) · 운용 3+1/3+1/1/1 · 2026-07-18 f_Si wt%·"Chapter 2 도입"·moyassari 등재 | **P3-5 ref.6·7 확인 대기** · **FR 보류 풀 M 158 + L ~120**(각 A##_REVIEW.md 에 LaTeX 보존) · SiO_x 절대값 placeholder · Si dS_rxn 미부여(블렌드 발열 미구현) · GS-1 소성 히스·GS-2 유한율속 비가산 공백 · sethuraman 쪽 번호·L5 재소싱 · **병합 이관 5항(부록 카운터·xr 제거·파트 명칭·tier 범례·bib 중복) = 사용자 별도 세션, 착수 근거 미발견** · 다음 버전 후보 7건 | `docs\v1.0.22\results\HANDOVER_v1.0.22.md` L10-L143 · `plans\2026-07-17-v1022-master-plan.md` L3-L99 |
| **v1.0.23** JCP147 ratio 접목 + 고등수학 | 계획 2026-07-18 · P5 마감 | 3챕터 유지 · **부록 E 신설**(E.1~E.6 · bib 3종 · §8 말미 포인터 1줄) · 87/25/17p(VERSION_COMPARISON 기재) | JCP 147(14) 144111 의 Fredholm 2종 ratio 닫힘(Eq.32→33→34/37→39)을 **동역학 lag(II) 한 자리에만** 접목 · 전하보존 반전(I)·배경 자기일관(III)은 대수근이라 대상 아님(warnbox) · 1차 ratio 닫힘 재유도 · 타당성 부등식 ε=2χ_d(Ω/RT)Δξ_supp≪1(Δξ_supp≈L_V/(4w)) · 동결극한 정확 회수 · 전달함수 H(ω)=1/(1+iωL_V) · 실이득창 0.1≲L_V/w≲0.6 · "계산 절감 아님" 프레임 | ratio/transfer 옵션(`lag_ratio_correction=False` 기본 → bit-exact) · `test_gates_v1023.py`·`_selfconsistent.py` · v1.0.22 parity 순수 additive(47섹션 sha256 동일) | P0 GREEN baseline 83/25/17 · 적대적 5창 AUD-1~5 치명 0 · 중대 2건(부록 E 수치 증거 과장/오귀속) 정정 · 검수 7항 정합 | "본문의 수식을 푸는 기법"(→부록 E) · "제대로 적용은 코드" · "양 버전 빡세게 코드↔문건" · D3 P4 Fisher 미실행 · D1/D2/D4 = 기본값 집행(명시 확정 근거 미발견) | P4 Fisher 정보기하(D3 보류) · Legendre-Fenchel 명명노트(Tier3) · **Ref.6·7 원문 제목·DOI 근거 미발견**(서지: Ref.6 = S. Lee, C. Y. Son, J. Sung, S. Chong, JCP 134, 121102 (2011) · Ref.7 = C. Y. Son 외, JCP 138, 164123 (2013)) · 양 버전 샘플 이미지 QA "진행 예정"(후속 근거 미발견) · **v1.0.24 역문제 후보 → 실제 v1.0.24 는 반영·검증으로 방향 전환** · 기각군 7종 | `docs\v1.0.23\results\HANDOVER_v23.md` L3-L43 · `plans\2026-07-18-v1023-ratio-and-advanced-methods-plan.md` L11-L225 |
| **[계획 전용]** anodefit MASTER + v1.0.24 완성도 검증 계획 | 2026-07-18 (두 계획서 동일 일자) | 북극성 = 물리 forward 곡선 엔진 → 노이즈 실측 대체·M/X/Y fudge 대체·LAM/LLI/RI 상태 추론 · 캠페인 A~G · 로드맵 v1.0.24=A+D·v1.0.25=B+C·v1.1.0=E · 완성도 검증 계획 V0~V6(Steps 1–31, 매트릭스 GITT/0.05/0.1/0.2C × 15/23/35/45 °C) | M 통찰(M = dQ/dV 브로드닝 → dV/dQ 팽창) · 브로드닝 3출처(① L_V ∝\|I\| · ② n_jRT/F · ③ σ_η) · 폭 예산 `eq:widthbudget` · w_j = ②⊗③ 흡수 현상학적 폭 · 1C 휴면 L_V~1e-7 | (계획) 코드 T/I/V 구현범위 확인(V0) | (계획) M=1 고정 재현 RMSPE · ∝\|I\| 1:2:4 · L_V(T) Arrhenius | GO 접수 2026-07-18: D2 대상 = LCO·흑연·흑연+Si · 순서 흑연→LCO→블렌드 · "BDD는 참고 예시일 뿐"(3회) · "극도로 민감" · 회사 표준 조건 제공 | **캠페인 B 전셀·C T/I/V·E 상태추론 = 미착수(사용자 스코프 제외)** · **V2~V5(GITT×T 검증·휴면 판정·L_V Arrhenius·M-제거 증명·식별성) 집행 근거 미발견** — 추정: 2026-07-19 reflect 계획으로 대체(DQ-3) | `plans\2026-07-18-anodefit-MASTER-plan.md` L9-L128 · `plans\2026-07-18-v1024-completeness-validation-plan.md` L6-L198 |
| **v1.0.24** 최근문헌+Codex 반영(@3/@5) + 사후 강화 | 계획서 2026-07-19(추정·미정독) · R4 마감 커밋 709d9e9 · 사후 강화 ~07-22 | 3챕터 유지 · 신규 소절 3(§1.5.4 stage-2L `ch1_sec05b_gr2L` · §3.2.5 Si Frumkin `ch3v22_sec02b_sifr` · §2.6.1 LCO 전자항 토글 `ch1_sec16b_lcoomega`) · 91/28/20p · R1 9창 경쟁→W9 base · CODE_GUIDE_v24(.md/.html) | @5 stage-2L 엔트로피 온도분리 Δ(ΔS)≈29 J/mol/K → 0.30 mV/℃(재현 0.271) · 병합 ~10 ℃ · 판정자 dμ/dθ\|½=4RT−2Ω · 분류는 §7 위임 · @3 Si Frumkin 폭 판정 w/(RT/F)=[1.45,2.74,1.09] → 단일상 고용체 · 커널 dQ/dV=QF/\|RT/[θ(1−θ)]−2Ω\|(Ω<2RT) · sifr Ω>2RT = Maxwell 공존(코드에 맞춰 정정) · LCO 전자항 기본 False(상온 커브 불변·∂U/∂T 만 가름) · #7 Ω_j^cat = 유효 평균장 축약 · #1 func_L_q 단위계약(dH_a^phys = dH_a + RT ln3600 ≈ +20.3 kJ/mol) · 6-gallery MSMR opt-in(gallery ≠ 물리상) | additive bit-exact 4건(@3 `'kernel':'regsol'`·@5 `GRAPHITE_STAGING_XRD_v1024`·`include_electronic_entropy`·단위 주석) · `GRAPHITE_STAGING_MSMR6_LIT` opt-in · `_regsol_dqdv` 용량 +0.063% 버그 수정(wi=Q/xg.size) · sha256 f230f59b | 0-error 91/28/20 · undefined 0 · STRUCTURE PASS · G1 0·reflect 4/4·selfconsistent 5/5·R6 3/3 · R3 적대검수 3차원 CLEAN · **R0 도구 JSON 덮어쓰기 사고 → ch1 마스터 재구성** · SINTEF Zenodo 20086298 실측 피팅(흑연 @5 0.9525→0.9731 · Si @3 0.9944 · 블렌드 0.9848) · 전수 doc↔code 감사(6 병렬) BUG 0 | 사용자 선택 @3·@5 · 사용자 안 A(챕터 유지+토글) · "커브 구할 땐 빼고" | stage-2L 정량 다온도 미검증(tier B) · Ω_Si·Ω_j^cat 점값 미식별 · O3-LCO 전자항 T의존 미검증 · tab:staging ΔS(+15/−14) 초기값 → 피팅 갱신 대상 · 유한율속 `dqdv()` regsol 확장(→v1.0.25 삭제로 소멸) · **Task #38** · IMPROVEMENT #2 비대칭 폭(→v1.0.25 @2) · **#4 정칙용액 자유에너지 = R²≈0.96 천장의 진짜 해법(Ch2–3 열역학 과제, park)** | `docs\v1.0.25.1\results\HANDOVER_v24.md` L3-L73 · `results\comp_v24\USER_FEEDBACK_v1024_READING.md` L189-L191 |
| **v1.0.24.1** 1차 정독 피드백 리비전 FB0~FB7 | 2026-07-22 | 문건 한정 리비전(코드 무변경) · 97/30/21p · 폴더 `docs\v1.0.24.1\`(동결 사본+리비전 식별) · 제목 N-태그 제거 ~33 · §1.1.4 배경 박스 ~50% 압축 · LCO 서두 차이-선도 재균형 · 조판 여백 25 mm·줄간 1.16·문단 0.55 em·microtype · E.3 itemize 전환 · overflow 3건 추가 수정 | 물리·식번호·label 정의 불변 · 노테이션 확률 P→소문자 p(압력 P 유지) · f_int/s_int 소문자 유지+자리당 가드 · 요동/양성→영문(body 0) · 음함수/섭동/준위→국문+첫 병기 · 유일근→"유일한 근" | 무변경(sha256 f230f59b 불변) | 0-err·undefined 0 · 본문 코드토큰 grep 0 · FB7 적대검수 3창 → `PHASE_FB7_RESULT` · **CLAUDE.md P3-8 명문화** · 재검 감사: 품질 하락 0·의도된 voice 평탄화 | "1차 피드백 끝. 수정하여 1.0.24 리비전하라. 작업 계획서부터." · "챕터1 문건 피드백 끝." · "누가 1.0.24만 읽으래" · "이전 이력 전부 보라" · "v19=구문 최고·v23=논리 최고. 이 둘과 v24를 어투·구문·내용·논리로 재검. 과거 이력 대조해 의도된 변경인지 퀄리티 하락인지 판정." · F-04·F-10·F-11 지적(요지) · D1~D6 기본값 GO | **voice 복원 옵션 3(§1.1.4 교차지도 문장·appE/sec01_map 투명 voice·fluctuation 혼합 register) = 사용자 판단 미집행** · U_j 표시 반올림 210.87→210.88(F-추적 밖·무해) · 지배 문서 4종(CLOSING·rubric·TERMS_POLICY·TONE_AUDIT) 승계 | `docs\v1.0.25.1\results\HANDOVER_v24.md` L77-L89 · `plans\2026-07-22-v1024-feedback-revision-plan.md` L10-L226 · `results\comp_v24\USER_FEEDBACK_v1024_READING.md` L12-L206 · `results\comp_v24\VERSION_COMPARISON_v19_v23_v24.md` L3-L79 |
| **v1.0.25** 국소 수정판 | 2026-07-26 | 3챕터 유지 · `_sections` 14파일 +257줄 · 신규 라벨 3(`eq:skewpeak`·`eq:skewapex`·`eq:gr2l-fwhm`) · 삭제 라벨 0 · `\boxed` 38→39 · 문장 삭제 1건(sifr 코드 폴백 서술) · 마스터 3 tex 표시 버전만 1.0.25(DG-2) · ARCHIVE_NOTE S1~S6 추기 · 코드 파일명 `Anode_Fit_v1.0.24.py` 유지 | @2 skew-logistic dQ/dV=Q(α/w)ξ_eq^α(1−ξ_eq) · α = 현상학 형상 파라미터(tier C) · 반높이 폭 4.45/3.53/3.02/2.74 w(α=0.5/1/2/4) · 정점 이동 σ_d w_j ln α_j(α=2 → +17.8 mV) · 4-손잡이 식별 가드(α·L_V·gallery·w_j) · 인과 pad(`eq:lag` 하한 −∞ 실현, 74.31%→2.17e-04) · 상수 SI opt-in(25.693 vs 25.6912 mV) · **regsol dQ/dV 커널 삭제**(실측 역전 +0.97→−0.53 %p; Ω 물리 전량 존치; `eq:sifr-kernel`·`eq:sifr-blend` 보존·"해석적 기록") · w_eff 정정(중심 높이 Q/(4w_eff) 정확·폭 오독 6.6/21/30배·FWHM 점근 (16/3)(RT/F)λ^{3/2}·Ω=2RT Maxwell 불연속) · gallery ≠ 상(ΔU<12 mV 근축퇴·XRD 상 수 불변) · C_bg = 창-국소 상수 근사 · 데이터 정직화(gr=p-ocv/si=p-ocvhold · 0.9770→0.9945) | 추가 `func_dxi_eq`·`_alpha_factor`·`alpha` 키·`_causal_pad`·`R_SI/F_SI/use_si_constants()`·`SI_MSMR7_LIT` · 삭제 `_REGSOL_XG`·`_regsol_binodal_xa`·`_regsol_dqdv`+`'kernel'` 분기 · 1734→1917줄(+183; regsol 단계 1957→1917) · `test_gates_v1025.py` 신설 · G-R3 "삭제 확인" 재작성 | 게이트 GREEN·골든 bit-exact 0.0 · STRUCTURE PASS·STRICT ALL PASS·doc↔code 30/30(02:06 이전 실행분) · ★**LaTeX 빌드 미수행**(TeX 부재, N1) · @1~@5 실측표(@2 0.98078 최대 이득·@4 0.93215 유해) · 계획 이탈 3건(C3 opt-in·C6 완전 삭제·라벨 1→3) | "regsol 삭제"(DG-1) · "파일명을 왜 바꿔? 버전명만 바꿔주면 되는거 아니냐?"(DG-2) · "물리·화학 논리를 건드리는 문건 작업은 Opus 5.0, 나머지는 Opus 4.8"(요지 인용) · D-A~D-D · 지시 1~11(요지; 지시 6 세 물리 질문 원문 미전달) | N1~N13(§4 참조) · CODE_GUIDE_v24·FITTING_GUIDE 미갱신 · MERGE_READINESS_v25 X1~X14(미정독) | `docs\v1.0.25.1\results\HANDOVER_v25.md` L13-L170 · `docs\v1.0.25.1\results\INDEX_v25.md` L13-L138 · `plans\2026-07-26-v1025-surgical-skew-consistency-plan.md` L10-L240 |
| **v1.0.25.1** 검증+touch-up (현행 최신 문건) | 2026-07-26 | 별도 폴더 `docs\v1.0.25.1\` · v1.0.25 무수정 보존 · touch-up 4건 = `_sections` 3파일(ch3v22_sec02b_sifr F1·F3 / ch1_sec05_width M-w / ch1_sec06_eqpeak L-bg) · 표시 버전 v1.0.25.1 · **102/30/22p** | 식·라벨·boxed(39) 불변 · F1 regsol 삭제 근거 정직화("더 적은 가정으로"→"별도 커널 계열 도입 없이 기존 로지스틱 자유도만으로" + n=1·AIC/BIC 미확정 유보) · L-bg 감수율 항등 유도 = α=1 한정 명시 · 마스터 손검산: 정점이동·높이 (Q/w)[α/(α+1)]^{α+1}·FWHM (16/3)(RT/F)λ^{3/2} 독립 유도 | byte-identical(release 1.0.25 유지) · 코드 델타 289줄 전문 정독 | 4종 스위트 직접 재실행(v1024·reflect 4/4·selfconsistent 5/5·**v1025 9/9(G-금지 포함)**) · 골든 0.0 · STRUCTURE PASS·STRICT ALL PASS · **XeLaTeX(MiKTeX 25.12) 3-pass+xr 빌드 오류 0·undefined 0·PDF 3종 커밋** · origin/main push | 사용자 지시로 Claude 작업만 현행화(요지) · 판정 = 반영(마스터 판단) | N4·N6~N9 이월 · F2 supersede 데이터 리포 미보존 | `docs\v1.0.25.1\results\V1025_1_TOUCHUP_NOTE.md` L3-L61 |
| **v1.0.26 A/B** regsol 재검증(두 판 산출) | 2026-07-27 · 커밋 4069cb3 | 문건 tex 무변경 · 작업 폴더 `results\comp_v26_data\` · 결과 문서 `docs\v1.0.26A-regsol\README.md`·`docs\v1.0.26B-gallery\README.md` · 기준 코드 v1.0.25.1 | A regsol-4(흑연 R²=0.91506·BIC 2609.6·면적 결손 +12.05 %) vs B logistic-7(R²=0.97389·BIC 1765.1) → ΔBIC +844.5 · 흑연 Ω/RT = 2.54/2.03/1.88/2.30 ≈ 2RT(Cordoba 2024 Ω_a≈2.5RT 앵커 정합) · 판정 "흑연이 두-상이다 = 참 / regsol 커널이 gallery 를 대체한다 = 거짓" · 스윕: skew-logistic-7 BIC 991.5(최선)·skew-regsol-6 BIC 1264.9 · regsol_kernel = 혼화갭 닫힌형 + 밀도⊛FFT 합성곱 · dQ/dV = BDD `99_Backend` 방식 이식(dMSMCD+웨이블릿+savgol) | 조사 스크립트만(`regsol_kernel.py`·`test_skew_regsol_v2.py`·`test_gallery_vs_regsol.py`·`build_two_versions.py`·`make_version_docs.py`) · 문건·본 코드 무변경 · 초기 `test_skew_regsol.py`·`out_skew/` = 결함 3건으로 폐기 | 빌드 없음 · 착수 시점 서비스 장애로 실행 차단(HANDOVER) → 이후 실행 완료(README·build.log) · 평형 데이터(GITT/hold) 재검 미실행 · bootstrap 미수행 | "24regsol 식에 25에 추가하기로한 내용들 추가해서 테스트 해보고 그 결과를 나한테 제시해. 그 결과를 이미지로 확인하고 나서 정할려니까." · "두상으로 분리되는 걸 표현하려면 regsol이 들어가야 한다." · "지금 저게 잘맞는다고 보이냐? 개판인데?" · "미분이 매끄러워지라고 쓰라는 거지 안 맞는 게 맞게 되지는 않는다. 제대로 데이터 다시 찾아와." · "regsol에 비대칭 반영했던 그 시리즈를 반영해서 테스트하랬지? 그런데 그걸 했냐?" · "그래프 그려서 이미지를 달랬지? 왜 수치만 적냐" | **★평형 데이터 재검(GITT/p-OCV+hold) 미실행** · 흑연 0.104 V 피크 FWHM ≲1 mV(RT/F 의 1/25) 두-상 vs 비평형 인공물 미판정 · regsol 소재별 되살리기 = 사용자 결정 대기 · N6 데이터 provenance · N4 | `results\comp_v26_data\HANDOVER_regsol_investigation.md` L3-L55 · `results\comp_v26_data\README.md` L1-L50 · `docs\v1.0.26A-regsol\README.md` L1-L199 · `docs\v1.0.26B-gallery\README.md` L1-L193 · `results\comp_v26_data\out_versions\build.log` L1-L36 |

---

## 2. 버전별 상세

### 2.1 v1.0.20 — 품질 정정판 (v1.0.19 대비 물리 골격 무변경)

**날짜.** 사용자 지시 chain 은 2026-07-15~17 이고(`docs\v1.0.20\HANDOVER_v1.0.20.md` L5), 확장 분리 결정은 2026-07-16 이다(`plans\2026-07-16-v1021-master-plan.md` L3). 마감 커밋 chain 은 730fc40(P5)→…→ba41c90(최종 빌드)→HANDOVER 커밋이다(HANDOVER L7).

**구조.** v1.0.19 의 2챕터 체제를 그대로 두고 P0~P8 을 돌렸다. Ch1 Part 0 에 양자통계 배경(Ξ 대정준·q(T) 재배열), 흑연 §3~§10 에 중간다리, LCO §11~§17 에 수식사슬 대보강, 구 Ch2 에 FD/BE 정통 유도 선행이 들어갔다(L24). 최종 빌드는 Ch1 66p·Ch2 25p·appendix 8p 이고 구조 검사 자산은 336/21 이다(L26). 이 버전은 **동결**됐고 이후 결함은 v1.0.21 ERRATA 체계(E-002~)로만 다룬다(L69).

**물리·식.** 사용자 지적 두 건이 즉시 집행됐다 — bgbox "말로만" 지적 → B-009 수식화로 `eq:sm-exch`·`eq:sm-fdbe`·`eq:lco-mottcrit` 3식 추가, 과거 버전 이력 의존 금지 → B-008 자립성 스윕 6곳(L15·L25). 첫 ERRATA E-001(ch2_sec00 과일반화 정정, 코드 무영향)과 B-006 U_j 평가 규약((−ΔH+TΔS)/F 환산값 필수·표시 반올림 85 mV 입력 금지)도 여기서 생겼다(L25·L29). P7 통합 검수는 문서 전체 물리 오류 H 0 으로 닫혔다(L25).

**코드.** `Anode_Fit_v1.0.20.py` 는 v1.0.19 구현이 v1.0.20 문건 요구를 이미 충족한다는 appB 대조에 따라 **matched 이월**(변경 함수 0·헤더만 갱신)이다(L29). 게이트 G1(v1.0.19 bit-exact)·G2(회귀 전건: U_oc=74.4 mV·−0.204/−0.134/−0.070 mV/K·tab:qrev 5점·175점 2.9e-07 mV/K)·G3(θ_E 미지정 bit-exact)·n(T) 가 전건 PASS 다(L29). 이 회귀 기준 수치는 v1.0.25 의 SI 상수 논의(74.4→74.3 표시 절벽)까지 그대로 이어진다.

**게이트·빌드.** 3본 err0·undef0, 구조 PASS(dup0·미해소0), snapshot diff p7b→final ±0, 서지 3자 정합 cite=bib 36/16 불일치 0, CHANGE_LOG(C-019·B-009·E-001)↔diff 1:1(L47). 서지 원장 `V1020_REFERENCE_LEDGER.md` 가 **V1 키만 인용 가능** 규칙을 세웠다(L23·L70).

**사용자 결정 verbatim.** "확장 전건은 v1.0.21로 분리 — 원본(v1.0.20)을 살린다."(L17) · "v1.0.20 마무리 잘 짓고 v1.0.21로 이어가자."(L18) · "이번 건(v1.0.21 저작)은 Fable 마스터 세션 단독 작업"(L19) · "할 수 있는 데까지 해놔줘"(L19) · "이 문서만 보고 이해되는 교과서"(L15) · "체리픽은 신규-대-기존 비교 포함"(L14) · "통계역학이 초반만 반짝하고 끝나 아쉽다 — 뒤 내용도 통계역학적으로 유도 가능한 부분?"(L13). 같은 확장 분리 지시가 v1.0.21 계획서에는 "확장 관련 내용은 21 버전으로 — 원본(v1.0.20) 보존", "20버전 마무리 잘 지어주고 21에서 이어가자" 로 기록돼 있다(`plans\2026-07-16-v1021-master-plan.md` L3) — 두 표기 중 어느 쪽이 원 발화인지 배정 원천만으로는 가릴 수 없다(DQ-6). 결정 표 D-1(실측 데이터 부재는 구조적·피팅은 회사 수행)·D-2(bgbox 본문 유지+수식화)·D-3(자립 교과서)·D-4(확장 분리)·D-5(그림 체리픽 비교 포함)와 D21-1~6 은 L32-L44 에 "사용자 확정·재론 불요" 로 고정돼 있다.

**유실·park·미결.** 추가 후보 5건(`TRIAGE_P7.md` §B 기각·보류분, `REVIEW_FINAL_FABLE.md` 최약점, ch1_sec07 keybox "셋" 축약, ch2 appB 파일명 v1.0.19 표기, 그림 후보 FF2-6·fig:lco-electronic·fig:sm-reservoir·LCO 3-peak·FO3-[5]/[6]·N-11 peak 해부도)는 "실제 수정하지 않음 — 보고만" 상태다(L52-L57). V2 = safran1987 보류(L70). 미검증 항목으로 appendix 스냅샷이 final 이 최초라는 점(L50)이 남았다.

### 2.2 v1.0.21 — 확장판 (통계역학 관통·독자 인프라·LCO 심화·Si 접목)

**날짜.** 계획 v2 확정 2026-07-17(`plans\2026-07-16-v1021-master-plan.md` L3). Q0~Q8 마감 후 Q9/Q10 은 v1.0.22 R0 에 흡수됐다(`docs\v1.0.21\HANDOVER_v1.0.21.md` L1).

**구조.** 2챕터 체제 유지. 기본판 76/26p, 항법판 78/26p(단일 소스 + `\ifnavaid` 토글 이원 빌드)(L8·계획 L67). 신설 = 다클래스 대정준 전하 보존 소절 `sec:sm-mc`(Part 0 §2.5 sec:sm-mf 와 §2.6 sec:sm-macro 사이, 초안 6본 체리픽) · TST 배경 bgbox `eq:tst-box` · 그림 A급 5본(fig:UjT p.22 · fig:hysgap p.25 · fig:sumcurve p.44 · fig:qrevsoc Ch2 p.22 · fig:svibid Ch2 p.13) · 일반 확장 top3(끝-대-끝 worked example·Ch1↔Ch2 로드맵 표·측정 원리 bgbox) · LCO 게이트 한 점 시연 · Si 예비 지도 부록(tab:simap·GS-1·서지 14건) · 서지 54종(L8; 계획 L53-L54).

**물리·식.** 전하 보존식이 **대정준 기원으로 1급 승격**됐다: Ξ=Π_j Ξ_{1,j}^{M_j} → ⟨N⟩=Σ_j M_jθ_j 반전 = `eq:implicit` 식별, ∂⟨N⟩/∂μ = β·var(N) > 0 로 유일근 증명(계획 L8; HANDOVER L11 ③). 요동–응답 축(∂⟨N⟩/∂μ = β var(N) → dQ/dV = 감수율)이 D21-5 로 이 절에 합류했다(`HANDOVER_v1.0.20.md` L43). TST 는 k_BT/h 의 미시 기원과 ΔS_a = R ln(q‡/q_R) 부호 읽기를 Part 0 의 q(T) 언어로 연결한다(계획 L8·L54). LCO 게이트 시연은 코드 재현으로 +0.160→−0.128 mV/K 부호 반전을 보였다(L8). Q9 스폿 검수는 4분류 진단에서 sm-mc = "정의상 implicit", GS-1 = "가정 충돌+유도 미착수" 로 분리했다(L11 ④).

**코드.** matched 판정, 게이트 exit 0(L8).

**게이트·빌드.** 기본판·항법판 전건 err0(L8). 서지 54종 전건 검증·미인용 0. 심층 검수(물리 적대 검산·register 전수)는 재편 후 v1.0.22 R8 이 전 문서 대상으로 하는 것이 중복 없는 경로라고 판정해 이월했다(L11).

**사용자 결정 verbatim.** D21-1 "항법 어쩌구 적용한 버전 안한버전 둘다 작업해줘"(계획 L67) · D21-6′ "이번 건은 페이블 마스터 세션 즉 이 세션에서 단독 작업"(계획 L72) · D-6 "굳이 B급 교체 불필요"(HANDOVER L16) · D-7 항법판 폐기 확정(L17) · D22 전건(L18). D21-2~5 는 추천안 위임 채택이다(계획 L68-L71).

**유실·park·미결.** ★항법 3종(①식 의존성 지도 ②통합 기호 대응표 ③독자 경로 안내)은 이 버전에서 만들어졌다가 D-7/D22-1 로 폐기됐고, 기호 대응표 기능만 장별 기호표로 흡수됐다(`plans\2026-07-17-v1022-master-plan.md` L24). 이는 사용자 결정에 의한 폐기이지 무기록 유실은 아니다 — 다만 v2.0.0 이 "일반→특수" 재구조를 택할 경우 식 의존성 지도의 기능은 다시 필요해질 수 있어 재개방 후보로 적어 둔다(내 판단). B급 그림 6건 취소(기록은 FIGS_PICK 보존), Q1 조사 §7~§8 미완(계획 L76), DIRECTION_GENERAL 17건 중 14건 추가 후보 대기(계획 L68), STATMECH 후보 (v) 단상 폭 Ω 재규격화 보류·축 B/C 범위 밖(v1.0.22 계획 L93), Ω(ξ)·Cahn–Hilliard 급 미시 모델 확장 X(계획 L47).

### 2.3 v1.0.22 — 활물질별 3챕터 재편 + 동기화 코드

**날짜.** 계획 v2 확정·GO 2026-07-17(`plans\2026-07-17-v1022-master-plan.md` L1). R9 인계 초안 2026-07-18(`docs\v1.0.22\results\HANDOVER_v1.0.22.md` L3).

**구조.** ★이 버전이 현행 문건 골격의 출발점이다. Ch1 흑연+열특성 = Part 0(통계역학 공통 뿌리, 전 장 상주) + Part I(흑연 §0~10) + Part T(구 Ch2 열특성 전량 흡수) + 부록 4본 / Ch2 LCO = 구 Part II(§11~17) 승격, "Ch1 식 기반 추가 텀만" 방식 / Ch3 Si·혼합음극 신설 = 케이스별(원소 Si / SiO_x / Si–C) + 블렌드 f_Si 0~30 wt%(L14-L16). 최종 83/25/17p, 소스 라벨 241/77/38, bibitem 39/15/33(L55-L57). 장별 기호표(계승 2단)·장별 참고문헌(리뷰 모음형)·항법판 제거·preamble 통합·xr 교차참조가 R1 에서 집행됐다(L28). 독립 `appendix_phase_separation.pdf` 가 별도 컴파일된다(L60). 병합 빌드는 D22-8 로 금지되고 `MERGE_READINESS` 문서까지만 냈다(L12).

**물리·식.** 관통 축 두 개가 들어갔다. (a) 인용 다리 수식화 — load-bearing 인용마다 "우리 식 ↔ 논문 식" 변수 대응·중간 수식 1~3개·방법 요지·가정 차 1문장(계획 L71). 흑연분 7·LCO분 4(L31-L32). 대상 목록 = dreyer2010/2011·mckinnon1983·bazant2013·marianetti2004·vanderven1998·msmr_origin2017/bakerverbrugge2018·weppner_huggins1977·sethuraman·larchecahn1973·verbrugge_lisi2016·baek_pilon2022(계획 L71). (b) 통계역학 증축 — CLT broadening·CNT 연결(L31), 블렌드 공통-μ 대정준 Σ_host Σ_j Q_j ξ_eq,j(U_oc,T) = Q x̄, Q=Q_gr+Q_Si, f_Si=Q_Si/Q(계획 L72, Ch3 의 통계역학 앵커이자 코드 합성 규칙), Larché–Cahn 시도(GS-1 접속 범위까지만, L120). SM2 3본(susceptibility·ensemble·two-responses)이 `comp_SM2/` 에 있다(L36·L80) — brief §4.5 가 "집행 여부 미확정" 으로 둔 항목의 원천이다. FR 심층 검토 대공사(23창·H 29·M 208·L ~120)는 H 전건 재검산·집행(C-040~049), M/L 정정형 38 집행(C-051)으로 처리됐다(L37-L39). 사용자 결정으로 f_Si 가 wt% 기준으로 재선언(C-052)되고 "Part II 도입" 절 제목이 "Chapter 2 도입"(C-055, 라벨 `sec:lco-intro` 불변)으로 정합화됐다(L95-L96).

**코드.** `Anode_Fit_v1.0.22.py`(92 KB) + `test_gates_v1022.py`(33 KB). `BlendedAnodeDQDV`(+348줄)·게이트(+201줄), 순수 추가·삭제 0(L64). GS-1 소성 히스·GS-2 유한율속 비가산 = `NotImplementedError`, SiO_x 절대 전위·히스 = placeholder+경고(L66).

**게이트·빌드.** 3장 전건 GREEN(err0·미해소0·구조 PASS·dup 0·cite↔bibitem 정합)(L59). 게이트 R9 재실행 exit 0 — 기존 G1~G3·n(T) + R6-G1(f_Si=0 bit-exact 9진입점 max|d|=0.0)·R6-G2(스윕 Lipschitz 0.502)·R6-G3(용량 보존 rel≤1.5e-9)·coverage(L65). ★RA 계보 무결 감사(v1.0.19→v1.0.22, 사용자 지시)는 **미로그 축소·생략·왜곡 = 0** 으로 닫혔다(L29) — brief §4.4 의 "자산 무유실 원칙(계보 감사 ③=0건 기준)" 의 근거가 이것이다.

**사용자 결정.** D22-1~8 은 계획서 헤더에 확정 기록으로 있다(L3): 항법판 폐기 / 버전 v1.0.22 / Si–C 복합 확정 / 서지 저비용 모델 + 부족 시 한 단계 승급 규칙 / 인용 다리 핵심 ~12곳 / 통계역학 증축 전건 GO(사후 제거 조항 — "이해를 돕지 못하고 혼란 가중 판단 시 사용자 지시로 제거") / 무응답→권고 (a) / 병합 시험 금지(사용자 별도 세션). 운용 구성 3+1/3+1/1/1 도 사용자 확정(계획 L25). 지시 원문 요지 ①~⑩(계획 L4)은 요지이지 verbatim 이 아니다. 2026-07-18 결정 3건(f_Si wt%·"Chapter 2 도입"·moyassari_blend2022 등재)은 L95-L97.

**유실·park·미결.** **P3-5 ref.6·7 방법론 확인 대기**(L93, CLAUDE.md P1)는 v1.0.23 으로 넘어갔다. 그 접목 계획(삽입 지점 5곳·선행 절차 5단계)이 L99-L115 에 있고, v1.0.23 은 그중 #1 본체를 부록 E 로 옮겨 실현했다(원안은 `ch1_sec02b_part0` §2.5 직후 소절 신설). **FR 보류 풀 M 158 + L ~120** 은 "각 A##_REVIEW.md 에 완성 LaTeX 보존·후속 phase 권고" 상태로 park 됐다(L94·L138). 정직 공백: SiO_x 절대값 placeholder·Si 열역학 dS_rxn 미부여(블렌드 발열 미구현)·GS-1/GS-2 공백·sethuraman_stresspot2010 쪽 번호·L5 charge-order ΔS 0.47/1.49 재소싱(L119-L122). **병합 이관 5항**(부록 카운터 `\ref`화·xr 제거→단일 카운터·파트 명칭 선형화·tier 범례 전역 이동·swiderska2019 중복 제거)은 사용자 별도 세션으로 이관됐고, 이후 버전 어느 인계 문서에도 착수 기록이 없다(근거 미발견)(L124-L129). 다음 버전 후보 7건(L137-L143) 중 "P3-5 반영 후 Chapter 1 self-consistent loop 재구성" 은 v1.0.23 부록 E 로 부분 실현됐고, 블렌드 발열·구간별 host 전환·반응전류 배분(ai_composite2022, GS-2 동역학 층)·SiO_x 절대값·moyassari G2 강화는 후속 근거 미발견이다.

### 2.4 v1.0.23 — 사용자 JCP147 Fredholm ratio 방법 접목 + 고등수학 Tier1

**날짜.** 계획서 2026-07-18(`plans\2026-07-18-v1023-ratio-and-advanced-methods-plan.md` L3). P0~P5 마감(`docs\v1.0.23\results\HANDOVER_v23.md` L3). 인계 문서에 마감 일자는 없다.

**구조.** 3챕터 유지. **부록 E 신설**("자기일관 해법 — ratio 닫힘과 전달함수"; 계획 골격 E.1~E.4, 집행 결과 E.1~E.6)·bib 3종·본문 포인터 §8 말미 1줄(HANDOVER L11; 계획 L80-L86). 페이지는 인계 문서에 없고 `results\comp_v24\VERSION_COMPARISON_v19_v23_v24.md` L22 가 87+25+17 로 적었다.

**물리·식.** 사용자 논문 JCP 147(14) 144111 (2017) 의 간판 기법 = 제2종 Fredholm Eq.(32) `1 − W̄(r) = ∫K(r,r₁)W̄(r₁)dr₁` → (33) 양변 나눠 미지량을 비 W̄(r₁)/W̄(r) 로만 남김 → (34/37) 그 비를 가해 기준문제의 비로 치환 → (39) 닫힌형(계획 L26, 원문 Eq. 번호 근거). 문건의 자기일관 구조 3종 중 **동역학 lag(II, Volterra 인과 합성곱)만이 접목 대상**이고 전하보존 반전(I)·배경 자기일관(III)은 적분핵 없는 대수근이라 대상이 아님을 부록 E 서두 warnbox 로 명시했다(HANDOVER L19; 계획 L30-L35). P1 조건검수가 1차 ratio 닫힘 재유도·타당성 부등식 ε ≡ 2χ_d(Ω/RT)Δξ_supp ≪ 1(Δξ_supp ≈ L_V/(4w))·동결극한 정확 회수를 통과했다(HANDOVER L10·L20; 계획 L103-L104). 전달함수 H(ω)=1/(1+iωL_V), dQ/dV_app = H·dQ/dV_eq(계획 L166). 정직 프레임: lag 은 이미 O(N) 전진 ODE(Markov)라 "계산 절감" 이 아니라 (a) 동결 0차 위 분석적 1차 닫힌형 (b) 타당성 증명서 (c) 사용자 방법 시연이 가치이며, 실이득창은 중간 전류 0.1≲L_V/w≲0.6(2–10× 오차감축), 기본 흑연은 휴면이다(HANDOVER L20·L22). 서술 순서는 사용자 논문 convention(원형식 먼저 → 상호작용 항 추가)을 따른다(계획 L115·L200).

**코드.** `func_L_q`·`_causal_memory` 에 ratio 보정·전달함수(FFT) 옵션, 기본 `lag_ratio_correction=False` → 기존 dQ/dV bit-exact(G1 max|d|=0.0)(HANDOVER L21). 게이트 `test_gates_v1023.py` + `test_gates_v1023_selfconsistent.py`(L43). v1.0.22 parity 는 순수 additive(공유 함수·47섹션 byte/sha256 동일)(L29).

**게이트·빌드.** P0 GREEN baseline 83/25/17·bit-exact·구조 PASS(계획 L25). 코드↔문건 적대적 5창(AUD-1~5) 치명 0, 중대 2건(부록 E 수치 증거 문장 과장/오귀속) 정정 완료(HANDOVER L26-L28).

**사용자 결정 verbatim.** "본문의 수식을 푸는 기법" → 수학은 부록 E(계획 L15) · "제대로 적용은 코드"(계획 L127) · "양 버전 빡세게 코드↔문건"(HANDOVER L24) · D3 = P4 Tier2 Fisher 미실행(HANDOVER L15). D1(Tier1 만)·D2(부록 E + §8 포인터)·D4(Ref.6·7 미제공 전제)는 계획서 기본값과 집행 결과가 일치하나 사용자의 명시 확정 기록은 배정 원천에 없다(근거 미발견 — 계획 L216 "무응답 시 기본값으로 진행" 규약 적용 추정).

**유실·park·미결.** P4 Fisher 정보기하(Tier2, 피팅 식별성)·Legendre-Fenchel 명명노트(Tier3)는 D3 보류(HANDOVER L34; 계획 L142-L143·L210). **Ref.6·7 원문 미소장** — 서지는 Ref.6 = S. Lee, C. Y. Son, J. Sung, S. Chong, JCP 134, 121102 (2011); Ref.7 = C. Y. Son 외, JCP 138, 164123 (2013) 으로 계획서에 적혀 있고(계획 L43), 제목·DOI 는 "정직 유보"(HANDOVER L35). 이것이 brief §4.1 "refs 6·7 원문 미소장" 과 DR-8 의 원천이다. "양 버전 샘플 이미지 QA(연속·매끄러움·미분가능성, 전이 경계·미해상 가드 전환점 line 574·ratio 경로 kink)" 는 "진행 예정" 으로 기록됐고(L33) 후속 집행 기록은 배정 원천에 없다(근거 미발견; git untracked 에 `results\process\C3_graph_check\`·`docs\v1.0.17\sample_test_*.png` 류가 있으나 미정독). **"v1.0.24 역문제(Tikhonov/Bayes deconvolution) 후보"**(L36; 계획 L71)는 실제 v1.0.24 가 반영·검증 캠페인으로 진행되며 채택되지 않았다 — 방향 전환 지점이다. 기각 서베이군(Wiener-Hopf·WKB·다중척도·중심다양체·Langevin·Preisach 연산자·Kubo 동적 χ)은 non-goal 로 정직 표기(계획 L70) — brief §4.5 의 "SURV 기각군 승계" 근거.

### 2.5 [계획 전용] anodefit 마스터 플랜 · v1.0.24 완성도 검증 계획

두 계획서는 같은 날(2026-07-18) 작성됐고 어느 쪽도 그 형태 그대로 실행 Result 를 남기지 않았다(배정 원천 기준 근거 미발견). 등록부에 넣는 이유는 방향성 유실·park 의 시드가 여기 있기 때문이다.

**anodefit MASTER(`plans\2026-07-18-anodefit-MASTER-plan.md`).** 북극성 = 문건·코드가 노이즈 없는·물리 기반·T/I/V 의존 반쪽셀/전셀 dQ/dV 곡선 엔진이 되어 ① 노이즈 코인셀 실측 대체 ② 매칭의 경험적 fudge(M·X·Y) 물리 대체 ③ LAM·LLI·RI 상태 추론(L11-L16). 핵심 통찰 = M 은 dQ/dV 브로드닝으로 낮아진 피크가 dV/dQ=1/(dQ/dV) 에서 커 보인 것을 억지로 맞춘 인자이며, 브로드닝 물리(폭 w + lag L_V)가 작동하면 M 은 사라진다(L23). 캠페인 A(브로드닝·M-제거)·B(전셀·LLI carrier)·C(T/I/V 스케일)·D(공개데이터 검증)·E(상태추론)·G(문서)(L48-L76). 버전 로드맵 v1.0.24 = A+D, v1.0.25 = B+C, v1.1.0 = E(L80-L86). D1~D7 결정 요청 상태(L109-L126). 거버넌스 문구 "확인 받을 방향성을 최대한 상세히"(L5), 사용자 "극도로 민감"(L61)이 인용돼 있다.

**v1.0.24 완성도 검증 계획(`plans\2026-07-18-v1024-completeness-validation-plan.md`).** 사용자 확정·GO 2026-07-18: 대상 화학 = LCO·흑연·흑연+Si(세 화학 전부 v1.0.23 보유 → 커버리지 gap 없음), 순서 흑연→LCO→블렌드, V1(공개데이터 조사)부터 착수(L8-L11). 회사 표준 조건(사용자 제공) GITT·0.05C·0.1C·0.2C × 15·23·35·45 °C(L36-L38)가 브로드닝 3출처를 자연 분리한다(L19·L40-L46). Phase V0~V6, Steps 1–31(L57-L65). Correction History 에 "BDD·풀셀·매칭·상태추론을 스코프에서 완전 제외(사용자 3회 지적 — 'BDD는 참고 예시일 뿐')" 가 기록돼 있어(L184) 마스터 플랜의 캠페인 B·E 는 사용자 결정으로 이 프로젝트 밖으로 밀려났다.

**집행 상태(추정).** `docs\v1.0.25.1\results\HANDOVER_v24.md` L9-L15 의 Phase 표는 R0~R4(reflect) 이고 `plans\2026-07-22-v1024-feedback-revision-plan.md` L30 은 직전 계획서를 `plans\2026-07-19-v1024-si-2L-codex-reflection-plan.md`(미정독)·원장을 `V1024_REFLECT_EXECUTION_LEDGER.md`(R0–R5 = step 1–27) 로 지목한다. 따라서 V0~V6 계획은 하루 뒤 reflect 계획으로 대체된 것으로 보이며, V2(GITT×T 폭 T-스케일)·V3(율 시리즈 ∝|I|·휴면 판정·L_V(T) Arrhenius)·V4(M-제거 증명)·V5(식별성)는 **미집행 후보**다. 다만 D 캠페인의 일부는 v1.0.24 사후 강화의 SINTEF 공개데이터 피팅(단일 프로토콜·상온)으로 부분 실현됐다. 이 판단은 추정이며 DQ-3 에 올린다.

### 2.6 v1.0.24 — 최근문헌+Codex 반영(@3 Si Frumkin·@5 stage-2L·LCO 전자항 토글) + 사후 강화

**날짜.** 계획서는 2026-07-19 reflect plan(미정독·추정). R4 마감 후 강화분 최종 커밋 709d9e9(`docs\v1.0.25.1\results\HANDOVER_v24.md` L64). 사후 강화는 FB 리비전(07-22) 이전이다.

**구조.** 3챕터 유지. 신규 소절 3 = §1.5.4 stage-2L(`ch1_sec05b_gr2L.tex`), §3.2.5 Si Frumkin(`ch3v22_sec02b_sifr.tex`), §2.6.1 LCO 전자항 토글(`ch1_sec16b_lcoomega.tex`)(HANDOVER L6; 파일명은 `results\comp_v24\USER_FEEDBACK_v1024_READING.md` L189-L191). R1 은 9창 병렬 경쟁 저작 → W9 base·master 재조정(L13·L17). 빌드 91/28/20p(L47). `CODE_GUIDE_v24.md/.html`(`INDEX_v25.md` L94-L95).

**물리·식.** @5 stage-2L = 진짜 두-상 stage-2L 의 엔트로피 온도분리. 가운데 쌍(3↔2L·2L↔2) 반응 엔트로피 차 Δ(ΔS)≈29 J/mol/K → ∂/∂T(U−U) = Δ(ΔS)/F = 0.30 mV/℃(재현 0.271, ~90 %), 병합 ~10 ℃, 45 ℃ 2피크/25 ℃ 병합, operando XRD 독립근거(Schmitt 2022). 정직: 상온 단일 곡선 R² 이득이 아니라 **다온도 서명**이다. 판정자 dμ/dθ|½ = 4RT−2Ω 는 얹되 두-상/고용체 분류는 §7(sec:broadening-class)+피팅 Ω 로 위임하고, 5-feature 세분은 선택 코드 시드로 4-전이 기준을 대체하지 않는다(L21-L26). @3 Si Frumkin = a-Si 는 폭 판정 w/(RT/F) = [1.45, 2.74, 1.09] ≳ 1(흑연 두-상 20–50× 대조)로 단일상 고용체; 커널 dQ/dV = QF/|RT/[θ(1−θ)] − 2Ω|(Ω<2RT), Ω→0 로지스틱 폴백 bit-exact; 유일 두-상 = 1차 c-Li₁₅Si₄; Ω_Si 는 범위 시드일 뿐 점-식별 안 됨(L27-L29). 사후 강화에서 sifr warnbox(v) "Ω>2RT 커널 유효범위 밖" 을 코드(`_regsol_binodal_xa` Maxwell 공존)에 맞춰 정정했다(L69). LCO 전자항 토글 `include_electronic_entropy` 기본 False — 상온 커브는 토글 무관 불변(전자항이 ΔH^eff 로 흡수), 토글은 ∂U/∂T 만 가름, plain MSMR R²=0.944≈흑연 0.940(L30-L34). #7 Ω_j^cat = 유효 평균장 쌍상호작용 축약(미시 질서상 아님)(L35). #1 `func_L_q` 단위계약 c-rate[1/h] vs Eyring[1/s] 3600× → dH_a^phys = dH_a + RT ln3600 ≈ dH_a + 20.3 kJ/mol(감사서 부호 −→+ 정정, 값 bit-exact 무변경)(L36·L70). 흑연 6-gallery MSMR(`GRAPHITE_STAGING_MSMR6_LIT`, ad2061 ω_j·U0_j) opt-in — 해상도 사다리 {4-전이(기본)·5-feature XRD·6-gallery MSMR}, §5b 에 gallery ≠ 물리상 명시(L73).

**코드.** additive·bit-exact 4건(L7). 사후 감사에서 잠재 코드버그 1건 수정 — `_regsol_dqdv` 용량 +0.063 % → `wi=Q/xg.size`(area=1.000000·로지스틱 bit-exact 불변)(L70). 코드 sha256 `f230f59b`(L87; 이후 v1.0.24.1 까지 불변).

**게이트·빌드.** 3장 0-error 91/28/20·undefined 0·STRUCTURE PASS(L47). 게이트 G1 bit-exact 0·selfconsistent 5/5·reflect 4/4·R6 3/3(L48·L71). R3 통합 적대검수 3차원 CLEAN·blocker 0(L49). ★부수 복구: R0 에서 구조검증 도구 JSON 모드가 `ch1_graphite_v1.0.24.tex` 마스터를 덮어써 커밋됐던 것을 v1.0.23 셸+빌드로그로 재구성(L50) — brief §4.1 의 "`check` 서브커맨드만 사용" 경고의 원천이다. 사후 강화: SINTEF Zenodo 20086298(CC-BY-4.0) 실측 pOCV 를 @3/@5 실제 코드경로로 피팅 — 흑연 @5 5-feature 0.9525→0.9731, Si @3 Frumkin regsol 0.9944(a-Si 고용체 + c-Li₁₅Si₄ 두-상 자발 재현), 블렌드 0.9848(f_Si≈0.75)(L68); 전수 doc↔code 정합 감사(`AUDIT_v1024_DOC_CODE.md`, 6 병렬 에이전트 + 마스터 재검증) 곡선·피팅 정확성 BUG 0(L70).

**사용자 결정.** 사용자 선택 @3·@5(L6) · LCO 전자항은 사용자 안 A(챕터 유지 + on/off 토글)(L7) · "커브 구할 땐 빼고"(L31, 원천 큰따옴표). 반영 계획서(2026-07-19)의 결정 표는 미정독이라 여기 옮기지 않았다.

**유실·park·미결.** 정직한 한계(회사 데이터 위임, L52-L57): stage-2L 0.30 mV/℃·병합 10 ℃ 다온도 미검증(tier B, Schmitt 2022 는 부호·경향만) · Ω_Si·Ω_j^cat 점값 미식별 · O3-LCO 전자항 온도의존 미검증 · tab:staging ΔS(+15/−14)는 초기값(0/−5)의 피팅 갱신 대상(표 미편집·P5). 차기 옵션(L59-L62): 유한율속 `dqdv()` regsol 커널 확장(v1.0.25 의 regsol 삭제로 소멸) · 회사 다온도 반쪽셀 데이터 후 round-trip 확정(**Task #38 미완**) · 모델 개선 후보 #1 흑연 전이 4→5–6(사후 6-gallery 로 집행) · #2 비대칭 폭(+~1 %, → v1.0.25 @2) · **#4 정칙용액 자유에너지 = R²≈0.96 천장(MSMR 두-상 near-delta 한계)의 진짜 해법, Ch2–3 열역학 과제** — 이것이 brief B2 IMPROVEMENT #4·B3 정칙용액+Maxwell 헤드라인의 원천이며 v2.0.0 작업 챕터 3.1 의 핵심 후보다(내 판단).

### 2.7 v1.0.24.1 — 1차 정독 피드백 리비전(F-01~F-11 · FB0~FB7)

**날짜.** 2026-07-22(`docs\v1.0.25.1\results\HANDOVER_v24.md` L77; `plans\2026-07-22-v1024-feedback-revision-plan.md` L3). Ch1 피드백 완료 선언 2026-07-22(`results\comp_v24\USER_FEEDBACK_v1024_READING.md` L126).

**구조.** 문건 한정 리비전, 코드 bit-exact 무변경(HANDOVER L79·L87). 계획서 D1 은 "v1.0.24 in-place 리비전(신 버전번호 X)" 이었으나(계획 L219) 결과물은 `docs\v1.0.24.1\` 폴더로 남았고 v1.0.25.1 이 이를 "동결 사본 + 리비전 식별 = 폴더명" 선례로 승계했다(`V1025_1_TOUCHUP_NOTE.md` L4; `HANDOVER_v25.md` L153)(DQ-9). 빌드 97/30/21p(L87). FB1(F-11) 본문 코드 함수명 → 부록 전용(grep 0) + CLAUDE.md P3-8 명문화 · FB2(F-06) 여백 25 mm·줄간 1.16·문단 0.55 em·microtype · FB3(F-04·05·10) register+제목+용어(수필체·survival 술어·판번호·자기-diff·정직 형용사 평서화, 제목 N-태그 제거 ~33) · FB4(F-02·03) 노테이션 · FB5(F-07·09) E.3 itemize 전환·식 2.39 재확인·전역 픽셀-스캔 149쪽으로 overflow 3건 추가(Table11 `l l l l`→p{}·식 2.18 주석 축약·식 2.36 multline) · FB6(F-01·08) §1.1.4 배경 박스 ~50 %↓(인용 5종 보존)·LCO 서두+제목 차이-선도(σ_d·order-disorder·전자항)(L81-L86).

**물리·식.** 물리·식번호·label 정의 불변(P→p 개명·식 2.36 multline 도 식번호 보존)(L87). 확률 P→소문자 p(압력 P 유지·Part T 소문자 p 와 정합), f_int 자리당 vs Helmholtz F 가드(L84). 용어: 요동/양성→영문(body 0)·음함수/섭동/준위→국문+첫 병기·유일근→"유일한 근"(L83). 이력이 확정한 재-litigate 금지 항목(계획 L34-L39): 제목 명사구화·물음형 제거(rubric A·V1014 audit), 대정준·정준·분배함수 = 유지 확정(V1013 정책·rubric C2), 코드=부록(헌법①·rubric A5·CODE_MENTION_AUDIT 1차 집행 → F-11 은 2차 재발), 대문자 총량 F/S vs 소문자 자리당 f/s 노테이션 락(convention-lock), 기호 충돌 = 각주 가드 선례(rubric B5).

**코드.** 무변경, sha256 `f230f59b` 불변(L87).

**게이트·빌드.** 0-err·undefined 0·본문 코드 grep 0(L81·L87). FB7 적대검수 3창 병렬(피드백완전성·register/용어·물리/label) → `PHASE_FB7_RESULT.md`(L88). 사용자 요청 재검 감사(`VERSION_COMPARISON_v19_v23_v24.md`): 3창 대조 37 공통 절, **품질 하락 0**, v19 구문·v23 논리 모두 보존, 유일한 실질 변화 = 의도된 voice 평탄화(F-04/F-10/F-01 trade-off)(L10-L12·L52). v23→v24 변경은 파일당 0~16줄 lexical, Part T/LCO 5파일 byte-identical(L25). Part T 사슬·부록 E 자기일관 사슬 100 % 동일(L58-L59).

**사용자 결정 verbatim.** "1차 피드백 끝. 수정하여 1.0.24 리비전하라. 작업 계획서부터."(계획 L206) · "챕터1 문건 피드백 끝."(USER_FEEDBACK L126) · "피드백 전부 줬다"(조건 발화, L4) · "누가 1.0.24만 읽으래"(계획 L210) · "이전 버전 계획서·이력 전부 확인하고 계획서 쓰라"(계획 L210) · "이전 이력 전부 보라"(계획 L21) · "v19=구문 최고·v23=논리 최고. 이 둘과 v24를 어투·구문·내용·논리로 재검. 과거 이력 대조해 의도된 변경인지 퀄리티 하락인지 판정."(VERSION_COMPARISON L3). 피드백 원장의 F-04(전공서적 문체, "거시 열역학으로" 예시)·F-10(억지 한글화 금지, "요동"·"양성" 예시, 일본어 기반 번역 단어 배제)·F-11(코드는 부록 외 언급 금지)·F-02(확률 소문자 p)·F-06(조판)·F-08(Ch2 도입 차이 중심)은 원장이 "사용자 지적" 으로 요지 기록한 것이라 verbatim 이 아니다. 계획서 D1~D6 은 기본값 GO 이며 F-02 P→p·F-08 은 "이미 방향 주신 항목" 으로 재질의 없이 집행됐다(계획 L216-L224).

**유실·park·미결.** VERSION_COMPARISON §5 복원 옵션 3건 — (권장) §1.1.4 "엔트로피 해석지도 → 본문 4절" 교차지도 문장 1개 복원, (선택) appE·sec01_map 투명/교육 voice 부분 복원(F-04 재판단 필요), (선택) fluctuation 혼합 register 재판단(F-10 사용자 직접 지목) — 사용자 판단 미집행(L64-L72). 항목 #7 worked example U_j(298.15) 표시값 210.87→210.88·85.29→85.30 은 F-번호 미추적 유일 변경이나 표시 반올림·물리 영향 0(L50). 지배 문서 4종(`CLOSING_v1.0.15`·`V1020_STYLE_RUBRIC`·`V1013_TERMS_POLICY`·`V1014_TONE_AUDIT`)은 계획서가 gate 로 편입했으며 본 등록부에서는 미정독·참조만이다.

### 2.8 v1.0.25 — 국소 수정판(@2 skew opt-in·인과 pad·SI opt-in·regsol 삭제·데이터 정직화)

**날짜.** 2026-07-26(`docs\v1.0.25.1\results\HANDOVER_v25.md` L8; 계획 v1 및 v2 모두 2026-07-26, `plans\2026-07-26-v1025-surgical-skew-consistency-plan.md` L227-L228).

**구조.** 전문 재작성이 아닌 국소 수정판(계획 L3). `_sections` 14파일 +257줄(마스터 보고 +250, 서브 재계수 +257 — 편집 진행 중 계수)(HANDOVER L56; `INDEX_v25.md` L39-L40), 신규 라벨 3(`eq:skewpeak` boxed·`eq:skewapex`·`eq:gr2l-fwhm`)·삭제 라벨 0·`\boxed` 38→39·문장 삭제 전 버전 통틀어 1건(sifr 의 코드 폴백 서술 — 코드 삭제로 거짓이 됨)(INDEX L46-L47·L58·L134-L135). 편집 파일별 요지는 INDEX L46-L59 에 있다(§6 skew 식 2개 / §5b FWHM·해상도 사다리 7-gallery / §7 "(추가 축) 평형 비대칭 α" / §18 4-손잡이 warnbox / §5 폭·형상 분업 / §9 pad 각주 / §10 C_bg·CODATA 각주 / 부록 B 코드맵 3행 / 부록 E 양 경로 pad / Part T mixing warnbox 조준 좁힘 / Part T §8 74.4(raw 74.35) 병기 / Ch2 부록 B raw 판정 / Ch3 sifr 4건 / Ch3 cases 프로토콜 의존 feature). 마스터 3 tex 는 표시 버전(pdftitle·lhead·`\date`)만 1.0.25(DG-2), 파일명·`\input` 46개·`\externaldocument` 4개·`common_preamble_v1024` 개명 금지, 잔존 `1.0.24` 문자열 12곳은 전건 "남겨야 함"(HANDOVER L47·L140-L142). `ARCHIVE_NOTE.md` 40줄 무삭제 + S1~S6 추기(109줄)(L57).

**물리·식.** (1) @2 skew-logistic: dQ/dV = Q(α/w)ξ_eq^α(1−ξ_eq), 면적 α 무관. ★α 는 현상학적 형상 파라미터(tier C)이고 새 물리·새 상이 아니며 순수 비대칭 손잡이도 아니다 — 반높이 폭이 α=0.5/1/2/4 에서 4.45/3.53/3.02/2.74 w 로 함께 좁아져 w_j(n_j)와 축퇴하고 정점이 σ_d w_j ln α_j 만큼 밀린다(α=2 → +17.8 mV) → "정점 = 중심 U_j^d" 는 α=1 한정, §18 4-손잡이(α·L_V·gallery 세분·w_j) 식별 가드(L73-L77·L143-L144). (2) 인과 pad: `eq:lag` 하한 −∞ 실현, 세 시작점 상대산포 74.31 % → 2.17e-04, pad 잔여 e^{-5}≈0.674 %; ratio 경로에도 같은 pad 를 넣어야 동결 극한 정확 회수가 유지(L78-L80). (3) 상수 SI opt-in: 문건 25.693 mV = CODATA-2018 vs 구현 기본 25.6912 mV; 즉시 교체는 골든 bit-exact 계약과 양립 불가; SI 발효 시 회귀 기준은 표시 자리까지 불변, `U_oc(x̄=0.25)` 만 raw 74.3511→74.3497(−1.42 µV)로 `.1f` 표시 74.4→74.3 반올림 절벽 → 정합 판정은 raw 값(L81-L84). (4) regsol 삭제: 근거는 물리 오류가 아니라 실측 역전 — 전이 수 고정(흑연4+Si3) +0.97 %p → 승격(흑연7+Si7) −0.53 %p; 이득의 실체 = 전이 수 부족의 우회·gallery 세분과 중복. ★Ω 파라미터 전량 존치(히스 gap·ΔH_a^eff·§7 상성격 판정); `eq:sifr-kernel`·`eq:sifr-blend` 식·라벨·boxed 보존, 지위만 "해석적 기록 — 미채택·코드 미구현"(L85-L89). (5) w_eff 정정: 중심 높이 Q/(4w_eff) 는 전 λ 정확 항등이나 폭으로 읽으면 ≈0.66/√λ 배 과대(λ=10⁻²/10⁻³/5×10⁻⁴ 에서 6.6/21/30배); FWHM 닫힌형 `eq:gr2l-fwhm` 점근 (16/3)(RT/F)λ^{3/2}, 과대율 λ=0.01: 0.6 % · 0.02: 1.2 % · 0.05: 3.0 % · 0.5: 27 % → λ≳0.02 에서는 닫힌형; Ω=2RT 초과 시 Maxwell 공존평탄으로 불연속 전환이라 "연속 보간이 아니다"(L90-L94). (6) gallery ≠ 상: 7·9전이 중심 U 가 기존 3위치(105/141/227 mV)에 ΔU<12 mV 근축퇴로 붙고 검출 피크 수는 prominence 문턱 따라 3→4→5, Si 0.43–0.46 V feature 는 `p-ocvhold` 전용; XRD 상 수 불변(L95-L97). (7) 데이터 정직화: 레포 `gr.csv` = gr_A = `p-ocv` / `si.csv` = si_Dhold = `p-ocvhold`(프로토콜 혼용); 같은 7전이로 0.9770 → 0.9945(피크역 RMSE 4.708→2.701) → 잔차 상당분이 데이터의 비평형 잔여; comp_v24 원본 무수정·addendum supersede(L98-L100). (8) 배경 C_bg: 0.3–0.9 V 에서 0.433→0.032 단조 감쇠(창 평균의 ~230 %·4셀·2프로토콜 일치) — 창-국소 상수 근사; 광폭 종 단독 대체는 악화(0.97702→0.97415), skew 동반 시에만 이득(0.98178)(L101-L102). @1~@5 실측표(계획 L44-L53): 기준 5전이 0.97090 → @5 7전이 0.97702 → 9전이 0.97890 / @1 near-delta 0.97436(무익) / @3 0.95~0.97(악화) / @4 U 고정 0.93215(유해) / **@2 skew 0.98078(최대 이득)** / @2+광폭 0.98178. Si 전이 수 스윕 7전이 포화(0.99974)(HANDOVER L43).

**코드.** 파일명 유지·내부 release 1.0.25. 추가(전부 additive·미지정 시 bit-exact): `func_dxi_eq`(L148)·`_alpha_factor`(L511)·전이키 `alpha`(부재=1.0)·`_causal_pad`(L199, `_LAG_PAD_NLV=5.0`·`_LAG_PAD_MAXPTS=4000`·간격 ≤ L_V/20)·`R_SI`/`F_SI`/`use_si_constants()`(L106-L111)·`SI_MSMR7_LIT`(L1357). 삭제: `_REGSOL_XG`·`_regsol_binodal_xa`·`_regsol_dqdv` + `equilibrium()` 의 `'kernel'` 분기 → 커널 계통 = 로지스틱 단일계. 보존: Ω 코드 전량(`func_dU_hys` L312·`func_dH_a_eff` L330). 아카이브 1734 → 1917줄(+183); 1957→1917(−40)은 regsol 삭제 그 단계만의 변화(INDEX L17·L131-L132). 게이트 `test_gates_v1025.py` 신설(G-α1~4·G-창·G-극단·G-SI·G-si7 8종, ★G-금지 미구현 — INDEX L23), `test_gates_v1024_reflect.py` G-R3 를 "regsol 삭제 확인"(심볼 부재 3/3 + `'kernel'` 키 무시 legacy dict `array_equal` + 면적=Q=0.999881)으로 재작성해 4/4 유지(INDEX L24).

**게이트·빌드.** 게이트 전건 GREEN·골든 bit-exact max|d|=0.0(HANDOVER L55). STRUCTURE PASS·STRICT ALL PASS·doc↔code 30/30 — 전부 02:06 이전 실행분이고 그 뒤 마스터가 `_sections` 4파일을 더 수정(N3)(L56·L112). ★**LaTeX 빌드 미수행**(이 PC 에 TeX 배포판 부재) — 머지 차단 유일 항목 N1(L59·L110; 계획 L190). 계획 이탈 3건 = C3 "즉시 교체"→opt-in(골든 bit-exact 와 수학적으로 양립 불가) · C6 "강등"→완전 삭제(DG-1(b)) · 신규 라벨 1→3(계획 L229-L234; INDEX L68).

**사용자 결정 verbatim.** DG-1 "regsol 삭제"(HANDOVER L46; 계획 L16·L210) · DG-2 "파일명을 왜 바꿔? 버전명만 바꿔주면 되는거 아니냐?"(HANDOVER L47; 계획 L17·L217-L218) · 지시 10 "물리·화학 논리를 건드리는 문건 작업은 Opus 5.0, 나머지는 Opus 4.8"(HANDOVER L48 — 원천이 "요지 인용" 으로 표시). D-A(@2 opt-in)·D-B(gallery opt-in 유지·기본 전이 수 승격 X)·D-C(regsol/@1/@3/@4 배제·Ω 존치)·D-D(국소 수정 원칙)는 사용자 2026-07-26 확정(계획 L10-L15). 지시 1~11(검수 요청·패치 결정·"문건 = 코드" 프레이밍·공개 데이터 실측 판정·@1~@5 조합 재검증·세 물리 질문·계획서+Fable 집행·DG-1·DG-2·모델 배분·GitHub 업로드)은 HANDOVER L37-L49 에 요지로 재구성돼 있고, 지시 6 세 물리 질문은 "(전문 미전달) — 원문 확인은 마스터 소관" 이다(L44)(DQ-7). 모델 배분 이력 표(L63-L69)는 attribution 근거로 보존해야 한다(마스터 Opus 5.0 문건 T1~T12 직접 편집 / 실무 서브 Opus 4.8 T13·T14·마감문서 / 코드 서브 Fable 5.0 C1·C2·C3·C7 + G0).

**유실·park·미결.** N1~N13(HANDOVER L108-L122)은 §4 에서 현행 상태와 함께 다룬다. `CODE_GUIDE_v24.md/.html` 은 v1.0.25 미갱신이라 서술된 `'kernel':'regsol'` 경로가 더 이상 존재하지 않고, `FITTING_GUIDE.md` 는 `alpha`(tier C)·`use_si_constants()` 미반영이다(INDEX L94·L96). `MERGE_READINESS_v25.md` 의 미해결 통합 표 X1~X14(INDEX L67)는 미정독이다. `REFLECT_SEED_TABLE.md` §1 "@3 개선효과" 행과 §2 "6+ = curve-fitting" 행은 addendum A4·A7 이 supersede 한다(INDEX L83) — 읽는 순서 = comp_v24 원본 → addendum(충돌 시 addendum 우선)(HANDOVER L150-L152).

### 2.9 v1.0.25.1 — v1.0.25 독립 검증 + 정직성 touch-up 리비전 (현행 최신 문건)

**날짜.** 2026-07-26(`docs\v1.0.25.1\results\V1025_1_TOUCHUP_NOTE.md` L3).

**구조.** 별도 폴더 `docs\v1.0.25.1\`, v1.0.25 의 폴더·보고서·커밋은 무수정 보존(main 에 cherry-pick, L5-L6). touch-up 4건 = 전부 산문 additive, `_sections` 3파일: `ch3v22_sec02b_sifr.tex`(F1 HIGH·F3 LOW)·`ch1_sec05_width.tex`(M-w MED)·`ch1_sec06_eqpeak.tex`(L-bg LOW-MED)(L30-L35). 표시 버전만 v1.0.25.1(DG-2 승계), 코드 release 문자열 1.0.25 유지(L48). 빌드 **102/30/22p**(L55). brief §4.2 의 자산 카운트(display 230·boxed 64·label 429·bibitem 95·cite 265/93·section 49·subsection 115·figure 28·table 20·박스 7종)는 master 실측이며 본 등록부 원천에는 없다(미검증 — 작업 챕터 2.1 이 재계수).

**물리·식.** 식·라벨·`\boxed`(39) 불변(L28·L49). F1 = regsol 삭제 근거가 n=1·기준불일치·미검증임에도 확정처럼 서술되던 것을 완화 — "더 적은 가정으로"(방향 오류: gallery 는 모수가 더 많음) → "별도 커널 계열 도입 없이 기존 로지스틱 자유도만으로" + 단일 셀·AIC/BIC 미확정 유보 1문(재현 위임 M6)(L32). F3 = 긍정형 boxed 의 Frumkin-Si 항에 "해석적 기록·채택 경로는 로지스틱 단일계" inline 표식(L33). M-w = §5 "유효 폭" 서술에 "중심 높이 척도이지 반높이 폭 아님 — FWHM 은 λ^{3/2}, §5b" 포인터(L34). L-bg = §6 verifybox iii 감수율 항등 유도 서식이 이상격자(Ω=0)뿐 아니라 대칭 종(α=1) 한정임을 명시(L35). 마스터 독립 검증: skew 손검산(정점이동 σ_d w ln α, α=2 → +17.8 mV; 높이 (Q/w)[α/(α+1)]^{α+1}; 면적 α 무관), FWHM (16/3)(RT/F)λ^{3/2} 독립 유도 정확·λ=0.5 에서 27.5 %, v1.0.24 "폭=λ 연속화" 오류 정정 타당(L21-L22).

**코드.** byte-identical(v1.0.25 와 동일), 델타 289줄 전문 정독 — 매 변경 `if α==1: bit-exact` 분기·가드·regsol 삭제 클린·Ω 물리 전량 보존(L23·L43).

**게이트·빌드.** 4종 스위트 직접 재실행 — v1024(G1~R6)·reflect 4/4·selfconsistent 5/5·**v1025 9/9(G-금지 포함)**(L19) · 골든 max|d| = 0.0(L20) · 문건 산문 적대검수 2세션 정확성 오류 0(L24) · STRUCTURE PASS·STRICT ALL PASS·[E] 신규 라벨 0(L41-L42) · CRLF/BOM 편집 6파일 순수 CRLF·BOM 0(L44) · ★**XeLaTeX(MiKTeX 25.12) ch1→ch2→ch3 3-pass+xr 재빌드, 오류 0·undefined ref/cite 0·102/30/22p·대형 overfull 0·PDF 3종 커밋**(L55) — v1.0.25 N1 해소. origin/main push 성공(`results\comp_v26_data\HANDOVER_regsol_investigation.md` L8) — N2 해소.

**사용자 결정.** "사용자 지시로 Claude 작업만 현행화(로컬 `main` = v1.0.24.1 동기화)"(L12-L13, 요지). 반영 판정은 마스터 판단(L26). 이 PC 가 v1.0.19 시점에서 정체돼 있었고 origin 은 v1.0.24.1, 브랜치 `v1.0.25-surgical` 은 그 위 2커밋이었다는 git 위상 기록(L10-L12)이 brief §4.1 "모든 버전 브랜치가 main 의 조상" 의 배경이다.

**유실·park·미결.** N4(흑연 두-상 4 vs 2)·N6~N9(CSV 8종 보존·재현 스크립트·sigr 프로토콜·regsol 철회 다중셀)(L56-L57). F2 = supersede 데이터의 리포 미보존 = 재현성 후속 과제(문건은 이미 "미측정" tier 표기라 산문 수정 불필요)(L37).

### 2.10 v1.0.26 A/B — regsol 재검증(물리 4전이 regsol 판 vs gallery 7전이 판)

**날짜.** 착수 인계 2026-07-27(`results\comp_v26_data\HANDOVER_regsol_investigation.md` L3). 결과 문서 작성 2026-07-27(`docs\v1.0.26A-regsol\README.md` L5; `docs\v1.0.26B-gallery\README.md` L5). 커밋 4069cb3 "feat(v1.0.26 A/B): regsol 재검증 — 물리 4전이 vs gallery 7전이 두 버전 산출"(세션 git status 기재).

**구조.** 문건 tex 는 무변경이다. 이 버전은 tex 리비전이 아니라 **판정용 실측 조사**이며 산출은 작업 폴더 `results\comp_v26_data\` 와 결과 문서 두 본이다. ★brief §4.3 은 이 항목을 "실행 차단·미완" 으로 적었으나 실물은 다르다 — 배정 원천인 `HANDOVER_regsol_investigation.md` 는 "착수 시점 인계문서(서비스 장애로 실행 차단됐던 기록)" 이고(`results\comp_v26_data\README.md` L23), 그 뒤 실행이 재개돼 `out_versions\A_regsol\`·`B_gallery\`(07:42~07:44)·`out_v3\graphite_sweep.png`·`docs\v1.0.26A-regsol\`·`docs\v1.0.26B-gallery\` 가 생성됐다(폴더 실측 + `out_versions\build.log` L1-L36). 기준 코드 = v1.0.25.1(`main`)(A README L5). 다만 **평형 데이터 재검은 여전히 미실행**이므로 "판정 미완" 이라는 brief 의 실질은 유지된다(DQ-2).

**물리·식.** 질문 두 개 — ① regsol 은 물리 전이 4개로 gallery 7개로의 분화를 스스로 모사하는가 → 아니다(ΔBIC +844.5) ② regsol 을 되살릴 근거가 있는가 → 적합도로는 없다, 단 흑연 Ω≈2RT 는 문헌 앵커와 맞는다(README L9-L10). 결과(A README L51-L55; B README L50-L54): A regsol-4 흑연 R²=0.91506·BIC 2609.6·피크역 RMSE 18.754·**면적 결손 +12.05 %**(전하 보존 파손 — 급준 피크를 못 세워 과소적분) / Si regsol-4 0.99881·BIC −2665.7 / 블렌드 regsol-8 0.99717 · B logistic-7 흑연 0.97389·BIC 1765.1·면적 결손 +0.06 % / Si logistic-7 0.99975 / 블렌드 logistic-14 0.99953. 흑연 4전이 Ω/RT = 2.54/2.03/1.88/2.30 — 전부 2RT 근방(marginal 두-상), Cordoba 2024 Ω_a≈2.5RT 앵커와 정합(A L19·L124-L128). 판정 문장: **"흑연이 두-상이다"는 참이고, "그래서 regsol 커널이 gallery 를 대체한다"는 거짓**(A L19). regsol 의 우위는 N=4·5 에서만이고 N=6 부터 역전 — v1.0.25 의 "@3 이득은 전이 수 부족의 우회" 판정과 같은 구조(A L17). Si·블렌드에서 Ω 가 탐색 경계(Ω/RT=8.00·0.00)에 붙어 식별된 값이 아니며 near-delta 급준화 손잡이로 쓰임 = v1.0.24 가 @1 로 기각한 거동(A L116-L121). 전이 수 스윕(N=3~8, 흑연 BIC): logistic 3105/2714/2585/2128/1765/1768 · skew-logistic 2913/2388/2134/1954/**992** · regsol 3026/2610/2536/2491/1825 · skew-regsol 2816/2235/2093/1265(A L134-L143) → **skew-logistic-7(BIC 991.5, ΔBIC −773.6)이 최선**이고 "비대칭 α 가 전이 수보다 큰 단일 효과"(B L18). gallery 의 늘어난 전이는 새 봉우리가 아니라 같은 전압에 폭만 다른 근축퇴쌍(1→6개), N=8 은 과적합(B L16-L17). 방법: dQ/dV = 사용자 BDD `99_Backend` 방식 이식(dMSMCD 다중창 중앙값 미분 + 웨이블릿 denoise + savgol 앙상블, 등장성회귀 → 균일 V 격자), 피팅 `scipy.least_squares`(trf, bounded) 3-시드 × 4-재시작, 지표 R²·BIC·피크/벨리 RMSE·면적 보존(A L25-L31). 함정 2건 반영: 전압 1 µV 양자화(ΔV=0 550쌍) → `np.gradient` 로 10¹² 발산, regsol 조성격자 ripple → 혼화갭 닫힌형 + 고용체 밀도⊛FFT 합성곱으로 격자 의존 제거(v1.0.24 `_REGSOL_XG=1200` 대비 꼬리 위글 140배 감소·속도 55배)(A L36-L44).

**코드.** 문건 본 코드 무변경. 조사 코드 = `bdd_dqdv.py`·`regsol_kernel.py`(regsol/skew-regsol)·`test_skew_regsol_v2.py`(커널 4종·로더)·`test_gallery_vs_regsol.py`(전이 수 스윕 → out_v3)·`build_two_versions.py`(→ out_versions)·`make_version_docs.py`(→ docs README, 수치 전사 오류 0)(README L14-L21). ★폐기: `test_skew_regsol.py`·`out_skew/`(결함 3건 — `np.gradient` 발산·비대칭을 δL≠δR 조각폭으로 구현[v1.0.25 실제 채택분은 α 지수형]·정규화 4×·2× 오류로 면적=Q 파괴; 피팅 예외를 삼켜 4종 전부 실패한 채 빈 JSON), `regsol_decision.html`·`../regsol_test/`(README L28-L31; `out_skew\summary_skew.json` 실측 = `{"graphite": {}, "blend": {}}`). 배정 원천 HANDOVER 가 "지시 정확 이행" 이라 소개한 스크립트가 바로 이 폐기분이다(HANDOVER L35).

**게이트·빌드.** 빌드 없음. 착수 시점 차단 사유 = Anthropic 안전 분류기 서비스(`claude-sonnet-4-6[1m]`) 다운으로 모든 비-읽기 도구 fail-closed(HANDOVER L28-L30). 이후 실행 재개(폴더 실측). GITT/p-OCV+hold 평형 데이터 파이프라인(`dl_sintef.ps1`·`analyze_sintef.py`·`run.bat`)은 **미실행(잔여 과제)**(README L24). bootstrap 불확실도 미산출(README L49).

**사용자 결정 verbatim.** "24regsol 식에 25에 추가하기로한 내용들 추가해서 테스트 해보고 그 결과를 나한테 제시해. 그 결과를 이미지로 확인하고 나서 정할려니까."(HANDOVER L13, ★핵심 지시) · "두상으로 분리되는 걸 표현하려면 regsol이 들어가야 한다."(L12) · "지금 저게 잘맞는다고 보이냐? 개판인데?"(L15) · "미분이 매끄러워지라고 쓰라는 거지 안 맞는 게 맞게 되지는 않는다. 제대로 데이터 다시 찾아와."(L16) · "regsol에 비대칭 반영했던 그 시리즈를 반영해서 테스트하랬지? 그런데 그걸 했냐?"(L18) · "그래프 그려서 이미지를 달랬지? 왜 수치만 적냐"(L19). 요지: dQ/dV 는 사용자 BDD 프로젝트 `99_Backend` 방식 참고, 흑연·실리콘·블렌드 3종 전부(L15), 야간 자율 완수(L17). ★regsol 되살리기 여부는 **사용자가 이미지로 확인하고 결정**하는 것으로 명시돼 있으며(L13·L54), 결정 기록은 배정 원천·추가 확인 원천 어디에도 없다(근거 미발견).

**유실·park·미결.** ★평형 데이터 재검 — 현 판정은 전부 plain p-OCV(C/50, 가장 비평형) 위에서 나왔고 GITT/p-OCV+hold 로 재실행해야 확정된다(A L162-L166; README L46-L48). 흑연 0.104 V 피크 FWHM ≲ 1 mV(RT/F 의 1/25; V 폭 0.6 mV 에 2,400점·0.29 mAh) — 대칭 로지스틱은 w 0.4 mV 가 필요해 고용체로는 불가, 두-상이면 자연스럽지만 비평형 인공물 가능성 미배제(A L167-L170). 소재별 되살리기(Si = Frumkin 고용체 유력 / 흑연 = near-delta 불필요·regsol+유한δ 검토)는 사용자 결정(HANDOVER L54). N6 신규 CSV 리포 영구보존·N4 Dahn1991 본문(HANDOVER L55; README L49). "파라미터는 seed 이지 신뢰값이 아니다"(단일 셀·단일 온도·단일 율속·bootstrap 미수행)(A L173-L174).

---

## 3. 후반 구간의 계보 연결선

v1.0.20 은 v1.0.19 를 물리 골격 무변경으로 정정·보강해 동결했고, 확장 전건을 v1.0.21 로 분리한다는 사용자 결정이 이후 "원본 보존 + 새 폴더" 관행의 출발점이 됐다. v1.0.21 은 전하 보존식을 대정준 반전으로 1급 승격하고 TST 배경을 붙였으며, 항법 인프라와 Si 예비 지도를 만들었다. v1.0.22 는 활물질별 3챕터로 재편하면서 열특성을 Ch1 Part T 로 흡수하고 Si·블렌드 장과 코드를 신설했으며, 계보 감사로 자산 무유실을 확인했다 — 현행 v1.0.25.1 의 골격은 여기서 고정됐다. v1.0.23 은 사용자 논문의 ratio 닫힘을 동역학 lag 한 자리에 정직하게 접목해 부록 E 를 세웠고, 사용자는 이 판을 "논리 최고" 로 평가했다(`results\comp_v24\VERSION_COMPARISON_v19_v23_v24.md` L3·L22). 2026-07-18 의 두 계획서(북극성·완성도 검증)는 캠페인 지도와 회사 표준 조건 매트릭스를 남겼으나 그 형태로 집행되지 않았고, v1.0.24 는 @3/@5/LCO 토글 반영과 SINTEF 공개데이터 피팅·전수 doc↔code 감사로 진행됐다. v1.0.24.1 은 사용자 정독 피드백 11건을 집행한 문건 리비전이며 재검 감사가 "품질 하락 0·의도된 voice 평탄화" 로 판정했다. v1.0.25 는 실측이 뒤집은 판단(@3 역전·w_eff 폭 오독·데이터 프로토콜 혼용)을 국소 수정하고 regsol 커널을 삭제했으며, v1.0.25.1 이 이를 독립 검증·빌드해 현행 최신 문건이 됐다. v1.0.26 A/B 는 삭제된 regsol 을 되살릴지 판정하기 위한 실측 조사이며 "흑연 두-상은 참 / regsol 커널의 gallery 대체는 거짓 / skew-logistic 이 최선" 까지 왔으나 평형 데이터 재검과 사용자 결정이 남았다.

이 구간에서 방향이 바뀐 지점 세 곳을 명시한다. 첫째, v1.0.23 이 "v1.0.24 = 역문제 동반문건" 을 후보로 뒀으나 v1.0.24 는 forward 반영·검증으로 갔고 역문제·상태추론은 사용자 결정으로 프로젝트 밖(BDD 하류)이 됐다. 둘째, 완성도 검증 계획(V0~V6)의 M-제거 증명·휴면 판정·L_V Arrhenius 는 집행 근거가 없다. 셋째, v1.0.24 가 채택한 @3 regsol 커널이 v1.0.25 에서 실측 역전으로 삭제됐고, v1.0.26 에서 사용자가 "두상 표현에는 regsol 이 필요하다" 며 재검증을 지시했다 — 두-상 커널 문제는 이 구간 내내 열려 있다.

---

## 4. 현재 미완·미결 항목 (N4·N6~N9·regsol·Task #38 등)

상태 열은 4-tier 다. "승계처(추정)" 열은 brief §5 골격의 어느 작업 Phase 가 자연스럽게 흡수할지에 대한 **내 판단**이며 골격 변경 제안이 아니다.

| ID | 항목 | 발생 | 현행 상태 | 차단성 | 승계처(추정) | 근거 |
|---|---|---|---|---|---|---|
| **N1** | LaTeX 3-pass 빌드 | v1.0.25 | **해소**(확정) — v1.0.25.1 XeLaTeX 102/30/22p·오류 0·PDF 커밋 | — | — | `V1025_1_TOUCHUP_NOTE.md` L55 |
| **N2** | GitHub 업로드 | v1.0.25 | **해소**(확정) — origin/main push 성공 | — | — | `HANDOVER_regsol_investigation.md` L8 |
| **N3** | 정적 검사·doc↔code 감사 재실행 | v1.0.25 | STRUCTURE·STRICT 는 v1.0.25.1 에서 재실행 PASS(확정) · doc↔code 30/30 재실행 기록은 근거 미발견 | 비차단 | 2.1 자산 지도 | `V1025_1_TOUCHUP_NOTE.md` L41-L42 · `HANDOVER_v25.md` L112 |
| **N4** | 흑연 물리 두-상 4(Dahn 1991 초록, `comp_v24/GRAPHITE_STAGING_XRD.md`) vs 2(§7 권위: 2L→2·2→1) 표기 불일치 | v1.0.24 선행 | **미해소**(확정) — Dahn 1991 본문 확인 필요 · 챕터 내부 정합은 유지 | 비차단 | 2.6 두-상 커널 정식화 / 2.4 서지 | `HANDOVER_v25.md` L113 · `V1025_1_TOUCHUP_NOTE.md` L56 · `HANDOVER_regsol_investigation.md` L55 |
| **N5** | `ARCHIVE_NOTE.md` 표제 "v1.0.24.1 … 동결 아카이브" 잔존 | v1.0.25 | 근거 미발견(v1.0.25.1 note 무언급) | 비차단 | 2.1 | `HANDOVER_v25.md` L114 · `INDEX_v25.md` L93 |
| **N6** | 신규 CSV 8종(gr_B·gr_Dhold·si_A·si_Chold 등) 리포 영구보존·`DATASETS` 편입 | v1.0.25 | **미결**(확정) — v1.0.26 README 도 잔여로 재등재 | 비차단(재현성 손실 위험) | 2.6 / DR-6 | `HANDOVER_v25.md` L115 · `README.md`(comp_v26_data) L49 |
| **N7** | addendum A2·A4~A7 수치의 재현 스크립트 등재 | v1.0.25 | **미등재**(확정) | 비차단 | 2.6 | `HANDOVER_v25.md` L116 |
| **N8** | `sigr.csv`(블렌드) 원자료 키·프로토콜 | v1.0.25 | **미측정**(확정) | 비차단 | 2.6 | `HANDOVER_v25.md` L117 |
| **N9** | @3 철회의 다중 셀(n>1) 통계 | v1.0.25 | **미측정**(확정) — v1.0.26 도 단일 셀·bootstrap 미수행 | 비차단 | 2.6 | `HANDOVER_v25.md` L118 · `docs\v1.0.26A-regsol\README.md` L173-L174 |
| **N10** | 게이트 PASS 독립 재확인 | v1.0.25 | **해소**(확정) — v1.0.25.1 마스터 직접 재실행 | — | — | `V1025_1_TOUCHUP_NOTE.md` L19 |
| **N11** | G-금지 게이트(금지어 grep) | v1.0.25 | **원천 간 모순** — `INDEX_v25.md` L23 "8종·G-금지 미구현" vs `V1025_1_TOUCHUP_NOTE.md` L19 "v1025 9/9(G-금지 포함)" | 비차단 | 2.1(실물 `test_gates_v1025.py` 게이트 수 확인) | DQ-1 |
| **N12** | md 줄바꿈 CRLF/LF 이원화 | v1.0.25 | 근거 미발견(결정 기록 없음) | 비차단 | — | `HANDOVER_v25.md` L121 |
| **N13 / Task #38** | 회사 다온도·다율속 반쪽셀 데이터 의존 정량 — stage-2L 0.30 mV/℃·병합 10 ℃ · Ω 점값 · O3-LCO 전자항 T의존 · α↔L_V 율속 분리 | v1.0.24 승계 | **미완**(확정) — brief §6 Non-goal(warnbox·tier 정직 표기) | 비차단 | Non-goal | `HANDOVER_v25.md` L122 · `HANDOVER_v24.md` L52-L61 |
| **R-1** | ★v1.0.26 regsol 재검증 — skew-regsol/regsol vs gallery 판정의 **평형 데이터(GITT/p-OCV+hold) 재검** | v1.0.26 | **미실행**(확정) — 비평형 p-OCV 위 판정만 존재 | 비차단(설계 입력) | 2.6 / 3.1 | `docs\v1.0.26A-regsol\README.md` L162-L166 · `README.md` L24·L46-L48 |
| **R-2** | 흑연 0.104 V 피크 FWHM ≲1 mV 의 정체(두-상 vs 비평형 인공물) | v1.0.26 | **미판정**(확정) | 비차단 | 2.6 | `docs\v1.0.26A-regsol\README.md` L167-L170 |
| **R-3** | regsol 소재별 되살리기 결정(사용자 이미지 확인 후) | v1.0.26 | 결정 기록 근거 미발견 | ★사용자 결정 | 3.7 DG-B / DR-1 | `HANDOVER_regsol_investigation.md` L13·L54 |
| **R-4** | skew-logistic-7 이 BIC 최선이라는 v1.0.26 발견을 문건이 아직 반영하지 않음(v1.0.25.1 은 skew 를 opt-in·tier C 로만 둠) | v1.0.26 | **미반영**(확정 — 문건 tex 무변경) | 비차단 | 3.2 / 4.2 | `docs\v1.0.26B-gallery\README.md` L18 |
| **P-1** | P3-5 ref.6·7 원문 미소장(Ref.6 JCP 134, 121102 (2011) · Ref.7 JCP 138, 164123 (2013)) — 제목·DOI 미확정 | v1.0.22→23 | **정직 유보**(확정) | DR-8 | 2.4 / 3.5 | `HANDOVER_v23.md` L35 · `plans\...v1023...md` L43 |
| **P-2** | FR 보류 풀 M 158 + L ~120(각 `A##_REVIEW.md` LaTeX 보존) | v1.0.22 | **park**(확정) — 이후 채택 기록 근거 미발견 | 비차단 | 1.4 / 2.2 | `HANDOVER_v1.0.22.md` L94·L138 |
| **P-3** | 단일 문건 병합 이관 5항(부록 카운터·xr 제거·파트 명칭·tier 범례·bib 중복) | v1.0.22 | 착수 근거 미발견 | 비차단 | 3.3 구조 결정(xr 영향) | `HANDOVER_v1.0.22.md` L124-L129 |
| **P-4** | SiO_x 절대값 placeholder · Si dS_rxn 미부여(블렌드 발열 미구현) · GS-1 소성 히스 · GS-2 유한율속 비가산 | v1.0.22 | **정직 공백**(확정) | 비차단 | 3.1(히스·동역학 축) / 4.8 | `HANDOVER_v1.0.22.md` L119-L120 |
| **P-5** | sethuraman_stresspot2010 쪽 번호 · L5 charge-order ΔS 0.47/1.49 재소싱(reynier2004 x=½·5/6 vs 본문 x=⅔) | v1.0.22 | 후속 근거 미발견 | 비차단 | 2.4 | `HANDOVER_v1.0.22.md` L121-L122 |
| **P-6** | P4 Fisher 정보기하(Tier2) · Legendre-Fenchel 명명노트(Tier3) | v1.0.23 | **보류**(확정, D3) | 비차단 | 3.1(기각군·보류군 승계) | `HANDOVER_v23.md` L34 · `plans\...v1023...md` L142-L143 |
| **P-7** | 양 버전 샘플 이미지 QA(연속·매끄러움·미분가능성) | v1.0.23 | "진행 예정" 이후 근거 미발견 | 비차단 | 6.1 실행 기반 검증 렌즈 | `HANDOVER_v23.md` L33 |
| **P-8** | 완성도 검증 계획 V2~V5(GITT×T 폭 T-스케일 · 율 ∝\|I\| · 휴면 판정 · L_V(T) Arrhenius · M-제거 증명 · 식별성) | 2026-07-18 계획 | 집행 근거 미발견(추정: reflect 계획으로 대체) | 비차단 | 1.4 등록부 시드 추가 후보 | `plans\2026-07-18-v1024-completeness-validation-plan.md` L61-L65 · DQ-3 |
| **P-9** | anodefit 캠페인 B 전셀·C T/I/V·E 상태추론 | 2026-07-18 계획 | **미착수**(확정) — B·E 는 사용자 스코프 제외 | brief §6 Non-goal | — | `plans\2026-07-18-anodefit-MASTER-plan.md` L54-L73 · `...completeness...md` L184 |
| **P-10** | IMPROVEMENT #4 정칙용액 자유에너지(R²≈0.96 천장의 해법, Ch2–3 열역학 과제) | v1.0.24 | **park**(확정) | 비차단 | 3.1 핵심 후보 | `HANDOVER_v24.md` L62 |
| **P-11** | tab:staging ΔS(+15/−14) 초기값 피팅 갱신 | v1.0.24 | 표 미편집(확정) | 비차단 | 4.6 | `HANDOVER_v24.md` L57 |
| **P-12** | voice 복원 옵션 3(§1.1.4 교차지도 문장 · appE/sec01_map 투명 voice · fluctuation 혼합 register) | v1.0.24.1 | 사용자 판단 미집행(확정) | 사용자 결정 | 2.5 / 3.7 | `VERSION_COMPARISON_v19_v23_v24.md` L64-L72 |
| **P-13** | 항법 3종 중 식 의존성 지도·독자 경로 안내·로드맵 표 | v1.0.21→22 | 사용자 결정으로 **폐기**(확정) — 재개방은 사용자 결정 | — | 3.3(구조 재편 시 재검토 후보) | `plans\2026-07-17-v1022-master-plan.md` L24 |
| **P-14** | `CODE_GUIDE_v24`(regsol 경로 서술 잔존) · `FITTING_GUIDE`(alpha·SI 미반영) 미갱신 | v1.0.25 | **미갱신**(확정) | 비차단 | 코드 동기 별도 플랜(DR-4) | `INDEX_v25.md` L94·L96 |
| **P-15** | `MERGE_READINESS_v25.md` X1~X14 미해결 통합 표 | v1.0.25 | 미정독 | — | 1.1 인벤토리 | `INDEX_v25.md` L67 |
| **P-16** | v1.0.22 다음 버전 후보(블렌드 발열·구간별 host 전환·반응전류 배분[ai_composite2022, GS-2 동역학 층]·moyassari G2 강화) | v1.0.22 | 후속 근거 미발견 | 비차단 | 3.1 동역학 축 | `HANDOVER_v1.0.22.md` L137-L143 |

---

## 5. Decision Queue

골격·결정을 바꾸지 않고, master 가 통합 시 판단할 사항만 근거와 함께 적는다.

- **DQ-1 (원천 간 모순 · 실물 확인)** N11 G-금지 게이트: `docs\v1.0.25.1\results\INDEX_v25.md` L23 은 `test_gates_v1025.py` 를 "8종·ALL PASS(8/8)·G-금지 미구현" 으로, `V1025_1_TOUCHUP_NOTE.md` L19 는 "v1025 9/9(G-금지 포함)" 으로 적는다. 코드 byte-identical 주장(L43·L48)은 `Anode_Fit_v1.0.24.py` 에 대한 것이고 게이트 파일은 별도이므로, v1.0.25 마스터가 서브의 INDEX 작성 이후 G-금지를 추가했을 가능성이 있다(추정). 작업 챕터 2.1 에서 실물 게이트 수를 세어 등록부를 확정하기 바란다.
- **DQ-2 (brief 원천 불일치)** brief §4.3 "v1.0.26 A/B(regsol 재검증 조사, 실행 차단·미완)" 과 §4.1 커밋 4069cb3 "두 버전 산출" 은 서로 다른 시점을 가리킨다. 실물(`results\comp_v26_data\README.md`·`out_versions\build.log`·`docs\v1.0.26A-regsol\`·`docs\v1.0.26B-gallery\`)은 실행이 완료돼 A/B 결과 문서까지 생성됐음을 보여준다. "미완" 의 실질은 **평형 데이터 재검 미실행 + 사용자 결정 미기록**이다. 마스터 플랜 Current Ground Truth 의 문구를 "실행 차단" 에서 "A/B 결과 산출·평형 재검 미실행·결정 대기" 로 고치는 것을 권고한다. 또한 brief 가 배정한 `HANDOVER_regsol_investigation.md` 는 README 가 "착수 시점 인계문서" 로 규정한 stale 문서이므로, 작업 챕터 1.1 인벤토리에 `docs\v1.0.26A-regsol\README.md`·`docs\v1.0.26B-gallery\README.md`·`results\comp_v26_data\README.md` 를 정독 대상으로 추가하기 바란다.
- **DQ-3 (집행 여부 미확인)** `plans\2026-07-18-v1024-completeness-validation-plan.md` 의 V0~V6(회사 표준 조건 매트릭스·M-제거 증명·휴면 판정·L_V Arrhenius·식별성)은 배정 원천 안에 Result·ledger 기록이 없다. `plans\2026-07-22-v1024-feedback-revision-plan.md` L30 이 직전 계획서를 `plans\2026-07-19-v1024-si-2L-codex-reflection-plan.md`(미정독)로 지목하므로 V-계획은 하루 뒤 reflect 계획으로 대체된 것으로 추정된다. brief §4.5 의 방향성 유실 시드에는 "M-제거 증명(V4)·휴면 판정(V3)" 이 없으므로 작업 챕터 1.4 등록부 시드에 추가하고, 1.1 에서 2026-07-19 reflect 계획과 `V1024_REFLECT_EXECUTION_LEDGER.md` 를 정독해 확정하기 바란다.
- **DQ-4 (계보 표현)** brief §4.3 의 "v1.0.24(공개데이터 검증 캠페인·@3 regsol/@5 stage-2L·…)" 은 V-계획의 "검증 캠페인" 이 집행된 것처럼 읽힐 수 있다. 원천 기준으로 v1.0.24 는 reflect(@3/@5/토글) 캠페인 + 사후 SINTEF 단일 프로토콜 피팅·doc↔code 감사이며, 회사 조건 매트릭스 검증은 없다. 표현 조정 후보.
- **DQ-5 (물리 판정 상충 · 2.6 입력)** 두-상 커널을 둘러싼 판정이 버전마다 조건이 달라 상충한다 — v1.0.24 @3 채택(Si 0.9944) → v1.0.25 @3 역전(−0.53 %p, 전이 승격 조건) → v1.0.26 HANDOVER "@3 Si Frumkin +0.67 %p 유일 실효(별개 ablation, 블렌드 p-OCV)" → v1.0.26 A/B "regsol-4 는 gallery-7 대체 불가(ΔBIC +844.5), 흑연 Ω≈2RT 는 참, skew-logistic-7 최선(BIC 991.5)". 작업 챕터 2.6 의 정식화는 이 네 판정의 조건(전이 수·프로토콜·소재·지표)을 표로 분리해야 한다. 또한 v1.0.26 이 "정칙용액 + Maxwell 공존 닫힌형" 커널을 조사 코드(`regsol_kernel.py`)로 이미 구현했으므로, brief B2/B3 의 "정칙용액 자유에너지 = 근본 해법" 후보 평가(3.1)에 이 실측 결과가 선행 데이터로 들어가야 한다.
- **DQ-6 (verbatim 정본)** v1.0.20 의 확장 분리 지시가 `docs\v1.0.20\HANDOVER_v1.0.20.md` L17-L18("확장 전건은 v1.0.21로 분리 — 원본(v1.0.20)을 살린다." / "v1.0.20 마무리 잘 짓고 v1.0.21로 이어가자.")과 `plans\2026-07-16-v1021-master-plan.md` L3("확장 관련 내용은 21 버전으로 — 원본(v1.0.20) 보존" / "20버전 마무리 잘 지어주고 21에서 이어가자")에 서로 다른 표기로 남아 있다. 어느 쪽이 원 발화인지 배정 원천만으로는 가릴 수 없어 등록부는 병기했다. 작업 챕터 1.3 유효 결정 등록부에서 정본을 정하기 바란다.
- **DQ-7 (verbatim 승격 불가 항목)** `HANDOVER_v25.md` L37-L49 의 사용자 지시 11건은 서브세션이 "전달된 범위에서 재구성" 한 요지이며, 지시 6(세 물리 질문)은 "전문 미전달·원문 확인은 마스터 소관", 지시 10(모델 배분)은 "요지 인용" 으로 표시돼 있다. 등록부는 이들을 verbatim 으로 올리지 않았다. 1.3 에서 master 가 원 발화를 보유하고 있으면 승격, 아니면 요지로 확정하기 바란다.
- **DQ-8 (regsol 결정의 재개방 신호)** v1.0.25 DG-1 "regsol 삭제" 는 확정 결정이지만, v1.0.26 사용자 발화 "두상으로 분리되는 걸 표현하려면 regsol이 들어가야 한다." 와 "이미지로 확인하고 나서 정할려니까" 는 그 결정의 재개방을 사용자 자신이 열어 둔 것이다. brief §4.4 "Ω 물리 전량 유효(regsol 은 dQ/dV 커널만 삭제)" 는 그대로 유효하되, DR-1 대안 해석(v1.0.26 A/B)과 3.7 DG-B(채택 이론 목록)에 이 결정 대기 상태를 명시적으로 연결하기 바란다.
- **DQ-9 (버전 명칭 이력)** FB 리비전 계획 D1 은 "v1.0.24 in-place(신 버전번호 X)" 였으나 결과물은 `docs\v1.0.24.1\` 폴더로 실체화됐고 v1.0.25.1 이 이를 선례로 인용한다. 계보 표기에서 "v1.0.24.1 = FB 리비전 결과 폴더(코드 sha256 f230f59b 불변)" 로 통일하는 것을 권고한다.
- **DQ-10 (코드 문서 정합)** `CODE_GUIDE_v24`·`FITTING_GUIDE` 미갱신(P-14)은 코드 동기 Non-goal(DR-4) 소관이지만, 문건 부록 B 코드맵과 이 가이드가 어긋난 채 남아 있으므로 2.1 자산 지도의 "코드 문서 정합" 확인 항목으로 넣을지 판단 필요.
- **DQ-11 (인벤토리 후보)** git untracked 의 `Claude\results\regsol_test\`(v1.0.26 README 가 폐기 판정)·`Claude\results\process\C3_graph_check\`·`C3_pdf_render\`·`docs\v1.0.17\`·`v1.0.18.x\` 의 `sample_test_*.png`/`graph_suite_*.png` 는 v1.0.23 P-7 샘플 이미지 QA 와 관련이 있을 수 있다(추정). 1.1 인벤토리에서 지위(유효/폐기)를 확정하기 바란다.
- **DQ-12 (자산 카운트 미검증)** brief §4.2 의 v1.0.25.1 자산 카운트(display 230·boxed 64·label 429·bibitem 95·cite 265/93 등)는 master 실측이며 배정 원천에는 없다. 원천이 주는 값은 v1.0.25 baseline(ch1 라벨 263·ref 1064·cite 138/bib 44 / ch2 82·355·77/15 / ch3 44·190·86/36 / 부록 30·41, `plans\...v1025...md` L191)과 boxed 39(v1.0.25.1 note L49)다. "boxed 64" 와 "boxed 39" 는 집계 범위(본문 39 vs 부록·기타 포함 64)가 다른 것으로 보이나(추정) 2.1 에서 한 기준으로 재계수해 등록부에 확정하기 바란다.

---

## 6. Read Coverage (파일·행 범위 전건)

배정 원천 18건 + brief 는 Read 도구로 head→tail 전 영역을 한 번에 읽었다(행 번호 = Read 도구 표시 기준). 추가 6건은 v1.0.26 실물 상태 확인 목적으로 전문을 읽었다.

| # | 파일 | 읽은 행 범위 | 비고 |
|---|---|---|---|
| 0 | `results\handoffs\2026-09-02-v2-master-plan\brief.md` | L1–L219 | 지시·골격 |
| 1 | `docs\v1.0.20\HANDOVER_v1.0.20.md` | L1–L75 | 전문 |
| 2 | `docs\v1.0.21\HANDOVER_v1.0.21.md` | L1–L25 | 전문 |
| 3 | `docs\v1.0.22\results\HANDOVER_v1.0.22.md` | L1–L147 | 전문 |
| 4 | `docs\v1.0.23\results\HANDOVER_v23.md` | L1–L44 | 전문 |
| 5 | `docs\v1.0.25.1\results\HANDOVER_v24.md` | L1–L89 | 전문(v1.0.24 인계 + FB 리비전 절) |
| 6 | `docs\v1.0.25.1\results\HANDOVER_v25.md` | L1–L171 | 전문 |
| 7 | `docs\v1.0.25.1\results\V1025_1_TOUCHUP_NOTE.md` | L1–L62 | 전문 |
| 8 | `docs\v1.0.25.1\results\INDEX_v25.md` | L1–L139 | 전문 |
| 9 | `results\comp_v26_data\HANDOVER_regsol_investigation.md` | L1–L56 | 전문(README 가 stale 로 규정) |
| 10 | `results\comp_v24\VERSION_COMPARISON_v19_v23_v24.md` | L1–L80 | 전문(L80 에 `</content>` 잔존 문자열) |
| 11 | `results\comp_v24\USER_FEEDBACK_v1024_READING.md` | L1–L207 | 전문 |
| 12 | `plans\2026-07-16-v1021-master-plan.md` | L1–L77 | 전문 |
| 13 | `plans\2026-07-17-v1022-master-plan.md` | L1–L100 | 전문 |
| 14 | `plans\2026-07-18-v1023-ratio-and-advanced-methods-plan.md` | L1–L226 | 전문 |
| 15 | `plans\2026-07-18-anodefit-MASTER-plan.md` | L1–L129 | 전문 |
| 16 | `plans\2026-07-18-v1024-completeness-validation-plan.md` | L1–L199 | 전문 |
| 17 | `plans\2026-07-22-v1024-feedback-revision-plan.md` | L1–L227 | 전문 |
| 18 | `plans\2026-07-26-v1025-surgical-skew-consistency-plan.md` | L1–L241 | 전문 |
| +1 | `results\comp_v26_data\README.md` | L1–L50 | 추가(실물 확인) |
| +2 | `results\comp_v26_data\out_skew\summary_skew.json` | L1–L4 | 추가(빈 JSON 확인) |
| +3 | `results\comp_v26_data\skew_log.txt` | L1–L12 | 추가 |
| +4 | `results\comp_v26_data\out_versions\build.log` | L1–L36 | 추가(A/B 수치 원천) |
| +5 | `docs\v1.0.26A-regsol\README.md` | L1–L199 | 추가(결과 문서) |
| +6 | `docs\v1.0.26B-gallery\README.md` | L1–L193 | 추가(결과 문서) |

폴더 목록만 확인(내용 미정독): `results\comp_v26_data\` 하위 전건(파일명·크기·시각) · `results\handoffs\2026-09-02-v2-master-plan\` 하위(`iter_1\plan_draft.md`·`work_log.md`·`audit_checklist.md` 는 열지 않음).

미정독(참조만 — 본 등록부의 확정 근거로 쓰지 않음): `plans\2026-07-19-v1024-si-2L-codex-reflection-plan.md` · `V1024_REFLECT_EXECUTION_LEDGER.md` · `V1024_FEEDBACK_EXECUTION_LEDGER.md` · `PHASE_FB*_RESULT.md` · `MERGE_READINESS_v25.md` · `V1025_CHANGE_LEDGER.md` · `V1025_DATA_ADDENDUM.md` · `V1025_DOC_EDIT_REPORT.md` · `V1025_T13_T14_REPORT.md` · `V1025_DOC_CASCADE_TODO.md` · `ARCHIVE_NOTE.md` · `MULTI_DATASET_REVIEW.md` · `comp_v24\`(FIT_CHECK·DATA_REGISTRY·ABLATION_ANODE·GRAPHITE_STAGING_XRD·AUDIT_v1024_DOC_CODE·IMPROVEMENT_DIRECTIONS·LIT_ADVANCE_SYNTHESIS·HIST_*) · `docs\v1.0.22\results\`(V1022_EXECUTION_LEDGER·CHANGE_LOG·AUDIT_LINEAGE·comp_FR·comp_SM2·MERGE_READINESS) · `docs\v1.0.23\results\PHASE_P*_RESULT.md`·`comp_v23\` · `docs\v1.0.20\results\`(FIGS_PICK_JUDGMENT·DIRECTION_*·TRIAGE_P7·V1020_STYLE_RUBRIC) · `docs\v1.0.15\CLOSING_v1.0.15.md` · `V1013_TERMS_POLICY.md` · `V1014_TONE_AUDIT.md` · 문건 tex 전건 · 코드 `.py` 전건. `Codex\` 는 접근하지 않았다.
