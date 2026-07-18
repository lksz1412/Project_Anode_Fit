# Phase P2 — 부록 E 저작 (ratio 닫힘·전달함수·P3-5·warnbox·본문 포인터) Result

## Summary

P1 조건검수(COND-PASS)의 재프레이밍 조건 하에, 자기일관 해법을 **부록 E "자기일관 해법 --- ratio 닫힘과 전달함수"** 로 저작했다(신규 `_sections/ch1_appE_selfconsistent.tex`, ch1_graphite 부록군 말미 편입, 인쇄 letter **E**). 구성 = E.1 참 문제(비선형 Volterra 자기일관)+동결 0차 기준 / E.2 1차 ratio 닫힘(사용자 Eq.34 철학 이식) / E.3 P3-5 5항(서지·위치·구조·매핑·가정차) / E.4 타당성 부등식+(i)(ii)(iii) 1:1 매핑+열화 warnbox / E.5 Laplace 전달함수 / E.6 구현 대응 지도. 서두 warnbox 에 적용 불가(I·III 대수근) 명시. 본문 §8(lag) 말미에 부록 E 포인터 1줄 추가(코드 언급 0). bib 3종 추가(사용자 JCP147 + Ref.6·7). 재빌드 GREEN(err0/undef0/87p), 구조 additive(회귀 0). Prof. 이상엽 convention(원형 식 먼저 → 상호작용 항 복원) 준수.

## Step Range

Cumulative **Step 9 – Step 15** (P1 = 4–8 완료 승계).
- Step 9: 부록 E 골격(E.1~E.6) 신규 파일 + ch1 부록군 편입(letter E)
- Step 10: E.1 lag Volterra 자기일관 + 동결 0차(Prof. convention: 원형 먼저→상호작용 항)
- Step 11: E.3 P3-5 5항 별도 sub-section(enumerate ①~⑤)
- Step 12: E.4 warnbox(열화=타당성 부등식) + 서두 warnbox(적용 불가 I·III)
- Step 13: E.5 Laplace 전달함수 H(ω)=1/(1+iωL_V)
- Step 14: E.6 코드 대응 지도 + bib Ref6·7·JCP147 + 본문 §8 포인터 1줄
- Step 15: 3-pass 재빌드 + 구조 검사 + 본 Result + ledger

## Inputs

- `_sections/ch1_sec08_lag.tex`(L1–145, 전문) — eq:Lq/eq:kuniv/eq:Acut/eq:dHeff/eq:LV 근거.
- `_sections/ch1_appB_codemap.tex`(L1–158, 전문)·`ch2_appA_traps.tex`(L1–76, 전문) — 부록 스타일·letter 규약.
- `_sections/common_preamble_v1023.tex`(L32–62) — 박스 매크로(warnbox/keybox/bgbox/derivbox/srcbox/codebox)·\code.
- `ch1_graphite_v1.0.23.tex`(L1–58, 전문) — 부록 input 순서.
- `_sections/ch1v22_bib.tex`(head+tail) — bibitem 스타일.
- `jcp_extract.txt`(L1–25·711–714) — 서지 grounding.
- `results/PHASE_P1_RESULT.md`·`comp_v23/COND_AUDIT.md` — 저작 근거 수식(P1 검증분).

## Files Created

- `_sections/ch1_appE_selfconsistent.tex` (신규 부록 E, ~135행) — ratio 닫힘·전달함수·P3-5·warnbox·코드 지도.

## Files Updated

- `ch1_graphite_v1.0.23.tex` — 부록 input 목록에 `\input{_sections/ch1_appE_selfconsistent}` 1줄(ch2_appB 뒤).
- `_sections/ch1_sec08_lag.tex` — N7 요약 말미에 부록 E 포인터 1문장(코드 언급 0).
- `_sections/ch1v22_bib.tex` — bibitem 3종(lee2017jcp·lee2011jcp·son2013jcp) `\end{thebibliography}` 앞 삽입.

