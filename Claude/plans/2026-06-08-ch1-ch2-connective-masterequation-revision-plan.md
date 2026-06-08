# Ch1·Ch2 연결고리 + 최종 피팅식 절 단위 개정 계획

## Summary
박사님 누적 지시(6-08): 두 챕터가 "(가) 내용 부족, (나) 중간 연결고리 없음, (다) Ch1 전반부–후반부 단절, (라) 최종적으로 떨어지는 피팅식·결론 부재"라 *쓸 수 없다*. 본 계획은 두 챕터를 **절 단위 루프**(한 절 개정→그 절 검수 until clean→앞 절·Ch1 정합→다음 절, 챕터 완료까지 멈춤 없음)로 개정해, ① 각 챕터가 **단일 master 피팅식 + 파라미터 표 + 데이터→파라미터→예측 결론 박스**로 닫히게 하고, ② 절간·전후반 **연결고리를 본문 다리로** 메우고, ③ 얇은 내용을 보강하며, ④ 검토에서 확정된 표기·정합 결함(C2-1~C2-9)을 시정한다. 기존 정확한 유도(손유도 재현 완료)는 보존하고 surgical 개정만 한다. 대상: `Claude/docs/graphite_ica_ch1.tex`(953줄), `graphite_ica_ch2.tex`(391줄). Ch3(발열)·Ch4(반응속도론)는 범위 밖.

## Current Ground Truth
**확인된 사실(전문 정독·손유도 재현 완료):**
- Ch1 전문(1–953) 정독. 핵심 유도(logistic 1.11, eqcond 1.10 부호사슬, detailed balance 1.25, dξ/dV 1.13, dU/dT 1.15) **손검 정확**. 닫힌식 eq:closed·실무식 eq:simplefit·S1–S4 식별 사다리 존재.
- Ch2 전문(1–391) 정독. V_eq(ξ) 2.5, g''·spinodal 2.7, ΔU_hys 2.10 **손검 정확**. 단일문건 규율(§1 Chapter-1 언급 0, 인계/전달/결론 절 0) 준수. Ch1 인용(1.1/1.3/1.9/1.10/1.11/1.19) 전부 정확.
- 검토 결과 문건: `Claude/results/REVIEW_CH1_CH2_6LENS_section-by-section_2026-06-08.md`(커밋 9f06579). 확정 결함 9건(C2-1 MEDIUM, 나머지 MINOR/LOW), 추정 개선 5건, 누락 0.
- Ch1 전후반 단절 진단(S1~S4): §5→§6 전기화학→추상통계 급강하 / 꼬리 4토막 분절 / 물리모드→피팅모드 단절 / C2-1 길이식 어긋남.

**기존 결정:**
- 의존 트리 1→2→{3,4}(유일 권위). Ch1=방전 dQ/dV, Ch2=충방전 히스테리시스(Ch1만 기반, BV/DFN X).
- 박사님 목표 = OCV+0.1C/0.2C, 15/23/45℃로 전이별 dQ/dV 피팅 → 타 조건 예측(DFN 아님).
- 브랜치 `rb-rebuild-2026-05-30`. 직전 커밋 9f06579.

**미확인:** 최종 master 식의 파라미터 집합 세부(이상 폭 w_j=RT/F 고정 vs 자유)는 Assumptions 로 둠(non-blocking).

