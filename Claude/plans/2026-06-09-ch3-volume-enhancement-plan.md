# Chapter 3 (발열) 볼륨 보강 계획 — 교과서 깊이 · 절 단위 루프 · 최대 effort

## Summary
Ch3(현재 8p)을 Ch1(24p)$\cdot$Ch2(11p) 수준의 \emph{교과서 깊이}로 보강. 각 절에 \textbf{직관(physical picture) → 전 단계 유도 → worked example → 물리 해석}을 충실히 채운다 — \emph{패딩$\cdot$동어반복 금지, 진짜 물리만}. 핵심 보강: §2 비가역 열역학(엔트로피 생성)·§3 삽입 엔트로피 부호 물리·§4 히스 소산 전 유도·§5 과전압 3분해·§7 lumped 타당성(Biot)·§8 선형 안정성·§11 전 방전 $T(t)$ worked example. 방식 = 누적 피드백 그대로: 절 단위 루프(절마다 빌드·Ch1/Ch2 정합)·최대 effort·NO Workflow·단일문건 규율·master 직접 손검·Codex 적대검수·result/ledger·auto-commit. 정확성 확인된 식·인계 번호 보존, 추가만.

## Current Ground Truth
- `graphite_ica_ch3.tex` 8p, 완료·Codex 검증(커밋 `d695077`). master 식 $Q_\gen=q_\rev+q_\hys+q_\pol$ + 열 수지 확정.
- 절: 서론·§1 기호·§2 Bernardi 배경·§3 가역열·§4 히스 소산열·§5 분극열·§6 전이별·§7 열수지·§8 되먹임·§9/§10 파라미터·§11 종합식.
- 인계(보존): Ch1 1.3/1.15/1.17/1.19, Ch2 2.5/2.10/2.14. 신규 열 $\{C_\Th=mc_p,hA_s\}$.
- 이전 ledger `PHASE_CH3_EXECUTION_LEDGER.md` Next=done(3.12). 본 보강 plan = Phase 3.13~, cumulative step 45부터.

## Phase Range
| Phase | 이름 | Steps | 절 | 핵심 보강 |
|---|---|---:|---|---|
| 3.13 | §서론·§1 보강 | 45–46 | 서론·기호 | 발열 큰 그림(왜 중요·세 갈래 직관) |
| 3.14 | §2 배경 심화 | 47–51 | bg | 1법칙 제어부피·엔트로피 생성 σ≥0·De Donder·세 갈래 검산 |
| 3.15 | §3 가역열 심화 | 52–56 | rev | 삽입 엔트로피(배열+진동)·staging ∂U/∂T 부호 물리·전이별 프로파일·worked |
| 3.16 | §4 히스 소산열 심화 | 57–62 | hys | loop=비가역일 전 유도·spinodal 상한 vs nucleation·다입자 평활·T 의존·worked ★ |
| 3.17 | §5 분극열 심화 | 63–67 | pol | 과전압 3분해(ohmic·η_ct·확산)·Joule·완화 소산 유도·worked |
| 3.18 | §6 전이별 심화 | 68–70 | perpeak | 열량 ICA(dQ_heat/dV)·entropy ICA |
| 3.19 | §7 열수지 심화 | 71–75 | balance | lumped 타당성(Biot)·전 transient 해·다펄스·극한 |
| 3.20 | §8 되먹임 심화 | 76–79 | feedback | 선형 안정성(dQ_gen/dT<hA_s)·고정점·runaway 조건 |
| 3.21 | §9/§10 심화 | 80–83 | param/fit | 열량계법(ARC·IMC·potentiometric entropy)·식별 순서·예측 검증 |
| 3.22 | §11 master worked | 84–87 | master | 전 방전 Q_gen(SOC)·T(t) 종합 worked example |
| 3.23 | 빌드·Codex·커밋 | 88–90 | 전체 | 2-pass 0/0·인계 대조·Codex·커밋 |

