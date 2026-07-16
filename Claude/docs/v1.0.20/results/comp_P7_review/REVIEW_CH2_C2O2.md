# REVIEW_CH2_C2O2 — 독립 검수 (v1.0.20 Ch2 + Appendix)

> 검수자: C2O2 (독립). 언어: 한국어. 다른 REVIEW_*.md 미열람(독립성 보존).
> 대상: `_sections/ch2_*.tex` + `appendix_phase_separation.tex`
> 신본: `/home/user/Project_Anode_Fit/Claude/docs/v1.0.20/`
> 구본(대조 read-only): `/home/user/Project_Anode_Fit/Claude/docs/v1.0.19/`
> 검수 3축: ① 신본 자체 결함 · ② v1.0.19 regression · ③ 신설 다리 물리·서지 정확성
> 심각도: H=물리·수식 오류/오귀속 · M=유도 비약·정합 결손·regression · L=표기·문장·일관성
> 발견 # = C2O2-NN

기준 문건 정독 완료: V1020_STYLE_RUBRIC.md · V1020_REFERENCE_LEDGER.md · V1020_CHANGE_LOG.md · V1020_P1_CITATION_BASELINE.md
이 창 소관 변경: C-017 · C-018 · B-005 · C-019 (CHANGE_LOG) · U9 · U10 (CITATION_BASELINE)

---

## 발견 목록 (파일별 — 정독 완료 시 append)

발견 형식: | # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
Cross-ref(특별축)·수치검산은 전용 섹션에서 별도 정리.

---

### ch2_preamble.tex (전문 정독 완료, 52행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | 신본 line 35 `\newtheorem*{bgbox}{배경}` 1행 추가 외 v1.0.19와 완전 동일. B-003(bgbox 환경 신설) 의도된 변경과 1:1 대응 — regression 없음. | CHANGE_LOG B-003; 구본 51행 vs 신본 52행 diff = bgbox 1행. | 조치 불요. |

가장 약한 곳: bgbox 신설이 ch2에서 실제로 사용되는지는 sec03 서두(페르미온/보손 배경 참조)에서 검증 예정 — 환경만 있고 미사용이면 orphan 후보(A3). → sec03에서 확인.

### ch2_sec00_intro.tex (전문 정독 완료, 69행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | 신본·구본 완전 동일(69행, byte-identical 수준). 의미 약화·자산 유실 없음. | 구본/신본 대조. | 조치 불요. |

물리 검산: line 8 $U_j=(-\Delta H+T\Delta S)/F$ = $-\Delta G/F$ (정합), line 26 $\dot Q_\rev=-IT\partial U/\partial T=-(IT/F)\Delta S$ 는 $\partial U/\partial T=\Delta S/F$ 식별과 내부 정합. cross-ref: Ch1 §3(평형중심전위)·§15(LCO 전자엔트로피) — 특별축에서 검증.
가장 약한 곳: line 61 "그 상세 전개는 Chapter 1 §15" — §15 실제 내용이 LCO 전자엔트로피인지 Ch1 대조 필요(특별축).

### ch2_sec01_partition.tex (전문 정독 완료, 145행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | 신본·구본 완전 동일(145행). regression 없음. | 대조. | 조치 불요. |
| C2O2-01 | ch2_sec01_partition.tex:82,85 | L | ① | keybox 일반형 $w_j=n_jRT/F$ 도입하면서 두-상 임계는 $\Omega_j>2RT$ 로 적음 — spinodal 유도(eq:slope_BW)는 $n_j{=}1$ 격자기체 기준이라, $n_j\ne1$ 서식에서 임계값이 $2RT$ 그대로인지 $2n_jRT$ 인지 본문상 미봉합. | line 82 일반형 $w_j=n_jRT/F$ 도입 vs line 131 임계 $\Omega=2RT$(n=1 유도). 구본에도 동일 존재 → 신규 결함 아님(선재). | 선재·방어가능(평균장 임계는 자리당 정의). 지적은 정직성 차원 L; 수정 불요. |

