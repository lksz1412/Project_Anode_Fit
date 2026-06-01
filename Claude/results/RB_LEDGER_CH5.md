# RB_LEDGER_CH5 — Chapter 5 재구성 Result (Phase 5, step 111–132)

> 자율 진행(사용자 위임). Ch1 방식. Decision Gate → 3렌즈 적대검수 대체.

## 1. Phase·범위
Ch5 = (Ch3 기반) **충방전 히스테리시스 데이터 해석** — signed current/branch, metastable target, ΔV_obs≠ΔV_hys, q_hys. CHARTER 의 **충전 branch 부호 $s_\phi^b$ 유도장(Phase A HIGH, Ch4 이월 수령)**. 산출 `graphite_ica_ch5_rebuilt.tex`.

## 2. Read Coverage
draft: `consolidated_ch5.tex`+`_body_ch5_v2`+Ch1/Ch3/Ch4 rebuilt+CHARTER+AL_MASTER+DOSSIER 전문. Codex/ 금지.

## 3. G-flow
consolidated_ch5 핵심식(signed coord·charge sign·branch target·hys state·branch kinetics·ΔV decomp·ICA/DVA·full-cell·loop area·branch heat·rest) 보존+무비약. 신설: 충전 부호 유도 §, Ch3→Ch5 keystone 붕괴 소절.

## 4. Grounding / AL
AL-50·51 기등재 + AL-52~59 신규(`RB_AL_MASTER` 등재). DOI 정확 귀속(dreyer=nmat2730, sethna=PhysRevLett, onsager=PhysRev.37, schnakenberg=RevModPhys, degrootmazur=book). 오귀속 0.

## 5. 무비약 재유도
s_φ^chg=−1 logistic 유도, branch target=ξ_ss 항등, ΔV 분리, loop 면적 적분 — 중간단계 전부. 본문 비약어 0.

## 6. 적대검수 (3렌즈)
물리 / 수학 / 정합. **물리·수학 두 agent 독립 CRITICAL 수렴**(정합 agent는 놓침 — 표면 통과만 봄): 충전 η^chg 부호 유도가 자기모순.

## 7. 발견·정정 (1 CRITICAL[물리·수학 수렴] + robust 보강, 삭제 0)
| 등급 | 위치 | 정정 |
|---|---|---|
| **CRITICAL** | verifybox 충전 η^chg 부호 + V_tar^b 정의 | **근본=V_eq^b/V_tar^b 정의에 s_φ^b 누락**(증가형이라 verifybox 추론과 충돌, 수학 agent 수치확인 V_eq^chg>V_drive). 정정: $V_\eq^b=U^b+s_\phi^b w^b\ln[\xi/(1-\xi)]$ (branch logistic 역함수, 충전 ξ-감소형) → η^chg<0 정의에서 닫힘, 음×음=양 정합. verifybox step2 근거화 |
| 보강 | 부호 상쇄 mechanism | "두 인자 동시 뒤집힘"의 robust 근거 = flux $I_j\propto(\xi_\eq^b-\xi_j)$ 와 공액력 η_j^b 의 conjugacy(부호 우연 아님) 명시 |

결론(충전 q_irr≥0 2법칙)은 옳았으나 유도가 거짓 단조성으로 패치돼 있던 것 → 정의 수정으로 진짜 유도화. 미정정: bibitem orphan 7/9(series-wide, 빌드 무해 → Ch7 sweep), eq:ch5_A_branch U_j/U_j^chg 표기(LOW).

## 8. 빌드·무결성
tex **899줄**, PDF **19p** → `Claude/results/graphite_ica_ch5_rebuilt.pdf`. env: equation 29/29, begin/end 53/53. 진짜 undefined ref/cite **0**, overfull **0**, `!` 0.

## 9. CHARTER 준수 (G-cross)
**step1 충전 branch 부호 유도**(s_φ^chg=−1 logistic 유도 + n^eff I_j η^b≥0 부호 상쇄 — 정의 정정 후 진짜 유도) / step2 η 단일 / step3 n^eff 일반형 상속 / **step4 keystone**(branch 비대칭 = Ch3 detailed-balance 극한 붕괴, 동일 입도) / step5 AL-50~59 + DOI 오귀속 0. 정합 agent CHARTER 5규약 "통과" 판정.

## 10. FLAGGED/BOUNDED 잔존
- FLAGGED 0.
- BOUNDED: AL-52·55(metastable)·56·57(이중계상)·58(ΔV 식별성)·59(분리비) — 독립 calorimetry/GITT/rest 검증 전제.

## 11. Next
Phase 6 (Ch6 = 피팅 실무 부록, step 133–146). **5-30 사용자 지시 = 기존 내용 검토 우선 → Gate → 조건부 재유도**. consolidated_ch6(수치 DAE/solver) 검토 + FLAGGED 허위(ε_tol) 점검. main 자동 머지.
