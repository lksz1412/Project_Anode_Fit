# HIST — 조판·그림 결정 + 버전 계보 + Standing Non-goals + Handover Chain (검토 sub 산출)

> 작성 2026-07-22. 검토 sub(읽기·요약 전용, 수정·commit 금지). 4-tier: **[확정]**(원문 file:line 직접 확인)·**[근거 미발견]**·**[추정]**·**[미검증]**(2차 인덱스 요약 의존, 원문 미대조).
> 임무 = F-06(조판)·F-07/F-09(overflow)가 과거 조판 결정과 정합하는지 + 전체 버전 계보 + 반복 확정된 금지사항 승계.
> 원문 대량 인용 없음. 근거 경로는 절대경로 아닌 프로젝트 상대(`Claude/...`)로 표기.

---

## 1. 확정된 조판·레이아웃 결정 (폰트·여백·줄간격·그림 규약·인라인 vs 디스플레이)

### 1-A. 현행 조판 설정 — **[확정]** (`Claude/docs/v1.0.24/_sections/common_preamble_v1024.tex`, 동일값 `ch1_preamble.tex`·`ch2_preamble.tex`)

| 레버 | 현재 값 | preamble 위치 | 비고 |
|---|---|---|---|
| 문서클래스 | `\documentclass[11pt,a4paper]{article}` | common_preamble L14 | 11pt·A4 |
| 여백 | `\usepackage[margin=22mm]{geometry}` | L15 | 텍스트폭 ≈166mm(A4 210−2·22) = 긴 줄·밀도 상승 주원인(F-06) |
| 줄간격 | `\setstretch{1.12}` | L27 | 단일행보다 약간 넓음 |
| 문단간격 | `\setlength{\parskip}{0.45em}` · `\parindent 0pt` | L28 | 들여쓰기 없음 |
| 넘침 완충 | `\setlength{\emergencystretch}{2em}` | L29 | 우측 overfull 완화용 |
| microtype | **미로드(0건)** | — | protrusion/justification 미적용 |
| 한글 폰트 | `kotex` | L16 | 한글 조판 엔진(XeLaTeX 전제) |
| mono 폰트 | `\setmonofont{D2Coding}[Scale=MatchLowercase]` | L17 | `\code{}`=`\texttt{}`(L~) 렌더용 |
| 빌드 | `xelatex` 3-pass, **ch1 먼저**(xr 외부참조) | preamble 주석 | |

- **★핵심 [확정]**: 세 preamble 파일 주석에 **"렌더 목표 = v1.0.18.2 동등(문서클래스·패키지·박스 체계·매크로 계승)"** 명시(`ch1_preamble.tex`·`ch2_preamble.tex` 헤더). → 여백 22mm·`setstretch 1.12`·`parskip 0.45em` 등 조판 레버는 **최소 v1.0.18.2(2026-07-08) 이래 동결·계승**돼 왔고 이번 F-06 이 **밀도/간격/여백을 처음 튜닝**하는 시점. **[추정]** 그 이전(v1.0.13~)도 동일 계열값(당시 INDEX 가 "overfull 0" 만 gate).

### 1-B. 그림 규약 — **[확정]** (초기 그림 계획서 2건 + v1.0.14 계획서)

