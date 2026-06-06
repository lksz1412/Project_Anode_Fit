# Phase F.0 — 인벤토리·설계 Result

**Date**: 2026-06-06 · **Plan**: `2026-06-06-ch1-textbook-form-plan.md` · **Step Range**: 1–4 · **챕터**: F(Form)

## Summary
완료본 Ch1(958줄·20p) 전문 재정독 → 교과서 형식화 대상(메타·자기참조·절 구조 불일치) 전수 인벤토리 + 고정 절 골격(§FT)·박스 분류(§BX)·제목(§TT)·서 trim 확정. 사용자 5+1 피드백 전부 반영.

## Read Coverage
- `graphite_ica_ch1.tex` L1~958 \emph{전문 2분할 정독}(1~490, 490~958). 절 11개·박스 6종·소제목·마감 패턴 전수.

## 인벤토리(확정)

### A. 제거/격식화 대상 메타·자기참조
| 위치 | 현재 | 처리 |
|---|---|---|
| L55~58 | verbose 3행 제목(ICA 피크의 물리 + 부제 2행) | 교과서식 "Chapter 1" + 간결 주제(§TT) |
| L59 | `\author{Project_Anode_Fit (새 트랙)}` | `\author{}` |
| L60 | `\date{2026-06-03}` | `\date{}` |
| L97~112 | "전개의 뼈대." enumerate 로드맵 | 제거(목차 \tableofcontents 가 대체) |
| L114~120 | "읽기 규약." keybox(작성 방법론) | 제거 |
| L39 | flagbox "미확정(FLAGGED)" | "비고"로 리네임 |
| L40 | rigorbox "심화(형식적 엄밀화 — 줄기 밖)" | "심화"로 리네임 |
| L38 | boundbox "유효범위(Validity bound)" | "유효 범위" 간결화 |
| L41 | verifybox "검산 (차원·극한·부호)" | "검산" 간결화 |
| L802 | "실무 피팅 근사식 (Chapter 1 만으로 사용 가능)" | 괄호 제거 → "실무 피팅 근사식" |
| L316 | "본 장 줄기는 이상 극한…" | "본 장 본문은…" |
| L681 | "줄기에는 분율 보존만으로 충분" | "본문에는 분율 보존만으로 충분" |
| L747 | "본문 줄기에는 이 형식이 필요 없다" | "본문에는 이 형식이 필요 없다" |
| L861 | "본 장 범위와 식별 교란 요인(정직 표기)" | "(정직 표기)" 제거 |
| L368 | "검산 박스에서 …" | "아래 검산에서 …" 또는 식 직접 참조 |
| 주석 L2·5·9·12·15 | "백지/줄기/Author/도구" 주석 메타 | 정리(빌드 무영향, 경량) |

### B. 절 구조 불일치(점 5)
- **도입**: 본문 절 9개(§stage·eqpeak·lag·barrier·stattools·dist·synth·overlap·falsify) 모두 `\textbf{질문.}` 일관 ✓. §notation 만 사전 도입문(예외 OK).
- **소제목(\textbf / \subsection)**:
  - 명사구: "전하 보존식." "해의 유일성(…)." "측정 전위와 구동 전위." "도함수." "세 결과(…)." "지연의 방정식과 그 해." "배리어 분포." (다수)
  - 의문형(통일 대상): "왜 이 양인가." "왜 1차 완화인가." "왜 $\chi$ 와 $1-\chi$ 로 쪼개지고 합이 1인가." "$\dd Q/\dd V_n$ 가 왜 peak 인가"(\subsection)
  - 문장형(통일 대상): "정상점이 평형값과 같다" "전위가 forward 장벽을 낮춘다." "속도상수는 활성화 배리어가 정한다(Eyring)." "평형은 그대로(detailed balance)." "총합은 선형 중첩."
- **마감(통일 대상)**: keybox(§stage 무대 요지 / §eqpeak 평형만으로는 / §stattools 요약) · "의미."(§lag L510 / §barrier L622) · boundbox 마감(§dist / §synth) · 평문(§overlap 분리 가능성의 한계 / §falsify).

## 확정 결정(권고값 채택)
- **§TT 제목**: `\textbf{\LARGE Chapter 1}` + 줄바꿈 + `\Large 흑연 음극 dQ/dV 피크의 물리`. author/date 비움.
- **§BX 박스 5↔6종 리네임**: keybox "핵심"(유지) · stagebox "흑연 staging 배경"(유지) · boundbox **"유효 범위"** · flagbox **"비고"**(←미확정/FLAGGED) · rigorbox **"심화"**(←형식적 엄밀화—줄기 밖) · verifybox **"검산"**(괄호 간결화).
- **§FT 고정 절 골격**(본문 절): ① 도입 `\textbf{질문.}` → ② 전개(소제목 **명사구 통일**·정의→유도 중간단계→\boxed) → ③ 결과·해석 → ④ 단서 박스(§BX) → ⑤ 마감(요지=keybox 「핵심」 / 범위·한계=boundbox / 해석=prose, "의미." 라벨 제거).
  - **소제목 명사구화 매핑**: "왜 이 양인가."→"평형 전환율의 출처"; "왜 1차 완화인가."→"1차 완화의 근거"; "왜 $\chi$·$1-\chi$…합 1인가."→"$\chi$·$(1-\chi)$ 분할과 합 1의 근거"; "$\dd Q/\dd V_n$ 가 왜 peak 인가"→"$\dd Q/\dd V_n$ 의 peak 발생"; "정상점이 평형값과 같다"→"정상점과 평형값의 일치"; "전위가 forward 장벽을 낮춘다."→"구동력에 의한 forward 장벽 강하"; "속도상수는 활성화 배리어가 정한다(Eyring)."→"속도상수의 활성화 배리어 (Eyring)"; "평형은 그대로(detailed balance)."→"detailed balance 와 평형 불변"; "전위가 forward…"·"총합은 선형 중첩."→"선형 중첩".
  - **마감 통일**: §lag·§barrier 의 "의미." → 라벨 제거 후 해석 문단으로(또는 keybox 「핵심」). §overlap "분리 가능성의 한계." → boundbox 또는 유지.

## Validation (4-tier)
- **확정**: 전문 정독 완료·인벤토리 전수·결정 확정. 본문 절 도입 "질문." 이미 일관(통일 부담 경감).
- **추정**: 없음.
- **미검증**: 소제목 명사구화·마감 통일의 \emph{의미 보존}은 절별 적용 시 G-flow·Codex 로 확인.

## Gate
**PASS** — 정독 커버리지 100%·메타 목록 전수·§FT/§BX/§TT/서trim 확정.

## Next
F.1 front matter(제목·author/date·서 trim) → 빌드.