수식 재검산(전부 정합): eq:occ FD형 마지막 등식(분자분모 ÷$e^{-\beta(\varepsilon_0-\mu)}$) OK · line 45 $s_\mathrm{int}=-\partial f_\mathrm{int}/\partial T$, $f_\mathrm{int}=-\kB T\ln q$ ⇒ $\kB\partial(T\ln q)/\partial T$, 선도항 $+\kB\ln q$ OK · eq:logistic θ/ξ 부호·극한(ξ→1 고전위) OK · eq:Vxi Nernst OK · eq:Veq_BW $\partial g/\partial\theta$ 미분 OK · eq:slope_BW $\theta=1/2$서 $(2\Omega-4RT)/F$, 임계 $\Omega=2RT$ OK.
cross-ref 표시(특별축 검증): §2 Part0(line 13·39·42·47·113)·§1 σ_d(line 58-59)·§5 ξ_eq(line 77)·§4 spinodal(line 133)·ε̃=ε_0−k_BT ln q(T)(line 43)·Ξ₁ 표기(line 39).

보강: ch2_preamble bgbox 관련 — ch2_*.tex 전체에 `\begin{bgbox}` grep 0건. ch2_preamble line 35의 bgbox 정의는 Ch2에서 미사용(정의만 존재). B-003이 명시적으로 ch2_preamble 포함이라 의도된 추가이며 페르미온/보손 bgbox 실체는 Ch1 §2에 있고 sec03이 후방참조하므로 분업 성립. → L급 관찰(아래 C2O2-02).

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| C2O2-02 | ch2_preamble.tex:35 | L | ①/② | bgbox 환경이 ch2_preamble에 정의되나 Ch2 절 어디서도 `\begin{bgbox}` 미사용(grep 0건). | Grep ch2_*.tex. B-003(CHANGE_LOG)이 ch1+ch2 preamble 동시 추가 명시. Ch2의 페르미온/보손 배경은 Ch1 §2 bgbox를 참조(sec03:9). | 결함 아님·B-003 의도(대칭·자족블록 이동 설계). 향후 Ch2 자체 bgbox 미도입 시 정리 후보로만 기록. |

### ch2_sec02_config.tex (전문 정독 완료, 189행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ②/③ | 신본 line 9 `(\S\ref{ssec:litverif})` 1개 추가 외 v1.0.19와 동일(15040 vs 15017 byte). U10(CITATION_BASELINE) 처리와 1:1 — regression 없음. 참조 타겟 ssec:litverif(line 132) 실재, 실 인용 reynier2003·allart2018(line 135) 존재 = U10 적정 해소. | CHANGE_LOG/CITATION_BASELINE U10; 구본/신본 대조. | 조치 불요. |

수식 재검산(전부 정합): eq:Sconfig=−R∑p ln p OK · line 19 "BW 둘째항/(−T)=S_config" OK($RT[\cdot]/(-T)=-R[\cdot]$) · eq:dSconfig $\partial_\theta$ 상수±1 상쇄 OK · eq:dVdT_config $\partial V/\partial T|_\xi=\Delta S_{rxn,j}/F+(R/F)\ln[\xi/(1-\xi)]$, 둘째항=$(1/F)\partial S_config/\partial\theta|_{1-\xi}$ 등식 OK · 부호 3분기(ξ→1:+∞, ξ→0:−∞, ξ=½:0) OK · line 176 $\Delta H^0_j=-FU_j+FT\partial U_j/\partial T$ = $\Delta G+T\Delta S$ OK(예 −13.0 kJ/mol은 $U_j\approx0.085$V·$\Delta S=-16$서 재현).
관용 판정 준수: line 138-140 [미검증] MCMB 단위 각주 = 정직 공백 관용, 지적 대상 아님(맥락 확인).
cross-ref 표시: §14 반응엔트로피 삼분해·슬롯(line 128) — 특별축.
가장 약한 곳: tab:ds에서 4→3 전이 $\Delta S^0_j{=}+29$를 $x{=}0.08$(창 끝, ξ≈1로 config 발산 자리) 측정점과 등치. 중심 표준값 정의($[\Delta S(x)]_{\xi=1/2}$, config=0)와 원리상 상충하나, 본문(line 143-145·168)이 "구간 대표값 수준"으로 명시 한정 → 정직 처리, 결함 아님. 다만 헤드라인 "부호·규모 정합"이 이 각주로 상당히 약화됨(L 미만, 관찰).

