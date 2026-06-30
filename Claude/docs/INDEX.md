# docs/ INDEX (MOC) — 구조 A (문건=docs / 코드·빌드·조사=results)

> 문서 탐색 진입점. **docs/ = 문건(최종 .tex/.pdf, 버전별 폴더)만**. 코드·빌드과정·조사는 `../results/`.
> 본문이 진실 — INDEX 와 충돌 시 INDEX 를 고친다. 문서 추가·수정 시 같은 턴에 해당 행 갱신.
> ★2026-06-30 구조 A 재정리: 흩어진 결과물을 docs(문건)/results(코드·빌드·조사)로 통일. 구버전·빌드산물 → `docs/_archive/`.

## 현재 문건 (docs/ 버전 폴더) — ★최신 = Ch1_v10·Ch2_v5
| 경로 | 1줄 요약 | 동의어 키워드 | 갱신일 |
|---|---|---|---|
| **Ch1_v10/graphite_ica_ch1_v10.tex** | ★★Ch1 v10 **최신**(34p) — v9 + **종모양 broadening 복원**(전이별·현상학적 w·**집합 다입자 통계역학** apparent-U=U_j+η 앙상블·중심 상수·**사이즈 효과 제외**) + w 이중지위 + **w_eff 제거**. LCO 전자 엔트로피·분포 보존 | chapter1, v10, broadening, 종모양, 현상학적 w, 집합 통계역학, ensemble, apparent-U, w_eff 제거, LCO, 전자엔트로피 | 2026-07-01 |
| **Ch2_v5/graphite_ica_ch2_v5.tex** | ★★Ch2 v5 **최신**(13p) — v4 + **w_eff(Ω) 절 제거** + w=두-상 현상학적 자유 피팅 + 종 폭 기원은 Ch1 broadening 참조. 통계열역학 본체 보존 | chapter2, v5, w_eff 제거, 자유피팅, 통계열역학, 분포, 섞임 | 2026-07-01 |
| Ch1_v9/graphite_ica_ch1_v9.tex | Ch1 v9(30p) — 흑연+LCO 통합(전자 엔트로피). ⚠️**broadening 누락 → v10 으로 대체됨** | chapter1, v9, LCO, superseded | 2026-06-30 |
| Ch2_v4/graphite_ica_ch2_v4.tex | Ch2 v4(13p) — 통계열역학. ⚠️**§C w_eff 잘못 → v5 로 대체됨** | chapter2, v4, w_eff, superseded | 2026-06-30 |
| Ch1_v8/v8-11.tex | Ch1 v8(21p) — 유도 확장판(흑연). ⚠️broadening 누락 | chapter1, v8, 유도확장, 흑연 | 2026-06-30 |
| Ch1_v7/v7-11.tex | Ch1 v7(17p) — 코드흐름 간결판 | chapter1, v7, 간결, 코드흐름 | 2026-06-30 |
| Ch2_v3/graphite_ica_ch2_v3.tex | Ch2 v3(5p) — 가역 발열 survey 초안 | chapter2, v3, 가역발열, Bernardi, 초안 | 2026-06-30 |
| _archive/ | 구버전(Opus_v4/v5/v6·Fable_v3·원본 ch1/ch2 — ★broadening 설명 원천) + 빌드산물(.aux/.log) + Archive_old/rebuilt | archive, 구버전, broadening 원천, Opus, Fable | 2026-06-30 |

## ★재작업 진행 중 (2026-06-30, `../plans/2026-06-30-rework-broadening-restore-weff-fix-reorg-plan.md`)
- **Ch1 v10**(예정) = v9 정정·통합 — broadening 복원 + w 이중지위 + w_eff 제거 + 기존 LCO/분포 유지.
- **Ch2 v5**(예정) = w_eff 절 제거 + broadening 참조.
- 누락·개선 분석: `../results/MISSING_CONTENT_REVIEW.md`. 조사: `../results/research/radius`(종모양 origin).

## results/ 안내 (문건 아님)
- `results/builds/{v7,v8,v9,ch2_v4}` — 9종 competition 빌드 과정. `results/code/Anode_Fit_v11_final.py` — Ch1 forward 모델(⚠️use_w_eff 버그·v12 정정 대상). `results/research/` — 조사(LCO·통계열역학·radius). `results/process/` — PHASE/LEDGER/HANDOVER.
