# 재작업 계획서 (제대로) — broadening 복원 + w_eff 제거 + 정리(A) / Ch1 v9→v10 통합 / 9종 체리픽

> 핸드오버(`results/process/HANDOVER_2026-06-30_radius-dqdv-distribution-and-w-eff-bug.md`)·누락검토(`results/_FINAL/MISSING_CONTENT_REVIEW.md`)·radius verdict 기반. ★사용자 결정 4건 baked(아래). GO 시 P1부터 무중단. 원본불가침(현 v9·이전 result·구버전 tex·radius 산출).

## ★결정 사항 (사용자 확정 — Decision Gate 없음)
- **D1**: Ch1 = **현 v9 를 정정·업데이트한 통합본 v10** 작성 — broadening + LCO 전자 엔트로피 + ξ_eq 분포 + w 이중지위 + 모든 정정 "**전부 통합**"(현 v9 는 archive 보존).
- **D2**: **w_eff 완전 제거** — 코드 `use_w_eff` 경로 제거 + 문서(Ch1·Ch2)의 w_eff(Ω) 절 제거. **w 는 두-상서 자유 피팅 파라미터**(평형 예측 아님).
- **D3**: **다입자/PSD convolution 모델 제외** — radius 조사(PC Claude Code, `research/radius`) 결론 = 입자분포 추출 *의미 없음*. broadening 은 *설명(텍스트)*으로만 복원, 모델 확장 X.
- **D4**: 문서 작성 = **9종 competition-cherrypick** 스킬(`Project_skills/competition-cherrypick-authoring`).

## 1. Summary
v8/v9 가 v3/v4/v5 의 **종모양 broadening 설명**(평형 델타 vs 실측 종·w=현상학적 피팅 폭)을 덜어냈고, 내가 Ch2 v4 에 **두-상서 무의미한 w_eff(Ω)→델타 그림**을 새로 박았으며, 코드 `use_w_eff` 는 면적보존 깨진 버그다. 본 재작업 = (1) 파일 구조 정리(A) (2) ★**Ch1 v10 통합본** 9종 체리픽 — broadening 설명 복원 + w 이중지위 + w_eff 제거 + 기존 LCO/분포 유지 (3) Ch2 v5 — w_eff 절 제거 + broadening 참조 (4) 코드 v12 — use_w_eff 제거. **다입자 모델은 안 만든다**(설명만).

## 2. Current Ground Truth (확정)
- **누락(grep)**: v9·v8 에 broadening/현상학적-w 0건; v5 에 22건.
- **종모양 = 현상학적 피팅 폭**(radius·v4/v5): two-phase(LiC₁₂·LiC₆) 평형은 델타에 가깝지만 실측은 **유한 종** — 유한율속 꼬리(모델 L_V) + 내재 RT/F 폭이 폭을 정함 → **w_j(두-상) = 자유 피팅 폭, 평형 예측 아님**. dilute·4L↔3L = 원래 종(solid-solution). ★평형 U_j 분포·반경 분포 추출 = 무효/의미없음(D3).
- **w 이중지위**: 단상 Ω<2RT = nRT/F 평형 예측 / 두-상 Ω>2RT(staging 4개 전부) = 현상학적 자유 피팅.
- **코드 버그**: use_w_eff 시 면적 9.29(Q=0.5 위반)·ξ_eq 폭(25.7mV) ≠ 분모 w(1.28mV). 기본(use_w_eff=False·명시 w)은 정상 종.
- **현 산출**: docs/results 중복·research 임의폴더(정리 P1 대상). 구버전 broadening 원천 = docs/graphite_ica_ch1_Opus_v4·v5·Fable_v3.

## 3. Phase Range (chapter→Phase→step, cumulative)
| Chapter | Phase | 이름 | Steps | 주체 |
|---|---|---|---|---|
| A 정리 | P1 | 구조 A 통일(docs/results·research 귀속) | 1–4 | master |
| B 설계 | P2 | broadening+w 통합 설계(radius grounded·모델확장 X) | 5–9 | master(+서브 검증) |
| C Ch1 v10 | P3 | spine·AUTHOR_BRIEF(현 v9 + broadening + w 정정 명세) | 10–12 | master |
| C | P4 | 9종 독립 빌드 → 커밋#1 | 13–17 | 9 Agent |
| C | P5 | 검토1→보완→검토2→체리픽 v10c→adversarial→**Ch1 v10**+10회 | 18–36 | 스킬 골격 |
| D Ch2 v5 | P6 | w_eff 절 제거 + broadening 참조(9종 or master+sub) | 37–45 | 스킬/서브 |
| E 코드 | P7 | use_w_eff 제거 → v12 + round-trip 검증(승인 baked) | 46–49 | master |
| F | P8 | 종합 RESULT·교수님 제시본 | 50–52 | master |

## 4. Non-goals
- ★**다입자/PSD convolution 모델 X**(D3). dQ/dV=∫g(r)f(V;r)dr 안 만든다. broadening 은 *설명*만.
- ★**반경→평형 U_j 분포 부활 X**·**dQ/dV→분포 역산 X**(ill-posed).
- ★원본불가침: 현 graphite_ica_ch1_v9(archive 보존·overwrite X)·`Anode_Fit_v11_final.py`(정정은 새 v12)·이전 result/ledger/handover·구버전 tex·radius.
- LCO 전자 엔트로피·통계열역학 분포(기존 v9·Ch2 v4 추가분)는 *유지·통합*(삭제 X).
- work/·old/(이전 세션) 삭제 X — 보고만.

