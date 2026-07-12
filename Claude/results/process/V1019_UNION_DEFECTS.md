# V1.0.19 — 10종 검수 UNION 결함 목록 (이전본 v1.0.18.2 vs 신본 v1.0.19, master 삼각검증·직접판정)

> P3 산출. 10창(W1~W9 콘텐츠+regression 비교 / W10 Fable 전체 물리 적대검산) → master union·중복제거·삼각검증. P4에서 Fable(작성 세션 이어서)이 수정.

## ★ 종합 판정 (2대 무결 확인)
- **물리·화학·수학 골격 오류 = 0.** W7(Opus)·W10(Fable) 독립 재유도 + 전 창 재검산: CENTRAL 12종·비자명 유도 11종·부호검산 S1-S8·R1-R6·수치(U(298)=0.08529·gap 54.76mV·게이트골 −45.68·metal 1.106 k_B/atom·N_A~10²³·eV 3.9×10³⁷) 전부 재현. 일부 **강화**(A-094 Taylor 두 급수 명시·N_A 누락 경고 신설·Kirchhoff 라벨 부여).
- **regression(자산 유실) = 0.** 336 자산 전건, 9개 콘텐츠 창 전부 "verbatim 보존 또는 강화" 확인.
- **결함 = 전부 (1)구조 재배치 부작용 (2)doc↔code 정정 (3)이전본 계승** — 물리 골격 무관. 총 24항목(HIGH 3·MED 8·LOW-MED 3·LOW 9·NOTE 1).

## master 직접 검증(코드 대조 완료 = CONFIRMED)
- U-8: 코드 `ksi_lag`(L578)·`occ_lagged` 0회 → 표 오기 CONFIRMED.
- U-9: 코드 `func_L_q`가 raw(정규화 Q_cell=1, c-rate 숫자 그대로) 규약으로 §10 수치 재현 CONFIRMED(결론 L_V≪w 불변).
- U-10: `LCO_MSMR_LIT` T1 `dS_rxn:+6.0`(L739)→dS_eff=−39.7<0 CONFIRMED.
- U-11: `T_rep=np.mean(T_prog)`(L525) 전 구간 단일평균 CONFIRMED.
- U-12: 시연 순서 3.930>3.880<4.050(전이 정체 표와 상이) CONFIRMED.

---

## Cluster 1 — 구조 재배치 전환·recap (HIGH)
- **[U-1] HIGH** `ch1_sec01_n0n1.tex` L153-156 (W1-1): §1.2 말미 "Part 0가 바로 다음" 전환문이 실제론 §1.3(분극)·§1.4가 먼저 오고 L202에 동취지 전환문 중복. **N0+N1 통합 부작용.** → L153-155 전환문 삭제 또는 "분극(N1)까지 마친 뒤 Part 0가…"로 §1.3/1.4 경유 명시(L202 전환문과 하나로 통합).
- **[U-2] HIGH** `ch1_sec07_broadening.tex` L296-297 ↔ `ch1_sec08_lag.tex` L4-8 (W5-1): §7 마무리 + §8 도입이 "§lag=세 출처 ①의 답"을 파일 경계 두고 두 번, §8이 ①②③ 재나열 → recap 비계 규범 위반. → **§8 도입의 ①②③ 재나열 제거**, "\S\ref{sec:broadening}의 ①(식 eq:ensavg)에 대한 답으로 이 절이 L_V를 세운다" 한 줄 inline 참조로 축약(§7 마무리는 유지).

## Cluster 2 — swap/재배치 방향 문구 (MEDIUM)
- **[U-3] MED** `ch1_sec05_width.tex` L207 (W3-1): fig:logistic 도입문 "다음 절이 이 종이 평형 peak임을 닫는다" — 재배치 후 "다음 절"=§5.3(dist)는 peak 안 닫음(§6에서 닫힘). → "다음 절이" → "\S\ref{sec:eqpeak}(§6)이".
- **[U-4] MED** `ch1_sec05_width.tex` L150-164 (W3-2): §5.2가 선행 (a)(b)(c) 없이 "(d) 박스" 고립(§5 유도선행 재배치로 (a)(b)(c)는 §5.1로 이동, (d) 라벨만 잔존). → (d) 태그 제거해 무라벨 "박스 — 폭 다중도·방향 부호 일반화"로 통일(또는 §5.2 도입부에 (a)(b)(c) 신설).
- **[U-5] MED** `ch1_sec15_lcoelec.tex` L73-74 (W7-1): §14→§15 swap 후에도 §15가 "Gn=일련번호"를 1차 재선언 — §14 L86이 이제 1차 선언. → §15는 "갭 G2(\S\ref{sec:lco-decomp}에서 정의)" back-ref로 격하. Gn 1차 선언은 §14 단일.
- **[U-6] MED** `ch1_sec14_lcodecomp.tex` L76-80 (electronic 불릿) ↔ L5 도입 (W7-2): §14 도입은 "전자항이 무엇인가는 §15의 몫"이라 선언했는데 electronic 불릿이 §15 정량치(≈1.1 k_B/atom·Reynier 0.18)를 미리 단정(forward-leak·중복). → 불릿의 "1.1/0.18" 절을 §15로 미루고(또는 "정량은 §15") 불릿은 부호<0·∝T·흑연 0 역할만. (또는 도입 L5를 "정량·닫힌식은 §15"로 완화.)

