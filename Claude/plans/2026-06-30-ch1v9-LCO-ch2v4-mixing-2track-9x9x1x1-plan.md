# Ch1 v9(LCO 양극 확장) + Ch2 v4(섞임 항 명시) — 2-트랙 순차 / 각 9종 병렬 체리픽 Plan

> ★두 트랙 **순차**(Track1 Ch1 v9 먼저 → Track2 Ch2 v4). **각 build = 9종 병렬 competition-cherrypick 스킬**(`Project_skills/competition-cherrypick-authoring`). 범위 = **코인 하프셀 데이터 해석용 물리 피팅식**(전셀 합성 E/G 는 범위 외). 교수님 피드백 버전 = Ch1 v10(후속). GO 대기.

## Summary
**목표.** (Track 1) Chapter 1 을 **흑연 음극 + LCO 양극**(둘 다 코인 하프셀 intercalation 전극)으로 **통합 확장**해 v9 를 만든다 — ★v8(v8-11)의 큰 틀·흑연 서술을 그대로 유지하고 *양극 설명이 필요한 부분만 추가*하는 단일 통합본(별도 LCO 문건 아님). ★**전자(electronic) 엔트로피 항은 Chapter 1 본문에 들어가는 게 맞고**(반응 엔트로피의 한 성분), 그것이 Chapter 2(가역 발열)로 확장되는 것이 순서다. 양극 기준 가역 발열을 제대로 구하고, 하프셀 데이터로 전극별 열역학을 분리·해석할 토대를 놓는다. (Track 2) Chapter 2 를 **intercalation 전극의 엔트로피·가역 발열 *통계열역학* 챕터**로 제대로 세워 v4 를 만든다 — ★v3(얇은 "Ch1+ΔS 한 절") 수준을 넘어, **분포(distribution)를 명시 전개**: 격자기체 분배함수 → Li 점유 분포 → $S_\mathrm{config}=-R\sum p\ln p$(Ch1 logistic 의 *기원*), vibrational(포논 분포)·**electronic(Fermi–Dirac, LCO metal–insulator)** 분해, 다전이 겹침의 분포 중첩, 상전이·order parameter(Ω), 분포 재배열 = 가역 발열, 다온도 dQ/dV 피팅. 섞임 항(겹침 dQ/dV-가중·봉우리 내부 config, ξ·Ω 든 닫힌식)은 이 통계열역학 전개의 *일부*로 박힌다. 각 build 는 9종 병렬 경쟁·체리픽. Track 1 은 **LCO 조사 선행**(전자 엔트로피 등), Track 2 는 **통계열역학·분포 설계 선행**. ★Ch1/Ch2 경계: Ch1 = forward dQ/dV(평형 점유+동역학), Ch2 = 그 분포의 엔트로피·온도·가역 발열 통계열역학(고유 챕터 면모).

**왜.** (1) 가역 발열은 전셀=양극−음극이라 양극(LCO) 정량이 선행돼야 함(사용자 지시). LCO 는 graphite 의 config/vib 외에 $x\approx0.5$ order–disorder + **metal–insulator 전이의 전자 엔트로피** 가 추가됨(파생 F) → 조사로 근거화. (2) 섞임 항은 단순 줄글로 부족 — ξ·Ω 든 수식으로 교과서에 명시해야 본인·타인 이해·설명 가능(사용자 지시). (3) 파생 B(섞임 이미 logistic 내장·이중계산 주의)는 본 plan 입력으로 *해결됨*.

**파생 매핑(사용자 확인)**: Track 1 ⊃ **F**(LCO 전자 엔트로피)·**H**(Ch1 forward 코드 LCO 일반화). Track 2 ⊃ **A**(겹침 가중 수치검증)·**C**($w$ vs $w_\eff(\Omega)$)·**D**(히스 하 겹침)·**I**(극한·코너로 "$\Delta S_{\rxn,j}$ 상수" 근사 타당성 확인). **B**(이중계산)=해결·양 트랙에 baked. **E·G**(전셀 합성)=범위 외(후속).

