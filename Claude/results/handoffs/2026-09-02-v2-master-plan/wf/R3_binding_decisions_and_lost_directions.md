# R3 — 구속력 있는 결정·제약 등록부 (A) · 방향성 유실·park·미착수 등록부 (B)

> 작성 = 「v2.0.0 수식 연구 진보 마스터 플랜」 워크플로의 판독·등록부 초안 에이전트 [decisions] (Fable 5.1), 2026-09-03.
> 상위 문건 = `Claude/results/handoffs/2026-09-02-v2-master-plan/brief.md`(이하 brief). 본 문건은 brief §5 작업 챕터 1 의 Phase 1.3(유효 결정·제약 등록부)·1.4(방향성 유실·park·미결 등록부)가 채울 표의 **초안**이다. 최종 통합·commit 은 master 가 한다.
> 경로는 특별한 표시가 없으면 `D:\Projects\Project_Anode_Fit\Claude\` 기준이고, 프로젝트 지침은 `D:\Projects\Project_Anode_Fit\CLAUDE.md` 다.
> 보고 규약 = 4-tier(**확정** / **근거 미발견** / **추정** / **미검증**). 확정 행에는 path+line 을 붙였다. "사용자 결정"·"사용자 지적"이라는 표현은 brief §2 verbatim 발화와 원천 문건에 사용자 결정으로 기록된 항목에만 썼고, 그 밖의 판정(특히 「현재 상태」·「v2.0.0 승계」 열)은 본 에이전트의 판단이며 그 사실을 열 머리에 밝혔다.

---

## 0. 범위·방법·판정 규약

본 문건은 brief §3 이 본 에이전트에 배정한 원천 12건을 head→tail 전문 정독한 뒤, 현행 문건 `docs/v1.0.25.1/_sections/*.tex` 와 마스터 tex·프리앰블·서지 파일에 대한 확인용 grep 으로 각 항목의 **현행 집행 상태**를 대조해 작성했다. 정독 범위와 grep 대상은 말미 「Read Coverage」에 전건 기록했다. 원천 밖의 사실(예: `HANDOVER_v24.md` 의 FB0~FB9 리비전 내용, v1.0.20~v1.0.23 결정 이력 본문)은 정독하지 않았으므로 그 항목은 **미검증** 또는 **근거 미발견**으로 두었고, grep 으로 위치만 확인한 것은 "grep 위치 확인(전문 정독 아님)" 이라 적었다.

「현재 상태」 열의 값은 세 가지다. **존속** = 지금도 구속력이 있고 v1.0.25.1 에 실제로 반영돼 있거나 규범으로 살아 있음. **v1.0.25 한정** = 그 버전의 국소 수정 작업에만 걸리던 규약. **폐기** = 후속 결정·재편으로 효력을 잃음. 「v2.0.0 승계」 열은 본 에이전트의 판단(출처 = [decisions])이며, master 가 마스터 플랜 Non-goals·Assumptions 로 옮길 때 재판정한다.

등록부 B 의 「재개방 후보 여부」도 본 에이전트의 판단이다. "재개방" 은 과거에 지시·제안됐다가 절삭·park·미착수된 것을 v2.0.0 이론 진보 설계(brief 작업 챕터 3)의 정식 후보로 다시 올린다는 뜻이고, "신규" 는 과거 이력에 없던 후보, "승계 기각" 은 과거 기각 판정을 그대로 잇는다는 뜻이다.

---

## A. 현재 구속력 있는 결정·제약 등록부

### A-1. 헌법 3종과 D1~D6 (v1.0.15 CLOSING)

`docs/v1.0.15/CLOSING_v1.0.15.md` 는 스스로를 "다음 버전 계획서·실행의 상위 근거이며 HANDOVER·INDEX 보다 먼저 읽는다"(line 3)고 규정한다. 사용자 verbatim 은 line 9 에 있다: "이 문건의 제일 중요한 두가지는 교과서 수준의 문건, 논문의 깊이의 전문성이고, 세번째가 수식 주도의 문건이다. 수식만 쭉 따라가도 제대로 된 물리, 화학적 논리를 대부분 이해할 수 있는 수준의 문건." 이 세 조항은 2026-09-02 사용자 지시(brief §2 기준 1~4)와 내용이 일치하므로, 본 에이전트는 헌법 3종을 v2.0.0 의 게이트 축으로 **그대로 승계**하는 것이 맞다고 판단한다.

| 항목 | verbatim 또는 요지 | 출처 path+line | 현재 상태 | v2.0.0 승계 [decisions 판단] |
|---|---|---|---|---|
| 헌법 ① 교과서 register(최우선) | 안정·객관·정중한 어투, 완성된 물리를 그냥 제시, 교재는 자기 자신을 narrate 하지 않는다 | CLOSING_v1.0.15.md:11–16 | 존속(F-04 로 재확인·집행) | 승계 — 작업 챕터 2.5·6.2 게이트 |
| [D1] 자기 diff·버전 이력 서술 금지 | "구판은/이전에는/폐지했다" 류를 본문·각주·캡션·주석 어디에도 쓰지 않는다 | CLOSING_v1.0.15.md:13 | 존속 | 승계 — v2.0.0 이 대규모 재구조라 위반 유혹이 큼(v1.0.25 touch-up 도 "v1.0.24.1 대비" 표현을 본문에 남김: `_sections/ch1_sec10_sum.tex:145`) |
| [D2] 방어 어투 금지 | "X 가 아니다" 방어 서술 대신 긍정 서술 | CLOSING_v1.0.15.md:14 | 존속 | 승계 |
| 내부 라벨·고백조 누출 금지 | 작업단계 라벨·코드 함수명·"정직하게 적어두면" 류를 렌더링 텍스트에 넣지 않는다 | CLOSING_v1.0.15.md:15 | 존속(코드 함수명 조항은 P3 #8·F-11 로 강화) | 승계 |
| 연속성 | v1.0.14 목소리·구성 계승, 백지 재작성 지시가 아니면 뼈대·목소리를 끊지 않는다 | CLOSING_v1.0.15.md:16 | 존속 — 단 2026-09-02 지시는 "통합하든 수정하든 전혀 다른 새로운 이론을 끌고와서 엮든"(brief §2) 이라 백지 재작성을 **배제하지 않음** | 조건부 승계 — 목소리·자산(라벨·식)은 잇되 구조는 DG-A 결정에 따름 |
| 헌법 ② 논문 깊이 | 완결 유도, tier A/B/C 분리, 실측 검증 vs 자기일관성 검증 구분, DOI 병기, 1차 문헌 공백(Gn) 정직 노출 | CLOSING_v1.0.15.md:18–21 | 존속 | 승계 — 기준 3)·5) 와 직결 |
| 헌법 ③ 수식-주도 · [D3] | 각 결과 박스 = (a)출발식→(b)연산→(c)중간식≥1→(d)박스, "대입하면 [박스]" 점프 0 | CLOSING_v1.0.15.md:23–26 | 존속 | 승계 — 작업 챕터 2.2 의 boxed 64 판정 기준 |
| 완결 문장·orphan 0 | 전보체 괄호 금지, 절 도입/마무리 다리 의무 | CLOSING_v1.0.15.md:29 | 존속 | 승계 |
| 한글 prose + 영어 학술 원어 | 한글 번역 강요 X, 두문자어 첫 출현 병기, 특정 국적 표현 회피 | CLOSING_v1.0.15.md:30 | 존속(F-10 로 강화) | 승계 |
| [D4] 격자 잔재 0 · [D5] 대조 수식어 불요 · [D6] 스위치 잔재 본문 밖 | v1.0.15 특화 | CLOSING_v1.0.15.md:31 | 존속(격자 퇴출은 완료 상태; 재도입 금지 규범으로만 살아 있음) | 승계(재도입 금지 grep 항목으로) |
| 분량·그림 = 콘텐츠의 자연 결과 | 억지 조사-급 보완 라운드 금지 | CLOSING_v1.0.15.md:32 | 존속 | 승계 |

### A-2. CLOSING Part 2 프로세스 규율과 Part 4 w/T 결정

Part 2 는 문건이 아니라 **작업 방법**에 대한 사용자 지적을 규율화한 것이다. 2026-09-02 기준 6)("무슨일이 있어도 절대 나의 지침을 따를것")과 같은 방향이다.

| 항목 | 요지 | 출처 | 현재 상태 | v2.0.0 승계 |
|---|---|---|---|---|
| 2-1 제안·플래그 전 과거 이력 확인 | "새 이슈로 보이면 = 과거 이력을 아직 안 본 신호" | CLOSING_v1.0.15.md:38–41 | 존속 | 승계 — 작업 챕터 1 전체가 이 규율의 구현 |
| 2-2 지침·과거 이력 실제 확인 | 사용자 verbatim "내 지침이랑 과거 이력좀 제대로 확인좀해라." | CLOSING_v1.0.15.md:43–45 | 존속 | 승계 |
| 2-3 base 문건 전문 정독 후 착수 | 사용자 verbatim "하다못해 1.0.14 본 문건을 제대로 파악했으면 이런짓을 했을까?" | CLOSING_v1.0.15.md:47–49 | 존속 | 승계 — v1.0.25·v1.0.25.1 전문 정독이 작업 챕터 2 의 전제 |
| 2-4 흐름 끊는 UI 금지 | AskUserQuestion·자동 EnterPlanMode·Workflow 금지 | CLOSING_v1.0.15.md:51–54 | 존속(헌법 상시 조항) | 승계 |
| 2-5 명시 선택을 효율 판단으로 대체 금지 | 우려는 평문 1회, 말없이 바꿔 실행 X | CLOSING_v1.0.15.md:56–57 | 존속 | 승계 — 기준 6) 과 동일 취지 |
| 2-6 검증 없이 완료·골든 처리 금지 | 실증(해석적 극한 + Δ→0 수렴 + round-trip) 후 확정 | CLOSING_v1.0.15.md:59–60 | 존속 | 승계 — 작업 챕터 6.1 실행 기반 검증 렌즈 |
| Part 4 (1) 폭은 w 맨값이 아니라 n 으로 fit(w=n·RT/F) | 사용자 결정(이번 세션 사용자 결정, line 86) | CLOSING_v1.0.15.md:88 | 존속 — 현행 문건 폭 이중지위·n_j 가 이를 구현(`_sections/ch1_sec06_eqpeak.tex:106–112` 의 n_j 재척도 가드) | 승계 |
| Part 4 (2) T 는 실측 환경온도 투입 | 코드 `dqdv(V_app, T, …)` 스칼라/배열 T(V) 지원 | CLOSING_v1.0.15.md:89 | 존속 | 승계(코드는 Non-goal 이나 문건의 비등온 점별 평가 원칙은 승계) |
| Part 4 (3) 폭 T-의존 4단 사다리 | (i) 상수 n → (ii) per-T n 진단 → (iii) 상수 w 전환 → (iv) 최소 n(T) | CLOSING_v1.0.15.md:90–91 | 존속 — (i) 집행, (ii)~(iv) 는 다온도 데이터 의존(→ B-11) | 승계(이론 규칙으로) |
| Part 4 (4) n(T) 채택 시 가역열 config 항 동반 변경 | ∂w/∂T=(R/F)(n+T·n′) | CLOSING_v1.0.15.md:92 | 존속 | 승계 — 작업 챕터 3.2 사다리의 열특성 단계에 규칙으로 명기 |
| Part 4 (5) w 이중지위·use_w_eff 제거 | 단상 Ω≤2RT 평형 예측 폭 / 두-상 Ω>2RT 현상학 폭, Ω 는 히스테리시스에만 | CLOSING_v1.0.15.md:93 | 존속(v1.0.25 C5 로 "두-상 한정 금지"로 정련) | 승계 |

### A-3. 프로젝트 CLAUDE.md P1~P5

P3 는 제목이 "검수 7 항목"이나 실제로는 8 항이 있다(#8 은 v1.0.24 이후 추가, `CLAUDE.md:46`). 각 항의 **현행 문건 충족 상태**를 grep 으로 대조한 결과, P1 의 "Chapter 1~5" 원구상과 P3 #1·#6·#7·P5 의 일부 조항은 현행 문건(재료별 3장 + Part T)과 **표기가 어긋나 있다**. 이는 위반이 아니라 CLAUDE.md 가 v1.0.22 재편 이전 구조를 기준으로 쓰였기 때문이며, v2.0.0 계획서에서 어떻게 다룰지는 Decision Queue(DQ-2·DQ-4)에 올렸다.

| 항목 | verbatim 또는 요지 | 출처 | 현재 상태 | v2.0.0 승계 |
|---|---|---|---|---|
| P1 목표 | 흑연 음극 ICA(dQ/dV)·DVA(dV/dQ)를 열역학적/동역학적으로 설명하고 피팅 가능한 문건·방법론 | CLAUDE.md:11 | 존속 | 승계 — 2026-09-02 지시가 "열역학적, 동역학적 관점"을 재천명 |
| P1 원구상 Chapter 1~5 | Ch1 전하 보존식 기반 내부 전위 결정 → Ch2~5 발열·반응속도론·통합 상태방정식·히스테리시스 적층 | CLAUDE.md:13–17 | **부분 폐기(구조)** — 현행은 재료별 Ch1 흑연·Ch2 LCO·Ch3 Si + Part T(D22 재편, A-6) ; 다만 "전하 보존식 = 중심식"·"refs 6/7 실제 확인" 조항은 존속 | 조건부 — 구조 결정 DG-A 에서 P1 원구상과 D22 재편 중 무엇을 잇는지 명시(DQ-4) |
| P1 refs 6/7 "실제 확인한 뒤 반영" | 사용자 논문 JCP 147(14) 144111 (2017) 의 ref. 6, 7 | CLAUDE.md:16 | 존속 — 서지는 Crossref 확정(`_sections/ch1v22_bib.tex:46–47`), 원문은 미소장(brief §4.1) | 승계 — DR-8 |
| P2 경계 | `Codex/` 읽기·쓰기 금지(운용 지침 문건만 예외), 원천 자료 덮어쓰기 X, 계획서=`Claude/plans/`, 산출=`Claude/results/` | CLAUDE.md:21–28 | 존속 | 승계 |
| P3 #1 V_n 계열 구분 일관 | `V_n`, `V_{n,app}`, `V_{n,drive}`, `V_{n,OCV}` | CLAUDE.md:34 | **표기 스테일** — 현행 문건에 `V_{n,…}` 형 기호 0건(grep `V_\{n,` = 0), 현행 체계는 두 전위 `V_app`·`V_n`(F-01 keybox, `USER_FEEDBACK_v1024_READING.md:17`) | 승계하되 현행 기호로 재해석(DQ-2) |
| P3 #2 전하 보존식 = 중심식 | OCV 에서 읽는 흐름으로 회귀 X | CLAUDE.md:35 | 존속·충족 — `_sections/ch1_sec02b_part0.tex:286–350`(전하 보존 음함수 = 대정준 제약 반전), `ch2_sec08_synthesis.tex:37·50` | 승계 |
| P3 #3 순환 의존 dependency graph | ξ_j·Q_bg·dQ/dV·dV/dQ 의 self-consistent loop 표시 | CLAUDE.md:36 | 존속 — 부록 E 가 담당(`ch1_appE_selfconsistent.tex:29` Volterra 자기일관) ; 표/그래프 형태 여부는 **미검증**(appE 본문 미정독) | 승계 — 작업 챕터 3.4 |
| P3 #4 4분류 진단 | 정의상 implicit / 수치해법 필요 / 논리 공백 / 물리 가정 충돌 | CLAUDE.md:37 | 존속 — `ch1_sec02b_part0.tex:355` "논리 공백이 아니라 … implicit" 식 서술 존재 ; 4분류 표 형태 여부 미검증 | 승계 |
| P3 #5 refs 6/7 5항 sub-section | 서지·위치·수학 구조·변수 매핑·물리 가정 차이 | CLAUDE.md:38–43 | 존속·충족 — `ch1_appE_selfconsistent.tex:113` `\subsection{ref. 방법론 도입 기록 --- 서지·위치·구조·매핑·가정차}\label{sec:sc-p35}` | 승계 |
| P3 #6 Ch1 기준식 ↔ Ch2~5 전달식 정합 | `ver.N 으로 전달되는 기준식` 절 | CLAUDE.md:44 | **표기 스테일** — 현행 문건에 `ver.N` 문자열 0건(grep) ; 정합 대상은 Ch1↔Part T↔Ch2 LCO↔Ch3 Si 의 xr 교차참조 | 승계하되 대상을 현행 구조로 재정의 |
| P3 #7 ver.N ↔ Chapter N 혼동 금지 | 역사 명칭 vs 새 구조 명칭 명시 매핑 | CLAUDE.md:45 | 존속 — brief §5 머리말이 3축(작업 챕터/문건 Chapter/역사 ver) 대응 주석을 요구 | 승계 |
| P3 #8 코드 = 부록 전용 | 본문 절 grep 코드 토큰 = 0 이 확인 가능 게이트 | CLAUDE.md:46 | **존속·현행 미충족 3건** — 본문(비부록) `\code{}`·`\texttt{}` 잔존: `_sections/ch1_sec10_sum.tex:145`(`\code{use\_si\_constants()}`), `ch2_sec08_synthesis.tex:56`(동일 토큰, Part T 본문), `ch3v22_sec02b_sifr.tex:43`(`\texttt{V1025\_DATA\_ADDENDUM.md}` 파일명). 셋 다 v1.0.25 C3/C9 정직화 문장이 만든 것. §3.5 코드 명세절은 `\appendix` 뒤로 이동됨(`ch3_si_v1.0.24.tex:30–31`) ; 서지 내 코드 인용은 제거됨(`ch1v22_bib.tex` grep 0) | 승계 — 게이트 grep=0 은 base 부터 3건 위반이므로 작업 챕터 2.5 GAP 등재(DQ-1) |
| P4 시작 체크리스트 8항 | 활성 폴더·원천 목록·전문/부분 분리·기존 계획서·cumulative step·중단 조건·검증 명령·저장 위치 | CLAUDE.md:52–59 | 존속 | 승계 — 마스터 플랜 §Current Ground Truth·§Test Plan 에 대응 |
| P5 이름·구조 보존 | 변수명·기호·라벨·식 번호·한글 표현 임의 변경 X ; `ver.N으로 전달되는 기준식` 절 제목 보존 ; Ch1 기준식 확정 전 Ch2~5 정합 완료 보고 X ; 추가 개선 후보는 수정하지 말고 보고 | CLAUDE.md:63–67 | 존속(첫·넷째 조항) / **스테일**(둘째·셋째 — `ver.N` 절이 현행 문건에 없음) | 첫 조항은 "자산 무유실 원칙"으로 승계, 넷째 조항은 작업 챕터 3.7 정지 게이트로 승계 |

### A-4. 사용자 정독 피드백 F-01~F-11 (v1.0.24 접수 → 집행 완료·규범 존속)

`results/comp_v24/USER_FEEDBACK_v1024_READING.md` 는 접수 시점 문건이라 전 항목 상태가 "접수(미착수)"다(line 206). 집행 기록(FB0~FB9 리비전)은 `HANDOVER_v24.md` 소관이며 본 에이전트의 정독 범위 밖이다. 따라서 아래 「현재 상태」는 **현행 v1.0.25.1 파일 grep 으로 직접 확인한 사실**만 확정으로 적고, grep 으로 판정할 수 없는 항목(문체 스윕·Ch2 도입부 분량)은 미검증으로 두었다.

| 항목 | 사용자 지적(요지) | 출처 | 현재 상태(v1.0.25.1 직접 확인) | v2.0.0 승계 |
|---|---|---|---|---|
| F-01 §1.1.4 필요성 | 물리 이해에 필수가 아닌 "알아두면 좋은" 절 | USER_FEEDBACK:12–22 | 절은 **유지**됨(`_sections/ch1_sec01_n0n1.tex:190` `\label{sec:pointwise}` 존재) ; 축약·강등 여부 미검증 | 승계 — 작업 챕터 2.5 에서 (a)(b) load-bearing / (c)(d) 배경의 분리 재판정 |
| F-02 확률 P → 소문자 p | 압력 P 는 유지, 확률만 소문자 | USER_FEEDBACK:26–34 | **집행 확인** — `ch1_sec02a_part0.tex:47·60·77` 에 `p_i` | 승계(노테이션 규약 A-7) |
| F-03 f_int·s_int 소문자 직관성 | 대문자 총량 / 소문자 자리당 규약과의 충돌 | USER_FEEDBACK:38–45 | **집행 확인(옵션 i)** — `ch1_sec02a_part0.tex:319` "소문자 f --- 계 전체 Helmholtz F 가 아니라 자리당 양" 명시, `:321` `s_int` | 승계(자리당 소문자 규약 유지) |
| F-04 전공서적 문체(전역·최우선·재발) | 구어·수필·역사서체 잔존, "수십 차례" 요청 | USER_FEEDBACK:49–74 | **제목 레벨 집행 확인** — F-04 표의 문제 제목 11종 렌더 텍스트 잔존 0(유일 잔존 = `ch2_sec00_intro.tex:1` % 주석) ; 본문 산문 스윕은 grep 으로 판정 불가 → **미검증** | 승계 — 작업 챕터 2.5·6.2 |
| F-05 절 제목의 N-태그 | "(N2)" 등 내부 파이프라인 코드 제목 노출 | USER_FEEDBACK:78–88 | **집행 확인** — `\section`·`\subsection` 제목 내 `(N#)` 0건 | 승계 |
| F-06 조판 밀도 완화 | 줄간·문단·여백·microtype·인라인→디스플레이 승격 | USER_FEEDBACK:92–108 | **집행 확인** — `_sections/common_preamble_v1024.tex:9` margin=25mm · `:23` microtype protrusion · `:24` setstretch 1.16 · `:25` parskip 0.55em ; 인라인→디스플레이 승격 범위 미검증 | 승계(프리앰블 규약) |
| F-07 E.3 서지 라벨 좌측 잘림 | `\item[\textbf{①…}]` 커스텀 라벨 5곳 | USER_FEEDBACK:112–121 | **집행 확인** — `ch1_appE_selfconsistent.tex` 에 `\item[` 0건 ; 렌더 기반 시각 게이트 권고(line 116)는 규범으로 승계할 것 | 승계 — 작업 챕터 6.3 빌드 게이트에 "렌더 육안 점검" 추가 후보 |
| F-08 Ch2 도입부 "같은 점" 최소화 | σ_d·추가된 점 중심 | USER_FEEDBACK:139–150 | 미검증(분량 판정 필요) | 승계 — 재료 적용 파트 저작 원칙 |
| F-09 식 2.39 cases 우측 넘침 | cases 내부 긴 국문 | USER_FEEDBACK:154–161 | **집행 확인** — `ch1_sec16b_lcoomega.tex:100–103` cases 분기 텍스트 단축 | 승계(조판 규범) |
| F-10 억지 한글화 금지(전역·용어 정책) | 요동·양성 등 일본식 calque 배제, 표준 용어(정준/대정준)는 사용자 판단 | USER_FEEDBACK:165–176 | **집행 확인** — 비주석 행 "요동" 0건·"양성 유일근" 0건 ; "음함수(implicit function)"·"섭동(perturbation)" 은 한글 유지+영어 병기(`ch1_sec02b_part0.tex:286`, `ch1_appE_selfconsistent.tex:163`) ; "정준/대정준" 유지 | 승계 — 용어 결정 표 = A-7 |
| F-11 코드 = 부록 전용(전역·최우선·POLICY) | 본문·그림·캡션·표·제목 절대 금지 + 이력 승계 실패 지적 | USER_FEEDBACK:180–202 | **대부분 집행 확인** — ①② 열거 파일의 토큰은 제거(sec05b·lcoomega·sifr 본문·blend 캡션 grep 0) ; ③ §3.5 코드절 → `\appendix` 뒤 이동(`ch3_si_v1.0.24.tex:30–31`) ; 서지 내 코드 인용 제거 ; **단 v1.0.25 신규 3건 잔존**(A-3 P3 #8 행) | 승계 — 재발 방지 게이트 grep=0 은 이미 CLAUDE.md P3 #8 로 명문화됨 |

### A-5. v1.0.24/25 결정 (D-A~D-D · DG-1 · DG-2 · 물리 판정 · 계약)

| 항목 | verbatim 또는 요지 | 출처 | 현재 상태 | v2.0.0 승계 |
|---|---|---|---|---|
| D-A @2 비대칭 커널 opt-in | 전이 dict `alpha` 키, 부재=1.0=bit-exact | v1025 plan:12 (사용자 확정 2026-07-26) | 존속(문건 `eq:skewpeak`·`eq:skewapex` 신설) | 승계 — 단 α 는 tier C 현상학 파라미터(아래) |
| D-B gallery opt-in 유지 | 기본 전이 수 승격 X, `GRAPHITE_STAGING_MSMR6_LIT` 존치 + Si opt-in | v1025 plan:13 | 존속 | 승계(코드 Non-goal 이나 "gallery ≠ 상" 서술 규범) |
| D-C regsol/@1/@3/@4 커널 배제 | 해석적 유도 `eq:sifr-kernel`·`eq:sifr-blend` 는 유효 물리로 보존, "미채택·코드 미구현" 명기, Ω 파라미터 전량 존치 | v1025 plan:14 | 존속 | 승계 — 작업 챕터 2.6 의 입력 |
| D-D 국소 수정 원칙 | 물리 골격·식 번호·`\label`·변수명·한글 표현 불변, 신규는 additive | v1025 plan:15 | **v1.0.25 한정** — brief §4.4 가 명시 | 원칙 자체는 미승계 ; "자산 무유실"(라벨·식 번호 체계 유실 0)만 승계 |
| DG-1 regsol (b) 완전 삭제 | 사용자 verbatim "regsol 삭제" ; G-R3 "삭제 확인" 게이트 재작성 | v1025 plan:16·210–216 ; HANDOVER_v25:46 | 존속(코드) | 승계 사실로 기록 — v2.0.0 이 정칙용액+Maxwell 을 재개방하면 "코드 삭제된 커널의 문건 재도입"이 되므로 D-C 지위 warnbox 와의 정합을 결정해야 함(DQ-7 · B-4 #4 행) |
| DG-2 파일명 유지 | 사용자 verbatim "파일명을 왜 바꿔? 버전명만 바꿔주면 되는거 아니냐?" | v1025 plan:17·217–219 ; HANDOVER_v25:47 | **v1.0.25 한정**(brief §4.4) — 마스터 tex `*_v1.0.24.tex`·xr 키·`common_preamble_v1024` 유지 | 미승계(v2.0.0 새 폴더·새 파일명 가능) ; 단 규약 취지("불필요한 개명 X")는 존중 |
| C3 상수 SI opt-in(집행 정정) | 즉시 교체는 골든 bit-exact 와 수학적 양립 불가 → `use_si_constants()` opt-in | v1025 plan:105·129·230–231 ; HANDOVER_v25:81–84 | 존속 | 코드 Non-goal ; 문건 표시 상수 = CODATA-2018(25.693 mV) 승계 |
| 골든 bit-exact 계약 | G1 `max|d|=0`, 기본 데이터셋 무변경 | v1025 plan:181 ; HANDOVER_v25:55 | 존속(코드) | 코드 Non-goal — 문건 확정 후 doc-leads 플랜의 계약 |
| Ω 물리 전량 유효 | 삭제된 것은 dQ/dV 커널뿐, `func_dU_hys`·`func_dH_a_eff`·§7 상성격 판정 존치 | HANDOVER_v25:136–137 | 존속 | 승계 |
| gallery ≠ 상 | 7·9전이 중심이 기존 3위치에 ΔU<12 mV 근축퇴, XRD 상 수(4 staging·두-상 2) 불변, "봉우리 수를 상 수의 증거로 제시하지 말 것" | HANDOVER_v25:95–97 ; v1025 plan:59–61·201 | 존속 | 승계 — 이론 설계의 경계 조건 |
| @2 α = 현상학 형상 파라미터(tier C) | 새 물리·새 상 아님 ; 순수 비대칭 손잡이도 아님(폭·정점 동반 이동) ; 4-손잡이 축퇴(α·L_V·gallery·w_j) | HANDOVER_v25:73–77·143–144 ; v1025 plan:199–201 | 존속 | 승계 — 작업 챕터 3.2 에서 α 를 정칙용액/Ω(ξ) 비대칭의 현상학 극한으로 회수할 수 있는지가 설계 과제 |
| $w_\mathrm{eff}$ 를 폭으로 읽기 금지 | 허용 = 단상 중심 높이 지표뿐 ; FWHM ∝ λ^{3/2}(`eq:gr2l-fwhm`) ; Ω=2RT 초과 시 Maxwell 불연속 | HANDOVER_v25:90–94·145–147 ; v1025 plan:107·142 | 존속 ; G-금지 게이트 미구현(N11)이라 사람이 지키는 규율 | 승계 — 6.2 grep 게이트 후보로 기계화 |
| $C_\mathrm{bg}$ = 창-국소 상수 근사 | 배경 감쇠는 실재(4셀 일치), 창 확장 시 광폭 종 필요, skew 동반 시만 이득 | HANDOVER_v25:101–102 ; v1025 plan:110·203 | 존속 | 승계 |
| comp_v24 무수정·addendum 우선 | 읽는 순서 = 원본 → `V1025_DATA_ADDENDUM.md`(충돌 시 addendum) | HANDOVER_v25:150–152 | 존속 | 승계 — 작업 챕터 1.2 정독 순서 규칙 |
| 원본 아카이브 불가침 | `docs/v1.0.24/`·`v1.0.24.1/` 무변경 | HANDOVER_v25:153–154 | 존속 ; brief §6 가 v1.0.25·v1.0.25.1 까지 확장 | 승계(Non-goal) |
| 회사 데이터 위임분(Task #38) | stage-2L 0.30 mV/℃·Ω 점값·O3-LCO 전자항 T-의존·α↔L_V 율속 분리 | HANDOVER_v25:122 ; v1025 plan:204 | 존속(미완 N13) | 승계(Non-goal — warnbox·tier 정직 표기) |
| 모델 배분(v1.0.25 한정) | "물리·화학 논리를 건드리는 문건 작업은 Opus 5.0, 나머지는 Opus 4.8"(요지 인용) | HANDOVER_v25:48 ; v1025 plan:235–236 | **폐기** — 2026-09-02 사용자 지시 "이 작업은 모델 배정을 예외적으로 모두 페이블 5.1로 진행한다"(brief:45) | 미승계 |

### A-6. D21/D22 계열 (v1.0.21·v1.0.22 결정 — grep 위치 확인, 전문 정독 아님)

brief 가 열거한 "D21/D22 계열"은 본 에이전트 배정 원천에 본문이 없어 grep 으로 위치만 확인했다. 내용 요지는 grep 결과 행의 문면에서 옮긴 것이며, 그 결정의 상세 조건·예외는 **미검증**이다.

| 항목 | 요지(grep 행 문면) | 출처(grep) | 현재 상태 | v2.0.0 승계 |
|---|---|---|---|---|
| D21-1 항법 적용판+미적용판 이원 빌드 | `\ifnavaid` 토글·드라이버 2본 | `docs/INDEX.md:43` ; `docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md:5·13` | **폐기** — D22-1 항법판 폐기(`plans/2026-07-17-v1022-master-plan.md:24`) | 미승계 |
| D21-2 일반 top3 | 끝-대-끝 계산 예제·Ch1↔Ch2 로드맵 표·측정 원리 bgbox | `V1021_EXECUTION_LEDGER.md:14–15` | 존속(현행 §1.1.4 bgbox 등이 그 잔존 — F-01 대상) | 승계 여부는 F-01 재판정과 연동 |
| D21-3 Si = 예비 부록 → 독립 장 단계화 | | `docs/INDEX.md:43` | 집행 완료(Ch3 독립) ; `_sections/ch1_appD_si.tex` 는 ch1 마스터 `\input` 목록에 없음(`ch1_graphite_v1.0.24.tex:54–58`) → **빌드 미포함 잔존 파일(추정: v1.0.22 승격 후 잔존)** | 자산 지도(2.1)에서 "빌드 미포함 파일" 명시(DQ-6) |
| D21-5 요동-응답 포함 | 대정준 전하 보존 소절 `sec:sm-mc` 에 합류 | `docs/v1.0.21/results/V1021_CHANGE_LOG.md:10` | 존속·집행 | 승계 |
| D21-6′ Fable 마스터 세션 단독 저작 | | `HANDOVER_v1.0.21.md:7` | v1.0.21 한정 | 미승계(v2.0.0 은 전원 Fable 5.1 유닛 분업) |
| D22 v1.0.22 전건 확정 | 활물질별 재편·Si–C·서지 저비용+승급 규칙·인용 다리 12곳·통계역학 증축 GO[사후 제거 조항]·병합 시험 금지[사용자 별도 세션] | `docs/v1.0.21/HANDOVER_v1.0.21.md:18` | 존속(현행 구조의 근거) | **DG-A 와 직접 충돌 가능** — brief 3.3 (b) Part I/II 재구조는 D22 활물질별 재편을 supersede 하는 사용자 결정이어야 함(DQ-3) |
| D22-1 항법판 폐기 | 단일판 | `plans/2026-07-17-v1022-master-plan.md:24` | 존속 | 승계 |
| D22-3 Si 케이스 셋(원소 Si/SiO$_x$/Si–C) | | `…v1022-master-plan.md:12` | 존속 | 승계 |
| D22-4 서지 저비용+승급 규칙 | 조사는 저비용 모델, 부족 시 한 단계 승급 | `…v1022-master-plan.md:25` ; `docs/INDEX.md:30` | 존속 | 모델 배분은 2026-09-02 지시로 대체(전원 Fable 5.1) ; "서지 검증 후 등재" 규율은 승계 |
| D22-8 병합 빌드 금지 | 3장 분리 빌드·xr 교차참조 유지, 병합은 사용자 별도 세션 | `plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md:72` ; `…v1022-master-plan.md:47` | 존속 | **결정 필요** — v2.0.0 이 단일 문서인지 3장 분리+xr 인지(DQ-3) |
| D22 "사후 제거 조항"(통계역학 증축) | 혼란 가중 시 빼라 — SM2 세 블록이 제거 용이 독립 bgbox 로 설계된 근거 | `SM2_SURVEY.md:133` | 존속 | 승계 — 일반 이론 파트 증축 시 같은 원칙 |

### A-7. 노테이션·용어·코드=부록·자산 태그·서지 원장 규약

| 항목 | 규약 내용 | 출처 | 현재 상태 | v2.0.0 승계 |
|---|---|---|---|---|
| 확률 소문자 p / 열역학 상태함수 대문자 유지 | 압력 P·Helmholtz F(총량)·엔트로피 S(총량) 대문자, 확률 p_i 소문자 | USER_FEEDBACK:27·31 ; `ch1_sec02a_part0.tex:47·60·77` | 존속 | 승계 — 기호표(작업 챕터 4.0)에 규약으로 명문화 |
| 자리당(intensive) 소문자 f_int·s_int / 총량 대문자 F·S | | USER_FEEDBACK:42 ; `ch1_sec02a_part0.tex:319–321` | 존속 | 승계 |
| Helmholtz F vs Faraday F | "기호만 같고 문맥으로 갈린다" 명시 처리 전례 | USER_FEEDBACK:31 | 존속 | 승계 — 일반 이론 파트에서는 충돌 빈도가 커지므로 기호표에서 재점검 권고 |
| 용어 정책 | 국문 문단 + 용어 억지 한글화·일본식 calque 배제 ; 요동→fluctuation ; 음함수·섭동은 한글+영어 병기 ; 정준/대정준·분배함수 표준 한글 유지 | USER_FEEDBACK:172–175 ; grep 결과(A-4 F-10 행) | 존속 | 승계 — v2.0.0 신규 개념(Onsager·affinity·flux-force 등)의 용어 결정 표를 4.0 에서 선제 작성 권고 |
| 코드 = 부록 전용 | A-3 P3 #8·A-4 F-11 | | 존속(현행 3건 위반) | 승계 |
| 자산 태그 체계 | 각 절 말미 `% 자산…[태그]` 주석 — 태그 계열 = `[C-nn]`·`[V21-Qn-nn]`·`[V22-SM2-X]`·`[V22-R5-nn]`·`[LCOΩ-n]`·`A-0nn` 등 다계열 ; `% 자산` 주석 46건·31파일, 태그 패턴 138건·34파일(grep) | `_sections/ch1_sec06_eqpeak.tex:119`, `ch1_sec02b_part0.tex:409`, `ch2_sec07_revheat.tex:95–100`, `ch3v22_sec04_mech.tex:107`, `ch1_sec16b_lcoomega.tex:155–160` | 존속 | 승계 — brief §4.4 의 `[A-xxx]·[E-xxx]` 표기는 실제 계열과 다름(DQ-11) ; v2.0.0 은 "승계/회수/신규" 3분류 태그 설계 필요 |
| 서지 원장 규약 | `V10xx_REFERENCE_LEDGER.md` 의 V1 키만 인용 ; 표준 정리는 무인용 관용 ; 기억 기반 서지 0건 | `SM2_SURVEY.md:5·130` ; brief §5 3.5 | 존속 — 원장 파일 최신 = `docs/v1.0.23/results/V1023_REFERENCE_LEDGER.md`(glob) ; v1.0.24/25 원장 파일 **근거 미발견** ; 현행 bibitem 95(`ch1v22_bib` 44 + `ch2v22_bib` 15 + `ch3v22_bib` 36) | 승계 — 작업 챕터 2.4 에 "V1023 원장 ↔ 현행 95 bibitem 대조" 게이트(DQ-5) |
| 서지 정직 단서 표기 | 유료 전문·저널판 미확인·저자 미확인은 명시 | LIT_ADVANCE:129 ; IMPROVEMENT:77 | 존속 | 승계 |
| 빌드·구조 게이트 | xelatex 3-pass err0·undefined 0 ; `tools_check_structure.py check`(JSON 모드 금지) | brief §4.1 ; v1025 plan:189–191 | 존속 | 승계 |
| 렌더 육안 게이트 권고 | 좌측 흘러넘침은 Overfull 경고를 내지 않음 | USER_FEEDBACK:116 | 규범(미기계화) | 승계 후보 |

### A-8. 2026-09-02 사용자 지시 (최신·최상위 구속)

brief §2 verbatim 을 등록부 항목으로 분해한다. 이 지시는 위 A-1~A-7 의 어느 항목과도 모순되지 않으며, 모델 배분(A-5 마지막 행)만 명시적으로 대체한다.

| 항목 | verbatim | 출처 | v2.0.0 승계 |
|---|---|---|---|
| Codex 무접근 | "코덱스가 지금 지 나름대로 뭔가를 하고 있는데 … 그냥 놔둬." | brief:31 | Non-goal |
| 이력 전수 파악 → 두 버전 검토 → 진보 | "지금까지 클로드로 진행한 모든 작업 이력 버전 변경점들, 마스터 플랜들, 버전별 이력을 파악하고, … 현재의 가장 1.0.25 두 가지 버전을 검토하고, … 물리적, 화학적, 특히 열역학적, 동역학적 관점에서 이 수식 연구의 진보를 이뤄야한다." | brief:33 | 작업 챕터 1→2→3 골격 |
| 기준 1) 유도에 가까운 전개 | "수식만으로도 80~90% 이상의 내용을 이해할 수 있을정도로 비약, 누락, 생략 없는 거의 유도에 가까운 수식 전개" | brief:36 | 헌법 ③·[D3] 강화판 — 2.2 게이트 |
| 기준 2) 대학원 교재 수준 설명 | "포맷은 대학원 수준의 열역학, 통계역학, 동역학 교재 수준의 상세한 설명" | brief:37 | 헌법 ① 강화판 — 2.5 게이트 |
| 기준 3) 리뷰 논문급 레퍼런스 | "리뷰 논문급의 빈틈 없는 레퍼런스 작업 및 내용" | brief:38 | 헌법 ② 강화판 — 2.4·5.x |
| 기준 4) 청중 | "전공은 다를지언정 석박사급 인력" | brief:39 | 2.5 가독성 판정 기준 |
| 기준 5) 일반식 → 간소화 | "최대한 일반화된 식을 유도하고 거기서 우리가 필요한 방향으로 수식을 간소화할 수 있는 레퍼런스가 확실한 가정" | brief:40 | 3.2 "일반→특수" 사다리의 근거 |
| 기준 6) 방법론 | "작업 방식은 나의 계획 스킬, 지침을 따를 것. 마스터플랜 - 세부계획서 - 작업이력서 단계. 무슨일이 있어도 절대 나의 지침을 따를것. … 나는 효율이 아닌 결과물의 완성도 신뢰도를 중요시한다." | brief:41 | 운용 §7 전건 |
| 모델 배분 예외 | "이 작업은 모델 배정을 예외적으로 모두 페이블 5.1로 진행한다." | brief:45 | 운용 — 헌법 배분표의 사용자 명시 예외 |

### A-9. anodefit MASTER plan 의 결정 상태

`plans/2026-07-18-anodefit-MASTER-plan.md` 는 "방향성 확인용 … GO 대기"(line 5)로 작성됐고 D1~D7(line 109–126)에 대한 사용자 응답은 본 에이전트 정독 범위에서 **근거 미발견**이다. 다만 v1.0.24 가 "A(브로드닝·M 제거) + D 착수(검증)"(line 82)로 실제 진행됐다는 사실(brief §4.3 계보 "v1.0.24 공개데이터 검증 캠페인")로부터 D2 기본값(Campaign A)이 채택됐다고 **추정**한다. 사용자 결정으로 기록된 것은 "BDD 는 스코프 밖(사용자 결정)"(line 101) 하나다. 북극성(line 11–16)과 "M = 브로드닝으로 낮아진 피크가 dV/dQ 에서 커진 것처럼 보인 상황을 억지로 맞춘 인자"라는 핵심 통찰(line 23, "사용자·본 문건 작업 중 규명")은 v2.0.0 이론 진보의 **동기 층**으로 승계하는 것이 옳다고 본다 — 단 캠페인 B·C·E 는 brief §6 Non-goal 이다(B-8).

---

## B. 방향성 유실·park·미착수 등록부

### B-1. 계보 감사가 적발한 사용자 방향 미계승분 (FABLE_AUDIT §4·§5)

`docs/Fable_점검/FABLE_AUDIT_01_history_v3-v1011.md` §4 표(line 44–54)는 "v12 결정 대상"으로 다섯 항목을 올렸고 §5-8(line 64)이 "Phase 4.1 명시 결정 항목"으로 재열거했다. 본 에이전트 정독 범위(v1.0.15 CLOSING·v1.0.24/25 문건)에서 이 다섯 항목이 **명시적으로 결정된 기록을 찾지 못했다**(근거 미발견). 현행 문건 grep 으로 확인한 처리 상태는 아래와 같다.

| 항목 | 원 지시 시점·출처 | 현행 처리 상태(v1.0.25.1 grep) | 재개방 후보 [decisions 판단] | 근거 |
|---|---|---|---|---|
| ★Eyring 근본식이 척추 | 사용자 2026-06-11 "모든 것이 Eyring 식에서 뻗어야" → Fable v2 유일 완전 구현 | **미계승 지속** — Eyring 은 §5 TST bgbox(`_sections/ch1_sec05_width.tex:13–14·88·112`)·§8 lag(`ch1_sec08_lag.tex:100`)·Part 0 합류 1문장(`ch1_sec02b_part0.tex:207`)의 **국소 유도**로만 존재 ; 척추는 코드 spine N0~N9 | **재개방(1순위)** — 2026-09-02 기준 5)(일반식→특수식)와 동역학 축의 자연 출발점이 TST/Eyring 이므로 작업 챕터 3.1 동역학 축·3.2 사다리 "동역학 일반(TST)→lag→동결" 에 정식 후보 | FABLE_AUDIT:47·64 ; brief §5 3.1 |
| 역방향 식별 사슬 S0~S5·16-울타리 | v5/v6 → v7 절삭 | **미복원** — `S0`·`역방향 식별`·`16-울타리` 본문 0건(유일 매치 = `ch2_sec08_synthesis.tex:165` 주석의 `dS0_j`) | 재개방 검토 — G-usable(피팅) 관점 ; 단 §18 입력 절(`ch1_sec18_inputs`)이 4-손잡이 식별 가드로 부분 대체했으므로 "무엇이 유실됐는가"를 v5/v6 원문 대조로 먼저 확정해야 함(작업 챕터 1.2) | FABLE_AUDIT:50 ; HANDOVER_v25:143–144 |
| §1.18 적층 준안정·athermal 훅 | Opus v4 순수 추가 158줄 → v5 부터 park | **park 지속** — `athermal` 0건 ; "준안정" 은 히스(§4)·broadening(§7)·Si Li₁₅Si₄ 맥락에만 존재(`ch1_sec04_hys.tex:7·13–14·255`, `ch1_sec07_broadening.tex:86·94`) | 재개방 검토 — v2.0.0 열역학 축 "sublattice/staging·transfer matrix" 후보(brief 3.1)와 같은 자리 ; v4 §1.18 원문 정독 후 판정 | FABLE_AUDIT:51 |
| KWW/장벽분포 꼬리 일반형 | v3~v5 → v7 절삭, v10 은 apparent-U/η 로 부분 대체(2026-06-30 [MODEL-1 선택] 의도적 scope-out) | **scope-out 지속** — `KWW`·`stretched`·`장벽분포` 0건 | 재개방 검토(조건부) — brief 3.1 동역학 축이 "master equation/Fokker-Planck·KWW/장벽분포" 를 후보로 명시 ; 단 v10 의 [MODEL-1 선택]이 사용자 결정인지 master 결정인지 **미검증** → 재개방 전 그 기록 확인 필요 | FABLE_AUDIT:52 |
| "논문수준 논리를 학부생도" — LCO 6절 산문 잔존 | RB·상시 → v9 기원 | 부분 계승 — v1.0.19 Fable 전면 재작성(brief §4.3)이 Ch1+Ch2 를 수식화했으나 현행 LCO 장 산문 비율은 **미검증** | 작업 챕터 2.2 에서 boxed 64 판정 시 LCO 장 산문 비율을 별도 계측 권고 | FABLE_AUDIT:48 |
| "실제 표현에 필요한 수식만"(v7) vs 자기완결 교과서 | 두 지시의 긴장 — "v12서 명시 조율 필요" | **미조율 기록** — 2026-09-02 기준 1)·2)(비약 없는 유도·교재 수준)가 사실상 자기완결 쪽으로 결정한 것으로 읽힘 | 재개방 아님 — 초안에 "이 긴장은 2026-09-02 지시로 해소"라고 적되 사용자 확인 권고(DQ-13) | FABLE_AUDIT:54·64 ; brief:36–37 |
| v12 병합 전략(v5 식 사슬 + v3 산문 다리 + v10 broadening + v8 G-derive + v1.0.11 P1.1 supplement 흡수) | FABLE_AUDIT §5-7 | v1.0.12 N=10 경쟁·체리픽(brief §4.3)이 이를 집행했다고 **추정** ; P1.1 supplement 흡수 여부 미검증 | 작업 챕터 1.2 v1.0.12 행에서 확인 | FABLE_AUDIT:63 |
| 설계서 자체 adversarial·실행 기반 검증 렌즈 상설·수렴 후 편집 게이트 재실행 | FABLE_AUDIT §3·§5 교훈 1~6 | 규범으로 존속(A-2 2-6 와 정합) | 승계 — brief 3.6·6.1 이 이미 반영 | FABLE_AUDIT:37–42·57–62 |

### B-2. CLAUDE.md P1 원구상 Chapter 2~5 의 현행 대응

P1(`CLAUDE.md:17`)은 "Chapter 2~5 는 Chapter 1 기준식 확정 후 발열·반응속도론·통합 상태방정식·히스테리시스 계층으로 적층"이라 했다. 현행 문건은 재료별 3장 + Part T 로 재편됐으므로(A-6 D22), 원구상의 네 계층이 어디로 갔는지를 매핑한다. 이 매핑은 본 에이전트의 grep 기반 판정이다.

| 원구상 계층 | 현행 대응 위치 | 처리 상태 | 재개방 후보 |
|---|---|---|---|
| 발열 | Part T `ch2_sec07_revheat.tex`(Bernardi 에너지 수지 `:11–48`, 켤레 쌍 `:78–92`), `ch2_sec08_synthesis`, `ch2_sec09_method:25` | **재편 흡수(가역 발열 한정)** — 비가역 소산·entropy production 은 1문장 언급(`ch2_sec05_mixing.tex:233`)뿐 | 재개방 — brief 3.1 열 축(entropy production·Bernardi) ; 4.4 "엔트로피 분해·가역발열·entropy production" |
| 반응속도론 | §5 TST bgbox(`ch1_sec05_width.tex:13–14·88·148` 일반화 Butler–Volmer 언급)·§8 lag·§9 tail·부록 E ratio/전달함수 | **재편 흡수(국소)** — 독립 "동역학 장" 없음 ; Marcus·Nernst–Planck·Warburg·Fokker–Planck 0건 | 재개방 — brief 3.1 동역학 축 전건 ; ROADMAP 제안 4(B-3) |
| 통합 상태방정식 | **근거 미발견** — 대응 절 없음(대정준 전하 보존 `sec:sm-mc` 가 평형 상태식 역할은 하나 "통합"(평형+동역학+열) 상태식은 없음) | **미착수** | 재개방(핵심) — brief 3.2 "일반 비평형 열역학 상태식(affinity·flux-force)→준평형→평형" 사다리가 곧 이 계층 ; Onsager·Prigogine 0건 |
| 히스테리시스 | §4(`ch1_sec04_hys.tex`, Dreyer·CNT), Ch2 `ch1_sec13_lcohys`(정규용액 gap `:186–197`), Ch3 `ch3v22_sec04_mech`(Larché–Cahn 시도·GS-1 공백), 부록 `appendix_phase_separation.tex`(Cahn–Hilliard `:439·485–494`) | **재편 흡수(평형 gap 중심)** — Preisach·Jarzynski/Crooks 0건 ; γ_j 현상학(ROADMAP 제안 3) 미유도 | 재개방 — brief 3.1 히스 축(spinodal·CNT·Preisach) ; 4.5 |

### B-3. ROADMAP 제안 2~5 (v1.0.18.2 외부 위임 과제)

`docs/v1.0.18.2/ROADMAP_future_physics.md` 는 제안 1(vib Einstein)만 구현·검증 완료(line 3·10)이고 2~5 는 "외부 위임 과제로 문서화"했다. 현행 상태:

| 제안 | 내용 | 원 출처 | 현행 처리 상태(grep) | 재개방 후보 | 근거 |
|---|---|---|---|---|---|
| 2 Ω(ξ) 조성 의존(차기 후보 1순위) | Ω→Ω₀+Ω₁(2ξ−1), sublattice(Bragg–Williams) 확장, 침습도 높음 | ROADMAP:18–23 | **미착수** — `Redlich`·`\Omega(\xi)`·`Omega_1`(조성 계수 의미) 0건(LCO `Ω_1^cat` 매치는 전이 1 의 Ω 이지 조성 계수가 아님) ; Bragg–Williams 평균장은 존재(`ch2_sec01_partition.tex:108–110`, `ch1_sec02b_part0.tex:9`) | **재개방(열역학 축 핵심)** — LIT_ADVANCE §1 Redlich–Kister 초과 자유에너지·IMPROVEMENT #4 와 같은 갈래 | ROADMAP:11 |
| 3 Cahn–Hilliard → γ_j 유도 | 부록 CH 를 본문 N3–N7 로 승격, 핵생성 장벽에서 γ_j | ROADMAP:25–29 | **미착수** — CH 는 부록에만(`appendix_phase_separation.tex:439`), `_sections` 본문 0건 | 재개방 — brief 3.1 히스 축·열역학 축(phase-field) ; 단 LIT_ADVANCE M6 가 "Bazant/Dreyer PDE 를 생성기로" 는 ✗ 로 기각했으므로 "유도·정당화용 승격"과 "커널 생성기"를 분리해 다뤄야 함 | ROADMAP:12 ; LIT_ADVANCE:97 |
| 4 Butler–Volmer + Nernst–Planck 농도 분극 | R_n → R_ct + Warburg, Nernst shift | ROADMAP:31–35 | **미착수** — `Nernst.Planck`·`Warburg` 0건 ; BV 는 TST 절 언급만(`ch1_sec05_width.tex:148`) | 재개방 — brief 3.1 동역학 축(BV·Nernst–Planck) ; 데이터 의존(EIS·율속)은 warnbox | ROADMAP:13 |
| 5 PSD 컨볼루션 나노 | Gibbs–Thomson 을 PSD 위 적분, Dreyer 유한 N | ROADMAP:37–41 | **의도적 scope-out 유지** — 일반형 `eq:psdconv` 와 Gibbs–Thomson 수치 배제는 본문에 있고(`ch1_sec07_broadening.tex:254–295`), "PSD 다입자 처리는 모델에 넣지 않는다" 명시(`:313`) ; v1.0.25 Non-goal(`v1025 plan:91`) | 승계 기각(마이크론 흑연 범위) — 나노 Si 확장 시에만 재개방 ; brief §6 도 상시 파이프라인 X | ROADMAP:14 |
| v1.0.16 물리-데이터 이월(다온도 per-T n·LCO 실값) | 실측 대기 | ROADMAP:45–49 | park(Task #38) | Non-goal 유지 | HANDOVER_v25:122 |

### B-4. IMPROVEMENT_DIRECTIONS #1~#4 와 부수 후보 (v1.0.24)

| 항목 | 내용 | 출처 | 현행 처리 상태 | 재개방 후보 | 근거 |
|---|---|---|---|---|---|
| §0 "각짐" = 그림 격자 아티팩트 | 물리 결함 아님, 전 그림 고해상 재생성 | IMPROVEMENT:8–12 | 해소 | — | |
| §1 모델 = MSMR 동형 | Q_j↔X_j, U_j↔U0_j, w_j↔ω_j·RT/F | IMPROVEMENT:14–21 | 존속(현행 `ch1_sec17_msmr` 절 존재 — brief §4.2) | 승계(일반 이론의 특수 극한으로 위치 재정의) | |
| §2 전이 간 coupling 가설 | 물리는 맞으나 1-D 곡선에서 식별 불가 | IMPROVEMENT:23–35 | 판정 존속 | 재개방(조건부) — T/율속/히스처럼 외부변수 이동이 있을 때만(#3 행) | |
| #1 전이 4→5/6 canonical 고정 | ✅ 반영(opt-in, `GRAPHITE_STAGING_MSMR6_LIT`) | IMPROVEMENT:39–44 | 집행(D-B gallery opt-in) | — | v1025 plan:13 |
| #2 두 저전위 피크 비대칭 폭 | 일반화 로지스틱 | IMPROVEMENT:46–49 | 집행 — v1.0.25 @2 skew opt-in(D-A) | — ; 단 α 의 이론적 회수(정칙용액 비대칭 극한) 는 신규 설계 과제 | HANDOVER_v25:73–77 |
| #3 최근접 stage 결합 λ_{j,j+1} | 고위험, T/율속/히스 전용 | IMPROVEMENT:51–53 | **미착수** | 재개방(조건부) — brief 3.1 열역학 축 "sublattice/staging·transfer matrix" 와 동일 물리(Safran 층간 결합) ; 정적 곡선 피팅 목적으로는 승계 기각 | |
| #4 정칙용액(다층) 자유에너지 → common-tangent OCV | 최물리, "Chapter 2–3 열역학 타깃" | IMPROVEMENT:55–57·65–68 | **미채택** — v1.0.24 regsol 프로토(R²=0.79 단일상) → LIT_ADVANCE §6 Ω>2RT+Maxwell 정정판(R² 0.943) → v1.0.25 실측 역전(−0.53%p)으로 코드 삭제(DG-1) ; 문건 `eq:sifr-kernel`·`eq:sifr-blend` 는 "미채택·코드 미구현" 지위로 보존 | **재개방(열역학 축 핵심·brief 2.6 의 판정 대상)** — 삭제 근거는 "물리 오류가 아니라 실측 역전"(v1025 plan:202)이고 "파라미터 물리성·일관성" 가치는 LIT_ADVANCE §6 이 인정 ; v1.0.26 A/B 조사(실행 차단·미완)가 이 판정을 다시 열어 둠 | LIT_ADVANCE:108–113 ; HANDOVER_v25:85–89 ; brief §4.4 |
| §4 정직 한계 문단(MSMR 은 진짜 delta 재현 불가) | §7 에 1문단 명시 후보 | IMPROVEMENT:70–71 | 집행 여부 **미검증** | 작업 챕터 2.2 에서 확인 | |
| §5 저Si f_Si 과대·율속 washout 정량(V3) | Si U 약구속·C_bg(V) 분리·출하 `dqdv()` 전체 피팅 | IMPROVEMENT:73–75 | C_bg 는 "창-국소 상수" 로 정직화(C8) ; 나머지 미착수 | 코드·데이터 의존 → Non-goal ; 문건에는 tier 로 표기 | |

### B-5. LIT_ADVANCE_SYNTHESIS 4-tier 군 (v1.0.24 B트랙)

`results/comp_v24/LIT_ADVANCE_SYNTHESIS.md` 의 판정(★반영준비·◐선검증·○인용만·✗미반영)이 v1.0.24.1/v1.0.25 에 실제 반영됐는지는 본 에이전트 원천(HANDOVER_v25·v1025 plan)에 기록이 없다. v1.0.25 는 "국소 수정판"이라 ★군 대부분이 미반영일 것으로 **추정**하며, 확정은 작업 챕터 1.2(v1.0.24.1 행)·2.x 에서 한다(DQ-8).

| 군 | 항목 | 출처 | 현행 처리 상태 | 재개방 후보 |
|---|---|---|---|---|
| 헤드라인(4창 수렴) | 로지스틱 → 정칙용액(Frumkin) 최소일반화 + Ω>2RT Maxwell = near-delta, 평형 sharp ⊗ kinetic broadening 2단 구조 | LIT_ADVANCE:15–23 | 실검증(§6, R² 0.943 vs 0.938) 후 v1.0.25 에서 코드 삭제(B-4 #4) | **재개방** — brief 2.6·3.1 ; "율의존 폭을 열역학 w_j 로 우겨넣으면 오fit"(`:28`) 경계는 승계 |
| 두 번째 수렴 | 두-상 vs 고용체는 율의존 — Ω>2RT 기준 = 저율 envelope 만, 유한율 폭은 kinetic 층 | LIT_ADVANCE:25–29 | 아키텍처 원칙으로 존속(폭 이중지위와 정합) | 승계 |
| ★군 흑연 G1·G2 | Ω>2RT 폭 시드·Paul 2024 U_j·ΔS_j 실측 시드 | LIT_ADVANCE:59–60 | 반영 여부 미검증 | 시드값은 코드 소관(Non-goal) ; 서지(Paul 2024·Cordoba 2024)는 2.4 원장 후보 |
| ◐군 G3·G5 | G3 near-delta 정칙용액(§5 검증) ; G5 dilute 1′↔4 농도의존(Mercer 2019 vs Azizi 2025 상충) | LIT_ADVANCE:61·63 | G3 = B-4 #4 ; G5 미착수 | G3 재개방 ; G5 는 상충 해소 전 하드코딩 X 승계 |
| ✗군 G6·G7 | 전이 6+ 증설 ; DFT 결합E 를 Ω 로 대입 | LIT_ADVANCE:64–65 | 기각 존속 | 승계 기각 |
| ★군 LCO L1·L2·L3 | 3 feature 3 물리 골격 ; x=0.5 doublet ; ΔS_rxn 실측 시드 | LIT_ADVANCE:70–72 | 반영 여부 미검증(현행 Ch2 sec11~17 구조가 T1/T2/T3 를 갖는 것은 확인 — `ch1_sec13_lcohys.tex:186–197`) | 2.x 확인 후 승계 |
| ◐군 L4·L5·L6 | ΔS_e 작게 fit ; 3.94 V 두-상 near-delta ; R_n(x) SOC 의존 | LIT_ADVANCE:73–75 | L4 = 현행 토글 기본 off(`ch1_sec16b_lcoomega.tex:100–111`)로 부분 반영 ; L5·L6 미착수 | L5 는 G3 와 함께 재개방 ; L6 은 >4.4 V 전용 → 조건부 |
| ✗군 L7·L8 | diffthermo LCO 파라미터(O2 폴리타입) ; double-Gaussian | LIT_ADVANCE:76–77 | 기각 존속 | 승계 기각 |
| ★군 Si S1·S2·S3 | 가산 중첩 유지 ; 유효경계 명기 ; Si=연속 고용체 | LIT_ADVANCE:82–84 | S1 은 현행 `sec:si-blend` 골격 ; S2·S3 미검증 | 승계 |
| ◐군 S4·S5 | Si 히스 = 분리 U_j branch ; c-Li₁₅Si₄ 1차 plateau 별도항 | LIT_ADVANCE:85–86 | 미착수(Li₁₅Si₄ 는 서술로만 존재 `ch3v22_sec02_cases.tex:42`) | 재개방 검토(4.8 Si·블렌드) |
| ✗군 S6 | 블렌드 역학결합 | LIT_ADVANCE:87 | 기각 존속(Ch3 §3.4 GS-1 공백 선언과 정합) | 승계 기각(스코프) |
| 교차 방법론 M1~M7 | M1 정칙용액⊗kinetic(◐) ; M2 열역학 제약+베이지안 공유셋(★방법론) ; M3 stoich 정렬(★) ; M4 U_j(T)·ω_j 단일셋(◐) ; M5 dV/dQ 강건성(○) ; M6 PDE 생성기(✗) ; M7 비대칭 커널 "문헌 근거" 주장(✗) | LIT_ADVANCE:92–98 | M1 = B-4 #4 ; M2~M5 는 코드·피팅 방법론(Non-goal) ; M7 은 v1.0.25 @2 서술 규범("창시 = 우리 몫")으로 존속 | M1 재개방 ; M6·M7 승계 기각 ; M4 의 "폭이 ω·RT/F(고정 ω) vs ω(T)" 결정은 CLOSING Part 4 (3) 사다리와 동일 물음 → 3.2 에서 이론으로 다룸 |
| §7 정직 갭 | Ω_Si fitted 값 없음 ; Si gallery ΔS_j 없음 ; clean O3-LCO 오픈 셋 없음 ; 흑연 비대칭 폐형 커널 미발표 ; 다셀 공유 전역 fit turnkey 없음 | LIT_ADVANCE:115–120 | 존속 | 승계 — 2.4 "1차 문헌 공백" 표에 그대로 |
| §8 데이터 타깃 | Reynier 2004·Hudak 2014·Reimers–Dahn 1992 디지타이즈 ; diffthermo·PyBOP·Hu-Schwartz | LIT_ADVANCE:122–125 | 미착수 | brief §6(신규 다운로드 DQ)·DR-6 소관 |

### B-6. SURV_SYNTHESIS Tier 1~3·기각군 (v1.0.23 고등수학 서베이)

| 항목 | 내용 | 출처 | 현행 처리 상태(grep) | 재개방 후보 |
|---|---|---|---|---|
| Tier 1 #0 Fredholm 2종 ratio(사용자 논문) | lag 자기일관의 1차 ratio 닫힘 | SURV:14 | **집행(v1.0.23)** — `ch1_appE_selfconsistent.tex:75` `sec:sc-ratio` | 승계 — 4.3 동역학 |
| Tier 1 Laplace 전달함수 | H=1/(1+iωL_V) 저역통과 | SURV:15–17 | **집행** — `ch1_appE_selfconsistent.tex:180` `sec:sc-transfer` | 승계 |
| Tier 2 Fisher/정보기하 | 3온도점+공선형+과식별을 sloppy-model 식별성으로 | SURV:22 | **미집행** — `Fisher` 0건 | 재개방 검토 — 방법론층(4.9 부록 또는 별도) ; 기준 3)·5) 와의 관련은 낮음 |
| Tier 2 정합점근/Watson 꼬리 | L_V² 분산항·왜도 제1원리 확증(휴면) | SURV:23 | 미검증(`eq:widthbudget` 주변 미정독) | 조건부 |
| Tier 3 Legendre–Fenchel 볼록쌍대 | 반전 유일성 = 볼록성 | SURV:26 | **부분** — "Legendre-켤레 반전" 명명은 존재(`ch1_sec02b_part0.tex:357·390`, `ch3v22_sec03_blend.tex:86`) ; `Fenchel` 0건 | 승계(명명 노트 수준) |
| Tier 3 Preisach 명명 노트 | 전이 = 단일 릴레이 히스테론 embed ; **연산자 채택은 D(기각)** | SURV:27·34 | 미집행 — `Preisach` 0건 | brief 3.1 히스 축이 Preisach 를 후보로 올렸으므로 **기각 승계와 충돌** — 명명 노트만 허용·연산자 채택 금지를 설계서에 명기(DQ-15) |
| Tier 3 cusp 지수 3/2·FPT/Kramers·베이즈·안장점·RG caveat | 각주·부록 노트 | SURV:28–31 | cusp/Kramers 는 CNT 연결(`ch1_sec04_hys.tex:255`)로 부분 ; 베이즈·MCMC 0건 | 4.9 "수학 방법 노트" 부록 후보로 승계 |
| 기각군(D) | Wiener–Hopf·WKB·다중척도·중심다양체·Langevin·Preisach 연산자 | SURV:34 | 승계 기각 | 승계 기각 — 3.1 후보 카탈로그에 "기각 승계" 열로 명시(재조사 0) |
| 가정 충돌 경고 | Kubo 동적 χ(ω) — 구동 lag ≠ 평형 상관시간 | SURV:35 | 존속 | 승계 — 3.1 통계역학 축 "요동-응답" 설계 시 경고 필수 |
| 별도 역문제 버전 | Tikhonov·MaxEnt·볼록최적화 | SURV:36·44 | 미착수 | Non-goal(anodefit E 와 동일) |

### B-7. SM2_SURVEY 후보 (v1.0.22 통계역학 심화) — 집행 여부 확정

brief §4.5 는 SM2-A/B/C 집행 여부를 "미확정"으로 두었다. 본 정독·grep 으로 **세 건 모두 v1.0.25.1 에 집행돼 있음을 확정**한다(DQ-10).

| 항목 | 내용 | 출처 | 현행 처리 상태 | 재개방 후보 |
|---|---|---|---|---|
| SM2-A 평형 peak = 등온 입자수 감수율 | (dQ/dV)^eq = (F²/N_A RT)var(N) = e²∂⟨N⟩/∂μ | SM2:62–78 | **집행 확정** — `ch1_sec06_eqpeak.tex:75–112` 본문 + `:119` `% 자산(v1.0.22 SM2): [V22-SM2-A …]` | 승계 — v2.0.0 통계역학 파트의 캡스톤 항등식 |
| SM2-B 앙상블 동등성 = 1/√M 소멸 | | SM2:80–88 | **집행 확정** — `ch1_sec02b_part0.tex:388–400` + `:409` `[V22-SM2-B …]` | 승계 |
| SM2-C 한 자유에너지의 두 응답(∂_V↔∂_T 켤레 쌍) | | SM2:90–98 | **집행 확정** — `ch2_sec07_revheat.tex:78–92` + `:95` `[V22-SM2-C …]` | 승계 — Part 0↔Part T 다리 |
| (v) 단상 w_eff(Ω) 각주 | 보류(C-2/C-87 재도입 오독 리스크 최상) | SM2:32–35 | 보류 존속 ; v1.0.25 C5 가 금지 범위를 "두-상 한정"으로 좁힘(`v1025 plan:142`) | 승계 — 단상 유도식은 3.2 사다리에서 정칙용액 극한으로 자연 등장하므로 "두-상 폭 읽기 금지" 가드와 함께 다룸 |
| 축 B staging 상관함수·구조 인자 | 미시 상도표 이론으로 팽창 = 스코프 위반 | SM2:41–42 | 범위 밖 존속 | **재개방 검토** — 2026-09-02 지시("전혀 다른 새로운 이론을 끌고와서 엮든")와 기준 5)가 스코프를 넓혔으므로 v1.0.22 판정을 그대로 잇지 않고 3.1 열역학 축(sublattice/staging·transfer matrix)에서 재판정 |
| 축 C Jarzynski/Crooks | Part T 파생 D warnbox 가 소산 정량을 범위 밖 선언 | SM2:44–45 | 범위 밖 존속(`Jarzynski`·`Crooks` 0건) | 재개방 검토(조건부) — 열 축 entropy production 을 넣으면 [C-92] warnbox 와의 정합 결정 필요 |
| SM2-D Lindeberg 실측 대응 ; SM2-E 겹침 가중 = 감수율 가중 | 미초안 / SM2-A 흡수 | SM2:100–107 | SM2-E 흡수 여부 미검증 | 2.2 확인 |
| flow-1 사다리 1:1 대조표 · flow-3 기호 충돌 통합표 | flow성(심화 아님) | SM2:50–54 | **미집행** | 승계 — 4.0 기호표·3.4 derivation skeleton 이 정확히 이 표들 |

### B-8. anodefit MASTER 캠페인 A~G

| 캠페인 | 목표 | 출처 | 현행 처리 상태 | 재개방 후보 |
|---|---|---|---|---|
| A 브로드닝 실측 정합·M 제거 증명 | 문건 브로드닝이 실측 피크 높이·폭 재현 → M→1 | MASTER:48–52 | v1.0.24 착수(brief §4.3 "공개데이터 검증 캠페인") ; **성패 판정 기록은 본 원천에 없음(미검증)** — HANDOVER_v24 정독 필요(DQ-9) | 문건 측 A-1(dQ/dV↔dV/dQ 높이 관계 정식화)은 승계 후보 ; 실측 재현은 Non-goal |
| B 전셀 합성(LLI carrier) | | MASTER:54–58 | **미착수** | Non-goal(brief §6) |
| C T/I/V 스케일 완성 | C-1 rate·C-2 온도·C-3 전위창 | MASTER:60–63 | 부분 — 온도는 Part T·Einstein ; rate 는 pad·ratio ; 정량은 Task #38 | 이론 층(T·I 의존의 일반식)은 4.3·4.4 에 승계 ; 정량은 Non-goal |
| D 외부 검증(공개 데이터) | | MASTER:65–68 | 집행(SINTEF Zenodo 20086298, HANDOVER_v25:42) | brief §6 — 기존 확보 데이터 재사용만 |
| E 상태추론(역문제) | LAM·LLI·RI | MASTER:70–73 | **미착수** | Non-goal(brief §6) |
| G 문서/온보딩 | 클래스 가이드·온보딩 | MASTER:75–76 | 부분(`CODE_GUIDE_v23.md` 존재, MASTER:29) | Non-goal(코드) |
| D1~D7 결정 | 북극성 범위·즉시 착수·실측 rate·화학 우선순위·전셀 타이밍·공개데이터 선호·가이드 타이밍 | MASTER:109–126 | 응답 기록 **근거 미발견** ; D2 기본값 채택 추정(B-8 A 행) | 작업 챕터 1.2 에서 확정 |
| 운용(하이쿠/소넷 조사·Opus 마스터·적대 4~5창) | | MASTER:100 | 폐기(2026-09-02 전원 Fable 5.1) | 미승계 |

### B-9. refs 6·7 원문과 P3 #5

| 항목 | 상태 | 근거 |
|---|---|---|
| 서지 | **확정** — Ref. 6 = `lee2011jcp` S. Lee et al., *J. Chem. Phys.* **134**, 121102 (2011), DOI 10.1063/1.3565476 ; Ref. 7 = `son2013jcp` C. Y. Son et al., *J. Chem. Phys.* **138**(16), 164123 (2013), DOI 10.1063/1.4802584 ; 적용 논문 `lee2017jcp` **147**(14), 144111, DOI 10.1063/1.5000882 — 셋 다 "제목·DOI Crossref 확정" 주석 | `_sections/ch1v22_bib.tex:45–47` |
| 원문 소장 | **미소장**(brief §4.1) ; 방법론 추출본 = `old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md`(glob 존재 확인, 미정독) | brief:102 |
| P3 #5 5항 sub-section | **존재** — `sec:sc-p35` "ref. 방법론 도입 기록 — 서지·위치·구조·매핑·가정차" | `ch1_appE_selfconsistent.tex:113` |
| CLAUDE.md P1 "실제 확인한 뒤" | 서지 확정 + dossier 로 **부분 충족** ; 원문 정독은 미수행 → DR-8 사용자 결정 | CLAUDE.md:16 |

### B-10. v1.0.25 미완 N1~N13 과 v1.0.26 미결

| # | 항목 | 출처 | 현행 상태 | v2.0.0 처리 |
|---|---|---|---|---|
| N1 실제 LaTeX 빌드 | HANDOVER_v25:110 | **해소** — v1.0.25.1 빌드 102/30/22p(brief §4.2·A4) | — |
| N2 GitHub 업로드 | :111 | 해소(commit `bada485`·`27062ee`, git log) | — |
| N3 정적 검사 재실행 | :112 | v1.0.25.1 빌드로 사실상 해소(추정) | 2.1 자산 지도에서 재실행 |
| N4 흑연 두-상 4 vs 2 표기 불일치 | :113 | **미해소** — Dahn 1991 본문 확인 필요(사용자 확인 → master) | 2.3 가정 사다리·2.4 서지에 등재 ; DR 후보 |
| N5 ARCHIVE_NOTE 표제 | :114 | 미검증 | 경량 |
| N6 신규 CSV 8종 리포 보존 | :115 | 미결정 | DR-6 와 연동 |
| N7 재현 스크립트 등재 | :116 | 미등재 | 2.6 판정 시 필요하면 등재 |
| N8 sigr.csv 프로토콜 | :117 | 미측정 | 2.6 |
| N9 @3 철회 다중 셀 통계 | :118 | 미측정 ; 문건이 "미확정"으로 정직 표기(`ch3v22_sec02b_sifr.tex:43`) | 2.6 판정 기준에 포함 |
| N10 게이트 독립 재확인 | :119 | 미재실행 | 코드 Non-goal |
| N11 G-금지 게이트 미구현 | :120 | 미구현 | 6.2 grep 게이트로 문건 측 기계화 |
| N12 CRLF/LF 이원화 | :121 | 미결정 | 4.0 baseline 에서 규약 확정 |
| N13 회사 데이터 위임분 | :122 | park | Non-goal |
| v1.0.26 A/B regsol 재검증(물리 4전이 vs gallery 7전이) | brief §4.3·A7 (본 에이전트 미정독) | 실행 차단·미완 | 2.6 의 설계 입력 ; DR-1 대안 해석 |

### B-11. CLOSING Part 4 w/T 사다리의 미집행 단계

(i) 상수 n 은 집행됐고 n(T) 도입은 v1.0.16 에서 이뤄졌다(brief §4.3 "v1.0.16(n(T))" — 본 에이전트 미정독, brief 인용). (ii) 다온도 per-T n 상수성 진단·(iii) 상수 w 전환·(iv) 최소 n(T) 는 다온도 실측이 있어야 판정되므로 Task #38 에 park 돼 있다(ROADMAP:46·HANDOVER_v25:122). v2.0.0 은 이를 데이터로 닫지 않되, (4) "n(T) 채택 시 config 항 동반 변경" 규칙(CLOSING:92)을 열특성 사다리의 **이론 규칙**으로 명문화해야 한다(DQ-12).

### B-12. 정독 중 발견분 (brief §4.5 시드에 없던 항목)

| 항목 | 발견 내용 | 근거 | 처리 제안 |
|---|---|---|---|
| P3 #8 본문 코드 토큰 3건 | `ch1_sec10_sum.tex:145`·`ch2_sec08_synthesis.tex:56`(`\code{use\_si\_constants()}`), `ch3v22_sec02b_sifr.tex:43`(`\texttt{V1025\_DATA\_ADDENDUM.md}`) — 모두 ch1/ch3 마스터의 `\appendix` 앞 `\input`(`ch1_graphite_v1.0.24.tex:37·48`, `ch3_si_v1.0.24.tex:27`) | grep | DQ-1 |
| P3 #1 기호 체계 불일치 | `V_{n,app}`·`V_{n,drive}`·`V_{n,OCV}` 0건 ; 현행 = `V_app`·`V_n` | grep | DQ-2 |
| P3 #6·P5 `ver.N` 절 부재 | `ver.1~5`·`ver.N` 0건 | grep | DQ-4 |
| `ch1_appD_si.tex` 빌드 미포함 | ch1·ch3 마스터 어느 쪽 `\input` 에도 없음 ; 파일은 `_sections` 에 존재(코드 토큰 grep 에도 잡힘) | `ch1_graphite_v1.0.24.tex:54–58`, `ch3_si_v1.0.24.tex:23–32` | DQ-6 — 자산 지도에서 "빌드 미포함 파일" 열 ; brief §4.2 "_sections 56" 카운트에 포함돼 있을 가능성 |
| 서지 원장 체인 종료점 | 원장 파일 = V1020·V1021·V1022·V1023 뿐(glob) ; v1.0.24/25 신규 bibitem(lee2011jcp·son2013jcp 는 v1.0.23 등재 추정, Paul 2024 등 v1.0.24 문헌은 미확인)의 원장 등재 상태 미검증 | glob | DQ-5 |
| SM2-A/B/C 집행 확정 | B-7 | grep | DQ-10(brief 갱신) |
| 자산 태그 계열 다양 | A-7 | grep | DQ-11(brief 표기 정정) |
| F-11 ③ 구조 항목 해소 | §3.5 코드절 부록 이동·서지 내 코드 인용 제거 | `ch3_si_v1.0.24.tex:30–31`, `ch1v22_bib.tex` grep 0 | 등록부 A-4 반영 완료 |
| 모델 배분 이력의 다층성 | v1.0.25 는 Opus 5.0 master 직접 편집(HANDOVER_v25:65) — 헌법 "Opus 5.0 은 master 로 쓰지 않는다"와 어긋나는 선례 ; 2026-09-02 전원 Fable 5.1 로 대체 | HANDOVER_v25:48·65 | 초안 Assumptions 에 "v1.0.25 저작 주체 = Opus 5.0 master 직접" 사실만 기록(판단 X) |

---

## Decision Queue (골격 이견·brief 오류·추가 후보 — 근거 첨부, 결정은 master·사용자)

- **DQ-1 [brief 보강] P3 #8 게이트의 base 위반 3건.** 브리프 작업 챕터 4 는 "본문 코드 토큰 0" 을 저작 게이트로 두는데, 동결 base v1.0.25.1 이 이미 3건(`ch1_sec10_sum.tex:145`·`ch2_sec08_synthesis.tex:56`·`ch3v22_sec02b_sifr.tex:43`)을 갖고 있다. v1.0.25.1 은 무수정 동결이므로 고치지 않고, 작업 챕터 2.5 GAP REGISTER 에 "base 위반 3건 — v2.0.0 저작 시 물리 개념 서술로 대체(상수 opt-in 은 부록 코드맵으로)"로 등재할 것을 제안한다. 근거 = CLAUDE.md:46, ch1 마스터 `\input` 순서(:37·48 < 부록 :54).
- **DQ-2 [brief 보강] P3 #1 의 기호 체계가 현행 문건과 불일치.** CLAUDE.md:34 의 네 기호(`V_{n,app}` 등)는 현행 문건에 0건이고, 현행은 두 전위 `V_app`·`V_n`(F-01 keybox)이다. 초안 Test Plan 의 P3 #1 게이트는 "현행 기호로 재해석(V_app·V_n·U_j·U_oc 의 구분 일관)"으로 쓰고, CLAUDE.md 자체 개정은 사용자 소관임을 명기할 것을 제안한다.
- **DQ-3 [골격 이견 아님·결정 선행 조건] DG-A 와 D22 의 관계.** brief 3.3 (b) Part I 일반 이론 + Part II 재료 적용은 v1.0.22 사용자 확정 D22 "활물질별 재편"(`docs/v1.0.21/HANDOVER_v1.0.21.md:18`)을 되돌리는 구조다. 3.7 정지 시 DG-A 는 "D22 를 supersede 한다"는 문구를 사용자 결정 항목에 포함해야 하고, D22-8 "병합 빌드 금지·3장 분리+xr" 도 v2.0.0 에 적용할지(단일 문서 vs 분리 빌드) 같은 자리에서 결정해야 한다. 근거 = A-6.
- **DQ-4 [brief 보강] CLAUDE.md P1·P3 #6·P5 의 `ver.N`/`Chapter 1~5` 조항이 스테일.** 현행 문건에 `ver.N` 0건. 초안 Current Ground Truth 에 "P1 원구상 4계층 → 현행 대응(B-2 표)"을 넣고, v2.0.0 이 원구상(발열·반응속도론·통합 상태방정식·히스테리시스)을 Part I 일반 이론의 장 구성으로 **회복**하는 안이 (b) 구조와 자연스럽게 겹친다는 점을 DG-A 근거에 추가할 것을 제안한다.
- **DQ-5 [추가 게이트] 서지 원장 체인.** 원장 파일은 V1023 까지만 존재(glob)하고 현행 bibitem 은 95 다. 작업 챕터 2.4 게이트에 "V1023 원장 키 ↔ 현행 95 bibitem 전건 대조 · 원장 밖 키 목록화 · DOI 재검증" 을 명시할 것을 제안한다. 근거 = A-7 서지 원장 행.
- **DQ-6 [추가 게이트] 빌드 미포함 잔존 파일.** `_sections/ch1_appD_si.tex` 는 어느 마스터에도 `\input` 되지 않는다. 자산 지도(2.1)에 "빌드 포함/미포함" 열을 두고, 미포함 파일의 자산(라벨·식)을 무유실 원칙 적용 대상에서 어떻게 다룰지(회수 or 아카이브) 3.4 에서 판정하도록 제안한다.
- **DQ-7 [결정 선행 조건] 정칙용액+Maxwell 재개방 시 DG-1·D-C 와의 정합.** 사용자 verbatim "regsol 삭제"(코드)와 D-C "미채택·코드 미구현" 지위 warnbox(문건)가 살아 있다. v2.0.0 이 브리프 2.6·3.1 에서 정칙용액 커널을 이론으로 재개방하면 "코드 삭제된 것을 문건 일반 이론으로 복원"하는 셈이 되므로, 3.7 의 DG-B(채택 이론 목록)에 "DG-1 은 코드 결정이고 문건 이론 채택은 별개"임을 명시하고 사용자 재확인을 받을 것을 제안한다. 근거 = v1025 plan:14·202, LIT_ADVANCE:108–113.
- **DQ-8 [미검증 표시] LIT_ADVANCE ★군의 반영 여부.** 본 에이전트 원천에는 기록이 없다. 초안에서 B-5 의 ★군을 "반영 여부 미검증 — 작업 챕터 1.2(v1.0.24.1 행)에서 확정"으로 표기할 것.
- **DQ-9 [미검증 표시] Campaign A(M 제거 증명) 성패.** anodefit MASTER D1~D7 응답과 Campaign A 결과는 `HANDOVER_v24.md`(brief A6) 소관이며 본 에이전트 미정독. 초안 Current Ground Truth 에 "미검독"으로 표시하고 1.2 에서 확정.
- **DQ-10 [brief 정정] SM2-A/B/C 집행 확정.** brief §4.5 "집행 여부 미확정" → 확정(`ch1_sec06_eqpeak.tex:119`·`ch1_sec02b_part0.tex:409`·`ch2_sec07_revheat.tex:95` 자산 태그). 초안 §4.5 상당 절에서 갱신.
- **DQ-11 [brief 정정] 자산 태그 표기.** brief §4.4 의 `[A-xxx]`·`[E-xxx]` 는 grep 에서 직접 확인되지 않았고, 실제 계열은 `[C-nn]`·`[V21-Qn-nn]`·`[V22-SM2-X]`·`[V22-R5-nn]`·`[LCOΩ-n]`·`A-0nn`(138건·34파일)이다. 초안에서는 "절 말미 `% 자산` 주석 태그 체계(다계열)"로 쓰고 2.1 에서 계열 목록을 기계 추출하도록 제안한다.
- **DQ-12 [추가 후보] CLOSING Part 4 (4) n(T)↔config 동반 규칙의 이론 승계.** 데이터 의존 단계 (ii)~(iv) 는 Non-goal 이지만, "폭 n(T) 를 열면 가역열 config 항이 함께 바뀐다"는 규칙은 4.4 열특성 사다리의 정합 조건으로 명문화해야 한다. 근거 = CLOSING:92.
- **DQ-13 [사용자 확인 권고] "필요한 식만"(v7) vs "자기완결 교과서" 긴장의 해소 선언.** 2026-09-02 기준 1)·2) 가 자기완결 쪽을 택한 것으로 읽히나, FABLE_AUDIT:54·64 가 "v12서 명시 조율 필요"로 남긴 항목이므로 초안 Assumptions 에 "이 긴장은 2026-09-02 지시로 해소된 것으로 본다(사용자 확인 대상)"로 적을 것을 제안한다.
- **DQ-14 [추가 후보] Eyring 척추 회복 여부의 정식 결정.** FABLE_AUDIT:47·64 의 "Phase 4.1 명시 결정 항목"이 결정된 기록을 본 에이전트 원천에서 찾지 못했다(근거 미발견). 작업 챕터 3.1 동역학 축의 첫 후보로 올리고 DG-B 에서 명시 결정하도록 제안한다.
- **DQ-15 [골격 보강] Preisach 는 명명 노트만·연산자 채택 금지.** brief 3.1 히스 축이 Preisach 를 후보로 열거하나 SURV:27·34 는 "연산자 채택은 D(차원폭발·경로의존 스코프 위반)"로 기각했다. 3.1 후보 카탈로그에 "Preisach = 명명·embed 노트 한정, 연산자 채택 = 기각 승계"로 적을 것을 제안한다.
- **DQ-16 [골격 보강] SM2 축 B(staging 미시화)의 재판정.** v1.0.22 판정은 "스코프 위반"이었으나 2026-09-02 지시가 스코프를 넓혔다. brief 3.1 열역학 축(sublattice/staging·transfer matrix)에서 "v1.0.22 기각 승계"가 아니라 "재판정"으로 다루도록 제안한다. 근거 = SM2:41–42, brief:33·40.

---

## Read Coverage (파일·행 범위 전건)

전문 정독(head→tail, 생략 없음):

| # | 파일(`D:\Projects\Project_Anode_Fit\` 기준) | 행 범위 | 비고 |
|---|---|---|---|
| 0 | `Claude\results\handoffs\2026-09-02-v2-master-plan\brief.md` | 1–219(전건) | 과제·골격 |
| 1 | `CLAUDE.md` | 1–89(전건) | brief 표기 90줄, 실측 89행 |
| 2 | `Claude\docs\v1.0.15\CLOSING_v1.0.15.md` | 1–106(전건) | |
| 3 | `Claude\results\comp_v24\USER_FEEDBACK_v1024_READING.md` | 1–207(전건) | |
| 4 | `Claude\docs\Fable_점검\FABLE_AUDIT_01_history_v3-v1011.md` | 1–73(전건) | |
| 5 | `Claude\docs\v1.0.18.2\ROADMAP_future_physics.md` | 1–50(전건) | |
| 6 | `Claude\results\comp_v24\IMPROVEMENT_DIRECTIONS.md` | 1–87(전건) | |
| 7 | `Claude\results\comp_v24\LIT_ADVANCE_SYNTHESIS.md` | 1–130(전건) | |
| 8 | `Claude\docs\v1.0.22\results\comp_v23\SURV_SYNTHESIS.md` | 1–45(전건) | |
| 9 | `Claude\docs\v1.0.22\results\comp_SM2\SM2_SURVEY.md` | 1–136(전건) | |
| 10 | `Claude\plans\2026-07-18-anodefit-MASTER-plan.md` | 1–129(전건) | |
| 11 | `Claude\plans\2026-07-26-v1025-surgical-skew-consistency-plan.md` | 1–241(전건) | |
| 12 | `Claude\docs\v1.0.25.1\results\HANDOVER_v25.md` | 1–171(전건) | |

확인용 grep(전문 정독 아님 — 매치 행만 열람):

| 대상 | 패턴(요지) | 목적 |
|---|---|---|
| `Claude\docs\v1.0.25.1\_sections\*.tex` | 감수율·var(N)·앙상블 동등성·켤레 쌍 / `\code{`·`\texttt{` / Eyring / KWW·stretched·장벽분포 / 준안정·athermal·역방향 식별·S0·16-울타리 / Cahn·Fisher·Preisach·Legendre·Butler·Nernst-Planck·Warburg·PSD·Gibbs-Thomson·Redlich·Ω(ξ)·Omega_1 / Fenchel·Onsager·Bernardi·Marcus·Fokker·Prigogine·entropy production·transfer matrix·sublattice·Bragg·Jarzynski·Crooks / `% 자산` 태그 / 제목 내 `(N#)` / F-04 문제 제목 11종 / `sec:pointwise` / 요동·음함수·섭동·양성 유일근(비주석 행) / `V_{n,` / `ver.N` / `\bibitem` 수 | SM2 집행 확인 · P3 #8·#1·#6·#7 · F-04/05/10 집행 확인 · B-1~B-7 현행 상태 |
| `_sections\ch1_sec02a_part0.tex` | `p_i`·`f_int`·`s_int` | F-02·F-03 |
| `_sections\common_preamble_v1024.tex` | margin·setstretch·parskip·microtype | F-06 |
| `_sections\ch1_appE_selfconsistent.tex` | `\item[`·`\section`·`\subsection`·`sec:sc-p35`·refs 6/7 서지 문자열 | F-07·P3 #5 |
| `_sections\ch1_sec16b_lcoomega.tex` | `eq:lcoomega-toggle`·`\begin{cases}` 전후 | F-09·L4 |
| `_sections\ch1v22_bib.tex` | `J. Chem. Phys`·144111·121102·164123·`\code{` | refs 6/7 서지·F-11 ③ |
| `ch1_graphite_v1.0.24.tex`·`ch3_si_v1.0.24.tex` | `\appendix`·`\input{` | 본문/부록 경계·빌드 포함 파일 |
| `Claude\**\*.md` | `D21`·`D22` | A-6 위치 확인(전문 정독 아님: `docs/INDEX.md`, `docs/v1.0.21/HANDOVER_v1.0.21.md`, `docs/v1.0.21/results/V1021_EXECUTION_LEDGER.md`·`V1021_CHANGE_LOG.md`·`V1021_REFERENCE_LEDGER.md`, `plans/2026-07-17-v1022-master-plan.md`, `plans/2026-07-18-v1023-ratio-and-advanced-methods-plan.md`, `docs/v1.0.25.1/results/PHASE_R1_RESULT.md`) |
| glob | `Claude/**/V10*_REFERENCE_LEDGER*.md`·`Claude/old/Archive_oldtrack/PHASE_DIAG_REFS67_DOSSIER.md` | 존재 확인만 |

미정독(본 에이전트 배정 밖 — 초안·후속 Phase 에서 확정 필요): `HANDOVER_v24.md`(FB0~FB9·Campaign A 결과), `HANDOVER_regsol_investigation.md`(v1.0.26), `docs/INDEX.md`·`plans/INDEX.md` 본문, v1.0.20~v1.0.23 결정 이력 본문, `PHASE_DIAG_REFS67_DOSSIER.md`, `appendix_phase_separation.tex` 본문, `_sections/*.tex` 본문(grep 매치 행 외), `Codex/`(접근 금지).

미접근·미수정: `Codex/` 무접근. 기존 파일 생성·수정·삭제 0(본 파일 신규 1건만). git 명령 미실행.