## Phase Range
| Phase | 이름 | Steps | 대상 절 |
|---|---|---:|---|
| 1.1 | Ch1 서론 — 최종식 도착점 thread | 1–2 | 서론 |
| 1.2 | Ch1 §3 평형 peak — forward-thread + loop-closure + 8.314× | 3–5 | §eqpeak |
| 1.3 | Ch1 §4 지연 — "단일지수=근사, 실측 stretched" 관측 동기(S2 다리) | 6–8 | §lag |
| 1.4 | Ch1 §5 배리어 — §6 다리(S1)·disclaimer prune·keff 조건 | 9–12 | §barrier |
| 1.5 | Ch1 §6 통계 — 도구막간 reframe·**C2-1 길이식 시정**(S1·S4) | 13–16 | §stattools |
| 1.6 | Ch1 §7 분포 — stretched payoff 가시화(S2) | 17–18 | §dist |
| 1.7 | Ch1 §8 종합 — 분포↔단일지수 환원 명시·메타/부록 정리 | 19–23 | §synth |
| 1.8 | Ch1 **신규 §최종 종합식·피팅·예측 결론** | 24–28 | 신규 절 |
| 1.9 | Ch1 빌드·전수정합·Codex 적대검수·커밋 | 29–31 | 전체 |
| 2.1 | Ch2 §1 기호·서론 — γ_j 정의역·최종식 thread | 32–34 | §1·서론 |
| 2.2 | Ch2 §2.1 — staging 일차성 보강(P-4) | 35–36 | §hys_bg |
| 2.3 | Ch2 §2.4↔§3 — 두 기원 중복 축약(P-3) | 37–39 | §hys_bg·§hys_decomp |
| 2.4 | Ch2 §5 — ΔU_hys 중간 로그 이중화 명시(C2-8) | 40–41 | §hys_branch |
| 2.5 | Ch2 §6 — w_j^b 근거(P-5)·bare V→V_n(C2-9) | 42–44 | §hys_dQdV |
| 2.6 | Ch2 문헌 — reynier2004 cite/제거(C2-7) | 45–46 | bib |
| 2.7 | Ch2 **신규 §최종 종합식·피팅·예측 결론** | 47–51 | 신규 절 |
| 2.8 | Ch2 빌드·Ch1 정합·Codex 적대검수·커밋 | 52–54 | 전체 |

## Non-goals
- 정확성 확인된 유도(상기 손검 목록) 재작성·재유도 금지 — 연결·결론·결함만 surgical 개정.
- **챕터 통째 배치 Write/Edit 금지**(절 단위 루프 위반). 한 절씩.
- Ch1 식별자·라벨·식 번호 임의 변경 금지(P5). 신규 식·신규 절만 add(식 번호는 말미 연번).
- Ch2 단일문건 규율 위반 금지(§1에 Chapter-1 언급, 인계/전달/결론 절 신설 X). 신규 "최종 종합식" 절은 *결론*이 아니라 본 장 물리의 *도착식*(피팅·예측 산출물)으로 작성.
- Ch2에 BV/DFN/반응속도론 도입 금지(Ch4 영역). Ch3(발열) 작성 안 함.
- `Codex/` read/write 금지. working tree의 Archive_*·zip·이전 트랙 삭제분 스테이징 금지 — 내 개정분만 명시 스테이징.

## Implementation Changes
- 수정: `Claude/docs/graphite_ica_ch1.tex`, `Claude/docs/graphite_ica_ch2.tex`(절 단위 Edit).
- 신규 절 2개: Ch1 §"종합 모델식과 피팅·예측"(§synth 뒤, §overlap 앞 또는 §falsify 앞), Ch2 §"충방전 종합 모델식과 피팅·예측"(§hys_param·§hys_fit 통합·강화 또는 그 뒤).
- 빌드 산출: `graphite_ica_ch1.pdf`, `graphite_ica_ch2.pdf`(검증용).
- Phase별 result: `Claude/results/PHASE_<id>_<topic>_RESULT.md`.
- Ledger: `Claude/results/PHASE_CM_EXECUTION_LEDGER.md`(CM=connective+masterequation, 12-col).

## Phase 1.1 — Ch1 서론: 최종식 도착점 thread
- **Steps 1–2.** 입력: ch1.tex 54–86. 산출: 서론에 "이 장은 *하나의 피팅식*에 도달하며, 그 식의 각 항을 절마다 세운다"는 도착점 명시 1–2문장(S3 목적의식 실의 시작). 기존 "실데이터 피팅에 바로" 목적을 본문 실로 승격.
- **Gate G1.1:** `grep`로 서론에 신규 thread 문장 존재 확인 + 빌드 시 문단 깨짐 0 + 기존 stagebox·목표 문장 보존(diff로 add-only 확인).
- 중단: 없음(서론 텍스트 add). 다음 phase 조건: G1.1 PASS.

## Phase 1.2 — Ch1 §3 평형 peak: forward-thread + loop-closure + 8.314×
- **Steps 3–5.** 입력: 195–368. 산출: (a) §3 keybox/소절에 "U_j·w_j·Q_j 가 최종식의 *평형(rise) 항*이 된다" forward-thread 1문장; (b) §3.2→§3.3 loop-closure 문장("logistic(1.13)을 (1.4)에 대입하면") 보강; (c) C2-5 줄350 "8.314×" 명시.
- **Gate G1.2:** 줄350에 `8.314\times258` 표기 확인(grep) + forward-thread 문장 존재 + eq 번호·라벨 불변(grep `\label{eq:` 전수 동일).
- 중단: 없음. 다음: G1.2 PASS.