## Current Ground Truth
- **Ch1 현재 = v8**(`Claude/results/v8-11/v8-11.tex`, 유도 확장 교과서판, 흑연 음극 only) + `Anode_Fit_v11_final.py`(forward 코드). **Ch1 v9 = v8-11 base + LCO 양극 확장.** v10 = 교수님 피드백(후속).
- **Ch2 현재 = v3**(`Claude/docs/graphite_ica_ch2_v3.tex`, 가역 발열 초안) + `research/CH2_v3/`(조사). **Ch2 v4 = v3 base + 섞임 항 명시.**
- **확정 물리(파생 B)**: Ch1 봉우리 내부 $\partial V/\partial T|_\xi=\Delta S_{\rxn,j}/F+(R/F)\ln[\xi/(1-\xi)]$ — configurational 이 $w=RT/F$ 에 내장. $\Delta S_{\rxn,j}$=중심(표준) 값. 겹침 $\partial U_\oc/\partial T=\sum_j Q_jg_j\Delta S_{\rxn,j}/(F\sum_j Q_jg_j)$ (dQ/dV-비중 가중).
- **검증된 사슬**(Ch2 v3 조사): ΔS=+nF·∂U/∂T, $\dot Q_\rev=-IT\,\partial U/\partial T$; Ch1 ΔS_rxn ↔ Allart 흑연 ΔS 정량 일치.
- **방법 자산**: competition-cherrypick 스킬(9+9+1+1)·G-derive/G-usable/부호 렌즈·KNOWN_DEFECTS 전파추적·단계적 참고문헌·그림 경쟁.
- **미확인(Track 1 조사 표적)**: LCO 하프셀 entropy coefficient ∂U/∂T(x) 측정값·전자 엔트로피(MIT @x≈0.5) 모델식·LCO dQ/dV 전이 파라미터·도핑/첨가제 보정. (Track 2)는 자체 유도(문헌 보조).

## Phase Range
| Track | Chapter | Phase | 이름 | Steps | 주체·방법 |
|---|---|---|---|---:|---|
| **1** | A 조사(선행) | A.1 | LCO 범위·축·F/H 질문 | 1–4 | master |
| 1 | A | A.2 | LCO 수집·정독·추출 | 5–12 | master + 서브 다세션 sweep(읽기, 비경쟁) |
| 1 | A | A.3 | 종합·Ch1 프레임 적용 설계(전자 엔트로피 항) | 13–17 | master |
| 1 | B build(9종) | B.1 | spine·AUTHOR_BRIEF(v8-11+LCO 명세) | 18–20 | master |
| 1 | B | B.2 | 9종 독립(3S·3O·3C) → 커밋#1 | 21–25 | 9 Agent 병렬 |
| 1 | B | B.3 | 검토1→보완→검토2→체리픽 v9c→재검수→**Ch1 v9**+10회 → 커밋#2~4 | 26–44 | 스킬 골격 |
| **2** | C 설계(선행) | C.1 | 통계역학 분포 spine 조사·설계 | 45–47 | master + 서브 |
| 2 | C | C.2 | 섞임/겹침·극한 수식 설계(A/C/D/I·B) | 48–52 | master |
| 2 | D build(9종) | D.1 | spine·BRIEF(통계열역학 *챕터*) | 53–55 | master |
| 2 | D | D.2 | 9종 독립 → 커밋#5 | 56–60 | 9 Agent 병렬 |
| 2 | D | D.3 | 검토1→보완→검토2→체리픽 v4c→재검수→**Ch2 v4**+10회 → 커밋#6~8 | 61–79 | 스킬 골격 |
| 종합 | E | E.1 | 양 트랙 RESULT·메타·교수님 입력 | 80–82 | master |

