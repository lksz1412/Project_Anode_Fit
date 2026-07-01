# Anode_Fit v1.0.11 개정 작업계획서 (v1.0.10 → v1.0.11 핸드오버) — 정정본 rev.2

> Chain: v1.0.10 문제점 대검수(9종+10차) → **인계 무결성 대검수(9종 Sonnet5/Opus/Codex + 10차, 기록 SPEC 대조, `V1010_HANDOVER_INTEGRITY_REPORT.md`)** + **LCO 수식-주도 검수(3종, `V1010_LCO_STYLE_REPORT.md`)** → 본 핸드오버 rev.2. v1.0.10 동결, 개정은 v1.0.11. 표준 11-section.
> ★rev.1(구본)의 **R1 "폭 모델 구조결함" CRIT은 오판으로 철회**됨(Correction History 참조). 본 rev.2가 유효본.

## Summary
v1.0.11은 **물리 불변** 개정이다 — v1.0.10 인계는 견고함(broadening 복원·KNOWN_DEFECTS·전자엔트로피·Ch2·두 축 전부 보존, 기록 SPEC 대조로 확인)이 확정됐고, 실 개선은 세 가지: ① **LCO 절 수식화**(흑연 forward 틀을 LCO에 재적용하는 6개 절이 "같은 틀 적용/한 줄 더한다"식 줄글 결론 → G-derive 수식 사슬로, 물리·결과식·부호 불변) ② **인계 무결성 minor 정합**(문서 라벨·기록 stale) ③ **default 사용성**(기본 n=1이 4 staging 미표시 — 모델 불변, 표시만). ★**R1 물리 재설계는 철회**(bell은 의도된 apparent-U/η 물리·near-delta 강제 금지). 오적발(bell·면적·논리점핑 6·E2/E3/z_cut)은 개정 대상 아님.

## Current Ground Truth
- **인계 견고(9종+10차·기록 SPEC 대조 확정)**: v10 broadening 복원 word-for-word 보존·KNOWN_DEFECTS 6대 정정 보존·전자엔트로피 무손실 강화·Ch2 무결·두 축(G-derive/G-follow) 유지.
- **★R1 철회(10차 코드 실행 확정)**: 폭을 좁히면(n=0.1→w=2.57mV) 병합 bell이 **4 staging near-delta로 완전 분리** — 모델은 다봉 생성 가능. 단일 bell = 기본값 n=1의 결과, **구조결함 아님**. v1.0.10=v11_final byte 동일(회귀 아님)·면적 0.970000 보존. 두-상 w=SPEC 명시 현상학적 자유 피팅폭(near-delta 낼 의무 없음).
- **LCO 줄글 회귀(3종 확정)**: sec:lco-center(∂U/∂T 괄호 전보체)·sec:lco-hys("같은 틀 적용"×3·Ω_j spinodal 대입 없음)·sec:lco-peak(3전이 박스식 없음)·sec:lco-decomp(config 슬롯 줄글)·전자항 plug-in("한 줄 더한다")·MSMR(변환 사슬 미폐쇄). 정상=sec:lco-map(도입)·lco-Se(완전유도)·lco-gate·N7-9.
- **원천**: `Anode_Fit_v1.0.10.py`·`graphite_ica_ch1_v1.0.10.tex`·`graphite_ica_ch2_v1.0.10.tex`·`FITTING_GUIDE.md`. 검수 `results/process/V1010_HANDOVER_INSPECT_*`·`V1010_LCO_STYLE_*`. cross-version `old/`·`results/code/Anode_Fit_v11_final.py`.
- **기존 결정 계승(불가침)**: use_w_eff 제거·radius/PSD 역변환 배제·forward-only·bell=의도 물리·흑연 회귀 0-diff.

## Phase Range
| 챕터 | Phase | 이름 | Steps | 산출 |
|---|---|---|---|---|
| 1 (LCO 수식화, 물리불변) | 1.1 | sec:lco-center·hys 수식 사슬 | 1-4 | ∂U/∂T·정규용액 LCO 대입 유도 |
| 1 | 1.2 | sec:lco-peak·decomp 수식 사슬 | 5-8 | 3전이 peak 박스·분해 슬롯·이중계산 금지식 |
| 1 | 1.3 | plug-in·MSMR 수식 사슬 + 재빌드 | 9-12 | forward 사슬·MSMR→eqpeak·PDF 0-error |
| 2 (인계 minor) | 2.1 | 기록/라벨 정합 | 13-16 | byte-claim·버전라벨·w_eff 주석·forward-ref·동반개정 제약 |
| 2 | 2.2 | ρ_G 진단 예고 prose(모델 X) | 17 | stretched-tail 후속장 예고 |
| 3 (default 사용성, 모델불변) | 3.1 | 기본값 표시 개선 | 18-20 | n 초기값 4 staging 분리 or 그래프 라벨·꼬리 default 라벨 |
| 4 (이월) | 4.1 | LCO round-trip 피팅·잔여 | 21-25 | x_MIT 0.85·T1 재정렬·T3·T_ref 해제·overfull 재확인 |

