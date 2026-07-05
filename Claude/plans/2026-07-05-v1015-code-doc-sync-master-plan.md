# ★MASTER 계획서 (rev.2) — v1.0.15 교재 증판본: 이산 격자 완전 퇴출(점별 연속 아키텍처) + Ch2 발열 상세화 + Fable 물리 논리 6종 검토·보고 (코드↔Ch1↔Ch2 동기, 순차 7-페이즈)

> **이 문서 = v1.0.15 작업의 단일 마스터 진입점**(컴팩션 복구 시 여기부터 읽는다). 페이즈별 세부 계획·result·ledger 위치는 §6·도서관 규약. 인덱스 = `plans/INDEX.md`.
> **기획 단계 — Phase 1 착수 전 사용자 검토·GO 대기.**
> **관계**: `plans/2026-07-04-v1015-code-update-plan.md`(Fable rev.3)를 재프레이밍·대체(이력 보존). 방법론 정본 = 검증 모델 `2026-07-01-v1010-code-doc-sync-bdd-fitting-plan.md` + 스킬 `D:\Projects\Project_skills\competition-cherrypick-authoring\SKILL.md`.

---

## 0. 재프레이밍 배경 + 이번 세션 확정 사항

Fable rev.3("코드 재아키텍처 ★1급 + 문건 사후 각주 동기")를 사용자 4차 정정으로 재프레이밍:

1. **보존 구역·dead 처리 = 정책 전환**. "1바이트도 변조 X" 보존 구역은 v04_opus 경연에서 **AI 가 붙인 관습**(이전 세션 Fable rev.3 도 "orphan 이어도 보존 구역이면 삭제 금지"로 승계 — 세션 로그 L39639). **이번 세션 사용자 override: "죽는 부분은 지워야지"** → dead 코드·격자 param **삭제**(이력은 동결 v1.0.14). ★이력 확증(V1014_EXECUTION_LEDGER 줄 34): v1.0.14 Step 12 에서 master 가 보존 구역 내 주석을 "소유권 위반"으로 전량 원복 = AI 자기강제였음.
2. **Ch1·Ch2·코드 = 동등 세 축, 양방향 동기**("코드에 없는 내용 X + 문건 내용은 코드에 반영" — `v1010-code-doc-sync` §Summary⑦ 사용자 확정 루프).
3. **작업 순서 = 코드→문건→코드**(검증 모델). v1.0.15 코어(격자 퇴출)는 물리 서술 교정이라 **theory-first**(Ch1 격자 서술 확정 → 코드).
4. **그림 = 상한 없이 콘텐츠 기반 경연**(Fable "승자 재기용·4매" → 사용자 "Ch1 처럼 상한 없이 경연"으로 상향, 이번 세션).
5. **골든 = 검사 후 재캡처**(구 골든은 격자 아키텍처 ν=2 산물 — 병리 점검 후 등가 검증하고 재캡처).

### ★이번 세션 신규 확정 (rev.2 반영)
6. **문건 물리·화학 논리 = 기본 무수정(Fable 상위 모델 산출·완성도 높음).** 단 오판 방지를 위해 **6종(Codex 3 + Opus 3) 독립 검토 → 문제점 union → 공통 발견 = 진짜 문제로 인식 / 단독 발견 = master(Opus) 정밀 재확인으로 진위 판정 → 사용자에게 보고**(자동 수정 X, 수정 여부는 사용자 결정). = 스킬 §4 "검수 N종 union + 재검(오적발 필터)" 변형.
7. **Fable 사용 불가**(한도 소진 — 세션 로그 L39632). 스킬 §7 "10번째=기본 Opus, Fable 가용이면 Fable" → **Fable 불가이므로 1급 과제·체리픽 통합·최종 마감·master 판정 전부 Opus(본 세션).** 경쟁 N = **9종**(3 Sonnet + 3 Opus + 3 Codex; Fable ×1 가중3 없음 = 스킬 §1).
8. **뉘앙스(세션 로그)**: 간결성보다 **면밀·논리적 납득 우선**(L37154) — 격자 퇴출 재유도(R5·eq:branch)는 각주 압축이 아니라 완결 유도로. **물리 결함 > 논리 비약 > 수식-주도** 우선순위(L34346).