## Non-goals (주의점)
- ★**범위 = 코인 하프셀 데이터 해석용 물리 피팅식.** 전셀 합성($\partial U_\mathrm{cell}=\partial U_\mathrm{cat}-\partial U_\mathrm{an}$·calorimetry 결합·E/G)은 **범위 외**(후속). LCO 도 *하프셀(vs Li)* 로 다룬다.
- ★**순차**: Track 1(Ch1 v9) 완료 후 Track 2(Ch2 v4). 동시 진행 X.
- **base 보존·확장만**: Ch1 v9 = v8-11 의 흑연 부분 보존 + LCO 추가(흑연 결과·부호·식별자 변경 X). Ch2 v4 = v3 보존 + 섞임 항 추가. 원본(v8-11·v3·코드·v2 등) 수정 X.
- **이중계산 금지(B)**: 섞임 항 도입 시 $\Delta S_{\rxn,j}$=표준(중심) 값으로 명확히, logistic config 와 이중계산 X.
- Workflow 금지(Agent만)·푸쉬 정책 준수·단계 팝업 0. 추측 인용·미검증 단정 X(4-tier).

## Implementation Changes
- Track1 조사: `Claude/research/CH1v9_LCO/{00_scope, 10_sources, 20_extraction/, 30_synthesis, 35_electronic_entropy_design}.md`.
- Track1 build: `Claude/results/ch1v9/v9-00_spine/` + `v9-01…v9-11/` + 검토·`CH1v9_LEDGER.md` + 최종 `Claude/docs/graphite_ica_ch1_v9.tex`.
- Track2 설계: `Claude/research/CH2v4/41_statmech_spine.md`(분포→엔트로피·config/vib/electronic) + `40_mixing_term_design.md`(A/C/D/I).
- Track2 build: `Claude/results/ch2v4/v4-00_spine/` + `v4-01…v4-11/` + 검토·`CH2v4_LEDGER.md` + 최종 `Claude/docs/graphite_ica_ch2_v4.tex`.
- 종합 `PHASE_2TRACK_RESULT.md`. 본 plan.

## Phase A (Track1 조사 선행) — Steps 1–17 [master + 서브 sweep]
- **A.1 (1–4)** LCO 연구질문: (L1) LCO 하프셀 ∂U/∂T(x)·ΔS(x) 측정 프로파일? (L2) $x\approx0.5$ order–disorder·**metal–insulator 전이의 전자 엔트로피** 모델식·크기(파생 F)? (L3) LCO dQ/dV 전이(주 3.9V·4.05/4.17V) 파라미터(U_j·ΔS_rxn·Ω·폭)? (L4) 도핑/첨가제 보정(pure-LCO 문헌값=초기값)? (L5) Ch1 forward 코드의 LCO 일반화 — 전이 파라미터 교체 + 전자 엔트로피 항 추가로 가능?(파생 H) (L6) LCO 히스/상전이 가역성? **Gate**: 질문·축·쿼리.
- **A.2 (5–12)** 수집·정독·추출(master + 서브 다세션, 읽기 sweep·비경쟁). ★**조사 규모 = master(나) 직접 판단**(사용자 지정 아님). 6축 = ①LCO 하프셀 엔트로피 계수·dV/dT 측정 ②Li$_x$CoO$_2$ 상전이($x\!\approx\!0.5$ order–disorder·**insulator–metal**)·전자 엔트로피 모델 ③LCO OCV/dQ-dV 열역학 ④LCO calorimetry/가역열 ⑤도핑·코팅의 열역학 영향(우리 시료 보정) ⑥양극 엔트로피 계수 추정(MSMR-cathode). **포화 기준**: 각 축에 seminal(예: Reimers&Dahn 1992 상도·Thomas/Reynier cathode entropy) + 최신 권위 + 상충 해소까지 — 목표 ~25–40 수집·~12–18 핵심 정독, *주요 sub-topic 미해결 0* 일 때 종료. 추출카드(방법·식·값·조건·tier·출처). **Gate**: 축별 포화·카드·출처 폐쇄.
- **A.3 (13–17)** 종합 + ★**Ch1 프레임 적용 설계**: LCO 를 같은 전이별 logistic + $U_j(T)$ 로, **추가 전자 엔트로피 항** $\Delta S_{\rxn,j}^\mathrm{cat}=\Delta S_{\rxn,j}^\mathrm{config/vib}+\Delta S_{e,j}(x)$ 형태로 — 전자 엔트로피의 닫힌식·발현 SOC·크기 근거화. forward 코드 일반화(H) 설계. **Gate**: `35_electronic_entropy_design.md`·Ch1 프레임 LCO 적용 명세·4-tier.

