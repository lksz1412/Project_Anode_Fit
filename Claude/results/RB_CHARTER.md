# RB_CHARTER — Cross-chapter 규약 동결 (Phase 0.1, step 1–5)

> **위치**: RB Phase 0.1. **입력**: `PHASE_A_consolidated_adversarial_review_RESULT.md`, `PHASE_B_crosschapter_build_review_RESULT.md`.
> **목적**: Phase A/B 가 적발한 교차장(cross-chapter) 결함은 \emph{장별로 따로 고치면 재발}한다. 본 charter 가
> 5개 규약을 동결하고, RB Phase 1~7 의 모든 장이 이를 \textbf{상속}한다. 각 규약은 "확인 가능한 조건"
> (`feedback_gate_design_principle`) 으로 기술 — gate `G-cross` 의 판정 기준.
> **계획서**: `Claude/plans/2026-05-30-undergrad-rederivation-rebuild-plan.md` (Implementation Interfaces).

---

## step 1 — 부호 인자 $s_{\phi,j}$ (방전 방향 지시자)

**정의(기준 = Ch3 명시형)**:
$$\mathcal A_j \;=\; s_{\phi,j}\,n_j^{\eff}\,F\,(V_{n,\drive}-U_j), \qquad s_{\phi,j}\in\{+1,-1\}.$$
- $s_{\phi,j}$ 는 transition $j$ 의 방전 방향 부호. 방전 기준 $s_{\phi,j}=+1$ (Ch1~4 기본), 충전 branch 는 Ch5 에서 branch-부호 $s_{\phi,j}^{b}$ 로 일반화.
- **전 장 동일 convention**: $\mathcal A_j$, $\eta_j$, $q_\irr$ 의 부호가 $s_{\phi,j}$ 에 일관 종속.
- **$q_\irr\ge0$ 보장**: $q_\irr=|I|\eta\ge0$ (2법칙). $\eta_j$ 기반 보장이며, 단일 transition 항별 부호는 BOUNDED, 다중 transition 합 $\ge0$ 은 2법칙으로 별도 진술(Phase A Ch2 HIGH 해소).

**확인 가능한 조건 (G-cross-1)**:
- [ ] $\mathcal A_j$ 정의식에 $s_{\phi,j}$ 가 \emph{명시}된다 (verifybox·branch affinity 포함 — Ch4/Ch5 누락이 Phase A HIGH 였음).
- [ ] $q_\irr$ 정의가 $|I|\eta$ 형(부호 양정치) — `I\eta` 단독 금지.
- [ ] Ch5 충전 branch 에서 $n^\eff I_j\eta^b\ge0$ 의 부호 상쇄가 \emph{유도}로 본문에 있다 (주장만 금지).

**적용 장**: Ch1(도입)·Ch3(명시형 기준)·Ch4(verifybox 복원)·Ch5(branch 부호 유도).

---

## step 2 — 구동전위 $V_n$ vs $V_{n,\drive}$ (이중정의 차단)

**정의(기준 = Ch2 `eq:ch2_fluxforce`)**:
- 내부 음극 전위 $V_n$ = 전하보존식의 해(무대).
- 구동전위 $V_{n,\drive}$ = 상변이 속도식·dissipation force 계산에 쓰는 전위. **기본가정 $V_{n,\drive}=V_n$** ($\eta_{n,\drive}=0$).
- dissipation force(과전압) $\eta_j \equiv V_{n,\drive}-V_{\eq,j}(\xi_j)$ — **전 장 $V_{n,\drive}$ 기준으로 통일**.
- 강구동($\eta_{n,\drive}\ne0$) 확장은 BOUNDED(유효범위 병기), 기본 전개에서는 $V_{n,\drive}=V_n$ 사용.

**확인 가능한 조건 (G-cross-2)**:
- [ ] $\eta_j$ 의 기준 전위가 한 문서 내 단일($V_{n,\drive}$) — $V_n$/$V_{n,\drive}$ 혼용 0 (Ch4 의 $V_n$/$V_{n,\drive}$ 이중정의가 Phase A CRITICAL 였음).
- [ ] 미시=거시 정합(Ch4)·detailed balance 대입에서 $V_{n,\drive}=V_n$ 전제가 \emph{명시}된다.
- [ ] $V_{n,\app}$(관측, polarization 포함)·$V_{n,\OCV}$(평형해)·$V_{n,\drive}$(구동) 3종 역할이 구분된다.

**적용 장**: Ch2(기준)·Ch3(V_{n,drive} 정의)·Ch4(이중정의 해소)·Ch5(branch별).

---

## step 3 — effective 전자수 $n_j^{\eff}$ (위계 명문화)

**정의**:
$$n_j^{\eff} \;=\; \frac{RT}{F\,w_j}, \qquad w_j = \text{평형 전이 폭}.$$
- $w_j=RT/F$ (ideal width) 일 때 $n_j^{\eff}=1$.
- **위계(Phase B 가 정합 확인)**: Ch4 = \emph{일반형} $\dot Q_\irr=\sum_j n_j^{\eff}I_j\eta_j$. Ch2 = \emph{특수형}($n^\eff=1$, ideal width). 두 장은 모순이 아니라 일반/특수 위계.
- Ch2 본문에 "이 식은 ideal-width($n^\eff=1$) 가정; 일반형은 Ch4" forward-ref 1줄(Phase B LOW 해소).