### ch2_sec03_vibel.tex (전문 정독 완료, 102행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ③ | **B-005 재유도 전 단계 검산 통과.** 본문 line 19 중간식 $S_{vib,k}=-\kB\ln(1-e^{-\beta\hbar\omega_k})+\kB\beta\hbar\omega_k n_k$ = 손 재유도 결과와 일치(둘째항 $\frac{e^{-x}}{1-e^{-x}}=n_k$, $k_B\beta\hbar\omega_k=\hbar\omega_k/T$). 항등식1·2 각각 참, 대입 경로로 eq:Svib_mode $k_B[(1+n_k)\ln(1+n_k)-n_k\ln n_k]$ 정확 회수. 표시블록·라벨·최종식 불변(B-005 명세 준수). | 손 재유도(위 검산). 구본 line 15 "어느 경로든 닫힌형" 점프 → 신본이 중간식 인라인 노출. | 조치 불요(정확). |
| — | — | — | ③ | sec03:9 페르미온/보손 배경 참조 1문장 신설 — Ch1 §2 bgbox(ch1_sec02a_part0.tex:171-188)와 분업 성립. bgbox가 교환대칭·스핀통계·Pauli·BE/FD + "진짜 양자통계는 Ch2"(포논 BE·전자 FD) forward 다리를 자족 정리. sec03 문장이 이를 정확 후방참조. | 양 파일 대조. B-002 설계와 정합. | 조치 불요. |

수식 재검산(전부 정합): BE $n_k=1/(e^{\beta\hbar\omega_k}-1)$·$f_k$ OK · eq:Se_start FD 엔트로피 범함수 OK · Sommerfeld $\int(-\partial f/\partial E)(E-E_F)^2dE=\frac{\pi^2}{3}(k_BT)^2$ OK · $C_e=\frac{\pi^2}{3}k_B^2 Tg(E_F)$·eq:Se-ch2 $S_e=\int C_e/T'dT'=\gamma T$ OK · 차원 $k_B^2Tg=k_B$ OK.
cross-ref 검증: eq:Se-ch2(line 61) vs Ch1 eq:Se(ch1_sec15:82) 별개 라벨 ✓ · §15 전자엔트로피 유도($S_e/k_B=\frac{\pi^2}{3}(k_BT)g(E_F)$, ch1_sec15:235/245) 실재·형태 일치 ✓ · §13·§15(line 76)·§8·§9(line 89) — 특별축 잔여 검증.
가장 약한 곳: line 90 "$\Delta S_{a,j}$(…prefactor 온도의존)" — Eyring $e^{\Delta S_a/R}$은 엄밀히 T-무관 상수(전체 prefactor $\frac{k_BT}{h}e^{\Delta S_a/R}$만 T-의존). "prefactor 온도의존" 표현이 압축적이나 오류는 아님(TST prefactor에 $\Delta S_a$가 든다는 취지). 구본에도 동일 → 선재·비regression. L 미만.

### ch2_sec04_einstein.tex (전문 정독 완료, 116행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | 신본·구본 완전 동일(116행). regression 없음. | 대조. | 조치 불요. |
| C2O2-03 | ch2_sec04_einstein.tex:61-63 | L | ① | $\Delta F_\vib(T)\equiv RT\ln(1-e^{-\theta_{E,j}/T})$를 "모드 자유에너지 편차"로 명명하나, 이 식은 절대 모드 자유에너지($F_\vib(T)$)이지 $T_{ref}$ 대비 편차가 아님. $\Delta S_\vib$(eq:dSvib)·$\Delta U_\vib$는 $T_{ref}$서 0인 편차 규약을 따르는데 $\Delta F_\vib$만 규약 이탈($T_{ref}$서 비영). | eq:dSvib/eq:dUvib은 편차, $\Delta F_\vib(T)\equiv RT\ln(...)$은 절대량. 단 eq:dUvib이 $\Delta F_\vib(T)-\Delta F_\vib(T_{ref})$로 쓰므로 최종 결과 무영향. 구본 동일 → 선재. | 명명 정합 위해 $F_\vib$로 표기하거나 "편차" 어휘 완화 후보(수정 불요·결과 정확). |