## Phase B (Track1 Ch1 v9 build) — Steps 18–44 [9종 competition-cherrypick]
- **B.1 (18–20)** spine = v8-11(흑연, 보존) + LCO 확장 명세(A.3) + ★**통계역학 1점 보강**(`CH1_statmech_review.md`): $\xi_\eq$ 를 *평형 점유 확률 분포*(단일 자리 $Z=1+e^{-\beta\Delta\mu}$, Ω=0 Fermi-함수형)로 명시하는 짧은 소절 — kinetic·thermo 두 경로를 *분포* 한 언어로 통합 + Ch2 분포 전개·LCO 전자(Fermi–Dirac) 엔트로피로 가는 다리. (그 외 통계역학은 v8-11 에 이미 완비 — W→Stirling→S_mix·μ(θ)·logistic 2경로·정규용액·spinodal — 보강 불요.) AUTHOR_BRIEF: 목표(Ch1 = Gr 음극 + LCO 양극 통합 하프셀 프레임), 보존(흑연 v8-11 불가침·결과식·부호), 추가(LCO 전이·전자 엔트로피 항·ξ_eq 분포 프레이밍), 부호·G-derive·그림 경쟁·자체 10회·KNOWN_DEFECTS.
- **B.2 (21–25)** 9종 독립(v9-01–03 Sonnet·04–06 Opus·07–09 Codex, **무통신**, 입력 = v8-11 + A 조사 근거). 단계적 참고문헌·그림 경쟁(v8-11 그림 후보+신규). master 검증·**커밋#1**.
- **B.3 (26–44)** 검토1(G-derive·부호·LCO 정합 렌즈)→방향성-만 보완→검토2(신규 회귀)→Opus 체리픽 **v9c**→adversarial 재검수→**Ch1 v9** 최종+정식 10회. 커밋#2(검토1+보완)·#3(체리픽)·#4(최종). **Gate**: xelatex 0-err·흑연 부분 v8-11 보존·LCO 추가 무비약·부호·전자 엔트로피 항 근거·G-usable.

## Phase C (Track2 통계열역학·분포 설계 선행) — Steps 45–52 [master + 서브(통계역학 문헌 sweep·검증)]
- **C.1 (45–47) 통계역학 spine 조사·설계**(★조사 규모 = master 직접 판단·포화): 분배함수→점유 분포→엔트로피 정전. 축 = ①격자기체/Bragg–Williams 분배함수·점유 분포(Ch1 logistic 의 *기원* 명시) ②configurational 엔트로피 $S_\mathrm{config}=-R\sum p\ln p$ ③**vibrational**(포논 Bose–Einstein 분포·고-$x$ 음 ΔS) ④**electronic**(Fermi–Dirac·LCO MIT — Ch1 v9 전자 엔트로피 항을 *분포로* 유도) ⑤상전이·order parameter(Ω>2RT 분포 bimodal·엔트로피 이상). seed = Newman·Huggins·통계열역학 정전 + intercalation lattice-gas 1차 문헌. **Gate**: `41_statmech_spine.md`(분포→엔트로피 유도·분해·출처·4-tier).
- **C.2 (48–52) 섞임/겹침·극한 수식 설계**(C.1 위에서):
  - **A**: 겹침 가중 $\partial U_\oc/\partial T(x)=\dfrac{\sum_j Q_jg_j\,\Delta S_{\rxn,j}}{F\sum_j Q_jg_j}$ — 음함수 미분(다전이 분포 중첩) 유도 + **Ch1 코드 수치 검증**(매끄러움·계단 부재·실측 비선형 재현).
  - 봉우리 내부 config: $\Delta S(\xi)=\Delta S_{\rxn,j}+R\ln[(1-\xi)/\xi]$(분포의 부분몰 엔트로피) 유도(★B: $\Delta S_{\rxn,j}$=중심 표준값, 이중계산 금지 명시).
  - **C**: $w$ vs $w_\eff(\Omega)$ 의 config 기여 차이(Ω-narrowing → 분포 폭·ΔS 모양). **D**: 히스 하 겹침(충/방전 분기 $U_j^d$ 별 ∂U/∂T·경로의존)=가역(평균)/비가역 분리.
  - **I**: 극한·코너 검산($\xi\!\to\!0,1$ config 발산·$\xi=\tfrac12$ 표준·$\Omega\!\le\!2RT$·단일봉우리 환원·고온 전자 엔트로피 $\propto T$)으로 "$\Delta S_{\rxn,j}$ 상수" 근사 타당성/한계($\Delta S_{\rxn,j}(x)$ 필요 여부) 확정.
  - **Gate**: `40_mixing_term_design.md` — 닫힌식·수치검증·B 해소·극한 통과·4-tier.

