# PHASE_MERGE Ledger — Ch1+Ch2 단일 챕터 병합 (50p+, 실질·무패딩)

Plan: `Claude/plans/2026-06-09-merge-ch1-ch2-single-chapter-plan.md`. 작업본 `graphite_ica_merged.tex`(완료 시 정식 ch1 승격, 구 ch2 아카이브).
원칙: 절 단위 순차 루프·절마다 빌드·최대 effort·NO Workflow·**실질 물리만(무패딩, 비약 0)**·keep/cut 권고표 확정.

| Phase | 절 | 출처 | 작업 | Status |
|---|---|---|---|---|
| M0 | preamble·서론 | 신설 | 통합 기호(dis/chg/hys/pol/kin/obs)·제목·식번호 단일 | 작업본 골격 PASS(24p) / 서론 통합 TODO |
| M1 | §2 기호 | 구1+2 | 통합 표 | TODO |
| M2 | §3 전하보존 | 구1 §2 | 이식 | (ch1 그대로 존재) |
| M3 | §4 평형 peak | 구1 §3 | 이상 logistic | (존재) |
| M4 | §정규용액·상분리(sec:regsol) | 구2 §2 이동 | Ω≠0 확장·g''/T_c·binodal/spinodal·**lever rule CUT·CNT 정성 trim·vdW 도구 KEEP·Dreyer KEEP** ★ | PASS 25p (앞 §3 eq:mu/smix 내부 인용, 뒤 sec:hys_branch forward) |
| M5–M10 | §6–§11 | 구1 §4–§9 | 동역학·통계·종합(방전)·겹침 + worked 피팅anchor 통합 | TODO |
| M11–M12 | §충방전 분기(sec:hys_branch) | 구2 §4+§5 | V_eq 부호반전·spinodal ξ_s±·ΔU_hys·γ_j 중심 — §정규용액 g'' 위에서, **master 직접 손검(Codex 0)** | PASS 26p, undefined 0 |
| M13–M15 | §분기dQ/dV·분극·부분cycle | 구2 §6–§8 | (분극 3분해 trim·Preisach trim) | TODO |
| M16 | §17 통합 종합식 | 신설 | eq:master+eq:hys_master 한 절 ★ | TODO |
| M17 | §18 데이터→예측 | 구1§8+구2§10 | 전 파라미터 피팅·예측 | TODO |
| M18 | §19 검증·반증 | 구1§11+히스 | 진단표 falsify 사용 | TODO |
| M19 | 검증 | — | 50p+·orphan 0·Codex·구ch2 아카이브·ch1 승격·커밋 | TODO |

## keep/cut 적용 추적
- CUT: lever rule(구2 §2). TRIM: CNT식→정성(구2§2.3), 과전압3분해→lumped(구2§7), Preisach/FORC→return-point+h_j(구2§8).
- KEEP+재작성: g''·T_c·common tangent·vdW(도구화)·Dreyer·미시기원·worked들·식별성 — 모두 뒤 사용처 연결.

## Findings
- M0: 작업본=ch1 복사+통합 preamble. 24p clean. git이 원본 ch1/ch2 보존.
