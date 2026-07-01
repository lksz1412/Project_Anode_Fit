# Anode_Fit v1.0.11 제작 작업계획서 — LCO 수식화 + 인계 minor 정합 (9종 경쟁-체리픽)

> 기반: `docs/v1.0.10/HANDOVER_v1.0.11.md`(rev.2) + `V1010_HANDOVER_INTEGRITY_REPORT.md` + `V1010_LCO_STYLE_REPORT.md`. 작업 방식 = v1.0.10과 완전 동일(9종·검수 별세션·커밋 4/phase·master commit·Agent만·Sonnet5). ★물리 불변 개정(R1 재설계 철회).

## Summary
v1.0.11은 **물리 불변** 증판이다. 인계 무결성 대검수로 v1.0.10 인계는 견고함이 확정됐고(broadening 복원·KNOWN_DEFECTS·전자엔트로피·Ch2·두 축 보존), 실 개선은 셋: ① **LCO 절 수식화**(흑연 forward 틀을 LCO에 재적용하는 6개 절의 줄글 결론 → G-derive 수식 사슬, 물리·결과식·부호·수치 불변) ② **인계 minor 정합**(문서 라벨·기록 stale) ③ **default 사용성**(n=1 병합 표시 — 모델 불변, 표시만). ★**broadening 물리 재설계·ρ(U_app)/PSD convolution·near-delta 강제는 금지**(Non-goals). 본 계획은 `docs/v1.0.11/` 증판 폴더에 Ch1/Ch2 문건·코드·figs·guide 최종 산출물을 모은다.

## Current Ground Truth
- **인계 견고(확정)**: `V1010_HANDOVER_INTEGRITY_REPORT.md` — v10 broadening word-for-word 보존·KNOWN_DEFECTS 6대·전자엔트로피 무손실·Ch2 무결·두 축 유지. R1 "구조결함" 철회.
- **LCO 줄글 회귀(확정 위치)**: `V1010_LCO_STYLE_REPORT.md §1` — sec:lco-center(∂U/∂T 괄호 전보체)·sec:lco-hys(Ω_j spinodal 대입 없음)·sec:lco-peak(3전이 박스식 없음)·sec:lco-decomp(config 슬롯 줄글)·plug-in("한 줄 더한다")·MSMR(변환 사슬 미폐쇄). 각 절 "필요한 수식 사슬"이 REPORT §1 표에 명시됨.
- **정상(불가침)**: sec:lco-map·lco-Se·lco-gate·N7-9 흑연 forward — 수식-주도, 손대지 말 것.
- **원천**: `docs/v1.0.10/{graphite_ica_ch1_v1.0.10.tex(1821줄), graphite_ica_ch2_v1.0.10.tex(750줄), Anode_Fit_v1.0.10.py(742줄), FITTING_GUIDE.md}`. SPEC 기록: `results/builds/v9/v9-00_spine/AUTHOR_BRIEF.md`(LCO G-derive 요구)·`V1010_LCO_STYLE_REPORT.md`·인계 무결성 원자료.
- **인계 minor(H-1~H-8)**: byte-claim stale·버전라벨(Ch1 v9·Ch2 v5)·w_eff 코드주석·magnitude forward-ref·§broadening↔파생C 제약·ρ_G 진단 예고·LCO placeholder(이월).
- **미확인**: default 4-staging 분리 폭 초기값(문헌/피팅 값 — Phase 4 이월 가능).

## Phase Range
| 챕터 | Phase | 이름 | Steps | 산출 |
|---|---|---|---|---|
| 0 | 0.1 | v1.0.11 폴더 증판·전제검증 | 1-2 | docs/v1.0.11/ 복사·인벤토리 대조 |
| 1 (Ch1 LCO 수식화) | 1.1 | sec:lco-center·hys 수식화(9종) | 3-8 | ∂U/∂T·정규용액 LCO 대입 유도 |
| 1 | 1.2 | sec:lco-peak·decomp 수식화(9종) | 9-14 | 3전이 peak 박스·분해 슬롯·이중계산 금지식 |
| 1 | 1.3 | plug-in·MSMR 수식화(9종)·Ch1 재빌드 | 15-20 | forward 사슬·MSMR→eqpeak·PDF 0-error |
| 2 (인계 minor) | 2.1 | Ch1/Ch2 기록·라벨 정합 | 21-24 | byte-claim·버전라벨·w_eff주석·forward-ref·제약·ρ_G 예고 |
| 3 (default 사용성) | 3.1 | 기본값 표시·그래프·샘플 이미지 | 25-27 | n 초기값 or 라벨·figs·글자깨짐0 |
| 4 (최종 점검) | 4.1 | 상호충실도·완성도 최종(9종) | 28-32 | adversarial·마감·result·이월 목록 |

