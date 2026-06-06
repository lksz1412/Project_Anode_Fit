# 계획서(최종) — Chapter 1 완전 백지 재작성: 논리 사슬에서 구조를 도출 (CH1R-series)

**Date**: 2026-06-03 · **Author**: Claude · **상태**: 최종 계획(설계도). **사용자 GO 대기 — 본 turn 에 tex 작성 X.**
**Supersedes**: `2026-06-03-ch1-blank-page-clean-spine-rebuild-plan.md`(BP v1) + `2026-06-03-ch1-from-scratch-intersection-bridge-plan.md`(BP2 v1). 두 선행본의 결함(아래 §Correction History)을 정정.
**검토 근거**: 3-렌즈 적대 검토(목표충분성·작업방식·Bridge 비약) + 사용자 정정 2건 + 인프라 실측(RB_CHARTER/RB_AL_MASTER/RB_EXECUTION_LEDGER/RB_REFERENCES_DOSSIER 직접 read).
**양식**: 표준 11-section(`feedback_plan_template_11sections`) + cumulative step + Phase 5-stage 루프(`feedback_phase_execution_loop`).

---

## Summary

Chapter 1 을 **완전 백지**에서 다시 쓴다. \*가져오는 것은 사용자가 명시한 출발 재료 3가지뿐\* — **(가) 관찰**(저온 긴 꼬리·다음 peak 겹침·C-rate 겹침 심화), **(나) 서의 5단계 기획의도**, **(다) 물리 정전**(통계역학·전기화학·속도론). **기존 tex 문건의 식·문장·구조·절 진행은 가져오지 않는다**(사용자 2026-06-03 정정: "각 절의 진행까지 복사하라는 얘기는 안 했다"). 즉 \*절 구성도 미리 정하지 않는다\* — 위 3 재료에서 **논리 사슬(Logical Chain)을 도출**하고, 그 사슬이 \*필연적으로\* 만드는 자연스러운 덩어리가 절이 된다. 지난 버전 최악 결함은 \*절 내용\*이 아니라 **절과 절 사이 논리 비약**이었으므로, 본 작업의 1급 설계 대상 = \*논리 사슬의 연속성\*이다(사슬이 연속이면 절 경계는 끊기지 않는다). 단 \*근거 인프라\*(RB_CHARTER 규약·RB_AL_MASTER AL 번호·RB_REFERENCES_DOSSIER DOI·RB_EXECUTION_LEDGER step 좌표)는 \*누적 자산\*이라 **계승**한다(백지 대상은 tex 본문에 한정). 부록 B(피팅 워크플로) 분리. 산출 = `graphite_ica_ch1.tex`(백지 신규) + RB 인프라 갱신.

## Current Ground Truth

**사용자 명시 (절대 기준, 2026-06-03)**
- "출발 재료·조건·기획의도를 가져가는 것은 맞다. 내용은 다시 처음부터. **기존 문건을 가져오지 않는다.**"
- "**각 절의 진행까지 복사해오라는 얘기는 안 했다**" — 출발 재료는 위 (가)(나)(다) 3가지뿐. 절 구성은 도출 대상이지 계승 대상 아님.
- "절 내용은 내 지시를 따랐으나 **절끼리 논리 비약**이 심했다 — 그걸 개선." → 개선 본질 = 절간 연결(비약 제거).
- 조건: 방전(탈리튬화)만 · Ch1 최대한 심플 · grounding 의무 · 부록 B 분리 · 흐름 끊는 도구 금지(Agent only).