## Phase 1.3 — Ch1 §4 지연: 단일지수=근사, 실측 stretched (S2 다리)
- **Steps 6–8.** 입력: 371–480. 산출: §4 말미 keybox 직전에 "단일지수 꼬리는 *단일 입자·단일 배리어 근사*이며, 실측 꼬리는 늘어진다(stretched) — 그 원인은 전극 입자의 배리어 *분포*로, §dist 에서 다룬다"는 관측 동기 1–2문장(전반부→후반부 대동맥의 출발점). forward-thread "이 꼬리 항이 최종식의 *동역학 항*".
- **Gate G1.3:** "stretched"·"\S\ref{sec:dist}" 연결 문장 존재(grep) + 기존 eq:tail·eq:Lq 보존 + 빌드 ref 해소.
- 중단: 없음. 다음: G1.3 PASS.

## Phase 1.4 — Ch1 §5 배리어: §6 다리(S1) + disclaimer prune + keff 조건
- **Steps 9–12.** 입력: 483–592. 산출: (a) §5 종료 keybox를 §6로 잇는 다리 강화 — "한 값 배리어에서 *입자 분포*로 넘어가려면 분포·평균·분산 전파 도구가 필요하다(다음 절은 그 도구 정비)"; (b) C2-4 k_0/"무근거 단정" disclaimer 적층 1곳으로 통합(rigorbox); (c) C2-2 eq:keff 유효조건 "𝒜≳RT"를 본문 수치(37%@RT,5%@3RT)와 정합하게 "수 RT(≳3RT)"로 통일.
- **Gate G1.4:** eq:keff 박스 조건 문자열이 본문 "수 RT"와 일치(grep 대조) + disclaimer 중복 라인 수 감소(before/after grep count) + §5→§6 다리 문장 존재 + 부호·식 보존.
- 중단: 없음. 다음: G1.4 PASS.

## Phase 1.5 — Ch1 §6 통계: 도구막간 reframe + C2-1 길이식 시정 (S1·S4)
- **Steps 13–16.** 입력: 595–661(+679/702 대조). 산출: (a) §6 도입을 "도구 정비 *막간*"으로 명시하고 §4의 stretched 관측과 직접 연결; (b) **C2-1 시정** — §6의 `L_q∝e^{G/RT}`를 §7/§8의 `e^{(G−χ𝒜)/RT}`와 정합화: "χ𝒜_j 는 집단 *공통*(동일 V_n)이라 ln L_q 의 *상수 오프셋*이므로 분산에 무관 — 그래서 σ_{ln L_q}=σ_G/RT"를 명시(또는 길이식을 e^{(G−χ𝒜)/RT}로 통일하고 상수항이 분산서 탈락함을 한 줄).
- **Gate G1.5:** §6 본문에 "집단 공통"·"상수 오프셋"(또는 `e^{(G-\chi\mathcal A` 통일) 문구 존재(grep) + eq:varprop 결론 σ_G/RT 불변 확인(손검) + §6↔§7 길이식 표기 모순 0(두 식 비교 기록).
- 중단: 길이식 통일이 eq:varprop·eq:jacobian에 파급되면 §7도 동일 phase서 정합(범위 내). 다음: G1.5 PASS.

## Phase 1.6 — Ch1 §7 분포: stretched payoff 가시화 (S2)
- **Steps 17–18.** 입력: 664–723. 산출: §7가 §4의 "stretched 관측"을 *해소*함을 명시("§lag 에서 예고한 늘어진 꼬리가 여기서 분포 적분으로 설명된다"). §6 도구 인용 정합 확인(C2-1 파급).
- **Gate G1.6:** §7에 §lag 관측 해소 연결 문장 존재(grep `\S\ref{sec:lag}`) + eq:superpose 보존 + §6 길이식과 정합.
- 중단: 없음. 다음: G1.6 PASS.

## Phase 1.7 — Ch1 §8 종합: 분포↔단일지수 환원 명시 + 메타·부록 정리
- **Steps 19–23.** 입력: 726–861. 산출: (a) §8.3에서 "좁은 분포 극한 → §lag 단일지수로 환원, 넓은 분포 → stretched"를 명시해 후반부(분포)의 값어치를 가시화(S2 마감); (b) C2-4 메타문장(줄297 류 잔재)·disclaimer prune; (c) C2-3 "부록" 참조 2곳(433·824) — 부록 신설 대신 본문 절차 포인터로 치환하거나 "(피팅 절에서 상술)"로 정리.
- **Gate G1.7:** "부록" 잔존 0(grep `부록`) + 분포↔단일지수 환원 문장 존재 + eq:closed·eq:simplefit·S1–S4 보존(라벨 grep).
- 중단: 없음. 다음: G1.7 PASS.