## Non-goals (★불가침 — v1.0.11이 하지 말 것)
- **★broadening 물리 재설계 금지**: bell=의도된 apparent-U/η 물리. **near-delta 강제·"near-delta+broadening 2층 convolution 구현" 금지** — 문서가 이미 그 2층을 코드차원 0으로 서술·흡수하고 있으며, 실제 ρ(U_app)/PSD convolution 구현은 SPEC이 ill-posed·forward-only로 배제한 역산 부활 → 복원된 broadening 물리 붕괴(10차 경고).
- **use_w_eff 부활 금지**·**radius/PSD 역변환 도입 금지**·**ρ_G 배리어분포 모델 기계장치 도입 금지**(6-30 [과제 MODEL-1] scope-out 유지 — 진단 prose 예고만 허용).
- **LCO 수식화는 전개 형식만**: 물리·결과식·부호·수치 불변(줄글→수식, 새 물리 X). 전자엔트로피·gate·map 절 손대지 말 것.
- **v1.0.10 파일 in-place 수정 금지** — v1.0.11은 `docs/v1.0.11/` 별도 증판(원본 불가침).
- 오적발(bell·면적 ratio·논리점핑 6·E2/E3/z_cut·use_w_eff 제거) 재개정 금지.

## Implementation Changes
- 신규 `docs/v1.0.11/`(v1.0.10 복사 후 증판). 개정: Ch1 LCO 6절 수식 사슬 추가(Ch1)·헤더 byte-claim/버전라벨(Ch1·Ch2)·코드 헤더 w_eff 주석·FITTING_GUIDE. 신규 ledger·Phase result.

## Phase 1.1 — sec:lco-center·hys 수식화 (Steps 1-4)
- Step 1: sec:lco-center ∂U_j/∂T — ΔG=−sFU→∂U/∂T=ΔS_rxn/F 다리 문장 + (a출발→b미분→c중간식→d박스). 전극무관 논증을 식 eq:n0map 대입으로. 
- Step 2: sec:lco-hys — 흑연 μ(θ)→g″→spinodal→ΔU_hys 사슬에 LCO Ω_j(T2 0.47·T3 1.49 등) **실제 대입 중간식**. "같은 틀 적용" 서술 3회를 LCO-특화 대입 유도로.
- Step 3-4: 자체검수·앞 절 정합·빌드. gate=center·hys 각 결과박스 위 (a)→(d) 사슬·물리 불변(diff=식 추가만).

## Phase 1.2 — sec:lco-peak·decomp (Steps 5-8)
- Step 5: sec:lco-peak — ξ_eq,j→dξ/dV→ΣQ_j peak_shape_j(j∈{T1,T2,T3})→center/height/area 박스(LCO 3전이 합산식).
- Step 6: sec:lco-decomp — Z=Z_config·Z_elec→슬롯 정의 ΔS_j^config=ΔS⁰_j→이중계산 금지식 박스(ΔS_slot≠ΔS⁰_j+R ln[(1−ξ)/ξ]).
- Step 7-8: 검수·정합·빌드.

## Phase 1.3 — plug-in·MSMR + 재빌드 (Steps 9-12)
- Step 9: 전자항 plug-in forward 사슬 x=x(ξ_eq,1(V))→ΔS_e,1(V,T)→ΔS_rxn,1(V,T)→U_1(T)→dQ/dV.
- Step 10: MSMR→정규화→대응대입(f=−σ_d)→ξ_eq,j→peak 박스.
- Step 11-12: 전체 정합·xelatex 0-error·PDF. gate=LCO 6절 전부 수식-주도·G-usable(문건으로 LCO ∂U/∂T·세 봉우리 산출 가능)·물리 불변.