- **외부 이미지 금지 · 전 그림 TikZ 실계산 좌표 원칙** — `Claude/plans/2026-06-12-ch1-v2-friendly-math-figures-pass-plan.md:6,45`("외부 이미지 = 저작권 리스크 + 실계산 좌표 원칙 위배"·"TikZ 재설계로 달성") + `2026-06-13-ch1-v3-...:31,60`("전부 python 실계산 좌표"·"TikZ 실계산 생성 유지—저작권·정합"). 그림 개선=인터넷 이미지 대체가 아니라 **TikZ 신규 생성/재설계**.
- **그림 제작 워크플로**: 좌표 python 실계산 → TikZ 교체 → 렌더(pdftoppm) 시각 확인 → 커밋 (`2026-06-12-...:22`).
- **그림 품질 규격**: 축 눈금·수치 라벨 추가, 선 두께·폰트 크기 통일, 패널 (a)(b) 라벨 규격화, 캡션-본문 식번호 결속 전수(`2026-06-13-...:35-36`).
- **그림 경연(체리픽)** 체제 — v1.0.14 서 "기존(v7-11 유래) 이미지 불만족 → 9안(Sonnet3+Opus3+Codex3) 경연 후 체리픽" 확립(`2026-07-04-v1014-...:22,100-105`). v1.0.20 그림 경쟁 6창 31본, v1.0.21 "A급 그림 5본" 편입(`Claude/docs/INDEX.md:22,43`) **[미검증-INDEX요약]**.

### 1-C. 인라인 vs 디스플레이 수식 방침 — **[근거 미발견]**(명문 규약)

- 과거 계획서에 **"복잡 인라인 수식→디스플레이 승격"의 성문 기준은 발견 못 함**. F-06(`USER_FEEDBACK_v1024_READING.md:105`)이 처음으로 복잡도 기준(분수 중첩·합/적분·다항·조건부→승격, 단항·짧은 관계식→인라인 유지)을 제안. **[추정]** 즉 이 방침은 이번 리비전에서 신설되는 규약.
- 다만 **"글로 말하던 논리를 식·정렬·case 표로 옮기고 prose 압축"**(수식-주도)은 v3(`2026-06-13-...:16-17`)·헌법③에서 반복된 상위 원칙 → F-06 인라인→디스플레이는 그 **연장선상 [추정]**.

---

## 2. 버전 계보 (version arc) 요약 — ch1 v2~v9 → v1.0.10 → … → v1.0.24

> 근거: `Claude/docs/INDEX.md`(전 버전 블록, **[확정]** 원문 인덱스)·`_FINAL_README.md`·`Fable_점검/FABLE_AUDIT_*`·각 HANDOVER. v1.0.16~v1.0.22 세부는 INDEX 요약 의존 **[미검증]** 표기.

### 2-A. 1.0.x 이전 개발 계보 (ch1 v2~v10) — **[확정 from INDEX/_FINAL/audits]**
| 버전 | 날짜(계획) | 확정한 것(1줄) | p |
|---|---|---|---|
| ch1 v2 | 06-10~12 | 백지 재작성 + 친절 수식 보강(§1.8/1.11–1.13) + 그림 개선 pass | 42 |
| ch1 v3 | 06-12~13 | `Fable_v3` equation-selfcontained·W4(수식 증량·물리 논리 정식 검증·글 압축) | 45(91식) |
| ch1 v4 | 06-13 | `Opus_v4` stacking 절 redo(§1.18 적층; σ충돌·산수오류→V4R redo) | — |
| ch1 v5 | 06-17~22 | `Opus_v5` equation-driven 장르전환(97식 verbatim·prose 32%↓·keybox 14→1) | — |
| ch1 v5RR/v6 | 06-22 | v5 재검수 R0~R3 + v6 flowchart 재조립(97식 보존 손실0) | — |
| ch1 v7 | 06-29 | codeflow 간결판(유도 압축·KWW 의도적 절삭→사후 불만) | 17 |
| ch1 v8 | 06-29 | 유도 확장판(v7 생략 유도 복원) | 21 |
| ch1 v9 | 06-30 | 흑연+LCO 통합(전자 엔트로피). ⚠broadening 누락 | 30 |
| ch1 v10 | 07-01 | broadening 복원·집합 통계역학·w_eff 제거 = **release 1.0.10 본체** | 34 |
| (Ch2 병렬) | 06-30~07-01 | Ch2 v3(가역발열 survey 5p)→v4(통계열역학 13p, ⚠w_eff 오류)→v5(w_eff 절 제거 13p) | |