## 5. Implementation Changes (구조 A 경로)
- 정리: 최종 문건 → `docs/`(버전별·구버전 `docs/_archive/`); 코드·빌드·조사 → `results/`(버전별·`results/code/`·`results/process/`); `research/`→results 귀속·비움.
- Ch1 v10: `results/ch1v10/`(9종 빌드) → `docs/graphite_ica_ch1_v10.tex`(+pdf).
- Ch2 v5: `results/ch2v5/` → `docs/graphite_ica_ch2_v5.tex`.
- 코드 v12: `results/code/Anode_Fit_v12.py`(use_w_eff 제거; 현 v11 보존).
- 종합 `results/process/PHASE_REWORK_RESULT.md`.

## 6. Phase 상세 (5-stage: plan→exec→result→validation→ledger)

### P1 (1–4) 구조 A 통일
- docs = 문건(최종 .tex/.pdf, 버전별) + `_archive/`(구버전 Opus_v4/v5·Fable·원본 ch1/ch2·빌드산물) + INDEX. results = 코드·빌드(버전 폴더)·`code/`·`process/`(PHASE/LEDGER/HANDOVER)·조사(research 귀속). research/ 비움. **Gate**: docs/results 분리·research 빔·중복 0·INDEX 갱신·git 정밀 스테이징(RB 삭제 미혼입)·work/old 보고.

### P2 (5–9) broadening+w 통합 설계 [radius grounded]
- `DOCS_say`(v4/v5 verbatim)·ORIGIN/RADIUS/BAND_VERDICT 종합 → **Ch1 v10 broadening 절 설계**: ① 전이별 출발(dilute·4L-3L solid-solution = 원래 종 / LiC₁₂·LiC₆ two-phase = 평형 델타) ② 실측 종 = 유한율속 꼬리(L_V) + 내재 RT/F 폭 → **w_j(두-상)=현상학적 자유 피팅 폭** ③ ★평형 U_j·반경 분포 추출 무효(forward-only·ill-posed, D3 모델화 X) ④ w 이중지위 ⑤ w_eff 제거 사유. **Gate**: 배치·물리 근거(radius DOI)·모델확장 0·4-tier.

### P3 (10–12) Ch1 v10 spine·BRIEF
- base = 현 v9(graphite_ica_ch1_v9). AUTHOR_BRIEF: 통합 명세(broadening 절 신규 + w 이중지위 + w_eff 제거 + 기존 흑연/LCO/분포 보존). 9 작가 배포.

### P4 (13–17) 9종 독립 빌드 → 커밋#1
- v10-01–03 Sonnet·04–06 Opus·07–09 Codex(무통신). broadening 설계(P2) + w 정정 반영. master 검증·커밋.

### P5 (18–36) 검토1→보완→검토2→체리픽→adversarial→Ch1 v10
- 렌즈: ★broadening 정합(전이별·현상학적 w·forward-only·모델확장 0)·w_eff 잔존 0·기존 LCO/분포 보존·G-derive·부호·인용. 체리픽 v10c → adversarial → v10 최종 + 10회. 커밋#2~4.

### P6 (37–45) Ch2 v5 — w_eff 제거 + broadening 참조
- Ch2 v4 §C(w_eff) **제거** + w=자유 피팅 명시 + 종모양은 Ch1 broadening 참조. 9종(또는 master+sub — 정정 규모 따라). **Gate**: w_eff 잔존 0·통계열역학 분포 유지·Ch1 정합.

### P7 (46–49) 코드 v12 — use_w_eff 제거 (D2 승인 baked)
- `Anode_Fit_v11_final.py` 복사→v12, use_w_eff 경로·플래그 제거(w 명시만). round-trip: 면적=Q 보존·종모양·기본 거동 불변. 현 v11 보존. **Gate**: 면적 보존·거동 동일·v11 불변.

### P8 (50–52) 종합·교수님 제시본
- RESULT 11항목·누락 0(broadening·w·ρ_G 설명)·제시 패키지. **Gate**: broadening 복원 확인·제시 준비.

## 7. Implementation Interfaces
- 정리=PowerShell/git mv(원본 보존). 설계=radius 1차문헌 grounded(추측 0). 문서=9종 competition-cherrypick(N+9+9+1+1)·4-세션 고지·sub commit/push 금지. 코드=현 v11 불가침→v12 신규. Agent만(Workflow X)·milestone commit+push(Anode_Fit 자동).

## 8. Test Plan
- 정리: docs/results 분리·research 빔·중복 0·INDEX 정합.
- broadening: 전이별 구분·현상학적 w·forward-only·★모델확장 0(다입자 X)·radius DOI 정확.
- w_eff: 코드·문서서 잔존 0·w 이중지위·종모양 broadening 일관.
- 코드 v12: 면적 보존 round-trip·기본 거동 불변·v11 보존.
- 전반: xelatex 0-err·기존 LCO/분포 보존·tier 정직.

## 9. Assumptions
- broadening 복원이 핵심(사용자 분노 직결). radius 물리 근거 검증됨. 다입자 모델 불요(D3). 코드 v12 승인됨(D2). 구버전 tex 접근 가능.

## 10. (Decision Gate 없음 — 4건 전부 확정)

## 11. Correction History
- 2026-06-30 v1(DG 4건 open) → v2(제대로): 사용자 결정 baked — D1 v10 통합·D2 w_eff 제거·D3 다입자 X·D4 9종. ★GO 시 P1(정리)부터 P8 무중단(정지 5조건만).
