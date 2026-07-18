# v1.0.23 Plan — 사용자 Fredholm-2종 ratio 방법 접목 + 고등수학 Tier1-2 (부록 E + 코드)

> 작성 2026-07-18. 표준 11-section 양식([[feedback_plan_template_11sections]]). cumulative step 단조 증가(P0=1-3 완료·다음=4).
> 근거 = 사용자 논문 JCP **147**(14) 144111 (2017) 전문 정독 + v1.0.22 문건·코드 실측 + comp_v23 서베이 4창·조건검수.
> 성격 = **계획서**(GO 대기·[[feedback_planning_vs_execution]]). 실행 phase 미착수.

---

## Summary

**목표.** v1.0.22(완결·검증종료)를 승계한 v1.0.23 에, 사용자 논문의 간판 기법 = **되먹임 적분방정식(Fredholm 2종)의 미지량 자기참조를 특정 ratio 로 치환해 닫는 방법**을, 문건의 자기일관(되먹임) 구조에 **정직하게** 접목한다.

**왜.** v1.0.22 는 dQ/dV·DVA 를 열역·동역학으로 닫았으나 자기일관 구조(P3-3/P3-4)를 전부 **수치 유일근** 또는 **동결(frozen) 근사**로 처리한다. 사용자 기법은 그 되먹임 층을 **닫힌형(또는 1차 보정)** 으로 승격시키고, 무엇보다 **언제 그 근사가 신뢰되는가**를 논문 Sec.III 근거로 부등식화(P3-5 이행)한다.