### 2-B. 1.0.10 → 1.0.24 안정판 계보 — **[확정 from INDEX blocks]** (세부는 [미검증])
| 버전 | 확정한 것(1~2줄) | ch1 p |
|---|---|---|
| v1.0.10 | 코드 `Anode_Fit_v1.0.10.py`와 **matched**·dQ/dV 정상 종개형 실증 | 34 |
| v1.0.11 | **중단**(docs 폴더가 v1.0.10 과 byte-identical, Phase1.1 이후 미착수) | — |
| v1.0.12 | LCO 6절 줄글→(a)-(d) 수식사슬·방향규약 원자정정(f=+σ_d)·verify10 반영 | 41 |
| v1.0.13 | Part0 통계역학 기초 신설·LCO 전부 Part II 통합·산문 압축·**overfull 0**·용어 영어 원어 정책 | 50 |
| v1.0.14 | eq1.8 Hill 유도·PSD 유도-배제·부록 A(부호검산)/B(구현대응)·**본문 코드-언급 0**·어투 정련·그림 경연 72안 중 8승자 | 57 |
| v1.0.15 | 이산 전압 격자 **완전 퇴출**→점별 연속 아키텍처·§1.9 인과 기억 적분·Ch2 발열 상세화 | 58 |
| v1.0.16 | 폭 다중도 n(T) 온도함수 피팅 지원(`_dwdT` config 전파) | 58 |
| v1.0.17 | register 정련(제목/본문 "코드 진행→계산 진행"·**본문 코드 참조 제거**)·Ch2 서지 보강 | 58 |
| v1.0.18.1 | v1.0.17 register/정합 이월 완결(verifybox·longtable·endfirsthead)·물리 무변경 | 59 |
| v1.0.18.2 | 제안1 vib Einstein 양자보정(동결 ΔS_vib→S_vib(T;θ_E) additive)+연구 로드맵 | 59 |
| v1.0.19 | **Fable 전면 재작성**(페이블→10종→페이블)·Part II 7분할·broadening 독립절·doc-leads(코드가 문건에 정합) | 61 |
| v1.0.20 | 서지 전수 검증·중간다리·컨벤션 통일·통합 검수 H0 — **동결 릴리스** | 66 |
| v1.0.21 | 확장판 Q0~Q8(통계역학 2건·항법 이원판·top3·LCO 시연·Si 예비 부록·**A급 그림 5본**) | 76 |
| v1.0.22 | **활물질별 3챕터 재편**(Ch1 흑연+열/Ch2 LCO/Ch3 Si·혼합)·공통 preamble·xr 양방향·장별 bib | 77/23/5 |
| v1.0.23 | 사용자 JCP147 ratio(Fredholm-2종 닫힘) 기법을 lag 자기일관에 접목·**부록 E**·코드옵션(기본 off·bit-exact) | 83+/25/17 |
| v1.0.24 | 최근문헌+Codex 반영: @3 Si Frumkin(§3.2.5)·@5 stage-2L(§1.5.4)·LCO 전자항 토글(§2.6.1 기본 False)·SINTEF 실측 피팅·전수 doc↔code 감사 | 91/28/20 |

- v1.0.24 현재 = **F-01~F-11 1차 피드백 리비전 중**(계획 `Claude/plans/2026-07-22-v1024-feedback-revision-plan.md`, GO 대기). in-place·문건만·코드 bit-exact.

---

## 3. Standing Non-goals / 반복 확정 금지사항 — **[확정]** (복수 계획서 반복 등장)

> ★ = **최상위 헌법**(`Claude/docs/v1.0.15/CLOSING_v1.0.15.md` Part1·2, "다음 버전 착수 전 필독"). 사용자 verbatim 근거 보유.