---

## 1. Summary

v1.0.15 = **한 권의 물리화학 교재 증판본**(`docs/v1.0.15/`). 세 갈래 실질 작업:

- **(코어·user-mandated) 이산 전압 격자 완전 퇴출 → 점별 연속 아키텍처.** 인과 꼬리를 연속 메모리 적분 $\xi_\mathrm{lag}(V)=\frac1{L_V}\int_{-\infty}^{V}\xi_\eq(u)e^{-(V-u)/L_V}du$ 의 점별 수치적분으로 직접 평가. $L_V\to0$ 에서 평형 peak 으로 해석적 매끈 환원($(\xi_\eq-\xi_\mathrm{lag})/L_V\to\tfrac{s}{w}\xi_\eq(1-\xi_\eq)$) → 작업 격자·리샘플·역보간·ν 스위치·23% 점프를 아키텍처에서 원천 제거. 코드(dqdv 재구현·dead 삭제) + Ch1 격자 서술 교정(§1.9·eq:branch·부록 A R5) 동반.
- **(상세화·additive) Ch2 발열 교재 상세화.** 그림 상한없음 경연·worked example 신설·표 보강(Fable 기존 논리는 보존, 추가만).
- **(검증·report-only) Fable 물리 논리 6종 검토 → 사용자 보고.** Ch1·Ch2 물리·화학 논리 무결성을 6종 union 으로 검증하고 문제를 보고(자동 수정 X).

검증 모델(6-페이즈) + 스킬(경쟁·체리픽·union 검수)을 v1.0.15 에 맞춰 **순차 7-페이즈**로. Fable 불가 → master·통합·최종 = Opus. 코드 = Serena 우선.

## 2. 문건·코드 품질 기준 (승계 + 세션 우선순위)

- **우선순위(L34346)**: ①물리·화학 논리 무결 ②논리 비약 제거 ③수식-주도 ④교과서급 어투.
- **면밀 우선(L37154)**: 간결보다 논리적 납득·완결 유도. 격자 퇴출 재유도는 면밀판.
- 형식 = 물리화학 교재(줄글 X·유도 사슬·보편식 먼저). 자기완결(비약 0). 어투 안정·객관(독자평가 표현 0). 피팅 실행력("이 문건만 보고 피팅 코드 작성 가능"). 분량·그림 = 콘텐츠의 자연 결과([[feedback_anode_fit_textbook_style]]).

## 3. Current Ground Truth (전제 검증)

- **현행 동결본 = v1.0.14**. Ch1 3445줄(57p)·Ch2 795줄(14p)·코드 `Anode_Fit_v1.0.14.py`. 회귀 `test_regression_graphite.py` 무인자 verify **13/13 bit-exact**(V1013·V1014 result — P1.1 라이브 재확인 전제).
- **격자 기구(퇴출) — 코드**: `dqdv`(L400–518, `V_work` L451·`np.interp` L458/517·ν 스위치 L499·`_causal_lowpass` L508/510)·생성자 격자 param(L257–278)·`_causal_lowpass`(L113, 재아키텍처 후 dead)·`func_U_j_hys`(L83, 이미 dead).
- **격자 기구 — 문건(Ch1)**: §1.3 eq:vwork(L964)·§1.9 연속 eq:memory(L1993, **이미 유도됨**)+이산 eq:lowpass(L1999)·eq:branch+23% 점프(L2053)·ν 각주(L2066)·staging 주석(L2192)·spine(L183/209)·부록 A **R5**(L3259)·부록 B tab:inputs 격자행(L3353)·keybox(L3138).
- **Ch2 현황**(격자와 무관): 그림 2개(개념도·includegraphics 0)·6절 중 4절 무삽화·worked example 0·§2.3 vib/elec 얇음. 발열 = 코드 `entropy_coefficient`(L565)·`reversible_heat`(L611)·`_effective_dS_rxn`(L554)·`func_dSe_molar`·`LCOCathodeDQDV`(L683)에 구현.
- **essential vs dead**: 활성 = func_w·func_U_j·func_ksi_eq·func_L_q(L372)·GRAPHITE_STAGING_LIT / dead = _causal_lowpass(재아키텍처 후)·func_U_j_hys.
- **★코드 작업의 문서화된 기원 = 문건 약속 3건 이행**(V1014_LEDGER 줄 17): ①eq:U1T2 정밀형 ②x-매핑 고정점 ③ν 처리(=격자 퇴출로 해소). = 문건→코드 방향. ①② 데이터 불요 → 범위 내.
- **이월(실데이터 소관·실값 배정 범위 밖)**: 다온도 T² 실측·LCO Ω^cat/dH_a·ν≳10 실값·서지 재확인.

