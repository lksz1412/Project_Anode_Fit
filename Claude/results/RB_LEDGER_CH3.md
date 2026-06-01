# RB_LEDGER_CH3 — Chapter 3 재구성 Result (Phase 3, step 63–88)

> 자율 진행(사용자 위임). Ch1 방식. Decision Gate → 3렌즈 적대검수 대체. 계획서 Phase 3, 규약 RB_CHARTER, AL RB_AL_MASTER.

## 1. Phase·범위
Ch3 = (Ch1 기반) **전기화학 반응속도론 일반화** — Level A(mobility, 방향성 X) → Level B(forward/backward $r^\pm$, $\chi=\beta$, 방향성 O) zoom-in. CHARTER 의 **s_φ 명시형 기준장 + V_drive 정의장 + n^eff 정의장 + keystone 한정장**. 산출 `graphite_ica_ch3_rebuilt.tex`.

## 2. Read Coverage
draft 에이전트: `consolidated_ch3.tex`(골격) + `_body_ch3_v2.tex` + Ch1/Ch2 rebuilt(상속·스타일) + CHARTER + AL_MASTER + DOSSIER 전문 정독. Codex/ 금지 준수(원본 무수정).

## 3. G-flow
consolidated_ch3 핵심식(fb·db_width·recover·xiss·ratio_B·ksum·neff·verifybox·bv·rct·forward_limiter·current·Rn·crate·T) 전부 보존+무비약 재유도. 신규: BV small-signal 1차 Taylor→R_ct 유도(골격엔 없던 무비약). dangling AL-K1~K3 → AL-30~32 실제 정의.

## 4. Grounding / AL
AL-30·31 기등재 확정 + AL-32~39 신규(`RB_AL_MASTER` 등재). FLAGGED 0(전부 GROUNDED/BOUNDED — 반응속도론·BV·전하보존 확립). 무태그 established 0.

## 5. 무비약 재유도
detailed balance odds 대입, Level B β 상쇄($\beta+(1-\beta)=1$), n^eff 2-조건 정합, ξ_ss→ξ_eq 극한, Level A 복원($-\xi_\eq\xi_j$ 상쇄), BV Taylor→R_ct — 중간단계 전부. 본문 비약어 0(정밀 scan: 헤더 주석·검수표만).

## 6. 적대검수 (3렌즈)
물리·반응속도론 / 수학·무생략 / 정합·CHARTER. **CRITICAL 0**(양측 sympy keystone 항등식 전수 교차검증 일치). CHARTER 5규약 준수, Ch1↔Ch3·Ch2↔Ch3 정합 clean, 차원 정합(ρ_G/σ_j류 재발 0).

## 7. 발견·정정 (2 HIGH + 1 MED, 삭제 0)
| 등급 | 위치 | 정정 |
|---|---|---|
| HIGH | verifybox keystone | Level A=Level B 극한($\xi_\ss\to\xi_\eq$) 닫힘이 detailed balance \emph{만}이 아니라 **r±비의 $\xi_j$-무관(대칭 split)**도 필요 명시(Ch1 keystone "r± ξ-무관 국소상수" 정정과 동일 입도). line 462 branch 비대칭 조건에 "$r^+/r^-$ $\xi_j$-의존" 추가 |
| HIGH | AL-30·35 DOI 오귀속 | Onsager DOI(10.1103/PhysRev.37.405)가 DOI 없는 단행본 degrootmazur1962에 부착됨 → onsager1931에 귀속, degrootmazur=book 표기(dossier svare/macdonald 오귀속 유형 재발 차단) |
| MED | forward_limiter | 기본형(DB 보존)은 병목을 mobility/net에 대칭 적용; forward-only 식은 Ch5 강구동 비대칭용 template(기본값 아님) 명시 |

미정정(사유): orphan bibitem(onsager/doyle/fly2020) = 빌드 무해 + AL표 plaintext 양식 일관(LOW); C_j≡0 명시 = keystone 정정에 흡수.

## 8. 빌드·무결성
tex **834줄**, PDF **18p** → `Claude/results/graphite_ica_ch3_rebuilt.pdf`. env: equation 28/28, begin/end 53/53. 진짜 undefined ref/cite **0**, overfull **0**(draft서 22→0 해소), `!` 0.

## 9. CHARTER 준수 (G-cross)
step1 s_φ 명시형 기준(eq:ch3_Aj) / step2 V_drive=V_n+η_drive 정의, η_n≠η_drive≠V_app 3구분(AL-32) / step3 n^eff=RT/(Fw_j) 정의 + Ch2특수형/Ch4일반형 위계 / **step4 keystone 한정장: ξ_ss→ξ_eq 한정·χ=β·Level A/B 방향성 구분, Ch1 동일 입도(닫힘조건 보강)** / step5 AL-30~39 단일번호. 3렌즈 정합 에이전트 각 "준수" 판정.

## 10. FLAGGED/BOUNDED 잔존
- FLAGGED 0.
- BOUNDED: AL-32(전위 동일시)·AL-33(Marcus 곡률)·AL-34(partition+keystone ξ_j-무관 닫힘조건)·AL-35(비대칭 병목)·AL-36(double-counting)·AL-38(식별성)·AL-39(상관 chain).

## 11. Next
Phase 4 (Ch4 = Ch3 기반 전지 가역 반응열, step 89–110). Ch3의 forward/backward + entropy production → 거시 $\sum n^\eff I_j\eta_j$ 정합, Ch2 강구동 q_irr 일반형 양정치 닫음. main 자동 머지.
