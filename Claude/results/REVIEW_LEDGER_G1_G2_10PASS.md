# 10-Pass 논리 검토 Ledger — 합류 G1(Ch1) + G2(Ch2~4)

**대상**: `Claude/docs/graphite_ica_consolidated_ch1_G1.tex`, `..._ch2_ch4_G2.tex`
**원칙**: 10회 = 서로 다른 중점 관점, **논리 검증 위주**, 필요시 논문 검색 보완(GS-1~4 기준).
**일자**: 2026-05-29 · 사용자 지시: "진행 결과 검토 10회, 관점 달리, 논리 검증 위주, 필요시 논문 검색 보완."
**심각도**: CRIT(피팅 전 필수) / HIGH / MED / LOW(표현·명료) / PASS(무결).

---

## 검색 보완(논문) 요약
- **S1 (entropy production 형식)**: Schnakenberg network theory — CRN entropy production = $\sum$(reaction current)$\times$(affinity) $\ge0$, master equation 의 비가역성. → `eq:ch4_trep` 의 $(\mathcal J^+-\mathcal J^-)\ln(\mathcal J^+/\mathcal J^-)$ 형 grounding 확정. [Schnakenberg, Rev. Mod. Phys. 48, 571 (1976)]
- **S2 (stretched tail 메커니즘)**: 고정 activation-energy 분포 → \emph{T-의존} stretched 완화가 disordered/fast-ion-conductor kinetics 에 \emph{확립}. → AL-8 의 "novel·선행모델 부재"는 과대. [Macdonald, PRB 61, 228 (2000); Lindsey--Patterson, JCP 73, 3348 (1980); Plonka, JPCB 102, 5835 (1998)]

---

## Round 별 결과 (관점 달리)

### R1 — 차원/단위 정합
- 점검: $\mathcal A_j$=J/mol, $\chi\mathcal A$=J/mol, $\Delta G/RT$ 무차원, $L=|I|/(Q_\cell k)$ 무차원,
  $A_L=\rho_G(RT/L)A_0$, kernel integral, `eq:fiteq` $Q_p\,d\Theta/dQ$ 무차원, `eq:ch4_trep`=W.
- 결과: **PASS**. (LOW 명료화: $q$-좌표서 $L$ 무차원이라 $A_L$ 도 무차원 — 본문에 density 의미 명시되어 있음.)

### R2 — 논리 비약(GS-1) 단계 추적
- 점검: G1 keystone 2-state chain(net rate→정상점→선형화→$k=r^++r^-$); G2 §reconcile 항등식;
  Ch4 $(x-y)\ln(x/y)\ge0$.
- 결과: **PASS**. (LOW: $G$ vs $\Delta G_{a,j}$ 표기 — notation 표서 $G$=분포 barrier, $\Delta G_{a,j}$=mode 값으로 이미 구분.)

### R3 — ★keystone / detailed-balance 정합 (중점)
- **발견 R3-1 (HIGH)**: G2 Level B 의 affinity $\mathcal A_j=F(V-U)$ 가 평형형태(width $w_j$)의 detailed
  balance $r^+/r^-=\exp[(V-U)/w_j]$ 와 정합하려면 \emph{구동 척도}가 같아야 함 → \textbf{$w_j=RT/F$(ideal)
  에서만} 성립. effective $w_j\ne RT/F$ 면 비에 들어가는 것은 \textbf{thermodynamic affinity}
  $\mathcal A_j^{\mathrm{th}}=RT(V-U)/w_j$. 기존 "$\Pi_j^0=\exp[-\mathcal A_j^0/RT]$" 문장은 모호.
- **조치**: G2 §ch3\_levelB 에 `eq:ch3_dbconsist` 신설 + 정합 조건 명시; $\chi_j=\beta_j$ 가 \emph{동일
  thermodynamic 구동} $\mathcal A_j^{\mathrm{th}}$ 에 작용, $\Pi_j^0=1$ 이 intrinsic barrier 를 묶음(자유
  파라미터 아님)으로 수정. → keystone 정합 강화. **해소.**

### R4 — grounding(GS-3) + 논문 검색
- **발견 R4-1 (MED)**: `eq:ch4_trep` 무인용. → **조치**: Schnakenberg 1976 인용 추가(S1).
- **발견 R4-2 (MED, 정직성)**: AL-8 "FLAGGED novel, 선행모델 부재" 과대. → **조치**: G1 §tailT 에 메커니즘
  grounding(Macdonald PRB 61,228; Lindsey--Patterson JCP 73,3348; Plonka JPCB) 추가, "novel"→
  "BOUNDED: 메커니즘 grounded, graphite ICA tail 적용이 기여"로 정정 + bib 3건 추가(S2).
- 결과: 위 2건 반영 후 **PASS**.