## 4. Phase Range (순차 7-페이즈)

| Phase | 이름 | 성격 | Steps |
|---|---|---|---|
| P1 | **앵커·증판** — 격자 기구 코드·문건 맵 + v1.0.15 증판 + baseline gate + dead/essential 인벤토리 | 비파괴 | 1–4 |
| P2 | **Fable 물리 논리 6종 검토·보고**(Codex3+Opus3 union → 보고, 자동수정 X) | 검증·보고 | 5–8 |
| P3 | **Ch1 격자 퇴출 修正**(eq:memory 승격·eq:branch→L_V→0 극한·R5 재유도·문턱 재산출 — ★theory-first) | user-mandated 수정 | 9–14 |
| P4 | **Ch2 발열 상세화**(worked example·표·그림 위치 선정 — additive·코드 결합점 식별) | additive | 15–19 |
| P5 | **코드 개정**(dqdv 점별·dead 삭제·격자 param 제거·등가 3종·골든 검증 후 재캡처·Ch2 증분 반영, ★Serena) | user-mandated 수정 | 20–27 |
| P6 | **그림 경연**(스킬 N=9=3S+3O+3C·master=Opus 체리픽 — Ch1 꼬리 recompute + Ch2 신규, 상한 없음, 좌표=코드 수치평가) | 경쟁·체리픽 | 28–32 |
| P7 | **N회 가변-청크 검수(변경분) + 최종 동시 점검·마감** | 검수·마감 | 33–37 |

## 5. Non-goals

- 격자 경로 잔존 0(플래그·legacy 모드 X — 사용자 확정). dead 함수 orphan 보존 X → **삭제**(이력=v1.0.14).
- **Fable 물리 논리 임의 수정 X** — P2 는 검토·보고까지(수정은 사용자 결정 = Decision Gate). 단 코어 격자 퇴출(P3)·Ch2 추가(P4)는 user-mandated 예외.
- 실데이터 이월 4건 실값 배정 X(x-매핑 고정점·정밀형 해석 대조는 범위 내).
- v1.0.14 이하 폴더·golden·이전 result/ledger/handover·Codex 산출물 수정 X(증판·Addendum). 피팅 wrapper X. spinodal 부록 편입 X. 새 챕터 X.

## 6. Phase 상세 (5-stage 루프 + 단위 구성 루프 + gate)

> ★작업 방식 = 스킬 `competition-cherrypick-authoring` + 검증 모델. **전부 Agent 도구(Workflow·권한팝업 X)·GO 후 팝업 0·커밋만(푸쉬는 버전 확정 시).** sub 머리에 역할·경계·범위밖 금지·허위 attribution 금지 고지. **검수·경쟁 = 작업 세션과 다른 세션(자기검사 금지)·refute+가장약한1곳+빈통과금지·coverage missing=0.** 병렬 최소화(목적적). ★**Fable 불가 → master·체리픽 통합·최종 마감·단독발견 재검 = Opus.** ★**체리픽 비교 베이스 = 이전 버전 v1.0.14**(Fable 작성 — 사용자 배제 지정분[격자] 외에는 근접 정답 수준): 신규 후보를 반드시 v1.0.14 원본과 나란히 비교해 **신규가 명백히 우월할 때만 교체**(기본 = v1.0.14 보존, 격자 관련만 필수 recompute). 그림·문건·코드 공통. 커밋 = master 전용, 페이즈마다.
> ★도서관 규약: 각 Phase 착수 = 세부 계획서 `plans/2026-07-05-v1015-P{n}-*.md`. Phase 종료 = result 의무 저장(`results/process/V1015_P{n}_*_RESULT.md`) + ledger + INDEX 갱신. result 없이 다음 Phase 금지. 컴팩션·재개 직후 5-check.

