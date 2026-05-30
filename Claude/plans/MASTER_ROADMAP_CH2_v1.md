# Master Roadmap — Chapter 2: 흑연 음극 ICA 의 열·entropy signature (가역/비가역 heat, dV/dT)

**Date**: 2026-05-29
**상위 chain**: Chapter 1 (graphite_ica_chapter1.tex v5.3 merged canonical, ACCEPT) → 본 Chapter 2.
**주제 확정**: 사용자 선택 (2026-05-29) = "열·entropy signature". roadmap_v3 §4 "Out(후속 ch2~):
열 해석(가역/비가역 heat), … dV/dT" 와 정합.
**역할**: Chapter 1 의 effective barrier $\Delta G_\eff=\Delta G_a-\chi\mathcal A$, $\Delta G_a=
\Delta H_a-T\Delta S_a$ 분해와 relaxation-length spectrum 을 \emph{열역학·calorimetry 로 독립
grounding + orthogonal test} 한다. ICA(전기) 와 calorimetry/entropy(열) 의 cross-check 로
kinetic-spectrum 귀속을 보강·반증한다.

---

## §0. 사용자 의도 (절대 기준, Chapter 1 에서 승계)
- 온도·전위에 따른 ICA peak-tail 거동을 grounded·비약 없는 물리로 설명하고 \emph{피팅 가능한
  논리식}을 만든다. 모든 assumption 은 문헌/이론 근거 (없으면 FLAGGED).
- **P1**: 이론 only. solver/numerical-fitting/수치검증 워크플로우 구현은 범위 외.
- smooth only (step-function·$0\!\to\!1$ 급점프·$\max$·$\min$·Heaviside 정의식 금지).
- 한글 prose + 영어 학술 용어. activation barrier 유지.
- Chapter 1 의 notation·AGP grounding tier·Plan-B-core 철학·VG(validation gate) 규약을 그대로 승계.

## §1. Summary
Chapter 2 는 Chapter 1 의 barrier·spectrum 을 \textbf{열역학 1·2법칙과 calorimetry 로 닫는
orthogonal layer} 다. 핵심 논지: (i) 평형 전위의 온도의존 $\partial U_j/\partial T$ 가 \emph{reaction
entropy} $\Delta S_{\mathrm{rxn},j}$ 를 주고(potentiometric entropy, grounded), (ii) 이는 Eyring
prefactor 의 온도의존이 주는 \emph{activation entropy} $\Delta S_a$ 와 \textbf{별개}이며(혼동
금지), (iii) Bernardi energy balance 의 reversible heat $q_\mathrm{rev}=s_\phi I T\,\partial U/\partial T$
와 irreversible heat $q_\mathrm{irr}=I\eta$ 가 ICA 와 독립인 측정 handle 을 준다. (iv) Chapter 1
의 kinetic lag $r=\theta_\eq-\theta$ (tail 의 근원) 는 \emph{entropy production} $\sigma\ge0$ 을
만들어 \textbf{irreversible-heat tail signature} 로 나타난다 — 저온 긴 tail = 큰 lag = 큰 비가역
열의 열적 거울. (v) 따라서 barrier-spectrum 파라미터 ($\Delta H_a,\Delta S_a,U_j(T)$) 는
calorimetry 와 \emph{정합해야} 하며, 불일치 시 kinetic 귀속이 반증된다. deliverable = ICA tail
이론과 cross-check 가능한 \emph{열·entropy 논리식} (peak/tail 의 열적 signature), P1 준수.

## §2. Governing Standard — AGP (Chapter 1 승계)
GROUNDED(established) / BOUNDED(유효범위 병기) / FLAGGED(미검증 hypothesis, established 사용
금지) / GATED(method candidate) / METHOD. 모든 본문 assumption AL-\# 인용. FLAGGED 는 established
로 쓰지 않음. smooth only. solver/numerical-validation 워크플로우 금지(P1).

## §3. Objective & Background
- **Objective**: Chapter 1 의 $\Delta G_\eff$·spectrum 을 열역학적으로 독립 grounding 하고,
  reversible/irreversible heat + $dU/dT$ 로 ICA 귀속의 orthogonal test/falsification 을 구성.
- **Background**: 평형전위 entropy coefficient $\partial U/\partial T$ 와 battery 에너지 balance
  (Bernardi 1985) 는 확립된 이론. 흑연 $\mathrm{Li_xC_6}$ 의 staging-resolved entropy profile 도
  실측 존재(Reynier-Yazami-Fultz). 본 chapter 는 이들을 Chapter 1 의 kinetic·barrier 구조와
  \emph{정합 연결}하되, reaction entropy 와 activation entropy 의 혼동을 명시적으로 차단한다.