## Non-goals (★불가침)
- **broadening 물리 재설계 금지**(bell=의도 apparent-U/η·near-delta 강제 X·ρ(U_app)/PSD convolution X·ρ_G 배리어 모델 X). **use_w_eff 부활·radius 역변환 금지.**
- **LCO 수식화는 전개 형식만** — 물리·결과식·부호·수치 불변(새 물리 X). sec:lco-map·lco-Se·lco-gate·N7-9·전자엔트로피 절 손대지 말 것(byte 보존).
- **v1.0.10 원본 in-place 수정 금지**(별도 v1.0.11 폴더). 이전 result·핸드오버 덮어쓰기 금지.
- **오적발 재개정 금지**(bell·면적·논리점핑 6·E2/E3/z_cut). **흑연 회귀 0-diff·전자엔트로피 byte** 유지.
- default 사용성은 **초기값/라벨만**(모델식 불변).

## Implementation Changes
- **Phase 0**: `docs/v1.0.11/` = `docs/v1.0.10/` 복사(Ch1 tex·Ch2 tex·`Anode_Fit_v1.0.11.py`·figs/·FITTING_GUIDE.md). 헤더 버전 v1.0.11로.
- **개정 대상**: Ch1 v1.0.11 tex의 LCO 6절(수식 사슬 추가)·헤더 byte-claim/버전라벨 · Ch2 v1.0.11 tex 버전라벨·§broadening 제약 · 코드 헤더 w_eff 주석·default 초기값(선택) · FITTING_GUIDE.
- 신규 `V1011_EXECUTION_LEDGER.md`·Phase result `V1011_P*_RESULT.md`·Codex 거울 동반.

## Phase 0.1 — 폴더 증판·전제 검증 (Steps 1-2)
- Step 1: `docs/v1.0.11/` 생성(v1.0.10 복사)·헤더 버전 갱신. gate=파일 존재·xelatex 기존 0-error 재현.
- Step 2: 전제 검증 — LCO 6절 줄번호·"필요한 수식 사슬"(REPORT §1)·손대지 말 절 경계를 실제 tex와 대조(load-bearing 전제). 거짓이면 STOP→Correction History.

## Phase 1.1 — sec:lco-center·hys 수식화 (Steps 3-8, 9종)
- Step 3(9 드래프트, 3S·3O·3C 무통신): sec:lco-center(∂U/∂T: ΔG=−sFU→∂U/∂T=ΔS/F 다리+(a→d)·전극무관 eq:n0map 대입) + sec:lco-hys(μ(θ)→g″→spinodal→ΔU_hys에 LCO Ω_j 실제 대입 중간식) 수식 사슬 supplement. **커밋①**.
- Step 4: 검토1(별세션)+보완. **커밋②**. Step 5: master 체리픽 vN-10. **커밋③**. Step 6: adversarial(별세션)+finalizer(Ch1 tex 실편입·재빌드). **커밋④**. Step 7-8: 물리 불변 검증(결과식 diff=식 추가만·부호·수치 불변)·앞 절 정합.
- gate: center·hys 각 (a)→(d) 사슬·"같은 틀 적용" 서술 3회→LCO 대입 유도로·물리 결과식 불변·xelatex 0-error.

## Phase 1.2 — sec:lco-peak·decomp 수식화 (Steps 9-14, 9종)
- Step 9-12(9종 루프): sec:lco-peak(ξ_eq,j→dξ/dV→ΣQ_j peak_shape→center/height/area 박스, j∈{T1,T2,T3}) + sec:lco-decomp(Z=Z_config·Z_elec→슬롯 ΔS⁰_j→이중계산 금지식 박스). 커밋 4회.
- Step 13-14: 이중계산 직교 수식 잠금 검증·정합. gate=3전이 합산 peak 박스·분해 슬롯 명시·G-usable(세 봉우리 산출 가능).