## Non-goals
- 패딩$\cdot$동어반복$\cdot$disclaimer 적층 금지 — 교과서 prose(직관·유도·예제·해석)로만 볼륨.
- 확정 식(master·Bernardi·q_hys·열수지)·인계 번호 변경 금지(보강만 add).
- 발명 금지(임의 모델 X). DFN 공간 분해 금지(lumped; Biot은 \emph{타당성 판정}만, 분해 X).
- 단일문건 규율(Chapter-N 0·인계/전달/결론 절 0). Ch4 의존 X. 챕터 통째 배치 작성 금지. NO Workflow.

## Implementation Changes
- 수정: `graphite_ica_ch3.tex`(절별 add). 빌드 `graphite_ica_ch3.pdf`.
- Result: `PHASE_CH3_RESULT.md`(보강 누적). Ledger: 기존 `PHASE_CH3_EXECUTION_LEDGER.md` 에 Phase 3.13~ 행.

## Phase 3.13 — §서론·§1 보강
- **Steps 45–46.** 서론에 발열의 \emph{큰 그림}(왜 발열이 ICA·수명·안전에 중요한가; 세 갈래를 한 문장 직관으로). §1에 필요한 신규 기호(σ 엔트로피 생성, Bi Biot 등) 추가.
- **Gate G3.13:** 큰 그림 문단·신규 기호 존재, Chapter-N 0, 빌드 clean.

## Phase 3.14 — §2 배경 심화
- **Steps 47–51.** 제어부피 1법칙 전개(전기일·화학에너지·열 항 명시), \emph{엔트로피 생성} $\dot\sigma=q_\irr/T\ge0$(2법칙)로 비가역열의 부호 보장, De Donder(친화도·flux)로 $q_\irr=I\eta\ge0$ 재확인, 세 갈래 분해 검산(차원·극한). worked: 단위 전하당 각 항 mV 규모 비교 표.
- **Gate G3.14:** σ≥0·De Donder·세 갈래 검산·비교표 존재, 부호 손검, 빌드 clean.

## Phase 3.15 — §3 가역열 심화
- **Steps 52–56.** 삽입 엔트로피의 두 출처(배열 엔트로피 $-R[\theta\ln\theta+\dots]$·진동/전자 엔트로피), staging 전이서 $\partial U_j/\partial T$ 가 \emph{왜 부호를 바꾸는지}(질서화 peak), 전이별 $\Delta S_j$ 프로파일, 충/방전 발열↔흡열 대칭, fuller worked(흑연 ∂U/∂T 대표 프로파일→발열 곡선). \cite{reynier2004}.
- **Gate G3.15:** 엔트로피 출처·부호 물리·전이별·worked 손검, Ch1 1.15 정합, 빌드 clean.

## Phase 3.16 — §4 히스 소산열 심화 (핵심)
- **Steps 57–62.** loop 면적 $=$ 비가역일 전 유도(준정적 비가역 cycle), spinodal 상한($\gamma=1$) vs nucleation 축소($\gamma<1$)의 발열 의미, 다입자 평활화가 발열 분포에 주는 효과(Dreyer), $\Delta U_j^\hys(T)$ 가 $T_c$서 0 되는 자기제한 정량, 분극과 분리(저율 외삽) 정량, worked(여러 $\Omega_j,\gamma_j$).
- **Gate G3.16:** loop=비가역일 유도·γ 의미·다입자·T 의존·worked 손검, Ch2 2.10/2.14 정합, 빌드 clean.

## Phase 3.17 — §5 분극열 심화
- **Steps 63–67.** 과전압 3분해 — ohmic $I^2R_\ohm$·전하전달 $\eta_\mathrm{ct}I$(소전류 $(RT/F)I/i_0$)·확산(농도) 과전압, 각 Joule/활성 발열, 완화 지연 소산을 Ch1 $L_{q,j}$(1.19)에서 닫힌 형으로, 율 의존($\propto|I|^2$ vs $|I|$) 구분, worked.
- **Gate G3.17:** 3분해·완화 소산 유도·율 의존·worked 손검, Ch1 1.3/1.19 정합, 빌드 clean.

