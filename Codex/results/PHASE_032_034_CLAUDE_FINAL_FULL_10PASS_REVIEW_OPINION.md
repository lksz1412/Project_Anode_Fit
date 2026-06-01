# PHASE 032-034 - Claude Final Full 10-Pass Review Opinion

## 0. 결론 요약

Claude 최종본은 **컴파일은 통과하고 Ch2~Ch5의 확장 논리에는 salvage 가치가 큰 부분이 많지만, 현재 상태를 그대로 canonical 또는 논문급 최종본으로 쓰기는 어렵다.** 특히 Chapter 1과 Chapter 3의 핵심 convention이 Codex에서 바로잡은 기준과 충돌한다. 가장 큰 문제는 다음 네 가지다.

1. `chi_j`를 Chapter 3의 transfer coefficient `beta_j`와 동일물로 못박는다. 이는 Chapter 1의 Level-A common-mode mobility sensitivity와 Chapter 3 Level-B directional transfer coefficient의 경계를 무너뜨린다.
2. Chapter 1 simple-fit Eyring 보정에서 `y(T)=ln(1/(L T))+chi_j A_j/(RT)`를 쓴다. `ln(1/L)` 안에 이미 `+chi_j A_j/(RT)`가 있으므로 plus 보정은 double counting이다.
3. `Heaviside H(L-L_min)`와 `A_L=delta(...)` 표현이 남아 있다. 사용자가 우려한 step-function식 인상과 amplitude 손실 문제가 다시 열린다.
4. 본문/제목/통합 노트에 `RB 재구성본`, `CHARTER`, phase/process metadata, `구 Chapter 6` 해체 내역이 남아 있다. 프로젝트 규칙상 변경 이력과 process label은 본문이 아니라 result/ledger/handover에 있어야 한다.

따라서 이 버전은 **그대로 채택: 비권장**, **부분 흡수: 권장**이다. Ch2~Ch5의 세부 유도 중 일부는 후속 chapter 작성 시 좋은 재료가 되지만, Chapter 1 baseline과 convention은 Codex V4 쪽을 기준으로 삼는 것이 더 안전하다.

## 1. 검수 대상과 source freeze

| File | Lines | SHA256 |
|---|---:|---|
| `Claude/docs/graphite_ica_ch1_rebuilt.tex` | 1627 | `4EB24D9C7C2080B5AEC556BE0E98C8E2E88923F28DC4DDBBDCD3E4CF82AE33AE` |
| `Claude/docs/graphite_ica_ch2_rebuilt.tex` | 947 | `365EABB0941496BABD1A21E2E4697597BE3C17AC30D1F553DF7EB99990B14B04` |
| `Claude/docs/graphite_ica_ch3_rebuilt.tex` | 915 | `918FAF4F64F352357308A3361EBCCAE36348CB19A28C188B7FD60F32082463E8` |
| `Claude/docs/graphite_ica_ch4_rebuilt.tex` | 1004 | `114CAFF228701ACC5BA4480AB1AE6FF8E391DCA7A45C0FE2A095F97E254FFB77` |
| `Claude/docs/graphite_ica_ch5_rebuilt.tex` | 999 | `605CA50987909B9774B191DF93F91C4EC8DB51143D797D1FCCA3CE157C31ACF6` |
| `Claude/docs/graphite_ica_full_rebuilt.tex` | 5141 | `A449B8F974A9567D9FC71EDCB5399A37119D1D578ED2F76214E411B13D4AC133` |
| `Claude/docs/graphite_ica_refs_rebuilt.tex` | 184 | `8C95D32D21E080AAB7A3CE41F65ADCD6E8E9A0CB863C633367673AAE12297617` |

## 2. 10-pass 검수 방식

Codex Chapter 1 V4 검수와 동일하게 서로 다른 chunk scheme을 적용했다. 본문 논리 검수의 중심 원천은 5141행 통합본이며, 개별 chapter 파일은 preamble/title/meta, standalone references, source-set consistency 확인에 사용했다.

| Pass | Chunk scheme | Chunks | Missing |
|---|---|---:|---:|
| P1 | chapter blocks: 1-139, 140-1627, 1628-2474, 2475-3280, 3281-4162, 4163-5039, 5040-5141 | 7 | 0 |
| P2 | fixed 300-line chunks | 18 | 0 |
| P3 | 175-line offset chunks | 30 | 0 |
| P4 | fixed 500-line chunks | 11 | 0 |
| P5 | fixed 125-line chunks | 42 | 0 |
| P6 | dependency-chain chunks | 12 | 0 |
| P7 | reverse 350-line chunks | 15 | 0 |
| P8 | risk-focus chunks | 9 | 0 |
| P9 | fitting-logic chunks | 8 | 0 |
| P10 | full sweep 1-5141 | 1 | 0 |