| # | 금지/불변 규칙 | 근거(대표) | 재발 여부 |
|---|---|---|---|
| N1 | ★**코드(함수·플래그·`\code{}`·`\texttt{}`) 언급 = 부록(코드맵)에만** — 본문 산문·그림·**캡션·표·절 제목 절대 금지** | 헌법①(CLOSING L15) · v1.0.14 F-F · v1.0.17 P2 · v1.0.23 계획 P2(L68) · **F-11** | **재발**(v1.0.24 신규 절 gr2L·lcoomega·sifr·Ch3 Fig2 캡션서 위반 → F-11 최우선) |
| N2 | ★**자기 diff·버전-이력 서술 금지**(D1: "구판은/이전에는/폐지" 류 본문·각주·캡션 X) | 헌법① D1(CLOSING L13) · v1.0.17 D1 | — |
| N3 | ★**방어 어투 "X가 아니다" 금지**(D2) — 긍정 서술로 | 헌법① D2(CLOSING L14) | — |
| N4 | ★**"대입하면 [박스]" 점프 0**(D3) — 중간식 ≥1 반드시 노출(수식-주도) | 헌법③ D3(CLOSING L25) | — |
| N5 | ★**흐름 끊는 UI 금지**: 팝업·AskUserQuestion·자동 EnterPlanMode·**Workflow 전부 금지 → Agent만** | 헌법 2-4(CLOSING L51-54) · `2026-06-10-ch1-blank-rewrite-v2:50` · F-revision 계획 Non-goals | **재발**(CLOSING 에 "재위반" 자인) |
| N6 | ★**제안·플래그 전 과거 이력 먼저 확인**(새 이슈로 보이면 = 이력 미확인 신호) | 헌법 2-1(CLOSING L38-41) | **재발**(F-11 "이력 무시" 지적의 직접 근거) |
| N7 | ★**base 문건 전문 정독 후 착수**(head→tail 전 영역) | 헌법 2-3(CLOSING L47-49) · [[feedback_full_file_read_required]] | — |
| N8 | ★**명시 선택을 효율 판단으로 대체 금지**(A 선택 시 B가 나아도 A 실행) | 헌법 2-5(CLOSING L56) | — |
| N9 | ★**검증 없이 "완료/골든" 금지**(import·grep·샘플 통과 ≠ 완료) | 헌법 2-6(CLOSING L59) | — |
| N10 | **원본 불가침**: 이전 버전 폴더·golden·result/ledger/handover·원천 자료·Codex 산출물 수정 X(신 폴더 증판) | v8·v1010·v1013·v1017·v1023·v1024 계획 반복 | — |
| N11 | **코드 물리 로직 변경 금지·회귀 bit-exact 유지**(주석 eq 참조 보강만; 옵션은 동결 off=bit-exact) | v1014·v1017·v1023·F-revision Non-goals | — |
| N12 | **FWHM 류 불요 유도 부활 금지** | `2026-06-12-v2:39`·`2026-06-13-v3`·`2026-06-12-v3-equation-selfcontained:19` | — |
| N13 | **외부 이미지 금지**(전 그림 TikZ 실계산 좌표) | §1-B 근거 | — |
| N14 | **새 물리 주장 추가 금지**(형식 변환·검증·형식화만) | `2026-06-12-v3-equation-selfcontained:31`·v3 W4 Non-goals·F-revision | — |
| N15 | **챕터 통째 배치 작성 금지 → 절(파일) 단위 루프** | `2026-06-10-blank-rewrite-v2:50`·1챕터=1Phase 금지(F-revision GT) | — |
| N16 | **역문제(dQ/dV→ρ 역산)·PSD 크기 convolution·입자크기 효과 = forward-only 로 스코프 배제**(gap 아닌 의도된 경계) | v1024-completeness Non-goals(L72-73) | — |
| N17 | **BDD·풀셀 분해·매칭·상태추론 = 하류/타 프로젝트, 스코프 밖** | v1024-completeness Correction(L184, 사용자 3회 지적) | — |
| N18 | **v1.0.24 in-place 리비전(신 버전번호 X)·대상 문건만** | F-revision Non-goals(L50) | 현행 |

