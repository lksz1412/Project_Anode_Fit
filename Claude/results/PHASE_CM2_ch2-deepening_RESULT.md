# PHASE 3.1–3.9 — Ch2 내용 심화 + 구조·표기 수정 Result

## Summary
박사님 지적(절번호 11.1·식 2.13 칸 벗어남·내용 부족) 수용. (1) 절번호 챕터 anchor(Ch1=1.x, Ch2=2.x), (2) eq:hys_master(2.12)·eq:hys_master_center(2.13) 다단 박스로 overfull 해소, (3) Ch2를 교과서 깊이로 실질 보강(9p→11p).

## Step Range
Steps 55–90 (Phase 3.1–3.9).

## Inputs
- `graphite_ica_ch2.tex`(주), `graphite_ica_ch1.tex`(\thesection만). 계획 `2026-06-08-ch2-content-deepening-plan.md`. 직전 fe53739.

## Files Updated
- `graphite_ica_ch1.tex`: `\thesection=1.\arabic{section}` (절번호 1.x) [3.1].
- `graphite_ica_ch2.tex`:
  - [3.1] `\thesection=2.\arabic{section}`; eq:hys_master·eq:hys_master_center 다단 박스(overfull 해소).
  - [3.2] §2.2 심화: 혼합 entropy 조합론 기원·평균장 enthalpy(쌍확률 ξ(1−ξ), Ω~z[ε_AB−½(ε_AA+ε_BB)])·**g'' 곡률 eq:hys_gpp**·임계온도 T_c=Ω/2R·공통접선=등μ·lever rule·van der Waals 등온선 유추.
  - [3.3] §2.3 심화: 세 영역(안정/준안정/불안정)·고전 핵생성 이론(임계반지름 r*~γ_s/|Δg|, 장벽 ΔG*∝γ_s³/Δg²)·spinodal 과주행 기전.
  - [3.3] §2.4 flagbox: Dreyer 풍선 다발 비유 추가.
  - [3.4] §4: g'' 중복 제거(eq:hys_gpp 참조)·vdW loop/Maxwell 등면적 작도→평탄선 vs 준안정 가지.
  - [3.5] §5: 히스테리시스 loop 일주 그림·분기 선택 단조성 근거·U_j=(U_dis+U_chg)/2.
  - [3.6] §7 대폭: R_n 과전압 3원 분해(ohmic·전하전달 η_ct≈(RT/F)|I|/i_0·확산)·충방전 반대부호·kinetic lag 정량(ΔV_kin≈|dV_n/dq|L_q)·분극 vs lag 형상 구별·수치 감(R_n 20Ω·cm², ΔV_pol~16mV).
  - [3.7] §8: Preisach/hysteron·scanning curve·FORC·major loop=포락선.
  - [3.8] §6: 수치 예제 박스(Ω=4RT→T_c=596K, ξ_s±≈{0.15,0.85}, ΔU_spin=54mV, γ=0.6→gap≈32mV; Ω=8RT→0.22V).

## Read Coverage
- ch2.tex 개정 구간(§2 113–217, §4 244–292, §5 295–337, §6 340–369, §7 362–404, §8 385–410) 정독·재확인. ch1.tex preamble.

## Execution Evidence
- 빌드 2-pass: ch1 exit0 overfull0 undefined0 21p; ch2 exit0 overfull0 undefined0 11p.

## Validation (4-tier)
- **확정 PASS** — G3.1(절번호 2.x/1.x·overfull0)·G3.2~G3.8(보강 요소 grep 존재)·빌드 clean.
- **확정 PASS** — 신규 수치 손검: T_c=2T=596K, ξ_s±=½±½√0.5≈{0.146,0.854}, γ·54=32.4mV, Ω=8RT→8.59RT/F=0.221V, |I|R_n=8mV·ΔV_pol=16mV 전부 재현. g''=RT/[ξ(1−ξ)]−2Ω=eq:hys_slope 정합. CNT·Preisach·vdW 표준.
- **미검증** — Codex 교차검수: 본 phase 직후 foreground.

## Gate
**CONDITIONAL PASS** — 빌드·손검 PASS. Codex 직후.

## Confirmed Non-Changes
- 정확성 확인 유도(V_eq·spinodal·ΔU_hys·master) 식 본체 불변(eq:hys_gpp는 §4가 이미 쓰던 g''을 §2에 numbered로 승격, §4는 참조로 전환). 라벨 보존(신규 eq:hys_gpp만 add). 단일문건 규율 유지.

## Open Issues / Decision Queue
- 없음. (추가 분량은 물리가 요구하는 만큼; 패딩 회피.)

## Next
- Codex foreground 적대검수(보강 물리·수치·정합) → MAJOR 시 정정·재커밋 → 종합 보고.