수식·수치 재검산(전부 정합): eq:Svib-einstein = eq:Svib_mode에 $n=1/(e^{u}-1)$ 대입($un=u/(e^u-1)$) OK · 고온극한 $R[1+\ln(T/\theta_E)]$($-\ln u+u/2$와 $1-u/2$ 상쇄) OK · 저온 $S_\vib\to0$ OK · $S_\vib=-\partial\Delta F_\vib/\partial T$ 손 재유도 = eq:Svib-einstein OK · **수치 4점 직접 재계산: −3.74/0/+3.70/+9.14 µV/K 전부 일치**(θ_E=700K·T_ref=298.15K).
cross-ref 검증: u_j 동명 각주(line 20-22) — Ch1 §4 spinodal 근 $u_j=\sqrt{1-2RT/\Omega_j}$와 별개 명시(특별축에서 Ch1 §4 대조 예정). $\theta_E$ vs $\theta$(점유율) 기호 가드(line 10-12) 적정.

### ch2_sec06_limits.tex (전문 정독 완료, 53행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | 신본·구본 완전 동일(53행). regression 없음. | 대조. | 조치 불요. |

검산: tab:limits 6코너 전부 앞 절 유도와 정합(ξ→1:+∞·ξ→0:−∞·ξ=½:ΔS/F config=0·Ω→2RT plateau·단일봉우리 환원·고온 Sommerfeld 축퇴극한 전용 "정량 부적용" 정직 한정). keybox "전이당 상수+분포" 판정 물리 타당.
가장 약한 곳: 고온행(line 26-28) "electronic ∝T 우세화"는 금속성 호스트 전제 — 흑연 하프셀(준금속·소수 electronic)엔 약한 코너이나, 표가 일반 ∂U_oc/∂T용이고 "정량 부적용" caveat 있어 결함 아님.

### ch2_sec05_mixing.tex (전문 정독 완료, 241행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ②/③ | 유일 diff = line 168-169 각주에 `\cite{dahn1991,ohzuku1993}` 추가(21298→21325 byte) = U9 처리. 그 외 v1.0.19와 동일. regression 없음. | 구본/신본 대조; CITATION_BASELINE U9. | 조치 불요. |
| — | — | — | ③ | **U9 인용-주장 정합 확인.** 주장(line 168-169) "2L→2·2→1을 두-상으로 지목하는 근거는…실측 plateau·staging 문헌의 상평형". dahn1991=Li_xC6 상도표·staging 표준(PRB44,9170), ohzuku1993=Li-GIC 형성·staging(JES140,2490) — 둘 다 주장을 직접 지지, 과대·부정합 없음. 각주 산술 2RT≈4957 J/mol(=2·8.314·298.15) 정확. | 문헌 정체 대조; 산술 재계산. 두 키 원장 V1 등재. | 조치 불요. bib 필드 대조는 ch2_bib에서. |

수식 재검산(전부 정합): eq:implicit_diff 음함수미분 부호 OK · eq:gj $\partial\xi_j/\partial U=\xi(1-\xi)/w_j$(logistic 증가) OK · eq:dxidT $a_j=(U-U_j)/w_j$ 연쇄율 2조각($-g_j\partial U_j/\partial T$·$-g_j n_jR z_j/F$) 손 재유도 일치 · eq:dwdT-nT 곱미분 OK · eq:weighted 분모=측정 dQ/dV($\sum Q_jg_j=\partial(Q\bar x)/\partial U$) OK · eq:single_config 단일전이 환원($+n_jR z_j/F$, sec02 $n_j{=}1$ config와 정합) OK · eq:hys_rev 분기평균 상쇄 OK · 소산 차원 $I\Delta U$=[W]·$Q_{cyc}\Delta U$=[J] OK.
내부정합 통과(교차): fig:blend 캡션 "탈리튬화 진행 −16→−5→0→+29 상승"은 tab:ds(sec02, x증가서 +29→0→−5→−16 하강)를 $\bar x=1-x$ 좌표반전과 정확 일치. g_j 4종 기호충돌 가드(line 39-40) 명시.
cross-ref 표시: §2 g_j(ξ)(line 39)·§4 분기중심 $\gamma_jh_{\eta,j}{=}1$ 특수형(line 196)·§7 broadening 세출처(line 177) — 특별축.
수치 표시(appB/sec08 대조 예정): config 항 범위 [−0.21,+0.14] mV/K·단순식 최대오차 0.18·해석상한 0.21·양끝 폭 0.35·~0.3 mV/K 우열역전(line 92-108).
가장 약한 곳: srcbox 수치검증(line 87-111)이 전적으로 내부자료 \cite{numverif2026}에 의존(원장상 "검증 대상 아님") — 독립 확인 불가. 단 "★전제 명시" 문단(line 102-110)이 "해석 미분 사슬의 자기일관성 검증이지 실측 검증 아님"으로 강하게 정직 한정 → 과장 아님, 결함 아님(오히려 강점). 논리적 최약점: Ω 초기값이 네 전이 모두 2RT 초과라면 모델 자체론 넷 다 불안정(두-상)인데 일부만 두-상 지목 — 각주가 "문턱이 특정 못함→문헌 특정"으로 봉합(선재·Ch1 Ω 소관, sec05는 정직 처리).

