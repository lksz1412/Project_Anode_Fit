# 재작업 종합 RESULT — broadening 복원·w_eff 제거·정리(구조 A) [P1-P8]

> plan = `plans/2026-06-30-rework-broadening-restore-weff-fix-reorg-plan.md`. 2026-06-30~07-01. 사용자 분노 3축(broadening 누락·w_eff 오류·파일 중구난방) 대응.

## 0. 산출물
| 항목 | 경로 | 상태 |
|---|---|---|
| **Ch1 v10** | `docs/Ch1_v10/graphite_ica_ch1_v10.tex`(34p) | ★최종 — broadening 복원 |
| **Ch2 v5** | `docs/Ch2_v5/graphite_ica_ch2_v5.tex`(13p) | ★최종 — w_eff 제거 |
| **코드 v12** | `results/code/Anode_Fit_v12.py`(695줄) | ★최종 — use_w_eff 제거 |
| 구조 A | docs=문건 / results=코드·빌드·조사 | ★정리 완료 |

## 1. 사용자 분노 3축 → 대응
### (A) ★종모양 broadening 설명 누락 (v3/v4/v5엔 있고 v8/v9엔 0) → Ch1 v10 복원
- **전이별**: dilute·4L↔3L = solid-solution(이미 종) / **LiC₁₂·LiC₆ 2개만 two-phase**.
- **3기작**: ① 단일입자 유한율속 비대칭 꼬리(L_V) ② 내재 RT/F 폭 ③ ★**집합 다입자 통계역학**(사용자 명확화: 사이즈 빼고 집합 통계역학 반영) — Dreyer 평형 통계역학=plateau 구조 + **apparent-U=U_j+η 앙상블 분포**(★중심 U_j=입자 무관 상수·분포는 η, 비-크기). forward 통계평균 ρ(U_app)·역산 X.
- ★**w_j(두-상)=현상학적 자유 피팅 폭**(평형 예측 아님). ★**사이즈 효과(τ∝r²·반경·PSD) 전면 제외**(사용자 명시·radius 결론).

### (B) ★w_eff 오류 → Ch2 v5·코드 v12 제거
- Ch2 v4 §C 의 $w_\eff(\Omega)$ "종 좁힘→델타" = two-phase 실측(종)과 반대 → 절 완전 제거, w=자유 피팅.
- 코드 `use_w_eff` = 면적보존 깨진 버그(area 9.29 vs Q 0.5) → v12 제거. round-trip: 면적 보존·종모양·v11 거동 동일(diff 0). v11 원본 불가침.

### (C) ★파일 중구난방 → 구조 A
- **docs/** = 문건(Ch1_v7/v8/v9/v10·Ch2_v3/v4/v5 버전폴더) + `_archive`(구버전·빌드산물) + INDEX.
- **results/** = `builds/`(v7·v8·v9·ch1v10·ch2v4·ch2v5)·`code/`(v11·v12)·`research/`(LCO·통계열역학·radius·broadening)·`process/`(PHASE/LEDGER/HANDOVER).
- 임의 폴더 `research/`(최상위) 제거·귀속. 코드 표면화. (work/·old/ = 이전 세션, 미수정.)

## 2. 방법·품질 (competition-cherrypick)
- Ch1 v10 = 9종 빌드 → 검토1(3) → 체리픽 v10-10 → adversarial(3) → finalizer v10-11. ★adversarial A1 이 기작③ "ρ(U_j) 중심 분포 ↔ 중심 상수" **자기모순(CRIT)** 적발 → ρ(U_app=U_j+η)·중심 상수로 재정초(ORIGIN 정합).
- Ch2 v5·코드 v12 = master+sub(surgical). 전자엔트로피 절 byte-identical(SHA 687ba7e6) 보존·w_eff 본문 0·사이즈 cite 0·xelatex 0-error.

## 3. ★확인 요 (사용자)
1. **fly2020·rsc2021 인용**: radius 조사(ORIGIN_VERDICT)의 저자/제목이 실제 DOI 논문과 불일치 — finalizer Crossref 증거우선 교정·tier 정직. 의도 인용이 다른 논문일 가능성.
2. ★**git RB 삭제**: 작업트리에 ★이전 세션의 RB 문건 대량 삭제(RB_LEDGER·graphite_ica_*_rebuilt·_bib_merged 등 470 deletion 중 일부)가 미커밋 — **내 세션 것 아님·git 복구 가능**. 구조 A reorg 이동과 섞여 있어 깨끗한 커밋 위해 **RB 삭제 처리(복구 / 유지) 결정 필요**. (rework 산출물·정리는 별도로 정밀 커밋·푸시됨.)
3. 집합 통계역학③ LCO 적용 = 일반 η 분포(tier-C 가정 명기).

## 4. 커밋 (전부 정밀 스테이징·푸시)
- P1-P4(정리+broadening 설계+9종)·검토1·Ch1 v10 최종·P6/P7(Ch2 v5+코드 v12). RB 삭제 미혼입.
