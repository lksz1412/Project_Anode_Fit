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