## Phase 3.18 — §6 전이별 심화
- **Steps 68–70.** 열량 기반 ICA: $\dd Q_\mathrm{heat}/\dd V$ 가 $\dd Q/\dd V$ peak·가역열 골을 보임, entropy ICA(전위 온도계수의 SOC 곡선)로 전이 구조 역독.
- **Gate G3.18:** 열량 ICA·entropy ICA 서술·정합, 빌드 clean.

## Phase 3.19 — §7 열수지 심화
- **Steps 71–75.** lumped 타당성: Biot 수 $Bi=hL/k_\Th\ll1$ 면 내부 균일(분해 불요), 그 조건 명시. 시변 $Q_\gen(t)$ 의 전 transient 해(적분), 다펄스/cycle 누적 승온, 등온/단열/정상 극한 상세, worked(0.2C·5C 비교).
- **Gate G3.19:** Biot 타당성·전 해·극한·worked 손검, 빌드 clean.

## Phase 3.20 — §8 되먹임 심화
- **Steps 76–79.** 선형 안정성: 고정점 $T^\ast$ 둘레 $\dd Q_\gen/\dd T<hA_s$ 면 안정(음의 되먹임), $>$ 면 runaway. 본 장 항들은 $\dd Q_\gen/\dd T<0$(히스↓·k↑)라 안정. 양의 되먹임원(Arrhenius 부반응 $\propto e^{-E_a/RT}$) 더하면 임계 $T$서 runaway 판정식. 자기일관 고정점.
- **Gate G3.20:** 선형 안정성 조건·runaway 판정·고정점 손검, 빌드 clean.

## Phase 3.21 — §9/§10 심화
- **Steps 80–83.** 열량계법 상세: ARC(단열)·IMC(등온 microcalorimetry)·potentiometric entropy(∂U/∂T 직접). $C_\Th,hA_s$ 식별 절차(펄스 transient 회귀), 예측 검증(외삽 조건 calorimetry 대조).
- **Gate G3.21:** 측정법·식별·검증 서술·정합, 빌드 clean.

## Phase 3.22 — §11 master worked example
- **Steps 84–87.** 전 방전 한 번의 종합 worked: 대표 파라미터로 $Q_\gen(\mathrm{SOC})$(세 갈래 SOC 프로파일)·$T(t)$(열수지 적분) 산출, 관측 규모(수십 mV/charge, 수 K) 대조. master 식 환원검산 재확인.
- **Gate G3.22:** 종합 worked 수치·SOC·T(t)·환원검산 손검, 빌드 clean.

## Phase 3.23 — 빌드·Codex·커밋
- **Steps 88–90.** 2-pass overfull 0·undefined 0; 인계 .aux 재대조; Codex foreground(보강 물리·유도·수치, MAJOR 0, Ch1/Ch2 대조); result+ledger; ch3 tex+pdf 커밋·푸쉬.
- **Gate G3.23:** 빌드 0/0, Codex MAJOR 0(시정 후), 인계 대조, git 해시. 목표 $\ge16$p.

## Implementation Interfaces
- 보강 prose = (물리 직관 → 전 단계 유도 → worked example → 해석). 별행 수식, 인라인 cramming 금지.
- 신규 식 손검(부호·차원·극한). worked = 대표 수치(규모 예시, 실측 아님 명시).
- Result 11항목·Ledger 12-col.

## Test Plan
- 빌드 2-pass: overfull 0·undefined 0, 페이지 수(목표 ≥16p).
- 추가식·worked 수치 손검. 인계 번호 .aux 재대조. 단일문건 규율 grep. Codex foreground 1회.

## Assumptions
- A1: 보강은 깊이$\cdot$예제$\cdot$배경 — 물리가 요구하는 만큼(인위 분량 X).
- A2: lumped 유지(Biot는 타당성 판정만, 공간 분해 X).
- A3: worked 대표값 규모 예시 명시.

## Correction History
- 2026-06-09 v1: 작성. 박사님 "볼륨 보강 필요, 계획서+절별 루프". Ch3 8p→교과서 깊이(≥16p 목표). PHASE_CH3 이어 Phase 3.13~, step 45부터. 확정 식·인계 보존, 깊이만 add. GO 시 3.13부터 마지막까지 절 단위 연속.