## Read Coverage

- `ch1_sec08_lag.tex`·`ch1_appB_codemap.tex`·`ch2_appA_traps.tex`·`ch1_graphite_v1.0.23.tex` — **전문 검독**.
- `common_preamble_v1023.tex` — **부분 검독**(박스/매크로 정의 L32–62; 그 외 미검독).
- `ch1v22_bib.tex` — **부분 검독**(head 30행 + tail; 중간 bibitem 미전독이나 삽입엔 무관).
- 라벨 존재 사전 검증: eq:lag/eq:LV/eq:Lqfull/eq:Acut/eq:dHeff/eq:kuniv/eq:Lq/eq:reversal/fig:reversal/eq:sm-mc-balance/eq:memory-Vaxis/eq:tail-limit/sec:tail/sec:lag/sec:eqpeak/sec:broadening/sec:appendix-code — 전부 존재 확인(grep). eq:blend-balance(ch3, 빌드 밖)는 **참조 회피**(산문 처리).

## Execution Evidence

**(1) 3-pass 재빌드** (xelatex nonstopmode, ch2 aux 선존):
```
pass 1 OK / pass 2 OK / pass 3 OK
errors(^!): 0    undefined(ref|citation): 0
Output written on ch1_graphite_v1.0.23.pdf (87 pages)   [P0 baseline 83p + 4p(부록 E)]
```

**(2) 부록 letter 검증** (aux — 충돌 없음, 읽기 순서 A·B·C·D·E):
```
{A}{73}{곡선 부호 사슬 검산표}{appendix.A}
{B}{75}{곡선 계산 구현 대응표}{appendix.B}
{E}{80}{자기일관 해법 --- ratio 닫힘과 전달함수}{appendix.E}   ← \setcounter{section}{4} 로 E 고정
sec:sc-ratio → {E.2}(subsection.E.2)   sec:appendix-selfconsistent → {E}
```
(부록 C·D 는 ch2_appA/appB 의 수동 \section*("부록 C/D") — counter 미증가. auto \section 이 C 로 충돌하던 것을 \setcounter{section}{4} 로 해소 → E.)

**(3) 구조 검사 baseline 대조** (`tools_check_structure.py check`):
| 지표 | baseline(부록E 전) | after(부록E) | 델타 |
|---|---|---|---|
| labels (dup) | 241 (0) | 258 (0) | +17 신규·중복 0 |
| refs (unresolved) | 980 (**19**) | 1026 (**19**) | unresolved **동일**(전부 lco xr) |
| cites / bibitems | 114 / 39 (undef 0) | 127 / 42 (undef 0) | +3 bibitem 전부 인용·undef 0 |
| math blocks (boxed) | 130 (33) | 139 (37) | +4 boxed 신규·파손 0 |
| env pairing errors | 0 | 0 | 0 |
```
unresolved 19 = eq:lco-*·sec:lco-* (Chapter2) — \externaldocument xr 로 실빌드서 해소(undef0).
STRUCTURE_CHECK: FAIL 은 xr 미추적 도구한계(baseline 동일)이지 회귀 아님.
```

## Validation

| Gate (계획서 P2) | 판정 | 근거 |
|---|---|---|
| 재빌드 err0·undef0 | **PASS** | [확인] 3-pass exit0·^! 0건·undef 0건·87p. |
| boxed 무파손 | **PASS** | [확인] boxed 33→37(+4 신규 eq:sc-true/ratio/valid/transfer)·env pairing 0. |
| 구조 PASS(회귀 0) | **PASS** | [확인] unresolved 19 동일(전부 lco xr)·dup 0·신규 label 17 additive·asset tag 265 unique. STRUCTURE_CHECK FAIL=xr 도구한계(baseline 동일). |
| 본문 코드언급 0 | **PASS** | [확인] 본문 편집=§8 포인터 1문장(\code 0·코드 식별자 0·"수치 해법"은 방법 용어). 코드 언급은 부록 E.6(부록 예외 규정). |
| P3-5 5항 별도 sub-section | **PASS** | [확인] E.3 enumerate ①서지 ②위치 ③구조 ④매핑 ⑤가정차. |
| Prof. 이상엽 convention | **PASS** | [확인] E.1 "(원형--동결)" eq:sc-frozen/ref **먼저** → "(상호작용 항 복원--참)" eq:sc-true. |
| 적용 불가(I·III) 서두 명시 | **PASS** | [확인] 서두 warnbox: U_oc 대수근·배경 순환 "이 기법 대상 아님". |
| 수식↔코드 정합 | **예약(P3)** | E.6 지도 서술; 실제 코드 옵션·정합 확인은 P3 Step 16–19. |

