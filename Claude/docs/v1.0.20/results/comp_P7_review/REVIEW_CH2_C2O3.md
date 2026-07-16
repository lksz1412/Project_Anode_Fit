# REVIEW_CH2_C2O3 — 독립 검수 (v1.0.20 Chapter 2 + appendix_phase_separation)

- 검수자: C2O3 (독립 창, 타 REVIEW 파일 미열람)
- 대상 신본: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.20/_sections/ch2_*.tex` + `appendix_phase_separation.tex`
- 대조 구본(read-only): `/home/user/Project_Anode_Fit/Claude/docs/v1.0.19/`
- 검수 3축: ① 신본 자체 결함 · ② v1.0.19 대비 regression · ③ 신설 다리 물리·서지 정확성
- 심각도: H=물리·수식 오류/오귀속 · M=유도 비약·정합 결손·regression · L=표기·문장·일관성
- 판정 렌즈: G-follow · G-usable · G-derive + refute 시도 + '가장 약한 1곳' + 빈 통과 금지

---

## 발견 목록

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| C2O3-01 | ch2_preamble.tex:35 | —(PASS) | ② | `\newtheorem*{bgbox}{배경}` 1줄 추가 외 diff = 버전 스탬프(2,3,27,29행)뿐. bgbox 는 B-003 등재 변경과 정합. regression 없음 | v1.0.19 대비 diff 전수 대조 | 무 |
| C2O3-02 | ch2_sec03:17-21 (B-005) | —(PASS·강) | ③ | B-005 중간식 인라인 전 단계 손 재유도 검산 통과. $f_k=k_BT\ln(1-e^{-\beta\hbar\omega})$→$S=-\partial f/\partial T=-k_B\ln(1-e^{-\beta\hbar\omega})+k_B\beta\hbar\omega\,n$(중간식 line19 일치); 항등식 ①$1-e^{-\beta\hbar\omega}=1/(1+n)$·②$\beta\hbar\omega=\ln[(1+n)/n]$ 각각 $n=1/(e^{x}-1)$에서 검증; 대입 시 $k_B[(1+n)\ln(1+n)-n\ln n]$=eq:Svib_mode(line23) 일치 | 독립 재유도(위 본문) | 무 |

### ch2_preamble.tex (전문 정독 완료, 53행)
### ch2_sec00_intro.tex (전문 정독 완료, 69행) — 무변경(구본 동일). $\dot Q_\rev=-IT\,\partial U_\oc/\partial T=-(IT/F)\Delta S(x)$ 차원([W]) 정합, $\partial U_\oc/\partial T=\Delta S/F$ 내부 일관.
### ch2_sec01_partition.tex (전문 정독 완료, 145행) — 무변경. Ξ₁ 통일 표기·ε̃ 정의·s=+1 각주 Ch1 정합.
### ch2_sec03_vibel.tex (전문 정독 완료, 102행) — B-005 검산 통과. 배경 다리(L9) = Ch1 §2 bgbox 제목 문자 일치.
### ch2_sec04_einstein.tex (전문 정독 완료, 116행) — 무변경. eq:Svib-einstein 중간식 항등식·고온/저온 극한 재검산 통과. u_j 각주 정합.

| C2O3-03 | ch2_sec02:9 (U10) | —(PASS) | ③ | U10 `(\S\ref{ssec:litverif})` 병기. 라벨 `ssec:litverif` 는 동일 파일 L132 `\subsection{...}\label{ssec:litverif}` 로 실재. 인용 실체(reynier2003·allart2018)가 그 소절에 존재 | sec02 L132 대조 | 무 |
| C2O3-04 | ch2_sec05:169 (U9) | —(PASS) | ③ | U9 `\cite{dahn1991,ohzuku1993}` 서지-주장 정합. dahn1991="Phase diagram of Li_xC6"(staging 상도표)·ohzuku1993="Formation of Li-Graphite Intercalation Compounds"(staging 형성) 둘 다 "실측 plateau·staging 문헌 상평형" 주장 뒷받침 | 원장/bib 서지 대조 | 무 |
| C2O3-05 | ch2_sec08 tab:worked·(c)·(e) | —(PASS·강) | ① | 가중평균 산술 −0.204/단순 −0.134/config −0.070, ΔS=−19.7, Q̇/I=+60.8 mV 전부 직접 재계산 일치. tab:qrev 5행 내부 정합 | 위 재계산 | 무 |
| C2O3-06 | 교차정합: Ch2→Ch1 §N 리터럴 11종 | —(PASS) | 특별축 | §1·2·3·4·5·7·8·13·14·15·17 리터럴 참조 전건이 Ch1 toc 절 제목·내용과 일치(서론 무번호→§N=sec0N 매핑). eq:Se(Ch1)/eq:Se-ch2(Ch2) 별개·u_j 동명 별개 각주·ε̃·Ξ₁ 문자 일치 | Ch1 toc + sec02a 대조 | 무 |

### ch2_sec02_config.tex (전문 정독 완료, 189행) — U10 병기 외 무변경. eq:Sconfig·eq:dSconfig·eq:dVdT_config 부호 3분기 정합. §14 삼분해 참조 정합.
### ch2_sec05_mixing.tex (전문 정독 완료, 241행) — U9 인용 외 무변경. 파생 A~D 유도 정합. g_j 4종 충돌 가드 유효.
### ch2_sec08_synthesis.tex (전문 정독 완료, 145행) — 무변경. 수치 전건 재검산 통과.

| C2O3-07 | ch2_bib:9-10 (C-017·C-018) | —(PASS·강) | ③ | dahn1991·ohzuku1993 신규 2종이 ch1_bib(L5-6)·원장 V1과 **3자 문자 완전 동일**. ch2_bib 카운트 "16" 정확(15 외부+numverif2026). 부수 C-005/006/007(msmr_partI 023502·msmr_partII 제목 전문+103505·hysteresis2018 179--184)도 CHANGE_LOG P1 등재와 정합 | ch1_bib/ch2_bib/원장 대조 | 무 |
| C2O3-08 | ch2_sec00:8 vs ch1_sec03:52-54 | —(PASS) | 특별축 | sec00 인용 `U_j(T)=(-ΔH_{rxn,j}+TΔS_{rxn,j})/F` = Ch1 §3 eq:Uj 문자 일치, §3 제목 "평형 중심 U_j(T)"·∂U_j/∂T=ΔS/F 관계까지 교차 정합 | ch1_sec03 대조 | 무 |
| C2O3-09 | appendix:494 (C-019) | —(PASS) | ③ | [A5] "Ch.~17--18"→"Ch.~18--19" 정정 적용. 본문 [A5] 인용 2곳(L403 핵생성↔Ch.19·L439 spinodal 선형이론↔Ch.18)이 정정 귀속과 내부 정합. "Wiley" 브랜드 표기 원장 허용 | appendix L403·439·494 + 원장 D | 무 |
| C2O3-10 | appendix:44·69·104·163·210·245·352·380 (P6) | —(PASS) | ③ | 정규용액 7·격자기체 1 붙임 정정. 8건 전부 주변 문장 무훼손(복합어 간격만 변경, 나머지 행 동일) | v1.0.19 대비 diff | 무 |
| C2O3-11 | appendix 전문 (497행) | —(PASS·강) | ① | binodal(ξ_b=0.0707/0.9293·f/RT=−0.0583)·spinodal(ξ_s=0.2113/0.7887·f/RT=−0.0157)·μ_A/μ_B·핵생성 r*=2γ/|Δg_v|·ΔG*=16πγ³/3Δg_v²·Cahn-Hilliard R(k)·차원([κ]=J/m,[M]=m⁵/Js) 전부 재검산 통과. 본문 §2·§4.1·§4.2·§7 참조 Ch1 정합 | 독립 재계산 | 무 |
| C2O3-12 | ch2_sec03:27-28 | L | ①(G-follow) | (구본 계승·B-005 무관) "전 모드에 대해 합하고 1몰당 환산(R=N_A k_B)"하여 `S_vib=R∑_k[...]`로 적음. ∑_k 가 자리당 대표모드인지 몰 전체 3N_A 모드인지 표면상 모호(후자면 k_B). sec04 R-접두 단일모드형과는 내부 정합하는 표준 관용 축약 | sec03 L27-28 대 sec04 L34 | 표준 관용이라 no-action 가능; 원한다면 "자리당 대표모드 합" 1구 명시 |
| C2O3-13 | ch2_sec03:17-21 (B-005) | L | ①(G-follow) | B-005 중간식 인라인이 4개 논리단계(곱/연쇄율 귀속·중간식·항등식 2개·대입)를 단일 장문 1문장에 압축. 물리·수식은 전부 옳음(C2O3-02). CHANGE_LOG 의 "FD 측과 노출 수준 평행화" 설계 의도에는 부합하나, 절 대부분이 쓰는 (a)-(d) 박스 사슬 대비 학부생 추적 마찰이 이 창 담당분에서 가장 큼 | 형식 대조 | (선택) 항등식 2개를 별행 표시로 빼면 추적성↑ — 물리 무변경 |

### ch2_sec06_limits.tex (전문 정독 완료, 53행) — 무변경. 6코너 검산표 물리 정합, eq:Se-ch2 축퇴극한 한정 정확.
### ch2_sec07_revheat.tex (전문 정독 완료, 59행) — 무변경. eq:qrev 부호(방전 I>0·ΔS<0→발열) sec08과 정합, 방전 라벨 층위 가드 유효.
### ch2_sec09_method.tex (전문 정독 완료, 44행) — 무변경. §1(V_n)·§17(MSMR) 참조 정합, MSMR 풀네임 rubric C4 일치.
### ch2_sec10_closing.tex (전문 정독 완료, 26행) — 무변경. §7(broadening 기원) 참조 정합, 수미상관.
### ch2_appA_traps.tex (전문 정독 완료, 75행) — 무변경. u_j·eq:Se-ch2·방전 라벨 CRITICAL 가드 재수록, 신규 자산 없음.
### ch2_bib.tex (전문 정독 완료, 28행) — C-017/018/005/006/007 반영, 3자 정합.
### appendix_phase_separation.tex (전문 정독 완료, 497행) — C-019·P6 8건·버전 스탬프 갱신 외 무개정. 물리·교차참조 정합.

---

## REVIEW COMPLETE — 발견 총 13건 (H 0 / M 0 / L 2 / PASS·검증기록 11)

담당 청크 16개 Ch2 파일 + appendix_phase_separation 전문(모든 행) 정독 완료. 이 창 소관 의도된 변경(C-017·C-018·B-005·C-019·U9·U10) 및 부수 변경(P1 서지정정 C-005/006/007·P6 8건 스윕·B-003 bgbox·버전 스탬프)을 3축으로 검증한 결과:

- **① 신본 자체 결함**: H·M 없음. B-005 중간식 손 재유도(f_k→S=-∂f/∂T→중간식→BE 항등식 2개→닫힌형) 전 단계 정확. sec08 tab:worked 가중평균 산술(−0.204/−0.134/−0.070)·ΔS=−19.7·Q̇/I=+60.8 mV·tab:qrev 5행 직접 재계산 일치. appendix binodal·spinodal·Maxwell·핵생성·Cahn-Hilliard 수치·차원 전부 독립 재검산 통과. L급 2건은 물리·수식 오류가 아닌 학부생 추적성(G-follow) 마찰(C2O3-12·13).
- **② v1.0.19 대비 regression**: 없음. 전 파일 diff 대조 결과 CHANGE_LOG 등재 변경 외 의미 약화·자산 유실·문장 훼손·수치 변화 0. 무변경 파일(sec00·01·04·06·07·08·09·10·appA·appB) 구본과 의미 동일. appendix P6 8건은 복합어 붙임만 변경(주변 문장 무훼손).
- **③ 신설 다리 물리·서지 정확성**: dahn1991·ohzuku1993 3자(ch2_bib↔ch1_bib↔원장) 문자 완전 동일. U9 서지-주장 정합(staging 상평형). U10 라벨(ssec:litverif) 실재·인용 실체 정합. ch2_sec03 배경 다리 = Ch1 §2 bgbox 제목 문자 일치(분업 성립). C-019 정정 후 본문 [A5] 인용과 내부 정합.
- **특별축(교차 정합)**: Ch2→Ch1 §N 리터럴 참조 11종(§1·2·3·4·5·7·8·13·14·15·17) 전건이 Ch1 toc 절 제목·내용·기호와 일치. eq:Se(Ch1)/eq:Se-ch2(Ch2) 별개·u_j 동명 별개 각주·ε̃·Ξ₁·q(T)→ε̃ 정의 문자 일치. appendix 본문 §2·§4.1·§4.2·§7 참조 정합. ch2_appB 회귀 기준값 5항목 sec08 문자 일치.

## 가장 약한 1곳

**C2O3-13 — ch2_sec03:17-21 (B-005 중간식 인라인의 학부생 추적성)**. 이 창 담당 변경분 중 물리·수식은 전부 옳으나(독립 재유도 완전 일치, C2O3-02), 유일하게 "결함이라기보다 개선 여지"가 남는 지점. B-005 는 4개 논리단계 — (i) 곱의 규칙→로그항·연쇄율→점유항 귀속, (ii) 중간식 S=−k_B ln(1−e^{−βℏω})+k_B βℏω n_k, (iii) BE 항등식 2개, (iv) 전량 n_k 치환 — 를 **단일 장문 1문장**에 압축했다. 절 대부분이 (a)-(b)-(c)-(d) 박스 사슬(rubric B1)로 전개되는 것과 대비되어, 이 인라인 산문은 G-follow(학부생이 한 줄씩 따라가기) 마찰이 청크 내 최대다. CHANGE_LOG 의 "FD 측(eq:Se_start→eq:Se-ch2)과 노출 수준 평행화" 설계 의도에는 부합하므로 결함(H/M)은 아니나, 두 BE 항등식을 별행 표시식으로 빼면(물리 무변경) 추적성이 개선된다 — 추가 후보(실수정 아님).

(주: 이 창은 담당 16파일 + appendix 전문에서 H·M 결함을 발견하지 못했다. 의도된 변경 전건이 물리·서지·교차정합에서 정확하며, 핵심 검산 대상(B-005 재유도·tab:worked 산술·appendix 수치·3자 서지 정합)이 모두 독립 재현되었다. 이는 빈 통과가 아니라 근거 있는 검증 결과다.)
