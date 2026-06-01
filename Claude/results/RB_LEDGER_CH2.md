# RB_LEDGER_CH2 — Chapter 2 재구성 Result (Phase 2, step 43–62)

> 자율 진행(사용자 위임 5-31/6-1): Ch1 방식(grounded 무비약 재유도 + 3렌즈 빡센 적대검수) 그대로. Decision Gate(사용자 검토) → 적대검수 통과로 대체. 매 단계 commit/push/merge.
> 계획서: `Claude/plans/2026-05-30-undergrad-rederivation-rebuild-plan.md` Phase 2. 규약: `RB_CHARTER.md`. AL: `RB_AL_MASTER.md`.

## 1. Phase·범위
Ch2 = (Ch1 상태변수 $V_n,\xi_j,k_j$ 위) **전지 가역 반응열 해석**. 산출 `graphite_ica_ch2_rebuilt.tex`.

## 2. Read Coverage (전문 정독 대상)
- 입력: `graphite_ica_consolidated_ch2.tex`(흐름 골격) + `_body_ch2_v2.tex` + `graphite_ica_chapter2_CLAUDE_criticalfix_5-29.tex`(salvage) — draft 에이전트 전문 정독.
- 상속: `graphite_ica_ch1_rebuilt.tex`(상태변수·gold standard), `RB_CHARTER.md`(5규약), `RB_AL_MASTER.md`(AL-20·21 + 채울 22~29), `RB_REFERENCES_DOSSIER.md`(DOI).
- Codex/ 산출물 read 금지 준수.

## 3. G-flow (골격 보존)
consolidated_ch2 핵심식(eqbal·implicitT·dVocvdT·dxidV/dT·srcdecomp·balance·fluxforce·Ieta·revOCV·revxi·consistency·hbg/bgsplit·rest/relax/feedback) 전부 보존+무비약 재유도. salvage 흡수: entropy_coeff·eyring_entropy·qrev(Peltier)·affinity/sigma·thermal_kernel → 새 §3(entropy 토대)·§11(열적 거울).

## 4. Grounding / AL 추가
AL-22~29 신규 정의(`RB_AL_MASTER.md` 등재 완료). AL-20(Bernardi balance)·AL-21(∂U/∂T=reaction entropy) 기등재 인용. 모든 본문 가정식 AL-# 태그, 무태그 established 0.

## 5. 무비약 재유도 (방향-1·2)
온도미분(∂/∂T at fixed q) 음함수 정리, 몫미분(∂z/∂T), logistic 역함수 $V_{\eq,j}$, Bernardi $\dot n=I/(s_\phi F)$ $s_\phi$ 상쇄, σ_j Taylor 1차전개 — 중간단계 전부. 본문 비약어("자명/clearly/obviously/쉽게") **0건**(헤더 주석만).

## 6. 적대검수 (3렌즈 병렬, 반증 임무)
물리·열역학 / 수학·무생략 / 정합·CHARTER·grounding. **CRITICAL 0**(양측 sympy 17개 항등식 교차검증 일치). CHARTER 5규약 전부 준수, Ch1↔Ch2 정합 clean, cite↔bibitem·DOI 프로그램 검증 clean.

## 7. 발견·정정 (2 HIGH + 3 MEDIUM, 삭제 0)
| 등급 | 위치 | 정정 |
|---|---|---|
| HIGH | eq:ch2_qirr 양정치 | q_irr≥0 (2법칙)이 **기본형 $V_\drive=V_n$ 전제**에서만 항별 닫힘 명문화. 강구동 일반형 → Ch3(forward/back)+Ch4($n^\eff$) forward-ref (over-claim 해소) |
| HIGH | eq:ch2_sigma 차원 | per-mode σ_j = W/mol(intensive)인데 W로 취급되던 것 → $(Q_{j,\tot}/F)$[mol] 환산식 eq:ch2_qirrkin_ext 추가(Ch1 ρ_G 교훈의 Ch2 대응). 형제 발열항(W)과 차원 정합 |
| MED | thermal_kernel | calorimetry 검정 독립성 = $r_j(q_a)$ 공통값 근사를 Ch1과 공유 → **준독립** cross-modality 정합으로 한정 명시 |
| MED | eq:ch2_consistency | A/B의 $s^\conv$가 동일 heat-positive 규약에서 유도돼야 제약이 부호모순 없이 닫힘 명시 |
| MED | AL-27 | degrootmazur1962 = book(ISBN), DOI 누락 오독 방지 표기 |

## 8. 빌드·무결성
tex **908줄**, PDF **20p** → `Claude/results/graphite_ica_ch2_rebuilt.pdf`. env: equation 36/36, begin/end 64/64. 진짜 undefined ref/cite **0**, "undefined references"/"may have changed" 경고 0, Overfull hbox **0**, `!` 에러 0.

## 9. CHARTER 준수 (G-cross)
step1 s_φ 명시·q_irr=|I|η 양정치 / step2 η=V_drive−V_eq 단일·기본 V_drive=V_n·4전위 구분·∂V_app/∂T 금지차단 / step3 n^eff=1 특수형+Ch4 forward-ref / step4 keystone 열적대응 detailed-balance 극한 한정 / step5 AL-20~29 단일번호. 3렌즈 정합 에이전트 각 항목 "준수" 판정.

## 10. FLAGGED/BOUNDED 잔존 (정직)
- FLAGGED: AL-29 열적 tail novel(저온 긴 ICA tail ↔ 저온 큰 비가역열 tail) — 준독립 calorimetry forward-prediction 전제.
- BOUNDED: AL-22(용량 온도무관)·AL-23(OCV계수 SOC 부호반전)·AL-24(두 entropy 별개)·AL-26(background entropy)·AL-28(rate≠heat force)·AL-29-σ(near-eq 선형). q_irr 양정치 = V_drive=V_n + n^eff=1 이중 전제(명시됨).

## 11. Next
Phase 3 (Ch3 = Ch1 기반 전기화학 반응속도론 일반화, step 63–88). Ch3에서 Level B(forward/backward $r^\pm$, χ=β) zoom-in → Ch2의 강구동 q_irr 일반형 양정치를 Ch4와 함께 닫음. main 머지·push 자동(사용자 위임).