### R5 — self-consistency / 순환 의존(P3-3/4)
- **발견 R5-2 (LOW)**: `eq:fiteq` 의 $d\Theta/dQ$(전체)와 엔진의 $d\Theta_\mathrm{tail}/dq$ 연결 미명시;
  $\rho_G$ 모수형 미지정; $1-Q_p d\Theta/dQ>0$ 조건. → **조치**: G1 §fiteq 에 좌표 bridge
  ($d\Theta/dQ=(1/Q_\cell)d\Theta/dq$, post-peak $\simeq d\Theta_\mathrm{tail}/dq$) + $\rho_G$ 모수형 +
  단조성 동치 명시.
- Volterra→Fredholm(Plan A)·broad-kernel 열화 caveat: 이미 G1 §closure 에 존재 → **PASS**.

### R6 — 부호 convention
- 점검: $s_{\phi,j}$($\mathcal A_j>0$⇒방전 촉진), $s_I$, $\partial\ln L/\partial V_\drive=-\chi s_\phi F/RT<0$
  (forward: $V\uparrow⇒k\uparrow⇒L\downarrow$ ✓), entropy production $\ge0$.
- 결과: **PASS**.

### R7 — 극한/점근
- **발견 R7-1 (LOW)**: 빠른 kinetics 극한($k\to\infty$, $L\to0$) 및 single-mode 복귀(M4) 미명시.
  → **조치**: G1 §fiteq 에 극한 점검 추가 — $d\Theta_\mathrm{tail}/dq\to d\Theta_\eq/dq$ (singular
  perturbation; $\delta$-함수 아님), $A_L=\delta(L-L_0)$ 서 single-mode 복귀(M4).
- $\beta\to0/1$, $\mathcal A_j\to0$(Level A=B 일치) 점검: 정합 → **PASS**.

### R8 — 관찰 anchor(N-1) + 피팅식(N-2) 사용성
- 점검: G1 서·G2 anchorbox 로 관찰 연결; `eq:fiteq` + 평가순서 S1--S6.
- 결과: **PASS** (R5-2 의 $\rho_G$ 모수형 보강으로 사용성 향상).

### R9 — 장간 전달(P3-6) + 표기
- **발견 R9-1 (LOW)**: G1 이 $\Theta$(전체 progress)와 $\xi_j$(transition별)의 관계를 미정의 — kernel
  integral($\Theta$)와 charge balance($\xi_j$)가 끊김. → **조치**: G1 §charge 에
  $Q_p\Theta\equiv\sum_j Q_{j,\tot}\xi_j$ 정의 추가.
- $\theta\!\leftrightarrow\!\xi$, ver$\!\leftrightarrow\!$Chapter 매핑: G1 §notation 존재 → **PASS**.

### R10 — 과도가정(GS-4) + falsification 완결
- 점검: cap/clip/softplus/step 정의식 0(양 파일 명시); log floor=domain guard; Marcus bound 병기;
  Plan A broad-kernel 열화 caveat; falsification N1--N4 + $\chi$ vs $\eta_\ct$ co-linearity.
- 결과: **PASS**. (LOW: Marcus 정량 진입 기준은 데이터 영역 — 수용.)

---

## 조치 요약 (적용 완료)
| # | 심각도 | 파일 | 조치 |
|---|---|---|---|
| R3-1 | HIGH | G2 | detailed-balance 정합 조건 `eq:ch3_dbconsist`; thermodynamic affinity $\mathcal A^{\mathrm{th}}=RT(V-U)/w_j$; $\chi=\beta$ 동일 구동; $\Pi^0=1$ |
| R4-1 | MED | G2 | Schnakenberg 1976 인용(`eq:ch4_trep`) |
| R4-2 | MED | G1 | AL-8 novelty 정정(메커니즘 grounded) + 3 refs(Macdonald/Lindsey-Patterson/Plonka) |
| R5-2 | LOW | G1 | $d\Theta/dQ$↔$d\Theta_\mathrm{tail}/dq$ bridge + $\rho_G$ 모수형 + 단조성 |
| R7-1 | LOW | G1 | 빠른 kinetics 극한 + single-mode 복귀(M4) |
| R9-1 | LOW | G1 | $Q_p\Theta\equiv\sum_j Q_{j,\tot}\xi_j$ 정의 |
| — | LOW | G2 | dangling marcus bibitem 제거 |

## 검토 후 상태
- 균형: G1 begin/end 27/27, G2 22/22. cite↔bibitem 정합(dangling 0).
- CRIT 잔존 **0**. HIGH(R3-1) 해소. 나머지 MED/LOW 반영 완료.
- **유일했던 hard 검증점(roadmap R2)** = Level A↔B 극한 일치: G2 §reconcile 항등식 + R3-1 정합 조건으로 \emph{이중 확인}.
- 빌드(xelatex/kotex)는 사용자 환경(엔진 부재). 다음: **G3(Ch5~6)** 또는 사용자 검토.

## Correction History
| 일자 | 변경 |
|---|---|
| 2026-05-29 | G1+G2 10-pass 논리 검토. 검색 보완 2건(Schnakenberg, stretched-from-DAE). 발견 7건(HIGH 1: detailed-balance↔effective width 정합; MED 2; LOW 4) 전부 반영. CRIT 0. |
