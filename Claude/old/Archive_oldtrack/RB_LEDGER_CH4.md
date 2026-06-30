# RB_LEDGER_CH4 — Chapter 4 재구성 Result (Phase 4, step 89–110)

> 자율 진행(사용자 위임). Ch1 방식. Decision Gate → 3렌즈 적대검수 대체.

## 1. Phase·범위
Ch4 = (Ch3 이용) **전지 가역/비가역 발열의 entropy-production 기반 일반화** — Ch3 forward/backward $r^\pm$ → transition-level entropy production → 거시 $\sum_j n_j^\eff I_j\eta_j$. CHARTER 의 **η 이중정의 해소장(Phase A CRITICAL)·s_φ verifybox 복원장·n^eff 일반형장**. 산출 `graphite_ica_ch4_rebuilt.tex`.

## 2. Read Coverage
draft: `consolidated_ch4.tex`(골격)+`_body_ch4_v2`+Ch1/Ch2/Ch3 rebuilt+CHARTER+AL_MASTER+DOSSIER 전문. Codex/ 금지.

## 3. G-flow
consolidated_ch4 핵심식(fluxforce·tr_entropy·micro_macro·rev_OCV·transition entropy·consistency·bg split·transport·rest relaxation) 보존+무비약. 신규: 부호보조정리 3-case 증명, 미시=거시 5단계 분해, Bernardi=미시 reaction entropy 합 verifybox.

## 4. Grounding / AL
AL-40·41 기등재 + AL-42~49 신규(`RB_AL_MASTER` 등재). **DOI 정확 귀속**(degrootmazur/prigogine=book, onsager=PhysRev, schnakenberg=RevModPhys — Ch3 오귀속 교훈 계승, 재발 0).

## 5. 무비약 재유도
$(x-y)\ln(x/y)\ge0$ 보조정리, 미시=거시 5단계, extensivation 다리(k_B→R·½부재·mol인자), Bernardi $s_\phi$ 상쇄 — 중간단계 전부. 본문 비약어 0.

## 6. 적대검수 (3렌즈)
물리·열역학 / 수학·무생략 / 정합·CHARTER·DOI. **CRITICAL(식 자체 틀림) 0**(수학 agent sympy로 5단계+부호보조정리 전건 잔차 0; 정합 agent CHARTER 5규약·DOI 전건 통과·오귀속 0 확인). 발견은 전부 "결과 정확하나 전제·다리 미명시" 유형.

## 7. 발견·정정 (4 HIGH + 2 MED, 삭제 0)
| 등급 | 위치 | 정정 |
|---|---|---|
| HIGH | verifybox 2단계 | micro=macro detailed balance 대입이 **C_j≡0(r±비 ξ_j-무관, 대칭 split, Ch3 keystone 조건)** 전제 필요 명시. AL-44 tier 조건부화 |
| HIGH | eq:ch4_tr_entropy | extensivation 다리(per-site $k_B$→per-mole $R$, ½부재=단일 directed edge, site수=$N_A(Q/F)$) 4줄 보강. AL-41 ½ 불일치 해소 |
| HIGH | eq:ch4_affinity_eta | s_φ 복원이 1~3단계 대수에 없음(사후부착) → boxed 일반 s_φ는 Ch3 표기 일관용, 충전 branch 유도 Ch5 이월, 본 장 s_φ=+1 한정 명시 |
| HIGH | 휴지 ≥0 근거 | "전류 보존"이 아니라 "공통 무대 V_n 공유 → 항별 동부호"로 정정(전류 보존은 별개 진술) |
| MED | eq:ch4_consistency | 좌변 평형미분 vs 우변 dξ_j/dt = 준평형 극한 한정 명시 |
| MED | AL_MASTER AL-41/44 | ½ per-transition 명시 / AL-44 C_j≡0+V_drive=V_n 전제 등재 |

미정정(사유): dead bibitem `thomasnewman2003`(Ch4 미인용) + orphan bibitem(bazant2013/newman/bardfaulkner AL표 plaintext) = 빌드 무해. **Ch7 통합서 bibitem-cite sweep 권고**(정합 agent 권고).

## 8. 빌드·무결성
tex **929줄**, PDF **19p** → `Claude/results/graphite_ica_ch4_rebuilt.pdf`. env: equation 29/29, begin/end 53/53. 진짜 undefined ref/cite **0**, overfull **0**, `!` 0.

## 9. CHARTER 준수 (G-cross)
**step1 s_φ verifybox 복원**(eq:ch4_affinity_eta, s_φ=+1 한정 명시) / **step2 η 단일정의 — Phase A CRITICAL 진짜 해소**(V_n/V_drive 혼용 0, 기본형 V_drive=V_n 명시) / **step3 n^eff 일반형**(Σn^eff I_jη_j boxed + Ch2 특수형 양방향 정합) / step4 keystone 상속 / step5 AL-40~49 + DOI 오귀속 0. 3렌즈 정합 agent 각 "통과".

## 10. FLAGGED/BOUNDED 잔존
- FLAGGED: AL-48 가역/비가역 정량 분리비(독립 calorimetry 검증 전제).
- BOUNDED: AL-44(C_j≡0+V_drive=V_n 전제)·AL-46(3→4분해)·AL-47(transport/저항)·AL-49(domain guard).

## 11. Next
Phase 5 (Ch5 = Ch3 기반 충방전 히스테리시스, step 111–132). Ch5에서 충전 branch $s_\phi^b$ 부호 유도(Ch4가 이월), metastable target, $\Delta V_\obs\ne\Delta V_\hys$, $q_\hys$. main 자동 머지.