## Phase D (Track2 Ch2 v4 build) — Steps 53–79 [9종 competition-cherrypick]
- **D.1 (53–55)** spine = ★**통계열역학 챕터 골격**(C.1 분포 spine + C.2 섞임/겹침) — v3 는 *얇은 출발 skeleton* 으로만 참조(대폭 심화·구조 재편). BRIEF: 목표(Ch2 = intercalation 엔트로피·가역 발열 통계열역학 *제대로 된 챕터* — 분배함수→분포→엔트로피 유도·config/vib/electronic 분해·겹침 중첩·상전이·분포 재배열=가역 발열·피팅). 보존(v3 사슬·부호 결과). 추가(★분포 명시 전개·vibrational·electronic(Ch1 v9 전자 엔트로피를 분포로)·겹침 가중·w_eff·히스·극한). B 이중계산 금지·부호·G-derive(분포→엔트로피 무비약)·그림(분포·겹침·config 시각화)·자체 10회. ★Ch1 한 절이 아닌 *고유 챕터 면모*(분량은 통계열역학 전개의 자연 결과).
- **D.2 (56–60)** 9종 독립(입력 = C.1 spine + C.2 설계 + Ch1 v9 + v3 skeleton). 커밋#5.
- **D.3 (61–79)** 검토1(★분포 유도 무비약·통계역학 정합·부호·G-derive 렌즈)→보완→검토2→체리픽 **v4c**→재검수→**Ch2 v4** 최종+10회. 커밋#6~8. **Gate**: 0-err·분포→엔트로피 닫힌 유도 무비약·config/vib/electronic 분해 근거·겹침 수치검증·이중계산 0·극한 검산·G-usable·★*챕터급 충실도*(Ch1 한 절 아님).

## Phase E (종합) — Steps 80–82 [master]
- 양 트랙 `PHASE_2TRACK_RESULT.md`(11항목)·메타평가(LCO 확장·섞임 명시가 9-way 로 잘 됐나)·교수님 입력 갱신·다음(v10 통합·전셀). 커밋.