**이번 계획이 다루는 범위.** (1) 접목이 실제로 성립하는 **단 하나의 자리**(동역학 lag)만 접목하고 성립 안 하는 자리(대수근 I·III)는 "적용 불가"로 본문에 명시. (2) 수학 해법은 **부록 E** 에 두고(사용자 결정: "본문의 수식을 푸는 기법"), **실제 적용은 코드**에 한다(본문 코드언급 금지·부록 예외 준수). (3) 서베이 4창이 확정한 **Tier 1 코어**(#0 Fredholm ratio + Laplace 전달함수) + **Tier 2 옵션**(Fisher 정보기하)만 채택하고 기각군은 non-goal 로 정직 표기.

**핵심 정직 프레임(P1 조건검수 결론).** 문건의 lag 은 이미 **값싼 O(N) 전방 ODE**(지수핵=Markov)라 "계산 절감"은 셀링포인트가 못 된다. 접목의 참 가치는 **(a) 동결 0차 위의 해석적 1차 닫힘 + (b) 그 닫힘이 언제 유효한지 증명하는 타당성 인증서(validity certificate)**다. 과장 금지가 이 문건의 v1.0.22 대비 차별점.

---

## Current Ground Truth

**확인된 사실 (원천 실측).**
- v1.0.22 = **완결·검증 종료**. 4창 적대적 검수 치명 0·C-056 마감. 3장 GREEN(ch1 83p·ch2 25p·ch3 17p, err0/undef0), 게이트 exit0 bit-exact max|d|=0.0. → v1.0.22 는 **닫힌 문건**(수정 금지·Non-goals).
- **P0 완료(PASS·ledger 확정)**: `Claude/docs/v1.0.23/` 골격 = v1.0.22 3장·코드·test·_sections·appendix·FITTING_GUIDE 승계. 버전 결합(common_preamble_v1022→v1023·externaldocument·test CODE 경로) 갱신. GREEN baseline 재현(3장 err0/undef0·83/25/17p·게이트 exit0 bit-exact·구조 PASS). cumulative step **1-3 소진·다음 = 4**.
- **사용자 논문 방법론(원문 Eq. 번호 근거·기억 아님)**: 지연 재결합쌍 궁극 분리확률 W̄_u(r) 의 **제2종 Fredholm** Eq.(32) `1 − W̄(r) = ∫K(r,r₁)W̄(r₁)dr₁` → 3단: **(33)** 양변 W̄(r) 나눠 미지량을 **비 W̄(r₁)/W̄(r)** 로만 남김 → **(34/37)** 그 비를 더 단순·가해(δ-싱크, 닫힌형 Eq.25) 기준문제의 비 W̄⁰(r₁)/W̄⁰(r) 로 치환 → **(39)** 닫힌형. 물리 근거 = **함수보다 비가 근사에 훨씬 둔감**.
- **적용 조건(논문 Sec.III·line 380-388)**: (i) 비등방 섭동 K 과대 아님, (ii) 온사거 척도 r_c 가 초기분리 대비 지배적, (iii) 접촉 반응성 σ 작음(싱크 단거리). **"반응대 넓어지면 근사 악화"** — 명시적 열화 조건.
- **문건 자기일관 구조 3종 vs 기법 요구** (comp_v23/COND_AUDIT.md 예비 판정):

  | # | 구조 | 위치 | 형태 | 현행 | 기법 정합 |
  |---|---|---|---|---|---|
  | I | 전하보존 U_oc 반전 | eq:sm-mc-balance·eq:blend-balance | 초월 **대수** | 수치 유일근 | **✗** 적분핵 없음·이미 저렴·정확 |
  | II | **동역학 lag** | eq:Lq + `_causal_memory` | **Volterra**(인과 합성곱) | **L_V 동결 0차·선형 합성곱** | **◑ 최강 정합** — 참 문제 L_V=L_V(ξ)(Ω(1−2ξ) 경유) 비선형 자기일관을 동결로 우회 |
  | III | 배경 자기일관(P3-3) | q=Q_bg(V_n)+ΣQ_jξ_j | 대수 순환 | 수치 | **✗** I 과 동류 |

- **코드 실측(동결 증거)**: `func_L_q(T,I,Q_cell,dH_a,dS_a,x,A)` 는 affinity A 를 **입력으로 동결**해 받음. `_causal_memory_pointwise(V_prog, ksi_eq, lag_length)` 는 **상수 lag_length** → 선형 합성곱 = 0차. 즉 가해 기준(0차)이 **이미 코드에 존재** → 논문 Eq.34 철학의 "가해 기준"이 자연 확보돼 있음.

**예비 산출물(P1 재확정 대상).**
- `comp_v23/COND_AUDIT.md` — 조건검수 예비 분석(PASS + reframe 권고). **P1 에서 마스터 재유도 검산으로 정식화**(현 상태 = 예비).
- `comp_v23/SURV1-4_*.md` + `SURV_SYNTHESIS.md` — 고등수학 서베이 4창 종합(Tier 랭크 확정).

**미확인 사항 (추정 금지·명시).**
- **Ref.6·7 원문 미소장**: Ref.6 = S. Lee, C. Y. Son, J. Sung, S. Chong, *JCP* **134**, 121102 (2011); Ref.7 = C. Y. Son 외, *JCP* **138**, 164123 (2013). JCP147 은 이 둘을 **적용**만 하고 원 유도는 6·7. → P1 에서 원문 확보 여부 판단, 미확보 시 **JCP147 자족 기술로 진행·정직 표기**.
- Volterra(인과 1방향)↔Fredholm(양방향 커널) **재유도 등가성**: 1차 보정의 수렴·오차한계가 P1 검산 통과해야 본체 유지(불통과 시 교육적 예시로 강등).

---

## Phase Range

| Phase | 이름 | Steps(cumulative) | 게이트 요지 | 상태 |
|---|---|---:|---|---|
| **P0** | 셋업·골격 복제 | **1-3** | 3장 GREEN·게이트 bit-exact·구조 PASS | **PASS(완료)** |
| **P1** | 조건검수 게이트 | **4-8** | 마스터 재유도 검산 통과·타당성 부등식·동결극한 회수 | 대기 |
| **P2** | 부록 E 저작 | **9-15** | 재빌드 GREEN·구조 PASS·P3-5 5항·warnbox·본문 코드언급 0 | 대기 |
| **P3** | 코드 적용(ratio 옵션) | **16-20** | 동결 off=기존 bit-exact·신옵션 수렴·수식↔코드 정합 | 대기 |
| **P4** | Tier2 선택 확장 | **21-24** | (사용자 택) Fisher 정보기하·Legendre 명명노트·재빌드 GREEN | 대기(옵션) |
| **P5** | 마감·적대검수 | **25-28** | 치명 0·3장 GREEN·게이트 exit0·HANDOVER | 대기 |

> Phase = v1.0.23 챕터 귀속(1챕터=1Phase 아님·각 Phase 다중 step). step 번호 phase 넘어가도 재시작 X([[feedback_plan_template_11sections]] §4).
> `ver.1~ver.5`(역사적 파일 이력) ↔ `Chapter 1~5`(구조 명칭) ↔ `P0~P5`(작업 phase) — **셋은 서로 다른 축**(프로젝트 검수 7항 #7).

---

## Non-goals

- **v1.0.22 수정 X** — 완결·검증종료 문건. read only(비교 기준). 모든 저작은 `docs/v1.0.23/`.
- **Fredholm 기계장치 리터럴 복붙 X** — 문건에 제2종 Fredholm 방정식이 **없다**. 대수근 I·III 에 이 기법 이식 **금지**(이미 저렴·정확). "적용 불가"를 부록 E 서두에 명시.
- **본문(챕터 본체)에 수학 해법·코드 언급 X** — 해법은 부록 E, 코드 적용은 `.py`. 본문은 물리 서사만 + 부록 포인터 1줄(부록·참고 예외 규정 준수).
- **"계산 절감" 셀링 X** — lag 은 이미 O(N) 전방 ODE. 절감 아닌 **해석적 닫힘 + 타당성 인증**으로만 프레이밍.
- **기각 서베이군 채택 X**(non-goal 본문 정직 표기): Wiener-Hopf·WKB·다중척도·중심다양체·Langevin·Preisach 연산자채택·Kubo 동적 χ(가정충돌 경고).
- **역문제(inverse) 방향 X** — Tikhonov·MaxEnt·Bayes deconvolution 은 forward-only 선언과 충돌 → **v1.0.24 동반문건 후보**(이번 스코프 밖).
- **병합 빌드 X**(D22-8) — 3장 분리 빌드·xr 교차참조 유지.
- **사용자 승인 전 실행 금지** — 본 계획서는 GO 대기. Decisions Required 확정 전 P1 착수 X.

---

## Implementation Changes

**신설·수정 문서/코드 (docs/v1.0.23/ 내부 한정).**
- **부록 E(신설)** "자기일관 해법 — ratio 닫힘과 전달함수" — `_sections/` 신규 파일, ch1_graphite 부록군 말미(부록 letter 순 편입).
  - E.1 lag Volterra 자기일관 + 동결 0차 기준(현행 코드 대응)
  - E.2 Fredholm-2종 ratio 닫힘(사용자 Ref6·7) + **P3-5 5항 sub-section** + 타당성 부등식 + warnbox(열화)
  - E.3 Laplace 전달함수(동결 기준해 주파수형·기기응답·FFT)
  - E.4 코드 대응 지도(부록 수식 ↔ `.py` 함수)
- **본문 포인터(신설 절 아님)**: `ch1_sec08_lag.tex` 말미 1줄 "해석적 닫힘·수치 해법 → 부록 E". §7 전달함수 물리 1문장은 Decisions Required D2.
- **bib**: Ref.6·7 + JCP147 등재(P1 서지 검증 선행).
- **코드** `Anode_Fit_v1.0.23.py`: `func_L_q`/`_causal_memory` 에 **ratio 보정 옵션** + 전달함수(FFT) apparent-dQ/dV 경로. **동결 경로 off = 기존 bit-exact 유지**.
- **test**: 신옵션 수렴·동결 bit-exact 게이트 신설(기존 게이트 exit0 불변).
- **(옵션 P4)** Fisher 정보기하 = FITTING_GUIDE 확장 or 부록 소절.

**원장·결과 문서.**
- `results/V1023_EXECUTION_LEDGER.md`(12-col·승계·P1~P5 row 추가) · `V1023_CHANGE_LOG.md` · `V1023_REFERENCE_LEDGER.md`.
- **phase별 Result 11항 문서** `results/PHASE_P{1..5}_RESULT.md`([[feedback_phase_execution_loop]] 양식·다음 phase 진입 전 저장 필수).
- `comp_v23/COND_AUDIT.md`(P1 재확정) · P5 검수 4창 · `MERGE_READINESS_v23.md` · `HANDOVER_v23.md` · `INDEX`.

---

## Phase 1 — 조건검수 게이트 (Steps 4-8)

집행 전 정식 검증. **여기 통과 못하면 본체 저작(P2) 착수 금지.**

- **Step 4**: II lag 을 **Volterra→ratio 형식**으로 재유도. 참 lag(L_V=L_V(ξ))/동결 lag(L_V=const) 의 비를 논문 Eq.37 꼴로 세우고, 1차 보정식 도출.
- **Step 5**: **타당성 부등식** 도출 — `ε ≡ 2·χ_d·(Ω/RT)·Δξ_supp ≪ 1`, `Δξ_supp ≈ L_V/(4w)`. 논문 (i)(ii)(iii) ↔ 문건 조건 **1:1 대응표** 작성(Picard/ratio 수축률과 일치 확인).
- **Step 6**: **동결극한 회수 증명** — L_V=const 대입 시 ratio 보정식이 기존 선형 합성곱해로 **정확 회수**(닫힘 무결성). 해석 + 수치 대조.
- **Step 7**: **Ref.6·7 원문 확보 여부 판단**(미확보 시 JCP147 자족 기술 경로 확정) + 서지 정밀 검증(하이쿠 하위작업).
- **Step 8**: `comp_v23/COND_AUDIT.md` 정식화(유도·부등식·적용/불가 판정) + **마스터 검산 게이트** + `PHASE_P1_RESULT.md`(11항) + ledger P1 row.
- **입력**: jcp_extract.txt·ch1_sec08_lag.tex·`Anode_Fit_v1.0.23.py`(func_L_q·_causal_memory)·SURV_SYNTHESIS.md.
- **게이트**: 마스터 재유도 검산 통과 + 부등식 (i)(ii)(iii) 대응 명시 + 동결극한 회수 확인.
- **중단 조건**: 1차 보정 수렴·오차한계 검산 불통과 → 본체 축소·교육적 예시로 **강등** 보고(과장 이식 방지).
- **다음 phase 조건**: 게이트 PASS + Result 저장.

## Phase 2 — 부록 E 저작 (Steps 9-15)

- **Step 9**: 부록 E 골격(E.1~E.4) 신규 `_sections` 파일 + ch1_graphite 부록군 편입(letter 순).
- **Step 10**: E.1 lag Volterra 자기일관 + 동결 0차 기준 서술. **Prof. 이상엽 convention**: 동결 0차(원형) 식 **먼저** 제시 → 그 위에 ratio 보정(상호작용 항 추가) 식 제시.
- **Step 11**: E.2 Fredholm ratio 닫힘 + **P3-5 5항**(①서지 ②논문 내 위치 page·para ③원 방법 수학구조 ④변수 매핑 ⑤물리 가정 차) 별도 sub-section.
- **Step 12**: E.2 warnbox(열화 조건 = 타당성 부등식) + **적용 불가(I·III) 정직 명시** 서두 박스.
- **Step 13**: E.3 Laplace 전달함수 `H(ω)=1/(1+iωL_V)`·`dQ/dV_app=H·dQ/dV_eq`·기기응답 저역통과·FFT. convention 동일(동결 선형해=원형 → 전달함수 형).
- **Step 14**: E.4 코드 대응 지도 + bib Ref6·7·JCP147 등재 + 본문 포인터 1줄(§8 말미).
- **Step 15**: 3장 재빌드 + 구조 검사 + `PHASE_P2_RESULT.md` + ledger P2 row.
- **게이트**: 재빌드 err0/undef0·83+/25/17p·boxed 무파손·구조 PASS·**본문 코드언급 0**(부록·포인터 예외만)·수식↔(P3 예정)코드 정합 예약.
- **중단 조건**: 재빌드 error 또는 구조 회귀 → 저작 롤백·원인 문서화.
- **다음 phase 조건**: GREEN + Result 저장.

## Phase 3 — 코드 적용 (Steps 16-20)

수학 기법의 **실제 적용**(사용자 결정: "제대로 적용은 코드").

- **Step 16**: `func_L_q` 에 ratio 보정 옵션(신 인자·기본 off). off = 기존 동결 경로 **bit-exact**.
- **Step 17**: `_causal_memory` 계열에 전달함수(FFT) apparent-dQ/dV 경로 추가(E.3 대응).
- **Step 18**: 신옵션 수렴 테스트 + **동결=기존 bit-exact 게이트** 신설(기존 게이트 exit0 불변 확인).
- **Step 19**: 코드 ↔ 부록 E 수식 **정합 확인**(E.4 지도 대조·P2 예약 게이트 해소).
- **Step 20**: `PHASE_P3_RESULT.md` + ledger P3 row + CHANGE_LOG.
- **게이트**: 기존 게이트 exit0 유지 + 동결 off max|d|=0.0 + 신옵션 수렴 + 수식↔코드 1:1.
- **중단 조건**: 동결 bit-exact 깨짐 → 옵션 격리 실패로 롤백.
- **다음 phase 조건**: 게이트 PASS + Result 저장.

## Phase 4 — Tier2 선택 확장 (Steps 21-24, 옵션)

Decisions Required D3 승인 시에만.

- **Step 21**: Fisher 정보기하(3온도점+피팅 공선형+과식별을 sloppy-model 식별성으로 통일) — FITTING_GUIDE 확장 or 부록 소절(방법론층 격리·forward 모델 불변).
- **Step 22**: (택) Legendre-Fenchel 볼록쌍대 명명노트 — 반전 유일성=볼록성 엄밀화(신규 물리 아님·명명층).
- **Step 23**: 재빌드 GREEN + 신규 서지 검증.
- **Step 24**: `PHASE_P4_RESULT.md` + ledger P4 row.
- **게이트**: 재빌드 GREEN·forward 모델 무변경·신규 서지 무날조.
- **다음 phase 조건**: GREEN 또는 D3 미승인 시 skip.

## Phase 5 — 마감·적대검수 (Steps 25-28)

- **Step 25**: 독립 **적대적 검수 4창**(AUD 재판·프로젝트 검수 7항 + 신규 게이트) — 다중 에이전트 per-section(~500행/창·[[feedback_multiagent_review_chunking]]).
- **Step 26**: `MERGE_READINESS_v23.md` 갱신 + 치명 잔여 0 확인.
- **Step 27**: `HANDOVER_v23.md` + INDEX + 원장 최종.
- **Step 28**: 최종 게이트 + `PHASE_P5_RESULT.md`.
- **게이트**: 치명 0·3장 GREEN·게이트 exit0·부록 E 무결·본문 코드언급 0.
- **중단 조건**: 치명 발견 → 해당 phase 로 회귀 수정 후 재검수.

---

## Implementation Interfaces

**수식 인터페이스 (실행자가 그대로 따를 형).**
- **동결 0차(원형)** — Prof. convention 첫 제시: `ξ_lag(V) = (1/L_V)∫^V ξ_eq(u)·e^{−(V−u)/L_V} du` (L_V=const, 선형 합성곱).
- **ratio 1차 보정(상호작용 항 추가)** — 두 번째 제시: 참/동결 비를 가해 기준비로 치환 → `ξ_lag(V) ≈ ξ_lag^(0)(V)·R̄(V)`, `R̄` = 논문 Eq.37 꼴 기준비.
- **타당성 인증서**: `ε ≡ 2·χ_d·(Ω/RT)·Δξ_supp ≪ 1`, `Δξ_supp ≈ L_V/(4w)`. 논문 (i)(ii)(iii)↔(K 완만·r_c 지배·σ 단거리) 대응표.
- **전달함수**: `H(ω)=1/(1+iωL_V)`, `dQ/dV_app(ω)=H(ω)·dQ/dV_eq(ω)`. 폭예산 ②③=|H|·① 꼬리=arg H.

**코드 인터페이스.**
- `func_L_q(...)` — 기존 시그니처 보존 + ratio 보정 키워드 인자(기본 off).
- `_causal_memory_*` — 전달함수(FFT) 경로 분기 인자. off 경로 = 기존 출력 bit-exact.
- **식별자·기호·한글 표현 임의 변경 금지**([[feedback_user_code_conventions]]·P5).

**문서 양식.**
- Result = 11항([[feedback_phase_execution_loop]]): Summary/Step Range/Inputs/Files Created/Files Updated/Read Coverage/Execution Evidence/Validation/Gate/Confirmed Non-Changes/Open Issues/Next.
- Ledger = 12-col. Phase ID·step 범위·Result 파일명·`Plan Steps` 상호 정합.

**부록 박스 양식.** warnbox(열화 조건) + 적용불가 명시 박스 = 문건 기존 박스 매크로 재사용(신 매크로 신설 X).

---

## Test Plan

- **LaTeX 빌드**: 3장 분리 빌드(병합 금지) err0/undef0. ch1 xr 2단 통과(ch2·ch3 aux 선행). 페이지 83+/25/17 회귀 감시.
- **구조 검사**: boxed/eq 라벨 무파손·부록 letter 순·**본문 코드언급 스캔 0**(부록·포인터 예외 화이트리스트).
- **코드 게이트**: 기존 게이트 스크립트 exit0 + 동결 off `max|d|=0.0`(bit-exact) + 신옵션 수렴 임계.
- **수식↔코드 정합**: E.4 지도의 각 수식이 `.py` 함수와 1:1(P3 Step 19).
- **문헌 대조**: Ref.6·7·JCP147 서지 필드 검증(하이쿠)·날조 0([[강한 레퍼런스 관리]]).
- **읽은 범위 대조**: 각 phase Result `Read Coverage` 항에 실제 read 파일·행/페이지 명시(미검독 표시).
- **논리 의존성**: P1 타당성 부등식이 논문 (i)(ii)(iii)과 1:1 대응(항목 누락 스캔).
- **동결극한 회수**: ratio 식 → L_V const 대입 → 기존 선형해 수치 일치(P1 Step 6).

---

## Assumptions

- Volterra(인과 1방향 지수핵) 의 1차 ratio 보정이 논문 Fredholm(양방향) ratio 와 **동일 수축 구조**를 가진다 — **P1 검산으로 확정 대상**(가정 상태). 불통과 시 본체 강등.
- Ref.6·7 원문 미확보 시 JCP147 본문 + 본 문건 자족 유도로 P3-5 5항 충족 가능(원 유도 재현 아닌 **적용 조건 명시**가 목표).
- 부록 E 를 ch1_graphite 에 편입해도 ch2·ch3 xr 교차참조·페이지 예산에 회귀 없음(P2 재빌드로 확인).
- `func_L_q` affinity A 동결 입력 구조가 곧 논문의 "가해 기준문제"에 대응(코드 실측 근거·P1 재확인).
- 사용자 Prof. 이상엽 convention(원형식 먼저→상호작용 항 추가형)이 부록 E 서술 순서에 적용된다.

---

## Correction History

- **본 계획서 = 직전 draft(동일 파일)의 양식 정정판.** 직전본은 자체 절 이름(1.배경 … 11.운용)으로 표준 11-section 을 이탈 → 섹션명·순서를 [[feedback_plan_template_11sections]] 표준(Summary…Correction History + Decisions Required 분리)으로 복원. **내용은 보존·재배치**(서베이·조건검수·아키텍처 결정 전부 승계).
- cumulative step 도입: P0=1-3(완료)·P1-P5=4-28 단조 부여(직전본은 phase 표만 있고 step 누적 없음).
- phase별 **Result 11항 문서**를 Implementation Changes·각 Phase 다음조건에 명시(직전본 누락).
- 셀링포인트 정정: "계산 절감" → **"해석적 1차 닫힘 + 타당성 인증서"**(P1 조건검수 = lag 은 이미 O(N) 전방 ODE 반영).
- 서베이 코어 갱신 반영: 기존 "#0+A+B" → **Tier1 = #0 Fredholm ratio + Laplace 전달함수**(신 A급), Tier2 = Fisher 정보기하, Legendre-Fenchel = Tier3(SURV_SYNTHESIS.md).

---

## Decisions Required (사용자 확인 — GO 전)

> 평문 확인 요청. 기본값(권고) 명시 — 무응답 시 기본값으로 진행.

- **D1 — 코어 스코프.** 기본값(권고) = **Tier1(#0 Fredholm ratio + Laplace 전달함수)만** 부록 E 코어로. Tier2 Fisher 는 P4 옵션 보류.
  - 대안: Tier1 + Tier2(Fisher) 동시.
- **D2 — 전달함수 물리 1문장 본문 노출.** 기본값 = **부록 E 만 + §8 포인터 1줄**(본문 물리 서사 최소 개입). 대안: §7 에 전달함수 물리 통찰 1문장 본문 삽입.
- **D3 — P4(Tier2) 실행 여부.** 기본값 = **P3 까지 완료 후 별도 GO 대기**(P4 는 조건부). 대안: 지금 P4 포함 승인.
- **D4 — Ref.6·7 원문.** 사용자 제공 가능 여부. 기본값 = **미제공 전제·JCP147 자족 기술로 진행**(P1 Step 7 에서 확정·정직 표기).
- **D5 — 실행 착수.** 위 확정 후 **P1(조건검수 게이트)부터** 착수. P1 게이트 통과 전 P2 저작 없음.

> **GO 사인 주시면 P1 Step 4 부터 5-stage 루프로 실행.** 무응답 기본값 진행도 지시 주시면 그대로.