**계승할 인프라 (백지 ≠ 인프라 폐기; 실측 확인)**
- `RB_CHARTER.md`(step1–5): $s_{\phi,j}$ 부호 · $V_n/V_{n,\drive}/V_{n,\app}/V_{n,\OCV}$ 4종 구분 · $n_j^\eff=RT/(Fw_j)$ 위계 · keystone Level A 한정어 · AL 통합 번호. → 본문 \*규약\*으로 상속.
- `RB_AL_MASTER.md`: AL-1~63 기등재, Ch1 그룹 ≈ AL-1~19, **AL-14**(stretched tail = 지수완화 연속합; svare2000+johnston2006+lindsey1980, tier=BOUNDED, gap 정직표기) = 본 장 핵심 물리. → AL 번호 \*재사용\*, 신규만 추가.
- `RB_REFERENCES_DOSSIER.md`: DOI 검증분(macdonald2000→svare2000 저자 정정 등). → 인용 \*대조\*, 신규만 검증·추가.
- `RB_EXECUTION_LEDGER.md`: RB 시리즈 step 1–157 **완주**(Ch1~6+통합 전부 PASS). 본 작업은 "step 26 재개"가 아니라 \*완성된 Ch1(`_rebuilt`, 1629줄)을 사용자가 반려해 백지 재작성\*하는 것 → step 좌표는 157 이후로 이어감(아래 Phase Range).

**버리는 것**: `graphite_ica_ch1_rebuilt.tex`·`graphite_ica_ch1_clean.tex` 의 식 표현·문장·**절 진행 구조**(베끼기·구조 계승 금지; 물리 모순 점검용 \*사후 대조\*만, 그나마 정량 diff 로 표현 복사 0 확인).

## Phase Range

> Phase ID = `CH1R.<n>`. Step = RB 누적 이어감(158–). result 없는 Phase 진입 금지(컴팩션 환각 방지). 매 Phase 종료 = `Claude/results/` result(11항목) 저장 + `RB_EXECUTION_LEDGER.md` 행 추가(12-col).

| Phase | 이름 | Step | 산출물(result) |
|---|---|---|---|
| **CH1R.0** | 인프라 정독 계승 + **논리 사슬 도출** + 절 덩어리화 + 게이트 동결 | 158–162 | `PHASE_CH1R0_chain_RESULT.md`(Logical Chain 확정) |
| **CH1R.1** | 사슬 전반(무대) 백지 작성 | 163–167 | `graphite_ica_ch1.tex`(전반) + result |
| **CH1R.2** | 사슬 중반(주역: 속도→길이→분포→중첩) 백지 작성 | 168–174 | 동 파일(중반) + result |
| **CH1R.3** | 사슬 후반(되먹임→닫힘→피팅식→반증) 백지 작성 | 175–179 | 동 파일(후반) + result |
| **CH1R.4** | 검증: transition + 절내 fine 검수 + P3 7항목 + 적대 다중렌즈 | 180–184 | `PHASE_CH1R4_verify_RESULT.md` |
| **CH1R.5** | 수정 + 빌드 GREEN + result(11항목) + Decision Gate | 185–188 | 확정본 + ledger 갱신 |

## Non-goals

- 절 \*구성을 미리 고정\*하거나 기존 문건에서 가져오기(구조도 도출 대상). 기존 tex 식·문장 옮겨심기.
- Ch2~5 손대기. 부록 B 를 메인에 재흡수. solver 코드. RB 인프라(ledger/AL/charter/dossier) 폐기·중복 신설.
- 측도론 형식·BOUNDED/FLAGGED 단서를 본문 줄기에 노출(→ box). push·main 머지(별도 GO). Workflow 등 권한팝업 도구 사용(Agent only).

## Implementation Changes

- 생성: `Claude/docs/graphite_ica_ch1.tex`(백지; preamble 표준 LaTeX 새로). result 6종(Phase별). 
- 갱신(덮어쓰기 아닌 \*행 추가/계승\*): `RB_EXECUTION_LEDGER.md`(step 158– 행), `RB_AL_MASTER.md`(신규 AL 만 추가), `RB_REFERENCES_DOSSIER.md`(신규 ref 만).
- 폐기: `graphite_ica_ch1_clean.tex`(transplant 혼입) → `_discarded/` 이동(삭제 아님, 문건 보호).
- 보존: `graphite_ica_ch1_rebuilt.tex` 등 기존 전부(덮어쓰기 0).

