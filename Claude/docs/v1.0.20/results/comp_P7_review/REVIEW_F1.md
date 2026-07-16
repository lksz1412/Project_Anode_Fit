# REVIEW_F1 — v1.0.20 독립 검수 (검수자 F1)

> 담당 청크: `_sections/ch2_sec00_intro.tex` ~ `ch2_sec10_closing.tex` · `ch2_appA_traps.tex` · `ch2_appB_codemap.tex` · `ch2_bib.tex` · `ch2_preamble.tex` + `appendix_phase_separation.tex` (전문 정독).
> 검수 3축: ① 신본 자체 결함 · ② v1.0.19 대비 regression · ③ 신설 다리(P5 인용·B-005 중간식·교차 참조)의 물리·서지 정확성.
> 기준 문건 정독 완료: V1020_STYLE_RUBRIC.md · V1020_REFERENCE_LEDGER.md · V1020_CHANGE_LOG.md · V1020_P1_CITATION_BASELINE.md.
> 심각도: H=물리·수식 오류/오귀속 · M=유도 비약·정합 결손·regression · L=표기·문장·일관성. 축: ①/②/③.
> 다른 검수 창(O1/O2/O3) 산출물 미참조. 문서 파일 무수정(read-only) — 본 파일만 기록.

## 발견 목록

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|

### ch2_sec00_intro.tex (전문 정독 완료, 69행)
- ② regression: v1.0.19 와 바이트 동일(diff 무변경) — regression 없음.
- ③ 교차: L8 "Chapter 1 §3 의 평형 중심 전위" — Ch1 신본 `ch1_sec03_center.tex` eq:Uj(L53) $U_j(T)=(-\Delta H+T\Delta S)/F$ 와 문자 일치 확인. L61 "Chapter 1 §15" — Ch1 toc §1.15 = LCO 전자 엔트로피 항, 일치.
- refute 시도: L26 $\dot Q_\rev=-IT\,\partial U_\oc/\partial T=-(IT/F)\Delta S(x)$ — $\partial U_\oc/\partial T=\Delta S/F$(L49 사슬 박스)와 자기정합. 부호 규약의 실체 검증은 sec07 정독에서 수행(후술).

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| F1-01 | ch2_sec00_intro.tex:20–21 | L | ① | "상수 엔트로피는 SOC 축 위에서 봉우리·골·부호 반전을 만들 자유도 자체가 없다"는 동기 서술이 다전이 겹침 하에서는 과장 — 전이별 상수 $\Delta S_j$ 라도 부호가 다르면 겹침 가중 블렌드(본 장 파생 A 자신)만으로 SOC 축 부호 교대·계단형 요철은 재현 가능. 재현 불가한 것은 봉우리 내부 발산(config 부분몰 꼬리)과 비계단 연속 모양이다 | 파생 A(ch2_sec05) 자신이 $\sum_j w_j[\Delta S_j/F+\text{config}]$ 로 모양을 만듦 — config 항 없이도 $w_j$ 블렌드가 $x$-의존 생성. v1.0.19 동문(신규 결함 아님) | "봉우리 내부의 발산·연속 모양까지는 만들 수 없다" 수준으로 한정하는 후보(v1.0.21). 서론 동기 문단이므로 존치 가능 |