## 3. 정적 검증 및 컴파일 결과

### 3.1 Label/ref/cite

| File | labels | duplicate labels | refs | missing refs | cites | bibs | missing cites | unused bibs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Ch1 | 89 | 0 | 246 | 0 | 62 | 27 | 0 | 0 |
| Ch2 | 62 | 0 | 131 | 0 | 18 | 10 | 0 | 0 |
| Ch3 | 50 | 0 | 162 | 0 | 10 | 10 | 0 | 3 |
| Ch4 | 48 | 0 | 138 | 0 | 9 | 10 | 0 | 4 |
| Ch5 | 54 | 0 | 157 | 0 | 4 | 9 | 0 | 7 |
| Full | 309 | 0 | 834 | 0 | 103 | 33 | 0 | 0 |
| Refs | 1 | 0 | 0 | 0 | 0 | 33 | 0 | 33 |

판단: 통합본 기준 label/ref/cite gate는 PASS다. 개별 Ch3~Ch5 unused bib는 standalone chapter bibliography 청소 문제이며 논리 오류는 아니다. `refs_rebuilt`의 unused bib 33개는 standalone bibliography 문건 성격상 자연스럽다.

### 3.2 XeLaTeX fresh compile

Target: `Claude/docs/graphite_ica_full_rebuilt.tex`

- Pass 1 exit: 0
- Pass 2 exit: 0
- Pass 3 exit: 0
- PDF: `C:\Users\lksz1\OneDrive\문서\New project\_texcheck_claude_final_full\graphite_ica_full_rebuilt.pdf`
- PDF bytes: 1110270

Log scan:

| Item | Count | 판단 |
|---|---:|---|
| LaTeX Error | 0 | compile PASS |
| Undefined control sequence | 0 | PASS |
| Undefined references | 0 | PASS |
| Undefined citations | 0 | PASS |
| Rerun requested | 0 | PASS |
| Missing character | 3 | 조판 품질 문제 |
| Hyperref PDF-string warnings | 284 | bookmark/title math cleanup 필요 |
| Overfull hbox | 31 | 조판 품질 문제 |
| Underfull hbox | 41 | 조판 품질 문제 |
| Font warnings | 6 | 한글 italic/font fallback |

판단: 기술적으로 PDF는 생성된다. 그러나 출판용 PDF 품질 gate는 PASS로 볼 수 없다.

## 4. Severity Findings

### Critical 1 — `chi_j`와 `beta_j` 동일시가 Chapter 1/3 경계를 붕괴시킨다

근거:

- Full line 202: `chi_j`를 `Ch.3 transfer coefficient beta_j 와 동일물`로 정의.
- Full line 2499: Chapter 3 서두에서 `chi_j equiv beta_j`를 명시.
- Full lines 2747-2748: Level B 도입 시 `chi_j`가 `beta_j`와 동일물이 된다고 단정.
- Full line 3211: 자체 검수표에서 이를 PASS로 선언.

문제:

Chapter 1의 `chi_j A_j`는 Level-A에서 relaxation mobility scale을 common-mode로 바꾸는 scalar sensitivity로 쓰여야 한다. 반면 `beta_j`는 forward/backward barrier를 비대칭으로 나누는 Level-B transfer coefficient다. 둘을 동일물로 못박으면 “방향 없는 tail relaxation acceleration”과 “방향 있는 charge-transfer split”이 같은 물리량이 되어, Chapter 1의 fitting parameter와 Chapter 3의 electrochemical kinetic parameter가 공선형으로 무너진다.

개선 방향:

- Chapter 1: `chi_j`는 `Level-A scalar relaxation-barrier sensitivity`로 고정.
- Chapter 3: `beta_j`를 새로 정의하고, `chi_j -> beta_j` mapping은 추가 kinetic model, detailed-balance split, small-driving-force limit, 동일 driving coordinate가 모두 성립할 때의 `conditional correspondence`로만 둔다.
- 자체 검수표의 “동일물 PASS”는 삭제하거나 “conditional mapping only”로 바꾼다.

### Critical 2 — Eyring 보정식의 부호가 잘못되어 potential assistance를 두 번 더한다

근거:

- Full line 839: `y(T)=ln(1/(L T))+chi_j A_j(T)/(RT)`.
- Full lines 841-849: `chi_j`는 (3)에서 먼저 얻는다고 쓰지만, 문서 순서는 (2)에서 이미 보정식에 `chi_j`를 사용한다.