## §4. Scope
- **In**: (a) $\partial U_j/\partial T$ = reaction entropy; (b) activation vs reaction entropy
  구분; (c) reversible heat $q_\mathrm{rev}$; (d) irreversible heat $q_\mathrm{irr}=I\eta$ +
  entropy production $\sigma$; (e) kinetic lag → 비가역열 tail signature (Ch1 spectrum 의 열적
  거울); (f) staging-resolved $dU/dT$ profile ↔ Ch1 $N_p$ transitions; (g) ICA–calorimetry
  orthogonal cross-check / falsification.
- **Out(후속)**: 완전 Butler–Volmer 전개, full-cell, 충방전 hysteresis, 수치 solver(P1),
  3D thermal transport/온도장 PDE.

## §5. Inputs (Read 대상)
- `Claude/docs/graphite_ica_chapter1.tex` (v5.3, notation·AL·spine·VG 규약 승계 — 정독).
- `Claude/results/ASSUMPTION_LEDGER_v3.md` (AL-1~10; Ch2 는 AL-11~ 확장).
- 신규 grounding 문헌 (DOI 검증 후 확정): Bernardi-Pawlikowski-Newman 1985(energy balance);
  Thomas-Newman 2003(heats of mixing/entropy in insertion electrodes); Reynier-Yazami-Fultz
  2003(흑연 intercalation entropy/enthalpy); de Groot-Mazur(entropy production, Ch1 기인용);
  Eyring(activation entropy, Ch1 기인용). → DOI 는 Phase 0 에서 web 검증.

## §6. Grounded Spine (Chapter 2, T1–T8)
| ID | 골격 | tier [AL] |
|---|---|---|
| T1 | $\partial U_j/\partial T=\Delta S_{\mathrm{rxn},j}/(s_\phi F)$ (reaction entropy coefficient) | GROUNDED \[AL-11\] |
| T2 | reaction entropy $\Delta S_\mathrm{rxn}$ ≠ activation entropy $\Delta S_a$ (Eyring prefactor) — 혼동 금지 | BOUNDED \[AL-14\] |
| T3 | reversible heat $q_\mathrm{rev}=s_\phi I T\,\partial U/\partial T$ (Bernardi energy balance) | GROUNDED \[AL-12\] |
| T4 | irreversible heat $q_\mathrm{irr}=I\eta$, $\eta=\eta_\mathrm{kin}+\eta_\mathrm{ohm}+\eta_\mathrm{conc}$ | GROUNDED \[AL-12\] |
| T5 | kinetic lag $r$ 의 entropy production $\sigma=\tfrac1T(\text{force})\cdot(\text{flux})\ge0$ → tail 의 비가역열 | BOUNDED \[AL-13\] |
| T6 | staging-resolved $dU/dx$, $dU/dT$ profile ↔ Ch1 $N_p$ effective transitions | GROUNDED \[AL-11\] |
| T7 | barrier-spectrum 파라미터 ↔ calorimetry orthogonal cross-check/falsification | METHOD \[AL-10,15\] |
| T8 | $T/\psi$ 의존: 저온 큰 lag → 큰 비가역열 tail (Ch1 stretched tail 의 열적 거울) | FLAGGED novel \[AL-15\] |

## §7. Chapter 1 과의 정합·강제 연결 (비약 차단)
1. **동일 notation**: $\Delta G_\eff,\Delta H_a,\Delta S_a,\theta_\eq,r,k,L_q,\rho_G,A_L,V_n,
   s_\phi,U_j$ 전부 Ch1 정의 그대로. 신규 기호만 추가 ($S,\,q_\mathrm{rev},q_\mathrm{irr},\eta,\sigma$).
2. **활성 entropy vs 반응 entropy** 는 Ch1 의 $\Delta G_a=\Delta H_a-T\Delta S_a$ (활성) 와
   평형 $\partial U/\partial T$ (반응) 를 구분 — Ch1 이 활성만 다뤘으므로 Ch2 가 반응 entropy 를
   추가하되 \emph{교차 오염 금지}.
3. **tail 의 열적 거울**: Ch1 의 $r(q)=r(q_a)e^{-(q-q_a)/L_q}$ 가 $\sigma\propto k r^2\cdot(\text{thermo
   factor})$ 의 비가역열을 만든다 — 동일 $L_q$·spectrum 이 열 신호를 지배 (FLAGGED novel).
4. **P1·smooth·VG·Plan-B-core** 규약 동일 적용.

## §8. Assumption Ledger 확장 (AL-11 ~ AL-15)
- **AL-11 GROUNDED**: 평형전위 entropy coefficient $\partial U/\partial T=\Delta S_\mathrm{rxn}/(s_\phi F)$
  (potentiometric entropy; Reynier-Yazami-Fultz, Thomas-Newman).