## Phase CH1R.0 — 인프라 계승 + ★ 논리 사슬 도출 (step 158–162)

**step158 인프라 전문 정독**: RB_CHARTER·RB_AL_MASTER·RB_REFERENCES_DOSSIER·RB_EXECUTION_LEDGER 를 \*여러 스케일 겹치는 청크\*로 head→tail 정독(앞뒤만 읽고 중간 추론 금지). 상속 규약·AL 번호·DOI·step 좌표 확정. gate: 계승 항목 체크리스트.

**step159–161 ★ Logical Chain 도출(본 계획 핵심 산출)**: 출발 재료 3가지에서, 각 고리가 \*앞 고리의 필연적 귀결\*이 되도록 사슬을 세운다. 각 고리 = `[가진 것] → [그래서 생기는 빈틈/질문] → [그 빈틈을 메우는 새 양·단계 + \*공식 앞 물리 동기\*] → [그것이 주는 것]`. \*절은 이 사슬의 자연 덩어리\*이며 미리 못 박지 않는다(아래는 \*도출된\* 사슬·잠정 덩어리; 작성 중 조정 가능, `feedback_step_granularity_flexibility`).

### 도출된 논리 사슬 (관찰 + 5단계 의도 + 물리에서 필연 전개)

| # | 가진 것 → 빈틈(질문) | 메우는 새 양 (★공식 앞 물리 동기) | 주는 것 | (잠정 절) |
|---|---|---|---|---|
| C0 | 관찰(저온 긴 꼬리). \*무엇\*에서 벗어난 꼬리인가? 벗어남의 기준=평형, 평형은 내부 전위가 정함 — 그 전위는 어디서? | **$V_n$**: 내부 전위는 외부 측정값 아님; \*전하 보존\*이 정함 | $V_n$=전하보존 해(무대) | 무대 |
| C1 | 보존식이 \*목표 진행률\*을 부른다 | **$\xi_\eq$**: 평형서 도달할 점유율(통계역학 lattice-gas→logistic, \*무비약 유도\*) | $\xi_\eq(V_n,T)$ | 무대 |
| C2 | 목표 있다 — 평형이 꼬리를 설명하나? | (음화 논증) $w=RT/F$ 저온 \*좁아짐\* → 평형은 "저온 짧은 꼬리" 예측=관찰 반대. C-rate 의존은 \*상태량으론 불가능\* → 시간(속도) 성분 필요 | "주역은 동역학" | 무대→주역 다리 |
| C3 | 목표를 \*유한 속도\*로 좇는다 — 속도는? | **$k$**: Eyring rate; 목표 추적의 시간 척도 | $k(T)$ | 주역 |
| C4 | (C-rate 관찰) 전류 흐르면 속도가 바뀐다 — 왜? | **$\mathcal A$**(구동력: 목표·상태 차이가 반응을 미는 열역학 force=$s_\phi F(V_\drive-U)$) → **$\chi$**(그 force 가 배리어를 \*얼마나\* 낮추나) → 낮춘 배리어가 $k$ 키움 | $k=k_0 e^{-(G-\chi\mathcal A)/RT}$ | 주역 |
| C5 | 목표+속도 → 지연. 지연은 \*시간\*인데 꼬리는 \*공간(q)\*. ★시간→공간 변환 | **$L$**: 전류가 q-속도이므로 시간 완화가 q-거리로 사상; $L=|I|/(Q_\cell k)$=꼬리 e-folding 거리 | $L$, 저온 $L$↑=꼬리↑(관찰 일치) | 주역 |
| C6 | $L$ 하나=한 도메인. 전극은 도메인이 여럿(입경·결정성·경계차) → 배리어가 제각각 | **$\rho_G$**: 배리어 분포(★단일 G 아님의 물리 근거) | $\rho_G(G)$ | 분포 |
| C7 | 배리어가 \*지수적\*으로 길이로 사상 | **$A_L$**: 배리어 분포의 좌표변환=길이 빈도 분포(측도 Jacobian 은 box) | $A_L(L)$ (순수 빈도) | 분포 |
| C8 | 길이별 빈도 + 각 길이의 지수 감쇠(지수는 $L$ 정의서 \*필연\*) → 합치면? 합을 담을 변수? | **$\Theta$**(누적 전체 진행; \*여기서 처음\* 정의 — C7 은 빈도만이라 forward 의존 0) + kernel 중첩 $\int A_L(1/L)e^{-(q-q_a)/L}dL$ | $d\Theta_\mathrm{tail}/dq$ (AL-14 BOUNDED) | 중첩 |
| C9 | 중첩은 \*목표 고정\* 가정. 진행→$V_n$→목표 이동(전하보존) → 고정 깨짐 | (자기참조) Volterra 2종 | $\Theta$=자기참조 적분해 | 되먹임 |
| C10 | Volterra 는 \*암시적\*(Θ가 제 적분 안) → 직접 못 푼다. 닫음=자기참조를 \*국소 미분 관계\*로 환산 | **$C_\bg$**(되먹임 0 일 때 수렴하는 기준 배경 용량) + closure | $dQ/dV_n=C_\bg/(1-Q_p\,d\Theta/dQ)$ + 심플 근사식($L$, $L_\varphi$, $\{L,\Delta H_a,\chi\}$ 추출) | 닫힘·피팅식 |
| C11 | 닫힌식은 \*검증 가능\* 예측을 주나? | tail Arrhenius 분해(Eyring 보정 $y(T)=\ln(1/LT)-\chi\mathcal A/RT$) + N1~N5(N5=transport·$\eta_\ct$ 분리 \*가장 약한 지점\*) | 반증 절차 | 반증 |