문제:

`L = |I|/(Q_cell k_0) exp[(G-chi_j A_j)/(RT)]`이므로 `ln(1/L)`에는 이미 `+chi_j A_j/(RT)` 항이 들어 있다. 순수 `Delta H_a`를 회귀하려면 이 항을 빼야 한다. plus로 더하면 potential-assisted barrier lowering을 double count한다.

개선 방향:

- `y(T)=ln[1/(L T)] - chi_j A_j(T)/(RT)`로 수정.
- extraction order를 `OCV/GITT stage/R_n 고정 -> L 추출 -> chi_j 추출 -> chi_j 고정 후 Eyring-corrected Delta H_a`로 재배치.
- “(2)↔(3) 닭-달걀 아님”이라는 선언은 수식 순서 자체를 바꾼 뒤에만 성립한다.

### Critical 3 — `Heaviside H(L-L_min)`는 사용자가 우려한 step-function 인상을 되살린다

근거:

- Full lines 561-564: support를 Heaviside로 부착한다고 설명.
- Full line 578: `A_L(L)` boxed 식 안에 `H(L-L_min)` 포함.
- Full line 1077: Ch1 부록 B에도 `H(L-L_min)`가 반복된다.

문제:

수학적으로 support indicator는 쓸 수 있지만, 이 프로젝트의 사용자 기준에서는 step-function식 급변/절단으로 오해될 수 있는 표현을 피해야 한다. 특히 `effective barrier`의 continuous lowering을 전개하는 문서에서 `H`를 본식에 넣으면 “장벽을 넘으면 0에서 1로 뛴다”는 이전 오류의 인상을 다시 만든다.

개선 방향:

- `L in [L_min, infinity)`를 정의역으로 선언.
- 적분을 `int_{L_min}^{infty}`로 쓰고, 본문에서 `G>=0`의 domain condition임을 설명.
- `H`는 수치 구현용 indicator로만 부록에 격리하거나 아예 제거한다.

### Critical 4 — 단일 mode spectrum에서 amplitude가 사라진다

근거:

- Full line 614: `single-mode ... A_L=delta(L-L*)`.
- Full line 814: simple-fit 극한 `A_L=delta(L-L_0)`.
- Full line 1158: grid check에서도 `A_L=delta(L-L_0)`.

문제:

앞에서는 `A_L`를 amplitude spectrum으로 정의한다. 그러면 single-mode 극한은 `A_L(L)=Theta_0 delta(L-L*)` 또는 amplitude factor를 포함해야 한다. `delta`만 쓰면 총 진행량/면적/진폭이 1로 고정되어, 실제 ICA tail amplitude 또는 transition capacity가 사라진다.

개선 방향:

- 확률 spectrum이면 `A_L^{prob}=delta(...)`라고 명시.
- 관측 amplitude spectrum이면 `A_L^{amp}(L)=A_* delta(L-L*)` 또는 `Theta_0 delta(...)`로 쓴다.
- simple-fit 절의 nuisance amplitude `A`와 일관되게 연결한다.

## 5. High Findings

### High 1 — 본문에 process metadata와 변경 이력이 남아 있다

근거:

- Full lines 1-20: file generation note, RB Phase, Ch6 해체, Date/Author.
- Full lines 105-110: title/author/date에 `RB 재구성본`, 날짜가 노출.
- Full lines 5122-5139: 통합 노트가 body 안에서 병합 메타를 설명.
- Pattern counts: Full `RB 재구성본=8`, `CHARTER=66`, `Date:=1`, `Author:=1`.

문제:

프로젝트 지침상 작업 날짜, phase, audit, commit, 변경 이력은 본문이 아니라 result/ledger/handover에 있어야 한다. 논문 또는 특허 후보 문건으로 보려면 `RB`, `CHARTER`, `Phase`, `구 Ch6 해체` 같은 운영 흔적은 제거해야 한다.

개선 방향:

- TeX 본문에서는 scientific title/abstract만 유지.
- `통합 노트`는 Codex/Claude results의 build report로 이동.
- `CHARTER step`은 물리적 명칭으로 치환한다. 예: `sign convention`, `driving-potential convention`, `detailed-balance consistency`.

### High 2 — Chapter 1이 theoretical background와 fitting workflow/solver appendix를 과도하게 한 몸에 넣었다

근거:

- Full line 944부터 Ch1 부록 B가 시작되어 1580행까지 fitting workflow, DAE, direct g-grid, Plan A tolerance, no-free parameter set, OCV/GITT/Arrhenius/C-rate workflow를 포함한다.
- `sec:ch6_` label이 full에 100개 남아 있다.

