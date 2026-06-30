# v5 수식-구동 변환 — 설계 스펙 (master 확정, Phase 1.0)

> 본 파일 = 5 초안 서브 + 검수 서브의 공통 사양. 원천 = `Claude/docs/graphite_ica_ch1_Opus_v4.tex`. 산출 = `graphite_ica_ch1_Opus_v5.tex`(§1.1~§1.17, §1.18 배제).

## 0. 변환 철학 (★ 가장 중요)

v4 는 **이미 equation chain** 이다 — boxed 결과식이 다음 절의 입력이 되도록 배열돼 있다. 따라서 v5 = "다시 쓰기"가 **아니라** **산문 벗기기(prose-stripping)** 다:

1. **모든 식 블록(`equation`/`align`/`equation*`/`align*`) 과 figure(TikZ) 블록은 v4 에서 verbatim 복사** — LaTeX 한 글자, `\label{}` 한 개도 바꾸지 않는다. (식 충실성 = 최우선. 새 오류 유입 0.)
2. 식 사이의 **산문 문단을 제거**하고, 논리 연결은 **§3 커넥터 화이트리스트**의 한 줄로 대체한다.
3. v4 가 **산문으로만** 설명한 유도 단계(식으로 안 적힌 것)는 **명시적 중간 식으로 승격**한다 — 이 경우에만 새 식이 생기며, label 은 `eq:v5-<seckey>-<n>`.
4. 결과: "수식만 따라가도 이해" — 독자가 식과 한 줄 커넥터만 따라가도 전 유도가 닫힌다.

**금지:** 식 변형·재유도·기호 변경·label 변경·식 삭제·논리 단계 누락. v4 에 있는 식은 v5 에 전부 있어야 한다(보존 감사 R7 이 1:1 대조).

## 1. KEEP / DROP / COMPRESS / PROMOTE

| 요소 | 처리 |
|---|---|
| 식 블록(equation/align ±*) | **KEEP verbatim** (label 포함) |
| figure(TikZ) 블록 | **KEEP verbatim** (D3) — 캡션만 식-참조 위주로 축약(물리 서술 문장 제거, 식 번호·축 의미만) |
| 절 제목 `\section{}`/`\subsection{}` | **KEEP** (번호 체계 `1.N` 유지). label `\label{sec:...}` 보존 |
| `verifybox`(검산) | **KEEP, COMPRESS** — 차원·극한·수치 검산은 식 콘텐츠. 산문 군더더기만 제거, 식·극한·수치는 보존 |
| `boundbox`(유효 범위) | **KEEP, COMPRESS** — 유효창 부등식(예 $3RT\lesssim\mathcal A\ll\lambda$)은 "수식으로 표현된 가정"이라 유지 |
| `keybox`(절 요지) | **DROP** — 순수 산문 recap. orphan. 전부 삭제 |
| `stagebox`(staging 배경, 서론) | **COMPRESS to 1-line** — 물리 배경 산문. staging 순서식 + figure 참조만 남김 |
| 동기 부여·직관·서술 문단 | **DROP** |
| 절간 다리 산문("다음 절은…") | **DROP** |
| 가정에 대한 *산문 설명* | **DROP** (가정 자체는 식 조건/부등식 한 줄로) |
| worked example 서술 | **COMPRESS** — 수치 계산식만 남기고 서술 제거 |
| §1.15 알고리즘 (1)–(8) | 아래 §4 특별 규칙 |
| §1.17 코드(verbatim) | **KEEP** (D2) — 코드 블록 그대로, 주변 해설 산문만 축약 |

## 2. 커넥터 화이트리스트 (식 사이 허용되는 유일한 한글 — 한 줄, 마침표로 끝)

식을 잇는 연산을 명시하는 한 줄만 허용. 서술 문단 금지.

- `식~\eqref{LBL} 에 식~\eqref{LBL2} 를 대입하면`
- `양변을 ...로 미분하면` / `양변에 ...를 곱하면` / `양변을 ...로 나누면`
- `정지점 조건 ...=0 에서` / `평형 조건 ...에서`
- `극한 ...→... 에서` / `... 이면`(조건부)
- `... 에 대해 풀면` / `정리하면` / `로그를 취하면` / `Taylor 전개 ...를 넣으면`
- `두 식의 비를 취하면(...약분)` / `... 끼리 묶으면`
- `여기서 ...는 식~\eqref{LBL} 로 정의된다` / `... 는 \S\ref{sec:...} 의 결과다`
- 결과 선언 한 구: `→ 평형 등온선이 닫힌다`, `→ 닫힌 일반해` 류(식 앞 한 구절, 절 도입에 1회 허용)