## Phase 1.3 — plug-in·MSMR + Ch1 재빌드 (Steps 15-20, 9종)
- Step 15-18(9종 루프): 전자항 plug-in forward 사슬(x=x(ξ_eq,1(V))→ΔS_e,1(V,T)→ΔS_rxn,1→U_1(T)→dQ/dV) + MSMR→정규화→대응대입(f=−σ_d)→ξ_eq,j→peak 박스. 커밋 4회.
- Step 19-20: Ch1 전체 정합·xelatex 0-error·PDF. gate=LCO 6절 전부 수식-주도·전자엔트로피 절 byte 보존·물리 불변.

## Phase 2.1 — 인계 minor 정합 (Steps 21-24)
- Step 21(H-1): 전자엔트로피 "byte-identical" 기록 → "additive·물리무손실" 재기술(Ch1 헤더).
- Step 22(H-2): 버전 라벨 Ch1 "(v9)"·Ch2 "v5" → "v1.0.11"(헤더·pdftitle·lhead·filename 주석).
- Step 23(H-5·H-4): 코드 헤더 w^eff 주석 제거·전자항 magnitude forward-ref 1줄.
- Step 24(H-7·H-3): Ch1§broadening↔Ch2파생C 동반개정 제약 명기·σ_G/RT stretched-tail 진단 "후속 kinetic-barrier 장 예고" prose(★모델 복원 X).
- gate: 라벨·기록 정합·물리 불변.

## Phase 3.1 — default 사용성·샘플 이미지 (Steps 25-27)
- Step 25: 기본 initial-value 4 staging 분리(전이별 n_j/w 초기값 조정, 모델식 불변) or 릴리스 그래프 "n=1 병합·피팅 시 분리" 라벨. 꼬리 default OFF "C-rate=ohmic-shift" 정직 라벨.
- Step 26-27: 샘플 테스트 이미지 재생성(코드 함수·클래스·★영어/ASCII 라벨·글자깨짐 0)·figs/ 정리. gate=4 staging 분리 실측(모델 불변)·글자깨짐 0.

## Phase 4.1 — 최종 점검 (Steps 28-32, 9종)
- Step 28-31(9종): 상호충실도(Ch1↔Ch2↔코드)·완성도·두 축 최종 감사 → 검토1 → 체리픽 → adversarial → finalizer. 
- Step 32: `V1011_P*_RESULT.md`·이월 목록(LCO round-trip 피팅·H-6 overfull·H-8 placeholder). gate=두 축 무결·LCO 수식-주도 달성·물리 불변·CRIT/HIGH 0·PDF 0-error.

## Implementation Interfaces
- LCO 수식화 = **추가만**(결과박스·부호·수치 불변, diff=식 사슬 삽입). Serena 심볼 도구(tex는 절 단위 편집). 흑연 회귀 0-diff·전자엔트로피 byte. Result 11항목·ledger 12-col. Codex 거울 동반 커밋.

## Test Plan
- LCO 수식화: 6절 각 (a)→(d) 사슬 존재·물리 결과식 diff 0(식 추가만)·부호검산·G-usable(LCO ∂U/∂T·세 봉우리 산출)·xelatex 0-error.
- 코드: 흑연 회귀 0-diff(np.array_equal)·default 4 staging 분리 실측·전자엔트로피 −45.68·글자깨짐 0.
- 인계 minor: 버전라벨·byte 기록·forward-ref 반영. ★오적발 6건 재검 금지·broadening 물리 불변.

## Assumptions
- LCO "필요한 수식 사슬"(REPORT §1)은 흑연 forward 패턴·v9 AUTHOR_BRIEF G-derive 기준 — 물리 불변 전제.
- default 4 staging 분리 폭 초기값은 문헌/피팅 값 필요 시 Phase 4 이월(모델식 불변).

## Correction History
- 본 계획 = 인계 무결성 대검수·LCO 수식-주도 검수 후 핸드오버 rev.2 기반 첫 실행 계획. 이전 rev.1 핸드오버의 R1 "구조결함" 물리 재설계는 철회됨(bell=의도 물리) — 본 계획은 물리 불변·수식화·정합만 다룬다. broadening 재설계·ρ 역산 도입은 Non-goals로 금지.