### ch2_sec07_revheat.tex (전문 정독 완료, 59행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | v1.0.19와 완전 동일(diff 0). regression 없음. | bash diff. | 조치 불요. |

수식·부호 재검산(전부 정합): eq:qrev $\dot Q_{irr}=I(U_oc-V)\ge0$(방전 V<U_oc) OK · $\dot Q_{rev}=-IT\partial U_oc/\partial T=-(IT/F)\Delta S$ OK · srcbox $\Delta G=-FU_oc$·$\Delta S=+F\partial U_oc/\partial T$ OK · 흡/발열 부호(방전 I>0: ΔS>0→흡열·ΔS<0→발열) OK.
cross-ref 표시: 라벨층위 "방전(I>0)=Bernardi 리튬화 vs Ch1 탈리튬화 σ_d=+1"(line 29-30) — Ch1 §1·§4 대조.
가장 약한 곳: sec07은 x(Li함량) 축("저-x 흡열·고-x 발열"), sec08/tab:qrev는 x̄=1−x 축("저-x̄ 발열·고-x̄ 흡열")로 표기 규약이 절 간 반전 — 각각 내부 라벨링되어 오류 아니나(저-x=고-x̄ 정합 확인), 절 넘나들 때 G-follow 혼동 위험(L 미만 관찰).

### ch2_sec08_synthesis.tex (전문 정독 완료, 145행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | v1.0.19와 완전 동일(diff 0). regression 없음. | bash diff. | 조치 불요. |
| — | — | — | ① | **tab:worked 가중평균 산술 직접 재계산 통과.** [중심+config] 4값(−0.203/−0.206/−0.220/−0.157) 표와 일치, 가중합=−0.204 mV/K, 단순식=−0.134, config몫=−0.070 전부 재현. g_j·config·ΔS⁰/F·비중합(=1.000)·ΔS=−19.7·Q_rev/I=+60.8mV·U_oc=74.4mV 독립 재계산 일치. | 직접 재계산(R/F=0.08617 mV/K·w=RT/F=25.69mV·F=96485). | 조치 불요(정확). |

수치 전수 검산: config_j=(R/F)ln[ξ_j/(1−ξ_j)] 4값 OK(−0.458/−0.220/−0.154/−0.037) · g_j=ξ(1−ξ)/w 4값 OK(0.19/2.61/4.77/9.30) · ΔS⁰/F 4값 OK(tab:ds ±29/0/−5/−16 ÷F) · (e) ΔS=F·∂U/∂T=−19.7·Q_rev/I=−T∂U/∂T=+60.8mV OK · tab:qrev 5행 ΔS·Q_rev/I 재계산(±0.1mV rounding) 정합·부호교대(발열→흡열) OK.
특별축(appB 대조 예정): 회귀 기준 후보값 −0.204/−0.134/−0.070·74.4mV·+60.8mV·5점표 — appB 문자 일치는 appB 정독에서.
가장 약한 곳: 없음(수치 자기일관 완결). 굳이 꼽으면 tab:worked에 Q_j 개별값 미노출로 비중을 g_j만으로 역산 불가 — 단 ∑Q_jg_j=6.18/V·Q=0.97Q_cell 병기 + 비중합=1 확인으로 자기일관.

### ch2_sec09_method.tex (전문 정독 완료, 43행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | v1.0.19와 완전 동일(diff 0). regression 없음. | bash diff. | 조치 불요. |

