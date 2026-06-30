# Phase 3.1–3.3 — Ch3_Fable(발열) 전면 재작업 Result

## Summary
`graphite_ica_ch3_Fable.tex` 11절 전부 전문 정독·재작업. **물리 결함 1건 적발·수정**(η_hys 비가중 vs q_hys 가중 불일치 — |I|·η_hys≠q_hys 였음 → α_j 전류분율 가중으로 정합) + 구조 표현 정정(병합 후 "직전 장"→"앞 장", 7곳).

## Step Range
25–38.

## Inputs
ch3_Fable 전문(479행) · ch1_Fable.aux 인계 스냅샷(불변 확인).

## Files Created / Updated
Updated: ch3_Fable.tex(기호표 η_hys·eq:h_eta_split+해설·직전→앞 장)·pdf. Created: 본 result.

## Read Coverage
ch3_Fable **전문**(서론 62–94 · 기호 100–125 · 배경 128–194 · 가역열 197–240 · 히스열 243–292 · 분극열 295–324 · 전이별 327–339 · 열수지 342–379 · 되먹임 382–413 · 파라미터 416–435 · 종합식 438–470 · bib) — 생략 0.

## Execution Evidence
xelatex 2-pass: 9p, overfull 0, undefined 0. 인계 인용 (1.1)(1.3)(1.6)(1.15)(1.20)(1.21)(1.23)(1.48)(1.49) — ch1_Fable .aux 와 전수 일치(불변).

## Validation
- 수정: η_hys=Σα_j½γΔU(기호표+eq:h_eta_split)+정합 해설("진행 중인 전이만 과전압으로 느낀다, |I|η_hys=q_hys") / "직전 장"→"앞 장"(병합 구조 정합).
- 검산 일치(무수정 근거): Bernardi 부호·차원 / σ̇=Iη/T≥0 / eq:h_dVdT 가중 / q_hys=loop 면적(방전+충전=γΔU·Q_j) / 준정적 비가역 논증 / τ_th·ΔT∞·Biot·Duhamel / 안정성 dQ/dT<hA_s / 환원검산 3종 / worked 수치(30·16·8mV·54mV·0.24K).

## Gate
**PASS** (빌드 0/0·인계 일치·복붙금지 gate: 전 절 행범위+수정/무수정 근거).

## Confirmed Non-Changes
가역열·히스열·분극열·열수지·되먹임·종합식 본문 물리 무수정(검산 일치). 원본 ch3.tex/pdf 불가침.

## Open Issues / Decision Queue
없음.

## Next
Phase 4.1(Ch4_Fable) · step 39.
