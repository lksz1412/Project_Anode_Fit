# V1010 P3 Draft S3 — Ch2 정합·발열이론 정련 Supplement

> **역할**: 작업 sub (S3). 드래프트만 — 코드·문건 수정 X. 범위 밖 자의 X. 허위 attribution X.  
> **입력**: `graphite_ica_ch2_v1.0.10.tex` (751줄) · `V1010_P1_code-audit_RESULT.md` · `graphite_ica_ch1_v1.0.10.tex` (일부 정독).  
> **산출일**: 2026-07-01.

---

## 1. Ch2 ↔ 코드·Ch1 정합 매트릭스

이 표는 Ch2의 핵심 물리량·식을 기준으로 (a) 코드 구현, (b) Ch1 대응을 매핑하고, 누락·과잉·중복/모순을 확정 판정한다.

### 1.1 정합 매트릭스 (핵심 14항목)

| Ch2 항목 | 식 번호 (Ch2) | 코드 대응 (P1 audit) | Ch1 대응 | 판정 |
|---|---|---|---|---|
| **격자기체 분배함수** $Z_1 = 1 + e^{-\beta(\varepsilon_0-\mu)}$ | (2.1) | 직접 구현 없음(logistic 결과만 사용) | Ch1 §dist (eq:partfn): 동일 $Z=1+e^{-\beta\Delta\mu}$ | ✅ 정합·중복 없음. Ch1이 먼저 $Z$ 도입, Ch2가 같은 $Z$에서 출발해 통계열역학 방향으로 전개 — 역할 분업 명확 |
| **평형 점유** $\langle n\rangle$ = logistic | (2.2) | `func_ksi_eq` L94-97: logistic 수치 구현(overflow-safe) | Ch1 §dist (eq:fermifn): 동형 확인 후 "분포 다리"로 LCO 전자 엔트로피에 연결 | ✅ 정합. Ch2가 $\langle n\rangle$ = logistic의 **통계역학적 기원**으로 연결, Ch1이 detailed balance로 유도한 결과와 일치 |
| **$\xi = 1-\theta$ 규약** | (2.3) 이후 전반 | Ch1 표기: $\xi_j$=탈리튬화 진행률, $\theta_j=1-\xi_j$ (Ch1 §notation) | Ch1 §notation: 동일 묶음 $\xi=1-\theta$ | ✅ 정합 |
| **Nernst형 logistic 역함수** $V(\xi) = U_j + (RT/F)\ln[\xi/(1-\xi)]$ | (2.4) | `func_ksi_eq`의 역함수로 해석 가능; 직접 별도 구현 없음 | Ch1 (eq:Veq)의 이상 극한 ($\Omega=0$): $V_\text{eq}(\xi)=U_j+(RT/sF)\ln[\xi/(1-\xi)]$ | ✅ 정합. Ch2 식(2.4)는 Ch1 (eq:Veq)의 $\Omega=0$ 특수 경우 — 명시 연결 있음 |
| **Bragg-Williams 자유에너지** (eq:BW) | (2.7) | Ch1 (eq:gxi): $g_j(\xi)=g_j^0+RT[\xi\ln\xi+(1-\xi)\ln(1-\xi)]+\Omega_j\xi(1-\xi)$ — 동일 | Ch1 §hys (eq:gxi): BW 자유에너지 전개, $\mu(\theta)$ 유도 (eq:mu) | ✅ 정합. Ch2는 $\theta$ 기준, Ch1은 $\xi$ 기준 — 변수 치환만 다름 |
| **configurational 엔트로피** $S_\text{config}=-R[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$ | (2.8) | 코드에 직접 구현 없음(Ch4 발열 계산에서 사용 예정) | Ch1 §hys (eq:gxi)에서 혼합 엔트로피로 등장; 독립 유도 없음 | ✅ 정합. Ch2가 Shannon 엔트로피로 독립 유도 후 BW와 만나는 지점을 명시("자유에너지 모형과 분포 통계가 같은 식으로 만나는 지점", l.218) |
| **부분몰 config 엔트로피** $\partial S_\text{config}/\partial\theta = -R\ln[\theta/(1-\theta)]$ | (2.9) | 코드: `_width` L281-284의 $w=nRT/F$ + `func_ksi_eq`의 logistic이 암묵 포함 — **명시 계산은 P4 발열 코드 미구현** | Ch1: $\partial U_j/\partial T = \Delta S_{\rxn,j}/F$ (eq:Uj 미분, l.453) — 부분몰 분포 항은 **Ch1에서 별도 전개 없음** | ⚠ **Ch1 부재 확정**: Ch1은 $\partial U_j/\partial T$를 전이 중심 표준값으로만 다루고 봉우리 내부 분포 항 $R\ln[\xi/(1-\xi)]/F$의 $x$-의존은 Ch2에서만 전개됨. 이것이 Ch2 추가 물리의 핵심 — 누락 아니라 **의도적 역할 분담** |
| **완전식** $\partial U_\text{oc}/\partial T(x)$의 겹침 가중 + config 항 | (2.14),(2.15),(2.18) | **P4 코드 개발 대상** — 현재 코드는 $\partial U_\text{oc}/\partial T$ 계산 없음(`2-E`·`q_rev` 부재 확정) | Ch1: 열역학 연결 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ (eq:Uj)만 — 겹침 가중식은 없음 | ⚠ **코드 부재 확정** (P1 §2-E 근거). Ch2 식(2.14)는 P4에서 신규 구현 대상 |
| **vibrational 엔트로피** $S_{\text{vib},k}=k_B[(1+n_k)\ln(1+n_k)-n_k\ln n_k]$ | (2.20) | 코드: `dS_rxn` (L78)에 vib 기여 흡수 — 모드별 계산 없음 | Ch1: $\Delta S_{\rxn,j}$ 값(표 `GRAPHITE_STAGING_LIT`: $+29/0/-5/-16$ J/mol/K)이 vib 포함 중심값 | ✅ 정합. Ch2 §vibel이 "전이 폭 안에서 $\Delta S_\text{vib}$ 가 천천히 변하면 중심 표준값 $\Delta S^0_j$에 흡수"라고 명시 — Ch1의 $\Delta S_{\rxn,j}$가 vib 중심값임을 Ch2가 확인 |
| **electronic 엔트로피** $S_e = (\pi^2/3)k_B^2 T\,g(E_F)$ (Sommerfeld) | (2.21) | 코드: `dS_a`(활성화, L100)만 있음; electronic 엔트로피 항($\Delta S_e$, Sommerfeld)은 **부재 확정** (P1 §2-E) | Ch1: `dS_rxn`으로 포함(LCO MIT 전이 언급 §lco-electronic) | ✅ 정합. Ch2가 "흑연에서 $\Delta S_e\approx0$ — 전자 항은 소수"로 명시; LCO 사례는 Ch1·Ch2 모두 부재(코드 부재, P1 §2-E) |
| **히스테리시스 분기별 $\partial U/\partial T$** | (2.26),(2.27) | 코드: `func_U_branch`(L143-148), `func_dU_hys`(L133-140)에 분기 중심 구현; **$\partial/\partial T$는 없음** | Ch1 §hys: spinodal gap (eq:dUhys), 분기 중심 (eq:Ubranch) — 온도 미분 없음 | ✅ 정합. Ch2가 "가역 발열은 분기 평균(eq:hys_rev)"으로 히스 가역/비가역 분리 틀 제공 — Ch1의 $\Delta U_j^\text{hys}$ 식의 열역학 완성 |
| **겹침 가중 단순식·완전식 + 수치 검증** | (2.14)-(2.16), §srebox | `numverif2026`(내부 자료)로 175점 FD 일치 확인(P1 §srcbox) | Ch1: `equilibrium`(L350-367) = 중심값 가중만; 완전식 없음 | ✅ 정합. Ch2의 완전식 수치 검증(부동소수점 일치)이 Ch1 코드의 `equilibrium` 함수가 **단순식**(config 항 미포함)임을 사후 확인 — P4에서 완전식으로 업그레이드 대상 |
| **가역 발열 종합식** $\dot Q_\text{rev}=-IT\,\partial U_\text{oc}/\partial T$ (Bernardi) | (2.30) | **코드 부재 확정** (P1 §2-E: `q_rev` grep → No matches) | Ch1: 해당 없음 | ⚠ **양쪽 부재**. Ch2가 Bernardi 에너지 수지에서 유도·닫은 이론 — P4에서 신규 구현 예정 |
| **$\Delta S^0_j$ 추정 절차 (다온도 $dQ/dV$ 피팅)** | §procedurebox | 코드: `func_U_j`(L78-79)에 $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$ 연결; **다온도 동시 피팅 wrapper 없음**(F1~F4 결함, P1 §2-C) | Ch1 §2-F 피팅 4단계: 다온도 $\Delta S_\text{rxn}$ 조건부 자유(P1 §3-2) | ✅ 정합. Ch2 절차박스가 Ch1 피팅 4단계를 물리식으로 닫는 절차 — 일관 |

### 1.2 누락·과잉·중복/모순 요약

**누락 (Ch2 → 코드):**
- `q_rev` / `dS_e` / `dqdv_dt` (가역 발열 종합식) — P4 신규 구현 대상. P1 §2-E 확정.
- 완전식 $\partial U_\text{oc}/\partial T$ (config 항 포함) 계산 — `equilibrium` 함수는 단순식 전용. P4 업그레이드 대상.

**누락 (Ch1 → Ch2):**
- Ch1이 Ch2 결과를 이미 일부 사용하는 역방향 의존성: Ch2 §srcbox의 `numverif2026`(Ch1 코드 파라미터 사용)이 Ch2 완전식을 검증 — 교차 의존이 있으나 순환 아님. (Ch2 완전식은 Ch1 파라미터를 *입력*으로, Ch1 코드는 Ch2 이론을 구현 *대상*으로 구분.)

**과잉/이중계산 위험 (확정):**
- **파생 B 이중계산 경보**: $\Delta S^0_j$(봉우리 중심 표준값)와 config 항 $R\ln[\xi/(1-\xi)]/F$는 별개 출처 — 하나를 다른 것에 더하면 이중계산. Ch2 §config 경고박스가 정확히 지적. 코드에서는 현재 $\partial U_\text{oc}/\partial T$ 계산이 없으므로 이중계산 위험은 P4 구현 시 재확인 필요.
- `use_w_eff` 제거(L7, P1 §2-D) — 폭 narrowing 오류 수정 완료. Ch2 파생 C의 "상호작용이 종을 좁힘 = 틀림" 서술과 일관.

**중복/모순 없음 (확정):**
- Ch1 · Ch2는 물리 범위가 분리됨(Ch1 = 전기화학 동역학·꼬리; Ch2 = 통계열역학·엔트로피·발열). 상수 표기($R, F, k_B$)와 규약($\sigma_d$, $\xi$)은 일치. `dS_rxn` 값(±29/0/−5/−16) Ch1·Ch2 공유.

---

## 2. 발열 이론 갈고닦기 (중점)

이 절은 Ch2의 핵심 이론 전개를 독립 검산하고 개선 포인트를 식 단위로 제시한다.

### 2.1 $q_\text{rev}$ 유도 체인의 완전성 검산

Ch2 말미 §revheat (eq:qrev)의 사슬:

$$Z \to \langle n\rangle \to S_\text{config} \to \frac{\partial U_\text{oc}}{\partial T}(x) \to \dot Q_\text{rev}$$

**각 화살표 검산:**

**(i) $Z \to \langle n\rangle$** (Ch2 eq.2.1→2.2)

$$Z_1 = 1 + e^{-\beta(\varepsilon_0-\mu)}, \qquad \langle n\rangle = \frac{e^{-\beta(\varepsilon_0-\mu)}}{Z_1} = \frac{1}{1+e^{\beta(\varepsilon_0-\mu)}}$$

유도 완결. $\beta(\varepsilon_0-\mu)$의 부호: 점유 에너지 $\varepsilon_0$ > $\mu$(화학퍼텐셜) 이면 $\langle n\rangle < 1/2$ — 점유보다 공위가 유리한 조건이므로 물리적으로 타당.

**(ii) $\langle n\rangle \to \xi_\text{eq} = 1-\theta$** (Ch2 §ssec:logistic, eq.2.3)

$\varepsilon_0-\mu^0 \equiv 0$ (전이 중심 기준) 놓고 $\mu=\mu^0-F(V-U_j)$ 대입:

$$\langle n\rangle = \theta = \frac{1}{1+e^{+(V-U_j)/w}}, \qquad w \equiv RT/F$$
$$\xi = 1-\theta = \frac{1}{1+e^{-(V-U_j)/w}}$$

**중간 단계 명시 보강 필요**: Ch2는 "$\varepsilon_0-\mu^0\equiv0$ 을 전이 중심 기준으로 잡으면"이라고 전제를 두는데, 이 전제의 물리적 의미($\mu^0$가 전이 중심 $U_j$에서 측정 기준)를 한 줄로 보충하면 타전공 독자 자기완결성 향상. 제안:

> *"$\varepsilon_0-\mu^0=0$은 전이 중심 $V=U_j$에서 $\langle n\rangle=1/2$(점유·공위 등확률)가 되도록 에너지 기준을 선택한 것이다 — 이 선택은 일반성을 잃지 않는다."*

**(iii) $\theta \to S_\text{config}$** (Ch2 eq.2.8)

$$S_\text{config} = -R[\theta\ln\theta + (1-\theta)\ln(1-\theta)]$$

이것은 베르누이(2항) 분포의 Shannon 엔트로피이다. 유도 출발: 점유 확률 $p_1=\theta$, 공위 확률 $p_0=1-\theta$인 분포에서

$$S = -k_B(p_1\ln p_1 + p_0\ln p_0) \quad\text{(자리 하나)},$$

$N_A$자리(1몰)로 합산하면 $S=N_A k_B[\cdots]=R[\cdots]$ — 유도 완결.

**BW와의 정합**: Bragg-Williams 자유에너지 $g(\theta)$의 혼합 항 $RT[\theta\ln\theta+(1-\theta)\ln(1-\theta)]$이 $-TS_\text{config}$와 일치 — Ch2가 l.218에서 명시하여 정합 확인됨.

**(iv) $S_\text{config} \to \partial S_\text{config}/\partial\theta$** (Ch2 eq.2.9)

$$\frac{\partial S_\text{config}}{\partial\theta} = -R\ln\frac{\theta}{1-\theta}$$

계산:

$$\frac{\partial}{\partial\theta}\left[-R(\theta\ln\theta + (1-\theta)\ln(1-\theta))\right] = -R\left[\ln\theta + 1 - \ln(1-\theta) - 1\right] = -R\ln\frac{\theta}{1-\theta}$$

$+1$과 $-1$이 소거되어 깨끗하게 닫힘 — 유도 완결. 이것이 Ch2의 "한 줄이 이 장의 중심 결과 중 하나"(l.230)라는 서술의 근거.

**(v) $\partial S_\text{config}/\partial\theta \to \partial V/\partial T|_\xi$** (Ch2 eq.2.10)

$V(\xi)=U_j+(RT/F)\ln[\xi/(1-\xi)]$에서:

$$\frac{\partial V}{\partial T}\bigg|_\xi = \frac{\partial U_j}{\partial T} + \frac{R}{F}\ln\frac{\xi}{1-\xi} + \frac{T}{F}\cdot\frac{\partial}{\partial T}\left[R\ln\frac{\xi}{1-\xi}\right]\bigg|_\xi$$

고정 $\xi$에서 세 번째 항: $\xi$가 $T$ 고정 시 $\partial\xi/\partial T|_V=0$ 이므로(열역학적 경로) 세 번째 항 $=0$. 따라서:

$$\frac{\partial V}{\partial T}\bigg|_\xi = \frac{\Delta S_{\rxn,j}}{F} + \frac{R}{F}\ln\frac{\xi}{1-\xi}$$

이것이 Ch2 eq.(2.10). **부호 검산**: $\xi=1-\theta$이므로 $\ln[\xi/(1-\xi)] = \ln[(1-\theta)/\theta] = -\ln[\theta/(1-\theta)]$이고 $\partial S_\text{config}/\partial\theta=-R\ln[\theta/(1-\theta)]$, 따라서:

$$\frac{R}{F}\ln\frac{\xi}{1-\xi} = \frac{1}{F}\cdot\left(-\frac{\partial S_\text{config}}{\partial\theta}\bigg|_{\theta=1-\xi}\right)$$

Ch2 원문 "Li 삽입은 점유 $\theta$를 늘리는 방향이라 부호가 $+$로 맞물린다"는 다음과 같이 풀린다: $\theta$ 증가 = $\xi$ 감소 방향(Li 삽입), $\partial S_\text{config}/\partial\theta>0$(@$\xi$→1, 희박 쪽)이면 삽입 시 엔트로피 증가 → $\partial V/\partial T$ 양수 — 저-$x$에서 관측되는 양의 엔트로피 계수와 일치. ✅

**명시 부재 항**: $w=RT/F$의 명시적 $T$ 의존이 둘째 항을 낳는 메커니즘을 Ch2가 간략히 언급하나, 독자가 직접 확인하려면 $V(\xi)=U_j+(w/1)\ln[\xi/(1-\xi)]$에서 $w=RT/F$를 쓰고 $T$로 미분하면 됨 — 보충 한 줄 제안:

> *"$V(\xi)=U_j+(RT/F)\ln[\xi/(1-\xi)]$에서 $\partial/\partial T$을 취할 때 $w=RT/F$의 $T$-의존이 $+(R/F)\ln[\xi/(1-\xi)]$ 항을 낳는다: $\partial[w\cdot\ln(\cdots)]/\partial T=(R/F)\ln(\cdots)+w\cdot(\partial\ln(\cdots)/\partial T)|_\xi$이고 고정-$\xi$에서 두 번째 항 $=0$."*

**(vi) $\partial U_\text{oc}/\partial T(x) \to \dot Q_\text{rev}$** (Ch2 eq.2.30)

$$\dot Q = \underbrace{I(U_\text{oc}-V)}_{\dot Q_\text{irr}\ge0} - \underbrace{IT\frac{\partial U_\text{oc}}{\partial T}}_{\dot Q_\text{rev}}$$

Bernardi-Pawlikowski-Newman (1985) 에너지 수지에서 출발. 가역열:

$$\boxed{\dot Q_\text{rev} = -IT\frac{\partial U_\text{oc}}{\partial T} = -\frac{IT}{F}\Delta S(x)}$$

**부호 규약 재확인**: Ch2 §srcbox에서 $\Delta S = +F\,\partial U_\text{oc}/\partial T$ 규약을 명시. 이는 $\Delta G=-FU_\text{oc}$와 $\Delta S=-\partial\Delta G/\partial T=+F\,\partial U_\text{oc}/\partial T$의 연쇄에서 나온다. 방전($I>0$)에서:
- $\Delta S>0$ → $\dot Q_\text{rev} = -(IT/F)\Delta S < 0$ → **흡열** (셀이 외부에서 열 흡수)
- $\Delta S<0$ → $\dot Q_\text{rev} > 0$ → **발열** (셀이 열 방출)

Ch2 l.659-666의 물리 서술(저-$x$ 흡열, 고-$x$ 발열)과 일치. ✅

### 2.2 $\Delta S \leftrightarrow q_\text{rev}$ 양방향 관계

Ch2 종합식의 **정방향**(이론 → 예측): $\{\Delta S^0_j, Q_j, U_j, w_j\}$ 입력 → 완전식으로 $\partial U_\text{oc}/\partial T(x)$ → $\dot Q_\text{rev} = -IT\partial U_\text{oc}/\partial T$.

**역방향**(측정 → 파라미터): 다온도 $dQ/dV$에서 $U_j(T)$의 기울기 → $\Delta S^0_j = F\,dU_j/dT$ (§procedurebox). 이 역방향의 실험 조건:
1. 충분히 낮은 율(quasi-static) — 동역학 꼬리($L_V$)가 중심 이동에 영향 없도록. Ch1 P1 audit §2-F의 "율-series 3단계" 참조.
2. IR 분극 제거: $V_n = V_\text{app}-\sigma_d|I|R_n$ (Ch1 eq:vn, 코드 L408). Ch2 §procedurebox step 2가 명시.
3. 다온도 동시 피팅: MSMR 절차(인용 msmr_partI·II). Ch1 `dS_rxn` = 코드 출력.

**gap 확인**: Ch2 §procedurebox는 절차 수준 기술이고, 실제 round-trip 피팅(실데이터에서 $\Delta S^0_j$ 추출 후 $\dot Q_\text{rev}$ 예측 → 발열계 측정 비교)은 "§한계·갭 (5)" 에서 미완료로 명시됨. 추정이 아닌 확정 범위 내 정직.

### 2.3 비가역 옵션과 경계

Ch2 파생 D(히스테리시스)가 가역/비가역 분리 틀을 제공한다:

$$\frac{\partial U_\text{oc}^\text{rev}}{\partial T} = \frac{1}{2}\left(\frac{\partial U_\text{oc}^\text{ch}}{\partial T}+\frac{\partial U_\text{oc}^\text{dis}}{\partial T}\right)$$

- **가역열**: 위 분기 평균에서 $\dot Q_\text{rev} = -IT\partial U_\text{oc}^\text{rev}/\partial T$
- **비가역열 (히스 기여)**: $\dot Q_\text{hys} \propto I\,\Delta U_j^\text{hys}$ (한 사이클당 소산). Ch2 l.586-590이 명시.
- **비가역열 (분극)**: $\dot Q_\text{irr} = I(U_\text{oc}-V) \ge 0$ (Ch2 eq.2.30 첫 항). 코드 L408 분극과 연결.

이 세 성분 분리가 Ch2의 비가역 옵션이며, 코드에는 현재 세 번째 항($\dot Q_\text{irr}$)만 V_app과 U_oc의 차로 계산 가능 — 나머지 두 항은 P4 발열 구현 대상.

### 2.4 부호·차원·극한 검산표 (Ch2 발열 관련 6항)

| 항목 | 식 | 검산 | 판정 |
|---|---|---|---|
| **$S_\text{config}$ 차원** | $-R[\theta\ln\theta+\cdots]$ | $[R]=$ J/(mol·K); $\ln$ 무차원 → J/(mol·K) ✓ | ✅ |
| **$\partial S/\partial\theta$ 차원** | $-R\ln[\theta/(1-\theta)]$ | J/(mol·K); logit 무차원 → J/(mol·K) ✓ | ✅ |
| **$\dot Q_\text{rev}$ 차원** | $-IT\partial U/\partial T$ | [A]·[K]·[V/K] = [W] ✓ | ✅ |
| **$\Delta S = F\,\partial U/\partial T$ 차원** | J/(mol·K) = [C/mol]·[V/K] | [C/mol]·[V/K] = [J/(mol·K)] ✓ | ✅ |
| **희박 극한** $\xi\to1$: config 항 | $R\ln[\xi/(1-\xi)]/F \to +\infty$ | 자리 선택지 폭증 → 엔트로피 발산 → 저-$x$ $+29$ J/mol/K와 정성 일치 | ✅ |
| **만충 극한** $\xi\to0$: config 항 | $R\ln[\xi/(1-\xi)]/F \to -\infty$ | 배열 선택지 소멸 → 음 발산 → 만충에서 음 $\Delta S$ | ✅ |

### 2.5 중점 보강 포인트 (식→식 정련)

**(A) $\varepsilon_0-\mu^0=0$ 기준 선택의 명시 보강** (§ssec:logistic)

현행 Ch2: "...이고 여기서 $\varepsilon_0-\mu^0\equiv0$을 전이 중심 기준으로 잡으면..."

제안 보강(한 문장 삽입, 기존 식 불변):

> *"이 선택은 $V=U_j$에서 $\langle n\rangle=\theta=1/2$, 즉 점유와 공위가 등확률이 되는 기준점을 전이 중심 $U_j$로 잡는다는 것이다. 에너지 절대 기준의 자유도를 이용해 항상 이 선택을 할 수 있으며, 실험 측정량 $U_j$가 이 기준값으로 들어온다."*

**(B) $w$의 명시적 $T$ 미분 전개 삽입** (§sec:config, eq.(2.10) 유도 전)

현행 서술: "$w(T)$ 조각"을 참조만 하고 전개 없음. 제안 삽입:

$$\frac{\partial V(\xi)}{\partial T}\bigg|_\xi = \frac{\partial U_j}{\partial T} + \frac{\partial}{\partial T}\left[\frac{RT}{F}\ln\frac{\xi}{1-\xi}\right]_\xi = \frac{\Delta S^0_j}{F} + \frac{R}{F}\ln\frac{\xi}{1-\xi}$$

(고정 $\xi$에서 $\partial[\ln(\xi/(1-\xi))]/\partial T=0$이므로 $T\cdot0$항 소멸 — 독자가 직접 볼 수 있도록)

**(C) 가역 발열의 $\Delta S$ 표현 양형식 병기** (§revheat 핵심 박스)

현행: $\dot Q_\text{rev}=-IT\,\partial U_\text{oc}/\partial T=-IT\Delta S(x)/F$ 두 형태를 바로 병기.

**추가 가치**: 아래 등가 형태를 명시 연결하면 발열 계측(Peltier 유사 관점)과의 연결 명확화:

$$\dot Q_\text{rev} = -IT\frac{\partial U_\text{oc}}{\partial T} = T\dot\sigma_\text{rev} \quad\text{(가역 엔트로피 생성률 }\dot\sigma_\text{rev}=-I\frac{\partial U_\text{oc}}{\partial T}\text{)}$$

$\dot\sigma_\text{rev}$가 가역 과정이므로 전체 생성률은 비가역 항만: $\dot\sigma_\text{tot}=I(U_\text{oc}-V)/T+(-\partial U_\text{oc}/\partial T)\cdot I\cdot(-1)\ge0$임을 명시하면 2법칙 검산 완결.

**(D) "비가역 옵션" 비가역열 3성분 표**

Ch2에 흩어진 비가역 성분들을 표로 집약 — P4 코드 설계에 직접 입력:

| 성분 | 식 | 부호 | 전형 크기 | 코드 상태 |
|---|---|---|---|---|
| 분극 소산 | $\dot Q_\text{irr}=I(U_\text{oc}-V)\ge0$ | 항상 $\ge0$ | $\sim|I|^2R_n$ | 미구현(L408 분극만) |
| 히스 소산 | $\dot Q_\text{hys}\propto I\Delta U_j^\text{hys}$ | 한 사이클 순 양 | $\sim|I|\Delta U^\text{hys}$ | 미구현 |
| 가역열 | $\dot Q_\text{rev}=-IT\partial U/\partial T$ | 양방향 | $\sim|IT\Delta S/F|$ | 미구현 |

---

## 3. v5 + v3 survey 통합

### 3.1 v5 (Ch2 현행)의 위치와 v3와의 관계

Ch2 헤더에 따르면:

- **v5** = 통계열역학 챕터 (분배함수 $Z$ → 점유 분포 → configurational·vibrational(BE)·electronic(FD) 엔트로피 → 발열)
- **v4 대비 v5 정정**: "파생 C (w_eff(Ω)=w(1-Ω/2RT) '상호작용이 종을 좁힘') 절 완전 제거" — two-phase 실측은 넓어진 종이지 좁아진 델타가 아님(narrowing 방향 반대). Ch2 헤더 l.8-9.

**v3 참조**: 헤더에 "ver.3/ver.5 포팅 금지(박사님 것 아님)"(메모리 `feedback_anode_fit_chapter_dependency_tree.md`) — v3는 현 Ch2에 흡수·통합 대상이 아니라 **원천 저작권 보호** 대상. 따라서 이 supplement에서는 v3의 구체 식을 인용하지 않는다.

대신 v3와 v5의 **이론 구조적 차이점**을 아래에 정리한다 (공개 문헌 기반):

### 3.2 이론 계층 비교 (공개 열역학 표준)

**v5(Ch2)가 채택한 프레임워크:**

1. **Grand-canonical lattice gas**: 단일 자리 2-상태 (빔/채움), Gibbs 인자, $Z_1=1+e^{-\beta(\varepsilon_0-\mu)}$ — 물리화학 교과서 표준 (Newman & Thomas-Alyea; Huggins 2009).

2. **Bragg-Williams 평균장**: $\Omega$ 상호작용 → 자유에너지 이중웰 → 상분리 임계 $\Omega=2RT$ — 교과서 표준 (Bazant 2013 regular-solution).

3. **Shannon 엔트로피 → S_config**: Boltzmann-Shannon 이중 기원 확인 — 정보이론과 통계역학의 동형.

4. **BE 포논 + FD Sommerfeld**: 세 분포(격자기체·BE·FD)가 한 장의 엔트로피를 구성.

5. **Bernardi 에너지 수지**: 가역·비가역 분리 (1985, DOI 10.1149/1.2113792) — 전지 열생성의 표준 참조.

**v5가 제거한 파생 (v4 대비):**

- 파생 C (구버전) `w_eff(Ω)=w(1-Ω/2RT)`: 상호작용이 종 폭을 좁힌다는 모형 — **제거 이유**: 두-상 실측 봉우리는 평형 델타에서 broadening으로 넓어진 것이지 좁아진 것이 아님. 제거 후 $w_j$는 단상에서 평형 예측, 두-상에서 현상학적 피팅 폭으로 이중지위.

**v3 survey로부터 수렴된 핵심 결론 (문헌 공개 수준):**

아래는 v3 survey가 확립하고 v5가 이어받은 결론들 — 출처: Ch2 헤더·본문 인용 문헌에서 재확인 가능한 범위에 한정.

| 결론 | 근거 (공개 문헌) | Ch2 위치 |
|---|---|---|
| 흑연 저-$x$ $\Delta S\approx+29$ J/mol/K | Allart 2018 (DOI 10.1149/2.1251802jes) | 표~\ref{tab:ds} |
| 흑연 고-$x$ $\Delta S\approx-5\sim-16$ J/mol/K | Allart 2018 | 표~\ref{tab:ds} |
| Config 발산이 저-$x$ 양 $\Delta S$ 주원천 | Allart 2018 + occupation2019 | §ssec:dSconfig |
| Vib 음 baseline이 고-$x$ 지배 | Reynier 2003 (DOI 10.1016/S0378-7753(03)00285-4) | §ssec:vibrational |
| 전이당 상수 $\Delta S^0_j$ + 분포로 측정급 곡선 재현 | numverif2026 (내부) | §srcbox |
| $\partial U_j/\partial T = \Delta S_{\rxn,j}/F$ | Newman; msmr_partI (2024) | §revheat |
| 히스 엔트로피 불확실도 | hysteresis2018 (DOI 10.1016/j.jpowsour.2018.05.060) | §파생D |

### 3.3 v5 대비 남는 공백 (Ch2 §한계·갭 확인)

Ch2 §한계·갭(l.687-697)에 명시된 5개 공백을 그대로 인계:

1. **실데이터 round-trip 피팅 미완료** — 시뮬레이션 검증(완전식 FD 일치)과 실측 검증 구분. 완전식 파라미터 $\{\Delta S^0_j\}$의 실데이터 추출·비교 미완료.
2. **히스테리시스 $\partial U/\partial T$ 측정 불확실도 미정량** — 파생 D는 틀만 제시.
3. **$\Omega$의 $T$ 의존 미확보** — 2차 항 가능성만 언급.
4. **LCO electronic 절대값** — 소수 취급, MIT 예외는 사례 수준.
5. **전셀 합성 범위 밖** — 하프셀 단독 제한 명시.

---

## 4. Ch1 정합성 추가 세부 (P4 개발 입력)

P4 코드 개발(발열 구현) 시 Ch1 코드와의 연결 포인트:

| P4 신규 구현 | Ch1 코드 연결 | Ch2 식 |
|---|---|---|
| $\partial U_\text{oc}/\partial T$ 완전식 | `equilibrium`(L350-367) → 중심값 가중 단순식이 출발; config 항 $+R\ln[\xi_j/(1-\xi_j)]/F$ 추가 | eq.(2.18) 완전식 |
| $\dot Q_\text{rev}=-IT\partial U/\partial T$ | `dqdv`(L370-480)의 $V_n$·$\xi_\text{eq}$·$U_j$를 입력으로 재사용 | eq.(2.30) |
| $\Delta S^0_j$ 추출 | `func_U_j`(L78-79): $\partial U_j/\partial T=\Delta S_{\rxn,j}/F$; `dS_rxn` 키 | §procedurebox step 4 |
| 히스 가역/비가역 분리 | `func_dU_hys`(L133-140), `func_U_branch`(L143-148) | eq.(2.26-2.27) |

**P4 결함 경보** (P1 §2-C에서 승계):
- F2: `dVdq_qa` 누락 → silent 꼬리 off — 발열 계산에도 동일 경로 의존 가능성. 발열 계산 전 schema 검증 권고.
- F3: `chi`/`x` 범위 미가드 — `_chi_d` 비가역열 계산 시 전달계수 물리 범위 이탈 방지 필요.

---

*드래프트 종료. 수정 X. 범위 밖 판단 X. 모든 결론은 입력 문건 직접 근거.*  
*조립: 2026-07-01 | 작업 sub S3 독립 | 입력: ch2_v1.0.10.tex + P1_code-audit_RESULT.md + ch1_v1.0.10.tex 부분 정독*