검토: procedurebox 5단계 정합(저율 다온도 dQ/dV→분극분리 Ch1 §1 $V_n=V_{app}-\sigma_d|I|R_n$→동시피팅 MSMR Ch1 §17→ΔS⁰=F dU_j/dT·Allart 대조→봉우리내부 자동). MSMR 풀네임 "Multi-Species, Multi-Reaction"(line 20) 원장 C4 일치. 정직한 한계 5항 전부 명시적 공백 선언.
cross-ref 표시: Ch1 §1 V_n(line 16)·§17 MSMR(line 20) — 특별축.
가장 약한 곳: step 2 $V_n=V_{app}-\sigma_d|I|R_n$의 Ch1 §1 실재·기호 일치는 Ch1 대조 필요(특별축).

### ch2_sec10_closing.tex (전문 정독 완료, 26행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | v1.0.19와 완전 동일(diff 0). regression 없음. | bash diff. | 조치 불요. |

검토: 맺음이 4파생·6코너·계산예제(−0.204·<0.001µV/K)·tab:qrev 부호교대·방법론출구를 정확 요약, 서두 C-6(가역발열 목적함수)와 수미상관. 자기이력 서술 없음(D1 준수). cross-ref §7 broadening(line 13).
가장 약한 곳: 없음(요약 절, 신규 주장 0).

### ch2_appA_traps.tex (전문 정독 완료, 75행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | v1.0.19와 완전 동일(diff 0). regression 없음. | bash diff. | 조치 불요. |

검토: 함정표 12항(s/σ_d·θ/ξ·θ/θ_E·x̄/x·g 4종·F_vib/F·u_j/x·u_j vs Ch1 u_j·방전 라벨·ΔS/ΔS_a·ΔS_vib(T)/∂S_vib/∂x·S_e 라벨) 전부 본문과 정합. line 65-68 "S_e 라벨: eq:Se-ch2 vs Ch1 §15 eq:Se(별개 컴파일 객체)" = sec03 cross-ref 재확인. line 49-51 "u_j vs Ch1 §4 spinodal 근" = sec04 각주 정합.
참고: line 42 "$\Delta F_\vib=RT\ln(1-e^{-\theta_E/T})$" 표기가 C2O2-03(sec04)의 절대량-편차 명명 이슈를 그대로 계승(내부 일관·결과 무영향).

### ch2_appB_codemap.tex (전문 정독 완료, 70행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ② | v1.0.19와 완전 동일(diff 0). regression 없음. | bash diff. | 조치 불요. |
| — | — | — | ①/특별축 | **appB 회귀 기준값 ↔ sec08 수치 문자 일치 확인.** B.2 표: entropy_coefficient_x(0.25)=−0.204·단순식 −0.134·config −0.070 · U_oc=74.4mV · round-trip −0.204·<0.001µV/K · ΔS=−19.7·Q_rev/I=+60.8mV · 5점(−0.307/−0.204/−0.089/+0.044/+0.218; +91.5/+60.8/+26.6/−13.2/−64.9) · 175점 파생A — sec08/tab:qrev와 전부 일치. | appB B.2 vs sec08(a-e)·tab:qrev 대조. | 조치 불요. |

검토: doc-leads 프레이밍(코드가 문건 구현)·함수명 부록B 국한(A5 준수)·B.3 θ_E 미지정 bit-exact 하위호환(sec04 C-61 정합)·B.4 입력규약(s=+1·두-상 w 자유폭) 정합.

### ch2_bib.tex (전문 정독 완료, 28행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ②/③ | 변경 6건 전부 CHANGE_LOG 대응: 헤더 14→16 카운트·dahn1991 신설(C-017)·ohzuku1993 신설(C-018)·msmr_partI 023502(C-005)·msmr_partII 제목전문+103505(C-006)·hysteresis2018 179-184(C-007). 무단 변경 0. | bash diff; CHANGE_LOG. | 조치 불요. |
| — | — | — | ③ | **dahn1991·ohzuku1993 3자 정합 확인.** ch2_bib(line 9-10) = ch1_bib(line 5-6) 저자·제목·권·쪽·DOI 문자 완전 동일; 원장 V1 등재 서지와 일치. | ch1_bib/ch2_bib/원장 대조. C-017 "3자 정합" 명세 충족. | 조치 불요. |

