# Review Ledger: graphite_ica_chapter2.tex — 10-round 재검

**Date**: 2026-05-29
**대상**: `Claude/docs/graphite_ica_chapter2.tex` (Chapter 2 v1, ~410 lines)
**주제**: 열·entropy signature (reaction-entropy 계수 $\partial U/\partial T$, 가역/비가역 heat,
kinetic-lag entropy production) — Chapter 1 의 orthogonal thermal grounding/falsification.
**계획서**: `Claude/plans/MASTER_ROADMAP_CH2_v1.md` (11-section, T1–T8 spine, AL-11~15+16).
**맥락**: 사용자 "챕터2 계획서 및 작성 그리고 10회 검수 ㄱㄱ". 주제는 사용자 선택(열·entropy).
**방식**: 독립 적대 검수 sub-agent 다중 렌즈 (전수 정독) + 자체 재유도 + grounding DOI web 검증.

---

## Phase 0: grounding DOI web 검증 (환각 방지, 사용자 "검색 우선")
- Bernardi-Pawlikowski-Newman 1985, J. Electrochem. Soc. 132(1):5 → **10.1149/1.2113792** (확인).
- Reynier-Yazami-Fultz 2003, J. Power Sources 119-121:850 → **10.1016/S0378-7753(03)00285-4** (확인).
- Thomas-Newman 2003, J. Power Sources 119-121:844 → **10.1016/S0378-7753(03)00283-0** (PII 확인).
- Eyring/de Groot-Mazur/Onsager/Bazant = Chapter 1 기인용(검증됨).

## 핵심 grounded 결과 (novel)
**비가역열 tail 은 ICA tail 과 \emph{같은} relaxation-length spectrum $\{L_q\}$ 를 공유하되,
entropy production $\sigma\propto r^2$ 때문에 decay length 가 $L_q/2$ — 즉 2배 빠르게 감쇠.**
→ ICA(전기) 와 calorimetry(열) 의 \emph{무료(파라미터 없는) orthogonal cross-check} (TN2).
reaction entropy($\partial U/\partial T$) ≠ activation entropy(Eyring prefactor) 명시 구분.

## 10 라운드 기록
| R | 렌즈 / 작업 | 방법 | 결과 |
|---|---|---|---|
| 1 | 물리·차원 정합 | adversarial agent + 자체 재유도 | **SOUND**. E1~E6 전부 독립 재유도 통과; ★factor-of-2 (열 tail $L_q/2$) 정확 확인. 결함 2(MEDIUM: per-transition current·per-mode/절대 W 단위), LOW 2. |
| 2 | LaTeX 무결성 | adversarial agent | **컴파일 clean**. ref/cite/label resolve, 중복 0, 환경 balanced, longtable 열수 OK. 단 eyring1935 bibitem 미인용(무해 nit). |
| 3 | P1·smooth·Ch1 notation 정합 | adversarial agent (Ch1 대조) | **PASS**. solver/step/max 없음; notation 충돌 0(신규 기호만); reaction/activation entropy 구분 exemplary. LOW 2(η_kin↔η_ct 명명, AL-10 재진술). |
| 4 | grounding·citations·DOI | adversarial agent | **PASS**. 6 DOI 전부 정확; tier 일관; AL-15 FLAGGED 적정. 결함 1(MEDIUM: g'' 에 AL 부재), LOW 1(thomasnewman2003 과잉귀속). |
| 5 | 내부 정합·논리·Ch1 link | adversarial agent | **PASS**. cross-section 일치, 논리 chain 무결, TN1–TN4 falsifiable, Ch1 link 정확. (Θ_tail vs θ = 의도된 aggregate/single 구분, 비결함.) |
| 6 | 수정 적용 | Edit | 7건: (1)eyring1935 인용; (2)E1→reynier2003만; (3)partial-current 주석; (4)η_kin↔η_ct; (5)AL-16 GROUNDED(g'') 신설+E5/T5 태그; (6)per-mode 단위 주석+TN2=형태검증; (7)AL-10 승계 명시. |
| 7 | 수정 검증 | 자체 read/grep | eyring1935 인용·AL-16 정의/사용·인용 비고아 확인 (grep tool 불안정 → read 로 보강). |
| 8–10 | 최종 종합 sign-off | adversarial agent (전수 재독) | **ACCEPT**. 7 수정 정확·회귀 0; LaTeX clean(7 bibitem 전부 인용, AL ledger 6행 AL-11~16 열수 OK); 물리 intact(factor-of-2 유지); P1/smooth/AL/FLAGGED/notation 준수. **잔여 결함 0.** |

## 발견·수정 요약 (전부 반영)
1. per-transition current 명확화 (R1) — $I\to I_j$ partial current 합산. ✅
2. per-mode molar vs 절대 W 단위 + TN2 는 \emph{형태} 검증 명시 (R1). ✅
3. eyring1935 인용 추가 (R2). ✅
4. η_kin = Ch1 η_ct 교차 주석 (R3). ✅
5. AL-10 승계 명시 (R3/R5). ✅
6. g'' GROUNDED 근거 → AL-16 신설 + 태그 (R4). ✅
7. thomasnewman2003 과잉귀속 → E1 은 reynier2003 만 (R4). ✅

비결함(검토 후 미수정): single_kernel↔kernel_integral "same spectrum support vs shape"(본문 이미
정확), Θ_tail(aggregate) vs θ(single-mode) 구분(의도적).

## 최종 상태
**Chapter 2 v1 = 10-round 재검 ACCEPT (잔여 결함 0).** 물리 SOUND(factor-of-2 핵심결과 독립검증) ·
LaTeX 컴파일 clean · P1/smooth/grounding 준수 · Ch1 notation 정합 · 6 DOI web 검증 · reaction vs
activation entropy 엄격 구분.

## 후속 (Chapter 3 후보, Ch2 §summary 전달)
staging-resolved $\partial U/\partial x$ 정량 모델; ICA tail + 비가역열 tail 동시 fitting
(cross-modal identifiability); 충방전 hysteresis 의 heat/entropy 비대칭; full-cell 열 balance.
"JCP 2017" Ch1 출처 미해결은 Ch2 와 무관(별건).