- **AL-12 GROUNDED**: battery 에너지 balance — $q_\mathrm{rev}=s_\phi I T\partial U/\partial T$,
  $q_\mathrm{irr}=I\eta$ (Bernardi-Pawlikowski-Newman 1985).
- **AL-13 BOUNDED**: entropy production $\sigma=\sum J_k X_k/T\ge0$ (linear irreversible
  thermodynamics, near-equilibrium; de Groot-Mazur) — Ch1 AL-5 와 동일 유효범위.
- **AL-14 BOUNDED**: activation entropy $\Delta S_a$(Eyring prefactor $T$-의존) 와 reaction
  entropy $\Delta S_\mathrm{rxn}$($\partial U/\partial T$) 는 별개 — 혼동·상호대입 금지.
- **AL-15 FLAGGED novel**: 저온 long-tail 의 큰 kinetic lag 가 비가역열 tail signature 를 만든다는
  해석 (Ch1 AL-8 의 열적 대응; consistency 로만, 확정은 calorimetry falsification 전제).

## §9. Phase 분해 (cumulative step, Ch1 series 이후 1321– ; 최소 기준점, 유연 확장 가능)
| Phase | step | 내용 | 산출 |
|---|---|---|---|
| CH2-P0 | 1321–1335 | Ch1 v5.3 정독 + grounding 문헌 DOI web 검증 + AL-11~15 확정 | inputs 확정 |
| CH2-P1 | 1336–1360 | §entropy coefficient (T1) + reaction/activation entropy 구분(T2) 유도 | tex §sec:entropy_coeff |
| CH2-P2 | 1361–1385 | §reversible heat (T3) + energy balance grounding | tex §sec:revheat |
| CH2-P3 | 1386–1415 | §irreversible heat + entropy production (T4,T5) | tex §sec:irrheat |
| CH2-P4 | 1416–1440 | §kinetic-lag 의 비가역열 tail signature (T8, Ch1 spectrum 연결) | tex §sec:thermal_tail |
| CH2-P5 | 1441–1465 | §staging-resolved dU/dT (T6) + ICA–calorimetry cross-check/falsification (T7) | tex §sec:cross_check |
| CH2-P6 | 1466–1490 | abstract·notation·spine·summary·bib 통합 + AGP self-check | graphite_ica_chapter2.tex |
| CH2-P7 | 1491–1520 | 10-round 재검 + 결함 수정 + ledger | REVIEW_LEDGER_CH2 |

## §10. Gates (verifiable only)
- G1: 모든 본문 assumption 이 AL-\#(11~15 포함) 인용. (확인 가능)
- G2: reaction entropy 와 activation entropy 가 본문에서 명시적으로 구분·교차오염 없음. (확인 가능)
- G3: $q_\mathrm{rev},q_\mathrm{irr}$ 정의식이 Bernardi balance 와 부호·차원 일치. (확인 가능)
- G4: smooth only — 정의식에 step/max/min/Heaviside 없음. (확인 가능)
- G5: P1 — solver/numerical-validation 워크플로우 없음. (확인 가능)
- G6: notation 이 Ch1 과 충돌 없음(신규 기호만 추가). (확인 가능)
- G7: LaTeX 무결 (eqref/cite/label resolve, 중복 없음, 환경 balanced). (확인 가능)
- G8: 10-round 재검 ACCEPT (잔여 결함 0). (확인 가능)

## §11. Test Plan + Decision Queue + 위험
**Test Plan**: 차원분석(모든 식); Ch1 limiting-case 일치(활성 entropy 가 Ch1 rate 와 정합);
$\sigma\ge0$ 2법칙 만족; entropy coefficient 부호가 staging 방향과 정합. 10-round adversarial.
**Decision Queue (사용자 대기)**: (D1) "JCP 2017" Ch1 출처 미해결 — Ch2 무관하나 bib 일관성
참고. (D2) Ch2 deliverable 을 별도 .tex 로 둘지(graphite_ica_chapter2.tex) — 기본 그렇게 진행.
**위험**: (R1) reaction/activation entropy 혼동(가장 흔한 오류) → AL-14 로 차단. (R2) reversible
heat 부호 convention($s_\phi$) → Ch1 과 통일. (R3) 비가역열 tail signature 의 overclaim →
FLAGGED+falsification 전제. (R4) DOI 환각 → Phase 0 web 검증.

## §12. Correction History
- v1 (2026-05-29): 최초 작성. 주제=열·entropy(사용자 확정). Ch1 v5.3 승계. AL-11~15 신설.