### P1 앵커·증판 (Steps 1–4) — 비파괴
- **S1** 증판: v1.0.14 전 파일 → `docs/v1.0.15/` 복사·버전 문자열 패치·잔재 0. v1.0.14 동결. 구 골든은 v1.0.14 이력 존치.
- **S2** baseline gate(라이브): 회귀 13/13·tex 3종 0-err/ref 0/of 0·demo/sample/suite PASS(격자 아키텍처 마지막 확인).
- **S3** 격자 의존 전수 맵(코드 Serena 심볼 + Ch1 문건, §3 목록 라인 확정·누락 0)·처분 초벌.
- **S4** dead/essential 인벤토리 + 피팅 파라미터 인벤토리. gate: 맵·인벤토리 명령+증거 완결.

### P2 Fable 물리 논리 6종 검토·보고 (Steps 5–8) — 검증·보고, 자동수정 X
> 스킬 §4.1 "상위 모델 유산 산출물 검증-전용 모드" + §4 교차합의 triage. 대상 = Ch1·Ch2 물리·화학 논리(격자 퇴출로 어차피 바뀔 §1.9/R5 제외 — P3 소관). **수정 안 함 — 문제 발견·보고만(수정 여부는 Decision Gate 에서 사용자 결정).**
- **S5** 6종 독립 검토 발진(Agent, 무통신·다른 세션): **Codex 3 + Opus 3**. 렌즈 = 물리·화학 논리 무결(우선)·논리 비약(G-follow/G-derive)·부호·차원·극한·detailed balance·Ch1↔Ch2 정합. 각 창 ~500줄 분할·coverage missing=0·refute mandate. 산출 = 문제 목록(위치|명제|근거|심각도).
- **S6** union 집계: 6종 문제 합집합 → **≥2종 공통 = 진짜 문제 가능성 높음(채택 후보)** / **1종 단독 = master(Opus) 정밀 재확인**(원문 재정독·재유도로 진짜 결함 vs 오적발[검수자 과민·산술오류·물리동치 미인지] 판정).
- **S7** 보고서 `V1015_P2_PHYSICS_REVIEW.md`: 확정 문제 / 단독-확정 / 오적발-기각을 4-tier 로. **수정 제안은 하되 실제 수정 X.**
- **S8** gate + **Decision Gate**: 물리 실결함 발견 시 사용자 보고·수정 여부 결정 대기(기본 무수정). 없으면 통과.

### P3 Ch1 격자 퇴출 修正 (Steps 9–14, Opus 직접 — 물리 1급·theory-first, 면밀판)
- **S9** §1.9 재서술: eq:memory(연속 적분형) **계산 정본 승격**, 이산 eq:lowpass = 구판 격자 이력 각주 강등.
- **S10** eq:branch 제거 → **연속 L_V→0 극한 유도 신설**(부분적분 완결판): $\xi_\mathrm{lag}=\int_0^\infty\xi_\eq(V-L_Vt)e^{-t}dt\approx\xi_\eq-L_V\xi_\eq' \Rightarrow (\xi_\eq-\xi_\mathrm{lag})/L_V\to\tfrac{s}{w}\xi_\eq(1-\xi_\eq)$. 충전 방향 반전(eq:reversal 연속형).
- **S11** 부록 A **R5 재유도**: 현행(이산형 매끈환원 부정·스위치 필요)을 (a) 이산 격자 병리=격자 폐기 이유로 재분류 + (b) 연속형 매끈 환원 증명(S10)을 새 검산항으로. "L_V 작으면 종 환원=거짓"은 이산형 한정 명기.
- **S12** §1.3 eq:vwork 재서술(작업격자 폐지 → 메모리 적분 적분창·경계 자연처리) + 격자 잔재 스윕(staging 주석·spine·keybox·부록 B tab:inputs 격자행 제거·tab:symcode/nodecode 정리[점별 API 반영은 P5 후]).
- **S13** FITTING_GUIDE 격자 언어 소거 + **문턱(70–74 kJ/mol) 재산출**(ν·Δ_grid 기반 → 정의 변경, 재유도)·"실측 V 직접 기입" 워크플로.
- **S14** gate: 신설 유도 Opus 독립 재검산(부호·차원·극한)·격자 용어 grep 0(이력 각주 제외)·ch1 빌드 0-err/ref 0. (전자항 T² 서술은 P4 §2.3 동기.)