## Phase 2.1-2.2 — 인계 minor (Steps 13-17)
- Step 13(H-1): 전자엔트로피 "byte-identical" 기록(헤더 L9·L32·PHASE_RESULT·FIX_LIST A2)을 "additive·물리무손실"로 재기술.
- Step 14(H-2): 버전 라벨 Ch1 L71/L73 "(v9)"·Ch2 L2/L35/L37 "v5" → "v1.0.11".
- Step 15(H-5): 코드 헤더 L43 w^eff 주석 잔재 제거. Step 16(H-4·H-7): L503-505→L1126-29 forward-ref 1줄·Ch1§broadening↔Ch2파생C 동반개정 제약 명기.
- Step 17(H-3): σ_G/RT stretched-tail 저온 꼬리 진단을 **"후속 kinetic-barrier 장 소관" 예고 prose로만**(★모델 복원 X — Non-goals 준수).

## Phase 3.1 — default 사용성 (Steps 18-20, 모델 불변)
- Step 18: 기본 initial-value가 4 staging 분리를 보이도록 전이별 폭 초기값 조정(n_j 또는 'w') — 모델식 불변, 초기값만. or Step 19: 릴리스 그래프에 "n=1 초기값 병합·피팅 시 분리" 라벨 + 꼬리 default OFF "C-rate=ohmic-shift" 정직 라벨. Step 20: 그래프 재생성·글자 깨짐 방지(영어 라벨 or 한글폰트).

## Phase 4.1 — 이월 (Steps 21-25)
- Step 21-25: LCO round-trip 피팅(x_MIT 0.85·전자항 T1 재정렬·T3 4.17 추가·T_ref 동결 해제 eq:U1T2 ½ 적분)·H-6 overfull 실컴파일 재확인. ★실측 데이터 필요 시 Decision Gate.

## Implementation Interfaces
- LCO 수식화 = **추가만**(결과박스·부호·수치 불변, diff=식 사슬 삽입). 흑연 회귀 0-diff·전자엔트로피 절 byte 보존. 결과 문건 11항목·ledger 12-col. LaTeX 0-error.

## Test Plan
- LCO 수식화: 6절 각 (a)→(d) 사슬 존재·물리 결과식 diff 0(식 추가만)·G-usable(LCO ∂U/∂T·세 봉우리 산출 가능)·xelatex 0-error.
- default: n 초기값으로 4 staging 분리 실측(모델식 불변 확인)·글자 깨짐 0.
- 인계 minor: 버전 라벨·byte 기록·forward-ref 반영. ★오적발 6건 재검 금지.

## Assumptions
- LCO 수식화의 "필요한 수식 사슬"(V1010_LCO_STYLE_REPORT §1)은 흑연 forward 패턴·v9 AUTHOR_BRIEF G-derive 기준 — 물리 불변 전제.
- default 4 staging 분리 폭 초기값은 문헌/피팅 값 필요 시 별도 확보(Phase 4 이월 가능).

## Correction History
- **★rev.1 → rev.2 (최우선 정정)**: rev.1의 **R1 "폭 모델 구조결함(near-delta 생성 불가, CRIT)" + "near-delta+broadening 2층 재설계"를 철회**한다. 근거 = 인계 무결성 대검수(9종+10차, 기록 SPEC 대조 + 코드 직접 실행): (1) 폭을 좁히면 n=0.1→4 staging near-delta 완전분리 → 모델은 다봉 생성 가능·**구조결함 아님** (2) 단일 bell=기본값 n=1의 결과·v11_final byte 동일(회귀 아님)·의도된 apparent-U/η 물리 (3) "2층 재설계"는 문서가 이미 코드차원 0으로 서술·흡수한 것을 실제 convolution으로 구현하려는 것이라, SPEC이 ill-posed·forward-only로 배제한 ρ(U_app)/PSD 역산을 부활시켜 **v3세대 복원 broadening 물리를 붕괴**시킬 위험. rev.1이 R1을 기록 SPEC(broadening_w_design·6-30 핸드오버) 미대조로 오판했음. → R1은 "default n=1 표시 문제(사용성, 모델 불변)"로 재규정, 물리 재설계 삭제.
- rev.1의 R2(꼬리 default OFF)·R3(본문-캡션 부호)·R4(FITTING_GUIDE Ω 충돌)는 유효하나 minor로 재분류(Phase 2-3). R5/R6/R7도 인계 minor로 흡수. LCO 수식화가 rev.2 신규 최대 항목.