## Cluster 3 — N3′ 노드 일관성 (MEDIUM, 동일 뿌리)
- **[U-7] MED** `ch1_sec13_lcohys.tex` L2/L4 title + `ch1_sec18_inputs.tex` tab:nodemap + `ch1_appB_codemap.tex` tab:nodecode (W6-1+W9-2): §13(N3′=LCO 히스, §4 N3 대응)이 제목에 N3′ 미노출·두 표에 N3′ 행 누락(§12 N2′·§14 N9′·§15 N5+는 태그·행 있음). → §13 `\section` 제목에 "(N3′)" 추가 + 두 표에 `N3′ | ΔU_hys^cat,U_j^d,cat | eq:lco-dUhys, eq:lco-Ubranch` 행 추가. §11도 `\section` 제목에 "(N0′)" 노출해 §12와 통일.

## Cluster 4 — doc↔code 정정 (코드=18.2 고정, doc 수정)
- **[U-8] HIGH** `ch1_appB_codemap.tex` tab:symcode ξ_lag 행 + tab:nodecode N8 행 (W9-1, CONFIRMED): 식별자 `occ_lagged`가 코드에 없음(실제 `ksi_lag`, L578-579). v1.0.18.2 계승 미포착 오류. → 두 표 `occ_lagged`→`ksi_lag` 정정.
- **[U-9] MED** `ch1_sec10_sum.tex` L50-55(및 `ch1_sec08_lag.tex` eq:Lqfull T* 정의) (W10-1, CONFIRMED): §10 L_V 규모(10⁻¹⁰–10⁻⁸V)·"가시꼬리 ΔH_a≈80kJ/mol"은 코드 raw 규약(정규화 Q_cell=1, c-rate 숫자 그대로)에서만 재현. §1/부록B SI 지침대로면 3600배 작음. **결론(L_V≪w→초기=평형종) 불변.** → T* 정의 옆 또는 §10 수치 문장에 한 줄: "본 수치는 |I|/Q_cell를 s⁻¹ 수치로 대입한 값(코드 규약: 정규화 Q_cell=1에서 c-rate 숫자 그대로); [1/h] 수치를 SI 환산하면 ~3600배 작아진다(결론 불변)."
- **[U-10] LOW** `ch1_sec12_lcocenter.tex` verifybox "★부호 공존" (W10-2, CONFIRMED): "창 중심 −46이 +80 기저에 더해져도 총부호 불변(+34>0)"이 코드 시연(T1 dS_rxn=+6→dS_eff−39.7<0)과 반대. +80은 대표스케일(tier B, x-의존)이라 창 중심 기저가 작으면 부호 뒤집힘. → "총 부호는 불변"을 조건부로: "기저가 대표스케일(+80)이면 +34로 양이나, 기저는 x-의존이라 창 중심 기저가 작으면(예 시연 +6) 총부호가 음이 될 수 있다 — 부호 판정 자체가 round-trip 피팅 대상" 한 문장 추가.
- **[U-11] LOW** `ch1_sec01_n0n1.tex` tab:notation T_rep 행 (W10-4, CONFIRMED): "전이당 대표(평균) 온도"가 코드 `np.mean(T_prog)` 전 구간 단일평균과 어긋나는 오독 소지. → "전이당 상수 평가에 공통으로 쓰는 전 구간 평균 T̄(전이 창별 평균 아님)"으로 명확화.
- **[U-12] LOW** `ch1_appB_codemap.tex` L14-15 "대응" + §11 표 캡션 (W10-3, CONFIRMED): 시연 리스트 전이 정체·순서(3.930>OD 3.880<곁가지 4.050)가 tab:lco-staging(T1 3.90<T2 4.05<T3 4.17)과 상이 → "대응" 과서술. → "(시연 리스트는 전이 구성·순서가 표의 물리 anchor와 다른 tier-C 데모 — 파라미터 *구조*의 대응이지 전이별 1:1 값 대응 아님)" 병기.