### P4 Ch2 발열 상세화 (Steps 15–19) — additive(Fable 논리 보존·추가만)
- **S15** worked example 신설(실제 흑연 파라미터 → 특정 SOC 의 ∂U_oc/∂T·q_rev 값, 코드 산출 정합).
- **S16** §2.3 vib/elec 확충(BE/FD·Sommerfeld — 신규 유도는 추가, 기존 논리 무수정)·전자항 정밀형(eq:U1T2) 물리 서술(옵트인, 코드 P5 동기).
- **S17** 코드 결합점 식별표: Ch2 물리↔코드 심볼 매핑 + 증분(코드 반영 필요)/기구현/문건전용 분류.
- **S18** 그림 위치 선정(제작 P6): ∂U_oc/∂T(x)·q_rev(x) 흡열/발열 교대·vib(BE)/elec(FD·Sommerfeld) 분포 등 전수(상한 없음)·브리프. 기호·물성 입력표 보강.
- **S19** gate: 발열 완결·Ch1 정합·교재 형식·ch2 빌드. 코드 없는 신설 물리는 "P5 반영 예고".

### P5 코드 개정 (Steps 20–27, ★Serena — 점별 재아키텍처 + dead 삭제 + 골든 검증)
- **S20** `dqdv` 점별 재구현(스칼라/비균일 배열 → 같은 좌표 dQ/dV; 꼬리=메모리 적분 점별 수치적분, 구간 $[V_i-40L_V,V_i]$ Gauss–Legendre 패널·rel-err ≤1e-8·충전 방향 반전; 스위치 없음, $L_V<\varepsilon_\mathrm{mach}$ 급만 해석 극한 수치가드 1줄). `curve` facade 유지.
- **S21** **dead 삭제**: `_causal_lowpass`·`func_U_j_hys` 제거·격자 param(grid_pad·n_work·v_span_floor·min_lag) 제거(잔존 입력=명시 경고)·`np.interp` 역보간 제거. essential 함수 정확성 재검산.
- **S22** `equilibrium`·`entropy_coefficient`·`reversible_heat` 점별 정합 + Ch2 증분(전자항 정밀형 opt-in `exact_electronic_T=False`·worked example 원천) 반영.
- **S23** **등가·연속성 실증**(골든 캡처 前): (i) 해석 L_V→0=평형 peak (ii) Δ→0 구판 수렴 rel<1e-6(꼬리 활성) (iii) L_V 스윕 점프 0 vs 23% (iv) 비균일 실측 V 데모 (v) 성능 1000점×4전이 <50 ms.
- **S24** **구 골든 병리 점검 + 신규 골든 재정초**: 구 골든의 ν 스위치·점프 아티팩트 정량 → S23 통과 후 신규 캡처(좌표=구판 V_n·값=점별)·재정초 사유·검증 증거 ledger 기록. 구 골든=v1.0.14 이력.
- **S25** demo·sample·suite 점별 이식·재실행.
- **S26** 전자항 정밀형 해석 대조(<1e-10·OFF bit-exact) + x-매핑 고정점(`verify_xmap_fixedpoint.py`).
- **S27** gate: 신규 골든 self-verify·등가 5종·연속 천이·전자항 대조·suite/sample/demo PASS.

