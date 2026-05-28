# Chapter 1 (v4 canonical synthesis) — 10-Round Review Ledger

**Date**: 2026-05-28
**Target**: `Claude/docs/graphite_ica_chapter1.tex` (canonical synthesis, ~705 lines)
**Binding**: Charter v3 / `MASTER_ROADMAP_v3.md` §9bis (synthesis spine) / `ASSUMPTION_LEDGER_v3.md`
**사용자 지시**: "작성하고 10회 검수 진행한 뒤 그 결과를 보고" (2026-05-28)
**검수 성격**: agent-driven 독립 검수(편향 제거) + orchestrator self-verification 혼합.

본 canonical = v4 synthesis(Codex spectrum + Claude rigor) 에 \textbf{dual-track closure}
(1안 Fredholm+Refs 6/7 closed-form / 2안 direct numerical validator+fallback / single-mode
floor + 정량 switch) 와 full-cell $V_{\cell}$ bridge 를 병합한 판.

---

## Round 요약

| R | Lens | Driver | 결과 | 핵심 |
|---:|---|---|---|---|
| 1 | LaTeX/ref integrity | self | FIX | broken ref `eq:relax`→`eq:r_ode` |
| 2 | math/dimensional/dual-track algebra/cross-section | agent | CONDITIONAL | ★ V_app bridge 기호 충돌(HIGH); 2안 validator 범위(LOW); L 정규화(LOW) — 나머지 차원·대수 PASS |
| 3 | grounding / dual-track HONESTY / non-uniqueness / verbatim | agent | CONDITIONAL | dual-track 정직성 PASS; S10 태그 GROUNDED→오해소지(HIGH); ratio ansatz "self-consistent" 문구(LOW) |
| 4 | logic/leaps / falsification / publication (referee) | agent | CONDITIONAL | ★ Volterra→Fredholm 근사 무명시(HIGH); eq:closed 대수 블랙박스(HIGH); ★ χ vs η_ct co-linearity = 최대 referee 공격면(MED); 2안 "always valid" 과장(MED) |
| 5 | mechanical re-verify | self | FIX | broken ref `sec:relax`→`sec:rate`; 그 외 0 broken, step-func 0 정의식 |
| 6 | 수정 후 독립 재검증 (8 fix items + new-issue) | agent | **PASS** | 8 fix 전부 FIXED-CORRECTLY; new issue 0; eq:closed 대수 재유도 일치 |
| 7 | cross-document (AL-# ↔ Ledger, spine S#) | self | PASS | AL-1~10 일치; S1-S14 완비(S3 복원) |
| 8 | Korean prose + English term | self | PASS | 학술 term 영어, prose 한글; 과도 한글화 0 |
| 9 | referee weakest-point / overclaim | self | PASS | χ/η_ct co-linearity 해소; dual-track honesty 확인; "확정"→"시사+protocol" |
| 10 | holistic sign-off | self | PASS | R5 mechanical + R6 독립 + R7 cross-doc 종합 PASS |

---

## 적용 수정 (Round 1-5 발견 → 전수, Round 6-7 검증)

| Fix | 출처 | 내용 | 검증 |
|---|---|---|---|
| F1 | R1 | `eq:relax`→`eq:r_ode` | R5 |
| F2 (★HIGH) | R2,R4 | **V_app bridge 분리**: anode `V_{n,app}=V_n+s_I\|I\|R_n` vs full-cell `V_cell=V_p−V_{n,app}−IR_{Ω,sep}` (eq:vapp_bridge) 별개 기호화 + η 중복계상 금지 | R6 FIXED-CORRECTLY |
| F3 (★HIGH) | R4 | **Volterra→Fredholm 단계 0 명시**: frozen source + kernel decay ≪ window 조건; §switch 가 오차 측정 | R6 FIXED-CORRECTLY |
| F4 (★HIGH) | R4 | **eq:closed 대수**: eq:closed_pre (ratio 대입) + factor-out 중간 단계 삽입 | R6 재유도 일치 |
| F5 (HIGH) | R3 | **S10 태그 GROUNDED+DQ→BOUNDED+DQ** + AGP self-check 에 "적용성 measured-switch 강등, exact 주장 X" | R6 FIXED-CORRECTLY |
| F6 (★MED) | R4 | **χ_j vs η_ct co-linearity caveat** (§falsify): 단일 electrode 데이터서 퇴화; 다중 T×\|I\|+GITT 로 분리, η_ct 분리 후에만 χ_j 귀속 | R6 FIXED-CORRECTLY |
| F7 (MED) | R2,R4 | 2안 "always valid"→"numerically exact given A_L+closure, discretization 제한" + "공유 모델 오류는 ε 로 안 잡힘" | R6 FIXED-CORRECTLY |
| F8 (LOW) | R2 | L 정규화 ($v_Q/k$ in Q ↔ $\|I\|/(Q_\cell k)$ in q) 명시 | R6 |
| F9 (LOW) | R3,R4 | ratio ansatz "self-consistent"→"reference 정의상"; "실제로 적용한 산출물"→"본 형식에 적용해 얻은" | R6 |
| F10 (LOW) | R4 | ε_tol "fitting/검증 단계서 설정, 구체값 P1 외" | R6 |
| F11 (cosmetic) | R6 | spine S3 행 복원 (broadening, S2/S8 흡수) | R7 |

---

## 최종 상태
- **CRITICAL 0 / HIGH 0 / MEDIUM 0** 잔존 (R6 독립 재검증 PASS).
- 0 broken refs/cites, 0 uncited bib, 0 boxed-align, step-function 정의식 0 (전부 negation).
- AL-1~10 grounding 완비; FLAGGED(AL-3b/7적용성/8) established 미사용; BOUNDED(AL-2/5/6) 유효범위 병기.
- ★ dual-track closure 정직성 확인: 1안 closed-form 은 exact 주장 X, measured switch(ε)로 gating; 2안 = numerically-exact-given-model reference; single-mode floor. Volterra→Fredholm 근사를 \emph{주장 아닌 측정}으로 처리.
- ★ 최대 referee 공격면(χ_j vs η_ct co-linearity) 명시적 caveat + 분리 설계로 방어.
- activation barrier 유지, equilibrium smooth, "가우시안"=예시, Korean prose+English terms.

## 잔여 (data/후속)
- DQ-v3-1 (isotherm/broadening 형태) · DQ-v3-2 (1안 Fredholm 적용성 = switch 로 측정) ·
  DQ-v3-3 (χ_j/Marcus) · DQ-v3-4 (tail source 판별) · DQ-v3-5 (ν_j(T)). 모두 fitting/실험.
- LaTeX build: 로컬 LaTeX 부재 → 사용자 환경(xelatex+kotex/Overleaf).
- Codex 도 병행 작성 중 (rebuilt_v1 과 수렴; `COMPARISON_CLAUDE_v4_vs_CODEX_REBUILT.md`).