**step162 게이트·박스·파일 규약 동결.** gate: 사슬 12 고리가 빈틈-연결 1:1(끊김 0) + 각 새 양에 \*공식 앞 동기\* 칸이 참(★ 위 표에 강제).

## Phase CH1R.1–CH1R.3 — 백지 작성 (step 163–179)

각 고리를 **5비트**로: ① 진입 빈틈 받아 질문 선언 → ② 새 양 \*물리 말 먼저\* 동기 → ③ 무비약 유도(한 줄도 안 건넘, 내가 직접·기존 문건 미참조) → ④ 의미·용도 → ⑤ 퇴장 빈틈 열기. 단서·측도·BOUNDED/FLAGGED 는 box(박스 빼고 본문만 읽어도 사슬 유지). forward ref 0. CHARTER 규약 적용($V_n$ 4종 구분·keystone 한정어·$s_\phi$). AL-# 인용(기존 재사용+신규).

## Phase CH1R.4–CH1R.5 — 검증·확정 (step 180–188)

검증 3층(아래 Test Plan) → 수정 → 빌드 GREEN → result 11항목 → 사용자 Decision Gate.

## Implementation Interfaces

- 파일: `graphite_ica_ch1.tex`(백지). label 새 체계. preamble 표준 LaTeX(kotex/amsmath/박스 환경).
- **인프라 계승 인터페이스**: 규약=RB_CHARTER step1–5 / AL=RB_AL_MASTER(재사용+신규는 그룹 여유번호) / DOI=RB_REFERENCES_DOSSIER 대조 / step·복구좌표=RB_EXECUTION_LEDGER(158–). \*기호 충돌 주의\*: Assumption Ledger=AL-#, relaxation-length spectrum 진폭=$A_L$ — 표기 분리.
- **부록 B 재동기**: 본문 닫힌식·기호 ↔ `graphite_ica_ch1_appendixB_fitting.tex` 1:1 대조표(불일치 0); Ch1 확정 후 부록 cross-ref 재동기.
- Result 11항목(`feedback_phase_execution_loop`, Read Coverage 필수). Ledger 12-col. 문건 보호(덮어쓰기 0, 폐기는 `_discarded`).