---

## 4. Handover Chain(최신→역방향) — **[확정]** (`Claude/docs/**/HANDOVER*.md` grep)

```
HANDOVER_v24 (v1.0.24 승계 선언 "v1.0.23 을 승계해", R0~R4; ★"④ Chain 헤더" 절 부재 — 서술형)
  ← HANDOVER_v23 (JCP147 ratio·부록E; "v1.0.22 를 승계해")
  ← HANDOVER_v1.0.22 (results/, 3챕터 재편·RA 계보감사 "미로그 축소/생략/왜곡=0")
  ← HANDOVER_v1.0.21 (근거=v1021-master-plan ← docs/v1.0.20/HANDOVER)
  ← HANDOVER_v1.0.20 (근거 chain ← v1.0.19/HANDOVER)
  ← HANDOVER_v1.0.19 (페이블→10종→페이블·doc-leads ← v1.0.18.2/HANDOVER)
  ← HANDOVER_v1.0.18.2 (vib Einstein ← v1.0.18.1/HANDOVER)
  ← HANDOVER_v1.0.18.1 (이월 완결 ← v1.0.17/HANDOVER)
  ← HANDOVER_v1.0.17 (근거 ← v1.0.16/HANDOVER ← v1.0.15/CLOSING[헌법3종·확정 w/T] ← v1.0.15/HANDOVER[격자 퇴출])
  ← HANDOVER_v1.0.16 (근거 ← v1.0.15/CLOSING Part4 ← v1.0.15/HANDOVER ← v1.0.14/KICKOFF)
  ← HANDOVER_v1.0.15 (← v1.0.14/HANDOVER ← v1.0.13/HANDOVER ← v1.0.10/HANDOVER_v1.0.11)
  ← HANDOVER_v1.0.14 (Chain: v1.0.10 대검수 → v1.0.11 → v1.0.12[ledger, 핸드오버 없음] → v1.0.13 → 본)
  ← HANDOVER_v1.0.13 (← v1.0.12 ledger ← v1.0.11 ← v1.0.10 문제점 대검수)
  ← HANDOVER_v1.0.11 (v1.0.10 동결·인계 무결성 대검수 9종+10차 — chain 기점)
```
- **[확정] 특이점**: (a) v1.0.11·v1.0.12 는 **독립 HANDOVER 없음**(v1.0.11=v1.0.10 byte-identical 중단; v1.0.12=ledger/result 로 갈음). (b) v1.0.24 HANDOVER 는 타 버전의 정형 "④ Chain 헤더" 절 없이 서술형("v1.0.23 을 승계해")로 chain 표시. (c) **v1.0.15/CLOSING** 이 chain 상 "HANDOVER·INDEX 보다 먼저 읽는" 상위 헌법 노드.

---

## 5. F-06 / F-07 / F-09 이 과거 조판 결정과 겹치는가 (핵심 판정)