### P6 그림 경연 (Steps 28–32) — 스킬 §1·§6, N=9, master=Opus
- **S28** 대상 선정(상한 없음·콘텐츠가 개수 정함): **Ch1 꼬리·격자 그림 recompute**(fig:reversal·fig:relaxode 등 — 격자 산출→점별 코드 재산출) + **Ch2 신규**(S18 전수) + §1.9 연속형 개형. 대상별 브리프(위치·전달 물리·현행 불만/부재).
- **S29–31** 경연: 대상마다 **9안 = Sonnet 3 + Opus 3 + Codex 3**(무통신·Codex 단계구동+폴링). 전 안 TikZ 소스+렌더·좌표 calc 동봉. 제작 머리에 좌표=식/코드 수치평가·라벨 무교차 고지. **master(Opus) 체리픽 = 9안 + 이전 버전 v1.0.14 원본을 나란히 비교**(물리 정확[좌표 검산]·전달력·정합 3축·필요 시 합성). ★**v1.0.14 가 근접 정답이므로 신규안이 명백히 우월할 때만 교체**(격자 산출 그림[fig:reversal·relaxode]은 점별 코드 recompute 필수라 예외).
- **S32** gate: 편입 그림 전점 좌표 재검산(코드/식 일치)·캡션-본문 정합·빌드. 교체 원본=`process/fig_contest/_replaced_originals.tex` 보존.

### P7 N회 가변-청크 검수(변경분) + 최종 마감 (Steps 33–37)
- **S33–35** 변경분(코드·격자修正·그림) N회 가변-청크(통독/절/식/함수/라인/도메인)+렌즈 로테이션(구조/물리 적대검산/G-follow·G-usable/완결성/시각/**코드↔문건 양방향[코드에 없는 서술 0·문건에 없는 코드 0]**/**그림 3자 정합**/직전수정 새 결함). Agent 병렬(refute)→master(Opus) 삼각검증·직접 정정→커밋. 기본 10회·수렴=연속 2R 확정결함 0(또는 결함 계층 하강 종결, v1.0.14 관행).
- **S36** 최종 게이트(전 빌드·신규 회귀·suite·sample·demo·xmap·등가·**3대 무결[코드에 없는 내용 0·문건에 없는 코드 0]**·CRIT/HIGH 0) + `V1015_RESULT.md`·ledger·INDEX·CODE_MAP.
- **S37** HANDOVER_v1.0.15(Chain 연장)·최종 커밋+푸쉬.

## 7. Implementation Interfaces

- `dqdv(V: scalar|array, s, T, ...) -> 같은 좌표 dQ/dV`(비균일 허용). `curve` facade 유지.
- **제거**: grid_pad_lo/hi·n_work_min·v_span_floor·min_lag_grid_steps(잔존=명시 경고)·_causal_lowpass·func_U_j_hys·np.interp 역보간.
- **유지·재검산**: func_w·func_U_j·func_ksi_eq·func_L_q·GRAPHITE_STAGING_LIT·entropy_coefficient·reversible_heat·_effective_dS_rxn·func_dSe_molar·LCOCathodeDQDV.
- `exact_electronic_T: bool = False`. 신규: verify_pointwise_equiv.py·verify_xmap_fixedpoint.py·golden_graphite_ref.npz 재캡처(v1.0.15).
- **에이전트 배분(Fable 불가)**: P2 검토=Codex 3+Opus 3(6종 union). P6 경연=Sonnet 3+Opus 3+Codex 3(9종). 체리픽 통합·최종 마감·단독발견 재검·삼각검증·정정·커밋 = master(Opus). Codex=단계구동+폴링. 전부 Agent(Workflow X).
- 코드=Serena 우선. 검증=실제 실행·round-trip·회귀. 커밋=페이즈마다 master 전용(Anode_Fit 버전 자동 commit+push·attribution 없음).
- 계획서 11-section·ledger 12-col·Result 11항목·검수 보고 양식 = v1.0.14 동일.

