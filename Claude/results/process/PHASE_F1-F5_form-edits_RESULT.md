# Phase F.1–F.5 — 교과서 형식화 편집 Result

**Date**: 2026-06-06 · **Plan**: `2026-06-06-ch1-textbook-form-plan.md` · **Step Range**: 5–30 · **챕터**: F(Form)

## Summary
완료본 Ch1 을 교과서/준-리뷰 논문 형식으로 마감하는 편집 전부 적용. (F.1) 제목 교과서식·author/date 제거·서론 표제·작성용 스캐폴딩 제거. (F.2) 박스 5종 격식 리네임·메타 자기참조 9곳 제거. (F.3~F.5) 소제목 의문형·문장형 9곳 명사구 통일. \emph{물리 내용·수식 값 무변경}; 빌드 GREEN.

## Files Updated (`graphite_ica_ch1.tex`)
### F.1 front matter
- **제목**: verbose 3행(리튬이온전지…ICA 피크의 물리 + 부제 2행) → `\textbf{\LARGE Chapter 1}` + `\Large 흑연 음극 $dQ/dV$ 피크의 물리`.
- `\author{}`·`\date{}` 비움(Project_Anode_Fit (새 트랙)·2026-06-03 제거).
- 서 표제 「서 — 무엇을 관측했고, 무엇을 설명하려 하는가」 → **「서론」**(의문형 부제 제거).
- 작성용 스캐폴딩 제거: **「전개의 뼈대」 enumerate 로드맵**(목차 \tableofcontents 가 대체) + **「읽기 규약」 keybox**(작성 방법론 메타). \emph{관측·목표 문단 + stagebox(흑연 staging 배경) 보존}.
- 주석 헤더(L1~16) "백지/새 트랙/원칙(NT plan v3)/Author" 메타 정리(렌더 무영향).

### F.2 박스·메타
- 박스 리네임: boundbox 「유효범위(Validity bound)」→**「유효 범위」** · flagbox 「미확정(FLAGGED)」→**「비고」** · rigorbox 「심화(형식적 엄밀화 — 줄기 밖)」→**「심화」** · verifybox 「검산(차원·극한·부호)」→**「검산」**. (keybox 핵심·stagebox 유지)
- 메타 자기참조 제거·격식화(9곳): "본 장 줄기는"→"본 장 본문은" · "아래 flagbox 와"→"아래 비고와" · "검산 박스에서"→"아래 검산에서" · "— flagbox·"→"— 비고·" · "rigorbox 에서"→"심화에서" · "줄기에는 분율 보존"→"본문에는…" · "본문 줄기에는"→"본문에는" · **"실무 피팅 근사식 (Chapter 1 만으로 사용 가능)"→"실무 피팅 근사식"** · "(정직 표기)" 제거.

### F.3~F.5 소제목 명사구 통일(9곳)
- §eqpeak: `\subsection{… 가 왜 peak 인가}`→`{… 의 peak 발생}`; 「왜 이 양인가.」→「유도의 출발점.」
- §lag: 「왜 1차 완화인가.」→「1차 완화의 근거.」; 「정상점이 평형값과 같다」→「정상점과 평형값의 일치」; 「속도상수는 활성화 배리어가 정한다(Eyring).」→「속도상수와 활성화 배리어 (Eyring).」
- §barrier: 「전위가 forward 장벽을 낮춘다.」→「구동력에 의한 forward 장벽 강하.」; 「평형은 그대로(detailed balance).」→「평형 불변 (detailed balance).」
- §overlap: 「총합은 선형 중첩.」→「총 ICA 의 선형 중첩.」; 「언제 겹치나(정량 기준).」→「겹침의 정량 기준.」

## 절 양식 일관(확정 정책)
각 본문 절 = **질문(도입) → 명사구 소제목 전개(정의→유도 중간단계→\boxed) → 결과식 직후 「의미.」 해석 → 단서 박스(핵심/유효 범위/비고/심화/검산) → 마감**. "의미."는 \emph{boxed 결과 직후 물리 해석} 라벨로 §lag·§barrier·§dist 3곳 일관 사용 — 유지(churn 회피·내용 보존). 절 요약이 필요한 절(§stage·§eqpeak·§stattools)은 keybox 「핵심」, 범위·한계가 핵심인 절(§dist·§synth)은 boundbox 「유효 범위」로 닫음.

## Read Coverage
- 전문 L1~958 정독(F.0) 기반. 편집 후 grep 전수 감사.

## Execution Evidence
- 빌드: xelatex ×3 → `!` 0 · ref/cite undefined 0 · **19 페이지**(20→19; 스캐폴딩·verbose 제목 제거분, \emph{물리 내용 무손실}) · overfull hbox 0.
- grep 감사: "줄기/정직 표기/만으로 사용/전개의 뼈대/읽기 규약/FLAGGED/미확정/왜 1차 완화/왜 이 양인가/가 왜 peak/정상점이 평형값과 같다/총합은 선형 중첩/언제 겹치나/새 트랙" 전 파일 **0**.

## Validation (4-tier)
- **확정**: 제목 교과서식·author/date 제거·서론 격식·스캐폴딩 제거·박스 5종 격식·메타 자기참조 0·소제목 명사구 일관. 빌드 GREEN. 물리·수식 값 무변경.
- **추정**: 없음.
- **미검증(F.6에서)**: 메타 제거·소제목 변경의 \emph{의미·논리·참조} 무손상 교차모델(Codex) 확인. 19p 감소가 내용 누락 아님을 Codex 로 재확인.

## Gate
**PASS(잠정)** — 형식 편집 완료·빌드 GREEN·grep 감사 0. F.6 Codex 통과 시 PASS_F 확정.

## Next
F.6 Codex 교차모델 적대 리뷰(형식 일관·메타 잔재·의미/논리/참조 무손상) → 판정 → 반복 → PASS_F. 이후 F.7 변경이력 대대적 감사.