## Implementation Interfaces
- **(1) 9종 build = competition-cherrypick 스킬**: 독립 N(무통신·3모델)→검토1(G-derive/부호/정합 렌즈·refute)→방향성-만 보완→검토2(신규 회귀)→master 체리픽(이식금지 명문·그림 경쟁·단계적 참고문헌)→adversarial 재검수→정식 10회. 커밋 4회/트랙·푸쉬 X·Workflow X(Agent만)·Codex 단계구동+status/result 관찰.
- **(2) 조사·설계 = master + 서브(읽기 sweep 다세션 허용·비경쟁)**. 4-세션 고지·추출카드 schema·4-tier.
- **(3) Ch1 v9 LCO 명세(B baked)**: 전이별 $U_j^\mathrm{cat}(T)$·$\Delta S_{\rxn,j}^\mathrm{cat}$(표준)·logistic config·**전자 엔트로피 항 $\Delta S_{e,j}(x)$**(MIT @x≈0.5). forward 코드 일반화(H): 전이 파라미터 교체 + 전자 항 plug-in.
- **(4) Ch2 v4 통계열역학 챕터 명세**: ★분포 spine(분배함수→점유 분포→$S_\mathrm{config}=-R\sum p\ln p$, Ch1 logistic 기원)·vibrational(포논)·**electronic(Fermi–Dirac, LCO MIT)** 분해 + 겹침 가중식(A)·config 봉우리내(B)·$w_\eff(\Omega,C)$·히스(D)·극한(I). ξ·Ω·분포 든 닫힌식 명시. Ch1 한 절 아닌 챕터급 충실도.
- **(5) Result 11항목·Ledger 12-col·KNOWN_DEFECTS·부호 체크리스트** = 표준.

## Test Plan
- 각 build: xelatex 0-err·부호 사슬(v11/문헌 1:1)·G-derive 무비약·G-usable(이 문건으로 재현)·그림 영어 ASCII·base 보존(흑연 v8-11/Ch2 v3 무변)·정식 10회 수렴.
- ★Ch1 v9: LCO 전이 파라미터·전자 엔트로피 항 출처·흑연 부분 불변·하프셀 ∂U/∂T 산출 닫힘.
- ★Ch2 v4: 겹침 가중식 **Ch1 코드 수치 round-trip**(매끄러움·실측 비선형)·이중계산 0(중심 표준값)·극한 4건(ξ→0,1·Ω≤2RT·단일봉우리) 검산.
- 조사: 출처 폐쇄·삼각검증·4-tier·정독 증명.

## Assumptions
- LCO 하프셀 1차 문헌 다수 접근(불가분 tier 강등). LCO 가 같은 전이별 logistic 프레임에 적합(전자 엔트로피만 추가 — A.3 검증, 부적합 시 갭). Ch1 v8-11 흑연 결과는 확정(v9 는 확장만). 섞임 항은 모델로 유도 가능(문헌 보조). 9-way 토큰 비용 수용(사용자 전제).

## Correction History
- 2026-06-30 신규. 사용자 지시: Ch1 [확장]=LCO 양극(하프셀)·조사 선행·v8→v9·v10=교수님 / Ch2 [설명 추가]=섞임 항 명시·v3→v4 / 둘 순차·각 9종 병렬 / 전셀 범위 외 / 파생 F·H→Ch1, A·C·D·I→Ch2, B=본 답변서 해결(이중계산). 
- 2026-06-30 갱신(사용자 피드백): (a) Ch1 v9 = **통합 확장본**(v8 큰 틀 유지+양극 필요부만 추가, 단일 문건) (b) **전자 엔트로피=Ch1 본문**→Ch2 확장 순서 (c) **조사 규모=master 직접 판단**(사용자 지정 아님·포화 기준 명시) (d) ★**Ch2=통계열역학 *제대로 된 챕터***(분포 명시 전개·config/vib/electronic — v3 의 "Ch1+한 절" 수준 탈피).
- 2026-06-30 갱신2(사용자 검토): Ch1 v8-11 통계역학 *대체로 완비*(W→Stirling→S_mix·logistic 2경로) — 1점만 보강(ξ_eq 점유 *분포* 프레이밍, LCO 전자·Ch2 분포 다리). `CH1_statmech_review.md`.
- ★**GO 확정(2026-06-30): 무중단 완주**(사용자 출근·무피드백, 퇴근 전 완성). 서베이=master+병렬 읽기 sub, 빌드=9종 competition-cherrypick. 각 트랙 milestone 마다 커밋(컴팩션-안전). Track1(A→B: Ch1 v9) → Track2(C→D: Ch2 v4) → E 종합. 정지 5조건만.