| 축 | 과거 결정/상태 | F-06/07/09 와의 관계 | tier |
|---|---|---|---|
| 여백·줄간격·문단간격·글자간격(밀도) | **한 번도 튜닝된 적 없음.** v1.0.18.2 값(22mm·1.12·0.45em)을 preamble 이 "렌더 목표 v1.0.18.2 동등"으로 동결 계승. microtype 전무 | **F-06 = 조판 밀도의 첫 전역 튜닝.** 과거 결정과 충돌 없음(신규 영역). FB2 가 22→~26mm·1.12→~1.18·0.45→~0.6em·microtype 도입 | [확정]+[추정] |
| overflow 게이트 | 과거 gate = **"overfull \hbox >10pt = 0"**(v1.0.13 "overfull 0"·v1.0.14 "of 0"·v1.0.15 "of>10 0"·v1014 test plan L121/133) | **게이트에 사각(맹점) 있었음.** F-07(E.3 좌측 `\item[\textbf{}]` 라벨 넘침)은 **Overfull 경고를 안 냄**→"GREEN 빌드" 기준이 놓침. F-09(식2.39 `cases` 내부 텍스트 우측)도 표 스캔서 누락. → **렌더 기반 시각 점검을 게이트에 추가** 필요(F-07 원장 명시) | [확정] |
| 우측 overfull 잔존 | v1.0.24 빌드 로그 텍스트 overfull 13건(ch1_appE E.6 7-46pt·ch2 revheat 30pt·appA 24pt 등) + appB codemap longtable 568pt×3 | F-07 원장이 **F-06 넘침 스윕 대상으로 이미 목록화**(`USER_FEEDBACK...:120`). 과거엔 >10pt 만 gate → 잔존 다수 | [확정] |
| 인라인→디스플레이 승격 | 성문 기준 부재(§1-C). 상위 "수식-주도(글→식 이전)" 원칙만 존재 | F-06 이 복잡도 기준을 **신설**. 헌법③ 연장선 | [근거 미발견]+[추정] |
| 그림 규약 | 외부 이미지 금지·TikZ 실계산·경연 체리픽(§1-B) | F-06/07/09 **무충돌**(조판·overflow 만; 그림 내용 규약 불변). F-11(캡션 코드언급)만 그림 캡션에 접촉 | [확정] |

**종합 판정 [확정+추정]**: F-06 조판 밀도(여백·간격)는 **과거에 지적·해결된 적 없는 신규 축**이라 과거 결정과 정합 문제 없음 — 단 전역 리플로우로 **페이지수(91/28/20)·HANDOVER/INDEX/MERGE 페이지참조 갱신**이 수반된다(F-06 원장·FB2 게이트). F-07/F-09 overflow 는 과거 "overfull>10pt=0" gate 가 **좌측 라벨 넘침·cases 내부 넘침을 구조적으로 못 잡던** 맹점의 노출 → **렌더 시각 점검 게이트 신설**이 근본 교정(FB5·FB2 게이트에 반영됨).

---

## Read Coverage

**전문 정독 [확정 근거]**: `Claude/plans/INDEX.md` · `Claude/docs/INDEX.md`(39KB 전문) · `Claude/results/comp_v24/USER_FEEDBACK_v1024_READING.md`(F-01~11 전문) · `Claude/plans/2026-06-12-ch1-v2-friendly-math-figures-pass-plan.md` · `2026-06-13-ch1-v3-w4-math-physics-figures-plan.md` · `2026-07-04-v1014-tone-rigor-appendix-figures-plan.md` · `2026-07-18-v1024-completeness-validation-plan.md` · `2026-07-22-v1024-feedback-revision-plan.md` · `Claude/results/V1024_PROGRESS_SUMMARY.md` · `_FINAL_README.md` · `Claude/docs/v1.0.24/_sections/{common_preamble_v1024,ch1_preamble,ch2_preamble}.tex` · `Claude/docs/v1.0.24/results/HANDOVER_v24.md` · `Claude/docs/v1.0.15/CLOSING_v1.0.15.md`(헌법 3종).
**부분/head [확정]**: `Claude/docs/v1.0.23/results/HANDOVER_v23.md`(L1-45).
**grep [확정]**: 조판어(geometry/linespread/microtype/overfull/margin/여백/줄간격) across `plans/` · handover chain across `docs/**/HANDOVER*.md` · standing non-goals(FWHM/외부이미지/Workflow/코드=부록/원본 불가침) across `plans/` · figure/layout across `MASTER_ROADMAP_v3.md`(**결과 0건** → 로드맵엔 조판 규약 없음).
**미독(요약 의존) [미검증]**: v1.0.16~v1.0.22 개별 HANDOVER 원문(docs/INDEX 요약 채택) · MASTER_ROADMAP_v3/CH2 본문 · v1021/v1022/v1023/MASTER 개별 master-plan 본문 · INDEX_v24/MERGE_READINESS 원문.