## Phase 1.8 — Ch1 신규 §최종 종합식·피팅·예측 결론
- **Steps 24–28.** 입력: 위 전 절 + Implementation Interfaces(IF-1). 산출: 신규 절 1개 — **단일 master 식 한 줄**(IF-1) + **파라미터 표**(전이당 {U_j,w_j,Q_j,ΔH_{a,j},χ,R_n}+C_bg) + **데이터→파라미터 사상**(OCV→{U_j,w_j,Q_j}; 펄스→R_n; 0.1/0.2C→χ; 15/23/45℃ Arrhenius→ΔH_a) + **예측 단계**(임의 T,I 대입). 박스로 "이 식·이 데이터·이 순서로 피팅하면 닫힌다".
- **Gate G1.8:** 신규 절에 master 식(별행 boxed)·파라미터 표·데이터 매핑·예측 4요소 전부 존재(grep 4항목) + 신규 식 손검(차원·극한 ξ→평형 peak, I→0 환원) 기록 + 기존 식과 부호·기호 정합.
- 중단: master 식 파라미터 집합이 Assumptions와 다르게 요구되면 STOP(새 범위) — 그 외 진행. 다음: G1.8 PASS.

## Phase 1.9 — Ch1 빌드·전수정합·Codex 적대검수·커밋
- **Steps 29–31.** 산출: xelatex 2-pass 빌드, undefined ref 0; 절간·전후반 연결 전수 재독; Codex foreground(`codex:codex-rescue --wait --fresh`) 적대검수(연결 비약·신규식 정합·단일문건 규율, MAJOR 0, Ch1 원문 대조 검증); result+ledger; **개정 ch1.tex+pdf 만 명시 스테이징 커밋·푸쉬**.
- **Gate G1.9:** 빌드 로그 "0 undefined" + Codex MAJOR 0(또는 시정 후 재검 0) + Read Coverage 전절 + git 커밋 해시 기록(Archive/zip 미혼입 확인).
- 중단: Codex MAJOR 정정 후에도 FAIL 유지 시(정지조건 #3). 다음: G1.9 PASS → Phase 2.1.

## Phase 2.1 — Ch2 §1 기호·서론: γ_j 정의역 + 최종식 thread
- **Steps 32–34.** 입력: 57–110. 산출: (a) C2-6 기호표 γ_j 를 boundbox와 일치하게 `\in[0,1]` 통일; (b) 서론에 "본 장은 충방전 *하나의 모델식*에 도달한다" 도착점 thread.
- **Gate G2.1:** 표·본문 γ_j 정의역 문자열 일치(grep 두 위치) + 서론 thread 존재 + 단일문건 규율(§1 Chapter-1 언급 0) 유지(grep).
- 중단: 없음. 다음: G2.1 PASS.

## Phase 2.2 — Ch2 §2.1: staging 일차성 보강 (P-4)
- **Steps 35–36.** 입력: 119–125. 산출: staging 4→3→2L→2→1 의 *일차성 기원*(층간 격자 변형·정전 상호작용·staging 질서화로 두-상 공존이 에너지적으로 유리) 1–2문장 보강.
- **Gate G2.2:** §2.1에 일차성 기원 설명 문장 추가(grep) + 빌드 정상 + 기존 eq:hys_g 연결 보존.
- 중단: 없음. 다음: G2.2 PASS.

## Phase 2.3 — Ch2 §2.4↔§3: 두 기원 중복 축약 (P-3)
- **Steps 37–39.** 입력: 162–196. 산출: 두 기원(열역학/동역학) 분해가 서론·§2.4·§3 3회 반복 → §2.4를 *포인터*로 축약(§3가 정식 분해), 중복 제거. §2.4→§3 연결 자연화.
- **Gate G2.3:** "두 기원" 정식 분해 1곳(§3)·나머지 포인터화 확인(grep count 감소) + eq:hys_split 보존 + §2.4→§3 연결 문장.
- 중단: 없음. 다음: G2.3 PASS.

## Phase 2.4 — Ch2 §5: ΔU_hys 중간 로그 이중화 명시 (C2-8)
- **Steps 40–41.** 입력: 251–268. 산출: 두 분기 끝점 로그 차 = `2·ln[(1−u)/(1+u)] = −4 artanh u` 를 명시(현재 단일 로그 −2 artanh u 만 보임). boxed 결과(2/sF 인수) 불변.
- **Gate G2.4:** §5에 끝점 로그 *차*(−4 artanh u 또는 2× 명시) 한 줄 존재 + eq:hys_dU 결과식 불변(손검 재현) .
- 중단: 없음. 다음: G2.4 PASS.

## Phase 2.5 — Ch2 §6: w_j^b 근거 + bare V→V_n (C2-9, P-5)
- **Steps 42–44.** 입력: 280–298. 산출: (a) P-5 w_j^b 가 Ω_j 단독 아닌 *입자 크기·kinetic broadening*으로 정해져 독립 파라미터임을 1문장; (b) C2-9 eq:hys_dQdV·서론 V(q)의 bare V → V_n 통일(Ch1 1.11 정합).
- **Gate G2.5:** eq:hys_dQdV 인자 `V_n`로 통일 확인(grep) + w_j^b 근거 문장 존재 + Ch1 1.11 기호 정합.
- 중단: 없음. 다음: G2.5 PASS.

## Phase 2.6 — Ch2 문헌: reynier2004 cite/제거 (C2-7)
- **Steps 45–46.** 입력: 384–388 + §2.2. 산출: reynier2004 를 §2.2(Ω 기원/∂U/∂T 엔트로피) 자리에 `\cite` 하거나 bibliography에서 제거 — orphan 해소.
- **Gate G2.6:** `\cite{reynier2004}` 본문 존재 ∨ bibitem 제거(grep로 둘 중 하나 확정) + 빌드 미인용 경고 0.
- 중단: 없음. 다음: G2.6 PASS.

## Phase 2.7 — Ch2 신규 §충방전 종합 모델식·피팅·예측 결론
- **Steps 47–51.** 입력: 전 절 + Implementation Interfaces(IF-2). 산출: §hys_param·§hys_fit 를 통합·강화한 **최종 모델식 절** — 충방전 분기 master 식(IF-2: 분기 중심 U_j±½γ_jΔU_hys, 분기별 rise+꼬리) + 파라미터 표 8개{U_j,Ω_j,γ_j,w_j^b,Q_j,∂U_j/∂T,k_j,R_n} + 데이터 매핑(저율 충방전 OCV 15/23/45℃→앞 6개; 0.1/0.2C×3T→k_j,R_n) + 예측(임의 T·I·방향). 단일문건 규율 — *결론 절* 아닌 *도착 산출식* 으로.
- **Gate G2.7:** 신규 절 master 식(boxed)·파라미터 표·데이터 매핑·예측 4요소 존재(grep) + 신규식 손검(Ω≤2RT→Ch1 단일 peak 환원, I→0→ΔV_hys) + 단일문건 규율(인계/전달/결론 라벨 0).
- 중단: 파라미터 집합 변경 요구 시 STOP. 다음: G2.7 PASS.

## Phase 2.8 — Ch2 빌드·Ch1 정합·Codex 적대검수·커밋
- **Steps 52–54.** 산출: 빌드 undefined 0; Ch1↔Ch2 인용·기호 전수 재대조; Codex foreground 적대검수(MAJOR 0, Ch1 원문 대조); result+ledger; **개정 ch2.tex+pdf 만 명시 스테이징 커밋·푸쉬**.
- **Gate G2.8:** 빌드 "0 undefined" + Codex MAJOR 0 + Ch1 인용 6식 재확인 표 + git 해시 기록. 
- 중단: Codex FAIL 유지 시. 다음: 전 phase 종료 → 종합 보고 1회.

## Implementation Interfaces
**IF-1 (Ch1 최종 master 식):**
$$\frac{dQ}{dV}=C_\mathrm{bg}(V_n,T)+\sum_{j}Q_j\Big[\frac{\xi_{\mathrm{eq},j}(1-\xi_{\mathrm{eq},j})}{w_j}+\frac{r_{a,j}}{L_{V,j}}\,e^{-(V_n-V_a)/L_{V,j}}\ \ (s(V_n-V_a)\ge0)\Big]$$
$\xi_{\mathrm{eq},j}=[1+e^{-(V_n-U_j)/w_j}]^{-1}$, $L_{V,j}=|dV_n/dq|_{q_a}L_{q,j}$, $L_{q,j}=\frac{|I|}{Q_\mathrm{cell}}\frac{h}{k_BT}e^{(\Delta H_{a,j}-T\Delta S_{a,j}-\chi\mathcal A_j)/RT}$, $\mathcal A_j=F(V_n-U_j)$, $V_n=V_\mathrm{app}-|I|R_n$. 파라미터/전이: $\{U_j,w_j,Q_j,\Delta H_{a,j},\chi,R_n\}$(+$C_\mathrm{bg}$, 넓은 분포 시 $\rho_G$ 폭). 데이터 매핑 = 기존 S1–S4.

**IF-2 (Ch2 충방전 master 식, $b\in\{\dis,\chg\}$):**
$$\frac{dQ}{dV}\Big|^{b}=C_\mathrm{bg}+\sum_j Q_j\Big[\frac{\xi^b_{\mathrm{eq},j}(1-\xi^b_{\mathrm{eq},j})}{w_j^b}+(\text{동역학 꼬리, IF-1형})\Big],\quad U_j^{\dis/\chg}=U_j\pm\tfrac12\gamma_j\Delta U_j^\hys$$
$\Delta U_j^\hys=\frac{2}{F}[\Omega_j u_j-2RT\,\mathrm{artanh}\,u_j]$, $u_j=\sqrt{1-2RT/\Omega_j}$, $V_\mathrm{app}^b=V_n+s_I^b|I|R_n$($s_I^\dis{=}{+}1,s_I^\chg{=}{-}1$). 파라미터/전이: $\{U_j,\Omega_j,\gamma_j,w_j^b,Q_j,\partial U_j/\partial T,k_j,R_n\}$.

**IF-3 (Result 양식):** [[feedback_phase_execution_loop]] 11항목(Summary/Step Range/Inputs/Files Created/Files Updated/Read Coverage/Execution Evidence/Validation/Gate/Confirmed Non-Changes/Open Issues/Next).
**IF-4 (Ledger):** 12-col(Phase/Subphase|Planned|Actual|Block|Purpose|Status|Plan|Result|Machine Artifacts|Validation|Gate|Next Step).

## Test Plan
- **빌드:** `xelatex` 2-pass each → 로그 "0 undefined references", 페이지 수 기록.
- **단일문건 규율(Ch2):** grep `Chapter 1`/`다음 장`/`인계`/`전달` in §1 = 0; 결론/transmit 절 라벨 0.
- **식별자 보존(Ch1):** `\label{eq:` 전수 before/after 동일(신규만 add).
- **신규식 검수:** 손검(차원·부호·극한: I→0 평형 peak 환원, Ω≤2RT 단일 peak 환원) result에 기록.
- **연결고리:** S1–S4 다리 문장 grep 존재 + 전후반 재독 4-tier.
- **Codex 적대검수:** foreground, MAJOR 0(정정 후 재검). Codex 주장은 Ch1 원문 대조 검증(맹신 X).
- **Read Coverage:** 각 phase result에 읽은 행 범위 명시.

## Assumptions
- A1: IF-1·IF-2 의 파라미터 집합이 박사님이 원하는 "떨어지는 식"의 기준. 다른 집합 원하면 Phase 1.8/2.7서 조정(STOP 조건).
- A2: Ch1 이상 폭 $w_j=RT/F$ 유지(자유 폭 전환은 별도 지시 시).
- A3: 신규 "최종 종합식" 절은 기존 §synth/§hys_param·fit 를 *대체*가 아니라 *통합·강화*(기존 식 보존, 한 곳에 모아 식·표·매핑·예측으로 닫음).
- A4: Codex 적대검수는 Phase 1.9·2.8 각 1회(절 단위 내부 검수는 master 직접).

## Correction History
- 2026-06-08 v1: 작성. 박사님 분노 누적("최종 피팅식 결론 부재·중간 연결고리 없음·Ch1 전후반 단절·내용 부족, 절 단위 루프 계획 20+회 미이행") 수용. 11-section 양식·Phase `<챕터>.<n>`·step 누적·gate 검증가능조건·5-stage 루프·GO 후 끝까지 정합. 기존 검토 결과(REVIEW_CH1_CH2_6LENS, 9f06579)의 확정 결함 C2-1~9·추정 P-1~5·전후반 단절 S1~4를 절 단위 Phase로 사상. GO 시 Step 1(Phase 1.1)부터 Phase 2.8까지 연속 진행.