### ch2_sec01_partition.tex (전문 정독 완료, 145행)
- ① 수식 전 검산: eq:Z1·eq:occ(마지막 등식 분자분모 나눗셈 포함)·eq:muV·단위 환산(βF=N_A/w 재계산 일치)·eq:logistic(θ/ξ 여집합·부호 방향)·eq:Vxi(θ=1−ξ 대입 재유도)·eq:BW·eq:Veq_BW(∂g/∂θ 직접 미분 일치)·eq:slope_BW(θ=1/2 대입 (2Ω−4RT)/F 재계산 일치)·임계 Ω=2RT — 전부 재유도 일치.
- ② regression: v1.0.19 와 바이트 동일 — 없음.
- ③ 교차(전건 실검): L12·39·47 "Chapter 1 §2" → Ch1 toc §1.2(Part 0) 실재. L39–40 Ξ₁ 표기 통일 — Ch1 신본 `ch1_sec02a_part0.tex` L215–217 이 역방향으로 "Chapter 2 (eq:Z1) 같은 기호 Ξ₁ 통일" 명시, B-001 신설 원형은 Ξ₁⁰ 로 위첨자 구분되어 충돌 없음. L42–43 $\tilde\varepsilon=\varepsilon_0-k_BT\ln q(T)$ — Ch1 eq:sm-epstilde 와 문자 일치. L45–46 $s_\mathrm{int}=-\partial f_\mathrm{int}/\partial T=k_B\partial(T\ln q)/\partial T$ — Ch1 eq:sm-sint 문자 일치(선도항 $+k_B\ln q$ 포함). L58 각주 σ_d "Chapter 1 §1" — ch1_sec01_n0n1.tex L14·28–31 실재. L77 "Chapter 1 §5 의 logistic 평형 종" — Ch1 eq:xieq(L169) 실재. L82 "일반형 $w_j=n_jRT/F$" — Ch1 sec05 L154 문자 일치. L133 "Chapter 1 §4 spinodal 조건" — Ch1 toc §1.4.2 실재.
- refute 시도: eq:occ 를 로그 미분 경로($k_BT\,\partial\ln\Xi_1/\partial\mu$)로 재검 — 동일 결과. BW 항 Ω>0 부호 해석(동종 인력=상분리) — eq:BW 의 +Ωθ(1−θ) 는 혼합 벌점 방향으로 정합.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| F1-02 | ch2_sec01_partition.tex:34–36 | L | ① | FD 동형 서술의 "다른 점" 목록에 "단일 준위 에너지가 $\varepsilon_0-\mu$ 라는 것뿐"이 포함되나, 지수 인자가 $(\varepsilon-\mu)$ 꼴인 것은 FD 와 동일하므로 이는 '다른 점'이 아님 — 실제 차이는 (i) 입자 정체(Li 이온), (ii) 준위 스펙트럼이 아닌 단일 준위, (iii) 배타의 기원(기하 vs Pauli). (iii)은 이 문장에 없고 Ch1 §2 verifybox ★함수형 가드가 담당 | Ch1 ch1_sec02a L256–259 대조. FD 점유 $f(E)=1/(e^{\beta(E-\mu)}+1)$ 과 지수 구조 동일 | "다른 점은 입자가 Li 이온이고 준위가 연속 스펙트럼이 아닌 단일 준위라는 것뿐" 수준으로 정밀화 후보. v1.0.19 동문 |

### ch2_sec02_config.tex (전문 정독 완료, 189행)
- ② regression: 유일 변경 = L9 "(\S\ref{ssec:litverif})" 병기(U10) — 문장 훼손 없음, 나머지 전행 구본 동일.
- ③ U10 후방 참조 검증: L9 의 \ref{ssec:litverif} 는 L132 §2.2.4(문헌 검증 — reynier2003·allart2018 인용 실재)로 해소 — P1_CITATION_BASELINE U9/U10 처리 기록과 정확 일치. PASS.
- ① 수식 검산: eq:Sconfig(BW 둘째 항/(−T) 일치)·eq:dSconfig(±1 상쇄 재유도)·eq:dVdT_config(부분몰 항 부호 +R/F ln[ξ/(1−ξ)] 재유도 일치)·부호 3분기(ξ→1/0/½)·각주 단위 환산 29/96485=0.30 mV/K 재계산 일치·ΔH⁰_j=−FU_j+FT∂U_j/∂T 항등식 재유도 및 stage 2→1 수치(−96485×0.0853−4770=−13001 J/mol≈−13.0 kJ/mol) 재계산 일치.
- ③ 교차: L128 "Chapter 1 §14" — ch1_sec14_lcodecomp.tex eq:lco-configsplit 이 정확히 '중심 표준값/내부 분포' 분리를 가짐, 한정 문구("config 중심/분포 분리에 한정한 대응")도 실제 대응 범위와 일치. L141 "Chapter 1 의 전이별 중심 표준값 +29→0→−5→−16" — Ch1 tab:staging ΔS_rxn 열과 문자 일치. MCMB 단위 각주 [미검증] = 확정 판정 맥락상 정직 공백 관용(결함 아님) 확인.
- refute 시도: tab:ds 의 "정합" 주장 반박 시도 — +29 끝점 등치의 취약성은 본문 스스로 "구간 대표값 수준"으로 한정(L143–145)하여 과장 아님. 기각.

| # | 위치(파일:행) | 심각도 | 축 | 발견 | 근거 | 제안 |
|---|---|---|---|---|---|---|
| F1-03 | ch2_sec02_config.tex:49 | L | ① | "계수 $R/F$ 는 자리당 $n_j{=}1$ 서식이며"의 '자리당'이 모호 — $R/F$ 는 몰당 계수이고 여기서 의도는 '다중도 $n_j=1$ 인 기본 서식'. '자리당'이 단위(per site)로 오독될 여지 | Ch1 sec05 L154 는 같은 대상을 "기본 폭"으로 지칭. v1.0.19 동문 | "다중도 $n_j{=}1$ 기본 서식" 등으로 어휘 정리 후보(?) |
