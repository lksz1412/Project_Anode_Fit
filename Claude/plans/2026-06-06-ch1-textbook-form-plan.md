# Ch1 교과서 형식화 — 메타 제거 + 표제·박스 정리 + 절 구조 통일 Plan

**Date**: 2026-06-06 · **Author**: Claude · **챕터**: F(Form/구조) · **Phase**: F.0~F.6 · **Step**: 1~?
**대상**: `Claude/docs/graphite_ica_ch1.tex` (958줄·20p·GREEN; R/A/W 라운드로 논리·격식 완료본)
**트리거**: 사용자 5+1 피드백 — (1) 서의 작성용 메타(전개 뼈대·읽기 규약)는 문건에 불요 (2) 제목을 교과서식 "Chapter 1"로, verbose 부제 제거 (3) author/date 제거 (4) "미확정(FLAGGED)"·"(Chapter 1만으로 사용 가능)"·"줄기 밖" 같은 \emph{교과서도 논문도 아닌 메타 문구} 제거 (5) 절·하위토픽 전개 방식이 제각각 — 교과서처럼 \emph{일관된 고정 양식} 필요.

---

## Summary
완료본 Ch1 을 \emph{준-리뷰 논문 / 교과서} 형식으로 마감한다. (A) 작성용 메타·자기참조 문구 전수 제거(서 스캐폴딩·미확정/FLAGGED·(Chapter 1만으로)·줄기 밖·정직 표기 등). (B) 제목 교과서식 "Chapter 1" + verbose 부제 제거 + author/date 제거. (C) 박스 분류(5종) 격식 통일(미확정→비고, 줄기 밖→심화). (D) \emph{절·하위토픽 전개 양식을 하나의 고정 템플릿}으로 통일 적용. \emph{이번 라운드도 문구·구조 중점}; 논리·수식은 부수 검증(오류만).
**방법**: 기존 확립 워크플로 — 앞에서부터 절 하나씩, Codex+Claude 적대로 문제 안 나올 때까지 반복, 이전 절 연계 검토, 컴팩션·재개 시 §X 재정독, 분량 회귀 감시.

## Current Ground Truth
- 대상 958줄·20p·GREEN. R(논리)·A(eq·§6)·W(격식) 완료, Codex REGISTER CLEAN.
- **제거 대상 메타·자기참조(grep 확정)**:
  - 서 스캐폴딩: "전개의 뼈대"(L97 enumerate 로드맵)·"읽기 규약" keybox(L114~120, "박스 건너뛰고 본문만 읽어도" 등).
  - 박스 메타 레이블: flagbox "미확정(FLAGGED)"(L39)·rigorbox "심화(형식적 엄밀화 — 줄기 밖)"(L40).
  - 자기참조: "(Chapter 1 만으로 사용 가능)"(L802)·"줄기"(L316/681/747)·"검산 박스에서"(L368)·"정직 표기"(L861).
  - 제목/메타: verbose 3행 제목(L55~58)·\author(L59)·\date(L60).
- **절 구조 불일치(grep 확정)**: 절 도입 "질문."(9회 일관)이나, 하위 \textbf 소제목이 명사구("전하 보존식.")·문장형("정상점이 평형값과 같다")·의문형("왜 1차 완화인가")·해석형("의미." 3회) 혼재. 절 마감(keybox/의미./무 closer)도 제각각. 박스 5종 ad hoc.

## Phase Range
| Phase | 범위 | Steps | 핵심 |
|---|---|---:|---|
| **F.0** | 전체 인벤토리·설계 | 1–4 | 전문 재정독 + 메타 전수 목록 + \emph{고정 절 템플릿·박스 분류·제목·서 trim 확정}(Decision) |
| **F.1** | front matter | 5–8 | 제목 교과서식·author/date 제거·서 스캐폴딩(전개뼈대·읽기규약) 제거(동기·stagebox 유지) |
| **F.2** | 박스·메타 전수 | 9–12 | 박스 5종 격식 리네임(미확정→비고·줄기밖→심화) + 자기참조 문구((Chapter 1만으로)·줄기·정직표기) 제거 |
| **F.3** | §2~§5 구조 통일 | 13–19 | 고정 절 템플릿 적용(소제목 명사구·일관 마감·박스 분류). 절별 + 이전 절 연계 |
| **F.4** | §6~§7 구조 통일 | 20–25 | 〃 |
| **F.5** | §8~§10 구조 통일 | 26–30 | 〃 |
| **F.6** | 횡단·교차모델·빌드 | 31–34 | 전 문서 양식 일관 횡단 + Codex 전영역 → 판정 → 반복 + 빌드 |

**절별 게이트**: G-form(고정 템플릿 준수·소제목/마감/박스 일관) · G-meta(메타·자기참조 0) · G-flow(이전 절 연계·비약 0) · G-local(부수: 수식·논리 무손상) · G-build · G-review(Codex 적대→판정→반복) · **G-recovery(§X 컴팩션 재정독)**.
**정지 5조건**: Decision Gate/새 의존성/FAIL/사용자 stop/통제문서 모순.

## Non-goals
- 수식 \emph{값}·물리 결론·논리 변경(부수 검증은 오류 적발만). 식·라벨 번호. §1~5 \emph{내용}(구조·문구만). 충전 branch·Ch2~5·피팅 부록. Workflow 도구.

## Implementation Changes
`graphite_ica_ch1.tex`(제목·박스·서·절 구조) / `PHASE_F*_RESULT.md` + `PHASE_F_EXECUTION_LEDGER.md` / 본 계획. 문건 보호(R/A/W result 덮어쓰기 금지).

