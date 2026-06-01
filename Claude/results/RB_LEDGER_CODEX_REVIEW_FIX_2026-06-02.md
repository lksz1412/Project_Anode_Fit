# RB_LEDGER_CODEX_REVIEW_FIX — Codex 검수 adjudication + 확정 문제 수정 + 하류 10-pass (2026-06-02)

> 트리거: Codex 가 Claude 최종본(ch1~5+full+refs)을 10-pass 검수해 Critical 4·High 5 제출(`Codex/results/PHASE_032_034_…`). 사용자: 검수의견은 Codex 측에 넘김, **확정 문제 수정 + 하류 영향 수식 재검수·재작성, 챕터별 순차 정독 + 청크 길이 바꿔 10-pass**.

## 1. Codex 8개 지적 독립 교차검증 (현재 Claude 실텍스트 대조; `RB_CODEX_V4_CH1_REVIEW_CLAUDE_10PASS.md` 와 대칭)
| 지적 | Codex | 판정 | 비고 |
|---|---|---|---|
| C2 Eyring 부호 `+χA/RT` double-count | CRITICAL | **VALID** | ch1 L780 확정 부호오류(주변 산문·부록 B는 이미 minus) |
| H4 bib placeholder title | HIGH | **VALID(MED)** | jcp2017/lee2011/son2013 placeholder; 정식 title 은 Claude 자체 consolidated_ch1 에 존재 |
| C1 χ_j≡β_j 경계붕괴 | CRITICAL | 과장(LOW) | 본문 L329-330·L368-372 가 이미 강하게 한정; 기호표 gloss 만 무한정 |
| C3 Heaviside step-function | CRITICAL | 과장(수학적 틀림) | H(L−L_min)=Jacobian support 지시자, 유도 명시(L502-505·L1077) |
| C4 amplitude 없는 δ | CRITICAL | 과장(수학적 틀림) | δ=단위면적 확률, 진폭은 A_0/Θ_0 별도 보존(L149·L605-607); Codex Θ_0δ 와 동치 |
| H1 metadata/CHARTER | HIGH | 과장(MED) | 주석/preamble 한정; CHARTER 는 물리규약 anchor(제거 부적합), 단 정의문 부재가 진짜 결함 |
| H2 Ch1 Ch6 과적층 | HIGH | 설계 trade-off | 사용자 5-30 "Ch6 흡수" 지시 이행; label 실제 29(주장 100 오류) |
| H5 n_eff/w_j 충돌 | HIGH | 이미 해소 | Ch1 L315-316 + Ch3 reconcile boundbox(L477-481) |
→ **Critical 4 중 실제 유효 1(C2), High 4 중 1(H4). 나머지 6은 과장.** "Codex canonical" 권고는 Codex v4 자체 CRITICAL(AL-8/9 결번·기본상수 미정의·stretched↔single-L 모순)에 비춰 불성립.

## 2. 확정 문제 수정 (ch1·ch3·full·refs, 물리 변경 없이 부호/title/한정만)
- **★ C2 Eyring 부호**: ch1 L780·full L839 `y(T)=ln(1/(LT)) +χ_jA_j/RT` → **`−`**(minus). 독립 재유도(10개 agent + master): ln(1/(LT))=const+lnκ−ΔH_a/RT+ΔS_a/R+**χA/RT** → 순수 −ΔH_a/R 추출하려면 +χA/RT 를 빼야 함 → minus 가 옳다. 주변 산문 "공급해"→"빼서"(L789) 정합. **교차참조 1줄**(L785-786): raw ln(1/L)(부록 B eq:ch6_arrhenius)의 +χA/RT 를 여기서 빼 순수화, 유효기울기 −(ΔH_a−χA)/R=eq:ch6_arrhenius_slope.
- **H4 bib**: jcp2017(Effects of External Electric Field…)·lee2011(Communication: Propagator…)·son2013(An Accurate Expression…) 정식 title·저자 삽입(ch1·full·refs 3파일). DOI 불변(10.1063/1.5000882·1.3565476·1.4802584).
- **C1 χ_j gloss 한정**: "Ch3 β_j 와 대칭 Marcus 1차·정상 target 극한 한정으로만 동일물 — 일반은 별개" 를 \*모든\* χ_j≡β_j 단정(ch1 기호표·부록 매핑표 L925/L1306, ch3 L77/L109/L134/L174/L361/L676/L826/L858, full 대응)에 균일 부착 — **무한정 단정 잔존 0**(displaymath 사슬은 직후 산문 한정).

## 3. 하류 10-pass 검수 (챕터별 순차 정독, 청크 길이 변경 10회)
P1 기호표(section)→P2 §rate/keystone(70)→P3 §spectrum/kernel(90-offset)→**P4 §simplefit(40-정밀)**→P5 §falsify(55)→**P6 부록 B eq:ch6_arrhenius(dependency)**→P7 AL/bib(120)→P8 Ch2·Ch3(reverse-150)→P9 Ch4·Ch5(fitting-logic)→P10 통합본(full-sweep). 각 pass 독립 재유도.
- **Eyring 부호 수정 = 하류 전 식과 완전 정합**(eyring_consistency OK/NA, downstream "없음" ×10): §simplefit·부록 B eq:ch6_arrhenius(raw +χA/RT 는 모순 아닌 근거)·eq:ch6_arrhenius_slope(−(ΔH_a−χA)/R)·N1/N2·AL-69·파라미터표 모두 minus 정합. 잔존 `+`·double-count 0.
- **Ch2~5 파급 0 확정**: y(T)/ΔH_a 추출식은 Ch1 §simplefit+부록 B 전담. Ch3 는 \*별개\* intrinsic Eyring(eq:ch3_eyring, χA항 없음), Ch2/4/5 는 activation entropy 분리 맥락만 — double-count 버그 구조상 부재.
- **통합본 무결성**: 모든 수정 반영, standalone↔full drift 0. 빌드 GREEN(ch1 2-pass·ch3 2-pass·full 3-pass: `!` 0·undefined ref/cite 0·dup 0·rerun 0).

## 4. 잔존(별개 pre-existing — 이번 수정의 하류 아님, 보고만)
10-pass 가 부수 적발(Codex v4 도 공유하는 lineage 결함): ① Ch1 기호표에 q_a·기본상수 R/F/T/k_B/h 정의행 부재(HIGH, 표 내부 forward-ref) ② RB_CHARTER 미정의 internal term(MED) ③ ln(1/(LT)) vs ln(1/L) prefactor 처리 입도 차(NOTE, 교차참조로 완화). — 이번 Eyring/bib/χ_j 수정과 독립이며 사용자 결정 시 별도 처리.

## 5. 커밋
- 수정: graphite_ica_ch1·ch3·full·refs_rebuilt.tex. result: 본 ledger + `RB_CODEX_V4_CH1_REVIEW_CLAUDE_10PASS.md`(14322e6). commit·push(main+rb).