각 절 도입은 **최대 1문장**(앞 절에서 받은 결과식 번호 명시): 예 `\S\ref{sec:rate} 의 식~\eqref{eq:eyring} 과 \S\ref{sec:thermo} 의 식~\eqref{eq:eqcond} 에서 출발한다.` (D4 기본값.)

## 3. 절 → 서브 그룹 배정 (5 병렬 초안)

| 그룹 | 서브 | 절 | v4 줄범위 |
|---|---|---|---|
| A | sub1 | §1.1 기호와 규약 · §1.2 rate · §1.3 thermo | 261–664 |
| B | sub2 | §1.4 fwdrev · §1.5 regsol | 665–1048 |
| C | sub3 | §1.6 charge · §1.7 eqpeak · §1.8 lag | 1049–1442 |
| D | sub4 | §1.9 potbranch · §1.10 tempbranch · §1.11 synth · §1.12 overlap | 1443–1915 |
| E | sub5 | §1.13 hys · §1.14 hyspol · §1.15 master · §1.16 falsify · §1.17 code | 1916–2743 |

서론(83–129) + staging figure(131–255) + 프리앰블(1–80)은 **master 가 직접** 통합 단계에서 처리(공유 골격).

## 4. §1.15(master) 특별 규칙 — G-usable 보존

§1.15 는 피팅 알고리즘(실행력)이라 단순 산문 삭제로 망가지면 안 된다.

