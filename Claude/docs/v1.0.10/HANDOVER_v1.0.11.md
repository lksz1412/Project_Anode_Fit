# Anode_Fit v1.0.11 개정 작업계획서 (v1.0.10 → v1.0.11 핸드오버)

> Chain: v1.0.10 문제점 대검수(9종 절별 루핑 + 10차 재검, `V1010_PROBLEM_REPORT.md`) → 본 핸드오버. v1.0.10은 진단으로 동결, 개정은 v1.0.11에서 수행. 표준 11-section 양식.

## Summary
v1.0.10 문제검수가 확정한 진짜 문제(R1 CRIT · R2-R4 HIGH · R5-R6 MED · R7 문서)를 v1.0.11에서 개정한다. 뿌리는 **R1 폭 모델 구조 결함**(두-상 staging 전이에 단일자리 Nernstian 폭 `w=nRT/F` 보편 적용 → 4 전이 뭉갠 bell 병합, near-delta+broadening 2층 부재) 하나이며 R2(꼬리 default OFF)가 그 파생. 나머지는 저비용 실 결함·문서 정합·강등 이월. **오적발(논리점핑 6·면적 3·E2·E3·z_cut)은 개정 대상 아님**(쫓지 말 것). 이번 계획은 진단→설계→구현→검증까지 다루되, ★**설계 승인(Decision Gate)까지가 이 핸드오버 범위** — 물리 모델 변경(R1)은 사용자/교수 검토 후 GO.

## Current Ground Truth
- **확정 사실(10차 실측)**: 단일전이 FWHM=90.57mV·Ω 무관·4-staging peak 1개·면적 wide-window 1.000000(물리 정상)·L_V≤0.00125×격자문턱(꼬리 OFF)·충전꼬리 본문↔캡션 부호 모순·FITTING_GUIDE Ω 하한 vs Ch1 solid-solution 충돌.
- **원천 파일**: `Anode_Fit_v1.0.10.py`(742줄)·`graphite_ica_ch1_v1.0.10.tex`(35p)·`graphite_ica_ch2_v1.0.10.tex`(13p)·`FITTING_GUIDE.md`. 검수 원자료 `results/process/V1010_INSPECT_*`. cross-version `old/_archive/{v3,v4,v5}`·`old/Ch1_v{8,9,10}`.
- **기존 결정 계승**: use_w_eff 제거 정당(Ω>2RT 음수폭 버그) — 되살리지 않음. radius/PSD 역변환 배제·forward-only 정당 — 유지. 흑연 회귀 0-diff 원칙 유지.
- **미확인**: R1의 올바른 near-delta+broadening 2층 물리 형태(Maxwell 참 폭=kBT 가장자리 곡률 계산·실측 broadening 규모)는 미확정 — 설계 단계 과제. 두-상 초기 폭의 실측 앵커 값 미확정.

## Phase Range
| 챕터 | Phase | 이름 | Steps | 산출 |
|---|---|---|---|---|
| 1 (R1 CRIT) | 1.1 | 폭 구조 결함 진단·물리 확정 | 1-3 | near-delta+broadening 2층 물리 명세 |
| 1 | 1.2 | 모델 설계 (Decision Gate) | 4-6 | 설계안·API 변경 청사진·사용자 GO |
| 1 | 1.3 | 구현·검증(흑연 4 staging 분리·면적·회귀) | 7-11 | 개정 코드·그래프·회귀 |
| 2 (R2-R4 HIGH) | 2.1 | R3 본문 부호 정정 (저비용 선행) | 12 | Ch1 L1609-10 정정·재빌드 |
| 2 | 2.2 | R4 FITTING_GUIDE Ω 하한 전이별 재작성 | 13-14 | guide 정합 |
| 2 | 2.3 | R2 꼬리 활성화 or 그래프 라벨 명시 | 15-17 | 꼬리 default 재설정·검증 |
| 3 (R5-R7) | 3.1 | R5 v4 단상 narrowing prose 각주 복원 | 18 | Ch1 각주(코드 미개입) |
| 3 | 3.2 | R6 irreversible_heat 가드·R7 표시/글리프 | 19-20 | 코드 가드·회귀 명칭·폰트 |
| 4 (강등 이월) | 4.1 | 클러스터 D round-trip 피팅(LCO 물리값·T² 곡률) | 21-25 | 실측 피팅·전자항 T1 재정렬·Sommerfeld 복원 |

## Non-goals
- **오적발 개정 금지**: 논리점핑 6·면적(G1)·E2·E3·z_cut·q_rev/seam 무결 — 손대지 말 것(10차 오적발 확정).
- **use_w_eff 부활 금지**(정당 제거). **radius/PSD 역변환 도입 금지**(ill-posed).
- **v1.0.10 파일 in-place 수정 금지** — v1.0.11은 별도 버전 폴더/파일(`docs/v1.0.11/`)로 증판(v1.0.10 원본 불가침).
- Phase 1.2 Decision Gate 전 R1 물리 모델 변경 **착수 금지**(사용자/교수 GO 대기).
- 흑연 forward 무관 일반론(KWW·Marcus·lever) 재유입 금지(header 의도적 컷 계승).

## Implementation Changes
- 신규 버전 폴더 `docs/v1.0.11/`(v1.0.10 복사 후 증판) — 코드·Ch1·Ch2·figs·guide.
- 개정: 코드 `_width`/`GRAPHITE_STAGING_LIT`(R1)·`dqdv` 꼬리 디폴트(R2)·`irreversible_heat`(R6) · Ch1 §width·L1609-10(R3)·단상 각주(R5) · FITTING_GUIDE Ω 하한(R4)·표시 명칭(R7).
- 신규 ledger `V1011_EXECUTION_LEDGER.md` · 각 Phase result `results/process/V1011_P*_RESULT.md`.