## Cluster 5 — cross-ref 정밀도 (LOW-MED / LOW)
- **[U-13] LOW-MED** `ch1_sec11_lcointro.tex` L111-114 (W6-2): "위 '셀 방전=LCO 리튬화'…" 모호 지시어 → `\S\ref{sec:lco-map}` 복원(같은 파일 타 참조는 업그레이드됐는데 이 자리만 다운그레이드).
- **[U-14] LOW-MED** `ch1_sec13_lcohys.tex` L34 (W6-3): "아래 도핑 문단"이 이제 subsection 경계 넘음 → `\S\ref{sec:lco-hys-dope}`(라벨 존재·타 파일서 검증됨).
- **[U-15] LOW-MED** `ch1_sec05_width.tex` §5.2 ↔ `ch1_sec07_broadening.tex` §7.1 (W9-3): 흑연 4전이 solid-solution/two-phase 분류를 두 곳이 거의 중복 서술 + 인식론 층위 불일치(§5.2 "피팅 후 기대" 헤지 vs §7.1 확정). §5.2는 "지위만 세운다" 위임 선언과 실제 내용 어긋남. → §5.2의 전이 실명 나열 축소·"구체 분류는 §7.1"로 위임(또는 §7.1에도 "피팅 후 기대" 헤지 명시해 층위 통일).
- **[U-16] LOW** `ch1_sec07_broadening.tex` L118 (W4-1): "(ii)" dangling forward-ref("(c)-" 접두 탈락) → `\S\ref{sec:broadening-scope}의 (ii)`.
- **[U-17] LOW** `ch1_sec07_broadening.tex` L254 keybox (W4-2): "본문 (i)" → `본문 \S\ref{sec:broadening-scope}(i)`.
- **[U-18] LOW** `ch1_sec17_msmr.tex` L38 (W8-1): "(\S\ref{sec:lco-peak})" 뒤 "(b)" pinpoint 복원(종 항등식 도출부 특정).
- **[U-19] LOW** `ch1_sec15_lcoelec.tex` eq:lco-U1V 앞참조 (W9-4): signpost 없는 §17 식 인용 → "§lco-code에서 같은 구조로 재도출" signpost 추가 또는 제거(boxed eq:U1T2 자기완결).
- **[U-20] LOW** `ch1_sec14_lcodecomp.tex` L48/L54(S_e gloss), L52-55(슬롯 prose recap), `ch1_sec15_lcoelec.tex` L5/L6-7(도입 중복) (W7-3/4/5): §14 S_e 최초 등장에 한 어절 gloss("자리당 전자 엔트로피 S_e — 닫힌식 §15"), 슬롯 규칙 prose는 eq:lco-slots 참조로 축약, §15 도입 L5/L6-7 한 문장화.

## Cluster 6 — 이전본 계승 (재작성 기회, 선택적)
- **[U-21] MED** `ch1_sec02b_part0.tex` L14/L37/L45-46, `ch1_sec03_center.tex` L17/L39/L58-59 (W2-1): 괄호 보충 전보체 6곳(문체 규범 위반) — §sm-mf/electro/macro/center가 verbatim 재사용돼 미적용. → 각 괄호의 완결 명제를 본문 문장으로 풀어쓰기(물리·식 무변경, 산문만).
- **[U-22] LOW** `ch1_sec09_tail.tex` fig:reversal 주석 L207/223 (W5-2+W10-5): 노드 주석 "1.00w" vs 캡션 "1.01w" — 재계산 1.012w이므로 캡션 옳음. → 주석 1.00w→1.01w.
- **[U-23] LOW** `ch1_sec00_intro.tex` L14-19 (W1-3): 서론 "본론(N1--N9)…전이별" 서술이 fig:spine(N0·N1=loop 밖 1회)과 어긋남(이전본 계승). → "노드 N0·N1(1회 실행)에서 출발해 전이 루프 N2--N9로". + (W1-2) s/σ_d 표 행 축약("본문 §1.1 참조").

## Cluster 7 — 구조 판단 (NOTE, Fable 판단 위임)
- **[U-24] NOTE** `ch1_sec07_broadening.tex` 제목 "(N6 보강)" (W4-4): broadening \section 승격으로 N6가 두 절(eqpeak+broadening)에 걸침 → "\section=N단계 1:1"·fig:spine 정합 약화. → 제목·목차에서 broadening을 "N6 확장 절"로 표기하거나 N6a/N6b 서브라벨 검토(물리 무관, 표기 판단).

## 비결함(확인) — 수정 불요
- W9-5: §14→§15·§11→§17 예고는 의도적 signpost·후속과 정합 → **정상**.
- W9-9: 전 라벨 무결(중복0·미정의0·미참조 fig/tab 0), orphan은 정상 하위섹션/유도중간식 패턴.
- W2-2: §3 신규 라벨 sec:center-eqcond/Uj 미참조 — 무해(향후 §hys 역참조용). 선택: prune 또는 §hys 도입부서 배선.