**확인 가능한 조건 (G-cross-3)**:
- [ ] $n_j^{\eff}=RT/(Fw_j)$ 정의가 도입 장(Ch3)에 1회, 사용 장에 인용.
- [ ] Ch4 비가역열식에 $n_j^{\eff}$ 명시; Ch2 에 특수형 forward-ref.
- [ ] detailed balance 의 affinity scale 이 $w_j$ 와 정합($\mathcal A_j^{\mathrm{th}}=RT(V-U)/w_j$).

**적용 장**: Ch3(정의)·Ch2(특수형)·Ch4(일반형).

---

## step 4 — keystone: Level A ↔ Level B (한정 명제)

**정의**:
- **Level A (Ch1)**: $\chi_j\mathcal A_j$ = \emph{방향성 없는} relaxation mobility 가속. 평형 target $\xi_{\eq,j}$ 은 열역학 전담(ratio 불변). 진행률 완화 $d\xi_j/dt=k_j(\xi_{\eq,j}-\xi_j)$.
- **Level B (Ch3)**: forward 장벽 $-\beta_j\mathcal A_j$, backward $+(1-\beta_j)\mathcal A_j$ → rate ratio 가 $\mathcal A_j$ 의존. transfer coefficient $\beta_j\equiv\chi_j$ (동일물).
- **★ 한정 명제 (Phase A Ch3 HIGH 해소)**: "Level A = Level B" 를 \emph{무조건} 쓰지 않는다. 정확히는 **Level A 는 Level B 의 detailed-balance 극한**이며, 일치하는 것은 \emph{정상 target} $\xi_{\ss,j}\to\xi_{\eq,j}$ 다(mobility 의 $\mathcal A_j$-의존은 Level B 에서 비대칭, Level A 는 그 대칭 특수극한).

**확인 가능한 조건 (G-cross-4)**:
- [ ] "Level A = Level B" 표현에 항상 "detailed-balance 극한" 또는 "정상 target 일치" 한정어가 붙는다.
- [ ] Ch1 의 "$\xi_\ss\to\xi_\eq$ 극한 일치"(좁은 표현)와 Ch3 의 명제가 동일 입도로 진술된다.
- [ ] $\chi_j\equiv\beta_j$ 동일물 명시; Level A=방향성 X / Level B=방향성 O 구분.

**적용 장**: Ch1(Level A)·Ch3(Level B + 한정)·Ch4·Ch5(Level B 상속).

---

## step 5 — 통합 Assumption Ledger 번호 체계

**규칙**:
- **단일 통합 ledger** (`RB_AL_MASTER.md`, Phase 0.3 골격). 장별 prefix 없이 **AL-1, AL-2, … 연속 번호**.
- 각 AL 항목 = `| AL-# | 가정 진술 | tier | 근거 cite | DOI(검증) | 사용 장·식 |`.
- **tier 3종**: GROUNDED(논문/교과서 확립) / BOUNDED(유효범위 병기) / FLAGGED(미검증 — established 사용 금지, 정직 표기).
- 본문 모든 가정식은 AL-# 인용. **무근거 무리한 가정**(5-30 경고)은 grounding 못 찾으면 FLAGGED, 방향-3(재작성) 트리거.
- Phase A 적발 미정의 AL(Ch3 AL-K1~K3, Ch4 AL-H 계열, Ch1 AL-1~10 dangling)은 본 통합 ledger 에서 \emph{실제 정의} 부여.

**확인 가능한 조건 (G-cross-5 = G-ground 일부)**:
- [ ] AL 번호가 전 장 통합 단일 체계, 충돌 0.
- [ ] 모든 본문 가정식이 AL-# 인용(무태그 established 0건).
- [ ] 각 AL 항목에 tier + 근거 cite + DOI(검증) 또는 정직 FLAGGED.
- [ ] Phase A dangling AL 전부 실제 정의됨.

---

## 동결 요약 (전 장 상속 체크리스트)

| 규약 | 핵심 | Phase A/B 해소 결함 |
|---|---|---|
| 1. $s_{\phi,j}$ | $\mathcal A_j=s_{\phi,j}n^\eff F(V_\drive-U)$ 명시; $q_\irr=|I|\eta\ge0$; Ch5 충전 부호 유도 | Ch4 verifybox·Ch5 branch $s_\phi$ 누락(HIGH); Ch2 부호 양정치(HIGH) |
| 2. $V_{n,\drive}$ | $\eta=V_\drive-V_\eq$ 통일; 기본 $V_\drive=V_n$ 명시; 3전위 구분 | Ch4 $\eta$ 이중정의(CRITICAL) |
| 3. $n_j^\eff$ | $RT/(Fw_j)$; Ch4 일반형/Ch2 특수형 위계 | Ch4 "Ch2=특수형" 모순 주장(HIGH) |
| 4. keystone | Level A = Level B 의 detailed-balance 극한(한정어 필수) | Ch3 "A=B" 과대(HIGH) |
| 5. AL 체계 | 통합 단일 번호 + tier + cite + DOI; 무근거→FLAGGED→재작성 | AL ledger 본체 부재(전장 HIGH); dangling AL(Ch3/Ch4) |

**다음**: Phase 0.2 (references dossier — DOI 검증 워크플로 진행 중) → Phase 0.3 (통합 AL 체계 골격 `RB_AL_MASTER.md`).