검토: bibitem 16개 실카운트 확인(15외부+numverif2026). msmr_partI 식별함정 각주(Ch1 Part1[ECS Adv ad7d1c]과 별개) 보존. numverif2026 [내부자료] 표기 유지.
가장 약한 곳: dahn1991 쪽번호 "9170"은 article/시작쪽만(PRB staging 논문 관례) — ch1_bib·원장 모두 동일 표기라 정합, 문제 아님.

### ch1_bib.tex (교차 대조 목적 정독, 46행 — 담당 청크 아님·읽기만)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ③ | dahn1991(line 5)·ohzuku1993(line 6)이 ch2_bib 신규 2종과 문자 완전 동일 = 3자 정합 성립. 헤더 "36종" 실카운트 36 일치(P1 28 + P2/P4 C-009~C-016 8건 = 36). | 실카운트; CHANGE_LOG C-008~C-016. | 조치 불요(Ch1 소관, 대조만). |

### appendix_phase_separation.tex (전문 정독 완료, 497행)

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| — | — | — | ②/③ | 변경 전부 의도됨: line 3·39 버전스탬프(P6 유지판정)·정규용액×7(44/104/163/210/245/352/380)·격자기체×1(69) 띄어쓰기 정규화·C-019 [A5] Ch.17-18→18-19. 무단 물리변경 0. | bash diff; CHANGE_LOG C-019; rubric C2. | 조치 불요. |
| — | — | — | ③(P6) | **표기 8건 주변 문장 훼손 없음.** 각 "정규용액(regular solution)"/"격자기체(lattice gas)" 병기·문맥 온전, 순수 띄어쓰기 제거. | 8곳 문맥 정독. | 조치 불요. |
| — | — | — | ③(P7) | **C-019 [A5] 정정 정확.** line 494 "Ch.~18--19 (Cahn--Hilliard 선형화·핵생성 이론)" = 원장 [A5](Ch.18 Spinodal→CH선형화·Ch.19 Nucleation). 본문 [A5] 2곳(line 403 핵생성·line 439 spinodal분해) 장번호 무표기·무변경 — C-019 "2곳 무변경" 명세 충족. 사용처-장귀속 정합. | line 403·439·494 대조; 원장 [A5]. | 조치 불요. |

수식·수치 전수 재검산(전부 정합): eq:app-Smix(Stirling) OK · eq:app-Umix(쌍에너지 잉여) OK · eq:app-fxi 정규용액 OK · eq:app-chord/convex/gain OK · eq:app-statA/ct 공통접선 OK · eq:app-mus $\mu_B=g+(1-\xi)g'$·$\mu_A=g-\xi g'$ OK · eq:app-binodal($T_c=\Omega/2R$·Ω=3RT서 ξ_b=0.0707·f_b/RT=−0.0583) 재계산 OK · eq:app-spinodal $u=\sqrt{1-2RT/\Omega}$·ξ_s=0.2113·f/RT=−0.0157 OK · eq:app-maxwell 등면적 OK · eq:app-rstar $r^*=2\gamma/|\Delta g_v|$·$\Delta G^*=16\pi\gamma^3/3\Delta g_v^2$ OK · Cahn-Hilliard μ=f'−2κ∇²ξ·R(k)·k_m=k_c/√2 OK · 차원 [κ]=J/m·[M]=m⁵J⁻¹s⁻¹ OK.
[A1]-[A5] 원장 대조: 전건 일치([A1] sentence-case=서지재량 허용·[A5] "Wiley"=브랜드 통용 허용). μ(θ)=μ⁰+RTln[θ/(1-θ)]+Ω(1-2θ)(line 206)는 ch2 eq:Veq_BW와 부호 정합.
cross-ref 표시: 본문 절참조 §2(Part0)·§4.1(spinodal 근)·§4.2(히스 gap)·§7(broadening) — Ch1 §4.1/§4.2 실재는 특별축에서 확인.
가장 약한 곳: ★기호 배향 — 부록 ξ = 본문 θ(점유율), 본문 ξ(=1−θ)와 여집합. 같은 글자 ξ가 부록·본문에서 반대 양. line 8-9·57-63이 "f 우함수라 binodal·spinodal·Maxwell 결과는 두 좌표 동일, 1계 미분만 부호 반전(§4.2가 처리)"로 명시 한정 → 물리 정확·정직 처리이나, 절 넘나들 때 최대 G-follow 혼동 위험. 결함 아님(강한 가드).