- boxed 식 `eq:master`, `eq:hysmaster`, `eq:dHeff` : KEEP verbatim.
- 알고리즘 (1)–(8): **구조 보존, 산문 축약**. (1)입력·(2)전처리·(3)검출·(3')컷·(4)M1–M6 의사코드·(5)목적함수·(6)단계회귀표·(7)진단표·(8)참조표 — **표·의사코드·식은 KEEP**, 설명 산문은 절차 명령문(전보 아님, 짧은 완결 동사구)으로 축약. M1–M6 의사코드 enumerate, S0–S5 표, 진단표, 참조표(8)은 구조 그대로 유지(G-usable 핵심).
- `가정의 울타리` keybox(16항목 ①–⑯): 사용자 명시 "가정에 대한 설명 배제" → **terse 조건 목록으로 COMPRESS**(각 항목을 산문 설명 없이 조건/부등식·플래그 한 구로). 완전 삭제는 X(가정 자체는 유효범위라 식 조건으로 남김).

## 5. 라벨·번호 규약

- v4 식 → v4 의 `\label{eq:...}` 이름 **그대로 보존**. `\eqref`/`\ref` cross-ref 도 그대로(자동 해소).
- 신규 승격 식 → `\label{eq:v5-<seckey>-<n>}` (예 `eq:v5-thermo-1`). seckey = 절 label 접미(notation/rate/thermo/fwdrev/regsol/charge/eqpeak/lag/potbranch/tempbranch/synth/overlap/hys/hyspol/master/falsify/code).
- §1.18 전용 label(eq:gcoupled/xistack/dvstack/gapsplit/psieq, sec:stacking)·심볼(ψ,B,κ,ξ_c,ξ_open,ξ_close,ΔV_stack) **미사용**.
- `\thesection`/`\theequation` = `1.\arabic{...}` 유지(v5 도 Chapter 1).

## 6. §1.1 심볼표 처리

- 심볼표(longtable) KEEP — equation-following 의 사전(필수). 단:
  - **[확장] 적층 준안정(§1.18) 행 삭제**: `$\psi$`, `$B_j,\kappa_j$`, `$\xi_{c,j}$`, `$\xi_{open},\xi_{close}$`, `$\Delta V_{stack}$` 5행 + 그 multicolumn 헤더 1행 제거.
  - "충방전 확장" 행은 §1.13–§1.14 가 v5 범위 내라 KEEP.
  - 의미 칸의 긴 산문 동격 설명은 식·기호 위주로 축약(단위·정의식은 보존).
- 부호 규약 문단(273–282): 부호 정의는 식($V_\app=V_n+s_I|I|R_n$, $s,s_I,\sigma_d$ 정의)으로 KEEP, 산문 설명 축약.

## 7.5 특별 보존·처리 항목 (설계 검수 R0 반영 — ★ 서브 의무)

설계 검수가 잡은 prose-only load-bearing 단계. 해당 서브는 **DROP 금지, 아래대로 처리**:

- **[sub5 / §1.16] dangling 참조 삭제 (CRITICAL).** v4 줄 2576–2579 의 마지막 종속절 `— 다만 적층 기원의 athermal 절편 바닥은 $T_{c,j}$ 위에서도 남으므로, 소멸하는 몫과 남는 바닥의 구별은 \S\ref{sec:stacking} 가 한 단계 더 가른다.` 는 §1.18(배제) 을 가리킨다. **이 종속절을 삭제**하고 `절편이 온도에 아예 무관하면 정규용액 그림이 틀렸다는 신호다(표면 재구성·기계적 응력 기원 히스 등).` 에서 문장 종료. ("식·label verbatim 보존" 규칙의 유일 예외 — sec:stacking 참조는 v5 에서 미해소.)
- **[sub2 / §1.4 eq:affinity] 이중 계상 논거 승격 (HIGH).** v4 줄 681–685 "로그 항을 구동력에 넣지 않는 까닭 = 점유 인자가 자리 통계 담당, 또 넣으면 이중 계상 → 정지점 logit 두 번 → 폭이 $2RT/F$ 로 두 배" 는 eq:affinity 의 형태 정당성을 정하는 load-bearing 논거다. **DROP 금지** — 한 줄 식/조건으로 승격: eq:affinity 옆 또는 직후에 `로그 항 제외(점유 인자가 담당 — 중복 시 폭 $RT/F\to2RT/F$)` 정도의 조건 주석, 또는 `eq:v5-fwdrev-?` 승격식. (verifybox 가 인접하면 거기 극한 검산 항으로 흡수 가능.)
- **[sub2 / §1.4 eq:chisum] ∀𝒜 양화 보존 (HIGH).** χ+χ′=1 강제는 "모든 구동력 𝒜 에서 성립"이라는 양화가 핵심이나 산문에만 있다. eq:chisum 의 요구 등호 옆에 조건 `(∀\mathcal A_j)` 을 식으로 명시하거나 커넥터로 `모든 구동력에서 성립해야 하므로` 한 구 보존.
- **[sub2 / §1.4] 두 경로 일치(self-consistency)는 verifybox 로.** eq:logistic 직후 "detailed balance 정지점 = 열역학 평형, eq:eqcond 를 Ω=0 으로 풀어도 같은 식" 논거는 인접 verifybox(KEEP, 줄 809–815)에 이미 식으로 있다. 본문은 커넥터 `(두 경로 일치 — 아래 검산)` 한 구로 내리고 verifybox 의 식을 보존.
- **[sub5 / §1.15 (3')·M4] 수치 보존 의무 (MED).** (3')컷·M4 는 boxed 식이 없는 산문 절차지만 **G-usable 핵심**이다. 산문→절차 명령문 축약은 허용하되 다음 수치·조건은 **보존 의무**: 컷 분율 $5\%$, 창 시작 $\mathcal A\gtrsim3RT$, 꼬리-우세 전제 $L_V\gtrsim w$, regime 분기 $L_V<w/3$ / $w/3\lesssim L_V\lesssim w$, 자유분기 범위 $(0,\xi_{\eq}(q_a)]$, $\chi$ 편향 정량 $+0.07\to+0.03$.
- **[sub5 / §1.15 keybox 울타리 ①–⑯] 분류 처리.** 조건 보존(식/수치 직접 전제): ①④⑤⑦⑧⑪⑫⑬⑮⑯ — terse 조건 한 구. 조건 축약(처방 식 참조 1줄): ②⑥⑭. 삭제 가능(타 절차·진단표가 중복 수용): ③⑨⑩. → 16항목 keybox 를 "유효범위 조건" terse 목록으로 재구성(산문 설명 제거).

## 7. 서브 산출물 형식

각 서브는 담당 절의 **v5 LaTeX 텍스트만** return(파일 쓰기 X). 형식:
- 절별로 `\section{...}\label{...}` 부터 마지막 식/figure 까지 완결.
- 식·figure verbatim, 커넥터 한 줄, 승격 식 명시.
- 말미에 **변환 보고**: (a) 담당 절 Read 줄범위 (b) 보존한 식 label 목록 (c) 승격한 식 목록(eq:v5-...) (d) DROP 한 keybox/문단 수 (e) orphan 자가점검(승격 식이 앞 도입·뒤 사용 있는지).