## Phase F.0 — 인벤토리·설계
- **S1** 전문(L1~958) 재정독 — 메타·자기참조·절 구조 불일치 전수 목록(절별).
- **S2** \emph{고정 절 템플릿} 확정(§FT). **S3** 박스 5종 분류·리네임 확정(§BX) + 제목·서 trim 안 확정. **S4** result+ledger. **gate**: 목록·템플릿·Decision 확정.

## Phase F.1 — front matter
- 제목 교과서식(§TT) · `\author{}`·`\date{}` 비움 · 서에서 "전개의 뼈대" 로드맵·"읽기 규약" keybox 제거(관측·동기 문단 + stagebox 유지, 격식 도입으로). 빌드.

## Phase F.2 — 박스·메타 전수
- 박스 `\newtheorem` 리네임(§BX) · 본문 "(Chapter 1 만으로 사용 가능)"·"줄기"(3곳)·"검산 박스에서"·"정직 표기" 등 자기참조 제거·격식화. 빌드.

## Phase F.3~F.5 — 절 구조 통일(앞에서부터)
각 절: ① 재정독 → ② 고정 템플릿(§FT)으로 소제목 명사구화·마감 일관·박스 분류 적용 + 부수 수식·논리 점검 → ③ Codex 적대+판정→문제 0까지 반복 → ④ 이전 절 연계(양식·흐름) 확인 → ⑤ 빌드 → result.

## Phase F.6 — 횡단·교차모델·빌드
전 문서 템플릿·박스·메타 일관 횡단 + Codex 전영역(구조·격식·논리)→판정→반복 + 최종 빌드 GREEN + 분량 회귀 감시.

## Implementation Interfaces
**§FT 고정 절 템플릿(제안)**: 각 \section =
1. \textbf{도입}(1문단): 이 절의 물음·목표. [절 도입 라벨 = Decision D-도입]
2. \textbf{전개}(\subsection/문단): 정의 → 유도(중간 단계 명시) → \boxed 결과. 소제목·소표제 = \emph{descriptive 명사구 통일}(문장형·의문형 제거).
3. \textbf{결과·해석}: \boxed + 1~2문장.
4. \textbf{단서(박스)}: §BX 5종만.
5. \textbf{연결}(1문장): 다음 절로(일관 위치·톤).
**§BX 박스 5종(격식 통일)**: 핵심(keybox) · 유효 범위(boundbox; "Validity bound" 괄호 제거) · \emph{비고}(flagbox, 미확정/FLAGGED→) · \emph{심화}(rigorbox, "형식적 엄밀화 — 줄기 밖"→) · 검산(verifybox; "차원·극한·부호" 괄호 간결화).
**§TT 제목(안)**: verbose 3행 → 교과서식. 예: `\textbf{\Large Chapter 1}\\[0.3em] 흑연 음극 dQ/dV 피크의 물리` (부제·로드맵 행 제거). [정확 문구 = Decision D-제목]
**§X Anti-compaction**: 컴팩션·재개 직후 5단계 재정독 의무(직전 result·ledger·작업 절 tex 전문·계획 대조·분량 대조) — 기존 그대로.
**§R Result 11항목·Ledger 12-col**.

## Test Plan
- **메타 grep 감사**: "만으로 사용/줄기/FLAGGED/미확정/정직 표기/읽기 규약/전개의 뼈대/박스 건너" → 잔존 0. \author/\date 비움 확인.
- **양식 일관**: 절 도입·소제목·마감·박스가 §FT/§BX 따르는지 횡단 점검.
- **빌드 GREEN**: `!`0·undefined 0·식 overflow 0. \emph{분량 회귀 감시}(서·메타 제거로 감소 정상, 내용 누락 0).
- **부수 논리**: 절별 G-local. **Codex 교차모델**: F.6 STRUCTURE CLEAN. **연계**: 절별 G-flow.

## Assumptions
- A1: 수식 값·논리 불변(오류 발견 시만 별도). A2: §FT/§BX/§TT/서trim 은 Decision 승인 후 확정. A3: 서 동기·stagebox 는 reader 콘텐츠라 유지(스캐폴딩만 제거).

## Decisions Required (무응답 시 권고값)
- **D-제목**: "Chapter 1" 교과서식 + 짧은 주제(흑연 음극 dQ/dV 피크의 물리), verbose 부제·로드맵 행 제거. **권고: 그대로**(주제 문구는 조정 가능). 
- **D-서trim**: "전개의 뼈대" 로드맵 + "읽기 규약" keybox 제거. 관측·동기 문단 + stagebox 는 \emph{유지}(reader 도입). **권고: 그대로**(로드맵은 교과서면 목차로 대체, 읽기규약은 작성용 메타라 제거).
- **D-박스**: 미확정(FLAGGED)→비고 · 줄기밖→심화 · 나머지 괄호 간결화. **권고: 그대로.**
- **D-도입라벨**: 절 도입 `\textbf{질문.}`(9회 일관·만족 스타일) 유지 vs 라벨 없는 격식 도입문. **권고: 유지**(일관 anchor; 원하면 제거).
- **D-템플릿**: §FT 고정 양식. **권고: 그대로**(절별 적용).

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-06-06 (F v1) | 교과서 형식화 계획 신설 — 메타·자기참조(서 스캐폴딩·미확정/FLAGGED·(Chapter 1만으로)·줄기 밖·정직표기·verbose 제목·author/date) 제거 + 박스 5종 격식 통일 + 고정 절 템플릿(§FT) 일관 적용. 워크플로 = 절별 Codex+Claude 적대 iterate-until-clean + 이전 절 연계 + 부수 논리검증 + §X anti-compaction. |
