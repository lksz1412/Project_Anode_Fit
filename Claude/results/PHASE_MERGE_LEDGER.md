# PHASE_MERGE Ledger — Ch1+Ch2 단일 챕터 병합 (50p+, 실질·무패딩)

Plan: `Claude/plans/2026-06-09-merge-ch1-ch2-single-chapter-plan.md`. 작업본 `graphite_ica_merged.tex`(완료 시 정식 ch1 승격, 구 ch2 아카이브).
원칙: 절 단위 순차 루프·절마다 빌드·최대 effort·NO Workflow·**실질 물리만(무패딩, 비약 0)**·keep/cut 권고표 확정.

| Phase | 절 | 출처 | 작업 | Status |
|---|---|---|---|---|
| M0 | preamble·서론 | 신설 | 통합 기호·제목·식번호 단일 + **서론 병합 arc 재작성**(관측에 히스 추가·도착점=통합식·Ω spine·PART B forward) | PASS 26p, undefined 0 |
| M1 | §2 기호 | 구1+2 | 통합 표(히스 기호 dis/chg/hys/Ω/γ 합치기) | **TODO — 복사만, 통합 재작성 미완** |
| M2 | §3 전하보존 | 구1 §2 | 병합 맥락 정합 점검·다듬 | **TODO — 복사만, 통합 재작성 미완** |
| M3 | §평형 peak | 구1 §3 | 이상 logistic + §정규용액 forward 정합(범위밖→다음절, 일부 반영) | **부분 — flagbox만 수정, 절 전체 재검토 미완** |
| M4 | §정규용액·상분리(sec:regsol) | 구2 §2 이동 | Ω≠0 확장·g''/T_c·binodal/spinodal·**lever rule CUT·CNT 정성 trim·vdW 도구 KEEP·Dreyer KEEP** ★ | PASS 25p (앞 §3 eq:mu/smix 내부 인용, 뒤 sec:hys_branch forward) |
| M5–M10 | §동역학–§겹침 | 구1 §4–§9 | 동역학·통계·종합(방전)·겹침 — 병합 맥락 정합·worked 뒤사용·§master는 §통합 master로 흡수 | **TODO — 복사만, 통합 재작성 미완** |
| M11–M12 | §충방전 분기(sec:hys_branch) | 구2 §4+§5 | V_eq 부호반전·spinodal ξ_s±·ΔU_hys·γ_j 중심 — §정규용액 g'' 위에서, **master 직접 손검(Codex 0)** | PASS 26p, undefined 0 |
| M13–M15 | §분기dQ/dV·동역학 분극·부분cycle | 구2 §6–§8 | peak쌍(면적=Q_j,갈림=γΔU)·gap 분리(열역학 절편+2\|I\|R_n)·return-point+h_j(Preisach TRIM·3분해 lumped) | PASS 28p |
| M16 | §통합 master(sec:master) | 재작성 | 방전 eq:master + **충방전 통합 eq:hys_master**(분기중심·분극부호 방향별)·환원검산 2(Ω≤2RT→단상·I→0→열역학 gap)·파라미터 Ω/γ·S5 gap·예측 양방향 ★ | PASS 29p |
| M-기호 | §기호 | 통합 | Ω_j 확장·T_c/ξ_s±·γ_j·ΔU_hys·U_j^dis/chg 행 추가 | PASS |
| M18 | §검증·반증 | 구1+히스 | 기존 진단표 + **충방전 히스 반증**(\|I\|→0 절편 유무·온도 (T_c−T)^{3/2} 소멸) | PASS 29p |
| M17 | §데이터→예측 | 구1§8(통합 master서 흡수) | S1–S5·walkthrough·예측 양방향 | (통합 master 절에 포함) |
| M2–M10 PART A | 구1 §2–§9 | 정합 | 평형/동역학 물리는 건전·§정규용액·통합 master로 연결됨. 잔여=경미 정합 점검 | 부분(복사 본문+forward 연결) |
| M19 | 최종 검증 | — | 50p+ 여부·orphan 0·Codex 적대검수·구ch2 아카이브·ch1 승격·커밋 | TODO (현재 29p) |

## keep/cut 적용 추적
- CUT: lever rule(구2 §2). TRIM: CNT식→정성(구2§2.3), 과전압3분해→lumped(구2§7), Preisach/FORC→return-point+h_j(구2§8).
- KEEP+재작성: g''·T_c·common tangent·vdW(도구화)·Dreyer·미시기원·worked들·식별성 — 모두 뒤 사용처 연결.

## Findings
- M0: 작업본=ch1 복사+통합 preamble. 24p clean. git이 원본 ch1/ch2 보존.
- **6-09 시정(박사님 분노)**: 구 Ch1 복사를 "PART A 완료"로 친 것이 잘못. PART A 절들은 \emph{복사일 뿐} — 계획서 line 77 규율(구 원문 이식→통합 재작성→빌드→앞 절 정합) 미적용. 서론도 standalone 그대로였음. → 메모리 `feedback_no_shortcut_reuse_as_done`. PART A 각 절을 병합 맥락으로 genuine 재작성해야 PASS. (Codex 적대검수 위임은 문제 아님 — 직전 오해 메모리 삭제.)
- M0 서론: 병합 arc 재작성 완료(관측 히스 추가·도착점 통합식·Ω spine·PART B forward). 26p, undefined 0.