**수식 정합(P1 검증분과 대조)**: eq:sc-true κ=κ₀exp[−2χ_d(Ω/RT)(1−ξ)]·eq:sc-valid ε=2χ_d(Ω/RT)Δξ_supp(Δξ_supp≈L_V/4w)·eq:sc-transfer H=1/(1+iωL_V)·동결극한 r₁=r₀ — 전부 PHASE_P1_RESULT 검증치와 일치(전사 오류 0).

## Gate

**PASS.** 부록 E 저작·빌드·구조 게이트 통과. 코드 적용(P3) 진입 허가. 남은 예약 = 수식↔코드 정합(P3 Step 19).

## Confirmed Non-Changes

- **v1.0.22 무접근** — read-only 기준선.
- **ch2·ch3 tex 무수정** — 부록 E 는 ch1 전용. ch2/ch3 aux 재생성 불요(externaldocument 유효).
- **`.py` 코드·test 무수정** — 코드 적용은 P3. 부록 E.6 은 현행 동결 경로(`_causal_memory_pointwise`) 기술 + P3 옵션 예고.
- **본문 물리 서사 무개입** — §8 포인터 1문장 외 본문 무변경. 물리 논리·기존 수식·라벨·기호 보존.
- **기존 bibitem 39종 무변경** — 3종 순수 추가.

## Open Issues / Decision Queue

- **[예약·P3]** 수식↔코드 정합(E.6 지도): P3 에서 func_L_q/_causal_memory ratio·전달함수 옵션 구현 후 Step 19 확정.
- **[근거 미발견·잔존]** Ref.6·7 제목·DOI 미확보(bibitem 에 "원문 대조로 확정" 명기) — D4 기본값 유지.
- **[P5 대상]** 부록 E 독립 적대적 검수(수식 유도 정합·물리 가정·프로젝트 검수 7항)는 P5 4창에서.

## Next

**P3 — 코드 적용(ratio 옵션) (Step 16–20) 진입 허가.** 다음 cumulative step = **16**.
진입 조건: 부록 E.6 지도 기준으로 func_L_q/_causal_memory 에 ratio 보정·전달함수 옵션 추가(동결 경로 bit-exact 보존). Step 16 = func_L_q ratio 보정 옵션(기본 off·동결 bit-exact).

<!-- 자산(P2_RESULT): [P2-01 부록E 신설·letter E(setcounter 충돌해소)·A~E 읽기순서] [P2-02 E.1 Prof convention 원형먼저→상호작용] [P2-03 E.3 P3-5 5항 enumerate] [P2-04 E.4 ε 부등식+(i)(ii)(iii)+열화warnbox] [P2-05 E.5 전달함수 H=1/(1+iωL_V)] [P2-06 E.6 코드지도·현행 동결경로+P3예고] [P2-07 서두 warnbox 적용불가 I·III] [P2-08 재빌드 err0/undef0/87p] [P2-09 구조 additive·unresolved 19 baseline동일·boxed 33→37 파손0] [P2-10 bib 3종·서지 grounding·DOI 미확보 명기] [P2-11 본문 코드언급 0·§8 포인터만] [P2-12 수식↔P1검증분 전사오류0] -->