## Test Plan

**A. 사슬·서술 게이트 (verifiable 분해형)**
- **G-bridge**: 각 고리 전이 i — (a) 앞 고리 마지막 문단에 "다음이 답할 질문 1문장" \*존재\*, (b) 다음 고리 첫 문단이 그 질문을 \*재인용/직접응답\*, (c) **2 이상 독립 agent 가 박스 제외 본문만 읽고 "이 전이에 미정의 양·\*물리적으로 한 단 건너뛴\* 도약이 있나" Y/N → 전원 N**. (전이×(a)(b)(c) 표를 result 에. 한 칸 FAIL→다리 재작성.) ※"물리적 한 단 건너뜀"은 문자적 연결만으론 못 잡으니 (c)에 명시(C2 시간성분·C5 시간→공간 특히).
- **G-motive / G-interpret**: 모든 새 양($V_n,\xi_\eq,\mathcal A,\chi,k,L,\rho_G,A_L,\Theta,C_\bg,\mathcal K$)이 공식 \*앞\*에서 물리 동기 / 공식 \*뒤\*에서 의미·용도. (특히 $\mathcal A,\chi,\rho_G,C_\bg$ — 비평 3 적발 누락분.)
- **G-nofwd**: 본문 forward ref 0($\Theta$ 는 C8 first-use 정의, C7 은 빈도분포로 제한).
- **G-spine**: 박스 전부 건너뛰고 본문만 읽어도 사슬 유지.
- **G-usable(★ 비평 1·2 적발 2급 결함)**: Ch1 \*만으로\* 실데이터 피팅 닫힌식 + 심플 근사식($L$·$L_\varphi$ 추출, $\{L,\Delta H_a,\chi\}$ 식별 순서, 0.2C anchor)이 \*본문 결과\*로 표면화(없으면 FAIL — 지난 반려 핵심).
- **G-noleap·G-dim**: 무비약(자명/clearly 0)·차원.

**B. 프로젝트 물리 규약 게이트 (P3 7항목 + CHARTER, 의무)**
- **G-P3-1**: $V_n/V_{n,\app}/V_{n,\drive}/V_{n,\OCV}$ 4종 구분 grep 일관성.
- **G-P3-2**: 전하보존=내부전위 결정 중심식(OCV lookup 회귀 0).
- **G-P3-3/4**: $\xi_j,Q_\bg,d\Theta/dQ$ self-consistent loop 를 dependency 표로 + 순환을 \*implicit정의/수치해법/논리공백/물리충돌\* 4분류 진단(C9~C10 이 implicit→국소화임을 명시).
- **G-P3-5**: closure 에 쓰는 ref(JCP 147(14)144111(2017))를 서지·논문내 위치·수학구조(Fredholm)·변수매핑·\*물리가정 차이\*(Volterra vs Fredholm) 로 기록 — 단 \*Ch1 심플 경계상 상세는 부록 B\* 면 그 경계 명시.
- **G-cross(CHARTER)**: keystone Level A 한정어 필수(C4 절 제목에 "배리어 낮춤" Level B 함의어 단독 금지)·$n^\eff$ 위계·$s_\phi$ 명시.

**C. 검수 입도·근거 게이트**
- **G-fine(절내 정밀)**: 절 \*경계\*만 보는 transition test 외에, \*절 내부\*도 ~500줄/다창 1 agent 전담 정독(`feedback_multiagent_review_chunking`; 거친 청크 금지).
- **G-readcov(읽기 커버리지)**: 근거 논문/교재는 해당 범위 전문 정독 + DOI 를 dossier 대조(신규 검증·추가), result Read Coverage 에 파일·범위 기록.
- **G-ground**: 모든 가정=AL-#+tier+cite+DOI(무태그 established 0).
- **G-noTransplant(정량)**: 기존 `_rebuilt`·`_clean` LaTeX 소스와 신규본 \*문자열 일치 수식·문장 0건\*(우연 동일식은 유도 서술이 달라야 PASS) — diff 로 측정.
- **G-latex**: 빌드 `!`=0·undefined ref/cite 0·dup label 0.