## Phase 1.1 — 폭 구조 결함 진단·물리 확정 (Steps 1-3)
- Step 1: Maxwell 공통접선 두-상 평형 dQ/dV의 참 폭 유도(kBT 가장자리 곡률·유한 Ω 효과)·near-delta 규모 정량. 입력=Ch1 broadening 절·regular-solution. 산출=참 평형 폭 닫힌식. gate=식→식 유도 완결·수치 검산.
- Step 2: 관측 유한 폭의 물리 기원 분리 — 열역학(near-delta) vs kinetic 분극(꼬리) vs 이질성(apparent-U 분포). 실측 broadening 규모 앵커. gate=3원 분리 명세.
- Step 3: 2층 모델 요구사항 확정(평형 near-delta core + phenomenological broadening layer, Ω 반영 채널). gate=요구사항 명세서.

## Phase 1.2 — 모델 설계 · Decision Gate (Steps 4-6)
- Step 4: 설계안 N종(예: (a)near-delta+Gaussian/Lorentzian broadening 합성곱 (b)Ω-의존 유효폭 재도입(음수폭 가드) (c)전이별 broadening 자유 파라미터 분리) 비교·물리 타당성. 
- Step 5: API 변경 청사진(`_width` 확장·transition dict 키·흑연 회귀 영향·면적보존 유지). 
- Step 6: **★Decision Gate** — 사용자/교수에 설계안 제시, GO 대기(물리 모델 변경은 승인 필수). 중단 조건=GO 전 구현 금지.

## Phase 1.3 — 구현·검증 (Steps 7-11)
- Step 7-8: 승인 설계 구현(Serena, 흑연 경로 회귀 영향 최소화). Step 9: 4 staging 분리 실측(local max 4개·FWHM 전이별). Step 10: 면적보존·온도의존·부호 회귀. Step 11: 그래프 재생성·bell→spike 확인. gate=4 peak 분리·면적 1.000·회귀 PASS.

## Phase 2.1-2.3 — HIGH 실결함 (Steps 12-17)
- Step 12 (R3): Ch1 L1609-10 "V가 큰 쪽"→"낮은 V 쪽" 1문장 정정·부호검산 재실행·재빌드. gate=본문↔캡션↔코드 일치.
- Step 13-14 (R4): FITTING_GUIDE Ω 하한을 전이별로(단상 후보 Ω<2RT 허용·two-phase만 Ω>2RT) 재작성. gate=Ch1 solid-solution 구분과 정합.
- Step 15-17 (R2): 디폴트 dVdq_qa/L_V 재설정으로 꼬리 활성화 or graph suite "C-rate 의존"이 ohmic-shift임을 명시. 실측 꼬리 개형 확인. gate=꼬리 활성 or 라벨 정직.

## Phase 3.1-3.2 — MED·문서 (Steps 18-20)
- Step 18 (R5): Ch1에 v4 단상 narrowing `w_eff=(RT/F)(1−Ω/2RT)`(Ω<2RT 평형 예측) prose 각주 복원(코드 미개입). 
- Step 19 (R6): `irreversible_heat` q_irr 부호 가드 또는 docstring caller 계약 강화. 
- Step 20 (R7): 회귀 "면적=Q assert" 명칭↔gate(golden bit-exact) 정합·PNG 한글 폰트.

## Phase 4.1 — 강등 이월 (Steps 21-25)
- Step 21-25: 클러스터 D — LCO 실측 round-trip 피팅(x_MIT=0.85·전자항 T1=MIT 재정렬·T3 4.17 추가)·T_ref 동결 해제(`func_dSe_molar` T 전달·eq:U1T2 center-T_ref 별도적분 ½=a_e/2F). ★독립 실측 데이터 필요 시 Decision Gate.

## Implementation Interfaces
- 개정 코드는 흑연 forward 회귀(np.array_equal 골든) 유지가 원칙이나, R1은 폭 물리 변경이라 **의도적 회귀**(골든 재캡처+변경 사유 ledger). transition dict 신규 키(broadening 파라미터)는 하위호환(부재 시 기존 거동). 결과 문건 = 11항목·ledger 12-col. 그래프는 4 staging 분리·spike/bell 라벨 명시.

## Test Plan
- R1: 4 staging local max 개수·전이별 FWHM·면적보존(wide window 1.000)·Ω 의존성(폭이 Ω 반영되는지)·온도의존.
- R2: L_V vs 격자문턱·C-rate 곡선 변화(꼬리 vs ohmic 분리).
- R3: 본문↔캡션↔코드 방향 일치·부호검산 재실행.
- R4: guide bounds로 단상 전이 Ω<2RT 피팅 가능성.
- 전반: LaTeX 0-error 재빌드·회귀 스크립트·논리 의존성 검수(단 오적발 6건 재검 금지).

## Assumptions
- R1의 올바른 2층 물리 형태는 Phase 1.1-1.2에서 확정(현재 미확정) — 설계 승인 전 임시.
- 두-상 초기 폭 실측 앵커는 문헌/GITT 값 필요 시 별도 확보.
- LCO round-trip(Phase 4)은 실측 데이터 가용성에 의존 — 없으면 tier-C 유지·이월.

## Correction History
- 본 핸드오버 = v1.0.10 문제검수(9종+10차)의 첫 산출. 이전 계획 없음.
- ★10차 재검이 union의 오적발(논리점핑 6·면적 3·E2·E3·z_cut) 기각 → v1.0.11 개정 대상에서 제외(과거 계획이 이들을 포함했다면 여기서 정정). R1이 유일 CRIT임을 확정, 나머지 저비용·강등으로 재baseline.