문제:

사용자의 핵심 요청은 현재 “수식 논리 전개와 이론적 배경”이며 solver 구축이 아니다. Claude 버전은 구 Ch6를 Ch1에 통째로 흡수해 Chapter 1의 초점을 흐린다. 내용 일부는 유용하지만 Chapter 1 본문 안에 전부 넣으면 독자가 핵심 인과 사슬을 따라가기 어렵다.

개선 방향:

- Chapter 1에는 theory + simple-fit approximation + bounded Plan A/B statement까지만 둔다.
- fitting workflow, DAE, solver tolerance, no-free parameter set은 별도 “Fitting Methodology Appendix” 또는 후속 methods chapter로 분리한다.
- `sec:ch6_` label namespace는 `sec:fit_` 또는 `app:fit_`로 재정리한다.

### High 3 — 자체 검수표가 실제 본문 상태를 과신한다

근거:

- Full lines 1549, 3228, 4095, 4969: `자명/clearly/쉽게/obviously 본문 0건`을 PASS로 선언.
- 실제 pattern scan에서는 해당 문자열이 self-check와 comments에 남아 있다. 더 중요한 것은 self-check가 Critical 1~4를 PASS로 선언하거나 포착하지 못한다는 점이다.

문제:

검수표가 “검수했다”는 선언을 문서 안에 남기지만, 실제로는 핵심 convention 충돌과 fitting sign error를 통과시킨다. 논문 본문에 자체 검수표를 넣는 것도 부자연스럽고, 검수 기록은 별도 report에 있어야 한다.

개선 방향:

- 자체 검수표는 본문에서 제거하고 result/ledger로 이동.
- 검수표를 남길 경우 `PASS` 대신 evidence link와 line-specific check를 별도 문건에 둔다.

### High 4 — bibliography placeholder가 남아 있다

근거:

- Full line 5084: 사용자 논문 title이 `\dots reaction-diffusion / first-passage ratio-substitution closure` placeholder.
- Full line 5086: Ref. 6 title이 `Propagator / ratio-substitution method` placeholder.
- Full line 5088: Ref. 7 title이 `Ratio-substitution closed-form` placeholder.
- Refs rebuilt에도 같은 placeholder가 남아 있다.

문제:

사용자 논문과 ref. 6, 7은 이 프로젝트의 self-consistent integral closure 근거다. 이 서지가 placeholder이면 핵심 근거가 논문급 문건 기준을 만족하지 못한다.

개선 방향:

- JCP 2017: “Effects of External Electric Field and Anisotropic Long-Range Reactivity on Charge Separation Probability”.
- Lee 2011: “Communication: Propagator for Diffusive Dynamics of an Interacting Molecular Pair”.
- Son 2013: “An Accurate Expression for the Rates of Diffusion-Influenced Bimolecular Reactions with Long-Range Reactivity”.
- refs rebuilt와 통합본 bibliography를 동시에 정정한다.

### High 5 — `n_eff=RT/(F w_j)` reconcile가 Chapter 1의 affinity scale 충돌을 드러낸다

근거:

- Full lines 2830-2869: Chapter 3에서 detailed-balance 정합으로 `n_eff=RT/(F w_j)`를 도출하고, Ch1은 `n_eff=1` 원형에 effective `w_j`를 함께 썼다고 설명한다.

문제:

이 절 자체는 정직하게 문제를 드러낸다는 장점이 있다. 그러나 그 결과는 “Chapter 1의 `A_j=s_phi F(V-U)`와 effective `w_j`는 nonideal width에서 그대로 쓰면 정합하지 않는다”는 뜻이다. 즉 Chapter 1과 Chapter 3이 동시에 canonical이 되려면 Chapter 1부터 affinity scale convention을 정리해야 한다.

개선 방향:

- Chapter 1에서 ideal-width form과 effective-width form을 분리한다.
- `A_j=s_phi n_eff F(V_drive-U_j)`를 일반형으로 두고, Ch1 simple form은 `n_eff=1` 또는 `w_j=RT/F`인 ideal limit로 명확히 제한한다.
- 또는 Chapter 1의 `chi_j A_j`를 Level-A phenomenological scalar로 두고, Ch3의 `n_eff` 일반형과는 mapping 조건을 별도로 둔다.

## 6. Medium Findings