**충돌 규칙**: G-spine/G-bridge 와 G-noleap/G-ground 충돌 시 → 엄밀 단서는 box, 본문 사슬은 깨끗.

## Assumptions

- A1: 출발 재료는 (가)관찰+(나)5단계 의도+(다)물리 정전 \*뿐\*(사용자 명시). 절 구성·식·문장은 \*도출/백지\* — 기존 문건 미계승.
- A2: 식은 물리가 정하므로 백지 유도여도 정전과 같은 식에 도달할 수 있음 — 그건 transplant 아님(표현·구조·절진행을 베끼지 않고 G-noTransplant diff 0 이면 됨). \*이 논리를 "그러니 옮겨와도 된다"로 오용 금지\*(`feedback_execute_explicit_choice_not_judgment`).
- A3: grounding 인프라(AL/CHARTER/DOI/ledger)는 누적 자산이라 계승 — \*백지의 대상이 아님\*. (D-인프라 확인 필요.)
- A4: 빌드 환경 사용자 측; 정적 검수+PDF 확인. 부록 B 는 별도 보조 문서(D2 확정).

## Decisions Required (사용자 — 평문, 무응답 시 권고값; GO 후 정지 5조건 외 자동)

- **D-구조**: 절을 미리 고정하지 않고 \*위 논리 사슬에서 도출\*(잠정 덩어리: 무대/주역/분포/중첩/되먹임/닫힘/반증). 권고: 그대로. \*특정 절 구성을 따로 지시하셨다면 그 목록만 주면 사슬 덩어리화를 거기 맞춤.\*
- **D-인프라**: "백지"=tex 본문(식·문장·구조·절진행)에 한정, RB 인프라(AL-1~19·CHARTER 규약·DOI dossier·step 좌표 158–)는 \*계승\*. 권고: 그대로. \*완전 단절 새 트랙을 원하시면 그것만 명시.\*
- **D-파일/폐기**: 백지본 `graphite_ica_ch1.tex`; `_clean.tex` → `_discarded/`. 권고: 그대로.
- **D-기호표**: 독립 선두 표 대신 본문 first-use 정의 + 말미 compact 참조(지난 "기호 밑도끝도없이 등장"의 진짜 해법). 권고: 그대로.

## Correction History

| 일자 | 변경 |
|---|---|
| 2026-06-03 (BP v1) | 최초 clean-spine 계획. \*결함\*: 식·구조를 기존 문건서 옮기는 re-expose 혼입(완전 백지 불이행). |
| 2026-06-03 (BP2 v1) | 절간 다리(Bridge Map) 1급화. \*결함\*: 절 구성(서+§1~§10)을 폐기 대상 `_clean.tex`서 복사하고 "사용자 지시"로 오라벨(사용자 정정: 절 진행 복사 안 시킴); RB 인프라 무시·단절 좌표 신설; P3 게이트 0; 게이트 정성; G-usable 부재; 다리 잔존비약(시간→공간·ρ_G·implicit). |
| 2026-06-03 (FINAL v1) | **구조를 출발 재료서 도출**(논리 사슬 C0~C11, 절은 자연 덩어리)·사용자 정정 반영·**인프라 계승**(AL/CHARTER/DOI/step 158–, 백지는 tex 본문 한정)·**P3 7항목+CHARTER+G-usable+G-fine+G-readcov+G-noTransplant(정량) 게이트 추가**·비평3 다리 보강(C5 시간→공간·C6 $\rho_G$·C8 $\Theta$ first-use·C10 implicit→국소·$\mathcal A/\chi/C_\bg$ 동기)·step 좌표 정정(157 완주 후 이어감, "26 재개" 아님). |