## 8. Test Plan

- 회귀: 신규 골든 13/13 self-verify(점별). 구 골든 등가는 Δ→0 수렴 검증(bit-exact 승계 아님=의도적 재정초).
- 등가·연속성: 해석 L_V→0=평형 peak / Δ→0 rel<1e-6 / L_V 스윕 점프 0 / 비균일 V 데모 / <50 ms.
- 전자항: <1e-10·OFF bit-exact. x-매핑 고정점 잔차.
- 문건: 코드 step↔식 1:1·**코드에 없는 서술 0·문건에 없는 코드 0**·격자 용어 grep 0(이력 각주 제외)·교재 형식·orphan 0·tex 0-err/ref 0/of 0.
- 검토(P2): 6종 union coverage missing=0·단독발견 master 재검 100%.
- 그림: 편입안 전점 좌표=코드/식 재계산 일치·라벨 무교차·캡션-본문 정합.

## 9. Assumptions / Decisions (기본값 — GO 시 진행)

- 실측 데이터 없음 → 등가·해석 대조로 검증(실값 배정 X). 신규 골든 좌표=구판 V_n.
- **결정 기본값**:
  1. dead·격자 param **삭제** — 사용자 확정.
  2. Fable 물리 논리 = **기본 무수정 + 6종 검토·보고**(수정은 P2 Decision Gate 에서 사용자 결정).
  3. 그림 = **상한없이 콘텐츠 기반 9종 경연**(스킬), master=Opus 체리픽.
  4. 전자항 정밀형 = 문건(Ch2 §2.3)+코드(opt-in OFF) 양방향 동기.
  5. 골든 = 등가 3종 검증 후 재캡처.
  6. eq:vwork/lowpass/branch = 본문 연속형 재서술(면밀판) + 이산 이력 각주.
  7. 실데이터 이월 4건 = 범위 밖 / x-매핑 고정점·정밀형 해석 대조 = 범위 내.

## 10. Decision Gate / 정지 조건

- 스코프·순서 = 본 마스터 확정 제안 → 사용자 검토·GO 후 P1→P7 연속 무중단(매 phase 재승인 X).
- **정지 조건**: ★P2 물리 실결함 보고(무수정 원칙이라 수정 여부 = 사용자 결정) / Decision Gate / 새 의존성 / FAIL gate / 사용자 stop / 두 통제문서 모순(→더 제한적).
- **theory-first 불변**: P3(Ch1 격자 서술 확정) 전 P5(코드 재아키텍처) 착수 금지.

## 11. Correction History

- **rev.1 (2026-07-05)**: Fable `2026-07-04-v1015-code-update-plan.md`(rev.3) 재프레이밍 — 검증 모델(코드→문건→코드·theory-first) + 사용자 3차 정정(보존구역=AI관습·dead 삭제 / 세 축 양방향 동기 / 작업순서 / 그림 상한없음 / 골든 검사후 재캡처). V1014 ledger 대조(문건 약속 3건 기원·보존구역 AI 자기강제 확증).
- **rev.2 (2026-07-05)**: 사용자 4차 지시 반영. ①**스킬 `competition-cherrypick-authoring` 명시 참조**(N+N+1+1·검수 union 변형·Fable 가중). ②**Fable 물리 논리 = 기본 무수정 + 6종(Codex3+Opus3) union 검토→보고** Phase(P2) 신설 — 공통=진짜/단독=master 재검, 자동수정 X. ③**Fable 사용 불가 확정**(로그 L39632) → 1급·체리픽·최종·재검 = **Opus**, 경쟁 **N=9**(Fable ×1 가중3 없음). ④그림 경연 = 스킬 9종(3S+3O+3C)·master=Opus. ⑤세션 로그 뉘앙스 반영(면밀 우선 L37154·물리>비약>수식 L34346·격자 퇴출 경위=ν 파라미터 논쟁을 아키텍처 결정으로 상향). Phase 재편(7-페이즈: P2 검토 신설·Ch1 修正/Ch2 additive 분리)·Steps 재번호(37).