1. Full에는 `$$` 인접 delimiter가 22건 남아 있다. 이는 수식 실패는 아니지만 LaTeX source 품질이 낮고 유지보수 중 오류를 만들 수 있다.
2. Full에는 `AL{9}`가 2건 남아 있어 기존 assumption ledger numbering과 충돌/구버전 잔재 가능성이 있다.
3. `구 Chapter 6`, `Ch6`, `Ch.6` 표현이 통합본과 refs에 남아 있어 독자에게 현재 구조가 Chapter 1~5인지 Chapter 1~6인지 혼란을 준다.
4. `Heaviside`는 Ch2~Ch5 preamble comments에도 “금지” 문맥으로 남아 있다. 주석이라 물리 오류는 아니지만 본문 deliverable에는 운영 규칙 주석 자체가 불필요하다.
5. Ch2의 thermal mirror hypothesis는 좋은 아이디어이나, calorimetry 없이는 novel hypothesis/consistency로만 둬야 한다. 문서가 이를 flagbox로 제한한 점은 좋지만, Chapter 2 결론에서 과도하게 확정적으로 읽히지 않게 조심해야 한다.
6. Ch5 full-cell voltage decomposition은 유용하지만 `eta_loss^b`, 양극/음극 apparent decomposition, polarization/true hysteresis 분리는 실험 설계 없이는 식별 불가능하다. 현재도 bound가 있으나, 후속 문건에서는 decision queue로 더 강하게 분리해야 한다.
7. Hyperref warning 284건은 section title에 수식이 너무 많다는 신호다. PDF bookmark 품질까지 보려면 `texorpdfstring` 또는 짧은 heading이 필요하다.

## 7. 잘된 점

1. Ch2~Ch5는 “무비약”을 의식한 중간 유도와 조건부 bound가 많이 들어가 있다.
2. Ch4의 transition-level entropy production에서 `n_eff I_j eta_j`로 가는 미시-거시 유도는 조건을 명시한 점이 좋다.
3. Ch5의 충전 branch sign derivation은 `s_phi^chg=-1`, `I_j<0`, `eta_j^chg<0`, product positive로 이어지는 설명이 비교적 명확하다.
4. `R_n`, `R_ct`, `R_n,eff`를 구분하려는 노력은 전체 chapter 간 식별성 측면에서 중요하다.
5. 통합본 label/ref/cite gate는 깨끗하다. 통합 빌드도 3-pass 성공했다.
6. Ch2 thermal-tail mirror, Ch4 entropy-production heat, Ch5 hysteresis loop decomposition은 후속 chapter 개발 재료로 흡수 가치가 있다.

## 8. 권고안

### 권고 1 — Chapter 1 canonical은 Codex V4를 기준으로 삼는다

Claude Ch1은 중요한 내용을 많이 담았지만 Critical 1~4 때문에 현재 canonical baseline으로 쓰기 어렵다. Chapter 1은 Codex V4의 convention을 기준으로 삼고, Claude Ch1의 좋은 설명만 선별 흡수하는 편이 안전하다.

### 권고 2 — Claude Ch2~Ch5는 “재료 문건”으로 보존한다

Ch2~Ch5는 완전히 버릴 문건은 아니다. 특히 Ch4/Ch5는 구조적 장점이 있다. 다만 본문 내 `CHARTER`, `RB`, `동일물`, `$$`, self-check table, process label을 제거하고 Chapter 1 convention과 맞춘 뒤에야 재사용 가능하다.

### 권고 3 — Fitting workflow appendix는 별도 문건으로 분리한다

Ch1 부록 B에 흡수된 구 Ch6 내용은 fitting methodology 문건으로는 가치가 있다. 하지만 Chapter 1 theoretical background에는 과하다. 별도 `Fitting Methodology` 또는 `Appendix: numerical/identifiability workflow`로 분리하는 것이 낫다.

### 권고 4 — 수정 우선순위

1. `chi_j`/`beta_j` convention 재정의.
2. Eyring correction sign/order 수정.
3. `Heaviside` support와 amplitude-less delta 정리.
4. bibliography placeholder 정정.
5. process metadata와 self-check table 제거.
6. Ch1/Ch3 `n_eff`/`w_j`/affinity scale convention 통일.
7. TeX delimiter, hyperref bookmark, overfull/missing character cleanup.

## 9. 최종 판단

- Compile/build 관점: PASS with warnings.
- Reference integrity 관점: 통합본 PASS.
- 논문급 본문 품질 관점: FAIL until Critical 1~4 are repaired.
- 후속 개발 재료 가치: HIGH, 특히 Ch2~Ch5.
- 즉시 canonical 채택: 비권장.
- 선별 흡수 후 재작성: 권장.
